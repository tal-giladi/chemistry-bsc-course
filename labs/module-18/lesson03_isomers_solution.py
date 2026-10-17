"""Lesson 18.3 reference solution: count the isomers of an octahedral complex by symmetry.

Run (from this folder):
    py lesson03_isomers_solution.py                  # the standard table
    py lesson03_isomers_solution.py A A B B C C      # any six monodentate ligands
    py lesson03_isomers_solution.py en en B B        # 'en' (or any name in CHELATES) spans two cis positions

Idea: write every way of placing the ligands on the six positions, then treat two placements as the same
isomer if a rotation of the octahedron turns one into the other. Rotations only (24 of them, group O)
count mirror images separately, so a chiral complex gives 2; adding reflections (48, group Oh) merges
each mirror pair. The difference is the number of enantiomer pairs.
"""
import itertools
import sys

from inorg18 import is_cis, octahedral_operations

CHELATES = {"en", "ox", "bpy", "phen", "AA"}     # symmetric bidentate ligands
ROTATIONS = octahedral_operations(proper_only=True)
ALL_OPS = octahedral_operations(proper_only=False)


def placements(ligands):
    """Every placement of the ligands. A placement is (labels, rings): labels[i] is the ligand name on
    position i, rings is a frozenset of the position pairs joined by a chelate."""
    chel = [x for x in ligands if x in CHELATES]
    mono = [x for x in ligands if x not in CHELATES]
    if len(mono) + 2 * len(chel) != 6:
        raise ValueError("ligands must fill exactly six positions (a chelate counts two)")
    results = set()

    def place_chelates(k, free, labels, rings):
        if k == len(chel):
            for perm in set(itertools.permutations(mono)):
                lab = list(labels)
                for pos, name in zip(sorted(free), perm):
                    lab[pos] = name
                results.add((tuple(lab), frozenset(rings)))
            return
        for i, j in itertools.combinations(sorted(free), 2):
            if is_cis(i, j):
                lab = list(labels)
                lab[i] = lab[j] = chel[k]
                place_chelates(k + 1, free - {i, j}, lab, rings | {(i, j)})

    place_chelates(0, set(range(6)), [None] * 6, frozenset())
    return results


def apply(op, placement):
    """The placement after symmetry operation op (op[i] = where position i goes)."""
    labels, rings = placement
    new = [None] * 6
    for i, name in enumerate(labels):
        new[op[i]] = name
    new_rings = frozenset(tuple(sorted((op[i], op[j]))) for i, j in rings)
    return tuple(new), new_rings


def canonical(placement, ops):
    """A label shared by all placements related by the operations: the smallest image under ops.
    Images are compared as (labels, sorted list of rings)."""
    images = []
    for op in ops:
        labels, rings = apply(op, placement)
        images.append((labels, tuple(sorted(rings))))
    return min(images)


def count_isomers(ligands):
    """(stereoisomers counting enantiomers separately, isomers with mirror pairs merged)."""
    ps = placements(ligands)
    stereo = {canonical(p, ROTATIONS) for p in ps}
    geometric = {canonical(p, ALL_OPS) for p in ps}
    return len(stereo), len(geometric)


def describe(ligands):
    n_stereo, n_geo = count_isomers(ligands)
    pairs = n_stereo - n_geo
    return f"{n_stereo:>3} stereoisomers = {n_geo:>2} if mirror images are merged, {pairs} enantiomer pair(s)"


def main():
    if len(sys.argv) > 1:
        lig = sys.argv[1:]
        print(f"M{''.join(lig)}: {describe(lig)}")
        return
    cases = {
        "MA6       e.g. [Co(NH3)6]3+": "A A A A A A",
        "MA5B      e.g. [Co(NH3)5Cl]2+": "A A A A A B",
        "MA4B2     e.g. [Co(NH3)4Cl2]+": "A A A A B B",
        "MA3B3     e.g. [Co(NH3)3(NO2)3]": "A A A B B B",
        "MA2B2C2": "A A B B C C",
        "M(AA)3    e.g. [Co(en)3]3+": "en en en",
        "M(AA)2B2  e.g. [Co(en)2Cl2]+": "en en B B",
        "M(AA)B4   e.g. [Co(en)(NH3)4]3+": "en A A A A",
        "MABCDEF   six different ligands": "A B C D E F",
    }
    print(f"{'formula':<34} result")
    for name, lig in cases.items():
        print(f"{name:<34} {describe(lig.split())}")


if __name__ == "__main__":
    main()
