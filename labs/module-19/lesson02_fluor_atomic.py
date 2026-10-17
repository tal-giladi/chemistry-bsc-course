"""Lesson 19.2: fluorescence quenching (Stern-Volmer), the inner-filter limit, and Boltzmann
populations in flames and plasmas.

Fill in the two TODOs, then run (from this folder):
    py lesson02_fluor_atomic.py
Reference solution: lesson02_fluor_atomic_solution.py
Data: quinine_chloride.csv (simulated; columns chloride_mM,fluorescence).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from ana19 import HERE, read_csv, line_fit, save

# CODATA 2022 exact constants (NIST)
H_PLANCK, C_LIGHT, K_B = 6.62607015e-34, 299792458.0, 1.380649e-23
NACL_G_PER_MOL = 58.44

LINES = [  # element, wavelength (nm), g(upper)/g(lower) for the resonance line
    ("Na", 589.0, 3.0),
    ("Ca", 422.7, 3.0),
    ("Zn", 213.9, 3.0),
]


def stern_volmer_K(q_mol_per_L, F, F0):
    """Stern-Volmer constant from F0/F = 1 + K [Q]: the slope of F0/F against [Q] (L/mol)."""
    # TODO 1: fit a straight line to F0/F (y) against [Q] (x) with line_fit and return (slope, intercept).
    return None, None


def excited_fraction(wavelength_nm, g_ratio, T):
    """Boltzmann ratio N*/N0 for a resonance line at temperature T (K)."""
    # TODO 2: photon energy dE = h c / lambda (lambda in metres), then N*/N0 = g_ratio * exp(-dE / (k_B T)).
    return None


def main():
    d = read_csv(HERE / "quinine_chloride.csv")
    q = d["chloride_mM"] / 1000
    F = d["fluorescence"]
    F0 = F[q == 0][0]
    K, b = stern_volmer_K(q, F, F0)
    print(f"Stern-Volmer: F0/F = {b:.3f} + {K:.0f} [Cl-]   (K_SV = {K:.0f} L/mol)")
    for ppm in (100, 1000):
        cl = ppm / 1000 / NACL_G_PER_MOL
        print(f"   {ppm} ppm NaCl = {1000 * cl:5.2f} mM chloride: signal falls to {100 / (1 + K * cl):.0f} % of F0")

    print("Inner filter: fluorescence follows 1 - 10^-A, not 2.303 A")
    for A in (0.005, 0.01, 0.02, 0.05, 0.1):
        print(f"   A = {A:5.3f}: signal {100 * ((1 - 10 ** -A) / (2.303 * A) - 1):+.1f} % from the straight line")

    print("Fraction of atoms in the upper state, N*/N0:")
    for el, lam, g in LINES:
        cells = "  ".join(f"{T} K: {excited_fraction(lam, g, T):.1e}" for T in (2500, 3000, 7000))
        print(f"   {el} {lam} nm   {cells}")

    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    ax[0].plot(1000 * q, F0 / F, "o")
    qq = np.linspace(0, q.max(), 50)
    ax[0].plot(1000 * qq, b + K * qq, "-")
    ax[0].set(xlabel="[Cl-] (mM)", ylabel="F0 / F", title="Stern-Volmer plot, quinine")
    TT = np.linspace(2000, 8000, 200)
    for el, lam, g in LINES:
        ax[1].semilogy(TT, excited_fraction(lam, g, TT), label=f"{el} {lam} nm")
    ax[1].set(xlabel="T (K)", ylabel="N*/N0", title="Boltzmann population of the upper level")
    ax[1].legend()
    save(fig, "lesson02_fluor_atomic.png")


if __name__ == "__main__":
    main()
