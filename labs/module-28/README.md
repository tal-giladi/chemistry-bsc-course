# Module 28 labs — Structure and Reactivity in Organic Chemistry

Python exercises on a model potential energy surface and on published physical-organic data: C–H bond enthalpies, halogenation product ratios, Hammett substituent constants, evaluated aqueous pKa values from the IUPAC Digitized pKa Dataset, and the 2025 rate constants and isotope effects for an azo coupling. Each exercise file has functions marked TODO; the matching `*_solution.py` file is the reference solution. This module has no home experiment: nothing in it can be measured safely in a kitchen with useful precision.

Setup (once, Python 3.14, packages pinned in `labs/common/requirements.txt`; checked 2026-10-17):

```bash
py -3.14 -m venv .venv
.venv\Scripts\python -m pip install -r labs/common/requirements.txt
```

On macOS or Linux use `python3.14` and `.venv/bin/python`. These labs need numpy, scipy and matplotlib; `fetch_iupac_pka.py` also needs RDKit (to match structures). Run each file from this folder, for example `py lesson01_pes.py`. Plots are saved to `runs/` (not tracked by git). `py sr28.py` prints a short self-check.

| Lesson | Exercise | Solution | Data |
|---|---|---|---|
| 28.1 Stationary points and minimum-energy path on the Müller–Brown surface | `lesson01_pes.py` | `lesson01_pes_solution.py` | surface defined in the script |
| 28.2 Halogenation selectivity, Leffler α, Marcus α | `lesson02_hammond.py` | `lesson02_hammond_solution.py` | bond enthalpies in `sr28.py`, propane ratios in the script |
| 28.3 σ from benzoic acids; ρ for phenols and anilinium ions | `lesson03_hammett.py` | `lesson03_hammett_solution.py` | run `fetch_iupac_pka.py` first; `sigma_hansch.csv` |
| 28.4 Radical stabilisation energies, cumyl chloride σ+, carbene spin populations | `lesson04_intermediates.py` | `lesson04_intermediates_solution.py` | `sr28.py`, `sigma_hansch.csv` |
| 28.5 Isotope effect from ZPE, radical clock, module practical (Hammett and KIE of an azo coupling) | `lesson05_practical.py` | `lesson05_practical_solution.py` | `diazonium_coupling.csv` |

Shared file you do not need to edit: `sr28.py` — CODATA 2022 constants, bond dissociation enthalpies, a CSV reader that skips `#` comment lines, the σ table loader, a straight-line fit with uncertainties and the Eyring rate constant.

## Downloading the pKa data (lesson 28.3)

```bash
py fetch_iupac_pka.py
```

This downloads `iupac_high-confidence_v2_4.csv` (about 7 MB) from the IUPAC GitHub repository into `data/downloaded/`, which git ignores, and writes `data/downloaded/aromatic_pka.csv` with one median pKa per substituted benzoic acid, phenol and anilinium ion. The selection rules (water only, 25 °C, ordinary pressure, "Reliable" values preferred over "Approximate", median) are written at the top of the script so you can change them. The dataset is not stored in the course because its licence (CC BY-NC 4.0) does not allow it.

## Data and sources

- `diazonium_coupling.csv`: second-order rate constants for 3-aminothiophene + eight para-substituted benzenediazonium ions in 50 % H₂O–50 % DMSO, 20 °C, I = 0.1 M, at pH 2 and pH 1, the free-amine constants $k_1$ and the values for 2-deuterio-3-aminothiophene, with σp and σp+. Source: R. El Abed, T. Slama, F. Mahdhaoui and T. Boubaker, ChemPhysChem 26, e202500553 (2025), Table 1, doi:10.1002/cphc.202500553, open access under CC BY 4.0 (https://pmc.ncbi.nlm.nih.gov/articles/PMC12710183/), retrieved 2026-10-17 from the PMC full text. Values copied unchanged; column names are ours.
- `sigma_hansch.csv`: σm, σp and σp+ from C. Hansch, A. Leo and R. W. Taft, Chem. Rev. 91, 165 (1991), as reproduced in the H. Zipse (LMU Munich) teaching table (https://zipse.cup.uni-muenchen.de/site/assets/files/1480/hammett_19_06_02.pdf) and in Table 1 of El Abed et al. (2025); σm of CF₃ and both values for COCH₃ from the Reusch Virtual Textbook (https://organicchemistrydata.org/reusch/virtualtext/linear-free-energy-relationships/). Checked 2026-10-17.
- IUPAC Digitized pKa Dataset v2.4 (released 2026-09-21): J. W. Zheng and O. Lafontant-Joseph, https://github.com/IUPAC/Dissociation-Constants, Zenodo doi 10.5281/zenodo.7236452. Copyright 2026 IUPAC, CC BY-NC 4.0, "Reproduced by permission of International Union of Pure and Applied Chemistry". Downloaded by the learner, not redistributed.
- Bond dissociation enthalpies in `sr28.py` (298 K): C–H values from S. J. Blanksby and G. B. Ellison, Acc. Chem. Res. 36, 255 (2003), as listed by P. G. Wenthold on Chemistry LibreTexts; H–Cl and H–Br computed from the NIST WebBook enthalpies of formation (CODATA key values: H 217.998, Cl 121.301, Br 111.87, HCl −92.31, HBr −36.29 kJ/mol).
- Propane halogenation product ratios at 25 °C (45:55 chlorination, 3:97 bromination): Chemistry LibreTexts, Morsch and Andrews, 15.06 Chlorination versus Bromination.
- Müller–Brown surface: K. Müller and L. D. Brown, Theor. Chim. Acta 53, 75 (1979); parameters as widely used in the reaction-path literature, stationary points recomputed in `lesson01_pes_solution.py`.
- Cumyl chloride ρ = −4.54: H. C. Brown and Y. Okamoto, J. Am. Chem. Soc. 80, 4979 (1958). Radical clock 1.2 × 10⁸ s⁻¹ at 37 °C: A. W. Bowry, J. Lusztyk and K. U. Ingold, J. Am. Chem. Soc. 113, 5687 (1991).
- Constants: CODATA 2022 via NIST (https://physics.nist.gov/cuu/Constants/).

## What these labs do not train

They do not run a reaction or an instrument: no stopped-flow spectrometer, no deuterium labelling, no trapping experiment, no quantum-chemistry calculation of a real transition state. The Müller–Brown surface is a two-coordinate model, not a molecule; Module 31 finds real minima and transition states with xtb and ORCA. The pKa values were measured decades ago and some are only "Approximate", which you will see as scatter in the phenol plot.
