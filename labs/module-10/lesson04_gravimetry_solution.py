"""Lesson 10.4 reference solution: heating to constant mass (baking soda in a kitchen oven),
gravimetric factors, coulometry and electrogravimetry with Faraday's law.

Run:   py lesson04_gravimetry_solution.py
       py lesson04_gravimetry_solution.py my_oven.csv   (columns t_min,m_total_g)
Edit TRAY_G to the mass of your empty tray. Reaction: 2 NaHCO3 -> Na2CO3 + H2O + CO2.
"""
import csv
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
F = 96485.33212            # C/mol, CODATA 2022 (exact)
M = {"NaHCO3": 84.006, "Na2CO3": 105.988, "H2O": 18.015, "CO2": 44.009,
     "Cl": 35.453, "AgCl": 143.32, "Cu": 63.546}
TRAY_G = 3.52              # empty foil tray, g
SCALE_D = 0.01             # scale resolution, g
TOL_G = 0.02               # constant mass: two weighings agree within this


def constant_mass(masses, tol):
    """Return the index of the first weighing that agrees with the one before it within tol
    (the sample has reached constant mass), or None if it never does."""
    for i in range(1, len(masses)):
        if abs(masses[i] - masses[i - 1]) <= tol:
            return i
    return None


def moles_from_charge(current_a, time_s, n):
    """Faraday's law at constant current: moles = I t / (n F)."""
    return current_a * time_s / (n * F)


def read_oven(path):
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    return [float(r["t_min"]) for r in rows], [float(r["m_total_g"]) for r in rows]


def main():
    if constant_mass([1.0, 1.0], 0.01) is None or moles_from_charge(1.0, 1.0, 1) is None:
        print("TODO: write constant_mass() and moles_from_charge() first.")
        return
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "oven_example.csv"
    t, m = read_oven(path)
    sample = m[0] - TRAY_G
    i = constant_mass(m[1:], TOL_G)
    if i is None:
        print("not yet at constant mass: heat for another 15 min and weigh again")
        return
    final = m[1:][i]
    loss = m[0] - final
    theory = (M["H2O"] + M["CO2"]) / (2 * M["NaHCO3"])
    u_loss = SCALE_D / math.sqrt(6)                           # difference of two readings
    u_rel = math.hypot(u_loss / loss, u_loss / sample)
    purity = loss / sample / theory
    print(f"sample {sample:.2f} g; constant mass {final:.2f} g reached at {t[1:][i]:.0f} min")
    print(f"mass loss {loss:.2f} g = {100 * loss / sample:.2f} % (theory {100 * theory:.2f} %)")
    print(f"apparent NaHCO3 content {100 * purity:.1f} +/- {100 * purity * u_rel:.1f} % (scale resolution only)")

    gf = M["Cl"] / M["AgCl"]
    m_agcl, v_sample = 0.2856, 0.05000
    print(f"gravimetric factor Cl/AgCl = {gf:.4f}; 0.2856 g AgCl from 50.00 mL -> "
          f"{1000 * m_agcl * gf / v_sample:.0f} mg/L chloride")

    n_oh = moles_from_charge(0.01000, 482.5, 1)
    print(f"coulometric titration: 10.00 mA for 482.5 s generates {n_oh:.4e} mol OH- "
          f"-> HCl in a 10.00 mL sample {n_oh / 0.01000:.5f} mol/L")

    q = 0.500 * 960.0
    m_cu_theory = moles_from_charge(0.500, 960.0, 2) * M["Cu"]
    m_cu = 0.1572
    print(f"electrogravimetry: {q:.0f} C would deposit {m_cu_theory:.4f} g Cu; "
          f"cathode gained {m_cu:.4f} g -> current efficiency {100 * m_cu / m_cu_theory:.1f} %")


if __name__ == "__main__":
    main()
