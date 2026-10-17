"""Lesson 08.1 hands-on, reaction enthalpies from formation enthalpies.

Fill in the two TODO functions, then run:
       py lesson01_hess.py
Reference solution: lesson01_hess_solution.py
Data:  thermo_data.csv (OpenStax Chemistry 2e Appendix G; NaHCO3(s) from NBS via Wikipedia).
"""
from thermo import load_table

C_WATER = 4.184   # J/(g K), specific heat of liquid water near 25 C

# A reaction is a dict {species: coefficient}; products positive, reactants negative.
REACTIONS = {
    "methane combustion":   {"CH4(g)": -1, "O2(g)": -2, "CO2(g)": 1, "H2O(l)": 2},
    "propane combustion":   {"C3H8(g)": -1, "O2(g)": -5, "CO2(g)": 3, "H2O(l)": 4},
    "ethanol combustion":   {"C2H5OH(l)": -1, "O2(g)": -3, "CO2(g)": 2, "H2O(l)": 3},
    "hydrogen combustion":  {"H2(g)": -1, "O2(g)": -0.5, "H2O(l)": 1},
    "NH4NO3 dissolving":    {"NH4NO3(s)": -1, "NH4+(aq)": 1, "NO3-(aq)": 1},
    "NaHCO3 dissolving":    {"NaHCO3(s)": -1, "Na+(aq)": 1, "HCO3-(aq)": 1},
}
FUELS = {"methane combustion": "CH4(g)", "propane combustion": "C3H8(g)",
         "ethanol combustion": "C2H5OH(l)", "hydrogen combustion": "H2(g)"}


def reaction_value(reaction, table, column="dHf_kJ_mol"):
    """Sum of coefficient x formation value: Delta_r H = sum(nu * Delta_f H), products minus reactants.
    TODO: loop over reaction.items() and add nu * table[species][column]."""
    return None


def delta_t(q_joule, mass_g, c=C_WATER):
    """Temperature change of the solution when the reaction RELEASES q (J): dT = q / (m c).
    A positive Delta H (endothermic) means q < 0 for the surroundings, so the water cools.
    TODO: one line."""
    return None


def main():
    table = load_table()
    if reaction_value({"H2(g)": 1}, table) is None or delta_t(1.0, 1.0) is None:
        print("TODO: write reaction_value() and delta_t() first.")
        return
    print(f"{'reaction':<22}{'Delta_r H (kJ/mol)':>20}")
    results = {}
    for name, rxn in REACTIONS.items():
        results[name] = reaction_value(rxn, table)
        print(f"{name:<22}{results[name]:>20.1f}")

    print("\nfuel energy (heat released per gram of fuel, liquid water formed):")
    for name, fuel in FUELS.items():
        per_g = -results[name] / table[fuel]["M_g_mol"]
        print(f"  {fuel:<11} {per_g:6.1f} kJ/g")

    # Hess check: C -> CO -> CO2 equals C -> CO2
    step1 = reaction_value({"C(graphite)": -1, "O2(g)": -0.5, "CO(g)": 1}, table)
    step2 = reaction_value({"CO(g)": -1, "O2(g)": -0.5, "CO2(g)": 1}, table)
    direct = reaction_value({"C(graphite)": -1, "O2(g)": -1, "CO2(g)": 1}, table)
    print(f"\nHess: C->CO {step1:.2f} + CO->CO2 {step2:.2f} = {step1 + step2:.2f} kJ; direct {direct:.2f} kJ")

    # Prediction for the lesson 08.7 practical: 5.00 g baking soda in 100.0 g water
    dh = results["NaHCO3 dissolving"]
    n = 5.00 / table["NaHCO3(s)"]["M_g_mol"]
    q_released = -dh * 1000 * n
    print(f"\n5.00 g NaHCO3 ({n:.4f} mol) in 100.0 g water: q released = {q_released:.0f} J")
    print(f"  predicted Delta T (cup heat capacity ignored) = {delta_t(q_released, 105.0):.2f} K")


if __name__ == "__main__":
    main()
