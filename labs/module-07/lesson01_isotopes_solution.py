"""Lesson 07.1 reference solution: atomic weights and isotope patterns.

Run (from this folder):
    py lesson01_isotopes_solution.py
"""
from itertools import product

# NIST "Atomic Weights and Isotopic Compositions" (relative atomic mass, mole-fraction abundance),
# https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl, retrieved 2026-10-16.
ISOTOPES = {
    "H": [(1.00782503223, 0.999885), (2.01410177812, 0.000115)],
    "C": [(12.0, 0.9893), (13.00335483507, 0.0107)],
    "B": [(10.01293695, 0.199), (11.00930536, 0.801)],
    "Mg": [(23.985041697, 0.7899), (24.985836976, 0.1000), (25.982592968, 0.1101)],
    "Cl": [(34.968852682, 0.7576), (36.965902602, 0.2424)],
    "Cu": [(62.92959772, 0.6915), (64.92778970, 0.3085)],
    "Br": [(78.9183376, 0.5069), (80.9162897, 0.4931)],
}

# IUPAC CIAAW abridged standard atomic weights 2024 (https://www.ciaaw.org/abridged-atomic-weights.htm)
CIAAW = {"H": 1.0080, "C": 12.011, "B": 10.81, "Mg": 24.305, "Cl": 35.45, "Cu": 63.546, "Br": 79.904}

N_A = 6.02214076e23  # mol^-1, exact (SI 2019)


def atomic_weight(element):
    """Abundance-weighted mean of the isotope masses."""
    iso = ISOTOPES[element]
    total = sum(x for _, x in iso)
    return sum(m * x for m, x in iso) / total


def isotope_pattern(atoms):
    """atoms: list of element symbols, one entry per atom, e.g. ["C", "H", "H", "Br", "Br"].
    Returns {nominal mass: relative intensity (largest = 100)}."""
    peaks = {}
    for combo in product(*(ISOTOPES[a] for a in atoms)):
        mass = round(sum(m for m, _ in combo))
        p = 1.0
        for _, x in combo:
            p *= x
        peaks[mass] = peaks.get(mass, 0.0) + p
    top = max(peaks.values())
    return {m: 100 * p / top for m, p in sorted(peaks.items()) if 100 * p / top >= 0.5}


def main():
    print(f"{'element':<8}{'from isotopes':>15}{'CIAAW 2024':>12}")
    for el in ISOTOPES:
        print(f"{el:<8}{atomic_weight(el):>15.4f}{CIAAW[el]:>12}")

    print("\nIsotope patterns (nominal mass: % of tallest peak, >= 0.5 %)")
    for name, atoms in [("Cl2", ["Cl", "Cl"]), ("CH2Br2", ["C", "H", "H", "Br", "Br"]),
                        ("CHCl3", ["C", "H", "Cl", "Cl", "Cl"])]:
        pat = isotope_pattern(atoms)
        print(f"{name:<8}" + "  ".join(f"{m}: {p:.0f}" for m, p in pat.items()))

    # mass -> amount -> particles: one 5.00 g teaspoon of table salt
    m, M = 5.00, 22.990 + 35.45
    n = m / M
    print(f"\n5.00 g NaCl = {n:.4f} mol = {n * N_A:.3e} formula units = {2 * n * N_A:.3e} ions")


if __name__ == "__main__":
    main()
