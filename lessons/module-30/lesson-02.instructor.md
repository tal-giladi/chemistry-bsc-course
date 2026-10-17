# Instructor notes — 30.2 Electron spin resonance and hyperfine splitting

- Objective: the learner predicts and reads ESR patterns (2nI + 1, binomial intensities), extracts g and a from a methyl spectrum, uses McConnell, and recognises when second-order (Breit–Rabi) shifts matter (H atom).
- Likely confusion: field-swept spectra (why not frequency); derivative lineshape; sign of a (spin polarisation gives negative a, ESR of tumbling radicals gives only |a|).
- Misconception: "no s orbital at the proton, so no coupling" (methyl); and "the midpoint is always B0" (H atom).
- Analogy: the hyperfine splitting is like a compass needle beside a few small fridge magnets; each magnet orientation nudges the needle's resonance a fixed amount, whatever the strength of the Earth field (the main field).
- Expected hands-on result: CH3 lines 333.705, 336.009, 338.313, 340.617 mT; g 2.00255; a 2.304 mT = 64.6 MHz; heights 1.01 : 2.94 : 2.95 : 1.00; CD3 7 lines, a_D 0.354 mT, width 2.12 mT. H atom: 309.81 and 360.78 mT (exact), 311.86 / 362.55 first order, centre shift −1.91 mT, spacing +0.29 mT, naive g 2.01370. Pencil: ethyl 12 lines; Q 2.25 mT; naphthalene ρ 0.22 and 0.08. Sim parts depend on ir-esr `esr-methyl` and `esr-hydrogen` (not built yet).
- Extension: add a 13C (I = 1/2) satellite to the methyl simulation in Python and estimate the s character of the carbon orbital from a(13C); or compute CH3 g and a with ORCA in Module 31.
