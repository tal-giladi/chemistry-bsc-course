# Module 20 labs — Molecular Spectroscopy and Symmetry

Python exercises that work on real NIST data: populations and line widths, the CO microwave spectrum, the HCl infrared band, Franck–Condon factors of iodine, a symmetry-element finder and the reduction formula. Each exercise file has functions marked TODO; the matching `*_solution.py` file is the reference solution. No chemicals are used anywhere in this module.

Setup (once, Python 3.14, packages pinned in `labs/common/requirements.txt`; checked 2026-10-17):

```bash
py -3.14 -m venv .venv
.venv\Scripts\python -m pip install -r labs/common/requirements.txt
```

On macOS or Linux use `python3.14` and `.venv/bin/python`. These labs need only numpy, scipy and matplotlib. Run each file from this folder, for example `py lesson02_rotor.py`. Plots are saved to `runs/` (not tracked by git).

| Lesson | Exercise | Solution | Data |
|---|---|---|---|
| 20.1 Populations, Einstein A/B, Doppler widths | `lesson01_light.py` | `lesson01_light_solution.py` | constants in `spec20.py` |
| 20.2 Fit the CO microwave lines | `lesson02_rotor.py` | `lesson02_rotor_solution.py` | `co_rotational_lines.csv` |
| 20.3 Assign and fit the HCl infrared band; rotational Raman | `lesson03_hcl_band.py` | `lesson03_hcl_band_solution.py` | `hcl_band_peaks.csv` |
| 20.4 Franck–Condon factors and Birge–Sponer for I₂ | `lesson04_franck_condon.py` | `lesson04_franck_condon_solution.py` | constants in `spec20.py` |
| 20.5 Point groups from 3D coordinates | `lesson05_pointgroups.py` | `lesson05_pointgroups_solution.py` | `molecules20.py` |
| 20.6 Module practical (HCl and CO, ten point groups, band counts) | `lesson06_practical.py` | `lesson06_practical_solution.py` | all of the above and `nist_fundamentals.csv` |

The module practical imports your own functions from lessons 20.2, 20.3 and 20.5, so finish those first. `py lesson05_pointgroups.py practical` runs the point-group finder on the ten practical molecules.

Shared files you do not need to edit:

- `spec20.py`: CODATA 2022 constants, NIST atomic masses, NIST WebBook constants of HCl, CO, N₂ and I₂ (X and B states), term values, a finite-difference Schrödinger solver for Morse wavefunctions, the symmetry-element finder and the character tables of C2v, C3v, C2h, D2h, D3h, Td, D4h and Oh (`py spec20.py` checks their orthogonality).
- `molecules20.py`: idealised geometries of the 18 molecules used in lessons 20.5 and 20.6.

## Kitchen activities

- Lesson 20.4 (optional): a highlighter in a glass of water under a phone torch, to see fluorescence and the Stokes shift.
- Lesson 20.5: molecular models from toothpicks and grapes or modelling clay.

Read the CAUTION box in each lesson first: no UV lamps or lasers, do not drink the highlighter water, keep toothpicks away from small children.

## Data and sources

- `co_rotational_lines.csv`: 31 ¹²C¹⁶O and 9 ¹³C¹⁶O pure rotational lines (v = 0) from the NIST Diatomic Spectral Database, SRD 114 (https://physics.nist.gov/cgi-bin/MolSpec/diperiodic.pl), retrieved 2026-10-17. US government work.
- `hcl_band_peaks.csv`: the 20 absorption maxima of the HCl fundamental, located by the author in the JCAMP-DX data of the NIST WebBook gas-phase spectrum (Coblentz Society No. 8758, 4 cm⁻¹ resolution; https://webbook.nist.gov/cgi/cbook.cgi?ID=C7647010&Mask=80), retrieved 2026-10-17. Only peak positions are stored, not the spectrum.
- `nist_fundamentals.csv`: fundamental frequencies and symmetry species of H₂O, NH₃, CH₄, CCl₄, C₂H₄ and trans-1,2-dichloroethene from the NIST WebBook vibrational tables (Shimanouchi, NSRDS-NBS 39, 1972), retrieved 2026-10-17.
- Diatomic constants in `spec20.py`: NIST Chemistry WebBook, constants of diatomic molecules (https://webbook.nist.gov/chemistry/), retrieved 2026-10-17.
- Constants: CODATA 2022 via NIST (https://physics.nist.gov/cuu/Constants/); isotope masses from NIST Atomic Weights and Isotopic Compositions.
- The CO branch maxima (2119.5 and 2176 cm⁻¹) in `lesson06_practical.py` were read from the NIST CO spectrum (Coblentz No. 8755).

## What these labs do not train

They do not run a spectrometer: no sample cells, no alignment, no calibration, no baseline correction. The HCl data are a digitised 1964 chart, so your constants will be about 1 % off; Module 30 repeats the analysis with a modern spectrum and the ir-esr simulation. The Morse model of I₂ and the idealised geometries are approximations chosen to show the principles.
