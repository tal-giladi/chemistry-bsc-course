"""Lesson 23.1 (exercise: fill in the TODO functions): kinetic theory and the heat-capacity ratio of air.

Run from this folder:
    py lesson01_gases.py                                   (example data)
    py lesson01_gases.py my_speeds.csv my_clement.csv      (your simulation export and readings)
Files: md_speeds_example.csv (column speed_m_s, exported from the gas-laws simulation, argon) and
clement_desormes_example.csv (columns trial,h1_cm,h2_cm: manometer heights after pumping and after
the adiabatic release and warming back).
Part 1: temperature from the speeds and a Maxwell-Boltzmann check. Part 2: gamma = Cp/Cv with a 95 %
interval, and the molar heat capacities it implies. Writes runs/lesson01_gases.png.
"""
import sys
from pathlib import Path

import numpy as np

from pc23 import HERE, R, read_csv, column, t95, todo, save_plot, pyplot

M_GAS = 39.948e-3      # kg/mol, argon (the simulation's preset gas)


def mb_pdf(v, T, M):
    """Maxwell-Boltzmann speed distribution f(v) in s/m (integrates to 1 over v)."""
    a = M / (2 * R * T)
    return 4 * np.pi * (a / np.pi) ** 1.5 * v ** 2 * np.exp(-a * v ** 2)


def temperature_from_speeds(v, M):
    """Temperature (K) from a sample of molecular speeds: (1/2) M <v^2> = (3/2) R T per mole.
    TODO: one line with the mean of v**2."""
    return None  # TODO


def gamma_clement(h1, h2):
    """Clement-Desormes: gamma = h1 / (h1 - h2) for each trial (arrays in, array out).
    TODO: one line."""
    return None  # TODO


def main():
    sp = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "md_speeds_example.csv"
    cd = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "clement_desormes_example.csv"
    v = column(read_csv(sp), "speed_m_s")
    rows = read_csv(cd)
    h1, h2 = column(rows, "h1_cm"), column(rows, "h2_cm")
    T = temperature_from_speeds(v, M_GAS)
    g = gamma_clement(h1, h2)
    if todo(T, g):
        return

    # Part 1
    sT = T * np.sqrt(2 / (3 * len(v)))      # <v^2> of N molecules: relative SD sqrt(2/(3N))
    print(f"Part 1: {len(v)} speeds, T = {T:.1f} +/- {sT:.1f} K")
    for name, f in (("most probable", 2), ("mean", 8 / np.pi), ("rms", 3)):
        print(f"  {name:13s} speed: theory {np.sqrt(f * R * T / M_GAS):6.1f} m/s", end="")
        sample = {2: None, 8 / np.pi: np.mean(v), 3: np.sqrt(np.mean(v ** 2))}[f]
        print("" if sample is None else f", sample {sample:6.1f} m/s")
    hist, edges = np.histogram(v, bins=30)
    centres = 0.5 * (edges[1:] + edges[:-1])
    expected = mb_pdf(centres, T, M_GAS) * len(v) * (edges[1] - edges[0])
    ok = expected > 5
    chi2 = float(np.sum((hist[ok] - expected[ok]) ** 2 / expected[ok]))
    print(f"  histogram vs Maxwell-Boltzmann: chi^2 = {chi2:.1f} for {ok.sum() - 1} degrees of freedom")

    # Part 2
    mean, sd = g.mean(), g.std(ddof=1)
    ci = t95(len(g) - 1) * sd / np.sqrt(len(g))
    print(f"Part 2: gamma per trial: {', '.join(f'{x:.3f}' for x in g)}")
    print(f"  gamma = {mean:.3f}, SD {sd:.3f}, 95 % CI +/- {ci:.3f} (air, diatomic ideal: 1.400)")
    cv = R / (mean - 1)
    print(f"  Cv,m = R/(gamma-1) = {cv:.1f} J/(mol K) = {cv / R:.2f} R;  Cp,m = {cv + R:.1f} J/(mol K)")

    plt = pyplot()
    if plt is None:
        return
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.6))
    a1.hist(v, bins=30, density=True, alpha=0.5, label="simulation")
    vv = np.linspace(0, v.max(), 300)
    a1.plot(vv, mb_pdf(vv, T, M_GAS), label=f"Maxwell-Boltzmann, {T:.0f} K")
    a1.set_xlabel("speed (m/s)")
    a1.set_ylabel("f(v) (s/m)")
    a1.legend()
    a2.errorbar(range(1, len(g) + 1), g, fmt="o")
    a2.axhline(1.4, ls="--", color="grey")
    a2.set_xlabel("trial")
    a2.set_ylabel("gamma")
    save_plot(fig, "lesson01_gases.png")


if __name__ == "__main__":
    main()
