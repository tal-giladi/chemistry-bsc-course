# Instructor notes — 23.3 Equilibrium constant by spectrophotometry

- Objective: the learner designs standards (excess Fe³⁺) and mixtures (comparable concentrations), computes K per mixture with an ICE table after dilution, corrects εb for incomplete complexation by iteration, and judges the model from spread, trend and a Job plot.
- Likely confusion: why the standards and the mixtures need different concentration regimes; that "initial" means after mixing; why ionic strength matters to a "constant".
- Misconception: "more precise readings fix everything". The incomplete-complexation bias (4–5 %) is larger than the random error (2 %), and no number of repeats removes it.
- Analogy: calibrating with standards that are 97 % complexed is like weighing flour on a scale that always reads 3 % low; every later number inherits it.
- Expected hands-on result: example data εb apparent 4432, corrected 4590 L/mol (96.6 % complexed); naive K 143–151, corrected K = 140, SD 3, 95 % CI ± 3, drift −2; Job maximum at 0.5. Pencil: K = 118; 0.020 M Fe standards → K about 45 % high; trend from Fe(SCN)₂⁺.
- Extension: fit K and εb together by nonlinear least squares over standards and mixtures at once (scipy.optimize.curve_fit) and compare with the iterative result; or measure K at two temperatures in the simulation and estimate ΔrH° with van 't Hoff (lesson 13.6).
