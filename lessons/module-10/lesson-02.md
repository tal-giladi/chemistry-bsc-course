---
id: "10.2"
module: 10
minutes: 20
practice_minutes: 60
prerequisites: ["10.1", "08.6", "08.5", "09.5"]
objectives:
  - Locate the end point of a potentiometric titration from the first derivative, the second derivative and a Gran plot, and say which errors each method is sensitive to.
  - Predict the potential at the equivalence point of a redox titration from formal potentials and choose a redox indicator that changes inside the jump.
  - Extract a formal potential and an acid dissociation constant from real-looking titration data.
  - Describe how manganese in steel is determined and why each step of the method is needed.
volatility: concept
sources:
  - title: "LibreTexts — Harvey, Analytical Chemistry 2.1, 9.4 Redox Titrations"
    url: https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/09%3A_Titrimetric_Methods/9.04%3A_Redox_Titrations
  - title: "LibreTexts — Harvey, Analytical Chemistry 2.1, 9.2 Acid–Base Titrations (derivative methods, Gran plots)"
    url: https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/09%3A_Titrimetric_Methods/9.02%3A_AcidBase_Titrations
  - title: "LibreTexts — Harvey, Analytical Chemistry 2.1, 11.2 Potentiometric Methods"
    url: https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/11%3A_Electrochemical_Methods/11.02%3A_Potentiometric_Methods
  - title: "LibreTexts — Harvey, Analytical Chemistry 2.1, 16.13 Standard Reduction Potentials"
    url: https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/16%3A_Appendix/16.13%3A_Standard_Reduction_Potentials
  - title: "LibreTexts, Determination of the Mn Content of Steel"
    url: https://chem.libretexts.org/Ancillary_Materials/Laboratory_Experiments/Wet_Lab_Experiments/Analytical_Chemistry_Labs/Determination_of_the_Mn_Content_of_Steel
last_verified: "2026-10-17"
---

# 10.2 · Potentiometric and redox titrations

A colour indicator is not always possible: the sample may be coloured or cloudy, or no indicator changes at the right point. Then you follow the titration with an electrode and find the end point from the numbers. This lesson covers the two classic electrode titrations of the S3 lab. The first is an acid–base titration with a pH electrode, where the end point comes from derivatives and a Gran plot. The second is a redox titration of iron(II) with cerium(IV), followed with a platinum electrode, where the curve itself gives formal potentials. It ends with the manganese-in-steel method, a redox reaction turned into a colour measurement.

## Why it matters

An iron-supplement factory must show that each tablet contains its labelled 65 mg of iron. The tablets are dissolved and titrated with cerium(IV). The solution is pale yellow-green and turns darker as cerium is added, so the eye struggles. A platinum electrode does not care about colour. It reads a potential that jumps by about 0.4 V at the equivalence point, and software finds the end point to a few hundredths of a millilitre. Automatic titrators do this in almost every quality-control lab. Knowing how the end point is found tells you when to trust the printout and when the electrode is fooling you.

## Core ideas

> [!NOTE]
> Stable: Nernst-based curve shapes, derivative and Gran methods. Formal potentials used here (Fe³⁺/Fe²⁺ 0.68 V and Ce⁴⁺/Ce³⁺ 1.44 V in 1 M H₂SO₄; ferroin 1.147 V) are from Harvey, Analytical Chemistry 2.1, Appendix 16.13 and section 9.4, checked 2026-10-17. Commercial titrator software and electrode models change; the methods do not.

### Electrodes measure activity, not colour

A **potentiometric titration** follows the cell potential between an **indicator electrode**, which responds to the analyte, and a **reference electrode**, whose potential stays constant. A common reference is silver/silver chloride in saturated KCl, at +0.197 V against the standard hydrogen electrode (SHE). For acid–base work the indicator electrode is a **glass pH electrode**; at 25 °C its response is 59.16 mV per pH unit, the Nernst slope from lesson [08.6](../module-08/lesson-06.md). It must be calibrated with two buffers before use, because each electrode has its own offset and slightly lower slope.

### Finding the end point from data

Near equivalence the curve is steepest. Three ways to locate that point:

- **First derivative.** Compute $\Delta\text{pH}/\Delta V$ between neighbouring points and place it at the midpoint volume. The peak is the end point. Its precision is limited by the step size, so add small increments (0.05–0.1 mL) near the end.
- **Second derivative.** Take the derivative of the first derivative. It crosses zero at the inflection point. Interpolating that crossing usually gives a better estimate than the first-derivative peak.
- **Gran plot.** Before equivalence, a weak acid titrated with a strong base obeys $[\mathrm{H^+}] = K_a\,[\mathrm{HA}]/[\mathrm{A^-}]$. Rearranged, the quantity $V_b \times 10^{-\text{pH}}$ falls on a straight line, $V_b\,10^{-\text{pH}} = K_a (V_\text{eq} - V_b)$. A fit through points at about 50–95 % of the way gives $V_\text{eq}$ as the x-intercept and $K_a$ as minus the slope. Its strength is that it uses many points away from the steep part, where readings are slow and noisy.

A constant pH offset multiplies every Gran point by the same factor. It changes the slope (so $K_a$ comes out wrong) but not the x-intercept (so $V_\text{eq}$ stays right). A drift that grows during the titration bends the line and moves the intercept too.

### The shape of a redox curve

In a redox titration, the potential of the platinum electrode is set by whichever couple has both forms present. For iron(II) titrated with cerium(IV):

$$\mathrm{Fe^{2+} + Ce^{4+} \rightarrow Fe^{3+} + Ce^{3+}}$$

Before equivalence, Fe²⁺ and Fe³⁺ are both present, so the Nernst equation of iron sets the potential:

$$E = E^{\circ\prime}_\mathrm{Fe} + 0.05916 \log\frac{[\mathrm{Fe^{3+}}]}{[\mathrm{Fe^{2+}}]} = E^{\circ\prime}_\mathrm{Fe} + 0.05916 \log\frac{V}{V_\text{eq} - V}$$

After equivalence, cerium sets it: $E = E^{\circ\prime}_\mathrm{Ce} + 0.05916 \log\frac{V - V_\text{eq}}{V_\text{eq}}$. At half-equivalence the log term is zero, so $E = E^{\circ\prime}_\mathrm{Fe}$: the curve measures the formal potential directly, just as the pH at half-equivalence equals p$K_a$. At twice the equivalence volume, $E = E^{\circ\prime}_\mathrm{Ce}$.

A **formal potential**, $E^{\circ\prime}$, is the measured potential when the oxidised and reduced forms have equal total concentrations in a stated medium. It includes activity and complexation effects, so it depends on the acid: the Ce⁴⁺/Ce³⁺ formal potential is 1.70 V in 1 M HClO₄ but 1.44 V in 1 M H₂SO₄, because sulfate binds Ce⁴⁺. Always use the value for your medium.

At equivalence, for two one-electron couples, the potential is the average:

$$E_\text{eq} = \frac{n_1 E^{\circ\prime}_1 + n_2 E^{\circ\prime}_2}{n_1 + n_2}$$

### Visual redox indicators

A **redox indicator** is a molecule whose oxidised and reduced forms have different colours. It changes over about $E^\circ_\text{In} \pm 0.059/n$ V. **Ferroin** ($E^\circ$ = 1.147 V, red when reduced, pale blue when oxidised) suits the Fe/Ce titration. **Permanganate** needs no indicator: MnO₄⁻ is intensely purple and Mn²⁺ nearly colourless, so the first excess drop turns the solution pale pink. **Starch** forms a dark blue-purple complex with iodine, as in the vitamin C titration of lesson [08.5](../module-08/lesson-05.md).

### Manganese in steel

Ordinary steels contain around one percent of manganese, which makes them stronger; ISO 629 covers 0.001 to 4 %. The classic teaching method (and the basis of the standard ISO 629) turns the manganese into permanganate and measures its colour:

1. Dissolve about 0.8 g of steel in hot nitric acid. Iron becomes Fe³⁺, manganese becomes Mn²⁺.
2. Destroy nitrogen oxides and carbon with peroxydisulfate and boiling. Nitrogen oxides would otherwise use up the periodate in step 4.
3. Add phosphoric acid. It binds Fe³⁺ into a colourless complex, so the yellow iron colour does not add to the reading.
4. Oxidise Mn²⁺ to purple MnO₄⁻ with potassium periodate, a strong oxidant: $\mathrm{2Mn^{2+} + 5IO_4^- + 3H_2O \rightarrow 2MnO_4^- + 5IO_3^- + 6H^+}$.
5. Measure the absorbance at 525 nm against a calibration line made from manganese standards that went through the same steps.

This is a redox reaction used as a colour-forming step, followed by the calibration methods of lesson [09.4](../module-09/lesson-04.md). It needs hot concentrated acids and a fume hood; it is shown in the simulation only.

## Worked example

### 1. Predicting the iron/cerium curve

25.00 mL of 0.0500 M Fe²⁺ in 1 M H₂SO₄ is titrated with 0.1000 M Ce⁴⁺. Equivalence: $V_\text{eq} = 25.00 \times 0.0500 / 0.1000 = 12.50$ mL.

- At 6.25 mL (half-way): $E = 0.68$ V vs SHE.
- At 12.49 mL (99.9 %): $E = 0.68 + 0.05916 \log(999) = 0.68 + 0.18 = 0.86$ V.
- At equivalence: $E = (0.68 + 1.44)/2 = 1.06$ V.
- At 12.51 mL (100.1 %): $E = 1.44 + 0.05916 \log(0.001) = 1.44 - 0.18 = 1.26$ V.

Between 99.9 % and 100.1 % the potential jumps by 0.40 V, so one drop (0.05 mL, 0.4 %) crosses the whole jump. Ferroin changes between about 1.09 and 1.21 V, inside the jump, so it is a good choice. The electrode reads against Ag/AgCl, so subtract 0.197 V: the meter shows about 0.86 V at equivalence.

### 2. Derivatives from real-looking pH data

The example file `potentiometric_example.csv` has these four readings around the jump:

| V (mL) | 19.80 | 19.90 | 20.00 | 20.10 |
|---|---|---|---|---|
| pH | 6.851 | 7.128 | 8.795 | 10.431 |

First derivatives: 2.77, 16.67 and 16.36 pH/mL at 19.85, 19.95 and 20.05 mL. The peak is at 19.95 mL, but two steps are almost equal, so the true end point lies between them. Second derivatives: $(16.67 - 2.77)/0.1 = +139$ at 19.90 mL and $(16.36 - 16.67)/0.1 = -3$ at 20.00 mL. Interpolating the zero crossing:

$$V_\text{end} = 19.90 + 0.10 \times \frac{139}{139 + 3} = 20.00\ \text{mL}$$

The acid was 25.00 mL, so its concentration is $0.1000 \times 20.00/25.00 = 0.0800$ mol/L. The Gran plot from 10 to 19 mL gives 19.92 mL, 0.4 % low, because the example electrode drifts upward by 0.002 pH per reading. The pH at half-equivalence reads 4.79 instead of the true p$K_a$ of 4.757, because the electrode also has a +0.04 offset. Both errors are invisible on the raw curve.

## Hands-on

What you need: the [Module 10 lab folder](../../labs/module-10/) and Python. Time: about 60 minutes. There is no home version: potentiometric work needs a pH meter, and the iron/cerium and manganese methods need concentrated acids and a fume hood. If you want a visual redox titration at home, repeat the vitamin C and povidone-iodine titration of lesson 08.5.

### Part A — simulations (25 min)

[Simulation: Titration bench — potentiometric end point with electrode drift](../../simulations/titration/index.html?preset=potentiometric)

1. Calibrate the pH electrode with the two buffers offered, then titrate the weak acid. Use 1 mL steps at first and 0.1 mL steps between 18 and 21 mL.
2. Read the end point from the simulation's derivative plot. Then repeat without calibrating and compare.

[Simulation: Titration bench — iron(II) with cerium(IV), ferroin or electrode](../../simulations/titration/index.html?preset=redox)

3. Titrate once with ferroin by eye and once with the platinum electrode. Record both end points.

Target: the two redox end points agree within 0.05 mL; the uncalibrated pH titration gives the same end-point volume but a p$K_a$ that is off.

### Part B — Python: derivatives, Gran plot and formal potentials (35 min)

Open `lesson02_potentiometric.py`, fill in `derivative_endpoint` and `gran_endpoint`, and run:

```bash
py lesson02_potentiometric.py
```

It prints the end points by three methods, $K_a$ from the Gran slope, the iron concentration, and the two formal potentials read from the redox curve, and saves `runs/lesson02_potentiometric.png`. Put your numbers in the [error-analysis template](../../templates/error-analysis.md): which result is affected by the electrode offset, which by the drift, and which by neither?

How you know it worked: acid-base end points of 19.95 (first derivative), 20.00 (second) and 19.92 mL (Gran); $\mathrm{p}K_a$ from Gran 4.80; Fe²⁺ 0.0500 mol/L; $E^{\circ\prime}$ 0.682 V for iron and 1.440 V for cerium.

<details><summary>Reference solution</summary>

`derivative_endpoint`: `d1 = np.diff(y) / np.diff(v)`, `vm = (v[:-1] + v[1:]) / 2`, return `vm[np.argmax(np.abs(d1))]`. `gran_endpoint`: select the window, `g = v * 10 ** -ph`, `slope, intercept = np.polyfit(v, g, 1)`, return `(-intercept / slope, -slope)`. Full code in `lesson02_potentiometric_solution.py`.

Discussion: the offset shifts every pH by +0.04, so p$K_a$ reads 0.04 high, but the derivative end points do not move. The drift grows with each reading, so it tilts the Gran line and its intercept comes out 0.08 mL low. The second-derivative end point is the most robust here.

</details>

## Common mistakes

- **Big volume steps near the end point.** The derivative peak can only be as sharp as your step. Add 0.05–0.1 mL at a time where the readings change fastest.
- **Reading before the electrode settles.** Near equivalence the potential takes longer to stabilise; wait for a steady reading (within 0.1 mV or 0.002 pH over 10 s).
- **Using standard instead of formal potentials.** $E^\circ$ for Ce⁴⁺/Ce³⁺ is 1.72 V, but in sulfuric acid the curve levels off near 1.44 V. Use $E^{\circ\prime}$ for the medium.
- **Forgetting the reference electrode.** A meter reading of 0.86 V against Ag/AgCl is 1.06 V against SHE. Mixing scales makes indicator choices look wrong.
- **Fitting the Gran plot through the steep region.** Points close to equivalence break the straight-line assumption. Use about 50–95 % of the way.
- **Skipping the reagent blank in the manganese method.** Iron and other ions absorb a little at 525 nm; the untreated aliquot corrects for it.

## Key takeaways

- An electrode follows the titration when colour cannot; the end point is found from the data.
- The second derivative's zero crossing and the Gran plot beat the first-derivative peak; each has its own sensitivity to offsets and drift.
- In a redox titration the half-equivalence potential equals the analyte's formal potential, and for two one-electron couples $E_\text{eq}$ is the average of the two.
- Formal potentials depend on the medium; choose an indicator whose window lies inside the jump.
- Manganese in steel is oxidised to permanganate by periodate and measured at 525 nm, after removing nitrogen oxides and masking iron.

## Sources

- [Harvey, Analytical Chemistry 2.1, 9.4 Redox Titrations](https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/09%3A_Titrimetric_Methods/9.04%3A_Redox_Titrations) — Fe/Ce curve, equivalence potential, ferroin, permanganate, starch.
- [Harvey, Analytical Chemistry 2.1, 9.2 Acid–Base Titrations](https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/09%3A_Titrimetric_Methods/9.02%3A_AcidBase_Titrations) — derivative methods and Gran plots.
- [Harvey, Analytical Chemistry 2.1, 11.2 Potentiometric Methods](https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/11%3A_Electrochemical_Methods/11.02%3A_Potentiometric_Methods) — reference electrodes, glass electrode.
- [Harvey, Analytical Chemistry 2.1, 16.13 Standard Reduction Potentials](https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/16%3A_Appendix/16.13%3A_Standard_Reduction_Potentials) — formal potentials in 1 M H₂SO₄ and HClO₄.
- [LibreTexts, Determination of the Mn Content of Steel](https://chem.libretexts.org/Ancillary_Materials/Laboratory_Experiments/Wet_Lab_Experiments/Analytical_Chemistry_Labs/Determination_of_the_Mn_Content_of_Steel) — the periodate method, step by step.
