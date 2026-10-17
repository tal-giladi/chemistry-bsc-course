# Instructor notes — 17.1 Mass spectrometry: molecular ion and fragments

- Objective: the learner finds M⁺·, applies the nitrogen rule and DBE, reads M+1/M+2 for carbon count and Cl/Br, picks a formula from an HRMS value within 5 ppm, and explains alpha-cleavage, McLafferty and benzylic fragments in real NIST spectra.
- Likely confusion: base peak vs molecular ion; M+1 (¹³C) vs M+2 (Cl, Br, S); why the electron mass matters in HRMS; the same nominal m/z (43) standing for two different ions (CH₃CO⁺ and C₃H₇⁺).
- Misconception: "the biggest peak at the right-hand end is always M". Alcohols, amines, chloroalkanes and branched compounds often show weak or no M⁺·. 1-chlorobutane's spectrum (base peak 56 from loss of HCl) is the best counterexample.
- Analogy: EI is dropping a vase from a fixed height; the vase breaks along its weakest seams, and the same vase always breaks the same way, which is why library matching works.
- Expected hands-on result: DBE 1.0 and exact mass 100.08882 for C₆H₁₂O; C₄H₉Cl M+2 ≈ 32 %, C₃H₇Br ≈ 97 %, CH₂Br₂ ≈ 51 : 100 : 49; only C₆H₁₂O within 5 ppm of 100.0883. NIST: 1-bromopropane 122/124 small, base 43; butylbenzene 134, base 91, strong 92; diethylamine 73, base 58, 30; 1-chlorobutane 92/94 tiny, base 56.
- Extension: ask for the expected M, M+2, M+4 pattern of C₆H₄Cl₂ (about 100 : 64 : 10) and check it with `isotope_pattern`, then with the NIST spectrum of 1,4-dichlorobenzene.
