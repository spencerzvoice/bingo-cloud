"""Funnel re-voicing package builder (Steps 2, 3, 5 of revoice-material-process.md).
Usage: python revoice_build.py "<Funnel dir>" [Client ...]
Per client with a sources.txt: download source if missing, Demucs NOVOX if missing,
Ableton project from template if missing. Idempotent: only fills gaps.
"""
import gzip, json, os, re, shutil, subprocess, sys, tempfile
import xml.etree.ElementTree as ET

FF = r"C:\Users\spenc\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-full_build\bin"
DENO = r"C:\Users\spenc\AppData\Roaming\Python\Python314\Scripts"
os.environ["PATH"] = FF + os.pathsep + DENO + os.pathsep + os.environ["PATH"]
TEMPLATE = r"D:\My Drive\Client Outreach\Ableton Template Project"
WORK = os.path.join(tempfile.gettempdir(), "revoice_work")
FMT = "bestvideo[height<=1080][vcodec^=avc1]+bestaudio[ext=m4a]/bestvideo[height<=1080]+bestaudio/best[height<=1080]/best"


def log(*a):
    print(*a, flush=True)


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)
    if r.returncode != 0:
        raise RuntimeError(f"{cmd[0]} failed ({r.returncode}): {r.stderr[-800:]}")
    return r.stdout


def probe(path):
    d = json.loads(run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,sample_rate", "-of", "json", path]))
    dur = float(d["format"]["duration"])
    sr = next((int(s["sample_rate"]) for s in d["streams"] if s.get("codec_type") == "audio"), 44100)
    return dur, sr


def videos(cdir):
    return sorted(f for f in os.listdir(cdir) if f.lower().endswith((".mp4", ".mov", ".webm")) and "NOVOX" not in f and "no_vocals" not in f)


def download(cdir, url):
    for f in os.listdir(cdir):
        if f.endswith((".part", ".ytdl")) or ".part-Frag" in f:
            os.remove(os.path.join(cdir, f))
    run([sys.executable, "-m", "yt_dlp", "-f", FMT, "--merge-output-format", "mp4", "--restrict-filenames",
         "--ffmpeg-location", FF, "-o", os.path.join(cdir, "%(title)s [%(id)s].%(ext)s"), url])


def novox(client, cdir, src):
    out = os.path.join(cdir, f"{client}_NOVOX.mp4")
    if os.path.exists(out):
        return out
    tmp = tempfile.mkdtemp(dir=WORK)
    wav = os.path.join(tmp, "audio.wav")
    run(["ffmpeg", "-y", "-i", src, "-vn", "-ac", "2", "-ar", "44100", wav])
    run([sys.executable, "-m", "demucs", "--two-stems=vocals", "-o", os.path.join(tmp, "stems"), wav])
    nv = os.path.join(tmp, "stems", "htdemucs", "audio", "no_vocals.wav")
    run(["ffmpeg", "-y", "-i", src, "-i", nv, "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-shortest", out])
    shutil.rmtree(tmp, ignore_errors=True)
    return out


def set_attr(seg, tag, value):
    return re.sub(r'(<%s Value=")[^"]*(" />)' % tag, lambda m: m.group(1) + str(value) + m.group(2), seg, count=1)


def patch_clip(xml, track_name, fpath):
    """Point the one clip on `track_name` at `fpath`, written the way a manual drag-in writes it:
    clip gain 0 dB (template placeholders sit at -70 dB), unwarped, named after the file.
    Unwarped clips: CurrentEnd is in beats (120 BPM -> s*2); loop/marker fields are in seconds."""
    dur, sr = probe(fpath)
    for m in re.finditer(r"<AudioTrack Id=\"\d+\"[^>]*>", xml):
        tend = xml.find("</AudioTrack>", m.start())
        track = xml[m.start():tend]
        if f'<EffectiveName Value="{track_name}" />' not in track:
            continue
        cm = re.search(r"<AudioClip [^>]*>.*?</AudioClip>", track, re.S)
        seg = cm.group(0)
        seg = set_attr(seg, "Name", os.path.splitext(os.path.basename(fpath))[0])
        seg = set_attr(seg, "CurrentStart", 0)
        seg = set_attr(seg, "CurrentEnd", dur * 2)
        seg = set_attr(seg, "LoopStart", 0)
        seg = set_attr(seg, "StartRelative", 0)
        for t in ("LoopEnd", "OutMarker", "HiddenLoopEnd", "RightTime"):
            seg = set_attr(seg, t, dur)
        seg = set_attr(seg, "IsWarped", "false")
        seg = set_attr(seg, "SampleVolume", 1)
        seg = set_attr(seg, "RelativePath", "../" + os.path.basename(fpath))
        seg = set_attr(seg, "Path", fpath.replace("\\", "/"))
        seg = set_attr(seg, "OriginalFileSize", os.path.getsize(fpath))
        seg = set_attr(seg, "DefaultDuration", int(round(dur * sr)))
        seg = set_attr(seg, "DefaultSampleRate", sr)
        track = track[:cm.start()] + seg + track[cm.end():]
        return xml[:m.start()] + track + xml[tend:]
    raise RuntimeError(f"track {track_name} not found")


def repatch(als, src, nv):
    """Re-point an existing project's two video tracks (idempotent)."""
    xml = gzip.open(als).read().decode("utf-8")
    xml = patch_clip(xml, "ORIGINAL VIDEO", src)
    xml = patch_clip(xml, "VIDEO WITHOUT VOX", nv)
    ET.fromstring(xml.encode("utf-8"))
    with gzip.GzipFile(als, "wb", mtime=0) as g:
        g.write(xml.encode("utf-8"))
    ET.fromstring(gzip.open(als).read())


def ableton(client, cdir, src, nv, n=1):
    pname = f"{client} Project" if n == 1 else f"{client} {n} Project"
    pdir = os.path.join(cdir, pname)
    if os.path.exists(pdir):
        return pdir
    shutil.copytree(TEMPLATE, pdir, ignore=shutil.ignore_patterns("Desktop.ini", "desktop.ini", "Backup"))
    old = os.path.join(pdir, "Ableton Template.als")
    als = os.path.join(pdir, f"{pname}.als")
    os.rename(old, als)
    xml = gzip.open(als).read().decode("utf-8")
    ET.fromstring(xml.encode("utf-8"))
    xml = patch_clip(xml, "ORIGINAL VIDEO", src)
    xml = patch_clip(xml, "VIDEO WITHOUT VOX", nv)
    ET.fromstring(xml.encode("utf-8"))
    with gzip.GzipFile(als, "wb", mtime=0) as g:
        g.write(xml.encode("utf-8"))
    ET.fromstring(gzip.open(als).read())
    return pdir


def main():
    fdir = sys.argv[1]
    only = set(sys.argv[2:])
    os.makedirs(WORK, exist_ok=True)
    results = {}
    for client in sorted(os.listdir(fdir)):
        cdir = os.path.join(fdir, client)
        if not os.path.isdir(cdir) or (only and client not in only):
            continue
        sf = os.path.join(cdir, "sources.txt")
        if not os.path.exists(sf):
            results[client] = "SKIP - no sources.txt (needs a pick)"
            continue
        try:
            url = [l.strip() for l in open(sf, encoding="utf-8") if l.strip().startswith("http")][0]
            if not videos(cdir):
                log(client, "downloading", url)
                download(cdir, url)
            src = os.path.join(cdir, videos(cdir)[0])
            log(client, "NOVOX from", os.path.basename(src))
            nv = novox(client, cdir, src)
            log(client, "Ableton")
            ableton(client, cdir, src, nv)
            dur, _ = probe(src)
            results[client] = f"OK - {os.path.basename(src)} ({dur:.0f}s)"
        except Exception as e:
            results[client] = f"FAIL - {e}"
        log(client, "->", results[client])
    log("\n=== SUMMARY ===")
    for k, v in results.items():
        log(f"{k}: {v}")


if __name__ == "__main__":
    main()
