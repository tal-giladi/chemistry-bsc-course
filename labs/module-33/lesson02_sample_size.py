"""Lesson 33.2 (exercise: fill in the two TODO functions): how many repeats, how many molecules?

Run from this folder:
    py lesson02_sample_size.py
    py lesson02_sample_size.py 0.12 0.10      (pilot SD and target 95 % half-width, same unit)
Part 1: repeats of one measurement. From a pilot standard deviation s, the 95 % confidence half-width
        of the mean is t(0.975, n-1) s / sqrt(n) (Lesson 09.2). Find the smallest n that reaches the target.
Part 2: molecules in a benchmark. A scale factor c = sum(nu_exp nu_calc) / sum(nu_calc^2) is fitted
        through the origin (Lesson 31.4). Simulate how its standard error and the scaled RMS error settle
        as the number of molecules grows, by resampling example_parity.csv (generated demo data),
        and check every fit on 10 molecules that were never used to fit.
"""
import csv
import sys
from pathlib import Path

import numpy as np
from scipy import stats

HERE = Path(__file__).resolve().parent


def ci_halfwidth(s, n, conf=0.95):
    """Half-width of the confidence interval of a mean of n repeats with sample SD s.
    TODO: one line with stats.t.ppf(0.5 + conf / 2, n - 1)."""
    return None  # TODO


def repeats_needed(s, target, conf=0.95, n_max=1000):
    """Smallest n >= 2 whose half-width is <= target (None if n_max is not enough).
    TODO: loop n = 2, 3, ... and return the first n that meets the target. Four lines."""
    return None  # TODO


def scale_factor(nu_exp, nu_calc):
    """Least-squares scale factor through the origin and its standard error."""
    c = np.sum(nu_exp * nu_calc) / np.sum(nu_calc ** 2)
    resid = nu_exp - c * nu_calc
    se = np.sqrt(np.sum(resid ** 2) / (len(resid) - 1) / np.sum(nu_calc ** 2))
    return c, se


def read_parity(path):
    with open(path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    mol = np.array([r["molecule"] for r in rows])
    e = np.array([float(r["nu_exp_cm1"]) for r in rows])
    c = np.array([float(r["nu_calc_cm1"]) for r in rows])
    return mol, e, c


def main(argv):
    s = float(argv[1]) if len(argv) > 1 else 0.12
    target = float(argv[2]) if len(argv) > 2 else 0.10
    if ci_halfwidth(s, 5) is None:
        print("TODO: complete ci_halfwidth() and repeats_needed(), then run again.")
        return
    print("Part 1: repeats")
    for n in (3, 5, 7, 10):
        print(f"  n = {n:2d}: 95 % half-width = {ci_halfwidth(s, n):.3f}")
    print(f"  pilot SD {s:g}, target +-{target:g}: need n = {repeats_needed(s, target)}")

    mol, e, c = read_parity(HERE / "example_parity.csv")
    names = np.unique(mol)
    test = np.isin(mol, names[-10:])          # last 10 molecules: a fixed test set, never fitted
    pool = names[:-10]
    rng = np.random.default_rng(2)
    print("Part 2: molecules (generated demo data, 3 modes each; 10 molecules held out as a test set)")
    for k in (3, 5, 10, 20):
        cs, rms_in, rms_test = [], [], []
        for _ in range(500):
            m = np.isin(mol, rng.choice(pool, size=k, replace=False))
            cf, _ = scale_factor(e[m], c[m])
            cs.append(cf)
            rms_in.append(np.sqrt(np.mean((e[m] - cf * c[m]) ** 2)))
            rms_test.append(np.sqrt(np.mean((e[test] - cf * c[test]) ** 2)))
        print(f"  {k:2d} molecules: c = {np.mean(cs):.4f} +- {np.std(cs):.4f}; "
              f"RMS estimated from the fit {np.mean(rms_in):4.1f} +- {np.std(rms_in):3.1f} cm-1; "
              f"RMS on the test set {np.mean(rms_test):4.1f} cm-1")


if __name__ == "__main__":
    main(sys.argv)
