---
id: "08.2"
module: 8
minutes: 20
practice_minutes: 60
prerequisites: ["08.1", "02.1"]
objectives:
  - Calculate a standard reaction entropy from tabulated S° values and say whether its sign makes physical sense.
  - Use ΔG = ΔH − TΔS to decide whether a process is spontaneous at a given temperature, and find the crossover temperature where ΔG = 0.
  - Convert a standard free energy into an equilibrium constant with ΔG° = −RT ln K, and back.
volatility: concept
sources:
  - title: "OpenStax Chemistry 2e, 16.2 Entropy"
    url: https://openstax.org/books/chemistry-2e/pages/16-2-entropy
  - title: "OpenStax Chemistry 2e, 16.3 The Second and Third Laws of Thermodynamics"
    url: https://openstax.org/books/chemistry-2e/pages/16-3-the-second-and-third-laws-of-thermodynamics
  - title: "OpenStax Chemistry 2e, 16.4 Free Energy"
    url: https://openstax.org/books/chemistry-2e/pages/16-4-free-energy
  - title: "OpenStax Chemistry 2e, Appendix G: Standard Thermodynamic Properties for Selected Substances"
    url: https://openstax.org/books/chemistry-2e/pages/g-standard-thermodynamic-properties-for-selected-substances
  - title: "NIST CODATA value: molar gas constant"
    url: https://physics.nist.gov/cgi-bin/cuu/Value?r
last_verified: "2026-10-17"
---

# 08.2 · Entropy, free energy and spontaneity

Heat alone does not decide which way a process goes. Ice melts on a warm day although melting absorbs heat, and a cold pack gets cold by itself. The missing piece is entropy, a measure of how widely energy and matter are spread out. Combining heat and entropy gives one number, the Gibbs free energy, whose sign tells you whether a process can run on its own at a given temperature. Its size tells you how far the process goes before it stops, through the equilibrium constant you will use in the rest of this module.

## Why it matters

Ammonia for fertiliser is made from nitrogen and hydrogen. The reaction gives out heat and, at room temperature, it is strongly favoured. Yet industry runs it at about 400–500 °C, where it is much less favoured, and pays for huge compressors. Why not just run it cold? And why does salt on an icy road melt the ice when the air is below 0 °C? Both answers come from the same equation, $\Delta G = \Delta H - T\Delta S$. Once you can use it, you can say in a minute whether a proposed reaction is worth trying at all, and at what temperature.

## Core ideas

> [!NOTE]
> Entropy, free energy and $\Delta G^\circ = -RT\ln K$ are settled physics. The table values are from OpenStax Chemistry 2e Appendix G (298.15 K, 1 bar) and $R$ = 8.314462618 J mol⁻¹ K⁻¹ is the CODATA 2022 value from NIST, both checked 2026-10-17. Treating $\Delta H$ and $\Delta S$ as constant with temperature is an approximation; Module 13 removes it.

### Spontaneous does not mean fast

A **spontaneous** process is one that can happen without being driven from outside, once it gets going. Iron rusting is spontaneous; so is diamond turning into graphite. Diamond still lasts for ever, because the reaction is extremely slow. Thermodynamics tells you *whether* and *how far*; kinetics (Module 22) tells you *how fast*. Keep them apart.

### Entropy: counting the ways

**Entropy**, $S$, measures how many microscopic arrangements (positions and energies of the molecules) are consistent with what you see. More arrangements, more entropy. In practice, entropy goes up when:

- a solid melts or a liquid evaporates (molecules move more freely; a gas has far more entropy than a liquid);
- a reaction makes more moles of gas than it uses;
- a solid dissolves and its ions spread through the water (usually);
- the temperature rises (energy can be shared among more levels).

Units are J mol⁻¹ K⁻¹: note **joules**, not kilojoules. Tables list **absolute** entropies $S^\circ$, measured from zero at 0 K for a perfect crystal (the third law), so elements do *not* have $S^\circ = 0$. The reaction entropy uses the same products-minus-reactants sum as lesson [08.1](lesson-01.md):

$$\Delta_r S^\circ = \sum_\text{products} \nu\,S^\circ - \sum_\text{reactants} \nu\,S^\circ$$

Tiny example, ammonia synthesis $\mathrm{N_2 + 3H_2 \rightarrow 2NH_3}$: $\Delta_r S^\circ = 2(192.8) - [191.6 + 3(130.7)] = -198.1$ J mol⁻¹ K⁻¹. Four moles of gas become two, so the entropy falls. The sign makes sense; always check that it does.

### The second law and the surroundings

The **second law** says that a spontaneous process increases the total entropy of the system plus its surroundings. A reaction that releases heat $-\Delta H$ to surroundings at temperature $T$ raises *their* entropy by $-\Delta H/T$. So the total entropy change is

$$\Delta S_\text{total} = \Delta S - \frac{\Delta H}{T}$$

Multiply by $-T$ and you get a quantity about the system alone. That is the **Gibbs free energy** change:

$$\Delta G = \Delta H - T\Delta S$$

At constant temperature and pressure, a process is spontaneous when $\Delta G < 0$, at equilibrium when $\Delta G = 0$, and runs the other way when $\Delta G > 0$. Here $T$ must be in **kelvin**, and $\Delta S$ must be turned into kJ before you subtract.

### Four sign cases

| $\Delta H$ | $\Delta S$ | $\Delta G = \Delta H - T\Delta S$ | Example |
|---|---|---|---|
| − | + | always negative: spontaneous at all T | burning fuel |
| + | − | always positive: never spontaneous | the reverse of burning |
| − | − | negative only at low T | ammonia synthesis, water freezing |
| + | + | negative only at high T | ice melting, NH₄NO₃ dissolving |

In the two mixed cases the sign changes at a **crossover temperature** where $\Delta G = 0$:

$$T^* = \frac{\Delta H}{\Delta S}$$

For water evaporating, $\Delta H = +44.0$ kJ/mol and $\Delta S = +118.8$ J mol⁻¹ K⁻¹ from the table, so $T^* = 44\,000 / 118.8 = 370$ K. The real boiling point is 373 K: the constant-$\Delta H$ approximation is good to a few kelvin.

### From free energy to the equilibrium constant

A reaction does not simply "go" or "not go". It runs until it reaches **equilibrium**, a mixture where the forward and backward tendencies balance. How far it runs is set by the **equilibrium constant** $K$ (lesson 08.3 defines it fully). The standard free energy fixes $K$:

$$\Delta G^\circ = -RT\ln K \qquad\Longleftrightarrow\qquad K = e^{-\Delta G^\circ/RT}$$

$RT$ at 298 K is 2.479 kJ/mol, so every 5.7 kJ/mol of $\Delta G^\circ$ changes $K$ by a factor of 10 (because $2.479 \times \ln 10 = 5.71$). A $\Delta G^\circ$ of −30 kJ/mol means $K \approx 10^5$: practically complete. +30 kJ/mol means $K \approx 10^{-5}$: practically nothing happens. Near zero, both sides are present in similar amounts. This is the same logarithm you met in lesson [02.1](../module-02/lesson-01.md), and the same $\Delta G = \Delta G^\circ + RT\ln Q$ you used for ATP in lesson [06.4](../module-06/lesson-04.md).

The superscript ° matters. $\Delta G^\circ$ is for every species in its standard state (1 bar, 1 mol/L). $\Delta G$ in a real mixture differs, and at equilibrium $\Delta G = 0$ while $\Delta G^\circ$ is whatever the table says.

### Why salt melts ice

Melting ice has $\Delta H = +6.01$ kJ/mol and $\Delta S = +22.0$ J mol⁻¹ K⁻¹, so $T^* = 273$ K: below 0 °C, ice wins. Dissolve salt in the meltwater and the liquid gains extra entropy of mixing, which lowers the free energy of the liquid. Now melting is spontaneous below 0 °C. But melting still needs 6.01 kJ per mole, and the only place to get it is the mixture itself. So an ice–salt mixture melts *and gets colder*, down towards about −21 °C, the lowest temperature at which salt water can stay liquid. You will measure this.

## Worked example

### 1. Ammonia: favoured cold, made hot

Use $\Delta_r H^\circ = 2(-45.9) = -91.8$ kJ/mol and $\Delta_r S^\circ = -198.1$ J mol⁻¹ K⁻¹ (above).

At 298 K: $\Delta G^\circ = -91.8 - 298.15 \times (-0.1981) = -91.8 + 59.1 = -32.7$ kJ/mol. Check against the table's $\Delta_f G^\circ$: $2(-16.5) = -33.0$ kJ/mol. Close.

$K = e^{32\,700/(8.314 \times 298.15)} = e^{13.2} = 5.4 \times 10^5$. Strongly favoured.

Both signs negative, so it is favoured only below $T^* = 91\,800 / 198.1 = 463$ K (190 °C). At 700 K, $\Delta G^\circ = -91.8 + 700 \times 0.1981 = +46.9$ kJ/mol and $K = 3 \times 10^{-4}$.

So why run hot? Because at room temperature the reaction is far too slow, even with a catalyst. Industry accepts a smaller $K$ for a usable rate, then pushes the yield back up with high pressure (lesson 08.3). Thermodynamics says what is possible; kinetics decides what is practical.

### 2. A cold pack that works at room temperature

Ammonium nitrate dissolving: $\Delta H^\circ = +28.1$ kJ/mol (lesson 08.1). Entropy: $S^\circ$ of NH₄⁺(aq) 113.4, NO₃⁻(aq) 146.4, NH₄NO₃(s) 151.08 J mol⁻¹ K⁻¹:

$$\Delta S^\circ = 113.4 + 146.4 - 151.08 = +108.7\ \text{J mol}^{-1}\text{K}^{-1}$$

$$\Delta G^\circ = 28.1 - 298.15 \times 0.1087 = 28.1 - 32.4 = -4.3\ \text{kJ/mol}$$

Negative: it dissolves on its own, although it absorbs heat. The entropy of the spreading ions pays for it. The crossover is $28\,100 / 108.7 = 258$ K: in a freezer at −15 °C, the standard-state dissolving would no longer be favoured.

## Hands-on

What you need: about 300 g of ice (crushed or small cubes), table salt, table sugar (optional), two plastic cups, a teaspoon, a kitchen scale, a digital kitchen or food thermometer that reads below −10 °C, a timer, the [Module 8 lab folder](../../labs/module-08/) with Python 3.14, and your notebook. Time: about 1 hour.

### Part A — home: an ice–salt freezing mixture (25 min)

> [!WARNING]
> An ice–salt mixture can reach −15 °C or lower. Do not hold it in a bare hand or press it against skin for more than a few seconds: it can cause a cold burn. Use a plastic cup, not thin glass. Wear safety glasses while crushing ice or stirring salt, and rinse salt out of eyes with plenty of water. Wash the thermometer probe before it touches food again.

1. Put about 150 g of ice in each cup. Add a few spoons of cold tap water to each so the probe touches wet ice. Stir and record the temperature of both. They should read close to 0 °C.
2. Cup 1 is the control: ice and water only. Into cup 2, add 50 g of salt and stir steadily.
3. Record both temperatures every 30 s for 6 minutes. Note what you see (melting, frost on the outside of the cup).
4. Optional: repeat cup 2 with 50 g of sugar instead of salt.
5. Plot temperature against time for each cup by hand or in Python, and record the lowest value.

How you know it worked: the control stays within about 1 °C of zero. The salt cup falls fast in the first two minutes and levels off somewhere between −10 °C and −20 °C, depending on how finely the ice is crushed and how well you stir. The outside of the cup frosts over.

<details><summary>Explaining your result</summary>

Melting is endothermic ($\Delta H = +6.01$ kJ/mol), and in the control it stops at 0 °C because there $\Delta G = 0$. Salt dissolving in the meltwater raises the entropy of the liquid, which makes $\Delta G$ for melting negative below 0 °C. The ice melts, and the heat for melting comes out of the mixture, so it cools. It cannot go below about −21 °C, where ice, salt and saturated brine coexist. Sugar works far less well per gram: what counts is the number of dissolved particles, and 50 g of sugar (342 g/mol, one particle) gives about 0.15 mol of particles, while 50 g of salt (58.4 g/mol, two ions) gives about 1.7 mol.

</details>

### Part B — pencil (15 min)

1. For $\mathrm{N_2O_4(g) \rightarrow 2NO_2(g)}$, $\Delta H^\circ = +55.3$ kJ/mol. With $S^\circ$ of NO₂ 240.1 and N₂O₄ 304.4 J mol⁻¹ K⁻¹, find $\Delta S^\circ$, $\Delta G^\circ$ at 298 K and $K$.
2. Above what temperature is the reaction in question 1 favoured?
3. Predict the sign of $\Delta S$ without numbers: (a) $\mathrm{CaCO_3(s) \rightarrow CaO(s) + CO_2(g)}$; (b) $\mathrm{2H_2(g) + O_2(g) \rightarrow 2H_2O(l)}$; (c) sugar dissolving in tea.
4. A reaction has $K = 1.0 \times 10^{-3}$ at 298 K. What is $\Delta G^\circ$?

<details><summary>Answers to Part B</summary>

1. $\Delta S^\circ = 2(240.1) - 304.4 = +175.8$ J mol⁻¹ K⁻¹; $\Delta G^\circ = 55.3 - 298.15 \times 0.1758 = +2.9$ kJ/mol; $K = e^{-2900/2479} = 0.31$. Slightly unfavoured: at 1 bar both gases are present, which is why the brown NO₂ colour never quite disappears.
2. $T^* = 55\,300 / 175.8 = 315$ K, about 42 °C. Above it, $K > 1$.
3. (a) positive, a gas forms from a solid; (b) negative, three moles of gas become liquid; (c) positive, the molecules spread through the tea.
4. $\Delta G^\circ = -RT\ln K = -2.479 \times \ln(10^{-3}) = +17.1$ kJ/mol.

</details>

### Part C — Python: ΔG against temperature (20 min)

Open `lesson02_free_energy.py` and write the three TODO functions: `delta_g`, `crossover_t` and `equilibrium_constant`. Then run:

```bash
py lesson02_free_energy.py
```

How you know it worked: the table prints, at 298 K, $\Delta G$ = −4.35 kJ/mol for NH₄NO₃ dissolving, −32.74 for NH₃ synthesis, +2.89 for N₂O₄ and +8.59 for water evaporation, each within 0.3 kJ/mol of the value from the $\Delta_f G^\circ$ column. Crossover temperatures are 258, 463, 315 and 370 K. A plot `runs/lesson02_dG_vs_T.png` shows four straight lines crossing zero. Look at the $K$ for water evaporation, 0.031: it is the vapour pressure of water at 25 °C in bar (the measured value is 0.032 bar). Record your results on a [notebook page](../../templates/notebook-page.md).

<details><summary>Reference solution</summary>

`delta_g`: `return dh_kj - t * ds_j / 1000`. `crossover_t`: `return None if dh_kj * ds_j <= 0 else dh_kj * 1000 / ds_j`. `equilibrium_constant`: `return float(np.exp(-dg_kj * 1000 / (R * t)))`. Full code in `lesson02_free_energy_solution.py`. The NH₃ table shows $K$ falling from 5.4 × 10⁵ at 298 K to 3 × 10⁻⁴ at 700 K: heat makes ammonia synthesis faster but less complete.

</details>

## Common mistakes

- **kJ and J mixed.** $\Delta H$ is in kJ/mol, $S$ in J mol⁻¹ K⁻¹. Writing $-91.8 - 298 \times (-198.1)$ gives +58 950, nonsense. Divide $\Delta S$ by 1000 first.
- **Celsius in $T\Delta S$ or $RT$.** Only kelvin. At 25 °C, $T$ = 298.15 K, not 25.
- **Giving elements $S^\circ = 0$.** That is true for $\Delta_f H^\circ$ and $\Delta_f G^\circ$, not for absolute entropy. O₂(g) has 205.2 J mol⁻¹ K⁻¹.
- **Reading "spontaneous" as "fast".** A negative $\Delta G$ says the process can run, not that it will run in your lifetime.
- **Confusing $\Delta G$ and $\Delta G^\circ$.** At equilibrium $\Delta G = 0$; $\Delta G^\circ$ is a fixed number for the reaction that tells you $K$.

## Key takeaways

- Entropy counts arrangements; it rises when gases form, solids melt or dissolve, and temperature rises. $\Delta_r S^\circ$ is products minus reactants, in J mol⁻¹ K⁻¹.
- $\Delta G = \Delta H - T\Delta S$; a process is spontaneous when $\Delta G < 0$. Use kelvin and convert J to kJ.
- When $\Delta H$ and $\Delta S$ have the same sign, temperature decides, and the switch is at $T^* = \Delta H/\Delta S$.
- $\Delta G^\circ = -RT\ln K$: each 5.7 kJ/mol at 298 K is a factor of 10 in $K$.
- Thermodynamics says whether and how far; kinetics says how fast. Ammonia synthesis is run hot for speed, not for yield.

## Sources

- [OpenStax Chemistry 2e, 16.2 Entropy](https://openstax.org/books/chemistry-2e/pages/16-2-entropy) — entropy as a count of microstates; when entropy increases.
- [OpenStax Chemistry 2e, 16.3 The Second and Third Laws](https://openstax.org/books/chemistry-2e/pages/16-3-the-second-and-third-laws-of-thermodynamics) — total entropy, absolute entropies, $\Delta_r S^\circ$.
- [OpenStax Chemistry 2e, 16.4 Free Energy](https://openstax.org/books/chemistry-2e/pages/16-4-free-energy) — $\Delta G = \Delta H - T\Delta S$, the four sign cases, $\Delta G^\circ = -RT\ln K$.
- [OpenStax Chemistry 2e, Appendix G](https://openstax.org/books/chemistry-2e/pages/g-standard-thermodynamic-properties-for-selected-substances) — all $\Delta_f H^\circ$, $\Delta_f G^\circ$ and $S^\circ$ values used here.
- [NIST CODATA, molar gas constant](https://physics.nist.gov/cgi-bin/cuu/Value?r) — $R$ = 8.314462618 J mol⁻¹ K⁻¹ (exact).
