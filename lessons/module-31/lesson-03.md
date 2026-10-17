---
id: "31.3"
module: 31
minutes: 22
practice_minutes: 60
prerequisites: ["31.1", "12.6"]
objectives:
  - Explain what Hartree–Fock leaves out and how density functional theory puts electron correlation back in, and place common functionals on the rungs of Jacob's ladder.
  - Choose a basis set and read the effect of basis size on energy and geometry from a series of calculations.
  - Optimise water with HF and B3LYP in two basis sets, compare bond length and angle with experiment, and explain the pattern of errors.
  - Prove that an optimised structure is a minimum with a frequency calculation, and repair a false minimum.
volatility: implementation
sources:
  - title: "ORCA 6.1 manual, 3.6 Composite methods (r2SCAN-3c)"
    url: https://www.faccts.de/docs/orca/6.1/manual/contents/modelchemistries/3cmethods.html
  - title: "ORCA 6.1 manual, 2.1 General structure of the input file"
    url: https://www.faccts.de/docs/orca/6.1/manual/contents/essentialelements/input.html
  - title: "Grimme, Hansen, Ehlert and Mewes (2021), r2SCAN-3c: a Swiss army knife composite electronic-structure method, J. Chem. Phys. 154, 064103"
    url: https://doi.org/10.1063/5.0040021
  - title: "NIST CCCBDB, experimental data for water (geometry and vibrations)"
    url: https://cccbdb.nist.gov/exp2x.asp?casno=7732185&charge=0
  - title: "PySCF (open-source quantum chemistry in Python), used for the reference values"
    url: https://pyscf.org/
last_verified: "2026-10-17"
---

# 31.3 · Hartree-Fock and DFT: geometry optimisation

The calculations behind almost every modern structure, spectrum and mechanism paper are Hartree–Fock and, far more often, density functional theory. This lesson explains in plain terms what each method approximates, what a basis set is and how to pick one, and how to optimise a geometry you can trust. You will optimise water four ways in ORCA, compare the results with experiment and with reference values, and catch a structure that every optimiser reported as converged but that is not a minimum.

## Why it matters

A paper reports a new catalyst and its key intermediate, optimised with B3LYP in a small basis set. The reviewer asks two things: does a larger basis change the key distance, and did the authors check the frequencies? Both questions are about this lesson. Bond lengths change by 0.01 Å from one basis to the next, which is enough to change which hydrogen bond forms, and an unchecked "minimum" can be a saddle point that falls apart when you push it. A chemist who can choose a method and basis, and prove a structure is a minimum, can both write and review such work.

## Core ideas

> [!NOTE]
> Hartree–Fock, Kohn–Sham DFT, Jacob's ladder and basis-set convergence are stable theory. Program specifics were checked on 2026-10-17 against the ORCA 6.1 manual (keywords `HF`, `B3LYP`, `r2SCAN-3c`, `def2-SVP`, `def2-TZVP`, `TightOpt`, `Freq`). The reference numbers in the lab were computed with PySCF 2.14.0 because ORCA was not run when this lesson was written; ORCA with the same method and basis should agree to about 0.002 Å and 0.3°.

### Hartree–Fock: one electron at a time

**Hartree–Fock** (HF) treats each electron as moving in the average field of all the others. The wavefunction is a single antisymmetrised product of orbitals (a Slater determinant), and the variational principle of [12.6](../module-12/lesson-06.md) picks the best orbitals. Because each orbital depends on the field made by all the others, the equations are solved by the self-consistent field loop from [31.1](lesson-01.md).

What HF misses is **electron correlation**: electrons dodge each other more cleverly than an average field allows. The missing energy is small in relative terms (under 1 % of the total) but large chemically, hundreds of kJ/mol for a medium molecule. Its typical symptoms are bonds slightly too short, vibrational frequencies about 10 % too high, and no dispersion (London) attraction at all. Methods that add correlation on top of HF (MP2, coupled cluster CCSD(T)) are accurate but cost $N^5$ to $N^7$.

### DFT: get correlation from the density

**Density functional theory** (DFT) rests on a theorem (Hohenberg and Kohn, 1964): the ground-state energy is a functional of the electron density alone. In practice (Kohn–Sham DFT) the program still uses orbitals and an SCF loop, but adds an **exchange–correlation functional**, an approximate formula that turns the density into the exchange and correlation energy. The exact functional is unknown, so there are hundreds of approximations, arranged on "Jacob's ladder" by the ingredients they use:

| Rung | Ingredients | Examples |
|---|---|---|
| LDA | density | SVWN (historical) |
| GGA | + density gradient | PBE, BLYP |
| meta-GGA | + kinetic-energy density | TPSS, r2SCAN |
| hybrid | + a fraction of HF exchange | B3LYP (20 %), PBE0 (25 %) |
| range-separated hybrid | HF exchange growing with distance | CAM-B3LYP, ωB97X-D3 |
| double hybrid | + MP2-like correlation | B2PLYP |

Higher rungs are usually more accurate and more expensive, but not always better for every property. Most functionals also miss dispersion, so modern practice adds an empirical **dispersion correction** such as D3 or D4.

### Basis sets

A **basis set** is the set of atom-centred functions from which the program builds the orbitals. More functions give more flexible orbitals and, for variational methods, a lower energy. Names describe the size:

- **def2-SVP** (split valence plus polarisation): two functions per valence orbital plus one set of polarisation functions (d on O, p on H). Fast; good for first geometries.
- **def2-TZVP** (triple zeta): three per valence orbital and more polarisation. The usual choice for final geometries and energies.
- **diffuse** functions (def2-SVPD, aug-cc-pVDZ) are spread out and are needed for anions, excited states and weak interactions.

The basis error and the method error are separate. A cheap method in a huge basis is still a cheap method, and a good functional in a tiny basis can be badly wrong.

### Composite "3c" methods

**r2SCAN-3c** combines the r2SCAN meta-GGA functional with a purpose-built triple-zeta basis, the D4 dispersion correction and a correction for basis-set superposition error, all with fixed settings. It costs about as much as a GGA in a triple-zeta basis and for geometries and thermochemistry often matches hybrid functionals in larger basis sets. In ORCA it is one keyword, `! r2SCAN-3c`, which is why the module uses it as the default "good" method.

### An optimisation is finished only when frequencies say so

An optimiser stops when the gradient and the energy change fall below thresholds. That happens at any stationary point: a minimum, a saddle point, even a point where a soft rotation is nearly flat. Only the Hessian distinguishes them ([28.1](../module-28/lesson-01.md)). So every structure you report needs a frequency calculation at the same level: zero imaginary frequencies for a minimum. If you find one, displace the structure along that mode and optimise again, with tighter thresholds if the mode is soft.

## Worked example

### Reading a method-and-basis table for water

The table holds optimised water geometries and total energies (reference values computed for this course with PySCF 2.14; your ORCA runs should match within about 0.002 Å and 0.3°). Experiment: $r_e$ = 0.958 Å, angle 104.48° (CCCBDB).

| Level | r(O–H) / Å | angle / ° | E / Eh |
|---|---|---|---|
| HF/def2-SVP | 0.9450 | 105.13 | −75.961338 |
| HF/def2-TZVP | 0.9420 | 106.51 | −76.059579 |
| B3LYP/def2-SVP | 0.9667 | 103.10 | −76.358316 |
| B3LYP/def2-TZVP | 0.9627 | 105.24 | −76.462996 |
| GFN2-xTB | 0.9592 | 107.30 | −5.070544 |

1. Method error, HF: the bond is too short by $0.942 - 0.958 = -0.016$ Å in the larger basis, −1.7 %. Enlarging the basis makes it slightly worse, which tells you the error is in the method (no correlation), not the basis. As the basis grows, HF tends to a fixed answer, the "HF limit", and that limit itself has bonds that are too short.
2. Method error, B3LYP: +0.0047 Å in def2-TZVP, +0.5 %. Correlation lengthens the bond; B3LYP overshoots slightly.
3. Basis error, B3LYP: going from def2-SVP to def2-TZVP changes the bond by −0.004 Å and the angle by +2.1°. The angle is the more basis-sensitive quantity: def2-SVP is too small to describe the oxygen lone pairs fully.
4. Energies: in each method the larger basis gives the lower energy (HF by 0.098 Eh, B3LYP by 0.105 Eh, about 260–275 kJ/mol), as the variational principle requires. That number is not chemically meaningful by itself; only differences between molecules at one level are.
5. GFN2-xTB gets the bond length right but the angle 2.8° too wide. It is parameterised for many elements and many properties, so small-molecule angles are not its strength.

Conclusion for practice: use at least a triple-zeta basis for final geometries, a correlated method (DFT with dispersion, or r2SCAN-3c) rather than HF, and expect bond lengths good to about 0.01 Å and angles to about 1°.

## Hands-on

What you need: ORCA 6.1.1 and xtb, Python with the course packages, the [Module 31 lab folder](../../labs/module-31/) and a [notebook page](../../templates/notebook-page.md). Time: about 60 minutes.

### Part A — water four ways in ORCA (25 min)

1. In `orca/` run the four inputs, each under a minute:

   ```bash
   orca 03_water_hf_svp.inp > 03_water_hf_svp.out
   orca 03_water_hf_tzvp.inp > 03_water_hf_tzvp.out
   orca 03_water_b3lyp_svp.inp > 03_water_b3lyp_svp.out
   orca 03_water_b3lyp_tzvp.inp > 03_water_b3lyp_tzvp.out
   ```

2. For each, check termination, convergence and zero imaginary frequencies, as in 31.1. Note the `FINAL SINGLE POINT ENERGY` and the time (`TOTAL RUN TIME` at the end).
3. ORCA writes each final geometry to an `.xyz` file with the same base name. Open `lesson03_geometry.py`, complete `water_geometry()` (mean O–H distance and the H–O–H angle; atom 0 is oxygen) and `n_imaginary()`, then run `py lesson03_geometry.py`. It optimises water with xtb, reads every `orca/03_water_*.xyz` it finds and prints them next to the reference table.

How you know it worked: your ORCA rows agree with the reference rows above to within about 0.002 Å and 0.3°; total energies may differ in the third decimal (integration grids and the exact B3LYP definition differ between programs). The xtb tight optimisation gives 0.9593 Å and 107.22°. The ORCA inputs were not run when this lesson was written; the reference rows are PySCF results for the same method and basis.

### Part B — a converged optimisation that is not a minimum (20 min)

The same script optimises acetone from the MMFF94 start geometry in `molecules/acetone.xyz` with `xtb --ohess`. The optimiser reports convergence, but the frequency check finds one imaginary mode: the start structure had a methyl group twisted near the top of its rotation barrier, and the default thresholds let the optimiser stop on that flat saddle. The script then restarts from `xtbhess.xyz` (the structure pushed along the imaginary mode, which xtb writes for you) with tighter thresholds.

How you know it worked (xtb 6.7.1, checked 2026-10-17; printout in `expected/31.3_geometry.txt`):

- first try: E = −13.534140 Eh, lowest mode −62.4 cm⁻¹, one imaginary frequency;
- restart: E = −13.534178 Eh, lowest mode 71.8 cm⁻¹, no imaginary frequencies;
- energy gained: 0.10 kJ/mol.

Optional: `orca/03_acetone_xtb2_check.inp` repeats the check through ORCA's own xtb (`! XTB2 Opt NumFreq`).

<details><summary>Reference solution and questions</summary>

```python
def water_geometry(x):
    r = (c.distance(x, 0, 1) + c.distance(x, 0, 2)) / 2.0
    return r, c.angle(x, 1, 0, 2)

def n_imaginary(modes, cutoff=-10.0):
    return sum(1 for w, *_ in modes if w < cutoff)
```

Full code: `lesson03_geometry_solution.py`.

1. Why use a cutoff of −10 cm⁻¹ rather than 0? Numerical noise produces tiny negative values (a few cm⁻¹) for nearly free motions; a real imaginary mode is usually tens or hundreds of cm⁻¹.
2. The acetone energy changed by only 0.10 kJ/mol. Does the fix matter? Yes, for anything computed from the Hessian: the imaginary mode would be dropped from the zero-point energy and from the entropy, and the frequency list would have one mode missing. For larger molecules the energy difference can be several kJ/mol.
3. Which water level would you choose for a 30-atom molecule? r2SCAN-3c or B3LYP-D4/def2-TZVP for the final geometry, after an xtb pre-optimisation.

</details>

## Common mistakes

- Reporting an optimised structure without a frequency check. Convergence only means a stationary point.
- Using HF for geometries or energies of real problems. It lacks correlation and dispersion; use DFT with a dispersion correction or a 3c method.
- Using a minimal or double-zeta basis for final numbers. Use def2-SVP to explore and def2-TZVP (or r2SCAN-3c) to finish.
- Leaving out diffuse functions for anions. An anion's extra electron is spread out; without diffuse functions its energy and geometry are poor.
- Changing two things at once. If you change functional and basis together, you cannot tell which change moved the result.
- Restarting from scratch after a false minimum. Displace along the imaginary mode (xtb writes `xtbhess.xyz`; in ORCA, follow the mode with Avogadro or restart from a displaced geometry) and tighten the thresholds.

## Key takeaways

- HF is the mean-field method: no correlation, bonds too short, frequencies about 10 % high, no dispersion.
- DFT adds correlation through an approximate exchange–correlation functional; climb Jacob's ladder from GGA to hybrids and add D3/D4 dispersion.
- Bigger basis, lower variational energy; final geometries need at least triple zeta; anions and excited states need diffuse functions.
- r2SCAN-3c is a cheap, robust default for geometries of ordinary molecules.
- Optimised does not mean minimum: check frequencies, and fix an imaginary mode by displacing along it and re-optimising more tightly.

## Sources

- [ORCA 6.1 manual, Composite methods](https://www.faccts.de/docs/orca/6.1/manual/contents/modelchemistries/3cmethods.html) — r2SCAN-3c and the other 3c methods as single keywords.
- [ORCA 6.1 manual, Structure of the input file](https://www.faccts.de/docs/orca/6.1/manual/contents/essentialelements/input.html) — `!` keyword lines, `%` blocks and `* xyzfile` coordinates.
- [Grimme et al. (2021), r2SCAN-3c, J. Chem. Phys. 154, 064103](https://doi.org/10.1063/5.0040021) — composition and benchmark accuracy of r2SCAN-3c.
- [NIST CCCBDB, water](https://cccbdb.nist.gov/exp2x.asp?casno=7732185&charge=0) — experimental $r_e$ = 0.958 Å and angle 104.48°.
- [PySCF](https://pyscf.org/) — open-source program (version 2.14.0, with geomeTRIC 1.1.1) used to compute the reference rows of `reference_water.csv`.
