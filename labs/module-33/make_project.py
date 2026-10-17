"""Creates an empty research-project folder with the layout of Lesson 33.2.

Run from this folder:
    py make_project.py ../../../my-ir-benchmark          (any new, empty folder outside the course repo)
    py make_project.py runs/demo-project --demo           (a filled-in demo used by lesson04_package_check.py)
The layout follows Wilson et al. (2017), "Good enough practices in scientific computing":
  README.md          what the project is, how to rerun it, licence, contact
  hours_log.csv      date,phase,hours,note  - one row per working session
  requirements.txt   pinned versions (name==version) of every package you use
  data/raw/          original data, never edited by hand (make it read-only)
  data/processed/    files your code writes from data/raw
  data/README.md     the data dictionary: every file, every column, unit, source, licence
  src/               your code; run_all.py reruns everything from data/raw to results
  results/           figures and tables, written only by code
  notebook/          dated notebook pages (templates/notebook-page.md)
  doc/               proposal.md, report.md, poster (PDF or PNG), reader-feedback.md
It refuses to write into a folder that already has files in it.
"""
import sys
from pathlib import Path

PHASES = ["reading", "setup and pilot", "data collection or runs", "analysis", "report", "poster",
          "feedback and revision"]

README = """# {name}

One sentence: the question this project answers.

## How to rerun

1. Create an environment with Python 3.14 and `pip install -r requirements.txt`.
2. Put the raw data in data/raw (see data/README.md for where each file comes from).
3. Run `python src/run_all.py`. Every figure and table in results/ is rebuilt.

## Licence and contact

Code: MIT. Text and figures: CC BY 4.0. Data: see data/README.md (each source keeps its own licence).
Author and contact: your name, e-mail, ORCID iD.
"""

DATA_README = """# Data dictionary

| file | source and licence | date downloaded | columns (unit) | changes made |
|---|---|---|---|---|
| raw/example.csv | where it came from, its licence | YYYY-MM-DD | name (unit), ... | none |
"""

REPORT = """# Title that states the result

## Abstract
## Introduction
## Methods
## Results
## Discussion and limitations
## Conclusion
## References
"""

RUN_ALL = '''"""Rebuilds everything in results/ from data/raw. Keep this the only entry point."""
print("TODO: call your analysis steps here, in order.")
'''


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def make(root, demo=False):
    root = Path(root)
    if root.exists() and any(root.iterdir()):
        sys.exit(f"{root} is not empty; choose a new folder.")
    name = root.name
    write(root / "README.md", README.format(name=name))
    write(root / "requirements.txt", "numpy==2.5.4\nscipy==1.18.1\nmatplotlib==3.11.2\n")
    write(root / "hours_log.csv", "date,phase,hours,note\n")
    write(root / "data" / "README.md", DATA_README)
    for d in ("data/raw", "data/processed", "results", "notebook", "doc"):
        (root / d).mkdir(parents=True, exist_ok=True)
    write(root / "src" / "run_all.py", RUN_ALL)
    write(root / "doc" / "proposal.md", "# Proposal\n\nCopy templates/research-proposal.md here.\n")
    write(root / "doc" / "report.md", REPORT)
    if demo:
        rows = ["date,phase,hours,note"]
        plan = [25, 20, 50, 35, 30, 10, 10]
        day = 1
        for phase, h in zip(PHASES, plan):
            while h > 0:
                step = min(5, h)
                rows.append(f"2027-{1 + day // 28:02d}-{1 + day % 28:02d},{phase},{step},demo session")
                h -= step
                day += 1
        write(root / "hours_log.csv", "\n".join(rows) + "\n")
        write(root / "data" / "raw" / "example.csv", "x,y\n1,2\n2,4\n")
        write(root / "results" / "figure1.png.txt", "placeholder for a figure written by src/run_all.py\n")
        write(root / "doc" / "poster.pdf.txt", "placeholder for the poster PDF\n")
        write(root / "doc" / "reader-feedback.md", "# Feedback\n\nReader, date, comments, what I changed.\n")
    print(f"created {root}{' (demo)' if demo else ''}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    make(sys.argv[1], demo="--demo" in sys.argv)
