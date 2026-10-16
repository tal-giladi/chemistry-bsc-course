# Instructor notes — 03.1 Vectors, matrices and solving linear systems

- Objective: the learner turns a chemistry problem (atom balance, mixture absorbances) into $E\mathbf{c} = \mathbf{A}$ or $M\boldsymbol{\nu} = 0$, solves it, and checks whether the answer can be trusted.
- Likely confusion: why balancing has a zero right-hand side and still a non-zero answer. Stress that we want the null space, and that only the ratio of coefficients is fixed.
- Misconception: "Any two wavelengths work for a two-component mixture." Show the 425/450 nm pair in the lab: condition number about 330, negative c_Y.
- Analogy: two rows of a nearly singular matrix are like two people giving you directions from almost the same spot; triangulating from them puts the target anywhere along a long line.
- Expected hands-on result: 2 KMnO4 + 16 HCl → 2 KCl + 2 MnCl2 + 5 Cl2 + 8 H2O; peaks give c_X 2.70e-5, c_Y 3.49e-5 mol/L (cond 1.5); 425/450 nm gives c_Y −4.2e-5 (cond 333); least squares 2.69e-5 and 3.51e-5 mol/L, rms residual 0.0022.
- Extension: add a third column (a hypothetical dye Z) to the least-squares fit and see that its concentration comes out near zero with no change in residual; then corrupt one absorbance by 0.05 and watch the residual flag it.
