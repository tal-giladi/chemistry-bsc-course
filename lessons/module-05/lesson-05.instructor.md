# Instructor notes — 05.5 Reproducible analysis notebooks (module practical)

- Objective: JupyterLab with no hidden state; raw data read-only, relative paths, seeds, version record; pass restart-and-run-all and `nbconvert --execute`; the plan 1.7 straight-line fit, extended to a model choice and an unknown with uncertainty.
- Likely confusion: why a notebook that "shows" a result is not proof of it. Demonstrate live: run a cell twice that does `x = x * 2`, then restart and run all.
- Misconception: "High R² means the line is right." The sucrose standards give R² = 0.9985 with a U-shaped residual pattern and χ²_ν = 9.1.
- Analogy: the kernel is a whiteboard nobody erases; the notebook is the printed handout. Restart-and-run-all wipes the board and rewrites it from the handout.
- Expected hands-on result (density_raw.csv): 45 rows × 8 columns, 10 NaN in w_percent; pooled SD 0.00143 g/mL, SEM 0.00064; line χ²_ν = 9.11, quadratic 1.34, line 0–15 % 4.70; soft drink 9.85 ± 0.18 % (true 9.8), diet drink 0.04 ± 0.23 % (true 0.3); straight line would give 9.54 % and 0.55 %. Learner's own Module 1 data (1 g scale): line χ²_ν ≈ 2, curvature not detectable.
- Watch for: JupyterLab started in the repo root, so `density_raw.csv` is not found; start it in `labs/module-05`. Windows users who open the notebook by double-click in Explorer get a different working directory.
- Extension: move `weighted_fit`, `line` and `quad` into a `calib.py` module and import it; add a Monte Carlo check of the quadratic inversion uncertainty with a fixed seed.
