"""Generate the example data sets for the Module 13 labs from known models (fixed seed).

    py make_data.py

The files are realistic but NOT measured. The true model parameters are below, so you can check
what your analysis recovers. Replace them with your own measurements when you have them.
"""
import csv
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
rng = np.random.default_rng(13)

# ---------------- syringe_example.csv (lesson 13.1) ----------------
# Sealed 10 mL syringe pressed onto a kitchen scale, isothermal (slow pushing).
P_ATM = 100_800.0      # Pa, room pressure on the day
AREA = 1.65e-4         # m^2, inner cross-section of the barrel (10 mL mark spans 60.6 mm)
DEAD = 0.15e-6         # m^3, air trapped in the nozzle below the 0 mL mark
FRICTION = 1.2         # N, plunger friction (adds when pushing in, subtracts when letting out)
G = 9.80665            # m/s^2


def syringe():
    rows = []
    v0 = 10e-6 + DEAD
    for direction, marks in (("in", [10, 9, 8, 7, 6, 5]), ("out", [5, 6, 7, 8, 9, 10])):
        for v_ml in marks:
            v = v_ml * 1e-6 + DEAD
            p = P_ATM * v0 / v                      # Boyle's law, isothermal
            force = (p - P_ATM) * AREA + (FRICTION if direction == "in" else -FRICTION)
            if v_ml == 10:
                force = 0.0 if direction == "in" else max(force, 0.0)
            grams = force / G * 1000 + rng.normal(0, 8)
            rows.append((direction, v_ml, round(max(grams, 0.0))))
    with open(HERE / "syringe_example.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["direction", "V_mL", "scale_g"])
        w.writerows(rows)


# ---------------- freezing_example.csv (lesson 13.6) ----------------
# 200 g of tap water and 200 g of 0.50 mol/kg NaCl solution in a freezer at -18 C, read with a
# kitchen thermometer that reads 0.3 C too high. True freezing points: 0.00 C and -1.72 C
# (the model value is set a few per cent below the ideal 1.86 K, as real NaCl solutions are).
BIAS = 0.3


def freezing():
    rows = []
    for sample, tf, t_super in (("water", 0.0, -2.4), ("salt_0.50m", -1.72, -4.1)):
        temp, frozen_frac = 18.0, 0.0
        nucleated = False
        for minute in range(0, 121, 2):
            if not nucleated:
                temp = -18 + (18.0 + 18) * np.exp(-minute / 38)
                if temp <= t_super:
                    nucleated = True
                    temp = tf
            elif frozen_frac < 0.8:
                frozen_frac += 0.03
                # salt is pushed out of the ice, so the remaining liquid gets saltier and colder
                temp = tf / (1 - frozen_frac) if tf < 0 else tf
                temp = max(temp, tf - 2.5)
            else:
                temp = -18 + (temp + 18) * np.exp(-2 / 15)   # solid block cools to freezer T
            rows.append((sample, minute, round(temp + BIAS + rng.normal(0, 0.05), 1)))
    with open(HERE / "freezing_example.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["sample", "t_min", "T_C"])
        w.writerows(rows)


if __name__ == "__main__":
    syringe()
    freezing()
    print("wrote syringe_example.csv and freezing_example.csv")
