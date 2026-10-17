"""Generate the example data for the Module 10 labs (seeded, so the files never change).

Run:   py make_data.py
The models and their true parameters are written here so you can check your answers.
The data are realistic but NOT measured. Replace them with your own measurements.
"""
import math
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
rng = np.random.default_rng(1010)
KW = 1.0e-14


def write(name, lines):
    (HERE / name).write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def drop_calibration():
    """Lesson 10.1. A 10 mL oral syringe (no needle) is weighed, 40 drops of baking-soda
    titrant are squeezed out, and it is weighed again; three trials.
    True drop mass 0.0450 g, drop-to-drop sd 0.0025 g; scale resolution 0.01 g."""
    lines = ["trial,n_drops,m_before_g,m_after_g"]
    for trial in (1, 2, 3):
        before = 18.0 + rng.uniform(0, 2)
        out = rng.normal(0.0450, 0.0025, 40).sum()
        lines.append(f"{trial},40,{round(before, 2):.2f},{round(before - out, 2):.2f}")
    write("drop_calibration_example.csv", lines)


def ph_of_volume(v_b, c_a, v_a, c_b, ka):
    """Exact pH of weak acid HA (c_a, v_a mL) after v_b mL of strong base, from the charge balance."""
    def f(ph):
        h = 10.0 ** -ph
        alpha = ka / (ka + h)
        return v_b * (c_b + h - KW / h) - v_a * (c_a * alpha - h + KW / h)
    return brentq(f, 0.0, 14.0)


def potentiometric():
    """Lesson 10.2. 25.00 mL of 0.0800 M acetic acid (pKa 4.757) titrated with 0.1000 M NaOH,
    pH electrode read after each addition. True V_eq = 20.00 mL.
    Electrode: calibration offset +0.04 pH, slow drift +0.002 pH per reading, noise sd 0.01 pH.
    Activity effects ignored (so the Gran slope gives Ka directly)."""
    ka = 10 ** -4.757
    vols = list(np.arange(0, 16, 2.0)) + list(np.arange(16, 19, 0.5)) + \
        list(np.arange(19, 21.001, 0.1)) + list(np.arange(21.5, 24.01, 0.5)) + list(np.arange(26, 30.01, 2.0))
    lines = ["V_mL,pH"]
    for i, v in enumerate(vols):
        ph = ph_of_volume(v, 0.0800, 25.00, 0.1000, ka) + 0.04 + 0.002 * i + rng.normal(0, 0.01)
        lines.append(f"{v:.2f},{ph:.3f}")
    write("potentiometric_example.csv", lines)


def redox():
    """Lesson 10.2. 25.00 mL of 0.0500 M Fe2+ in 1 M H2SO4 titrated with 0.1000 M Ce4+.
    Formal potentials in 1 M H2SO4 (Harvey App. 16.13): Fe3+/Fe2+ 0.68 V, Ce4+/Ce3+ 1.44 V vs SHE.
    Platinum indicator electrode against Ag/AgCl (saturated KCl, +0.197 V vs SHE). True V_eq = 12.50 mL.
    Noise sd 2 mV."""
    e_fe, e_ce, ref, veq = 0.68, 1.44, 0.197, 12.50
    vols = list(np.arange(0.5, 11.0, 1.0)) + list(np.arange(11.0, 12.0, 0.5)) + \
        list(np.arange(12.0, 13.001, 0.1)) + list(np.arange(13.5, 15.01, 0.5)) + list(np.arange(16, 20.01, 1.0))
    lines = ["V_mL,E_mV"]
    for v in vols:
        if abs(v - veq) < 1e-6:
            e = (e_fe + e_ce) / 2
        elif v < veq:
            e = e_fe + 0.05916 * math.log10(v / (veq - v))
        else:
            e = e_ce + 0.05916 * math.log10((v - veq) / veq)
        lines.append(f"{v:.2f},{1000 * (e - ref) + rng.normal(0, 2):.1f}")
    write("redox_example.csv", lines)


def oven():
    """Lesson 10.4. 10.00 g of baking soda in a 3.52 g foil tray, heated at about 200 C in a kitchen
    oven, cooled 15 min and weighed after each period. 2 NaHCO3 -> Na2CO3 + H2O + CO2.
    True purity 100 %; theoretical mass loss 36.92 %. Conversion x = 1 - exp(-k t), k = 0.08 per min.
    Systematic error: the warm, dry Na2CO3 takes up 0.015 g of water vapour while it cools.
    Scale resolution 0.01 g, noise sd 0.005 g."""
    tray, m0, k = 3.52, 10.00, 0.08
    loss = (18.015 + 44.009) / (2 * 84.006)
    lines = ["t_min,m_total_g"]
    for t in (0, 15, 30, 45, 60, 75, 90):
        x = 1 - math.exp(-k * t)
        m = tray + m0 * (1 - loss * x) + (0.015 if t else 0.0) + rng.normal(0, 0.005)
        lines.append(f"{t},{round(m, 2):.2f}")
    write("oven_example.csv", lines)


def fluoride_ise():
    """Lesson 10.5. Fluoride ISE with TISAB II, standards and samples mixed 1:1 with TISAB.
    Concentrations are those of the standard or sample BEFORE adding TISAB (mg/L F-).
    Response in the mixture: E = K - S log10(c_mix + c_low), K = -60.0 mV, S = 57.8 mV/decade,
    c_low = 0.01 mg/L (curvature near the detection limit). Noise sd 0.3 mV.
    Samples: A true 0.85 mg/L, B true 0.12 mg/L.
    Standard addition on A: 50.0 mL sample + 50.0 mL TISAB, then 1.00 mL of 100.0 mg/L F- added."""
    k, s, c_low = -60.0, 57.8, 0.01

    def e(c_mix):
        return k - s * math.log10(c_mix + c_low) + rng.normal(0, 0.3)
    lines = ["kind,label,c_mg_L,E_mV"]
    for c in (0.10, 0.20, 0.50, 1.00, 2.00, 5.00, 10.0):
        lines.append(f"standard,std {c:g},{c:.2f},{e(c / 2):.1f}")
    lines.append(f"sample,A,,{e(0.85 / 2):.1f}")
    lines.append(f"sample,B,,{e(0.12 / 2):.1f}")
    lines.append(f"addition_before,A,,{e(0.85 * 50.0 / 100.0):.1f}")
    lines.append(f"addition_after,A,,{e((0.85 * 50.0 + 100.0 * 1.00) / 101.0):.1f}")
    write("fluoride_ise_example.csv", lines)


def soap_test():
    """Lesson 10.5. 20 mL of each water in a small jar with a lid; liquid castile-type soap (no
    detergent) added one drop at a time with shaking until a lather lasts 30 s.
    Model: drops = 2.0 + 0.055 * hardness (mg/L as CaCO3), noise sd 0.6 drop, rounded.
    Bottled waters (labels): low-mineral Ca 6 Mg 2; B Ca 32 Mg 12; C Ca 75 Mg 30 mg/L.
    True tap hardness 260 mg/L; boiled and cooled tap water 200 mg/L (some temporary hardness removed)."""
    waters = [("low-mineral bottled", 6, 2, None), ("bottled B", 32, 12, None),
              ("bottled C", 75, 30, None), ("tap", None, None, 260.0), ("tap boiled", None, None, 200.0)]
    lines = ["water,ca_mg_L,mg_mg_L,drops"]
    for name, ca, mg, h in waters:
        hard = h if h is not None else 2.497 * ca + 4.118 * mg
        for _ in range(2):
            d = round(2.0 + 0.055 * hard + rng.normal(0, 0.6))
            lines.append(f"{name},{'' if ca is None else ca},{'' if mg is None else mg},{d}")
    write("soap_test_example.csv", lines)


def vinegar_project():
    """Lesson 10.6. Mass-based titration of white vinegar with baking-soda titrant
    (5.00 g NaHCO3 made up to 100.00 g), red-cabbage indicator, five trials and one indicator blank
    (25 mL water + 2 mL indicator titrated to the same blue-green). True acetic acid 4.95 % w/w.
    End point overshoots by 0.07 g titrant on average (sd 0.04 g); the blank needs 0.06 g.
    Scale resolution 0.01 g."""
    w = 5.00 / 100.00 / 84.006        # mol per g
    lines = ["trial,m_vinegar_g,m_syringe_before_g,m_syringe_after_g"]
    for trial in range(1, 6):
        m_v = round(rng.uniform(4.9, 5.2), 2)
        need = m_v * 0.0495 / 60.052 / w + 0.07 + rng.normal(0, 0.04)
        before = round(rng.uniform(17.5, 18.5), 2)
        lines.append(f"{trial},{m_v:.2f},{before:.2f},{round(before - need, 2):.2f}")
    before = round(rng.uniform(17.5, 18.5), 2)
    lines.append(f"blank,0.00,{before:.2f},{round(before - 0.06, 2):.2f}")
    write("vinegar_project_example.csv", lines)


if __name__ == "__main__":
    drop_calibration()
    potentiometric()
    redox()
    oven()
    fluoride_ise()
    soap_test()
    vinegar_project()
    print("wrote 7 example files")
