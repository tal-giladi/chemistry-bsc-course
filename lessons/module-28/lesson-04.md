---
id: "28.4"
module: 28
minutes: 22
practice_minutes: 50
prerequisites: ["28.3", "15.5", "21.1"]
objectives:
  - Rank carbocations and radicals by stability using hyperconjugation, resonance and bond dissociation enthalpies, and calculate radical stabilisation energies.
  - Predict when a carbocation will rearrange by a 1,2-hydride or 1,2-alkyl shift and draw the product.
  - Use σ+ and ρ = −4.54 to predict relative SN1 rates of substituted cumyl chlorides.
  - Distinguish singlet and triplet carbenes by electron configuration and by the stereochemistry of their cyclopropanation products.
volatility: concept
sources:
  - title: "Chemistry LibreTexts, Rearrangement of Carbocations (Supplemental Modules, Organic Chemistry)"
    url: https://chem.libretexts.org/Bookshelves/Organic_Chemistry/Supplemental_Modules_(Organic_Chemistry)/Alkenes/Reactivity_of_Alkenes/Addition_Reactions_of_Alkenes/Rearrangement_of_Carbocations
  - title: "Chemistry LibreTexts, Carbenes (Supplemental Modules, Reactive Intermediates)"
    url: https://chem.libretexts.org/Bookshelves/Organic_Chemistry/Supplemental_Modules_(Organic_Chemistry)/Fundamentals/Reactive_Intermediates/Carbenes
  - title: "Wenthold, Homolytic C-H Bond Dissociation Energies of Organic Molecules (Chemistry LibreTexts; values from Blanksby and Ellison 2003)"
    url: https://chem.libretexts.org/Bookshelves/Organic_Chemistry/Supplemental_Modules_(Organic_Chemistry)/Fundamentals/Homolytic_C-H_Bond_Dissociation_Energies_of_Organic_Molecules
  - title: "Brown and Okamoto (1958), Electrophilic Substituent Constants, J. Am. Chem. Soc. 80, 4979"
    url: https://doi.org/10.1021/ja01551a055
  - title: "The Nobel Prize in Chemistry 1994 (George A. Olah, carbocation chemistry)"
    url: https://www.nobelprize.org/prizes/chemistry/1994/summary/
last_verified: "2026-10-17"
---

# 28.4 · Reactive intermediates: carbocations, radicals, carbenes

Most of the mechanisms in Modules 15 and 16 pass through a species that lives for nanoseconds or less: a carbocation in SN1 and E1, a radical in halogenation and polymerisation, a σ-complex in aromatic substitution. In the language of [28.1](lesson-01.md) these are intermediates: shallow valleys on the energy surface. Their stability decides which path a reaction takes, because by the Hammond postulate ([28.2](lesson-02.md)) the transition state that leads to them looks like them. This lesson puts numbers on the three classic carbon intermediates, carbocations, radicals and carbenes, using bond enthalpies, σ+ constants and the Boltzmann distribution.

## Why it matters

Add HCl to 3,3-dimethyl-1-butene and you might expect 2-chloro-3,3-dimethylbutane, the Markovnikov product. The main product is 2-chloro-2,3-dimethylbutane instead: the chlorine ends up on a different carbon, and the carbon skeleton has changed. A methyl group moved while the reaction was under way. In a pharmaceutical process an unexpected rearrangement like this is a new impurity with its own toxicology. Recognising which intermediate forms, and whether it can improve itself by a shift, lets you predict the product before the analytical lab finds it.

## Core ideas

> [!NOTE]
> The structures and stability orders are stable textbook chemistry. Bond enthalpies are the evaluated 298 K values of Blanksby and Ellison (2003); σ+ values are from Hansch, Leo and Taft (1991); the carbene singlet–triplet gap is the typical value given on LibreTexts for simple hydrocarbon carbenes. Checked on 2026-10-17.

### Carbocations

A **carbocation** has a carbon with only six valence electrons and a positive charge. The carbon is sp² hybridised and planar, with an empty p orbital perpendicular to the plane. Anything that can push electron density into that empty orbital stabilises it:

- **Hyperconjugation**: a neighbouring C–H or C–C σ bond lined up with the empty p orbital shares some of its electron density. Each alkyl group adds such bonds, so stability rises methyl < primary < secondary < tertiary.
- **Resonance**: an adjacent C=C (allyl cation) or benzene ring (benzyl cation) spreads the charge over several carbons. A lone pair on an adjacent O or N does even better (an oxocarbenium or iminium ion).
- **Para substituents on an aryl ring**: measured by σ+ (lesson [28.3](lesson-03.md)). SN1 solvolysis of cumyl chlorides, ArC(CH₃)₂Cl, has ρ = −4.54, so a para-methoxy group (σ+ = −0.78) speeds ionisation by a factor of about 3500.

Vinyl and aryl cations, whose empty orbital is an sp² orbital in the plane, are very unstable and rarely form. Carbocations were long known only as fleeting intermediates. George Olah showed in the 1960s that in very strong acids ("superacids") simple carbocations live long enough to record their NMR spectra, work recognised by the 1994 Nobel Prize in Chemistry.

### Carbocation rearrangements

A carbocation next to a carbon that carries an H atom or an alkyl group can let that group slide over, with its bonding pair, to the positive carbon. This is a **1,2-shift** (hydride shift or alkyl shift). The positive charge moves to the carbon that lost the group. Such shifts have small barriers and happen whenever they give a more stable cation, usually secondary to tertiary. In the HCl example, protonation gives a secondary cation next to a quaternary carbon; a methyl shift makes it tertiary, and chloride is captured there. Watch for rearrangements in any SN1, E1 or acid-catalysed reaction ([15.5](../module-15/lesson-05.md), [15.6](../module-15/lesson-06.md)).

### Radicals

A **radical** has an unpaired electron; a carbon radical has seven valence electrons. Simple alkyl radicals are nearly planar, with the odd electron in a p orbital. Radicals are stabilised by the same effects as carbocations, but less strongly, because one electron in the p orbital needs less help than an empty one. The cleanest measure is the **bond dissociation enthalpy** (BDE) of the R–H bond: the weaker the bond, the more stable the radical it gives. The **radical stabilisation energy** (RSE) compares each radical with methyl:

$$\mathrm{RSE(R\cdot)} = \mathrm{BDE(CH_3{-}H)} - \mathrm{BDE(R{-}H)}$$

| Radical | BDE of R–H (kJ/mol) | RSE (kJ/mol) |
|---|---|---|
| methyl | 439.3 | 0 |
| ethyl (primary) | 423.0 | 16 |
| isopropyl (secondary) | 412.5 | 27 |
| tert-butyl (tertiary) | 403.8 | 36 |
| benzyl | 375.3 | 64 |
| allyl | 371.5 | 68 |
| vinyl | 463.2 | −24 |
| phenyl | 472.4 | −33 |

Resonance (allyl, benzyl) is worth about twice as much as three alkyl groups. Vinyl and phenyl radicals, with the odd electron in an sp² orbital, are less stable than methyl, so their C–H bonds are hard to break. Most radicals react in microseconds or faster with each other or with other molecules; **persistent** radicals such as TEMPO or the triphenylmethyl radical survive because bulk or resonance blocks their reactions. Radical chain reactions follow the initiation, propagation and termination steps of [22.3](../module-22/lesson-03.md).

### Carbenes

A **carbene** is a neutral carbon with only two bonds and two non-bonding electrons, as in methylene, CH₂. The two electrons can be arranged in two ways:

- **Singlet**: both electrons paired in one sp² orbital, with an empty p orbital. Bent (about 102° for CH₂). It behaves like a carbocation and a carbanion at once.
- **Triplet**: one electron in each of two orbitals, spins parallel. Wider angle (125–140° for CH₂). It behaves like a diradical.

For CH₂ and simple hydrocarbon carbenes the triplet is the ground state, typically about 33 kJ/mol below the singlet. Carbenes with a halogen, O or N on the carbene carbon, such as dichlorocarbene, are usually singlets, because the lone pairs of those atoms donate into the empty p orbital.

The **Skell test** tells the two apart by stereochemistry. A singlet carbene adds to an alkene in one step, so cis-2-butene gives only cis-1,2-dimethylcyclopropane and trans gives only trans. A triplet adds in two steps through a diradical that can rotate before the second bond closes, so both alkenes give similar cis/trans mixtures. A triplet ground state does not mean triplet chemistry: if the singlet is much more reactive and the two interconvert quickly, most of the product can come from the tiny singlet population. That is the Curtin–Hammett principle of [28.1](lesson-01.md) again.

## Worked example

### 1. How much does a para substituent change an SN1 rate?

Cumyl chlorides ionise to tertiary benzylic cations, ρ = −4.54 with σ+. Compare p-methoxy and p-nitro with the parent.

1. p-OCH₃: $\log(k/k_H) = -4.54 \times (-0.78) = 3.54$, so $k/k_H = 3.5\times10^3$.
2. p-NO₂: $\log(k/k_H) = -4.54 \times 0.79 = -3.59$, so $k/k_H = 2.6\times10^{-4}$.
3. Between them: $10^{3.54 + 3.59} = 10^{7.1} \approx 1.3\times10^7$.

With ordinary σp for methoxy (−0.27) you would predict only $10^{1.23} = 17$, two hundred times too low. The methoxy lone pair conjugates directly with the cationic centre, which is exactly what σ+ captures. For p-NO₂ the two scales agree (0.78 against 0.79): a nitro group cannot donate electrons, so there is no extra resonance to count.

### 2. Why radical bromination attacks the side chain of toluene

Toluene has three benzylic C–H bonds (375.3 kJ/mol) and five aromatic C–H bonds (472.4 kJ/mol). A bromine atom makes H–Br (366.2 kJ/mol).

1. Benzylic abstraction: $\Delta H = 375.3 - 366.2 = +9.1$ kJ/mol.
2. Ring abstraction: $\Delta H = 472.4 - 366.2 = +106.2$ kJ/mol.
3. Compared with a primary alkyl C–H (423.0 kJ/mol, $\Delta H = +56.8$), the benzylic step is 47.7 kJ/mol less uphill.

The bromine transition state is late (α ≈ 1, lesson 28.2), so nearly all of that difference appears in the barrier: the side chain reacts and the ring hydrogens are untouched. The benzyl radical's 64 kJ/mol of resonance stabilisation is the reason.

## Hands-on

What you need: Python with the course packages and the [Module 28 lab folder](../../labs/module-28/), pencil and paper. Time: about 50 minutes.

### Part A — Python: three intermediates, three kinds of number (25 min)

1. Open `lesson04_intermediates.py`. It uses the bond enthalpies and σ table from `sr28.py`.
2. Complete `rse()` (radical stabilisation energy), `hammett_factor()` (rate ratio from ρ and σ) and `singlet_fraction()` (Boltzmann populations with degeneracies, as in [21.1](../module-21/lesson-01.md): the triplet has three spin states, the singlet one).
3. Run it and open `runs/lesson04_intermediates.png`:

```bash
py lesson04_intermediates.py
```

How you know it worked: RSE +16.3 (ethyl), +26.8 (isopropyl), +35.5 (tert-butyl), +64.0 (benzyl), +67.8 (allyl), −23.9 (vinyl) and −33.1 kJ/mol (phenyl). Cumyl factors with σ+: p-OCH₃ 3.48 × 10³, p-CH₃ 25.6, p-F 2.08, p-Cl 0.317, p-NO₂ 2.6 × 10⁻⁴ (with σp, p-OCH₃ would be only 16.8 and p-F would even come out slower than the parent). Carbene singlet fraction at 298 K with a 33 kJ/mol gap: 5.5 × 10⁻⁷.

<details><summary>Reference solution</summary>

```python
def rse(bond):
    return BDE["CH3-H"] - BDE[bond]

def hammett_factor(rho, sigma):
    return 10 ** (rho * sigma)

def singlet_fraction(gap_kj, T=298.15, g_singlet=1, g_triplet=3):
    w_s = g_singlet * math.exp(-gap_kj * 1000 / (R * T))
    return w_s / (w_s + g_triplet)
```

Full code: `lesson04_intermediates_solution.py`. The script also asks what happens if the singlet reacts a million times faster than the triplet: it then makes about a third of the product even though only one carbene in two million is a singlet, provided spin interconversion is faster than either reaction. Whether that proviso holds has to be measured; it is not true for every carbene.

</details>

### Part B — pencil (25 min)

1. 3-Methyl-1-butene reacts with HBr. Draw the first carbocation, the rearrangement, and the main product.
2. Rank these cations from least to most stable and give one reason for each step: phenyl cation C₆H₅⁺, ethyl CH₃CH₂⁺, tert-butyl (CH₃)₃C⁺, methoxymethyl CH₃O–CH₂⁺.
3. A carbene made by photolysis adds to cis-2-butene and to trans-2-butene. Both alkenes give the same 60:40 mixture of trans- and cis-1,2-dimethylcyclopropane. Which spin state reacted, and why?
4. Take α = 1 for bromine. Estimate how much faster, per hydrogen, a bromine atom abstracts a benzylic H from toluene than a primary H from ethane at 25 °C. Why is this an upper limit?

<details><summary>Answers to Part B</summary>

1. Protonation at C1 (Markovnikov) gives a secondary cation at C2, next to C3, which carries one H. A 1,2-hydride shift moves that H to C2 and the charge to C3, which is tertiary. Bromide adds there: the main product is 2-bromo-2-methylbutane, (CH₃)₂CBr–CH₂CH₃.
2. Phenyl < ethyl < tert-butyl < methoxymethyl. Phenyl: the empty orbital is an in-plane sp² orbital that the ring π system cannot reach. Ethyl: one alkyl group, a few hyperconjugating C–H bonds. Tert-butyl: three alkyl groups, nine C–H bonds for hyperconjugation. Methoxymethyl: the oxygen lone pair forms a π bond to the cationic carbon (an oxocarbenium ion), the strongest donation of all.
3. A triplet. The same mixture from both alkene isomers means the first C–C bond formed a diradical that could rotate before the ring closed, so the alkene geometry was lost. A singlet would add in one step and keep it: cis from cis, trans from trans.
4. $\delta\Delta H = 423.0 - 375.3 = 47.7$ kJ/mol, so $e^{47.7/2.479} = e^{19.2} \approx 2\times10^8$. It is an upper limit because α = 1 assumes the transition state feels all of the radical's stabilisation; real transition states are a little earlier, and entropy and tunnelling differences are ignored.

</details>

## Common mistakes

- Treating a carbocation and a radical as equally sensitive to substitution. Radicals gain only about half as much from each alkyl or resonance contribution.
- Forgetting rearrangements in SN1, E1 and acid-catalysed additions. Always ask whether a 1,2-shift gives a more stable cation.
- Reading a low bond dissociation enthalpy as a "strong" radical. A low BDE means a stable, less reactive radical.
- Using σp instead of σ+ for cations conjugated with a para donor; the error for methoxy is a factor of 200 in rate.
- Assuming a triplet ground-state carbene must react as a triplet. Product stereochemistry, not the ground state, tells you which spin state reacted.

## Key takeaways

- Carbocations are planar with an empty p orbital; stability rises with alkyl substitution (hyperconjugation), resonance and adjacent lone pairs; vinyl and aryl cations are poor.
- 1,2-Hydride and 1,2-alkyl shifts convert a cation into a more stable one; expect them whenever a carbocation forms next to a more substituted carbon.
- Radical stability follows bond enthalpies: RSE = BDE(CH₃–H) − BDE(R–H), from 16 kJ/mol for ethyl to 68 kJ/mol for allyl.
- Carbenes come as singlets (paired, bent, concerted and stereospecific additions) or triplets (diradical, stepwise, stereochemistry lost); simple hydrocarbon carbenes have triplet ground states about 33 kJ/mol below the singlet.
- σ+ and ρ = −4.54 turn carbocation stability into predicted SN1 rates over seven orders of magnitude.

## Sources

- [Chemistry LibreTexts, Rearrangement of Carbocations](https://chem.libretexts.org/Bookshelves/Organic_Chemistry/Supplemental_Modules_(Organic_Chemistry)/Alkenes/Reactivity_of_Alkenes/Addition_Reactions_of_Alkenes/Rearrangement_of_Carbocations) — HCl and 3,3-dimethyl-1-butene, 1,2-methyl and hydride shifts.
- [Chemistry LibreTexts, Carbenes](https://chem.libretexts.org/Bookshelves/Organic_Chemistry/Supplemental_Modules_(Organic_Chemistry)/Fundamentals/Reactive_Intermediates/Carbenes) — singlet and triplet structures, bond angles of CH₂ (102° and 125–140°), triplet about 33 kJ/mol lower for simple hydrocarbons, Skell test, dichlorocarbene.
- [Wenthold, Homolytic C–H Bond Dissociation Energies of Organic Molecules (LibreTexts)](https://chem.libretexts.org/Bookshelves/Organic_Chemistry/Supplemental_Modules_(Organic_Chemistry)/Fundamentals/Homolytic_C-H_Bond_Dissociation_Energies_of_Organic_Molecules) — 298 K C–H bond enthalpies from Blanksby and Ellison, Acc. Chem. Res. 36, 255 (2003).
- [Brown and Okamoto, J. Am. Chem. Soc. 80, 4979 (1958)](https://doi.org/10.1021/ja01551a055) — σ+ from cumyl chloride solvolysis, ρ = −4.54.
- [The Nobel Prize in Chemistry 1994](https://www.nobelprize.org/prizes/chemistry/1994/summary/) — George A. Olah, "for his contribution to carbocation chemistry".
