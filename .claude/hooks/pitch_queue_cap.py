# Pitch queue cap: never more than 20 unsent new-client pitch drafts in Drafts.
# Spencer, 2026-10-13: "There's only supposed to be 20 draft in my Drafts at a time ... make sure this doesn't
# happen again." Cause: a desktop session told to "fully build Funnels P and K, then continue" created 28 pitch
# drafts on top of the 16 already there (44 total). The 20 rule lived only in the Morning Build prompt, and
# nothing counted the live queue before a create. A rule in a prompt can be skipped; this can't.
#
# How it works (no credentials needed):
#   PostToolUse on google_api_get: a full drafts list with q=subject:"A voice for" records the live pitch count
#     and the time in ~/.claude/bingo_pitch_queue.json (shared by every session on this machine, worktrees too).
#   PreToolUse on google_api_modify: a draft CREATE (POST gmail/v1/users/me/drafts, no draft id) of a new-client
#     pitch is BLOCKED unless a count from the last 10 minutes exists AND that count + creates since < 20.
#   PostToolUse on google_api_modify: each successful pitch create adds 1 to the recorded count.
# Updates to an existing draft (PUT drafts/<id>), replies and follow-ups are never counted or blocked.
import base64, email, json, os, re, sys, time, urllib.parse
from email import policy

CAP = 20
FRESH_SECONDS = 600
STATE = os.path.join(os.path.expanduser("~"), ".claude", "bingo_pitch_queue.json")
# One-off exceptions Spencer approves in chat, per recipient address (remove the entry once that draft exists).
# 2026-10-16 Spencer: "Yes, one-off exception: create the Lambda draft to Alex Morris now even though the queue is over 20."
CAP_EXCEPTIONS = ()  # alex@lambdafilms.co.uk used + removed 2026-10-16 (draft r7294973271141785164)
COUNT_PATH = 'gmail/v1/users/me/drafts?q=subject:"A voice for"&maxResults=200'

data = json.load(sys.stdin)
event = data.get("hook_event_name", "")
tool = data.get("tool_name", "")
ti = data.get("tool_input") or {}
path = str(ti.get("path", ""))


def load():
    try:
        return json.load(open(STATE))
    except Exception:
        return {}


def save(s):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    json.dump(s, open(STATE, "w"))


def is_pitch_create():
    p = path.split("?")[0].rstrip("/")
    if not p.endswith("gmail/v1/users/me/drafts") or str(ti.get("method") or "POST").upper() != "POST":
        return False
    body = ti.get("body") or {}
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except Exception:
            return False
    raw = ((body.get("message") or {}).get("raw")) if isinstance(body, dict) else None
    if not raw:
        return False
    try:
        msg = email.message_from_bytes(base64.urlsafe_b64decode(raw + "=" * (-len(raw) % 4)), policy=policy.default)
    except Exception:
        return False
    subject = str(msg.get("Subject", "") or "").strip().lower()
    if subject.startswith("re:") or msg.get("In-Reply-To") or msg.get("References"):
        return False
    part = msg.get_body(preferencelist=("html", "plain"))
    text = part.get_content() if part else ""
    return subject.startswith("a voice for") or "My name is Spencer Pearman" in text


# PostToolUse on a drafts list: record the live count.
if event == "PostToolUse" and tool.endswith("google_api_get"):
    p = urllib.parse.unquote(path).lower()
    if p.startswith("gmail/v1/users/me/drafts?") and 'subject:"a voice for"' in p and "pagetoken" not in p \
            and ti.get("offset") is None and ti.get("limit") is None:
        resp = json.dumps(data.get("tool_response"))
        if "next_offset" in resp or "nextPageToken" in resp:
            sys.exit(0)  # partial list: not a count
        n = len(set(re.findall(r'\\*"id\\*":\s*\\*"(r-?\d+)', resp)))
        save({"count": n, "at": time.time()})
    sys.exit(0)

# PostToolUse on a successful pitch create: count it.
if event == "PostToolUse" and tool.endswith("google_api_modify"):
    if is_pitch_create() and '"error' not in json.dumps(data.get("tool_response")).lower()[:400]:
        s = load()
        if s:
            s["count"] = s.get("count", 0) + 1
            save(s)
    sys.exit(0)

# PreToolUse: gate pitch creates.
if event == "PreToolUse" and tool.endswith("google_api_modify") and is_pitch_create():
    s = load()
    if not s or time.time() - s.get("at", 0) > FRESH_SECONDS:
        sys.stderr.write(
            "BLOCKED by pitch_queue_cap: count the live pitch queue first (Spencer, 2026-10-13: max 20 pitch drafts "
            "in Drafts). Call google_api_get with path exactly " + COUNT_PATH + " (no offset/limit), then retry. "
            "The count is good for 10 minutes.\n")
        sys.exit(2)
    _to = ""
    try:
        _b = ti.get("body") or {}
        _b = json.loads(_b) if isinstance(_b, str) else _b
        _raw = _b["message"]["raw"]
        _to = str(email.message_from_bytes(base64.urlsafe_b64decode(_raw + "=" * (-len(_raw) % 4)),
                                           policy=policy.default).get("To", "")).lower()
    except Exception:
        pass
    if s.get("count", 0) >= CAP and not any(x in _to for x in CAP_EXCEPTIONS):
        sys.stderr.write(
            "BLOCKED by pitch_queue_cap: Drafts already holds %d new-client pitch drafts; the cap is %d "
            "(Spencer, 2026-10-13). Do NOT create this draft. Keep the built payload as a STAGED spec in the funnel's "
            "contacts doc and draft it when Spencer sends and the queue drops below 20. Never delete drafts to make "
            "room.\n" % (s.get("count", 0), CAP))
        sys.exit(2)
sys.exit(0)
