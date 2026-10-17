"""Lesson 07.5 reference solution: find the limiting-reagent break point in a vinegar + baking soda series.

Run (from this folder):
    py lesson05_limiting_solution.py                    # example data, saves runs/limiting.png
    py lesson05_limiting_solution.py my_vinegar.csv 50  # your data, vinegar volume in mL
"""
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
M_NAHCO3 = 84.007   # g/mol, PubChem CID 516892
M_CO2 = 44.009      # g/mol, PubChem CID 280
M_ACOH = 60.052     # g/mol, PubChem CID 176


def load(path):
    """Return arrays (m_bicarb_g, mass_loss_g) from a CSV with those two columns."""
    lines = [r for r in Path(path).read_text(encoding="utf-8").splitlines() if r.strip() and not r.startswith("#")]
    data = np.array([[float(v) for v in r.split(",")[:2]] for r in lines[1:]])   # lines[0] is the header
    return data[:, 0], data[:, 1]


def hinge(x, xb, c, s1, s2):
    """Two straight lines that meet at x = xb."""
    return c + s1 * np.minimum(x, xb) + s2 * np.maximum(x - xb, 0.0)


def fit_break_point(x, y):
    """Least-squares two-line fit. For each trial break point xb the model is linear in (c, s1, s2),
    so solve it with lstsq and keep the xb with the smallest sum of squared residuals."""
    best = None
    xs = np.sort(x)
    for xb in np.linspace(xs[1], xs[-2], 2001):    # keep at least two points on each line
        A = np.column_stack([np.ones_like(x), np.minimum(x, xb), np.maximum(x - xb, 0.0)])
        coef, *_ = np.linalg.lstsq(A, y, rcond=None)
        sse = float(np.sum((A @ coef - y) ** 2))
        if best is None or sse < best[0]:
            best = (sse, xb, *coef)
    sse, xb, c, s1, s2 = best
    return xb, c, s1, s2, sse


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "vinegar_example.csv"
    v_ml = float(sys.argv[2]) if len(sys.argv) > 2 else 50.0
    x, y = load(path)
    xb, c, s1, s2, sse = fit_break_point(x, y)

    n_acid = xb / M_NAHCO3                      # 1:1 reaction, so mol acid = mol NaHCO3 at the break point
    conc = n_acid / (v_ml / 1000)               # mol/L
    w_v = conc * M_ACOH / 10                    # g per 100 mL
    slope_ideal = M_CO2 / M_NAHCO3
    plateau = hinge(np.array([x.max()]), xb, c, s1, s2)[0]
    print(f"break point        : {xb:.2f} g NaHCO3")
    print(f"acetic acid        : {n_acid * 1000:.1f} mmol in {v_ml:.0f} mL -> {conc:.3f} mol/L = {w_v:.2f} % w/v")
    print(f"rising slope       : {s1:.3f} g CO2 per g NaHCO3 (ideal {slope_ideal:.3f}) -> {100 * s1 / slope_ideal:.0f} % of CO2 escaped")
    print(f"plateau slope      : {s2:.3f} (should be close to 0)")
    print(f"plateau mass loss  : {plateau:.2f} g -> naive concentration from plateau {plateau / M_CO2 / (v_ml / 1000):.3f} mol/L")
    print(f"rms residual       : {np.sqrt(sse / x.size):.3f} g")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return
    out = HERE / "runs"
    out.mkdir(exist_ok=True)
    xs = np.linspace(0, x.max(), 300)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(x, y, "o", label="measured")
    ax.plot(xs, hinge(xs, xb, c, s1, s2), "-", label="two-line fit")
    ax.plot(xs, slope_ideal * xs, ":", label="all CO2 escapes, acid in excess")
    ax.axvline(xb, color="grey", lw=0.8)
    ax.set_xlabel("baking soda added / g")
    ax.set_ylabel("mass lost / g")
    ax.set_ylim(bottom=0)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out / "limiting.png", dpi=120)
    print(f"\nPlot saved to {out / 'limiting.png'}")


if __name__ == "__main__":
    main()
