"""Lesson 15.7 module practical: check your answers to the mechanism workbook.

1. Work each reaction on paper first (arrows, intermediates, stereochemistry).
2. Write each product as a SMILES string in practical_answers.csv (column `smiles`).
   Stereochemistry matters: use @/@@ for stereocentres and / \\ for E/Z double bonds.
   For a racemic product, write either enantiomer.
3. Run (from this folder):
       py lesson07_practical.py
The key below is hashed, so it does not give the answers away. Full answers with reasons:
lesson07_practical_solution.py. The hashes assume RDKit 2026.9.1 (labs/common/requirements.txt):
another RDKit version may write canonical SMILES differently.
"""
import hashlib

from org15 import need_rdkit, read_csv

need_rdkit()
from rdkit import Chem  # noqa: E402
from rdkit import RDLogger  # noqa: E402

RDLogger.DisableLog("rdApp.*")  # we report unreadable SMILES ourselves

# id: (hashes of every accepted canonical SMILES, hash of the answer without stereochemistry)
KEY = {
    1: (["4ffae2ebed8eb810"], "4ffae2ebed8eb810"),
    2: (["baf10c6263079f54"], "baf10c6263079f54"),
    3: (["c838eb933cab8c49", "fd315ccfd792f333"], "02f2f1f032ffb5d9"),
    4: (["df11ca1621870862", "e590e9b7c18057f0"], "71318e67a5954c9e"),
    5: (["8f3dc374218ff002"], "a224db44823018da"),
    6: (["9fc79b3c6b6b2e29"], "a224db44823018da"),
    7: (["a92065fa276e3f6f"], "a92065fa276e3f6f"),
    8: (["7b7cbd00a58b906c"], "0b5f8187ee713c8b"),
    9: (["3073319e2005750d"], "3073319e2005750d"),
    10: (["3612e8cd9e45d1cd"], "3612e8cd9e45d1cd"),
}


def digest(smiles):
    return hashlib.sha256(smiles.encode("utf-8")).hexdigest()[:16]


def grade(i, smiles):
    if not smiles.strip():
        return "not answered"
    mol = Chem.MolFromSmiles(smiles.strip())
    if mol is None:
        return "RDKit cannot read this SMILES: check brackets, ring digits and charges"
    full, flat = KEY[i]
    if digest(Chem.MolToSmiles(mol)) in full:
        return "correct"
    if digest(Chem.MolToSmiles(mol, isomericSmiles=False)) == flat:
        return "right constitution, wrong or missing stereochemistry"
    return "wrong product: recheck the mechanism"


def main():
    rows = read_csv("practical_answers.csv")
    score = 0
    for r in rows:
        i = int(r["id"])
        verdict = grade(i, r.get("smiles", ""))
        score += verdict == "correct"
        print(f"{i:>2}. {r['reaction']:<52} {verdict}")
    print(f"\nscore: {score} / {len(KEY)}")


if __name__ == "__main__":
    main()
