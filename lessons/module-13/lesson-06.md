---
id: "13.6"
module: 13
minutes: 24
practice_minutes: 120
prerequisites: ["13.5", "13.4", "08.4"]
objectives:
  - Write the chemical potential of a solvent and a solute with activities, and name the standard state behind each.
  - Derive the freezing-point constant of water from its enthalpy of fusion and use a measured freezing point to get the activity of water.
  - Calculate ionic strength and a Debye–Hückel activity coefficient, and show how it shifts an apparent equilibrium constant.
  - Build a thermodynamic data sheet (ΔH, ΔS, ΔG, K and equilibrium conversion against T) for a real reaction from NIST data and check it against an independent table.
volatility: concept
sources:
  - title: "OpenStax Chemistry 2e, 11.4 Colligative Properties"
    url: https://openstax.org/books/chemistry-2e/pages/11-4-colligative-properties
  - title: "LibreTexts, Debye–Hückel theory (supplemental module)"
    url: https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Supplemental_Modules_%28Physical_and_Theoretical_Chemistry%29/Physical_Properties_of_Matter/Solutions_and_Mixtures/Nonideal_Solutions/Debye-Huckel
  - title: "OpenStax Chemistry 2e, Appendix H: Ionization Constants of Weak Acids"
    url: https://openstax.org/books/chemistry-2e/pages/h-ionization-constants-of-weak-acids
  - title: "MIT OpenCourseWare 5.60 Thermodynamics and Kinetics (Spring 2008), lecture notes"
    url: https://ocw.mit.edu/courses/5-60-thermodynamics-kinetics-spring-2008/pages/lecture-notes/
  - title: "NIST-JANAF Thermochemical Tables (Chase 1998), online edition"
    url: https://janaf.nist.gov/
last_verified: "2026-10-17"
---

# 13.6 · Solutions, activity and equilibrium constants

Every equilibrium constant you have used so far was written with concentrations or partial pressures, as if molecules ignored each other. Real ions in salt water attract and screen each other, and real molecules in a mixture are not indifferent to their neighbours. Thermodynamics handles this with one idea, activity: an "effective concentration" that makes the equations of lesson 13.4 exact again. This lesson introduces activity, shows how to measure it with a freezer and a kitchen thermometer, and ends with the module practical, a full thermodynamic data sheet for a real industrial reaction built from NIST tables.

## Why it matters

Seawater is about 0.5 mol/kg salt. A geochemist predicting whether calcium carbonate dissolves in it, a pharmacist checking whether a drug stays dissolved in saline, and a process engineer reading a pH meter in brine all meet the same problem: the textbook $K$ is defined in activities, and at this ionic strength activities differ from concentrations by 20–40 %. Ignore it and a predicted solubility can be off by a factor of two. The same mathematics explains why salt lowers the freezing point of water, which you will measure.

## Core ideas

> [!NOTE]
> Activity, standard states and the colligative relations are settled theory. $K_f$ = 1.86 K kg/mol for water (OpenStax Chemistry 2e Table 11.2) and the Debye–Hückel constant 0.509 (water, 25 °C, LibreTexts) were checked 2026-10-17. Thermochemical data are from the NIST WebBook and NIST-JANAF, as in lessons 13.2 and 13.4. The limiting law holds only in dilute solutions (ionic strength below about 0.01); better models (extended Debye–Hückel, Pitzer) are beyond this course.

### Partial molar quantities

In a mixture, each component's contribution to an extensive property depends on its neighbours. The **partial molar volume** $V_i = (\partial V/\partial n_i)_{T,p,n_{j\ne i}}$ is how much the volume grows when you add a little of $i$. Mix 50 mL of ethanol with 50 mL of water and you get less than 100 mL, because each molecule packs differently among the other kind. The chemical potential $\mu_i$ of lesson [13.4](lesson-04.md) is the partial molar Gibbs energy, and everything below is about how $\mu_i$ depends on composition.

### Ideal solutions: Raoult and Henry

In an **ideal solution** all molecules interact equally, and the chemical potential of each component has the same form as for an ideal gas, with mole fraction $x_i$ in place of pressure:

$$\mu_i = \mu_i^* + RT\ln x_i$$

where $\mu_i^*$ is the pure liquid. It follows that the vapour pressure of each component is **Raoult's law**, $p_i = x_i p_i^*$. For a dilute solute, a different straight line holds: **Henry's law**, $p_i = K_H x_i$, with a constant $K_H$ that reflects how the solute feels surrounded by solvent. You used Henry's law for CO₂ in sparkling water in lesson [08.3](../module-08/lesson-03.md).

### Activity and standard states

For a real solution, keep the same form and define the **activity** $a_i$ so that it is exact:

$$\mu_i = \mu_i^\circ + RT\ln a_i, \qquad a_i = \gamma_i\,\frac{c_i}{c^\circ}\ \text{or}\ \gamma_i x_i$$

$\gamma_i$ is the **activity coefficient**; $\gamma_i = 1$ means ideal. What $a = 1$ means depends on the **standard state** you choose, and every $K$ table assumes one:

| Species | Standard state ($a = 1$) | Activity in practice |
|---|---|---|
| gas | ideal gas at $p^\circ$ = 1 bar | $p_i/p^\circ$ (fugacity at high pressure) |
| solvent | pure liquid | $\gamma x$, close to 1 in dilute solution |
| solute | ideal 1 mol/kg (or 1 mol/L) solution | $\gamma\,m/m^\circ$ |
| pure solid or liquid | the pure phase | 1 |

That last row is why solids drop out of $K$ expressions: they have activity 1, not "concentration 1".

### Freezing-point depression from chemical potential

Ice and the liquid coexist where $\mu(\text{ice}) = \mu(\text{water in solution}) = \mu^*(\text{liquid}) + RT\ln a_w$. A solute lowers $a_w$, so the liquid's $\mu$ drops and the crossing with ice moves to a lower temperature. Using the Gibbs–Helmholtz equation from lesson 13.4:

$$\ln a_w = -\frac{\Delta_\text{fus}H}{R}\left(\frac{1}{T_f} - \frac{1}{T_f^*}\right)$$

For a dilute ideal solution, $\ln a_w \approx -\nu m M_w$ (with $M_w$ = 0.018015 kg/mol, $m$ the molality, $\nu$ ions per formula unit), and the equation simplifies to

$$\Delta T_f = K_f\,\nu\,m, \qquad K_f = \frac{R\,{T_f^*}^2 M_w}{\Delta_\text{fus}H} = \frac{8.3145 \times 273.15^2 \times 0.018015}{6010} = 1.86\ \text{K kg mol}^{-1}$$

The table value of $K_f$ is not a separate measurement; it follows from water's enthalpy of fusion. Real NaCl solutions freeze a little less than this predicts: even at 0.05 mol/kg, NaCl behaves as if it gave 1.9 particles, not 2 (OpenStax). The ratio of measured to ideal is the **osmotic coefficient** $\phi$, a direct measure of non-ideality.

### Ions: ionic strength and Debye–Hückel

Each ion is surrounded by a cloud of ions of the opposite charge, which lowers its chemical potential: $\gamma < 1$. The effect depends on the **ionic strength**

$$I = \tfrac{1}{2}\sum_i m_i z_i^2$$

and, in dilute water at 25 °C, the **Debye–Hückel limiting law** gives the mean activity coefficient of a salt:

$$\log_{10}\gamma_\pm = -0.509\,|z_+z_-|\sqrt{I}$$

For 0.010 mol/kg NaCl, $I = 0.010$ and $\gamma_\pm = 10^{-0.0509} = 0.89$. For MgSO₄ at the same molality, $I = 0.040$ and $\gamma_\pm = 10^{-0.509 \times 4 \times 0.2} = 0.39$ (already past the limiting law's range, so only a rough value). Doubly charged ions are far from ideal even when dilute.

### Thermodynamic K is written in activities

$\Delta_r G^\circ = -RT\ln K$ is exact only with activities:

$$K = \prod_i a_i^{\nu_i}$$

The concentration ratio you measure, $K_c$, then varies with ionic strength while $K$ stays fixed. That is why careful acid–base work (lesson [08.4](../module-08/lesson-04.md)) controls ionic strength, and why lesson 13.4's gas-phase $K$ uses $p_i/p^\circ$, which is the activity of an ideal gas.

## Worked example

### 1. What will the freezer show?

You dissolve 5.84 g of NaCl (58.44 g/mol, 0.0999 mol) in 200 g of water: $m$ = 0.500 mol/kg, $\nu$ = 2. Ideal prediction: $\Delta T_f = 1.86 \times 2 \times 0.500 = 1.86$ K, so the solution should freeze at −1.86 °C. Suppose you measure −1.70 °C relative to pure water. Then

$$\phi = \frac{1.70}{1.86} = 0.91, \qquad \ln a_w = -\frac{6010}{8.3145}\left(\frac{1}{271.45} - \frac{1}{273.15}\right) = -0.0166, \quad a_w = 0.9836$$

Raoult's law with full dissociation gives $x_w = 55.51/(55.51 + 1.00) = 0.9823$. The measured water activity is slightly *higher* than ideal: the ions hold each other back and act like fewer particles, which is the same non-ideality that makes $\gamma_\pm < 1$.

### 2. Acetic acid in salt water

Acetic acid has $K_a = 1.8\times10^{-5}$ (OpenStax Appendix H), defined in activities: $K_a = a_{\mathrm{H^+}}a_{\mathrm{A^-}}/a_{\mathrm{HA}}$. In 0.010 mol/kg NaCl, $\gamma_\pm = 0.89$ for the two ions, and the neutral acid has $\gamma \approx 1$. The concentration ratio you would measure is

$$K_c = \frac{[\mathrm{H^+}][\mathrm{A^-}]}{[\mathrm{HA}]} = \frac{K_a}{\gamma_\pm^2} = \frac{1.8\times10^{-5}}{0.79} = 2.3\times10^{-5}$$

The acid looks about 27 % stronger in salt water. The thermodynamic constant has not changed; the ions are stabilised by their ionic atmosphere, so more of them form.

## Hands-on

This is the module's practical piece. It uses the first law and heat capacities (13.1–13.2), entropy (13.3), Gibbs energy and $K$ (13.4), phase equilibrium (13.5) and activity (this lesson).

What you need: two small plastic cups, table salt (plain, no additives if possible), a kitchen scale (0.01 g pocket scale best), a digital kitchen thermometer, a freezer, a timer, the [Module 13 lab folder](../../labs/module-13/) with Python 3.14, and the [lab report template](../../templates/lab-report.md). Time: about 2 hours, most of it waiting for the freezer.

### Part A — home: freezing point of salt water (90 min, mostly waiting)

> [!CAUTION]
> Use only table salt and tap water, in plastic cups, and label them so nobody drinks or eats them. Do not put glass in the freezer with liquid in it. Clean the thermometer probe before it touches food again.

1. Weigh 200 g of tap water into each cup. Into cup 2 dissolve 5.84 g of salt (0.50 mol/kg); stir until clear.
2. Put both cups in the freezer side by side. Every 2 minutes, read the temperature of each (open the door briefly, stir gently with the probe, read, close). Record time and both readings.
3. Watch for the jump: the liquid cools below its freezing point without freezing (supercooling), then ice suddenly forms and the reading jumps *up* to the freezing point. Pure water then stays flat at 0 °C until frozen through; the salt water keeps drifting down slowly, because ice removes water and the remaining liquid gets saltier.
4. Stop when both cups have passed their plateau. Save the readings as `my_freezing.csv` with the header `sample,t_min,T_C` and the sample names `water` and `salt_0.50m` (see `freezing_example.csv`).

How you know it worked: both curves show a clear jump after supercooling; the pure-water plateau is within your thermometer's offset of 0 °C; the salt water starts its plateau about 1.6–1.9 °C below the pure water. Use the *difference* between the two cups: the thermometer's offset cancels.

### Part B — Python: the data sheet (30 min)

Open `lesson06_practical.py` and write the three TODO functions: `kf_from_fusion`, `water_activity` and `wgs_conversion`. The rest is already wired up with `thermo13.py`, which you know from lessons 13.2 and 13.4. Run it on the example data and then on yours:

```bash
py lesson06_practical.py
py lesson06_practical.py my_freezing.csv
```

The first part is a data sheet for the **water-gas shift**, $\mathrm{CO + H_2O(g) \rightleftharpoons CO_2 + H_2}$, the step that makes hydrogen from synthesis gas. In lesson 08.3 you estimated $K$ = 0.91 at 1000 K assuming constant $\Delta H$ and $\Delta S$.

How you know it worked: the table lists, from 500 to 1200 K, $\Delta_r H$ (−39.8 to −32.8 kJ/mol), $\Delta_r S$, $\Delta_r G$ (crossing zero near 1100 K), and $K$ from NIST data matching the JANAF column within 1 % (1.44 at 1000 K, 9.42 at 700 K). The constant-$\Delta H$ column gives 0.90 at 1000 K, as in Module 8. The CO conversion falls from 0.92 at 500 K to 0.55 at 1000 K for a 1 : 1 feed, and rises to 0.80 at 1000 K with three moles of steam. On the example freezing data it reports $K_f$ = 1.860, $\Delta T_f$ = 1.70 K, $\phi$ = 0.91 and $a_w$ = 0.9836. The plot `runs/lesson06_practical.png` shows $K(T)$ and your freezing curves.

<details><summary>Reference solution</summary>

`kf_from_fusion`: `return R * tf**2 * m_solvent / dh_fus`. `water_activity`: `t = tf - delta_tf` then `return math.exp(-dh_fus / R * (1 / t - 1 / tf))`. `wgs_conversion`: `return brentq(lambda x: x * x - k * (1 - x) * (steam_ratio - x), 0.0, min(1.0, steam_ratio))`. Full code in `lesson06_practical_solution.py`.

</details>

### Part C — write it up (30 min)

Use the [lab report template](../../templates/lab-report.md). Answer in the discussion:

1. At 1000 K the Module 8 estimate of $K$ was 0.90 and the full NIST value is 1.44. Which approximation caused the difference, and in which direction did each of $\Delta H$ and $\Delta S$ move between 298 K and 1000 K?
2. Real shift reactors run in two stages, about 600–700 K and about 470–520 K. Use your table to explain why the second, cooler stage exists, and what limits how cool it can be.
3. Your measured $\phi$ for salt water: is it below 1, as expected, and is the difference from 1 larger than your uncertainty (thermometer resolution and the spread of plateau readings)?

<details><summary>Hints for the discussion</summary>

1. $\Delta_r C_p$ of the shift is positive, so $\Delta_r H$ becomes less negative with $T$ (−41.2 to −34.8 kJ/mol) and $\Delta_r S$ less negative (−42.0 to −31.8). The entropy change dominates: $-T\Delta S$ is 10 kJ/mol smaller in magnitude at 1000 K, which more than offsets the weaker $\Delta H$, so $K$ is larger than the estimate.
2. The reaction is exothermic, so $K$ and the conversion rise as $T$ falls (0.98 at 600 K with 1 : 3 steam). The limit is kinetic: below roughly 470 K the catalyst becomes too slow, and steam must not condense.
3. With 0.1 °C resolution, the difference of two readings is uncertain by about ±0.1–0.15 K, so $\Delta T_f$ = 1.70 ± 0.15 K gives $\phi$ = 0.91 ± 0.08. You can say $\phi < 1$ only with a better thermometer or several repeats; say so plainly.

</details>

## Common mistakes

- **Treating $K_c$ as a constant at high ionic strength.** Only the activity-based $K$ is constant; $K_c$ drifts with ionic strength.
- **Applying the Debye–Hückel limiting law to seawater.** It is good below about 0.01 mol/kg; at 0.5 mol/kg it is badly wrong.
- **Forgetting $\nu$.** NaCl gives two particles per formula unit, CaCl₂ three. A colligative calculation without $\nu$ is off by that factor.
- **Reading the salt-water freezing point at the end of the plateau.** The liquid gets saltier as ice forms, so its temperature drifts down. Use the start of the plateau.
- **Mixing standard states.** A $K$ built from mol/L data with a $\Delta_r G^\circ$ based on 1 mol/kg or on 1 atm is slightly inconsistent; say which one you use.

## Key takeaways

- Real solutions: $\mu_i = \mu_i^\circ + RT\ln a_i$, with $a = \gamma \times$ (concentration over its standard value). Pure solids and liquids have $a = 1$.
- $K_f = R{T_f^*}^2M/\Delta_\text{fus}H$ = 1.86 K kg/mol for water; a measured freezing point gives the activity of water directly.
- Ionic strength $I = \tfrac12\sum m_iz_i^2$; dilute water at 25 °C: $\log\gamma_\pm = -0.509|z_+z_-|\sqrt I$.
- Thermodynamic $K$ is written in activities; concentration ratios shift with ionic strength.
- From NIST $\Delta_f H^\circ$, $S^\circ$ and $C_p(T)$ you can build a complete data sheet for any gas reaction and check it against JANAF: for the water-gas shift, $K$(1000 K) = 1.44, not the 0.90 of the constant-$\Delta H$ shortcut.

## Sources

- [OpenStax Chemistry 2e, 11.4 Colligative Properties](https://openstax.org/books/chemistry-2e/pages/11-4-colligative-properties) — Raoult's law, $K_f$ = 1.86 K kg/mol, van 't Hoff factor of 1.9 for 0.050 m NaCl.
- [LibreTexts, Debye–Hückel theory](https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Supplemental_Modules_%28Physical_and_Theoretical_Chemistry%29/Physical_Properties_of_Matter/Solutions_and_Mixtures/Nonideal_Solutions/Debye-Huckel) — limiting law with $A$ = 0.509 for water at 25 °C, ionic strength.
- [OpenStax Chemistry 2e, Appendix H](https://openstax.org/books/chemistry-2e/pages/h-ionization-constants-of-weak-acids) — $K_a$ of acetic acid.
- [MIT OpenCourseWare 5.60, lecture notes](https://ocw.mit.edu/courses/5-60-thermodynamics-kinetics-spring-2008/pages/lecture-notes/) — chemical potential in solutions, ideal and real solutions, colligative properties, equilibrium in solution.
- [NIST-JANAF Thermochemical Tables](https://janaf.nist.gov/) — $\log K_f$ of CO, CO₂ and H₂O(g) used to check the water-gas shift data sheet.
