---
id: "08.5"
module: 8
minutes: 20
practice_minutes: 75
prerequisites: ["08.4", "03.1"]
objectives:
  - Assign oxidation numbers and identify the species oxidised and reduced, and the oxidising and reducing agents, in a reaction.
  - Balance a redox equation by the half-reaction method in acidic and in basic solution.
  - Balance any equation as a linear system by finding the null space of its composition matrix.
  - Measure the vitamin C content of a juice by redox titration with povidone-iodine and starch.
volatility: concept
sources:
  - title: "OpenStax Chemistry 2e, 17.1 Review of Redox Chemistry"
    url: https://openstax.org/books/chemistry-2e/pages/17-1-review-of-redox-chemistry
  - title: "OpenStax Chemistry 2e, 4.2 Classifying Chemical Reactions (oxidation numbers)"
    url: https://openstax.org/books/chemistry-2e/pages/4-2-classifying-chemical-reactions
  - title: "OpenStax Chemistry 2e, Appendix L: Standard Electrode (Half-Cell) Potentials"
    url: https://openstax.org/books/chemistry-2e/pages/l-standard-electrode-half-cell-potentials
  - title: "PubChem, L-Ascorbic acid (CID 54670067)"
    url: https://pubchem.ncbi.nlm.nih.gov/compound/54670067
  - title: "PubChem, Povidone-iodine (CID 410087)"
    url: https://pubchem.ncbi.nlm.nih.gov/compound/410087
  - title: "SciPy documentation, scipy.linalg.null_space"
    url: https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.null_space.html
last_verified: "2026-10-17"
---

# 08.5 · Redox reactions and balancing

In an acid–base reaction a proton moves from one species to another. In a redox reaction an electron moves. Rusting, burning, batteries, bleaching, breathing and the vitamin C in your juice are all redox chemistry. This lesson gives you the bookkeeping: oxidation numbers to see who loses electrons and who gains them, the half-reaction method to balance the equations, and a linear-algebra method that balances any equation at all. You will finish by measuring vitamin C in juice with a pharmacy iodine antiseptic.

## Why it matters

A food lab must check that a carton of orange juice holds the vitamin C on its label. A water engineer must know how much chlorine a reservoir will use up. A breathalyser turns a colour in proportion to the alcohol in breath. All three are redox titrations or redox sensors, and each calculation starts from a correctly balanced equation. Get one coefficient wrong and the result is off by a factor of two or five. Balancing redox equations by inspection rarely works; you need a method that always does.

## Core ideas

> [!NOTE]
> The rules here are stable. The povidone-iodine strength (10 % povidone-iodine = 1 % available iodine) is the usual pharmacy product as sold in 2026; check the label of yours. SciPy 1.18.1 is the version pinned for this course (checked 2026-10-16).

### Oxidation and reduction

**Oxidation** is loss of electrons; **reduction** is gain of electrons. They always happen together: electrons lost by one species are gained by another. The species that is reduced takes electrons from the other one, so it is the **oxidising agent**; the species oxidised is the **reducing agent**.

$$\mathrm{Zn(s) + Cu^{2+}(aq) \rightarrow Zn^{2+}(aq) + Cu(s)}$$

Zinc loses two electrons (oxidised, the reducing agent). Cu²⁺ gains two (reduced, the oxidising agent). A memory aid: "OIL RIG", oxidation is loss, reduction is gain.

### Oxidation numbers

For molecules, electrons are shared, so we use **oxidation numbers**: the charge an atom would have if every bond were fully ionic, with the electrons given to the more electronegative atom (lesson [07.3](../module-07/lesson-03.md)). The rules, in order of priority:

1. An atom in an element is 0 (Zn, O₂, Cl₂).
2. A monatomic ion has its charge (Cu²⁺ is +2).
3. Fluorine is −1. Oxygen is −2, except in peroxides (−1). Hydrogen is +1 with non-metals, −1 in metal hydrides.
4. The oxidation numbers in a species add up to its charge.

Example, permanganate MnO₄⁻: four O at −2 give −8; the total is −1; so Mn is +7. In Mn²⁺ it is +2. Going from +7 to +2, manganese gains 5 electrons: it is reduced. An increase in oxidation number is oxidation; a decrease is reduction.

### Half-reactions in acid

Split the reaction into an oxidation half and a reduction half, balance each, then add them so the electrons cancel. In acidic solution:

1. Balance the atoms other than O and H.
2. Balance O by adding H₂O.
3. Balance H by adding H⁺.
4. Balance charge by adding electrons, e⁻.
5. Multiply each half so both have the same number of electrons, add, cancel what appears on both sides.

For permanganate oxidising iron(II):

$$\mathrm{MnO_4^- + 8H^+ + 5e^- \rightarrow Mn^{2+} + 4H_2O} \qquad \text{(reduction)}$$

$$\mathrm{Fe^{2+} \rightarrow Fe^{3+} + e^-} \qquad \text{(oxidation, } \times 5\text{)}$$

$$\mathrm{MnO_4^- + 5Fe^{2+} + 8H^+ \rightarrow Mn^{2+} + 5Fe^{3+} + 4H_2O}$$

Check: Mn 1 = 1, Fe 5 = 5, O 4 = 4, H 8 = 8, charge $-1 + 10 + 8 = 17$ on the left, $2 + 15 = 17$ on the right. Always check both atoms and charge.

### Half-reactions in base

In basic solution there is almost no H⁺. Balance as if in acid, then add as many OH⁻ to *both* sides as there are H⁺. Each H⁺ + OH⁻ becomes H₂O; cancel waters that appear on both sides. Permanganate in base is reduced only to MnO₂:

$$\mathrm{MnO_4^- + 2H_2O + 3e^- \rightarrow MnO_2 + 4OH^-}$$

### Balancing as linear algebra

Any chemical equation, redox or not, says that each element and the total charge are conserved. Give each species an unknown coefficient. Each element gives one linear equation, and charge gives one more. This is a homogeneous system $A\mathbf{x} = \mathbf{0}$ (lesson [03.1](../module-03/lesson-01.md)), where $A$ is the **composition matrix**: one row per element plus a charge row, one column per species, with reactant columns positive and product columns negative. The coefficients are a vector in the **null space** of $A$.

For $\mathrm{Fe^{2+} + MnO_4^- + H^+ \rightarrow Fe^{3+} + Mn^{2+} + H_2O}$:

| | Fe²⁺ | MnO₄⁻ | H⁺ | Fe³⁺ | Mn²⁺ | H₂O |
|---|---|---|---|---|---|---|
| Fe | 1 | 0 | 0 | −1 | 0 | 0 |
| Mn | 0 | 1 | 0 | 0 | −1 | 0 |
| O | 0 | 4 | 0 | 0 | 0 | −1 |
| H | 0 | 0 | 1 | 0 | 0 | −2 |
| charge | 2 | −1 | 1 | −3 | −2 | 0 |

Five equations, six unknowns, rank 5: the null space is one line, and scaling it to the smallest whole numbers gives 5, 1, 8, 5, 1, 4. If the null space has two or more dimensions, the equation describes two independent reactions mixed together, and chemistry, not algebra, must decide the ratio.

## Worked example

### Vitamin C and iodine: the equation behind the titration

Vitamin C is ascorbic acid, C₆H₈O₆ (176.12 g/mol). It is a reducing agent: iodine oxidises it to dehydroascorbic acid, C₆H₆O₆, and is itself reduced to iodide. Starch turns deep blue-black with iodine but not with iodide, so the blue colour disappears when all the iodine is used up. That moment is the **end point**.

Half-reactions (acidic, since ascorbic acid is an acid):

$$\mathrm{C_6H_8O_6 \rightarrow C_6H_6O_6 + 2H^+ + 2e^-} \qquad \text{(oxidation)}$$

$$\mathrm{I_2 + 2e^- \rightarrow 2I^-} \qquad \text{(reduction)}$$

$$\mathrm{C_6H_8O_6 + I_2 \rightarrow C_6H_6O_6 + 2I^- + 2H^+}$$

The ratio is 1 : 1. Pharmacy povidone-iodine 10 % contains 1 % available iodine: 10 mg I₂ per mL. So 1.00 mL holds $10 / 253.8 = 0.0394$ mmol I₂, which reacts with 0.0394 mmol ascorbic acid, or $0.0394 \times 176.12 = 6.94$ mg.

If 1.00 mL of povidone-iodine needs 14.0 mL of orange juice to lose its colour, the juice contains $6.94 / 14.0 = 0.50$ mg of vitamin C per mL, or 50 mg per 100 mL. A fresh orange juice typically has 30–60 mg per 100 mL.

The "1 % available iodine" is a label value with a tolerance, and iodine slowly escapes from an opened bottle. So in the hands-on you first **standardise** the iodine against a vitamin C tablet of known mass, then measure the juice. That cancels the uncertainty in the label.

## Hands-on

What you need: povidone-iodine 10 % solution (pharmacy antiseptic), a 500 mg vitamin C tablet (plain, not effervescent), orange juice (fresh or carton), cornflour, a kettle, a 1 mL and a 10 mL oral syringe, clear cups, a kitchen scale, a white sheet of paper, and the [Module 8 lab folder](../../labs/module-08/) with Python 3.14. Time: about 75 minutes.

### Part A — home: vitamin C by redox titration (45 min)

> [!WARNING]
> Povidone-iodine stains skin, clothes and counters; it irritates eyes. Do not use it if you are allergic to iodine. Wear safety glasses, rinse splashes with water, and work on a tray. Do not drink any of the mixtures; label the cups and pour them away down the sink with plenty of water when done. Take care with boiling water for the starch.

1. **Starch indicator.** Stir 1 level teaspoon of cornflour into a little cold water, pour on 100 mL of boiling water, stir and let it cool.
2. **Standard vitamin C.** Crush the tablet, dissolve it in water and make it up to 500 g on the scale (500 mL). That is 1.00 mg/mL if the tablet holds 500 mg. Some filler will stay undissolved; let it settle and use the clear top.
3. **Iodine cup.** With the 1 mL syringe, put exactly 1.00 mL of povidone-iodine into a cup, add about 50 mL of water and 1 teaspoon of starch. It turns blue-black.
4. **Standardise.** Fill the 10 mL syringe with vitamin C solution. Add it to the cup on the white paper, 1 mL at a time with swirling, then a few drops at a time near the end. Stop when the blue just disappears and does not come back within 30 seconds. Record the volume. Repeat twice more.
5. **Juice.** Repeat steps 3–4 with strained juice instead of the standard. Expect 10–25 mL; refill the syringe and add the volumes. The end point is the change from dark blue-grey to the plain colour of the juice.
6. Record all volumes in a table on a [notebook page](../../templates/notebook-page.md).

How you know it worked: the three standardisation volumes agree within about 0.3 mL and lie near 6.9 mL (5.5–8 mL is normal, depending on the iodine). The juice volumes agree within about 1 mL.

<details><summary>Calculation and expected result</summary>

From the standardisation, 1.00 mL of iodine solution reacts with $V_\text{std} \times 1.00$ mg of vitamin C. For example $V_\text{std}$ = 7.2 mL gives 7.2 mg. If the juice needed $V_\text{juice}$ = 15.0 mL, the juice has $7.2 / 15.0 = 0.48$ mg/mL, or 48 mg per 100 mL. Compare with the label if there is one. Carton juice that has been open a few days usually comes out lower: dissolved oxygen slowly oxidises vitamin C, the same kind of reaction with O₂ as the oxidising agent.

</details>

### Part B — pencil (15 min)

1. Give the oxidation number of: (a) S in SO₄²⁻, (b) Cr in Cr₂O₇²⁻, (c) C in CH₄ and in CO₂, (d) O in H₂O₂.
2. Balance in acid: $\mathrm{Cu + NO_3^- \rightarrow Cu^{2+} + NO}$.
3. In a breathalyser, orange dichromate (Cr₂O₇²⁻) oxidises ethanol to acetic acid and becomes green Cr³⁺. Which is the oxidising agent, and how many electrons does each Cr gain?

<details><summary>Answers to Part B</summary>

1. (a) +6; (b) +6; (c) −4 in CH₄, +4 in CO₂, so burning methane oxidises carbon by 8 electrons; (d) −1 (peroxide).
2. Reduction $\mathrm{NO_3^- + 4H^+ + 3e^- \rightarrow NO + 2H_2O}$ (×2); oxidation $\mathrm{Cu \rightarrow Cu^{2+} + 2e^-}$ (×3). Sum: $\mathrm{3Cu + 2NO_3^- + 8H^+ \rightarrow 3Cu^{2+} + 2NO + 4H_2O}$. Charge: $-2 + 8 = +6$ on both sides.
3. Dichromate is the oxidising agent; each Cr goes from +6 to +3, gaining 3 electrons (6 per Cr₂O₇²⁻).

</details>

### Part C — Python: a balancer that always works (15 min)

Open `lesson05_redox.py` and write `composition_matrix`: one row per element (the count in each species, times +1 for reactants and −1 for products) and a last row for charge. The rest is done for you: `scipy.linalg.null_space` finds the null space and `smallest_integers` scales it to whole numbers. Run:

```bash
py lesson05_redox.py
py lesson05_redox.py "MnO4^- + C2O4^2- + H^+ -> Mn^2+ + CO2 + H2O"
```

How you know it worked: the six built-in examples print the permanganate–iron equation 5, 1, 8 → 5, 1, 4; copper and nitrate 3, 2, 8 → 3, 2, 4; vitamin C and iodine 1, 1 → 1, 2, 2; the breathalyser 2, 3, 16 → 4, 3, 11; permanganate and iodide in base 2, 6, 4 → 2, 3, 8; and propane 1, 5 → 3, 4. The oxalate line gives 2, 5, 16 → 2, 10, 8. Then try `"H2 + O2 -> H2O + H2O2"` and read the message.

<details><summary>Reference solution</summary>

```python
rows = [[sign * atoms.get(el, 0) for (atoms, _), sign in zip(species, signs)] for el in elements]
rows.append([sign * charge for (_, charge), sign in zip(species, signs)])
```

Full code in `lesson05_redox_solution.py`. For H₂ + O₂ → H₂O + H₂O₂ the null space is two-dimensional: water and hydrogen peroxide can form in any ratio, so there is no single balanced equation. The algebra tells you when the chemistry is under-specified.

</details>

## Common mistakes

- **Balancing atoms but not charge.** $\mathrm{Fe^{2+} + MnO_4^- + 8H^+ \rightarrow Fe^{3+} + Mn^{2+} + 4H_2O}$ balances every atom, but the charges are +9 and +5. Always check charge last.
- **Adding O₂ or O atoms to balance oxygen.** In water, use H₂O and H⁺ (or OH⁻ in base), never free O.
- **Mixing up agent and process.** The oxidising agent is the one *reduced*. Write "X is reduced, so X is the oxidising agent" every time.
- **Forgetting peroxides and hydrides.** O in H₂O₂ is −1, H in NaH is −1.
- **Using H⁺ in a basic solution.** Convert with OH⁻ at the end, adding it to both sides.
- **Overshooting the iodine end point.** Near the end add drops, swirl, and wait.

## Key takeaways

- Oxidation is loss of electrons (oxidation number up); reduction is gain (oxidation number down). The oxidising agent is reduced.
- Oxidation numbers follow a short list of rules and add up to the charge of the species.
- Half-reactions in acid: balance other atoms, then O with H₂O, H with H⁺, charge with e⁻; equalise electrons and add. In base, neutralise H⁺ with OH⁻.
- Every balanced equation is a null-space vector of the composition matrix; a two-dimensional null space means two independent reactions.
- Vitamin C reduces iodine 1 : 1 and starch marks the end point; standardise the iodine against a known tablet.

## Sources

- [OpenStax Chemistry 2e, 17.1 Review of Redox Chemistry](https://openstax.org/books/chemistry-2e/pages/17-1-review-of-redox-chemistry) — half-reaction method in acid and base.
- [OpenStax Chemistry 2e, 4.2 Classifying Chemical Reactions](https://openstax.org/books/chemistry-2e/pages/4-2-classifying-chemical-reactions) — oxidation-number rules, oxidising and reducing agents.
- [OpenStax Chemistry 2e, Appendix L](https://openstax.org/books/chemistry-2e/pages/l-standard-electrode-half-cell-potentials) — half-reactions used here, in reduction form.
- [PubChem, L-Ascorbic acid](https://pubchem.ncbi.nlm.nih.gov/compound/54670067) — C₆H₈O₆, 176.12 g/mol, not GHS-classified.
- [PubChem, Povidone-iodine](https://pubchem.ncbi.nlm.nih.gov/compound/410087) — the antiseptic complex; pharmacy 10 % solutions are labelled 1 % available iodine.
- [SciPy, `scipy.linalg.null_space`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.null_space.html) — the function used in the balancer.
