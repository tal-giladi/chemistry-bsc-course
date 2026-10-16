"""Lesson 02.1 hands-on: linearise the Arrhenius equation and read Ea from a slope.

Reference solution. Run:   py lesson01_arrhenius_solution.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
R = 8.314462618  # J/(mol K), CODATA 2022 (exact)


def linearise(T, k):
    """Return (x, y) for the straight-line form of k = A exp(-Ea / (R T)).
    x is 1/T and y is ln k (natural log)."""
    return 1.0 / T, np.log(k)


def fit_line(x, y):
    """Return (slope, intercept) of the least-squares line y = slope * x + intercept.
    np.polyfit returns the highest power first."""
    slope, intercept = np.polyfit(x, y, 1)
    return slope, intercept


def activation_energy(slope):
    """Return Ea in kJ/mol from the slope of ln k vs 1/T.
    slope = -Ea / R, so Ea = -slope * R (J/mol), then /1000 for kJ/mol."""
    return -slope * R / 1000.0


def main():
    T, k = np.loadtxt(HERE / "arrhenius_rates.csv", delimiter=",", skiprows=1, unpack=True)
    x, y = linearise(T, k)
    if x is None:
        print("TODO: write linearise() first.")
        return
    slope, intercept = fit_line(x, y)
    if slope is None:
        print("TODO: write fit_line() next.")
        return
    Ea = activation_energy(slope)
    if Ea is None:
        print("TODO: write activation_energy() last.")
        return
    A = np.exp(intercept)
    print(f"slope = {slope:.1f} K, intercept = {intercept:.2f}")
    print(f"Ea = {Ea:.1f} kJ/mol, A = {A:.2e} 1/s")
    print(f"predicted k at 37 C (310.15 K) = {A * np.exp(-Ea * 1e3 / (R * 310.15)):.2e} 1/s")

    (HERE / "runs").mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.plot(x * 1e3, y, "o", label="data")
    ax.plot(x * 1e3, slope * x + intercept, "-", label=f"fit, Ea = {Ea:.0f} kJ/mol")
    ax.set_xlabel("1000 / T  (1/K)")
    ax.set_ylabel("ln(k / s$^{-1}$)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(HERE / "runs" / "lesson01_arrhenius_solution.png", dpi=120)
    print("plot saved to runs/lesson01_arrhenius_solution.png")


if __name__ == "__main__":
    main()
