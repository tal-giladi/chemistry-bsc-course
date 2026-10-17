---
id: "09.3"
module: 9
minutes: 25
practice_minutes: 60
prerequisites: ["09.2", "02.5", "05.3", "07.7"]
objectives:
  - Propagate standard uncertainties through a measurement model with the first-order (partial-derivative) formula and its shortcuts for sums, products, powers and logarithms.
  - Build an uncertainty budget for a titrant standardisation and name the input that dominates it.
  - Run a Monte Carlo propagation in Python, compare it with the first-order result and explain when the first-order formula fails.
volatility: concept
sources:
  - title: "LibreTexts — Harvey, Analytical Chemistry 2.1, 4.3 Propagation of Uncertainty"
    url: https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/04%3A_Evaluating_Analytical_Data/4.03%3A_Propagation_of_Uncertainty
  - title: "JCGM 100:2008 — Guide to the Expression of Uncertainty in Measurement (GUM), BIPM"
    url: https://www.bipm.org/en/doi/10.59161/jcgm100-2008e
  - title: "JCGM 101:2008 — GUM Supplement 1: Propagation of distributions using a Monte Carlo method, BIPM"
    url: https://www.bipm.org/doi/10.59161/JCGM101-2008
  - title: "PubChem — Potassium hydrogen phthalate (CID 23676735)"
    url: https://pubchem.ncbi.nlm.nih.gov/compound/23676735
  - title: "uncertainties 3.2.3 documentation"
    url: https://uncertainties.readthedocs.io/
last_verified: "2026-10-17"
---

# 09.3 · Propagation of uncertainty

A result is almost never measured directly: it is calculated from masses, volumes, purities and readings, each with its own uncertainty. Propagation is the arithmetic that turns those input uncertainties into the uncertainty of the result. You met the idea in [Lesson 02.5](../module-02/lesson-05.md) and built a first budget in [Lesson 07.7](../module-07/lesson-07.md). Here you learn the general rule, the shortcuts, the trap of correlated inputs, and the Monte Carlo method that works when the shortcuts break.

## Why it matters

Every titration result in a lab depends on the titrant concentration, and that comes from a **standardisation**: titrating a weighed amount of a pure primary standard. If the NaOH concentration is known to 0.18 %, no titration done with it can be better than 0.18 %, however careful the analyst. The budget also tells the lab where to spend money. In the worked example below, the burette volume carries 97 % of the variance. A better balance would change nothing; a better end-point detection would. Without propagation you are guessing.

## Core ideas

> [!NOTE]
> The propagation rules and the Monte Carlo method are fixed by the GUM (JCGM 100:2008) and its Supplement 1 (JCGM 101:2008), and are stable. The Python package `uncertainties` is pinned at 3.2.3 in `labs/common/requirements.txt` (its authors have announced a 4.0 that changes some functions). The KHP molar mass is from PubChem. Checked on 2026-10-17.

### The measurement model

Write the result $y$ as a formula of its inputs $x_1, x_2, \dots$: the **measurement model** $y = f(x_1, x_2, \dots)$. For a NaOH standardisation with potassium hydrogen phthalate (KHP, a stable, non-hygroscopic solid acid, $M = 204.22$ g/mol):

$$c_\text{NaOH} = \frac{m_\text{KHP}\,P}{M_\text{KHP}\,V}$$

with $m$ the mass weighed, $P$ the purity and $V$ the titrant volume at the end point. Each input has a **standard uncertainty** $u(x_i)$, from repeats (Type A) or from a certificate, tolerance or resolution (Type B, [Lesson 01.5](../module-01/lesson-05.md)).

### The general first-order rule

If the inputs are independent and their uncertainties are small, each input's effect is its uncertainty times the slope of $f$ in that direction, the partial derivative:

$$u(y)^2 = \sum_i \left(\frac{\partial f}{\partial x_i}\right)^2 u(x_i)^2$$

The terms $(\partial f/\partial x_i)\,u(x_i)$ are the **contributions**. Squared and divided by $u(y)^2$, they give each input's **share of the variance**, the column you look at first in a budget.

### The shortcuts

Working out the partial derivatives for common shapes gives rules you can use without calculus:

| Model | Rule |
|---|---|
| $y = a + b$ or $a - b$ | $u(y)^2 = u(a)^2 + u(b)^2$ (absolute uncertainties) |
| $y = ab$ or $a/b$ | $\left(\frac{u(y)}{y}\right)^2 = \left(\frac{u(a)}{a}\right)^2 + \left(\frac{u(b)}{b}\right)^2$ (relative) |
| $y = a^n$ | $\frac{u(y)}{y} = \lvert n \rvert \frac{u(a)}{a}$ |
| $y = \log_{10} a$ | $u(y) = 0.434\,\frac{u(a)}{a}$ |
| $y = 10^a$ | $\frac{u(y)}{y} = 2.303\,u(a)$ |

The last two matter for pH. A pH meter reading of $4.00 \pm 0.02$ means $[\text{H}_3\text{O}^+] = 1.00 \times 10^{-4}$ mol/L with a relative uncertainty of $2.303 \times 0.02 = 4.6\ \%$. A "small" 0.02 pH unit is a large concentration uncertainty.

### Correlated inputs

The rule above assumes independent inputs. A burette volume is a difference of two readings, $V = R_2 - R_1$. Random reading errors are independent, so they add in quadrature. But a constant offset in the scale (say the zero mark is 0.03 mL off) appears in both readings and cancels in the difference. In general, for $y = a - b$:

$$u(y)^2 = u(a)^2 + u(b)^2 - 2\,r\,u(a)\,u(b)$$

where $r$ is the **correlation coefficient** between the errors of $a$ and $b$. Fully correlated errors ($r = 1$, equal size) cancel completely in a difference and add directly in a sum. You saw the same effect with the slope and intercept of a calibration line in [Lesson 05.3](../module-05/lesson-03.md).

### When the first-order rule fails: Monte Carlo

The first-order rule replaces $f$ by a straight line around the input values. That is fine when the relative uncertainties are small (a few percent). It fails when an input is uncertain enough that $f$ curves noticeably across its spread, for example $1/V$ when $V$ is small and poorly known, or near a detection limit.

The **Monte Carlo method** (JCGM 101) needs no derivatives:

1. Give each input a probability distribution: normal for a Type A uncertainty, rectangular for a tolerance or a certificate's ± limit.
2. Draw a large number of random input sets, for example $10^6$.
3. Push every set through the model.
4. Use the spread of the results: the standard deviation is $u(y)$, and the 2.5th and 97.5th percentiles give a 95 % **coverage interval**, which may be asymmetric.

If Monte Carlo and the first-order rule agree, the simple rule was good enough. If they disagree, trust Monte Carlo.

## Worked example

### 1. Standardising NaOH with KHP

An analyst weighs 0.5106 g KHP by difference on a 0.1 mg balance, dissolves it, and titrates with NaOH to a phenolphthalein end point at 24.87 mL in a 50 mL Class A burette. The KHP certificate says 99.95 ± 0.05 %.

$$c = \frac{0.5106 \times 0.9995}{204.221 \times 0.02487} = 0.10048\ \text{mol/L}$$

The budget:

| Input | Value | Standard uncertainty | How it was found | Relative | Share of variance |
|---|---|---|---|---|---|
| Mass | 0.5106 g | $0.1/\sqrt{6} = 0.041$ mg | resolution, two readings | 0.008 % | 0.2 % |
| Purity | 0.9995 | $0.0005/\sqrt{3} = 0.00029$ | certificate, rectangular | 0.029 % | 2.6 % |
| Volume | 24.87 mL | 0.044 mL | see below | 0.177 % | 97.2 % |
| Molar mass | 204.221 g/mol | negligible | | | 0 % |

The volume uncertainty itself combines three terms: the burette tolerance $0.05/\sqrt{3} = 0.029$ mL, two readings of 0.01 mL each ($0.01\sqrt{2} = 0.014$ mL), and judging the end point, 0.03 mL (about half a drop). $\sqrt{0.029^2 + 0.014^2 + 0.03^2} = 0.044$ mL.

Combined: $\sqrt{0.008^2 + 0.029^2 + 0.177^2} = 0.179\ \%$, so $c = 0.10048 \pm 0.00018$ mol/L. To improve it, sharpen the end point (a pH meter, Lesson 09.5) or use a larger sample and a larger volume. A better balance is pointless.

A Monte Carlo run with $10^6$ draws gives the same: $0.10048 \pm 0.00018$ mol/L, 95 % interval [0.10013, 0.10084]. Here the simple rule was good enough.

### 2. A design where the simple rule fails

Suppose the analyst used only 0.0511 g KHP and measured the 2.00 mL end point with an uncertainty of 0.30 mL (15 %). First order: $c = 0.1250 \pm 0.0188$ mol/L, and a symmetric 95 % interval of [0.0883, 0.1618]. Monte Carlo gives a median of 0.1250 but a mean of 0.1281 and an asymmetric interval of [0.0967, 0.1771]. The reason is the curvature of $1/V$: a volume 0.3 mL too small raises $c$ more than a volume 0.3 mL too large lowers it. The real lesson is the design: never let a result rest on a small, poorly measured quantity.

## Hands-on

**What you need:** a computer with the [Module 9 lab folder](../../labs/module-09/); pencil and paper; the [error analysis template](../../templates/error-analysis.md). **Time:** about 60 minutes.

### Part A — feel the quadrature (15 min)

[Simulation: Measurement error — propagation of uncertainty](../../simulations/measurement-error/index.html?preset=propagation)

Task: the simulation computes a result from several inputs, each with an uncertainty you can change. Halve each input's uncertainty in turn and write down the new combined uncertainty. Target: find the one input whose halving lowers the combined uncertainty most, and check that the simulation's value matches $\sqrt{\sum u_i^2}$ for relative terms to within 2 %.

### Part B — three ways in Python (30 min)

1. Open `lesson03_propagation.py`. Complete TODO 1 (combine the relative uncertainties) and TODO 2 (draw the volumes for the Monte Carlo).
2. Run it:

```bash
py lesson03_propagation.py
```

3. Look at `runs/lesson03_propagation.png`. The left histogram should be a symmetric bell; the right one should have a long tail to high concentrations.
4. Change `u_end` from 0.03 to 0.01 mL and run again. Write down the new combined relative uncertainty and the new share of the volume.

**How you know it worked:** all three methods give $0.10048 \pm 0.00018$ mol/L for the good design, and the bad design shows the asymmetric Monte Carlo interval [0.0967, 0.1771]. With `u_end = 0.01` the combined uncertainty drops to about 0.14 %.

<details><summary>Reference solution for the TODOs</summary>

```python
# TODO 1
u_rel = math.sqrt(sum(r ** 2 for r in rel.values()))
# TODO 2
vs = rng.normal(v_mean, u_v, N_MC)
return conc(ms, ps, vs)
```

With `u_end = 0.01` the volume uncertainty is $\sqrt{0.029^2 + 0.014^2 + 0.01^2} = 0.034$ mL, or 0.135 %, and the combined value is about 0.138 %. The volume still dominates (95 % of the variance), now because of the burette tolerance. The next step would be to calibrate the burette by weighing water, as you did for a syringe in Lesson 01.5. The full script is `lesson03_propagation_solution.py`.

</details>

### Part C — pencil (15 min)

1. A blood sample has pH $7.40 \pm 0.02$. Give $[\text{H}_3\text{O}^+]$ with its standard uncertainty.
2. A density is $\rho = m/V$ with $m = 20.05 \pm 0.04$ g and $V = 20.00 \pm 0.10$ mL. Give $\rho$ and $u(\rho)$, and the share of each input.
3. A volume is read as $R_2 - R_1 = 24.87 - 0.12$ mL. Each reading has a random uncertainty of 0.01 mL and the burette has a constant zero offset of 0.03 mL. What is $u(V)$, and why does the offset not count?

<details><summary>Answers</summary>

1. $[\text{H}_3\text{O}^+] = 10^{-7.40} = 3.98 \times 10^{-8}$ mol/L; relative uncertainty $2.303 \times 0.02 = 4.6\ \%$, so $u = 0.18 \times 10^{-8}$ mol/L.
2. $\rho = 1.0025$ g/mL. Relative: mass 0.20 %, volume 0.50 %; combined 0.54 %, so $u(\rho) = 0.0054$ g/mL. Shares: mass 14 %, volume 86 %.
3. $u(V) = \sqrt{0.01^2 + 0.01^2} = 0.014$ mL. The offset is the same in both readings ($r = 1$), so it cancels in the difference.

</details>

## Common mistakes

- **Adding absolute uncertainties for a product.** For products and quotients, add relative uncertainties in quadrature; for sums and differences, absolute ones.
- **Adding uncertainties linearly.** $0.03 + 0.04 = 0.07$ overstates the result; independent terms combine as $\sqrt{0.03^2 + 0.04^2} = 0.05$.
- **Using a tolerance as a standard uncertainty.** Divide a ±$t$ limit by $\sqrt{3}$ first (Lesson 07.7).
- **Ignoring correlation.** A shared offset cancels in a difference and doubles in a sum; treating it as independent gets both wrong.
- **Trusting the formula for large uncertainties.** When an input's relative uncertainty is more than about 10 % and the model curves, check with Monte Carlo.

## Key takeaways

- Write the measurement model first; the uncertainty follows from it with $u(y)^2 = \sum (\partial f/\partial x_i)^2 u(x_i)^2$.
- Sums: absolute uncertainties in quadrature. Products and quotients: relative ones. Logs and pH: $u(\text{pH}) = 0.434\,u(c)/c$.
- The budget's share-of-variance column shows the one input worth improving.
- Correlated errors cancel in differences; the burette's zero offset is the classic example.
- Monte Carlo propagation (JCGM 101) needs no derivatives and shows asymmetric intervals; use it to check the first-order rule.

## Sources

- [LibreTexts — Harvey, Analytical Chemistry 2.1, 4.3 Propagation of Uncertainty](https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/04%3A_Evaluating_Analytical_Data/4.03%3A_Propagation_of_Uncertainty) (rules for sums, products, powers and logs).
- [JCGM 100:2008 — Guide to the Expression of Uncertainty in Measurement](https://www.bipm.org/en/doi/10.59161/jcgm100-2008e) (law of propagation of uncertainty, correlated inputs).
- [JCGM 101:2008 — GUM Supplement 1, Monte Carlo method](https://www.bipm.org/doi/10.59161/JCGM101-2008) (propagation of distributions, coverage intervals).
- [PubChem — Potassium hydrogen phthalate](https://pubchem.ncbi.nlm.nih.gov/compound/23676735) (molar mass 204.22 g/mol).
- [uncertainties documentation](https://uncertainties.readthedocs.io/) (version 3.2.3 used in the lab).
