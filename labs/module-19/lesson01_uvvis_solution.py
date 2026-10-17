"""Lesson 19.1: Beer-Lambert calibration, stray light, linear range and photometric error.

Reference solution. Run from this folder:
    py lesson01_uvvis_solution.py
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

from ana19 import HERE, read_csv, line_fit, conc_from_line, save


def stray_absorbance(A_true, s):
    """Absorbance the instrument reports when a fraction s of the light is stray (Harvey 10.2)."""
    # TODO 1
    T = 10.0 ** (-A_true)
    return -np.log10((T + s) / (1 + s))


def rel_conc_error(A, s_T):
    """Relative standard deviation of c when the transmittance noise s_T is constant (Harvey 10.3)."""
    # TODO 2
    T = 10.0 ** (-A)
    return 0.4343 * s_T / (T * np.abs(np.log10(T)))


def main():
    d = read_csv(HERE / "dye_uvvis.csv")
    std = d["type"] == "standard"
    c, A = d["c_mg_per_L"][std], d["absorbance"][std]

    m_all, b_all, s_all, res_all = line_fit(c, A)
    print(f"All 10 standards:   A = {b_all:.4f} + {m_all:.4f} c   s_r = {s_all:.4f}")
    print("   residuals: " + " ".join(f"{r:+.3f}" for r in res_all))

    low = c <= 6
    m, b, s_r, res = line_fit(c[low], A[low])
    print(f"Standards 0-6 mg/L: A = {b:.4f} + {m:.4f} c   s_r = {s_r:.4f}")

    (a_fit, s_fit), cov = curve_fit(lambda x, a, s: stray_absorbance(a * x, s), c, A, p0=[0.15, 0.001])
    print(f"Stray-light model on all standards: absorptivity a = {a_fit:.4f} L mg-1 cm-1, stray fraction s = {100 * s_fit:.2f} %")
    print(f"   highest absorbance this instrument can ever report: -log10(s/(1+s)) = {-np.log10(s_fit / (1 + s_fit)):.2f}")
    for A_t in (0.5, 1.0, 1.5, 2.0):
        A_o = stray_absorbance(A_t, s_fit)
        print(f"   true A {A_t:.1f} reads {A_o:.3f}  ({100 * (A_o - A_t) / A_t:+.1f} %)")

    und = d["absorbance"][d["type"] == "undiluted"]
    dil = d["absorbance"][d["type"] == "diluted_1to20"]
    c_und = (und.mean() - b) / m
    c_dil, s_dil = conc_from_line(dil, c[low], A[low], m, b, s_r)
    print(f"Undiluted drink reads A = {und.mean():.3f}: the 0-6 line would say {c_und:.1f} mg/L (meaningless, above every standard)")
    print(f"Diluted 1+19 reads A = {dil.mean():.3f}: {c_dil:.3f} +/- {s_dil:.3f} mg/L in the cell, so {20 * c_dil:.1f} +/- {20 * s_dil:.1f} mg/L in the drink")

    s_T = 0.002
    grid = np.array([0.05, 0.1, 0.2, 0.4343, 0.7, 1.0, 1.5, 2.0])
    print(f"Relative error of c for s_T = {s_T} (0.2 %T):")
    for Ai, e in zip(grid, rel_conc_error(grid, s_T)):
        print(f"   A = {Ai:6.4f}: {100 * e:5.2f} %")

    fig, ax = plt.subplots(1, 3, figsize=(13, 4))
    cc = np.linspace(0, 20, 200)
    ax[0].plot(c, A, "o", label="standards")
    ax[0].plot(cc, b + m * cc, "--", label="line from 0-6 mg/L")
    ax[0].plot(cc, stray_absorbance(a_fit * cc, s_fit), "-", label="stray-light model")
    ax[0].set(xlabel="c (mg/L)", ylabel="absorbance", title="Calibration, 1 cm cell")
    ax[0].legend()
    ax[1].axhline(0, color="grey", lw=0.8)
    ax[1].plot(c, res_all, "o")
    ax[1].set(xlabel="c (mg/L)", ylabel="residual", title="Residuals of the straight line on all points")
    AA = np.linspace(0.03, 2.5, 300)
    ax[2].plot(AA, 100 * rel_conc_error(AA, s_T))
    ax[2].set(xlabel="absorbance", ylabel="relative error of c (%)", title="Photometric error, s_T = 0.002", ylim=(0, 3))
    save(fig, "lesson01_uvvis.png")


if __name__ == "__main__":
    main()
