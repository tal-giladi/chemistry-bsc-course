"""Lesson 27.4 (exercise, module practical: fill in the TODO functions): intermolecular forces from electrostatics.

Run from this folder:
    py lesson04_imf.py              (imf_molecules.csv, water_tip3p.csv, co2_point_charges.csv)
    py lesson04_imf.py 350          (same, with the Keesom term at 350 K instead of 298 K)
Part 1: Keesom, Debye and London r^-6 coefficients for real molecules (CCCBDB mu and alpha', NIST WebBook IE)
        and how their total tracks the normal boiling point.
Part 2: the water dimer with TIP3P point charges plus the O-O Lennard-Jones term: scan the O...O distance and
        the tilt of the acceptor, find the minimum, and compare with the point-dipole approximation.
Part 3: the CO2 dimer (EPM2 charges): electrostatic energy of end-to-end, parallel and T-shaped pairs.
Writes runs/lesson04_imf.png.
"""
import sys

import numpy as np

from pc27 import HERE, K_C, K_B, N_A, DEBYE, ANGSTROM, EV, read_csv, column, read_charges, todo, save_plot, pyplot

KJ = 1000 / N_A                       # J per (kJ/mol)
LJ_EPS = 0.1521 * 4.184 * KJ          # TIP3P O-O well depth, J (0.1521 kcal/mol)
LJ_SIG = 3.1507 * ANGSTROM            # TIP3P O-O sigma, m


def keesom_c6(mu, T):
    """Boltzmann-averaged dipole-dipole attraction between two identical molecules: V = -C/r^6 with
    C = (2/3) mu^4 / ((4 pi eps0)^2 k_B T).  mu in C m, result in J m^6. K_C = 1/(4 pi eps0).
    TODO: one line."""
    return None  # TODO


def debye_c6(mu, alpha_v):
    """Dipole-induced-dipole attraction between two identical molecules (each induces the other):
    C = 2 mu^2 alpha' / (4 pi eps0) = 2 K_C mu^2 alpha', with alpha' in m^3.
    TODO: one line."""
    return None  # TODO


def london_c6(alpha_v, ie):
    """London dispersion between two identical molecules: C = (3/4) I alpha'^2, I in J, alpha' in m^3.
    TODO: one line."""
    return None  # TODO


def pair_energy(xyz1, q1, xyz2, q2):
    """Coulomb energy (J) between two sets of point charges (intermolecular pairs only):
    U = sum_i sum_j K_C q1_i q2_j / |r1_i - r2_j|.
    TODO: two lines (a double loop is fine)."""
    return None  # TODO


def lennard_jones(r):
    return 4 * LJ_EPS * ((LJ_SIG / r) ** 12 - (LJ_SIG / r) ** 6)


def water_dimer(R, tilt_deg):
    """TIP3P water dimer with a linear O-H...O bond along x. Donor in the xy plane; acceptor O at (R, 0, 0),
    its bisector (pointing away from the donor) tilted by tilt_deg out of the x axis in the xz plane, its
    plane perpendicular to the donor plane. Returns (xyz_donor, q, xyz_acceptor, q) in m and C."""
    _, w, q = read_charges(HERE / "water_tip3p.csv")
    r_oh = np.linalg.norm(w[1] - w[0])
    half = np.arccos(np.dot(w[1] - w[0], w[2] - w[0]) / r_oh ** 2) / 2
    ang = 2 * half
    donor = np.array([[0, 0, 0], [r_oh, 0, 0], [r_oh * np.cos(ang), r_oh * np.sin(ang), 0]])
    t = np.radians(tilt_deg)
    b = np.array([np.cos(t), 0, np.sin(t)])
    y = np.array([0, 1.0, 0])
    oa = np.array([R, 0, 0])
    acc = np.array([oa, oa + r_oh * (np.cos(half) * b + np.sin(half) * y),
                    oa + r_oh * (np.cos(half) * b - np.sin(half) * y)])
    return donor, q, acc, q


def dimer_energy(R, tilt_deg):
    d, qd, a, qa = water_dimer(R, tilt_deg)
    return pair_energy(d, qd, a, qa) + lennard_jones(R)


def dipole_vector(xyz, q):
    return np.sum(q[:, None] * (xyz - xyz.mean(axis=0)), axis=0)


def main():
    T = float(sys.argv[1]) if len(sys.argv) > 1 else 298.15
    mol = read_csv(HERE / "imf_molecules.csv")
    mu = column(mol, "mu_D") * DEBYE
    al = column(mol, "alpha_A3") * ANGSTROM ** 3
    ie = column(mol, "IE_eV") * EV
    bp = column(mol, "bp_K")
    ck, cd, cl = keesom_c6(mu, T), debye_c6(mu, al), london_c6(al, ie)
    if todo(ck, cd, cl, pair_energy(np.zeros((1, 3)), np.ones(1), np.ones((1, 3)), np.ones(1))):
        return

    # Part 1
    unit = 1e-79                                     # J m^6
    tot = ck + cd + cl
    print(f"Part 1: r^-6 coefficients for like pairs, in 10^-79 J m^6 (Keesom at {T:.0f} K)")
    print(f"  {'molecule':8s} {'Keesom':>8s} {'Debye':>7s} {'London':>8s} {'total':>8s}  "
          f"{'%K':>4s} {'%D':>4s} {'%L':>4s}  {'bp/K':>6s}")
    for m, k, d, l, t, b in zip(mol, ck, cd, cl, tot, bp):
        print(f"  {m['molecule']:8s} {k / unit:8.1f} {d / unit:7.1f} {l / unit:8.1f} {t / unit:8.1f}  "
              f"{k / t:4.0%} {d / t:4.0%} {l / t:4.0%}  {b:6.1f}")
    nonpolar = column(mol, "mu_D") == 0
    rho = np.corrcoef(np.log(tot[nonpolar]), bp[nonpolar])[0, 1]
    print(f"  non-polar molecules: correlation of bp with ln(C6) r = {rho:.3f}")
    print("  energy at 0.4 nm for HCl pair: "
          f"{-tot[[m['molecule'] for m in mol].index('HCl')] / (0.4e-9) ** 6 / KJ:.2f} kJ/mol (r^-6 terms only)")

    # Part 2
    Rs = np.linspace(2.5, 4.0, 61) * ANGSTROM
    tilts = np.arange(0, 91, 5)
    E = np.array([[dimer_energy(R, t) for t in tilts] for R in Rs]) / KJ
    i, j = np.unravel_index(np.argmin(E), E.shape)
    print("Part 2: TIP3P water dimer (Coulomb + O-O Lennard-Jones), linear H-bond")
    print(f"  minimum E = {E[i, j]:.1f} kJ/mol at R(O...O) = {Rs[i] / ANGSTROM:.2f} A, acceptor tilt {tilts[j]} deg")
    print(f"  at the same geometry: Coulomb {pair_energy(*water_dimer(Rs[i], tilts[j])) / KJ:.1f}, "
          f"LJ {lennard_jones(Rs[i]) / KJ:+.1f} kJ/mol")
    d, qd, a, qa = water_dimer(Rs[i], tilts[j])
    m1, m2 = dipole_vector(d, qd), dipole_vector(a, qa)
    rv = a.mean(axis=0) - d.mean(axis=0)
    rr = np.linalg.norm(rv)
    u = rv / rr
    e_dd = K_C * (m1 @ m2 - 3 * (m1 @ u) * (m2 @ u)) / rr ** 3
    print(f"  point-dipole estimate at the same geometry: {e_dd / KJ:.1f} kJ/mol (centre distance {rr / ANGSTROM:.2f} A)")
    for t in (0, 30, 60, 90):
        print(f"  tilt {t:2d} deg: E = {dimer_energy(Rs[i], t) / KJ:6.1f} kJ/mol")

    # Part 3
    _, c, qc = read_charges(HERE / "co2_point_charges.csv")
    rco = 1.162 * ANGSTROM
    rot = np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]])      # turns the molecular axis from z to x
    geoms = {
        "end-to-end, O...O 3.2 A": c + np.array([0, 0, 2 * rco + 3.2 * ANGSTROM]),
        "parallel, centres 4.0 A": c + np.array([4.0 * ANGSTROM, 0, 0]),
        "T-shaped, centres 4.0 A": (c @ rot.T) + np.array([0, 0, 4.0 * ANGSTROM]),
    }
    print("Part 3: CO2 dimer, electrostatics only (EPM2 charges)")
    for name, xyz2 in geoms.items():
        print(f"  {name:26s} {pair_energy(c, qc, xyz2, qc) / KJ:+6.2f} kJ/mol")

    plt = pyplot()
    if plt is None:
        return
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.5, 3.8))
    a1.semilogx(tot / unit, bp, "o")
    for x, yv, m in zip(tot / unit, bp, mol):
        a1.annotate(m["molecule"], (x, yv), fontsize=7)
    a1.set_xlabel("C6 total (10^-79 J m^6)")
    a1.set_ylabel("normal boiling point (K)")
    a2.plot(Rs / ANGSTROM, E[:, j], label=f"tilt {tilts[j]} deg")
    a2.plot(Rs / ANGSTROM, E[:, 0], "--", label="tilt 0 deg")
    a2.set_ylim(E.min() * 1.2, 15)
    a2.axhline(0, color="grey", lw=0.5)
    a2.set_xlabel("R(O...O) (A)")
    a2.set_ylabel("E (kJ/mol)")
    a2.legend()
    save_plot(fig, "lesson04_imf.png")


if __name__ == "__main__":
    main()
