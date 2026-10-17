---
id: "09.2"
module: 9
minutes: 25
practice_minutes: 70
prerequisites: ["09.1", "01.5"]
objectives:
  - Calculate the mean, standard deviation, relative standard deviation and 95 % confidence interval of a set of replicate results using Student's t.
  - Use a one-sample t-test to decide whether a mean differs significantly from a certified value, and state the conclusion in plain words.
  - Compare two methods with an F-test followed by the right two-sample t-test.
  - Apply Grubbs' test to one suspected outlier and explain when removing it is justified.
volatility: concept
sources:
  - title: "LibreTexts — Harvey, Analytical Chemistry 2.1, 4.4 The Distribution of Measurements and Results"
    url: https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/04%3A_Evaluating_Analytical_Data/4.04%3A_The_Distribution_of_Measurements_and_Results
  - title: "LibreTexts — Harvey, Analytical Chemistry 2.1, 4.5 Statistical Analysis of Data"
    url: https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/04%3A_Evaluating_Analytical_Data/4.05%3A_Statistical_Analysis_of_Data
  - title: "LibreTexts — Harvey, Analytical Chemistry 2.1, 4.6 Statistical Methods for Normal Distributions"
    url: https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/04%3A_Evaluating_Analytical_Data/4.06%3A_Statistical_Methods_for_Normal_Distributions
  - title: "LibreTexts — Harvey, Analytical Chemistry 2.1, 16.7 Critical Values for Grubb's Test"
    url: https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/16%3A_Appendix/16.07%3A_Critical_Values_for_Grubb's_Test
  - title: "NIST/SEMATECH e-Handbook of Statistical Methods, 1.3.5.17.1 Grubbs' Test for Outliers"
    url: https://itl.nist.gov/div898/handbook/eda/section3/eda35h1.htm
  - title: "SciPy 1.18 documentation — scipy.stats"
    url: https://docs.scipy.org/doc/scipy/reference/stats.html
last_verified: "2026-10-17"
---

# 09.2 · Statistics: mean, standard deviation and confidence intervals

A handful of replicate results is a small sample of all the results you could have got. Statistics tells you what that sample allows you to say about the true value, and how sure you can be. This lesson turns the mean and standard deviation of [Lesson 01.5](../module-01/lesson-05.md) into a confidence interval, and then into the three tests an analyst uses every week: is my mean different from the certificate, are these two methods different, and is this odd result a blunder?

## Why it matters

A lab is deciding whether to replace its slow chloride titration with a fast ion-selective electrode (ISE). Both are run on the same certified reference material, seven times each. The ISE's mean is 24.74 mg/L against a certificate of 25.0 mg/L, and a quick test says the difference is not significant. The lab almost switches. Then someone notices that one ISE result, 26.87, sits far above the rest. Testing it, removing it for a recorded reason and re-testing changes the answer completely: the ISE reads 2.4 % low. One unexamined number nearly decided a purchase. The tests below make that kind of decision honest.

## Core ideas

> [!NOTE]
> The statistics here (normal and t distributions, t-, F- and Grubbs' tests) are stable textbook methods; the conventions follow Harvey's Analytical Chemistry 2.1 and the NIST/SEMATECH e-Handbook. The function names are from SciPy 1.18 (pinned in `labs/common/requirements.txt`), checked on 2026-10-17.

### Population and sample

Imagine repeating a measurement forever. All those results form the **population**, with a true mean $\mu$ and a true standard deviation $\sigma$. You only ever have a **sample** of $n$ results, with mean $\bar{x}$ and standard deviation

$$s = \sqrt{\frac{\sum (x_i - \bar{x})^2}{n-1}}$$

The $n - 1$ is the number of **degrees of freedom**: once you know the mean, only $n - 1$ of the deviations are free. The **relative standard deviation** is $\text{RSD} = 100\,\% \times s/\bar{x}$; analysts often call it the coefficient of variation.

### The normal distribution

Random errors from many small causes add up to a bell-shaped **normal distribution**. About 68 % of results lie within $\pm 1\sigma$ of $\mu$, 95 % within $\pm 1.96\sigma$, and 99.7 % within $\pm 3\sigma$. The mean of $n$ results is less scattered than a single result; its standard deviation is $\sigma/\sqrt{n}$, the **standard error of the mean**.

### Confidence intervals and Student's t

If you knew $\sigma$, the interval $\bar{x} \pm 1.96\,\sigma/\sqrt{n}$ would contain $\mu$ in 95 % of experiments. But you only have $s$, which is itself uncertain when $n$ is small. William Gosset ("Student") worked out the fix: replace 1.96 by a larger number $t$ that depends on the degrees of freedom.

$$\mu = \bar{x} \pm \frac{t\,s}{\sqrt{n}}$$

| $n$ | 3 | 5 | 7 | 10 | ∞ |
|---|---|---|---|---|---|
| $t$ (95 %, two-sided) | 4.303 | 2.776 | 2.447 | 2.262 | 1.960 |

With three replicates the interval is more than twice as wide as the large-sample one. That is why analysts rarely report fewer than three.

A 95 % **confidence interval** does not mean "the true value is inside with 95 % probability" for this one interval. It means that if you repeated the whole experiment many times, 95 % of the intervals made this way would contain $\mu$. You will see that directly in the simulation.

### The logic of a significance test

Every test has the same shape.

1. State a **null hypothesis** $H_0$: there is no difference (no bias, the methods agree).
2. Compute a test statistic from the data.
3. Compare it with a **critical value** for a chosen **significance level** $\alpha$, usually 0.05. Equivalently, compute the **p-value**: the probability of a statistic at least this large if $H_0$ were true.
4. If the statistic exceeds the critical value ($p < \alpha$), reject $H_0$: the difference is "significant". Otherwise you have **no evidence** of a difference, which is not the same as proof that there is none.

Two mistakes are possible. A **type I error** rejects a true $H_0$ (a false alarm, probability $\alpha$). A **type II error** keeps a false $H_0$ (a missed bias). Small samples make type II errors likely.

### Mean versus a reference: the one-sample t-test

$$t_\text{exp} = \frac{|\bar{x} - \mu_\text{ref}|}{s/\sqrt{n}}$$

Compare $t_\text{exp}$ with $t$ for $n - 1$ degrees of freedom. This is the formal version of the $z$-score in [Lesson 09.1](lesson-01.md). It ignores the certificate's own uncertainty, so use it when that uncertainty is small compared with $s/\sqrt{n}$.

### Two methods: the F-test, then a t-test

To compare two sets of results, first ask whether their precisions differ. The **F-test** uses the ratio of variances, larger over smaller:

$$F_\text{exp} = \frac{s_A^2}{s_B^2} \quad (s_A > s_B)$$

If $F_\text{exp}$ is below the critical value, the variances can be **pooled**:

$$s_p = \sqrt{\frac{(n_A - 1)s_A^2 + (n_B - 1)s_B^2}{n_A + n_B - 2}} \qquad t_\text{exp} = \frac{|\bar{x}_A - \bar{x}_B|}{s_p\sqrt{1/n_A + 1/n_B}}$$

with $n_A + n_B - 2$ degrees of freedom. If the variances differ, use **Welch's t-test** instead (`equal_var=False` in SciPy).

### One suspicious result: Grubbs' test

**Grubbs' test** checks whether the result farthest from the mean is an outlier:

$$G = \frac{\max |x_i - \bar{x}|}{s}$$

Compare $G$ with the tabulated critical value (2.020 for $n = 7$ at $\alpha = 0.05$). Rules: the data must be roughly normal; test one suspect only; never apply it again and again to the same set. A significant $G$ is a reason to look in the notebook for a cause, and to report that you removed the value and why.

## Worked example

### Titration or ISE?

The chloride CRM is certified at 25.0 mg/L. Results (`replicates.csv`, simulated):

- Titration: 24.77, 24.94, 25.58, 25.23, 24.43, 25.00, 24.78
- ISE: 24.44, 23.92, 24.47, 24.47, 26.87, 24.49, 24.55

**Step 1: ISE as it stands.** $\bar{x} = 24.74$, $s = 0.96$, $t_\text{exp} = 0.26/(0.96/\sqrt{7}) = 0.70$, below $t = 2.447$. No evidence of bias. This is the quick test that nearly decided the purchase.

**Step 2: the suspect.** $G = (26.87 - 24.74)/0.96 = 2.21$, above the critical 2.020 for $n = 7$. The notebook shows that 26.87 was copied from the line below (a gross error). It is removed, and the removal is written in the report.

**Step 3: ISE again, $n = 6$.** $\bar{x} = 24.39$, $s = 0.233$, 95 % CI $= 24.39 \pm 2.571 \times 0.233/\sqrt{6} = 24.39 \pm 0.24$ mg/L. The certificate value 25.0 lies outside the interval. Formally, $t_\text{exp} = 0.61/(0.233/\sqrt{6}) = 6.41 > 2.571$ ($p = 0.0014$): the ISE reads significantly low, by 2.4 %.

**Step 4: titration.** $\bar{x} = 24.96$, $s = 0.367$, CI $= 24.96 \pm 0.34$ mg/L, $t_\text{exp} = 0.28$. No evidence of bias.

**Step 5: compare the two.** $F = 0.367^2/0.233^2 = 2.48$, below the critical $F_{6,5} = 6.98$, so pool: $s_p = 0.313$ and

$$t_\text{exp} = \frac{24.96 - 24.39}{0.313\sqrt{1/7 + 1/6}} = 3.28 > t_{11} = 2.201$$

The methods differ. The ISE is more precise but biased; it could be used only after its calibration is fixed and a CRM confirms the fix.

## Hands-on

**What you need:** a computer with the [Module 9 lab folder](../../labs/module-09/); for Part C, your scale and one coin; the [error analysis template](../../templates/error-analysis.md). **Time:** about 70 minutes.

### Part A — what "95 % confidence" means (20 min)

[Simulation: Measurement error — repeat readings](../../simulations/measurement-error/index.html?preset=repeat)

Task: take a set of 5 readings and write down the 95 % confidence interval of the mean. Repeat for 20 sets. Then reveal the true value and count how many of your intervals contain it. Target: about 19 of 20 (anything from 17 to 20 is normal). Then repeat with sets of 3 and notice how much wider the intervals become.

### Part B — the tests in Python (30 min)

1. Open `lesson02_stats.py` and complete the two TODOs: the confidence-interval half-width and Grubbs' $G$.
2. Run it:

```bash
py lesson02_stats.py
```

3. Set `REMOVE_OUTLIERS = False` near the top of the script and run it again. Write down how the ISE verdict changes.

**How you know it worked:** the output matches the worked example: Grubbs flags ISE result 5 ($G = 2.21$ against 2.02), the ISE $t_\text{exp}$ is 6.41 with $p = 0.0014$, $F = 2.48$ and the pooled two-sample test gives $t = 3.28$, $p = 0.0074$.

<details><summary>Reference solution for the TODOs</summary>

```python
# TODO 1
half = t * s / np.sqrt(n)
# TODO 2
g = dev[i] / x.std(ddof=1)
```

With the outlier kept, the ISE mean is 24.74 with $s = 0.96$, and the one-sample test gives $p = 0.51$: "no significant bias". The single gross error inflates $s$ fourfold and hides a real 2.4 % bias. This is a type II error caused by bad data, not by bad luck. The full script is `lesson02_stats_solution.py`.

</details>

### Part C — home: when s comes out as zero (20 min)

> [!WARNING]
> A coin and a kitchen scale only. Keep small coins away from young children.

1. Weigh one coin ten times. Lift it off and put it back on a different spot each time, and wait for the reading to settle.
2. Write the results in `my_repeats.csv` with the columns `method,value` (use `coin` as the method name) and run `py lesson02_stats.py my_repeats.csv`. Ignore the t-test line; it compares with the chloride certificate.
3. On a 0.1 g scale you will probably get the same reading every time, so $s = 0$ and the confidence interval has zero width. Explain in your template why that interval is wrong, and what uncertainty you would report instead.

**How you know it worked:** you can say that the scale's resolution hides the scatter, so the standard uncertainty is at least $d/\sqrt{12} = 0.029$ g (Lesson 01.5), whatever the repeats show.

## Common mistakes

- **Using 1.96 instead of t for a small sample.** With $n = 3$ the right factor is 4.303; the 1.96 interval is far too narrow.
- **Reading "not significant" as "no difference".** A small sample may simply be too weak to show a real bias. Report the confidence interval, not just the verdict.
- **Skipping the F-test.** Pooling variances that clearly differ gives the wrong degrees of freedom and the wrong answer; use Welch's test then.
- **Removing outliers by eye, or repeatedly.** Use Grubbs' test once, on one suspect, and record the reason. Never "clean" data until it looks nice.
- **Dividing by $n$ instead of $n - 1$.** NumPy's `std()` divides by $n$ unless you pass `ddof=1`.

## Key takeaways

- Report a mean with its confidence interval $\bar{x} \pm t s/\sqrt{n}$, with $t$ for $n - 1$ degrees of freedom.
- A significance test asks whether a difference is larger than the scatter could explain; $p < 0.05$ means "significant at 95 %".
- Compare a mean with a certificate using a one-sample t-test; compare two methods with an F-test and then a pooled or Welch t-test.
- Grubbs' test can flag one outlier; removing it needs a recorded reason.
- A single gross error can hide a real bias by inflating $s$.

## Sources

- [LibreTexts — Harvey, Analytical Chemistry 2.1, 4.4 The Distribution of Measurements and Results](https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/04%3A_Evaluating_Analytical_Data/4.04%3A_The_Distribution_of_Measurements_and_Results) (normal distribution, confidence intervals).
- [LibreTexts — Harvey, Analytical Chemistry 2.1, 4.5 Statistical Analysis of Data](https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/04%3A_Evaluating_Analytical_Data/4.05%3A_Statistical_Analysis_of_Data) (significance testing, type I and II errors).
- [LibreTexts — Harvey, Analytical Chemistry 2.1, 4.6 Statistical Methods for Normal Distributions](https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/04%3A_Evaluating_Analytical_Data/4.06%3A_Statistical_Methods_for_Normal_Distributions) (t-tests, F-test, outliers).
- [LibreTexts — Harvey, Analytical Chemistry 2.1, 16.7 Critical Values for Grubb's Test](https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/16%3A_Appendix/16.07%3A_Critical_Values_for_Grubb's_Test) (critical G).
- [NIST/SEMATECH e-Handbook of Statistical Methods, Grubbs' Test for Outliers](https://itl.nist.gov/div898/handbook/eda/section3/eda35h1.htm) (assumptions; one outlier only).
- [SciPy 1.18 documentation — scipy.stats](https://docs.scipy.org/doc/scipy/reference/stats.html) (`t.ppf`, `f.ppf`, `ttest_1samp`, `ttest_ind`).
