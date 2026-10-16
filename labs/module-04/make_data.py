"""Generate the example data for the Module 4 labs (seeded, so the files never change).

Run:   py make_data.py
The models and their true parameters are written here so you can check your answers.
The data are realistic but NOT measured. Replace them with your own measurements.
"""
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
rng = np.random.default_rng(404)

# CODATA 2022 exact constants (NIST)
H = 6.62607015e-34
C = 299792458.0
E = 1.602176634e-19


def pendulum():
    """Keys on a string. True g = 9.795 m/s^2 (about right for Israel at sea level).
    Small-angle period plus a tiny finite-amplitude effect (10 degrees: +0.19 %).
    The length is measured to the centre of the keys with a +/- 3 mm tape error.
    Each trial: time for 20 swings with a hand stopwatch (reaction-time noise sd 0.15 s)."""
    g = 9.795
    lines = ["L_m,trial,t20_s"]
    for L in (0.30, 0.45, 0.60, 0.75, 0.90):
        L_true = L + rng.normal(0, 0.003)
        T = 2 * np.pi * np.sqrt(L_true / g) * 1.0019
        for trial in (1, 2, 3):
            t20 = 20 * T + rng.normal(0, 0.15)
            lines.append(f"{L:.2f},{trial},{t20:.2f}")
    (HERE / "pendulum_example.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")


def network():
    """Resistor ladder on a breadboard, two fresh AA cells.
    Nominal 220, 470, 330, 1000 ohm (5 % tolerance); true values drawn inside tolerance.
    Meter: 3.5-digit, reading noise about 1 count. Battery: EMF 3.12 V, internal resistance 0.4 ohm."""
    nominal = {"R1": 220.0, "R2": 470.0, "R3": 330.0, "R4": 1000.0}
    true = {k: v * (1 + rng.uniform(-0.03, 0.03)) for k, v in nominal.items()}
    emf, r_int = 3.12, 0.4
    # node analysis with the true values (A after R1, B after R3)
    g1, g2, g3, g4 = (1 / true[k] for k in ("R1", "R2", "R3", "R4"))
    gi = 1 / (true["R1"] + r_int)  # internal resistance in series with R1
    M = np.array([[gi + g2 + g3, -g3], [-g3, g3 + g4]])
    b = np.array([gi * emf, 0.0])
    va, vb = np.linalg.solve(M, b)
    i_batt = (emf - va) / (true["R1"] + r_int)
    v_term = emf - i_batt * r_int
    rows = [
        ("Vs_V", round(v_term + rng.normal(0, 0.001), 3), "battery terminal voltage with the network connected"),
    ]
    for k in ("R1", "R2", "R3", "R4"):
        rows.append((f"{k}_ohm", round(true[k] + rng.normal(0, 0.1), 1), f"measured out of circuit; nominal {nominal[k]:.0f} ohm"))
    rows.append(("VA_V", round(va + rng.normal(0, 0.001), 3), "node A to battery minus"))
    rows.append(("VB_V", round(vb + rng.normal(0, 0.001), 3), "node B to battery minus"))
    lines = ["quantity,value,note"] + [f"{q},{v},{n}" for q, v, n in rows]
    (HERE / "network_example.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")


def led():
    """Four LEDs, each in series with a 150 ohm resistor and a 1 kohm potentiometer, three AA cells.
    LED model: I = (w / Rs) * ln(1 + exp((V - V0) / w)), a smooth knee that becomes a straight
    line of slope 1/Rs above the turn-on voltage V0. True V0 = h c / (e lambda) - 0.04 V plus a
    small LED-to-LED scatter (sd 0.02 V). Meter noise 1 mV on both readings."""
    R = 150.0
    leds = [("red", 630, 13.0, 0.045), ("amber", 595, 14.0, 0.045),
            ("yellow-green", 570, 16.0, 0.05), ("blue", 470, 18.0, 0.06)]
    lines = ["led,lambda_nm,R_ohm,V_led_V,V_res_V"]
    for name, lam, rs, w in leds:
        v0 = H * C / (E * lam * 1e-9) - 0.04 + rng.normal(0, 0.02)
        imax = (4.5 - v0 - 0.3) / R
        for i in np.linspace(0.0002, imax, 14):
            # invert the model: V = V0 + w ln(exp(I Rs / w) - 1)
            v = v0 + w * np.log(np.expm1(i * rs / w))
            lines.append(f"{name},{lam},{R:.0f},{v + rng.normal(0, 0.001):.3f},{i * R + rng.normal(0, 0.001):.3f}")
    (HERE / "led_example.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    pendulum()
    network()
    led()
    print("wrote pendulum_example.csv, network_example.csv, led_example.csv")
