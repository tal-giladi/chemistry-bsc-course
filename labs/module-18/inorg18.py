"""Shared helpers for the Module 18 labs (Inorganic Chemistry).

Constants are CODATA 2022 values from NIST (https://physics.nist.gov/cuu/Constants/), checked 2026-10-17.
Nothing here needs editing; the lesson files import from it.
"""
import csv
import itertools
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent

# CODATA 2022 (e, h, c, N_A, k exact; epsilon_0 measured)
E = 1.602176634e-19          # C
EPS0 = 8.8541878188e-12      # F/m
NA = 6.02214076e23           # 1/mol
H = 6.62607015e-34           # J s
C = 299792458.0              # m/s
R = 8.314462618              # J/(mol K)
EV_KJ = E * NA / 1000        # 1 eV per particle in kJ/mol = 96.485
CM_KJ = H * C * 100 * NA / 1000   # 1 cm^-1 per particle in kJ/mol = 0.011963
# e^2 N_A / (4 pi eps0) in kJ/mol times angstrom: the Coulomb prefactor for lattice energies
COULOMB_KJ_A = E ** 2 * NA / (4 * math.pi * EPS0) / 1e-10 / 1000   # = 1389.35

SYMBOLS = ("H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn "
           "Ga Ge As Se Br Kr").split()

# Aufbau order up to krypton, as (n, l)
_ORDER = [(1, 0), (2, 0), (2, 1), (3, 0), (3, 1), (4, 0), (3, 2), (4, 1)]
_CAP = {0: 2, 1: 6, 2: 10}


def configuration(z):
    """Ground-state configuration of a neutral atom Z <= 36 as a list of (n, l, count),
    with the two exceptions Cr (3d5 4s1) and Cu (3d10 4s1) from lesson 07.2."""
    if not 1 <= z <= 36:
        raise ValueError("this helper covers H to Kr")
    left, conf = z, []
    for n, l in _ORDER:
        k = min(left, _CAP[l])
        if k:
            conf.append([n, l, k])
        left -= k
        if not left:
            break
    if z in (24, 29):                       # Cr, Cu: one 4s electron moves into 3d
        for item in conf:
            if (item[0], item[1]) == (4, 0):
                item[2] -= 1
            if (item[0], item[1]) == (3, 2):
                item[2] += 1
    return [tuple(x) for x in conf if x[2] > 0]


def config_string(conf):
    letters = "spdf"
    return " ".join(f"{n}{letters[l]}{k}" for n, l, k in sorted(conf, key=lambda t: (t[0], t[1])))


def load_ie(path=HERE / "ionization_energies.csv"):
    """{symbol: (IE1, IE2, IE3)} in eV from the NIST ASD file (None where missing)."""
    out = {}
    with open(path, encoding="utf-8") as f:
        rows = [r for r in f if r.strip() and not r.startswith("#")]
    for row in csv.DictReader(rows):
        out[row["symbol"]] = tuple(float(row[k]) if row[k] else None for k in ("IE1_eV", "IE2_eV", "IE3_eV"))
    return out


def load_csv(name):
    """Read a CSV from this folder, skipping '#' comment lines, as a list of dicts."""
    with open(HERE / name, encoding="utf-8") as f:
        rows = [r for r in f if r.strip() and not r.startswith("#")]
    return list(csv.DictReader(rows))


# ---------- octahedral geometry (lesson 18.3) ----------
# The six positions of an octahedron, as unit vectors: 0 +x, 1 -x, 2 +y, 3 -y, 4 +z, 5 -z
OCT = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]


def _det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def octahedral_operations(proper_only=True):
    """Symmetry operations of the octahedron as permutations of the six positions.
    proper_only=True gives the 24 rotations (group O); False gives all 48 (group Oh, with
    reflections and inversion). Each permutation p sends position i to position p[i]."""
    ops = []
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product((1, -1), repeat=3):
            m = [[0] * 3 for _ in range(3)]
            for row, (col, s) in enumerate(zip(perm, signs)):
                m[row][col] = s
            if proper_only and _det3(m) != 1:
                continue
            p = []
            for v in OCT:
                w = tuple(sum(m[r][c] * v[c] for c in range(3)) for r in range(3))
                p.append(OCT.index(w))
            ops.append(tuple(p))
    return ops


def trans_partner(i):
    """The position opposite position i (trans to it)."""
    return i ^ 1


def is_cis(i, j):
    return i != j and trans_partner(i) != j


# ---------- d-electron counting (lessons 18.3 to 18.5) ----------
GROUP = {"Sc": 3, "Ti": 4, "V": 5, "Cr": 6, "Mn": 7, "Fe": 8, "Co": 9, "Ni": 10, "Cu": 11, "Zn": 12,
         "Y": 3, "Zr": 4, "Nb": 5, "Mo": 6, "Tc": 7, "Ru": 8, "Rh": 9, "Pd": 10, "Ag": 11, "Cd": 12,
         "Hf": 4, "Ta": 5, "W": 6, "Re": 7, "Os": 8, "Ir": 9, "Pt": 10, "Au": 11, "Hg": 12}


def d_count(metal, oxidation_state):
    """d-electron count of a transition-metal ion: group number minus oxidation state."""
    d = GROUP[metal] - oxidation_state
    if not 0 <= d <= 10:
        raise ValueError(f"{metal}({oxidation_state}) gives d{d}, outside 0-10")
    return d


# ---------- colour (lesson 18.5) ----------
# Bands of the visible spectrum (nm), following the MIT 5.111SC lecture 28 handout, and the
# colour seen when that band is removed from white light (opposite on the colour wheel).
BANDS = [(380, 430, "violet", "yellow"), (430, 490, "blue", "orange"), (490, 560, "green", "red-purple"),
         (560, 580, "yellow", "violet"), (580, 620, "orange", "blue"), (620, 780, "red", "green")]


def band_of(nm):
    """(absorbed colour, colour seen) for a single absorption maximum in nm; None outside 380-780 nm."""
    for lo, hi, absorbed, seen in BANDS:
        if lo <= nm < hi:
            return absorbed, seen
    return None


def nm_to_cm1(nm):
    return 1e7 / nm


def cm1_to_nm(cm1):
    return 1e7 / cm1


def spin_only(n_unpaired):
    """Spin-only magnetic moment in Bohr magnetons, sqrt(n(n+2))."""
    return math.sqrt(n_unpaired * (n_unpaired + 2))
