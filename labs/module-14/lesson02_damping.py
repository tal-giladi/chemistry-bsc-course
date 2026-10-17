"""Lesson 14.2 hands-on: damping rate, Q factor and anharmonicity from a phyphox ringdown.

For each recording (time, then acceleration columns, as phyphox exports them):
1. Peak method: find the positive peaks, fit ln(peak height) against time; the slope is -gamma.
2. Full fit: a(t) = A exp(-gamma t) cos(omega_d t + phi) + c with scipy curve_fit.
3. Q = omega_0 / (2 gamma) with omega_0 = sqrt(omega_d^2 + gamma^2); log decrement delta = gamma T_d.
4. Anharmonicity: fit the frequency in short windows and see whether it drifts as the amplitude falls.

Run:   py lesson02_damping.py                 (the three example recordings)
       py lesson02_damping.py my_ringdown.csv 3  (your file; 3 = column of the spring axis)
Plots are saved to runs/ next to this file.
Fill in the functions marked TODO. Reference solution: lesson02_damping_solution.py
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.signal import find_peaks

from phyphox_csv import time_and_column

HERE = Path(__file__).resolve().parent


def damped(t, A, gamma, omega_d, phi, c):
    # TODO: return A exp(-gamma t) cos(omega_d t + phi) + c   (use np.exp, np.cos)
    return None


def rough_frequency(t, a):
    """Angular frequency of the strongest peak of the spectrum (a first guess for the fit)."""
    dt = np.median(np.diff(t))
    spec = np.abs(np.fft.rfft(a - a.mean()))
    f = np.fft.rfftfreq(a.size, dt)
    return 2 * np.pi * f[1:][np.argmax(spec[1:])]


def gamma_from_peaks(t, a, omega):
    """Damping rate from the decay of the peak heights. Return gamma, peak times, peak heights."""
    dt = np.median(np.diff(t))
    period_samples = int(2 * np.pi / omega / dt)
    idx, _ = find_peaks(a - a.mean(), distance=int(0.7 * period_samples))
    tp, hp = t[idx], a[idx] - a.mean()
    good = hp > 0.3 * hp.max()        # small peaks are biased upwards by sensor noise
    slope, _ = np.polyfit(tp[good], np.log(hp[good]), 1)
    return -slope, tp, hp


def fit_ringdown(t, a, omega_guess, gamma_guess):
    """Least-squares fit of the damped cosine. Return parameters and standard uncertainties."""
    A0 = np.max(np.abs(a[: int(a.size / 20) + 5] - a.mean()))
    p0 = [A0, gamma_guess, omega_guess, 0.0, a.mean()]
    best = None
    for phi in np.linspace(-np.pi, np.pi, 8, endpoint=False):   # try a few phases, keep the best
        p0[3] = phi
        try:
            p, cov = curve_fit(damped, t, a, p0=p0, maxfev=20000)
        except RuntimeError:
            continue
        rss = np.sum((a - damped(t, *p)) ** 2)
        if best is None or rss < best[2]:
            best = (p, cov, rss)
    p, cov, _ = best
    if p[0] < 0:                       # same curve with positive amplitude
        p[0], p[3] = -p[0], p[3] + np.pi
    return p, np.sqrt(np.diag(cov))


def q_factor(gamma, omega_d):
    # TODO: omega0 = sqrt(omega_d^2 + gamma^2); return omega0 / (2 gamma), omega0
    return None


def windowed_frequency(t, a, omega, gamma, window=6.0):
    """Fit frequency and amplitude in consecutive windows. Return arrays (amplitude, frequency Hz)."""
    amps, freqs = [], []
    start = t[0]
    while start + window <= t[-1]:
        sel = (t >= start) & (t < start + window)
        tt, aa = t[sel] - start, a[sel]
        A0 = np.max(np.abs(aa - aa.mean()))
        if A0 < 0.15:                  # too small to fit reliably above the sensor noise
            break
        try:
            p, _ = curve_fit(damped, tt, aa, p0=[A0, gamma, omega, 0.0, aa.mean()], maxfev=20000)
            for phi in (np.pi / 2, np.pi, -np.pi / 2):
                q, _ = curve_fit(damped, tt, aa, p0=[A0, gamma, omega, phi, aa.mean()], maxfev=20000)
                if np.sum((aa - damped(tt, *q)) ** 2) < np.sum((aa - damped(tt, *p)) ** 2):
                    p = q
        except RuntimeError:
            break
        amps.append(abs(p[0]) * np.exp(-p[1] * window / 2))
        freqs.append(p[2] / (2 * np.pi))
        start += window
    return np.array(amps), np.array(freqs)


def analyse(path, column):
    t, a, name = time_and_column(path, column)
    omega = rough_frequency(t, a)
    g_peaks, tp, hp = gamma_from_peaks(t, a, omega)
    p, u = fit_ringdown(t, a, omega, g_peaks)
    A, gamma, omega_d, phi, c = p
    Q, omega0 = q_factor(gamma, omega_d)
    uQ = Q * u[1] / gamma
    Td = 2 * np.pi / omega_d
    print(f"\n{path.name}  ({name})")
    print(f"  f_d = {omega_d / 2 / np.pi:.4f} Hz, period {Td:.4f} s")
    print(f"  gamma from peaks = {g_peaks:.4f} 1/s; from full fit = {gamma:.4f} +/- {u[1]:.5f} 1/s")
    print(f"  Q = omega0/(2 gamma) = {Q:.1f} +/- {uQ:.2f};  log decrement delta = {gamma * Td:.4f}, "
          f"pi/delta = {np.pi / (gamma * Td):.1f}")
    print(f"  energy decay time 1/(2 gamma) = {1 / (2 * gamma):.1f} s; "
          f"the amplitude falls by e in {1 / gamma / Td:.0f} cycles")
    amps, freqs = windowed_frequency(t, a, omega_d, gamma)
    if len(amps) >= 3:
        slope = np.polyfit(amps, freqs, 1)[0]
        print(f"  windowed: amplitude {amps[0]:.2f} -> {amps[-1]:.2f} m/s^2, "
              f"frequency {freqs[0]:.4f} -> {freqs[-1]:.4f} Hz "
              f"(change {100 * (freqs[-1] - freqs[0]) / freqs[0]:+.2f} %)")
        verdict = ("frequency rises as amplitude falls: the restoring force softens at large stretch"
                   if slope < 0 and abs(freqs[-1] - freqs[0]) / freqs[0] > 0.003 else
                   "frequency falls as amplitude falls: the restoring force stiffens at large stretch"
                   if slope > 0 and abs(freqs[-1] - freqs[0]) / freqs[0] > 0.003 else
                   "no frequency drift above the noise: harmonic within this precision")
        print(f"  -> {verdict}")

    (HERE / "runs").mkdir(exist_ok=True)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(8, 5.5))
    a1.plot(t, a, lw=0.5, label="data")
    a1.plot(t, damped(t, *p), lw=0.8, label=f"fit, Q = {Q:.0f}")
    a1.set_xlabel("time (s)")
    a1.set_ylabel("acceleration (m/s$^2$)")
    a1.legend(loc="upper right")
    a2.semilogy(tp, np.clip(hp, 1e-3, None), "o", ms=3)
    a2.semilogy(t, A * np.exp(-gamma * t), "-")
    a2.set_xlabel("time (s)")
    a2.set_ylabel("peak height (m/s$^2$)")
    fig.tight_layout()
    out = HERE / "runs" / f"lesson02_{path.stem}.png"
    fig.savefig(out, dpi=120)
    plt.close(fig)
    print(f"  plot saved to runs/{out.name}")
    return Q


def main():
    if len(sys.argv) > 1:
        column = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        analyse(Path(sys.argv[1]), column)
    else:
        for name in ("ringdown_spring.csv", "ringdown_card.csv", "ringdown_band.csv"):
            analyse(HERE / name, 3)


if __name__ == "__main__":
    try:
        main()
    except TypeError as exc:
        print(f"Fill in the functions marked TODO first ({exc}).")
