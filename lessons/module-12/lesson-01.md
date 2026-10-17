---
id: "12.1"
module: 12
minutes: 20
practice_minutes: 65
prerequisites: ["04.5", "07.2", "02.1"]
objectives:
  - Use the Rydberg formula to predict a hydrogen line and identify the transition behind a measured wavelength.
  - Compute the de Broglie wavelength of an electron or a molecule and decide whether quantum effects matter for it.
  - Estimate the minimum kinetic energy of a confined electron from the uncertainty principle.
  - Fit the Rydberg constant from NIST hydrogen wavelengths, including the air-to-vacuum correction.
volatility: concept
sources:
  - title: "NIST Handbook of Basic Atomic Spectroscopic Data: strong lines of hydrogen"
    url: https://physics.nist.gov/PhysRefData/Handbook/Tables/hydrogentable2.htm
  - title: "NIST CODATA 2022: Rydberg constant"
    url: https://physics.nist.gov/cgi-bin/cuu/Value?ryd
  - title: "NIST CODATA 2022: electron mass"
    url: https://physics.nist.gov/cgi-bin/cuu/Value?me
  - title: "LibreTexts Physical Chemistry, chapter 1: The Dawn of the Quantum Theory"
    url: https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Physical_Chemistry_(LibreTexts)/01%3A_The_Dawn_of_the_Quantum_Theory
  - title: "MIT OpenCourseWare 5.61 Physical Chemistry (Field, Fall 2017)"
    url: https://ocw.mit.edu/courses/5-61-physical-chemistry-fall-2017/
last_verified: "2026-10-17"
---

# 12.1 · Why classical physics fails: photons, spectra and waves

Around 1900 physics could explain planets, steam engines and radio waves, but not why a hot gas of hydrogen glows at only four sharp visible colours, or why an atom does not collapse. This lesson walks through the experiments that broke classical physics and the two ideas that replaced it: energy comes in quanta, and matter behaves as a wave. You will predict hydrogen lines with the Rydberg formula, decide when a particle is "quantum" from its de Broglie wavelength, and fit the Rydberg constant from real NIST wavelengths.

## Why it matters

An astronomer sees a red line at 656.3 nm in the light of a distant nebula and says "hydrogen". A forensic lab burns a paint chip in a flame and names the metals from the colours. A chemist shines ultraviolet light on a molecule and reads its electronic structure from the absorption bands. All of this rests on one fact: atoms and molecules absorb and emit light only at particular energies. Classical physics predicts the opposite, a smooth smear of colours and atoms that collapse in a fraction of a nanosecond. Knowing where classical physics fails tells you when you need quantum mechanics and when you can safely ignore it.

## Core ideas

> [!NOTE]
> The physics here is stable and a century old. The constants are CODATA 2022 values from NIST and the hydrogen wavelengths are from the NIST Handbook of Basic Atomic Spectroscopic Data, both checked 2026-10-17. The lab uses numpy and matplotlib as pinned in `labs/common/requirements.txt`.

### Three experiments classical physics could not explain

1. Hot-body (blackbody) radiation. A glowing object emits a spectrum whose peak moves to shorter wavelength as it gets hotter. Classical theory predicts that the emitted power grows without limit at short wavelength, the "ultraviolet catastrophe". Max Planck fixed it in 1900 by assuming that an oscillator of frequency $\nu$ can only hold energy in whole steps of $h\nu$, where $h = 6.626\,070\,15\times10^{-34}$ J s is Planck's constant.
2. The photoelectric effect. Light ejects electrons from a metal only above a threshold frequency, however bright it is. Einstein explained it with photons of energy $E = h\nu$, as you saw in [04.5](../module-04/lesson-05.md).
3. Atomic line spectra and stability. A classical electron circling a nucleus is an accelerating charge, so it should radiate continuously and spiral into the nucleus in about $10^{-11}$ s. Real atoms are stable and emit only sharp lines.

The common thread: energy inside atoms and molecules is quantised. It can take only certain values, called energy levels. A photon is absorbed or emitted only when its energy matches the gap between two levels:

$$\Delta E = E_\text{upper} - E_\text{lower} = h\nu = \frac{hc}{\lambda}$$

### Line spectra and the Rydberg formula

Hydrogen's lines fit a simple empirical formula, found by Rydberg in 1888:

$$\frac{1}{\lambda} = R_\mathrm{H}\left(\frac{1}{n_1^2} - \frac{1}{n_2^2}\right),\qquad n_2 > n_1$$

where $n_1$ and $n_2$ are positive whole numbers and $R_\mathrm{H} = 1.096\,776\times10^{7}$ m⁻¹ is the Rydberg constant for hydrogen. The visible Balmer series has $n_1 = 2$. The formula says the energy levels of hydrogen are

$$E_n = -\frac{hcR_\mathrm{H}}{n^2} = -\frac{13.598\ \text{eV}}{n^2}$$

Energy zero is the electron at rest far away from the proton, so bound levels are negative. The ionisation energy from $n = 1$ is 13.598 eV.

Tiny example: the $n = 3 \to 2$ line. $1/\lambda = R_\mathrm{H}(1/4 - 1/9) = R_\mathrm{H}\times 5/36 = 1.5233\times10^{6}$ m⁻¹, so $\lambda = 656.47$ nm in vacuum. That is H-alpha, the red line in every hydrogen lamp.

The constant $R_\mathrm{H}$ is not quite the fundamental Rydberg constant $R_\infty = 10\,973\,731.568\,157$ m⁻¹ (CODATA 2022). $R_\infty$ assumes an infinitely heavy nucleus. Hydrogen's proton is only 1836 times heavier than the electron, so the electron's mass is replaced by the reduced mass $\mu = m_e/(1 + m_e/m_p)$, and $R_\mathrm{H} = R_\infty/(1 + m_e/m_p)$. You met reduced mass for vibrations in [03.4](../module-03/lesson-04.md); the same idea works for atoms.

### Bohr's model: right numbers, wrong picture

In 1913 Niels Bohr reproduced $E_n$ by assuming circular orbits whose angular momentum is a whole multiple of $\hbar = h/2\pi$. The smallest orbit has radius $a_0 = 52.9$ pm, the Bohr radius. Bohr's model gets hydrogen's energies right and gave chemistry the idea of shells, which you used in [07.2](../module-07/lesson-02.md). But it fails for every atom with more than one electron, and it is wrong about orbits: electrons do not move on paths. The correct picture, wavefunctions and orbitals, starts in [12.2](lesson-02.md).

### Matter is a wave too

In 1924 Louis de Broglie proposed that every particle with momentum $p$ has a wavelength

$$\lambda = \frac{h}{p} = \frac{h}{\sqrt{2mE_\text{kin}}}$$

For an electron this gives a handy shortcut, $\lambda\,[\text{nm}] = 1.226/\sqrt{E_\text{kin}\,[\text{eV}]}$. An electron with 54 eV has $\lambda = 0.167$ nm, close to the spacing of atoms in a crystal. In 1927 Davisson and Germer fired such electrons at a nickel crystal and saw diffraction, the signature of waves.

The rule of thumb that follows: quantum effects matter when a particle's de Broglie wavelength is comparable to the size of the region it is confined in. An electron in an atom (0.1 nm) is fully quantum. A 150 g ball at 30 m/s has $\lambda \approx 10^{-34}$ m and behaves classically.

### The uncertainty principle sets a minimum energy

Heisenberg's uncertainty principle says that position and momentum cannot both be sharp:

$$\Delta x\,\Delta p \ge \frac{\hbar}{2}$$

Confine an electron to $\Delta x = 0.1$ nm and its momentum must spread by at least $\Delta p = \hbar/(2\Delta x) = 5.3\times10^{-25}$ kg m/s. That spread carries kinetic energy of about $(\Delta p)^2/2m_e \approx 1$ eV. So a confined particle can never be at rest, and the smaller the box, the higher this zero-point energy. That is why atoms have a size: pulling the electron closer to the nucleus lowers its potential energy but raises its kinetic energy, and the balance sits near $a_0$.

### When can a chemist ignore quantum mechanics?

| Motion | Typical $\lambda$ | Confinement | Quantum? |
|---|---|---|---|
| Electron in a bond | about 0.4 nm | about 0.1 nm | yes, always |
| H atom vibrating in a bond | about 0.1 nm | about 0.01 nm amplitude | yes: vibrations are quantised (12.4) |
| N₂ moving in a flask | 0.03 nm | cm | no: translation is classical |
| Molecule rotating | levels about 1–20 cm⁻¹ apart | — | quantised, but many levels filled at room temperature (12.5) |

## Worked example

### 1. Which transition made this line?

A hydrogen lamp shows a violet line at 410.17 nm (measured in air). Which transition is it?

1. Convert to vacuum. Air has refractive index about 1.000282 at 410 nm, so $\lambda_\text{vac} = 410.17 \times 1.000282 = 410.29$ nm.
2. $1/\lambda = 1/(410.29\times10^{-9}\ \text{m}) = 2.4373\times10^{6}$ m⁻¹.
3. Divide by $R_\mathrm{H}$: $2.4373\times10^{6}/1.096776\times10^{7} = 0.22222$.
4. For the Balmer series, $1/4 - 1/n_2^2 = 0.22222$, so $1/n_2^2 = 0.02778$ and $n_2 = 6.00$.

It is H-delta, $n = 6 \to 2$. If you skip step 1 you get $n_2 = 6.01$, still clearly 6. For precise work, as in the lab, the air correction matters: it shifts $R_\mathrm{H}$ by about 300 parts per million.

### 2. Is a nitrogen molecule in air quantum?

At 298 K a typical N₂ molecule ($m = 28.01$ u $= 4.65\times10^{-26}$ kg) has momentum about $p = \sqrt{3mk_BT}$.

1. $k_BT = 1.380649\times10^{-23} \times 298 = 4.11\times10^{-21}$ J.
2. $p = \sqrt{3 \times 4.65\times10^{-26} \times 4.11\times10^{-21}} = 2.40\times10^{-23}$ kg m/s.
3. $\lambda = h/p = 6.626\times10^{-34}/2.40\times10^{-23} = 2.8\times10^{-11}$ m $= 0.028$ nm.

Molecules in air are about 3 nm apart, a hundred times more than $\lambda$, so their translation is classical. That is why the ideal-gas law of Module 7 works without quantum mechanics.

## Hands-on

What you need: pencil and calculator; Python with the course packages and the [Module 12 lab folder](../../labs/module-12/); for Part C an old CD or DVD, a cardboard tube or box, tape, and two or three different lamps. Record everything on a [notebook page](../../templates/notebook-page.md). Time: about 65 minutes.

### Part A — pencil (15 min)

1. Predict the wavelength (vacuum) of the $n = 4 \to 2$ line of hydrogen.
2. What is the longest wavelength in the Lyman series ($n_1 = 1$), and in which region of the spectrum is it?
3. An electron microscope accelerates electrons through 100 kV. Ignoring relativity, what is their de Broglie wavelength?
4. Estimate the minimum kinetic energy of an electron confined to a 1.0 nm conjugated molecule, using $\Delta p \ge \hbar/(2\Delta x)$.

<details><summary>Answers to Part A</summary>

1. $1/\lambda = R_\mathrm{H}(1/4 - 1/16) = R_\mathrm{H}\times 3/16 = 2.0565\times10^{6}$ m⁻¹, $\lambda = 486.27$ nm (H-beta, blue-green; 486.14 nm in air).
2. $n = 2 \to 1$: $1/\lambda = R_\mathrm{H}\times 3/4$, $\lambda = 121.6$ nm, in the vacuum ultraviolet.
3. $\lambda = 1.226/\sqrt{100\,000} = 0.0039$ nm $= 3.9$ pm. Relativity shortens it to 3.7 pm, a 5 % correction at this voltage.
4. $\Delta p = 1.055\times10^{-34}/(2\times10^{-9}) = 5.3\times10^{-26}$ kg m/s; $E \approx (\Delta p)^2/2m_e = 1.5\times10^{-21}$ J $\approx 0.01$ eV. The particle in a box of 12.2 gives the exact answer.

</details>

### Part B — Python: the Rydberg constant from NIST data (30 min)

The file `balmer_nist.csv` holds the air wavelengths of the four visible hydrogen lines from the NIST Handbook.

1. Open `lesson01_balmer.py` and fill in `air_to_vacuum` (the Edlén formula for the refractive index of air is given in the comments) and `fit_rydberg` (a straight line of $1/\lambda$ against $1/4 - 1/n^2$).
2. Run it from the lab folder:

```bash
py lesson01_balmer.py
```

3. Look at `runs/lesson01_balmer.png`.

How you know it worked: the vacuum wavelengths are 656.4665, 486.2719, 434.1682 and 410.2898 nm; the fitted slope is $R_\mathrm{H} = 1.096797\times10^{7}$ m⁻¹ with a standard error near 100 m⁻¹ and an intercept close to zero; that is within 20 parts per million of $R_\infty/(1 + m_e/m_p) = 1.0967758\times10^{7}$ m⁻¹. Without the air correction the error grows to about 310 ppm. The script also prints the ionisation energy of hydrogen, 13.598 eV, and the Balmer series limit, 364.7 nm.

<details><summary>Reference solution and what to notice</summary>

`air_to_vacuum` multiplies by $n_\text{air} = 1 + 10^{-8}\,[8342.13 + 2\,406\,030/(130 - \sigma^2) + 15\,997/(38.9 - \sigma^2)]$ with $\sigma = 1/\lambda$ in µm⁻¹. `fit_rydberg` uses `np.polyfit(x, y, 1, cov=True)` and takes the square root of `cov[0, 0]` as the slope's standard error. Full code: `lesson01_balmer_solution.py`.

What to notice: the remaining 20 ppm is not noise. Each NIST "line" is a cluster of fine-structure components that the simple formula ignores, and the table lists the strongest one. A straight line through the origin is the test of the theory: if the levels were not $-hcR_\mathrm{H}/n^2$, no single slope would fit all four points.

</details>

### Part C — home: see line spectra with a CD (20 min)

> [!WARNING]
> Never point the spectroscope at the Sun, and never look into a laser. Do not open, break or heat any lamp: compact fluorescent lamps contain a small amount of mercury. Use only lamps already working in normal fittings.

1. Cut a narrow slit (about 1 mm) in a piece of card and tape it over one end of a tube or box. Tape a piece of CD or DVD at the other end, tilted about 45°, so that you look at the shiny side through a hole in the side of the box.
2. Point the slit at a lamp from about 1 m. Look at the coloured band reflected by the disc.
3. Compare an old incandescent or halogen bulb (or white paper in daylight), a white LED, and a compact fluorescent lamp or a yellow sodium street lamp if you have one. Sketch each spectrum and note which are smooth and which are made of separate bright lines.

Expected result: the incandescent bulb and daylight give a smooth rainbow (a hot solid, like a blackbody). The white LED gives a narrow blue band plus a broad yellow one (a blue chip and a phosphor). The fluorescent lamp shows sharp lines, including a bright green one (mercury at 546 nm) and a violet-blue one (436 nm). A sodium lamp shows one strong yellow line near 589 nm. Sharp lines mean free atoms with quantised levels. This home spectroscope does not train measuring wavelengths precisely; Module 25 builds a calibrated phone spectrometer.

## Common mistakes

- Using wavelengths in air in formulas that assume vacuum. The difference is about 0.03 %, small but larger than the precision of tabulated lines.
- Using $R_\infty$ for hydrogen. For precise work use $R_\mathrm{H} = R_\infty/(1 + m_e/m_p)$; the difference is 545 ppm.
- Putting $n_1 > n_2$ in the Rydberg formula and getting a negative wavelength. The lower level always has the smaller $n$.
- Calling the Bohr orbit the "real" picture of the atom. It reproduces hydrogen's energies, but electrons do not follow paths; use orbitals (12.5) for anything beyond hydrogen.
- Using $\lambda = h/(mv)$ with the speed of light for an electron, or forgetting to convert eV to joules before $\sqrt{2mE}$.
- Concluding that everything small is quantum. The test is the de Broglie wavelength against the confinement size, not the mass alone.

## Key takeaways

- Blackbody radiation, the photoelectric effect and sharp atomic lines all show that energy in atoms is quantised; light is absorbed or emitted only when $h\nu$ matches a level gap.
- Hydrogen's levels are $E_n = -13.598\ \text{eV}/n^2$; the Rydberg formula follows, with $R_\mathrm{H}$ corrected for the reduced mass.
- Every particle has a de Broglie wavelength $\lambda = h/p$; quantum behaviour appears when $\lambda$ is comparable to the size of the confinement.
- The uncertainty principle gives a confined particle a minimum kinetic energy that grows as the box shrinks.
- Electrons in molecules are always quantum; molecular translation in a flask is classical.

## Sources

- [NIST Handbook of Basic Atomic Spectroscopic Data, hydrogen strong lines](https://physics.nist.gov/PhysRefData/Handbook/Tables/hydrogentable2.htm) — air wavelengths 6562.85, 4861.36, 4340.46 and 4101.74 Å used in the lab.
- [NIST CODATA 2022: Rydberg constant](https://physics.nist.gov/cgi-bin/cuu/Value?ryd) — $R_\infty = 10\,973\,731.568\,157(12)$ m⁻¹.
- [NIST CODATA 2022: electron mass](https://physics.nist.gov/cgi-bin/cuu/Value?me) — $m_e = 9.109\,383\,7139\times10^{-31}$ kg.
- [LibreTexts Physical Chemistry, chapter 1: The Dawn of the Quantum Theory](https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Physical_Chemistry_(LibreTexts)/01%3A_The_Dawn_of_the_Quantum_Theory) — blackbody radiation, photoelectric effect, Bohr model, de Broglie and uncertainty.
- [MIT OCW 5.61 Physical Chemistry (Field, Fall 2017)](https://ocw.mit.edu/courses/5-61-physical-chemistry-fall-2017/) — the course this module follows; lectures 1–4 cover this lesson.
