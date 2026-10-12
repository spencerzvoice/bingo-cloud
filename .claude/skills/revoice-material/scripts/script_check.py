"""SCRIPT CHECK: does <Client>_script hold every narrated line of its own video, word for word?

Spencer, 2026-10-12 (Airbnb's script was missing its tag line "Now you can Airbnb more than an Airbnb."):
"Make the script writing fool proof. This is the easiest part of the process."

Independent check: a fresh Whisper pass over the client's own source video, compared word by word
with the script text. Whisper text past the end of the video is dropped (it hallucinates repeats over
silence), and so are 1-2 word differences (Whisper mishears "après" as "appraise"). What fails:
  - any run of 3+ narrated words missing from the script (a dropped line, a dropped tag)
  - any run of 3+ script words not in the video (wrong video, a paraphrase, a summary)
  - overall match under 0.85
Prints SCRIPT CHECK OK / SCRIPT CHECK FAILED plus each gap with its timestamp. Exit 1 on FAILED.

Usage:
  python script_check.py "<client folder>"                     # finds the source + <Client>_script.docx
  python script_check.py --src video.mp4 --text script.txt      # cloud: before uploading the script
  add --model medium for a slower, more exact pass (default small)
"""
import argparse, difflib, glob, json, os, re, subprocess, sys

FF = r"C:\Users\spenc\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-full_build\bin"
if os.path.isdir(FF):
    os.environ["PATH"] = FF + os.pathsep + os.environ["PATH"]
GAP = 3          # words in a row
MIN_RATIO = 0.85


def words(t):
    t = t.lower().replace("’", "'").replace("‘", "'")
    t = re.sub(r"(\d),(\d)", r"\1\2", t)
    return re.sub(r"[^a-z0-9' ]", " ", t).split()


def duration(src):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src],
                       capture_output=True, text=True)
    return float(r.stdout.strip() or 0)


def transcribe(src, model):
    import whisper
    dur = duration(src)
    r = whisper.load_model(model).transcribe(src, fp16=False, language="en", condition_on_previous_text=False,
                                             word_timestamps=True)
    out = []  # (word, start) for every word inside the video
    for s in r["segments"]:
        for w in s.get("words", []):
            if dur and w["start"] > dur - 0.3:
                continue
            for x in words(w["word"]):
                out.append((x, w["start"]))
    return out, dur


def script_text(path):
    if path.endswith(".docx"):
        import docx
        paras = [p.text for p in docx.Document(path).paragraphs if p.text.strip()]
    else:
        paras = [l for l in open(path, encoding="utf-8") if l.strip()]
    # drop the "Original copy - from ..., verify against the video." header and anything after a NOTES heading
    body = []
    for p in paras:
        if re.search(r"verify against the video", p, re.I):
            continue
        if re.match(r"\s*(notes?|read notes|direction)\b", p, re.I):
            break
        body.append(p)
    return " ".join(body)


def check(src, text, model="small"):
    vid, dur = transcribe(src, model)
    a = [w for w, _ in vid]
    b = words(text)
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    gaps = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            continue
        t = vid[i1][1] if i1 < len(vid) else (vid[-1][1] if vid else 0)
        if i2 - i1 >= GAP and (op == "delete" or (i2 - i1) - (j2 - j1) >= GAP or j2 - j1 < 2):
            gaps.append(f"MISSING @ {t:.1f}s: video says \"{' '.join(a[i1:i2])}\"" +
                        (f", script has \"{' '.join(b[j1:j2])}\"" if j2 > j1 else ""))
        elif j2 - j1 >= GAP and (op == "insert" or (j2 - j1) - (i2 - i1) >= GAP or i2 - i1 < 2):
            gaps.append(f"EXTRA @ {t:.1f}s: script has \"{' '.join(b[j1:j2])}\", not heard in the video")
        elif i2 - i1 >= GAP or j2 - j1 >= GAP:
            gaps.append(f"DIFFERENT @ {t:.1f}s: video \"{' '.join(a[i1:i2])}\" vs script \"{' '.join(b[j1:j2])}\"")
    ratio = sm.ratio()
    ok = not gaps and ratio >= MIN_RATIO and len(b) > 0
    return ok, ratio, len(a), len(b), dur, gaps


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder", nargs="?")
    ap.add_argument("--src")
    ap.add_argument("--text")
    ap.add_argument("--model", default="small")
    ap.add_argument("--json", action="store_true")
    o = ap.parse_args()
    src, txt = o.src, o.text
    if o.folder:
        fs = os.listdir(o.folder)
        src = src or os.path.join(o.folder, next(f for f in sorted(fs) if " - SOURCE - " in f and f.lower().endswith((".mp4", ".mov"))))
        if not txt:
            d = [f for f in fs if f.endswith("_script.docx") and not f.startswith("~$")]
            if not d:
                print("SCRIPT CHECK FAILED: no _script.docx (a Google Doc script can't be read here; "
                      "export its text and pass --text)")
                sys.exit(1)
            txt = os.path.join(o.folder, d[0])
    ok, ratio, nv, ns, dur, gaps = check(src, script_text(txt), o.model)
    if o.json:
        print(json.dumps({"ok": ok, "ratio": round(ratio, 2), "video_words": nv, "script_words": ns, "gaps": gaps}))
    else:
        print(f"SCRIPT CHECK {'OK' if ok else 'FAILED'}  match {ratio:.2f}  video {nv} words / script {ns} words / {dur:.0f}s")
        for g in gaps:
            print("  " + g)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
