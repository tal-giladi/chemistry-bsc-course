"""Lesson 23.4 (exercise: fill in the TODO functions): kinetics of a blue food dye fading in dilute bleach, from phone photos.

Run from this folder:
    py lesson04_dye_fading.py                        (uses dye_fading_example.csv)
    py lesson04_dye_fading.py my_dye_fading.csv      (columns run,type,T_C,bleach_mL,t_s,R,G,B;
                                                      type = blank or sample; RGB from rgb_from_photos.py
                                                      in the Module 9 lab folder)
Steps: (1) red channel -> linear intensity -> pseudo-absorbance against the run's blank (lesson 09.6);
(2) fit A(t) = A0 exp(-k t) + A_inf for each run (pseudo-first-order, isolation method);
(3) order in hypochlorite from two bleach volumes; (4) a rough activation energy from two temperatures.
Writes runs/lesson04_dye_fading.png.
"""
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import curve_fit

from pc23 import HERE, R, read_csv, srgb_to_linear, linfit, todo, save_plot, pyplot


def pseudo_absorbance(R_sample, R_blank):
    """A = -log10(I / I_blank) with I the LINEAR red intensity (undo sRGB first with srgb_to_linear).
    A blue dye absorbs red light, so the red channel carries the signal.
    TODO: two lines."""
    return None  # TODO


def decay(t, A0, k, A_inf):
    return A0 * np.exp(-k * t) + A_inf


def fit_run(t, A):
    """Fit decay() to one run. Returns (k, sigma_k, A0, A_inf)."""
    p0 = (A[0] - A[-1], 1.0 / max(t[-1], 1), max(A[-1], 0.0))
    popt, pcov = curve_fit(decay, t, A, p0=p0)
    return popt[1], float(np.sqrt(pcov[1, 1])), popt[0], popt[2]


def order_in_bleach(k1, v1, k2, v2):
    """k' = k [OCl-]^n, and [OCl-] is proportional to the bleach volume: n = ln(k2/k1) / ln(v2/v1).
    TODO: one line."""
    return None  # TODO


def activation_energy(k1, T1_C, k2, T2_C):
    """Two-point Arrhenius: Ea = R ln(k2/k1) / (1/T1 - 1/T2), temperatures in kelvin. Returns J/mol.
    TODO: one line (convert C to K)."""
    return None  # TODO


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "dye_fading_example.csv"
    rows = read_csv(path)
    if todo(pseudo_absorbance(np.array([100.0]), np.array([200.0])), order_in_bleach(1, 1, 2, 2),
            activation_energy(1, 20, 2, 30)):
        return
    runs = {}
    for r in rows:
        runs.setdefault(r["run"], {"blank": [], "t": [], "R": [], "T": float(r["T_C"]), "v": float(r["bleach_mL"])})
        if r["type"] == "blank":
            runs[r["run"]]["blank"].append(float(r["R"]))
        else:
            runs[r["run"]]["t"].append(float(r["t_s"]))
            runs[r["run"]]["R"].append(float(r["R"]))

    results = {}
    for name, d in runs.items():
        t, Rs = np.array(d["t"]), np.array(d["R"])
        A = pseudo_absorbance(Rs, np.mean(d["blank"]))
        k, sk, A0, Ainf = fit_run(t, A)
        early = A - Ainf > 0.25 * A0                          # about the first two half-lives
        a, b, sa, sb, _, _ = linfit(t[early], np.log(A[early] - Ainf))
        results[name] = (k, sk, d["T"], d["v"], t, A)
        print(f"run {name}: {d['v']:.1f} mL bleach, {d['T']:.0f} C: A0 = {A0:.3f}, A_inf = {Ainf:.3f}, "
              f"k' = {k * 1000:.2f} +/- {sk * 1000:.2f} 1e-3/s (ln-plot slope {-b * 1000:.2f}), "
              f"half-life {np.log(2) / k / 60:.1f} min")

    names = sorted(results)
    same_T = [n for n in names if results[n][2] == results[names[0]][2]]
    if len(same_T) >= 2:
        n1, n2 = same_T[0], same_T[1]
        n = order_in_bleach(results[n1][0], results[n1][3], results[n2][0], results[n2][3])
        rel = np.hypot(results[n1][1] / results[n1][0], results[n2][1] / results[n2][0])
        print(f"order in hypochlorite (runs {n1}, {n2}): n = {n:.2f} +/- {rel / np.log(results[n2][3] / results[n1][3]):.2f}")
    same_v = [n for n in names if results[n][3] == results[names[0]][3] and results[n][2] != results[names[0]][2]]
    if same_v:
        n1, n2 = names[0], same_v[0]
        ea = activation_energy(results[n1][0], results[n1][2], results[n2][0], results[n2][2])
        print(f"activation energy (runs {n1}, {n2}): Ea = {ea / 1000:.0f} kJ/mol (two points only: a rough value)")

    plt = pyplot()
    if plt is None:
        return
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.6))
    for name in names:
        k, sk, T, v, t, A = results[name]
        a1.plot(t / 60, A, "o", ms=3, label=f"{name}: {v:.0f} mL, {T:.0f} C")
        A0, kk, Ainf = curve_fit(decay, t, A, p0=(A[0], k, 0.01))[0]
        a1.plot(t / 60, decay(t, A0, kk, Ainf), "-", lw=1)
        a2.plot(t / 60, np.log(np.clip(A - Ainf, 1e-4, None)), "o", ms=3, label=name)
    a1.set_xlabel("t (min)")
    a1.set_ylabel("pseudo-absorbance (red)")
    a1.legend(fontsize=8)
    a2.set_xlabel("t (min)")
    a2.set_ylabel("ln(A - A_inf)")
    save_plot(fig, "lesson04_dye_fading.png")


if __name__ == "__main__":
    main()
