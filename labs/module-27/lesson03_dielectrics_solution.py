"""Lesson 27.3 (reference solution): polarisability and dipole moments from dielectric data.

Run from this folder:
    py lesson03_dielectrics_solution.py                       (data files in this folder)
    py lesson03_dielectrics_solution.py my_debye_points.csv   (your own T_K,eps_minus_1_ppm data at 1 atm)
Part 1: Clausius-Mossotti for the NBS reference gases: polarisability volume from (eps - 1), against CCCBDB.
Part 2: molar polarisation P and molar refraction R of liquids (NBS Circular 514, PubChem): where P = R and
        where it fails; naive Debye and Onsager dipole moments of polar liquids against the gas values.
Part 3: Debye plot for HCl gas: P against 1/T gives A (intercept) and mu (slope).
Writes runs/lesson03_dielectrics.png.
"""
import sys
from pathlib import Path

import numpy as np

from pc27 import HERE, EPS0, K_B, N_A, R, ATM, DEBYE, ANGSTROM, read_csv, column, linfit, todo, save_plot, pyplot

T20 = 293.15


def cm_ratio(eps):
    """Clausius-Mossotti ratio (eps - 1)/(eps + 2)."""
    eps = np.asarray(eps, float)
    return (eps - 1) / (eps + 2)


def alpha_volume_gas(eps_minus_1, T, p):
    """Polarisability volume alpha' (m^3) of an ideal gas from its dielectric constant:
    (eps - 1)/(eps + 2) = N alpha' 4 pi / 3, with number density N = p/(k_B T)."""
    N = p / (K_B * T)
    return 3 * cm_ratio(1 + np.asarray(eps_minus_1)) / (4 * np.pi * N)


def molar_polarisation(eps, M, rho):
    """Molar polarisation P = (eps - 1)/(eps + 2) * M/rho, in cm^3/mol for M in g/mol and rho in g/cm^3.
    With n^2 in place of eps the same formula gives the molar refraction R (Lorentz-Lorenz)."""
    return cm_ratio(eps) * np.asarray(M) / np.asarray(rho)


def debye_mu(B):
    """Dipole moment (C m) from the slope B (m^3 K/mol) of P = A + B/T, since B = N_A mu^2/(9 eps0 k_B)."""
    return np.sqrt(9 * EPS0 * K_B * np.asarray(B) / N_A)


def onsager_mu(eps, n2, M, rho, T):
    """Onsager's dipole moment (C m) for a polar liquid:
    (eps - n^2)(2 eps + n^2) / (eps (n^2 + 2)^2) = N mu^2 / (9 eps0 k_B T), N = rho N_A / M (molecules per m^3)."""
    N = np.asarray(rho) * 1e6 / np.asarray(M) * N_A
    lhs = np.clip((eps - n2) * (2 * eps + n2) / (eps * (n2 + 2) ** 2), 0, None)
    return np.sqrt(lhs * 9 * EPS0 * K_B * T / N)


def main():
    pts = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "hcl_debye_points.csv"
    gases = read_csv(HERE / "reference_gases_nbs537.csv")
    em1 = column(gases, "eps_minus_1_ppm") * 1e-6
    a_cm = alpha_volume_gas(em1, T20, ATM)
    liq = read_csv(HERE / "liquids_nbs514.csv")
    M, rho, eps, nD = (column(liq, k) for k in ("M_g_mol", "rho_g_cm3", "eps_r", "n_D"))
    P = molar_polarisation(eps, M, rho)
    rows = read_csv(pts)
    T, e1 = column(rows, "T_K"), column(rows, "eps_minus_1_ppm") * 1e-6
    if todo(a_cm, P, debye_mu(1.0)):
        return

    # Part 1
    print("Part 1: Clausius-Mossotti for the reference gases at 20 C, 1 atm (NBS Circular 537)")
    print(f"  {'gas':5s} {'(eps-1)/ppm':>11s} {'alpha_CM/A^3':>13s} {'CCCBDB/A^3':>11s} {'diff':>6s}")
    for g, e, a in zip(gases, em1, a_cm):
        ref = g["alpha_A3_cccbdb"]
        diff = f"{(a / ANGSTROM ** 3) / float(ref) - 1:+6.1%}" if ref else ""
        print(f"  {g['gas']:5s} {e * 1e6:11.1f} {a / ANGSTROM ** 3:13.3f} {ref or '-':>11s} {diff}")

    # Part 2
    Rm = molar_polarisation(nD ** 2, M, rho)
    mu_gas = column(liq, "mu_gas_D")
    naive = debye_mu(np.clip(P - Rm, 0, None) * 1e-6 * T20) / DEBYE
    ons = onsager_mu(eps, nD ** 2, M, rho, T20) / DEBYE
    print("Part 2: liquids at 20 C. P and R in cm^3/mol; mu in debye")
    print(f"  {'liquid':21s} {'P':>6s} {'R':>6s} {'P-R':>6s} {'alpha_R/A^3':>11s} {'mu naive':>9s} {'Onsager':>8s} {'gas':>6s}")
    for r, p_, rm, nv, on, mg in zip(liq, P, Rm, naive, ons, mu_gas):
        a_r = 3 * rm * 1e-6 / (4 * np.pi * N_A) / ANGSTROM ** 3
        print(f"  {r['name']:21s} {p_:6.2f} {rm:6.2f} {p_ - rm:6.2f} {a_r:11.2f} {nv:9.2f} {on:8.2f} {mg:6.2f}")

    # Part 3
    Pm = cm_ratio(1 + e1) * R * T / ATM * 1e6          # cm^3/mol, ideal gas at 1 atm
    a, b, sa, sb = linfit(1 / T, Pm)
    mu, smu = debye_mu(b * 1e-6), debye_mu(b * 1e-6) * sb / (2 * b)
    print(f"Part 3: Debye plot for {pts.name} ({len(T)} temperatures, {T.min():.0f}-{T.max():.0f} K)")
    print(f"  P = A + B/T:  A = {a:.2f} +/- {sa:.2f} cm^3/mol,  B = {b:.0f} +/- {sb:.0f} cm^3 K/mol")
    print(f"  mu = {mu / DEBYE:.3f} +/- {smu / DEBYE:.3f} D   (NBS Circ. 537 fit of Zahn: 1.050 D, A = 7.63; "
          f"microwave Stark: 1.093 D)")
    print(f"  alpha' from A = {3 * a * 1e-6 / (4 * np.pi * N_A) / ANGSTROM ** 3:.2f} A^3 (CCCBDB electronic: 2.515 A^3)")
    print(f"  orientation share of P at 298 K: {b / 298 / (a + b / 298):.0%}")

    deb = read_csv(HERE / "debye_gases_nbs537.csv")
    print("  other gases (NBS Circ. 537): orientation share of P at 298 K")
    for g in deb:
        Bg = N_A * (float(g["mu_D"]) * DEBYE) ** 2 / (9 * EPS0 * K_B) * 1e6
        A = float(g["A_cm3_mol"])
        print(f"    {g['gas']:4s} mu {float(g['mu_D']):.3f} D (Stark {float(g['mu_stark_D']):.3f}), "
              f"A {A:5.2f}, B/298 {Bg / 298:6.1f} cm^3/mol -> {Bg / 298 / (A + Bg / 298):.0%}")

    plt = pyplot()
    if plt is None:
        return
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.6))
    x = 1 / T
    a1.plot(x * 1000, Pm, "o", label=pts.name)
    xx = np.linspace(0, x.max() * 1.05, 50)
    a1.plot(xx * 1000, a + b * xx, "-", label=f"fit: mu = {mu / DEBYE:.3f} D")
    a1.set_xlabel("1000/T (1/K)")
    a1.set_ylabel("P (cm^3/mol)")
    a1.legend(fontsize=8)
    a2.bar(range(len(liq)), P, label="P (static)")
    a2.bar(range(len(liq)), Rm, label="R (optical)")
    a2.set_xticks(range(len(liq)))
    a2.set_xticklabels([r["formula"] for r in liq], rotation=45, fontsize=8)
    a2.set_ylabel("cm^3/mol")
    a2.legend(fontsize=8)
    save_plot(fig, "lesson03_dielectrics.png")


if __name__ == "__main__":
    main()
