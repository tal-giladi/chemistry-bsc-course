"""Lesson 02.4 hands-on: when does the small-x approximation for a weak acid break?

For HA with acid constant Ka at formal concentration C, x = [H+] solves x^2 + Ka x - Ka C = 0
(water's own H+ ignored). The small-x shortcut drops x next to C and gives x = sqrt(Ka C).
Fill in the two TODO functions, then run:   py lesson04_small_x.py
The plot is saved to runs/lesson04_small_x.png next to this file.
Reference solution: lesson04_small_x_solution.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
KA_ACETIC = 1.8e-5  # OpenStax Chemistry 2e, section 14.3


def x_exact(Ka, C):
    """Positive root of x^2 + Ka x - Ka C = 0.
    TODO: (-Ka + sqrt(Ka^2 + 4 Ka C)) / 2, with np.sqrt so arrays work."""
    return None


def x_small(Ka, C):
    """Small-x approximation.
    TODO: sqrt(Ka C)."""
    return None


def main():
    C = np.logspace(-5, 0, 200)          # mol/L, from 1e-5 to 1 M
    xe, xa = x_exact(KA_ACETIC, C), x_small(KA_ACETIC, C)
    if xe is None or xa is None:
        print("TODO: write x_exact() and x_small() first.")
        return
    rel_err = (xa - xe) / xe
    dpH = -np.log10(xa) + np.log10(xe)
    ratio = xe / C

    print("   C (M)    x/C     error in [H+]   error in pH")
    for c0 in (1.0, 0.1, 0.01, 1e-3, 1e-4):
        i = np.argmin(abs(C - c0))
        print(f"{C[i]:8.0e}  {ratio[i]:6.1%}   {rel_err[i]:+8.1%}       {dpH[i]:+.3f}")
    i5 = np.argmax(ratio < 0.05)        # first C where x/C drops below 5 %
    print(f"x/C falls below 5 % for C above about {C[i5]:.1e} M "
          f"(rule of thumb C/Ka > {C[i5] / KA_ACETIC:.0f})")
    print(f"Taylor estimate of the error: 0.5*sqrt(Ka/C) at C = 0.1 M is {0.5 * np.sqrt(KA_ACETIC / 0.1):.2%}")

    (HERE / "runs").mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    ax.semilogx(C, 100 * rel_err, label="error of sqrt(Ka C), %")
    ax.semilogx(C, 100 * ratio, "--", label="x / C, %")
    ax.axhline(5, color="grey", lw=0.8)
    ax.set_xlabel("formal concentration C (mol/L)")
    ax.set_ylabel("percent")
    ax.set_title("acetic acid, Ka = 1.8e-5")
    ax.legend()
    fig.tight_layout()
    fig.savefig(HERE / "runs" / "lesson04_small_x.png", dpi=120)
    print("plot saved to runs/lesson04_small_x.png")


if __name__ == "__main__":
    main()
