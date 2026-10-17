---
id: "31.2"
module: 31
minutes: 20
practice_minutes: 60
prerequisites: ["31.1", "15.2"]
objectives:
  - Write the terms of a molecular-mechanics force field and say what MMFF94 and UFF are and are not good for.
  - Run a relaxed dihedral scan with xtb and compare the torsion profile with a force field and with measured values.
  - Find the conformers of a flexible molecule with a stochastic search, remove duplicates, re-rank them at a better level and compute Boltzmann populations with degeneracies.
volatility: implementation
sources:
  - title: "Halgren (1996), Merck molecular force field. I. Basis, form, scope, parameterization, and performance of MMFF94, J. Comput. Chem. 17, 490"
    url: https://doi.org/10.1002/(SICI)1096-987X(199604)17:5/6%3C490::AID-JCC1%3E3.0.CO;2-P
  - title: "RDKit documentation, Getting Started in Python (conformer generation and MMFF)"
    url: https://www.rdkit.org/docs/GettingStartedInPython.html
  - title: "xtb documentation, Exploration of the potential energy surface (constrained scans)"
    url: https://xtb-docs.readthedocs.io/en/latest/scan.html
  - title: "CREST v3.0.2 release (GitHub, crest-lab/crest)"
    url: https://github.com/crest-lab/crest/releases/tag/v3.0.2
  - title: "OpenStax Organic Chemistry, 3.7 Conformations of Other Alkanes"
    url: https://openstax.org/books/organic-chemistry/pages/3-7-conformations-of-other-alkanes
last_verified: "2026-10-17"
---

# 31.2 · Molecular mechanics and conformer search

A flexible molecule is not one structure but a family of conformers, and every property you calculate later, from an IR spectrum to a reaction barrier, depends on starting from the right ones. In lesson [15.2](../module-15/lesson-02.md) you ran a force-field scan of butane. Here you look inside the force field, repeat the butane scan with the quantum-mechanical GFN2-xTB method, and run a real conformer search on n-pentane: generate many structures cheaply, throw out duplicates, re-rank the survivors with a better method and turn the energies into populations.

## Why it matters

A colleague calculates the 13C NMR spectrum of a drug-like molecule with eight rotatable bonds from the one structure she drew. The calculated shifts are off by 6 ppm at two carbons, and she starts to doubt the assignment. The problem is the structure: her drawing was a high-energy conformer, and in solution three other conformers carry 90 % of the population. Conformer searching is the first step of almost every computational study of a flexible molecule. Skipping it produces errors larger than any difference between DFT functionals, and they are the hardest to notice, because each individual calculation looks fine.

## Core ideas

> [!NOTE]
> The force-field form, Boltzmann statistics and the "funnel" strategy are stable. Program details were checked on 2026-10-17: RDKit 2026.9.1 (ETKDG and MMFF94), xtb 6.7.1 (`$constrain`/`$scan` input) and CREST 3.0.2 (Linux builds only). The numbers quoted come from runs made with those versions.

### A force field is a sum of simple terms

**Molecular mechanics** (MM) gives the energy of a molecule from its geometry with classical formulas, without electrons. Each atom gets an **atom type** (an sp³ carbon, a carbonyl oxygen, an amide nitrogen), and the energy is a sum:

$$E_\text{MM} = \sum_\text{bonds} k_b (r - r_0)^2 + \sum_\text{angles} k_\theta (\theta - \theta_0)^2 + \sum_\text{dihedrals} \sum_n \frac{V_n}{2}\left[1 + \cos(n\varphi - \gamma)\right] + E_\text{vdW} + E_\text{elec}$$

The first two terms are springs, like the harmonic oscillator of [12.4](../module-12/lesson-04.md). The torsion term is a short Fourier series in the dihedral angle φ; a threefold term ($n = 3$) gives the staggered/eclipsed pattern of ethane. The **non-bonded** terms act between atoms more than three bonds apart: van der Waals repulsion and attraction (MMFF94 uses a "buffered 14-7" form instead of Lennard-Jones) and Coulomb interactions between fixed partial charges. The force constants, reference values and charges are the **parameters**, fitted to experiments and quantum calculations.

Two force fields are built into RDKit and Avogadro:

- **MMFF94** (Merck, 1996) is parameterised carefully for organic and drug-like molecules, largely against high-level quantum calculations. It is a good default for conformers of organic molecules.
- **UFF** (Universal Force Field) has parameters for the whole periodic table, derived from simple rules. It is useful for building metal complexes or odd elements, but its conformational energies are rough.

A force field cannot break or make bonds, knows nothing about electronic structure (no aromaticity changes, no charge transfer) and is only as good as its parameters for your atom types. Lesson 15.2 showed it putting methylcyclohexane's axial–equatorial gap 2 kJ/mol too low.

### Scans: rigid and relaxed

A **scan** steps one coordinate, such as a dihedral, through a range of values. In a **rigid scan** nothing else moves. In a **relaxed scan** every other coordinate is re-optimised at each step, which is what a real molecule does. xtb runs relaxed scans with a constraint plus a scan instruction in a small input file (`xtb/butane_scan.inp` in the lab):

```text
$constrain
   force constant=1.0
   dihedral: 1,2,3,4,180.0
$scan
   1: 180.0,-180.0,37
$end
```

This holds the dihedral of atoms 1–2–3–4 (counting from 1) with a stiff spring and moves its target from 180° to −180° in 37 steps of 10°. The structures and energies go to `xtbscan.log`.

### Searching conformer space

A molecule with $n$ rotatable single bonds, each with three staggered minima, has up to $3^n$ conformers: 9 for pentane, 243 for octane, 6561 for a drug with eight rotatable bonds. There are three practical strategies:

1. **Systematic search**: step every dihedral through its minima. Exhaustive, but only feasible for a few bonds.
2. **Stochastic search**: generate many random but sensible starting structures and minimise each. RDKit's **ETKDG** method builds 3D structures from distance limits plus knowledge of preferred torsions; minimising 50–300 of them with MMFF94 usually finds the important conformers of a mid-sized molecule.
3. **Metadynamics**: run molecular dynamics while pushing the molecule away from structures it has already visited. CREST does this with GFN2-xTB and is the standard tool for serious work (release binaries for Linux only).

Whatever generates the structures, many minimisations end in the same minimum. You remove **duplicates** by comparing energies and geometry descriptors (here the backbone dihedrals; in general the RMSD of atom positions after alignment).

### The funnel and the populations

Cheap methods can rank conformers wrongly, so real studies use a **funnel**: many structures with MM, the low-energy ones re-optimised with xtb, the best few with DFT. At each stage the energy window narrows.

The fraction of molecules in conformer $i$ at temperature $T$ is the Boltzmann population

$$p_i = \frac{g_i\, e^{-\Delta E_i/RT}}{\sum_j g_j\, e^{-\Delta E_j/RT}}$$

where $g_i$ counts equivalent copies (mirror images and symmetry-related forms). For pentane, "tg" stands for four equivalent structures: the gauche twist can be at either bond and can be +60° or −60°. Strictly, populations follow Gibbs energies, which add zero-point and entropy terms from a frequency calculation; with electronic energies alone they are an approximation good to a factor of about 1.5 for alkanes.

## Worked example

### Populations of n-pentane from four conformer energies

A search on n-pentane, re-optimised with GFN2-xTB, gives these unique conformers (energies relative to the all-anti form, from this lesson's lab run):

| Conformer | Backbone dihedrals | $g$ | $\Delta E$ / kJ mol⁻¹ |
|---|---|---|---|
| tt | 180°, 180° | 1 | 0.00 |
| tg | 180°, ±60° (either bond) | 4 | 2.40 |
| g+g+ | +60°, +60° (or −60°, −60°) | 2 | 4.93 |
| g+g− | +60°, −60° | 2 | 10.16 |

At 298 K, $RT = 2.479$ kJ/mol.

1. Weights $g\,e^{-\Delta E/RT}$: tt $1 \times 1 = 1$; tg $4 \times e^{-0.968} = 4 \times 0.380 = 1.519$; g+g+ $2 \times e^{-1.989} = 0.274$; g+g− $2 \times e^{-4.098} = 0.033$.
2. Sum: $1 + 1.519 + 0.274 + 0.033 = 2.826$.
3. Populations: tt 35.4 %, tg 53.8 %, g+g+ 9.7 %, g+g− 1.2 %.

Two lessons hide in these numbers. First, the lowest-energy conformer (tt) is not the most populated form: the four equivalent tg structures together win. Forgetting $g$ would give tt 65 % instead of 35 %. Second, g+g− is high because the two terminal methyl groups collide, the "syn-pentane" interaction; MMFF94 puts it at 15.5 kJ/mol and GFN2-xTB at 10.2 kJ/mol, a reminder that methods disagree most on the crowded, high-energy structures.

## Hands-on

What you need: xtb, Python with the course packages, the [Module 31 lab folder](../../labs/module-31/), Avogadro to look at structures, and a [notebook page](../../templates/notebook-page.md). Time: about 60 minutes.

### Part A — butane relaxed scan with xtb (20 min)

1. Run the scan by hand once, from a new folder containing copies of `molecules/butane.xyz` and `xtb/butane_scan.inp`:

   ```bash
   xtb butane.xyz --opt --input butane_scan.inp > scan.out
   ```

   It takes a few seconds and writes `xtbscan.log`: 37 structures, each with its energy in the comment line.
2. Open `lesson02_conformers.py` and complete `scan_profile()`: for each frame, measure the C1–C2–C3–C4 dihedral (`comp31.dihedral`, map it to 0–360°) and convert the energy to kJ/mol relative to the lowest frame.
3. Complete `label()`, which names a dihedral t (120–240°), g+ (below 120°) or g− (above 240°). Then run `py lesson02_conformers.py`; it repeats the scan in `runs/31.2-butane-scan/` and plots `runs/lesson02_conformers.png`.

### Part B — pentane conformer search (25 min)

The same script runs the search: 60 ETKDG structures, MMFF94 minimisation, duplicates removed by naming each structure from its two backbone dihedrals, then an xtb re-optimisation of each unique conformer and Boltzmann populations with degeneracies. Open the four `runs/31.2-pentane/*/xtbopt.xyz` files in Avogadro and look at the g+g− structure from the side to see the two methyl groups meet.

How you know it worked (RDKit 2026.9.1, xtb 6.7.1, checked 2026-10-17; full printout in `expected/31.2_conformers.txt`):

| Butane, kJ/mol above anti | GFN2-xTB scan | MMFF94 scan (15.2) | OpenStax values (15.2) |
|---|---|---|---|
| gauche | 2.5 | 3.5 | 3.8 |
| eclipsed CH₃/H | 10.7 | 16.6 | 16 |
| syn | 20.7 | 21.8 | 19 |

Pentane: four unique conformers, tt 0.00 / tg 3.47 / g+g+ 5.95 / g+g− 15.48 kJ/mol with MMFF94 and 0.00 / 2.40 / 4.93 / 10.16 kJ/mol with GFN2-xTB; populations 46 / 45 / 8 / 0.2 % (MMFF94) and 35 / 54 / 10 / 1.2 % (GFN2-xTB). No conformer changes its name during the xtb re-optimisation.

<details><summary>Reference solution and interpretation</summary>

```python
def scan_profile(frames, atoms=(0, 1, 2, 3)):
    e_min = min(e for _, _, e in frames)
    pts = [(c.dihedral(x, *atoms) % 360.0, (e - e_min) * c.HARTREE_KJMOL) for _, x, e in frames]
    return sorted(pts)

def label(phi):
    phi = phi % 360.0
    if 120.0 <= phi <= 240.0:
        return "t"
    return "g+" if phi < 120.0 else "g-"
```

Full code: `lesson02_conformers_solution.py`. Reading the result: GFN2-xTB agrees with the measured gauche preference to about 1 kJ/mol but puts the CH₃/H eclipsed barrier about 5 kJ/mol too low. The same method gives 10.8 kJ/mol for ethane's barrier against the measured 12 kJ/mol (lesson [31.5](lesson-05.md)): semiempirical methods are often too soft in torsions. Use xtb to find and pre-rank conformers, not for final barriers. The force field and xtb agree on the order of the four pentane conformers, so for this molecule the funnel would keep the same three low-energy structures; with more polar molecules the order often changes.

</details>

### Part C — optional: CREST on Linux or macOS (15 min)

If you have CREST 3.0.2 (the Linux release binary, or a conda-forge build where one exists for your system), run `crest pentane.xyz --gfn2 -T 2` on `molecules/pentane.xyz`. It writes `crest_conformers.xyz`, a multi-structure file you can read with `comp31.read_multixyz`. Check that it finds the same four conformer types. CREST has no Windows build; Windows users can skip this part or use WSL.

## Common mistakes

- Calculating properties from one drawn structure of a flexible molecule. Search first, then compute each low-energy conformer and Boltzmann-average.
- Forgetting degeneracies. Count mirror images and equivalent rotations, or the populations come out wrong by factors of 2 to 4.
- Trusting a rigid scan. Without relaxation, other parts of the molecule clash and barriers come out far too high.
- Generating too few starting structures. If the number of unique conformers is still growing when you double the number of starts, you have not finished.
- Treating xtb or MMFF energies as final. Use them to find and rank candidates, then re-rank the best ones with DFT (lesson [31.3](lesson-03.md)).
- Mixing index conventions. xtb input files count atoms from 1, Python and RDKit from 0.

## Key takeaways

- A force field is springs plus torsion cosines plus van der Waals and Coulomb terms with fitted parameters; MMFF94 suits organic molecules, UFF covers the periodic table roughly.
- A relaxed scan re-optimises everything except the scanned coordinate; xtb does it with `$constrain` and `$scan`.
- Up to $3^n$ conformers for $n$ rotatable bonds: search stochastically (ETKDG + MMFF94) or with metadynamics (CREST), then remove duplicates.
- Use a funnel: many structures cheaply, fewer with xtb, the best with DFT.
- Populations need degeneracies: $p_i \propto g_i e^{-\Delta E_i/RT}$; the lowest conformer is not always the most populated one.

## Sources

- [Halgren (1996), MMFF94 I, J. Comput. Chem. 17, 490](https://doi.org/10.1002/(SICI)1096-987X(199604)17:5/6%3C490::AID-JCC1%3E3.0.CO;2-P) — form and parameterisation of MMFF94, including the buffered 14-7 van der Waals term.
- [RDKit, Getting Started in Python](https://www.rdkit.org/docs/GettingStartedInPython.html) — ETKDG conformer embedding and MMFF optimisation used in the lab.
- [xtb documentation, Exploration of the potential energy surface](https://xtb-docs.readthedocs.io/en/latest/scan.html) — `$constrain` and `$scan` input; scans in xtb are always relaxed.
- [CREST v3.0.2 release](https://github.com/crest-lab/crest/releases/tag/v3.0.2) — current release (2024-08-25), Linux builds.
- [OpenStax Organic Chemistry, 3.7 Conformations of Other Alkanes](https://openstax.org/books/organic-chemistry/pages/3-7-conformations-of-other-alkanes) — measured butane conformer energies used in 15.2.
