"""Lesson 21.1 exercise: microstates, temperature and the Boltzmann distribution.

Fill in the functions marked TODO, then run this file. Reference solution: lesson01_microstates_solution.py.

Run from this folder:  py lesson01_microstates.py  [my_cups.csv]
my_cups.csv (optional) is your coins-and-cups tally with columns n,count
(n = coins in a cup, count = how many cup-snapshots had that many coins).
"""
import csv
import math
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from stat21 import HC_K, DIATOMIC, w0, B0

RUNS = Path(__file__).resolve().parent / "runs"


# ---------------- TODO 1 ----------------
def multiplicity(n_osc, quanta):
    """Number of ways W to share `quanta` identical energy quanta among `n_osc` oscillators."""
    # TODO: one line with math.comb: W = (q + N - 1)! / (q! (N - 1)!)
    return None


# ---------------- TODO 2 ----------------
def boltzmann_fractions(energies_cm, degeneracies, T):
    """Fraction of molecules in each level: g_i exp(-E_i/kT) / sum, energies in cm^-1."""
    # TODO: weights g_i * exp(-HC_K * E_i / T), then divide each by their sum; return a list
    return None


def two_solids(n_a=300, n_b=200, q_total=100):
    """W_total(q_A) for two Einstein solids sharing q_total quanta."""
    qa = np.arange(q_total + 1)
    ln_w = np.array([math.log(multiplicity(n_a, q)) + math.log(multiplicity(n_b, q_total - q)) for q in qa])
    return qa, ln_w


def exchange_game(n_osc=400, quanta=400, moves=200_000, seed=21):
    """Random energy exchange: move one quantum from a random non-empty oscillator to a random one."""
    rng = np.random.default_rng(seed)
    n = np.ones(n_osc, dtype=int) * (quanta // n_osc)
    for _ in range(moves):
        i = rng.integers(n_osc)
        if n[i] == 0:
            continue
        j = rng.integers(n_osc)
        n[i] -= 1
        n[j] += 1
    return n


def missing():
    """Names of the exercise functions that still return None (TODO)."""
    tests = {"multiplicity": lambda: multiplicity(3, 3),
             "boltzmann_fractions": lambda: boltzmann_fractions([0.0, 100.0], [1, 1], 300.0)}
    return [name for name, f in tests.items() if f() is None]


def main():
    if missing():
        print("TODO: write " + ", ".join(f"{m}()" for m in missing()) + " first (see lesson 21.1).")
        return
    RUNS.mkdir(exist_ok=True)

    # Part 1: two solids in thermal contact
    n_a, n_b, q_total = 300, 200, 100
    qa, ln_w = two_solids(n_a, n_b, q_total)
    k = int(np.argmax(ln_w))
    p = np.exp(ln_w - ln_w.max())
    p /= p.sum()
    print(f"W for 3 oscillators sharing 3 quanta: {multiplicity(3, 3)}")
    print(f"Two solids (N_A = {n_a}, N_B = {n_b}, q = {q_total}): most probable q_A = {qa[k]} "
          f"(equal sharing per oscillator would give {q_total * n_a / (n_a + n_b):.0f})")
    slope_a = math.log(multiplicity(n_a, k + 1)) - math.log(multiplicity(n_a, k))
    slope_b = math.log(multiplicity(n_b, q_total - k + 1)) - math.log(multiplicity(n_b, q_total - k))
    print(f"  d lnW_A/dq_A = {slope_a:.3f},  d lnW_B/dq_B = {slope_b:.3f}  (equal: same temperature)")
    inside = p[(qa >= k - 10) & (qa <= k + 10)].sum()
    print(f"  probability that q_A is within +/-10 of the peak: {inside:.3f}")

    # Part 2: exchange game -> Boltzmann (geometric) distribution
    n = exchange_game()
    counts = np.bincount(n)
    mean = n.mean()
    x = mean / (1 + mean)
    print(f"\nExchange game, 400 oscillators, mean {mean:.2f} quanta each:")
    print("  n   simulated  Boltzmann")
    for j in range(6):
        print(f"  {j}   {counts[j] / len(n):9.3f}  {(1 - x) * x**j:9.3f}")
    T_eff = 1 / math.log(1 / x)
    print(f"  ratio N(n+1)/N(n) = {x:.3f}, so kT = {T_eff:.2f} quanta")

    # Part 3: real molecules
    T = 298.15
    I2 = DIATOMIC["I2"]
    ev = [I2["we"] * (v + 0.5) - I2["wexe"] * (v + 0.5) ** 2 for v in range(6)]
    ev = [e - ev[0] for e in ev]
    fv = boltzmann_fractions(ev, [1] * 6, T)
    print(f"\nI2 vibrational populations at {T} K (v = 0..5): " + ", ".join(f"{f:.3f}" for f in fv))
    B = B0("HCl")
    js = list(range(31))
    fj = boltzmann_fractions([B * j * (j + 1) for j in js], [2 * j + 1 for j in js], T)
    jmax = int(np.argmax(fj))
    print(f"HCl rotational populations at {T} K: most populated J = {jmax} ({fj[jmax]:.3f}); "
          f"J = 0 holds {fj[0]:.3f}")
    print(f"HCl v = 1 population at {T} K: {math.exp(-HC_K * w0('HCl') / T):.1e}")

    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    ax[0].plot(qa, p)
    ax[0].set_xlabel("quanta in solid A")
    ax[0].set_ylabel("probability")
    ax[0].set_title("Two solids in contact")
    jj = np.arange(len(counts))
    ax[1].bar(jj, counts / len(n), label="exchange game")
    ax[1].plot(jj, (1 - x) * x**jj, "o-", color="k", label="Boltzmann")
    ax[1].set_xlabel("quanta in one oscillator")
    ax[1].set_ylabel("fraction")
    ax[1].legend()
    fig.tight_layout()
    fig.savefig(RUNS / "lesson01_microstates.png", dpi=120)
    print(f"\nPlot written to {RUNS / 'lesson01_microstates.png'}")

    if len(sys.argv) > 1:
        rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
        tally = {int(r["n"]): int(r["count"]) for r in rows}
        total = sum(tally.values())
        m = sum(k_ * c for k_, c in tally.items()) / total
        xx = m / (1 + m)
        print(f"\nYour cups: mean {m:.2f} coins per cup")
        for k_ in sorted(tally):
            print(f"  {k_} coins: measured {tally[k_] / total:.3f}, Boltzmann {(1 - xx) * xx**k_:.3f}")


if __name__ == "__main__":
    main()
