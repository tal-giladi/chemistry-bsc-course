---
id: "24.2"
module: 24
minutes: 22
practice_minutes: 120
prerequisites: ["24.1", "07.4", "13.6"]
objectives:
  - Choose a recrystallisation solvent from solubility data and calculate the minimum volume and the best possible recovery.
  - Explain oiling out, hot filtration, slow cooling and the second crop, and avoid the common recrystallisation failures on the virtual bench.
  - Use Raoult's law to predict the vapour composition over a liquid mixture and the number of theoretical plates a separation needs.
  - Recrystallise alum (or sugar) at home and compare your recovery with the limit set by solubility.
volatility: concept
sources:
  - title: "MIT OpenCourseWare RES.5-0001 Digital Lab Techniques Manual, Video 9: Recrystallization"
    url: https://ocw.mit.edu/courses/res-5-0001-digital-lab-techniques-manual-spring-2007/resources/recrystallization/
  - title: "MIT OpenCourseWare RES.5-0001, Video 15: Distillation I, Simple and Fractional Distillations"
    url: https://ocw.mit.edu/courses/res-5-0001-digital-lab-techniques-manual-spring-2007/resources/distillation-i-simple-fractional-distillations/
  - title: "LibreTexts, Nichols, Organic Chemistry Lab Techniques, chapter 3 Crystallization"
    url: https://chem.libretexts.org/Bookshelves/Organic_Chemistry/Organic_Chemistry_Lab_Techniques_(Nichols)/03%3A_Crystallization
  - title: "LibreTexts, Nichols, Organic Chemistry Lab Techniques, chapter 5 Distillation"
    url: https://chem.libretexts.org/Bookshelves/Organic_Chemistry/Organic_Chemistry_Lab_Techniques_(Nichols)/05%3A_Distillation
  - title: "PubChem, Acetanilide (CID 904): solubility in cold and boiling water"
    url: https://pubchem.ncbi.nlm.nih.gov/compound/904
  - title: "PubChem, Potassium alum (CID 24856): solubility"
    url: https://pubchem.ncbi.nlm.nih.gov/compound/24856
  - title: "NIST Chemistry WebBook, Cyclohexane: phase change data and Antoine constants"
    url: https://webbook.nist.gov/cgi/cbook.cgi?ID=C110827&Mask=4
  - title: "NIST Chemistry WebBook, Toluene: phase change data and Antoine constants"
    url: https://webbook.nist.gov/cgi/cbook.cgi?ID=C108883&Mask=4
last_verified: "2026-10-17"
---

# 24.2 · Purification: recrystallisation and distillation

A crude product is never pure. Solids are purified by recrystallisation: dissolve in a hot solvent, let the solution cool, and collect the crystals that grow while the impurities stay behind. Liquids are purified by distillation: boil, and collect what condenses at the right temperature. Both rest on physical chemistry you already know, solubility and intermolecular forces from [07.4](../module-07/lesson-04.md) and Raoult's law from [13.6](../module-13/lesson-06.md), and both fail in predictable ways. This lesson turns the theory into the decisions you make at the bench, and ends with a real recrystallisation in your kitchen.

## Why it matters

Your crude aspirin melts over 128–133 °C instead of sharply at 135 °C, and the iron(III) test says salicylic acid is still in it. A pharmacy would reject it; so would the grader. One recrystallisation, done well, fixes it. Done badly, with three times too much solvent, it fixes the purity but throws away a third of the product; with cooling that is too fast, the impurity is trapped inside the crystals. Distillation has the same kind of trade-off. Two liquids that boil 30 °C apart cannot be separated in one simple distillation, and knowing why saves an afternoon.

## Core ideas

> [!NOTE]
> The principles are stable. Solubilities are from PubChem and Antoine constants from the NIST Chemistry WebBook, both checked 2026-10-17. The cyclohexane–toluene model assumes an ideal solution (Raoult's law), which this nearly ideal pair follows closely; real mixtures can deviate strongly.

### Recrystallisation: the solvent does the work

A good recrystallisation solvent:

1. dissolves the compound **well when hot** and **poorly when cold** (a large solubility difference is the whole point);
2. either dissolves the impurities well even when cold (they stay in the **mother liquor**, the liquid left after crystallisation) or does not dissolve them at all (they are filtered off hot);
3. does not react with the compound, and is volatile enough to evaporate from the crystals;
4. boils **below the melting point** of the compound. Otherwise the compound melts in the hot solvent and separates as an oil, which traps impurities and sets into a sticky lump. This is **oiling out**.

"Like dissolves like" ([07.4](../module-07/lesson-04.md)) gives the first guess: water or ethanol–water for polar compounds that can hydrogen-bond, such as acetanilide or aspirin; hexane or ethyl acetate–hexane for non-polar ones. If no single solvent works, a **two-solvent** method dissolves the compound in a hot "good" solvent and adds a "poor" one drop by drop until the solution just turns cloudy.

### The procedure, step by reason

| Step | Why |
|---|---|
| Add the **minimum** amount of boiling solvent | Every millilitre keeps some product dissolved when cold. |
| **Hot gravity filtration** through fluted paper (only if solid impurities remain) | Removes insoluble dirt; done hot and fast so the product does not crystallise in the funnel. |
| Cool **slowly** to room temperature, then in ice | Slow growth builds ordered crystals that exclude impurities; fast cooling traps them. |
| Scratch the glass or add a **seed crystal** if nothing forms | A supersaturated solution needs a surface to start crystals. |
| **Vacuum filtration** on a Büchner funnel; wash with a little **ice-cold** solvent | Removes the mother liquor that wets the crystals without redissolving them. |
| Dry to constant mass | Wet crystals give yields over 100 % and low melting points. |

Concentrating the mother liquor gives a **second crop**: more product, but less pure, because the impurities are now more concentrated. Keep it separate and check its melting point.

Recovery is limited by the cold solubility. If $s_\text{cold}$ is the solubility in g/mL and you used volume $V$, at least $s_\text{cold}V$ grams stay dissolved:

$$\text{recovery}_\text{max} = \frac{m - s_\text{cold}\,V}{m}$$

### Distillation: one boil is one equilibrium stage

For an ideal liquid mixture, **Raoult's law** gives each component's partial pressure as its mole fraction times its pure vapour pressure, $p_i = x_i P_i^*(T)$. The mixture boils when the partial pressures add up to the outside pressure. The vapour is richer in the more volatile component:

$$y_1 = \frac{x_1 P_1^*(T)}{P}, \qquad \alpha = \frac{P_1^*}{P_2^*}$$

where $\alpha$, the **relative volatility**, measures how easy the separation is. The pure vapour pressures come from the Antoine equation, $\log_{10}(P^*/\text{bar}) = A - B/(T + C)$, with constants from the NIST WebBook.

A **simple distillation** gives one equilibrium stage: boil the liquid, condense the vapour, done. It is enough when the boiling points differ by more than about 100 °C (Nichols), or to separate a volatile liquid from a solid. A **fractional distillation** puts a column (packed or with indentations) between flask and condenser. Vapour condenses and re-boils many times on the way up; each cycle is one **theoretical plate**. At total reflux, the minimum number of plates to go from pot composition $x_B$ to distillate $x_D$ is the **Fenske equation**:

$$N_\text{min} = \frac{\ln\left[\dfrac{x_D}{1-x_D}\cdot\dfrac{1-x_B}{x_B}\right]}{\ln \alpha}$$

Real columns need more plates than $N_\text{min}$, and you must distil slowly so that each stage can reach equilibrium.

Two more tools. **Vacuum distillation** lowers the boiling point, for compounds that boil above about 150 °C or decompose when heated. **Azeotropes** are mixtures that boil without changing composition: ethanol and water boil together at about 78 °C with roughly 96 % ethanol, so no column can give pure ethanol from wine. Raoult's law fails for them.

Distillation safety: never heat a closed system; add boiling chips or stir; put the thermometer bulb level with the side arm so it reads the vapour that is leaving; never distil to dryness, because residues can overheat and ethers can leave explosive peroxides.

## Worked example

### 1. Recrystallise 2.00 g of acetanilide from water

PubChem: 1 g of acetanilide dissolves in 185 mL of cold water and in 20 mL of boiling water, so $s_\text{cold}$ = 0.0054 g/mL and $s_\text{hot}$ = 0.050 g/mL. Water is a good solvent: a ninefold difference, no reaction, and it boils at 100 °C, below the melting point of 114 °C, so no oiling out.

1. Minimum boiling water: $2.00 / 0.050 = 40$ mL.
2. Best possible recovery with 40 mL: $(2.00 - 0.0054 \times 40)/2.00 = 89\,\%$.
3. A practical 10 % excess (44 mL, so it does not crystallise during hot filtration) gives 88 %. Twice the minimum (80 mL) gives 78 %: one careless pour costs a tenth of the product.

Real recoveries are lower still, because some product is lost on the filter paper and in the cold wash.

### 2. How far does one boil get you? Cyclohexane and toluene

Cyclohexane boils at 80.7 °C and toluene at 110.6 °C, only 30 °C apart. With the NIST Antoine constants and Raoult's law, a 50:50 mixture boils at 92.8 °C and the first vapour is 71 % cyclohexane. Condense that and boil it again: 87.2 °C, vapour 86 %. The mean relative volatility is $\alpha$ = 2.42, so reaching 95 % cyclohexane needs

$$N_\text{min} = \frac{\ln[(0.95/0.05)(0.5/0.5)]}{\ln 2.42} = 3.3 \text{ plates}$$

A simple distillation (one plate) gives 71 %, not 95 %: use a fractionating column and distil slowly.

## Hands-on

What you need: the simulation, the [Module 24 lab folder](../../labs/module-24/) and, for Part D, 50 g of potassium alum (sold as "alum" in pharmacies and spice shops for pickling) or table sugar, a kitchen scale (1 g), two heat-proof glass jars, a kettle, an oven glove, a spoon, a coffee filter, a towel, safety glasses. Write Part D on the [lab report template](../../templates/lab-report.md). Time: about 2 hours of work, plus an overnight wait.

### Part A — virtual bench: recrystallisation and distillation (30 min)

[Simulation: Organic bench — techniques (recrystallisation and distillation)](../../simulations/organic-bench/index.html?preset=techniques)

1. Recrystallise crude acetanilide. First pick a solvent from the sim's solubility table. Then make three runs: minimum hot water and slow cooling; double the water; minimum water but straight into ice.
2. Try a solvent that boils above 114 °C and record what happens.
3. Distil a 50:50 cyclohexane–toluene mixture, once simply and once with the column, and read the head temperature and distillate composition.

How you know it worked: the slow run gives the best purity and close to 88 % recovery; double solvent lowers recovery; crash cooling gives small crystals with a lower melting point; the high-boiling solvent oils out. The simple distillation starts near 71 % cyclohexane; the column gives over 90 % in the first fraction.

### Part B — videos (20 min)

Watch MIT's [Video 9: Recrystallization](https://ocw.mit.edu/courses/res-5-0001-digital-lab-techniques-manual-spring-2007/resources/recrystallization/), [Video 7: Filtration](https://ocw.mit.edu/courses/res-5-0001-digital-lab-techniques-manual-spring-2007/resources/filtration/), and [Video 15: Distillation I](https://ocw.mit.edu/courses/res-5-0001-digital-lab-techniques-manual-spring-2007/resources/distillation-i-simple-fractional-distillations/). Optional: [Video 16: Distillation II, vacuum distillations](https://ocw.mit.edu/courses/res-5-0001-digital-lab-techniques-manual-spring-2007/resources/distillation-ii-vacuum-distillations/). Note where the thermometer bulb sits and how the crystals are washed.

### Part C — Python: recovery and a T–x–y diagram (20 min)

Complete `min_hot_volume()`, `max_recovery()`, `bubble_point()` and `fenske_plates()` in `lesson02_purification.py`, then run:

```bash
py lesson02_purification.py
```

How you know it worked: 40 mL; 89 %, 88 % and 78 % recovery; 92.8 °C and 71 %; 87.2 °C and 86 %; $\alpha$ = 2.42; 3.3 plates. `runs/lesson02_purification.png` shows the lens-shaped diagram with three stair steps.

<details><summary>Reference solution</summary>

```python
def max_recovery(mass_g, volume_mL, s_cold):
    lost = volume_mL * s_cold
    return max(0.0, (mass_g - lost) / mass_g)

def bubble_point(x1, a="cyclohexane", b="toluene", P=P_ATM):
    f = lambda T: x1 * antoine_bar(a, T) + (1 - x1) * antoine_bar(b, T) - P
    T = brentq(f, 300.0, 420.0)
    return T, x1 * antoine_bar(a, T) / P

def fenske_plates(xD, xB, alpha):
    return math.log((xD / (1 - xD)) * ((1 - xB) / xB)) / math.log(alpha)
```

Full code: `lesson02_purification_solution.py`. The cyclohexane Antoine constants are fitted up to 355 K, so the toluene-rich end of the diagram extrapolates slightly.

</details>

### Part D — home: recrystallise alum (or sugar)

> [!WARNING]
> Water from a kettle scalds. An adult pours it, with an oven glove, into a heat-proof glass jar standing in the sink; do not use a stove and never heat sugar syrup. Wear safety glasses. Alum is an astringent salt: do not eat it or the crystals, keep it out of eyes (rinse with water if it gets in), and keep the jars away from children. Pour the solutions down the sink with plenty of water. Only alum or sugar, nothing else.

1. Weigh about 50 g of alum. Pour 100 mL of water just off the boil into the first jar. Add the alum a spoonful at a time, stirring, until it is all in or a little stays undissolved even after two minutes of stirring. Weigh what you did not add (and blot and weigh any undissolved residue) to find how much dissolved.
2. Pour the clear solution through a coffee filter into the second, pre-warmed jar (rinse it with hot water first). This is your hot gravity filtration.
3. Cover the jar with paper, wrap it in a towel, and leave it overnight to cool slowly. If you have enough alum, do a second, smaller batch cooled fast in a bowl of cold water and compare.
4. Next day pour off the mother liquor, dry the crystals on paper towel for a day, and weigh them. Enter the run in a copy of `alum_recrystallisation_template.csv` named `alum_recrystallisation.csv` and rerun the Python script.

How you know it worked: the slowly cooled jar grows fewer, larger, clear octahedral crystals; the fast batch gives many small ones. The script compares your recovery with the limit set by about 1 g per 20 mL of cold water (PubChem); 50–75 % is typical, below the limit because crystals stay wet and some stick to the jar. Optional: tie the best small crystal to a thread and hang it in fresh saturated solution for a week to grow a single large crystal.

With sugar instead: dissolve as much as you can in 100 mL of hot water (about 200 g). On cooling, almost nothing crystallises in a day, because sugar is very soluble even when cold (PubChem: 1 g in 0.5 mL). Crystals ("rock candy") grow only as the water evaporates over a week. This is the lesson: a good recrystallisation solvent needs a large difference between hot and cold solubility.

## Common mistakes

- **Too much solvent.** Recovery falls fast. If it happens, boil some off and cool again.
- **Cooling too fast.** Small, impure crystals; let the flask reach room temperature before the ice bath.
- **A solvent that boils above the compound's melting point.** The product oils out. Choose a lower-boiling solvent or a two-solvent pair.
- **Washing crystals with warm solvent.** It redissolves the product; use a little ice-cold solvent.
- **Expecting one simple distillation to separate liquids 30 °C apart.** Use a column and distil slowly.
- **Distilling to dryness or with the thermometer in the wrong place.** Leave a residue in the flask; put the bulb level with the side arm.

## Key takeaways

- A recrystallisation solvent dissolves the compound well hot and poorly cold, keeps impurities in solution (or out of it), and boils below the compound's melting point.
- Minimum hot solvent, slow cooling, ice-cold wash; the best recovery is $(m - s_\text{cold}V)/m$.
- Raoult's law makes the vapour richer in the more volatile liquid; each boil–condense cycle is one theoretical plate, and the Fenske equation counts how many you need.
- Simple distillation is for boiling points far apart or a liquid from a solid; use a fractionating column for close boilers and vacuum for high-boiling or fragile compounds.
- Alum at home shows the same rules: slow cooling, big crystals; sugar shows why a small hot–cold difference makes a poor recrystallisation.

## Sources

- [MIT OCW RES.5-0001 Digital Lab Techniques Manual, Video 9: Recrystallization](https://ocw.mit.edu/courses/res-5-0001-digital-lab-techniques-manual-spring-2007/resources/recrystallization/) — one- and two-solvent methods; Videos 7, 15 and 16 on filtration and distillation.
- [MIT OCW RES.5-0001, Video 15: Distillation I](https://ocw.mit.edu/courses/res-5-0001-digital-lab-techniques-manual-spring-2007/resources/distillation-i-simple-fractional-distillations/) — simple and fractional distillation.
- [LibreTexts, Nichols, ch. 3 Crystallization](https://chem.libretexts.org/Bookshelves/Organic_Chemistry/Organic_Chemistry_Lab_Techniques_(Nichols)/03%3A_Crystallization) — solvent choice, oiling out, second crops.
- [LibreTexts, Nichols, ch. 5 Distillation](https://chem.libretexts.org/Bookshelves/Organic_Chemistry/Organic_Chemistry_Lab_Techniques_(Nichols)/05%3A_Distillation) — simple distillation for boiling points more than 100 °C apart; fractional, vacuum and steam distillation.
- [PubChem, Acetanilide (CID 904)](https://pubchem.ncbi.nlm.nih.gov/compound/904) — 1 g in 185 mL cold water, 20 mL boiling water; mp 114.3 °C.
- [PubChem, Potassium alum (CID 24856)](https://pubchem.ncbi.nlm.nih.gov/compound/24856) — about 1 g in 20 mL cold water, far more soluble hot. Sucrose solubility from [PubChem CID 5988](https://pubchem.ncbi.nlm.nih.gov/compound/5988).
- [NIST WebBook, Cyclohexane](https://webbook.nist.gov/cgi/cbook.cgi?ID=C110827&Mask=4) and [Toluene](https://webbook.nist.gov/cgi/cbook.cgi?ID=C108883&Mask=4) — Antoine constants (Williamham, Taylor et al. 1945) and boiling points.
