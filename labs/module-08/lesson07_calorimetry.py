"""Lesson 08.7 module practical: coffee-cup calorimetry of baking soda.

Fill in the two TODO functions, then run:
       py lesson07_calorimetry.py                    (uses calorimetry_example.csv)
       py lesson07_calorimetry.py my_calorimetry.csv (columns run,t_s,T_C; runs named
                                                               'calibration' and 'dissolution')
Reference solution: lesson07_calorimetry_solution.py
Edit the SETUP block to your own masses and times.
Steps: (1) fit straight lines to the readings before and after mixing and extrapolate both to the
mixing time; (2) the calibration run gives the heat capacity of the cup; (3) the dissolution run
gives Delta_sol H of NaHCO3 with an uncertainty, propagated numerically.
Writes runs/lesson07_calorimetry.png.
"""
import csv
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
C_WATER = 4.184        # J/(g K)
C_SALT = 1.0           # J/(g K), approximate specific heat of solid NaHCO3
M_NAHCO3 = 84.006      # g/mol
DH_TABLE = 19.6        # kJ/mol, from formation enthalpies at infinite dilution (lesson 08.1)

# SETUP: value and standard uncertainty for each quantity you measured
SETUP = {
    "calibration": {"t_mix": 180, "pre_until": 150, "post_from": 270,
                    "m_cold": (100.0, 0.1), "m_hot": (50.0, 0.1), "T_hot": (45.0, 0.3)},
    "dissolution": {"t_mix": 180, "pre_until": 150, "post_from": 300,
                    "m_water": (100.0, 0.1), "m_salt": (5.00, 0.01)},
}
T_RESOLUTION = 0.1     # thermometer resolution, C (adds 0.1/sqrt(12) to each extrapolated value)


def read_runs(path):
    runs = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            runs.setdefault(row["run"], []).append((float(row["t_s"]), float(row["T_C"])))
    return {k: np.array(v) for k, v in runs.items()}


def extrapolate(t, temp, t_at):
    """Fit temp = a + b t by least squares; return the value at t_at and its standard uncertainty."""
    (b, a), cov = np.polyfit(t, temp, 1, cov=True)
    value = a + b * t_at
    var = cov[1, 1] + t_at ** 2 * cov[0, 0] + 2 * t_at * cov[0, 1]
    return value, float(np.sqrt(var + (T_RESOLUTION / np.sqrt(12)) ** 2))


def jumps(data, cfg):
    t, temp = data[:, 0], data[:, 1]
    pre = t <= cfg["pre_until"]
    post = t >= cfg["post_from"]
    t_before = extrapolate(t[pre], temp[pre], cfg["t_mix"])
    t_after = extrapolate(t[post], temp[post], cfg["t_mix"])
    return t_before, t_after


def propagate(f, values):
    """Value of f and its standard uncertainty for independent inputs {name: (value, sigma)},
    by numerical partial derivatives: sigma_f^2 = sum (df/dx_i * sigma_i)^2."""
    x0 = {k: v for k, (v, _) in values.items()}
    f0 = f(**x0)
    var = 0.0
    for k, (v, s) in values.items():
        if s == 0:
            continue
        h = s * 1e-3
        dfdx = (f(**{**x0, k: v + h}) - f(**{**x0, k: v - h})) / (2 * h)
        var += (dfdx * s) ** 2
    return f0, float(np.sqrt(var))


def cup_heat_capacity(m_cold, m_hot, T_hot, T_cold, T_final):
    """Heat lost by hot water = heat gained by cold water and cup:
    m_hot c (T_hot - T_final) = (m_cold c + C_cup) (T_final - T_cold). Solve for C_cup (J/K).
    TODO: one line."""
    return None


def dissolution_enthalpy(m_water, m_salt, C_cup, T_before, T_after):
    """Delta_sol H in kJ/mol: the salt absorbs the heat the water, cup and salt lose.
    TODO: q_absorbed = (total heat capacity of water + cup + salt) x (T_before - T_after) in J;
    divide by the moles of NaHCO3 and by 1000."""
    return None


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "calorimetry_example.csv"
    runs = read_runs(path)
    if cup_heat_capacity(1, 1, 1, 0, 0.5) is None or dissolution_enthalpy(1, 1, 0, 1, 0) is None:
        print("TODO: write cup_heat_capacity() and dissolution_enthalpy() first.")
        return

    cal = SETUP["calibration"]
    tc, tf = jumps(runs["calibration"], cal)
    print(f"calibration: T_cold = {tc[0]:.2f} +/- {tc[1]:.2f} C, T_final = {tf[0]:.2f} +/- {tf[1]:.2f} C")
    c_cup = propagate(cup_heat_capacity, {"m_cold": cal["m_cold"], "m_hot": cal["m_hot"],
                                          "T_hot": cal["T_hot"], "T_cold": tc, "T_final": tf})
    print(f"  cup heat capacity C_cup = {c_cup[0]:.0f} +/- {c_cup[1]:.0f} J/K "
          f"(the water alone is {cal['m_cold'][0] * C_WATER:.0f} J/K)")

    dis = SETUP["dissolution"]
    tb, ta = jumps(runs["dissolution"], dis)
    print(f"dissolution: T_before = {tb[0]:.2f} +/- {tb[1]:.2f} C, T_after = {ta[0]:.2f} +/- {ta[1]:.2f} C, "
          f"Delta T = {ta[0] - tb[0]:.2f} K")
    dh = propagate(dissolution_enthalpy, {"m_water": dis["m_water"], "m_salt": dis["m_salt"],
                                          "C_cup": c_cup, "T_before": tb, "T_after": ta})
    print(f"  Delta_sol H(NaHCO3) = {dh[0]:.1f} +/- {dh[1]:.1f} kJ/mol "
          f"(table, infinite dilution: +{DH_TABLE} kJ/mol)")
    no_cup = dissolution_enthalpy(dis["m_water"][0], dis["m_salt"][0], 0.0, tb[0], ta[0])
    print(f"  ignoring the cup would give {no_cup:.1f} kJ/mol")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed: skipping the plot")
        return
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.6))
    for ax, name in zip(axes, ("calibration", "dissolution")):
        cfg, d = SETUP[name], runs[name]
        ax.plot(d[:, 0], d[:, 1], "o", ms=4)
        for mask in (d[:, 0] <= cfg["pre_until"], d[:, 0] >= cfg["post_from"]):
            b, a = np.polyfit(d[mask, 0], d[mask, 1], 1)
            tt = np.array([d[mask, 0].min(), d[mask, 0].max(), cfg["t_mix"]])
            tt.sort()
            ax.plot(tt, a + b * tt, "--")
        ax.axvline(cfg["t_mix"], color="grey", lw=0.8)
        ax.set_title(name)
        ax.set_xlabel("t (s)")
        ax.set_ylabel("T (C)")
    out = HERE / "runs"
    out.mkdir(exist_ok=True)
    fig.tight_layout()
    fig.savefig(out / "lesson07_calorimetry.png", dpi=120)
    print(f"\nplot written to {out / 'lesson07_calorimetry.png'}")


if __name__ == "__main__":
    main()
