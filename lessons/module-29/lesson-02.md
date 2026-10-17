---
id: "29.2"
module: 29
minutes: 22
practice_minutes: 75
prerequisites: ["22.5", "22.3", "05.3", "29.1"]
objectives:
  - State the conditions under which the Michaelis–Menten equation holds and recognise data that break them.
  - Use kcat, Km and kcat/Km to compare enzymes and to predict which of two competing substrates is turned over faster.
  - Fit Km and Vmax by nonlinear least squares and by three linear plots, and show with a Monte Carlo test why the Lineweaver–Burk values are least precise.
  - Choose substrate concentrations for an assay that determine Km well, and use the integrated rate law to predict a time course.
volatility: concept
sources:
  - title: "Johnson and Goody (2011), The original Michaelis constant: translation of the 1913 Michaelis–Menten paper, Biochemistry 50, 8264"
    url: https://pmc.ncbi.nlm.nih.gov/articles/PMC3381512/
  - title: "Bar-Even et al. (2011), The moderately efficient enzyme, Biochemistry 50, 4402"
    url: https://pubmed.ncbi.nlm.nih.gov/21506553/
  - title: "Lineweaver and Burk (1934), The determination of enzyme dissociation constants, J. Am. Chem. Soc. 56, 658"
    url: https://pubs.acs.org/doi/10.1021/ja01318a036
  - title: "LibreTexts Physical Chemistry, 29.9 The Michaelis-Menten Mechanism for Enzyme Catalysis"
    url: https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Physical_Chemistry_(LibreTexts)/29%3A_Chemical_Kinetics_II-_Reaction_Mechanisms/29.09%3A_The_Michaelis-Menten_Mechanism_for_Enzyme_Catalysis
  - title: "MIT OpenCourseWare 5.07SC Biological Chemistry I (Fall 2013)"
    url: https://ocw.mit.edu/courses/5-07sc-biological-chemistry-i-fall-2013/
last_verified: "2026-10-17"
---

# 29.2 · Enzyme kinetics: Michaelis-Menten in depth

Lesson [22.5](../module-22/lesson-05.md) derived the Michaelis–Menten equation from the steady-state approximation and fitted the 1913 invertase data. This lesson is about using it well. You will see exactly when the equation holds, what its three parameters tell you about an enzyme, why the straight-line plots in older textbooks give poor numbers, how to design an assay, and how to predict a whole time course instead of just the first minute.

## Why it matters

A lab screens a library of enzyme variants for one that degrades a plastic additive. Each variant gets one plate of assays: eight substrate concentrations, one reading per well. Pick the concentrations badly and every $K_m$ comes out with an uncertainty of ±50 %, and the best variant cannot be told from the tenth best. Fit the data with a Lineweaver–Burk line and the ranking can change again. The same choices decide whether a clinical lab's enzyme test for liver damage reads true, and whether a published $k_\text{cat}/K_m$ can be compared with anyone else's. Enzyme kinetics is an exercise in getting two numbers right, and most of the errors are in the design and the fit, not in the biology.

## Core ideas

> [!NOTE]
> The kinetics is stable. Typical values of $k_\text{cat}$ and $K_m$ are from the 2011 survey of several thousand enzymes by Bar-Even et al.; the 1913 data are from the Johnson and Goody translation. The labs use NumPy 2.5 and SciPy 1.18 (`curve_fit`), pinned in `labs/common/requirements.txt`, checked 2026-10-17.

### The equation and what it assumes

$$v_0 = \frac{V_\text{max}[\mathrm{S}]}{K_m + [\mathrm{S}]}, \qquad V_\text{max} = k_\text{cat}[\mathrm{E}]_0$$

The derivation in 22.5 needs four conditions. Each one is something you check in the lab, not something you assume:

1. **Initial rate.** $v_0$ is measured before more than about 10 % of the substrate is used, so [S] is still the concentration you added and no product has built up. Products often inhibit (invertase is slowed by fructose and glucose).
2. **Enzyme much scarcer than substrate.** The steady state for ES (lesson [22.3](../module-22/lesson-03.md)) and the use of added [S] as free [S] both need $[\mathrm{E}]_0 \ll K_m + [\mathrm{S}]$. When an inhibitor or substrate binds so tightly that this fails, use the full quadratic binding equation instead.
3. **One substrate, or the others held constant.** For a two-substrate enzyme, the $K_m$ you measure for one substrate depends on the concentration of the other.
4. **A stable enzyme at fixed pH and temperature.** If activity drops during the assay, the "initial rate" falls with time for a reason that has nothing to do with substrate.

### What the parameters tell you

- $k_\text{cat}$, the **turnover number**, is the number of substrate molecules one active site converts per second when saturated. It is a first-order rate constant (s⁻¹) for the slowest step after binding.
- $K_m$ is the substrate concentration that gives half the maximal rate. It sets the working range: below $K_m$ the rate is almost proportional to [S], above $10K_m$ it hardly changes.
- $k_\text{cat}/K_m$, the **specificity constant**, is the second-order rate constant of free enzyme with substrate at low [S]. It cannot exceed the diffusion limit, about $10^8$–$10^9$ M⁻¹ s⁻¹.

Bar-Even and colleagues collected these numbers for several thousand enzymes. The median enzyme has $k_\text{cat}$ near 10 s⁻¹, $K_m$ near 100 µM and $k_\text{cat}/K_m$ near $10^5$ M⁻¹ s⁻¹, a thousand times below the diffusion limit. Enzymes of central metabolism are on average faster than those of secondary metabolism. Textbook "perfect" enzymes are the exception.

When two substrates A and B compete for the same enzyme, the ratio of their rates is

$$\frac{v_A}{v_B} = \frac{(k_\text{cat}/K_m)_A[\mathrm{A}]}{(k_\text{cat}/K_m)_B[\mathrm{B}]}$$

whatever the total concentration. This is why the specificity constant, not $k_\text{cat}$ alone, says which substrate an enzyme prefers.

### Four ways to get Km and Vmax

Before computers, people rearranged the equation into straight lines:

| Plot | y | x | slope | intercept |
|---|---|---|---|---|
| Lineweaver–Burk (1934) | $1/v$ | $1/[\mathrm{S}]$ | $K_m/V_\text{max}$ | $1/V_\text{max}$ |
| Hanes–Woolf | $[\mathrm{S}]/v$ | $[\mathrm{S}]$ | $1/V_\text{max}$ | $K_m/V_\text{max}$ |
| Eadie–Hofstee | $v$ | $v/[\mathrm{S}]$ | $-K_m$ | $V_\text{max}$ |

All three are exact for perfect data. With real data they distort the errors. Suppose every rate has the same absolute error $\sigma$. Then $1/v$ has error $\sigma/v^2$: at the lowest [S], where $v$ is perhaps a fifth of $V_\text{max}$, the error in $1/v$ is 25 times larger than at the top, yet ordinary linear regression weights every point equally. The slowest, least certain rates control the Lineweaver–Burk line. Hanes–Woolf is the least distorting of the three; Eadie–Hofstee puts $v$ on both axes, so its errors are correlated.

Today the answer is simple: fit the hyperbola directly by **nonlinear least squares** (lesson [05.3](../module-05/lesson-03.md)), with weights if you know how the error depends on $v$, and report the standard errors. Use linear plots only to look at the data, for instance to recognise inhibition patterns in lesson [29.3](lesson-03.md).

### Designing the assay

$K_m$ is defined by the bend of the curve, so the data must show the bend. A good design spreads [S] from about $0.2K_m$ to $5K_m$ or more, spaced geometrically (each step a factor of two). If every [S] is well above $K_m$, all rates are near $V_\text{max}$ and the data carry little information about $K_m$; if every [S] is well below $K_m$, you get only the ratio $V_\text{max}/K_m$. A first range-finding experiment with widely spaced concentrations tells you where $K_m$ is, so the second experiment can be designed around it.

Explore the saturation curve, and where data points carry information about $K_m$:

[Simulation: Kinetics — enzyme saturation (Michaelis–Menten)](../../simulations/kinetics/index.html?preset=enzyme)

### The whole time course: integrated Michaelis–Menten

If there is no product inhibition, $-d[\mathrm{S}]/dt = V_\text{max}[\mathrm{S}]/(K_m + [\mathrm{S}])$ can be separated and integrated:

$$V_\text{max}\,t = ([\mathrm{S}]_0 - [\mathrm{S}]) + K_m\ln\frac{[\mathrm{S}]_0}{[\mathrm{S}]}$$

The first term is the zero-order part, which dominates while [S] ≫ $K_m$; the second is the first-order part (lesson [22.1](../module-22/lesson-01.md)). One progress curve contains information about both parameters. The equation can be solved for [S] with the Lambert W function (`scipy.special.lambertw`), or you can integrate the rate law numerically as in 22.5. Use it only after checking for product inhibition: in 1913 invertase it was not negligible.

## Worked example

### 1. Which substrate wins?

An esterase hydrolyses two esters. Substrate A: $k_\text{cat}$ = 100 s⁻¹, $K_m$ = 1.0 mM. Substrate B: $k_\text{cat}$ = 10 s⁻¹, $K_m$ = 0.010 mM. Both are present at 0.10 mM.

1. Specificity constants: A, $100/(1.0 \times 10^{-3}\ \mathrm{M}) = 1.0 \times 10^5$ M⁻¹ s⁻¹; B, $10/(1.0 \times 10^{-5}\ \mathrm{M}) = 1.0 \times 10^6$ M⁻¹ s⁻¹.
2. At equal concentrations, $v_B/v_A = 10^6/10^5 = 10$.

B is hydrolysed ten times faster, although A has the larger turnover number. B binds so well that it occupies most of the active sites, and A has to compete for the rest. Judging by $k_\text{cat}$ alone gives the wrong answer.

### 2. How long does an assay take?

An enzyme with $K_m$ = 0.50 mM and $V_\text{max}$ = 0.10 mM/min is mixed with [S]₀ = 0.50 mM. How long until 90 % is converted, and is the first minute a true initial rate?

1. At 90 % conversion [S] = 0.050 mM. Integrated rate law: $V_\text{max}t = (0.50 - 0.05) + 0.50\ln(0.50/0.05) = 0.45 + 1.15 = 1.60$ mM.
2. $t = 1.60/0.10 = 16$ min.
3. In the first minute the rate is at most $v_0 = 0.10 \times 0.50/1.00 = 0.050$ mM/min, so at most 0.05 mM, 10 % of the substrate, is used. One minute is just within the initial-rate rule; two minutes would not be.

### 3. The 1913 data four ways

The lab fits the seven invertase rates of lesson 22.5 with all four methods. Nonlinear least squares gives $V_\text{max}$ = 3.91 ± 0.06 (arbitrary units) and $K_m$ = 17.9 ± 1.0 mM. Lineweaver–Burk gives 3.95 and 18.4 mM, Hanes–Woolf 3.85 and 16.6 mM, Eadie–Hofstee 3.91 and 17.9 mM. All agree with the 16.7 mM of Michaelis and Menten within about 2 mM, because the 1913 rates are unusually precise and well spread around $K_m$. With noisier data the methods drift apart, which the Monte Carlo test in the lab shows.

## Hands-on

What you need: Python with the course packages and the [Module 29 lab folder](../../labs/module-29/), a browser for the simulation, paper and a calculator. Write up Part A with the [error-analysis template](../../templates/error-analysis.md). Time: about 75 min.

### Part A — Python: four fits and a Monte Carlo test (45 min)

1. Open `lesson02_mm.py`. It reads `invertase_initial_rates.csv` (the seven 1913 rates) and already contains the nonlinear fit.
2. Complete `lineweaver_burk()`, `hanes_woolf()` and `eadie_hofstee()` from the table above. Each is one `np.polyfit` on transformed data, then $V_\text{max}$ and $K_m$ from the slope and intercept.
3. Run it (about 10 s) and open `runs/lesson02_mm.png`:

```bash
py lesson02_mm.py
```

The script then makes 2000 copies of an exact data set ($K_m$ = 1, $V_\text{max}$ = 1, six [S] from 0.2 to 6.4 $K_m$), adds random noise of 3 % of $V_\text{max}$ to each rate, fits every copy with all four methods, and reports the median bias and the spread of $K_m$. Part 3 repeats this for a poor design with all [S] between 2 and 10 $K_m$.

4. Answer: (a) Which method gives the most precise $K_m$, and how many times wider is the Lineweaver–Burk spread? (b) Is the Lineweaver–Burk problem mainly bias or scatter? (c) What happens to the nonlinear fit with the poor design, and why?

How you know it worked: 1913 data as in worked example 3. Good design, spread of $K_m$ (16–84 % range): nonlinear ±12 %, Hanes–Woolf ±14 %, Eadie–Hofstee ±17 % (median bias −4 %), Lineweaver–Burk ±43 %. Poor design: nonlinear ±20 %, and all four methods are about equally poor.

<details><summary>Reference solution and model answers</summary>

```python
def lineweaver_burk(S, v):
    slope, intercept = np.polyfit(1 / S, 1 / v, 1)
    return 1 / intercept, slope / intercept

def hanes_woolf(S, v):
    slope, intercept = np.polyfit(S, S / v, 1)
    return 1 / slope, intercept / slope

def eadie_hofstee(S, v):
    slope, intercept = np.polyfit(v / S, v, 1)
    return intercept, -slope
```

Full code: `lesson02_mm_solution.py`.

(a) Nonlinear least squares; Lineweaver–Burk is about 3.5 times wider (±43 % against ±12 %). (b) Mostly scatter: its median is nearly right, but single experiments land far off, sometimes with negative or huge $K_m$, because the noisy low-[S] points dominate the line. (c) Its spread grows from ±12 % to ±20 %: with no points below $K_m$ the curve's bend is barely sampled, so even the best fitting method has little information. Good design matters more than the choice between good methods.

</details>

### Part B — simulation: read the curve (10 min)

Open the enzyme preset:

[Simulation: Kinetics — enzyme saturation (Michaelis–Menten)](../../simulations/kinetics/index.html?preset=enzyme)

Set any $K_m$ and $V_\text{max}$. Find the [S] that gives $v = 0.5V_\text{max}$, $0.8V_\text{max}$ and $0.9V_\text{max}$, and write each as a multiple of $K_m$. Target: $1K_m$, $4K_m$ and $9K_m$, from $[\mathrm{S}]/(K_m + [\mathrm{S}]) = f$, so $[\mathrm{S}] = K_m f/(1 - f)$. Getting from 90 % to 99 % of $V_\text{max}$ needs $99K_m$: "saturating" substrate is rarely truly saturating.

### Part C — pencil: design an assay (20 min)

A range-finding experiment suggests $K_m \approx 40$ µM. The substrate dissolves only up to 300 µM, and you have eight wells.

1. Choose eight concentrations.
2. Your detector's noise is about 0.02 absorbance units, and the fastest rate gives 0.5 absorbance units per minute. Over how many minutes must you read each well so that the slowest rate is still measured to about 10 %? (Assume the slowest well runs at $v_0 = 0.2V_\text{max}$.)

<details><summary>Model answer</summary>

1. For example 8, 12, 20, 30, 50, 80, 150 and 300 µM: from $0.2K_m$ to $7.5K_m$, roughly geometric, with more points near $K_m$, where the curve bends. Going higher is impossible and would add little.
2. The slowest well changes by $0.2 \times 0.5 = 0.1$ absorbance units per minute. To measure that change to 10 %, the total change must be about ten times the noise, 0.2 units, so read for about 2 minutes. Check that this stays under 10 % conversion of the lowest [S]; if not, use less enzyme for every well and read longer.

</details>

## Common mistakes

- Measuring "initial" rates after a large fraction of substrate has reacted, or after a lag while the instrument settles. Plot product against time for every well and use only the straight early part.
- Quoting $K_m$ and $V_\text{max}$ from a Lineweaver–Burk line. Use it to look; fit the hyperbola for the numbers.
- Reporting $V_\text{max}$ as a property of the enzyme. It depends on how much enzyme was added; report $k_\text{cat} = V_\text{max}/[\mathrm{E}]_0$ with the active-site concentration.
- Choosing [S] all above $K_m$ "to be safe". The data then hardly constrain $K_m$.
- Comparing enzymes or substrates by $k_\text{cat}$ alone. For competing substrates and low [S], $k_\text{cat}/K_m$ decides.
- Using the integrated equation when products inhibit. Test it first, as in 22.5.

## Key takeaways

- Michaelis–Menten holds for initial rates, enzyme far below $K_m + [\mathrm{S}]$, one varied substrate and a stable enzyme; check each condition.
- $k_\text{cat}$ is turnover at saturation, $K_m$ is the half-saturating concentration, $k_\text{cat}/K_m$ is the second-order constant that decides between competing substrates; the median enzyme has about 10 s⁻¹, 100 µM and $10^5$ M⁻¹ s⁻¹.
- Linear plots distort errors; Lineweaver–Burk scatters about 3.5 times more than a nonlinear fit in a typical design.
- Spread [S] geometrically from about $0.2K_m$ to $5K_m$; design matters as much as the fitting method.
- The integrated rate law, $V_\text{max}t = ([\mathrm{S}]_0 - [\mathrm{S}]) + K_m\ln([\mathrm{S}]_0/[\mathrm{S}])$, predicts whole time courses when there is no product inhibition.

## Sources

- [Johnson and Goody (2011), Biochemistry 50, 8264](https://pmc.ncbi.nlm.nih.gov/articles/PMC3381512/) — translation of Michaelis and Menten (1913); Table I initial rates, $K_m$ = 16.7 mM; the original paper already fitted whole time courses.
- [Bar-Even et al. (2011), Biochemistry 50, 4402](https://pubmed.ncbi.nlm.nih.gov/21506553/) — survey of several thousand enzymes: median $k_\text{cat}$ about 10 s⁻¹, $k_\text{cat}/K_m$ about $10^5$ M⁻¹ s⁻¹; central metabolism about 30 times faster than secondary.
- [Lineweaver and Burk (1934), J. Am. Chem. Soc. 56, 658](https://pubs.acs.org/doi/10.1021/ja01318a036) — the double-reciprocal plot.
- [LibreTexts Physical Chemistry, 29.9 The Michaelis-Menten Mechanism](https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Physical_Chemistry_(LibreTexts)/29%3A_Chemical_Kinetics_II-_Reaction_Mechanisms/29.09%3A_The_Michaelis-Menten_Mechanism_for_Enzyme_Catalysis) — derivation, $k_\text{cat}$ and $K_m$, the double-reciprocal plot.
- [MIT OCW 5.07SC Biological Chemistry I](https://ocw.mit.edu/courses/5-07sc-biological-chemistry-i-fall-2013/) — Module I, enzyme kinetics and catalysis.
