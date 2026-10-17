# Calculated versus measured IR spectra for 30 molecules

This is the example project named in the course plan: calculate the vibrational frequencies of about 30 small molecules with a fast method and with DFT, compare them with measured gas-phase fundamentals, and find out how large the error is, whether one scale factor removes it, and which kinds of vibration remain wrong. It is a computational project with no chemicals, and it extends the six-molecule practical of Module 31 to a real benchmark.

## Question

What is the RMS error of GFN2-xTB and of r2SCAN-3c harmonic frequencies against measured gas-phase fundamentals for 30 small molecules, before and after one fitted scale factor, and which mode types (X–H stretches, bends, torsions) carry most of the remaining error?

Narrower versions: only carbonyl stretches in 30 carbonyl compounds; only X–H stretches; xtb against two DFT methods.

## Why it is worth doing

Calculated spectra are used to identify unknowns and to screen molecules. Users need to know how far to trust each method and for which modes. Published scale factors exist for many methods (NIST CCCBDB), but not always for the newest fast methods, and an error broken down by mode type is more useful than one number.

## What you need

- xtb and ORCA set up as in [31.1](../../lessons/module-31/lesson-01.md); Avogadro to build and inspect molecules.
- Reference data: experimental fundamentals from the [NIST CCCBDB](https://cccbdb.nist.gov/) (release 22) and gas-phase IR spectra from the [NIST Chemistry WebBook](https://webbook.nist.gov/chemistry/). Cite both; record the page and date for every molecule.
- Python with numpy, scipy and matplotlib (`labs/common/requirements.txt`).

## Method

1. Choose 30 molecules with complete, reliable experimental fundamentals (small, rigid, one dominant conformer). Hold 10 out from the start.
2. Known-answer test: reproduce the water and formaldehyde results of [31.4](../../lessons/module-31/lesson-04.md).
3. For each molecule: optimise, run frequencies, confirm no imaginary frequency, and match each calculated mode to its measured partner by symmetry and by animating it ([20.6](../../lessons/module-20/lesson-06.md)).
4. Fit the scale factor on the 20 fitting molecules; report the RMS error on the 10 held-out ones, before and after scaling, for each method and each mode type.
5. Write the report and poster (Lesson [33.3](../../lessons/module-33/lesson-03.md)); the residual plot of `labs/module-33/lesson03_poster_figure.py` is a good main figure.

## Validation

Your scale factor for a method should be close to the published CCCBDB value where one exists. Check five mode assignments a second time by eye. Compare your unscaled water frequencies with the 31.4 reference numbers.

## Hours budget

Reading 25 (Module 31 again, CCCBDB scaling notes, one benchmark paper) · setup and pilot 20 (five molecules end to end) · runs 50 (about 10 attended minutes per molecule and method, plus mode matching, which is the slow part) · analysis 35 · report 30 · poster 10 · feedback 10.

## What it cannot show

Harmonic frequencies are compared with anharmonic fundamentals, so part of the "error" is physics the method does not attempt. Gas-phase results say little about spectra in solution or in solids. Intensities are not tested unless you add them. Thirty small molecules do not represent large, flexible ones.

## Starting links

- [31.4 · Calculated IR and NMR spectra versus experiment](../../lessons/module-31/lesson-04.md)
- [31.6 · Excited states with time-dependent DFT](../../lessons/module-31/lesson-06.md) (its module practical compares six molecules)
- [09.3 · Propagation of uncertainty](../../lessons/module-09/lesson-03.md)
- [11.2 · Finding and judging sources and data](../../lessons/module-11/lesson-02.md)
