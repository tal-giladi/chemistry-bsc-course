"""Lesson 19.3: liquid-liquid extraction (one big or several small portions, and pH) and a
van Deemter fit for a packed GC column.

Fill in the two TODOs, then run (from this folder):
    py lesson03_extraction_vandeemter.py
    py lesson03_extraction_vandeemter.py my_vandeemter.csv     # your data, same columns
Reference solution: lesson03_extraction_vandeemter_solution.py
Data: vandeemter_gc.csv (simulated; columns u_cm_per_s,H_mm).
"""
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

from ana19 import HERE, read_csv, save

COLUMN_LENGTH_MM = 2000.0   # the packed column of vandeemter_gc.csv is 2 m long


def fraction_left(D, V_aq, V_org, n):
    """Fraction of solute still in the water after n extractions with V_org each (Harvey 7.7)."""
    # TODO 1: one extraction leaves V_aq / (D V_org + V_aq) of the solute behind; n extractions
    # leave that fraction to the power n.
    return None


def D_weak_acid(K_D, Ka, pH):
    """Distribution ratio of a weak acid HA: only the neutral form enters the organic phase."""
    h = 10.0 ** (-pH)
    return K_D * h / (h + Ka)


def van_deemter(u, A, B, C):
    return A + B / u + C * u


def fit_van_deemter(u, H):
    """Fit H = A + B/u + C u. Returns A, B, C, their standard errors, u_opt and H_min."""
    # TODO 2: p, cov = curve_fit(van_deemter, u, H, p0=[0.5, 5.0, 0.05]); the standard errors are
    # np.sqrt(np.diag(cov)); then u_opt = sqrt(B/C) and H_min = A + 2 sqrt(B C).
    p, cov = None, None
    u_opt, H_min = None, None
    return p, cov, u_opt, H_min


def main():
    print("Extraction, 100 mL water, D = 4.0:")
    for V_org, n in ((30, 1), (15, 2), (10, 3), (5, 6)):
        q = fraction_left(4.0, 100, V_org, n)
        print(f"   {n} x {V_org:2d} mL: {100 * q:5.1f} % left, {100 * (1 - q):5.1f} % extracted")
    print("Benzoic acid (pKa 4.20, K_D = 50 assumed), 50 mL water + 50 mL organic, one extraction:")
    for pH in (2.0, 4.2, 6.0, 8.0):
        D = D_weak_acid(50.0, 10 ** -4.20, pH)
        print(f"   pH {pH:.1f}: D = {D:7.3f}, extracted {100 * (1 - fraction_left(D, 50, 50, 1)):5.1f} %")

    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "vandeemter_gc.csv"
    d = read_csv(path)
    u, H = d["u_cm_per_s"], d["H_mm"]
    (A, B, C), (sA, sB, sC), u_opt, H_min = fit_van_deemter(u, H)
    print("van Deemter fit, H in mm and u in cm/s:")
    print(f"   A = {A:.3f} +/- {sA:.3f} mm,  B = {B:.2f} +/- {sB:.2f} mm cm/s,  C = {C:.4f} +/- {sC:.4f} mm s/cm")
    print(f"   u_opt = sqrt(B/C) = {u_opt:.1f} cm/s,  H_min = A + 2 sqrt(BC) = {H_min:.2f} mm")
    print(f"   plates at the optimum for a {COLUMN_LENGTH_MM / 1000:.0f} m column: N = L/H = {COLUMN_LENGTH_MM / H_min:.0f}")
    print(f"   at 2 u_opt: H = {van_deemter(2 * u_opt, A, B, C):.2f} mm (run twice as fast, lose {100 * (1 - H_min / van_deemter(2 * u_opt, A, B, C)):.0f} % of the plates)")

    fig, ax = plt.subplots(figsize=(6, 4))
    uu = np.linspace(u.min(), u.max(), 200)
    ax.plot(u, H, "o", label="measured")
    ax.plot(uu, van_deemter(uu, A, B, C), "-", label="fit")
    ax.plot(uu, np.full_like(uu, A), ":", label="A (multiple paths)")
    ax.plot(uu, B / uu, ":", label="B/u (longitudinal diffusion)")
    ax.plot(uu, C * uu, ":", label="Cu (mass transfer)")
    ax.axvline(u_opt, color="grey", lw=0.8)
    ax.set(xlabel="u (cm/s)", ylabel="H (mm)", title="van Deemter plot", ylim=(0, max(H) * 1.1))
    ax.legend(fontsize=8)
    save(fig, "lesson03_vandeemter.png")


if __name__ == "__main__":
    main()
