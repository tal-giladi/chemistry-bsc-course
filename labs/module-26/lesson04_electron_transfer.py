"""Lesson 26.4 Part A - electron transfer in proteins: Marcus rates and the respiratory chain.

Fill in the functions marked TODO, then run:  py lesson04_electron_transfer.py
Reference solution: lesson04_electron_transfer_solution.py
Writes runs/lesson04_electron_transfer.png.
"""
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from bio26 import E_CHARGE, F, K_B, T_BODY, runs_dir

KT_EV = K_B * T_BODY / E_CHARGE          # thermal energy in eV at 37 °C (about 0.0267 eV)
# Tunnelling timetable for Ru-modified proteins (Gray and Winkler, PNAS 102, 3534, 2005)
K0, R0, BETA = 1e13, 3.0, 1.1            # s^-1 at contact, angstrom, 1/angstrom

# Standard reduction potentials at pH 7, 25 °C (E°', V), Jakubowski, Biochemistry Online, table B03
CHAIN = [("NAD+/NADH", -0.32), ("ubiquinone/ubiquinol", 0.06), ("cytochrome c Fe3+/Fe2+", 0.25),
         ("1/2 O2/H2O", 0.816)]


def marcus_rate(dG, lam, r):
    """Electron-transfer rate (s^-1): k = K0 exp(-BETA (r - R0)) exp(-(dG + lam)^2 / (4 lam kT)).
    dG and lam in eV, r (edge-to-edge distance) in angstrom."""
    # TODO: write the two factors: distance (tunnelling) and activation (Marcus parabola)
    return None


def dG_per_electron(E_donor, E_acceptor):
    """Gibbs energy (eV) for moving one electron from the donor couple to the acceptor couple."""
    # TODO: dG = -(E_acceptor - E_donor)   (one electron, so -nFE in eV is just -E in volts)
    return None


def o2_potential_at_pH(pH, E0=1.229, T=298.15):
    """E for O2 + 4H+ + 4e- -> 2H2O at a given pH (Nernst, lesson 08.6): E = E0 - (ln10 RT/F) pH."""
    # TODO: return E0 - math.log(10) * (K_B * T / E_CHARGE) * pH     (K_B T / e = RT/F, in volts)
    return None


def main():
    if marcus_rate(-0.5, 0.5, 3.0) is None or dG_per_electron(0.0, 0.1) is None or o2_potential_at_pH(0.0) is None:
        print("TODO: write marcus_rate(), dG_per_electron() and o2_potential_at_pH() first.")
        return
    print(f"E(O2/H2O) at pH 7 from 1.229 V: {o2_potential_at_pH(7.0):.3f} V (tables list 0.816 V)")

    print("\nRespiratory chain, Gibbs energy per 2 electrons:")
    total = 0.0
    for (d, Ed), (a, Ea) in zip(CHAIN, CHAIN[1:]):
        g = 2 * dG_per_electron(Ed, Ea) * F / 1000   # eV per electron -> kJ/mol for 2 mol electrons
        total += g
        print(f"  {d:24s} -> {a:24s} {g:7.1f} kJ/mol")
    print(f"  total NADH -> 1/2 O2: {total:.1f} kJ/mol; per O2 (4 electrons): {2 * total:.1f} kJ/mol")

    lam = 0.8
    print(f"\nTunnelling at the optimum (dG = -lambda = -{lam} eV):")
    for r in (5, 10, 14, 20, 25):
        k = marcus_rate(-lam, lam, r)
        print(f"  r = {r:2d} A: k = {k:.1e} s^-1, time = {1 / k:.1e} s")
    g = dG_per_electron(0.25, 0.29)   # cytochrome c -> cytochrome a (CHAIN table values)
    print(f"\ncyt c -> cyt a: dG = {g:+.2f} eV; at 14 A with lambda = {lam} eV, k = {marcus_rate(g, lam, 14):.1e} s^-1")

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 4))
    rr = np.linspace(3, 30, 100)
    a1.semilogy(rr, [marcus_rate(-lam, lam, r) for r in rr])
    a1.axhline(1e3, ls=":", c="gray"); a1.text(20, 2e3, "1 ms", color="gray")
    a1.set_xlabel("donor-acceptor distance (angstrom)"); a1.set_ylabel("k (s$^{-1}$)"); a1.set_title("Distance")
    gg = np.linspace(-2.0, 0.3, 200)
    a2.semilogy(-gg, [marcus_rate(x, lam, 10) for x in gg])
    a2.axvline(lam, ls=":", c="gray"); a2.text(lam + 0.05, 1e4, "-dG = lambda")
    a2.set_xlabel("driving force -dG (eV)"); a2.set_ylabel("k at 10 angstrom (s$^{-1}$)"); a2.set_title("Driving force")
    fig.tight_layout()
    fig.savefig(runs_dir() / "lesson04_electron_transfer.png", dpi=120)
    print("wrote runs/lesson04_electron_transfer.png")


if __name__ == "__main__":
    main()
