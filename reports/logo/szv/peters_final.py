"""Builds ../logo-concepts-4-peters.html: the Allan Peters-method round on Spencer's SZV mark.
Noun list -> 15 vector sketches -> top 3 refined -> pressure tests -> recommendation."""
import math, itertools, os
import szv_line as L
import peters_sketches as PS
from szv_line import SW, NAVY, CREAM, AMBER, VARIANTS

V = "soft"; Wd, a, s, Bv, r = VARIANTS[V]; H = L.H; D = L.d_attr(V)
OUT = os.path.dirname(os.path.abspath(__file__))
_id = itertools.count()


def cut_lines_svg(color="#000", sw=SW):
    return "".join(f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}" stroke="{color}" stroke-width="{L.CUT}"/>'
                   for p, q in L.cut_lines(V, sw=sw))


def p(color, sw):
    return f'<path d="{D}" fill="none" stroke="{color}" stroke-width="{sw:.1f}" stroke-linejoin="miter" stroke-miterlimit="12"/>'


def masked(color, sw, mask_inner):
    uid = f"f{next(_id)}"
    return (f'<mask id="{uid}" maskUnits="userSpaceOnUse" x="-2000" y="-2000" width="4000" height="4000">'
            f'<rect x="-2000" y="-2000" width="4000" height="4000" fill="#fff"/>{mask_inner}</mask>'
            f'<g mask="url(#{uid})">{p(color, sw)}</g>')


# ---- the three finalists, refined (true knockouts, so they work on any background) ----
def solid(color):                       # the base mark = small-size partner for all three
    return masked(color, SW, cut_lines_svg())


def resonance(color):
    # Inline: outer rails + centre line, all ~equal weight (three 9-unit lines, two 8-unit gaps)
    uid = f"f{next(_id)}"
    return (f'<mask id="{uid}" maskUnits="userSpaceOnUse" x="-2000" y="-2000" width="4000" height="4000">'
            f'<rect x="-2000" y="-2000" width="4000" height="4000" fill="#000"/>{p("#fff", SW)}{p("#000", SW*0.52)}{p("#fff", SW*0.2)}'
            f'{cut_lines_svg()}</mask><g mask="url(#{uid})"><rect x="-600" y="-300" width="1200" height="1000" fill="{color}"/></g>')


def on_air(color, accent=None):
    accent = accent or color
    arcs = ""
    for R in (372, 440):                     # reduced from 3 arcs to 2: the third added nothing
        ang = math.radians(15)
        x1, y1 = -R * math.sin(ang), Bv - R * math.cos(ang)
        arcs += f'<path d="M{x1:.1f},{y1:.1f} A{R},{R} 0 0 1 {-x1:.1f},{y1:.1f}" fill="none" stroke="{accent}" stroke-width="30" stroke-linecap="round"/>'
    return solid(color) + arcs


def signal(color):
    # heavier stroke, 3 scan lines splitting the height into equal bands; line width tied to the sliver gap
    lines = "".join(f'<rect x="-2000" y="{y - L.CUT*0.75:.1f}" width="4000" height="{L.CUT*1.5:.1f}" fill="#000"/>' for y in (H * .25, H * .5, H * .75))
    return masked(color, SW * 1.25, cut_lines_svg(sw=SW * 1.25) + lines)


FINALS = [
    ("01 · Resonance", resonance, "-380 -100 760 600", "-380 -140 760 760",
     "Your one line, echoed. I took the inline technique I use on badges and ran your SZV line through it, "
     "so it reads as a voice that rings in the room. One idea, very ownable. At small sizes it hands off to the solid mark, which is how a logo system should work."),
    ("02 · On Air", on_air, "-380 -260 760 760", "-420 -280 840 840",
     "The V opens like a mouth and two signal arcs come out of it. Two ideas in one mark: your initials and a broadcast. "
     "I cut it from three arcs to two; the third added nothing, and that's the line where simplifying stops."),
    ("11 · Signal", signal, "-390 -100 780 600", "-380 -140 760 760",
     "The same line, heavier, cut by three scan lines that split it into equal bands. It reads as transmission, it's bold enough to hold at 16px, "
     "and the scan lines match the width of the sliver you asked for, so it's one consistent system."),
]


def svgwrap(inner, vb, bg, w="100%", rx=14):
    return f'<svg viewBox="{vb}" width="{w}" style="display:block;background:{bg};border-radius:{rx}px">{inner}</svg>'


def icon(fn, fg, bg, px, vb):
    x, y, w, h = map(float, vb.split()); sq = max(w, h); x -= (sq - w) / 2; y -= (sq - h) / 2
    pad = sq * 0.14; x -= pad; y -= pad; sq += 2 * pad
    small = fn is resonance and px <= 48          # responsive: the inline mark hands off to the solid one
    body = solid(fg) if small else (fn(fg) if fn is not on_air else on_air(fg, AMBER if fg != AMBER else fg))
    return (f'<svg viewBox="{x:.0f} {y:.0f} {sq:.0f} {sq:.0f}" width="{px}" height="{px}">'
            f'<rect x="{x:.0f}" y="{y:.0f}" width="{sq:.0f}" height="{sq:.0f}" rx="{sq*0.22:.0f}" fill="{bg}"/>{body}</svg>')


HOSTILE = ('<defs><pattern id="hz" width="60" height="60" patternUnits="userSpaceOnUse" patternTransform="rotate(30)">'
           '<rect width="60" height="60" fill="#c43d2b"/><rect width="30" height="60" fill="#2c7a4b"/></pattern></defs>'
           '<rect x="-2000" y="-2000" width="4000" height="4000" fill="url(#hz)"/>')

finals_html = ""
for title, fn, vb, vbsq, why in FINALS:
    big_dark = svgwrap(fn(AMBER) if fn is not on_air else on_air(CREAM, AMBER), vb, NAVY)
    big_light = svgwrap(fn(NAVY) if fn is not on_air else on_air(NAVY, "#D9971F"), vb, CREAM)
    one_black = svgwrap(fn("#000"), vb, "#fff")
    hostile = svgwrap(HOSTILE + (fn("#fff")), vb, "#000")
    lock = (f'<div class="lock">{svgwrap(fn(AMBER) if fn is not on_air else on_air(CREAM, AMBER), vb, "transparent", w="130px", rx=0)}'
            f'<div class="wm"><span class="name">SPENCER Z</span><span class="tag">VOICEOVERS</span></div></div>')
    smalls = "".join(f'<figure>{icon(fn, CREAM if fn is not on_air else CREAM, NAVY, px, vbsq)}{px}px</figure>' for px in (96, 48, 32, 16))
    finals_html += f'''<section class="final"><h3>{title}</h3><p class="why">{why}</p>
<div class="g2">{big_dark}{big_light}</div>
<div class="tests"><figure>{one_black}<figcaption>one colour</figcaption></figure><figure>{hostile}<figcaption>hostile background</figcaption></figure>
<figure class="lk">{lock}<figcaption>lockup</figcaption></figure></div>
<div class="smalls">{smalls}</div></section>'''

NOUNS = [("Sound", "voice, soundwave, echo / reverb, resonance, low frequency"),
         ("Gear", "microphone, pop filter, headphones, booth, VU meter"),
         ("Broadcast", "on-air light, signal, transmission, airwaves"),
         ("Speech", "mouth, speech bubble, quotation marks, script"),
         ("Spencer", "S · Z · V initials, the one line, Lisbon (azulejo tile), returning clients (loop)")]
nouns_html = "".join(f'<div class="noun"><b>{k}</b><span>{v}</span></div>' for k, v in NOUNS)

html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>SZV Peters Method</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Work+Sans:wght@400;500;600&family=Fraunces:wght@600&display=swap" rel="stylesheet">
<style>
:root{{--navy:{NAVY};--cream:{CREAM};--amber:{AMBER};--soft:#A9B2BE;--surface:#141B25}}
*{{box-sizing:border-box}}
body{{margin:0;background:#06080c;color:var(--cream);font-family:"Work Sans",system-ui,sans-serif;padding:32px 16px 72px;line-height:1.5}}
main{{max-width:1120px;margin:0 auto}}
h1{{font-family:"Space Grotesk";font-weight:600;font-size:26px;margin:0 0 6px}}
h2{{font-family:"Space Grotesk";font-weight:600;font-size:18px;color:var(--amber);margin:44px 0 6px}}
h3{{font-family:"Space Grotesk";font-weight:600;font-size:17px;margin:0 0 4px;color:var(--amber)}}
.lede{{color:var(--soft);max-width:72ch;margin:0}}
.steps{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:18px}}
.step{{background:var(--surface);border-radius:12px;padding:14px}} .step b{{display:block;font-family:"Space Grotesk";margin-bottom:4px}} .step span{{color:var(--soft);font-size:13.5px}}
.nouns{{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin-top:10px}}
.noun{{background:var(--surface);border-radius:12px;padding:12px;font-size:13.5px}} .noun b{{display:block;color:var(--amber);font-family:"Space Grotesk"}} .noun span{{color:var(--soft)}}
.sketches{{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin-top:12px}}
.sketches figure{{margin:0}} .sketches figcaption{{display:flex;flex-direction:column;font-size:12.5px;margin-top:5px}} .sketches figcaption span{{color:var(--soft)}}
.final{{background:#0d1219;border:1px solid #1d2531;border-radius:16px;padding:20px;margin-top:16px}}
.why{{color:var(--soft);margin:0 0 14px;max-width:80ch;font-size:14.5px}}
.g2{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}
.tests{{display:grid;grid-template-columns:1fr 1fr 1.4fr;gap:10px;margin-top:10px}} .tests figure{{margin:0}} .tests figcaption{{font-size:12px;color:var(--soft);margin-top:4px}}
.lk .lock{{background:var(--navy);border-radius:14px;height:calc(100% - 22px);display:flex;align-items:center;justify-content:center;gap:18px;padding:16px}}
.wm{{display:flex;flex-direction:column;line-height:1}} .name{{font-family:"Space Grotesk";font-weight:600;font-size:26px;letter-spacing:.14em}} .tag{{font-weight:600;font-size:10.5px;letter-spacing:.6em;margin-top:8px;opacity:.7}}
.smalls{{display:flex;gap:18px;align-items:flex-end;margin-top:10px;padding:14px 16px;background:var(--surface);border-radius:12px;flex-wrap:wrap}}
.smalls figure{{margin:0;display:flex;flex-direction:column;align-items:center;gap:6px;font-size:11px;color:var(--soft)}}
.verdict{{background:var(--amber);color:#1C1405;border-radius:16px;padding:20px 22px;margin-top:28px}} .verdict h2{{color:#1C1405;margin:0 0 6px}} .verdict p{{margin:0 0 8px}}
.src{{color:var(--soft);font-size:12.5px;margin-top:36px}} .src a{{color:var(--soft)}}
@media (max-width:820px){{.steps,.nouns{{grid-template-columns:1fr 1fr}} .sketches{{grid-template-columns:repeat(3,1fr)}} .g2,.tests{{grid-template-columns:1fr}}}}
</style></head><body><main>
<h1>SZV: the Allan Peters method</h1>
<p class="lede">I ran your SZV through Allan Peters' published process (designer behind Peters Design Company, author of <i>Logos That Last</i>) and made the calls the way he describes making them. Where his own words drive a decision, the step says so.</p>
<div class="steps">
 <div class="step"><b>1 · Brand noun list</b><span>Before drawing anything, list what the mark could be, so you don't design stars for a client who hates stars.</span></div>
 <div class="step"><b>2 · Rough sketches, wide</b><span>Ugly on purpose, lots of them. He shows clients 15 vector sketches, not 3, so the one they "wished for" is already on the table.</span></div>
 <div class="step"><b>3 · Combine ideas</b><span>"Usually it's multiple ideas": two nouns in one mark, using negative space, overlapping geometry, visual rhythm, visual flow.</span></div>
 <div class="step"><b>4 · Narrow, reduce, test</b><span>Pick a top 3 by gut, strip each until it stops communicating, then check the curves, stroke weight and spacing at 16px and on hostile backgrounds.</span></div>
</div>

<h2>1 · Brand noun list</h2>
<div class="nouns">{nouns_html}</div>

<h2>2 · Fifteen sketches: SZV plus one more idea</h2>
<p class="lede">Every sketch keeps your one-line SZV and pairs it with a noun from the list. Rough, not precious.</p>
<div class="sketches">{PS.CARDS}</div>

<h2>3 · Top three, refined and pressure-tested</h2>
<p class="lede">Each one is shown on your navy and cream, in one colour, on a deliberately hostile background, as a lockup with your name, and at 96, 48, 32 and 16px.</p>
{finals_html}

<div class="verdict"><h2>If I'm Allan: my call</h2>
<p><b>01 · Resonance as the primary mark, with the solid SZV as its small-size partner.</b> It's the only one of the three that couldn't belong to anyone else. It keeps your one-line idea and adds the thing you sell: a voice that fills the room. On Air explains itself more, but radio arcs are a category cliché. Signal is the strongest at tiny sizes, so it's the fallback if you want one mark that does everything without a partner.</p>
<p>He'd also push you here rather than follow: lead the client, take the creative risk. Resonance is that risk.</p></div>

<p class="src">Sources: <a href="https://logogeek.uk/podcast/badge-logos-allan-peters">Logo Geek podcast, "On Target To Design Badge Logos"</a> (brand noun list, 15 vector sketches, top three, combining ideas, badge inlining) · <a href="https://theangrydesigner.com/episodes/a-conversation-with-allan-peters-logo-process-bad-customers-a-gunshot-wound/">The Angry Designer podcast</a> (rough "ugly" sketches, ~70 ideas narrowed down, negative space / overlapping geometry / visual rhythm / visual flow) · <a href="https://weandthecolor.com/logos-that-last-how-allan-peters-turns-visual-branding-into-enduring-identity/209357">WE AND THE COLOR on <i>Logos That Last</i></a> (curve geometry, stroke weight and optical spacing; reads at 16px; simplify until meaning would go; pressure tests) · <a href="https://www.adobe.com/max/2025/sessions/design-the-logo-sell-the-logo-chase-the-dream-s6001.html">Adobe MAX 2025 session</a> (leading clients, creative risk) · <a href="https://www.petersdesigncompany.com/">petersdesigncompany.com</a> (portfolio).</p>
</main></body></html>'''

open(os.path.join(OUT, "..", "logo-concepts-4-peters.html"), "w", encoding="utf-8").write(html)
print("ok")
