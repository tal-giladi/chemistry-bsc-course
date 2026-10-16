# Module 01 plan — Orientation, Units and Safe Practice

Planning file, not imported. Written 2026-10-16. Technion mapping: none (orientation module).
Practical piece: lesson 01.5, density of water and sugar solutions with a kitchen scale and a syringe, with uncertainty and a syringe calibration.
Simulations linked: `measurement-error` presets `repeat`, `bias` (lesson 01.5).

## 01.1 How this course works and what it cannot train
- Objectives: describe the lesson anatomy and the study loop; list four bench skills the course cannot train; budget study hours for a module; schedule spaced review.
- Prerequisites: none.
- Hands-on: 30-minute self-diagnostic (scientific notation, rearranging, percent, logs, unit conversion) with worked answers; write a 4-week study plan.
- Sources: Technion undergraduate page, plan.md scope list, Dunlosky et al. 2013 (via APS release), MIT OCW 5.111SC.

## 01.2 Units, significant figures and dimensional analysis
- Objectives: name the 7 SI base units and the 2019 definition idea; convert with prefixes and the factor-label method; apply sig-fig rules for ×/÷ and +/−; detect a unit error by checking dimensions.
- Prerequisites: 01.1.
- Hands-on: pencil set of 8 problems, answers in details.
- Sources: BIPM SI brochure and defining constants, NIST SP 811, NIST CODATA (Avogadro constant), OpenStax Chemistry 2e 1.5 and 1.6.

## 01.3 The lab notebook and the lab report
- Objectives: write a notebook page that another person can repeat; correct an entry without destroying it; structure a short report; report a result with uncertainty and the right digits.
- Prerequisites: 01.2.
- Hands-on: set up the notebook; measure how much water a teaspoon holds (5 repeats, kitchen scale); write a one-page mini report.
- Sources: NIH OIR record keeping / ELN pages, Truman State lab report guide, UCLA report guidelines.

## 01.4 Chemical safety: hazards, SDS and Israeli law
- Objectives: read GHS pictograms, signal words and H/P statements; find the GHS section in PubChem; explain why concentration changes the hazard (glacial acetic acid vs vinegar); state what the Hazardous Substances Law 1993 means for a home learner.
- Prerequisites: 01.1.
- Hands-on: PubChem lookup of CIDs 176, 23665760, 516892, 702 plus your own bleach label; written risk assessment for lesson 01.5.
- Sources: UNECE GHS Rev.11 (2025), PubChem PUG-View GHS data (checked 2026-10-16), Hazardous Substances Law 1993 summary (Israel MFA via AMPEID / InforMEA), Ministry of Environmental Protection.

## 01.5 Your home kit and first measurement
- Objectives: assemble the home kit; calibrate a syringe with water; measure density of water and 10/20/30 % w/w sugar solutions with mean, SD and standard uncertainty; compare with reference values.
- Prerequisites: 01.2, 01.3, 01.4.
- Hands-on: module practical; Python analysis `labs/module-01/density_analysis.py` (solution file included); simulations `measurement-error?preset=repeat` and `?preset=bias`.
- Sources: Tanaka et al. 2001 (water density), NBS Letter Circular LC 770 (sucrose solutions, Plato values), JCGM 100:2008 GUM, NIST TN 1297.
