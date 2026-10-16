"""Lesson 06.1 reference solution: diffusion times, the potato isotonic point, osmotic pressure
and Nernst potentials.

Run:   py lesson01_osmosis_solution.py              (example data)
       py lesson01_osmosis_solution.py my_potato.csv
The plot is saved to runs/lesson01_osmosis.png next to this file.
"""
import csv
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent

# CODATA 2022 via NIST (R and F follow from exact N_A, k and e)
R = 8.314462618      # J/(mol K)
F = 96485.33212      # C/mol

# Typical mammalian ion concentrations in mM (PhysiologyWeb, Table 1), inside and outside
IONS = {"K+": (1, 150.0, 4.0), "Na+": (1, 15.0, 145.0), "Cl-": (-1, 10.0, 110.0)}


def diffusion_time(x, D):
    """Typical time (s) to diffuse a distance x (m) in one direction, t = x^2 / (2 D)."""
    return x ** 2 / (2 * D)


def osmotic_pressure(c_osm, T):
    """van 't Hoff osmotic pressure (Pa) of a solution of c_osm osmol/L at T (K): Pi = c R T,
    with c converted to mol/m^3."""
    return c_osm * 1000.0 * R * T


def isotonic_point(c, pct, c_max=0.3):
    """Fit a straight line to the percentage mass change against concentration, using only the
    points with c <= c_max, and return (c0, u_c0): the concentration where the line crosses zero
    and its standard uncertainty from the fit covariance."""
    m = c <= c_max + 1e-9
    (s, b), cov = np.polyfit(c[m], pct[m], 1, cov=True)
    c0 = -b / s
    # c0 = -b/s; propagate with the full covariance matrix
    j = np.array([b / s ** 2, -1 / s])
    u = float(np.sqrt(j @ cov @ j))
    return c0, u


def nernst(z, c_in, c_out, T):
    """Equilibrium (Nernst) potential in volts, inside relative to outside:
    E = (R T / z F) ln(c_out / c_in)."""
    return R * T / (z * F) * np.log(c_out / c_in)


def read_osmosis(path):
    c, pct = [], []
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            m0, m1 = float(row["m_before_g"]), float(row["m_after_g"])
            c.append(float(row["c_NaCl_M"]))
            pct.append(100 * (m1 - m0) / m0)
    return np.array(c), np.array(pct)


def main():
    print("Diffusion times, t = x^2 / 2D")
    for label, x, D in [("small molecule across a bacterium, 1 um", 1e-6, 1e-9),
                        ("small molecule across a human cell, 20 um", 20e-6, 1e-9),
                        ("protein across a human cell, 20 um", 20e-6, 1e-10),
                        ("small molecule along a 1 cm tissue", 1e-2, 1e-9)]:
        t = diffusion_time(x, D)
        print(f"  {label:<45} {t:10.3g} s")

    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "osmosis_example.csv"
    c, pct = read_osmosis(path)
    c0, u = isotonic_point(c, pct)
    c0_all, u_all = isotonic_point(c, pct, c_max=1.0)
    print(f"\nPotato data: {path.name}")
    for cc in np.unique(c):
        g = pct[c == cc]
        print(f"  {cc:.2f} M NaCl: mass change {g.mean():+6.2f} % (sd {g.std(ddof=1):.2f}, n = {g.size})")
    print(f"isotonic point (fit c <= 0.3 M): {c0:.3f} +/- {u:.3f} mol/L NaCl")
    print(f"isotonic point (fit all points): {c0_all:.3f} +/- {u_all:.3f} mol/L NaCl")
    c_osm = 2 * c0          # ideal i = 2 for NaCl; measured i is about 1.9
    T = 295.15
    print(f"potato cell sap about {c_osm:.2f} osmol/L -> Pi = {osmotic_pressure(c_osm, T) / 1e5:.1f} bar at 22 C")

    print("\nNernst potentials at 37 C (inside relative to outside)")
    for ion, (z, ci, co) in IONS.items():
        print(f"  {ion:<4} in {ci:6.1f} mM, out {co:6.1f} mM: E = {1000 * nernst(z, ci, co, 310.15):+6.1f} mV")

    (HERE / "runs").mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.plot(c, pct, "o", label="strips")
    xs = np.linspace(0, 0.3, 50)
    s, b = np.polyfit(c[c <= 0.3 + 1e-9], pct[c <= 0.3 + 1e-9], 1)
    ax.plot(xs, s * xs + b, "-", label=f"line, c <= 0.3 M; zero at {c0:.3f} M")
    ax.axhline(0, color="grey", lw=0.8)
    ax.set_xlabel("NaCl concentration (mol/L)")
    ax.set_ylabel("mass change (%)")
    ax.set_title("Potato strips after 2 h")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(HERE / "runs" / "lesson01_osmosis.png", dpi=120)
    print("\nplot saved to runs/lesson01_osmosis.png")


if __name__ == "__main__":
    main()
