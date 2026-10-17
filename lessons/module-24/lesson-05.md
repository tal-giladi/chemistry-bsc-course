---
id: "24.5"
module: 24
minutes: 24
practice_minutes: 110
prerequisites: ["24.4", "15.5", "16.2", "16.4"]
objectives:
  - Explain the mechanism, the key conditions and the main side reactions of three teaching syntheses: 1-bromobutane (SN2), triphenylmethanol (Grignard) and dibenzalacetone (aldol).
  - Plan each work-up from the properties of the product and the impurities, including which layer the product is in.
  - Calculate amounts, theoretical yields and the water budget of a Grignard reaction.
  - Diagnose a failed run on the virtual bench from its yield, melting or boiling point and IR spectrum.
volatility: concept
sources:
  - title: "OpenStax Organic Chemistry (2023), 11.2 The SN2 Reaction"
    url: https://openstax.org/books/organic-chemistry/pages/11-2-the-sn2-reaction
  - title: "OpenStax Organic Chemistry (2023), 19.7 Nucleophilic Addition of Hydride and Grignard Reagents"
    url: https://openstax.org/books/organic-chemistry/pages/19-7-nucleophilic-addition-of-hydride-and-grignard-reagents-alcohol-formation
  - title: "OpenStax Organic Chemistry (2023), 23.5 Mixed Aldol Reactions"
    url: https://openstax.org/books/organic-chemistry/pages/23-5-mixed-aldol-reactions
  - title: "PubChem, 1-Bromobutane (CID 8002): density, GHS"
    url: https://pubchem.ncbi.nlm.nih.gov/compound/8002
  - title: "PubChem, Bromobenzene (CID 7961): density, GHS"
    url: https://pubchem.ncbi.nlm.nih.gov/compound/7961
  - title: "NIST Chemistry WebBook, Triphenylmethanol: phase change and IR"
    url: https://webbook.nist.gov/cgi/cbook.cgi?ID=C76846&Mask=80
  - title: "NIST Chemistry WebBook, 1,5-Diphenyl-1,4-pentadien-3-one (dibenzalacetone): IR"
    url: https://webbook.nist.gov/cgi/cbook.cgi?ID=C538589&Mask=80
last_verified: "2026-10-17"
---

# 24.5 · Virtual synthesis: substitution, Grignard and aldol

Three more classic teaching syntheses, each built on a reaction you have already drawn on paper: an SN2 substitution ([15.5](../module-15/lesson-05.md)), a Grignard addition ([16.2](../module-16/lesson-02.md)) and a crossed aldol condensation ([16.4](../module-16/lesson-04.md)). Each one teaches a different lesson about the bench. The substitution teaches work-up by washing and the danger of assuming which layer is which. The Grignard teaches that a few drops of water can ruin a reaction. The aldol teaches that stoichiometry decides which product you get. You run all three on the virtual bench and learn to read what went wrong.

## Why it matters

On paper, $\mathrm{RMgBr + R_2C{=}O \to R_3COH}$ always works. At the bench, the same student's first Grignard often never starts, or starts and gives a yellow oil smelling of biphenyl instead of white crystals. The difference is technique and understanding: dry glassware, how to start the reaction, how fast to add the halide, and how to remove the side product. Each of these syntheses has one or two such decisions that make or break it, and the virtual bench lets you make the wrong decision safely and see why it is wrong.

## Core ideas

> [!NOTE]
> The reactions and procedures are classic and stable. Physical data and hazards are from PubChem and the NIST WebBook, checked 2026-10-17. Amounts are typical teaching-lab scale; real lab manuals differ in detail.

> [!IMPORTANT]
> None of these can be done at home. They use concentrated sulfuric acid (H314), extremely flammable diethyl ether (H224), bromobenzene (toxic if inhaled, H331), 1-bromobutane (highly flammable, H225) and sodium hydroxide, and they need a fume hood. The virtual bench teaches the procedure and reasoning; it does not train the hands.

### 1. SN2: 1-bromobutane from 1-butanol

$$\mathrm{CH_3CH_2CH_2CH_2OH + NaBr + H_2SO_4 \xrightarrow{\text{reflux}} CH_3CH_2CH_2CH_2Br + NaHSO_4 + H_2O}$$

**Mechanism.** OH⁻ is a poor leaving group, so sulfuric acid protonates the alcohol; water is a good leaving group. Bromide (from NaBr, which with H₂SO₄ gives HBr in the flask) attacks the primary carbon from the back side and water leaves in one step: SN2 ([15.5](../module-15/lesson-05.md)). A primary carbon does not form a stable carbocation, so SN1 is negligible.

**Side reactions.** Elimination gives 1-butene (gas); a second butanol molecule can attack instead of bromide and give dibutyl ether. Both increase if the mixture is overheated.

**Work-up, step by reason.**

1. Distil the crude product out of the reaction flask (simple distillation; 1-bromobutane co-distils with water).
2. Wash with water. 1-Bromobutane (1.27 g/mL) is now the **lower** layer.
3. Wash with cold **concentrated** sulfuric acid. It dissolves leftover butanol and dibutyl ether (they are protonated and become ionic). Now the 1-bromobutane (1.27 g/mL) floats on the acid (1.84 g/mL) and is the **upper** layer. The layer switched: this is the step where students lose their product.
4. Wash with aqueous NaHCO₃ to remove acid (vent!), dry over anhydrous calcium chloride, and distil, collecting the fraction near 100–103 °C (bp 101.6 °C).

**Check.** IR: the broad O–H band of butanol near 3300 cm⁻¹ is gone. ¹H NMR: a two-proton triplet near 3.4 ppm (CH₂Br), compared with 3.6 ppm for CH₂OH in butanol.

### 2. Grignard: triphenylmethanol from bromobenzene and benzophenone

$$\mathrm{PhBr + Mg \xrightarrow{\text{dry ether}} PhMgBr}; \qquad \mathrm{PhMgBr + Ph_2C{=}O \to Ph_3COMgBr \xrightarrow{\mathrm{H_3O^+}} Ph_3COH}$$

**Mechanism.** The phenyl carbon of the Grignard reagent behaves as a carbanion and adds to the carbonyl carbon of benzophenone; acid work-up protonates the alkoxide ([16.2](../module-16/lesson-02.md)).

**Water is the enemy.** The reagent is a very strong base, so any water protonates it to benzene at once. All glassware is oven-dried, the ether is anhydrous, and a drying tube protects the condenser. At teaching scale (about 20 mmol), 37 mg of water, less than one drop, destroys 10 % of the reagent.

**Starting the reaction.** Magnesium is coated with oxide. A small iodine crystal, crushing a turning with a dry glass rod, or gentle warming starts it. Signs: cloudiness, the iodine colour fading, and the ether beginning to boil by itself. Then add the rest of the bromobenzene slowly, so the exotherm keeps a gentle reflux.

**Side product.** Biphenyl (Ph–Ph) forms when the Grignard reagent couples with unreacted bromobenzene, favoured by adding the halide too fast and by overheating. It is removed by stirring the crude solid with cold hexane or petroleum ether, in which biphenyl dissolves and triphenylmethanol does not; then recrystallise.

**Check.** Triphenylmethanol melts at about 160–162 °C (NIST); biphenyl at 69 °C. IR: an O–H band near 3470 cm⁻¹ appears and benzophenone's C=O near 1660 cm⁻¹ is gone.

### 3. Aldol: dibenzalacetone from benzaldehyde and acetone

$$\mathrm{2\,PhCHO + CH_3COCH_3 \xrightarrow{\text{NaOH, EtOH/H}_2\text{O}} PhCH{=}CHCOCH{=}CHPh + 2\,H_2O}$$

**Mechanism.** Hydroxide removes an α-hydrogen of acetone to form an enolate; the enolate adds to benzaldehyde; the β-hydroxy ketone loses water to give a C=C conjugated with the ring and the carbonyl. Then the other side of acetone does the same. This crossed aldol (Claisen–Schmidt) works cleanly because benzaldehyde has **no α-hydrogens** and cannot form an enolate itself ([16.4](../module-16/lesson-04.md)).

**Stoichiometry decides the product.** Two benzaldehydes per acetone gives dibenzalacetone, which precipitates as a yellow solid and so drives the equilibrium. With excess acetone you get mainly the single product, benzalacetone. With too much benzaldehyde, the excess stays as an oily, almond-smelling contaminant.

**Check.** The trans,trans isomer melts at 110–111 °C. IR: a conjugated C=O near 1650 cm⁻¹, lower than acetone's 1715, because conjugation weakens the C=O bond. ¹H NMR: the alkene protons are doublets with a coupling constant near 16 Hz, which shows the trans geometry ([17.3](../module-17/lesson-03.md)).

## Worked example

### Amounts for the three runs

Densities at 20 °C from PubChem; molar masses from the formulas.

| Synthesis | Reagents | Limiting | Theoretical yield |
|---|---|---|---|
| SN2 | 10.0 mL 1-butanol (0.810 g/mL, 74.12 g/mol) = 109 mmol; 13.0 g NaBr = 126 mmol | 1-butanol | 109 mmol × 137.02 g/mol = 14.97 g (11.8 mL) |
| Grignard | 2.2 mL bromobenzene (1.495 g/mL) = 21.0 mmol; 0.50 g Mg = 20.6 mmol; 3.64 g benzophenone = 20.0 mmol | benzophenone | 20.0 mmol × 260.34 g/mol = 5.20 g |
| Aldol | 2.0 mL benzaldehyde (1.046 g/mL) = 19.7 mmol; 0.73 mL acetone (0.785 g/mL) = 9.9 mmol; needs 2:1 | both (exactly 2:1) | 9.9 mmol × 234.29 g/mol = 2.31 g |

Interpretation:

- **SN2:** 10.5 g of distilled 1-bromobutane is a 70 % yield, typical. NaBr is in excess so that bromide wins the competition with butanol as nucleophile.
- **Grignard:** the reagent (limited by Mg, 20.6 mmol) is only 3 % in excess over the ketone. If 37 mg of water gets in, 10 % of the reagent is lost and the Grignard becomes limiting at 18.5 mmol; the maximum yield falls to 4.8 g, and unreacted benzophenone contaminates the product. Dryness is not a detail.
- **Aldol:** exactly 2:1. A small excess of benzaldehyde is easier to wash out (with cold ethanol) than a mixture of mono- and di-condensation products.

## Hands-on

What you need: the simulation, the [Module 24 lab folder](../../labs/module-24/), a web browser. Record each run on a [notebook page](../../templates/notebook-page.md). Time: about 110 minutes.

### Part A — virtual bench: three syntheses, one mistake each (70 min)

[Simulation: Organic bench — SN2: 1-bromobutane from 1-butanol](../../simulations/organic-bench/index.html?preset=sn2)

1. Run the synthesis as described. At the sulfuric acid wash, the sim asks which layer to keep: answer from densities, not position on the screen.
2. Run it again but overheat the reflux. Record the yield and what the sim's gas readout and IR show.

[Simulation: Organic bench — Grignard: triphenylmethanol](../../simulations/organic-bench/index.html?preset=grignard)

3. Run with oven-dried glassware. Start the reaction (try first without iodine), then add the bromobenzene slowly.
4. Run again with "air-dried" glassware and fast addition. Compare yields, melting points and the amount of biphenyl removed by the hexane wash.

[Simulation: Organic bench — aldol: dibenzalacetone](../../simulations/organic-bench/index.html?preset=aldol)

5. Run with the 2:1 ratio, then with 1:1 and with 3:1. Record the product mass, colour and melting point each time.

How you know it worked: SN2 gives 60–75 % of a liquid boiling near 101 °C with no O–H band; overheating lowers the yield and the sim reports butene and dibutyl ether. The dry Grignard gives 60–80 % of white crystals melting near 160 °C; the wet, fast run gives under 40 %, a lower melting point and more biphenyl. The 2:1 aldol gives a yellow solid melting near 110 °C; 1:1 gives mainly benzalacetone (a low-melting solid), and 3:1 gives an oily, almond-smelling product.

### Part B — Python: amounts and the water budget (15 min)

Complete `mmol_from_mL()`, `mmol_from_g()`, `theoretical_g()` and `water_that_destroys()` in `lesson05_reactions.py` and run it:

```bash
py lesson05_reactions.py
```

How you know it worked: it prints the three theoretical yields of the worked example (14.97 g, 5.20 g, 2.31 g), 70 % for the SN2 run, and 19, 37 and 185 mg of water to destroy 5, 10 and 50 % of the Grignard reagent.

<details><summary>Reference solution</summary>

```python
def mmol_from_mL(volume_mL, name):
    return 1000 * volume_mL * DENSITY[name] / molar_mass(name)

def theoretical_g(reagents, product):
    n_product = min(n / per for n, per in reagents)
    return n_product * molar_mass(product) / 1000

def water_that_destroys(mmol_grignard, fraction):
    return fraction * mmol_grignard * molar_mass("water")
```

Full code: `lesson05_reactions_solution.py`.

</details>

### Part C — real spectra: did the functional group change? (25 min)

For each pair, open both IR spectra in the NIST WebBook and write one sentence naming the band that appears or disappears:

1. [1-butanol](https://webbook.nist.gov/cgi/cbook.cgi?ID=C71363&Mask=80) → [1-bromobutane](https://webbook.nist.gov/cgi/cbook.cgi?ID=C109659&Mask=80)
2. [benzophenone](https://webbook.nist.gov/cgi/cbook.cgi?ID=C119619&Mask=80) → [triphenylmethanol](https://webbook.nist.gov/cgi/cbook.cgi?ID=C76846&Mask=80)
3. acetone → [dibenzalacetone](https://webbook.nist.gov/cgi/cbook.cgi?ID=C538589&Mask=80) (compare the C=O position)

Then open [SDBS](https://sdbs.db.aist.go.jp/), search by name for "1-bromobutane" and "dibenzylideneacetone", and find the CH₂Br triplet and the 16 Hz alkene doublets in the ¹H NMR spectra.

How you know it worked: (1) the broad O–H near 3300 cm⁻¹ disappears; (2) the C=O near 1660 cm⁻¹ disappears and an O–H near 3470 cm⁻¹ appears; (3) the C=O moves from about 1715 to about 1650 cm⁻¹. Check each spectrum's state line: gas-phase and condensed-phase band positions differ ([17.2](../module-17/lesson-02.md)).

## Common mistakes

- **Keeping the wrong layer after the sulfuric acid wash.** 1-Bromobutane is below water but above concentrated sulfuric acid.
- **Using wet glassware or ordinary ether for a Grignard.** Less than a drop of water destroys a tenth of the reagent; oven-dry everything.
- **Adding all the bromobenzene at once.** The reaction can run away, boil the ether out of the condenser, and make more biphenyl.
- **Forgetting the acid work-up.** The Grignard product is a magnesium alkoxide until acid protonates it.
- **Using the wrong ratio in the aldol.** 2:1 benzaldehyde to acetone for dibenzalacetone; excess acetone gives the mono product.
- **Heating the aldol to speed it up.** Above about 30 °C side reactions increase; the precipitation at room temperature drives it.

## Key takeaways

- 1-Bromobutane: SN2 on a protonated primary alcohol; washes with water, cold conc. H₂SO₄ and bicarbonate remove water-soluble impurities, butanol and ether, and acid; the product layer switches from bottom to top.
- Triphenylmethanol: a Grignard needs strictly dry conditions; slow addition limits biphenyl, which a hexane wash removes.
- Dibenzalacetone: a crossed aldol works because benzaldehyde has no α-H; the 2:1 ratio and precipitation give the double condensation product.
- For each product, one IR change proves the reaction: O–H lost, C=O lost and O–H gained, or C=O shifted by conjugation.

## Sources

- [OpenStax Organic Chemistry (2023), 11.2 The SN2 Reaction](https://openstax.org/books/organic-chemistry/pages/11-2-the-sn2-reaction) — backside attack, primary substrates.
- [OpenStax Organic Chemistry (2023), 19.7 Grignard Reagents](https://openstax.org/books/organic-chemistry/pages/19-7-nucleophilic-addition-of-hydride-and-grignard-reagents-alcohol-formation) — addition to ketones, need for dry conditions.
- [OpenStax Organic Chemistry (2023), 23.5 Mixed Aldol Reactions](https://openstax.org/books/organic-chemistry/pages/23-5-mixed-aldol-reactions) — why a partner without α-hydrogens gives one product.
- [PubChem, 1-Bromobutane (CID 8002)](https://pubchem.ncbi.nlm.nih.gov/compound/8002) — density 1.27 g/mL, bp 101.6 °C, H225. [Bromobenzene (CID 7961)](https://pubchem.ncbi.nlm.nih.gov/compound/7961) — density 1.495 g/mL, H331. Other densities from PubChem CIDs 263 (1-butanol), 240 (benzaldehyde), 180 (acetone).
- [NIST WebBook, Triphenylmethanol](https://webbook.nist.gov/cgi/cbook.cgi?ID=C76846&Mask=80) — IR; melting point about 433–436 K on the phase-change page.
- [NIST WebBook, Dibenzalacetone](https://webbook.nist.gov/cgi/cbook.cgi?ID=C538589&Mask=80) — IR. Melting point 110–111 °C for the trans,trans isomer (teaching-lab literature value).
