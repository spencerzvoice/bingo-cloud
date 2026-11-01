# Buyer gate: a new-client pitch only goes to someone who hires voice talent.
# Spencer, 2026-10-26 (Maersk: "Tell me why we reached out to the wrong person" -> "build the buyer gate").
# Cause: both researched Maersk targets had dead emails, so the 10-13 build pitched the first video-titled person
# with a valid email (Cameron Robertson, Senior Producer & Videographer). The employment gate only checks "works
# there"; nothing checked "buys VO". Same fallback hit Schneider (Web Content Producer), HashiCorp (content strategy)
# and Okta (Keynote Producer). A rule in a prompt can be skipped; this can't.
#
# PreToolUse on google_api_modify: any draft CREATE or UPDATE (POST/PUT gmail/v1/users/me/drafts...) of a new-client
# pitch is BLOCKED unless every To address has a row in reference/client-acquisition/BUYER-GATE.json with verdict
# PASS, PASS-EVIDENCE or KEEP-SPENCER. Rows are written by scripts/buyer_gate.py. Replies/follow-ups pass through.
import base64, email, json, os, re, sys
from email import policy

OK = ("PASS", "PASS-EVIDENCE", "KEEP-SPENCER")
ROOT = os.environ.get("CLAUDE_PROJECT_DIR") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
LEDGER = os.path.join(ROOT, "reference", "client-acquisition", "BUYER-GATE.json")

data = json.load(sys.stdin)
ti = data.get("tool_input") or {}
path = str(ti.get("path", "")).split("?")[0].rstrip("/")
if not re.search(r"gmail/v1/users/me/drafts(/[^/]+)?$", path):
    sys.exit(0)
body = ti.get("body") or {}
if isinstance(body, str):
    try:
        body = json.loads(body)
    except Exception:
        sys.exit(0)
raw = ((body.get("message") or {}).get("raw")) if isinstance(body, dict) else None
if not raw:
    sys.exit(0)
try:
    msg = email.message_from_bytes(base64.urlsafe_b64decode(raw + "=" * (-len(raw) % 4)), policy=policy.default)
except Exception:
    sys.exit(0)
subject = str(msg.get("Subject", "") or "").strip().lower()
if subject.startswith("re:") or msg.get("In-Reply-To") or msg.get("References"):
    sys.exit(0)
part = msg.get_body(preferencelist=("html", "plain"))
text = part.get_content() if part else ""
if not (subject.startswith("a voice for") or "My name is Spencer Pearman" in text):
    sys.exit(0)

to = [a.lower() for a in re.findall(r"[\w.+'-]+@[\w-]+(?:\.[\w-]+)+", str(msg.get("To", "") or ""))]
if not to:
    sys.exit(0)  # no recipient yet (e.g. To cleared because the contact left): nothing to gate
try:
    ledger = json.load(open(LEDGER, encoding="utf-8"))
except Exception:
    ledger = {}

bad = []
for a in to:
    row = ledger.get(a)
    if not row:
        bad.append("%s: no buyer-gate row" % a)
    elif row.get("verdict") not in OK:
        bad.append("%s: %s (%s, %s) %s" % (a, row.get("verdict"), row.get("name"), row.get("title"), row.get("why", "")))
if bad:
    sys.stderr.write(
        "BLOCKED by buyer_gate_guard (Spencer, 2026-10-26, Maersk): a new-client pitch only goes to someone who hires "
        "voice talent.\n  " + "\n  ".join(bad) + "\n"
        "Fix: read the contact's CURRENT title on their live LinkedIn (or today's Apollo match), then run\n"
        "  python scripts/buyer_gate.py record <email> \"<Name>\" \"<Company>\" \"<title>\" --company-type inhouse|studio|agency "
        "--practice in-house-vo|agency|interviewee|unknown --source \"<where you read it>\" [--evidence \"...\"]\n"
        "FAIL = never fall back to them: go up the org (LinkedIn People tab, theorg.com) to the head of video/brand/"
        "creative, get that person's email through Apollo (waterfall, ZeroBounce valid), or mark the company BLOCKED. "
        "REVIEW passes only with written evidence (VO they booked, or the senior-most video owner + who you checked). "
        "Only Spencer can keep a FAIL (buyer_gate.py keep <email> \"<his words, date>\").\n")
    sys.exit(2)
sys.exit(0)
