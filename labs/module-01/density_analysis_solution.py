"""Module 01 practical: density of water and sugar solutions (reference solution).

Reads a CSV of kitchen-scale weighings, calibrates the syringe with water,
and reports each density with a standard uncertainty and a comparison with
reference values.

Usage (from the repo root or this folder):
    python density_analysis_solution.py                 # uses my_data.csv if present, else example_data.csv
    python density_analysis_solution.py my_data.csv
    python density_analysis_solution.py my_data.csv --plot   # also saves density_plot.png

Needs only numpy (and matplotlib for --plot), pinned in labs/common/requirements.txt.
"""
import csv
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
SCALE_RESOLUTION_G = 1.0  # change to 0.1 if your scale shows 0.1 g steps


def water_density(t_celsius):
    """Density of air-free water in g/mL, CIPM formula (Tanaka et al., Metrologia 38, 301, 2001). Valid 0-40 C."""
    a1, a2, a3, a4, a5 = -3.983035, 301.797, 522528.9, 69.34881, 999.974950
    t = t_celsius
    rho_kg_m3 = a5 * (1 - (t + a1) ** 2 * (t + a2) / (a3 * (t + a4)))
    return rho_kg_m3 / 1000.0


def load_reference():
    """Sucrose solution densities at 20 C (g/mL) from reference_sucrose_density.csv."""
    w, rho = [], []
    with open(HERE / "reference_sucrose_density.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            w.append(float(row["w_percent"]))
            rho.append(float(row["density_g_per_mL_20C"]))
    return np.array(w), np.array(rho)


def load_data(path):
    groups = {}
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            key = (row["sample"], float(row["w_percent"]))
            mass = float(row["cup_full_g"]) - float(row["cup_empty_g"])
            v_nominal = float(row["fills"]) * float(row["fill_volume_mL"])
            groups.setdefault(key, {"mass": [], "v": [], "t": []})
            groups[key]["mass"].append(mass)
            groups[key]["v"].append(v_nominal)
            groups[key]["t"].append(float(row["temp_C"]))
    return groups


def summarise(g):
    """Mean nominal density (mass / marked volume) and its standard uncertainty."""
    rho = np.array(g["mass"]) / np.array(g["v"])
    n = len(rho)
    mean = rho.mean()
    s = rho.std(ddof=1) if n > 1 else 0.0
    u_a = s / math.sqrt(n)                                  # Type A: spread of the repeats
    # Type B: scale resolution. Each mass is a difference of two readings, each with
    # a rectangular error of +/- d/2, so u = d/sqrt(12) per reading and d/sqrt(6) for the
    # difference. Cautious rule: do not divide this by sqrt(n).
    u_res = SCALE_RESOLUTION_G / math.sqrt(6) / np.mean(g["mass"]) * mean
    u = math.sqrt(u_a ** 2 + u_res ** 2)
    return n, mean, s, u, float(np.mean(g["t"]))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if args:
        path = Path(args[0])
    else:
        path = HERE / "my_data.csv" if (HERE / "my_data.csv").exists() else HERE / "example_data.csv"
    groups = load_data(path)
    if not groups:
        sys.exit(f"No data rows in {path}. Fill in your measurements first.")
    print(f"Data file: {path.name}   scale resolution: {SCALE_RESOLUTION_G} g\n")

    stats = {k: summarise(g) for k, g in groups.items()}

    # 1. Calibrate the syringe with water: f = true volume / marked volume.
    water = [k for k in stats if k[1] == 0]
    if not water:
        sys.exit("No water rows (w_percent = 0): the syringe cannot be calibrated.")
    n_w, rho_nom_w, _, u_nom_w, t_w = stats[water[0]]
    rho_w_true = water_density(t_w)
    f = rho_nom_w / rho_w_true
    u_f_rel = u_nom_w / rho_nom_w
    print(f"Water at {t_w:.1f} C: true density {rho_w_true:.5f} g/mL (CIPM formula)")
    print(f"Syringe calibration factor f = {f:.4f} +/- {f * u_f_rel:.4f}"
          f"  (5 fills deliver {100 * f:.1f} mL, not 100.0 mL)\n")

    # 2. Corrected densities, uncertainties, and comparison with the reference.
    w_ref, rho_ref_20 = load_reference()
    header = f"{'sample':<11}{'w/%':>5}{'n':>3}{'rho/(g/mL)':>12}{'u':>8}{'ref':>9}{'diff':>8}{'|z|':>6}  verdict"
    print(header)
    print("-" * len(header))
    results = []
    for (name, w), (n, rho_nom, s, u_nom, t) in sorted(stats.items(), key=lambda kv: kv[0][1]):
        rho = rho_nom / f
        u_rel = math.sqrt((u_nom / rho_nom) ** 2 + (u_f_rel if w != 0 else 0.0) ** 2)
        u = rho * u_rel
        # Reference at 20 C, shifted to the measurement temperature using water's change
        # (a good approximation for dilute sugar solutions).
        ref = float(np.interp(w, w_ref, rho_ref_20)) * water_density(t) / water_density(20.0)
        z = (rho - ref) / u
        verdict = "agrees" if abs(z) <= 2 else "check for a systematic error"
        if w == 0:
            verdict = "used for calibration"
        print(f"{name:<11}{w:>5.0f}{n:>3}{rho:>12.4f}{u:>8.4f}{ref:>9.4f}{rho - ref:>8.4f}{abs(z):>6.1f}  {verdict}")
        results.append((w, rho, u, ref))

    print("\nReport each value as rho = value +/- u (standard uncertainty), e.g. "
          f"{results[1][1]:.3f} +/- {results[1][2]:.3f} g/mL." if len(results) > 1 else "")

    if "--plot" in sys.argv:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        w, rho, u, ref = map(np.array, zip(*results))
        fig, ax = plt.subplots(figsize=(5, 3.5))
        ax.errorbar(w, rho, yerr=2 * u, fmt="o", capsize=3, label="measured (±2u)")
        ax.plot(w_ref, rho_ref_20, "-", label="reference, 20 °C")
        ax.set_xlabel("sugar mass fraction / %")
        ax.set_ylabel("density / (g/mL)")
        ax.legend()
        fig.tight_layout()
        out = HERE / "density_plot.png"
        fig.savefig(out, dpi=120)
        print(f"Saved {out.name}")


if __name__ == "__main__":
    main()
