# Send window guard: no email reaches a contact before 08:32 or after 15:00 in THEIR local time.
# Spencer, 2026-10-15: "Nothing goes out before 8:32AM or after 3PM" / "Its scheduled, otherwise."
# Cause: on 10-15 at 11:13 UTC a desktop session sent 11 US follow-ups in one batch through a key script. They
# landed at 04:13-07:13 local. The 8:32 rule lived only in prompts and memory, and nothing checked the clock.
#
# How it works (no credentials needed):
#   PreToolUse on google_api_modify, path gmail/.../messages/send or drafts/send: find every recipient (To/Cc/Bcc),
#     look up each one's zone in reference/client-acquisition/CONTACT-TZ.json, and BLOCK unless it is 08:32-15:00
#     there right now. "US" = must be inside the window in both New York and Los Angeles. Unknown contact = BLOCK.
#     Spencer's own addresses are exempt (digest, reminders). Any error while checking = BLOCK (fail closed).
#   drafts/send only carries a draft id, so recipients come from a cache that this same hook fills:
#     PostToolUse on google_api_get of drafts/<id> and on google_api_modify draft create/update.
#     No cached recipients = BLOCK with "GET the draft first".
#   Outside the window the fix is to SCHEDULE: the block message prints the next weekday 08:32 local in UTC.
# Sends from scripts (key + urllib/curl) are blocked separately by no_script_sends.py, so this hook sees them all.
import base64, datetime, email, json, os, re, sys
from email import policy
from email.utils import getaddresses

try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover
    ZoneInfo = None

SELF = {"spencer@spencerzvoice.com", "spencerzpearman@gmail.com"}
OPEN, CLOSE = (8, 32), (15, 0)
US_ZONES = ["America/New_York", "America/Los_Angeles"]
CACHE = os.path.join(os.path.expanduser("~"), ".claude", "bingo_draft_recipients.json")
ROOT = os.environ.get("CLAUDE_PROJECT_DIR") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REGISTRY = os.path.join(ROOT, "reference", "client-acquisition", "CONTACT-TZ.json")

data = json.load(sys.stdin)
event = data.get("hook_event_name", "")
tool = data.get("tool_name", "")
ti = data.get("tool_input") or {}
path = str(ti.get("path", "")).split("?")[0].rstrip("/")


def block(msg):
    sys.stderr.write("BLOCKED by send_window_guard: " + msg + "\n")
    sys.exit(2)


def body():
    b = ti.get("body") or {}
    if isinstance(b, str):
        try:
            b = json.loads(b)
        except Exception:
            b = {}
    return b if isinstance(b, dict) else {}


def addrs_from_raw(raw):
    msg = email.message_from_bytes(base64.urlsafe_b64decode(raw + "=" * (-len(raw) % 4)), policy=policy.default)
    vals = [str(msg.get(h, "") or "").strip() for h in ("To", "Cc", "Bcc")]
    vals = [v for v in vals if v]  # an empty header makes getaddresses() return nothing at all (Python 3.13+)
    return sorted({a.strip().lower() for v in vals for _, a in getaddresses([v]) if a and "@" in a})


def load_cache():
    try:
        return json.load(open(CACHE))
    except Exception:
        return {}


def save_cache(c):
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    json.dump(c, open(CACHE, "w"))


def is_send():
    return bool(re.search(r"gmail/v1/users/[^/]+/(messages|drafts)/send$", path))


# ---- PostToolUse: remember draft recipients ----
if event == "PostToolUse":
    try:
        resp = data.get("tool_response")
        text = resp if isinstance(resp, str) else json.dumps(resp)
        text_u = text.replace('\\"', '"').replace("\\\\", "\\")
        c = load_cache()
        m = re.search(r"gmail/v1/users/[^/]+/drafts/(r-?\d+)$", path)
        if tool.endswith("google_api_get") and m:
            found = []
            for hm in re.finditer(r'"name":\s*"(To|Cc|Bcc)",\s*"value":\s*"([^"]*)"', text_u, re.I):
                found.append(hm.group(2))
            if found:
                c[m.group(1)] = sorted({a.strip().lower() for v in found if v.strip() for _, a in getaddresses([v]) if "@" in a})
                save_cache(c)
        elif tool.endswith("google_api_modify") and re.search(r"gmail/v1/users/[^/]+/drafts(/r-?\d+)?$", path):
            raw = (body().get("message") or {}).get("raw")
            idm = re.search(r'"id":\s*"(r-?\d+)"', text_u)
            if raw and idm:
                c[idm.group(1)] = addrs_from_raw(raw)
                save_cache(c)
    except Exception:
        pass
    sys.exit(0)

# ---- PreToolUse: gate every send ----
if not (event == "PreToolUse" and tool.endswith("google_api_modify") and is_send()):
    sys.exit(0)

try:
    b = body()
    if path.endswith("messages/send"):
        raw = b.get("raw")
        if not raw:
            block("messages/send without a raw body; can't see the recipients.")
        rcpts = addrs_from_raw(raw)
    else:
        raw = (b.get("message") or {}).get("raw")
        if raw:
            rcpts = addrs_from_raw(raw)
        else:
            did = str(b.get("id", ""))
            rcpts = load_cache().get(did)
            if not rcpts:
                block("no recipients on record for draft %s. First call google_api_get with path "
                      "gmail/v1/users/me/drafts/%s?format=metadata so the guard can read To/Cc/Bcc, then retry." % (did, did))
    if not rcpts:
        block("couldn't read any recipient address from this send; failing closed.")
    rcpts = [r for r in rcpts if r not in SELF]
    if not rcpts:
        sys.exit(0)  # only Spencer himself (digest, reminders)
    if ZoneInfo is None:
        block("Python zoneinfo unavailable; can't check local time. Install tzdata (pip install tzdata).")
    try:
        reg = {k.lower(): v for k, v in json.load(open(REGISTRY, encoding="utf-8")).items() if not k.startswith("_")}
    except Exception as e:
        block("can't read %s (%s)." % (REGISTRY, e))
    now = datetime.datetime.now(datetime.timezone.utc)
    bad, zones_all = [], []
    for r in rcpts:
        z = reg.get(r)
        if not z:
            block("%s has no time zone in reference/client-acquisition/CONTACT-TZ.json. Look up their location "
                  "(live LinkedIn), add the IANA zone (or \"US\" if only the country is known), then retry. "
                  "Nothing is sent to a contact whose local time is unknown." % r)
        zs = US_ZONES if z == "US" else [z]
        for zn in zs:
            loc = now.astimezone(ZoneInfo(zn))
            zones_all.append(zn)
            hm = (loc.hour, loc.minute)
            inside = hm >= OPEN and (hm < CLOSE or (hm == CLOSE and loc.second == 0))
            if not inside:
                bad.append("%s is %s %s (%s)" % (r, loc.strftime("%a %H:%M"), zn, z))
    if bad:
        # next weekday 08:32 that is inside the window for every recipient zone
        cands = []
        for zn in set(zones_all):
            loc = now.astimezone(ZoneInfo(zn))
            d = loc.replace(hour=8, minute=32, second=0, microsecond=0)
            if d <= loc:
                d += datetime.timedelta(days=1)
            while d.weekday() >= 5:
                d += datetime.timedelta(days=1)
            cands.append(d.astimezone(datetime.timezone.utc))
        nxt = max(cands)
        block("outside the 08:32-15:00 local window (Spencer, 2026-10-15: nothing goes out before 8:32AM or after "
              "3PM; otherwise it's scheduled). " + "; ".join(bad) + ". Do NOT send now. SCHEDULE it for the next "
              "08:32 local: %s UTC (book a one-shot trigger / Gmail Schedule send at that time)." % nxt.strftime("%a %Y-%m-%d %H:%M"))
except SystemExit:
    raise
except Exception as e:
    hint = " Time-zone data is missing: run `python -m pip install tzdata` (or `pip3 install tzdata`), then retry." \
        if "time zone" in str(e).lower() or "tzdata" in str(e).lower() else ""
    block("guard error (%s); failing closed.%s Fix the guard or the input, don't route around it." % (e, hint))
sys.exit(0)
