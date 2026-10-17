---
id: "33.2"
module: 33
minutes: 20
practice_minutes: 180
prerequisites: ["33.1", "09.2", "09.3", "05.5"]
objectives:
  - Design a study with a known-answer test, a pilot, a held-out check and an analysis plan written before the data are seen.
  - Calculate from a pilot standard deviation how many repeats give a target 95 % confidence half-width.
  - Set up a project folder in which raw data stay unchanged, every result is rebuilt by code, and every file and column is described.
  - Keep an hours log and a dated notebook that let a reader reconstruct what was done.
volatility: concept
sources:
  - title: "Wilson et al. (2017), Good enough practices in scientific computing, PLOS Computational Biology 13(6), e1005510"
    url: https://doi.org/10.1371/journal.pcbi.1005510
  - title: "Wilkinson et al. (2016), The FAIR Guiding Principles for scientific data management and stewardship, Scientific Data 3, 160018"
    url: https://doi.org/10.1038/sdata.2016.18
  - title: "GO FAIR Foundation, FAIR principles"
    url: https://www.gofair.foundation/fair-principles
  - title: "NIST/SEMATECH e-Handbook of Statistical Methods, 1.3.5.2 Confidence limits for the mean"
    url: https://www.itl.nist.gov/div898/handbook/eda/section3/eda352.htm
  - title: "Git documentation"
    url: https://git-scm.com/doc
last_verified: "2026-10-17"
---

# 33.2 · Designing the study and managing the data

With a question and a proposal in hand, the next step is the design: what you will measure or calculate, in what order, how many times, and how you will know the method works before you trust it. The second half of the lesson is about the data themselves. A project of 180 hours produces hundreds of files; if you cannot find the raw data, rerun the analysis or say which version of a figure is in the report, the result cannot be checked, not even by you.

## Why it matters

Imagine week 14 of your project. Your reader asks: "How did you get 47 cm⁻¹ for the esters? I get 52 from your table." You find three versions of the spreadsheet, one edited by hand, and a figure made from a file that no longer exists. You cannot answer. This happens to experienced researchers too, and it is why journals now ask for data and code. The habits in this lesson cost a few hours at the start and save the project at the end.

A design flaw is worse, because no amount of tidy files fixes it. If you titrate brand A on Monday and brand B on Thursday with a new batch of baking-soda solution, any difference between the brands is mixed up with the difference between the batches. You only find out when it is too late to repeat.

## Core ideas

> [!NOTE]
> Stable: the design ideas (known-answer test, pilot, blanks, randomised order, held-out data, analysis plan) and the statistics of repeats. Will go out of date: tools and versions (Python 3.14 and the packages in `labs/common/requirements.txt`, checked 2026-10-16; git as current on 2026-10-17). The folder layout follows Wilson et al. (2017); FAIR principles as published in 2016 and summarised by the GO FAIR Foundation (checked 2026-10-17).

### Five design elements

1. **Known-answer test.** Before you run the real population, reproduce a value someone else has published: the formaldehyde frequencies of [31.4](../module-31/lesson-04.md), the water density of [01.5](../module-01/lesson-05.md), the label of one vinegar. If your method cannot reproduce a known answer, its new answers mean nothing.
2. **Pilot.** Run the whole procedure on two to five items before the main run. The pilot finds the steps that take three times longer than planned and gives the first estimate of scatter, which you need to decide how many repeats to do.
3. **Blanks and controls.** A blank is a run without the thing you measure (the indicator blank in [10.6](../module-10/lesson-06.md)); a control is a run where you know the answer. They separate your signal from the method's own response.
4. **Randomised order.** Do the measurements in a shuffled order, not brand by brand. Drift (a solution ageing, a phone camera warming up, a laptop updating its software) then spreads over all groups instead of looking like a difference between them.
5. **Held-out check.** In a data or computational project, keep some items aside and never use them to fit anything. A scale factor or a model is then tested on items it has not seen. An error measured on the items used for fitting is always too optimistic.

Write the **analysis plan** before you see the main results: which number you will report, which items you may exclude and why, and which test decides the question. Deciding these after seeing the data makes it easy to pick, without meaning to, the version that looks best.

### How many repeats

The 95 % confidence interval of a mean of $n$ repeats (Lesson [09.2](../module-09/lesson-02.md)) is

$$\bar{x} \pm t_{0.975,\,n-1}\,\frac{s}{\sqrt{n}}$$

where $s$ is the sample standard deviation and $t$ the Student t value. The half-width shrinks with $\sqrt{n}$, and for small $n$ also because $t$ falls (12.7 for $n$ = 2, 2.78 for $n$ = 5, 2.26 for $n$ = 10). Turn it around: take $s$ from the pilot, choose the half-width you need to answer your question, and find the smallest $n$ that reaches it. If the answer is 40 titrations, the method is too noisy for the question and you improve the method, not the count.

Uncertainties that do not average away (a calibration error, a wrong label on the balance) are not reduced by repeats at all. Lesson [09.3](../module-09/lesson-03.md) shows how to add them to the budget.

### How many molecules

In a benchmark, the question is not repeats but population size. Two things settle at different speeds. A single parameter such as a scale factor is pinned down by a few molecules, because every mode contributes. The typical error (RMS) of the method needs more, because it describes the scatter itself, and a few unlucky molecules move it a lot. Twenty to thirty molecules, with a held-out set of ten, is a sensible size for a home benchmark.

### Managing the data

Use one folder per project with a fixed layout (after Wilson et al. 2017):

```text
my-ir-benchmark/
  README.md          what, how to rerun, licence, contact
  hours_log.csv      date,phase,hours,note
  requirements.txt   pinned versions
  data/raw/          original files, never edited
  data/processed/    written only by code
  data/README.md     data dictionary
  src/run_all.py     rebuilds every result from data/raw
  results/           figures and tables, written only by code
  notebook/          dated pages
  doc/               proposal, report, poster, feedback
```

Four rules make it work:

- **Raw data are read-only.** Download or record them once, note the source, licence and date in the data dictionary, and make the files read-only. Every correction happens in code, so it is visible and repeatable.
- **Every result is rebuilt by code.** `run_all.py` goes from raw data to every figure and table. If a number in the report did not come from it, you cannot defend it.
- **Every file and column is described.** The data dictionary lists each file with its source, licence and date, and each column with its unit. This is the small-scale version of the FAIR principles: data that are Findable, Accessible, Interoperable and Reusable.
- **Version control and two copies.** Put the folder under git ([05.5](../module-05/lesson-05.md)) and commit at the end of each session with a message saying what changed. Keep a second copy somewhere else (another disk or a cloud folder).

The **hours log** is one line per working session: date, phase, hours, a note. It shows where the 180 hours went and is the evidence that the project was done at the stated size. The **notebook** ([01.3](../module-01/lesson-03.md)) records what you did and saw on each day, including failures.

## Worked example

### How many dye-fading runs?

Amir's question: does a 10 °C rise in water temperature double the rate of food-dye fading in dilute bleach ([23.4](../module-23/lesson-04.md))? He needs each rate constant to ±0.10 × 10⁻³ s⁻¹ (95 %) to tell a factor of 2 from a factor of 1.5. His pilot at room temperature gives four runs:

$$k = 2.31,\ 2.47,\ 2.20,\ 2.43 \times 10^{-3}\ \text{s}^{-1}$$

Mean 2.35, $s$ = 0.122 (same unit). With the 4 pilot runs the half-width is $3.18 \times 0.122/\sqrt{4} = 0.19$: too wide. Trying larger $n$:

| $n$ | $t_{0.975,\,n-1}$ | half-width |
|---|---|---|
| 8 | 2.36 | 0.102 |
| 9 | 2.31 | 0.094 |

He needs 9 runs at each temperature. With two temperatures that is 18 runs; he shuffles them (cold, warm, warm, cold, …) so that the slow ageing of the bleach solution over the day spreads over both groups. He also writes his analysis plan now: report $k$ at each temperature with its 95 % interval, and the ratio with its propagated uncertainty ([09.3](../module-09/lesson-03.md)); exclude a run only if the camera exposure changed, noted in the notebook at the time.

### Fitting on the data you test on

Noa fits a scale factor to 3 of her molecules and reports an RMS error of 10.6 cm⁻¹. On 10 molecules she never used for fitting, the same scale factor gives 15.1 cm⁻¹. The first number is too optimistic for two reasons: the fit was tuned to those molecules, and three molecules are too few to estimate a scatter. With 20 fitting molecules the two numbers are 11.6 and 14.3 cm⁻¹ and stable from draw to draw. She reports the held-out value.

## Hands-on

What you need: the [Module 33 lab folder](../../labs/module-33/), your proposal from 33.1, the [notebook page template](../../templates/notebook-page.md) and the [error analysis template](../../templates/error-analysis.md). Time: about 3 hours, plus the pilot itself.

1. **Create the project folder (15 min).** Choose a folder outside the course repository and run:

```bash
py make_project.py ../../../my-project
```

Open the README and write one sentence: the question. Put the folder under git and make the first commit.

2. **Write the design (45 min).** In `doc/proposal.md`, below the proposal, add: the known-answer test, the pilot (how many items), blanks or controls, the order of runs (write the shuffled list), the held-out set (which items), and the analysis plan.
3. **Run the known-answer test and the pilot (time depends on the project).** Record each session in `hours_log.csv` and on a dated notebook page. Put the raw files in `data/raw/` and describe each in `data/README.md` with source, licence, date and units.
4. **Decide the numbers (30 min).** Complete the two TODO functions in `lesson02_sample_size.py` (`ci_halfwidth` and `repeats_needed`), check with the defaults, then use your own pilot:

```bash
py lesson02_sample_size.py
py lesson02_sample_size.py 0.122 0.10
```

5. **Write `src/run_all.py` for the pilot (45 min).** It reads `data/raw/`, writes the pilot table to `results/`, and runs from a fresh clone.

How you know it worked: a friend, or you in a week, can clone the folder, run `run_all.py` and get the same pilot table; the known-answer test reproduces the published value within your uncertainty; you have a number of repeats or molecules with a reason.

<details><summary>Reference output</summary>

`py lesson02_sample_size_solution.py` prints half-widths 0.298, 0.149, 0.111 and 0.086 for $n$ = 3, 5, 7 and 10 (pilot SD 0.12) and `need n = 9`. Part 2 (generated demo data, 10 molecules held out): the scale factor is 0.9613 ± 0.0019 from 3 molecules and 0.9614 ± 0.0007 from 10; the RMS estimated from the fitting set is 10.6 ± 2.1 cm⁻¹ from 3 molecules and 11.6 cm⁻¹ from 20, while the held-out RMS is 15.1 and 14.3 cm⁻¹. Lesson: the scale factor settles fast; the error estimate needs more molecules and must come from held-out data. (The held-out set here happens to scatter a little more than the rest, which is why its RMS stays higher.)

If the known-answer test fails, stop. Find the cause (wrong units, wrong mode assignment, an old solution) before you collect any main data.

</details>

## Common mistakes

- **No known-answer test.** Without it, a systematic error in your method looks like a finding. Reproduce one published value first.
- **Measuring groups in blocks.** Brand A on Monday, brand B on Thursday mixes brands with days. Shuffle the order.
- **Reporting the error on the fitting set.** It is too small. Report the held-out error.
- **Editing raw data by hand.** A deleted outlier in a spreadsheet leaves no trace. Exclusions happen in code, with the reason in the analysis plan.
- **Repeating a noisy method instead of improving it.** If the pilot says 40 repeats, fix the largest source of scatter first.
- **An hours log written from memory at the end.** Write one line after each session; it takes ten seconds.

## Key takeaways

- Every study needs a known-answer test, a pilot, blanks or controls, randomised order and, for models, a held-out set.
- Write the analysis plan before you see the main data.
- The number of repeats follows from the pilot SD and the half-width the question needs: $t\,s/\sqrt{n} \le$ target.
- Raw data are read-only, every result is rebuilt by code, every file and column is described, and the folder is under git with a second copy.

## Sources

- [Wilson et al. (2017), Good enough practices in scientific computing](https://doi.org/10.1371/journal.pcbi.1005510) — the project layout, raw data read-only, one script to rebuild results.
- [Wilkinson et al. (2016), The FAIR Guiding Principles](https://doi.org/10.1038/sdata.2016.18) and the [GO FAIR summary](https://www.gofair.foundation/fair-principles) — findable, accessible, interoperable, reusable data.
- [NIST/SEMATECH e-Handbook, confidence limits for the mean](https://www.itl.nist.gov/div898/handbook/eda/section3/eda352.htm) — the t-interval used for the number of repeats.
- [Git documentation](https://git-scm.com/doc) — version control for the project folder.
