---
id: "22.1"
module: 22
minutes: 22
practice_minutes: 50
prerequisites: ["03.3", "03.5", "13.6"]
objectives:
  - Write the rate of reaction from a balanced equation and give the units of the rate constant for any order, in solution and gas-phase units.
  - Distinguish the order of a rate law from the molecularity of a step, and reduce a second-order reaction to pseudo-first-order conditions.
  - Solve the reversible first-order reaction A ⇌ B and relate kf + kr to the relaxation time and kf/kr to the equilibrium constant.
  - Decide the order of a real reaction by testing how its rate responds to concentration, not only by comparing R² values.
volatility: concept
sources:
  - title: "OpenStax Chemistry 2e, 12.3 Rate Laws"
    url: https://openstax.org/books/chemistry-2e/pages/12-3-rate-laws
  - title: "LibreTexts Physical Chemistry, 28.5 Reactions can also be Reversible"
    url: https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Physical_Chemistry_(LibreTexts)/28%3A_Chemical_Kinetics_I_-_Rate_Laws/28.05%3A_Reactions_can_also_be_Reversible
  - title: "NIST Chemical Kinetics Database (SRD 17), CH4 + OH → CH3 + H2O"
    url: https://kinetics.nist.gov/kinetics/
  - title: "Prather, Holmes and Hsu (2012), Reactive greenhouse gas scenarios, Geophys. Res. Lett. 39, L09803"
    url: https://escholarship.org/uc/item/1g30p07v
  - title: "Johnson and Goody (2011), The original Michaelis constant: translation of the 1913 Michaelis–Menten paper, Biochemistry 50, 8264"
    url: https://pmc.ncbi.nlm.nih.gov/articles/PMC3381512/
last_verified: "2026-10-17"
---

# 22.1 · Rate laws and integrated rate laws

Thermodynamics tells you where a reaction ends; kinetics tells you how fast it gets there and by which route. In [03.3](../module-03/lesson-03.md) you solved the zero-, first- and second-order rate laws as differential equations, and in [03.5](../module-03/lesson-05.md) you coupled two of them. This lesson adds the chemistry: rates when the coefficients are not 1, orders as measured numbers, pseudo-first-order conditions and reactions that run both ways. You will finish by testing the order of the first enzyme reaction ever studied quantitatively, with the data Maud Menten recorded in 1913.

## Why it matters

Methane is the second most important greenhouse gas made by people. Its warming effect depends on how long it stays in the air, a kinetics question. Methane is removed mainly by the hydroxyl radical, OH, in a single second-order step, $\mathrm{OH + CH_4 \to CH_3 + H_2O}$. OH is so reactive that its concentration stays tiny and roughly constant, so the loss of methane looks first order, with a lifetime of about a decade. Get the rate constant wrong by a factor of two and the lifetime, and the warming from a methane leak, is wrong by the same factor. The same reasoning sets drug half-lives and shelf lives.

## Core ideas

> [!NOTE]
> The ideas here are stable. The OH + CH₄ rate constant is the JPL evaluation (1997) as listed in the NIST Chemical Kinetics Database, SRD 17, Data Version 2026, checked on 2026-10-17; later evaluations differ by under 2 % at room temperature. The invertase data are from the 1913 paper as tabulated by Johnson and Goody (2011).

### The rate of reaction

For a reaction $a\mathrm{A} + b\mathrm{B} \to c\mathrm{C} + d\mathrm{D}$, each species changes at a different speed. To get one number for the whole reaction, divide each derivative by its stoichiometric coefficient:

$$v = -\frac{1}{a}\frac{d[\mathrm{A}]}{dt} = -\frac{1}{b}\frac{d[\mathrm{B}]}{dt} = \frac{1}{c}\frac{d[\mathrm{C}]}{dt} = \frac{1}{d}\frac{d[\mathrm{D}]}{dt}$$

$v$ is the **rate of reaction**, in mol L⁻¹ s⁻¹. For $2\mathrm{N_2O_5} \to 4\mathrm{NO_2} + \mathrm{O_2}$, NO₂ appears four times as fast as O₂ and twice as fast as N₂O₅ disappears, but $v$ is the same whichever species you measure. Always say which definition you use: a rate constant quoted for $-d[\mathrm{N_2O_5}]/dt$ is twice the one for $v$.

### Rate laws and order

A **rate law** is the measured link between rate and concentrations, usually a product of powers:

$$v = k[\mathrm{A}]^{\alpha}[\mathrm{B}]^{\beta}$$

$\alpha$ is the **order** with respect to A, $\alpha + \beta$ the overall order and $k$ the **rate constant**. Orders come from experiment. They need not match the coefficients in the equation and need not be whole numbers: the gas-phase reaction $\mathrm{H_2 + Br_2 \to 2HBr}$ is order ½ in Br₂ at the start (lesson [22.3](lesson-03.md)). Some rate laws have no order at all, because they are not a simple product of powers; enzyme kinetics is the standard example.

The units of $k$ follow from the order $n$: (mol L⁻¹)$^{1-n}$ s⁻¹. Gas-phase chemists count molecules instead of moles, so a second-order $k$ is in cm³ molecule⁻¹ s⁻¹. To convert, multiply by $N_A$ and by 10⁻³ L cm⁻³:

$$6.26\times10^{-15}\ \mathrm{cm^3\,molecule^{-1}\,s^{-1}} \times 6.022\times10^{23} \times 10^{-3} = 3.77\times10^{6}\ \mathrm{L\,mol^{-1}\,s^{-1}}$$

### Order is not molecularity

An **elementary reaction** is one step that happens as written, in one collision or one molecular event. Its **molecularity** is the number of particles that take part: one (unimolecular, a molecule falling apart), two (bimolecular, a collision) or, rarely, three (termolecular). For an elementary step, and only then, the order equals the molecularity and the orders equal the coefficients. $\mathrm{OH + CH_4 \to CH_3 + H_2O}$ is elementary: first order in each reactant. Most overall equations are not; their rate laws are clues to the mechanism (lesson [22.3](lesson-03.md)).

### Integrated rate laws, briefly

The integrated forms from [03.3](../module-03/lesson-03.md) still hold: $[\mathrm{A}] = [\mathrm{A}]_0 - kt$ (zero order), $\ln[\mathrm{A}] = \ln[\mathrm{A}]_0 - kt$ (first) and $1/[\mathrm{A}] = 1/[\mathrm{A}]_0 + kt$ (second, $2\mathrm{A}\to$ products with $-d[\mathrm{A}]/dt = k[\mathrm{A}]^2$). For $\mathrm{A + B}$ with unequal starting concentrations:

$$\ln\frac{[\mathrm{B}][\mathrm{A}]_0}{[\mathrm{A}][\mathrm{B}]_0} = ([\mathrm{B}]_0 - [\mathrm{A}]_0)\,kt$$

Chemists usually avoid this form with the next trick.

### Pseudo-first-order conditions

If B is in large excess, $[\mathrm{B}]$ hardly changes while A is used up. Then $v = k[\mathrm{A}][\mathrm{B}] \approx k'[\mathrm{A}]$ with $k' = k[\mathrm{B}]_0$, and A decays as a single exponential. This is called **pseudo-first-order** (or isolation) conditions. Measure $k'$ at several values of $[\mathrm{B}]_0$; a straight line of $k'$ against $[\mathrm{B}]_0$ through the origin confirms first order in B and its slope is $k$. A tenfold excess makes the error in $k'$ a few per cent; a fiftyfold excess makes it negligible.

The atmosphere runs this experiment for us. OH is held near a steady, very low level (of order 10⁶ molecules cm⁻³, about one OH per 10¹³ air molecules) by its fast formation and loss, so methane decays with $k' = k[\mathrm{OH}]$ and a **lifetime** $\tau = 1/k'$, the time to fall to $1/e$ of its value. The half-life is $\tau\ln 2$.

### Reversible first-order reactions

Many reactions run both ways: $\mathrm{A} \rightleftharpoons \mathrm{B}$ with forward constant $k_f$ and reverse constant $k_r$. Then

$$\frac{d[\mathrm{A}]}{dt} = -k_f[\mathrm{A}] + k_r[\mathrm{B}]$$

With $[\mathrm{A}] + [\mathrm{B}]$ constant, the solution is

$$[\mathrm{A}] - [\mathrm{A}]_\text{eq} = ([\mathrm{A}]_0 - [\mathrm{A}]_\text{eq})\,e^{-(k_f + k_r)t}$$

Two results follow. First, the system relaxes to equilibrium with the rate constant $k_f + k_r$, the *sum*, not $k_f$; the relaxation time is $\tau = 1/(k_f + k_r)$. Second, at equilibrium the forward and reverse rates are equal, so

$$K = \frac{[\mathrm{B}]_\text{eq}}{[\mathrm{A}]_\text{eq}} = \frac{k_f}{k_r}$$

This links kinetics to the equilibrium constants of [13.6](../module-13/lesson-06.md): if you know $K$ from thermodynamics and measure the relaxation, you get both rate constants. It is the basis of the relaxation methods in lesson [22.2](lesson-02.md).

### The same reaction can change order

Invertase splits sucrose into glucose and fructose. In 1913 Michaelis and Menten found it **zero order** in sucrose at high concentration (the enzyme is saturated) and nearly **first order** at low concentration (worked example 2). Order describes a range of conditions, not a fixed property of a reaction; lesson [22.5](lesson-05.md) gives the full rate law.

Try both simple orders in the simulation and watch which plot turns straight:

[Simulation: Kinetics — first-order decay](../../simulations/kinetics/index.html?preset=first-order)

[Simulation: Kinetics — second-order decay](../../simulations/kinetics/index.html?preset=second-order)

## Worked example

### 1. The lifetime of methane

The JPL evaluation gives $k = 2.46\times10^{-12}\,e^{-1780/T}$ cm³ molecule⁻¹ s⁻¹ (activation energy 14.8 kJ/mol, valid 200–300 K). Most methane is destroyed in the lower atmosphere, where a typical temperature is about 272 K (the value Prather and co-workers use to scale OH reactions).

1. $k(272\ \mathrm{K}) = 2.46\times10^{-12} \times e^{-6.544} = 2.46\times10^{-12} \times 1.44\times10^{-3} = 3.54\times10^{-15}$ cm³ molecule⁻¹ s⁻¹.
2. With $[\mathrm{OH}] = 1.0\times10^6$ cm⁻³: $k' = 3.54\times10^{-9}$ s⁻¹.
3. $\tau = 1/k' = 2.83\times10^8$ s $= 9.0$ years; half-life $9.0 \times 0.693 = 6.2$ years.

Prather and co-workers (2012) derived a total lifetime of 9.1 ± 0.9 years from observations. Their budget assigns lifetimes of about 120 years to stratospheric loss, 150 years to soils and 200 years to chlorine; because loss frequencies add, the part due to tropospheric OH is $1/(1/9.1 - 1/120 - 1/150 - 1/200) pprox 11$ years. Our one-line estimate lands in the right place. It cannot do better because OH is not uniform: it is highest in the sunny tropics, and methane that sits in cold air reacts more slowly.

### 2. Zero order or first order? Read the 1913 data

From Johnson and Goody's Table 1 (fraction $x$ of the sucrose converted):

| Sucrose at start | Time | $x$ | Average rate $x[\mathrm{S}]_0/t$ |
|---|---|---|---|
| 333 mM | 117 min | 0.2137 | 0.608 mM/min |
| 166.7 mM | 103 min | 0.378 | 0.612 mM/min |

Halving the sucrose left the rate unchanged: zero order. At 20.8 mM, $\ln(1-x)$ is $-0.944$ at 38 min and $-1.333$ at 62 min, giving $k = 0.0248$ and $0.0215$ min⁻¹, close to each other: nearly first order, with a half-life near 30 minutes. The small drift in $k$ is real: the products bind to the enzyme and slow it down, an effect the 1913 authors already included (lesson [22.5](lesson-05.md)).

## Hands-on

What you need: pencil, calculator, Python with the course packages and the [Module 22 lab folder](../../labs/module-22/). Record the results on a [notebook page](../../templates/notebook-page.md). Time: about 50 minutes.

### Part A — pencil (15 min)

1. NIST SRD 17 lists $k(298\ \mathrm{K}) = 1.95\times10^{-38}$ cm⁶ molecule⁻² s⁻¹ for $\mathrm{2NO + O_2 \to 2NO_2}$, third order. What are the units of $k$ in mol and L, and what is the overall order?
2. An isomerisation $\mathrm{A} \rightleftharpoons \mathrm{B}$ has $k_f = 0.030$ s⁻¹ and $k_r = 0.010$ s⁻¹. Start with $[\mathrm{A}]_0 = 1.00$ M and no B. Find $K$, the relaxation time and $[\mathrm{A}]$ after 30 s.
3. A dye at $1\times10^{-5}$ M fades in 0.10 M NaOH with $k' = 0.024$ s⁻¹ (an illustrative case). What is the second-order rate constant? Would pseudo-first-order analysis still work in $1\times10^{-4}$ M NaOH?
4. Hydroxyl at $1\times10^6$ cm⁻³ removes methane with a lifetime of 9 years. If a change in emissions lowered OH by 10 %, by how much would the lifetime change?

<details><summary>Answers to Part A</summary>

1. Third order overall (second in NO, first in O₂). Units: L² mol⁻² s⁻¹. Converting: multiply by $N_A^2 \times 10^{-6}$, giving $1.95\times10^{-38} \times 3.63\times10^{47} \times 10^{-6} = 7.1\times10^{3}$ L² mol⁻² s⁻¹.
2. $K = 0.030/0.010 = 3.0$, so $[\mathrm{A}]_\text{eq} = 1/(1+K) = 0.25$ M. Relaxation constant $k_f + k_r = 0.040$ s⁻¹, $\tau = 25$ s. $[\mathrm{A}](30\ \mathrm{s}) = 0.25 + 0.75\,e^{-1.2} = 0.25 + 0.226 = 0.48$ M.
3. $k = k'/[\mathrm{OH^-}] = 0.024/0.10 = 0.24$ L mol⁻¹ s⁻¹. In $1\times10^{-4}$ M NaOH the excess is only tenfold, so [OH⁻] falls by up to 10 % during the run: the decay is no longer a clean exponential and $k'$ is a few per cent off. Use at least a tenfold, better a fiftyfold, excess.
4. $\tau = 1/(k[\mathrm{OH}])$, so 10 % less OH means $\tau = 9/0.9 = 10$ years, 11 % longer.

</details>

### Part B — Python: the order of the first enzyme reaction (35 min)

1. Open `lesson01_orders.py`. It reads `invertase_timecourse.csv`: the fraction of sucrose converted against time at five starting concentrations, from Michaelis and Menten (1913) as tabulated by Johnson and Goody (2011).
2. Complete `zero_order_test()` (straight line of $x$ against $t$), `first_order_test()` (straight line of $\ln(1-x)$ against $t$) and `pseudo_first_order_lifetime()`.
3. Run it and open `runs/lesson01_orders.png`:

```bash
py lesson01_orders.py
```

How you know it worked: at 333 mM and 166.7 mM the zero-order rates are 0.594 and 0.600 mM/min, equal within 1 %, so the rate does not depend on the concentration. At 41.6 mM and 20.8 mM the first-order constants are 0.019 and 0.021 min⁻¹, nearly equal, and the first-order $R^2$ (0.983, 0.982) beats the zero-order one (0.931, 0.942). The methane lifetime at 272 K is 9.0 years for $[\mathrm{OH}] = 1.0\times10^6$ cm⁻³.

Look at the 333 mM row: both $R^2$ values are above 0.999. Only 21 % of the sucrose reacted, and over a small conversion every order gives a straight line. The test that decides is the comparison between concentrations, not the $R^2$.

<details><summary>Reference solution</summary>

```python
def zero_order_test(t, x):
    return line_fit(t, x)

def first_order_test(t, x):
    return line_fit(t, np.log(1 - x))

def pseudo_first_order_lifetime(k2, partner):
    return 1.0 / (k2 * partner)
```

Full code: `lesson01_orders_solution.py`. The zero-order rate in mM/min is the slope times $[\mathrm{S}]_0$, because $x$ is a fraction.

</details>

## Common mistakes

- Reading orders off the balanced equation. Orders are measured. They equal the coefficients only for an elementary step.
- Quoting $k$ without saying whether the rate is $v$ or $-d[\mathrm{A}]/dt$. For $2\mathrm{A} \to$ products the two differ by a factor of 2.
- Mixing units: a gas-phase $k$ in cm³ molecule⁻¹ s⁻¹ used with concentrations in mol/L is wrong by a factor of $6\times10^{20}$.
- Fitting $e^{-k_f t}$ to a reversible reaction. The observed constant is $k_f + k_r$, and the curve levels off at $[\mathrm{A}]_\text{eq}$, not at zero.
- Deciding the order from a few per cent of conversion. Follow the reaction past 50 % or, better, change the starting concentration and see how the rate responds.
- Forgetting that pseudo-first-order needs a real excess. Check that the excess reagent changes by less than a few per cent.

## Key takeaways

- The rate of reaction is $\frac{1}{\nu_i}\frac{d[i]}{dt}$, the same whichever species you follow.
- Orders are experimental; molecularity belongs to elementary steps, where the two agree.
- Units of $k$ are (mol L⁻¹)$^{1-n}$ s⁻¹; gas-phase values use molecules and cm³.
- A large excess of B turns $k[\mathrm{A}][\mathrm{B}]$ into $k'[\mathrm{A}]$ with lifetime $1/(k[\mathrm{B}])$: this is how methane's decade-long lifetime arises.
- A reversible reaction relaxes with $k_f + k_r$ and settles at $K = k_f/k_r$.
- The same reaction can be zero order in one range and first order in another; test the order where you will use it.

## Sources

- [OpenStax Chemistry 2e, 12.3 Rate Laws](https://openstax.org/books/chemistry-2e/pages/12-3-rate-laws) — rate of reaction, orders, units of $k$.
- [LibreTexts Physical Chemistry, 28.5 Reactions can also be Reversible](https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Physical_Chemistry_(LibreTexts)/28%3A_Chemical_Kinetics_I_-_Rate_Laws/28.05%3A_Reactions_can_also_be_Reversible) — A ⇌ B and the relaxation constant $k_f + k_r$.
- [NIST Chemical Kinetics Database, SRD 17](https://kinetics.nist.gov/kinetics/) — CH₄ + OH → CH₃ + H₂O (JPL 1997 evaluation: $A = 2.46\times10^{-12}$ cm³ molecule⁻¹ s⁻¹, $E_a = 14.8$ kJ/mol, $k_{298} = 6.26\times10^{-15}$) and 2NO + O₂ (IUPAC 2004, $k_{298} = 1.95\times10^{-38}$ cm⁶ molecule⁻² s⁻¹), retrieved 2026-10-17.
- [Prather, Holmes and Hsu (2012), Geophys. Res. Lett. 39, L09803](https://escholarship.org/uc/item/1g30p07v) — methane lifetime 9.1 ± 0.9 years; budget terms for stratosphere, soils and chlorine; 272 K for scaling OH reactions.
- [Johnson and Goody (2011), Biochemistry 50, 8264](https://pmc.ncbi.nlm.nih.gov/articles/PMC3381512/) — Table 1, the 1913 invertase time courses in `invertase_timecourse.csv`.
