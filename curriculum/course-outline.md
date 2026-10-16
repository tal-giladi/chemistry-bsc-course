# Course outline — Self-taught Chemistry Degree (Technion B.Sc. track)

Planning file, never imported. Binding rules, in order of precedence:
1. `C:\Users\TalGiladi\OneDrive\repos\tals-academy\docs\new-course-instructions.md` (the Academy import contract).
2. This outline.
3. `plan.md` (the original degree plan: Technion course numbers, simulations S1–S11, home experiments, safety rule, "what this plan does not train").

Titles and paths: `scripts/manifest.py` is the single source of truth (33 modules, 176 lessons). Never change them.

## 1. Who it is for and what it is

An adult self-learner, about 10–12 hours a week, who wants the understanding a Technion chemistry graduate has. It mirrors the Technion B.Sc. in Chemistry (program 012042-1-000, catalog 2025/2026). It awards no degree and trains no bench hands (Module 1, lesson 1 says this plainly; every lab lesson repeats it in one sentence where relevant).

Assume: high-school maths and some high-school chemistry. Nothing else. Math, physics, biology and Python are short *bridge* modules: they teach exactly what the chemistry modules need, with exercises and quizzes, and point to the full MIT OCW course for depth.

## 2. Principles

- **Learning by doing.** Every lesson ends in a hands-on part: a simulation run with a task and a target number, a Python analysis of real or realistic data (code in `labs/module-NN/`), a real-data exercise (SDBS, NIST WebBook, PubChem), a safe home experiment, or a pencil problem set with worked answers in `<details>`. Each module's last lesson (or a clearly marked part of it) is the module's larger practical piece that uses everything in the module.
- **Simulations replace wet labs** (Tal's rule): a simulation counts if the learner learns everything the lab teaches apart from physical hand practice. Each lab simulation must teach five things: the procedure, why each step is done, the safety reasoning, what can go wrong, and how to analyse the data and its error.
- **Current sources.** Verify facts, constants, safety guidance, software versions and URLs against primary sources (IUPAC, NIST/CODATA, GHS/UN, PubChem, Israeli Ministry of Environmental Protection, official software docs, MIT OCW, LibreTexts, OpenStax). Constants: CODATA 2022 values from NIST. Software versions pinned in `labs/common/requirements.txt` (Python 3.14, checked 2026-10-16). Avogadro, xtb and ORCA versions: verify on the official sites when writing Module 31 and pin them in that module's lab README.
- **Practical over exhaustive.** Worked examples with real numbers, the decisions a chemist makes, common mistakes and how to recover.
- **Honest scope.** Say what the simulation or home experiment does not train.

## 3. Lesson anatomy (fixed — every lesson, this order, these exact `##` headings)

1. `## Why it matters` — a concrete situation where this knowledge decides something.
2. `## Core ideas` — the mechanism, with `###` sub-sections. Math as intuition → equation (KaTeX) → tiny numeric example → interpretation. Diagrams as ```` ```mermaid ```` or SVG in `assets/` (`assets/mNN-<name>.svg`, meaningful alt text).
3. `## Worked example` — one or two fully worked problems with real numbers and units.
4. `## Hands-on` — the practical part: what you need, time, steps, expected result / how you know it worked, reference solution in `<details>`. Simulation links alone on their own line: `[Simulation: Titration bench — weak acid with indicator choice](../../simulations/titration/index.html?preset=weak-acid)`. Home experiments open with `> [!WARNING]` or `> [!CAUTION]` and use kitchen/pharmacy materials only.
5. `## Common mistakes` — 3–6 mistakes and how to spot and fix them.
6. `## Key takeaways` — 3–6 bullets.
7. `## Sources` — linked primary sources (also in the front-matter `sources`).

Right after the H1: one plain intro paragraph (no bold, no list, no heading) — it becomes the summary.
A `> [!NOTE]` in Core ideas says, in plain sentences, which ideas are stable and which details (software versions, prices, regulations) will go out of date and as of when.
Length: 1,200–2,200 words. Reading `minutes` ~15–25; `practice_minutes` honest (30–120).
`last_verified`: the date you verified the sources.

## 4. Hands-on sources and rules

- Python labs: `labs/module-NN/*.py` or `.ipynb`, small, runnable with `labs/common/requirements.txt`, data as small CSV in the lab folder (generated or public-domain; cite the source). Never large binaries.
- Real spectra: link SDBS / NIST WebBook pages and tell the learner which compound number to look up; do not copy SDBS data into the repo (their terms forbid redistribution). NIST WebBook data may be used with citation (US government work) — still keep files small.
- Home experiments: only the ones listed in `plan.md` or equally safe kitchen/pharmacy ones. Never mix bleach with acids or ammonia; small amounts, good airflow, eye protection (ordinary safety glasses), no heating flammables, no lab reagents. Israel: Hazardous Substances Law 1993 — do not buy lab reagents.
- No content that instructs synthesis of controlled substances, explosives, toxic gases or weapons. Virtual syntheses stay in the classic teaching set (aspirin, SN1/SN2, Grignard, aldol, esterification).

## 5. Modules (Technion mapping, focus, practical piece, simulations)

Simulation names are fixed (folder `simulations/<name>/`). Lesson writers link them with presets; the simulation agents build them later and support every preset linked. Choose preset names from the list, or add a new short kebab-case one and list it in your report.

| M | Title | Technion | Focus and practical piece | Simulations (presets) |
|---|---|---|---|---|
| 1 | Orientation, Units and Safe Practice | — | Study method, the honest scope, SI and sig figs, notebook and report, GHS/SDS reading, Israeli law, home kit. Practical: first measurement — density of water/sugar solutions with kitchen scale + syringe, with uncertainty. | measurement-error (`repeat`, `bias`) |
| 2 | Calculus for Chemists | 01040003/4 | exp/log (Arrhenius, pH, decay), derivatives as rates, integrals (work, heat, half-life), Taylor approximations (small-x in equilibria), partials (thermo). Practical: Python numeric differentiation/integration of a real cooling curve. | — |
| 3 | Linear Algebra and Differential Equations | 01040019, 01040131 | Linear systems (balancing equations, mixture analysis), eigenproblems (Hückel, normal modes), first-order ODE (rate laws), oscillators, consecutive A→B→C. Practical: solve A→B→C analytically and numerically. | kinetics (`first-order`, `consecutive`), oscillators (`single`, `damped`) |
| 4 | Physics for Chemists | 01140077, 01140052 | Energy, oscillations, Coulomb, potential, circuits, EM spectrum and photons. Practical: phyphox pendulum/spring + a resistor network with a multimeter. | oscillators (`single`), rlc (`dc`) |
| 5 | Python for Scientists | 02340128 | Setup (pinned), numpy/matplotlib, curve_fit with uncertainty, reading CSV/JCAMP-DX spectra, reproducible notebooks. Practical: straight-line fit with error, as in plan 1.7. | — |
| 6 | Biology for Chemists | 01340127 | Cells, proteins, DNA, metabolism/ATP — chemistry lens. Practical: PDB/UniProt exploration, count H-bonds in a structure (Mol* viewer), ATP free-energy calculation. | — |
| 7 | Foundations of Chemistry A | 01240117 | Atoms, periodic trends, bonding, VSEPR, stoichiometry, gases. Lab lesson = S1. | glassware (`weighing`, `dilution`, `parallax`), gas-laws (`ideal`, `real`) |
| 8 | Foundations of Chemistry B | 01240118 | Thermochem, entropy/G, equilibrium, acid–base, redox, Nernst. Lab lesson = S2 + red-cabbage indicator. | calorimetry (`coffee-cup`), titration (`strong-acid`) |
| 9 | Analytical Chemistry 1 | 01240220 | Error types, statistics, propagation, calibration and LOD, titration curves, buffers and gravimetry (Harvey, LibreTexts). Practical: full calibration + LOD in Python. | measurement-error (`repeat`, `bias`, `propagation`), titration (`weak-acid`, `buffer`) |
| 10 | Analytical Chemistry Lab 1 | 01240212 | S3: 11 experiments covered across the lessons; last lesson is the home vinegar titration project (5 repeats, mean, SD, CI). | titration (`indicator-choice`, `potentiometric`, `redox`, `precipitation`, `edta`), gravimetry (`precipitate`, `electrogravimetry`, `coulometry`) |
| 11 | Scientific English | 03240033 | Reading papers, judging sources, writing the report. Practical: summarise a real open-access paper; rewrite a bad figure. | — |
| 12 | Quantum Theory in Chemistry | 01240408 | MIT 5.61 scope. Practical: numerical Schrödinger solver in Python (finite differences). | quantum-box (`box`, `tunnel`, `oscillator`, `rotor`) |
| 13 | Chemical Thermodynamics | 01240415 | MIT 5.60 scope. Practical: build a phase diagram / compute K from NIST ΔfH and S° data. | calorimetry (`bomb`), gas-laws (`real`) |
| 14 | Chemical Physics Lab | 01240611 | S4 for real at home: phyphox springs, damping, Q, coupled masses, CO2 modes, FFT, RLC resonance project (battery/USB only). | oscillators (`damped`, `coupled-three`, `co2`), rlc (`resonance`) |
| 15 | Organic Chemistry 1 | 01240708 | Yale CHEM 125 / MIT 5.12. Practical: molecular models (Avogadro or MolView), mechanism drills. | — |
| 16 | Organic Chemistry 2 | 01240711 | MIT 5.13 scope. Practical: retrosynthesis problems; final multi-step plan. | — |
| 17 | Identifying Compounds from Spectra | (part of 01240708/711) | MS, IR, 1H/13C NMR, 2D basics. Project: 50 SDBS unknowns (list of SDBS numbers + answer key in `<details>`). | nmr (`ethyl`, `isopropyl`, `second-order`, `unknown`) |
| 18 | Inorganic Chemistry | 01240305 | Main group, solids, coordination, CFT/LFT, colour & magnetism. Practical: predict colour/spin; lattice energy Born–Haber in Python. | — |
| 19 | Analytical Chemistry 2 | 01240213 | UV-Vis, fluorescence, AAS/ICP, extraction, GC/LC theory, CV. Practical: van Deemter fit, calibration. | spectrometer (`beer-lambert`, `stray-light`), chromatography (`gc`, `van-deemter`), voltammetry (`reversible`) |
| 20 | Molecular Spectroscopy and Symmetry | 01240417 | Selection rules, rot, vib, Raman, electronic, point groups, character tables. Practical: assign HCl/CO from NIST; point groups of 10 molecules. | ir-esr (`hcl`) |
| 21 | Statistical Thermodynamics | 01240413 | MIT 5.62. Practical: compute q and K for a real gas-phase equilibrium from spectroscopic constants. | boltzmann (`two-level`, `ladder`, `rotor`) |
| 22 | Chemical Kinetics | 01240414 | Rate laws, methods, mechanisms/SSA, Arrhenius/TST, catalysis. Practical: fit real kinetic data. | kinetics (`first-order`, `second-order`, `consecutive`, `arrhenius`) |
| 23 | Physical Chemistry Lab 1 | 01240610 | S5: one lesson per topic with sim + home experiment from plan.md. | gas-laws (`kinetic`), calorimetry (`neutralisation`, `dissolution`), spectrometer (`equilibrium`), kinetics (`dye-fading`) |
| 24 | Organic Chemistry Lab 1 | 01240911 (+S9 01240912) | S6 virtual bench, MIT 5.301 videos, home alum recrystallisation and paper chromatography; last lesson = S9 multi-step with spectra. | organic-bench (`techniques`, `aspirin`, `sn2`, `grignard`, `aldol`, `multistep`) |
| 25 | Analytical Chemistry Lab 2 | 01240214 | S7 instrument sims, phone spectrometer, tonic-water fluorescence, GC-MS against NIST. | spectrometer (`mixture`, `fluorescence`, `aas`), chromatography (`gc`, `temperature-program`, `hplc`, `overlap`), voltammetry (`scan-rate`, `quasi`) |
| 26 | Bio-inorganic Chemistry | 01240210 | Metals in biology, O2 binding (Hill), metalloenzymes, ET. Practical: fit an O2 saturation curve. | — |
| 27 | Electromagnetism and Matter | 01240416 | Maxwell, multipoles, polarisability, dielectrics, intermolecular forces. Practical: compute dipole/quadrupole from charges; Clausius–Mossotti with real data. | — |
| 28 | Structure and Reactivity | 01240703 | PES, Hammond, Hammett, intermediates, KIE. Practical: Hammett plot from published rate data. | — |
| 29 | Biochemistry and Enzymology | 01340019 | MIT 5.07SC. Practical: Michaelis–Menten fit (nonlinear vs Lineweaver–Burk), inhibition type. | kinetics (`enzyme`) |
| 30 | Physical Chemistry Lab 2 | 01240613 | S8: HCl rovib, ESR hyperfine, speed of sound → γ of air at home, dye particle-in-a-box. | ir-esr (`hcl`, `esr-methyl`, `esr-hydrogen`), quantum-box (`dye`) |
| 31 | Computational Chemistry Lab | 01260603 | S10 done for real: Avogadro, xtb, ORCA (verify licence and current versions). Practical: compare calculated vs measured IR. | — |
| 32 | Electives: Electrochemistry and Solid State | 01270453, 01270427 | Butler–Volmer, batteries, corrosion, XRD, bands; last lesson points to the other electives. Practical: Tafel fit; index a powder pattern. | voltammetry (`butler-volmer`) |
| 33 | Research Project | 01240353 (S11) | 180-hour home project; report + poster. Project briefs in `projects/`. | — |

## 6. Quizzes

Per the Academy instructions §5: lesson quiz 3–5, module quiz 8–10 scenario questions, 4 options, one correct, `correct` spread 0–3, plausible distractors of similar length, `>-` block scalars, explanation that teaches. Numeric chemistry questions are fine as MCQ: distractors are the answers from the typical mistakes (wrong units, forgot stoichiometric factor, ln vs log10, sign error).

## 7. Shared files (main session only)

`_sidebar.md` (generated by `scripts/manifest.py`), `README.md`, `COURSE-MAP.md`, `glossary.md`, `references/`, `templates/`, `labs/common/`, `simulations/common/`, `simulations/README.md` (sim agents may add their rows), `BUILD_PROGRESS.md`, `TODO_FOR_TAL.md`.

Templates already planned (main session writes them; lessons may link): `templates/lab-report.md`, `templates/notebook-page.md`, `templates/error-analysis.md`, `templates/spectrum-assignment.md`, `templates/research-proposal.md`. If a module needs another template, write it to `curriculum/template-inbox/<name>.md` and say so in the report.
