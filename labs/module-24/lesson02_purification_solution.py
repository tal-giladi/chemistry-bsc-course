"""Lesson 24.2 - recrystallisation recovery and a distillation T-x-y diagram.

Reference solution for lesson02_purification.py.  Run:  py lesson02_purification_solution.py
Optional: copy alum_recrystallisation_template.csv to alum_recrystallisation.csv and enter your home runs.
Writes runs/lesson02_purification.png.
"""
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq

from org24 import HERE, antoine_bar, read_csv, runs_dir

P_ATM = 1.01325   # bar

# Acetanilide in water (PubChem CID 904): 1 g dissolves in 185 mL cold water and in 20 mL boiling water
S_COLD = 1 / 185   # g/mL near 25 C
S_HOT = 1 / 20     # g/mL near 100 C


def min_hot_volume(mass_g, s_hot):
    """Smallest volume (mL) of hot solvent that dissolves mass_g."""
    # TODO: return mass_g / s_hot
    return mass_g / s_hot


def max_recovery(mass_g, volume_mL, s_cold):
    """Largest fraction of the compound that can crystallise on cooling (the rest stays dissolved)."""
    # TODO: lost = volume_mL * s_cold; return max(0, (mass_g - lost) / mass_g)
    lost = volume_mL * s_cold
    return max(0.0, (mass_g - lost) / mass_g)


def bubble_point(x1, a="cyclohexane", b="toluene", P=P_ATM):
    """Ideal (Raoult) solution: temperature T (K) where x1 Pa(T) + (1 - x1) Pb(T) = P,
    and the vapour mole fraction y1 = x1 Pa(T) / P. Returns (T, y1)."""
    # TODO: solve f(T) = x1*antoine_bar(a, T) + (1-x1)*antoine_bar(b, T) - P = 0 with brentq on [300, 420]
    f = lambda T: x1 * antoine_bar(a, T) + (1 - x1) * antoine_bar(b, T) - P
    T = brentq(f, 300.0, 420.0)
    return T, x1 * antoine_bar(a, T) / P


def fenske_plates(xD, xB, alpha):
    """Minimum number of equilibrium stages (total reflux) to go from bottoms xB to distillate xD."""
    # TODO: return ln[(xD/(1-xD)) * ((1-xB)/xB)] / ln(alpha)
    return math.log((xD / (1 - xD)) * ((1 - xB) / xB)) / math.log(alpha)


def home_runs():
    p = HERE / "alum_recrystallisation.csv"
    if not p.exists():
        print("(no alum_recrystallisation.csv yet - copy the template and enter your runs to analyse them)")
        return
    for r in read_csv(p.name):
        dissolved, water, got = float(r["alum_dissolved_g"]), float(r["water_mL"]), float(r["crystals_dry_g"])
        expected = max_recovery(dissolved, water, 1 / 20)   # about 1 g per 20 mL cold water (PubChem)
        print(f"run {r['run']}: recovered {got:.1f} g of {dissolved:.1f} g = {100 * got / dissolved:.0f} %; "
              f"solubility limit {100 * expected:.0f} %")


def main():
    if min_hot_volume(1, 1) is None or max_recovery(1, 1, 0.1) is None or bubble_point(0.5) is None \
            or fenske_plates(0.9, 0.1, 2) is None:
        print("TODO: write min_hot_volume(), max_recovery(), bubble_point() and fenske_plates() first.")
        return

    crude = 2.00
    V = min_hot_volume(crude, S_HOT)
    print(f"acetanilide: {crude:.2f} g needs at least {V:.0f} mL of boiling water")
    for vol in (V, 1.1 * V, 2 * V):
        print(f"  {vol:5.0f} mL -> at most {100 * max_recovery(crude, vol, S_COLD):.0f} % recovered on cooling to 25 C")

    T, y = bubble_point(0.5)
    print(f"50:50 cyclohexane/toluene boils at {T - 273.15:.1f} C; first vapour is {100 * y:.0f} % cyclohexane")
    T1, y1 = bubble_point(y)
    print(f"condense it and re-boil: {T1 - 273.15:.1f} C, vapour {100 * y1:.0f} % cyclohexane")
    xs = np.linspace(0.001, 0.999, 120)
    pts = [bubble_point(x) for x in xs]
    alpha = np.mean([antoine_bar("cyclohexane", t) / antoine_bar("toluene", t) for t, _ in pts])
    print(f"mean relative volatility alpha = {alpha:.2f}")
    print(f"minimum stages for 95 % cyclohexane distillate from a 50 % pot: {fenske_plates(0.95, 0.5, alpha):.1f}")
    home_runs()

    fig, ax = plt.subplots(figsize=(6, 4.5))
    ax.plot(xs, [t - 273.15 for t, _ in pts], label="liquid (bubble point)")
    ax.plot([p[1] for p in pts], [t - 273.15 for t, _ in pts], label="vapour (dew point)")
    x = 0.5
    for _ in range(3):   # stair steps: one equilibrium stage each
        t, yy = bubble_point(x)
        ax.plot([x, yy], [t - 273.15] * 2, "k:", lw=1)
        x = yy
        ax.plot([x, x], [t - 273.15, bubble_point(x)[0] - 273.15], "k:", lw=1)
    ax.set_xlabel("mole fraction cyclohexane")
    ax.set_ylabel("temperature / C at 1 atm")
    ax.set_title("Ideal cyclohexane-toluene (Raoult + NIST Antoine)")
    ax.legend()
    fig.tight_layout()
    out = runs_dir() / "lesson02_purification.png"
    fig.savefig(out, dpi=120)
    print("plot:", out)


if __name__ == "__main__":
    main()
