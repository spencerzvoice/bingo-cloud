"""T-shirt mockups with the SZV mark only (no wordmark) + print-ready mark files.
Builds ../tee-mockups.html and print/szv-print-*.svg. Mark = final geometry, stroke 68."""
import os
OUT = os.path.dirname(os.path.abspath(__file__))
P = "M300,400 L40,400 L300,0 L110,0 L0,290 L-110,0 L-300,0 L-40,400 L-300,400"
NAVY, CREAM, AMBER, BLACK, HEATHER, WHITE = "#0B0F15", "#F1ECE3", "#F0B13C", "#151515", "#8B8F96", "#F7F6F2"


def mark(color, cx, cy, width):
    """The mark centred on (cx, cy), `width` = the mark's visual width (600 units + miter tips)."""
    s = width / 680.0
    return (f'<g transform="translate({cx},{cy}) scale({s:.4f}) translate(0,-200)">'
            f'<path d="{P}" fill="none" stroke="{color}" stroke-width="68" stroke-linejoin="miter" stroke-miterlimit="12"/></g>')


# Front tee silhouette on a 600x640 canvas
FRONT = ("M214,58 C240,82 360,82 386,58 L470,88 L580,172 L520,262 L470,232 L470,610 Q470,622 458,622 "
         "L142,622 Q130,622 130,610 L130,232 L80,262 L20,172 L130,88 Z")
COLLAR = "M214,58 C240,82 360,82 386,58 C372,104 228,104 214,58 Z"
BACK_COLLAR = "M214,58 C240,70 360,70 386,58 C366,74 234,74 214,58 Z"


def tee(body, ink, placement, back=False, label=""):
    collar = BACK_COLLAR if back else COLLAR
    shade = ('<defs><linearGradient id="g{0}" x1="0" x2="1"><stop offset="0" stop-color="#000" stop-opacity=".18"/>'
             '<stop offset=".22" stop-color="#000" stop-opacity="0"/><stop offset=".78" stop-color="#000" stop-opacity="0"/>'
             '<stop offset="1" stop-color="#000" stop-opacity=".18"/></linearGradient></defs>').format(label)
    art = {
        "left-chest": mark(ink, 372, 200, 62),      # wearer's left chest = viewer's right
        "centre-chest": mark(ink, 300, 240, 130),
        "big-front": mark(ink, 300, 300, 200),
        "back-yoke": mark(ink, 300, 128, 70),
        "back-big": mark(ink, 300, 300, 200),
        "sleeve": mark(ink, 520, 200, 48),
        "tonal": mark(ink, 372, 200, 62),
    }[placement]
    return (f'<svg viewBox="0 0 600 640" role="img" aria-label="{label}">{shade}'
            f'<path d="{FRONT}" fill="{body}"/><path d="{FRONT}" fill="url(#g{label})"/>'
            f'<path d="{collar}" fill="#000" opacity=".22"/>'
            f'<path d="M130,232 L130,610 M470,232 L470,610" stroke="#000" stroke-opacity=".08" stroke-width="2"/>{art}</svg>')


LOOKS = [
    ("Left chest · amber on navy", NAVY, AMBER, "left-chest", False,
     "The classic. Small mark where a pocket would be. Screen print or embroidery."),
    ("Centre chest · amber on black", BLACK, AMBER, "centre-chest", False,
     "Bigger and bolder, still clean. Best as a one-colour screen print."),
    ("Big front · navy on cream", CREAM, NAVY, "big-front", False,
     "Statement piece. The shape carries it on its own, no words needed."),
    ("Tonal · navy on navy", NAVY, "#1F2A3A", "tonal", False,
     "Quiet luxury: dark ink on a dark shirt, only visible up close. Great as embroidery."),
    ("Back yoke · amber on navy", NAVY, AMBER, "back-yoke", True,
     "Small mark under the collar on the back. Pairs with a plain or left-chest front."),
    ("Big back · cream on heather grey", HEATHER, CREAM, "back-big", True,
     "Large back print, plain front. Reads from across a room or a stage."),
]


def card(title, body, ink, place, back, note, i):
    side = "Back" if back else "Front"
    return (f'<figure><div class="tee">{tee(body, ink, place, back, f"t{i}")}</div>'
            f'<figcaption><b>{title}</b><span class="side">{side}</span><p>{note}</p></figcaption></figure>')


cards = "".join(card(*l, i) for i, l in enumerate(LOOKS))

html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>SZV Tee Mockups</title>
<link href="https://fonts.googleapis.com/css2?family=Lexend+Exa:wght@500&family=Work+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{{--navy:{NAVY};--cream:{CREAM};--amber:{AMBER};--soft:#A9B2BE;--surface:#141B25}}
*{{box-sizing:border-box}}
body{{margin:0;background:#06080c;color:var(--cream);font-family:"Work Sans",system-ui,sans-serif;padding:32px 16px 64px;line-height:1.5}}
main{{max-width:1180px;margin:0 auto}}
h1{{font-family:"Lexend Exa";font-weight:500;font-size:24px;letter-spacing:.04em;margin:0 0 6px}}
.lede{{color:var(--soft);margin:0 0 24px;max-width:72ch}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:16px}}
figure{{margin:0;background:var(--surface);border-radius:18px;padding:14px;display:flex;flex-direction:column}}
.tee{{background:radial-gradient(circle at 50% 40%,#E9E5DD 0%,#CFC9BE 100%);border-radius:12px;padding:18px 18px 6px}}
.tee svg{{display:block;width:100%;height:auto}}
figcaption{{padding:12px 4px 2px;position:relative}}
figcaption b{{font-weight:600}} .side{{position:absolute;right:4px;top:12px;font-size:12px;color:var(--amber);letter-spacing:.12em;text-transform:uppercase}}
figcaption p{{margin:4px 0 0;color:var(--soft);font-size:14px}}
@media (max-width:420px){{.grid{{grid-template-columns:1fr}}}}
</style></head><body><main>
<h1>SZV tees · mark only</h1>
<p class="lede">Just the mark, no wordmark. Six ways to wear it, on the brand colours. Sizes are drawn roughly to scale for an adult medium tee: left chest ≈ 9 cm wide, centre chest ≈ 20 cm, big front/back ≈ 30 cm.</p>
<div class="grid">{cards}</div>
</main></body></html>'''

open(os.path.join(OUT, "..", "tee-mockups.html"), "w", encoding="utf-8").write(html)

# Print-ready vector files: mark only, transparent background, one colour each
os.makedirs(os.path.join(OUT, "print"), exist_ok=True)
for name, col in (("amber", AMBER), ("navy", NAVY), ("cream", CREAM), ("black", "#000000"), ("white", "#FFFFFF")):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-375 -50 750 500" width="300mm" height="200mm">'
           f'<path d="{P}" fill="none" stroke="{col}" stroke-width="68" stroke-linejoin="miter" stroke-miterlimit="12"/></svg>\n')
    open(os.path.join(OUT, "print", f"szv-print-{name}.svg"), "w").write(svg)
print("ok")
