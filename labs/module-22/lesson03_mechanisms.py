"""Lesson 22.3 - mechanisms: the steady-state test, Lindemann falloff of N2O5, 2NO + O2.

Fill in the functions marked TODO, then run:  py lesson03_mechanisms.py
Reference solution: lesson03_mechanisms_solution.py
Writes runs/lesson03_mechanisms.png.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

from kin22 import K_B, N2O5_K0, N2O5_KINF, NO_O2, R, k_mod_arrhenius, number_density, runs_dir


def exact_product(t, A0, k1, k2):
    """[P](t) for A -> I -> P solved numerically with tight tolerances."""
    f = lambda _t, y: [-k1 * y[0], k1 * y[0] - k2 * y[1], k2 * y[1]]
    sol = solve_ivp(f, (0, t[-1]), [A0, 0.0, 0.0], t_eval=t, method="LSODA", rtol=1e-10, atol=1e-14)
    return sol.y[2]


def ssa_product(t, A0, k1):
    """Steady-state approximation for A -> I -> P: d[P]/dt = k1[A], so [P] = A0 (1 - exp(-k1 t))."""
    # TODO: return A0 * (1 - np.exp(-k1 * t))
    raise NotImplementedError("TODO: write ssa_product() first (see the hints in the code).")


def lindemann(k0, kinf, M):
    """Lindemann unimolecular rate constant k = k0[M] kinf / (k0[M] + kinf)."""
    # TODO: return k0 * M * kinf / (k0 * M + kinf)
    raise NotImplementedError("TODO: write lindemann() first (see the hints in the code).")


def half_pressure(k0, kinf, T):
    """Pressure (bar) at which k0[M] = kinf, so k = kinf/2."""
    # TODO: M_half = kinf / k0 (molecules per cm^3)
    # TODO: convert to bar with p = M_half * 1e6 * K_B * T / 1e5
    raise NotImplementedError("TODO: write half_pressure() first (see the hints in the code).")


def main():
    t = np.linspace(0, 10, 201)                  # time in units of 1/k1
    for ratio in (20.0, 1.0):
        err = np.max(np.abs(exact_product(t, 1.0, 1.0, ratio) - ssa_product(t, 1.0, 1.0)))
        print(f"k2/k1 = {ratio:4.0f}: largest error of the SSA product curve = {err:.3f} (fraction of A0)")

    T = 298.0
    k0, kinf = k_mod_arrhenius(N2O5_K0, T), k_mod_arrhenius(N2O5_KINF, T)
    print(f"N2O5 at {T:.0f} K: k0 = {k0:.2e} cm3 molecule-1 s-1, kinf = {kinf:.3f} s-1")
    for p in (1e-4, 1e-3, 1e-2, 0.1, 1.0):
        k = lindemann(k0, kinf, number_density(p, T))
        print(f"   p = {p:7.4f} bar: k_uni = {k:.3e} s-1 = {k / kinf:.3f} kinf")
    print(f"   half-pressure (Lindemann) = {half_pressure(k0, kinf, T) * 1000:.0f} mbar")

    for T in (270.0, 298.0, 400.0, 600.0):
        print(f"2NO + O2 at {T:3.0f} K: k = {k_mod_arrhenius(NO_O2, T):.2e} cm6 molecule-2 s-1")
    print(f"   apparent Ea = {NO_O2['Ea'] / 1000:.1f} kJ/mol (negative: k falls as T rises)")

    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    for ratio in (20.0, 1.0):
        ax[0].plot(t, exact_product(t, 1.0, 1.0, ratio), label=f"exact, k2/k1 = {ratio:g}")
    ax[0].plot(t, ssa_product(t, 1.0, 1.0), "k--", label="steady state")
    ax[0].set_xlabel("k1 t"); ax[0].set_ylabel("[P]/[A]0"); ax[0].legend()
    p = np.logspace(-5, 1, 200)
    T = 298.0
    ax[1].semilogx(p, lindemann(k0, kinf, number_density(p, T)) / kinf)
    ax[1].set_xlabel("pressure of N2 / bar"); ax[1].set_ylabel("k_uni / k_inf (Lindemann)")
    fig.tight_layout(); fig.savefig(runs_dir() / "lesson03_mechanisms.png", dpi=120)
    print("saved runs/lesson03_mechanisms.png")


if __name__ == "__main__":
    try:
        main()
    except NotImplementedError as e:
        print(e)
