---
id: "08.3"
module: 8
minutes: 20
practice_minutes: 70
prerequisites: ["08.2", "02.4"]
objectives:
  - Write the equilibrium-constant expression for a reaction and use Q versus K to predict which way a mixture will shift.
  - Solve an equilibrium problem with an ICE table, both exactly and with the small-x approximation, and judge when the approximation is acceptable.
  - Predict and calculate the effect of changing concentration, pressure and temperature (van 't Hoff equation) on an equilibrium.
volatility: concept
sources:
  - title: "OpenStax Chemistry 2e, 13.2 Equilibrium Constants"
    url: https://openstax.org/books/chemistry-2e/pages/13-2-equilibrium-constants
  - title: "OpenStax Chemistry 2e, 13.3 Shifting Equilibria: Le Châtelier's Principle"
    url: https://openstax.org/books/chemistry-2e/pages/13-3-shifting-equilibria-le-chateliers-principle
  - title: "OpenStax Chemistry 2e, 13.4 Equilibrium Calculations"
    url: https://openstax.org/books/chemistry-2e/pages/13-4-equilibrium-calculations
  - title: "OpenStax Chemistry 2e, Appendix G: Standard Thermodynamic Properties for Selected Substances"
    url: https://openstax.org/books/chemistry-2e/pages/g-standard-thermodynamic-properties-for-selected-substances
  - title: "Sander, Compilation of Henry's Law Constants: carbon dioxide (henrys-law.org)"
    url: https://henrys-law.org/henry/casrn/124-38-9
last_verified: "2026-10-17"
---

# 08.3 · Chemical equilibrium and Le Chatelier

Most reactions do not run to completion. They stop at a mixture of reactants and products whose make-up is fixed by one number, the equilibrium constant. In this lesson you learn to write that number for any reaction, to compare it with the present state of a mixture to see which way it will move, and to calculate the final composition with an ICE table. Then you will push on the equilibrium, by adding a reagent, squeezing the gas or heating it, and predict how it responds. These are the tools of every later topic in this module: acids, buffers, cells and titrations.

## Why it matters

A hydrogen plant runs the water-gas shift, $\mathrm{CO + H_2O \rightleftharpoons CO_2 + H_2}$, to turn poisonous carbon monoxide into more hydrogen. At the operating temperature, a 1 : 1 feed converts only about half the CO. Should the engineer raise the temperature, raise the pressure, or add more steam? Each choice costs money, and only one of them helps. The same reasoning tells you why a bottle of sparkling water goes flat faster on a hot day, and why your blood can carry oxygen to tissues and drop it there. You can answer all of these with an equilibrium constant and a short calculation.

## Core ideas

> [!NOTE]
> The laws here (mass action, Le Chatelier, van 't Hoff) are stable. Numerical $K$ values come from OpenStax Chemistry 2e Appendix G via $\Delta G^\circ = -RT\ln K$ (lesson 08.2), assuming constant $\Delta H$ and $\Delta S$, checked 2026-10-17. Other tables can give $K$ values that differ by a factor of 2: a difference of only 2 kJ/mol in $\Delta G^\circ$ does that.

### Dynamic equilibrium

At equilibrium the reaction has not stopped. The forward and backward reactions both still run, at equal rates, so the amounts no longer change. Label one molecule with an isotope and it will turn up on the other side, although nothing seems to happen. The double arrow $\rightleftharpoons$ means exactly this.

### The equilibrium constant

For a general reaction $a\mathrm{A} + b\mathrm{B} \rightleftharpoons c\mathrm{C} + d\mathrm{D}$, the **equilibrium constant** is

$$K = \frac{[\mathrm{C}]^c\,[\mathrm{D}]^d}{[\mathrm{A}]^a\,[\mathrm{B}]^b}$$

with each concentration divided by the standard 1 mol/L, so $K$ has no units. For gases you can use partial pressures in bar instead; then the constant is written $K_p$. Pure solids and pure liquids (including water as the solvent) do not appear: their "concentration" does not change. The rules follow from lesson 08.2: reverse the reaction and $K$ becomes $1/K$; double the coefficients and $K$ becomes $K^2$.

The same expression with the *present* amounts, not the equilibrium ones, is the **reaction quotient** $Q$. Compare it with $K$:

- $Q < K$: too little product. The reaction runs forward.
- $Q > K$: too much product. It runs backward.
- $Q = K$: at equilibrium, $\Delta G = 0$.

This is the same statement as $\Delta G = \Delta G^\circ + RT\ln Q = RT\ln(Q/K)$, which is negative exactly when $Q < K$.

### ICE tables

To find the equilibrium composition, write three rows under the equation: **I**nitial amounts, **C**hange, **E**quilibrium. The change is set by the stoichiometry and one unknown, $x$, the **extent** of reaction. Put the E row into $K$ and solve for $x$.

Example: $\mathrm{N_2O_4(g) \rightleftharpoons 2NO_2(g)}$, $K_p = 0.31$ at 298 K. Start with 1 mol N₂O₄ and let a fraction $\alpha$ dissociate at total pressure $P$.

| | N₂O₄ | NO₂ | total |
|---|---|---|---|
| I | 1 | 0 | 1 |
| C | $-\alpha$ | $+2\alpha$ | |
| E | $1-\alpha$ | $2\alpha$ | $1+\alpha$ |

Partial pressures are mole fraction times $P$, so

$$K_p = \frac{\left(\frac{2\alpha}{1+\alpha}P\right)^2}{\frac{1-\alpha}{1+\alpha}P} = \frac{4\alpha^2 P}{1-\alpha^2}$$

At 1 bar, $\alpha = \sqrt{K_p/(K_p + 4P)} = \sqrt{0.31/4.31} = 0.27$: about a quarter of the N₂O₄ has split.

### The small-x approximation, and when it fails

Most ICE equations are quadratics or worse. When $K$ is small, $x$ is small, and you can drop $x$ next to larger numbers: here $1 - \alpha^2 \approx 1$, so $\alpha \approx \sqrt{K_p/4P}$. That is the first term of a Taylor series (lesson [02.4](../module-02/lesson-04.md)). At 1 bar it gives 0.28 instead of 0.27, an error of 4 %. The usual rule: accept the approximation if $x$ is under 5 % of the number you dropped it from, and *check afterwards*. At 0.1 bar the shortcut gives 0.88 against the true 0.66, which is useless. When in doubt, solve exactly: the quadratic formula, or a numerical root finder, which you will use in the hands-on.

### Le Chatelier's principle

**Le Chatelier's principle**: if you disturb a system at equilibrium, it shifts in the direction that partly undoes the disturbance. Each case is just $Q$ compared with $K$.

- **Add a reactant or remove a product.** $Q$ drops below $K$, so the reaction runs forward. Adding steam to the water-gas shift raises the CO conversion.
- **Raise the pressure by compressing a gas mixture.** The side with fewer moles of gas is favoured. In $\mathrm{N_2O_4 \rightleftharpoons 2NO_2}$, $\alpha$ falls from 0.27 at 1 bar to 0.09 at 10 bar. When both sides have the same number of gas moles, as in the water-gas shift, pressure has no effect. Adding an inert gas at constant volume changes nothing either.
- **Change the temperature.** This is the only change that alters $K$ itself. Heating favours the endothermic direction.

### Temperature and the van 't Hoff equation

From $\ln K = -\Delta H^\circ/RT + \Delta S^\circ/R$, two temperatures give

$$\ln\frac{K_2}{K_1} = -\frac{\Delta H^\circ}{R}\left(\frac{1}{T_2} - \frac{1}{T_1}\right)$$

the **van 't Hoff equation**. For N₂O₄ dissociation, $\Delta H^\circ = +55.3$ kJ/mol (endothermic). Cooling to 0 °C:

$$\ln\frac{K_{273}}{0.31} = -\frac{55\,300}{8.314}\left(\frac{1}{273.15} - \frac{1}{298.15}\right) = -2.04, \quad K_{273} = 0.040$$

The brown NO₂ fades in an ice bath and darkens in hot water, which is a classic lecture demonstration. Do not try it at home: NO₂ is a toxic gas.

Gases dissolving in water are usually exothermic, so warming water drives gas out. For CO₂, the Henry's-law solubility at 5 °C is about 1.8 times that at 25 °C (Sander's compilation, temperature coefficient 2400 K). A warm bottle of soda goes flat faster.

## Worked example

### Water-gas shift: more steam or more pressure?

At 1000 K, $K = 0.91$ for $\mathrm{CO + H_2O \rightleftharpoons CO_2 + H_2}$ (from Appendix G and lesson 08.2). Feed 1 mol CO and 1 mol H₂O.

| | CO | H₂O | CO₂ | H₂ |
|---|---|---|---|---|
| I | 1 | 1 | 0 | 0 |
| C | $-x$ | $-x$ | $+x$ | $+x$ |
| E | $1-x$ | $1-x$ | $x$ | $x$ |

The total moles stay 2, and both sides have 2 moles of gas, so the pressure cancels:

$$K = \frac{x^2}{(1-x)^2} = 0.91 \;\Rightarrow\; \frac{x}{1-x} = \sqrt{0.91} = 0.95 \;\Rightarrow\; x = 0.49$$

Only 49 % of the CO is converted. Now feed 3 mol of steam per mole of CO:

$$\frac{x^2}{(1-x)(3-x)} = 0.905 \;\Rightarrow\; 0.095x^2 + 3.62x - 2.715 = 0 \;\Rightarrow\; x = 0.74$$

(from the quadratic formula, keeping the root between 0 and 1). Excess steam lifts the conversion to 74 %. Raising the pressure would do nothing, because the gas moles are equal on both sides. The reaction is exothermic ($\Delta H^\circ = -41$ kJ/mol), so lowering the temperature also helps, which is why real plants run a second, cooler shift stage with a catalyst that still works there.

## Hands-on

What you need: the [Module 8 lab folder](../../labs/module-08/) with Python 3.14, a calculator and your notebook; for the optional part, two identical sealed 500 mL bottles of sparkling water, a fridge and a kitchen scale (0.1 g). Time: about 70 minutes, plus 40 minutes for the optional part.

### Part A — pencil (20 min)

1. A water-gas-shift reactor at 1000 K ($K = 0.91$) contains CO, H₂O and CO₂ at 1 bar each and H₂ at 2 bar. Which way does it shift?
2. Find $\alpha$ for N₂O₄ ($K_p = 0.31$) at 10 bar, exactly and with the small-x shortcut. Is the shortcut acceptable?
3. Ammonia synthesis, $\mathrm{N_2 + 3H_2 \rightleftharpoons 2NH_3}$, is exothermic. What happens to the equilibrium amount of NH₃ if you (a) raise the temperature, (b) raise the pressure, (c) add an iron catalyst?
4. Use the van 't Hoff equation to find $K_p$ for N₂O₄ dissociation at 50 °C.

<details><summary>Answers to Part A</summary>

1. $Q = (1 \times 2)/(1 \times 1) = 2 > K$: too much product, so it shifts backward, making CO and H₂O.
2. Exact: $\alpha = \sqrt{0.31/40.31} = 0.088$. Small-x: $\sqrt{0.31/40} = 0.088$. They agree to 0.4 %; acceptable.
3. (a) Less NH₃: heating favours the endothermic, backward direction, and $K$ falls. (b) More NH₃: four moles of gas become two. (c) No change in the amount: a catalyst speeds both directions equally and leaves $K$ alone, so equilibrium is only reached sooner.
4. $\ln(K/0.31) = -(55\,300/8.314)(1/323.15 - 1/298.15) = +1.73$, so $K = 0.31 \times 5.6 = 1.75$.

</details>

### Part B — Python: exact equilibria with a root finder (40 min)

Open `lesson03_equilibrium.py`. Fill in the two TODOs: `reaction_quotient` (the product of $(x_i P)^{\nu_i}$) and the inner function `f(xi)` that builds the ICE row and returns $\ln Q - \ln K$. The script then uses `scipy.optimize.brentq`, a root finder that brackets the answer between the two extents where some amount would reach zero, so it never returns a negative concentration. Run:

```bash
py lesson03_equilibrium.py
```

How you know it worked: the water-gas shift at 1000 K prints $K = 0.905$ and conversions of 48.8 % (1 : 1 feed) and 73.6 % (1 : 3 feed). The N₂O₄ table shows the small-x error growing from 0.1 % at 30 bar to 3.8 % at 1 bar and 33 % at 0.1 bar. The van 't Hoff block gives $K$ = 0.0405 at 0 °C and 27.7 at 100 °C, with $\alpha$ at 1 bar rising from 0.10 to 0.94. The plot `runs/lesson03_N2O4_vs_P.png` shows where the two curves part.

Then change the water-gas-shift temperature to 700 K and predict the conversion before you run it.

<details><summary>Reference solution</summary>

`reaction_quotient`: `n_tot = sum(moles.values())`, then multiply `(moles[sp] / n_tot * p_total) ** nu` for every species. `f`: `moles = {sp: n0[sp] + nu * xi for sp, nu in reaction.items()}` and `return np.log(reaction_quotient(reaction, moles, p_total)) - np.log(k)`. Full code in `lesson03_equilibrium_solution.py`. Using $\ln Q - \ln K$ instead of $Q - K$ keeps the function well behaved when $K$ is huge or tiny. At 700 K, $K$ rises to about 7.6 and the 1 : 1 conversion to about 73 %: exothermic, so cooler is better for the yield.

</details>

### Part C — optional home: does warm soda go flat faster? (40 min)

> [!CAUTION]
> Never heat a closed bottle, and never leave one in a hot car or in the sun: the pressure can burst it. Open bottles slowly, cap pointing away from faces, and do not shake them first. Use plastic bottles, not glass.

1. Put one bottle in the fridge and leave the other at room temperature for at least 3 hours. Record both temperatures (measure a little poured into a cup).
2. Open both slowly at the same time. Put the caps aside. Weigh each open bottle right away and then every 10 minutes for 30 minutes, without shaking.
3. The mass lost is mostly CO₂ (water evaporation is a few tenths of a gram at most in 30 minutes). Write the result on a [notebook page](../../templates/notebook-page.md).

How you know it worked: both bottles lose most mass in the first 10 minutes; the warm bottle typically loses two to four times as much CO₂ as the cold one in 30 minutes. That is Le Chatelier for $\mathrm{CO_2(g) \rightleftharpoons CO_2(aq)}$, an exothermic dissolving: warming shifts it towards the gas.

## Common mistakes

- **Putting solids, pure liquids or solvent water in $K$.** Leave them out. In aqueous reactions $[\mathrm{H_2O}]$ is not in $K$.
- **Forgetting the exponents.** In $K_p$ for N₂O₄, the NO₂ pressure is squared because its coefficient is 2.
- **Using small-x without checking.** Compute $x$, then check it is under 5 % of what you dropped it from. If not, solve exactly.
- **Thinking a catalyst or added reagent changes $K$.** Only temperature changes $K$. Adding reagents changes $Q$; a catalyst changes neither, only the speed.
- **Applying the pressure rule when gas moles are equal, or when an inert gas is added at constant volume.** No shift in either case.
- **Choosing the wrong root of the quadratic.** Keep the root that gives no negative amounts.

## Key takeaways

- At equilibrium both directions run at equal rates. $K$ is products over reactants, each raised to its coefficient, without solids, pure liquids or solvent.
- Compare $Q$ with $K$: $Q < K$ runs forward, $Q > K$ runs backward. This is $\Delta G = RT\ln(Q/K)$.
- ICE tables give one equation in one unknown. Use small-x only when it passes the 5 % check; otherwise solve exactly or numerically.
- Le Chatelier: adding a reagent, changing the pressure or changing the temperature each shifts the equilibrium so as to oppose the change, but only temperature changes $K$, as the van 't Hoff equation shows.

## Sources

- [OpenStax Chemistry 2e, 13.2 Equilibrium Constants](https://openstax.org/books/chemistry-2e/pages/13-2-equilibrium-constants) — $K$, $Q$, $K_p$, what is left out of $K$.
- [OpenStax Chemistry 2e, 13.3 Le Châtelier's Principle](https://openstax.org/books/chemistry-2e/pages/13-3-shifting-equilibria-le-chateliers-principle) — effects of concentration, pressure, temperature and catalysts.
- [OpenStax Chemistry 2e, 13.4 Equilibrium Calculations](https://openstax.org/books/chemistry-2e/pages/13-4-equilibrium-calculations) — ICE tables and the small-x approximation.
- [OpenStax Chemistry 2e, Appendix G](https://openstax.org/books/chemistry-2e/pages/g-standard-thermodynamic-properties-for-selected-substances) — data for every $K$ calculated here.
- [Sander, Henry's law constants: carbon dioxide](https://henrys-law.org/henry/casrn/124-38-9) — CO₂ solubility $3.3 \times 10^{-4}$ mol m⁻³ Pa⁻¹ at 298 K, temperature coefficient 2400 K.
