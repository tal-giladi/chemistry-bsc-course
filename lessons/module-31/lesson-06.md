---
id: "31.6"
module: 31
minutes: 20
practice_minutes: 120
prerequisites: ["31.4", "31.5", "20.4", "12.2"]
objectives:
  - Explain what a TD-DFT calculation returns (vertical excitation energies and oscillator strengths) and how it relates to a measured absorption band.
  - Choose a functional, basis set and number of states for a TD-DFT job and recognise dark states, charge-transfer problems and missing diffuse functions.
  - Compare calculated excitations of a homologous series with measured absorption maxima and judge which part of the error is systematic.
  - Carry out the module practical - calculated versus measured IR for six molecules - with mode matching, a fitted scale factor and a lab report.
volatility: implementation
sources:
  - title: "ORCA 6.1 manual, 5.6 Excited states via RPA, CIS, TD-DFT and SF-TDA"
    url: https://www.faccts.de/docs/orca/6.1/manual/contents/spectroscopyproperties/tddft.html
  - title: "Yanai, Tew and Handy (2004), A new hybrid exchange-correlation functional using the Coulomb-attenuating method (CAM-B3LYP), Chem. Phys. Lett. 393, 51"
    url: https://doi.org/10.1016/j.cplett.2004.06.011
  - title: "OpenStax Organic Chemistry, 14.8 Interpreting Ultraviolet Spectra: The Effect of Conjugation"
    url: https://openstax.org/books/organic-chemistry/pages/14-8-interpreting-ultraviolet-spectra-the-effect-of-conjugation
  - title: "NIST CCCBDB, experimental vibrational frequencies (module practical data)"
    url: https://cccbdb.nist.gov/exp2x.asp?casno=7732185&charge=0
  - title: "PySCF (open-source quantum chemistry in Python), used for the reference excitation energies"
    url: https://pyscf.org/
last_verified: "2026-10-17"
---

# 31.6 · Excited states with time-dependent DFT

Colour, photochemistry, solar cells and fluorescent labels all depend on excited states, and the everyday tool for calculating them is time-dependent DFT. This lesson explains what a TD-DFT job gives you, how it connects to the absorption band you would measure, and which choices make the numbers trustworthy or misleading. You will calculate the bright state of three conjugated polyenes and the dark n→π* state of formaldehyde. The second half of the lesson is the module practical: a full comparison of calculated and measured IR spectra for six molecules, written up as a lab report.

## Why it matters

A materials chemist wants a dye that absorbs at 450 nm and has ten candidate structures. Synthesising all ten takes months; ten TD-DFT jobs take an afternoon. The calculations will not land on 450 nm exactly, but if the method's error is systematic, the ranking and the size of each shift are reliable, and two or three candidates go to the lab. The same job can mislead badly: a global hybrid functional can put a charge-transfer state far too low, and a basis without diffuse functions can push states up by tenths of an eV. Knowing which errors are systematic and which are not is what makes the afternoon useful.

## Core ideas

> [!NOTE]
> Vertical excitations, oscillator strengths and the Franck–Condon picture are stable. Software details were checked on 2026-10-17 against the ORCA 6.1 manual: `%tddft NRoots … end`, the Tamm–Dancoff approximation (TDA) as ORCA's default for TD-DFT (`TDA false` turns it off), and the absorption table layout introduced in ORCA 6.0. Reference excitation energies in the lab were computed with PySCF 2.14.0 because ORCA was not run when this lesson was written.

### What TD-DFT calculates

TD-DFT asks how the ground-state density of [31.3](lesson-03.md) responds to a weak oscillating electric field, such as light. The response has peaks at the **excitation energies** of the molecule. For each excited state the program reports:

- the **vertical excitation energy**: the energy to jump to the excited state without moving the nuclei, in eV (with cm⁻¹ and nm alongside);
- the **oscillator strength** $f$: a dimensionless intensity, proportional to the square of the transition dipole moment. $f$ near 1 is a strong band; $f$ near 0 is a **dark state** (forbidden or nearly forbidden, [12.6](../module-12/lesson-06.md));
- the orbitals involved, for example HOMO → LUMO, which tell you whether a state is π→π*, n→π* or charge transfer.

Convert with $\lambda/\text{nm} = 1239.84/(E/\text{eV})$. A state at 5.00 eV absorbs at 248 nm.

### Vertical energies and measured bands

By the Franck–Condon principle ([20.4](../module-20/lesson-04.md)) absorption happens at the ground-state geometry, so the vertical energy belongs near the band maximum. It is not the same thing: the band maximum also depends on the vibrational structure, on the solvent and on temperature, and the 0–0 transition lies lower than both. Measured $\lambda_\text{max}$ values for polyenes are solution values; calculations here are for isolated molecules. Expect a few tenths of an eV of systematic difference before any method error.

### Choosing the functional and basis

- **Global hybrids** (B3LYP, PBE0) are good for local valence states but put **charge-transfer** states (an electron moving from one end of a molecule to the other) far too low.
- **Range-separated hybrids** (CAM-B3LYP, ωB97X-D3) switch to full exact exchange at long range, which fixes charge-transfer and improves Rydberg-like states. For valence π→π* states of polyenes they tend to give higher energies than B3LYP.
- **Basis**: def2-SVP is enough for a first look at valence states; diffuse functions (def2-SVPD, def2-TZVPD) are needed for anions, Rydberg states and accurate absolute energies.
- **TDA versus full TD-DFT**: TDA is cheaper and more robust, and it is ORCA's default. For bright π→π* states of conjugated molecules it gives clearly higher energies and larger oscillator strengths than full TD-DFT: by 0.4–0.5 eV for the polyenes in this lesson. Switch it off (`TDA false`) for such states.
- **Number of roots**: ask for more states than you need (`NRoots 5` to `10`). The bright state is often not the lowest one.

Typical accuracy for valence excitations of organic molecules with a well-chosen functional is a few tenths of an eV. That sounds large, but at 250 nm 0.3 eV is about 30 nm, and a systematic shift across a series cancels when you compare members of the series.

### Conjugation and the particle in a box

In [12.2](../module-12/lesson-02.md) the π electrons of a conjugated chain behaved like particles in a box, and a longer box gave a smaller HOMO–LUMO gap. Polyenes follow the trend: measured $\lambda_\text{max}$ is 217 nm for 1,3-butadiene, 258 nm for 1,3,5-hexatriene and 290 nm for 1,3,5,7-octatetraene. The steps shrink (41 nm, then 32 nm) because real polyenes alternate between short double and long single bonds, which the simple box ignores. TD-DFT includes that alternation through the geometry and reproduces the shrinking steps, though not their exact size.

## Worked example

### Three polyenes, three settings

The reference calculations for this lesson (PySCF 2.14, def2-SVP, GFN2-xTB geometries, `polyenes_uv.csv`) give the brightest of the lowest singlet states:

| | butadiene | hexatriene | octatetraene |
|---|---|---|---|
| measured $\lambda_\text{max}$ | 217 nm (5.71 eV) | 258 nm (4.81 eV) | 290 nm (4.28 eV) |
| CAM-B3LYP, full TD-DFT | 6.22 eV, $f$ = 0.72 | 5.10 eV, $f$ = 1.12 | 4.38 eV, $f$ = 1.55 |
| CAM-B3LYP, TDA | 6.73 eV, $f$ = 1.07 | 5.53 eV, $f$ = 1.66 | 4.76 eV, $f$ = 2.27 |
| B3LYP, full TD-DFT | 6.06 eV, $f$ = 0.67 | 4.89 eV, $f$ = 1.06 | 4.15 eV, $f$ = 1.47 |

1. Convert one value: CAM-B3LYP full for hexatriene, $\lambda = 1239.84/5.098 = 243$ nm, against 258 nm measured.
2. Errors in eV, CAM-B3LYP full: +0.51, +0.29, +0.11. With TDA: +1.01, +0.72, +0.48. TDA adds about 0.4–0.5 eV to every bright state here.
3. Trend: every setting puts the states in the right order and shifts them to the red with each added C=C, and every bright state gets stronger with chain length, as the transition dipole grows with the length of the box.
4. The errors are not constant: they shrink along the series. So a single shift would not fit all three, and the calculated step from butadiene to hexatriene (1.13 eV, CAM-B3LYP full) is larger than the measured one (0.91 eV).

The honest conclusion: with full TD-DFT, CAM-B3LYP/def2-SVP gets the series right to about 0.1–0.5 eV against solution maxima, which is typical. B3LYP happens to land closer here, which is not proof that it is the better functional: part of the difference between a vertical gas-phase energy and a solution band maximum is in the comparison itself. Each row also has states with $f$ near zero between the bright ones (for octatetraene a dark state sits only about 0.8 eV above the bright one at B3LYP). Real polyenes have a low-lying dark state that TD-DFT describes poorly; it does not show in absorption but matters for fluorescence.

## Hands-on

What you need: xtb and ORCA, Python with the course packages, the [Module 31 lab folder](../../labs/module-31/), Avogadro, the [lab report template](../../templates/lab-report.md) and a [notebook page](../../templates/notebook-page.md). Time: about 2 hours: 45 minutes for Parts A and B and 75 minutes for the module practical.

### Part A — geometries and the analysis script (15 min)

1. Open `lesson06_uvvis.py` and complete `ev_to_nm()` and `brightest()` (the state with the largest oscillator strength).
2. Run `py lesson06_uvvis.py`. Part A of the script optimises all-trans butadiene, hexatriene and octatetraene and formaldehyde with `xtb --ohess` into `runs/31.6-polyenes/`, checking that none has an imaginary frequency. Part B prints the reference rows above and plots `runs/lesson06_uvvis.png`.

How you know it worked (xtb 6.7.1, checked 2026-10-17; printout in `expected/31.6_uvvis.txt`): lowest modes 145.1, 86.6, 54.9 and 1085.6 cm⁻¹, no imaginary frequencies, and the reference rows of the table above.

### Part B — your own TD-DFT runs (30 min)

1. In `orca/` run `06_butadiene_tddft.inp`, `06_hexatriene_tddft.inp` and `06_octatetraene_tddft.inp` (CAM-B3LYP/def2-SVP, five roots, `TDA false`), one to a few minutes each.
2. In each output find the table `ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS`: one row per state with energy (eV and cm⁻¹), wavelength (nm) and `fosc`. Rerun `py lesson06_uvvis.py`: it reads your outputs and prints them above the reference rows.
3. Delete the line `TDA false` in the butadiene input, run it again into a different output file and compare the bright state.
4. Run `06_formaldehyde_tddft.inp`. The lowest state is the n→π* excitation with an oscillator strength of essentially zero, a dark state that is symmetry-forbidden in the planar molecule; the first state with a sizeable $f$ lies far higher in the vacuum UV.

How you know it worked: your full TD-DFT values agree with the CAM-B3LYP rows above to about 0.02 eV, and the TDA run is about 0.5 eV higher for butadiene. For formaldehyde, the reference (CAM-B3LYP/def2-SVP, TDA) gives the dark state at 4.10 eV with $f$ = 0.000 and the first bright state at 8.71 eV with $f$ = 0.18. The ORCA jobs were not run when the module was written; the reference values are PySCF results with the same settings.

<details><summary>Reference solution for Parts A and B</summary>

```python
def ev_to_nm(e_ev):
    return c.HC_EV_NM / e_ev

def brightest(states):
    return max(states, key=lambda s: s[2])
```

Full code: `lesson06_uvvis_solution.py`. If `brightest()` returns a state you did not expect, look at the orbital composition printed under each state in the ORCA output: the bright polyene state is dominated by HOMO → LUMO. If your bright state is missing, ask for more roots.

</details>

### Part C — module practical: calculated versus measured IR (75 min)

This is the larger practical piece of the module. It uses every skill so far: start geometries, optimisation, the minimum check, frequencies, mode matching, scaling and an honest error analysis. Write it up with the [lab report template](../../templates/lab-report.md) and put your error discussion in the [error analysis template](../../templates/error-analysis.md).

The question: how well do GFN2-xTB and r2SCAN-3c reproduce the measured gas-phase fundamentals of H₂O, NH₃, CH₄, CO₂, H₂CO and HCN (32 modes), and which modes are hardest?

1. In `orca/`, run the six inputs `06_ir_water.inp`, `06_ir_ammonia.inp`, `06_ir_methane.inp`, `06_ir_co2.inp`, `06_ir_formaldehyde.inp` and `06_ir_hcn.inp` (r2SCAN-3c TightOpt + Freq, under a minute each). If you cannot run ORCA, do the practical with xtb alone and say so in the report.
2. Open `lesson06_practical.py` and write `summarise()`: pool all (calculated, measured) pairs of one level, fit the least-squares scale factor, print the RMS error before and after scaling for the whole set and for each molecule, and list the three worst modes after scaling. The rest of the script runs xtb (`--ohess tight`) on all six molecules, reads your ORCA outputs, warns about imaginary frequencies and pairs modes by order with `exp_fundamentals.csv`.
3. Run `py lesson06_practical.py` and open `runs/lesson06_practical.png` (scaled calculated against measured, with the diagonal).
4. In the report: a table of scale factors and RMS errors per level; the worst modes and a physical reason for each (anharmonicity of X–H stretches, a mode GFN2-xTB is known to treat poorly); whether the IR-inactive modes (CO₂ symmetric stretch, CH₄ A₁ and E) belong in an IR comparison; and one paragraph on what the work does not test (only six small molecules, gas phase, harmonic model).

How you know it worked (GFN2-xTB with xtb 6.7.1, checked 2026-10-17; printout in `expected/31.6_practical.txt`): 32 modes in 6 molecules; scale factor 0.9824; RMS error 94 cm⁻¹ unscaled and 85 cm⁻¹ scaled; per molecule after scaling H₂O 118, NH₃ 87, CH₄ 54, CO₂ 117, H₂CO 60, HCN 100 cm⁻¹; worst modes after scaling CO₂ 2349 (calculated 2546), NH₃ 950 (calculated 1139) and H₂O 3756 (calculated 3586) cm⁻¹. No molecule has an imaginary frequency. Your r2SCAN-3c rows were not available when the module was written; expect a scale factor a few per cent below 1 and a clearly smaller scaled RMS than xtb.

<details><summary>Reference solution for summarise() and notes for the report</summary>

```python
def summarise(level, data):
    pairs = [p for v in data.values() for p in v]
    s = c.best_scale(pairs)
    print(f"\n{level}: {len(pairs)} modes in {len(data)} molecules")
    print(f"  scale factor {s:.4f}; RMS error {c.rms(pairs):.0f} cm-1 unscaled -> {c.rms(pairs, s):.0f} cm-1 scaled")
    for f, v in data.items():
        print(f"  {f:5s} RMS unscaled {c.rms(v):5.0f}  scaled {c.rms(v, s):5.0f} cm-1")
    worst = sorted(((abs(s * w - e), f, w, e) for f, v in data.items() for w, e in v), reverse=True)[:3]
    print("  worst modes after scaling:", "; ".join(f"{f} {e:.0f} (calc {s * w:.0f})" for _, f, w, e in worst))
    return pairs, s
```

Full code: `lesson06_practical_solution.py`. Points a good report makes:

- GFN2-xTB needs almost no global scaling (0.98) but its errors are random, so scaling barely helps (94 → 85 cm⁻¹), and for water it makes things worse (69 → 118 cm⁻¹). A method whose errors are systematic gains much more from scaling; compare your r2SCAN-3c numbers.
- The worst xtb modes are not the X–H stretches but the CO₂ antisymmetric stretch (about 200 cm⁻¹ too high) and the NH₃ umbrella (about 190 cm⁻¹ too high). The umbrella is the mode that leads over the inversion barrier of 31.5: its well is strongly anharmonic and split by tunnelling, so no harmonic model fits it well.
- Water's two stretches come out only 8 cm⁻¹ apart with GFN2-xTB, against 99 cm⁻¹ measured; pairing by order still works here, but in a larger molecule such near-degeneracies are where order-pairing goes wrong.
- Including IR-inactive modes is legitimate for testing the force field (they are measured by Raman), but a comparison with an IR spectrum should drop them or say clearly that it includes them.

</details>

## Common mistakes

- Taking the lowest excited state as the absorption band. Check the oscillator strengths; the bright state may be the third or fifth root.
- Leaving ORCA's default TDA on for bright π→π* states of conjugated molecules. Here it costs 0.4–0.5 eV; use `TDA false`.
- Comparing a single absolute number with experiment and declaring success or failure. Vertical gas-phase energies and solution band maxima differ by tenths of an eV; compare trends within a series.
- Using a global hybrid for donor–acceptor dyes. Charge-transfer states come out far too low; use a range-separated hybrid.
- Omitting diffuse functions for anions or Rydberg states, or asking for too few roots.
- In the IR practical: pooling different levels into one scale factor, or quietly including IR-inactive modes in an "IR" comparison.

## Key takeaways

- TD-DFT gives vertical excitation energies and oscillator strengths; $\lambda/\text{nm} = 1239.84/(E/\text{eV})$, and $f \approx 0$ marks a dark state.
- A vertical energy belongs near, not at, the band maximum; solvent and vibrational structure add systematic differences.
- Choose a range-separated hybrid for charge transfer, add diffuse functions where needed, request enough roots, and use full TD-DFT for bright π→π* states.
- For the polyenes, CAM-B3LYP/def2-SVP full TD-DFT is 0.1–0.5 eV high and gets the red shift with chain length right; trends are more reliable than single numbers.
- The module practical shows the same lesson for IR: a scale factor removes systematic error, the remaining scatter tells you how far to trust a method.

## Sources

- [ORCA 6.1 manual, Excited states via TD-DFT](https://www.faccts.de/docs/orca/6.1/manual/contents/spectroscopyproperties/tddft.html) — the `%tddft` block, `NRoots`, TDA as the default and `TDA false`, the ORCA 6 absorption table layout.
- [Yanai, Tew and Handy, Chem. Phys. Lett. 393, 51 (2004)](https://doi.org/10.1016/j.cplett.2004.06.011) — the CAM-B3LYP range-separated functional.
- [OpenStax Organic Chemistry, 14.8](https://openstax.org/books/organic-chemistry/pages/14-8-interpreting-ultraviolet-spectra-the-effect-of-conjugation) — measured $\lambda_\text{max}$ of butadiene (217 nm), hexatriene (258 nm) and octatetraene (290 nm).
- [NIST CCCBDB](https://cccbdb.nist.gov/exp2x.asp?casno=7732185&charge=0) — experimental fundamentals for the module practical (water page shown; the other five molecules are listed in `exp_fundamentals.csv`).
- [PySCF](https://pyscf.org/) — open-source program (version 2.14.0) used for the reference excitation energies in `polyenes_uv.csv`.
