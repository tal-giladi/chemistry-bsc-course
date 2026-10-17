# Instructor notes — 21.2 The partition function

- Objective: compute q from levels, read it as "number of accessible states", get U, Cv, S and A from it, apply N! for gases, and reproduce NIST heat capacities for Cl(g) and N₂.
- Likely confusion: the zero of energy. q, U and A all depend on it; S and Cv do not. Insist that the lowest level is zero and that results are U − U(0), A − A(0); 21.4 brings U(0) back as D0.
- Misconception: "N! is just a constant, so it cannot matter". It does not affect U or Cv, but it changes S by k ln N! ≈ R(ln N − 1) per mole, which is the difference between a correct and a non-extensive entropy (Gibbs paradox).
- Analogy: q as the number of seats in a theatre that people are willing to walk to; far seats (high energy) count only fractionally, and heating the audience makes them walk further.
- Expected hands-on result: q_el(Cl) 4.0000 (100 K), 4.0283 (298.15 K), 4.5619 (1000 K), 5.5515 (5000 K); Cl(g) Cp model vs JANAF identical to ±0.001 from 100 to 2000 K, peak 2.002 J/(mol K) near 573 K. N₂ (θ = 3352 K): 7/2R + Cv_vib = 29.560/31.380/32.613/34.673/35.714 vs Shomate 29.581/31.438/32.692/34.847/35.976 at 500/800/1000/1500/2000 K. I₂: Cv_vib 7.618, Cp 36.718 (JANAF 36.887). Pencil: 443 K; 72 K; S_vib(I₂) 8.43 J/(mol K).
- Extension: add the 2Π3/2 level of NO and compare with the NIST-JANAF NO table at 50–300 K; or derive the high-temperature expansion of the Einstein function, Cv/R ≈ 1 − x²/12.
