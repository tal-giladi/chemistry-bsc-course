# Instructor notes — 09.3 Propagation of uncertainty

- **Objective:** write a measurement model; propagate with partial derivatives and the shortcuts (sums, products, powers, logs); build and read a budget; check with Monte Carlo.
- **Likely confusion:** when to add absolute and when relative uncertainties; the direction of the pH factors (0.434 from concentration to pH, 2.303 from pH to concentration; quiz q2).
- **Misconception:** "every source of error makes things worse, so a difference of two readings doubles the error". Correlated offsets cancel in differences (quiz q3).
- **Analogy:** the budget is a household budget: one big expense dominates, and cutting the coffee money (the balance) does nothing while the rent (the end point) stays.
- **Expected hands-on result:** good design 0.10048 ± 0.00018 mol/L (0.179 %), volume 97 % of the variance, all three methods agree; bad design first order 0.1250 ± 0.0188, Monte Carlo median 0.1250, mean 0.1281, interval [0.0967, 0.1771]. With `u_end = 0.01`: about 0.14 %. Pencil: 3.98 ± 0.18 × 10⁻⁸ mol/L; ρ = 1.0025 ± 0.0054 g/mL (volume 86 %); u(V) = 0.014 mL.
- **Extension:** redo the Lesson 07.7 salt standard budget by Monte Carlo and compare; or add a correlated pair (two masses on the same balance with a shared calibration error, r = 1) to the Monte Carlo by drawing one shared offset.
- **Scope:** expanded uncertainty and coverage factors are mentioned only; the full GUM reporting format comes back in Module 10's project.
