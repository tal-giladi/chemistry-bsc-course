# Module 18 labs — Inorganic Chemistry

Python exercises for periodic trends, lattice energies, isomer counting, crystal-field theory and the module practical (decoding nine complexes from colour and magnetism), plus two kitchen activities. Each exercise file has functions marked TODO; the matching `*_solution.py` file is the reference solution. No lab reagents are used anywhere in this module.

Setup (once, Python 3.14, packages pinned in `labs/common/requirements.txt`; checked 2026-10-17):

```bash
py -3.14 -m venv .venv
.venv\Scripts\python -m pip install -r labs/common/requirements.txt
```

On macOS or Linux use `python3.14` and `.venv/bin/python`. These labs need only numpy and matplotlib. Run each file from this folder, for example `py lesson01_trends.py`. Plots are saved to `runs/` (not tracked by git).

| Lesson | Exercise | Solution | Data |
|---|---|---|---|
| 18.1 Slater's rules against NIST ionisation energies | `lesson01_trends.py` | `lesson01_trends_solution.py` | `ionization_energies.csv` |
| 18.2 Born–Haber cycles, Born–Mayer and Kapustinskii | `lesson02_born_haber.py` | `lesson02_born_haber_solution.py` | `born_haber.csv` |
| 18.3 Counting isomers of octahedral complexes | `lesson03_isomers.py` | `lesson03_isomers_solution.py` | none; optional ligand list, e.g. `py lesson03_isomers.py en en B B` |
| 18.4 CFSE and the high/low-spin decision | `lesson04_cfse.py` | `lesson04_cfse_solution.py` | `complexes.csv`; optional pairing-energy factor, e.g. `py lesson04_cfse.py 1.0` |
| 18.5 Module practical: nine complex cards | `lesson05_practical.py` | `lesson05_practical_solution.py` | `cards.csv` |

`inorg18.py` is the shared helper: CODATA 2022 constants, electron configurations up to krypton (with the Cr and Cu exceptions), the 24 rotations and 48 symmetry operations of an octahedron as permutations of its corners, d-electron counting, the visible colour bands and the spin-only formula. You do not need to edit it.

## Kitchen activities

- Lesson 18.1: red-cabbage indicator with milk of magnesia, exhaled CO₂ and baking soda (acidic and basic oxides).
- Lesson 18.3: one iron supplement tablet (ferrous sulfate or fumarate) in strong black tea, then lemon juice (iron–polyphenol chelates and ligand competition).

Read the CAUTION box in each lesson first. Iron tablets are dangerous to young children: use one tablet, keep the pack out of reach and pour the test liquids away.

## Data and sources

- `ionization_energies.csv`: a copy of the Module 7 file, first to third ionisation energies of H to Kr from the NIST Atomic Spectra Database (https://physics.nist.gov/PhysRefData/ASD/ionEnergy.html), retrieved 2026-10-16. US government work.
- `born_haber.csv`: formation enthalpies of the solids from the NIST Chemistry WebBook (NIST-JANAF tables, Chase 1998; CODATA review values for MgO and CaO); gas-phase atom formation enthalpies from the CODATA Key Values (https://www.codata.info/resources/databases/key1.html); electron affinities from the primary measurements listed on the Wikipedia electron affinity data page; lattice constants from the Wikipedia lattice-constant table and calcium fluoride article; Madelung constants from the Wikipedia Madelung constant article; Shannon (1976) radii. All retrieved 2026-10-17. Details in the file header.
- `complexes.csv`: octahedral and tetrahedral splittings from a university crystal-field lecture table (University of Mustansiriyah; values agree with OpenStax Chemistry 2e 19.3 where they overlap) and free-ion pairing energies from LibreTexts, retrieved 2026-10-17. Details in the file header.
- `cards.csv`: absorption maxima and colours from OpenStax Chemistry 2e 19.3 and the lesson 18.4 splittings; band-intensity classes from LibreTexts (selection rules); magnetic moments are the mid-points of the observed ranges in LibreTexts, Magnetic Moments of Transition Metals. Details in the file header.
- Constants: CODATA 2022 via NIST (https://physics.nist.gov/cuu/Constants/).

## What these labs do not train

They do not measure anything: no Gouy balance, no spectrometer, no synthesis. The models are the textbook ones (Slater's rules, ionic lattice models, crystal-field theory with a rule-of-thumb pairing energy), and the lessons say where each one fails.
