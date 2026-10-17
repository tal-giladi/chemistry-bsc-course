"""Lesson 10.5 reference solution: fluoride ion-selective electrode calibration, standard addition,
and water hardness from bottled-water labels and a soap-lather test.

Run:   py lesson05_ise_solution.py
       py lesson05_ise_solution.py my_ise.csv my_soap.csv
ISE file columns: kind,label,c_mg_L,E_mV  (kind = standard, sample, addition_before, addition_after).
Soap file columns: water,ca_mg_L,mg_mg_L,drops  (leave ca and mg empty for unknown waters).
Standards and samples are mixed 1:1 with TISAB; concentrations refer to the solution before TISAB.
"""
import csv
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
NERNST_25C = 59.16           # mV per decade for a 1- ion at 25 C
LINEAR_FROM = 0.5            # mg/L, lowest standard used in the straight-line fit
ADDITION = {"v_x": 50.0, "v_tisab": 50.0, "v_s": 1.00, "c_s": 100.0}   # mL, mL, mL, mg/L


def fit_calibration(logc, e):
    """Straight-line fit E = intercept + slope * log10(c). Return (slope, intercept)."""
    slope, intercept = np.polyfit(logc, e, 1)
    return float(slope), float(intercept)


def standard_addition(e1, e2, slope, c_s, v_s, v_x, v_t):
    """Concentration of the sample from one standard addition.
    Before: v_x mL of sample in v_t mL total (sample + TISAB), c1 = c_x v_x / v_t.
    After adding v_s mL of standard c_s: c2 = (c_x v_x + c_s v_s) / (v_t + v_s).
    The electrode gives R = c2 / c1 = 10**((e2 - e1) / slope). Solve for c_x:
    c_x = c_s v_s / ((v_t + v_s) v_x (R / v_t - 1 / (v_t + v_s)))."""
    r = 10.0 ** ((e2 - e1) / slope)
    return c_s * v_s / ((v_t + v_s) * v_x * (r / v_t - 1.0 / (v_t + v_s)))


def hardness(ca_mg_l, mg_mg_l):
    """Hardness in mg/L as CaCO3 from Ca and Mg in mg/L (100.09/40.08 and 100.09/24.31)."""
    return 2.497 * ca_mg_l + 4.118 * mg_mg_l


def read_rows(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main():
    if fit_calibration(np.array([0.0, 1.0]), np.array([0.0, -59.0])) is None or \
            standard_addition(-40.0, -70.0, -59.0, 100.0, 1.0, 50.0, 100.0) is None:
        print("TODO: write fit_calibration() and standard_addition() first.")
        return
    ise_path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "fluoride_ise_example.csv"
    soap_path = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "soap_test_example.csv"
    rows = read_rows(ise_path)
    std = [(float(r["c_mg_L"]), float(r["E_mV"])) for r in rows if r["kind"] == "standard"]
    c = np.array([s[0] for s in std])
    e = np.array([s[1] for s in std])
    lin = c >= LINEAR_FROM
    slope, icpt = fit_calibration(np.log10(c[lin]), e[lin])
    print(f"Fluoride ISE: slope {slope:.1f} mV/decade ({100 * abs(slope) / NERNST_25C:.0f} % of Nernstian), "
          f"intercept {icpt:.1f} mV, fit on {lin.sum()} standards >= {LINEAR_FROM} mg/L")
    for ci, ei in zip(c, e):
        print(f"  standard {ci:6.2f} mg/L  E {ei:7.1f} mV  residual {ei - (icpt + slope * math.log10(ci)):+5.1f} mV")
    for r in rows:
        if r["kind"] == "sample":
            cx = 10 ** ((float(r["E_mV"]) - icpt) / slope)
            flag = "" if cx >= LINEAR_FROM else "  (below the linear range: biased high, use low-level method)"
            print(f"  sample {r['label']}: {cx:.3f} mg/L{flag}")
    e1 = next(float(r["E_mV"]) for r in rows if r["kind"] == "addition_before")
    e2 = next(float(r["E_mV"]) for r in rows if r["kind"] == "addition_after")
    a = ADDITION
    cx = standard_addition(e1, e2, slope, a["c_s"], a["v_s"], a["v_x"], a["v_x"] + a["v_tisab"])
    print(f"  standard addition on A: dE = {e2 - e1:.1f} mV -> {cx:.3f} mg/L")

    soap = read_rows(soap_path)
    known = [(hardness(float(r["ca_mg_L"]), float(r["mg_mg_L"])), float(r["drops"])) for r in soap if r["ca_mg_L"]]
    h = np.array([k[0] for k in known])
    d = np.array([k[1] for k in known])
    m, b = np.polyfit(h, d, 1)
    print(f"Soap test: drops = {b:.1f} + {m:.4f} x hardness (from {len(known)} bottled-water readings)")
    for name in dict.fromkeys(r["water"] for r in soap):
        ds = [float(r["drops"]) for r in soap if r["water"] == name]
        lab = [r for r in soap if r["water"] == name][0]
        label = f"label {hardness(float(lab['ca_mg_L']), float(lab['mg_mg_L'])):.0f}" if lab["ca_mg_L"] else "unknown"
        print(f"  {name:20s} mean {np.mean(ds):5.1f} drops -> about {(np.mean(ds) - b) / m:4.0f} mg/L as CaCO3 ({label})")


if __name__ == "__main__":
    main()
