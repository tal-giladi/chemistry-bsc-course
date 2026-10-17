# Instructor notes — 17.3 Proton NMR: shift, integration and splitting

- Objective: the learner predicts the number of ¹H signals and their shifts, scales integrals to the formula, applies the n+1 rule with J, recognises ethyl and isopropyl patterns, and knows when Δν/J is too small for first-order reading.
- Likely confusion: counting the signal's own protons as neighbours; δ in ppm vs Δν and J in Hz; why OH/NH do not split; "downfield" meaning higher δ (left on the page).
- Misconception: "a higher-field magnet moves the peaks". In ppm the shifts stay the same; the multiplets get narrower in ppm because J (Hz) is fixed while Hz per ppm grows. Second: "equivalent = same shift". Accidental overlap is not equivalence.
- Analogy: each neighbour is a coin that can land heads or tails; n coins give n+1 totals with Pascal-triangle odds, which is the multiplet.
- Expected hands-on result: Pascal rows to 1 6 15 20 15 6 1; counts 2, 2, 3, 5, 2, 1. Bromoethane Δν/J = 14.5 at 60 MHz. SDBS: bromoethane q ≈ 3.4 / t ≈ 1.7; 2-chloropropane septet ≈ 4.1 / d ≈ 1.5; 1-nitropropane t ≈ 4.4 / m ≈ 2.0 / t ≈ 1.0. Simulation: J ≈ 7 Hz in both ethyl multiplets; roofing at low Δν/J.
- Extension: predict the spectrum of propyl acetate and compare with SDBS (search `propyl acetate`); or add a second coupling constant to `lines_for_signal` to draw a doublet of doublets for a vinyl proton.
