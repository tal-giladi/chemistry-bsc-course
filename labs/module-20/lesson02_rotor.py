"""Lesson 20.2 - fit the NIST microwave lines of CO.

Fill in the functions marked TODO, then run:  py lesson02_rotor.py
Reference solution: lesson02_rotor_solution.py
Writes runs/lesson02_co_lines.png.
"""
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from spec20 import B_v, C_CM, DIATOMIC, HC_K, MASS, bond_length_from_B, read_csv, reduced_mass

MHZ_TO_CM = 1e6 / C_CM          # 1 MHz in cm^-1


def load_lines(isotopologue):
    """Upper J and line wavenumbers (cm^-1) for one isotopologue from co_rotational_lines.csv."""
    rows = [r for r in read_csv("co_rotational_lines.csv") if r["isotopologue"] == isotopologue]
    J = np.array([int(r["J_upper"]) for r in rows])
    nu = np.array([float(r["freq_MHz"]) for r in rows]) * MHZ_TO_CM
    return J, nu


def fit_B_D(J_upper, nu):
    """Fit nu = 2B J_upper - 4D J_upper^3 (J_upper = J + 1). Returns B, D in cm^-1.
    Divide by J_upper: nu/J_upper = 2B - 4D J_upper^2, a straight line in J_upper^2."""
    # TODO: fit a straight line to y = nu / J_upper against x = J_upper**2 (np.polyfit(x, y, 1))
    # TODO: intercept = 2B and slope = -4D: return B, D
    return None


def j_max(B, T):
    """Most populated rotational level, J_max = sqrt(kT / 2hcB) - 1/2 (as a real number)."""
    # TODO: return sqrt(T / (HC_K * 2 * B)) - 0.5   (HC_K = hc/k in cm K)
    return None


def main():
    if fit_B_D(np.array([1, 2]), np.array([2.0, 4.0])) is None or j_max(1.0, 1.0) is None:
        print("TODO: write fit_B_D() and j_max() first.")
        return
    J12, nu12 = load_lines("12C16O")
    B12, D12 = fit_B_D(J12, nu12)
    mu12 = reduced_mass("C", "O")
    print(f"12C16O: {len(J12)} lines, J_upper {J12.min()}-{J12.max()}")
    print(f"  B0 = {B12:.6f} cm-1 = {B12 / MHZ_TO_CM:.2f} MHz,  D = {D12:.3e} cm-1")
    print(f"  NIST WebBook: B0 = Be - ae/2 = {B_v('CO', 0):.6f} cm-1, De = {DIATOMIC['CO']['De']:.3e} cm-1")
    print(f"  r0 = {bond_length_from_B(B12, mu12):.5f} A  (re = {DIATOMIC['CO']['re']} A)")
    resid_rigid = nu12 - 2 * B12 * J12
    print(f"  rigid-rotor misfit at J_upper = {J12.max()}: {resid_rigid[-1]:.3f} cm-1")

    J13, nu13 = load_lines("13C16O")
    B13, D13 = fit_B_D(J13, nu13)
    mu13 = reduced_mass("13C", "O")
    print(f"13C16O: B0 = {B13:.6f} cm-1;  predicted from 12C16O x mu12/mu13 = {B12 * mu12 / mu13:.6f} cm-1")
    print(f"  first line 13CO J=1<-0: {2 * B13 - 4 * D13:.4f} cm-1 vs 12CO {2 * B12 - 4 * D12:.4f} cm-1")

    for T in (10.0, 298.15):
        print(f"J_max at {T:6.1f} K: {j_max(B12, T):.2f}")

    Path("runs").mkdir(exist_ok=True)
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    ax[0].plot(J12, nu12, "o", label="NIST SRD 114")
    ax[0].plot(J12, 2 * B12 * J12, "-", label="rigid rotor 2B(J+1)")
    ax[0].set_xlabel("J + 1"); ax[0].set_ylabel("line position / cm$^{-1}$"); ax[0].legend()
    ax[1].plot(J12**2, nu12 / J12, "o")
    ax[1].plot(J12**2, 2 * B12 - 4 * D12 * J12**2, "-")
    ax[1].set_xlabel("(J + 1)$^2$"); ax[1].set_ylabel(r"$\tilde\nu/(J+1)$ / cm$^{-1}$")
    fig.tight_layout(); fig.savefig("runs/lesson02_co_lines.png", dpi=120)
    print("saved runs/lesson02_co_lines.png")


if __name__ == "__main__":
    main()
