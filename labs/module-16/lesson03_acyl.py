"""Lesson 16.3 exercise: acid strength, the acyl reactivity ladder and Fischer esterification yield.

Run (from this folder):
    py lesson03_acyl.py
"""
import math

from org16 import attempt, check_drill

# pKa values: OpenStax Organic Chemistry 20.4 (benzoic acids, acetic, trifluoroacetic);
# aspirin from PubChem CID 2244 (3.49 at 25 C). Accessed 2026-10-17.
ACIDS = [("trifluoroacetic acid", -0.23), ("aspirin", 3.49), ("4-nitrobenzoic acid", 3.41),
         ("benzoic acid", 4.19), ("4-methoxybenzoic acid", 4.46), ("acetic acid", 4.76)]

# Acyl derivatives CH3C(=O)-Y with the approximate pKa of H-Y, the conjugate acid of the leaving group.
# A weaker base (lower pKa of H-Y) is a better leaving group, so the derivative is more reactive.
DERIVATIVES = [("N,N-dimethylacetamide", "Me2N-", "Me2NH", 36), ("acetyl chloride", "Cl-", "HCl", -7),
               ("ethyl acetate", "EtO-", "EtOH", 16), ("acetic anhydride", "AcO-", "AcOH", 4.76)]


def percent_ionised(pka, ph):
    """Percentage of a carboxylic acid present as the carboxylate at this pH (Henderson-Hasselbalch)."""
    # TODO: ratio A-/HA = 10**(pH - pKa); the ionised fraction is ratio/(1 + ratio). Return a percentage.
    raise NotImplementedError("write this part")


def ester_yield(k, acid0, alcohol0, water0=0.0):
    """Fischer esterification acid + alcohol <=> ester + water, equilibrium constant k (concentration
    ratio). Start with acid0, alcohol0 and water0 mol (no ester). Return the fraction of the limiting
    reagent converted to ester."""
    # TODO: with x mol of ester formed, k = x (water0 + x) / ((acid0 - x)(alcohol0 - x)).
    # TODO: Rearrange to a x^2 + b x + c = 0 with a = k - 1, b = -(k (acid0 + alcohol0) + water0),
    # TODO: c = k acid0 alcohol0. Take the root between 0 and min(acid0, alcohol0). Careful when k == 1.
    raise NotImplementedError("write this part")


ANSWERS = {
    "a benzoic acid + SOCl2": "",
    "b acetyl chloride + dimethylamine (2 equiv)": "",
    "c salicylic acid + acetic anhydride": "",
    "d ethyl benzoate + NaOH/water, heat, then HCl": "",
    "e ethyl acetate + LiAlH4, then water (the product from the acyl part)": "",
}
KEYS = {
    "a benzoic acid + SOCl2": "83dfdb4fc675bd56",
    "b acetyl chloride + dimethylamine (2 equiv)": "c67b7b2d299cd279",
    "c salicylic acid + acetic anhydride": "56de9fefcf1645df",
    "d ethyl benzoate + NaOH/water, heat, then HCl": "fb7121a404676cf4",
    "e ethyl acetate + LiAlH4, then water (the product from the acyl part)": "ab1de819ede91df4",
}


def main():
    print("Carboxylic acids: % as carboxylate at stomach pH 1.5, at pH 4.0 and in blood (pH 7.4)")
    for name, pka in ACIDS:
        vals = [attempt(percent_ionised, pka, ph) for ph in (1.5, 4.0, 7.4)]
        shown = "  ".join(f"{v:7.2f} %" if v != "TODO" else "   TODO" for v in vals)
        print(f"  {name:22s} pKa {pka:5.2f}  {shown}")

    print("\nAcyl reactivity ladder (most reactive first), ranked by the pKa of H-Y")
    for name, lg, conj, pka in sorted(DERIVATIVES, key=lambda d: d[3]):
        print(f"  {name:22s} leaving group {lg:6s} (pKa of {conj} about {pka})")

    print("\nFischer esterification, K = 4.0, 1.00 mol acetic acid")
    for alcohol in (1.0, 2.0, 3.0, 10.0):
        y = attempt(ester_yield, 4.0, 1.0, alcohol)
        print(f"  {alcohol:5.1f} mol ethanol: yield {y if y == 'TODO' else f'{100 * y:5.1f} %'}")
    y = attempt(ester_yield, 4.0, 1.0, 1.0, 5.0)
    print(f"  1.0 mol ethanol but 5.0 mol water present at the start: "
          f"{y if y == 'TODO' else f'{100 * y:5.1f} %'}")
    print("\nProduct drill")
    check_drill(ANSWERS, KEYS)


if __name__ == "__main__":
    main()
