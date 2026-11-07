"""File a finished invoice PDF where Spencer keeps them (Spencer, 2026-11-07: "Make this the default").

Desktop only (Windows). Copies the PDF to:
  1. F:\\Invoices\\<Client>\\            (client folder created if missing)
  2. %USERPROFILE%\\Desktop\\<YYYY> Invoices\\   (invoice only, no client subfolder)
YYYY comes from the invoice date at the end of the file name (NN_Client_Job_MM-DD-YYYY.pdf).

Usage: python scripts/file_invoice.py <invoice.pdf> "<Client folder name>"
  e.g. python scripts/file_invoice.py "45_Highlanders_Creative_US_Army_Gala_VO_11-07-2026.pdf" "Highlanders Creative"
Never overwrites: stops if a file with the same name is already there.
"""
import os
import re
import shutil
import sys
from pathlib import Path


def main(pdf, client):
    pdf = Path(pdf)
    m = re.search(r"_(\d{2})-(\d{2})-(\d{4})\.pdf$", pdf.name)
    if not m:
        sys.exit(f"File name doesn't end in _MM-DD-YYYY.pdf: {pdf.name}")
    year = m.group(3)
    targets = [
        Path("F:/Invoices") / client,
        Path(os.environ.get("USERPROFILE", str(Path.home()))) / "Desktop" / f"{year} Invoices",
    ]
    for d in targets:
        d.mkdir(parents=True, exist_ok=True)
        dest = d / pdf.name
        if dest.exists():
            print("already there, left alone:", dest)
            continue
        shutil.copy2(pdf, dest)
        print("filed:", dest)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
