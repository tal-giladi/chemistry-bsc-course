---
id: "32.2"
module: 32
minutes: 24
practice_minutes: 100
prerequisites: ["32.1", "08.6", "23.5"]
objectives:
  - Calculate the voltage, theoretical capacity and specific energy of a battery or fuel cell from thermodynamic data and Faraday's law.
  - Explain where a working cell loses voltage (activation, resistance, mass transport) using the Butler–Volmer picture.
  - Describe corrosion as a mixed-potential process and determine a corrosion current from a polarisation curve by Tafel extrapolation and by polarisation resistance.
  - Convert a corrosion current into a penetration rate and choose a protection method for a given situation.
volatility: concept
sources:
  - title: "OpenStax Chemistry 2e, 17.5 Batteries and Fuel Cells"
    url: https://openstax.org/books/chemistry-2e/pages/17-5-batteries-and-fuel-cells
  - title: "OpenStax Chemistry 2e, 17.6 Corrosion"
    url: https://openstax.org/books/chemistry-2e/pages/17-6-corrosion
  - title: "Goodenough and Park, The Li-ion rechargeable battery: a perspective, J. Am. Chem. Soc. 135, 1167 (2013)"
    url: https://doi.org/10.1021/ja3091438
  - title: "Stern and Geary, Electrochemical polarization, J. Electrochem. Soc. 104, 56 (1957)"
    url: https://doi.org/10.1149/1.2428496
  - title: "ASTM G102-23, Calculation of corrosion rates and related information from electrochemical measurements"
    url: https://store.astm.org/g0102-23.html
  - title: "US EPA, Used lithium-ion batteries (updated 2026-03-20)"
    url: https://www.epa.gov/recycle/used-lithium-ion-batteries
last_verified: "2026-10-17"
---

# 32.2 · Batteries, fuel cells and corrosion

A battery, a fuel cell and a rusting bridge run on the same chemistry: an oxidation and a reduction joined by a path for electrons and a path for ions. In a battery you want that reaction to happen only when you ask, and to give back as much of its free energy as possible. In a bridge you want it never to happen at all. This lesson uses the Nernst equation from [Lesson 08.6](../module-08/lesson-06.md) and the electrode kinetics of [Lesson 32.1](lesson-01.md) to calculate what a cell can deliver, why it delivers less, and how fast steel corrodes.

## Why it matters

A water utility must decide whether to replace a steel pipe section in a salty aquifer or protect it with zinc anodes. Weight-loss coupons would take a year to answer. A ten-minute polarisation scan on a probe in the pipe gives a corrosion current, and the current gives a rate in millimetres per year. If the rate is 0.03 mm/y, the pipe will outlive everyone. If it is 3 mm/y, a 6 mm wall is gone in two years. The same curve, read wrongly (for example without the resistance correction), can overstate the rate by more than half, and the utility pays for the wrong job.

## Core ideas

> [!NOTE]
> Stable: cell thermodynamics, Faraday's law, mixed-potential theory, the Stern–Geary relation (1957) and the ASTM G102 conversion. Battery chemistries, practical capacities and costs change every year; the numbers here are textbook values checked 2026-10-17 against OpenStax 17.5–17.6 and Goodenough and Park (2013). The EPA guidance on used lithium-ion batteries was last updated 2026-03-20. Lab data are generated.

### What a cell can deliver: voltage, capacity, energy

The open-circuit voltage comes from the free energy of the cell reaction, as in 08.6: $E_\text{cell} = -\Delta_r G / nF$.

The **theoretical specific capacity** of an electrode material of molar mass $M$ (g/mol) that exchanges $n$ electrons per formula unit is

$$Q = \frac{nF}{3.6\,M}\ \ \text{mAh/g}$$

(3.6 converts coulombs to milliampere-hours). For graphite, which stores one lithium per six carbons (LiC₆, $M$ = 72.07 g/mol for C₆), $Q = 96485/(3.6 \times 72.07)$ = 372 mAh/g. For LiFePO₄ ($M$ = 157.8) it is 170 mAh/g. For LiCoO₂ ($M$ = 97.9) it is 274 mAh/g, but only about half of the lithium can be removed without damaging the structure, so about 140 mAh/g is usable (Goodenough and Park 2013).

**Specific energy** is capacity times voltage. Watch the units: mAh/g × V = mWh/g = Wh/kg.

### Three cells you meet every day

| Cell | Reactions (discharge) | Nominal voltage | Notes |
|---|---|---|---|
| Lead–acid | Pb + PbO₂ + 2 H₂SO₄ → 2 PbSO₄ + 2 H₂O | 2.0 V per cell | heavy, cheap, recyclable; car starters |
| Lithium-ion (LFP) | LiC₆ + FePO₄ → C₆ + LiFePO₄ | about 3.2 V | Li⁺ shuttles between two host lattices; no metal plated in normal use |
| H₂/O₂ fuel cell (PEM) | 2 H₂ + O₂ → 2 H₂O | 1.23 V at open circuit (theory) | fuel is fed continuously; Pt catalysts |

In a lithium-ion cell neither electrode dissolves. Lithium ions move through the electrolyte and slide into the layers or channels of the host solids, while electrons go round the outside circuit. The organic electrolyte is flammable, which is why a damaged cell can catch fire.

### Why the working voltage is lower

A fuel cell with $\Delta_r G^\circ$ = −237.1 kJ per mole of liquid water should give 237100/(2 × 96485) = 1.229 V. Under load it gives 0.6–0.8 V. The missing voltage is the overpotential of 32.1, added up around the cell:

$$V = E_\text{cell} - |\eta_\text{anode}| - |\eta_\text{cathode}| - iR_\text{cell} - \eta_\text{mass transport}$$

In a PEM fuel cell the biggest loss is at the oxygen cathode, because oxygen reduction on platinum has a tiny exchange current density. A battery shows the same terms: charging needs more voltage than discharging gives, and the gap, times the charge, is heat.

### Corrosion is a short-circuited cell

When steel sits in salty water, iron is oxidised at some spots ($\text{Fe} \rightarrow \text{Fe}^{2+} + 2\text{e}^-$) and oxygen or hydrogen ions are reduced at others ($\text{O}_2 + 2\text{H}_2\text{O} + 4\text{e}^- \rightarrow 4\text{OH}^-$ in neutral water; $2\text{H}^+ + 2\text{e}^- \rightarrow \text{H}_2$ in acid). The metal itself is the wire.

```mermaid
flowchart LR
  A["anodic area: Fe to Fe2+ + 2e-"] -- "electrons through the steel" --> C["cathodic area: O2 or H+ reduced"]
  C -- "ions through the water" --> A
```

Both reactions run on the same piece of metal, so they must share one potential and their currents must be equal and opposite. That potential is the **corrosion potential** $E_\text{corr}$; the current that flows each way is the **corrosion current** $i_\text{corr}$. It is a mixed potential, not an equilibrium potential: two different reactions are balanced, not one reaction and its reverse.

Near $E_\text{corr}$ each reaction follows its own Tafel law, so the net current is

$$i = i_\text{corr}\left[10^{(E - E_\text{corr})/\beta_a} - 10^{-(E - E_\text{corr})/\beta_c}\right]$$

where $\beta_a$ and $\beta_c$ are the anodic and cathodic Tafel slopes in V/decade.

### Two ways to measure $i_\text{corr}$

**Tafel extrapolation.** Scan about ±250 mV around $E_\text{corr}$, plot $\log|i|$ against $E$ (an Evans plot), fit both straight branches and extend them. They cross at $E_\text{corr}$ and $\log i_\text{corr}$. The scan pushes the metal far from its natural state, so it is destructive.

**Polarisation resistance.** Within ±10 mV of $E_\text{corr}$ the curve is a straight line. Its slope $R_p = dE/di$ gives (Stern and Geary 1957)

$$i_\text{corr} = \frac{B}{R_p}, \qquad B = \frac{\beta_a \beta_c}{2.303(\beta_a + \beta_c)}$$

This barely disturbs the metal, so it can be repeated every hour on a pipe probe. You need the Tafel slopes once, from a separate scan or the literature.

### From current to millimetres per year

Faraday's law turns the current into mass lost. ASTM G102 writes it as

$$\text{CR (mm/y)} = 3.27\times10^{-3}\ \frac{i_\text{corr}\ (\mu\text{A/cm}^2) \times EW}{\rho}$$

where $EW$ is the equivalent weight (molar mass divided by the electrons lost: 55.845/2 = 27.92 g for iron) and $\rho$ the density (7.87 g/cm³). For iron, 1 µA/cm² is about 0.0116 mm/y. This assumes uniform corrosion; pitting can perforate a wall far faster than the average suggests.

### Protection

- **Barrier:** paint or polymer coatings keep water and oxygen away.
- **Sacrificial anode:** a more active metal (zinc on galvanised steel, magnesium rods in water heaters) corrodes instead of the steel, because it pulls the mixed potential down to where iron hardly oxidises.
- **Impressed current:** a power supply holds the structure at a negative potential (ships, pipelines).
- **Passivation and alloying:** chromium in stainless steel forms a thin protective oxide film.
- **Inhibitors:** molecules that adsorb on the surface and slow one or both reactions.
- **Avoid galvanic couples:** steel bolted to copper corrodes faster, because copper is a good cathode.

## Worked example

### 1. The energy ceiling of an LFP/graphite cell

Per gram of active material, the cathode stores 170 mAh and the anode 372 mAh. The cell needs both, in matched amounts, so the capacity per gram of the pair is

$$Q_\text{pair} = \left(\frac{1}{170} + \frac{1}{372}\right)^{-1} = 117\ \text{mAh/g}$$

At 3.2 V that is 117 × 3.2 = 373 Wh/kg of active material. A real cell also carries electrolyte, separator, copper and aluminium foils and a case, so its specific energy is well under half of this ceiling. To beat the ceiling you need a new chemistry, not better engineering.

### 2. How fast does the steel corrode?

A polarisation scan of carbon steel in 1 M HCl (after iR correction) gives $E_\text{corr}$ = −0.470 V vs SCE, $\beta_a$ = 70 mV/dec, $\beta_c$ = 120 mV/dec, and Tafel lines that cross at $i_\text{corr}$ = 250 µA/cm².

Rate: $\text{CR} = 3.27\times10^{-3} \times 250 \times 27.92 / 7.87$ = 2.90 mm/y.

Check by polarisation resistance: $B = (0.070 \times 0.120)/(2.303 \times 0.190)$ = 0.0192 V. The slope near $E_\text{corr}$ is $R_p$ = 76 Ω cm², so $i_\text{corr}$ = 0.0192/76 = 2.53 × 10⁻⁴ A/cm², the same within 1 %.

## Hands-on

> [!WARNING]
> Never open, cut, puncture, crush, heat or short-circuit a battery, and never charge a swollen or damaged one. Lithium-ion cells can catch fire or vent toxic, flammable gas even when they look flat. Do not use batteries in any home experiment in this lesson. Take used cells to a battery collection point (in Israel, the collection boxes in shops and municipal centres), with the terminals taped, as the US EPA also advises. The nail experiment below uses only kitchen salt, water and ordinary hardware: wear safety glasses when you cut wire, handle nails with care, keep the jars away from children and food, and wash your hands afterwards.

What you need: the [Module 32 lab folder](../../labs/module-32/), five clean glass jars, four ordinary steel nails (not galvanised), one galvanised nail, a short piece of copper wire stripped from an old cable, kitchen aluminium foil, table salt, fine sandpaper, a phone camera, and a [notebook page](../../templates/notebook-page.md). Time: 30 minutes to set up, 2 minutes a day for a week, 60 minutes for the Python and pencil parts.

### Part A — home: galvanic couples in salt water (30 min + one week)

1. Dissolve 2 level teaspoons of salt (about 12 g) in 350 mL of tap water, close to sea water (3.5 %).
2. Lightly sand four plain nails to bare metal. Leave one as it is (jar 1). Wrap copper wire tightly round the middle of the second (jar 2) and a 2 cm strip of aluminium foil round the third (jar 3). Put the fourth plain nail in a jar of tap water without salt (jar 4). Put the galvanised nail in salt water (jar 5).
3. Cover each nail with about 70 mL of the liquid. Photograph all jars every day at the same time, with the same light.
4. Predict before you look: rank the jars from most to least rust, and write the reason using $E_\text{corr}$ and the role of each metal as anode or cathode.

How you know it worked: by day 2–3 the nail touching copper shows the most orange rust, concentrated away from the copper; the plain nail in salt water rusts clearly; tap water rusts more slowly; the galvanised nail stays almost clean while its zinc turns white; aluminium protects partly and unevenly, because its own oxide film limits how well it acts as an anode.

### Part B — Python: corrosion rate from a polarisation curve (40 min)

Open `lesson02_corrosion.py`. The data in `corrosion_steel.csv` are generated: carbon steel in 1 M HCl, 1.00 cm², $R_u$ = 1.0 Ω. Complete `stern_geary()` (TODO 1) and `corrosion_rate()` (TODO 2), then run:

```bash
py lesson02_corrosion.py
py lesson02_corrosion.py bare 0
```

The second command skips the resistance correction. Compare the two results in your notebook.

How you know it worked: with the correction, $E_\text{corr}$ = −470 mV, $\beta_a$ = 70 and $\beta_c$ = 120 mV/dec, $i_\text{corr}$ = 250 µA/cm² by Tafel extrapolation and 253 µA/cm² by Stern–Geary, 2.90 mm/y. Without it the anodic slope looks like 106 mV/dec and the Tafel estimate rises to 408 µA/cm² (4.7 mm/y, 63 % high).

### Part C — pencil (20 min)

1. A PEM fuel cell delivers 0.70 V. What fraction of the free energy of the reaction becomes electrical work?
2. A zinc anode on a ship hull corrodes at 30 µA/cm². Zinc: 65.38 g/mol, 2 electrons, 7.13 g/cm³. What is its penetration rate in mm/y?
3. A steel tank in seawater shows $R_p$ = 2500 Ω cm² and $B$ = 26 mV. Is a 3 mm corrosion allowance enough for 30 years of uniform corrosion?

<details><summary>Answers</summary>

1. 0.70/1.229 = 57 %. The rest is heat from the overpotentials and the cell resistance.
2. $EW$ = 32.69 g; CR = 3.27 × 10⁻³ × 30 × 32.69/7.13 = 0.45 mm/y.
3. $i_\text{corr}$ = 0.026/2500 = 1.04 × 10⁻⁵ A/cm² = 10.4 µA/cm², so CR = 0.12 mm/y and 3.6 mm in 30 years. No: the allowance runs out after about 25 years, and pitting would make it worse.

</details>

## Common mistakes

- **Mixing up mAh/g and Wh/kg.** Capacity becomes energy only after you multiply by the voltage.
- **Using one electrode's capacity for a whole cell.** The pair's capacity is the reciprocal sum, and the inactive parts lower it further.
- **Reading $E_\text{corr}$ as an equilibrium potential.** It is a mixed potential of two different reactions, so the Nernst equation does not give it.
- **Fitting Tafel lines too close to $E_\text{corr}$.** Within about 50–80 mV the opposite reaction still contributes. Start further out, and correct for iR.
- **Trusting a uniform rate for pitting metals.** Stainless steel or aluminium in chloride can fail by pits while the average rate looks tiny.

## Key takeaways

- Cell voltage comes from $\Delta_r G$; capacity from $nF/M$; energy is their product, and real cells reach only part of it.
- Every working cell loses voltage to activation, resistance and mass transport, the same terms as in 32.1.
- Corrosion is two reactions sharing one metal: $E_\text{corr}$ and $i_\text{corr}$ come from where their Tafel lines cross.
- Stern–Geary gives $i_\text{corr}$ non-destructively from $R_p$; ASTM G102 turns it into mm/y.
- Batteries are energy stores: never open, damage or short them, and recycle them.

## Sources

- [OpenStax Chemistry 2e, 17.5](https://openstax.org/books/chemistry-2e/pages/17-5-batteries-and-fuel-cells) — primary and secondary batteries, lead–acid, lithium-ion and fuel cells.
- [OpenStax Chemistry 2e, 17.6](https://openstax.org/books/chemistry-2e/pages/17-6-corrosion) — corrosion of iron, galvanising and sacrificial anodes.
- [Goodenough and Park 2013, J. Am. Chem. Soc. 135, 1167](https://doi.org/10.1021/ja3091438) — lithium-ion electrode chemistry and its limits.
- [Stern and Geary 1957, J. Electrochem. Soc. 104, 56](https://doi.org/10.1149/1.2428496) — the polarisation-resistance method.
- [ASTM G102-23](https://store.astm.org/g0102-23.html) — converting corrosion current into penetration rate (paid standard; the equation used here is the standard Faraday conversion).
- [US EPA, Used lithium-ion batteries](https://www.epa.gov/recycle/used-lithium-ion-batteries) — safe storage and recycling of used cells.
