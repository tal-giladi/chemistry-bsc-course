"""Shared helpers for the Module 24 organic-lab exercises. You do not need to edit this file.

Data sources (retrieved 2026-10-17):
- Melting points, solubilities, pKa and log Kow: PubChem (https://pubchem.ncbi.nlm.nih.gov/),
  compound pages named in COMPOUNDS below, and the NIST Chemistry WebBook phase-change pages.
- Antoine constants for cyclohexane and toluene: NIST Chemistry WebBook (Williamham, Taylor et al. 1945),
  log10(P/bar) = A - B / (T/K + C).
- Benzoic acid enthalpy of fusion: NIST Chemistry WebBook (Ginnings and Furukawa 1953).
- Gas constant: CODATA 2022 via NIST (exact).
Molar masses are computed by RDKit from the SMILES (IUPAC standard atomic weights).
Run  py org24.py  to print a short self-check.
"""
import csv
from pathlib import Path

from rdkit import Chem
from rdkit.Chem import Descriptors

HERE = Path(__file__).resolve().parent
R = 1.380649e-23 * 6.02214076e23     # J/(mol K), CODATA 2022

# name: (SMILES, literature melting point in deg C or None, note)
COMPOUNDS = {
    "salicylic acid": ("OC(=O)c1ccccc1O", 159.0, "PubChem CID 338"),
    "acetic anhydride": ("CC(=O)OC(C)=O", None, "PubChem CID 7918, liquid, density 1.082 g/mL at 20 C"),
    "aspirin": ("CC(=O)Oc1ccccc1C(=O)O", 135.0, "PubChem CID 2244, rapid heating"),
    "acetic acid": ("CC(=O)O", None, "by-product"),
    "1-butanol": ("CCCCO", None, "PubChem CID 263, bp 117.7 C"),
    "sodium bromide": ("[Na+].[Br-]", None, "PubChem CID 253881"),
    "1-bromobutane": ("CCCCBr", None, "PubChem CID 8002, bp 101.6 C"),
    "bromobenzene": ("Brc1ccccc1", None, "PubChem CID 7961"),
    "magnesium": ("[Mg]", None, "metal turnings"),
    "benzophenone": ("O=C(c1ccccc1)c1ccccc1", 48.0, "PubChem CID 3102"),
    "triphenylmethanol": ("OC(c1ccccc1)(c1ccccc1)c1ccccc1", 162.0, "NIST WebBook, Tfus about 435 K"),
    "biphenyl": ("c1ccc(-c2ccccc2)cc1", 69.0, "PubChem CID 7095, Grignard side product"),
    "benzaldehyde": ("O=Cc1ccccc1", None, "PubChem CID 240"),
    "acetone": ("CC(C)=O", None, "PubChem CID 180"),
    "dibenzalacetone": ("O=C(/C=C/c1ccccc1)/C=C/c1ccccc1", 111.0, "trans,trans isomer, lit. 110-111 C"),
    "benzoin": ("OC(C(=O)c1ccccc1)c1ccccc1", 137.0, "PubChem CID 8400, lit. 133-137 C"),
    "benzil": ("O=C(C(=O)c1ccccc1)c1ccccc1", 95.0, "NIST WebBook, Tfus 368 +/- 1 K"),
    "benzilic acid": ("OC(=O)C(O)(c1ccccc1)c1ccccc1", 150.0, "PubChem CID 6463"),
    "benzoic acid": ("OC(=O)c1ccccc1", 122.4, "PubChem CID 243; NIST Tfus 395.5 K"),
    "acetanilide": ("CC(=O)Nc1ccccc1", 114.3, "PubChem CID 904"),
    "water": ("O", 0.0, ""),
}

# Antoine constants, NIST WebBook (Williamham, Taylor et al. 1945): A, B, C, valid range in K
ANTOINE = {
    "cyclohexane": (3.96988, 1203.526, -50.287, (293.06, 354.73)),
    "toluene": (4.07827, 1343.943, -53.773, (308.52, 384.66)),
}

# Benzoic acid fusion (NIST WebBook, Ginnings and Furukawa 1953)
BENZOIC_TFUS_K = 395.52
BENZOIC_DFUS_H = 18006.0      # J/mol

# Acid data (PubChem): pKa and log Kow (octanol-water, used as a stand-in for ether-water)
ACIDS = {
    "benzoic acid": (4.20, 1.87),
    "salicylic acid": (2.97, 2.26),
    "aspirin": (3.49, 1.19),
}


def smiles(name):
    return COMPOUNDS[name][0]


def molar_mass(name_or_smiles):
    """Molar mass in g/mol from a compound name in COMPOUNDS or a SMILES string."""
    s = COMPOUNDS[name_or_smiles][0] if name_or_smiles in COMPOUNDS else name_or_smiles
    mol = Chem.MolFromSmiles(s)
    if mol is None:
        raise ValueError(f"not a valid SMILES: {s}")
    return Descriptors.MolWt(mol)


def antoine_bar(name, T):
    """Vapour pressure in bar at T (K)."""
    A, B, C, _ = ANTOINE[name]
    return 10 ** (A - B / (T + C))


def read_csv(name):
    """Rows of a CSV file in this folder as a list of dicts (strings); lines starting with # are skipped."""
    with open(HERE / name, newline="", encoding="utf-8") as f:
        lines = [ln for ln in f if not ln.startswith("#")]
    return list(csv.DictReader(lines))


def runs_dir():
    d = HERE / "runs"
    d.mkdir(exist_ok=True)
    return d


if __name__ == "__main__":
    for n in ("salicylic acid", "aspirin", "triphenylmethanol", "benzilic acid"):
        print(f"{n:18s} M = {molar_mass(n):7.2f} g/mol")
    for n in ANTOINE:
        print(f"{n:12s} P(353.15 K) = {antoine_bar(n, 353.15):.3f} bar")
    print(f"R = {R:.6f} J/(mol K)")
