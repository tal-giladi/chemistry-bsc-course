"""Lesson 13.1 reference solution: p-V work from a sealed syringe pressed on a kitchen scale.

    py lesson01_work_solution.py                 # example data
    py lesson01_work_solution.py my_syringe.csv  # your data: direction,V_mL,scale_g

Edit the setup block for your syringe (length of the 0-10 mL scale) and room pressure.
Writes runs/lesson01_pV.png.
"""
import csv
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
G = 9.80665                 # m/s^2, standard gravity

# ---- setup: your syringe and your room ----
SCALE_LENGTH_MM = 60.6      # ruler length of the 0 -> 10 mL graduations
SCALE_VOLUME_ML = 10.0
DEAD_ML = 0.15              # air in the nozzle below the 0 mark (estimate: about 0.1-0.2 mL)
P_ATM = 100_800.0           # Pa, from a phone barometer or a nearby weather station


def area_m2(length_mm=SCALE_LENGTH_MM, volume_ml=SCALE_VOLUME_ML):
    return volume_ml * 1e-6 / (length_mm / 1000)


def pressure_from_scale(grams, area, p_atm):
    """Absolute gas pressure (Pa): room pressure plus the scale force divided by the area."""
    return p_atm + grams / 1000 * G / area


def work_on_gas_trapezoid(v_m3, p_pa):
    """w = -integral p dV along the measured path, by the trapezoid rule (J).
    Positive when the gas is compressed (work done ON the gas, IUPAC sign)."""
    return float(-np.trapezoid(p_pa, v_m3))


def work_isothermal_reversible(p1, v1, v2):
    """Reversible isothermal ideal gas: w = -nRT ln(V2/V1) = -p1 V1 ln(V2/V1) (J)."""
    return -p1 * v1 * math.log(v2 / v1)


def _missing():
    """Names of the exercise functions that still return None (TODO)."""
    tests = {
        "pressure_from_scale": lambda: pressure_from_scale(100, 1e-4, 1e5),
        "work_on_gas_trapezoid": lambda: work_on_gas_trapezoid(np.array([2.0, 1.0]), np.array([1.0, 2.0])),
        "work_isothermal_reversible": lambda: work_isothermal_reversible(1e5, 1e-5, 5e-6),
    }
    return [name for name, f in tests.items() if f() is None]


def read(path):
    rows = {"in": [], "out": []}
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            rows[r["direction"]].append((float(r["V_mL"]), float(r["scale_g"])))
    return rows


def main():
    missing = _missing()
    if missing:
        print("TODO: write " + ", ".join(f"{m}()" for m in missing) + " first (see the lesson).")
        return
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "syringe_example.csv"
    rows = read(path)
    area = area_m2()
    print(f"barrel area A = {area * 1e4:.3f} cm^2")
    vols = sorted({v for v, _ in rows["in"]}, reverse=True)
    g_in = dict(rows["in"])
    g_out = dict(rows["out"])
    print(f"{'V mL':>6}{'in g':>8}{'out g':>8}{'mean g':>8}{'p kPa':>9}{'pV J':>8}")
    v_m3, p_pa = [], []
    for v in vols:
        g_mean = (g_in[v] + g_out[v]) / 2           # averaging in and out cancels friction
        p = pressure_from_scale(g_mean, area, P_ATM)
        v_tot = (v + DEAD_ML) * 1e-6
        v_m3.append(v_tot)
        p_pa.append(p)
        print(f"{v:6.1f}{g_in[v]:8.0f}{g_out[v]:8.0f}{g_mean:8.0f}{p / 1000:9.1f}{p * v_tot:8.4f}")
    v_m3, p_pa = np.array(v_m3), np.array(p_pa)
    pv = p_pa * v_m3
    print(f"pV mean {pv.mean():.4f} J, spread {100 * pv.std(ddof=1) / pv.mean():.1f} % (Boyle: constant)")
    friction = np.mean([(g_in[v] - g_out[v]) / 2 for v in vols if v != vols[0]]) / 1000 * G
    print(f"plunger friction from the in/out difference: about {friction:.1f} N")

    w_meas = work_on_gas_trapezoid(v_m3, p_pa)
    w_rev = work_isothermal_reversible(p_pa[0], v_m3[0], v_m3[-1])
    w_atm = P_ATM * (v_m3[0] - v_m3[-1])
    w_one_step = p_pa[-1] * (v_m3[0] - v_m3[-1])
    print(f"\nwork done on the gas, measured (trapezoid):  {w_meas:.3f} J")
    print(f"reversible isothermal, p1 V1 ln(V1/V2):      {w_rev:.3f} J")
    print(f"  of which the atmosphere pushed:            {w_atm:.3f} J")
    print(f"  and your hand pushed:                      {w_meas - w_atm:.3f} J")
    print(f"one-step compression against final p:        {w_one_step:.3f} J (irreversible, more work)")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return
    vv = np.linspace(v_m3[-1], v_m3[0], 100)
    fig, ax = plt.subplots(figsize=(5.5, 4))
    ax.fill_between(v_m3 * 1e6, p_pa / 1000, alpha=0.2, label="area = work on gas")
    ax.plot(v_m3 * 1e6, p_pa / 1000, "o", label="measured (mean of in/out)")
    ax.plot(vv * 1e6, p_pa[0] * v_m3[0] / vv / 1000, "-", label="Boyle isotherm")
    ax.set_xlabel("V (mL)")
    ax.set_ylabel("p (kPa)")
    ax.set_ylim(0, None)
    ax.legend()
    out = HERE / "runs"
    out.mkdir(exist_ok=True)
    fig.tight_layout()
    fig.savefig(out / "lesson01_pV.png", dpi=120)
    print(f"plot written to {out / 'lesson01_pV.png'}")


if __name__ == "__main__":
    main()
