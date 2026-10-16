"""Lesson 03.1 hands-on: balance a reaction from a null space, and analyse a two-dye mixture.

Reference solution. Run:   py lesson01_linear_solution.py
The figure is saved to runs/lesson01_linear.png next to this file.
"""
from fractions import Fraction
from math import lcm
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import null_space

HERE = Path(__file__).resolve().parent

# KMnO4 + HCl -> KCl + MnCl2 + Cl2 + H2O. Columns are species, rows are elements.
# Products get a minus sign, so "atoms in = atoms out" becomes M @ nu = 0.
SPECIES = ["KMnO4", "HCl", "KCl", "MnCl2", "Cl2", "H2O"]
ELEMENTS = ["K", "Mn", "O", "H", "Cl"]
COMPOSITION = {  # element counts per formula unit
    "KMnO4": {"K": 1, "Mn": 1, "O": 4},
    "HCl": {"H": 1, "Cl": 1},
    "KCl": {"K": 1, "Cl": 1},
    "MnCl2": {"Mn": 1, "Cl": 2},
    "Cl2": {"Cl": 2},
    "H2O": {"H": 2, "O": 1},
}
N_REACTANTS = 2


def composition_matrix(species, elements, composition, n_reactants):
    """Return the element-by-species matrix, with product columns multiplied by -1."""
    M = np.array([[composition[s].get(e, 0) for s in species] for e in elements], dtype=float)
    M[:, n_reactants:] *= -1
    return M


def balance(M):
    """Return the smallest positive integer coefficients nu with M @ nu = 0.
    The null space of M is one vector here (the reaction is unique up to scale)."""
    ns = null_space(M)
    if ns.shape[1] != 1:
        raise ValueError(f"null space has dimension {ns.shape[1]}: not a single reaction")
    v = ns[:, 0] / np.min(np.abs(ns[:, 0]))      # smallest entry becomes 1
    v *= np.sign(v[0])                            # make the coefficients positive
    fr = [Fraction(x).limit_denominator(100) for x in v]
    scale = lcm(*(f.denominator for f in fr))
    return [int(f * scale) for f in fr]


def solve_two(eps_1, eps_2, A_1, A_2, path_cm=1.0):
    """Beer-Lambert at two wavelengths: [[eX1, eY1], [eX2, eY2]] b [cX, cY] = [A1, A2]."""
    E = path_cm * np.array([eps_1, eps_2])
    return np.linalg.solve(E, np.array([A_1, A_2]))


def solve_lstsq(eps_X, eps_Y, A, path_cm=1.0):
    """All wavelengths at once: least-squares solution of E c = A, E has one row per wavelength."""
    E = path_cm * np.column_stack([eps_X, eps_Y])
    c, *_ = np.linalg.lstsq(E, A, rcond=None)
    return c


def main():
    M = composition_matrix(SPECIES, ELEMENTS, COMPOSITION, N_REACTANTS)
    nu = balance(M)
    if nu is None:
        print("TODO: write balance() first.")
        return
    lhs = " + ".join(f"{n} {s}" for n, s in zip(nu[:N_REACTANTS], SPECIES[:N_REACTANTS]))
    rhs = " + ".join(f"{n} {s}" for n, s in zip(nu[N_REACTANTS:], SPECIES[N_REACTANTS:]))
    print(f"1. balanced: {lhs} -> {rhs}")
    print(f"   check M @ nu = {M @ np.array(nu)} (all zeros means every element balances)")

    lam, eX, eY, A = np.loadtxt(HERE / "mixture_absorbance.csv", delimiter=",", skiprows=1, unpack=True)
    i1, i2 = np.argmax(eX), np.argmax(eY)          # each dye's own peak
    c2 = solve_two([eX[i1], eY[i1]], [eX[i2], eY[i2]], A[i1], A[i2])
    if c2 is None:
        print("TODO: write solve_two() next.")
        return
    cond_good = np.linalg.cond(np.array([[eX[i1], eY[i1]], [eX[i2], eY[i2]]]))
    print(f"2. two wavelengths ({lam[i1]:.0f}, {lam[i2]:.0f} nm): c_X = {c2[0]:.3e}, c_Y = {c2[1]:.3e} mol/L"
          f"  (condition number {cond_good:.1f})")
    j1, j2 = list(lam).index(425), list(lam).index(450)   # a poor choice: both on the dye X band
    c_bad = solve_two([eX[j1], eY[j1]], [eX[j2], eY[j2]], A[j1], A[j2])
    cond_bad = np.linalg.cond(np.array([[eX[j1], eY[j1]], [eX[j2], eY[j2]]]))
    print(f"   poor choice (425, 450 nm): c_X = {c_bad[0]:.3e}, c_Y = {c_bad[1]:.3e} mol/L"
          f"  (condition number {cond_bad:.1f})")

    c_ls = solve_lstsq(eX, eY, A)
    if c_ls is None:
        print("TODO: write solve_lstsq() last.")
        return
    resid = A - (eX * c_ls[0] + eY * c_ls[1])
    print(f"3. all {lam.size} wavelengths: c_X = {c_ls[0]:.3e}, c_Y = {c_ls[1]:.3e} mol/L, "
          f"rms residual {np.sqrt(np.mean(resid ** 2)):.4f}")
    print("   model values used to make the data: c_X = 2.700e-05, c_Y = 3.500e-05 mol/L")

    (HERE / "runs").mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(6.5, 3.6))
    ax.plot(lam, A, "o", label="mixture (data)")
    ax.plot(lam, eX * c_ls[0], "--", label="dye X part")
    ax.plot(lam, eY * c_ls[1], "--", label="dye Y part")
    ax.plot(lam, eX * c_ls[0] + eY * c_ls[1], "-", label="least-squares sum")
    ax.set_xlabel("wavelength (nm)")
    ax.set_ylabel("absorbance")
    ax.legend()
    fig.tight_layout()
    out = HERE / "runs" / "lesson01_linear.png"
    fig.savefig(out, dpi=120)
    print(f"plot saved to runs/{out.name}")


if __name__ == "__main__":
    main()
