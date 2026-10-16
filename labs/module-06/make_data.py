"""Generate the example data for the Module 6 labs (seeded, so the files never change).

Run:   py make_data.py
The models and their true parameters are written here so you can check your answers.
The data are realistic but NOT measured. Replace them with your own measurements.
"""
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
rng = np.random.default_rng(606)


def osmosis():
    """Potato strips (about 1 x 1 x 4 cm, 3-5 g) soaked 2 h in NaCl solutions at about 22 C.
    True isotonic point C_ISO = 0.14 mol/L NaCl. The response is not linear: the percentage mass
    change saturates at both ends, dm% = 18 tanh(-3.2 (c - C_ISO)).
    Strip-to-strip noise sd 1.0 % of the mass; scale resolution 0.01 g (pocket scale)."""
    c_iso = 0.14
    lines = ["c_NaCl_M,strip,m_before_g,m_after_g"]
    for c in (0.0, 0.1, 0.2, 0.3, 0.4, 0.5):
        for strip in (1, 2, 3):
            m0 = rng.uniform(3.0, 5.0)
            pct = 18 * np.tanh(-3.2 * (c - c_iso)) + rng.normal(0, 1.0)
            m1 = m0 * (1 + pct / 100)
            lines.append(f"{c:.1f},{strip},{m0:.2f},{m1:.2f}")
    (HERE / "osmosis_example.csv").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def fermentation():
    """Two open 500 mL bottles (cotton-wool plug, never a tight cap) at about 30 C.
    Yeast bottle: 25.0 g bottle + 250 g warm water + 20.0 g table sugar + 7.0 g dry yeast.
    Control bottle: same without yeast.
    Sucrose 20.0 g = 0.05843 mol -> 4 CO2 each -> 10.29 g CO2 at complete conversion.
    True model: 88 % of the sugar is fermented in the end (the rest goes to yeast growth or is
    left over); about 0.40 g CO2 stays dissolved and never leaves; CO2 out
    = A (1 - exp(-(t - 0.5 h)/7.0 h)) for t > 0.5 h, A = 0.88 * 10.29 - 0.40 = 8.66 g.
    Both bottles lose water by evaporation at 0.030 g/h. Scale resolution 0.1 g, noise sd 0.05 g."""
    co2_full = 20.0 / 342.30 * 4 * 44.01
    a = 0.88 * co2_full - 0.40
    m_yeast0 = 25.0 + 250.0 + 20.0 + 7.0
    m_ctrl0 = 25.0 + 250.0 + 20.0
    lines = ["t_h,m_yeast_g,m_control_g"]
    for t in (0, 1, 2, 3, 4, 6, 8, 10, 12, 24):
        co2 = a * (1 - np.exp(-(t - 0.5) / 7.0)) if t > 0.5 else 0.0
        evap = 0.030 * t
        my = m_yeast0 - co2 - evap + rng.normal(0, 0.05)
        mc = m_ctrl0 - evap + rng.normal(0, 0.05)
        lines.append(f"{t},{np.round(my, 1):.1f},{np.round(mc, 1):.1f}")
    (HERE / "fermentation_example.csv").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    osmosis()
    fermentation()
    print("wrote osmosis_example.csv and fermentation_example.csv")
