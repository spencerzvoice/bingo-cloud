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
"""
import argparse, gzip, os, shutil, sys
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


def build(template, funnel, client, src, novox, out, n=1):
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
    for k in ("template", "funnel", "client", "src", "novox", "out"):
        a.add_argument("--" + k, required=True)
    a.add_argument("--n", type=int, default=1)
    p = a.parse_args()
    print(build(p.template, p.funnel, p.client, p.src, p.novox, p.out, p.n))
