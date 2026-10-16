"""Write a re-voice <Client>_script.docx laid out the way the narrator says it: one line per spoken phrase.

Spencer, 2026-10-14: "Scripts need to be written better. They're sentences that are run on and should be
chopped up. Pay attention to the pauses and the audio, and present the lines as they are heard ... Make sure
there are no weird spaces and random places."

How: a word-timestamped Whisper pass over the narration (the Demucs vocal stem when there is one) gives every
word's start/end. A line ends where the narrator breathes or holds (gap >= PAUSE) and at every sentence end.
A phrase still longer than MAX_WORDS is split at its comma nearest the middle, else at its longest gap. A
one- or two-word scrap is folded back into its neighbour unless the narrator really isolates it (gap >= HOLD).
Every line is whitespace-cleaned (no doubled/leading/trailing spaces, no space before punctuation, no NBSP or
tabs, no empty paragraphs).

--text: when better words exist (human captions), the words come from that text and only the line breaks come
from the audio (difflib aligns the two). Words are never changed, only where the lines break.

Never run on an existing script without Spencer's OK (10-13: re-flowing finished scripts "made them worse").
This is for NEW scripts; revoice_build.whisper_script() and the cloud Re-Voicing step 2c call it.

Usage:
  python script_lines.py --audio <vocals.wav or source.mp4> --video <source.mp4> --out <Client>_script.docx
                         [--text captions.txt] [--client Sophos] [--header "Original copy - ..."] [--model medium]
  python script_lines.py --lint <script.docx> [...]     # format check only, prints FORMAT OK / issues
"""
import argparse, difflib, json, os, re, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from script_check import HALLU, CACHE, duration, words as norm_words  # noqa: E402

PAUSE = 0.30      # s of silence that ends a spoken line
HOLD = 0.60       # s of silence that keeps even a 1-2 word line on its own ("Cash App.")
MAX_WORDS = 12    # a phrase longer than this gets split
MIN_WORDS = 3     # shorter lines are folded into a neighbour unless held
# a spoken line doesn't end on these unless the narrator really holds (gap >= HOLD)
CLINGY = set("a an the your my our their his her its this that these those to of for with in on at by from "
             "and or but so as into onto than like every each no".split())
DEFAULT_HEADER = "Original copy - from Whisper transcription, verify against the video."


def norm(w):
    return re.sub(r"[^a-z']", "", w.lower())


def fix_brand(tw, client):
    """Whisper spells a brand by ear ("Sofos"); a near-miss of a one-word client name gets the real spelling."""
    if not client or " " in client.strip():
        return tw
    c = norm(client)
    out = []
    for w, s, e in tw:
        core = re.sub(r"^[^A-Za-z]+|[^A-Za-z']+$", "", w.strip())
        k = norm(core)
        if core and k != c and len(k) >= 3 and abs(len(k) - len(c)) <= 2 and difflib.SequenceMatcher(None, k, c).ratio() >= 0.7:
            w = w.replace(core, client)
        out.append((w, s, e))
    return out


def clean(t):
    t = t.replace(" ", " ").replace("\t", " ").replace("​", "")
    t = re.sub(r" {2,}", " ", t)
    t = re.sub(r" +([.,!?;:%])", r"\1", t)
    t = re.sub(r"([(\[“]) +", r"\1", t)
    t = re.sub(r" +([)\]”])", r"\1", t)
    t = re.sub(r"([,;:!?])(?=[A-Za-z“\"])", r"\1 ", t)
    t = re.sub(r"(?<![.\d])\.(?=[A-Z])", ". ", t)
    return t.strip()


def timed_words(audio, video, model="medium"):
    """[(text, start, end)] for every narrated word inside the video, Whisper filler dropped. Cached."""
    dur = duration(video or audio)
    st = os.stat(audio)
    key = "lines_" + re.sub(r"[^A-Za-z0-9]+", "_", os.path.basename(audio))[:80] + f"_{st.st_size}_{int(st.st_mtime)}_{model}.json"
    cf = os.path.join(CACHE, key)
    if os.path.exists(cf):
        segs = json.load(open(cf, encoding="utf-8"))
    else:
        import whisper
        r = whisper.load_model(model).transcribe(audio, fp16=False, language="en",
                                                 condition_on_previous_text=False, word_timestamps=True)
        segs = [[{"w": w["word"], "s": w["start"], "e": w["end"]} for w in s.get("words", [])] for s in r["segments"]]
        os.makedirs(CACHE, exist_ok=True)
        json.dump(segs, open(cf, "w", encoding="utf-8"))
    out = []
    for seg in segs:
        txt = re.sub(r"[^a-z' ]", "", "".join(w["w"] for w in seg).lower()).strip()
        if txt in HALLU:
            continue
        for w in seg:
            if dur and w["s"] > dur - 0.3:
                continue
            if w["w"].strip():
                out.append((w["w"], w["s"], w["e"]))
    return out


def adopt_text(tw, text):
    """Swap Whisper's words for the caption text's, keeping Whisper's timing: [(word, start, end)]."""
    toks = clean(" ".join(text.split())).split(" ")
    a = [" ".join(norm_words(t)) for t in toks]  # noqa
    b = [" ".join(norm_words(w)) for w, _, _ in tw]
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    times = [None] * len(toks)
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            times[blk.a + k] = tw[blk.b + k][1:]
    # unmatched tokens borrow the previous token's end so they never create a fake gap
    last = (0.0, 0.0)
    out = []
    for t, tm in zip(toks, times):
        tm = tm or (last[1], last[1])
        out.append((" " + t, tm[0], tm[1]))
        last = tm
    return out


def split_long(line):
    """line = [(word, s, e)] -> list of lines, none over MAX_WORDS where a clean split exists."""
    if len(line) <= MAX_WORDS:
        return [line]
    mid = len(line) / 2
    commas = [i for i, (w, _, _) in enumerate(line[:-1]) if w.rstrip().endswith((",", ";", ":", "—"))
              and i + 1 >= MIN_WORDS and len(line) - i - 1 >= MIN_WORDS]
    if commas:
        i = min(commas, key=lambda i: abs(i + 1 - mid))
    else:
        cands = range(MIN_WORDS - 1, len(line) - MIN_WORDS)
        if not cands:
            return [line]
        i = max(cands, key=lambda i: (line[i + 1][1] - line[i][2], -abs(i + 1 - mid)))
    return split_long(line[:i + 1]) + split_long(line[i + 1:])


def phrase_lines(tw):
    """Break the timed words where the narrator pauses and at sentence ends."""
    lines, cur, gaps = [], [], []
    for i, w in enumerate(tw):
        cur.append(w)
        nxt = tw[i + 1] if i + 1 < len(tw) else None
        gap = (nxt[1] - w[2]) if nxt else 9.9
        end = w[0].strip()
        if end.endswith((".", "!", "?")) or (gap >= PAUSE and (gap >= HOLD or norm(end) not in CLINGY)):
            lines.append(cur)
            gaps.append(gap)
            cur = []
    if cur:
        lines.append(cur)
        gaps.append(9.9)
    # fold short scraps into a neighbour unless the narrator isolates them
    i = 0
    while i < len(lines):
        ln = lines[i]
        before = gaps[i - 1] if i else 9.9
        after = gaps[i]
        if len(ln) < MIN_WORDS and len(lines) > 1 and not (before >= HOLD and after >= HOLD) \
                and not ln[-1][0].strip().endswith((".", "!", "?")):
            # glue to the side with the shorter silence, never across a sentence end
            prev_ok = i > 0 and not lines[i - 1][-1][0].strip().endswith((".", "!", "?"))
            if i + 1 < len(lines) and (after <= before or not prev_ok):
                lines[i + 1] = ln + lines[i + 1]
                del lines[i], gaps[i]
                continue
            if prev_ok:
                lines[i - 1] = lines[i - 1] + ln
                gaps[i - 1] = gaps[i]
                del lines[i], gaps[i]
                continue
        i += 1
    out = []
    for ln in lines:
        out += split_long(ln)
    return [clean("".join(w for w, _, _ in ln)) for ln in out if ln]


def cap_first(lines):
    """A line that starts a new sentence starts with a capital; mid-sentence lines stay as spoken."""
    out = []
    for i, l in enumerate(lines):
        if l and (i == 0 or out[-1].endswith((".", "!", "?"))):
            l = l[0].upper() + l[1:]
        out.append(l)
    return out


def write_docx(lines, out, header=DEFAULT_HEADER):
    import docx
    from docx.shared import Pt
    d = docx.Document()
    st = d.styles["Normal"]
    st.font.name, st.font.size = "Arial", Pt(14)
    st.paragraph_format.space_after = Pt(6)
    st.paragraph_format.line_spacing = 1.15
    d.add_paragraph(clean(header))
    for l in lines:
        d.add_paragraph(l)
    d.save(out)


def build(audio, video, out, text=None, header=DEFAULT_HEADER, model="medium", client=None):
    tw = timed_words(audio, video, model)
    if text:
        tw = adopt_text(tw, text)
    tw = fix_brand(tw, client)
    lines = cap_first(phrase_lines(tw))
    write_docx(lines, out, header)
    return lines


def lint(paras):
    """Format issues in a script's paragraphs (list of str). Empty list = FORMAT OK."""
    issues = []
    for n, p in enumerate(paras, 1):
        if not p.strip():
            if 1 < n < len(paras):
                issues.append(f"para {n}: empty line inside the script")
            continue
        for pat, what in [(r"^\s|\s$", "leading/trailing space"), (r" {2,}", "double space"),
                          (r" [.,!?;:]", "space before punctuation"), (r"[ \t​]", "tab/non-breaking space"),
                          (r"[,;:!?](?=[A-Za-z])", "no space after punctuation")]:
            if re.search(pat, p):
                issues.append(f"para {n}: {what}: {p.strip()[:60]!r}")
        if len(p.split()) > MAX_WORDS + 4 and not p.lstrip().startswith(("[", "Original copy", "Note")):
            issues.append(f"para {n}: run-on line ({len(p.split())} words): {p.strip()[:60]!r}")
    return issues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audio")
    ap.add_argument("--video")
    ap.add_argument("--out")
    ap.add_argument("--text", help="file with better words (captions); breaks still come from the audio")
    ap.add_argument("--header", default=DEFAULT_HEADER)
    ap.add_argument("--model", default="medium")
    ap.add_argument("--client", help="one-word brand name, used to correct Whisper's spelling of it")
    ap.add_argument("--lint", nargs="+")
    a = ap.parse_args()
    if a.lint:
        import docx
        bad = 0
        for f in a.lint:
            iss = lint([p.text for p in docx.Document(f).paragraphs])
            print(f"{os.path.basename(f)}: " + ("FORMAT OK" if not iss else f"{len(iss)} FORMAT ISSUES"))
            for i in iss:
                print("   " + i)
            bad += bool(iss)
        sys.exit(1 if bad else 0)
    if not (a.audio and a.out):
        ap.error("--audio and --out are required (or --lint)")
    text = open(a.text, encoding="utf-8").read() if a.text else None
    for l in build(a.audio, a.video or a.audio, a.out, text, a.header, a.model, a.client):
        print(l)


if __name__ == "__main__":
    main()
