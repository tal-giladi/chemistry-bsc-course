# Module 25 labs — Analytical Chemistry Lab 2

One Python exercise per lesson plus the module practical (a quality-control dossier for a bitter-lemon drink, Lesson 25.6 Part C). Each exercise file has parts marked TODO; the matching `*_solution.py` file is the reference solution. Plots are written to `runs/` in this folder (ignored by git). The instrument data are simulated; the home experiments (phone spectrometer, tonic water under UV, salt flame) produce your own data in the same CSV format.

Setup (once, Python 3.14, packages pinned in `labs/common/requirements.txt`; checked 2026-10-17 with numpy 2.5, scipy 1.18 and matplotlib 3.11):

```bash
py -3.14 -m venv .venv
.venv\Scripts\python -m pip install -r labs/common/requirements.txt
```

On macOS or Linux use `python3.14` and `.venv/bin/python`. Run each file from this folder, for example `py lesson01_phone_spectrometer.py`. Keep `ana25.py` in the same folder.

| Lesson | Exercise | Solution | Data |
|---|---|---|---|
| 25.1 Mixtures and a phone spectrometer | `lesson01_phone_spectrometer.py` | `lesson01_phone_spectrometer_solution.py` | `phone_spectra_example.csv` or yours via `photo_to_profile.py` |
| 25.2 Fluorescence: quinine in tonic water | `lesson02_quinine.py` | `lesson02_quinine_solution.py` | `tonic_home_example.csv` (or yours), `quinine_fluorimeter.csv` |
| 25.3 Atomic absorption and emission | `lesson03_aas.py` | `lesson03_aas_solution.py` | `aas_calcium.csv` |
| 25.4 GC and GC-MS | `lesson04_gcms.py` | `lesson04_gcms_solution.py` | `gcms_alkanes.csv`; run `get_nist_ms.py` first |
| 25.5 HPLC method thinking | `lesson05_hplc_method.py` | `lesson05_hplc_method_solution.py` | `hplc_scouting.csv`, `hplc_sst.csv` |
| 25.6 Cyclic voltammetry in practice | `lesson06_cv.py` | `lesson06_cv_solution.py` | `cv_quasi.csv` |
| 25.6 Module practical: QC dossier | `practical_dossier.py` | `practical_dossier_solution.py` | `practical_drink.csv` + the GC-MS run |

Shared: `ana25.py` holds a CSV reader, the least-squares line, the concentration-with-uncertainty formula of Lesson 09.4 (Harvey eq. 5.12), standard addition, the sRGB linearisation of Lesson 09.6 and a plot saver.

## Your own phone-spectrometer photos

Take every photo with the phone taped in place and exposure and white balance locked. Then:

```bash
py photo_to_profile.py my_spectra.csv cfl=cfl.jpg blank=water.jpg blue_0.1=b01.jpg blue_0.5=b05.jpg yellow_0.5=y05.jpg green_unknown=g.jpg
py lesson01_phone_spectrometer_solution.py my_spectra.csv
```

`photo_to_profile.py` averages a band of rows across the spectrum (`--rows 0.45 0.55` by default), undoes the sRGB curve and writes one column per photo. It warns if pixels are saturated. Use `--vertical` if your rainbow runs top to bottom. Lesson 25.1 needs at least `cfl`, `blank`, `blue_0.5`, `yellow_0.5` and `green_unknown`.

## NIST mass spectra (Lesson 25.4)

`get_nist_ms.py` downloads ten electron-ionisation spectra from the NIST Chemistry WebBook into `data/downloaded/nist_ms/` and builds the simulated lemon-oil run `data/downloaded/gcms_run.csv` from them. It needs internet once and takes about a minute (it pauses between requests and retries if the server asks it to slow down). The NIST spectra are copyrighted by the U.S. Secretary of Commerce, so they are not in this folder: download them for your own study and do not redistribute them. The WebBook IDs (for example `C138863`, limonene) are in the script; the matching page is `https://webbook.nist.gov/cgi/cbook.cgi?ID=C138863&Mask=200`. The retention indices in the script are medians of the 5 %-phenyl temperature-ramp entries on each compound's WebBook gas-chromatography page, read 2026-10-17.

## Data

All committed CSV files are simulated by `make_data.py` (fixed random seed; run `py make_data.py` to regenerate them). Each file's first lines say what it models and the true values. No database records are copied.

- `phone_spectra_example.csv`: a cardboard + DVD spectrometer seen by a phone (600 pixels): a fluorescent lamp (Hg lines at 404.66, 435.83, 546.07, 576.96 and 579.07 nm from NIST; Eu³⁺ 611.6 nm), and a white LED through water, a blue and a yellow food-dye dilution series and a green mixture (0.35 blue + 0.60 yellow). Instrument width 2.5 nm (sigma), stray light 2 %.
- `tonic_home_example.csv`: blue-channel values of phone photos of tonic dilutions and of a 1/8 dilution with table salt, under a 365 nm torch. Inner-filter model and Stern–Volmer K = 130 L/mol.
- `quinine_fluorimeter.csv`: quinine standards, tonic diluted 1 + 199 and a standard-addition series (true 72.0 mg/L).
- `aas_calcium.csv`: flame AAS calcium standards with La, a mineral water (48.0 mg/L) with and without La, a spike and check standards.
- `gcms_alkanes.csv`: n-alkane ladder C8–C14 on a 5 % phenyl column, 60 °C then 3 K/min.
- `hplc_scouting.csv`, `hplc_sst.csv`: two isocratic scouting runs and six system-suitability injections (new and worn column) for paracetamol, caffeine, aspirin and salicylic acid.
- `cv_quasi.csv`: CVs of a 1.0 mM quasi-reversible couple at six scan rates from an explicit finite-difference simulation with Butler–Volmer kinetics (k⁰ = 0.004 cm/s, α = 0.5, D = 7.0 × 10⁻⁶ cm²/s, E°′ = 0.220 V, 3 mm disc, 20 µF/cm²). Its peak separations agree with Nicholson's 1965 working curve.
- `practical_drink.csv`: tartrazine at 426 and 700 nm, quinine external and standard-addition fluorescence, vitamin C voltammetric standard addition for a cloudy drink (true 24.0, 62.0 and 110 mg/L).

Constants: CODATA 2022 from NIST (F, R). Absorptivities: Brilliant Blue FCF 164 L g⁻¹ cm⁻¹ at 629 nm (FAO/JECFA), tartrazine 53 L g⁻¹ cm⁻¹ at 426 nm (EU Regulation 231/2012). Quinine limit 83 mg/L: 21 CFR 172.575 (eCFR, read 2026-10-17). pKa and log P: PubChem.
