---
id: "01.2"
module: 1
minutes: 20
practice_minutes: 60
prerequisites: ["01.1"]
objectives:
  - Name the seven SI base units and explain how they have been defined since 2019.
  - Convert between units with prefixes and the factor-label method, writing units on every line.
  - Round results correctly for multiplication, division, addition and subtraction.
  - Find a unit error in a calculation by checking that the units on both sides agree.
volatility: concept
sources:
  - title: "BIPM — The International System of Units (SI Brochure, 9th edition)"
    url: https://www.bipm.org/en/publications/si-brochure
  - title: "BIPM — SI defining constants"
    url: https://www.bipm.org/en/measurement-units/si-defining-constants
  - title: "NIST SP 811 — Guide for the Use of the International System of Units"
    url: https://www.nist.gov/pml/special-publication-811
  - title: "NIST — CODATA value of the Avogadro constant"
    url: https://physics.nist.gov/cgi-bin/cuu/Value?na
  - title: "OpenStax Chemistry 2e, 1.5 Measurement Uncertainty, Accuracy, and Precision"
    url: https://openstax.org/books/chemistry-2e/pages/1-5-measurement-uncertainty-accuracy-and-precision
  - title: "OpenStax Chemistry 2e, 1.6 Mathematical Treatment of Measurement Results"
    url: https://openstax.org/books/chemistry-2e/pages/1-6-mathematical-treatment-of-measurement-results
last_verified: "2026-10-16"
---

# 01.2 · Units, significant figures and dimensional analysis

Every number in chemistry carries a unit and an honest number of digits. This lesson teaches the SI units, how to convert between units without guessing, how many digits a result deserves, and how units themselves can catch your mistakes before anyone else does.

## Why it matters

In 1999 NASA lost the Mars Climate Orbiter. One team's software reported thruster impulse in pound-force seconds. Another team's software read the numbers as newton seconds. The factor between them is about 4.45. The spacecraft flew too low and was destroyed.

Chemistry has its own versions of this. A nurse mixes up milligrams and micrograms, which is a factor of 1000. A student uses millilitres where the formula wants litres, and the concentration comes out 1000 times too small. In each case the arithmetic was fine. The units were wrong. The habits in this lesson catch these errors on paper.

## Core ideas

### A quantity is a number times a unit

A physical quantity is something you can measure, such as a mass or a temperature. Its value is always a number multiplied by a unit:

$$m = 25.4 \text{ g}$$

The unit is part of the value. "25.4" alone means nothing. Treat units like algebra symbols: they multiply, divide and cancel.

### The SI: seven base units

The SI (International System of Units) is the system all science uses. It has seven base units. Every other unit is built from them.

| Quantity | Unit | Symbol |
|---|---|---|
| time | second | s |
| length | metre | m |
| mass | kilogram | kg |
| electric current | ampere | A |
| temperature | kelvin | K |
| amount of substance | mole | mol |
| luminous intensity | candela | cd |

Since 20 May 2019, all seven are defined by fixing the exact values of seven constants of nature. For example, the Planck constant is fixed at exactly $6.626\,070\,15 \times 10^{-34}$ J s, and that fixes the kilogram. The Avogadro constant is fixed at exactly

$$N_A = 6.022\,140\,76 \times 10^{23} \text{ mol}^{-1}$$

So one **mole** is exactly $6.022\,140\,76 \times 10^{23}$ particles (atoms, molecules, ions, whatever you are counting). Before 2019 the mole was defined through 12 g of carbon-12. Old textbooks still say that; the number is almost the same, but the definition changed.

### Derived units, prefixes and the units chemists really use

A **derived unit** is built from base units. Some have their own names:

- newton (force): $1 \text{ N} = 1 \text{ kg m s}^{-2}$
- joule (energy): $1 \text{ J} = 1 \text{ N m} = 1 \text{ kg m}^2 \text{ s}^{-2}$
- pascal (pressure): $1 \text{ Pa} = 1 \text{ N m}^{-2}$

A **prefix** multiplies a unit by a power of ten. The ones you will meet most:

| Prefix | Symbol | Factor |
|---|---|---|
| kilo | k | $10^{3}$ |
| centi | c | $10^{-2}$ |
| milli | m | $10^{-3}$ |
| micro | µ | $10^{-6}$ |
| nano | n | $10^{-9}$ |
| pico | p | $10^{-12}$ |

Chemists also use a few non-SI units every day. Know them and their exact links to the SI:

- litre: $1 \text{ L} = 1 \text{ dm}^3 = 10^{-3} \text{ m}^3$, and $1 \text{ mL} = 1 \text{ cm}^3$.
- degree Celsius: $T/\text{K} = t/{}^\circ\text{C} + 273.15$.
- standard atmosphere: $1 \text{ atm} = 101\,325 \text{ Pa}$ exactly. The bar: $1 \text{ bar} = 10^5 \text{ Pa}$.
- molarity: $1 \text{ M} = 1 \text{ mol L}^{-1}$ (a concentration).
- ångström: $1 \text{ Å} = 10^{-10} \text{ m}$ (bond lengths).

> [!NOTE]
> The SI definitions, the unit rules and the rounding rules here are stable. The defining constants are exact and will not change. Measured constants (CODATA values) are updated every four years; this course uses CODATA 2022, checked on the NIST site on 2026-10-16. The SI Brochure is in its 9th edition (2019), last updated in 2026.

### Dimensional analysis: the factor-label method

**Dimensional analysis** means using units to guide and check a calculation. The main tool is the **conversion factor**: a fraction equal to 1, such as

$$\frac{1000 \text{ mL}}{1 \text{ L}} = 1$$

Multiplying by 1 does not change a quantity. It only changes its units. So you choose the factor that cancels the unit you have and leaves the one you want:

$$0.250 \text{ L} \times \frac{1000 \text{ mL}}{1 \text{ L}} = 250 \text{ mL}$$

The L on top cancels the L on the bottom. If the units you are left with are not the ones you wanted, the factor is upside down.

The same idea checks formulas. Both sides of an equation must have the same units. If you calculate a temperature and the units come out as L kPa atm$^{-1}$ K, something is wrong before you look at the number.

### Significant figures: honest digits

A measurement is never exact. A kitchen scale that shows 254 g tells you the mass is somewhere near 254 g, perhaps between 253 and 255 g. The digits you can trust, plus the first uncertain one, are the **significant figures** (sig figs).

Counting rules:

- Non-zero digits always count. 254 has 3.
- Zeros between non-zero digits count. 305 has 3.
- Leading zeros never count. They only place the decimal point. 0.00450 has 3.
- Trailing zeros after a decimal point count. 0.00450 has 3, and 2.50 has 3.
- Trailing zeros in a whole number without a decimal point are unclear. Write 1200 as $1.2 \times 10^{3}$ (2 sig figs) or $1.200 \times 10^{3}$ (4 sig figs) to say what you mean.
- **Exact numbers** have unlimited sig figs. Counted things (5 repeats) and defined factors (1000 mL in 1 L, 273.15 in the Celsius conversion) never limit a result.

Rounding rules for calculations:

- **Multiplying or dividing:** keep as many sig figs as the input with the fewest sig figs.
- **Adding or subtracting:** keep as many decimal places as the input with the fewest decimal places.
- Keep all digits during the calculation. Round only the final answer. Rounding at every step adds errors.

Sig figs are a quick rule of thumb. In Lesson 01.5 you start writing a real uncertainty, such as $1.04 \pm 0.01$ g/mL, which says much more.

## Worked example

### How many water molecules are in a glass?

A glass holds 250.0 mL of water at 20 °C. The density of water at 20 °C is 0.9982 g/mL. The molar mass of water is 18.015 g/mol. How many molecules are there?

**Step 1: volume to mass.**

$$m = 250.0 \text{ mL} \times \frac{0.9982 \text{ g}}{1 \text{ mL}} = 249.55 \text{ g}$$

**Step 2: mass to amount (moles).**

$$n = 249.55 \text{ g} \times \frac{1 \text{ mol}}{18.015 \text{ g}} = 13.852 \text{ mol}$$

**Step 3: amount to number of molecules.**

$$N = 13.852 \text{ mol} \times \frac{6.022\,140\,76 \times 10^{23}}{1 \text{ mol}} = 8.342 \times 10^{24}$$

**Sig figs.** The inputs have 4 (250.0), 4 (0.9982) and 5 (18.015) sig figs. The Avogadro constant is exact. So the answer gets 4: $8.342 \times 10^{24}$ molecules. Note that the intermediate results kept extra digits; only the final answer was rounded.

**Check.** The units cancel to a pure number, which is right for a count. A glass of water is about 14 mol, and a mole is about $6 \times 10^{23}$, so about $8 \times 10^{24}$ makes sense.

### Catching a unit error

A student wants the temperature of 1.00 mol of gas at 101.3 kPa in 22.4 L. They write $T = PV/(nR)$ with $R = 0.08206$ L atm mol$^{-1}$ K$^{-1}$ and get 27 650 K. Look at the units:

$$\frac{\text{kPa} \times \text{L}}{\text{mol} \times \text{L atm mol}^{-1} \text{K}^{-1}} = \frac{\text{kPa}}{\text{atm}} \text{ K}$$

kPa and atm do not cancel. The fix is to use $R$ in matching units, $R = 8.314$ L kPa mol$^{-1}$ K$^{-1}$:

$$T = \frac{101.3 \text{ kPa} \times 22.4 \text{ L}}{1.00 \text{ mol} \times 8.314 \text{ L kPa mol}^{-1} \text{K}^{-1}} = 273 \text{ K}$$

That is 0 °C, which is what you expect for these conditions.

## Hands-on

**What you need:** paper, a pen, a calculator. **Time:** about 60 minutes.

Solve each problem. Write the units on every line. Give the answer with the right number of sig figs. Then check.

1. Convert 1.25 atm to kPa.
2. Convert a body temperature of 37.0 °C to kelvin.
3. How many sig figs do these have: 0.00450, 305, $1.200 \times 10^{3}$, 1200?
4. Add 12.51 g + 0.0034 g + 3.2 g.
5. A sample has a mass of 25.43 g and a volume of 23.1 mL. What is its density?
6. How many moles are in 5.00 g of table salt, NaCl (molar mass 58.44 g/mol)?
7. How many moles of sugar are in 250 mL of a 0.150 M sugar solution?
8. A recipe says "dissolve 2 µg per mL". Your scale reads in grams. How many grams do you need for 500 mL? Is a kitchen scale that reads to 1 g any use here?

<details><summary>Answers</summary>

1. $1.25 \text{ atm} \times \frac{101.325 \text{ kPa}}{1 \text{ atm}} = 126.66 \text{ kPa} \rightarrow 127 \text{ kPa}$ (3 sig figs; the factor is exact).
2. $37.0 + 273.15 = 310.15 \rightarrow 310.2 \text{ K}$. This is addition, so keep one decimal place, as in 37.0.
3. 0.00450 has 3. 305 has 3. $1.200 \times 10^{3}$ has 4. 1200 is unclear; read it as 2 unless told otherwise.
4. $15.7134 \text{ g} \rightarrow 15.7 \text{ g}$. The input 3.2 has only one decimal place.
5. $\rho = \frac{25.43 \text{ g}}{23.1 \text{ mL}} = 1.1009 \rightarrow 1.10 \text{ g/mL}$ (3 sig figs, from 23.1).
6. $5.00 \text{ g} \times \frac{1 \text{ mol}}{58.44 \text{ g}} = 0.085558 \rightarrow 0.0856 \text{ mol}$.
7. First convert mL to L: $250 \text{ mL} = 0.250 \text{ L}$. Then $0.250 \text{ L} \times 0.150 \frac{\text{mol}}{\text{L}} = 0.0375 \text{ mol}$. If you got 37.5 mol, you multiplied by mL.
8. $500 \text{ mL} \times \frac{2 \text{ µg}}{1 \text{ mL}} = 1000 \text{ µg} = 1 \times 10^{-3} \text{ g}$, one milligram. A scale that reads to 1 g cannot weigh this at all. You would need a balance that reads to at least 0.1 mg, or a dilution step: weigh a larger amount, dissolve it, and take a known fraction.

**How you know it worked:** 7 or 8 correct, and every line of your working shows units. If a mistake came from a unit, not from arithmetic, redo that problem tomorrow from a blank page.

</details>

## Common mistakes

- **Dropping units halfway.** Without units on every line you cannot see a wrong conversion. Write them, even when it feels slow.
- **Upside-down conversion factors.** If the unit you wanted to cancel is still there, flip the factor.
- **Rounding at every step.** Carry extra digits through the calculation; round once at the end.
- **Letting exact numbers limit sig figs.** "5 repeats" and "1000 mL per L" are exact. They never reduce the digits of the answer.
- **mL versus L in concentration.** Molarity is per litre. Convert millilitres first.
- **Mixing R values.** $R$ comes in several units (8.314 J mol$^{-1}$ K$^{-1}$, 0.08206 L atm mol$^{-1}$ K$^{-1}$). Pick the one whose units cancel with yours.

## Key takeaways

- A quantity is a number times a unit. Units multiply, divide and cancel like algebra.
- The SI has seven base units, defined since 2019 by seven fixed constants. One mole is exactly $6.022\,140\,76 \times 10^{23}$ particles.
- Convert with factors equal to 1, chosen so the unwanted unit cancels.
- Multiply/divide: fewest sig figs. Add/subtract: fewest decimal places. Exact numbers never limit. Round only at the end.
- If the units of a result are wrong, the result is wrong.

## Sources

- [BIPM — The International System of Units (SI Brochure, 9th edition, 2019, updated 2026)](https://www.bipm.org/en/publications/si-brochure).
- [BIPM — SI defining constants](https://www.bipm.org/en/measurement-units/si-defining-constants) (exact values; adopted by the CGPM in 2018, in force since 20 May 2019).
- [NIST SP 811 — Guide for the Use of the International System of Units](https://www.nist.gov/pml/special-publication-811) (writing quantities and units).
- [NIST — CODATA value of the Avogadro constant](https://physics.nist.gov/cgi-bin/cuu/Value?na) (checked 2026-10-16).
- [OpenStax Chemistry 2e, 1.5 Measurement Uncertainty, Accuracy, and Precision](https://openstax.org/books/chemistry-2e/pages/1-5-measurement-uncertainty-accuracy-and-precision) (sig-fig and rounding rules).
- [OpenStax Chemistry 2e, 1.6 Mathematical Treatment of Measurement Results](https://openstax.org/books/chemistry-2e/pages/1-6-mathematical-treatment-of-measurement-results) (dimensional analysis).
