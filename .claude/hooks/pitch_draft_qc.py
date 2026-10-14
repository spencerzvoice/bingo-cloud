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
# House template v5 = v4 (Spencer's own Calm + Premier Padel drafts, 2026-10-13) with the re-voice line moved up and reworded
# (Spencer's Docebo send, 2026-10-14: "apply that to all first touches").
need("My name is Spencer Pearman and I'm a professional Voiceover Artist and audio engineer based in Lisbon, Portugal", "v4 intro")
if not any(d in to for d in CUSTOM_REACHING_OUT_DOMAINS):
    need("based in Lisbon, Portugal, and I'd love to", "v4 intro + reaching-out sentence")
need("My standard turnaround is within 24 hours and within 2-3 hours for rush projects", "v4 turnaround line (Spencer 10-13: '2-3 hours')")
need("My recent work includes", "credits paragraph")
need("You can see more of my work at", "v4 website line")
# NO-SAMPLE exceptions = Spencer's own call per client, never Bingo's (2026-10-07: Pushkin Industries is audio-only,
# every trailer is read first-person by its host, 3 checks found nothing to re-voice -> "Go with 2", pitch without one).
if not any(d in to for d in NO_SAMPLE_DOMAINS):
    # v5 (Spencer's Docebo send, 2026-10-14): the re-voice line comes RIGHT AFTER the intro sentence and BEFORE the
    # turnaround/credits paragraph, and opens "To give you an idea of my voice, I re-voiced your ...".
    need("To give you an idea of my voice, I re-voiced your", "v5 re-voice line (title or VIDEO TITLE PENDING)")
    need("I'd appreciate it if you gave it a listen!", "re-voice follow-on")
    _l = text.lower()
    _i, _r, _t = _l.find("my name is spencer pearman"), _l.find("i re-voiced your"), _l.find("my standard turnaround")
    if min(_i, _r, _t) >= 0 and not (_i < _r < _t):
        fails.append("v5 order: the re-voice line must sit between the intro sentence and 'My standard turnaround'")
need("I'd love to get on a call and talk about working together, please don't hesitate to reach out. Hope to hear from you soon!", "v4 close")
need("Best,", "sign-off")
# Old v1/v2/v3 lines.
ban(r"finds you well", "old opener 'I hope this message finds you well' (v4: 'hope you're doing well!')")
ban(r"my work is high quality", "old 'My work is high quality'")
ban(r"feel free to reach out or schedule a call", "old close (v4: 'I'd love to get on a call ...')")
ban(r"just reply here and we can set up a call", "v3 close (v4: 'I'd love to get on a call ...')")
ban(r"I turn work around within 24 hours and run my own sessions", "v3 turnaround line (v4: 'My standard turnaround is within 24 hours ...')")
ban(r"my reels are at", "v3 website line (v4: 'You can see more of my work at spencerzvoice.com')")
ban(r"so you can hear how my voice meshes well", "v4 re-voice line (v5: 'To give you an idea of my voice, I re-voiced your ...')")
ban(r"I also re-voiced your", "v3 re-voice order (v4: 'Also, so you can hear ..., I re-voiced your ...')")
ban(r"starting with the ones about", "v3 callback (v4: 'especially the ones that spread the word about ...')")
ban(r"(to|with) the world", "v2 'to the world' callback")
ban(r"also, i put together a re-voice", "v2 re-voice opener")
ban(r"go-to voiceover artist", "v2 reaching-out line")
ban(r"among others \(", "v2 'among others (FIFA, ...)'")
ban(r"you can hear my work at", "v2 website line")
ban(r"at at", "typo 'at at'")
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
ban(r"starting with the videos that will tell this story", "old 10-05 bridge")
# Bingo writes the whole hook and leaves a yellow [Source: <link>] marker for Spencer (v2, kept in v3).
if "[Source:" in content and "href" not in content.split("[Source:", 1)[1][:400]:
    fails.append("[Source: ...] marker is not a clickable link")
if "[YOUR TAKE]" in text and not re.search(r"\[YOUR TAKE\]\s*Source:", text):
    fails.append("[YOUR TAKE] has no 'Source:' link")
if "[YOUR TAKE]" in content and "href" not in content.split("[YOUR TAKE]", 1)[1][:600]:
    fails.append("[YOUR TAKE] source is not a clickable link")

if fails:
    sys.stderr.write(
        "BLOCKED by pitch_draft_qc: pitch drafts must follow the house template v5 (Spencer, 2026-10-14; "
        "full text in reference/client-acquisition/PITCH-TEMPLATE.md). Rebuild the draft to it and retry. Problems: " + "; ".join(fails) + "\n"
    )
    sys.exit(2)
sys.exit(0)
