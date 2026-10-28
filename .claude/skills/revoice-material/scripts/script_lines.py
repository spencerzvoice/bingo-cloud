"""Write a re-voice <Client>_script.docx laid out the way the narrator says it: one line per spoken phrase.

Spencer, 2026-10-14: "Scripts need to be written better. They're sentences that are run on and should be
chopped up. Pay attention to the pauses and the audio, and present the lines as they are heard ... Make sure
there are no weird spaces and random places."

How: a word-timestamped Whisper pass over the narration (the Demucs vocal stem when there is one) gives every
word's start/end. A line ends at every sentence end and at clause punctuation; a clause still over MAX_CHARS is
split at the narrator's longest pause, never after "the/a/to/and..." and never inside a number or date.
Spencer, 2026-10-28 ("weird formatting issues, random indentations and spacing that is distracting"): the old
pause-only breaker cut mid-phrase ("just caught / up with", "platoon / leader", "December 22, / 1941") and let
66-character lines wrap one word onto its own line. Now no line wraps on the page (MAX_CHARS, 1" margins), one
font, the same 6 pt after every line, and a small grey header.
Every line is whitespace-cleaned (no doubled/leading/trailing spaces, no space before punctuation, no NBSP or
tabs, no empty paragraphs).

--text: when better words exist (human captions), the words come from that text and only the line breaks come
from the audio (difflib aligns the two). Words are never changed, only where the lines break.

Never run on an existing script without Spencer's OK (10-13: re-flowing finished scripts "made them worse").
This is for NEW scripts; revoice_build.whisper_script() and the cloud Re-Voicing step 2c call it.

Usage:
  python script_lines.py --audio <vocals.wav or source.mp4> --video <source.mp4> --out <Client>_script.docx
                         [--text captions.txt] [--client Sophos] [--header "Original copy - ..."] [--model large-v3|medium]
  python script_lines.py --lint <script.docx> [...]     # format check only, prints FORMAT OK / issues
"""
import argparse, difflib, json, os, re, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from script_check import HALLU, CACHE, duration, words as norm_words  # noqa: E402

PAUSE = 0.30      # s of silence that ends a spoken line
HOLD = 0.60       # s of silence that keeps even a 1-2 word line on its own ("Cash App.")
MAX_WORDS = 12    # a phrase longer than this gets split
MIN_WORDS = 3     # shorter lines are folded into a neighbour unless held
MAX_CHARS = 68    # longest built line; Arial 14 at 6" wrapped a 71-char line, the 6.5" text width holds ~75 (Word, 10-28)
# a split lands best just before one of these ("... locked on company servers, / and Kimi is ...")
LEADS = set("and but or so because since while when where which who whose that if though although as until "
            "unless after before with without from into across through for on in at by".split())
# a spoken line doesn't end on these unless the narrator really holds (gap >= HOLD)
CLINGY = set("a an the your my our their his her its this that these those to of for with in on at by from "
             "and or but so as into onto than like every each no just".split())
DEFAULT_HEADER = "Original copy - from Whisper transcription, verify against the video."
try:  # large-v3 wherever faster-whisper is installed (desktop); the cloud keeps openai-whisper medium
    import faster_whisper  # noqa: F401
    DEFAULT_MODEL = "large-v3"
except ImportError:
    DEFAULT_MODEL = "medium"


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


def timed_words(audio, video, model=DEFAULT_MODEL):
    """[(text, start, end)] for every narrated word inside the video, Whisper filler dropped. Cached."""
    dur = duration(video or audio)
    st = os.stat(audio)
    key = "lines_" + re.sub(r"[^A-Za-z0-9]+", "_", os.path.basename(audio))[:80] + f"_{st.st_size}_{int(st.st_mtime)}_{model}.json"
    cf = os.path.join(CACHE, key)
    if os.path.exists(cf):
        segs = json.load(open(cf, encoding="utf-8"))
    elif model.startswith("large"):
        # faster-whisper large-v3 (desktop): the medium pass dropped words on Funnel S (Spencer, 2026-10-28)
        from script_verify import large_words
        segs = [[{"w": w, "s": a, "e": b} for w, a, b in seg] for seg in large_words(audio, model)]
        os.makedirs(CACHE, exist_ok=True)
        json.dump(segs, open(cf, "w", encoding="utf-8"))
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
    """line = [(word, s, e)] -> lines of at most MAX_CHARS, split at the narrator's longest pause on a clean
    boundary (a comma first; never after a clingy word, never inside a number), each side MIN_WORDS or more."""
    if chars(line) <= MAX_CHARS or len(line) < 2 * MIN_WORDS:
        return [line]
    span = range(MIN_WORDS - 1, len(line) - MIN_WORDS)
    cands = [i for i in span if not bad_break(line, i)] or list(span)
    mid = len(line) / 2
    i = max(cands, key=lambda i: (wtxt(line[i]).endswith((",", ";", ":", "—")), norm(wtxt(line[i + 1])) in LEADS,
                                  round(line[i + 1][1] - line[i][2], 1), -abs(i + 1 - mid)))
    return split_long(line[:i + 1]) + split_long(line[i + 1:])


def wtxt(w):
    return w[0].strip()


def chars(line):
    return len(" ".join(wtxt(w) for w in line))


def bad_break(line, i):
    """True when a line must not end after word i: a clingy word, or inside a number/date ("22, 1941")."""
    cur, nxt = wtxt(line[i]), (wtxt(line[i + 1]) if i + 1 < len(line) else "")
    if norm(cur) in CLINGY or (re.search(r"\d,?$", cur) and re.match(r"[$\d]", nxt)):
        return True
    # inside a name or model number: "Kimi K3.1 / Pro", "Benjamin / Morin"
    return bool(nxt and not re.search(r"[,.;:!?]$", cur) and re.match(r"[A-Z0-9]", cur) and re.match(r"[A-Z0-9]", nxt))


def phrase_lines(tw):
    """Sentence ends always break. Clause punctuation (, ; : —) breaks when both halves are real phrases
    (MIN_WORDS+) and it isn't inside a number. A clause still over MAX_CHARS goes to split_long(). Short
    neighbours that fit on one line are joined, so no line is a 1-2 word scrap."""
    sents, cur = [], []
    for w in tw:
        cur.append(w)
        if wtxt(w).endswith((".", "!", "?")):
            sents.append(cur)
            cur = []
    if cur:
        sents.append(cur)
    out = []
    for sent in sents:
        clauses, c = [], []
        for i, w in enumerate(sent):
            c.append(w)
            if wtxt(w).endswith((",", ";", ":", "—")) and not bad_break(sent, i):
                clauses.append(c)
                c = []
        if c:
            clauses.append(c)
        merged = []
        for c in clauses:
            if merged and (len(merged[-1]) < MIN_WORDS or len(c) < MIN_WORDS) and chars(merged[-1] + c) <= MAX_CHARS:
                merged[-1] = merged[-1] + c
            else:
                merged.append(c)
        for c in merged:
            out += split_long(c)
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
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn
    from docx.shared import Inches, Pt, RGBColor
    d = docx.Document()
    for sec in d.sections:
        sec.left_margin = sec.right_margin = sec.top_margin = sec.bottom_margin = Inches(1)
    st = d.styles["Normal"]
    st.font.name, st.font.size = "Arial", Pt(14)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")  # one font for every glyph
    pf = st.paragraph_format
    pf.space_before, pf.space_after, pf.line_spacing = Pt(0), Pt(6), 1.15
    pf.left_indent = pf.right_indent = pf.first_line_indent = Inches(0)
    pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    h = d.add_paragraph()  # small grey header, so it never reads as copy
    r = h.add_run(clean(header))
    r.font.size, r.italic, r.font.color.rgb = Pt(10), True, RGBColor(0x80, 0x80, 0x80)
    h.paragraph_format.space_after = Pt(14)
    for l in lines:
        d.add_paragraph(l)
    d.save(out)


def build(audio, video, out, text=None, header=DEFAULT_HEADER, model=DEFAULT_MODEL, client=None):
    tw = timed_words(audio, video, model)
    if text:
        tw = adopt_text(tw, text)
    tw = fix_brand(tw, client)
    lines = cap_first(phrase_lines(tw))
    write_docx(lines, out, header)
    return lines


def lint(paras, doc=None):
    """Format issues in a script's paragraphs (list of str), plus the page layout when the python-docx `doc` is
    given. Empty list = FORMAT OK."""
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
        if p.lstrip().startswith(("[", "Original copy", "Note")):
            continue
        if len(p.strip()) > MAX_CHARS + 4:
            issues.append(f"para {n}: long line, wraps on the page ({len(p.strip())} chars): {p.strip()[:60]!r}")
        last = norm(p.split()[-1])
        if last in CLINGY and not p.rstrip().endswith((".", "!", "?", ",", ";", ":")):
            issues.append(f"para {n}: breaks mid-phrase after \"{last}\": {p.strip()[-40:]!r}")
        if n < len(paras) and re.search(r"\d,?$", p.strip()) and re.match(r"\s*[$\d]", paras[n]):
            issues.append(f"para {n}: number/date split across lines: {p.strip()[-20:]!r} / {paras[n].strip()[:12]!r}")
    if doc is not None:  # the page itself: indents, tabs/breaks inside a line, uneven spacing
        for n, para in enumerate(doc.paragraphs, 1):
            f = para.paragraph_format
            if any(x not in (None, 0) for x in (f.left_indent, f.first_line_indent, f.right_indent)):
                issues.append(f"para {n}: indented")
            if any("\n" in r.text or "\t" in r.text for r in para.runs):
                issues.append(f"para {n}: line break/tab inside a line")
            if n > 1 and (f.space_before not in (None, 0) or f.space_after is not None):
                issues.append(f"para {n}: its own spacing, uneven with the rest")
    return issues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audio")
    ap.add_argument("--video")
    ap.add_argument("--out")
    ap.add_argument("--text", help="file with better words (captions); breaks still come from the audio")
    ap.add_argument("--header", default=DEFAULT_HEADER)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--client", help="one-word brand name, used to correct Whisper's spelling of it")
    ap.add_argument("--lint", nargs="+")
    a = ap.parse_args()
    if a.lint:
        import docx
        bad = 0
        for f in a.lint:
            dd = docx.Document(f)
            iss = lint([p.text for p in dd.paragraphs], dd)
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
