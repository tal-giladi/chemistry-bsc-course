"""Lesson 15.2 reference solution: conformations of butane and methylcyclohexane with the MMFF94 force field.

Run (from this folder):
    py lesson02_conformers_solution.py      # prints the tables, saves runs/butane_scan.png
"""
import math

from org15 import R_KJ, need_rdkit, runs_dir

need_rdkit()
from rdkit import Chem  # noqa: E402
from rdkit.Chem import AllChem, rdMolTransforms  # noqa: E402

KCAL = 4.184  # RDKit force fields report kcal/mol; 1 kcal = 4.184 kJ


def butane():
    mol = Chem.AddHs(Chem.MolFromSmiles("CCCC"))
    AllChem.EmbedMolecule(mol, randomSeed=15)
    return mol


def energy_at_dihedral(mol, phi):
    """MMFF energy (kJ/mol) of butane with the C1-C2-C3-C4 dihedral held at phi degrees,
    everything else relaxed."""
    m = Chem.Mol(mol)
    if phi > 180:  # the constraint expects -180..180
        phi -= 360
    rdMolTransforms.SetDihedralDeg(m.GetConformer(), 0, 1, 2, 3, float(phi))  # rotate first
    props = AllChem.MMFFGetMoleculeProperties(m)
    ff = AllChem.MMFFGetMoleculeForceField(m, props)
    ff.MMFFAddTorsionConstraint(0, 1, 2, 3, False, phi, phi, 1.0e4)
    ff.Minimize(maxIts=2000)
    free = AllChem.MMFFGetMoleculeForceField(m, props)  # same geometry, no constraint term
    return free.CalcEnergy() * KCAL


def boltzmann_ratio(delta_e_kj, T=298.15):
    """Population ratio of the higher state to the lower one, exp(-dE/RT)."""
    return math.exp(-delta_e_kj / (R_KJ * T))


def classify_methyl(dihedral_deg):
    """Return 'equatorial' or 'axial' from the CH3-C1-C2-C3 dihedral (0-180 deg).
    Equatorial methyls sit near 175-180 deg (anti to C3), axial ones near 70-75 deg (gauche)."""
    return "equatorial" if dihedral_deg > 130 else "axial"


def methylcyclohexane_conformers(n=30):
    """Return (energy kJ/mol, 'axial' or 'equatorial') for each optimised chair conformer."""
    mol = Chem.AddHs(Chem.MolFromSmiles("CC1CCCCC1"))
    ids = AllChem.EmbedMultipleConfs(mol, numConfs=n, randomSeed=15)
    res = AllChem.MMFFOptimizeMoleculeConfs(mol, maxIters=5000)
    out = []
    for cid, (conv, e) in zip(ids, res):
        conf = mol.GetConformer(cid)
        # Dihedral CH3-C1-C2-C3: about 180 deg if the methyl is equatorial, about 75 deg if axial.
        d = abs(rdMolTransforms.GetDihedralDeg(conf, 0, 1, 2, 3))
        ring = abs(rdMolTransforms.GetDihedralDeg(conf, 1, 2, 3, 4))
        if ring < 40:  # not a chair (twist-boat etc.): skip
            continue
        out.append((e * KCAL, classify_methyl(d)))
    return out


def main():
    mol = butane()
    angles = list(range(0, 361, 15))
    energies = [energy_at_dihedral(mol, a) for a in angles]
    e_min = min(energies)
    rel = [e - e_min for e in energies]
    print("Butane, MMFF94, energy relative to anti (kJ/mol)")
    for a, e in zip(angles, rel):
        if a % 60 == 0:
            name = {0: "syn (CH3/CH3 eclipsed)", 60: "gauche", 120: "eclipsed CH3/H",
                    180: "anti", 240: "eclipsed CH3/H", 300: "gauche", 360: "syn"}[a]
            print(f"  {a:>3} deg  {e:6.1f}   {name}")
    gauche = rel[angles.index(60)]
    print(f"gauche - anti = {gauche:.1f} kJ/mol (OpenStax 3.8);"
          f" barrier at 0 deg = {rel[0]:.1f} kJ/mol (OpenStax 19)")
    print(f"gauche:anti population ratio per gauche form at 298 K = {boltzmann_ratio(gauche):.2f}")

    confs = methylcyclohexane_conformers()
    eq = min(e for e, k in confs if k == "equatorial")
    ax = min(e for e, k in confs if k == "axial")
    d = ax - eq
    r = boltzmann_ratio(d)
    print(f"\nMethylcyclohexane chairs: {sum(k == 'equatorial' for _, k in confs)} equatorial,"
          f" {sum(k == 'axial' for _, k in confs)} axial out of {len(confs)}")
    print(f"axial - equatorial = {d:.1f} kJ/mol (OpenStax 7.6);"
          f" equatorial fraction at 298 K = {100 / (1 + r):.0f} %")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return
    fig, ax_ = plt.subplots(figsize=(6, 3.5))
    ax_.plot(angles, rel, "o-")
    ax_.set_xticks(range(0, 361, 60))
    ax_.set_xlabel("C1-C2-C3-C4 dihedral / degrees")
    ax_.set_ylabel("energy relative to anti / kJ mol$^{-1}$")
    ax_.set_title("Butane torsion scan (MMFF94, RDKit)")
    fig.tight_layout()
    fig.savefig(runs_dir() / "butane_scan.png", dpi=150)
    print("saved runs/butane_scan.png")


if __name__ == "__main__":
    main()
