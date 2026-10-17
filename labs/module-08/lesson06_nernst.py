"""Lesson 08.6 hands-on: cell potentials, Nernst, and a real lemon cell.

Fill in the two TODO functions, then run:
       py lesson06_nernst.py                  (uses lemon_cell_example.csv)
       py lesson06_nernst.py my_cells.csv     (columns electrolyte,R_ohm,V_V; R 'open' = no load)
Reference solution: lesson06_nernst_solution.py
Constants: F = 96485.33212 C/mol and R = 8.314462618 J/(mol K), CODATA 2022 via NIST (exact).
E standard values: OpenStax Chemistry 2e Appendix L (Zn2+/Zn -0.7618 V, Cu2+/Cu +0.337 V).
Writes runs/lesson06_load_curve.png.
"""
import csv
import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import curve_fit

F = 96485.33212
R = 8.314462618
T = 298.15
E_ZN = -0.7618
E_CU = 0.337
HERE = Path(__file__).resolve().parent


def nernst(e_standard, n, q, t=T):
    """E = E standard - (RT / nF) ln Q.
    TODO: one line with math.log."""
    return None


def loaded_voltage(r_load, emf, r_internal):
    """Voltage across a load resistor for a cell with internal resistance: V = E R / (R + r).
    TODO: one line. It must work when r_load is a numpy array (curve_fit passes arrays)."""
    return None


def read_cells(path):
    data = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            data.setdefault(row["electrolyte"], []).append((row["R_ohm"], float(row["V_V"])))
    return data


def main():
    if nernst(1.0, 1, 1.0) is None or loaded_voltage(1.0, 1.0, 1.0) is None:
        print("TODO: write nernst() and loaded_voltage() first.")
        return
    # 1. Daniell cell from the table
    e0 = E_CU - E_ZN
    dg0 = -2 * F * e0 / 1000
    k = math.exp(2 * F * e0 / (R * T))
    print(f"Daniell cell Zn|Zn2+||Cu2+|Cu: E0 = {e0:.3f} V, dG0 = {dg0:.0f} kJ/mol, K = {k:.2e}")
    for zn, cu in ((1.0, 1.0), (0.10, 1.0), (1.0, 0.010), (1.0, 1e-6)):
        print(f"  [Zn2+] = {zn:g} M, [Cu2+] = {cu:g} M: E = {nernst(e0, 2, zn / cu):.3f} V")

    # 2. Copper concentration cell: same electrodes, different concentrations
    print(f"Cu concentration cell 0.0010 M | 1.0 M: E = {nernst(0.0, 2, 0.0010 / 1.0):.4f} V")

    # 3. Lemon cell as the chemistry really is: Zn -> Zn2+ and 2 H+ -> H2 on the copper
    print("Lemon-cell estimate (Zn anode, H+/H2 cathode on copper, p(H2) = 1e-6 bar):")
    for ph in (2.2, 3.0):
        for zn in (1e-6, 1e-4):
            e_cathode = nernst(0.0, 2, 1e-6 / (10 ** -ph) ** 2)    # 2H+ + 2e- -> H2
            e_anode = nernst(E_ZN, 2, 1 / zn)                     # Zn2+ + 2e- -> Zn
            print(f"  pH {ph}, [Zn2+] = {zn:g} M: E = {e_cathode - e_anode:.2f} V")

    # 4. Real cells: fit E and the internal resistance from the load curve
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "lemon_cell_example.csv"
    data = read_cells(path)
    print(f"\nLoad-curve fits from {path.name}:")
    fits = {}
    for name, rows in data.items():
        r_load = np.array([float(r) for r, _ in rows if r != "open"])
        v = np.array([v for r, v in rows if r != "open"])
        v_open = [v for r, v in rows if r == "open"]
        popt, pcov = curve_fit(loaded_voltage, r_load, v, p0=[max(v), 1000.0])
        err = np.sqrt(np.diag(pcov))
        fits[name] = (r_load, v, popt)
        i_short = popt[0] / popt[1] * 1000
        p_max = popt[0] ** 2 / (4 * popt[1]) * 1000
        open_txt = f", open-circuit reading {v_open[0]:.3f} V" if v_open else ""
        print(f"  {name:<11} E = {popt[0]:.3f} +/- {err[0]:.3f} V, r = {popt[1]:.0f} +/- {err[1]:.0f} ohm"
              f"{open_txt}; max current {i_short:.2f} mA, max power {p_max:.3f} mW")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed: skipping the plot")
        return
    fig, ax = plt.subplots(figsize=(6, 4))
    grid = np.logspace(1.8, 4.2, 100)
    for name, (r_load, v, popt) in fits.items():
        line, = ax.semilogx(r_load, v, "o", label=name)
        ax.semilogx(grid, loaded_voltage(grid, *popt), color=line.get_color())
    ax.set_xlabel("load resistance (ohm)")
    ax.set_ylabel("voltage across load (V)")
    ax.legend()
    out = HERE / "runs"
    out.mkdir(exist_ok=True)
    fig.tight_layout()
    fig.savefig(out / "lesson06_load_curve.png", dpi=120)
    print(f"\nplot written to {out / 'lesson06_load_curve.png'}")


if __name__ == "__main__":
    main()
