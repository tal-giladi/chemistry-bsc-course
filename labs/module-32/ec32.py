"""Shared constants and helpers for the Module 32 labs (electrochemistry and solid state). Keep this file next
to the lesson scripts.

Constants: CODATA 2022 values from NIST (https://physics.nist.gov/cuu/Constants/), checked 2026-10-17.
X-ray wavelengths: NIST X-ray Transition Energies Database, direct experimental values for Cu
(https://physics.nist.gov/PhysRefData/XrayTrans/Html/search.html), checked 2026-10-17.
"""
import csv
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent

# ---------------- CODATA 2022 ----------------
F = 96485.33212               # C/mol, exact (N_A e)
R = 8.314462618               # J/(mol K), exact
K_B_EV = 8.617333262e-5       # eV/K, exact
H = 6.62607015e-34            # J s, exact
C = 299792458.0               # m/s, exact
E_CHARGE = 1.602176634e-19    # C, exact
LN10 = math.log(10.0)

# ---------------- Cu X-ray lines (angstrom), NIST direct experimental values ----------------
CU_KA1 = 1.5405929            # K-L3
CU_KA2 = 1.5444274            # K-L2
CU_KB = 1.392234              # K-M2,3
CU_KA_MEAN = (2 * CU_KA1 + CU_KA2) / 3   # intensity-weighted K-alpha, 1.54187


def f_over_rt(T=298.15):
    """F/RT in 1/V (38.92 at 25 C)."""
    return F / (R * T)


def bragg_two_theta(d, lam=CU_KA1):
    """2 theta (degrees) for spacing d (angstrom); NaN where no reflection is possible."""
    s = lam / (2 * np.asarray(d, float))
    with np.errstate(invalid="ignore"):
        return np.degrees(2 * np.arcsin(np.where(s <= 1, s, np.nan)))


def d_from_two_theta(tt, lam=CU_KA1):
    """d spacing (angstrom) from 2 theta (degrees)."""
    return lam / (2 * np.sin(np.radians(np.asarray(tt, float)) / 2))


def read_csv(path):
    """Read a CSV file into a list of dicts (strings), skipping lines that start with '#'."""
    with open(path, newline="", encoding="utf-8") as fh:
        rows = [line for line in fh if not line.startswith("#")]
    return list(csv.DictReader(rows))


def column(rows, name, cast=float):
    return np.array([cast(r[name]) for r in rows])


def read_xrd(path):
    """(two_theta_deg, counts) arrays from one of the XRD CSV files."""
    rows = read_csv(path)
    return column(rows, "two_theta_deg"), column(rows, "counts")


def find_xrd_peaks(tt, y, rel_prominence=0.02, window=11):
    """Peak list of a powder pattern: (two_theta, height above background, fwhm_deg) arrays.
    Smooths with a Savitzky-Golay filter, finds peaks with scipy, refines each centre with a parabola
    through the top three points. FWHM from scipy's half-prominence width."""
    from scipy.signal import find_peaks, savgol_filter
    ys = savgol_filter(y, window, 2)
    step = float(np.median(np.diff(tt)))
    idx, prop = find_peaks(ys, prominence=rel_prominence * (ys.max() - ys.min()), distance=8,
                           width=2, rel_height=0.5)
    centres = []
    for i in idx:
        i = int(min(max(i, 1), len(ys) - 2))
        a, b, c = ys[i - 1], ys[i], ys[i + 1]
        den = a - 2 * b + c
        shift = 0.5 * (a - c) / den if den != 0 else 0.0
        centres.append(tt[i] + shift * step)
    return np.array(centres), prop["prominences"], prop["widths"] * step


def linfit(x, y):
    """Least-squares line y = a + b x. Returns (a, b, sa, sb)."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    (b, a), cov = np.polyfit(x, y, 1, cov=True)
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


if __name__ == "__main__":
    print(f"F/RT at 25 C = {f_over_rt():.3f} 1/V; 2.303RT/F = {1000 * LN10 / f_over_rt():.2f} mV")
    print(f"Cu Ka1 {CU_KA1} A, Ka2 {CU_KA2} A, weighted Ka {CU_KA_MEAN:.5f} A, Kb {CU_KB} A")
