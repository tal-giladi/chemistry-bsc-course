---
id: "02.1"
module: 2
minutes: 20
practice_minutes: 40
prerequisites: ["01.2"]
objectives:
  - Convert between natural and base-10 logarithms and compute pH and [H+] in both directions.
  - Calculate a rate constant from a half-life and the time needed to reach a given fraction remaining.
  - Linearise the Arrhenius equation and read an activation energy from the slope of ln k against 1/T.
  - Choose which plot turns a power-law or exponential relationship into a straight line.
volatility: concept
sources:
  - title: "OpenStax Chemistry 2e, 12.5 Collision Theory (Arrhenius equation)"
    url: https://openstax.org/books/chemistry-2e/pages/12-5-collision-theory
  - title: "OpenStax Calculus Volume 1, 6.8 Exponential Growth and Decay"
    url: https://openstax.org/books/calculus-volume-1/pages/6-8-exponential-growth-and-decay
  - title: "NIST CODATA 2022: molar gas constant R"
    url: https://physics.nist.gov/cgi-bin/cuu/Value?r
  - title: "Kutschera (2019), The Half-Life of 14C: Why Is It So Long? Radiocarbon"
    url: https://www.cambridge.org/core/journals/radiocarbon/article/abs/halflife-of-14cwhy-is-it-so-long/40C969D635697E923338763B56402862
  - title: "MIT OpenCourseWare 18.01SC Single Variable Calculus"
    url: https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/
last_verified: "2026-10-16"
---

# 02.1 · Functions chemists meet: power, exponential and logarithm

Three kinds of function describe most of the numbers in chemistry: power laws, exponentials and logarithms. This lesson shows what each one looks like, where it turns up (gas laws, pH, radioactive decay, the Arrhenius equation), and the one trick that makes all of them easy to handle with data: take a logarithm and get a straight line.

## Why it matters

A colleague measures a reaction rate at five temperatures and asks: "How much faster will it run at body temperature?" A spreadsheet of numbers cannot answer that. The answer comes from knowing that rate constants follow an exponential in $1/T$, plotting $\ln k$ against $1/T$, and reading the slope. The same move tells you how old a piece of charcoal is from its carbon-14 content, or why a pH change of 1 means a tenfold change in acidity. If you can switch between a curve and its straight-line form, you can extract a physical constant from almost any data set.

## Core ideas

> [!NOTE]
> Everything in this lesson is stable mathematics. The only numbers that can change are measured constants: the gas constant $R$ is exact in SI since 2019 (CODATA 2022 value checked 2026-10-16), and the carbon-14 half-life used here is the 2019 recommended value.

### Power laws

A power law has the form $y = a\,x^n$. The exponent $n$ is fixed. Examples:

- Ideal gas at fixed $n$ and $T$: $p = (nRT)\,V^{-1}$, so $n = -1$. Double the volume and the pressure halves.
- A second-order rate law: rate $= k[\mathrm{A}]^2$. Double the concentration and the rate goes up four times.

Take the log of both sides: $\log y = \log a + n \log x$. A plot of $\log y$ against $\log x$ is a straight line with slope $n$. That is how kinetic orders are found from data.

### Exponentials

An exponential has the variable in the exponent: $y = y_0\,e^{-kt}$. Here $e \approx 2.71828$ and $k$ is a rate constant with units of 1/time. The key property: in every equal time step the quantity falls by the same factor. That is why exponentials describe first-order decay, radioactive decay and the cooling of a hot drink (lesson [02.5](lesson-05.md)).

The half-life $t_{1/2}$ is the time for $y$ to halve. Set $y = y_0/2$:

$$\tfrac{1}{2} = e^{-k t_{1/2}} \quad\Rightarrow\quad t_{1/2} = \frac{\ln 2}{k}$$

Tiny example: if $k = 0.0040\ \mathrm{s^{-1}}$, then $t_{1/2} = 0.693/0.0040 = 173\ \mathrm{s}$. After 173 s half is left; after 346 s a quarter.

### Logarithms

A logarithm undoes an exponential. The natural log $\ln$ undoes $e^x$; the base-10 log $\log_{10}$ undoes $10^x$. Rules you will use every week:

$$\ln(ab) = \ln a + \ln b,\qquad \ln(a/b) = \ln a - \ln b,\qquad \ln(a^n) = n\ln a$$

$$\ln x = \ln 10 \cdot \log_{10} x \approx 2.303\,\log_{10} x$$

Chemistry uses base 10 for pH: $\mathrm{pH} = -\log_{10}[\mathrm{H^+}]$, with $[\mathrm{H^+}]$ in mol/L divided by 1 mol/L so the log is of a pure number. You can only take the log of a dimensionless number. That is why the units always sit inside the bracket as a ratio.

### The Arrhenius equation

Rate constants depend on temperature as

$$k = A\,e^{-E_a/(RT)}$$

where $A$ is the pre-exponential factor (same units as $k$), $E_a$ is the activation energy in J/mol, $R = 8.314462618\ \mathrm{J\,mol^{-1}\,K^{-1}}$ (exact) and $T$ is in kelvin. Take $\ln$ of both sides:

$$\ln k = \ln A - \frac{E_a}{R}\cdot\frac{1}{T}$$

This is $y = b + m x$ with $y = \ln k$, $x = 1/T$, slope $m = -E_a/R$. Measure $k$ at several temperatures, plot, fit a line, multiply the slope by $-R$. For two temperatures only:

$$\ln\frac{k_2}{k_1} = \frac{E_a}{R}\left(\frac{1}{T_1} - \frac{1}{T_2}\right)$$

### Which plot straightens which law

| Relationship | Plot | Slope gives |
|---|---|---|
| $y = a x^n$ (power) | $\log y$ vs $\log x$ | $n$ |
| $y = y_0 e^{-kt}$ (exponential) | $\ln y$ vs $t$ | $-k$ |
| $k = A e^{-E_a/RT}$ (Arrhenius) | $\ln k$ vs $1/T$ | $-E_a/R$ |

## Worked example

### 1. pH both ways

A solution has $[\mathrm{H^+}] = 3.2\times10^{-4}$ mol/L. $\mathrm{pH} = -\log_{10}(3.2\times10^{-4}) = 3.49$. Going back: a pH of 4.76 means $[\mathrm{H^+}] = 10^{-4.76} = 1.7\times10^{-5}$ mol/L. A pH lower by 1 means ten times more $\mathrm{H^+}$.

Significant figures: the digits after the decimal point of a pH match the significant figures of the concentration. $3.2\times10^{-4}$ has two, so pH 3.49 has two decimals.

### 2. Carbon-14 age

The half-life of carbon-14 is $5700 \pm 30$ years. A piece of charcoal has 40.0 % of the carbon-14 of living wood. How old is it?

1. $k = \ln 2 / 5700\ \mathrm{y} = 1.216\times10^{-4}\ \mathrm{y^{-1}}$.
2. $0.400 = e^{-kt}$, so $t = \ln(1/0.400)/k = 0.9163 / 1.216\times10^{-4} = 7.53\times10^{3}$ years.

Sanity check: 40 % is between one half-life (50 %, 5700 y) and two (25 %, 11 400 y). 7 500 years fits.

### 3. Arrhenius between two temperatures

A reaction has $E_a = 50.0$ kJ/mol. How much faster is it at 35 °C than at 25 °C?

$$\ln\frac{k_2}{k_1} = \frac{50\,000}{8.314}\left(\frac{1}{298.15} - \frac{1}{308.15}\right) = 6014 \times 1.088\times10^{-4} = 0.655$$

$k_2/k_1 = e^{0.655} = 1.92$. A 10 K rise roughly doubles the rate, which is the old rule of thumb for $E_a$ near 50 kJ/mol.

## Hands-on

What you need: Python 3.14 with the course packages ([setup in labs/common](../../labs/common/requirements.txt)), the Module 2 lab folder ([labs/module-02](../../labs/module-02/)), pencil and paper. Time: about 40 minutes.

### Part A — pencil (15 min)

1. pH of $[\mathrm{H^+}] = 2.5\times10^{-3}$ mol/L?
2. $[\mathrm{H^+}]$ at pH 8.20?
3. A first-order reaction has $t_{1/2} = 12.0$ min. What fraction is left after 30.0 min?
4. Write $\ln x$ for $x = 1000$ using only $\ln 10 = 2.303$.

<details><summary>Answers to Part A</summary>

1. $-\log_{10}(2.5\times10^{-3}) = 2.60$.
2. $10^{-8.20} = 6.3\times10^{-9}$ mol/L.
3. $30/12 = 2.5$ half-lives, so $(1/2)^{2.5} = 0.177$, about 17.7 %.
4. $\ln 1000 = 3 \ln 10 = 6.908$.

</details>

### Part B — Python: Arrhenius from data (25 min)

The file `arrhenius_rates.csv` holds rate constants at eight temperatures from 25 °C to 60 °C. The data are generated from a known model with 3 % noise (see `make_data.py`), so you can check your answer.

1. Open `lesson01_arrhenius.py`. Fill in the three functions marked TODO: `linearise`, `fit_line`, `activation_energy`.
2. Run it from the lab folder:

```bash
py lesson01_arrhenius.py
```

3. Open `runs/lesson01_arrhenius.png`. The points should lie on a straight line falling to the right.

How you know it worked: you get $E_a$ between 100 and 107 kJ/mol (the model used 103 kJ/mol) and a predicted $k$ at 37 °C close to $1.8\times10^{-4}\ \mathrm{s^{-1}}$.

<details><summary>Reference solution</summary>

`linearise` returns `1/T, np.log(k)`. `fit_line` returns `np.polyfit(x, y, 1)`. `activation_energy` returns `-slope * R / 1000`. The fit gives slope about $-12\,455$ K, so $E_a = 12\,455 \times 8.314 / 1000 = 103.6$ kJ/mol and $A \approx 4.9\times10^{13}\ \mathrm{s^{-1}}$. The full file is `lesson01_arrhenius_solution.py`. The small gap from 103 kJ/mol is the 3 % noise: in lesson 05.3 (Module 5) you will learn to put an uncertainty on the slope.

</details>

## Common mistakes

- Using $\log_{10}$ where the formula needs $\ln$. Arrhenius and half-life formulas use $\ln$. If your $E_a$ comes out 2.3 times too small, you used `log10`. In numpy, `np.log` is the natural log.
- Plotting $\ln k$ against $T$ instead of $1/T$. The plot curves slightly and the slope has no meaning. Always convert to kelvin, then invert.
- Using Celsius in $1/T$. $1/25$ and $1/298.15$ are very different. Kelvin only.
- Dropping the minus sign. The slope is $-E_a/R$, so a falling line gives a positive $E_a$. A negative activation energy almost always means a sign slip.
- Mixing J and kJ. $R$ is in J/(mol K). Put $E_a$ in J/mol in the formula, then report it in kJ/mol.
- Taking the log of a quantity with units. Write $\ln(k / \mathrm{s^{-1}})$ on the axis label so the reader knows what was divided out.

## Key takeaways

- Power laws become straight on log–log axes; the slope is the exponent.
- Exponentials become straight on a ln–linear plot; the slope is $-k$, and $t_{1/2} = \ln 2/k$.
- $\ln x \approx 2.303 \log_{10} x$. pH is base 10; kinetics and thermodynamics are base $e$.
- Arrhenius: plot $\ln k$ against $1/T$ in kelvin; $E_a = -R \times$ slope.
- Only take logs of dimensionless numbers; divide by the unit first.

## Sources

- [OpenStax Chemistry 2e, 12.5 Collision Theory](https://openstax.org/books/chemistry-2e/pages/12-5-collision-theory) — Arrhenius equation and its linear form.
- [OpenStax Calculus Volume 1, 6.8 Exponential Growth and Decay](https://openstax.org/books/calculus-volume-1/pages/6-8-exponential-growth-and-decay) — exponential decay and half-life.
- [NIST CODATA 2022: molar gas constant](https://physics.nist.gov/cgi-bin/cuu/Value?r) — $R = 8.314462618\ \mathrm{J\,mol^{-1}\,K^{-1}}$, exact.
- [Kutschera (2019), Radiocarbon](https://www.cambridge.org/core/journals/radiocarbon/article/abs/halflife-of-14cwhy-is-it-so-long/40C969D635697E923338763B56402862) — carbon-14 half-life $5700 \pm 30$ years.
- [MIT OCW 18.01SC Single Variable Calculus](https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/) — full course for more depth on exponentials and logs.
