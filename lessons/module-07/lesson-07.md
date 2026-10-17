---
id: "07.7"
module: 7
minutes: 20
practice_minutes: 120
prerequisites: ["07.5", "01.4", "01.5", "05.3"]
objectives:
  - Weigh a sample by difference and explain why this cancels the scale's offset.
  - Choose glassware for a task from its Class A tolerance and read a meniscus without parallax error.
  - Prepare a standard solution by mass and a serial dilution, and calculate their concentrations.
  - Build an uncertainty budget for a prepared solution and name the input that limits it.
volatility: concept
sources:
  - title: "LibreTexts — Harvey, Analytical Chemistry 2.1, 2.4 Basic Equipment"
    url: https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/02%3A_Basic_Tools_of_Analytical_Chemistry/2.04%3A_Basic_Equipment
  - title: "LibreTexts — Harvey, Analytical Chemistry 2.1, 2.5 Preparing Solutions"
    url: https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/02%3A_Basic_Tools_of_Analytical_Chemistry/2.05%3A_Preparing_Solutions
  - title: "Ricca Chemical — Volumetric glassware (Class A tolerances, ASTM E288 and E542)"
    url: https://riccachemical.com/pages/tech-tips/volumetric-glassware
  - title: "UKAS LAB 15 — Traceability: volumetric apparatus"
    url: https://www.ukas.com/wp-content/uploads/2023/05/LAB-15-Traceability-Volumetric-apparatus.pdf
  - title: "ASTM E288-10(2025) Standard Specification for Laboratory Glass Volumetric Flasks"
    url: https://store.astm.org/e0288-10r25.html
  - title: "Engineering ToolBox — Aqueous solutions of inorganic sodium salts, densities"
    url: https://www.engineeringtoolbox.com/density-aqueous-solution-inorganic-sodium-salt-concentration-d_1957.html
  - title: "OpenStax Chemistry 2e, 3.3 Molarity"
    url: https://openstax.org/books/chemistry-2e/pages/3-3-molarity
last_verified: "2026-10-17"
---

# 07.7 · Lab: weighing, glassware and making solutions

Almost every number a chemistry lab produces is traced back to a solution someone weighed and made up by hand. This lesson is the module's practical. You learn the moves of the first-year bench in a simulation: weighing by difference, choosing and reading volumetric glassware, and diluting. Then you make a real salt standard and a food-colour dilution series at home, work out the uncertainty of each in Python, and write a lab report.

## Why it matters

A water lab measures sodium in drinking water against standards of known concentration. If the main standard is made up 2 % too strong, every result for every customer that month is 2 % too low, and no amount of repeating the measurements will show it. That is the systematic error of [Lesson 01.5](../module-01/lesson-05.md), built into the lab's reference. The skills are simple, but each has a reason, and the reasons are what this lesson is about. This course cannot train your hands at a real bench; it trains the decisions and the arithmetic, so that the bench time you get later is spent on technique alone.

## Core ideas

> [!NOTE]
> Weighing by difference, glassware classes and uncertainty budgets are stable practice. The tolerance values below come from ASTM-based tables quoted by Harvey's open textbook and a glassware supplier, checked on 2026-10-17. ASTM revises its standards (E288 for flasks was last reapproved in 2025), so for real work use the tolerance printed on your glassware or its certificate.

### Weighing and weighing by difference

An **analytical balance** reads to 0.1 mg (some to 0.01 mg); a kitchen or pocket scale reads to 1 g, 0.1 g or 0.01 g. The smallest step is the **readability** $d$.

Every scale can have a small **offset**: it shows a little more or less than zero with nothing on it, and that offset can drift. **Weighing by difference** removes it. You weigh a container with the substance ($m_1$), tip out what you need, and weigh the container again ($m_2$). The mass delivered is $m_1 - m_2$, and the offset cancels because it appears in both readings.

The uncertainty of one reading from resolution alone is $d/\sqrt{12}$; for a difference of two readings it is

$$u(\Delta m) = \sqrt{2}\,\frac{d}{\sqrt{12}} = \frac{d}{\sqrt{6}}$$

the value you used in Lesson 01.5. On a 0.1 g scale that is 0.041 g. On an analytical balance it is 0.04 mg.

Let objects reach room temperature first: warm objects create air currents that make them seem lighter.

### Volumetric glassware

Glassware is made either **to contain** (TC, marked "TC" or "In") or **to deliver** (TD, "TD" or "Ex"). A **volumetric flask** contains its volume when filled to the mark; a **transfer pipette** delivers its volume; a **burette** delivers variable, measured volumes. Beakers and graduated cylinders are for rough volumes only.

**Class A** glassware meets the tightest tolerance; **Class B** is allowed twice the Class A tolerance. Typical Class A tolerances at 20 °C:

| Item | Capacity | Class A tolerance | Relative |
|---|---|---|---|
| Volumetric flask | 100 mL | ±0.08 mL | 0.08 % |
| Volumetric flask | 250 mL | ±0.12 mL | 0.05 % |
| Transfer pipette | 10 mL | ±0.02 mL | 0.2 % |
| Transfer pipette | 25 mL | ±0.03 mL | 0.12 % |
| Burette | 50 mL | ±0.05 mL | 0.1 % |
| Oral syringe, uncalibrated | 20 mL | about ±1 % (Lesson 01.5) | 1 % |

A tolerance is a limit, not a standard uncertainty. If any value inside $\pm t$ is equally likely, the standard uncertainty is $t/\sqrt{3}$.

### Reading a meniscus

Water in a narrow tube forms a curved surface, the **meniscus**. For clear liquids you read the **bottom** of the curve. Your eye must be level with it: looking from above makes the volume seem larger, from below smaller. This **parallax error** is systematic for a given habit, so it does not average out.

### Making a standard solution

A **standard solution** has a concentration known accurately enough to calibrate other measurements. There are two routes.

- **By volume:** weigh the solid, dissolve it, transfer quantitatively (rinse everything into the flask), fill to the mark, mix. Then $c = m P / (M V)$, with $P$ the purity as a fraction.
- **By mass:** weigh the solid and the final solution. The **mass fraction** is $w = m_{\text{solute}} P / m_{\text{solution}}$. This needs no flask and is often more accurate. To convert to molar concentration you need the solution's density $\rho$: $c = w\rho/M$.

### Dilutions

Diluting keeps the amount of solute and increases the volume, so $c_1V_1 = c_2V_2$. A **dilution factor** $f = V_1/V_2$ tells how much weaker the new solution is. A **serial dilution** repeats the same step, for example 1:2 five times to reach 1/32. Each step adds a little uncertainty, but every step uses a large, easily measured volume. A single direct 1/32 dilution needs a tiny aliquot whose relative error is large, as you will compute.

### The uncertainty budget

For a result that is a product or quotient of inputs, such as $c = mP/(MV)$, the relative standard uncertainties add in quadrature ([Lesson 02.5](../module-02/lesson-05.md), [Lesson 05.3](../module-05/lesson-03.md)):

$$\frac{u(c)}{c} = \sqrt{\left(\frac{u(m)}{m}\right)^2 + \left(\frac{u(P)}{P}\right)^2 + \left(\frac{u(M)}{M}\right)^2 + \left(\frac{u(V)}{V}\right)^2}$$

An **uncertainty budget** lists each term and its share. Because the terms are squared, the largest one dominates; improve that one first and ignore the rest.

## Worked example

### 1. A 0.1000 mol/L NaCl standard in a 250 mL flask

A lab needs 250.0 mL of 0.1000 mol/L NaCl. The certificate says the NaCl is 99.9 ± 0.1 % pure; $M = 58.44$ g/mol.

**Mass to weigh.** $m = cVM/P = 0.1000 \times 0.2500 \times 58.44 / 0.999 = 1.4625$ g. The analyst weighs by difference and gets 1.4631 g (close is fine; you use the real mass).

**Concentration.**

$$c = \frac{1.4631 \times 0.999}{58.44 \times 0.2500} = 0.10004\ \text{mol/L}$$

**Budget.**

| Input | Value | Standard uncertainty | Relative | Share of variance |
|---|---|---|---|---|
| Mass (0.1 mg balance, by difference) | 1.4631 g | $0.1/\sqrt{6} = 0.041$ mg | 0.003 % | 0.2 % |
| Purity (±0.1 %, rectangular) | 0.999 | $0.001/\sqrt{3} = 0.00058$ | 0.058 % | 81 % |
| Flask (±0.12 mL, rectangular) | 250.0 mL | $0.12/\sqrt{3} = 0.069$ mL | 0.028 % | 19 % |
| Molar mass | 58.44 g/mol | negligible | — | 0 % |

Combined: $\sqrt{0.003^2 + 0.058^2 + 0.028^2} = 0.065$ %, so $c = 0.10004 \pm 0.00006$ mol/L. The purity limits the result. A better balance would change nothing; a purer reagent would.

### 2. Diluting it ten times

Pipette 10.00 mL of the standard into a 100.0 mL flask and fill to the mark: $c_2 = 0.10004 \times 10.00/100.0 = 0.010004$ mol/L.

Relative uncertainties: pipette $0.02/\sqrt{3}/10.00 = 0.115$ %, flask $0.08/\sqrt{3}/100.0 = 0.046$ %, stock 0.065 %. Combined: $\sqrt{0.115^2 + 0.046^2 + 0.065^2} = 0.14$ %. The pipette now dominates; the dilute standard is about twice as uncertain as its parent.

## Hands-on

**What you need:** a computer; the [Module 7 lab folder](../../labs/module-07/); for the home part: non-iodised table salt (read the label), tap or bottled water, liquid food colouring, a clean bottle of 150 mL or more with a lid, six small clear cups, oral syringes of 10 mL and 20 mL (no needles; the 20 mL one calibrated in Lesson 01.5), a 0.1 g or 0.01 g scale, a sheet of white paper, labels, safety glasses; the [notebook page template](../../templates/notebook-page.md). **Time:** about 2 hours.

### Part A — the bench in the simulation (30 min)

[Simulation: Glassware bench — weighing by difference](../../simulations/glassware/index.html?preset=weighing)

Task: weigh about 0.5 g of solid into a beaker, once from a weighing paper and once by difference from a weighing bottle, on a balance whose offset drifts. Target: by difference, within 0.2 mg of the true mass the simulation reveals.

[Simulation: Glassware bench — making a dilution](../../simulations/glassware/index.html?preset=dilution)

Task: make 100.0 mL of a 1/50 dilution, choosing the glassware yourself. Target: a relative uncertainty below 0.3 %. Then repeat it with a graduated cylinder and compare.

[Simulation: Glassware bench — reading a meniscus without parallax](../../simulations/glassware/index.html?preset=parallax)

Task: read a burette with your eye at different heights. Target: the parallax error, in mL, when your eye is 2 cm too high.

### Part B — a salt standard by mass (30 min)

> [!WARNING]
> Kitchen materials only: table salt, water and food colouring. Wear safety glasses. Label every container ("salt solution 5 % — not for drinking") and keep it away from children and from food. Food colouring stains skin, clothes and counters; work on a tray or newspaper. Pour everything down the sink with plenty of water when you finish. Do the risk assessment from [Lesson 01.4](../module-01/lesson-04.md) first.

1. Weigh the empty, dry bottle with its lid ($m_0$).
2. Add about 5 g of salt with a teaspoon and weigh again ($m_1$). Mass of salt: $m_1 - m_0$.
3. Add water until the total is about 100 g above $m_0$ and weigh again ($m_2$). Mass of solution: $m_2 - m_0$.
4. Close and shake until no crystals remain. Let it reach room temperature.
5. Check it: draw 20.0 mL with your calibrated syringe, eye level with the mark, and weigh what it delivers into a cup. Divide by the calibrated volume to get the density. A 5.0 % NaCl solution has a density of 1.034 g/mL at 20 °C.
6. Write all readings in your notebook, then in `my_salt.csv` (copy `salt_standard_example.csv` and replace the masses; keep or change the purity line according to your label).

### Part C — a food-colour serial dilution (30 min)

1. Stock: in a cup, mix 5 drops of food colouring with about 40 g of water.
2. Label five cups 1/2, 1/4, 1/8, 1/16, 1/32. Put cup 1/2 on the scale and note the reading. Add about 10 mL of stock with the 10 mL syringe and note the reading. Add about 10 mL of water and note the reading. The two differences are the aliquot and water masses.
3. Mix well. Make cup 1/4 from cup 1/2 the same way, and so on to 1/32. Rinse the syringe with the next solution before you draw it.
4. Line the cups up on white paper and photograph them in daylight; the colour should fade evenly. Check: equal masses of cup 1/8 and water should match cup 1/16 by eye.
5. Write the masses in `my_dilution.csv` (same columns as `dilution_example.csv`).

### Part D — the uncertainty budget in Python (20 min)

1. Open `lesson07_solutions.py` and complete the two TODOs: combine the relative uncertainties of the salt standard, and propagate the uncertainty of one dilution factor $f = a/(a+w)$ with partial derivatives.
2. Run it on the example data, then on yours:

```bash
py lesson07_solutions.py
py lesson07_solutions.py my_salt.csv my_dilution.csv
```

3. Write a lab report with the [lab report template](../../templates/lab-report.md): aim, method, raw data table, concentration of the salt standard in % w/w and in mol/L with its uncertainty, the budget table, the dilution table and photo, the density check, and a discussion of which input you would improve first.

**How you know it worked:** on the example data the salt standard comes out at $w = 4.999$ %, $c = 0.8845 \pm 0.0078$ mol/L, with the salt mass giving about 85 % of the variance. The serial dilution reaches 1/32 with 0.64 % relative uncertainty, against 6.3 % for a direct one-step dilution on the same scale. Your density check should land within about ±0.005 g/mL of 1.034 g/mL.

<details><summary>Reference solution for the TODOs</summary>

```python
# TODO 1
u_rel = math.sqrt(sum(v ** 2 for v in budget.values()))
# TODO 2
u = math.sqrt((w * ua) ** 2 + (a * uw) ** 2) / (a + w) ** 2
```

The salt mass dominates because 0.041 g is 0.8 % of 5 g but only 0.04 % of 100 g. To halve the uncertainty, weigh 10 g of salt into 200 g of solution, or use a 0.01 g scale. In the dilution, each step adds about 0.29 %, and the cumulative uncertainty grows as $\sqrt{n}$. A direct 1/32 dilution needs only 0.63 g of stock, so the same 0.041 g is about 6 % of it. But a systematic error in one step is carried into every later cup. The full script is `lesson07_solutions_solution.py`.

</details>

## Common mistakes

- **Weighing directly onto paper and tipping it in.** Whatever stays on the paper is lost but counted. Weigh by difference.
- **Measuring a standard in a beaker or graduated cylinder.** Their tolerances are percent-level. Use a volumetric flask, or work by mass.
- **Reading the meniscus from above.** The volume looks larger. Put your eye level with the mark every time.
- **Forgetting purity.** Table salt is not 100 % NaCl; iodised salt and anti-caking agents add a few tenths of a percent or more. Include purity in the budget.
- **Treating a tolerance as a standard uncertainty.** Divide a ±$t$ tolerance by $\sqrt{3}$ first.

## Key takeaways

- Weighing by difference cancels the scale's offset and counts everything you deliver; its resolution uncertainty is $d/\sqrt{6}$.
- Class A volumetric flasks and pipettes are accurate to about 0.05–0.2 %; Class B to twice that; beakers and cylinders are for rough volumes only.
- Read a clear meniscus at the bottom of the curve with your eye level with it.
- Standards can be made by volume ($c = mP/MV$) or by mass ($w = mP/m_{\text{solution}}$, then $c = w\rho/M$).
- In an uncertainty budget, relative uncertainties of a product add in quadrature; find the largest term and improve that one.

## Sources

- [LibreTexts — Harvey, Analytical Chemistry 2.1, 2.4 Basic Equipment](https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/02%3A_Basic_Tools_of_Analytical_Chemistry/2.04%3A_Basic_Equipment) (balances, TC/TD glassware, tolerances).
- [LibreTexts — Harvey, Analytical Chemistry 2.1, 2.5 Preparing Solutions](https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/02%3A_Basic_Tools_of_Analytical_Chemistry/2.05%3A_Preparing_Solutions) (standard solutions, dilutions).
- [Ricca Chemical — Volumetric glassware](https://riccachemical.com/pages/tech-tips/volumetric-glassware) (pipette and burette tolerances; retrieved 2026-10-17).
- [UKAS LAB 15 — Traceability: volumetric apparatus](https://www.ukas.com/wp-content/uploads/2023/05/LAB-15-Traceability-Volumetric-apparatus.pdf) (Class B tolerance is twice Class A).
- [ASTM E288-10(2025) Standard Specification for Laboratory Glass Volumetric Flasks](https://store.astm.org/e0288-10r25.html) (paywalled).
- [Engineering ToolBox — Aqueous solutions of inorganic sodium salts, densities](https://www.engineeringtoolbox.com/density-aqueous-solution-inorganic-sodium-salt-concentration-d_1957.html) (5 % NaCl, 1.034 g/cm³ at 20 °C; retrieved 2026-10-17).
- [OpenStax Chemistry 2e, 3.3 Molarity](https://openstax.org/books/chemistry-2e/pages/3-3-molarity) (molarity and dilution).
