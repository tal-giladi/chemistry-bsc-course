"""Lesson 24.3 - Rf values from your paper chromatogram and the melting-point depression of an impure solid.

Fill in the functions marked TODO, then run:  py lesson03_purity.py
Reference solution: lesson03_purity_solution.py
Uses chromatogram.csv if you made one (copy chromatogram_template.csv), else the template's example rows.
Writes runs/lesson03_purity.png.
"""
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from org24 import BENZOIC_DFUS_H, BENZOIC_TFUS_K, HERE, R, read_csv, runs_dir


def rf(spot_mm, front_mm):
    """Retention factor: distance moved by the spot centre / distance moved by the solvent front,
    both measured from the pencil start line."""
    # TODO: return spot_mm / front_mm
    return None


def ideal_melting_point(x_main, Tm=BENZOIC_TFUS_K, dH=BENZOIC_DFUS_H):
    """Temperature (K) at which the last crystal of the main compound melts when its mole fraction in
    the liquid is x_main (ideal solution, impurity insoluble in the solid):
        ln x_main = -(dH/R) (1/T - 1/Tm)   ->   1/T = 1/Tm - R ln(x_main) / dH"""
    # TODO: return 1 / (1/Tm - R * ln(x_main) / dH)
    return None


def depression_estimate(x_impurity, Tm=BENZOIC_TFUS_K, dH=BENZOIC_DFUS_H):
    """Small-x approximation: dT = R Tm^2 x_impurity / dH (the same form as freezing-point depression)."""
    # TODO: return R * Tm**2 * x_impurity / dH
    return None


def main():
    if rf(1, 2) is None or ideal_melting_point(0.9) is None or depression_estimate(0.01) is None:
        print("TODO: write rf(), ideal_melting_point() and depression_estimate() first.")
        return

    name = "chromatogram.csv" if (HERE / "chromatogram.csv").exists() else "chromatogram_template.csv"
    print(f"Rf values from {name}:")
    rows = read_csv(name)
    for r in rows:
        print(f"  {r['sample']:22s} spot {r['spot']:10s} Rf = {rf(float(r['spot_mm']), float(r['front_mm'])):.2f}")

    print("benzoic acid (Tm = 122.4 C, dfusH = 18.0 kJ/mol, NIST):")
    for xi in (0.01, 0.02, 0.05, 0.10):
        T = ideal_melting_point(1 - xi)
        print(f"  {100 * xi:4.0f} mol% impurity: last crystal melts at {T - 273.15:6.1f} C "
              f"(depression {BENZOIC_TFUS_K - T:.1f} K; small-x estimate {depression_estimate(xi):.1f} K)")

    x = np.linspace(0.0, 0.3, 61)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 4))
    a1.plot(100 * x, [ideal_melting_point(1 - xi) - 273.15 for xi in x])
    a1.set_xlabel("impurity / mol %")
    a1.set_ylabel("end of melting / C")
    a1.set_title("Benzoic acid, ideal liquid")
    for i, r in enumerate(rows):
        val = rf(float(r["spot_mm"]), float(r["front_mm"]))
        a2.plot([i], [val], "o")
        a2.annotate(f"{r['sample']} {r['spot']}", (i, val), fontsize=7, rotation=30)
    a2.set_ylim(0, 1)
    a2.set_ylabel("Rf")
    a2.set_xticks([])
    a2.set_title("Your chromatogram")
    fig.tight_layout()
    out = runs_dir() / "lesson03_purity.png"
    fig.savefig(out, dpi=120)
    print("plot:", out)


if __name__ == "__main__":
    main()
