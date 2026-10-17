---
id: "08.6"
module: 8
minutes: 20
practice_minutes: 75
prerequisites: ["08.5", "08.2", "04.4"]
objectives:
  - Identify the anode and cathode of a galvanic cell, write its cell notation and calculate E°cell from a table of standard reduction potentials.
  - Convert between E°cell, ΔG° and K using ΔG° = −nFE° and ΔG° = −RT ln K.
  - Use the Nernst equation to calculate a cell potential at non-standard concentrations.
  - Build a zinc–copper fruit or vinegar cell, measure its voltage and internal resistance with a multimeter, and explain why it is not a Daniell cell.
volatility: concept
sources:
  - title: "OpenStax Chemistry 2e, 17.2 Galvanic Cells"
    url: https://openstax.org/books/chemistry-2e/pages/17-2-galvanic-cells
  - title: "OpenStax Chemistry 2e, 17.3 Electrode and Cell Potentials"
    url: https://openstax.org/books/chemistry-2e/pages/17-3-electrode-and-cell-potentials
  - title: "OpenStax Chemistry 2e, 17.4 Potential, Free Energy, and Equilibrium"
    url: https://openstax.org/books/chemistry-2e/pages/17-4-potential-free-energy-and-equilibrium
  - title: "OpenStax Chemistry 2e, Appendix L: Standard Electrode (Half-Cell) Potentials"
    url: https://openstax.org/books/chemistry-2e/pages/l-standard-electrode-half-cell-potentials
  - title: "Goodisman, J. (2001) Observations on Lemon Cells. Journal of Chemical Education 78 (Syracuse University repository)"
    url: https://surface.syr.edu/che/2
  - title: "NIST CODATA value: Faraday constant"
    url: https://physics.nist.gov/cgi-bin/cuu/Value?f
last_verified: "2026-10-17"
---

# 08.6 · Electrochemical cells and the Nernst equation

A redox reaction moves electrons from one species to another. If you keep the two species apart and give the electrons a wire to travel through, the reaction drives a current: that is a battery. This lesson shows how to predict the voltage of such a cell from a table, how that voltage is tied to the free energy and the equilibrium constant you met earlier in this module, and how it changes with concentration through the Nernst equation. Then you will build the famous lemon battery, measure it, and find out why the textbook explanation of it is wrong.

## Why it matters

Every phone, car battery, glucose meter and pH electrode is an electrochemical cell. A corrosion engineer asks whether a steel bolt in an aluminium frame will rot, and the answer is a cell potential. A pH meter reads the hydrogen-ion concentration as a voltage, through the Nernst equation, and so does every nerve cell in your body (lesson [06.1](../module-06/lesson-01.md)). The same few equations answer how much voltage a cell gives, how much energy it can deliver, and how that changes as it runs down.

## Core ideas

> [!NOTE]
> The theory is stable. $E^\circ$ values are from OpenStax Chemistry 2e Appendix L (25 °C, 1 mol/L, 1 bar); $F$ = 96 485.33212 C/mol and $R$ = 8.314462618 J mol⁻¹ K⁻¹ are exact CODATA 2022 values from NIST. All checked 2026-10-17.

### The galvanic cell

Put a zinc strip in zinc sulfate solution and a copper strip in copper sulfate solution, in separate beakers. Join the metals with a wire, and join the solutions with a **salt bridge** (a tube of salt solution or gel that lets ions move but stops the solutions mixing). Electrons flow through the wire from zinc to copper. This is the **Daniell cell**, a **galvanic cell**: a cell in which a spontaneous reaction produces electrical work.

- The **anode** is where oxidation happens: $\mathrm{Zn \rightarrow Zn^{2+} + 2e^-}$. Electrons leave the cell here, so in a battery it is the negative terminal.
- The **cathode** is where reduction happens: $\mathrm{Cu^{2+} + 2e^- \rightarrow Cu}$. It is the positive terminal.
- The salt bridge carries ions to keep each solution electrically neutral. Without it the current stops at once.

A memory aid: "An Ox, Red Cat": anode oxidation, reduction cathode. Cell notation writes the anode on the left, phase boundaries as single bars and the salt bridge as a double bar:

$$\mathrm{Zn(s)\,|\,Zn^{2+}(aq)\,\|\,Cu^{2+}(aq)\,|\,Cu(s)}$$

### Standard reduction potentials

The voltage between the electrodes is the **cell potential** $E_\text{cell}$, in volts (joules per coulomb of charge; lesson [04.4](../module-04/lesson-04.md)). You cannot measure one electrode alone, so all are measured against the **standard hydrogen electrode** (H⁺ at 1 mol/L, H₂ at 1 bar, platinum), defined as 0 V. Each half-reaction, written as a reduction, has a **standard reduction potential** $E^\circ$. The more positive $E^\circ$, the more strongly the species pulls electrons in.

| Half-reaction | $E^\circ$ (V) |
|---|---|
| $\mathrm{Ag^+ + e^- \rightarrow Ag}$ | +0.7996 |
| $\mathrm{Cu^{2+} + 2e^- \rightarrow Cu}$ | +0.337 |
| $\mathrm{2H^+ + 2e^- \rightarrow H_2}$ | 0.00 |
| $\mathrm{Fe^{2+} + 2e^- \rightarrow Fe}$ | −0.447 |
| $\mathrm{Zn^{2+} + 2e^- \rightarrow Zn}$ | −0.7618 |
| $\mathrm{Mg^{2+} + 2e^- \rightarrow Mg}$ | −2.372 |

For any cell:

$$E^\circ_\text{cell} = E^\circ_\text{cathode} - E^\circ_\text{anode}$$

Both values are taken as reductions straight from the table; the subtraction does the reversal. Do *not* multiply $E^\circ$ by the coefficients: a potential is energy per charge, so it does not depend on how much reacts. Daniell cell: $0.337 - (-0.7618) = 1.099$ V. A positive $E^\circ_\text{cell}$ means the reaction as written is spontaneous.

### Potential, free energy and K

The electrical work a cell can do is charge times voltage. For $n$ moles of electrons transferred per mole of reaction, the charge is $nF$, where the **Faraday constant** $F$ = 96 485 C/mol is the charge of one mole of electrons. So

$$\Delta G^\circ = -nFE^\circ_\text{cell}$$

Combining with $\Delta G^\circ = -RT\ln K$ (lesson [08.2](lesson-02.md)):

$$E^\circ_\text{cell} = \frac{RT}{nF}\ln K$$

Daniell cell: $\Delta G^\circ = -2 \times 96\,485 \times 1.099 = -212$ kJ/mol and $K = e^{2 \times 96\,485 \times 1.099/(8.314 \times 298.15)} = 1.4 \times 10^{37}$. Zinc in copper sulfate turns essentially all the Cu²⁺ into copper metal. A cell voltage of only one volt means an enormous $K$, because $nF/RT$ is about 78 per volt for $n = 2$.

### The Nernst equation

Away from standard concentrations, use $\Delta G = \Delta G^\circ + RT\ln Q$ and divide by $-nF$:

$$E = E^\circ - \frac{RT}{nF}\ln Q \qquad\text{or, at 25 °C,}\qquad E = E^\circ - \frac{0.05916\ \text{V}}{n}\log_{10} Q$$

This is the **Nernst equation**. $Q$ is the reaction quotient (lesson [08.3](lesson-03.md)) for the cell reaction; solids are left out. For the Daniell cell $Q = [\mathrm{Zn^{2+}}]/[\mathrm{Cu^{2+}}]$. Each factor of ten in $Q$ changes $E$ by 59 mV divided by $n$. As a battery runs, $Q$ grows and $E$ falls; when $Q = K$, $E = 0$ and the battery is flat: it has reached equilibrium.

A **concentration cell** has the same electrode on both sides and only different concentrations. Its $E^\circ$ is zero, and its whole voltage comes from the Nernst term. That is exactly how a membrane potential arises in a nerve cell, and how a glass pH electrode works (59 mV per pH unit).

### Why a lemon battery is not a Daniell cell

Push a galvanised (zinc-coated) nail and a copper wire into a lemon and you read about 0.9 V. Textbooks often call this a zinc–copper cell. But there is no Cu²⁺ in a lemon, so copper cannot be the thing reduced. Goodisman (2001) measured lemon cells and showed what happens instead. Zinc is oxidised at the anode, as expected. At the copper, the acid's H⁺ is reduced to hydrogen (and some dissolved O₂ is reduced too). Copper is only an inert conductor that hosts the reaction:

$$\mathrm{Zn + 2H^+ \rightarrow Zn^{2+} + H_2} \qquad E^\circ = 0.7618\ \text{V}$$

The Nernst equation with the lemon's real conditions (pH about 2–3, almost no Zn²⁺ or H₂ yet) raises this to about 0.9 V, which is what you measure. The cell also has a large **internal resistance**, $r$, of a kilohm or more, because the juice conducts poorly and the electrodes are small. So the voltage collapses as soon as you draw current, and a lemon cannot light an ordinary bulb.

## Worked example

### 1. A Daniell cell running down

A Daniell cell starts with 1.0 M Zn²⁺ and 1.0 M Cu²⁺, so $E = E^\circ = 1.099$ V. After long use, [Zn²⁺] = 1.99 M and [Cu²⁺] = 0.010 M (each mole of Cu²⁺ used makes one of Zn²⁺).

$$E = 1.099 - \frac{0.05916}{2}\log_{10}\frac{1.99}{0.010} = 1.099 - 0.02958 \times 2.30 = 1.031\ \text{V}$$

With 99 % of the copper ions gone, the voltage has dropped by only 68 mV. That flat curve is why battery voltage is a poor fuel gauge until the very end.

### 2. Will an iron nail plate out silver?

Fe(s) in Ag⁺ solution: cathode Ag⁺/Ag (+0.7996), anode Fe²⁺/Fe (−0.447).

$$E^\circ_\text{cell} = 0.7996 - (-0.447) = 1.247\ \text{V}, \qquad \mathrm{Fe + 2Ag^+ \rightarrow Fe^{2+} + 2Ag}, \quad n = 2$$

$\Delta G^\circ = -2 \times 96\,485 \times 1.247 = -241$ kJ/mol. Yes, strongly: silver crystals grow on the nail. Note that the silver half-reaction is doubled to balance electrons, but its $E^\circ$ is not.

## Hands-on

What you need: a digital multimeter (the one from lesson 04.4), two or three galvanised nails (zinc coated, grey and slightly rough), the same number of pieces of thick copper wire (strip the insulation from an offcut of household cable) or copper pipe offcuts, a lemon, white vinegar, table salt, small cups, resistors from your lesson 04.4 kit (100 Ω to 10 kΩ) or any you have, crocodile-clip leads, and the [Module 8 lab folder](../../labs/module-08/). Time: about 75 minutes.

### Part A — home: three fruit and kitchen cells (40 min)

> [!WARNING]
> Use only these cells and the multimeter; never connect anything to mains power. Nails and wire ends are sharp: handle them with care. Wear safety glasses, because lemon juice and vinegar sting the eyes. Do not eat the lemon or drink the liquids afterwards: they contain dissolved zinc. Throw them away and wash your hands.

1. Roll the lemon on the table to free the juice. Push in a nail and a copper wire about 2 cm apart, not touching.
2. Set the multimeter to DC volts (2 V or 20 V range). Red lead to copper, black to zinc. Record the open-circuit voltage. Swap the leads and note the sign change: copper is the positive terminal.
3. Connect a resistor across the electrodes, measure the voltage across it, and record $R$ and $V$. Repeat with 4–6 resistors from about 100 Ω to 10 kΩ.
4. Repeat steps 1–3 in a cup of vinegar and in a cup of salt water (1 teaspoon of salt in 100 mL of water), with fresh electrode positions.
5. Optional: connect two lemon cells in series (copper of one to zinc of the next) and measure again.
6. Type your readings into a CSV file with columns `electrolyte,R_ohm,V_V` (write `open` for no resistor), using `lemon_cell_example.csv` as a model. Record the setup on a [notebook page](../../templates/notebook-page.md).

How you know it worked: open-circuit voltages of about 0.8–1.0 V in lemon and vinegar and a little lower in salt water; two cells in series give nearly twice the voltage. With a 100 Ω resistor the voltage drops to well under 0.1 V.

### Part B — Python: Nernst and the internal resistance (25 min)

Open `lesson06_nernst.py` and write `nernst` (one line) and `loaded_voltage`, the model $V = ER/(R + r)$ for a cell with internal resistance $r$ driving a load $R$. Then run the example data, then your own file:

```bash
py lesson06_nernst.py
py lesson06_nernst.py my_cells.csv
```

How you know it worked: the Daniell block prints $E^\circ$ = 1.099 V, $\Delta G^\circ$ = −212 kJ/mol, $K$ = 1.40 × 10³⁷, and 1.128, 1.040 and 0.921 V for the three non-standard cases. The copper concentration cell gives 0.0887 V. The lemon-cell estimate (Zn anode, H⁺/H₂ cathode) gives 0.88–0.99 V depending on the pH and [Zn²⁺] assumed. The fit of the example data gives, for the lemon, $E = 0.919 \pm 0.006$ V and $r = 1761 \pm 33$ Ω, with a maximum current of about 0.5 mA. The plot `runs/lesson06_load_curve.png` shows each curve rising from near zero to its plateau at $E$.

<details><summary>Reference solution and interpretation</summary>

`nernst`: `return e_standard - R * t / (n * F) * math.log(q)`. `loaded_voltage`: `return emf * r_load / (r_load + r_internal)`. Full code in `lesson06_nernst_solution.py`.

The fitted $E$ matches the open-circuit reading, which checks the model. The kilohm internal resistance limits the current to $E/r \approx 0.5$ mA and the power to $E^2/4r \approx 0.1$ mW. A small LED needs about 2 V and a few mA, so you need several cells in series and still get only a faint glow. Salt water has a lower $r$ (it conducts better) but a lower $E$: with almost no H⁺, the cathode reaction is mainly O₂ reduction, slowed by how fast oxygen reaches the copper.

</details>

### Part C — pencil (10 min)

1. Write the cell notation and $E^\circ_\text{cell}$ for a magnesium–copper cell.
2. A cell has $E^\circ$ = 0.46 V and $n$ = 2. Find $K$ at 25 °C.
3. A glass pH electrode follows $E = \text{const} - 0.05916\,\mathrm{pH}$. By how much does its voltage change between vinegar (pH 2.4) and baking-soda solution (pH 8.3)?

<details><summary>Answers to Part C</summary>

1. $\mathrm{Mg(s)\,|\,Mg^{2+}(aq)\,\|\,Cu^{2+}(aq)\,|\,Cu(s)}$; $E^\circ = 0.337 - (-2.372) = 2.709$ V.
2. $\ln K = 2 \times 96\,485 \times 0.46 / (8.314 \times 298.15) = 35.8$, so $K = 3.6 \times 10^{15}$.
3. $0.05916 \times (8.3 - 2.4) = 0.35$ V. The meter turns this voltage into a pH reading.

</details>

## Common mistakes

- **Multiplying $E^\circ$ by the stoichiometric coefficient.** Potentials are per charge. Balance the electrons in the equation, but leave $E^\circ$ alone.
- **Reversing the sign twice.** Use $E^\circ_\text{cathode} - E^\circ_\text{anode}$ with both values as listed (reductions). Do not also flip the anode's sign.
- **Forgetting $n$ in $\Delta G^\circ = -nFE^\circ$ or in the Nernst term.** For Zn/Cu, $n = 2$.
- **Using concentrations of solids in $Q$.** Zn(s) and Cu(s) are left out, as in lesson 08.3.
- **Believing the lemon cell is a Zn/Cu²⁺ cell.** There is no Cu²⁺; the copper hosts H⁺ (or O₂) reduction.
- **Reading voltage under load as the cell's $E$.** A high internal resistance makes the loaded voltage much smaller. Measure open-circuit for $E$.

## Key takeaways

- In a galvanic cell, oxidation at the anode (negative terminal) and reduction at the cathode (positive) are joined by a wire and a salt bridge.
- $E^\circ_\text{cell} = E^\circ_\text{cathode} - E^\circ_\text{anode}$ from the reduction-potential table; positive means spontaneous.
- $\Delta G^\circ = -nFE^\circ$ and $E^\circ = (RT/nF)\ln K$: about 1 V for $n = 2$ means $K \approx 10^{37}$.
- Nernst: $E = E^\circ - (0.05916/n)\log_{10}Q$ at 25 °C. $E$ falls slowly as a cell runs down and is zero at equilibrium.
- A lemon cell is zinc oxidised and H⁺ reduced on copper, with a kilohm internal resistance: about 0.9 V but well under 1 mA.

## Sources

- [OpenStax Chemistry 2e, 17.2 Galvanic Cells](https://openstax.org/books/chemistry-2e/pages/17-2-galvanic-cells) — anode, cathode, salt bridge, cell notation.
- [OpenStax Chemistry 2e, 17.3 Electrode and Cell Potentials](https://openstax.org/books/chemistry-2e/pages/17-3-electrode-and-cell-potentials) — standard hydrogen electrode, $E^\circ_\text{cell}$.
- [OpenStax Chemistry 2e, 17.4 Potential, Free Energy, and Equilibrium](https://openstax.org/books/chemistry-2e/pages/17-4-potential-free-energy-and-equilibrium) — $\Delta G^\circ = -nFE^\circ$, $K$, Nernst equation.
- [OpenStax Chemistry 2e, Appendix L](https://openstax.org/books/chemistry-2e/pages/l-standard-electrode-half-cell-potentials) — all $E^\circ$ values used here.
- [Goodisman (2001), Observations on Lemon Cells](https://surface.syr.edu/che/2) — measurements showing the lemon cell is not a Zn/Cu²⁺ cell.
- [NIST CODATA, Faraday constant](https://physics.nist.gov/cgi-bin/cuu/Value?f) — $F$ = 96 485.33212 C/mol (exact).
