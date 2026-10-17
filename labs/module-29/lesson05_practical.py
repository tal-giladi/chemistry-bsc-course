"""Lesson 29.5 Part B - module practical, reference solution: characterise enzyme E1 and three inhibitors.

Fill in the functions marked TODO, then run:  py lesson05_practical.py
Reference solution: lesson05_practical_solution.py
Writes runs/lesson05_practical.png.
Step 1: Km and Vmax without inhibitor, nonlinear least squares against Lineweaver-Burk, with a
        parametric bootstrap for honest uncertainties.
Step 2: for each inhibitor X, Y, Z: global fits of competitive, uncompetitive and mixed models,
        choose by AICc, check against the Lineweaver-Burk pattern, report the inhibition constants.
Step 3: pathway consequence: E1's substrate builds up when E1 is inhibited. How much flux is left?
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

from enz29 import aic, column, mixed, mm, read_csv, runs_dir

BIG = 1e9
REL, ABS = 0.04, 0.8          # noise model stated in the data file: 4 % relative + 0.8 uM/min


def sigma_of(v):
    return np.sqrt((REL * v) ** 2 + ABS ** 2)


def fit_mm(S, v):
    # TODO: popt, pcov = curve_fit(mm, S, v, p0=(v.max(), np.median(S)), sigma=sigma_of(v), absolute_sigma=True)
    # TODO: return popt, np.sqrt(np.diag(pcov))
    raise NotImplementedError("TODO: write fit_mm() first (see the hints in the code).")


def lineweaver_burk(S, v):
    # TODO: slope, intercept = np.polyfit(1 / S, 1 / v, 1)
    # TODO: return 1 / intercept, slope / intercept
    raise NotImplementedError("TODO: write lineweaver_burk() first (see the hints in the code).")


def bootstrap_mm(S, V, K, n=1000, seed=2):
    """Parametric bootstrap: refit n synthetic data sets drawn from the fitted curve and the noise model."""
    rng = np.random.default_rng(seed)
    nl, lb = [], []
    for _ in range(n):
        v0 = mm(S, V, K)
        v = v0 + rng.normal(0, 1, S.size) * sigma_of(v0)
        nl.append(fit_mm(S, v)[0])
        lb.append(lineweaver_burk(S, np.clip(v, 0.1, None)))
    return np.array(nl), np.array(lb)


MODELS = {
    "competitive": (lambda X, V, K, Ki: mixed(X[0], X[1], V, K, Ki, BIG), 3),
    "uncompetitive": (lambda X, V, K, Kii: mixed(X[0], X[1], V, K, BIG, Kii), 3),
    "mixed": (lambda X, V, K, Ki, Kii: mixed(X[0], X[1], V, K, Ki, Kii), 4),
}


def global_fits(S, I, v):
    """Fit all three models to one inhibitor's data plus the no-inhibitor data. Returns {name: (popt, perr, AICc)}."""
    out = {}
    for name, (f, k) in MODELS.items():
        p0 = [v.max(), 0.5] + [0.5] * (k - 2)
        popt, pcov = curve_fit(f, (S, I), v, p0=p0, sigma=sigma_of(v), absolute_sigma=True,
                               bounds=(1e-6, np.inf), maxfev=20000)
        rss = float(np.sum(((v - f((S, I), *popt)) / sigma_of(v)) ** 2))
        out[name] = (popt, np.sqrt(np.diag(pcov)), aic(rss, v.size, k))
    return out


def flux_left(S, I, V, K, Ki, Kii):
    """Rate with inhibitor as a fraction of the uninhibited rate at the same S."""
    # TODO: return mixed(S, I, V, K, Ki, Kii) / mm(S, V, K)
    raise NotImplementedError("TODO: write flux_left() first (see the hints in the code).")


def dose_for_half(S, V, K, Ki, Kii):
    """[I] that halves the rate at S (closed form for the mixed model)."""
    return 1.0 / (K / (K + S) / Ki + S / (K + S) / Kii)


def fmt(p, e):
    return "-> infinity" if p > 1e6 else f"{p:.3g} +/- {e:.2g}"


def main():
    rows = read_csv("practical_rates.csv")
    inh = np.array([r["inhibitor"] for r in rows])
    I = column(rows, "I_mM"); S = column(rows, "S_mM"); v = column(rows, "v_uM_per_min")

    m0 = inh == "none"
    (V, K), (sV, sK) = fit_mm(S[m0], v[m0])
    Vlb, Klb = lineweaver_burk(S[m0], v[m0])
    print("Step 1: no inhibitor")
    print(f"  nonlinear:        Vmax = {V:.1f} +/- {sV:.1f} uM/min, Km = {K:.3f} +/- {sK:.3f} mM")
    print(f"  Lineweaver-Burk:  Vmax = {Vlb:.1f} uM/min,          Km = {Klb:.3f} mM")
    nl, lb = bootstrap_mm(S[m0], V, K)
    for name, arr in (("nonlinear", nl), ("Lineweaver-Burk", lb)):
        lo, hi = np.percentile(arr[:, 1], [2.5, 97.5])
        print(f"  bootstrap 95 % range of Km, {name:16s}: {lo:.3f} - {hi:.3f} mM")

    print("\nStep 2: inhibition type (each inhibitor fitted together with the no-inhibitor data)")
    best = {}
    for name in ("X", "Y", "Z"):
        m = m0 | (inh == name)
        fits = global_fits(S[m], I[m], v[m])
        ranked = sorted(fits, key=lambda k: fits[k][2])
        best[name] = (ranked[0], fits[ranked[0]][0])
        print(f"  inhibitor {name}:")
        for model in ranked:
            popt, perr, a = fits[model]
            print(f"    {model:14s} AICc = {a:7.1f}  [{', '.join(fmt(p, e) for p, e in zip(popt, perr))}]")
        print(f"    -> {ranked[0]} (dAICc to next = {fits[ranked[1]][2] - fits[ranked[0]][2]:.1f})")

    print("\nStep 3: pathway consequence. Dose each inhibitor to halve the rate at S = 0.25 mM,")
    print("then let S build up tenfold to 2.5 mM, as substrate does in front of an inhibited step while supply continues.")
    for name, (model, p) in best.items():
        Ki = p[2] if model in ("competitive", "mixed") else BIG
        Kii = p[2] if model == "uncompetitive" else (p[3] if model == "mixed" else BIG)
        Vf, Kf = p[0], p[1]
        dose = dose_for_half(0.25, Vf, Kf, Ki, Kii)
        print(f"  {name} ({model:13s}): dose {dose:.2f} mM; flux left at 0.25 mM = "
              f"{flux_left(0.25, dose, Vf, Kf, Ki, Kii):.2f}, at 2.5 mM = {flux_left(2.5, dose, Vf, Kf, Ki, Kii):.2f}")

    fig, ax = plt.subplots(1, 3, figsize=(15, 4))
    for a, name in zip(ax, ("X", "Y", "Z")):
        model, p = best[name]
        f = MODELS[model][0]
        for Ii in np.unique(I[m0 | (inh == name)]):
            mm_ = (inh == name) & (I == Ii) if Ii > 0 else m0
            line, = a.plot(1 / S[mm_], 1 / v[mm_], "o", ms=4, label=f"[I] = {Ii:g} mM")
            x = np.linspace(-3, 11, 100)
            Sx = 1 / np.where(np.abs(x) < 1e-9, 1e-9, x)
            a.plot(x, 1 / f((Sx, np.full_like(x, Ii)), *p), "-", c=line.get_color(), lw=1)
        a.axhline(0, c="k", lw=0.5); a.axvline(0, c="k", lw=0.5)
        a.set_ylim(-0.02, 0.12); a.set_xlim(-3, 11)
        a.set_xlabel("1/[S] / mM$^{-1}$"); a.set_ylabel("1/v / (uM/min)$^{-1}$")
        a.set_title(f"inhibitor {name}: best model {model}", fontsize=9); a.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(runs_dir() / "lesson05_practical.png", dpi=120)
    print("saved runs/lesson05_practical.png")


if __name__ == "__main__":
    try:
        main()
    except NotImplementedError as e:
        print(e)
