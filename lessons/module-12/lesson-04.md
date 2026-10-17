---
id: "12.4"
module: 12
minutes: 20
practice_minutes: 50
prerequisites: ["12.2", "03.4"]
objectives:
  - Compute harmonic-oscillator levels and the zero-point energy of a diatomic molecule from its vibrational wavenumber.
  - Describe the shape, nodes and parity of the oscillator wavefunctions and where they leak beyond the classical turning points.
  - Predict the fundamental, the first overtone and the dissociation behaviour from the anharmonic constants omega_e and omega_e x_e.
  - Predict an isotope shift and the zero-point energy difference behind a kinetic isotope effect.
volatility: concept
sources:
  - title: "NIST Chemistry WebBook: hydrogen chloride, constants of diatomic molecules"
    url: https://webbook.nist.gov/cgi/cbook.cgi?ID=C7647010&Mask=1000
  - title: "LibreTexts Physical Chemistry, chapter 5: The Harmonic Oscillator and the Rigid Rotor"
    url: https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Physical_Chemistry_(LibreTexts)/05%3A_The_Harmonic_Oscillator_and_the_Rigid_Rotor
  - title: "NIST Atomic Weights and Isotopic Compositions"
    url: https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl
  - title: "MIT OpenCourseWare 5.61 Physical Chemistry (Field, Fall 2017)"
    url: https://ocw.mit.edu/courses/5-61-physical-chemistry-fall-2017/
last_verified: "2026-10-17"
---

# 12.4 · The harmonic oscillator and molecular vibrations

A chemical bond behaves like a spring, as you saw in [03.4](../module-03/lesson-04.md). Quantum mechanics adds two things a classical spring does not have: the vibrational energy comes in equal steps, and the lowest level is not at rest but holds a zero-point energy. Real bonds are not perfect springs, so the steps shrink as the molecule climbs towards breaking. This lesson solves the quantum oscillator, then upgrades it to the anharmonic Morse oscillator and checks both against the measured constants of HCl from the NIST WebBook.

## Why it matters

An infrared spectrum is a list of vibrational energy gaps. To assign a band, decide whether it is a fundamental or an overtone, or predict where it moves when you deuterate a sample, you need the oscillator's energy levels. The zero-point energy matters far beyond spectroscopy: it is part of every bond energy, it makes C–H bonds break faster than C–D bonds (the kinetic isotope effect used to prove mechanisms in Module 28), and it explains why near-infrared analysers that measure moisture in grain work at all, on weak overtones that a perfect spring would not have.

## Core ideas

> [!NOTE]
> The theory is stable. The HCl constants are the NIST Chemistry WebBook values (from Huber and Herzberg) and the masses are NIST atomic masses, checked 2026-10-17. The lab uses the solver `qm_solver.py` with numpy 2.5 and scipy 1.18.

### The quantum harmonic oscillator

A diatomic molecule with reduced mass $\mu$ and force constant $k$ has, near the bottom of its well, $V(x) = \tfrac12 kx^2$, where $x = r - r_e$ is the stretch from the equilibrium bond length $r_e$. The Schrödinger equation with this potential has exact solutions:

$$E_v = \left(v + \tfrac12\right)\hbar\omega,\qquad \omega = \sqrt{\frac{k}{\mu}},\qquad v = 0, 1, 2, \dots$$

where $v$ is the vibrational quantum number. In spectroscopic units, $G(v) = \omega_e(v + \tfrac12)$ in cm⁻¹, with $\omega_e = \omega/(2\pi c)$. Three facts follow:

- The levels are equally spaced, by $\hbar\omega$.
- The lowest level, $v = 0$, has the zero-point energy $\tfrac12\hbar\omega$. The molecule can never stop vibrating.
- The spacing depends on $k$ and $\mu$ only through $\sqrt{k/\mu}$, as classically.

Tiny example: H³⁵Cl has $\omega_e = 2990.95$ cm⁻¹. Its harmonic zero-point energy is 1495 cm⁻¹, or 17.9 kJ/mol (1 cm⁻¹ = 0.0119627 kJ/mol).

### The wavefunctions

The oscillator wavefunctions are a Gaussian times a polynomial:

$$\psi_v(x) = N_v\,H_v(x/\alpha)\,e^{-x^2/2\alpha^2},\qquad \alpha = \sqrt{\frac{\hbar}{\mu\omega}}$$

$H_v$ is the Hermite polynomial of degree $v$ ($H_0 = 1$, $H_1 = 2y$, $H_2 = 4y^2 - 2$) and $N_v$ a normalisation constant. The length $\alpha$ sets the size of the zero-point motion: for HCl, $\alpha = 0.107$ Å, about 8 % of the 1.275 Å bond.

- $\psi_v$ has $v$ nodes, like the box.
- Even $v$ are symmetric about $x = 0$ and odd $v$ antisymmetric. This parity decides the selection rules in [12.6](lesson-06.md).
- The wavefunction extends beyond the classical turning points, where $V = E$, with a decaying tail: the same leakage as under a barrier in [12.3](lesson-03.md).
- At high $v$ the probability piles up near the turning points, where a classical spring moves slowest. Quantum and classical pictures merge.

An oscillating dipole absorbs light only for $\Delta v = \pm1$ in the harmonic model, so a harmonic diatomic shows one IR band at $\omega_e$. You derive this rule numerically in 12.6.

[Simulation: Quantum box — harmonic oscillator levels and wavefunctions](../../simulations/quantum-box/index.html?preset=oscillator)

### Real bonds are anharmonic

Stretch a real bond far enough and it breaks; a parabola never does. A good model of a real bond is the Morse potential

$$V(x) = D_e\left(1 - e^{-ax}\right)^2$$

$D_e$ is the well depth (the dissociation energy measured from the bottom) and $a$ sets its width. Near $x = 0$ it is a parabola with $k = 2D_ea^2$; at large $x$ it flattens to $D_e$. Its levels are, exactly,

$$G(v) = \omega_e\left(v + \tfrac12\right) - \omega_e x_e\left(v + \tfrac12\right)^2$$

The anharmonicity constant $\omega_e x_e$ makes the gaps shrink as $v$ rises: $G(v+1) - G(v) = \omega_e - 2\omega_e x_e(v + 1)$. The levels crowd together towards the dissociation limit, with $D_e = \omega_e^2/(4\omega_e x_e)$. Anharmonicity also relaxes the selection rule: overtones ($\Delta v = 2, 3, \dots$) appear, weakly. Tables such as the NIST WebBook give $\omega_e$ and $\omega_e x_e$ (and sometimes a cubic term $\omega_e y_e$) for each diatomic molecule; these are the constants you will use in Module 20.

### Isotopes: same potential, new mass

Electrons are so much lighter than nuclei that the potential energy curve does not depend on which isotope sits at each end (the Born–Oppenheimer approximation, Module 20). Swapping H for D keeps $k$ and $D_e$ but changes $\mu$, so $\omega_e \propto \mu^{-1/2}$ and $\omega_e x_e \propto \mu^{-1}$. The heavier molecule has lower vibrational levels and a smaller zero-point energy. If a reaction breaks that bond, the D compound starts lower in the well and needs more energy to reach the top: this is the semi-classical kinetic isotope effect.

## Worked example

### 1. The HCl spectrum from the NIST constants

NIST gives for H³⁵Cl: $\omega_e = 2990.9463$ cm⁻¹, $\omega_e x_e = 52.8186$ cm⁻¹ (and a small $\omega_e y_e = 0.22437$ cm⁻¹, ignored here).

1. Zero-point energy: $G(0) = \omega_e/2 - \omega_e x_e/4 = 1495.47 - 13.20 = 1482.3$ cm⁻¹.
2. Fundamental $0 \to 1$: $G(1) - G(0) = \omega_e - 2\omega_e x_e = 2990.95 - 105.64 = 2885.3$ cm⁻¹. The observed band centre is 2886 cm⁻¹.
3. First overtone $0 \to 2$: $G(2) - G(0) = 2\omega_e - 6\omega_e x_e = 5981.89 - 316.91 = 5665.0$ cm⁻¹, not $2 \times 2885.3 = 5770.6$. Adding the cubic term gives 5668.5 cm⁻¹.
4. Morse well depth: $D_e = 2990.95^2/(4 \times 52.82) = 42\,340$ cm⁻¹ $= 5.25$ eV. Subtract the zero-point energy for the energy needed from $v = 0$: $D_0 = 40\,860$ cm⁻¹ $= 5.07$ eV.

The measured bond energy is $D_0 = 4.43$ eV ([04.5](../module-04/lesson-05.md)). The Morse model built only from the two lowest-level constants overestimates it by 14 %: it is excellent near the bottom of the well and approximate near the top.

### 2. Deuterium chloride and the isotope effect

$\mu(\mathrm{H^{35}Cl}) = 0.97959$ u and $\mu(\mathrm{D^{35}Cl}) = 1.90441$ u, ratio 0.51438.

1. $\omega_e(\mathrm{DCl}) = 2990.95 \times \sqrt{0.51438} = 2145.1$ cm⁻¹; $\omega_e x_e(\mathrm{DCl}) = 52.82 \times 0.51438 = 27.17$ cm⁻¹.
2. Predicted fundamental: $2145.1 - 2 \times 27.17 = 2090.8$ cm⁻¹, a shift of 795 cm⁻¹ from HCl.
3. Zero-point energies: HCl 1482.3, DCl $1072.6 - 6.8 = 1065.8$ cm⁻¹. Difference 416.5 cm⁻¹ $= 4.98$ kJ/mol.

If this bond were completely broken at the transition state, the D molecule would face a barrier 4.98 kJ/mol higher. At 298 K that slows it by $e^{4.98/2.479} = 7.5$. This is where the "up to about 7" classical isotope effect of [12.3](lesson-03.md) comes from.

## Hands-on

What you need: pencil and calculator; Python with the course packages and the [Module 12 lab folder](../../labs/module-12/); a browser for the NIST WebBook. Time: about 50 minutes.

### Part A — real data and pencil (15 min)

1. Open the [NIST WebBook HCl diatomic constants](https://webbook.nist.gov/cgi/cbook.cgi?ID=C7647010&Mask=1000) and find $\omega_e$, $\omega_e x_e$ and $r_e$ for the ground state X ¹Σ⁺. Confirm the values used in this lesson.
2. Using only $\omega_e$ and $\omega_e x_e$, predict the $1 \to 2$ hot band (absorption from $v = 1$). Why is it weak at room temperature?
3. H³⁷Cl has $\mu = 0.98108$ u. By how many cm⁻¹ is its fundamental below that of H³⁵Cl? Would you see both in a high-resolution spectrum?

<details><summary>Answers to Part A</summary>

1. $\omega_e = 2990.9463$, $\omega_e x_e = 52.8186$ cm⁻¹, $r_e = 1.274552$ Å.
2. $G(2) - G(1) = \omega_e - 4\omega_e x_e = 2779.7$ cm⁻¹. It is weak because almost no molecules are in $v = 1$: the fraction is about $e^{-2886/207} \approx 10^{-6}$ at 298 K ($k_BT/hc = 207$ cm⁻¹).
3. $\omega \propto \mu^{-1/2}$: the fundamental scales by $\sqrt{0.97959/0.98108} = 0.99924$, so it is about 2.2 cm⁻¹ lower. Yes: natural chlorine is about 3:1 ³⁵Cl:³⁷Cl, and every rotational line of the HCl band is a doublet with that intensity ratio (Module 20).

</details>

### Part B — Python: Morse HCl with the numerical solver (35 min)

1. Open `lesson04_vib.py`. Fill in `reduced_mass` and `morse_params` (the formulas are in the docstring and in Core ideas).
2. Run it from the lab folder:

```bash
py lesson04_vib.py
```

3. Look at `runs/lesson04_vib.png`: the Morse curve, the harmonic parabola, and the first six levels with their wavefunctions.
4. Record the level table, the fundamental and overtone, and the bond lengths in a [notebook page](../../templates/notebook-page.md).

How you know it worked:

- $\mu = 0.979593$ u, $D_e = 42\,342$ cm⁻¹ (5.25 eV), $a = 1.7519$ Å⁻¹, $k = 516$ N/m (the value from [03.4](../module-03/lesson-04.md)).
- Harmonic levels 1495.5, 4486.4, 7477.3 cm⁻¹, equally spaced. Morse levels 1482.3, 4367.5, 7147.2, 9821.2 cm⁻¹, matching the Morse formula to 0.2 cm⁻¹; the node count is 0, 1, 2, ...
- Fundamental: harmonic 2990.9, Morse 2885.3, NIST constants 2886.0 cm⁻¹. Overtone: 5981.8, 5664.9 and 5668.5 cm⁻¹.
- Average bond length grows from 1.290 Å ($v = 0$) to 1.389 Å ($v = 3$).
- D³⁵Cl: predicted fundamental 2090.8 cm⁻¹, ratio 0.725 to HCl.

<details><summary>Reference solution and what to notice</summary>

`reduced_mass` returns `m1 * m2 / (m1 + m2)`. `morse_params` computes `De = we**2 / (4 * wexe)`, `k = we**2 / (2 * c)` with `c = HB2M_U_CM_A2 / mu` (that is $\hbar^2/2\mu$ in cm⁻¹ Å²), and `a = np.sqrt(k / (2 * De))`. Full code: `lesson04_vib_solution.py`.

What to notice: the ground state is already 0.015 Å longer than $r_e$ because the Morse well is softer on the stretched side. That is why a bond length measured from the rotational constant of $v = 0$ ($r_0$) is longer than $r_e$, as you will see in 12.5. The numerical levels drift above the NIST values at high $v$ because the real potential is not exactly Morse; the small $\omega_e y_e$ term in the NIST table captures part of that.

</details>

Then open the simulation with the `oscillator` preset. Switch on anharmonicity and check that the level spacing shrinks as you go up, and that the $v = 0$ wavefunction leaks past the classical turning points.

## Common mistakes

- Forgetting the zero-point energy and putting $v = 0$ at the bottom of the well. Every level is $\tfrac12\hbar\omega$ (minus a small anharmonic correction) higher than you think.
- Using $\omega_e$ as the band position. The fundamental is $\omega_e - 2\omega_e x_e$, about 105 cm⁻¹ lower for HCl.
- Predicting an overtone as twice the fundamental. With anharmonicity it is lower by $2\omega_e x_e$.
- Scaling $\omega_e x_e$ by $\mu^{-1/2}$ for an isotope. The anharmonicity constant scales as $\mu^{-1}$.
- Using the atomic mass instead of the reduced mass, or mixing u with kg. For HCl, $\mu$ is just under 1 u because H is so light.
- Treating the Morse $D_e$ from two spectroscopic constants as the true dissociation energy. It is a good estimate near the bottom of the well and often 10–20 % off at the top.

## Key takeaways

- Quantum oscillator: $E_v = (v + \tfrac12)\hbar\omega$, equally spaced, with a zero-point energy that never goes away.
- Wavefunctions have $v$ nodes, alternate parity, and leak beyond the classical turning points.
- Real bonds are anharmonic: $G(v) = \omega_e(v + \tfrac12) - \omega_e x_e(v + \tfrac12)^2$; gaps shrink with $v$, overtones appear weakly.
- Isotopic substitution keeps the potential and changes $\mu$: $\omega_e \propto \mu^{-1/2}$, $\omega_e x_e \propto \mu^{-1}$.
- The zero-point energy difference between X–H and X–D (about 5 kJ/mol for HCl) gives classical kinetic isotope effects of about 7 at room temperature.

## Sources

- [NIST Chemistry WebBook: HCl constants of diatomic molecules](https://webbook.nist.gov/cgi/cbook.cgi?ID=C7647010&Mask=1000) — H³⁵Cl $\omega_e = 2990.9463$, $\omega_e x_e = 52.8186$, $\omega_e y_e = 0.22437$ cm⁻¹, $r_e = 1.274552$ Å.
- [LibreTexts Physical Chemistry, chapter 5](https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Physical_Chemistry_(LibreTexts)/05%3A_The_Harmonic_Oscillator_and_the_Rigid_Rotor) — harmonic oscillator levels, Hermite wavefunctions, anharmonicity.
- [NIST Atomic Weights and Isotopic Compositions](https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl) — masses of ¹H, ²H, ³⁵Cl and ³⁷Cl.
- [MIT OCW 5.61 Physical Chemistry (Field, Fall 2017)](https://ocw.mit.edu/courses/5-61-physical-chemistry-fall-2017/) — lectures on the harmonic oscillator and anharmonic vibrations.
