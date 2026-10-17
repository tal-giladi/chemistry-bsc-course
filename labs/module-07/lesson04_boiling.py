"""Lesson 07.4: boiling points of main-group hydrides.

Fill in the function marked TODO, then run (from this folder):
    py lesson04_boiling.py        # prints the analysis, saves runs/hydrides.png
Reference solution: lesson04_boiling_solution.py
"""
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent


def load(path=HERE / "hydride_boiling_points.csv"):
    """Return a list of dicts: formula, group, period, bp_C."""
    lines = [r for r in path.read_text(encoding="utf-8").splitlines() if r and not r.startswith("#")]
    keys = lines[0].split(",")
    rows = [dict(zip(keys, r.split(","))) for r in lines[1:]]
    for r in rows:
        r["group"], r["period"], r["bp_C"] = int(r["group"]), int(r["period"]), float(r["bp_C"])
    return rows


def extrapolate_period2(rows, group):
    """Straight line through the period 3 and 4 points of a group, evaluated at period 2.
    This is the boiling point the period-2 hydride 'should' have with dispersion and dipoles only."""
    pts = sorted((r["period"], r["bp_C"]) for r in rows if r["group"] == group and r["period"] in (3, 4))
    # pts is [(3, bp3), (4, bp4)].
    # TODO: slope = change in bp per period; go back one period from period 3 to period 2.
    return None


def main():
    rows = load()
    if extrapolate_period2(rows, 14) is None:
        print("TODO: write extrapolate_period2() first.")
        return
    print(f"{'group':>5} {'period-2 hydride':>17} {'measured':>9} {'trend':>8} {'anomaly':>8}  (degC)")
    for g in (14, 15, 16, 17):
        r2 = next(r for r in rows if r["group"] == g and r["period"] == 2)
        guess = extrapolate_period2(rows, g)
        print(f"{g:>5} {r2['formula']:>17} {r2['bp_C']:>9.1f} {guess:>8.1f} {r2['bp_C'] - guess:>8.1f}")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return
    out = HERE / "runs"
    out.mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(6, 4))
    for g, mk in zip((14, 15, 16, 17), "osD^"):
        pts = sorted((r["period"], r["bp_C"], r["formula"]) for r in rows if r["group"] == g)
        p = np.array([x[0] for x in pts]); b = np.array([x[1] for x in pts])
        ax.plot(p, b, marker=mk, label=f"group {g}")
        for x, y, f in pts:
            ax.annotate(f, (x, y), textcoords="offset points", xytext=(4, 4), fontsize=7)
    ax.set_xlabel("period of the central atom")
    ax.set_ylabel("normal boiling point / °C")
    ax.set_xticks([2, 3, 4, 5])
    ax.legend()
    fig.tight_layout()
    fig.savefig(out / "hydrides.png", dpi=120)
    print(f"\nPlot saved to {out / 'hydrides.png'}")


if __name__ == "__main__":
    main()
