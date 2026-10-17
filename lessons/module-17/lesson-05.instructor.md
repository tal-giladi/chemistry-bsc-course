# Instructor notes — 17.5 Putting it together: solving unknowns

- Objective: the learner follows the fixed workflow (formula → DBE → MS → IR → ¹³C → ¹H → all candidates → eliminate → check), names a decisive observation against each wrong candidate, and solves five real unknowns from NIST and SDBS.
- Likely confusion: which evidence is strong and which is weak; how to join fragments into all possible structures; using the NIST pages without seeing the name (scroll from the anchor, full screen).
- Misconception: "the first structure that fits is the answer". Methyl 4-methylbenzoate fits most of the worked example's data; only the ¹³C carbonyl (197 vs 167) kills it.
- Analogy: a detective lists every suspect first, then needs one alibi that clears each innocent one; a single fingerprint is not enough if two suspects have similar hands.
- Expected hands-on result: solver 13 → 5 → 3 → 2 candidates (methyl butanoate, propyl acetate). Practice: P1 propyl acetate, P2 methyl butanoate, P3 trans-cinnamaldehyde, P4 butylamine, P5 isobutyl acetate. Simulation preset `unknown`: every signal assigned before choosing.
- Extension: ask the learner to add the C₆H₁₂O₂ acetates (butyl, isobutyl, sec-butyl, tert-butyl acetate) to `candidates.csv` and find which evidence separates them (OCH₂ triplet vs doublet vs OCH vs no O–C–H).
