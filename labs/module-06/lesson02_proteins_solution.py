"""Lesson 06.2 reference solution: the charge of a protein against pH, and its backbone
hydrogen bonds counted from a real crystal structure.

Run:   py lesson02_proteins_solution.py                       (ubiquitin, PDB 1UBQ)
       py lesson02_proteins_solution.py data/downloaded/XXXX.pdb   (any PDB file, chain A)
The plot is saved to runs/lesson02_charge.png next to this file.
"""
import sys
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent

THREE_TO_ONE = {"ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C", "GLN": "Q", "GLU": "E",
                "GLY": "G", "HIS": "H", "ILE": "I", "LEU": "L", "LYS": "K", "MET": "M", "PHE": "F",
                "PRO": "P", "SER": "S", "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V"}

# pKa values of the EMBOSS iep program (Epk.dat). Other tables differ by a few tenths.
PKA_POS = {"Nterm": 8.6, "K": 10.8, "R": 12.5, "H": 6.5}
PKA_NEG = {"Cterm": 3.6, "D": 3.9, "E": 4.1, "C": 8.5, "Y": 10.1}

KCAL = 4.184   # kJ per kcal


def net_charge(seq, pH):
    """Net charge of a peptide or protein (one-letter sequence) at a given pH.
    Each basic group carries +1/(1 + 10^(pH - pKa)), each acidic group -1/(1 + 10^(pKa - pH)).
    Count the N- and C-terminus once each."""
    pos = 1 / (1 + 10 ** (pH - PKA_POS["Nterm"]))
    neg = -1 / (1 + 10 ** (PKA_NEG["Cterm"] - pH))
    for aa in seq:
        if aa in PKA_POS:
            pos += 1 / (1 + 10 ** (pH - PKA_POS[aa]))
        elif aa in PKA_NEG:
            neg -= 1 / (1 + 10 ** (PKA_NEG[aa] - pH))
    return pos + neg


def isoelectric_point(seq):
    """pH at which the net charge is zero, by bisection (net charge falls as pH rises)."""
    lo, hi = 0.0, 14.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if net_charge(seq, mid) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def read_backbone(path, chain="A"):
    """Return {residue number: {"resn": three-letter name, "N"/"CA"/"C"/"O": xyz in angstrom}}
    for the protein atoms of one chain (first alternate location only)."""
    res = {}
    for line in Path(path).read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("ATOM") and line[21] == chain and line[16] in " A":
            name = line[12:16].strip()
            if name in ("N", "CA", "C", "O"):
                num = int(line[22:26])
                r = res.setdefault(num, {"resn": line[17:20]})
                r[name] = np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])])
    return {k: v for k, v in res.items() if all(a in v for a in ("N", "CA", "C", "O"))}


def add_amide_h(res):
    """Place the amide H of each residue as DSSP does: 1.0 angstrom from N, along the direction
    from O to C of the previous residue. Proline and the first residue have no amide H."""
    h = {}
    for i, r in res.items():
        if i - 1 in res and r["resn"] != "PRO":
            v = res[i - 1]["C"] - res[i - 1]["O"]
            h[i] = r["N"] + v / np.linalg.norm(v)
    return h


def hbond_energy(n, h, c, o):
    """DSSP electrostatic energy (kJ/mol) between N-H of one residue and C=O of another
    (Kabsch and Sander 1983): E = 0.084 * 332 * (1/r_ON + 1/r_CH - 1/r_OH - 1/r_CN) kcal/mol,
    distances in angstrom. A hydrogen bond is counted when E < -0.5 kcal/mol (-2.1 kJ/mol)."""
    d = np.linalg.norm
    e_kcal = 0.084 * 332 * (1 / d(o - n) + 1 / d(c - h) - 1 / d(o - h) - 1 / d(c - n))
    return e_kcal * KCAL


def find_hbonds(res, min_sep=3, cutoff=-0.5 * KCAL):
    """List (acceptor i, donor j, energy kJ/mol) for every backbone C=O(i) ... H-N(j) pair with
    |j - i| >= min_sep and energy below the cutoff."""
    hs = add_amide_h(res)
    out = []
    for j, h in hs.items():
        for i, r in res.items():
            if abs(j - i) < min_sep:
                continue
            if np.linalg.norm(r["O"] - res[j]["N"]) > 5.2:   # too far to matter; saves time
                continue
            e = hbond_energy(res[j]["N"], h, r["C"], r["O"])
            if e < cutoff:
                out.append((i, j, e))
    return out


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "ubiquitin_1UBQ.pdb"
    res = read_backbone(path)
    seq = "".join(THREE_TO_ONE.get(res[k]["resn"], "X") for k in sorted(res))
    print(f"{path.name}: {len(seq)} residues with a complete backbone")
    print(seq)
    for pH in (3.0, 7.0, 7.4, 11.0):
        print(f"net charge at pH {pH:4.1f}: {net_charge(seq, pH):+6.2f}")
    print(f"isoelectric point (EMBOSS pKa set): {isoelectric_point(seq):.2f}")

    hb = find_hbonds(res)
    sep = Counter(j - i for i, j, _ in hb)
    print(f"\nbackbone hydrogen bonds (|i - j| >= 3, E < -2.1 kJ/mol): {len(hb)}")
    print(f"  O(i) -> H-N(i+4), alpha-helix pattern: {sep[4]}")
    print(f"  O(i) -> H-N(i+3), turns and helix ends:  {sep[3]}")
    print(f"  all others (mostly beta-sheet pairs):    {len(hb) - sep[4] - sep[3]}")
    print(f"  mean energy {np.mean([e for *_, e in hb]):.1f} kJ/mol, strongest {min(e for *_, e in hb):.1f} kJ/mol")
    print(f"  share of i -> i+4 bonds: {sep[4] / len(hb):.0%}")
    if "1UBQ" in path.name.upper():
        helix = [(i, j) for i, j, _ in hb if j - i == 4 and 22 <= i <= 31]
        print(f"  i -> i+4 bonds starting at residues 22-31 (the ubiquitin helix): {len(helix)}")
        print("  " + ", ".join(f"O{i}-N{j}" for i, j in helix))

    (HERE / "runs").mkdir(exist_ok=True)
    ph = np.linspace(0, 14, 281)
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.plot(ph, [net_charge(seq, p) for p in ph])
    ax.axhline(0, color="grey", lw=0.8)
    ax.axvline(isoelectric_point(seq), color="grey", ls=":", label=f"pI = {isoelectric_point(seq):.2f}")
    ax.set_xlabel("pH")
    ax.set_ylabel("net charge (e)")
    ax.set_title(f"Net charge of {path.stem}")
    ax.legend()
    fig.tight_layout()
    fig.savefig(HERE / "runs" / "lesson02_charge.png", dpi=120)
    print("\nplot saved to runs/lesson02_charge.png")


if __name__ == "__main__":
    main()
