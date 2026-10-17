"""Lesson 08.2 hands-on, reference solution: free energy, crossover temperature and K.

Run:   py lesson02_free_energy_solution.py
Data:  thermo_data.csv (OpenStax Chemistry 2e Appendix G).
Writes runs/lesson02_dG_vs_T.png.
Approximation: Delta H and Delta S are taken as constant with temperature (good to a few kJ/mol
over a few hundred kelvin; Module 13 removes it).
"""
from pathlib import Path

import numpy as np

from thermo import load_table

R = 8.314462618   # J/(mol K), CODATA 2022 (exact in the SI)
T0 = 298.15       # K

REACTIONS = {
    "NH4NO3 dissolving":  {"NH4NO3(s)": -1, "NH4+(aq)": 1, "NO3-(aq)": 1},
    "NH3 synthesis":      {"N2(g)": -1, "H2(g)": -3, "NH3(g)": 2},
    "N2O4 -> 2 NO2":      {"N2O4(g)": -1, "NO2(g)": 2},
    "water evaporation":  {"H2O(l)": -1, "H2O(g)": 1},
}


def reaction_value(reaction, table, column):
    return sum(nu * table[sp][column] for sp, nu in reaction.items())


def delta_g(dh_kj, ds_j, t):
    """Delta G (kJ/mol) = Delta H - T Delta S, with Delta S given in J/(mol K)."""
    return dh_kj - t * ds_j / 1000


def crossover_t(dh_kj, ds_j):
    """Temperature (K) where Delta G = 0, or None if Delta H and Delta S have opposite signs."""
    if dh_kj * ds_j <= 0:
        return None
    return dh_kj * 1000 / ds_j


def equilibrium_constant(dg_kj, t):
    """K = exp(-Delta G / RT)."""
    return float(np.exp(-dg_kj * 1000 / (R * t)))


def main():
    table = load_table()
    print(f"{'reaction':<20}{'dH kJ':>9}{'dS J/K':>9}{'dG(298) kJ':>12}{'from dGf':>10}{'T* (K)':>9}{'K(298)':>11}")
    curves = {}
    for name, rxn in REACTIONS.items():
        dh = reaction_value(rxn, table, "dHf_kJ_mol")
        ds = reaction_value(rxn, table, "S_J_molK")
        dg = delta_g(dh, ds, T0)
        dg_f = reaction_value(rxn, table, "dGf_kJ_mol")
        tx = crossover_t(dh, ds)
        k = equilibrium_constant(dg, T0)
        tx_s = f"{tx:9.0f}" if tx else f"{'none':>9}"
        print(f"{name:<20}{dh:9.1f}{ds:9.1f}{dg:12.2f}{dg_f:10.2f}{tx_s}{k:11.3g}")
        curves[name] = (dh, ds)

    print("\nNH3 synthesis at higher temperature (why industry needs a catalyst, not heat alone):")
    dh, ds = curves["NH3 synthesis"]
    for t in (298.15, 400, 500, 700):
        dg = delta_g(dh, ds, t)
        print(f"  T = {t:6.1f} K  dG = {dg:7.2f} kJ/mol  K = {equilibrium_constant(dg, t):.3g}")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed: skipping the plot")
        return
    t = np.linspace(200, 800, 200)
    fig, ax = plt.subplots(figsize=(6, 4))
    for name, (dh, ds) in curves.items():
        ax.plot(t, delta_g(dh, ds, t), label=name)
    ax.axhline(0, color="k", lw=0.8)
    ax.set_xlabel("T (K)")
    ax.set_ylabel("Delta G (kJ/mol)")
    ax.legend()
    ax.set_title("Delta G = Delta H - T Delta S (constant Delta H, Delta S)")
    out = Path(__file__).resolve().parent / "runs"
    out.mkdir(exist_ok=True)
    fig.tight_layout()
    fig.savefig(out / "lesson02_dG_vs_T.png", dpi=120)
    print(f"\nplot written to {out / 'lesson02_dG_vs_T.png'}")


if __name__ == "__main__":
    main()
