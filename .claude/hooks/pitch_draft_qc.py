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

# Only new-client PITCHES are checked: subject "A voice for ...", the v3 intro, or the old v2 go-to line
# (so an old-format draft still FAILS the sweep). Review requests, roster submissions and other one-off
# emails pass (Lilah Kohlman review ask, Great Voices, 10-06/10-07).
part = msg.get_body(preferencelist=("html", "plain"))
_body = part.get_content() if part else ""
if (not subject.strip().lower().startswith("a voice for") and "go-to Voiceover Artist" not in _body
        and "My name is Spencer Pearman" not in _body):
    sys.exit(0)
content = part.get_content() if part else ""
# Inline tags (links, highlights) are dropped so a linked "spencerzvoice.com" or title still matches;
# block tags become spaces. Spencer links the site himself in Gmail (YETI, 2026-10-07).
text = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(r"</?(a|span|b|i|u|strong|em|font)\b[^>]*>", "", content))))
text = text.replace("’", "'")

fails = []
def need(snippet, label):
    if snippet.lower() not in text.lower():
        fails.append("missing " + label + ": \"" + snippet + "\"")
def ban(pattern, label):
    if re.search(pattern, text, re.I):
        fails.append("banned " + label)

# House template v3 (Spencer approved 2026-10-12, humanizer pass on v2): reference/client-acquisition/PITCH-TEMPLATE.md.
# Spencer's own per-client reaching-out line, kept word for word (Pushkin: audiobooks/podcasts, 2026-10-07).
CUSTOM_REACHING_OUT_DOMAINS = ("@pushkin.fm",)
NO_SAMPLE_DOMAINS = ("@pushkin.fm",)
to = str(msg.get("To", "")).lower()
need("My name is Spencer Pearman. I'm a voiceover artist and audio engineer in Lisbon", "v3 intro")
if not any(d in to for d in CUSTOM_REACHING_OUT_DOMAINS):
    need("My name is Spencer Pearman. I'm a voiceover artist and audio engineer in Lisbon, and I'd love to voice the videos that come out of", "v3 intro + reaching-out sentence")
need("I turn work around within 24 hours and run my own sessions, so it's one less thing for you to manage.", "v3 turnaround line")
need("My recent work includes", "credits paragraph")
need("my reels are at spencerzvoice.com", "v3 website line")
# NO-SAMPLE exceptions = Spencer's own call per client, never Bingo's (2026-10-07: Pushkin Industries is audio-only,
# every trailer is read first-person by its host, 3 checks found nothing to re-voice -> "Go with 2", pitch without one).
if not any(d in to for d in NO_SAMPLE_DOMAINS):
    if "I also re-voiced your" not in text and "VIDEO TITLE PENDING" not in text:
        fails.append("missing re-voice line ('I also re-voiced your ...' or VIDEO TITLE PENDING)")
    need("so you can hear how my voice meshes well with your content. I'd appreciate it if you gave it a listen!", "re-voice follow-on")
need("If you'd like to work together, just reply here and we can set up a call. Hope to hear from you soon!", "v3 close")
need("Best,", "sign-off")
# Old v1/v2 lines (humanizer pass 2026-10-12): stock opener, unsupported claim, inflated callback, stock close.
ban(r"finds you well", "v2 opener 'I hope this message finds you well' (v3: 'hope you're doing well!')")
ban(r"my work is high quality", "v2 'My work is high quality' (v3 turnaround line)")
ban(r"feel free to reach out or schedule a call", "v2 close (v3: 'If you'd like to work together, just reply here...')")
ban(r"\b(to|with) the world\b", "v2 'to the world' callback (v3: 'starting with the ones about <event>')")
ban(r"also, i put together a re-voice", "v2 re-voice opener (v3: 'I also re-voiced your')")
ban(r"go-to voiceover artist", "v2 reaching-out line (v3 merges it into the intro)")
ban(r"among others \(", "v2 'among others (FIFA, ...)' (v3: 'plus FIFA and EuroLeague Basketball')")
ban(r"you can hear my work at", "v2 website line (v3: 'my reels are at spencerzvoice.com')")
ban(r"professional voiceover artist", "v2 intro 'professional Voiceover Artist ... based in Lisbon, Portugal'")
ban(r"warm bass/baritone|record and produce everything myself", "voice line (Spencer 10-05 night: cut, the samples show the voice)")
ban(r"so turnaround is fast", "duplicate turnaround line (Spencer 10-05: cut it from the intro)")
ban(r"would love to be a voice you can call on regularly", "old close 'Would love to be a voice you can call on regularly'")
ban(r"let me introduce myself", "old intro 'Let me introduce myself' (template starts 'My name is')")
ban(r"[—–]", "em/en dash")
ban(r"please keep me in mind", "old close 'Please keep me in mind'")
ban(r"keep on file", "old close 'keep on file'")
ban(r"custom read", "'custom read' offer (re-voice line is never substituted)")
ban(r"american voice|professional american", "'American' in the voice line")
ban(r"low-register", "'low-register'")
ban(r"starting with the videos that will tell this story", "old 10-05 bridge (v3: 'starting with the ones about <event>')")
# Bingo writes the whole hook and leaves a yellow [Source: <link>] marker for Spencer (v2, kept in v3).
if "[Source:" in content and "href" not in content.split("[Source:", 1)[1][:400]:
    fails.append("[Source: ...] marker is not a clickable link")
if "[YOUR TAKE]" in text and not re.search(r"\[YOUR TAKE\]\s*Source:", text):
    fails.append("[YOUR TAKE] has no 'Source:' link")
if "[YOUR TAKE]" in content and "href" not in content.split("[YOUR TAKE]", 1)[1][:600]:
    fails.append("[YOUR TAKE] source is not a clickable link")

if fails:
    sys.stderr.write(
        "BLOCKED by pitch_draft_qc: pitch drafts must follow the house template v3 (Spencer, 2026-10-12; "
        "full text in reference/client-acquisition/PITCH-TEMPLATE.md). Rebuild the draft to it and retry. Problems: " + "; ".join(fails) + "\n"
    )
    sys.exit(2)
sys.exit(0)
