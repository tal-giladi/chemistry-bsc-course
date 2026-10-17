# Module 21 plan — Statistical Thermodynamics

Technion: 01240413 Statistical Thermodynamics (2.5 points). Course: MIT 5.62 Physical Chemistry II (Spring 2008), lectures 1–17 (ensembles, molecular partition function, indistinguishability, q_trans, q_rot with symmetry number, q_vib, chemical equilibrium). Depth: a first statistical-thermodynamics course for chemists (Atkins / McQuarrie level), every number checked against NIST data.
Builds on: 13.3 (S, third law, S = k ln W promised), 13.4 (ΔrG° = −RT ln K, K(T) from NIST tables), 12.4 and 12.5 (oscillator and rotor levels, rotational populations), 20.1 (Boltzmann ratios with degeneracy), 20.2 and 20.3 (B, ω from spectra), 20.4 (D0, Birge–Sponer). Forward: 22 (transition-state theory uses the same q's), 30, 31.
Simulations (outline §5, built later): boltzmann `two-level` (21.1), `ladder` (21.2), `rotor` (21.3).
Hands-on: Python labs in `labs/module-21/` (numpy, scipy, matplotlib only). Shared helper `stat21.py`: CODATA 2022 constants, NIST standard atomic weights, NIST WebBook diatomic constants (N2, CO, HCl, O2, I2), NIST ASD atomic levels (I, Cl), level-sum partition functions and thermodynamic functions. Check data `janaf_check.csv` from the NIST-JANAF tables (I, I2, Cl). One kitchen activity (21.1: coins and cups energy-exchange game).
Module practical: 21.4 Part B — K(T) for I2(g) ⇌ 2I(g) from 500 to 1500 K from spectroscopic constants only (ω, ωx, B, D0 from JANAF 0 K enthalpies, I-atom 2P levels), harmonic vs anharmonic, against JANAF; degree of dissociation at 1 bar; ΔrH° and ΔrS° from q; written up with the lab-report template.

| Lesson | Objectives (short) | Prerequisites | Hands-on | Sources to verify |
|---|---|---|---|---|
| 21.1 Microstates, the Boltzmann distribution and temperature | count W for an Einstein solid; S = k ln W; 1/T = ∂S/∂U from two solids in contact; derive and apply the Boltzmann distribution with degeneracy | 13.3, 12.5, 20.1 | `lesson01_microstates.py`; coins-and-cups game; sim `two-level`; pencil | MIT 5.62 L2–L4; CODATA k; NIST WebBook I2; LibreTexts UC Davis 110B ch. 18 |
| 21.2 The partition function | q as the number of accessible states; U, Cv, S, A from q; two-level (Schottky) and ladder; Q = q^N/N! | 21.1, 13.4 | `lesson02_partition.py` (Cl atom Cp vs JANAF, N2 vibrational Cp vs NIST Shomate); sim `ladder`; pencil | MIT 5.62 L3–L6; NIST ASD Cl; JANAF Cl(g); NIST WebBook N2 |
| 21.3 Molecular partition functions: translation, rotation, vibration | q_trans and thermal wavelength; q_rot with σ and θ_rot; q_vib from v = 0; q_el degeneracy; S° of diatomics within 0.1 J/(mol K) of NIST | 21.2, 20.2, 20.3, 12.4 | `lesson03_molecular_q.py` (S° and Cp of N2, CO, HCl, O2, I2, I); sim `rotor`; pencil | MIT 5.62 L7–L14; NIST WebBook constants and S°; LibreTexts symmetry number |
| 21.4 From partition functions to equilibrium constants (module practical) | K = Π(q°/N_A)^ν exp(−ΔE0/RT); D0 from data; K(T) for I2 ⇌ 2I vs JANAF; dissociation degree; entropy of dissociation explained | 21.3, 13.4, 20.4 | Part A pencil worked through; Part B `lesson04_practical.py` | MIT 5.62 L16–17; JANAF I-001, I-027; NIST ASD I; LibreTexts 26.8 |

Data: all constants CODATA 2022 and NIST (WebBook, ASD, JANAF), retrieved 2026-10-17. No SDBS.
Safety: no reagents. 21.1 coins: keep away from small children (choking).
