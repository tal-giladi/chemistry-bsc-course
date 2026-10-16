"""Lesson 04.1 hands-on: the HCl bond as a potential-energy curve.

Fill in the three TODO functions, then run:   py lesson01_morse.py
The plot is saved to runs/lesson01_morse.png next to this file.
Reference solution: lesson01_morse_solution.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent

# Constants: CODATA 2022 via NIST (h, c, k_B exact).
H, C, KB = 6.62607015e-34, 299792458.0, 1.380649e-23
# H-35Cl ground state: re and omega_e from the NIST Chemistry WebBook (constants of diatomic
# molecules); D0 = 35748.2 cm^-1 from Hu, Melville and Hepburn (2003). De = D0 + zero-point energy.
RE = 1.274552e-10                         # m
DE = (35748.2 + 2990.9463 / 2 - 52.8186 / 4) * 100 * H * C   # J, about 4.62 eV
K_BOND = 516.3                            # N/m, from omega_e and the reduced mass (lesson 04.2)
A = np.sqrt(K_BOND / (2 * DE))            # Morse width parameter, 1/m


def morse_energy(r):
    """U(r) = De * (1 - exp(-a (r - re)))^2, in joules. Zero at the bottom of the well.
    TODO: write it with np.exp, using the constants DE, A and RE above."""
    return None


def force(r, U):
    """F = -dU/dr, estimated with central differences (lesson 02.2).
    TODO: use np.gradient(U, r) and mind the minus sign."""
    return None


def work_to_stretch(r, F, r1, r2):
    """Work you must do to pull the atoms from r1 to r2 against the bond force:
    W = -integral of F dr from r1 to r2 (lesson 02.3). Uses the trapezoid rule on the grid.
    TODO: select the grid points with r1 <= r <= r2, then use np.trapezoid(F[m], r[m])."""
    return None


def main():
    r = np.linspace(0.09e-9, 0.60e-9, 5101)   # 0.1 pm steps
    U = morse_energy(r)
    if U is None:
        print("TODO: write morse_energy() first.")
        return
    F = force(r, U)
    if F is None:
        print("TODO: write force() next.")
        return
    kT = KB * 298.15

    near = r < 0.3e-9                       # far away F is also ~0, so search near the bottom
    i0 = np.argmin(np.abs(np.where(near, F, np.inf)))
    imax = np.argmin(F)  # most negative force = strongest pull back towards re
    W = work_to_stretch(r, F, RE, RE + 0.01e-9)
    if W is None:
        print("TODO: write work_to_stretch() last.")
        return
    harmonic = 0.5 * K_BOND * (0.01e-9) ** 2
    print(f"well depth De             = {DE:.3e} J = {DE / 1.602176634e-19:.2f} eV")
    print(f"force is zero at r        = {r[i0] * 1e9:.4f} nm (re = {RE * 1e9:.4f} nm)")
    print(f"largest restoring force   = {-F[imax] * 1e9:.2f} nN at r = {r[imax] * 1e9:.4f} nm")
    print(f"work to stretch by 0.01 nm = {W:.3e} J = {W / kT:.1f} kT at 298 K")
    print(f"harmonic estimate          = {harmonic:.3e} J ({(harmonic / W - 1) * 100:+.0f} %)")
    print(f"thermal energy kT (298 K)  = {kT:.3e} J = {kT / DE * 100:.2f} % of De")

    (HERE / "runs").mkdir(exist_ok=True)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.5))
    a1.plot(r * 1e9, U / 1.602176634e-19)
    a1.plot(r * 1e9, 0.5 * K_BOND * (r - RE) ** 2 / 1.602176634e-19, "--", label="harmonic")
    a1.set_ylim(0, 6)
    a1.set_xlabel("r (nm)")
    a1.set_ylabel("U (eV)")
    a1.set_title("HCl Morse potential")
    a1.legend()
    a2.plot(r * 1e9, F * 1e9)
    a2.axhline(0, color="grey", lw=0.5)
    a2.set_xlabel("r (nm)")
    a2.set_ylabel("F (nN)")
    a2.set_title("force = -dU/dr")
    a2.set_ylim(-10, 20)
    fig.tight_layout()
    fig.savefig(HERE / "runs" / "lesson01_morse.png", dpi=120)
    print("plot saved to runs/lesson01_morse.png")


if __name__ == "__main__":
    main()
