"""SCRIPT CHECK: does <Client>_script hold every narrated line of its own video, word for word?

Spencer, 2026-10-12 (Airbnb's script was missing its tag line "Now you can Airbnb more than an Airbnb."):
"Make the script writing fool proof. This is the easiest part of the process."

Independent check: a fresh Whisper pass over the client's own source video, compared word by word
with the script text. Whisper text past the end of the video is dropped (it hallucinates repeats over
silence), and so are 1-2 word differences (Whisper mishears "après" as "appraise"). What fails:
  - narrated words missing from the script: any clean hole of 2+ words, or a swap that loses 3+ (a dropped
    line, a dropped tag)
  - any run of 3+ script words not in the video (wrong video, a paraphrase, a summary)
  - overall letter-level match under 0.85 (another video's copy)
A same-length swap that sounds alike ("in go1 learn" / "and go unlearn") is a mishearing and passes.
Prints SCRIPT CHECK OK / SCRIPT CHECK FAILED plus each gap with its timestamp. Exit 1 on FAILED.

Usage:
  python script_check.py "<client folder>"                     # finds the source + <Client>_script.docx
  python script_check.py --src video.mp4 --text script.txt      # cloud: before uploading the script
  add --model medium to skip the small pass (default: small, and a FAILED small pass is re-run on medium
  before it's reported, so a mishearing doesn't fail a good script)

Transcripts are cached per video (by path, size, mtime, model) in %TEMP%/script_check_cache, so re-running
the gate after a script fix costs nothing. [Bracketed notes] in the script are not read as script; a run
of video words that a note names ("[Not narrator: ... says 'Happy birthday!']") is waived, not failed.
"""
import argparse, difflib, glob, json, os, re, subprocess, sys

FF = r"C:\Users\spenc\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-full_build\bin"
if os.path.isdir(FF):
    os.environ["PATH"] = FF + os.pathsep + os.environ["PATH"]
GAP = 3          # words in a row
MIN_RATIO = 0.85
CACHE = os.path.join(os.environ.get("TEMP") or os.environ.get("TMPDIR") or "/tmp", "script_check_cache")
# Whisper's stock hallucinations over trailing music/silence; dropped unless the script really has them
HALLU = ["thanks for watching", "thank you for watching", "see you in the next video", "i'll see you in the next video",
         "please subscribe", "subscribe to the channel", "like and subscribe", "bye"]


def words(t):
    t = t.lower().replace("’", "'").replace("‘", "'")
    t = re.sub(r"(\d),(\d)", r"\1\2", t)
    t = re.sub(r"(?<=[a-z])(\d)\b", r" \1", t)  # "go1" -> "go 1"
    t = re.sub(r"\b(\d)\b", lambda m: DIGITS[int(m.group(1))], t)  # Whisper spells single digits out
    return re.sub(r"[^a-z0-9' ]", " ", t).split()


DIGITS = "zero one two three four five six seven eight nine".split()


def duration(src):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src],
                       capture_output=True, text=True)
    return float(r.stdout.strip() or 0)


def transcribe(src, model):
    dur = duration(src)
    st = os.stat(src)
    key = re.sub(r"[^A-Za-z0-9]+", "_", os.path.basename(src))[:80] + f"_{st.st_size}_{int(st.st_mtime)}_{model}.json"
    cf = os.path.join(CACHE, key)
    if os.path.exists(cf):
        r = json.load(open(cf, encoding="utf-8"))
    else:
        import whisper
        r = whisper.load_model(model).transcribe(src, fp16=False, language="en", condition_on_previous_text=False,
                                                 word_timestamps=True)
        r = {"segments": [{"words": [{"word": w["word"], "start": w["start"]} for w in s.get("words", [])]}
                          for s in r["segments"]]}
        os.makedirs(CACHE, exist_ok=True)
        json.dump(r, open(cf, "w", encoding="utf-8"))
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
        if re.match(r"\s*(notes?|read notes|direction)\s*(:|$)", p, re.I):
            break
        body.append(p)
    return " ".join(body)


def split_notes(text):
    """(script without [bracketed notes], the words inside the notes)"""
    notes = " ".join(re.findall(r"\[([^\]]*)\]", text))
    return re.sub(r"\[[^\]]*\]", " ", text), words(notes)


def drop_hallucinations(vid, script_words):
    sj = " " + " ".join(script_words) + " "
    a = [w for w, _ in vid]
    keep = [True] * len(vid)
    for ph in HALLU:
        pw = ph.split()
        if " " + ph + " " in sj:
            continue
        for i in range(len(a) - len(pw) + 1):
            if a[i:i + len(pw)] == pw:
                for k in range(i, i + len(pw)):
                    keep[k] = False
    return [v for v, k in zip(vid, keep) if k]


def in_notes(run, notes):
    """True if a run of video words is named inside a script note (an on-camera line kept out of the read)."""
    if not run or not notes:
        return False
    hits = sum(1 for w in run if w in notes)
    return hits >= max(2, round(0.75 * len(run)))


def misheard(va, sb):
    """A same-length swap that sounds alike is Whisper mishearing, not a script fault: "in go1 learn" heard as
    "and go unlearn" (Go1), "speedvault" as "speed vault". Dropped/added lines change the length, so they
    never land here; a long swap must sound very alike to pass."""
    if abs(len(va) - len(sb)) > 1:
        return False
    sim = difflib.SequenceMatcher(None, "".join(va), "".join(sb), autojunk=False).ratio()
    return sim >= (0.6 if max(len(va), len(sb)) <= 4 else 0.75)


def check(src, text, model="small"):
    body, notes = split_notes(text)
    b = words(body)
    vid, dur = transcribe(src, model)
    vid = drop_hallucinations(vid, b)
    a = [w for w, _ in vid]
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    gaps = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            continue
        t = vid[i1][1] if i1 < len(vid) else (vid[-1][1] if vid else 0)
        if op == "delete" and in_notes(a[i1:i2], notes):
            continue
        if op == "replace" and misheard(a[i1:i2], b[j1:j2]):
            continue
        if op == "delete" and i2 - i1 >= 2:  # a clean 2-word hole is a dropped tag ("Calm Business."), not a mishearing
            gaps.append(f"MISSING @ {t:.1f}s: video says \"{' '.join(a[i1:i2])}\"")
        elif i2 - i1 >= GAP and (op == "delete" or (i2 - i1) - (j2 - j1) >= GAP or j2 - j1 < 2):
            gaps.append(f"MISSING @ {t:.1f}s: video says \"{' '.join(a[i1:i2])}\"" +
                        (f", script has \"{' '.join(b[j1:j2])}\"" if j2 > j1 else ""))
        elif j2 - j1 >= GAP and (op == "insert" or (j2 - j1) - (i2 - i1) >= GAP or i2 - i1 < 2):
            gaps.append(f"EXTRA @ {t:.1f}s: script has \"{' '.join(b[j1:j2])}\", not heard in the video")
        elif i2 - i1 >= GAP or j2 - j1 >= GAP:
            gaps.append(f"DIFFERENT @ {t:.1f}s: video \"{' '.join(a[i1:i2])}\" vs script \"{' '.join(b[j1:j2])}\"")
    # letter-level match: a run of sound-alike mishearings ("fast is when" / "fast as one", On) barely moves it,
    # another video's copy sinks it
    ratio = difflib.SequenceMatcher(None, "".join(a), "".join(b), autojunk=False).ratio()
    ok = not gaps and ratio >= MIN_RATIO and len(b) > 0
    return ok, ratio, len(a), len(b), dur, gaps


def verify(src, text, model="small"):
    """check() with the medium re-hear on a small-model miss. Returns (ok, one-line verdict, gaps)."""
    ok, ratio, nv, ns, dur, gaps = check(src, text, model)
    if not ok and model == "small":
        model = "medium"
        ok, ratio, nv, ns, dur, gaps = check(src, text, model)
    line = (f"SCRIPT CHECK {'OK' if ok else 'FAILED'}  match {ratio:.2f}  video {nv} words / script {ns} words / "
            f"{dur:.0f}s ({model})")
    return ok, line, gaps


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
    ok, line, gaps = verify(src, script_text(txt), o.model)
    if o.json:
        print(json.dumps({"ok": ok, "verdict": line, "gaps": gaps}))
    else:
        print(line)
        for g in gaps:
            print("  " + g)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
