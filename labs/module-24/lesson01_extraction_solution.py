"""Lesson 24.1 - planning an extraction work-up on paper before the bench.

Reference solution for lesson01_extraction.py.  Run:  py lesson01_extraction_solution.py
Writes runs/lesson01_extraction.png.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from org24 import ACIDS, runs_dir


def fraction_left(D, V_aq, V_org, n=1):
    """Fraction of solute left in the water after n extractions, each with fresh V_org (lesson 19.3)."""
    # TODO: q1 = V_aq / (D V_org + V_aq); return q1 ** n
    q1 = V_aq / (D * V_org + V_aq)
    return q1 ** n


def distribution_ratio(K_D, pH, pKa):
    """D for a weak acid HA when only neutral HA dissolves in the organic layer."""
    # TODO: h = 10**-pH, Ka = 10**-pKa; return K_D * h / (h + Ka)
    h, Ka = 10.0 ** (-pH), 10.0 ** (-pKa)
    return K_D * h / (h + Ka)


def fraction_into_organic_from_organic(D, V_org, V_aq, n=1):
    """Washing an ORGANIC layer with n portions of water of volume V_aq each:
    fraction of solute that stays in the organic layer.  One wash keeps D V_org / (D V_org + V_aq)."""
    # TODO: keep1 = D V_org / (D V_org + V_aq); return keep1 ** n
    keep1 = D * V_org / (D * V_org + V_aq)
    return keep1 ** n


def main():
    if fraction_left(4, 100, 30) is None or distribution_ratio(10, 2, 4) is None \
            or fraction_into_organic_from_organic(1, 1, 1) is None:
        print("TODO: write fraction_left(), distribution_ratio() and fraction_into_organic_from_organic() first.")
        return

    # 1. One 30 mL portion or three 10 mL portions (D = 4, 100 mL water)
    one = fraction_left(4, 100, 30, 1)
    three = fraction_left(4, 100, 10, 3)
    print(f"D = 4: one 30 mL extraction leaves {100 * one:.1f} %, three 10 mL leave {100 * three:.1f} %")

    # 2. Acid-base work-up: benzoic acid in 50 mL ether, washed with 3 x 15 mL of base or of water
    pKa, logK = ACIDS["benzoic acid"]
    K_D = 10 ** logK
    for label, pH in (("water, pH 3", 3.0), ("NaHCO3(aq), pH 8.3", 8.3), ("NaOH(aq), pH 13", 13.0)):
        D = distribution_ratio(K_D, pH, pKa)
        keep = fraction_into_organic_from_organic(D, 50, 15, 3)
        print(f"benzoic acid, wash with {label:20s}: D = {D:9.4g}; stays in ether after 3 washes: {100 * keep:.3g} %")

    # 3. Recover it: acidify the combined basic washes (45 mL) to pH 1, extract with 2 x 20 mL ether
    D1 = distribution_ratio(K_D, 1.0, pKa)
    recovered = 1 - fraction_left(D1, 45, 20, 2)
    print(f"after acidifying to pH 1: D = {D1:.1f}; 2 x 20 mL ether recover {100 * recovered:.2f} %")

    # Plot: D against pH for the three acids of this module
    pH = np.linspace(0, 10, 201)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 4))
    for name, (pk, lk) in ACIDS.items():
        a1.semilogy(pH, distribution_ratio(10 ** lk, pH, pk), label=f"{name} (pKa {pk})")
    a1.axhline(1, color="grey", lw=0.8)
    a1.set_xlabel("pH of the water layer")
    a1.set_ylabel("distribution ratio D (organic/water)")
    a1.legend(fontsize=8)
    n = np.arange(1, 7)
    a2.plot(n, [100 * fraction_left(4, 100, 30 / k, k) for k in n], "o-")
    a2.set_xlabel("number of portions (30 mL total)")
    a2.set_ylabel("% left in 100 mL water (D = 4)")
    fig.tight_layout()
    out = runs_dir() / "lesson01_extraction.png"
    fig.savefig(out, dpi=120)
    print("plot:", out)


if __name__ == "__main__":
    main()
