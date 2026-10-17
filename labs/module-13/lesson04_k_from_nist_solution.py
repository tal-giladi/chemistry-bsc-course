"""Lesson 13.4 reference solution: the equilibrium constant of ammonia synthesis from NIST data.

    py lesson04_k_from_nist_solution.py

Compares K(T) from (a) constant Delta H and Delta S (Module 8), (b) full NIST heat capacities, and
(c) the NIST-JANAF log Kf values in janaf_check.csv; then finds the ideal-gas equilibrium NH3 mole
fraction for a 1:3 N2:H2 feed at several pressures. Writes runs/lesson04_lnK.png.
"""
import csv
import math
from pathlib import Path

from scipy.optimize import brentq

from thermo13 import R, T0, reaction_h, reaction_k, reaction_s

HERE = Path(__file__).resolve().parent
NH3_SYNTHESIS = {"N2(g)": -1, "H2(g)": -3, "NH3(g)": 2}
P_STD = 1.0  # bar


def k_constant_dh_ds(dh298_kj, ds298_j, t):
    """K from Delta G(T) = Delta H(298) - T Delta S(298): the Module 8 approximation."""
    return math.exp(-(dh298_kj * 1000 - t * ds298_j) / (R * t))


def delta_g_actual(dg0_kj, t, q):
    """Delta_r G (kJ/mol) of a mixture with reaction quotient Q: Delta G0 + RT ln Q."""
    return dg0_kj + R * t * math.log(q) / 1000


def nh3_mole_fraction(k, p_bar):
    """Equilibrium NH3 mole fraction for a 1 N2 : 3 H2 feed at total pressure p (ideal gases).
    Extent xi: N2 1-xi, H2 3-3xi, NH3 2xi, total 4-2xi. Solve K = y_NH3^2 / (y_N2 y_H2^3) (p0/p)^2."""
    def f(xi):
        tot = 4 - 2 * xi
        y_n2, y_h2, y_nh3 = (1 - xi) / tot, (3 - 3 * xi) / tot, 2 * xi / tot
        return math.log(y_nh3**2 / (y_n2 * y_h2**3) * (P_STD / p_bar) ** 2) - math.log(k)
    xi = brentq(f, 1e-12, 1 - 1e-12)
    return 2 * xi / (4 - 2 * xi)


def janaf_nh3():
    out = {}
    with open(HERE / "janaf_check.csv", newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["species"] == "NH3(g)":
                out[float(r["T_K"])] = 10 ** (2 * float(r["log10_Kf"]))   # 2 mol NH3 per reaction
    return out


def _missing():
    """Names of the exercise functions that still return None (TODO)."""
    tests = {
        "k_constant_dh_ds": lambda: k_constant_dh_ds(-91.9, -198.1, 298.15),
        "delta_g_actual": lambda: delta_g_actual(-10.0, 298.15, 2.0),
        "nh3_mole_fraction": lambda: nh3_mole_fraction(1e-4, 200.0),
    }
    return [name for name, f in tests.items() if f() is None]


def main():
    missing = _missing()
    if missing:
        print("TODO: write " + ", ".join(f"{m}()" for m in missing) + " first (see the lesson).")
        return
    dh298 = reaction_h(NH3_SYNTHESIS, T0)
    ds298 = reaction_s(NH3_SYNTHESIS, T0)
    janaf = janaf_nh3()
    print(f"N2 + 3 H2 -> 2 NH3: Delta H(298) = {dh298:.2f} kJ/mol, Delta S(298) = {ds298:.2f} J/(mol K)")
    print(f"{'T (K)':>7}{'K const dH,dS':>15}{'K NIST Cp(T)':>14}{'K JANAF':>11}{'ratio':>8}")
    temps = [298.15, 400, 500, 600, 700, 800]
    rows = []
    for t in temps:
        k_c = k_constant_dh_ds(dh298, ds298, t)
        k_f = reaction_k(NH3_SYNTHESIS, t)
        k_j = janaf.get(float(t))
        print(f"{t:7.1f}{k_c:15.3g}{k_f:14.3g}{k_j:11.3g}{k_c / k_f:8.2f}")
        rows.append((t, k_c, k_f, k_j))

    print("\nWhich way does a reactor mixture go? 700 K, partial pressures N2 50, H2 150, NH3 10 bar")
    q = (10 / P_STD) ** 2 / ((50 / P_STD) * (150 / P_STD) ** 3)
    dg0 = -R * 700 * math.log(reaction_k(NH3_SYNTHESIS, 700)) / 1000
    dg = delta_g_actual(dg0, 700, q)
    print(f"  Q = {q:.3g}, Delta G0 = {dg0:+.1f} kJ/mol, Delta G = {dg:+.1f} kJ/mol ->",
          "forms NH3" if dg < 0 else "NH3 decomposes")

    print("\nEquilibrium NH3 mole fraction, 1:3 feed, ideal gases")
    print(f"{'p (bar)':>8}" + "".join(f"{t:>9.0f} K" for t in (500, 600, 700, 800)))
    for p in (1, 50, 100, 200, 300):
        print(f"{p:8.0f}" + "".join(f"{nh3_mole_fraction(reaction_k(NH3_SYNTHESIS, t), p):11.3f}"
                                    for t in (500, 600, 700, 800)))

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return
    fig, ax = plt.subplots(figsize=(5.5, 4))
    inv = [1000 / r[0] for r in rows]
    ax.plot(inv, [math.log(r[1]) for r in rows], "--", label="constant Delta H, Delta S")
    ax.plot(inv, [math.log(r[2]) for r in rows], "-", label="NIST Cp(T)")
    ax.plot(inv, [math.log(r[3]) for r in rows], "o", label="JANAF log Kf")
    ax.set_xlabel("1000 K / T")
    ax.set_ylabel("ln K")
    ax.set_title("van 't Hoff plot, N2 + 3 H2 -> 2 NH3")
    ax.legend()
    out = HERE / "runs"
    out.mkdir(exist_ok=True)
    fig.tight_layout()
    fig.savefig(out / "lesson04_lnK.png", dpi=120)
    print(f"plot written to {out / 'lesson04_lnK.png'}")


if __name__ == "__main__":
    main()
