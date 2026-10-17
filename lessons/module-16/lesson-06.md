---
id: "16.6"
module: 16
minutes: 24
practice_minutes: 70
prerequisites: ["16.5", "16.2", "06.3"]
objectives:
  - Rank amines, anilines, amides and nitrogen heterocycles by basicity, and calculate the fraction protonated at pH 7.4.
  - Choose a route to a primary, secondary or tertiary amine (reductive amination, nitro or nitrile reduction) and explain why direct alkylation of ammonia fails.
  - Draw glucose as a cyclic hemiacetal, identify the anomeric carbon, and calculate the α : β ratio at equilibrium from optical rotation data.
  - Classify pyridine, pyrrole, furan and imidazole as aromatic, and say whose lone pair is available for protonation.
volatility: concept
sources:
  - title: "OpenStax Organic Chemistry (2023), 24.3 Basicity of Amines"
    url: https://openstax.org/books/organic-chemistry/pages/24-3-basicity-of-amines
  - title: "OpenStax Organic Chemistry (2023), 24.6 Synthesis of Amines"
    url: https://openstax.org/books/organic-chemistry/pages/24-6-synthesis-of-amines
  - title: "OpenStax Organic Chemistry (2023), 24.9 Heterocyclic Amines"
    url: https://openstax.org/books/organic-chemistry/pages/24-9-heterocyclic-amines
  - title: "OpenStax Organic Chemistry (2023), 25.5 Cyclic Structures of Monosaccharides: Anomers"
    url: https://openstax.org/books/organic-chemistry/pages/25-5-cyclic-structures-of-monosaccharides-anomers
  - title: "OpenStax Organic Chemistry (2023), 25.6 Reactions of Monosaccharides"
    url: https://openstax.org/books/organic-chemistry/pages/25-6-reactions-of-monosaccharides
  - title: "OpenStax Organic Chemistry (2023), 15.5 Aromatic Heterocycles: Pyridine and Pyrrole"
    url: https://openstax.org/books/organic-chemistry/pages/15-5-aromatic-heterocycles-pyridine-and-pyrrole
  - title: "PubChem: alpha-D-glucopyranose (CID 79025)"
    url: https://pubchem.ncbi.nlm.nih.gov/compound/79025
  - title: "PubChem: beta-D-glucopyranose (CID 64689)"
    url: https://pubchem.ncbi.nlm.nih.gov/compound/64689
last_verified: "2026-10-17"
---

# 16.6 · Amines, sugars and heterocycles

Three families meet in this lesson because they share one idea from lesson 16.2: a lone pair or an OH group attacking a carbonyl. Amines are the organic bases; how basic they are decides whether a drug is charged in your blood. Sugars are polyhydroxy aldehydes and ketones that close into rings by forming hemiacetals with themselves. Heterocycles, rings that contain N, O or S, combine both ideas with the aromaticity of lesson 16.5, and they make up the bases of DNA. A kitchen experiment, browning toast, joins amines and sugars in one reaction.

## Why it matters

Imidazole has a conjugate-acid $\mathrm{p}K_a$ of 6.95, almost exactly the pH inside a cell. That is why histidine, the amino acid with an imidazole side chain, is the residue enzymes use to pass protons back and forth: at pH 7.4 it is about a quarter protonated, so it can give or take a proton with little energy cost. Ethylamine, $\mathrm{p}K_{aH}$ 10.75, is more than 99.9 % protonated at the same pH and is useless for that job. Telling those two apart takes one $\mathrm{p}K_a$ comparison, and the same comparison tells a formulation chemist whether an amine drug needs to be sold as its hydrochloride salt to dissolve.

## Core ideas

> [!NOTE]
> Amine basicity, sugar ring chemistry and heterocyclic aromaticity are settled theory. The $\mathrm{p}K_{aH}$ values are from OpenStax 24.3; the rotations of glucose (α +112.2, β +18.7, equilibrium +52.6) and the 37 : 63 ratio are from OpenStax 25.5; glucose structures from PubChem. All checked 2026-10-17.

### Amines as bases

An amine is ammonia with one, two or three H replaced by carbon groups (primary, secondary, tertiary). The N lone pair makes amines bases and nucleophiles. Basicity is quoted as the $\mathrm{p}K_a$ of the conjugate acid, $\mathrm{p}K_{aH}$: the higher it is, the stronger the base.

| Base | $\mathrm{p}K_{aH}$ | Why |
|---|---|---|
| pyrrolidine | 11.27 | alkyl groups donate; ring holds the lone pair exposed |
| ethylamine | 10.75 | alkyl donation |
| ammonia | 9.26 | reference |
| imidazole | 6.95 | sp² N; the cation is stabilised by resonance over both N |
| pyridine | 5.25 | sp² lone pair: more s character, held closer to N |
| aniline | 4.63 | lone pair delocalised into the ring |
| pyrrole | 0.4 | lone pair is part of the aromatic sextet; it protonates on carbon |

**Amides are not basic** in water: the N lone pair is delocalised into the C=O (lesson [16.3](lesson-03.md)), and strong acid protonates the oxygen instead.

The fraction protonated follows from Henderson–Hasselbalch, as for acids in lesson 16.3:

$$\%\,\mathrm{BH^+} = \frac{100}{1 + 10^{\,\mathrm{pH} - \mathrm{p}K_{aH}}}$$

### Making amines

Ammonia plus an alkyl halide (SN2) does not stop at the primary amine: the product is a better nucleophile than ammonia and reacts again, giving a mixture up to the quaternary ammonium salt. Better routes:

- **Reductive amination**: an aldehyde or ketone plus ammonia or an amine gives an imine (lesson [16.2](lesson-02.md)); NaBH₃CN reduces the C=N as it forms. Ammonia gives a primary amine, a primary amine a secondary one, a secondary amine a tertiary one. This is the most used route in medicinal chemistry.
- **Reduction of nitro groups**: Fe or Sn with HCl, or H₂ over Pd, turns ArNO₂ into ArNH₂. Nitration (lesson [16.5](lesson-05.md)) then reduction is how anilines are made.
- **Reduction of nitriles and amides** with LiAlH₄ (lesson 16.3).

### Sugars: hemiacetals that close on themselves

Glucose, C₆H₁₂O₆, is an aldohexose: a six-carbon chain with an aldehyde at C1 and OH groups on C2–C6. Its four stereocentres (C2–C5) are drawn in a **Fischer projection**; the OH on C5, the stereocentre furthest from C=O, points right, which makes it a **D**-sugar.

In water, the C5 OH attacks the C1 aldehyde: an intramolecular hemiacetal, a six-membered ring called a **pyranose**. C1 becomes a new stereocentre, the **anomeric carbon**. The two possible configurations are the **anomers**:

- **α-D-glucopyranose**: anomeric OH axial in the chair (trans to the CH₂OH on C5), $[\alpha]_D$ = +112.2;
- **β-D-glucopyranose**: anomeric OH equatorial; every substituent on the chair is equatorial (lesson [15.2](../module-15/lesson-02.md)), $[\alpha]_D$ = +18.7.

Dissolve either one and the rotation drifts to +52.6 over a few hours: **mutarotation**. The ring opens to the aldehyde (under 0.1 % at any moment), rotates, and closes again from either face. At equilibrium the mixture is 37 % α and 63 % β.

Because the ring is a hemiacetal, sugars react as aldehydes:

- **Glycosides**: with an alcohol and acid, the anomeric OH is replaced by OR, giving an acetal. Glycosides no longer open, so they do not mutarotate. Methyl glucoside is the simplest; the bonds that link sugars in starch, cellulose and DNA are all glycosidic.
- **Reducing sugars**: sugars with a free hemiacetal reduce mild oxidants such as Tollens' or Benedict's reagent (the open aldehyde is oxidised to an acid). Sucrose has both anomeric carbons tied up in its glycosidic bond and is non-reducing.
- **Starch versus cellulose**: both are glucose chains linked C1 to C4. Starch uses α links and coils; cellulose uses β links, which stack into straight, hydrogen-bonded fibres that human enzymes cannot cut.

### Heterocycles

Lesson 16.5 counted π electrons in pyridine, pyrrole and furan; here is what follows for reactions:

- **Pyridine** is aromatic and basic (lone pair in the ring plane). Its ring N pulls electron density like a nitro group, so EAS is very slow and goes to C3.
- **Pyrrole and furan** are aromatic because the heteroatom's lone pair is in the ring. They are electron-rich, much more reactive than benzene in EAS, at C2.
- **Imidazole** has one pyridine-like N (basic) and one pyrrole-like N–H. **Pyrimidine** and **purine** rings carry the bases of DNA and RNA (lesson [06.3](../module-06/lesson-03.md)): cytosine, thymine and uracil are pyrimidines; adenine and guanine are purines.

### The Maillard reaction: amines meet sugars

When food is heated, the amino groups of proteins add to the open-chain aldehyde of reducing sugars to form imines (lesson 16.2). These rearrange (the Amadori rearrangement) and then break down and recombine into hundreds of flavour compounds and brown polymers. It is faster at higher pH, which is why pretzels are dipped in alkaline solution before baking.

## Worked example

### 1. Charged or neutral at pH 7.4?

Imidazole, $\mathrm{p}K_{aH}$ = 6.95:

$$\%\,\mathrm{BH^+} = \frac{100}{1 + 10^{7.4 - 6.95}} = \frac{100}{1 + 2.82} = 26\ \%$$

Ethylamine, $\mathrm{p}K_{aH}$ = 10.75: $100/(1 + 10^{-3.35}) = 99.96$ %. Aniline, 4.63: $100/(1 + 10^{2.77}) = 0.17$ %. Rule of thumb: a base is mostly protonated at any pH more than one unit below its $\mathrm{p}K_{aH}$, and mostly neutral more than one unit above. Amine drugs are often sold as hydrochloride salts because the protonated form dissolves in water.

### 2. Anomer ratio from optical rotation

The equilibrium rotation is the mole-fraction-weighted average of the two anomers (the open chain is negligible):

$$52.6 = x_\beta (18.7) + (1 - x_\beta)(112.2) \;\Rightarrow\; x_\beta = \frac{112.2 - 52.6}{112.2 - 18.7} = 0.637$$

So 64 % β and 36 % α, matching the reported 63 : 37. The free-energy difference at 298 K is $\Delta G^\circ = -RT\ln(0.637/0.363) = -1.4$ kJ/mol in favour of β, the anomer with every group equatorial (compare 7.6 kJ/mol for one methyl group in methylcyclohexane, lesson 15.2: the anomeric OH has a smaller preference, for reasons studied in Module 28).

## Hands-on

What you need: the [Module 16 lab folder](../../labs/module-16/) with Python 3.14, RDKit 2026.9.1 and scipy (all pinned in `labs/common/requirements.txt`); for Part A, a toaster or oven, three slices of the same white bread, a little milk, baking soda, a teaspoon, a pastry brush or clean fingers, and your phone camera; a [notebook page](../../templates/notebook-page.md). Time: about 70 minutes.

### Part A — kitchen: Maillard browning on toast (20 min)

> [!CAUTION]
> Toasters and ovens are hot and toasters are live electrical devices. Never put a knife or other metal into a toaster, unplug it before freeing a stuck slice, and use oven gloves. Do not leave the toaster unattended. Food-grade materials only; eat nothing that is burnt.

1. Mark three slices A, B and C with a toothpick on one corner.
2. Brush A with 1 teaspoon of water, B with 1 teaspoon of milk (proteins and lactose, a reducing sugar), and C with 1 teaspoon of water in which you have dissolved a pinch (about 0.5 g) of baking soda (pH about 8).
3. Toast all three together, side by side in the oven or one after another for the same time in the toaster, on a medium setting.
4. Photograph them together in the same light. Rank the browning and note the smell.

Expected result: B and C are browner than A. Milk adds both amines and reducing sugar; baking soda raises the pH, which keeps more amino groups as free, unprotonated nucleophiles ($\mathrm{p}K_{aH}$ of lysine side chains about 10.5), so imine formation is faster. This is a qualitative comparison: bread thickness and moisture vary, so repeat with a second set if the result is close. It does not measure anything chemical directly.

### Part B — Python: protonation and mutarotation (30 min)

Open `lesson06_amines_sugars.py` and write the three TODO functions: `percent_protonated(pkah, ph)`, `fit_mutarotation(t, a)` with `scipy.optimize.curve_fit` and the model $\alpha(t) = \alpha_\infty + (\alpha_0 - \alpha_\infty)e^{-kt}$ (a first-order approach to equilibrium, lesson [03.3](../module-03/lesson-03.md)), and `beta_fraction(a_eq)`.

```bash
py lesson06_amines_sugars.py
```

The polarimeter data in `mutarotation_example.csv` are generated from a model with noise (see `make_data.py`), not measured.

How you know it worked: imidazole is 26 % protonated, ethylamine 99.96 %, aniline 0.17 %, pyridine 0.7 %. RDKit finds 5 stereocentres in each glucopyranose and 4 in open-chain glucose; the two anomers differ only at the anomeric carbon. The fit gives $\alpha_\infty$ = 52.6, $k$ = 0.012 min⁻¹ (half-life about 58 min) and 64 % β.

<details><summary>Reference solution for Part B</summary>

`percent_protonated`: `return 100 / (1 + 10 ** (ph - pkah))`. `fit_mutarotation`: `popt, _ = curve_fit(model, t, a, p0=[a[-1], a[0], 0.01])`, `return tuple(popt)`. `beta_fraction`: `return (ALPHA_PURE - a_eq) / (ALPHA_PURE - BETA_PURE)`. Full code in `lesson06_amines_sugars_solution.py`.

The fitted $k$ is the sum of the forward and reverse rate constants of α ⇌ β, as for any reversible first-order reaction; it is not the rate of α → β alone.

</details>

### Part C — product drill (20 min)

Type each product's SMILES into `ANSWERS` in `lesson06_amines_sugars.py`:

a. Cyclohexanone with ammonia, then NaBH₃CN.
b. Benzaldehyde with dimethylamine, then NaBH₃CN.
c. Aniline with acetic anhydride.
d. Nitrobenzene with iron and HCl, then NaOH.
e. D-glucose with methanol and an HCl catalyst (stereochemistry is ignored by the checker).

<details><summary>Worked answers to Part C</summary>

a. Cyclohexylamine, `NC1CCCCC1`. Imine, then reduction: a primary amine with no over-alkylation.
b. N,N-dimethylbenzylamine, `CN(C)Cc1ccccc1`. A secondary amine gives an iminium ion, reduced to a tertiary amine.
c. Acetanilide, `CC(=O)Nc1ccccc1`. Acylation (lesson 16.3); the amide N is no longer basic.
d. Aniline, `Nc1ccccc1`. Six electrons per nitro group; NaOH frees the amine from its hydrochloride.
e. Methyl D-glucopyranoside, `COC1OC(CO)C(O)C(O)C1O`, a mixture of α and β. Only the anomeric OH is replaced: it is the hemiacetal OH, the one that can leave as water through an oxocarbenium ion. The other OH groups are ordinary alcohols.

</details>

## Common mistakes

- **Calling amides bases.** The N lone pair is tied up in resonance with C=O; amides are neutral at every pH you will meet.
- **Making a primary amine by SN2 of ammonia on an alkyl halide.** It over-alkylates. Use reductive amination or reduce a nitrile, amide or nitro group.
- **Counting pyrrole's lone pair as available.** It is part of the aromatic sextet; protonating it destroys aromaticity. Pyrrole is not a useful base.
- **Thinking α and β glucose are enantiomers.** They differ at one stereocentre out of five: they are diastereomers (lesson 15.3), with different rotations and properties.
- **Expecting glycosides or sucrose to mutarotate or reduce Benedict's reagent.** No free hemiacetal, no ring opening.

## Key takeaways

- Basicity is measured by $\mathrm{p}K_{aH}$: alkylamines about 10–11, ammonia 9.3, imidazole 7.0, pyridine 5.3, aniline 4.6, amides and pyrrole not basic.
- At pH 7.4 alkylamines are over 99 % protonated, imidazole about a quarter, anilines and pyridines almost neutral.
- Make amines by reductive amination or by reducing nitro groups, nitriles and amides.
- Glucose is a cyclic hemiacetal; the anomers α and β interconvert through the open chain (mutarotation) to 37 : 63.
- Pyridine's lone pair is basic and outside the π system; pyrrole's and furan's are inside it, which makes these rings electron-rich.

## Sources

- [OpenStax Organic Chemistry, 24.3 Basicity of Amines](https://openstax.org/books/organic-chemistry/pages/24-3-basicity-of-amines) — the $\mathrm{p}K_{aH}$ table used here.
- [OpenStax Organic Chemistry, 24.6 Synthesis of Amines](https://openstax.org/books/organic-chemistry/pages/24-6-synthesis-of-amines) — reductive amination, reductions, why alkylation over-reacts.
- [OpenStax Organic Chemistry, 24.9 Heterocyclic Amines](https://openstax.org/books/organic-chemistry/pages/24-9-heterocyclic-amines) and [15.5 Aromatic Heterocycles](https://openstax.org/books/organic-chemistry/pages/15-5-aromatic-heterocycles-pyridine-and-pyrrole) — pyridine, pyrrole, imidazole, purines and pyrimidines.
- [OpenStax Organic Chemistry, 25.5 Anomers](https://openstax.org/books/organic-chemistry/pages/25-5-cyclic-structures-of-monosaccharides-anomers) — pyranose rings, rotations, mutarotation, 37 : 63.
- [OpenStax Organic Chemistry, 25.6 Reactions of Monosaccharides](https://openstax.org/books/organic-chemistry/pages/25-6-reactions-of-monosaccharides) — glycosides and reducing sugars.
- PubChem: [α-D-glucopyranose](https://pubchem.ncbi.nlm.nih.gov/compound/79025) and [β-D-glucopyranose](https://pubchem.ncbi.nlm.nih.gov/compound/64689) — isomeric SMILES used in the lab.
