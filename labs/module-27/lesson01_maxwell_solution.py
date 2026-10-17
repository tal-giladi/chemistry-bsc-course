"""Lesson 27.1 (reference solution): Maxwell's equations in numbers.

Run from this folder:
    py lesson01_maxwell_solution.py                          (example microwave data, 2450 MHz)
    py lesson01_maxwell_solution.py my_microwave.csv 2450    (your spot spacings and the oven's frequency in MHz)
Part 1: the speed of light from eps0 and mu0 (CODATA 2022).
Part 2: Gauss's law checked numerically: the flux of E through a sphere equals Q_enclosed/eps0, whatever the
        charges outside do.
Part 3: the speed of light from the melted spots in a microwave oven (standing wave, spots lambda/2 apart).
Part 4: Maxwell's relation eps_r = n^2 tested on real liquids (NBS Circular 514, PubChem).
Writes runs/lesson01_maxwell.png.
"""
import sys
from pathlib import Path

import numpy as np

from pc27 import HERE, EPS0, MU0, C_LIGHT, K_C, E, read_csv, column, todo, save_plot, pyplot


def speed_of_light(eps0, mu0):
    """c = 1/sqrt(eps0 mu0), in m/s."""
    return 1 / np.sqrt(eps0 * mu0)


def field_at(points, xyz, q):
    """Electric field (V/m) at each row of `points` (N x 3, metres) from point charges q (C) at xyz (M x 3).
    Coulomb's law summed over charges (superposition, lesson 04.3)."""
    d = points[:, None, :] - xyz[None, :, :]               # N x M x 3 separation vectors
    r = np.linalg.norm(d, axis=2)                           # N x M distances
    return K_C * np.sum(q[None, :, None] * d / r[:, :, None] ** 3, axis=1)


def c_from_spots(spacing_cm, f_hz):
    """Neighbouring hot spots of a standing wave are half a wavelength apart: c = 2 d f (m/s)."""
    return 2 * np.asarray(spacing_cm) / 100 * f_hz


def sphere_points(n):
    """n nearly evenly spread points on the unit sphere (Fibonacci lattice); each stands for area 4 pi / n."""
    k = np.arange(n) + 0.5
    phi = np.arccos(1 - 2 * k / n)
    theta = np.pi * (1 + 5 ** 0.5) * k
    return np.column_stack([np.cos(theta) * np.sin(phi), np.sin(theta) * np.sin(phi), np.cos(phi)])


def main():
    mw = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "microwave_example.csv"
    f_hz = (float(sys.argv[2]) if len(sys.argv) > 2 else 2450.0) * 1e6
    c = speed_of_light(EPS0, MU0)
    spacing = column(read_csv(mw), "spacing_cm")
    c_mw = c_from_spots(spacing, f_hz)
    test = field_at(np.array([[1e-9, 0.0, 0.0]]), np.zeros((1, 3)), np.array([E]))
    if todo(c, c_mw, test):
        return

    # Part 1
    print(f"Part 1: c = 1/sqrt(eps0 mu0) = {c:,.1f} m/s (defined value {C_LIGHT:,.0f} m/s, "
          f"difference {abs(c - C_LIGHT) / C_LIGHT:.1e})")

    # Part 2: three charges inside a 5 A sphere, two outside (all in units of e, positions in A)
    rng = np.random.default_rng(1)
    q = np.array([+1.0, -0.4, -0.4, +2.0, -3.0]) * E
    xyz = np.array([[0.5, 0.2, -0.3], [-1.0, 0.8, 0.4], [1.2, -1.5, 0.9],
                    [7.0, 0.0, 0.0], [0.0, -6.5, 2.0]]) * 1e-10
    radius = 5e-10
    n = 20000
    u = sphere_points(n)
    E_surf = field_at(u * radius, xyz, q)
    flux = np.sum(np.sum(E_surf * u, axis=1)) * 4 * np.pi * radius ** 2 / n
    inside = np.linalg.norm(xyz, axis=1) < radius
    print(f"Part 2: flux through the sphere = {flux:.4e} V m;  Q_enclosed/eps0 = {q[inside].sum() / EPS0:.4e} V m")
    print(f"  enclosed charge {q[inside].sum() / E:+.2f} e; the {(~inside).sum()} outside charges "
          f"({q[~inside].sum() / E:+.1f} e) add nothing to the flux")
    xyz_moved = xyz + np.where(inside[:, None], 0.0, rng.normal(0, 2e-10, xyz.shape))
    flux2 = np.sum(np.sum(field_at(u * radius, xyz_moved, q) * u, axis=1)) * 4 * np.pi * radius ** 2 / n
    print(f"  after moving the outside charges at random: flux = {flux2:.4e} V m")

    # Part 3
    m, s = c_mw.mean(), c_mw.std(ddof=1) / np.sqrt(len(c_mw))
    print(f"Part 3: spot spacing {spacing.mean():.2f} cm (n = {len(spacing)}), f = {f_hz / 1e6:.0f} MHz")
    print(f"  c = 2 d f = ({m / 1e8:.3f} +/- {s / 1e8:.3f}) x 10^8 m/s; true value 2.998 x 10^8 m/s")

    # Part 4
    liq = read_csv(HERE / "liquids_nbs514.csv")
    print("Part 4: Maxwell's relation eps_r = n^2 (static permittivity vs optical refractive index, 20 C)")
    print(f"  {'liquid':22s} {'eps_r':>7s} {'n_D^2':>7s} {'ratio':>6s}  mu(gas)/D")
    for r in liq:
        eps, n2 = float(r["eps_r"]), float(r["n_D"]) ** 2
        print(f"  {r['name']:22s} {eps:7.3f} {n2:7.3f} {eps / n2:6.2f}  {float(r['mu_gas_D']):.2f}")

    plt = pyplot()
    if plt is None:
        return
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.6))
    a1.errorbar(range(1, len(c_mw) + 1), c_mw / 1e8, fmt="o")
    a1.axhline(C_LIGHT / 1e8, ls="--", color="grey", label="c (defined)")
    a1.set_xlabel("trial")
    a1.set_ylabel("c from spots (10^8 m/s)")
    a1.legend()
    eps = column(liq, "eps_r")
    n2 = column(liq, "n_D") ** 2
    a2.loglog(n2, eps, "o")
    for x, y, r in zip(n2, eps, liq):
        a2.annotate(r["name"], (x, y), fontsize=7)
    a2.plot([1.5, 3], [1.5, 3], "--", color="grey")
    a2.set_xlabel("n_D^2 (optical)")
    a2.set_ylabel("eps_r (static)")
    save_plot(fig, "lesson01_maxwell.png")


if __name__ == "__main__":
    main()
