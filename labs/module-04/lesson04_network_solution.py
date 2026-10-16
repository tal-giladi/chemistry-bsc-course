"""Lesson 04.4 reference solution: predict the voltages in a resistor network and compare with a multimeter.

Circuit (battery minus is 0 V):
    battery + --R1-- A --R3-- B
                     |        |
                     R2       R4
                     |        |
    battery - -------+--------+

Run:   py lesson04_network_solution.py                 (example data)
       py lesson04_network_solution.py my_network.csv  (your own data, same format as network_example.csv)
"""
import csv
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent


def read_values(path):
    """Return {quantity: float} from a CSV with columns quantity,value,note."""
    with open(path, newline="", encoding="utf-8") as f:
        return {row["quantity"]: float(row["value"]) for row in csv.DictReader(f)}


def equivalent_resistance(R1, R2, R3, R4):
    """Series and parallel rules: R1 in series with (R2 parallel to (R3 + R4))."""
    r34 = R3 + R4
    return R1 + R2 * r34 / (R2 + r34)


def node_voltages(Vs, R1, R2, R3, R4):
    """Kirchhoff's current law at nodes A and B, written as a 2x2 linear system G v = b
    (conductances G = 1/R), solved with numpy (the linear-systems method of Module 3)."""
    g1, g2, g3, g4 = 1 / R1, 1 / R2, 1 / R3, 1 / R4
    G = np.array([[g1 + g2 + g3, -g3],
                  [-g3, g3 + g4]])
    b = np.array([g1 * Vs, 0.0])
    return np.linalg.solve(G, b)


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "network_example.csv"
    d = read_values(path)
    Vs, R = d["Vs_V"], [d[f"R{i}_ohm"] for i in (1, 2, 3, 4)]
    VA, VB = node_voltages(Vs, *R)
    Req = equivalent_resistance(*R)
    I_total = Vs / Req
    print(f"equivalent resistance  = {Req:.1f} ohm, battery current = {I_total * 1e3:.2f} mA")
    print(f"from node voltages     : battery current = {(Vs - VA) / R[0] * 1e3:.2f} mA (must agree)")
    for name, pred in (("VA", VA), ("VB", VB)):
        meas = d.get(f"{name}_V")
        line = f"{name}: predicted {pred:.3f} V"
        if meas is not None:
            line += f", measured {meas:.3f} V, difference {(meas - pred) * 1e3:+.1f} mV ({(meas / pred - 1) * 100:+.2f} %)"
        print(line)
    drops = {"R1": Vs - VA, "R2": VA, "R3": VA - VB, "R4": VB}
    for (k, v), r in zip(drops.items(), R):
        print(f"{k}: {v:.3f} V, {v / r * 1e3:.2f} mA, {v * v / r * 1e3:.1f} mW (rating 250 mW)")


if __name__ == "__main__":
    main()
