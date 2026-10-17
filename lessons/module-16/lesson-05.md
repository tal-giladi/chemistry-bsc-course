---
id: "16.5"
module: 16
minutes: 24
practice_minutes: 60
prerequisites: ["16.4", "12.6", "15.7"]
objectives:
  - Use hydrogenation enthalpies to estimate the aromatic stabilisation of benzene, and apply Hückel's 4n+2 rule to rings, ions and heterocycles.
  - Draw the two-step mechanism of electrophilic aromatic substitution and name the electrophile in halogenation, nitration, sulfonation and Friedel–Crafts acylation.
  - Predict where a second substituent goes from the first one (activating or deactivating, ortho/para or meta), and choose the order of steps to make a disubstituted benzene.
volatility: concept
sources:
  - title: "OpenStax Organic Chemistry (2023), 15.2 Structure and Stability of Benzene"
    url: https://openstax.org/books/organic-chemistry/pages/15-2-structure-and-stability-of-benzene
  - title: "OpenStax Organic Chemistry (2023), 15.3 Aromaticity and the Hückel 4n + 2 Rule"
    url: https://openstax.org/books/organic-chemistry/pages/15-3-aromaticity-and-the-huckel-4n-2-rule
  - title: "OpenStax Organic Chemistry (2023), 16.1 Electrophilic Aromatic Substitution Reactions: Bromination"
    url: https://openstax.org/books/organic-chemistry/pages/16-1-electrophilic-aromatic-substitution-reactions-bromination
  - title: "OpenStax Organic Chemistry (2023), 16.2 Other Aromatic Substitutions"
    url: https://openstax.org/books/organic-chemistry/pages/16-2-other-aromatic-substitutions
  - title: "OpenStax Organic Chemistry (2023), 16.3 Alkylation and Acylation of Aromatic Rings: The Friedel–Crafts Reaction"
    url: https://openstax.org/books/organic-chemistry/pages/16-3-alkylation-and-acylation-of-aromatic-rings-the-friedel-crafts-reaction
  - title: "OpenStax Organic Chemistry (2023), 16.4 Substituent Effects in Electrophilic Substitutions"
    url: https://openstax.org/books/organic-chemistry/pages/16-4-substituent-effects-in-electrophilic-substitutions
  - title: "OpenStax Organic Chemistry (2023), 16.10 Synthesis of Polysubstituted Benzenes"
    url: https://openstax.org/books/organic-chemistry/pages/16-10-synthesis-of-polysubstituted-benzenes
  - title: "RDKit Book: aromaticity model"
    url: https://www.rdkit.org/docs/RDKit_Book.html
last_verified: "2026-10-17"
---

# 16.5 · Aromaticity and electrophilic aromatic substitution

Benzene has three C=C double bonds on paper, yet it does not behave like an alkene. Bromine adds instantly to cyclohexene but leaves benzene alone unless a catalyst is present, and even then benzene substitutes a hydrogen instead of adding. This lesson explains the extra stability called aromaticity, gives you Hückel's rule to recognise it, and then works through the reaction aromatic rings do best: electrophilic aromatic substitution. The last part, directing effects and the order of steps, is the most used idea in planning aromatic syntheses.

## Why it matters

A dye chemist needs 3-bromonitrobenzene, and her colleague needs 4-bromonitrobenzene. Both start from benzene and use the same two reactions, bromination and nitration. The only difference is the order. Nitrate first, then brominate: the nitro group sends bromine to the meta position. Brominate first, then nitrate: bromine sends the nitro group to ortho and para, and the para isomer is separated. You will meet this decision in every aromatic synthesis in lesson 16.7.

## Core ideas

> [!NOTE]
> Aromaticity, Hückel's rule and directing effects are settled theory. The hydrogenation enthalpies are from OpenStax 15.2 (cyclohexene −118, 1,3-cyclohexadiene −230, benzene −206 kJ/mol), checked 2026-10-17. RDKit 2026.9.1 uses its own aromaticity model (described in the RDKit Book), which agrees with Hückel for every ring in this lesson.

### How stable is benzene?

Adding H₂ to cyclohexene releases 118 kJ/mol. If benzene were "cyclohexatriene" with three ordinary double bonds, hydrogenating it to cyclohexane should release about $3 \times 118 = 354$ kJ/mol. The measured value is 206 kJ/mol. Benzene is about **148 kJ/mol** more stable than expected:

$$E_\text{stabilisation} \approx 354 - 206 = 148\ \text{kJ/mol}$$

All six C–C bonds are the same length (139 pm, between single and double). The six π electrons are delocalised over the ring. In the molecular-orbital picture of lesson [12.6](../module-12/lesson-06.md), the six p orbitals combine into six π MOs: one at the bottom, two degenerate pairs, one at the top. Six electrons fill exactly the three bonding MOs, a closed shell like a noble gas.

### Hückel's rule

A ring is **aromatic** when it is (1) cyclic, (2) planar, (3) fully conjugated, with a p orbital on every ring atom, and (4) has **4n + 2** π electrons (2, 6, 10, ...). A planar, fully conjugated ring with **4n** π electrons (4, 8) is **antiaromatic**, less stable than an open chain; real molecules avoid it by bending (cyclooctatetraene is tub-shaped) or reacting (cyclobutadiene).

Counting π electrons per ring atom: 1 for each atom in a ring double bond, 2 for an atom that can donate a lone pair (N–H in pyrrole, O in furan, a carbanion), 0 for a carbocation's empty p orbital. An sp³ CH₂ breaks the conjugation.

| Species | π electrons | Verdict |
|---|---|---|
| benzene | 6 | aromatic |
| cyclopentadienyl anion | 6 (4 + lone pair) | aromatic; this is why cyclopentadiene has $\mathrm{p}K_a$ about 16 |
| tropylium cation, C₇H₇⁺ | 6 (empty p on C⁺) | aromatic; a stable carbocation salt |
| cyclobutadiene | 4 | antiaromatic |
| pyridine | 6 (N lone pair is in the ring plane, not counted) | aromatic |
| pyrrole, furan | 6 (N or O lone pair is part of the π system) | aromatic |

The difference between pyridine and pyrrole decides their basicity, which lesson 16.6 uses.

### Electrophilic aromatic substitution (EAS)

An aromatic ring is a weak nucleophile. It reacts only with strong electrophiles, in two steps:

1. The π system attacks the electrophile E⁺. One ring carbon becomes sp³ and the positive charge spreads over three carbons: the **σ-complex** (arenium ion). Aromaticity is lost, so this step is slow.
2. A base removes the H⁺ from the sp³ carbon; the ring becomes aromatic again. Substitution, not addition, because addition would throw away the 148 kJ/mol.

The reactions differ only in how E⁺ is made:

| Reaction | Reagents | Electrophile |
|---|---|---|
| bromination | Br₂, FeBr₃ | Br⁺ (Br–Br–FeBr₃ complex) |
| nitration | HNO₃, H₂SO₄ | nitronium ion, NO₂⁺ |
| sulfonation | SO₃, H₂SO₄ | SO₃ (or HSO₃⁺); reversible |
| Friedel–Crafts acylation | RCOCl, AlCl₃ | acylium ion, RC≡O⁺ |
| Friedel–Crafts alkylation | RCl, AlCl₃ | carbocation R⁺ |

**Friedel–Crafts alkylation** has two problems: the carbocation rearranges (1-chloropropane gives mainly isopropylbenzene), and the alkylated product is more reactive than benzene, so it alkylates again. **Acylation** has neither problem: the acylium ion does not rearrange, and the ketone product is deactivated. To get a straight-chain alkyl group, acylate and then reduce the C=O to CH₂. Neither Friedel–Crafts reaction works on a ring that carries a strongly deactivating (meta-directing) group or an NH₂ (which binds AlCl₃).

### Directing effects: where the second group goes

A substituent already on the ring changes both the **rate** (activating or deactivating) and the **position** of the next substitution. The position follows from the σ-complex: attack ortho or para puts the positive charge on the carbon that carries the substituent. A group that can donate a lone pair (OH, OR, NH₂, NHCOR) stabilises that cation by resonance; an alkyl group stabilises it by induction. A group with a positive or δ+ atom next to the ring (NO₂, C=O, CN, SO₃H, CF₃) destabilises it most at ortho and para, so meta wins by default.

| Group | Effect on rate | Directs to |
|---|---|---|
| –NH₂, –NHR, –OH, –OR | strongly activating | ortho, para |
| –NHCOR, –OCOR | moderately activating | ortho, para |
| –R (alkyl), –Ar | weakly activating | ortho, para |
| –F, –Cl, –Br, –I | weakly deactivating | ortho, para |
| –CHO, –COR, –COOH, –COOR, –CN, –SO₃H, –CF₃, –NO₂ | deactivating | meta |

Halogens are the odd case: they withdraw by induction (slower than benzene) but donate a lone pair by resonance (ortho/para). With two groups on the ring, the **stronger activator wins**, and substitution between two groups that are meta to each other is rare for steric reasons. Para is usually the major ortho/para product with bulky groups.

### Order of events

Three rules plan most disubstituted benzenes:

- Put the group that directs correctly on first.
- Do Friedel–Crafts before any deactivating group is on the ring.
- Use **functional-group interconversion** to change a director: nitro (meta) can be reduced to amino (ortho/para); a methyl (ortho/para) can be oxidised to COOH (meta) with KMnO₄ (lesson [16.1](lesson-01.md)); an acetylated amine (NHCOCH₃) is a gentler ortho/para director than NH₂ and survives nitration.

## Worked example

### 1. Two nitrobenzoic acids from toluene

Both 4-nitrobenzoic acid and 3-nitrobenzoic acid can be made from toluene with the same two steps: nitration (HNO₃, H₂SO₄) and side-chain oxidation (hot KMnO₄, which turns a ring CH₃ into COOH).

- **4-Nitrobenzoic acid**: nitrate first. CH₃ is an ortho/para director, so toluene gives 2- and 4-nitrotoluene; separate the para isomer (it is a solid, the ortho isomer a liquid). Then oxidise CH₃ to COOH. The NO₂ is para to the carbon that becomes COOH.
- **3-Nitrobenzoic acid**: oxidise first. Toluene → benzoic acid; COOH is a meta director, so nitration puts NO₂ meta.

Same reagents, opposite order, different isomer. In the route checker of lesson 16.7 the second route is two lines:

```text
1; oxidise_strong; Cc1ccccc1; OC(=O)c1ccccc1
2; nitration; OC(=O)c1ccccc1; OC(=O)c1cccc([N+](=O)[O-])c1
```

If you swap in the para product at step 2, the checker answers "wrong position: para to C=O ... (meta director)".

### 2. Propylbenzene without rearrangement

Friedel–Crafts alkylation of benzene with 1-chloropropane and AlCl₃ gives mostly isopropylbenzene (cumene): the primary carbocation-like complex rearranges by a hydride shift to the secondary cation. To get the straight chain, acylate with propanoyl chloride and AlCl₃ (no rearrangement; product propiophenone, $\mathrm{C_6H_5COCH_2CH_3}$), then reduce C=O to CH₂ (H₂ over Pd for an aryl ketone, or the Wolff–Kishner reduction). Two steps instead of one, but one product instead of a mixture.

## Hands-on

What you need: the [Module 16 lab folder](../../labs/module-16/) with Python 3.14 and RDKit 2026.9.1, paper and pencil, and a [notebook page](../../templates/notebook-page.md). Time: about 60 minutes. Paper and screen only: nitrating and Friedel–Crafts mixtures are corrosive and are never made at home.

### Part A — Python: a Hückel counter (25 min)

Open `lesson05_aromatic.py` and write `pi_electrons(m, ring)`. The rings are given in Kekulé form, so you can count per atom: 1 for an atom in a ring double bond, 0 for a carbocation carbon, 2 for N, O, S or a carbanion carbon with only single bonds in the ring, and `None` for anything else (an sp³ CH₂).

```bash
py lesson05_aromatic.py
py lesson05_aromatic.py "O=C(O)c1ccccc1"
```

How you know it worked: benzene, cyclopentadienyl anion, tropylium, pyridine, pyrrole, furan and thiophene give 6 (the cyclopropenyl cation 2) and "aromatic", matching RDKit's flag. Cyclobutadiene (4) and cyclooctatetraene (8) print "antiaromatic if planar", and cyclopentadiene prints "not aromatic". The second half of the output, which uses the module's directing rules from `org16.py`, shows toluene and chlorobenzene nitrating ortho/para, nitrobenzene meta, and 4-methylanisole ortho to OCH₃ (the stronger activator wins over CH₃). Benzoic acid, your own run, gives meta.

<details><summary>Reference solution for Part A</summary>

For each ring atom: `double_in_ring = any(b.GetBondType() == Chem.BondType.DOUBLE and b.GetOtherAtomIdx(i) in ring_set for b in a.GetBonds())`; if true add 1; elif carbon with `GetFormalCharge() == 1` add 0; elif symbol in N, O, S, or carbon with charge −1, add 2; else return `None`. Full code in `lesson05_aromatic_solution.py`.

Pyridine's N is in a ring double bond, so it counts 1 and its lone pair (in the ring plane) is not part of the π system. Pyrrole's N has only single bonds in the ring, so its lone pair counts 2. Same element, different job.

</details>

### Part B — product drill (20 min)

Type the major product's SMILES into `ANSWERS` in `lesson05_aromatic.py`:

a. Benzene with acetyl chloride and AlCl₃.
b. Toluene with Br₂ and FeBr₃ (the major isomer).
c. Nitrobenzene with Br₂ and FeBr₃.
d. Anisole with HNO₃ and H₂SO₄ (the major isomer).
e. Acetanilide (N-phenylacetamide) with Br₂ (the major isomer).

<details><summary>Worked answers to Part B</summary>

a. Acetophenone, `CC(=O)c1ccccc1`. Acylium ion; one acylation only, because the ketone deactivates the ring.
b. 4-Bromotoluene, `Cc1ccc(Br)cc1`. CH₃ directs ortho/para; para is the major isomer, with 2-bromotoluene as the minor one.
c. 1-Bromo-3-nitrobenzene, `O=[N+]([O-])c1cccc(Br)c1`. NO₂ is a meta director and makes the reaction slow.
d. 4-Nitroanisole, `COc1ccc([N+](=O)[O-])cc1`. OCH₃ is a strong ortho/para activator; para dominates.
e. 4-Bromoacetanilide, `CC(=O)Nc1ccc(Br)cc1`. The acetamido group activates less than NH₂, so the reaction stops at one bromine; the bulky group favours para. Aniline itself would give 2,4,6-tribromoaniline at once.

</details>

### Part C — pencil: order of events (15 min)

Plan each from benzene, giving reagents and the order: (1) 1-bromo-3-nitrobenzene; (2) 1-bromo-4-nitrobenzene; (3) 3-bromoacetophenone (1-(3-bromophenyl)ethanone). For each, say which group goes on first and why.

<details><summary>Worked answers to Part C</summary>

(1) Nitrate first (HNO₃, H₂SO₄), then brominate (Br₂, FeBr₃): NO₂ directs meta.

(2) Brominate first, then nitrate: Br directs ortho/para; separate the para isomer from the ortho.

(3) Acylate first (CH₃COCl, AlCl₃), then brominate (Br₂, FeBr₃): the acetyl group directs meta. The other order fails twice: bromobenzene would acylate para, and Friedel–Crafts on a ring that already has a meta director does not work at all. Check (3) with the route checker in lesson 16.7: it accepts `fc_acylation` then `bromination_arene` at the meta position.

</details>

## Common mistakes

- **Counting pyridine's lone pair as π electrons.** It lies in the ring plane. Pyridine has 6 π electrons from three C=C/C=N bonds; pyrrole's N lone pair, by contrast, is part of the six.
- **Adding to benzene like an alkene.** EAS restores the ring; the product keeps all three formal double bonds.
- **Using Friedel–Crafts alkylation for a straight chain.** The cation rearranges and the product reacts again. Acylate, then reduce.
- **Running Friedel–Crafts on nitrobenzene or aniline.** Strongly deactivated rings do not react; NH₂ binds AlCl₃.
- **Treating halogens as meta directors because they deactivate.** They deactivate but direct ortho/para.

## Key takeaways

- Benzene is about 148 kJ/mol more stable than three isolated double bonds (206 vs 354 kJ/mol on hydrogenation).
- Aromatic: cyclic, planar, fully conjugated, 4n + 2 π electrons; 4n is antiaromatic.
- EAS: the ring attacks E⁺ to give a σ-complex, then loses H⁺; only the way E⁺ is made changes between reactions.
- Lone-pair donors and alkyl groups direct ortho/para (halogens too, while deactivating); C=O, NO₂, CN, SO₃H, CF₃ direct meta. The strongest activator wins.
- Plan the order: right director first, Friedel–Crafts before deactivators, and interconvert groups (NO₂ → NH₂, CH₃ → COOH) to switch a director.

## Sources

- [OpenStax Organic Chemistry, 15.2 Structure and Stability of Benzene](https://openstax.org/books/organic-chemistry/pages/15-2-structure-and-stability-of-benzene) — hydrogenation enthalpies and the 148 kJ/mol stabilisation.
- [OpenStax Organic Chemistry, 15.3 Aromaticity and the Hückel 4n + 2 Rule](https://openstax.org/books/organic-chemistry/pages/15-3-aromaticity-and-the-huckel-4n-2-rule) — the criteria, antiaromaticity, ions.
- [OpenStax Organic Chemistry, 16.1 Bromination](https://openstax.org/books/organic-chemistry/pages/16-1-electrophilic-aromatic-substitution-reactions-bromination) and [16.2 Other Aromatic Substitutions](https://openstax.org/books/organic-chemistry/pages/16-2-other-aromatic-substitutions) — the EAS mechanism, nitration, sulfonation.
- [OpenStax Organic Chemistry, 16.3 The Friedel–Crafts Reaction](https://openstax.org/books/organic-chemistry/pages/16-3-alkylation-and-acylation-of-aromatic-rings-the-friedel-crafts-reaction) — alkylation limits and acylation.
- [OpenStax Organic Chemistry, 16.4 Substituent Effects](https://openstax.org/books/organic-chemistry/pages/16-4-substituent-effects-in-electrophilic-substitutions) and [16.10 Synthesis of Polysubstituted Benzenes](https://openstax.org/books/organic-chemistry/pages/16-10-synthesis-of-polysubstituted-benzenes) — directing effects and order of steps.
- [RDKit Book](https://www.rdkit.org/docs/RDKit_Book.html) — how RDKit decides aromaticity.
