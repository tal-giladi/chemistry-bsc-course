# Instructor notes — 11.3 Writing a lab report and a figure that tells the story (module practical)

- **Objective:** results stated first as value ± uncertainty, unit and meaning; tense and hedging matched to evidence; a misleading figure diagnosed and redrawn; a complete report from the learner's own 10.6 (or 09.6) data, checked with a reverse outline and `writing_checklist.md`.
- **Likely confusion:** when a y-axis may start above zero (dot and line plots yes, bars no); SD versus 95 % CI in error bars; "consistent with" versus "proves".
- **Misconception:** "a good figure is a pretty figure". The test is whether a reader gets the one message and can see the data behind it; Rougier's rule "message trumps beauty".
- **Analogy:** a report is a newspaper story: the headline (first sentence) carries the news, the body adds evidence, and the photo (figure) must show what the caption says.
- **Expected hands-on result:** `good_figure.py` prints means A 4.955, B 4.948, C 4.895, D 5.018, E 4.957, F 4.979 % with s 0.028, 0.014, 0.111, 0.011, 0.012, 0.053 and CI half-widths 0.035, 0.017, 0.137, 0.013, 0.015, 0.066; end point 8.35 mL (model 8.30). Bad-figure problems: empty titles, no units, bars hide C's spill, cut axis (C's bar about a quarter of D's for 2.5 %), upward-only population SD, jet colours and redundant legend, twin axis plus colour bar, heavy grid, no end point.
- **Extension:** redraw a figure from one of the 11.1 papers from its published table values; or apply Grubbs' test (09.2) to C's spill and discuss whether to exclude it, with a stated reason.
- **Scope:** class data and titration curve are simulated (`make_data.py`, seeds 1103/1104). Report quality is not auto-graded; the module quiz tests the decisions.
