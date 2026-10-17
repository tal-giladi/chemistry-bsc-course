"""Lesson 12.5 hands-on (reference solution): the rigid rotor and the hydrogen atom.

1. HCl as a rigid rotor: bond length from B, pure-rotation line positions, which J is most
   populated at room temperature. Constants for H35Cl from the NIST Chemistry WebBook
   (B_e = 10.593416, alpha_e = 0.307181, D_e = 5.3194e-4 cm^-1), accessed 2026-10-17.
2. The hydrogen atom: solve the radial equation numerically (qm_solver) in atomic units,
       -1/2 u'' + [ l(l+1) / (2 r^2) - 1/r ] u = E u,     psi = u(r)/r * Y_lm,
   and compare with E_n = -1/(2 n^2) hartree. Count the radial nodes.

Run:   py lesson05_rotor_h_solution.py
The figure is saved to runs/lesson05_rotor_h.png next to this file.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from qm_solver import solve, count_nodes, H, C_LIGHT, M_U, HARTREE_EV, A0_NM

HERE = Path(__file__).resolve().parent
BE, ALPHA_E, DE_CD = 10.593416, 0.307181, 5.3194e-4     # cm^-1, H35Cl
MU_HCL = 0.979593                                        # u (lesson 12.4)
KT_CM_298 = 207.22                                       # k_B T / (h c) at 298.15 K, cm^-1
MP_ME = 1836.152673426


def bond_length(B_cm, mu_u):
    """r = sqrt(h / (8 pi^2 c mu B)) in angstrom (c in cm/s so B stays in cm^-1)."""
    I = H / (8 * np.pi**2 * C_LIGHT * 100 * B_cm)     # kg m^2
    return np.sqrt(I / (mu_u * M_U)) * 1e10


def rotation_lines(B, D, J_max=10):
    """Wavenumbers of J -> J+1 absorption lines: 2B(J+1) - 4D(J+1)^3."""
    J = np.arange(J_max + 1)
    return J, 2 * B * (J + 1) - 4 * D * (J + 1) ** 3


def populations(B, kT, J_max=20):
    """Relative populations (2J+1) exp(-B J(J+1) / kT), normalised to sum 1."""
    J = np.arange(J_max + 1)
    p = (2 * J + 1) * np.exp(-B * J * (J + 1) / kT)
    return J, p / p.sum()


def hydrogen_radial(l, n_states=3, r_max=80.0, N=8000):
    """Lowest radial states for angular momentum l (atomic units). Grid starts at dr, u(0) = 0."""
    r = np.linspace(r_max / N, r_max, N)
    V = l * (l + 1) / (2 * r**2) - 1.0 / r
    E, u = solve(r, V, 0.5, n_states)
    return r, E, u


def main():
    B0 = BE - ALPHA_E / 2
    print("1. H35Cl rigid rotor")
    print(f"   r_e from B_e = {BE} cm^-1: {bond_length(BE, MU_HCL):.4f} angstrom (NIST r_e 1.274552)")
    print(f"   r_0 from B_0 = {B0:.4f} cm^-1: {bond_length(B0, MU_HCL):.4f} angstrom")
    J, lines = rotation_lines(B0, DE_CD)
    print("   J -> J+1 lines (cm^-1): " + ", ".join(f"{w:.2f}" for w in lines[:6]))
    print(f"   spacing between the first two lines: {lines[1]-lines[0]:.2f} cm^-1 (about 2B)")
    Jp, p = populations(B0, KT_CM_298)
    jmax = Jp[np.argmax(p)]
    print(f"   most populated level at 298 K: J = {jmax} "
          f"(formula sqrt(kT/2B) - 1/2 = {np.sqrt(KT_CM_298/(2*B0)) - 0.5:.2f})")

    print("\n2. Hydrogen atom, radial equation (atomic units, infinite nuclear mass)")
    print("   n  l   E_num/hartree   -1/(2n^2)   radial nodes   E/eV")
    states = {}
    for l in range(3):
        r, E, u = hydrogen_radial(l)
        for k in range(3):
            n = k + l + 1
            states[(n, l)] = u[:, k]
            print(f"   {n}  {l}   {E[k]:12.6f}   {-0.5/n**2:9.6f}   {count_nodes(u[:, k]):6d}"
                  f"        {E[k]*HARTREE_EV:8.4f}")
    dr = r[1] - r[0]
    u1s = states[(1, 0)]
    print(f"   <r> for 1s = {np.sum(r * u1s**2) * dr:.4f} bohr (exact 1.5) = {1.5*A0_NM*1000:.1f} pm")
    print(f"   radial maximum of 1s at r = {r[np.argmax(u1s**2)]:.3f} bohr (exact 1, the Bohr radius)")
    mu_corr = 1 / (1 + 1 / MP_ME)
    print(f"   with the reduced-mass correction, H ionisation energy = {0.5*HARTREE_EV*mu_corr:.4f} eV")

    out = HERE / "runs"
    out.mkdir(exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].bar(Jp, p, color="tab:blue")
    axes[0].set_xlabel("J")
    axes[0].set_ylabel("fraction of molecules")
    axes[0].set_title("H$^{35}$Cl rotational populations, 298 K")
    for key in [(1, 0), (2, 0), (2, 1), (3, 0), (3, 1), (3, 2)]:
        axes[1].plot(r, states[key] ** 2, label=f"n={key[0]}, l={key[1]}")
    axes[1].set_xlim(0, 25)
    axes[1].set_xlabel("r (bohr)")
    axes[1].set_ylabel("radial probability $P(r) = u^2$")
    axes[1].set_title("Hydrogen radial distributions")
    axes[1].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out / "lesson05_rotor_h.png", dpi=120)
    print(f"\nFigure saved to {out / 'lesson05_rotor_h.png'}")


if __name__ == "__main__":
    main()
