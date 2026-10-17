"""Lesson 09.2: mean, standard deviation, confidence interval and significance tests.

Fill in the two TODOs, then run (from this folder):
    py lesson02_stats.py                           # example data (replicates.csv)
    py lesson02_stats.py my_repeats.csv            # your data, same columns: method,value
Reference solution: lesson02_stats_solution.py
"""
import sys
from pathlib import Path

import numpy as np
from scipy import stats

HERE = Path(__file__).resolve().parent
CERTIFIED = 25.0      # mg/L
ALPHA = 0.05          # 95 % confidence
REMOVE_OUTLIERS = True    # set to False to keep a value that Grubbs flags


def read_groups(path):
    lines = [r for r in Path(path).read_text(encoding="utf-8").splitlines() if r.strip() and not r.startswith("#")]
    groups = {}
    for r in lines[1:]:
        name, value = r.split(",")[:2]
        groups.setdefault(name, []).append(float(value))
    return {k: np.array(v) for k, v in groups.items()}


def summary(x):
    """Mean, sample standard deviation, RSD (%) and the 95 % confidence interval half-width t*s/sqrt(n)."""
    n, mean, s = x.size, x.mean(), x.std(ddof=1)
    t = stats.t.ppf(1 - ALPHA / 2, n - 1)
    # TODO 1: the 95 % confidence-interval half-width is t * s / sqrt(n).
    half = None
    return n, mean, s, 100 * s / mean, half, t


def grubbs(x):
    """Grubbs' test for one outlier (two-sided). Returns G, the critical value and the index of the suspect."""
    n = x.size
    dev = np.abs(x - x.mean())
    i = int(dev.argmax())
    # TODO 2: Grubbs' G is the largest absolute deviation from the mean divided by the sample standard deviation.
    g = None
    t = stats.t.ppf(1 - ALPHA / (2 * n), n - 2)
    g_crit = (n - 1) / np.sqrt(n) * np.sqrt(t ** 2 / (n - 2 + t ** 2))
    return g, g_crit, i


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "replicates.csv"
    groups = read_groups(path)
    print(f"Data: {path.name}; certified value {CERTIFIED}")
    for name, x in list(groups.items()):
        if x.std(ddof=1) == 0:
            print(f"\n{name}: all {x.size} results are {x[0]}, so s = 0. The instrument's resolution hides the scatter;")
            print("   report at least the resolution uncertainty d/sqrt(12) instead (Lesson 01.5).")
            del groups[name]
            continue
        g, g_crit, i = grubbs(x)
        flag = "OUTLIER" if g > g_crit else "keep"
        print(f"\n{name}: Grubbs G = {g:.2f} vs G_crit = {g_crit:.2f} for result {i + 1} ({x[i]}) -> {flag}")
        if g > g_crit and REMOVE_OUTLIERS:
            print("   (removed for the tests below; check the notebook for a reason before you do this for real)")
            groups[name] = x = np.delete(x, i)
        n, mean, s, rsd, half, t = summary(x)
        print(f"   n={n} mean={mean:.3f} s={s:.3f} RSD={rsd:.2f} %  95 % CI = {mean:.2f} +/- {half:.2f} (t={t:.3f})")
        res = stats.ttest_1samp(x, CERTIFIED)
        t_exp = abs(mean - CERTIFIED) / (s / np.sqrt(n))
        verdict = "significant bias" if res.pvalue < ALPHA else "no significant bias"
        print(f"   one-sample t-test vs {CERTIFIED}: t_exp={t_exp:.2f}, t_crit={t:.3f}, p={res.pvalue:.4f} -> {verdict}")

    if len(groups) == 2:
        (n1, a), (n2, b) = groups.items()
        f = max(a.var(ddof=1), b.var(ddof=1)) / min(a.var(ddof=1), b.var(ddof=1))
        num, den = (a.size - 1, b.size - 1) if a.var(ddof=1) >= b.var(ddof=1) else (b.size - 1, a.size - 1)
        f_crit = stats.f.ppf(1 - ALPHA / 2, num, den)
        equal = f < f_crit
        print(f"\nF-test {n1} vs {n2}: F={f:.2f}, F_crit={f_crit:.2f} -> "
              f"{'variances can be pooled' if equal else 'variances differ'}")
        res = stats.ttest_ind(a, b, equal_var=equal)
        print(f"two-sample t-test ({'pooled' if equal else 'Welch'}): t={abs(res.statistic):.2f}, p={res.pvalue:.4f} -> "
              f"{'the methods differ' if res.pvalue < ALPHA else 'no significant difference'}")


if __name__ == "__main__":
    main()
