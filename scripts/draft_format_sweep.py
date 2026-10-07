"""Draft format sweep (Spencer, 2026-10-07: "anytime we update our process and we have drafts,
we need to go back and touch those drafts and bring them up to date").

Lists EVERY unsent new-client pitch draft in spencer@spencerzvoice.com and runs the house QC
(.claude/hooks/pitch_draft_qc.py) on each one. Run it after ANY change to the pitch template,
the QC hook, the outreach-email skill or a pick rule, and fix every FAIL before saying done.
Usage: set K to a FGAC temporary API key (create_temporary_api_key, purpose bulk_calls), then
    python scripts/draft_format_sweep.py
Prints PASS/FAIL per draft. Replies and follow-ups (Re:, In-Reply-To) are skipped by the hook.
"""
import base64, json, os, re, subprocess, sys, urllib.request
from email.mime.text import MIMEText

K = os.environ["K"]
B = "https://fgac.ai/api/proxy/gmail/v1/users/me/"
QC = os.path.join(os.path.dirname(__file__), "..", ".claude", "hooks", "pitch_draft_qc.py")

def get(p):
    return json.load(urllib.request.urlopen(urllib.request.Request(B + p, headers={"Authorization": "Bearer " + K})))

def html(payload):
    out = []
    def walk(p):
        if p.get("mimeType") == "text/html" and p.get("body", {}).get("data"):
            out.append(base64.urlsafe_b64decode(p["body"]["data"] + "==").decode("utf8", "replace"))
        for c in p.get("parts") or []:
            walk(c)
    walk(payload)
    return out[0] if out else ""

fails = 0
for d in get("drafts?maxResults=200").get("drafts", []):
    m = get("messages/" + d["message"]["id"] + "?format=full")
    hdr = {h["name"]: h["value"] for h in m["payload"]["headers"]}
    msg = MIMEText(html(m["payload"]), "html", "utf-8")
    msg["Subject"] = hdr.get("Subject", "")
    for k in ("In-Reply-To", "References"):
        if hdr.get(k):
            msg[k] = hdr[k]
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    r = subprocess.run([sys.executable, QC], input=json.dumps({"tool_input": {"path": "gmail/v1/users/me/drafts/x", "body": {"message": {"raw": raw}}}}), capture_output=True, text=True)
    ok = r.returncode == 0
    fails += not ok
    why = "" if ok else " | " + r.stderr.split("Problems:")[-1].strip()[:240]
    print(("PASS " if ok else "FAIL ") + d["id"] + " | " + hdr.get("To", "") + " | " + hdr.get("Subject", "") + why)
print(f"\n{fails} draft(s) need updating." if fails else "\nAll drafts match the current format.")
