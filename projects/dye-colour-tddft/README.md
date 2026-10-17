# Colour of conjugated dyes: particle in a box against TD-DFT

Module 30 explained the colour of cyanine dyes with a particle in a box, and Module 31 calculated excited states with time-dependent DFT. This project puts the two side by side on a larger set of dyes with published absorption maxima and asks when the simple model is good enough and when the calculation earns its cost. It is a computational project with no chemicals.

## Question

For about 12 cyanine dyes and 8 linear polyenes with published absorption maxima, what is the mean absolute error in λmax of (a) the fitted particle-in-a-box model and (b) TD-DFT with two functionals, and does either capture the different behaviour of cyanines (steady shift per added CH=CH) and polyenes (approach to a limit)?

## Why it is worth doing

Dye chemists still use simple models to design colours, and TD-DFT is known to struggle with cyanines. A small, clean comparison on a common set shows the strengths and limits of each, and the polyene/cyanine contrast is a real test of physics rather than a curve fit.

## What you need

- ORCA and xtb as set up in [31.1](../../lessons/module-31/lesson-01.md); Avogadro to build the structures.
- Published λmax values with solvent, from supplier specifications and the literature you cite (as in [30.4](../../lessons/module-30/lesson-04.md)); record the source, solvent and date for each. Values for one dye can differ by a few nm between sources; note the spread.
- Python with numpy, scipy and matplotlib.

## Method

1. Build the set and hold out four dyes (two of each family) that no model may be fitted to.
2. Known-answer test: reproduce the box-model fit and blind prediction of 30.4.
3. Fit the box model (bond length fixed, end extension fitted) on the fitting dyes; predict the held-out ones.
4. Optimise each dye (xtb, then DFT), run TD-DFT for the first excited states with a global hybrid and a range-separated functional as in [31.6](../../lessons/module-31/lesson-06.md), and convert the brightest low-lying transition to λmax.
5. Compare errors by family and model; plot λmax against chain length for both families with the predictions.

## Validation

The box model must reproduce the 30.4 numbers. For TD-DFT, check that the brightest transition is the HOMO→LUMO π→π* one and that the geometry has no imaginary frequencies. Compare a known polyene with the value in 31.6.

## Hours budget

Reading 25 · setup and pilot 20 (one cyanine, one polyene end to end) · runs 50 (larger dyes need hours of machine time each; budget calendar days) · analysis 35 · report 30 · poster 10 · feedback 10.

## What it cannot show

Calculations are in the gas phase or with a simple solvent model, while the measurements are in solution. Vertical excitation energies are not band maxima; vibronic structure shifts the peak. Counter-ions and aggregation in real dye solutions are ignored. Twenty dyes are a small set.

## Starting links

- [30.4 · Electronic spectra of conjugated dyes: particle in a box](../../lessons/module-30/lesson-04.md)
- [31.6 · Excited states with time-dependent DFT](../../lessons/module-31/lesson-06.md)
- [12.2 · The Schrödinger equation and the particle in a box](../../lessons/module-12/lesson-02.md)
- [09.4 · Calibration, linear regression and detection limits](../../lessons/module-09/lesson-04.md)
