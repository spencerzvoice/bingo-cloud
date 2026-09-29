"""Clean up stray whitespace in a _script.docx (collapsed multi-space runs from caption
scraping, space before punctuation, etc.) without touching the actual words.

Usage: python fix_script_spacing.py "<path to _script.docx>" [more paths...]
Prints a before/after character-count diff per file so the fix is auditable without
dumping the script text itself.
"""
import re
import sys
from docx import Document


def clean(text: str) -> str:
    text = text.replace(" ", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\s+([.,!?;:])", r"\1", text)
    text = re.sub(r"([.,!?;:])(?=[A-Za-z])", r"\1 ", text)
    text = text.strip()
    return text


def fix_docx(path: str) -> None:
    doc = Document(path)
    before = 0
    after = 0
    changed = 0
    for para in doc.paragraphs:
        if not para.runs:
            continue
        original = "".join(r.text for r in para.runs)
        before += len(original)
        cleaned = clean(original)
        after += len(cleaned)
        if cleaned != original:
            changed += 1
            para.runs[0].text = cleaned
            for r in para.runs[1:]:
                r.text = ""
    doc.save(path)
    print(f"{path}\n  paragraphs changed: {changed}\n  chars: {before} -> {after}")


if __name__ == "__main__":
    for p in sys.argv[1:]:
        fix_docx(p)
