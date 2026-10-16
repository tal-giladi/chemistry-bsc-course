---
id: "06.1"
module: 6
minutes: 22
practice_minutes: 150
prerequisites: ["01.5", "02.1", "04.3"]
objectives:
  - Estimate how long a molecule takes to diffuse across a cell, an organelle or a tissue with t = x²/2D, and explain why cells are small.
  - Explain with the hydrophobic effect why phospholipids form bilayers and predict which molecules cross a bilayer unaided.
  - Calculate osmolarity and osmotic pressure with Π = icRT and predict which way water moves.
  - Calculate the Nernst potential of an ion from its concentrations inside and outside a cell, and measure the isotonic point of potato tissue with a home experiment.
volatility: concept
sources:
  - title: "OpenStax Biology 2e, 4.2 Prokaryotic Cells (cell size)"
    url: https://openstax.org/books/biology-2e/pages/4-2-prokaryotic-cells
  - title: "OpenStax Biology 2e, 5.1 Components and Structure"
    url: https://openstax.org/books/biology-2e/pages/5-1-components-and-structure
  - title: "OpenStax Biology 2e, 5.2 Passive Transport"
    url: https://openstax.org/books/biology-2e/pages/5-2-passive-transport
  - title: "OpenStax Chemistry 2e, 11.4 Colligative Properties"
    url: https://openstax.org/books/chemistry-2e/pages/11-4-colligative-properties
  - title: "PhysiologyWeb, Nernst equilibrium potential (Table 1, typical mammalian ion concentrations)"
    url: https://physiologyweb.com/lecture_notes/resting_membrane_potential/resting_membrane_potential_nernst_equilibrium_potential.html
  - title: "OpenStax Anatomy and Physiology 2e, 12.4 The Action Potential"
    url: https://openstax.org/books/anatomy-and-physiology-2e/pages/12-4-the-action-potential
  - title: "NIST CODATA 2022: molar gas constant"
    url: https://physics.nist.gov/cgi-bin/cuu/Value?r
last_verified: "2026-10-16"
---

# 06.1 · Cells, membranes and compartments

A cell is a tiny bag of concentrated aqueous solution, wrapped in a film of grease only a few nanometres thick. To a chemist, almost everything a cell does follows from three facts: molecules move by diffusion, which is fast over short distances and hopelessly slow over long ones; the grease film lets only some molecules through; and the different solutions on each side of it store energy as concentration and charge differences. This lesson turns those facts into numbers, and you will measure the salt concentration that matches the inside of a potato.

## Why it matters

A hospital drip of "normal saline" is 0.9 % sodium chloride, never pure water. Pure water flowing into a vein would rush into red blood cells by osmosis until they burst. The 0.9 % figure is a chemistry result: it is the salt concentration whose particle count matches the inside of the cell, so water has no net reason to move. The same reasoning explains pickling, why a drug must be partly fat-soluble to enter cells, and why a nerve cell can fire. You will meet it again in the Nernst equation (Module 8), ion-selective electrodes (Module 10) and biochemistry (Module 29).

## Core ideas

> [!NOTE]
> The physics and chemistry here are stable. Cell sizes and membrane thickness are from OpenStax Biology 2e; ion concentrations are typical textbook values for mammalian cells (PhysiologyWeb), and real cells vary around them. $R$ and $F$ are CODATA 2022 values from NIST. Checked 2026-10-16.

### Cells are small because diffusion is slow over distance

Inside a cell, molecules move by diffusion: random thermal jostling that, on average, spreads them from high to low concentration. The typical time to wander a distance $x$ in one direction is

$$t \approx \frac{x^2}{2D}$$

where $D$ is the diffusion coefficient. For a small molecule such as glucose or O₂ in water, $D$ is about $10^{-9}$ m²/s; for a protein it is about ten times smaller. The square is the key. Across a human cell of 20 µm: $t = (2\times10^{-5})^2 / (2\times10^{-9}) = 0.2$ s. Across 1 cm of tissue: $5\times10^{4}$ s, about 14 hours. Prokaryotes (bacteria, 0.1–5 µm) and eukaryotic cells (10–100 µm) stay small so that diffusion can feed them. Bigger organisms need pumps and pipes: a heart, blood vessels, phloem.

Size also sets the surface-to-volume ratio: surface grows as $r^2$ and volume as $r^3$, so a cell twice as wide has half the membrane per unit of cytoplasm.

### The membrane is a self-assembled film

A phospholipid has a polar, charged head and two long hydrocarbon tails. A molecule with a water-loving part and a water-fearing part is called amphiphilic. In water, phospholipids arrange themselves into a bilayer: two sheets, tails facing each other inside, heads facing the water on both sides. Plasma membranes, with their proteins, are 5–10 nm thick; the oily core is about 3 nm.

It forms by itself, through the hydrophobic effect. Water molecules next to a hydrocarbon cannot hydrogen-bond to it, so they arrange into more ordered cages around it. Pushing the tails together frees much of that ordered water, and the entropy of the water rises. In the language of Module 8, $\Delta G = \Delta H - T\Delta S$ is negative mainly because $\Delta S$ of the water is positive. Soap does the same thing with one tail per molecule, which favours small spheres called micelles; two tails make a cylinder shape that packs into flat sheets.

### What crosses the bilayer

![A lipid bilayer with polar heads facing water on both sides and nonpolar tails in the middle. O2 and CO2 cross directly and fast, water crosses slowly on its own and quickly through an aquaporin, glucose needs a carrier protein, and ions such as K+ and Na+ need an ion channel](../../assets/m06-membrane.svg)

To cross, a molecule must leave water, dissolve in the oily core and come out the other side. So the rule is the chemist's "like dissolves like":

- Small nonpolar molecules (O₂, CO₂, N₂, steroid hormones) cross quickly.
- Small polar molecules (water, urea, ethanol) cross slowly; water also has its own protein channels, aquaporins.
- Larger polar molecules (glucose, amino acids) barely cross; they need carrier proteins.
- Ions (Na⁺, K⁺, Cl⁻, Ca²⁺) essentially never cross the lipid itself. Moving a charge from water (relative permittivity about 78) into oil (about 2) costs a huge Coulomb energy, as in lesson [04.3](../module-04/lesson-03.md). They need ion channels or pumps.

### Compartments keep different chemistry apart

A eukaryotic cell is divided by internal membranes into organelles: the nucleus (DNA), mitochondria (aerobic respiration), the endoplasmic reticulum and Golgi (making and shipping proteins), lysosomes (an acidic digestion compartment). Each keeps its own pH, ions and enzymes, so incompatible reactions run side by side.

### Osmosis: water follows the particles

When two solutions are separated by a membrane that lets water through but not solute, water moves towards the side with more dissolved particles. The driving force is measured by the osmotic pressure

$$\Pi = i c R T$$

where $c$ is the molar concentration, $T$ the absolute temperature, and $i$ the van 't Hoff factor: the number of particles each formula unit gives in solution (1 for sucrose, ideally 2 for NaCl, measured about 1.9). The product $ic$ is the osmolarity, in osmol/L. Use $c$ in mol/m³ (1 mol/L = 1000 mol/m³) and $R = 8.314$ J mol⁻¹ K⁻¹ to get pascals.

A cell in a solution of lower osmolarity than its inside (hypotonic) takes in water and swells. In a higher one (hypertonic) it loses water and shrinks. At equal osmolarity (isotonic) there is no net flow. Plant cells, like the potato's, have a stiff wall, so they swell only until the wall pushes back.

### Membrane potential: ions store energy as charge

Pumps in the membrane keep K⁺ high inside the cell and Na⁺ high outside. Typical mammalian values are K⁺ 150 mM inside and 4 mM outside, Na⁺ 15 mM inside and 145 mM outside. If the membrane let only K⁺ through, K⁺ would leak out until the negative charge left behind pulled it back. The voltage at which the two tendencies balance is the Nernst potential:

$$E_\text{ion} = \frac{RT}{zF}\ln\frac{c_\text{out}}{c_\text{in}}$$

with $z$ the ion's charge number and $F = 96\,485$ C/mol the Faraday constant. At 37 °C, $RT/F = 26.7$ mV. Real resting cells sit near −70 mV (inside negative), close to the K⁺ value because at rest the membrane is mostly permeable to K⁺. Module 8 derives this equation properly for electrochemical cells; here it is the same physics in a cell.

## Worked example

### 1. The K⁺ equilibrium potential

At 37 °C (310.15 K), with K⁺ 150 mM inside and 4 mM outside:

$$E_\text{K} = \frac{8.314 \times 310.15}{1 \times 96\,485}\ln\frac{4}{150} = 0.02673 \times (-3.624) = -0.0969\ \text{V} = -96.9\ \text{mV}$$

Interpretation: the inside must be 97 mV negative to hold K⁺ in. The energy to move one mole of K⁺ across 70 mV is $zF\Delta V = 96\,485 \times 0.070 = 6.8$ kJ/mol, comparable to a weak hydrogen bond. The field across a 5 nm membrane is $0.070 / 5\times10^{-9} = 1.4\times10^{7}$ V/m, strong enough to move charged parts of channel proteins.

### 2. Why saline is 0.9 %

0.9 % (w/v) NaCl is 9.0 g per litre. With $M$ = 58.44 g/mol, $c = 9.0 / 58.44 = 0.154$ mol/L, so the osmolarity is about $2 \times 0.154 = 0.308$ osmol/L (a little less with $i$ = 1.9). At 37 °C:

$$\Pi = 0.308 \times 1000 \times 8.314 \times 310.15 = 7.9\times10^{5}\ \text{Pa} \approx 7.9\ \text{bar}$$

Interpretation: blood plasma has about the same osmolarity, so saline causes no net flow. Against pure water the push is nearly 8 atmospheres, which a lipid film cannot resist.

## Hands-on

### Part A — the isotonic point of a potato (home, about 2 h 30 min including soaking)

> [!WARNING]
> Kitchen materials only: potatoes, table salt and tap water. Cut away from your fingers on a board; an apple corer or chip cutter is safer than a knife. Wipe salt water off the scale at once. Do not eat the soaked potato. Do the risk assessment from lesson [01.4](../module-01/lesson-04.md) first.

What you need: one large raw potato, table salt, six cups or jars, a 20 mL oral syringe, a ruler, kitchen paper, a marker, a scale (a 0.01 g pocket scale is strongly recommended; with a 1 g kitchen scale use about 40 g of potato per cup and expect a larger uncertainty), the [Module 6 lab folder](../../labs/module-06/) and a [notebook page](../../templates/notebook-page.md).

Steps:

1. Make a 0.50 mol/L stock: weigh 14.6 g of salt (write the actual reading), dissolve it in water and make it up to 500 mL in a measuring jug. Your concentration is (mass / 58.44) / 0.500 L.
2. Make 50 mL each of 0, 0.1, 0.2, 0.3, 0.4 and 0.5 mol/L by mixing stock and water with the syringe (for 0.1: 10 mL stock + 40 mL water). Label the cups.
3. Cut 18 strips of about 1 × 1 × 4 cm from the same potato, without skin. Same size matters more than exact size.
4. Blot each strip, weigh it, and put three into each cup. Record `c_NaCl_M,strip,m_before_g` in a CSV like `osmosis_example.csv`.
5. Leave for 2 hours at room temperature. Take the strips out, blot each one the same way (one roll on paper, no squeezing), and weigh it again (`m_after_g`).
6. Complete the four TODO functions in `lesson01_osmosis.py`, test on the example data, then run on yours:

```bash
py lesson01_osmosis.py
py lesson01_osmosis.py my_potato.csv
```

The script computes the percentage mass change of each strip, fits a straight line to the points from 0 to 0.3 mol/L, finds where it crosses zero (the isotonic point) with its uncertainty, and converts it to osmolarity and osmotic pressure. It also prints diffusion times and Nernst potentials for the ions in the Core ideas.

How you know it worked: on the example data the isotonic point is 0.145 ± 0.005 mol/L NaCl, about 0.29 osmol/L, or 7.1 bar at 22 °C. The strips in water gain about 9 %, those in 0.5 mol/L lose about 14 %. The Nernst potentials are −96.9 mV (K⁺), +60.6 mV (Na⁺) and −64.1 mV (Cl⁻). Your potato will give its own value; it depends on the variety and how long it has been stored.

<details><summary>Reference solution and how to read your result</summary>

`diffusion_time`: `x**2 / (2*D)`. `osmotic_pressure`: `c_osm * 1000 * R * T`. `isotonic_point`: mask, `np.polyfit(c[m], pct[m], 1, cov=True)`, `c0 = -b/s`, and propagation with partial derivatives as in lesson [02.5](../module-02/lesson-05.md). `nernst`: `R*T/(z*F)*np.log(c_out/c_in)`. Full code: `lesson01_osmosis_solution.py`.

Why fit only up to 0.3 mol/L: the response flattens at both ends (a strip cannot lose more water than it has, and the cell wall stops swelling), so a straight line through all points tilts and moves the crossing. On the example data the all-points fit gives 0.151 ± 0.010 instead of 0.145 ± 0.005. Fit where the curve is close to straight and the crossing lies inside the data.

Errors to name in your notebook: unequal blotting (the largest), strips from different parts of the potato, evaporation, and a biased syringe (calibrate it as in lesson [01.5](../module-01/lesson-05.md)). Two hours is not full equilibrium, but at the isotonic point there is no flow at any time, so the crossing is still valid.

</details>

## Common mistakes

- Using $x/D$ or $x/2D$ for diffusion time. The time grows with distance squared; check the units, m² divided by m²/s gives seconds.
- Forgetting the van 't Hoff factor. 0.15 mol/L NaCl is about 0.30 osmol/L, the same particle count as 0.30 mol/L glucose.
- Using mol/L in $\Pi = icRT$ with $R$ = 8.314. That gives kPa-sized numbers a thousand times too small; convert to mol/m³ or use $R$ = 0.08206 L atm mol⁻¹ K⁻¹.
- Swapping inside and outside in the Nernst equation. The sign check: K⁺ is high inside, so the inside must be negative to hold it; $E_\text{K}$ must come out negative.
- Fitting a straight line through saturated points in the potato data. Look at the plot first, then choose the window.

## Key takeaways

- Diffusion time grows as distance squared: fractions of a second across a cell, hours across a centimetre. That is why cells are small.
- Bilayers assemble by themselves through the hydrophobic effect; small nonpolar molecules cross them, ions and large polar molecules need proteins.
- Water moves towards higher osmolarity; $\Pi = icRT$ gives the size of that push, about 8 bar for blood against pure water.
- Concentration differences across a membrane create a voltage, the Nernst potential, about −97 mV for K⁺ in a typical cell.
- Membranes divide a cell into compartments that run different chemistry side by side.

## Sources

- [OpenStax Biology 2e, 4.2 Prokaryotic Cells](https://openstax.org/books/biology-2e/pages/4-2-prokaryotic-cells) — cell sizes and the surface-to-volume argument.
- [OpenStax Biology 2e, 5.1 Components and Structure](https://openstax.org/books/biology-2e/pages/5-1-components-and-structure) — the fluid mosaic membrane, amphiphilic lipids, thickness 5–10 nm.
- [OpenStax Biology 2e, 5.2 Passive Transport](https://openstax.org/books/biology-2e/pages/5-2-passive-transport) — selective permeability, osmosis and tonicity.
- [OpenStax Chemistry 2e, 11.4 Colligative Properties](https://openstax.org/books/chemistry-2e/pages/11-4-colligative-properties) — osmotic pressure and the van 't Hoff factor (measured $i$ = 1.9 for dilute NaCl).
- [PhysiologyWeb, Nernst equilibrium potential](https://physiologyweb.com/lecture_notes/resting_membrane_potential/resting_membrane_potential_nernst_equilibrium_potential.html) — typical mammalian ion concentrations and equilibrium potentials at 37 °C.
- [OpenStax Anatomy and Physiology 2e, 12.4 The Action Potential](https://openstax.org/books/anatomy-and-physiology-2e/pages/12-4-the-action-potential) — resting potential about −70 mV.
- [NIST CODATA 2022: molar gas constant](https://physics.nist.gov/cgi-bin/cuu/Value?r) — $R$.
