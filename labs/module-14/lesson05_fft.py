"""Lesson 14.5 hands-on: sampling, aliasing and the Fourier transform of real recordings.

1. Aliasing: what frequency you see when you sample too slowly.
2. A spectrum helper: resample phyphox data onto an even time grid, window it, FFT it.
3. Three coupled pendulums recorded by the phone on pendulum 1: the three mode frequencies are
   only 0.013 and 0.028 Hz apart. A 20 s record cannot separate them; a 120 s record can.
4. The spring ringdown of lesson 14.2: peak frequency, line width and Q from the spectrum, and
   why the record must be several decay times long for the width to mean anything.

Run:   py lesson05_fft.py                    (example data)
       py lesson05_fft.py my_recording.csv 1 (your file; 1 = column to analyse)
Plots are saved to runs/ next to this file.
Fill in the functions marked TODO. Reference solution: lesson05_fft_solution.py
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks

from phyphox_csv import time_and_column

HERE = Path(__file__).resolve().parent


def alias_frequency(f, fs):
    """The frequency (0 to fs/2) that a sine of frequency f appears at when sampled at fs."""
    # TODO: r = f mod fs; return the smaller of r and fs - r
    return None


def spectrum(t, a, pad=4, window=True):
    """Amplitude spectrum of an unevenly sampled record.
    Resample on an even grid (np.interp), remove the mean, apply a Hann window, zero-pad by `pad`
    to draw the peaks smoothly. Return frequencies (Hz), amplitudes, sample rate, record length."""
    fs = (t.size - 1) / (t[-1] - t[0])
    tt = np.linspace(t[0], t[-1], t.size)
    y = np.interp(tt, t, a)
    y = y - y.mean()
    w = np.hanning(y.size) if window else np.ones(y.size)
    n = pad * y.size
    amp = np.abs(np.fft.rfft(y * w, n)) * 2 / w.sum()
    return np.fft.rfftfreq(n, 1 / fs), amp, fs, tt[-1] - tt[0]


def peak_list(f, amp, fmin, fmax, rel=0.1):
    sel = (f >= fmin) & (f <= fmax)
    idx, _ = find_peaks(amp[sel], height=rel * amp[sel].max())
    return f[sel][idx], amp[sel][idx]


def fwhm(f, power, i_peak):
    """Full width at half maximum of the peak at index i_peak, by linear interpolation."""
    # TODO: walk left and right from i_peak until power drops below half the peak;
    #       interpolate the two crossing frequencies (np.interp) and return their difference
    return None


def main():
    print("1. Aliasing")
    for f, fs in ((3.0, 100.0), (3.0, 4.0), (49.0, 50.0), (1.40, 2.0)):
        print(f"   a {f} Hz signal sampled at {fs} Hz appears at {alias_frequency(f, fs):.2f} Hz "
              f"(Nyquist limit {fs / 2} Hz)")

    if len(sys.argv) > 1:
        col = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        t, a, name = time_and_column(Path(sys.argv[1]), col)
        f, amp, fs, T = spectrum(t, a)
        i = np.argmax(amp[1:]) + 1
        print(f"\n{sys.argv[1]} ({name}): fs = {fs:.1f} Hz, record {T:.1f} s, resolution {1 / T:.4f} Hz")
        print(f"   strongest peak at {f[i]:.4f} Hz")
        return

    print("\n2. Coupled pendulums, phone on pendulum 1 (pendulum_phone_example.csv)")
    t, a, _ = time_and_column(HERE / "pendulum_phone_example.csv", 1)
    (HERE / "runs").mkdir(exist_ok=True)
    fig, axs = plt.subplots(2, 1, figsize=(8, 5.5))
    for T_rec, ax in ((20.0, axs[0]), (120.0, axs[0])):
        sel = t < T_rec
        f, amp, fs, T = spectrum(t[sel], a[sel], pad=16)
        pk, _ = peak_list(f, amp, 0.6, 0.85)
        print(f"   record {T:5.1f} s: resolution 1/T = {1 / T:.4f} Hz -> peaks at {np.round(pk, 4)} Hz")
        ax.plot(f, amp, label=f"{T_rec:.0f} s record")
    axs[0].set_xlim(0.6, 0.85)
    axs[0].set_xlabel("frequency (Hz)")
    axs[0].set_ylabel("amplitude")
    axs[0].legend()
    print(f"   sample rate {fs:.0f} Hz: Nyquist {fs / 2:.0f} Hz, far above 0.75 Hz, so no aliasing")

    print("\n3. Spring ringdown from lesson 14.2 (ringdown_spring.csv)")
    t, a, _ = time_and_column(HERE / "ringdown_spring.csv", 3)
    for T_rec in (10.0, 30.0, 60.0):
        sel = t < T_rec
        f, amp, fs, T = spectrum(t[sel], a[sel], pad=32, window=False)
        p = amp ** 2
        i = np.argmax(p[1:]) + 1
        width = fwhm(f, p, i)
        print(f"   record {T:4.0f} s: peak {f[i]:.4f} Hz, FWHM {width:.4f} Hz, Q = f/FWHM = {f[i] / width:.0f}"
              f"   (resolution 1/T = {1 / T:.4f} Hz)")
        if T_rec == 60.0:
            axs[1].plot(f, p / p.max(), label="60 s record, no window")
    gamma = 0.040
    print(f"   from the time-domain fit (lesson 14.2): gamma = {gamma} 1/s, line width gamma/pi = "
          f"{gamma / np.pi:.4f} Hz, Q = 110")
    print("   The width is trustworthy only when the record is several decay times (1/gamma = 25 s)")
    print("   long; shorter records give a width set by 1/T and a Q that is too low.")
    axs[1].set_xlim(1.30, 1.50)
    axs[1].set_xlabel("frequency (Hz)")
    axs[1].set_ylabel("power (normalised)")
    axs[1].legend()
    fig.tight_layout()
    fig.savefig(HERE / "runs" / "lesson05_fft.png", dpi=120)
    print("Plot saved to runs/lesson05_fft.png")


if __name__ == "__main__":
    try:
        main()
    except TypeError as exc:
        print(f"Fill in the functions marked TODO first ({exc}).")
