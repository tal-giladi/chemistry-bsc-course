---
id: "15.7"
module: 15
minutes: 25
practice_minutes: 120
prerequisites: ["15.6", "15.5", "15.4"]
objectives:
  - Predict the product, regiochemistry and stereochemistry of HX addition, hydration, halogenation, hydroboration–oxidation and hydrogenation of alkenes.
  - Explain Markovnikov's rule from carbocation stability, and anti addition from the bromonium ion.
  - Use alkyne acidity and alkyne reductions to plan a short route to a cis or trans alkene.
  - Complete the module practical, a ten-reaction mechanism workbook checked with RDKit, and build the key products as 3D models.
volatility: concept
sources:
  - title: "OpenStax Organic Chemistry (McMurry, 2023), 7.6 Stability of Alkenes"
    url: https://openstax.org/books/organic-chemistry/pages/7-6-stability-of-alkenes
  - title: "OpenStax Organic Chemistry, 7.8 Orientation of Electrophilic Additions: Markovnikov's Rule"
    url: https://openstax.org/books/organic-chemistry/pages/7-8-orientation-of-electrophilic-additions-markovnikovs-rule
  - title: "OpenStax Organic Chemistry, 7.9 Carbocation Structure and Stability"
    url: https://openstax.org/books/organic-chemistry/pages/7-9-carbocation-structure-and-stability
  - title: "OpenStax Organic Chemistry, 8.2 Halogenation of Alkenes: Addition of X2"
    url: https://openstax.org/books/organic-chemistry/pages/8-2-halogenation-of-alkenes-addition-of-x2
  - title: "OpenStax Organic Chemistry, 8.5 Hydration of Alkenes: Addition of H2O by Hydroboration"
    url: https://openstax.org/books/organic-chemistry/pages/8-5-hydration-of-alkenes-addition-of-h2o-by-hydroboration
  - title: "OpenStax Organic Chemistry, 8.6 Reduction of Alkenes: Hydrogenation"
    url: https://openstax.org/books/organic-chemistry/pages/8-6-reduction-of-alkenes-hydrogenation
  - title: "OpenStax Organic Chemistry, 9.5 Reduction of Alkynes"
    url: https://openstax.org/books/organic-chemistry/pages/9-5-reduction-of-alkynes
  - title: "NIST Chemistry WebBook: butane, gas-phase thermochemistry"
    url: https://webbook.nist.gov/cgi/cbook.cgi?ID=C106978&Mask=1
last_verified: "2026-10-17"
---

# 15.7 · Alkenes and alkynes

Alkenes and alkynes are where organic synthesis starts: their π bonds are electron-rich, so electrophiles add to them, and a small set of additions turns one double bond into alcohols, halides or alkanes with the regiochemistry and stereochemistry you choose. This lesson collects those reactions, explains each with the ideas of lessons 15.1 to 15.6, and ends with the module practical: a ten-reaction mechanism workbook that you check with RDKit and model in 3D.

## Why it matters

Margarine was once made by hydrogenating vegetable oils, which turns some cis C=C bonds into trans ones as a side reaction. Trans fats raise heart-disease risk; Denmark capped industrial trans fats in 2003, and the World Health Organization now asks every country to eliminate them. One step of alkene chemistry, cis or trans, had a measurable effect on public health. In the lab the same choice appears every day: Lindlar hydrogenation gives a cis alkene, sodium in ammonia a trans one, and a chemist who picks the wrong one makes the wrong compound. The cis double bond in a pheromone or a vitamin decides whether it works.

## Core ideas

> [!NOTE]
> The reactions here are stable textbook chemistry. Enthalpies are NIST WebBook gas-phase values (Prosen, Maron and Rossini 1951), checked 2026-10-17. The practical checker relies on RDKit 2026.9.1 canonical SMILES; other RDKit versions may write them differently.

### Electrophilic addition: the π bond attacks

The π bond is a nucleophile (15.1, 15.4). A strong electrophile takes its electron pair, and the alkene carbons end up with two new σ bonds:

$$\mathrm{C{=}C + E\text{–}Nu \longrightarrow E\text{–}C\text{–}C\text{–}Nu}$$

For HBr: (1) arrow from the C=C π bond to H, arrow from the H–Br bond onto Br, giving a carbocation; (2) arrow from a Br⁻ lone pair to C⁺.

### Markovnikov's rule

With an unsymmetrical alkene, H adds to the carbon that already has more H's, and the nucleophile goes to the more substituted carbon. Propene + HBr gives 2-bromopropane, not 1-bromopropane. The reason is step 1: protonating the CH₂ end gives a secondary carbocation, protonating the middle gives a primary one. Carbocation stability is tertiary > secondary > primary (hyperconjugation, 15.5), and by the **Hammond postulate** the transition state of an endothermic step resembles its product, so the more stable cation also forms faster.

Because a carbocation is involved, rearrangements are possible (15.5): 3-methyl-1-butene + HCl gives a large share of 2-chloro-2-methylbutane after a hydride shift.

**Acid-catalysed hydration** works the same way with water as the nucleophile: H₃O⁺ protonates the alkene, water adds to C⁺, and a proton transfer gives a Markovnikov alcohol. It is the reverse of E1 dehydration (15.6): high water concentration and low temperature push it towards the alcohol, heat and removal of water push it towards the alkene.

### Halogenation: anti addition through a bromonium ion

Br₂ adds across C=C to give a 1,2-dibromide. No ordinary carbocation forms. The π bond attacks one Br, and a lone pair of that Br bonds back to the second carbon, giving a three-membered ring with Br⁺: a **bromonium ion**. Br⁻ then opens the ring from the back side, an SN2 on one ring carbon (15.5). The two Br's end up on opposite faces: **anti addition**. Cyclohexene gives only trans-1,2-dibromocyclohexane, as a racemic mixture of (R,R) and (S,S). Bromine's colour disappearing is the classic test for C=C.

### Hydroboration–oxidation: anti-Markovnikov and syn

Borane (BH₃, as a THF complex) adds H and B across the C=C in one step, from the same face (**syn addition**). Boron, the electrophile, goes to the less substituted and less crowded carbon. Oxidation with H₂O₂ and NaOH then replaces B with OH on the same carbon, keeping the geometry.

Net: H and OH added syn, with OH on the **less** substituted carbon (**anti-Markovnikov**). 1-Methylcyclohexene gives trans-2-methylcyclohexanol: the H and OH entered from the same face, so OH ends up trans to the methyl. Hydroboration and acid hydration together let you put OH on either carbon.

### Hydrogenation: syn, and a measure of stability

H₂ with a metal catalyst (Pd on carbon, Pt, Ni) adds two H atoms from the catalyst surface to one face of the alkene: **syn addition**. The heat released, the **enthalpy of hydrogenation**, measures alkene stability, because all three butenes give the same butane. From NIST ΔfH°(g) values (butane −127.1 kJ/mol):

| Alkene | ΔfH°(g) / kJ mol⁻¹ | ΔhydH° to butane / kJ mol⁻¹ |
|---|---|---|
| 1-butene | −0.6 | −126.5 |
| (Z)-2-butene | −7.7 | −119.4 |
| (E)-2-butene | −10.8 | −116.3 |

Less heat released means a more stable alkene, the same ranking as Zaitsev's rule in 15.6.

**Ozonolysis** (O₃, then a mild reducing agent such as zinc or dimethyl sulfide) cuts the C=C completely and gives two C=O compounds. It is used to locate a double bond; Module 16 uses the carbonyl products.

### Alkynes: acidity and reductions

An alkyne's carbons are sp (15.1). Two consequences:

- **Acidity.** A terminal C≡C–H has pKa 25, much more acidic than an alkene (44) or alkane (about 60) C–H, because the lone pair of the acetylide sits in an sp orbital, 50 % s (15.4). Sodium amide (NH₃, pKa 35) deprotonates it completely; hydroxide (water, 15.7) does not.
- **Acetylide alkylation.** The acetylide anion is a strong nucleophile. With a methyl or primary halide it does SN2 and makes a new C–C bond: HC≡CH → HC≡C⁻ → HC≡C–CH₂CH₃. With secondary or tertiary halides, the strongly basic acetylide eliminates instead (15.6).

Reductions control the geometry of the alkene you get:

| Reagent | Product | Stereochemistry | Why |
|---|---|---|---|
| H₂, Pd/C (excess) | alkane | — | both π bonds hydrogenated |
| H₂, Lindlar catalyst (Pd poisoned with lead and quinoline) | cis alkene | syn | surface addition, stops after one π bond |
| Na or Li in liquid NH₃ | trans alkene | anti | electron transfer, then protonation of a radical anion that prefers trans |

### Summary of additions

| Reaction | Regiochemistry | Stereochemistry | Intermediate |
|---|---|---|---|
| HX | Markovnikov | not controlled | carbocation |
| H₂O, H₃O⁺ | Markovnikov | not controlled | carbocation |
| X₂ | — | anti | halonium ion |
| BH₃, then H₂O₂/NaOH | anti-Markovnikov | syn | concerted, no cation |
| H₂, Pd | — | syn | metal surface |

## Worked example

### Plan a route to (Z)-hex-3-ene from ethyne

(Z)-Hex-3-ene, CH₃CH₂CH=CHCH₂CH₃ with the ethyl groups cis, is a model for the cis double bonds in natural fats and leaf odours.

1. **Build the carbon chain.** Six carbons from a two-carbon alkyne means adding two ethyl groups. Acetylide alkylation does it: ethyne + NaNH₂ → HC≡C⁻ Na⁺ (log K = 35 − 25 = 10, complete). Add CH₃CH₂Br: SN2 on a primary carbon gives but-1-yne. Repeat: NaNH₂, then CH₃CH₂Br, giving hex-3-yne, CH₃CH₂C≡CCH₂CH₃.
2. **Set the geometry.** H₂ with Lindlar catalyst adds two H's syn and stops at the alkene: (Z)-hex-3-ene. Sodium in liquid ammonia would give the (E) isomer instead.
3. **Check the traps.** Ethyl bromide is primary, so the acetylide substitutes rather than eliminates (with 2-bromopropane it would mostly do E2, 15.6). NaOH cannot replace NaNH₂, because water (15.7) is a stronger acid than ethyne (25). Excess H₂ on ordinary Pd would go all the way to hexane.

SMILES of the target: `CC/C=C\CC`. Every step uses one idea from this module: acidity (15.4), SN2 (15.5), substitution versus elimination (15.6), syn addition (15.7), E/Z (15.3).

## Hands-on

This is the module practical. It uses everything in Module 15. What you need: pencil and paper; MolView or Avogadro; Python with the course packages and the [Module 15 lab folder](../../labs/module-15/) (`lesson07_practical.py`, `practical_answers.csv`); the [lab report template](../../templates/lab-report.md). Time: about 120 minutes.

### Part A — the mechanism workbook on paper (50 min)

For each reaction, draw the full mechanism with curved arrows (every lone pair that moves, every intermediate, every formal charge), name the mechanism type, and draw the major product with its stereochemistry. Write which lesson's idea decides the outcome.

1. Propene + HBr.
2. 2-Methylpropene + H₂O with H₂SO₄ catalyst.
3. Cyclohexene + Br₂ in CH₂Cl₂.
4. 1-Methylcyclohexene + BH₃ in THF, then H₂O₂ and NaOH.
5. 2-Butyne + H₂ with Lindlar catalyst.
6. 2-Butyne + Na in liquid NH₃.
7. 1-Butyne + NaNH₂, then CH₃CH₂Br.
8. (R)-2-Bromobutane + NaN₃ in DMF.
9. 2-Bromo-2-methylbutane + potassium tert-butoxide.
10. 2-Methylcyclohexanol + H₂SO₄, heated.

### Part B — check with RDKit (25 min)

1. Write each product as SMILES in the `smiles` column of `practical_answers.csv`. Use `@`/`@@` for stereocentres and `/` and `\` for E/Z bonds. For a racemic product, write either enantiomer. Lesson 15.1 explains SMILES; if you are unsure, draw the product in MolView, save it as a MOL file, and convert it in Python with `Chem.MolToSmiles(Chem.MolFromMolFile("product.mol"))`.
2. Run the checker from the lab folder:

```bash
py lesson07_practical.py
```

3. For every answer that is not "correct", go back to your mechanism, not to the SMILES. The checker says whether you have the right atoms in the wrong arrangement in space ("right constitution, wrong or missing stereochemistry") or a different compound.

How you know it worked: `score: 10 / 10`. The hashed key does not reveal the answers, so a full score means your mechanisms are right.

<details><summary>Reference answers</summary>

1. 2-Bromopropane, `CC(C)Br`: Markovnikov via the secondary cation (15.7, 15.5).
2. tert-Butyl alcohol, `CC(C)(C)O`: tertiary cation, water adds, proton transfer.
3. trans-1,2-Dibromocyclohexane, `Br[C@@H]1CCCC[C@H]1Br` (or its enantiomer): bromonium ion, backside opening, anti addition, racemic (15.3, 15.5).
4. trans-2-Methylcyclohexanol, `C[C@@H]1CCCC[C@H]1O` (or its enantiomer): syn addition, OH on the less substituted carbon.
5. (Z)-2-Butene, `C/C=C\C`: Lindlar, syn.
6. (E)-2-Butene, `C/C=C/C`: dissolving metal, anti.
7. Hex-3-yne, `CCC#CCC`: acidity then SN2 (15.4, 15.5).
8. (S)-2-Azidobutane, `CC[C@H](C)N=[N+]=[N-]`: SN2 inversion; azide outranks ethyl just as Br did, so the letter flips (15.3).
9. 2-Methylbut-1-ene, `C=C(C)CC`: E2 with a bulky base gives the Hofmann product (15.6).
10. 1-Methylcyclohexene, `CC1=CCCCC1`: E1, Zaitsev (15.6). A hydride shift from C2 to C1 gives a tertiary cation that leads to the same alkene.

Full reasons: `py lesson07_practical_solution.py`.

</details>

### Part C — models and write-up (45 min)

1. Build the products of reactions 3 and 4 in MolView or Avogadro and optimise them. For 3, check that the two Br's are on opposite faces (look at the ring edge-on) and find the chair in which both are equatorial and the one in which both are axial. For 4, check that the OH and the CH₃ are trans and both equatorial in the stable chair.
2. Build (Z)- and (E)-2-butene. Measure the C–C=C–C dihedral: 0° and 180°.
3. Write a two-page report with the [lab report template](../../templates/lab-report.md): your ten mechanisms (photos of the paper are fine), your score, each mistake you made and the idea you had missed, and one paragraph on the route to (Z)-hex-3-ene. Paper mechanisms and models do not train bench skills; Module 24 runs several of these reactions on the virtual organic bench.

## Common mistakes

- Putting Br on the less substituted carbon with HBr. Ask which carbocation forms; the nucleophile follows the cation.
- Drawing syn products for Br₂ or anti products for hydroboration. Bromonium → anti; borane → syn.
- Using NaOH or an alkoxide to deprotonate a terminal alkyne. Compare pKa values first: you need NH₂⁻ or a stronger base.
- Alkylating an acetylide with a secondary or tertiary halide. The acetylide is a strong base and eliminates.
- Over-reducing an alkyne. Plain Pd/C with excess H₂ gives the alkane; Lindlar stops at the cis alkene.
- Writing an achiral SMILES for a product that has stereocentres. Racemic still means "trans" or "cis" relative geometry; include it.

## Key takeaways

- Electrophiles add to the π bond. HX and H₃O⁺ go through the more stable carbocation: Markovnikov, with possible rearrangements.
- Br₂ adds anti through a bromonium ion; BH₃ then H₂O₂/NaOH adds H and OH syn with anti-Markovnikov regiochemistry; H₂/Pd adds syn.
- Enthalpies of hydrogenation from NIST data rank alkene stability: 1-butene −126.5, (Z)-2-butene −119.4, (E)-2-butene −116.3 kJ/mol.
- Terminal alkynes (pKa 25) are deprotonated by amide; acetylides do SN2 on methyl and primary halides to make C–C bonds.
- Lindlar gives cis alkenes, Na/NH₃ trans alkenes: choose the reagent for the geometry you need.

## Sources

- [OpenStax Organic Chemistry, 7.6 Stability of Alkenes](https://openstax.org/books/organic-chemistry/pages/7-6-stability-of-alkenes) — heats of hydrogenation and substitution.
- [OpenStax Organic Chemistry, 7.8 Markovnikov's Rule](https://openstax.org/books/organic-chemistry/pages/7-8-orientation-of-electrophilic-additions-markovnikovs-rule) — regiochemistry of HX addition.
- [OpenStax Organic Chemistry, 7.9 Carbocation Structure and Stability](https://openstax.org/books/organic-chemistry/pages/7-9-carbocation-structure-and-stability) — hyperconjugation and the cation order.
- [OpenStax Organic Chemistry, 8.2 Halogenation of Alkenes](https://openstax.org/books/organic-chemistry/pages/8-2-halogenation-of-alkenes-addition-of-x2) — bromonium ion and anti addition.
- [OpenStax Organic Chemistry, 8.5 Hydroboration](https://openstax.org/books/organic-chemistry/pages/8-5-hydration-of-alkenes-addition-of-h2o-by-hydroboration) — syn, anti-Markovnikov hydration.
- [OpenStax Organic Chemistry, 8.6 Hydrogenation](https://openstax.org/books/organic-chemistry/pages/8-6-reduction-of-alkenes-hydrogenation) — catalytic syn addition of H₂.
- [OpenStax Organic Chemistry, 9.5 Reduction of Alkynes](https://openstax.org/books/organic-chemistry/pages/9-5-reduction-of-alkynes) — Lindlar and Na/NH₃.
- [NIST Chemistry WebBook, butane](https://webbook.nist.gov/cgi/cbook.cgi?ID=C106978&Mask=1) — ΔfH°(g) −127.1 kJ/mol (Prosen, Maron and Rossini 1951), used with the butene values of 15.6.
