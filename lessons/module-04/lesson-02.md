---
id: "04.2"
module: 4
minutes: 20
practice_minutes: 75
prerequisites: ["04.1", "02.1", "03.4"]
objectives:
  - Calculate the frequency and period of a mass on a spring and of a pendulum from their parameters.
  - Derive a bond force constant from an infrared wavenumber and predict the isotope shift for a heavier atom.
  - Use v = fλ and the wavenumber 1/λ to move between frequency, wavelength and wavenumber.
  - Measure g with a home pendulum by fitting T² against length and report it with an uncertainty.
volatility: concept
sources:
  - title: "OpenStax University Physics Volume 1, 15.1 Simple Harmonic Motion"
    url: https://openstax.org/books/university-physics-volume-1/pages/15-1-simple-harmonic-motion
  - title: "OpenStax University Physics Volume 1, 15.4 Pendulums"
    url: https://openstax.org/books/university-physics-volume-1/pages/15-4-pendulums
  - title: "OpenStax University Physics Volume 1, 15.5 Damped Oscillations"
    url: https://openstax.org/books/university-physics-volume-1/pages/15-5-damped-oscillations
  - title: "OpenStax University Physics Volume 1, 16.2 Mathematics of Waves"
    url: https://openstax.org/books/university-physics-volume-1/pages/16-2-mathematics-of-waves
  - title: "OpenStax University Physics Volume 1, 16.6 Standing Waves and Resonance"
    url: https://openstax.org/books/university-physics-volume-1/pages/16-6-standing-waves-and-resonance
  - title: "NIST Chemistry WebBook: Hydrogen chloride, constants of diatomic molecules"
    url: https://webbook.nist.gov/cgi/cbook.cgi?ID=C7647010&Mask=1000
  - title: "NIST Chemistry WebBook: Deuterium chloride, constants of diatomic molecules"
    url: https://webbook.nist.gov/cgi/cbook.cgi?ID=C7698057&Mask=1000
  - title: "NIST: standard acceleration of gravity"
    url: https://physics.nist.gov/cgi-bin/cuu/Value?gn
  - title: "phyphox wiki: built-in experiments"
    url: https://phyphox.org/wiki/index.php/Category:Built-in_experiments
  - title: "MIT OpenCourseWare 8.03SC Physics III: Vibrations and Waves"
    url: https://ocw.mit.edu/courses/8-03sc-physics-iii-vibrations-and-waves-fall-2016/
last_verified: "2026-10-16"
---

# 04.2 · Oscillations and waves

Anything pulled back towards a resting point by a force proportional to the displacement oscillates, and it does so at a frequency fixed by just two numbers: how stiff the restoring force is and how heavy the moving part is. That one rule describes a pendulum in your kitchen and the vibration of an HCl molecule, which is why infrared spectroscopy can tell you about bond strength. This lesson covers oscillators, damping and waves, then you measure the acceleration of gravity with keys on a string.

## Why it matters

An infrared spectrum of HCl gas shows strong absorption near 2886 cm⁻¹; deuterium chloride, DCl, absorbs near 2091 cm⁻¹. The bond, the electrons and the chemistry are the same. Only the mass of the moving atom changed. With the oscillator formula you can predict that shift before you measure it, and use it the other way round: chemists swap H for D on purpose to find out which IR band belongs to which bond (Module 17, Module 20). Waves matter just as much. Every spectrum you will read is labelled in wavelength, frequency or wavenumber, and you must convert between them without hesitation.

## Core ideas

> [!NOTE]
> The physics here is stable. The HCl and DCl constants come from the NIST Chemistry WebBook and standard gravity from NIST, checked 2026-10-16. The phyphox app is optional; its experiment list may change between versions.

### Simple harmonic motion

A mass $m$ on a spring of stiffness $k$ (in N/m) feels a restoring force $F = -kx$ (lesson [04.1](lesson-01.md), Part A). Newton's second law then gives

$$m\frac{d^2x}{dt^2} = -kx \quad\Rightarrow\quad x(t) = A\cos(\omega t + \phi),\qquad \omega = \sqrt{\frac{k}{m}}$$

This differential equation and its solution are the subject of lesson [03.4](../module-03/lesson-04.md). Here we use the result. $A$ is the amplitude, $\omega$ the angular frequency in rad/s, $\phi$ the starting phase. The ordinary frequency is $f = \omega/2\pi$ in hertz (Hz, cycles per second), and the period is $T = 1/f = 2\pi\sqrt{m/k}$.

Two facts matter. A stiffer spring vibrates faster; a heavier mass vibrates slower. And the period does not depend on the amplitude, as long as the force stays proportional to $x$.

Energy sloshes between kinetic and potential, with a constant total $E = \tfrac12 kA^2$.

### The pendulum

A small mass on a string of length $L$, swinging by a small angle, is a harmonic oscillator with $\omega = \sqrt{g/L}$:

$$T = 2\pi\sqrt{\frac{L}{g}}$$

The mass cancels. Square both sides: $T^2 = (4\pi^2/g)\,L$. A plot of $T^2$ against $L$ is a straight line through the origin with slope $4\pi^2/g$. That is the plot you will make. At a 10° swing the true period is only about 0.2 % longer than the formula; at 30° it is about 1.7 % longer, so keep the swings small.

### A molecule as two masses on a spring

A diatomic molecule vibrates as two masses joined by a spring, the bond. Both atoms move, and the motion behaves like a single mass equal to the reduced mass:

$$\mu = \frac{m_1 m_2}{m_1 + m_2},\qquad \omega = \sqrt{\frac{k}{\mu}}$$

For HCl, $\mu$ is almost the mass of H, because the heavy Cl barely moves. Spectroscopists report vibrations as a wavenumber $\tilde\nu = f/c$, in cm⁻¹ (see waves below). Turning that around gives the force constant:

$$k = \mu\,(2\pi c\tilde\nu)^2$$

### Damping and resonance

Real oscillators lose energy, to air drag in a pendulum or to neighbouring molecules in a liquid. The amplitude then decays as $e^{-t/\tau}$. The quality factor $Q$ is roughly the number of radians of swinging before the energy falls to $1/e$; a good pendulum has $Q$ in the hundreds. If you push an oscillator periodically, it responds most strongly when you push at its natural frequency. That is resonance, and absorbing light at a molecule's vibrational frequency is the same idea (lesson [04.5](lesson-05.md)).

### Waves: frequency, wavelength, wavenumber

A wave is an oscillation that travels. Its speed $v$, frequency $f$ and wavelength $\lambda$ obey

$$v = f\lambda$$

Sound in air at 20 °C travels at about 343 m/s, so a 440 Hz tone has $\lambda = 343/440 = 0.78$ m. Light in vacuum travels at $c = 299\,792\,458$ m/s, exactly. The wavenumber is the number of waves per unit length, $\tilde\nu = 1/\lambda$. Chemists use cm⁻¹: a wavelength of 3.34 µm is $1/(3.34\times10^{-4}\ \mathrm{cm}) = 2991\ \mathrm{cm^{-1}}$. Wavenumber is proportional to frequency and to energy, which is why IR spectra use it.

A wave held at both ends, like a guitar string of length $L$, can only fit whole numbers of half-wavelengths: $\lambda_n = 2L/n$. These standing waves have fixed allowed frequencies. In Module 12 the same picture explains why an electron in a box has fixed allowed energies.

## Worked example

### 1. HCl: force constant and period

NIST gives $\omega_e = 2990.95\ \mathrm{cm^{-1}}$ for H³⁵Cl. This is the harmonic wavenumber of the bond. (The observed band at 2886 cm⁻¹ is lower because the real well is not a perfect parabola, lesson 04.1.)

- Reduced mass: $\mu = \dfrac{1.00783 \times 34.96885}{1.00783 + 34.96885}$ u $= 0.97959$ u $= 0.97959 \times 1.66054\times10^{-27} = 1.6267\times10^{-27}$ kg.
- Angular frequency: $\omega = 2\pi c\tilde\nu = 2\pi \times 2.99792\times10^{10}\ \mathrm{cm/s} \times 2990.95\ \mathrm{cm^{-1}} = 5.634\times10^{14}$ rad/s.
- Force constant: $k = \mu\omega^2 = 1.6267\times10^{-27} \times (5.634\times10^{14})^2 = 516$ N/m.
- Frequency $f = 8.97\times10^{13}$ Hz, period $T = 11.2$ fs, wavelength of the matching light $\lambda = 1/\tilde\nu = 3.34$ µm, in the infrared.

Interpretation: a bond is about as stiff as a firm kitchen spring (hundreds of N/m), but the mass on it is $10^{27}$ times smaller, so it vibrates $10^{14}$ times a second.

### 2. Predicting the DCl shift

Replace H (1.00783 u) by D (2.01410 u). The bond force constant is the same, because the electrons are the same. New reduced mass: $\mu_D = \dfrac{2.01410 \times 34.96885}{2.01410 + 34.96885} = 1.90441$ u.

$$\tilde\nu_D = \tilde\nu_H\sqrt{\frac{\mu_H}{\mu_D}} = 2990.95 \times \sqrt{\frac{0.97959}{1.90441}} = 2145\ \mathrm{cm^{-1}}$$

NIST lists 2145.16 cm⁻¹ for D³⁵Cl. A two-line calculation predicts a measured constant to four figures. The ratio is close to $1/\sqrt2$ because the reduced mass almost doubles.

## Hands-on

First, explore the model. Set a mass and a spring, change one at a time and watch the period; then add damping and read off how fast the amplitude falls.

[Simulation: Oscillators — a single mass on a spring](../../simulations/oscillators/index.html?preset=single)

Task in the simulation: with $m$ = 0.20 kg, find the spring constant that gives a period of exactly 1.00 s. Target: $k = 4\pi^2 m / T^2 = 7.9$ N/m.

### Home experiment: measure g with a pendulum (about 60 min)

> [!CAUTION]
> Use something light as the bob: a bunch of keys or a large nut, not a phone, glass or anything heavy. Tie the string firmly to a hook, a door-frame screw or a broom handle laid across two chairs, so nothing can fall on feet. Keep the swing small (a hand's width), keep faces and children out of the swing path, and do not climb on furniture to hang it. No chemicals are involved.

What you need: about 1.2 m of thin string or dental floss, a light bob (keys), a tape measure, the phone stopwatch, your notebook, and the [Module 4 lab folder](../../labs/module-04/). Optional: the free phyphox app has a built-in Pendulum experiment, but it uses the phone itself as the bob, so only try it with the phone in a padded bag hanging a few centimetres above a bed.

Steps:

1. Hang the bob so the length from the knot to the centre of the keys is about 0.30 m. Measure $L$ to the nearest millimetre and write down your reading uncertainty.
2. Pull the bob aside by about 10 cm (about 10°) and let go without pushing.
3. Start the stopwatch when the bob passes the lowest point, and count 20 full swings (back to the same point, moving the same way). Stop on the 20th. Timing many swings divides your reaction-time error by 20.
4. Repeat three times at this length.
5. Repeat for $L$ ≈ 0.45, 0.60, 0.75 and 0.90 m.
6. Type the data into a CSV with the header `L_m,trial,t20_s`, in the same format as `pendulum_example.csv`.
7. Fill in the three TODO functions in `lesson02_pendulum.py`, check them on the example data, then run on yours:

```bash
py lesson02_pendulum.py
py lesson02_pendulum.py my_pendulum.csv
```

How you know it worked: on the example data you get $g = 9.78 \pm 0.08\ \mathrm{m/s^2}$, an intercept near zero, and the script also prints the HCl frequency (2991 cm⁻¹, period 11.2 fs) from the same formula. Your own result should land within 1–2 % of standard gravity, $g_n = 9.80665\ \mathrm{m/s^2}$ (local $g$ in Israel is close to 9.79–9.80). Repeat trials should agree to about 0.2 s on a 20-swing time.

<details><summary>Reference solution and what real data show</summary>

`periods`: `t_n / n`. `mean_by_length`: group by `np.unique(L)`, take the mean and `std(ddof=1)/sqrt(n)`. `fit_g`: `np.polyfit(Ls, T_mean**2, 1, cov=True)`, then $g = 4\pi^2/\text{slope}$ and $u_g = g\,u_\text{slope}/\text{slope}$. Full code: `lesson02_pendulum_solution.py`.

If your intercept is clearly non-zero, you measured every length with the same offset, usually to the top of the keys instead of their centre. The slope, and so $g$, is not affected by a constant offset: this is why the fit uses the slope and not a single length. If your $g$ comes out 1–3 % low, check the swing size: large swings lengthen the period. If it is wildly off, check that you counted full swings (there and back), not half swings; half swings make $g$ four times too large.

Write it up with the [lab report template](../../templates/lab-report.md): aim, method, data table, plot, $g$ with uncertainty, and the comparison with standard gravity.

</details>

## Common mistakes

- Confusing $\omega$ and $f$. Angular frequency $\omega$ (rad/s) is $2\pi$ times the frequency $f$ (Hz). A missing $2\pi$ makes a force constant 40 times wrong.
- Using the mass of one atom instead of the reduced mass. For HCl the error is 2 %; for a molecule of two equal atoms such as O₂ it is a factor of 2.
- Mixing cm and m in $k = \mu(2\pi c\tilde\nu)^2$. With $\tilde\nu$ in cm⁻¹, use $c$ in cm/s ($2.998\times10^{10}$).
- Counting half swings as periods. A period is a full there-and-back cycle.
- Measuring the pendulum length to the top of the bob. Use the centre of mass of the bob; the fit's intercept tells you if you got this wrong.
- Expecting the observed IR band to equal $\omega_e$. The band is lower because real bonds are anharmonic.

## Key takeaways

- A restoring force proportional to displacement gives oscillation at $\omega = \sqrt{k/m}$, independent of amplitude.
- A pendulum has $T = 2\pi\sqrt{L/g}$; plotting $T^2$ against $L$ gives $g$ from the slope.
- A diatomic bond is a spring with the reduced mass on it; its IR wavenumber gives the force constant.
- Isotope substitution changes the mass, not the force constant, so the frequency scales as $1/\sqrt{\mu}$.
- Waves obey $v = f\lambda$; chemists use the wavenumber $1/\lambda$ in cm⁻¹ because it is proportional to energy.

## Sources

- [OpenStax University Physics Volume 1, 15.1 Simple Harmonic Motion](https://openstax.org/books/university-physics-volume-1/pages/15-1-simple-harmonic-motion) — the spring oscillator and its energy.
- [OpenStax University Physics Volume 1, 15.4 Pendulums](https://openstax.org/books/university-physics-volume-1/pages/15-4-pendulums) — period of a simple pendulum.
- [OpenStax University Physics Volume 1, 15.5 Damped Oscillations](https://openstax.org/books/university-physics-volume-1/pages/15-5-damped-oscillations) — damping and decay.
- [OpenStax University Physics Volume 1, 16.2 Mathematics of Waves](https://openstax.org/books/university-physics-volume-1/pages/16-2-mathematics-of-waves) — $v = f\lambda$ and wave functions.
- [OpenStax University Physics Volume 1, 16.6 Standing Waves and Resonance](https://openstax.org/books/university-physics-volume-1/pages/16-6-standing-waves-and-resonance) — allowed wavelengths on a string.
- [NIST Chemistry WebBook: HCl](https://webbook.nist.gov/cgi/cbook.cgi?ID=C7647010&Mask=1000) and [DCl](https://webbook.nist.gov/cgi/cbook.cgi?ID=C7698057&Mask=1000) — harmonic wavenumbers 2990.95 and 2145.16 cm⁻¹.
- [NIST: standard acceleration of gravity](https://physics.nist.gov/cgi-bin/cuu/Value?gn) — $g_n = 9.80665\ \mathrm{m/s^2}$, exact by definition.
- [phyphox wiki: built-in experiments](https://phyphox.org/wiki/index.php/Category:Built-in_experiments) — the optional phone Pendulum experiment.
- [MIT OCW 8.03SC Vibrations and Waves](https://ocw.mit.edu/courses/8-03sc-physics-iii-vibrations-and-waves-fall-2016/) — the full course for depth.
