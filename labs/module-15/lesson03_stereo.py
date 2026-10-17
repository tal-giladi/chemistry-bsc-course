"""Lesson 15.3: stereocentres, CIP labels, mirror images and meso compounds with RDKit.

Fill in mirror() and relation() (marked TODO), then run (from this folder):
    py lesson03_stereo.py
Reference solution: lesson03_stereo_solution.py
"""
from org15 import need_rdkit

need_rdkit()
from rdkit import Chem  # noqa: E402
from rdkit.Chem import rdCIPLabeler  # noqa: E402
from rdkit.Chem.EnumerateStereoisomers import EnumerateStereoisomers  # noqa: E402

EXAMPLES = {
    "(R)-carvone (PubChem CID 439570)": "CC1=CC[C@H](CC1=O)C(=C)C",
    "L-alanine": "C[C@@H](C(=O)O)N",
    "2-butanol, one enantiomer": "CC[C@@H](C)O",
    "(E)-2-butene": "C/C=C/C",
    "(Z)-2-butene": r"C/C=C\C",
}


def atom_name(a):
    """Atom symbol, its index in the SMILES (0-based) and any non-carbon neighbours, e.g. C3(Br)."""
    het = [n.GetSymbol() for n in a.GetNeighbors() if n.GetSymbol() not in ("C", "H")]
    return f"{a.GetSymbol()}{a.GetIdx()}" + (f"({','.join(het)})" if het else "")


def cip_labels(smiles):
    """Return a list like ['C3(O): R'] or ['bond 1=2: E'] using RDKit's new CIP labeller."""
    mol = Chem.MolFromSmiles(smiles)
    rdCIPLabeler.AssignCIPLabels(mol)
    out = [f"{atom_name(a)}: {a.GetProp('_CIPCode')}" for a in mol.GetAtoms() if a.HasProp("_CIPCode")]
    out += [f"bond {b.GetBeginAtomIdx()}={b.GetEndAtomIdx()}: {b.GetProp('_CIPCode')}"
            for b in mol.GetBonds() if b.HasProp("_CIPCode")]
    return out


def mirror(smiles):
    """SMILES of the mirror image. Reflection inverts every stereocentre (@ <-> @@);
    E/Z double bonds (/ and backslash) are unchanged by a reflection."""
    # TODO: swap every "@@" for "@" and every "@" for "@@" (careful: do it in a way that does not
    # swap the same characters twice), then return the canonical SMILES of the result.
    return None


def relation(a, b):
    """Classify two structures: identical, enantiomers, diastereomers or constitutional isomers."""
    ca, cb = Chem.MolToSmiles(Chem.MolFromSmiles(a)), Chem.MolToSmiles(Chem.MolFromSmiles(b))
    # TODO: return "identical" if ca == cb; "enantiomers" if the mirror of a equals cb;
    # "diastereomers" if the SMILES without stereochemistry (isomericSmiles=False) are equal;
    # otherwise "constitutional isomers".
    return None


def stereoisomers(smiles):
    """All distinct stereoisomers of a constitution, each flagged meso (its own mirror image) or chiral."""
    mol = Chem.MolFromSmiles(smiles)
    seen = sorted({Chem.MolToSmiles(m) for m in EnumerateStereoisomers(mol)})
    return [(s, "meso (achiral)" if mirror(s) == s else "chiral") for s in seen]


def main():
    if mirror("C[C@H](O)CC") is None or relation("CCO", "CCO") is None:
        raise SystemExit("TODO: write mirror() and relation() first.")
    print("CIP labels")
    for name, smi in EXAMPLES.items():
        print(f"  {name:<34} {smi:<28} {', '.join(cip_labels(smi))}")

    print("\nPairs")
    pairs = [("C[C@@H](O)CC", "C[C@H](O)CC"),
             ("C[C@@H](O)CC", "CC[C@H](C)O"),
             ("C[C@@H](Br)[C@@H](C)Br", "C[C@@H](Br)[C@H](C)Br"),
             ("C/C=C/C", r"C/C=C\C"),
             ("CCC(C)O", "CCCCO")]
    for a, b in pairs:
        print(f"  {a:<26} vs {b:<26} -> {relation(a, b)}")

    for name, smi in [("tartaric acid", "OC(=O)C(O)C(O)C(=O)O"), ("2,3-dibromobutane", "CC(Br)C(C)Br"),
                      ("2-bromo-3-chlorobutane", "CC(Br)C(C)Cl")]:
        isos = stereoisomers(smi)
        print(f"\n{name}: {len(isos)} stereoisomers (2^n rule gives {2 ** 2})")
        for s, kind in isos:
            print(f"  {s:<36} {kind:<15} {', '.join(cip_labels(s))}")


if __name__ == "__main__":
    main()
