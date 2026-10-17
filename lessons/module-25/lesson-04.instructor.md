# Instructor notes — 25.4 Gas chromatography and GC-MS

- Objective: the learner sets up a GC-MS run with reasons (tune, blank, split, programme, solvent delay, scan range, ladder), computes a weighted dot-product match factor, combines MF with RI into an accept/reject/flag rule, spots co-elution from unexplained ions, and uses the NIST WebBook for spectra and indices.
- Likely confusion: TIC versus EIC; forward match versus reverse match (only forward is coded here); that a library search never returns "nothing"; why mass weighting.
- Misconception: "MF 950 means 95 % certain". The score is a similarity, not a probability, and isomers score alike.
- Analogy: the library search is a face-recognition app that always names someone; the retention index is checking the person's height.
- Expected hands-on result (after `get_nist_ms.py`): P1 α-pinene 976 / RI 936; P2 β-pinene 970 / 973; P3 myrcene 971 / 993; P4 limonene 918 / 1030, 11 % residual → p-cymene 884; P5 γ-terpinene 984 / 1062; P6 linalool 980 / 1101; P7 not identified (γ-terpinene 861, limonene 844); P8 neral 886 vs geranial 883 at 1241; P9 geranial 887 at 1271. With C98555 added, P7 α-terpineol 973. With a ± 15 window P3 becomes ambiguous (β-pinene at 979 is 14 away) — a good discussion point on window choice. Part C: limonene base 68, M⁺ 136.
- Note: NIST spectra are not in the repo; learners download them. If NIST rate-limits (HTTP 429), the script waits and retries; rerunning skips files already downloaded.
- Extension: implement a reverse match (ignore library ions absent from the measured spectrum) and see how it changes P4; discuss why "natural" lemon oil cannot be proven by GC-MS (enantiomer ratio by chiral GC, isotope ratios by IRMS).
