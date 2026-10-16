---
id: "03.4"
module: 3
minutes: 20
practice_minutes: 60
prerequisites: ["03.2", "03.3", "02.4"]
objectives:
  - Solve m x'' + b x' + k x = 0 with the characteristic equation and classify the motion as under-, critically or overdamped.
  - Calculate the force constant of a diatomic bond from its vibrational wavenumber and reduced mass.
  - Rewrite a second-order equation as two first-order equations and solve it with solve_ivp.
  - Measure the damping rate and quality factor of a home pendulum from amplitude readings.
volatility: concept
sources:
  - title: "OpenStax University Physics Volume 1, 15.5 Damped Oscillations"
    url: https://openstax.org/books/university-physics-volume-1/pages/15-5-damped-oscillations
  - title: "NIST Chemistry WebBook: Hydrogen chloride, constants of diatomic molecules"
    url: https://webbook.nist.gov/cgi/cbook.cgi?ID=C7647010&Mask=1000
  - title: "NIST Atomic Weights and Isotopic Compositions: chlorine"
    url: https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl?ele=Cl&ascii=html&isotype=some
  - title: "MIT OpenCourseWare 18.03 Differential Equations (Miller and Mattuck, Spring 2010)"
    url: https://ocw.mit.edu/courses/18-03-differential-equations-spring-2010/
last_verified: "2026-10-16"
---

# 03.4 · Second-order equations and oscillators

Anything that is pulled back towards a resting position and has inertia will oscillate: a pendulum, a mass on a spring, the two atoms of a chemical bond. Newton's second law turns each of these into a second-order differential equation, one with a second derivative in it. This lesson solves that equation with one trick, a trial exponential, sorts the solutions into the three kinds of damping, applies it to the HCl bond, and ends with a pendulum you build from a string and a bunch of keys.

## Why it matters

The infrared spectrum of HCl shows a strong band near 2886 cm⁻¹. From that one number and the masses of H and Cl you can work out how stiff the bond is: about 500 N/m. The same equation decides how fast a balance pan settles, why an analogue meter needle overshoots, and how a molecule's vibration gives its energy away to the solvent. Spectroscopy (Modules 14, 20 and 30) uses the oscillator equation constantly; this lesson is where it comes from.

## Core ideas

> [!NOTE]
> The mathematics is stable. The HCl harmonic wavenumber $\omega_e = 2990.9463$ cm⁻¹ is from the NIST Chemistry WebBook (diatomic constants, checked 2026-10-16); atomic masses are NIST values and the atomic mass constant is CODATA 2022. The lab uses `solve_ivp` from SciPy 1.18.

### Newton's law for a spring

A mass $m$ on a spring with force constant $k$ (N/m) feels a force $-kx$ when displaced by $x$ (Hooke's law). Friction or drag adds a force $-b\,\dot x$ proportional to the velocity, with damping coefficient $b$ (kg/s). Newton's second law, force = mass × acceleration, gives

$$m\ddot{x} + b\dot{x} + kx = 0$$

The dots mean time derivatives: $\dot{x} = dx/dt$ is the velocity and $\ddot{x} = d^2x/dt^2$ the acceleration. The equation is linear (no $x^2$ or $x\dot x$ terms), with constant coefficients and second order.

### The trial exponential and the characteristic equation

Try $x = e^{rt}$. Then $\dot{x} = re^{rt}$ and $\ddot{x} = r^2e^{rt}$. Substituting and dividing by $e^{rt}$ (never zero) leaves an ordinary quadratic, the characteristic equation:

$$m r^2 + b r + k = 0 \quad\Rightarrow\quad r = -\gamma \pm \sqrt{\gamma^2 - \omega_0^2}, \qquad \gamma = \frac{b}{2m},\ \ \omega_0 = \sqrt{\frac{k}{m}}$$

Here $\omega_0$ is the natural angular frequency (rad/s) and $\gamma$ the damping rate (1/s). The sign under the root decides everything:

| Case | Condition | Motion |
|---|---|---|
| Underdamped | $\gamma < \omega_0$ ($b^2 < 4mk$) | oscillates inside a decaying envelope $e^{-\gamma t}$, at $\omega_d = \sqrt{\omega_0^2 - \gamma^2}$ |
| Critically damped | $\gamma = \omega_0$ | returns to rest fastest without overshooting |
| Overdamped | $\gamma > \omega_0$ | creeps back slowly, no oscillation |

In the underdamped case the roots are complex, $r = -\gamma \pm i\omega_d$, and Euler's formula $e^{i\theta} = \cos\theta + i\sin\theta$ turns them into a real solution:

$$x(t) = A\,e^{-\gamma t}\cos(\omega_d t + \phi)$$

$A$ and $\phi$ come from the starting position and velocity. Without damping ($b = 0$) this is simple harmonic motion with period $T = 2\pi/\omega_0$, independent of amplitude.

Watch the three cases change into each other as you raise the damping:

[Simulation: Oscillators — damped mass on a spring](../../simulations/oscillators/index.html?preset=damped)

### Quality factor

How many oscillations before the motion dies out? The quality factor $Q = \omega_0/(2\gamma)$ measures it. The amplitude falls by a factor $e$ in about $Q/\pi$ cycles. A pendulum in air has $Q$ of a few hundred; a tuning fork thousands; a car suspension only about 1 to 2 (damped on purpose so it barely bounces). The amplitude envelope $e^{-\gamma t}$ is first-order decay, so the log plot of [02.1](../module-02/lesson-01.md) gives $\gamma$ from amplitude readings.

### A diatomic molecule is an oscillator

Near the bottom of the bond's potential well, the harmonic approximation of [02.4](../module-02/lesson-04.md) makes the bond a spring. Two atoms moving against each other behave like a single mass, the reduced mass

$$\mu = \frac{m_1 m_2}{m_1 + m_2}$$

so $\omega = \sqrt{k/\mu}$. This is the two-atom case of the normal modes in [03.2](lesson-02.md): one eigenvalue is zero (the molecule sliding) and the other is $k/\mu$. Spectroscopists give $\omega_e$ as a wavenumber, $\tilde\nu = \omega/(2\pi c)$, so $k = \mu(2\pi c\,\omega_e)^2$. The observed fundamental (2886 cm⁻¹ for HCl) is a little lower than $\omega_e$ because real bonds are anharmonic; Module 20 handles that correction.

The undamped case is the starting point for all of this:

[Simulation: Oscillators — simple harmonic oscillator](../../simulations/oscillators/index.html?preset=single)

### Any second-order equation is two first-order ones

Numerical solvers such as `solve_ivp` only take first-order equations. Introduce the velocity $v = \dot x$ as a second unknown:

$$\frac{d}{dt}\begin{pmatrix} x \\ v \end{pmatrix} = \begin{pmatrix} 0 & 1 \\ -k/m & -b/m \end{pmatrix}\begin{pmatrix} x \\ v \end{pmatrix}$$

The eigenvalues of this matrix are exactly the roots $r$ of the characteristic equation. Linear algebra (03.2) and differential equations meet here, and lesson [03.5](lesson-05.md) uses the same idea for coupled reactions.

## Worked example

### 1. The force constant of HCl

$\omega_e = 2990.95$ cm⁻¹ for H³⁵Cl. Masses: $^1$H 1.007825 u, $^{35}$Cl 34.968853 u.

1. $\mu = \dfrac{1.007825 \times 34.968853}{35.976678} = 0.97959$ u $= 0.97959 \times 1.66054\times10^{-27} = 1.6267\times10^{-27}$ kg. Almost the mass of the H atom: the light atom does nearly all the moving.
2. $\omega = 2\pi \times 2.99792\times10^{10}\ \mathrm{cm/s} \times 2990.95\ \mathrm{cm^{-1}} = 5.634\times10^{14}$ rad/s.
3. $k = \mu\omega^2 = 1.6267\times10^{-27} \times 3.174\times10^{29} = 516$ N/m.

One vibration takes $1/(c\,\omega_e) = 11.2$ fs. For D³⁵Cl the force constant is the same (same electrons), but $\mu$ nearly doubles, so $\omega_e$ drops by a factor of about 1.39, to near 2145 cm⁻¹. That isotope shift is how spectroscopists confirm which atom moves in a band.

### 2. Classify a damped spring

$m = 0.200$ kg, $k = 20.0$ N/m, $b = 0.40$ kg/s.

1. $\omega_0 = \sqrt{20.0/0.200} = 10.0$ rad/s; $\gamma = 0.40/(2 \times 0.200) = 1.0$ s⁻¹.
2. $\gamma < \omega_0$: underdamped. $\omega_d = \sqrt{100 - 1} = 9.95$ rad/s, period 0.632 s (0.628 s undamped).
3. $Q = 10.0/2.0 = 5$. The amplitude halves every $\ln 2/\gamma = 0.69$ s, about one period.
4. Critical damping needs $b = 2\sqrt{mk} = 2\sqrt{4.0} = 4.0$ kg/s, ten times more.

## Hands-on

### Part A — home pendulum (30 min)

> [!CAUTION]
> Tie the string to something solid that cannot fall: a door handle, a hook, or a broom handle across two chairs. Keep the swing clear of faces, glass and screens, and keep small children and pets away from the swinging weight. Use a light weight such as a bunch of keys; no glass, nothing sharp.

What you need: about 60 cm of string or thread, a bunch of keys (or a small bag of rice), a ruler or tape measure, sticky tape, a phone stopwatch, and a sheet of paper marked with lines every centimetre placed just behind the swing.

1. Hang the keys so the length from the knot to the middle of the keys is 50 cm.
2. Pull the keys 20 cm to one side along the paper scale and let go without pushing.
3. Count 10 full swings (out and back) and time them. Divide by 10 for the period.
4. Release again from 20 cm. Every 5 full swings, read how far the keys go on the scale (peak amplitude), until about 60 swings. Ask a helper to count while you read, or film it with the phone and read off afterwards.
5. Type your readings into a CSV with the header `swings,t_s,amplitude_cm` (time = swings × period), like `pendulum_example.csv`.

This trains reading a decaying signal and extracting a rate from it. It does not train precision timing; that comes with phyphox in Module 4.

### Part B — Python (30 min)

1. Open `lesson04_oscillator.py` in the [Module 3 lab folder](../../labs/module-03/) and fill in `classify`, `rhs`, `force_constant` and `fit_decay`.
2. Run on the example data, then on yours:

```bash
py lesson04_oscillator.py
py lesson04_oscillator.py my_pendulum.csv
```

How you know it worked: for $m = 1$, $k = 4$ the script reports $b = 0.4$ underdamped, $b = 4$ critically damped (double root −2), $b = 10$ overdamped (roots −9.58 and −0.42). `solve_ivp` matches the formula to better than $10^{-9}$. HCl gives $\mu = 0.97959$ u and $k = 516$ N/m. The example pendulum gives a period of 1.420 s (a 0.50 m pendulum), $\gamma \approx 0.011$ s⁻¹, amplitude half-life about 60 s and $Q \approx 200$. With your keys expect a period near 1.42 s and a $Q$ between about 50 and 500, depending on how much the keys flap.

<details><summary>Reference solution and what real data show</summary>

`classify`: `np.roots([m, b, k])` and the sign of $b^2 - 4mk$. `rhs`: `[v, -(b*v + k*x)/m]`. `force_constant`: reduced mass in kg times $(2\pi c\,\omega_e)^2$. `fit_decay`: `np.polyfit(t, np.log(amp), 1)`, $\gamma = -$slope. Full code: `lesson04_oscillator_solution.py`.

Real pendulums often decay faster at large amplitude, because air drag grows with speed squared, not linearly. On the log plot you see the first points falling more steeply. Fit only readings below 10 cm and compare $\gamma$: if the two differ, the linear-damping model $b\dot x$ is only an approximation for your pendulum. Flat keys catch more air than a compact bag of rice and give a lower $Q$.

</details>

## Common mistakes

- Using the atom's mass instead of the reduced mass. For HCl the difference is 3 %; for CO (two similar masses) it is a factor of two.
- Mixing $\omega$ (rad/s) and frequency $f$ (Hz). $\omega = 2\pi f$; the period is $2\pi/\omega$.
- Calling a slowly returning system "critically damped". Critical damping is the fastest return without overshoot; slower than that is overdamped.
- Giving `solve_ivp` a second-order equation directly. It needs the state vector $[x, v]$ and two first-order equations.
- Expecting the damped period to differ much from the undamped one. For $Q$ above about 5 the difference is under 1 %; the damping shows in the amplitude, not the period.

## Key takeaways

- $m\ddot x + b\dot x + kx = 0$ is solved by $e^{rt}$ with $mr^2 + br + k = 0$.
- The discriminant decides the motion: underdamped (oscillating, decaying), critically damped, or overdamped.
- $\omega_0 = \sqrt{k/m}$, $\gamma = b/2m$ and $Q = \omega_0/2\gamma$; the amplitude envelope is $e^{-\gamma t}$.
- A diatomic bond is a spring with the reduced mass: $k = \mu(2\pi c\,\omega_e)^2$, 516 N/m for HCl.
- Any second-order ODE becomes two first-order ones; the matrix's eigenvalues are the characteristic roots.

## Sources

- [OpenStax University Physics Volume 1, 15.5 Damped Oscillations](https://openstax.org/books/university-physics-volume-1/pages/15-5-damped-oscillations) — damped frequency and the three damping cases.
- [NIST Chemistry WebBook: HCl diatomic constants](https://webbook.nist.gov/cgi/cbook.cgi?ID=C7647010&Mask=1000) — $\omega_e = 2990.9463$ cm⁻¹ for H³⁵Cl.
- [NIST Atomic Weights and Isotopic Compositions: chlorine](https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl?ele=Cl&ascii=html&isotype=some) — mass of ³⁵Cl, 34.968852682 u.
- [MIT OCW 18.03 Differential Equations](https://ocw.mit.edu/courses/18-03-differential-equations-spring-2010/) — characteristic equations, damping and first-order systems.
