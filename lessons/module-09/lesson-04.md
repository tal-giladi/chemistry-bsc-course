---
id: "09.4"
module: 9
minutes: 25
practice_minutes: 60
prerequisites: ["09.3", "05.3"]
objectives:
  - Design an external-standard calibration, fit it, and judge its linear range from the residuals.
  - Calculate the limit of detection and limit of quantification from blank replicates and from the regression, and report a low result correctly.
  - Recognise a matrix effect and correct for it with the method of standard additions.
volatility: concept
sources:
  - title: "LibreTexts — Harvey, Analytical Chemistry 2.1, 5.3 Determining the Sensitivity"
    url: https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/05%3A_Standardizing_Analytical_Methods/5.03%3A_Determining_the_Sensitivity
  - title: "LibreTexts — Harvey, Analytical Chemistry 2.1, 5.4 Linear Regression and Calibration Curves"
    url: https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/05%3A_Standardizing_Analytical_Methods/5.04%3A_Linear_Regression_and_Calibration_Curves
  - title: "LibreTexts — Harvey, Analytical Chemistry 2.1, 4.7 Detection Limits"
    url: https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/04%3A_Evaluating_Analytical_Data/4.07%3A_Detection_Limits
  - title: "IUPAC Gold Book — limit of detection"
    url: https://goldbook.iupac.org/terms/view/L03540
  - title: "ICH Q2(R2) Validation of analytical procedures — scientific guideline (EMA)"
    url: https://www.ema.europa.eu/en/ich-q2r2-validation-analytical-procedures-scientific-guideline
  - title: "Eurachem — The Fitness for Purpose of Analytical Methods (3rd edition, 2025)"
    url: https://eurachem.org/index.php/publications/guides/mv
last_verified: "2026-10-17"
---

# 09.4 · Calibration, linear regression and detection limits

Most instruments do not measure concentration; they measure a signal, such as an absorbance, a current or a peak area. A calibration turns the signal into a concentration, and its quality limits every result you report. In [Lesson 05.3](../module-05/lesson-03.md) you fitted a calibration line and found an unknown with its uncertainty. This lesson adds what an analyst needs on top: how to design the standards, how low you can go before "zero" and "a little" become indistinguishable, and what to do when the sample itself changes the signal.

## Why it matters

A well-water customer asks whether her water contains nitrite. The lab's colorimetric test gives a signal a hair above the blank. Is the answer "0.003 mg/L", "not detected", or "present, but too low to measure"? Each answer means something different to the customer, and to a regulator. A second sample, from a farm, reads 0.035 mg/L on the calibration line; but its brownish colour and salts suppress the colour reaction, and the true value is 0.040 mg/L. A calibration made in clean water silently underreports by 12 %. Both decisions come down to the ideas in this lesson.

## Core ideas

> [!NOTE]
> Calibration by least squares, blank-based detection limits and standard additions are stable methods (Harvey, chapters 4 and 5). Definitions of the detection limit differ slightly between bodies: the IUPAC Gold Book, ICH Q2(R2) (in force in the EU since June 2024) and the Eurachem *Fitness for Purpose* guide (3rd edition, 2025). Checked on 2026-10-17. For regulated work, use the definition your method or regulator names.

### Signal, sensitivity and the calibration function

The **calibration function** links the signal $S$ to the concentration $c$. For many methods it is a straight line:

$$S = m\,c + S_\text{blank}$$

The slope $m$ is the **sensitivity**: how much the signal changes per unit of concentration. $S_\text{blank}$ is the signal with no analyte, from the reagents, the cell or the instrument. A **single-point** calibration uses one standard and assumes the line passes through the blank; a **multi-point** calibration fits several standards and tests that assumption. Prefer multi-point.

### Designing external standards

With **external standards**, you prepare a series of standards in clean solvent and measure them separately from the samples. Good practice:

- at least five or six concentration levels, spread evenly over the range, plus a blank;
- the unknowns inside the range, ideally near the middle, never extrapolated above the top standard;
- standards made independently or by serial dilution with a known uncertainty ([Lesson 07.7](../module-07/lesson-07.md));
- residuals checked by eye. A random scatter around zero means the straight line is right; a curve or a funnel means it is not ([Lesson 05.3](../module-05/lesson-03.md)).

Ordinary least squares assumes that the concentrations are exact, that the noise is in the signal only, and that the noise is the same size everywhere. If the noise grows with the signal (a funnel in the residuals), use a **weighted** fit.

### The uncertainty of an unknown

The standard deviation of a concentration read from the line (Harvey eq. 5.12, used in Lesson 05.3) is

$$s_c = \frac{s_r}{m}\sqrt{\frac{1}{k} + \frac{1}{n} + \frac{(\bar{S}_\text{unk} - \bar{S}_\text{std})^2}{m^2 \sum (c_i - \bar{c})^2}}$$

where $s_r$ is the residual standard deviation, $k$ the number of readings of the unknown and $n$ the number of standards. It is smallest near the centre of the standards ($\bar{S}_\text{std}$) and grows towards the ends.

### Detection and quantification limits

At low concentration the question changes from "how much?" to "is it there at all?". Measure a **blank** many times (7 to 10 is usual). Its mean is $\bar{S}_\text{bl}$ and its standard deviation $s_\text{bl}$.

- The **limit of detection (LOD)** is the smallest concentration whose signal can be told apart from the blank: a signal of $\bar{S}_\text{bl} + 3s_\text{bl}$, which in concentration is
$$\text{LOD} = \frac{3\,s_\text{bl}}{m}$$
- The **limit of quantification (LOQ)** is the smallest concentration that can be measured with acceptable precision:
$$\text{LOQ} = \frac{10\,s_\text{bl}}{m}$$

The factor 3 keeps false positives (a type I error, [Lesson 09.2](lesson-02.md)) rare: if the blank noise is normal, a blank exceeds $3s$ only about 0.1 % of the time. But a sample whose true concentration sits exactly at the LOD will read below it half the time. So the LOD is a fuzzy boundary, not a sharp line.

ICH Q2(R2), used for pharmaceuticals, gives a related **regression-based** form: $\text{DL} = 3.3\,\sigma/S$ and $\text{QL} = 10\,\sigma/S$, where $\sigma$ can be the blank standard deviation or the residual standard deviation $s_r$ of the line, and $S$ is the slope.

Report a result in three tiers:

| Result | What to write |
|---|---|
| below the LOD | "not detected (< LOD)", and give the LOD |
| between LOD and LOQ | "detected, below the LOQ" |
| above the LOQ | the value with its uncertainty |

### The linear range

The **linear range** runs from the LOQ to the concentration where the response stops being straight, often because the detector saturates or stray light flattens the top (you will see this in the module practical, Lesson 09.6). The **working range** is the part of it you have validated with standards.

### Matrix effects and standard additions

The **matrix** is everything in the sample except the analyte: salts, colour, other compounds. If it changes the sensitivity, the external line gives the wrong answer, and no amount of care with the standards will show it. A **spike recovery** reveals it: add a known amount to the sample and see whether you get it back ([Lesson 09.1](lesson-01.md)).

The cure is the **method of standard additions**: add increasing known amounts of analyte to equal portions of the sample itself, and measure each. All portions share the same matrix, so they share the same (changed) slope. Fit the signal against the concentration added; the line crosses zero signal at $-c_\text{sample}$:

$$c_\text{sample} = \frac{b}{m_\text{SA}}$$

with $b$ the intercept and $m_\text{SA}$ the slope of the standard-additions line. Its standard deviation is

$$s_{c} = \frac{s_r}{m_\text{SA}}\sqrt{\frac{1}{n} + \frac{\bar{S}^2}{m_\text{SA}^2 \sum (c_{\text{add},i} - \bar{c}_\text{add})^2}}$$

The price is extra work per sample and an extrapolation, which makes the result less precise than one from an external line. An **internal standard**, a different compound added in equal amount to every standard and sample, corrects for losses and instrument drift instead; you will meet it in chromatography (Module 19).

## Worked example

### Nitrite in two well waters

The data are in `nitrite_calibration.csv` (simulated, modelled on a Griess-type colour test read at 540 nm in a 1 cm cell).

**1. The line.** Seven standards from 0 to 0.25 mg/L (as N) give $A = 0.0032 + 2.905\,c$ with $s_r = 0.0030$. The residuals scatter between −0.004 and +0.005 with no pattern, so the straight line holds over the whole range.

**2. The limits.** Ten blanks have a mean of 0.0039 and $s_\text{bl} = 0.0023$.

$$\text{LOD} = \frac{3 \times 0.0023}{2.905} = 0.0024\ \text{mg/L} \qquad \text{LOQ} = \frac{10 \times 0.0023}{2.905} = 0.0080\ \text{mg/L}$$

The regression-based ICH values are $3.3 \times 0.0030/2.905 = 0.0034$ and $10 \times 0.0030/2.905 = 0.0104$ mg/L, a little higher because $s_r$ also contains the scatter of the standards. Whichever you use, say which.

**3. The first well.** Three readings average 0.1816:

$$c = \frac{0.1816 - 0.0032}{2.905} = 0.0614\ \text{mg/L}, \qquad s_c = \frac{0.0030}{2.905}\sqrt{\frac{1}{3} + \frac{1}{7} + \frac{(0.1816 - 0.3228)^2}{2.905^2 \times 0.0532}} = 0.0008\ \text{mg/L}$$

It is well above the LOQ, so report $0.0614 \pm 0.0008$ mg/L.

**4. The farm well.** Read on the external line, it gives 0.0348 mg/L. A spike recovery is low, so the analyst runs standard additions: four portions spiked with 0, 0.05, 0.10 and 0.15 mg/L. The line is $A = 0.1060 + 2.543\,c_\text{add}$. Its slope is only 0.88 of the external slope: the matrix suppresses the colour by 12 %. The sample concentration is

$$c_\text{sample} = \frac{0.1060}{2.543} = 0.0417 \pm 0.0010\ \text{mg/L}$$

The external value of 0.0348 mg/L was far too low. (The simulation's true value is 0.0400 mg/L, within two standard deviations.)

## Hands-on

**What you need:** a computer with the [Module 9 lab folder](../../labs/module-09/); pencil and paper. **Time:** about 60 minutes. You will build a full calibration with your own measurements in the module practical, Lesson 09.6.

### Part A — the calibration in Python (35 min)

1. Open `lesson04_calibration.py`. Complete TODO 1 (LOD and LOQ from the blanks) and TODO 2 (the sample concentration from the standard-additions line).
2. Run it:

```bash
py lesson04_calibration.py
```

3. Open `runs/lesson04_calibration.png`. On the left, find where the dashed standard-additions line crosses zero absorbance. On the right, check that the residuals show no pattern.
4. Delete the 0.000 and 0.020 standards from a copy of the data file, run the script on the copy, and note how the intercept, the first well's result and its $s_c$ change.

**How you know it worked:** your numbers match the worked example: slope 2.905, LOD 0.0024 mg/L, LOQ 0.0080 mg/L, first well $0.0614 \pm 0.0008$ mg/L, farm well 0.0417 ± 0.0010 mg/L by standard additions against 0.0348 mg/L on the external line.

<details><summary>Reference solution for the TODOs</summary>

```python
# TODO 1
lod = 3 * s_bl / m
loq = 10 * s_bl / m
# TODO 2
c_sa = ba / ma
```

Without the two lowest standards the intercept is now extrapolated from 0.05 mg/L down to zero and moves from 0.0032 to 0.0063. The first well (0.061 mg/L) sits at the bottom edge of the remaining standards, its result shifts to 0.0607 mg/L, and $s_c$ rises from 0.0008 to 0.0010 mg/L. Low standards and a blank matter most for low samples: standards must bracket the unknowns. The full script is `lesson04_calibration_solution.py`.

</details>

### Part B — pencil: report it right (25 min)

Use the line and limits from the worked example.

1. A sample reads $A = 0.0080$ (mean of three). Compute its concentration and decide how to report it.
2. Another reads $A = 0.0240$. Compute and report it.
3. A colleague proposes a two-point calibration (blank and 0.25 mg/L) to save time. Give two things the seven-point line tells you that the two-point line cannot.
4. A sample reads $A = 0.95$, above the top standard. What should you do instead of extrapolating?

<details><summary>Answers</summary>

1. $c = (0.0080 - 0.0032)/2.905 = 0.0017$ mg/L, below the LOD (0.0024). Report "not detected, < 0.0024 mg/L".
2. $c = 0.0072$ mg/L, between the LOD and the LOQ (0.0080). Report "detected, below the LOQ of 0.008 mg/L".
3. Whether the response is really straight (residuals), and an estimate of the scatter ($s_r$) and so of the uncertainty of every result. A two-point line passes exactly through both points and hides both.
4. Dilute the sample by a known factor into the range, measure again, and multiply back; the dilution's uncertainty enters the budget (Lesson 09.3).

</details>

## Common mistakes

- **Extrapolating above the top standard.** The line is only known where you measured; dilute the sample instead.
- **Taking the LOD from a single blank reading.** One reading has no standard deviation. Measure at least seven blanks, carried through the whole method.
- **Reporting a number below the LOD as a concentration.** "0.0017 mg/L" implies a precision you do not have; report "< LOD" with the LOD.
- **Trusting $R^2$.** $R^2 = 0.999$ can hide a curve. Look at the residuals ([Lesson 05.3](../module-05/lesson-03.md)).
- **Calibrating in clean water for a dirty sample.** If the matrix changes the slope, only a spike recovery or standard additions will show it.

## Key takeaways

- The slope of the calibration line is the sensitivity; standards should bracket the samples, with five or more levels and a blank.
- The uncertainty of an unknown is smallest near the centre of the standards and grows with extrapolation.
- LOD = $3s_\text{bl}/m$, LOQ = $10s_\text{bl}/m$; report "not detected", "detected, below LOQ", or a value with uncertainty.
- A matrix that changes the slope makes external calibration biased; standard additions measure the slope in the sample itself.
- State which definition of the detection limit you used; IUPAC, ICH and Eurachem differ in detail.

## Sources

- [LibreTexts — Harvey, Analytical Chemistry 2.1, 5.3 Determining the Sensitivity](https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/05%3A_Standardizing_Analytical_Methods/5.03%3A_Determining_the_Sensitivity) (external standards, standard additions, internal standards).
- [LibreTexts — Harvey, Analytical Chemistry 2.1, 5.4 Linear Regression and Calibration Curves](https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/05%3A_Standardizing_Analytical_Methods/5.04%3A_Linear_Regression_and_Calibration_Curves) (eq. 5.12; uncertainty of a standard-additions result).
- [LibreTexts — Harvey, Analytical Chemistry 2.1, 4.7 Detection Limits](https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/04%3A_Evaluating_Analytical_Data/4.07%3A_Detection_Limits) (blank + 3σ, LOQ at 10σ, type I and II errors at the LOD).
- [IUPAC Gold Book — limit of detection](https://goldbook.iupac.org/terms/view/L03540) (definition from blank mean and standard deviation).
- [ICH Q2(R2) Validation of analytical procedures (EMA page)](https://www.ema.europa.eu/en/ich-q2r2-validation-analytical-procedures-scientific-guideline) (section 3.2.3.3: DL = 3.3σ/S, QL = 10σ/S; effective in the EU from 14 June 2024).
- [Eurachem — The Fitness for Purpose of Analytical Methods (3rd ed., 2025)](https://eurachem.org/index.php/publications/guides/mv) (section 6.2, LOD and LOQ in method validation).
