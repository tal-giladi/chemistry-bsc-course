"""Lesson 19.4: retention indices on two GC columns, and an internal-standard calibration
(ethanol in hand sanitizer by GC-FID).

Reference solution. Run from this folder:
    py lesson04_gc_solution.py
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from ana19 import HERE, read_csv, line_fit, conc_from_line, save

NIST_RI = {  # NIST Chemistry WebBook, Gas Chromatography pages, checked 2026-10-17 (ramped runs)
    "limonene (CAS 138-86-3)": {"DB-5": 1031, "DB-Wax": 1196},
    "linalool (CAS 78-70-6)": {"DB-5": 1098, "DB-Wax": 1552},
}


def retention_index(t_x, alkanes):
    """Linear (temperature-programmed) retention index. alkanes = {carbon number: retention time}."""
    ns = sorted(alkanes)
    for n, n1 in zip(ns, ns[1:]):
        if alkanes[n] <= t_x <= alkanes[n1]:
            # TODO 1
            return 100 * (n + (t_x - alkanes[n]) / (alkanes[n1] - alkanes[n]))
    raise ValueError("peak is outside the alkane ladder: add more alkanes")


def internal_standard_result(c_std, ratio_std, ratio_sample):
    """Fit area ratio (analyte/IS) against concentration and read the sample. Returns m, b, s_r, c, s_c."""
    # TODO 2
    m, b, s_r, res = line_fit(c_std, ratio_std)
    c, s_c = conc_from_line(ratio_sample, c_std, ratio_std, m, b, s_r)
    return m, b, s_r, c, s_c


def main():
    g = read_csv(HERE / "gc_retention.csv")
    print("Retention indices (linear, temperature-programmed):")
    for col in ("DB-5", "DB-Wax"):
        sel = g["column"] == col
        alk = {int(p[1:]): t for p, t in zip(g["peak"][sel], g["t_min"][sel]) if p.startswith("C")}
        for p, t in zip(g["peak"][sel], g["t_min"][sel]):
            if not p.startswith("C"):
                print(f"   {col:6s} {p}: t = {t:6.3f} min  I = {retention_index(t, alk):6.0f}")
    print("NIST WebBook values for the two candidates:")
    for name, v in NIST_RI.items():
        print(f"   {name}: DB-5 {v['DB-5']}, DB-Wax {v['DB-Wax']}")

    d = read_csv(HERE / "sanitizer_gc_is.csv")
    std = d["type"] == "standard"
    c = d["ethanol_percent_v_v"][std]
    raw = d["area_ethanol"][std]
    ratio = d["area_ethanol"] / d["area_is"]
    m0, b0, s0, _ = line_fit(c, raw)
    print(f"Without the internal standard: area = {b0:.0f} + {m0:.0f} c,  s_r / mean = {100 * s0 / raw.mean():.1f} %")
    m, b, s_r, c_s, s_c = internal_standard_result(c, ratio[std], ratio[d["type"] == "sample_1to100"])
    print(f"With the internal standard:    ratio = {b:.4f} + {m:.4f} c,  s_r / mean = {100 * s_r / ratio[std].mean():.1f} %")
    print(f"   sample vial {c_s:.4f} +/- {s_c:.4f} % v/v, so the sanitizer holds {100 * c_s:.1f} +/- {100 * s_c:.1f} % v/v ethanol")

    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    ax[0].plot(c, raw, "o")
    ax[0].set(xlabel="ethanol (% v/v)", ylabel="ethanol peak area", title="Raw areas: injection scatter")
    ax[1].plot(c, ratio[std], "o")
    cc = np.linspace(0, 1.05, 20)
    ax[1].plot(cc, b + m * cc, "-")
    ax[1].set(xlabel="ethanol (% v/v)", ylabel="area ethanol / area 1-butanol", title="Internal standard")
    save(fig, "lesson04_gc.png")


if __name__ == "__main__":
    main()
