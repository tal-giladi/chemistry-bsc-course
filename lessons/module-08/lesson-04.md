---
id: "08.4"
module: 8
minutes: 20
practice_minutes: 60
prerequisites: ["08.3", "02.1"]
objectives:
  - Identify Brønsted acids, bases and conjugate pairs, and convert between [H₃O⁺], [OH⁻], pH and pOH using Kw.
  - Calculate the pH of a strong acid and of a weak acid from its concentration and Ka, and check the small-x approximation.
  - Calculate the pH of a buffer with the Henderson–Hasselbalch equation and explain how an indicator such as red cabbage changes colour.
volatility: concept
sources:
  - title: "OpenStax Chemistry 2e, 14.1 Brønsted-Lowry Acids and Bases"
    url: https://openstax.org/books/chemistry-2e/pages/14-1-bronsted-lowry-acids-and-bases
  - title: "OpenStax Chemistry 2e, 14.2 pH and pOH"
    url: https://openstax.org/books/chemistry-2e/pages/14-2-ph-and-poh
  - title: "OpenStax Chemistry 2e, 14.3 Relative Strengths of Acids and Bases"
    url: https://openstax.org/books/chemistry-2e/pages/14-3-relative-strengths-of-acids-and-bases
  - title: "OpenStax Chemistry 2e, 14.6 Buffers"
    url: https://openstax.org/books/chemistry-2e/pages/14-6-buffers
  - title: "OpenStax Chemistry 2e, Appendix H: Ionization Constants of Weak Acids"
    url: https://openstax.org/books/chemistry-2e/pages/h-ionization-constants-of-weak-acids
  - title: "Royal Society of Chemistry, Making a pH indicator using red cabbage"
    url: https://edu.rsc.org/experiments/making-a-ph-indicator-using-red-cabbage/422.article
  - title: "RHS Campaign for School Gardening, Red cabbage indicator colour chart (PDF)"
    url: https://www.rhs.org.uk/getmedia/386dd481-7d8c-43c0-b64e-ff66bf02dbe9/Res-L-Red-Cabbage-Indicator-Colour-Chart.pdf
  - title: "PubChem, Acetic acid (CID 176): pKa and GHS classification"
    url: https://pubchem.ncbi.nlm.nih.gov/compound/176
last_verified: "2026-10-17"
---

# 08.4 · Acids, bases and pH

An acid gives away a proton and a base takes one. That simple picture explains why vinegar is sour, why baking soda fizzes in it, why blood stays at pH 7.4 and why red cabbage juice changes colour. In this lesson you learn the pH scale, how to tell strong acids from weak ones, how to calculate the pH of a solution from its concentration, and how buffers resist change. You will then make your own indicator from red cabbage and test the predictions on liquids from your kitchen.

## Why it matters

You want to know how much acid is in a bottle of vinegar. You will titrate it with baking soda in lesson 08.7, and you need to know when to stop. Will the cabbage turn green at the end, or blue, or just a slightly paler pink? The answer depends on the pH at each stage, which depends on whether the acid is strong or weak, and on what buffer forms in the cup halfway through. The same questions decide which antacid works fastest, why rain is slightly acidic even in a clean forest, and why a pharmacist adds a buffer to eye drops.

## Core ideas

> [!NOTE]
> The theory is stable. $K_a$ values are from OpenStax Chemistry 2e Appendix H (25 °C) and the acetic acid $\mathrm{p}K_a$ 4.76 matches PubChem, both checked 2026-10-17. Red-cabbage colours vary with the cabbage and the extract strength; the colour chart is approximate.

### Brønsted acids and bases

A **Brønsted acid** is a proton (H⁺) donor; a **Brønsted base** is a proton acceptor. In water a bare proton never exists alone: it sits on a water molecule as the **hydronium ion**, H₃O⁺.

$$\mathrm{CH_3COOH + H_2O \rightleftharpoons H_3O^+ + CH_3COO^-}$$

Acetic acid gives its proton to water. On the right, acetate (CH₃COO⁻) can take a proton back, so it is a base: the **conjugate base** of acetic acid. Every acid–base reaction has two such **conjugate pairs**, differing by one H⁺. Water can act as either: it is a base above and an acid towards ammonia. Such substances are **amphiprotic**. The hydrogen carbonate ion HCO₃⁻ from baking soda is amphiprotic too.

### Water, Kw and the pH scale

Pure water ionises a tiny amount:

$$\mathrm{2H_2O \rightleftharpoons H_3O^+ + OH^-} \qquad K_w = [\mathrm{H_3O^+}][\mathrm{OH^-}] = 1.0 \times 10^{-14}\ \text{at 25 °C}$$

Concentrations span many powers of ten, so we use logarithms (lesson [02.1](../module-02/lesson-01.md)):

$$\mathrm{pH} = -\log_{10}[\mathrm{H_3O^+}], \qquad \mathrm{pOH} = -\log_{10}[\mathrm{OH^-}], \qquad \mathrm{pH} + \mathrm{pOH} = 14.00$$

Neutral is pH 7 at 25 °C, acidic below, basic above. One pH unit is a factor of ten in [H₃O⁺]: pH 3 has ten times more than pH 4. The number of decimal places in a pH equals the number of significant figures in the concentration: $[\mathrm{H_3O^+}] = 3.9 \times 10^{-3}$ M gives pH 2.41.

### Strong and weak acids

A **strong acid** ionises completely in water: HCl, HNO₃, H₂SO₄ (first proton). So $[\mathrm{H_3O^+}]$ equals the acid concentration: 0.010 M HCl has pH 2.00. A **weak acid** ionises only partly and reaches an equilibrium (lesson [08.3](lesson-03.md)) with the **acid ionisation constant**

$$K_a = \frac{[\mathrm{H_3O^+}][\mathrm{A^-}]}{[\mathrm{HA}]}, \qquad \mathrm{p}K_a = -\log_{10}K_a$$

Smaller $K_a$, larger $\mathrm{p}K_a$, weaker acid. Acetic acid: $K_a = 1.8 \times 10^{-5}$, $\mathrm{p}K_a = 4.74$ (PubChem lists 4.76; tables differ in the last digit). For a base B, $K_b$ is defined in the same way, and for a conjugate pair $K_a K_b = K_w$: the stronger the acid, the weaker its conjugate base.

"Strong" and "concentrated" are different ideas. Strong is about the *fraction* that ionises; concentrated is about how *much* is dissolved. Concentrated vinegar is still a weak acid.

### pH of a weak acid

With an initial concentration $c$, the ICE row is $c - x$, $x$, $x$, so

$$K_a = \frac{x^2}{c - x}$$

If $x \ll c$, then $x \approx \sqrt{K_a c}$. Otherwise solve the quadratic $x^2 + K_a x - K_a c = 0$. Diluting a weak acid raises the *fraction* ionised, because $x/c \approx \sqrt{K_a/c}$ grows as $c$ falls.

### Buffers and Henderson–Hasselbalch

A **buffer** is a solution of a weak acid and its conjugate base in similar amounts. Added H₃O⁺ is used up by the base; added OH⁻ is used up by the acid. So the pH barely moves. Rearranging $K_a$ and taking logs gives the **Henderson–Hasselbalch equation**:

$$\mathrm{pH} = \mathrm{p}K_a + \log_{10}\frac{[\mathrm{A^-}]}{[\mathrm{HA}]}$$

With equal amounts of acid and base, the log term is zero and pH = p$K_a$. A buffer works best within about one pH unit of its p$K_a$, where neither form runs out. Blood uses the H₂CO₃/HCO₃⁻ pair; the full treatment of buffer capacity comes in Module 9.

### Indicators

An **indicator** is a weak acid, HIn, whose acid and base forms have different colours. By Henderson–Hasselbalch, the colour switches over about p$K_\text{In} \pm 1$. Red cabbage contains **anthocyanins**, a family of pigments with several proton-loss steps, so instead of one switch it runs through a whole rainbow:

| pH (approximate) | below 3 | 3–5 | 5–6.5 | 6.5–7.5 | 7.5–9 | 9–12 | above 12 |
|---|---|---|---|---|---|---|---|
| Cabbage colour | red | pink | violet | purple | blue | green | yellow |

That makes it a cheap universal indicator, accurate to about one pH unit.

## Worked example

### 1. The pH of vinegar

Kitchen vinegar is 5 % acidity: 50 g of acetic acid per litre. $c = 50 / 60.05 = 0.833$ M.

Small-x: $x = \sqrt{1.8 \times 10^{-5} \times 0.833} = 3.87 \times 10^{-3}$ M. Check: $x/c = 0.46\,\%$, well under 5 %, so the shortcut is fine. pH $= -\log_{10}(3.87 \times 10^{-3}) = 2.41$.

Only half a percent of the acetic acid molecules are ionised. Compare 0.833 M HCl, which would have pH 0.08. Same concentration, about two hundred times less H₃O⁺: that is what "weak" means.

### 2. Half-neutralised vinegar is a buffer

Add 0.35 g of baking soda (4.17 mmol) to 10 mL of vinegar (8.33 mmol acetic acid). The reaction

$$\mathrm{CH_3COOH + HCO_3^- \rightarrow CH_3COO^- + H_2O + CO_2(g)}$$

goes essentially to completion because the CO₂ fizzes away (Le Chatelier, lesson 08.3). It leaves 4.16 mmol acid and 4.17 mmol acetate. Volumes cancel in the ratio, so

$$\mathrm{pH} = 4.74 + \log_{10}\frac{4.17}{4.16} = 4.74$$

The cup is now a buffer. Add a few more drops of vinegar or a pinch more soda and the pH hardly changes, which is why, in a titration, the indicator sits on one colour for most of the run and then switches suddenly near the end.

## Hands-on

What you need: a quarter of a red cabbage, a kettle, a heat-proof jug, a sieve, 6–8 small clear glasses or cups, teaspoons, a pipette or oral syringe, and test liquids: white vinegar, lemon juice, baking soda (1 teaspoon in 100 mL water), hand soap or bar soap shaken in water, tap water, sparkling water. Optional: an antacid tablet from the pharmacy. Also the [Module 8 lab folder](../../labs/module-08/) with Python 3.14. Time: about 1 hour.

### Part A — home: a red-cabbage indicator (35 min)

> [!WARNING]
> Boiling water scalds: pour it carefully and let the jug cool before handling. Wear safety glasses while testing, and rinse any splash from your eyes with plenty of water. Test only food, drink and personal-care liquids. Do not test bleach, oven cleaner, drain cleaner or descaler, and never mix bleach with anything: with acids such as vinegar it releases toxic chlorine.

1. Chop the cabbage finely, put it in the jug and cover it with about 500 mL of just-boiled water. Stir and leave it 15 minutes until the water is deep purple. Strain. This is your indicator; it keeps a few days in the fridge.
2. Pour about 30 mL of indicator into each glass. Label the glasses.
3. Before adding anything, write a predicted pH and colour for each liquid in your notebook, using the table in Core ideas.
4. Add the test liquids one at a time, about 1 teaspoon each, and stir. Photograph all the glasses side by side on a white background.
5. Into the vinegar glass, add baking-soda solution a few drops at a time, stirring. Watch the colour as it passes through the buffer region and beyond.

How you know it worked: vinegar and lemon go red to pink, tap water stays purple, sparkling water turns slightly pinker than tap water, baking soda goes blue to blue-green, and most soaps go blue-green or green. In step 5 the colour stays pink for a long time, then moves quickly through purple to blue when the acid is used up. Record everything on a [notebook page](../../templates/notebook-page.md).

<details><summary>Explaining your result</summary>

Vinegar (pH about 2.4) and lemon juice (citric acid, measured pH usually 2–2.6) are both acidic. Sparkling water is a solution of CO₂, which forms carbonic acid, so it is a little more acidic than tap water. Baking soda is amphiprotic and gives about pH 8.3. Soaps are salts of fatty acids (weak acids) with sodium or potassium hydroxide, so they are basic; many liquid hand soaps are buffered to pH 5–7 for the skin, and then stay purple. If your colours differ by one step from the chart, that is normal: the extract strength and the cabbage both matter. In step 5, the pink plateau is the acetic acid/acetate buffer of Worked example 2.

</details>

### Part B — Python: predict the pH (20 min)

Open `lesson04_ph.py` and write the two TODO functions: `ph_weak_acid` (the exact quadratic) and `ph_buffer` (Henderson–Hasselbalch). Then run:

```bash
py lesson04_ph.py
```

How you know it worked: 0.010 M HCl 2.00; 5 % vinegar 2.41; vinegar diluted 1 : 10 2.92; water open to air 5.65; baking soda 8.35; the half-neutralised vinegar 4.75. The script prints the cabbage colour for each, and the small-x check for vinegar (0.46 %). Compare each prediction with your glasses from Part A, and explain any that disagree.

<details><summary>Reference solution</summary>

`ph_weak_acid`: `x = (-ka + math.sqrt(ka * ka + 4 * ka * c)) / 2`, then `return -math.log10(x)`. `ph_buffer`: `return -math.log10(ka) + math.log10(n_base / n_acid)`. Full code in `lesson04_ph_solution.py`.

Diluting vinegar ten times raises the pH by only 0.5, not 1, because the fraction ionised rises from 0.46 % to 1.5 %. Water open to air is pH 5.6, not 7, because it dissolves CO₂ from the air (about 0.042 %): this is why clean rain is slightly acidic.

</details>

### Part C — pencil (5 min)

1. What is the pH of a solution with $[\mathrm{OH^-}] = 2.0 \times 10^{-4}$ M?
2. Formic acid has $K_a = 1.8 \times 10^{-4}$. Is 0.10 M formic acid more or less acidic than 0.10 M acetic acid, and by how many pH units, roughly?

<details><summary>Answers to Part C</summary>

1. pOH $= 3.70$, so pH $= 14.00 - 3.70 = 10.30$.
2. More acidic. $K_a$ is ten times larger, $x \approx \sqrt{K_a c}$ is $\sqrt{10} = 3.2$ times larger, so the pH is about 0.5 lower (2.4 against 2.9).

</details>

## Common mistakes

- **Treating a weak acid as strong.** Writing pH = $-\log c$ for vinegar gives 0.08 instead of 2.41. Check the $K_a$ table first.
- **Confusing strong with concentrated.** Concentration says how much; strength says what fraction ionises.
- **Natural log instead of log₁₀.** pH uses base 10. $\ln(3.87 \times 10^{-3}) = -5.55$ is not the pH.
- **Using Henderson–Hasselbalch with only acid or only base present.** It needs both forms in similar amounts; for a pure weak acid, use the ICE table.
- **Forgetting pH + pOH = 14 only at 25 °C.** $K_w$ grows with temperature; at 37 °C, neutral water has pH 6.8.
- **Expecting cabbage to give an exact pH.** It brackets the pH to about one unit; use a pH meter or the titration curve for more.

## Key takeaways

- An acid donates H⁺, a base accepts it; each acid has a conjugate base. Water and HCO₃⁻ can do both.
- pH $= -\log_{10}[\mathrm{H_3O^+}]$; pH + pOH = 14.00 at 25 °C; one unit is a factor of ten.
- Strong acids ionise completely. A weak acid has $K_a$; its pH comes from $x^2/(c - x) = K_a$, with $x \approx \sqrt{K_a c}$ when the 5 % check passes.
- A buffer holds a weak acid and its conjugate base; pH $= \mathrm{p}K_a + \log_{10}([\mathrm{A^-}]/[\mathrm{HA}])$.
- Indicators are weak acids with coloured forms; red cabbage gives a rainbow from red (acid) to green and yellow (base).

## Sources

- [OpenStax Chemistry 2e, 14.1 Brønsted-Lowry Acids and Bases](https://openstax.org/books/chemistry-2e/pages/14-1-bronsted-lowry-acids-and-bases) — definitions, conjugate pairs, amphiprotic species, $K_w$.
- [OpenStax Chemistry 2e, 14.2 pH and pOH](https://openstax.org/books/chemistry-2e/pages/14-2-ph-and-poh) — the pH scale and significant figures.
- [OpenStax Chemistry 2e, 14.3 Relative Strengths of Acids and Bases](https://openstax.org/books/chemistry-2e/pages/14-3-relative-strengths-of-acids-and-bases) — $K_a$, $K_b$, $K_aK_b = K_w$, weak-acid pH.
- [OpenStax Chemistry 2e, 14.6 Buffers](https://openstax.org/books/chemistry-2e/pages/14-6-buffers) — Henderson–Hasselbalch, buffer range.
- [OpenStax Chemistry 2e, Appendix H](https://openstax.org/books/chemistry-2e/pages/h-ionization-constants-of-weak-acids) — $K_a$ of acetic acid, H₂CO₃ and HCO₃⁻.
- [RSC, Making a pH indicator using red cabbage](https://edu.rsc.org/experiments/making-a-ph-indicator-using-red-cabbage/422.article) — the classroom method.
- [RHS, Red cabbage indicator colour chart](https://www.rhs.org.uk/getmedia/386dd481-7d8c-43c0-b64e-ff66bf02dbe9/Res-L-Red-Cabbage-Indicator-Colour-Chart.pdf) — approximate colours from pH 1 to 14.
- [PubChem, Acetic acid](https://pubchem.ncbi.nlm.nih.gov/compound/176) — p$K_a$ 4.76 at 25 °C; GHS H226 and H314 for the concentrated acid (household vinegar is about 5 % and far milder).
