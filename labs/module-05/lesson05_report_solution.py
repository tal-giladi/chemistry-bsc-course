"""Lesson 05.5 module practical, reference solution: sugar in a soft drink from its density.

The same steps as the notebook lesson05_report.ipynb, as one script you can run top to bottom:
record the environment, read the raw measurements, compute densities, fit a calibration with
uncertainty, check the residuals, choose the model, predict the unknown, save figure and results.

Usage (from this folder):
    py lesson05_report_solution.py                          # density_raw.csv
    py lesson05_report_solution.py ../module-01/my_data.csv  # your own Module 1 measurements
Outputs go to runs/ next to this file.
"""
import sys
from datetime import date
from importlib.metadata import version
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from uncertainties import correlated_values, ufloat

HERE = Path(__file__).resolve().parent
RUNS = HERE / "runs"


def environment():
    """One line that says what produced these results."""
    pkgs = ", ".join(f"{p} {version(p)}" for p in ("numpy", "scipy", "pandas", "uncertainties"))
    return f"{date.today().isoformat()}; Python {sys.version.split()[0]}; {pkgs}"


def densities(raw):
    """Add a density column (g/mL) to the raw table: mass of the fills / their volume."""
    out = raw.copy()
    out["rho_g_per_mL"] = (out["cup_full_g"] - out["cup_empty_g"]) / (out["fills"] * out["fill_volume_mL"])
    return out


def summarise(df):
    """Mean, standard deviation and count per sample, and the standard error of each mean.
    Five repeats give a shaky SD (about +-35 %), and every sample was measured the same way, so
    the SEM uses the pooled SD of all samples: sqrt(mean of the variances) / sqrt(n)."""
    g = df.groupby("sample", sort=False).agg(w_percent=("w_percent", "first"),
                                             rho=("rho_g_per_mL", "mean"),
                                             sd=("rho_g_per_mL", "std"),
                                             n=("rho_g_per_mL", "size"))
    sd_pooled = np.sqrt(np.mean(g["sd"] ** 2))
    g["sem"] = sd_pooled / np.sqrt(g["n"])
    return g


def line(w, a, b):
    return a + b * w


def quad(w, a, b, c):
    return a + b * w + c * w**2


def weighted_fit(f, x, y, s, p0):
    popt, pcov = curve_fit(f, x, y, p0=p0, sigma=s, absolute_sigma=True)
    chi2_red = np.sum(((y - f(x, *popt)) / s) ** 2) / (x.size - len(popt))
    return popt, pcov, chi2_red


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "density_raw.csv"
    RUNS.mkdir(exist_ok=True)
    env = environment()
    print("Environment:", env)

    raw = pd.read_csv(path)                         # raw data are read, never edited
    df = densities(raw)
    summary = summarise(df)
    std = summary[summary["w_percent"].notna()]
    unk = summary[summary["w_percent"].isna()]
    print(f"\n{path.name}: {len(raw)} rows, {len(std)} standards, {len(unk)} unknown(s)")
    print(summary.round(5).to_string())

    x, y = std["w_percent"].to_numpy(float), std["rho"].to_numpy()
    s = std["sem"].to_numpy()

    fits = {"line 0-30 %": (line, *weighted_fit(line, x, y, s, [1.0, 0.004])),
            "quadratic 0-30 %": (quad, *weighted_fit(quad, x, y, s, [1.0, 0.004, 0.0]))}
    low = x <= 15
    if low.sum() >= 3:
        fits["line 0-15 %"] = (line, *weighted_fit(line, x[low], y[low], s[low], [1.0, 0.004]))
    print("\nModel comparison (reduced chi-square near 1 = residuals match the stated noise):")
    for name, (f, popt, pcov, chi2r) in fits.items():
        print(f"  {name:<17} chi2_red = {chi2r:6.2f}   parameters = {np.array2string(popt, precision=6)}")

    # Decision: the straight line over 0-30 % leaves curved residuals (chi2_red >> 1), so the
    # quadratic is the calibration. Invert it for each unknown, keeping the correlations.
    qa, qb, qc = correlated_values(fits["quadratic 0-30 %"][1], fits["quadratic 0-30 %"][2])
    la, lb = fits["line 0-30 %"][1]
    results = []
    for name, row in unk.iterrows():
        rho_u = ufloat(row["rho"], row["sem"])
        w_q = (-qb + (qb**2 - 4 * qc * (qa - rho_u)) ** 0.5) / (2 * qc)
        results.append({"sample": name, "rho_g_per_mL": row["rho"], "u_rho": row["sem"],
                        "w_percent": w_q.n, "u_w_percent": w_q.s})
        print(f"\nUnknown '{name}': rho = {rho_u:.5f} g/mL -> sugar w = {w_q:.2f} % "
              "(quadratic, standard uncertainty)")
        if "line 0-15 %" in fits:
            a, b = correlated_values(fits["line 0-15 %"][1], fits["line 0-15 %"][2])
            print(f"  cross-check, local line 0-15 %: w = {(rho_u - a) / b:.2f} %")
        print(f"  straight line 0-30 % would say: w = {(row['rho'] - la) / lb:.2f} %")

    pd.DataFrame(results).to_csv(RUNS / "lesson05_results.csv", index=False, float_format="%.5f")
    (RUNS / "lesson05_environment.txt").write_text(env + "\n", encoding="utf-8")

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.4, 6), sharex=True,
                                   gridspec_kw={"height_ratios": [2, 1]})
    ww = np.linspace(0, x.max(), 100)
    ax1.errorbar(x, y, yerr=s, fmt="o", ms=4, label="standards (mean $\\pm$ SEM)")
    ax1.plot(ww, line(ww, *fits["line 0-30 %"][1]), "--", label="line 0-30 %")
    ax1.plot(ww, quad(ww, *fits["quadratic 0-30 %"][1]), "-", label="quadratic 0-30 %")
    for r in results:
        ax1.plot(r["w_percent"], r["rho_g_per_mL"], "s", label=r["sample"])
    ax1.set_ylabel("density (g/mL)")
    ax1.legend(fontsize=8)
    ax2.axhline(0, color="grey", lw=0.8)
    ax2.plot(x, (y - line(x, *fits["line 0-30 %"][1])) / s, "o--", label="line 0-30 %")
    ax2.plot(x, (y - quad(x, *fits["quadratic 0-30 %"][1])) / s, "s", label="quadratic 0-30 %")
    ax2.set_xlabel("sucrose (% by mass)")
    ax2.set_ylabel("residual / SEM")
    ax2.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(RUNS / "lesson05_calibration.png", dpi=120)
    print("\nSaved runs/lesson05_results.csv, runs/lesson05_environment.txt, runs/lesson05_calibration.png")


if __name__ == "__main__":
    main()
