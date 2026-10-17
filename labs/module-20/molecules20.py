"""Idealised 3D geometries (angstrom) for the Module 20 symmetry labs.

Bond lengths and angles are rounded textbook values; the symmetry, not the exact numbers, is what matters.
Each molecule is a list of (element, x, y, z). LESSON05 is the set for lesson 20.5, PRACTICAL the ten
molecules of the module practical in lesson 20.6. EXPECTED gives the answers for checking.
"""
import math

T = 1 / math.sqrt(3)          # direction cosine of a tetrahedral bond


def _tetra(center_label, ligands, lengths):
    dirs = [(T, T, T), (T, -T, -T), (-T, T, -T), (-T, -T, T)]
    return [(center_label, 0.0, 0.0, 0.0)] + [(lab, L * d[0], L * d[1], L * d[2])
                                                for lab, L, d in zip(ligands, lengths, dirs)]


def _ring(label, r, n, z=0.0, phase=0.0):
    return [(label, r * math.cos(phase + 2 * math.pi * k / n), r * math.sin(phase + 2 * math.pi * k / n), z)
            for k in range(n)]


def water():
    return [("O", 0, 0, 0), ("H", 0.757, 0.586, 0), ("H", -0.757, 0.586, 0)]


def ammonia():
    return [("N", 0, 0, 0.38)] + _ring("H", 0.94, 3)


def methane():
    return _tetra("C", ["H"] * 4, [1.09] * 4)


def boron_trifluoride():
    return [("B", 0, 0, 0)] + _ring("F", 1.31, 3)


def ethene():
    return [("C", 0.667, 0, 0), ("C", -0.667, 0, 0), ("H", 1.23, 0.92, 0), ("H", 1.23, -0.92, 0),
            ("H", -1.23, 0.92, 0), ("H", -1.23, -0.92, 0)]


def bromochlorofluoromethane():
    return _tetra("C", ["H", "F", "Cl", "Br"], [1.09, 1.35, 1.76, 1.93])


def hydrogen_cyanide():
    return [("H", 0, 0, -1.066), ("C", 0, 0, 0), ("N", 0, 0, 1.156)]


def dichloromethane():
    s, c = math.sin(math.radians(54.5)), math.cos(math.radians(54.5))
    return [("C", 0, 0, 0), ("H", 1.09 * s, 0, 1.09 * c), ("H", -1.09 * s, 0, 1.09 * c),
            ("Cl", 0, 1.77 * s, -1.77 * c), ("Cl", 0, -1.77 * s, -1.77 * c)]


def sulfur_hexafluoride():
    d = 1.56
    return [("S", 0, 0, 0), ("F", d, 0, 0), ("F", -d, 0, 0), ("F", 0, d, 0), ("F", 0, -d, 0),
            ("F", 0, 0, d), ("F", 0, 0, -d)]


def xenon_tetrafluoride():
    return [("Xe", 0, 0, 0)] + _ring("F", 1.95, 4)


def benzene():
    return _ring("C", 1.39, 6) + _ring("H", 2.48, 6)


def ethane(staggered=True):
    top = _ring("H", 1.02, 3, z=1.16)
    bottom = _ring("H", 1.02, 3, z=-1.16, phase=math.pi / 3 if staggered else 0.0)
    return [("C", 0, 0, 0.765), ("C", 0, 0, -0.765)] + top + bottom


def trans_dichloroethene():
    return [("C", 0.665, 0, 0), ("C", -0.665, 0, 0), ("H", 1.21, 0.93, 0), ("H", -1.21, -0.93, 0),
            ("Cl", 1.55, -1.45, 0), ("Cl", -1.55, 1.45, 0)]


def hydrogen_peroxide():
    phi = math.radians(111.5) / 2          # half the H-O-O-H dihedral angle
    return [("O", 0, 0.7375, 0), ("O", 0, -0.7375, 0),
            ("H", 0.92 * math.cos(phi), 0.98, 0.92 * math.sin(phi)),
            ("H", 0.92 * math.cos(phi), -0.98, -0.92 * math.sin(phi))]


def allene():
    return [("C", 0, 0, 0), ("C", 0, 0, 1.31), ("C", 0, 0, -1.31), ("H", 0.93, 0, 1.87), ("H", -0.93, 0, 1.87),
            ("H", 0, 0.93, -1.87), ("H", 0, -0.93, -1.87)]


def chloroform():
    return [("C", 0, 0, 0), ("H", 0, 0, 1.07)] + _ring("Cl", 1.67, 3, z=-0.59)


def carbon_dioxide():
    return [("O", 0, 0, -1.16), ("C", 0, 0, 0), ("O", 0, 0, 1.16)]


LESSON05 = {"H2O": water(), "NH3": ammonia(), "CH4": methane(), "BF3": boron_trifluoride(),
            "C2H4": ethene(), "CHFClBr": bromochlorofluoromethane(), "HCN": hydrogen_cyanide(),
            "CH2Cl2": dichloromethane()}

PRACTICAL = {"SF6": sulfur_hexafluoride(), "XeF4": xenon_tetrafluoride(), "C6H6": benzene(),
             "C2H6 staggered": ethane(True), "C2H6 eclipsed": ethane(False),
             "trans-C2H2Cl2": trans_dichloroethene(), "H2O2": hydrogen_peroxide(), "allene": allene(),
             "CHCl3": chloroform(), "CO2": carbon_dioxide()}

EXPECTED = {"H2O": "C2v", "NH3": "C3v", "CH4": "Td", "BF3": "D3h", "C2H4": "D2h", "CHFClBr": "C1",
            "HCN": "Cinfv", "CH2Cl2": "C2v", "SF6": "Oh", "XeF4": "D4h", "C6H6": "D6h",
            "C2H6 staggered": "D3d", "C2H6 eclipsed": "D3h", "trans-C2H2Cl2": "C2h", "H2O2": "C2",
            "allene": "D2d", "CHCl3": "C3v", "CO2": "Dinfh"}
