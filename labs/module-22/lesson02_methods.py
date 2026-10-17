"""Lesson 22.2 - from polarimeter readings to rate constants and orders.

Fill in the functions marked TODO, then run:  py lesson02_methods.py
Reference solution: lesson02_methods_solution.py
Writes runs/lesson02_methods.png.
Data: Michaelis & Menten (1913) Table I, experiments 1 and 5 (invertase_rotation.csv) and the seven
initial rates of the same table (invertase_initial_rates.csv), from the Johnson & Goody translation.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

from kin22 import read_csv, runs_dir

# Theoretical total change in rotation for complete inversion (Michaelis & Menten, Table I)
X_INF = {1: 18.57, 5: 1.190}


def rotation_to_fraction(rot, rot0, rot_inf):
    """Fraction converted from a property that changes linearly with extent: (P0 - P)/(P0 - Pinf)."""
    # TODO: return (rot0 - rot) / (rot0 - rot_inf)
    raise NotImplementedError("TODO: write rotation_to_fraction() first (see the hints in the code).")


def first_order_property(t, p_inf, p0, k):
    """Property of a first-order reaction: P(t) = Pinf + (P0 - Pinf) exp(-k t)."""
    return p_inf + (p0 - p_inf) * np.exp(-k * t)


def fit_free_endpoint(t, p):
    """Nonlinear fit of first_order_property with Pinf, P0 and k all free. Returns values and 1-sigma errors."""
    # TODO: guess = (p[-1], p[0], 3 / t[-1])
    # TODO: popt, pcov = curve_fit(first_order_property, t, p, p0=guess)
    # TODO: return popt and the square roots of the diagonal of pcov
    raise NotImplementedError("TODO: write fit_free_endpoint() first (see the hints in the code).")


def initial_rate(t, p, t_max):
    """Slope of a straight line through the points with t <= t_max (property units per time)."""
    # TODO: keep the points with t <= t_max (a boolean mask)
    # TODO: return the slope of np.polyfit(t[mask], p[mask], 1)
    raise NotImplementedError("TODO: write initial_rate() first (see the hints in the code).")


def local_orders(S, v):
    """Order between neighbouring points: d ln v / d ln S."""
    # TODO: return np.diff(np.log(v)) / np.diff(np.log(S))
    raise NotImplementedError("TODO: write local_orders() first (see the hints in the code).")


def load(exp):
    rows = [r for r in read_csv("invertase_rotation.csv") if int(r["experiment"]) == exp]
    return np.array([float(r["t_min"]) for r in rows]), np.array([float(r["rotation_deg"]) for r in rows])


def main():
    t5, r5 = load(5)
    r0, rinf_theory = r5[0], r5[0] - X_INF[5]
    x5 = rotation_to_fraction(r5, r0, rinf_theory)
    print("Experiment 5 (20.8 mM): fraction converted", np.round(x5, 3))

    popt, perr = fit_free_endpoint(t5, r5)
    print(f"  free-endpoint fit: Pinf = {popt[0]:.3f} +/- {perr[0]:.3f} deg (theory {rinf_theory:.3f}), "
          f"k = {popt[2]:.4f} +/- {perr[2]:.4f} min^-1")
    for label, rinf in (("theoretical endpoint", rinf_theory), ("last reading as 'infinity'", r5[-1] - 1e-3)):
        m = t5 > 0
        y = np.log((r5[m] - rinf) / (r0 - rinf))
        k = -np.polyfit(t5[m], y, 1)[0]
        print(f"  ln plot with {label:26s}: k = {k:.4f} min^-1")

    t1, r1 = load(1)
    slope = initial_rate(t1, r1, 26)
    mM_per_deg = 333.0 / X_INF[1]
    print(f"Experiment 1 (333 mM): initial rate {-slope:.4f} deg/min = {-slope * mM_per_deg:.3f} mM/min")

    rows = read_csv("invertase_initial_rates.csv")
    S = np.array([float(r["sucrose_M"]) for r in rows])[::-1] * 1000
    v = np.array([float(r["initial_rate_arb"]) for r in rows])[::-1]
    orders = local_orders(S, v)
    for (a, b), n in zip(zip(S[:-1], S[1:]), orders):
        print(f"  local order between {a:6.1f} and {b:6.1f} mM: {n:5.2f}")

    fig, ax = plt.subplots(1, 3, figsize=(13, 4))
    tt = np.linspace(0, t5.max() * 1.5, 200)
    ax[0].plot(t5, r5, "o", label="Exp. 5, 20.8 mM")
    ax[0].plot(tt, first_order_property(tt, *popt), "-", label="free-endpoint fit")
    ax[0].axhline(rinf_theory, ls="--", c="grey", label="theoretical endpoint")
    ax[0].set_xlabel("t / min"); ax[0].set_ylabel("rotation / degree"); ax[0].legend()
    ax[1].plot(t5, r5 - first_order_property(t5, *popt), "o")
    ax[1].axhline(0, c="grey"); ax[1].set_xlabel("t / min"); ax[1].set_ylabel("residual / degree")
    ax[2].loglog(S, v, "o-"); ax[2].set_xlabel("[sucrose] / mM"); ax[2].set_ylabel("initial rate (arb.)")
    fig.tight_layout(); fig.savefig(runs_dir() / "lesson02_methods.png", dpi=120)
    print("saved runs/lesson02_methods.png")


if __name__ == "__main__":
    try:
        main()
    except NotImplementedError as e:
        print(e)
