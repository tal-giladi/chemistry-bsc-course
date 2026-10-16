---
id: "05.5"
module: 5
minutes: 20
practice_minutes: 120
prerequisites: ["05.1", "05.2", "05.3", "05.4", "01.5"]
objectives:
  - Run JupyterLab from the course environment and explain how hidden state makes a notebook give results that cannot be reproduced.
  - Structure an analysis so that raw data are read but never edited, paths are relative, random seeds are fixed and software versions are recorded.
  - Prove a notebook is reproducible by restarting the kernel and running all cells, or executing it from the command line.
  - Complete the module practical, a calibration with model choice and an unknown with its uncertainty, as one reproducible notebook.
volatility: implementation
sources:
  - title: "Sandve, Nekrutenko, Taylor and Hovig, Ten Simple Rules for Reproducible Computational Research, PLOS Computational Biology 9 (2013) e1003285"
    url: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003285
  - title: "JupyterLab 4.6 documentation, Starting JupyterLab"
    url: https://jupyterlab.readthedocs.io/en/stable/getting_started/starting.html
  - title: "nbconvert documentation, Executing notebooks"
    url: https://nbconvert.readthedocs.io/en/latest/execute_api.html
  - title: "Software Carpentry, Plotting and Programming in Python (lesson source on GitHub)"
    url: https://github.com/swcarpentry/python-novice-gapminder
last_verified: "2026-10-16"
---

# 05.5 · Reproducible analysis notebooks

A notebook mixes code, results, plots and your explanation in one document, which makes it the natural lab notebook for data analysis. It also makes it easy to fool yourself: cells can be run out of order, deleted after they changed a variable, or depend on a file that only exists on your laptop. This lesson shows how to use JupyterLab so that anyone, including you next year, gets the same numbers by pressing one button. It ends with the module practical: a full calibration and unknown analysis as one reproducible notebook.

## Why it matters

A student reports that a soft drink contains 9.9 % sugar. The notebook shows the number, but when the supervisor reruns it from the top, the result is 9.5 %: a cell that removed an "outlier" had been run twice, and later deleted. Nobody can now say which result is right, and the report has to be withdrawn. In research the same failure shows up as results nobody can reproduce. The fix costs nothing but habits, the computational version of the lab-notebook rules from [01.3](../module-01/lesson-03.md): record how every result was made, never edit raw data by hand, and write down the exact software versions.

## Core ideas

> [!NOTE]
> The habits are stable; they are the "ten simple rules" of Sandve and co-workers (2013). The tools change: checked on 2026-10-16 with JupyterLab 4.6.4 and nbconvert from the pinned environment. Menu names can move between JupyterLab versions; the command `jupyter lab` and the idea of "restart and run all" have been stable for years.

### Notebooks, cells and the kernel

A **notebook** (`.ipynb` file) is a list of **cells**. A **markdown cell** holds text and equations; a **code cell** holds Python and, after running, its output. The code runs in a **kernel**, a Python process that stays alive in the background and keeps every variable you have created.

That is the source of **hidden state**: the kernel remembers what you ran, not what is on the page. If you run cell 5, then edit cell 3 and run it, then delete cell 4, the variables in memory no longer match the document. The little numbers `[7]` next to each cell show the order things really ran in. Out-of-order numbers are a warning sign.

### The one test that matters

**Kernel → Restart Kernel and Run All Cells** throws away the memory and runs the document from top to bottom. If it finishes without errors and gives the same numbers, the notebook is reproducible on your machine. The same test from a terminal, useful before you hand in or share:

```bash
jupyter nbconvert --to notebook --execute lesson05_report.ipynb --output checked.ipynb
```

### Habits that make results repeatable

1. **Raw data are read-only.** Never fix a number in the CSV by hand. Corrections and exclusions happen in code, with a comment that says why.
2. **Relative paths.** `Path("density_raw.csv")`, not `C:\Users\you\Desktop\data.csv`. The notebook then works in anyone's copy of the folder.
3. **Record the environment.** Print the date, the Python version and the package versions at the top, and save them with the results. The pins from [05.1](lesson-01.md) let someone rebuild the same environment.
4. **Fix random seeds.** Any simulation or Monte Carlo step (as in [05.3](lesson-03.md)) uses `np.random.default_rng(seed)` with a written seed.
5. **Save outputs from code.** Figures and result tables are written by the notebook into `runs/`, never copied by hand.
6. **One notebook, one question.** Steps in order: read → check → process → fit → judge → predict → save → conclude.
7. **Version control.** Keep notebooks and scripts in git (the course itself is a git repo). Clear outputs before committing if they are large.

### Notebook or script?

Notebooks are best for exploring and explaining: the plot sits next to the sentence that interprets it. Scripts (`.py`) are best for code you reuse or run many times, such as the JCAMP reader from [05.4](lesson-04.md). A good pattern is to keep reusable functions in a `.py` file and import them into the notebook.

## Worked example

### Choosing the calibration model for sugar solutions

Seven sucrose standards (0 to 30 % by mass) were measured five times each with a syringe and a 0.01 g pocket scale, the method of [01.5](../module-01/lesson-05.md) with a better scale (`density_raw.csv`, simulated). The SD of five repeats is itself uncertain by about ±35 %, and all samples were measured the same way, so the notebook uses the pooled SD, $\sqrt{\overline{s^2}} = 0.00143$ g/mL, and the standard error $0.00143/\sqrt{5} = 0.00064$ g/mL for every mean.

Two weighted fits (`absolute_sigma=True`):

| Model | Reduced chi-square (degrees of freedom) | Residual pattern |
|---|---|---|
| Straight line, 0–30 % | 9.11 (5) | U shape: positive at both ends, negative in the middle |
| Quadratic, 0–30 % | 1.34 (4) | random |

The straight line has $R^2 = 0.9985$ and still fails: the residuals form a U shape and $\chi^2_\nu \approx 9$. Sugar solutions really are slightly curved, a fact the reference table in Module 1 already hints at (the density step per 10 % grows from 0.0399 to 0.0460 g/mL). The quadratic leaves random residuals, so it is the calibration.

Inverting the quadratic $\rho = a + bw + cw^2$ for an unknown gives

$$w = \frac{-b + \sqrt{b^2 - 4c\,(a - \rho)}}{2c}$$

and with `correlated_values` the uncertainty follows automatically. The regular soft drink ($\rho = 1.03706 \pm 0.00064$ g/mL) contains $9.85 \pm 0.18$ % sugar; the diet drink ($0.99860 \pm 0.00064$ g/mL) contains $0.04 \pm 0.23$ %, consistent with zero. The straight line would have reported 9.54 % and 0.55 %: the diet drink would then appear to contain sugar it does not have.

## Hands-on

### Module practical: one reproducible notebook (about 2 hours)

What you need: your environment from [05.1](lesson-01.md), the [Module 5 lab folder](../../labs/module-05/) with `lesson05_report.ipynb` and `density_raw.csv`. Optional: your own density measurements from [01.5](../module-01/lesson-05.md) in the same columns. To include a drink, add its rows with `w_percent` left empty.

1. Start JupyterLab from the lab folder, so relative paths work:

```bash
cd labs/module-05
..\..\.venv\Scripts\jupyter lab
```

   It opens in your browser. Open `lesson05_report.ipynb` and save a copy as `my_report.ipynb`.

2. Work through Steps 1–7. Each code cell has TODO lines; each step uses one earlier lesson: reading and checking (05.4), a vectorised density column and a grouped summary (05.2), weighted fits and reduced chi-square (05.3), propagation to the unknown (05.3), and the version record (05.1).
3. Write the model-choice sentence after Step 5 and the conclusion at the end, using only numbers the notebook printed.
4. Restart the kernel and run all cells. Then check from a terminal in the same folder:

```bash
..\..\.venv\Scripts\jupyter nbconvert --to notebook --execute my_report.ipynb --output checked.ipynb
```

5. Export or print the notebook and file it with a page made from the [lab report template](../../templates/lab-report.md).

How you know it worked:

- Step 1: 45 rows, 8 columns, `sample` is `str`, the measurement columns are numeric, 10 missing `w_percent` values (the two drinks).
- Step 3: pooled SEM 0.00064 g/mL for every sample.
- Step 4: line $\chi^2_\nu = 9.11$; quadratic $\chi^2_\nu = 1.34$.
- Step 6: soft drink $9.85 \pm 0.18$ %, diet drink $0.04 \pm 0.23$ %. The values used to make the data were 9.8 % and 0.3 %.
- `runs/` contains `lesson05_calibration.png`, `lesson05_results.csv` and `lesson05_environment.txt`.
- Restart-and-run-all and the `nbconvert` command both finish without errors and give the same numbers.

With your own Module 1 data (1 g kitchen scale, four standards) the curvature is hidden in the noise: expect the straight line to pass ($\chi^2_\nu$ near 1 or 2) and the quadratic to be unnecessary. That is a correct conclusion for that data, not a failure.

<details><summary>Reference solution and discussion</summary>

The full analysis as a script, with the same steps and numbers, is `labs/module-05/lesson05_report_solution.py`:

```bash
..\..\.venv\Scripts\python lesson05_report_solution.py
..\..\.venv\Scripts\python lesson05_report_solution.py ../module-01/my_data.csv
```

It also prints a third model, a straight line over 0–15 % only. Its $\chi^2_\nu$ of 4.7 shows that even a narrower range is still visibly curved with this precision, so the quadratic is the better choice.

Key cells:

```python
df["rho_g_per_mL"] = (df["cup_full_g"] - df["cup_empty_g"]) / (df["fills"] * df["fill_volume_mL"])
summary["sem"] = np.sqrt(np.mean(summary["sd"] ** 2)) / np.sqrt(summary["n"])
qa, qb, qc = correlated_values(p_quad, c_quad)
w = (-qb + (qb**2 - 4 * qc * (qa - rho_u)) ** 0.5) / (2 * qc)
```

A good conclusion names the uncertainty budget: about 0.15 % of the 0.18 % comes from the drink's own density reading, so more repeats of the drink help more than more standards. And it names what density cannot see: acids, salts and dissolved CO₂ also change the density, so a real lab confirms with a second method such as refractometry or HPLC (Module 25).

</details>

## Common mistakes

- Trusting a notebook you never restarted. Hidden state from deleted or re-run cells can produce numbers the document cannot reproduce. Restart and run all before you believe a result.
- Editing the raw CSV to drop an outlier. Exclude it in code, with the reason in a comment, and report it.
- Absolute paths to your own disk. Start JupyterLab in the data folder and use relative paths.
- Choosing a model by $R^2$. A curved residual plot and $\chi^2_\nu \gg 1$ say "wrong model" even at $R^2 = 0.998$.
- Using each sample's own SD from 3 to 5 repeats as the weight. Those SDs are themselves very uncertain; when the method is the same for all samples, pool them.
- Not recording versions. "It worked on my machine" is only useful if you can say which machine, which Python and which packages.

## Key takeaways

- The kernel remembers what you ran, not what the page shows; out-of-order cell numbers warn of hidden state.
- Restart-and-run-all (or `nbconvert --execute`) is the test of a reproducible notebook.
- Read raw data, never edit it; use relative paths, fixed seeds, saved outputs and a version record.
- Let residuals and reduced chi-square choose the model, then propagate the uncertainty to the unknown.
- Notebooks explain an analysis; reusable functions belong in `.py` files that the notebook imports.

## Sources

- [Sandve et al. 2013, Ten Simple Rules for Reproducible Computational Research](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003285) — the habits behind this lesson.
- [Starting JupyterLab (JupyterLab 4.6 docs)](https://jupyterlab.readthedocs.io/en/stable/getting_started/starting.html) — `jupyter lab` and where it opens.
- [nbconvert: Executing notebooks](https://nbconvert.readthedocs.io/en/latest/execute_api.html) — running a notebook from the command line.
- [Software Carpentry, Plotting and Programming in Python](https://github.com/swcarpentry/python-novice-gapminder) — a free, hands-on course for more practice with pandas, plotting and notebooks.
