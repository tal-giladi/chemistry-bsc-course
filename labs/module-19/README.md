# Module 19 labs — Analytical Chemistry 2: Instrumental Methods

One Python exercise per lesson plus the module practical (an HPLC method for caffeine in an energy drink, lesson 19.5 Part C). Each exercise file has parts marked TODO; the matching `*_solution.py` file is the reference solution. Plots are written to `runs/` in this folder (ignored by git). No wet chemistry: every data set is simulated.

Setup (once, Python 3.14, packages pinned in `labs/common/requirements.txt`; checked 2026-10-17 with numpy 2.5, scipy 1.18 and matplotlib 3.11):

```bash
py -3.14 -m venv .venv
.venv\Scripts\python -m pip install -r labs/common/requirements.txt
```

On macOS or Linux use `python3.14` and `.venv/bin/python`. Run each file from this folder, for example `py lesson01_uvvis.py`. Keep `ana19.py` in the same folder.

| Lesson | Exercise | Solution | Data |
|---|---|---|---|
| 19.1 UV-Vis and Beer-Lambert | `lesson01_uvvis.py` | `lesson01_uvvis_solution.py` | `dye_uvvis.csv` |
| 19.2 Fluorescence and atomic spectroscopy | `lesson02_fluor_atomic.py` | `lesson02_fluor_atomic_solution.py` | `quinine_chloride.csv` |
| 19.3 Extraction and chromatography theory | `lesson03_extraction_vandeemter.py` | `lesson03_extraction_vandeemter_solution.py` | `vandeemter_gc.csv` or your own (`u_cm_per_s,H_mm`) |
| 19.4 Gas and liquid chromatography | `lesson04_gc.py` | `lesson04_gc_solution.py` | `gc_retention.csv`, `sanitizer_gc_is.csv` |
| 19.5 Electroanalysis and CV | `lesson05_cv.py` | `lesson05_cv_solution.py` | `cv_ferricyanide.csv` |
| 19.5 Module practical: HPLC method for caffeine | `practical_hplc.py` | `practical_hplc_solution.py` | `hplc_vandeemter.csv`, `caffeine_hplc.csv` |

Shared: `ana19.py` holds a small CSV reader, the least-squares line, the concentration-with-uncertainty formula of Lesson 09.4 (Harvey eq. 5.12) and a plot saver.

## Data

All CSV files are simulated by `make_data.py` (fixed random seed; run `py make_data.py` to regenerate them). Each file's first line says what it models. No database records are copied.

- `dye_uvvis.csv`: blue food dye standards at 630 nm on an instrument with 0.40 % stray light (absorptivity 0.160 L mg⁻¹ cm⁻¹), a sports drink undiluted and diluted 1 + 19.
- `quinine_chloride.csv`: quinine fluorescence with added chloride, Stern–Volmer constant 130 L/mol, chosen to match the quenching Harvey reports (83 % of the signal left at 100 mg/L NaCl).
- `vandeemter_gc.csv`: plate height against velocity for a 2 m packed GC column, from H = A + B/u + Cu with 2 % noise.
- `gc_retention.csv`: alkane ladders and two peaks on DB-5 and DB-Wax columns. Peaks X and Y are placed at the retention indices of limonene and linalool listed by the NIST Chemistry WebBook (read 2026-10-17): https://webbook.nist.gov/cgi/cbook.cgi?ID=C138863&Mask=2000 and https://webbook.nist.gov/cgi/cbook.cgi?ID=C78706&Mask=2000.
- `sanitizer_gc_is.csv`: GC-FID peak areas of ethanol and the internal standard 1-butanol, with ±15 % injection-volume scatter.
- `cv_ferricyanide.csv`: cyclic voltammograms of 2.0 mM ferricyanide at five scan rates, from an explicit finite-difference simulation with Butler–Volmer kinetics (E°′ = 0.220 V vs Ag/AgCl, k⁰ = 0.02 cm/s, α = 0.5, D = 7.2 × 10⁻⁶ cm²/s, 3 mm disc, double-layer capacitance 20 µF/cm², IUPAC sign convention). With a very large k⁰ the same code reproduces the Randles–Ševčík peak current within 0.2 % and a peak separation of 58.5 mV.
- `hplc_vandeemter.csv`, `caffeine_hplc.csv`: van Deemter data for a 5 µm and a 2.7 µm core–shell C18 column; caffeine blanks, standards, a drink diluted 1 + 9 and spiked portions.

Constants: CODATA 2022 from NIST (h, c, k, F, R). Benzoic acid pKa 4.20 from PubChem (CID 243). The EU 150 mg/L caffeine labelling threshold is from Regulation (EU) 1169/2011, Annex III.
