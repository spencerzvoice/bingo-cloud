"""Build a client's Ableton project + MAKE VIDEO launcher anywhere (cloud or desktop).

Usage:
  python cloud_ableton.py --template "<Ableton Template Project dir>" --funnel "Funnel G" \
      --client "YETI" --src "<source.mp4>" --novox "<Client>_NOVOX.mp4" --out "<staging dir>" [--n 2]

Writes into <out>/:
  <Client> Project/<Client> Project.als     (template copy, ORIGINAL VIDEO + VIDEO WITHOUT VOX patched)
  Ready to Link to Drafted Email/MAKE VIDEO - double-click me.bat
The .als records Spencer's local Drive path (D:/My Drive/Client Outreach/<Funnel>/<Client>/<file>) plus
RelativePath ../<file>, so it opens straight from his synced folder even though it was built elsewhere.
Needs ffprobe on PATH. Upload <out>/* into the client's Drive folder (rclone copy).

--src / --novox MUST already carry their final Drive names ("<Client> - SOURCE - <title>.mp4",
"<Client>_NOVOX.mp4"): the .als links by filename, so a scratch name like src.mp4 that gets renamed
on upload leaves ORIGINAL VIDEO pointing at a file that doesn't exist (Funnel G, 2026-09-30: 11 of 18
broken). build() refuses any other name. Desktop check/repair of a whole funnel:
  python cloud_ableton.py --check "D:/My Drive/Client Outreach/Funnel G" [--fix]
"""
import argparse, glob, gzip, os, re, shutil, sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from revoice_build import patch_clip  # noqa: E402

DRIVE_ROOT = "D:/My Drive/Client Outreach"
BAT = r'''@echo off
title Make Video - {client}
echo.
echo  {client} : putting your newest WAV mix onto the original video...
echo.
"C:\Users\spenc\AppData\Local\Programs\Python\Python314\python.exe" "C:\Users\spenc\Bingo\.claude\skills\revoice-material\scripts\mux_take.py" "%~dp0.."
if errorlevel 1 (
  echo.
  echo  Something went wrong. Make sure you exported a .wav from Ableton into this folder.
) else (
  echo.
  echo  Done. The .mp4 is in this folder, named after your .wav.
)
echo.
pause
'''


def check_names(client, src, novox):
    """Refuse scratch filenames: the .als records basename(src)/basename(novox) as the Drive file."""
    s, v = os.path.basename(src), os.path.basename(novox)
    bad = []
    if not (s.startswith(f"{client} - SOURCE - ") and s.lower().endswith(".mp4")):
        bad.append(f"--src is '{s}', must be '{client} - SOURCE - <title>.mp4'")
    if v != f"{client}_NOVOX.mp4":
        bad.append(f"--novox is '{v}', must be '{client}_NOVOX.mp4'")
    if bad:
        sys.exit("REFUSED - rename the file(s) to their final Drive names BEFORE building, "
                 "then upload under exactly those names:\n  " + "\n  ".join(bad))


def check_links(funnel_dir, fix=False):
    """Report (and with fix=True, repair) ORIGINAL VIDEO / VIDEO WITHOUT VOX links that point at
    missing files. Repair only when exactly one same-size candidate exists in the client folder."""
    from revoice_build import patch_clip as _patch
    broken = 0
    for als in sorted(glob.glob(os.path.join(funnel_dir, "*", "*Project", "*.als"))):
        cdir = os.path.dirname(os.path.dirname(als))
        client = os.path.basename(cdir)
        xml = gzip.open(als).read().decode("utf-8")
        changed = False
        for track, pat in (("ORIGINAL VIDEO", f"{client} - SOURCE - *.mp4"),
                           ("VIDEO WITHOUT VOX", f"{client}_NOVOX.mp4")):
            i = xml.find(f'<EffectiveName Value="{track}" />')
            if i < 0:
                continue
            seg = xml[i:xml.find("</AudioTrack>", i)]
            path = re.search(r'<Path Value="([^"]*)"', seg).group(1)
            if os.path.exists(path):
                continue
            broken += 1
            size = int(re.search(r'<OriginalFileSize Value="(\d+)"', seg).group(1))
            cands = [f for f in glob.glob(os.path.join(cdir, pat)) if os.path.getsize(f) == size]
            if fix and len(cands) == 1:
                xml = _patch(xml, track, cands[0].replace("\\", "/"))
                changed = True
                print(f"FIXED  {client} / {track} -> {os.path.basename(cands[0])}")
            else:
                print(f"BROKEN {client} / {track} -> {path}  (candidates: {len(cands)})")
        if changed:
            ET.fromstring(xml.encode("utf-8"))
            with gzip.GzipFile(als, "wb", mtime=0) as g:
                g.write(xml.encode("utf-8"))
            ET.fromstring(gzip.open(als).read())
    print(f"{broken} broken link(s) found")
    return broken


def build(template, funnel, client, src, novox, out, n=1):
    check_names(client, src, novox)
    pname = f"{client} Project" if n == 1 else f"{client} {n} Project"
    pdir = os.path.join(out, pname)
    if os.path.exists(pdir):
        shutil.rmtree(pdir)
    shutil.copytree(template, pdir, ignore=shutil.ignore_patterns(
        "Desktop.ini", "desktop.ini", "Backup", "*.pre_sidechain"))
    als = os.path.join(pdir, f"{pname}.als")
    os.rename(os.path.join(pdir, "Ableton Template.als"), als)
    xml = gzip.open(als).read().decode("utf-8")
    ET.fromstring(xml.encode("utf-8"))
    base = f"{DRIVE_ROOT}/{funnel}/{client}"
    xml = patch_clip(xml, "ORIGINAL VIDEO", src, f"{base}/{os.path.basename(src)}")
    xml = patch_clip(xml, "VIDEO WITHOUT VOX", novox, f"{base}/{os.path.basename(novox)}")
    ET.fromstring(xml.encode("utf-8"))
    with gzip.GzipFile(als, "wb", mtime=0) as g:
        g.write(xml.encode("utf-8"))
    ET.fromstring(gzip.open(als).read())  # round-trip check
    rdir = os.path.join(out, "Ready to Link to Drafted Email")
    os.makedirs(rdir, exist_ok=True)
    bat = "MAKE VIDEO - double-click me.bat" if n == 1 else f"MAKE VIDEO {n} - double-click me.bat"
    with open(os.path.join(rdir, bat), "w", newline="\r\n") as f:
        f.write(BAT.format(client=client))
    return als


if __name__ == "__main__":
    a = argparse.ArgumentParser()
    a.add_argument("--check", help="funnel dir: verify every project's video links")
    a.add_argument("--fix", action="store_true", help="with --check: repair by same-size match")
    for k in ("template", "funnel", "client", "src", "novox", "out"):
        a.add_argument("--" + k)
    a.add_argument("--n", type=int, default=1)
    p = a.parse_args()
    if p.check:
        sys.exit(1 if check_links(p.check, p.fix) else 0)
    missing = [k for k in ("template", "funnel", "client", "src", "novox", "out") if not getattr(p, k)]
    if missing:
        a.error("missing: " + ", ".join("--" + k for k in missing))
    print(build(p.template, p.funnel, p.client, p.src, p.novox, p.out, p.n))
