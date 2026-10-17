# Instructor notes — 10.5 Ion-selective electrodes and water testing

- Objective: ISE calibration with slope and linear-range check; selectivity and TISAB; standard addition; water testing as a summary of the module; hardness from labels and a calibrated soap titration. Covers the S3 experiments "ion-selective electrodes" and "water testing".
- Likely confusion: why the fluoride slope is negative; why concentrations "before TISAB" can be used throughout (the 1:1 dilution only shifts K); 59.16/z.
- Misconception: "the line can be extrapolated, it is logarithmic anyway" — the response flattens near the detection limit (EPA: up to 160 % high below 0.5 mg/L). And "lather = clean water": detergents lather in hard water.
- Analogy: TISAB as making every runner wear the same shoes, so only speed (concentration) differs.
- Expected hands-on result: slope −57.6 mV/decade (97 %), intercept −43.0 mV; residuals −4.1, −1.8 mV at 0.10 and 0.20 mg/L; A 0.857 mg/L (true 0.85), B 0.136 (true 0.12, flagged); standard addition 0.837 mg/L. Soap: drops = 1.3 + 0.0596 H; tap ≈ 255 (true 260), boiled ≈ 196 (true 200). Real soap tests: duplicates within 1–2 drops; boiled tap lower only if carbonate hardness is present.
- Data note: example files from `make_data.py` (seed 1010), not measured. Israeli regulation numbers were not verified to the parameter level; the lesson cites WHO for fluoride and tells learners to check the Ministry of Health.
- Safety: soap and drinking water only; glasses; cooled water.
- Extension: alkalinity of tap water by titration with vinegar to the cabbage colour of pH ~4.5, compared with the bicarbonate on a bottled-water label.
