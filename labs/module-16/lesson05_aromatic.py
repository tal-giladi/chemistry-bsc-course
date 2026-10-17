"""Lesson 16.5 exercise: Hueckel's rule by counting pi electrons, and where substitution goes.

Run (from this folder):
    py lesson05_aromatic.py
    py lesson05_aromatic.py "O=C(O)c1ccccc1"      # predict nitration sites of your own arene
"""
import sys

from org16 import Chem, attempt, canon, check_drill, eas_judgement, mol, run_reaction

# Monocyclic rings written in Kekule form (explicit double bonds), so the count is done on one
# resonance structure. Cyclooctatetraene is really tub-shaped (not planar); the count assumes planarity.
RINGS = [("benzene", "C1=CC=CC=C1"), ("cyclobutadiene", "C1=CC=C1"), ("cyclooctatetraene", "C1=CC=CC=CC=C1"),
         ("cyclopentadiene", "C1=CCC=C1"), ("cyclopentadienyl anion", "[CH-]1C=CC=C1"),
         ("tropylium cation", "[CH+]1C=CC=CC=C1"), ("cyclopropenyl cation", "[CH+]1C=C1"),
         ("pyridine", "C1=CC=NC=C1"), ("pyrrole", "C1=CNC=C1"), ("furan", "C1=COC=C1"),
         ("thiophene", "C1=CSC=C1")]


def pi_electrons(m, ring):
    """Pi electrons a ring atom set contributes, or None if one atom breaks the conjugation.
    Per atom: 1 if it has a double bond to another ring atom; 0 if it is a carbocation (empty p orbital);
    2 if it can give a lone pair (N, O or S with only single bonds, or a carbanion); otherwise None."""
    ring_set = set(ring)
    total = 0
    for i in ring:
        a = m.GetAtomWithIdx(i)
        # TODO: check, in this order: a double bond to a ring neighbour -> 1; carbon with formal charge
        # TODO: +1 -> 0; N, O or S, or carbon with charge -1 -> 2; anything else (an sp3 CH2) -> None.
        raise NotImplementedError("write this part")
    return total


def huckel(n_pi):
    if n_pi is None:
        return "not aromatic (conjugation broken by an sp3 atom)"
    if n_pi % 4 == 2:
        return "aromatic (4n+2)"
    return "antiaromatic if planar (4n)"


def nitration_sites(smiles):
    """Ring positions where nitration is predicted, with the reason, using the module's directing rules."""
    out = []
    for products, reactant, site in run_reaction("nitration", [smiles]):
        ok, why = eas_judgement(reactant, site)
        out.append((ok, ", ".join(sorted(products)), why))
    return sorted(set(out), key=lambda t: (not t[0], t[1]))


ANSWERS = {
    "a benzene + CH3COCl, AlCl3": "",
    "b toluene + Br2, FeBr3 (major)": "",
    "c nitrobenzene + Br2, FeBr3": "",
    "d anisole + HNO3, H2SO4 (major)": "",
    "e acetanilide + Br2 (major)": "",
}
KEYS = {
    "a benzene + CH3COCl, AlCl3": "7c59097771241e56",
    "b toluene + Br2, FeBr3 (major)": "6af69b5f20fc2939",
    "c nitrobenzene + Br2, FeBr3": "83e9a3f69240e49f",
    "d anisole + HNO3, H2SO4 (major)": "44cfdfd40cd53ece",
    "e acetanilide + Br2 (major)": "26bff77a998543f3",
}


def main():
    print("Hueckel count (on the Kekule structure) and RDKit's own aromaticity flag")
    for name, smi in RINGS:
        m = Chem.MolFromSmiles(smi, sanitize=False)
        Chem.SanitizeMol(m, Chem.SanitizeFlags.SANITIZE_ALL ^ Chem.SanitizeFlags.SANITIZE_SETAROMATICITY)
        ring = list(m.GetRingInfo().AtomRings()[0])
        n = attempt(pi_electrons, m, ring)
        verdict = huckel(n) if n != "TODO" else "TODO"
        rdkit_flag = all(a.GetIsAromatic() for a in mol(smi).GetAtoms() if a.IsInRing())
        print(f"  {name:24s} pi = {str(n):5s} {verdict:48s} RDKit aromatic: {rdkit_flag}")

    targets = [sys.argv[1]] if len(sys.argv) > 1 else ["Cc1ccccc1", "O=[N+]([O-])c1ccccc1", "Clc1ccccc1",
                                                     "COc1ccc(C)cc1"]
    for t in targets:
        print(f"\nNitration of {canon(t)}")
        for ok, prod, why in nitration_sites(t):
            print(f"  {'yes' if ok else 'no '}  {prod:34s} {why}")
    print("\nProduct drill")
    check_drill(ANSWERS, KEYS)


if __name__ == "__main__":
    main()
