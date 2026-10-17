# Temperature and the fading of food dye in bleach

> [!WARNING]
> **Never mix bleach with acids or with ammonia.** Bleach with vinegar, citric acid, lemon juice, descalers or toilet cleaners releases chlorine gas; bleach with ammonia, glass cleaners or urine releases chloramine gases. Use only plain unscented household bleach, tap water and blue food colouring (E133), exactly as in Lesson [23.4](../../lessons/module-23/lesson-04.md). Never more than 10 mL of bleach in one run, always added to a lot of water. Work by an open window or with a fan, wear safety glasses and gloves, and use water no hotter than hand-warm (about 35 °C): never heat bleach solutions on a stove or in a microwave. Pour finished runs down the sink with plenty of water.

In 23.4 you followed the fading of a blue food dye in dilute bleach with a phone camera and estimated an activation energy from two temperatures. This project turns that into a proper study: five or six temperatures between cold tap water and hand-warm, enough repeats at each, and an Arrhenius plot with an honest uncertainty. It is a safe home-measurement project.

## Question

What is the activation energy, with its 95 % confidence interval, of the pseudo-first-order fading of food dye E133 in dilute household bleach between about 10 °C and 35 °C, and is the Arrhenius plot straight over that range?

## Why it is worth doing

An activation energy from two points has no check of the model. Five or six temperatures with repeats test whether the Arrhenius law holds and give an uncertainty you can defend. The project trains the whole kinetics workflow of Module 22 on your own data: rate constants from absorbance-like signals, their scatter, and a weighted fit.

## What you need

- The 23.4 kit: bleach, E133 blue food colouring, clear plastic cups, oral syringe, phone on a fixed stand, white paper, a kitchen thermometer.
- Cold water from the refrigerator and hand-warm tap water to set the temperatures; a larger bowl of water at the same temperature around the cup helps keep it steady.
- The Module 23 analysis scripts for $k'$ from photos.

## Method

1. Known-answer test: repeat the 23.4 room-temperature run and get $k'$ within your earlier interval.
2. Pilot: four runs at room temperature give the scatter; compute the repeats needed per temperature (Lesson [33.2](../../lessons/module-33/lesson-02.md)).
3. Main run: five or six temperatures, the same bleach volume, all runs in a shuffled order, temperature read at the start and end of each run. Use the same bottle of bleach, and note its age; it loses strength over weeks.
4. Fit $\ln k'$ against $1/T$ with uncertainties ([22.4](../../lessons/module-22/lesson-04.md)); look at the residuals for curvature.

## Validation

Every session starts with one room-temperature run; if its $k'$ drifts, the bleach is weakening and you correct for it. The order in bleach (from two bleach volumes at one temperature) should be close to 1, as in 23.4.

## Hours budget

Reading 25 · setup and pilot 20 · runs 50 (about 30 minutes each including photos and cleaning) · analysis 35 · report 30 · poster 10 · feedback 10.

## What it cannot show

Phone-camera colour is not a calibrated absorbance; the temperature drifts during a run; household bleach is not of known, constant concentration. The narrow temperature range limits the precision of $E_a$. A real lab would use a thermostatted spectrophotometer and a standardised hypochlorite solution.

## Starting links

- [23.4 · Kinetics: dye fading tracked with a phone camera](../../lessons/module-23/lesson-04.md)
- [22.4 · Temperature dependence: Arrhenius and transition-state theory](../../lessons/module-22/lesson-04.md)
- [22.2 · Measuring rates: methods and data analysis](../../lessons/module-22/lesson-02.md)
- [09.3 · Propagation of uncertainty](../../lessons/module-09/lesson-03.md)
