# Module 1 lab — density of water and sugar solutions

Files for the practical in lesson 01.5 ("Your home kit and first measurement").

| File | What it is |
|---|---|
| `density_analysis.py` | Your analysis script. It runs as it is; two steps are left as TODOs. |
| `density_analysis_solution.py` | Reference solution. Look at it after you have tried. |
| `data_template.csv` | Empty data file with the right columns. Copy it to `my_data.csv` and fill it in. |
| `example_data.csv` | Simulated example data (generated, not measured): a 20 mL syringe that delivers about 1% more than its marks, a 1 g kitchen scale, 23 °C. Use it to test the scripts. |
| `reference_sucrose_density.csv` | Reference densities of sucrose solutions at 20 °C. |

## Setup

Python 3.14 and the packages in `labs/common/requirements.txt` (only `numpy` is needed, plus `matplotlib` for the plot). From the repo root:

```bash
py -3.14 -m venv .venv
.venv\Scripts\python -m pip install -r labs/common/requirements.txt
```

On macOS or Linux use `python3.14` and `.venv/bin/python`. Checked on 2026-10-16 with Python 3.14.3, numpy 2.5 and matplotlib 3.11.2.

## Run

```bash
.venv\Scripts\python labs/module-01/density_analysis.py                          # example data
.venv\Scripts\python labs/module-01/density_analysis.py labs/module-01/my_data.csv --plot
```

If your scale shows 0.1 g steps, change `SCALE_RESOLUTION_G` at the top of the script to `0.1`.

## Data columns

One row per repeat: `sample` (a name), `w_percent` (sugar mass percent; 0 for water, which must be included because it calibrates the syringe), `repeat`, `fills` (syringe fills per repeat), `fill_volume_mL` (the mark you filled to), `cup_empty_g`, `cup_full_g`, `temp_C`.

## Sources of the reference data

- Sucrose solutions: Plato's density table at 20 °C, as reprinted by the US National Bureau of Standards, Letter Circular LC 770, https://nvlpubs.nist.gov/nistpubs/Legacy/LC/nbslettercircular770.pdf (US government work).
- Water: CIPM formula of Tanaka et al., Metrologia 38 (2001) 301–309, https://doi.org/10.1088/0026-1394/38/4/3, coded in the scripts.
