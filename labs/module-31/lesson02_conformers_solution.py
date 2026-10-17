"""Lesson 31.2 reference solution: molecular mechanics and conformer search.

Part A  butane C1-C2-C3-C4 relaxed scan with GFN2-xTB (xtb --opt --input xtb/butane_scan.inp),
        compared with the MMFF94 scan of lesson 15.2.
Part B  n-pentane conformer search: RDKit ETKDG embedding + MMFF94 minimisation, duplicates
        removed by the two backbone dihedrals, then every unique conformer re-optimised with
        GFN2-xTB and both rankings turned into Boltzmann populations at 298 K.

Run from this folder:  py lesson02_conformers_solution.py      (about 30 s; needs xtb for A and B2)
Writes runs/31.2-*/ and runs/lesson02_conformers.png."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from rdkit import Chem
from rdkit.Chem import AllChem

import comp31 as c

MMFF_152 = {"anti": 0.0, "gauche": 3.5, "eclipsed CH3/H": 16.6, "syn": 21.8}   # lesson 15.2


def scan_profile(frames, atoms=(0, 1, 2, 3)):
    """(dihedral in degrees, energy relative to the lowest frame in kJ/mol), sorted by dihedral."""
    e_min = min(e for _, _, e in frames)
    pts = [(c.dihedral(x, *atoms) % 360.0, (e - e_min) * c.HARTREE_KJMOL) for _, x, e in frames]
    return sorted(pts)


def label(phi):
    """Name a backbone dihedral: t (anti, near 180), g+ (near +60) or g- (near -60 = 300)."""
    phi = phi % 360.0
    if 120.0 <= phi <= 240.0:
        return "t"
    return "g+" if phi < 120.0 else "g-"


def conformer_name(d1, d2):
    a, b = label(d1), label(d2)
    if a == "t" and b == "t":
        return "tt"
    if "t" in (a, b):
        return "tg"
    return "g+g+" if a == b else "g+g-"


def pentane_search(n_confs=60, seed=31):
    """Embed and MMFF94-minimise n-pentane conformers; return the unique ones, lowest energy first.

    Each item: (name, MMFF energy kJ/mol, RDKit mol, conformer id)."""
    mol = Chem.AddHs(Chem.MolFromSmiles("CCCCC"))
    ids = AllChem.EmbedMultipleConfs(mol, numConfs=n_confs, randomSeed=seed)
    res = AllChem.MMFFOptimizeMoleculeConfs(mol, maxIters=2000)
    best = {}
    for cid, (_, e_kcal) in zip(ids, res):
        x = mol.GetConformer(cid).GetPositions()
        name = conformer_name(c.dihedral(x, 0, 1, 2, 3), c.dihedral(x, 1, 2, 3, 4))
        e = e_kcal * 4.184
        if name not in best or e < best[name][0]:
            best[name] = (e, cid)
    return sorted(((n, e, mol, cid) for n, (e, cid) in best.items()), key=lambda t: t[1])


def degeneracy(name):
    """Number of equivalent forms: tg has 4 (tg+, tg-, g+t, g-t), g+g+ has 2, g+g- has 2."""
    return {"tt": 1, "tg": 4, "g+g+": 2, "g+g-": 2}[name]


def main():
    # ---------------- Part A: butane scan
    out = c.run_xtb(c.MOLECULES / "butane.xyz", ["--opt", "--input", str(c.HERE / "xtb" / "butane_scan.inp")],
                    c.RUNS / "31.2-butane-scan", "scan.out")
    prof = scan_profile(c.read_multixyz(out.parent / "xtbscan.log"))
    phi = np.array([p[0] for p in prof])
    e = np.array([p[1] for p in prof])
    pick = lambda lo, hi, f: f(e[(phi >= lo) & (phi <= hi)])
    gfn2 = {"anti": pick(170, 190, np.min), "gauche": pick(50, 90, np.min),
            "eclipsed CH3/H": pick(100, 140, np.max), "syn": pick(0, 10, np.max)}
    print("Part A - butane torsion, kJ/mol relative to anti")
    print(f"  {'point':16s} {'GFN2-xTB':>9s} {'MMFF94 (15.2)':>14s}")
    for k in MMFF_152:
        print(f"  {k:16s} {gfn2[k]:9.1f} {MMFF_152[k]:14.1f}")

    # ---------------- Part B: pentane
    confs = pentane_search()
    print("\nPart B - n-pentane conformers")
    print(f"  {'name':6s} {'g':>2s} {'MMFF94':>7s} {'GFN2':>6s}  (kJ/mol, relative)")
    rows = []
    for name, e_mmff, mol, cid in confs:
        x = mol.GetConformer(cid).GetPositions()
        sym = [a.GetSymbol() for a in mol.GetAtoms()]
        work = c.RUNS / "31.2-pentane" / name
        work.mkdir(parents=True, exist_ok=True)
        c.write_xyz(work / "start.xyz", sym, x, f"pentane {name} MMFF94")
        o = c.run_xtb(work / "start.xyz", ["--opt"], work, "opt.out")
        _, xo, _ = c.read_xyz(work / "xtbopt.xyz")
        still = conformer_name(c.dihedral(xo, 0, 1, 2, 3), c.dihedral(xo, 1, 2, 3, 4))
        rows.append((name, e_mmff, c.xtb_total_energy(o) * c.HARTREE_KJMOL, still))
    e0m = min(r[1] for r in rows)
    e0x = min(r[2] for r in rows)
    pm = c.boltzmann([r[1] - e0m for r in rows], g=[degeneracy(r[0]) for r in rows])
    px = c.boltzmann([r[2] - e0x for r in rows], g=[degeneracy(r[0]) for r in rows])
    for (name, em, ex, still), a, b in zip(rows, pm, px):
        note = "" if still == name else f"  (xtb moved it to {still})"
        print(f"  {name:6s} {degeneracy(name):2d} {em - e0m:7.2f} {ex - e0x:6.2f}   populations "
              f"{100 * a:4.1f} % / {100 * b:4.1f} %{note}")

    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.plot(phi, e, "o-", ms=3, label="GFN2-xTB relaxed scan")
    ax.plot([0, 60, 120, 180, 240, 300, 360], [21.8, 3.5, 16.6, 0, 16.6, 3.5, 21.8], "s--", label="MMFF94 points (15.2)")
    ax.set_xlabel("C1-C2-C3-C4 dihedral (degrees)")
    ax.set_ylabel("relative energy (kJ/mol)")
    ax.set_xticks(range(0, 361, 60))
    ax.legend()
    fig.tight_layout()
    c.RUNS.mkdir(exist_ok=True)
    fig.savefig(c.RUNS / "lesson02_conformers.png", dpi=120)
    print("\nplot: runs/lesson02_conformers.png")


if __name__ == "__main__":
    main()
