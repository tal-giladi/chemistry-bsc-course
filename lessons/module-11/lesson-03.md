---
id: "11.3"
module: 11
minutes: 20
practice_minutes: 150
prerequisites: ["11.2", "01.3", "05.2", "10.6"]
objectives:
  - Write a results paragraph whose first sentence states the result as value, uncertainty and unit, with the meaning of the uncertainty.
  - Match the strength of each claim to the evidence, using tense and hedging words correctly.
  - List the problems in a misleading figure and redraw it so that one message is clear, the data are visible and colours are colour-blind safe.
  - Write a complete lab report from your own data and check it against a self-check list.
volatility: concept
sources:
  - title: "Rougier, Droettboom and Bourne (2014), Ten simple rules for better figures, PLoS Computational Biology 10(9), e1003833"
    url: https://doi.org/10.1371/journal.pcbi.1003833
  - title: "Weissgerber et al. (2015), Beyond bar and line graphs: time for a new data presentation paradigm, PLOS Biology 13(4), e1002128"
    url: https://doi.org/10.1371/journal.pbio.1002128
  - title: "Crameri, Shephard and Heron (2020), The misuse of colour in science communication, Nature Communications 11, 5444"
    url: https://doi.org/10.1038/s41467-020-19160-7
  - title: "Mensh and Kording (2017), Ten simple rules for structuring papers, PLOS Computational Biology 13(9), e1005619"
    url: https://doi.org/10.1371/journal.pcbi.1005619
  - title: "Matplotlib 3.11 — Choosing colormaps"
    url: https://matplotlib.org/stable/users/explain/colors/colormaps.html
  - title: "NIST SP 811 — Guide for the Use of the International System of Units"
    url: https://www.nist.gov/pml/special-publication-811
last_verified: "2026-10-17"
---

# 11.3 · Writing a lab report and a figure that tells the story

A lab report succeeds when a reader who was not there finds your result, believes it to the right degree, and could repeat the work. This lesson adds the writing skills to the report structure from lesson 01.3: paragraphs that make one point each, sentences that carry numbers properly, claims as strong as the evidence and no stronger, and figures that show the data and state their message. In the module practical you redraw a misleading figure and write the full report of your vinegar project.

## Why it matters

Two learners titrate the same vinegar and get the same numbers. One writes "very good results were obtained, which prove the label is correct" under a bar chart with no units. The other writes "4.97 ± 0.04 g/100 mL (k = 2), consistent with the label's 5.0 g/100 mL" under a plot of every titration. A reader trusts the second and can check it. The first gives the reader nothing to check, so a careful reader trusts nothing in it.

## Core ideas

### The report and its reader

The sections are those of lesson [01.3](../module-01/lesson-03.md) and the [lab report template](../../templates/lab-report.md): aim, background, method, safety, results, analysis, discussion, conclusion, references. Write for a reader who knows chemistry but was not in your kitchen. Write the results and figures first, then the method, the discussion, the introduction, and the abstract last.

### Paragraphs: one point, stated first

Mensh and Kording recommend that every paragraph, like every paper, follow **context – content – conclusion**: the first sentence says what the paragraph is about, the middle gives the evidence, the last says what it means. In a report the most useful form is: **the first sentence states the point.** A reader who reads only first sentences should get the whole story. Test it with a **reverse outline**: list the first sentence of every paragraph and read the list alone.

### Sentences that carry numbers

A result sentence has a value, its uncertainty, a unit, and what the uncertainty means (lesson [09.2](../module-09/lesson-02.md)):

> The acetic acid content was 4.948 ± 0.026 % w/w (mean ± 95 % confidence interval, n = 5).

Rules that make numbers readable:

- Say what "±" is: standard deviation, 95 % confidence interval, or expanded uncertainty with its coverage factor $k$.
- Round the uncertainty to one or two significant figures, and the value to the same decimal place (lesson [01.2](../module-01/lesson-02.md)).
- Put a space between number and unit (5.0 mL), and write units in table headers and axis labels as "quantity / unit", as NIST SP 811 recommends.
- Refer to the evidence: "(Table 1)", "(Figure 2)".

### Tense, voice and hedging

- **Past tense** for what you did and saw: "The titrant was added dropwise." "The end point was reached at 8.35 mL."
- **Present tense** for accepted facts and for what your figures show: "Acetic acid is a weak acid." "Figure 1 shows all thirty titrations."
- **Active or passive**: both are fine; prefer the active voice ("we weighed") when it is shorter.
- **Hedging** should match the evidence. "The data show" when the result is inside a stated uncertainty and the comparison is direct. "The data suggest" when it is indirect or n is small. "May" for a possible cause you did not test. Never "prove" for a measurement: measurements support, they do not prove.
- Cut empty words ("very good results", "human error"); name the specific result or error instead.

### Figures that tell the story

Rougier, Droettboom and Bourne list ten rules for figures. The ones that matter most for lab reports:

1. **Identify your message.** One figure, one message, sayable in one sentence.
2. **Captions are not optional.** Say what is plotted, what symbols and error bars mean, n, and the message. A **sentence title** ("D reads high") does this on a slide.
3. **Do not trust the defaults.** They were not designed for your message.
4. **Use colour effectively.** Colour should encode something, and work in greyscale.
5. **Do not mislead.** Axes, scales and aspect ratio must not exaggerate or hide differences.
6. **Avoid chartjunk.** Remove 3D effects, heavy grids and legends that repeat the axis.

Three further rules come from the literature:

- **Show the data when n is small.** Weissgerber and colleagues showed that bar charts of means hide the distribution: very different data sets give the same bars. For fewer than about 20 points per group, plot every point, with the mean and its interval beside them.
- **Bars start at zero.** A bar's length encodes its value, so a cut axis makes small differences look large. A dot plot has no length, so it may zoom in.
- **Avoid rainbow colour maps.** Crameri, Shephard and Heron showed that rainbow maps such as "jet" distort data (bright bands look like features) and are unreadable for many colour-blind readers. Use perceptually uniform maps such as viridis or cividis for continuous data, and a colour-blind-safe palette (for example Okabe–Ito) for categories. Matplotlib's default map has been viridis since version 2.0.

Every axis needs a quantity and a unit, written as in lesson [05.2](../module-05/lesson-02.md): "volume of NaOH added / mL", "pH" (no unit), "ΔpH/ΔV / mL⁻¹".

> [!NOTE]
> The writing and figure rules here are stable; they come from papers published between 2014 and 2020 and from long-standing SI conventions. The plotting code was checked with Matplotlib 3.11.2 on Python 3.14 (2026-10-17); colour-map names and the `layout="constrained"` option may change in later versions.

## Worked example

### 1. Rewriting a results paragraph

A first draft, based on the example data of lesson [10.6](../module-10/lesson-06.md):

> The experiment was performed and very good results were obtained. The concentration was found to be 4.9483 % which is very close to the label and proves that the vinegar is correct. The error was small. Figure 1 shows the results. Some errors could be due to human error.

What is wrong: the point comes last or never; "very good", "very close" and "small" have no numbers; 4.9483 has more digits than the data support; "%" is not said to be w/w, while the label is in g/100 mL; "proves" is too strong; "human error" names nothing; the uncertainty is missing.

The rewrite, first sentence first:

> The five blank-corrected titrations gave an acetic acid content of 4.948 ± 0.026 % w/w (mean ± 95 % confidence interval; SD 0.021 %, n = 5; Table 1). With an assumed density of 1.005 g/mL this is 4.97 ± 0.04 g/100 mL (expanded uncertainty, k = 2), consistent with the label value of 5.0 g/100 mL. The largest term in the uncertainty budget was the purity of the baking soda, not the scatter of the repeats (Table 2); drying the baking soda in an oven before use would reduce it.

Every adjective became a number, every claim points to its evidence, and the limitation is specific enough to act on.

### 2. Redrawing a misleading figure

Six learners titrated the same vinegar five times each (simulated data in the lab folder, modelled on lesson 10.6). One learner also recorded a pH titration curve. Here is a figure of the kind often handed in:

![Two-panel figure drawn badly: a bar chart of six learners' mean results with rainbow colours, upward-only error bars, a y-axis cut at 4.85 and labelled only "Result"; and a titration curve with a rainbow-coloured derivative on a second unlabelled axis with a colour bar](../../assets/m11-bad-figure.svg)

The problems, in the order a reader meets them:

1. Neither title says anything ("Results", "Titration"), and the left axis says "Result" with no quantity or unit. The right panel has no axis labels at all.
2. Bars of five values hide the points. Learner C's mean is pulled down by one spilled titration, but the reader cannot see that.
3. The bar axis starts at 4.85, so C's bar looks a quarter the height of D's for a 2.5 % difference.
4. The error bars point only upward, are not defined, and use the population formula ($n$ instead of $n-1$).
5. Rainbow (jet) colours encode nothing, are not colour-blind safe, and the legend repeats the x-axis labels.
6. The derivative shares the panel on a second y-axis with a different scale, and a colour bar encodes the volume a second time.
7. The heavy grid competes with the data, and the end point, the whole purpose of the curve, is not marked.

The redrawn figure, produced by `good_figure_solution.py`:

![Two-panel figure drawn well: every titration shown as a point with each learner's mean and 95 % confidence interval, learner D highlighted in orange as lacking a blank and C's spill labelled; and the titration curve with its first derivative in an aligned panel below, the end point at 8.35 mL marked by a dashed line](../../assets/m11-good-figure.svg)

Its caption:

> **Figure 1.** (a) Acetic acid content of one vinegar measured by six learners, five titrations each (simulated data). Points: single titrations; squares: mean ± 95 % confidence interval. Learner D did not subtract the indicator blank and reads about 0.07 % high; C's low value followed a spill; F used a 0.1 g scale. (b) Potentiometric titration of 10.00 mL of diluted vinegar with 0.1000 mol/L NaOH; the end point, 8.35 mL, is the midpoint of the steepest interval (equivalence volume of the model: 8.30 mL).

With 0.1 mL steps the derivative locates the end point only to about ±0.05 mL; the figure makes that limit visible.

## Hands-on

What you need: the [Module 11 lab folder](../../labs/module-11/) with Python 3.14 and the pinned packages (lesson [05.1](../module-05/lesson-01.md); this lab needs numpy, scipy and matplotlib); your data and notebook from the vinegar project in lesson [10.6](../module-10/lesson-06.md) (or from the phone calibration in lesson [09.6](../module-09/lesson-06.md)); the [lab report template](../../templates/lab-report.md); the self-check list `writing_checklist.md` in the lab folder. Time: about 2.5 hours. Together with the paper summary from lesson [11.1](lesson-01.md), this is the module's practical piece.

### Part A — redraw a figure (45 min)

1. Run the bad figure and open `runs/bad_figure.png`:

```bash
py bad_figure.py
```

2. Before reading the list in the worked example, write down every problem you see.
3. Open `good_figure.py` and complete the three TODOs: the standard deviation and 95 % confidence interval of each learner (TODO 1), the first derivative and its end point (TODO 2), and every axis label as "quantity / unit" (TODO 3).
4. Run it and compare `runs/good_figure.png` with the figure above:

```bash
py good_figure.py
```

5. Write a caption for your figure in your own words, with a first sentence that states its message.

How you know it worked: the script prints, for learner D, mean 5.018 %, s 0.011 %, CI half-width 0.013 %; for C, s 0.111 % and half-width 0.137 %; and an end point of 8.35 mL.

<details><summary>Reference solution for the TODOs</summary>

```python
# TODO 1
s = x.std(ddof=1)
half = stats.t.ppf(0.975, n - 1) * s / np.sqrt(n)
# TODO 2
vm = (v[1:] + v[:-1]) / 2
d = np.diff(ph) / np.diff(v)
return vm, d, vm[np.argmax(d)]
# TODO 3
ax.set_ylabel("acetic acid / % w/w")
top.set_ylabel("pH")
bot.set_ylabel("ΔpH/ΔV / mL⁻¹")
bot.set_xlabel("volume of NaOH added / mL")
```

`ddof=1` gives the sample standard deviation with $n-1$; with $n = 5$, $t_{0.975,4} = 2.776$. The full script is `good_figure_solution.py`.

</details>

### Part B — write the full report (90 min)

1. Use the template's sections. Draft the results first: one table of raw data (quantity / unit headers), one figure drawn with the rules above, and the result sentence in the form of Worked example 1.
2. Write the method in the past tense, complete enough to repeat. Then the discussion: compare with the label inside your uncertainty, name the largest uncertainty term and one concrete improvement, and say what the home version could not show compared with a real lab.
3. Cite every value you did not measure as close to the measurement as you can, with the date for online sources (lesson [11.2](lesson-02.md)).
4. Write the abstract last: aim, method in one line, result with uncertainty, conclusion; 3–5 sentences.

### Part C — check it (15 min)

1. Make a reverse outline: copy the first sentence of every paragraph into a list. Read only the list. Does it tell the whole story? If not, move the point to the front of the paragraph.
2. Go through `writing_checklist.md` line by line and fix every unticked item.
3. Search your text for "very", "proves", "human error" and "it is interesting". Replace each with something specific, or delete it.

How you know it worked: a reader who sees only the abstract, the figure with its caption and the reverse outline can state your result with its uncertainty and its main limitation.

## Common mistakes

- **Burying the result.** If the number with its uncertainty is not in the first sentence of the results and in the abstract, readers miss it.
- **Undefined error bars and "±".** SD, standard error and 95 % CI differ by large factors. Always say which, and give n.
- **Bars for a handful of points.** Show the points; bars hide outliers, skew and groups.
- **Cut bar axes and rainbow colours.** Both distort what the reader sees. Start bars at zero or use dots; use viridis or a colour-blind-safe palette.
- **Claims stronger than the data.** A measurement supports or is consistent with; it does not prove.
- **Writing in the order you worked.** Readers want the result first. Write results and figures first, the abstract last.

## Key takeaways

- Write for a reader who was not there: results first, one point per paragraph, stated in the first sentence.
- A result is value ± uncertainty, unit, and what the uncertainty means, with digits to match.
- Use the past tense for what you did, the present for facts and figures, and hedging that matches the evidence.
- A figure has one message, shows the data when n is small, labels every axis as quantity / unit, defines its error bars and avoids misleading axes and rainbow colours.
- Check the report with a reverse outline and a self-check list before anyone else reads it.

## Sources

- [Rougier, Droettboom and Bourne (2014), Ten simple rules for better figures, PLoS Comput Biol 10(9), e1003833](https://doi.org/10.1371/journal.pcbi.1003833).
- [Weissgerber et al. (2015), Beyond bar and line graphs, PLOS Biol 13(4), e1002128](https://doi.org/10.1371/journal.pbio.1002128) (show the data for small samples).
- [Crameri, Shephard and Heron (2020), The misuse of colour in science communication, Nat Commun 11, 5444](https://doi.org/10.1038/s41467-020-19160-7) (rainbow maps distort data and exclude colour-blind readers).
- [Mensh and Kording (2017), Ten simple rules for structuring papers, PLOS Comput Biol 13(9), e1005619](https://doi.org/10.1371/journal.pcbi.1005619).
- [Matplotlib 3.11 — Choosing colormaps](https://matplotlib.org/stable/users/explain/colors/colormaps.html) (checked 2026-10-17).
- [NIST SP 811](https://www.nist.gov/pml/special-publication-811).
