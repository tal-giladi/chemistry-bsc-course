---
id: "10.6"
module: 10
minutes: 15
practice_minutes: 180
prerequisites: ["10.1", "10.4", "10.5", "09.2", "09.3", "08.7"]
objectives:
  - Plan and carry out five mass-based titrations of vinegar with an indicator blank, keeping a notebook that another person could follow.
  - Report the acetic acid content as mean, standard deviation and 95 % confidence interval, and show what the blank correction changes.
  - Build an uncertainty budget that combines Type A and Type B terms, and name the term that dominates.
  - Compare the result with the label using a t-test and the expanded uncertainty, and explain why the two can disagree.
volatility: concept
sources:
  - title: "LibreTexts — Harvey, Analytical Chemistry 2.1, 4.6 Statistical Methods for Normal Distributions"
    url: https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/04%3A_Evaluating_Analytical_Data/4.06%3A_Statistical_Methods_for_Normal_Distributions
  - title: "LibreTexts — Harvey, Analytical Chemistry 2.1, 16.4 Critical Values for t-Test"
    url: https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/16%3A_Appendix/16.04%3A_Critical_Values_for_t-Test
  - title: "JCGM 100:2008, Evaluation of measurement data — Guide to the expression of uncertainty in measurement (GUM)"
    url: https://www.bipm.org/en/doi/10.59161/jcgm100-2008e
  - title: "PubChem, Acetic acid (CID 176)"
    url: https://pubchem.ncbi.nlm.nih.gov/compound/176
  - title: "PubChem, Sodium bicarbonate (CID 516892)"
    url: https://pubchem.ncbi.nlm.nih.gov/compound/516892
last_verified: "2026-10-17"
---

# 10.6 · Project: home vinegar titration with full error analysis

This is the module's practical piece and the home version of the S3 lab course. You titrate white vinegar with baking-soda solution five times, by mass, with red-cabbage indicator and an indicator blank, and you report the acetic acid content the way an analytical lab would: a mean with its standard deviation and confidence interval, an uncertainty budget, and a test against the label. It uses the bench routine and drop size from lesson 10.1, the end-point reasoning from 10.2, the purity question from 10.4 and the statistics of Module 9. It ends in a lab report that someone else could check.

## Why it matters

A food inspector buys a bottle labelled "5 % acidity" and must decide whether it meets its label. Five titrations give 4.97 g per 100 mL. Is that "5 %", or is the producer diluting the product? The answer depends on two different questions. Do the repeats differ from 5.00 by more than their scatter? That is a t-test. And is 5.00 inside the full uncertainty, which also includes the scale, the end point and the titrant? Those questions can give opposite answers. Learning to keep them apart, and to say which one you are answering, is what turns a measurement into a decision.

## Core ideas

> [!NOTE]
> Stable: the titration chemistry and the GUM method of combining uncertainties. Checked 2026-10-17: acetic acid 60.052 g/mol and sodium bicarbonate 84.006 g/mol (PubChem); Student t values from Harvey Appendix 16.4. The example data come from `make_data.py`, a stated model with a true value of 4.95 % w/w, not a measurement.

### What changes from lesson 08.7

In lesson [08.7](../module-08/lesson-07.md) you did three trials and found that cabbage needs a little excess bicarbonate, so the results came out about 1 % high. Three changes fix that and tighten the result:

1. **An indicator blank.** Titrate 25 mL of water with the same 2 mL of indicator to the same blue-green. The titrant it takes is the excess the indicator needs, and you subtract it from every trial. This is the same idea as the Mohr blank in lesson [10.3](lesson-03.md).
2. **Five trials**, so the confidence interval uses $t = 2.78$ (4 degrees of freedom) instead of 4.30 for three trials. The interval shrinks by more than a third for the same scatter.
3. **A known drop size** (lesson [10.1](lesson-01.md)), so the end-point term in the budget is a number, not a guess.

### The result of one trial

With titrant made from $m_\mathrm{B}$ g of NaHCO₃ in $m_\text{sol}$ g of solution, its strength is $w = m_\mathrm{B}/(m_\text{sol}\,M_{\mathrm{NaHCO_3}})$ in mol per gram. For a trial with vinegar mass $m_v$, titrant mass $m_t$ and blank $m_\text{blank}$:

$$\%\,\mathrm{CH_3COOH}\ (w/w) = \frac{100\,(m_t - m_\text{blank})\,w\,M_{\mathrm{CH_3COOH}}}{m_v}$$

### Type A and Type B together

The **Type A** uncertainty comes from the repeats: $s/\sqrt{n}$ for the mean (lesson [09.2](../module-09/lesson-02.md)). The **Type B** terms come from what you know about the equipment (lesson [01.5](../module-01/lesson-05.md)):

- each mass found as a difference of two readings: $d/\sqrt{6}$, with $d$ the scale resolution;
- the end point, ± half a drop, rectangular: $(\text{drop}/2)/\sqrt{3}$;
- baking-soda purity, assumed 100 ± 0.5 %, rectangular: $0.5\,\%/\sqrt{3} = 0.29\,\%$.

The result is a product and quotient of these quantities, so their relative uncertainties add in quadrature (lesson [09.3](../module-09/lesson-03.md)):

$$\frac{u(c)}{c} = \sqrt{\sum_i \left(\frac{u_i}{x_i}\right)^2}$$

The **expanded uncertainty** $U = k\,u$ with coverage factor $k = 2$ gives an interval that should contain the true value about 95 % of the time. The share of each term in the total variance tells you what to improve next.

### Two ways to compare with the label

The **one-sample t-test** asks whether the mean differs from a reference value by more than the scatter of the repeats explains:

$$t = \frac{\bar{x} - \mu_0}{s/\sqrt{n}}$$

If $|t|$ is larger than the critical value (2.78 for $n = 5$ at 95 %), the difference is significant. But this test sees only random error. A systematic error, such as impure baking soda, shifts all five results together and is invisible to it. The second comparison asks whether the label value lies within $\bar{x} \pm U$. That interval includes the Type B terms. When the t-test says "different" but the label is inside $\pm U$, the honest conclusion is: the repeats are precise enough to detect a difference, but the difference is smaller than what the systematic uncertainties allow.

### Labels are in grams per 100 mL

Vinegar labels give "acidity" as grams of acetic acid per 100 mL. Your result is per 100 g. Multiply by the density, about 1.005 g/mL for white vinegar, to compare.

## Worked example

### The example data set

`vinegar_project_example.csv` holds five trials and a blank. Titrant: 5.00 g NaHCO₃ made up to 100.00 g, so $w = 5.00/(100.00 \times 84.006) = 5.952 \times 10^{-4}$ mol/g. The blank used 0.06 g.

Trial 1: 5.16 g of vinegar, 7.18 g of titrant.

$$\% = \frac{100 \times (7.18 - 0.06) \times 5.952 \times 10^{-4} \times 60.052}{5.16} = 4.932\,\%\ w/w$$

All five: 4.932, 4.929, 4.943, 4.953 and 4.980 %. Mean 4.948 %, $s$ = 0.021 %, RSD 0.42 %.

$$\text{95 \% CI} = 4.948 \pm \frac{2.78 \times 0.021}{\sqrt{5}} = 4.948 \pm 0.026\,\%$$

Without the blank the mean would be 4.990 %. The model's true value is 4.95 %, so the blank removed almost all of the 1 % end-point bias seen in lesson 08.7.

### The budget

| Term | Relative u | Share of variance |
|---|---|---|
| NaHCO₃ purity, ±0.5 % rectangular | 0.29 % | 48 % |
| Repeatability, $s/\sqrt{5}$ | 0.19 % | 20 % |
| End point, half a 45 mg drop over 7 g | 0.19 % | 20 % |
| Vinegar mass and NaHCO₃ mass, scale | 0.08 % each | 4 % each |
| Titrant and blank mass, scale | 0.06 % each | 2 % each |

Combined: 0.42 % relative, so $u$ = 0.021 % and $U$ = 0.04 %. Result: **4.95 ± 0.04 % w/w** ($k$ = 2). The biggest term is not the scale or the end point but what you assumed about the baking soda. Your oven measurement in lesson [10.4](lesson-04.md) is a way to shrink it.

### Against the label

Per 100 mL: $4.948 \times 1.005 = 4.97$ g/100 mL, with $U$ = 0.04. The t-test gives $t = (4.972 - 5.000)/(0.021/\sqrt{5}) = -2.98$, beyond 2.78: significantly different, on repeatability alone. But 5.00 lies within 4.97 ± 0.04. Conclusion: the vinegar contains slightly less than 5.0 g/100 mL, but the difference (0.6 %) is within what the purity of the baking soda and the end point allow. You cannot claim the label is wrong.

## Hands-on

What you need: white vinegar ("5 % acidity" on the label), baking soda, the red-cabbage indicator from lesson 08.4 (fresh, or kept in the fridge for no more than a few days), a 10 mL oral syringe, a kitchen scale with 0.01 g resolution, 6 small cups or glasses, a white sheet of paper as background, safety glasses, a tray, the [Module 10 lab folder](../../labs/module-10/) and the [lab report template](../../templates/lab-report.md). Time: about 3 hours including the report.

> [!WARNING]
> Wear safety glasses: vinegar and baking soda fizz and can spurt when swirled. Use only household white vinegar (about 5 %), never concentrated "cleaning vinegar" or vinegar essence, which is corrosive. Never mix vinegar with bleach: it releases chlorine gas. Work over a tray and rinse everything down the sink afterwards.

### Part A — warm-up in the simulation (15 min)

[Simulation: Titration bench — choosing an indicator](../../simulations/titration/index.html?preset=indicator-choice)

Titrate the weak acid three times with phenolphthalein, adding single drops near the end. Note how many drops past equivalence your end points are. Target: three end points within one drop of each other.

### Part B — plan and prepare (20 min)

1. Copy the [notebook page template](../../templates/notebook-page.md). Write the aim, the reaction, the safety notes and an empty table for the five trials and the blank.
2. **Titrant.** Weigh 5.00 g of baking soda into a clean cup, add water to a total of 100.00 g, and stir until clear. Record both masses exactly; type them into the SETUP block of `project_vinegar.py`, together with your drop mass from lesson 10.1.
3. **Plan the sample size.** About 5.0 g of vinegar needs about 7 g of titrant, so one syringe-and-a-bit per trial.

### Part C — the blank and five trials (90 min)

1. **Blank.** In a cup, put about 25 mL of water and 2 mL of cabbage indicator. Fill and weigh the syringe, add titrant drop by drop until the colour matches the blue-green you will use as the end point, and weigh again. Keep this cup as your colour reference.
2. **Trial.** Weigh about 5 g of vinegar into a cup (record it to 0.01 g), add about 20 mL of water and 2 mL of indicator.
3. Fill the syringe, wipe it, weigh it. Add titrant 1 mL at a time while swirling until the fizzing slows, then drop by drop with hard swirling between drops. Stop at the first blue-green that matches the reference cup and lasts 30 seconds.
4. Weigh the syringe again. If you needed a refill, record both fills.
5. Repeat steps 2–4 four more times. Do not discard a trial because it looks odd: note what happened and test it later with Grubbs' test (lesson 09.2).
6. Type the data into a CSV file: `trial,m_vinegar_g,m_syringe_before_g,m_syringe_after_g`, with a final row `blank,0.00,…,…`.

How you know it worked: each trial uses 6.8–7.2 g of titrant per 5 g of vinegar, the five results agree within about 1 % (RSD below 0.6 %), and the blank needs 1–3 drops.

### Part D — analysis and report (45 min)

Fill in `acid_percent` and `t_statistic` in `project_vinegar.py`, then run:

```bash
py project_vinegar.py
py project_vinegar.py my_vinegar.csv
```

With the example file it prints the five results, mean 4.948 %, SD 0.021 %, CI ± 0.026 %, the budget sorted by size, $U$ = 0.04 %, $t$ = −2.98, and the comparison with the label. Write the report with the lab report template: aim, method in your own words, data table, results with uncertainty, the budget table, the comparison with the label, and a discussion that names the largest term and how you would reduce it.

<details><summary>Reference solution and what a good discussion says</summary>

`acid_percent` returns `100 * (m_titrant - m_blank) * w_titrant * M_ACETIC / m_vinegar`; `t_statistic` returns `(mean - reference) / (sd / math.sqrt(n))`. Full code in `project_vinegar_solution.py`.

A good discussion says: the blank corrects the indicator excess (compare the mean with and without it); the confidence interval covers only random scatter; the largest Type B term is the baking-soda purity, which an oven test (10.4) or a standardisation against a second material could reduce; the end-point term could be halved with smaller drops (a fine-tipped dropper) or a potentiometric end point (10.2); the t-test and the expanded uncertainty answer different questions; and the result is per 100 g, converted to per 100 mL with an assumed density. A real kitchen result between 4.8 and 5.2 g/100 mL with an RSD below 1 % is a good measurement.

</details>

## Common mistakes

- **Skipping the blank or titrating it to a different colour.** The blank must match the end-point colour you use in the trials; keep the blank cup next to you as a reference.
- **Using a stale indicator.** Cabbage extract changes colour and grows mould after a few days at room temperature. Make it fresh or keep it cold.
- **Dropping a trial because it is inconvenient.** Only a gross error with a recorded cause, or a failed Grubbs' test, justifies removing a result.
- **Reporting the CI as the full uncertainty.** It ignores purity, scale and end-point terms. Report $U$ from the budget as well.
- **Comparing % w/w with a g/100 mL label.** Convert with the density before you compare.
- **Calling the label wrong on a t-test alone.** A significant t with the label inside $\pm U$ means "different, but within what systematic uncertainty allows".

## Key takeaways

- An indicator blank removes most of the end-point bias of a visual titration.
- Five repeats give a 95 % CI with $t$ = 2.78; with a kitchen scale and a known drop size, an RSD near 0.5 % is achievable.
- The uncertainty budget combines Type A and Type B terms in quadrature; its largest term, here reagent purity, tells you what to improve.
- A t-test sees only random error; the expanded uncertainty includes systematic terms. State which question you are answering.
- A complete report gives the value, its uncertainty, the method and an honest discussion of what limits it.

## Sources

- [Harvey, Analytical Chemistry 2.1, 4.6 Statistical Methods for Normal Distributions](https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/04%3A_Evaluating_Analytical_Data/4.06%3A_Statistical_Methods_for_Normal_Distributions) — one-sample t-test against a reference value.
- [Harvey, Analytical Chemistry 2.1, 16.4 Critical Values for t-Test](https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/16%3A_Appendix/16.04%3A_Critical_Values_for_t-Test) — t = 2.78 for 4 degrees of freedom at 95 %.
- [JCGM 100:2008 (GUM)](https://www.bipm.org/en/doi/10.59161/jcgm100-2008e) — Type A and Type B uncertainties, combined and expanded uncertainty.
- [PubChem, Acetic acid](https://pubchem.ncbi.nlm.nih.gov/compound/176) — molar mass 60.052 g/mol; hazards of the concentrated acid.
- [PubChem, Sodium bicarbonate](https://pubchem.ncbi.nlm.nih.gov/compound/516892) — molar mass 84.007 g/mol; not GHS-classified.
