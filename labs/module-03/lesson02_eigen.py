"""Lesson 03.2 hands-on: eigenvalue problems in chemistry.

Part 1: Hueckel pi energies of chains and rings (energies in units of beta, E = alpha + x beta).
Part 2: stretching normal modes of linear CO2 from a mass-weighted force-constant matrix.

Fill in the functions marked TODO, then run:   py lesson02_eigen.py
Reference solution: lesson02_eigen_solution.py
The figure is saved to runs/lesson02_eigen.png next to this file.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
M_U = 1.66053906892e-27      # kg, atomic mass constant (CODATA 2022)
C_CM = 2.99792458e10         # cm/s, speed of light (exact)
M_O, M_C = 15.99491462, 12.0  # u, 16O and 12C
CO2_OBS = {"symmetric stretch": 1333.0, "antisymmetric stretch": 2349.0}  # cm^-1, NIST CCCBDB


def huckel_matrix(n, ring=False):
    """Return the n x n Hueckel matrix in units of beta: 0 on the diagonal (alpha measured from
    alpha), 1 between bonded neighbours i and i+1, and also between atoms 0 and n-1 for a ring."""
    # TODO: H = np.zeros((n, n)); set H[i, i+1] = H[i+1, i] = 1 for i in range(n - 1)
    # TODO: if ring, also set H[0, n-1] = H[n-1, 0] = 1. Return H.
    return None


def pi_energy(x, n_electrons):
    """Total pi energy in units of beta (the n alpha part left out).
    beta is negative, so the LARGEST x is the LOWEST energy level. Fill levels two electrons at a
    time from the largest x down; an odd last electron goes in alone."""
    # TODO: sort x from largest to smallest; add 2 * x_i per level (1 * x_i for a last odd electron)
    # TODO: until n_electrons are placed. Return the total.
    return None


def co2_wavenumbers(k):
    """Stretching modes of O=C=O along its axis, force constant k (N/m) for each C=O bond.
    Build the force-constant matrix K, mass-weight it D = M^-1/2 K M^-1/2, take the eigenvalues
    (omega^2), and convert omega to wavenumbers nu~ = omega / (2 pi c). Return them sorted."""
    # TODO: K = k * [[1, -1, 0], [-1, 2, -1], [0, -1, 1]]; m = M_U * np.array([M_O, M_C, M_O])
    # TODO: D = K / np.sqrt(np.outer(m, m)); w2, vecs = np.linalg.eigh(D); clip w2 at 0
    # TODO: return np.sqrt(w2) / (2 * np.pi * C_CM), vecs
    return None, None


def main():
    print("1. Hueckel (E = alpha + x beta; beta < 0, so larger x is lower energy)")
    cases = [("ethylene", 2, False, 2), ("butadiene", 4, False, 4),
             ("hexatriene", 6, False, 6), ("benzene", 6, True, 6)]
    levels = {}
    for name, n, ring, ne in cases:
        H = huckel_matrix(n, ring)
        if H is None:
            print("TODO: write huckel_matrix() first.")
            return
        x = np.linalg.eigvalsh(H)
        e_pi = pi_energy(x, ne)
        if e_pi is None:
            print("TODO: write pi_energy() next.")
            return
        deloc = e_pi - ne              # localized: ne/2 ethylene bonds, each worth 2 beta
        levels[name] = x
        print(f"   {name:10s} x = {np.array2string(np.sort(x)[::-1], precision=3)}"
              f"  E_pi = {ne} alpha + {e_pi:.3f} beta, delocalization {deloc:.3f} beta"
              f" (about {abs(deloc) * 75:.0f} kJ/mol more stable, beta = -75 kJ/mol)")

    print("2. CO2 stretching modes (1D model, one force constant)")
    w_sym = 2 * np.pi * C_CM * CO2_OBS["symmetric stretch"]
    k = M_U * M_O * w_sym ** 2         # symmetric stretch: only the O atoms move, omega^2 = k / m_O
    nu, vecs = co2_wavenumbers(k)
    if nu is None:
        print("TODO: write co2_wavenumbers() last.")
        return
    print(f"   k from the 1333 cm^-1 symmetric stretch: {k:.0f} N/m")
    for value, v in zip(nu, vecs.T):
        shape = np.round(v / np.max(np.abs(v)), 2)
        print(f"   eigen-wavenumber {value:7.1f} cm^-1, mass-weighted displacements O, C, O = {shape}")
    print(f"   observed: symmetric 1333, antisymmetric 2349 cm^-1 (NIST CCCBDB); "
          f"model antisymmetric is {100 * (nu[-1] / 2349 - 1):+.0f} %")

    (HERE / "runs").mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(6.0, 3.8))
    for i, (name, x) in enumerate(levels.items()):
        for xi in x:
            ax.hlines(-xi, i - 0.3, i + 0.3)
    ax.set_xticks(range(len(levels)), list(levels))
    ax.set_ylabel("orbital energy  (E - alpha) / |beta|")
    ax.set_title("Hueckel pi levels (lower is more stable)")
    fig.tight_layout()
    out = HERE / "runs" / "lesson02_eigen.png"
    fig.savefig(out, dpi=120)
    print(f"plot saved to runs/{out.name}")


if __name__ == "__main__":
    main()
