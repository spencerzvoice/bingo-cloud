"""Ledger coverage check: every outbound-initiated thread must be on the follow-up ledger or EXEMPT.

Spencer, 2026-10-15 (after the Funnel G/G2 pitches of 10-02..10-07 got no touch 2 for 8-13 days because
nobody added them to memory/followups-queue.md): matching subjects that start with "A voice for" is not
enough. This is a THREAD-ORIGIN scan, whatever the subject.

READ-ONLY. GETs only; it never creates, edits or sends anything.

What it does:
 1. Lists ALL of Sent for the last N days (default 21; `--days 30` for a backfill), paging through every
    result, plus every Scheduled message.
 2. Keeps each thread whose FIRST message is from Spencer (spencer@spencerzvoice.com) and goes to at least one
    external address (not spencer@spencerzvoice.com, not spencerzpearman@gmail.com).
 3. Reconciles each one against memory/followups-queue.md: COVERED if the thread id or any recipient address
    appears in the ledger/queue, EXEMPT if it appears on an `EXEMPT:` line there, else MISSING.
 4. Tracker cross-check (`--tracker live` reads the Outreach Tracker through FGAC; or `--tracker file.json`,
    a JSON list of [name, company, email, status] rows): every row whose Status starts with Sent /
    Follow-Up Sent and whose email is not in the ledger is reported as TRACKER-MISSING.
 5. Prints one line per MISSING thread and ends with:
       Ledger coverage: X outbound threads, Y in ledger, Z exempt, M missing
    Exit code 1 when anything is missing, so routines fail loudly.

Usage: set KEY_FILE (or K) to a FGAC temporary API key (create_temporary_api_key, purpose bulk_calls), then
    python scripts/ledger_coverage.py [--days 21] [--tracker tracker.json] [--json out.json]
"""
import argparse, json, os, re, sys, urllib.parse, urllib.request

SELF = {"spencer@spencerzvoice.com", "spencerzpearman@gmail.com"}
SHEET = "1SBauz4dCodqnfSVD5yqKETjU-25TY5HEZ7KRGggbgT0"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "memory", "followups-queue.md")
B = "https://fgac.ai/api/proxy/gmail/v1/users/me/"


def key():
    if os.environ.get("KEY_FILE"):
        return open(os.environ["KEY_FILE"]).read().strip()
    return os.environ["K"]


K = None


def get(p):
    r = urllib.request.Request(B + p, headers={"Authorization": "Bearer " + K})
    return json.load(urllib.request.urlopen(r, timeout=55))


def list_ids(q):
    out, tok = [], None
    while True:
        p = "messages?maxResults=500&q=" + urllib.parse.quote(q) + ("&pageToken=" + tok if tok else "")
        d = get(p)
        out += d.get("messages", [])
        tok = d.get("nextPageToken")
        if not tok:
            return out


def addrs(v):
    return sorted({a.lower() for a in re.findall(r"[\w.+'-]+@[\w-]+(?:\.[\w-]+)+", v or "")})


def main():
    global K
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=21)
    ap.add_argument("--tracker")
    ap.add_argument("--json")
    a = ap.parse_args()
    K = key()
    ids = list_ids("in:sent newer_than:%dd" % a.days) + list_ids("in:scheduled")
    threads = sorted({m["threadId"] for m in ids})
    ledger = open(LEDGER, encoding="utf-8").read().lower()
    exempt_lines = [l for l in ledger.splitlines() if "exempt:" in l]
    rows, cov, exm, miss = [], 0, 0, 0
    for t in threads:
        th = get("threads/%s?format=metadata&metadataHeaders=From&metadataHeaders=To&metadataHeaders=Cc"
                 "&metadataHeaders=Subject&metadataHeaders=Date" % t)
        msgs = th.get("messages", [])
        if not msgs:
            continue
        h = {x["name"].lower(): x["value"] for x in msgs[0]["payload"].get("headers", [])}
        frm = addrs(h.get("from"))
        if "spencer@spencerzvoice.com" not in frm:
            continue  # not outbound-initiated
        rc = [x for x in addrs(h.get("to", "") + " " + h.get("cc", "")) if x not in SELF]
        if not rc:
            continue  # only to himself
        inbound = any("spencer@spencerzvoice.com" not in addrs(
            {y["name"].lower(): y["value"] for y in m["payload"].get("headers", [])}.get("from")) for m in msgs)
        hit = t in ledger or any(x in ledger for x in rc)
        ex = any(t in l or any(x in l for x in rc) for l in exempt_lines)
        state = "EXEMPT" if ex else ("COVERED" if hit else "MISSING")
        cov += state == "COVERED"; exm += state == "EXEMPT"; miss += state == "MISSING"
        rows.append({"thread": t, "date": h.get("date", ""), "to": rc, "subject": h.get("subject", ""),
                     "messages": len(msgs), "inbound": inbound, "state": state,
                     "scheduled": any("SCHEDULED" in (m.get("labelIds") or []) for m in msgs)})
    for r in rows:
        if r["state"] == "MISSING":
            print("MISSING | %s | %s | %s | msgs=%d inbound=%s | %s" % (
                r["date"][:16], ", ".join(r["to"]), r["subject"][:70], r["messages"], r["inbound"], r["thread"]))
    tmiss = []
    if a.tracker:
        if a.tracker == "live":  # read the Outreach Tracker itself (cols A, B, D, G) through FGAC
            u = ("https://fgac.ai/api/proxy/sheets/v4/spreadsheets/" + SHEET + "/values/"
                 + urllib.parse.quote("'Outreach Tracker'!A2:G400"))
            vals = json.load(urllib.request.urlopen(urllib.request.Request(
                u, headers={"Authorization": "Bearer " + K}), timeout=55)).get("values", [])
            trows = [(r + [""] * 7)[:7] for r in vals]
            trows = [(r[0], r[1], r[3], r[6]) for r in trows]
        else:
            trows = json.load(open(a.tracker, encoding="utf-8"))
        for name, comp, em, st in trows:
            em = (em or "").strip().lower()
            if em and re.match(r"^(sent|follow-up sent)", (st or "").strip(), re.I) and em not in ledger:
                tmiss.append((name, comp, em, st))
                print("TRACKER-MISSING | %s | %s | %s | %s" % (name, comp, em, st))
    if a.json:
        json.dump({"rows": rows, "tracker_missing": tmiss}, open(a.json, "w", encoding="utf-8"), indent=1)
    print("Ledger coverage: %d outbound threads, %d in ledger, %d exempt, %d missing%s" % (
        len(rows), cov, exm, miss, (" (+%d tracker rows not in ledger)" % len(tmiss)) if a.tracker else ""))
    sys.exit(1 if (miss or tmiss) else 0)


if __name__ == "__main__":
    main()
