# Instructor notes — 33.2 Designing the study and managing the data

- Objective: the learner designs the study (known-answer test, pilot, blanks or controls, randomised order, held-out set, analysis plan), computes the number of repeats from a pilot SD, and sets up a reproducible project folder with data dictionary, hours log and git.
- Likely confusion: why t and not 1.96 for small n; why the in-sample RMS is optimistic; the difference between a blank and a control.
- Misconception: "more repeats always fix a noisy result" (systematic errors do not average away); "tidy files are cosmetic"; "I will remember why I removed that point".
- Analogy: raw data are like the original receipt in an accounts audit. You may write notes and corrections in the ledger (the code), but you never alter the receipt.
- Expected hands-on result: `lesson02_sample_size_solution.py` defaults: half-widths 0.298, 0.149, 0.111, 0.086 for n = 3, 5, 7, 10; need n = 9. Part 2 (generated data, seed 2, 500 draws, 10 held out): c 0.9613 ± 0.0019 (3 molecules) → 0.9614 ± 0.0007 (10); fitting-set RMS 10.6 ± 2.1 → 11.6 cm-1; held-out RMS 15.1 → 14.3 cm-1. Worked example: k = 2.31, 2.47, 2.20, 2.43 (1e-3 s-1), s = 0.122, n = 8 → 0.102, n = 9 → 0.094.
- Extension: ask the learner to simulate drift (a linear 2 % per day loss of titrant strength) in a block design and a shuffled design and show the fake brand difference that the block design produces.
