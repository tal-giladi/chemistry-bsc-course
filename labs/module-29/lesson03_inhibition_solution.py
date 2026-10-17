"""Lesson 29.3 - reference solution: what kind of inhibitor is fructose for invertase?

Run:  py lesson03_inhibition_solution.py
Writes runs/lesson03_inhibition.png.
Part 1: fit each fructose concentration on its own and watch the apparent Km and Vmax.
Part 2: global fits of competitive, uncompetitive and mixed models; choose with residuals and AIC.
Part 3: IC50 at one sucrose concentration and the Cheng-Prusoff check.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq, curve_fit

from enz29 import aic, column, mixed, mm, read_csv, runs_dir

BIG = 1e9   # stands in for an infinite inhibition constant


def model_competitive(X, V, K, Ki):
    S, I = X
    return mixed(S, I, V, K, Ki, BIG)


def model_uncompetitive(X, V, K, Kii):
    S, I = X
    return mixed(S, I, V, K, BIG, Kii)


def model_mixed(X, V, K, Ki, Kii):
    S, I = X
    return mixed(S, I, V, K, Ki, Kii)


MODELS = {"competitive": (model_competitive, 3), "uncompetitive": (model_uncompetitive, 3),
          "mixed": (model_mixed, 4)}


def global_fit(S, I, v, name, p0_V, p0_K, p0_Ki, weights=None):
    """Fit one model to all points. Relative weights (sigma proportional to v) by default.
    Returns parameters, standard errors, weighted residual sum of squares."""
    f, k = MODELS[name]
    p0 = [p0_V, p0_K] + [p0_Ki] * (k - 2)
    sigma = v if weights is None else weights
    popt, pcov = curve_fit(f, (S, I), v, p0=p0, sigma=sigma, bounds=(1e-6, np.inf), maxfev=20000)
    rss = float(np.sum(((v - f((S, I), *popt)) / sigma) ** 2))
    return popt, np.sqrt(np.diag(pcov)), rss


def ic50(S, V, K, Ki, Kii):
    """Inhibitor concentration that halves the rate at substrate concentration S."""
    v0 = mm(S, V, K)
    return brentq(lambda I: mixed(S, I, V, K, Ki, Kii) - v0 / 2, 1e-9, 1e6)


def main():
    rows = read_csv("invertase_fructose_rates.csv")
    I = column(rows, "fructose_mM")
    S = column(rows, "sucrose_mM")
    v = column(rows, "rate_arb")

    print("Part 1: separate Michaelis-Menten fit at each fructose concentration")
    for Ii in np.unique(I):
        m = I == Ii
        (Va, Ka), _ = curve_fit(mm, S[m], v[m], p0=(4, 20), sigma=v[m])
        print(f"  fructose {Ii:5.0f} mM: apparent Vmax = {Va:.2f}, apparent Km = {Ka:5.1f} mM")

    print("\nPart 2: global fits (relative weighting)")
    n = v.size
    results = {}
    for name, (_, k) in MODELS.items():
        popt, perr, rss = global_fit(S, I, v, name, 4.0, 20.0, 50.0)
        results[name] = (popt, perr, rss, aic(rss, n, k))
        pars = ", ".join("-> infinity" if p > 1e6 else f"{p:.3g} +/- {e:.2g}" for p, e in zip(popt, perr))
        print(f"  {name:14s} params [{pars}]  wRSS = {rss:7.4f}  AICc = {results[name][3]:7.1f}")
    best = min(results, key=lambda k: results[k][3])
    print(f"  lowest AICc: {best}")
    V, K, Ki = results["competitive"][0]
    print(f"  competitive Ki = {Ki:.0f} mM (value used to make the data: 58 mM, Michaelis and Menten 1913)")

    print("\nPart 3: IC50 at 20.8 mM sucrose")
    I50 = ic50(20.8, V, K, Ki, BIG)
    print(f"  IC50 = {I50:.0f} mM fructose; Cheng-Prusoff Ki = IC50 / (1 + S/Km) = {I50 / (1 + 20.8 / K):.0f} mM")
    print(f"  at 166.7 mM sucrose the IC50 rises to {ic50(166.7, V, K, Ki, BIG):.0f} mM")

    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    for Ii in np.unique(I):
        m = I == Ii
        line, = ax[0].plot(1 / S[m], 1 / v[m], "o", label=f"{Ii:g} mM fructose")
        x = np.linspace(0, (1 / S).max() * 1.05, 50)
        ax[0].plot(x, 1 / mixed(1 / np.maximum(x, 1e-9), Ii, V, K, Ki, BIG), "-", c=line.get_color())
        ax[1].plot(S[m], v[m], "o", c=line.get_color())
        ss = np.linspace(1, S.max(), 200)
        ax[1].plot(ss, mixed(ss, Ii, V, K, Ki, BIG), "-", c=line.get_color())
    ax[0].set_xlabel("1/[sucrose] / mM$^{-1}$"); ax[0].set_ylabel("1/v"); ax[0].legend(fontsize=8)
    ax[0].set_title("lines from the global competitive fit, not from linear regression", fontsize=9)
    ax[1].set_xlabel("[sucrose] / mM"); ax[1].set_ylabel("v (arb.)")
    fig.tight_layout(); fig.savefig(runs_dir() / "lesson03_inhibition.png", dpi=120)
    print("saved runs/lesson03_inhibition.png")


if __name__ == "__main__":
    main()
