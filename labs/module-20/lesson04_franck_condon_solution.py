"""Lesson 20.4 - Franck-Condon factors and the visible absorption band of I2 (reference solution).

Both electronic states are modelled as Morse potentials built from the NIST WebBook constants
(omega_e, omega_e x_e, r_e, T_e). The vibrational wavefunctions come from the finite-difference
solver in spec20.py; the Franck-Condon factor is the squared overlap |<v'|v''>|^2.

Run:  py lesson04_franck_condon_solution.py
Writes runs/lesson04_i2_fc.png.
"""
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from spec20 import DIATOMIC, G, HC_K, morse, morse_from_constants, reduced_mass, solve_1d

T = 298.15
N_UPPER = 70          # B-state levels to compute
N_LOWER = 3           # X-state levels v'' = 0, 1, 2


def fc_factors(psi_upper, psi_lower, dx):
    """Matrix of Franck-Condon factors F[v', v''] = (sum psi_upper[:, v'] psi_lower[:, v''] dx)^2."""
    overlap = psi_upper.T @ psi_lower * dx
    return overlap**2


def birge_sponer(we, wexe, ve_max=None):
    """Birge-Sponer estimate of D0 for a Morse-like state: the area under Delta G(v + 1/2) = we - 2 wexe (v + 1),
    summed from v = 0 until Delta G reaches zero. Returns (D0 in cm^-1, v of the last bound level)."""
    v_last = int(we / (2 * wexe) - 1)
    return sum(we - 2 * wexe * (v + 1) for v in range(v_last + 1)), v_last


def main():
    mu = reduced_mass("127I", "127I")
    x = np.linspace(2.2, 6.0, 6000)
    dx = x[1] - x[0]
    VX = morse(x, *morse_from_constants("I2_X"))
    VB = morse(x, *morse_from_constants("I2_B"))
    EX, psiX = solve_1d(x, VX, mu, N_LOWER)
    EB, psiB = solve_1d(x, VB, mu, N_UPPER)
    print(f"Check solver: X G(1)-G(0) = {EX[1] - EX[0]:.2f} (NIST {G('I2_X', 1) - G('I2_X', 0):.2f}), "
          f"B G(1)-G(0) = {EB[1] - EB[0]:.2f} (NIST {G('I2_B', 1) - G('I2_B', 0):.2f}) cm-1")
    F = fc_factors(psiB, psiX, dx)
    print(f"Sum of FC factors from v''=0 over v'=0..{N_UPPER - 1}: {F[:, 0].sum():.3f}")
    best = int(np.argmax(F[:, 0]))
    print(f"Strongest band from v''=0: v' = {best}, at {EB[best] - EX[0]:.0f} cm-1 "
          f"({1e7 / (EB[best] - EX[0]):.0f} nm), FC factor {F[best, 0]:.4f}")
    print(f"Origin band 0-0 at {EB[0] - EX[0]:.1f} cm-1 (NIST nu00 = 15724.57), FC factor {F[0, 0]:.1e}")

    pop = np.exp(-(EX - EX[0]) * HC_K / T)
    pop /= pop.sum()
    print("Populations of v'' = 0, 1, 2 at 298 K:", ", ".join(f"{p:.3f}" for p in pop))
    nu = (EB[:, None] - EX[None, :]).ravel()
    inten = (F * pop[None, :]).ravel()
    grid = np.linspace(15000, 21500, 3000)
    env = sum(i * np.exp(-((grid - n) / 60.0) ** 2) for n, i in zip(nu, inten))
    print(f"Envelope maximum (bound-bound bands only): {grid[np.argmax(env)]:.0f} cm-1 = "
          f"{1e7 / grid[np.argmax(env)]:.0f} nm")

    for state in ("I2_X", "I2_B"):
        d = DIATOMIC[state]
        D0, vl = birge_sponer(d["we"], d["wexe"])
        print(f"Birge-Sponer {state}: D0 = {D0:.0f} cm-1 (last level v = {vl})")
    print("Measured: X D0 = 12440 cm-1; B D0 = 20043 - 15725 = 4318 cm-1")

    Path("runs").mkdir(exist_ok=True)
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    ax[0].plot(x, VX, "k"); ax[0].plot(x, VB, "k")
    for v in range(0, N_UPPER, 5):
        ax[0].plot(x, EB[v] + 400 * psiB[:, v] ** 2 / psiB[:, v].max() ** 2 * 0.3, lw=0.6)
    ax[0].plot(x, EX[0] + 1500 * psiX[:, 0] ** 2 / psiX[:, 0].max() ** 2, "b")
    ax[0].axvline(DIATOMIC["I2_X"]["re"], ls=":", color="gray")
    ax[0].set_ylim(-500, 22000); ax[0].set_xlim(2.3, 4.5)
    ax[0].set_xlabel("r / A"); ax[0].set_ylabel("energy / cm$^{-1}$")
    ax[1].vlines(nu, 0, inten, lw=0.8); ax[1].plot(grid, env / env.max() * inten.max(), "r")
    ax[1].set_xlabel("wavenumber / cm$^{-1}$"); ax[1].set_ylabel("relative intensity")
    fig.tight_layout(); fig.savefig("runs/lesson04_i2_fc.png", dpi=120)
    print("saved runs/lesson04_i2_fc.png")


if __name__ == "__main__":
    main()
