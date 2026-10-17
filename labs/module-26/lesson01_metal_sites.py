"""Lesson 26.1 - metal sites in real proteins, and why iron is hard to get.

Fill in the functions marked TODO, then run:  py lesson01_metal_sites.py
Reference solution: lesson01_metal_sites_solution.py
Reads the trimmed structures in data/ (or any PDB file you pass), prints each metal's donor set.
"""
import sys

import numpy as np

from bio26 import DATA, METALS, N_A, label, read_pdb

# Largest metal-donor distance (angstrom) that still counts as a bond. Ca2+ is larger, and
# sulfur donors (Cys, Met) sit further out than N or O.
CUTOFF = {"CA": 2.9, "default": 2.5}
CUTOFF_S = 3.0
STRUCTURES = {
    "1A6M_sites.pdb": "oxy-myoglobin, sperm whale (Fe)",
    "3KS3_sites.pdb": "carbonic anhydrase II, human (Zn)",
    "1CLL_sites.pdb": "calmodulin, human (Ca)",
    "1PLC_sites.pdb": "plastocyanin, poplar (Cu)",
}


def distance(a, b):
    """Distance in angstrom between two atoms (their 'xyz' arrays)."""
    # TODO: return the length of a["xyz"] - b["xyz"]   (np.linalg.norm)
    return None


def donors(atoms, metal):
    """N, O and S atoms bonded to `metal`, as a list of (atom, distance) sorted by distance."""
    # TODO: for every atom that is not the metal and whose element is N, O or S, compute the distance;
    # keep it if distance < CUTOFF.get(metal["el"], CUTOFF["default"]) (for S use max(that, CUTOFF_S)).
    # Return the kept pairs sorted by distance.
    return None


def free_fe3(pH, ksp=1e-39, kw=1e-14):
    """Free [Fe3+] (mol/L) in equilibrium with Fe(OH)3: Ksp = [Fe3+][OH-]^3."""
    # TODO: [OH-] = kw / 10**(-pH); return ksp / [OH-]**3
    return None


def describe(path, title=""):
    atoms = read_pdb(path)
    metals = [a for a in atoms if a["el"] in METALS and a["rec"] == "HETATM"]
    print(f"\n{path.name}  {title}")
    for m in metals:
        ds = donors(atoms, m)
        kinds = "".join(sorted(a["el"] for a, _ in ds))
        print(f"  {m['el']:2s} chain {m['chain']}  CN = {len(ds)}  donors {kinds:8s} "
              + ", ".join(f"{label(a)} {d:.2f}" for a, d in ds))


def main():
    probe = dict(el="FE", xyz=np.zeros(3)), dict(el="N", xyz=np.array([2.0, 0.0, 0.0]))
    if distance(*probe) is None or donors([probe[1]], probe[0]) is None or free_fe3(7.0) is None:
        print("TODO: write distance(), donors() and free_fe3() first.")
        return
    if len(sys.argv) > 1:
        from pathlib import Path
        describe(Path(sys.argv[1]))
        return
    for name, title in STRUCTURES.items():
        describe(DATA / name, title)

    print("\nIron(III) at equilibrium with Fe(OH)3 (Ksp = 1e-39):")
    for pH in (2.0, 4.0, 7.0, 8.1):
        print(f"  pH {pH:4.1f}: [Fe3+] = {free_fe3(pH):.1e} M")
    cell_L = 1e-15   # a bacterium of about 1 femtolitre
    n = free_fe3(7.0) * cell_L * N_A
    print(f"  free Fe3+ ions in 1 fL at pH 7: {n:.1e}  (one ion per {1 / n:.1e} cells)")


if __name__ == "__main__":
    main()
