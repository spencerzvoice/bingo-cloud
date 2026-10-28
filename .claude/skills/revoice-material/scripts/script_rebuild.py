"""Rebuild a client's <Client>_script.docx from corrected words, laid out by script_lines.py.

Spencer, 2026-10-28: Funnel S scripts were missing words and read badly ("random indentations and spacing").
Words come from a corrected text file (the large-v3 transcript, fixed where the strict check's ears agree,
names spelled from the channel's own page); line breaks come from the cached large-v3 word timings of the
source video. The old script is moved (never deleted) to "_rejected - old script <date>/".

Usage:
  python script_rebuild.py "<client folder>" --text corrected.txt [--header "..."] [--dry]
  python script_rebuild.py "<client folder>" --print-transcript     # the large-v3 words to start from
Then: script_verify.py "<client folder>" must say STRICT CHECK OK and script_lines.py --lint FORMAT OK.
"""
import argparse, datetime, os, shutil, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from script_lines import adopt_text, cap_first, clean, lint, phrase_lines, write_docx  # noqa: E402
from script_verify import CACHE, ear_large, large_text  # noqa: E402

HEADER = "Original copy - Whisper large-v3, checked against the captions. Verify against the video."


def source(folder):
    return os.path.join(folder, next(f for f in sorted(os.listdir(folder))
                                     if " - SOURCE - " in f and f.lower().endswith((".mp4", ".mov"))))


def timed(src):
    """(word, start, end) from the cached large-v3 pass over the source."""
    import glob, json, re
    ear_large(src)  # fills the cache
    st = os.stat(src)
    cf = os.path.join(CACHE, "fw_large-v3_" + re.sub(r"[^A-Za-z0-9]+", "_", os.path.basename(src))[:80]
                      + f"_{st.st_size}_{int(st.st_mtime)}.json")
    return [(w["w"], w["s"], w["e"]) for w in json.load(open(cf, encoding="utf-8"))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--text")
    ap.add_argument("--header", default=HEADER)
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--note", action="append", default=[],
                    help="a [bracketed] read note, placed after the copy ('[Clip ends on ... skip it.]')")
    ap.add_argument("--print-transcript", action="store_true")
    o = ap.parse_args()
    src = source(o.folder)
    if o.print_transcript:
        print(large_text(src))
        return
    text = clean(" ".join(open(o.text, encoding="utf-8").read().split()))
    lines = cap_first(phrase_lines(adopt_text(timed(src), text)))
    for l in lines:
        print(l)
    iss = lint([o.header] + lines)
    print("FORMAT OK" if not iss else "\n".join(iss))
    if o.dry:
        return
    client = os.path.basename(os.path.normpath(o.folder))
    out = os.path.join(o.folder, f"{client}_script.docx")
    if os.path.exists(out):
        old = os.path.join(o.folder, f"_rejected - old script {datetime.date.today()}")
        os.makedirs(old, exist_ok=True)
        keep = os.path.join(old, f"{client}_script.docx")
        if os.path.exists(keep):  # the original is already kept: never overwrite it with a later rebuild
            os.remove(out)
        else:
            shutil.move(out, keep)
    write_docx(lines + [clean(n) for n in o.note], out, o.header)
    print("wrote", out)


if __name__ == "__main__":
    main()
