"""Lesson 16.1 reference solution: carbon oxidation levels, alcohol classes and oxidation products.

Run (from this folder):
    py lesson01_oxidation_solution.py
"""
from org16 import Chem, attempt, mol, run_reaction, check_drill

# Bonds from carbon to these atoms raise its oxidation level (they are more electronegative).
ELECTRONEGATIVE = {"O", "N", "F", "Cl", "Br", "I"}

LADDER = [  # (name, SMILES); each row is one more oxidation step for the marked carbon
    ("methane", "C"), ("methanol", "CO"), ("formaldehyde", "C=O"), ("formic acid", "OC=O"),
    ("carbon dioxide", "O=C=O"), ("ethanol", "CCO"), ("acetaldehyde", "CC=O"),
    ("acetic acid", "CC(=O)O"), ("2-propanol", "CC(C)O"), ("acetone", "CC(C)=O"),
    ("tert-butanol", "CC(C)(C)O"), ("chloromethane", "CCl"), ("ethene", "C=C"),
]
ALCOHOLS = [("1-butanol", "CCCCO"), ("2-butanol", "CCC(C)O"), ("tert-butanol", "CC(C)(C)O"),
            ("cyclohexanol", "OC1CCCCC1"), ("benzyl alcohol", "OCc1ccccc1"), ("methanol", "CO")]


def oxidation_level(atom):
    """Oxidation level of one carbon atom: +1 for each bond (counting bond order) to O, N or a
    halogen, -1 for each attached hydrogen, 0 for bonds to carbon."""
    # [your code]
    # TODO: start from -atom.GetTotalNumHs(); loop over atom.GetBonds(); for a bond to an atom in
    # TODO: ELECTRONEGATIVE add int(bond.GetBondTypeAsDouble()) (so C=O counts 2).
    level = -atom.GetTotalNumHs()
    for bond in atom.GetBonds():
        other = bond.GetOtherAtom(atom)
        if other.GetSymbol() in ELECTRONEGATIVE:
            level += int(bond.GetBondTypeAsDouble())
    return level
    # [end of your code]


def alcohol_class(m):
    """Return 'methyl', 'primary', 'secondary' or 'tertiary' for the first C-OH carbon, or None."""
    names = {0: "methyl", 1: "primary", 2: "secondary", 3: "tertiary"}
    # [your code]
    # TODO: find C-OH carbons with the SMARTS "[CX4][OX2H]"; count that carbon's carbon neighbours
    # TODO: and return names[count]. Return None if there is no alcohol.
    for match in m.GetSubstructMatches(Chem.MolFromSmarts("[CX4][OX2H]")):
        c = m.GetAtomWithIdx(match[0])
        carbons = sum(1 for nb in c.GetNeighbors() if nb.GetSymbol() == "C")
        return names[carbons]
    return None
    # [end of your code]


# Product drill: write the main organic product as SMILES. Worked answers: lesson 16.1, Hands-on.
ANSWERS = {
    "a 1-butanol + PCC": "CCCC=O",
    "b cyclohexanol + Jones reagent": "O=C1CCCCC1",
    "c phenol + NaH, then CH3I": "COc1ccccc1",
    "d 2-methyl-2-butanol + H2SO4, heat": "CC=C(C)C",
    "e CH3MgBr + ethylene oxide, then H3O+": "CCCO",
}
KEYS = {
    "a 1-butanol + PCC": "db6de2fd6561aa41",
    "b cyclohexanol + Jones reagent": "28ed7f4abc3f3609",
    "c phenol + NaH, then CH3I": "d85965b591680f6e",
    "d 2-methyl-2-butanol + H2SO4, heat": "2178f5cbdb57c6a5",
    "e CH3MgBr + ethylene oxide, then H3O+": "462b618a7419d00d",
}


def main():
    print("Oxidation level of each carbon (heavy-atom order as in the SMILES)")
    for name, smi in LADDER:
        m = mol(smi)
        levels = [attempt(oxidation_level, a) for a in m.GetAtoms() if a.GetSymbol() == "C"]
        print(f"  {name:15s} {smi:10s} {levels}")
    print("\nAlcohols: class, then what mild (PCC/DMP) and strong (Jones) oxidation give")
    for name, smi in ALCOHOLS:
        cls = attempt(alcohol_class, mol(smi))
        out = []
        for rx in ("oxidise_mild", "oxidise_strong"):
            prods = sorted({p for o in run_reaction(rx, [smi]) for p in o[0]})
            out.append(", ".join(prods) if prods else "no reaction")
        print(f"  {name:15s} {cls:10s} mild: {out[0]:18s} strong: {out[1]}")
    print("\nProduct drill")
    check_drill(ANSWERS, KEYS)


if __name__ == "__main__":
    main()
