# Module 21 labs — Statistical Thermodynamics

Python exercises that turn spectroscopic data into thermodynamics, plus one kitchen activity (coins and cups, lesson 21.1) and the module practical: the equilibrium constant of I₂(g) ⇌ 2I(g) from 500 to 1500 K, calculated from NIST spectroscopic constants and checked against the NIST-JANAF tables (lesson 21.4). Each exercise file has functions marked TODO; the matching `*_solution.py` file is the reference solution. Plots are written to `runs/` in this folder (ignored by git).

Setup (once, Python 3.14, packages pinned in `labs/common/requirements.txt`; checked 2026-10-16):

```bash
py -3.14 -m venv .venv
.venv\Scripts\python -m pip install -r labs/common/requirements.txt
```

On macOS or Linux use `python3.14` and `.venv/bin/python`. These labs need numpy and matplotlib only. Run each file from this folder, for example `py lesson02_partition.py`.

| Lesson | Exercise | Solution | Data |
|---|---|---|---|
| 21.1 Microstates and the Boltzmann distribution | `lesson01_microstates.py` | `lesson01_microstates_solution.py` | constants in `stat21.py`; optional `my_cups.csv` (`n,count`) from the coins game |
| 21.2 The partition function | `lesson02_partition.py` | `lesson02_partition_solution.py` | `janaf_check.csv` (Cl), N₂ Shomate coefficients in the file |
| 21.3 Molecular partition functions | `lesson03_molecular_q.py` | `lesson03_molecular_q_solution.py` | `stat21.py`, NIST S° values in the file |
| 21.4 Practical: K for I₂ ⇌ 2I | `lesson04_practical.py` | `lesson04_practical_solution.py` | `stat21.py`, `janaf_check.csv` (I, I₂) |

```bash
py lesson01_microstates.py my_cups.csv
py lesson04_practical.py
```

`stat21.py` is the shared helper: CODATA 2022 constants, molar masses, the diatomic constants and atomic levels below, partition functions (translation, rotation by direct sum or high-T formula, harmonic and anharmonic vibration, electronic levels) and `thermo_from_lnq`, which turns $\ln q^\circ$ into $H - H(0)$, $S^\circ$ and $C_p$ by numerical derivatives. Read it after lesson 21.3; it is about 150 lines.

## Home materials

10 paper cups (or an egg box), 10 identical coins, a phone with a random-number app or a 10-sided die, a notebook. Coins are a choking hazard: keep them away from small children and pets.

## Data and sources

- Constants: CODATA 2022 via NIST (https://physics.nist.gov/cuu/Constants/): $h$, $c$, $k_B$, $N_A$ exact; atomic mass constant 1.66053906892 × 10⁻²⁷ kg. Retrieved 2026-10-17.
- Molar masses: NIST standard atomic weights (https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl), natural isotope mixtures, as the NIST thermochemical tables use.
- Diatomic constants ($\omega_e$, $\omega_e x_e$, $B_e$, $\alpha_e$) of N₂, CO, HCl (H³⁵Cl), O₂ and ¹²⁷I₂: NIST Chemistry WebBook, constants of diatomic molecules (https://webbook.nist.gov/chemistry/, pages C7727379, C630080, C7647010, C7782447, C7553562, Mask=1000), retrieved 2026-10-17.
- Atomic levels: NIST Atomic Spectra Database (https://physics.nist.gov/PhysRefData/ASD/levels_form.html): Cl I ²P₁/₂ at 882.3515 cm⁻¹, I I ²P₁/₂ at 7602.9762 cm⁻¹, retrieved 2026-10-17.
- $D_0$(I₂) = 148.824 kJ/mol from the NIST-JANAF 0 K formation enthalpies of I(g) (107.164) and I₂(g) (65.504), tables I-001 and I-027.
- `janaf_check.csv`: $C_p$, $S^\circ$ and $\log_{10}K_f$ of I(g), I₂(g) and Cl(g) from the NIST-JANAF tables online (https://janaf.nist.gov/, tables I-001, I-027, Cl-001), retrieved 2026-10-17. Used only to check the calculations.
- Reference entropies in `lesson03_molecular_q*.py`: CODATA Key Values (Cox, Wagman and Medvedev 1984) as listed in the NIST WebBook (Ar 154.846, N₂ 191.609, CO 197.660, HCl 186.902, O₂ 205.152 J mol⁻¹ K⁻¹), and JANAF for I₂, I and Cl.
- N₂ Shomate coefficients (500–2000 K) in `lesson02_partition*.py`: NIST WebBook gas-phase thermochemistry of N₂ (Chase 1998).
- NIST data are a U.S. government compilation and may be used with citation; the files here are small extracts.
