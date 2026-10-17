"""Lesson 12.2 hands-on (reference solution): a finite-difference Schroedinger solver.

1. Write the solver: the Hamiltonian -c d2/dx2 + V on a grid is a tridiagonal matrix.
2. Check it against the exact particle-in-a-box energies E_n = n^2 h^2 / (8 m L^2).
3. Measure how the error shrinks with the grid spacing.
4. Make the walls finite and see the levels drop and the wavefunction leak out.

Units: x in nm, energies in eV, an electron (c = hbar^2/2m_e = 0.0381 eV nm^2).
Run:   py lesson02_box_solution.py
The figure is saved to runs/lesson02_box.png next to this file.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from qm_solver import H, M_E, E_CHARGE, HB2M_E_EV_NM2

HERE = Path(__file__).resolve().parent
C = HB2M_E_EV_NM2      # eV nm^2
L = 1.0                # nm, box length


def my_solve(x, V, c, n_states):
    """Lowest n_states energies and normalised wavefunctions of -c psi'' + V psi = E psi on the
    uniform grid x, with psi = 0 just outside the grid."""
    dx = x[1] - x[0]
    t = c / dx**2
    Hm = np.diag(2 * t + V) + np.diag(-t * np.ones(len(x) - 1), 1) + np.diag(-t * np.ones(len(x) - 1), -1)
    E, psi = np.linalg.eigh(Hm)
    return E[:n_states], psi[:, :n_states] / np.sqrt(dx)


def exact_box(n, L_nm):
    """E_n = n^2 h^2 / (8 m_e L^2), in eV."""
    return n**2 * H**2 / (8 * M_E * (L_nm * 1e-9) ** 2) / E_CHARGE


def box_grid(N, L_nm):
    """N interior points; psi = 0 at x = 0 and x = L (the walls are not grid points)."""
    dx = L_nm / (N + 1)
    return np.arange(1, N + 1) * dx


def main():
    print(f"hbar^2/2m_e = {C:.5f} eV nm^2")
    x = box_grid(200, L)
    E, psi = my_solve(x, np.zeros_like(x), C, 5)
    print("\n1. Electron in a 1.00 nm box, 200 grid points")
    print(" n   E_numeric/eV   E_exact/eV   rel. error")
    for n in range(1, 6):
        ex = exact_box(n, L)
        print(f"{n:2d}   {E[n-1]:11.5f}   {ex:10.5f}   {(E[n-1]-ex)/ex:+.2e}")

    print("\n2. Grid convergence for n = 1")
    print("   N    dx/nm     rel. error")
    for N in (25, 50, 100, 200, 400):
        xg = box_grid(N, L)
        En, _ = my_solve(xg, np.zeros_like(xg), C, 1)
        print(f"{N:5d}  {xg[1]-xg[0]:.5f}  {(En[0]-exact_box(1, L))/exact_box(1, L):+.2e}")
    print("   Halving dx cuts the error about four times: the method is second order.")

    print("\n3. Finite well: 1.00 nm wide, walls 1.00 eV high, grid from -1 to 2 nm")
    xf = np.linspace(-1.0, 2.0, 1501)
    Vf = np.where((xf > 0) & (xf < L), 0.0, 1.0)
    Ef, psif = my_solve(xf, Vf, C, 4)
    bound = Ef[Ef < 1.0]
    print(f"   bound states below 1 eV: {len(bound)}")
    for n, e in enumerate(bound, 1):
        print(f"   n = {n}: {e:.4f} eV (infinite box {exact_box(n, L):.4f} eV)")
    dx = xf[1] - xf[0]
    outside = np.sum(psif[(xf < 0) | (xf > L), 0] ** 2) * dx
    print(f"   probability of finding the n = 1 electron in the forbidden walls: {outside:.3f}")

    out = HERE / "runs"
    out.mkdir(exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(9, 4))
    xs = np.concatenate([[0], x, [L]])
    for n in range(4):
        ps = np.concatenate([[0], psi[:, n], [0]])
        axes[0].plot(xs, E[n] + 0.08 * ps, label=f"n = {n+1}")
        axes[0].axhline(E[n], color="0.8", lw=0.5)
    axes[0].set_title("Infinite box, L = 1 nm")
    axes[0].set_xlabel("x (nm)")
    axes[0].set_ylabel("energy (eV); psi offset")
    axes[1].plot(xf, Vf, "k-", lw=1)
    for n in range(len(bound)):
        axes[1].plot(xf, Ef[n] + 0.08 * psif[:, n])
    axes[1].set_ylim(-0.1, 1.3)
    axes[1].set_title("Finite well, walls 1 eV")
    axes[1].set_xlabel("x (nm)")
    fig.tight_layout()
    fig.savefig(out / "lesson02_box.png", dpi=120)
    print(f"\nFigure saved to {out / 'lesson02_box.png'}")


if __name__ == "__main__":
    main()
