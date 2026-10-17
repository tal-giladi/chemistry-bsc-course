"""Lesson 32.3 (reference solution): index a REAL powder pattern of cadmium oxide and refine its lattice parameter.

Run from this folder:
    py lesson03_xrd_solution.py
    py lesson03_xrd_solution.py my_pattern.csv      (columns two_theta_deg,counts; Cu tube)
File: cdo_xrd.csv, real data from Dahiya, Dahiya and Sabarwal (2026), Zenodo, doi:10.5281/zenodo.18522088,
CC BY 4.0 (see get_zenodo_xrd.py). Reference: COD 9006671, CdO, Fm-3m, a = 4.6963 A (Zhang 1999).
Steps: peak list; flag Cu K-beta satellites of the strong peaks; index the remaining strong peaks with the
1/d^2 ratio method; least-squares fit of a and a zero shift; compare with COD; density.
Writes runs/lesson03_xrd.png.
"""
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares

from ec32 import (HERE, CU_KA1, CU_KB, bragg_two_theta, d_from_two_theta, find_xrd_peaks, read_xrd, todo,
                  save_plot, pyplot)

N_A = 6.02214076e23
A_COD = 4.6963          # COD 9006671
M_CDO = 112.414 + 15.999
_HKL = [(h, k, l) for h in range(13) for k in range(13) for l in range(13) if h + k + l > 0]
SC = sorted({h * h + k * k + l * l for h, k, l in _HKL})                       # any sum of three squares
BCC = sorted({h * h + k * k + l * l for h, k, l in _HKL if (h + k + l) % 2 == 0})
FCC = sorted({h * h + k * k + l * l for h, k, l in _HKL if h % 2 == k % 2 == l % 2})


def kbeta_partner(tt_alpha):
    """2 theta (deg) where the Cu K-beta line of a K-alpha peak at tt_alpha appears (same d, shorter wavelength)."""
    s = np.sin(np.radians(np.asarray(tt_alpha) / 2)) * CU_KB / CU_KA1
    return np.degrees(2 * np.arcsin(s))


def index_cubic(d):
    """Assign N = h^2 + k^2 + l^2 to each d spacing by the ratio method.
    r = (1/d^2) / (1/d_first^2) gives ratios; try multipliers m = 1..8 for the first line and keep the m for
    which m * r is closest to whole numbers. Return (N array of ints, m, rms distance from integers)."""
    r = (1 / np.asarray(d) ** 2) / (1 / d[0] ** 2)
    best = None
    for m in range(1, 9):
        x = m * r
        rms = float(np.sqrt(np.mean((x - np.round(x)) ** 2)))
        if best is None or rms < best[2] - 0.01:
            best = (np.round(x).astype(int), m, rms)
    return best


def fit_cubic(tt, N, lam=CU_KA1):
    """Least-squares fit of a (angstrom) and a zero shift z (deg): tt_obs = 2theta(a, N) + z.
    Return (a, z, sigma_a, rms residual in deg)."""
    def resid(p):
        return bragg_two_theta(p[0] / np.sqrt(N), lam) + p[1] - tt
    res = least_squares(resid, [float(np.median(d_from_two_theta(tt, lam) * np.sqrt(N))), 0.0])
    J = res.jac
    dof = max(1, len(tt) - 2)
    s2 = float(np.sum(res.fun ** 2) / dof)
    cov = np.linalg.inv(J.T @ J) * s2
    return float(res.x[0]), float(res.x[1]), float(np.sqrt(cov[0, 0])), float(np.sqrt(s2))


def lattice_type(N):
    """Name the cubic lattice whose allowed list contains every N (fcc and bcc are tested before sc)."""
    for name, allowed in (("face-centred (fcc)", FCC), ("body-centred (bcc)", BCC), ("primitive (sc)", SC)):
        if all(n in allowed for n in N):
            return name
    return "not cubic, or a wrong assignment"


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "cdo_xrd.csv"
    tt, y = read_xrd(path)
    pk, height, fwhm = find_xrd_peaks(tt, y)
    strong = height > 0.05 * height.max()
    print("Peak list (2theta, height above background, FWHM):")
    for p, h, w in zip(pk, height, fwhm):
        print(f"  {p:7.3f} deg  {h:6.0f}  {w:.3f} deg")
    satellites = []
    for p in pk[strong]:
        kb = kbeta_partner(p)
        hit = pk[(np.abs(pk - kb) < 0.12) & ~strong]
        if hit.size:
            satellites.append(hit[0])
            print(f"  K-beta of the {p:.2f} peak expected at {kb:.2f}: found at {hit[0]:.2f}")
    main_pk = pk[strong]
    d = d_from_two_theta(main_pk)
    res = index_cubic(d)
    fit = fit_cubic(main_pk, res[0]) if res is not None else None
    if todo(res, fit):
        return
    N, m, rms = res
    print(f"Ratio method: multiplier {m}, N = {[int(n) for n in N]}, rms distance from integers {rms:.3f}"
          f" -> {lattice_type(N)}")
    a, z, sa, srms = fit
    rho = 4 * M_CDO / (N_A * (a * 1e-8) ** 3)
    print(f"Fit: a = {a:.4f} +- {sa:.4f} A, zero shift {z:+.3f} deg, rms residual {srms:.3f} deg")
    print(f"COD 9006671: a = {A_COD} A; difference {(a - A_COD) / A_COD * 100:+.2f} %; "
          f"X-ray density {rho:.2f} g/cm3 (Z = 4)")
    a0 = np.median(d * np.sqrt(N))
    print(f"Without the zero shift (median of d sqrt(N)): a = {a0:.4f} A ({(a0 - A_COD) / A_COD * 100:+.2f} %)")
    known = set(np.round(main_pk, 2)) | set(np.round(satellites, 2))
    left = [p for p in pk if round(p, 2) not in known]
    print("Unassigned peaks (not CdO K-alpha, not K-beta):", ", ".join(f"{p:.2f}" for p in left) or "none")
    plt = pyplot()
    if plt:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(tt, y, lw=0.8)
        for n, p in zip(N, main_pk):
            ax.annotate(f"N={n}", (p, y[np.argmin(abs(tt - p))]), textcoords="offset points", xytext=(0, 4),
                        ha="center", fontsize=7)
        for s in satellites:
            ax.axvline(s, color="r", lw=0.6, ls=":")
        ax.set_xlabel("2θ / degrees (Cu Kα)")
        ax.set_ylabel("counts")
        ax.set_title("CdO powder pattern (real data, Zenodo 18522088, CC BY 4.0)")
        save_plot(fig, "lesson03_xrd.png")


if __name__ == "__main__":
    main()
