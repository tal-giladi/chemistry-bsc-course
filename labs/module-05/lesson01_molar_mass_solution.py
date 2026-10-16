"""Lesson 05.1 reference solution: molar masses and solution recipes from formulas.

Usage (from this folder):
    py lesson01_molar_mass_solution.py
    py lesson01_molar_mass_solution.py C6H12O6      # any simple formula without brackets
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
    for symbol, number in re.findall(r"([A-Z][a-z]?)(\d*)", formula):
        if symbol not in ATOMIC_WEIGHT:
            raise ValueError(f"unknown element symbol {symbol!r} in {formula!r}")
        counts[symbol] = counts.get(symbol, 0) + (int(number) if number else 1)
    if not counts:
        raise ValueError(f"no elements found in {formula!r}")
    return counts


def molar_mass(counts):
    """Sum of count x atomic weight, in g/mol."""
    return sum(n * ATOMIC_WEIGHT[symbol] for symbol, n in counts.items())


def mass_for_solution(M, conc_mol_per_L, volume_mL):
    """Grams of solute for a solution of the given concentration and volume: m = c V M."""
    return conc_mol_per_L * volume_mL / 1000 * M


def main():
    if len(sys.argv) > 1:
        f = sys.argv[1]
        print(f"{f}: M = {molar_mass(parse_formula(f)):.3f} g/mol")
        return
    print(f"{'substance':<24}{'formula':<12}{'M (g/mol)':>10}{'g for 250 mL of 0.100 M':>26}")
    for name, formula in KITCHEN.items():
        M = molar_mass(parse_formula(formula))
        g = mass_for_solution(M, 0.100, 250)
        print(f"{name:<24}{formula:<12}{M:>10.3f}{g:>26.3f}")
    # Check against a value you can work out by hand: water = 2(1.0080) + 15.999 = 18.015 g/mol
    assert abs(molar_mass(parse_formula("H2O")) - 18.015) < 1e-3
    print("\nCheck passed: M(H2O) = 18.015 g/mol.")


if __name__ == "__main__":
    main()
