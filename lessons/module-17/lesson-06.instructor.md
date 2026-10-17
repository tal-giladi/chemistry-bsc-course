# Instructor notes — 17.6 Project: 50 unknowns from real SDBS spectra

- Objective: the learner solves 50 unknowns in two phases (blind MS + IR from NIST, then NMR from SDBS), fills one spectrum assignment sheet per unknown, checks answers with `lesson06_project.py` and keeps a mistakes log.
- Why names, not SDBS numbers: SDBS requires accepting its disclaimer each session and forbids robot collection, so SDBS numbers were not fetched or verified when the course was written (2026-10-17). Every unknown is identified by CAS (checked against PubChem and NIST) and the learner searches SDBS by name. SDBS has no CAS search. If AIST later adds stable public links, SDBS numbers could be added after manual checking.
- Likely confusion: gas-phase NIST IR vs liquid SDBS IR; SDBS's exact-match name search; the name showing at the top of every database page (hence the two-phase design, F11, or a study partner).
- Misconception: "once I know the name, the work is done". Phase 2 is full assignment; it trains the reading skill.
- Expected result: most learners get 35–45 right in phase 1. Typical misses: 13 (1,4-dioxane, forgetting a ring), 36/40/44 (rings vs double bonds), 39 vs 42 (pentanone isomers), 31 (DMF's two methyl singlets), 50 (keto–enol signals of ethyl acetoacetate).
- Tiers: 1–15 one group, small; 16–35 aromatic, halogens, nitrogen; 36–50 rings, alkenes, alkynes, close isomers.
- Extension: have the learner build ten more unknowns for a partner from NIST (any compound with MS and IR), with the answer key in details; or rerun five tier-3 unknowns using only ¹³C and ¹H, without MS and IR.
