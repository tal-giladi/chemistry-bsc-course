"""Lesson 17.5 reference solution: filter candidate structures with the evidence from all four spectra.

Run (from this folder):
    py lesson05_solver_solution.py
"""
from spec17 import need_rdkit, read_csv

need_rdkit()
from rdkit import Chem  # noqa: E402
from rdkit.Chem.rdMolDescriptors import CalcMolFormula  # noqa: E402

# Formates get their own class: their H-C(=O)O proton (a singlet near 8 ppm) and C=O near 161 ppm give
# them away, and IR alone would not separate them from other esters.
CLASSES = {  # checked in this order; the first match wins
    "carboxylic acid": "[CX3](=O)[OX2H1]",
    "ester": "[#6][CX3](=O)[OX2][#6]",
    "formate ester": "[CX3H1](=O)[OX2][#6]",
    "aldehyde": "[CX3H1](=O)[#6]",
    "ketone": "[#6][CX3](=O)[#6]",
    "alcohol": "[OX2H][CX4]",
}
TYPE = {3: "CH3", 2: "CH2", 1: "CH", 0: "C"}


def features(smiles):
    """What the four spectra could tell you about a structure."""
    m = Chem.MolFromSmiles(smiles)
    mh = Chem.AddHs(m)
    ranks = list(Chem.CanonicalRankAtoms(mh, breakTies=False))
    cls = next((c for c, s in CLASSES.items() if m.HasSubstructMatch(Chem.MolFromSmarts(s))), "other")
    carbons = {}
    for a in mh.GetAtoms():
        if a.GetSymbol() == "C":
            carbons[ranks[a.GetIdx()]] = TYPE[a.GetTotalNumHs(includeNeighbors=True)]
    dept = {t: list(carbons.values()).count(t) for t in ("CH3", "CH2", "CH", "C")}
    h_classes, singlets = set(), set()
    for a in mh.GetAtoms():
        if a.GetSymbol() != "H":
            continue
        r = ranks[a.GetIdx()]
        h_classes.add(r)
        heavy = a.GetNeighbors()[0]
        if heavy.GetSymbol() != "C":
            singlets.add(r)  # OH: exchanges, so a broad singlet
            continue
        # neighbours three bonds away: H on the carbons bonded to this H's carbon
        if not any(nb.GetSymbol() == "C" and nb.GetTotalNumHs(includeNeighbors=True) > 0 for nb in heavy.GetNeighbors()):
            singlets.add(r)
    return {"formula": CalcMolFormula(m), "class": cls, "c13_lines": len(carbons), "dept": dept,
            "h1_signals": len(h_classes), "h1_singlets": len(singlets)}


def consistent(f, evidence):
    """True if every piece of evidence given agrees with the features f."""
    return all(f[k] == v for k, v in evidence.items())


EVIDENCE = {
    "MS + IR only": {"formula": "C5H10O2", "class": "ester"},
    "+ 13C and DEPT": {"formula": "C5H10O2", "class": "ester", "c13_lines": 5,
                       "dept": {"CH3": 2, "CH2": 2, "CH": 0, "C": 1}},
    "+ 1H count and singlets": {"formula": "C5H10O2", "class": "ester", "c13_lines": 5,
                                "dept": {"CH3": 2, "CH2": 2, "CH": 0, "C": 1},
                                "h1_signals": 4, "h1_singlets": 1},
}


def main():
    rows = read_csv("candidates.csv")
    print("Features of each candidate")
    for r in rows:
        f = features(r["smiles"])
        print(f"  {r['name'].replace(';', ','):28s} {f['class']:16s} 13C {f['c13_lines']}  1H {f['h1_signals']}"
              f"  singlets {f['h1_singlets']}")
    print("\nCandidates left as evidence is added")
    for step, ev in EVIDENCE.items():
        left = [r["name"].replace(";", ",") for r in rows if consistent(features(r["smiles"]), ev)]
        print(f"  {step:24s} {len(left):2d}: {', '.join(left)}")
    print("\n  The last two differ only in where the singlet is: OCH3 near 3.7 ppm (methyl butanoate)")
    print("  or CH3C=O near 2.0 ppm (propyl acetate). Shifts, not counts, make the final call.")


if __name__ == "__main__":
    main()
