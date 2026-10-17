---
id: "10.5"
module: 10
minutes: 20
practice_minutes: 75
prerequisites: ["10.2", "10.3", "09.4", "08.6"]
objectives:
  - Calibrate an ion-selective electrode, check its slope against the Nernst value and find the range where the calibration is linear.
  - Explain what a selectivity coefficient and a total ionic strength adjustment buffer do, and when to use standard addition instead of a calibration line.
  - Calculate the hardness of a water from the calcium and magnesium on its label, and estimate an unknown water's hardness with a calibrated soap-lather test.
volatility: implementation
sources:
  - title: "LibreTexts — Harvey, Analytical Chemistry 2.1, 11.2 Potentiometric Methods"
    url: https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/11%3A_Electrochemical_Methods/11.02%3A_Potentiometric_Methods
  - title: "US EPA, SW-846 Method 9214: Potentiometric determination of fluoride with an ion-selective electrode"
    url: https://www.epa.gov/sites/default/files/2015-12/documents/9214.pdf
  - title: "WHO, Fluoride chemical fact sheet (Guidelines for drinking-water quality, 2022)"
    url: https://cdn.who.int/media/docs/default-source/wash-documents/water-safety-and-quality/chemical-fact-sheets-2022/fluoride-fact-sheet-2022.pdf?sfvrsn=4b5bc983_2&download=true
  - title: "USGS, Do you have information about water hardness in the United States?"
    url: https://www.usgs.gov/faqs/do-you-have-information-about-water-hardness-united-states
  - title: "Taub Center, Environmental Health in Israel: drinking water"
    url: https://ehf.taubcenter.org.il/en/tchum/drinking_water-2/
last_verified: "2026-10-17"
---

# 10.5 · Ion-selective electrodes and water testing

An ion-selective electrode is a pH electrode for one particular ion: fluoride, calcium, nitrate, sodium. Dip it in, read millivolts, convert to concentration. In this lesson you learn how to calibrate one honestly, what makes it respond to the wrong ion, and why a buffer called TISAB is added to every solution. Then you put the whole module together for the last S3 topic, water testing, and measure the hardness of your own tap water with soap, calibrated against the labels of bottled waters.

## Why it matters

Drinking water is tested for dozens of parameters, and the fast field methods are electrodes and titrations. Fluoride is the classic electrode case. A little protects teeth, but above the WHO guideline value of 1.5 mg/L it causes dental fluorosis, and much higher levels damage bones. In Israel, fluoride has not been added to drinking water since 2014, so the question is what occurs naturally. A fluoride electrode answers in a minute, but only if it is calibrated in the right range. Below about 0.5 mg/L a straight-line calibration can read far too high. The US EPA method warns of a bias of up to 160 %. Knowing where the line bends is the difference between a real result and a false alarm.

## Core ideas

> [!NOTE]
> Stable: the Nernst response, selectivity and standard addition. Will go out of date: guideline values and national regulations. Checked 2026-10-17: WHO fluoride guideline 1.5 mg/L (2022 fact sheet; the Guidelines' third addendum appeared in June 2026); Israel's drinking-water standards date from 1974, updated 2013, with no fluoridation since 2014 (Taub Center); US EPA Method 9214 (fluoride ISE, TISAB at pH 5–5.5); USGS hardness classes. Check the Israeli Ministry of Health for the current limits before using them.

### How an ion-selective electrode responds

An **ion-selective electrode** (ISE) has a membrane that lets only one kind of ion set up a potential across it. The fluoride electrode uses a single crystal of lanthanum fluoride, LaF₃; the pH electrode uses a thin glass. Against a reference electrode, the cell potential follows the Nernst equation of lesson [08.6](../module-08/lesson-06.md):

$$E = K + \frac{0.05916\ \text{V}}{z} \log a$$

Here $a$ is the ion's **activity** (its effective concentration), $z$ its charge (−1 for F⁻), and $K$ a constant that includes the reference electrode and the junction potential. At 25 °C a one-charge ion gives 59.16 mV per tenfold change; a two-charge ion such as Ca²⁺ only 29.6 mV. For fluoride the sign is negative: more fluoride, lower potential. $K$ is different for every electrode and drifts slowly, so you never use it from a book. You calibrate.

### Calibrating: slope, linear range and detection limit

Measure standards that bracket the samples, plot $E$ against $\log c$ and fit a straight line (lesson [09.4](../module-09/lesson-04.md)). Check three things:

- **Slope.** It should be close to the Nernst value for the temperature. A much smaller slope means a worn or dirty membrane.
- **Linear range.** At low concentrations the response flattens, because the membrane itself dissolves a little and other ions contribute. Look at the residuals: if the lowest standards fall off the line, fit only the linear part and do not extrapolate below it.
- **Temperature.** Standards and samples must be within about 1 °C of each other. In the EPA method, an electrode calibrated at 22 °C read a 20.0 mg/L fluoride solution as 13.6 mg/L at 32 °C.

### Selectivity and the role of TISAB

No membrane is perfectly selective. The **selectivity coefficient** $K_{A,I}$ measures how strongly an interfering ion $I$ is mistaken for the analyte $A$; a small value means good selectivity. For the fluoride electrode the main interferent is OH⁻ ($K \approx 0.1$). The glass pH electrode has a small sodium error: at pH 12.7 in 0.05 M Na⁺ it reads about 12.2.

For fluoride, every standard and sample is mixed 1 : 1 with a **total ionic strength adjustment buffer** (TISAB), which does three jobs:

1. It sets a high, constant ionic strength, so activity coefficients are the same in all solutions and the electrode responds to concentration.
2. It buffers at pH 5–5.5. Higher pH lets OH⁻ interfere; below pH 4 fluoride turns into HF, which the electrode does not see.
3. It contains a chelating agent that frees fluoride bound to Al³⁺ and Fe³⁺.

### Standard addition: when the matrix matters

If the sample matrix might change the response, use **standard addition**: measure the sample, add a small known amount of analyte to the same solution, and measure again. Because both readings are in the same matrix, matrix effects cancel. With slope $S$ (mV per decade) and potentials $E_1$ and $E_2$, the concentration ratio after/before is $R = 10^{(E_2 - E_1)/S}$. Before the addition the analyte is at $c_1 = c_x V_x / V_t$, where $V_x$ is the sample volume and $V_t$ the total with TISAB. After adding $V_s$ of standard $c_s$ it is $c_2 = (c_x V_x + c_s V_s)/(V_t + V_s)$. Setting $c_2 = R\,c_1$ and solving gives $c_x$; the script does it for you.

### Water testing: putting the module together

A basic water analysis uses every method in this module:

| Parameter | Method | Lesson |
|---|---|---|
| pH, alkalinity | glass electrode; titration with acid to pH 4.5 | 10.1, 10.2 |
| Total, Ca and Mg hardness | EDTA titration at pH 10 and pH 12–13 | 10.3 |
| Chloride | Mohr or Volhard titration | 10.3 |
| Dissolved solids, sulfate | evaporation or BaSO₄ gravimetry | 10.4 |
| Fluoride | ISE with TISAB | 10.5 |

**Hardness** is reported as mg/L of CaCO₃. From a label listing calcium and magnesium in mg/L:

$$\text{hardness} = 2.497\,[\mathrm{Ca}] + 4.118\,[\mathrm{Mg}]$$

The factors are $100.09/40.08$ and $100.09/24.31$. The USGS calls water soft below 60 mg/L, moderately hard at 61–120, hard at 121–180 and very hard above 180. Israeli tap water depends on its source. Desalinated water is soft (calcium is added back after desalination), while water from limestone aquifers is often very hard.

Soap measures hardness directly. Ca²⁺ and Mg²⁺ precipitate soap as scum, so no lasting lather forms until they are used up. The number of soap drops needed is a rough titration of hardness. Pure soap is needed: synthetic detergents lather even in hard water.

## Worked example

### 1. Fluoride by calibration line

From `fluoride_ise_example.csv`, five standards from 0.50 to 10.0 mg/L give a slope of −57.6 mV/decade (97 % of the Nernst value of 59.16 at 25 °C) and an intercept of −43.0 mV. Sample A reads −39.1 mV:

$$\log c = \frac{-39.1 - (-43.0)}{-57.6} = -0.0677, \qquad c = 0.86\ \text{mg/L}$$

The 0.10 and 0.20 mg/L standards sit 4.1 and 1.8 mV below the line, because the response flattens. Sample B reads +7.0 mV, which is below the linear range. The line gives 0.136 mg/L, but the true value in the model is 0.12 mg/L: 13 % high, just the bias the EPA method warns about. Report it as "below 0.5 mg/L", or measure it with a low-level calibration.

### 2. The same sample by standard addition

50.0 mL of sample A plus 50.0 mL of TISAB reads −39.3 mV. After adding 1.00 mL of a 100.0 mg/L fluoride standard it reads −69.6 mV, so $\Delta E = -30.3$ mV.

$$R = 10^{-30.3/-57.6} = 3.36$$

With $V_x = 50.0$, $V_t = 100.0$ and $V_s = 1.00$ mL:

$$c_x = \frac{100.0 \times 1.00}{101.0 \times 50.0 \times (3.36/100.0 - 1/101.0)} = 0.84\ \text{mg/L}$$

It agrees with the calibration result within 2 %, so the matrix has no large effect. Both are well below the WHO guideline of 1.5 mg/L.

### 3. Hardness from a label

A bottled water lists Ca 32 mg/L and Mg 12 mg/L. Hardness $= 2.497 \times 32 + 4.118 \times 12 = 79.9 + 49.4 = 129$ mg/L as CaCO₃: hard, by the USGS classes.

## Hands-on

What you need: the [Module 10 lab folder](../../labs/module-10/) and Python; for Part B three bottled waters with different calcium and magnesium on the label (one low-mineral), tap water, a little boiled and fully cooled tap water, pure liquid soap (castile-type, made from oils; not a "body wash" or dishwashing detergent), a small screw-top jar or bottle, a 20 mL syringe, a dropper, and safety glasses. Time: about 75 minutes.

### Part A — simulation (15 min)

[Simulation: Titration bench — potentiometric end point with electrode drift](../../simulations/titration/index.html?preset=potentiometric)

Calibrate the electrode with two buffers and note the slope the simulation reports. Then calibrate again after the "aged electrode" option and see how the slope and the end point change. Target: say which result (end-point volume or measured pH) the aged electrode spoils.

### Part B — home: a soap titration of water hardness (40 min)

> [!WARNING]
> Soap stings the eyes: wear safety glasses when shaking the jar. Let boiled water cool completely before using it. Use only soap and drinking water; do not add washing soda, vinegar or any cleaning product. Never mix bleach with anything.

1. Write down Ca and Mg from each bottled-water label and compute its hardness.
2. Put 20 mL of the first water in the clean jar. Add one drop of soap, close the lid and shake hard for 10 seconds.
3. Repeat until a lather covers the whole surface and lasts 30 seconds. Count the drops.
4. Rinse the jar well and repeat for every water, twice each, from the softest to the hardest. Use the same dropper and hold it the same way every time (you calibrated a drop in lesson 10.1).
5. Write the results as `water,ca_mg_L,mg_mg_L,drops`, leaving Ca and Mg empty for tap and boiled tap water.

How you know it worked: the drop count rises steadily with the label hardness, and duplicate counts agree within one or two drops. Boiled tap water needs fewer drops than unboiled tap water if your water has temporary (carbonate) hardness, because boiling precipitates part of the calcium as CaCO₃, the scale in your kettle.

### Part C — Python (20 min)

Fill in `fit_calibration` and `standard_addition` in `lesson05_ise.py`, and run:

```bash
py lesson05_ise.py
py lesson05_ise.py fluoride_ise_example.csv my_soap.csv
```

With the example data it prints the electrode slope, the residuals of every standard, both samples (with a warning for B), the standard-addition result of 0.837 mg/L, and the soap calibration line with an estimate of about 255 mg/L for the tap water. Record your soap results on a [notebook page](../../templates/notebook-page.md) and state the uncertainty honestly: one drop is about 17 mg/L of hardness in the example.

<details><summary>Reference solution</summary>

`fit_calibration`: `slope, intercept = np.polyfit(logc, e, 1)` and return both as floats. `standard_addition`: `r = 10 ** ((e2 - e1) / slope)`, return `c_s * v_s / ((v_t + v_s) * v_x * (r / v_t - 1 / (v_t + v_s)))`. Full code in `lesson05_ise_solution.py`.

The soap test is a rough titration: it has a blank (about 1–2 drops needed even in pure water), the end point is subjective, and soaps differ. The bottled-water calibration corrects for the soap and your judgement, which is exactly what a calibration is for.

</details>

## Common mistakes

- **Extrapolating below the lowest standard.** ISE responses flatten at low concentration and the line reads high. Fit the linear range and report results below it as "less than".
- **Forgetting TISAB in the standards.** Samples and standards must be treated the same, or activity and pH differ between them.
- **Measuring cold samples against warm standards.** The slope and $K$ change with temperature. Equilibrate all solutions to within 1 °C.
- **Using the book value of $K$.** Every electrode has its own; calibrate each session.
- **Testing hardness with detergent.** Synthetic detergents lather in hard water and show nothing. Use pure soap.
- **Reporting hardness as calcium.** Hardness includes magnesium and is reported as mg/L CaCO₃.

## Key takeaways

- An ISE follows the Nernst equation, 59.16/$z$ mV per decade at 25 °C; calibrate every session and check the slope.
- Fit only the linear range; below it, results are biased high.
- TISAB fixes ionic strength, sets the pH to 5–5.5 and frees fluoride from Al³⁺ and Fe³⁺.
- Standard addition cancels matrix effects; agreement with the calibration line shows the matrix is harmless.
- Hardness $= 2.497\,[\mathrm{Ca}] + 4.118\,[\mathrm{Mg}]$ in mg/L CaCO₃; a soap titration calibrated with bottled-water labels gives a usable estimate at home.

## Sources

- [Harvey, Analytical Chemistry 2.1, 11.2 Potentiometric Methods](https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/11%3A_Electrochemical_Methods/11.02%3A_Potentiometric_Methods) — ISE response, selectivity coefficients, LaF₃ electrode, sodium error.
- [US EPA, SW-846 Method 9214](https://www.epa.gov/sites/default/files/2015-12/documents/9214.pdf) — fluoride ISE, TISAB at pH 5–5.5, bias below 0.5 mg/L, temperature effect.
- [WHO, Fluoride fact sheet (2022)](https://cdn.who.int/media/docs/default-source/wash-documents/water-safety-and-quality/chemical-fact-sheets-2022/fluoride-fact-sheet-2022.pdf?sfvrsn=4b5bc983_2&download=true) — guideline value 1.5 mg/L.
- [USGS, Water hardness](https://www.usgs.gov/faqs/do-you-have-information-about-water-hardness-united-states) — soft, moderately hard, hard and very hard classes.
- [Taub Center, Environmental Health in Israel: drinking water](https://ehf.taubcenter.org.il/en/tchum/drinking_water-2/) — 1974 standards updated 2013; no fluoridation since 2014; calcium added to desalinated water.
