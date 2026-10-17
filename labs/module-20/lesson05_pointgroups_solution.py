"""Lesson 20.5 - find symmetry elements and assign point groups with the flowchart (reference solution).

spec20.symmetry_elements() finds the elements of a molecule from its 3D coordinates; you turn the
elements into a point group with the standard flowchart.

Run:  py lesson05_pointgroups_solution.py            (the eight lesson molecules)
      py lesson05_pointgroups_solution.py practical  (the ten molecules of the module practical)
"""
import sys

from molecules20 import EXPECTED, LESSON05, PRACTICAL
from spec20 import symmetry_elements

PAR = 0.02     # tolerance on |cos| for parallel / perpendicular directions


def point_group(el):
    """Point group name (e.g. 'C2v', 'D3h', 'Td', 'Cinfv') from the dict returned by symmetry_elements()."""
    if el["linear"]:
        return "Dinfh" if el["inversion"] else "Cinfv"
    axes, planes, improper = el["axes"], el["planes"], el["improper"]
    high = [n for n, _ in axes if n >= 3]
    if len(high) > 1:                                   # several C3 or higher axes: cubic groups
        if 5 in high:
            return "Ih" if el["inversion"] else "I"
        if 4 in high:
            return "Oh" if el["inversion"] else "O"
        if el["inversion"]:
            return "Th"
        return "Td" if planes else "T"
    if not axes:                                        # no proper axis at all
        if planes:
            return "Cs"
        return "Ci" if el["inversion"] else "C1"
    n = max(k for k, _ in axes)
    candidates = [d for k, d in axes if k == n]
    # with several equal axes (D2, D2h, D2d) prefer one that is coaxial with an S_2n axis
    main = next((d for d in candidates for k, s in improper if k == 2 * n and abs(abs(d @ s) - 1) < PAR),
                candidates[0])
    perp_c2 = [d for k, d in axes if k % 2 == 0 and abs(d @ main) < PAR]
    sigma_h = any(abs(abs(p @ main) - 1) < PAR for p in planes)
    sigma_v = [p for p in planes if abs(p @ main) < PAR]
    if len(perp_c2) >= n:
        if sigma_h:
            return f"D{n}h"
        return f"D{n}d" if len(sigma_v) >= n else f"D{n}"
    if sigma_h:
        return f"C{n}h"
    if len(sigma_v) >= n:
        return f"C{n}v"
    if any(k == 2 * n and abs(abs(main @ s) - 1) < PAR for k, s in improper):
        return f"S{2 * n}"
    return f"C{n}"


def describe(el):
    """Short text summary of the elements found, e.g. '1 C3, 3 C2, 1 S3, 4 sigma'."""
    if el["linear"]:
        return "linear, C-infinity axis" + (", i" if el["inversion"] else "")
    counts = {}
    for n, _ in el["axes"]:
        counts[f"C{n}"] = counts.get(f"C{n}", 0) + 1
    for n, _ in el["improper"]:
        counts[f"S{n}"] = counts.get(f"S{n}", 0) + 1
    parts = [f"{v} {k}" for k, v in sorted(counts.items(), key=lambda kv: (kv[0][0], -int(kv[0][1:])))]
    if el["planes"]:
        parts.append(f"{len(el['planes'])} sigma")
    if el["inversion"]:
        parts.append("i")
    return ", ".join(parts) if parts else "E only"


def main():
    mols = PRACTICAL if "practical" in sys.argv[1:] else LESSON05
    ok = 0
    for name, mol in mols.items():
        el = symmetry_elements(mol)
        pg = point_group(el)
        good = pg == EXPECTED[name]
        ok += good
        print(f"{name:16s} {describe(el):40s} -> {pg:6s} {'OK' if good else 'expected ' + EXPECTED[name]}")
    print(f"{ok}/{len(mols)} point groups correct")


if __name__ == "__main__":
    main()
