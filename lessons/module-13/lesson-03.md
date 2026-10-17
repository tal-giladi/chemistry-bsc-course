---
id: "13.3"
module: 13
minutes: 22
practice_minutes: 60
prerequisites: ["13.2", "08.2"]
objectives:
  - Calculate entropy changes for heating, phase changes, isothermal gas expansion and mixing from dS = δq_rev/T.
  - Use the total entropy change of system plus surroundings to decide whether a process is reversible, irreversible or impossible.
  - State the Carnot limit on a heat engine and calculate it for given temperatures.
  - Check that entropy is a state function by computing the entropy of vaporisation of water by two routes from NIST data.
volatility: concept
sources:
  - title: "MIT OpenCourseWare 5.60 Thermodynamics and Kinetics (Spring 2008), lecture notes"
    url: https://ocw.mit.edu/courses/5-60-thermodynamics-kinetics-spring-2008/pages/lecture-notes/
  - title: "OpenStax University Physics Volume 2, 4.5 The Carnot Cycle"
    url: https://openstax.org/books/university-physics-volume-2/pages/4-5-the-carnot-cycle
  - title: "OpenStax University Physics Volume 2, 4.6 Entropy"
    url: https://openstax.org/books/university-physics-volume-2/pages/4-6-entropy
  - title: "NIST Chemistry WebBook: Water (gas and condensed phase thermochemistry, phase change data)"
    url: https://webbook.nist.gov/cgi/cbook.cgi?ID=C7732185&Mask=7
  - title: "OpenStax Chemistry 2e, 10.3 Phase Transitions"
    url: https://openstax.org/books/chemistry-2e/pages/10-3-phase-transitions
last_verified: "2026-10-17"
---

# 13.3 · The second law and entropy

The first law says energy is conserved, but it does not say which way things go: heat flowing from a cold spoon into hot tea would conserve energy just as well. The second law supplies the direction, through entropy. In lesson 08.2 you used tabulated entropies; here you will learn how they are measured, how to calculate entropy changes for heating, boiling, expanding and mixing, and why every real process creates entropy. At home you will feel entropy at work in a rubber band.

## Why it matters

A power station burns gas at about 1500 °C and turns at best roughly 60 % of the heat into electricity; the rest warms a river or the air. Is that bad engineering? Partly no: the second law sets an upper limit that depends only on the hot and cold temperatures, and no design can beat it. The same law tells a chemist why a mixture never unmixes by itself, why a fast compression wastes work, and how to get the absolute entropies in every table from heat-capacity measurements alone.

## Core ideas

> [!NOTE]
> The second and third laws are settled physics (MIT 5.60 scope). Water data are from the NIST Chemistry WebBook (CODATA Key Values for $\Delta_f H^\circ$ and $S^\circ$; Antoine coefficients for vapour pressure), checked 2026-10-17. The statistical meaning of entropy, $S = k_\text{B}\ln W$, is developed in Module 21.

### Entropy from reversible heat

**Entropy** $S$ is a state function defined through heat exchanged *reversibly*:

$$dS = \frac{\delta q_\text{rev}}{T}$$

Even if the real process is fast and messy, you find $\Delta S$ of the system by inventing *any* reversible path between the same two states and adding up $\delta q_\text{rev}/T$ along it. Since $S$ is a state function, the answer is the same for every path. Four paths cover most of chemistry.

**Heating at constant pressure.** $\delta q_\text{rev} = C_p\,dT$, so

$$\Delta S = \int_{T_1}^{T_2}\frac{C_p}{T}\,dT \approx C_p \ln\frac{T_2}{T_1}\quad(\text{constant } C_p)$$

Warming 1 mol of liquid water from 25 °C to 100 °C: $75.3 \times \ln(373.15/298.15) = +16.9$ J mol⁻¹ K⁻¹.

**A phase change at its equilibrium temperature.** Heat flows at constant $T$, so $\Delta S = \Delta H_\text{trs}/T_\text{trs}$. Boiling water at 100 °C: $40\,670 / 373.15 = +109.0$ J mol⁻¹ K⁻¹. Melting ice at 0 °C: $6010 / 273.15 = +22.0$ J mol⁻¹ K⁻¹.

**Isothermal ideal gas.** $\Delta U = 0$, so $q_\text{rev} = -w_\text{rev} = nRT\ln(V_2/V_1)$ and

$$\Delta S = nR\ln\frac{V_2}{V_1} = -nR\ln\frac{p_2}{p_1}$$

**Mixing ideal gases** (or ideal solutions). Each component expands into the whole volume, so for total amount $n$ with mole fractions $x_i$:

$$\Delta_\text{mix}S = -nR\sum_i x_i \ln x_i$$

Mixing equal amounts gives $R\ln 2 = 5.76$ J K⁻¹ per mole of mixture. It is always positive, which is why mixtures never unmix by themselves.

### The second law: total entropy never falls

The **second law** in Clausius's form says that for any change, $dS \geq \delta q/T$, with equality only for a reversible change. For an **isolated** system ($q = 0$) this means $\Delta S \geq 0$. Taking the system and its surroundings together as one isolated whole:

$$\Delta S_\text{total} = \Delta S_\text{sys} + \Delta S_\text{surr} \;\begin{cases} > 0 & \text{irreversible (it happens)} \\ = 0 & \text{reversible (the limit)} \\ < 0 & \text{impossible} \end{cases}$$

The surroundings are usually a big reservoir at constant $T$, so $\Delta S_\text{surr} = -q_\text{sys}/T$, the heat they receive divided by their temperature.

Go back to the compressions in lesson [13.1](lesson-01.md), 1 mol from 1 to 2 bar at 298.15 K. Both paths have $\Delta S_\text{sys} = -R\ln 2 = -5.76$ J/K. Reversibly, the surroundings receive 1718 J: $+5.76$ J/K, total zero. In one push they receive 2479 J: $+8.31$ J/K, total $+2.55$ J/K. The extra work of the fast push became entropy created. This is what "irreversible" means.

### Heat engines and the Carnot limit

A **heat engine** takes heat $q_h$ from a hot reservoir at $T_h$, turns part into work, and dumps $q_c$ into a cold reservoir at $T_c$. For one full cycle the engine's own entropy returns to its start value, so the reservoirs must not lose entropy overall: $q_c/T_c \geq q_h/T_h$. The best possible efficiency, reached by a reversible (Carnot) engine, is

$$\eta_\text{max} = \frac{w}{q_h} = 1 - \frac{T_c}{T_h}$$

with kelvin temperatures. A steam turbine with steam at 800 K and a river at 300 K: $\eta_\text{max} = 1 - 300/800 = 62.5$ %. Real turbines reach about 40 %; combined-cycle gas plants push the hot side higher to approach 60 %. A refrigerator and a heat pump are the same cycle run backwards.

### The third law and absolute entropies

The **third law** says the entropy of a perfect crystal is zero at 0 K. That gives entropy an absolute zero point, which enthalpy lacks. To get $S^\circ$ at 298 K, measure $C_p$ from near 0 K upwards and add every phase change:

$$S^\circ(T) = \int_0^{T}\frac{C_p}{T}\,dT + \sum_\text{transitions}\frac{\Delta H_\text{trs}}{T_\text{trs}}$$

That is how the $S^\circ$ column of the tables you used in lesson [08.2](../module-08/lesson-02.md) was made: by careful heat-capacity measurements, not by theory. (Below about 10 K, where it is hard to measure, the Debye law $C_p \propto T^3$ fills the gap.)

### Entropy you can feel: a rubber band

Rubber is a tangle of long, flexible polymer chains. Stretched, the chains straighten and line up: fewer possible shapes, lower **conformational entropy**. Stretch it *fast*, so no heat leaves (adiabatic, close to reversible), and the total entropy of the band cannot change. The lost shape entropy must reappear as thermal entropy: the band warms up. Let it contract fast and it cools. This is the opposite of a metal spring, whose energy is stored in stretched bonds, and it is why a rubber band under load shortens, not lengthens, when you heat it.

## Worked example

### 1. Mixing hot and cold water

You pour 100.0 g of water at 60.0 °C into 100.0 g at 20.0 °C in an insulated cup ($c$ = 4.184 J g⁻¹ K⁻¹). Energy balance: equal masses, so $T_f$ = 40.0 °C = 313.15 K. No heat leaves the cup, so the whole cup is an isolated system, and its entropy change is the total.

$$\Delta S_\text{hot} = 100.0 \times 4.184 \times \ln\frac{313.15}{333.15} = -25.90\ \text{J/K}$$

$$\Delta S_\text{cold} = 100.0 \times 4.184 \times \ln\frac{313.15}{293.15} = +27.61\ \text{J/K}$$

$$\Delta S_\text{total} = +1.71\ \text{J/K} > 0$$

The cold water gains more entropy than the hot water loses, because the same heat counts for more at a lower temperature ($q/T$). The reverse, warm water separating into a hot and a cold half, would have $\Delta S_\text{total} = -1.71$ J/K: allowed by the first law, forbidden by the second.

### 2. Entropy of vaporisation by two routes

The tables give $S^\circ$(H₂O, g) = 188.835 and $S^\circ$(H₂O, l) = 69.95 J mol⁻¹ K⁻¹ at 298.15 K, so $\Delta_\text{vap}S^\circ = 118.89$ J mol⁻¹ K⁻¹. This refers to liquid going to vapour *at 1 bar*, a state that cannot be in equilibrium with liquid at 25 °C. Build a reversible path instead:

1. Evaporate at the equilibrium vapour pressure, $p_\text{sat}$ = 0.03167 bar at 298.15 K (NIST Antoine equation). This is reversible, so $\Delta S_1 = \Delta_\text{vap}H/T = 44\,004 / 298.15 = +147.59$ J mol⁻¹ K⁻¹, with $\Delta_\text{vap}H = -241.826 - (-285.830) = 44.004$ kJ/mol.
2. Compress the vapour isothermally from 0.03167 to 1 bar: $\Delta S_2 = -R\ln(1/0.03167) = -28.71$ J mol⁻¹ K⁻¹.

Sum: $+118.88$ J mol⁻¹ K⁻¹, the table value to 0.01. Three independent NIST measurements (two enthalpies of formation, a vapour pressure curve) and two absolute entropies agree, because entropy is a state function.

## Hands-on

What you need: a wide rubber band (the flat kind used for parcels); two mugs, a kitchen scale, a digital kitchen thermometer, a kettle, tap water and a lid or plate; the [Module 13 lab folder](../../labs/module-13/) with Python 3.14; your notebook. Time: about 60 minutes.

### Part A — home: a rubber band heat engine you can feel (10 min)

> [!WARNING]
> A stretched rubber band can snap and hit an eye: wear safety glasses, stretch it away from your face and stop well before it is at full stretch. Use a clean band, touch it only briefly to your lips or forehead, and do not use a latex band if you are allergic to latex.

1. Touch the relaxed band to your upper lip or forehead (both are sensitive to small temperature changes) and note how it feels.
2. Stretch it quickly to about twice its length and immediately touch the stretched middle to your lip. Note the feeling.
3. Hold it stretched for about 20 seconds (it returns to room temperature), then let it contract quickly and touch it again.

How you know it worked: the band feels distinctly warm right after a fast stretch and cool right after a fast release.

<details><summary>Explaining your result</summary>

A fast stretch is nearly adiabatic and nearly reversible, so the band's entropy stays roughly constant. Straightening the chains lowers their conformational entropy; to compensate, the thermal (vibrational) entropy rises, and the band warms. While you hold it, heat leaks to the air and it returns to room temperature at the lower entropy. A fast release reverses the process: the chains regain their freedom, and the thermal entropy falls, so the band cools. Run stretch–hold–release–hold as a cycle and you have a (very feeble) heat engine.

</details>

### Part B — home: mixing hot and cold water (20 min)

> [!WARNING]
> Hot water scalds. Use water no hotter than about 60 °C (kettle water mixed with cold), pour slowly, keep children away and put mugs on a stable surface.

1. Weigh 100 g of cold tap water into mug 1 and record its temperature. Weigh 100 g of water at about 60 °C into mug 2 and record its temperature.
2. Pour mug 2 into mug 1, cover, stir gently with the thermometer for 30 s and record the final temperature.
3. Put your three temperatures in the setup block of `lesson03_entropy.py` (Part C).

How you know it worked: the final temperature is within 1–3 °C below the simple average; the lost heat went into the mug and air. The script prints the ideal final temperature and $\Delta S_\text{total}$, about +1.7 J/K for 60 °C and 20 °C.

### Part C — Python: three entropy calculations (30 min)

Open `lesson03_entropy.py` and write the three TODO functions: `ds_heating` (integrate $C_p/T$ with `scipy.integrate.quad`), `ds_isothermal_ideal_gas` and `mixing`. Then run:

```bash
py lesson03_entropy.py
```

How you know it worked: part 1 prints a final temperature of 40.00 °C and $\Delta S_\text{total}$ = +1.71 J/K for the example numbers; part 2 gives 16.93 J mol⁻¹ K⁻¹ for heating liquid water from 298.15 to 373.15 K with the NIST $C_p(T)$ (the constant-$C_p$ estimate is within 0.02); part 3 prints 118.89 by both routes. Record your mixing result on a [notebook page](../../templates/notebook-page.md).

<details><summary>Reference solution</summary>

`ds_heating`: `value, _ = quad(lambda t: cp_func(t) / t, t1, t2)` then `return value`. `ds_isothermal_ideal_gas`: `return -n * R * math.log(p2 / p1)`. `mixing`: `t_f = (m_hot * t_hot_k + m_cold * t_cold_k) / (m_hot + m_cold)`, then `m * c * math.log(t_f / t)` for each sample and their sum. Full code in `lesson03_entropy_solution.py`.

</details>

Pencil, 5 minutes: a heat pump keeps a house at 21 °C when it is 5 °C outside. What is the most heat it can deliver per joule of electricity? (Answer: run backwards, the Carnot limit gives $q_h/w = T_h/(T_h - T_c) = 294.15/16 = 18$. Real units reach about 3–5.)

## Common mistakes

- **Using the real (irreversible) heat in $\Delta S = q/T$.** Only reversible heat counts. Find a reversible path between the same states.
- **Celsius in $\ln(T_2/T_1)$ or in $1 - T_c/T_h$.** Both need kelvin; $\ln(100/25)$ is nonsense.
- **"Entropy of the system always increases."** Only the *total* (or that of an isolated system) must. Water freezing in a freezer lowers its own entropy; the freezer's surroundings gain more.
- **Treating $\Delta S_\text{surr}$ as zero.** In open air or a water bath it is $-q_\text{sys}/T$, and it is often the larger term.
- **Forgetting that $S^\circ$ refers to 1 bar.** A gas at another pressure has $S = S^\circ - R\ln(p/p^\circ)$.

## Key takeaways

- $dS = \delta q_\text{rev}/T$. Heating: $\int C_p/T\,dT$. Phase change: $\Delta H/T$. Ideal gas: $-nR\ln(p_2/p_1)$. Mixing: $-nR\sum x_i\ln x_i$.
- $\Delta S_\text{total} > 0$ for every real process, $= 0$ only in the reversible limit; the extra work of an irreversible process becomes entropy.
- No heat engine beats $\eta = 1 - T_c/T_h$.
- The third law fixes $S = 0$ for a perfect crystal at 0 K, so absolute entropies come from heat-capacity measurements.
- Entropy is a state function: two routes to $\Delta_\text{vap}S^\circ$ of water from NIST data agree to 0.01 J mol⁻¹ K⁻¹.

## Sources

- [MIT OpenCourseWare 5.60, lecture notes](https://ocw.mit.edu/courses/5-60-thermodynamics-kinetics-spring-2008/pages/lecture-notes/) — Clausius inequality, entropy calculations, Carnot cycle, third law.
- [OpenStax University Physics Volume 2, 4.5 The Carnot Cycle](https://openstax.org/books/university-physics-volume-2/pages/4-5-the-carnot-cycle) — Carnot efficiency and heat pumps.
- [OpenStax University Physics Volume 2, 4.6 Entropy](https://openstax.org/books/university-physics-volume-2/pages/4-6-entropy) — $dS = \delta q_\text{rev}/T$ and entropy changes of irreversible processes.
- [NIST Chemistry WebBook: Water](https://webbook.nist.gov/cgi/cbook.cgi?ID=C7732185&Mask=7) — $\Delta_f H^\circ$ and $S^\circ$ for liquid and gas (CODATA), liquid $C_p$ Shomate fit, Antoine vapour-pressure coefficients.
- [OpenStax Chemistry 2e, 10.3 Phase Transitions](https://openstax.org/books/chemistry-2e/pages/10-3-phase-transitions) — $\Delta_\text{vap}H$ = 40.67 kJ/mol at 100 °C and $\Delta_\text{fus}H$ = 6.01 kJ/mol.
