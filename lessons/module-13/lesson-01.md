---
id: "13.1"
module: 13
minutes: 22
practice_minutes: 75
prerequisites: ["08.1", "02.5", "07.6", "04.1"]
objectives:
  - Classify a quantity as a state function or a path function, and test a differential for exactness with mixed partial derivatives.
  - Apply the first law, ΔU = q + w, with the IUPAC sign convention to compression, expansion and heating of an ideal gas.
  - Calculate the work of a reversible and of a one-step isothermal compression, and of a reversible adiabatic compression, and explain why they differ.
  - Measure a p–V isotherm with a sealed syringe and a kitchen scale and get the work from the area under it.
volatility: concept
sources:
  - title: "MIT OpenCourseWare 5.60 Thermodynamics and Kinetics (Spring 2008), lecture notes"
    url: https://ocw.mit.edu/courses/5-60-thermodynamics-kinetics-spring-2008/pages/lecture-notes/
  - title: "OpenStax University Physics Volume 2, 3.2 Work, Heat, and Internal Energy"
    url: https://openstax.org/books/university-physics-volume-2/pages/3-2-work-heat-and-internal-energy
  - title: "OpenStax University Physics Volume 2, 3.6 Adiabatic Processes for an Ideal Gas"
    url: https://openstax.org/books/university-physics-volume-2/pages/3-6-adiabatic-processes-for-an-ideal-gas
  - title: "IUPAC Green Book: Quantities, Units and Symbols in Physical Chemistry"
    url: https://iupac.org/what-we-do/books/greenbook/
  - title: "NIST CODATA value: molar gas constant"
    url: https://physics.nist.gov/cgi-bin/cuu/Value?r
last_verified: "2026-10-17"
---

# 13.1 · Systems, state functions and the first law

Module 8 used heat and enthalpy as tools. This module builds them from the ground up, so that you can trust them at any temperature and pressure. The first step is bookkeeping: say exactly what your system is, which quantities belong to its state and which describe only the path it took, and how energy enters as heat or as work. The first law of thermodynamics is that bookkeeping rule. You will test it at home by squeezing the air in a sealed syringe on a kitchen scale and measuring the work you did.

## Why it matters

A diving shop fills a scuba tank to 200 bar, and the tank gets hot. A diesel engine squeezes air so fast that it ignites the fuel without a spark plug. How much energy does each compression take, and where does it go? The answer depends on *how* you compress: fast or slow, in one push or gently. Engineers who size compressors and chemists who run high-pressure reactors use the same few lines of algebra you will learn here, and one sign error puts an energy budget out by a factor of two.

## Core ideas

> [!NOTE]
> The first law, state functions and the work formulas are settled physics (MIT 5.60 scope). The sign convention is the IUPAC one ($w$ = work done *on* the system), checked against the IUPAC Green Book on 2026-10-17. Some physics and engineering books write $\Delta U = q - w$ with $w$ done *by* the system; the physics is the same, only the sign of $w$ flips. $R$ = 8.314462618 J mol⁻¹ K⁻¹ is the exact CODATA 2022 value from NIST.

### System, surroundings and boundary

The **system** is the part of the world you choose to study; everything else is the **surroundings**; the **boundary** separates them. You choose it, and the choice changes what counts as heat and work. An **open** system exchanges matter and energy (a boiling pan). A **closed** system exchanges energy only (the sealed syringe). An **isolated** system exchanges neither (a perfect thermos, an approximation).

The **state** of a simple system is fixed by a few **state variables**: $n$, $p$, $V$, $T$. **Extensive** quantities scale with the amount ($V$, $U$); **intensive** ones do not ($p$, $T$, molar volume $V_m = V/n$).

### State functions and path functions

A **state function** depends only on the present state, not on how the system got there: $U$, $H$, $p$, $V$, $T$, and (lesson 13.3) $S$. Altitude is the analogy: the climb from the bottom to the top of Masada is the same by cable car or by the snake path.

**Heat** $q$ and **work** $w$ are **path functions**. They are not things a system *has*; they are energy *in transit* across the boundary, like the distance walked up Masada. Small amounts are written $\delta q$ and $\delta w$, not $dq$, as a reminder.

There is a mathematical test, and it is the mixed-partials rule from lesson [02.5](../module-02/lesson-05.md). A differential $dz = M\,dx + N\,dy$ is **exact** (belongs to a state function $z$) only if

$$\left(\frac{\partial M}{\partial y}\right)_x = \left(\frac{\partial N}{\partial x}\right)_y$$

For an ideal gas $V = nRT/p$, so $dV = (nR/p)\,dT - (nRT/p^2)\,dp$. Check: $\partial(nR/p)/\partial p = -nR/p^2$ and $\partial(-nRT/p^2)/\partial T = -nR/p^2$. Equal, so $V$ is a state function, as it must be. Now try the work $\delta w = -p\,dV$ written in $T$ and $p$: $\delta w = -nR\,dT + (nRT/p)\,dp$. The cross derivatives are $0$ and $nR/p$. Not equal: work is not a state function.

### The first law

The **internal energy** $U$ is the total energy of the molecules inside the system: their motion, rotation, vibration and the energy of their bonds and attractions. The first law says energy is conserved, so $U$ changes only by what crosses the boundary:

$$\Delta U = q + w$$

Here $q > 0$ when heat flows *into* the system and $w > 0$ when work is done *on* it (you compress it). For an isolated system $q = w = 0$, so $\Delta U = 0$. You met energy conservation in lesson [04.1](../module-04/lesson-01.md); this is the same law with heat added.

### Pressure–volume work

When the boundary moves against an external pressure $p_\text{ext}$, the work done on the gas is

$$\delta w = -p_\text{ext}\,dV \qquad w = -\int_{V_1}^{V_2} p_\text{ext}\,dV$$

Compression ($dV < 0$) gives $w > 0$. Two limiting paths matter.

**One step against a constant pressure.** Push suddenly with a constant outside pressure $p_\text{ext}$: $w = -p_\text{ext}(V_2 - V_1)$.

**Reversible.** Push so slowly that the outside pressure is always only infinitesimally above the gas pressure, $p_\text{ext} = p$. For an ideal gas at constant $T$, $p = nRT/V$, and the integral (lesson [02.3](../module-02/lesson-03.md)) gives

$$w_\text{rev} = -nRT\ln\frac{V_2}{V_1}$$

The figure shows both paths between the same two states. The work is the area under the path on a $p$–$V$ plot. For compression, the reversible path needs the *least* work; any real, faster push needs more. For expansion it is the other way round: a reversible expansion gets the *most* work out.

![Pressure against volume for compressing an ideal gas from V1 to V2 at constant temperature. The reversible path follows the curved isotherm and its work is the shaded area under it; the one-step path at the final pressure p2 encloses a larger rectangle, so it needs more work.](../../assets/m13-pv-work.svg)

### Ideal gas: U depends on T only

The molecules of an ideal gas do not attract each other, so their energy does not depend on how far apart they are. $U$ of an ideal gas depends only on $T$. Two consequences:

- **Isothermal** (constant $T$): $\Delta U = 0$, so $q = -w$. Every joule you push in as work leaves as heat to the surroundings. That is why you must compress slowly, with time for heat to leak out, to stay at constant $T$.
- **Adiabatic** (no heat, $q = 0$): $\Delta U = w$. The work stays inside and the gas warms. For a reversible adiabatic change of an ideal gas, $\Delta U = nC_V\,dT$ and $-p\,dV$ combine to

$$T V^{\gamma - 1} = \text{const}, \qquad pV^\gamma = \text{const}, \qquad \gamma = \frac{C_p}{C_V}$$

For air (mostly N₂ and O₂), $C_V \approx \tfrac{5}{2}R$ and $\gamma \approx 1.40$ near room temperature. Lesson 13.2 explains where these heat capacities come from. A fast bicycle pump is nearly adiabatic; a slow syringe on the kitchen table is nearly isothermal.

## Worked example

### 1. Same start, same end, different work

One mole of ideal gas at 298.15 K and 1.000 bar is compressed at constant temperature to 2.000 bar.

Volumes: $V_1 = RT/p_1 = 8.3145 \times 298.15 / 1.000\times10^5 = 0.02479$ m³ (24.79 L), and $V_2 = 12.39$ L.

Reversible: $w = -RT\ln(V_2/V_1) = RT\ln 2 = 2479 \times 0.6931 = +1718$ J.

One step, the piston pushed by a constant 2.000 bar: $w = -p_\text{ext}(V_2 - V_1) = 2.000\times10^5 \times 0.01239 = +2479$ J.

In both cases $\Delta U = 0$ (ideal gas, same $T$), so $q = -w$: the gas gives out 1718 J of heat on the reversible path and 2479 J on the fast one. Same initial and final state, same $\Delta U$, different $q$ and $w$. That is what "path function" means. The extra 761 J of the fast push is not lost from the universe; it ends up as extra heat in the surroundings, and lesson 13.3 will show it as entropy created.

### 2. Why a pump gets hot

Now compress one mole of air from 298.15 K and 1 bar to half its volume, so fast that no heat escapes (reversible adiabatic, $\gamma = 1.40$, $C_V = \tfrac{5}{2}R = 20.79$ J mol⁻¹ K⁻¹).

$$T_2 = T_1\left(\frac{V_1}{V_2}\right)^{\gamma-1} = 298.15 \times 2^{0.40} = 393.4\ \text{K} \quad (120\ ^\circ\text{C})$$

$$w = \Delta U = nC_V\,\Delta T = 20.79 \times 95.3 = +1981\ \text{J}, \qquad p_2 = p_1\, 2^{1.40} = 2.64\ \text{bar}$$

The air reaches 120 °C in a single halving of volume. A diesel engine compresses by a factor of about 16–20, which gives $298 \times 16^{0.40} \approx 900$ K, hot enough to ignite the fuel. A real pump stays cooler because heat leaks into the metal: it is between the two limits.

## Hands-on

What you need: a 10 mL plastic oral syringe (from your Module 1 kit) with its cap, or a small piece of eraser to seal the nozzle; a kitchen scale (up to at least 3 kg); a ruler; your phone (a barometer app such as [phyphox](https://phyphox.org/) if your phone has a pressure sensor) or the station pressure from a nearby weather station; the [Module 13 lab folder](../../labs/module-13/) with Python 3.14. Time: about 75 minutes.

### Part A — home: a p–V isotherm with a syringe (35 min)

> [!WARNING]
> Use a plastic syringe, never glass. Keep the nozzle pointing down onto the scale, away from your face, and wear safety glasses: a cap can pop off under pressure. Do not push harder than about 3 kg on the scale; stop at the 5 mL mark. If the plunger jumps, let go slowly. Do not use a syringe that has held medicine or anything other than clean water.

1. Pull the plunger to exactly 10 mL of air. Seal the nozzle with the cap (or press it firmly into the eraser). Measure with the ruler the length of the barrel between the 0 and 10 mL marks; the inner area is $A = 10\ \text{mL} / \text{length}$.
2. Stand the syringe nozzle-down on the scale (on the eraser if you use one) and press **tare**.
3. Press the plunger down slowly to 9, 8, 7, 6 and 5 mL. At each mark, hold still for 5 seconds and record the scale reading in grams. This is the "in" series.
4. Now let the plunger rise slowly through 6, 7, 8, 9 and 10 mL, recording again. This is the "out" series. The two series differ because friction always opposes the motion; averaging them cancels it.
5. Record the room pressure. Type your readings into a file `my_syringe.csv` with the header `direction,V_mL,scale_g` (see `syringe_example.csv`).

How you know it worked: the readings rise smoothly to roughly 1.5–1.8 kg at 5 mL, the "in" readings are above the "out" readings at every mark, and the scale goes back to near zero at 10 mL (if not, the seal leaks; reseal and repeat).

### Part B — Python: Boyle's law and the work (25 min)

Open `lesson01_work.py` and write the three TODO functions: `pressure_from_scale` (absolute pressure $p = p_\text{atm} + mg/A$), `work_on_gas_trapezoid` ($w = -\int p\,dV$ with `np.trapezoid`) and `work_isothermal_reversible`. Edit the setup block first: your scale length, room pressure and an estimate of the air trapped in the nozzle below the 0 mark (about 0.15 mL). Then run it on the example data and on yours:

```bash
py lesson01_work.py
py lesson01_work.py my_syringe.csv
```

How you know it worked: on the example data, $pV$ is constant to within 0.5 %, the measured work on the gas is 0.697 J and equals the reversible isothermal value $p_1V_1\ln(V_1/V_2)$, and the friction comes out at about 1.2 N. Your own data should give $pV$ constant within a few per cent and work near 0.7 J. The script also splits the work: about 0.50 J was done by the atmosphere pushing on the plunger and only about 0.19 J by your hand. Record the results on a [notebook page](../../templates/notebook-page.md).

<details><summary>Reference solution and interpretation</summary>

`pressure_from_scale`: `return p_atm + grams / 1000 * G / area`. `work_on_gas_trapezoid`: `return float(-np.trapezoid(p_pa, v_m3))`. `work_isothermal_reversible`: `return -p1 * v1 * math.log(v2 / v1)`. Full code in `lesson01_work_solution.py`.

Measured equals reversible because you pushed slowly and paused, so heat leaked out and the gas stayed at room temperature, and averaging "in" and "out" removed friction, the irreversible part. With the gas as the system, the work on it is $-\int p\,dV$ with the full gas pressure; the atmosphere supplies $p_\text{atm}\,|\Delta V|$ of it and your hand the rest. The one-step value (about 1.0 J) is what a sudden push against the final pressure would cost.

</details>

### Part C — pencil (15 min)

1. 2.00 mol of ideal gas expands isothermally at 350 K from 10.0 L to 30.0 L, (a) reversibly and (b) against a constant 1.00 bar. Find $w$, $q$ and $\Delta U$ for each.
2. Is $\delta z = 2xy\,dx + x^2\,dy$ exact? Is $\delta z = xy\,dx + x^2\,dy$?

<details><summary>Answers to Part C</summary>

1. (a) $w = -nRT\ln(V_2/V_1) = -2.00 \times 8.3145 \times 350 \times \ln 3 = -6394$ J; $\Delta U = 0$; $q = +6394$ J. (b) $w = -p_\text{ext}\Delta V = -1.00\times10^5 \times 0.0200 = -2000$ J; $\Delta U = 0$; $q = +2000$ J. The reversible expansion gets more than three times as much work out.
2. First: $\partial(2xy)/\partial y = 2x$ and $\partial(x^2)/\partial x = 2x$, exact ($z = x^2 y$). Second: $x$ against $2x$, not exact.

</details>

Optional: in the simulation, compress an ideal gas slowly and quickly and compare the work shown with your syringe numbers.

[Simulation: Gas laws — ideal gas](../../simulations/gas-laws/index.html?preset=ideal)

## Common mistakes

- **Mixing sign conventions.** Chemistry (IUPAC) uses $\Delta U = q + w$ with $w$ on the system. If a book writes $q - w$, its $w$ is work *by* the system. Pick one and write it at the top of your page.
- **Using $p$ instead of $p_\text{ext}$ for a fast process.** Only a reversible process lets you put the gas pressure into $-\int p\,dV$. For a sudden push, use the outside pressure.
- **Calling heat a property.** "The gas contains 500 J of heat" is meaningless; it contains internal energy. Heat and work exist only while crossing the boundary.
- **Gauge pressure in $pV = nRT$.** The scale measures pressure *above* the room's. Add atmospheric pressure before using Boyle's law.

## Key takeaways

- Choose the system and boundary first; the choice decides what counts as heat and as work.
- $U$, $H$, $p$, $V$, $T$ are state functions; $q$ and $w$ depend on the path. Mixed partials test exactness.
- First law: $\Delta U = q + w$, with $w > 0$ when work is done on the system and $\delta w = -p_\text{ext}\,dV$.
- Reversible isothermal ideal gas: $w = -nRT\ln(V_2/V_1)$. Compressing reversibly takes the least work; expanding reversibly gives the most.
- For an ideal gas, isothermal means $q = -w$; adiabatic means $\Delta U = w$ and $TV^{\gamma-1}$ = const, which is why fast compression heats a gas.

## Sources

- [MIT OpenCourseWare 5.60 Thermodynamics and Kinetics, lecture notes](https://ocw.mit.edu/courses/5-60-thermodynamics-kinetics-spring-2008/pages/lecture-notes/) — state functions, exact differentials, first law, reversible and irreversible work, adiabatic ideal gas.
- [OpenStax University Physics Volume 2, 3.2 Work, Heat, and Internal Energy](https://openstax.org/books/university-physics-volume-2/pages/3-2-work-heat-and-internal-energy) — work as area under a p–V curve; heat and work as path quantities.
- [OpenStax University Physics Volume 2, 3.6 Adiabatic Processes for an Ideal Gas](https://openstax.org/books/university-physics-volume-2/pages/3-6-adiabatic-processes-for-an-ideal-gas) — $pV^\gamma$ = const and the adiabatic temperature rise.
- [IUPAC Green Book](https://iupac.org/what-we-do/books/greenbook/) — symbols and the sign convention $\Delta U = q + w$.
- [NIST CODATA, molar gas constant](https://physics.nist.gov/cgi-bin/cuu/Value?r) — $R$ = 8.314462618 J mol⁻¹ K⁻¹ (exact).
