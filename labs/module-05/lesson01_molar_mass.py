"""Lesson 05.1: molar masses and solution recipes from formulas.

Fill in the three functions marked TODO, then run (from this folder):
    py lesson01_molar_mass.py
    py lesson01_molar_mass.py C6H12O6      # any simple formula without brackets
Reference solution: lesson01_molar_mass_solution.py
"""
import re
import sys

# IUPAC CIAAW abridged standard atomic weights 2024, g/mol (https://www.ciaaw.org/abridged-atomic-weights.htm)
ATOMIC_WEIGHT = {
    "H": 1.0080, "C": 12.011, "N": 14.007, "O": 15.999, "Na": 22.990, "Mg": 24.305,
    "S": 32.06, "Cl": 35.45, "K": 39.098, "Ca": 40.078, "Mn": 54.938, "Fe": 55.845, "Cu": 63.546,
}

KITCHEN = {
    "table salt": "NaCl",
    "sucrose (sugar)": "C12H22O11",
    "baking soda": "NaHCO3",
    "citric acid": "C6H8O7",
    "acetic acid (vinegar)": "C2H4O2",
    "water": "H2O",
}


def parse_formula(formula):
    """'C12H22O11' -> {'C': 12, 'H': 22, 'O': 11}. Simple formulas only (no brackets)."""
    counts = {}
    # re.findall(r"([A-Z][a-z]?)(\d*)", formula) gives pairs like ('C', '12'), ('Na', '').
    # TODO: loop over the pairs; an empty number means 1. Add to counts[symbol] (an element can
    #       appear twice, as in C2H4O2 written CH3COOH). Raise ValueError for a symbol that is not
    #       in ATOMIC_WEIGHT, and for a formula with no elements at all.
    return None


def molar_mass(counts):
    """Sum of count x atomic weight, in g/mol."""
    # TODO: one line with sum(...) over counts.items()
    return None


def mass_for_solution(M, conc_mol_per_L, volume_mL):
    """Grams of solute for a solution of the given concentration and volume: m = c V M."""
    # TODO: watch the units: volume is in mL, concentration in mol/L
    return None


def main():
    if parse_formula("H2O") is None or molar_mass({"H": 2, "O": 1}) is None:
        print("TODO: write parse_formula() and molar_mass() first.")
        return
    if len(sys.argv) > 1:
        f = sys.argv[1]
        print(f"{f}: M = {molar_mass(parse_formula(f)):.3f} g/mol")
        return
    if mass_for_solution(18.0, 0.1, 250) is None:
        print("TODO: write mass_for_solution() next.")
        return
    print(f"{'substance':<24}{'formula':<12}{'M (g/mol)':>10}{'g for 250 mL of 0.100 M':>26}")
    for name, formula in KITCHEN.items():
        M = molar_mass(parse_formula(formula))
        g = mass_for_solution(M, 0.100, 250)
        print(f"{name:<24}{formula:<12}{M:>10.3f}{g:>26.3f}")
    # Check against a value you can work out by hand: water = 2(1.0080) + 15.999 = 18.015 g/mol
    assert abs(molar_mass(parse_formula("H2O")) - 18.015) < 1e-3, "M(H2O) should be 18.015 g/mol"
    print("\nCheck passed: M(H2O) = 18.015 g/mol.")


if __name__ == "__main__":
    main()
