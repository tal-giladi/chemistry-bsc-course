---
id: "30.3"
module: 30
minutes: 20
practice_minutes: 100
prerequisites: ["23.1", "14.5", "21.3", "09.3"]
objectives:
  - Derive the resonance frequencies of a tube closed at one end and design a length series that removes the end correction from the result.
  - Measure the speed of sound in air at home with a phone running phyphox Audio Spectrum, with a stated uncertainty.
  - Calculate the heat-capacity ratio of humid air from the speed of sound, temperature and humidity, and propagate the uncertainties.
  - Decide from the measured γ how many degrees of freedom of N₂ and O₂ are active at room temperature.
volatility: implementation
sources:
  - title: "Cramer, The variation of the specific heat ratio and the speed of sound in air with temperature, pressure, humidity, and CO2 concentration, J. Acoust. Soc. Am. 93, 2510 (1993)"
    url: https://doi.org/10.1121/1.405827
  - title: "Levine and Schwinger, On the radiation of sound from an unflanged circular pipe, Phys. Rev. 73, 383 (1948)"
    url: https://doi.org/10.1103/PhysRev.73.383
  - title: "phyphox wiki: Experiment Audio Spectrum"
    url: https://phyphox.org/wiki/index.php/Experiment:_Audio_Spectrum
  - title: "phyphox version history: 1.2.1"
    url: https://phyphox.org/docs/reference/version-history/1.2.1/
  - title: "NIST CODATA 2022: molar gas constant"
    url: https://physics.nist.gov/cgi-bin/cuu/Value?r
last_verified: "2026-10-17"
---

# 30.3 · Speed of sound and the heat-capacity ratio of air

Sound is a pressure wave, and the squeezes and stretches happen too fast for heat to flow. So the speed of sound depends on how stiff a gas is under adiabatic compression, and that stiffness is the heat-capacity ratio γ that you measured with a bottle and a manometer in lesson [23.1](../module-23/lesson-01.md). Here you measure it again, this time with a tube, a tape measure and the microphone of your phone. It is one of the few experiments of a third-year physical chemistry lab that you can do at home with full precision, and it gives γ of air to about half a per cent.

## Why it matters

The speed of sound is the most precise way to measure γ, and acoustic thermometers based on it are among the most accurate thermometers in the world. Gas companies and anaesthetic monitors check gas mixtures from their sound speed. For a chemist the point is that a single number, γ, tells you which ways a molecule stores energy. If air gave 1.67, its molecules would not rotate; if it gave 1.29, they would vibrate. The answer you get in your kitchen is a direct test of the quantum picture of [21.3](../module-21/lesson-03.md): rotation active, vibration frozen.

## Core ideas

> [!NOTE]
> The physics is stable. The app details are not: they were checked against phyphox 1.2.1 and its Audio Spectrum wiki page on 2026-10-17; menu names can change between versions. $R$ = 8.314 462 618 J mol⁻¹ K⁻¹ (CODATA 2022, exact). Reference values for air follow Cramer (1993): dry air at 20 °C has $c$ = 343.2 m/s. The example data in the lab folder are generated, not measured.

### Sound speed and γ

For an ideal gas the speed of sound is

$$c = \sqrt{\frac{\gamma RT}{M}}$$

with $M$ the molar mass in kg/mol and $T$ in kelvin. Solved for γ:

$$\gamma = \frac{Mc^2}{RT}$$

Tiny example: dry air, $M$ = 0.028965 kg/mol, 20.0 °C, $c$ = 343.2 m/s gives $\gamma = 0.028965 \times 343.2^2/(8.3145 \times 293.15) = 1.3997$. The rigid-diatomic value is $7/5$ = 1.400 (lesson 23.1): three translations and two rotations, no vibration.

Why adiabatic? A sound wave at a few hundred hertz squeezes each parcel of air for about a millisecond, in which heat diffuses only about 0.1 mm, far less than the wavelength. The compression warms the gas and stiffens it; that is where γ comes from. Newton assumed isothermal compression and got a speed 16 % too low; Laplace added γ.

### Standing waves in a closed tube

Hold a tube closed at one end and tap or snap near the open end. The air column rings at its resonances. At the closed end the air cannot move (a displacement node); at the open end the pressure stays at the room value (a pressure node). The column therefore holds an odd number of quarter wavelengths:

$$f_n = \frac{n\,c}{4(L + e)}, \qquad n = 1, 3, 5, \dots$$

Only odd harmonics appear, so the spectrum of a closed tube has peaks in the ratio 1 : 3 : 5 : 7. That ratio is your first check that you are seeing the tube and not the room.

The **end correction** $e$ is there because the pressure node sits a little outside the open end: the moving air just beyond the rim belongs to the column. For a thin-walled, unflanged round tube of inner radius $r$, Levine and Schwinger (1948) calculated $e = 0.6133\,r$. For a 4 cm tube, $e$ = 12 mm, which on a 30 cm tube is a 4 % error in $c$ and an 8 % error in γ. You must not ignore it.

### Remove the end correction with a length series

Rearrange the resonance condition into a straight line:

$$L = c \cdot \frac{n}{4f_n} - e$$

Plot $L$ against $n/(4f_n)$ for several lengths and modes. The slope is $c$, and the intercept is $-e$. You never need to know $e$ in advance, and the fitted $e$ is a check: it should come out close to $0.61r$. This is the standard trick of experimental physical chemistry: when a correction is hard to calculate, design the experiment so that it falls into the intercept.

### Humid air and the error budget

Room air contains water vapour, which is lighter (18.0 g/mol) than dry air (28.96 g/mol). The water mole fraction is $x_w = \text{RH} \times p_\text{sat}(T)/p$. At 23 °C and 50 % relative humidity, $x_w$ = 0.014 and $M$ = 28.81 g/mol. Ignoring humidity would make γ 0.5 % too high, because $M$ enters γ directly.

The relative uncertainty of γ is

$$\frac{\sigma_\gamma}{\gamma} = \sqrt{\left(2\frac{\sigma_c}{c}\right)^2 + \left(\frac{\sigma_T}{T}\right)^2 + \left(\frac{\sigma_M}{M}\right)^2}$$

The factor 2 matters: a 0.5 % error in $c$ becomes 1 % in γ. A 1 K error in $T$ costs 0.34 %, a 10 % error in RH about 0.1 %. Real-gas corrections (about 0.1 %) and the drag of the tube wall (a fraction of a per cent for tubes wider than about 3 cm) can be neglected here.


## Worked example

A tube of inner radius 2.0 cm, closed at one end, at 23.0 °C, 50 % RH, 101.0 kPa. Five lengths, fundamental frequencies:

| $L$ (m) | 0.300 | 0.400 | 0.500 | 0.600 | 0.700 |
|---|---|---|---|---|---|
| $f_1$ (Hz) | 276.7 | 210.5 | 169.2 | 141.1 | 121.4 |

1. Naive single-length estimate: $c = 4Lf_1$ for the 0.300 m tube is $4 \times 0.300 \times 276.7 = 332$ m/s, 4 % low, because $L$ leaves out $e$.
2. Line fit of $L$ against $1/(4f_1)$ (in ms: 0.9035, 1.1876, 1.4775, 1.7718, 2.0593): slope $c$ = 345.3 ± 1.1 m/s, intercept $-e = -0.0110$ m, so $e$ = 11 mm, close to $0.6133 \times 20 = 12.3$ mm.
3. Molar mass: $p_\text{sat}$(23 °C) = 2.81 kPa, $x_w = 0.5 \times 2.81/101.0 = 0.0139$, $M = 0.9861 \times 28.965 + 0.0139 \times 18.015 = 28.81$ g/mol.
4. $\gamma = 0.028812 \times 345.3^2/(8.3145 \times 296.15) = 1.395$.
5. Uncertainty: with $\sigma_c$ = 1.1 m/s (0.32 %, so 0.64 % in γ), $\sigma_T$ = 0.5 K (0.17 %) and $\sigma_\text{RH}$ = 0.10 (0.1 %), $\sigma_\gamma$ = 0.009. Result: $\gamma = 1.395 \pm 0.009$, so $C_{V,m} = R/(\gamma - 1) = 2.53R$.

Interpretation: 2.5 R means five active degrees of freedom. A vibrating diatomic would give 3.5 R and γ = 1.29; that is excluded by 12 standard deviations. Compare with lesson 23.1, where the Clément–Desormes bottle gave ± 0.02: the acoustic method is twice as precise with cheaper equipment, and adding the third and fifth harmonics (Hands-on) improves it further.

## Hands-on

> [!CAUTION]
> Keep sounds at a comfortable volume: snaps, taps or quiet noise from a second phone, never a speaker held to your ear or played at full volume. Cut tubes with a saw or knife on a board, cutting away from your body; let an adult do it if you are not used to tools. If you use a vase with water, keep the phone well above the water and the vase on a stable surface. No chemicals are used.

What you need: a phone with phyphox (free; checked with version 1.2.1); a tube 50–100 cm long with a 3–6 cm inner diameter that you can close at one end (a cardboard poster tube with its cap, a PVC pipe with a cap, or a tall straight vase); a tight plug you can push to different depths (a rolled towel or a sock on the end of a stick), or water to pour into the vase; a tape measure; a thermometer and the relative humidity (a hygrometer or a local weather service); the [Module 30 lab folder](../../labs/module-30/) and the [lab report template](../../templates/lab-report.md). Time: about 100 minutes. This is the real experiment, not a substitute. What it does not train is the use of a laboratory acoustic interferometer and a signal generator.

### Part A — find the resonances of one tube (25 min)

1. Measure the inner diameter at the open end and halve it to get $r$. Measure $L$ from the inside of the closed end (or the plug face, or the water surface) to the rim, to 1 mm.
2. Open phyphox, then Audio Spectrum. In its settings choose 16384 samples (at 48 kHz this gives about 2.9 Hz per point, lesson [14.5](../module-14/lesson-05.md)).
3. Hold the phone so the microphone is level with the rim, about 1 cm outside the tube, not covering it. Snap your fingers or tap the rim several times while the spectrum runs. Read the peak frequencies (pause the measurement, or export the data from the three-dot menu).
4. Check the pattern: peaks near $f_1$, $3f_1$, $5f_1$ and no strong peaks at the even multiples. If the even ones are strong, the closed end leaks or the phone is in the column.
5. Note the air temperature near the tube and the relative humidity.

How you know it worked: for a 50 cm tube you see peaks near 170, 510 and 850 Hz with ratios 1 : 3 : 5 within 1 %. Run `py lesson03_sound.py spectrum my_audio_spectrum.csv` on your export to list the peaks.

### Part B — the length series (40 min)

1. Change the length five times between about 30 and 70 cm (push the plug in, or add water). At each length record $f_1$, $f_3$ and $f_5$: 15 numbers. Repeat any length whose peaks look doubled.
2. Save them as `length_m,mode_n,f_Hz` in `my_tube.csv` (one row per resonance), in the lab folder.
3. Open `lesson03_sound.py`. Complete `speed_from_series()` (line fit of $L$ against $n/4f$), `moist_air_molar_mass()` and `gamma_from_speed()`. Run on the example and then on your data:

```bash
py lesson03_sound.py
py lesson03_sound.py my_tube.csv 22.5 0.45 100.8 0.019
```

The four numbers are the air temperature in °C, the relative humidity as a fraction, the pressure in kPa (use 101.3 if you do not know it; 1 kPa changes $M$ by much less than 0.1 %) and the inner radius of the tube in metres.

How you know it worked: on the example data the script prints peaks at 168.8, 506.2, 843.6 and 1181.1 Hz (ratios 1, 3, 5, 7); $c$ = 345.4 ± 0.8 m/s from all 15 resonances; $e$ = 11 ± 1 mm against 12.3 mm from theory; naive $4Lf_1$ values of 332–340 m/s; $M$ = 28.812 g/mol; $\gamma$ = 1.396 ± 0.007 and $C_{V,m}$ = 2.52 R. On your data, $\gamma$ between 1.38 and 1.42 means the experiment worked. The plot `runs/lesson03_sound.png` shows all three modes on one straight line.

<details><summary>Reference solution</summary>

```python
x = np.asarray(n) / (4 * np.asarray(f))
a, b, sa, sb, _, _ = linfit(x, L)
return b, sb, -a, sa                                    # speed_from_series
p_sat = 0.61121 * math.exp((18.678 - T_C / 234.5) * (T_C / (257.14 + T_C)))
x = RH * p_sat / p_kPa
return (1 - x) * M_DRY + x * M_WATER                    # moist_air_molar_mass
return M * c**2 / (R * T_K)                             # gamma_from_speed
```

Full code: `lesson03_sound_solution.py`. If your three modes do not fall on one line, look for a mode you mislabelled (an even harmonic from a leak, or a room noise). A constant error in every length, for example measuring to the outside of the cap, is harmless: it goes into the intercept along with $e$.

</details>

### Part C — report and pencil (35 min)

Write a one-page report with the template (apparatus sketch, the plot, $c$, $e$, γ with its error budget, degrees of freedom). Then answer:

1. Your thermometer reads 2 K too high. By how much, and in which direction, does γ change?
2. You forget the humidity on a humid summer day (30 °C, 80 % RH, $p_\text{sat}$ = 4.25 kPa). Estimate the error in γ.
3. A friend fills the tube with helium from a party balloon and finds the fundamental 2.9 times higher. What γ does that suggest, taking $M$ = 4.0 g/mol? (Do not breathe the helium.)

<details><summary>Answers</summary>

1. γ is proportional to 1/T, so γ comes out too low by 2/296 = 0.7 %, about 0.009.
2. $x_w = 0.8 \times 4.25/101.3 = 0.034$; $M$ drops from 28.97 to 28.59 g/mol, 1.3 %. Using the dry $M$ makes γ 1.3 % too high, about 1.418 instead of 1.400.
3. Same tube, so $c_\text{He}/c_\text{air} = 2.9$ and $\gamma_\text{He} = \gamma_\text{air}(M_\text{He}/M_\text{air})(c_\text{He}/c_\text{air})^2 = 1.40 \times (4.0/28.8) \times 8.41 = 1.64$, close to 5/3 for a monatomic gas. Balloon helium is often mixed with some air, which lowers the frequency ratio a little.

</details>

## Common mistakes

- **Using one length and $c = 4Lf$.** The end correction makes $c$ several per cent low. Use a length series and let $e$ go into the intercept.
- **Putting the phone inside the tube.** It shortens the column and adds a reflector; keep the microphone just outside the rim.
- **Mistaking a room noise for the fundamental.** Check the 1 : 3 : 5 pattern; mains hum sits at 50 and 100 Hz in Israel.
- **Forgetting that γ goes as $c^2$.** The relative uncertainty of γ is at least twice that of $c$.
- **Ignoring humidity.** Moist air is lighter; on a humid day the error is about 1 %, larger than everything else in the budget.
- **Temperature from the wrong place.** Read the air near the tube, not the wall thermostat.

## Key takeaways

- $c = \sqrt{\gamma RT/M}$, so $\gamma = Mc^2/RT$; sound is adiabatic because heat cannot follow a millisecond squeeze.
- A tube closed at one end resonates at $f_n = nc/4(L + e)$ with only odd $n$.
- A length series turns the end correction into an intercept: slope $c$, intercept $-e \approx -0.61r$.
- Humidity lowers $M$; temperature and humidity must be measured, and $c$ counts twice in the error budget.
- Air at room temperature gives γ = 1.40 within about 0.01: rotation active, vibration frozen.

## Sources

- [Cramer, J. Acoust. Soc. Am. 93, 2510 (1993)](https://doi.org/10.1121/1.405827) — reference speed of sound and γ of air as functions of temperature, pressure, humidity and CO₂; 343.2 m/s for dry air at 20 °C.
- [Levine and Schwinger, Phys. Rev. 73, 383 (1948)](https://doi.org/10.1103/PhysRev.73.383) — end correction 0.6133 r of an unflanged circular pipe.
- [phyphox wiki: Experiment Audio Spectrum](https://phyphox.org/wiki/index.php/Experiment:_Audio_Spectrum) — how the app's FFT spectrum works and its settings.
- [phyphox version history: 1.2.1](https://phyphox.org/docs/reference/version-history/1.2.1/) — the app version checked for this lesson.
- [NIST CODATA 2022: molar gas constant](https://physics.nist.gov/cgi-bin/cuu/Value?r) — $R$ exact.
