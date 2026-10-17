# Instructor notes — 10.1 The titration bench: indicators, burettes and endpoints

- Objective: indicator choice from the curve with a calculated titration error (closed-form V(pH) from the charge balance); burette reading and a three-term volume budget; NaOH standardised with KHP; syringe drop calibration. Covers the S3 experiments "solutions and solubility" and "acid–base titrations".
- Likely confusion: end point vs equivalence point; why the error for a weak acid is huge with methyl red but tiny for a strong acid. Show both curves on the script's plot with the indicator bands.
- Misconception: "pH 7 indicator is always right because neutralisation gives pH 7". The equivalence pH of acetic acid with NaOH is about 8.7. Also "weighing the titrant removes the drop problem" — it removes volume reading, not end-point resolution.
- Analogy: the indicator as a referee who blows the whistle at a fixed pH; if the referee stands at the wrong line, the play stops early.
- Expected hands-on result: script errors (acetic, 0.1 M): methyl orange −92.15 %, methyl red −36.38 %, BTB −0.45 %, phenol red −0.09 %, phenolphthalein +0.08 %; HCl all within 0.4 %. Example drops 44.9 mg (true model 45.0 mg), 0.64 % of 7 g. Real oral syringes give 30–60 mg drops depending on tip and liquid.
- Data note: `drop_calibration_example.csv` from `make_data.py` (seed 1010), not measured.
- Safety: water or 5 % baking-soda solution only; glasses; no needles.
- Extension: add the carbonate error — titrate KHP to phenolphthalein with NaOH containing 2 % Na2CO3 and compute the bias; or run the ChemCollective KHP standardisation and compare.
