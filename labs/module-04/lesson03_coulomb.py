"""Lesson 04.3 hands-on: Coulomb energies of ions, in vacuum, in water and in a crystal.

Fill in the three TODO functions, then run:   py lesson03_coulomb.py
Reference solution: lesson03_coulomb_solution.py
The plot is saved to runs/lesson03_coulomb.png next to this file.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent

# CODATA 2022 via NIST: e and N_A exact; epsilon_0 measured.
E = 1.602176634e-19        # C
EPS0 = 8.8541878188e-12    # F/m
NA = 6.02214076e23         # 1/mol
KB = 1.380649e-23          # J/K
R_NACL = 2.360795e-10      # m, gas-phase NaCl bond length (NIST Chemistry WebBook)
EPS_WATER = 78.4           # relative permittivity of water at 25 C (Malmberg and Maryott 1956 give 78.3)


def coulomb_energy(q1, q2, r, eps_r=1.0):
    """Potential energy (J) of charges q1, q2 (in units of e) a distance r (m) apart in a medium.
    TODO: U = q1 q2 e^2 / (4 pi eps0 eps_r r). Use the constants E and EPS0 above."""
    return None


def madelung_chain(n):
    """Madelung constant of an infinite line of alternating +/- ions, summed out to n neighbours
    on each side: M = 2 * sum_{j=1..n} (-1)^(j+1) / j. Exact limit 2 ln 2.
    TODO: j = np.arange(1, n + 1), then the alternating sum."""
    return None


def madelung_rocksalt(n):
    """Madelung constant of rock salt (NaCl) by Evjen's method: sum over a cube of
    (2n+1)^3 ions around a central ion, with ions on a face counted 1/2, on an edge 1/4 and on a
    corner 1/8, so that the cube is neutral. Converges to 1.7476 for modest n."""
    r = np.arange(-n, n + 1)
    i, j, k = np.meshgrid(r, r, r, indexing="ij")
    d = np.sqrt(i ** 2 + j ** 2 + k ** 2)
    sign = (-1.0) ** (i + j + k + 1)       # neighbours at odd distance have opposite charge
    # TODO: build the weights w: start from np.ones_like(d) and, for each of i, j, k, multiply
    # by 0.5 where abs(index) == n. Then sum sign * w / d over all points with d > 0.
    return None


def main():
    kT = KB * 298.15
    u_vac = coulomb_energy(+1, -1, R_NACL)
    if u_vac is None:
        print("TODO: write coulomb_energy() first.")
        return
    u_wat = coulomb_energy(+1, -1, R_NACL, EPS_WATER)
    print(f"Na+ Cl- at {R_NACL * 1e9:.4f} nm, vacuum: {u_vac:.3e} J = {u_vac / E:.2f} eV = {u_vac * NA / 1e3:.0f} kJ/mol")
    print(f"same pair in water:          {u_wat * NA / 1e3:.1f} kJ/mol = {u_wat / kT:.1f} kT")
    if madelung_chain(10) is None or madelung_rocksalt(2) is None:
        print("TODO: write madelung_chain() and madelung_rocksalt() next.")
        return
    for n in (10, 100, 10000):
        print(f"1D chain, n = {n:>5}: M = {madelung_chain(n):.5f}   (2 ln 2 = {2 * np.log(2):.5f})")
    for n in (2, 4, 8, 16):
        print(f"rock salt, Evjen n = {n:>2}: M = {madelung_rocksalt(n):.5f}")
    m = madelung_rocksalt(16)
    r0 = 2.82e-10   # nearest-neighbour distance in solid NaCl, m (half the 0.564 nm cell edge)
    print(f"crystal Coulomb energy per ion pair, M e^2/(4 pi eps0 r0) = {m * coulomb_energy(1, -1, r0) * NA / 1e3:.0f} kJ/mol")

    (HERE / "runs").mkdir(exist_ok=True)
    r = np.linspace(0.2e-9, 1.5e-9, 300)
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.plot(r * 1e9, coulomb_energy(1, -1, r) * NA / 1e3, label="vacuum")
    ax.plot(r * 1e9, coulomb_energy(1, -1, r, EPS_WATER) * NA / 1e3, label="water")
    ax.axhline(-kT * NA / 1e3, color="grey", ls=":", label="-RT at 298 K")
    ax.set_ylim(-700, 10)
    ax.set_xlabel("r (nm)")
    ax.set_ylabel("U (kJ/mol)")
    ax.set_title("Na+ Cl- Coulomb energy")
    ax.legend()
    fig.tight_layout()
    fig.savefig(HERE / "runs" / "lesson03_coulomb.png", dpi=120)
    print("plot saved to runs/lesson03_coulomb.png")


if __name__ == "__main__":
    main()
