"""Lesson 03.3 hands-on: rate laws as differential equations.

Part 1: Euler's method for dc/dt = -k c and how its error shrinks with the step size.
Part 2: the same equation with scipy's solve_ivp.
Part 3: find the order of a reaction from data by testing the three integrated rate laws.

Fill in the functions marked TODO, then run:   py lesson03_ode.py
Reference solution: lesson03_ode_solution.py
The figure is saved to runs/lesson03_ode.png next to this file.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

HERE = Path(__file__).resolve().parent
K1, C0, T_END = 0.0040, 0.100, 300.0   # 1/s, mol/L, s (same reaction as lesson 02.2)


def rate_law(t, c, k, n):
    """Right-hand side of dc/dt = -k c^n (n = 0, 1 or 2). t is unused but solve_ivp passes it."""
    return -k * c ** n


def euler(f, c0, t_end, h, *args):
    """Euler's method: c[i+1] = c[i] + h f(t[i], c[i]). Return arrays t and c, t from 0 to t_end."""
    # TODO: n_steps = int(round(t_end / h)); t = np.linspace(0, n_steps * h, n_steps + 1)
    # TODO: c = np.empty(n_steps + 1); c[0] = c0
    # TODO: for i in range(n_steps): c[i + 1] = c[i] + h * f(t[i], c[i], *args)
    # TODO: return t, c
    return None


def order_fits(t, c):
    """Fit the three linearised integrated rate laws. Return {order: (slope, r_squared)} for
    order 0: c vs t, order 1: ln c vs t, order 2: 1/c vs t."""
    # TODO: for each (order, y) in [(0, c), (1, np.log(c)), (2, 1 / c)]: slope, intercept = np.polyfit(t, y, 1)
    # TODO: r2 = 1 - sum of squared residuals / sum((y - y.mean())**2); store out[order] = (slope, r2).
    return None


def main():
    exact = C0 * np.exp(-K1 * T_END)
    print(f"1. Euler for dc/dt = -k c, k = {K1} 1/s, c0 = {C0} mol/L, exact c({T_END:.0f} s) = {exact:.5f}")
    steps, errors = [60.0, 30.0, 15.0, 7.5, 3.75], []
    for h in steps:
        res = euler(rate_law, C0, T_END, h, K1, 1)
        if res is None:
            print("TODO: write euler() first.")
            return
        err = res[1][-1] - exact
        errors.append(abs(err))
        print(f"   h = {h:5.2f} s: c = {res[1][-1]:.5f}, error = {err:+.2e} mol/L")
    ratios = np.array(errors[:-1]) / np.array(errors[1:])
    print(f"   error ratio when h halves: {np.array2string(ratios, precision=2)} (about 2: first-order method)")

    sol = solve_ivp(rate_law, (0, T_END), [C0], args=(K1, 1), rtol=1e-8, atol=1e-12)
    print(f"2. solve_ivp (RK45, rtol 1e-8): c = {sol.y[0, -1]:.6f}, error {sol.y[0, -1] - exact:+.1e}, "
          f"{sol.t.size - 1} steps")

    t, c = np.loadtxt(HERE / "order_test.csv", delimiter=",", skiprows=1, unpack=True)
    fits = order_fits(t, c)
    if fits is None:
        print("TODO: write order_fits() last.")
        return
    print("3. which integrated rate law is straight?")
    for order, (slope, r2) in fits.items():
        print(f"   order {order}: slope {slope:+.3e}, R^2 = {r2:.5f}")
    best = max(fits, key=lambda n: fits[n][1])
    k_best = fits[best][0] if best == 2 else -fits[best][0]
    print(f"   best: order {best}, k = {k_best:.3g} (L/mol)/s" if best == 2 else f"   best: order {best}, k = {k_best:.3g}")

    (HERE / "runs").mkdir(exist_ok=True)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.5, 3.6))
    tt = np.linspace(0, T_END, 200)
    a1.plot(tt, C0 * np.exp(-K1 * tt), "k-", label="exact")
    for h in (60.0, 15.0):
        te, ce = euler(rate_law, C0, T_END, h, K1, 1)
        a1.plot(te, ce, "o--", ms=3, label=f"Euler h = {h:.0f} s")
    a1.set_xlabel("t (s)")
    a1.set_ylabel("c (mol/L)")
    a1.legend()
    a2.plot(t, 1 / c, "o", ms=3, label="1/c (second order)")
    a2.set_xlabel("t (s)")
    a2.set_ylabel("1/c (L/mol)")
    a2.legend()
    fig.tight_layout()
    out = HERE / "runs" / "lesson03_ode.png"
    fig.savefig(out, dpi=120)
    print(f"plot saved to runs/{out.name}")


if __name__ == "__main__":
    main()
