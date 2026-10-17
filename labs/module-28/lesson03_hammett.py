"""Lesson 28.3 - Hammett plots from evaluated pKa values.

Fill in the functions marked TODO. Reference solution: lesson03_hammett_solution.py

First run  py fetch_iupac_pka.py  once (downloads the IUPAC Digitized pKa Dataset, about 7 MB).
Run:  py lesson03_hammett.py
Writes runs/lesson03_hammett.png.
"""
import csv
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from sr28 import HERE, line_fit, runs_dir, sigma_table

TABLE = HERE / "data" / "downloaded" / "aromatic_pka.csv"
# para groups that can conjugate directly with a negative charge (phenoxide) or a lone pair (aniline)
THROUGH_CONJUGATING = {"NO2", "CN", "COCH3"}


def load_pka():
    """{series: {(position, substituent): pKa}} from the extracted IUPAC table."""
    if not TABLE.exists():
        sys.exit("data/downloaded/aromatic_pka.csv not found: run  py fetch_iupac_pka.py  first.")
    out = {}
    with open(TABLE, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            out.setdefault(r["series"], {})[(r["position"], r["substituent"])] = float(r["pKa"])
    return out


def sigma_from_benzoic(benzoic):
    """Hammett's definition: sigma_X = pKa(benzoic acid) - pKa(X-benzoic acid), water, 25 C."""
    # TODO: ref = benzoic[("", "H")]  (the parent acid; key is (position, substituent))
    # TODO: return {key: ref - pka for every other key}
    raise NotImplementedError("TODO: write sigma_from_benzoic() first (see the hints in the code).")


def log_k_ratio(series_pka):
    """log10(K_X / K_H) = pKa(H) - pKa(X) for every substituted member of a series."""
    # TODO: same pattern as sigma_from_benzoic(): pKa(parent) - pKa(substituted) for every substituted member
    raise NotImplementedError("TODO: write log_k_ratio() first (see the hints in the code).")


def hammett_points(series_pka, sigma, exclude_para=()):
    """Matching (sigma, log K/K0, label) lists; para groups in exclude_para are left out."""
    xs, ys, labels = [], [], []
    for (pos, name), y in sorted(log_k_ratio(series_pka).items()):
        if name not in sigma or (pos == "p" and name in exclude_para):
            continue
        xs.append(sigma[name][pos])
        ys.append(y)
        labels.append(f"{pos}-{name}")
    return np.array(xs), np.array(ys), labels


def effective_sigma(series_pka, rho, names):
    """sigma a para group 'needs' to sit on the line: log(K/K0) / rho (this is sigma-minus)."""
    # TODO: lk = log_k_ratio(series_pka); return {n: lk[("p", n)] / rho for n in names if ("p", n) in lk}
    raise NotImplementedError("TODO: write effective_sigma() first (see the hints in the code).")


def main():
    data = load_pka()
    sigma = sigma_table()

    own = sigma_from_benzoic(data["benzoic acid"])
    print("sigma from IUPAC benzoic acid pKa vs Hansch-Leo-Taft table:")
    diffs = []
    for (pos, name), s in sorted(own.items()):
        if name in sigma:
            diffs.append(s - sigma[name][pos])
            print(f"  {pos}-{name:6s} this data {s:+.3f}   table {sigma[name][pos]:+.2f}")
    print(f"  mean absolute difference {np.mean(np.abs(diffs)):.3f} over {len(diffs)} substituents")

    fig, axes = plt.subplots(1, 3, figsize=(14, 4.3))
    x, y, lab = hammett_points(data["benzoic acid"], sigma)
    fit = line_fit(x, y)
    print(f"benzoic acids: rho = {fit['slope']:.3f} +/- {fit['s_slope']:.3f}, R2 = {fit['r2']:.3f} (1 by definition)")
    axes[0].plot(x, y, "o")
    axes[0].plot(x, fit["intercept"] + fit["slope"] * x, "-")
    axes[0].set(title="Benzoic acids (defines sigma)")

    for ax, series in zip(axes[1:], ("phenol", "anilinium")):
        x, y, lab = hammett_points(data[series], sigma, exclude_para=THROUGH_CONJUGATING)
        fit = line_fit(x, y)
        print(f"{series}: rho = {fit['slope']:.2f} +/- {fit['s_slope']:.2f}, intercept {fit['intercept']:+.2f}, "
              f"R2 = {fit['r2']:.3f}, n = {len(x)}")
        eff = effective_sigma(data[series], fit["slope"], THROUGH_CONJUGATING)
        for n, s in eff.items():
            print(f"    p-{n}: sigma_p {sigma[n]['p']:.2f}, effective sigma (sigma-minus) {s:.2f}")
        ax.plot(x, y, "o", label="meta and normal para")
        xx = np.linspace(-0.3, 1.3, 2)
        ax.plot(xx, fit["intercept"] + fit["slope"] * xx, "-", label=f"rho = {fit['slope']:.2f}")
        lk = log_k_ratio(data[series])
        for n in eff:
            ax.plot(sigma[n]["p"], lk[("p", n)], "rs")
            ax.annotate(f"p-{n}", (sigma[n]["p"], lk[("p", n)]), xytext=(4, 4), textcoords="offset points")
        ax.set(title=f"{series} pKa, water, 25 C")
        ax.legend(fontsize=8)
    for ax in axes:
        ax.set(xlabel="sigma (Hansch-Leo-Taft)", ylabel="log(K/K0)")
    fig.tight_layout()
    out = runs_dir() / "lesson03_hammett.png"
    fig.savefig(out, dpi=120)
    print(f"Saved {out.name}")


if __name__ == "__main__":
    main()
