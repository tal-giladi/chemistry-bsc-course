"""Generate the example data for the Module 8 labs (seeded, so the files never change).

Run:   py make_data.py
The models and their true parameters are written here so you can check your answers.
The data are realistic but NOT measured. Replace them with your own measurements.
"""
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
rng = np.random.default_rng(808)
C_WATER = 4.184   # J/(g K)


def write(name, lines):
    (HERE / name).write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def lemon_cell():
    """Lesson 08.6. A galvanised nail (zinc) and a copper wire or coin, 2-3 cm apart, in three
    electrolytes, measured with a multimeter across load resistors (R = 'open' means no load).
    Model: V = E R / (R + r). True values (E in V, r in ohm):
      lemon 0.93 V, 1800 ohm; vinegar 0.89 V, 2500 ohm; salt water (1 tsp in 100 mL) 0.78 V, 900 ohm.
    Multimeter reading noise sd 0.004 V; 3 decimals."""
    cells = {"lemon": (0.93, 1800.0), "vinegar": (0.89, 2500.0), "salt water": (0.78, 900.0)}
    loads = [100, 220, 470, 1000, 2200, 4700, 10000, None]
    lines = ["electrolyte,R_ohm,V_V"]
    for name, (e, r) in cells.items():
        for load in loads:
            v = e if load is None else e * load / (load + r)
            v += rng.normal(0, 0.004)
            lines.append(f"{name},{'open' if load is None else load},{v:.3f}")
    write("lemon_cell_example.csv", lines)


def calorimetry():
    """Lesson 08.7. Two nested foam cups with a lid, 22.0 C room.
    Run 'calibration': 100.0 g water at about 21.0 C in the cup; at t = 180 s add 50.0 g hot water,
    measured at 45.0 C just before pouring (it loses 0.5 K while pouring, a real systematic error).
    Run 'dissolution': 100.0 g water at about 22.5 C; at t = 180 s add 5.00 g NaHCO3; it dissolves
    with a time constant of 40 s. True integral heat of solution at this concentration +17.5 kJ/mol
    (a little below the infinite-dilution value +19.6 from the tables).
    True cup heat capacity C_CUP = 30 J/K. Heat leak: dT/dt = -k (T - T_room), k = 1.0e-4 per s.
    Thermometer resolution 0.1 C, noise sd 0.03 C. Reading every 30 s for 12 min."""
    c_cup, k, t_room = 30.0, 1.0e-4, 22.0
    dt = 1.0
    t_read = np.arange(0, 721, 30)
    lines = ["run,t_s,T_C"]

    # calibration: heat capacity before and after mixing changes
    temp = 21.0
    heat_cap = 100.0 * C_WATER + c_cup
    rows = []
    for t in np.arange(0, 721, dt):
        if t == 180:
            t_hot = 45.0 - 0.5
            heat_cap_new = heat_cap + 50.0 * C_WATER
            temp = (heat_cap * temp + 50.0 * C_WATER * t_hot) / heat_cap_new
            heat_cap = heat_cap_new
        temp += -k * (temp - t_room) * dt
        if t in t_read:
            rows.append((t, temp))
    for t, temp_t in rows:
        lines.append(f"calibration,{int(t)},{np.round(temp_t + rng.normal(0, 0.03), 1):.1f}")

    # dissolution: heat absorbed q_total spread over the dissolving time
    n = 5.00 / 84.006
    q_total = n * 17500.0            # J absorbed by the dissolving salt
    heat_cap = 100.0 * C_WATER + c_cup + 5.00 * 1.0   # salt adds a little (c about 1 J/(g K))
    temp = 22.5
    rows = []
    for t in np.arange(0, 721, dt):
        if t >= 180:
            frac_rate = np.exp(-(t - 180) / 40.0) / 40.0
            temp -= q_total * frac_rate * dt / heat_cap
        temp += -k * (temp - t_room) * dt
        if t in t_read:
            rows.append((t, temp))
    for t, temp_t in rows:
        lines.append(f"dissolution,{int(t)},{np.round(temp_t + rng.normal(0, 0.03), 1):.1f}")
    write("calorimetry_example.csv", lines)


def titration():
    """Lesson 08.7. Titrant: 5.00 g NaHCO3 made up to 100.00 g with water (0.05000 g/g).
    Sample: about 5 g of white vinegar weighed into a cup, 20 mL water and 2 mL cabbage indicator.
    True acetic acid content 4.95 % by mass. The titrant is delivered from a 10 mL syringe weighed
    before and after (pocket scale, 0.01 g). End point: first lasting blue-green, which needs a small
    excess of bicarbonate: on average 0.08 g of titrant, sd 0.05 g, plus scale noise sd 0.005 g."""
    w_titrant = 5.00 / 100.00 / 84.006       # mol NaHCO3 per g titrant
    lines = ["trial,m_vinegar_g,m_syringe_before_g,m_syringe_after_g"]
    for trial in (1, 2, 3):
        m_v = np.round(rng.uniform(4.90, 5.10), 2)
        n_acid = m_v * 0.0495 / 60.052
        m_titrant = n_acid / w_titrant + rng.normal(0.08, 0.05)
        before = np.round(rng.uniform(15.0, 16.5), 2)
        after = np.round(before - m_titrant + rng.normal(0, 0.005), 2)
        lines.append(f"{trial},{m_v:.2f},{before:.2f},{after:.2f}")
    write("titration_example.csv", lines)


if __name__ == "__main__":
    lemon_cell()
    calorimetry()
    titration()
    print("wrote lemon_cell_example.csv, calorimetry_example.csv, titration_example.csv")
