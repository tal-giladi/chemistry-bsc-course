"""Lesson 14.4 hands-on: the vibrations of CO2 as three coupled masses.

Measured fundamentals (NIST CCCBDB, accessed 2026-10-17): symmetric stretch 1333 (Raman only,
unperturbed value), bend 667 (doubly degenerate), antisymmetric stretch 2349 cm^-1.

1. One bond constant k fitted to the antisymmetric stretch: predict the symmetric stretch.
2. Bond constant k plus a bond-bond interaction k12, fitted to both stretches.
3. The bend from a bending constant, using the same eigen solver on sideways displacements.
4. Isotopes 13C16O2 and 12C18O2 predicted from the same force constants.
5. Which modes change the dipole moment (IR active) for partial charges -q, +2q, -q.

Run:   py lesson04_co2.py
The plot is saved to runs/lesson04_co2.png next to this file.
Fill in the functions marked TODO. Reference solution: lesson04_co2_solution.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import eigh

HERE = Path(__file__).resolve().parent
U = 1.66053906892e-27       # kg, atomic mass constant (CODATA 2022)
C_CM = 2.99792458e10        # cm/s
H = 6.62607015e-34          # J s
NA = 6.02214076e23
M_O16, M_O18 = 15.99491462, 17.99915961   # u, NIST atomic masses
M_C12, M_C13 = 12.0, 13.00335484
NU1, NU2, NU3 = 1333.0, 667.0, 2349.0     # cm^-1, CCCBDB fundamentals
R_CO = 1.160e-10                          # m, C=O bond length (about 1.16 angstrom)


def to_lambda(nu):
    """omega^2 in s^-2 from a wavenumber in cm^-1."""
    return (2 * np.pi * C_CM * nu) ** 2


def to_nu(w2):
    return np.sqrt(np.clip(w2, 0, None)) / (2 * np.pi * C_CM)


def stretch_K(k, k12):
    """Force constants for the axial displacements (x_O, x_C, x_O) of O=C=O.
    V = k/2 (s1^2 + s2^2) + k12 s1 s2 with bond stretches s1 = x_C - x_O1, s2 = x_O2 - x_C."""
    B = np.array([[-1.0, 1.0, 0.0], [0.0, -1.0, 1.0]])    # s = B x
    F = np.array([[k, k12], [k12, k]])
    return B.T @ F @ B


def bend_K(k_delta, r=R_CO):
    """Force constants for sideways displacements (y_O, y_C, y_O). The bend angle is
    delta = (y_O1 - 2 y_C + y_O2) / r, and V = k_delta/2 delta^2 with k_delta in N m / rad^2."""
    u = np.array([1.0, -2.0, 1.0]) / r
    return k_delta * np.outer(u, u)


def modes(K, masses_u):
    """Wavenumbers (cm^-1, ascending) and mode shapes of K v = w^2 M v."""
    w2, V = eigh(K, np.diag(np.array(masses_u) * U))
    return to_nu(w2), V


def fit_k_one(nu3, mO, mC):
    """One constant k from the antisymmetric stretch: w3^2 = k (1/mO + 2/mC)."""
    return to_lambda(nu3) / ((1 / mO + 2 / mC) / U)


def fit_k_k12(nu1, nu3, mO, mC):
    """k and k12 from both stretches: w1^2 = (k + k12)/mO,  w3^2 = (k - k12)(1/mO + 2/mC)."""
    # TODO: s = to_lambda(nu1) mO U  (= k + k12);  d = to_lambda(nu3) / ((1/mO + 2/mC) / U)  (= k - k12);
    #       return (s + d) / 2, (s - d) / 2
    return None


def fit_k_bend(nu2, mO, mC, r=R_CO):
    """Bending constant from w2^2 = (2 k_delta / r^2)(1/mO)(1 + 2 mO/mC)."""
    # TODO: return to_lambda(nu2) r^2 mO U / (2 (1 + 2 mO/mC))
    return None


def dipole_change(shape, charges=(-1.0, 2.0, -1.0)):
    """Change of the dipole moment along a mode (charges in units of q, shape in any units)."""
    # TODO: return the dot product of the charges with the mode shape (np.dot), as a float
    return None


def all_modes(k, k12, kd, mO, mC):
    nus, Vs = modes(stretch_K(k, k12), [mO, mC, mO])
    nub, Vb = modes(bend_K(kd), [mO, mC, mO])
    return nus[1], nub[2], nus[2], Vs, Vb


def main():
    mO, mC = M_O16, M_C12
    k1 = fit_k_one(NU3, mO, mC)
    print(f"Model 1, one constant from nu3: k = {k1:.0f} N/m")
    nus, Vs = modes(stretch_K(k1, 0.0), [mO, mC, mO])
    print(f"  stretches {nus[1]:.0f} and {nus[2]:.0f} cm^-1 (measured {NU1:.0f} and {NU3:.0f}); "
          f"ratio nu3/nu1 = {nus[2] / nus[1]:.3f} vs measured {NU3 / NU1:.3f}")
    print(f"  (lesson 03.2 fitted k to nu1 instead: k = {to_lambda(NU1) * mO * U:.0f} N/m, nu3 = "
          f"{to_nu(to_lambda(NU1) * (1 + 2 * mO / mC)):.0f} cm^-1)")

    k, k12 = fit_k_k12(NU1, NU3, mO, mC)
    kd = fit_k_bend(NU2, mO, mC)
    print(f"\nModel 2, valence force field: k = {k:.0f} N/m, interaction k12 = {k12:.0f} N/m "
          f"({k12 / k * 100:.1f} % of k), bend k_delta = {kd * 1e18:.3f} aJ/rad^2")
    nu1, nu2, nu3, Vs, Vb = all_modes(k, k12, kd, mO, mC)
    print(f"  reproduces nu1 = {nu1:.1f}, nu2 = {nu2:.1f} (x2), nu3 = {nu3:.1f} cm^-1")
    for name, shape in (("translation", Vs[:, 0]), ("symmetric stretch", Vs[:, 1]),
                        ("antisymmetric stretch", Vs[:, 2]), ("bend", Vb[:, 2])):
        s = shape / np.max(np.abs(shape))
        dmu = dipole_change(s)
        print(f"  {name:22s} shape (O, C, O) = {np.round(s, 3)}   dipole change {dmu:+.2f} q"
              f"  -> {'IR active' if abs(dmu) > 1e-6 and name != 'translation' else 'IR inactive'}")

    zpe = 0.5 * (nu1 + 2 * nu2 + nu3)
    print(f"  zero-point energy 1/2 (nu1 + 2 nu2 + nu3) = {zpe:.0f} cm^-1 = "
          f"{zpe * H * C_CM * NA / 1000:.1f} kJ/mol")

    print("\nIsotopes, same force constants (Born-Oppenheimer), harmonic model:")
    print("  molecule      nu1     nu2     nu3   (cm^-1)")
    rows = []
    for label, o, c in (("12C16O2", M_O16, M_C12), ("13C16O2", M_O16, M_C13), ("12C18O2", M_O18, M_C12)):
        n1, n2, n3, _, _ = all_modes(k, k12, kd, o, c)
        rows.append((label, n1, n2, n3))
        print(f"  {label}   {n1:7.1f} {n2:7.1f} {n3:7.1f}")
    print(f"  13C shift of nu3: {rows[1][3] - rows[0][3]:.1f} cm^-1. Measured 13C16O2 nu3: 2282.4 cm^-1 "
          f"in CO2 ice at 70 K (SSHADE); gas and solid values differ by only a few cm^-1.")
    print("  nu1 does not move with 13C, because the carbon atom sits still in that mode.")
    print(f"  Wavelengths: nu2 = {1e4 / NU2:.1f} um, nu3 = {1e4 / NU3:.2f} um "
          f"(Earth's thermal emission peaks near {2898 / 288:.0f} um)")

    (HERE / "runs").mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(7, 2.8))
    for label, n1, n2, n3 in rows:
        y = rows.index((label, n1, n2, n3))
        ax.vlines([n2, n3], y, y + 0.8, colors="C0", lw=2)
        ax.vlines([n1], y, y + 0.8, colors="C1", lw=2, linestyles="dashed")
        ax.text(3000, y + 0.3, label)
    ax.set_xlim(500, 3300)
    ax.set_yticks([])
    ax.set_xlabel("wavenumber (cm$^{-1}$); solid = IR active, dashed = Raman only")
    ax.invert_xaxis()
    fig.tight_layout()
    fig.savefig(HERE / "runs" / "lesson04_co2.png", dpi=120)
    print("Plot saved to runs/lesson04_co2.png")


if __name__ == "__main__":
    try:
        main()
    except TypeError as exc:
        print(f"Fill in the functions marked TODO first ({exc}).")
