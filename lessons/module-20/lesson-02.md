---
id: "20.2"
module: 20
minutes: 20
practice_minutes: 40
prerequisites: ["20.1", "12.5"]
objectives:
  - Assign the lines of a pure rotational spectrum and extract B, the centrifugal distortion constant D and the bond length.
  - Explain the difference between B_e and B_0, and between r_e and r_0.
  - Predict how isotopic substitution shifts rotational lines.
  - Decide which polyatomic molecules (linear, symmetric, spherical and asymmetric tops) show a rotational spectrum and what it looks like.
volatility: concept
sources:
  - title: "NIST Diatomic Spectral Database (SRD 114)"
    url: https://physics.nist.gov/cgi-bin/MolSpec/diperiodic.pl
  - title: "NIST Chemistry WebBook, carbon monoxide: constants of diatomic molecules"
    url: https://webbook.nist.gov/cgi/cbook.cgi?ID=C630080&Mask=1000
  - title: "LibreTexts Physical Chemistry, 13.4 Unequal Spacings in Pure Rotational Spectra"
    url: https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Physical_Chemistry_(LibreTexts)/13%3A_Molecular_Spectroscopy/13.04%3A_Unequal_Spacings_in_Pure_Rotational_Spectra
  - title: "LibreTexts Physical Chemistry, 13.8 Rotational Spectra of Polyatomic Molecules"
    url: https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Physical_Chemistry_(LibreTexts)/13%3A_Molecular_Spectroscopy/13.08%3A_Rotational_Spectra_of_Polyatomic_Molecules
  - title: "NIST Atomic Weights and Isotopic Compositions"
    url: https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl
last_verified: "2026-10-17"
---

# 20.2 · Rotational spectra

A molecule with a permanent dipole absorbs microwave and far-infrared light as it spins faster. The lines are almost evenly spaced, and the spacing gives the moment of inertia and so the bond length, often to four or five significant figures. In [12.5](../module-12/lesson-05.md) you met the rigid rotor and its lines at $2B(J+1)$. This lesson adds what real spectra show: the slow drift of the lines caused by centrifugal stretching, the difference between the equilibrium and the averaged bond length, isotope shifts, and how polyatomic molecules rotate. You will fit 31 measured CO lines from the NIST Diatomic Spectral Database.

## Why it matters

Hydrogen, H₂, makes up most of the gas in the cold clouds where stars form, but it has no dipole and is invisible to radio telescopes. Astronomers map the clouds with carbon monoxide instead: its $J = 1 \leftarrow 0$ line at 115.271 GHz is the most observed molecular line in astronomy. Which line is strongest tells them the temperature of the gas; the ratio of the ¹²CO and ¹³CO lines tells them how much gas there is along the line of sight. All of that rests on the few equations in this lesson and on laboratory line positions like the ones you will fit.

## Core ideas

> [!NOTE]
> The theory is stable. The CO line frequencies are from the NIST Diatomic Spectral Database (SRD 114, last updated 2005), the CO constants from the NIST Chemistry WebBook and the isotope masses from NIST, all checked on 2026-10-17. Line positions measured since 2005 are more precise but agree with these to the digits used here.

### The rigid rotor and its lines

The rotational energy levels of a linear molecule, in wavenumbers, are $F(J) = BJ(J+1)$ with

$$B = \frac{h}{8\pi^2 c I}, \qquad I = \mu r^2$$

where $I$ is the moment of inertia, $\mu$ the reduced mass and $r$ the bond length. Microwave spectroscopists quote $B$ in MHz (multiply cm⁻¹ by 29 979.2458). With the rule $\Delta J = +1$ (lesson [20.1](lesson-01.md)), the absorption lines are

$$\tilde\nu(J+1 \leftarrow J) = 2B(J+1)$$

a ladder of lines spaced by $2B$, the first one at $2B$. For CO, $B \approx 1.92$ cm⁻¹, so the lines sit at 3.85, 7.69, 11.53 cm⁻¹ and so on.

### Centrifugal distortion

A real bond is a spring. As the molecule spins faster, the atoms are flung outwards, the bond stretches, $I$ grows and the levels drop a little. The correction is

$$F(J) = BJ(J+1) - DJ^2(J+1)^2, \qquad \tilde\nu = 2B(J+1) - 4D(J+1)^3$$

$D$ is the **centrifugal distortion constant**. It is tiny, but because it is multiplied by $(J+1)^3$ it shows at high $J$. For a diatomic it follows from the stiffness of the bond: $D \approx 4B^3/\omega_e^2$. For CO, $4 \times 1.9313^3 / 2169.8^2 = 6.12 \times 10^{-6}$ cm⁻¹, exactly the NIST value. A floppy bond stretches more and has a larger $D$.

To fit $B$ and $D$, divide the line formula by $(J+1)$:

$$\frac{\tilde\nu}{J+1} = 2B - 4D(J+1)^2$$

A plot of $\tilde\nu/(J+1)$ against $(J+1)^2$ is a straight line with intercept $2B$ and slope $-4D$.

### $B_0$ is not $B_e$

The molecule vibrates while it rotates, even in $v = 0$. Because the potential is anharmonic ([12.4](../module-12/lesson-04.md)), the average bond is longer than the bottom of the well, and the average of $1/r^2$ is smaller. So each vibrational level has its own rotational constant:

$$B_v = B_e - \alpha_e\left(v + \tfrac12\right)$$

A microwave spectrum of a cold or room-temperature gas measures $B_0$, not $B_e$. For CO, $B_0 = 1.93128 - 0.01750/2 = 1.92253$ cm⁻¹. The bond length you calculate from $B_0$ is $r_0 = 1.1309$ Å, a little longer than the equilibrium $r_e = 1.1283$ Å. Tables of "bond lengths" mix the two; for precise work, say which one you mean.

### Which lines are strongest

The population of level $J$ is proportional to $(2J+1)e^{-hcBJ(J+1)/k_BT}$, which peaks at

$$J_\text{max} \approx \sqrt{\frac{k_BT}{2hcB}} - \frac12$$

For CO at 298 K that is $J \approx 7$; at 10 K in an interstellar cloud it is $J \approx 1$, so only the first few lines are bright. The absorption intensity also depends on the photon frequency and on stimulated emission, which shift the strongest absorption line to somewhat higher $J$ than $J_\text{max}$, but the population peak is the main effect. Module 21 builds the rotational partition function from the same sum.

### Isotopes

Changing an isotope changes the masses but not the bonding, so the potential and $r_e$ stay the same, and $B$ scales as $1/\mu$. For ¹³C¹⁶O, $\mu$ rises from 6.8562 to 7.1724 u and $B$ falls by 4.4 %: the first line moves from 115.271 to 110.201 GHz. Natural carbon is about 1.1 % ¹³C, so every CO spectrum has weak ¹³CO lines beside the strong ones. HCl shows the same effect with ³⁵Cl and ³⁷Cl (lesson [20.3](lesson-03.md)).

### Polyatomic molecules

Molecules are classified by their three principal moments of inertia $I_a \le I_b \le I_c$:

| Type | Moments | Examples | Rotational spectrum |
|---|---|---|---|
| linear | $I_a = 0$, $I_b = I_c$ | OCS, HCN, HC≡CH | like a diatomic, $2B(J+1)$, if polar (HC≡CH and CO₂ are not) |
| symmetric top | two equal | NH₃, CH₃Cl, C₆H₆ | $\Delta J = \pm1$, $\Delta K = 0$: lines at $2B(J+1)$, split slightly by distortion, if polar |
| spherical top | all equal | CH₄, SF₆, CCl₄ | none: no permanent dipole |
| asymmetric top | all different | H₂O, CH₂O, most molecules | many irregular lines; fitted by computer |

$K$ is the quantum number for rotation about the symmetry axis of a symmetric top. One measured $B$ gives one moment of inertia, which is not enough to fix every bond length in a polyatomic molecule. Spectroscopists measure several isotopologues (for OCS: ¹⁶O¹²C³²S, ¹⁶O¹²C³⁴S, ¹⁸O¹²C³²S) and solve for all the bond lengths together.

## Worked example

### 1. The bond length of CO from one line

NIST lists the ¹²C¹⁶O $J = 1 \leftarrow 0$ line at 115 271.202 MHz.

1. Convert: $115\,271.202 / 29\,979.2458 = 3.84503$ cm⁻¹.
2. Ignoring $D$ (which changes the fifth digit only): $B_0 = 3.84503/2 = 1.92252$ cm⁻¹.
3. $I = h/(8\pi^2 c B_0) = 6.62607\times10^{-34} / (78.957 \times 2.99792\times10^{10} \times 1.92252) = 1.4561\times10^{-46}$ kg m².
4. $\mu = 12 \times 15.99491 / 27.99491 = 6.85621$ u $= 1.13851\times10^{-26}$ kg.
5. $r_0 = \sqrt{I/\mu} = \sqrt{1.4561\times10^{-46} / 1.13851\times10^{-26}} = 1.1309\times10^{-10}$ m $= 1.1309$ Å.

### 2. Centrifugal distortion at high J

The NIST line $J = 38 \leftarrow 37$ is at 4 340 138.124 MHz $= 144.772$ cm⁻¹. The rigid rotor predicts $2B_0 \times 38 = 2 \times 1.922526 \times 38 = 146.112$ cm⁻¹. The measured line is 1.34 cm⁻¹ lower. The distortion term gives $4D(J+1)^3 = 4 \times 6.11\times10^{-6} \times 38^3 = 1.341$ cm⁻¹, which explains the whole gap. A rigid-rotor fit to all 31 lines would be visibly bent; the fit with $D$ leaves residuals below 0.001 cm⁻¹.

## Hands-on

What you need: pencil, Python with the course packages and the [Module 20 lab folder](../../labs/module-20/). Record the fit on a [notebook page](../../templates/notebook-page.md). Time: about 40 minutes.

### Part A — pencil (15 min)

1. Predict the $J = 1 \leftarrow 0$ frequency of ¹³C¹⁶O from the ¹²C¹⁶O value of $B_0$ and the masses ¹³C = 13.003355 u, ¹⁶O = 15.994915 u. Compare with the NIST value 110 201.37 MHz.
2. Which of these have a pure rotational spectrum: OCS, CH₄, NH₃, CH₃Cl, SF₆, BF₃, H₂O, HC≡CH?
3. At what $J$ does the CO population peak in a cloud at 10 K? Why do radio astronomers observe mainly the first two CO lines there?

<details><summary>Answers</summary>

1. $\mu(^{13}\mathrm{CO}) = 13.003355 \times 15.994915 / 28.998270 = 7.17240$ u. $B_0 \approx 1.922526 \times 6.85621/7.17240 = 1.83777$ cm⁻¹, so $2B = 3.67554$ cm⁻¹ $= 110\,190$ MHz. NIST: 110 201 MHz. The 0.01 % difference is real: $\alpha_e$ also depends on the isotope, so $B_0$ does not scale exactly as $1/\mu$ (only $B_e$ does).
2. Yes: OCS (linear, polar), NH₃ and CH₃Cl (polar symmetric tops), H₂O (polar asymmetric top). No: CH₄ and SF₆ (spherical tops), BF₃ (planar, symmetric, no dipole), HC≡CH (linear, no dipole).
3. $J_\text{max} = \sqrt{10/(1.4388 \times 2 \times 1.9225)} - 0.5 = 0.84$, so $J = 1$ (with $J = 0$ close behind). Almost all molecules are in $J = 0, 1, 2$, so only the lines $1 \leftarrow 0$ and $2 \leftarrow 1$ are bright.

</details>

### Part B — Python: fit 31 NIST lines of CO (25 min)

1. Open `lesson02_rotor.py`. The file `co_rotational_lines.csv` holds the NIST SRD 114 line list for ¹²C¹⁶O and ¹³C¹⁶O in the ground vibrational state.
2. Complete `fit_B_D()` (the straight-line fit above) and `j_max()`.
3. Run it and open `runs/lesson02_co_lines.png`:

```bash
py lesson02_rotor.py
```

How you know it worked: $B_0 = 1.922526$ cm⁻¹ (57 635.9 MHz), $D = 6.11\times10^{-6}$ cm⁻¹, $r_0 = 1.13089$ Å, rigid-rotor misfit at $J+1 = 38$ about $-1.34$ cm⁻¹; ¹³CO $B_0 = 1.83797$ cm⁻¹ against 1.83777 predicted; $J_\text{max}$ 0.84 at 10 K and 6.84 at 298 K. The right-hand plot is a straight line.

<details><summary>Reference solution</summary>

```python
slope, intercept = np.polyfit(J_upper.astype(float)**2, nu / J_upper, 1)
return intercept / 2, -slope / 4
```

and `j_max` returns `math.sqrt(T / (HC_K * 2 * B)) - 0.5`. Full code: `lesson02_rotor_solution.py`. Your fitted $B_0$ agrees with the WebBook value $B_e - \alpha_e/2 = 1.922529$ cm⁻¹ to six figures, from completely independent data.

</details>

## Common mistakes

- Using $B_0$ from a spectrum to get $r_e$. A microwave spectrum gives $r_0$; you need $\alpha_e$ (from a vibrational band, lesson 20.3) to reach $B_e$ and $r_e$.
- Forgetting that line spacing is $2B$, not $B$. Levels are $BJ(J+1)$; lines are differences of levels.
- Mixing units: $B$ in MHz with $c$ in cm/s, or atomic masses in u used as kg. Convert once and keep track.
- Ignoring distortion at high $J$. A rigid-rotor fit of CO over $J$ up to 38 gives $B = 1.912$ instead of 1.923 cm⁻¹ and a curved residual plot.
- Expecting a rotational spectrum from every molecule. Spherical tops and any molecule without a permanent dipole (CO₂, BF₃, HC≡CH) have none.

## Key takeaways

- Lines at $2B(J+1) - 4D(J+1)^3$; plot $\tilde\nu/(J+1)$ against $(J+1)^2$ to get $B$ and $D$.
- $B = h/(8\pi^2 cI)$ gives the bond length; a microwave spectrum gives $B_0$ and $r_0$, slightly longer than $r_e$.
- $D \approx 4B^3/\omega_e^2$: stiffer bonds distort less.
- Isotopes change $\mu$ but not the potential: $B_e \propto 1/\mu$.
- Linear and symmetric tops show $2B(J+1)$ ladders if polar; spherical tops show nothing; asymmetric tops need a computer fit.

## Sources

- [NIST Diatomic Spectral Database (SRD 114)](https://physics.nist.gov/cgi-bin/MolSpec/diperiodic.pl) — 31 ¹²C¹⁶O and 9 ¹³C¹⁶O rotational lines in `co_rotational_lines.csv`, retrieved 2026-10-17.
- [NIST Chemistry WebBook, CO diatomic constants](https://webbook.nist.gov/cgi/cbook.cgi?ID=C630080&Mask=1000) — $B_e = 1.93128087$, $\alpha_e = 0.01750441$, $D_e = 6.12147\times10^{-6}$ cm⁻¹, $r_e = 1.128323$ Å, $\omega_e = 2169.81358$ cm⁻¹.
- [LibreTexts Physical Chemistry, 13.4 Unequal Spacings in Pure Rotational Spectra](https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Physical_Chemistry_(LibreTexts)/13%3A_Molecular_Spectroscopy/13.04%3A_Unequal_Spacings_in_Pure_Rotational_Spectra) — centrifugal distortion.
- [LibreTexts Physical Chemistry, 13.8 Rotational Spectra of Polyatomic Molecules](https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Physical_Chemistry_(LibreTexts)/13%3A_Molecular_Spectroscopy/13.08%3A_Rotational_Spectra_of_Polyatomic_Molecules) — linear, symmetric, spherical and asymmetric tops.
- [NIST Atomic Weights and Isotopic Compositions](https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl) — ¹³C, ¹⁶O and other isotope masses.
