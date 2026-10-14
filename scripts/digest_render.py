"""Render the VO Pipeline Digest as an HTML email (Spencer, 2026-10-14).

Same skeleton as Paige's Portio Daily Brief (big title, stat row, one labelled
card per section, footer link), in a business-report style (Spencer, 10-14: "more business and less personal",
then "too round"): navy band, Georgia headings + Arial body, square corners, tinted status tags.

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
  "pipeline": {"pitch_drafts": 44, "cap": 20, "followup_drafts": 12, "scheduled": 0, "staged": 20},
  "season": {"now_label": "Oct 5-31:", "now": "Best window of the year ...",
             "timeline": [{"label": "Oct", "state": "full", "now": true}, ...],   # state: full|peak|light|black
             "windows": [{"who": "Corporate L&D", "window": "Oct 5 - early Dec", "status": "Open",
                          "state": "open", "why": "..."}]},                     # state: open|closing|soon|closed
  "funnels": [{"name": "I", "type": "Corporate L&D + dev", "drafts": 10, "staged": 0, "sent": 0, "note": ""}],
  "reach_out": [{"who": "Funnel I", "count": "10 drafts", "when": "Send now", "why": "..."}],
  "coverage": {"checked": 202, "active": 202, "as_of": "06:30 UTC", "unchecked": []},
  "bingo_call": "One plain sentence: the first thing to do today.",
  "due": [{"who": "Andrew Linsk", "company": "Psyop", "action": "Touch 2",
           "detail": "Thread reply. OOO since 10/7.", "days": 7,
           "draft": true, "level": "due", "thread": "<gmail threadId>"}],  # level: overdue|due|final|fix; thread -> name links to the draft
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
body,table,td,div,span,a{font-family:Arial,'Helvetica Neue',Helvetica,sans-serif}
body{margin:0;padding:0;background:#E9ECF0}
table{border-collapse:collapse;border-spacing:0}td{padding:0}
.w{max-width:600px;background:#fff;border:1px solid #D0D5DD}
.hd{background:#0B1F3A;padding:22px 24px 20px}
.br{font-size:10.5px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:#9FB0C8}
.tt{font-family:Georgia,'Times New Roman',serif;font-size:26px;font-weight:400;line-height:1.2;color:#fff;margin-top:8px}
.dt{font-size:12px;color:#9FB0C8;margin-top:6px}
.sb{padding:18px 24px 6px}
.st{padding:12px 4px;text-align:center;border:1px solid #D0D5DD;border-top:3px solid #0B1F3A}
.sn{font-size:24px;font-weight:700;line-height:1;color:#0B1F3A}
.sh{color:#9A3412}
.sl{font-size:9.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#475467;margin-top:7px}
.cv{font-size:11px;line-height:1.5;color:#667085;padding:8px 24px 0}
.cl{background:#F2F4F7;border-left:3px solid #0B1F3A;padding:12px 16px}
.ck{font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#0B1F3A}
.cb{font-size:14px;line-height:1.5;color:#101828;margin-top:5px}
.lb{font-size:10.5px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#0B1F3A;white-space:nowrap;padding-right:12px}
.ln{border-bottom:1px solid #0B1F3A}
.cd{padding:0 2px}
.rw{border-bottom:1px solid #EAECF0}
.it{font-size:14px;font-weight:700;line-height:1.35;color:#101828}
.co{color:#475467;font-weight:400}
.ib{font-size:13px;line-height:1.5;color:#475467;margin-top:3px}
.ac{color:#101828;font-weight:400}
.bg{display:inline-block;font-size:9.5px;font-weight:700;line-height:1;letter-spacing:.08em;text-transform:uppercase;padding:4px 6px;border-radius:2px;white-space:nowrap;border:1px solid}
.b-red{background:#FEF3F2;color:#912018;border-color:#FDA29B}.b-org{background:#FFFAEB;color:#93370D;border-color:#FEC84B}
.b-nav{background:#EEF2F6;color:#0B1F3A;border-color:#98A2B3}.b-grn{background:#ECFDF3;color:#05603A;border-color:#75E0A7}
.b-sl{background:#F2F4F7;color:#344054;border-color:#D0D5DD}.b-ms{background:#F9FAFB;color:#667085;border-color:#EAECF0}
.b-out{background:#fff;color:#667085;border-color:#D0D5DD}
.ok{font-size:13px;font-weight:700;color:#05603A;padding:12px 0}
.bt{display:inline-block;background:#0B1F3A;color:#fff;font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;text-decoration:none;padding:12px 20px;border-radius:2px}
.ft{font-size:11px;color:#667085;margin-top:14px}
.red{color:#912018;font-weight:700}
.lk{color:#0B1F3A;text-decoration:underline}
.il{padding:12px 0;vertical-align:top}.ir{padding:12px 0 12px 10px;vertical-align:top;text-align:right;white-space:nowrap}
.ob{display:inline-block;background:#0B1F3A;color:#fff;font-size:9.5px;font-weight:700;line-height:1;letter-spacing:.08em;text-transform:uppercase;padding:5px 8px;border-radius:2px;text-decoration:none;white-space:nowrap}
.pp{padding:0 24px}
.pt{padding:10px 4px;text-align:center;border:1px solid #D0D5DD;background:#F8FAFC}
.pn{font-size:20px;font-weight:700;line-height:1;color:#0B1F3A}
.pl{font-size:9px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#475467;margin-top:6px}
.ps{font-size:10px;color:#667085;margin-top:3px}
.ov{border-top:3px solid #912018}.ov .pn{color:#912018}
.tc{font-size:9px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;text-align:center;padding:7px 2px;border-right:2px solid #fff}
.s-full{background:#1D3A63;color:#fff}.s-peak{background:#0B1F3A;color:#fff}.s-light{background:#D0D5DD;color:#344054}.s-black{background:#FEF3F2;color:#912018}
.tn{font-size:9px;font-weight:700;color:#912018;text-align:center;padding-top:3px}
.nw{font-size:13px;line-height:1.5;color:#101828;padding:10px 0 4px}
.lg{font-size:10px;color:#667085;padding:4px 0 8px}
.fh{font-size:9.5px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#475467;padding:8px 6px 6px 0;border-bottom:1px solid #0B1F3A;text-align:left}
.fd{font-size:12.5px;color:#101828;padding:8px 6px 8px 0;border-bottom:1px solid #EAECF0;vertical-align:top}
.fn{font-weight:700;color:#0B1F3A;white-space:nowrap}
.fc{text-align:center;white-space:nowrap}
"""
T = '<table width="100%"'
NL = "\n"

GMAIL = "https://mail.google.com/mail/u/?authuser=spencer@spencerzvoice.com#all/"

LEVEL = {"overdue": ("Overdue", "b-red"), "fix": ("Fix + resend", "b-red"),
         "final": ("Final touch", "b-nav"), "due": ("Due today", "b-org")}
TAG = {"OOO": "b-sl", "Bounce": "b-red", "Unverified": "b-org", "System": "b-ms"}


def e(s):
    return html.escape("" if s is None else str(s), quote=True)


def badge(text, cls):
    return f'<span class="bg {cls}">{e(text)}</span>'


def section(label, inner, accent=""):
    return (f'<tr><td style="padding:24px 24px 4px">{T}><tr><td class="lb">{e(label)}</td>'
            f'<td width="100%" class="ln"></td></tr></table></td></tr>'
            f'<tr><td style="padding:0 24px"><div class="cd {accent}">{inner}</div></td></tr>')


def item(title, sub="", right="", body="", last=False, raw_title=False):
    sub_html = f'<span class="co"> &middot; {e(sub)}</span>' if sub else ""
    t = title if raw_title else e(title)
    title_html = f'<div class="it">{t}{sub_html}</div>' if title else ""
    body_html = f'<div class="ib">{body}</div>' if body else ""
    row_cls = "" if last else ' class="rw"'
    return (f'{T}{row_cls}><tr>'
            f'<td class="il">{title_html}{body_html}</td><td class="ir">{right}</td>'
            f'</tr></table>')


def items(rows, raw_title=False):
    return "".join(item(*r[:4], last=(i == len(rows) - 1), raw_title=raw_title) for i, r in enumerate(rows))


def due_rows(lst, show_draft):
    out = []
    for d in lst:
        right = badge(*LEVEL.get(d.get("level", "due"), LEVEL["due"]))
        link = GMAIL + d["thread"] if d.get("thread") else ""
        if show_draft:
            right += '<div style="height:5px"></div>' + (
                f'<a class="ob" href="{e(link)}">Open draft &rsaquo;</a>' if (d.get("draft") and link)
                else badge("Draft ready", "b-grn") if d.get("draft") else badge("No draft", "b-out"))
        bits = [e(d.get("action", ""))]
        if d.get("days") not in (None, ""):
            bits.append(f'day {e(d["days"])}')
        line = f'<b class="ac">{" &middot; ".join(b for b in bits if b)}</b>'
        if d.get("detail"):
            line += f"<br>{e(d['detail'])}"
        who = e(d.get("who", ""))
        title = f'<a class="lk" href="{e(link)}">{who}</a>' if link else who
        out.append((title, d.get("company", ""), right, line))
    return items(out, raw_title=True)


def pipeline_block(pp):
    if not pp:
        return ""
    cap = pp.get("cap", 20)
    q = pp.get("pitch_drafts", 0)
    over = q > cap
    gap = '<td width="6" style="font-size:0">&nbsp;</td>'

    def tile(n, label, sub, cls=""):
        return (f'<td width="25%" class="pt {cls}"><div class="pn">{e(n)}</div>'
                f'<div class="pl">{e(label)}</div><div class="ps">{e(sub)}</div></td>')
    q_sub = f"{q - cap} over the {cap} cap" if over else f"{cap - q} free of {cap}"
    row = (tile(q, "Pitch drafts", q_sub, "ov" if over else "") + gap
           + tile(pp.get("followup_drafts", 0), "Follow-up drafts", "in Drafts") + gap
           + tile(pp.get("scheduled", 0), "Scheduled", "in the outbox") + gap
           + tile(pp.get("staged", 0), "Staged", "built, not drafted"))
    return (f'<tr><td style="padding:22px 24px 4px">{T}><tr><td class="lb">Pipeline</td>'
            f'<td width="100%" class="ln"></td></tr></table></td></tr>'
            f'<tr><td class="pp" style="padding-top:8px">{T} style="border-collapse:separate"><tr>{row}</tr></table></td></tr>')


def season_block(sn):
    if not sn:
        return ""
    cells, marks = "", ""
    for c in sn.get("timeline", []):
        cells += f'<td class="tc s-{e(c.get("state", "full"))}">{e(c.get("label", ""))}</td>'
        marks += f'<td class="tn">{"&#9650; NOW" if c.get("now") else ""}</td>'
    strip = f'{T}><tr>{cells}</tr><tr>{marks}</tr></table>' if cells else ""
    legend = ('<div class="lg"><span style="color:#1D3A63">&#9632;</span> Full volume &nbsp; '
              '<span style="color:#0B1F3A">&#9632;</span> Peak &nbsp; '
              '<span style="color:#98A2B3">&#9632;</span> Light &nbsp; '
              '<span style="color:#F04438">&#9632;</span> No cold sends</div>') if cells else ""
    now = f'<div class="nw"><b>{e(sn.get("now_label", ""))}</b> {e(sn.get("now", ""))}</div>' if sn.get("now") else ""
    rows = [(w.get("who", ""), w.get("window", ""), badge(w.get("status", ""), {"open": "b-grn", "closing": "b-org", "soon": "b-nav", "closed": "b-ms"}.get(w.get("state"), "b-sl")) if w.get("status") else "", e(w.get("why", "")))
            for w in sn.get("windows", [])]
    return section("Budget season", strip + legend + now + items(rows))


def funnels_block(fs):
    if not fs:
        return ""
    head = ('<tr><th class="fh">Funnel</th><th class="fh">Who</th><th class="fh fc">Drafts</th>'
            '<th class="fh fc">Staged</th><th class="fh fc">Sent</th></tr>')
    body = "".join(
        f'<tr><td class="fd fn">{e(f.get("name", ""))}</td><td class="fd">{e(f.get("type", ""))}'
        + (f'<div style="font-size:11px;color:#667085;margin-top:2px">{e(f["note"])}</div>' if f.get("note") else "")
        + f'</td><td class="fd fc">{e(f.get("drafts", 0) or "-")}</td>'
        f'<td class="fd fc">{e(f.get("staged", 0) or "-")}</td><td class="fd fc">{e(f.get("sent", 0) or "-")}</td></tr>'
        for f in fs)
    return section("Funnels in play", f'{T}>{head}{body}</table>')


def reach_block(rs):
    if not rs:
        return ""
    rows = [(r.get("who", ""), r.get("count", ""), badge(r.get("when", ""), "b-nav") if r.get("when") else "",
             f'<b class="ac">Why:</b> {e(r.get("why", ""))}') for r in rs]
    return section("Who to contact next", items(rows))


def stat(label, value, hot=False):
    return (f'<td width="25%" class="st"><div class="sn{" sh" if hot else ""}">{e(value)}</div>'
            f'<div class="sl">{e(label)}</div></td>')


def build_html(d):
    date = dt.date.fromisoformat(d["date"])
    nice = f"{date.strftime('%A, %B')} {date.day}, {date.year}"
    c = d.get("counts", {})
    cov = d.get("coverage", {})
    gap = '<td width="6" style="font-size:0">&nbsp;</td>'
    stats = (f'{T} style="border-collapse:separate"><tr>'
             + stat("Due today", c.get("due_today", 0), hot=c.get("due_today", 0) > 0) + gap
             + stat("Replies", c.get("replies", 0), hot=c.get("replies", 0) > 0) + gap
             + stat("New", c.get("new_contacts", 0)) + gap
             + stat("Bounces", c.get("bounces", 0)) + "</tr></table>")
    cov_line = f'Gmail checked {e(cov.get("checked"))}/{e(cov.get("active"))} rows &middot; {e(cov.get("as_of"))}'
    if cov.get("checked") != cov.get("active"):
        cov_line += f' &middot; <span class="red">NOT CHECKED: {e(", ".join(cov.get("unchecked", [])))}</span>'

    header = (f'<tr><td class="hd"><div class="br">Spencer Z Voiceovers</div>'
              f'<div class="tt">VO Pipeline Digest</div><div class="dt">{e(nice)}</div></td></tr>'
              f'<tr><td class="sb">{stats}</td></tr><tr><td><div class="cv">{cov_line}</div></td></tr>')
    call = ""
    if d.get("bingo_call"):
        call = (f'<tr><td style="padding:16px 24px 0"><div class="cl">'
                f'<div class="ck">Priority today</div><div class="cb">{e(d["bingo_call"])}</div></div></td></tr>')

    body = []
    if d.get("due"):
        body.append(section("Follow-ups due today", due_rows(d["due"], True)))
    else:
        body.append(section("Follow-ups due today", '<div class="ok">No follow-ups due today.</div>', "a-g"))
    body += [reach_block(d.get("reach_out")), funnels_block(d.get("funnels")), season_block(d.get("season"))]
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

    footer = (f'<tr><td style="padding:26px 24px 24px;border-top:1px solid #EAECF0"><a class="bt" href="{e(d.get("tracker_url", ""))}">'
              f'Open tracker</a><div class="ft">Prepared by Bingo &middot; spencerzvoice.com</div></td></tr>')
    return ('<!doctype html><html><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<style>{CSS}</style></head><body>'
            f'{T} style="background:#E9ECF0"><tr><td align="center" style="padding:16px 8px">'
            f'{T} class="w">' + header + pipeline_block(d.get("pipeline")) + call + "".join(body) + footer +
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
