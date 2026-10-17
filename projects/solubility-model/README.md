# Predicting aqueous solubility from structure

This is the second example project named in the course plan: build a model that predicts a property from public data. Water solubility decides whether a drug can be absorbed, how a pesticide spreads and how a pollutant is cleaned up. You will build a simple, explainable model from a large, freely licensed data set, test it honestly on compounds it never saw, and find out which kinds of molecules it gets wrong. It is a data project with no chemicals.

## Question

On held-out compounds from AqSolDB, how much lower is the RMS error in log S of a model using a dozen RDKit descriptors than that of a four-descriptor linear equation in the style of ESOL (Delaney 2004), and which compound classes have the largest errors?

## Why it is worth doing

Solubility models are everywhere, and many report errors measured on the data they were fitted to. A careful, honest comparison of a simple baseline and a slightly richer model, with a held-out test and an analysis of failures, is exactly what a reader needs to judge such models. You also meet the thermodynamics of [13.6](../../lessons/module-13/lesson-06.md) in a practical form: solubility is an equilibrium constant.

## What you need

- AqSolDB: about 10,000 curated aqueous solubilities with reliability labels (Sorkun, Khetan and Er 2019, [Scientific Data](https://doi.org/10.1038/s41597-019-0151-1)); data on [Harvard Dataverse](https://doi.org/10.7910/DVN/OVHAW8) under CC0 1.0 (checked 2026-10-17). Download it into `data/raw/` with the date.
- The ESOL paper for the baseline descriptors: Delaney (2004), [J. Chem. Inf. Comput. Sci. 44, 1000](https://doi.org/10.1021/ci034243x).
- Python with pandas, numpy, scipy, matplotlib and RDKit (pinned in `labs/common/requirements.txt`).

## Method

1. Keep only the most reliable entries (read the reliability groups in the paper), remove duplicates and salts, and record every filter in code.
2. Split once into fitting (80 %) and held-out (20 %) sets with a fixed seed, before looking at any result. Better: split by chemical scaffold so similar molecules do not sit on both sides.
3. Baseline: refit the four ESOL descriptors (calculated logP, molecular weight, rotatable bonds, aromatic proportion) by least squares ([05.3](../../lessons/module-05/lesson-03.md)).
4. Richer model: add about ten RDKit descriptors (polar surface area, H-bond donors and acceptors, charge, ring counts) to a linear model; avoid black-box methods you cannot explain.
5. Report held-out RMS and mean absolute error with bootstrap uncertainties, and list the 20 worst predictions with a chemical reason for each.

## Validation

The refitted baseline should reach an error of the size reported in the literature for ESOL-type models (find and cite it). A model that is much better on the fitting set than on the held-out set is overfitting. Check ten random structures by eye against their names.

## Hours budget

Reading 25 · setup and pilot 20 (download, clean, baseline on a sample) · data work 50 (cleaning and descriptor calculation take longer than the modelling) · analysis 35 · report 30 · poster 10 · feedback 10.

## What it cannot show

The measurements come from many labs with different methods and temperatures; part of the error is in the data. Solubility depends on the solid form (polymorphs, hydrates), which a 2D structure does not describe. A model that works on this chemical space may fail on very different molecules.

## Starting links

- [05.3 · Fitting models to data with uncertainty](../../lessons/module-05/lesson-03.md)
- [09.4 · Calibration, linear regression and detection limits](../../lessons/module-09/lesson-04.md)
- [11.2 · Finding and judging sources and data](../../lessons/module-11/lesson-02.md)
- [13.6 · Solutions, activity and equilibrium constants](../../lessons/module-13/lesson-06.md)
