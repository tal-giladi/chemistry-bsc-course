# Error analysis

## 1. Repeated measurements

| Trial | Value | Unit |
|---|---|---|
| 1 | | |
| 2 | | |
| 3 | | |

- Mean $\bar{x} = \frac{1}{n}\sum x_i$
- Sample standard deviation $s = \sqrt{\frac{\sum (x_i-\bar{x})^2}{n-1}}$
- Standard error $s/\sqrt{n}$
- 95% confidence interval $\bar{x} \pm t_{0.975,\,n-1}\, s/\sqrt{n}$

## 2. Uncertainty budget

| Source | Type (random / systematic) | Size | How estimated |
|---|---|---|---|
| | | | |

## 3. Propagation

For $y = f(x_1, x_2, \dots)$ with independent uncertainties:

$$u_y^2 = \sum_i \left(\frac{\partial f}{\partial x_i}\right)^2 u_{x_i}^2$$

Shortcuts: sums and differences add absolute uncertainties in quadrature; products and quotients add relative uncertainties in quadrature.

## 4. Result

$y = \dots \pm \dots$ (unit), coverage (for example 95%), number of trials, dominant source of uncertainty.
