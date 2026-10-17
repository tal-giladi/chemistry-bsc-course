"""Lesson 25.2 (reference solution): quinine fluorescence in tonic water.
Part 1 (home photos): linear range and inner filter of a tonic dilution series; Stern-Volmer quenching by table salt.
Part 2 (bench fluorimeter, simulated): quinine by external calibration and by standard addition, against the
83 mg/L limit of 21 CFR 172.575.

Run (from this folder):
    py lesson02_quinine_solution.py                      # example data
    py lesson02_quinine_solution.py my_tonic.csv         # your own photos, same columns as tonic_home_example.csv
"""
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

from ana25 import HERE, read_csv, line_fit, conc_from_line, standard_addition, srgb_to_linear, save

M_NACL = 58.44          # g/mol (PubChem)
LIMIT = 83.0            # mg/L quinine, 21 CFR 172.575 (eCFR, read 2026-10-17)


def stern_volmer(cl_molar, F):
    """Return K_SV (L/mol) and intercept from F0/F = 1 + K [Cl-], with F0 the salt-free signal."""
    F0 = F[cl_molar == 0].mean()
    m, b, _, _ = line_fit(cl_molar, F0 / F)
    return m, b


def tonic_by_standard_addition(added, signal, flask_factor, dilution):
    """Quinine in the tonic (mg/L) and its standard deviation from a standard-addition series.
    flask_factor: final volume / volume of diluted tonic in the flask; dilution: dilution of the tonic."""
    c, s, m, b = standard_addition(added, signal)
    return c * flask_factor * dilution, s * flask_factor * dilution


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else HERE / "tonic_home_example.csv"
    h = read_csv(path)
    F = srgb_to_linear(h["blue_srgb"]) - srgb_to_linear(h["dark_srgb"])
    dil = h["series"] == "dilution"
    fr = np.unique(h["tonic_fraction"][dil])
    Fm = np.array([F[dil & (h["tonic_fraction"] == x)].mean() for x in fr])
    low = (fr > 0) & (fr <= 0.0625)
    slope = np.sum(fr[low] * Fm[low]) / np.sum(fr[low] ** 2)      # line through the origin
    print("Home dilution series (linear blue signal, dark subtracted):")
    for x, y in zip(fr, Fm):
        print(f"   tonic fraction {x:7.4f}: F = {y:.4f}   ({100 * y / (slope * x) if x > 0 else 0:5.0f} % of the low-range line)")

    salt = h["series"] == "salt"
    cl = h["salt_g_per_100mL"][salt] / M_NACL * 10
    K, b0 = stern_volmer(cl, F[salt])
    print(f"Stern-Volmer with table salt: K_SV = {K:.0f} L/mol (intercept {b0:.2f}); "
          f"half the signal is gone at {1000 / K:.1f} mmol/L chloride = {M_NACL / K * 0.1:.2f} g salt per 100 mL")

    q = read_csv(HERE / "quinine_fluorimeter.csv")
    t, x, y = q["type"], q["quinine_added_or_std_mg_per_L"], q["fluorescence"]
    ext = t == "external_std"
    m, b, s_r, _ = line_fit(x[ext], y[ext])
    c1, s1 = conc_from_line(y[t == "tonic_1to200"], x[ext], y[ext], m, b, s_r)
    ext_mgL, ext_s = 200 * c1, 200 * s1
    sa = t == "std_addition"
    sa_mgL, sa_s = tonic_by_standard_addition(x[sa], y[sa], flask_factor=2.0, dilution=100)
    t95 = stats.t.ppf(0.975, sa.sum() - 2)
    print(f"External calibration: F = {b:.1f} + {m:.1f} c; tonic = {ext_mgL:.1f} +/- {ext_s:.1f} mg/L (s)")
    print(f"Standard addition:    tonic = {sa_mgL:.1f} +/- {sa_s:.1f} mg/L (s); 95 % interval +/- {t95 * sa_s:.1f}")
    verdict = "below" if sa_mgL + t95 * sa_s < LIMIT else "NOT clearly below"
    print(f"Limit {LIMIT:.0f} mg/L: the tonic is {verdict} the limit.")

    fig, ax = plt.subplots(1, 3, figsize=(14, 4))
    ax[0].plot(fr, Fm, "o")
    ff = np.linspace(0, 1, 50)
    ax[0].plot(ff, slope * ff, "--", label="low-range line")
    ax[0].set(xlabel="tonic fraction", ylabel="linear blue signal", title="Inner filter at high strength", ylim=(0, 1.2 * Fm.max()))
    ax[0].legend()
    F0 = F[salt][cl == 0].mean()
    ax[1].plot(1000 * cl, F0 / F[salt], "o")
    cc = np.linspace(0, cl.max(), 20)
    ax[1].plot(1000 * cc, b0 + K * cc, "-")
    ax[1].set(xlabel="chloride (mmol/L)", ylabel="F0 / F", title="Stern-Volmer")
    ax[2].plot(x[sa], y[sa], "o")
    xx = np.linspace(-sa_mgL / 200 * 1.1, x[sa].max(), 20)
    cs, _, ms, bs = standard_addition(x[sa], y[sa])
    ax[2].plot(xx, bs + ms * xx, "-")
    ax[2].axhline(0, color="grey", lw=0.8)
    ax[2].set(xlabel="quinine added (mg/L in flask)", ylabel="fluorescence", title="Standard addition")
    save(fig, "lesson02_quinine.png")


if __name__ == "__main__":
    main()
