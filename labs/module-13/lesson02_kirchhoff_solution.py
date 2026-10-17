"""Lesson 13.2 reference solution: bomb calorimetry and Kirchhoff's law with NIST heat capacities.

    py lesson02_kirchhoff_solution.py

Data: nist_shomate.csv through thermo13.py (NIST WebBook Shomate fits; CODATA dHf298).
Benzoic acid: NIST SRM 39j certified energy of combustion 26.434 kJ/g (certificate conditions).
Writes runs/lesson02_dH_vs_T.png.
"""
from pathlib import Path

from scipy.integrate import quad

from thermo13 import R, T0, cp, reaction_h

HERE = Path(__file__).resolve().parent

# ---- bomb calorimeter run (edit with your own simulation numbers) ----
BENZOIC_KJ_PER_G = 26.434   # NIST SRM 39j
M_STD_G, DT_STD_K = 0.9862, 2.395          # calibration: benzoic acid mass and corrected rise
M_SAMPLE_G, DT_SAMPLE_K = 1.2034, 1.823    # sample: sucrose
M_SUCROSE = 342.30                          # g/mol, C12H22O11
DN_GAS_SUCROSE = 12 - 12                    # C12H22O11(s) + 12 O2 -> 12 CO2 + 11 H2O(l)

NH3_SYNTHESIS = {"N2(g)": -1, "H2(g)": -3, "NH3(g)": 2}


def calorimeter_constant(m_std_g, kj_per_g, dt_k):
    """Heat capacity of the whole bomb calorimeter (kJ/K) from a standard of known energy."""
    return m_std_g * kj_per_g / dt_k


def delta_h_from_delta_u(du_kj_mol, dn_gas, t=T0):
    """Delta H = Delta U + Delta n_gas R T (ideal gases), kJ/mol."""
    return du_kj_mol + dn_gas * R * t / 1000


def delta_cp(reaction, t):
    """Delta_r Cp (J/(mol K)) = sum of nu * Cp at temperature t."""
    return sum(nu * cp(sp, t) for sp, nu in reaction.items())


def kirchhoff_integrated(dh298_kj, reaction, t):
    """Delta_r H(T) = Delta_r H(298.15) + integral of Delta_r Cp dT from 298.15 K to T (kJ/mol)."""
    integral, _ = quad(lambda x: delta_cp(reaction, x), T0, t)
    return dh298_kj + integral / 1000


def _missing():
    """Names of the exercise functions that still return None (TODO)."""
    tests = {
        "calorimeter_constant": lambda: calorimeter_constant(1.0, 26.434, 2.4),
        "delta_h_from_delta_u": lambda: delta_h_from_delta_u(-3228.0, -0.5),
        "kirchhoff_integrated": lambda: kirchhoff_integrated(-91.88, NH3_SYNTHESIS, 400.0),
    }
    return [name for name, f in tests.items() if f() is None]


def main():
    missing = _missing()
    if missing:
        print("TODO: write " + ", ".join(f"{m}()" for m in missing) + " first (see the lesson).")
        return
    print("Bomb calorimetry")
    c_cal = calorimeter_constant(M_STD_G, BENZOIC_KJ_PER_G, DT_STD_K)
    q = c_cal * DT_SAMPLE_K
    du = -q / M_SAMPLE_G * M_SUCROSE
    dh = delta_h_from_delta_u(du, DN_GAS_SUCROSE)
    print(f"  calorimeter constant C = {c_cal:.3f} kJ/K")
    print(f"  sample heat {q:.2f} kJ, {q / M_SAMPLE_G:.2f} kJ/g")
    print(f"  Delta_c U = {du:.0f} kJ/mol, Delta_c H = {dh:.0f} kJ/mol (NIST WebBook: -5644)")
    du_b = -BENZOIC_KJ_PER_G * 122.12
    print(f"  benzoic acid: Delta_c U = {du_b:.1f}, Delta_c H = {delta_h_from_delta_u(du_b, -0.5):.1f} kJ/mol"
          " (NIST WebBook average: -3228 +- 4)")

    print("\nHeat capacities from the NIST Shomate fits, J/(mol K)")
    print(f"{'T (K)':>7}" + "".join(f"{sp:>9}" for sp in NH3_SYNTHESIS) + f"{'dCp':>9}")
    for t in (298.15, 400, 500, 700, 1000):
        print(f"{t:7.1f}" + "".join(f"{cp(sp, t):9.2f}" for sp in NH3_SYNTHESIS)
              + f"{delta_cp(NH3_SYNTHESIS, t):9.2f}")
    print(f"  for comparison 7/2 R = {3.5 * R:.2f} (rigid diatomic), 4 R = {4 * R:.2f} (rigid non-linear)")

    dh298 = reaction_h(NH3_SYNTHESIS, T0)
    dcp298 = delta_cp(NH3_SYNTHESIS, T0)
    print(f"\nN2 + 3 H2 -> 2 NH3: Delta_r H(298) = {dh298:.2f} kJ/mol, Delta_r Cp(298) = {dcp298:.2f} J/(mol K)")
    print(f"{'T (K)':>7}{'constant dH':>13}{'const dCp':>11}{'integrated':>12}{'Shomate H':>11}")
    temps, rows = [], []
    for t in (298.15, 400, 500, 600, 700, 800, 1000):
        const_dcp = dh298 + dcp298 * (t - T0) / 1000
        integ = kirchhoff_integrated(dh298, NH3_SYNTHESIS, t)
        direct = reaction_h(NH3_SYNTHESIS, t)
        print(f"{t:7.1f}{dh298:13.2f}{const_dcp:11.2f}{integ:12.2f}{direct:11.2f}")
        temps.append(t)
        rows.append((const_dcp, integ))

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return
    fig, ax = plt.subplots(figsize=(5.5, 4))
    ax.axhline(dh298, color="grey", ls=":", label="constant Delta H (Module 8)")
    ax.plot(temps, [r[0] for r in rows], "--", label="constant Delta Cp")
    ax.plot(temps, [r[1] for r in rows], "o-", label="Kirchhoff with Cp(T)")
    ax.set_xlabel("T (K)")
    ax.set_ylabel("Delta_r H (kJ/mol)")
    ax.set_title("N2 + 3 H2 -> 2 NH3")
    ax.legend()
    out = HERE / "runs"
    out.mkdir(exist_ok=True)
    fig.tight_layout()
    fig.savefig(out / "lesson02_dH_vs_T.png", dpi=120)
    print(f"plot written to {out / 'lesson02_dH_vs_T.png'}")


if __name__ == "__main__":
    main()
