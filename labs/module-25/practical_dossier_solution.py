"""Module 25 practical (reference solution): a quality-control dossier for a cloudy bitter-lemon drink.
  1. tartrazine by UV-Vis at 426 nm with a 700 nm turbidity baseline       (Lesson 25.1)
  2. quinine by fluorescence: external calibration against standard addition (Lesson 25.2)
  3. flavour identity by GC-MS match + retention index                     (Lesson 25.4)
  4. vitamin C by voltammetric standard addition                           (Lesson 25.6)
Every result gets an expanded uncertainty U = 2 s and a decision against the label or the legal limit.

Run (from this folder):
    py practical_dossier_solution.py
Data: practical_drink.csv (simulated); part 3 uses the GC-MS run made by get_nist_ms.py.
"""
import numpy as np

from ana25 import HERE, DOWNLOADED, read_csv, line_fit, conc_from_line, standard_addition

QUININE_LIMIT = 83.0     # mg/L, 21 CFR 172.575
LABEL = {"tartrazine": 25.0, "quinine target": 65.0, "vitamin C": 120.0}   # mg/L, from the recipe and label
TOLERANCE = {"tartrazine": (0.90, 1.10), "vitamin C": (0.80, 1.50)}         # the producer's own specification


def turbidity_corrected(A426, A700):
    """Subtract the scattering baseline read at 700 nm, where neither dye nor drink absorbs."""
    return A426 - A700


def decide(value, U, low=None, high=None):
    """'pass' if the whole interval value +/- U lies inside [low, high], 'fail' if it lies wholly outside,
    otherwise 'inconclusive' (more replicates or a better method needed)."""
    lo, hi = value - U, value + U
    low = -np.inf if low is None else low
    high = np.inf if high is None else high
    if lo >= low and hi <= high:
        return "pass"
    if hi < low or lo > high:
        return "fail"
    return "inconclusive"


def main():
    d = read_csv(HERE / "practical_drink.csv")
    t, x, y, y2 = d["type"], d["x"], d["signal"], d["signal2"]
    print("QC dossier: bitter-lemon soft drink (simulated data)\n")

    # 1. tartrazine
    std = t == "uv_std"
    Ac = turbidity_corrected(y[std], y2[std])
    m, b, s_r, _ = line_fit(x[std], Ac)
    smp = t == "uv_drink_1to5"
    c, s = conc_from_line(turbidity_corrected(y[smp], y2[smp]), x[std], Ac, m, b, s_r)
    tz, U = 5 * c, 2 * 5 * s
    raw, _ = conc_from_line(y[smp], x[std], Ac, m, b, s_r)
    lo, hi = TOLERANCE["tartrazine"]
    print(f"1. Tartrazine: {tz:.1f} +/- {U:.1f} mg/L (U, k = 2); without the 700 nm baseline {5 * raw:.1f} mg/L")
    print(f"   recipe {LABEL['tartrazine']:.0f} mg/L, accepted {100 * lo:.0f}-{100 * hi:.0f} %: "
          f"{decide(tz, U, lo * LABEL['tartrazine'], hi * LABEL['tartrazine'])}")

    # 2. quinine
    ext = t == "fl_std"
    m, b, s_r, _ = line_fit(x[ext], y[ext])
    sa = t == "fl_std_addition"
    unspiked = y[sa & (x == 0)]
    c_ext, s_ext = conc_from_line(unspiked, x[ext], y[ext], m, b, s_r)
    c_sa, s_sa, m_sa, _ = standard_addition(x[sa], y[sa])
    factor = 2 * 50                                # 5 mL in 10 mL, drink diluted 1 + 49
    q_ext, q_sa, U_sa = factor * c_ext, factor * c_sa, 2 * factor * s_sa
    print(f"2. Quinine: external calibration {q_ext:.1f} mg/L; standard addition {q_sa:.1f} +/- {U_sa:.1f} mg/L")
    print(f"   slope in the drink / slope in clean acid = {m_sa / m:.2f}: the matrix removes {100 * (1 - m_sa / m):.0f} % of the signal,"
          f" so the standard-addition value is reported")
    print(f"   legal limit {QUININE_LIMIT:.0f} mg/L: {decide(q_sa, U_sa, high=QUININE_LIMIT)}; "
          f"recipe target {LABEL['quinine target']:.0f} mg/L ({100 * q_sa / LABEL['quinine target']:.0f} % of target)")

    # 3. GC-MS
    print("3. Flavour (GC-MS of the oil fraction, Lesson 25.4):")
    if (DOWNLOADED / "gcms_run.csv").exists():
        import lesson04_gcms_solution as g
        g.main()
        print("   limonene, neral and geranial identified by MS + RI: consistent with lemon flavour. GC-MS cannot"
              " show that it is natural; that needs the enantiomer ratio (chiral GC) or isotope ratios.")
    else:
        print("   run  py get_nist_ms.py  first, then repeat (needs internet once)")

    # 4. vitamin C
    cv = t == "cv_std_addition"
    c_v, s_v, m_v, b_v = standard_addition(x[cv], y[cv])
    vc, Uv = 10 * c_v, 2 * 10 * s_v
    lo, hi = TOLERANCE["vitamin C"]
    print(f"4. Vitamin C: peak current = {b_v:.2f} + {m_v:.3f} x added (uA, mg/L); drink {vc:.0f} +/- {Uv:.0f} mg/L "
          f"= {100 * vc / LABEL['vitamin C']:.0f} % of the declared {LABEL['vitamin C']:.0f} mg/L")
    print(f"   accepted {100 * lo:.0f}-{100 * hi:.0f} % of the declared value: "
          f"{decide(vc, Uv, lo * LABEL['vitamin C'], hi * LABEL['vitamin C'])}")


if __name__ == "__main__":
    main()
