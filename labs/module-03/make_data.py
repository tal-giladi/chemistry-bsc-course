"""Regenerate the small example data sets for Module 03.

The data are generated from known models with a fixed random seed, so they are realistic but not
measured. Each block below states the model and its parameters, so you can check your answers.
Run from anywhere:

    py make_data.py
"""
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
rng = np.random.default_rng(2026)


def write(name, header, cols, fmt):
    path = HERE / name
    data = np.column_stack(cols)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:  # LF on every OS
        np.savetxt(fh, data, delimiter=",", header=header, comments="", fmt=fmt)
    print(f"wrote {path.name} ({len(data)} rows)")


# 1. Absorbance of a mixture of two dyes, X (peak 430 nm) and Y (peak 630 nm), 1.00 cm cell.
#    Molar absorptivities are illustrative Gaussian bands (L mol^-1 cm^-1), not real dyes.
#    True concentrations: c_X = 2.70e-5 mol/L, c_Y = 3.50e-5 mol/L. Absorbance noise 0.003.
lam = np.arange(400, 701, 25.0)
eps_X = 1.60e4 * np.exp(-((lam - 430) / 40) ** 2) + 600
eps_Y = 1.05e4 * np.exp(-((lam - 630) / 45) ** 2) + 400
A_mix = eps_X * 2.70e-5 + eps_Y * 3.50e-5 + 0.003 * rng.standard_normal(lam.size)
write("mixture_absorbance.csv", "wavelength_nm,eps_X,eps_Y,A_mix",
      [lam, eps_X, eps_Y, A_mix], ["%.0f", "%.0f", "%.0f", "%.4f"])

# 2. A reaction followed by its reactant concentration. Model: second order, 2A -> products,
#    rate = k c^2 with k = 0.54 L mol^-1 s^-1, c0 = 0.0100 mol/L, noise 0.00005 mol/L.
t = np.arange(0, 1201, 60.0)
c = 0.0100 / (1 + 0.54 * 0.0100 * t) + 0.00005 * rng.standard_normal(t.size)
write("order_test.csv", "t_s,c_mol_per_L", [t, c], ["%.0f", "%.5f"])

# 3. A home pendulum (string 0.50 m, keys as the bob). Peak amplitude read against a ruler every
#    5 full swings. Model: period 1.42 s, amplitude 20.0 cm, gamma = 0.0120 1/s (amplitude
#    halves in about 58 s), readings rounded to 0.5 cm with 0.3 cm reading scatter.
n = np.arange(0, 61, 5.0)
t = 1.42 * n
amp = 20.0 * np.exp(-0.0120 * t) + 0.3 * rng.standard_normal(n.size)
write("pendulum_example.csv", "swings,t_s,amplitude_cm", [n, t, np.round(amp * 2) / 2],
      ["%.0f", "%.2f", "%.1f"])

# 4. Consecutive first-order reactions A -> B -> C, A0 = 10.0 mmol/L, k1 = 0.150 1/min,
#    k2 = 0.050 1/min, all three species measured every 2 min for 60 min, noise 0.10 mmol/L.
t = np.arange(0, 61, 2.0)
k1, k2, A0 = 0.150, 0.050, 10.0
A = A0 * np.exp(-k1 * t)
B = A0 * k1 / (k2 - k1) * (np.exp(-k1 * t) - np.exp(-k2 * t))
C = A0 - A - B
noisy = [x + 0.10 * rng.standard_normal(t.size) for x in (A, B, C)]
write("consecutive_example.csv", "t_min,A_mM,B_mM,C_mM", [t, *noisy],
      ["%.0f", "%.3f", "%.3f", "%.3f"])
