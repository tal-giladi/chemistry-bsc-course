---
id: "24.4"
module: 24
minutes: 20
practice_minutes: 100
prerequisites: ["24.1", "24.2", "24.3", "16.3", "17.2"]
objectives:
  - Explain the mechanism of the acid-catalysed acetylation of salicylic acid and the reason for every step of the aspirin procedure.
  - Calculate the limiting reagent, theoretical yield, percent yield and atom economy of the synthesis.
  - Judge the purity of a run from its yield, melting range and iron(III) chloride test, and decide what to do next.
  - Confirm the product from real spectra by finding the bands and signals that distinguish aspirin from salicylic acid.
volatility: concept
sources:
  - title: "OpenStax Organic Chemistry (2023), 21.2 Nucleophilic Acyl Substitution Reactions"
    url: https://openstax.org/books/organic-chemistry/pages/21-2-nucleophilic-acyl-substitution-reactions
  - title: "PubChem, Aspirin (CID 2244): melting point, pKa, GHS"
    url: https://pubchem.ncbi.nlm.nih.gov/compound/2244
  - title: "PubChem, Salicylic acid (CID 338): melting point, GHS"
    url: https://pubchem.ncbi.nlm.nih.gov/compound/338
  - title: "PubChem, Acetic anhydride (CID 7918): density, GHS"
    url: https://pubchem.ncbi.nlm.nih.gov/compound/7918
  - title: "NIST Chemistry WebBook, Aspirin: IR spectrum"
    url: https://webbook.nist.gov/cgi/cbook.cgi?ID=C50782&Mask=80
  - title: "NIST Chemistry WebBook, Salicylic acid: IR spectrum"
    url: https://webbook.nist.gov/cgi/cbook.cgi?ID=C69727&Mask=80
  - title: "SDBS Spectral Database for Organic Compounds (AIST)"
    url: https://sdbs.db.aist.go.jp/
last_verified: "2026-10-17"
---

# 24.4 · Virtual synthesis: aspirin

Aspirin, acetylsalicylic acid, is made in teaching labs all over the world because one short reaction uses every technique of this module: heating, quenching, crystallisation, vacuum filtration, recrystallisation, a colour test, a melting point and spectra. You met the chemistry on paper in [16.3](../module-16/lesson-03.md), where acetic anhydride turned out to be the right acetylating agent. Here you run it on the virtual bench, make the decisions a student makes at the real bench, and learn to tell from the evidence whether the white powder is aspirin, wet aspirin, or aspirin full of salicylic acid.

## Why it matters

Unreacted salicylic acid is the classic impurity in this synthesis, and it matters outside the lab: it irritates the stomach more than aspirin, and its phenol group is what the iron(III) test sees. Pharmacopoeias set a limit on free salicylic acid in aspirin tablets for exactly this reason. A teaching run with 89 % crude yield sounds good until the melting range and the violet colour show that a fifth of it may be starting material. Learning to read those signs, and to decide between "dry it", "recrystallise it" and "repeat it", is the real skill.

## Core ideas

> [!NOTE]
> The chemistry and the procedure are stable; this is a classic teaching synthesis. Physical data and hazards are from PubChem and spectra from the NIST WebBook and SDBS, checked 2026-10-17. Procedures differ between labs in scale, catalyst (phosphoric or sulfuric acid) and recrystallisation solvent.

> [!IMPORTANT]
> This synthesis cannot be done at home. Acetic anhydride is flammable and corrosive (GHS H226, H314) and its vapour attacks eyes and lungs; the acid catalysts cause severe burns; salicylic acid can cause serious eye damage (H318). The real experiment needs a fume hood, goggles, gloves and supervised waste disposal. Do it here, on the virtual bench.

### The reaction and its mechanism

$$\text{salicylic acid} + (\mathrm{CH_3CO})_2\mathrm{O} \xrightarrow{\ \mathrm{H^+},\ 75\,^\circ\mathrm{C}\ } \text{aspirin} + \mathrm{CH_3COOH}$$

It is a nucleophilic acyl substitution ([16.3](../module-16/lesson-03.md)):

1. The acid catalyst protonates a C=O oxygen of the anhydride, making that carbon more electrophilic.
2. The phenol oxygen of salicylic acid adds to it, giving a tetrahedral intermediate.
3. The intermediate collapses and expels acetic acid, a good leaving group; loss of a proton gives the ester.

Why the phenol and not the carboxylic acid? The carboxylic acid is the poorer nucleophile, and if it does react, the mixed anhydride it forms is hydrolysed back during the water quench. The phenol O–H becomes the acetyl ester, and the carboxylic acid stays.

### Every step and its reason

| Step | Reason | What goes wrong |
|---|---|---|
| Weigh dry salicylic acid into a dry flask; add excess acetic anhydride (about 3–4 equivalents) and a few drops of 85 % phosphoric acid | Excess anhydride is cheap, acts as solvent and pushes the reaction to completion; acid catalyses it | Wet glassware or old anhydride: water destroys anhydride, low yield |
| Heat in a water bath at 70–80 °C for 10–15 min, swirling | Fast at this temperature; well below the anhydride's boiling point (139 °C), so no reflux is needed | Too hot or too long: coloured by-products and polymeric esters |
| Remove from heat, add a little cold water dropwise, then more cold water | Destroys the excess anhydride (exothermic, gives acetic acid vapour) and makes aspirin insoluble | Water added fast and hot: spattering; added before the reaction is done: unreacted salicylic acid |
| Cool in ice; scratch if needed; vacuum-filter; wash with ice water | Aspirin is only slightly soluble in cold water; washing removes acetic and phosphoric acid | Filtering warm: product lost in the filtrate |
| Recrystallise (ethanol and warm water, or water alone) and dry | Salicylic acid stays in the mother liquor | Boiling in water too long hydrolyses aspirin back to salicylic acid |
| Check: yield, melting point, FeCl₃ test, TLC, IR | Each catches a different failure | Weighing before drying: yield over 100 % |

### Three tests, three questions

- **Iron(III) chloride test: is the phenol gone?** Phenols form a violet complex with Fe³⁺. Salicylic acid gives a deep violet; pure aspirin, whose phenol oxygen is now an ester, stays yellow (the colour of the reagent). A faint violet means a little salicylic acid. It is very sensitive, so a crude product almost always tests positive.
- **Melting point: is it pure and dry?** Aspirin 135 °C (PubChem, rapid heating; it decomposes near its melting point), salicylic acid 159 °C. A mixture melts low and broad ([24.3](lesson-03.md)).
- **IR: did the right bond form?** Aspirin shows two C=O bands, the ester near 1750 cm⁻¹ and the hydrogen-bonded acid near 1690, and no phenol O–H. Salicylic acid shows one acid C=O near 1660 (lowered by an internal hydrogen bond to the phenol) and broad O–H absorption ([17.2](../module-17/lesson-02.md)). In ¹H NMR, the new acetyl group appears as a three-proton singlet near 2.3 ppm ([17.3](../module-17/lesson-03.md)).

### Yield and atom economy

The **theoretical yield** comes from the limiting reagent. The **percent yield** is what you got divided by that. The **atom economy** asks how much of the reactants' mass ends up in the product even at 100 % yield:

$$\text{atom economy} = \frac{M_\text{product}}{\sum M_\text{reactants}} \times 100\,\%$$

Here the acetic acid by-product carries away a quarter of the mass. Atom economy is one of the measures of "green" chemistry; acetic acid can at least be recovered and reused.

## Worked example

### Amounts, yield and verdicts

You start with 2.00 g of salicylic acid ($M$ = 138.12 g/mol) and 5.0 mL of acetic anhydride (1.082 g/mL, $M$ = 102.09 g/mol).

1. Salicylic acid: $2.00/138.12 = 14.48$ mmol. Anhydride: $5.0 \times 1.082 / 102.09 = 53.0$ mmol, 3.7 equivalents. The reaction is 1:1, so **salicylic acid is limiting**.
2. Theoretical yield: $14.48 \text{ mmol} \times 180.16 \text{ g/mol} = 2.61$ g of aspirin.
3. Atom economy: $180.16/(138.12 + 102.09) = 75.0\,\%$.

Three runs on the virtual bench:

| Run | Mass | mp | FeCl₃ | Yield | Verdict |
|---|---|---|---|---|---|
| A, crude | 2.31 g | 128–133 °C | violet | 88.6 % | Impure: broad and low mp, phenol present. Recrystallise. |
| A, recrystallised and dry | 1.92 g | 134–136 °C | yellow | 73.6 % | Pure enough: sharp, close to 135 °C, no phenol. |
| B, filtered but not dried | 2.95 g | 118–131 °C | violet | 113 % | Over 100 %: wet. Dry to constant mass, then judge again. |

Interpretation: the honest yield is the one of a pure, dry product, 73.6 % for run A. The 15 % lost in recrystallisation bought the purity; most of the loss is aspirin left dissolved in the mother liquor ([24.2](lesson-02.md)). A yield over 100 % is never good news.

## Hands-on

What you need: the simulation, the [Module 24 lab folder](../../labs/module-24/), a web browser for the NIST WebBook and SDBS, and the [spectrum assignment template](../../templates/spectrum-assignment.md). Write up Part A on the [lab report template](../../templates/lab-report.md). Time: about 100 minutes.

### Part A — virtual bench: make aspirin (45 min)

[Simulation: Organic bench — aspirin synthesis](../../simulations/organic-bench/index.html?preset=aspirin)

1. Plan: from the sim's reagent cards, write the amounts and the hazard of each reagent in your notebook (GHS pictograms and H-statements), as in [01.4](../module-01/lesson-04.md).
2. Run the synthesis once following the procedure table. Record crude mass, melting range and the FeCl₃ result, then recrystallise, dry and record again.
3. Make two deliberate mistakes in separate runs: use "wet" salicylic acid and skip the drying step. Record what the sim shows and why.
4. Run a TLC of crude product, recrystallised product and salicylic acid, with a co-spot.

How you know it worked: a careful run gives 2.2–2.4 g crude and, after recrystallisation, 1.8–2.1 g (70–80 %) melting within 2 °C of 135 °C with a negative FeCl₃ test, and the recrystallised lane shows no salicylic-acid spot. The wet run gives a low yield; the undried run gives more than 2.61 g.

### Part B — Python: amounts and verdicts (15 min)

Complete `moles()`, `limiting()`, `atom_economy()` and `verdict()` in `lesson04_aspirin.py`, then replace the example runs in `RUNS` with your own from Part A and run it:

```bash
py lesson04_aspirin.py
```

How you know it worked: with the example runs the script prints 14.48 mmol, 53.0 mmol (3.7 equivalents), 2.61 g, 75.0 % and the three verdicts of the worked example.

<details><summary>Reference solution</summary>

```python
def limiting(n_salicylic, n_anhydride):
    if n_salicylic <= n_anhydride:
        return "salicylic acid", n_salicylic
    return "acetic anhydride", n_anhydride

def atom_economy(product, reactants):
    return 100 * molar_mass(product) / sum(molar_mass(r) for r in reactants)
```

`verdict()` flags a yield over 100 %, a range wider than 2 °C or ending more than 2 °C below 135 °C, and a violet FeCl₃ test. Full code: `lesson04_aspirin_solution.py`.

</details>

### Part C — real spectra: aspirin or salicylic acid? (40 min)

1. Open the IR spectra of [aspirin](https://webbook.nist.gov/cgi/cbook.cgi?ID=C50782&Mask=80) and [salicylic acid](https://webbook.nist.gov/cgi/cbook.cgi?ID=C69727&Mask=80) in the NIST WebBook. Read the state line first (these are solid-state spectra, not gas).
2. Mark the C=O bands of each and the O–H region. Which band appears only in aspirin?
3. Open [SDBS](https://sdbs.db.aist.go.jp/), accept the disclaimer, and search by compound name for "acetylsalicylic acid" and "salicylic acid". Open the ¹H NMR spectrum of each.
4. Fill in the spectrum assignment template for aspirin: every signal, its integral and the protons it belongs to.

How you know it worked: aspirin shows two strong C=O bands, roughly 1750 (ester) and 1690 cm⁻¹ (acid), and no sharp phenol O–H; salicylic acid has one C=O band near 1660 cm⁻¹. In the NMR, aspirin has a 3H singlet near 2.3 ppm (the acetyl CH₃), four aromatic protons between about 7.1 and 8.2 ppm, and a broad acid proton far downfield; salicylic acid has no signal near 2.3 ppm. If your product spectrum (the sim shows one) has a 2.3 ppm singlet integrating to less than 3H against four aromatic protons, salicylic acid is still present.

## Common mistakes

- **Taking the anhydride as limiting because it is listed first.** Convert both to moles; here salicylic acid is limiting.
- **Weighing the product wet.** It inflates the yield and lowers the melting point. Dry to constant mass.
- **Adding the quench water quickly to a hot mixture.** The excess anhydride reacts violently with water; add it slowly to the cooled mixture.
- **Recrystallising by long boiling in water.** Aspirin hydrolyses back to salicylic acid; dissolve quickly and cool.
- **Reading a negative FeCl₃ test as proof of identity.** It only says the phenol is gone; confirm with the melting point and spectra.
- **Comparing a gas-phase IR spectrum with a solid one.** Hydrogen bonding shifts O–H and C=O bands; check the state.

## Key takeaways

- Aspirin forms by acid-catalysed nucleophilic acyl substitution of acetic anhydride by the phenol O–H of salicylic acid; acetic acid is the by-product.
- Salicylic acid is limiting; 2.00 g gives at most 2.61 g of aspirin, and the atom economy is 75 %.
- Every step has a reason: excess anhydride and acid catalyst for rate, water quench to destroy anhydride, cold filtration to keep the product, recrystallisation to remove salicylic acid, drying to get an honest yield.
- FeCl₃ (phenol), melting point (purity, dryness) and IR or NMR (the new ester C=O and acetyl CH₃) answer different questions; use all three.

## Sources

- [OpenStax Organic Chemistry (2023), 21.2 Nucleophilic Acyl Substitution Reactions](https://openstax.org/books/organic-chemistry/pages/21-2-nucleophilic-acyl-substitution-reactions) — the addition–elimination mechanism.
- [PubChem, Aspirin (CID 2244)](https://pubchem.ncbi.nlm.nih.gov/compound/2244) — mp 135 °C (rapid heating), pKa 3.5, GHS.
- [PubChem, Salicylic acid (CID 338)](https://pubchem.ncbi.nlm.nih.gov/compound/338) — mp 159 °C; H302, H318, H361.
- [PubChem, Acetic anhydride (CID 7918)](https://pubchem.ncbi.nlm.nih.gov/compound/7918) — density 1.082 g/mL at 20 °C; H226, H302, H314.
- [NIST WebBook, Aspirin IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C50782&Mask=80) and [Salicylic acid IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C69727&Mask=80) — Coblentz Society condensed-phase spectra.
- [SDBS (AIST)](https://sdbs.db.aist.go.jp/) — ¹H NMR of acetylsalicylic acid and salicylic acid, searched by name.
