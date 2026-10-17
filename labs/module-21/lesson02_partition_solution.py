"""Lesson 21.2 reference solution: the partition function and what it predicts.

Run from this folder:  py lesson02_partition_solution.py

Builds q, U and Cv from a list of levels, then checks two real cases against NIST data:
(1) the electronic heat capacity of Cl atoms (2P3/2, 2P1/2; NIST ASD) against the NIST-JANAF Cp of Cl(g);
(2) the vibrational heat capacity of N2 (harmonic ladder, NIST WebBook constants) against the NIST
    Shomate Cp of N2(g). Writes runs/lesson02_heat_capacity.png.
"""
import math
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from stat21 import HC_K, R, ATOM_LEVELS, w0, read_janaf

RUNS = Path(__file__).resolve().parent / "runs"

# NIST WebBook N2(g) Shomate coefficients, 500-2000 K (Chase 1998), Cp in J/(mol K), t = T/1000
N2_SHOMATE = dict(A=19.50583, B=19.88705, C=-8.598535, D=1.369784, E=0.527601)


def n2_cp_nist(T):
    t = T / 1000
    c = N2_SHOMATE
    return c["A"] + c["B"] * t + c["C"] * t**2 + c["D"] * t**3 + c["E"] / t**2


# ---------------- TODO 1 ----------------
def q_levels(levels, T):
    """Partition function q = sum g exp(-E/kT) for levels given as (E in cm^-1, g)."""
    return sum(g * math.exp(-HC_K * e / T) for e, g in levels)


# ---------------- TODO 2 ----------------
def mean_energy(levels, T):
    """Mean energy per molecule in cm^-1: sum E g exp(-E/kT) / q."""
    return sum(e * g * math.exp(-HC_K * e / T) for e, g in levels) / q_levels(levels, T)


# ---------------- TODO 3 ----------------
def cv_molar(levels, T, dT=0.01):
    """Molar heat capacity (J/(mol K)) of these levels: R * HC_K * d<E>/dT, by a central difference."""
    return R * HC_K * (mean_energy(levels, T + dT) - mean_energy(levels, T - dT)) / (2 * dT)


def missing():
    """Names of the exercise functions that still return None (TODO)."""
    tests = {"q_levels": lambda: q_levels([(0, 1)], 300),
             "mean_energy": lambda: mean_energy([(0, 1), (100, 1)], 300),
             "cv_molar": lambda: cv_molar([(0, 1), (100, 1)], 300)}
    out = []
    for name, f in tests.items():
        try:
            if f() is None:
                out.append(name)
        except TypeError:
            out.append(name)
    return out


def main():
    if missing():
        print("TODO: write " + ", ".join(f"{m}()" for m in missing()) + " first (see lesson 21.2).")
        return
    RUNS.mkdir(exist_ok=True)

    # 1. Two-level example and the meaning of q
    cl = ATOM_LEVELS["Cl"]
    print("Cl atom electronic partition function (levels 0 g=4, 882.35 g=2):")
    for T in (100, 298.15, 1000, 5000, 1e6):
        print(f"  T = {T:>9.2f} K   q_el = {q_levels(cl, T):.4f}   <E> = {mean_energy(cl, T):7.2f} cm-1")

    # 2. Cl(g) Cp = 5/2 R (translation) + electronic part, against JANAF
    print("\nCl(g) heat capacity, J/(mol K):   T     model    JANAF")
    for row in read_janaf():
        if row["species"] != "Cl(g)":
            continue
        T = row["T_K"]
        cp = 2.5 * R + cv_molar(cl, T)
        print(f"                                {T:6.0f}  {cp:7.3f}  {row['Cp']:7.3f}")
    ts = np.linspace(50, 3000, 300)
    cv_el = [cv_molar(cl, T) for T in ts]
    k = int(np.argmax(cv_el))
    print(f"  electronic peak: {cv_el[k]:.3f} J/(mol K) at about {ts[k]:.0f} K (Schottky anomaly)")

    # 3. N2 vibration: harmonic ladder from v = 0
    nu = w0("N2")
    ladder = [(v * nu, 1) for v in range(60)]
    print(f"\nN2 heat capacity, harmonic ladder with w0 = {nu:.2f} cm-1 (theta_vib = {HC_K * nu:.0f} K):")
    print("    T    Cv_vib   7/2 R + Cv_vib   NIST Shomate")
    for T in (500, 800, 1000, 1500, 2000):
        cvv = cv_molar(ladder, T)
        print(f"  {T:5.0f}  {cvv:6.3f}   {3.5 * R + cvv:8.3f}        {n2_cp_nist(T):8.3f}")

    # 4. I2 at 298.15 K: a soft vibration
    i2 = [(v * w0("I2"), 1) for v in range(200)]
    cvv = cv_molar(i2, 298.15)
    print(f"\nI2 at 298.15 K: Cv_vib = {cvv:.3f}, Cp = 7/2 R + Cv_vib = {3.5 * R + cvv:.3f} J/(mol K) "
          f"(JANAF 36.887)")

    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    ax[0].plot(ts, np.array(cv_el) + 2.5 * R, label="model: 5/2 R + electronic")
    jan = [r for r in read_janaf() if r["species"] == "Cl(g)"]
    ax[0].plot([r["T_K"] for r in jan], [r["Cp"] for r in jan], "o", label="NIST-JANAF")
    ax[0].set_xlabel("T / K")
    ax[0].set_ylabel("Cp / J mol$^{-1}$ K$^{-1}$")
    ax[0].set_title("Cl(g): Schottky anomaly")
    ax[0].legend()
    t2 = np.linspace(300, 2000, 100)
    ax[1].plot(t2, [3.5 * R + cv_molar(ladder, T) for T in t2], label="model: 7/2 R + harmonic ladder")
    ax[1].plot(t2, [n2_cp_nist(T) for T in t2], "--", label="NIST Shomate (500-2000 K)")
    ax[1].set_xlabel("T / K")
    ax[1].set_title("N2(g)")
    ax[1].legend()
    fig.tight_layout()
    fig.savefig(RUNS / "lesson02_heat_capacity.png", dpi=120)
    print(f"\nPlot written to {RUNS / 'lesson02_heat_capacity.png'}")


if __name__ == "__main__":
    main()
