---
id: "05.3"
module: 5
minutes: 25
practice_minutes: 60
prerequisites: ["05.2", "01.5", "02.5"]
objectives:
  - Fit a straight calibration line with curve_fit and report slope and intercept with standard uncertainties read from the covariance matrix.
  - Predict an unknown concentration from a calibration line with its uncertainty, keeping the slope–intercept correlation.
  - Choose between absolute_sigma=True and False and run a weighted nonlinear fit when each point has its own known uncertainty.
  - Judge a fit by its residual plot and reduced chi-square instead of by R² alone.
volatility: concept
sources:
  - title: "SciPy v1.18 manual, scipy.optimize.curve_fit"
    url: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html
  - title: "Harvey, Analytical Chemistry 2.1 (LibreTexts), 5.4 Linear Regression and Calibration Curves"
    url: https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_(Harvey)/05%3A_Standardizing_Analytical_Methods/5.04%3A_Linear_Regression_and_Calibration_Curves
  - title: "NIST/SEMATECH e-Handbook of Statistical Methods, 4.4.4 How can I tell if a model fits my data?"
    url: https://www.itl.nist.gov/div898/handbook/pmd/section4/pmd44.htm
  - title: "uncertainties package documentation"
    url: https://uncertainties.readthedocs.io/en/latest/
  - title: "lmfit 1.3.4 on PyPI (links to the documentation)"
    url: https://pypi.org/project/lmfit/1.3.4/
last_verified: "2026-10-16"
---

# 05.3 · Fitting models to data with uncertainty

A fit turns noisy measurements into the numbers a chemist reports: a slope that is a molar absorptivity, a rate constant, a concentration. A fit without an uncertainty is only half a result. This lesson shows how to fit a straight line and a nonlinear model with scipy, read the uncertainties from the covariance matrix, carry them into a prediction, and check whether the model actually describes the data. The hands-on is the task from the original degree plan: fit a straight line to data and report the error.

## Why it matters

A quality lab measures the dye in a soft drink against a calibration line and reports 3.70 µmol/L. Is an in-house limit of 3.80 exceeded or not? With an uncertainty of ±0.03 the answer is a clear no; with ±0.15 nobody can say. The uncertainty decides the action, and it comes from the fit. Two common errors make it wrong: ignoring that the slope and intercept are correlated (the uncertainty comes out too large), and fitting points that have very different noise as if they were equal (the quoted uncertainty comes out too small, and the value scatters more than it should). Both are easy to avoid with the right two lines of code.

## Core ideas

> [!NOTE]
> Least squares, covariance and residual analysis are stable statistics. Function names and defaults are from SciPy 1.18, uncertainties 3.2.3 and lmfit 1.3.4, checked on 2026-10-16. The uncertainties package has announced a version 4.0 that will remove some functions; the course pins 3.2.3.

### Least squares

A **model** is a formula with unknown **parameters**, such as $A = m\,c + b$. The **residual** of a point is measured minus model: $r_i = y_i - f(x_i)$. **Least squares** chooses the parameters that make the sum of squared residuals as small as possible. When each point has a known standard uncertainty $\sigma_i$, each residual is divided by it first, which gives the quantity called **chi-square**:

$$\chi^2 = \sum_i \left(\frac{y_i - f(x_i)}{\sigma_i}\right)^2$$

Noisy points then count less. That is a **weighted** fit.

### The covariance matrix

`popt, pcov = curve_fit(f, x, y)` returns the best parameters and their **covariance matrix**. The diagonal holds the variances, so the standard uncertainties are `np.sqrt(np.diag(pcov))`. The off-diagonal element tells you how the parameters move together. For a calibration line with all standards at positive concentration, slope and intercept are negatively correlated: a slightly steeper line must start slightly lower to pass through the same points. The correlation coefficient is $r = \mathrm{cov}(m,b)/(u_m u_b)$; in the worked example it is −0.78.

### absolute_sigma: who sets the scale?

- `absolute_sigma=False` (the default): the `sigma` values, if you give any, are only relative weights. SciPy rescales the covariance so that the reduced chi-square equals 1. In effect the scatter of your residuals sets the uncertainty. Use it when you do not know the noise level, as for a calibration line with single readings.
- `absolute_sigma=True`: your `sigma` values are real standard uncertainties in the units of $y$. Use it when the instrument or your repeats tell you the noise of each point.

### Is the model right? Residuals and reduced chi-square

$R^2$ near 1 is not proof of a good fit; the NIST/SEMATECH handbook stresses this. Look at the **residual plot** (residual against $x$). A good model leaves random scatter around zero. A curve, a trend or a funnel shape means the model is wrong or the weights are. With known $\sigma_i$, compute the **reduced chi-square**, $\chi^2_\nu = \chi^2/(N - p)$ for $N$ points and $p$ parameters. A value near 1 means the residuals match the stated noise. For about 20 degrees of freedom, values between roughly 0.5 and 1.5 are normal; 3 or more means a wrong model or underestimated errors.

### Carrying the uncertainty into a prediction

The `uncertainties` package does first-order error propagation ([02.5](../module-02/lesson-05.md)) automatically. `correlated_values(popt, pcov)` turns the fitted parameters into numbers that remember their correlation; any formula you then write with them carries the correct uncertainty. **lmfit** wraps the same least-squares engine in a friendlier interface with named parameters, bounds and a printed report; it gives the same answer.

## Worked example

### A dye calibration and an unknown

Six standards of a blue dye were read at 630 nm in a 1.00 cm cell (`calibration_dye.csv`, simulated):

| $c$ (µmol/L) | 0 | 1 | 2 | 4 | 6 | 8 |
|---|---|---|---|---|---|---|
| $A_{630}$ | 0.0008 | 0.1100 | 0.2064 | 0.4296 | 0.6366 | 0.8428 |

The unknown was read three times: 0.3913, 0.3937, 0.3914 (mean 0.39213).

1. Fit: slope $m = 0.10551 \pm 0.00071$ L/µmol, intercept $b = 0.0018 \pm 0.0032$, correlation −0.78. The residual standard deviation is $s_r = \sqrt{\sum r_i^2/(n-2)} = 0.0049$.
2. Concentration: $c = (0.39213 - 0.0018)/0.10551 = 3.700$ µmol/L.
3. Uncertainty, with the textbook formula (Harvey, eq. 5.12), $k = 3$ readings, $n = 6$ standards, mean standard signal 0.37103, $\sum (c_i - \bar c)^2 = 47.5$:

$$s_c = \frac{s_r}{m}\sqrt{\frac{1}{k} + \frac{1}{n} + \frac{(\bar A_\text{unk} - \bar A_\text{std})^2}{m^2 \sum (c_i - \bar c)^2}} = \frac{0.0049}{0.1055}\sqrt{0.333 + 0.167 + 0.0008} = 0.033\ \mathrm{\mu mol/L}$$

4. The same in Python, in three lines:

```python
from uncertainties import correlated_values, ufloat
m, b = correlated_values(popt, pcov)
c = (ufloat(A_unk.mean(), s_r / 3**0.5) - b) / m      # 3.700+/-0.033
```

Result: $c = 3.700 \pm 0.033$ µmol/L, the same as the formula. If you instead treat $m$ and $b$ as independent, you get ±0.047, about 40 % too large, because you count the same "steeper but lower" freedom twice. Notice also that the largest term under the root is $1/k$: reading the unknown more often would help more than adding standards.

## Hands-on

What you need: your environment from [05.1](lesson-01.md), `labs/module-05/lesson03_fitting.py`, `calibration_dye.csv` and `dye_fading.csv`. Time: about 60 minutes.

Fill in three functions:

1. `fit_line(x, y)`: an unweighted `curve_fit` of a straight line; return the parameters, covariance and $s_r$.
2. `predict_unknown(popt, pcov, A_unk, s_r)`: the unknown concentration as a `ufloat`, with `correlated_values`.
3. `fit_decay(t, A, sigma)`: a weighted fit of $A(t) = A_0 e^{-kt} + C$ to the fading data with `sigma=sigma, absolute_sigma=True`, plus the reduced chi-square.

```bash
..\..\.venv\Scripts\python lesson03_fitting.py
```

How you know it worked:

- Part 1 prints $m = 0.10551 \pm 0.00071$, $b = 0.0018 \pm 0.0032$, correlation −0.78, and `linregress` agrees to every digit. The unknown is $3.700 \pm 0.033$ µmol/L, matching the textbook formula; ignoring the correlation gives ±0.047.
- Part 2 prints $k = 0.02354 \pm 0.00062$ min⁻¹ (half-life 29.4 min) with reduced chi-square 0.69, normal for 22 degrees of freedom. The model value used to make the data, 0.02300, is within one uncertainty.
- The Monte Carlo check, 500 simulated repeats of the experiment, shows the weighted $k$ really scatters by about 0.0006, as quoted. The unweighted fit scatters by about 0.0010 but quotes only 0.0004.
- lmfit (Part 3) gives the same $k$ and uncertainty as your weighted `curve_fit`.
- `runs/lesson03_fitting.png` shows both fits with residual panels; the normalised residuals scatter between about −2 and +2 with no pattern.

Finally, apply the original plan's task to your own numbers: refit your sugar-solution densities from [01.5](../module-01/lesson-05.md) as density against sugar percentage and report slope ± uncertainty. Write the result on a page made from the [error-analysis template](../../templates/error-analysis.md).

<details><summary>Reference solution</summary>

```python
def fit_line(x, y):
    popt, pcov = curve_fit(line, x, y)
    resid = y - line(x, *popt)
    return popt, pcov, np.sqrt(np.sum(resid**2) / (x.size - 2))

def predict_unknown(popt, pcov, A_unk, s_r):
    m, b = correlated_values(popt, pcov)
    return (ufloat(np.mean(A_unk), s_r / np.sqrt(len(A_unk))) - b) / m

def fit_decay(t, A, sigma):
    popt, pcov = curve_fit(decay, t, A, p0=[A[0] - A[-1], 0.02, A[-1]],
                           sigma=sigma, absolute_sigma=True)
    chi2 = np.sum(((A - decay(t, *popt)) / sigma) ** 2)
    return popt, pcov, chi2 / (t.size - 3)
```

Why the unweighted fit misleads: the early points have about six times the noise of the late ones (their `sigma_A` is 0.026 against 0.004). Without weights they pull the curve as hard as the precise points, so $k$ scatters more. Then the default `absolute_sigma=False` estimates one average noise level from all residuals, which is too small for the noisy points that control $k$, so the quoted error is too small as well. Full code: `labs/module-05/lesson03_fitting_solution.py`.

</details>

## Common mistakes

- Reporting a fit with no uncertainty, or with $R^2$ as the only quality measure. Report parameter ± standard uncertainty and look at the residuals.
- Using `absolute_sigma=False` when you know the noise. Your stated errors are then thrown away and replaced by the scatter.
- Leaving out the starting guess `p0` for a nonlinear model. The default guess is 1 for every parameter; for a rate constant of 0.02 min⁻¹ that can send the fit to a wrong minimum or no convergence. Estimate `p0` from the data.
- Ignoring the slope–intercept correlation when propagating to an unknown, which overstates the uncertainty.
- Fitting a straight line through the origin because "Beer's law has no intercept". A real blank or baseline gives a small intercept; force it to zero only if you have measured that it is zero.
- Extrapolating beyond the standards. The calibration says nothing above the highest standard; dilute the sample instead.

## Key takeaways

- `curve_fit` returns parameters and a covariance matrix; uncertainties are the square roots of its diagonal.
- `absolute_sigma=True` when you know each point's noise; the default when you don't.
- Weight points that have different noise; otherwise the value scatters more and the quoted uncertainty is too small.
- Judge the model by residual plots and reduced chi-square near 1, not by $R^2$.
- Propagate with `correlated_values` so the slope–intercept correlation is kept; then read off which term dominates.

## Sources

- [SciPy 1.18 curve_fit](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html) — parameters, `sigma` and `absolute_sigma` semantics, default method.
- [Harvey, Analytical Chemistry 2.1, 5.4](https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_(Harvey)/05%3A_Standardizing_Analytical_Methods/5.04%3A_Linear_Regression_and_Calibration_Curves) — linear regression for calibration and the uncertainty of a predicted concentration.
- [NIST/SEMATECH e-Handbook 4.4.4](https://www.itl.nist.gov/div898/handbook/pmd/section4/pmd44.htm) — residual analysis and why $R^2$ alone is not enough.
- [uncertainties documentation](https://uncertainties.readthedocs.io/en/latest/) — linear error propagation with correlations.
- [lmfit 1.3.4 on PyPI](https://pypi.org/project/lmfit/1.3.4/) — the `Model` interface on top of scipy's least squares.
