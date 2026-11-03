"""Nomadic Light LLC invoice PDF (ReportLab).

Rebuilt 2026-11-03 from the layout of NL-2026-007 (the original script was never
saved). Layout, fonts, colours and positions match the 007 PDF.

Usage: python scripts/invoice_pdf.py <spec.json> <out.pdf>
spec.json keys: number, job, date, due_date, terms, bill_to (list of lines),
lines (list of {qty, description, unit_price}), notes (list of lines, optional),
payment_link, payment_link_label (optional), logo (path, optional).
"""
import json
import sys
from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

NAVY = HexColor("#2f4a63")
GREY = HexColor("#666666")
TEXT = HexColor("#333333")
LINK = HexColor("#5980a6")
HEADER_BG = HexColor("#5980a6")
DUE_BG = HexColor("#e8ecf1")
RULE = HexColor("#cccccc")

W, H = letter
LM, RM = 47, 565  # left / right margin x
DEFAULT_LOGO = Path(__file__).resolve().parent.parent / "reference" / "invoice-logo.png"

FROM_LINES = [
    "Spencer Pearman",
    "Nomadic Light LLC",
    "28 Cary Court",
    "Oakland, CA, USA 94603",
    "+1 (510) 316-9382",
    "spencer@spencerzvoice.com",
]
BANK = [
    ("WISE'S ADDRESS", ["Community Federal Savings Bank, 89-16", "Jamaica Ave, Woodhaven, NY 11421"]),
    ("ACCOUNT HOLDER", ["Nomadic Light LLC"]),
    ("ACCOUNT TYPE", ["Checking"]),
    ("ACH ROUTING NUMBER", ["026073150"]),
    ("SWIFT/BIC", ["CMFGUS33"]),
    ("ACCOUNT NUMBER", ["822000208583"]),
]


def y(top):
    """Convert a top-origin y (as measured in the 007 PDF) to ReportLab's bottom origin."""
    return H - top


def money(v):
    return "${:,.2f}".format(v)


def label(c, x, top, text, size=7.5):
    c.setFont("Helvetica-Bold", size)
    c.setFillColor(NAVY)
    c.drawString(x, y(top), text)


def body(c, x, top, text, size=9.5, color=TEXT, font="Helvetica"):
    c.setFont(font, size)
    c.setFillColor(color)
    c.drawString(x, y(top), text)


def rule(c, top, color=RULE, width=0.6):
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.line(LM, y(top), RM, y(top))


def build(spec, out):
    c = canvas.Canvas(str(out), pagesize=letter)
    c.setTitle("Invoice " + spec["number"])
    c.setAuthor("Nomadic Light LLC")

    # Header
    logo = Path(spec.get("logo") or DEFAULT_LOGO)
    if logo.exists():
        c.drawImage(str(logo), 46.8, y(102.8), 56, 56, mask="auto")
    body(c, 115, 50, "NOMADIC LIGHT LLC", 15, NAVY, "Helvetica-Bold")
    body(c, 115, 68, "28 Cary Court, Oakland, CA, USA 94603", 8.5, GREY)
    body(c, 115, 79, "+1 (510) 316-9382  |  spencer@spencerzvoice.com", 8.5, GREY)
    c.setFont("Helvetica-Bold", 22)
    c.setFillColor(NAVY)
    c.drawRightString(RM, y(44), "INVOICE")
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(GREY)
    c.drawRightString(RM, y(66), "Invoice #: " + spec["number"])
    c.setStrokeColor(HEADER_BG)
    c.setLineWidth(2.5)
    c.line(115, y(95), RM, y(95))

    # From / Bill to
    label(c, LM, 120, "FROM", 9)
    label(c, 316, 120, "BILL TO", 9)
    top = 135
    for line in FROM_LINES:
        body(c, LM, top, line)
        top += 12
    top = 135
    for line in spec["bill_to"]:
        body(c, 316, top, line)
        top += 12
    block_end = max(135 + 12 * len(FROM_LINES), 135 + 12 * len(spec["bill_to"])) + 10

    # Job
    rule(c, block_end)
    jt = block_end + 20
    label(c, LM, jt + 2, "JOB")
    body(c, 87, jt, spec["job"])
    rule(c, jt + 18)

    # Date row
    dt = jt + 44
    for x, lab, val in (
        (LM, "DATE", spec["date"]),
        (176, "DUE DATE", spec["due_date"]),
        (306, "PAYMENT TERMS", spec["terms"]),
        (436, "SALESPERSON", "Spencer Pearman"),
    ):
        label(c, x, dt, lab)
        body(c, x, dt + 11, val)
    rule(c, dt + 24)

    # Line items table
    th = dt + 56
    c.setFillColor(HEADER_BG)
    c.rect(LM, y(th + 8), RM - LM, 22, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(white)
    c.drawString(52, y(th), "QTY")
    c.drawString(97, y(th), "DESCRIPTION")
    c.drawRightString(450, y(th), "UNIT PRICE")
    c.drawRightString(RM, y(th), "LINE TOTAL")

    style = ParagraphStyle("d", fontName="Helvetica", fontSize=9.5, leading=12, textColor=TEXT)
    row_top = th + 21
    subtotal = 0.0
    for ln in spec["lines"]:
        qty = ln.get("qty", 1)
        total = qty * ln["unit_price"]
        subtotal += total
        p = Paragraph(ln["description"], style)
        pw, ph = p.wrap(300, 400)
        p.drawOn(c, 97, y(row_top) + 9.5 - ph)
        body(c, 52, row_top, str(qty))
        c.setFont("Helvetica", 9.5)
        c.setFillColor(TEXT)
        c.drawRightString(450, y(row_top), money(ln["unit_price"]))
        c.drawRightString(RM, y(row_top), money(total))
        row_top += ph + 10
    rule(c, row_top - 4)

    # Totals
    tt = row_top + 21
    body(c, 415, tt, "Subtotal")
    c.drawRightString(RM, y(tt), money(subtotal))
    body(c, 415, tt + 16, "Total")
    c.drawRightString(RM, y(tt + 16), money(subtotal))
    c.setFillColor(DUE_BG)
    c.rect(405, y(tt + 43), RM - 405, 25, fill=1, stroke=0)
    body(c, 415, tt + 35, "AMOUNT DUE", 11, NAVY, "Helvetica-Bold")
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(NAVY)
    c.drawRightString(RM, y(tt + 35), money(subtotal))

    c.setFont("Helvetica", 10)
    c.setFillColor(GREY)
    c.drawCentredString(W / 2, y(tt + 73), "Thank you for your business.")

    nt = tt + 82
    notes = spec.get("notes") or []
    if notes:
        rule(c, nt, NAVY, 1)
        label(c, LM, nt + 19, "LICENSE TERMS", 10)
        nstyle = ParagraphStyle("n", fontName="Helvetica", fontSize=8.5, leading=11, textColor=TEXT)
        ntop = nt + 32
        for line in notes:
            p = Paragraph(line, nstyle)
            pw, ph = p.wrap(RM - LM, 400)
            p.drawOn(c, LM, y(ntop) + 8.5 - ph)
            ntop += ph + 3
        nt = ntop + 6

    # Banking
    rule(c, nt, NAVY, 1)
    label(c, LM, nt + 19, "BANKING INFORMATION — USD", 10)
    cols = [LM, 220, 392]
    for i, (lab, vals) in enumerate(BANK):
        x = cols[i % 3]
        row = nt + 40 + (i // 3) * 34
        label(c, x, row, lab)
        for j, v in enumerate(vals):
            body(c, x, row + 10 + 10 * j, v, 8.5)

    # Payment link
    pt = nt + 40 + 2 * 34 + 2
    rule(c, pt, NAVY, 1)
    label(c, LM, pt + 19, spec.get("payment_link_label", "PAYMENT LINK"), 10)
    body(c, LM, pt + 38, spec["payment_link"], 9, LINK)
    c.linkURL(spec["payment_link"], (LM, y(pt + 46), RM, y(pt + 28)), relative=0)

    c.showPage()
    c.save()


if __name__ == "__main__":
    spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    build(spec, Path(sys.argv[2]))
    print("wrote", sys.argv[2])
