---
id: "25.5"
module: 25
minutes: 22
practice_minutes: 80
prerequisites: ["19.4", "19.5", "08.4"]
objectives:
  - Choose the HPLC mode, column, mobile-phase pH, buffer and organic solvent for a set of analytes from their pKa, log P and UV absorption.
  - Fit the linear-solvent-strength model to two scouting runs and predict retention and resolution at any solvent composition.
  - Use a resolution map to pick an isocratic composition, and quantify how sensitive the separation is to pH near an analyte's pKa.
  - Run a system-suitability test from replicate injections and decide whether a column may still be used, and list what a validation must show.
volatility: implementation
sources:
  - title: "Harvey, Analytical Chemistry 2.1, 12.5 High-Performance Liquid Chromatography (LibreTexts)"
    url: https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_(Harvey)/12%3A_Chromatographic_and_Electrophoretic_Methods/12.05%3A_High-Performance_Liquid_Chromatography
  - title: "PubChem, Aspirin (CID 2244)"
    url: https://pubchem.ncbi.nlm.nih.gov/compound/2244
  - title: "PubChem, Salicylic acid (CID 338)"
    url: https://pubchem.ncbi.nlm.nih.gov/compound/338
  - title: "PubChem, Acetaminophen (CID 1983)"
    url: https://pubchem.ncbi.nlm.nih.gov/compound/1983
  - title: "PubChem, Caffeine (CID 2519)"
    url: https://pubchem.ncbi.nlm.nih.gov/compound/2519
  - title: "EMA, ICH Q2(R2) Validation of analytical procedures (effective 14 June 2024)"
    url: https://www.ema.europa.eu/en/ich-q2r2-validation-analytical-procedures-scientific-guideline
  - title: "Phenomenex, What is USP Chapter 621?"
    url: https://www.phenomenex.com/resources/blog/what-is-usp-chapter-621
last_verified: "2026-10-17"
---

# 25.5 · HPLC method thinking

An HPLC method is a chain of decisions: which column, which pH, which solvent and how much of it, isocratic or gradient, and what the system must show before every run. Good chromatographers make most of those decisions on paper, from the structures of the analytes and two scouting runs, before they spend a day at the instrument. This lesson takes a painkiller tablet with paracetamol, caffeine and aspirin, plus aspirin's breakdown product salicylic acid, and builds its method step by step. It uses the column theory of [Lesson 19.3](../module-19/lesson-03.md), the instrument of [Lesson 19.4](../module-19/lesson-04.md) and the validation numbers of the caffeine practical in [Lesson 19.5](../module-19/lesson-05.md).

## Why it matters

Aspirin slowly hydrolyses to salicylic acid and acetic acid, faster in warm, humid storage. A quality lab must report the salicylic acid in each batch of a combination tablet, so the method has to separate four compounds, quantify a small impurity next to a large peak, and give the same answer in a lab in another country on another instrument. A method developed by trial and error often works on the day and fails in transfer: run at pH 3.5, it separates beautifully, but a buffer made 0.1 pH unit off moves the aspirin peak by 10 % and the order of two peaks can flip. Method thinking finds those weak points before they become a failed batch.

## Core ideas

> [!NOTE]
> Stable: reversed-phase retention, the effect of pH on weak acids and bases, the linear-solvent-strength model and the logic of system suitability (Harvey 12.5, checked 2026-10-17). These change: column chemistries, pharmacopoeial system-suitability limits (USP <621>, harmonised with the European and Japanese pharmacopoeias) and validation guidance (ICH Q2(R2), effective in the EU since 14 June 2024, together with ICH Q14 on method development). Acceptance limits below are typical values; the monograph or your validated method sets the real ones. pKa and log P: PubChem. Lab data are simulated.

### Start from the molecules

| Compound | pKa | log P | Retained as |
|---|---|---|---|
| paracetamol (acetaminophen) | 9.4 (phenol) | 0.46 | neutral at any pH below 8 |
| caffeine | 0.7 (conjugate acid) | −0.07 | neutral above pH 2 |
| aspirin | 3.5 (carboxylic acid) | 1.19 | neutral only at low pH |
| salicylic acid | 3.0 (carboxylic acid) | 2.26 | neutral only at low pH |

All four are small and moderately polar with log P between −0.1 and 2.3, so **reversed phase** on a C18 column fits: a non-polar stationary phase, water plus an organic solvent as mobile phase, and the more hydrophobic compound elutes later. All four absorb UV strongly; 230 nm sees them all.

### pH decides for acids and bases

A carboxylic acid is retained as the neutral molecule; its anion is far more water-loving and comes out almost at once. The neutral fraction is

$$f_\text{HA} = \frac{1}{1 + 10^{\,\mathrm{pH} - \mathrm{p}K_\mathrm{a}}}$$

and retention follows it. Near the pKa, $f$ changes fastest: at pH = pKa, a 0.1 pH error changes $k$ by about 11 %. Two pH units below the pKa, the same error changes $k$ by 0.2 %. The rule: buffer at least 1.5–2 units away from every pKa, or accept a fragile method. For these acids that means pH ≈ 2.5, close to the lower limit of ordinary silica C18 columns (about pH 2). Use 25 mM phosphate for UV detection, or formic acid if the method must also run on LC-MS, because phosphate is not volatile.

### Which organic solvent

Acetonitrile has lower viscosity (lower pressure, Lesson 19.4) and transmits UV down to about 190 nm; methanol is cheaper and gives different selectivity, useful when two peaks will not separate. Start with acetonitrile; keep methanol as the selectivity lever.

### Scouting and the linear-solvent-strength model

For small molecules, the logarithm of the retention factor falls almost linearly with the volume fraction $\varphi$ of organic solvent:

$$\log_{10} k = \log_{10} k_w - S\,\varphi$$

$k_w$ is the (extrapolated) retention in pure water and $S$ is typically 3–6 for molecules of this size. With $S$ = 4, adding 10 % organic divides $k$ by $10^{0.4}$ ≈ 2.5, the chromatographer's "rule of three". Two isocratic runs, or two gradients, give $k_w$ and $S$ for every compound. Because the $S$ values differ, the lines can cross: two compounds may swap order as $\varphi$ changes, and resolution falls to zero at the crossing.

### The resolution map

With $k(\varphi)$ for each compound and the Purnell equation (Lesson 19.3), you can compute the resolution of the worst pair at every composition without another injection. The best isocratic composition is the highest point on that map that keeps the run short enough. If no composition gives all compounds $1 \lesssim k \lesssim 10$, the retention range is too wide for isocratic elution and a gradient is the answer (the general elution problem of Lesson 19.4).

### System suitability and validation

Before each sequence, a **system-suitability test** (SST) injects a reference mix, typically five or six times, and checks that the system can do the job today:

| Check | Typical limit | Protects against |
|---|---|---|
| resolution of the critical pair | ≥ 2.0 | peaks merging as the column ages |
| tailing factor | ≤ 2.0 | inaccurate integration of small peaks next to big ones |
| area RSD of replicate injections | ≤ 2.0 % | an unreliable injector or pump |
| plate number | above a set value | a damaged or contaminated column |

**Validation** happens once, before the method is used, and shows it is fit for purpose: specificity (the impurity is measured without interference), range and linearity of the response, accuracy (recovery), precision (repeatability and between days or analysts), and detection and quantitation limits for impurities. Robustness, how much small changes in pH, temperature or % organic matter, is studied during development (ICH Q14), which is exactly the pH calculation above.

### Safety reasoning in the real lab

Acetonitrile is flammable and toxic by inhalation and skin contact; prepare mobile phases in a fume hood and cap reservoirs. HPLC pumps run at 100–400 bar: tighten fittings with the pump stopped, and never look into a leaking fitting under pressure. Phosphate buffer left in the system crystallises when acetonitrile is added; flush with water before switching to high organic.

## Worked example

### 1. From scouting runs to a prediction

With $t_0$ = 1.00 min, aspirin elutes at 13.62 min in 20 % acetonitrile ($k$ = 12.6) and 2.26 min in 40 % ($k$ = 1.26):

$$S = \frac{\log 12.6 - \log 1.26}{0.40 - 0.20} = \frac{1.100 - 0.100}{0.20} = 5.0, \qquad \log k_w = 1.100 + 5.0 \times 0.20 = 2.10$$

At 25 %: $\log k = 2.10 - 1.25 = 0.85$, $k$ = 7.1, $t_R = 1.00 \times (1 + 7.1) = 8.1$ min. The six system-suitability injections at 25 % give 8.08 min.

### 2. What happens at pH 3.5?

At pH 2.5 aspirin is $1/(1 + 10^{-1.0})$ = 91 % neutral and salicylic acid $1/(1 + 10^{-0.47})$ = 75 %. At pH 3.5 they are 50 % and 23 %. If only the neutral form is retained, at 25 % acetonitrile aspirin's $k$ drops from 7.1 to $7.1 \times 0.50/0.91$ = 3.9 and salicylic acid's from 10.0 to $10.0 \times 0.23/0.75$ = 3.1. The two peaks swap order and move closer, and at pH 3.5 aspirin's $k$ changes by about 11 % per 0.1 pH unit. At pH 2.5 the same pH error moves it by about 2 %. The lower pH costs nothing and buys robustness.

## Hands-on

What you need: the [Module 25 lab folder](../../labs/module-25/) with Python set up, a calculator, and the [lab report template](../../templates/lab-report.md). Time: about 80 minutes. There is no home version of HPLC; the simulations and the calculation train the method decisions, not the hands-on care of pumps and columns.

### Part A — simulation: build the method (25 min)

[Simulation: Chromatography — HPLC method building](../../simulations/chromatography/index.html?preset=hplc)

1. Inject the four-compound standard on a C18 column, pH 2.5, at 20 % and at 40 % acetonitrile. Record the four retention times and $t_0$.
2. Change the pH to 3.5, then 4.5, at 25 % acetonitrile. Watch aspirin and salicylic acid.
3. Replace acetonitrile with methanol at a composition that gives similar retention. Which pair changes its spacing most?
4. Run a 5–60 % gradient in 10 min and compare its run time and peak widths with your best isocratic run.

How you know it worked: at pH 4.5 the two acids elute near the void and almost together; methanol changes the spacing of paracetamol and caffeine; the gradient is faster but its baseline drifts.

### Part B — simulation: the critical pair (15 min)

[Simulation: Chromatography — overlapping peaks and the three levers](../../simulations/chromatography/index.html?preset=overlap)

Take the paracetamol/caffeine pair at 33 % acetonitrile ($R_s$ about 1). Improve it three ways: double the column length (more $N$), lower the acetonitrile by 5 % (more $k$), and switch to methanol (different $\alpha$). Note the gain in $R_s$ and the cost in time for each.

How you know it worked: doubling the length gains about 40 % in $R_s$ for twice the time; changing $k$ or $\alpha$ gains more for less.

### Part C — Python: resolution map and system suitability (40 min)

Open `lesson05_hplc_method.py`. Complete `lss_from_two_runs()` (TODO 1) and `resolution()` (TODO 2). Run:

```bash
py lesson05_hplc_method.py
```

How you know it worked: $S$ = 3.26, 4.30, 5.01 and 5.20 and $\log k_w$ = 0.91, 1.30, 2.10 and 2.30; the worst pair is paracetamol/caffeine from 20 % up, with $R_s$ 3.9 at 25 % and 0.45 at 35 %, where the two swap order (near 38 %); best isocratic choice within 15 min: 23 % acetonitrile, $R_s$ 4.8, 13.7 min. The new column passes the SST (critical-pair $R_s$ 4.2, all tailing ≤ 1.3, area RSD ≤ 0.6 %); after 400 injections the salicylic acid tailing is 2.36 and the SST fails.

<details><summary>What to do about the failed SST</summary>

Do not adjust integration settings to hide the tailing. Check first what changed: tailing of an acid on an aged silica column usually means exposed silanol groups or a blocked inlet frit. Flush or reverse-flush per the column instructions, check the buffer pH, and if the tailing stays above 2.0 replace the column (or its guard column) and repeat the SST. Record the failure; results of the sequence would not be valid.

</details>

## Common mistakes

- **Choosing the pH by habit.** Compute the neutral fraction of every acid and base at the pH you plan; stay 1.5–2 units from each pKa.
- **Identifying peaks by elution order.** Orders swap with pH and solvent; identify by retention time of standards run the same day, or by spectrum (diode-array or MS).
- **Fixing every overlap with a longer column.** $R_s$ grows only with $\sqrt{N}$; changing $\alpha$ (solvent, pH, temperature) or $k$ is cheaper.
- **Treating SST as paperwork.** It is the evidence that the day's results are valid; a failed SST invalidates the sequence.
- **Putting phosphate into an LC-MS method.** It is not volatile and fouls the source; use formic acid or ammonium formate.

## Key takeaways

- Start from pKa, log P and UV: they decide mode, pH, solvent and detector before any injection.
- For acids and bases, retention follows the neutral fraction; work 1.5–2 pH units away from every pKa for a robust method.
- Two scouting runs give the linear-solvent-strength model, which predicts retention, elution-order crossings and the resolution map.
- System suitability proves the system works today; validation proves the method is fit for purpose once.

## Sources

- [Harvey, Analytical Chemistry 2.1, 12.5](https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_(Harvey)/12%3A_Chromatographic_and_Electrophoretic_Methods/12.05%3A_High-Performance_Liquid_Chromatography) — reversed phase, mobile-phase strength, pH and method development.
- PubChem: [aspirin](https://pubchem.ncbi.nlm.nih.gov/compound/2244) (pKa 3.5, log P 1.19), [salicylic acid](https://pubchem.ncbi.nlm.nih.gov/compound/338) (pKa 2.97, log P 2.26), [acetaminophen](https://pubchem.ncbi.nlm.nih.gov/compound/1983) (pKa 9.38, log P 0.46), [caffeine](https://pubchem.ncbi.nlm.nih.gov/compound/2519) (cation pKa 0.7, log P −0.07).
- [EMA, ICH Q2(R2)](https://www.ema.europa.eu/en/ich-q2r2-validation-analytical-procedures-scientific-guideline) — validation characteristics; effective 14 June 2024.
- [Phenomenex, What is USP Chapter 621?](https://www.phenomenex.com/resources/blog/what-is-usp-chapter-621) — system suitability and allowed adjustments (summary; the binding text is the USP–NF).
