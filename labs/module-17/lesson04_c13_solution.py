"""Lesson 17.4 reference solution: 13C signal count and DEPT types from symmetry, used to pick isomers.

Run (from this folder):
    py lesson04_c13_solution.py
"""
from spec17 import need_rdkit

need_rdkit()
from rdkit import Chem  # noqa: E402

ISOMERS = {
    "C4H10O": {"1-butanol": "CCCCO", "2-butanol": "CCC(C)O", "2-methyl-1-propanol": "CC(C)CO",
               "2-methyl-2-propanol": "CC(C)(C)O", "diethyl ether": "CCOCC",
               "methyl propyl ether": "CCCOC", "2-methoxypropane": "COC(C)C"},
    "C6H4Cl2": {"1,2-dichlorobenzene": "Clc1ccccc1Cl", "1,3-dichlorobenzene": "Clc1cccc(Cl)c1",
                "1,4-dichlorobenzene": "Clc1ccc(Cl)cc1"},
}

# What an observer reports: number of 13C signals and the DEPT count of each type.
# (Teaching descriptions; check the real spectra in SDBS as the lesson asks.)
OBSERVED = {
    "P (C4H10O)": ("C4H10O", {"CH3": 2, "CH2": 1, "CH": 1, "C": 0}),
    "Q (C4H10O)": ("C4H10O", {"CH3": 1, "CH2": 0, "CH": 0, "C": 1}),
    "R (C4H10O)": ("C4H10O", {"CH3": 1, "CH2": 1, "CH": 1, "C": 0}),
    "S (C4H10O)": ("C4H10O", {"CH3": 2, "CH2": 0, "CH": 1, "C": 0}),
    "T (C6H4Cl2)": ("C6H4Cl2", {"CH3": 0, "CH2": 0, "CH": 2, "C": 1}),
}

TYPE = {3: "CH3", 2: "CH2", 1: "CH", 0: "C"}


def carbon_signals(smiles):
    """One entry per symmetry-distinct carbon: its type (CH3, CH2, CH or C) and how many carbons share it."""
    m = Chem.MolFromSmiles(smiles)
    ranks = list(Chem.CanonicalRankAtoms(m, breakTies=False))
    classes = {}
    for a in m.GetAtoms():
        if a.GetSymbol() == "C":
            r = ranks[a.GetIdx()]
            t = TYPE[a.GetTotalNumHs()]
            classes.setdefault(r, [t, 0])[1] += 1
    return [tuple(v) for v in classes.values()]


def dept_counts(smiles):
    """Count signals of each type, as DEPT-90/DEPT-135 plus the broadband spectrum would report them."""
    counts = {"CH3": 0, "CH2": 0, "CH": 0, "C": 0}
    for t, _ in carbon_signals(smiles):
        counts[t] += 1
    return counts


def matches(formula, observed):
    return [name for name, smi in ISOMERS[formula].items() if dept_counts(smi) == observed]


def main():
    print("Part 1 - predicted 13C signals (type x number of equivalent carbons)")
    for formula, isomers in ISOMERS.items():
        for name, smi in isomers.items():
            sig = carbon_signals(smi)
            print(f"  {name:22s} {len(sig)} signals: " + ", ".join(f"{t}x{n}" for t, n in sig))

    print("\nPart 2 - which isomer fits each observation?")
    for label, (formula, obs) in OBSERVED.items():
        print(f"  {label}: {', '.join(matches(formula, obs)) or 'no match'}")


if __name__ == "__main__":
    main()
