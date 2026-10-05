# PreToolUse hook: format QC on every Gmail draft write that goes through FGAC.
# Spencer, 2026-10-05: Bingo kept editing pitch drafts without checking them
# against the standard 6-part format ("you didn't follow the standard wording").
# A rule in a skill can be skipped; this can't. It runs before every
# google_api_modify call on gmail/v1/users/me/drafts, decodes the message, and
# BLOCKS the write (exit 2) if a new-client pitch breaks the house format.
# Replies and follow-ups (Re: subject, In-Reply-To/References) are not checked.
import base64, email, html, json, re, sys
from email import policy

data = json.load(sys.stdin)
ti = data.get("tool_input") or {}
path = str(ti.get("path", ""))
if "gmail/v1/users/me/drafts" not in path or path.rstrip("/").endswith("/send"):
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

subject = str(msg.get("Subject", "") or "")
if subject.strip().lower().startswith("re:") or msg.get("In-Reply-To") or msg.get("References"):
    sys.exit(0)  # follow-up / thread reply: different format, not checked here

part = msg.get_body(preferencelist=("html", "plain"))
content = part.get_content() if part else ""
text = html.unescape(re.sub(r"\s+", " ", content))

fails = []
def need(snippet, label):
    if snippet.lower() not in text.lower():
        fails.append("missing " + label + ": \"" + snippet + "\"")
def ban(pattern, label):
    if re.search(pattern, text, re.I):
        fails.append("banned " + label)

need("Let me introduce myself, my name is Spencer Pearman", "intro opener")
need("warm bass/baritone voice", "voice line")
need("Recent work includes", "credits in the intro")
need("You can hear my work at spencerzvoice.com", "website line")
if "I put together a re-voice of your" not in text and "VIDEO TITLE PENDING" not in text:
    fails.append("missing re-voice line (real title or VIDEO TITLE PENDING)")
need("Would love to be a voice you can call on regularly for", "standard close")
need("Feel free to reach out or schedule a call if this is something you're looking for. Hope to hear from you soon!", "standard close CTA")
need("Best,", "sign-off")
ban(r"[—–]", "em/en dash")
ban(r"please keep me in mind", "old close 'Please keep me in mind'")
ban(r"keep on file", "old close 'keep on file'")
ban(r"custom read", "'custom read' offer (re-voice line is never substituted)")
ban(r"american voice|professional american", "'American' in the voice line")
ban(r"low-register", "'low-register'")
if "[YOUR TAKE]" in text and not re.search(r"\[YOUR TAKE\]\s*Source:", text):
    fails.append("[YOUR TAKE] has no 'Source:' link")
if "[YOUR TAKE]" in content and "href" not in content.split("[YOUR TAKE]", 1)[1][:600]:
    fails.append("[YOUR TAKE] source is not a clickable link")

if fails:
    sys.stderr.write(
        "BLOCKED by pitch_draft_qc (Spencer's standard 6-part format, outreach-email Step 0c). "
        "Rebuild the draft and retry. Problems: " + "; ".join(fails) + "\n"
    )
    sys.exit(2)
sys.exit(0)
