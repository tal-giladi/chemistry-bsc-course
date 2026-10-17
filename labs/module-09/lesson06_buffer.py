"""Lesson 09.6: buffer capacity and a gravimetric calculation.

Fill in the two TODOs, then run (from this folder):
    py lesson06_buffer.py
Reference solution: lesson06_buffer_solution.py
"""
import math
from pathlib import Path

import numpy as np
from scipy.optimize import brentq
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
RUNS = HERE / "runs"
KW = 1.0e-14
KA = 10 ** -4.757          # acetic acid (Harvey, Appendix 11)
KSP_AGCL = 1.8e-10         # Harvey, Appendix 10
M_AGCL, M_CL = 143.32, 35.45


def beta(ph, c_total, ka=KA):
    """Buffer capacity (mol/L per pH unit) of a weak acid HA + A- with total concentration c_total, plus water:
    beta = 2.303 ([H3O+] + [OH-] + C Ka [H3O+] / (Ka + [H3O+])^2)."""
    h = 10.0 ** -ph
    # TODO 1: return the buffer capacity from the formula in the docstring (KW / h is [OH-]).
    raise NotImplementedError("TODO 1")


def ph_exact(n_ha, n_a, n_na_extra, v_l, ka=KA):
    """Exact pH of HA/A- (amounts in mol) in v_l litres, with n_na_extra = net strong base added (negative = acid).
    Charge balance: [Na+] + [H3O+] = [OH-] + [A-] (+ [Cl-] if strong acid was added)."""
    c_t = (n_ha + n_a) / v_l
    na = (n_a + max(n_na_extra, 0)) / v_l
    cl = max(-n_na_extra, 0) / v_l
    f = lambda p: na + 10 ** -p - KW / 10 ** -p - cl - c_t * ka / (ka + 10 ** -p)
    return brentq(f, 0, 14)


def main():
    RUNS.mkdir(exist_ok=True)
    pka = -math.log10(KA)
    for c in (0.10, 0.010):
        print(f"Acetate buffer, total {c} mol/L: beta at pH = pKa ({pka:.2f}) = {beta(pka, c):.4f} mol/L per pH;"
              f" at pKa + 1 = {beta(pka + 1, c):.4f}; at pKa + 2 = {beta(pka + 2, c):.5f}")

    print("\nAdd 1.00 mmol HCl to 100.0 mL of 0.100 M acetate buffer (5.00 mmol HA + 5.00 mmol A-):")
    v = 0.1000
    before = ph_exact(5.00e-3, 5.00e-3, 0, v)
    after = ph_exact(5.00e-3, 5.00e-3, -1.00e-3, v)
    hh = pka + math.log10(4.00 / 6.00)
    print(f"   exact pH {before:.3f} -> {after:.3f} (change {after - before:+.3f}); Henderson-Hasselbalch {hh:.3f}")
    water = -math.log10(1.00e-3 / v)
    print(f"   the same HCl in 100.0 mL of pure water: pH 7.00 -> {water:.2f}")

    print("\nGravimetric chloride: 0.2500 g sample gives 0.6012 g AgCl")
    # TODO 2: mass of chloride (g) = mass of AgCl times the gravimetric factor M(Cl) / M(AgCl).
    m_cl = None
    print(f"   gravimetric factor M(Cl)/M(AgCl) = {M_CL / M_AGCL:.5f}; chloride = {1000 * m_cl:.1f} mg = {100 * m_cl / 0.2500:.2f} %")
    s_pure = math.sqrt(KSP_AGCL)
    s_common = KSP_AGCL / 0.010
    for label, s in (("pure water", s_pure), ("0.010 M chloride (common ion)", s_common)):
        print(f"   AgCl dissolved by 200 mL of {label}: {1000 * s * 0.200 * M_AGCL:.4f} mg")

    ph = np.linspace(2, 12, 400)
    fig, ax = plt.subplots(figsize=(6, 4))
    for c in (0.10, 0.010):
        ax.plot(ph, beta(ph, c), label=f"acetate, {c} mol/L")
    ax.plot(ph, beta(ph, 0.0), "--", label="water only")
    ax.set(xlabel="pH", ylabel="buffer capacity (mol/L per pH)", yscale="log", title="Buffer capacity")
    ax.legend()
    fig.tight_layout()
    fig.savefig(RUNS / "lesson06_buffer.png", dpi=120)
    print("plot written to runs/lesson06_buffer.png")


if __name__ == "__main__":
    main()
