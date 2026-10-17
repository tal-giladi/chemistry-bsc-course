# Hammett constants from the IUPAC pKa compilation

The Hammett σ constants of [28.3](../../lessons/module-28/lesson-03.md) are defined by the acidity of substituted benzoic acids in water at 25 °C. A large digitized data set of measured pKa values is now freely available. This project recomputes σ from it, compares the values with the standard table, and then uses them to measure the sensitivity ρ of other acid families. It is a data project with no chemicals.

## Question

Do the meta- and para-substituted benzoic acids in the IUPAC digitized pKa dataset reproduce the tabulated Hammett σ values within their measurement scatter, and what ρ do phenols and phenylacetic acids give when plotted against those σ values?

## Why it is worth doing

Hammett constants are used every day to reason about mechanisms and to design molecules, but most people take them from a 1991 table. Checking them against the original measurements, with a proper uncertainty for each, shows how solid the foundation is. The ρ values then test the theory of [28.3](../../lessons/module-28/lesson-03.md) on real data.

## What you need

- The [IUPAC Digitized pKa Dataset](https://github.com/IUPAC/Dissociation-Constants) (v2.4a, digitized from the IUPAC compilations; licence CC BY-NC 4.0 with the attribution "Reproduced by permission of International Union of Pure and Applied Chemistry", checked 2026-10-17). Non-commercial use only; cite the dataset DOI given in its README.
- The reference table: Hansch, Leo and Taft (1991), [Chem. Rev. 91, 165](https://doi.org/10.1021/cr00002a004), as used in 28.3.
- Python with pandas, numpy, scipy, matplotlib and RDKit (to recognise substituents from structures).

## Method

1. Select aqueous values at 25 °C (or within a stated window) for benzoic acid and its monosubstituted meta and para derivatives. Record each filter in code and keep the reference codes.
2. Where several measurements exist for one acid, take a weighted mean and its spread ([09.2](../../lessons/module-09/lesson-02.md)).
3. Compute $\sigma_X = \mathrm{p}K_a(\mathrm{H}) - \mathrm{p}K_a(\mathrm{X})$ with propagated uncertainty ([09.3](../../lessons/module-09/lesson-03.md)) and compare with the table.
4. For phenols and phenylacetic acids, plot pKa against σ and fit ρ with its uncertainty; look for substituents that need σ⁻ instead of σ.

## Validation

Benzoic acid itself should come out near pKa 4.20; your σ for p-NO₂ and p-CH₃ should match the table to a few hundredths. The ρ for phenols should be clearly larger than 1, as 28.3 predicts; check its sign and size against the textbook value you cite.

## Hours budget

Reading 25 · setup and pilot 20 (load the data, find benzoic acid and five derivatives) · data work 50 (substituent recognition and cleaning) · analysis 35 · report 30 · poster 10 · feedback 10.

## What it cannot show

The compilations mix methods, ionic strengths and temperatures; filtering helps but does not remove all differences. Ortho substituents do not follow simple Hammett behaviour and are left out. The data set ends with the compilations it digitizes and does not include newer measurements.

## Starting links

- [28.3 · Linear free-energy relationships: Hammett](../../lessons/module-28/lesson-03.md)
- [09.2 · Statistics: mean, standard deviation and confidence intervals](../../lessons/module-09/lesson-02.md)
- [09.3 · Propagation of uncertainty](../../lessons/module-09/lesson-03.md)
- [11.1 · Reading a research paper efficiently](../../lessons/module-11/lesson-01.md)
