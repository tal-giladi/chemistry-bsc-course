"""Lesson 29.4 - reference solution: the serine-protease active site and a pH-rate profile.

Run:  py lesson04_mechanism_solution.py            (uses data/4CHA_site.pdb)
      py lesson04_mechanism_solution.py data/downloaded/4CHA.pdb   (the full entry, after py fetch_pdb.py 4CHA)
Writes runs/lesson04_mechanism.png.
Part 1: catalytic triad and oxyanion-hole distances in alpha-chymotrypsin (PDB 4CHA, 1.68 A).
Part 2: fit a bell-shaped pH-rate profile of kcat/Km and read the two pKa values.
"""
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

from enz29 import column, find_atom, read_pdb, read_csv, runs_dir


def distance(a, b):
    return float(np.linalg.norm(a["xyz"] - b["xyz"]))


def triad_distances(atoms):
    """Key distances (Angstrom) of the chymotrypsin active site."""
    og = find_atom(atoms, "SER", 195, "OG")
    ne2 = find_atom(atoms, "HIS", 57, "NE2")
    nd1 = find_atom(atoms, "HIS", 57, "ND1")
    od = min((find_atom(atoms, "ASP", 102, n) for n in ("OD1", "OD2")), key=lambda a: distance(a, nd1))
    n193 = find_atom(atoms, "GLY", 193, "N")
    n195 = find_atom(atoms, "SER", 195, "N")
    return {"Ser195 OG - His57 NE2": distance(og, ne2),
            f"His57 ND1 - Asp102 {od['name']}": distance(nd1, od),
            "Gly193 N - Ser195 N (oxyanion hole)": distance(n193, n195),
            "Ser195 OG - Gly193 N": distance(og, n193)}


def log_bell(pH, log_kmax, pKa1, pKa2):
    """log10 of kcat/Km = kmax / (1 + 10^(pKa1 - pH) + 10^(pH - pKa2))."""
    return log_kmax - np.log10(1 + 10 ** (pKa1 - pH) + 10 ** (pH - pKa2))


def fit_ph_profile(pH, k):
    popt, pcov = curve_fit(log_bell, pH, np.log10(k), p0=(np.log10(k.max()), 6.5, 9.0))
    return popt, np.sqrt(np.diag(pcov))


def fraction_active(pH, pKa1, pKa2):
    """Fraction of enzyme with His57 neutral AND the second group protonated."""
    return 1 / (1 + 10 ** (pKa1 - pH) + 10 ** (pH - pKa2))


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "4CHA_site.pdb"
    atoms = read_pdb(path)
    print(f"Part 1: {path}, {len(atoms)} atoms")
    for name, d in triad_distances(atoms).items():
        print(f"  {name:38s} {d:.2f} A")

    rows = read_csv("chymotrypsin_ph_rate.csv")
    pH = column(rows, "pH")
    k = column(rows, "kcat_over_Km_per_M_per_s")
    (lk, p1, p2), (slk, sp1, sp2) = fit_ph_profile(pH, k)
    print("\nPart 2: pH-rate profile of kcat/Km")
    print(f"  kmax = {10 ** lk:.2e} M^-1 s^-1, pKa1 = {p1:.2f} +/- {sp1:.2f}, pKa2 = {p2:.2f} +/- {sp2:.2f}")
    for x in (6.0, 7.4, 8.0):
        print(f"  active fraction at pH {x}: {fraction_active(x, p1, p2):.2f}")
    print(f"  pH optimum = (pKa1 + pKa2)/2 = {(p1 + p2) / 2:.1f}")

    fig, ax = plt.subplots(figsize=(6, 4))
    xx = np.linspace(4.5, 11, 200)
    ax.plot(pH, np.log10(k), "o", label="data (generated)")
    ax.plot(xx, log_bell(xx, lk, p1, p2), "-", label=f"fit: pKa {p1:.1f} and {p2:.1f}")
    ax.set_xlabel("pH"); ax.set_ylabel("log10(kcat/Km / M$^{-1}$ s$^{-1}$)"); ax.legend()
    fig.tight_layout(); fig.savefig(runs_dir() / "lesson04_mechanism.png", dpi=120)
    print("saved runs/lesson04_mechanism.png")


if __name__ == "__main__":
    main()
