# Module 17 plan — Identifying Compounds from Spectra

Technion: the spectroscopy parts of 01240708 Organic Chemistry 1 and 01240711 Organic Chemistry 2. Depth: OpenStax Organic Chemistry (McMurry, 2023) chapters 12 (MS, IR) and 13 (NMR), Reich's NMR pages (organicchemistrydata.org) for shift and coupling data.
Simulation: `nmr` with presets `ethyl`, `isopropyl`, `second-order` (17.3) and `unknown` (17.5). Built later.
Real spectra: SDBS (AIST) for ¹H, ¹³C and condensed-phase IR; NIST Chemistry WebBook for EI mass spectra and gas-phase IR.
SDBS decision (2026-10-17): SDBS asks every user to accept its disclaimer before each use and forbids robot collection, so SDBS numbers were not fetched or verified. Every compound is given by name + CAS (CAS checked against PubChem and NIST WebBook); learners search SDBS by compound name (SDBS has no CAS search; its help page says so). The only SDBS number quoted is toluene = 97, which AIST's own help page uses as its URL example; even that is not needed by any exercise. No SDBS data is copied into the repo.
Hands-on: Python labs in `labs/module-17/` (numpy, matplotlib, RDKit 2026.9.1): isotope patterns and exact masses, Hooke's-law band positions and a band classifier, a first-order ¹H multiplet simulator, ¹³C symmetry and DEPT from RDKit symmetry classes, a candidate filter, and the project answer checker (hashed key). Template: `templates/spectrum-assignment.md`.
Module practical: 17.6, 50 unknowns in three tiers (MS + IR from NIST by CAS, ¹H/¹³C from SDBS by name), answers in `<details>`, checker `lesson06_project.py`.

| Lesson | Objectives (short) | Prerequisites | Hands-on | Sources to verify |
|---|---|---|---|---|
| 17.1 Mass spectrometry | M⁺·, base peak; nitrogen rule; DBE; M+1 → C count, M+2 for Cl/Br; HRMS formula; α-cleavage, McLafferty, 91/105/77 | 15.1, 07.1, 05.4 | `lesson01_ms.py` (exact mass, isotope pattern, HRMS match); NIST EI spectra of 2-hexanone, 1-bromopropane, butylbenzene, diethylamine | OpenStax 12.1–12.3; NIST isotopic compositions; NIST WebBook |
| 17.2 IR | Hooke's law and reduced mass; the four regions; C=O by class; O–H/N–H shapes; gas vs condensed phase | 17.1, 12.4, 14.4 | `lesson02_ir.py` (wavenumbers from k; band classifier on six described spectra); NIST IR of 2-hexanone, butanoic acid, propanenitrile, 1-octyne; SDBS IR of 1-butanol | OpenStax 12.7, 12.8; NIST WebBook |
| 17.3 ¹H NMR | shielding and δ; shift ranges; integration; n+1, J, Pascal; equivalence; OH/NH exchange; second order when Δν/J small | 17.2, 12.5 | `nmr` sim (ethyl, isopropyl, second-order); `lesson03_nmr1h.py` (first-order simulator, equivalence count); SDBS ¹H of bromoethane, 2-chloropropane, 1-nitropropane | OpenStax 13.2–13.8; Reich |
| 17.4 ¹³C and 2D | ¹³C ranges; signal count from symmetry; DEPT; COSY, HSQC, HMBC questions | 17.3 | `lesson04_c13.py` (RDKit symmetry classes, DEPT filter of C4H10O and C6H4Cl2 isomers); SDBS ¹³C of 2-butanol, MTBE, dichlorobenzenes | OpenStax 13.10–13.13; Reich |
| 17.5 Putting it together | the workflow: formula → DBE → MS → IR → ¹³C → ¹H → candidates → check; ranking evidence | 17.4, 16.3 | worked unknown (4'-methoxyacetophenone); `lesson05_solver.py` (candidate filter, C5H10O2 esters); `nmr` sim (unknown); five practice unknowns | OpenStax 7.2, 13.13; NIST, SDBS |
| 17.6 Project: 50 unknowns | solve 50 unknowns with the template; record evidence; self-check | 17.5 | project with three tiers; `lesson06_project.py` checker | NIST WebBook (50 CAS checked), PubChem |

Links back: 15.1 (functional groups, SMILES), 07.1 (isotopes), 12.4 (harmonic oscillator), 12.5 (spin/angular momentum), 14.4 (CO₂ modes), 14.5 (Fourier transform), 05.4 (reading instrument data, JCAMP-DX), 16.1–16.6 (functional groups met in the unknowns). Forward: 19 (UV-Vis), 20 (selection rules, symmetry), 24 (organic lab with product spectra), 25 (GC-MS), 31 (calculated IR).
Safety: no reagents, no experiments; all spectra are database records.
