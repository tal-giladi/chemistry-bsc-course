"""Lesson 20.3 - assign and fit the NIST infrared band of HCl, and predict a rotational Raman spectrum
(reference solution).

Fill in the functions marked TODO, then run:  py lesson03_hcl_band.py
Reference solution: lesson03_hcl_band_solution.py
Writes runs/lesson03_hcl_band.png.
"""
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from spec20 import B_v, C_CM, DIATOMIC, G, U, bond_length_from_B, read_csv, reduced_mass, term


def load_peaks():
    rows = sorted(read_csv("hcl_band_peaks.csv"), key=lambda r: float(r["wavenumber_cm1"]))
    return np.array([float(r["wavenumber_cm1"]) for r in rows]), np.array([float(r["transmittance"]) for r in rows])


def assign_branches(peaks):
    """Give each peak its running number m: R(J) has m = J + 1, P(J) has m = -J.
    The band centre is the biggest gap between neighbouring peaks (there is no Q branch)."""
    peaks = np.sort(peaks)
    gap = int(np.argmax(np.diff(peaks)))          # last P line is peaks[gap], first R line peaks[gap+1]
    m = np.empty(len(peaks), int)
    m[: gap + 1] = -np.arange(gap + 1, 0, -1)     # ..., P(3), P(2), P(1) -> m = ..., -3, -2, -1
    m[gap + 1:] = np.arange(1, len(peaks) - gap)  # R(0), R(1), ... -> m = 1, 2, ...
    return peaks, m


def fit_band(peaks, m):
    """Fit nu(m) = nu0 + (B1 + B0) m + (B1 - B0) m^2. Returns nu0, B0, B1."""
    # TODO: c2, c1, c0 = np.polyfit(m, peaks, 2)   (quadratic in m)
    # TODO: c0 = nu0, c1 = B1 + B0, c2 = B1 - B0: solve for B0 and B1 and return nu0, B0, B1
    return None


def combination_differences(peaks, m):
    """B0 from R(J-1) - P(J+1) = 4 B0 (J + 1/2) and B1 from R(J) - P(J) = 4 B1 (J + 1/2).
    Returns the mean B0 and mean B1 over all J where both lines exist."""
    # TODO: R = {J: position} from peaks with m > 0 (J = m - 1); P = {J: position} from m < 0 (J = -m)
    # TODO: B0 values: (R[J-1] - P[J+1]) / (4 (J + 1/2)) for every J where both exist
    # TODO: B1 values: (R[J] - P[J]) / (4 (J + 1/2)) for every J where both exist
    # TODO: return the mean of each list
    return None


def force_constant(nu_cm, mu_u):
    """Harmonic force constant k = mu (2 pi c nu)^2 in N/m."""
    return mu_u * U * (2 * math.pi * C_CM * nu_cm) ** 2


def rotational_raman(B, n_lines=5):
    """Stokes rotational Raman shifts (cm^-1) for Delta J = +2: F(J+2) - F(J) = 4B(J + 3/2)."""
    # TODO: return [4 * B * (J + 1.5) for J in range(n_lines)]
    return None


def predicted_lines(mol, jmax=11):
    """P and R lines of the fundamental from the NIST constants."""
    lines = []
    for J in range(jmax):
        lines.append(term(mol, 1, J + 1) - term(mol, 0, J))
        if J > 0:
            lines.append(term(mol, 1, J - 1) - term(mol, 0, J))
    return np.array(sorted(lines))


def main():
    stubs = (fit_band(np.array([1.0, 2, 3]), np.array([1, 2, 3])), rotational_raman(1.0),
             combination_differences(np.array([1.0, 2]), np.array([-1, 1])))
    if any(x is None for x in stubs):
        print("TODO: write fit_band(), combination_differences() and rotational_raman() first.")
        return
    peaks, T = load_peaks()
    peaks, m = assign_branches(peaks)
    nu0, B0, B1 = fit_band(peaks, m)
    mu = reduced_mass("H", "35Cl")
    print(f"{len(peaks)} peaks: P lines m = {m[m < 0].min()}..-1, R lines m = 1..{m.max()}")
    print(f"Fit to NIST spectrum : nu0 = {nu0:.1f}, B0 = {B0:.3f}, B1 = {B1:.3f} cm-1")
    print(f"NIST constants       : nu0 = {G('HCl', 1) - G('HCl', 0):.1f}, B0 = {B_v('HCl', 0):.3f}, "
          f"B1 = {B_v('HCl', 1):.3f} cm-1")
    cb0, cb1 = combination_differences(peaks, m)
    print(f"Combination diffs    : B0 = {cb0:.3f}, B1 = {cb1:.3f} cm-1")
    alpha = B0 - B1
    Be = B0 + alpha / 2
    print(f"alpha_e = {alpha:.3f} cm-1, Be = {Be:.3f} cm-1, re = {bond_length_from_B(Be, mu):.4f} A "
          f"(NIST {DIATOMIC['HCl']['re']} A), r0 = {bond_length_from_B(B0, mu):.4f} A")
    print(f"force constant from nu0: k = {force_constant(nu0, mu):.0f} N/m "
          f"(from omega_e: {force_constant(DIATOMIC['HCl']['we'], mu):.0f} N/m)")
    resid = peaks - np.polyval([B1 - B0, B1 + B0, nu0], m)
    print(f"rms residual of the fit: {np.sqrt(np.mean(resid**2)):.2f} cm-1 (spectrum resolution 4 cm-1)")
    mu37 = reduced_mass("H", "37Cl")
    shift = (G("HCl", 1) - G("HCl", 0)) * (1 - math.sqrt(mu / mu37))
    print(f"H37Cl band centre is {shift:.2f} cm-1 lower (not resolved at 4 cm-1)")
    nB0 = B_v("N2", 0)
    print("N2 rotational Raman Stokes shifts (cm-1):", ", ".join(f"{x:.2f}" for x in rotational_raman(nB0)))
    print(f"N2 vibrational Raman Q branch near {G('N2', 1) - G('N2', 0):.1f} cm-1")

    Path("runs").mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.vlines(peaks, T, 1.0, color="k", label="NIST spectrum peaks (Coblentz 8758)")
    pred = predicted_lines("HCl")
    ax.plot(pred, np.full(len(pred), 1.02), "v", color="tab:red", label="H35Cl from NIST constants")
    for p, t, mm in zip(peaks, T, m):
        ax.text(p, t - 0.04, f"{'R' if mm > 0 else 'P'}({mm - 1 if mm > 0 else -mm})",
                ha="center", fontsize=7)
    ax.set_xlabel("wavenumber / cm$^{-1}$"); ax.set_ylabel("transmittance"); ax.invert_xaxis(); ax.legend()
    fig.tight_layout(); fig.savefig("runs/lesson03_hcl_band.png", dpi=120)
    print("saved runs/lesson03_hcl_band.png")


if __name__ == "__main__":
    main()
