"""Lesson 32.4 (reference solution): from molecular orbitals to bands, and intrinsic carriers in semiconductors.

Run from this folder:
    py lesson04_bands_solution.py
No data file: everything is calculated.
Part 1: Hueckel (tight-binding) chain of N identical atoms, alpha = 0, beta = -2.5 eV: levels for N = 2..1000,
        band width -> 4|beta|, density of states against the analytic 1 / (pi sqrt(4 beta^2 - E^2)).
Part 2: chain with alternating site energies alpha_A, alpha_B: a gap of |alpha_A - alpha_B| opens.
Part 3: intrinsic carrier density n_i(T) = sqrt(Nc Nv) exp(-Eg(T) / 2kT) for Si, Ge and GaAs with the
        Ioffe NSM archive parameters (Nc, Nv at 300 K scaled as T^1.5; Varshni Eg(T)), checked 2026-10-17:
        http://www.ioffe.ru/SVA/NSM/Semicond/
Writes runs/lesson04_bands.png.
"""
import numpy as np

from ec32 import K_B_EV, todo, save_plot, pyplot

# Ioffe NSM: Nc, Nv at 300 K (cm^-3); Varshni Eg(T) = E0 - a T^2 / (T + b) (eV)
SEMI = {
    "Si": dict(Nc=3.2e19, Nv=1.8e19, E0=1.17, a=4.73e-4, b=636),
    "Ge": dict(Nc=1.0e19, Nv=5.0e18, E0=0.742, a=4.8e-4, b=235),
    "GaAs": dict(Nc=4.7e17, Nv=9.0e18, E0=1.519, a=5.405e-4, b=204),
}


def chain_levels(N, alpha=0.0, beta=-2.5, alpha_b=None):
    """Eigenvalues (eV, sorted) of an open Hueckel chain of N sites with nearest-neighbour coupling beta.
    If alpha_b is given, the site energies alternate alpha, alpha_b, alpha, ... (two atoms per cell)."""
    diag = np.full(N, alpha, float)
    if alpha_b is not None:
        diag[1::2] = alpha_b
    H = np.diag(diag) + np.diag(np.full(N - 1, beta), 1) + np.diag(np.full(N - 1, beta), -1)
    return np.linalg.eigvalsh(H)


def eg(T, E0, a, b, **_):
    """Varshni band gap (eV) at temperature T (K)."""
    return E0 - a * T**2 / (T + b)


def n_intrinsic(T, Nc, Nv, E0, a, b):
    """Intrinsic carrier density (cm^-3) at T (K): Nc and Nv scale as (T/300)^1.5."""
    s = (np.asarray(T, float) / 300.0) ** 1.5
    return np.sqrt(Nc * s * Nv * s) * np.exp(-eg(T, E0, a, b) / (2 * K_B_EV * np.asarray(T, float)))


def main():
    if todo(chain_levels(4), n_intrinsic(300.0, **SEMI["Si"])):
        return
    print("Part 1: Hueckel chain, alpha = 0, beta = -2.5 eV (4|beta| = 10 eV)")
    for N in (2, 4, 10, 100, 1000):
        E = chain_levels(N)
        gap = np.min(np.diff(E))
        print(f"  N = {N:4d}: lowest {E[0]:7.3f}, highest {E[-1]:6.3f} eV, width {E[-1] - E[0]:6.3f} eV, "
              f"smallest spacing {gap:.4f} eV")
    E = chain_levels(1000)
    hist, edges = np.histogram(E, bins=20, range=(-5, 5), density=True)
    mid = 0.5 * (edges[1:] + edges[:-1])
    print(f"  DOS at band centre {hist[9]:.3f} vs analytic {1 / (np.pi * 5):.3f} per eV; "
          f"edge bin {hist[0]:.3f} (it diverges at the band edge)")
    print("Part 2: alternating site energies (two atoms per cell), beta = -2.5 eV, N = 1000")
    for da in (0.0, 1.0, 3.0, 6.0):
        E2 = chain_levels(1000, alpha=+da / 2, alpha_b=-da / 2)
        lower, upper = E2[:500], E2[500:]
        print(f"  alpha_A - alpha_B = {da:.1f} eV: gap = {upper.min() - lower.max():.3f} eV")
    print("  One electron per atom fills the lower band exactly: no gap = metal, a gap = semiconductor or insulator.")
    print("Part 3: intrinsic carriers")
    for name, p in SEMI.items():
        n300 = n_intrinsic(300.0, **p)
        n400 = n_intrinsic(400.0, **p)
        print(f"  {name:4s}: Eg(300 K) = {eg(300, **p):.3f} eV, n_i(300 K) = {n300:.2e} cm^-3, "
              f"n_i(400 K) = {n400:.2e} (x {n400 / n300:.0f})")
    T = np.linspace(250, 500, 6)
    p = SEMI["Si"]
    y = np.log(n_intrinsic(T, **p) / T**1.5)
    slope = np.polyfit(1 / T, y, 1)[0]
    print(f"  Si: slope of ln(n_i / T^1.5) against 1/T gives Eg = {-2 * K_B_EV * slope:.3f} eV "
          f"(the 0 K extrapolation of the linear part of Eg(T), not Eg at 300 K)")
    plt = pyplot()
    if plt:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        ax1.bar(mid, hist, width=0.45, label="N = 1000 chain")
        xx = np.linspace(-4.99, 4.99, 400)
        ax1.plot(xx, 1 / (np.pi * np.sqrt(25 - xx**2)), "r", label="analytic DOS")
        ax1.set_xlabel("E / eV")
        ax1.set_ylabel("density of states / eV$^{-1}$ per site")
        ax1.set_ylim(0, 0.6)
        ax1.legend(fontsize=8)
        TT = np.linspace(200, 600, 100)
        for name, q in SEMI.items():
            ax2.semilogy(1000 / TT, n_intrinsic(TT, **q), label=name)
        ax2.set_xlabel("1000 / T (K$^{-1}$)")
        ax2.set_ylabel("$n_i$ / cm$^{-3}$")
        ax2.legend(fontsize=8)
        save_plot(fig, "lesson04_bands.png")


if __name__ == "__main__":
    main()
