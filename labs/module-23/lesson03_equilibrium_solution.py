"""Lesson 23.3 (reference solution): the formation constant of FeSCN2+ by spectrophotometry.

Run from this folder:
    py lesson03_equilibrium.py                  (uses fescn_example.csv)
    py lesson03_equilibrium.py my_fescn.csv     (your simulation export: columns type,Fe0_M,SCN0_M,A447;
                                                 type = standard, mix or job; 1 cm cell)
Steps: (1) calibration line from the standards (large excess of Fe3+); (2) [FeSCN2+] in each mixture from
its absorbance, then an ICE table and K for each mixture; (3) correct the calibration for the small part of
SCN- the standards did NOT complex, and iterate; (4) a Job plot to confirm the 1:1 ratio.
Writes runs/lesson03_equilibrium.png.
"""
import sys
from pathlib import Path

import numpy as np

from pc23 import HERE, read_csv, column, linfit, t95, todo, save_plot, pyplot


def k_from_mixture(A, eps_b, Fe0, SCN0):
    """K = [FeSCN] / ([Fe3+][SCN-]) with [FeSCN] = A / (eps b) and the ICE table
    [Fe3+] = Fe0 - x, [SCN-] = SCN0 - x. Works on arrays.
    TODO: three lines."""
    x = A / eps_b
    return x / ((Fe0 - x) * (SCN0 - x))


def fraction_complexed(K, Fe0):
    """Fraction of SCN- present as FeSCN2+ in a standard with Fe3+ in large excess: K Fe0 / (1 + K Fe0).
    TODO: one line."""
    return K * Fe0 / (1 + K * Fe0)


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "fescn_example.csv"
    rows = read_csv(path)
    typ = np.array([r["type"] for r in rows])
    Fe0, SCN0, A = column(rows, "Fe0_M"), column(rows, "SCN0_M"), column(rows, "A447")
    if todo(k_from_mixture(np.array([0.1]), 1.0, 1.0, 1.0), fraction_complexed(1.0, 1.0)):
        return

    st, mx, jb = typ == "standard", typ == "mix", typ == "job"
    a, b, sa, sb, _, s = linfit(SCN0[st], A[st])
    print(f"calibration: A = {a:.4f} + {b:.0f} [SCN-]0   (s_b = {sb:.0f}, s_y = {s:.4f})")
    print(f"  apparent eps*b = {b:.0f} L/mol (1 cm cell)")

    K = k_from_mixture(A[mx] - a, b, Fe0[mx], SCN0[mx])
    print("naive K per mixture (standards assumed 100 % complexed):", ", ".join(f"{k:.0f}" for k in K))
    Kmean = K.mean()
    fe_std = Fe0[st][0]
    for it in range(1, 20):
        eps_b = b / fraction_complexed(Kmean, fe_std)
        K = k_from_mixture(A[mx] - a, eps_b, Fe0[mx], SCN0[mx])
        if abs(K.mean() - Kmean) < 0.01:
            break
        Kmean = K.mean()
    sd = K.std(ddof=1)
    ci = t95(len(K) - 1) * sd / np.sqrt(len(K))
    print(f"after correction ({it} iterations): {fraction_complexed(Kmean, fe_std):.1%} of SCN- complexed in "
          f"the standards, eps*b = {eps_b:.0f} L/mol")
    print("  K per mixture:", ", ".join(f"{k:.0f}" for k in K))
    print(f"  K = {K.mean():.0f}, SD {sd:.0f}, 95 % CI +/- {ci:.0f}")
    trend = np.polyfit(SCN0[mx], K, 1)[0] * (SCN0[mx].max() - SCN0[mx].min())
    print(f"  drift of K across the series: {trend:+.0f} (a large trend means a wrong model)")

    if jb.any():
        x = Fe0[jb] / (Fe0[jb] + SCN0[jb])
        print(f"Job plot: maximum absorbance at x(Fe) = {x[np.argmax(A[jb])]:.1f} (1:1 complex -> 0.5)")

    plt = pyplot()
    if plt is None:
        return
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.6))
    a1.plot(SCN0[st] * 1e4, A[st], "o", label="standards")
    xx = np.linspace(0, SCN0[st].max(), 50)
    a1.plot(xx * 1e4, a + b * xx, "--")
    a1.set_xlabel("[SCN-]0 (1e-4 M)")
    a1.set_ylabel("A at 447 nm")
    a1.legend()
    if jb.any():
        a2.plot(Fe0[jb] / (Fe0[jb] + SCN0[jb]), A[jb], "o-")
        a2.set_xlabel("mole fraction of Fe3+")
        a2.set_ylabel("A at 447 nm")
        a2.set_title("Job plot")
    save_plot(fig, "lesson03_equilibrium.png")


if __name__ == "__main__":
    main()
