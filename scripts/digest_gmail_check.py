"""Digest Step 3 Gmail check (Spencer, 2026-10-08: the 10-08 digest stopped at 0/~150 rows because
the per-row check had no committed script, and an ad-hoc temp-key script was blocked).

READ-ONLY. Only GET requests, through the FGAC proxy, with a FGAC temporary key that has exactly the
connector's own permissions. Never sends, writes, labels or deletes anything. Never prints the key.

What it does (DIGEST-ROUTINE-PROMPT.md Step 3a/3b/3c/3e in one run):
  - reads the "Outreach Tracker" tab; active row = has an email and Status is not Dropped / Left Company
  - per unique address: latest inbound (date, subject), latest outbound from Spencer (date, subject),
    out-of-office replies (subject + snippet, for the return date), drafts addressed to it
  - bounces: mailer-daemon / postmaster messages that name the address
  - new contacts: addresses in Inbox/Sent from the last 3 days that are not in the tracker
  - coverage: CHECKED vs ACTIVE, and the rows that failed

Usage (key from FGAC create_temporary_api_key, purpose bulk_calls, ttl 30):
    1. Write tool: put the key alone in local/.fgac_key (local/ is gitignored; mkdir -p local first)
    2. python scripts/digest_gmail_check.py [--out digest_gmail.json]
The script deletes local/.fgac_key when it finishes, pass or fail.
Prints a compact per-row summary; full JSON goes to --out (default: digest_gmail.json in the temp dir).
"""
import argparse, json, os, re, sys, tempfile, time, urllib.error, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor
from email.utils import parsedate_to_datetime

KEY_FILE = os.environ.get("KEY_FILE") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "local", ".fgac_key")
K = os.environ.get("K") or (open(KEY_FILE).read().strip() if os.path.exists(KEY_FILE) else "")
if not K:
    sys.exit("No key: write the FGAC temporary key to local/.fgac_key (gitignored) first.")
BASE = "https://fgac.ai/api/proxy/"
SHEET = "1SBauz4dCodqnfSVD5yqKETjU-25TY5HEZ7KRGggbgT0"
ME = "spencer@spencerzvoice.com"
INACTIVE = {"dropped", "left company"}
OOO = re.compile(r"out of (the )?office|automatic reply|auto(matic)?[- ]?reply|autoreply|away from|on leave|vacation", re.I)


def get(path, params=None):
    url = BASE + path + ("?" + urllib.parse.urlencode(params, doseq=True) if params else "")
    for attempt in range(6):
        try:
            req = urllib.request.Request(url, headers={"Authorization": "Bearer " + K})
            return json.load(urllib.request.urlopen(req, timeout=60))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < 5:
                time.sleep(2 ** attempt)
                continue
            raise
        except urllib.error.URLError:
            if attempt < 5:
                time.sleep(2 ** attempt)
                continue
            raise


def ids(q, n):
    return [m["id"] for m in get("gmail/v1/users/me/messages", {"q": q, "maxResults": n}).get("messages", [])]


def meta(mid):
    m = get(f"gmail/v1/users/me/messages/{mid}",
            {"format": "metadata", "metadataHeaders": ["From", "To", "Cc", "Date", "Subject"]})
    h = {x["name"].lower(): x["value"] for x in m.get("payload", {}).get("headers", [])}
    try:
        date = parsedate_to_datetime(h.get("date", "")).date().isoformat()
    except Exception:
        date = time.strftime("%Y-%m-%d", time.gmtime(int(m.get("internalDate", 0)) / 1000))
    return {"id": mid, "thread": m.get("threadId"), "date": date, "from": h.get("from", ""), "to": h.get("to", ""),
            "cc": h.get("cc", ""), "subject": h.get("subject", ""), "snippet": m.get("snippet", ""),
            "labels": m.get("labelIds", [])}


def check(addr):
    inbound = [meta(i) for i in ids(f"from:{addr} -in:drafts", 5)]
    outbound = [meta(i) for i in ids(f"from:me to:{addr} -in:drafts", 2)]
    ooo = [m for m in inbound if OOO.search(m["subject"]) or OOO.search(m["snippet"][:200])]
    real_in = [m for m in inbound if m not in ooo]
    pick = lambda ms: {k: ms[0][k] for k in ("date", "subject", "thread")} if ms else None
    return {"latest_inbound": pick(real_in), "latest_outbound": pick(outbound),
            "ooo": [{"date": m["date"], "subject": m["subject"], "snippet": m["snippet"][:240]} for m in ooo[:2]]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(tempfile.gettempdir(), "digest_gmail.json"))
    ap.add_argument("--workers", type=int, default=6)
    a = ap.parse_args()

    vals = get(f"sheets/v4/spreadsheets/{SHEET}/values/" + urllib.parse.quote("'Outreach Tracker'!A1:L1000")).get("values", [])
    rows = []
    for n, r in enumerate(vals[1:], start=2):
        r = r + [""] * (12 - len(r))
        email = r[3].strip().lower()
        if email and "@" in email and r[6].strip().lower() not in INACTIVE:
            rows.append({"row": n, "name": r[0], "company": r[1], "email": email, "status": r[6],
                         "sheet_last_contact": r[8], "flag": r[10]})
    addrs = sorted({r["email"] for r in rows})

    results, errors = {}, {}
    def run(addr):
        try:
            results[addr] = check(addr)
        except Exception as e:
            errors[addr] = f"{type(e).__name__}: {e}"[:200]
    with ThreadPoolExecutor(a.workers) as ex:
        list(ex.map(run, addrs))

    # Bounces: one sweep of delivery-failure notices, matched to tracker addresses by snippet/subject.
    bounces = {}
    for i in ids("from:(mailer-daemon OR postmaster) OR subject:(undeliverable OR \"delivery status notification\")", 300):
        m = meta(i)
        text = (m["snippet"] + " " + m["subject"]).lower()
        for addr in addrs:
            if addr in text and (addr not in bounces or m["date"] > bounces[addr]["date"]):
                bounces[addr] = {"date": m["date"], "subject": m["subject"]}

    # Drafts addressed to each tracker address (Step 3b).
    drafts = {}
    all_drafts = get("gmail/v1/users/me/drafts", {"maxResults": 500}).get("drafts", [])
    for d in all_drafts:
        m = meta(d["message"]["id"])
        for addr in re.findall(r"[\w.+'-]+@[\w-]+(?:\.[\w-]+)+", (m["to"] + " " + m["cc"]).lower()):
            drafts.setdefault(addr, []).append({"draft_id": d["id"], "subject": m["subject"]})

    # New contacts in the last 3 days not in the tracker (Step 3c).
    known = set(addrs) | {r[3].strip().lower() for r in vals[1:] if len(r) > 3}
    skip = re.compile(r"no-?reply|mailer-daemon|postmaster|notification|voices\.com|bodalgo|voice123|google\.com|calendar", re.I)
    new = {}
    for i in ids("newer_than:3d (in:inbox OR in:sent) -in:drafts -category:promotions -category:social", 200):
        m = meta(i)
        field = m["to"] + " " + m["cc"] if ME in m["from"].lower() else m["from"]
        for addr in re.findall(r"[\w.+'-]+@[\w-]+(?:\.[\w-]+)+", field.lower()):
            if addr != ME and addr not in known and not skip.search(addr):
                new.setdefault(addr, {"date": m["date"], "subject": m["subject"],
                                      "direction": "out" if ME in m["from"].lower() else "in"})

    for r in rows:
        r["gmail"] = results.get(r["email"])
        r["bounce"] = bounces.get(r["email"])
        r["drafts"] = drafts.get(r["email"], [])
        r["error"] = errors.get(r["email"])
    checked = [r for r in rows if r["gmail"] is not None]
    out = {"run_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "ACTIVE": len(rows), "CHECKED": len(checked),
           "not_checked": [{"row": r["row"], "name": r["name"], "email": r["email"], "error": r["error"]} for r in rows if r["gmail"] is None],
           "drafts_total": len(all_drafts), "rows": rows, "new_contacts_3d": new}
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=True)

    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    for r in rows:
        g = r["gmail"] or {}
        li, lo = g.get("latest_inbound"), g.get("latest_outbound")
        print(f"r{r['row']} | {r['name']} | {r['company']} | {r['email']} | sheet:{r['status']}/{r['sheet_last_contact']}"
              f" | IN:{li['date'] + ' ' + li['subject'][:50] if li else '-'}"
              f" | OUT:{lo['date'] + ' ' + lo['subject'][:50] if lo else '-'}"
              + (f" | OOO:{g['ooo'][0]['date']}" if g.get("ooo") else "")
              + (f" | BOUNCE:{r['bounce']['date']}" if r["bounce"] else "")
              + (f" | DRAFT x{len(r['drafts'])}" if r["drafts"] else "")
              + (f" | ERROR:{r['error']}" if r["error"] else ""))
    if new:
        print("\nNEW CONTACTS (last 3 days, not in tracker):")
        for addr, v in new.items():
            print(f"  {addr} | {v['direction']} {v['date']} | {v['subject'][:60]}")
    print(f"\nDrafts in Gmail: {len(all_drafts)} ({sum(bool(r['drafts']) for r in rows)} on tracker rows)")
    print(f"\nCHECKED {len(checked)}/{len(rows)} active rows. Full JSON: {a.out}")


if __name__ == "__main__":
    try:
        main()
    finally:
        if not os.environ.get("K") and os.path.exists(KEY_FILE):
            os.remove(KEY_FILE)
