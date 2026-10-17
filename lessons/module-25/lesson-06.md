---
id: "25.6"
module: 25
minutes: 22
practice_minutes: 180
prerequisites: ["19.5", "25.1", "25.2", "25.3", "25.4", "25.5"]
objectives:
  - Prepare and run a cyclic voltammetry experiment (electrode polishing, reference check, supporting electrolyte, purging, blank, potential window) and explain each step.
  - Use a scan-rate study to tell diffusion-controlled from adsorbed species, and kinetic peak separation from uncompensated resistance.
  - Calculate the standard heterogeneous rate constant from peak separations with Nicholson's method, and state the range where the method is valid.
  - Produce a quality-control dossier for a drink that combines UV-Vis, fluorescence, GC-MS and voltammetry, with an expanded uncertainty and a decision for each result.
volatility: concept
sources:
  - title: "Harvey, Analytical Chemistry 2.1, 11.4 Voltammetric and Amperometric Methods (LibreTexts)"
    url: https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_(Harvey)/11%3A_Electrochemical_Methods/11.04%3A_Voltammetric_and_Amperometric_Methods
  - title: "Nicholson, Theory and application of cyclic voltammetry for measurement of electrode reaction kinetics, Anal. Chem. 37, 1351 (1965)"
    url: https://doi.org/10.1021/ac60230a016
  - title: "Lavagnini, Antiochia and Magno, An extended method for the practical evaluation of the standard rate constant from cyclic voltammetric data, Electroanalysis 16, 505 (2004)"
    url: https://doi.org/10.1002/elan.200302851
  - title: "NIST, CODATA 2022 fundamental physical constants"
    url: https://physics.nist.gov/cuu/Constants/
  - title: "eCFR, 21 CFR 172.575 Quinine"
    url: https://www.ecfr.gov/current/title-21/chapter-I/subchapter-B/part-172/subpart-F/section-172.575
last_verified: "2026-10-17"
---

# 25.6 · Cyclic voltammetry in practice

[Lesson 19.5](../module-19/lesson-05.md) showed what a cyclic voltammogram (CV) is and how to read a reversible one. In the lab most couples are not perfectly reversible, electrodes get dirty, and the solution resists the current. This lesson is the bench version: how to prepare a cell that gives trustworthy curves, how a scan-rate study tells you what controls the current, and how to turn peak separations into an electron-transfer rate constant. The second half is the module practical: a quality-control dossier for a soft drink that uses every instrument in this module.

## Why it matters

A sensor company tests a new electrode material for a vitamin C sensor. On the first day the peaks of a test couple are 70 mV apart; a week later they are 140 mV apart and the sensor reads 20 % low. Is the material slowing electron transfer, has the surface fouled, or is the new reference electrode's frit blocked so that the solution resistance has gone up? Each cause needs a different fix: re-polishing, a new material, or a new reference electrode. A ten-minute scan-rate study with one concentration change separates them. Without it the team may spend a month on the wrong problem.

## Core ideas

> [!NOTE]
> Stable: diffusion and kinetics in CV, the Randles–Ševčík and Nicholson analyses, the role of supporting electrolyte and iR drop (Harvey 11.4, checked 2026-10-17). Constants: CODATA 2022 (NIST); $F/RT$ = 38.92 V⁻¹ at 25 °C. Lavagnini's empirical equation replaces Nicholson's working curve; in this lab it agrees with Nicholson's table to about 5 % only up to about 150 mV of peak separation. Instrument software and electrode products change; the procedure does not. Lab data are simulated.

### Preparing the cell

1. **Polish the working electrode.** Glassy carbon is polished with 0.05 µm alumina slurry on a pad in figure-eight strokes, rinsed and briefly sonicated. A fouled surface slows electron transfer and widens the peaks.
2. **Check the reference.** Ag/AgCl filled with 3 M KCl, no air bubbles at the tip, frit wet. A blocked frit adds resistance and makes the potential drift.
3. **Supporting electrolyte, 0.1–0.5 M.** Carries the current so the analyte moves only by diffusion (no migration), and keeps the solution resistance low.
4. **Purge with nitrogen or argon for 10 minutes**, then keep a gas blanket over the solution. Dissolved oxygen is reduced at negative potentials and adds its own wave.
5. **Blank CV** of the electrolyte alone: it shows the usable window and the background.
6. **Choose the window.** Start where no reaction occurs, and switch about 150–200 mV past the peak so the curve has time to decay.
7. **Test couple.** Before measuring, run a known reversible couple (ferricyanide or a ferrocene derivative). If its $\Delta E_p$ is far above 60–70 mV, repolish.

### What a scan-rate study tells you

Record CVs from 20 mV/s to 1 V/s and look at four things:

| Observation | Reversible, diffusing | Quasi-reversible | Adsorbed on the surface |
|---|---|---|---|
| $i_p$ against $v$ | $\propto \sqrt{v}$ | about $\sqrt{v}$, a little lower | $\propto v$ |
| slope of $\log i_p$ against $\log v$ | 0.50 | slightly below 0.50 | 1.0 |
| $\Delta E_p$ | 57–60 mV, constant | grows with $v$ | near 0 |
| $E_{1/2}$ | constant | nearly constant | constant |

The charging current grows in proportion to $v$, faster than the diffusion peak, so at high scan rates the background takes a larger share.

### Kinetics or resistance?

A peak separation that grows with scan rate has two possible causes. **Slow electron transfer** (a small standard rate constant $k^0$) is a property of the couple and the electrode surface. **Uncompensated resistance** $R_u$ between the reference tip and the working electrode shifts each peak by $i_p R_u$. With $R_u$ = 200 Ω and a peak current of 40 µA, each peak moves 8 mV and $\Delta E_p$ grows by 16 mV. The test: halve the concentration. Halving $i_p$ halves the iR shift, but the kinetic separation does not depend on concentration. Moving the reference closer, adding electrolyte, or using the potentiostat's iR compensation reduces $R_u$.

### Nicholson's method for $k^0$

Nicholson (1965) showed that, for $\alpha$ near 0.5, the peak separation depends on one dimensionless number:

$$\psi = \frac{k^0}{\sqrt{\pi D\, n F v / RT}}$$

Large $\psi$ (fast transfer or slow scans) gives the reversible 57–60 mV; $\psi$ = 1 gives about 84 mV; $\psi$ = 0.25 gives about 141 mV. Lavagnini and co-workers fitted the working curve with

$$\psi = \frac{-0.6288 + 0.0021\,X}{1 - 0.017\,X}, \qquad X = n\,\Delta E_p\ (\text{mV})$$

Measure $\Delta E_p$ at several scan rates, convert each to $\psi$, and solve for $k^0$. You need $D$ from an independent measurement (for example chronoamperometry), because the reversible Randles–Ševčík equation overestimates the peak of a slow couple and so underestimates $D$. Use only scans with $\Delta E_p$ between about 63 and 150 mV: below that the method has no sensitivity, above it the empirical equation drifts.

### A chemical step after the electron transfer

If the product reacts away (an EC mechanism), the return peak shrinks. Measure the ratio with Nicholson's correction, because the return peak sits on the decaying forward current: $i_{pa}/i_{pc} = (i_{pa})_0/i_{pc} + 0.485\,(i_{sp})_0/i_{pc} + 0.086$, where the subscript 0 means "read from zero current" and $i_{sp}$ is the current at the switching potential. A ratio of 1.0 at every scan rate means no follow-up chemistry.

### Safety reasoning

Potentials and currents are harmless, but the chemicals are not always. Alumina slurry is a fine dust when dry; keep it wet. Organic electrolytes such as tetrabutylammonium perchlorate are oxidisers that can be explosive when dry with organic material; never scrape dry residues. Gas cylinders are chained upright.

## Worked example

### 1. $k^0$ from one scan

At $v$ = 0.100 V/s the peaks are 113 mV apart ($n$ = 1, 25 °C, $D$ = 7.0 × 10⁻⁶ cm²/s). Then

$$\psi = \frac{-0.6288 + 0.0021 \times 113}{1 - 0.017 \times 113} = \frac{-0.3915}{-0.921} = 0.425$$

$$\sqrt{\pi D F v / RT} = \sqrt{\pi \times 7.0\times10^{-6} \times 38.92 \times 0.100} = 9.25\times10^{-3}\ \text{cm/s}$$

$$k^0 = 0.425 \times 9.25\times10^{-3} = 3.9\times10^{-3}\ \text{cm/s}$$

That is a quasi-reversible couple: reversible-looking at 10 mV/s, clearly slow at 1 V/s.

### 2. A drink's vitamin C by standard addition

Ascorbic acid oxidises irreversibly at carbon near +0.3–0.4 V in pH 4 buffer; its peak current is proportional to concentration. A drink diluted 1 + 9 gives peak currents (µA) of 9.43 + 0.837 × (mg/L added). The x intercept is 9.43/0.837 = 11.3 mg/L in the cell, so the drink holds 113 mg/L. Standard addition is used because the drink's sugars, acids and pulp change the electrode response.

## Hands-on

What you need: the [Module 25 lab folder](../../labs/module-25/) with Python set up, your results and notebook pages from Lessons 25.1–25.5, `get_nist_ms.py` already run once (Lesson 25.4), and the [lab report template](../../templates/lab-report.md). Time: about 3 hours: 70 minutes for Parts A and B, 110 minutes for the module practical. No home part: CV needs a potentiostat.

### Part A — simulation: diagnose the couple (30 min)

[Simulation: Voltammetry — scan-rate study](../../simulations/voltammetry/index.html?preset=scan-rate)

1. Record CVs at 20, 50, 100, 200, 500 and 1000 mV/s. Plot $i_p$ against $\sqrt{v}$.
2. Switch to the adsorbed-species option and repeat. What changes in the shape and in the plot?
3. Switch on 300 Ω of uncompensated resistance. Repeat at 1 mM and at 0.5 mM and compare $\Delta E_p$.

[Simulation: Voltammetry — quasi-reversible kinetics](../../simulations/voltammetry/index.html?preset=quasi)

4. Set $k^0$ to 1, 0.01 and 0.001 cm/s and run each at 0.1 V/s. Read $\Delta E_p$ and compare with $\psi$.

How you know it worked: adsorbed peaks are symmetric with near-zero separation and $i_p \propto v$; the resistance-induced extra separation halves when the concentration halves; $\Delta E_p$ rises from about 59 to more than 150 mV as $k^0$ falls.

### Part B — Python: $k^0$ from a scan-rate series (40 min)

Open `lesson06_cv.py`. Complete `psi_from_dEp()` (TODO 1) and `k0_from_psi()` (TODO 2). Run `py lesson06_cv.py`.

How you know it worked: the log–log slope is 0.465; the apparent Randles–Ševčík $D$ is 6.0 × 10⁻⁶ cm²/s (low, as expected for a slow couple); $\Delta E_p$ grows from 84 to 190 mV, $E_{1/2}$ stays at 0.216–0.219 V and the corrected current ratio is 1.01–1.03; from the four scans with $\Delta E_p \le$ 150 mV, $k^0$ = 0.0041 ± 0.0002 cm/s (true value 0.004). The two fastest scans give lower values because the empirical equation drifts there.

### Part C — module practical: a QC dossier for a bitter-lemon drink (110 min)

A producer sends you a cloudy bitter-lemon drink and its specification: tartrazine 25 mg/L (accept 90–110 %), quinine below the 83 mg/L legal limit (21 CFR 172.575; recipe target 65 mg/L), natural lemon flavour, vitamin C declared at 120 mg/L (accept 80–150 %). The instrument data are in `practical_drink.csv`.

1. **Plan.** For each claim, write in your notebook which instrument and calibration you will use and why (UV-Vis, fluorescence, GC-MS, voltammetry; external or standard addition). Name the main risk for each: turbidity, matrix absorption of the excitation light, isomers, the electrode response in a sugary matrix.
2. **Compute.** Open `practical_dossier.py` and complete `turbidity_corrected()` (TODO 1) and `decide()` (TODO 2). Run it:

```bash
py practical_dossier.py
```

3. **Judge each result.** Use the rule in `decide()`: pass if the whole interval value ± U lies inside the limits, fail if it lies wholly outside, inconclusive otherwise.
4. **Report.** Fill in the lab-report template: one section per analyte with method, calibration, result ± U (k = 2), decision and the quality evidence (baseline correction, slope ratio, MS + RI, standard addition). End with what the data cannot show.

How you know it worked: tartrazine 24.5 ± 0.2 mg/L (27.4 without the baseline correction), pass; quinine 54.9 mg/L by external calibration but 62.8 ± 1.0 mg/L by standard addition (matrix slope 0.87), below 83 mg/L, pass; the GC-MS table from Lesson 25.4 with limonene, neral and geranial identified; vitamin C 113 ± 5 mg/L, 94 % of the declared value, pass.

<details><summary>Reference conclusions for the report</summary>

The cloudiness adds about 0.03 absorbance at every wavelength; without the 700 nm baseline the tartrazine result is 12 % high and would fail the specification. The drink's matrix absorbs part of the 350 nm excitation light, so external calibration reads quinine 13 % low; standard addition corrects it, and the slope ratio documents the effect. GC-MS with retention indices shows the expected lemon terpenes and citrals; it cannot prove that the flavour is natural, which needs chiral GC (limonene enantiomers) or isotope-ratio MS. Vitamin C is within specification, though below the declared value, which is common because ascorbic acid oxidises during storage; a stability study would tell the producer how much overage to add.

</details>

## Common mistakes

- **Skipping the test couple.** Without a known reversible couple you cannot tell a slow analyte from a dirty electrode.
- **Reading resistance as kinetics.** If $\Delta E_p$ depends on concentration, the cause is iR drop, not slow electron transfer.
- **Using Randles–Ševčík to get $D$ for a slow couple.** The reversible equation underestimates $D$, and every $k^0$ from it is then wrong too.
- **Applying Nicholson's method outside its range.** Below about 63 mV there is no kinetic information; above about 150 mV use the full working curve or a digital simulation.
- **Reporting a result without its decision rule.** "113 mg/L" helps no one; "113 ± 5 mg/L, inside 96–180 mg/L, pass" does.

## Key takeaways

- Trustworthy CVs start with a polished electrode, a checked reference, enough supporting electrolyte, a purge and a blank.
- A scan-rate study separates diffusion ($i_p \propto \sqrt{v}$) from adsorption ($i_p \propto v$), and a concentration change separates iR drop from slow kinetics.
- Nicholson's $\psi$ links peak separation to $k^0$; use it with an independent $D$ and peak separations of about 63–150 mV.
- An analytical result is a value, an uncertainty, the evidence that the method worked on this sample, and a decision.

## Sources

- [Harvey, Analytical Chemistry 2.1, 11.4](https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_(Harvey)/11%3A_Electrochemical_Methods/11.04%3A_Voltammetric_and_Amperometric_Methods) — cells, electrolytes, CV and quantitative voltammetry.
- [Nicholson 1965, Anal. Chem. 37, 1351](https://doi.org/10.1021/ac60230a016) — the ψ working curve for quasi-reversible CVs and the return-peak correction.
- [Lavagnini et al. 2004, Electroanalysis 16, 505](https://doi.org/10.1002/elan.200302851) — the empirical ψ(ΔEp) equation.
- [NIST CODATA 2022 constants](https://physics.nist.gov/cuu/Constants/) — F and R.
- [eCFR, 21 CFR 172.575](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-B/part-172/subpart-F/section-172.575) — the quinine limit used in the practical.
