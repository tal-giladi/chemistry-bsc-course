"""Lesson 13.3 hands-on: entropy changes from heat capacities, and a state-function check.

Fill in the functions marked TODO, then run this file. Reference solution: lesson03_entropy_solution.py.

    py lesson03_entropy.py

Part 1: mixing hot and cold water (edit the setup block with your own kitchen numbers).
Part 2: entropy of heating liquid water, integrating the NIST Cp(T).
Part 3: two routes to the standard entropy of vaporisation of water at 298.15 K.
Data: thermo13.py (NIST/CODATA), NIST WebBook Antoine coefficients for water (273-303 K range).
"""
import math

from scipy.integrate import quad

from thermo13 import R, T0, cp, dhf298, s298

# ---- setup: your mixing experiment ----
M_HOT_G, T_HOT_C = 100.0, 60.0
M_COLD_G, T_COLD_C = 100.0, 20.0
T_FINAL_MEASURED_C = None        # put your measured final temperature here, e.g. 39.2
C_WATER = 4.184                  # J/(g K)

# NIST WebBook, water, Antoine equation log10(p/bar) = A - B/(T/K + C), 273-303 K (Bridgeman and Aldrich)
ANTOINE = (5.40221, 1838.675, -31.737)
P_STD = 1.0                      # bar


def ds_heating(cp_func, t1, t2):
    """Entropy change (J/(mol K)) for heating at constant p from t1 to t2: integral of Cp/T dT."""
    # TODO: integrate cp_func(t) / t from t1 to t2 with quad; return the value only
    return None


def ds_isothermal_ideal_gas(p1, p2, n=1.0):
    """Entropy change (J/K) of n mol of ideal gas taken isothermally from p1 to p2."""
    # TODO: one line; entropy falls when the gas is compressed
    return None


def mixing(m_hot, t_hot_k, m_cold, t_cold_k, c=C_WATER):
    """Final temperature (K) and entropy changes (J/K) of the hot water, cold water and total,
    for two water samples mixed in a perfectly insulated cup."""
    # TODO: heat lost by hot = heat gained by cold gives t_f; then m c ln(t_f / t) for each sample
    return None


def p_sat_water(t_k):
    a, b, c = ANTOINE
    return 10 ** (a - b / (t_k + c))


def _missing():
    """Names of the exercise functions that still return None (TODO)."""
    tests = {
        "ds_heating": lambda: ds_heating(lambda t: 75.0, 300.0, 350.0),
        "ds_isothermal_ideal_gas": lambda: ds_isothermal_ideal_gas(1.0, 2.0),
        "mixing": lambda: mixing(1.0, 330.0, 1.0, 290.0),
    }
    return [name for name, f in tests.items() if f() is None]


def main():
    missing = _missing()
    if missing:
        print("TODO: write " + ", ".join(f"{m}()" for m in missing) + " first (see the lesson).")
        return
    print("1. Mixing hot and cold water (perfect insulation)")
    t_f, dsh, dsc, dst = mixing(M_HOT_G, T_HOT_C + 273.15, M_COLD_G, T_COLD_C + 273.15)
    print(f"   final T = {t_f - 273.15:.2f} C; dS hot = {dsh:+.2f} J/K, dS cold = {dsc:+.2f} J/K,"
          f" total = {dst:+.2f} J/K")
    if T_FINAL_MEASURED_C is not None:
        loss = (M_HOT_G + M_COLD_G) * C_WATER * (t_f - 273.15 - T_FINAL_MEASURED_C)
        print(f"   measured final T = {T_FINAL_MEASURED_C:.1f} C: about {loss:.0f} J went into the cup and air")

    print("\n2. Heating liquid water at 1 bar, NIST Cp(T) of H2O(l)")
    for t2 in (323.15, 348.15, 373.15):
        ds = ds_heating(lambda t: cp("H2O(l)", t), T0, t2)
        approx = cp("H2O(l)", T0) * math.log(t2 / T0)
        print(f"   298.15 -> {t2:.2f} K: dS = {ds:6.3f} J/(mol K)   (constant Cp: {approx:6.3f})")

    print("\n3. Standard entropy of vaporisation of water at 298.15 K, two routes")
    table = s298("H2O(g)") - s298("H2O(l)")
    dh_vap = dhf298("H2O(g)") - dhf298("H2O(l)")          # kJ/mol
    p_sat = p_sat_water(T0)
    step1 = dh_vap * 1000 / T0                               # evaporate at p_sat (equilibrium)
    step2 = ds_isothermal_ideal_gas(p_sat, P_STD)            # compress vapour to 1 bar
    print(f"   route A, table:   S(g) - S(l) = {s298('H2O(g)'):.3f} - {s298('H2O(l)'):.2f} = {table:.2f} J/(mol K)")
    print(f"   route B, path:    p_sat(298.15 K) = {p_sat:.5f} bar (NIST Antoine)")
    print(f"                     evaporate at p_sat: dH/T = {dh_vap:.3f} kJ/mol / T = {step1:+.2f}")
    print(f"                     compress to 1 bar: -R ln(1/p_sat) = {step2:+.2f}")
    print(f"                     sum = {step1 + step2:.2f} J/(mol K)")
    print(f"   difference = {step1 + step2 - table:+.2f} J/(mol K): entropy is a state function")


if __name__ == "__main__":
    main()
