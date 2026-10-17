"""Lesson 23.6 module practical (exercise: fill in the TODO functions): surface tension of detergent solutions by drop weight.

Run from this folder:
    py lesson06_surface.py                       (uses drops_example.csv)
    py lesson06_surface.py my_drops.csv 21.0     (columns c_mL_per_L,trial,n_drops,mass_g; then the water
                                                  temperature in C)
Steps: (1) mass per drop for each solution, mean and standard error over trials; (2) surface tension
gamma = gamma_water x (m_drop / m_drop_water) (Tate's law, same tip), with gamma_water from IAPWS at your
temperature; (3) gamma against ln c: two straight lines, their intersection is the break (effective CMC);
(4) Gibbs surface excess from the slope just below the break and the area per molecule.
Writes runs/lesson06_surface.png.
"""
import sys
from pathlib import Path

import numpy as np

from pc23 import HERE, R, N_A, read_csv, column, linfit, todo, save_plot, pyplot


def gamma_water(T_C):
    """Surface tension of water in mN/m, IAPWS R1-76(2014): 235.8 tau^1.256 (1 - 0.625 tau), tau = 1 - T/Tc."""
    tau = 1 - (T_C + 273.15) / 647.096
    return 235.8 * tau ** 1.256 * (1 - 0.625 * tau)


def surface_tension(m_drop, m_drop_water, g_water):
    """Tate's law with the same tip: drop mass is proportional to gamma. Returns gamma in mN/m.
    TODO: one line."""
    return None  # TODO


def break_point(lnc, g, split):
    """Fit one line to the points with index < split (falling part) and one to index >= split (plateau).
    Return (lnc_break, slope_below, intercept_below, slope_above, intercept_above).
    TODO: two linfit calls; the lines a1 + b1 x and a2 + b2 x meet at x = (a2 - a1) / (b1 - b2)."""
    return None  # TODO


def surface_excess(slope_mN, T_C, n_ions=1):
    """Gibbs adsorption: Gamma = -(1/(n R T)) d gamma / d ln c, slope in mN/m per ln unit -> mol/m^2.
    n_ions = 1 for a non-ionic surfactant or an ionic one in excess salt, 2 for a 1:1 ionic one in water.
    TODO: one line (convert mN/m to N/m)."""
    return None  # TODO


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "drops_example.csv"
    T_C = float(sys.argv[2]) if len(sys.argv) > 2 else 21.0
    if todo(surface_tension(1, 1, 1), break_point(np.arange(4.0), np.array([4, 3, 1, 1.0]), 2), surface_excess(-1, 25)):
        return
    rows = read_csv(path)
    c, m, n = column(rows, "c_mL_per_L"), column(rows, "mass_g"), column(rows, "n_drops")
    per_drop = m / n
    levels = np.unique(c)
    md = np.array([per_drop[c == x].mean() for x in levels])
    se = np.array([per_drop[c == x].std(ddof=1) / np.sqrt((c == x).sum()) for x in levels])
    gw = gamma_water(T_C)
    print(f"water at {T_C:.1f} C: gamma = {gw:.2f} mN/m (IAPWS); drop mass {md[0] * 1000:.2f} +/- {se[0] * 1000:.2f} mg")
    g = surface_tension(md, md[0], gw)
    sg = g * np.sqrt((se / md) ** 2 + (se[0] / md[0]) ** 2)
    print(" c (mL/L)  drop (mg)  gamma (mN/m)")
    for x, d, gg, s in zip(levels, md, g, sg):
        print(f" {x:8.2f}  {d * 1000:9.2f}  {gg:6.1f} +/- {s:.1f}")

    pos = levels > 0                                 # ln c needs c > 0; water is the reference
    lnc, gp = np.log(levels[pos]), g[pos]
    best = None
    for split in range(2, len(lnc) - 1):             # choose the split with the smallest total residual
        x, b1, a1, b2, a2 = break_point(lnc, gp, split)
        sse = np.sum((gp[:split] - (a1 + b1 * lnc[:split])) ** 2) + np.sum((gp[split:] - (a2 + b2 * lnc[split:])) ** 2)
        if best is None or sse < best[0]:
            best = (sse, split, x, b1, a1, b2, a2)
    _, split, x, b1, a1, b2, a2 = best
    # slope just below the break: the last three points of the falling part
    s_low = linfit(lnc[split - 3:split], gp[split - 3:split])[1] if split >= 3 else b1
    print(f"break (effective CMC) at c = {np.exp(x):.2f} mL/L, gamma there {a2 + b2 * x:.1f} mN/m")
    print(f"slope just below the break: {s_low:.1f} mN/m per ln unit")
    for n_ions in (1, 2):
        G = surface_excess(s_low, T_C, n_ions)
        print(f"  n = {n_ions}: surface excess {G * 1e6:.2f} umol/m^2, area per molecule {1e18 / (G * N_A):.2f} nm^2")

    plt = pyplot()
    if plt is None:
        return
    fig, ax = plt.subplots(figsize=(5.5, 3.8))
    ax.errorbar(lnc, gp, yerr=sg[pos], fmt="o", label="detergent solutions")
    ax.axhline(gw, ls=":", color="grey", label="water")
    xx = np.linspace(lnc.min(), x, 20)
    ax.plot(xx, a1 + b1 * xx, "--")
    xx = np.linspace(x, lnc.max(), 20)
    ax.plot(xx, a2 + b2 * xx, "--")
    ax.set_xlabel("ln c  (c in mL detergent per L)")
    ax.set_ylabel("surface tension (mN/m)")
    ax.legend()
    save_plot(fig, "lesson06_surface.png")


if __name__ == "__main__":
    main()
