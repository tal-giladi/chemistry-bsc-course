"""Shared helpers for the Module 27 labs (Electromagnetism and Matter). Keep this file next to the lesson scripts.

Constants: CODATA 2022 values from NIST (https://physics.nist.gov/cuu/Constants/), checked 2026-10-17.
e, k_B, N_A and c are exact; eps0 and mu0 are measured (relative uncertainty 1.6e-10).
"""
import csv
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
E = 1.602176634e-19          # C, elementary charge (exact)
K_B = 1.380649e-23           # J/K (exact)
N_A = 6.02214076e23          # 1/mol (exact)
C_LIGHT = 299792458.0        # m/s (exact)
EPS0 = 8.8541878188e-12      # F/m
MU0 = 1.25663706127e-6       # N/A^2
R = N_A * K_B                # J/(mol K)
K_C = 1 / (4 * np.pi * EPS0)  # Coulomb constant, N m^2 C^-2
DEBYE = 1e-21 / C_LIGHT      # C m (1 D = 3.33564e-30 C m)
ANGSTROM = 1e-10             # m
EV = E                       # J per eV
ATM = 101325.0               # Pa


def read_csv(path):
    """Read a CSV file (lines starting with # are comments) into a list of dicts of strings."""
    with open(path, newline="", encoding="utf-8") as fh:
        lines = [ln for ln in fh if not ln.startswith("#")]
    return list(csv.DictReader(lines))


def column(rows, name, cast=float):
    return np.array([cast(r[name]) for r in rows])


def read_charges(path):
    """Point-charge model: columns label,x_A,y_A,z_A,q_e. Returns (labels, positions in m, charges in C)."""
    rows = read_csv(path)
    labels = [r["label"] for r in rows]
    xyz = np.array([[float(r["x_A"]), float(r["y_A"]), float(r["z_A"])] for r in rows]) * ANGSTROM
    q = column(rows, "q_e") * E
    return labels, xyz, q


def linfit(x, y):
    """Least-squares line y = a + b x. Returns (a, b, sa, sb)."""
    (b, a), cov = np.polyfit(np.asarray(x, float), np.asarray(y, float), 1, cov=True)
    return float(a), float(b), float(np.sqrt(cov[1, 1])), float(np.sqrt(cov[0, 0]))


def todo(*results):
    """True if any TODO function still returns None."""
    if any(r is None for r in results):
        print("Some TODO functions still return None: fill them in first (see the docstrings).")
        return True
    return False


def save_plot(fig, name):
    out = HERE / "runs"
    out.mkdir(exist_ok=True)
    fig.tight_layout()
    fig.savefig(out / name, dpi=120)
    print(f"plot written to {out / name}")


def pyplot():
    """matplotlib.pyplot with a file-only backend, or None if matplotlib is missing."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        return plt
    except ImportError:
        print("matplotlib not installed: skipping the plot")
        return None
