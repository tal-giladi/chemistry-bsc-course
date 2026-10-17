# Instructor notes — 10.6 Project: home vinegar titration with full error analysis

- Objective: the module practical (plan.md S3 home experiment): five mass-based titrations of vinegar with baking-soda titrant and cabbage indicator, an indicator blank, mean, SD, 95 % CI, a GUM-style budget, t-test and expanded-uncertainty comparison with the label, and a lab report.
- Likely confusion: CI vs expanded uncertainty; why a significant t-test does not prove the label wrong; w/w vs g/100 mL.
- Misconception: "more repeats fix everything" — they shrink only the Type A term. And "the scale is the weak point" — in the budget the reagent purity dominates.
- Analogy: the budget as a household budget: cut the biggest expense first, not the coffee.
- Expected hands-on result: example 4.932, 4.929, 4.943, 4.953, 4.980 % w/w; mean 4.948, SD 0.021, RSD 0.42 %, CI ± 0.026; without blank 4.990; U (k = 2) 0.041; 4.972 g/100 mL; t = −2.98 vs 2.78; label inside ±U. True model 4.95 % w/w, end-point excess 0.07 g, blank 0.06 g. Real kitchen runs: 4.8–5.2 g/100 mL, RSD 0.4–1 %.
- Data note: `vinegar_project_example.csv` from `make_data.py` (seed 1010), not measured.
- Safety: household 5 % vinegar only (not vinegar essence or cleaning vinegar, which can be 10–25 % and corrosive); glasses; never with bleach.
- Extension: replace the cabbage end point with a pH-strip or phone-photo colour series and a derivative end point; or measure the density of the vinegar with the syringe-and-scale method of lesson 01.5 instead of assuming 1.005 g/mL.
