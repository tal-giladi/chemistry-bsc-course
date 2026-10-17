"""Lesson 29.2 - exercise: Michaelis-Menten fits, three linear plots, and a Monte Carlo test.

Fill in the functions marked TODO, then run:  py lesson02_mm.py
Reference solution: lesson02_mm_solution.py
Writes runs/lesson02_mm.png.
Part 1: the seven 1913 invertase initial rates fitted four ways.
Part 2: 2000 simulated data sets with known Km and Vmax: which method gets Km right, and how precisely?
Part 3: the same test with a poor design (all [S] above Km).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

from enz29 import column, mm, read_csv, runs_dir


def fit_nonlinear(S, v):
    popt, pcov = curve_fit(mm, S, v, p0=(v.max(), np.median(S)), maxfev=5000)
    return popt, np.sqrt(np.diag(pcov))


def lineweaver_burk(S, v):
    """1/v = 1/V + (K/V)(1/S)."""
    # TODO: slope, intercept = np.polyfit(1 / S, 1 / v, 1)
    # TODO: return 1 / intercept, slope / intercept
    raise NotImplementedError("TODO: write lineweaver_burk() first (see the hints in the code).")


def hanes_woolf(S, v):
    """S/v = K/V + S/V."""
    # TODO: slope, intercept = np.polyfit(S, S / v, 1)
    # TODO: return 1 / slope, intercept / slope
    raise NotImplementedError("TODO: write hanes_woolf() first (see the hints in the code).")


def eadie_hofstee(S, v):
    """v = V - K (v/S)."""
    # TODO: slope, intercept = np.polyfit(v / S, v, 1)
    # TODO: return intercept, -slope
    raise NotImplementedError("TODO: write eadie_hofstee() first (see the hints in the code).")


METHODS = {"nonlinear": lambda S, v: tuple(fit_nonlinear(S, v)[0]), "Lineweaver-Burk": lineweaver_burk,
           "Hanes-Woolf": hanes_woolf, "Eadie-Hofstee": eadie_hofstee}


def monte_carlo(S, V=1.0, K=1.0, sd=0.03, n=2000, seed=1):
    """Fit n noisy copies of an exact data set (constant absolute noise sd, in units of V).
    Returns {method: array of fitted Km}."""
    rng = np.random.default_rng(seed)
    out = {m: [] for m in METHODS}
    for _ in range(n):
        v = mm(S, V, K) + rng.normal(0, sd * V, S.size)
        v = np.clip(v, 1e-4, None)
        for name, f in METHODS.items():
            try:
                out[name].append(f(S, v)[1])
            except RuntimeError:
                out[name].append(np.nan)
    return {k: np.array(x) for k, x in out.items()}


def summary(Ks, K=1.0):
    """Median Km relative to the truth and the 16-84 % range (about +/- 1 SD), as % of K."""
    lo, med, hi = np.nanpercentile(Ks, [16, 50, 84])
    return 100 * (med / K - 1), 100 * (hi - lo) / 2 / K


def main():
    rows = read_csv("invertase_initial_rates.csv")
    S = column(rows, "sucrose_M") * 1000
    v = column(rows, "initial_rate_arb")
    print("Part 1: 1913 invertase initial rates (Km from Michaelis and Menten: 16.7 mM)")
    (V, K), (sV, sK) = fit_nonlinear(S, v)
    print(f"  {'nonlinear':16s} V = {V:.2f} +/- {sV:.2f}, Km = {K:.1f} +/- {sK:.1f} mM")
    for name in ("Lineweaver-Burk", "Hanes-Woolf", "Eadie-Hofstee"):
        Vx, Kx = METHODS[name](S, v)
        print(f"  {name:16s} V = {Vx:.2f},          Km = {Kx:.1f} mM")

    good = np.array([0.2, 0.4, 0.8, 1.6, 3.2, 6.4])   # in units of Km
    poor = np.array([2.0, 3.0, 4.5, 6.0, 8.0, 10.0])
    print("\nPart 2: Monte Carlo, true Km = 1, Vmax = 1, noise SD 3 % of Vmax, [S] = 0.2-6.4 Km, 2000 sets")
    mc_good = monte_carlo(good)
    for name, Ks in mc_good.items():
        bias, spread = summary(Ks)
        print(f"  {name:16s} median bias {bias:+5.1f} %, spread (16-84 %) +/- {spread:4.1f} %")
    print("\nPart 3: same noise, poor design [S] = 2-10 Km")
    mc_poor = monte_carlo(poor)
    for name, Ks in mc_poor.items():
        bias, spread = summary(Ks)
        print(f"  {name:16s} median bias {bias:+5.1f} %, spread (16-84 %) +/- {spread:4.1f} %")

    fig, ax = plt.subplots(1, 3, figsize=(14, 4))
    ss = np.linspace(0.1, S.max(), 300)
    ax[0].plot(S, v, "o", label="1913 data")
    ax[0].plot(ss, mm(ss, V, K), "-", label=f"nonlinear, Km = {K:.1f} mM")
    ax[0].set_xlabel("[sucrose] / mM"); ax[0].set_ylabel("v (arb.)"); ax[0].legend()
    Vlb, Klb = lineweaver_burk(S, v)
    x = np.linspace(-1 / Klb * 1.2, (1 / S).max() * 1.05, 100)
    ax[1].plot(1 / S, 1 / v, "o"); ax[1].plot(x, 1 / Vlb + Klb / Vlb * x, "-")
    ax[1].axhline(0, c="k", lw=0.5); ax[1].axvline(0, c="k", lw=0.5)
    ax[1].set_xlabel("1/[S] / mM$^{-1}$"); ax[1].set_ylabel("1/v"); ax[1].set_title("Lineweaver-Burk", fontsize=9)
    bins = np.linspace(0, 3, 61)
    for name in ("nonlinear", "Lineweaver-Burk"):
        ax[2].hist(np.clip(mc_good[name], 0, 3), bins=bins, histtype="step", label=name)
    ax[2].axvline(1, c="k", lw=0.8)
    ax[2].set_xlabel("fitted Km / true Km"); ax[2].set_ylabel("count"); ax[2].legend()
    ax[2].set_title("2000 simulated data sets", fontsize=9)
    fig.tight_layout(); fig.savefig(runs_dir() / "lesson02_mm.png", dpi=120)
    print("saved runs/lesson02_mm.png")


if __name__ == "__main__":
    try:
        main()
    except NotImplementedError as e:
        print(e)
