# Module 9 labs — Analytical Chemistry 1: Measurement and Error

One Python exercise per lesson, two home experiments (a coin series on a kitchen scale in lesson 09.1 and the phone-photo calibration of the module practical in lesson 09.6) and a photo helper. Each exercise file has functions marked TODO; the matching `*_solution.py` file is the reference solution. Plots are written to `runs/` in this folder (ignored by git).

Setup (once, Python 3.14, packages pinned in `labs/common/requirements.txt`; checked 2026-10-17):

```bash
py -3.14 -m venv .venv
.venv\Scripts\python -m pip install -r labs/common/requirements.txt
```

On macOS or Linux use `python3.14` and `.venv/bin/python`. These labs need numpy, scipy, matplotlib and uncertainties (lesson 09.3).

Run each file from this folder, for example `py lesson04_calibration.py`.

| Lesson | Exercise | Solution | Data |
|---|---|---|---|
| 09.1 Types of error, accuracy and precision | `lesson01_bias.py` | `lesson01_bias_solution.py` | `crm_analysts.csv`, `sample_size_series.csv`, `coins_example.csv` or your own (`n_coins,reading_g`) |
| 09.2 Statistics: mean, SD and confidence intervals | `lesson02_stats.py` | `lesson02_stats_solution.py` | `replicates.csv` or your own (`method,value`) |
| 09.3 Propagation of uncertainty | `lesson03_propagation.py` | `lesson03_propagation_solution.py` | inputs inside the script |
| 09.4 Calibration, regression and detection limits | `lesson04_calibration.py` | `lesson04_calibration_solution.py` | `nitrite_calibration.csv` |
| 09.5 Titration theory and titration curves | `lesson05_titration.py` | `lesson05_titration_solution.py` | `titration_weak_acid.csv` or your own (`V_NaOH_mL,pH`) |
| 09.6 Buffers and gravimetric analysis | `lesson06_buffer.py` | `lesson06_buffer_solution.py` | constants inside the script |
| 09.6 Module practical: calibration from phone photos | `practical_dye_calibration.py` | `practical_dye_calibration_solution.py` | `dye_photo_example.csv` or your own (`type,c_percent_stock,R,G,B`) |

To run on your own measurements, pass the file as an argument:

```bash
py lesson01_bias.py my_coins.csv 3.5
py lesson02_stats.py my_repeats.csv
py rgb_from_photos.py blank1.jpg std01.jpg
py practical_dye_calibration.py my_photos.csv
```

The `3.5` is the nominal mass of your coin in grams (one shekel, Bank of Israel). `rgb_from_photos.py` prints the mean red, green and blue values of the central square of each photo (PNG or JPEG).

## Home materials (lessons 09.1 and 09.6)

Ten coins of one kind, a small dish, a kitchen or pocket scale (0.1 g is best), liquid blue food colouring, tap water, 13 identical clear plastic cups, white paper, a phone camera and a stack of books or a phone stand, labels and safety glasses. Kitchen materials only; read the safety box in each lesson first.

## Data

All data files here are simulated by `make_data.py` from known models with fixed random seeds (run `py make_data.py` to regenerate them). They are realistic but not measured, so you can check your analysis against the true values written in each file's header.

- `crm_analysts.csv`, `sample_size_series.csv`, `replicates.csv`: a chloride CRM certified at 25.0 ± 0.3 mg/L (k = 2) and pure NaCl (606.6 mg chloride per gram, IUPAC atomic weights).
- `coins_example.csv`: one-shekel coins (nominal 3.5 g, Bank of Israel, https://boi.org.il/en/economic-roles/coins/new-agora-and-sheqel-series/) on a 0.1 g scale with an offset.
- `nitrite_calibration.csv`: modelled on a Griess-type nitrite colour test at 540 nm; the slope is illustrative, not a validated method value.
- `titration_weak_acid.csv`: exact charge-balance curve for acetic acid (pKa 4.757, Harvey, Analytical Chemistry 2.1, Appendix 11) with pH-meter offset and noise.
- `dye_photo_example.csv`: a phone-camera model for Brilliant Blue FCF (absorbs near 630 nm) with stray light and lighting noise, encoded with the sRGB transfer function.
