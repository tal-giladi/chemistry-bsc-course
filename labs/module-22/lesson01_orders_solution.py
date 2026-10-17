"""Lesson 22.1 - reference solution. Same reaction, two apparent orders: the 1913 invertase data.

Run:  py lesson01_orders_solution.py      Writes runs/lesson01_orders.png.
"""
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from kin22 import OH_CH4_JPL, k_mod_arrhenius, read_csv, runs_dir

SECONDS_PER_YEAR = 365.25 * 24 * 3600


def line_fit(x, y):
    """Straight line y = a + b x. Returns slope b, intercept a and R^2."""
    b, a = np.polyfit(x, y, 1)
    resid = y - (a + b * x)
    r2 = 1 - np.sum(resid**2) / np.sum((y - y.mean()) ** 2)
    return b, a, r2


def zero_order_test(t, x):
    """Zero order in sucrose: x = (k0/S0) t, so x against t is a straight line."""
    return line_fit(t, x)


def first_order_test(t, x):
    """First order: ln(1 - x) = -k t, so ln(1 - x) against t is a straight line."""
    return line_fit(t, np.log(1 - x))


def pseudo_first_order_lifetime(k2, partner):
    """Lifetime tau = 1/(k2 [partner]) for a second-order loss with the partner held constant."""
    return 1.0 / (k2 * partner)


def load(S0):
    rows = [r for r in read_csv("invertase_timecourse.csv")
            if float(r["sucrose_mM"]) == S0 and r["used_in_MM_constant"] == "1"]
    return np.array([float(r["t_min"]) for r in rows]), np.array([float(r["fraction_converted"]) for r in rows])


def main():
    out = {}
    for S0 in (333.0, 166.7, 41.6, 20.8):
        t, x = load(S0)
        b0, a0, r0 = zero_order_test(t, x)
        b1, a1, r1 = first_order_test(t, x)
        out[S0] = (t, x, b0, a0, b1, a1)
        print(f"S0 = {S0:5.1f} mM: zero-order R^2 = {r0:.4f}, first-order R^2 = {r1:.4f}")
        print(f"   zero-order rate = {b0 * S0:.3f} mM/min;  first-order k = {-b1:.4f} min^-1 "
              f"(t1/2 = {math.log(2) / -b1:.0f} min)")

    k = k_mod_arrhenius(OH_CH4_JPL, 272.0)
    for oh in (1.0e6, 9.4e5):
        tau = pseudo_first_order_lifetime(k, oh)
        print(f"OH + CH4 at 272 K: k = {k:.2e} cm3/s; [OH] = {oh:.1e} cm-3 -> lifetime {tau / SECONDS_PER_YEAR:.1f} yr")

    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    for S0, (t, x, b0, a0, b1, a1) in out.items():
        tt = np.linspace(0, t.max(), 100)
        ax[0].plot(t, x, "o", label=f"{S0:g} mM")
        ax[0].plot(tt, a0 + b0 * tt, "-")
        ax[1].plot(t, np.log(1 - x), "o", label=f"{S0:g} mM")
        ax[1].plot(tt, a1 + b1 * tt, "-")
    ax[0].set_xlabel("t / min"); ax[0].set_ylabel("fraction converted x"); ax[0].legend()
    ax[1].set_xlabel("t / min"); ax[1].set_ylabel("ln(1 - x)"); ax[1].legend()
    fig.tight_layout(); fig.savefig(runs_dir() / "lesson01_orders.png", dpi=120)
    print("saved runs/lesson01_orders.png")


if __name__ == "__main__":
    main()
