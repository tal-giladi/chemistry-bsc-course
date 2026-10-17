# Instructor notes — 31.2 Molecular mechanics and conformer search

- Objective: the learner writes the force-field energy terms, knows when MMFF94 or UFF fits, runs a relaxed xtb dihedral scan, runs a stochastic conformer search with duplicate removal and re-ranking, and computes Boltzmann populations with degeneracies.
- Likely confusion: rigid versus relaxed scans; why many minimisations give the same conformer; 1-based xtb atom numbers versus 0-based Python indices.
- Misconception: "the lowest-energy conformer is the major species." Pentane's tg family (g = 4) outweighs tt at 298 K. Second: "a better method always changes the ranking" (here MMFF94 and GFN2-xTB agree on the order but not the gaps).
- Analogy: a conformer search is surveying a mountain range with many valleys by dropping hikers at random points and letting each walk downhill; you count distinct valleys, not hikers.
- Expected hands-on result (RDKit 2026.9.1, xtb 6.7.1pre): butane GFN2-xTB gauche 2.5, eclipsed CH3/H 10.7, syn 20.7 kJ/mol (MMFF94 3.5/16.6/21.8; OpenStax 3.8/16/19). Pentane MMFF94 tt 0, tg 3.47, g+g+ 5.95, g+g− 15.48; GFN2-xTB 0, 2.40, 4.93, 10.16 kJ/mol; populations 46.1/45.4/8.3/0.2 % and 35.4/53.8/9.7/1.2 %. Run time about 10 s.
- Extension: extend the search to n-hexane (three backbone dihedrals, 10 conformer classes) and check the number of unique conformers against $3^n$ with symmetry; or run CREST on Linux/WSL and compare with the ETKDG funnel.
