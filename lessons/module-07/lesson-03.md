---
id: "07.3"
module: 7
minutes: 25
practice_minutes: 45
prerequisites: ["07.2", "04.3"]
objectives:
  - Classify a bond as non-polar covalent, polar covalent or ionic from the electronegativity difference of its atoms.
  - Draw a correct Lewis structure for a molecule or polyatomic ion, with lone pairs and formal charges.
  - Choose the best Lewis structure among several by formal charge, and draw the resonance forms of an ion such as nitrate.
  - Recognise the three kinds of octet exception (too few electrons, odd electron count, expanded valence shell).
volatility: concept
sources:
  - title: "OpenStax Chemistry 2e, 7.1 Ionic Bonding"
    url: https://openstax.org/books/chemistry-2e/pages/7-1-ionic-bonding
  - title: "OpenStax Chemistry 2e, 7.2 Covalent Bonding"
    url: https://openstax.org/books/chemistry-2e/pages/7-2-covalent-bonding
  - title: "OpenStax Chemistry 2e, 7.3 Lewis Symbols and Structures"
    url: https://openstax.org/books/chemistry-2e/pages/7-3-lewis-symbols-and-structures
  - title: "OpenStax Chemistry 2e, 7.4 Formal Charges and Resonance"
    url: https://openstax.org/books/chemistry-2e/pages/7-4-formal-charges-and-resonance
  - title: "OpenStax Chemistry 2e, 7.5 Strengths of Ionic and Covalent Bonds"
    url: https://openstax.org/books/chemistry-2e/pages/7-5-strengths-of-ionic-and-covalent-bonds
  - title: "PubChem (NIH) — compound pages with 2D and 3D structures"
    url: https://pubchem.ncbi.nlm.nih.gov/
last_verified: "2026-10-16"
---

# 07.3 · Ionic and covalent bonding, Lewis structures

Atoms stick together because the electrons of one are attracted to the nucleus of another. This lesson shows the two ends of that story, electrons handed over (ionic bonds) and electrons shared (covalent bonds), and gives you the chemist's quickest tool for picturing a molecule: the Lewis structure. With it you can count bonds, find lone pairs and charges, and spot when one drawing is not enough.

## Why it matters

Baking soda, NaHCO₃, contains both kinds of bond. Na⁺ is held to HCO₃⁻ by an ionic bond, which is why it dissolves in water into ions. Inside HCO₃⁻ the atoms are covalently bonded, which is why the ion stays in one piece and can pick up an H⁺ from vinegar to become carbonic acid and then CO₂. Every reaction mechanism you draw in organic chemistry (Modules 15 and 16) starts from a Lewis structure: the lone pairs are where a molecule attacks, and the formal charges show where it can be attacked. A wrong Lewis structure means a wrong mechanism.

## Core ideas

> [!NOTE]
> Lewis structures, formal charge and resonance are stable teaching models. Electronegativities are Pauling values as printed in OpenStax Chemistry 2e (checked 2026-10-16). The boundaries 0.4 and 1.8 between bond types are rules of thumb, not laws.

### Ionic bonding

In an **ionic bond** one atom gives electrons to another, and the ions that form attract each other by Coulomb's law ([Lesson 04.3](../module-04/lesson-03.md)). Sodium has one valence electron and a low ionisation energy (5.14 eV). Chlorine needs one electron to fill its 3p subshell. The result is Na⁺ and Cl⁻, both with noble-gas configurations.

Taking an electron from Na and giving it to a lone Cl atom actually costs energy (5.14 eV in, about 3.6 eV back from chlorine's electron affinity). What pays for it is the **lattice energy**: the large energy released when the ions pack into a crystal, each surrounded by ions of opposite charge. Ionic solids have no separate molecules; their formula, such as NaCl, gives the ratio of ions.

### Covalent bonding

In a **covalent bond** two atoms share a pair of electrons. The shared pair sits between the two nuclei and attracts both. H₂ is the simplest case. Atoms can share one, two or three pairs: a **single**, **double** or **triple** bond. More shared pairs pull the atoms closer and hold them more strongly:

| Bond | Length (pm) | Bond energy (kJ/mol) |
|---|---|---|
| C–C | 154 | 345 |
| C=C | 134 | 611 |
| C≡C | 120 | 837 |

(Values from OpenStax 7.5.) The **bond order** is the number of shared pairs.

### Electronegativity decides the bond type

When the two atoms are different, the shared pair is pulled toward the more **electronegative** atom (Lesson 07.2). The bond becomes **polar**: one end slightly negative ($\delta-$), the other slightly positive ($\delta+$). The electronegativity difference $\Delta\chi$ is a rough guide:

| $\Delta\chi$ | Bond type | Example |
|---|---|---|
| below 0.4 | non-polar covalent | C–H: $2.55 - 2.20 = 0.35$ |
| 0.4 to 1.8 | polar covalent | O–H: $3.44 - 2.20 = 1.24$ |
| above 1.8 | ionic | Na–Cl: $3.16 - 0.93 = 2.23$ |

The types blend into each other; there is no sharp line. Some Pauling values: H 2.20, C 2.55, N 3.04, O 3.44, F 3.98, Cl 3.16, S 2.58, Na 0.93, K 0.82, Mg 1.31.

### Drawing a Lewis structure

A **Lewis structure** shows every valence electron: bonds as lines (each line is two electrons) and **lone pairs** (pairs not shared) as dots. Main-group atoms in period 2 aim for 8 valence electrons around them (the **octet rule**); hydrogen aims for 2.

The procedure:

1. Count all valence electrons. Add one per negative charge, subtract one per positive charge.
2. Pick the central atom: usually the least electronegative one, and never H.
3. Connect the atoms with single bonds.
4. Put the remaining electrons as lone pairs, outer atoms first, until each has an octet.
5. If the central atom still lacks an octet, turn an outer lone pair into a double (or triple) bond.
6. Check the total and work out the formal charges.

### Formal charge

The **formal charge** is the charge an atom would have if every bond were shared exactly equally:

$$FC = V - L - \tfrac{1}{2}B$$

where $V$ is the atom's valence electrons, $L$ the electrons in its lone pairs, and $B$ the electrons in its bonds. The formal charges add up to the charge of the species. When you can draw more than one structure, the best one has formal charges as close to zero as possible, and any negative formal charge on the most electronegative atom.

### Resonance

Sometimes one Lewis structure cannot describe a molecule. In nitrate, NO₃⁻, you can put the double bond on any of the three oxygens. These three drawings are **resonance structures**, joined by a double-headed arrow ↔. The real ion is none of them: it is a blend, a **resonance hybrid**, with all three N–O bonds the same, each with bond order $1\tfrac13$. Experiment confirms it: all three N–O bonds in nitrate have the same length. The electrons do not flip between structures; the drawings are a limit of the notation.

### Exceptions to the octet rule

- **Too few electrons:** boron in BF₃ has only 6. It readily accepts a lone pair from another molecule.
- **Odd electron count:** NO (11 valence electrons) and NO₂ (17) cannot pair everything. Species with an unpaired electron are **radicals** and are usually reactive.
- **Expanded valence shell:** atoms from period 3 down, such as S in SF₆ (12 electrons around S) and P in PCl₅ (10).

## Worked example

### 1. Carbon dioxide: which structure?

CO₂ has $4 + 2 \times 6 = 16$ valence electrons. Carbon is central. Two structures give every atom an octet:

- A: O=C=O, each O with two lone pairs.
- B: O≡C–O, with one lone pair on the triple-bonded O and three on the single-bonded O.

Formal charges in A: C $= 4 - 0 - 4 = 0$; each O $= 6 - 4 - 2 = 0$. In B: triple-bonded O $= 6 - 2 - 3 = +1$; C $= 0$; single-bonded O $= 6 - 6 - 1 = -1$. Structure A has all zeros, so it is the better one. Measurement agrees: both C–O bonds in CO₂ are 116 pm, the same length.

### 2. Nitrate, NO₃⁻

Electrons: $5 + 3 \times 6 + 1 = 24$. N is central with three single bonds (6 electrons). Give each O three lone pairs (18 more; total 24). N has only 6 electrons, so make one N=O double bond. Formal charges: double-bonded O $= 6 - 4 - 2 = 0$; each single-bonded O $= 6 - 6 - 1 = -1$; N $= 5 - 0 - 4 = +1$. Sum: $0 - 1 - 1 + 1 = -1$, the charge of the ion. The double bond can sit on any of the three O atoms, so there are three resonance structures and the real ion is their average.

## Hands-on

**What you need:** paper and pencil, a web browser for [PubChem](https://pubchem.ncbi.nlm.nih.gov/). **Time:** about 45 minutes.

### Part A — Lewis structures (30 min)

Draw the Lewis structure of each species. Give the total valence electrons and the formal charge of every atom that is not zero. Draw resonance structures where they exist.

1. H₂O
2. NH₄⁺
3. HCN
4. CH₂O (formaldehyde)
5. CO₃²⁻
6. O₃ (ozone)
7. CH₃COOH (acetic acid, in vinegar)
8. BF₃
9. SF₆
10. NO₂

<details><summary>Answers to Part A</summary>

1. H₂O, 8 electrons: two O–H bonds, two lone pairs on O. All formal charges 0.
2. NH₄⁺, 8 electrons: four N–H bonds, no lone pairs. N is +1.
3. HCN, 10 electrons: H–C≡N, one lone pair on N. All 0.
4. CH₂O, 12 electrons: C=O with two C–H; two lone pairs on O. All 0.
5. CO₃²⁻, 24 electrons: one C=O and two C–O. Each single-bonded O is −1. Three resonance structures; every C–O has bond order $1\tfrac13$.
6. O₃, 18 electrons: O=O–O. Central O +1, single-bonded end O −1. Two resonance structures; both O–O bonds equal (128 pm).
7. CH₃COOH, 24 electrons: CH₃–C(=O)–O–H. Two lone pairs on each O. All 0. (A second structure with C–O⁻ and =O⁺–H has charges and is a minor contributor.)
8. BF₃, 24 electrons: three B–F single bonds, three lone pairs on each F. B has only 6 electrons. All 0.
9. SF₆, 48 electrons: six S–F bonds, three lone pairs on each F. S has 12 electrons around it. All 0.
10. NO₂, 17 electrons: O=N–O with one unpaired electron on N. The single-bonded O is −1 and N is +1. Two resonance structures. It is a radical (and a brown, toxic gas in smog).

</details>

### Part B — check against PubChem (15 min)

1. Search PubChem for "formaldehyde", "acetic acid", "carbonate" and "sulfur hexafluoride".
2. On each compound page, look at the 2D structure and the "3D Conformer" view. Compare the connections and any charges with your drawings.
3. For carbonate, notice that PubChem draws one resonance structure. Write one sentence on why the 3D model shows three equal C–O bonds anyway.

**How you know it worked:** 9 or 10 of your structures have the right connections, electron count and formal charges. Your sentence for carbonate says that the real ion is a resonance hybrid, so the drawn single and double bonds are an artefact of drawing one structure.

## Common mistakes

- **Wrong electron count.** Forgetting the ion charge is the most common error. CO₃²⁻ has 24 electrons, not 22.
- **Hydrogen in the centre or with two bonds.** H forms one bond only.
- **Calling one resonance structure "the" structure.** The real species is the hybrid; equal bonds prove it.
- **Using formal charge as the real charge.** Formal charge is bookkeeping. In NH₄⁺ the +1 is spread over the whole ion, not sitting on nitrogen.
- **Forcing an octet on B or on period 3 atoms.** BF₃ is fine with 6; SF₆ needs 12.
- **Treating $\Delta\chi = 1.8$ as a wall.** HF ($\Delta\chi = 1.78$) is a polar covalent molecule; there is a continuum.

## Key takeaways

- Ionic bonds come from electron transfer and Coulomb attraction in a lattice; covalent bonds from shared pairs.
- The electronegativity difference sets how polar a bond is: roughly under 0.4 non-polar, 0.4–1.8 polar, over 1.8 ionic.
- Lewis structures: count electrons, connect, fill outer atoms, make multiple bonds if needed, check formal charges.
- $FC = V - L - B/2$. Prefer the structure with formal charges nearest zero, negative charge on the electronegative atom.
- Resonance structures describe one real hybrid. Octet exceptions: electron-poor B, odd-electron radicals, expanded period 3 atoms.

## Sources

- [OpenStax Chemistry 2e, 7.1 Ionic Bonding](https://openstax.org/books/chemistry-2e/pages/7-1-ionic-bonding).
- [OpenStax Chemistry 2e, 7.2 Covalent Bonding](https://openstax.org/books/chemistry-2e/pages/7-2-covalent-bonding) (electronegativity values and bond types).
- [OpenStax Chemistry 2e, 7.3 Lewis Symbols and Structures](https://openstax.org/books/chemistry-2e/pages/7-3-lewis-symbols-and-structures).
- [OpenStax Chemistry 2e, 7.4 Formal Charges and Resonance](https://openstax.org/books/chemistry-2e/pages/7-4-formal-charges-and-resonance).
- [OpenStax Chemistry 2e, 7.5 Strengths of Ionic and Covalent Bonds](https://openstax.org/books/chemistry-2e/pages/7-5-strengths-of-ionic-and-covalent-bonds) (bond lengths and bond energies).
- [PubChem (NIH)](https://pubchem.ncbi.nlm.nih.gov/) (structures for the hands-on check).
