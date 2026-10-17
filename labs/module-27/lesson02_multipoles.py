"""Lesson 27.2 (exercise: fill in the TODO functions): multipole moments from point charges.

Run from this folder:
    py lesson02_multipoles.py                     (water, CO2 and OH- models in this folder)
    py lesson02_multipoles.py my_molecule.csv     (your own model: label,x_A,y_A,z_A,q_e)
Part 1: charge, dipole and traceless quadrupole of each model, about its centre of mass.
Part 2: origin dependence: shift the origin by 1 A and see which moments change.
Part 3: the multipole expansion of the potential of water along its dipole axis against the exact sum.
Writes runs/lesson02_multipoles.png.
"""
import sys
from pathlib import Path

import numpy as np

from pc27 import HERE, E, K_C, DEBYE, ANGSTROM, read_charges, todo, save_plot, pyplot

MASS = {"O": 15.999, "H": 1.008, "C": 12.011, "N": 14.007, "Cl": 35.45}
D_A = DEBYE * ANGSTROM          # 1 D A = 3.33564e-40 C m^2
EXPERIMENT = {                  # gas-phase values, NIST CCCBDB (dipoles and quadrupoles lists), checked 2026-10-17
    "water_tip3p.csv": "experiment: mu = 1.857 D (gas)",
    "co2_point_charges.csv": "experiment: Theta_zz = -14.27 +/- 0.61 x 10^-40 C m^2 = -4.28 D A (Graham et al. 1998)",
}


def total_charge(q):
    """Net charge (C)."""
    return float(np.sum(q))


def dipole(xyz, q, origin):
    """Dipole moment vector mu = sum_i q_i (r_i - origin), in C m.
    TODO: one line. xyz is N x 3, q has length N; q[:, None] broadcasts the charges over x, y, z."""
    return None  # TODO


def quadrupole(xyz, q, origin):
    """Traceless (Buckingham) quadrupole tensor Theta_ab = 1/2 sum_i q_i (3 r_a r_b - r^2 delta_ab), in C m^2,
    with r measured from `origin`. Returns a 3 x 3 array.
    TODO: a double loop over a, b in range(3) is fine: Theta[a, b] = 0.5 * sum(q * (3 r[:, a] r[:, b] - r2 * (a == b))),
    with r = xyz - origin and r2 = |r|^2 for each charge. Check: the trace of the result must be zero."""
    return None  # TODO


def potential_exact(points, xyz, q):
    """Electrostatic potential (V) at points (N x 3) from all point charges: sum K_C q_i / |r - r_i|."""
    d = np.linalg.norm(points[:, None, :] - xyz[None, :, :], axis=2)
    return K_C * np.sum(q[None, :] / d, axis=1)


def potential_multipole(points, origin, Q, mu, theta, order):
    """Multipole expansion of the potential (V) about `origin`, up to `order` (0 charge, 1 dipole, 2 quadrupole):
    phi = K_C [ Q/r + mu.r/r^3 + sum_ab Theta_ab r_a r_b / r^5 ]."""
    r = points - origin
    rn = np.linalg.norm(r, axis=1)
    phi = Q / rn
    if order >= 1:
        phi = phi + r @ mu / rn ** 3
    if order >= 2:
        phi = phi + np.einsum("na,ab,nb->n", r, theta, r) / rn ** 5
    return K_C * phi


def centre_of_mass(labels, xyz):
    m = np.array([MASS[''.join(c for c in lab if c.isalpha())] for lab in labels])
    return np.sum(m[:, None] * xyz, axis=0) / m.sum()


def describe(path):
    labels, xyz, q = read_charges(path)
    o = centre_of_mass(labels, xyz)
    Q, mu, th = total_charge(q), dipole(xyz, q, o), quadrupole(xyz, q, o)
    print(f"  {path.name}: atoms {', '.join(labels)}")
    print(f"    charge {Q / E:+.3f} e;  dipole ({', '.join(f'{x / DEBYE:+.3f}' for x in mu)}) D, "
          f"|mu| = {np.linalg.norm(mu) / DEBYE:.3f} D")
    print(f"    quadrupole diagonal (xx, yy, zz) = ({', '.join(f'{th[i, i] / D_A:+.3f}' for i in range(3))}) D A "
          f"= ({', '.join(f'{th[i, i] / 1e-40:+.2f}' for i in range(3))}) x 10^-40 C m^2; trace {np.trace(th) / D_A:.1e}")
    if path.name in EXPERIMENT:
        print(f"    {EXPERIMENT[path.name]}")
    return labels, xyz, q, o


def main():
    files = [Path(p) for p in sys.argv[1:]] or [HERE / "water_tip3p.csv", HERE / "co2_point_charges.csv",
                                                HERE / "oh_minus_illustrative.csv"]
    _, xyz0, q0 = read_charges(HERE / "water_tip3p.csv")
    if todo(dipole(xyz0, q0, np.zeros(3)), quadrupole(xyz0, q0, np.zeros(3))):
        return

    print("Part 1: moments about the centre of mass")
    models = {p.name: describe(p) for p in files}

    print("Part 2: shift the origin by +1 A along x")
    shift = np.array([1.0, 0, 0]) * ANGSTROM
    for name, (labels, xyz, q, o) in models.items():
        dmu = (dipole(xyz, q, o + shift) - dipole(xyz, q, o)) / DEBYE
        dth = (quadrupole(xyz, q, o + shift) - quadrupole(xyz, q, o)) / D_A
        print(f"  {name}: change in mu = ({', '.join(f'{x:+.3f}' for x in dmu)}) D;  "
              f"largest change in Theta = {np.abs(dth).max():.3f} D A")

    if "water_tip3p.csv" not in models:
        return
    labels, xyz, q, o = models["water_tip3p.csv"]
    mu, th = dipole(xyz, q, o), quadrupole(xyz, q, o)
    r = np.linspace(2.5, 12, 60) * ANGSTROM
    pts = o + np.column_stack([np.zeros_like(r), np.zeros_like(r), r])
    exact = potential_exact(pts, xyz, q)
    dip = potential_multipole(pts, o, 0.0, mu, th, 1)
    quad = potential_multipole(pts, o, 0.0, mu, th, 2)
    print("Part 3: water, potential on the dipole axis (H side), exact vs expansion")
    print(f"  {'r/A':>5s} {'exact/V':>9s} {'dipole only':>12s} {'+quadrupole':>12s}")
    for k in (0, 7, 15, 31, 59):
        print(f"  {r[k] / ANGSTROM:5.1f} {exact[k]:9.4f} {dip[k]:12.4f} {quad[k]:12.4f}")
    plt = pyplot()
    if plt is None:
        return
    fig, ax = plt.subplots(figsize=(5.5, 3.8))
    ax.loglog(r / ANGSTROM, np.abs(dip / exact - 1), label="dipole only")
    ax.loglog(r / ANGSTROM, np.abs(quad / exact - 1), label="dipole + quadrupole")
    ax.set_xlabel("distance from centre of mass (A)")
    ax.set_ylabel("relative error of expansion")
    ax.set_title("water (TIP3P charges), on the dipole axis")
    ax.legend()
    save_plot(fig, "lesson02_multipoles.png")


if __name__ == "__main__":
    main()
