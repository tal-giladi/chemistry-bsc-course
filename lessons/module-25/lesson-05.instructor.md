# Instructor notes — 25.5 HPLC method thinking

- Objective: the learner chooses mode, column, pH, buffer, solvent and detector from pKa, log P and UV; fits the LSS model to two scouting runs; reads a resolution map and spots an elution-order crossing; quantifies pH robustness; runs and judges a system-suitability test; lists validation characteristics.
- Likely confusion: φ as a fraction versus per cent; S as minus the slope; the difference between system suitability (every day) and validation (once); why caffeine's pKa of 0.7 belongs to its conjugate acid.
- Misconception: "pH matters only for ionic compounds" or "a method that separates today is robust". The pH sensitivity calculation shows the opposite near a pKa.
- Analogy: the resolution map is a weather map for the separation: you look for the high-pressure ridge before you plan the trip.
- Expected hands-on result: S 3.26/4.30/5.01/5.20; log kw 0.91/1.30/2.10/2.30; worst pair paracetamol/caffeine; Rs 6.1 (20 %), 3.9 (25 %), 1.95 (30 %), 0.45 (35 %); crossing near 38 %; best within 15 min 23 %, Rs 4.8, 13.7 min. SST new column PASS (Rs 4.22, tailing ≤ 1.25, area RSD ≤ 0.52 %, N ≈ 10 000); after 400 injections FAIL (salicylic acid tailing 2.36, N ≈ 5500). Worked example: aspirin S 5.0, log kw 2.10, tR 8.1 min at 25 %; at pH 3.5 k 3.9 (aspirin) and 3.1 (salicylic acid), order reversed.
- Extension: write the gradient retention equation (linear gradient, LSS) and compare predicted gradient retention with the simulation; add the neutral-fraction model to the script to build a pH–φ resolution map.
