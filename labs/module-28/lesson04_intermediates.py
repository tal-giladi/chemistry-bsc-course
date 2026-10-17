"""Lesson 28.4 - putting numbers on reactive intermediates.

Fill in the functions marked TODO, then run:  py lesson04_intermediates.py
Reference solution: lesson04_intermediates_solution.py
Writes runs/lesson04_intermediates.png.
1. Radical stabilisation energies from C-H bond enthalpies (sr28.BDE).
2. Carbocations: SN1 solvolysis of para-substituted cumyl chlorides, rho = -4.54 (Brown and Okamoto 1958),
   predicted with sigma_p+ and, wrongly, with sigma_p.
3. Carbenes: singlet/triplet populations for a triplet ground state 33 kJ/mol below the singlet
   (typical for simple hydrocarbon carbenes, Chemistry LibreTexts 'Carbenes').
"""
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sr28 import BDE, R, runs_dir, sigma_table

T = 298.15
RHO_CUMYL = -4.54
RADICALS = ["CH3CH2-H", "(CH3)2CH-H", "(CH3)3C-H", "C6H5CH2-H", "CH2=CHCH2-H", "CH2=CH-H", "C6H5-H"]


def rse(bond):
    """Radical stabilisation energy (kJ/mol): how much weaker R-H is than CH3-H."""
    # TODO: return BDE["CH3-H"] - BDE[bond]   (positive = the radical is more stable than methyl)
    raise NotImplementedError("TODO: write rse() first (see the hints in the code).")


def hammett_factor(rho, sigma):
    """k_X / k_H from log10(k_X/k_H) = rho * sigma."""
    # TODO: the Hammett equation gives log10 of the ratio; return 10 ** (rho * sigma)
    raise NotImplementedError("TODO: write hammett_factor() first (see the hints in the code).")


def singlet_fraction(gap_kj, T=T, g_singlet=1, g_triplet=3):
    """Fraction of carbene molecules in the singlet when the triplet lies gap_kj below it."""
    # TODO: Boltzmann weights (lesson 21.1): triplet g_triplet * 1 (it is the ground state),
    # TODO: singlet g_singlet * exp(-gap / RT) with the gap in J/mol; return singlet / (singlet + triplet)
    raise NotImplementedError("TODO: write singlet_fraction() first (see the hints in the code).")


def main():
    print("Radical stabilisation energies (RSE = BDE(CH3-H) - BDE(R-H)), kJ/mol:")
    names, values = [], []
    for b in RADICALS:
        names.append(b.replace("-H", "."))
        values.append(rse(b))
        print(f"  {b:14s} BDE {BDE[b]:6.1f}  RSE {rse(b):+6.1f}")

    sig = sigma_table()
    print(f"Cumyl chloride solvolysis, rho = {RHO_CUMYL}: k_X/k_H")
    for X in ("OCH3", "CH3", "F", "Cl", "Br", "CF3", "NO2"):
        f_plus = hammett_factor(RHO_CUMYL, sig[X]["p+"])
        f_norm = hammett_factor(RHO_CUMYL, sig[X]["p"])
        print(f"  p-{X:5s} sigma_p+ {sig[X]['p+']:+.2f} -> {f_plus:9.3g}   (sigma_p {sig[X]['p']:+.2f} would give {f_norm:8.3g})")

    gap = 33.0
    fs = singlet_fraction(gap)
    print(f"Carbene, triplet {gap:.0f} kJ/mol below singlet: singlet fraction at 298 K = {fs:.2e}")
    print(f"If the singlet reacts 1e6 times faster than the triplet, its share of the product "
          f"= {fs * 1e6 / (fs * 1e6 + (1 - fs)):.2f} (as long as the two interconvert faster than they react)")

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.barh(names, values, color=["C0" if v >= 0 else "C3" for v in values])
    ax.axvline(0, color="k", lw=0.8)
    ax.set(xlabel="radical stabilisation energy (kJ/mol, relative to CH3.)",
           title="Radical stability from C-H bond enthalpies (298 K)")
    fig.tight_layout()
    out = runs_dir() / "lesson04_intermediates.png"
    fig.savefig(out, dpi=120)
    print(f"Saved {out.name}")


if __name__ == "__main__":
    main()
