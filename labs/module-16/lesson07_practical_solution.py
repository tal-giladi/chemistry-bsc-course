"""Lesson 16.7 reference solution: routes to every target, checked with the reaction library,
plus two deliberately wrong routes to show what the checker catches.

Run (from this folder):
    py lesson07_practical_solution.py
Other correct routes exist; the checker accepts any route whose steps are all valid."""
from lesson07_practical import TARGETS
from org16 import catalogue, check_route

SOLUTIONS = {
    "W1": [  # acetoacetic ester synthesis
        ("1", "enolate_alkylation", ["CCOC(=O)CC(C)=O", "CCCCBr"], "CCCCC(C(C)=O)C(=O)OCC"),
        ("2", "ester_hydrolysis", ["CCCCC(C(C)=O)C(=O)OCC"], "CCCCC(C(C)=O)C(=O)O"),
        ("3", "decarboxylate", ["CCCCC(C(C)=O)C(=O)O"], "CCCCCC(C)=O")],
    "W2": [  # Grignard + ethylene oxide adds CH2CH2OH; then acetylate
        ("1", "grignard", ["Brc1ccccc1", "C1CO1"], "OCCc1ccccc1"),
        ("2", "acylation", ["OCCc1ccccc1", "CC(=O)OC(C)=O"], "CC(=O)OCCc1ccccc1")],
    "W3": [  # brominate first (CH3 directs para), then oxidise CH3 to COOH
        ("1", "bromination_arene", ["Cc1ccccc1"], "Cc1ccc(Br)cc1"),
        ("2", "oxidise_strong", ["Cc1ccc(Br)cc1"], "OC(=O)c1ccc(Br)cc1")],
    "P1": [  # acyl first (Friedel-Crafts before any deactivator), nitrate meta, reduce C=O only
        ("1", "fc_acylation", ["c1ccccc1", "CC(=O)Cl"], "CC(=O)c1ccccc1"),
        ("2", "nitration", ["CC(=O)c1ccccc1"], "CC(=O)c1cccc([N+](=O)[O-])c1"),
        ("3", "reduce_nabh4", ["CC(=O)c1cccc([N+](=O)[O-])c1"], "CC(O)c1cccc([N+](=O)[O-])c1")],
    "P2": [  # Claisen-Schmidt, then C=C only, then Grignard
        ("1", "aldol_condensation", ["O=Cc1ccccc1", "CC(C)=O"], "CC(=O)C=Cc1ccccc1"),
        ("2", "hydrogenate_alkene", ["CC(=O)C=Cc1ccccc1"], "CC(=O)CCc1ccccc1"),
        ("3", "grignard", ["CBr", "CC(=O)CCc1ccccc1"], "CC(C)(O)CCc1ccccc1")],
}
ALTERNATIVES = {
    "P2 (three steps, all Grignard chemistry)": ("P2", [
        ("1", "grignard", ["Brc1ccccc1", "C1CO1"], "OCCc1ccccc1"),
        ("2", "pbr3", ["OCCc1ccccc1"], "BrCCc1ccccc1"),
        ("3", "grignard", ["BrCCc1ccccc1", "CC(C)=O"], "CC(C)(O)CCc1ccccc1")]),
}
WRONG = {
    "P1 with the nitration first (Friedel-Crafts on a deactivated ring)": ("P1", [
        ("1", "nitration", ["c1ccccc1"], "O=[N+]([O-])c1ccccc1"),
        ("2", "fc_acylation", ["O=[N+]([O-])c1ccccc1", "CC(=O)Cl"], "CC(=O)c1cccc([N+](=O)[O-])c1"),
        ("3", "reduce_nabh4", ["CC(=O)c1cccc([N+](=O)[O-])c1"], "CC(O)c1cccc([N+](=O)[O-])c1")]),
    "P1 with the reduction before the nitration (CH(OH)CH3 directs ortho/para)": ("P1", [
        ("1", "fc_acylation", ["c1ccccc1", "CC(=O)Cl"], "CC(=O)c1ccccc1"),
        ("2", "reduce_nabh4", ["CC(=O)c1ccccc1"], "CC(O)c1ccccc1"),
        ("3", "nitration", ["CC(O)c1ccccc1"], "CC(O)c1cccc([N+](=O)[O-])c1")]),
}


def main():
    cat = catalogue()
    print("Reference routes")
    for tid, steps in SOLUTIONS.items():
        print(f"\n{tid} {TARGETS[tid][0]}")
        check_route(steps, TARGETS[tid][1], cat)
    for label, (tid, steps) in ALTERNATIVES.items():
        print(f"\nAlternative: {label}")
        check_route(steps, TARGETS[tid][1], cat)
    print("\nDeliberately wrong routes (the checker should object)")
    for label, (tid, steps) in WRONG.items():
        print(f"\n{label}")
        check_route(steps, TARGETS[tid][1], cat)


if __name__ == "__main__":
    main()
