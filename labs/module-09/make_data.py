"""Generate the simulated example data sets for the Module 9 labs (fixed seeds, so the files are reproducible).

Run (from this folder):
    py make_data.py
Every data set is made from a known model; the true values are written in the file header and below,
so you can check your analysis against them. None of these numbers is a real measurement.
"""
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
W_CL_NACL = 35.453 / 58.443   # mass fraction of chloride in pure NaCl (IUPAC atomic weights), 0.6066


def write(name, header, cols, rows):
    lines = [f"# {h}" for h in header] + [",".join(cols)]
    lines += [",".join(str(v) for v in r) for r in rows]
    (HERE / name).write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print("wrote", name)


def crm_analysts(seed=1):
    """09.1: two analysts each analyse a chloride CRM certified at 25.0 mg/L, 6 times.
    Analyst A: unbiased, sd 0.8 mg/L (imprecise). Analyst B: bias -1.2 mg/L, sd 0.2 mg/L (precise, inaccurate)."""
    rng = np.random.default_rng(seed)
    a = 25.0 + rng.normal(0, 0.8, 6)
    b = 25.0 - 1.2 + rng.normal(0, 0.2, 6)
    rows = [("A", f"{x:.2f}") for x in a] + [("B", f"{x:.2f}") for x in b]
    write("crm_analysts.csv",
          ["Simulated (make_data.py, seed 1). Chloride CRM, certified 25.0 +/- 0.3 mg/L (k = 2).",
           "True model: analyst A no bias, sd 0.8; analyst B bias -1.2 mg/L, sd 0.2."],
          ["analyst", "chloride_mg_per_L"], rows)


def sample_size_series(seed=2):
    """09.1: chloride found (mg) in different masses of pure NaCl (the reference material).
    True model: found = 606.6 * (1 - 0.015) * m + 0.80 mg, noise sd 0.25 mg.
    1.5 % proportional error (titrant concentration taken too high), +0.80 mg constant error (indicator blank)."""
    rng = np.random.default_rng(seed)
    m = np.array([0.050, 0.075, 0.100, 0.150, 0.200, 0.250, 0.300])
    found = 1000 * W_CL_NACL * (1 - 0.015) * m + 0.80 + rng.normal(0, 0.25, m.size)
    write("sample_size_series.csv",
          ["Simulated (make_data.py, seed 2). Chloride found by titration in weighed portions of pure NaCl.",
           "Expected chloride = 606.6 mg/g x sample mass. True errors: proportional -1.5 %, constant +0.80 mg."],
          ["sample_g", "chloride_found_mg"], [(f"{a:.4f}", f"{b:.2f}") for a, b in zip(m, found)])


def coins(seed=3):
    """09.1 home: n one-shekel coins on a 0.1 g kitchen scale. True mean coin 3.48 g (slightly worn),
    scale offset +0.3 g (constant error), gain +0.4 % (proportional), read to 0.1 g."""
    rng = np.random.default_rng(seed)
    n = np.arange(0, 11)
    true = n * 3.48 + rng.normal(0, 0.02, n.size) * np.sqrt(n)
    reading = np.round((true * 1.004 + 0.3) / 0.1) * 0.1
    write("coins_example.csv",
          ["Simulated (make_data.py, seed 3). n one-shekel coins (nominal 3.5 g, Bank of Israel) on a 0.1 g scale.",
           "True model: coin 3.48 g, scale offset +0.3 g, gain +0.4 %."],
          ["n_coins", "reading_g"], [(a, f"{b:.1f}") for a, b in zip(n, reading)])


def replicates(seed=4):
    """09.2: two methods on the chloride CRM (certified 25.0 mg/L).
    Method 1 (titration): 7 results, mean 25.0, sd 0.35. Method 2 (ion-selective electrode): 6 results,
    mean 24.4 (bias -0.6), sd 0.30, plus one transcription slip (an extra 2.0 mg/L on one result)."""
    rng = np.random.default_rng(seed)
    m1 = 25.0 + rng.normal(0, 0.35, 7)
    m2 = 24.4 + rng.normal(0, 0.30, 7)
    m2[4] += 2.0
    rows = [("titration", f"{x:.2f}") for x in m1] + [("ise", f"{x:.2f}") for x in m2]
    write("replicates.csv",
          ["Simulated (make_data.py, seed 4). Chloride CRM certified 25.0 +/- 0.3 mg/L (k = 2).",
           "True model: titration unbiased sd 0.35; ISE bias -0.6 sd 0.30; ISE result 5 has a +2.0 slip."],
          ["method", "chloride_mg_per_L"], rows)


def nitrite(seed=5):
    """09.4: Griess-type nitrite calibration at 540 nm, 1 cm cell (simulated, not a real method validation).
    True model: A = 0.004 + 2.90 * c (c in mg/L as N), noise sd 0.0020 + 0.5 % of A.
    Blanks: 10 reagent blanks. Unknown: 3 readings of a sample, true 0.0620 mg/L.
    Standard additions on a second sample whose matrix lowers the slope by 12 %, true 0.0400 mg/L."""
    rng = np.random.default_rng(seed)
    noise = lambda a: rng.normal(0, 0.0020 + 0.005 * a)
    c = np.array([0.0, 0.02, 0.05, 0.10, 0.15, 0.20, 0.25])
    rows = []
    for x in c:
        a = 0.004 + 2.90 * x
        rows.append(("standard", f"{x:.3f}", f"{a + noise(a):.4f}"))
    for _ in range(10):
        rows.append(("blank", "0.000", f"{0.004 + noise(0.004):.4f}"))
    for _ in range(3):
        a = 0.004 + 2.90 * 0.0620
        rows.append(("unknown", "", f"{a + noise(a):.4f}"))
    for add in (0.0, 0.05, 0.10, 0.15):   # added concentration after spiking, mg/L
        a = 0.004 + 2.90 * 0.88 * (0.0400 + add)
        rows.append(("addition", f"{add:.3f}", f"{a + noise(a):.4f}"))
    write("nitrite_calibration.csv",
          ["Simulated (make_data.py, seed 5). Nitrite (as N) by a Griess-type colour reaction, 540 nm, 1 cm.",
           "True: A = 0.004 + 2.90 c; unknown 0.0620 mg/L; addition sample 0.0400 mg/L with slope x 0.88 (matrix).",
           "type: standard (c = standard conc), blank, unknown (c empty), addition (c = conc added by the spike)."],
          ["type", "c_mg_per_L", "absorbance"], rows)


def titration(seed=6):
    """09.5: 25.00 mL of 0.1000 mol/L acetic acid titrated with 0.1000 mol/L NaOH, pH meter.
    Exact curve from the charge balance (pKa 4.757, Kw 1.0e-14), then a +0.03 pH calibration offset and
    noise sd 0.01 pH. Steps of 1 mL, 0.2 mL from 23 to 27 mL."""
    from scipy.optimize import brentq
    rng = np.random.default_rng(seed)
    ka, kw, ca, va, cb = 10 ** -4.757, 1.0e-14, 0.1000, 25.00, 0.1000

    def ph(vb):
        cat, na = ca * va / (va + vb), cb * vb / (va + vb)
        f = lambda p: na + 10 ** -p - kw / 10 ** -p - cat * ka / (ka + 10 ** -p)
        return brentq(f, 0, 14)

    v = np.concatenate([np.arange(0, 23, 1.0), np.arange(23, 27.01, 0.2), np.arange(28, 36, 1.0)])
    rows = [(f"{x:.2f}", f"{ph(x) + 0.03 + rng.normal(0, 0.01):.3f}") for x in v]
    write("titration_weak_acid.csv",
          ["Simulated (make_data.py, seed 6). 25.00 mL 0.1000 M acetic acid + 0.1000 M NaOH.",
           "True equivalence 25.00 mL; pKa 4.757; meter offset +0.03 pH; noise sd 0.01 pH."],
          ["V_NaOH_mL", "pH"], rows)


def srgb_encode(lin):
    lin = np.clip(lin, 0, 1)
    return np.where(lin <= 0.0031308, 12.92 * lin, 1.055 * lin ** (1 / 2.4) - 0.055)


def dye_photos(seed=7):
    """09.6 module practical: blue food colouring (Brilliant Blue FCF absorbs near 630 nm, so the red
    channel carries the signal). Standards by mass as % of a stock, photographed from above in identical cups.
    Camera model: true red absorbance A = 0.105 * c (c in % stock); 3 % stray light flattens the top;
    lighting changes 1.5 % between photos; green and blue channels absorb a little; values in sRGB 0-255."""
    rng = np.random.default_rng(seed)
    white = np.array([0.80, 0.82, 0.78])          # linear RGB of the white paper under daylight
    k = np.array([0.105, 0.020, 0.004])           # absorbance per % stock in R, G, B
    stray = 0.03

    def photo(c):
        a = k * c
        lin = white * (10 ** -a + stray) / (1 + stray) * (1 + rng.normal(0, 0.015))
        return np.round(255 * srgb_encode(lin)).astype(int)

    rows = []
    for c in (0, 1, 2, 3, 4, 6, 8, 10, 14):
        r, g, b = photo(c)
        rows.append(("standard", c, r, g, b))
    for _ in range(7):
        r, g, b = photo(0)
        rows.append(("blank", 0, r, g, b))
    for _ in range(3):
        r, g, b = photo(4.7)
        rows.append(("unknown", "", r, g, b))
    for _ in range(3):
        r, g, b = photo(5.0)
        rows.append(("check", 5, r, g, b))
    write("dye_photo_example.csv",
          ["Simulated (make_data.py, seed 7). Blue food colouring, % of stock by mass, phone photos from above.",
           "True: A_red = 0.105 c, 3 % stray light, lighting noise 1.5 %. Unknown 4.7 %; check standard 5.0 %.",
           "type: standard, blank (repeat photos of the water cup), unknown, check (independent 5 % standard)."],
          ["type", "c_percent_stock", "R", "G", "B"], rows)


if __name__ == "__main__":
    crm_analysts()
    sample_size_series()
    coins()
    replicates()
    nitrite()
    titration()
    dye_photos()
