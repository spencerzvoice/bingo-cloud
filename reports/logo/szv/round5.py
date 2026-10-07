"""Round 5: eight new SZV designs, more Peters techniques (negative space, knockout shapes,
visual rhythm, overlapping colour, stencil breaks). Builds ../logo-concepts-5.html."""
import math, itertools, os
import szv_line as L
from szv_line import NAVY, CREAM, AMBER, VARIANTS

OUT = os.path.dirname(os.path.abspath(__file__))
TEAL, CORAL = "#3FA7B5", "#E4572E"
Wd, a, s, Bv, r = VARIANTS["soft"]; H = L.H
_id = itertools.count()


def uid():
    return f"r{next(_id)}"


def poly(pts):
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def stroke(d, color, sw, join="miter", cap="butt", extra=""):
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linejoin="{join}" '
            f'stroke-miterlimit="12" stroke-linecap="{cap}" {extra}/>')


def mask(inner, base="#fff"):
    i = uid()
    return i, (f'<mask id="{i}" maskUnits="userSpaceOnUse" x="-3000" y="-3000" width="6000" height="6000">'
               f'<rect x="-3000" y="-3000" width="6000" height="6000" fill="{base}"/>{inner}</mask>')


# --- shared geometry -------------------------------------------------------------------------
SOFT = L.d_attr("soft")
CUTS = lambda sw=L.SW: "".join(f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}" stroke="#000" stroke-width="{L.CUT}"/>'
                               for p, q in L.cut_lines("soft", sw=sw))


def soft_mark(color, sw=L.SW, extra_mask=""):
    i, m = mask(CUTS(sw) + extra_mask)
    return m + stroke(SOFT, color, sw, extra=f'mask="url(#{i})"')


# Hidden V: S and Z only; the V is the space between their diagonals
HV_SW, HV_GAP, HV_W, HV_A = 64, 58, 300, 48
def hidden_v_paths():
    z = poly([(HV_W, H), (HV_A, H), (HV_W, 0), (HV_GAP, 0)])
    s_ = poly([(-HV_W, H), (-HV_A, H), (-HV_W, 0), (-HV_GAP, 0)])
    return z, s_


def hidden_v(color, sw=HV_SW):
    z, s_ = hidden_v_paths()
    return stroke(z, color, sw) + stroke(s_, color, sw)


# --- the eight designs ------------------------------------------------------------------------
def d1(fg, bg):     # Hidden V
    return hidden_v(fg)


def d2(fg, bg):     # Hidden V knocked out of a solid circle
    i, m = mask(hidden_v("#000"))
    return m + f'<circle cx="0" cy="200" r="400" fill="{fg}" mask="url(#{i})"/>'


def d3(fg, bg):     # Shield: the point of the shield repeats the V
    shield = "M-400,-110 H400 V250 Q400,330 330,390 L0,640 L-330,390 Q-400,330 -400,250 Z"
    i, m = mask(f'<g transform="translate(0,20) scale(.86)">{hidden_v("#000")}</g>')
    return m + f'<path d="{shield}" fill="{fg}" mask="url(#{i})"/>'


def d4(fg, bg):     # Retro stripes: thick mark cut into horizontal bands
    bands = "".join(f'<rect x="-3000" y="{y}" width="6000" height="11" fill="#000"/>' for y in range(-60, 480, 30))
    i, m = mask(bands)
    return m + f'<g mask="url(#{i})">{hidden_v(fg, sw=96)}</g>'


def d5(fg, bg):     # Overlap: S, V, Z as three transparent pieces that overlap at the joins
    ext = 30
    z = poly([(Wd, H), (a, H), (Wd, 0), (s - ext, 0)])
    v = poly([(s + ext * .4 * s / Bv, -ext * .4), (0, Bv), (-s - ext * .4 * s / Bv, -ext * .4)])
    s_ = poly([(-s + ext, 0), (-Wd, 0), (-a, H), (-Wd, H)])
    blend = 'style="mix-blend-mode:multiply"' if bg == CREAM else 'opacity=".9"'
    cols = (AMBER, CORAL, TEAL)
    c = uid()
    clip = f'<clipPath id="{c}"><rect x="-1000" y="-26" width="2000" height="1000"/></clipPath>'
    return clip + f'<g clip-path="url(#{c})">' + "".join(f'<g {blend}>{stroke(d, col, 52)}</g>' for d, col in ((s_, cols[0]), (v, cols[1]), (z, cols[2]))) + "</g>"


def d6(fg, bg):     # Rounded: friendly, every join and end rounded
    return stroke(SOFT, fg, 58, join="round", cap="round")


def d7(fg, bg):     # Stencil: the sliver idea taken to every corner; every cut is horizontal and even
    sw, g = L.SW, 14; h = sw / 2
    k = (Wd - a) / H; hw = h * math.sqrt(1 + k * k)
    xc = lambda y: a + k * (H - y); xo = lambda y: xc(y) + hw; xi = lambda y: xc(y) - hw
    kv = s / Bv; hv = h * math.sqrt(1 + kv * kv)
    y1, y2 = h + g, H - h - g
    half = (poly([(s - hv, -h), (xo(-h), -h), (xo(h), h), (s - hv, h)]) + "Z " +                 # top bar
            poly([(xi(H - h), H - h), (Wd, H - h), (Wd, H + h), (xi(H + h), H + h)]) + "Z " +    # bottom bar
            poly([(xi(y1), y1), (xo(y1), y1), (xo(y2), y2), (xi(y2), y2)]) + "Z")               # diagonal
    c = uid()
    v = (f'<clipPath id="{c}"><rect x="-1000" y="{y1}" width="2000" height="1000"/></clipPath>'
         + stroke(poly([(s, -40), (0, Bv), (-s, -40)]), fg, sw, extra=f'clip-path="url(#{c})"'))
    return (f'<path d="{half}" fill="{fg}"/><g transform="scale(-1,1)"><path d="{half}" fill="{fg}"/></g>' + v)


def d8(fg, bg):     # Ring break: the S and Z tips break out through a ring
    gap = stroke(SOFT, "#000", L.SW + 44)
    i, m = mask(f'<g transform="translate(0,-6) scale(1.12)">{gap}</g>')
    ring = f'<circle cx="0" cy="210" r="330" fill="none" stroke="{AMBER if fg != NAVY else "#D9971F"}" stroke-width="22" mask="url(#{i})"/>'
    return m + ring + f'<g transform="translate(0,-6) scale(1.12)">{soft_mark(fg)}</g>'


DESIGNS = [
    ("Hidden V", d1, "-400 -140 800 680",
     "No V stroke at all. The S and the Z lean into each other and the V is the space between them, so people find the third letter themselves. Pure negative space."),
    ("Hidden V · Coin", d2, "-440 -240 880 880",
     "The same mark knocked out of a solid disc: one bold shape that's ready for an avatar, a sticker or a favicon."),
    ("Shield", d3, "-440 -150 880 830",
     "The hidden-V mark in a shield whose point repeats the V. It reads as a crest, which feels established and premium."),
    ("Retro Stripes", d4, "-420 -140 840 680",
     "Heavy letters cut into even horizontal bands: visual rhythm, like sound bars or 70s broadcast graphics. Loud and confident."),
    ("Three Voices", d5, "-400 -140 800 680",
     "S, V and Z as three transparent pieces that overlap where they meet, so the joins become new colours. Overlapping geometry, more playful."),
    ("Rounded", d6, "-400 -140 800 680",
     "Your one line with every corner and end rounded. Warm and friendly, closer to how you sound than the sharp version."),
    ("Stencil", d7, "-400 -140 800 680",
     "Your sliver idea taken to every corner, so the line breaks into clean pieces like a stencil. Crisp and engineered."),
    ("Ring Break", d8, "-440 -180 880 800",
     "A ring around the mark that the S and Z tips break through. A small twist on the badge: the voice won't stay in the box."),
]


def svgwrap(inner, vb, bg, w="100%"):
    return f'<svg viewBox="{vb}" width="{w}" style="display:block;background:{bg};border-radius:14px">{inner}</svg>'


def icon(fn, px, vb):
    x, y, w, h = map(float, vb.split()); sq = max(w, h); x -= (sq - w) / 2; y -= (sq - h) / 2
    return (f'<svg viewBox="{x:.0f} {y:.0f} {sq:.0f} {sq:.0f}" width="{px}" height="{px}">'
            f'<rect x="{x:.0f}" y="{y:.0f}" width="{sq:.0f}" height="{sq:.0f}" rx="{sq*0.22:.0f}" fill="{NAVY}"/>{fn(CREAM if fn not in (d2, d3) else AMBER, NAVY)}</svg>')


cards = ""
for n, (title, fn, vb, why) in enumerate(DESIGNS, 1):
    dark_fg = AMBER if fn not in (d6,) else CREAM
    cards += f'''<article><h3><span>{n:02d}</span>{title}</h3><p>{why}</p>
<div class="pair">{svgwrap(fn(dark_fg, NAVY), vb, NAVY)}{svgwrap(fn(NAVY, CREAM), vb, CREAM)}</div>
<div class="smalls">{"".join(f"<figure>{icon(fn, px, vb)}{px}px</figure>" for px in (64, 32, 16))}
<div class="lock">{svgwrap(fn(AMBER if fn not in (d6,) else CREAM, NAVY), vb, "transparent", w="70px")}<div class="wm"><span class="name">SPENCER Z</span><span class="tag">VOICEOVERS</span></div></div></div>
</article>'''

html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>SZV Round Five</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Work+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{{--navy:{NAVY};--cream:{CREAM};--amber:{AMBER};--soft:#A9B2BE;--surface:#141B25}}
*{{box-sizing:border-box}}
body{{margin:0;background:#06080c;color:var(--cream);font-family:"Work Sans",system-ui,sans-serif;padding:32px 16px 72px;line-height:1.5}}
main{{max-width:1180px;margin:0 auto}}
h1{{font-family:"Space Grotesk";font-weight:600;font-size:26px;margin:0 0 6px}}
.lede{{color:var(--soft);max-width:78ch;margin:0 0 22px}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
article{{background:#0d1219;border:1px solid #1d2531;border-radius:16px;padding:18px}}
h3{{font-family:"Space Grotesk";font-weight:600;font-size:18px;margin:0 0 4px;display:flex;gap:10px;align-items:baseline}}
h3 span{{color:var(--amber);font-size:14px}}
article p{{color:var(--soft);font-size:14px;margin:0 0 12px;min-height:3em}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:8px}}
.smalls{{display:flex;gap:14px;align-items:flex-end;margin-top:10px;padding:12px 14px;background:var(--surface);border-radius:12px;flex-wrap:wrap}}
.smalls figure{{margin:0;display:flex;flex-direction:column;align-items:center;gap:5px;font-size:11px;color:var(--soft)}}
.lock{{margin-left:auto;display:flex;align-items:center;gap:12px}}
.wm{{display:flex;flex-direction:column;line-height:1}} .name{{font-family:"Space Grotesk";font-weight:600;font-size:17px;letter-spacing:.14em}} .tag{{font-weight:600;font-size:8.5px;letter-spacing:.55em;margin-top:6px;opacity:.7}}
.verdict{{background:var(--amber);color:#1C1405;border-radius:16px;padding:20px 22px;margin-top:22px}} .verdict h2{{font-family:"Space Grotesk";margin:0 0 6px;font-size:19px}} .verdict p{{margin:0}}
@media (max-width:860px){{.grid{{grid-template-columns:1fr}}}}
</style></head><body><main>
<h1>SZV, round five: eight new directions</h1>
<p class="lede">A fresh set, each one pushing a different technique from Allan Peters' toolkit (negative space, a bold knocked-out shape, visual rhythm, overlapping colour, a twist on the badge). All of them keep your S, Z and V. Each is shown on navy and cream, as an app icon at 64, 32 and 16px, and next to your name.</p>
<div class="grid">{cards}</div>
<div class="verdict"><h2>My pick: 01 Hidden V (and 02 for the avatar)</h2>
<p>It's the smartest idea on the page. Two letters do the work of three, and the V appears in the gap between them, which is exactly the kind of moment people remember. It's also the simplest shape here, so it holds at 16px. Use the coin version (02) for Instagram, LinkedIn, Google and the favicon.</p><p style="margin-top:8px"><b>Runner-up: 07 Stencil.</b> It's the cleanest version of your own sliver idea and looks the most premium, but it keeps the V as a drawn letter, so there's less of a surprise.</p></div>
</main></body></html>'''

open(os.path.join(OUT, "..", "logo-concepts-5.html"), "w", encoding="utf-8").write(html)
print("ok", len(DESIGNS))
