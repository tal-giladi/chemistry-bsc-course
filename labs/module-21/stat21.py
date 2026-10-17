"""Shared helper for the Module 21 labs (statistical thermodynamics).

You do not need to edit this file. It holds:
- CODATA 2022 constants (via NIST, https://physics.nist.gov/cuu/Constants/), checked 2026-10-17;
- NIST standard atomic weights for the molar masses (natural isotope mixtures, as the NIST tables use);
- NIST Chemistry WebBook constants of diatomic molecules (Huber and Herzberg, with NIST updates);
- NIST Atomic Spectra Database levels of the I and Cl atoms;
- partition functions (level sums and closed forms) and thermodynamic functions built from them;
- a reader for janaf_check.csv (NIST-JANAF values used only to check your results).

Energies of internal levels are in cm^-1. Vibrational energies are measured from v = 0, so the
zero of energy of every molecule is its lowest level; D0 (not De) is then the dissociation energy.
Standard pressure p° = 1 bar.
"""
import csv
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent

# ---------------- CODATA 2022 ----------------
H = 6.62607015e-34          # J s (exact)
C_CM = 29979245800.0        # cm/s (exact)
K_B = 1.380649e-23          # J/K (exact)
N_A = 6.02214076e23         # 1/mol (exact)
R = K_B * N_A               # 8.314462618 J/(mol K) (exact)
U = 1.66053906892e-27       # kg, atomic mass constant
HC_K = H * C_CM / K_B       # second radiation constant c2, 1.438777 cm K
CM1_TO_KJMOL = H * C_CM * N_A / 1000   # 1 cm^-1 = 0.01196266 kJ/mol
P_STD = 1.0e5               # Pa (1 bar)

# ---------------- molar masses, g/mol (NIST standard atomic weights) ----------------
MOLAR_MASS = {"N2": 28.0134, "CO": 28.0101, "HCl": 36.4609, "O2": 31.9988,
              "I2": 253.80894, "I": 126.90447, "Cl": 35.453, "Ar": 39.948}

# ---------------- NIST WebBook constants of diatomic molecules, X state (cm^-1) ----------------
# N2  https://webbook.nist.gov/cgi/cbook.cgi?ID=C7727379&Mask=1000
# CO  https://webbook.nist.gov/cgi/cbook.cgi?ID=C630080&Mask=1000
# HCl https://webbook.nist.gov/cgi/cbook.cgi?ID=C7647010&Mask=1000 (H35Cl constants)
# O2  https://webbook.nist.gov/cgi/cbook.cgi?ID=C7782447&Mask=1000 (X 3Sigma_g-, g_el = 3)
# I2  https://webbook.nist.gov/cgi/cbook.cgi?ID=C7553562&Mask=1000 (127I2)
# sigma = rotational symmetry number; g_el = degeneracy of the ground electronic state.
DIATOMIC = {
    "N2": dict(we=2358.57, wexe=14.324, Be=1.998241, ae=0.017318, sigma=2, g_el=1),
    "CO": dict(we=2169.81358, wexe=13.28831, Be=1.93128087, ae=0.01750441, sigma=1, g_el=1),
    "HCl": dict(we=2990.9463, wexe=52.8186, Be=10.593416, ae=0.307181, sigma=1, g_el=1),
    "O2": dict(we=1580.193, wexe=11.981, Be=1.4376766, ae=0.01593, sigma=2, g_el=3),
    "I2": dict(we=214.502, wexe=0.6147, Be=0.037372, ae=0.0001138, sigma=2, g_el=1),
}

# I2 dissociation energy from the NIST-JANAF 0 K formation enthalpies (tables I-001 and I-027):
# D0 = 2 x 107.164 - 65.504 = 148.824 kJ/mol = 12 440.7 cm^-1.
D0_I2_KJMOL = 2 * 107.164 - 65.504
D0_I2_CM = D0_I2_KJMOL / CM1_TO_KJMOL

# ---------------- NIST ASD atomic levels: (energy cm^-1, degeneracy 2J+1) ----------------
# I I : 5p5 2P3/2 at 0, 2P1/2 at 7602.9762;  Cl I : 3p5 2P3/2 at 0, 2P1/2 at 882.3515;  Ar I: 1S0 only
# (its first excited level is above 93 000 cm^-1).
ATOM_LEVELS = {"I": [(0.0, 4), (7602.9762, 2)], "Cl": [(0.0, 4), (882.3515, 2)], "Ar": [(0.0, 1)]}


# ---------------- partition functions ----------------
def thermal_wavelength(molar_mass, T):
    """Thermal de Broglie wavelength h / sqrt(2 pi m k T), in m."""
    m = molar_mass / 1000 / N_A
    return H / math.sqrt(2 * math.pi * m * K_B * T)


def q_trans_std(molar_mass, T):
    """Standard translational partition function per molecule, q°/N_A = (kT/p°) / Lambda^3."""
    return K_B * T / P_STD / thermal_wavelength(molar_mass, T) ** 3


def q_rot_sum(B, T, sigma, jmax=None):
    """Rotational partition function by direct sum over J, divided by the symmetry number."""
    if jmax is None:
        jmax = int(10 * math.sqrt(T / (HC_K * B))) + 20
    return sum((2 * J + 1) * math.exp(-HC_K * B * J * (J + 1) / T) for J in range(jmax + 1)) / sigma


def q_rot_high_t(B, T, sigma):
    """High-temperature rotational partition function kT/(sigma h c B)."""
    return T / (sigma * HC_K * B)


def q_vib_harmonic(w0, T):
    """Harmonic vibrational partition function with energies from v = 0; w0 = G(1) - G(0)."""
    return 1.0 / (1.0 - math.exp(-HC_K * w0 / T))


def q_vib_anharmonic(we, wexe, T, d0):
    """Sum over anharmonic levels G(v) - G(0) up to the dissociation energy d0 (all cm^-1)."""
    g0 = 0.5 * we - 0.25 * wexe
    total, v = 0.0, 0
    while True:
        e = we * (v + 0.5) - wexe * (v + 0.5) ** 2 - g0
        if e > d0 or (v > 0 and e < prev):     # stop at D0 or where the expansion turns over
            break
        total += math.exp(-HC_K * e / T)
        prev, v = e, v + 1
    return total


def q_elec(levels, T):
    """Electronic partition function from (energy cm^-1, degeneracy) pairs."""
    return sum(g * math.exp(-HC_K * e / T) for e, g in levels)


def w0(name):
    """Fundamental wavenumber G(1) - G(0) = we - 2 wexe, cm^-1."""
    d = DIATOMIC[name]
    return d["we"] - 2 * d["wexe"]


def B0(name):
    """Rotational constant of v = 0, B0 = Be - ae/2, cm^-1."""
    d = DIATOMIC[name]
    return d["Be"] - d["ae"] / 2


def ln_q_diatomic(name, T, vib="harmonic", d0=None):
    """ln of the standard molecular partition function q°/N_A of a diatomic (rigid rotor, B0)."""
    d = DIATOMIC[name]
    qt = q_trans_std(MOLAR_MASS[name], T)
    qr = q_rot_sum(B0(name), T, d["sigma"])
    if vib == "harmonic":
        qv = q_vib_harmonic(w0(name), T)
    else:
        qv = q_vib_anharmonic(d["we"], d["wexe"], T, d0)
    return math.log(qt * qr * qv * d["g_el"])


def ln_q_atom(name, T):
    """ln of q°/N_A of an atom: translation times electronic levels."""
    return math.log(q_trans_std(MOLAR_MASS[name], T) * q_elec(ATOM_LEVELS[name], T))


# ---------------- thermodynamic functions from ln q (ideal gas, per mole, at p°) ----------------
def thermo_from_lnq(ln_q, T, dT=0.01):
    """Return dict with H - H0 (kJ/mol), S (J/(mol K)) and Cp (J/(mol K)) at p°.

    ln_q(T) must be ln(q°/N_A) including the kT/p° factor, so that
    H - H0 = R T^2 d ln q°/dT,  S = R (ln q°/N_A + T d ln q°/dT),  Cp = dH/dT.
    The '+1' of Stirling's N! is already inside the kT/p° factor's T-derivative.
    """
    f0, fp, fm = ln_q(T), ln_q(T + dT), ln_q(T - dT)
    d1 = (fp - fm) / (2 * dT)
    d2 = (fp - 2 * f0 + fm) / dT**2
    h = R * T**2 * d1
    cp = R * (2 * T * d1 + T**2 * d2)
    s = R * (f0 + T * d1)
    return {"H_minus_H0": h / 1000, "S": s, "Cp": cp}


def read_janaf(path=HERE / "janaf_check.csv"):
    """Rows of janaf_check.csv as dicts with float values (except 'species')."""
    with open(path, encoding="utf-8") as f:
        rows = [line for line in f if not line.startswith("#")]
    out = []
    for row in csv.DictReader(rows):
        out.append({k: (v if k == "species" else float(v)) for k, v in row.items()})
    return out
