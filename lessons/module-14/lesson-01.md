---
id: "14.1"
module: 14
minutes: 20
practice_minutes: 90
prerequisites: ["04.2", "03.4", "05.3"]
objectives:
  - Measure the force constant of a real spring statically (stretch under known masses) and dynamically (period with phyphox), each with an uncertainty.
  - Fit T² against hanging mass and extract both the force constant and the effective mass of the spring.
  - Judge whether two measurements of the same quantity agree, using their combined standard uncertainty.
  - Record and export an accelerometer time series from phyphox for later analysis.
volatility: implementation
sources:
  - title: "phyphox wiki: Experiment Spring"
    url: https://phyphox.org/wiki/index.php/Experiment:_Spring
  - title: "phyphox version history: 1.2.1"
    url: https://phyphox.org/docs/reference/version-history/1.2.1/
  - title: "phyphox documentation: remote interface"
    url: https://phyphox.org/docs/remote-interface/
  - title: "OpenStax University Physics Volume 1, 15.1 Simple Harmonic Motion"
    url: https://openstax.org/books/university-physics-volume-1/pages/15-1-simple-harmonic-motion
  - title: "MIT OpenCourseWare 8.03SC Physics III: Vibrations and Waves"
    url: https://ocw.mit.edu/courses/8-03sc-physics-iii-vibrations-and-waves-fall-2016/
last_verified: "2026-10-17"
---

# 14.1 · Measuring a spring with your phone

Your phone has an accelerometer good enough for a first-year physics lab, and a free app called phyphox turns it into a recording instrument. In this lesson you hang the phone on a spring, let it bounce, and measure the spring's force constant two independent ways: by stretching it with known masses and by timing its oscillation. The two numbers should agree. When they do not, the disagreement teaches you something, here that the spring's own mass takes part in the motion. This is the first real experiment of the chemical physics lab, and every later lesson in the module builds on the same oscillator.

## Why it matters

A chemist never weighs a bond or stretches it with a ruler. Everything we know about bond stiffness comes from the second method: measure a vibration frequency and compute $k = \mu\omega^2$ (lesson [04.2](../module-04/lesson-02.md)). That only works if the oscillator model is right. On a kitchen-sized spring you can test the model directly, because you can also do the first method. If the static and dynamic values of $k$ agree within their uncertainties, you have earned the right to trust the formula when you can no longer check it, as with the 516 N/m of the H–Cl bond. If they disagree, you learn which assumption broke. The Technion chemical physics lab (01240611) opens with exactly this kind of comparison; at home you do it for real, with your hands, not in a simulation.

## Core ideas

> [!NOTE]
> The physics is stable. The app details are not: they were checked against phyphox 1.2.1 (released September 2026) and the phyphox wiki on 2026-10-17. Menu names, available experiments and export options can change between versions; if a menu item has moved, look for it in the three-dot menu of the experiment.

### Two ways to measure k

A spring obeys Hooke's law, $F = -kx$, as long as you do not overstretch it. The force constant $k$ (in N/m) is the force needed per metre of stretch.

Static method. Hang a mass $m$ and the spring lengthens by $\Delta L = mg/k$. Plot the spring length against the hanging mass. The points lie on a straight line whose slope is $g/k$, so $k = g/\text{slope}$. The intercept is the unloaded length, which you do not need.

Dynamic method. Pull the mass down a little and let go. It oscillates with period

$$T = 2\pi\sqrt{\frac{m}{k}}$$

This is the oscillator of lessons [03.4](../module-03/lesson-04.md) and [04.2](../module-04/lesson-02.md). Square it and you get a straight line in $m$: $T^2 = (4\pi^2/k)\,m$. Slope $4\pi^2/k$.

The static method uses gravity and a ruler. The dynamic method uses a clock and does not need $g$ at all. They are independent, which is what makes the comparison a real test.

### The spring's own mass

The spring moves too. Its bottom coil moves as much as the phone; its top coil does not move at all. For a uniform spring, the moving spring behaves as if one third of its mass $m_s$ were added to the hanging mass:

$$T^2 = \frac{4\pi^2}{k}\left(m + m_\text{eff}\right),\qquad m_\text{eff} \approx \frac{m_s}{3}$$

So the $T^2$ against $m$ line does not pass through the origin. Its intercept divided by its slope is $m_\text{eff}$. With a 30 g spring and a 200 g phone the correction is 5 %, larger than the precision of the measurement, so you must include it. The same idea, motion shared between parts that move by different amounts, gives the reduced mass of a diatomic molecule.

### What phyphox measures

phyphox is a free app from RWTH Aachen University for Android and iOS. Its Spring experiment reads the acceleration sensor with gravity removed ("acceleration without g"). When the phone bounces on a spring, its acceleration along the spring is a sine wave: $a(t) = -\omega^2 x(t)$. The app finds the period from the autocorrelation of this signal (how well the signal matches a time-shifted copy of itself): the first peak after zero shift is one period. It shows the period and the frequency $f = 1/T$.

Two app features make the experiment easier:

- Remote access. The app's menu has an option to allow remote access. It then shows a web address; open it in a browser on a computer or second phone on the same Wi-Fi and you can start and stop the run without touching the bouncing phone.
- Export. The menu's export option saves the raw data as CSV (comma-separated values), tab-separated values or an Excel file (xlsx since version 1.2.1). Choose CSV with a decimal point. The first column is time in seconds, the next ones the sensor axes. You will analyse these files in lessons 14.2 and 14.5.

The accelerometer samples at a rate that depends on the phone, typically 100–500 times a second. That is plenty for a spring at 1–2 Hz.

### When do two measurements agree?

Each value comes with a standard uncertainty $u$ from its fit (lesson [05.3](../module-05/lesson-03.md)). Two independent values agree if their difference is small compared with the combined uncertainty $u_c = \sqrt{u_1^2 + u_2^2}$. A difference under $2u_c$ is normal. A difference of $3u_c$ or more means a systematic error or a wrong model, and you should find it before you report either number.

[Simulation: Oscillators — a single mass on a spring](../../simulations/oscillators/index.html?preset=single)

## Worked example

### 1. Static and dynamic k for the same spring

A 200 g bottle of water stretches a spring by 8.2 cm. Static estimate:

$$k = \frac{mg}{\Delta L} = \frac{0.200 \times 9.795}{0.082} = 23.9\ \mathrm{N/m}$$

The same spring carries the phone in a zip bag (200 g together) and phyphox reports $T = 0.588$ s. Ignoring the spring's mass:

$$k = \frac{4\pi^2 m}{T^2} = \frac{39.48 \times 0.200}{0.588^2} = 22.8\ \mathrm{N/m}$$

That is 5 % lower than the static value. The spring weighs 30 g on the kitchen scale, so $m_\text{eff} \approx 10$ g. Include it:

$$k = \frac{39.48 \times 0.210}{0.588^2} = 24.0\ \mathrm{N/m}$$

Now the two methods agree. The "missing" 5 % was the spring itself moving.

### 2. How precise is the dynamic value?

phyphox gives the period to about ±0.003 s between runs. Since $k \propto 1/T^2$, the relative uncertainty in $k$ is twice that in $T$:

$$\frac{u_k}{k} = 2\,\frac{u_T}{T} = 2 \times \frac{0.003}{0.588} = 1.0\ \%$$

So one run gives $k = 24.0 \pm 0.2$ N/m. Five masses and three runs each, fitted together, shrink this further, and the fit also gives $m_\text{eff}$ instead of you assuming it. For comparison, the H–Cl bond of lesson 04.2 is about 21 times stiffer (516 N/m), but its "mass" is $10^{-27}$ kg, so it vibrates $10^{14}$ times faster.

## Hands-on

> [!CAUTION]
> The only real risk is dropping your phone. Hang the spring from something that cannot slip: a hook screwed into a door frame, or a broom handle laid across the backs of two heavy chairs and taped down. Put the phone in a sealed zip bag and tie the bag to the spring with a knot, not tape alone. Work over a bed or a pile of cushions, with the phone no more than about 30 cm above them. Pull it down only 2–3 cm. Keep faces away from a stretched spring, and keep small children and pets out of the area. Nothing here uses mains power.

What you need: an extension spring from a hardware store (soft, about 20–40 N/m, 10–20 cm long; a 200 g load should stretch it by 5–10 cm), the phone with phyphox installed (free; Android or iOS), a zip bag and string, a kitchen scale, a tape measure, four or five small water bottles or bags of rice of known mass (weigh them), your notebook and the [Module 14 lab folder](../../labs/module-14/) with Python 3.14. Time: about 90 minutes.

### Part A — static stretch (20 min)

1. Weigh the spring alone on the kitchen scale. Write down $m_s$.
2. Hang the spring empty and read its length with the tape measure, from the top of the top coil to the bottom of the bottom coil. Always read the same two points.
3. Hang 50, 100, 150, 200, 250 and 300 g and read the length each time. Reading uncertainty: about 1 mm.
4. Type `mass_kg,length_m` into a CSV, as in `spring_static_example.csv`.

### Part B — dynamic period with phyphox (40 min)

1. Open phyphox, then the Spring experiment (in the Mechanics group). Optionally turn on remote access from the menu and open the shown address on a computer.
2. Weigh the phone in its bag. Hang it and let it come to rest.
3. Pull it down 2 cm, release gently without twisting, wait two or three bounces, then start the measurement. Let it run 20–30 s and read the period.
4. Repeat three times. Then add masses to the bag (50 g steps, up to 200 g extra) and repeat.
5. Type `mass_kg,trial,period_s` into a CSV, with the total hanging mass (phone + bag + added), as in `spring_dynamic_example.csv`.
6. For one run, use the menu's export option and save the raw data as CSV. Keep it; lesson 14.2 uses the same kind of file.

### Part C — Python (30 min)

Fill in the two TODO functions in `lesson01_spring.py`, check them on the example data, then run on yours:

```bash
py lesson01_spring.py
py lesson01_spring.py my_static.csv my_dynamic.csv
```

How you know it worked: on the example data you get $k = 24.06 \pm 0.20$ N/m (static) and $24.03 \pm 0.11$ N/m (dynamic), a difference of 0.1 combined uncertainties, and $m_\text{eff} = 10.7 \pm 1.5$ g, close to one third of the 30 g spring. On your own spring the two values of $k$ should agree within about 2 %, and $m_\text{eff}$ should land between a quarter and a half of $m_s$.

<details><summary>Reference solution and troubleshooting</summary>

`k_static`: fit length against mass with `line_fit`; $k = g/\text{slope}$, $u_k = k\,u_\text{slope}/\text{slope}$. `k_dynamic`: fit $T^2$ against mass; $k = 4\pi^2/\text{slope}$, $m_\text{eff} = \text{intercept}/\text{slope}$. Full code: `lesson01_spring_solution.py`.

If the period jumps between runs, the phone is swinging sideways or twisting as well as bouncing; release it more gently and wait for the sideways swing to die out. If the static $k$ is clearly higher than the dynamic one and $m_\text{eff}$ comes out large, check that the dynamic masses include the bag and string. If the static line is flat at the lowest load, many extension springs are wound with built-in tension and do not stretch at all until a minimum load: drop the zero-mass point and start from 50 g. If the line bends at high masses, you overstretched the spring; it will not return to its old length.

Write it up with the [lab report template](../../templates/lab-report.md): aim, both methods, data tables, both plots, the two values of $k$ with uncertainties, their difference in units of $u_c$, and $m_\text{eff}$ against $m_s/3$.

</details>

## Common mistakes

- Leaving out the spring's mass. The dynamic $k$ comes out a few percent low and seems to disagree with the static one. Fit $T^2$ against $m$ with a free intercept.
- Forcing the $T^2$ line through the origin. That hides $m_\text{eff}$ inside a wrong slope.
- Using the phone's mass without the bag, string and added weights. The total hanging mass is what oscillates.
- Starting the measurement while you are still letting go. The first bounce contains the jerk of your hand; wait two or three cycles.
- Overstretching the spring. Past its elastic limit it stays longer and $k$ changes; keep the total stretch well below the spring's own length.
- Calling two values "different" without uncertainties. A 1 % difference means nothing if each value is only good to 2 %.

## Key takeaways

- A spring's force constant can be measured statically ($k = g/\text{slope}$ of length against mass) and dynamically ($k = 4\pi^2/\text{slope}$ of $T^2$ against mass).
- The spring's own mass adds about $m_s/3$ to the moving mass; the intercept of the $T^2$ line measures it.
- phyphox's Spring experiment uses the accelerometer and autocorrelation to give the period; export raw data as CSV for your own analysis.
- Two independent values agree when their difference is under about twice their combined uncertainty.
- Measuring $k$ from a frequency is how chemists measure bond stiffness; the spring is where you test that the method works.

## Sources

- [phyphox wiki: Experiment Spring](https://phyphox.org/wiki/index.php/Experiment:_Spring) — sensor used, autocorrelation period, mounting tips.
- [phyphox version history: 1.2.1](https://phyphox.org/docs/reference/version-history/1.2.1/) — current version (September 2026); Excel export now xlsx.
- [phyphox documentation: remote interface](https://phyphox.org/docs/remote-interface/) — remote access from a browser, CSV and Excel export.
- [OpenStax University Physics Volume 1, 15.1 Simple Harmonic Motion](https://openstax.org/books/university-physics-volume-1/pages/15-1-simple-harmonic-motion) — mass on a spring and its period.
- [MIT OCW 8.03SC Vibrations and Waves](https://ocw.mit.edu/courses/8-03sc-physics-iii-vibrations-and-waves-fall-2016/) — the full course for depth.
