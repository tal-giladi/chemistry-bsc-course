"""Lesson 05.2 reference solution: Maxwell-Boltzmann speeds of N2 with numpy arrays.

Usage (from this folder):
    py lesson02_maxwell_solution.py
The figure is saved to runs/lesson02_maxwell.png next to this file.
"""
import time
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent

K_B = 1.380649e-23          # J/K, exact (SI 2019; CODATA 2022)
M_U = 1.66053906892e-27     # kg, atomic mass constant (CODATA 2022)
M_N2 = 2 * 14.007 * M_U     # kg per N2 molecule (IUPAC abridged atomic weight of N)


def mb_pdf(v, T, m=M_N2):
    """Maxwell-Boltzmann speed distribution f(v) in s/m, vectorised over v and T.
    f(v) = 4 pi (m / (2 pi k T))^(3/2) v^2 exp(-m v^2 / (2 k T))"""
    a = m / (2 * K_B * T)
    return 4 * np.pi * (a / np.pi) ** 1.5 * v**2 * np.exp(-a * v**2)


def mean_speed(v, f):
    """Mean speed <v> = integral of v f(v) dv, for each row of f (one row per temperature)."""
    return np.trapezoid(v * f, v, axis=-1)


def fraction_above(v, f, v_cut):
    """Fraction of molecules faster than v_cut = integral of f from v_cut to the end of the grid."""
    return np.trapezoid(np.where(v > v_cut, f, 0.0), v, axis=-1)


def mb_pdf_loop(v, T, m=M_N2):
    """The same thing with a Python loop, to compare speed. Do not write code like this."""
    out = []
    for vi in v:
        a = m / (2 * K_B * T)
        out.append(4 * np.pi * (a / np.pi) ** 1.5 * vi**2 * np.exp(-a * vi**2))
    return np.array(out)


def main():
    v = np.linspace(0, 2500, 2501)                 # m/s, 1 m/s steps
    T = np.array([200.0, 298.15, 500.0])[:, None]  # column: shape (3, 1)
    f = mb_pdf(v, T)                               # broadcasting -> shape (3, 2501)
    print(f"v has shape {v.shape}, T has shape {T.shape}, f has shape {f.shape}")

    area = np.trapezoid(f, v, axis=1)
    v_mean_num = mean_speed(v, f)
    v_mean_formula = np.sqrt(8 * K_B * T[:, 0] / (np.pi * M_N2))
    v_mp = v[np.argmax(f, axis=1)]
    v_mp_formula = np.sqrt(2 * K_B * T[:, 0] / M_N2)
    above = fraction_above(v, f, 1000.0)

    print(f"{'T (K)':>8}{'area':>9}{'<v> num':>10}{'<v> formula':>13}{'v_mp grid':>11}"
          f"{'v_mp formula':>14}{'P(v>1000)':>11}")
    for i, Ti in enumerate(T[:, 0]):
        print(f"{Ti:8.2f}{area[i]:9.5f}{v_mean_num[i]:10.1f}{v_mean_formula[i]:13.1f}"
              f"{v_mp[i]:11.0f}{v_mp_formula[i]:14.1f}{above[i]:11.4f}")

    t0 = time.perf_counter(); mb_pdf_loop(v, 298.15); t1 = time.perf_counter()
    mb_pdf(v, 298.15); t2 = time.perf_counter()
    print(f"loop {1e3 * (t1 - t0):.2f} ms vs vectorised {1e3 * (t2 - t1):.3f} ms "
          f"(about {(t1 - t0) / max(t2 - t1, 1e-9):.0f}x faster)")

    (HERE / "runs").mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    for i, Ti in enumerate(T[:, 0]):
        ax.plot(v, f[i] * 1e3, label=f"{Ti:.0f} K")
    ax.set_xlabel("speed $v$ (m/s)")
    ax.set_ylabel("$f(v)$ (10$^{-3}$ s/m)")
    ax.set_title("Maxwell-Boltzmann speeds of N$_2$")
    ax.legend()
    fig.tight_layout()
    out = HERE / "runs" / "lesson02_maxwell.png"
    fig.savefig(out, dpi=120)
    print(f"plot saved to runs/{out.name}")


if __name__ == "__main__":
    main()
