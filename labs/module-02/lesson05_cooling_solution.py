"""Lesson 02.5 module practical: analyse a cooling curve with everything from Module 2.

Model (Newton's law of cooling): dT/dt = -k (T - T_env), so T(t) = T_env + (T0 - T_env) exp(-k t).

Usage (from this folder):
    py lesson05_cooling_solution.py                              # the example data, T_env = 23.0 C, 250 g water
    py lesson05_cooling_solution.py my_curve.csv 22.5 0.262      # your CSV (t_s,T_C), room temp in C, water mass in kg

Reference solution. The figure is saved to runs/lesson05_cooling_solution.png next to this file.
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import trapezoid

HERE = Path(__file__).resolve().parent
C_WATER = 4.18  # J/(g K), liquid water near 25-80 C (NIST WebBook: Cp about 75.4 J/(mol K) / 18.015 g/mol)
T_DRINK = 60.0  # C, a comfortable drinking temperature used for the "when can I drink it" question


def fit_log(t, T, T_env):
    """Lesson 02.1: fit ln(T - T_env) = ln(T0 - T_env) - k t. Return (k, T0).
    Readings within 0.5 C of room temperature are dropped: their log is dominated by noise."""
    keep = (T - T_env) > 0.5
    slope, intercept = np.polyfit(t[keep], np.log(T[keep] - T_env), 1)
    return -slope, T_env + np.exp(intercept)


def cooling_rate(t, T):
    """Lesson 02.2: dT/dt at every point by central differences (C/s).
    Central differences inside, one-sided at the two ends."""
    return np.gradient(T, t)


def sensitivities(t, k, T0, T_env):
    """Lesson 02.5: partial derivatives of T(t) = T_env + (T0 - T_env) exp(-k t).
    Return (dT/dk, dT/dT_env) at time t.
    Hold the other inputs fixed and differentiate with the chain rule."""
    e = np.exp(-k * t)
    return -t * (T0 - T_env) * e, 1.0 - e


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "cooling_example.csv"
    T_env = float(sys.argv[2]) if len(sys.argv) > 2 else 23.0
    mass_g = 1000 * float(sys.argv[3]) if len(sys.argv) > 3 else 250.0
    t, T = np.loadtxt(path, delimiter=",", skiprows=1, unpack=True)
    print(f"{path.name}: {t.size} readings over {t[-1] / 60:.0f} min, T_env = {T_env} C, water {mass_g:.0f} g")

    # 1. Exponential and logarithm (02.1)
    k, T0 = fit_log(t, T, T_env)
    if k is None:
        print("TODO: write fit_log() first.")
        return
    print(f"1. log fit: k = {k:.3e} 1/s (time constant {1 / k / 60:.1f} min), T0 = {T0:.1f} C")

    # 2. Derivative (02.2): rate against temperature excess should be a line through 0, slope -k
    dTdt = cooling_rate(t, T)
    if dTdt is None:
        print("TODO: write cooling_rate() next.")
        return
    excess = T - T_env
    k_rate = -np.sum(excess * dTdt) / np.sum(excess**2)
    print(f"2. from dT/dt vs (T - T_env): k = {k_rate:.3e} 1/s; initial rate {dTdt[0] * 60:.2f} C/min")

    # 3. Integral (02.3): integrating dT/dt gives back the total change; heat lost by the water
    dT_int = trapezoid(dTdt, x=t)
    Q = mass_g * C_WATER * (T[0] - T[-1])
    print(f"3. integral of dT/dt = {dT_int:.1f} C vs T_end - T_start = {T[-1] - T[0]:.1f} C")
    print(f"   heat lost = m c dT = {Q / 1000:.1f} kJ, mean power {Q / t[-1]:.1f} W, "
          f"initial power {mass_g * C_WATER * k * (T0 - T_env):.1f} W")

    # 4. Series (02.4): early times T is about T0 - k (T0 - T_env) t
    t_lin = 120.0
    T_exact = T_env + (T0 - T_env) * np.exp(-k * t_lin)
    T_line = T0 - k * (T0 - T_env) * t_lin
    print(f"4. at t = {t_lin:.0f} s: model {T_exact:.2f} C, linear Taylor {T_line:.2f} C")

    # 5. Partial derivatives (02.5): which input limits a 1-hour prediction?
    dk, dTe = 0.05 * k, 1.0  # assume 5 % uncertainty in k and 1 C in room temperature
    s_k, s_env = sensitivities(3600.0, k, T0, T_env)
    if s_k is None:
        print("TODO: write sensitivities() last.")
        return
    T_1h = T_env + (T0 - T_env) * np.exp(-k * 3600.0)
    u = np.hypot(s_k * dk, s_env * dTe)
    print(f"5. T at 60 min = {T_1h:.1f} +- {u:.1f} C  "
          f"(k term {abs(s_k * dk):.2f} C, T_env term {abs(s_env * dTe):.2f} C)")
    t_drink = np.log((T0 - T_env) / (T_DRINK - T_env)) / k
    print(f"   drinkable ({T_DRINK:.0f} C) after {t_drink / 60:.1f} min")

    (HERE / "runs").mkdir(exist_ok=True)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.5, 3.6))
    tm = t / 60
    a1.plot(tm, T, "o", ms=3, label="data")
    a1.plot(tm, T_env + (T0 - T_env) * np.exp(-k * t), "-", label="Newton fit")
    a1.axhline(T_env, color="grey", lw=0.8)
    a1.set_xlabel("t (min)")
    a1.set_ylabel("T (C)")
    a1.legend()
    a2.plot(excess, dTdt * 60, "o", ms=3, label="central differences")
    a2.plot(excess, -k_rate * excess * 60, "-", label="slope -k")
    a2.set_xlabel("T - T_env (C)")
    a2.set_ylabel("dT/dt (C/min)")
    a2.legend()
    fig.tight_layout()
    out = HERE / "runs" / "lesson05_cooling_solution.png"
    fig.savefig(out, dpi=120)
    print(f"plot saved to runs/{out.name}")


if __name__ == "__main__":
    main()
