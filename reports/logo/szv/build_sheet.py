"""Builds ../logo-concepts-3-szv.html from szv_line.py so the sheet never drifts from the SVG exports."""
import itertools, os
import szv_line as L
from szv_line import VARIANTS, SW, NAVY, CREAM, AMBER

_ids = itertools.count()

def mk(n, color, width, pad=SW * 1.6):
    x, y, w, h = L.bbox(n, pad)
    return f'<svg viewBox="{x:.1f} {y:.1f} {w:.1f} {h:.1f}" width="{width}">{L.path_el(n, color, f"m{next(_ids)}")}</svg>'

def av(n, fg, bg, size, circle=True):
    x, y, w, h = L.bbox(n, 200); s = max(w, h); x -= (s - w) / 2; y -= (s - h) / 2
    shape = (f'<circle cx="{x+s/2:.1f}" cy="{y+s/2:.1f}" r="{s/2:.1f}" fill="{bg}"/>' if circle else
             f'<rect x="{x:.1f}" y="{y:.1f}" width="{s:.1f}" height="{s:.1f}" rx="{s*0.22:.1f}" fill="{bg}"/>')
    return f'<svg viewBox="{x:.1f} {y:.1f} {s:.1f} {s:.1f}" width="{size}" height="{size}">{shape}{L.path_el(n, fg, f"m{next(_ids)}")}</svg>'

names = {"sharp": "1 · Sharp", "soft": "2 · Soft tips", "deep": "3 · Deep V"}
notes = {"sharp": "wide V, crisp pointed corners. Closest to the reference marks (VAIO, Raptors, Yankees).",
         "soft": "same build, with the two outer top corners rounded like your original SZV. Warmer, more \"voice\".",
         "deep": "narrower, deeper V, so the S, V and Z read as three separate letters. Busier when small."}

sec = ""
for n in VARIANTS:
    sec += f'''<section><h2>{names[n]} <span>{notes[n]}</span></h2>
<div class="row3">
 <div class="tile" style="background:#fff">{mk(n, "#000", 230)}</div>
 <div class="tile" style="background:{NAVY}">{mk(n, AMBER, 230)}</div>
 <div class="tile" style="background:{CREAM}">{mk(n, NAVY, 230)}</div>
</div>
<div class="row">
 <div class="tile dark"><div class="lock">{mk(n, AMBER, 120, pad=SW*.6)}<div class="wm"><span class="name">SPENCER Z</span><span class="tag">VOICEOVERS</span></div></div></div>
 <div class="tile light"><div class="stack">{mk(n, NAVY, 140, pad=SW*.6)}<span class="name">SPENCER Z</span><span class="tag">VOICEOVERS</span></div></div>
</div>
<div class="smalls">
 <figure>{av(n, AMBER, NAVY, 96)}avatar</figure>
 <figure>{av(n, NAVY, AMBER, 96)}avatar alt</figure>
 <figure>{av(n, CREAM, NAVY, 48, False)}48px</figure>
 <figure>{av(n, CREAM, NAVY, 32, False)}32px</figure>
 <figure>{av(n, CREAM, NAVY, 16, False)}16px</figure>
</div></section>'''

html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>SZV One-Line Logo</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600&family=Work+Sans:wght@500;600&display=swap" rel="stylesheet">
<style>
:root{{--navy:{NAVY};--cream:{CREAM};--amber:{AMBER};--soft:#A9B2BE;--surface:#141B25}}
*{{box-sizing:border-box}}
body{{margin:0;background:#06080c;color:var(--cream);font-family:"Work Sans",system-ui,sans-serif;padding:32px 16px 64px}}
h1,.sub,section{{max-width:1100px;margin-inline:auto}}
h1{{font-family:"Space Grotesk";font-weight:600;font-size:22px;margin-top:0;margin-bottom:4px}}
.sub{{color:var(--soft);font-size:14px;margin-bottom:28px;line-height:1.5}}
section{{margin-bottom:44px}}
h2{{font-family:"Space Grotesk";font-weight:600;font-size:16px;margin:0 0 10px;color:var(--amber)}}
h2 span{{color:var(--soft);font-weight:500;font-family:"Work Sans";margin-left:8px;font-size:14px}}
.row,.row3{{display:grid;gap:12px;margin-bottom:12px}} .row{{grid-template-columns:1fr 1fr}} .row3{{grid-template-columns:repeat(3,1fr)}}
.tile{{border-radius:14px;padding:32px 20px;display:flex;align-items:center;justify-content:center;min-height:200px}}
.tile svg{{max-width:100%;height:auto}}
.dark{{background:var(--navy);border:1px solid #1d2531;color:var(--cream)}} .light{{background:var(--cream);color:var(--navy)}}
.lock{{display:flex;align-items:center;gap:22px}} .wm{{display:flex;flex-direction:column;line-height:1}}
.name{{font-family:"Space Grotesk";font-weight:600;font-size:34px;letter-spacing:.14em}}
.tag{{font-family:"Work Sans";font-weight:600;font-size:12px;letter-spacing:.62em;margin-top:10px;opacity:.7}}
.stack{{display:flex;flex-direction:column;align-items:center;line-height:1}} .stack .name{{margin-top:22px;font-size:28px;padding-left:.14em}} .stack .tag{{padding-left:.62em}}
.smalls{{display:flex;gap:18px;align-items:flex-end;padding:16px 20px;background:var(--surface);border-radius:12px;flex-wrap:wrap}}
.smalls figure{{margin:0;display:flex;flex-direction:column;align-items:center;gap:6px;font-size:11px;color:var(--soft)}}
@media (max-width:760px){{.row,.row3{{grid-template-columns:1fr}} .lock{{flex-direction:column}} .name{{font-size:26px}}}}
</style></head><body>
<h1>SZV one-line logo</h1>
<p class="sub">Your SZV monogram as one line: up the Z, down into the V, up to the S and down its bottom bar, with an even stroke weight throughout. A thin sliver now separates each leg of the V from the S and Z top bars. Shown in black on white, in your site colours, as a lockup with your name, and at avatar and favicon sizes.</p>
{sec}</body></html>'''

open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logo-concepts-3-szv.html"), "w", encoding="utf-8").write(html)
print("sheet ok")
