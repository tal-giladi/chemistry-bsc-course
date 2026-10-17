"""Lesson 13.5 hands-on: phase diagrams of water and CO2 from NIST data.

Fill in the functions marked TODO, then run this file. Reference solution: lesson05_phase_diagram_solution.py.

    py lesson05_phase_diagram.py

Data: phase_data.csv (triple and critical points, transition enthalpies) and antoine.csv
(NIST WebBook Antoine coefficients, log10(p/bar) = A - B/(T/K + C)).
Edit P_HOME_BAR with your own station pressure for the boiling-point prediction.
Writes runs/lesson05_phase_diagrams.png.
"""
import csv
import math
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
R = 8.314462618

P_HOME_BAR = 0.920        # your station pressure (bar); 0.92 is typical for Jerusalem, about 800 m


def load_phase():
    d = {}
    with open(HERE / "phase_data.csv", newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            d[(r["substance"], r["quantity"])] = float(r["value"])
    return d


def load_antoine():
    rows = []
    with open(HERE / "antoine.csv", newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            rows.append({k: (float(v) if k not in ("substance", "reference") else v) for k, v in r.items()})
    return rows


PH = load_phase()
ANT = load_antoine()


def antoine_p(substance, t):
    """Vapour (or sublimation) pressure in bar from the NIST Antoine fit covering t, else None."""
    for r in ANT:
        if r["substance"] == substance and r["Tmin_K"] - 0.5 <= t <= r["Tmax_K"] + 0.5:
            return 10 ** (r["A"] - r["B"] / (t + r["C"]))
    return None


def clausius_clapeyron_p(p1, t1, dh_kj, t):
    """p at t from a known point (p1, t1) with constant transition enthalpy (kJ/mol)."""
    # TODO: one line with math.exp; convert kJ to J
    return None


def clapeyron_slope(dh_kj, t, dv_cm3):
    """dp/dT in bar/K = Delta H / (T Delta V), with Delta V in cm3/mol."""
    # TODO: one line; convert cm3 to m3 and Pa to bar
    return None


BOIL = (5.08354, 1663.125, -45.622)   # NIST Antoine set for water fitted at 344-373 K


def boiling_point(p_bar):
    """Temperature (K) at which water's vapour pressure equals p_bar, solving the 344-373 K
    Antoine equation (log10 p = A - B/(T + C)) with brentq between 340 and 380 K
    (a few kelvin of extrapolation above 373 K is acceptable for this fit)."""
    # TODO: a, b, c = BOIL; solve 10 ** (a - b / (t + c)) = p_bar with brentq between 340 and 380 K
    return None


def _missing():
    """Names of the exercise functions that still return None (TODO)."""
    tests = {
        "clausius_clapeyron_p": lambda: clausius_clapeyron_p(1.0, 373.15, 40.67, 363.15),
        "clapeyron_slope": lambda: clapeyron_slope(6.01, 273.15, -1.63),
        "boiling_point": lambda: boiling_point(1.01325),
    }
    return [name for name, f in tests.items() if f() is None]


def main():
    missing = _missing()
    if missing:
        print("TODO: write " + ", ".join(f"{m}()" for m in missing) + " first (see the lesson).")
        return
    print("Water")
    tt, pt = PH[("H2O", "T_triple")], PH[("H2O", "p_triple")]
    dv = PH[("H2O", "Vm_liquid_273")] - PH[("H2O", "Vm_ice_273")]
    slope = clapeyron_slope(PH[("H2O", "dH_fus")], tt, dv)
    print(f"  melting line slope (Clapeyron) = {slope:.0f} bar/K ({1000 / slope:.2f} mK per bar)")
    print(f"  Antoine p(373.15 K) = {antoine_p('H2O', 373.15):.4f} bar (1 atm = 1.01325 bar)")
    print(f"  Antoine p(273.16 K) = {antoine_p('H2O', 273.16) * 1e5:.0f} Pa (triple point 611.657 Pa)")
    dh_vap_cc = -R * math.log(antoine_p("H2O", 363.15) / antoine_p("H2O", 343.15)) / (1 / 363.15 - 1 / 343.15) / 1000
    print(f"  Delta_vap H from the Antoine slope at 343-363 K = {dh_vap_cc:.1f} kJ/mol")
    print("  boiling point of water against pressure:")
    for label, p in (("Dead Sea shore, about -430 m", 1.06), ("sea level", 1.01325),
                     ("Jerusalem, about 800 m", 0.92), ("your station", P_HOME_BAR)):
        tb = boiling_point(p)
        tb_cc = 1 / (1 / 373.124 - R * math.log(p / 1.01325) / (PH[("H2O", "dH_vap_373")] * 1000))
        print(f"    {label:<30} p = {p:.3f} bar: Antoine {tb - 273.15:6.2f} C, Clausius-Clapeyron {tb_cc - 273.15:6.2f} C")

    print("\nCO2")
    tt2, pt2 = PH[("CO2", "T_triple")], PH[("CO2", "p_triple")]
    tc2, pc2 = PH[("CO2", "T_crit")], PH[("CO2", "p_crit")]
    p_sub = clausius_clapeyron_p(pt2, tt2, PH[("CO2", "dH_sub_207")], 194.65)
    print(f"  sublimation p at 194.65 K (-78.5 C): Clausius-Clapeyron from triple point {p_sub:.3f} bar,"
          f" Antoine {antoine_p('CO2', 194.65):.3f} bar")
    dh_vap_co2 = R * math.log(pc2 / pt2) / (1 / tt2 - 1 / tc2) / 1000
    print(f"  average Delta_vap H implied by triple and critical points = {dh_vap_co2:.1f} kJ/mol (NIST lists 16.4-16.7)")
    rbar = 0.08314462618
    print(f"  van der Waals from Tc, pc: a = {27 * rbar**2 * tc2**2 / (64 * pc2):.3f} L2 bar/mol2,"
          f" b = {rbar * tc2 / (8 * pc2):.4f} L/mol")
    print(f"  at 1 atm CO2 is solid or gas only: triple-point pressure {pt2} bar > 1.013 bar")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    t_l = np.linspace(273.16, 573, 300)
    p_l = [antoine_p("H2O", t) or np.nan for t in t_l]
    t_cc = np.linspace(573, PH[("H2O", "T_crit")], 50)
    p573 = antoine_p("H2O", 573)
    dh_hi = R * math.log(PH[("H2O", "p_crit")] / p573) / (1 / 573 - 1 / PH[("H2O", "T_crit")]) / 1000
    ax1.semilogy(t_l, p_l, label="liquid-vapour (NIST Antoine)")
    ax1.semilogy(t_cc, [clausius_clapeyron_p(p573, 573, dh_hi, t) for t in t_cc], ":", label="to critical point (C-C)")
    t_s = np.linspace(230, tt, 50)
    dh_sub = PH[("H2O", "dH_fus")] + 45.05          # Delta_sub H = Delta_fus H + Delta_vap H near 273 K
    ax1.semilogy(t_s, [clausius_clapeyron_p(pt, tt, dh_sub, t) for t in t_s], label="solid-vapour (C-C)")
    p_m = np.logspace(math.log10(pt), 3, 50)
    ax1.semilogy(tt + (p_m - pt) / slope, p_m, label="solid-liquid (Clapeyron)")
    ax1.plot([tt], [pt], "ko")
    ax1.plot([PH[("H2O", "T_crit")]], [PH[("H2O", "p_crit")]], "k^")
    ax1.set_title("H2O")
    ax1.set_xlabel("T (K)")
    ax1.set_ylabel("p (bar)")
    ax1.legend(fontsize=7)
    t_s2 = np.linspace(160, tt2, 50)
    ax2.semilogy(t_s2, [clausius_clapeyron_p(pt2, tt2, PH[("CO2", "dH_sub_207")], t) for t in t_s2], label="solid-vapour (C-C)")
    t_a = np.linspace(155, 195.8, 30)
    ax2.semilogy(t_a, [antoine_p("CO2", t) for t in t_a], "--", label="solid-vapour (NIST Antoine)")
    t_v = np.linspace(tt2, tc2, 50)
    ax2.semilogy(t_v, [clausius_clapeyron_p(pt2, tt2, dh_vap_co2, t) for t in t_v], label="liquid-vapour (C-C)")
    ax2.plot([tt2], [pt2], "ko")
    ax2.plot([tc2], [pc2], "k^")
    ax2.axhline(1.01325, color="grey", lw=0.8)
    ax2.text(165, 1.15, "1 atm", fontsize=8)
    ax2.set_title("CO2 (melting line steep and positive, not drawn)")
    ax2.set_xlabel("T (K)")
    ax2.legend(fontsize=7)
    out = HERE / "runs"
    out.mkdir(exist_ok=True)
    fig.tight_layout()
    fig.savefig(out / "lesson05_phase_diagrams.png", dpi=120)
    print(f"\nplot written to {out / 'lesson05_phase_diagrams.png'}")


if __name__ == "__main__":
    main()
