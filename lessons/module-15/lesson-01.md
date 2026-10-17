---
id: "15.1"
module: 15
minutes: 20
practice_minutes: 60
prerequisites: ["07.3", "07.4", "12.6"]
objectives:
  - Assign sp³, sp² or sp hybridisation to every carbon, nitrogen and oxygen in a molecule and predict its bond angles.
  - Count the σ and π bonds in a molecule and relate bond order to bond length and strength.
  - Translate between condensed, skeletal and SMILES formulas.
  - Identify the functional groups in a drug-sized molecule by eye and with an RDKit substructure search.
volatility: concept
sources:
  - title: "OpenStax Organic Chemistry (McMurry, 2023), 1.6 sp3 Hybrid Orbitals and the Structure of Methane"
    url: https://openstax.org/books/organic-chemistry/pages/1-6-sp3-hybrid-orbitals-and-the-structure-of-methane
  - title: "OpenStax Organic Chemistry, 1.8 sp2 Hybrid Orbitals and the Structure of Ethylene"
    url: https://openstax.org/books/organic-chemistry/pages/1-8-sp2-hybrid-orbitals-and-the-structure-of-ethylene
  - title: "OpenStax Organic Chemistry, 1.9 sp Hybrid Orbitals and the Structure of Acetylene"
    url: https://openstax.org/books/organic-chemistry/pages/1-9-sp-hybrid-orbitals-and-the-structure-of-acetylene
  - title: "OpenStax Organic Chemistry, 3.1 Functional Groups"
    url: https://openstax.org/books/organic-chemistry/pages/3-1-functional-groups
  - title: "Open Yale Courses, CHEM 125a Freshman Organic Chemistry I (McBride, Fall 2008)"
    url: https://oyc.yale.edu/chemistry/chem-125a
  - title: "RDKit 2026.09.1 documentation: Getting Started with the RDKit in Python"
    url: https://www.rdkit.org/docs/GettingStartedInPython.html
  - title: "MolView: web-based molecule sketcher and 3D viewer"
    url: https://molview.org/
  - title: "Avogadro 2.0.0 documentation"
    url: https://two.avogadro.cc/docs/
last_verified: "2026-10-17"
---

# 15.1 · Bonding, hybridisation and functional groups

Organic chemistry is the chemistry of carbon compounds, and almost all of it follows from a few facts about how carbon bonds. This lesson joins the two pictures you already have, VSEPR shapes from Module 7 and molecular orbitals from Module 12, into the one organic chemists use every day: hybrid orbitals, σ and π bonds, and functional groups. You will build molecules in a 3D model viewer and let RDKit, a free chemistry library for Python, check your reading of their structures.

## Why it matters

Aspirin and paracetamol both relieve pain, and both are small molecules built on a benzene ring. Yet aspirin can give up its acetyl group to a protein and paracetamol cannot, and aspirin turns to vinegar-smelling acetic acid in a damp bathroom cabinet while paracetamol does not. The difference is one functional group: aspirin has an ester, paracetamol an amide. Seeing that at a glance tells you which drug is unstable in water and how each will look in an IR spectrum (Module 17). Reading a structure correctly is the first step of every mechanism in Modules 15 and 16.

## Core ideas

> [!NOTE]
> Hybridisation, σ/π bonding and functional groups are stable ideas. Bond lengths and strengths are the values in OpenStax Organic Chemistry (2023), checked 2026-10-17. The tools are MolView (web, free), Avogadro 2.0.0 (free, open source, released 2026-04-01) and RDKit 2026.9.1 from `labs/common/requirements.txt`; menus and versions will change.

### Hybrid orbitals: the shape comes first

Carbon has four valence electrons in one 2s and three 2p orbitals. Yet methane, CH₄, has four identical C–H bonds pointing to the corners of a tetrahedron, 109.5° apart, which is exactly the shape VSEPR predicts for four electron domains ([07.4](../module-07/lesson-04.md)). The orbital model that matches this shape mixes the 2s and the three 2p orbitals into four equivalent **sp³ hybrid orbitals**. A **hybrid orbital** is a mathematical mix of atomic orbitals on one atom, chosen so that it points along a bond.

Count the electron domains (bonds to other atoms plus lone pairs; a double or triple bond counts as one domain) and you know the hybridisation:

| Electron domains | Hybridisation | Shape of domains | Ideal angle | Unused p orbitals | Example |
|---|---|---|---|---|---|
| 4 | sp³ | tetrahedral | 109.5° | 0 | C in ethane, N in NH₃, O in H₂O |
| 3 | sp² | trigonal planar | 120° | 1 | C in ethene, C and O in C=O |
| 2 | sp | linear | 180° | 2 | C in ethyne, C and N in C≡N |

Hybridisation does not cause the shape; it is a convenient way to describe the bonds of a shape that electron repulsion has already fixed.

### σ bonds and π bonds

In the language of [12.6](../module-12/lesson-06.md), a bond is a bonding molecular orbital. Two kinds matter here:

- A **σ (sigma) bond** has its electron density on the line between the two nuclei. Every single bond is a σ bond. It forms from hybrid orbitals (or H 1s) pointing at each other.
- A **π (pi) bond** forms when two parallel p orbitals overlap side by side. Its electron density lies above and below the bond axis, with a node on the axis itself.

A double bond is one σ plus one π; a triple bond is one σ plus two π. Two consequences follow:

1. **Rotation.** You can spin the two ends of a σ bond without breaking it. You cannot twist a π bond, because the p orbitals would stop overlapping. That is why cis- and trans-2-butene are different compounds (lesson [15.3](lesson-03.md)).
2. **Reactivity.** π electrons sit further from the nuclei and are held less tightly. They are where alkenes are attacked ([15.7](lesson-07.md)).

### Bond order, length and strength

More shared electron pairs pull the atoms closer and hold them harder:

| Bond (molecule) | Length / pm | Strength / kJ mol⁻¹ |
|---|---|---|
| C–C (ethane) | 153 | 377 |
| C=C (ethene) | 134 | 728 |
| C≡C (ethyne) | 120 | 965 |
| C–H in ethane / ethene / ethyne | 109 / 109 / 106 | 421 / 464 / 558 |

C=C is not twice as strong as C–C: the π part (about $728 - 377 \approx 350$ kJ/mol) is weaker than the σ part, which is why alkenes react with reagents that leave alkanes alone. The C–H bond gets stronger and shorter from sp³ to sp, because an sp orbital has more s character (50 % against 25 %) and so holds its electrons closer to the nucleus. The same s character makes ethyne's C–H about 10¹⁹ times more acidic than ethene's ([15.4](lesson-04.md)).

### Nitrogen and oxygen hybridise too

Lone pairs are electron domains. Ammonia's N (three bonds, one lone pair) and water's O (two bonds, two lone pairs) are sp³. A carbonyl O is sp². A lone pair next to a π bond often joins it by resonance ([07.3](../module-07/lesson-03.md)); the amide N in paracetamol is then flat and better described as sp².

### Drawing organic molecules

Chemists use three shorthand forms:

- **Condensed formula**: CH₃CH₂OH, groups written in bonding order.
- **Skeletal (line-angle) formula**: every corner and line end is a carbon; hydrogens on carbon are not drawn; every other atom (O, N, Cl, and H on them) is written. Ethanol is a zig-zag of two lines with OH on the end.
- **SMILES** (Simplified Molecular-Input Line-Entry System): a line of text a computer can read. Atoms are letters, `=` and `#` are double and triple bonds, branches go in brackets, ring closures are digits, and lowercase letters are aromatic atoms. Ethanol is `CCO`, acetic acid `CC(=O)O`, benzene `c1ccccc1`, aspirin `CC(=O)Oc1ccccc1C(=O)O`. PubChem lists the SMILES of every compound.

### Functional groups

A **functional group** is a group of atoms that reacts in much the same way in every molecule that carries it. The carbon skeleton is mostly a spectator; the functional group decides the chemistry. Learn these fourteen now (R is any carbon group):

| Group | Pattern | Example | Key behaviour |
|---|---|---|---|
| alkene | C=C | ethene | π bond attacked by electrophiles |
| alkyne | C≡C | ethyne | two π bonds; terminal C–H weakly acidic |
| arene | benzene ring | benzene | aromatic, unusually stable (Module 16) |
| haloalkane | R–X (X = F, Cl, Br, I) | chloroethane | C–X carbon is attacked by nucleophiles |
| alcohol | R–OH (sp³ C) | ethanol | H-bond donor; weak acid and weak base |
| phenol | Ar–OH | paracetamol | more acidic than an alcohol |
| ether | R–O–R | diethyl ether | unreactive; a common solvent |
| amine | R–NH₂, R₂NH, R₃N | ethylamine | basic lone pair on N |
| aldehyde | R–CHO | acetaldehyde | C=O at the end of a chain |
| ketone | R–CO–R | acetone | C=O between two carbons |
| carboxylic acid | R–COOH | acetic acid | acid, pKa about 4–5 |
| ester | R–COO–R | ethyl acetate | hydrolysed by water, faster with acid or base |
| amide | R–CO–NR₂ | acetamide | very stable C–N bond; no basic N |
| nitrile | R–C≡N | acetonitrile | sp carbon and nitrogen |

The order of atoms matters. C(=O)–O–C is an ester, but C–O–C with no C=O is an ether. An OH on an sp³ carbon is an alcohol; on a benzene ring it is a phenol.

## Worked example

### 1. Hybridisation and bonds in acetonitrile, CH₃C≡N

1. CH₃ carbon: four σ bonds (three H, one C), no lone pairs → 4 domains → sp³, angles 109.5°.
2. Nitrile carbon: one σ to CH₃ and a triple bond to N (one domain) → 2 domains → sp. The C–C≡N unit is linear, 180°.
3. Nitrogen: the triple bond and one lone pair → 2 domains → sp.
4. Bonds: 3 C–H + 1 C–C + 1 C≡N σ = 5 σ bonds. The triple bond adds 2 π bonds. Total 5 σ, 2 π.

So C–C≡N is a straight line; a model viewer shows H–C–C about 110° and C–C–N 180°.

### 2. Functional groups in aspirin, `CC(=O)Oc1ccccc1C(=O)O`

Read the SMILES from left to right:

- `CC(=O)O` followed by the ring carbon `c1`: a carbon with C=O, single-bonded to an O that is bonded to the ring. That is an **ester**, C(=O)–O–C; here an aryl ester.
- `c1ccccc1`: six aromatic carbons, a benzene ring, an **arene**.
- `C(=O)O` at the end, with the H of the OH implicit: a **carboxylic acid**.

Bonds: a molecule with $N$ atoms and $r$ rings has $N - 1 + r$ σ bonds. Aspirin, C₉H₈O₄, has 21 atoms and one ring, so 21 σ bonds; π bonds are the two C=O plus three in the Kekulé ring, 5 π. The ester is the weak spot: water slowly cuts it into salicylic acid and acetic acid, which is the vinegar smell of old aspirin.

## Hands-on

What you need: a browser with [MolView](https://molview.org/), or Avogadro 2.0.0 from the [Avogadro site](https://two.avogadro.cc/docs/) if you prefer a desktop program; Python with the course packages (Module 5 setup; `labs/common/requirements.txt` pins RDKit 2026.9.1) and the [Module 15 lab folder](../../labs/module-15/). Record your answers on a [notebook page](../../templates/notebook-page.md). Time: about 60 minutes.

### Part A — build and measure (25 min)

1. In MolView, type `ethane` in the search box, load it and switch the 3D view to ball-and-stick. In Avogadro, draw it with the Draw tool, then run **Extensions → Optimize Geometry**.
2. Use the measure tool to record the C–C length and the H–C–H angle. (MolView: the measurement buttons in the 3D toolbar; Avogadro: the Measure tool, then click two atoms for a distance or three for an angle.)
3. Repeat for ethene and ethyne. For ethene, check that all six atoms lie in one plane: rotate the model to look along the C=C bond.
4. Load paracetamol and write the hybridisation next to each heavy atom.

How you know it worked: C–C 153–154 pm, C=C about 133–134 pm, C≡C about 120–121 pm; angles near 109.5°, 120° and 180°. Values within 1–2 pm of the table are normal, because viewers use slightly different force fields.

### Part B — RDKit reads the structures (25 min)

1. Open `lesson01_groups.py`. Complete `count_sigma_pi` and the two SMARTS patterns for ester and amide. SMARTS is a pattern language for substructures, an extension of SMILES.
2. Run it from the lab folder:

```bash
py lesson01_groups.py
```

3. Compare the table with your pencil answers for aspirin, paracetamol and carvone.

How you know it worked: ethane 7 σ / 0 π, ethene 5 / 1, ethyne 3 / 2, benzene 12 / 3, aspirin 21 / 5, paracetamol 20 / 4. Aspirin shows arene, carboxylic acid and ester; paracetamol arene, phenol and amide; carvone two alkenes and a ketone.

<details><summary>Reference solution and what to notice</summary>

`count_sigma_pi` adds hydrogens, kekulises, and returns `m.GetNumBonds()` and `sum(int(b.GetBondTypeAsDouble()) - 1 for b in m.GetBonds())`. SMARTS: ester `[#6][CX3](=O)[OX2][#6]`, amide `[CX3](=O)[NX3]`. Full code: `lesson01_groups_solution.py`.

What to notice:

- RDKit calls the OH oxygen of acetic acid and the N of acetamide sp², not sp³. Their lone pairs are conjugated with the C=O, which flattens them. Many textbooks still call them sp³; the conjugated description is closer to the measured geometry.
- A SMARTS pattern is only as good as its definition. Delete `;!$(N[CX3]=O)` from the amine pattern and paracetamol's amide N becomes an "amine". That is chemically wrong: an amide N is not basic.

</details>

### Part C — pencil drill (10 min)

For each molecule, give the hybridisation of the named atom and the number of π bonds in the molecule: (a) the central C of allene, H₂C=C=CH₂; (b) the N of trimethylamine, (CH₃)₃N; (c) the C of carbon dioxide; (d) the carbonyl O of acetone.

<details><summary>Answers</summary>

(a) sp, 2 π bonds: two double bonds, two domains. (b) sp³, 0 π: three bonds and a lone pair, pyramidal. (c) sp, 2 π. (d) sp², 1 π in acetone. Build allene in MolView: its two CH₂ ends are twisted 90°, because the central carbon's two p orbitals are at 90° to each other.

</details>

## Common mistakes

- Counting a double bond as two electron domains. A multiple bond is one domain: count the attached atoms plus the lone pairs.
- Forgetting lone pairs. Water's O has only two bonds but four domains, so it is sp³ and bent, not sp and linear.
- Losing the hidden hydrogens of a skeletal formula. Every carbon still has four bonds; add the implicit H's when you count σ bonds.
- Calling an ester an ether or a ketone because it contains C–O–C or C=O. Look at the whole pattern: C(=O)–O–C is an ester.

## Key takeaways

- Count electron domains: 4 → sp³ (109.5°), 3 → sp² (120°), 2 → sp (180°). Lone pairs count.
- Every bond has one σ part; a double bond adds one π bond, a triple bond two. π bonds block rotation and are the reactive part.
- Higher bond order means a shorter, stronger bond; more s character means a shorter, stronger C–H bond.
- Functional groups decide reactivity. Read them from the full pattern of atoms, not from one bond.

## Sources

- [OpenStax Organic Chemistry, 1.6 sp3 Hybrid Orbitals and the Structure of Methane](https://openstax.org/books/organic-chemistry/pages/1-6-sp3-hybrid-orbitals-and-the-structure-of-methane) — sp³ hybrids and the tetrahedral carbon.
- [OpenStax Organic Chemistry, 1.8 sp2 Hybrid Orbitals and the Structure of Ethylene](https://openstax.org/books/organic-chemistry/pages/1-8-sp2-hybrid-orbitals-and-the-structure-of-ethylene) — σ and π bonds in ethene.
- [OpenStax Organic Chemistry, 1.9 sp Hybrid Orbitals and the Structure of Acetylene](https://openstax.org/books/organic-chemistry/pages/1-9-sp-hybrid-orbitals-and-the-structure-of-acetylene) — the bond length and strength table used here.
- [OpenStax Organic Chemistry, 3.1 Functional Groups](https://openstax.org/books/organic-chemistry/pages/3-1-functional-groups) — the functional-group table.
- [Open Yale Courses, CHEM 125a (McBride, Fall 2008)](https://oyc.yale.edu/chemistry/chem-125a) — lectures on bonds and orbitals.
- [RDKit 2026.09.1 documentation: Getting Started in Python](https://www.rdkit.org/docs/GettingStartedInPython.html) — reading SMILES and substructure search with SMARTS.
- [MolView](https://molview.org/) — free web sketcher and 3D viewer with PubChem search.
- [Avogadro 2.0.0 documentation](https://two.avogadro.cc/docs/) — free, open-source desktop molecule editor (BSD licence).
