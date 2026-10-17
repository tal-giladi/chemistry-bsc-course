"""Lesson 20.5 - find symmetry elements and assign point groups with the flowchart.

spec20.symmetry_elements() finds the elements of a molecule from its 3D coordinates; you turn the
elements into a point group with the standard flowchart.

Fill in the functions marked TODO, then run:  py lesson05_pointgroups.py
Reference solution: lesson05_pointgroups_solution.py            (the eight lesson molecules)
      py lesson05_pointgroups_solution.py practical  (the ten molecules of the module practical)
"""
import sys

from molecules20 import EXPECTED, LESSON05, PRACTICAL
from spec20 import symmetry_elements

PAR = 0.02     # tolerance on |cos| for parallel / perpendicular directions


def point_group(el):
    """Point group name (e.g. 'C2v', 'D3h', 'Td', 'Cinfv') from the dict returned by symmetry_elements()."""
    # TODO: follow the flowchart of lesson 20.5. el has keys linear, inversion (bools), axes [(n, unit vector)],
    # TODO: planes [unit normal], improper [(n, unit vector)]. Use d1 @ d2 for the cosine between two directions.
    # TODO: 1. linear: 'Dinfh' with inversion, else 'Cinfv'
    # TODO: 2. more than one axis with n >= 3: 'Oh' if some n == 4 and inversion, 'Td' if planes, else 'T' (or 'Ih'/'Th')
    # TODO: 3. no axes: 'Cs' with a plane, 'Ci' with inversion, else 'C1'
    # TODO: 4. principal axis = highest n (if several, take one coaxial with an S_2n axis, see PAR)
    # TODO: 5. count C2 axes perpendicular to it (|cos| < PAR): n or more -> D groups (Dnh if sigma_h, Dnd if n sigma_v, Dn)
    # TODO: 6. otherwise C groups: Cnh if sigma_h, Cnv if n planes contain the axis, S2n if an S2n axis, else Cn
    # TODO: return the name as a string, e.g. 'C2v'
    return None


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
    if point_group({"linear": True, "inversion": True, "axes": [], "planes": [], "improper": []}) is None:
        print("TODO: write point_group() first.")
        return
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
