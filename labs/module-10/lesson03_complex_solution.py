"""Lesson 10.3 reference solution: a precipitation titration curve from Ksp, the Mohr indicator,
and EDTA conditional formation constants for water hardness.

Run:   py lesson03_complex_solution.py
Constants: Harvey, Analytical Chemistry 2.1, App. 16.10 (Ksp), 16.12 (log K of EDTA complexes)
and 9.3 (EDTA pKa values).
"""
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
KSP = {"AgCl": 1.8e-10, "AgBr": 5.0e-13, "AgI": 8.3e-17}
KSP_AG2CRO4 = 1.2e-12
EDTA_PKA = [0.0, 1.5, 2.0, 2.66, 6.16, 10.24]           # H6Y2+ ... HY3-
LOGK_EDTA = {"Ca2+": 10.69, "Mg2+": 8.79}
M_CACO3 = 100.09                                          # g/mol


def pag_curve(v, c_x, v_x, c_ag, ksp):
    """pAg after v mL of c_ag M AgNO3 is added to v_x mL of c_x M halide X-.
    Mass balance: [Ag+] - [X-] = (c_ag v - c_x v_x) / (v + v_x) = e, and [Ag+][X-] = Ksp,
    so [Ag+] = (e + sqrt(e**2 + 4 Ksp)) / 2. Return -log10([Ag+])."""
    e = (c_ag * v - c_x * v_x) / (v + v_x)
    ag = (e + np.sqrt(e ** 2 + 4 * ksp)) / 2
    return -np.log10(ag)


def alpha_y4(ph):
    """Fraction of all uncomplexed EDTA present as Y4- at this pH.
    With h = [H+] and K1..K6 the successive Ka values (from EDTA_PKA):
    alpha = K1K2K3K4K5K6 / (h^6 + h^5 K1 + h^4 K1K2 + ... + K1K2K3K4K5K6)."""
    h = 10.0 ** -ph
    ks = [10.0 ** -p for p in EDTA_PKA]
    terms, prod = [h ** 6], 1.0
    for i, k in enumerate(ks, start=1):
        prod *= k
        terms.append(prod * h ** (6 - i))
    return terms[-1] / sum(terms)


def main():
    if pag_curve(np.array([1.0]), 0.05, 50.0, 0.1, 1.8e-10) is None or alpha_y4(10.0) is None:
        print("TODO: write pag_curve() and alpha_y4() first.")
        return
    c_cl, v_cl, c_ag = 0.0500, 50.00, 0.1000
    print("50.00 mL of 0.0500 M NaCl with 0.1000 M AgNO3 (V_eq = 25.00 mL)")
    for v in (10.0, 20.0, 24.9, 25.0, 25.1, 30.0):
        print(f"  V = {v:5.1f} mL   pAg = {float(pag_curve(np.array([v]), c_cl, v_cl, c_ag, KSP['AgCl'])[0]):.2f}")

    ag_eq = math.sqrt(KSP["AgCl"])
    print(f"Mohr: [CrO4 2-] for Ag2CrO4 to start exactly at equivalence = {KSP_AG2CRO4 / ag_eq ** 2:.2e} M")
    cro4 = 2.5e-3
    ag_end = math.sqrt(KSP_AG2CRO4 / cro4)
    excess = (ag_end - KSP["AgCl"] / ag_end) * (v_cl + 25.0) / c_ag      # mL of titrant past V_eq
    print(f"  with {cro4:.1e} M chromate, Ag2CrO4 starts at [Ag+] = {ag_end:.2e} M, "
          f"{excess:.3f} mL past V_eq (plus the visible amount: run a blank)")

    print("EDTA: alpha(Y4-) and conditional log K'")
    print(f"  {'pH':>4s} {'alpha':>10s} " + " ".join(f"{m:>10s}" for m in LOGK_EDTA))
    for ph in (7, 8, 9, 10, 11, 12):
        a = alpha_y4(ph)
        print(f"  {ph:4d} {a:10.3e} " + " ".join(f"{lk + math.log10(a):10.2f}" for lk in LOGK_EDTA.values()))
    for ion, lk in LOGK_EDTA.items():
        ph_min = next(p for p in np.arange(4, 13, 0.01) if lk + math.log10(alpha_y4(p)) >= 8.0)
        print(f"  {ion}: log K' reaches 8 (sharp end point) at pH {ph_min:.1f}")

    v_edta, c_edta, v_water = 12.85, 0.01000, 50.00
    hard = c_edta * v_edta / v_water * M_CACO3 * 1000
    print(f"Hardness: {v_edta} mL of {c_edta} M EDTA for {v_water} mL water = {hard:.0f} mg/L as CaCO3")

    v = np.linspace(0.5, 40, 400)
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    for name, ksp in KSP.items():
        ax.plot(v, pag_curve(v, c_cl, v_cl, c_ag, ksp), label=name.replace("Ag", "X = ", 1))
    ax.axhline(-math.log10(ag_end), ls=":", label="Mohr end point, 2.5 mM CrO4 2-")
    ax.set(xlabel="AgNO3 added / mL", ylabel="pAg")
    ax.invert_yaxis()
    ax.legend()
    out = HERE / "runs"
    out.mkdir(exist_ok=True)
    fig.savefig(out / "lesson03_pag.png", dpi=120, bbox_inches="tight")
    print(f"plot: {out / 'lesson03_pag.png'}")


if __name__ == "__main__":
    main()
