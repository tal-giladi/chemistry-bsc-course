"""Lesson 16.6 exercise: which amines are charged in blood, and glucose mutarotation.

Run (from this folder):
    py lesson06_amines_sugars.py
    py lesson06_amines_sugars.py my_polarimeter.csv     # your own t_min,alpha_deg data
"""
import math
import sys

import numpy as np
from scipy.optimize import curve_fit

from org16 import Chem, attempt, check_drill, mol, read_csv

ALPHA_PURE, BETA_PURE = 112.2, 18.7  # specific rotations of the pure anomers, OpenStax 25.5
# PubChem isomeric SMILES (accessed 2026-10-17): CID 79025 alpha-D-glucopyranose,
# CID 64689 beta-D-glucopyranose, CID 107526 open-chain (aldehydo) D-glucose.
GLUCOSE = {"alpha-D-glucopyranose": "C([C@@H]1[C@H]([C@@H]([C@H]([C@H](O1)O)O)O)O)O",
           "beta-D-glucopyranose": "C([C@@H]1[C@H]([C@@H]([C@H]([C@@H](O1)O)O)O)O)O",
           "open-chain D-glucose": "C([C@H]([C@H]([C@@H]([C@H](C=O)O)O)O)O)O"}


def percent_protonated(pkah, ph):
    """Percentage of an amine present as its ammonium ion (BH+) at this pH."""
    # TODO: [B]/[BH+] = 10**(pH - pKaH), so the protonated fraction is 1 / (1 + 10**(pH - pKaH)).
    raise NotImplementedError("write this part")


def model(t, a_eq, a0, k):
    return a_eq + (a0 - a_eq) * np.exp(-k * t)


def fit_mutarotation(t, a):
    """Fit the first-order approach to equilibrium. Returns (a_eq, a0, k in min^-1)."""
    # TODO: use curve_fit(model, t, a, p0=[a[-1], a[0], 0.01]) and return the three fitted parameters.
    raise NotImplementedError("write this part")


def beta_fraction(a_eq):
    """Fraction of beta anomer at equilibrium from the rotations (the open chain is under 0.1 %)."""
    # TODO: a_eq = x_beta * BETA_PURE + (1 - x_beta) * ALPHA_PURE; solve for x_beta.
    raise NotImplementedError("write this part")


ANSWERS = {
    "a cyclohexanone + NH3, then NaBH3CN": "",
    "b benzaldehyde + dimethylamine, then NaBH3CN": "",
    "c aniline + acetic anhydride": "",
    "d nitrobenzene + Fe, HCl, then NaOH": "",
    "e D-glucose + methanol, HCl catalyst (any anomer; stereo ignored)": "",
}
KEYS = {
    "a cyclohexanone + NH3, then NaBH3CN": "1ab5212917da36f9",
    "b benzaldehyde + dimethylamine, then NaBH3CN": "7bb0415c98ac6e17",
    "c aniline + acetic anhydride": "e9d92b28db6a4f52",
    "d nitrobenzene + Fe, HCl, then NaOH": "21e9e6150c40c857",
    "e D-glucose + methanol, HCl catalyst (any anomer; stereo ignored)": "a5c3695a320acedd",
}


def main():
    print("Amines: % protonated (BH+) in blood at pH 7.4")
    for r in read_csv("amines_pka.csv"):
        p = attempt(percent_protonated, float(r["pKaH"]), 7.4)
        print(f"  {r['name']:14s} pKaH {float(r['pKaH']):5.2f}  {p if p == 'TODO' else f'{p:8.3f} %'}")

    print("\nGlucose: stereocentres (RDKit, CIP labels)")
    for name, smi in GLUCOSE.items():
        centres = Chem.FindMolChiralCenters(mol(smi), includeUnassigned=True, useLegacyImplementation=False)
        print(f"  {name:22s} {len(centres)} stereocentres {centres}")

    path = sys.argv[1] if len(sys.argv) > 1 else "mutarotation_example.csv"
    rows = read_csv(path)
    t = np.array([float(r["t_min"]) for r in rows])
    a = np.array([float(r["alpha_deg"]) for r in rows])
    fit = attempt(fit_mutarotation, t, a, default=None)
    print(f"\nMutarotation fit of {path}")
    if fit is None:
        print("  TODO: write fit_mutarotation()")
    else:
        a_eq, a0, k = fit
        print(f"  a_eq = {a_eq:.1f}, a0 = {a0:.1f}, k = {k:.4f} min^-1, half-life = {math.log(2) / k:.0f} min")
        xb = attempt(beta_fraction, a_eq)
        if xb != "TODO":
            print(f"  equilibrium: {100 * xb:.0f} % beta, {100 * (1 - xb):.0f} % alpha (OpenStax: 63 : 37)")
    print("\nProduct drill")
    check_drill(ANSWERS, KEYS)


if __name__ == "__main__":
    main()
