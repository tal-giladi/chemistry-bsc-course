"""Lesson 10.1 exercise: indicator choice, titration error and the size of one drop.
Fill in the TODO functions. Reference solution: lesson01_indicator_solution.py

Run:   py lesson01_indicator.py
       py lesson01_indicator.py my_drops.csv   (columns trial,n_drops,m_before_g,m_after_g)
The titration curve is computed from the charge balance in its 'inverse' form: for a chosen pH,
the volume of base that gives that pH has a closed formula, so no root finder is needed.
"""
import csv
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
KW = 1.0e-14
KA_ACETIC = 10 ** -4.757          # Harvey, Analytical Chemistry 2.1, App. 16.11
# Indicator transition pH taken as the indicator pKa (Harvey Table 9.2.3)
INDICATORS = {"methyl orange": 3.7, "methyl red": 5.0, "bromothymol blue": 7.1,
              "phenol red": 7.8, "phenolphthalein": 9.6}
C_ACID, V_ACID, C_BASE = 0.1000, 25.00, 0.1000      # mol/L, mL, mol/L
TITRANT_DENSITY = 1.03            # g/mL, 5 % w/w NaHCO3 solution (approximate)


def volume_at_ph(ph, c_a, v_a, c_b, ka=None):
    """Volume of strong base (mL) at which the titrand reaches this pH.
    Charge balance: [H+] + [Na+] = [OH-] + [A-]. ka=None means a strong acid."""
    # TODO: h = 10**-pH, delta = h - KW/h, alpha = Ka/(Ka + h) (1 for a strong acid); return v_a (c_a alpha - delta) / (c_b + delta).
    return None


def titration_error_percent(v_end, v_eq):
    """Relative titration error of an end point, in percent (negative = stopped too early)."""
    # TODO: one line, 100 (v_end - v_eq) / v_eq.
    return None


def read_drops(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return [{k: float(v) for k, v in row.items()} for row in csv.DictReader(fh)]


def main():
    if volume_at_ph(7.0, 0.1, 25.0, 0.1) is None or titration_error_percent(1.0, 1.0) is None:
        print("TODO: write volume_at_ph() and titration_error_percent() first.")
        return
    v_eq = C_ACID * V_ACID / C_BASE
    print(f"25.00 mL of 0.1000 M acid with 0.1000 M NaOH: V_eq = {v_eq:.2f} mL")
    print(f"{'indicator':18s} {'pH':>4s} {'HCl: V/mL':>10s} {'error %':>8s} {'acetic: V/mL':>13s} {'error %':>8s}")
    for name, ph in INDICATORS.items():
        v_s = volume_at_ph(ph, C_ACID, V_ACID, C_BASE)
        v_w = volume_at_ph(ph, C_ACID, V_ACID, C_BASE, KA_ACETIC)
        print(f"{name:18s} {ph:4.1f} {v_s:10.3f} {titration_error_percent(v_s, v_eq):8.2f} "
              f"{v_w:13.3f} {titration_error_percent(v_w, v_eq):8.2f}")

    ph = np.linspace(1.0, 12.5, 1000)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for label, ka in (("HCl", None), ("acetic acid", KA_ACETIC)):
        v = volume_at_ph(ph, C_ACID, V_ACID, C_BASE, ka)
        ok = (v >= 0) & (v <= 40)
        ax.plot(v[ok], ph[ok], label=label)
    for name, p in INDICATORS.items():
        ax.axhspan(p - 1, p + 1, alpha=0.06)
        ax.text(39.5, p, name, ha="right", va="center", fontsize=8)
    ax.set_xlabel("NaOH added / mL")
    ax.set_ylabel("pH")
    ax.set_xlim(0, 40)
    ax.legend(loc="upper left")
    out = HERE / "runs"
    out.mkdir(exist_ok=True)
    fig.savefig(out / "lesson01_indicators.png", dpi=120, bbox_inches="tight")
    print(f"plot: {out / 'lesson01_indicators.png'}")

    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "drop_calibration_example.csv"
    per_drop = [(r["m_before_g"] - r["m_after_g"]) / r["n_drops"] for r in read_drops(path)]
    mean = sum(per_drop) / len(per_drop)
    sd = math.sqrt(sum((x - mean) ** 2 for x in per_drop) / (len(per_drop) - 1))
    print(f"drop mass {mean * 1000:.1f} mg (SD of trial means {sd * 1000:.1f} mg, n = {len(per_drop)}); "
          f"volume about {mean / TITRANT_DENSITY:.3f} mL")
    print(f"one drop is {100 * mean / 7.0:.2f} % of a 7 g titration")


if __name__ == "__main__":
    main()
