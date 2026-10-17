"""Lesson 17.2 reference solution: IR band positions from Hooke's law, and a band classifier.

Run (from this folder):
    py lesson02_ir_solution.py
"""
import math

C_CM_PER_S = 2.99792458e10   # speed of light in cm/s (exact, SI)
U_KG = 1.66053906892e-27      # atomic mass constant in kg, CODATA 2022
MASS = {"H": 1.008, "D": 2.014, "C": 12.011, "N": 14.007, "O": 15.999}

# Typical stretching force constants in N/m (textbook orders of magnitude, not measurements)
BONDS = [("C-H", "C", "H", 500), ("C-D", "C", "D", 500), ("O-H", "O", "H", 770),
         ("C-O", "C", "O", 500), ("C=O", "C", "O", 1200), ("C=C", "C", "C", 960),
         ("C#N", "C", "N", 1850), ("C#C", "C", "C", 1560)]


def reduced_mass_kg(a, b):
    ma, mb = MASS[a], MASS[b]
    return ma * mb / (ma + mb) * U_KG


def wavenumber(k, a, b):
    """Harmonic stretching wavenumber in cm^-1: (1 / 2 pi c) * sqrt(k / mu)."""
    return math.sqrt(k / reduced_mass_kg(a, b)) / (2 * math.pi * C_CM_PER_S)


def has(peaks, lo, hi, strength=None, shape=None):
    """True if a peak lies in [lo, hi] (and has the given strength 's'/'m'/'w' and shape if asked)."""
    return any(lo <= w <= hi and (strength is None or s in strength) and (shape is None or sh == shape)
               for w, s, sh in peaks)


def classify(peaks):
    """Return the functional-group calls a chemist would make from a list of (cm^-1, strength, shape)."""
    calls = []
    carbonyl = has(peaks, 1650, 1820, "s")
    if has(peaks, 2500, 3300, "sm", "broad") and has(peaks, 1690, 1730, "s"):
        calls.append("carboxylic acid (very broad O-H + C=O)")
    elif has(peaks, 3200, 3550, "sm", "broad") and not carbonyl:
        calls.append("alcohol or phenol (broad O-H, no C=O)")
    if len([p for p in peaks if 3300 <= p[0] <= 3500 and p[2] == "sharp"]) == 2:
        calls.append("primary amine or amide (two N-H bands)")
    if has(peaks, 1735, 1755, "s") and has(peaks, 1000, 1300, "s"):
        calls.append("ester (C=O near 1740 + strong C-O)")
    elif has(peaks, 1720, 1740, "s") and has(peaks, 2700, 2830, "wm"):
        calls.append("aldehyde (C=O + C-H doublet near 2720/2820)")
    elif has(peaks, 1705, 1725, "s"):
        if not calls:
            calls.append("ketone (C=O near 1715)")
    elif has(peaks, 1680, 1700, "s") and has(peaks, 1450, 1600, "m"):
        calls.append("conjugated (aryl) ketone or aldehyde")
    if has(peaks, 2210, 2260, "ms", "sharp"):
        calls.append("nitrile (C#N)")
    if has(peaks, 3260, 3330, "ms", "sharp") and has(peaks, 2100, 2150, "wm"):
        calls.append("terminal alkyne (sharp C-H at 3300 + weak C#C)")
    if has(peaks, 1630, 1680, "wm") and has(peaks, 3010, 3100, "wm") and not carbonyl:
        calls.append("alkene (=C-H above 3000 + C=C)")
    if has(peaks, 1500, 1560, "s") and has(peaks, 1320, 1390, "s"):
        calls.append("nitro group")
    return calls or ["saturated hydrocarbon part only (C-H below 3000)"]


# Six spectra described by their typical band positions (cm^-1, strength, shape),
# as a textbook would list them for a liquid film. They are teaching data, not database records.
UNKNOWNS = {
    "A": [(2960, "s", "sharp"), (2875, "m", "sharp"), (1716, "s", "sharp"), (1365, "m", "sharp")],
    "B": [(3000, "m", "broad"), (2965, "m", "sharp"), (1711, "s", "sharp"), (1290, "m", "sharp"), (935, "m", "broad")],
    "C": [(3330, "s", "broad"), (2960, "s", "sharp"), (2875, "m", "sharp"), (1060, "s", "sharp")],
    "D": [(2985, "m", "sharp"), (2250, "m", "sharp"), (1460, "m", "sharp")],
    "E": [(3310, "s", "sharp"), (2930, "s", "sharp"), (2120, "w", "sharp"), (630, "s", "broad")],
    "F": [(2985, "m", "sharp"), (1742, "s", "sharp"), (1240, "s", "sharp"), (1050, "s", "sharp")],
}


def main():
    print("Part 1 - harmonic wavenumbers from Hooke's law")
    for name, a, b, k in BONDS:
        print(f"  {name:4s} k = {k:5d} N/m  mu = {reduced_mass_kg(a, b) / U_KG:5.2f} u  "
              f"-> {wavenumber(k, a, b):6.0f} cm^-1")
    ratio = wavenumber(500, "C", "H") / wavenumber(500, "C", "D")
    print(f"  C-H / C-D ratio = {ratio:.3f} (a bit less than sqrt(2) = 1.414: mu does not quite double)")

    print("\nPart 2 - classify six described spectra")
    for label, peaks in UNKNOWNS.items():
        print(f"  {label}: " + "; ".join(classify(peaks)))


if __name__ == "__main__":
    main()
