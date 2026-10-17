"""Shared helper for the Module 20 labs (molecular spectroscopy and symmetry).

You do not need to edit this file. It holds:
- CODATA 2022 constants and NIST atomic masses (checked 2026-10-17);
- NIST Chemistry WebBook constants of diatomic molecules (Huber and Herzberg, with NIST updates);
- term values for a vibrating rotor;
- a finite-difference solver for one-dimensional wavefunctions (used for Franck-Condon factors);
- a symmetry-element finder for a set of atoms;
- character tables for the point groups used in lesson 20.6.
"""
import csv
import itertools
import math
from pathlib import Path

import numpy as np
from scipy.linalg import eigh_tridiagonal

HERE = Path(__file__).resolve().parent

# ---------------- CODATA 2022 via NIST (https://physics.nist.gov/cuu/Constants/) ----------------
H = 6.62607015e-34          # J s (exact)
C = 299792458.0             # m/s (exact)
C_CM = C * 100              # cm/s
K_B = 1.380649e-23          # J/K (exact)
N_A = 6.02214076e23         # 1/mol (exact)
U = 1.66053906892e-27       # kg, atomic mass constant
HC_K = H * C_CM / K_B       # second radiation constant, cm K (1.438777)
CM1_TO_KJMOL = H * C_CM * N_A / 1000   # 1 cm^-1 = 0.0119627 kJ/mol

# ---------------- NIST atomic masses (u), Atomic Weights and Isotopic Compositions ----------------
MASS = {"H": 1.00782503223, "D": 2.01410177812, "C": 12.0, "13C": 13.00335483507,
        "N": 14.00307400443, "O": 15.99491461957, "F": 18.99840316273,
        "35Cl": 34.968852682, "37Cl": 36.965902602, "Cl": 34.968852682, "127I": 126.9044719,
        "Br": 78.9183376, "B": 11.00930536, "S": 31.9720711744, "Xe": 131.9041550856, "P": 30.97376199842}

# ---------------- NIST WebBook constants of diatomic molecules (cm^-1, r_e in angstrom) ----------------
# HCl: https://webbook.nist.gov/cgi/cbook.cgi?ID=C7647010&Mask=1000  (H35Cl, X 1Sigma+)
# CO:  https://webbook.nist.gov/cgi/cbook.cgi?ID=C630080&Mask=1000   (12C16O, X 1Sigma+)
# N2:  https://webbook.nist.gov/cgi/cbook.cgi?ID=C7727379&Mask=1000  (14N2, X 1Sigma_g+)
# I2:  https://webbook.nist.gov/cgi/cbook.cgi?ID=C7553562&Mask=1000  (127I2, X 1Sigma_g+ and B 3Pi0u+)
DIATOMIC = {
    "HCl": dict(atoms=("H", "35Cl"), Te=0.0, we=2990.9463, wexe=52.8186, weye=0.22437,
                Be=10.593416, ae=0.307181, De=5.3194e-4, re=1.274552),
    "CO": dict(atoms=("C", "O"), Te=0.0, we=2169.81358, wexe=13.28831, weye=0.0,
               Be=1.93128087, ae=0.01750441, De=6.12147e-6, re=1.128323),
    "N2": dict(atoms=("N", "N"), Te=0.0, we=2358.57, wexe=14.324, weye=-2.26e-3,
               Be=1.998241, ae=0.017318, De=5.76e-6, re=1.097685),
    "I2_X": dict(atoms=("127I", "127I"), Te=0.0, we=214.502, wexe=0.6147, weye=0.0,
                 Be=0.037372, ae=0.0001138, De=4.25e-9, re=2.6663),
    "I2_B": dict(atoms=("127I", "127I"), Te=15769.01, we=125.697, wexe=0.7642, weye=0.0,
                 Be=0.029039, ae=0.0001582, De=5.43e-9, re=3.0247),
}


def reduced_mass(a, b):
    """Reduced mass in u of two atoms given by their MASS keys."""
    return MASS[a] * MASS[b] / (MASS[a] + MASS[b])


def G(mol, v):
    """Vibrational term value G(v) in cm^-1 (measured from the potential minimum)."""
    d = DIATOMIC[mol]
    x = v + 0.5
    return d["we"] * x - d["wexe"] * x**2 + d["weye"] * x**3


def B_v(mol, v):
    """Rotational constant of level v, B_v = B_e - alpha_e (v + 1/2), in cm^-1."""
    d = DIATOMIC[mol]
    return d["Be"] - d["ae"] * (v + 0.5)


def term(mol, v, J):
    """Rovibrational term value G(v) + F_v(J) in cm^-1, with centrifugal distortion."""
    d = DIATOMIC[mol]
    jj = J * (J + 1)
    return G(mol, v) + B_v(mol, v) * jj - d["De"] * jj**2


def bond_length_from_B(B_cm, mu_u):
    """Bond length in angstrom from a rotational constant (cm^-1) and reduced mass (u)."""
    inertia = H / (8 * math.pi**2 * C_CM * B_cm)          # kg m^2
    return math.sqrt(inertia / (mu_u * U)) * 1e10


def read_csv(name):
    """Read a CSV file from this folder, skipping lines that start with '#'."""
    with open(HERE / name, encoding="utf-8") as f:
        rows = [line for line in f if not line.startswith("#")]
    return list(csv.DictReader(rows))


# ---------------- 1D Schroedinger solver (finite differences, as in Module 12) ----------------
HB2M_U_CM_A2 = (H / (2 * math.pi))**2 / (2 * U) / (H * C_CM) * 1e20   # hbar^2/(2 u) in cm^-1 A^2


def solve_1d(x, V, mu_u, n_states):
    """Lowest n_states levels (cm^-1) and normalised wavefunctions for potential V (cm^-1) on grid x (A)."""
    dx = x[1] - x[0]
    t = HB2M_U_CM_A2 / mu_u / dx**2
    E, psi = eigh_tridiagonal(2 * t + V, -t * np.ones(len(x) - 1), select="i",
                              select_range=(0, n_states - 1))
    psi = psi / math.sqrt(dx)
    for k in range(psi.shape[1]):
        if psi[np.argmax(np.abs(psi[:, k]) > 0.3 * np.abs(psi[:, k]).max()), k] < 0:
            psi[:, k] *= -1
    return E, psi


def morse(x, De, a, re, Te=0.0):
    """Morse potential in cm^-1: Te + De (1 - exp(-a (x - re)))^2."""
    return Te + De * (1 - np.exp(-a * (x - re)))**2


def morse_from_constants(mol):
    """Morse parameters (De, a, re, Te) from we and wexe: De = we^2/(4 wexe), a = sqrt(2 mu wexe hc)/hbar."""
    d = DIATOMIC[mol]
    De = d["we"]**2 / (4 * d["wexe"])
    mu = reduced_mass(*d["atoms"])
    a = math.sqrt(d["wexe"] / (HB2M_U_CM_A2 / mu))     # 1/A
    return De, a, d["re"], d["Te"]


# ---------------- symmetry elements of a set of atoms ----------------
def _rot(axis, angle):
    ax = axis / np.linalg.norm(axis)
    K = np.array([[0, -ax[2], ax[1]], [ax[2], 0, -ax[0]], [-ax[1], ax[0], 0]])
    return np.eye(3) + math.sin(angle) * K + (1 - math.cos(angle)) * K @ K


def _refl(normal):
    n = normal / np.linalg.norm(normal)
    return np.eye(3) - 2 * np.outer(n, n)


def _maps(labels, X, M, tol):
    Y = X @ M.T
    for lab, y in zip(labels, Y):
        d = np.linalg.norm(X - y, axis=1)
        if not any(d[j] < tol and labels[j] == lab for j in range(len(labels))):
            return False
    return True


def _unique(vectors, tol=1e-3):
    out = []
    for v in vectors:
        n = np.linalg.norm(v)
        if n < tol:
            continue
        v = v / n
        if not any(abs(abs(v @ u) - 1) < tol for u in out):
            out.append(v)
    return out


def symmetry_elements(molecule, tol=0.02):
    """Find the symmetry elements of a molecule given as a list of (label, x, y, z) in angstrom.

    Returns a dict:
      linear (bool), inversion (bool),
      axes: list of (n, unit vector) for every proper axis Cn, n = 2..8 (highest n per direction),
      planes: list of unit normals of mirror planes,
      improper: list of (n, unit vector) for S_n axes with n >= 3 (S_2 is inversion, S_1 a plane)."""
    labels = [a[0] for a in molecule]
    X = np.array([a[1:] for a in molecule], float)
    w = np.array([MASS.get(l, MASS.get(l.rstrip("0123456789"), 1.0)) for l in labels])
    X = X - (w[:, None] * X).sum(0) / w.sum()
    # candidate directions: atoms, pair midpoints, cross products, differences, face centres, inertia axes
    cand = list(X) + [X[i] + X[j] for i, j in itertools.combinations(range(len(X)), 2)]
    cand += [np.cross(X[i], X[j]) for i, j in itertools.combinations(range(len(X)), 2)]
    cand += [X[i] - X[j] for i, j in itertools.combinations(range(len(X)), 2) if labels[i] == labels[j]]
    cand += [X[i] + X[j] + X[k] for i, j, k in itertools.combinations(range(len(X)), 3)
             if labels[i] == labels[j] == labels[k]]
    inertia = sum(wi * (xi @ xi * np.eye(3) - np.outer(xi, xi)) for wi, xi in zip(w, X))
    cand += list(np.linalg.eigh(inertia)[1].T) + list(np.eye(3))
    dirs = _unique(cand)
    rank = np.linalg.matrix_rank(X, tol=0.05) if len(X) > 1 else 0
    linear = rank <= 1
    res = dict(linear=linear, inversion=_maps(labels, X, -np.eye(3), tol), axes=[], planes=[], improper=[])
    if linear:
        return res
    for d in dirs:
        best = max([n for n in range(2, 9) if _maps(labels, X, _rot(d, 2 * math.pi / n), tol)], default=0)
        if best:
            res["axes"].append((best, d))
        if _maps(labels, X, _refl(d), tol):
            res["planes"].append(d)
        s = max([n for n in range(3, 17) if _maps(labels, X, _refl(d) @ _rot(d, 2 * math.pi / n), tol)],
                default=0)
        if s:
            res["improper"].append((s, d))
    return res


# ---------------- character tables (lesson 20.6) ----------------
# Each table: classes as (name, number of operations, contribution of one unmoved atom to Gamma_3N),
# then irreps as (name, characters, linear functions, quadratic functions).
def _chi(kind, n=1):
    """Contribution of one unmoved atom to Gamma_3N: 1 + 2cos(2pi/n) for Cn, -1 + 2cos(2pi/n) for Sn."""
    if kind == "E":
        return 3
    if kind == "i":
        return -3
    if kind == "s":
        return 1
    th = 2 * math.pi / n
    return round(1 + 2 * math.cos(th)) if kind == "C" else round(-1 + 2 * math.cos(th))


TABLES = {
    "C2v": dict(classes=[("E", 1, _chi("E")), ("C2", 1, _chi("C", 2)), ("sv(xz)", 1, 1), ("sv'(yz)", 1, 1)],
                irreps=[("A1", [1, 1, 1, 1], "z", "x2,y2,z2"), ("A2", [1, 1, -1, -1], "Rz", "xy"),
                        ("B1", [1, -1, 1, -1], "x,Ry", "xz"), ("B2", [1, -1, -1, 1], "y,Rx", "yz")]),
    "C3v": dict(classes=[("E", 1, 3), ("2C3", 2, _chi("C", 3)), ("3sv", 3, 1)],
                irreps=[("A1", [1, 1, 1], "z", "x2+y2,z2"), ("A2", [1, 1, -1], "Rz", ""),
                        ("E", [2, -1, 0], "x,y,Rx,Ry", "x2-y2,xy,xz,yz")]),
    "C2h": dict(classes=[("E", 1, 3), ("C2", 1, -1), ("i", 1, -3), ("sh", 1, 1)],
                irreps=[("Ag", [1, 1, 1, 1], "Rz", "x2,y2,z2,xy"), ("Bg", [1, -1, 1, -1], "Rx,Ry", "xz,yz"),
                        ("Au", [1, 1, -1, -1], "z", ""), ("Bu", [1, -1, -1, 1], "x,y", "")]),
    "D2h": dict(classes=[("E", 1, 3), ("C2(z)", 1, -1), ("C2(y)", 1, -1), ("C2(x)", 1, -1), ("i", 1, -3),
                         ("s(xy)", 1, 1), ("s(xz)", 1, 1), ("s(yz)", 1, 1)],
                irreps=[("Ag", [1, 1, 1, 1, 1, 1, 1, 1], "", "x2,y2,z2"),
                        ("B1g", [1, 1, -1, -1, 1, 1, -1, -1], "Rz", "xy"),
                        ("B2g", [1, -1, 1, -1, 1, -1, 1, -1], "Ry", "xz"),
                        ("B3g", [1, -1, -1, 1, 1, -1, -1, 1], "Rx", "yz"),
                        ("Au", [1, 1, 1, 1, -1, -1, -1, -1], "", ""),
                        ("B1u", [1, 1, -1, -1, -1, -1, 1, 1], "z", ""),
                        ("B2u", [1, -1, 1, -1, -1, 1, -1, 1], "y", ""),
                        ("B3u", [1, -1, -1, 1, -1, 1, 1, -1], "x", "")]),
    "D3h": dict(classes=[("E", 1, 3), ("2C3", 2, 0), ("3C2", 3, -1), ("sh", 1, 1), ("2S3", 2, _chi("S", 3)),
                         ("3sv", 3, 1)],
                irreps=[("A1'", [1, 1, 1, 1, 1, 1], "", "x2+y2,z2"), ("A2'", [1, 1, -1, 1, 1, -1], "Rz", ""),
                        ("E'", [2, -1, 0, 2, -1, 0], "x,y", "x2-y2,xy"),
                        ("A1''", [1, 1, 1, -1, -1, -1], "", ""), ("A2''", [1, 1, -1, -1, -1, 1], "z", ""),
                        ("E''", [2, -1, 0, -2, 1, 0], "Rx,Ry", "xz,yz")]),
    "Td": dict(classes=[("E", 1, 3), ("8C3", 8, 0), ("3C2", 3, -1), ("6S4", 6, _chi("S", 4)), ("6sd", 6, 1)],
               irreps=[("A1", [1, 1, 1, 1, 1], "", "x2+y2+z2"), ("A2", [1, 1, 1, -1, -1], "", ""),
                       ("E", [2, -1, 2, 0, 0], "", "2z2-x2-y2,x2-y2"),
                       ("T1", [3, 0, -1, 1, -1], "Rx,Ry,Rz", ""), ("T2", [3, 0, -1, -1, 1], "x,y,z", "xy,xz,yz")]),
    "D4h": dict(classes=[("E", 1, 3), ("2C4", 2, 1), ("C2", 1, -1), ("2C2'", 2, -1), ("2C2''", 2, -1),
                         ("i", 1, -3), ("2S4", 2, -1), ("sh", 1, 1), ("2sv", 2, 1), ("2sd", 2, 1)],
                irreps=[("A1g", [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], "", "x2+y2,z2"),
                        ("A2g", [1, 1, 1, -1, -1, 1, 1, 1, -1, -1], "Rz", ""),
                        ("B1g", [1, -1, 1, 1, -1, 1, -1, 1, 1, -1], "", "x2-y2"),
                        ("B2g", [1, -1, 1, -1, 1, 1, -1, 1, -1, 1], "", "xy"),
                        ("Eg", [2, 0, -2, 0, 0, 2, 0, -2, 0, 0], "Rx,Ry", "xz,yz"),
                        ("A1u", [1, 1, 1, 1, 1, -1, -1, -1, -1, -1], "", ""),
                        ("A2u", [1, 1, 1, -1, -1, -1, -1, -1, 1, 1], "z", ""),
                        ("B1u", [1, -1, 1, 1, -1, -1, 1, -1, -1, 1], "", ""),
                        ("B2u", [1, -1, 1, -1, 1, -1, 1, -1, 1, -1], "", ""),
                        ("Eu", [2, 0, -2, 0, 0, -2, 0, 2, 0, 0], "x,y", "")]),
    "Oh": dict(classes=[("E", 1, 3), ("8C3", 8, 0), ("6C2", 6, -1), ("6C4", 6, 1), ("3C2=C4^2", 3, -1),
                        ("i", 1, -3), ("6S4", 6, -1), ("8S6", 8, 0), ("3sh", 3, 1), ("6sd", 6, 1)],
               irreps=[("A1g", [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], "", "x2+y2+z2"),
                       ("A2g", [1, 1, -1, -1, 1, 1, -1, 1, 1, -1], "", ""),
                       ("Eg", [2, -1, 0, 0, 2, 2, 0, -1, 2, 0], "", "2z2-x2-y2,x2-y2"),
                       ("T1g", [3, 0, -1, 1, -1, 3, 1, 0, -1, -1], "Rx,Ry,Rz", ""),
                       ("T2g", [3, 0, 1, -1, -1, 3, -1, 0, -1, 1], "", "xy,xz,yz"),
                       ("A1u", [1, 1, 1, 1, 1, -1, -1, -1, -1, -1], "", ""),
                       ("A2u", [1, 1, -1, -1, 1, -1, 1, -1, -1, 1], "", ""),
                       ("Eu", [2, -1, 0, 0, 2, -2, 0, 1, -2, 0], "", ""),
                       ("T1u", [3, 0, -1, 1, -1, -3, -1, 0, 1, 1], "x,y,z", ""),
                       ("T2u", [3, 0, 1, -1, -1, -3, 1, 0, 1, -1], "", "")]),
}


def check_tables():
    """Great orthogonality test: sum over classes of g_k chi_i chi_j = h delta_ij for every table."""
    for name, t in TABLES.items():
        g = np.array([c[1] for c in t["classes"]])
        chars = np.array([ir[1] for ir in t["irreps"]], float)
        gram = (chars * g) @ chars.T
        assert np.allclose(gram, g.sum() * np.eye(len(chars))), name
    return True


if __name__ == "__main__":
    check_tables()
    print("character tables orthonormal: OK")
    print(f"hc/k = {HC_K:.6f} cm K, 1 cm-1 = {CM1_TO_KJMOL:.7f} kJ/mol")
    for m in ("HCl", "CO"):
        mu = reduced_mass(*DIATOMIC[m]["atoms"])
        print(f"{m}: mu = {mu:.6f} u, r_e from B_e = {bond_length_from_B(DIATOMIC[m]['Be'], mu):.4f} A")
