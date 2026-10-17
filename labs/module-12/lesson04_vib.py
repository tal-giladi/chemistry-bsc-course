"""Lesson 12.4 hands-on: vibrational levels of HCl, harmonic and Morse.

Constants for H35Cl from the NIST Chemistry WebBook (Huber and Herzberg), accessed 2026-10-17:
omega_e = 2990.9463, omega_e x_e = 52.8186, omega_e y_e = 0.22437 cm^-1, r_e = 1.274552 angstrom.

1. Harmonic levels (v + 1/2) omega_e and the zero-point energy.
2. A Morse potential built from omega_e and omega_e x_e, solved numerically with qm_solver.
3. Fundamental and first overtone vs the values the NIST constants predict.
4. Bond lengthening with v, and the isotope shift for D35Cl.

Units: displacement in angstrom, energy in cm^-1, masses in u.
Fill in the functions marked TODO, then run:   py lesson04_vib.py
Reference solution: lesson04_vib_solution.py
The figure is saved to runs/lesson04_vib.png next to this file.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from qm_solver import solve, count_nodes, HB2M_U_CM_A2

HERE = Path(__file__).resolve().parent
WE, WEXE, WEYE, RE = 2990.9463, 52.8186, 0.22437, 1.274552   # H35Cl, NIST WebBook
M_H, M_D, M_CL35 = 1.00782503223, 2.01410177812, 34.968852682  # u, NIST atomic masses


def reduced_mass(m1, m2):
    # TODO: return m1 m2 / (m1 + m2)
    return None


def morse_params(we, wexe, mu):
    """Well depth De (cm^-1) and range a (1/angstrom) of V = De (1 - exp(-a x))^2 with the given
    harmonic wavenumber and anharmonicity. Uses De = we^2 / (4 wexe) and k = 2 De a^2, where the
    force constant (V = k x^2 / 2 near the bottom) is k = we^2 / (2 c) with c = hbar^2 / (2 mu),
    because hbar omega = sqrt(2 c k) in these units."""
    # TODO: De = we^2 / (4 wexe);  c = HB2M_U_CM_A2 / mu;  k = we^2 / (2 c);  a = sqrt(k / (2 De))
    # TODO: return De, a, k
    return None


def nist_term(v):
    """Vibrational term G(v) from the NIST constants, including omega_e y_e."""
    h = v + 0.5
    return WE * h - WEXE * h**2 + WEYE * h**3


def main():
    mu = reduced_mass(M_H, M_CL35)
    if mu is None or morse_params(WE, WEXE, mu) is None:
        print("TODO: write reduced_mass() and morse_params() first.")
        return
    De, a, k = morse_params(WE, WEXE, mu)
    k_si = k * 1.98644586e-23 * 1e20       # cm^-1/angstrom^2 -> J/m^2 = N/m (hc = 1.98645e-23 J cm)
    print(f"H35Cl: mu = {mu:.6f} u, Morse De = {De:.0f} cm^-1 ({De/8065.544:.2f} eV), a = {a:.4f} 1/angstrom")
    print(f"       force constant k = {k_si:.0f} N/m")

    x = np.linspace(-0.6, 3.0, 4001)
    V_harm = 0.5 * k * x**2             # the same curvature as the Morse well at its bottom
    V_morse = De * (1 - np.exp(-a * x)) ** 2
    c = HB2M_U_CM_A2 / mu
    Eh, psih = solve(x, V_harm, c, 6)
    Em, psim = solve(x, V_morse, c, 6)

    print("\n v   harmonic   Morse(num)  Morse(formula)   NIST G(v)   nodes")
    for v in range(6):
        form = WE * (v + 0.5) - WEXE * (v + 0.5) ** 2
        print(f"{v:2d}  {Eh[v]:9.1f}  {Em[v]:10.1f}  {form:13.1f}  {nist_term(v):11.1f}   {count_nodes(psim[:, v])}")
    print(f"\nZero-point energy (Morse): {Em[0]:.1f} cm^-1 = {Em[0]*0.0119627:.2f} kJ/mol")
    print(f"Fundamental 0->1: harmonic {Eh[1]-Eh[0]:.1f}, Morse {Em[1]-Em[0]:.1f}, NIST {nist_term(1)-nist_term(0):.1f} cm^-1")
    print(f"Overtone    0->2: harmonic {Eh[2]-Eh[0]:.1f}, Morse {Em[2]-Em[0]:.1f}, NIST {nist_term(2)-nist_term(0):.1f} cm^-1")

    dx = x[1] - x[0]
    print("\nAverage bond length <r> = r_e + <x>:")
    for v in range(4):
        xm = np.sum(x * psim[:, v] ** 2) * dx
        print(f"   v = {v}: {RE + xm:.4f} angstrom")

    mu_d = reduced_mass(M_D, M_CL35)
    we_d = WE * np.sqrt(mu / mu_d)
    wexe_d = WEXE * mu / mu_d          # omega_e x_e scales as 1/mu
    De_d, a_d, _ = morse_params(we_d, wexe_d, mu_d)
    Ed, _ = solve(x, De_d * (1 - np.exp(-a_d * x)) ** 2, HB2M_U_CM_A2 / mu_d, 3)
    print(f"\nD35Cl: mu = {mu_d:.4f} u, omega_e = {we_d:.1f} cm^-1 (same force constant, same De = {De_d:.0f})")
    print(f"       predicted fundamental {Ed[1]-Ed[0]:.1f} cm^-1, ratio to HCl {(Ed[1]-Ed[0])/(Em[1]-Em[0]):.3f}")

    out = HERE / "runs"
    out.mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    r = RE + x
    ax.plot(r, V_morse, "k-", lw=1, label="Morse")
    ax.plot(r, V_harm, "k--", lw=0.8, label="harmonic")
    for v in range(6):
        ax.plot(r, Em[v] + 1500 * psim[:, v] * 0.25)
        ax.axhline(Em[v], color="0.85", lw=0.5)
    ax.set_ylim(0, 20000)
    ax.set_xlim(0.8, 2.6)
    ax.set_xlabel("H-Cl distance (angstrom)")
    ax.set_ylabel("energy (cm$^{-1}$)")
    ax.set_title("H$^{35}$Cl vibrational levels (Morse, numerical)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out / "lesson04_vib.png", dpi=120)
    print(f"\nFigure saved to {out / 'lesson04_vib.png'}")


if __name__ == "__main__":
    main()
