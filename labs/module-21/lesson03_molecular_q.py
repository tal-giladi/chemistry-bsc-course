"""Lesson 21.3 exercise: molecular partition functions and standard entropies.

Fill in the functions marked TODO, then run this file. Reference solution: lesson03_molecular_q_solution.py.

Run from this folder:  py lesson03_molecular_q.py

Builds q_trans, q_rot and q_vib from NIST constants, then computes S°(298.15 K) and Cp of seven gases
and compares them with the CODATA / NIST-JANAF values. Writes runs/lesson03_entropy_terms.png.
"""
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from stat21 import (H, K_B, N_A, P_STD, HC_K, R, MOLAR_MASS, DIATOMIC, ATOM_LEVELS,
                    q_elec, q_rot_sum, w0, B0, thermo_from_lnq)

RUNS = Path(__file__).resolve().parent / "runs"
T0 = 298.15

# S°(298.15 K, 1 bar) in J/(mol K): CODATA Key Values (Cox, Wagman and Medvedev 1984) as listed in the
# NIST Chemistry WebBook, except I2(g) and I(g) from the NIST-JANAF tables (I-027, I-001) and Cl(g) (Cl-001).
S_NIST = {"Ar": 154.846, "N2": 191.609, "CO": 197.660, "HCl": 186.902, "O2": 205.152,
          "I2": 260.685, "I": 180.786, "Cl": 165.189}


# ---------------- TODO 1 ----------------
def q_trans_std(molar_mass, T):
    """Standard translational partition function per molecule, (kT/p°) / Lambda^3, molar mass in g/mol."""
    # TODO: mass per molecule m = molar_mass / 1000 / N_A; Lambda = H / sqrt(2 pi m K_B T); return K_B T / P_STD / Lambda**3
    return None


# ---------------- TODO 2 ----------------
def q_rot_high_t(B, T, sigma):
    """High-temperature rotational partition function of a linear molecule, kT / (sigma h c B)."""
    # TODO: one line: T / (sigma * HC_K * B)
    return None


# ---------------- TODO 3 ----------------
def q_vib_harmonic(nu, T):
    """Harmonic vibrational partition function with v = 0 as zero of energy, nu in cm^-1."""
    # TODO: one line: 1 / (1 - exp(-HC_K * nu / T))
    return None


def missing():
    """Names of the exercise functions that still return None (TODO)."""
    tests = {"q_trans_std": lambda: q_trans_std(28.0, 298.15),
             "q_rot_high_t": lambda: q_rot_high_t(2.0, 298.15, 2),
             "q_vib_harmonic": lambda: q_vib_harmonic(2000.0, 298.15)}
    return [name for name, f in tests.items() if f() is None]


def ln_q(name, T, exact_rot=False):
    """ln(q°/N_A) of an atom or a diatomic from your functions."""
    lq = math.log(q_trans_std(MOLAR_MASS[name], T))
    if name in ATOM_LEVELS:
        return lq + math.log(q_elec(ATOM_LEVELS[name], T))
    d = DIATOMIC[name]
    qr = q_rot_sum(B0(name), T, d["sigma"]) if exact_rot else q_rot_high_t(B0(name), T, d["sigma"])
    return lq + math.log(qr) + math.log(q_vib_harmonic(w0(name), T)) + math.log(d["g_el"])


def entropy_terms(name, T):
    """Translational, rotational, vibrational and electronic entropy (J/(mol K)) from your functions."""
    s_tr = R * (math.log(q_trans_std(MOLAR_MASS[name], T)) + 2.5)
    if name in ATOM_LEVELS:
        lv = ATOM_LEVELS[name]
        q = q_elec(lv, T)
        e_mean = sum(e * g * math.exp(-HC_K * e / T) for e, g in lv) / q
        return s_tr, 0.0, 0.0, R * (math.log(q) + HC_K * e_mean / T)
    d = DIATOMIC[name]
    s_rot = R * (math.log(q_rot_high_t(B0(name), T, d["sigma"])) + 1)
    x = HC_K * w0(name) / T
    s_vib = R * (x / math.expm1(x) - math.log(-math.expm1(-x)))
    return s_tr, s_rot, s_vib, R * math.log(d["g_el"])


def main():
    if missing():
        print("TODO: write " + ", ".join(f"{m}()" for m in missing()) + " first (see lesson 21.3).")
        return
    RUNS.mkdir(exist_ok=True)

    lam = H / math.sqrt(2 * math.pi * MOLAR_MASS["N2"] / 1000 / N_A * K_B * T0)
    print(f"N2 at {T0} K: thermal wavelength {lam * 1e12:.2f} pm, q_trans/N_A at 1 bar = {q_trans_std(28.0134, T0):.3e}")
    for name in ("N2", "HCl", "I2"):
        d = DIATOMIC[name]
        print(f"{name}: theta_rot = {HC_K * B0(name):7.3f} K, q_rot high-T = "
              f"{q_rot_high_t(B0(name), T0, d['sigma']):8.2f}, exact sum = {q_rot_sum(B0(name), T0, d['sigma']):8.2f}; "
              f"theta_vib = {HC_K * w0(name):6.0f} K, q_vib = {q_vib_harmonic(w0(name), T0):.6f}")

    print(f"\nStandard entropy at {T0} K, J/(mol K)")
    print("species   S_trans   S_rot   S_vib    S_el    total   NIST     diff")
    names = ["Ar", "N2", "CO", "HCl", "O2", "I2", "I", "Cl"]
    rows = []
    for name in names:
        terms = entropy_terms(name, T0)
        tot = sum(terms)
        rows.append(terms)
        print(f"{name:7s} {terms[0]:8.2f} {terms[1]:7.2f} {terms[2]:7.2f} {terms[3]:7.2f} "
              f"{tot:8.2f} {S_NIST[name]:8.2f} {tot - S_NIST[name]:+7.2f}")

    print("\nSame entropies from ln q by numerical derivatives (exact rotational sum):")
    for name in names:
        t = thermo_from_lnq(lambda T: ln_q(name, T, exact_rot=True), T0)
        print(f"  {name:4s} S = {t['S']:8.3f}  Cp = {t['Cp']:6.3f}  H - H0 = {t['H_minus_H0']:6.3f} kJ/mol")

    fig, ax = plt.subplots(figsize=(8, 4))
    bottom = [0.0] * len(names)
    for k, label in enumerate(["translation", "rotation", "vibration", "electronic"]):
        vals = [r[k] for r in rows]
        ax.bar(names, vals, bottom=bottom, label=label)
        bottom = [b + v for b, v in zip(bottom, vals)]
    ax.plot(names, [S_NIST[n] for n in names], "k_", markersize=30, label="NIST")
    ax.set_ylabel("S° (298.15 K) / J mol$^{-1}$ K$^{-1}$")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(RUNS / "lesson03_entropy_terms.png", dpi=120)
    print(f"\nPlot written to {RUNS / 'lesson03_entropy_terms.png'}")


if __name__ == "__main__":
    main()
