"""Lesson 04.5 module practical: Planck's constant from LED turn-on voltages.

Circuit per LED: 3 x AA -> potentiometer -> resistor R -> LED -> back to battery minus.
For each potentiometer setting you read V_led (across the LED) and V_res (across R).

Fill in the three TODO functions, then run:
       py lesson05_led_planck.py              (example data)
       py lesson05_led_planck.py my_leds.csv  (header led,lambda_nm,R_ohm,V_led_V,V_res_V)
Reference solution: lesson05_led_planck_solution.py
The plot is saved to runs/lesson05_led_planck.png next to this file.
"""
import csv
import sys
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
H = 6.62607015e-34   # J s, exact (CODATA 2022, NIST)
C = 299792458.0      # m/s, exact
E = 1.602176634e-19  # C, exact


def read_leds(path):
    """Return {led name: (lambda_nm, R_ohm, V_led array, V_res array)}."""
    rows = defaultdict(list)
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows[r["led"]].append(r)
    out = {}
    for name, rs in rows.items():
        out[name] = (float(rs[0]["lambda_nm"]), float(rs[0]["R_ohm"]),
                     np.array([float(r["V_led_V"]) for r in rs]),
                     np.array([float(r["V_res_V"]) for r in rs]))
    return out


def current(V_res, R):
    """Current through the LED from Ohm's law on the series resistor (lesson 04.4).
    TODO: one line."""
    return None


def turn_on_voltage(V, I, frac=0.5):
    """Fit a straight line I = s (V - V0) to the points with I >= frac * max(I), the linear part
    of the curve, and return V0, where the line crosses I = 0.
    TODO: m = I >= frac * I.max(); s, b = np.polyfit(V[m], I[m], 1); solve s*V0 + b = 0."""
    return None


def fit_planck(lam_nm, V0):
    """e V0 = h c / lambda + offset, so V0 against 1/lambda is a line with slope h c / e.
    Return h, its standard uncertainty from the fit, and the intercept in volts.
    TODO: x = 1/lambda in metres^-1; (slope, b), cov = np.polyfit(x, V0, 1, cov=True);
    h = slope * E / C and u_h = sqrt(cov[0, 0]) * E / C."""
    return None


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "led_example.csv"
    leds = read_leds(path)
    lams, V0s = [], []
    (HERE / "runs").mkdir(exist_ok=True)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.5))
    for name, (lam, R, V, Vr) in leds.items():
        I = current(Vr, R)
        V0 = None if I is None else turn_on_voltage(V, I)
        if V0 is None:
            print("TODO: write current() and turn_on_voltage() first.")
            return
        photon_eV = H * C / (lam * 1e-9) / E
        print(f"{name:>13}: lambda = {lam:.0f} nm, photon energy = {photon_eV:.3f} eV, turn-on V0 = {V0:.3f} V")
        lams.append(lam)
        V0s.append(V0)
        a1.plot(V, I * 1e3, "o-", ms=3, label=f"{name} {lam:.0f} nm")
    lams, V0s = np.array(lams), np.array(V0s)
    res = fit_planck(lams, V0s) if len(lams) >= 3 else None
    if len(lams) >= 3 and res is None:
        print("TODO: write fit_planck() last.")
        return
    if res is not None:
        h, u_h, b = res
        print(f"h = {h:.3e} +/- {u_h:.1e} J s   (exact {H:.5e}; difference {(h / H - 1) * 100:+.1f} %)")
        print(f"intercept = {b:+.3f} V (energy lost or gained besides the photon; ideally near 0)")
        x = np.linspace(0, 1 / (lams.min() * 1e-9) * 1.05, 50)
        a2.plot(x * 1e-6, h * C / E * x + b, label=f"fit, h = {h:.2e} J s")
    else:
        print("need at least 3 LEDs of different colours to fit h; with fewer, compare V0 with hc/(e lambda) per LED")
        h = None
    a2.plot(1 / (lams * 1e-9) * 1e-6, V0s, "o", label="turn-on voltages")
    a1.set_xlabel("V across LED (V)")
    a1.set_ylabel("I (mA)")
    a1.legend(fontsize=8)
    a2.set_xlabel("1/lambda (1/um)")
    a2.set_ylabel("V0 (V)")
    a2.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(HERE / "runs" / "lesson05_led_planck.png", dpi=120)
    print("plot saved to runs/lesson05_led_planck.png")


if __name__ == "__main__":
    main()
