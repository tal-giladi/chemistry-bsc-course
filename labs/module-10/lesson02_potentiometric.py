"""Lesson 10.2 exercise: end points from potentiometric data (derivatives and a Gran plot)
Fill in the TODO functions. Reference solution: lesson02_potentiometric_solution.py
and formal potentials from a redox titration curve.

Run:   py lesson02_potentiometric.py
       py lesson02_potentiometric.py my_ph.csv my_redox.csv   (columns V_mL,pH and V_mL,E_mV)
Acid-base example: 25.00 mL acetic acid titrated with 0.1000 M NaOH.
Redox example: 25.00 mL Fe2+ in 1 M H2SO4 titrated with 0.1000 M Ce4+, Pt vs Ag/AgCl (sat. KCl, +197 mV vs SHE).
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
C_TITRANT = 0.1000          # mol/L, NaOH and Ce4+
V_SAMPLE = 25.00            # mL
E_REF_MV = 197.0            # Ag/AgCl, saturated KCl, vs SHE
GRAN_WINDOW = (10.0, 19.0)  # mL, the straight part before equivalence (80-95 % of V_eq)


def read_xy(path, ycol):
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    return np.array([float(r["V_mL"]) for r in rows]), np.array([float(r[ycol]) for r in rows])


def derivative_endpoint(v, y):
    """End point = volume of the steepest step. Use the first derivative dy/dV between neighbouring
    points, placed at the midpoint volumes, and return the midpoint where |dy/dV| is largest."""
    # TODO: d1 = np.diff(y) / np.diff(v); midpoints vm = (v[:-1] + v[1:]) / 2; return vm at np.argmax(abs(d1)).
    return None


def gran_endpoint(v, ph, vmin, vmax):
    """Gran plot for a weak acid with strong base: before equivalence V * 10**-pH = Ka (V_eq - V).
    Fit a straight line to the points with vmin <= V <= vmax; return (V_eq, Ka) where
    V_eq = -intercept / slope and Ka = -slope."""
    # TODO: select vmin <= v <= vmax, g = v * 10**-ph, np.polyfit(v, g, 1) gives slope and intercept; return (-intercept / slope, -slope).
    return None


def second_derivative_endpoint(v, y):
    """Volume where the second derivative crosses zero, by linear interpolation."""
    d1 = np.diff(y) / np.diff(v)
    vm = (v[:-1] + v[1:]) / 2
    d2 = np.diff(d1) / np.diff(vm)
    vmm = (vm[:-1] + vm[1:]) / 2
    i = int(np.argmax(np.abs(d1)))
    for j in range(max(i - 2, 0), min(i + 1, len(d2) - 1)):
        if d2[j] > 0 >= d2[j + 1] or d2[j] < 0 <= d2[j + 1]:
            return float(vmm[j] - d2[j] * (vmm[j + 1] - vmm[j]) / (d2[j + 1] - d2[j]))
    return float(vm[i])


def main():
    if derivative_endpoint(np.array([0.0, 1.0, 2.0]), np.array([0.0, 1.0, 3.0])) is None or \
            gran_endpoint(np.array([1.0, 2.0, 3.0]), np.array([4.0, 4.3, 4.6]), 0, 5) is None:
        print("TODO: write derivative_endpoint() and gran_endpoint() first.")
        return
    ph_path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "potentiometric_example.csv"
    rx_path = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "redox_example.csv"

    v, ph = read_xy(ph_path, "pH")
    v1 = derivative_endpoint(v, ph)
    v2 = second_derivative_endpoint(v, ph)
    vg, ka = gran_endpoint(v, ph, *GRAN_WINDOW)
    ph_half = float(np.interp(vg / 2, v, ph))
    print("Acid-base (pH electrode)")
    print(f"  first derivative end point  {v1:.3f} mL")
    print(f"  second derivative end point {v2:.3f} mL")
    print(f"  Gran end point              {vg:.3f} mL, Ka {ka:.3g} (pKa {-math.log10(ka):.3f})")
    print(f"  pH at half-equivalence      {ph_half:.3f}  (true pKa 4.757)")
    print(f"  acid concentration          {C_TITRANT * v2 / V_SAMPLE:.5f} mol/L (from the second derivative)")

    vr, e = read_xy(rx_path, "E_mV")
    ve1 = derivative_endpoint(vr, e)
    ve = second_derivative_endpoint(vr, e)
    e_half = float(np.interp(ve / 2, vr, e)) + E_REF_MV
    after = vr > ve + 1.0
    e_ce = np.mean(e[after] + E_REF_MV - 59.16 * np.log10((vr[after] - ve) / ve))
    e_eq = float(e[np.argmin(np.abs(vr - ve))]) + E_REF_MV
    print("Redox (Pt vs Ag/AgCl)")
    print(f"  first derivative end point  {ve1:.3f} mL")
    print(f"  second derivative end point {ve:.3f} mL -> Fe2+ {C_TITRANT * ve / V_SAMPLE:.5f} mol/L")
    print(f"  E at half-equivalence       {e_half / 1000:.3f} V vs SHE = E0' Fe3+/Fe2+")
    print(f"  E0' Ce4+/Ce3+ from the points after equivalence {e_ce / 1000:.3f} V vs SHE")
    print(f"  E of the reading nearest the end point {e_eq / 1000:.3f} V vs SHE (predicted (0.68 + 1.44)/2 = 1.06 V)")

    fig, axes = plt.subplots(1, 3, figsize=(13, 4))
    axes[0].plot(v, ph, "o-", ms=3)
    axes[0].axvline(v1, ls="--")
    axes[0].set(xlabel="NaOH / mL", ylabel="pH", title="pH curve")
    sel = (v >= GRAN_WINDOW[0]) & (v <= GRAN_WINDOW[1])
    axes[1].plot(v[v < vg], v[v < vg] * 10 ** -ph[v < vg] * 1e5, "o", ms=3)
    xs = np.linspace(GRAN_WINDOW[0], vg, 10)
    axes[1].plot(xs, ka * (vg - xs) * 1e5, "-")
    axes[1].plot(v[sel], v[sel] * 10 ** -ph[sel] * 1e5, "o", ms=5, mfc="none")
    axes[1].set(xlabel="NaOH / mL", ylabel="V x 10^-pH  (x 1e5)", title="Gran plot")
    axes[2].plot(vr, e, "o-", ms=3)
    axes[2].axvline(ve, ls="--")
    axes[2].set(xlabel="Ce4+ / mL", ylabel="E / mV vs Ag/AgCl", title="Redox curve")
    out = HERE / "runs"
    out.mkdir(exist_ok=True)
    fig.savefig(out / "lesson02_potentiometric.png", dpi=120, bbox_inches="tight")
    print(f"plot: {out / 'lesson02_potentiometric.png'}")


if __name__ == "__main__":
    main()
