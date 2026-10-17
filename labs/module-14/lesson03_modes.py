"""Lesson 14.3 hands-on: normal modes of three coupled oscillators.

1. Build the mass and force-constant matrices of a chain of masses and springs (with or without
   walls) and solve K v = omega^2 M v with scipy.linalg.eigh.
2. Three equal masses between two walls: frequencies sqrt(2 - sqrt2), sqrt2, sqrt(2 + sqrt2) x sqrt(k/m).
3. Three pendulums joined by rubber bands: omega^2 = g/L + c {0, 1, 3}. Fit g/L and c to the
   measured mode periods and check the 0 : 1 : 3 pattern.
4. Release pendulum 1 alone: predict how its swing passes to the others (modal superposition).

Run:   py lesson03_modes.py                     (example data)
       py lesson03_modes.py my_pendulums.csv    (header mode,trial,t10_s)
The plot is saved to runs/lesson03_modes.png next to this file.
Fill in the functions marked TODO. Reference solution: lesson03_modes_solution.py
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import eigh

HERE = Path(__file__).resolve().parent
G = 9.795
L_PEND = 0.500   # m, pivot to centre of the bob; put your own length here
SWINGS = 10


def chain_K(springs, walls):
    """Force-constant matrix of masses in a line.
    walls=False: springs[i] joins mass i and i+1 (n-1 springs for n masses).
    walls=True:  springs[0] joins the left wall and mass 0, springs[-1] mass n-1 and the right wall
                 (n+1 springs for n masses)."""
    springs = list(springs)
    n = len(springs) - 1 if walls else len(springs) + 1
    K = np.zeros((n, n))
    pairs = [(i - 1, i) for i in range(n + 1)] if walls else [(i, i + 1) for i in range(n - 1)]
    for k, (i, j) in zip(springs, pairs):
        for a in (i, j):
            if 0 <= a < n:
                K[a, a] += k
        if 0 <= i < n and 0 <= j < n:
            K[i, j] -= k
            K[j, i] -= k
    return K


def normal_modes(K, masses):
    """Angular frequencies (ascending) and mode shapes (columns) from K v = w^2 M v."""
    # TODO: w2, V = eigh(K, np.diag(masses)); return np.sqrt(np.clip(w2, 0, None)), V
    return None


def fit_pendulum_modes(lam, omega):
    """Least-squares straight line omega^2 = w0^2 + c lam. Return w0^2, c and the residuals."""
    # TODO: least squares for omega^2 = w0sq + c lam: build A = [1, lam] columns,
    #       np.linalg.lstsq(A, omega**2); return w0sq, c, residuals
    return None


def release_one(omegas, V, masses, t, x0=0.04):
    """Displacements when mass 0 starts at x0 and everything else at rest, as a sum of modes."""
    start = np.zeros(len(masses))
    start[0] = x0
    amps = V.T @ np.diag(masses) @ start        # modal amplitudes (V is M-orthonormal)
    return (V * amps) @ np.cos(np.outer(omegas, t))


def main():
    print("Three equal masses (1 kg) between walls, four equal springs (1 N/m):")
    w, V = normal_modes(chain_K([1, 1, 1, 1], walls=True), [1, 1, 1])
    for i in range(3):
        shape = V[:, i] / np.max(np.abs(V[:, i]))
        print(f"  mode {i + 1}: omega = {w[i]:.4f} sqrt(k/m)   shape {np.round(shape, 3)}")
    print("  exact: sqrt(2 - sqrt2) = 0.7654, sqrt2 = 1.4142, sqrt(2 + sqrt2) = 1.8478")

    print("\nFree chain (no walls), springs 1 N/m: one zero mode (the whole chain sliding):")
    w, _ = normal_modes(chain_K([1, 1], walls=False), [1, 1, 1])
    print(f"  omega = {np.round(w, 4)} sqrt(k/m)   (0, 1, sqrt3)")

    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "coupled_pendulums_example.csv"
    mode, _, t10 = np.loadtxt(path, delimiter=",", skiprows=1, unpack=True)
    modes = np.unique(mode).astype(int)
    T = np.array([t10[mode == m].mean() / SWINGS for m in modes])
    uT = np.array([t10[mode == m].std(ddof=1) / SWINGS / np.sqrt((mode == m).sum()) for m in modes])
    omega = 2 * np.pi / T
    lam = np.array([0.0, 1.0, 3.0])[modes - 1]
    w0sq, c, res = fit_pendulum_modes(lam, omega)
    print(f"\nPendulums ({path.name}):")
    for m, Ti, ui, r in zip(modes, T, uT, res):
        print(f"  mode {m}: T = {Ti:.4f} +/- {ui:.4f} s, f = {1 / Ti:.4f} Hz, residual in omega^2 {r:+.3f} 1/s^2")
    print(f"  fit: g/L = {w0sq:.2f} 1/s^2 (expected {G / L_PEND:.2f} for L = {L_PEND} m), "
          f"coupling c = {c:.3f} 1/s^2")
    print(f"  coupling strength c / (g/L) = {c / w0sq * 100:.1f} %  (weak coupling: modes close together)")

    # Model of the chain: K = (m g/L) I + kappa * free-chain Laplacian, per unit mass.
    K = w0sq * np.eye(3) + chain_K([c, c], walls=False)
    omegas, V = normal_modes(K, [1.0, 1.0, 1.0])
    t = np.linspace(0, 120, 6001)
    x = release_one(omegas, V, [1.0, 1.0, 1.0], t)
    env = np.array([np.max(np.abs(x[0, max(0, i - 50):i + 50])) for i in range(0, t.size, 25)])
    tt = t[::25]
    low = tt[np.argmax(env < 0.35 * env[0])]
    print(f"  release pendulum 1 alone: its swing first falls below a third of the start near "
          f"t = {low:.0f} s, while pendulums 2 and 3 carry the energy")
    print(f"  slowest beat period 2 pi/(w2 - w1) = {2 * np.pi / (omegas[1] - omegas[0]):.0f} s")

    (HERE / "runs").mkdir(exist_ok=True)
    fig, axs = plt.subplots(3, 1, figsize=(8, 5.5), sharex=True)
    for i, ax in enumerate(axs):
        ax.plot(t, x[i] * 100, lw=0.6)
        ax.set_ylabel(f"x{i + 1} (cm)")
    axs[-1].set_xlabel("time (s)")
    axs[0].set_title("release pendulum 1 alone: energy moves along the chain and back")
    fig.tight_layout()
    fig.savefig(HERE / "runs" / "lesson03_modes.png", dpi=120)
    print("Plot saved to runs/lesson03_modes.png")


if __name__ == "__main__":
    try:
        main()
    except TypeError as exc:
        print(f"Fill in the functions marked TODO first ({exc}).")
