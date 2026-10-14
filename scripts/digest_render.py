"""Render the VO Pipeline Digest as an HTML email (Spencer, 2026-10-14).

Same skeleton as Paige's Portio Daily Brief (big title, stat row, one labelled
card per section, footer link), in a plain business style (Spencer, 10-14:
"more business and less personal"): system sans, navy + grey, muted status colours.

Usage:
    python scripts/digest_render.py local/digest-data-<date>.json

Writes next to the input:
    digest-<date>.html  - the HTML body (open it in a browser to preview)
    digest-<date>.txt   - plain-text version (for the log; not sent)
    digest-<date>.raw   - base64url RFC 2822 message, ready for
                          FGAC google_api_modify POST gmail/v1/users/me/messages/send
                          with body {"raw": <file contents>}

Input JSON (every list optional; empty lists hide their section):
{
  "date": "2026-10-14",
  "to": "spencer@spencerzvoice.com",
  "counts": {"new_contacts": 0, "replies": 0, "bounces": 2, "due_today": 12},
  "pitch_queue": 18,                       # unsent "A voice for" drafts, or null
  "coverage": {"checked": 202, "active": 202, "as_of": "06:30 UTC", "unchecked": []},
  "bingo_call": "One plain sentence: the first thing to do today.",
  "due": [{"who": "Andrew Linsk", "company": "Psyop", "action": "Touch 2",
           "detail": "Thread reply. OOO since 10/7.", "days": 7,
           "draft": true, "level": "due"}],       # level: overdue | due | final | fix
  "due_no_draft": [ same shape ],
  "coming_up": ["Funnel D / Airtable touch 3 - Thu 10/15"],
  "this_week": [{"when": "Thu 10/15", "text": "Funnel D touch 3 (6)"}],   # Mondays
  "replies": [{"who": "...", "company": "...", "gist": "...", "next": "..."}],
  "new_contacts": [{"who": "...", "company": "...", "what": "...", "why": "..."}],
  "heads_up": [{"tag": "OOO", "text": "..."}],   # tag: OOO | Bounce | Unverified | System
  "tracker_url": "https://docs.google.com/spreadsheets/d/..."
}
"""
import base64
import datetime as dt
import html
import json
import sys
from email.message import EmailMessage
from email.policy import SMTP
from pathlib import Path

# Styles live in one <style> block (Gmail honours it for Workspace inboxes) instead of
# inline on every tag, so the raw message stays small enough for the FGAC send call.
CSS = """
body,table,td,div,span,a{font-family:'Segoe UI',Inter,Roboto,'Helvetica Neue',Helvetica,Arial,sans-serif}
body{margin:0;padding:0;background:#EEF1F5}
table{border-collapse:collapse;border-spacing:0}td{padding:0}
.w{max-width:600px}
.hd{background:#fff;padding:24px 24px 20px;border-top:4px solid #14284B;border-radius:4px 4px 0 0}
.br{font-size:11px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:#5B6577}
.tt{font-size:28px;font-weight:700;line-height:1.15;color:#14284B;margin-top:10px}
.dt{font-size:13px;color:#5B6577;margin-top:6px}
.st{padding:14px 4px;text-align:center;background:#F5F7FA;border:1px solid #E4E7EC;border-radius:8px}
.sn{font-size:26px;font-weight:700;line-height:1;color:#14284B}
.sh{color:#B54708}
.sl{font-size:10px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#5B6577;margin-top:7px}
.cv{font-size:11.5px;line-height:1.5;color:#5B6577;margin-top:12px}
.cl{background:#EFF4FF;border-left:3px solid #1849A9;border-radius:4px;padding:12px 16px}
.ck{font-size:10.5px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:#1849A9}
.cb{font-size:14.5px;font-weight:500;line-height:1.5;color:#1D2939;margin-top:6px}
.lb{font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#5B6577;white-space:nowrap;padding-right:12px}
.ln{border-bottom:1px solid #E4E7EC}
.cd{background:#fff;border-radius:10px;border:1px solid #E4E7EC;border-top:3px solid #14284B;padding:4px 18px}
.a-g{border-top-color:#067647}.a-m{border-top-color:#98A2B3}.a-s{border-top-color:#5B6577}
.rw{border-bottom:1px solid #E4E7EC}
.it{font-size:15px;font-weight:600;line-height:1.35;color:#1D2939}
.co{color:#5B6577;font-weight:400}
.ib{font-size:13px;line-height:1.55;color:#5B6577;margin-top:4px}
.ac{color:#14284B;font-weight:600}
.bg{display:inline-block;font-size:10.5px;font-weight:600;line-height:1;letter-spacing:.04em;padding:4px 8px;border-radius:999px;white-space:nowrap;color:#fff;border:1.5px solid}
.b-red{background:#B42318;border-color:#B42318}.b-org{background:#B54708;border-color:#B54708}
.b-nav{background:#14284B;border-color:#14284B}.b-grn{background:#067647;border-color:#067647}
.b-sl{background:#5B6577;border-color:#5B6577}.b-ms{background:#98A2B3;border-color:#98A2B3}
.b-out{background:transparent;color:#5B6577;border-color:#98A2B3}
.ok{font-size:14px;font-weight:600;color:#067647;padding:12px 0}
.bt{display:inline-block;background:#14284B;color:#fff;font-size:13px;font-weight:600;text-decoration:none;padding:12px 20px;border-radius:6px}
.ft{font-size:11.5px;color:#5B6577;margin-top:16px}
.red{color:#B42318;font-weight:600}
"""
T = '<table width="100%"'
NL = "\n"

LEVEL = {"overdue": ("Overdue", "b-red"), "fix": ("Fix + resend", "b-red"),
         "final": ("Final touch", "b-nav"), "due": ("Due today", "b-org")}
TAG = {"OOO": "b-sl", "Bounce": "b-red", "Unverified": "b-org", "System": "b-ms"}


def e(s):
    return html.escape("" if s is None else str(s), quote=True)


def badge(text, cls):
    return f'<span class="bg {cls}">{e(text)}</span>'


def section(label, inner, accent=""):
    return (f'<tr><td style="padding:26px 24px 8px">{T}><tr><td class="lb">{e(label)}</td>'
            f'<td width="100%" class="ln"></td></tr></table></td></tr>'
            f'<tr><td style="padding:6px 24px 0"><div class="cd {accent}">{inner}</div></td></tr>')


def item(title, sub="", right="", body="", last=False):
    sub_html = f'<span class="co"> &middot; {e(sub)}</span>' if sub else ""
    title_html = f'<div class="it">{e(title)}{sub_html}</div>' if title else ""
    body_html = f'<div class="ib">{body}</div>' if body else ""
    row_cls = "" if last else ' class="rw"'
    return (f'{T}{row_cls}><tr>'
            f'<td style="padding:12px 0;vertical-align:top">{title_html}{body_html}</td>'
            f'<td style="padding:12px 0 12px 10px;vertical-align:top;text-align:right;white-space:nowrap">{right}</td>'
            f'</tr></table>')


def items(rows):
    return "".join(item(*r[:4], last=(i == len(rows) - 1)) for i, r in enumerate(rows))


def due_rows(lst, show_draft):
    out = []
    for d in lst:
        right = badge(*LEVEL.get(d.get("level", "due"), LEVEL["due"]))
        if show_draft:
            right += '<div style="height:5px"></div>' + (
                badge("Draft ready", "b-grn") if d.get("draft") else badge("No draft", "b-out"))
        bits = [e(d.get("action", ""))]
        if d.get("days") not in (None, ""):
            bits.append(f'day {e(d["days"])}')
        line = f'<b class="ac">{" &middot; ".join(b for b in bits if b)}</b>'
        if d.get("detail"):
            line += f"<br>{e(d['detail'])}"
        out.append((d.get("who", ""), d.get("company", ""), right, line))
    return items(out)


def stat(label, value, hot=False):
    return (f'<td width="25%" class="st"><div class="sn{" sh" if hot else ""}">{e(value)}</div>'
            f'<div class="sl">{e(label)}</div></td>')


def build_html(d):
    date = dt.date.fromisoformat(d["date"])
    nice = f"{date.strftime('%A, %B')} {date.day}, {date.year}"
    c = d.get("counts", {})
    cov = d.get("coverage", {})
    gap = '<td width="8" style="font-size:0">&nbsp;</td>'
    stats = (f'{T} style="border-collapse:separate"><tr>'
             + stat("Due today", c.get("due_today", 0), hot=c.get("due_today", 0) > 0) + gap
             + stat("Replies", c.get("replies", 0), hot=c.get("replies", 0) > 0) + gap
             + stat("New", c.get("new_contacts", 0)) + gap
             + stat("Bounces", c.get("bounces", 0)) + "</tr></table>")
    cov_line = f'Gmail checked {e(cov.get("checked"))}/{e(cov.get("active"))} rows &middot; {e(cov.get("as_of"))}'
    if cov.get("checked") != cov.get("active"):
        cov_line += f' &middot; <span class="red">NOT CHECKED: {e(", ".join(cov.get("unchecked", [])))}</span>'
    if d.get("pitch_queue") is not None:
        cov_line += f' &middot; Pitch queue {e(d["pitch_queue"])}/20'

    header = (f'<tr><td class="hd"><div class="br">Spencer Z Voiceovers</div>'
              f'<div class="tt">VO Pipeline Digest</div><div class="dt">{e(nice)}</div>'
              f'<div style="height:18px"></div>{stats}<div class="cv">{cov_line}</div></td></tr>')
    call = ""
    if d.get("bingo_call"):
        call = (f'<tr><td style="background:#fff;padding:0 24px 20px"><div class="cl">'
                f'<div class="ck">Priority today</div><div class="cb">{e(d["bingo_call"])}</div></div></td></tr>')

    body = []
    if d.get("due"):
        body.append(section("Follow-ups due today", due_rows(d["due"], True)))
    else:
        body.append(section("Follow-ups due today", '<div class="ok">No follow-ups due today.</div>', "a-g"))
    if d.get("due_no_draft"):
        body.append(section("Due, no draft yet", due_rows(d["due_no_draft"], False), "a-m"))
    if d.get("this_week"):
        body.append(section("This week", items([(w.get("when", ""), "", "", e(w.get("text", ""))) for w in d["this_week"]]), "a-s"))
    if d.get("replies"):
        body.append(section("Replies + status changes", items([
            (r.get("who", ""), r.get("company", ""), "",
             e(r.get("gist", "")) + (f'<br><b class="ac">Next:</b> {e(r["next"])}' if r.get("next") else ""))
            for r in d["replies"]])))
    if d.get("new_contacts"):
        body.append(section("New contacts", items([
            (n.get("who", ""), n.get("company", ""), "",
             e(n.get("what", "")) + (f' &middot; {e(n["why"])}' if n.get("why") else ""))
            for n in d["new_contacts"]]), "a-g"))
    if d.get("heads_up"):
        body.append(section("Heads up", items([
            ("", "", badge(h.get("tag", "Note"), TAG.get(h.get("tag"), "b-sl")), e(h.get("text", "")))
            for h in d["heads_up"]]), "a-s"))
    if d.get("coming_up"):
        body.append(section("Coming up", items([("", "", "", e(x)) for x in d["coming_up"]]), "a-m"))

    footer = (f'<tr><td style="padding:28px 24px 26px"><a class="bt" href="{e(d.get("tracker_url", ""))}">'
              f'Open the tracker &rarr;</a><div class="ft">Prepared by Bingo &middot; spencerzvoice.com</div></td></tr>')
    return ('<!doctype html><html><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<style>{CSS}</style></head><body>'
            f'{T} style="background:#EEF1F5"><tr><td align="center" style="padding:18px 8px">'
            f'{T} class="w">' + header + call + "".join(body) + footer +
            '</table></td></tr></table></body></html>')


def build_text(d):
    c = d.get("counts", {})
    cov = d.get("coverage", {})
    L = [f'{c.get("new_contacts", 0)} new contacts, {c.get("replies", 0)} replies, '
         f'{c.get("bounces", 0)} bounces, {c.get("due_today", 0)} follow-ups due today.',
         f'Gmail checked: {cov.get("checked")}/{cov.get("active")} active rows, as of {cov.get("as_of")}.']
    if d.get("bingo_call"):
        L += ["", "PRIORITY TODAY: " + d["bingo_call"]]

    def due_txt(lst):
        return [f'- {x.get("who")}, {x.get("company")} - {x.get("action")}'
                + (f' (day {x["days"]})' if x.get("days") not in (None, "") else "")
                + (". Draft ready." if x.get("draft") else ".")
                + (f' {x["detail"]}' if x.get("detail") else "") for x in lst]
    L += ["", "FOLLOW-UPS DUE TODAY"] + (due_txt(d["due"]) if d.get("due") else ["No follow-ups due today."])
    if d.get("due_no_draft"):
        L += ["", "DUE, NO DRAFT YET"] + due_txt(d["due_no_draft"])
    if d.get("this_week"):
        L += ["", "THIS WEEK"] + [f'- {w.get("when")}: {w.get("text")}' for w in d["this_week"]]
    if d.get("replies"):
        L += ["", "REPLIES / STATUS CHANGES"] + [f'- {r.get("who")}, {r.get("company")}: {r.get("gist")}'
                                                 + (f' Next: {r["next"]}' if r.get("next") else "") for r in d["replies"]]
    if d.get("new_contacts"):
        L += ["", "NEW CONTACTS"] + [f'- {n.get("who")}, {n.get("company")}: {n.get("what")} {n.get("why", "")}'.rstrip()
                                     for n in d["new_contacts"]]
    if d.get("heads_up"):
        L += ["", "HEADS UP"] + [f'- [{h.get("tag")}] {h.get("text")}' for h in d["heads_up"]]
    if d.get("coming_up"):
        L += ["", "COMING UP"] + [f"- {x}" for x in d["coming_up"]]
    L += ["", d.get("tracker_url", "")]
    return "\n".join(L)


def main():
    src = Path(sys.argv[1])
    d = json.loads(src.read_text(encoding="utf-8"))
    date = dt.date.fromisoformat(d["date"])
    html_body, text_body = build_html(d), build_text(d)
    msg = EmailMessage(policy=SMTP)
    msg["To"] = d.get("to", "spencer@spencerzvoice.com")
    msg["From"] = "Spencer Pearman <spencer@spencerzvoice.com>"
    n = d.get("counts", {}).get("due_today", 0)
    lead = f"{n} due today" if n else "nothing due"
    msg["Subject"] = f"VO Pipeline Digest - {date.strftime('%B')} {date.day}, {date.year} - {lead}"
    # Pure ASCII + short lines lets both parts go 7bit instead of base64 (smaller raw).
    html_ascii = html_body.encode("ascii", "xmlcharrefreplace").decode("ascii")
    for tag in ("</tr>", "</td>", "</div>", "</table>", "</a>", "</head>", "</style>"):
        html_ascii = html_ascii.replace(tag, tag + NL)
    html_ascii = html_ascii.replace("<table", NL + "<table")
    # HTML only: Gmail renders it everywhere Spencer reads, and dropping the text part
    # keeps the raw ~20 KB. The .txt is still written for the log.
    msg.set_content(html_ascii, subtype="html", charset="us-ascii", cte="7bit")
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode("ascii")
    out = src.parent
    (out / f"digest-{d['date']}.html").write_text(html_body, encoding="utf-8")
    (out / f"digest-{d['date']}.txt").write_text(text_body, encoding="utf-8")
    (out / f"digest-{d['date']}.raw").write_text(raw, encoding="ascii")
    print(f"OK html={len(html_body)} raw={len(raw)} -> {out / ('digest-' + d['date'] + '.raw')}")


if __name__ == "__main__":
    main()
