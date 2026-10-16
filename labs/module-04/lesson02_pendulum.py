"""Lesson 04.2 hands-on: measure g with a pendulum, then use the same physics on a bond.

Fill in the three TODO functions, then run:
       py lesson02_pendulum.py                 (example data)
       py lesson02_pendulum.py my_pendulum.csv (your own data, header L_m,trial,t20_s)
Reference solution: lesson02_pendulum_solution.py
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
    """Period of one full swing from the time for n swings.
    TODO: one line."""
    return None


def mean_by_length(L, T):
    """Return the distinct lengths, the mean period at each, and the standard error of each mean.
    TODO: Ls = np.unique(L); for each x in Ls take T[L == x], its mean, and its
    standard error std(ddof=1) / sqrt(number of trials). Return three numpy arrays."""
    return None


def fit_g(Ls, T_mean):
    """Fit T^2 = (4 pi^2 / g) L + c with a straight line. Return g, its standard uncertainty and c.
    The uncertainty comes from the slope's uncertainty: u_g / g = u_slope / slope.
    TODO: (slope, c), cov = np.polyfit(Ls, T_mean**2, 1, cov=True); u_slope = sqrt(cov[0, 0])."""
    return None


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "pendulum_example.csv"
    L, _, t_n = np.loadtxt(path, delimiter=",", skiprows=1, unpack=True)
    T = periods(t_n)
    if T is None:
        print("TODO: write periods() first.")
        return
    res = mean_by_length(L, T)
    if res is None:
        print("TODO: write mean_by_length() next.")
        return
    Ls, T_mean, T_sem = res
    res = fit_g(Ls, T_mean)
    if res is None:
        print("TODO: write fit_g() last.")
        return
    g, u_g, c = res
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
