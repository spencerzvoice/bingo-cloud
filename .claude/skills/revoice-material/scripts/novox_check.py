"""NOVOX match gate (Spencer, 2026-10-07: The Economist + BUCK NOVOX files were from other videos and
"this is killing my flow"). A matching length is NOT proof (BUCK's wrong NOVOX was also 30 s).

For every Ableton project in a client folder, reads the two clips it actually plays (ORIGINAL VIDEO,
VIDEO WITHOUT VOX) and checks that the NOVOX's audio is the source's own music bed: the
vocals-stripped stem of a video correlates strongly with that video's full mix, a different video's
does not. Also checks both clips sit in this client's folder and that the video streams are identical
(NOVOX = source picture + no_vocals audio).

Usage: python novox_check.py "<client dir or funnel dir or Client Outreach root>" ...
Exit 1 if any project FAILs. revoice_build.py runs check_project() on every project it builds/touches.
"""
import glob, os, re, shutil, subprocess, sys, tempfile, zlib
import numpy as np

FF = r"C:\Users\spenc\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-full_build\bin"
os.environ["PATH"] = FF + os.pathsep + os.environ["PATH"]
SR = 4000
sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def pcm(path, secs=90):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-t", str(secs), "-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                       capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(f"can't decode {os.path.basename(path)}: {r.stderr.decode(errors='replace')[-300:]}")
    return np.frombuffer(r.stdout, dtype=np.float32)


def audio_corr(src, nv):
    """Peak normalised cross-correlation (lag within +-1 s) between the source mix and the NOVOX."""
    a, b = pcm(src), pcm(nv)
    n = min(len(a), len(b))
    if n < SR:
        return 0.0
    a, b = a[:n] - a[:n].mean(), b[:n] - b[:n].mean()
    if not a.any() or not b.any():
        return 0.0
    size = 1 << (2 * n - 1).bit_length()
    xc = np.fft.irfft(np.fft.rfft(a, size) * np.conj(np.fft.rfft(b, size)), size)
    lag = SR
    window = np.concatenate([xc[:lag + 1], xc[-lag:]])
    return float(np.abs(window).max() / (np.linalg.norm(a) * np.linalg.norm(b)))


FAST_PASS = 0.30  # above this the NOVOX is clearly the source's own bed; below it, re-separate to be sure
REF_PASS = 0.40   # calibrated 10-07: right NOVOX 0.99 (Economist), near-silent right bed 0.65 (Plaid); wrong NOVOX 0.01-0.02 (old Economist, old BUCK)


def demucs_ref(src, nv, secs=60):
    """Decisive test for quiet beds: re-run Demucs on the source's first `secs` and compare with the NOVOX."""
    tmp = tempfile.mkdtemp()
    try:
        wav = os.path.join(tmp, "audio.wav")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-t", str(secs), "-vn", "-ac", "2", "-ar", "44100", wav], check=True)
        subprocess.run([sys.executable, "-m", "demucs", "--two-stems=vocals", "-o", tmp, wav], check=True, capture_output=True)
        return audio_corr(os.path.join(tmp, "htdemucs", "audio", "no_vocals.wav"), nv)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def video_md5(path):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-map", "0:v:0", "-c", "copy", "-f", "md5", "-"],
                       capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def clips(als):
    """{track name: absolute file path} for the ORIGINAL VIDEO / VIDEO WITHOUT VOX tracks."""
    # Ableton's gzip can carry trailing bytes that gzip.open rejects (Airwallex, Booking.com 10-07)
    xml = zlib.decompressobj(31).decompress(open(als, "rb").read()).decode("utf-8", "replace")
    out = {}
    for m in re.finditer(r"<AudioTrack Id=\"\d+\"[^>]*>", xml):
        track = xml[m.start():xml.find("</AudioTrack>", m.start())]
        name = re.search(r'<EffectiveName Value="([^"]*)" />', track)
        if not name or name.group(1) not in ("ORIGINAL VIDEO", "VIDEO WITHOUT VOX"):
            continue
        clip = re.search(r"<AudioClip [^>]*>.*?</AudioClip>", track, re.S)
        if not clip:
            continue
        rel = re.search(r'<RelativePath Value="([^"]*)" />', clip.group(0))
        absp = re.search(r'<Path Value="([^"]*)" />', clip.group(0))
        cand = []
        if rel and rel.group(1):
            cand.append(os.path.normpath(os.path.join(os.path.dirname(als), rel.group(1))))
        if absp and absp.group(1):
            cand.append(os.path.normpath(absp.group(1)))
        out[name.group(1)] = next((c for c in cand if os.path.exists(c)), cand[0] if cand else None)
    return out


def check_project(als):
    """Returns (ok, message) for one .als."""
    cdir = os.path.dirname(os.path.dirname(als))
    c = clips(als)
    src, nv = c.get("ORIGINAL VIDEO"), c.get("VIDEO WITHOUT VOX")
    if not src or not nv:
        return False, "project is missing an ORIGINAL VIDEO or VIDEO WITHOUT VOX clip"
    for label, p in (("ORIGINAL VIDEO", src), ("VIDEO WITHOUT VOX", nv)):
        if not os.path.exists(p):
            return False, f"{label} file not found: {p}"
        if os.path.normcase(os.path.dirname(p)) != os.path.normcase(cdir):
            return False, f"{label} points outside this client's folder: {p}"
    corr = audio_corr(src, nv)
    same_pic = video_md5(src) == video_md5(nv)
    tag = f"corr {corr:.2f}, picture {'identical' if same_pic else 'DIFFERENT'} | {os.path.basename(src)} <-> {os.path.basename(nv)}"
    if corr >= FAST_PASS:
        return True, tag
    ref = demucs_ref(src, nv)
    tag += f", fresh-Demucs match {ref:.2f}"
    if ref >= REF_PASS:
        return True, tag
    if np.sqrt((pcm(nv) ** 2).mean()) < 0.05 * np.sqrt((pcm(src) ** 2).mean()):
        tag += " | NOVOX is near-silent (quiet music bed?) - open it and listen before trusting it"
    return False, tag


def projects(root):
    return sorted(p for p in glob.glob(os.path.join(root, "**", "*.als"), recursive=True)
                  if "Backup" not in p and not re.search(r"[\\/]_(old|unused|rejected|bad)", p) and "AbletonTmp" not in p and not re.search(r"\[\d{4}-\d\d-\d\d \d{6}\]", p)
                  and "Ableton Template Project" not in p)


if __name__ == "__main__":
    bad = 0
    for root in sys.argv[1:]:
        for als in projects(root):
            try:
                ok, msg = check_project(als)
            except Exception as e:
                ok, msg = False, f"ERROR {e}"
            bad += not ok
            print(("PASS " if ok else "FAIL ") + os.path.relpath(als, root) + " | " + msg, flush=True)
    print(f"\n{bad} project(s) FAIL" if bad else "\nAll projects PASS")
    sys.exit(1 if bad else 0)
