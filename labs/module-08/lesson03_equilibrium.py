"""Lesson 08.3 hands-on: exact equilibrium (ICE) with a root finder.

Fill in the two TODOs, then run:
       py lesson03_equilibrium.py
Reference solution: lesson03_equilibrium_solution.py
Data:  thermo_data.csv (OpenStax Chemistry 2e Appendix G); K from Delta G = Delta H - T Delta S
       with Delta H and Delta S taken as constant (lesson 08.2).
Writes runs/lesson03_N2O4_vs_P.png.
Gas-phase K here is Kp with pressures in bar (standard pressure 1 bar).
"""
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

from thermo import load_table

R = 8.314462618   # J/(mol K), CODATA 2022


def k_from_table(reaction, table, t):
    """K at temperature t from tabulated Delta_f H and S (constant-Delta H, Delta S approximation)."""
    dh = sum(nu * table[sp]["dHf_kJ_mol"] for sp, nu in reaction.items()) * 1000
    ds = sum(nu * table[sp]["S_J_molK"] for sp, nu in reaction.items())
    return float(np.exp(-(dh - t * ds) / (R * t)))


def reaction_quotient(reaction, moles, p_total):
    """Qp = product of (x_i P)^nu_i over gases, x_i = mole fraction, P in bar.
    TODO: total moles, then multiply (moles[sp] / n_tot * p_total) ** nu over the species."""
    return None


def equilibrium_extent(reaction, n0, k, p_total):
    """Extent xi (mol) at which Qp = K. Species amounts are n0[sp] + nu * xi.
    Searches between the two limits where some amount reaches zero, using ln Q - ln K."""
    lo = max(-n0[sp] / nu for sp, nu in reaction.items() if nu > 0)
    hi = min(-n0[sp] / nu for sp, nu in reaction.items() if nu < 0)
    eps = 1e-12 * (hi - lo)

    def f(xi):
        # TODO: build the ICE row (amount of each species at extent xi) as a dict, then
        # return ln Q - ln K. brentq finds the xi where this is zero.
        return None

    return brentq(f, lo + eps, hi - eps, xtol=1e-14)


def main():
    table = load_table()
    if reaction_quotient({"A": 1}, {"A": 1.0}, 1.0) is None:
        print("TODO: write reaction_quotient() and the ICE function f() first.")
        return

    # 1. Water-gas shift at 1000 K: CO + H2O <=> CO2 + H2
    wgs = {"CO(g)": -1, "H2O(g)": -1, "CO2(g)": 1, "H2(g)": 1}
    k = k_from_table(wgs, table, 1000)
    print(f"Water-gas shift at 1000 K: K = {k:.3f}")
    for steam in (1.0, 3.0):
        n0 = {"CO(g)": 1.0, "H2O(g)": steam, "CO2(g)": 0.0, "H2(g)": 0.0}
        xi = equilibrium_extent(wgs, n0, k, 1.0)
        print(f"  1 mol CO + {steam:.0f} mol H2O: {xi:.3f} mol CO converted ({100 * xi:.1f} %)")

    # 2. N2O4 <=> 2 NO2 at 298 K, starting from 1 mol N2O4, at several total pressures
    rxn = {"N2O4(g)": -1, "NO2(g)": 2}
    k = k_from_table(rxn, table, 298.15)
    print(f"\nN2O4 <=> 2 NO2 at 298 K: K = {k:.3f}")
    print(f"{'P (bar)':>8}{'alpha exact':>13}{'alpha small-x':>15}{'error %':>9}")
    pressures = np.array([0.1, 0.3, 1.0, 3.0, 10.0, 30.0])
    alphas = []
    for p in pressures:
        alpha = equilibrium_extent(rxn, {"N2O4(g)": 1.0, "NO2(g)": 0.0}, k, p)
        small = np.sqrt(k / (4 * p))   # from K = 4 alpha^2 P / (1 - alpha^2) with alpha << 1
        alphas.append(alpha)
        print(f"{p:8.1f}{alpha:13.4f}{small:15.4f}{100 * (small - alpha) / alpha:9.1f}")

    # 3. van 't Hoff: K of N2O4 dissociation at other temperatures
    dh = (2 * table["NO2(g)"]["dHf_kJ_mol"] - table["N2O4(g)"]["dHf_kJ_mol"]) * 1000
    print(f"\nvan 't Hoff with Delta H = {dh / 1000:.1f} kJ/mol:")
    for t in (273.15, 298.15, 323.15, 373.15):
        k_t = k * np.exp(-dh / R * (1 / t - 1 / 298.15))
        alpha = equilibrium_extent(rxn, {"N2O4(g)": 1.0, "NO2(g)": 0.0}, k_t, 1.0)
        print(f"  T = {t:6.1f} K  K = {k_t:8.3g}  alpha at 1 bar = {alpha:.3f}")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed: skipping the plot")
        return
    p = np.logspace(-2, 2, 60)
    exact = [equilibrium_extent(rxn, {"N2O4(g)": 1.0, "NO2(g)": 0.0}, k, pi) for pi in p]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.semilogx(p, exact, label="exact (brentq)")
    ax.semilogx(p, np.minimum(np.sqrt(k / (4 * p)), 1.5), "--", label="small-x approximation")
    ax.set_xlabel("total pressure (bar)")
    ax.set_ylabel("fraction of N2O4 dissociated")
    ax.set_ylim(0, 1.05)
    ax.legend()
    out = Path(__file__).resolve().parent / "runs"
    out.mkdir(exist_ok=True)
    fig.tight_layout()
    fig.savefig(out / "lesson03_N2O4_vs_P.png", dpi=120)
    print(f"\nplot written to {out / 'lesson03_N2O4_vs_P.png'}")


if __name__ == "__main__":
    main()
