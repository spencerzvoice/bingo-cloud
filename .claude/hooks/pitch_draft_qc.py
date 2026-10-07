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
# Inline tags (links, highlights) are dropped so a linked "spencerzvoice.com" or title still matches;
# block tags become spaces. Spencer links the site himself in Gmail (YETI, 2026-10-07).
text = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(r"</?(a|span|b|i|u|strong|em|font)\b[^>]*>", "", content))))

fails = []
def need(snippet, label):
    if snippet.lower() not in text.lower():
        fails.append("missing " + label + ": \"" + snippet + "\"")
def ban(pattern, label):
    if re.search(pattern, text, re.I):
        fails.append("banned " + label)

# House template = Spencer's own Hitachi Rail email, sent 2026-10-05 11:54 (Gmail 1a10bb33cf02b312),
# plus his 10-05 edits: "turnaround is fast" cut from the intro, "24hrs" -> "24 hours", "Voiceover Artist" capitalized.
need("My name is Spencer Pearman and I'm a professional Voiceover Artist and audio engineer based in Lisbon, Portugal.", "intro")
ban(r"warm bass/baritone|record and produce everything myself", "voice line (Spencer 10-05 night: cut, the samples show the voice)")
ban(r"so turnaround is fast", "duplicate turnaround line (Spencer 10-05: cut it from the intro)")
need("I'm reaching out because I'd love to be your go-to Voiceover Artist for the projects that come through", "reaching-out paragraph")
need("My work is high quality, my turnaround is within 24 hours, and I run self-directed sessions, so it's one less thing to manage on a job.", "quality line (Spencer 10-05 night: high quality, not reliable)")
need("My recent work includes", "credits paragraph")
need("and you can hear my work at spencerzvoice.com", "website line")
# NO-SAMPLE exceptions = Spencer's own call per client, never Bingo's (2026-10-07: Pushkin Industries is audio-only,
# every trailer is read first-person by its host, 3 checks found nothing to re-voice -> "Go with 2", pitch without one).
NO_SAMPLE_DOMAINS = ("@pushkin.fm",)
if not any(d in str(msg.get("To", "")).lower() for d in NO_SAMPLE_DOMAINS):
    if "Also, I put together a re-voice of your" not in text and "VIDEO TITLE PENDING" not in text:
        fails.append("missing re-voice line ('Also, I put together a re-voice of your ...' or VIDEO TITLE PENDING)")
    need("so you can hear how my voice meshes well with your content. I'd appreciate it if you gave it a listen!", "re-voice follow-on")
need("Feel free to reach out or schedule a call if you'd like to talk about working together. I hope to hear from you soon!", "close (Spencer's TVA send, 10-05)")
need("Best,", "sign-off")
ban(r"would love to be a voice you can call on regularly", "old close 'Would love to be a voice you can call on regularly'")
ban(r"let me introduce myself", "old intro 'Let me introduce myself' (template starts 'My name is')")
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
        "BLOCKED by pitch_draft_qc: pitch drafts must follow the house template (Spencer's Hitachi Rail email of 2026-10-05; "
        "full text in .claude/skills/outreach-email/SKILL.md Step 0c). Rebuild the draft to it and retry. Problems: " + "; ".join(fails) + "\n"
    )
    sys.exit(2)
sys.exit(0)
