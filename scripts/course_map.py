"""Regenerate COURSE-MAP.md from the manifest: `py scripts/course_map.py`."""
from pathlib import Path
from manifest import MODULES, STAGES, lessons

TECHNION = ["—", "01040003, 01040004", "01040019, 01040131", "01140077, 01140052", "02340128",
            "01340127", "01240117", "01240118", "01240220", "01240212", "03240033", "01240408",
            "01240415", "01240611", "01240708", "01240711", "part of 01240708 / 01240711", "01240305",
            "01240213", "01240417", "01240413", "01240414", "01240610", "01240911 (+ 01240912)",
            "01240214", "01240210", "01240416", "01240703", "01340019", "01240613", "01260603",
            "01270453, 01270427", "01240353"]

root = Path(__file__).resolve().parent.parent
n = len(list(lessons()))
out = ["# Course map", "",
       f"{len(MODULES)} modules in 3 years, {n} lessons. Each module depends only on earlier ones. "
       "The Technion column gives the matching course number in the 2025/2026 catalog of the Technion "
       "B.Sc. in Chemistry (see [the plan](plan.md)).", "",
       "| Year | # | Module | Technion course | Lessons |", "|---|---|---|---|---|"]
for m, (title, ls) in enumerate(MODULES, 1):
    year = STAGES.get(m, "").split(" — ")[0]
    out.append(f"| {year} | {m} | [{title}](lessons/module-{m:02d}/lesson-01.md) | {TECHNION[m-1]} | {len(ls)} |")
out += ["", "## Fast route (about 18 months)", "",
        "If you only want to understand chemistry, not cover the whole degree: Modules 1, 7, 8, 9, 10, 13, 15, 16, 17, 19, 20, 22, 23, 24 and 25.", "",
        "## Pace", "",
        "At 10–12 hours a week the full course takes about 5.5–6 years; at 18–20 hours about 3.5–4 years. "
        "If you already know the maths and physics, skip Modules 2–4 after passing their module quizzes.", ""]
(root / "COURSE-MAP.md").write_text("\n".join(out), encoding="utf-8", newline="\n")
print("ok")
