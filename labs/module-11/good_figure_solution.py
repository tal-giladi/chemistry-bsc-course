"""Lesson 11.3 — the same data as bad_figure.py, drawn so that the figure tells the story (reference solution).

(a) every titration is a point; each learner's mean with its 95 % confidence interval; the odd results labelled.
(b) the titration curve and its first derivative on separate, aligned panels, with the end point marked.
Run from this folder:  py good_figure_solution.py   -> runs/good_figure.png
Add --assets to also write SVG copies of both figures for the lesson (course maintainers only).
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from bad_figure import HERE, bad_figure, load

# Okabe–Ito colours: distinguishable with the common forms of colour blindness.
BLUE, VERMILION, GREY = "#0072B2", "#D55E00", "#666666"
MODEL_VALUE = 4.95  # the value used to simulate the data (make_data.py)


def learner_summary(vin):
    """Return {learner: (mean, s, ci95_half_width, n)} for the acid results."""
    out = {}
    for k in sorted(set(vin["learner"])):
        x = vin["acid_percent_ww"][vin["learner"] == k]
        n = x.size
        s = x.std(ddof=1)
        half = stats.t.ppf(0.975, n - 1) * s / np.sqrt(n)
        out[k] = (x.mean(), s, half, n)
    return out


def end_point(v, ph):
    """First derivative at interval midpoints and the volume where it is largest."""
    vm = (v[1:] + v[:-1]) / 2
    d = np.diff(ph) / np.diff(v)
    return vm, d, vm[np.argmax(d)]


def good_figure(vin, tit, out):
    summ = learner_summary(vin)
    learners = list(summ)
    fig = plt.figure(figsize=(10, 4.6), layout="constrained")
    gs = fig.add_gridspec(2, 2, width_ratios=[1.1, 1])
    ax = fig.add_subplot(gs[:, 0])
    top = fig.add_subplot(gs[0, 1])
    bot = fig.add_subplot(gs[1, 1], sharex=top)

    # (a) all points, mean and 95 % CI
    rng = np.random.default_rng(0)
    for i, k in enumerate(learners):
        sel = vin["learner"] == k
        x = vin["acid_percent_ww"][sel]
        colour = VERMILION if k == "D" else BLUE
        ax.plot(i + rng.uniform(-0.12, 0.12, x.size), x, "o", ms=5, color=colour, alpha=0.6, mec="none")
        m, s, h, n = summ[k]
        ax.errorbar(i + 0.3, m, yerr=h, fmt="s", ms=5, color=colour, capsize=3, lw=1.2)
    ax.axhline(MODEL_VALUE, color=GREY, ls=":", lw=1)
    ax.text(-0.45, 4.675, f"dotted line: value used to simulate the data, {MODEL_VALUE:.2f} %", color=GREY, fontsize=8)
    ax.annotate("spill, trial 4", xy=(2, vin["acid_percent_ww"][(vin["learner"] == "C") & (vin["trial"] == 4)][0]),
                xytext=(2.4, 4.74), fontsize=8, arrowprops=dict(arrowstyle="-", color=GREY))
    ax.annotate("no indicator blank", xy=(3.3, summ["D"][0]), xytext=(3.6, 5.07), fontsize=8, color=VERMILION,
                arrowprops=dict(arrowstyle="-", color=VERMILION))
    ax.set_xticks(range(len(learners)), [f"{k}\n0.1 g scale" if k == "F" else k for k in learners])
    ax.set_xlabel("learner (points: single titrations; squares: mean ± 95 % CI)")
    ax.set_ylabel("acetic acid / % w/w")
    ax.set_ylim(4.66, 5.10)
    ax.set_title("(a) D reads high; C and F scatter widely", loc="left", fontsize=10)

    # (b) titration curve and derivative
    v, ph = tit["V_NaOH_mL"], tit["pH"]
    vm, d, vep = end_point(v, ph)
    top.plot(v, ph, "o-", ms=3, lw=0.8, color=BLUE)
    top.set_ylabel("pH")
    top.set_title(f"(b) End point at {vep:.2f} mL from the steepest rise", loc="left", fontsize=10)
    bot.plot(vm, d, "o-", ms=3, lw=0.8, color=BLUE)
    bot.set_ylabel("ΔpH/ΔV / mL⁻¹")
    bot.set_xlabel("volume of NaOH added / mL")
    for a in (top, bot):
        a.axvline(vep, color=VERMILION, lw=1, ls="--")
    top.tick_params(labelbottom=False)
    for a in (ax, top, bot):
        a.spines[["top", "right"]].set_visible(False)

    out.parent.mkdir(exist_ok=True)
    fig.savefig(out, dpi=150)
    return fig, summ, vep


if __name__ == "__main__":
    vin, tit = load()
    out = HERE / "runs" / "good_figure.png"
    fig, summ, vep = good_figure(vin, tit, out)
    print("learner  mean / %   s / %    95 % CI half-width / %")
    for k, (m, s, h, n) in summ.items():
        print(f"   {k}     {m:.3f}    {s:.3f}    {h:.3f}")
    print(f"end point from the first derivative: {vep:.2f} mL")
    print(f"wrote {out.relative_to(HERE)}")
    if "--assets" in sys.argv:
        plt.rcParams["svg.fonttype"] = "none"
        assets = HERE.parent.parent / "assets"
        fig.savefig(assets / "m11-good-figure.svg")
        bad_figure(vin, tit, assets / "m11-bad-figure.svg")
        print("wrote assets/m11-good-figure.svg and assets/m11-bad-figure.svg")
    plt.close("all")
