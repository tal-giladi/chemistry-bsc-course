"""Lesson 07.1: atomic weights and isotope patterns.

Fill in the two functions marked TODO, then run (from this folder):
    py lesson01_isotopes.py
Reference solution: lesson01_isotopes_solution.py
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
    # TODO: return sum(mass * abundance) / sum(abundance). Dividing by the sum protects you
    #       when the published abundances do not add up to exactly 1.
    return None


def isotope_pattern(atoms):
    """atoms: list of element symbols, one entry per atom, e.g. ["C", "H", "H", "Br", "Br"].
    Returns {nominal mass: relative intensity (largest = 100)}."""
    peaks = {}
    for combo in product(*(ISOTOPES[a] for a in atoms)):
        # combo is one choice of isotope for every atom, e.g. ((34.97, 0.7576), (36.97, 0.2424))
        # TODO: nominal mass = round(sum of the masses); probability = product of the abundances.
        #       Add the probability to peaks[mass].
        pass
    if not peaks:
        return None
    top = max(peaks.values())
    return {m: 100 * p / top for m, p in sorted(peaks.items()) if 100 * p / top >= 0.5}


def main():
    if atomic_weight("Cl") is None:
        print("TODO: write atomic_weight() first.")
        return
    print(f"{'element':<8}{'from isotopes':>15}{'CIAAW 2024':>12}")
    for el in ISOTOPES:
        print(f"{el:<8}{atomic_weight(el):>15.4f}{CIAAW[el]:>12}")

    if isotope_pattern(["Cl", "Cl"]) is None:
        print("\nTODO: write isotope_pattern() next.")
        return
    print("\nIsotope patterns (nominal mass: % of tallest peak, >= 0.5 %)")
    for name, atoms in [("Cl2", ["Cl", "Cl"]), ("CH2Br2", ["C", "H", "H", "Br", "Br"]),
                        ("CHCl3", ["C", "H", "Cl", "Cl", "Cl"])]:
        pat = isotope_pattern(atoms)
        print(f"{name:<8}" + "  ".join(f"{m}: {p:.0f}" for m, p in pat.items()))

    m, M = 5.00, 22.990 + 35.45
    n = m / M
    print(f"\n5.00 g NaCl = {n:.4f} mol = {n * N_A:.3e} formula units = {2 * n * N_A:.3e} ions")


if __name__ == "__main__":
    main()
