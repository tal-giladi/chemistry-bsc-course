# Instructor notes — 03.5 Coupled systems: consecutive reactions

- Objective: the learner solves A → B → C by formula, by eigen-decomposition of the rate matrix and numerically, checks they agree, and fits k1 and k2 to data. This is the module practical.
- Likely confusion: why the matrix exponential is not "exponentiate each entry". Show the eigen route: each eigenvector evolves with its own e^(λt).
- Misconception: "The intermediate's curve tells you which step is slow." It does not if its scale is unknown (flip-flop); Part 3 of the lab shows it numerically.
- Analogy: two buckets in series, the top one draining into the bottom one, which drains onto the floor. The bottom bucket's level peaks when inflow equals outflow.
- Expected hands-on result: eigenvalues −0.15, −0.05, 0; formula vs eigen 2e-15, vs solve_ivp 7e-10 mM; B(20 min) = 4.7714 mM by formula and expm; fit k1 = 0.1468 ± 0.0016, k2 = 0.0501 ± 0.0003 1/min; t_max 11.1 min, B_max 5.82 mM; B-only fits k1/k2 = 0.158/0.049 (scale 0.96) and 0.049/0.158 (scale 3.10), both rms 0.095 mM.
- Extension: make the second step reversible (B ⇌ C) and repeat with the new rate matrix; or fit a published oral-dose plasma curve with the Bateman form and discuss flip-flop.
