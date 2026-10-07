"""SZV one-line monogram (Spencer's concept, 2026-10-07).
One continuous stroke: Z bottom-right -> Z bottom bar -> Z diagonal up -> Z top bar -> V down
-> V up -> S top bar -> S diagonal down -> S bottom bar. Mirror-symmetric about x=0."""
import math, os
OUT = os.path.dirname(os.path.abspath(__file__))
NAVY, CREAM, AMBER, BLACK = "#0B0F15", "#F1ECE3", "#F0B13C", "#000000"

VARIANTS = {
    # name: (W top half-width, a foot offset, s V top half-width, Bv apex depth, round-tip radius)
    "sharp": (300, 64, 110, 290, 0),
    "soft":  (300, 64, 110, 290, 46),
    "deep":  (280, 90, 60, 250, 0),
}
H, SW = 400, 44

def fillet(corner, prev, nxt, r):
    cx, cy = corner
    u1 = (prev[0] - cx, prev[1] - cy); n1 = math.hypot(*u1); u1 = (u1[0] / n1, u1[1] / n1)
    u2 = (nxt[0] - cx, nxt[1] - cy); n2 = math.hypot(*u2); u2 = (u2[0] / n2, u2[1] / n2)
    th = math.acos(u1[0] * u2[0] + u1[1] * u2[1]); t = r / math.tan(th / 2)
    return (cx + t * u1[0], cy + t * u1[1]), (cx + t * u2[0], cy + t * u2[1])

def d_attr(name):
    W, a, s, Bv, r = VARIANTS[name]
    P = [(W, H), (a, H), (W, 0), (s, 0), (0, Bv), (-s, 0), (-W, 0), (-a, H), (-W, H)]
    f = lambda p: f"{p[0]:.2f},{p[1]:.2f}"
    if not r:
        return "M" + " L".join(f(p) for p in P)
    c1, c2 = fillet(P[2], P[1], P[3], r)
    c3, c4 = fillet(P[6], P[5], P[7], r)
    return (f"M{f(P[0])} L{f(P[1])} L{f(c1)} A{r},{r} 0 0 0 {f(c2)} L{f(P[3])} L{f(P[4])} "
            f"L{f(P[5])} L{f(c3)} A{r},{r} 0 0 0 {f(c4)} L{f(P[7])} L{f(P[8])}")

def path_el(name, color):
    return (f'<path d="{d_attr(name)}" fill="none" stroke="{color}" stroke-width="{SW}" '
            f'stroke-linejoin="miter" stroke-miterlimit="12" stroke-linecap="butt"/>')

def bbox(name, pad):
    W = VARIANTS[name][0]
    return -W - pad, -pad, 2 * W + 2 * pad, H + 2 * pad

def svg(name, color, pad=SW * 1.6, bg=None, square=False, circle=False, rx=0, px=1024):
    x, y, w, h = bbox(name, pad)
    if square:
        s = max(w, h); x -= (s - w) / 2; y -= (s - h) / 2; w = h = s
    back = ""
    if bg:
        back = (f'<circle cx="{x+w/2:.1f}" cy="{y+h/2:.1f}" r="{w/2:.1f}" fill="{bg}"/>' if circle else
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{bg}"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x:.1f} {y:.1f} {w:.1f} {h:.1f}" '
            f'width="{px}" height="{round(px*h/w)}">{back}{path_el(name, color)}</svg>\n')

if __name__ == "__main__":
    for old in os.listdir(OUT):
        if old.endswith(".svg"):
            os.remove(os.path.join(OUT, old))       # earlier filled-rebuild exports, superseded
    for n in VARIANTS:
        for cname, col in (("black", BLACK), ("navy", NAVY), ("cream", CREAM), ("amber", AMBER)):
            open(os.path.join(OUT, f"szv-{n}-{cname}.svg"), "w").write(svg(n, col))
        open(os.path.join(OUT, f"szv-{n}-icon.svg"), "w").write(svg(n, AMBER, pad=150, bg=NAVY, square=True, rx=150))
        open(os.path.join(OUT, f"szv-{n}-avatar.svg"), "w").write(svg(n, AMBER, pad=200, bg=NAVY, square=True, circle=True))
    print(sorted(f for f in os.listdir(OUT) if f.endswith(".svg")).__len__(), "svgs")
