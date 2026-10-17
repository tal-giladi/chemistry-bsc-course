---
id: "31.5"
module: 31
minutes: 22
practice_minutes: 60
prerequisites: ["31.3", "28.1", "22.4", "12.3"]
objectives:
  - Build a transition-state guess, optimise it to a first-order saddle point and prove it with exactly one imaginary frequency whose motion is the reaction.
  - Compute an electronic barrier, correct it for zero-point energy and convert it into a rate constant with the Eyring equation.
  - Compare calculated barriers for ammonia inversion and ethane rotation with measured values and explain the role of tunnelling.
  - Choose between a symmetric guess, a relaxed scan and a nudged-elastic-band search for a new reaction.
volatility: implementation
sources:
  - title: "ORCA 6.1 manual, 4.3 Transition state searches (OptTS, Calc_Hess, TS_Mode, ScanTS)"
    url: https://www.faccts.de/docs/orca/6.1/manual/contents/structurereactivity/optimizations_TS.html
  - title: "ORCA 6.1 manual, Nudged elastic band and NEB-TS"
    url: https://www.faccts.de/docs/orca/6.1/manual/contents/structurereactivity/neb.html
  - title: "Al Derzi, Furtenbacher, Tennyson, Yurchenko and Császár (2015), MARVEL analysis of the measured high-resolution spectra of 14NH3, J. Quant. Spectrosc. Radiat. Transf. 161, 117"
    url: https://doi.org/10.1016/j.jqsrt.2015.03.034
  - title: "OpenStax Organic Chemistry, 3.6 Conformations of Ethane"
    url: https://openstax.org/books/organic-chemistry/pages/3-6-conformations-of-ethane
  - title: "NIST CODATA fundamental physical constants"
    url: https://physics.nist.gov/cuu/Constants/
last_verified: "2026-10-17"
---

# 31.5 · Transition states and reaction barriers

In [28.1](../module-28/lesson-01.md) you found the passes of a model energy landscape with Python. Real molecules have landscapes in dozens of dimensions, and finding the pass is the hardest routine job in computational chemistry. This lesson shows the standard workflow: make a good guess, optimise uphill along one direction and downhill along all others, prove the result with a frequency calculation, and only then turn the barrier into a rate with the Eyring equation of [22.4](../module-22/lesson-04.md). You will compute two textbook barriers, ammonia's umbrella inversion and ethane's rotation, and compare them with experiment.

## Why it matters

A process chemist must decide whether a reaction step can be run at 25 °C or needs 80 °C, and whether a side reaction will compete. A calculated barrier answers this before anyone orders reagents, but only if the "transition state" really is one. A common failure in student work, and in published work, is a structure called a transition state that has two imaginary frequencies, or one that belongs to a different motion, such as a methyl rotation rather than the bond being broken. The barrier then refers to a different process, and the predicted rate can be wrong by many orders of magnitude, since every 5.7 kJ/mol is a factor of 10 at room temperature.

## Core ideas

> [!NOTE]
> Saddle points, Eyring theory and zero-point corrections are stable theory. Software details were checked on 2026-10-17 against the ORCA 6.1 manual (`OptTS`, `%geom Calc_Hess`, `NEB-TS`, `NEB_End_XYZFile`) and xtb 6.7.1. Barrier values in the lab were computed with xtb 6.7.1; the measured ammonia barrier is the effective value summarised in 2015, and the ethane value is the textbook one used in lesson 15.2.

### What you are looking for

A **transition state** (TS) is a first-order saddle point on the potential energy surface: the gradient is zero, the Hessian has exactly one negative eigenvalue, and therefore the frequency calculation shows exactly **one imaginary frequency**. Its **normal mode**, animated in Avogadro, must look like the reaction: atoms moving from reactant towards product. A frequency calculation is not optional here. It is the definition.

### Step 1: a good guess

Transition-state optimisers only work close to the saddle. Three ways to get there:

1. **Symmetry.** Some transition states have higher symmetry than the minima. Planar ammonia ($D_{3h}$) sits between two pyramids; eclipsed ethane ($D_{3h}$) between two staggered forms. Because the gradient along the symmetry-breaking reaction mode is exactly zero in a symmetric structure, an ordinary optimisation that keeps the symmetry stops on the saddle.
2. **Relaxed scan.** Scan the coordinate that changes most (a forming bond, a dihedral) as in [31.2](lesson-02.md) and take the highest point. ORCA's `! ScanTS` does the scan and starts the TS search from the maximum in one job.
3. **Nudged elastic band (NEB).** Give the optimised reactant and product, let the program build a chain of intermediate structures ("images") and relax the chain towards the minimum-energy path. The highest image is the TS guess; ORCA's `! NEB-TS` refines it automatically.

### Step 2: optimise to the saddle

A TS optimiser (ORCA `! OptTS`) uses the Hessian to go uphill along the one mode with negative curvature and downhill along all the others. It needs a good starting Hessian: `%geom Calc_Hess true end` computes the exact one before the first step, and `TS_Mode` lets you choose which mode to follow if the lowest one is the wrong motion. An ordinary minimiser cannot find a saddle except in the symmetric case above, because it only goes downhill.

### Step 3: prove it

1. Frequency calculation at the same level: exactly one imaginary frequency.
2. Animate it: the motion connects the intended reactant and product.
3. For a new reaction, run an **intrinsic reaction coordinate** (IRC) calculation (`! IRC` in ORCA): it follows the steepest-descent path down both sides of the saddle, the minimum-energy path of 28.1, and shows which minima the TS connects.

### From energies to a rate

The **electronic barrier** is $\Delta E^\ddagger = E_\text{TS} - E_\text{min}$. Each structure also has a harmonic **zero-point energy** (ZPE), half the sum of its real vibrational wavenumbers:

$$E_\text{ZPE} = \tfrac{1}{2} \sum_i h c\,\tilde\nu_i$$

The TS has one real mode fewer (the reaction mode became imaginary), so its ZPE is usually lower and the ZPE-corrected barrier $\Delta E_0^\ddagger$ smaller. A full frequency job also prints enthalpy and Gibbs-energy corrections, which give $\Delta^\ddagger G$ at 298 K for the Eyring equation:

$$k = \frac{k_BT}{h}\, e^{-\Delta^\ddagger G/RT}, \qquad \frac{k_BT}{h} = 6.21\times10^{12}\ \text{s}^{-1}\ \text{at 298 K}$$

For a conformational change without big entropy differences, $\Delta E_0^\ddagger$ is a reasonable stand-in for $\Delta^\ddagger G$.

### When transition-state theory fails: tunnelling

Eyring's equation counts molecules going over the pass. Light atoms can also go through it ([12.3](../module-12/lesson-03.md)). Ammonia is the extreme case: even in the vibrational ground state, far below the top of the barrier, the two pyramids are mixed by tunnelling, and the measured inversion splitting is 23.79 GHz. A molecule prepared in one pyramid reaches the other after about $1/(2 \times 23.79\ \text{GHz}) = 21$ ps, a rate of about $5\times10^{10}$ s⁻¹. Hydrogen-transfer reactions often run several times faster than the calculated over-the-barrier rate for the same reason.

## Worked example

### Ammonia inversion from two xtb calculations

GFN2-xTB (this lesson's lab run) gives:

| Structure | E / Eh | Real wavenumbers / cm⁻¹ | Imaginary |
|---|---|---|---|
| pyramidal NH₃ (minimum) | −4.426244 | 1159, 1593, 1593, 3426, 3478, 3478 | none |
| planar NH₃ (TS) | −4.416506 | 1461, 1461, 3621, 3732, 3732 | 975i |

1. Check: the minimum has no imaginary mode; the planar structure has exactly one, and its animation is the umbrella motion. Both pass.
2. Electronic barrier: $(-4.416506 + 4.426244) \times 2625.5 = 0.009738 \times 2625.5 = 25.6$ kJ/mol.
3. ZPE: minimum $\tfrac12 \times 14\,727$ cm⁻¹ $= 7364$ cm⁻¹ $= 88.1$ kJ/mol (1 cm⁻¹ = 0.011963 kJ/mol); TS $\tfrac12 \times 14\,008$ cm⁻¹ $= 7004$ cm⁻¹ $= 83.8$ kJ/mol. The ZPE change is −4.3 kJ/mol, so $\Delta E_0^\ddagger = 21.3$ kJ/mol.
4. Eyring at 298 K: $k = 6.21\times10^{12} \times e^{-21\,300/2479} = 6.21\times10^{12} \times 1.86\times10^{-4} = 1.2\times10^9$ s⁻¹.
5. Compare: the measured effective barrier is about 24.2 kJ/mol (2021 ± 20 cm⁻¹). How zero-point energy is counted differs between analyses, so agreement within about 3 kJ/mol is as much as one can ask; GFN2-xTB does well here. The rate is another matter: tunnelling makes the real inversion about $5\times10^{10}$ s⁻¹, some 40 times faster than the over-the-barrier estimate.

## Hands-on

What you need: xtb and ORCA, Python with the course packages, Avogadro, the [Module 31 lab folder](../../labs/module-31/) and a [notebook page](../../templates/notebook-page.md). Time: about 60 minutes.

### Part A — two barriers with xtb (20 min)

1. Open `lesson05_barriers.py` and complete `n_imaginary()`, `zpe_kj()` (half the sum of the real wavenumbers, converted with 1 cm⁻¹ = 0.01196266 kJ/mol) and `barrier_kj()`.
2. Run `py lesson05_barriers.py`. For each system it optimises the minimum with `--ohess`, optimises the symmetric TS guess (`molecules/ammonia_planar.xyz`, `molecules/ethane_eclipsed.xyz`) with a plain `--opt`, which stays on the saddle by symmetry, and checks it with `--hess`.
3. Open `runs/31.5-barriers/ammonia-inversion/ts/xtbopt.xyz` in Avogadro to see the planar structure.

How you know it worked (xtb 6.7.1, checked 2026-10-17; printout in `expected/31.5_barriers.txt`):

| | imaginary mode | ΔE‡ | ΔE₀‡ | k(298 K) | measured |
|---|---|---|---|---|---|
| NH₃ inversion | 975i cm⁻¹ | 25.6 kJ/mol | 21.3 kJ/mol | 1.2 × 10⁹ s⁻¹ | about 24.2 kJ/mol |
| ethane rotation | 293i cm⁻¹ | 10.8 kJ/mol | 10.0 kJ/mol | 1.1 × 10¹¹ s⁻¹ | 12 kJ/mol |

### Part B — a real TS optimisation in ORCA (25 min)

1. In `orca/` run `05_nh3_min.inp` (pyramidal ammonia, r2SCAN-3c, TightOpt + Freq) and `05_nh3_ts.inp` (`! r2SCAN-3c OptTS Freq` with `Calc_Hess true`, started from the planar guess). Each takes about a minute.
2. Check the TS output: `THE OPTIMIZATION HAS CONVERGED`, then in `VIBRATIONAL FREQUENCIES` exactly one negative value (ORCA marks it as imaginary). Open the output in Avogadro and animate that mode: the nitrogen should move through the plane of the hydrogens.
3. Rerun `py lesson05_barriers.py`; it adds an r2SCAN-3c row from your two outputs. Record the barrier next to the xtb value and the measured 24.2 kJ/mol.

These ORCA inputs were not run when the module was written, so there is no reference row; what must hold is one imaginary frequency for the TS, none for the minimum, and a barrier of the same size as the xtb and measured values.

### Part C — optional: a TS without symmetry (15 min)

`orca/05_hcn_hnc_nebts.inp` runs a nudged-elastic-band search plus TS optimisation (`! XTB2 NEB-TS Freq`, eight images) for the hydrogen shift HCN → HNC, with ORCA's built-in GFN2-xTB. The two end structures in `molecules/` list the atoms in the same order, which NEB requires. Check the result the same way: one imaginary frequency, and an animation that moves H from C to N. This input was not run when the module was written.

<details><summary>Reference solution and interpretation</summary>

```python
def n_imaginary(wavenumbers, cutoff=-10.0):
    return sum(1 for w in wavenumbers if w < cutoff)

def zpe_kj(wavenumbers):
    return 0.5 * sum(w for w in wavenumbers if w > 0) * CM1_KJMOL

def barrier_kj(e_ts, e_min):
    return (e_ts - e_min) * c.HARTREE_KJMOL
```

Full code: `lesson05_barriers_solution.py`.

1. Why must the ZPE sum skip the imaginary mode? It is not a vibration: along it the structure falls apart towards reactant or product, so it holds no zero-point energy.
2. Ethane's barrier is 10.8 kJ/mol with GFN2-xTB against 12 kJ/mol measured, the same "too soft torsion" you saw for butane in 31.2. For final torsion barriers use DFT.
3. The ethane rate, about 10¹¹ s⁻¹, means one jump between staggered forms every 10 ps or so: at room temperature ethane rotates almost freely, and its conformers can never be separated (compare the 80–120 kJ/mol barriers of 28.1).

</details>

## Common mistakes

- Calling a structure a TS without a frequency calculation, or accepting two imaginary frequencies. Exactly one, and it must be the reaction motion.
- Trying to find a TS with a minimiser from an unsymmetric guess. It slides down to a minimum; use OptTS, ScanTS or NEB-TS.
- Following the wrong mode. If the lowest Hessian mode is a methyl rotation, set `TS_Mode` to the bond or angle that changes in the reaction.
- Mixing levels: reactant at one level, TS at another. Barrier = difference at one model chemistry.
- Including the imaginary mode in the zero-point energy, or dropping the ZPE altogether when comparing with experiment.
- Trusting Eyring rates for hydrogen transfer or inversion at low temperature without considering tunnelling.

## Key takeaways

- A transition state is a first-order saddle point: exactly one imaginary frequency whose motion is the reaction.
- Get a guess from symmetry, a relaxed scan or NEB; optimise with a TS optimiser and an exact starting Hessian; confirm with frequencies and, for new reactions, an IRC.
- Barrier = $E_\text{TS} - E_\text{min}$ at one level; correct for ZPE (and thermal terms) before using $k = (k_BT/h)e^{-\Delta^\ddagger G/RT}$.
- GFN2-xTB gives ammonia inversion well (25.6 kJ/mol, 21.3 with ZPE, against about 24) and ethane rotation a little low (10.8 against 12).
- Tunnelling can make light-atom processes far faster than transition-state theory predicts: ammonia inverts about 40 times faster than the Eyring estimate.

## Sources

- [ORCA 6.1 manual, Transition state searches](https://www.faccts.de/docs/orca/6.1/manual/contents/structurereactivity/optimizations_TS.html) — OptTS, `Calc_Hess`, `TS_Mode`, ScanTS and the one-imaginary-frequency check.
- [ORCA 6.1 manual, NEB and NEB-TS](https://www.faccts.de/docs/orca/6.1/manual/contents/structurereactivity/neb.html) — `NEB_End_XYZFile`, `NImages` (default 8) and GFN2-xTB path options.
- [Al Derzi et al., J. Quant. Spectrosc. Radiat. Transf. 161, 117 (2015)](https://doi.org/10.1016/j.jqsrt.2015.03.034) — effective inversion barrier of NH₃, 2021 ± 20 cm⁻¹, and how relativistic, Born–Oppenheimer and zero-point terms enter it.
- [OpenStax Organic Chemistry, 3.6 Conformations of Ethane](https://openstax.org/books/organic-chemistry/pages/3-6-conformations-of-ethane) — ethane rotation barrier 12 kJ/mol.
- [NIST CODATA constants](https://physics.nist.gov/cuu/Constants/) — $k_B$, $h$, $c$ and $N_A$ for the Eyring prefactor and the cm⁻¹ to kJ/mol conversion.
