# Instructor notes — 13.2 Enthalpy, heat capacity and calorimetry

- Objective: q_p = ΔH and q_V = ΔU; ΔH = ΔU + Δn_gas RT; bomb calibration with benzoic acid; Cp(T) from Shomate; Kirchhoff's law (constant ΔCp vs integrated).
- Likely confusion: counting Δn_gas with liquid water as gas, and per what amount (per mole of fuel as written). Also mixing J (RT, Cp) with kJ (ΔH).
- Misconception: "a bomb calorimeter measures enthalpy" (it measures ΔU) and "ΔrH is a constant of the reaction" (it depends on T through ΔrCp).
- Analogy: Kirchhoff as a detour on a map. You cannot react at 700 K directly in the table, so you cool down, react at 298 K, and heat up again; a state function does not care about the detour.
- Expected hands-on result: script C_cal = 10.885 kJ/K, ΔcH(sucrose) = −5644 kJ/mol; benzoic acid ΔcH −3229.4 kJ/mol; NH₃ synthesis ΔrH −91.88 (298 K), −99.79 (500 K), −105.32 (700 K), −110.11 (1000 K); constant-ΔCp estimate −109.70 at 700 K. Cp(NH₃) 35.65 → 56.50 J/(mol K) from 298 to 1000 K. Part B: ΔcU(CH₄) −885 kJ/mol; C_cal 10.9 kJ/K; q_p 11.8 kJ, q_V 8.5 kJ. Simulation: two calibrations should agree within ~0.5 % if the corrected rise is used.
- Data note: the SRM 39j value is for the certificate's bomb conditions, not exactly the standard state; the Washburn corrections are a few parts in 10⁴ and are not taught here.
- Extension: compute Cp − Cv for liquid water from α, κ_T (Cp − Cv = TVα²/κ_T, about 0.8 J/(mol K) at 25 °C with α ≈ 2.6 × 10⁻⁴ K⁻¹ and κ_T ≈ 4.5 × 10⁻¹⁰ Pa⁻¹), to show that the ideal-gas R does not apply to liquids.
