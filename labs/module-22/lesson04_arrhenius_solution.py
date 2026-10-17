"""Lesson 22.4 - reference solution. Arrhenius and Eyring analysis of real evaluated rate constants.

Run:  py lesson04_arrhenius_solution.py      Writes runs/lesson04_arrhenius.png.
Optional: put your effervescent-tablet times in tablet_times.csv (same columns as
tablet_times_template.csv) and the script fits them too.
"""
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from kin22 import H, HERE, K_B, N2O5_KINF, R, k_mod_arrhenius, read_csv, runs_dir


def arrhenius_fit(T, k):
    """Fit ln k = ln A - Ea/(R T). Returns Ea (J/mol), A, and their standard uncertainties."""
    (slope, intercept), cov = np.polyfit(1.0 / T, np.log(k), 1, cov=True)
    Ea, lnA = -slope * R, intercept
    sEa, slnA = math.sqrt(cov[0, 0]) * R, math.sqrt(cov[1, 1])
    return Ea, math.exp(lnA), sEa, math.exp(lnA) * slnA


def eyring_fit(T, k):
    """Fit ln(k/T) = ln(kB/h) + dS/R - dH/(R T) for a first-order k. Returns dH (J/mol), dS (J/(mol K))."""
    slope, intercept = np.polyfit(1.0 / T, np.log(k / T), 1)
    return -slope * R, (intercept - math.log(K_B / H)) * R


def local_ea(T, k):
    """Apparent activation energy from neighbouring points: Ea = -R d(ln k)/d(1/T)."""
    return -R * np.diff(np.log(k)) / np.diff(1.0 / T)


def main():
    rows = read_csv("oh_ch4_k.csv")
    T = np.array([float(r["T_K"]) for r in rows])
    k = np.array([float(r["k_cm3_molecule_s"]) for r in rows])
    study = np.array([r["study"] for r in rows])

    for name, (lo, hi) in (("196-300 K", (190, 301)), ("300-420 K", (299, 421)), ("840-2000 K", (800, 2100))):
        m = (T >= lo) & (T <= hi)
        Ea, A, sEa, sA = arrhenius_fit(T[m], k[m])
        print(f"OH + CH4 {name:11s}: Ea = {Ea / 1000:5.1f} +/- {sEa / 1000:.1f} kJ/mol, A = {A:.2e} cm3 molecule-1 s-1")
    Tm = np.sqrt(T[:-1] * T[1:])
    ea = local_ea(T, k)
    print("  local Ea at", ", ".join(f"{a:.0f} K: {b / 1000:.1f}" for a, b in zip(Tm[::3], ea[::3])), "kJ/mol")

    TN = np.arange(200.0, 301.0, 10.0)
    kN = np.array([k_mod_arrhenius(N2O5_KINF, t) for t in TN])
    Ea, A, _, _ = arrhenius_fit(TN, kN)
    dH, dS = eyring_fit(TN, kN)
    print(f"N2O5 -> NO2 + NO3 (k_inf, 200-300 K): Ea = {Ea / 1000:.1f} kJ/mol, A = {A:.2e} s-1")
    print(f"  Eyring: dH = {dH / 1000:.1f} kJ/mol (Ea - RT at 250 K = {(Ea - R * 250) / 1000:.1f}), dS = {dS:+.0f} J mol-1 K-1")

    user = HERE / "tablet_times.csv"
    if user.exists():
        tab = read_csv("tablet_times.csv")
        if len(tab) >= 2:
            Tt = np.array([float(r["water_temp_C"]) for r in tab]) + 273.15
            rate = 1.0 / np.array([float(r["dissolve_time_s"]) for r in tab])
            Ea_t, _, sEa_t, _ = arrhenius_fit(Tt, rate)
            print(f"Your tablet: apparent Ea = {Ea_t / 1000:.0f} +/- {sEa_t / 1000:.0f} kJ/mol from {len(tab)} runs")
    else:
        print("No tablet_times.csv yet: copy tablet_times_template.csv, add your runs and rerun.")

    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    for s in np.unique(study):
        m = study == s
        ax[0].semilogy(1000 / T[m], k[m], "o", label=s)
    m = T < 301
    Ea, A, _, _ = arrhenius_fit(T[m], k[m])
    x = np.linspace(0.4, 5.2, 100)
    ax[0].semilogy(x, A * np.exp(-Ea / (R * 1000 / x)), "k--", label="Arrhenius fit 196-300 K")
    ax[0].set_xlabel("1000 K / T"); ax[0].set_ylabel("k / cm$^3$ molecule$^{-1}$ s$^{-1}$"); ax[0].legend()
    ax[1].plot(1000 / TN, np.log(kN / TN), "o")
    ax[1].set_xlabel("1000 K / T"); ax[1].set_ylabel("ln(k/T) for N$_2$O$_5$ (Eyring plot)")
    fig.tight_layout(); fig.savefig(runs_dir() / "lesson04_arrhenius.png", dpi=120)
    print("saved runs/lesson04_arrhenius.png")


if __name__ == "__main__":
    main()
