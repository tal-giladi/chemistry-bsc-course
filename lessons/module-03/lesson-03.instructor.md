# Instructor notes — 03.3 First-order differential equations and rate laws

- Objective: the learner treats a rate law as an ODE, solves orders 0/1/2 by separation, picks the order from data, and runs and judges a numerical solver.
- Likely confusion: "first-order ODE" (only dc/dt appears) versus "first-order reaction" (n = 1). A second-order reaction is still a first-order ODE.
- Misconception: "A higher R² always wins." Show the residual pattern of the wrong order (systematic curve) versus the right one (scatter that grows at low c in 1/c).
- Analogy: Euler is driving with your eyes closed between glances at the speedometer; shorter glances (smaller h) keep you on the road, and too long a gap sends you off it (instability, hk > 2).
- Expected hands-on result: Euler error at 300 s 4.76e-3 → 2.73e-4 mol/L, ratios 2.10, 2.05, 2.02, 2.01; solve_ivp error ~1e-10 in 16 steps; R² 0.734, 0.927, 0.995; k ≈ 0.528 L/(mol s) (model 0.54).
- Extension: implement Heun's method (average of two slopes) and show the error ratio becomes about 4 (second order); fit the order-test data with weights 1/c² to remove the noise bias.
