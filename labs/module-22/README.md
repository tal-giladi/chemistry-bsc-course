# Module 22 labs — Chemical Kinetics

Python exercises on real published kinetic data: the 1913 Michaelis–Menten invertase measurements (time courses, raw polarimeter readings and initial rates) and evaluated gas-phase rate constants from the NIST Chemical Kinetics Database (OH + CH₄, N₂O₅, 2NO + O₂). Each exercise file has functions marked TODO; the matching `*_solution.py` file is the reference solution. Two lessons add a kitchen experiment (no lab reagents).

Setup (once, Python 3.14, packages pinned in `labs/common/requirements.txt`; checked 2026-10-17):

```bash
py -3.14 -m venv .venv
.venv\Scripts\python -m pip install -r labs/common/requirements.txt
```

On macOS or Linux use `python3.14` and `.venv/bin/python`. These labs need only numpy, scipy and matplotlib. Run each file from this folder, for example `py lesson01_orders.py`. Plots are saved to `runs/` (not tracked by git). `py kin22.py` prints a short self-check of the constants.

| Lesson | Exercise | Solution | Data |
|---|---|---|---|
| 22.1 Order of the invertase reaction; methane lifetime | `lesson01_orders.py` | `lesson01_orders_solution.py` | `invertase_timecourse.csv` |
| 22.2 Polarimeter readings, endpoints, initial rates, local orders | `lesson02_methods.py` | `lesson02_methods_solution.py` | `invertase_rotation.csv`, `invertase_initial_rates.csv` |
| 22.3 Steady-state test, Lindemann falloff of N₂O₅, 2NO + O₂ | `lesson03_mechanisms.py` | `lesson03_mechanisms_solution.py` | constants in `kin22.py` |
| 22.4 Arrhenius and Eyring fits; your tablet data | `lesson04_arrhenius.py` | `lesson04_arrhenius_solution.py` | `oh_ch4_k.csv`, `tablet_times_template.csv` |
| 22.5 Module practical: Michaelis–Menten and global time-course fit | `lesson05_practical.py` | `lesson05_practical_solution.py` | `invertase_initial_rates.csv`, `invertase_timecourse.csv` |

Shared file you do not need to edit: `kin22.py` — CODATA 2022 constants, the NIST SRD 17 rate parameters used in lessons 22.1, 22.3 and 22.4, the Michaelis–Menten dissociation constants, a CSV reader and the modified Arrhenius function $k = A(T/298)^n e^{-E_a/RT}$.

## Kitchen activities

- Lesson 22.4: an effervescent tablet dissolving in water at four temperatures. Copy `tablet_times_template.csv` to `tablet_times.csv`, enter your runs and rerun `lesson04_arrhenius.py`.
- Lesson 22.5: dry baker's yeast with 3 % pharmacy hydrogen peroxide and a drop of washing-up liquid.

Read the WARNING and CAUTION boxes in the lessons first: hot tap water no hotter than about 50 °C, do not drink the solutions, only 3 % hydrogen peroxide and never mixed with anything else, safety glasses, work at a sink.

## Data and sources

- `invertase_timecourse.csv`: fraction of sucrose converted against time at 333, 166.7, 83, 41.6 and 20.8 mM, from Michaelis and Menten, Biochem. Z. 49, 333 (1913), as tabulated in Johnson and Goody, Biochemistry 50, 8264 (2011), Table 1 (https://pmc.ncbi.nlm.nih.gov/articles/PMC3381512/), retrieved 2026-10-17. The column `used_in_MM_constant` is 0 for the three values Michaelis and Menten left out of their average (bracketed in the table).
- `invertase_rotation.csv`: corrected polarimeter angles of experiments 1 (0.333 M) and 5 (0.0208 M) of Table I of the 1913 paper, from the Johnson and Goody translation (Supporting Information). The start values at t = 0 are the authors' extrapolations. Theoretical total changes for complete inversion: 18.57° (experiment 1) and 1.190° (experiment 5). Experiment 5 is included up to 95 min.
- `invertase_initial_rates.csv`: the seven initial rates of Table I in the paper's arbitrary units (proportional to degrees of rotation lost per minute).
- `oh_ch4_k.csv`: CH₄ + OH → CH₃ + H₂O rate constants from two experimental studies in the NIST Chemical Kinetics Database, SRD 17, Data Version 2026 (https://kinetics.nist.gov/kinetics/), retrieved 2026-10-17: Gierczak et al., J. Phys. Chem. A 101, 3125 (1997), 196–420 K, and Srinivasan et al., J. Phys. Chem. A 109, 1857 (2005), 840–2000 K. The values are computed from each study's fitted expression (the tables NIST prints, plus four values computed by the author from the same expression above 1200 K), not raw individual measurements. US government work.
- Rate parameters in `kin22.py`: N₂O₅ → NO₂ + NO₃ high- and low-pressure limits (IUPAC 1997 evaluation), 2NO + O₂ → 2NO₂ (IUPAC 2004) and OH + CH₄ (JPL 1997 evaluation), all as listed in NIST SRD 17.
- Michaelis–Menten dissociation constants: sucrose 0.0167 M, fructose 0.058 M, glucose 0.089 M (1913 paper, summary table, in the Johnson and Goody translation).
- Constants: CODATA 2022 via NIST (https://physics.nist.gov/cuu/Constants/).

## What these labs do not train

They do not run an instrument: no polarimeter, no stopped flow, no flash photolysis, no temperature control. The invertase data are a century old and were read by hand; the OH + CH₄ values are smooth fitted curves, so their fit uncertainties are unrealistically small. The kitchen experiments train reasoning about rates, not quantitative technique. Module 23 (lesson 23.4) follows a reaction quantitatively at home with a phone camera.
