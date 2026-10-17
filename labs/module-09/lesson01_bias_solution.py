"""Lesson 09.1 (reference solution): bias, precision and constant versus proportional error.

Run (from this folder):
    py lesson01_bias_solution.py                     # example data
    py lesson01_bias_solution.py my_coins.csv 3.5    # your coin series and the nominal coin mass in g
"""
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
RUNS = HERE / "runs"
CERTIFIED = 25.0          # mg/L, chloride CRM
W_CL = 606.6              # mg chloride per g of pure NaCl (35.453 / 58.443)


def read_csv(path):
    """Return header names and rows (lists of strings), skipping # comment lines."""
    lines = [r for r in Path(path).read_text(encoding="utf-8").splitlines() if r.strip() and not r.startswith("#")]
    return lines[0].split(","), [r.split(",") for r in lines[1:]]


def bias_table(path):
    """Mean, standard deviation, bias and relative error of each analyst against the certified value."""
    _, rows = read_csv(path)
    out = {}
    for name in sorted({r[0] for r in rows}):
        x = np.array([float(r[1]) for r in rows if r[0] == name])
        mean, s = x.mean(), x.std(ddof=1)
        bias = mean - CERTIFIED
        out[name] = dict(n=x.size, mean=mean, s=s, bias=bias, rel=100 * bias / CERTIFIED,
                         recovery=100 * mean / CERTIFIED)
    return out


def fit_line(x, y):
    """Least-squares straight line y = b0 + b1 x. Returns (b0, u_b0, b1, u_b1)."""
    (b1, b0), cov = np.polyfit(x, y, 1, cov=True)
    return b0, np.sqrt(cov[1, 1]), b1, np.sqrt(cov[0, 0])


def main():
    RUNS.mkdir(exist_ok=True)
    print("1. Two analysts on a CRM certified at 25.0 mg/L")
    for name, t in bias_table(HERE / "crm_analysts.csv").items():
        print(f"   analyst {name}: n={t['n']} mean={t['mean']:.2f} s={t['s']:.2f} "
              f"bias={t['bias']:+.2f} mg/L ({t['rel']:+.1f} %), recovery={t['recovery']:.1f} %")

    print("2. Sample-size series on pure NaCl")
    _, rows = read_csv(HERE / "sample_size_series.csv")
    m = np.array([float(r[0]) for r in rows])
    found = np.array([float(r[1]) for r in rows])
    b0, ub0, b1, ub1 = fit_line(m, found)
    prop = 100 * (b1 / W_CL - 1)
    print(f"   intercept (constant error) = {b0:+.2f} +/- {ub0:.2f} mg")
    print(f"   slope = {b1:.1f} +/- {ub1:.1f} mg/g vs expected {W_CL} -> proportional error {prop:+.2f} %")

    coin_file = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "coins_example.csv"
    nominal = float(sys.argv[2]) if len(sys.argv) > 2 else 3.5
    _, rows = read_csv(coin_file)
    n = np.array([float(r[0]) for r in rows])
    g = np.array([float(r[1]) for r in rows])
    c0, uc0, c1, uc1 = fit_line(n, g)
    print(f"3. Coins on the kitchen scale ({coin_file.name})")
    print(f"   intercept (constant error of the scale) = {c0:+.2f} +/- {uc0:.2f} g")
    print(f"   slope = {c1:.3f} +/- {uc1:.3f} g per coin; nominal {nominal} g -> "
          f"{100 * (c1 / nominal - 1):+.1f} % (scale gain and coin wear together)")

    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    ax[0].plot(m, found - W_CL * m, "o")
    ax[0].plot(m, b0 + b1 * m - W_CL * m, "-")
    ax[0].axhline(0, color="grey", lw=0.8)
    ax[0].set(xlabel="sample mass (g)", ylabel="found - expected (mg)", title="Constant + proportional error")
    ax[1].plot(n, g, "o")
    ax[1].plot(n, c0 + c1 * n, "-")
    ax[1].set(xlabel="number of coins", ylabel="scale reading (g)", title="Coin series")
    fig.tight_layout()
    fig.savefig(RUNS / "lesson01_bias.png", dpi=120)
    print("   plot written to runs/lesson01_bias.png")


if __name__ == "__main__":
    main()
