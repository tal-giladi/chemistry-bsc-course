# Instructor notes — 23.6 Surface tension and detergents (module practical)

- Objective: the learner measures γ by drop weight relative to water (IAPWS at the measured T), locates the break by a two-line fit in ln c, computes Γ and the area per molecule with the ionic factor stated, and writes a full report with an uncertainty budget.
- Likely confusion: why ln c (and why its units cancel in the slope); what "surface excess" means; why the plateau is flat when more soap is added; n = 1 versus n = 2.
- Misconception: "more soap always cleans better". Above the CMC surface tension no longer falls; extra soap builds micelles (useful for holding grease, but not for wetting).
- Analogy: the surface is a car park; cars (surfactant molecules) fill it until it is full, then the rest queue in the streets (micelles) and the car park looks the same.
- Expected hands-on result: example data water 72.58 mN/m (21 °C), drop 49.63 mg; plateau 31.5 mN/m; break 1.72 mL/L (true 1.5), slope −10.8 mN/m per ln unit, Γ 4.40 µmol/m² and 0.38 nm² (n = 1), 2.20 and 0.75 nm² (n = 2). Home: break 0.3–3 mL/L, plateau 25–35 mN/m; counted γ within 5 % of weighed.
- Extension: fit the Szyszkowski equation γ = γ0 − a ln(1 + c/b) below the CMC with curve_fit and take dγ/dln c analytically at the break; or add 1 g/L of salt to every solution and see the break move to lower concentration (screening of head-group repulsion).
