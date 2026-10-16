---
id: "04.1"
module: 4
minutes: 20
practice_minutes: 60
prerequisites: ["01.2", "02.2", "02.3"]
objectives:
  - Compute the kinetic energy, speed and momentum of a gas molecule from its molar mass and temperature, in SI units.
  - Obtain a force from a potential-energy curve as F = −dU/dx and locate the equilibrium and the largest restoring force.
  - Calculate the work needed to stretch a bond by integrating the force, and compare it with the thermal energy kT.
  - Convert energies between J per molecule, kJ/mol and eV without losing a factor of Avogadro's number.
volatility: concept
sources:
  - title: "OpenStax University Physics Volume 1, 7.2 Kinetic Energy"
    url: https://openstax.org/books/university-physics-volume-1/pages/7-2-kinetic-energy
  - title: "OpenStax University Physics Volume 1, 8.4 Potential Energy Diagrams and Stability"
    url: https://openstax.org/books/university-physics-volume-1/pages/8-4-potential-energy-diagrams-and-stability
  - title: "OpenStax University Physics Volume 1, 9.1 Linear Momentum"
    url: https://openstax.org/books/university-physics-volume-1/pages/9-1-linear-momentum
  - title: "OpenStax Chemistry 2e, 9.5 The Kinetic-Molecular Theory"
    url: https://openstax.org/books/chemistry-2e/pages/9-5-the-kinetic-molecular-theory
  - title: "NIST Chemistry WebBook: Hydrogen chloride, constants of diatomic molecules"
    url: https://webbook.nist.gov/cgi/cbook.cgi?ID=C7647010&Mask=1000
  - title: "Hu, Melville and Hepburn (2003), threshold ion-pair spectroscopy of HCl, J. Chem. Phys. 119, 8938 (abstract)"
    url: https://chem.ubc.ca/node/8128
  - title: "NIST CODATA 2022: Boltzmann constant"
    url: https://physics.nist.gov/cgi-bin/cuu/Value?k
  - title: "MIT OpenCourseWare 8.01SC Classical Mechanics"
    url: https://ocw.mit.edu/courses/8-01sc-classical-mechanics-fall-2016/
last_verified: "2026-10-16"
---

# 04.1 · Forces, energy and momentum

Chemistry runs on mechanics at the scale of molecules. Gas pressure is molecules bouncing off walls, a chemical bond is a valley in a potential-energy curve, and every kJ/mol you will ever quote is, at bottom, work done by a force. This lesson gives you the four ideas physics contributes, force, work, energy and momentum, with molecular numbers in SI units. You then compute the force inside an HCl bond from its energy curve in Python.

## Why it matters

Suppose a colleague asks whether HCl gas could fall apart into H and Cl just from bumping into other molecules at room temperature. You can answer in one line once you can compare energies: a typical collision carries about $kT \approx 0.026$ eV, while the H–Cl bond needs about 4.4 eV. That is a factor of 170, so ordinary collisions cannot break it; light or a flame can. The same comparison decides which reactions go at room temperature, why a catalyst helps, and why gases at the same temperature have the same average kinetic energy. Gas laws (Module 7), thermodynamics (Module 13) and kinetics (Module 22) all build on it.

## Core ideas

> [!NOTE]
> Newtonian mechanics is stable and needs no update. Constants are CODATA 2022 values from NIST ($k_B$, $N_A$ and $h$ are exact by definition of the SI). The HCl bond data are from the NIST Chemistry WebBook and a 2003 measurement of the bond energy, checked 2026-10-16.

### Force and Newton's second law

A force is a push or a pull. Its SI unit is the newton: $1\ \mathrm{N} = 1\ \mathrm{kg\,m\,s^{-2}}$. Newton's second law links force to motion:

$$F = m a = m\frac{dv}{dt}$$

Here $m$ is mass and $a$ is acceleration, the rate of change of velocity $v$ (lesson [02.2](../module-02/lesson-02.md)). Force and velocity are vectors: they have a size and a direction. In this module we mostly work along one line, so a sign carries the direction.

Tiny example: a 1.0 kg book feels a gravitational force $F = mg = 1.0 \times 9.81 = 9.8$ N.

### Work and kinetic energy

Work is force times the distance moved along the force. For a force that changes with position, it is an integral (lesson [02.3](../module-02/lesson-03.md)):

$$W = \int_{x_1}^{x_2} F(x)\,dx$$

The unit is the joule: $1\ \mathrm{J} = 1\ \mathrm{N\,m}$. Work done on an object changes its kinetic energy, the energy of motion:

$$E_k = \tfrac12 m v^2$$

This is the work–energy theorem. Lifting the 1.0 kg book by 1.5 m takes $W = 9.8 \times 1.5 = 15$ J.

### Potential energy and force as a slope

Some forces store the work you do against them as potential energy $U$, energy of position. Gravity, springs and the electric force between charges are of this kind; they are called conservative forces. The force is minus the slope of the potential energy:

$$F(x) = -\frac{dU}{dx}$$

The minus sign means the force pushes downhill, towards lower $U$. Where the curve has a minimum, the slope is zero, so the force is zero: that is an equilibrium. On either side of the minimum the force points back towards it.

A chemical bond is exactly this. Plot the energy of two atoms against their distance $r$ and you get a well. Its bottom sits at the bond length $r_e$; its depth $D_e$ is the energy needed to pull the atoms apart. A common model is the Morse potential:

$$U(r) = D_e\left(1 - e^{-a(r - r_e)}\right)^2$$

The parameter $a$ sets the width of the well. Near the bottom it looks like a parabola, $U \approx \tfrac12 k (r - r_e)^2$, which is a spring with force constant $k = 2D_e a^2$. Lesson [04.2](lesson-02.md) uses that spring to explain infrared spectra.

### Conservation of energy

Without friction, kinetic plus potential energy stays constant. An atom in a bond trades kinetic for potential energy as it vibrates, just like a mass on a spring. With friction, mechanical energy seems to vanish, but it becomes the random motion of molecules, which is heat. Thermodynamics (Module 8) is the bookkeeping of that conversion. Energy is never lost, only moved or changed in form.

### Momentum and collisions

Momentum is mass times velocity, $p = mv$, in kg m/s. Newton's second law can be written $F = dp/dt$: a force is a rate of momentum change. When two objects collide, the forces between them are equal and opposite, so the total momentum is conserved in every collision.

Kinetic energy is conserved only in elastic collisions. Gas molecules colliding with each other at room temperature are close to elastic. A molecule of mass $m$ hitting a wall head-on at speed $v$ and bouncing back changes its momentum from $+mv$ to $-mv$, a change of $2mv$. Billions of such impacts per second per square millimetre are what a pressure gauge reads. Module 7 builds the gas laws on this.

### Per molecule, per mole, and electronvolts

Chemists use three energy scales. Mixing them up is the most common error in this module.

| Scale | Unit | Typical use | Link |
|---|---|---|---|
| Per molecule | J | physics formulas | — |
| Per mole | kJ/mol | reaction energies | multiply J by $N_A = 6.022\times10^{23}\ \mathrm{mol^{-1}}$ |
| Per molecule | eV | bonds, photons, electrochemistry | $1\ \mathrm{eV} = 1.602\times10^{-19}$ J = 96.49 kJ/mol |

The thermal energy scale is $k_BT$ per molecule or $RT$ per mole. At 298.15 K, $k_BT = 4.12\times10^{-21}$ J = 0.0257 eV and $RT = 2.48$ kJ/mol. The average kinetic energy of a gas molecule is $\tfrac32 k_BT$, whatever the gas.

## Worked example

### 1. A nitrogen molecule at room temperature

Find the average kinetic energy, the root-mean-square (rms) speed and the momentum change at a wall for N₂ at 298.15 K. The molar mass is 28.0134 g/mol.

- Mass of one molecule: $m = 0.0280134\ \mathrm{kg\,mol^{-1}} / 6.02214\times10^{23}\ \mathrm{mol^{-1}} = 4.652\times10^{-26}$ kg. Note grams converted to kilograms first.
- Average kinetic energy: $\tfrac32 k_BT = 1.5 \times 1.380649\times10^{-23} \times 298.15 = 6.17\times10^{-21}$ J. Per mole that is 3.72 kJ/mol.
- Setting $\tfrac12 m v_\text{rms}^2 = \tfrac32 k_BT$ gives $v_\text{rms} = \sqrt{3RT/M} = \sqrt{3 \times 8.314 \times 298.15 / 0.0280134} = 515$ m/s, faster than a passenger jet.
- A head-on bounce at that speed changes the momentum by $2mv = 2 \times 4.652\times10^{-26} \times 515 = 4.79\times10^{-23}$ kg m/s.

Interpretation: each impact is tiny. Pressure is large only because there are about $2.5\times10^{25}$ molecules in every cubic metre of air.

### 2. The force inside an HCl bond

For H³⁵Cl, NIST gives $r_e = 0.12746$ nm. The measured bond energy from the lowest vibrational level is $D_0 = 35\,748\ \mathrm{cm^{-1}}$ (4.43 eV); adding the zero-point energy gives the well depth $D_e = 4.62$ eV $= 7.40\times10^{-19}$ J. The force constant is $k = 516$ N/m (derived in lesson 04.2), so $a = \sqrt{k/2D_e} = 1.87\times10^{10}\ \mathrm{m^{-1}}$.

Where is the restoring force largest? Differentiate the Morse curve twice and set the result to zero: the steepest point is at $r = r_e + \ln 2 / a = 0.1275 + 0.0371 = 0.1646$ nm, and there $|F| = D_e a / 2 = 7.40\times10^{-19} \times 1.87\times10^{10} / 2 = 6.9\times10^{-9}$ N, about 7 nN. Pull harder than that and the bond cannot hold you back; it breaks.

How much work does it take to stretch the bond by only 0.01 nm? The Morse formula gives $U(r_e + 0.01\ \mathrm{nm}) = 2.15\times10^{-20}$ J. That is $5.2\,k_BT$ at room temperature, and the harmonic (spring) formula $\tfrac12 k x^2 = 2.58\times10^{-20}$ J overestimates it by about 20 %, because the real well widens as you pull.

## Hands-on

### Part A — pencil (20 min)

1. Lifting a 1.0 kg book by 1.5 m takes 15 J. The HCl well depth is 445 kJ/mol. How many moles of HCl bonds could that work break?
2. Find the rms speed of argon ($M$ = 39.948 g/mol) at 298.15 K. Is it faster or slower than N₂, and why?
3. An N₂ molecule at 500 m/s hits a stationary N₂ head-on and the collision is elastic. Show that the first molecule stops and the second moves off at 500 m/s, by checking momentum and kinetic energy.
4. For a spring, $U = \tfrac12 k x^2$. Use $F = -dU/dx$ to find the force law.

<details><summary>Answers to Part A</summary>

1. $15\ \mathrm{J} / 445\,000\ \mathrm{J\,mol^{-1}} = 3.4\times10^{-5}$ mol. Chemical energies per mole are large: the work of lifting a book breaks only a tiny amount of bonds.
2. $\sqrt{3 \times 8.314 \times 298.15 / 0.039948} = 431$ m/s. Slower than N₂ (515 m/s): same average kinetic energy, heavier atom, so lower speed.
3. Before: $p = m \times 500$, $E_k = \tfrac12 m \times 500^2$. After: the same totals, with the velocities swapped. Any other outcome would break one of the two conservation laws for equal masses.
4. $F = -kx$, Hooke's law: the force is proportional to the displacement and points back to $x = 0$.

</details>

### Part B — Python: a bond as a potential well (40 min)

What you need: Python with the course packages and the [Module 4 lab folder](../../labs/module-04/). Setup steps are in the lab README.

1. Open `lesson01_morse.py`. The HCl constants are already set at the top, with their sources.
2. Fill in `morse_energy(r)` using the formula above.
3. Fill in `force(r, U)` with a numerical derivative, `-np.gradient(U, r)`, exactly the method of lesson 02.2.
4. Fill in `work_to_stretch(r, F, r1, r2)` with the trapezoid rule, as in lesson 02.3.
5. Run it and look at the plot in `runs/lesson01_morse.png`:

```bash
py lesson01_morse.py
```

How you know it worked: the force is zero at 0.1275 nm, the largest restoring force is 6.9 nN at 0.1646 nm, the work to stretch by 0.01 nm is about $2.1\times10^{-20}$ J (about 5 $k_BT$), and the harmonic estimate is about 20 % too high. Your numerical answers should agree with the pencil formulas of Worked example 2 to within 1–2 %.

<details><summary>Reference solution</summary>

`morse_energy`: `DE * (1 - np.exp(-A * (r - RE)))**2`. `force`: `-np.gradient(U, r)`. `work_to_stretch`: build a mask `m = (r >= r1) & (r <= r2)` and return `-np.trapezoid(F[m], r[m])`. Full code: `lesson01_morse_solution.py`.

The small difference from the exact $2.15\times10^{-20}$ J comes from the grid: the mask starts at the first grid point after $r_e$, not exactly at $r_e$. A finer grid shrinks it. The plot shows the key physics: the Morse curve and the parabola agree at the bottom, but the Morse curve flattens out at large $r$ (the bond breaks) and rises steeply at small $r$ (atoms repel when squeezed).

Record the results on a [notebook page](../../templates/notebook-page.md): constants and sources, the three numbers, and one sentence on why kT is so much smaller than $D_e$.

</details>

## Common mistakes

- Using grams instead of kilograms. Molar mass in g/mol must become kg/mol before it goes into $\sqrt{3RT/M}$. Using 28.0 instead of 0.0280 gives a speed 32 times too small.
- Mixing per molecule and per mole. $k_B$ goes with J per molecule; $R$ goes with J per mole. If a bond energy comes out as $10^{-19}$ kJ/mol, you forgot $N_A$.
- Dropping the minus sign in $F = -dU/dx$. The force points downhill. A positive slope means the force pulls towards smaller $x$.
- Taking the momentum change at a wall as $mv$. The molecule reverses, so the change is $2mv$.
- Assuming kinetic energy is always conserved. Momentum is conserved in every collision; kinetic energy only in elastic ones.
- Treating the bond as a perfect spring far from the bottom. The harmonic model works for small stretches only; large ones need the full curve.

## Key takeaways

- Force is the rate of change of momentum, $F = dp/dt = ma$; work is the integral of force over distance.
- A conservative force is minus the slope of its potential energy; equilibrium sits at the minimum.
- A chemical bond is a potential well: depth $D_e$, position $r_e$, and near the bottom a spring of constant $k = 2D_e a^2$.
- Momentum is conserved in every collision; pressure comes from momentum transfer to walls.
- Compare energies on one scale: $k_BT$ (0.026 eV) against bond energies (a few eV) tells you what heat alone can do.

## Sources

- [OpenStax University Physics Volume 1, 7.2 Kinetic Energy](https://openstax.org/books/university-physics-volume-1/pages/7-2-kinetic-energy) — work and kinetic energy.
- [OpenStax University Physics Volume 1, 8.4 Potential Energy Diagrams and Stability](https://openstax.org/books/university-physics-volume-1/pages/8-4-potential-energy-diagrams-and-stability) — force as the slope of a potential, equilibrium points.
- [OpenStax University Physics Volume 1, 9.1 Linear Momentum](https://openstax.org/books/university-physics-volume-1/pages/9-1-linear-momentum) — momentum and Newton's second law in momentum form.
- [OpenStax Chemistry 2e, 9.5 The Kinetic-Molecular Theory](https://openstax.org/books/chemistry-2e/pages/9-5-the-kinetic-molecular-theory) — average kinetic energy and rms speed of gas molecules.
- [NIST Chemistry WebBook: Hydrogen chloride, diatomic constants](https://webbook.nist.gov/cgi/cbook.cgi?ID=C7647010&Mask=1000) — $r_e$, $\omega_e$ and $\omega_e x_e$ of H³⁵Cl.
- [Hu, Melville and Hepburn (2003), J. Chem. Phys. 119, 8938](https://chem.ubc.ca/node/8128) — the measured HCl bond energy $D_0 = 35\,748.2\ \mathrm{cm^{-1}}$.
- [NIST CODATA 2022: Boltzmann constant](https://physics.nist.gov/cgi-bin/cuu/Value?k) — exact value of $k_B$.
- [MIT OCW 8.01SC Classical Mechanics](https://ocw.mit.edu/courses/8-01sc-classical-mechanics-fall-2016/) — the full course for depth.
