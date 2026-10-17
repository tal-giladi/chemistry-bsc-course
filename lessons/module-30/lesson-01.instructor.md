# Instructor notes — 30.1 IR spectroscopy from first principles: HCl rotation-vibration

- Objective: the learner plans a safe gas-phase FTIR measurement of HCl, assigns both isotopologues at high resolution, fits ν0, B0, B1, D per band, extracts ωe and ωexe from fundamental + overtone, and validates the result with isotope ratios and a Boltzmann temperature.
- Likely confusion: which level each prime refers to; why the cubic term is −2(D′ + D″)m³; why ωexe from two bands differs from NIST's (ωeye absorbed).
- Misconception: "higher resolution only makes the plot prettier". In 20.3 resolution was the whole 1 % error in B0.
- Analogy: the isotope doublets are like two choirs singing the same song a semitone apart; a bad microphone (4 cm⁻¹) hears one blurred voice, and you misjudge the pitch of both.
- Expected hands-on result (example data, 296 K true): H³⁵Cl fundamental ν0 2886.038, B0 10.4399, B1 10.1327, D 5.32e-4, rms 0.003 cm⁻¹; overtone ν0 5668.460, B2 9.8254; αe 0.3072, Be 10.5935, re 1.2745 Å; ωe 2989.7, ωexe 51.81; Morse De 43 131, D0 41 649 cm⁻¹ = 5.16 eV vs real 4.43 eV; isotope ratios 0.999269 (ρ 0.999243) and 0.998528 (ρ² 0.998487); T 292 ± 1 K. Quadratic-only fit: rms 0.32 cm⁻¹, max 0.62. Pencil: DCl 2070 cm⁻¹ (measured ~2091), B0 5.37. Sim part depends on ir-esr `hcl` (not built yet).
- Extension: fit line areas instead of heights and see the temperature move towards 296 K; or add ωeye using a third band (3–0 near 8347 cm⁻¹) and see ωexe approach 52.82.
