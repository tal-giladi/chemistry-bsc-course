"""Writes the GENERATED demo data for Module 33 (seeded, so the numbers are always the same).

Run from this folder:
    py make_data.py
Writes:
  example_parity.csv   columns molecule,mode,nu_exp_cm1,nu_calc_cm1
                       90 vibrational modes of 30 imaginary molecules. "Experimental" values are drawn
                       between 500 and 3800 cm-1; "calculated" values are 4.0 % too high (a typical
                       harmonic overestimate) plus 15 cm-1 random scatter. Generated, NOT real data:
                       use it only to practise the poster figure (Lesson 33.3).
  example_hours_plan.csv  columns phase,planned_h (the 180-hour split used in Lesson 33.1).
"""
import csv
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent

PLAN = [("reading", 25), ("setup and pilot", 20), ("data collection or runs", 50),
        ("analysis", 35), ("report", 30), ("poster", 10), ("feedback and revision", 10)]


def main():
    rng = np.random.default_rng(33)
    rows = []
    for m in range(1, 31):
        for k in range(1, 4):
            nu_exp = float(rng.uniform(500, 3800))
            nu_calc = 1.040 * nu_exp + float(rng.normal(0, 15))
            rows.append((f"M{m:02d}", k, round(nu_exp, 1), round(nu_calc, 1)))
    with open(HERE / "example_parity.csv", "w", newline="\n", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["molecule", "mode", "nu_exp_cm1", "nu_calc_cm1"])
        w.writerows(rows)
    with open(HERE / "example_hours_plan.csv", "w", newline="\n", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["phase", "planned_h"])
        w.writerows(PLAN)
    print(f"wrote example_parity.csv ({len(rows)} modes) and example_hours_plan.csv "
          f"({sum(h for _, h in PLAN)} h)")


if __name__ == "__main__":
    main()
