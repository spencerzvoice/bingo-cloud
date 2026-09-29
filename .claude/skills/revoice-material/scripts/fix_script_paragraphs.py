"""Rebuild a _script.docx's body as one paragraph per sentence.

These scripts were built by hard-wrapping the transcript at a fixed line width instead of
breaking on sentence boundaries, so a paragraph break (a visible gap in Word) lands mid-
sentence. That reads as broken flow / "random spaces" between phrases. This re-flows the
body into full sentences -- it only changes paragraph breaks and joins fragments with a
single space; it never changes a word. The header line ("Original copy - ...") and any
trailing blank / "Note:" paragraphs are left untouched.

Usage: python fix_script_paragraphs.py "<path to _script.docx>" [more paths...]
"""
import re
import sys
from docx import Document

SENTENCE_SPLIT = re.compile(r'(?<=[.!?])\s+(?=[A-Z0-9"\'])')


def is_note_or_blank(text: str) -> bool:
    t = text.strip()
    return t == "" or t.lower().startswith("note:")


def fix_docx(path: str) -> None:
    doc = Document(path)
    paras = doc.paragraphs
    if len(paras) < 2:
        print(f"{path}\n  skipped (only {len(paras)} paragraph)")
        return

    body_idx = []
    i = 1  # skip header paragraph 0
    while i < len(paras):
        text = "".join(r.text for r in paras[i].runs).strip()
        if is_note_or_blank(text):
            break
        body_idx.append(i)
        i += 1
    tail_idx = list(range(i, len(paras)))  # blank/Note paragraphs, left untouched

    if not body_idx:
        print(f"{path}\n  no body paragraphs found; left as-is")
        return

    full_text = re.sub(r"\s+", " ", " ".join(
        "".join(r.text for r in paras[j].runs).strip() for j in body_idx
    )).strip()
    sentences = [s.strip() for s in SENTENCE_SPLIT.split(full_text) if s.strip()]

    if sentences == ["".join(r.text for r in paras[j].runs).strip() for j in body_idx]:
        print(f"{path}\n  already one paragraph per sentence; left as-is")
        return

    # Write sentences into the first len(sentences) body paragraphs, drop the rest.
    for k, sentence in enumerate(sentences):
        p = paras[body_idx[k]] if k < len(body_idx) else None
        if p is None:
            # more sentences than original paragraphs (shouldn't normally happen) -
            # append after the last body paragraph
            last = paras[body_idx[-1]]
            new_p = last.insert_paragraph_before(sentence) if hasattr(last, "insert_paragraph_before") else None
            continue
        if p.runs:
            p.runs[0].text = sentence
            for r in p.runs[1:]:
                r.text = ""
    # remove any leftover body paragraphs beyond the number of sentences
    for j in body_idx[len(sentences):]:
        p = paras[j]
        p._element.getparent().remove(p._element)

    doc.save(path)
    print(f"{path}\n  body paragraphs: {len(body_idx)} -> {len(sentences)} (one per sentence)")


if __name__ == "__main__":
    for p in sys.argv[1:]:
        fix_docx(p)
