"""Lesson 12.6 module practical (reference solution): a numerical Schroedinger toolkit put to work.

Part 1  Validate the solver against two exact answers (box and harmonic oscillator).
Part 2  Selection rules from transition dipoles <m|x|n> for the box, the harmonic oscillator and
        the HCl Morse oscillator (lesson 12.4).
Part 3  Variational helium: scan the effective charge zeta in E(zeta) = zeta^2 - 2 Z zeta + 5/8 zeta.
Part 4  The cyanine dye series as particles in a box: fit the box length to measured maxima
        (cyanine_dyes.csv) and predict the next dye.

Run:   py lesson06_practical_solution.py
Figures are saved to runs/lesson06_practical.png next to this file.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

from qm_solver import (solve, read_csv, H, C_LIGHT, M_E, HARTREE_EV, HB2M_U_CM_A2)

HERE = Path(__file__).resolve().parent
HE_EXACT = -2.903724        # hartree, nonrelativistic He ground state (Sims and Hagstrom)
HE_IE_EXP = 24.587387       # eV, NIST
WE, WEXE, MU_HCL = 2990.9463, 52.8186, 0.979593


def validate():
    """Return the worst relative error of the solver for the box and the oscillator (c = 1/2)."""
    N = 2000
    x = np.linspace(1, N, N) / (N + 1)                 # box of length 1, walls at 0 and 1
    E, _ = solve(x, np.zeros(N), 0.5, 5)
    exact_box = 0.5 * (np.pi * np.arange(1, 6)) ** 2
    xo = np.linspace(-10, 10, 4001)
    Eo, _ = solve(xo, 0.5 * xo**2, 0.5, 5)
    exact_ho = np.arange(5) + 0.5
    return np.max(np.abs(E / exact_box - 1)), np.max(np.abs(Eo / exact_ho - 1))


def dipole_matrix(x, psi):
    """|<m|x|n>| for all pairs of the columns of psi (real wavefunctions on a uniform grid)."""
    dx = x[1] - x[0]
    return np.abs(psi.T @ (x[:, None] * psi) * dx)


def helium_energy(zeta, Z=2):
    """Variational energy (hartree) of two 1s electrons with effective charge zeta."""
    return zeta**2 - 2 * Z * zeta + 5 / 8 * zeta


def dye_lambda(carbons, beta_nm, delta_nm):
    """Particle-in-a-box lambda_max (nm) of (CH3)2N-(CH=CH)k-CH=N+(CH3)2 with `carbons` chain carbons.
    pi electrons N = carbons + 3; bonds between the two N atoms b = carbons + 1;
    L = b beta + 2 delta; HOMO n = N/2 -> LUMO n + 1: lambda = 8 m c L^2 / (h (N + 1))."""
    N = carbons + 3
    L = ((carbons + 1) * beta_nm + 2 * delta_nm) * 1e-9
    return 8 * M_E * C_LIGHT * L**2 / (H * (N + 1)) * 1e9


def main():
    eb, eo = validate()
    print(f"Part 1  worst relative error: box {eb:.1e}, oscillator {eo:.1e} (both should be < 1e-4)")

    print("\nPart 2  transition dipoles |<m|x|n>|, normalised to the largest in each table")
    xb = np.linspace(1, 1000, 1000) / 1001
    _, psib = solve(xb, np.zeros(1000), 0.5, 5)
    xo = np.linspace(-10, 10, 4001)
    _, psio = solve(xo, 0.5 * xo**2, 0.5, 5)
    xm = np.linspace(-0.6, 3.0, 4001)
    De = WE**2 / (4 * WEXE)
    c = HB2M_U_CM_A2 / MU_HCL
    a = np.sqrt(WE**2 / (2 * c) / (2 * De))
    _, psim = solve(xm, De * (1 - np.exp(-a * xm)) ** 2, c, 5)
    tables = {}
    for name, (x, psi) in {"box (n = 1..5)": (xb, psib), "harmonic (v = 0..4)": (xo, psio),
                           "HCl Morse (v = 0..4)": (xm, psim)}.items():
        M = dipole_matrix(x - x.mean() if "box" in name else x, psi)
        M = M / M.max()
        np.fill_diagonal(M, 0.0)        # diagonal = average position, not a transition
        tables[name] = M
        print(f"\n  {name}: row = lower state, columns = upper state")
        for i in range(5):
            print("   " + " ".join(f"{M[i, j]:7.4f}" for j in range(5)))
    Mm = tables["HCl Morse (v = 0..4)"]
    print(f"\n  HCl: overtone/fundamental dipole ratio |<0|x|2>|/|<0|x|1>| = {Mm[0, 2]/Mm[0, 1]:.4f}"
          f" (intensity ratio about {(Mm[0, 2]/Mm[0, 1])**2:.1e}, ignoring the dipole function)")

    print("\nPart 3  variational helium")
    z = np.linspace(1.0, 2.5, 15001)
    E = helium_energy(z)
    zbest = z[np.argmin(E)]
    Ebest = E.min()
    print(f"  best zeta = {zbest:.4f} (exact 27/16 = {27/16:.4f}), E = {Ebest:.4f} hartree = {Ebest*HARTREE_EV:.2f} eV")
    print(f"  exact E = {HE_EXACT} hartree = {HE_EXACT*HARTREE_EV:.2f} eV; error {(Ebest-HE_EXACT)*HARTREE_EV:.2f} eV"
          f" ({(Ebest-HE_EXACT)/abs(HE_EXACT)*100:.1f} %), above the exact value as the variational principle demands")
    ie = (-2.0 - Ebest) * HARTREE_EV
    print(f"  predicted first ionisation energy {ie:.2f} eV vs measured {HE_IE_EXP:.2f} eV")
    print(f"  no screening (zeta = 2): E = {helium_energy(2.0):.4f} hartree")

    print("\nPart 4  cyanine dyes as particles in a box")
    rows = read_csv(HERE / "cyanine_dyes.csv")
    carb = np.array([float(r["chain_carbons"]) for r in rows])
    lam = np.array([float(r["lambda_max_nm"]) for r in rows])
    print("  no end correction, beta = 0.139 nm, delta = 0:  " +
          ", ".join(f"{dye_lambda(cc, 0.139, 0.0):.0f}" for cc in carb) + " nm  (measured " +
          ", ".join(f"{v:.0f}" for v in lam) + ")")
    (beta, delta), cov = curve_fit(dye_lambda, carb, lam, p0=(0.14, 0.1))
    print(f"  fitted beta = {beta:.4f} nm, delta = {delta:.4f} nm")
    print("  fit: " + ", ".join(f"{dye_lambda(cc, beta, delta):.0f}" for cc in carb) + " nm")
    print(f"  prediction for the 9-carbon dye: {dye_lambda(9, beta, delta):.0f} nm")

    out = HERE / "runs"
    out.mkdir(exist_ok=True)
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.8))
    for ax, name in zip(axes[:2], ["box (n = 1..5)", "harmonic (v = 0..4)"]):
        ax.imshow(tables[name], cmap="Blues", vmin=0, vmax=1)
        ax.set_title(name + "\n|<m|x|n>| (relative)")
        ax.set_xticks(range(5))
        ax.set_yticks(range(5))
    axes[2].plot(z, E * HARTREE_EV, label="variational E(zeta)")
    axes[2].axhline(HE_EXACT * HARTREE_EV, color="k", ls="--", label="exact")
    axes[2].set_xlabel("effective charge zeta")
    axes[2].set_ylabel("energy (eV)")
    axes[2].set_title("Helium ground state")
    axes[2].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out / "lesson06_practical.png", dpi=120)
    print(f"\nFigure saved to {out / 'lesson06_practical.png'}")


if __name__ == "__main__":
    main()
