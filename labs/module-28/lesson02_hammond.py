"""Lesson 28.2 - the Hammond postulate made quantitative.

Fill in the functions marked TODO, then run:  py lesson02_hammond.py
Reference solution: lesson02_hammond_solution.py
Writes runs/lesson02_hammond.png.
Data: light-induced halogenation of propane at 25 C (Chemistry LibreTexts, Morsch and Andrews,
15.06 Chlorination versus Bromination): chlorination 45 % 1-chloro- and 55 % 2-chloropropane,
bromination 3 % 1-bromo- and 97 % 2-bromopropane. Bond enthalpies in sr28.BDE.
"""
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from sr28 import BDE, R, runs_dir

T = 298.15
PROPANE = {"Cl": (45.0, 55.0), "Br": (3.0, 97.0)}   # % primary product, % secondary product
N_PRIMARY_H, N_SECONDARY_H = 6, 2


def per_h_selectivity(pct_primary, pct_secondary, n_primary=N_PRIMARY_H, n_secondary=N_SECONDARY_H):
    """Reactivity of one secondary H relative to one primary H."""
    # TODO: divide each product percentage by the number of H atoms that give it, then take the ratio
    raise NotImplementedError("TODO: write per_h_selectivity() first (see the hints in the code).")


def ddg_barrier(selectivity, T=T):
    """Difference in free energy of activation (kJ/mol) that gives this rate ratio."""
    # TODO: rate ratio = exp(ddG / RT), so ddG = R T ln(ratio); return it in kJ/mol (R is in J/(mol K))
    raise NotImplementedError("TODO: write ddg_barrier() first (see the hints in the code).")


def abstraction_enthalpy(ch_bond, hx_bond):
    """Enthalpy (kJ/mol) of X. + R-H -> HX + R. : bond broken minus bond made."""
    return BDE[ch_bond] - BDE[hx_bond]


def leffler_alpha(ddg_barrier_kj, ddh_reaction_kj):
    """Fraction of the change in reaction enthalpy that shows up in the barrier (0 = early TS, 1 = late)."""
    # TODO: alpha = (change in barrier) / (change in reaction enthalpy)
    raise NotImplementedError("TODO: write leffler_alpha() first (see the hints in the code).")


def marcus_barrier(dG0, lam):
    """Marcus: dG(barrier) = (lam/4)(1 + dG0/lam)^2, all in kJ/mol."""
    return lam / 4 * (1 + dG0 / lam) ** 2


def marcus_alpha(dG0, lam):
    """Slope d(barrier)/d(dG0) = (1 + dG0/lam)/2, the Marcus measure of transition-state position."""
    # TODO: differentiate marcus_barrier() with respect to dG0: (1 + dG0/lam)/2
    raise NotImplementedError("TODO: write marcus_alpha() first (see the hints in the code).")


def main():
    ddh_radicals = BDE["CH3CH2-H"] - BDE["(CH3)2CH-H"]
    print(f"Secondary radical is {ddh_radicals:.1f} kJ/mol more stable than primary (from C-H bond enthalpies)")
    alphas = {}
    for X, (p1, p2) in PROPANE.items():
        s = per_h_selectivity(p1, p2)
        dd = ddg_barrier(s)
        h1 = abstraction_enthalpy("CH3CH2-H", f"H-{X}")
        h2 = abstraction_enthalpy("(CH3)2CH-H", f"H-{X}")
        alphas[X] = leffler_alpha(dd, ddh_radicals)
        print(f"{X}: per-H selectivity 2/1 = {s:5.1f}; ddG(barrier) = {dd:5.2f} kJ/mol; "
              f"dH(abstraction) primary {h1:+6.1f}, secondary {h2:+6.1f} kJ/mol; alpha = {alphas[X]:.2f}")

    # Prediction for 2-methylpropane (9 primary H, 1 tertiary H), using each halogen's alpha
    ddh_t = BDE["CH3CH2-H"] - BDE["(CH3)3C-H"]
    for X, a in alphas.items():
        s = math.exp(a * ddh_t * 1000 / (R * T))
        frac_t = s * 1 / (s * 1 + 9)
        print(f"Estimate for 2-methylpropane + {X}: per-H tertiary/primary {s:7.0f}, tertiary product {100 * frac_t:5.1f} %")

    lam = 60.0
    dG0 = np.linspace(-50, 50, 201)
    for X in PROPANE:
        h2 = abstraction_enthalpy("(CH3)2CH-H", f"H-{X}")
        print(f"Marcus (lambda = {lam:.0f} kJ/mol): {X} step dG0 ~ {h2:+.0f} -> barrier {marcus_barrier(h2, lam):5.1f} kJ/mol, "
              f"alpha {marcus_alpha(h2, lam):.2f}")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    ax1.plot(dG0, marcus_barrier(dG0, lam))
    ax1.set(xlabel="reaction free energy dG0 (kJ/mol)", ylabel="barrier (kJ/mol)",
            title=f"Marcus barrier, lambda = {lam:.0f} kJ/mol")
    ax2.plot(dG0, marcus_alpha(dG0, lam))
    for X in PROPANE:
        h2 = abstraction_enthalpy("(CH3)2CH-H", f"H-{X}")
        ax2.plot(h2, marcus_alpha(h2, lam), "o")
        ax2.annotate(f"{X} (model)", (h2, marcus_alpha(h2, lam)), xytext=(5, -12), textcoords="offset points")
        ax2.plot(h2, alphas[X], "kx")
        ax2.annotate(f"{X} (data)", (h2, alphas[X]), xytext=(5, 5), textcoords="offset points")
    ax2.axhline(0.5, color="grey", lw=0.8)
    ax2.set(xlabel="reaction free energy dG0 (kJ/mol)", ylabel="alpha (0 early, 1 late)",
            title="Transition-state position (Hammond)")
    fig.tight_layout()
    out = runs_dir() / "lesson02_hammond.png"
    fig.savefig(out, dpi=120)
    print(f"Saved {out.name}")


if __name__ == "__main__":
    main()
