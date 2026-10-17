# Instructor notes — 13.4 Free energy and chemical potential

- Objective: G and A from the second law; dG = V dp − S dT and Maxwell relations; μ = μ° + RT ln(p/p°); ΔrG = ΔrG° + RT ln Q; K(T) from NIST data with heat capacities.
- Likely confusion: ΔrG vs ΔrG°. Students read a positive ΔrG° as "the reaction cannot go". Worked example 2 is the antidote; have them compute ΔrG for a few Q values.
- Misconception: "Maxwell relations are abstract tricks". Show the payoff: S(p) of an ideal gas and (∂S/∂V)_T both drop out in one line, and in real fluids they let you get entropy from p–V–T data.
- Analogy: chemical potential as "chemical pressure" or "escaping tendency": matter flows downhill in μ, just as heat flows downhill in T and gas flows downhill in p.
- Expected hands-on result: K (constant ΔH, ΔS / NIST Cp / JANAF): 298 K 5.61e5/5.61e5/5.42e5; 500 K 0.178/0.101/0.0995; 700 K 3.22e-4/8.88e-5/8.75e-5; 800 K 4.48e-5/9.05e-6/8.95e-6. Reactor mixture Q = 5.93e-7, ΔrG = −29.2 kJ/mol. Ideal-gas NH₃ mole fraction at 700 K: 0.003 (1 bar), 0.119 (50), 0.197 (100), 0.300 (200), 0.367 (300). The 298 K JANAF/NIST difference (3.5 %) is the CODATA (−45.94) vs JANAF (−45.898) ΔfH of NH₃.
- Data note: Shomate fits for N₂ change range at 500 K; the helper switches automatically. Water vapour's NIST fit starts at 500 K, so the water-gas shift (13.6) is done from 500 K up.
- Extension: add a fugacity correction with the virial equation at 200 bar (Module 7's van der Waals constants are good enough for a first estimate) and see how much the NH₃ fraction changes.
