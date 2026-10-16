---
id: "01.5"
module: 1
minutes: 20
practice_minutes: 120
prerequisites: ["01.2", "01.3", "01.4"]
objectives:
  - Assemble a safe home kit from kitchen and pharmacy items and record each instrument's resolution.
  - Calibrate a syringe by weighing water and explain why repeats alone cannot remove a systematic error.
  - Calculate a mean, a standard deviation and a combined standard uncertainty for a density.
  - Decide whether a measured density agrees with a reference value, using the uncertainty.
volatility: concept
sources:
  - title: "JCGM 100:2008 — Guide to the Expression of Uncertainty in Measurement (GUM)"
    url: https://www.bipm.org/en/committees/jc/jcgm/publications
  - title: "NIST Technical Note 1297 — Guidelines for Evaluating and Expressing the Uncertainty of NIST Measurement Results"
    url: https://www.nist.gov/pml/nist-technical-note-1297
  - title: "Tanaka et al. (2001), Recommended table for the density of water between 0 °C and 40 °C, Metrologia 38, 301"
    url: https://doi.org/10.1088/0026-1394/38/4/3
  - title: "NBS Letter Circular LC 770 — sucrose solution densities at 20 °C (Plato)"
    url: https://nvlpubs.nist.gov/nistpubs/Legacy/LC/nbslettercircular770.pdf
  - title: "OpenStax Chemistry 2e, 1.5 Measurement Uncertainty, Accuracy, and Precision"
    url: https://openstax.org/books/chemistry-2e/pages/1-5-measurement-uncertainty-accuracy-and-precision
last_verified: "2026-10-16"
---

# 01.5 · Your home kit and first measurement

This lesson builds your home kit and uses it for the module's practical: measuring the density of water and of three sugar solutions with a kitchen scale and a syringe. You will calibrate the syringe, repeat each measurement, work out how far to trust each result, and check it against reference data. It uses everything from this module: units, sig figs, the notebook, the report and the risk assessment.

## Why it matters

A drinks factory checks the sugar content of every batch. One fast way is density: more sugar, denser liquid. A density meter reading of 1.0381 g/mL means about 10% sugar. But a meter that reads 1% high would make every batch look sweeter than it is. Nobody would notice by repeating the measurement, because the meter would be wrong the same way every time. The factory catches it by **calibrating**: measuring something whose answer is already known, such as pure water.

That is exactly what you will do today, with a syringe instead of a density meter. The skills are the same ones used in every analytical lab: repeat, calibrate, estimate the uncertainty, compare with a reference.

## Core ideas

### Your home kit

Everything below comes from a kitchen shop, supermarket or pharmacy. Write each item and its **resolution** (smallest step it shows or marks) on your equipment page.

| Item | Use in this course | Note |
|---|---|---|
| Digital kitchen scale | weighing | 1 g steps is enough today; a 0.1 g or 0.01 g pocket scale is a good upgrade |
| Oral syringes, 10 mL and 20 mL | measuring and dispensing volume | pharmacy, **no needles**; label them for the kit only |
| Kitchen thermometer | temperature | optional today |
| Safety glasses | eye protection | ordinary safety glasses from a hardware shop |
| Clear cups and jam jars, labels, marker | containers | label every container |
| Bound notebook, pen | records | from Lesson 01.3 |
| Phone | photos, timer; the phyphox app in later modules | |
| Food items | sugar, salt, vinegar, baking soda, citric acid, red cabbage, food colouring | used across Modules 1–25 |

A real lab would use an analytical balance (0.1 mg steps) and a glass volumetric pipette. This experiment does not train those hands-on skills, but it teaches the reasoning behind them.

### Density

**Density** is mass per unit volume:

$$\rho = \frac{m}{V}$$

The symbol $\rho$ is the Greek letter rho. In chemistry it is usually given in g/mL (the same as g/cm³). Water at 20 °C has $\rho = 0.99821$ g/mL. Dissolving sugar adds mass faster than it adds volume, so sugar solutions are denser: about 1.038 g/mL at 10% sugar by mass, and 1.127 g/mL at 30%. Density falls slightly as temperature rises, by about 0.02–0.03% per °C near room temperature for water.

### Two kinds of error

An **error** is the difference between your result and the true value. It has two parts:

- **Random error** changes from repeat to repeat: how you read a mark, a bubble, the last digit of the scale. Repeats reveal it, and averaging reduces it.
- **Systematic error** (bias) is the same every time: a syringe whose marks are 1% off, a scale that reads 2 g high. Repeats do **not** reveal it, and averaging does **not** reduce it. Only a **calibration**, a check against a known value, finds it.

**Precision** is how close repeats are to each other. **Accuracy** is how close the result is to the true value. A biased syringe can be very precise and still inaccurate.

### Spread of the repeats: Type A

The international guide to uncertainty, the **GUM** (Guide to the Expression of Uncertainty in Measurement), calls an uncertainty worked out from repeats a **Type A** evaluation.

For $n$ repeats $x_1, \dots, x_n$, the **mean** is $\bar{x} = \frac{1}{n}\sum x_i$. The **standard deviation** measures the typical distance of a repeat from the mean:

$$s = \sqrt{\frac{\sum (x_i - \bar{x})^2}{n-1}}$$

The mean is more reliable than any single repeat. Its **standard uncertainty** is

$$u_A = \frac{s}{\sqrt{n}}$$

Tiny example: masses 101, 100, 101, 101, 101 g. The mean is 100.8 g, $s = 0.45$ g, and $u_A = 0.45/\sqrt{5} = 0.20$ g. Four times more repeats would halve $u_A$.

### What the instrument cannot show: Type B

A **Type B** evaluation uses other knowledge, such as the instrument's resolution. A scale with steps of $d = 1$ g shows 101 g for anything from 100.5 to 101.5 g. If every value in that window is equally likely, the standard uncertainty of one reading is

$$u = \frac{d}{\sqrt{12}} = 0.29 \text{ g}$$

Your water mass is a difference of two readings (full cup minus empty cup), so the two add: $u_{res} = d/\sqrt{6} = 0.41$ g. This matters when all your repeats show the same number: $s = 0$ does not mean the result is perfect.

### Combining uncertainties

Independent uncertainties combine like the sides of a right triangle:

$$u = \sqrt{u_A^2 + u_{res}^2}$$

For a quotient such as $\rho = m/V$, combine **relative** uncertainties (uncertainty divided by the value) in the same way:

$$\frac{u(\rho)}{\rho} = \sqrt{\left(\frac{u(m)}{m}\right)^2 + \left(\frac{u(V)}{V}\right)^2}$$

Module 9 treats this properly. Today, this rule is enough.

### Agreement with a reference

Your result agrees with a reference value if the difference is small compared with your uncertainty. A common rule is

$$|z| = \frac{|\rho - \rho_{ref}|}{u(\rho)} \le 2$$

If $|z|$ is much larger than 2, look for a systematic error before you blame the reference.

> [!NOTE]
> The ideas here (random and systematic error, Type A and B, calibration) are stable. The reference values are long-established: water from the CIPM formula (Tanaka et al., 2001) and sucrose solutions from Plato's table at 20 °C. Kit items and their prices vary by shop; none of the choices here depends on a specific product. Checked 2026-10-16.

## Worked example

These numbers are from `labs/module-01/example_data.csv`: simulated data for a 20 mL syringe filled 5 times (100 mL marked) at 23 °C, on a 1 g scale.

**Step 1: water, nominal density.** The five water masses are 101, 100, 101, 101, 101 g, mean 100.8 g. Using the marked volume:

$$\rho_{nom} = \frac{100.8 \text{ g}}{100.0 \text{ mL}} = 1.008 \text{ g/mL}$$

That is higher than water can be. Something is biased.

**Step 2: calibrate the syringe.** The CIPM formula gives water at 23 °C as 0.99754 g/mL. So the true volume delivered is $100.8 / 0.99754 = 101.05$ mL. The **calibration factor** is

$$f = \frac{V_{true}}{V_{marked}} = \frac{1.008}{0.99754} = 1.0105$$

Five fills of this syringe deliver about 101.0 mL, not 100.0 mL.

**Step 3: the 10% solution.** Masses 105, 105, 104, 104, 105 g, mean 104.6 g, so $\rho_{nom} = 1.046$ g/mL. Corrected:

$$\rho = \frac{1.046}{1.0105} = 1.035 \text{ g/mL}$$

**Step 4: uncertainty.** For the 10% solution: $s = 0.55$ g, $u_A = 0.25$ g, $u_{res} = 0.41$ g, so $u(m) = 0.48$ g, a relative 0.46%. The calibration factor carries the water's own relative uncertainty, 0.45%. Combined:

$$\frac{u(\rho)}{\rho} = \sqrt{0.0046^2 + 0.0045^2} = 0.0064, \quad u(\rho) = 0.007 \text{ g/mL}$$

**Step 5: compare.** The reference for 10% sugar is 1.0381 g/mL at 20 °C, which is 1.0374 g/mL at 23 °C. The difference is $-0.002$ g/mL, so $|z| = 0.3$. The result agrees.

**Result:** $\rho = 1.035 \pm 0.007$ g/mL (standard uncertainty) for 10% sugar at 23 °C. Without the calibration you would have reported 1.046 g/mL, with $|z| \approx 3$: a clear disagreement that no number of repeats would fix. The largest uncertainty is the 1 g scale resolution; a 0.1 g scale would cut it by ten.

## Hands-on

> [!WARNING]
> Kitchen materials only: tap water and table sugar. Use oral syringes without needles. Wipe spills straight away, because sugar solution makes floors slippery, and keep water away from the scale's electronics. Wear safety glasses. Do the risk assessment from Lesson 01.4 first.

**What you need:** the kit above, about 200 g of sugar, four jars, your notebook, a computer with Python and [the Module 1 lab files](../../labs/module-01/README.md) (setup steps are in the README). **Time:** about 2 hours.

### Warm-up in the simulation (15 minutes)

[Simulation: Measurement error — repeat readings](../../simulations/measurement-error/index.html?preset=repeat)

Task: take 5, then 20, then 80 readings. Note how $s$ stays about the same while $u_A = s/\sqrt{n}$ halves each time $n$ grows four times. Target: find the smallest $n$ that brings $u_A$ below a quarter of $s$.

[Simulation: Measurement error — a biased instrument](../../simulations/measurement-error/index.html?preset=bias)

Task: switch on the bias. Show that more repeats do not move the mean towards the true value, then use the calibration step to remove it.

### Make the solutions (25 minutes)

Make 200 g of each solution **by mass**, which is more accurate than by volume:

| Solution | Sugar / g | Water / g |
|---|---|---|
| 10% | 20 | 180 |
| 20% | 40 | 160 |
| 30% | 60 | 140 |

Weigh the sugar into a labelled jar, add water to the total mass, close and shake until no crystals are left. Let the jars reach room temperature (dissolving sugar cools them a little).

### Measure (50 minutes)

1. Copy `labs/module-01/data_template.csv` to `my_data.csv`. Draw the same table in your notebook.
2. **Water first.** Weigh an empty dry cup and write the reading. Draw 20 mL of water into the syringe slowly; tap out any bubble; set the plunger edge on the 20 mL mark with your eye level with it. Empty it into the cup. Repeat for 5 fills. Weigh the cup again.
3. Empty and dry the cup. Repeat step 2 until you have 5 repeats.
4. Measure the room or water temperature.
5. Do the same for the 10%, then 20%, then 30% solution. Rinse the syringe twice with the next solution before you start it.

### Analyse (30 minutes)

1. Open `labs/module-01/density_analysis.py` and complete the two TODOs: the calibration factor, then the resolution uncertainty.
2. Run it on the example data first. Your output should match the worked example. Then run it on `my_data.csv` with `--plot`.
3. Write a one-page report as in Lesson 01.3, with the results table, the plot and your discussion.

**How you know it worked:** your calibration factor is between about 0.97 and 1.03; your densities rise steadily with sugar content; the 30% solution is near 1.13 g/mL; and most values agree with the reference within $|z| \le 2$.

<details><summary>Reference solution for the two TODOs</summary>

TODO 1, calibration factor. The true volume is $m/\rho_{water}$ and the nominal density is $m/V_{marked}$, so

```python
f = rho_nom_w / rho_w_true
```

TODO 2, resolution uncertainty, converted from grams to g/mL by the same ratio as the mass:

```python
u_res = SCALE_RESOLUTION_G / math.sqrt(6) / np.mean(g["mass"]) * mean
u = math.sqrt(u_a ** 2 + u_res ** 2)
```

The full script is `labs/module-01/density_analysis_solution.py`. If a value fails the $|z|$ test, check: was the solution fully dissolved, was there a bubble, did you rinse the syringe with that solution, was the solution warm?

</details>

## Common mistakes

- **Trusting the syringe marks.** A 1% bias is normal for cheap syringes. Calibrate with water every session.
- **Thinking repeats remove bias.** They reduce random error only. Calibration removes bias.
- **Reporting zero uncertainty because all readings were equal.** That shows the scale's resolution is the limit. Use $d/\sqrt{6}$.
- **Bubbles in the syringe.** A bubble steals volume and makes the density look high. Draw slowly and tap.
- **Undissolved sugar or a warm solution.** Both shift the density. Shake until clear; wait for room temperature.
- **Too many digits.** With $u = 0.007$ g/mL, write 1.035, not 1.03512.

## Key takeaways

- The home kit uses kitchen and pharmacy items only. Record each instrument's resolution.
- Random errors show in repeats and shrink with averaging, as $s/\sqrt{n}$. Systematic errors need calibration.
- Type A uncertainty comes from repeats; Type B from other knowledge, such as resolution $d/\sqrt{12}$ per reading.
- For $\rho = m/V$, combine relative uncertainties as the square root of the sum of squares.
- A result agrees with a reference when $|\rho - \rho_{ref}|/u \le 2$.

## Sources

- [JCGM 100:2008 — Guide to the Expression of Uncertainty in Measurement (GUM)](https://www.bipm.org/en/committees/jc/jcgm/publications) (Type A and Type B evaluation; rectangular distribution).
- [NIST Technical Note 1297](https://www.nist.gov/pml/nist-technical-note-1297) (a short guide to the same rules).
- [Tanaka et al. (2001), Metrologia 38, 301](https://doi.org/10.1088/0026-1394/38/4/3) (CIPM formula for the density of water, 0–40 °C).
- [NBS Letter Circular LC 770](https://nvlpubs.nist.gov/nistpubs/Legacy/LC/nbslettercircular770.pdf) (sucrose solution densities at 20 °C, from Plato's table).
- [OpenStax Chemistry 2e, 1.5](https://openstax.org/books/chemistry-2e/pages/1-5-measurement-uncertainty-accuracy-and-precision) (accuracy and precision).
