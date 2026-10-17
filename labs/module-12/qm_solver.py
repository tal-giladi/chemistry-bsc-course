"""Reference finite-difference solver for the 1D time-independent Schroedinger equation.

    -c d^2 psi/dx^2 + V(x) psi = E psi,      c = hbar^2 / (2 m)

The solver is unit-agnostic: give x, V and c in consistent units (for example x in nm, V in eV
and c = HB2M_E_EV_NM2 / mass_in_electron_masses). The wavefunction is taken to be zero just
outside the grid, so the grid must reach far enough into the walls.

This is the solution of the lesson 12.2 exercise. Lessons 12.3-12.6 import it.
"""
import csv

import numpy as np
from scipy.linalg import eigh_tridiagonal

# CODATA 2022 (NIST), checked 2026-10-17
H = 6.62607015e-34            # J s, exact
HBAR = H / (2 * np.pi)        # J s
C_LIGHT = 299792458.0         # m/s, exact
E_CHARGE = 1.602176634e-19    # C, exact
M_E = 9.1093837139e-31        # kg
M_U = 1.66053906892e-27       # kg
A0_NM = 0.0529177210544       # nm, Bohr radius
HARTREE_EV = 27.211386245981  # eV

HB2M_E_EV_NM2 = HBAR**2 / (2 * M_E) / E_CHARGE * 1e18   # hbar^2/(2 m_e) in eV nm^2 (0.0381)
HB2M_U_CM_A2 = HBAR**2 / (2 * M_U) / (H * C_LIGHT * 100) * 1e20  # hbar^2/(2 u) in cm^-1 A^2 (16.86)


def solve(x, V, c, n_states=6):
    """Lowest n_states eigenvalues and normalised eigenvectors on a uniform grid x.
    Returns E (shape n_states) and psi (shape len(x) x n_states), with sum(psi^2) dx = 1."""
    x = np.asarray(x, float)
    dx = x[1] - x[0]
    t = c / dx**2
    diag = 2 * t + np.asarray(V, float)
    off = -t * np.ones(len(x) - 1)
    E, psi = eigh_tridiagonal(diag, off, select="i", select_range=(0, n_states - 1))
    psi = psi / np.sqrt(dx)
    for k in range(psi.shape[1]):          # fix the arbitrary sign: first big lobe positive
        i = np.argmax(np.abs(psi[:, k]) > 0.1 * np.abs(psi[:, k]).max())
        if psi[i, k] < 0:
            psi[:, k] *= -1
    return E, psi


def count_nodes(psi, tol=1e-6):
    """Number of sign changes of psi, ignoring the tiny tails."""
    p = psi[np.abs(psi) > tol * np.abs(psi).max()]
    return int(np.sum(p[1:] * p[:-1] < 0))


def read_csv(path):
    """Rows of a small CSV file as dicts, skipping lines that start with '#'."""
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(line for line in f if not line.startswith("#")))
