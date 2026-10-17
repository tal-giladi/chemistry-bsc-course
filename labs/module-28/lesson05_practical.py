"""Lesson 28.5 - isotope effects, a radical clock and the module practical.

Fill in the functions marked TODO, then run:  py lesson05_practical.py
Reference solution: lesson05_practical_solution.py
Writes runs/lesson05_practical.png.
Part A: a primary kinetic isotope effect from zero-point energies (harmonic model, lesson 12.4).
Part B: a radical clock (cyclopropylcarbinyl ring opening, 1.2e8 s-1 at 37 C, Bowry, Lusztyk and
        Ingold, J. Am. Chem. Soc. 113, 5687 (1991)).
Part C: module practical - Hammett analysis of the coupling of 3-aminothiophene with eight
        para-substituted benzenediazonium ions (El Abed et al., ChemPhysChem 26, e202500553 (2025),
        Table 1, CC BY 4.0; data in diazonium_coupling.csv).
"""
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

from sr28 import H, K_B, line_fit, num, read_csv, runs_dir

C_CM = 2.99792458e10          # speed of light, cm/s (exact)
M_H, M_D, M_C = 1.00782503, 2.01410178, 12.0   # atomic masses, u
KA_AMINE = 10 ** -3.38       # acidity constant of protonated 3-aminothiophene (from the paper)


# ---------- Part A ----------
def deuterium_wavenumber(nu_h, m_heavy=M_C):
    """C-D stretch from the C-H stretch: same force constant, so nu scales as 1/sqrt(reduced mass)."""
    mu_h = m_heavy * M_H / (m_heavy + M_H)
    mu_d = m_heavy * M_D / (m_heavy + M_D)
    return nu_h * math.sqrt(mu_h / mu_d)


def kie_from_zpe(nu_h, T=298.15, m_heavy=M_C):
    """kH/kD if the stretch's zero-point energy is completely lost at the transition state."""
    # TODO: zero-point energy difference per molecule: 0.5 * H * C_CM * (nu_h - nu_d), nu_d from deuterium_wavenumber()
    # TODO: return exp(dZPE / (K_B * T))
    raise NotImplementedError("TODO: write kie_from_zpe() first (see the hints in the code).")


# ---------- Part B ----------
def trap_rate_constant(ratio_unrearranged, k_clock, trap_conc):
    """Unrearranged/rearranged product = k_trap [trap] / k_clock  ->  k_trap (M-1 s-1)."""
    # TODO: rearrange ratio = k_trap * [trap] / k_clock for k_trap
    raise NotImplementedError("TODO: write trap_rate_constant() first (see the hints in the code).")


# ---------- Part C ----------
def k1_from_k(k, pH, ka=KA_AMINE):
    """Only the free amine reacts: k = k1 * Ka/(Ka + [H3O+])  ->  k1 = k (1 + [H3O+]/Ka)."""
    # TODO: [H3O+] = 10 ** -pH; return k * (1 + [H3O+] / ka)
    raise NotImplementedError("TODO: write k1_from_k() first (see the hints in the code).")


def yukawa_tsuno(X, logk0, rho, r):
    """log k = log k0 + rho [sigma + r (sigma+ - sigma)]."""
    # TODO: s, s_plus = X; return logk0 + rho * (s + r * (s_plus - s))
    raise NotImplementedError("TODO: write yukawa_tsuno() first (see the hints in the code).")


def main():
    print("Part A - primary KIE from zero-point energy (C-H stretch):")
    for nu in (2900.0, 3000.0):
        print(f"  nu(C-H) {nu:.0f} cm-1 -> nu(C-D) {deuterium_wavenumber(nu):.0f} cm-1, "
              f"kH/kD = {kie_from_zpe(nu):.1f} at 298 K, {kie_from_zpe(nu, T=373.15):.1f} at 373 K")

    print("Part B - radical clock:")
    k_trap = trap_rate_constant(0.25, 1.2e8, 0.10)
    print(f"  unrearranged/rearranged = 0.25 with 0.10 M trap -> k_trap = {k_trap:.1e} M-1 s-1")

    rows = read_csv("diazonium_coupling.csv")
    X = [r["X"] for r in rows]
    sp = np.array([num(r["sigma_p"]) for r in rows])
    spp = np.array([num(r["sigma_p_plus"]) for r in rows])
    print("Part C - check k1 = k (1 + [H3O+]/Ka) against the table:")
    for r in rows:
        print(f"  {r['X']:5s} pH 2: {k1_from_k(num(r['k_pH2']), 2):9.3g} (table {num(r['k1_pH2']):.3g});  "
              f"pH 1: {k1_from_k(num(r['k_pH1']), 1):9.3g} (table {num(r['k1_pH1']):.3g})")

    s2 = np.concatenate([sp, sp])
    sp2 = np.concatenate([spp, spp])
    y = np.log10([num(r["k1_pH2"]) for r in rows] + [num(r["k1_pH1"]) for r in rows])
    fits = {"sigma_p": line_fit(s2, y), "sigma_p+": line_fit(sp2, y)}
    for name, f in fits.items():
        print(f"  log k1 vs {name:8s}: rho = {f['slope']:.2f} +/- {f['s_slope']:.2f}, "
              f"log k1(H) = {f['intercept']:.2f}, R2 = {f['r2']:.3f}, rms residual {np.sqrt(np.mean(f['resid'] ** 2)):.2f}")
    p, cov = curve_fit(yukawa_tsuno, (s2, sp2), y, p0=(2.7, 2.5, 1.0))
    err = np.sqrt(np.diag(cov))
    corr = cov[1, 2] / (err[1] * err[2])
    print(f"  Yukawa-Tsuno: rho = {p[1]:.2f} +/- {err[1]:.2f}, r = {p[2]:.2f} +/- {err[2]:.2f}, "
          f"correlation(rho, r) = {corr:+.2f}  (paper: rho 2.11, r 1.54)")

    print("  Isotope effects kH/kD (2-deuterio-3-aminothiophene):")
    for r in rows:
        for pH in ("pH2", "pH1"):
            kd = num(r[f"kD_{pH}"])
            if not math.isnan(kd):
                print(f"    {r['X']:5s} {pH}: {num(r[f'k_{pH}']) / kd:.2f}")

    fig, axes = plt.subplots(1, 3, figsize=(14, 4.2))
    for ax, (name, x) in zip(axes[:2], (("sigma_p", s2), ("sigma_p+", sp2))):
        f = fits[name]
        ax.plot(x[:8], y[:8], "o", label="pH 2")
        ax.plot(x[8:], y[8:], "s", mfc="none", label="pH 1")
        xx = np.linspace(x.min() - 0.05, x.max() + 0.05, 2)
        ax.plot(xx, f["intercept"] + f["slope"] * xx, "-", label=f"rho = {f['slope']:.2f}")
        for xi, yi, lab in zip(x[:8], y[:8], X):
            ax.annotate(lab, (xi, yi), xytext=(4, -10), textcoords="offset points", fontsize=8)
        ax.set(xlabel=name, ylabel="log10 k1 (M-1 s-1)", title=f"Hammett plot with {name}")
        ax.legend(fontsize=8)
    for name, x, mk in (("sigma_p", s2, "o"), ("sigma_p+", sp2, "s")):
        order = np.argsort(x[:8])
        axes[2].plot(x[:8][order], fits[name]["resid"][:8][order], mk + "-", label=name)
    axes[2].axhline(0, color="k", lw=0.8)
    axes[2].set(xlabel="substituent constant", ylabel="residual (log units)", title="Residuals, pH 2 data")
    axes[2].legend(fontsize=8)
    fig.tight_layout()
    out = runs_dir() / "lesson05_practical.png"
    fig.savefig(out, dpi=120)
    print(f"Saved {out.name}")


if __name__ == "__main__":
    main()
