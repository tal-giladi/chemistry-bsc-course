"""Lesson 15.1 reference solution: hybridisation, sigma/pi bonds and functional groups with RDKit.

Run (from this folder):
    py lesson01_groups_solution.py
"""
from org15 import read_csv, need_rdkit

need_rdkit()
from rdkit import Chem  # noqa: E402

# SMARTS patterns: a small language for substructures (RDKit "Daylight SMARTS").
# X = total connections, H = attached hydrogens, D = heavy-atom neighbours, c = aromatic carbon.
GROUPS = {
    "alkene": "[CX3]=[CX3]",
    "alkyne": "[CX2]#[CX2]",
    "arene": "c1ccccc1",
    "haloalkane": "[CX4][F,Cl,Br,I]",
    "alcohol": "[OX2H][CX4]",
    "phenol": "[OX2H]c",
    "ether": "[OD2]([CX4,c])[CX4,c]",
    "amine": "[NX3;!$(N[CX3]=O)][CX4]",
    "aldehyde": "[CX3H1](=O)[#6]",
    "ketone": "[#6][CX3](=O)[#6]",
    "carboxylic acid": "[CX3](=O)[OX2H1]",
    "ester": "[#6][CX3](=O)[OX2][#6]",
    "amide": "[CX3](=O)[NX3]",
    "nitrile": "[CX2]#[NX1]",
}


def count_sigma_pi(mol):
    """Return (sigma, pi) for a molecule, hydrogens included.
    Every bond has one sigma part; a double bond adds one pi bond, a triple bond two.
    Aromatic rings are first written as alternating single and double bonds (Kekule form)."""
    m = Chem.AddHs(mol)
    Chem.Kekulize(m, clearAromaticFlags=True)
    sigma = m.GetNumBonds()
    pi = sum(int(b.GetBondTypeAsDouble()) - 1 for b in m.GetBonds())
    return sigma, pi


def hybridisation_summary(mol):
    """Count heavy atoms by hybridisation, e.g. {'SP3': 2, 'SP2': 1}."""
    counts = {}
    for a in mol.GetAtoms():
        h = str(a.GetHybridization())
        counts[h] = counts.get(h, 0) + 1
    return counts


def find_groups(mol):
    found = []
    for name, smarts in GROUPS.items():
        n = len(mol.GetSubstructMatches(Chem.MolFromSmarts(smarts)))
        if n:
            found.append(name if n == 1 else f"{name} x{n}")
    return found


def main():
    print(f"{'molecule':<15}{'sigma':>6}{'pi':>4}  hybridisation (heavy atoms)       functional groups")
    for row in read_csv("molecules.csv"):
        mol = Chem.MolFromSmiles(row["smiles"])
        s, p = count_sigma_pi(mol)
        hyb = ", ".join(f"{k.lower()} {v}" for k, v in sorted(hybridisation_summary(mol).items()))
        print(f"{row['name']:<15}{s:>6}{p:>4}  {hyb:<33}{'; '.join(find_groups(mol)) or '-'}")
    # One molecule in detail: which atom is which?
    mol = Chem.MolFromSmiles("CC#N")
    print("\nacetonitrile atom by atom:",
          ", ".join(f"{a.GetSymbol()}{a.GetIdx()} {str(a.GetHybridization()).lower()}" for a in mol.GetAtoms()))


if __name__ == "__main__":
    main()
