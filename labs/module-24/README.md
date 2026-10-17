# Module 24 labs — Organic Chemistry Lab 1

The organic lab itself cannot be done at home: it needs organic solvents, corrosive reagents and a fume hood. These files support the parts that can: Python exercises that plan and analyse the work of the virtual bench (`organic-bench` simulation), and two kitchen experiments with data templates. Each exercise file has functions marked TODO; the matching `*_solution.py` file is the reference solution.

Setup (once, Python 3.14, packages pinned in `labs/common/requirements.txt`; checked 2026-10-17):

```bash
py -3.14 -m venv .venv
.venv\Scripts\python -m pip install -r labs/common/requirements.txt
```

On macOS or Linux use `python3.14` and `.venv/bin/python`. These labs need numpy, scipy, matplotlib and rdkit (for molar masses from SMILES). Run each file from this folder, for example `py lesson01_extraction.py`. Plots are saved to `runs/` (not tracked by git). `py org24.py` prints a short self-check.

| Lesson | Exercise | Solution | Data |
|---|---|---|---|
| 24.1 Extraction planning: multiple extractions, acid–base work-up | `lesson01_extraction.py` | `lesson01_extraction_solution.py` | pKa and log Kow in `org24.py` |
| 24.2 Recrystallisation recovery; cyclohexane–toluene T–x–y and plates | `lesson02_purification.py` | `lesson02_purification_solution.py` | Antoine constants in `org24.py`; your `alum_recrystallisation.csv` |
| 24.3 Rf values; ideal melting-point depression of benzoic acid | `lesson03_purity.py` | `lesson03_purity_solution.py` | `chromatogram_template.csv` or your `chromatogram.csv` |
| 24.4 Aspirin: limiting reagent, yield, atom economy, verdicts | `lesson04_aspirin.py` | `lesson04_aspirin_solution.py` | runs in the script (replace with yours) |
| 24.5 SN2, Grignard and aldol amounts; Grignard water budget | `lesson05_reactions.py` | `lesson05_reactions_solution.py` | densities in the script |
| 24.6 Module practical: check every step of a three-step synthesis | `lesson06_practical.py` | `lesson06_practical_solution.py` | `multistep_observations.csv` (replace with yours) |

Shared file you do not need to edit: `org24.py` — compound names with SMILES and literature melting points, NIST Antoine constants, benzoic acid fusion data, acid pKa and log Kow values, the CODATA gas constant, a CSV reader and `molar_mass()`.

## Kitchen activities

- Lesson 24.1: oil, water, food colouring and turmeric in a closed jar (partition and emulsions).
- Lesson 24.2: recrystallise potassium alum (pharmacy or spice shop) or table sugar from hot water. Copy `alum_recrystallisation_template.csv` to `alum_recrystallisation.csv`, enter your runs and rerun `lesson02_purification.py`.
- Lesson 24.3: paper chromatography of food colourings and water-based markers with salt water. Copy `chromatogram_template.csv` to `chromatogram.csv`, enter your distances and rerun `lesson03_purity.py`.

Read the WARNING and CAUTION boxes in the lessons first: kitchen materials only, no solvents (no nail-polish remover, no rubbing alcohol), kettle water poured by an adult with an oven glove into a heat-proof jar, safety glasses, nothing tasted, crystals kept away from children.

## Data and sources

All values retrieved 2026-10-17.

- Melting points, solubilities, densities, pKa and log Kow: PubChem compound pages (aspirin CID 2244, salicylic acid 338, acetic anhydride 7918, potassium alum 24856, sucrose 5988, acetanilide 904, benzoic acid 243, benzilic acid 6463, benzoin 8400, 1-butanol 263, 1-bromobutane 8002, bromobenzene 7961, benzaldehyde 240, acetone 180). Benzil and triphenylmethanol melting points from the NIST Chemistry WebBook phase-change pages; dibenzalacetone (trans,trans) 110–111 °C from teaching-lab literature.
- Antoine constants: NIST Chemistry WebBook, cyclohexane (https://webbook.nist.gov/cgi/cbook.cgi?ID=C110827&Mask=4) and toluene (https://webbook.nist.gov/cgi/cbook.cgi?ID=C108883&Mask=4), both from Williamham, Taylor et al. (1945). The cyclohexane fit covers 293–355 K, so the toluene-rich end of the diagram extrapolates slightly. US government work.
- Benzoic acid: Tfus 395.52 K and ΔfusH 18.006 kJ/mol (Ginnings and Furukawa 1953), NIST Chemistry WebBook.
- `chromatogram_template.csv` and the runs in `lesson04_aspirin.py`: invented example values to show the format.
- `multistep_observations.csv`: illustrative bench observations written for lesson 24.6, consistent with literature band positions (OpenStax Organic Chemistry 12.8, 13.4) and melting points. They are not measured spectra. No SDBS data are copied into this folder; look up real spectra in SDBS by compound name and in the NIST WebBook.
- Gas constant: CODATA 2022 via NIST (exact).

## What these labs do not train

They do not train bench hands: assembling a reflux, using a separatory funnel, vacuum filtration, running a real TLC plate under UV, or operating a melting-point apparatus or an NMR. They do not train handling of corrosive, flammable and toxic reagents or chemical waste disposal. The kitchen experiments train solubility, crystallisation and partition at kitchen level only. An employer or a university lab would still have to train you at the bench.
