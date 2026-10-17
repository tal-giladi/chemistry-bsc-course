---
id: "07.6"
module: 7
minutes: 20
practice_minutes: 60
prerequisites: ["07.5", "02.5"]
objectives:
  - Use the ideal gas law with consistent units to find pressure, volume, amount or mass of a gas.
  - Calculate partial pressures from mole fractions with Dalton's law.
  - Calculate the compressibility factor Z from the van der Waals equation and from reference data, and explain why Z falls below or rises above 1.
  - Decide from Z whether the ideal gas law is good enough for a given pressure and temperature.
volatility: concept
sources:
  - title: "NIST — CODATA value of the molar gas constant"
    url: https://physics.nist.gov/cgi-bin/cuu/Value?r
  - title: "NIST Chemistry WebBook — Thermophysical Properties of Fluid Systems"
    url: https://webbook.nist.gov/chemistry/fluid/
  - title: "LibreTexts — A8: van der Waals Constants for Real Gases"
    url: https://chem.libretexts.org/Ancillary_Materials/Reference/Reference_Tables/Atomic_and_Molecular_Properties/A8%3A_van_der_Waal's_Constants_for_Real_Gases
  - title: "OpenStax Chemistry 2e, 9.2 Relating Pressure, Volume, Amount, and Temperature: The Ideal Gas Law"
    url: https://openstax.org/books/chemistry-2e/pages/9-2-relating-pressure-volume-amount-and-temperature-the-ideal-gas-law
  - title: "OpenStax Chemistry 2e, 9.3 Stoichiometry of Gaseous Substances, Mixtures, and Reactions"
    url: https://openstax.org/books/chemistry-2e/pages/9-3-stoichiometry-of-gaseous-substances-mixtures-and-reactions
  - title: "OpenStax Chemistry 2e, 9.6 Non-Ideal Gas Behavior"
    url: https://openstax.org/books/chemistry-2e/pages/9-6-non-ideal-gas-behavior
last_verified: "2026-10-17"
---

# 07.6 · Gases: ideal and real

A gas is mostly empty space with molecules flying through it, and that is why one simple equation describes almost every gas at room conditions. This lesson uses the ideal gas law and Dalton's law of partial pressures, then shows where they break down: at high pressure, molecules attract each other and take up room. You will measure how badly the ideal law fails for carbon dioxide, using real reference data from NIST and the van der Waals equation.

## Why it matters

Decaffeinated coffee and many natural flavours are extracted with carbon dioxide at about 100 to 300 bar and just above room temperature. An engineer sizing a 1 L test vessel for CO₂ at 120 bar and 320 K needs to know how much gas goes in. The ideal gas law says about 200 g. The vessel actually takes more than 600 g. A design based on the ideal law would order the wrong pump, the wrong cylinders and the wrong safety valve. At atmospheric pressure the same law is accurate to better than 1 %. Knowing which situation you are in, and how to correct for it, is the point of this lesson.

## Core ideas

> [!NOTE]
> The gas laws and the van der Waals model are stable ideas. The gas constant is the CODATA 2022 value from NIST (exact since the 2019 SI redefinition). The van der Waals constants are from the LibreTexts reference table, and the CO₂ data are from the NIST Chemistry WebBook fluid tables, all retrieved on 2026-10-17. Tables of $a$ and $b$ differ slightly between books because they are fitted in different ways.

### Pressure and its units

**Pressure** is force per area, $P = F/A$ ([Lesson 04.1](../module-04/lesson-01.md)). In a gas it comes from molecules hitting the walls. The SI unit is the pascal, 1 Pa = 1 N/m². Chemists also use the **bar** (1 bar = 10⁵ Pa exactly) and the **standard atmosphere** (1 atm = 101 325 Pa = 1.01325 bar exactly). Weather maps use hectopascals: 1013 hPa is 1.013 bar.

### The ideal gas law

An **ideal gas** is a model: point-like molecules that never attract each other and only bounce off each other and the walls. For it,

$$PV = nRT$$

with $P$ the pressure, $V$ the volume, $n$ the amount in moles, $T$ the absolute temperature in kelvin and $R$ the **molar gas constant**:

$$R = 8.314\,462\,618\ \mathrm{J\,mol^{-1}\,K^{-1}} = 0.083\,144\,626\ \mathrm{L\,bar\,mol^{-1}\,K^{-1}}$$

Use one set of units throughout. With $P$ in bar and $V$ in litres, use the second value. With pascals and cubic metres, use the first. The temperature must be in kelvin: $T/\mathrm{K} = t/{}^\circ\mathrm{C} + 273.15$.

Tiny example: 1.000 mol at 273.15 K and 1 bar fills $V = nRT/P = 0.083145 \times 273.15 / 1 = 22.71$ L. This is the molar volume at IUPAC standard temperature and pressure. At 25 °C and 1 bar it is 24.79 L.

The older named laws are special cases: Boyle ($PV$ constant at fixed $n$, $T$), Charles ($V \propto T$ at fixed $n$, $P$) and Avogadro ($V \propto n$ at fixed $P$, $T$). Because $n = m/M$, the ideal gas law also gives the molar mass of an unknown gas from its density: $M = \rho RT/P$.

### Mixtures: Dalton's law

In a mixture of ideal gases, each gas behaves as if it were alone. Its **partial pressure** $p_i$ is the pressure it would have alone in the same volume. **Dalton's law** says the partial pressures add up to the total:

$$P = \sum_i p_i, \qquad p_i = x_i P$$

where $x_i = n_i/n_{\text{total}}$ is the **mole fraction** of gas $i$. Dry air is 78.08 % N₂, 20.95 % O₂ and 0.93 % Ar by moles, so at 1.013 bar the oxygen partial pressure is $0.2095 \times 1.013 = 0.212$ bar.

### Real gases and the compressibility factor

Real molecules do two things the ideal model ignores. They **attract** each other (the intermolecular forces of [Lesson 07.4](lesson-04.md)), which pulls them away from the walls and lowers the pressure. And they have a **size**, so the volume they can move in is less than the volume of the container.

The **compressibility factor** measures the total effect:

$$Z = \frac{PV_m}{RT}$$

where $V_m = V/n$ is the **molar volume**. For an ideal gas $Z = 1$ exactly. When $Z < 1$, attractions win and the gas is easier to compress than the ideal law says. When $Z > 1$, the size of the molecules wins. For most gases at room temperature, $Z$ falls below 1 as the pressure rises, reaches a minimum, and then climbs as the molecules are squeezed into contact.

### The van der Waals equation

Johannes van der Waals (1873) corrected the ideal gas law with two constants:

$$\left(P + \frac{a}{V_m^2}\right)\left(V_m - b\right) = RT$$

- $a$ (bar L² mol⁻²) measures the attractions. Attraction depends on how many neighbours each molecule has, which grows with density, so the correction grows as $1/V_m^2$. Polar and large molecules have large $a$: H₂O 5.537, CO₂ 3.658, N₂ 1.370, He 0.0346.
- $b$ (L mol⁻¹) is the volume excluded by one mole of molecules: CO₂ 0.04286, N₂ 0.0387, He 0.0238.

Tiny example: for CO₂ at 10 bar and 320 K, $V_m \approx 2.56$ L/mol, so $a/V_m^2 = 3.658/2.56^2 = 0.56$ bar (a 6 % correction to the pressure) and $b/V_m = 1.7$ %. The attraction term is bigger, so $Z < 1$. At low pressure both corrections vanish and the equation becomes $PV_m = RT$ again.

The van der Waals equation is a cubic in $V_m$. Below a certain temperature it predicts the gas–liquid transition, which makes it historically important, but its numbers are only rough near and above the critical point. Accurate work uses reference equations of state, such as the Span–Wagner equation behind the NIST tables for CO₂.

### When is "ideal" good enough?

As a rule of thumb, the ideal gas law is within about 1 % for common gases below a few bar at room temperature or above. Real-gas corrections matter at high pressure, at low temperature, near the boiling point and for strongly attracting molecules (water vapour, ammonia, CO₂). Compute $Z$ when in doubt.

## Worked example

### 1. How much CO₂ fits in the extraction vessel?

A 1.000 L vessel holds CO₂ at 120 bar and 320 K. Find the mass three ways.

**Ideal gas.**

$$n = \frac{PV}{RT} = \frac{120 \times 1.000}{0.083145 \times 320} = \frac{120}{26.606} = 4.51\ \text{mol}$$

$m = 4.51 \times 44.009 = 198$ g.

**Van der Waals.** Solve the cubic for $V_m$ (the lab script does it with `np.roots`): $V_m = 0.0868$ L/mol, so $n = 1.000/0.0868 = 11.5$ mol and $m = 507$ g.

**Reference data.** The NIST table gives $V_m = 0.06961$ L/mol at 120 bar and 320 K, so $n = 14.4$ mol and $m = 632$ g.

**Interpretation.** $Z_{\text{NIST}} = 120 \times 0.06961 / 26.606 = 0.314$. The gas is three times denser than the ideal law says, because CO₂ at this point is a dense supercritical fluid, close to a liquid. Van der Waals catches most of the effect but is still 20 % off. For design, use reference data.

### 2. Partial pressure on a dive

A diver breathes air at 30 m depth in the sea, where the total pressure is about 4.0 bar (1 bar of atmosphere plus about 1 bar per 10 m of sea water). What are the partial pressures of O₂ and N₂?

$$p(\mathrm{O_2}) = 0.2095 \times 4.0 = 0.84\ \text{bar}, \qquad p(\mathrm{N_2}) = 0.7808 \times 4.0 = 3.1\ \text{bar}$$

The diver's lungs see four times the oxygen and nitrogen partial pressures they see on the beach. The extra nitrogen dissolves in the blood, which is why divers must come up slowly. Air is still close to ideal at 4 bar ($Z$ of N₂ and O₂ differs from 1 by well under 1 %), so Dalton's law is accurate here.

## Hands-on

**What you need:** Python with the course packages and the [Module 7 lab folder](../../labs/module-07/); a calculator; paper. **Time:** about 60 minutes.

### Part A — the ideal gas in the simulation (15 min)

[Simulation: Gas laws — ideal gas](../../simulations/gas-laws/index.html?preset=ideal)

Task: keep $n$ and $T$ fixed and set five volumes; record the pressure each time. Then plot $P$ against $1/V$ (on paper or in Python). Target: a straight line through the origin with slope $nRT$. Read the slope and get $R$ back to within 2 %. Then double $T$ at fixed $V$ and check that $P$ doubles.

### Part B — a real gas in the simulation (10 min)

[Simulation: Gas laws — real gas (van der Waals)](../../simulations/gas-laws/index.html?preset=real)

Task: choose CO₂, set 320 K and raise the pressure from 1 to 150 bar. Note the pressure at which $Z$ is smallest. Then switch to helium at the same temperature and describe how its $Z$ differs. Target: a CO₂ minimum near 100 bar with $Z$ well below 0.5; for helium, $Z$ slightly above 1 everywhere, because its attractions are tiny and only its size counts.

### Part C — van der Waals against NIST data (35 min)

The file `co2_320K_nist.csv` holds the molar volume of CO₂ at 320 K and 1 to 150 bar from the NIST Chemistry WebBook.

1. Open `lesson06_real_gas.py` and complete `vdw_molar_volume()`: multiply out the van der Waals equation to the cubic $PV_m^3 - (Pb + RT)V_m^2 + aV_m - ab = 0$, solve it with `np.roots`, and return the largest real root.
2. Run it and open `runs/co2_z.png`:

```bash
py lesson06_real_gas.py
```

3. Answer in your notebook: (a) Up to what pressure is the ideal gas law within 5 % of the NIST volume? (b) Up to what pressure is van der Waals within 2 %? (c) Above 100 bar, does van der Waals over- or underestimate $V_m$, and which of its two constants would you blame?

**How you know it worked:** the table shows $Z_{\text{NIST}} = 0.996$ at 1 bar, 0.771 at 50 bar and a minimum of 0.314 at 120 bar; van der Waals gives 0.785 at 50 bar and stays within about 0.1 of NIST everywhere.

<details><summary>Reference answers to step 3</summary>

(a) The ideal $V_m$ is $1/Z$ times the real one; $Z \ge 0.95$ holds only up to about 10 bar ($Z = 0.960$). (b) Van der Waals is within 2 % of NIST up to about 80 bar. (c) Above 100 bar it overestimates $V_m$ ($Z$ too high): its $b$ term treats the molecules as hard spheres that resist compression too early, and a single constant $a$ cannot follow how attractions change in a dense fluid. The reference code is `lesson06_real_gas_solution.py`:

```python
roots = np.roots([P, -(P * b + R * T), a, -a * b])
real = roots[np.abs(roots.imag) < 1e-9].real
return real.max()
```

</details>

### Part D — pencil check (optional, 10 min)

A 2.00 L flask holds 0.100 mol N₂ and 0.050 mol O₂ at 25 °C. Find the total pressure and the partial pressure of O₂.

<details><summary>Answer to Part D</summary>

$P = nRT/V = 0.150 \times 0.083145 \times 298.15 / 2.00 = 1.86$ bar. $x(\mathrm{O_2}) = 0.050/0.150 = 0.333$, so $p(\mathrm{O_2}) = 0.62$ bar.

</details>

## Common mistakes

- **Temperature in °C.** $PV = nRT$ needs kelvin. At 25 °C a Celsius value puts the answer off by a factor of about twelve.
- **Mixing units of $R$.** Pick the value of $R$ that matches your pressure and volume units, and write them out.
- **Using 22.4 L/mol everywhere.** That is the molar volume at 0 °C and 1 atm only; at 25 °C and 1 bar it is 24.8 L/mol.
- **Assuming a gas is ideal at high pressure.** Compute $Z$ or look up data for anything above a few bar, near condensation, or for polar gases.
- **Taking any root of the van der Waals cubic.** Below the critical temperature it can have three real roots; the largest is the gas, the smallest the liquid, and the middle one has no physical meaning.
- **Reading $Z < 1$ as "the gas has less volume because molecules are small".** $Z < 1$ means attractions dominate; size effects push $Z$ above 1.

## Key takeaways

- $PV = nRT$ with $R = 8.314\,462\,618$ J mol⁻¹ K⁻¹ (exact), temperature in kelvin and consistent units.
- Dalton: partial pressures add up, and $p_i = x_i P$.
- $Z = PV_m/RT$ measures non-ideality: below 1 attractions win, above 1 molecular size wins.
- Van der Waals adds an attraction term $a/V_m^2$ and an excluded volume $b$; it is qualitatively right but only roughly accurate at high density.
- For real design numbers use reference data such as the NIST fluid tables.

## Sources

- [NIST — CODATA value of the molar gas constant](https://physics.nist.gov/cgi-bin/cuu/Value?r) ($R$, CODATA 2022, exact; retrieved 2026-10-17).
- [NIST Chemistry WebBook — Thermophysical Properties of Fluid Systems](https://webbook.nist.gov/chemistry/fluid/) (CO₂ isotherm at 320 K, 1–150 bar, in `co2_320K_nist.csv`; retrieved 2026-10-17).
- [LibreTexts — A8: van der Waals Constants for Real Gases](https://chem.libretexts.org/Ancillary_Materials/Reference/Reference_Tables/Atomic_and_Molecular_Properties/A8%3A_van_der_Waal's_Constants_for_Real_Gases) ($a$ and $b$ for CO₂, N₂, He, H₂O; retrieved 2026-10-17).
- [OpenStax Chemistry 2e, 9.2 The Ideal Gas Law](https://openstax.org/books/chemistry-2e/pages/9-2-relating-pressure-volume-amount-and-temperature-the-ideal-gas-law) (gas laws, standard molar volume).
- [OpenStax Chemistry 2e, 9.3 Stoichiometry of Gaseous Substances, Mixtures, and Reactions](https://openstax.org/books/chemistry-2e/pages/9-3-stoichiometry-of-gaseous-substances-mixtures-and-reactions) (Dalton's law, mole fractions).
- [OpenStax Chemistry 2e, 9.6 Non-Ideal Gas Behavior](https://openstax.org/books/chemistry-2e/pages/9-6-non-ideal-gas-behavior) (compressibility factor, van der Waals equation).
