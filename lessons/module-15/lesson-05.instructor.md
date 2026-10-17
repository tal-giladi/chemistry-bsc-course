# Instructor notes — 15.5 Nucleophilic substitution: SN1 and SN2

- Objective: the learner writes SN2 and SN1 mechanisms with arrows, rate laws and stereochemistry; predicts the mechanism from substrate, nucleophile, leaving group and solvent; assigns the mechanism from the order in nucleophile; draws rearranged SN1 products.
- Likely confusion: "unimolecular/bimolecular" versus "first/second order"; why polar aprotic solvents speed SN2; why the R/S letter does not always flip on inversion; the role of the rate-determining step.
- Misconception: "tertiary halides do SN2 slowly" (they essentially do not); "a stronger nucleophile speeds SN1"; "HO⁻ can be a leaving group".
- Analogy: SN2 is a revolving door, one person enters as the other leaves; SN1 is a waiting room, the first person leaves, then anyone nearby can take the seat from either side.
- Expected hands-on result: A rates 7.7e−6 and 1.59e−5 mol L⁻¹ s⁻¹, order 1.04 (SN2); B 1.285e−5 and 1.279e−5, order −0.01 (SN1). True A run-1 rate 1.0e−5; five-point fit underestimates by 23 % because of curvature. RDKit: (S)-2-bromobutane → (R)-butan-2-ol. Drills: 1-azidopropane SN2; 3-methoxy-3-methylhexane near-racemic SN1; iodide exchange racemises at twice the exchange rate; methyl shift gives 2-bromo-2,3-dimethylbutane; protonation turns OH into a leaving group.
- Extension: fit the full curves of `sn_runs.csv` with the integrated rate laws (first order for B; mixed second order for A) using scipy `curve_fit` (Module 5), and compare the fitted k with the values in `make_data.py`.
