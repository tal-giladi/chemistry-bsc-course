"""Lesson 16.2 reference solution: hydrate equilibria and Grignard disconnections.

Run (from this folder):
    py lesson02_addition_solution.py
    py lesson02_addition_solution.py "CCC(C)(O)c1ccccc1"     # disconnect your own alcohol
"""
import sys

from org16 import Chem, attempt, canon, check_drill, check_step, mol

# Hydration constants K = [hydrate]/[carbonyl] in water (water's activity taken as 1).
# Orders of magnitude, as given by OpenStax Organic Chemistry 19.5 (formaldehyde 99.9 % hydrate,
# acetone 0.1 %) and the review values quoted for formaldehyde (~1e3) and hexafluoroacetone (~1e6);
# acetaldehyde is close to 1 (about half hydrated).
K_HYD = [("hexafluoroacetone", "O=C(C(F)(F)F)C(F)(F)F", 1e6), ("formaldehyde", "C=O", 1e3),
         ("acetaldehyde", "CC=O", 1.0), ("acetone", "CC(C)=O", 1e-3)]


def hydrate_percent(k):
    """Percentage of the carbonyl compound present as the hydrate at equilibrium."""
    # [your code]
    # TODO: K = hydrate/carbonyl, so the hydrate fraction is K/(1 + K). Return it as a percentage.
    return 100 * k / (1 + k)
    # [end of your code]


def grignard_disconnections(alcohol_smiles):
    """All (R-Br, carbonyl) pairs that give this secondary or tertiary alcohol by a Grignard addition.
    Break one C-C bond at the carbinol carbon: that carbon becomes C=O, the other piece becomes R-Br."""
    m = mol(alcohol_smiles)
    patt = Chem.MolFromSmarts("[CX4;!$(C(O)O)]([#6])[OX2H]")
    pairs = []
    for match in m.GetSubstructMatches(patt):
        carbinol, oxygen = match[0], match[2]
        for nb in m.GetAtomWithIdx(carbinol).GetNeighbors():
            if nb.GetSymbol() != "C":
                continue
            # [your code]
            # TODO: copy the molecule with Chem.RWMol(m); remove the bond carbinol-nb; make the C-O bond
            # TODO: double (SetBondType(Chem.BondType.DOUBLE)); add a Br atom bonded to nb; sanitize;
            # TODO: split the fragments with Chem.GetMolFrags(..., asMols=True) and sort them into
            # TODO: (halide, carbonyl) by which one contains Br. Append (halide SMILES, carbonyl SMILES).
            rw = Chem.RWMol(m)
            rw.RemoveBond(carbinol, nb.GetIdx())
            rw.GetBondBetweenAtoms(carbinol, oxygen).SetBondType(Chem.BondType.DOUBLE)
            br = rw.AddAtom(Chem.Atom(35))
            rw.AddBond(nb.GetIdx(), br, Chem.BondType.SINGLE)
            for a in rw.GetAtoms():
                a.SetNoImplicit(False)
                a.SetNumExplicitHs(0)
            Chem.SanitizeMol(rw)
            frags = Chem.GetMolFrags(rw.GetMol(), asMols=True)
            halide = next(f for f in frags if f.HasSubstructMatch(Chem.MolFromSmarts("Br")))
            carbonyl = next(f for f in frags if f is not halide)
            pairs.append((Chem.MolToSmiles(halide), Chem.MolToSmiles(carbonyl)))
            # [end of your code]
    return sorted(set(pairs))


# Product drill: main organic product as SMILES. Worked answers: lesson 16.2, Hands-on.
ANSWERS = {
    "a cyclohexanone + NaBH4, then water": "OC1CCCCC1",
    "b benzaldehyde + CH3CH2MgBr, then H3O+": "CCC(O)c1ccccc1",
    "c acetone + methylamine, acid catalyst, remove water": "CN=C(C)C",
    "d cyclohexanone + Ph3P=CH2": "C=C1CCCCC1",
    "e acetaldehyde + excess methanol, acid catalyst, remove water": "COC(C)OC",
}
KEYS = {
    "a cyclohexanone + NaBH4, then water": "e36b66a9146ed318",
    "b benzaldehyde + CH3CH2MgBr, then H3O+": "4eef64a2019ee3cf",
    "c acetone + methylamine, acid catalyst, remove water": "06178d45eb7f57e8",
    "d cyclohexanone + Ph3P=CH2": "558414c45da16376",
    "e acetaldehyde + excess methanol, acid catalyst, remove water": "2342647c04ddcf9a",
}


def main():
    print("Hydrate at equilibrium in water")
    for name, smi, k in K_HYD:
        p = attempt(hydrate_percent, k)
        shown = f"{p:9.4f} %" if p != "TODO" else "TODO"
        print(f"  {name:18s} K = {k:8.0e}  hydrate {shown}")

    target = sys.argv[1] if len(sys.argv) > 1 else "CCC(C)(O)c1ccccc1"  # 2-phenyl-2-butanol
    print(f"\nGrignard disconnections of {canon(target)}")
    pairs = attempt(grignard_disconnections, target, default=None)
    if pairs is None:
        print("  TODO: write grignard_disconnections()")
    for halide, carbonyl in pairs or []:
        ok, msgs = check_step("grignard", [halide, carbonyl], target)
        print(f"  {halide:14s} + {carbonyl:18s} {'checks' if ok else 'fails'} {'; '.join(msgs)}")
    print("\nProduct drill")
    check_drill(ANSWERS, KEYS)


if __name__ == "__main__":
    main()
