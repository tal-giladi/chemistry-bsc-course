"""Lesson 12.1 hands-on (reference solution): the Rydberg constant from the hydrogen Balmer lines.

Data: balmer_nist.csv, four H I lines in air from the NIST Handbook of Basic Atomic Spectroscopic Data.
Run:   py lesson01_balmer_solution.py
The figure is saved to runs/lesson01_balmer.png next to this file.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from qm_solver import H, C_LIGHT, E_CHARGE, read_csv

HERE = Path(__file__).resolve().parent
R_INF = 10973731.568157       # m^-1, CODATA 2022
MP_ME = 1836.152673426        # proton-electron mass ratio, CODATA 2022


def load_lines():
    rows = read_csv(HERE / "balmer_nist.csv")
    return ([r["name"] for r in rows], np.array([float(r["n_upper"]) for r in rows]),
            np.array([float(r["lambda_air_nm"]) for r in rows]))


def air_to_vacuum(lam_air_nm):
    """Edlen (1966) refractive index of standard air; sigma is the vacuum wavenumber in um^-1
    (the air value is close enough for this correction)."""
    sigma2 = (1000.0 / lam_air_nm) ** 2
    n = 1 + 1e-8 * (8342.13 + 2406030 / (130 - sigma2) + 15997 / (38.9 - sigma2))
    return lam_air_nm * n


def fit_rydberg(n_upper, lam_vac_nm):
    """Straight-line fit of 1/lambda (m^-1) against (1/4 - 1/n^2). Returns slope, intercept,
    and the standard error of the slope."""
    xdat = 0.25 - 1.0 / n_upper**2
    ydat = 1.0 / (lam_vac_nm * 1e-9)
    (slope, icpt), cov = np.polyfit(xdat, ydat, 1, cov=True)
    return slope, icpt, np.sqrt(cov[0, 0]), xdat, ydat


def main():
    names, n_up, lam_air = load_lines()
    lam_vac = air_to_vacuum(lam_air)
    print("line      n   lambda_air/nm  lambda_vac/nm")
    for nm, n, la, lv in zip(names, n_up, lam_air, lam_vac):
        print(f"{nm:8s} {int(n):2d}   {la:11.4f}   {lv:11.4f}")
    slope, icpt, s_slope, xdat, ydat = fit_rydberg(n_up, lam_vac)
    r_h_theory = R_INF / (1 + 1 / MP_ME)
    print(f"\nFitted R_H   = {slope:.1f} +/- {s_slope:.1f} m^-1 (intercept {icpt:.1f} m^-1)")
    print(f"R_inf mu/m_e = {r_h_theory:.1f} m^-1   (difference {(slope - r_h_theory) / r_h_theory * 1e6:+.1f} ppm)")
    ie_ev = H * C_LIGHT * slope / E_CHARGE
    print(f"Ionisation energy of H from the fit: hc R_H = {ie_ev:.4f} eV")
    lam_limit = 4 / slope * 1e9
    print(f"Balmer series limit (n -> infinity): {lam_limit:.2f} nm (vacuum)")
    # same fit without the air correction, to see why it matters
    s_air, *_ = fit_rydberg(n_up, lam_air)
    print(f"Without the air correction: R_H = {s_air:.1f} m^-1 ({(s_air - r_h_theory) / r_h_theory * 1e6:+.0f} ppm)")

    out = HERE / "runs"
    out.mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(xdat, ydat / 1e6, "o", label="NIST lines (vacuum)")
    xx = np.linspace(0, 0.25, 50)
    ax.plot(xx, (slope * xx + icpt) / 1e6, "-", label=f"fit, slope R_H = {slope:.4e} m$^{{-1}}$")
    ax.set_xlabel("1/4 - 1/n$^2$")
    ax.set_ylabel("1/$\\lambda$ (µm$^{-1}$)")
    ax.set_title("Balmer series of hydrogen")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out / "lesson01_balmer.png", dpi=120)
    print(f"Figure saved to {out / 'lesson01_balmer.png'}")


if __name__ == "__main__":
    main()
