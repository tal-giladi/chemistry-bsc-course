---
id: "10.4"
module: 10
minutes: 20
practice_minutes: 120
prerequisites: ["10.3", "09.6", "08.6"]
objectives:
  - Plan a precipitation gravimetry step by step and say how each step limits solubility losses, co-precipitation and weighing errors.
  - Heat a sample to constant mass and calculate its composition from the mass loss, with an uncertainty from the scale resolution.
  - Use Faraday's law to turn a charge into moles in coulometry and electrogravimetry, and calculate a current efficiency.
volatility: concept
sources:
  - title: "LibreTexts — Harvey, Analytical Chemistry 2.1, 8.2 Precipitation Gravimetry"
    url: https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/08%3A_Gravimetric_Methods/8.02%3A_Precipitation_Gravimetry
  - title: "LibreTexts — Harvey, Analytical Chemistry 2.1, 8.3 Volatilization Gravimetry"
    url: https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/08%3A_Gravimetric_Methods/8.03%3A_Volatilization_Gravimetry
  - title: "LibreTexts — Harvey, Analytical Chemistry 2.1, 11.3 Coulometric Methods"
    url: https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/11%3A_Electrochemical_Methods/11.03%3A_Coulometric_Methods
  - title: "Wikipedia, Sodium bicarbonate (thermal decomposition)"
    url: https://en.wikipedia.org/wiki/Sodium_bicarbonate
  - title: "PubChem, Sodium carbonate (CID 10340): GHS classification"
    url: https://pubchem.ncbi.nlm.nih.gov/compound/10340
  - title: "NIST CODATA, Faraday constant"
    url: https://physics.nist.gov/cgi-bin/cuu/Value?f
last_verified: "2026-10-17"
---

# 10.4 · Gravimetry, electrogravimetry and coulometry

Titrations count moles through a volume. The three methods in this lesson count them more directly: gravimetry through a mass on a balance, electrogravimetry through a metal plated onto an electrode, and coulometry through an electric charge. They need no standard solution, and done well they are among the most accurate methods in chemistry. You will plan a precipitation gravimetry in the simulation, do a real volatilisation gravimetry in your kitchen oven by heating baking soda to constant mass, and use Faraday's law to turn coulombs into moles.

## Why it matters

A cement plant must know the sulfate content of its gypsum to within a few tenths of a percent, or the concrete sets wrongly. The reference method is still gravimetric: precipitate barium sulfate, filter, ignite, weigh. A battery manufacturer checks the copper content of an electrolyte by plating it out on a platinum cathode and weighing it. And the water content of pharmaceuticals is routinely measured by Karl Fischer coulometry, where the instrument generates its own iodine and counts the electrons. These methods are slow or need care, but their answer traces straight to a mass or a charge, which is why they are used to check faster methods.

## Core ideas

> [!NOTE]
> Stable: gravimetric factors, constant-mass procedure, Faraday's law. Values checked 2026-10-17: F = 96 485.332 12 C/mol (CODATA 2022, exact); baking soda decomposes gradually from 80–100 °C and faster at 200 °C (Wikipedia, sodium bicarbonate); sodium carbonate is GHS H319, causes serious eye irritation (PubChem). Kitchen-oven temperatures vary by ±10–20 °C; check yours.

### Precipitation gravimetry, step by step

In **precipitation gravimetry** the analyte is turned into an insoluble solid of known formula, which is separated and weighed. Lesson [09.6](../module-09/lesson-06.md) gave the theory; here is the bench routine and why each step exists.

1. **Precipitate slowly from a hot, dilute solution**, adding the reagent with stirring. Low **relative supersaturation** favours a few large crystals over many tiny ones. Large crystals filter well and trap fewer impurities.
2. **Digest**: keep the mixture hot for an hour. Small crystals redissolve and large ones grow, and trapped impurities escape.
3. **Filter** through a weighed sintered-glass crucible or ashless filter paper.
4. **Wash** with a dilute solution of a volatile electrolyte (for AgCl, dilute nitric acid). Pure water can break the solid back into a colloid that passes the filter, called **peptisation**. Each wash also dissolves a little product, so use several small washes.
5. **Dry or ignite to constant mass**: heat, cool in a desiccator, weigh, and repeat until two weighings agree (for an analytical balance, within 0.2–0.3 mg).

The result comes from the **gravimetric factor**, the ratio of analyte mass to precipitate mass. For chloride weighed as AgCl:

$$\text{GF} = \frac{M(\mathrm{Cl})}{M(\mathrm{AgCl})} = \frac{35.453}{143.32} = 0.2474$$

### Errors that only gravimetry has

- **Solubility loss.** BaSO₄ ($K_{sp}$ 1.1 × 10⁻¹⁰) dissolves to $\sqrt{K_{sp}} = 1.05 \times 10^{-5}$ M. A 100 mL wash removes about $1.05 \times 10^{-6}$ mol, 0.24 mg: negligible on a 300 mg precipitate. An excess of the precipitating ion lowers this further (the common-ion effect).
- **Co-precipitation.** Impurities can be built into the crystal (**inclusion**), trapped inside it (**occlusion**) or stuck to its surface (**adsorption**). They add mass, so results read high. Digestion and washing reduce them.
- **Incomplete drying, or water picked up while cooling.** A warm, dry solid can take moisture from the air in seconds, and a warm crucible on a balance reads light because of rising air. Cool it in a desiccator to room temperature before every weighing.

### Volatilisation gravimetry

In **volatilisation gravimetry** you heat the sample and measure the mass of what leaves (or what remains). Your home experiment is the classic:

$$\mathrm{2NaHCO_3(s) \rightarrow Na_2CO_3(s) + H_2O(g) + CO_2(g)}$$

Two moles of baking soda (168.01 g) lose one mole of water and one of CO₂ (62.02 g). The theoretical mass loss is $62.02/168.01 = 36.92\,\%$. If your sample loses less, it either contained something that does not decompose or it has not finished. Heating to constant mass tells the two apart.

### Faraday's law: counting electrons

An electrode reaction transfers a fixed number of electrons, $n$, per particle. The charge passed, $Q$, counts them. With the **Faraday constant** $F$, the charge of one mole of electrons:

$$n_\text{analyte} = \frac{Q}{nF}, \qquad Q = I\,t \ \text{(constant current)}$$

Tiny example: 10.00 mA for 482.5 s is 4.825 C, or $4.825/96485 = 5.00 \times 10^{-5}$ mol of electrons.

This counts the analyte only if every electron goes to the reaction you want: 100 % **current efficiency**. Side reactions, such as hydrogen evolution at the cathode, waste charge.

### Electrogravimetry and coulometry

In **electrogravimetry** a metal is plated onto a weighed electrode, usually platinum gauze: $\mathrm{Cu^{2+} + 2e^- \rightarrow Cu(s)}$. You weigh the cathode before and after. To deposit 99.99 % of the copper from a 10⁻⁴ M solution, the cathode must be held below about +0.105 V against SHE (Harvey, section 11.3); going much more negative starts reducing other ions. To check completeness, add water to raise the level and see whether fresh copper forms on the newly covered metal.

In **coulometry** the charge itself is the measurement. In **controlled-potential coulometry** the electrode is held at a set potential and the current falls as the analyte runs out; the charge is the integral of current over time. In a **coulometric titration** a constant current generates the titrant in the cell, for example OH⁻ from water at a cathode, Ag⁺ from a silver anode, or I₂ from iodide. An indicator or electrode signals the end point, and $Q = It$ replaces the burette reading. No standard solution is needed, and microgram amounts can be titrated because currents and times are measured very precisely.

## Worked example

### 1. Baking soda to constant mass

From `oven_example.csv`: tray 3.52 g, tray plus baking soda 13.51 g, so the sample is 9.99 g. After heating at 200 °C and cooling 15 min each time, the total reads 10.96, 10.18, 9.95, 9.87, 9.85 and 9.85 g at 15 to 90 min. The 60 and 75 min weighings agree within 0.02 g, so constant mass is 9.85 g.

$$\text{loss} = 13.51 - 9.85 = 3.66\ \text{g} = \frac{3.66}{9.99} = 36.64\,\%$$

$$\text{apparent NaHCO}_3 = \frac{36.64}{36.92} = 99.2\,\%$$

Each mass is a difference of two scale readings, so $u = 0.01/\sqrt{6} = 0.004$ g ([lesson 01.5](../module-01/lesson-05.md)). That gives about ±0.1 % on the purity. Is the baking soda really 0.8 % impure? The model behind this data uses pure NaHCO₃, but the warm sodium carbonate picks up 0.015 g of water vapour while it cools on the bench. That systematic error alone accounts for 0.4 % of the 0.8 %; the rest is scale rounding. A desiccator would remove it. This is why gravimetry says "cool, then weigh, then repeat."

### 2. Electrogravimetry of copper

A constant current of 0.500 A for 960 s plates copper onto a platinum gauze cathode. The cathode gains 0.1572 g.

$$Q = 0.500 \times 960 = 480\ \text{C}, \qquad m_\text{theory} = \frac{480}{2 \times 96485} \times 63.546 = 0.1581\ \text{g}$$

$$\text{current efficiency} = \frac{0.1572}{0.1581} = 99.5\,\%$$

The missing 0.5 % of the charge went into hydrogen evolution. For electrogravimetry this does not matter, because you weigh the copper. For coulometry it would be a 0.5 % error, which is why coulometric methods are checked against a standard.

## Hands-on

What you need: the [Module 10 lab folder](../../labs/module-10/) and Python; for Part B baking soda (about 10 g), a small foil tray or oven-safe ceramic dish, a kitchen oven, oven mitts, a kitchen scale with 0.01 g resolution (most pocket scales weigh up to 100–200 g, so the tray must be light), safety glasses and a timer. Time: about 2 hours, mostly waiting.

### Part A — simulations (30 min)

[Simulation: Gravimetry — chloride as silver chloride](../../simulations/gravimetry/index.html?preset=precipitate)

1. Precipitate the chloride twice: once fast and cold, once slowly from hot solution with digestion. Compare the filtering losses.
2. Wash once with water and once with dilute nitric acid; dry once to constant mass and once for a fixed time. Note which choice moves the result most.

[Simulation: Gravimetry — copper by electrodeposition](../../simulations/gravimetry/index.html?preset=electrogravimetry)

[Simulation: Gravimetry — coulometric titration](../../simulations/gravimetry/index.html?preset=coulometry)

3. Plate the copper at two cathode potentials and compare the current efficiency. Then run the coulometric titration and compare the moles from $Q = It$ with the stated amount.

Target: precipitate result within 0.3 % of the stated chloride; current efficiency above 99 % at the better potential.

### Part B — home: baking soda to constant mass (75 min, mostly waiting)

> [!CAUTION]
> Hot oven and hot tray: use oven mitts and put the tray on a heat-proof board. Baking soda gives off only water vapour and carbon dioxide, but the product, sodium carbonate (washing soda), is an eye irritant (GHS H319): wear safety glasses, do not touch your eyes, and do not taste it. Keep children and pets away. Afterwards use it as washing soda or rinse it down the sink.

1. Preheat the oven to 200 °C. Weigh the empty tray and write the mass in `TRAY_G` at the top of `lesson04_gravimetry.py`.
2. Spread about 10 g of baking soda thinly in the tray. Weigh the tray plus sample: this is the reading at time 0.
3. Heat for 15 min. Take the tray out, let it cool on the board for 15 min (it must be at room temperature), and weigh.
4. Repeat step 3 until two weighings in a row agree within 0.02 g. Expect 60–90 minutes in total.
5. Record `t_min,m_total_g` in a CSV file (total heating time and mass).

How you know it worked: the mass falls fast at first, then levels off. The loss comes out between 36.0 and 37.0 % of the sample.

### Part C — Python (15 min)

Fill in `constant_mass` and `moles_from_charge` in `lesson04_gravimetry.py`, then run it on the example and on your data:

```bash
py lesson04_gravimetry.py
py lesson04_gravimetry.py my_oven.csv
```

With the example data it prints a loss of 36.64 %, an apparent content of 99.2 %, the chloride from a gravimetric factor, the moles from a coulometric titration and a current efficiency of 99.5 %. Write up the oven experiment on the [lab report template](../../templates/lab-report.md), with a paragraph on the water uptake while cooling.

<details><summary>Reference solution</summary>

`constant_mass` loops `for i in range(1, len(masses))` and returns `i` when `abs(masses[i] - masses[i - 1]) <= tol`, else `None`. `moles_from_charge` returns `current_a * time_s / (n * F)`. Full code in `lesson04_gravimetry_solution.py`. A real kitchen run usually gives 36.3–36.9 %; a result above 37 % suggests sample was spilled, and one well below 36 % that the oven runs cool or the heating was too short.

</details>

## Common mistakes

- **Weighing a warm tray.** Rising warm air makes it read light, and drying products take up water as they cool. Always cool to room temperature, in the same way each time.
- **Stopping after a fixed time instead of constant mass.** The sample may not be finished. Two agreeing weighings are the only proof.
- **Precipitating fast from cold, concentrated solution.** Tiny crystals pass the filter and trap impurities. Go slow, hot and dilute, then digest.
- **Washing AgCl with pure water.** It peptises and passes the filter. Wash with dilute nitric acid.
- **Assuming 100 % current efficiency.** Side reactions waste charge. Check a coulometric method with a standard, or weigh the product.
- **Using the wrong number of electrons.** Copper(II) needs two electrons per atom, silver(I) one. A wrong $n$ gives an error of a factor of 2.

## Key takeaways

- Gravimetry turns the analyte into a weighable solid; the gravimetric factor converts its mass to the analyte.
- Slow, hot, dilute precipitation, digestion and washing with a volatile electrolyte control crystal size, purity and losses.
- "Constant mass" means two weighings that agree after identical heating and cooling; cooling conditions matter as much as heating.
- Baking soda loses 36.92 % of its mass on heating; a kitchen measurement gets within about 0.5 % of that.
- Faraday's law counts moles from charge, $n_\text{analyte} = It/(nF)$; it is only valid at 100 % current efficiency, while electrogravimetry weighs the product directly.

## Sources

- [Harvey, Analytical Chemistry 2.1, 8.2 Precipitation Gravimetry](https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/08%3A_Gravimetric_Methods/8.02%3A_Precipitation_Gravimetry) — supersaturation, digestion, co-precipitation, washing, drying.
- [Harvey, Analytical Chemistry 2.1, 8.3 Volatilization Gravimetry](https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/08%3A_Gravimetric_Methods/8.03%3A_Volatilization_Gravimetry) — thermal decomposition methods.
- [Harvey, Analytical Chemistry 2.1, 11.3 Coulometric Methods](https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/11%3A_Electrochemical_Methods/11.03%3A_Coulometric_Methods) — Faraday's law, current efficiency, electrogravimetry of copper, coulometric titrations.
- [Wikipedia, Sodium bicarbonate](https://en.wikipedia.org/wiki/Sodium_bicarbonate) — gradual decomposition from 80–100 °C, faster at 200 °C.
- [PubChem, Sodium carbonate](https://pubchem.ncbi.nlm.nih.gov/compound/10340) — GHS H319, serious eye irritation.
- [NIST CODATA, Faraday constant](https://physics.nist.gov/cgi-bin/cuu/Value?f) — 96 485.332 12 C/mol.
