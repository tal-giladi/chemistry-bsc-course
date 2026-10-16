---
id: "02.5"
module: 2
minutes: 25
practice_minutes: 120
prerequisites: ["02.2", "02.3", "02.4"]
objectives:
  - Compute partial derivatives of a function of several variables, such as p(n, T, V), and state which variables are held constant.
  - Use the total differential to estimate how small changes or uncertainties in several inputs combine.
  - Measure a cooling curve at home and extract a cooling constant with a log fit and with numerical derivatives.
  - Identify which measured input limits a prediction by comparing partial-derivative error terms.
volatility: concept
sources:
  - title: "OpenStax Calculus Volume 3, 4.3 Partial Derivatives"
    url: https://openstax.org/books/calculus-volume-3/pages/4-3-partial-derivatives
  - title: "Levitus, Mathematical Methods in Chemistry (LibreTexts), chapter 8 Calculus in More than One Variable"
    url: https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Mathematical_Methods_in_Chemistry_(Levitus)
  - title: "OpenStax Calculus Volume 1, 6.8 Exponential Growth and Decay (Newton's law of cooling)"
    url: https://openstax.org/books/calculus-volume-1/pages/6-8-exponential-growth-and-decay
  - title: "NIST Chemistry WebBook: Water, condensed-phase thermochemistry"
    url: https://webbook.nist.gov/cgi/cbook.cgi?ID=C7732185&Mask=2
  - title: "MIT OpenCourseWare 18.02SC Multivariable Calculus"
    url: https://ocw.mit.edu/courses/18-02sc-multivariable-calculus-fall-2010/
last_verified: "2026-10-16"
---

# 02.5 · Functions of several variables and partial derivatives

Most chemical quantities depend on more than one thing: gas pressure on amount, temperature and volume; a cooling drink's temperature on time, room temperature and how well the mug is insulated. A partial derivative asks how the output changes when you nudge one input and hold the others still. This lesson teaches partial derivatives and the total differential, then ends with the module's practical: measure a cooling curve in your kitchen and analyse it with every tool from Module 2.

## Why it matters

Thermodynamics (Modules 8, 13 and 21) is written almost entirely in partial derivatives, such as $(\partial H/\partial T)_p$, the heat capacity at constant pressure. The subscript tells you what is held fixed, and getting it wrong gives a different, wrong quantity. Partial derivatives also answer a practical lab question every time you report a result: "Which of my measurements limits the accuracy?" If the answer is the thermometer, buying a better balance is wasted money.

## Core ideas

> [!NOTE]
> The mathematics is stable. The heat capacity of water (about 75.4 J mol⁻¹ K⁻¹, or 4.18 J g⁻¹ K⁻¹ near room temperature) is from the NIST Chemistry WebBook, checked 2026-10-16. Newton's law of cooling is an approximation for a mug of water; the practical shows where it bends.

### Partial derivatives

For $p(n, T, V) = nRT/V$, the partial derivative with respect to $T$ treats $n$ and $V$ as constants:

$$\left(\frac{\partial p}{\partial T}\right)_{n,V} = \frac{nR}{V},\qquad \left(\frac{\partial p}{\partial V}\right)_{n,T} = -\frac{nRT}{V^2},\qquad \left(\frac{\partial p}{\partial n}\right)_{T,V} = \frac{RT}{V}$$

The curly $\partial$ means "other variables held fixed". Chemists write those variables as subscripts, because in thermodynamics the same symbol can be a function of different sets of variables.

Tiny example: 1.00 mol at 298.15 K in 24.5 L. $(\partial p/\partial T)_V = 8.314/0.0245\ \mathrm{m^3} = 339$ Pa/K. Warm a sealed flask by 1 K and the pressure rises by 339 Pa, about 0.3 %.

### Mixed partials are equal

Differentiate first by $T$, then by $V$, or the other way round: you get the same answer for any smooth function.

$$\frac{\partial}{\partial V}\left(\frac{\partial p}{\partial T}\right) = \frac{\partial}{\partial T}\left(\frac{\partial p}{\partial V}\right) = -\frac{nR}{V^2}$$

This simple fact produces the Maxwell relations of thermodynamics, which let you compute hard-to-measure quantities from easy ones.

### The total differential

If every input changes a little, the output changes by the sum of the separate effects:

$$dp = \left(\frac{\partial p}{\partial T}\right)dT + \left(\frac{\partial p}{\partial V}\right)dV + \left(\frac{\partial p}{\partial n}\right)dn$$

This is a first-order Taylor expansion (lesson [02.4](lesson-04.md)) in several variables.

### From total differential to uncertainty

When the input errors are independent and random, they do not simply add; they add in quadrature (square, sum, square root):

$$u_f = \sqrt{\left(\frac{\partial f}{\partial x}u_x\right)^2 + \left(\frac{\partial f}{\partial y}u_y\right)^2 + \dots}$$

Each term is an error contribution. Compare them: the biggest one is the measurement worth improving. Module 9 builds this into a full uncertainty budget; here you only need the idea.

### The model for the practical: Newton's law of cooling

A hot object loses heat at a rate proportional to how much hotter it is than the room:

$$\frac{dT}{dt} = -k\,(T - T_\text{env}) \quad\Rightarrow\quad T(t) = T_\text{env} + (T_0 - T_\text{env})\,e^{-kt}$$

$T$ depends on time and on three parameters, $k$, $T_0$ and $T_\text{env}$. Its partials, by the chain rule:

$$\frac{\partial T}{\partial k} = -t\,(T_0 - T_\text{env})\,e^{-kt},\qquad \frac{\partial T}{\partial T_\text{env}} = 1 - e^{-kt}$$

Early on, $T$ barely depends on room temperature; after a long time, it depends on almost nothing else.

## Worked example

### 1. Total differential for a gas

1.00 mol of ideal gas at 298.15 K in 24.5 L. The temperature rises by 1.0 K and the volume by 0.10 L at the same time. Estimate the pressure change.

- $(\partial p/\partial T)_V\,dT = 339\ \mathrm{Pa/K} \times 1.0\ \mathrm{K} = +339$ Pa.
- $(\partial p/\partial V)_T\,dV = -4.13\times10^{6}\ \mathrm{Pa/m^3} \times 1.0\times10^{-4}\ \mathrm{m^3} = -413$ Pa.
- $dp \approx -74$ Pa.

Direct calculation, $p(299.15, 24.6) - p(298.15, 24.5)$, gives $-73$ Pa. The two effects nearly cancel; the total differential shows which one wins.

### 2. When can I drink my tea?

A mug fit gives $k = 6.7\times10^{-4}\ \mathrm{s^{-1}}$ (±5 %), $T_0 = 80.0$ °C, $T_\text{env} = 23.0$ °C (±1.0 °C). Time to reach 60 °C:

$$t^* = \frac{1}{k}\ln\frac{T_0 - T_\text{env}}{60 - T_\text{env}} = \frac{\ln(57.0/37.0)}{6.7\times10^{-4}} = 645\ \mathrm{s} = 10.7\ \mathrm{min}$$

Partials and error terms:

- $\partial t^*/\partial k = -t^*/k$, so the $k$ term is $t^* \times 0.05 = 32$ s.
- $\partial t^*/\partial T_\text{env} = \dfrac{1}{k}\left(\dfrac{1}{60 - T_\text{env}} - \dfrac{1}{T_0 - T_\text{env}}\right) = 14.2$ s/°C, so the room-temperature term is 14 s.
- Combined: $\sqrt{32^2 + 14^2} = 35$ s.

Answer: $10.7 \pm 0.6$ min. The cooling constant dominates. A better room thermometer would hardly help; a longer, cleaner cooling curve would.

## Hands-on

### Part A — pencil (20 min)

1. For $p = nRT/V$, write $(\partial p/\partial n)_{T,V}$ and evaluate it at 298.15 K, 24.5 L.
2. Show that $\partial^2 p/\partial n\,\partial T = \partial^2 p/\partial T\,\partial n$.
3. The density of a liquid is $\rho = m/V$, with $m = 24.95 \pm 0.02$ g and $V = 25.0 \pm 0.1$ mL. Find $\rho$ and its uncertainty with partial derivatives. Which input dominates?

<details><summary>Answers to Part A</summary>

1. $RT/V = 8.314 \times 298.15 / 0.0245 = 1.01\times10^{5}$ Pa/mol. Adding 0.01 mol raises $p$ by about 1 kPa.
2. Both orders give $R/V$.
3. $\rho = 0.998$ g/mL. $\partial\rho/\partial m = 1/V = 0.0400$ mL⁻¹, term $0.0400 \times 0.02 = 0.0008$ g/mL. $\partial\rho/\partial V = -m/V^2 = -0.0399$ g/mL², term $0.0399 \times 0.1 = 0.0040$ g/mL. Total $u_\rho = 0.004$ g/mL. The volume dominates by a factor of five. This is the calculus behind the significant-figure rule of [01.2](../module-01/lesson-02.md): the least precise input limits the result.

</details>

### Part B — module practical: your own cooling curve (about 100 min, most of it waiting)

> [!CAUTION]
> Hot water scalds. Use water from the kettle after it has stood for a minute, fill the mug no more than three-quarters, keep it on a stable table away from the edge, and keep children and pets away. Do not hold the thermometer probe in your hand over the mug; rest it in the water. No chemicals, only tap water.

What you need: a ceramic mug, a kitchen scale, a digital kitchen (probe) thermometer reading to 0.1 °C or 1 °C, a phone timer, a second thermometer or the same one for the room, Python with the course packages and the [Module 2 lab folder](../../labs/module-02/).

Steps:

1. Measure the room temperature away from windows and heaters. Write it down with its uncertainty (for example 22.5 ± 0.5 °C).
2. Weigh the empty mug, add about 250 g of hot water, weigh again. Record the water mass.
3. Put the probe in the middle of the water, not touching the side. Start the timer when the reading peaks.
4. Read the temperature every 60 s for at least 40 minutes. Do not stir, cover or move the mug.
5. Type the readings into a CSV with the header `t_s,T_C` (same format as `cooling_example.csv`).
6. Fill in the three TODO functions in `lesson05_cooling.py`, test them on the example data, then run on your data:

```bash
py lesson05_cooling.py
py lesson05_cooling.py my_curve.csv 22.5 0.252
```

The script uses every lesson: a log fit for $k$ (02.1), central differences for $dT/dt$ (02.2), an integral for the total change and the heat lost (02.3), the linear Taylor form at early times (02.4), and partial derivatives for the error budget (02.5).

How you know it worked: on the example data you get $k \approx 6.7\times10^{-4}\ \mathrm{s^{-1}}$ (time constant about 25 min) from both the log fit and the rate plot, the integral of $dT/dt$ equals $T_\text{end} - T_\text{start}$ (−45.8 °C), the heat lost is about 48 kJ, and the 60-minute prediction is about $28.2 \pm 1.1$ °C with the room-temperature term larger than the $k$ term. On a real mug expect a time constant of roughly 15–40 minutes, depending on the mug and the room.

<details><summary>Reference solution and what real data show</summary>

`fit_log`: drop readings within 0.5 °C of the room, then `np.polyfit(t, np.log(T - T_env), 1)`; $k = -$slope, $T_0 = T_\text{env} + e^{\text{intercept}}$. `cooling_rate`: `np.gradient(T, t)`. `sensitivities`: `-t*(T0 - T_env)*exp(-k*t)` and `1 - exp(-k*t)`. Full code: `lesson05_cooling_solution.py`.

On a real mug the first few minutes usually cool faster than the model, because evaporation from the hot surface and heat flowing into the cold mug wall add to plain convection. You see this as a log plot that curves downward at the start and a rate plot whose first points lie below the line. That is not a failed experiment: it shows the limit of a one-parameter model. Fit only the readings after the first five minutes and compare the two $k$ values. If your room temperature is uncertain by more than 1 °C, the 60-minute prediction becomes limited by $T_\text{env}$, exactly as the partial derivatives say.

Write it up with the [lab report template](../../templates/lab-report.md): aim, method, data table, both $k$ values, heat lost, error budget, and one paragraph on where Newton's law fails.

</details>

## Common mistakes

- Forgetting what is held constant. $(\partial p/\partial T)_V$ and $(\partial p/\partial T)_n$ at changing volume are different numbers. Always write the subscripts.
- Adding error terms directly when they are independent. Use the square root of the sum of squares; straight addition overstates the uncertainty.
- Dropping the sign of a partial when it matters. In the gas example the two terms nearly cancel; ignoring the minus sign gives +750 Pa instead of −74 Pa.
- Using room temperature from the thermostat setting. Measure it; it is a parameter of your model and the partials show it matters.
- Taking the log of $T - T_\text{env}$ when the excess is tiny or negative. Drop readings within about 0.5 °C of the room.

## Key takeaways

- A partial derivative changes one input and holds the rest fixed; write the fixed ones as subscripts.
- Mixed partials of a smooth function are equal, the root of the Maxwell relations.
- The total differential adds the separate effects of small changes: a multi-variable Taylor expansion.
- For independent uncertainties, combine the partial-derivative terms in quadrature; the largest term tells you what to improve.
- A cooling curve uses exponentials, derivatives, integrals, series and partials together: the whole calculus toolkit on one kitchen experiment.

## Sources

- [OpenStax Calculus Volume 3, 4.3 Partial Derivatives](https://openstax.org/books/calculus-volume-3/pages/4-3-partial-derivatives) — definitions, notation and mixed partials.
- [Levitus, Mathematical Methods in Chemistry (LibreTexts)](https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Mathematical_Methods_in_Chemistry_(Levitus)) — chapter 8 on calculus in more than one variable, with thermodynamic examples.
- [OpenStax Calculus Volume 1, 6.8 Exponential Growth and Decay](https://openstax.org/books/calculus-volume-1/pages/6-8-exponential-growth-and-decay) — Newton's law of cooling as an exponential model.
- [NIST Chemistry WebBook: Water](https://webbook.nist.gov/cgi/cbook.cgi?ID=C7732185&Mask=2) — heat capacity of liquid water.
- [MIT OCW 18.02SC Multivariable Calculus](https://ocw.mit.edu/courses/18-02sc-multivariable-calculus-fall-2010/) — the full course on partial derivatives.
