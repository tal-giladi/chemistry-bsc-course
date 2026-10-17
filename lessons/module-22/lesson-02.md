---
id: "22.2"
module: 22
minutes: 22
practice_minutes: 55
prerequisites: ["22.1", "05.3", "19.1"]
objectives:
  - Choose a measuring method that matches the timescale of a reaction, from sampling over hours to flash photolysis over nanoseconds.
  - Convert a physical property such as optical rotation or absorbance into fraction converted, and explain how the endpoint value biases the rate constant.
  - Find an order from initial rates on a log–log plot, from half-lives or under isolation conditions.
  - Fit a rate constant by nonlinear least squares with an uncertainty, and use residuals to judge the fit.
volatility: concept
sources:
  - title: "Johnson and Goody (2011), translation of Michaelis and Menten (1913), Supporting Information, Table I"
    url: https://pmc.ncbi.nlm.nih.gov/articles/PMC3381512/
  - title: "LibreTexts Physical Chemistry, 28.6 The Rate Constants of a Reversible Reaction Can Be Determined Using Relaxation Techniques"
    url: https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Physical_Chemistry_(LibreTexts)/28%3A_Chemical_Kinetics_I_-_Rate_Laws/28.06%3A_The_Rate_Constants_of_a_Reversible_Reaction_Can_Be_Determined_Using_Relaxation_Techniques
  - title: "The Nobel Prize in Chemistry 1967 (Eigen, Norrish, Porter)"
    url: https://www.nobelprize.org/prizes/chemistry/1967/summary/
  - title: "The Nobel Prize in Chemistry 1999 (Zewail)"
    url: https://www.nobelprize.org/prizes/chemistry/1999/summary/
  - title: "NIST Chemical Kinetics Database (SRD 17)"
    url: https://kinetics.nist.gov/kinetics/
last_verified: "2026-10-17"
---

# 22.2 · Measuring rates: methods and data analysis

A rate law is only as good as the measurements behind it. You almost never see concentrations directly: you see a colour, a pressure, an electrical conductivity or the angle of polarised light, and you have to turn that signal into concentration against time. Then you have to choose how to analyse it, and the choice can change the answer by a factor of three. This lesson matches methods to timescales, shows how to convert a physical property into fraction converted, collects the standard ways to find an order, and ends with a nonlinear fit of Maud Menten's raw polarimeter readings from 1913.

## Why it matters

In 1913 nobody could weigh or purify an enzyme. Michaelis and Menten still measured invertase kinetics precisely enough that a computer re-analysis a century later agreed with them within a few per cent. Their trick was the observable: sucrose turns polarised light to the right, the glucose and fructose it gives turn it to the left, and the angle changes in proportion to the amount converted. A polarimeter could follow the reaction in a closed tube without taking samples. The modern measurements of $\mathrm{OH + CH_4}$ behind lesson 22.1 do the same thing at a different speed: one laser pulse makes OH in microseconds and a second laser makes the remaining OH fluoresce. Choosing what to measure, how fast and how to fit it decides whether a rate constant is worth anything.

## Core ideas

> [!NOTE]
> The methods and analysis are stable. The polarimeter data are from Michaelis and Menten (1913), Table I, as translated by Johnson and Goody (2011); the technique descriptions for OH + CH₄ are from the NIST Chemical Kinetics Database records, checked on 2026-10-17. Software: SciPy 1.18 `curve_fit`, pinned in `labs/common/requirements.txt`.

### Match the method to the timescale

| Half-life | Method | What is measured |
|---|---|---|
| hours to months | take samples, stop (quench) them by cooling or dilution, analyse | titration, chromatography, NMR |
| seconds to hours | follow a physical property in place | absorbance ([19.1](../module-19/lesson-01.md)), conductivity, pressure, optical rotation |
| about 1 ms to seconds | stopped flow: two syringes push reactants through a mixer into a cell in about a millisecond | absorbance or fluorescence |
| nanoseconds to ms | flash photolysis: a light pulse creates a reactive species at time zero | absorption or laser-induced fluorescence |
| nanoseconds to ms, at equilibrium | relaxation: a sudden jump in temperature or pressure shifts an equilibrium | the return to the new equilibrium |
| femtoseconds to picoseconds | pump–probe lasers | the motion of atoms during the reaction itself |

Flash photolysis and relaxation methods won Norrish, Porter and Eigen the 1967 Nobel Prize; femtosecond pump–probe work won Zewail the 1999 prize. The rule is simple: the dead time of the method (the time before the first good reading) must be much shorter than the half-life. For high temperatures, chemists use **shock tubes**, where a shock wave heats a gas to over 1000 K in microseconds; the OH + CH₄ data up to 2025 K in lesson 22.4 come from one.

### Physical properties and the endpoint

Most physical properties $P$ are linear in the concentrations: absorbance by Beer–Lambert, optical rotation because each sugar adds its own angle, conductivity at low concentration. Then $P$ changes in proportion to the extent of reaction, and the fraction converted is

$$x = \frac{P_0 - P}{P_0 - P_\infty}$$

where $P_0$ is the value at the start and $P_\infty$ the value when the reaction is complete. You never need the absorptivity or the specific rotation. You do need $P_\infty$, and that is the weak point. There are three ways to get it:

1. **Measure it** after ten half-lives or more (Michaelis and Menten read their tubes again after 24 hours).
2. **Calculate it** from the stoichiometry and the properties of the pure products (their "theoretical endpoint").
3. **Fit it** as a free parameter together with $k$.

A common shortcut, taking the last reading as $P_\infty$, is a bad mistake: the last points then sit close to zero on the $\ln$ plot and drag the slope steeply down. For experiment 5 of the 1913 data it triples the rate constant (Hands-on).

### Four ways to find an order

- **Integral method.** Fit the integrated laws and see which describes the data over a large conversion (lesson [22.1](lesson-01.md)).
- **Initial rates.** Measure the rate at the start, $v_0$, for several starting concentrations. Since $v_0 = k[\mathrm{A}]_0^{\alpha}$, a plot of $\ln v_0$ against $\ln[\mathrm{A}]_0$ is a straight line with slope $\alpha$. Products have not built up yet, so they cannot interfere. If the plot is curved, the order changes with concentration.
- **Half-lives.** For order $n$, $t_{1/2} \propto [\mathrm{A}]_0^{1-n}$: independent of $[\mathrm{A}]_0$ for first order, doubling when $[\mathrm{A}]_0$ halves for second order.
- **Isolation.** Flood the reaction with all reactants but one, so the order in that one shows up alone (pseudo-first-order, lesson [22.1](lesson-01.md)).

### Relaxation methods

Some reactions are too fast to mix. If they are reversible, you can start them by shifting the equilibrium instead: heat the solution by a few kelvin in a microsecond with an electrical discharge or a laser pulse. The system relaxes to the new equilibrium exponentially. For $\mathrm{A} \rightleftharpoons \mathrm{B}$ the relaxation time is $\tau = 1/(k_f + k_r)$, as in lesson 22.1; together with $K = k_f/k_r$ this gives both constants. For $\mathrm{A + B} \rightleftharpoons \mathrm{C}$, linearising about equilibrium gives

$$\frac{1}{\tau} = k_f\left([\mathrm{A}]_\text{eq} + [\mathrm{B}]_\text{eq}\right) + k_r$$

Eigen used this to show that $\mathrm{H^+ + OH^-} \to \mathrm{H_2O}$ in water runs faster than 10¹¹ L mol⁻¹ s⁻¹, about as fast as the ions can diffuse together.

### Fitting: linearise or not?

The straight-line plots of lesson 22.1 are good for deciding an order by eye. For the final numbers, fit the model directly with nonlinear least squares (`scipy.optimize.curve_fit`, lesson [05.3](../module-05/lesson-03.md)), because taking logarithms distorts the noise: a reading uncertain by 0.01° near the end of a run, where $P - P_\infty$ is small, becomes a huge error in $\ln(P - P_\infty)$. A nonlinear fit also returns standard uncertainties from the covariance matrix. Then look at the residuals (data minus fit). Random scatter means the model is adequate. A smooth pattern, such as residuals that are negative in the middle and positive at both ends, means the model is wrong, however small the uncertainties look. A free endpoint makes model errors harder to see: it can shift to absorb them, which is what happens with the 1913 data, where product inhibition makes the decay slightly non-exponential.

## Worked example

### 1. From polarimeter angles to an initial rate

Experiment 1 of 1913: 333 mM sucrose, start angle 14.124° (extrapolated), and a theoretical total change of 18.57° for complete inversion.

1. At 117 min the angle is 10.156°, so $x = (14.124 - 10.156)/18.57 = 0.214$.
2. In the first 26 minutes the angle falls from 14.124° to 13.144°: $0.980/26 = 0.0377$ degrees per minute.
3. One degree corresponds to $333/18.57 = 17.9$ mM of sucrose, so the initial rate is $0.0377 \times 17.9 = 0.676$ mM/min.

No specific rotation or path length was needed: the theoretical endpoint carries the calibration.

### 2. The order from initial rates

Michaelis and Menten list initial rates (in their own units) of 0.866 at 5.2 mM and 1.466 at 10.4 mM, then 3.636 at both 167 mM and 333 mM.

1. Low range: $\alpha = \ln(1.466/0.866)/\ln(10.4/5.2) = 0.526/0.693 = 0.76$.
2. High range: $\alpha = \ln(3.636/3.636)/\ln 2 = 0$.

The local order falls smoothly from about 0.8 to 0 as the enzyme saturates. The arbitrary units cancel in the ratios, which is why initial-rate orders need no calibration at all.

## Hands-on

What you need: pencil, calculator, Python with the course packages and the [Module 22 lab folder](../../labs/module-22/). Write up Part B with the [error-analysis template](../../templates/error-analysis.md). Time: about 55 minutes.

### Part A — pencil (20 min)

1. Pick a method for each: (a) hydrolysis of aspirin in stored tablets, half-life of months; (b) a food dye fading in dilute bleach, half-life about 2 minutes; (c) carbon monoxide binding to haemoglobin after mixing, half-life about 5 ms; (d) a proton transfer at equilibrium in water, relaxation time about 1 µs.
2. For $2\mathrm{A} \to$ products, the half-life is 50 s when $[\mathrm{A}]_0 = 0.020$ M and 100 s when $[\mathrm{A}]_0 = 0.010$ M. What is the order and the rate constant for $-d[\mathrm{A}]/dt$?
3. After a temperature jump, $\mathrm{A} \rightleftharpoons \mathrm{B}$ relaxes with $\tau = 2.0$ µs. At the new temperature $K = 3.0$. Find $k_f$ and $k_r$.
4. A product absorbs light. The absorbance is 0.050 at the start, 0.450 at 60 s and 0.850 after an hour (complete). Find the first-order $k$. What do you get if you use the reading at 5 minutes, 0.800, as the endpoint?

<details><summary>Answers to Part A</summary>

1. (a) Samples analysed by chromatography (HPLC) every few weeks, often at raised temperature to speed it up. (b) Absorbance in a spectrophotometer or a phone camera (lesson 23.4). (c) Stopped flow with absorbance detection; its dead time of about 1 ms is shorter than 5 ms. (d) A temperature-jump relaxation experiment; nothing can be mixed in a microsecond.
2. Halving $[\mathrm{A}]_0$ doubled the half-life, so $t_{1/2} \propto 1/[\mathrm{A}]_0$: second order. $t_{1/2} = 1/(k[\mathrm{A}]_0)$ gives $k = 1/(0.020 \times 50) = 1.0$ L mol⁻¹ s⁻¹.
3. $k_f + k_r = 1/\tau = 5.0\times10^5$ s⁻¹ and $k_f = 3k_r$, so $k_r = 1.25\times10^5$ s⁻¹ and $k_f = 3.75\times10^5$ s⁻¹.
4. $x = (0.450 - 0.050)/(0.850 - 0.050) = 0.50$ at 60 s, so $k = \ln 2/60 = 0.0116$ s⁻¹. With 0.800 as the endpoint, $x = 0.533$ and $k = -\ln(0.467)/60 = 0.0127$ s⁻¹, 10 % too high from one early reading.

</details>

### Part B — Python: Menten's raw readings (35 min)

1. Open `lesson02_methods.py`. It reads `invertase_rotation.csv` (polarimeter angles of experiments 1 and 5 from Table I of the 1913 paper) and `invertase_initial_rates.csv` (the seven initial rates of the same table).
2. Complete `rotation_to_fraction()`, `fit_free_endpoint()` (a three-parameter `curve_fit`), `initial_rate()` and `local_orders()`.
3. Run it and open `runs/lesson02_methods.png`:

```bash
py lesson02_methods.py
```

How you know it worked: experiment 5 converts to $x$ = 0.331, 0.451, 0.611, 0.737 and 0.860 at 17, 27, 38, 62 and 95 min, the same values Johnson and Goody tabulate. The $\ln$ plot with the theoretical endpoint (−0.284°) gives $k = 0.0206$ min⁻¹; taking the last reading as the endpoint gives 0.0668 min⁻¹, more than three times too large. The free-endpoint fit gives $P_\infty = -0.210 \pm 0.033$° and $k = 0.0258 \pm 0.0018$ min⁻¹. The initial rate of experiment 1 is 0.0379 degrees per minute, 0.680 mM/min. The local orders fall from 0.76 to 0.00.

Look hard at the free fit. Its endpoint misses the theoretical value by more than twice its own uncertainty, and the reading Michaelis and Menten took after 24 hours (−0.272°) by almost twice. The residuals in the middle panel scatter by about ±0.03°, close to the reading precision the authors quote (a few hundredths of a degree), so with eight points they cannot show the problem. The decay is not quite a single exponential, because glucose and fructose slow the enzyme as they build up, and the free endpoint quietly bends to absorb that. A small error bar is not proof of a right model; an independent endpoint is a better check.

<details><summary>Reference solution</summary>

```python
def rotation_to_fraction(rot, rot0, rot_inf):
    return (rot0 - rot) / (rot0 - rot_inf)

def fit_free_endpoint(t, p):
    popt, pcov = curve_fit(first_order_property, t, p, p0=(p[-1], p[0], 3 / t[-1]))
    return popt, np.sqrt(np.diag(pcov))

def initial_rate(t, p, t_max):
    m = t <= t_max
    return np.polyfit(t[m], p[m], 1)[0]

def local_orders(S, v):
    return np.diff(np.log(v)) / np.diff(np.log(S))
```

Full code: `lesson02_methods_solution.py`.

</details>

## Common mistakes

- Using the last reading as $P_\infty$. Measure the endpoint after ten half-lives, calculate it, or fit it, and say which you did.
- Picking a method whose dead time is close to the half-life. You then miss the start and fit the tail.
- Taking an "initial rate" over too long a window. Use the part where the curve is still straight, here the first 10–20 % of conversion.
- Trusting a small fit uncertainty without looking at residuals. A wrong model fits with confident, wrong numbers.
- Treating linearised plots as the final analysis. Use them to choose the model, then fit the model to the raw signal.
- Forgetting that a physical property must be linear in concentration for $x = (P_0 - P)/(P_0 - P_\infty)$. Check Beer–Lambert linearity before trusting absorbances above about 1.

## Key takeaways

- Choose the method by the half-life: sampling, physical property, stopped flow, flash photolysis, relaxation, pump–probe.
- A linear property gives $x = (P_0 - P)/(P_0 - P_\infty)$ without any calibration, but the endpoint must be right.
- Orders come from integrated laws, initial rates (slope of $\ln v_0$ against $\ln[\mathrm{A}]_0$), half-lives or isolation.
- Relaxation after a jump gives $1/\tau = k_f + k_r$ for A ⇌ B, and with $K$ both rate constants.
- Fit the raw data by nonlinear least squares, report uncertainties, and read the residuals before believing them.

## Sources

- [Johnson and Goody (2011), translation of Michaelis and Menten (1913), Supporting Information](https://pmc.ncbi.nlm.nih.gov/articles/PMC3381512/) — Table I polarimeter readings, theoretical endpoints and initial rates in `invertase_rotation.csv` and `invertase_initial_rates.csv`.
- [LibreTexts Physical Chemistry, 28.6 Relaxation Techniques](https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Physical_Chemistry_(LibreTexts)/28%3A_Chemical_Kinetics_I_-_Rate_Laws/28.06%3A_The_Rate_Constants_of_a_Reversible_Reaction_Can_Be_Determined_Using_Relaxation_Techniques) — temperature jump and relaxation times.
- [The Nobel Prize in Chemistry 1967](https://www.nobelprize.org/prizes/chemistry/1967/summary/) — Eigen, Norrish and Porter, very fast reactions started by short pulses of energy.
- [The Nobel Prize in Chemistry 1999](https://www.nobelprize.org/prizes/chemistry/1999/summary/) — Zewail, femtosecond spectroscopy of transition states.
- [NIST Chemical Kinetics Database, SRD 17](https://kinetics.nist.gov/kinetics/) — technique fields of the OH + CH₄ records: flash photolysis with laser-induced fluorescence (Gierczak et al. 1997) and reflected shock tube with UV absorption of OH at 308 nm (Srinivasan et al. 2005).
