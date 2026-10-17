"""Shared constants and helpers for the Module 30 labs (Physical Chemistry Lab 2). Keep this file next to
the lesson scripts.

Constants: CODATA 2022 values from NIST (https://physics.nist.gov/cuu/Constants/), checked 2026-10-17.
Atomic masses: NIST Atomic Weights and Isotopic Compositions.
HCl constants: NIST Chemistry WebBook, constants of diatomic molecules, H35Cl X 1Sigma+
(https://webbook.nist.gov/cgi/cbook.cgi?ID=C7647010&Mask=1000), checked 2026-10-17.
"""
import csv
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent

# ---------------- CODATA 2022 ----------------
H = 6.62607015e-34            # J s, exact
C = 299792458.0               # m/s, exact
C_CM = C * 100                # cm/s
K_B = 1.380649e-23            # J/K, exact
N_A = 6.02214076e23           # 1/mol, exact
R = 8.314462618               # J/(mol K), exact (N_A k_B)
M_E = 9.1093837139e-31        # kg, electron mass
U = 1.66053906892e-27         # kg, atomic mass constant
MU_B = 9.2740100657e-24       # J/T, Bohr magneton
MU_N = 5.0507837393e-27       # J/T, nuclear magneton
G_E = 2.00231930436092        # free-electron g factor (magnitude)
G_P = 5.5856946893            # proton g factor
G_D = 0.8574382335            # deuteron g factor
HC_K = H * C_CM / K_B         # second radiation constant, cm K (1.438777)

# ---------------- NIST atomic masses (u) ----------------
MASS = {"H": 1.00782503223, "D": 2.01410177812, "35Cl": 34.968852682, "37Cl": 36.965902602}
ABUNDANCE_35CL = 0.7576       # IUPAC representative isotopic composition of chlorine

# ---------------- NIST WebBook constants of H35Cl, X 1Sigma+ (cm^-1) ----------------
HCL35 = dict(we=2990.9463, wexe=52.8186, weye=0.22437, Be=10.593416, ae=0.307181, De=5.3194e-4,
             re=1.274552)
D0_HCL_CM = 35748.0           # D0 of HCl, about 427.6 kJ/mol = 4.43 eV (thermochemical value, rounded)


def reduced_mass(a, b):
    """Reduced mass in u of two atoms given by their MASS keys."""
    return MASS[a] * MASS[b] / (MASS[a] + MASS[b])


def isotope_constants(const, rho):
    """Mass-scaled Dunham constants for an isotopologue with rho = sqrt(mu_ref / mu_new)."""
    return dict(we=const["we"] * rho, wexe=const["wexe"] * rho**2, weye=const["weye"] * rho**3,
                Be=const["Be"] * rho**2, ae=const["ae"] * rho**3, De=const["De"] * rho**4,
                re=const["re"])


def term(const, v, J):
    """Rovibrational term value G(v) + F_v(J) in cm^-1 (measured from the potential minimum)."""
    x = v + 0.5
    G = const["we"] * x - const["wexe"] * x**2 + const["weye"] * x**3
    Bv = const["Be"] - const["ae"] * x
    jj = J * (J + 1)
    return G + Bv * jj - const["De"] * jj**2


def bond_length_from_B(B_cm, mu_u):
    """Bond length in angstrom from a rotational constant (cm^-1) and a reduced mass (u)."""
    inertia = H / (8 * math.pi**2 * C_CM * B_cm)
    return math.sqrt(inertia / (mu_u * U)) * 1e10


# ---------------- small helpers ----------------
def read_csv(path):
    """Read a CSV file into a list of dicts (strings), skipping lines that start with '#'."""
    with open(path, newline="", encoding="utf-8") as fh:
        rows = [line for line in fh if not line.startswith("#")]
    return list(csv.DictReader(rows))


def column(rows, name, cast=float):
    return np.array([cast(r[name]) for r in rows])


def linfit(x, y):
    """Least-squares line y = a + b x. Returns (a, b, sa, sb, cov_ab, s_residual)."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    (b, a), cov = np.polyfit(x, y, 1, cov=True)
    resid = y - (a + b * x)
    s = float(np.sqrt(np.sum(resid**2) / max(1, len(x) - 2)))
    return float(a), float(b), float(np.sqrt(cov[1, 1])), float(np.sqrt(cov[0, 0])), float(cov[0, 1]), s


def propagate(f, values):
    """Value of f and its standard uncertainty for independent inputs {name: (value, sigma)},
    by numerical partial derivatives (lesson 09.3)."""
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


if __name__ == "__main__":
    rho = math.sqrt(reduced_mass("H", "35Cl") / reduced_mass("H", "37Cl"))
    nu0 = term(HCL35, 1, 0) - term(HCL35, 0, 0)
    print(f"H35Cl band centre {nu0:.3f} cm^-1, R(0) {term(HCL35, 1, 1) - term(HCL35, 0, 0):.3f}, "
          f"P(1) {term(HCL35, 1, 0) - term(HCL35, 0, 1):.3f}; rho(37/35) = {rho:.6f}")
