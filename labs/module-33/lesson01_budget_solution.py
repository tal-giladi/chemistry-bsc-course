"""Lesson 33.1 (reference solution): is the project possible in 180 hours?

Run from this folder:
    py lesson01_budget_solution.py
    py lesson01_budget_solution.py 30 25 10 1.3      (items, machine min/item, your min/item, rerun factor)
Reads example_hours_plan.csv (phase,planned_h) or your own plan file as a fifth argument.
Prints the plan, the time the data-collection phase really needs, and a verdict.
Machine time (a calculation running while you do something else) is not your time,
but it still needs calendar days; your own attended minutes per item are what eat the budget.
"""
import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOTAL = 180.0


def read_plan(path):
    with open(path, encoding="utf-8") as f:
        return [(r["phase"], float(r["planned_h"])) for r in csv.DictReader(f)]


def collection_hours(n_items, attended_min_per_item, rerun_factor):
    """Your own hours for the data phase: items x attended minutes x rerun factor, in hours."""
    return n_items * attended_min_per_item * rerun_factor / 60.0


def machine_days(n_items, machine_min_per_item, rerun_factor, hours_per_day=8.0):
    """Calendar days of computer time if the machine runs hours_per_day hours a day."""
    return n_items * machine_min_per_item * rerun_factor / 60.0 / hours_per_day


def verdict(plan, need_h, phase="data collection or runs"):
    """Compare the planned hours with the total and the data phase with what it needs."""
    total = sum(h for _, h in plan)
    planned = dict(plan).get(phase, 0.0)
    msgs = []
    if abs(total - TOTAL) > 0.5:
        msgs.append(f"plan adds up to {total:.0f} h, not {TOTAL:.0f} h")
    if need_h > planned:
        msgs.append(f"data phase needs {need_h:.1f} h but only {planned:.0f} h are planned")
    elif need_h > 0.8 * planned:
        msgs.append(f"data phase uses {need_h / planned:.0%} of its hours: little margin")
    return msgs or ["feasible: the plan adds up and the data phase fits with margin"]


def main(argv):
    n = int(argv[1]) if len(argv) > 1 else 30
    machine = float(argv[2]) if len(argv) > 2 else 25.0
    attended = float(argv[3]) if len(argv) > 3 else 10.0
    rerun = float(argv[4]) if len(argv) > 4 else 1.3
    plan = read_plan(argv[5] if len(argv) > 5 else HERE / "example_hours_plan.csv")
    for phase, h in plan:
        print(f"  {phase:<26}{h:6.0f} h  ({h / TOTAL:5.1%})")
    print(f"  {'total':<26}{sum(h for _, h in plan):6.0f} h")
    need = collection_hours(n, attended, rerun)
    days = machine_days(n, machine, rerun)
    print(f"{n} items, {attended:g} min of your time and {machine:g} min of machine time each, "
          f"rerun factor {rerun:g}:")
    print(f"  your hours for the data phase: {need:.1f} h")
    print(f"  machine time: {n * machine * rerun / 60:.1f} h = {days:.1f} days at 8 h a day")
    for m in verdict(plan, need):
        print("VERDICT:", m)


if __name__ == "__main__":
    main(sys.argv)
