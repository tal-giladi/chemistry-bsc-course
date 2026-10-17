"""Lesson 23.5 (exercise: fill in the TODO functions): EMF and internal resistance of home cells, and the Nernst slope.

Run from this folder:
    py lesson05_cells.py                                   (example data)
    py lesson05_cells.py my_cells.csv                      (columns cell,R_ohm,V_V; R_ohm = open for open circuit)
    py lesson05_cells.py my_cells.csv nernst_example.csv   (columns c_Cu_M,E_V)
Part 1: for each cell, I = V/R through each load resistor; fit V = E - I r (the load line) to get the EMF E
and the internal resistance r with uncertainties, and the largest power the cell can deliver.
Part 2: lab data for Zn | Zn2+ (0.100 M) || Cu2+ (c) | Cu at 25 C: fit E against log10 c, compare the slope
with 2.303 RT/(nF) and find n. Writes runs/lesson05_cells.png.
"""
import sys
from pathlib import Path

import numpy as np

from pc23 import HERE, R, F, read_csv, column, linfit, todo, save_plot, pyplot

T = 298.15


def load_line(V, R_load):
    """Currents I = V/R (A), then fit V = E - r I. Returns (E, sE, r, sr).
    TODO: compute I, call linfit(I, V) -> (a, b, sa, sb, ...): E = a, r = -b."""
    return None  # TODO


def max_power(E, r):
    """Largest power into a load (W), reached when R_load = r: P = E^2 / (4 r).
    TODO: one line."""
    return None  # TODO


def n_from_slope(slope):
    """Electrons transferred from the Nernst slope dE/dlog10(c) = 2.303 RT/(nF) (V per decade).
    TODO: one line."""
    return None  # TODO


def main():
    cells_path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "cells_example.csv"
    nernst_path = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "nernst_example.csv"
    if todo(load_line(np.array([0.5, 0.4, 0.3]), np.array([1000.0, 500.0, 250.0])), max_power(1, 1), n_from_slope(0.03)):
        return

    rows = read_csv(cells_path)
    names = list(dict.fromkeys(r["cell"] for r in rows))
    plt = pyplot()
    if plt:
        fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.6))
    print("Part 1: load lines")
    for name in names:
        rr = [r for r in rows if r["cell"] == name]
        closed = [r for r in rr if r["R_ohm"] != "open"]
        V = np.array([float(r["V_V"]) for r in closed])
        Rl = np.array([float(r["R_ohm"]) for r in closed])
        E, sE, r, sr = load_line(V, Rl)
        oc = [float(r["V_V"]) for r in rr if r["R_ohm"] == "open"]
        oc_txt = f", open-circuit reading {oc[0]:.3f} V" if oc else ""
        print(f"  {name:8s}: E = {E:.3f} +/- {sE:.3f} V, r = {r:.0f} +/- {sr:.0f} ohm{oc_txt}; "
              f"max power {max_power(E, r) * 1e6:.0f} uW at R = {r:.0f} ohm")
        if plt:
            a1.plot(V / Rl * 1000, V, "o", label=name)
            ii = np.linspace(0, (V / Rl).max(), 20)
            a1.plot(ii * 1000, E - r * ii, "--", lw=1)

    nrows = read_csv(nernst_path)
    c, E = column(nrows, "c_Cu_M"), column(nrows, "E_V")
    a, b, sa, sb, _, s = linfit(np.log10(c), E)
    theory = np.log(10) * R * T / (2 * F)
    print("Part 2: Nernst")
    print(f"  E = {a:.4f} + {b * 1000:.2f} log10(c)   (slope +/- {sb * 1000:.2f} mV/decade)")
    print(f"  theory for n = 2: {theory * 1000:.2f} mV/decade;  n from slope = {n_from_slope(b):.2f}")
    print(f"  E at c = 0.100 M (equal concentrations, ~E standard): {a + b * np.log10(0.100):.4f} V "
          f"(table: 1.099 V; a few mV of junction potential and activity effects are normal)")
    if plt:
        a1.set_xlabel("I (mA)")
        a1.set_ylabel("V (V)")
        a1.legend()
        a2.plot(np.log10(c), E, "o")
        xx = np.linspace(np.log10(c).min(), np.log10(c).max(), 10)
        a2.plot(xx, a + b * xx, "--")
        a2.set_xlabel("log10 [Cu2+] (M)")
        a2.set_ylabel("E cell (V)")
        save_plot(fig, "lesson05_cells.png")


if __name__ == "__main__":
    main()
