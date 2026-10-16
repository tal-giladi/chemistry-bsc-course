"""Lesson 04.2 reference solution: measure g with a pendulum, then use the same physics on a bond.

Run:   py lesson02_pendulum_solution.py                 (example data)
       py lesson02_pendulum_solution.py my_pendulum.csv (your own data, header L_m,trial,t20_s)
The plot is saved to runs/lesson02_pendulum.png next to this file.
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
G_STANDARD = 9.80665  # m/s^2, standard gravity (exact by definition; NIST)
SWINGS = 20           # each time in the CSV is for this many full swings


def periods(t_n, n=SWINGS):
    """Period of one full swing from the time for n swings."""
    return t_n / n


def mean_by_length(L, T):
    """Return the distinct lengths, the mean period at each, and the standard error of each mean."""
    Ls = np.unique(L)
    means = np.array([T[L == x].mean() for x in Ls])
    sems = np.array([T[L == x].std(ddof=1) / np.sqrt((L == x).sum()) for x in Ls])
    return Ls, means, sems


def fit_g(Ls, T_mean):
    """Fit T^2 = (4 pi^2 / g) L + c with a straight line. Return g, its standard uncertainty and c.
    The uncertainty comes from the slope's uncertainty: u_g / g = u_slope / slope."""
    (slope, c), cov = np.polyfit(Ls, T_mean ** 2, 1, cov=True)
    u_slope = np.sqrt(cov[0, 0])
    g = 4 * np.pi ** 2 / slope
    return g, g * u_slope / slope, c


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "pendulum_example.csv"
    L, _, t_n = np.loadtxt(path, delimiter=",", skiprows=1, unpack=True)
    T = periods(t_n)
    Ls, T_mean, T_sem = mean_by_length(L, T)
    g, u_g, c = fit_g(Ls, T_mean)
    for x, m, s in zip(Ls, T_mean, T_sem):
        print(f"L = {x:.2f} m   T = {m:.4f} +/- {s:.4f} s")
    print(f"g = {g:.3f} +/- {u_g:.3f} m/s^2   (standard gravity {G_STANDARD} m/s^2)")
    print(f"intercept of T^2 vs L = {c:+.4f} s^2 (should be near 0; a clear offset means a length error)")

    # The same formula on a molecule: omega = sqrt(k/mu)
    k, mu = 516.3, 1.6267e-27   # HCl force constant (N/m) and reduced mass (kg)
    nu = np.sqrt(k / mu) / (2 * np.pi)
    print(f"HCl: nu = {nu:.3e} Hz, wavenumber = {nu / 2.99792458e10:.0f} cm^-1, period = {1 / nu * 1e15:.1f} fs")

    (HERE / "runs").mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.errorbar(Ls, T_mean ** 2, yerr=2 * T_mean * T_sem, fmt="o", capsize=3, label="data")
    xx = np.linspace(0, Ls.max() * 1.05, 50)
    ax.plot(xx, 4 * np.pi ** 2 / g * xx + c, label=f"fit, g = {g:.2f} m/s$^2$")
    ax.set_xlabel("L (m)")
    ax.set_ylabel("T$^2$ (s$^2$)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(HERE / "runs" / "lesson02_pendulum.png", dpi=120)
    print("plot saved to runs/lesson02_pendulum.png")


if __name__ == "__main__":
    main()
