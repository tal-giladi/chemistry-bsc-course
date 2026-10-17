"""Shared helpers for the Module 28 structure-and-reactivity labs. You do not need to edit this file.

Constants: CODATA 2022 via NIST (exact SI values). Bond dissociation enthalpies: Blanksby and
Ellison, Acc. Chem. Res. 36, 255 (2003), as listed by P. G. Wenthold on Chemistry LibreTexts;
H-Cl and H-Br from NIST-JANAF / CODATA key-value enthalpies of formation (NIST WebBook).
All checked 2026-10-17. Run  py sr28.py  to print a short self-check.
"""
import csv
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent

# CODATA 2022 (exact in the 2019 SI)
K_B = 1.380649e-23        # J/K
H = 6.62607015e-34        # J s
N_A = 6.02214076e23       # 1/mol
R = K_B * N_A             # 8.314462618... J/(mol K)

# Bond dissociation enthalpies at 298 K, kJ/mol
BDE = {
    "CH3-H": 439.3,              # methane
    "CH3CH2-H": 423.0,           # ethane, primary
    "(CH3)2CH-H": 412.5,         # propane, secondary
    "(CH3)3C-H": 403.8,          # isobutane, tertiary
    "CH2=CHCH2-H": 371.5,        # propene, allylic
    "C6H5CH2-H": 375.3,          # toluene, benzylic
    "CH2=CH-H": 463.2,           # ethene, vinylic
    "C6H5-H": 472.4,             # benzene, aryl
    "H-Cl": 431.6,               # from dfH: H 217.998, Cl 121.301, HCl -92.31 kJ/mol
    "H-Br": 366.2,               # from dfH: H 217.998, Br 111.87, HBr -36.29 kJ/mol
}


def read_csv(name):
    """Rows of a CSV file (path relative to this folder) as a list of dicts; '#' lines are comments."""
    with open(HERE / name, newline="", encoding="utf-8") as f:
        lines = [ln for ln in f if not ln.startswith("#")]
    return list(csv.DictReader(lines))


def num(value):
    """Float from a CSV cell, or nan for an empty cell."""
    return float(value) if str(value).strip() else math.nan


def sigma_table():
    """Hansch-Leo-Taft constants as {substituent: {"m": .., "p": .., "p+": ..}}."""
    return {r["substituent"]: {"m": num(r["sigma_m"]), "p": num(r["sigma_p"]), "p+": num(r["sigma_p_plus"])}
            for r in read_csv("sigma_hansch.csv")}


def line_fit(x, y):
    """Least-squares straight line y = a + b x.
    Returns dict with slope, intercept, their standard uncertainties, r2 and residuals."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    (b, a), cov = np.polyfit(x, y, 1, cov=True)
    resid = y - (a + b * x)
    r2 = 1 - np.sum(resid ** 2) / np.sum((y - y.mean()) ** 2)
    return dict(slope=b, intercept=a, s_slope=math.sqrt(cov[0, 0]), s_intercept=math.sqrt(cov[1, 1]),
                r2=r2, resid=resid)


def eyring_k(dG_kJ, T=298.15):
    """Transition-state-theory rate constant (s^-1) for a free energy of activation in kJ/mol."""
    return K_B * T / H * math.exp(-dG_kJ * 1000 / (R * T))


def runs_dir():
    d = HERE / "runs"
    d.mkdir(exist_ok=True)
    return d


if __name__ == "__main__":
    print(f"R = {R:.6f} J/(mol K); kB T/h at 298.15 K = {K_B * 298.15 / H:.3e} s^-1")
    print(f"Eyring k for 45 kJ/mol at 298 K: {eyring_k(45):.2e} s^-1 (cyclohexane ring flip, about 1e5)")
    s = sigma_table()
    print(f"{len(s)} substituents; sigma_p(NO2) = {s['NO2']['p']}, sigma_p+(OCH3) = {s['OCH3']['p+']}")
    print(f"{len(read_csv('diazonium_coupling.csv'))} diazonium rows; BDE propane 2-H = {BDE['(CH3)2CH-H']} kJ/mol")
