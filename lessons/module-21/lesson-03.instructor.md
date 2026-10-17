# Instructor notes — 21.3 Molecular partition functions: translation, rotation, vibration

- Objective: build q_trans, q_rot (with σ), q_vib (from v = 0) and q_el from NIST constants; assemble S° and match NIST within 0.11 J/(mol K) for Ar, N₂, CO, HCl, O₂, I₂, I and Cl.
- Likely confusion: why σ is a division and not a correction to J levels. Explain through the N₂ Raman 2 : 1 alternation in 20.3: nuclear spin allows even or odd J per spin set; summed over spin sets and divided by the (ignored) nuclear-spin degeneracy, the high-T result is q/σ.
- Misconception: "vibration dominates entropy because it is the most 'chemical' motion". The bar chart shows translation is 75–100 % of S° at 298 K; vibration matters only for soft modes (I₂ 8.4 J/(mol K)).
- Analogy: the factorised q is a menu: number of dishes = starters × mains × desserts; each motion is one course, and the entropy adds the logs.
- Expected hands-on result: N₂ Λ = 19.10 pm, q_trans/N_A = 5.905e6; θ_rot N₂ 2.863 K, HCl 15.021 K, I₂ 0.054 K; q_rot high-T vs sum: N₂ 52.08/52.24, HCl 19.85/20.19, I₂ 2776.7/2776.9. S° (model / NIST): Ar 154.85/154.846, N₂ 191.60/191.609, CO 197.65/197.660, HCl 186.87/186.902, O₂ 205.18/205.152, I₂ 260.58/260.685, I 180.79/180.786, Cl 165.19/165.189. H − H0: N₂ 8.669, I₂ 10.095 kJ/mol (JANAF 8.670, 10.116). Cp(298): 29.11 (N₂), 36.72 (I₂).
- Data note: HCl uses H³⁵Cl constants with the natural-abundance mass; the 0.04 J/(mol K) low result is mostly the missing H³⁷Cl rotational contribution.
- Extension: compute S° of H₂O (σ = 2; NIST rotational constants A, B, C and three fundamentals) and compare with CODATA 188.835 J/(mol K); or show the CO residual entropy argument: R ln 2 = 5.76 is the maximum for random CO/OC orientation, against the measured ~4.6.
