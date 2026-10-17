# Module 26 labs — Bio-inorganic Chemistry

Python exercises on real data: metal sites in protein crystal structures from the Protein Data Bank, and the standard human blood oxygen dissociation curve. Each exercise file has functions marked TODO; the matching `*_solution.py` file is the reference solution. Lesson 26.1 adds a kitchen experiment and lesson 26.3 an optional pulse-oximeter reading (no lab reagents).

Setup (once, Python 3.14, packages pinned in `labs/common/requirements.txt`; checked 2026-10-17):

```bash
py -3.14 -m venv .venv
.venv\Scripts\python -m pip install -r labs/common/requirements.txt
```

On macOS or Linux use `python3.14` and `.venv/bin/python`. These labs need only numpy, scipy and matplotlib; `fetch_pdb.py` uses the standard library and an internet connection. Run each file from this folder, for example `py lesson01_metal_sites.py`. Plots are saved to `runs/` and downloaded structures to `data/downloaded/` (both ignored by git). `py bio26.py` prints a short self-check.

| Lesson | Exercise | Solution | Data |
|---|---|---|---|
| 26.1 Metal sites in four proteins; free Fe³⁺ at pH 7 | `lesson01_metal_sites.py` | `lesson01_metal_sites_solution.py` | `data/1A6M_sites.pdb`, `3KS3_sites.pdb`, `1CLL_sites.pdb`, `1PLC_sites.pdb`, or any PDB file you pass |
| 26.2 Haem spin states; iron in and out of the porphyrin plane | `lesson02_heme.py` | `lesson02_heme_solution.py` | `data/2DN2_sites.pdb`, `2DN1_sites.pdb`, `1A6M_sites.pdb` |
| 26.3 Hill plot of the standard blood curve; Bohr shift; your SpO₂ | `lesson03_hill.py` | `lesson03_hill_solution.py` | `hb_standard_curve.csv` |
| 26.4 Part A Marcus rates and the respiratory chain | `lesson04_electron_transfer.py` | `lesson04_electron_transfer_solution.py` | constants in the script |
| 26.4 Part B Module practical: fit the O₂ curve, delivery, electron current | `lesson04_practical.py` | `lesson04_practical_solution.py` | `hb_standard_curve.csv` |

Shared file you do not need to edit: `bio26.py` — CODATA 2022 constants, the myoglobin P50, the blood O₂ content and Bohr constants, a CSV reader, a small PDB reader and the Severinghaus equation.

To look at another structure, download it and pass it to the lesson 26.1 script:

```bash
py fetch_pdb.py 4HHB
py lesson01_metal_sites.py data/downloaded/4HHB.pdb
```

## Home activities

- Lesson 26.1: iron filings from iron-fortified breakfast cereal with a strong magnet. Read the WARNING box first: magnets out of reach of children, do not eat the cereal afterwards.
- Lesson 26.3 (optional): if you already own a fingertip pulse oximeter, read your SpO₂ at rest and pass it to `lesson03_hill.py`. It is not a medical test.

## Data and sources

- `hb_standard_curve.csv`: the standard human blood O₂ dissociation curve at 37 °C, pH 7.40 and PCO₂ 40 mmHg, 51 points from 1 to 500 mmHg. Values from Table 1 of Severinghaus, J. Appl. Physiol. 46, 599–602 (1979), in the author's revised version of 2007 (https://www.nickalls.org/dick/papers/anes/JWSrevised2007.pdf), retrieved 2026-10-17. Severinghaus interpolated the table between the measurements compiled by Roughton and Severinghaus, J. Appl. Physiol. 35, 861 (1973). It is a smoothed standard curve built from measurements, not one person's raw readings; the points carry no random scatter, so fit uncertainties are unrealistically small and any misfit you see is systematic.
- `data/*_sites.pdb`: PDB entries 1A6M (oxy-myoglobin, sperm whale, 1.0 Å; Vojtěchovský et al. 1999), 2DN1 and 2DN2 (human oxy- and deoxy-haemoglobin, 1.25 Å; Park et al. 2006), 3KS3 (human carbonic anhydrase II, 0.9 Å; Avvaru et al. 2010), 1CLL (human calmodulin with four Ca²⁺, 1.7 Å; Chattopadhyaya et al. 1992) and 1PLC (poplar plastocyanin, 1.33 Å; Guss et al. 1992), downloaded from https://files.rcsb.org/download/ on 2026-10-17 and trimmed to the residues within 10 Å of a metal ion (alternate location A only). PDB archive data are CC0 1.0 (https://www.wwpdb.org/about/usage-policies).
- Myoglobin P50 = 2.39 Torr at 37 °C and pH 7.0, Hill coefficient 1: Schenkman et al., J. Appl. Physiol. 82, 86 (1997), PubMed 9029202.
- Blood O₂ content $C = 1.34\,[\mathrm{Hb}]\,S + 0.0031\,P_{\mathrm{O_2}}$ (mL/dL) and the Bohr coefficient $\Delta\log_{10}P_{\mathrm{O_2}}/\Delta\mathrm{pH} = -0.48$: Severinghaus (1979, revised 2007).
- Tunnelling constants ($\beta$ = 1.1 Å⁻¹, $10^{13}$ s⁻¹ at 3 Å contact, $\lambda \approx$ 0.8 eV): Gray and Winkler, PNAS 102, 3534 (2005), https://pmc.ncbi.nlm.nih.gov/articles/PMC553296/.
- Reduction potentials at pH 7: Jakubowski, Biochemistry Online (LibreTexts), table in section 8B.3 Dehydrogenases.
- Constants: CODATA 2022 via NIST (https://physics.nist.gov/cuu/Constants/).

## What these labs do not train

They do not measure anything at the bench: no tonometer, no oxygen electrode, no spectrophotometer, no crystallography. The O₂ curve is a published standard, so you practise fitting and interpretation, not measurement error. The crystal structures are frozen snapshots; the distances you compute carry errors of roughly 0.02–0.05 Å at these resolutions. The magnet experiment shows that "iron" on a cereal label can be metallic iron; it does not measure how much the body absorbs.
