"""Lesson 15.7 reference solution: the answer key of the Module 15 mechanism workbook.

    py lesson07_practical_solution.py            # prints every answer with its reasoning
    py lesson07_practical_solution.py --key      # prints the hashed key used by lesson07_practical.py

Each answer lists every acceptable SMILES. For a racemic product, both enantiomers are accepted:
a SMILES can only describe one molecule, and the flask contains both.
"""
import hashlib
import sys

from org15 import canon, need_rdkit

need_rdkit()
from rdkit import Chem  # noqa: E402

ANSWERS = {
    1: ("propene + HBr", ["CC(C)Br"],
        "Markovnikov: H+ adds to CH2, giving the secondary cation; Br- adds there. 2-bromopropane."),
    2: ("2-methylpropene + H2O, H2SO4 catalyst", ["CC(C)(C)O"],
        "Acid-catalysed hydration via the tertiary cation: tert-butyl alcohol."),
    3: ("cyclohexene + Br2 in CH2Cl2", ["Br[C@@H]1CCCC[C@H]1Br", "Br[C@H]1CCCC[C@@H]1Br"],
        "Bromonium ion, then backside attack by Br-: anti addition, racemic trans-1,2-dibromocyclohexane."),
    4: ("1-methylcyclohexene + BH3 in THF, then H2O2, NaOH", ["C[C@@H]1CCCC[C@H]1O", "C[C@H]1CCCC[C@@H]1O"],
        "Hydroboration: B to the less substituted carbon, H and B add syn; oxidation keeps the geometry. "
        "Racemic trans-2-methylcyclohexanol (anti-Markovnikov, syn)."),
    5: ("2-butyne + H2, Lindlar catalyst", ["C/C=C\\C"],
        "Syn addition of H2 on the poisoned catalyst stops at the alkene: (Z)-2-butene."),
    6: ("2-butyne + Na in liquid NH3", ["C/C=C/C"],
        "Dissolving-metal reduction through a radical anion gives the trans alkene: (E)-2-butene."),
    7: ("1-butyne + NaNH2, then CH3CH2Br", ["CCC#CCC"],
        "Amide (NH3 pKa 35) deprotonates the alkyne (pKa 25); the acetylide does SN2 on the primary bromide: 3-hexyne."),
    8: ("(R)-2-bromobutane + NaN3 in DMF", ["CC[C@H](C)N=[N+]=[N-]"],
        "SN2 with inversion; azide ranks first like Br did, so R becomes (S)-2-azidobutane."),
    9: ("2-bromo-2-methylbutane + potassium tert-butoxide", ["C=C(C)CC"],
        "E2 with a bulky base: Hofmann product, 2-methyl-1-butene."),
    10: ("2-methylcyclohexanol + H2SO4, heat", ["CC1=CCCCC1"],
         "E1 dehydration: secondary cation, loss of H+ towards the more substituted carbon (Zaitsev): 1-methylcyclohexene."),
}


def digest(smiles):
    return hashlib.sha256(smiles.encode("utf-8")).hexdigest()[:16]


def flat(smiles):
    return Chem.MolToSmiles(Chem.MolFromSmiles(smiles), isomericSmiles=False)


def main():
    if "--key" in sys.argv:
        print("KEY = {")
        for i, (_, smis, _) in ANSWERS.items():
            full = sorted({digest(canon(s)) for s in smis})
            print(f"    {i}: ({full!r}, {digest(flat(smis[0]))!r}),")
        print("}")
        return
    for i, (q, smis, why) in ANSWERS.items():
        print(f"{i:>2}. {q}\n    answer: {' or '.join(canon(s) for s in smis)}\n    {why}")


if __name__ == "__main__":
    main()
