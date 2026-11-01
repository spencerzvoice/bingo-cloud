# HTML mail guard: no text/plain-only emails to other people.
# Spencer, 2026-10-21: an email Bingo built (Altra retainer pitch) "comes out skewed to the left ... a tell that I'm
# using AI", and he had seen it on other emails Bingo wrote. Cause: a message with only a text/plain part. Gmail
# re-folds plain text at ~72 columns on delivery, so Outlook/phones show a narrow, hard-wrapped column pinned left in a
# different font. Gmail's own compose always sends multipart/alternative with a text/html part (<div dir="ltr"> ...
# <br><br> ...), which reflows to the window. The offline follow-up sender (scripts/apps-script/FollowupSender.gs) had the
# same bug and was fixed the same day.
#
# PreToolUse on google_api_modify: BLOCK a Gmail draft create/update or a messages/send whose message has no text/html
# part, unless every recipient is Spencer himself (alerts, self-tests). Build messages with scripts/gmail_compose.py.
import base64, email, json, sys
from email import policy

ME = "spencer@spencerzvoice.com"

data = json.load(sys.stdin)
if data.get("hook_event_name") != "PreToolUse" or not str(data.get("tool_name", "")).endswith("google_api_modify"):
    sys.exit(0)
ti = data.get("tool_input") or {}
path = str(ti.get("path", "")).split("?")[0].rstrip("/")
is_draft_write = "gmail/v1/users/me/drafts" in path and not path.endswith("/send")
is_send = path.endswith("gmail/v1/users/me/messages/send")
if not (is_draft_write or is_send):
    sys.exit(0)

body = ti.get("body") or {}
if isinstance(body, str):
    try:
        body = json.loads(body)
    except Exception:
        sys.exit(0)
raw = (body.get("message") or {}).get("raw") if is_draft_write else body.get("raw")
if not raw:
    sys.exit(0)
try:
    msg = email.message_from_bytes(base64.urlsafe_b64decode(raw + "=" * (-len(raw) % 4)), policy=policy.default)
except Exception:
    sys.exit(0)

recips = " ".join(str(msg.get(h, "") or "") for h in ("To", "Cc", "Bcc")).lower()
addrs = [a for a in (email.utils.getaddresses([recips]) or []) if a[1]]
if addrs and all(a[1] == ME for a in addrs):
    sys.exit(0)  # internal note to Spencer: plain is fine

if not any(p.get_content_type() == "text/html" for p in msg.walk()):
    sys.stderr.write(
        "BLOCKED by html_mail_guard: this message is text/plain only. Gmail re-folds plain text at ~72 columns, so the "
        "recipient sees a narrow hard-wrapped column pinned left, which reads as machine-written (Spencer, 2026-10-21). "
        "Build it as multipart/alternative with an HTML part in Gmail's own structure: "
        "python scripts/gmail_compose.py --to ... --subject ... --body-file body.txt  (prints the raw string to pass as "
        "{\"message\":{\"raw\": ...}}).\n")
    sys.exit(2)
