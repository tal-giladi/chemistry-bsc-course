---
id: "14.2"
module: 14
minutes: 20
practice_minutes: 90
prerequisites: ["14.1", "03.4", "12.4"]
objectives:
  - Extract the damping rate of a real oscillator from a phyphox recording, by the decay of the peaks and by a full damped-cosine fit.
  - Calculate the quality factor Q from the damping rate, the logarithmic decrement and the number of cycles to decay.
  - Detect anharmonicity as a drift of frequency with amplitude and estimate its size.
  - Explain how an amplitude-dependent frequency in a spring relates to the converging vibrational levels of a real bond.
volatility: concept
sources:
  - title: "OpenStax University Physics Volume 1, 15.5 Damped Oscillations"
    url: https://openstax.org/books/university-physics-volume-1/pages/15-5-damped-oscillations
  - title: "OpenStax University Physics Volume 1, 15.4 Pendulums"
    url: https://openstax.org/books/university-physics-volume-1/pages/15-4-pendulums
  - title: "phyphox wiki: Experiment Spring"
    url: https://phyphox.org/wiki/index.php/Experiment:_Spring
  - title: "SciPy v1.18 manual, scipy.optimize.curve_fit"
    url: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html
  - title: "MIT OpenCourseWare 8.03SC Physics III: Vibrations and Waves"
    url: https://ocw.mit.edu/courses/8-03sc-physics-iii-vibrations-and-waves-fall-2016/
last_verified: "2026-10-17"
---

# 14.2 · Damping, anharmonicity and the Q factor

A real oscillator is never ideal in two ways. It loses energy, so its swing dies away; and its restoring force is never exactly proportional to the stretch, so its frequency depends a little on how hard it swings. The first is damping, measured by the quality factor Q. The second is anharmonicity. Both show up in molecules: damping as the width of a spectral line, anharmonicity as the shrinking gaps between vibrational levels that you met in lesson 12.4. In this lesson you record a spring ringing down with phyphox, measure Q two ways, make it worse on purpose with a cardboard disc, and catch an elastic band changing its frequency as it calms down.

## Why it matters

A spectroscopist looks at an infrared band and reads two things from it: its position and its width. The position comes from the stiffness and the masses. The width comes from how fast the vibration loses its energy or its phase, and $Q = \omega_0/\Delta\omega$ links the two. A narrow band means a long-lived vibration; a broad one means fast energy loss to the surroundings, as in a liquid full of hydrogen bonds. Anharmonicity decides whether the first overtone appears at exactly twice the fundamental (it never does) and how much energy it takes to break the bond. Both ideas are easier to see, and to trust, when you watch them on a spring you can touch.

## Core ideas

> [!NOTE]
> The physics is stable. The analysis uses SciPy 1.18 (`curve_fit`, `find_peaks`) and phyphox 1.2.1, checked 2026-10-17. Example recordings in the lab folder are generated from known parameters, so you can check your analysis before you trust it on your own data.

### The damped oscillator, measured

Lesson [03.4](../module-03/lesson-04.md) solved $m\ddot x + b\dot x + kx = 0$. For light damping the solution is

$$x(t) = A\,e^{-\gamma t}\cos(\omega_d t + \phi),\qquad \gamma = \frac{b}{2m},\qquad \omega_d = \sqrt{\omega_0^2 - \gamma^2}$$

The damping rate $\gamma$ (in s⁻¹) sets how fast the envelope $e^{-\gamma t}$ shrinks. The phone measures acceleration, not position, but for light damping $a \approx -\omega_0^2 x$, so the acceleration decays with the same envelope.

There are two ways to get $\gamma$ from a recording.

1. Peak method. Find the peak of each cycle. Plot $\ln(\text{peak height})$ against time: a straight line of slope $-\gamma$. This is first-order decay, the log plot of [02.1](../module-02/lesson-01.md).
2. Full fit. Fit $a(t) = A e^{-\gamma t}\cos(\omega_d t + \phi) + c$ to every data point with `curve_fit`. It uses all the data, not just the peaks, so it is more precise, but it needs good starting guesses: take $\omega_d$ from the strongest frequency and $\gamma$ from the peak method.

Use only peaks well above the sensor noise. Small peaks are pushed up by noise (the highest of several noisy samples is biased high), which makes the decay look slower than it is.

### The quality factor, three ways

The quality factor $Q$ counts how long an oscillator rings. All three of these definitions agree for light damping:

$$Q = \frac{\omega_0}{2\gamma} \qquad Q \approx \frac{\pi}{\delta},\ \ \delta = \ln\frac{A_n}{A_{n+1}} = \gamma T_d \qquad Q \approx \pi \times (\text{cycles for the amplitude to fall by } e)$$

The logarithmic decrement $\delta$ is the drop in $\ln(\text{amplitude})$ from one cycle to the next. A fourth form, $Q = f_0/\Delta f$ with $\Delta f$ the width of the resonance peak, is the one you will use in lessons 14.5 and 14.6. Typical values: a car suspension 1–2, a phone on a steel spring about 100, a tuning fork thousands, a quartz watch crystal tens of thousands.

Where does the energy go? Air drag and internal friction in the spring. At low speed air drag is proportional to velocity, which gives the exponential decay above. A large flat card under the bag adds drag and lowers $Q$. At high speed drag grows with the square of velocity and the decay is no longer exponential: the semi-log plot of the peaks then curves. A straight semi-log plot is your check that the linear damping model fits.

### Anharmonicity: frequency that depends on amplitude

In a harmonic oscillator the period does not depend on the amplitude. That is the one property a real oscillator always breaks a little. Write the restoring force as $F = -kx(1 + \beta x^2)$. For small $\beta$ the frequency becomes

$$\omega \approx \omega_0\left(1 + \tfrac{3}{8}\beta A^2\right)$$

with $A$ the displacement amplitude. If $\beta > 0$ the spring stiffens when stretched far and the frequency rises with amplitude. If $\beta < 0$ it softens and the frequency falls. A pendulum is a softening oscillator: at 30° its period is about 1.7 % longer than at small swings (lesson [04.2](../module-04/lesson-02.md)). A steel spring is very nearly harmonic. A loop of elastic hair bands is not.

You see anharmonicity in a ringdown by fitting the frequency in short windows. As the amplitude decays, a softening oscillator speeds up and a stiffening one slows down.

### The molecular connection

A chemical bond is a softening oscillator. The Morse potential of lesson [12.4](../module-12/lesson-04.md) is flatter than a parabola on the stretched side, so a classical bond vibrating with more energy has a lower frequency. In quantum terms the levels crowd together, $G(v+1) - G(v) = \omega_e - 2\omega_e x_e(v+1)$, and the first overtone of HCl sits at 5668 cm⁻¹, not at twice 2886. Your elastic band shows the same thing in slow motion: frequency depends on energy.

[Simulation: Oscillators — damped mass on a spring](../../simulations/oscillators/index.html?preset=damped)

## Worked example

### 1. Q from the peaks

A phone on a steel spring rings at $f_d = 1.40$ Hz. Its acceleration peaks fall from 2.00 to 1.00 m/s² in 24 cycles.

- Decrement per cycle: $\delta = \ln 2 / 24 = 0.0289$.
- Damping rate: $\gamma = \delta / T_d = \delta f_d = 0.0289 \times 1.40 = 0.0404\ \mathrm{s^{-1}}$.
- Quality factor: $Q = \pi/\delta = 109$. Check: $Q = \omega_0/2\gamma = 2\pi \times 1.40 / (2 \times 0.0404) = 109$.

The amplitude falls by $e$ in $1/\delta = 35$ cycles, about 25 s. The energy, which goes as amplitude squared, falls by $e$ twice as fast, in 12 s.

### 2. How anharmonic is an elastic band?

A phone hangs on a loop of elastic hair bands. Windowed fits of the ringdown give 1.968 Hz while the acceleration amplitude is 4.76 m/s², and 2.000 Hz near the end, at 0.56 m/s². The frequency rose by 1.6 % as the swing died: the band softens at large stretch, $\beta < 0$.

Convert acceleration to displacement with $x = a/\omega^2$: at the start $x = 4.76/(2\pi \times 1.968)^2 = 3.1$ cm; at the end 0.36 cm. Then

$$\frac{\Delta\omega}{\omega_0} \approx \tfrac38 \beta\,(A_1^2 - A_2^2) \;\Rightarrow\; \beta = \frac{-0.016 \times 8/3}{0.031^2 - 0.0036^2} = -46\ \mathrm{m^{-2}}$$

So at 3 cm the band is about 4 % softer than at small stretch ($\beta A^2 = -0.044$). Interpretation: the band behaves like a Morse bond, not like a parabola, and you can measure by how much.

## Hands-on

> [!CAUTION]
> Same set-up and rules as lesson 14.1: a hook that cannot slip, the phone sealed in a zip bag and tied on, cushions underneath, pulls of only 2–3 cm. Elastic hair bands can snap under load: check them for cracks, do not stretch them to more than about twice their length, and wear ordinary safety glasses from your Module 1 kit while the phone hangs on them. Nothing here uses mains power.

What you need: the spring and phone set-up from 14.1, a stiff paper plate or a 20 cm cardboard disc, tape, four or five elastic hair bands, phyphox, and the [Module 14 lab folder](../../labs/module-14/). Time: about 90 minutes.

### Part A — three ringdowns (45 min)

1. Hang the phone on the steel spring. In phyphox open Acceleration (without g) from the raw sensor group, or the Spring experiment; both record the time series.
2. Pull down 3 cm, release gently, start recording, and let it ring for 60 s. Stop, and export the data as CSV (menu, export, comma-separated values). Name it `my_spring.csv`.
3. Tape the cardboard disc flat under the bag, horizontal, so it pushes air as it moves. Repeat for 20 s. Name it `my_card.csv`.
4. Replace the spring with a chain or loop of hair bands that stretches about 10 cm under the phone. Pull down 4–5 cm, release, record 30 s, export as `my_band.csv`.
5. Note which column holds the axis along the spring. With the phone hanging upright it is usually the third sensor column (z for a phone hanging flat, y for one hanging on its short edge); the column with the big sine wave is the right one.

### Part B — Python (45 min)

Fill in `damped` and `q_factor` in `lesson02_damping.py`, run it on the three example recordings, then on yours (the number is the column index; time is column 0):

```bash
py lesson02_damping.py
py lesson02_damping.py my_spring.csv 3
py lesson02_damping.py my_band.csv 3
```

How you know it worked: on the example data the bare spring gives $f_d$ = 1.401 Hz, $\gamma$ = 0.0400 s⁻¹ and $Q$ = 110; the card gives $\gamma$ = 0.301 s⁻¹ and $Q$ = 14.6; the elastic band gives $Q$ = 51 and a frequency that rises 1.65 % as the amplitude decays. For the steel spring the frequency drift is below the noise. On your own phone expect $Q$ between about 30 and 200 for the spring, several times lower with the card, and a visible drift for the band.

<details><summary>Reference solution and what the numbers tell you</summary>

`damped`: `A * np.exp(-gamma * t) * np.cos(omega_d * t + phi) + c`. `q_factor`: $\omega_0 = \sqrt{\omega_d^2 + \gamma^2}$, return $\omega_0/(2\gamma)$ and $\omega_0$. Full code: `lesson02_damping_solution.py`.

The peak method gives a slightly smaller $\gamma$ than the full fit (0.039 against 0.040 for the spring). The full fit uses all 6000 points and is the better number; the peak method is your check that the fit did not lock onto a wrong frequency. For the band the two disagree more (0.113 against 0.123): with a non-linear force, the acceleration peaks shrink more slowly than the displacement, so the simple peak method is biased.

If $Q$ for your spring is far lower than 30, the phone is probably swinging sideways and trading energy between the two motions; the plot then shows a beating envelope instead of a smooth decay. Restart with a gentler release. If the semi-log plot of the peaks curves downward at the start, you pulled too far and quadratic air drag took over; start from a smaller amplitude. The disc should lower $Q$ by a factor of five or more; if not, it is too small or tilted.

Write it up with the [lab report template](../../templates/lab-report.md): one ringdown plot, the semi-log peak plot, a table of $f_d$, $\gamma$, $Q$ for the three set-ups, and one paragraph on what the band's frequency drift means.

</details>

## Common mistakes

- Using $\gamma$ where the formula needs $2\gamma$. $Q = \omega_0/(2\gamma)$; the energy decays at $2\gamma$, the amplitude at $\gamma$.
- Mixing $\omega$ and $f$ in Q. $Q = \omega_0/(2\gamma)$ needs $\omega_0$ in rad/s; with $f$ in Hz, write $Q = \pi f_0/\gamma$.
- Fitting peaks that are lost in the noise. They flatten the decay and make $Q$ too high; keep peaks well above the noise floor.
- Starting `curve_fit` from a poor guess. A damped cosine has many local minima; start from the measured frequency and the peak-method $\gamma$, and try a few phases.
- Calling any frequency change anharmonicity. Check first that the phone is not twisting or swinging sideways; those add other frequencies.
- Assuming the overtone of a real bond is twice the fundamental. Anharmonicity always pulls it lower.

## Key takeaways

- A ringdown's envelope $e^{-\gamma t}$ gives the damping rate, from the peaks or from a full fit; the fit is more precise.
- $Q = \omega_0/(2\gamma) \approx \pi/\delta$, and it equals π times the number of cycles for the amplitude to fall by $e$.
- Extra drag (a card) lowers $Q$; a straight semi-log peak plot confirms that damping is linear in velocity.
- Anharmonicity makes the frequency depend on amplitude: $\omega \approx \omega_0(1 + \tfrac38\beta A^2)$.
- Softening oscillators (pendulums, elastic bands, chemical bonds) slow down at large amplitude; that is why vibrational levels crowd together.

## Sources

- [OpenStax University Physics Volume 1, 15.5 Damped Oscillations](https://openstax.org/books/university-physics-volume-1/pages/15-5-damped-oscillations) — damped motion and its envelope.
- [OpenStax University Physics Volume 1, 15.4 Pendulums](https://openstax.org/books/university-physics-volume-1/pages/15-4-pendulums) — the small-angle limit and its breakdown.
- [phyphox wiki: Experiment Spring](https://phyphox.org/wiki/index.php/Experiment:_Spring) — recording a bouncing phone.
- [SciPy v1.18 manual, scipy.optimize.curve_fit](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html) — the non-linear fit used in the lab.
- [MIT OCW 8.03SC Vibrations and Waves](https://ocw.mit.edu/courses/8-03sc-physics-iii-vibrations-and-waves-fall-2016/) — damped and driven oscillators in depth.
