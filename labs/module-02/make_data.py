"""Regenerate the small example data sets for Module 02.

The data are generated from known models with a fixed random seed, so they are realistic but not
measured. Each file header says the model and parameters. Run from anywhere:

    py make_data.py
"""
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
R = 8.314462618  # J/(mol K), CODATA 2022 (exact)
rng = np.random.default_rng(2026)


def write(name, header, cols, fmt):
    path = HERE / name
    data = np.column_stack(cols)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:  # LF on every OS
        np.savetxt(fh, data, delimiter=",", header=header, comments="", fmt=fmt)
    print(f"wrote {path.name} ({len(data)} rows)")


# 1. Rate constants at several temperatures (Arrhenius, Ea = 103 kJ/mol, A = 4.0e13 1/s, 3 % noise)
T = np.array([298.15, 303.15, 308.15, 313.15, 318.15, 323.15, 328.15, 333.15])
k = 4.0e13 * np.exp(-103e3 / (R * T)) * (1 + 0.03 * rng.standard_normal(T.size))
write("arrhenius_rates.csv", "T_K,k_per_s", [T, k], ["%.2f", "%.4e"])

# 2. Concentration of a reactant decaying first order (k = 0.0040 1/s, c0 = 0.100 mol/L, noise 0.0002 mol/L)
t = np.arange(0, 901, 30.0)
c = 0.100 * np.exp(-0.0040 * t) + 0.0002 * rng.standard_normal(t.size)
write("decay_concentration.csv", "t_s,c_mol_per_L", [t, c], ["%.0f", "%.5f"])

# 3. Cooling of a mug of hot water (Newton: T_env = 23.0 C, T0 = 80.0 C, k = 1/1500 1/s),
#    read every 60 s for 40 min with a 0.1 C thermometer and +-0.3 C reading scatter
t = np.arange(0, 2401, 60.0)
T_c = 23.0 + (80.0 - 23.0) * np.exp(-t / 1500.0) + 0.3 * rng.standard_normal(t.size)
write("cooling_example.csv", "t_s,T_C", [t, np.round(T_c, 1)], ["%.0f", "%.1f"])
