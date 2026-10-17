"""Lesson 09.3: propagation of uncertainty three ways.

Standardising NaOH with potassium hydrogen phthalate (KHP):  c = 1000 * m * P / (M * V)   (mol/L, V in mL)
1. the first-order formula (relative uncertainties in quadrature),
2. the uncertainties package (automatic first-order propagation, Lesson 05.3),
3. a Monte Carlo simulation (JCGM 101), which also works when the model is far from linear.

Fill in the two TODOs, then run (from this folder):
    py lesson03_propagation.py
Reference solution: lesson03_propagation_solution.py
"""
import math
from pathlib import Path

import numpy as np
from uncertainties import ufloat
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
RUNS = HERE / "runs"
N_MC = 1_000_000
rng = np.random.default_rng(2026)

# Inputs: value, standard uncertainty, and the distribution used in the Monte Carlo
M_KHP = 204.221                         # g/mol (PubChem CID 23676735: 204.22); its uncertainty is negligible
m = (0.5106, 0.0001 / math.sqrt(6))     # g, by difference on a 0.1 mg balance -> d/sqrt(6)
P = (0.9995, 0.0005 / math.sqrt(3))     # purity, certificate 99.95 +/- 0.05 %, rectangular
u_tol = 0.05 / math.sqrt(3)             # 50 mL Class A burette tolerance, rectangular
u_read = 0.01 * math.sqrt(2)            # two readings, 0.01 mL each
u_end = 0.03                            # judging the end point (about half a drop)
V = (24.87, math.sqrt(u_tol ** 2 + u_read ** 2 + u_end ** 2))   # mL


def conc(m_, p_, v_):
    return 1000 * m_ * p_ / (M_KHP * v_)


def first_order():
    c = conc(m[0], P[0], V[0])
    rel = {"mass": m[1] / m[0], "purity": P[1] / P[0], "volume": V[1] / V[0]}
    # TODO 1: combine the relative uncertainties in rel (square, add, square root).
    u_rel = None
    return c, c * u_rel, rel


def with_uncertainties():
    c = conc(ufloat(*m), ufloat(*P), ufloat(*V))
    return c.nominal_value, c.std_dev


def monte_carlo(m_mean=m[0], v_mean=V[0], u_v=V[1]):
    """Draw every input from its distribution, push each draw through the model, look at the spread."""
    half_p = P[1] * math.sqrt(3)                 # back to the half-width of the rectangle
    ms = rng.normal(m_mean, m[1], N_MC)
    ps = rng.uniform(P[0] - half_p, P[0] + half_p, N_MC)
    # TODO 2: draw N_MC volumes from a normal distribution (mean v_mean, sd u_v) and return conc(ms, ps, vs).
    raise NotImplementedError("TODO 2")


def main():
    RUNS.mkdir(exist_ok=True)
    print(f"V = {V[0]} mL, u(V) = {V[1]:.4f} mL (tolerance {u_tol:.4f}, reading {u_read:.4f}, end point {u_end})")
    c, u, rel = first_order()
    print(f"1. first-order formula:  c = {c:.5f} +/- {u:.5f} mol/L ({100 * u / c:.4f} %)")
    for k, r in rel.items():
        print(f"     {k:7s} {100 * r:.4f} %  share of variance {100 * r ** 2 / sum(x ** 2 for x in rel.values()):.1f} %")
    c2, u2 = with_uncertainties()
    print(f"2. uncertainties package: c = {c2:.5f} +/- {u2:.5f} mol/L")
    sim = monte_carlo()
    lo, hi = np.percentile(sim, [2.5, 97.5])
    print(f"3. Monte Carlo (1e6):    c = {sim.mean():.5f} +/- {sim.std():.5f} mol/L, 95 % interval [{lo:.5f}, {hi:.5f}]")

    print("\nA bad design: 0.0511 g KHP, so only 2.00 +/- 0.30 mL of titrant is needed (a tiny, uncertain volume)")
    c_lin = conc(0.0511, P[0], 2.00)
    u_lin = c_lin * 0.30 / 2.00
    sim2 = monte_carlo(0.0511, 2.00, 0.30)
    lo2, med2, hi2 = np.percentile(sim2, [2.5, 50, 97.5])
    print(f"   first order: c = {c_lin:.4f} +/- {u_lin:.4f}, 95 % interval [{c_lin - 1.96 * u_lin:.4f}, {c_lin + 1.96 * u_lin:.4f}]")
    print(f"   Monte Carlo: median {med2:.4f}, mean {sim2.mean():.4f}, 95 % interval [{lo2:.4f}, {hi2:.4f}]  (asymmetric)")

    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    ax[0].hist(sim, bins=200, density=True)
    ax[0].set(xlabel="c(NaOH) (mol/L)", title="Good design: 24.87 mL")
    ax[1].hist(sim2[(sim2 > 0) & (sim2 < 0.3)], bins=200, density=True)
    ax[1].set(xlabel="c (mol/L)", title="Bad design: 2.00 +/- 0.30 mL")
    fig.tight_layout()
    fig.savefig(RUNS / "lesson03_propagation.png", dpi=120)
    print("plot written to runs/lesson03_propagation.png")


if __name__ == "__main__":
    main()
