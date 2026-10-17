"""Lesson 26.3 - the Hill plot of the standard human blood O2 dissociation curve.

Reference solution. Run:  py lesson03_hill_solution.py
Optional: py lesson03_hill.py 97    (your own pulse-oximeter reading in %, see the lesson)
Writes runs/lesson03_hill.png.
"""
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from bio26 import BOHR_LOG10, P50_MB, hb_standard_curve, runs_dir


def hill(p, p50, n):
    """Fractional saturation from the Hill equation: S = p^n / (p50^n + p^n)."""
    return p ** n / (p50 ** n + p ** n)


def hill_plot(p, s):
    """Hill-plot coordinates: x = log10(p), y = log10(S / (1 - S))."""
    return np.log10(p), np.log10(s / (1 - s))


def hill_line(p, s, lo=0.2, hi=0.8):
    """Straight-line fit of the Hill plot between saturations lo and hi. Returns n (slope) and P50."""
    m = (s > lo) & (s < hi)
    x, y = hill_plot(p[m], s[m])
    n, c = np.polyfit(x, y, 1)
    return n, 10 ** (-c / n)


def p50_at_ph(p50, pH):
    """P50 after a pH change, using the Bohr coefficient d log10(P50)/d pH = BOHR_LOG10 (-0.48)."""
    return p50 * 10 ** (BOHR_LOG10 * (pH - 7.40))


def main():
    if hill(1.0, 1.0, 1.0) is None or hill_plot(np.array([1.0]), np.array([0.5])) is None or p50_at_ph(1.0, 7.4) is None \
            or hill_line(np.array([1.0, 2.0, 4.0]), np.array([0.3, 0.5, 0.7])) is None:
        print("TODO: write hill(), hill_plot(), hill_line() and p50_at_ph() first.")
        return
    p, s = hb_standard_curve()
    n, p50 = hill_line(p, s)
    print(f"Hill plot, 20-80 % saturation: n = {n:.2f}, P50 = {p50:.1f} mmHg")
    x, y = hill_plot(p, s)
    slope = np.gradient(y, x)
    for target in (1, 10, 26, 50, 100, 500):
        i = int(np.argmin(abs(p - target)))
        print(f"  local Hill slope at {p[i]:5.0f} mmHg (S = {100 * s[i]:5.1f} %): {slope[i]:.2f}")

    print("\nO2 released between lungs (100 mmHg) and tissue:")
    for pt, what in ((40, "resting tissue"), (20, "working muscle")):
        hb = np.interp(100, p, s) - np.interp(pt, p, s)
        mb = hill(100, P50_MB, 1) - hill(pt, P50_MB, 1)
        print(f"  to {pt} mmHg ({what}): haemoglobin {100 * hb:.0f} %, myoglobin-like carrier {100 * mb:.0f} % of capacity")
    print(f"\nBohr effect: P50 at pH 7.20 = {p50_at_ph(p50, 7.20):.1f} mmHg, at pH 7.60 = {p50_at_ph(p50, 7.60):.1f} mmHg")

    if len(sys.argv) > 1:
        spo2 = float(sys.argv[1]) / 100
        guess = float(np.interp(spo2, s, p))
        print(f"\nYour reading SpO2 = {100 * spo2:.0f} % corresponds to an arterial PO2 of about {guess:.0f} mmHg "
              "on the standard curve (not a medical measurement).")

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 4))
    pp = np.linspace(0.5, 150, 400)
    a1.plot(p, 100 * s, "o", ms=4, label="Hb, standard curve (data)")
    a1.plot(pp, 100 * hill(pp, P50_MB, 1), "-", label=f"Mb, P50 = {P50_MB} mmHg, n = 1")
    a1.plot(pp, 100 * hill(pp, p50, n), "--", label=f"Hill line fit: n = {n:.2f}")
    a1.axvspan(20, 40, alpha=0.1, color="r"); a1.set_xlim(0, 150)
    a1.set_xlabel("PO2 (mmHg)"); a1.set_ylabel("saturation (%)"); a1.legend(fontsize=8)
    a2.plot(x, y, "o", ms=4, label="Hb data")
    a2.plot(x, n * x - n * np.log10(p50), "--", label=f"slope {n:.2f}")
    a2.plot(x, x - np.log10(P50_MB), ":", label="slope 1 (Mb)")
    a2.set_xlabel("log10 PO2"); a2.set_ylabel("log10 [S/(1-S)]"); a2.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(runs_dir() / "lesson03_hill.png", dpi=120)
    print("wrote runs/lesson03_hill.png")


if __name__ == "__main__":
    main()
