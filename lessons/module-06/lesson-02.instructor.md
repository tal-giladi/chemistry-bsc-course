# Instructor notes — 06.2 Proteins: from amino acids to folds

- Objective: net charge and pI from pKa values; peptide bond planarity; α-helix (i→i+4) and β-sheet patterns; reading UniProt/PDB entries; counting backbone H-bonds in Mol* and Python; marginal stability.
- Likely confusion: Henderson–Hasselbalch sign for basic versus acidic groups; "pI" versus "pKa".
- Misconception: "More hydrogen bonds means proportionally more stability." The unfolded chain hydrogen-bonds to water; folding gains the difference only.
- Analogy: changing seats at a crowded dinner — everyone still has a neighbour; what matters is whether the new arrangement is slightly better.
- Expected hands-on result: UniProt P0CG48, 685 residues, 9 ubiquitin repeats; PDB 1UBQ, X-ray, 1.8 Å, 1987, 76 residues. Script: net charge +0.23 at pH 7.0, +0.05 at 7.4, pI 7.54 (EMBOSS set); 47 H-bonds (12 i→i+4, 9 i→i+3, 26 others), helix bonds O22–N26 … O31–N35 (10), mean −9.0 kJ/mol, strongest −13.6. Mol* counts will differ slightly (different criterion). Extension 4HHB chain A: 110 bonds, 83 i→i+4 (75 %), pI 9.09.
- Safety: none (browser and Python only).
- Extension: mutate the logic — set the cutoff to −1.0 kcal/mol and see which bonds disappear first (the long, bent ones at helix ends); or compute the pI of the full 685-residue precursor from UniProt and compare with one repeat.
