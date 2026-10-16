"""Lesson 02.2 hands-on: a reaction rate is a derivative. Estimate it from concentration data.

Reference solution. Run:   py lesson02_rates_solution.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent


def forward_difference(t, c):
    """Return dc/dt at t[0] .. t[-2] using (c[i+1] - c[i]) / (t[i+1] - t[i]).
    The result has one point fewer than t."""
    return np.diff(c) / np.diff(t)


def central_difference(t, c):
    """Return dc/dt at every t: central differences inside, one-sided at the two ends.
    np.gradient is second-order accurate inside and first-order at the ends (edge_order=1)."""
    return np.gradient(c, t)


def fit_k(c, rate):
    """For rate = k * c (first order), return k from a least-squares line through the origin.
    Minimising sum((rate - k c)^2) gives k = sum(c rate) / sum(c^2)."""
    return np.sum(c * rate) / np.sum(c * c)


def main():
    t, c = np.loadtxt(HERE / "decay_concentration.csv", delimiter=",", skiprows=1, unpack=True)
    fwd = forward_difference(t, c)
    cen = central_difference(t, c)
    if fwd is None or cen is None:
        print("TODO: write forward_difference() and central_difference() first.")
        return
    rate = -cen  # rate of disappearance is minus the slope
    k = fit_k(c, rate)
    if k is None:
        print("TODO: write fit_k() next.")
        return
    print(f"initial rate (forward)  = {-fwd[0]:.3e} mol/(L s)")
    print(f"initial rate (central)  = {rate[0]:.3e} mol/(L s)")
    print(f"rate at t = 300 s       = {rate[t == 300][0]:.3e} mol/(L s)")
    print(f"k from rate vs c        = {k:.5f} 1/s  (half-life {np.log(2) / k:.0f} s)")
    k_ln = -np.polyfit(t, np.log(c), 1)[0]
    print(f"k from ln c vs t        = {k_ln:.5f} 1/s  (lesson 02.1 method, less noisy)")

    (HERE / "runs").mkdir(exist_ok=True)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.5))
    a1.plot(t, c, "o")
    a1.set_xlabel("t (s)")
    a1.set_ylabel("c (mol/L)")
    a1.set_title("concentration")
    a2.plot(c, rate, "o", label="central differences")
    a2.plot(c, k * c, "-", label=f"rate = {k:.4f} c")
    a2.set_xlabel("c (mol/L)")
    a2.set_ylabel("-dc/dt (mol L$^{-1}$ s$^{-1}$)")
    a2.set_title("rate against concentration")
    a2.legend()
    fig.tight_layout()
    fig.savefig(HERE / "runs" / "lesson02_rates_solution.png", dpi=120)
    print("plot saved to runs/lesson02_rates_solution.png")


if __name__ == "__main__":
    main()
