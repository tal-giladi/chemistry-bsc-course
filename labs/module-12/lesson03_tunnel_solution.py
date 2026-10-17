"""Lesson 12.3 hands-on (reference solution): tunnelling.

1. Transmission through a rectangular barrier (exact formula) for an electron: width dependence,
   the scanning tunnelling microscope rule of thumb.
2. The same barrier for a proton and a deuteron: why H tunnels and D much less.
3. A symmetric double well solved numerically (qm_solver): the tunnelling splitting of an
   ammonia-like umbrella inversion, for NH3 and ND3.

Run:   py lesson03_tunnel_solution.py
The figure is saved to runs/lesson03_tunnel.png next to this file.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from qm_solver import solve, HB2M_E_EV_NM2, HB2M_U_CM_A2

HERE = Path(__file__).resolve().parent
MP_ME, MD_ME = 1836.152673426, 3670.48296   # proton and deuteron masses in electron masses (CODATA 2022)
C_TO_GHZ = 29.9792458                       # 1 cm^-1 = 29.979 GHz


def kappa(E, V0, mass_me):
    """Decay constant inside the barrier, nm^-1: sqrt(2 m (V0 - E)) / hbar."""
    return np.sqrt((V0 - E) * mass_me / HB2M_E_EV_NM2)


def transmission(E, V0, d_nm, mass_me):
    """Exact transmission probability through a rectangular barrier, for E < V0 (eV, nm)."""
    k = kappa(E, V0, mass_me)
    return 1.0 / (1.0 + V0**2 * np.sinh(k * d_nm) ** 2 / (4 * E * (V0 - E)))


def double_well_splitting(mu_u, Vb=2020.0, a=0.40):
    """Symmetric quartic double well V = Vb ((x/a)^2 - 1)^2 (x in angstrom, V in cm^-1) for an
    effective mass mu_u (u). Returns the lowest four levels in cm^-1, the grid and the states."""
    x = np.linspace(-1.5, 1.5, 3001)
    V = Vb * ((x / a) ** 2 - 1) ** 2
    E, psi = solve(x, V, HB2M_U_CM_A2 / mu_u, 4)
    return E, x, V, psi


def main():
    print("1. Electron, 4.0 eV below the top of a barrier (a typical STM gap)")
    k = kappa(0.0, 4.0, 1.0)
    print(f"   kappa = {k:.2f} nm^-1, decay length 1/kappa = {1/k*1000:.0f} pm")
    print(f"   e^(-2 kappa * 0.1 nm) = {np.exp(-2*k*0.1):.3f}: each extra 0.1 nm cuts the current"
          f" about {1/np.exp(-2*k*0.1):.0f} times")
    print("\n   Electron, E = 1.0 eV, barrier V0 = 2.0 eV")
    for d in (0.1, 0.3, 0.5, 1.0):
        print(f"   width {d:.1f} nm: T = {transmission(1.0, 2.0, d, 1.0):.2e}")

    print("\n2. Proton vs deuteron, 0.20 eV below the top of a 0.050 nm wide barrier (V0 = 0.40 eV)")
    tH = transmission(0.20, 0.40, 0.050, MP_ME)
    tD = transmission(0.20, 0.40, 0.050, MD_ME)
    print(f"   T(H) = {tH:.2e}, T(D) = {tD:.2e}, ratio H/D = {tH/tD:.0f}")
    print(f"   an electron with the same numbers: T = {transmission(0.20, 0.40, 0.050, 1.0):.3f}")

    print("\n3. Ammonia-like double well (barrier 2020 cm^-1, minima at +/-0.40 angstrom)")
    rows = []
    for name, mu in (("NH3", 2.487), ("ND3", 4.22)):
        E, x, V, psi = double_well_splitting(mu)
        split = E[1] - E[0]
        rows.append((name, split, psi, E))
        print(f"   {name}: mu = {mu:.3f} u, E0 = {E[0]:.1f} cm^-1, splitting = {split:.3f} cm^-1"
              f" = {split*C_TO_GHZ:.2f} GHz; next pair {E[2]-E[0]:.0f} cm^-1 up, split {E[3]-E[2]:.1f} cm^-1")
    print(f"   ratio NH3/ND3 = {rows[0][1]/rows[1][1]:.0f}")
    print("   Measured: NH3 23.79 GHz (0.79 cm^-1), ND3 1.59 GHz (0.053 cm^-1), ratio 15")

    out = HERE / "runs"
    out.mkdir(exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(9, 4))
    dd = np.linspace(0.05, 1.0, 100)
    axes[0].semilogy(dd, transmission(1.0, 2.0, dd, 1.0))
    axes[0].set_xlabel("barrier width (nm)")
    axes[0].set_ylabel("transmission T")
    axes[0].set_title("Electron, E = 1 eV, V0 = 2 eV")
    _, x, V, _ = double_well_splitting(2.487)
    axes[1].plot(x, V, "k-", lw=1)
    E = rows[0][3]
    psi = rows[0][2]
    for n, lab in ((0, "symmetric"), (1, "antisymmetric")):
        axes[1].plot(x, E[n] + 300 * psi[:, n] * (1 if n == 0 else 1), label=lab)
    axes[1].set_ylim(0, 2600)
    axes[1].set_xlim(-1.0, 1.0)
    axes[1].set_xlabel("umbrella coordinate (angstrom)")
    axes[1].set_ylabel("energy (cm$^{-1}$)")
    axes[1].set_title("NH3-like double well")
    axes[1].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out / "lesson03_tunnel.png", dpi=120)
    print(f"\nFigure saved to {out / 'lesson03_tunnel.png'}")


if __name__ == "__main__":
    main()
