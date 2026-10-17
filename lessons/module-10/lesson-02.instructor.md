# Instructor notes — 10.2 Potentiometric and redox titrations

- Objective: end points from first/second derivatives and Gran plots; redox curve from Nernst on each side; E_eq as weighted average of formal potentials; ferroin choice; formal potentials read from the curve; the Mn-in-steel periodate method. Covers the S3 experiments "visual and potentiometric redox titrations" and "manganese in steel".
- Likely confusion: standard vs formal potential; SHE vs Ag/AgCl scales; why the Gran x-intercept survives a constant offset but not a drift.
- Misconception: "the steepest point of the data is the end point" — with coarse steps it is only within one step. And "the potential at equivalence is set by whichever is stronger" — it is the weighted average.
- Analogy: the half-equivalence point as a built-in calibration point, like the 50 % mark of a tug of war where both teams are equal.
- Expected hands-on result: acid–base 19.950 (first), 19.998 (second), 19.917 mL (Gran), pKa (Gran) 4.798, half-eq pH 4.794; true V_eq 20.00, pKa 4.757. Redox 12.450 (first), 12.500 (second), E0' Fe 0.682 V, E0' Ce 1.440 V, reading at 12.50 mL 1.061 V vs SHE.
- Data note: `potentiometric_example.csv` and `redox_example.csv` from `make_data.py` (seed 1010); model offset +0.04 pH, drift +0.002 pH per reading, redox noise 2 mV.
- Safety: no home version; concentrated acids and periodate are lab reagents (Israel: Hazardous Substances Law 1993). Point to the 08.5 vitamin C titration for a safe visual redox titration.
- Extension: activity correction of the Gran plot (Davies equation), or fit the whole redox curve with scipy curve_fit for V_eq, E0'Fe and E0'Ce at once.
