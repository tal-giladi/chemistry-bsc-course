---
id: "02.4"
module: 2
minutes: 20
practice_minutes: 35
prerequisites: ["02.1", "02.2"]
objectives:
  - Write the first two or three Taylor terms of exp, ln(1 + x), (1 + x)^n and sqrt(1 + x) and estimate the error of stopping there.
  - Apply the small-x approximation to a weak-acid equilibrium and check it with the 5 % rule.
  - Decide from Ka and concentration whether the approximation is safe or the quadratic must be solved.
  - Explain why a smooth potential near its minimum behaves like a spring.
volatility: concept
sources:
  - title: "OpenStax Calculus Volume 2, 6.3 Taylor and Maclaurin Series"
    url: https://openstax.org/books/calculus-volume-2/pages/6-3-taylor-and-maclaurin-series
  - title: "OpenStax Chemistry 2e, 14.3 Relative Strengths of Acids and Bases"
    url: https://openstax.org/books/chemistry-2e/pages/14-3-relative-strengths-of-acids-and-bases
  - title: "Levitus, Mathematical Methods in Chemistry (LibreTexts), chapter 3 Series"
    url: https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Mathematical_Methods_in_Chemistry_(Levitus)
  - title: "MIT OpenCourseWare 18.01SC Single Variable Calculus"
    url: https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/
last_verified: "2026-10-16"
---

# 02.4 · Series and approximations

Chemists approximate all the time: "x is small compared with 0.1 M", "the potential is harmonic near the bottom", "at short times the product grows linearly". Each of these is a Taylor series cut after one or two terms. This lesson shows where those shortcuts come from, how big their error is, and how to check them, using the weak-acid equilibrium as the main example.

## Why it matters

You calculate the pH of an acetic acid solution with the shortcut $[\mathrm{H^+}] = \sqrt{K_a C}$ and get 4.37 for a $1.0\times10^{-4}$ M solution. The real value is 4.46. In an analytical method validation that error of 0.09 pH units is a failure. The shortcut was not wrong; it was used outside its range. A Taylor series tells you exactly what the range is, so you know when to trust the quick answer and when to solve the full equation.

## Core ideas

> [!NOTE]
> Series expansions are stable mathematics. The acetic acid $K_a = 1.8\times10^{-5}$ is the textbook value at 25 °C from OpenStax Chemistry 2e, checked 2026-10-16. Other tables give values from 1.74 to $1.8\times10^{-5}$.

### A function near a point looks like a polynomial

Any smooth function can be written near a point $a$ as

$$f(x) = f(a) + f'(a)(x - a) + \frac{f''(a)}{2!}(x - a)^2 + \frac{f'''(a)}{3!}(x - a)^3 + \dots$$

This is the Taylor series. Around $a = 0$ it is called a Maclaurin series. Keep one term: the value. Keep two: the tangent line (lesson [02.2](lesson-02.md)). Keep three: a parabola that also matches the curvature.

The size of the first term you drop is a good estimate of the error.

### Four expansions to know by heart

For small $x$ (say $|x| < 0.1$):

| Function | Series | Two-term error |
|---|---|---|
| $e^{x}$ | $1 + x + x^2/2 + \dots$ | about $x^2/2$ |
| $\ln(1 + x)$ | $x - x^2/2 + x^3/3 - \dots$ | about $x^2/2$ |
| $(1 + x)^n$ | $1 + nx + n(n-1)x^2/2 + \dots$ | about $n(n-1)x^2/2$ |
| $\sqrt{1 + x}$ | $1 + x/2 - x^2/8 + \dots$ | about $x^2/8$ |

Tiny check: $e^{0.05} = 1.05127$; the two-term value is 1.05000. The error 0.00127 is close to $x^2/2 = 0.00125$.

### Short-time kinetics

The fraction of a first-order reactant used up is $1 - e^{-kt}$. For small $kt$, $e^{-kt} \approx 1 - kt$, so

$$1 - e^{-kt} \approx kt$$

The product grows linearly at the start. That is why the initial-rate method works: in the first few percent of a reaction, a straight line fits. With $k = 0.0040\ \mathrm{s^{-1}}$ and $t = 10$ s: exact 0.0392, linear 0.0400, 2 % off.

### The small-x approximation for a weak acid

For a weak acid HA at formal concentration $C$ (the amount dissolved per litre) with $x = [\mathrm{H^+}]$:

$$K_a = \frac{x^2}{C - x} \quad\Rightarrow\quad x^2 + K_a x - K_a C = 0$$

If $x \ll C$, replace $C - x$ by $C$: $x \approx \sqrt{K_a C}$. How good is that? Solve the quadratic exactly and expand the square root with $\sqrt{1 + u} \approx 1 + u/2$:

$$x = \frac{-K_a + \sqrt{K_a^2 + 4K_aC}}{2} \approx \sqrt{K_aC} - \frac{K_a}{2}$$

So the relative error of the shortcut is about

$$\frac{K_a/2}{\sqrt{K_aC}} = \frac{1}{2}\sqrt{\frac{K_a}{C}}$$

The usual "5 % rule" says: accept the shortcut if $x/C < 0.05$. Since $x/C \approx \sqrt{K_a/C}$, that means $C/K_a > 400$, and the error in $[\mathrm{H^+}]$ is then below 2.5 %, about 0.01 pH units.

### Potentials near a minimum

A bond's potential energy $V(r)$ has a minimum at the bond length $r_e$, so $V'(r_e) = 0$. Taylor to second order:

$$V(r) \approx V(r_e) + \tfrac{1}{2}V''(r_e)\,(r - r_e)^2$$

That is Hooke's law with spring constant $k = V''(r_e)$. Every vibrational spectrum you will analyse (Modules 4, 14, 20) starts from this harmonic approximation; the dropped cubic term is what makes real bonds anharmonic.

## Worked example

### 1. Acetic acid at 0.100 M

$K_a = 1.8\times10^{-5}$, $C = 0.100$ M.

1. Shortcut: $x = \sqrt{1.8\times10^{-6}} = 1.342\times10^{-3}$ M, pH 2.87.
2. Check: $x/C = 1.3\,\% < 5\,\%$. Accept.
3. Exact quadratic: $x = 1.333\times10^{-3}$ M, pH 2.88. The difference, 0.7 %, matches $\tfrac12\sqrt{K_a/C} = 0.67\,\%$.

### 2. Acetic acid at $1.0\times10^{-4}$ M

1. Shortcut: $x = \sqrt{1.8\times10^{-9}} = 4.24\times10^{-5}$ M, pH 4.37.
2. Check: $x/C = 42\,\%$. Far above 5 %. Reject.
3. Exact: $x = \big(-1.8\times10^{-5} + \sqrt{(1.8\times10^{-5})^2 + 4(1.8\times10^{-5})(1.0\times10^{-4})}\big)/2 = 3.44\times10^{-5}$ M, pH 4.46.

The shortcut overestimates $[\mathrm{H^+}]$ by 23 %. At this dilution about a third of the acid is ionised, so "x is small" is simply false. (At even lower concentrations you would also need to include water's own $\mathrm{H^+}$; that comes in Module 8.)

## Hands-on

What you need: Python with the course packages, the [Module 2 lab folder](../../labs/module-02/), a calculator, 35 minutes.

### Part A — pencil (15 min)

1. Use $\ln(1 + x) \approx x$ to estimate $\ln 1.02$. What is the error, roughly?
2. Use $(1 + x)^{-1} \approx 1 - x$ to estimate $1/1.03$.
3. Formic acid has $K_a = 1.8\times10^{-4}$. At $C = 0.010$ M, is the small-x shortcut safe by the 5 % rule?

<details><summary>Answers to Part A</summary>

1. $\ln 1.02 \approx 0.0200$. The exact value is 0.01980; the error is about $x^2/2 = 0.0002$.
2. $1/1.03 \approx 0.97$; exact 0.97087. Error about $x^2 = 0.0009$.
3. $\sqrt{K_a C} = \sqrt{1.8\times10^{-6}} = 1.34\times10^{-3}$ M, so $x/C = 13\,\%$. Not safe; $C/K_a = 56$, far below 400. Solve the quadratic: $x = 1.25\times10^{-3}$ M.

</details>

### Part B — Python: map where the shortcut fails (20 min)

1. Open `lesson04_small_x.py` and fill in `x_exact` (the quadratic root) and `x_small` (the shortcut).
2. Run:

```bash
py lesson04_small_x.py
```

3. Open `runs/lesson04_small_x.png`. Both curves rise as the solution gets more dilute.

How you know it worked: the printed table shows an error of +0.7 % at 0.1 M and about +23 % at $10^{-4}$ M, and the script reports that $x/C$ drops below 5 % above roughly $7\times10^{-3}$ M, which is $C/K_a$ near 400.

<details><summary>Reference solution</summary>

`x_exact`: `(-Ka + np.sqrt(Ka**2 + 4*Ka*C)) / 2`. `x_small`: `np.sqrt(Ka*C)`. Table (rounded): 1 M +0.2 %, 0.1 M +0.7 %, 0.01 M +2.2 %, $10^{-3}$ M +6.9 %, $10^{-4}$ M +23 %. The pH error stays below 0.01 down to 0.01 M. Full file: `lesson04_small_x_solution.py`.

</details>

## Common mistakes

- Using the shortcut without the check. Always compute $x/C$ afterwards; it costs one division.
- Checking against the wrong quantity. Compare $x$ with $C$, not with $K_a$.
- Expanding around the wrong point. $\ln x \approx x$ is wrong; it is $\ln(1 + x) \approx x$ for small $x$.
- Keeping too few terms when $x$ is not small. At $x = 0.5$, $e^x \approx 1 + x$ is 9 % off.
- Taking the negative root of the quadratic. A negative $[\mathrm{H^+}]$ means you picked the wrong sign.

## Key takeaways

- A Taylor series turns a function into a polynomial near a point; the first dropped term estimates the error.
- Know $e^x$, $\ln(1+x)$, $(1+x)^n$ and $\sqrt{1+x}$ to two terms.
- Small-x for a weak acid: $x \approx \sqrt{K_a C}$, error about $\tfrac12\sqrt{K_a/C}$; safe when $C/K_a > 400$.
- Early in a first-order reaction, conversion grows linearly: $1 - e^{-kt} \approx kt$.
- Near a minimum every smooth potential is a parabola: the harmonic approximation.

## Sources

- [OpenStax Calculus Volume 2, 6.3 Taylor and Maclaurin Series](https://openstax.org/books/calculus-volume-2/pages/6-3-taylor-and-maclaurin-series) — derivation and error of Taylor polynomials.
- [OpenStax Chemistry 2e, 14.3 Relative Strengths of Acids and Bases](https://openstax.org/books/chemistry-2e/pages/14-3-relative-strengths-of-acids-and-bases) — acetic acid $K_a$ and the 5 % check in worked examples.
- [Levitus, Mathematical Methods in Chemistry (LibreTexts)](https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Mathematical_Methods_in_Chemistry_(Levitus)) — chapter 3 on series, written for chemistry students.
- [MIT OCW 18.01SC Single Variable Calculus](https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/) — the full treatment of approximations and series.
