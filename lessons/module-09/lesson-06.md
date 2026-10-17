---
id: "09.6"
module: 9
minutes: 25
practice_minutes: 180
prerequisites: ["09.4", "09.5", "08.4", "07.7"]
objectives:
  - Calculate the buffer capacity of a weak-acid buffer, show that it peaks at pH = pKa, and design a buffer for a target pH and capacity.
  - Calculate an analyte's mass from a precipitate with the gravimetric factor and estimate solubility and co-precipitation errors.
  - Carry out a full calibration from photographed standards, including the linear range, LOD, LOQ, an unknown with its uncertainty and a check standard, and report it in a lab report.
volatility: concept
sources:
  - title: "LibreTexts — Harvey, Analytical Chemistry 2.1, 6.8 Buffer Solutions"
    url: https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/06%3A_Equilibrium_Chemistry/6.08%3A_Buffer_Solutions
  - title: "LibreTexts — Harvey, Analytical Chemistry 2.1, 8.2 Precipitation Gravimetry"
    url: https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/08%3A_Gravimetric_Methods/8.02%3A_Precipitation_Gravimetry
  - title: "LibreTexts — Harvey, Analytical Chemistry 2.1, 16.10 Solubility Products"
    url: https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/16%3A_Appendix/16.10%3A_Solubility_Products
  - title: "W3C CSS Color Module Level 4 — sRGB transfer function"
    url: https://www.w3.org/TR/css-color-4/#predefined-sRGB
  - title: "Wikipedia — Brilliant blue FCF (absorption maximum about 628 nm)"
    url: https://en.wikipedia.org/wiki/Brilliant_blue_FCF
last_verified: "2026-10-17"
---

# 09.6 · Buffers and gravimetric analysis

This lesson closes Analytical Chemistry 1 with two classic topics and the module's practical. Buffers hold a pH steady, and buffer capacity tells you how much acid or base they can absorb before they fail. Gravimetry, the oldest quantitative method, weighs an analyte as a pure precipitate and is still a reference method today. The practical then uses everything in the module: you build a calibration from phone photos of a food-colour dilution series, find its linear range and detection limit, measure an unknown, check for bias and write it up.

## Why it matters

A lab measures a drug whose colour reaction only works at pH 4.5 to 5.0. A technician makes the acetate buffer ten times more dilute to save reagent. Its pH is right, but each acidic sample now pushes it below 4.5 and the results drift low. The pH meter said "fine"; the buffer capacity said "not enough". On the next bench, a gravimetric chloride result comes out low because the precipitate was washed with pure water, which dissolves silver chloride and carries fine particles through the filter. Both errors follow from the equilibria of [Lesson 08.4](../module-08/lesson-04.md).

## Core ideas

> [!NOTE]
> Buffer theory and gravimetry are stable chemistry; the constants ($K_a$ of acetic acid, $K_{sp}$ of AgCl) are from Harvey's Analytical Chemistry 2.1 appendix tables. The sRGB conversion used in the practical is the published standard (IEC 61966-2-1, quoted in the W3C CSS Color 4 specification). Phone cameras differ in how they process images, and those settings change with software updates; checked on 2026-10-17.

### What a buffer does

A **buffer** is a solution of a weak acid HA and its conjugate base A⁻ in similar amounts. Added strong acid is turned into HA ($\text{A}^- + \text{H}_3\text{O}^+ \rightarrow \text{HA} + \text{H}_2\text{O}$); added strong base is turned into A⁻. Only the *ratio* changes, and the pH follows Henderson–Hasselbalch:

$$\text{pH} = \text{p}K_a + \log_{10}\frac{n_{\text{A}^-}}{n_\text{HA}}$$

This is the buffer region of the titration curve in [Lesson 09.5](lesson-05.md).

### Buffer capacity

The **buffer capacity** $\beta$ is the amount of strong base (mol/L) needed to raise the pH by one unit; in calculus terms $\beta = dc_\text{base}/d\text{pH}$. For a weak acid of total concentration $C$ plus water:

$$\beta = 2.303\left([\text{H}_3\text{O}^+] + [\text{OH}^-] + \frac{C\,K_a\,[\text{H}_3\text{O}^+]}{(K_a + [\text{H}_3\text{O}^+])^2}\right)$$

Three facts follow.

- $\beta$ is largest at pH = pKa, where it equals about $2.303\,C/4 = 0.576\,C$. For a 0.10 M acetate buffer that is 0.058 mol/L per pH unit.
- $\beta$ is proportional to $C$. A tenfold dilution keeps the pH but cuts the capacity tenfold, to 0.0058.
- One pH unit from the pKa the capacity has fallen to a third; two units away it is almost gone. So use a buffer only within pKa ± 1.

### Designing a buffer

1. Choose a weak acid with pKa within 1 of the target pH (acetic acid for pH 4–5.7, phosphate's second pKa of 7.20 for pH 6.2–8.2, ammonium at 9.24 for pH 8.2–10.2).
2. Get the ratio from Henderson–Hasselbalch.
3. Choose the total concentration from the capacity you need: the acid or base the samples will add must be small compared with $\beta \times$ (allowed pH change) $\times$ volume.
4. Check the pH with a calibrated meter and adjust; Henderson–Hasselbalch ignores activities and fails for very dilute buffers.

### Gravimetric analysis

In **precipitation gravimetry**, the analyte is converted to a solid of known composition, which is filtered, washed, dried and weighed. Chloride is precipitated with silver nitrate as AgCl; sulfate with barium as BaSO₄. The mass of analyte follows from the **gravimetric factor**, the ratio of molar masses with the stoichiometry:

$$m_\text{Cl} = m_\text{AgCl} \times \frac{M_\text{Cl}}{M_\text{AgCl}} = m_\text{AgCl} \times 0.24735$$

A good precipitate is very insoluble, pure, easy to filter and of exactly known composition after drying. The steps each have a reason:

- **Precipitate slowly from a hot, dilute solution** with slow addition of reagent: low supersaturation gives fewer, larger, purer crystals that filter well.
- **Digest** (keep warm for a while): small crystals dissolve and large ones grow, and trapped impurities escape.
- **Wash with a dilute electrolyte**, not pure water. Pure water dissolves some precipitate and can break a colloid back into particles that pass the filter (peptisation). A common ion in the wash, such as dilute HNO₃ or a little chloride, suppresses the solubility.
- **Dry or ignite to constant mass**: weigh, heat again, weigh again until two weighings agree.

The main errors are **solubility losses** (negative), **co-precipitation** of impurities trapped in or on the crystals (usually positive), and incomplete drying (positive). In **volatilisation gravimetry** the analyte leaves as a gas and the mass lost is measured, as in the baking-soda experiment of [Lesson 07.5](../module-07/lesson-05.md).

### The idea behind the module practical

A blue dye absorbs red light, so a photo's red value falls as the dye concentration rises. Phones store colour as **sRGB**, a non-linear code for screens; undo it to get linear intensity $I$, then compute a **pseudo-absorbance** $A = -\log_{10}(I/I_\text{blank})$, which behaves like the absorbance of Beer–Lambert's law (Module 19). The rest is Lesson 09.4.

## Worked example

### 1. Is the dilute buffer good enough?

A method buffer is 100.0 mL of acetate with equal amounts of HA and A⁻ (pH 4.76). Each sample adds 0.10 mmol of strong acid.

| Buffer | Capacity at pH 4.76 | After 0.10 mmol H⁺ | After 1.00 mmol H⁺ |
|---|---|---|---|
| 0.100 M (5.00 + 5.00 mmol) | 0.058 mol/L per pH | 4.74 (−0.02) | 4.58 (−0.18) |
| 0.010 M (0.50 + 0.50 mmol) | 0.0058 mol/L per pH | 4.59 (−0.17) | 2.30 (buffer exhausted) |
| pure water | about $5 \times 10^{-7}$ | 3.00 | 2.00 |

The concentrated buffer barely moves; the dilute one drops 0.17 per sample, enough to leave the method's window after a few acidic samples. A 1.00 mmol addition overwhelms it completely, because there are only 0.50 mmol of A⁻ to absorb it. For the 0.100 M buffer, Henderson–Hasselbalch gives $4.757 + \log_{10}(4.00/6.00) = 4.58$, the same as the exact charge balance.

### 2. Chloride by gravimetry

A 0.2500 g sample of a chloride salt gives 0.6012 g of dried AgCl.

$$m_\text{Cl} = 0.6012 \times \frac{35.45}{143.32} = 0.1487\ \text{g} \qquad w_\text{Cl} = \frac{0.1487}{0.2500} = 59.48\ \%$$

**Solubility loss.** In pure water $s = \sqrt{K_{sp}} = \sqrt{1.8 \times 10^{-10}} = 1.34 \times 10^{-5}$ mol/L. Washing with 200 mL of water could dissolve $1.34 \times 10^{-5} \times 0.200 \times 143.32 = 0.38$ mg of AgCl, a −0.06 % error. In a wash containing 0.010 M chloride, $s = K_{sp}/[\text{Cl}^-] = 1.8 \times 10^{-8}$ mol/L and the loss falls to 0.0005 mg. This is the **common-ion effect**, and it is why the wash liquid matters.

## Hands-on

**What you need:** the [Module 9 lab folder](../../labs/module-09/); for the practical: liquid **blue** food colouring, tap water, 13 identical clear plastic cups, a 0.1 g scale, white paper, a phone camera, a stack of books or a phone stand, labels, safety glasses, a helper (for the unknown); the [lab report template](../../templates/lab-report.md). **Time:** about 3 hours, of which 2 for the practical.

### Part A — buffers on the bench (20 min)

[Simulation: Titration bench — buffer capacity](../../simulations/titration/index.html?preset=buffer)

Task: add strong acid in small portions to water, to a 0.10 M acetate buffer and to a 0.010 M one, and watch the pH. Target: find how much acid moves each buffer down by 1 pH unit, and check that the ratio between the two buffers is about 10.

### Part B — buffer capacity and gravimetry in Python (25 min)

1. Open `lesson06_buffer.py`. Complete TODO 1 (the buffer capacity formula) and TODO 2 (the gravimetric factor).
2. Run `py lesson06_buffer.py` and open `runs/lesson06_buffer.png`.

**How you know it worked:** the output matches the worked examples ($\beta = 0.0576$ at pH 4.76 for 0.10 M; pH 4.581 after 1.00 mmol HCl; 59.48 % chloride; 0.38 mg lost to pure water). On the log-scale plot, each buffer shows a hump centred at pH 4.76, and water alone has its minimum near pH 7.

<details><summary>Reference solution for the TODOs</summary>

```python
# TODO 1
return 2.303 * (h + KW / h + c_total * ka * h / (ka + h) ** 2)
# TODO 2
m_cl = 0.6012 * M_CL / M_AGCL
```

The plot also shows why very acidic or very basic solutions "buffer" themselves: the $[\text{H}_3\text{O}^+]$ and $[\text{OH}^-]$ terms make $\beta$ large below pH 2 and above pH 12, with no buffer at all. The full script is `lesson06_buffer_solution.py`.

</details>

### Part C — module practical: a calibration with detection limit from phone photos (2 hours)

> [!WARNING]
> Kitchen materials only: food colouring and water. Wear safety glasses. Food colouring stains skin, clothes and counters; work on a tray or newspaper. Label every cup and keep them away from children and food. Pour everything down the sink with plenty of water at the end. Do the risk assessment from [Lesson 01.4](../module-01/lesson-04.md) first.

This experiment trains the analysis, not the use of a real spectrophotometer; Module 19 and Module 25 cover the instrument.

**Make the solutions by mass** (as in [Lesson 07.7](../module-07/lesson-07.md); weigh everything, record every reading).

1. **Stock:** about 10 drops of blue colouring in about 100 g of water. Mix well.
2. **Intermediate (20 % of stock):** 10.0 g stock plus 40.0 g water.
3. **Standards**, each 50.0 g in total, from the intermediate: 0 (water only), 2.5, 5.0, 7.5, 10.0, 15.0, 20.0, 25.0 and 35.0 g of intermediate, topped up with water to 50.0 g. These are 0, 1, 2, 3, 4, 6, 8, 10 and 14 % of stock. Compute the actual concentrations from your actual masses.
4. **Check standard:** a separate 5 % standard made directly from the stock (12.5 g stock + 37.5 g water).
5. **Unknown:** ask your helper to make one 50.0 g solution between 2 % and 6 % of stock and to write the value down without telling you.

**Photograph.**

1. Put a sheet of white paper by a window in daylight (no direct sun, no flash). Fix the phone on books, lens about 20 cm above the cup, looking straight down.
2. Lock exposure and white balance (on most phones: long-press on the image, or use a "pro" mode). If you cannot, take all photos within a few minutes and expect a larger blank scatter.
3. Photograph each cup in the same spot. Photograph the water cup 7 times, lifting and replacing it each time (the blanks), and the unknown and check standard 3 times each.
4. Copy the photos to the lab folder and read the colour values:

```bash
py rgb_from_photos.py blank1.jpg blank2.jpg std00.jpg std01.jpg
```

5. Make `my_photos.csv` with the columns `type,c_percent_stock,R,G,B` (copy `dye_photo_example.csv`, replace the rows, leave the unknown's concentration empty).

**Analyse.**

1. Open `practical_dye_calibration.py` and complete TODO 1 (undo the sRGB curve) and TODO 2 (LOD and LOQ).
2. Run it on the example data, then on yours:

```bash
py practical_dye_calibration.py
py practical_dye_calibration.py my_photos.csv
```

3. Open `runs/practical_dye_calibration.png`. Check that the residuals inside the linear range scatter randomly and that the top standards bend below the line.
4. Write the lab report: method (with the uncertainty of the 1 % standard's mass, Lesson 09.3), raw data, calibration plot with residuals, linear range, LOD and LOQ, the unknown ± standard uncertainty and 95 % interval, the check standard's recovery and $z$, and which errors are random or systematic (Lesson 09.1). Then ask your helper for the true value.

**How you know it worked:** on the example data the script finds a linear range up to 6 % of stock, $A = 0.0018 + 0.1000\,c$, LOD 0.115 % and LOQ 0.383 % of stock, the unknown at $4.74 \pm 0.04$ % (95 % interval ±0.11; the true value is 4.7 %), and the check standard at 100.7 % recovery with $z = +0.8$. With your own photos, expect a linear range up to roughly 5–10 % of stock, an LOD of a few tenths of a percent, and the unknown within about 5 % of the true value.

<details><summary>Reference solution for the TODOs</summary>

```python
# TODO 1
return np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)
# TODO 2
lod, loq = 3 * s_bl / m, 10 * s_bl / m
```

The top standards bend down because of **stray light**: some light reaches the camera without passing through the dye (reflections from the cup and the surface), so the darkest cups never get as dark as Beer–Lambert predicts. That sets the top of the linear range. The blank scatter, mostly small changes in lighting between photos, sets the LOD. Without linearising sRGB the slope comes out about 2.2 times smaller and has no meaning as an absorbance. The full script is `practical_dye_calibration_solution.py`.

</details>

## Common mistakes

- **Diluting a buffer "because the pH is the same".** The pH is the same; the capacity is not. Size the concentration for the acid or base the samples will add.
- **Using a buffer far from its pKa.** Beyond pKa ± 1 the capacity collapses; choose a different weak acid.
- **Washing a precipitate with pure water.** It dissolves some solid and can peptise colloids; wash with a dilute electrolyte that shares an ion.
- **Weighing a precipitate once.** Dry or ignite to constant mass: two weighings that agree.
- **Letting the phone set the exposure.** Auto-exposure changes the brightness between photos and turns every reading into a different calibration. Lock it, or include the blank in every frame.

## Key takeaways

- A buffer's capacity $\beta$ peaks at pH = pKa, is proportional to its concentration and falls to a third one pH unit away.
- Design a buffer by choosing the pKa, then the ratio, then the concentration from the capacity needed.
- Gravimetry converts a precipitate's mass into the analyte's mass with the gravimetric factor; solubility losses, co-precipitation and incomplete drying are its main errors.
- A common ion in the wash liquid suppresses solubility losses.
- A full calibration report gives the linear range, LOD, LOQ, the result with its uncertainty and a check-standard recovery.

## Sources

- [LibreTexts — Harvey, Analytical Chemistry 2.1, 6.8 Buffer Solutions](https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/06%3A_Equilibrium_Chemistry/6.08%3A_Buffer_Solutions) (buffers, Henderson–Hasselbalch, capacity).
- [LibreTexts — Harvey, Analytical Chemistry 2.1, 8.2 Precipitation Gravimetry](https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/08%3A_Gravimetric_Methods/8.02%3A_Precipitation_Gravimetry) (precipitate quality, digestion, washing, co-precipitation).
- [LibreTexts — Harvey, Analytical Chemistry 2.1, 16.10 Solubility Products](https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/16%3A_Appendix/16.10%3A_Solubility_Products) ($K_{sp}$ of AgCl, $1.8 \times 10^{-10}$ at 25 °C).
- [W3C CSS Color Module Level 4 — the predefined sRGB colour space](https://www.w3.org/TR/css-color-4/#predefined-sRGB) (sRGB transfer function).
- [Wikipedia — Brilliant blue FCF](https://en.wikipedia.org/wiki/Brilliant_blue_FCF) (food dye E133; absorption maximum near 628 nm, so it absorbs red light).
