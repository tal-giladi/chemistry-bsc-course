"""Lesson 17.6 project: check your answers to the 50 unknowns.

1. Solve each unknown (phase 1 at least: formula, DBE, MS, IR, candidates).
2. Write your structure as a SMILES string in project_answers.csv (column `smiles`).
   Stereochemistry is ignored: none of the 50 unknowns needs it.
3. Run (from this folder):
       py lesson06_project.py
The key below is hashed, so running the checker does not reveal the answers. The answers with
their key evidence are in the lesson's details blocks and in lesson06_project_solution.py.
The hashes assume RDKit 2026.9.1 (labs/common/requirements.txt); another RDKit version may write
canonical SMILES differently, so compare with the solution file if a correct answer is rejected.
"""
import hashlib

from spec17 import canon, need_rdkit, read_csv

need_rdkit()
from rdkit import Chem  # noqa: E402
from rdkit import RDLogger  # noqa: E402
from rdkit.Chem.rdMolDescriptors import CalcMolFormula  # noqa: E402

RDLogger.DisableLog("rdApp.*")  # unreadable SMILES are reported below

KEY = {
    1: "de84a3a5e7d86fb5",
    2: "ab1de819ede91df4",
    3: "b00014bedbaba3c9",
    4: "f2ef24d8a92c71b2",
    5: "dbb1ac6e5de73597",
    6: "fdd689a8c9458d0c",
    7: "aa776d017a7413ea",
    8: "462b618a7419d00d",
    9: "db6de2fd6561aa41",
    10: "baf10c6263079f54",
    11: "5a66bc5908e74d50",
    12: "a6d7f82acf053a5c",
    13: "53b5b2411b4bfe41",
    14: "ccc51878bebf4306",
    15: "ad2e64dffedc6a11",
    16: "5da1ba726f547074",
    17: "82b0491cd46906e0",
    18: "e16cf00bdc42a076",
    19: "8c15a1ca83578e93",
    20: "e0090ebb1b80e276",
    21: "d85965b591680f6e",
    22: "4ffae2ebed8eb810",
    23: "7c59097771241e56",
    24: "75c7a4b0b41e4390",
    25: "fb7121a404676cf4",
    26: "48220ac360214204",
    27: "21e9e6150c40c857",
    28: "da8f08afbbddb678",
    29: "9fbdac65e0c18c18",
    30: "f7baa28500cc392d",
    31: "aeb2e86e450d0fab",
    32: "3ed8c64f28bc36d6",
    33: "3f5d5a797945beb3",
    34: "7af636d52dc38439",
    35: "6f1b3105ba84bd88",
    36: "28ed7f4abc3f3609",
    37: "8c5b6f8d56de5b1b",
    38: "d5c6e524eb7b4107",
    39: "5c60918aba5fe746",
    40: "e36b66a9146ed318",
    41: "651b4073ef1ef05f",
    42: "48022b29c1cd04f7",
    43: "b1e84af38615924c",
    44: "fe8528cff2dfdfcc",
    45: "54af572f4ab14f31",
    46: "00afbb87cc755a4b",
    47: "a6a3a54dd9b87a8a",
    48: "4a1b4824ef248756",
    49: "e1010efe413a2631",
    50: "9db88c05897ab8e4",
}


def digest(smiles):
    c = canon(smiles)
    return None if c is None else hashlib.sha256(c.encode()).hexdigest()[:16]


def main():
    formulas = {int(r["no"]): r["formula"] for r in read_csv("unknowns.csv")}
    answers = {int(r["no"]): r.get("smiles", "").strip() for r in read_csv("project_answers.csv")}
    right = tried = 0
    for n in sorted(KEY):
        smi = answers.get(n, "")
        if not smi:
            continue
        tried += 1
        m = Chem.MolFromSmiles(smi)
        if m is None:
            print(f"  {n:2d}  cannot read SMILES {smi!r}")
            continue
        if digest(smi) == KEY[n]:
            right += 1
            print(f"  {n:2d}  correct")
        elif CalcMolFormula(m) != formulas[n]:
            print(f"  {n:2d}  wrong: your structure is {CalcMolFormula(m)}, the unknown is {formulas[n]}")
        else:
            print(f"  {n:2d}  wrong: right formula, wrong structure (an isomer); look again at the NMR")
    print(f"\n{right} correct out of {tried} answered ({len(KEY)} unknowns in total)")


if __name__ == "__main__":
    main()
