"""Lesson 11.3 — a deliberately BAD figure. Do not copy its style: list what is wrong with it.

It plots the class vinegar results (class_vinegar.csv) and a titration curve (titration_curve.csv).
Run from this folder:  py bad_figure.py   -> runs/bad_figure.png
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent


def read_csv(path):
    """Read a small CSV with '#' comment lines into a dict of numpy arrays (numbers where possible)."""
    lines = [ln for ln in Path(path).read_text(encoding="utf-8").splitlines() if ln and not ln.startswith("#")]
    head = lines[0].split(",")
    cols = list(zip(*(ln.split(",") for ln in lines[1:])))
    out = {}
    for name, col in zip(head, cols):
        try:
            out[name] = np.array(col, dtype=float)
        except ValueError:
            out[name] = np.array(col)
    return out


def load():
    return read_csv(HERE / "class_vinegar.csv"), read_csv(HERE / "titration_curve.csv")


def bad_figure(vin, tit, out):
    learners = sorted(set(vin["learner"]))
    means = [vin["acid_percent_ww"][vin["learner"] == k].mean() for k in learners]
    sds = [vin["acid_percent_ww"][vin["learner"] == k].std() for k in learners]
    colours = plt.cm.jet(np.linspace(0, 1, len(learners)))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    bars = ax1.bar(learners, means, color=colours, edgecolor="black", linewidth=2)
    ax1.errorbar(learners, means, yerr=[np.zeros(len(sds)), sds], fmt="none", ecolor="black", capsize=8)
    ax1.set_ylim(4.85, 5.05)
    ax1.set_title("Results")
    ax1.set_ylabel("Result")
    ax1.legend(bars, learners, loc="upper left", ncol=3)
    ax1.grid(True, linewidth=1.5)

    v, ph = tit["V_NaOH_mL"], tit["pH"]
    d = np.gradient(ph, v)
    ax2.plot(v, ph, "-o", color="red")
    ax2b = ax2.twinx()
    sc = ax2b.scatter(v, d, c=v, cmap="jet", s=40)
    fig.colorbar(sc, ax=ax2b)
    ax2.set_title("Titration")
    ax2.grid(True, linewidth=1.5)

    fig.tight_layout()
    out.parent.mkdir(exist_ok=True)
    fig.savefig(out, dpi=100)
    plt.close(fig)


if __name__ == "__main__":
    vin, tit = load()
    out = HERE / "runs" / "bad_figure.png"
    bad_figure(vin, tit, out)
    print(f"wrote {out.relative_to(HERE)}")
