# Module 29 labs — Biochemistry and Enzymology

Python exercises on protein stability, enzyme kinetics, inhibition, an enzyme active site and the energetics of glycolysis. Real data: the 1913 Michaelis–Menten invertase initial rates, the crystal structure of α-chymotrypsin (PDB 4CHA), and standard Gibbs energies and red-cell metabolite levels for glycolysis. Where no open measured data set teaches the point cleanly (melting curves, inhibitor series, a pH-rate profile), the data are generated from stated parameters by `make_data.py` and say so in their first lines. Each exercise file has functions marked TODO; the matching `*_solution.py` file is the reference solution. Lessons 29.1 and 29.4 add a kitchen experiment (no lab reagents).

Setup (once, Python 3.14, packages pinned in `labs/common/requirements.txt`; checked 2026-10-17):

```bash
py -3.14 -m venv .venv
.venv\Scripts\python -m pip install -r labs/common/requirements.txt
```

On macOS or Linux use `python3.14` and `.venv/bin/python`. These labs need only numpy, scipy and matplotlib; `fetch_pdb.py` uses the standard library and an internet connection. Run each file from this folder, for example `py lesson01_stability.py`. Plots are saved to `runs/` and downloaded structures to `data/downloaded/` (both ignored by git). `py enz29.py` prints a short self-check.

| Lesson | Exercise | Solution | Data |
|---|---|---|---|
| 29.1 Thermal and urea melts, stability curve | `lesson01_stability.py` | `lesson01_stability_solution.py` | `protein_thermal_melt.csv`, `protein_urea_melt.csv` (generated) |
| 29.2 Four ways to fit Michaelis–Menten; Monte Carlo test of Lineweaver–Burk | `lesson02_mm.py` | `lesson02_mm_solution.py` | `invertase_initial_rates.csv` (1913) |
| 29.3 Fructose as an inhibitor of invertase; model choice; IC50 | `lesson03_inhibition.py` | `lesson03_inhibition_solution.py` | `invertase_fructose_rates.csv` (generated from 1913 constants) |
| 29.4 Catalytic triad distances; pH-rate profile | `lesson04_mechanism.py` | `lesson04_mechanism_solution.py` | `data/4CHA_site.pdb`, `chymotrypsin_ph_rate.csv` (generated) |
| 29.5 Part A Gibbs energy of every glycolysis step in a red cell | `lesson05_glycolysis.py` | `lesson05_glycolysis_solution.py` | `glycolysis_steps.csv`, `rbc_metabolites.csv` |
| 29.5 Part B Module practical: characterise enzyme E1 and three inhibitors | `lesson05_practical.py` | `lesson05_practical_solution.py` | `practical_rates.csv` (generated) |

Shared files you do not need to edit: `enz29.py` (CODATA 2022 constants, the 1913 constants, the Michaelis–Menten and general inhibition rate laws, AICc, the two-state stability functions, a CSV reader and a small PDB reader) and `make_data.py` (rebuilds the generated files; `py make_data.py 7` makes a fresh noisy copy with seed 7).

To look at the full chymotrypsin entry, or at chymotrypsin bound to a protein inhibitor:

```bash
py fetch_pdb.py 4CHA 1CHO
py lesson04_mechanism.py data/downloaded/4CHA.pdb
```

## Kitchen activities

- Lesson 29.1: egg white in water at three temperatures (hot tap water, about 65 °C and about 85 °C).
- Lesson 29.4: fresh and canned pineapple with gelatin (bromelain, a cysteine protease).

Read the WARNING and CAUTION boxes in the lessons first: hot water scalds, so let kettle water cool in a mug before use and keep children away; do not eat the test samples; anyone with a pineapple or latex allergy skips the pineapple part.

## Data and sources

- `invertase_initial_rates.csv`: the seven initial rates of Table I of Michaelis and Menten, Biochem. Z. 49, 333 (1913), in the paper's arbitrary units, from the translation by Johnson and Goody, Biochemistry 50, 8264 (2011) (https://pmc.ncbi.nlm.nih.gov/articles/PMC3381512/), retrieved 2026-10-17. The same file is in the Module 22 labs.
- `data/4CHA_site.pdb`: α-chymotrypsin, PDB 4CHA (Tsukada and Blow, J. Mol. Biol. 184, 703, 1985; 1.68 Å), first molecule only (chains A, B, C), trimmed to whole residues within 12 Å of Ser195 Oγ plus waters within 8 Å. PDB archive files are CC0. Retrieved from https://files.rcsb.org/download/4CHA.pdb on 2026-10-17.
- `glycolysis_steps.csv`: standard biochemical Gibbs energies of the ten steps as printed in Jakubowski and Flatt, Fundamentals of Biochemistry, 13.1 Glycolysis (Biology LibreTexts), retrieved 2026-10-17.
- `rbc_metabolites.csv`: model steady-state concentrations in human red cells with the measured ranges, from Protasov et al., Sci. Rep. 9, 1455 (2019), Tables 1 and 2 (CC BY 4.0, https://www.nature.com/articles/s41598-018-37828-5), retrieved 2026-10-17 through Europe PMC. Glucose (5.0 mM) is an assumed normal blood value, not from that paper.
- Generated files (`protein_thermal_melt.csv`, `protein_urea_melt.csv`, `invertase_fructose_rates.csv`, `chymotrypsin_ph_rate.csv`, `practical_rates.csv`): made by `make_data.py` with seed 29; the parameters and noise are listed in each file's header. The protein parameters (Tm 64 °C, ΔH 380 kJ/mol, ΔCp 6 kJ mol⁻¹ K⁻¹, m 7 kJ mol⁻¹ M⁻¹) are typical of a small globular protein of about 100 residues, not of one particular protein. The pH-rate profile uses pKa values typical of chymotrypsin (about 7 and about 9).
- Constants: CODATA 2022 via NIST (https://physics.nist.gov/cuu/Constants/).

## What these labs do not train

They do not run an assay: no pipetting, no spectrophotometer or circular-dichroism instrument, no temperature control, no enzyme purification. The generated data have ideal, known noise; real assays add drifting baselines, enzyme losing activity during the run and substrate impurities. The kitchen experiments train observation and reasoning, not quantitative technique. A real bench course would also train you to plan an assay so that initial rates are truly initial, which these labs can only describe.
