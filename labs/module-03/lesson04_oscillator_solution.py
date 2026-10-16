"""Lesson 03.4 hands-on: second-order equations and oscillators.

Part 1: the characteristic equation m r^2 + b r + k = 0 and the three kinds of damping.
Part 2: a damped oscillator solved numerically (as two first-order equations) against the formula.
Part 3: the force constant of the HCl bond from its vibrational wavenumber.
Part 4: damping rate and quality factor from your pendulum's amplitude readings.

Usage (from this folder):
    py lesson04_oscillator_solution.py                       # the example pendulum data
    py lesson04_oscillator_solution.py my_pendulum.csv       # your CSV (swings,t_s,amplitude_cm)

Reference solution. Run:   py lesson04_oscillator_solution.py
The figure is saved to runs/lesson04_oscillator.png next to this file.
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

HERE = Path(__file__).resolve().parent
M_U = 1.66053906892e-27                      # kg, atomic mass constant (CODATA 2022)
C_CM = 2.99792458e10                         # cm/s
M_H, M_35CL = 1.00782503223, 34.968852682    # u, NIST atomic masses
OMEGA_E_HCL = 2990.9463                      # cm^-1, H35Cl, NIST WebBook (Huber and Herzberg)


def classify(m, b, k):
    """Return (roots, kind) of m r^2 + b r + k = 0, kind = 'underdamped', 'critically damped'
    or 'overdamped' from the sign of the discriminant b^2 - 4 m k."""
    roots = np.roots([m, b, k])
    disc = b * b - 4 * m * k
    if np.isclose(disc, 0.0, atol=1e-12 * max(b * b, 4 * m * k)):
        kind = "critically damped"
    elif disc < 0:
        kind = "underdamped"
    else:
        kind = "overdamped"
    return roots, kind


def rhs(t, y, m, b, k):
    """m x'' + b x' + k x = 0 written as two first-order equations for y = [x, v]:
    x' = v and v' = -(b v + k x) / m."""
    x, v = y
    return [v, -(b * v + k * x) / m]


def force_constant(omega_tilde_cm, m1_u, m2_u):
    """Force constant (N/m) of a diatomic from its harmonic wavenumber (cm^-1):
    reduced mass mu = m1 m2 / (m1 + m2), omega = 2 pi c omega_tilde, k = mu omega^2."""
    mu = M_U * m1_u * m2_u / (m1_u + m2_u)
    omega = 2 * np.pi * C_CM * omega_tilde_cm
    return mu * omega ** 2


def fit_decay(t, amp):
    """Fit amp = A0 exp(-gamma t) by a straight line through ln(amp) against t.
    Return (gamma in 1/s, A0)."""
    slope, intercept = np.polyfit(t, np.log(amp), 1)
    return -slope, np.exp(intercept)


def main():
    m, k = 1.0, 4.0
    print("1. m r^2 + b r + k = 0 with m = 1, k = 4 (omega0 = 2 rad/s)")
    for b in (0.4, 4.0, 10.0):
        res = classify(m, b, k)
        if res is None:
            print("TODO: write classify() first.")
            return
        roots, kind = res
        print(f"   b = {b:4.1f}: roots {np.array2string(roots, precision=3)} -> {kind}")

    b = 0.4
    if rhs(0.0, [1.0, 0.0], m, b, k) is None:
        print("TODO: write rhs() next.")
        return
    t = np.linspace(0, 20, 401)
    sol = solve_ivp(rhs, (0, 20), [1.0, 0.0], t_eval=t, args=(m, b, k), rtol=1e-9, atol=1e-12)
    g = b / (2 * m)
    wd = np.sqrt(k / m - g * g)
    x_exact = np.exp(-g * t) * (np.cos(wd * t) + g / wd * np.sin(wd * t))
    print(f"2. solve_ivp vs formula for b = {b}: max difference {np.max(np.abs(sol.y[0] - x_exact)):.1e}; "
          f"damped period {2 * np.pi / wd:.3f} s (undamped {2 * np.pi / np.sqrt(k / m):.3f} s)")

    kf = force_constant(OMEGA_E_HCL, M_H, M_35CL)
    if kf is None:
        print("TODO: write force_constant() next.")
        return
    mu_u = M_H * M_35CL / (M_H + M_35CL)
    print(f"3. H35Cl: reduced mass {mu_u:.5f} u, force constant k = {kf:.0f} N/m, "
          f"period {1e15 / (C_CM * OMEGA_E_HCL):.2f} fs")

    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "pendulum_example.csv"
    n, tp, amp = np.loadtxt(path, delimiter=",", skiprows=1, unpack=True)
    fit = fit_decay(tp, amp)
    if fit is None:
        print("TODO: write fit_decay() last.")
        return
    gamma, A0 = fit
    period = (tp[-1] - tp[0]) / (n[-1] - n[0])
    w0 = 2 * np.pi / period
    print(f"4. {path.name}: period {period:.3f} s, gamma = {gamma:.4f} 1/s, amplitude half-life "
          f"{np.log(2) / gamma:.0f} s, Q = omega0 / (2 gamma) = {w0 / (2 * gamma):.0f}")
    L = 9.81 * (period / (2 * np.pi)) ** 2
    print(f"   a simple pendulum with this period has length {L:.2f} m (T = 2 pi sqrt(L/g))")

    (HERE / "runs").mkdir(exist_ok=True)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.5, 3.6))
    a1.plot(t, sol.y[0], "-", label="solve_ivp")
    a1.plot(t[::10], x_exact[::10], "o", ms=3, label="formula")
    a1.plot(t, np.exp(-g * t), "k:", lw=0.8, label="envelope e^(-gamma t)")
    a1.set_xlabel("t (s)")
    a1.set_ylabel("x")
    a1.legend()
    a2.semilogy(tp, amp, "o", label="readings")
    a2.semilogy(tp, A0 * np.exp(-gamma * tp), "-", label="fit")
    a2.set_xlabel("t (s)")
    a2.set_ylabel("amplitude (cm)")
    a2.legend()
    fig.tight_layout()
    out = HERE / "runs" / "lesson04_oscillator.png"
    fig.savefig(out, dpi=120)
    print(f"plot saved to runs/{out.name}")


if __name__ == "__main__":
    main()
