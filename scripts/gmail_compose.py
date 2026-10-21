"""Build a Gmail-native email (multipart/alternative: soft-wrapped text/plain + text/html in Gmail's own structure).

Spencer, 2026-10-21: emails Bingo built as text/plain only reached recipients as a narrow, hard-wrapped column pinned
left ("a tell that I'm using AI"). Gmail's own compose never does that: it sends <div dir="ltr">...<br><br>...</div>.

Usage:
  python scripts/gmail_compose.py --to "Name <a@b.com>, Name2 <c@d.com>" --subject "Subject" --body-file body.txt [--reply-to-msgid "<id>" --references "<ids>"] [--cc ...]
Body file = plain text, blank line between paragraphs, sign-off lines last ("Best,\nSpencer\nspencerzvoice.com").
A line that is exactly spencerzvoice.com becomes a link; http(s) URLs become links. Prints the base64url raw string; pass it as
google_api_modify body {"message": {"raw": "<raw>"}} to POST gmail/v1/users/me/drafts (or PUT drafts/<id>).
"""
import argparse, base64, html, re, textwrap
from email.message import EmailMessage

def html_body(text: str) -> str:
    esc = html.escape(text, quote=False).replace("'", "&#39;")
    esc = re.sub(r'(https?://[^\s<]+[^\s<.,;:!?)])', r'<a href="\1" target="_blank">\1</a>', esc)
    esc = re.sub(r'(^|\n)spencerzvoice\.com(?=\n|$)', r'\1<a href="https://spencerzvoice.com" target="_blank">spencerzvoice.com</a>', esc)
    return '<div dir="ltr">' + esc.replace("\n\n", "<br><br>").replace("\n", "<br>") + "</div>"

def plain_body(text: str) -> str:
    return "\n".join(textwrap.fill(l, 72) if len(l) > 72 else l for l in text.split("\n")) + "\n"

def build(to, subject, body, cc=None, in_reply_to=None, references=None, sender="Spencer Pearman <spencer@spencerzvoice.com>"):
    body = body.replace("\r\n", "\n").rstrip()
    m = EmailMessage()
    m["From"], m["To"], m["Subject"] = sender, to, subject
    if cc: m["Cc"] = cc
    if in_reply_to: m["In-Reply-To"] = in_reply_to
    if references: m["References"] = references
    m.set_content(plain_body(body))
    m.add_alternative(html_body(body), subtype="html")
    return base64.urlsafe_b64encode(m.as_bytes()).decode().rstrip("=")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--to", required=True); ap.add_argument("--subject", required=True)
    ap.add_argument("--body-file", required=True); ap.add_argument("--cc")
    ap.add_argument("--reply-to-msgid"); ap.add_argument("--references")
    a = ap.parse_args()
    print(build(a.to, a.subject, open(a.body_file, encoding="utf-8").read(), a.cc, a.reply_to_msgid, a.references))
