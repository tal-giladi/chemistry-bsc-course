# Is supermarket vinegar what the label says?

> [!WARNING]
> Use only the materials of Lesson [10.6](../../lessons/module-10/lesson-06.md): white vinegar, baking soda, red-cabbage indicator, tap water, a kitchen scale and oral syringes. Wear safety glasses; vinegar stings the eyes. Never mix vinegar (or any acid) with bleach: it releases chlorine gas. Do not buy laboratory reagents for this project (Lesson [01.4](../../lessons/module-01/lesson-04.md)). Label every bottle and cup, and keep them away from children and food.

Vinegar labels give the acidity, usually around 4–6 % acetic acid. In 10.6 you measured one vinegar five times and compared it with its label. This project scales that up into a small market survey: several brands, enough repeats to tell them apart, a standard to control drift, and a full uncertainty budget. It is a safe home-measurement project.

## Question

For six to eight white-vinegar products sold in your area, is the measured acetic acid content (g per 100 g) equal to the label value within the combined uncertainty, and are the differences between products larger than the measurement uncertainty?

## Why it is worth doing

Label accuracy is a real quality-control question, and the answer depends entirely on the uncertainty: a 0.1 % difference means nothing if your 95 % interval is ±0.2 %. Doing it properly means designing for a target precision, controlling drift, and stating what the measurement can and cannot say, which is the core of analytical chemistry.

## What you need

- The 10.6 kit: kitchen scale (0.01 g if possible), oral syringes, cups, baking soda, red-cabbage indicator.
- Two bottles of each product if you can (from different shops or batches), to see bottle-to-bottle variation.
- A standard: a solution you make from a weighed amount of baking soda, titrated against a check vinegar every session to track drift.

## Method

1. Known-answer test: repeat the 10.6 measurement on the vinegar you used there and get the same result within its interval.
2. Pilot: four titrations of one product to estimate the standard deviation; compute the number of repeats with `labs/module-33/lesson02_sample_size.py` for the half-width you need (Lesson [33.2](../../lessons/module-33/lesson-02.md)).
3. Main run: all titrations in a shuffled order across products and days, with the check vinegar titrated at the start of each session.
4. Report each product as mean ± 95 % interval with an uncertainty budget ([error analysis template](../../templates/error-analysis.md)), the comparison with the label, and the between-product differences.

## Validation

The check vinegar must give the same value in every session within its uncertainty; if it drifts, correct with it or remake the titrant. The blank (indicator only) must be measured, as in 10.6.

## Hours budget

Reading 25 · setup and pilot 20 · titrations 50 (about 20 minutes each, about 100 titrations with reruns) · analysis 35 · report 30 · poster 10 · feedback 10.

## What it cannot show

Baking soda is not a primary standard of laboratory grade and absorbs moisture; the endpoint colour is judged by eye; a kitchen scale is not an analytical balance. The result is the acidity as total acid titrated, not acetic acid alone. A few bottles do not represent a product's whole production. A real quality-control lab would use standardised NaOH, a pH meter and certified glassware.

## Starting links

- [10.6 · Project: home vinegar titration with full error analysis](../../lessons/module-10/lesson-06.md)
- [09.2 · Statistics: mean, standard deviation and confidence intervals](../../lessons/module-09/lesson-02.md)
- [09.3 · Propagation of uncertainty](../../lessons/module-09/lesson-03.md)
- [33.2 · Designing the study and managing the data](../../lessons/module-33/lesson-02.md)
