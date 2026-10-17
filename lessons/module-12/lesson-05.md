---
id: "12.5"
module: 12
minutes: 22
practice_minutes: 50
prerequisites: ["12.4", "07.2"]
objectives:
  - Compute rigid-rotor levels, rotational line positions and a bond length from a rotational constant.
  - Predict the most populated rotational level at a given temperature from degeneracy and the Boltzmann factor.
  - State the hydrogen-atom energies and the allowed quantum numbers n, l and m, and count radial and angular nodes.
  - Solve the hydrogen radial equation numerically in atomic units and check the energies, nodes and mean radius.
volatility: concept
sources:
  - title: "NIST Chemistry WebBook: hydrogen chloride, constants of diatomic molecules"
    url: https://webbook.nist.gov/cgi/cbook.cgi?ID=C7647010&Mask=1000
  - title: "LibreTexts Physical Chemistry, chapter 5: The Harmonic Oscillator and the Rigid Rotor"
    url: https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Physical_Chemistry_(LibreTexts)/05%3A_The_Harmonic_Oscillator_and_the_Rigid_Rotor
  - title: "LibreTexts Physical Chemistry, chapter 6: The Hydrogen Atom"
    url: https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Physical_Chemistry_(LibreTexts)/06%3A_The_Hydrogen_Atom
  - title: "NIST CODATA 2022: Bohr radius"
    url: https://physics.nist.gov/cgi-bin/cuu/Value?bohrrada0
  - title: "NIST CODATA 2022: Hartree energy in eV"
    url: https://physics.nist.gov/cgi-bin/cuu/Value?hrev
last_verified: "2026-10-17"
---

# 12.5 · Rotors, angular momentum and the hydrogen atom

A molecule tumbling in a gas and an electron moving around a nucleus have one thing in common: angular momentum, and in quantum mechanics angular momentum comes in fixed amounts. This lesson starts with the rigid rotor, which gives the microwave spectra of molecules and their bond lengths, then uses the same angular momentum to build the hydrogen atom. The quantum numbers n, l and m that you used to fill shells in [07.2](../module-07/lesson-02.md) come out of the mathematics here, and you check them with the numerical solver.

## Why it matters

Radio astronomers have identified hundreds of molecules in interstellar space, almost all from their rotational lines, and the bond lengths in reference tables often come from the same spectra. Closer to home, every orbital diagram in chemistry, every "2p" and "3d", is a hydrogen-atom solution borrowed for bigger atoms. When you see why a p orbital has a nodal plane, or why a 3s electron spends time close to the nucleus, you can reason about periodic trends (Module 7), crystal-field splitting (Module 18) and NMR coupling (Module 17) instead of memorising them.

## Core ideas

> [!NOTE]
> The theory is stable. HCl constants are NIST WebBook values, and the Bohr radius and hartree are CODATA 2022 values, all checked 2026-10-17. The lab uses `qm_solver.py` with numpy 2.5 and scipy 1.18.

### The rigid rotor

Model a diatomic molecule as two masses at a fixed distance $r$ rotating about their centre of mass. Its moment of inertia is $I = \mu r^2$ (reduced mass again). Solving the Schrödinger equation for free rotation gives

$$E_J = \frac{\hbar^2}{2I}J(J+1),\qquad J = 0, 1, 2, \dots$$

Each level has $2J + 1$ states, labelled by $M_J = -J, \dots, +J$, which differ only in the orientation of the rotation axis. Spectroscopists write the energy in wavenumbers with the rotational constant $B$:

$$F(J) = BJ(J+1),\qquad B = \frac{h}{8\pi^2 cI}\ \ (\text{cm}^{-1},\ c\ \text{in cm/s})$$

Tiny example: H³⁵Cl has $B_e = 10.593$ cm⁻¹. The first excited level, $J = 1$, sits $2B = 21.19$ cm⁻¹ above $J = 0$, a hundred times below the vibrational gap of [12.4](lesson-04.md).

### Rotational spectra

A molecule absorbs a microwave or far-infrared photon and changes its rotation only if it has a permanent dipole moment (HCl yes, N₂ and O₂ no) and only for $\Delta J = \pm 1$. Absorption lines lie at

$$\tilde\nu = F(J+1) - F(J) = 2B(J + 1)$$

so the spectrum is a ladder of nearly equally spaced lines, $2B$ apart. Measure the spacing, get $B$, then $I$, then $r$: this is how many bond lengths are known to five or six digits. Real molecules stretch slightly when they spin faster (centrifugal distortion, a small constant $D$ in $F(J) = BJ(J+1) - DJ^2(J+1)^2$), and $B$ depends a little on the vibrational level: $B_v = B_e - \alpha_e(v + \tfrac12)$.

### Which levels are filled?

Rotational gaps are smaller than thermal energy ($k_BT/hc = 207$ cm⁻¹ at 298 K), so many levels are occupied. The fraction in level $J$ is proportional to its degeneracy times its Boltzmann factor:

$$N_J \propto (2J + 1)\,e^{-BJ(J+1)\,hc/k_BT}$$

The first factor grows with $J$, the second shrinks, so the population peaks at $J_\text{max} \approx \sqrt{k_BT/2hcB} - \tfrac12$. This decides which lines in a spectrum are strongest; Module 21 develops it into the rotational partition function.

[Simulation: Quantum box — rigid rotor levels and populations](../../simulations/quantum-box/index.html?preset=rotor)

### Angular momentum is quantised

The rotor's wavefunctions are the spherical harmonics $Y_{\ell m}(\theta, \phi)$, functions of the two angles on a sphere. They are the same functions for any rotation, molecular or electronic. They fix two quantities:

- the size of the angular momentum, $|L| = \hbar\sqrt{\ell(\ell+1)}$, with $\ell = 0, 1, 2, \dots$;
- its component along a chosen axis, $L_z = m\hbar$, with $m = -\ell, \dots, +\ell$.

Since $\sqrt{\ell(\ell+1)}$ is always larger than $|m|$, the angular momentum vector never points exactly along the axis. $Y_{\ell m}$ has $\ell$ angular nodes (nodal planes or cones). For $\ell = 0$ it is a constant, the round s shape; for $\ell = 1$ it has one nodal plane, the p shape; for $\ell = 2$ two, the d shapes.

### The hydrogen atom

For one electron around a proton the potential is the Coulomb attraction $V(r) = -e^2/(4\pi\varepsilon_0 r)$ from Module 4. Because $V$ depends only on $r$, the wavefunction separates into a radial part and a spherical harmonic:

$$\psi_{n\ell m}(r, \theta, \phi) = R_{n\ell}(r)\,Y_{\ell m}(\theta, \phi)$$

The allowed energies depend only on $n$:

$$E_n = -\frac{\mu e^4}{8\varepsilon_0^2h^2}\frac{1}{n^2} = -\frac{13.598\ \text{eV}}{n^2}$$

which is the Rydberg result of [12.1](lesson-01.md), now derived rather than guessed. The quantum numbers and their rules:

| Quantum number | Values | Decides |
|---|---|---|
| $n$ (principal) | 1, 2, 3, ... | energy, size |
| $\ell$ (angular momentum) | 0 to $n - 1$ | shape (s, p, d, f) |
| $m$ (magnetic) | $-\ell$ to $+\ell$ | orientation |

Each $n$ level holds $n^2$ orbitals, all with the same energy in hydrogen. Each orbital has $n - 1$ nodes in total: $\ell$ angular and $n - \ell - 1$ radial (spheres where $R = 0$).

### The radial equation is a one-dimensional problem

Write $u(r) = rR(r)$. Then $u$ obeys a one-dimensional Schrödinger equation with an effective potential

$$V_\text{eff}(r) = -\frac{e^2}{4\pi\varepsilon_0 r} + \frac{\ell(\ell+1)\hbar^2}{2\mu r^2}$$

The second term, the centrifugal barrier, pushes electrons with angular momentum away from the nucleus. That is why s electrons get closer to the nucleus than p or d electrons of the same shell, the root of the penetration and shielding you met in [07.2](../module-07/lesson-02.md). The radial probability $P(r) = u^2 = r^2R^2$ gives the chance of finding the electron at distance $r$; for 1s it peaks at the Bohr radius $a_0 = 52.9$ pm and its mean is $1.5a_0$.

Atomic units make this easy: set $\hbar = m_e = e = 4\pi\varepsilon_0 = 1$. Lengths come out in bohr ($a_0$), energies in hartree ($E_h = 27.211$ eV), and the radial equation becomes $-\tfrac12u'' + [\ell(\ell+1)/2r^2 - 1/r]\,u = Eu$, ready for the finite-difference solver with $E_n = -1/(2n^2)$ hartree.

## Worked example

### 1. The bond length of HCl from its rotational constant

$B_e = 10.593416$ cm⁻¹ and $\mu = 0.979593$ u.

1. $I = h/(8\pi^2 c B) = 6.62607\times10^{-34}/(78.957 \times 2.99792\times10^{10} \times 10.5934) = 2.6425\times10^{-47}$ kg m².
2. $\mu = 0.979593 \times 1.66054\times10^{-27} = 1.62665\times10^{-27}$ kg.
3. $r = \sqrt{I/\mu} = \sqrt{1.6245\times10^{-20}}$ m $= 1.2746\times10^{-10}$ m $= 1.2746$ Å.

NIST lists $r_e = 1.274552$ Å. With $B_0 = B_e - \alpha_e/2 = 10.4398$ cm⁻¹ for the ground vibrational level you get $r_0 = 1.2839$ Å, longer, because the anharmonic vibration of 12.4 stretches the average bond.

### 2. The strongest rotational line of HCl at room temperature

With $B_0 = 10.44$ cm⁻¹ and $k_BT/hc = 207.2$ cm⁻¹: $J_\text{max} \approx \sqrt{207.2/(2 \times 10.44)} - 0.5 = 3.15 - 0.5 = 2.65$, so the peak is at $J = 2$ or $J = 3$. Decide by computing $(2J + 1)e^{-BJ(J+1)/207.2}$ directly, with $B/207.2 = 0.0504$:

- $J = 2$: $5e^{-6 \times 0.0504} = 5 \times 0.739 = 3.70$
- $J = 3$: $7e^{-12 \times 0.0504} = 7 \times 0.546 = 3.82$
- $J = 4$: $9e^{-20 \times 0.0504} = 9 \times 0.365 = 3.29$

$J = 3$ is the most populated level, narrowly. The pure-rotation absorption from $J = 3$ lies at $2B_0 \times 4 = 83.5$ cm⁻¹ (83.4 cm⁻¹ with centrifugal distortion), in the far infrared. (Line intensities also depend on the photon frequency and on the population of the upper level, so the strongest line is not exactly the one from $J_\text{max}$; Module 20 treats this.)

## Hands-on

What you need: pencil and calculator; Python with the course packages and the [Module 12 lab folder](../../labs/module-12/). Time: about 50 minutes.

### Part A — pencil (15 min)

1. ¹²C¹⁶O has $B = 1.92$ cm⁻¹. At what wavenumber is its $J = 0 \to 1$ line, and what is the frequency in GHz (1 cm⁻¹ = 29.98 GHz)?
2. List all allowed $(\ell, m)$ pairs for $n = 3$ and confirm that there are $n^2$ orbitals.
3. How many radial and how many angular nodes do 3s, 3p and 3d have?
4. The 2s radial function is proportional to $(2 - r/a_0)e^{-r/2a_0}$. Where is its radial node, in pm?

<details><summary>Answers to Part A</summary>

1. $2B = 3.84$ cm⁻¹, 115 GHz. This CO line is the workhorse of radio astronomy for mapping molecular clouds.
2. $\ell = 0$: $m = 0$; $\ell = 1$: $m = -1, 0, 1$; $\ell = 2$: $m = -2 \dots 2$. That is 1 + 3 + 5 = 9 = $3^2$.
3. Total nodes $n - 1 = 2$. 3s: 2 radial, 0 angular. 3p: 1 radial, 1 angular. 3d: 0 radial, 2 angular.
4. $r = 2a_0 = 105.8$ pm.

</details>

### Part B — Python: HCl rotor and the hydrogen atom (35 min)

1. Open `lesson05_rotor_h.py`. Fill in `bond_length`, `rotation_lines` and the radial potential in `hydrogen_radial`.
2. Run it from the lab folder:

```bash
py lesson05_rotor_h.py
```

3. Look at `runs/lesson05_rotor_h.png`: the HCl rotational populations at 298 K and the radial probability $u^2$ of six hydrogen orbitals.
4. Record the bond lengths, the first lines and the hydrogen table on a [notebook page](../../templates/notebook-page.md).

How you know it worked:

- $r_e = 1.2746$ Å from $B_e$; $r_0 = 1.2839$ Å from $B_0 = 10.4398$ cm⁻¹.
- Lines at 20.88, 41.74, 62.58, 83.38, 104.13 cm⁻¹, spaced slightly less than $2B$ because of centrifugal distortion. The most populated level is $J = 3$.
- Hydrogen: $-0.49999$, $-0.12500$, $-0.05556$ hartree for $n = 1, 2, 3$, the same for every allowed $\ell$; radial nodes $n - \ell - 1$; $\langle r\rangle_{1s} = 1.5000$ bohr (79.4 pm) and the 1s radial maximum at 1.000 bohr.
- With the reduced-mass correction the ionisation energy is 13.598 eV, the value you fitted from the Balmer lines in 12.1.

<details><summary>Reference solution and what to notice</summary>

`bond_length`: `I = H / (8 * np.pi**2 * C_LIGHT * 100 * B_cm)`, then `np.sqrt(I / (mu_u * M_U)) * 1e10`. `rotation_lines`: `2 * B * (J + 1) - 4 * D * (J + 1)**3`. Radial potential: `l * (l + 1) / (2 * r**2) - 1.0 / r`. Full code: `lesson05_rotor_h_solution.py`.

What to notice: the 2s and 2p energies agree to six digits. This "accidental" degeneracy is special to the pure $1/r$ potential. In many-electron atoms the other electrons screen the nucleus, the potential is no longer $1/r$, and 2s drops below 2p (12.6). On the plot, the 3s curve has small inner peaks near the nucleus that 3d lacks: that is penetration, drawn from your own numbers.

</details>

Then open the simulation with the `rotor` preset, set $B = 10.4$ cm⁻¹ and $T = 298$ K, and check that the population bar chart peaks at $J = 3$. Cool to 50 K and find the new peak.

## Common mistakes

- Using the atomic mass instead of the reduced mass in $I = \mu r^2$.
- Forgetting that $c$ must be in cm/s when $B$ is in cm⁻¹ (a factor of 100 error in $I$ and 10 in $r$).
- Writing line positions as $BJ(J+1)$. Those are level energies; the lines are differences, $2B(J+1)$.
- Ignoring degeneracy when finding populations. Without the $2J + 1$ factor, $J = 0$ would always be the most populated level.
- Allowing $\ell = n$. The rule is $\ell \le n - 1$: there is no 1p or 2d orbital.
- Reading the 1s radial maximum at $a_0$ as "the electron orbits at $a_0$". It is the most likely distance, not a path; the mean distance is $1.5a_0$.

## Key takeaways

- Rigid rotor: $F(J) = BJ(J+1)$ with $B = h/8\pi^2cI$, degeneracy $2J + 1$, absorption lines at $2B(J+1)$; the spacing gives the bond length.
- Many rotational levels are filled at room temperature; the peak is near $J \approx \sqrt{k_BT/2hcB} - \tfrac12$.
- Angular momentum is quantised: $|L| = \hbar\sqrt{\ell(\ell+1)}$, $L_z = m\hbar$; $Y_{\ell m}$ has $\ell$ angular nodes.
- Hydrogen: $E_n = -13.598\ \text{eV}/n^2$, $\ell = 0 \dots n - 1$, $m = -\ell \dots \ell$, $n^2$ orbitals per shell, $n - \ell - 1$ radial nodes.
- The radial equation is a 1D problem with a centrifugal barrier, which keeps high-$\ell$ electrons away from the nucleus.

## Sources

- [NIST Chemistry WebBook: HCl constants](https://webbook.nist.gov/cgi/cbook.cgi?ID=C7647010&Mask=1000) — $B_e = 10.593416$, $\alpha_e = 0.307181$, $D_e = 5.3194\times10^{-4}$ cm⁻¹, $r_e = 1.274552$ Å.
- [LibreTexts Physical Chemistry, chapter 5](https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Physical_Chemistry_(LibreTexts)/05%3A_The_Harmonic_Oscillator_and_the_Rigid_Rotor) — rigid rotor, spherical harmonics, rotational spectra.
- [LibreTexts Physical Chemistry, chapter 6](https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Physical_Chemistry_(LibreTexts)/06%3A_The_Hydrogen_Atom) — hydrogen energies, quantum numbers, radial functions and nodes.
- [NIST CODATA 2022: Bohr radius](https://physics.nist.gov/cgi-bin/cuu/Value?bohrrada0) — $a_0 = 5.291\,772\,105\,44\times10^{-11}$ m.
- [NIST CODATA 2022: Hartree energy in eV](https://physics.nist.gov/cgi-bin/cuu/Value?hrev) — $E_h = 27.211\,386\,245\,981$ eV.
