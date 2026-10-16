---
id: "06.2"
module: 6
minutes: 22
practice_minutes: 75
prerequisites: ["06.1", "02.1"]
objectives:
  - Calculate the net charge of a peptide or protein at a given pH from its side-chain pKa values.
  - Describe the peptide bond and the hydrogen-bond patterns of the α-helix and the β-sheet in terms of backbone atoms.
  - Find a protein in UniProt and the PDB and read its sequence length, mass, method and resolution.
  - Count the backbone hydrogen bonds of ubiquitin in Mol* and in Python, and explain why many hydrogen bonds still give a protein only marginal stability.
volatility: concept
sources:
  - title: "OpenStax Biology 2e, 3.4 Proteins"
    url: https://openstax.org/books/biology-2e/pages/3-4-proteins
  - title: "RCSB PDB entry 1UBQ: Structure of ubiquitin refined at 1.8 Å resolution"
    url: https://www.rcsb.org/structure/1UBQ
  - title: "UniProt P0CG48 (UBC_HUMAN), Polyubiquitin-C"
    url: https://www.uniprot.org/uniprotkb/P0CG48/entry
  - title: "wwPDB usage policies (PDB data are CC0)"
    url: https://www.wwpdb.org/about/usage-policies
  - title: "Mol* Viewer documentation"
    url: https://molstar.org/viewer-docs/
  - title: "Kabsch and Sander (1983), Dictionary of protein secondary structure (DSSP), Biopolymers 22, 2577"
    url: https://doi.org/10.1002/bip.360221211
  - title: "EMBOSS iep: pKa values used for isoelectric points"
    url: https://emboss.sourceforge.net/apps/cvs/emboss/apps/iep.html
  - title: "Pace et al. (2014), Contribution of hydrogen bonds to protein stability, Protein Science 23, 652"
    url: https://doi.org/10.1002/pro.2449
  - title: "Dadarlat and Post (2008), charged groups and the stability of globular proteins, J. Phys. Chem. B"
    url: https://pmc.ncbi.nlm.nih.gov/articles/PMC4927099
last_verified: "2026-10-16"
---

# 06.2 · Proteins: from amino acids to folds

Proteins are the cell's machines: enzymes, pumps, channels, motors, sensors and scaffolds. Chemically, each one is a single long chain of amino acids joined by amide bonds, and the order of its 20 kinds of building block decides how the chain folds into a precise three-dimensional shape. This lesson reads proteins as a chemist does: acid–base groups that set the charge, a planar amide backbone that hydrogen-bonds to itself, and a fold held by many weak interactions. You will open a real crystal structure and count its hydrogen bonds, by eye and in Python.

## Why it matters

A biochemist wants to purify a protein by ion-exchange chromatography, which separates molecules by charge. Should the buffer be at pH 6 or pH 8, and should the column carry positive or negative groups? The answer comes from the protein's acid–base groups and their pKa values, the same chemistry as lesson [02.1](../module-02/lesson-01.md). A structural biologist asks a different question: a mutation removes one hydrogen bond deep inside an enzyme; will the protein still fold? Answering it needs the idea that a protein is only just stable. Proteins return in enzyme kinetics (Module 29), metal sites (Module 26) and protein assays by UV-Vis and fluorescence (Module 19).

## Core ideas

> [!NOTE]
> The chemistry is stable. The pKa values are the EMBOSS set; other tables differ by a few tenths, so computed isoelectric points differ too. Database pages (UniProt, RCSB PDB) and the Mol* interface change their layout from time to time; the entry IDs 1UBQ and P0CG48 do not. Checked 2026-10-16.

### Amino acids

An amino acid has a central carbon (the α-carbon) carrying an amino group, a carboxylic acid group, a hydrogen and a side chain, called R. The 20 common side chains fall into four chemical groups:

| Group | Examples | What the side chain does |
|---|---|---|
| Nonpolar | Ala, Val, Leu, Ile, Phe, Met, Trp, Pro | Hides from water in the protein's core |
| Polar, uncharged | Ser, Thr, Asn, Gln, Tyr, Cys | Hydrogen-bonds; Cys can form S–S bridges |
| Acidic | Asp, Glu | Carboxylate, negative at pH 7 |
| Basic | Lys, Arg, His | Ammonium or guanidinium, positive at pH 7; His is half-way |

In water at pH 7 a free amino acid is a zwitterion: $\text{H}_3\text{N}^+$ at one end and $\text{COO}^-$ at the other.

### Charge depends on pH

Each acid–base group follows the Henderson–Hasselbalch relation. For a basic group (pKa of its protonated form), the fraction carrying a positive charge is

$$f_+ = \frac{1}{1 + 10^{\,\mathrm{pH} - \mathrm{p}K_a}}$$

and for an acidic group the fraction carrying a negative charge is $f_- = 1/(1 + 10^{\,\mathrm{p}K_a - \mathrm{pH}})$. The net charge of a protein is the sum over its N-terminus, C-terminus and ionisable side chains. The pH where it is zero is the isoelectric point, pI. Below its pI a protein is positive; above it, negative.

The useful pattern: a group is half-charged at pH = pKa, about 91 % charged one unit beyond, and 99 % two units beyond. Histidine, with pKa about 6.5, is the only side chain that changes charge across the physiological range, which is why it so often sits in enzyme active sites.

### The peptide bond

Two amino acids join by a condensation reaction: the carboxyl of one and the amino group of the next lose a water molecule and form an amide, here called the peptide bond. A chain has a direction, from the free amino end (N-terminus) to the free carboxyl end (C-terminus).

The C–N bond has partial double-bond character: the nitrogen's lone pair is shared with the carbonyl (resonance, Module 7). As a result the six atoms around each peptide bond lie in one plane, almost always in the trans arrangement. The chain can only rotate about the two single bonds at each α-carbon. That restriction is what makes regular folds possible. Each peptide unit also has a hydrogen-bond donor (N–H) and an acceptor (C=O).

### Levels of structure

- Primary structure is the sequence, written N to C in one-letter codes.
- Secondary structure is the local backbone pattern. In the α-helix, the C=O of residue $i$ accepts a hydrogen bond from the N–H of residue $i+4$, so all the bonds run along the helix axis. A turn has 3.6 residues and rises 0.54 nm, or 0.15 nm per residue. In a β-sheet, extended strands lie side by side and hydrogen-bond across, between strands that can be far apart in sequence.
- Tertiary structure is the full fold of one chain: helices and sheets packed with nonpolar side chains inside, polar and charged ones outside.
- Quaternary structure is the assembly of several chains, as in haemoglobin's four.

### Why a fold is only just stable

A folded protein is held by hydrophobic burial (lesson [06.1](lesson-01.md)), hydrogen bonds, salt bridges between opposite charges, and sometimes disulfide bridges. A small protein has dozens of backbone hydrogen bonds, each worth roughly 10 kJ/mol as an electrostatic attraction. Yet the free energy difference between folded and unfolded forms is small: most globular proteins are only marginally stable at body temperature, and losing a few kJ/mol through one mutation can be enough to cause disease.

The reason is bookkeeping. In the unfolded chain, the same N–H and C=O groups hydrogen-bond to water. Folding swaps those for internal bonds and gains little per swap; it also pays a large entropy cost for fixing the chain in one shape. The net stability is the small difference of large terms. Measurements on mutants show that buried hydrogen bonds do stabilise proteins, by an amount that depends strongly on their surroundings.

### Where to find structures

- UniProt holds sequences and what is known about each protein's function. Entry P0CG48 is human polyubiquitin-C, a precursor of nine copies of the 76-residue protein ubiquitin.
- The Protein Data Bank (PDB) holds 3D structures. Entry 1UBQ is human ubiquitin, solved by X-ray diffraction at 1.8 Å resolution in 1987. Resolution is the smallest detail the data show; below about 2 Å, individual side chains are clear. PDB files are released as CC0, free for any use.
- Mol* is the free browser viewer used by the PDB. It colours by secondary structure and draws non-covalent interactions as dashed lines.

## Worked example

### 1. A histidine peptide near pH 7

What is the charge of the tripeptide Gly-His-Glu at pH 6.0 and at pH 7.4? EMBOSS pKa values: N-terminus 8.6, His 6.5, Glu 4.1, C-terminus 3.6.

At pH 7.4:

$$\underbrace{\tfrac{1}{1+10^{-1.2}}}_{\text{N-term } 0.941} + \underbrace{\tfrac{1}{1+10^{0.9}}}_{\text{His } 0.112} - \underbrace{\tfrac{1}{1+10^{-3.3}}}_{\text{Glu } 0.999} - \underbrace{\tfrac{1}{1+10^{-3.8}}}_{\text{C-term } 1.000} = -0.95$$

At pH 6.0 the terms are 0.997, 0.760, 0.987 and 0.996, giving −0.23.

Interpretation: almost all the change comes from histidine, whose charge goes from 0.76 to 0.11 over 1.4 pH units. The other groups are fully charged at both pH values.

### 2. Counting hydrogen bonds in a helix

Ubiquitin's helix runs from Ile23 to Glu34, 12 residues. Its length is $12 \times 0.15 = 1.8$ nm, and it makes $12 / 3.6 = 3.3$ turns. Inside a perfect helix of $n$ residues there are $n - 4$ bonds of the $i \to i+4$ type, here 8. The residues just before and after a helix, the caps, often add one bond at each end. So you expect 8 to 10 such bonds in the hands-on.

## Hands-on

What you need: a browser, the [Module 6 lab folder](../../labs/module-06/) with Python set up, and about 75 minutes. No home materials.

### Part A — read the entries (15 min)

1. Open the UniProt entry [P0CG48](https://www.uniprot.org/uniprotkb/P0CG48/entry). Note the length of the precursor, the number of ubiquitin repeats and the sequence of the first 76 residues.
2. Open the PDB entry [1UBQ](https://www.rcsb.org/structure/1UBQ). Note the method, the resolution, the deposition year and the number of residues modelled.

### Part B — look and count in Mol* (25 min)

1. Open the structure in the Mol* viewer: `https://molstar.org/viewer/?pdb=1UBQ`. The cartoon shows the helix as a ribbon spiral and the β-strands as arrows.
2. Find the helix (residues 23–34) in the sequence panel at the top. Click residue 27. Mol* focuses on it and draws its non-covalent interactions as dashed lines; hover over a line to see its type and length.
3. Click residues 23 to 35 one by one and write down every backbone hydrogen bond of the type O($i$)···H–N($i+4$) with its length. Then click residues in the long β-strand 10–17 and note which strand each partner belongs to.
4. Record your counts in a [notebook page](../../templates/notebook-page.md).

### Part C — check with Python (35 min)

`lesson02_proteins.py` reads `ubiquitin_1UBQ.pdb` (the protein atoms of 1UBQ, waters removed). It places each amide hydrogen the way the standard DSSP method does, then scores every N–H···O=C pair with DSSP's electrostatic energy

$$E = 0.084 \times 332 \left(\frac{1}{r_{ON}} + \frac{1}{r_{CH}} - \frac{1}{r_{OH}} - \frac{1}{r_{CN}}\right)\ \text{kcal/mol}$$

(distances in Å), counting a hydrogen bond when $E < -0.5$ kcal/mol (−2.1 kJ/mol). This is Coulomb's law from lesson [04.3](../module-04/lesson-03.md) with partial charges on four atoms. Fill in the three TODO functions and run:

```bash
py lesson02_proteins.py
```

How you know it worked: the script prints the 76-residue sequence (identical to the first 76 residues in UniProt), a net charge of +0.23 at pH 7.0, a pI of 7.54 with this pKa set, 47 backbone hydrogen bonds with $|i - j| \ge 3$ (12 of type $i \to i+4$, 9 of type $i \to i+3$, 26 others), and 10 helix bonds from O22–N26 to O31–N35. The mean energy is −9.0 kJ/mol. The charge plot is saved to `runs/lesson02_charge.png`.

<details><summary>Reference solution and interpretation</summary>

`net_charge`: start with `+1/(1+10**(pH-8.6))` for the N-terminus and `-1/(1+10**(3.6-pH))` for the C-terminus, then add a term for each K, R, H, D, E, C, Y. `hbond_energy`: the four distances with `np.linalg.norm`, the formula above, times 4.184. `find_hbonds`: two loops, skip near neighbours, keep pairs under the cutoff. Full code: `lesson02_proteins_solution.py`.

Your Mol* count will be close but rarely identical. Mol* uses distance and angle rules on its own hydrogen positions, while the script uses DSSP's energy; bonds near the cutoff, such as the weak O30–N35 contact (3.6 Å), may appear in one and not the other. Name the criterion whenever you report a count.

The 10 helix bonds include the two caps, residues 22 and 35, as predicted in the worked example. The 26 "other" bonds are mostly between β-strands: strand 1–7 pairs with 10–17 (a hairpin) and with 64–72, whose partners are about 60 residues away in sequence.

Interpretation: 47 bonds at about −9 kJ/mol would add up to more than −400 kJ/mol, far beyond any protein's real folding stability. In the unfolded chain each of those groups is bonded to water instead, so folding gains only the small difference. The pI of 7.54 also explains why ubiquitin has almost no net charge in a cell: at pH 7.4 it carries +0.05 with this pKa set. A different pKa table would move that value by several tenths, so for ion exchange you would choose a buffer at least one pH unit from the pI.

</details>

Extension: run `py fetch_pdb.py 4HHB` and then `py lesson02_proteins.py data/downloaded/4HHB.pdb` to count the bonds in chain A of haemoglobin, an all-helix protein. Compare its share of $i \to i+4$ bonds with ubiquitin's: about three quarters (83 of 110) against a quarter (12 of 47).

## Common mistakes

- Counting the termini as side chains, or forgetting them. Each chain has exactly one N-terminus and one C-terminus, whatever its length.
- Using pKa − pH instead of pH − pKa for a basic group. Sanity check: at very low pH every basic group must be fully positive.
- Reporting a hydrogen-bond count without its criterion. Distance-only, angle-based and energy-based methods give different numbers for the same file.
- Treating every hydrogen bond in a folded protein as a gain of its full energy. The unfolded chain is hydrogen-bonded to water.
- Reading a PDB structure as exact. It is a model fitted to data; check the resolution, and remember that every atom position has an uncertainty.

## Key takeaways

- A protein's charge is the sum of Henderson–Hasselbalch fractions over its termini and ionisable side chains; histidine is the group that changes near pH 7.
- The peptide bond is a planar amide with one donor and one acceptor; the α-helix bonds O($i$) to N–H($i+4$), the β-sheet bonds across strands.
- UniProt gives sequence and function, the PDB gives the 3D model with its method and resolution, and Mol* lets you inspect it in a browser.
- Ubiquitin has 47 backbone hydrogen bonds by the DSSP criterion, yet like most proteins it is only marginally stable, because folding trades bonds to water for bonds inside.

## Sources

- [OpenStax Biology 2e, 3.4 Proteins](https://openstax.org/books/biology-2e/pages/3-4-proteins) — amino acids, the peptide bond, the α-helix ($i \to i+4$) and β-sheet.
- [RCSB PDB 1UBQ](https://www.rcsb.org/structure/1UBQ) — ubiquitin, X-ray, 1.8 Å, 76 residues; [wwPDB usage policies](https://www.wwpdb.org/about/usage-policies) — CC0 licence.
- [UniProt P0CG48](https://www.uniprot.org/uniprotkb/P0CG48/entry) — polyubiquitin-C, 685 residues, nine ubiquitin repeats.
- [Mol* Viewer documentation](https://molstar.org/viewer-docs/) — interface, interactions on click, URL parameters.
- [Kabsch and Sander (1983)](https://doi.org/10.1002/bip.360221211) — the DSSP hydrogen-bond energy and cutoff.
- [EMBOSS iep](https://emboss.sourceforge.net/apps/cvs/emboss/apps/iep.html) — the pKa set used here.
- [Pace et al. (2014)](https://doi.org/10.1002/pro.2449) — buried hydrogen bonds stabilise proteins, by a context-dependent amount.
- [Dadarlat and Post (2008)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4927099) — most globular proteins are only marginally stable; 1–3 kcal/mol of destabilisation can contribute to disease.
