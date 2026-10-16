# Instructor notes — 05.3 Fitting models to data with uncertainty

- Objective: parameter ± uncertainty from `curve_fit`; correct use of `absolute_sigma`; weighted nonlinear fit; residuals and reduced chi-square; propagation to an unknown with correlations kept. This is plan 1.7's "fit a straight line and report the error".
- Likely confusion: `absolute_sigma`. Frame it as "who sets the noise scale: you, or the residuals?"
- Misconception: "R² = 0.999 means the model is right." Show a curved residual plot with R² = 0.998 (the sucrose densities in 05.5 do exactly this).
- Analogy: slope and intercept are a see-saw pivoting on the centre of the data; tilt it and one end goes up while the other goes down — that is the negative correlation.
- Expected hands-on result: m = 0.10551 ± 0.00071 L/µmol, b = 0.0018 ± 0.0032, r(m,b) = −0.78, s_r = 0.0049; unknown 3.700 ± 0.033 µmol/L (independent: ±0.047). Weighted k = 0.02354 ± 0.00062 1/min, χ²_ν = 0.69, half-life 29.4 min; Monte Carlo spread weighted 0.00059, unweighted 0.00096 (quoted 0.00041); lmfit identical to weighted curve_fit.
- Watch for: forgetting `p0` in the decay fit; learners passing `sigma` but leaving `absolute_sigma=False`.
- Extension: fit the sugar densities from Module 1 with a straight line and a quadratic; compare residual plots and decide (previews 05.5).
