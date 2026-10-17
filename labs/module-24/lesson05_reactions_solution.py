"""Lesson 24.5 - amounts and failure budgets for the SN2, Grignard and aldol teaching syntheses.

Reference solution for lesson05_reactions.py.  Run:  py lesson05_reactions_solution.py
Densities at 20 C from PubChem (retrieved 2026-10-17). Quantities are typical teaching-lab scale and are
used only in the virtual bench; none of these reactions is to be run at home.
"""
from org24 import molar_mass

DENSITY = {"1-butanol": 0.8098, "bromobenzene": 1.4952, "acetone": 0.7845, "benzaldehyde": 1.046,
           "1-bromobutane": 1.2686}


def mmol_from_mL(volume_mL, name):
    """Amount in mmol of a liquid measured by volume."""
    # TODO: mass = volume * density; return 1000 * mass / molar_mass(name)
    return 1000 * volume_mL * DENSITY[name] / molar_mass(name)


def mmol_from_g(mass_g, name):
    # TODO: return 1000 * mass_g / molar_mass(name)
    return 1000 * mass_g / molar_mass(name)


def theoretical_g(reagents, product):
    """reagents: list of (mmol available, mmol needed per mmol product). Returns grams of product
    from the limiting reagent."""
    # TODO: n_product = min(n / per for n, per in reagents); return n_product * M(product) / 1000
    n_product = min(n / per for n, per in reagents)
    return n_product * molar_mass(product) / 1000


def water_that_destroys(mmol_grignard, fraction):
    """mg of water that protonates a given fraction of a Grignard reagent (1:1, RMgBr + H2O -> RH + Mg(OH)Br)."""
    # TODO: return fraction * mmol_grignard * molar_mass("water")
    return fraction * mmol_grignard * molar_mass("water")


def main():
    if mmol_from_mL(1, "acetone") is None or mmol_from_g(1, "water") is None \
            or theoretical_g([(1, 1)], "water") is None or water_that_destroys(1, 0.1) is None:
        print("TODO: write mmol_from_mL(), mmol_from_g(), theoretical_g() and water_that_destroys() first.")
        return

    # SN2: 1-butanol + NaBr + H2SO4 -> 1-bromobutane
    bu = mmol_from_mL(10.0, "1-butanol")
    nabr = mmol_from_g(13.0, "sodium bromide")
    theo = theoretical_g([(bu, 1), (nabr, 1)], "1-bromobutane")
    print(f"SN2: 1-butanol {bu:.0f} mmol, NaBr {nabr:.0f} mmol -> theoretical {theo:.2f} g 1-bromobutane "
          f"({theo / DENSITY['1-bromobutane']:.1f} mL); 10.5 g isolated = {100 * 10.5 / theo:.0f} %")

    # Grignard: PhBr + Mg -> PhMgBr; + benzophenone -> triphenylmethanol (after acid work-up)
    phbr = mmol_from_mL(2.2, "bromobenzene")
    mg = mmol_from_g(0.50, "magnesium")
    ketone = mmol_from_g(3.64, "benzophenone")
    grig = min(phbr, mg)
    theo = theoretical_g([(grig, 1), (ketone, 1)], "triphenylmethanol")
    print(f"Grignard: PhBr {phbr:.1f} mmol, Mg {mg:.1f} mmol, benzophenone {ketone:.1f} mmol "
          f"-> theoretical {theo:.2f} g triphenylmethanol")
    for f in (0.05, 0.10, 0.50):
        print(f"   {water_that_destroys(grig, f):5.0f} mg of water destroys {100 * f:.0f} % of the Grignard reagent")

    # Aldol (Claisen-Schmidt): 2 PhCHO + acetone -> dibenzalacetone + 2 H2O
    ald = mmol_from_mL(2.0, "benzaldehyde")
    ace = mmol_from_mL(0.73, "acetone")
    theo = theoretical_g([(ald, 2), (ace, 1)], "dibenzalacetone")
    print(f"Aldol: benzaldehyde {ald:.1f} mmol, acetone {ace:.1f} mmol (ratio {ald / ace:.2f}) "
          f"-> theoretical {theo:.2f} g dibenzalacetone")


if __name__ == "__main__":
    main()
