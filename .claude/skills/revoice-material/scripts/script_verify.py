"""STRICT SCRIPT CHECK: three independent ears vote on every word of a re-voice script.

Spencer, 2026-10-28: "Tighten up your transcription, you're missing words on some scripts in Funnel S. With
Funnel S1 and S2 make sure your scripts are 100% correct."

Why script_check.py alone let words through: the script is written by Whisper and then checked by Whisper, so
both passes drop the same words (fast runs, words under music), and the check forgave any 1-word miss. Here:
  ear 1  faster-whisper large-v3 over the source video (a bigger, different model than the one that wrote it)
  ear 2  openai-whisper medium over the source video
  ear 3  the video's own YouTube captions (human ones when the channel uploaded them, else YouTube's ASR),
         trimmed to the excerpt window in sources.txt ("excerpt: 0-62.9 s" / "starts at 5.0 s")
Each ear is aligned to the script. A difference at the same script position heard by 2+ ears is CONFIRMED, at
any length, one word included: that fails the check. A difference only one ear hears is listed as REVIEW (look
at it, don't fail on it). Names spelled two ways ("Ruedel" / "Rudel") are SPELLING: check the proper spelling.
Numbers compare by presence ("twenty-four hundred" = "2,400"), case, punctuation, accents and apostrophes are
ignored.

Usage:
  python script_verify.py "<client folder>"            # source + <Client>_script.docx + sources.txt
  python script_verify.py --src v.mp4 --text s.docx [--url <youtube url> --start 5.0]
  python script_verify.py --funnel "E:/My Drive/Client Outreach/Funnel S"
  --transcript : also print the large-v3 transcript (what to build a fix from)
Exit 1 when any client FAILS. Transcripts and captions are cached in %TEMP%/script_check_cache.
"""
import argparse, difflib, glob, json, os, re, sys, unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from script_check import CACHE, HALLU, duration, script_text, split_notes, transcribe as whisper_ow  # noqa: E402

NUMW = set("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen "
           "seventeen eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety hundred thousand "
           "million billion trillion point percent".split())
SAME = {"mm": "millimeter", "millimetre": "millimeter", "millimeters": "millimeter", "vs": "versus",
        "ok": "okay", "mr": "mister", "dr": "doctor", "st": "saint"}


def toks(t):
    """Spoken-form tokens: lower case, no accents/apostrophes, hyphens split, digit runs and number words -> '#'."""
    t = unicodedata.normalize("NFKD", t)
    t = "".join(c for c in t if not unicodedata.combining(c)).lower()
    t = t.replace("%", " percent ").replace("’", "").replace("'", "").replace("‘", "")
    t = re.sub(r"(\d)[,.](\d)", r"\1\2", t)
    t = re.sub(r"(\d)(?=[a-z])|(?<=[a-z])(\d)", lambda m: (m.group(1) or "") + " " + (m.group(2) or ""), t)
    out = []
    for w in re.sub(r"[^a-z0-9 ]", " ", t).split():
        w = SAME.get(w, w)
        num = w.isdigit() or w in NUMW or (w == "and" and out and out[-1] == "#")
        if num:
            if not (out and out[-1] == "#"):
                out.append("#")
        else:
            out.append(w)
    # "two hundred and fifty": an "and" swallowed inside a number run leaves nothing behind
    return out


def timed_toks(pairs):
    """[(word, t)] -> [(tok, t)] in spoken form, number runs collapsed across word boundaries."""
    out = []
    for w, t in pairs:
        for x in toks(w):
            if x == "#" and out and out[-1][0] == "#":
                continue
            out.append((x, t))
    return out


# ---------- ear 1: faster-whisper large-v3 ----------
def pcm16k(path):
    """Mono 16 kHz float32 via ffmpeg (faster-whisper's own PyAV decoder breaks on this PyAV version)."""
    import subprocess
    import numpy as np
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vn", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def large_words(path, model="large-v3"):
    """[[(word, start, end)] per segment] from faster-whisper, condition_on_previous_text off, no VAD (VAD clips
    soft words)."""
    from faster_whisper import WhisperModel
    m = WhisperModel(model, device="cpu", compute_type="int8")
    segs, _ = m.transcribe(pcm16k(path), language="en", beam_size=5, word_timestamps=True,
                           condition_on_previous_text=False, vad_filter=False)
    return [[(w.word, w.start, w.end) for w in (s.words or [])] for s in segs]


def ear_large(src):
    st = os.stat(src)
    cf = os.path.join(CACHE, "fw_large-v3_" + re.sub(r"[^A-Za-z0-9]+", "_", os.path.basename(src))[:80]
                      + f"_{st.st_size}_{int(st.st_mtime)}.json")
    if os.path.exists(cf):
        ws = json.load(open(cf, encoding="utf-8"))
    else:
        ws = [{"w": w, "s": a, "e": b} for seg in large_words(src) for w, a, b in seg]
        os.makedirs(CACHE, exist_ok=True)
        json.dump(ws, open(cf, "w", encoding="utf-8"))
    dur = duration(src)
    return [(w["w"], w["s"]) for w in ws if not (dur and w["s"] > dur - 0.3)]


def large_text(src):
    return "".join(w for w, _ in ear_large(src)).strip()


# ---------- ear 2: openai-whisper medium ----------
def ear_medium(src):
    vid, _ = whisper_ow(src, "medium")
    return vid  # already (word, t), script_check normalised; toks() re-normalises harmlessly


# ---------- ear 3: YouTube captions ----------
def youtube_id(url):
    m = re.search(r"(?:v=|youtu\.be/|shorts/)([A-Za-z0-9_-]{11})", url or "")
    return m.group(1) if m else None


def fetch_captions(url):
    """{'kind': 'human'|'auto', 'events': [(t_sec, text)]} or None. Human subs win over YouTube's ASR."""
    vid = youtube_id(url)
    if not vid:
        return None
    cf = os.path.join(CACHE, f"yt_caps_{vid}.json")
    if os.path.exists(cf):
        return json.load(open(cf, encoding="utf-8"))
    import urllib.request
    import yt_dlp
    with yt_dlp.YoutubeDL({"quiet": True, "skip_download": True, "no_warnings": True}) as y:
        info = y.extract_info(url, download=False)
    pick = None
    for kind, pool in (("human", info.get("subtitles") or {}), ("auto", info.get("automatic_captions") or {})):
        for lang in ("en", "en-US", "en-GB", "en-orig", "en-en"):
            fmts = {f.get("ext"): f.get("url") for f in pool.get(lang, [])}
            if fmts.get("json3"):
                pick = (kind, fmts["json3"])
                break
        if pick:
            break
    if not pick:
        return None
    data = json.loads(urllib.request.urlopen(pick[1], timeout=60).read().decode("utf-8"))
    r = {"kind": pick[0], "events": parse_json3(data)}
    os.makedirs(CACHE, exist_ok=True)
    json.dump(r, open(cf, "w", encoding="utf-8"))
    return r


def parse_json3(data):
    """YouTube json3 captions -> [(t_sec, word)]."""
    events = []
    for ev in data.get("events", []):
        segs = ev.get("segs") or []
        t0, d = ev.get("tStartMs", 0) / 1000, (ev.get("dDurationMs") or 0) / 1000
        text = "".join(s.get("utf8", "") for s in segs).strip()
        if not text or text == "\n":
            continue
        if len(segs) > 1 and any("tOffsetMs" in s for s in segs):  # ASR: per-word offsets
            for s in segs:
                if s.get("utf8", "").strip():
                    events.append((t0 + s.get("tOffsetMs", 0) / 1000, s["utf8"]))
        else:  # human: one line per event, spread its words over the event
            ws = text.split()
            for k, w in enumerate(ws):
                events.append((t0 + d * k / max(1, len(ws)), w))
    return events


def ear_captions(url, start, dur):
    try:
        caps = fetch_captions(url)
    except Exception as e:  # 429 / offline: the check runs on two ears and says so
        return None, f"captions unavailable ({str(e)[:60]})"
    if not caps:
        return None, "no captions on the video"
    out = [(w, t - start) for t, w in caps["events"] if start - 0.2 <= t <= start + dur + 0.2]
    out = [(w, t) for w, t in out if not re.fullmatch(r"\[.*\]|\(.*\)|♪+", w.strip())]  # [Music], ♪
    return out, f"{caps['kind']} captions"


def excerpt_start(folder):
    p = os.path.join(folder, "sources.txt")
    if not os.path.exists(p):
        return None, 0.0
    txt = open(p, encoding="utf-8", errors="replace").read()
    url = next((l.strip() for l in txt.splitlines() if l.strip().startswith("http")), None)
    m = re.search(r"starts at\s*(\d+(?:\.\d+)?)\s*s", txt) or re.search(r"excerpt:\s*(\d+(?:\.\d+)?)\s*-", txt)
    return url, float(m.group(1)) if m else 0.0


# ---------- voting ----------
def diffs(ear, script):
    """Differences between one ear and the script, keyed by script position: [(j1, j2, ear_words, script_words, t)]."""
    a = [w for w, _ in ear]
    sm = difflib.SequenceMatcher(None, a, script, autojunk=False)
    out = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            continue
        t = ear[i1][1] if i1 < len(ear) else (ear[-1][1] if ear else 0)
        out.append((j1, j2, a[i1:i2], script[j1:j2], t))
    return out


def joined_sim(x, y):
    return difflib.SequenceMatcher(None, "".join(x), "".join(y), autojunk=False).ratio()


def strip_hallu(ear, script):
    sj = " " + " ".join(script) + " "
    a = [w for w, _ in ear]
    keep = [True] * len(ear)
    for ph in HALLU:
        pw = toks(ph)
        if " " + " ".join(pw) + " " in sj:
            continue
        for i in range(len(a) - len(pw) + 1):
            if a[i:i + len(pw)] == pw:
                keep[i:i + len(pw)] = [False] * len(pw)
    return [e for e, k in zip(ear, keep) if k]


def vote(ears, script, notes):
    """ears = {name: [(tok, t)]}. Returns issues [(level, kind, t, text)] sorted by time."""
    per = {n: [d for d in diffs(e, script)] for n, e in ears.items()}
    issues, used = [], set()
    names = list(ears)
    for n in names:
        for k, (j1, j2, ew, sw, t) in enumerate(per[n]):
            if (n, k) in used:
                continue
            if ew and notes and not sw and sum(w in notes for w in ew) * 2 >= len(ew):
                continue  # an on-camera line the script quotes in a [Not narrator] note
            agree, heard_by = [n], {n: ew}
            for m in names:
                if m == n:
                    continue
                for k2, (k1, k2b, ew2, sw2, _t2) in enumerate(per[m]):
                    if (m, k2) in used:
                        continue
                    near = k1 <= j2 + 1 and j1 <= k2b + 1
                    if near and (joined_sim(ew, ew2) >= 0.6 or (not ew and not ew2)):
                        agree.append(m)
                        heard_by[m] = ew2
                        used.add((m, k2))
                        break
            used.add((n, k))
            if sw and ew and len(sw) == len(ew) and joined_sim(ew, sw) >= 0.7:
                kind = "SPELLING"
            elif ew and not sw:
                kind = "MISSING"
            elif sw and not ew:
                kind = "EXTRA"
            else:
                kind = "DIFFERENT"
            same = len({" ".join(v) for v in heard_by.values()}) == 1
            if kind == "EXTRA":
                level = "CONFIRMED" if len(agree) == len(names) else "REVIEW"
            elif kind == "DIFFERENT" and not same and len(agree) >= 2 and sw and                     all(joined_sim(v, sw) >= 0.6 for v in heard_by.values()):
                level, kind = "SPELLING", "SPELLING"  # every ear spells a name its own way ("kimikey"/"kimik")
            elif kind == "SPELLING":
                # two ears that hear the SAME other word ("company" for "companies'") = a wrong word; ears that
                # spell it differently from each other ("kimikey"/"kimiki") = a name: check the spelling by hand
                level = "CONFIRMED" if len(agree) >= 2 and same else "SPELLING"
            else:
                level = "CONFIRMED" if len(agree) >= 2 else "REVIEW"
            ears_txt = "; ".join(f"{m}: {' '.join(v) or '-'}" for m, v in heard_by.items())
            text = (f"script \"{' '.join(sw)}\" not heard" if kind == "EXTRA" else
                    f"script \"{' '.join(sw) or '(nothing)'}\" / heard [{ears_txt}]")
            issues.append((level, kind, t, text))
    return sorted(issues, key=lambda x: x[2])


def strict(src, text_file_or_text, url=None, start=0.0):
    raw = script_text(text_file_or_text) if os.path.exists(str(text_file_or_text)) else text_file_or_text
    body, _ = split_notes(raw)
    notes = toks(" ".join(re.findall(r"\[([^\]]*)\]", raw)))
    script = toks(body)
    dur = duration(src)
    ears, info = {}, []
    ears["large-v3"] = timed_toks(ear_large(src))
    ears["medium"] = timed_toks(ear_medium(src))
    if url:
        caps, msg = ear_captions(url, start, dur)
        info.append(msg)
        if caps:
            ears["captions"] = timed_toks(caps)
    else:
        info.append("no URL, captions not used")
    ears = {n: strip_hallu(e, script) for n, e in ears.items()}
    issues = vote(ears, script, notes)
    bad = [i for i in issues if i[0] == "CONFIRMED"]
    ok = not bad and bool(script)
    head = (f"STRICT CHECK {'OK' if ok else 'FAILED'}  {len(bad)} confirmed / "
            f"{sum(i[0] == 'REVIEW' for i in issues)} review / {sum(i[0] == 'SPELLING' for i in issues)} spelling  "
            f"ears: {', '.join(ears)} ({'; '.join(info)})  script {len(script)} tokens / {dur:.0f}s")
    return ok, head, issues


def run_folder(folder, show_transcript=False):
    fs = os.listdir(folder)
    srcs = sorted(f for f in fs if " - SOURCE - " in f and f.lower().endswith((".mp4", ".mov")))
    scr = [f for f in fs if f.endswith("_script.docx") and not f.startswith("~$")]
    if not srcs or not scr:
        print(f"== {os.path.basename(folder)}: no source video or no _script.docx")
        return False
    url, start = excerpt_start(folder)
    ok, head, issues = strict(os.path.join(folder, srcs[0]), os.path.join(folder, scr[0]), url, start)
    print(f"== {os.path.basename(folder)}: {head}")
    for lvl, kind, t, txt in issues:
        print(f"   {lvl:9} {kind:9} @ {t:5.1f}s  {txt}")
    if show_transcript:
        print("   large-v3: " + large_text(os.path.join(folder, srcs[0])))
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder", nargs="?")
    ap.add_argument("--funnel")
    ap.add_argument("--src")
    ap.add_argument("--text")
    ap.add_argument("--url")
    ap.add_argument("--start", type=float, default=0.0)
    ap.add_argument("--transcript", action="store_true")
    o = ap.parse_args()
    if o.funnel:
        dirs = [d for d in sorted(glob.glob(os.path.join(o.funnel, "*"))) if os.path.isdir(d)
                and not os.path.basename(d).startswith("_")]
        res = [run_folder(d, o.transcript) for d in dirs]
        sys.exit(0 if all(res) else 1)
    if o.folder:
        sys.exit(0 if run_folder(o.folder, o.transcript) else 1)
    ok, head, issues = strict(o.src, o.text, o.url, o.start)
    print(head)
    for lvl, kind, t, txt in issues:
        print(f"   {lvl:9} {kind:9} @ {t:5.1f}s  {txt}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
