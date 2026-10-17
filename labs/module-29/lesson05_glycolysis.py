"""Lesson 29.5 Part A - exercise: which steps of glycolysis are far from equilibrium in a red cell?

Fill in the functions marked TODO, then run:  py lesson05_glycolysis.py
Reference solution: lesson05_glycolysis_solution.py
Writes runs/lesson05_glycolysis.png.
dG = dG0' + RT ln Q at 37 C, with dG0' from glycolysis_steps.csv and concentrations from rbc_metabolites.csv.
"""
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from enz29 import R, T37, read_csv, runs_dir


def load_concentrations():
    """Species -> concentration in mol/L (the file is in mM)."""
    return {r["species"]: float(r["conc_mM"]) / 1000 for r in read_csv("rbc_metabolites.csv")}


def ln_Q(substrates, products, conc):
    """ln of the reaction quotient, standard state 1 M (water and H+ are already in dG0')."""
    # TODO: return sum(math.log(conc[s]) for s in products) - sum(math.log(conc[s]) for s in substrates)
    raise NotImplementedError("TODO: write ln_Q() first (see the hints in the code).")


def dG_actual(dG0_kJ, lnQ, T=T37):
    """dG = dG0' + RT ln Q, kJ/mol."""
    # TODO: return dG0_kJ + R * T * lnQ / 1000
    raise NotImplementedError("TODO: write dG_actual() first (see the hints in the code).")


def main():
    conc = load_concentrations()
    steps = read_csv("glycolysis_steps.csv")
    names, g0s, gs = [], [], []
    print(f"{'step':>4} {'enzyme':42s} {'dG0prime':>9} {'dG(cell)':>9}   kJ/mol")
    for r in steps:
        lnq = ln_Q(r["substrates"].split(";"), r["products"].split(";"), conc)
        g0 = float(r["dG0prime_kJ_per_mol"])
        g = dG_actual(g0, lnq)
        names.append(f"{r['step']} {r['enzyme']}"); g0s.append(g0); gs.append(g)
        flag = "  far from equilibrium" if g < -10 else ""
        print(f"{r['step']:>4} {r['enzyme']:42s} {g0:9.1f} {g:9.1f}{flag}")
    gs = np.array(gs); g0s = np.array(g0s)
    # steps 6-10 happen twice per glucose (two trioses)
    per_glucose = gs[:5].sum() + 2 * gs[5:].sum()
    print(f"\nSum per glucose (steps 6-10 counted twice): {per_glucose:.0f} kJ/mol")
    print(f"Steps 6 + 7 together: {gs[5] + gs[6]:.1f} kJ/mol")
    K_tpi = math.exp(-7.5e3 / (R * T37))
    print(f"TPI: K = [GAP]/[DHAP] = {K_tpi:.3f} at equilibrium; in the cell {conc['GAP'] / conc['DHAP']:.3f}")

    fig, ax = plt.subplots(figsize=(9, 4))
    x = np.arange(len(gs))
    ax.bar(x - 0.2, g0s, 0.4, label="dG0' (standard)")
    ax.bar(x + 0.2, gs, 0.4, label="dG in the red cell")
    ax.axhline(0, c="k", lw=0.5)
    ax.set_xticks(x, [n.split()[0] for n in names])
    ax.set_xlabel("glycolysis step"); ax.set_ylabel("kJ/mol"); ax.legend()
    fig.tight_layout(); fig.savefig(runs_dir() / "lesson05_glycolysis.png", dpi=120)
    print("saved runs/lesson05_glycolysis.png")


if __name__ == "__main__":
    try:
        main()
    except NotImplementedError as e:
        print(e)
