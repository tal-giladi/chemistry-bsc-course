# Instructor notes — 08.7 Lab: coffee-cup calorimetry and a first titration

- Objective: calibrate a foam-cup calorimeter; extrapolate ΔT to the mixing time; ΔsolH(NaHCO3) with propagated uncertainty vs the Hess prediction (+19.6 kJ/mol); mass-based vinegar titration with cabbage indicator, mean, SD and 95 % CI. This is the module practical (the S2 lab part plus the red-cabbage indicator from plan.md).
- Likely confusion: why the cup needs calibrating, and why the extreme reading is not ΔT. Show both on the example plot.
- Misconception: "three repeats with a small SD means the answer is right". The example titration data has a built-in +1 % end-point bias that the SD does not show. Also "an acid–base titration is a redox reaction because something is neutralised": check oxidation numbers.
- Analogy: calibration as weighing the empty bowl (tare) before weighing flour.
- Expected hands-on result: C_cal 20–60 J/K (the example gives 46 ± 9, true model value 30; the pour loss biases it high); ΔT for 5.00 g NaHCO3 in 100 g water about −2.0 to −2.4 K; ΔsolH +15 to +19 kJ/mol (example 17.4 ± 0.7; true model 17.5). Titration about 7.0 g of 5 % w/w titrant per 5 g vinegar; results 4.8–5.2 % w/w, RSD 1–2 % (example 4.96, 5.00, 5.07; mean 5.01, SD 0.05, CI ± 0.14; true model 4.95).
- Data note: example CSVs are made by make_data.py from stated models (seed 808), not measured. The NaHCO3 table value is for infinite dilution; real integral heats at ~0.6 mol/kg are somewhat lower.
- Safety: hot water ≤ 45 °C; glasses for fizzing; never mix vinegar with bleach.
- Extension: replace NaHCO3 with citric acid + baking soda (a cold reaction, plan.md S5) and compare ΔH per mole of CO2; or analyse the titration as in Module 10 with five repeats and a potentiometric end point from a phone pH strip photo.
