"""Shared helpers for the Module 23 labs (Physical Chemistry Lab 1). Keep this file next to the lesson scripts.

Constants: CODATA 2022 exact values (https://physics.nist.gov/cuu/Constants/), checked 2026-10-17.
"""
import csv
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
R = 8.314462618          # J/(mol K), exact (N_A k_B)
K_B = 1.380649e-23       # J/K, exact
N_A = 6.02214076e23      # 1/mol, exact
F = 96485.33212          # C/mol, exact (N_A e)
C_WATER = 4.184          # J/(g K), specific heat of water near 25 C


def read_csv(path):
    """Read a CSV file into a list of dicts (strings); convert columns yourself."""
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def column(rows, name, cast=float):
    return np.array([cast(r[name]) for r in rows])


def linfit(x, y):
    """Least-squares line y = a + b x. Returns (a, b, sa, sb, cov_ab, s_residual)."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    if len(x) < 3:                       # a line through two points has no uncertainty estimate
        b, a = np.polyfit(x, y, 1)
        return float(a), float(b), float("nan"), float("nan"), float("nan"), float("nan")
    (b, a), cov = np.polyfit(x, y, 1, cov=True)
    resid = y - (a + b * x)
    s = float(np.sqrt(np.sum(resid ** 2) / max(1, len(x) - 2)))
    return float(a), float(b), float(np.sqrt(cov[1, 1])), float(np.sqrt(cov[0, 0])), float(cov[0, 1]), s


def extrapolate(t, y, t_at, resolution=0.0):
    """Fit a straight line to (t, y) and return its value at t_at with a standard uncertainty.
    `resolution` (display step) adds resolution/sqrt(12) in quadrature."""
    a, b, sa, sb, cab, _ = linfit(t, y)
    value = a + b * t_at
    var = sa ** 2 + (t_at * sb) ** 2 + 2 * t_at * cab + (resolution / np.sqrt(12)) ** 2
    return float(value), float(np.sqrt(var))


def propagate(f, values):
    """Value of f and its standard uncertainty for independent inputs {name: (value, sigma)},
    by numerical partial derivatives: sigma_f^2 = sum_i (df/dx_i sigma_i)^2 (lesson 09.3)."""
    x0 = {k: v for k, (v, _) in values.items()}
    f0 = f(**x0)
    var = 0.0
    for k, (v, s) in values.items():
        if s == 0:
            continue
        h = s * 1e-3
        dfdx = (f(**{**x0, k: v + h}) - f(**{**x0, k: v - h})) / (2 * h)
        var += (dfdx * s) ** 2
    return float(f0), float(np.sqrt(var))


def srgb_to_linear(v):
    """sRGB code value 0-255 to linear intensity 0-1 (IEC 61966-2-1; lesson 09.6)."""
    c = np.asarray(v, float) / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def linear_to_srgb(i):
    i = np.clip(np.asarray(i, float), 0, 1)
    c = np.where(i <= 0.0031308, 12.92 * i, 1.055 * i ** (1 / 2.4) - 0.055)
    return 255.0 * c


def t95(dof):
    """Two-sided 95 % Student t value."""
    from scipy import stats
    return float(stats.t.ppf(0.975, dof))


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
