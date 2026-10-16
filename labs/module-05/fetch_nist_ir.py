"""Lesson 05.4: download one IR spectrum (JCAMP-DX) from the NIST Chemistry WebBook.

NIST spectra are not stored in this repo: the WebBook data compilation is copyright the U.S.
Secretary of Commerce ("all rights reserved"), so each learner downloads a copy for personal study
and cites it. The file goes to data/downloaded/ (ignored by git).

Usage (from this folder):
    py fetch_nist_ir.py                     # ethanol, gas phase (NIST ID C64175)
    py fetch_nist_ir.py C67641 acetone      # any WebBook ID with an IR spectrum, and a file name
    py fetch_nist_ir.py --dry-run           # show the URL and target file, download nothing
Then:
    py lesson04_reading.py data/downloaded/ethanol_ir.jdx

Find the ID on the compound's WebBook page: it is the ID=... part of the page address
(C followed by the CAS number without dashes, e.g. ethanol 64-17-5 -> C64175).
"""
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
URL = "https://webbook.nist.gov/cgi/cbook.cgi?JCAMP={id}&Index=0&Type=IR"


def main():
    args = [a for a in sys.argv[1:] if a != "--dry-run"]
    nist_id = args[0] if args else "C64175"
    name = args[1] if len(args) > 1 else ("ethanol" if nist_id == "C64175" else nist_id)
    url = URL.format(id=nist_id)
    out = HERE / "data" / "downloaded" / f"{name}_ir.jdx"
    print(f"source: {url}\ntarget: {out.relative_to(HERE).as_posix()}")
    if "--dry-run" in sys.argv:
        return 0
    with urllib.request.urlopen(url, timeout=30) as response:
        text = response.read().decode("utf-8", errors="replace")
    if not text.startswith("##TITLE"):
        print("No JCAMP-DX file came back. Check the ID on the WebBook page (does it list an IR "
              "spectrum?) and try again.")
        return 1
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8", newline="\n")
    print(f"saved {len(text)} characters. Cite it as: NIST Chemistry WebBook, NIST Standard "
          f"Reference Database 69, IR spectrum of {name} ({nist_id}), accessed <today's date>.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
