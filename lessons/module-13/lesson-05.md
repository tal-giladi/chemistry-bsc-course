---
id: "13.5"
module: 13
minutes: 22
practice_minutes: 70
prerequisites: ["13.4", "07.6"]
objectives:
  - Use the Gibbs phase rule to count the degrees of freedom at a point, on a line and at the triple point of a phase diagram.
  - Apply the Clapeyron equation to the melting line and the Clausius–Clapeyron equation to vapour-pressure and sublimation curves.
  - Read and build the phase diagrams of water and CO₂ from NIST data, and explain why their melting lines lean in opposite directions.
  - Predict and measure the boiling point of water at your local pressure.
volatility: concept
sources:
  - title: "NIST Chemistry WebBook: Water, phase change data"
    url: https://webbook.nist.gov/cgi/cbook.cgi?ID=C7732185&Mask=4
  - title: "NIST Chemistry WebBook: Carbon dioxide, phase change data"
    url: https://webbook.nist.gov/cgi/cbook.cgi?ID=C124389&Mask=4
  - title: "OpenStax Chemistry 2e, 10.4 Phase Diagrams"
    url: https://openstax.org/books/chemistry-2e/pages/10-4-phase-diagrams
  - title: "OpenStax Chemistry 2e, 10.3 Phase Transitions"
    url: https://openstax.org/books/chemistry-2e/pages/10-3-phase-transitions
  - title: "IAPWS: Revised Release on the IAPWS-95 formulation for water"
    url: https://www.iapws.org/relguide/IAPWS95-2018.pdf
  - title: "phyphox: sensors and barometer experiment"
    url: https://phyphox.org/sensors/
last_verified: "2026-10-17"
---

# 13.5 · Phase equilibria and phase diagrams

Why does a pressure cooker cook faster, why does tea brewed in Jerusalem taste weaker than tea brewed at the Dead Sea, and why does dry ice never melt into a puddle? All three are questions about which phase has the lowest chemical potential at a given temperature and pressure. This lesson turns the chemical potential of lesson 13.4 into the lines of a phase diagram, gives you the two equations that draw those lines from measured enthalpies, and asks you to test one of them on your own stove.

## Why it matters

Pharmaceutical companies freeze-dry vaccines by holding them below water's triple-point pressure, so ice turns straight into vapour without melting. Coffee is decaffeinated with supercritical CO₂, above its critical point, where it dissolves caffeine like a liquid but flows like a gas. A chemist who distils a solvent under reduced pressure must know at what temperature it will boil. Each decision needs a phase diagram and the ability to read and extend it.

## Core ideas

> [!NOTE]
> The phase rule and the Clapeyron equations are settled theory. Triple and critical points, transition enthalpies and Antoine vapour-pressure coefficients are from the NIST Chemistry WebBook phase-change pages (water's triple point from IAPWS), retrieved 2026-10-17. Antoine fits are valid only in the temperature range NIST lists for them.

### Phases, components and the phase rule

A **phase** is a region of uniform composition and properties: ice, liquid water, water vapour. A **component** is an independent chemical substance needed to describe the composition (one for pure water). Two phases are in equilibrium when the chemical potential of every component is the same in both. The **Gibbs phase rule** counts how many intensive variables you can still change freely:

$$F = C - P + 2$$

For a pure substance ($C = 1$): in a single-phase region $F = 2$ (choose $T$ and $p$ freely); on a coexistence line $F = 1$ (choose $T$ and $p$ follows); at the **triple point**, where three phases coexist, $F = 0$: one fixed $T$ and $p$. Water's triple point is 273.16 K and 611.657 Pa, which is why it was used to define the kelvin until 2019.

### Why phase lines exist: μ against T

From lesson [13.4](lesson-04.md), $(\partial\mu/\partial T)_p = -S_m$. Every phase's chemical potential falls as $T$ rises, and the gas, with the largest entropy, falls fastest. At low $T$ the solid has the lowest $\mu$; at higher $T$ the liquid's line crosses below it (melting); higher still the gas wins (boiling). Raising the pressure lifts each line by $V_m\,\Delta p$, most for the gas, so the boiling point rises with pressure.

### The Clapeyron equation

Along a coexistence line, $\mu_\alpha = \mu_\beta$, so $d\mu_\alpha = d\mu_\beta$ for a step along it. Writing $d\mu = V_m\,dp - S_m\,dT$ for each phase and using $\Delta S = \Delta H/T$ gives the **Clapeyron equation**:

$$\frac{dp}{dT} = \frac{\Delta_\text{trs}H}{T\,\Delta_\text{trs}V}$$

It holds for any phase change. For ice melting, $\Delta_\text{fus}H$ = 6.01 kJ/mol and $\Delta_\text{fus}V$ = 18.02 − 19.65 = −1.63 cm³/mol: liquid water is *denser* than ice. So

$$\frac{dp}{dT} = \frac{6010}{273.15 \times (-1.63\times10^{-6})} = -1.35\times10^{7}\ \text{Pa/K} = -135\ \text{bar/K}$$

The melting line of water leans to the left: pressure *lowers* the melting point, but only by 0.0074 K per bar. (A skate blade adds tens of bar, which lowers the melting point by well under 1 K, so pressure melting cannot be why ice is slippery at −10 °C.) For almost every other substance, including CO₂, the solid is denser, $\Delta V > 0$, and the melting line leans right.

### The Clausius–Clapeyron equation

For evaporation or sublimation, the vapour volume dwarfs the condensed one: $\Delta V \approx V_\text{gas} = RT/p$. Substituting into Clapeyron and integrating with constant $\Delta H$:

$$\ln\frac{p_2}{p_1} = -\frac{\Delta_\text{vap}H}{R}\left(\frac{1}{T_2} - \frac{1}{T_1}\right)$$

This is the **Clausius–Clapeyron equation**. A plot of $\ln p$ against $1/T$ is a straight line with slope $-\Delta_\text{vap}H/R$, the same shape as the van 't Hoff plot of lesson [08.3](../module-08/lesson-03.md), and for the same reason: evaporation is an equilibrium whose $K$ is the vapour pressure in bar. Real data bend slightly because $\Delta_\text{vap}H$ falls as $T$ rises (44.0 kJ/mol for water at 25 °C, 40.67 at 100 °C), which is why NIST gives **Antoine** fits, $\log_{10}p = A - B/(T + C)$, for accurate work.

### Reading a phase diagram

![Schematic phase diagram of water, pressure on a log scale against temperature. The solid–liquid line leans slightly left from the triple point at 273.16 K and 611.657 Pa; the liquid–vapour line rises to the critical point at 647.1 K and 220.6 bar; the solid–vapour line falls below the triple point. A dashed 1 atm line meets melting at 0 °C and boiling at 100 °C.](../../assets/m13-phase-diagram.svg)

Three ideas let you read any one-component diagram:

- **Normal melting and boiling points** are where the 1 atm line crosses the solid–liquid and liquid–vapour lines.
- Below the **triple-point pressure**, the liquid cannot exist: the solid sublimes. Water's is tiny (0.006 bar), so only freeze-dryers and comets care. CO₂'s is **5.185 bar**, above atmospheric, so dry ice at 1 atm sublimes at −78.5 °C and never melts.
- The liquid–vapour line stops at the **critical point** (water 647.1 K and 220.6 bar; CO₂ 304.18 K and 73.80 bar). Above it, liquid and gas are no longer distinct: a **supercritical fluid**. You met the van der Waals equation in lesson [07.6](../module-07/lesson-06.md); its constants can be fixed from the critical point alone, $a = 27R^2T_c^2/64p_c$ and $b = RT_c/8p_c$.

## Worked example

### 1. Boiling water in Jerusalem and at the Dead Sea

Jerusalem sits about 800 m above sea level, with a typical station pressure of 0.92 bar. Use Clausius–Clapeyron from the normal boiling point (373.12 K at 1.01325 bar) with $\Delta_\text{vap}H$ = 40.67 kJ/mol:

$$\frac{1}{T_2} = \frac{1}{373.12} - \frac{8.3145}{40\,670}\ln\frac{0.92}{1.01325} = 0.0026801 + 0.0000197 = 0.0026998\ \text{K}^{-1}$$

$T_2$ = 370.4 K = 97.2 °C. The NIST Antoine equation gives 97.3 °C. On the Dead Sea shore, about 430 m below sea level at roughly 1.06 bar, the same calculation gives 101.3 °C. Four degrees between two places an hour's drive apart: enough to change cooking times for eggs and pasta.

### 2. Dry ice at 1 atm, from the triple point alone

CO₂'s triple point is 216.58 K and 5.185 bar, and NIST lists $\Delta_\text{sub}H$ ≈ 26.1 kJ/mol near 207 K. What is its sublimation pressure at −78.5 °C (194.65 K)?

$$\ln\frac{p}{5.185} = -\frac{26\,100}{8.3145}\left(\frac{1}{194.65} - \frac{1}{216.58}\right) = -3139 \times 5.20\times10^{-4} = -1.633$$

$p = 5.185 \times e^{-1.633} = 1.01$ bar. One atmosphere: that is exactly why dry ice sits at −78.5 °C in open air. The NIST Antoine fit to Giauque and Egan's 1937 measurements gives 1.006 bar.

## Hands-on

What you need: a saucepan, tap water, a cup of ice water, a digital kitchen thermometer (0.1 °C display), your phone with a barometer app such as [phyphox](https://phyphox.org/sensors/) (many phones have a pressure sensor; if yours does not, use the *station* pressure from a nearby weather station, not the sea-level pressure most weather apps show), the [Module 13 lab folder](../../labs/module-13/) with Python 3.14, and your notebook. Time: about 70 minutes.

### Part A — home: your local boiling point (30 min)

> [!WARNING]
> Boiling water and steam scald. Use a pan on a back burner with the handle turned inwards, keep children and pets away, and keep the thermometer cable and your sleeves away from the flame or hot plate. Hold the probe in the water, not touching the pan, and do not lean over the pan. Let everything cool before you clean up.

1. **Check the thermometer.** Fill a cup with crushed ice and a little cold water, stir for a minute and read the thermometer. It should read 0.0 °C; record the offset (for example, +0.3 °C means it reads 0.3 too high).
2. **Measure the pressure.** Open the barometer in phyphox (or note the station pressure) and record it in hPa (1 hPa = 0.001 bar).
3. **Boil.** Bring about 1 L of plain water (no salt) to a steady, rolling boil. Hold the probe tip 2–3 cm under the surface, away from the bottom. Record the reading every 30 s for 3 minutes; take the steady value.
4. Correct the reading with your offset. Put your pressure into `P_HOME_BAR` in `lesson05_phase_diagram.py` and compare with its prediction.

How you know it worked: the readings are steady within about 0.2 °C during a rolling boil, and your corrected value agrees with the prediction within the thermometer's accuracy (typically ±0.5 to ±1 °C; check its manual). At sea level expect 99.5–100.5 °C; in Jerusalem about 97 °C.

<details><summary>If your result is off</summary>

A reading 1–2 °C high usually means the probe touched the hot bottom of the pan; one that keeps rising means the water is not yet boiling everywhere. Salt or sugar in the water raises the boiling point (lesson 13.6). A cheap thermometer can be accurate at 0 °C and still off at 100 °C; that is a calibration slope error, which a single ice-point check cannot catch. The honest report says so.

</details>

### Part B — Python: two phase diagrams from NIST data (25 min)

Open `lesson05_phase_diagram.py` and write the three TODO functions: `clausius_clapeyron_p`, `clapeyron_slope` and `boiling_point` (solve the Antoine equation for $T$ with `brentq`). Then run:

```bash
py lesson05_phase_diagram.py
```

How you know it worked: it prints a melting slope of −135 bar/K for water, a boiling point of 100.00 °C at 1.01325 bar and 97.32 °C at 0.92 bar, a CO₂ sublimation pressure at −78.5 °C of 1.013 bar (Clausius–Clapeyron) and 1.006 bar (Antoine), an average $\Delta_\text{vap}H$ of CO₂ of 16.6 kJ/mol from the triple and critical points (NIST lists 16.4–16.7), and van der Waals constants for CO₂ of $a$ = 3.66 L² bar mol⁻² and $b$ = 0.0428 L/mol. Compare these with the table values you used in lesson 07.6. The plot `runs/lesson05_phase_diagrams.png` shows both diagrams side by side. Record your boiling-point result on a [notebook page](../../templates/notebook-page.md).

<details><summary>Reference solution</summary>

`clausius_clapeyron_p`: `return p1 * math.exp(-dh_kj * 1000 / R * (1 / t - 1 / t1))`. `clapeyron_slope`: `return dh_kj * 1000 / (t * dv_cm3 * 1e-6) / 1e5`. `boiling_point`: `a, b, c = BOIL` then `return brentq(lambda t: 10 ** (a - b / (t + c)) - p_bar, 340.0, 380.0)`. Full code in `lesson05_phase_diagram_solution.py`.

</details>

### Part C — simulation: approaching the critical point (15 min)

[Simulation: Gas laws — real gas (van der Waals)](../../simulations/gas-laws/index.html?preset=real)

Choose CO₂. Plot isotherms at 280 K, 300 K, 304 K and 320 K. Below the critical temperature, find the flat (two-phase) part of the isotherm and read the pressure there: it is the vapour pressure at that temperature. At 304 K the flat part shrinks to a single point. Above it, no compression produces a liquid. Note the van der Waals critical pressure the simulation reports and compare with NIST's 73.80 bar.

## Common mistakes

- **Celsius in $1/T$.** Clausius–Clapeyron needs kelvin; using °C gives nonsense, often a negative pressure ratio.
- **Using Clausius–Clapeyron for melting.** Its $\Delta V \approx RT/p$ step only works when one phase is a gas. For solid–liquid lines use the full Clapeyron equation.
- **Weather-app pressure.** Most apps report pressure corrected to sea level. Boiling depends on the actual pressure where you are.
- **Using an Antoine fit far outside its range.** Each NIST set lists the temperatures it was fitted to; mixing ranges at their edges can leave small jumps.
- **Assuming every substance behaves like water.** Water's negative melting slope is the exception; CO₂ and almost all others have a positive one.

## Key takeaways

- Phase rule $F = C - P + 2$: two free variables in a region, one on a line, none at the triple point.
- Clapeyron: $dp/dT = \Delta H/(T\Delta V)$. Water's melting line has slope −135 bar/K because ice is less dense than liquid water.
- Clausius–Clapeyron: $\ln(p_2/p_1) = -(\Delta_\text{vap}H/R)(1/T_2 - 1/T_1)$, for equilibria with a gas.
- CO₂ sublimes at 1 atm because its triple-point pressure (5.185 bar) is above atmospheric; Clausius–Clapeyron from the triple point predicts −78.5 °C at 1.01 bar.
- Water boils at about 97 °C in Jerusalem and 101 °C at the Dead Sea; you can measure it with a kitchen thermometer and a phone.

## Sources

- [NIST Chemistry WebBook: Water, phase change data](https://webbook.nist.gov/cgi/cbook.cgi?ID=C7732185&Mask=4) — Antoine coefficients (Bridgeman and Aldrich; Liu and Lindsay), critical pressure 220.64 bar.
- [NIST Chemistry WebBook: Carbon dioxide, phase change data](https://webbook.nist.gov/cgi/cbook.cgi?ID=C124389&Mask=4) — triple point 216.58 K and 5.185 bar, critical point 304.18 K and 73.80 bar, $\Delta_\text{sub}H$, $\Delta_\text{vap}H$, sublimation Antoine fit.
- [OpenStax Chemistry 2e, 10.4 Phase Diagrams](https://openstax.org/books/chemistry-2e/pages/10-4-phase-diagrams) — reading phase diagrams of water and CO₂, supercritical fluids.
- [OpenStax Chemistry 2e, 10.3 Phase Transitions](https://openstax.org/books/chemistry-2e/pages/10-3-phase-transitions) — Clausius–Clapeyron forms; $\Delta_\text{fus}H$ = 6.01 and $\Delta_\text{vap}H$ = 40.67 kJ/mol for water.
- [IAPWS-95 release](https://www.iapws.org/relguide/IAPWS95-2018.pdf) — the reference formulation for water's thermodynamic properties, including its triple and critical points.
- [phyphox sensors](https://phyphox.org/sensors/) — which phone sensors (including the barometer) the free app can read.
