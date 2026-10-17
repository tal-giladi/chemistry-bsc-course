"""Lesson 08.5 hands-on: balance redox equations as a linear system.

Fill in composition_matrix() (TODO), then run:
       py lesson05_redox.py
       py lesson05_redox.py "Cu + NO3^- + H^+ -> Cu^2+ + NO + H2O"
Formulas: element symbols with counts, no brackets (write CH3COOH as C2H4O2 if you like);
charge after ^, e.g. MnO4^-, Fe^3+, Cr2O7^2-.
Reference solution: lesson05_redox_solution.py
Method (lesson 03.1): one row per element plus one row for charge, one column per species
(reactants +, products -). The coefficients are a vector in the null space of that matrix.
"""
import re
import sys
from fractions import Fraction
from math import lcm

import numpy as np
from scipy.linalg import null_space

EXAMPLES = [
    "Fe^2+ + MnO4^- + H^+ -> Fe^3+ + Mn^2+ + H2O",
    "Cu + NO3^- + H^+ -> Cu^2+ + NO + H2O",
    "C6H8O6 + I2 -> C6H6O6 + I^- + H^+",
    "Cr2O7^2- + C2H6O + H^+ -> Cr^3+ + C2H4O2 + H2O",
    "MnO4^- + I^- + H2O -> MnO2 + I2 + OH^-",
    "C3H8 + O2 -> CO2 + H2O",
]


def parse_species(text):
    """'Cr2O7^2-' -> ({'Cr': 2, 'O': 7}, -2)."""
    formula, _, charge_txt = text.strip().partition("^")
    charge = 0
    if charge_txt:
        m = re.fullmatch(r"(\d*)([+-])", charge_txt)
        if not m:
            raise ValueError(f"bad charge in {text!r}")
        charge = int(m.group(1) or 1) * (1 if m.group(2) == "+" else -1)
    atoms = {}
    for el, n in re.findall(r"([A-Z][a-z]?)(\d*)", formula):
        atoms[el] = atoms.get(el, 0) + int(n or 1)
    if "".join(f"{el}{n}" for el, n in re.findall(r"([A-Z][a-z]?)(\d*)", formula)) != formula:
        raise ValueError(f"cannot read formula {formula!r}")
    return atoms, charge


def composition_matrix(reactants, products):
    """Rows: each element, then charge. Columns: species; reactants +, products -."""
    species = [parse_species(s) for s in reactants + products]
    signs = [1] * len(reactants) + [-1] * len(products)
    elements = sorted({el for atoms, _ in species for el in atoms})
    # TODO: build `rows`, a list of lists. For each element: one row with sign * (count of that
    # element in each species). Then one last row: sign * charge of each species.
    rows = None
    if rows is None:
        raise NotImplementedError("TODO: write composition_matrix() first")
    return np.array(rows, dtype=float), elements + ["charge"]


def smallest_integers(vector):
    """Scale a null-space vector to the smallest positive whole numbers."""
    v = vector / vector[np.argmax(np.abs(vector))]
    if np.any(v <= 0):
        raise ValueError("no all-positive solution: check the species")
    fracs = [Fraction(float(x)).limit_denominator(1000) for x in v / v.min()]
    m = lcm(*(f.denominator for f in fracs))
    ints = [int(f * m) for f in fracs]
    g = np.gcd.reduce(ints)
    return [i // g for i in ints]


def balance(equation):
    left, right = equation.split("->")
    reactants = [s.strip() for s in re.split(r"\s\+\s", left)]
    products = [s.strip() for s in re.split(r"\s\+\s", right)]
    a, _ = composition_matrix(reactants, products)
    ns = null_space(a)
    if ns.shape[1] != 1:
        raise ValueError(f"null space has dimension {ns.shape[1]}: the equation is not uniquely balanced")
    coeffs = smallest_integers(ns[:, 0])
    def side(names, cs):
        return " + ".join((f"{c} " if c != 1 else "") + n for n, c in zip(names, cs))
    return side(reactants, coeffs[:len(reactants)]) + " -> " + side(products, coeffs[len(reactants):])


def main():
    for eq in (sys.argv[1:] or EXAMPLES):
        try:
            composition_matrix(["H2"], ["H2"])
        except NotImplementedError as e:
            print(e)
            return
        try:
            print(balance(eq))
        except ValueError as e:
            print(f"{eq}\n  problem: {e}")


if __name__ == "__main__":
    main()
