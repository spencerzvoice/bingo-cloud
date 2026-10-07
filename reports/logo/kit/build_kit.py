"""Profile kit for the SZV logo (Spencer, 2026-10-07): avatars, banners, favicons, transparent lockups.
Each asset is an HTML page rendered to PNG at its exact pixel size by headless Chrome (a throwaway profile,
never Spencer's own), so the Lexend Exa wordmark matches the website and the brand book.
Run: python build_kit.py   -> PNGs in ./out/"""
import os, subprocess, tempfile, shutil
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PROFILE = os.path.join(tempfile.gettempdir(), "szv-kit-chrome")

NAVY, CREAM, AMBER, SOFT = "#0B0F15", "#F1ECE3", "#F0B13C", "#A9B2BE"
PATH = "M300,400 L40,400 L300,0 L110,0 L0,290 L-110,0 L-300,0 L-40,400 L-300,400"
FONT = '<link href="https://fonts.googleapis.com/css2?family=Lexend+Exa:wght@500&family=Work+Sans:wght@500&display=block" rel="stylesheet">'


def mark(color, w):
    """The mark at width w (750x500 box, stroke 68 = weight D)."""
    return (f'<svg viewBox="-375 -50 750 500" width="{w}" height="{w*2/3:.1f}" style="display:block;overflow:visible">'
            f'<path d="{PATH}" fill="none" stroke="{color}" stroke-width="68" stroke-linejoin="miter" stroke-miterlimit="12"/></svg>')


def wordmark(size, name_color, tag_color):
    """SPENCER Z over VOICEOVERS; each line pads left by its own letter-spacing so the centring is exact."""
    tag = size * 0.42
    return (f'<div style="display:flex;flex-direction:column;align-items:center;line-height:1">'
            f'<span style="font:500 {size}px/1 \'Lexend Exa\';letter-spacing:.14em;padding-left:.14em;color:{name_color}">SPENCER Z</span>'
            f'<span style="font:500 {tag:.1f}px/1 \'Lexend Exa\';letter-spacing:.52em;padding-left:.52em;color:{tag_color};margin-top:{size*0.36:.1f}px">VOICEOVERS</span></div>')


def lockup(size, mark_color, name_color, tag_color, stacked=False):
    m = mark(mark_color, size * (3.3 if stacked else 2.9))
    d = "column" if stacked else "row"
    gap = size * (0.9 if stacked else 0.8)
    return f'<div style="display:flex;flex-direction:{d};align-items:center;gap:{gap:.1f}px">{m}{wordmark(size, name_color, tag_color)}</div>'


def page(w, h, bg, inner, justify="center", pad=0):
    bgcss = "transparent" if bg is None else bg
    return (f'<!doctype html><html><head><meta charset="utf-8">{FONT}<style>html,body{{margin:0;width:{w}px;height:{h}px;'
            f'background:{bgcss};overflow:hidden}}body{{display:flex;align-items:center;justify-content:{justify};'
            f'box-sizing:border-box;padding:0 {pad}px}}</style></head><body>{inner}</body></html>')


def render(name, w, h, html):
    tmp = os.path.join(PROFILE, name + ".html")
    open(tmp, "w", encoding="utf-8").write(html)
    out = os.path.join(OUT, name + ".png")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--user-data-dir={PROFILE}",
                    f"--window-size={w},{h}", "--virtual-time-budget=8000", "--default-background-color=00000000",
                    f"--screenshot={out}", "file:///" + tmp.replace("\\", "/")],
                   check=True, capture_output=True, timeout=120)
    im = Image.open(out)
    if im.size != (w, h):                       # headless can add a few px on some builds: crop to spec
        im.crop((0, 0, w, h)).save(out)
    return out


def avatar(bg, fg, size):
    # mark sits well inside the circle every platform crops to
    return page(size, size, bg, mark(fg, size * 0.56))


def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(PROFILE, exist_ok=True)
    made = []
    # --- avatars (square files; Instagram, LinkedIn, YouTube, Google crop them to a circle) ---
    made.append(render("avatar-navy-1080", 1080, 1080, avatar(NAVY, AMBER, 1080)))
    made.append(render("avatar-amber-1080", 1080, 1080, avatar(AMBER, NAVY, 1080)))
    base = Image.open(os.path.join(OUT, "avatar-navy-1080.png")).convert("RGB")
    for name, px in (("instagram-profile-320", 320), ("linkedin-profile-400", 400), ("google-business-logo-720", 720),
                     ("youtube-profile-800", 800), ("casting-profile-1000", 1000)):
        p = os.path.join(OUT, name + ".png"); base.resize((px, px), Image.LANCZOS).save(p); made.append(p)

    # --- banners ---
    tagline = ('<div style="font:500 {s}px/1 \'Work Sans\';color:{c};letter-spacing:.06em;margin-top:{m}px;text-align:center">'
               'Commercial · Narration · E-learning</div>')
    # LinkedIn 1584x396: profile photo covers the lower-left on desktop, so the lockup sits right of centre.
    li = (f'<div style="display:flex;flex-direction:column;align-items:center">{lockup(46, AMBER, CREAM, SOFT)}'
          + tagline.format(s=24, c=SOFT, m=30) + '</div>')
    made.append(render("linkedin-banner-1584x396", 1584, 396, page(1584, 396, NAVY, li, "flex-end", 150)))
    # YouTube 2560x1440: everything inside the 1546x423 centre area that shows on every device.
    yt = (f'<div style="display:flex;flex-direction:column;align-items:center">{lockup(64, AMBER, CREAM, SOFT)}'
          + tagline.format(s=32, c=SOFT, m=40) + '</div>')
    made.append(render("youtube-banner-2560x1440", 2560, 1440, page(2560, 1440, NAVY, yt)))
    # Google Business cover 1080x608.
    gb = (f'<div style="display:flex;flex-direction:column;align-items:center">{lockup(40, AMBER, CREAM, SOFT, stacked=True)}'
          + tagline.format(s=22, c=SOFT, m=28) + '</div>')
    made.append(render("google-business-cover-1080x608", 1080, 608, page(1080, 608, NAVY, gb)))

    # --- transparent logo files for documents, invoices, email ---
    made.append(render("lockup-for-dark-backgrounds", 1400, 360, page(1400, 360, None, lockup(80, AMBER, CREAM, SOFT))))
    made.append(render("lockup-for-light-backgrounds", 1400, 360, page(1400, 360, None, lockup(80, NAVY, NAVY, "#4A5260"))))
    made.append(render("lockup-stacked-for-dark-backgrounds", 900, 900, page(900, 900, None, lockup(70, AMBER, CREAM, SOFT, True))))
    made.append(render("lockup-stacked-for-light-backgrounds", 900, 900, page(900, 900, None, lockup(70, NAVY, NAVY, "#4A5260", True))))
    made.append(render("email-signature-mark-navy", 240, 160, page(240, 160, None, mark(NAVY, 200))))
    made.append(render("email-signature-mark-amber", 240, 160, page(240, 160, None, mark(AMBER, 200))))

    # --- favicons (from a 512 tile: amber mark on a navy rounded square) ---
    tile = page(512, 512, None, f'<div style="width:512px;height:512px;border-radius:105px;background:{NAVY};'
                                f'display:flex;align-items:center;justify-content:center">{mark(AMBER, 400)}</div>')
    made.append(render("favicon-512", 512, 512, tile))
    t = Image.open(os.path.join(OUT, "favicon-512.png")).convert("RGBA")
    for px in (16, 32, 48, 180, 192):
        p = os.path.join(OUT, f"favicon-{px}.png"); t.resize((px, px), Image.LANCZOS).save(p); made.append(p)
    ico = os.path.join(OUT, "favicon.ico"); t.save(ico, sizes=[(16, 16), (32, 32), (48, 48)]); made.append(ico)

    shutil.rmtree(PROFILE, ignore_errors=True)
    for p in made:
        print(os.path.basename(p), Image.open(p).size)


if __name__ == "__main__":
    main()
