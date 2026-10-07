"""Allan Peters-method pass on the SZV mark: 15 rough vector sketches, each combining SZV with a
second brand noun. Rough on purpose, like his sketch round; finalists get refined later."""
import math, itertools, os
import szv_line as L
from szv_line import SW, NAVY, CREAM, AMBER, VARIANTS
V = "soft"; Wd, a, s, Bv, r = VARIANTS[V]; H = L.H
D = L.d_attr(V)
TEAL = "#3FA7B5"
_id = itertools.count()


def cutmask(extra=""):
    uid = f"k{next(_id)}"
    lines = "".join(f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}" stroke="#000" stroke-width="{L.CUT}"/>'
                    for p, q in L.cut_lines(V))
    return uid, (f'<mask id="{uid}" maskUnits="userSpaceOnUse" x="-2000" y="-2000" width="4000" height="4000">'
                 f'<rect x="-2000" y="-2000" width="4000" height="4000" fill="#fff"/>{lines}{extra}</mask>')


def mark(color, sw=SW, extra_mask="", d=D):
    uid, m = cutmask(extra_mask)
    return (f'{m}<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linejoin="miter" '
            f'stroke-miterlimit="12" mask="url(#{uid})"/>')


def frame(inner, bg=NAVY, vb="-420 -200 840 840"):
    return f'<svg viewBox="{vb}" width="100%" style="display:block;background:{bg};border-radius:12px">{inner}</svg>'


def path(color, sw):
    return f'<path d="{D}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linejoin="miter" stroke-miterlimit="12"/>'


S = []  # (title, nouns, svg)

# 1 inline: Peters' "inlining" badge technique; one line echoing like resonance
S.append(("Resonance", "letters + reverb", frame(mark(AMBER) + path(NAVY, SW * 0.56) + path(AMBER, SW * 0.2))))

# 2 broadcast arcs rising out of the V's mouth
arcs = ""
for R in (360, 430, 500):
    ang = math.radians(16)
    x1, y1 = -R * math.sin(ang), Bv - R * math.cos(ang)
    arcs += f'<path d="M{x1:.1f},{y1:.1f} A{R},{R} 0 0 1 {-x1:.1f},{y1:.1f}" fill="none" stroke="{AMBER}" stroke-width="22" stroke-linecap="round"/>'
S.append(("On Air", "letters + broadcast", frame(mark(CREAM) + arcs, vb="-420 -300 840 840")))

# 3 microphone capsule cradled in the V (the V becomes the mic's yoke)
grille = "".join(f'<line x1="-24" y1="{y}" x2="24" y2="{y}" stroke="{NAVY}" stroke-width="7" stroke-linecap="round"/>'
                 for y in range(-150, 70, 22))
S.append(("The Cradle", "letters + microphone",
          frame(mark(CREAM) + f'<rect x="-40" y="-190" width="80" height="270" rx="40" fill="{AMBER}"/>{grille}', vb="-420 -260 840 840")))

# 4 waveform bars: the mark built from vertical bars (visual rhythm, like his FM mark)
bars = "".join(f'<rect x="{x}" y="-2000" width="9" height="4000" fill="#000"/>' for x in range(-400, 400, 26))
S.append(("Level Meter", "letters + waveform", frame(mark(AMBER, sw=SW * 1.35, extra_mask=bars))))

# 5 speech bubble whose tail sits under the V's point
S.append(("Speak", "letters + speech bubble",
          frame(f'<path d="M-330,-150 H330 a70,70 0 0 1 70,70 V490 a70,70 0 0 1 -70,70 H50 L0,640 L-50,560 H-330 a70,70 0 0 1 -70,-70 V-80 a70,70 0 0 1 70,-70 Z" fill="{AMBER}"/>'
                f'<g transform="translate(0,40) scale(.82)">{mark(NAVY)}</g>', vb="-440 -200 880 880")))

# 6 badge (Peters' badge format)
badge = (f'<defs><path id="bt6" d="M-330,210 A330,330 0 0 1 330,210"/><path id="bb6" d="M-372,210 A372,372 0 0 0 372,210"/></defs>'
         f'<circle cx="0" cy="210" r="410" fill="none" stroke="{AMBER}" stroke-width="14"/>'
         f'<circle cx="0" cy="210" r="290" fill="none" stroke="{AMBER}" stroke-width="6" opacity=".6"/>'
         f'<text font-family="Space Grotesk" font-weight="700" font-size="64" letter-spacing="14" fill="{CREAM}"><textPath href="#bt6" startOffset="50%" text-anchor="middle">SPENCER Z</textPath></text>'
         f'<text font-family="Space Grotesk" font-weight="600" font-size="46" letter-spacing="18" fill="{CREAM}" opacity=".75"><textPath href="#bb6" startOffset="50%" text-anchor="middle">VOICEOVERS</textPath></text>'
         f'<g transform="translate(0,95) scale(.5)">{mark(AMBER)}</g>')
S.append(("Studio Seal", "letters + badge", frame(badge, vb="-440 -220 880 880")))

# 7 weight study: heavier stroke, tighter counters (stroke weight is structural)
S.append(("Heavyweight", "letters + low voice", frame(mark(AMBER, sw=SW * 1.55))))

# 8 headphones over the mark
S.append(("Booth", "letters + headphones",
          frame(f'<path d="M-300,-20 A300,300 0 0 1 300,-20" fill="none" stroke="{AMBER}" stroke-width="26" stroke-linecap="round"/>'
                f'<rect x="-352" y="-80" width="60" height="140" rx="26" fill="{AMBER}"/><rect x="292" y="-80" width="60" height="140" rx="26" fill="{AMBER}"/>'
                f'<g transform="translate(0,120) scale(.78)">{mark(CREAM)}</g>', vb="-420 -340 840 840")))

# 9 overlap echo (overlapping geometry, like his rings mark)
S.append(("Double Take", "letters + echo",
          frame(f'<g style="mix-blend-mode:multiply" transform="translate(-16,-14)">{mark(AMBER)}</g>'
                f'<g style="mix-blend-mode:multiply" transform="translate(16,14)">{mark(TEAL)}</g>', bg=CREAM)))

# 10 ring interlock: circle passing behind the S and Z
S.append(("Orbit", "letters + coming back (repeat clients)",
          frame('<mask id="rg10" maskUnits="userSpaceOnUse" x="-2000" y="-2000" width="4000" height="4000">'
                '<rect x="-2000" y="-2000" width="4000" height="4000" fill="#fff"/>' + path("#000", SW + 36) + '</mask>'
                f'<circle cx="0" cy="200" r="330" fill="none" stroke="{AMBER}" stroke-width="20" mask="url(#rg10)"/>' + mark(CREAM))))

# 11 scan lines: horizontal knockouts (signal), like the stripes in his tree mark
scan = "".join(f'<rect x="-2000" y="{y}" width="4000" height="12" fill="#000"/>' for y in (100, 175, 250, 325))
S.append(("Signal", "letters + transmission", frame(mark(AMBER, sw=SW * 1.2, extra_mask=scan))))

# 12 voice becomes the letter: a waveform flows into the S's bottom bar (visual flow)
pts = []
for i in range(241):
    t = i / 240; x = -Wd - 380 + 380 * t
    amp = 70 * math.sin(math.pi * t) ** 1.5
    pts.append(f"{x:.1f},{H - amp * math.sin(2 * math.pi * 4.5 * t):.1f}")
wave = f'<polyline points="{" ".join(pts)}" fill="none" stroke="{AMBER}" stroke-width="{SW * 0.55}" stroke-linecap="round" stroke-linejoin="round"/>'
S.append(("First Word", "letters + soundwave", frame(wave + mark(CREAM), vb="-760 -120 1120 640")))

# 13 quotation marks: words spoken
S.append(("Quoted", "letters + quotation",
          frame(f'<text x="-470" y="250" font-family="Fraunces" font-weight="600" font-size="520" fill="{AMBER}">“</text>'
                f'<text x="300" y="250" font-family="Fraunces" font-weight="600" font-size="520" fill="{AMBER}">”</text>'
                f'<g transform="translate(0,40) scale(.72)">{mark(CREAM)}</g>', vb="-520 -160 1040 720")))

# 14 Lisbon azulejo: the mark as a 4-way tile (brand pattern, not the mark itself)
tile = ""
for i, rot in enumerate((0, 90, 270, 180)):
    cx, cy = (i % 2) * 700, (i // 2) * 700
    tile += f'<g transform="translate({cx},{cy}) rotate({rot} 0 200) scale(.8)">{mark(NAVY if i in (0, 3) else AMBER)}</g>'
S.append(("Azulejo", "letters + Lisbon tile (pattern)", frame(tile, bg=CREAM, vb="-400 -200 1500 1500")))

# 15 on-air lamp: the mark lit inside a rounded lamp
S.append(("Lamp", "letters + on-air light",
          frame(f'<rect x="-400" y="-130" width="800" height="680" rx="110" fill="{AMBER}"/>'
                f'<rect x="-370" y="-100" width="740" height="620" rx="90" fill="none" stroke="{NAVY}" stroke-width="6" opacity=".35"/>'
                f'<g transform="translate(0,30) scale(.82)">{mark(NAVY)}</g>', vb="-440 -170 880 760")))

CARDS = "".join(f'<figure><div class="sk">{svg}</div><figcaption><b>{i+1:02d} · {t}</b><span>{n}</span></figcaption></figure>'
                for i, (t, n, svg) in enumerate(S))

if __name__ == "__main__":
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_sketches.html"), "w", encoding="utf-8").write(
        '<html><head><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700&family=Fraunces:wght@600&display=swap" rel="stylesheet">'
        '<style>body{background:#06080c;color:#ddd;font:13px sans-serif;margin:12px;display:grid;grid-template-columns:repeat(5,1fr);gap:10px}'
        'figure{margin:0}figcaption{display:flex;flex-direction:column;margin-top:4px}span{color:#999}</style></head><body>'
        + CARDS + '</body></html>')
    print(len(S), "sketches")
