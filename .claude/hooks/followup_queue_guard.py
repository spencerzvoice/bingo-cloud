# Follow-up queue guard: cold touches 2 and 3 never become Gmail drafts and are never sent from a Claude session.
# Spencer, 2026-10-20: "They should not even hit my draft box, they need to go straight to scheduled" /
# "This needs to be done offline". Cause: from 10-15 to 10-19 the routines kept writing touch 2/3 drafts that sat
# unsent in Drafts (cloud runs can't schedule a Gmail send), and Spencer had to ask four times.
# The fix: touch 2/3 are rows in the Follow-up Queue Sheet (1YVJbPnETd3gkX8dAwdHsiqijojgMlyCL_4Jaskk9aao); the Apps
# Script "Bingo Follow-up Sender" in Spencer's account sends them offline (skill followup-drafts, "Send queue").
#
# PreToolUse on google_api_modify: BLOCK a draft create/update (POST drafts, PUT drafts/<id>) or a messages/send whose
# message is a reply carrying Spencer's touch-2 or touch-3 wording. Warm / LT drafts (other wording) pass.
import base64, email, json, sys
from email import policy

TOUCH_MARKERS = (
    "following up on the re-voice i sent last week",  # touch 2 (skill Step 2)
    "last note from me for now",                       # touch 3 (skill Step 2)
)

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

subject = str(msg.get("Subject", "") or "").strip().lower()
is_reply = subject.startswith("re:") or bool(msg.get("In-Reply-To")) or bool(msg.get("References"))
text = ""
for part in msg.walk():
    if part.get_content_type() in ("text/plain", "text/html"):
        try:
            text += " " + part.get_content()
        except Exception:
            pass
text = " ".join(text.lower().replace("&#39;", "'").split())

if is_reply and any(m in text for m in TOUCH_MARKERS):
    sys.stderr.write(
        "BLOCKED by followup_queue_guard: this is a cold touch 2/3. Those never go into Gmail Drafts and are never "
        "sent from a session (Spencer, 2026-10-20: \"They should not even hit my draft box\"). Append a QUEUED row "
        "to the Follow-up Queue Sheet 1YVJbPnETd3gkX8dAwdHsiqijojgMlyCL_4Jaskk9aao (tab Queue) instead, exactly as "
        "the followup-drafts skill's \"Send queue\" section says (touch 2 = 09:04, touch 3 = 10:13 contact-local); "
        "the Apps Script sender sends it offline.\n")
    sys.exit(2)
sys.exit(0)
