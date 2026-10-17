"""Lesson 16.7 module practical: check multi-step routes with the Module 16 reaction library.

Run (from this folder):
    py lesson07_practical.py                        # check every routes/route_*.txt that has steps
    py lesson07_practical.py routes/route_P1.txt    # check one route file
    py lesson07_practical.py --list                 # list the targets and every reaction with its reagents

A route file has one step per line:  step; reaction; reactant SMILES joined by '.'; product SMILES
Every reactant must be in starting_materials.csv or made in an earlier step of the same file.
The checker is a teaching model: it knows the kind of change each reagent makes, aromatic directing
effects and a few classic incompatibilities. It does not know yields, rates, solvents or side products."""
import sys
from pathlib import Path

from org16 import HERE, REACTIONS, canon, catalogue, check_route, read_route

TARGETS = {  # id: (name, SMILES, what the lesson asks)
    "EX": ("paracetamol", "CC(=O)Nc1ccc(O)cc1", "worked example in lesson 16.7 (already filled in)"),
    "W1": ("2-heptanone", "CCCCCC(C)=O", "warm-up: acetoacetic ester synthesis (lesson 16.4)"),
    "W2": ("2-phenylethyl acetate", "CC(=O)OCCc1ccccc1", "warm-up: honey/rose fragrance ester from bromobenzene"),
    "W3": ("4-bromobenzoic acid", "OC(=O)c1ccc(Br)cc1", "warm-up: order of events from toluene"),
    "P1": ("1-(3-nitrophenyl)ethan-1-ol", "CC(O)c1cccc([N+](=O)[O-])c1", "project target 1, from benzene"),
    "P2": ("2-methyl-4-phenylbutan-2-ol", "CC(C)(O)CCc1ccccc1", "project target 2, a fragrance alcohol"),
}
STEP_YIELD = 0.80  # an assumed yield per step, to show how quickly long routes lose material


def target_for(path):
    stem = Path(path).stem  # route_P1 -> P1
    tid = stem.split("_")[-1].upper()
    return tid if tid in TARGETS else None


def check_file(path, cat):
    tid = target_for(path)
    steps = read_route(path)
    if tid is None:
        print(f"{path}: name the file route_<ID>.txt with an ID from --list")
        return False
    name, smiles, _ = TARGETS[tid]
    print(f"\n{tid} {name} ({canon(smiles)}) <- {Path(path).name}")
    if not steps:
        print("  no steps yet: write your route in this file")
        return False
    ok = check_route(steps, smiles, cat)
    print(f"  if every step gave {100 * STEP_YIELD:.0f} %, the overall yield would be {100 * STEP_YIELD ** len(steps):.0f} %")
    return ok


def main():
    if "--list" in sys.argv:
        print("Targets:")
        for tid, (name, smi, what) in TARGETS.items():
            print(f"  {tid}: {name:30s} {canon(smi):32s} {what}")
        print("\nReactions in the library (name: reagents it stands for; number of reactants):")
        for name, rx in REACTIONS.items():
            print(f"  {name:20s} {rx['reagents']} ({rx['n']})")
        return
    cat = catalogue()
    files = sys.argv[1:] or sorted(str(p) for p in (HERE / "routes").glob("route_*.txt"))
    results = {f: check_file(f, cat) for f in files}
    passed = sum(results.values())
    print(f"\n{passed}/{len(results)} route file(s) pass")


if __name__ == "__main__":
    main()
