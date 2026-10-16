"""Replace Ableton's video export: put an exported WAV mix onto the original picture.

Usage:  python mux_take.py "<client folder>" [take.wav] [source video]
Defaults: newest .wav in "<client>/Ready to Link to Drafted Email/", and the client's
source video (first non-NOVOX mp4/mov in the client folder).
Export the WAV from Ableton with the render range starting at 1.1.1 (bar 1 = video frame 0).
Output: "<Ready to Link>/<wav name>.mp4" - AAC 320k audio.

EDITS FOLLOW THE ABLETON PROJECT (Spencer, 2026-10-14, Vyond: cuts in Ableton froze its video export).
The script reads the saved .als in "<client>/<client> Project/" and rebuilds the picture from the clips on
the ORIGINAL VIDEO track (VIDEO WITHOUT VOX if that one is empty): every cut, trim and move is copied, gaps
go black. No edits = picture stream-copied as before (no re-encode). Edited = re-encoded (x264 CRF 16).
SAVE the Ableton project before double-clicking: the script sees the last save, not the open session.
"""
import bisect, glob, html, os, re, subprocess, sys, zlib

FF = r"C:\Users\spenc\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-full_build\bin"
VIDEO_TRACKS = ("ORIGINAL VIDEO", "VIDEO WITHOUT VOX")


def _v(tag, s):
    m = re.search(r'<' + tag + r' Value="([^"]*)"', s)
    return m.group(1) if m else None


def read_als(als):
    """Decompress a .als. First gzip member only: some saves carry trailing bytes that gzip.open rejects."""
    with open(als, "rb") as f:
        return zlib.decompressobj(31).decompress(f.read()).decode("utf-8")


def _has(als, name):
    try:
        return name in read_als(als)
    except Exception:
        return False


def find_als(cdir, src=None):
    """Newest saved .als in the client's '* Project' folder(s), skipping Backup and archived folders.
    With a source video (two-video folders: each button names its own), only a set that uses that video."""
    als = [a for a in glob.glob(os.path.join(glob.escape(cdir), "*Project", "*.als"))
           if not os.path.basename(a).startswith("AbletonTmp")]
    if src:
        name = html.escape(os.path.basename(src), quote=True)
        als = [a for a in als if _has(a, name)]
    return max(als, key=os.path.getmtime) if als else None


def warp_sec(markers, beat):
    """Clip-beat -> source seconds via the clip's warp markers (linear between, extrapolated at the ends)."""
    bs = [b for b, _ in markers]
    i = min(max(bisect.bisect_right(bs, beat) - 1, 0), len(markers) - 2)
    (b0, s0), (b1, s1) = markers[i], markers[i + 1]
    return s0 + (beat - b0) * (s1 - s0) / (b1 - b0)


def timeline(als):
    """Read the video clips off the saved Ableton set.
    Returns (tempo, [(tl_start_s, tl_end_s, src_path, src_in_s, src_out_s), ...]) sorted by timeline start."""
    x = read_als(als)
    t = x[x.find("<Tempo>"):x.find("</Tempo>")]
    tempo = float(_v("Manual", t))
    tid = re.search(r'<AutomationTarget Id="(\d+)"', t).group(1)
    env = re.search(r'<PointeeId Value="' + tid + r'" />\s*</EnvelopeTarget>\s*<Automation>\s*<Events>(.*?)</Events>', x, re.S)
    if env and len(re.findall(r"<\w+Event ", env.group(1))) > 1:  # Ableton always stores 1 default event
        sys.exit("STOP: the Ableton set has tempo automation. Remove it (one fixed tempo) so the video can follow the cuts.")
    spb = 60.0 / tempo
    for name in VIDEO_TRACKS:
        i = x.find(f'<EffectiveName Value="{name}" />')
        if i < 0:
            continue
        seg = x[i:x.find("</AudioTrack>", i)]
        arr = seg[seg.find("<ArrangerAutomation>"):seg.find("</ArrangerAutomation>")] if "<ArrangerAutomation>" in seg else seg
        clips = []
        for c in re.findall(r'<AudioClip Id="\d+" Time="[^"]+">(.*?)</AudioClip>', arr, re.S):
            if _v("Disabled", c) == "true":
                continue
            start, end = float(_v("CurrentStart", c)), float(_v("CurrentEnd", c))
            loop = re.search(r"<Loop>(.*?)</Loop>", c, re.S).group(1)
            ls = float(_v("LoopStart", loop))
            if _v("IsWarped", c) == "true":
                mk = sorted((float(b), float(s)) for s, b in
                            re.findall(r'<WarpMarker Id="\d+" SecTime="([^"]+)" BeatTime="([^"]+)"', c))
                src_in, src_out = warp_sec(mk, ls), warp_sec(mk, ls + (end - start))
            else:  # unwarped: LoopStart is seconds, plays at native speed
                src_in = ls
                src_out = ls + (end - start) * spb
            fr = c[c.find("<SampleRef>"):]
            path = html.unescape(_v("Path", fr) or "")
            rel = html.unescape(_v("RelativePath", fr) or "")
            if not os.path.exists(path):
                cand = os.path.normpath(os.path.join(os.path.dirname(als), rel))
                path = cand if os.path.exists(cand) else os.path.join(os.path.dirname(os.path.dirname(als)), os.path.basename(path.replace("\\", "/")))
            clips.append((start * spb, end * spb, path, src_in, src_out))
        if clips:
            return tempo, sorted(clips)
    return tempo, []


def duration(path):
    r = subprocess.run([os.path.join(FF, "ffprobe.exe"), "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", path], capture_output=True, text=True)
    return float(r.stdout.strip())


def main():
    cdir = sys.argv[1]
    rdir = os.path.join(cdir, "Ready to Link to Drafted Email")
    wav = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] else max(glob.glob(os.path.join(glob.escape(rdir), "*.wav")), key=os.path.getmtime)
    out = os.path.join(rdir, os.path.splitext(os.path.basename(wav))[0] + ".mp4")
    ff = os.path.join(FF, "ffmpeg.exe")
    als = find_als(cdir, sys.argv[3] if len(sys.argv) > 3 else None)
    try:
        clips = timeline(als)[1] if als else []
    except SystemExit:
        raise
    except Exception as e:  # unreadable set (Drive placeholder, mid-sync): old behaviour, whole source as is
        print(f"  note: couldn't read {os.path.basename(als)} ({e}); using the full source video, no edits")
        clips = []
    for c in clips:
        if not os.path.exists(c[2]):
            sys.exit(f"STOP: the video clip in Ableton points at a missing file:\n  {c[2]}")
    # Untouched project (one clip from 0, source from 0) = the old fast path: copy the picture as is.
    plain = not clips or (len(clips) == 1 and abs(clips[0][0]) < 0.01 and abs(clips[0][3]) < 0.01)
    if plain:
        if len(sys.argv) > 3:
            src = sys.argv[3]
        elif clips:
            src = clips[0][2]
        else:
            vids = sorted(f for f in os.listdir(cdir) if f.lower().endswith((".mp4", ".mov")) and "NOVOX" not in f and "no_vocals" not in f)
            src = os.path.join(cdir, vids[0])
        subprocess.run([ff, "-y", "-i", src, "-i", wav, "-map", "0:v:0", "-map", "1:a:0",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-shortest", "-movflags", "+faststart", out],
                       check=True, capture_output=True)
        print(f"{out}\n  picture: {os.path.basename(src)}\n  audio:   {os.path.basename(wav)}")
        return

    # Edited project: rebuild the picture cut for cut from the Ableton timeline.
    srcs = sorted({c[2] for c in clips})
    inputs, parts, chain, t = [], [], [], 0.0
    for s in srcs:
        inputs += ["-i", s]
    probe = subprocess.run([os.path.join(FF, "ffprobe.exe"), "-v", "error", "-select_streams", "v:0", "-show_entries",
                            "stream=width,height,r_frame_rate", "-of", "csv=p=0", srcs[0]], capture_output=True, text=True).stdout.strip()
    w, h, fps = probe.split(",")
    wav_i = len(srcs)
    inputs += ["-i", wav]
    n = 0
    for tl_in, tl_out, path, s_in, s_out in clips:
        tl_in = max(tl_in, t)  # overlapping clips: the later one wins from where it starts
        if tl_in - t > 0.02:  # gap on the timeline = black
            parts.append(f"color=c=black:s={w}x{h}:r={fps}:d={tl_in - t:.6f},setsar=1[v{n}]")
            chain.append(f"[v{n}]"); n += 1
        speed = (s_out - s_in) / (tl_out - tl_in) if tl_out > tl_in else 1
        s_from = s_out - (tl_out - tl_in) * speed
        parts.append(f"[{srcs.index(path)}:v:0]trim=start={s_from:.6f}:end={s_out:.6f},setpts=(PTS-STARTPTS)/{speed:.6f},"
                     f"fps={fps},scale={w}:{h},setsar=1[v{n}]")
        chain.append(f"[v{n}]"); n += 1
        t = tl_out
    parts.append("".join(chain) + f"concat=n={n}:v=1:a=0[vout]")
    subprocess.run([ff, "-y", *inputs, "-filter_complex", ";".join(parts), "-map", "[vout]", "-map", f"{wav_i}:a:0",
                    "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "320k", "-movflags", "+faststart", out], check=True, capture_output=True)
    print(f"{out}\n  picture: {len(clips)} clip(s) cut to match the Ableton edit ({os.path.basename(als)})")
    for tl_in, tl_out, path, s_in, s_out in clips:
        print(f"    {tl_in:7.2f}-{tl_out:7.2f}s  <-  source {s_in:7.2f}-{s_out:7.2f}s")
    print(f"  audio:   {os.path.basename(wav)}")
    d_wav = duration(wav)
    if abs(d_wav - t) > 0.5:
        print(f"\n  CHECK: the WAV is {d_wav:.2f}s but the video edit ends at {t:.2f}s. Did you save the Ableton project"
              f" after your last cut, and export from 1.1.1?")


if __name__ == "__main__":
    main()
