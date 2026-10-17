"""Shared helper for the Module 13 labs: NIST Shomate heat capacities and reaction functions.

Data: nist_shomate.csv. Shomate coefficients A-H from the NIST Chemistry WebBook (gas- and
condensed-phase thermochemistry pages, Chase 1998 = NIST-JANAF tables); dHf298 and S298 are the
CODATA Key Values (Cox, Wagman and Medvedev 1984) as listed on the same WebBook pages.
Checked 2026-10-17. Standard pressure 1 bar.

Shomate form (t = T/1000):
    Cp  = A + B t + C t^2 + D t^3 + E / t^2                       J/(mol K)
    H - H298 = A t + B t^2/2 + C t^3/3 + D t^4/4 - E/t + F - H     kJ/mol
    S   = A ln t + B t + C t^2/2 + D t^3/3 - E/(2 t^2) + G        J/(mol K)
"""
import csv
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
R = 8.314462618      # J/(mol K), CODATA 2022 (exact)
T0 = 298.15          # K
TOL = 2.0            # K of slack at the edges of a fitted range


def load_shomate(path=HERE / "nist_shomate.csv"):
    """Return {species: [row, ...]} with one row per fitted temperature range."""
    data = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            rec = {k: float(v) for k, v in row.items() if k != "species"}
            data.setdefault(row["species"], []).append(rec)
    return data


DATA = load_shomate()


def _coeffs(species, T):
    for rec in DATA[species]:
        if rec["Tmin_K"] - TOL <= T <= rec["Tmax_K"] + TOL:
            return rec
    lo = min(r["Tmin_K"] for r in DATA[species])
    hi = max(r["Tmax_K"] for r in DATA[species])
    raise ValueError(f"{species}: T = {T} K is outside the NIST fit ({lo:.0f}-{hi:.0f} K)")


def cp(species, T):
    """Heat capacity at constant pressure, J/(mol K)."""
    c = _coeffs(species, T)
    t = T / 1000
    return c["A"] + c["B"] * t + c["C"] * t**2 + c["D"] * t**3 + c["E"] / t**2


def h_minus_h298(species, T):
    """H(T) - H(298.15 K), kJ/mol."""
    c = _coeffs(species, T)
    t = T / 1000
    return (c["A"] * t + c["B"] * t**2 / 2 + c["C"] * t**3 / 3 + c["D"] * t**4 / 4
            - c["E"] / t + c["F"] - c["H"])


def s_abs(species, T):
    """Absolute standard entropy S(T) at 1 bar, J/(mol K)."""
    c = _coeffs(species, T)
    t = T / 1000
    return (c["A"] * math.log(t) + c["B"] * t + c["C"] * t**2 / 2 + c["D"] * t**3 / 3
            - c["E"] / (2 * t**2) + c["G"])


def dhf298(species):
    return DATA[species][0]["dHf298_kJ_mol"]


def s298(species):
    return DATA[species][0]["S298_J_molK"]


def reaction_h(reaction, T):
    """Standard reaction enthalpy at T (kJ/mol). reaction = {species: stoichiometric number}."""
    return sum(nu * (dhf298(sp) + h_minus_h298(sp, T)) for sp, nu in reaction.items())


def reaction_s(reaction, T):
    """Standard reaction entropy at T (J/(mol K))."""
    return sum(nu * s_abs(sp, T) for sp, nu in reaction.items())


def reaction_g(reaction, T):
    """Standard reaction Gibbs energy at T (kJ/mol)."""
    return reaction_h(reaction, T) - T * reaction_s(reaction, T) / 1000


def reaction_k(reaction, T):
    """Dimensionless standard equilibrium constant K at T (standard pressure 1 bar)."""
    return math.exp(-reaction_g(reaction, T) * 1000 / (R * T))
