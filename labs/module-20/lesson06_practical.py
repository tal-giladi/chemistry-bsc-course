"""Lesson 20.6 - module practical.

Part 1  HCl and CO side by side from NIST data: band centre, rotational constants, bond length, force constant.
Part 2  Point groups of the ten practical molecules (uses your point_group() from lesson 20.5).
Part 3  Normal modes by the reduction formula: how many IR and Raman bands, checked against NIST.

Fill in the functions marked TODO, then run:  py lesson06_practical.py
Reference solution: lesson06_practical_solution.py
"""
import math

import numpy as np

from lesson02_rotor import fit_B_D, load_lines
from lesson03_hcl_band import assign_branches, fit_band, force_constant, load_peaks
from lesson05_pointgroups import point_group
from molecules20 import EXPECTED, PRACTICAL
from spec20 import B_v, G, HC_K, TABLES, bond_length_from_B, read_csv, reduced_mass, symmetry_elements

T_ROOM = 298.15
CO_BRANCH_MAXIMA = (2119.5, 2176.0)   # cm-1, read from the NIST CO spectrum (Coblentz 8755), see lesson 20.3

# Unmoved atoms under one operation of each class, in the class order of spec20.TABLES[group].
UNMOVED = {
    "H2O": ("C2v", [3, 1, 3, 1]),                  # molecule in the xz plane (NIST convention)
    "NH3": ("C3v", [4, 1, 2]),
    "CH4": ("Td", [5, 2, 1, 1, 3]),
    "CCl4": ("Td", [5, 2, 1, 1, 3]),
    "C2H4": ("D2h", [6, 0, 0, 2, 0, 6, 2, 0]),     # x along C=C, z perpendicular to the plane
    "trans-C2H2Cl2": ("C2h", [6, 0, 0, 6]),
    "BF3": ("D3h", [4, 1, 2, 4, 1, 2]),
    "XeF4": ("D4h", None),   # TODO: unmoved atoms for E, 2C4, C2, 2C2', 2C2'', i, 2S4, sh, 2sv, 2sd
    "SF6": ("Oh", None),     # TODO: unmoved atoms for E, 8C3, 6C2, 6C4, 3C2, i, 6S4, 8S6, 3sh, 6sd
}


def gamma_3n(group, unmoved):
    """Characters of the 3N Cartesian representation: unmoved atoms x contribution per atom."""
    # TODO: chi(R) = (number of unmoved atoms) x (contribution per atom), class by class.
    # TODO: The contribution is the third entry of each class tuple in TABLES[group]['classes'] (E 3, C2 -1, sigma 1, i -3, ...)
    return None


def reduce(chars, group):
    """Reduction formula n_i = (1/h) sum_k g_k chi(k) chi_i(k). Returns {irrep: n_i} (n_i > 0 only)."""
    # TODO: t = TABLES[group]; g = class sizes; h = sum(g)
    # TODO: for each irrep (name, chi_i, linear, quadratic): n_i = sum(g * chars * chi_i) / h
    # TODO: return {name: n_i} for the irreps with n_i > 0 (round to integers)
    return None


def trans_rot(group):
    """Irreps of the three translations and three rotations, from the linear-function column."""
    out = {}
    for name, chi, lin, _ in TABLES[group]["irreps"]:
        f = [s for s in lin.split(",") if s]
        k = (sum(s in ("x", "y", "z") for s in f) + sum(s in ("Rx", "Ry", "Rz") for s in f)) // chi[0]
        if k:
            out[name] = k
    return out


def vibrations(group, unmoved):
    """Gamma_vib = Gamma_3N - Gamma_trans - Gamma_rot."""
    full = reduce(gamma_3n(group, unmoved), group)
    for name, k in trans_rot(group).items():
        full[name] -= k
    return {k: v for k, v in full.items() if v}


def activity(group, irrep):
    """(IR active, Raman active): IR if the irrep contains x, y or z; Raman if it contains a quadratic function."""
    # TODO: find the irrep in TABLES[group]['irreps']: (name, characters, linear, quadratic)
    # TODO: IR active if linear contains x, y or z (split on commas); Raman active if quadratic is not empty
    # TODO: return (ir, raman)
    return None


def nist_species():
    """{molecule: {species: count}} from nist_fundamentals.csv, with labels in this lab's style (f2 -> T2)."""
    out = {}
    for r in read_csv("nist_fundamentals.csv"):
        s = r["species"]
        s = s[0].upper().replace("F", "T") + s[1:]
        out.setdefault(r["molecule"], {})
        out[r["molecule"]][s] = out[r["molecule"]].get(s, 0) + 1
    return out


def part1():
    print("PART 1 - HCl and CO from NIST data")
    peaks, _ = load_peaks()
    peaks, m = assign_branches(peaks)
    nu0, B0, B1 = fit_band(peaks, m)
    mu_hcl = reduced_mass("H", "35Cl")
    Be = B0 + (B0 - B1) / 2
    J, nu = load_lines("12C16O")
    B0_co, D_co = fit_B_D(J, nu)
    mu_co = reduced_mass("C", "O")
    nu0_co = G("CO", 1) - G("CO", 0)
    dPR = CO_BRANCH_MAXIMA[1] - CO_BRANCH_MAXIMA[0]
    B_env = dPR**2 / (8 * T_ROOM / HC_K)
    print(f"{'':28s}{'HCl (IR band)':>16s}{'CO (microwave + IR)':>22s}")
    print(f"{'band centre nu0 / cm-1':28s}{nu0:16.1f}{nu0_co:22.1f}")
    print(f"{'B0 / cm-1':28s}{B0:16.3f}{B0_co:22.5f}")
    print(f"{'B1 / cm-1':28s}{B1:16.3f}{B_v('CO', 1):22.5f}  (CO B1 from NIST constants)")
    print(f"{'r0 / A':28s}{bond_length_from_B(B0, mu_hcl):16.4f}{bond_length_from_B(B0_co, mu_co):22.5f}")
    print(f"{'re / A':28s}{bond_length_from_B(Be, mu_hcl):16.4f}{bond_length_from_B(B_v('CO', -0.5), mu_co):22.5f}")
    print(f"{'k from nu0 / N m-1':28s}{force_constant(nu0, mu_hcl):16.0f}{force_constant(nu0_co, mu_co):22.0f}")
    print(f"CO branch maxima {CO_BRANCH_MAXIMA} -> B = {B_env:.3f} cm-1 at {T_ROOM} K "
          f"(microwave {B0_co:.4f}); implied T = {dPR**2 / (8 * B0_co) * HC_K:.0f} K\n")


def part2():
    print("PART 2 - point groups of the ten practical molecules")
    ok = 0
    for name, mol in PRACTICAL.items():
        pg = point_group(symmetry_elements(mol))
        ok += pg == EXPECTED[name]
        print(f"  {name:16s} {pg:6s} {'OK' if pg == EXPECTED[name] else 'expected ' + EXPECTED[name]}")
    print(f"  {ok}/{len(PRACTICAL)} correct\n")


def part3():
    print("PART 3 - normal modes, IR and Raman activity")
    nist = nist_species()
    for mol, (group, unmoved) in UNMOVED.items():
        if unmoved is None:
            print(f"  {mol:14s} TODO: fill in the unmoved atoms in UNMOVED")
            continue
        vib = vibrations(group, unmoved)
        n_modes = sum(k * TABLES[group]["irreps"][[i[0] for i in TABLES[group]["irreps"]].index(s)][1][0]
                      for s, k in vib.items())
        ir = sum(k for s, k in vib.items() if activity(group, s)[0])
        ra = sum(k for s, k in vib.items() if activity(group, s)[1])
        both = sum(k for s, k in vib.items() if all(activity(group, s)))
        text = " + ".join(f"{k if k > 1 else ''}{s}" for s, k in vib.items())
        check = ""
        if mol in nist:
            check = "NIST agrees" if nist[mol] == vib else f"NIST {nist[mol]}"
        print(f"  {mol:14s} {group:4s} {text:38s} {n_modes:2d} modes; IR {ir}, Raman {ra}, both {both}  {check}")


def main():
    if gamma_3n("C2v", [3, 1, 3, 1]) is None or reduce([9, -1, 3, 1], "C2v") is None or activity("C2v", "A1") is None:
        print("TODO: write gamma_3n(), reduce() and activity() first (and point_group() in lesson05_pointgroups.py).")
        return
    part1()
    part2()
    part3()


if __name__ == "__main__":
    main()
