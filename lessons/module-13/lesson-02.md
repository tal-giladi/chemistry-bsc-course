---
id: "13.2"
module: 13
minutes: 22
practice_minutes: 60
prerequisites: ["13.1", "02.3", "08.1"]
objectives:
  - Convert between ΔU and ΔH for a reaction with ΔH = ΔU + Δn_gas RT, and say which one a bomb and a coffee-cup calorimeter measure.
  - Calibrate a bomb calorimeter with benzoic acid and use it to find the molar combustion energy of an unknown.
  - Evaluate Cp(T) from NIST Shomate coefficients and explain why Cp of a gas rises with temperature.
  - Use Kirchhoff's law to move a reaction enthalpy from 298 K to another temperature, and judge when a constant ΔCp is good enough.
volatility: concept
sources:
  - title: "MIT OpenCourseWare 5.60 Thermodynamics and Kinetics (Spring 2008), lecture notes"
    url: https://ocw.mit.edu/courses/5-60-thermodynamics-kinetics-spring-2008/pages/lecture-notes/
  - title: "NIST SRM 39j Benzoic Acid (calorimetric standard), certificate"
    url: https://tsapps.nist.gov/srmext/certificates/39J.pdf
  - title: "NIST Chemistry WebBook: Sucrose, condensed phase thermochemistry"
    url: https://webbook.nist.gov/cgi/cbook.cgi?ID=C57501&Mask=2
  - title: "NIST Chemistry WebBook: Ammonia, gas phase thermochemistry (Shomate equation)"
    url: https://webbook.nist.gov/cgi/cbook.cgi?ID=C7664417&Mask=1
  - title: "NIST Chemistry WebBook: Benzoic acid, condensed phase thermochemistry"
    url: https://webbook.nist.gov/cgi/cbook.cgi?ID=C65850&Mask=2
last_verified: "2026-10-17"
---

# 13.2 · Enthalpy, heat capacity and calorimetry

In lesson 08.1 you treated enthalpy as "heat at constant pressure" and took one number from a table at 25 °C. This lesson shows why that works, how it differs from the internal energy measured in a sealed steel bomb, and how to move a reaction enthalpy to the temperature where a reactor actually runs. The key new quantity is the heat capacity, and the key new data source is the set of NIST heat-capacity equations you will use for the rest of the module.

## Why it matters

The energy on a food label was measured by burning the food in a bomb calorimeter, a sealed steel vessel full of oxygen. The bomb cannot expand, so it measures $\Delta U$, not $\Delta H$. Is the difference big enough to matter? For sugar it is zero; for a fuel it can be several kJ/mol. And an ammonia plant does not run at 25 °C but at about 700 K: the heat its cooling system must remove is the reaction enthalpy *at 700 K*, which differs from the table value by more than 10 %. Both corrections need only the first law and a heat capacity.

## Core ideas

> [!NOTE]
> The definitions and Kirchhoff's law are stable. Heat-capacity equations (Shomate coefficients) are from the NIST Chemistry WebBook, which takes them from the NIST-JANAF tables (Chase 1998); formation enthalpies are the CODATA Key Values listed on the same pages. The benzoic acid value is from the NIST SRM 39j certificate. All checked 2026-10-17. NIST occasionally revises WebBook entries; the values used are in `labs/module-13/nist_shomate.csv`.

### Enthalpy and why it is "heat at constant pressure"

**Enthalpy** is defined as $H = U + pV$. It is a state function because $U$, $p$ and $V$ are. Take a process at constant pressure where the only work is $p$–$V$ work, $w = -p\,\Delta V$. From the first law (lesson [13.1](lesson-01.md)):

$$\Delta H = \Delta U + p\,\Delta V = (q_p - p\,\Delta V) + p\,\Delta V = q_p$$

So at constant pressure the heat equals $\Delta H$. At constant volume no $p$–$V$ work is done, so the heat equals $\Delta U$: $q_V = \Delta U$. A coffee-cup calorimeter (open to the air) measures $\Delta H$; a sealed bomb measures $\Delta U$.

For a reaction, $p\,\Delta V$ comes almost entirely from gases. With ideal gases, $p\,\Delta V = \Delta n_\text{gas} RT$, where $\Delta n_\text{gas}$ is moles of gaseous products minus gaseous reactants:

$$\Delta H = \Delta U + \Delta n_\text{gas} RT$$

At 298 K, $RT = 2.479$ kJ/mol. Burning methane to liquid water ($\mathrm{CH_4 + 2O_2 \rightarrow CO_2 + 2H_2O(l)}$) has $\Delta n_\text{gas} = 1 - 3 = -2$, so $\Delta H$ is 4.96 kJ/mol more negative than $\Delta U$: 0.6 % of 890 kJ/mol. Small, but larger than a good bomb's uncertainty.

### Heat capacity

The **heat capacity** says how much heat raises the temperature by one kelvin. It depends on the path, so there are two, written as partial derivatives (lesson [02.5](../module-02/lesson-05.md)):

$$C_V = \left(\frac{\partial U}{\partial T}\right)_V \qquad C_p = \left(\frac{\partial H}{\partial T}\right)_p$$

At constant pressure some of the heat goes into pushing back the atmosphere as the gas expands, so $C_p > C_V$. For one mole of ideal gas, $H = U + RT$, which gives

$$C_{p,m} - C_{V,m} = R$$

Where do the numbers come from? Each way a molecule can hold energy adds to $C_V$. Translation gives $\tfrac{3}{2}R$. A linear molecule rotating adds $R$, a non-linear one $\tfrac{3}{2}R$. Vibrations add up to $R$ each, but only once $T$ is high enough to excite them (the quantum harmonic oscillator, lesson [12.4](../module-12/lesson-04.md)). So N₂ at 298 K has $C_p = 29.12$ J mol⁻¹ K⁻¹, almost exactly $\tfrac{7}{2}R = 29.10$: its stiff vibration is still "frozen". At 1000 K it has 32.69, because the vibration is starting to take energy. NH₃, with softer bending vibrations, climbs from 35.65 to 56.50 over the same range.

### Cp(T) from NIST: the Shomate equation

NIST gives gas heat capacities as a fitted polynomial in $t = T/1000$:

$$C_p^\circ = A + Bt + Ct^2 + Dt^3 + \frac{E}{t^2}$$

with coefficients $A$–$E$ for each temperature range, plus $F$, $G$ and $H$ for the matching enthalpy and entropy. Each fit is valid only inside its stated range; outside it, the polynomial can do anything. The helper `thermo13.py` in the lab folder evaluates them and refuses temperatures outside the range.

### Kirchhoff's law: reaction enthalpy at another temperature

Because $H$ is a state function, you can go from reactants at $T$ to products at $T$ by a detour: cool the reactants to 298 K, react there, heat the products back to $T$. Adding up the steps gives **Kirchhoff's law**:

$$\Delta_r H^\circ(T) = \Delta_r H^\circ(298\ \text{K}) + \int_{298}^{T} \Delta_r C_p^\circ\,dT, \qquad \Delta_r C_p^\circ = \sum \nu\,C_p^\circ$$

If $\Delta_r C_p$ is roughly constant, the integral is just $\Delta_r C_p\,(T - 298)$. For ammonia synthesis, $\Delta_r C_p(298) = 2(35.65) - 29.12 - 3(28.84) = -44.3$ J mol⁻¹ K⁻¹: the product, NH₃, holds less heat than the four molecules it replaces.

### The bomb calorimeter

A **bomb calorimeter** is a sealed steel vessel with the sample and about 30 bar of oxygen, sitting in a stirred, weighed water bath. An electric fuse ignites the sample; you record the bath temperature before and after. Nobody knows the heat capacity of the steel, water, stirrer and thermometer from first principles, so you **calibrate**: burn a standard of known energy, find the **calorimeter constant** $C_\text{cal}$ (kJ/K), then burn the unknown. The world's standard is benzoic acid, NIST SRM 39j, certified at **26.434 kJ/g** (±0.003) under its stated bomb conditions. Small corrections (fuse wire, nitric acid from the N₂ in air, the extrapolated temperature rise you met in lesson [08.7](../module-08/lesson-07.md)) are what separate a good result from a textbook one.

## Worked example

### 1. The energy in a sugar cube

Calibration: 0.9862 g of benzoic acid burns and the corrected temperature rise is 2.395 K.

$$C_\text{cal} = \frac{0.9862\ \text{g} \times 26.434\ \text{kJ/g}}{2.395\ \text{K}} = 10.885\ \text{kJ/K}$$

Sample: 1.2034 g of sucrose (C₁₂H₂₂O₁₁, 342.30 g/mol) gives a rise of 1.823 K.

$$q = 10.885 \times 1.823 = 19.84\ \text{kJ} \;\Rightarrow\; 16.49\ \text{kJ/g} \;\Rightarrow\; \Delta_c U = -16.49 \times 342.30 = -5644\ \text{kJ/mol}$$

The sign is negative because the sample *released* the heat the water absorbed. Now $\Delta H$: $\mathrm{C_{12}H_{22}O_{11}(s) + 12O_2 \rightarrow 12CO_2 + 11H_2O(l)}$ has 12 mol of gas on each side, so $\Delta n_\text{gas} = 0$ and $\Delta_c H = \Delta_c U = -5644$ kJ/mol. The NIST WebBook lists −5644 kJ/mol (Clarke and Stegeman). Food labels use 17 kJ/g (4 kcal/g) for sugar, the rounded value.

For benzoic acid itself, $\mathrm{C_7H_6O_2(s) + 7.5O_2 \rightarrow 7CO_2 + 3H_2O(l)}$ has $\Delta n_\text{gas} = -0.5$. $\Delta_c U = -26.434 \times 122.12 = -3228.1$ kJ/mol, so $\Delta_c H = -3228.1 - 0.5 \times 2.479 = -3229.4$ kJ/mol, inside the NIST average of −3228 ± 4.

### 2. Ammonia synthesis at 700 K

$\Delta_r H^\circ(298) = 2 \times (-45.94) = -91.88$ kJ/mol (CODATA value for NH₃). With a constant $\Delta_r C_p = -44.3$ J mol⁻¹ K⁻¹:

$$\Delta_r H^\circ(700) \approx -91.88 + (-0.0443)(700 - 298.15) = -109.7\ \text{kJ/mol}$$

Integrating the NIST $C_p(T)$ instead gives −105.3 kJ/mol. Why the difference? $\Delta_r C_p$ shrinks with temperature (−44.3 at 298 K, −22.4 at 700 K) as NH₃'s vibrations wake up. So: the constant-$\Delta H$ value of Module 8 is 13 kJ/mol off at 700 K; constant $\Delta C_p$ fixes most of that, and the full integral fixes the rest. Over 50–100 K, constant $\Delta C_p$ is fine; over 400 K, integrate.

## Hands-on

What you need: the [Module 13 lab folder](../../labs/module-13/) with Python 3.14 (numpy, scipy, matplotlib), the simulation below, a calculator and your notebook. Time: about 60 minutes.

### Part A — simulation: a bomb calorimeter run (20 min)

[Simulation: Calorimetry — bomb calorimeter](../../simulations/calorimetry/index.html?preset=bomb)

1. Run the calibration with benzoic acid. Record the mass, the temperature–time curve and the corrected rise $\Delta T$ (extrapolate the before and after lines to the moment of firing, as in lesson 08.7).
2. Calculate $C_\text{cal}$ from 26.434 kJ/g.
3. Burn the unknown sample offered. Calculate $\Delta_c U$ per gram and per mole, then $\Delta_c H$ from its balanced equation.
4. Repeat the calibration once more and compare the two $C_\text{cal}$ values: their difference is your first estimate of the uncertainty.

How you know it worked: $C_\text{cal}$ is around 10 kJ/K and two calibrations agree within about 0.5 %. If they differ more, check that you used the *corrected* rise and not the raw maximum.

### Part B — pencil (15 min)

1. Methane: $\Delta_c H^\circ = -890$ kJ/mol at 298 K (to liquid water). What is $\Delta_c U$?
2. A calorimeter is calibrated electrically: 12.0 V, 1.50 A for 120 s raises its temperature by 0.199 K. What is $C_\text{cal}$?
3. How much heat warms 2.00 mol of N₂ from 298 K to 500 K (a) at constant pressure, with a mean $C_p$ of 29.3 J mol⁻¹ K⁻¹, and (b) at constant volume?

<details><summary>Answers to Part B</summary>

1. $\Delta n_\text{gas} = 1 - 3 = -2$, so $\Delta U = \Delta H - \Delta n RT = -890 + 2 \times 2.479 = -885$ kJ/mol.
2. Electrical energy $= VIt = 12.0 \times 1.50 \times 120 = 2160$ J; $C_\text{cal} = 2160 / 0.199 = 10.9$ kJ/K.
3. (a) $q_p = nC_p\Delta T = 2.00 \times 29.3 \times 202 = 11.8$ kJ (the NIST integral gives 11.82 kJ). (b) $C_V = C_p - R = 21.0$, so $q_V = 2.00 \times 21.0 \times 202 = 8.5$ kJ. The difference, $nR\Delta T = 3.4$ kJ, is the work of pushing back the atmosphere.

</details>

### Part C — Python: Kirchhoff's law with NIST data (25 min)

Open `lesson02_kirchhoff.py` and write the three TODO functions: `calorimeter_constant`, `delta_h_from_delta_u` and `kirchhoff_integrated` (use `scipy.integrate.quad` on `delta_cp`). Put your Part A numbers in the setup block, then run:

```bash
py lesson02_kirchhoff.py
```

How you know it worked: with the example numbers it prints $C_\text{cal}$ = 10.885 kJ/K and $\Delta_c H$ = −5644 kJ/mol; a table of $C_p$ for N₂, H₂ and NH₃ from 298 to 1000 K; and $\Delta_r H$ for ammonia synthesis where your integrated column matches the "Shomate H" column (computed independently from the NIST enthalpy equation) to 0.01 kJ/mol: −99.79 at 500 K, −105.32 at 700 K. The plot `runs/lesson02_dH_vs_T.png` shows the three approximations drifting apart. Record your simulation result and the 700 K value on a [notebook page](../../templates/notebook-page.md).

<details><summary>Reference solution</summary>

`calorimeter_constant`: `return m_std_g * kj_per_g / dt_k`. `delta_h_from_delta_u`: `return du_kj_mol + dn_gas * R * t / 1000`. `kirchhoff_integrated`: `integral, _ = quad(lambda x: delta_cp(reaction, x), T0, t)` then `return dh298_kj + integral / 1000`. Full code in `lesson02_kirchhoff_solution.py`. The integral and the direct Shomate enthalpy agree because the Shomate $H$ equation is exactly the integral of its $C_p$ equation.

</details>

## Common mistakes

- **Reporting a bomb result as $\Delta H$ without the $\Delta n_\text{gas} RT$ correction.** Count only gases, and only on the balanced equation per mole of fuel.
- **Wrong sign for $\Delta_c U$.** The water gained heat; the reaction lost it. Combustion energies are negative.
- **Using a Shomate fit outside its range.** Water vapour's NIST fit starts at 500 K; below that, use another source. The helper stops you on purpose.
- **Using $C_V$ for an open, constant-pressure process** (or $C_p$ in a sealed bomb). Ask what is held constant.
- **Forgetting the stoichiometric numbers in $\Delta_r C_p$.** Three moles of H₂ count three times, with a minus sign.

## Key takeaways

- $H = U + pV$; at constant pressure $q_p = \Delta H$, at constant volume $q_V = \Delta U$; for reactions $\Delta H = \Delta U + \Delta n_\text{gas} RT$.
- A bomb calorimeter measures $\Delta U$ and must be calibrated, worldwide with benzoic acid (26.434 kJ/g, NIST SRM 39j).
- $C_p = (\partial H/\partial T)_p$, $C_V = (\partial U/\partial T)_V$, and $C_{p,m} - C_{V,m} = R$ for an ideal gas. Gas heat capacities rise with $T$ as vibrations switch on.
- Kirchhoff: $\Delta_r H(T) = \Delta_r H(298) + \int \Delta_r C_p\,dT$. Constant $\Delta C_p$ works over a short range; integrate the NIST $C_p(T)$ over a long one.

## Sources

- [MIT OpenCourseWare 5.60, lecture notes](https://ocw.mit.edu/courses/5-60-thermodynamics-kinetics-spring-2008/pages/lecture-notes/) — enthalpy, heat capacities, $C_p - C_V$, Kirchhoff's law, calorimetry.
- [NIST SRM 39j Benzoic Acid certificate](https://tsapps.nist.gov/srmext/certificates/39J.pdf) — certified energy of combustion 26 434 ± 3 J/g for bomb calibration.
- [NIST Chemistry WebBook: Sucrose](https://webbook.nist.gov/cgi/cbook.cgi?ID=C57501&Mask=2) — $\Delta_c H^\circ$(solid) −5644 kJ/mol.
- [NIST Chemistry WebBook: Benzoic acid](https://webbook.nist.gov/cgi/cbook.cgi?ID=C65850&Mask=2) — $\Delta_c H^\circ$(solid) −3228 ± 4 kJ/mol.
- [NIST Chemistry WebBook: Ammonia, gas phase](https://webbook.nist.gov/cgi/cbook.cgi?ID=C7664417&Mask=1) — Shomate coefficients, $\Delta_f H^\circ$ −45.94 kJ/mol (CODATA); N₂ and H₂ from their WebBook pages (see `nist_shomate.csv`).
