---
id: "03.3"
module: 3
minutes: 20
practice_minutes: 50
prerequisites: ["02.2", "02.3"]
objectives:
  - Solve the zero-, first- and second-order rate laws by separation of variables and state each half-life.
  - Identify the order of a reaction from data by testing which integrated rate law gives a straight line.
  - Integrate a rate law numerically with Euler's method and with solve_ivp, and show how the Euler error depends on the step size.
  - Solve a linear first-order equation with a constant source term and find its steady state.
volatility: concept
sources:
  - title: "OpenStax Chemistry 2e, 12.4 Integrated Rate Laws"
    url: https://openstax.org/books/chemistry-2e/pages/12-4-integrated-rate-laws
  - title: "OpenStax Calculus Volume 2, 4.3 Separable Equations"
    url: https://openstax.org/books/calculus-volume-2/pages/4-3-separable-equations
  - title: "SciPy v1.18 manual, scipy.integrate.solve_ivp"
    url: https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html
  - title: "MIT OpenCourseWare 18.03 Differential Equations (Miller and Mattuck, Spring 2010)"
    url: https://ocw.mit.edu/courses/18-03-differential-equations-spring-2010/
last_verified: "2026-10-16"
---

# 03.3 · First-order differential equations and rate laws

A rate law tells you how fast a concentration changes given the concentration now. That is a differential equation: an equation for a function that contains the function's own derivative. Solving it gives the concentration at every time. This lesson solves the three classic rate laws by hand, shows how to decide which one your data follow, and then solves the same equations on a computer, first with the simplest possible method and then with the one professionals use.

## Why it matters

A pharmaceutical stability lab measures the concentration of a drug in solution every week. The question is: "How long until 10 % has degraded?" To answer it you need the order of the degradation, a rate constant, and the integrated form of the rate law. Get the order wrong and the predicted shelf life can be off by months. Later, in kinetics (Module 22) and in every lab simulation, you will meet rate laws with no neat solution at all. Then the only way forward is numerical, and you must know how far to trust the numbers.

## Core ideas

> [!NOTE]
> The mathematics is stable. The code uses `scipy.integrate.solve_ivp` from SciPy 1.18 (default method RK45, default tolerances rtol = 1e-3 and atol = 1e-6), checked 2026-10-16. Those defaults are loose for small concentrations; the lab sets them explicitly.

### Rate laws are differential equations

In [02.2](../module-02/lesson-02.md) you met the rate of reaction as minus the slope of concentration against time. A rate law says what that slope depends on. For a reactant A with order $n$ and rate constant $k$:

$$\frac{dc}{dt} = -k\,c^n$$

An ordinary differential equation (ODE) is an equation like this, with one independent variable (time). It is first order because only the first derivative appears. A solution is a function $c(t)$ that makes it true for all $t$, and the initial condition $c(0) = c_0$ picks out one solution from a whole family.

### Separation of variables

If the right side is a product of a function of $c$ and a function of $t$, move everything with $c$ to one side and everything with $t$ to the other, then integrate both sides ([02.3](../module-02/lesson-03.md)):

$$\frac{dc}{c^n} = -k\,dt \quad\Rightarrow\quad \int_{c_0}^{c} \frac{dc'}{c'^n} = -k\int_0^t dt'$$

The three cases chemists need:

| Order | Integrated law | Straight-line plot | Half-life | Units of $k$ |
|---|---|---|---|---|
| 0 | $c = c_0 - kt$ | $c$ vs $t$, slope $-k$ | $c_0/(2k)$ | mol L⁻¹ s⁻¹ |
| 1 | $\ln c = \ln c_0 - kt$ | $\ln c$ vs $t$, slope $-k$ | $\ln 2/k$ | s⁻¹ |
| 2 | $1/c = 1/c_0 + kt$ | $1/c$ vs $t$, slope $+k$ | $1/(kc_0)$ | L mol⁻¹ s⁻¹ |

Notice that only the first-order half-life is independent of $c_0$. Measuring two half-lives in a row is a quick order test: if the second is twice as long as the first, the reaction is second order.

### Finding the order from data

Plot the data three ways: $c$, $\ln c$ and $1/c$ against $t$. The plot that is straight tells you the order, and its slope gives $k$. With noisy data, compare $R^2$ (the fraction of the variation a straight line explains) but also look at the residuals: a curved pattern of residuals is a stronger sign of the wrong order than a slightly lower $R^2$.

### Linear equations with a source term

Many systems have something flowing in as well as reacting away: a drug infused at a constant rate, a reactor fed with fresh reactant. Then

$$\frac{dc}{dt} = r - k\,c$$

with $r$ a constant input rate (mol L⁻¹ s⁻¹). At steady state nothing changes, $dc/dt = 0$, so $c_\text{ss} = r/k$. Separating variables with $u = c - c_\text{ss}$ gives $du/dt = -ku$, so

$$c(t) = c_\text{ss} + (c_0 - c_\text{ss})\,e^{-kt}$$

The approach to steady state is exponential, with the same time constant $1/k$ as plain decay. This is the same shape as Newton's cooling in [02.5](../module-02/lesson-05.md).

### Euler's method: the simplest numerical solver

When no formula exists, step forward in time. Euler's method uses the slope at the start of each step as if it stayed constant over the step of length $h$:

$$c_{i+1} = c_i + h\,f(t_i, c_i), \qquad f(t, c) = -k\,c^n$$

This is the forward difference of 02.2 run backwards. Its error at a fixed end time is proportional to $h$: halve the step, halve the error. That is called a first-order method. It is also unstable if the step is too big: for first-order decay, $hk > 2$ makes the numbers oscillate and grow.

### Professional solvers: solve_ivp

`scipy.integrate.solve_ivp` uses higher-order methods that combine several slope evaluations per step (the default RK45 is a Runge–Kutta method of order 5 with an order-4 error estimate). It also chooses the step size itself to meet the tolerances `rtol` (relative) and `atol` (absolute). For concentrations of $10^{-5}$ mol/L, the default `atol = 1e-6` is far too loose: set it a few orders below your smallest concentration. For stiff systems, where one process is thousands of times faster than another, use `method="LSODA"`, `"BDF"` or `"Radau"`.

Explore the first-order case interactively before the lab: change $k$ and $c_0$ and watch which quantities change the half-life.

[Simulation: Kinetics — first-order decay](../../simulations/kinetics/index.html?preset=first-order)

## Worked example

### 1. A second-order reaction

A reactant decays by $2\mathrm{A} \to$ products with rate law $dc/dt = -kc^2$, $k = 0.54$ L mol⁻¹ s⁻¹, $c_0 = 0.0100$ mol/L.

1. Half-life: $t_{1/2} = 1/(kc_0) = 1/(0.54 \times 0.0100) = 185$ s.
2. Concentration at 600 s: $1/c = 1/0.0100 + 0.54 \times 600 = 100 + 324 = 424$ L/mol, so $c = 2.36\times10^{-3}$ mol/L.
3. The next half-life (from 0.0050 to 0.0025 mol/L) is $1/(0.54 \times 0.0050) = 370$ s, twice the first. That doubling is the fingerprint of second order.

### 2. Two Euler steps by hand

First-order decay, $k = 0.0040\ \mathrm{s^{-1}}$, $c_0 = 0.100$ mol/L, step $h = 60$ s.

1. $c_1 = 0.100 + 60 \times (-0.0040 \times 0.100) = 0.100 \times (1 - 0.24) = 0.0760$ mol/L.
2. $c_2 = 0.0760 \times 0.76 = 0.0578$ mol/L at $t = 120$ s.
3. Exact: $0.100\,e^{-0.48} = 0.0619$ mol/L. Euler is 0.0041 mol/L (6.6 %) low, because it uses the steep slope at the start of each step for the whole step. Each step multiplies by $1 - hk$ instead of $e^{-hk}$; the Taylor series of 02.4 shows that these agree only when $hk$ is small.

## Hands-on

What you need: Python with the course packages and the [Module 3 lab folder](../../labs/module-03/). Time: about 50 minutes.

### Part A — pencil (15 min)

1. A first-order reaction has $k = 2.5\times10^{-3}\ \mathrm{s^{-1}}$. How long until 10 % has reacted?
2. A zero-order reaction (a catalyst surface that is saturated) has $k = 1.0\times10^{-4}$ mol L⁻¹ s⁻¹ and $c_0 = 0.050$ mol/L. When is A used up?
3. A drug is infused at $r = 2.0\ \mathrm{mg\,L^{-1}\,h^{-1}}$ and eliminated with $k = 0.25\ \mathrm{h^{-1}}$. What is the steady-state concentration, and how long until it reaches 90 % of it from zero?

<details><summary>Answers to Part A</summary>

1. $c/c_0 = 0.90$, so $t = \ln(1/0.90)/k = 0.1054/2.5\times10^{-3} = 42$ s.
2. $c = 0$ when $t = c_0/k = 500$ s. Zero-order reactions stop abruptly; exponentials never quite reach zero.
3. $c_\text{ss} = r/k = 8.0$ mg/L. $c/c_\text{ss} = 1 - e^{-kt} = 0.90$ gives $t = \ln 10/k = 9.2$ h.

</details>

### Part B — Python (35 min)

1. Open `lesson03_ode.py` and fill in `euler` and `order_fits`.
2. Run it:

```bash
py lesson03_ode.py
```

3. Look at `runs/lesson03_ode.png`: Euler with two step sizes against the exact curve, and the order test.

Part 1 runs Euler for the reaction of worked example 2 to 300 s with steps from 60 s down to 3.75 s. Part 2 runs `solve_ivp` with tight tolerances. Part 3 reads `order_test.csv` (21 concentrations over 20 minutes, generated from a known rate law with noise) and fits all three integrated laws.

How you know it worked: the Euler error at 300 s falls from about $4.8\times10^{-3}$ to $2.7\times10^{-4}$ mol/L and roughly halves each time $h$ halves (ratios near 2.0). `solve_ivp` hits the exact value 0.030119 mol/L to within $10^{-10}$ in about 16 steps. The order test gives $R^2$ about 0.73, 0.93 and 0.995 for orders 0, 1 and 2, so the data are second order with $k \approx 0.53$ L mol⁻¹ s⁻¹ (the model used 0.54).

<details><summary>Reference solution</summary>

`euler`: build `t` with `np.linspace(0, n*h, n+1)`, then loop `c[i+1] = c[i] + h*f(t[i], c[i], *args)`. `order_fits`: for each of `c`, `np.log(c)`, `1/c`, fit `np.polyfit(t, y, 1)` and compute $R^2 = 1 - \sum r^2 / \sum (y - \bar y)^2$. Full code: `lesson03_ode_solution.py`.

Why the second-order fit is not perfect: the noise is constant in $c$, so in $1/c$ it grows as $c$ falls; the last points scatter most. A weighted fit (Module 5) fixes this. Try `euler(rate_law, 0.100, 3000, 600, 0.0040, 1)`, a step with $hk = 2.4$, and watch the concentration go negative and swing ever wider: that is the instability.

</details>

## Common mistakes

- Using the first-order half-life for every reaction. $t_{1/2} = \ln 2/k$ only holds for first order; for second order it depends on $c_0$.
- Deciding the order from one plot. Always try all three; a curved $\ln c$ plot over a short time range can look straight.
- Getting the units of $k$ wrong. They change with order; check them before putting $k$ in a formula.
- Trusting Euler with a large step. Check by halving $h$: if the answer changes noticeably, the step was too big.
- Leaving `solve_ivp` at its default tolerances for small concentrations. `atol = 1e-6` mol/L is larger than a $10^{-5}$ mol/L signal's detail. Set `rtol` and `atol` explicitly.
- Forgetting the steady state in an equation with a source term. The exponential approaches $r/k$, not zero.

## Key takeaways

- A rate law $dc/dt = -kc^n$ is a first-order ODE; separation of variables solves orders 0, 1 and 2.
- The straight plot ($c$, $\ln c$ or $1/c$ against $t$) reveals the order; its slope gives $k$.
- Only first-order half-lives are constant; second-order half-lives double as $c$ halves.
- Euler's method is easy to write but its error is proportional to the step size; `solve_ivp` controls the error for you if you set sensible tolerances.
- With a constant input, $dc/dt = r - kc$ approaches the steady state $r/k$ exponentially.

## Sources

- [OpenStax Chemistry 2e, 12.4 Integrated Rate Laws](https://openstax.org/books/chemistry-2e/pages/12-4-integrated-rate-laws) — integrated laws and half-lives for orders 0, 1 and 2.
- [OpenStax Calculus Volume 2, 4.3 Separable Equations](https://openstax.org/books/calculus-volume-2/pages/4-3-separable-equations) — separation of variables, with mixing-tank and cooling examples.
- [SciPy v1.18 manual, solve_ivp](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html) — methods (RK45, LSODA, BDF, Radau) and default tolerances.
- [MIT OCW 18.03 Differential Equations](https://ocw.mit.edu/courses/18-03-differential-equations-spring-2010/) — the full course on first-order equations and numerical methods.
