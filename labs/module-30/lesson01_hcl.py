"""Lesson 30.1 (exercise: fill in the three TODO functions): the HCl rotation-vibration spectrum at high resolution.

Run from this folder:
    py lesson01_hcl.py                    (example spectrum)
    py lesson01_hcl.py my_spectrum.csv    (your export: columns wavenumber_cm1,absorbance)
The example file hcl_ftir_example.csv is GENERATED from NIST WebBook constants (see make_data.py), with
both chlorine isotopes, the fundamental (near 2886 cm^-1) and the first overtone (near 5668 cm^-1).
Steps: find peaks, sort them into H35Cl and H37Cl, number them (m), fit each band, get the vibrational
constants from fundamental + overtone, compare the Morse dissociation energy with the real one, check
the isotope ratios, and read the gas temperature from the line intensities. Writes runs/lesson01_hcl.png.
"""
import math
import sys
from pathlib import Path

import numpy as np
from scipy.signal import find_peaks

from pc30 import (HERE, HC_K, HCL35, D0_HCL_CM, read_csv, column, linfit, reduced_mass,
                  bond_length_from_B, todo, save_plot, pyplot)

RHO = math.sqrt(reduced_mass("H", "35Cl") / reduced_mass("H", "37Cl"))


# ---------------- given: peak picking and assignment ----------------
def pick_peaks(x, y, prominence=0.015):
    """Peak positions refined with a three-point parabola, and peak heights above the local baseline."""
    idx, props = find_peaks(y, prominence=prominence)
    pos, hgt = [], []
    for i in idx:
        y0, y1, y2 = y[i - 1], y[i], y[i + 1]
        d = 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2)
        pos.append(x[i] + d * (x[1] - x[0]))
        hgt.append(y1 - 0.25 * (y0 - y2) * d)
    base = np.median(y)
    return np.array(pos), np.array(hgt) - base


def split_isotopes(pos, hgt):
    """A weaker partner about (1 - rho) * nu below a line is the same line of H37Cl (24 % abundance)."""
    is35 = np.zeros(len(pos), bool)
    is37 = np.zeros(len(pos), bool)
    for i, (p, h) in enumerate(zip(pos, hgt)):
        shift = (1 - RHO) * p
        j = np.flatnonzero(np.abs(pos - (p - shift)) < 0.35 * shift)
        if len(j) and hgt[j[0]] < 0.6 * h:
            is35[i], is37[j[0]] = True, True
    return pos[is35], hgt[is35], pos[is37], hgt[is37]


def number_lines(pos):
    """Running number m: the widest gap is the band centre (no Q branch); R lines m = 1, 2, ... above it,
    P lines m = -1, -2, ... below it."""
    pos = np.sort(pos)
    k = int(np.argmax(np.diff(pos)))
    m = np.concatenate([-np.arange(k + 1, 0, -1), np.arange(1, len(pos) - k)])
    return m, pos


# ---------------- the analysis ----------------
def fit_band(m, nu):
    """Fit nu(m) = c0 + c1 m + c2 m^2 + c3 m^3 and return (nu0, B_lower, B_upper, D).
    With centrifugal distortion, c1 = B' + B'', c2 = B' - B'' (D' - D'' is negligible), c3 = -2 (D' + D'').
    TODO: np.polyfit(m, nu, 3) returns c3, c2, c1, c0; turn them into the four constants."""
    return None  # TODO


def vib_constants(nu01, nu02):
    """omega_e and omega_e x_e from the fundamental (we - 2 wexe) and the first overtone (2 we - 6 wexe).
    TODO: solve the two equations; return (we, wexe)."""
    return None  # TODO


def temperature_from_lines(m, nu, height, B0, D):
    """Boltzmann plot: height / (|m| nu) is proportional to exp(-hc E_J / kT), E_J = lower-level rotational
    energy in cm^-1. Returns T and its standard uncertainty from the slope -hc/k / T.
    Lower J: J = m - 1 for R lines (m > 0) and J = -m for P lines. Use linfit(E, ln(...)), which returns
    (a, b, sa, sb, cov, s); HC_K = hc/k in cm K.
    TODO: return (T, sigma_T)."""
    return None  # TODO


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "hcl_ftir_example.csv"
    rows = read_csv(path)
    x, y = column(rows, "wavenumber_cm1"), column(rows, "absorbance")
    results = {}
    for band, (lo, hi) in (("1-0", (2600, 3200)), ("2-0", (5400, 5900))):
        sel = (x > lo) & (x < hi)
        pos, hgt = pick_peaks(x[sel], y[sel])
        p35, h35, p37, h37 = split_isotopes(pos, hgt)
        for iso, p, h in (("H35Cl", p35, h35), ("H37Cl", p37, h37)):
            m, nu = number_lines(p)
            hh = h[np.argsort(p)]
            fit = fit_band(m, nu)
            if todo(fit):
                return
            results[(band, iso)] = (m, nu, hh, fit)
    print("Band     isotope  lines   nu0 (cm-1)    B_lower     B_upper     D (cm-1)   rms resid")
    for (band, iso), (m, nu, hh, (nu0, Bl, Bu, D)) in results.items():
        resid = nu - (nu0 + (Bu + Bl) * m + (Bu - Bl) * m**2 - 4 * D * m**3)
        print(f"{band:7s}  {iso:6s}  {len(m):4d}   {nu0:10.3f}   {Bl:9.4f}   {Bu:9.4f}   {D:9.2e}   "
              f"{np.sqrt(np.mean(resid**2)):.4f}")

    m, nu, hh, (nu01, B0, B1, D) = results[("1-0", "H35Cl")]
    nu02 = results[("2-0", "H35Cl")][3][0]
    we_wexe = vib_constants(nu01, nu02)
    T = temperature_from_lines(m, nu, hh, B0, D)
    if todo(we_wexe, T):
        return
    we, wexe = we_wexe
    ae = B0 - B1
    Be = B0 + ae / 2
    mu = reduced_mass("H", "35Cl")
    print(f"\nH35Cl: B0 = {B0:.4f}, B1 = {B1:.4f}, alpha_e = {ae:.4f}, Be = {Be:.4f} cm-1 "
          f"(NIST Be {HCL35['Be']:.4f}, alpha_e {HCL35['ae']:.4f})")
    print(f"  r_e = {bond_length_from_B(Be, mu):.4f} A (NIST {HCL35['re']:.4f}); "
          f"r_0 = {bond_length_from_B(B0, mu):.4f} A")
    print(f"  omega_e = {we:.1f}, omega_e x_e = {wexe:.2f} cm-1 (NIST {HCL35['we']:.1f}, {HCL35['wexe']:.2f})")
    De = we**2 / (4 * wexe)
    G0 = we / 2 - wexe / 4
    print(f"  Morse D_e = {De:.0f} cm-1, D_0 = D_e - G(0) = {De - G0:.0f} cm-1 = {(De - G0) / 8065.544:.2f} eV; "
          f"real D_0 about {D0_HCL_CM:.0f} cm-1 ({D0_HCL_CM / 8065.544:.2f} eV)")
    nu0_37, B0_37 = results[("1-0", "H37Cl")][3][:2]
    print(f"  isotopes: nu0(37)/nu0(35) = {nu0_37 / nu01:.6f}, B0(37)/B0(35) = {B0_37 / B0:.6f}; "
          f"rho = {RHO:.6f}, rho^2 = {RHO**2:.6f}")
    print(f"  temperature from the R and P line heights: {T[0]:.0f} +/- {T[1]:.0f} K")

    plt = pyplot()
    if plt is None:
        return
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(9, 6))
    sel = (x > 2640) & (x < 3090)
    a1.plot(x[sel], y[sel], lw=0.6)
    for iso, mk in (("H35Cl", "v"), ("H37Cl", "^")):
        mm, nn, hh2, _ = results[("1-0", iso)]
        a1.plot(nn, hh2 + np.median(y), mk, ms=4, label=iso)
    a1.set_xlabel("wavenumber (cm$^{-1}$)")
    a1.set_ylabel("absorbance")
    a1.legend()
    for (band, iso), (mm, nn, _, (nu0, Bl, Bu, DD)) in results.items():
        a2.plot(mm, nn - nu0 - (Bu + Bl) * mm, "o", ms=3, label=f"{band} {iso}")
    a2.set_xlabel("m")
    a2.set_ylabel(r"$\nu - \nu_0 - (B'+B'')m$ (cm$^{-1}$)")
    a2.legend(fontsize=8)
    save_plot(fig, "lesson01_hcl.png")


if __name__ == "__main__":
    main()
