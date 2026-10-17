"""Shared helpers for the Module 22 kinetics labs. You do not need to edit this file.

Constants: CODATA 2022 via NIST (exact SI values). Kinetic parameters: NIST Chemical Kinetics
Database (SRD 17, https://kinetics.nist.gov/kinetics/), records retrieved 2026-10-17, and
Michaelis & Menten (1913) as translated by Johnson & Goody, Biochemistry 50, 8264 (2011).
Run  py kin22.py  to print a short self-check.
"""
import csv
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent

# CODATA 2022 (exact in the 2019 SI)
K_B = 1.380649e-23        # J/K
H = 6.62607015e-34        # J s
N_A = 6.02214076e23       # 1/mol
R = K_B * N_A             # 8.314462618... J/(mol K)

# N2O5 -> NO2 + NO3 (IUPAC evaluation 1997, via NIST SRD 17), valid about 200-300 K
N2O5_KINF = dict(A=9.71e14, n=0.10, Ea=92291.0)     # s^-1, high-pressure limit
N2O5_K0 = dict(A=1.0e-3, n=-3.50, Ea=91459.0)       # cm^3 molecule^-1 s^-1, low-pressure limit, M = N2

# 2NO + O2 -> 2NO2 (IUPAC 2004, via NIST SRD 17), 270-600 K, third order
NO_O2 = dict(A=3.30e-39, n=0.0, Ea=-4407.0)         # cm^6 molecule^-2 s^-1

# OH + CH4 -> CH3 + H2O (JPL evaluation 97-4, via NIST SRD 17), 200-300 K
OH_CH4_JPL = dict(A=2.46e-12, n=0.0, Ea=14800.0)    # cm^3 molecule^-1 s^-1

# Michaelis & Menten (1913) dissociation constants, mM (sucrose = Km)
KS_MM, KF_MM, KG_MM = 16.7, 58.0, 89.0


def k_mod_arrhenius(p, T):
    """k = A (T/298)^n exp(-Ea/RT), the form NIST SRD 17 uses."""
    return p["A"] * (T / 298.0) ** p["n"] * math.exp(-p["Ea"] / (R * T))


def number_density(p_bar, T):
    """Molecules per cm^3 of an ideal gas at pressure p (bar) and temperature T (K)."""
    return p_bar * 1e5 / (K_B * T) / 1e6


def read_csv(name):
    """Rows of a CSV file in this folder as a list of dicts (strings)."""
    with open(HERE / name, newline="", encoding="utf-8") as f:
        return [row for row in csv.DictReader(f) if row and not str(next(iter(row.values()))).startswith("#")]


def column(rows, key, cast=float):
    return [cast(r[key]) for r in rows]


def runs_dir():
    d = HERE / "runs"
    d.mkdir(exist_ok=True)
    return d


if __name__ == "__main__":
    print(f"R = {R:.9f} J/(mol K)")
    print(f"N2O5 k_inf(298 K) = {k_mod_arrhenius(N2O5_KINF, 298.0):.3f} s^-1 (NIST lists 0.06)")
    print(f"N2O5 k0(298 K)    = {k_mod_arrhenius(N2O5_K0, 298.0):.3e} cm3/s (NIST lists 9.32e-20)")
    print(f"2NO+O2 k(298 K)   = {k_mod_arrhenius(NO_O2, 298.0):.3e} cm6/s (NIST lists 1.95e-38)")
    print(f"OH+CH4 k(298 K)   = {k_mod_arrhenius(OH_CH4_JPL, 298.0):.3e} cm3/s (NIST lists 6.26e-15)")
    print(f"[M] at 1 bar, 298 K = {number_density(1.0, 298.0):.3e} molecules/cm3")
    print(f"{len(read_csv('invertase_timecourse.csv'))} time-course rows, "
          f"{len(read_csv('invertase_initial_rates.csv'))} initial rates, {len(read_csv('oh_ch4_k.csv'))} OH+CH4 points")
