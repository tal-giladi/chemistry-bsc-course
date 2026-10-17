---
id: "10.3"
module: 10
minutes: 20
practice_minutes: 60
prerequisites: ["10.1", "08.3", "08.4"]
objectives:
  - Calculate a precipitation titration curve (pAg against volume) from the solubility product and explain why the jump is larger for iodide than for chloride.
  - Choose between the Mohr, Volhard and Fajans methods for a chloride sample and compute a Volhard back-titration result.
  - Compute the fraction of EDTA present as Y⁴⁻ and the conditional formation constant at a given pH, and use them to pick the pH of an EDTA titration.
  - Calculate the total, calcium and magnesium hardness of a water sample from EDTA titration volumes.
volatility: concept
sources:
  - title: "LibreTexts — Harvey, Analytical Chemistry 2.1, 9.5 Precipitation Titrations"
    url: https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/09%3A_Titrimetric_Methods/9.05%3A_Precipitation_Titrations
  - title: "LibreTexts — Harvey, Analytical Chemistry 2.1, 9.3 Complexation Titrations"
    url: https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/09%3A_Titrimetric_Methods/9.03%3A_Complexation_Titrations
  - title: "LibreTexts — Harvey, Analytical Chemistry 2.1, 16.10 Solubility Products"
    url: https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/16%3A_Appendix/16.10%3A_Solubility_Products
  - title: "LibreTexts — Harvey, Analytical Chemistry 2.1, 16.12 Formation Constants"
    url: https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/16%3A_Appendix/16.12%3A_Formation_Constants
last_verified: "2026-10-17"
---

# 10.3 · Precipitation and complexometric titrations

Not every titration is acid–base or redox. Chloride is titrated with silver ions, which form an insoluble precipitate, and calcium and magnesium are titrated with EDTA, which wraps around metal ions in a tight complex. Both are workhorse methods of water and food labs, and both are in the S3 course. In this lesson you build the precipitation curve from the solubility product, compare the three classic silver methods, and see why an EDTA titration only works at the right pH. You finish by calculating the hardness of a water sample, which leads into the water-testing lesson 10.5.

## Why it matters

A municipal water lab reports chloride and hardness for every source it supplies. Chloride above a few hundred milligrams per litre tastes salty and corrodes pipes; hard water leaves scale in kettles and boilers and wastes soap. Both are measured by titration in minutes, with no instrument beyond a burette. But each method has a trap. The Mohr method fails in acidic water. The Volhard method reads low unless you deal with the silver chloride. And an EDTA titration run at pH 9 instead of pH 10 can end early. Understanding the equilibria tells you which trap you are in.

## Core ideas

> [!NOTE]
> Stable: the equilibrium chemistry. Constants used here, checked 2026-10-17 in Harvey, Analytical Chemistry 2.1: $K_{sp}$ AgCl 1.8 × 10⁻¹⁰, AgBr 5.0 × 10⁻¹³, AgI 8.3 × 10⁻¹⁷, Ag₂CrO₄ 1.2 × 10⁻¹², AgSCN 1.1 × 10⁻¹² (Appendix 16.10); EDTA p$K_a$ 0.0, 1.5, 2.0, 2.66, 6.16, 10.24 (section 9.3); log $K_f$ CaY²⁻ 10.69 and MgY²⁻ 8.79 (Appendix 16.12).

### A precipitation titration curve

Adding silver nitrate to chloride forms solid silver chloride:

$$\mathrm{Ag^+(aq) + Cl^-(aq) \rightarrow AgCl(s)}, \qquad K_{sp} = [\mathrm{Ag^+}][\mathrm{Cl^-}] = 1.8 \times 10^{-10}$$

The curve plots $\mathrm{pAg} = -\log[\mathrm{Ag^+}]$ against volume, like pH. Before equivalence, chloride is in excess and $[\mathrm{Ag^+}] = K_{sp}/[\mathrm{Cl^-}]$ is tiny. After it, silver is in excess. One exact formula covers the whole curve. Let $e = [\mathrm{Ag^+}] - [\mathrm{Cl^-}]$, the excess of silver over chloride, which comes straight from the volumes:

$$e = \frac{C_\mathrm{Ag} V - C_\mathrm{Cl} V_\mathrm{Cl}}{V + V_\mathrm{Cl}}, \qquad [\mathrm{Ag^+}] = \frac{e + \sqrt{e^2 + 4K_{sp}}}{2}$$

At equivalence $e = 0$ and $[\mathrm{Ag^+}] = \sqrt{K_{sp}} = 1.3 \times 10^{-5}$ M, pAg 4.87. The smaller $K_{sp}$, the larger the jump: iodide (8.3 × 10⁻¹⁷) gives a much sharper end point than chloride. This is the same "small K, big jump" logic as a weak acid in lesson [08.3](../module-08/lesson-03.md).

### Three ways to see the end point

- **Mohr method** (direct). A little potassium chromate is added. After the last chloride precipitates, the next silver forms red-brown silver chromate, Ag₂CrO₄. The solution must be neutral to slightly basic (about pH 7–10): in acid, chromate becomes HCrO₄⁻ and the end point comes late; above pH 10, silver hydroxide precipitates. Because some excess silver is needed to see the red colour, subtract a **reagent blank**: titrate a chloride-free suspension of CaCO₃ to the same colour.
- **Volhard method** (back titration). Add a known excess of silver nitrate, then titrate the leftover silver with thiocyanate (SCN⁻), using Fe³⁺ as the indicator: the first excess SCN⁻ forms red Fe(SCN)²⁺. It runs in nitric acid, so it works in acidic samples. Trap: AgCl ($K_{sp}$ 1.8 × 10⁻¹⁰) is more soluble than AgSCN (1.1 × 10⁻¹²), so thiocyanate slowly dissolves AgCl and the result reads low. Filter off the AgCl first, or coat it.
- **Fajans method** (adsorption indicator). Dichlorofluorescein is an anionic dye. Before equivalence the AgCl particles carry excess Cl⁻ on their surface and repel it; after equivalence they carry Ag⁺ and the dye sticks to them, turning the precipitate pink.

### EDTA: one ligand, one metal

**EDTA** (ethylenediaminetetraacetic acid) is a **chelating agent**: one molecule grabs a metal ion with six donor atoms at once. It forms a 1 : 1 complex with almost every metal ion, which makes the stoichiometry simple. Written as Y⁴⁻ for the fully deprotonated form:

$$\mathrm{Ca^{2+} + Y^{4-} \rightleftharpoons CaY^{2-}}, \qquad K_f = 10^{10.69}$$

EDTA is also a hexaprotic acid. Only Y⁴⁻ binds the metal, and Y⁴⁻ dominates only above pH 10.24. The fraction of free EDTA present as Y⁴⁻ is called $\alpha_{\mathrm{Y^{4-}}}$; with $h = [\mathrm{H^+}]$ and $K_1 \ldots K_6$ the acid constants:

$$\alpha_{\mathrm{Y^{4-}}} = \frac{K_1K_2K_3K_4K_5K_6}{h^6 + h^5K_1 + h^4K_1K_2 + \dots + K_1K_2K_3K_4K_5K_6}$$

At pH 10 it is 0.37; at pH 8, 0.0056. The **conditional formation constant** folds this in: $K_f' = \alpha_{\mathrm{Y^{4-}}} K_f$. It tells you how strongly EDTA binds the metal *at that pH*. A common rule of thumb is that a sharp visual end point needs $K_f' \geq 10^8$. For calcium that holds above about pH 7.6; for magnesium only above about pH 9.5. That is why hardness titrations are buffered at pH 10 with ammonia and ammonium chloride.

### Metallochromic indicators and water hardness

A **metallochromic indicator**, such as Eriochrome Black T or calmagite, is a dye that changes colour when it binds a metal. Its metal complex is red, the free dye blue. It binds Mg²⁺ more weakly than EDTA does, so at the end point EDTA takes the last Mg²⁺ from the indicator and the solution turns blue. Calcium binds the indicator too weakly to give a sharp change, so a little Mg–EDTA is added to the buffer.

**Water hardness** is the total concentration of Ca²⁺ and Mg²⁺, reported as if it were all CaCO₃, in mg/L. At pH 10 EDTA titrates both together. At pH 12–13 magnesium precipitates as Mg(OH)₂, so the titration gives calcium alone; magnesium is the difference.

## Worked example

### 1. Chloride in brackish well water by Volhard

To 50.00 mL of water you add 25.00 mL of 0.02000 M AgNO₃ (0.5000 mmol, an excess), filter off the AgCl, and back-titrate the filtrate with 0.02000 M KSCN. It takes 11.30 mL (0.2260 mmol).

$$n(\mathrm{Cl^-}) = 0.5000 - 0.2260 = 0.2740\ \text{mmol}$$

$$c(\mathrm{Cl^-}) = \frac{0.2740\ \text{mmol} \times 35.45\ \text{mg/mmol}}{0.05000\ \text{L}} = 194\ \text{mg/L}$$

Had you not filtered, the SCN⁻ would have dissolved some AgCl, the back titration would have used more thiocyanate, and the chloride result would have come out low.

### 2. Total, calcium and magnesium hardness

A 50.00 mL tap-water sample at pH 10 with calmagite needs 12.85 mL of 0.01000 M EDTA. A second 50.00 mL portion, brought to pH 12.5 so that Mg(OH)₂ precipitates, needs 9.20 mL with a calcium indicator.

- Total: $0.01000 \times 12.85 = 0.1285$ mmol in 50 mL, or 2.570 mmol/L. As CaCO₃ (100.09 mg/mmol): **257 mg/L**.
- Calcium: $0.01000 \times 9.20 / 50.00 = 1.840$ mmol/L, times 40.08 mg/mmol = **73.7 mg/L Ca**.
- Magnesium: $(12.85 - 9.20) \times 0.01000 / 50.00 = 0.730$ mmol/L, times 24.31 = **17.7 mg/L Mg**.

On the usual scale (soft below 60, moderately hard 61–120, hard 121–180, very hard above 180 mg/L as CaCO₃), this water is very hard, typical of water from limestone aquifers.

## Hands-on

What you need: the [Module 10 lab folder](../../labs/module-10/) and Python; a calculator for Part C. Time: about 60 minutes. There is no home version of these titrations: silver nitrate stains skin and is toxic to aquatic life, chromate is a carcinogen, and EDTA titrations need ammonia buffer. The simulations show every step. Lesson 10.5 has a safe home hardness test.

### Part A — simulations (25 min)

[Simulation: Titration bench — chloride with silver nitrate (Mohr)](../../simulations/titration/index.html?preset=precipitation)

1. Titrate the chloride sample with chromate indicator at pH 8. Run the reagent blank and subtract it.
2. Repeat at pH 5 and note how much later the red colour appears.

[Simulation: Titration bench — water hardness with EDTA](../../simulations/titration/index.html?preset=edta)

3. Titrate at pH 10 with the indicator. Then try pH 8 and pH 12 and compare the end points.

Target: your pH 8 Mohr result, blank-corrected, within 0.5 % of the stated chloride; your pH 10 hardness within 2 % of the stated value.

### Part B — Python: curves and conditional constants (25 min)

Open `lesson03_complex.py`, fill in `pag_curve` and `alpha_y4`, and run:

```bash
py lesson03_complex.py
```

It prints pAg at six volumes, the chromate concentration the Mohr method would ideally need, a table of $\alpha_{\mathrm{Y^{4-}}}$ and log $K_f'$ from pH 7 to 12, and the lowest pH that gives log $K_f' \geq 8$ for Ca²⁺ and Mg²⁺. It saves the chloride, bromide and iodide curves to `runs/lesson03_pag.png`.

How you know it worked: pAg 4.87 at 25.00 mL; ideal chromate 6.7 × 10⁻³ M; $\alpha$ = 0.365 at pH 10; lowest pH 7.6 for calcium and 9.5 for magnesium.

<details><summary>Reference solution</summary>

`pag_curve`: `e = (c_ag * v - c_x * v_x) / (v + v_x)`, `ag = (e + np.sqrt(e ** 2 + 4 * ksp)) / 2`, return `-np.log10(ag)`. `alpha_y4`: start with `terms = [h ** 6]`, multiply a running product of the $K_i$ and append `prod * h ** (6 - i)` for i = 1 to 6, return `terms[-1] / sum(terms)`. Full code in `lesson03_complex_solution.py`.

</details>

### Part C — pencil problems (10 min)

1. A Mohr titration of 100.0 mL of water uses 8.42 mL of 0.01410 M AgNO₃; the blank uses 0.20 mL. What is the chloride concentration in mg/L?
2. Why would the Mohr method give a high result for a water sample at pH 5, and what would you do?

<details><summary>Answers</summary>

1. $(8.42 - 0.20) \times 0.01410 = 0.1159$ mmol in 100.0 mL; $0.1159 \times 35.45 / 0.1000 = 41.1$ mg/L.
2. At pH 5 much of the chromate is HCrO₄⁻, so more silver is needed before Ag₂CrO₄ forms and the end point comes late. Neutralise the sample with a little sodium bicarbonate first, or use the Volhard method, which works in acid.

</details>

## Common mistakes

- **Running a Mohr titration in acid.** The end point comes late. Check the pH; bring it to 7–10 with bicarbonate.
- **Skipping the Mohr blank.** Some excess silver is always needed to see the red colour; subtract a blank titrated to the same shade.
- **Back-titrating Volhard samples with AgCl still present.** Thiocyanate converts AgCl to AgSCN and the chloride result reads low. Filter first.
- **Forgetting the buffer in an EDTA titration.** EDTA releases H⁺ as it binds metals; without a buffer the pH falls, $K_f'$ drops and the end point fades.
- **Reporting hardness as mg/L of calcium.** Hardness is reported as mg/L CaCO₃ and includes magnesium. Convert with 100.09 mg per mmol.

## Key takeaways

- A precipitation curve follows from $K_{sp}$ alone; the smaller $K_{sp}$, the bigger the jump at equivalence.
- Mohr needs pH 7–10 and a blank; Volhard works in acid but needs the AgCl removed; Fajans uses a dye that sticks to the charged precipitate.
- Only Y⁴⁻ binds metals, so EDTA titrations depend on pH through $K_f' = \alpha_{\mathrm{Y^{4-}}} K_f$; magnesium needs pH 10.
- Hardness at pH 10 is Ca + Mg; at pH 12–13 it is Ca alone; report as mg/L CaCO₃.

## Sources

- [Harvey, Analytical Chemistry 2.1, 9.5 Precipitation Titrations](https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/09%3A_Titrimetric_Methods/9.05%3A_Precipitation_Titrations) — titration curve, Mohr, Volhard and Fajans methods.
- [Harvey, Analytical Chemistry 2.1, 9.3 Complexation Titrations](https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/09%3A_Titrimetric_Methods/9.03%3A_Complexation_Titrations) — EDTA, α(Y⁴⁻), conditional constants, hardness method.
- [Harvey, Analytical Chemistry 2.1, 16.10 Solubility Products](https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/16%3A_Appendix/16.10%3A_Solubility_Products) — $K_{sp}$ values.
- [Harvey, Analytical Chemistry 2.1, 16.12 Formation Constants](https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/16%3A_Appendix/16.12%3A_Formation_Constants) — log $K_f$ for CaY²⁻ and MgY²⁻.
