"""Lesson 29.1 - exercise: protein stability from a thermal melt and a urea melt.

Fill in the functions marked TODO, then run:  py lesson01_stability.py
Reference solution: lesson01_stability_solution.py
Writes runs/lesson01_stability.png.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq, curve_fit

from enz29 import R, T25, T37, column, dG_unfold, read_csv, runs_dir

DCP = 6000.0   # J/(mol K), assumed: about 60 J/(mol K) per residue for a ~100-residue protein


def thermal_model(T, Tm, dHm, aN, bN, aU, bU):
    """CD signal of a two-state thermal melt with sloping baselines. T in K, dHm in J/mol."""
    # TODO: dG = dG_unfold(T, Tm, dHm, DCP)
    # TODO: fU = 1.0 / (1.0 + np.exp(dG / (R * T)))
    # TODO: yN = aN + bN * (T - T25)
    # TODO: yU = aU + bU * (T - T25)
    # TODO: return yN + (yU - yN) * fU
    raise NotImplementedError("TODO: write thermal_model() first (see the hints in the code).")


def urea_model(D, dG0, m, aN, bN, aU, bU):
    """CD signal of a urea melt at 25 C: dG = dG0 - m [urea] (linear extrapolation method)."""
    # TODO: dG = dG0 - m * D
    # TODO: fU = 1.0 / (1.0 + np.exp(dG / (R * T25)))
    # TODO: return (aN + bN * D) + ((aU + bU * D) - (aN + bN * D)) * fU
    raise NotImplementedError("TODO: write urea_model() first (see the hints in the code).")


def fit_thermal(T, y):
    p0 = (T[np.argmin(np.abs(y - (y.min() + y.max()) / 2))], 300e3, y[0], 0.0, y[-1], 0.0)
    popt, pcov = curve_fit(thermal_model, T, y, p0=p0, maxfev=20000)
    return popt, np.sqrt(np.diag(pcov))


def fit_urea(D, y):
    popt, pcov = curve_fit(urea_model, D, y, p0=(20e3, 5e3, y[0], 0.0, y[-1], 0.0), maxfev=20000)
    return popt, np.sqrt(np.diag(pcov))


def fraction_unfolded(dG, T):
    # TODO: return 1.0 / (1.0 + np.exp(dG / (R * T)))
    raise NotImplementedError("TODO: write fraction_unfolded() first (see the hints in the code).")


def main():
    th = read_csv("protein_thermal_melt.csv")
    T = column(th, "T_C") + 273.15
    yT = column(th, "cd222_mdeg")
    (Tm, dHm, *_), (sTm, sdH, *_) = fit_thermal(T, yT)
    print(f"Thermal melt: Tm = {Tm - 273.15:.2f} +/- {sTm:.2f} C, dHm = {dHm / 1000:.0f} +/- {sdH / 1000:.0f} kJ/mol"
          f" (dCp fixed at {DCP / 1000:.1f} kJ/(mol K))")
    dG25_T = dG_unfold(T25, Tm, dHm, DCP)
    dG37_T = dG_unfold(T37, Tm, dHm, DCP)
    print(f"  extrapolated dG(25 C) = {dG25_T / 1000:.1f} kJ/mol, dG(37 C) = {dG37_T / 1000:.1f} kJ/mol")
    print(f"  fraction unfolded at 37 C = {fraction_unfolded(dG37_T, T37):.1e}")

    ur = read_csv("protein_urea_melt.csv")
    D = column(ur, "urea_M")
    yD = column(ur, "cd222_mdeg")
    (dG0, m, *_), (sdG0, sm, *_) = fit_urea(D, yD)
    print(f"Urea melt (25 C): dG(H2O) = {dG0 / 1000:.1f} +/- {sdG0 / 1000:.1f} kJ/mol, "
          f"m = {m / 1000:.2f} +/- {sm / 1000:.2f} kJ/(mol M), Cm = {dG0 / m:.2f} M")
    print(f"  a mutation that lowers Cm by 0.50 M costs ddG = m x 0.50 = {m * 0.5 / 1000:.1f} kJ/mol")

    Ts = Tm * np.exp(-dHm / (Tm * DCP))
    Tc = brentq(lambda x: dG_unfold(x, Tm, dHm, DCP), 150.0, Ts)
    print(f"Stability curve: maximum stability at {Ts - 273.15:.1f} C "
          f"(dG = {dG_unfold(Ts, Tm, dHm, DCP) / 1000:.1f} kJ/mol); cold denaturation predicted at {Tc - 273.15:.0f} C")

    fig, ax = plt.subplots(1, 3, figsize=(14, 4))
    TT = np.linspace(T.min(), T.max(), 300)
    ax[0].plot(T - 273.15, yT, "o", ms=3, label="data (generated)")
    ax[0].plot(TT - 273.15, thermal_model(TT, *fit_thermal(T, yT)[0]), "-", label=f"fit, Tm = {Tm - 273.15:.1f} C")
    ax[0].set_xlabel("T / C"); ax[0].set_ylabel("CD at 222 nm / mdeg"); ax[0].legend()
    DD = np.linspace(0, D.max(), 300)
    ax[1].plot(D, yD, "o", ms=3, label="data (generated)")
    ax[1].plot(DD, urea_model(DD, *fit_urea(D, yD)[0]), "-", label=f"fit, Cm = {dG0 / m:.2f} M")
    ax[1].set_xlabel("[urea] / M"); ax[1].set_ylabel("CD at 222 nm / mdeg"); ax[1].legend()
    Tc_plot = np.linspace(Tc - 10, Tm + 15, 300)
    ax[2].plot(Tc_plot - 273.15, dG_unfold(Tc_plot, Tm, dHm, DCP) / 1000, "-")
    ax[2].axhline(0, c="k", lw=0.5)
    ax[2].plot([25], [dG0 / 1000], "s", label="urea melt at 25 C")
    ax[2].set_xlabel("T / C"); ax[2].set_ylabel("dG unfolding / kJ/mol"); ax[2].legend()
    ax[2].set_title("stability curve from the thermal fit", fontsize=9)
    fig.tight_layout(); fig.savefig(runs_dir() / "lesson01_stability.png", dpi=120)
    print("saved runs/lesson01_stability.png")


if __name__ == "__main__":
    try:
        main()
    except NotImplementedError as e:
        print(e)
