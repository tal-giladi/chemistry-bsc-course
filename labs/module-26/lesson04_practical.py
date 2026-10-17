"""Lesson 26.4 Part B - module practical: from the lungs to cytochrome c oxidase.

Fill in the functions marked TODO, then run:  py lesson04_practical.py
Reference solution: lesson04_practical_solution.py
Fits the standard human blood O2 dissociation curve (hb_standard_curve.csv) with the Hill equation,
reads the cooperativity off the Hill plot, works out how much O2 the blood hands over, and turns that
O2 flow into the electric current and power of the respiratory chain.
Writes runs/lesson04_practical.png.
"""
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

from bio26 import (BOHR_LOG10, F, HUFNER, O2_SOLUBILITY, P50_MB, R, T_BODY, hb_standard_curve,
                   runs_dir, severinghaus)

HB_G_PER_DL = 15.0        # typical adult haemoglobin, g/dL
CARDIAC_OUTPUT = 50.0     # dL of blood per minute at rest (5 L/min)
MOLAR_VOLUME_STPD = 22.414  # L/mol, the volume behind "mL O2 STPD"
DELTA_E_CHAIN = 0.816 - (-0.32)  # V, NADH -> O2 (lesson 26.4, Part A)


def hill(p, p50, n):
    return p ** n / (p50 ** n + p ** n)


def fit_hill(p, s, lo=0.0, hi=1.0):
    """Nonlinear least-squares Hill fit to the points with lo < S < hi.
    Returns (p50, n) and their standard errors."""
    # TODO: m = (s > lo) & (s < hi); popt, pcov = curve_fit(hill, p[m], s[m], p0=(27, 2.7));
    # return popt, np.sqrt(np.diag(pcov))
    return None


def end_constants(p, s, low=2.0, high=400.0):
    """Dissociation constants of the first and last O2 from the ends of the Hill plot,
    where the slope returns to 1 and S/(1-S) = p/K. Returns (K_T, K_R) in mmHg."""
    # TODO: K = p * (1 - S) / S for each point; K_T = mean over p <= low, K_R = mean over p >= high
    return None


def o2_content(S, po2, hb=HB_G_PER_DL):
    """mL O2 per dL of blood: bound to Hb plus dissolved (Severinghaus eq. 6)."""
    # TODO: return HUFNER * hb * S + O2_SOLUBILITY * po2
    return None


def respiratory_current(vo2_ml_per_min):
    """Current (A) of electrons delivered to O2 by cytochrome c oxidase: 4 electrons per O2."""
    # TODO: mol O2 per second = vo2 / 1000 / MOLAR_VOLUME_STPD / 60; return 4 * F * that
    return None


def main():
    p, s = hb_standard_curve()
    if fit_hill(p, s) is None or end_constants(p, s) is None or o2_content(1.0, 0.0) is None \
            or respiratory_current(1.0) is None:
        print("TODO: write fit_hill(), end_constants(), o2_content() and respiratory_current() first.")
        return
    rms = lambda f: 100 * math.sqrt(np.mean((f - s) ** 2))

    print("1. Hill fits to the standard curve (37 C, pH 7.40)")
    (p50a, na), (ep, en) = fit_hill(p, s)
    print(f"   all 51 points:   P50 = {p50a:.2f} +/- {ep:.2f} mmHg, n = {na:.3f} +/- {en:.3f}, RMS = {rms(hill(p, p50a, na)):.2f} % sat")
    (p50m, nm), (ep, en) = fit_hill(p, s, 0.2, 0.8)
    print(f"   20-80 % only:    P50 = {p50m:.2f} +/- {ep:.2f} mmHg, n = {nm:.3f} +/- {en:.3f}, RMS (all points) = {rms(hill(p, p50m, nm)):.2f} % sat")
    print(f"   Severinghaus eq. (two terms, no fit): RMS = {rms(severinghaus(p)):.2f} % sat")
    worst = int(np.argmax(abs(hill(p, p50a, na) - s)))
    print(f"   largest Hill misfit at {p[worst]:.0f} mmHg: data {100 * s[worst]:.1f} %, Hill {100 * hill(p[worst], p50a, na):.1f} %")

    print("\n2. Cooperativity from the ends of the Hill plot")
    KT, KR = end_constants(p, s)
    dG = R * T_BODY * math.log(KT / KR) / 1000
    print(f"   K_T (first O2) = {KT:.0f} mmHg, K_R (last O2) = {KR:.2f} mmHg, ratio = {KT / KR:.0f}")
    print(f"   the fourth O2 binds {dG:.1f} kJ/mol more strongly than the first (RT ln ratio at 37 C)")
    print(f"   myoglobin for comparison: P50 = {P50_MB} mmHg, n = 1")

    print("\n3. O2 delivery at rest (arterial 100 mmHg, mixed venous 40 mmHg, Hb 15 g/dL, 5 L/min)")
    Sa, Sv = np.interp(100, p, s), np.interp(40, p, s)
    Ca, Cv = o2_content(Sa, 100), o2_content(Sv, 40)
    vo2 = (Ca - Cv) * CARDIAC_OUTPUT
    print(f"   arterial {Ca:.1f}, venous {Cv:.1f} mL O2/dL -> {Ca - Cv:.1f} mL/dL, VO2 = {vo2:.0f} mL O2/min")
    for label, f in (("standard curve", lambda x: np.interp(x, p, s)),
                     ("same P50, n = 1", lambda x: hill(x, p50a, 1.0)),
                     ("myoglobin-like", lambda x: hill(x, P50_MB, 1.0))):
        print(f"   share of bound O2 released 100 -> 40 mmHg, {label:16s}: {100 * (f(100) - f(40)):4.1f} %;"
              f" 100 -> 20 mmHg: {100 * (f(100) - f(20)):4.1f} %")
    p50_acid = p50a * 10 ** (BOHR_LOG10 * (7.20 - 7.40))
    print(f"   working muscle, pH 7.20: P50 -> {p50_acid:.1f} mmHg; S at 20 mmHg {100 * hill(20, p50a, na):.0f} % -> "
          f"{100 * hill(20, p50_acid, na):.0f} %")

    print("\n4. From O2 to electrons")
    I = respiratory_current(vo2)
    print(f"   {vo2:.0f} mL O2/min -> electron current {I:.0f} A; power at {DELTA_E_CHAIN:.3f} V = {I * DELTA_E_CHAIN:.0f} W")

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 4))
    pp = np.linspace(0.5, 150, 400)
    a1.plot(p, 100 * s, "o", ms=4, label="standard curve (data)")
    a1.plot(pp, 100 * hill(pp, p50a, na), "-", label=f"Hill, all points (n = {na:.2f})")
    a1.plot(pp, 100 * hill(pp, p50a, 1.0), ":", label="same P50, n = 1")
    a1.plot(pp, 100 * hill(pp, p50_acid, na), "--", label="Hill at pH 7.20 (Bohr)")
    a1.set_xlim(0, 150); a1.set_xlabel("PO2 (mmHg)"); a1.set_ylabel("saturation (%)"); a1.legend(fontsize=8)
    a2.semilogx(p, 100 * (hill(p, p50a, na) - s), "o-", ms=3, label="Hill (all points)")
    a2.semilogx(p, 100 * (severinghaus(p) - s), "s-", ms=3, label="Severinghaus equation")
    a2.axhline(0, color="k", lw=0.8)
    a2.set_xlabel("PO2 (mmHg)"); a2.set_ylabel("model - data (% saturation)"); a2.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(runs_dir() / "lesson04_practical.png", dpi=120)
    print("wrote runs/lesson04_practical.png")


if __name__ == "__main__":
    main()
