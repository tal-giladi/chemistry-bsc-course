"""Lesson 05.3: fitting models to data with uncertainty.

Part 1: a straight calibration line and an unknown concentration with its uncertainty.
Part 2: a weighted nonlinear fit of dye fading, judged by residuals and reduced chi-square.
Part 3: the same fit with lmfit, for comparison.

Fill in the three functions marked TODO, then run (from this folder):
    py lesson03_fitting.py
Reference solution: lesson03_fitting_solution.py
The figure is saved to runs/lesson03_fitting.png next to this file.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from lmfit import Model
from scipy.optimize import curve_fit
from scipy.stats import linregress
from uncertainties import correlated_values, ufloat

HERE = Path(__file__).resolve().parent


def line(x, m, b):
    return m * x + b


def decay(t, A0, k, C):
    return A0 * np.exp(-k * t) + C


def fit_line(x, y):
    """Unweighted straight-line fit. Return (popt, pcov, s_r), s_r = residual standard deviation.
    No sigma is given, so the scatter itself sets the uncertainty (absolute_sigma=False)."""
    # TODO: popt, pcov = curve_fit(line, x, y)
    # TODO: residuals y - line(x, *popt); s_r = sqrt(sum of squared residuals / (n - 2))
    return None


def predict_unknown(popt, pcov, A_unk, s_r):
    """Concentration of the unknown from the mean of its readings, with the slope-intercept
    correlation kept. Return a ufloat."""
    # TODO: m, b = correlated_values(popt, pcov)   (keeps their correlation)
    # TODO: the mean reading as ufloat(mean, s_r / sqrt(number of readings))
    # TODO: return (A_mean - b) / m
    return None


def fit_decay(t, A, sigma):
    """Weighted fit with the instrument's absolute sigma. Return (popt, pcov, chi2_red)."""
    # TODO: curve_fit(decay, t, A, p0=[A[0] - A[-1], 0.02, A[-1]], sigma=sigma, absolute_sigma=True)
    # TODO: chi2 = sum of ((A - model) / sigma)^2; return popt, pcov, chi2 / (n - number of parameters)
    return None


def main():
    # Part 1 -------------------------------------------------------------------------------
    cal = pd.read_csv(HERE / "calibration_dye.csv")
    std = cal[cal["sample"] == "standard"]
    x, y = std["c_umol_per_L"].to_numpy(), std["A630"].to_numpy()
    A_unk = cal.loc[cal["sample"] == "unknown", "A630"].to_numpy()

    res = fit_line(x, y)
    if res is None:
        print("TODO: write fit_line() first.")
        return
    popt, pcov, s_r = res
    (m, b), (um, ub) = popt, np.sqrt(np.diag(pcov))
    r = pcov[0, 1] / (um * ub)
    lr = linregress(x, y)
    print("Part 1: calibration line A = m c + b")
    print(f"  curve_fit: m = {m:.5f} +- {um:.5f} L/umol, b = {b:.4f} +- {ub:.4f}, "
          f"correlation(m, b) = {r:+.2f}, s_r = {s_r:.4f}")
    print(f"  linregress check: m = {lr.slope:.5f} +- {lr.stderr:.5f}, "
          f"b = {lr.intercept:.4f} +- {lr.intercept_stderr:.4f}")

    c = predict_unknown(popt, pcov, A_unk, s_r)
    if c is None:
        print("TODO: write predict_unknown() next.")
        return
    # Textbook formula for the same thing (Harvey, Analytical Chemistry 2.1, section 5.4)
    n, k_rep = x.size, A_unk.size
    s_c = (s_r / m) * np.sqrt(1 / k_rep + 1 / n + (A_unk.mean() - y.mean()) ** 2
                              / (m**2 * np.sum((x - x.mean()) ** 2)))
    c_nocorr = (ufloat(A_unk.mean(), s_r / np.sqrt(k_rep)) - ufloat(b, ub)) / ufloat(m, um)
    print(f"  unknown: c = {c.n:.3f} +- {c.s:.3f} umol/L (uncertainties, correlation kept)")
    print(f"           textbook formula: +- {s_c:.3f} umol/L")
    print(f"           correlation ignored: +- {c_nocorr.s:.3f} umol/L (too large)")
    print("  model value used to make the data: 3.70 umol/L")

    # Part 2 -------------------------------------------------------------------------------
    fad = pd.read_csv(HERE / "dye_fading.csv")
    t, A, sig = (fad[col].to_numpy() for col in ("t_min", "A", "sigma_A"))
    res = fit_decay(t, A, sig)
    if res is None:
        print("TODO: write fit_decay() last.")
        return
    pw, cw, chi2_red = res
    uw = np.sqrt(np.diag(cw))
    pu, cu = curve_fit(decay, t, A, p0=[0.9, 0.02, 0.02])
    print("\nPart 2: dye fading A = A0 exp(-k t) + C")
    print(f"  weighted:   k = {pw[1]:.5f} +- {uw[1]:.5f} 1/min, A0 = {pw[0]:.4f}, C = {pw[2]:.4f}, "
          f"reduced chi-square = {chi2_red:.2f}")
    print(f"  unweighted: k = {pu[1]:.5f} +- {np.sqrt(cu[1, 1]):.5f} 1/min")
    print(f"  half-life = ln2/k = {np.log(2) / pw[1]:.1f} min; model values: k = 0.02300, "
          "A0 = 0.950, C = 0.020")

    # Which quoted uncertainty is honest? Simulate 500 new data sets from the fitted model with
    # the same sigma, fit each both ways, and compare the real spread of k with the quoted one.
    rng = np.random.default_rng(1)
    k_w, k_u = [], []
    for _ in range(500):
        A_sim = decay(t, *pw) + sig * rng.standard_normal(t.size)
        k_w.append(curve_fit(decay, t, A_sim, p0=pw, sigma=sig, absolute_sigma=True)[0][1])
        k_u.append(curve_fit(decay, t, A_sim, p0=pw)[0][1])
    print(f"  Monte Carlo spread of k: weighted {np.std(k_w):.5f} (quoted {uw[1]:.5f}), "
          f"unweighted {np.std(k_u):.5f} (quoted {np.sqrt(cu[1, 1]):.5f})")
    print("  The unweighted fit scatters more AND quotes too small an uncertainty.")

    # Part 3 -------------------------------------------------------------------------------
    result = Model(decay).fit(A, t=t, A0=0.9, k=0.02, C=0.02, weights=1 / sig, scale_covar=False)
    kp = result.params["k"]
    print(f"\nPart 3: lmfit gives k = {kp.value:.5f} +- {kp.stderr:.5f} 1/min, "
          f"reduced chi-square = {result.redchi:.2f}")

    (HERE / "runs").mkdir(exist_ok=True)
    fig, axs = plt.subplots(2, 2, figsize=(8, 5.5), sharex="col",
                            gridspec_kw={"height_ratios": [3, 1]})
    xx = np.linspace(0, x.max(), 50)
    axs[0, 0].plot(x, y, "o", label="standards")
    axs[0, 0].plot(xx, line(xx, m, b), "-", label="fit")
    axs[0, 0].plot(c.n, A_unk.mean(), "s", label="unknown")
    axs[0, 0].set_ylabel("A at 630 nm")
    axs[0, 0].legend(fontsize=8)
    axs[1, 0].axhline(0, color="grey", lw=0.8)
    axs[1, 0].plot(x, y - line(x, m, b), "o")
    axs[1, 0].set_xlabel("c (umol/L)")
    axs[1, 0].set_ylabel("residual")
    tt = np.linspace(0, t.max(), 200)
    axs[0, 1].errorbar(t, A, yerr=sig, fmt="o", ms=3, label="data")
    axs[0, 1].plot(tt, decay(tt, *pw), "-", label="weighted fit")
    axs[0, 1].set_ylabel("A")
    axs[0, 1].legend(fontsize=8)
    axs[1, 1].axhline(0, color="grey", lw=0.8)
    axs[1, 1].plot(t, (A - decay(t, *pw)) / sig, "o")
    axs[1, 1].set_xlabel("t (min)")
    axs[1, 1].set_ylabel("residual / sigma")
    fig.tight_layout()
    out = HERE / "runs" / "lesson03_fitting.png"
    fig.savefig(out, dpi=120)
    print(f"plot saved to runs/{out.name}")


if __name__ == "__main__":
    main()
