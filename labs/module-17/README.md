# Module 17 labs — Identifying Compounds from Spectra

Small Python exercises, one per lesson, plus the answer checker for the 50-unknown project. They compute what spectra can tell you from a formula or a structure: exact masses and isotope patterns, IR band positions from Hooke's law, first-order ¹H multiplets, ¹³C signal counts and DEPT types from molecular symmetry (RDKit), and a candidate filter. Each exercise file has parts marked TODO; the matching `*_solution.py` file is the reference solution. Plots are written to `runs/` in this folder (ignored by git).

Setup (once, Python 3.14, packages pinned in `labs/common/requirements.txt`; checked 2026-10-17 with RDKit 2026.9.1, numpy 2.5 and matplotlib 3.11):

```bash
py -3.14 -m venv .venv
.venv\Scripts\python -m pip install -r labs/common/requirements.txt
```

On macOS or Linux use `python3.14` and `.venv/bin/python`. Run each file from this folder, for example `py lesson01_ms.py`. Keep `spec17.py` in the same folder.

| Lesson | Exercise | Solution | Data |
|---|---|---|---|
| 17.1 Mass spectrometry | `lesson01_ms.py` | `lesson01_ms_solution.py` | isotope table in `spec17.py` |
| 17.2 Infrared | `lesson02_ir.py` | `lesson02_ir_solution.py` | six described spectra in the code |
| 17.3 Proton NMR | `lesson03_nmr1h.py` | `lesson03_nmr1h_solution.py` | approximate shifts and J in the code |
| 17.4 Carbon NMR and DEPT | `lesson04_c13.py` | `lesson04_c13_solution.py` | isomer SMILES in the code |
| 17.5 Solving unknowns | `lesson05_solver.py` | `lesson05_solver_solution.py` | `candidates.csv` |
| 17.6 Project: 50 unknowns | `lesson06_project.py` + `project_answers.csv` | `lesson06_project_solution.py` | `unknowns.csv` |

Shared: `spec17.py` holds the isotope masses and abundances, a formula parser, a small CSV reader and `canon()` for canonical SMILES.

The project checker stores only hashes of the canonical answers, so running it does not reveal them. The hashes depend on how RDKit writes canonical SMILES; with an RDKit version other than 2026.9.1 a correct answer could be reported as wrong. If that happens, compare with `py lesson06_project_solution.py`.

## Real spectra

No spectra are stored in this folder. The lessons link to them:

- NIST Chemistry WebBook (https://webbook.nist.gov/chemistry/), a US government database: EI mass spectra (`&Mask=200`) and mostly gas-phase IR spectra (`&Mask=80`), opened by CAS number as `cbook.cgi?ID=C<CAS without dashes>`.
- SDBS (https://sdbs.db.aist.go.jp/), AIST Japan: ¹H and ¹³C NMR and liquid or solid IR. SDBS asks you to accept its disclaimer at each visit, forbids automated downloading, and asks users to cite "SDBS, https://sdbs.db.aist.go.jp/, National Institute of Advanced Industrial Science and Technology, date of access". Search it by compound name or formula; it has no CAS search. Do not copy SDBS data into files you share.

## Data

- `unknowns.csv`: number, molecular formula and CAS number of the 50 project unknowns. CAS numbers and formulas were taken from PubChem and checked against the NIST WebBook entry for each CAS number on 2026-10-17.
- `candidates.csv`: the 13 C₅H₁₀O₂ esters and acids for lesson 17.5, written by hand as SMILES. No spectral data.
- `project_answers.csv`: your answers (SMILES), empty to start.
- Isotope masses and abundances in `spec17.py`: NIST, Atomic Weights and Isotopic Compositions (https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl), checked 2026-10-17. Electron mass and atomic mass constant: CODATA 2022.
- Shifts, coupling constants and force constants inside the scripts are rounded textbook values for teaching (OpenStax Organic Chemistry, 2023, chapters 12–13), not database records.
