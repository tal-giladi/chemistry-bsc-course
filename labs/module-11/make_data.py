"""Make the simulated data sets for lesson 11.3 (fixed seeds, so the files are reproducible).

class_vinegar.csv   : six learners, five home vinegar titrations each (as in lesson 10.6), acetic acid in % w/w.
                      Model: true value 4.95 % w/w; repeatability SD 0.02 % (0.01 g scale) or 0.06 % (0.1 g scale);
                      learner D skipped the indicator blank (+0.06 % bias); learner C spilled in trial 4 (-0.25 %).
titration_curve.csv : potentiometric titration of 10.00 mL diluted vinegar (0.0830 mol/L acetic acid) with
                      0.1000 mol/L NaOH, exact charge balance with pKa 4.757 (Harvey, Analytical Chemistry 2.1,
                      Appendix 11), pH noise SD 0.02. Equivalence at 8.30 mL.
Simulated, not measured. Run: py make_data.py
"""
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
TRUE = 4.95
KA = 10 ** -4.757
KW = 1.0e-14


def class_vinegar():
    rng = np.random.default_rng(1103)
    rows = []
    learners = {"A": (0.02, 0.0, 0.01), "B": (0.02, 0.0, 0.01), "C": (0.02, 0.0, 0.01),
                "D": (0.02, 0.06, 0.01), "E": (0.02, 0.0, 0.01), "F": (0.06, 0.0, 0.1)}
    for name, (sd, bias, res) in learners.items():
        for trial in range(1, 6):
            x = TRUE + bias + rng.normal(0, sd)
            if name == "C" and trial == 4:
                x -= 0.25
            rows.append(f"{name},{trial},{x:.3f},{'no' if name == 'D' else 'yes'},{res}")
    head = ("# Simulated (make_data.py, seed 1103): true value 4.95 % w/w. Not measured.\n"
            "learner,trial,acid_percent_ww,blank_corrected,scale_resolution_g\n")
    (HERE / "class_vinegar.csv").write_text(head + "\n".join(rows) + "\n", encoding="utf-8", newline="\n")


def ph_at(v_ml, ca=0.0830, va=10.00, cb=0.1000):
    """Exact pH from the charge balance [H+] + [Na+] = [OH-] + [A-]."""
    vt = va + v_ml
    c_acid = ca * va / vt
    c_na = cb * v_ml / vt

    def f(log_h):
        h = 10 ** log_h
        return h + c_na - KW / h - c_acid * KA / (KA + h)

    return -brentq(f, -14, 0)


def titration_curve():
    rng = np.random.default_rng(1104)
    v = np.concatenate([np.arange(0, 7.0, 0.5), np.arange(7.0, 9.6, 0.1), np.arange(10.0, 14.01, 0.5)])
    ph = np.array([ph_at(x) for x in v]) + rng.normal(0, 0.02, v.size)
    head = ("# Simulated (make_data.py, seed 1104): 10.00 mL of 0.0830 mol/L acetic acid + 0.1000 mol/L NaOH;"
            " equivalence 8.30 mL. Not measured.\nV_NaOH_mL,pH\n")
    body = "\n".join(f"{a:.2f},{b:.3f}" for a, b in zip(v, ph))
    (HERE / "titration_curve.csv").write_text(head + body + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    class_vinegar()
    titration_curve()
    print("wrote class_vinegar.csv and titration_curve.csv")
