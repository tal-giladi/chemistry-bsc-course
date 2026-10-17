"""Lesson 25.1 (reference solution): calibrate a phone + DVD spectrometer with fluorescent-lamp lines,
build absorbance spectra of food dyes, check Beer-Lambert, and analyse a two-dye mixture.

Run (from this folder):
    py lesson01_phone_spectrometer_solution.py                    # example data
    py lesson01_phone_spectrometer_solution.py my_spectra.csv     # your own (same columns, see README)
"""
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

from ana25 import HERE, read_csv, line_fit, save

HG_EU_LINES = [404.66, 435.83, 546.07, 578.0, 611.6]   # nm: Hg lines (NIST ASD; 578.0 = the unresolved
# 576.96/579.07 doublet) and the Eu3+ red phosphor line of a compact fluorescent lamp


def find_lamp_lines(cfl):
    """Return the pixel positions of the five strongest narrow lamp lines, sorted by pixel."""
    y = cfl / cfl.max()
    peaks, props = find_peaks(y, prominence=0.08, width=(1, 15))
    best = peaks[np.argsort(props["prominences"])[::-1][:len(HG_EU_LINES)]]
    return np.sort(best)


def calibrate(pixels, wavelengths):
    """Fit wavelength = c0 + c1 p + c2 p^2 through the lamp lines. Returns the coefficients (highest first)."""
    return np.polyfit(pixels, wavelengths, 2)


def absorbance(I, I_blank):
    """Pseudo-absorbance A = -log10(I / I_blank); nan where the blank is too dim to trust (< 5 % of its maximum)."""
    A = -np.log10(I / I_blank)
    A[I_blank < 0.05 * I_blank.max()] = np.nan
    return A


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else HERE / "phone_spectra_example.csv"
    d = read_csv(path)
    px = d["pixel"]

    lines_px = find_lamp_lines(d["cfl"])
    coef = calibrate(lines_px, HG_EU_LINES)
    lam = np.polyval(coef, px)
    resid = np.polyval(coef, lines_px) - HG_EU_LINES
    print("Lamp lines found at pixels", lines_px.tolist())
    print(f"Calibration: lambda = {coef[2]:.2f} + {coef[1]:.4f} p + {coef[0]:.2e} p^2 nm"
          f"  (residuals {np.round(resid, 2).tolist()} nm, dispersion {coef[1]:.2f} nm/pixel)")

    blank = d["blank"]
    blue = {float(k.split("_")[1]): absorbance(d[k], blank) for k in d if k.startswith("blue_")}
    yel = {float(k.split("_")[1]): absorbance(d[k], blank) for k in d if k.startswith("yellow_")}
    ref_b = blue[0.5] / 0.5
    ref_y = yel[0.5] / 0.5
    i_b = np.nanargmax(ref_b)
    i_y = np.nanargmax(np.where(lam < 520, ref_y, np.nan))
    print(f"Blue dye maximum at {lam[i_b]:.0f} nm; yellow dye maximum at {lam[i_y]:.0f} nm")

    f = np.array(sorted(blue))
    A_max = np.array([np.nanmean(blue[x][i_b - 2:i_b + 3]) for x in f])
    lin = f <= 0.5
    m, b, s_r, _ = line_fit(f[lin], A_max[lin])
    print(f"Beer-Lambert (fractions <= 0.5): A = {b:.4f} + {m:.4f} f, s_r = {s_r:.4f}")
    for x, a in zip(f, A_max):
        print(f"   f = {x:.1f}: A = {a:.3f}, line predicts {b + m * x:.3f}, deviation {100 * (a - b - m * x) / (b + m * x):+.1f} %")

    green = absorbance(d["green_unknown"], blank)
    ok = (lam > 400) & (lam < 680) & np.isfinite(green) & np.isfinite(ref_b) & np.isfinite(ref_y)
    X = np.column_stack([ref_b[ok], ref_y[ok]])
    (fb, fy), *_ = np.linalg.lstsq(X, green[ok], rcond=None)
    print(f"Full-spectrum least squares ({ok.sum()} pixels): blue {fb:.3f}, yellow {fy:.3f} of stock")
    M = np.array([[ref_b[i_b], ref_y[i_b]], [ref_b[i_y], ref_y[i_y]]])
    fb2, fy2 = np.linalg.solve(M, [green[i_b], green[i_y]])
    print(f"Two wavelengths only:                  blue {fb2:.3f}, yellow {fy2:.3f} of stock")

    fig, ax = plt.subplots(1, 3, figsize=(14, 4))
    ax[0].plot(lam, d["cfl"], lw=1)
    for L in HG_EU_LINES:
        ax[0].axvline(L, color="grey", ls=":", lw=0.8)
    ax[0].set(xlabel="wavelength (nm)", ylabel="intensity", title="Fluorescent lamp after calibration")
    for x in f:
        ax[1].plot(lam, blue[x], lw=1, label=f"blue {x}")
    ax[1].plot(lam, green, "k", lw=1.5, label="green unknown")
    ax[1].set(xlabel="wavelength (nm)", ylabel="pseudo-absorbance", title="Absorbance spectra", ylim=(-0.05, 1.4))
    ax[1].legend(fontsize=7)
    ax[2].plot(f, A_max, "o")
    ff = np.linspace(0, 1, 20)
    ax[2].plot(ff, b + m * ff, "-")
    ax[2].set(xlabel="fraction of blue stock", ylabel=f"A at {lam[i_b]:.0f} nm", title="Beer-Lambert check")
    save(fig, "lesson01_phone_spectrometer.png")


if __name__ == "__main__":
    main()
