"""Lesson 06.4 reference solution (module practical, parts 1 and 2): the ATP budget of a yeast
fermentation and of the cell.

Run:   py lesson04_atp_budget_solution.py                  (example data)
       py lesson04_atp_budget_solution.py my_bottles.csv   (columns t_h,m_yeast_g,m_control_g)
Optional: set SUGAR_G and YEAST_G below to your own masses.
The plot is saved to runs/lesson04_fermentation.png next to this file.
"""
import csv
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent

R = 8.314462618          # J/(mol K), CODATA 2022 via NIST
M_SUCROSE = 342.30       # g/mol, C12H22O11
M_CO2 = 44.009           # g/mol
SUGAR_G = 20.0           # table sugar in the yeast bottle, g
YEAST_G = 7.0            # dry yeast in the yeast bottle, g

DG0_ATP = -30.5          # kJ/mol, ATP + H2O -> ADP + Pi, standard biochemical (OpenStax Biology 2e)
CELL_MM = {"ATP": 2.25, "ADP": 0.25, "Pi": 1.65}   # illustrative cytosol concentrations, mM
DG_GLUCOSE_OX = -2910.0  # kJ/mol, glucose + 6 O2 -> 6 CO2 + 6 H2O, eQuilibrator (1 mM standard)
# ethanol + 3 O2 -> 2 CO2 + 3 H2O from OpenStax Chemistry 2e Appendix G (Delta_f G, kJ/mol)
DG_ETHANOL_OX = 2 * (-394.36) + 3 * (-237.1) - (-174.8)


def atp_delta_g(dg0, atp_mM, adp_mM, pi_mM, T):
    """Delta G (kJ/mol) of ATP hydrolysis at the given concentrations:
    Delta G = Delta G0' + R T ln([ADP][Pi]/[ATP]), concentrations in mol/L."""
    q = (adp_mM / 1000) * (pi_mM / 1000) / (atp_mM / 1000)
    return dg0 + R * T * np.log(q) / 1000


def co2_released(m_yeast, m_control):
    """CO2 (g) that has left the yeast bottle at each time: its mass loss since t = 0, minus the
    control bottle's mass loss (evaporation) over the same time."""
    return (m_yeast[0] - m_yeast) - (m_control[0] - m_control)


def atp_from_co2(co2_g):
    """mol ATP made by fermentation: glucose -> 2 ethanol + 2 CO2 makes 2 ATP, so one ATP per CO2."""
    return co2_g / M_CO2


def read_bottles(path):
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    return (np.array([float(r[k]) for r in rows]) for k in ("t_h", "m_yeast_g", "m_control_g"))


def main():
    T = 310.15
    dg_cell = atp_delta_g(DG0_ATP, CELL_MM["ATP"], CELL_MM["ADP"], CELL_MM["Pi"], T)
    print(f"ATP hydrolysis at 37 C, ATP {CELL_MM['ATP']} mM, ADP {CELL_MM['ADP']} mM, Pi {CELL_MM['Pi']} mM:")
    print(f"  Delta G = {DG0_ATP} + RT ln Q = {dg_cell:.1f} kJ/mol")

    dg_ferm = DG_GLUCOSE_OX - 2 * DG_ETHANOL_OX     # Hess's law, rough (mixed standard states)
    print(f"\nglucose oxidation {DG_GLUCOSE_OX:.0f} kJ/mol; ethanol oxidation {DG_ETHANOL_OX:.0f} kJ/mol")
    print(f"fermentation, glucose -> 2 ethanol + 2 CO2 (Hess): about {dg_ferm:.0f} kJ/mol")
    for name, n_atp, dg in (("respiration, 30 ATP", 30, DG_GLUCOSE_OX), ("fermentation, 2 ATP", 2, dg_ferm)):
        print(f"  {name:<20} stores {n_atp * -dg_cell:6.0f} kJ of {-dg:5.0f} kJ released: {n_atp * dg_cell / dg:.0%}")

    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "fermentation_example.csv"
    t, my, mc = read_bottles(path)
    co2 = co2_released(my, mc)
    n_atp = atp_from_co2(co2)
    co2_max = SUGAR_G / M_SUCROSE * 4 * M_CO2
    early = (t >= 1) & (t <= 6)
    rate, _ = np.polyfit(t[early], co2[early], 1)
    print(f"\nbottles: {path.name}")
    print(f"  CO2 released after {t[-1]:.0f} h: {co2[-1]:.1f} g of {co2_max:.2f} g possible ({co2[-1] / co2_max:.0%})")
    print(f"  ATP made by the yeast: {n_atp[-1]:.3f} mol, storing {n_atp[-1] * -dg_cell:.1f} kJ")
    print(f"  early rate (1-6 h): {rate:.2f} g CO2/h = {atp_from_co2(rate) * 1000 / YEAST_G:.2f} mmol ATP per g yeast per hour")

    (HERE / "runs").mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.plot(t, co2, "o-", label="CO2 released (yeast - control)")
    ax.axhline(co2_max, color="grey", ls=":", label=f"all sugar fermented, {co2_max:.1f} g")
    ax.set_xlabel("time (h)")
    ax.set_ylabel("CO2 (g)")
    ax.set_title("Yeast fermentation of table sugar")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(HERE / "runs" / "lesson04_fermentation.png", dpi=120)
    print("plot saved to runs/lesson04_fermentation.png")


if __name__ == "__main__":
    main()
