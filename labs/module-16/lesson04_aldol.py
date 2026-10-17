"""Lesson 16.4 exercise: enolisable hydrogens, enolate equilibria and crossed-aldol mixtures.

Run (from this folder):
    py lesson04_aldol.py
    py lesson04_aldol.py "CC=O" "CCC=O"      # your own pair of carbonyl compounds
"""
import sys

from org16 import Chem, attempt, canon, check_drill, mol, run_reaction

# Approximate pKa values: OpenStax Organic Chemistry 22.5, Table 22.1 (accessed 2026-10-17).
PKA = {"acetone (alpha C-H)": 19.3, "ethanol (O-H)": 16, "diisopropylamine (N-H)": 36,
       "2,4-pentanedione (central C-H)": 9}


def alpha_hydrogens(m):
    """List (atom index, number of H) for every sp3 carbon next to an aldehyde, ketone or ester C=O
    that carries at least one H (an enolisable position)."""
    # TODO: match the SMARTS "[CX4;!H0][CX3]=O" and keep each first atom once, with its GetTotalNumHs().
    raise NotImplementedError("write this part")


def crossed_aldol_products(a, b):
    """All aldol ADDITION products from a mixture of carbonyl compounds a and b (SMILES), counting
    both self-aldols and both crossed aldols. Returns a sorted list of canonical SMILES."""
    # TODO: call run_reaction("aldol_addition", pair) for the pairs [a, a], [a, b] and [b, b];
    # TODO: each outcome is (set of product SMILES, ...); collect every product in one set.
    raise NotImplementedError("write this part")


ANSWERS = {
    "a acetone + LDA (-78 C), then CH3I": "",
    "b diethyl malonate + NaOEt, then 1-bromobutane; then H3O+, heat": "",
    "c benzaldehyde + acetone (1:1), NaOH, heat": "",
    "d ethyl acetate + NaOEt, then H3O+ (Claisen)": "",
    "e 2-methylcyclohexanone + LDA (-78 C), then CH3I": "",
}
KEYS = {
    "a acetone + LDA (-78 C), then CH3I": "a6d7f82acf053a5c",
    "b diethyl malonate + NaOEt, then 1-bromobutane; then H3O+, heat": "c0d22b5f44c4ee10",
    "c benzaldehyde + acetone (1:1), NaOH, heat": "641f567b19ba2b21",
    "d ethyl acetate + NaOEt, then H3O+ (Claisen)": "9db88c05897ab8e4",
    "e 2-methylcyclohexanone + LDA (-78 C), then CH3I": "798a50063d36a3d2",
}


def main():
    print("Enolate formation from acetone: K = 10^(pKa of the base's conjugate acid - 19.3)")
    for base, conj in (("NaOEt", "ethanol (O-H)"), ("LDA", "diisopropylamine (N-H)")):
        k = 10 ** (PKA[conj] - PKA["acetone (alpha C-H)"])
        print(f"  {base:6s} K = {k:9.2e}  -> {'complete' if k > 1e3 else 'tiny fraction of'} enolate")

    print("\nEnolisable positions (atom index, number of alpha-H)")
    for name, smi in (("acetone", "CC(C)=O"), ("benzaldehyde", "O=Cc1ccccc1"), ("2-methylcyclohexanone", "CC1CCCCC1=O"),
                      ("ethyl acetate", "CCOC(C)=O"), ("2,2-dimethylpropanal", "CC(C)(C)C=O")):
        print(f"  {name:22s} {attempt(alpha_hydrogens, mol(smi))}")

    pairs = [("CC=O", "CCC=O"), ("O=Cc1ccccc1", "CC(C)=O")]
    if len(sys.argv) == 3:
        pairs = [(sys.argv[1], sys.argv[2])]
    for a, b in pairs:
        prods = attempt(crossed_aldol_products, a, b, default=None)
        print(f"\nAldol addition products from a mixture of {canon(a)} and {canon(b)}:")
        if prods is None:
            print("  TODO: write crossed_aldol_products()")
            continue
        for p in prods:
            print(f"  {p}")
        print(f"  {len(prods)} product(s)")
    print("\nProduct drill")
    check_drill(ANSWERS, KEYS)


if __name__ == "__main__":
    main()
