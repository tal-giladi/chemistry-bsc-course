"""Lesson 15.6: enumerate E2 products and rank them with NIST enthalpies of formation.

Fill in the two functions marked TODO, then run (from this folder):
    py lesson06_elimination.py
Reference solution: lesson06_elimination_solution.py
"""
import math

from org15 import R_KJ, canon, need_rdkit, read_csv

need_rdkit()
from rdkit import Chem  # noqa: E402
from rdkit.Chem import AllChem  # noqa: E402
from rdkit.Chem.EnumerateStereoisomers import EnumerateStereoisomers  # noqa: E402

# Beta-elimination: remove H from carbon 1 and the halogen from the neighbouring carbon 2, make C1=C2.
E2 = AllChem.ReactionFromSmarts("[C;!H0:1]-[C:2]-[Cl,Br,I:3]>>[C:1]=[C:2].[*:3]")

NIST = {canon(r["smiles"]): (r["name"], float(r["dfH_kJ_mol"])) for r in read_csv("butenes_nist.csv")}


def alkene_products(substrate_smiles):
    """All distinct alkenes (with E/Z where it exists) from beta-elimination of one HX."""
    mol = Chem.MolFromSmiles(substrate_smiles)
    flat = set()
    for prods in E2.RunReactants((mol,)):
        p = prods[0]
        Chem.SanitizeMol(p)
        flat.add(Chem.MolToSmiles(p))
    out = set()
    for smi in flat:
        for iso in EnumerateStereoisomers(Chem.MolFromSmiles(smi)):
            out.add(Chem.MolToSmiles(iso))
    return sorted(out)


def substitution_degree(smiles):
    """Number of carbon substituents on the two C=C carbons (1 = monosubstituted ... 4 = tetrasubstituted)."""
    mol = Chem.MolFromSmiles(smiles)
    patt = Chem.MolFromSmarts("[C:1]=[C:2]")
    a, b = mol.GetSubstructMatch(patt)
    # TODO: for each of the two alkene carbons a and b, count its carbon neighbours other than
    # the partner carbon (mol.GetAtomWithIdx(i).GetNeighbors(), n.GetSymbol(), n.GetIdx()). Return the sum.
    return None


def equilibrium_fractions(dfh_list, T=298.15):
    """Fractions of isomers at equilibrium if only the enthalpy differs: x_i proportional to exp(-dfH_i/RT).
    (Entropy differences between these isomers are small but not zero; this is an estimate.)"""
    # TODO: weights w_i = exp(-dfH_i / RT) (R_KJ in kJ/(mol K)); return the list w_i / sum(w).
    return None


def main():
    if substitution_degree("CC=C") is None or equilibrium_fractions([0.0, 0.0]) is None:
        raise SystemExit("TODO: write substitution_degree() and equilibrium_fractions() first.")
    for name, smi in [("2-bromobutane", "CC(Br)CC"), ("2-bromo-2-methylpropane", "CC(C)(C)Br"),
                      ("1-bromobutane", "BrCCCC")]:
        prods = alkene_products(smi)
        print(f"\n{name} ({smi}) -> {len(prods)} alkene(s)")
        known = [(p, NIST.get(p)) for p in prods]
        hs = [k[1] for _, k in known if k]
        fr = equilibrium_fractions(hs) if len(hs) == len(known) else None
        for i, (p, k) in enumerate(known):
            label = f"{k[0]:<16} dfH = {k[1]:6.2f} kJ/mol" if k else "(no NIST value in the table)"
            extra = f"  equilibrium share {100 * fr[i]:5.1f} %" if fr else ""
            print(f"  {p:<12} substituents on C=C: {substitution_degree(p)}  {label}{extra}")
    print("\nOpenStax 11.7, 2-bromobutane + NaOEt in ethanol: 81 % 2-butene, 19 % 1-butene (kinetic, not equilibrium).")


if __name__ == "__main__":
    main()
