"""Lesson 33.4 (reference solution): is the project package ready for a reader?

Run from this folder:
    py make_project.py runs/demo-project --demo      (once, to have something to check)
    py lesson04_package_check_solution.py runs/demo-project
    py lesson04_package_check_solution.py ../../../my-ir-benchmark
Checks the layout of Lesson 33.2 and the minimum a reader needs:
  - README.md, requirements.txt, data/README.md, src/run_all.py, doc/report.md exist;
  - every requirement is pinned (name==version);
  - data/raw has at least one file and data/README.md names a licence or source for it;
  - doc/report.md has the sections Abstract, Methods, Results, Discussion and limitations, References;
  - a poster file (pdf, png or svg) and a feedback note are in doc/;
  - hours_log.csv adds up to at least 180 h, with every phase present.
Prints PASS or FAIL per check; exit code 1 if anything fails.
"""
import csv
import re
import sys
from pathlib import Path

PHASES = ["reading", "setup and pilot", "data collection or runs", "analysis", "report", "poster",
          "feedback and revision"]
REPORT_SECTIONS = ["Abstract", "Methods", "Results", "Discussion and limitations", "References"]


def check_hours(path, target=180.0):
    """Return (ok, message): total hours >= target and every phase in PHASES logged at least once."""
    with open(path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    total = sum(float(r["hours"]) for r in rows)
    by_phase = {}
    for r in rows:
        by_phase[r["phase"]] = by_phase.get(r["phase"], 0.0) + float(r["hours"])
    missing = [p for p in PHASES if p not in by_phase]
    ok = total >= target and not missing
    msg = f"{total:.0f} h logged" + (f"; phases never logged: {', '.join(missing)}" if missing else "")
    return ok, msg


def check_pinned(path):
    """Return (ok, message): every non-empty, non-comment line of requirements.txt is name==version."""
    lines = [x.strip() for x in Path(path).read_text(encoding="utf-8").splitlines()]
    bad = [x for x in lines if x and not x.startswith("#") and not re.fullmatch(r"[A-Za-z0-9_.\-\[\]]+==[\w.]+", x)]
    return not bad, ("all pinned" if not bad else f"not pinned: {', '.join(bad)}")


def run(root):
    root = Path(root)
    results = []
    for rel in ["README.md", "requirements.txt", "data/README.md", "src/run_all.py", "doc/report.md"]:
        results.append(((root / rel).exists(), f"{rel} exists"))
    if (root / "requirements.txt").exists():
        ok, msg = check_pinned(root / "requirements.txt")
        results.append((ok, f"requirements: {msg}"))
    raw = [p for p in (root / "data" / "raw").glob("*") if p.is_file()] if (root / "data" / "raw").exists() else []
    results.append((bool(raw), f"data/raw has {len(raw)} file(s)"))
    if (root / "data" / "README.md").exists():
        text = (root / "data" / "README.md").read_text(encoding="utf-8").lower()
        results.append(("licen" in text and "source" in text, "data/README.md names source and licence"))
    if (root / "doc" / "report.md").exists():
        heads = re.findall(r"^## (.+)$", (root / "doc" / "report.md").read_text(encoding="utf-8"), re.M)
        miss = [s for s in REPORT_SECTIONS if s not in heads]
        results.append((not miss, "report sections" + (f" missing: {', '.join(miss)}" if miss else " complete")))
    posters = [p for p in (root / "doc").glob("poster*") if re.search(r"\.(pdf|png|svg)", p.name)] if (root / "doc").exists() else []
    results.append((bool(posters), "poster file in doc/"))
    results.append(((root / "doc" / "reader-feedback.md").exists(), "doc/reader-feedback.md exists"))
    if (root / "hours_log.csv").exists():
        ok, msg = check_hours(root / "hours_log.csv")
        results.append((ok, f"hours: {msg}"))
    else:
        results.append((False, "hours_log.csv exists"))
    for ok, msg in results:
        print(("PASS " if ok else "FAIL ") + msg)
    n_fail = sum(not ok for ok, _ in results)
    print(f"{len(results) - n_fail} passed, {n_fail} failed")
    return n_fail


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    sys.exit(1 if run(sys.argv[1]) else 0)
