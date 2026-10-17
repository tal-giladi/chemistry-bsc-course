"""Module 19 practical: develop and validate an HPLC-UV method for caffeine in an energy drink.
Part 1 chooses the column and flow from van Deemter fits under a pressure limit; part 2 checks the
resolution; part 3 calibrates, finds the LOD and LOQ, checks recovery and reports the drink.

Reference solution. Run from this folder:
    py practical_hplc_solution.py
Data: hplc_vandeemter.csv and caffeine_hplc.csv (simulated).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

from ana19 import HERE, read_csv, line_fit, conc_from_line, save

L_MM, ID_MM, POROSITY = 100.0, 4.6, 0.65          # column length, inner diameter, total porosity
BAR_PER_ML_MIN = {"C18_5um": 80.0, "C18_2.7um_coreshell": 274.0}   # measured back-pressure at 1 mL/min
P_MAX_BAR = 400.0                                 # the pump's limit
K_CAFF, ALPHA = 3.0, 1.10                         # caffeine retention factor and selectivity to its neighbour
LABEL_MG_L, DILUTION, EU_WARNING_MG_L = 320.0, 10.0, 150.0


def van_deemter(u, A, B, C):
    return A + B / u + C * u


def flow_from_u(u_mm_s):
    """Volumetric flow (mL/min) that gives linear velocity u in this column."""
    area = np.pi * (ID_MM / 2) ** 2 * POROSITY     # mm2 of open cross-section
    return u_mm_s * area * 60 / 1000


def resolution(N, alpha, k):
    """Purnell equation (Harvey 12.3)."""
    return np.sqrt(N) / 4 * (alpha - 1) / alpha * k / (1 + k)


def choose_operating_point(col, u, H):
    """Fit van Deemter, then pick u_opt or, if the pump cannot reach it, the fastest allowed u."""
    # TODO 1
    (A, B, C), _ = curve_fit(van_deemter, u, H, p0=[3, 8, 2])
    u_opt = np.sqrt(B / C)
    u_max = P_MAX_BAR / BAR_PER_ML_MIN[col] / flow_from_u(1.0)
    u_run = min(u_opt, u_max)
    return (A, B, C), u_opt, u_max, u_run


def validate(d):
    """Calibration, LOD/LOQ from blanks, drink result and spike recovery (Lesson 09.4)."""
    std = d["type"] == "standard"
    x, y = d["c_mg_per_L"][std], d["peak_area"][std]
    m, b, s_r, res = line_fit(x, y)
    s_bl = d["peak_area"][d["type"] == "blank"].std(ddof=1)
    # TODO 2
    lod, loq = 3 * s_bl / m, 10 * s_bl / m
    c, s_c = conc_from_line(d["peak_area"][d["type"] == "drink_1to10"], x, y, m, b, s_r)
    sp = d["type"] == "spike_recovery"
    m_sp, b_sp, _, _ = line_fit(d["c_mg_per_L"][sp], d["peak_area"][sp])
    recovery = m_sp / m
    return m, b, s_r, res, x, lod, loq, c, s_c, recovery


def main():
    v = read_csv(HERE / "hplc_vandeemter.csv")
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    print("Part 1-2: columns (100 x 4.6 mm), pump limit 400 bar")
    for col in BAR_PER_ML_MIN:
        s = v["column"] == col
        u, H = v["u_mm_per_s"][s], v["H_um"][s]
        (A, B, C), u_opt, u_max, u_run = choose_operating_point(col, u, H)
        H_run = van_deemter(u_run, A, B, C)
        N = L_MM * 1000 / H_run
        t_r = L_MM * (1 + K_CAFF) / u_run / 60
        print(f"  {col}: A={A:.1f} um  B={B:.1f} um mm/s  C={C:.2f} um s/mm")
        print(f"     u_opt {u_opt:.2f} mm/s ({flow_from_u(u_opt):.2f} mL/min, {BAR_PER_ML_MIN[col] * flow_from_u(u_opt):.0f} bar); "
              f"pump allows u up to {u_max:.2f} mm/s")
        print(f"     run at {flow_from_u(u_run):.2f} mL/min: H = {H_run:.1f} um, N = {N:.0f}, Rs = {resolution(N, ALPHA, K_CAFF):.2f}, caffeine at {t_r:.1f} min")
        uu = np.linspace(0.3, 4.2, 200)
        ax[0].plot(u, H, "o")
        ax[0].plot(uu, van_deemter(uu, A, B, C), "-", label=col)
        ax[0].axvline(u_run, ls=":", color=ax[0].lines[-1].get_color())
    ax[0].set(xlabel="u (mm/s)", ylabel="H (um)", title="van Deemter, dotted = chosen u", ylim=(0, 40))
    ax[0].legend()

    d = read_csv(HERE / "caffeine_hplc.csv")
    m, b, s_r, res, x, lod, loq, c, s_c, rec = validate(d)
    print("Part 3: validation")
    print(f"  area = {b:.2f} + {m:.3f} c   s_r = {s_r:.2f}; residuals " + " ".join(f"{r:+.1f}" for r in res))
    print(f"  LOD = {lod:.3f} mg/L, LOQ = {loq:.3f} mg/L (from 10 blanks)")
    print(f"  spike recovery: slope ratio {rec:.3f} ({100 * rec:.1f} %)")
    drink, s_drink = DILUTION * c, DILUTION * s_c
    print(f"  vial {c:.2f} +/- {s_c:.2f} mg/L -> drink {drink:.0f} +/- {s_drink:.0f} mg/L "
          f"({drink / 10:.1f} mg per 100 mL; {100 * drink / LABEL_MG_L:.0f} % of the 320 mg/L label)")
    print(f"  above {EU_WARNING_MG_L:.0f} mg/L, so the EU 'high caffeine content' statement is required: {drink > EU_WARNING_MG_L}")
    ax[1].axhline(0, color="grey", lw=0.8)
    ax[1].plot(x, res, "o")
    ax[1].set(xlabel="c (mg/L)", ylabel="residual (area)", title="Calibration residuals")
    save(fig, "practical_hplc.png")


if __name__ == "__main__":
    main()
