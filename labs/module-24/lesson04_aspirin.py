"""Lesson 24.4 - the numbers of the aspirin synthesis: limiting reagent, yield, atom economy, purity.

Fill in the functions marked TODO, then run:  py lesson04_aspirin.py
Reference solution: lesson04_aspirin_solution.py
The three bench runs below are example outcomes of the kind the virtual bench produces; replace them
with your own runs from the organic-bench simulation (preset aspirin).
"""
from org24 import COMPOUNDS, molar_mass

AC2O_DENSITY = 1.082    # g/mL at 20 C (PubChem CID 7918)

# run name: (crude or final mass g, melting range low, high in C, iron(III) test violet?)
RUNS = {
    "A crude": (2.31, 128.0, 133.0, True),
    "A recrystallised": (1.92, 134.0, 136.0, False),
    "B (filtered, not dried)": (2.95, 118.0, 131.0, True),
}


def moles(mass_g, name):
    # TODO: return mass_g / molar_mass(name)
    return None


def limiting(n_salicylic, n_anhydride):
    """1:1 stoichiometry. Return the name of the limiting reagent and its amount in mol."""
    # TODO: compare the two amounts
    return None


def atom_economy(product, reactants):
    """Percent of the reactants' mass that ends up in the product: 100 M(product) / sum M(reactants)."""
    # TODO: 100 * molar_mass(product) / sum(molar_mass(r) for r in reactants)
    return None


def verdict(mass_g, theo_g, lo, hi, iron_violet, lit=COMPOUNDS["aspirin"][1]):
    """One-line judgement of a run from its yield, melting range and the iron(III) chloride test."""
    # TODO: flag yield > 100 % (wet or impure), a range wider than 2 C or ending more than 2 C below lit,
    #       and a violet iron(III) test (phenol OH of unreacted salicylic acid)
    return None


def main():
    if moles(1, "aspirin") is None or limiting(1, 2) is None or atom_economy("aspirin", ["aspirin"]) is None \
            or verdict(1, 2, 134, 135, False) is None:
        print("TODO: write moles(), limiting(), atom_economy() and verdict() first.")
        return
    n_sa = moles(2.00, "salicylic acid")
    n_ac = moles(5.0 * AC2O_DENSITY, "acetic anhydride")
    name, n = limiting(n_sa, n_ac)
    theo = n * molar_mass("aspirin")
    print(f"salicylic acid {n_sa * 1000:.2f} mmol, acetic anhydride {n_ac * 1000:.1f} mmol "
          f"({n_ac / n_sa:.1f} equivalents)")
    print(f"limiting reagent: {name}; theoretical yield {theo:.2f} g aspirin")
    print(f"atom economy: {atom_economy('aspirin', ['salicylic acid', 'acetic anhydride']):.1f} %")
    for run, (m, lo, hi, fe) in RUNS.items():
        print(f"  {run:24s} {m:.2f} g, mp {lo:.0f}-{hi:.0f} C: {verdict(m, theo, lo, hi, fe)}")


if __name__ == "__main__":
    main()
