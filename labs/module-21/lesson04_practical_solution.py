"""Lesson 21.4 reference solution (module practical): K(T) for I2(g) = 2 I(g) from spectroscopic constants.

Run from this folder:  py lesson04_practical_solution.py

Inputs: NIST WebBook constants of I2 (we, wexe, Be, ae), NIST ASD levels of the I atom, NIST standard
atomic weight of I, and D0 from the NIST-JANAF 0 K formation enthalpies (all in stat21.py).
Check data: NIST-JANAF log Kf of I(g) (janaf_check.csv). Writes runs/lesson04_vant_hoff.png.
"""
import math
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from stat21 import (R, HC_K, CM1_TO_KJMOL, MOLAR_MASS, DIATOMIC, ATOM_LEVELS, D0_I2_CM, D0_I2_KJMOL,
                    q_trans_std, q_rot_sum, q_vib_harmonic, q_vib_anharmonic, q_elec, w0, B0,
                    thermo_from_lnq, read_janaf)

RUNS = Path(__file__).resolve().parent / "runs"


def ln_q_i(T):
    """ln(q°/N_A) of the I atom: translation x electronic (2P3/2, 2P1/2)."""
    return math.log(q_trans_std(MOLAR_MASS["I"], T) * q_elec(ATOM_LEVELS["I"], T))


def ln_q_i2(T, vib="harmonic"):
    """ln(q°/N_A) of I2: translation x rotation (sum, sigma = 2) x vibration (from v = 0)."""
    d = DIATOMIC["I2"]
    qv = q_vib_harmonic(w0("I2"), T) if vib == "harmonic" else q_vib_anharmonic(d["we"], d["wexe"], T, D0_I2_CM)
    return math.log(q_trans_std(MOLAR_MASS["I2"], T) * q_rot_sum(B0("I2"), T, d["sigma"]) * qv)


# ---------------- TODO 1 ----------------
def k_dissociation(T, vib="harmonic", d0_cm=D0_I2_CM):
    """K for I2 = 2 I: (q_I°/N_A)^2 / (q_I2°/N_A) * exp(-D0 / kT), D0 in cm^-1."""
    return math.exp(2 * ln_q_i(T) - ln_q_i2(T, vib) - HC_K * d0_cm / T)


# ---------------- TODO 2 ----------------
def degree_of_dissociation(k, p_bar):
    """Fraction alpha of I2 dissociated at total pressure p: K = 4 alpha^2 / (1 - alpha^2) * p / p°."""
    return math.sqrt(k / (k + 4 * p_bar))


# ---------------- TODO 3 ----------------
def reaction_h_s(T, vib="anharmonic"):
    """Delta_r H° (kJ/mol) and Delta_r S° (J/(mol K)) of I2 = 2 I at T from the partition functions.
    Delta H = D0 (kJ/mol) + 2 [H - H0](I) - [H - H0](I2);  Delta S = 2 S(I) - S(I2)."""
    ti = thermo_from_lnq(ln_q_i, T)
    ti2 = thermo_from_lnq(lambda t: ln_q_i2(t, vib), T)
    dh = D0_I2_KJMOL + 2 * ti["H_minus_H0"] - ti2["H_minus_H0"]
    ds = 2 * ti["S"] - ti2["S"]
    return dh, ds


def missing():
    """Names of the exercise functions that still return None (TODO)."""
    tests = {"k_dissociation": lambda: k_dissociation(1000.0),
             "degree_of_dissociation": lambda: degree_of_dissociation(0.01, 1.0),
             "reaction_h_s": lambda: reaction_h_s(1000.0)}
    return [name for name, f in tests.items() if f() is None]


def main():
    if missing():
        print("TODO: write " + ", ".join(f"{m}()" for m in missing()) + " first (see lesson 21.4).")
        return
    RUNS.mkdir(exist_ok=True)
    jan = {r["T_K"]: r for r in read_janaf() if r["species"] == "I(g)" and r["T_K"] >= 500}

    print(f"D0(I2) = {D0_I2_KJMOL:.3f} kJ/mol = {D0_I2_CM:.1f} cm-1 (from JANAF 0 K formation enthalpies)")
    T = 1000.0
    print(f"\nPartition functions at {T:.0f} K:")
    print(f"  I : q_trans/N_A = {q_trans_std(MOLAR_MASS['I'], T):.4e}, q_el = {q_elec(ATOM_LEVELS['I'], T):.6f}")
    d = DIATOMIC["I2"]
    print(f"  I2: q_trans/N_A = {q_trans_std(MOLAR_MASS['I2'], T):.4e}, q_rot = {q_rot_sum(B0('I2'), T, 2):.1f}, "
          f"q_vib harmonic = {q_vib_harmonic(w0('I2'), T):.4f}, anharmonic = "
          f"{q_vib_anharmonic(d['we'], d['wexe'], T, D0_I2_CM):.4f}")
    print(f"  exp(-D0/kT) = {math.exp(-HC_K * D0_I2_CM / T):.4e}")

    print("\n  T/K    K harmonic   K anharmonic   K JANAF      anh/JANAF   alpha(1 bar)")
    for T, row in sorted(jan.items()):
        kh = k_dissociation(T, "harmonic")
        ka = k_dissociation(T, "anharmonic")
        kj = 10 ** (2 * row["logKf"])
        print(f"  {T:5.0f}  {kh:11.4e}  {ka:12.4e}  {kj:11.4e}   {ka / kj:8.3f}    {degree_of_dissociation(ka, 1.0):.4f}")

    T = 1000.0
    dh, ds = reaction_h_s(T)
    jan_dh = 2 * 76.937 - 0.0
    jan_ds = 2 * 205.942 - 306.087
    print(f"\nAt {T:.0f} K: Delta_r H = {dh:.2f} kJ/mol (JANAF {jan_dh:.2f}), "
          f"Delta_r S = {ds:.2f} J/(mol K) (JANAF {jan_ds:.2f})")
    print(f"  check: exp(-(dH - T dS)/RT) = {math.exp(-(dh * 1000 - T * ds) / (R * T)):.4e}")

    print("\nSensitivity: D0 raised by 1 % (124 cm-1):")
    for T in (800.0, 1000.0, 1500.0):
        r = k_dissociation(T, "anharmonic", 1.01 * D0_I2_CM) / k_dissociation(T, "anharmonic")
        print(f"  {T:5.0f} K: K falls to {r:.3f} of its value")

    print("\nDegree of dissociation at 1000 K vs pressure:")
    ka = k_dissociation(1000.0, "anharmonic")
    for p in (0.01, 0.1, 1.0, 10.0):
        print(f"  p = {p:5.2f} bar: alpha = {degree_of_dissociation(ka, p):.4f}")

    ts = np.linspace(500, 1500, 60)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(1000 / ts, [math.log(k_dissociation(t, "anharmonic")) for t in ts], label="from partition functions")
    ax.plot([1000 / t for t in jan], [2 * r["logKf"] * math.log(10) for r in jan.values()], "o", label="NIST-JANAF")
    ax.set_xlabel("1000 K / T")
    ax.set_ylabel("ln K")
    ax.set_title("I2(g) = 2 I(g)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(RUNS / "lesson04_vant_hoff.png", dpi=120)
    print(f"\nPlot written to {RUNS / 'lesson04_vant_hoff.png'}")


if __name__ == "__main__":
    main()
