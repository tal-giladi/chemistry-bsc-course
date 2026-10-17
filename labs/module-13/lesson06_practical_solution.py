"""Lesson 13.6 reference solution (module practical): a thermodynamic data sheet.

    py lesson06_practical_solution.py                       # example freezing data
    py lesson06_practical_solution.py my_freezing.csv       # your data: sample,t_min,T_C

Part 1: the water-gas shift CO + H2O -> CO2 + H2 from NIST data, 500-1200 K: Delta H, Delta S,
        Delta G, K, checked against NIST-JANAF and against the Module 8 constant-Delta H estimate;
        equilibrium CO conversion for 1:1 and 1:3 CO:steam feeds.
Part 2: freezing point of salt water -> Kf from Delta_fus H, water activity, osmotic coefficient.
Writes runs/lesson06_practical.png.
"""
import csv
import math
import sys
from pathlib import Path

from scipy.optimize import brentq

from thermo13 import R, T0, dhf298, reaction_g, reaction_h, reaction_k, reaction_s, s298

HERE = Path(__file__).resolve().parent
WGS = {"CO(g)": -1, "H2O(g)": -1, "CO2(g)": 1, "H2(g)": 1}

# ---- setup: your freezing experiment ----
SALT_MOLALITY = 0.50        # mol NaCl per kg water (5.84 g NaCl in 200 g water)
NU = 2                      # ions per formula unit
DH_FUS = 6010.0             # J/mol, water (OpenStax Chemistry 2e 10.3)
TF_WATER = 273.15           # K, normal freezing point of water
M_WATER = 0.018015          # kg/mol


def kf_from_fusion(dh_fus, tf, m_solvent):
    """Cryoscopic constant (K kg/mol) of a solvent: Kf = R Tf^2 M / Delta_fus H."""
    return R * tf**2 * m_solvent / dh_fus


def water_activity(delta_tf, dh_fus=DH_FUS, tf=TF_WATER):
    """Activity of water in a solution freezing delta_tf kelvin below pure water:
    ln a = -(Delta_fus H / R)(1/T - 1/Tf*), with T = Tf* - delta_tf."""
    t = tf - delta_tf
    return math.exp(-dh_fus / R * (1 / t - 1 / tf))


def wgs_conversion(k, steam_ratio):
    """Fraction of CO converted at equilibrium for 1 mol CO and steam_ratio mol H2O.
    Equal gas moles on both sides, so K = x^2 / ((1 - x)(r - x)) and pressure cancels."""
    return brentq(lambda x: x * x - k * (1 - x) * (steam_ratio - x), 0.0, min(1.0, steam_ratio))


def freezing_point(temps):
    """Freezing temperature from a cooling curve: after supercooling the reading jumps up when ice
    forms. A salt solution then keeps cooling slowly (ice removes water, the rest gets saltier), so
    use only the start of the plateau: the mean of the first two readings after the jump."""
    for i in range(1, len(temps)):
        if temps[i] - temps[i - 1] > 0.5:
            return sum(temps[i:i + 2]) / len(temps[i:i + 2])
    return None


def read_freezing(path):
    data = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            data.setdefault(r["sample"], []).append(float(r["T_C"]))
    return data


def _missing():
    """Names of the exercise functions that still return None (TODO)."""
    tests = {
        "kf_from_fusion": lambda: kf_from_fusion(6010.0, 273.15, 0.018015),
        "water_activity": lambda: water_activity(1.0),
        "wgs_conversion": lambda: wgs_conversion(1.0, 1.0),
    }
    return [name for name, f in tests.items() if f() is None]


def janaf_k_wgs():
    lk = {}
    with open(HERE / "janaf_check.csv", newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            lk[(r["species"], float(r["T_K"]))] = float(r["log10_Kf"])
    out = {}
    for t in (500, 600, 700, 800, 900, 1000, 1100, 1200):
        try:
            out[t] = 10 ** (lk[("CO2(g)", t)] - lk[("CO(g)", t)] - lk[("H2O(g)", t)])
        except KeyError:
            pass
    return out


def main():
    missing = _missing()
    if missing:
        print("TODO: write " + ", ".join(f"{m}()" for m in missing) + " first (see the lesson).")
        return
    print("PART 1. Water-gas shift CO + H2O(g) -> CO2 + H2, standard state 1 bar")
    dh298 = sum(nu * dhf298(sp) for sp, nu in WGS.items())
    ds298 = sum(nu * s298(sp) for sp, nu in WGS.items())
    print(f"  298.15 K (CODATA): Delta H = {dh298:.2f} kJ/mol, Delta S = {ds298:.2f} J/(mol K),"
          f" Delta G = {dh298 - T0 * ds298 / 1000:.2f} kJ/mol")
    janaf = janaf_k_wgs()
    print(f"{'T K':>6}{'dH kJ':>9}{'dS J/K':>9}{'dG kJ':>9}{'K NIST':>10}{'K JANAF':>10}{'K const':>9}"
          f"{'x 1:1':>8}{'x 1:3':>8}")
    rows = []
    for t in (500, 600, 700, 800, 900, 1000, 1100, 1200):
        k = reaction_k(WGS, t)
        k_const = math.exp(-(dh298 * 1000 - t * ds298) / (R * t))
        x1, x3 = wgs_conversion(k, 1.0), wgs_conversion(k, 3.0)
        print(f"{t:6d}{reaction_h(WGS, t):9.2f}{reaction_s(WGS, t):9.2f}{reaction_g(WGS, t):9.2f}"
              f"{k:10.3g}{janaf[t]:10.3g}{k_const:9.3g}{x1:8.3f}{x3:8.3f}")
        rows.append((t, k, janaf[t], k_const, x1, x3))

    print("\nPART 2. Freezing point of salt water")
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "freezing_example.csv"
    data = read_freezing(path)
    tf_w = freezing_point(data["water"])
    salt_key = [k for k in data if k != "water"][0]
    tf_s = freezing_point(data[salt_key])
    dtf = tf_w - tf_s
    kf = kf_from_fusion(DH_FUS, TF_WATER, M_WATER)
    ideal = kf * NU * SALT_MOLALITY
    a_w = water_activity(dtf)
    x_w = (1 / M_WATER) / (1 / M_WATER + NU * SALT_MOLALITY)
    print(f"  readings: water freezes at {tf_w:.2f} C, {salt_key} at {tf_s:.2f} C"
          " (the thermometer offset cancels in the difference)")
    print(f"  Kf from Delta_fus H = {kf:.3f} K kg/mol (OpenStax table: 1.86)")
    print(f"  measured Delta Tf = {dtf:.2f} K; ideal = Kf nu m = {ideal:.2f} K")
    print(f"  osmotic coefficient phi = {dtf / ideal:.2f}  (1 = ideal)")
    print(f"  water activity a_w = {a_w:.4f}; ideal (Raoult) x_w = {x_w:.4f};"
          f" activity coefficient of water = {a_w / x_w:.4f}")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    ts = [r[0] for r in rows]
    ax1.semilogy(ts, [r[1] for r in rows], "-", label="NIST Cp(T)")
    ax1.semilogy(ts, [r[2] for r in rows], "o", label="JANAF")
    ax1.semilogy(ts, [r[3] for r in rows], "--", label="constant dH, dS (298 K)")
    ax1.set_xlabel("T (K)")
    ax1.set_ylabel("K")
    ax1.set_title("Water-gas shift")
    ax1.legend()
    for sample, temps in data.items():
        ax2.plot([2 * i for i in range(len(temps))], temps, ".-", label=sample)
    ax2.axhline(0, color="grey", lw=0.8)
    ax2.set_xlabel("t (min)")
    ax2.set_ylabel("T reading (C)")
    ax2.set_title("Freezing curves")
    ax2.legend()
    out = HERE / "runs"
    out.mkdir(exist_ok=True)
    fig.tight_layout()
    fig.savefig(out / "lesson06_practical.png", dpi=120)
    print(f"\nplot written to {out / 'lesson06_practical.png'}")


if __name__ == "__main__":
    main()
