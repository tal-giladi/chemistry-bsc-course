"""Lesson 17.6 reference solution: the answers to the 50 unknowns.

Run (from this folder) to print them, or to write them into a copy of the answer file:
    py lesson06_project_solution.py
    py lesson06_project_solution.py --fill   (writes project_answers_solution.csv)
Open this file only after you have solved an unknown (phase 1) yourself.
The key evidence for each answer is in the lesson's details blocks.
"""
import sys

from spec17 import HERE

ANSWERS = {
    1: ("acetone (propan-2-one)", "CC(C)=O"),
    2: ("ethanol", "CCO"),
    3: ("acetic acid (ethanoic acid)", "CC(=O)O"),
    4: ("diethyl ether (ethoxyethane)", "CCOCC"),
    5: ("propan-2-ol", "CC(C)O"),
    6: ("acetonitrile (ethanenitrile)", "CC#N"),
    7: ("ethyl acetate (ethyl ethanoate)", "CCOC(C)=O"),
    8: ("propan-1-ol", "CCCO"),
    9: ("butanal", "CCCC=O"),
    10: ("2-methylpropan-2-ol", "CC(C)(C)O"),
    11: ("propanoic acid", "CCC(=O)O"),
    12: ("butan-2-one", "CCC(C)=O"),
    13: ("1,4-dioxane", "C1COCCO1"),
    14: ("methyl propanoate", "CCC(=O)OC"),
    15: ("2-methylpropan-1-ol", "CC(C)CO"),
    16: ("toluene (methylbenzene)", "Cc1ccccc1"),
    17: ("phenol", "Oc1ccccc1"),
    18: ("bromobenzene", "Brc1ccccc1"),
    19: ("benzaldehyde", "O=Cc1ccccc1"),
    20: ("triethylamine (N,N-diethylethanamine)", "CCN(CC)CC"),
    21: ("anisole (methoxybenzene)", "COc1ccccc1"),
    22: ("2-bromopropane", "CC(C)Br"),
    23: ("acetophenone (1-phenylethan-1-one)", "CC(=O)c1ccccc1"),
    24: ("pyridine", "c1ccncc1"),
    25: ("benzoic acid", "OC(=O)c1ccccc1"),
    26: ("chlorobenzene", "Clc1ccccc1"),
    27: ("aniline (benzenamine)", "Nc1ccccc1"),
    28: ("1,4-dimethylbenzene", "Cc1ccc(C)cc1"),
    29: ("1-bromobutane", "CCCCBr"),
    30: ("benzonitrile", "N#Cc1ccccc1"),
    31: ("N,N-dimethylformamide (DMF)", "CN(C)C=O"),
    32: ("ethylbenzene", "CCc1ccccc1"),
    33: ("phenylmethanol (benzyl alcohol)", "OCc1ccccc1"),
    34: ("methyl benzoate", "COC(=O)c1ccccc1"),
    35: ("4-methylphenol", "Cc1ccc(O)cc1"),
    36: ("cyclohexanone", "O=C1CCCCC1"),
    37: ("hex-1-ene", "C=CCCCC"),
    38: ("(propan-2-yl)benzene (cumene)", "CC(C)c1ccccc1"),
    39: ("pentan-3-one", "CCC(=O)CC"),
    40: ("cyclohexanol", "OC1CCCCC1"),
    41: ("hex-1-yne", "C#CCCCC"),
    42: ("pentan-2-one", "CCCC(C)=O"),
    43: ("ethyl propanoate", "CCOC(=O)CC"),
    44: ("cyclohexene", "C1=CCCCC1"),
    45: ("4-methylpentan-2-one", "CC(C)CC(C)=O"),
    46: ("2-phenylethan-1-ol", "OCCc1ccccc1"),
    47: ("methyl 2-methylprop-2-enoate", "C=C(C)C(=O)OC"),
    48: ("1-methyl-4-nitrobenzene", "Cc1ccc(cc1)[N+](=O)[O-]"),
    49: ("ethyl benzoate", "CCOC(=O)c1ccccc1"),
    50: ("ethyl 3-oxobutanoate", "CCOC(=O)CC(C)=O"),
}


def main():
    for n, (name, smiles) in ANSWERS.items():
        print(f"  {n:2d}  {name:40s} {smiles}")
    if "--fill" in sys.argv:
        lines = ["no,smiles"] + [f"{n},{s}" for n, (_, s) in ANSWERS.items()]
        (HERE / "project_answers_solution.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")
        print("written: project_answers_solution.csv")


if __name__ == "__main__":
    main()
