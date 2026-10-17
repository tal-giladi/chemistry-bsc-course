# Instructor notes — 21.1 Microstates, the Boltzmann distribution and temperature

- Objective: count W for an Einstein solid, connect it to S = k ln W, get 1/T = ∂S/∂U from two solids in contact, and use p_i = g_i e^(−E_i/kT)/q with real NIST levels.
- Likely confusion: "equally likely microstates" vs "equally likely macrostates". The 3 + 3 oscillator table (28, 63, 90, 100, …; total 462) settles it: the even split is the most likely macrostate but has only 22 % of the microstates.
- Misconception: "high temperature puts everything in the top level". Infinite T equalises states, not levels; for Cl the 2P1/2 fraction stops at 1/3. Population inversion needs pumping.
- Analogy: money randomly passed between people in a room ends up with many poor and few rich (an exponential distribution) without anyone being greedy; the coins-and-cups game is that experiment.
- Expected hands-on result: W(3,3) = 10; two solids peak q_A = 60, slopes 1.775 and 1.767, 95 % within ±10; exchange game fractions 0.49, 0.25, 0.14, 0.07 vs 0.500, 0.250, 0.125, 0.0625 (seed 21); I₂ populations v = 0–5: 0.643, 0.230, 0.083, 0.030, 0.011, 0.004; HCl J_max = 3 (0.189), J = 0 holds 0.050; HCl N1/N0 = 9.0e-7. Coins: about 0.5 / 0.25 / 0.12 with scatter of ±0.05 from 200 readings. Pencil: W = 5; NO upper fraction 0.36.
- Extension: derive the large-N slope ∂ln W/∂q = ln(1 + N/q) with Stirling's formula, show that it gives the Einstein-solid temperature kT = ε / ln(1 + N/q) (q_A = 60, N = 300: kT = 0.56 ε) and compare with the exchange game's kT = ε / ln 2.
