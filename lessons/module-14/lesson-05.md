---
id: "14.5"
module: 14
minutes: 25
practice_minutes: 75
prerequisites: ["14.2", "14.3", "04.2"]
objectives:
  - Choose a sampling rate and record length that capture a signal without aliasing and resolve the frequencies you need.
  - Compute the amplitude spectrum of an unevenly sampled phyphox recording with numpy, using resampling and a window.
  - Separate closely spaced normal-mode frequencies and explain why a short record merges them.
  - Estimate Q from a spectral line width and state when that estimate is trustworthy.
volatility: implementation
sources:
  - title: "NumPy manual, Discrete Fourier Transform (numpy.fft)"
    url: https://numpy.org/doc/stable/reference/routines.fft.html
  - title: "phyphox wiki: Experiment Audio Spectrum"
    url: https://phyphox.org/wiki/index.php/Experiment:_Audio_Spectrum
  - title: "phyphox wiki: Experiment Acceleration Spectrum"
    url: https://phyphox.org/wiki/index.php/Experiment:_Acceleration_Spectrum
  - title: "phyphox wiki: Experiment Audio Scope"
    url: https://phyphox.org/wiki/index.php/Experiment:_Audio_Scope
  - title: "MIT OpenCourseWare 8.03SC Physics III: Vibrations and Waves"
    url: https://ocw.mit.edu/courses/8-03sc-physics-iii-vibrations-and-waves-fall-2016/
last_verified: "2026-10-17"
---

# 14.5 · Signals, sampling and the Fourier transform

Every modern instrument records a time signal as a list of numbers and lets a computer turn it into a spectrum. The tool is the Fourier transform, which splits a signal into the sine waves it is made of. It is how an FT-IR spectrometer gets a spectrum out of a mirror scan, how an NMR machine gets peaks out of a decaying radio signal, and how phyphox shows the pitch of a sound. Using it well needs three rules: sample fast enough, record long enough, and know what a finite record does to a peak. This lesson teaches the rules on your own recordings: the spring from 14.2, the coupled pendulums from 14.3, and the sound of a bottle.

## Why it matters

An FT-NMR spectrometer records the free induction decay, a ringing signal like your spring's ringdown, and Fourier transforms it. If the recording is too short, two peaks 0.5 Hz apart merge into one and you miss a coupling. If the sample rate is too low, a peak shows up at a wrong, "folded" position. FT-IR has the same limits in a different disguise: the mirror travel sets the resolution in cm⁻¹. The rules are the same everywhere, and they are easier to learn on a signal you can make with a spring and a bottle than on a 600 MHz magnet.

## Core ideas

> [!NOTE]
> The mathematics is stable. The tools are not: numpy 2.5 (`numpy.fft`) and phyphox 1.2.1 were checked on 2026-10-17. Phone sensor sample rates differ from model to model; measure yours from the time column instead of assuming a number.

### Sampling and the Nyquist limit

A sensor reads the signal at regular instants $t_n = n/f_s$, where $f_s$ is the sample rate in hertz. To pin down a sine wave you need more than two samples per cycle. The highest frequency a record can represent is the Nyquist frequency

$$f_\text{N} = \frac{f_s}{2}$$

A frequency above $f_\text{N}$ does not vanish. It folds back and appears at a false, lower frequency, called an alias:

$$f_\text{alias} = |f - m f_s|\quad\text{for the whole number } m \text{ that puts it between 0 and } f_s/2$$

A phone accelerometer at 100 Hz cannot record a 60 Hz vibration; it shows it at 40 Hz. Once aliased, a signal cannot be told apart from a real one. The only cure is to sample faster or to filter out high frequencies before sampling, which is why sound cards and spectrometers have analogue filters in front of their converters.

### The discrete Fourier transform

Take $N$ samples covering a time $T = N/f_s$. The discrete Fourier transform (DFT) rewrites them as a sum of sines at the frequencies

$$f_j = \frac{j}{T},\qquad j = 0, 1, \dots, N/2$$

The fast Fourier transform (FFT) is just a quick algorithm for the DFT. In numpy, `np.fft.rfft(y)` gives the complex amplitudes and `np.fft.rfftfreq(N, 1/fs)` the matching frequencies.

Two numbers describe every spectrum:

- The frequency spacing, or resolution, $\Delta f = 1/T$. It depends only on how long you recorded, not on the sample rate. To resolve two peaks 0.03 Hz apart you need tens of seconds of data.
- The highest frequency, $f_s/2$. It depends only on the sample rate.

Zero-padding (adding zeros before the FFT) draws the peaks more smoothly but does not separate peaks that a short record merged. Only a longer recording does that.

### Leakage and windows

A finite record is the true signal multiplied by a rectangle that switches on at the start and off at the end. That sharp cut spreads each peak into side lobes, little false peaks on either side. This is spectral leakage. A window function, such as the Hann window (a smooth bump that goes to zero at both ends), tapers the edges and suppresses the side lobes. The price is a wider main peak: with a Hann window, two equal peaks need about $2/T$ separation to show as two. Use a window to look for small peaks next to big ones; skip it when you want the true width of a single decaying line.

### Uneven samples

Phone sensors do not tick perfectly evenly. phyphox writes the real time of each sample, and the gaps jitter. The FFT assumes even spacing, so first resample onto an even grid with `np.interp`. For slow signals like a spring this costs nothing.

### Line width and Q

A damped oscillation $e^{-\gamma t}\cos\omega_0 t$ does not give an infinitely sharp line. Its power spectrum is a Lorentzian peak with full width at half maximum

$$\Delta f = \frac{\gamma}{\pi},\qquad Q = \frac{f_0}{\Delta f}$$

the same $Q$ as in lesson [14.2](lesson-02.md). Fast decay, broad line; slow decay, sharp line. In spectroscopy this is lifetime broadening: a state that lives a short time gives a broad band. The width only means something if the record is several decay times $1/\gamma$ long. A shorter record makes every line about $1/T$ wide, whatever its true width, and the Q you read is too low.

### phyphox tools

- Audio Scope shows the raw microphone signal (phone microphones are usually sampled at 44.1 or 48 kHz).
- Audio Spectrum computes the FFT of short blocks of sound and shows the peak frequency. You choose the number of samples per block: more samples give finer resolution but slower updates. A block of 8192 samples lasts about 0.17 s, so its resolution is about 6 Hz.
- Acceleration Spectrum does the same for the accelerometer; its highest frequency is half the sensor's rate, which varies by phone.

## Worked example

### 1. Aliasing in practice

You record a spring at 1.40 Hz but the app, to save battery, samples only twice a second ($f_s$ = 2 Hz, Nyquist 1 Hz). The 1.40 Hz signal folds to $|1.40 - 1 \times 2| = 0.60$ Hz. The spectrum shows a clean, convincing peak at 0.60 Hz, and nothing in the data warns you. A second example: lights on Israel's 50 Hz mains flicker at 100 Hz; filmed at 30 frames per second, the flicker appears at $|100 - 3 \times 30| = 10$ Hz, a visible pulsing in the video.

### 2. How long must you record?

The three pendulum modes of lesson 14.3 lie at 0.704, 0.733 and 0.786 Hz. The closest pair is 0.028 Hz apart.

- Resolution needed with a Hann window: about $2/T \le 0.028$ Hz, so $T \ge 71$ s.
- A 20 s record has $\Delta f$ = 0.05 Hz: modes 1 and 2 merge into one lump near 0.72 Hz.
- A 120 s record ($\Delta f$ = 0.008 Hz) shows three clean peaks.

The sample rate is irrelevant here: 100 Hz is far above the 0.8 Hz signal. Only time buys resolution. The same is true in audio: to tell 440 Hz from 441 Hz you need about 2 s of sound, which at 48 kHz is about 96 000 samples, so choose a block of 131 072 (the next power of two).

## Hands-on

### Part A — Python on your recordings (40 min)

Fill in `alias_frequency` and `fwhm` in `lesson05_fft.py`. Run it on the example data, then on any phyphox CSV of your own (the number is the column to analyse):

```bash
py lesson05_fft.py
py lesson05_fft.py my_spring.csv 3
```

How you know it worked: the aliasing table gives 3.00, 1.00, 1.00 and 0.60 Hz. The 20 s pendulum record shows peaks at about 0.719 and 0.825 Hz (merged and distorted), the 120 s record three peaks at 0.7047, 0.7328 and 0.7859 Hz. For the spring ringdown the line width shrinks as the record grows: Q reads 16 from 10 s, 45 from 30 s and 80 from 60 s, still below the time-domain 110 because 60 s is only 2.4 decay times.

<details><summary>Reference solution and what it shows</summary>

`alias_frequency`: `r = f % fs`, return `min(r, fs - r)`. `fwhm`: walk left and right from the peak until the power falls below half; interpolate each crossing with `np.interp`; return the difference. Full code: `lesson05_fft_solution.py`.

Try the pendulum record without the window (set `window=False`): the 120 s spectrum then sprouts extra peaks between and beside the real ones. Those are side lobes from the sharp start and end of the record, not extra modes. With the window they vanish, at the cost of wider peaks. The ringdown shows the opposite trade-off: a window would widen its single line, so the code turns it off there.

The lesson for real instruments: a line width you read from a spectrum is the true width only when the recording is much longer than the decay time. In NMR, cutting the free induction decay short broadens every peak in exactly this way.

</details>

### Part B — the sound of a bottle (35 min)

> [!CAUTION]
> Use a plastic bottle, not glass. Blow gently across the opening; take a break after every few blows, because many fast breaths in a row can make you dizzy. Keep the phone at arm's length from your mouth, and do not play loud sounds into anyone's ear. Nothing here uses mains power.

What you need: an empty 0.5 L plastic bottle, a measuring jug, water, phyphox, your notebook.

1. Open phyphox Audio Scope and blow across the bottle mouth until you get a steady note. Look at the waveform: a near-sine wave at a few hundred hertz.
2. Switch to Audio Spectrum. Read the peak frequency with the bottle empty (air volume 500 mL).
3. Change the number of samples in Audio Spectrum (for example 4096, then 16384). Write down how the peak width and the update speed change. Resolution is $f_s/N$: about 12 Hz and 3 Hz.
4. Pour in 125 mL of water (air 375 mL), then 250 mL (air 250 mL), and read the peak each time.
5. A bottle is a Helmholtz resonator: the air in the neck is a mass, the air in the body a spring. Its frequency goes as $V^{-1/2}$. Check: the ratios $f(375)/f(500)$ and $f(250)/f(500)$ should be close to 1.15 and 1.41.

How you know it worked: a steady note gives one sharp peak with weaker overtones at multiples of it; the empty 0.5 L bottle typically sings between about 150 and 250 Hz, depending on its neck; the two ratios land within about 5 % of 1.15 and 1.41 (the neck length changes a little with the water level, so the agreement is not perfect). Record your readings on a [notebook page](../../templates/notebook-page.md).

## Common mistakes

- Trusting a peak above the Nyquist frequency, or a peak that could be an alias. Check that $f_s$ is at least several times the highest frequency you expect.
- Thinking a higher sample rate gives finer resolution. Resolution is $1/T$; only a longer recording sharpens peaks.
- Believing zero-padding adds resolution. It interpolates the curve but cannot split peaks a short record merged.
- Running the FFT on uneven time stamps. Resample onto an even grid first.
- Reading side lobes as real peaks. Apply a window and see whether they survive.
- Reading Q from a line width when the record is shorter than a few decay times. The width is then set by $1/T$.

## Key takeaways

- Sample at more than twice the highest frequency present; anything above $f_s/2$ folds to a false alias.
- A record of length $T$ resolves frequencies $1/T$ apart; with a Hann window, peaks need about $2/T$ to separate.
- Windows trade side lobes for wider peaks; use them to find weak peaks, not to measure a single line's width.
- A decaying signal gives a Lorentzian line of width $\gamma/\pi$; $Q = f_0/\Delta f$ if the record is long enough.
- FT-IR and FT-NMR obey the same rules: scan length or acquisition time sets the resolution.

## Sources

- [NumPy manual, Discrete Fourier Transform](https://numpy.org/doc/stable/reference/routines.fft.html) — `rfft`, `rfftfreq` and the conventions used.
- [phyphox wiki: Audio Spectrum](https://phyphox.org/wiki/index.php/Experiment:_Audio_Spectrum) — block FFT, choice of sample count, resolution limited by block length.
- [phyphox wiki: Acceleration Spectrum](https://phyphox.org/wiki/index.php/Experiment:_Acceleration_Spectrum) — accelerometer FFT; highest frequency is half the device's sensor rate.
- [phyphox wiki: Audio Scope](https://phyphox.org/wiki/index.php/Experiment:_Audio_Scope) — the raw microphone waveform.
- [MIT OCW 8.03SC Vibrations and Waves](https://ocw.mit.edu/courses/8-03sc-physics-iii-vibrations-and-waves-fall-2016/) — Fourier analysis of oscillations in depth.
