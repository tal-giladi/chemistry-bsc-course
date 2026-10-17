---
id: "09.5"
module: 9
minutes: 25
practice_minutes: 70
prerequisites: ["09.3", "08.3", "08.4", "08.7", "02.2"]
objectives:
  - Calculate the pH at the start, in the buffer region, at the equivalence point and past it for a strong-acid and a weak-acid titration with a strong base.
  - Compute a whole titration curve from the charge balance with a root finder.
  - Choose an indicator whose colour change falls on the steep part of the curve and estimate the titration error of a poor choice.
  - Locate the end point in noisy pH-meter data with the first and second derivatives, and estimate the pKa from the half-equivalence point.
volatility: concept
sources:
  - title: "LibreTexts — Harvey, Analytical Chemistry 2.1, 9.1 Overview of Titrimetry"
    url: https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/09%3A_Titrimetric_Methods/9.01%3A_Overview_of_Titrimetry
  - title: "LibreTexts — Harvey, Analytical Chemistry 2.1, 9.2 Acid–Base Titrations"
    url: https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/09%3A_Titrimetric_Methods/9.02%3A_AcidBase_Titrations
  - title: "LibreTexts — Harvey, Analytical Chemistry 2.1, 16.11 Acid Dissociation Constants"
    url: https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/16%3A_Appendix/16.11%3A__Acid_Dissociation_Constants
  - title: "SciPy 1.18 documentation — scipy.optimize.brentq"
    url: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.brentq.html
last_verified: "2026-10-17"
---

# 09.5 · Titration theory and titration curves

A titration curve is the pH of a solution plotted against the volume of titrant added. Its shape tells you where the equivalence point is, which indicator will find it, how big the error of a wrong indicator is, and even the pKa of the acid. In [Lesson 08.7](../module-08/lesson-07.md) you did a first titration with an indicator. This lesson explains the curve behind it, computes it exactly in Python, and finds the end point from pH-meter data the way an automatic titrator does.

## Why it matters

A quality lab titrates the acetic acid in vinegar with NaOH. A new technician runs out of phenolphthalein and uses methyl orange instead, because "it is also an acid–base indicator". It changes colour after barely a tenth of the base has been added, and the vinegar is reported at a tenth of its true strength. A less extreme mistake, bromothymol blue, gives results 0.6 % low: small enough to pass unnoticed, large enough to fail an audit. The titration curve predicts both errors before anyone picks up a burette.

## Core ideas

> [!NOTE]
> Titration theory is stable chemistry. The pKa of acetic acid (4.757 at 25 °C, zero ionic strength) and the indicator ranges are from Harvey's Analytical Chemistry 2.1 tables; $K_w = 1.0 \times 10^{-14}$ at 25 °C. The root finder is SciPy 1.18's `brentq`. Checked on 2026-10-17. Real solutions have ionic strengths above zero, so measured pKa values come out a little lower; activity is treated in Module 13.

### Vocabulary

The **analyte** is the substance you determine; the **titrant** is the solution of known concentration you add from the burette. At the **equivalence point** the amount of titrant added exactly matches the analyte by the reaction's stoichiometry. The **end point** is what you actually observe: an indicator's colour change or a jump in the pH reading. The difference between end point and equivalence point is the **titration error**, a systematic error ([Lesson 09.1](lesson-01.md)).

For an acid HA titrated with NaOH, the equivalence volume is

$$V_\text{eq} = \frac{c_\text{acid}\,V_\text{acid}}{c_\text{NaOH}}$$

### Strong acid with strong base

HCl and NaOH react completely. Before equivalence, the pH comes from the acid left over; after it, from the excess OH⁻. At equivalence only NaCl and water remain, so pH = 7.00 at 25 °C. Near equivalence the pH jumps by several units for a fraction of a millilitre. For 25.00 mL of 0.1000 M HCl with 0.1000 M NaOH, the pH is 3.70 at 24.90 mL and 10.30 at 25.10 mL.

### Weak acid with strong base: four regions

For acetic acid ($K_a = 10^{-4.757} = 1.75 \times 10^{-5}$) the curve has four regions.

1. **Start.** Only the weak acid: $[\text{H}_3\text{O}^+] \approx \sqrt{K_a c}$, the small-x result of [Lesson 08.4](../module-08/lesson-04.md).
2. **Buffer region.** Each OH⁻ turns one HA into A⁻. The mixture is a buffer, and Henderson–Hasselbalch applies:
$$\text{pH} = \text{p}K_a + \log_{10}\frac{n_{\text{A}^-}}{n_\text{HA}}$$
At **half-equivalence** the two amounts are equal, so **pH = pKa**. This is how a titration measures a pKa.
3. **Equivalence.** Only A⁻ remains, a weak base with $K_b = K_w/K_a$. So $[\text{OH}^-] \approx \sqrt{K_b\,c_{\text{A}^-}}$, and the pH is above 7.
4. **After equivalence.** The excess OH⁻ dominates, and the curve joins the strong-acid curve.

The weaker the acid, the higher the start, the higher the equivalence pH, and the smaller the jump. Below about $K_a c = 10^{-8}$ the jump is too small to see with an indicator.

### One equation for every point: the charge balance

The four regions need four formulas, with awkward joins. One equation covers them all. Every solution is electrically neutral, so the positive and negative charges balance:

$$[\text{Na}^+] + [\text{H}_3\text{O}^+] = [\text{OH}^-] + [\text{A}^-]$$

with $[\text{Na}^+] = c_b V_b/(V_a + V_b)$, $[\text{OH}^-] = K_w/[\text{H}_3\text{O}^+]$, and $[\text{A}^-] = C_\text{HA}\,K_a/(K_a + [\text{H}_3\text{O}^+])$, where $C_\text{HA} = c_a V_a/(V_a + V_b)$ is the total acid. Only $[\text{H}_3\text{O}^+]$ is unknown. A root finder solves it at each volume, as you did for equilibria in [Lesson 08.3](../module-08/lesson-03.md). Set $K_a$ very large and the same code gives the strong-acid curve.

### Choosing an indicator

An indicator is itself a weak acid whose two forms have different colours. Its colour changes over roughly its pKa ± 1. Pick one whose range lies on the steep part of the curve:

| Indicator | Colour change (pH) | Good for |
|---|---|---|
| Methyl orange | 3.4–4.4 | strong acids, weak bases |
| Bromothymol blue | 6.0–7.6 | strong acid with strong base |
| Phenolphthalein | 8.3–10.0 | weak acids such as acetic acid |

For a weak acid, the equivalence pH is about 8.7, so phenolphthalein is right. Methyl orange changes in the buffer region, long before equivalence.

### End points from pH data

A pH meter gives the curve itself. The **end point** is where the curve is steepest:

- **First derivative.** Compute $\Delta\text{pH}/\Delta V$ between neighbouring points and assign it to the midpoint volume. The peak marks the end point. Its precision is limited by the step size near the end point.
- **Second derivative.** The derivative of the first derivative crosses zero at the inflection point. Interpolating that zero crossing gives the end point to better than one step.

These are the numerical derivatives of [Lesson 02.2](../module-02/lesson-02.md). Noise is amplified by each derivative, so take small, even steps near the end point and do not over-interpret single points.

## Worked example

### 25.00 mL of 0.1000 M acetic acid with 0.1000 M NaOH

$V_\text{eq} = 0.1000 \times 25.00/0.1000 = 25.00$ mL.

| $V_\text{NaOH}$ | Region | Calculation | pH |
|---|---|---|---|
| 0 mL | start | $\sqrt{1.75 \times 10^{-5} \times 0.1000} = 1.32 \times 10^{-3}$ | 2.88 |
| 10.00 mL | buffer | $4.757 + \log_{10}(1.000/1.500)$ (mmol A⁻/HA) | 4.58 |
| 12.50 mL | half-equivalence | $\text{pH} = \text{p}K_a$ | 4.76 |
| 25.00 mL | equivalence | $c_{\text{A}^-} = 2.500/50.00 = 0.0500$ M; $K_b = 5.71 \times 10^{-10}$; $[\text{OH}^-] = 5.35 \times 10^{-6}$ | 8.73 |
| 26.00 mL | after | excess OH⁻ $= 0.100/51.00 = 1.96 \times 10^{-3}$ M; pOH 2.71 | 11.29 |

The exact charge-balance solution agrees to 0.01 pH unit at every point.

**Indicator error.** Taking each indicator's end point at a typical colour-change pH and reading the volume off the exact curve:

| Indicator (end point taken at) | End-point volume | Titration error |
|---|---|---|
| Methyl orange (pH 3.8) | 2.44 mL | −90 % |
| Bromothymol blue (pH 7.0) | 24.86 mL | −0.57 % |
| Phenolphthalein (pH 9.0) | 25.00 mL | +0.01 % |

Bromothymol blue's error comes from the steep but not vertical curve: at pH 7.0 about 0.14 mL of base is still missing. With phenolphthalein, the colour change sits on the steepest part, and the error is negligible.

## Hands-on

**What you need:** a computer with the [Module 9 lab folder](../../labs/module-09/); pencil and paper. **Time:** about 70 minutes.

### Part A — the titration bench (25 min)

[Simulation: Titration bench — weak acid with indicator choice](../../simulations/titration/index.html?preset=weak-acid)

Task: titrate 25.00 mL of acetic acid with 0.1000 M NaOH three times, once with each of the three indicators, slowing to single drops near the end point. Write down each end-point volume. Then switch on the pH meter and record the full curve. Target: with phenolphthalein your end point lies within 0.05 mL of the equivalence point the simulation reveals, and the pH at half that volume is within 0.05 of 4.76.

### Part B — the curve and the end point in Python (30 min)

1. Open `lesson05_titration.py`. Complete TODO 1 (the charge balance) and TODO 2 (the first-derivative end point).
2. Run it:

```bash
py lesson05_titration.py
```

3. Open `runs/lesson05_titration.png`. Compare the two exact curves, and look at the first-derivative peak.
4. Optional: export your simulation curve as CSV (columns `V_NaOH_mL,pH`) and run `py lesson05_titration.py my_titration.csv`.

**How you know it worked:** the printed key points match the table above. On the example data (`titration_weak_acid.csv`, simulated with a +0.03 pH meter offset), the first derivative gives 25.10 mL, the second derivative 25.00 mL, and the half-equivalence pH 4.79.

<details><summary>Reference solution for the TODOs</summary>

```python
# TODO 1
return na + h - KW / h - c_acid * ka / (ka + h)
# TODO 2
i = int(np.argmax(d1))
v_first = vm[i]
```

The first derivative is assigned to interval midpoints. The largest jump in the data is between 25.00 and 25.20 mL, so it reports 25.10 mL: with 0.2 mL steps it can only be right to about ±0.1 mL. The second-derivative zero crossing interpolates and recovers 25.00 mL. The half-equivalence pH, 4.79, is 0.03 above the true pKa: exactly the meter's calibration offset, a systematic error that no derivative can remove. Calibrate the meter with buffers first. The full script is `lesson05_titration_solution.py`.

</details>

### Part C — pencil (15 min)

1. Find the pH at the start, at half-equivalence and at equivalence for 20.00 mL of 0.0500 M formic acid (p$K_a$ 3.75) titrated with 0.1000 M NaOH.
2. Which of the three indicators in the table would you use, and why?

<details><summary>Answers</summary>

1. $V_\text{eq} = 10.00$ mL. Start: $\sqrt{1.78 \times 10^{-4} \times 0.0500} = 2.98 \times 10^{-3}$, pH 2.53 (the small-x approximation overestimates the hydronium concentration by about 3 % here; the exact value is 2.54). Half-equivalence: pH 3.75. Equivalence: $c = 1.000\ \text{mmol}/30.00\ \text{mL} = 0.0333$ M; $K_b = 5.62 \times 10^{-11}$; $[\text{OH}^-] = 1.37 \times 10^{-6}$; pOH 5.86, pH 8.14.
2. Phenolphthalein (8.3–10.0) is closest; its colour starts just after the equivalence pH of 8.14, on the steep part. Bromothymol blue would end slightly early.

</details>

## Common mistakes

- **Confusing end point and equivalence point.** The equivalence point is set by stoichiometry; the end point is what your indicator or meter shows. Their difference is a systematic error.
- **Assuming the equivalence pH is always 7.** That is only true for a strong acid with a strong base. A weak acid gives a basic solution at equivalence.
- **Choosing an indicator by name, not by range.** Check where its pKa ± 1 sits on the curve you expect.
- **Using large steps near the end point.** A first-derivative end point is only as good as the step size. Use 0.05–0.2 mL steps there.
- **Taking pKa from an uncalibrated meter.** A meter offset shifts every pH, including the half-equivalence pH.

## Key takeaways

- $V_\text{eq} = c_\text{acid}V_\text{acid}/c_\text{base}$; the end point is an experimental estimate of it.
- A weak-acid curve has four regions; at half-equivalence pH = pKa, and at equivalence the pH is above 7.
- The charge balance gives the whole curve in one equation; a root finder solves it at every volume.
- Pick an indicator whose colour range lies on the steep part; a poor choice gives a predictable titration error.
- First-derivative peaks and second-derivative zero crossings locate the end point in pH data.

## Sources

- [LibreTexts — Harvey, Analytical Chemistry 2.1, 9.1 Overview of Titrimetry](https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/09%3A_Titrimetric_Methods/9.01%3A_Overview_of_Titrimetry) (equivalence point, end point, titration error).
- [LibreTexts — Harvey, Analytical Chemistry 2.1, 9.2 Acid–Base Titrations](https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/09%3A_Titrimetric_Methods/9.02%3A_AcidBase_Titrations) (titration curves, indicator table 9.2.3, derivative end points).
- [LibreTexts — Harvey, Analytical Chemistry 2.1, 16.11 Acid Dissociation Constants](https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/16%3A_Appendix/16.11%3A__Acid_Dissociation_Constants) (acetic acid pKa 4.757).
- [SciPy 1.18 documentation — scipy.optimize.brentq](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.brentq.html) (bracketing root finder).
