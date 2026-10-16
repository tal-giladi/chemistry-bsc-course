---
id: "05.2"
module: 5
minutes: 20
practice_minutes: 45
prerequisites: ["05.1", "02.1", "02.3"]
objectives:
  - Replace a Python loop over data points with a numpy array expression and predict the shape of the result.
  - Use broadcasting to evaluate a formula on a grid of two variables, such as speed and temperature, in one line.
  - Integrate a sampled function with np.trapezoid and check the result against a closed-form value.
  - Produce a matplotlib figure with labelled axes and units, a legend, and a saved file.
volatility: implementation
sources:
  - title: "NumPy v2.5 manual, NumPy: the absolute basics for beginners"
    url: https://numpy.org/doc/stable/user/absolute_beginners.html
  - title: "NumPy 2.4.0 release notes (removal of numpy.trapz)"
    url: https://numpy.org/doc/stable/release/2.4.0-notes.html
  - title: "Matplotlib 3.11.2 documentation, Quick start guide"
    url: https://matplotlib.org/stable/users/explain/quick_start.html
  - title: "OpenStax University Physics Volume 2, 2.4 Distribution of Molecular Speeds"
    url: https://openstax.org/books/university-physics-volume-2/pages/2-4-distribution-of-molecular-speeds
  - title: "NIST CODATA 2022: atomic mass constant"
    url: https://physics.nist.gov/cgi-bin/cuu/Value?ukg
last_verified: "2026-10-16"
---

# 05.2 · Arrays, vectorised maths and plotting

Chemical data come as columns of numbers: absorbance at 500 wavelengths, temperature every second, a rate constant at ten temperatures. numpy treats a whole column as one object, an array, so a formula written once applies to every point at once. This lesson teaches arrays, vectorised maths and broadcasting, then shows how to make a clear, honest plot. The hands-on computes the speed distribution of nitrogen molecules at three temperatures.

## Why it matters

Suppose you need the Arrhenius rate constant ([02.1](../module-02/lesson-01.md)) at 300 temperatures for 4 candidate activation energies, or the absorbance of a dye at 600 wavelengths. Written as loops, such code is long, slow and easy to get wrong at the index level. Written as array expressions, it is one line that reads like the equation in the textbook, and it runs about 50 times faster or more. Every later lab in this course, from titration curves to NMR spectra, uses arrays this way. A plot then decides whether anyone, including you next month, can read the result.

## Core ideas

> [!NOTE]
> Arrays, broadcasting and plotting are stable ideas. Function names do change: checked against NumPy 2.5 and Matplotlib 3.11.2 on 2026-10-16, `np.trapz` no longer exists (removed in NumPy 2.4; use `np.trapezoid`). The constants are CODATA 2022 from NIST.

### Arrays

A numpy **array** is a grid of numbers of one type (usually 64-bit floats). Two attributes describe it:

- `shape`: the size along each axis. A spectrum of 500 points has shape `(500,)`; 3 spectra of 500 points have shape `(3, 500)`.
- `dtype`: the number type, such as `float64` or `int64`.

```python
import numpy as np
T = np.array([298.15, 308.15, 318.15])       # K, shape (3,)
v = np.linspace(0, 2500, 2501)               # 2501 points from 0 to 2500, both ends included
x = np.arange(0, 1, 0.1)                      # step 0.1, end excluded: 0.0 ... 0.9
```

Prefer `linspace` when you know the end points. `arange` with a float step can give one point more or less than you expect, because of float rounding ([05.1](lesson-01.md)).

### Vectorised maths

Arithmetic and numpy functions act element by element. This is called **vectorisation**:

```python
k = 1e13 * np.exp(-50e3 / (8.314 * T))        # Arrhenius at all three temperatures at once
```

No loop, no index, and the code matches the equation. Use `np.exp`, `np.log`, `np.sqrt` (not the `math` versions, which accept only single numbers). Remember from [02.1](../module-02/lesson-01.md): `np.log` is the natural log, `np.log10` the base-10 log.

### Boolean masks

A comparison gives an array of `True`/`False`, a **mask**, that selects points:

```python
fast = v > 1000                # mask, shape (2501,)
v[fast]                        # only the speeds above 1000 m/s
np.where(v > 1000, f, 0.0)     # keep f where the mask is True, else 0
```

### Broadcasting

**Broadcasting** is numpy's rule for combining arrays of different shapes. Shapes are compared from the right; two sizes are compatible when they are equal or one of them is 1, and a size-1 axis is stretched to match. So a row `(2501,)` and a column `(3, 1)` combine into a grid `(3, 2501)`:

```python
T = np.array([200.0, 298.15, 500.0])[:, None]   # shape (3, 1): a column
f = formula(v, T)                               # v (2501,) with T (3, 1) -> (3, 2501)
```

`[:, None]` adds an axis of length 1. Each row of the result is one temperature, each column one speed. If the shapes do not fit, for example `(3,)` with `(2501,)`, numpy raises a `ValueError` rather than guessing.

### Integrating sampled data

The trapezoid rule from [02.3](../module-02/lesson-03.md) is one call: `np.trapezoid(y, x, axis=-1)` integrates along the last axis, so a `(3, 2501)` array gives 3 integrals at once.

### Plotting that others can read

Matplotlib's documentation recommends the explicit style: make a figure and axes, then call methods on the axes.

```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6.4, 3.8))
ax.plot(v, f[1], label="298 K")
ax.set_xlabel("speed $v$ (m/s)")
ax.set_ylabel("$f(v)$ (s/m)")
ax.legend()
fig.savefig("speeds.png", dpi=120)
```

Rules that make a plot honest: every axis has a quantity and a unit; measured data are points, models are lines; several curves have a legend; the file is saved by the script, not copied by hand from a window. Scripts in this course call `matplotlib.use("Agg")` so they save files without needing a screen.

## Worked example

### 1. A grid of Arrhenius ratios with broadcasting

How much faster does a reaction run at 308.15 K and 318.15 K than at 298.15 K, for $E_a = 50$ and $80$ kJ/mol? The ratio is

$$\frac{k(T)}{k(298.15)} = \exp\left[\frac{E_a}{R}\left(\frac{1}{298.15} - \frac{1}{T}\right)\right]$$

```python
R = 8.314462618                                  # J mol^-1 K^-1
T = np.array([298.15, 308.15, 318.15])           # (3,)
Ea = np.array([50e3, 80e3])[:, None]             # (2, 1)
k = np.exp(-Ea / (R * T))                        # (2, 3); A cancels in the ratio
ratio = k / k[:, :1]                             # divide each row by its first column
```

Result: `[[1, 1.924, 3.554], [1, 2.850, 7.604]]`. A 10 K rise roughly doubles the rate at 50 kJ/mol and nearly triples it at 80 kJ/mol. One line covered six cases; adding a third activation energy changes nothing in the code.

### 2. Most probable and mean speed of N₂ at 298.15 K

The Maxwell–Boltzmann speed distribution gives the fraction of gas molecules with speeds near $v$:

$$f(v) = 4\pi\left(\frac{m}{2\pi k_B T}\right)^{3/2} v^2\, e^{-m v^2/(2 k_B T)}$$

For N₂, $m = 2 \times 14.007 \times 1.66053906892\times10^{-27}\ \mathrm{kg} = 4.6518\times10^{-26}$ kg, and $k_B = 1.380649\times10^{-23}$ J/K (exact). The peak and the mean have closed forms:

$$v_\text{mp} = \sqrt{\frac{2k_BT}{m}} = 420.7\ \mathrm{m/s},\qquad \bar v = \sqrt{\frac{8k_BT}{\pi m}} = 474.7\ \mathrm{m/s}$$

The mean is above the peak because the distribution has a long tail toward high speeds. In the hands-on you get the same two numbers numerically, from `argmax` and from $\bar v = \int v f(v)\,dv$, which tests that your array code is right.

## Hands-on

What you need: your course environment from [05.1](lesson-01.md) and `labs/module-05/lesson02_maxwell.py`. Time: about 45 minutes.

Open the file and fill in three functions:

1. `mb_pdf(v, T)`: the formula above with array operations only, so it works for a row of speeds and a column of temperatures.
2. `mean_speed(v, f)`: $\int v f\,dv$ with `np.trapezoid(..., axis=-1)`.
3. `fraction_above(v, f, v_cut)`: the fraction of molecules faster than `v_cut`, using `np.where` and `np.trapezoid`.

Run it from the lab folder:

```bash
..\..\.venv\Scripts\python lesson02_maxwell.py
```

How you know it worked:

- The shapes line reads `v (2501,)`, `T (3, 1)`, `f (3, 2501)`.
- The area under every curve is `1.00000`: the distribution is normalised.
- Mean speeds 388.8, 474.7 and 614.7 m/s at 200, 298.15 and 500 K, equal to the formula to 0.1 m/s.
- The fraction faster than 1000 m/s rises from 0.0008 at 200 K to 0.0102 at 298 K and 0.0805 at 500 K, a factor of about 100.
- The loop version is roughly 50 times slower than your vectorised one, or more (the exact factor depends on your computer).
- `runs/lesson02_maxwell.png` shows three curves; the hotter ones are lower, wider and shifted right.

Then answer in your notebook: why does a factor of 2.5 in temperature change the fast fraction by a factor of 100? (Hint: look at the exponent.) This is the same reason a small temperature rise speeds up reactions so much, and Module 22 returns to it.

<details><summary>Reference solution</summary>

```python
def mb_pdf(v, T, m=M_N2):
    a = m / (2 * K_B * T)
    return 4 * np.pi * (a / np.pi) ** 1.5 * v**2 * np.exp(-a * v**2)

def mean_speed(v, f):
    return np.trapezoid(v * f, v, axis=-1)

def fraction_above(v, f, v_cut):
    return np.trapezoid(np.where(v > v_cut, f, 0.0), v, axis=-1)
```

$(a/\pi)^{3/2}$ equals $(m/(2\pi k_B T))^{3/2}$. The fast fraction is controlled by $e^{-mv^2/(2k_BT)}$: at $v = 1000$ m/s the exponent is $-8.4$ at 200 K but $-3.4$ at 500 K, so the exponential alone grows by $e^{5} \approx 150$; the $T^{-3/2}$ prefactor and the shape of the tail bring the net factor to about 100. Full code: `labs/module-05/lesson02_maxwell_solution.py`.

</details>

## Common mistakes

- Using `math.exp` on an array. It raises `TypeError: only 0-dimensional arrays can be converted to Python scalars`. Use `np.exp`.
- Shapes that do not broadcast. `(3,)` with `(2501,)` fails; make one of them a column with `[:, None]`. Print `.shape` whenever you are unsure.
- Integrating along the wrong axis. For a `(3, 2501)` array, `axis=0` adds across temperatures, which is meaningless. Integrate along the axis that holds the `x` values.
- Copying `np.trapz` from an old tutorial. It is gone; use `np.trapezoid`.
- Axes without units, or a model drawn as dots and data as a smooth line. A reader then cannot tell measurement from theory.
- Forgetting that `arange(0, 1, 0.1)` excludes the end point. Use `linspace` when both ends matter.

## Key takeaways

- An array is one object with a shape; vectorised expressions apply a formula to every element and read like the equation.
- Broadcasting combines a row and a column into a grid; it is how one line covers many temperatures or concentrations.
- `np.trapezoid(..., axis=-1)` integrates many sampled curves at once; check it against a closed form when one exists.
- Use the explicit `fig, ax` style; every axis needs a quantity and a unit, and the script saves the figure.
- The fast tail of the Maxwell–Boltzmann distribution grows exponentially with temperature.

## Sources

- [NumPy: the absolute basics for beginners (NumPy 2.5)](https://numpy.org/doc/stable/user/absolute_beginners.html) — arrays, shapes, indexing and broadcasting.
- [NumPy 2.4.0 release notes](https://numpy.org/doc/stable/release/2.4.0-notes.html) — removal of `numpy.trapz` (deprecated since 2.0).
- [Matplotlib quick start guide (3.11.2)](https://matplotlib.org/stable/users/explain/quick_start.html) — the explicit figure and axes style.
- [OpenStax University Physics Volume 2, 2.4](https://openstax.org/books/university-physics-volume-2/pages/2-4-distribution-of-molecular-speeds) — the Maxwell–Boltzmann distribution and its characteristic speeds.
- [NIST CODATA 2022: atomic mass constant](https://physics.nist.gov/cgi-bin/cuu/Value?ukg) — $m_u$ used for the N₂ mass.
