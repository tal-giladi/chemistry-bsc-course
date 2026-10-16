# Instructor notes — 02.5 Several variables and partial derivatives (module practical)

- Objective: partials with explicit held-constant variables, total differential, quadrature error terms; then a full cooling-curve analysis that uses every Module 2 lesson.
- Likely confusion: the subscript notation (∂p/∂T)_V. Insist the learner says aloud what is held fixed.
- Misconception: "Independent errors add." They add in quadrature; straight addition is a worst case.
- Analogy: a mixing desk; each slider (input) changes the output by its own sensitivity, and the partial derivative is how far the sound moves per slider notch.
- Expected hands-on result (example data): k ≈ 6.68e-4 1/s (log fit) and 6.74e-4 1/s (rate plot), T0 ≈ 80.2 °C, integral of dT/dt = −45.8 °C, heat lost ≈ 47.9 kJ, mean power ≈ 20 W, T(60 min) = 28.2 ± 1.1 °C with T_env term 0.91 °C > k term 0.62 °C, drinkable after ≈ 10.9 min. Real mugs: time constant 15–40 min, early curvature from evaporation.
- Safety: hot water only, CAUTION box; no chemicals. The learner should not hold the probe over the mug.
- Extension: repeat with a lid or a glass instead of a ceramic mug and compare k; or fit the full model with scipy.optimize.curve_fit (Module 5 preview).
