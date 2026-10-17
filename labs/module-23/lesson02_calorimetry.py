"""Lesson 23.2 (exercise: fill in the TODO functions): coffee-cup calorimetry of citric acid + baking soda and of dissolving salts.

Run from this folder:
    py lesson02_calorimetry.py                      (uses calorimetry_example.csv)
    py lesson02_calorimetry.py my_calorimetry.csv   (columns run,t_s,T_C; runs named calibration,
                                                     reaction, nacl, epsom - leave out any you did not do)
Edit the SETUP block to your own masses and times. Steps: (1) extrapolate the before and after lines to
the mixing time; (2) the calibration gives the cup's heat capacity; (3) each run gives an enthalpy per mole
with a propagated uncertainty; (4) the reaction is corrected for the CO2 that stayed dissolved, found from
the mass loss, and compared with the Hess's-law prediction. Writes runs/lesson02_calorimetry.png.
"""
import sys
from pathlib import Path

import numpy as np

from pc23 import HERE, C_WATER, read_csv, extrapolate, propagate, todo, save_plot, pyplot

M = {"NaHCO3": 84.007, "citric": 192.12, "NaCl": 58.44, "epsom": 246.47, "CO2": 44.009}   # g/mol
C_SOLID = {"NaHCO3": 1.0, "NaCl": 0.86, "epsom": 1.5}      # J/(g K), approximate
DH_CO2_SOLN = -19.9        # kJ/mol, CO2(g) -> CO2(aq), from NIST WebBook Henry's law (2400 K)
T_RES = 0.1                # thermometer display step, C

# SETUP: (value, standard uncertainty). Times in s. "liquid" = mass of water or solution in the cup.
SETUP = {
    "calibration": {"t_mix": 180, "pre_until": 180, "post_from": 270,
                    "m_cold": (100.0, 0.1), "m_hot": (50.0, 0.1), "T_hot": (45.0, 0.3)},
    "reaction": {"t_mix": 180, "pre_until": 180, "post_from": 300, "solid": "NaHCO3",
                 "liquid": (104.0, 0.1), "m_solid": (3.00, 0.01), "mass_loss": (1.45, 0.02)},
    "nacl": {"t_mix": 180, "pre_until": 180, "post_from": 300, "solid": "NaCl",
             "liquid": (100.0, 0.1), "m_solid": (5.00, 0.01)},
    "epsom": {"t_mix": 180, "pre_until": 180, "post_from": 330, "solid": "epsom",
              "liquid": (100.0, 0.1), "m_solid": (10.00, 0.01)},
}
PREDICTED = {   # kJ/mol, from formation enthalpies (OpenStax App. G) and Goldberg 2002 for citric acid
    "reaction": 19.6 + 11.77 + 3.30,
    "nacl": 3.9,
    "epsom": 14.0,
}


def cup_heat_capacity(m_cold, m_hot, T_hot, T_cold, T_final):
    """m_hot c (T_hot - T_final) = (m_cold c + C_cup)(T_final - T_cold); return C_cup in J/K.
    TODO: one line."""
    return None  # TODO


def enthalpy_per_mol(liquid, m_solid, c_solid, molar_mass, C_cup, T_before, T_after):
    """Enthalpy change per mole of the added solid, kJ/mol. Positive when the cup cools.
    TODO: heat capacity of everything in the cup (liquid as water, solid, cup) times (T_before - T_after),
    divided by moles of solid and by 1000."""
    return None  # TODO


def all_gas_value(dH_obs, mass_loss, m_solid):
    """Correct the observed reaction enthalpy (per mol NaHCO3) to 'all CO2 escaped'.
    The fraction escaped is f = (mass_loss / M_CO2) / (m_solid / M_NaHCO3). The CO2 that stayed dissolved
    released DH_CO2_SOLN per mole, so dH_obs = dH_gas + (1 - f) DH_CO2_SOLN.
    TODO: return (dH_gas, f)."""
    return None  # TODO


def jumps(data, cfg):
    t, T = data[:, 0], data[:, 1]
    before = extrapolate(t[t <= cfg["pre_until"]], T[t <= cfg["pre_until"]], cfg["t_mix"], T_RES)
    after = extrapolate(t[t >= cfg["post_from"]], T[t >= cfg["post_from"]], cfg["t_mix"], T_RES)
    return before, after


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "calorimetry_example.csv"
    runs = {}
    for r in read_csv(path):
        runs.setdefault(r["run"], []).append((float(r["t_s"]), float(r["T_C"])))
    runs = {k: np.array(v) for k, v in runs.items()}
    if todo(cup_heat_capacity(1, 1, 1, 0, 0.5), enthalpy_per_mol(1, 1, 1, 1, 0, 1, 0), all_gas_value(1, 1, 1)):
        return

    cal = SETUP["calibration"]
    tc, tf = jumps(runs["calibration"], cal)
    C_cup = propagate(cup_heat_capacity, {"m_cold": cal["m_cold"], "m_hot": cal["m_hot"],
                                          "T_hot": cal["T_hot"], "T_cold": tc, "T_final": tf})
    print(f"calibration: T_cold {tc[0]:.2f}, T_final {tf[0]:.2f} C -> C_cup = {C_cup[0]:.0f} +/- {C_cup[1]:.0f} J/K")

    for name in ("reaction", "nacl", "epsom"):
        if name not in runs:
            continue
        cfg = SETUP[name]
        tb, ta = jumps(runs[name], cfg)
        s = cfg["solid"]
        f = lambda liquid, m_solid, C_cup, T_before, T_after: enthalpy_per_mol(
            liquid, m_solid, C_SOLID[s], M[s], C_cup, T_before, T_after)
        dh = propagate(f, {"liquid": cfg["liquid"], "m_solid": cfg["m_solid"], "C_cup": C_cup,
                           "T_before": tb, "T_after": ta})
        print(f"{name}: Delta T = {ta[0] - tb[0]:+.2f} K, Delta H = {dh[0]:+.1f} +/- {dh[1]:.1f} kJ/mol {s}")
        if name == "reaction":
            g = lambda dH_obs, mass_loss, m_solid: all_gas_value(dH_obs, mass_loss, m_solid)[0]
            gas = propagate(g, {"dH_obs": dh, "mass_loss": cfg["mass_loss"], "m_solid": cfg["m_solid"]})
            frac = all_gas_value(dh[0], cfg["mass_loss"][0], cfg["m_solid"][0])[1]
            print(f"  CO2 escaped {frac:.0%}; corrected to all CO2 gas: {gas[0]:+.1f} +/- {gas[1]:.1f} kJ/mol")
            print(f"  Hess prediction (all CO2 gas): {PREDICTED[name]:+.1f} kJ/mol")
        else:
            print(f"  table value: {PREDICTED[name]:+.1f} kJ/mol")

    plt = pyplot()
    if plt is None:
        return
    names = [n for n in ("calibration", "reaction", "nacl", "epsom") if n in runs]
    fig, axes = plt.subplots(1, len(names), figsize=(3.2 * len(names), 3.2))
    for ax, name in zip(np.atleast_1d(axes), names):
        d, cfg = runs[name], SETUP[name]
        ax.plot(d[:, 0], d[:, 1], "o", ms=3)
        for mask in (d[:, 0] <= cfg["pre_until"], d[:, 0] >= cfg["post_from"]):
            b, a = np.polyfit(d[mask, 0], d[mask, 1], 1)
            tt = np.sort(np.r_[d[mask, 0], cfg["t_mix"]])
            ax.plot(tt, a + b * tt, "--")
        ax.axvline(cfg["t_mix"], color="grey", lw=0.8)
        ax.set_title(name)
        ax.set_xlabel("t (s)")
        ax.set_ylabel("T (C)")
    save_plot(fig, "lesson02_calorimetry.png")


if __name__ == "__main__":
    main()
