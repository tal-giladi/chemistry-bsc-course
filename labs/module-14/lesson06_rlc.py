"""Lesson 14.6 reference solution (module practical): resonance curve and Q factor of a series RLC.

You drive a series R-L-C circuit with a sine from a battery-powered phone (phyphox Tone Generator)
and read, at each frequency, the voltage across the whole circuit (Vin) and across the resistor
(VR) with a multimeter on AC volts. The ratio H = VR/Vin cancels changes in the source level and
the meter's own frequency response.

Model:  H(f) = A / sqrt(1 + Q^2 (f/f0 - f0/f)^2),   A = R / R_total
From the fit:  R_total = R / A,  L = Q R_total / (2 pi f0),  C = 1 / (2 pi f0 Q R_total).

Run:   py lesson06_rlc.py                 (example data)
       py lesson06_rlc.py my_rlc.csv      (header f_Hz,Vin_mV,VR_mV)
Set R_OHM, L_NOM, C_NOM and R_COIL_DC below to your parts and meter readings.
The plot is saved to runs/lesson06_rlc.png next to this file.
Fill in the functions marked TODO. Reference solution: lesson06_rlc_solution.py
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

HERE = Path(__file__).resolve().parent
R_OHM = 10.1        # resistor, measured with the ohmmeter (circuit unpowered)
R_COIL_DC = 28.0    # inductor's DC resistance, measured with the ohmmeter
L_NOM = 10.0e-3     # H, printed value
C_NOM = 1.0e-6      # F, printed value
U_READ = 0.005      # relative standard uncertainty of one meter reading (0.5 %)


def response(f, f0, Q, A):
    # TODO: return A / sqrt(1 + Q^2 (f/f0 - f0/f)^2)
    return None


def predicted(L, C, R_total):
    """f0 and Q expected from part values."""
    return 1 / (2 * np.pi * np.sqrt(L * C)), np.sqrt(L / C) / R_total


def fit_resonance(f, H, uH):
    i = np.argmax(H)
    p0 = [f[i], 2.0, H[i]]
    p, cov = curve_fit(response, f, H, p0=p0, sigma=uH, absolute_sigma=True)
    return p, np.sqrt(np.diag(cov))


def half_power_width(f0, Q):
    """Frequencies where H falls to 1/sqrt2 of its peak (the half-power points)."""
    x = 1 / (2 * Q)
    f1 = f0 * (np.sqrt(1 + x ** 2) - x)
    f2 = f0 * (np.sqrt(1 + x ** 2) + x)
    return f1, f2


def derived(f0, Q, A, R):
    # TODO: R_total = R / A;  L = Q R_total / (2 pi f0);  C = 1 / (2 pi f0 Q R_total);  return R_total, L, C
    return None


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "rlc_example.csv"
    f, vin, vr = np.loadtxt(path, delimiter=",", skiprows=1, unpack=True)
    H = vr / vin
    uH = H * np.sqrt(2) * U_READ
    uH = np.hypot(uH, 0.1 / vin)         # plus one count (0.1 mV) on the small VR readings

    f0_p, Q_p = predicted(L_NOM, C_NOM, R_OHM + R_COIL_DC)
    print(f"Prediction from printed L, C and DC resistances: f0 = {f0_p:.0f} Hz, Q = {Q_p:.2f}")

    (f0, Q, A), (uf0, uQ, uA) = fit_resonance(f, H, uH)
    chi2 = np.sum(((H - response(f, f0, Q, A)) / uH) ** 2)
    dof = f.size - 3
    print(f"Fit: f0 = {f0:.1f} +/- {uf0:.1f} Hz, Q = {Q:.3f} +/- {uQ:.3f}, peak H = {A:.4f} +/- {uA:.4f}")
    print(f"     chi^2 = {chi2:.1f} for {dof} degrees of freedom")
    f1, f2 = half_power_width(f0, Q)
    print(f"Half-power points {f1:.0f} and {f2:.0f} Hz, bandwidth {f2 - f1:.0f} Hz = f0/Q")
    R_total, L, C = derived(f0, Q, A, R_OHM)
    print(f"Derived: R_total = {R_total:.1f} ohm (R + coil DC = {R_OHM + R_COIL_DC:.1f} ohm), "
          f"L = {L * 1e3:.2f} mH, C = {C * 1e6:.3f} uF")
    extra = R_total - R_OHM - R_COIL_DC
    print(f"The coil loses more at {f0:.0f} Hz than its DC resistance says: about {extra:.0f} ohm extra.")
    print(f"Check: 1/(2 pi sqrt(LC)) with derived L, C = {1 / (2 * np.pi * np.sqrt(L * C)):.1f} Hz")
    print(f"Ringdown: after a sudden stop the current would fall by e in Q/pi = {Q / np.pi:.1f} cycles")

    (HERE / "runs").mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(6.5, 4))
    ff = np.geomspace(f.min(), f.max(), 400)
    ax.errorbar(f, H, yerr=uH, fmt="o", ms=4, capsize=2, label="data")
    ax.plot(ff, response(ff, f0, Q, A), "-", label=f"fit: f0 = {f0:.0f} Hz, Q = {Q:.2f}")
    ax.axhline(A / np.sqrt(2), color="0.7", lw=0.8)
    ax.axvspan(f1, f2, color="0.92")
    ax.set_xscale("log")
    ax.set_xlabel("frequency (Hz)")
    ax.set_ylabel("$V_R / V_{in}$")
    ax.legend()
    fig.tight_layout()
    fig.savefig(HERE / "runs" / "lesson06_rlc.png", dpi=120)
    print("Plot saved to runs/lesson06_rlc.png")


if __name__ == "__main__":
    try:
        main()
    except TypeError as exc:
        print(f"Fill in the functions marked TODO first ({exc}).")
