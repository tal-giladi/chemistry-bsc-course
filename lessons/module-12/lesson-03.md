---
id: "12.3"
module: 12
minutes: 18
practice_minutes: 50
prerequisites: ["12.2", "02.1"]
objectives:
  - Compute the decay constant and decay length of a wavefunction inside a barrier.
  - Calculate the transmission through a rectangular barrier and explain its exponential dependence on width, height and mass.
  - Explain why a scanning tunnelling microscope resolves atoms and why hydrogen tunnels far more than deuterium.
  - Obtain a double-well tunnelling splitting numerically and compare NH3 with ND3.
volatility: concept
sources:
  - title: "OpenStax University Physics Volume 3, 7.7 Quantum Tunneling of Particles through Potential Barriers"
    url: https://phys.libretexts.org/Bookshelves/University_Physics/University_Physics_(OpenStax)/University_Physics_III_-_Optics_and_Modern_Physics_(OpenStax)/07%3A_Quantum_Mechanics/7.07%3A_Quantum_Tunneling_of_Particles_through_Potential_Barriers
  - title: "Flambaum and Kozlov (2007), Enhanced sensitivity to time-variation of mp/me in the inversion spectrum of ammonia, arXiv 0704.2301"
    url: https://arxiv.org/abs/0704.2301
  - title: "Nuckolls, Rueger and Lyons (1953), Microwave Absorption Spectrum of ND3, Phys. Rev. 89, 1101 (NIST archive)"
    url: https://tf.nist.gov/general/pdf/2840.pdf
  - title: "LibreTexts Physical Chemistry, chapter 4: Postulates and Principles of Quantum Mechanics"
    url: https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Physical_Chemistry_(LibreTexts)/04%3A_Postulates_and_Principles_of_Quantum_Mechanics
  - title: "MIT OpenCourseWare 5.61 Physical Chemistry (Field, Fall 2017)"
    url: https://ocw.mit.edu/courses/5-61-physical-chemistry-fall-2017/
last_verified: "2026-10-17"
---

# 12.3 · Tunnelling

A classical ball that does not have enough energy to climb a hill rolls back. A quantum particle sometimes appears on the other side. This is tunnelling, and it is not a curiosity: it lets microscopes image single atoms, makes hydrogen transfer reactions faster than they "should" be, and splits the energy levels of ammonia into the doublet that powered the first maser. This lesson shows why the wavefunction leaks through a barrier, how strongly that depends on width, height and mass, and how to compute a tunnelling splitting with the solver from [12.2](lesson-02.md).

## Why it matters

An enzyme moves a hydrogen atom from one carbon to another. Replace that hydrogen by deuterium and the reaction slows not by the factor of about 7 that zero-point energy explains (Module 22), but by 50 or more. That excess is a fingerprint of tunnelling, and enzymologists use it to prove the hydrogen goes through the barrier rather than over it. The same exponential sensitivity makes a scanning tunnelling microscope (STM) able to see a single atom: move the tip 0.1 nm and the current changes about eight times. If you can estimate a tunnelling probability you can tell when a mechanism needs quantum mechanics, a question that comes back in Modules 22 and 28.

## Core ideas

> [!NOTE]
> The theory is stable. Constants are CODATA 2022 (NIST, checked 2026-10-17). The ammonia inversion frequencies are measured values (NH3 23.79 GHz, ND3 1.59 GHz). The double-well potential in the lab is an illustrative model chosen to resemble ammonia, not a fitted potential.

### Inside a barrier the wave decays

Where the potential $V_0$ is higher than the particle's energy $E$, the Schrödinger equation of [12.2](lesson-02.md) becomes

$$\frac{d^2\psi}{dx^2} = \kappa^2\psi,\qquad \kappa = \frac{\sqrt{2m(V_0 - E)}}{\hbar}$$

Its solutions are not waves but exponentials, $e^{-\kappa x}$ and $e^{+\kappa x}$. Inside a thick wall only the decaying one survives. The distance over which $\psi$ drops by a factor $e$ is the decay length $1/\kappa$, and $|\psi|^2$ drops by $e^{-2\kappa x}$.

Tiny example: an electron 4.0 eV below the top of a barrier (about the work function of a metal). With $\hbar^2/2m_e = 0.0381$ eV nm², $\kappa = \sqrt{4.0/0.0381} = 10.25$ nm⁻¹, so the decay length is 98 pm, about the size of an atom.

### Transmission through a rectangular barrier

Send a particle of energy $E$ at a barrier of height $V_0 > E$ and width $d$. Matching $\psi$ and its slope at both edges gives the exact transmission probability

$$T = \left[1 + \frac{V_0^2\sinh^2(\kappa d)}{4E(V_0 - E)}\right]^{-1}$$

For a thick or high barrier ($\kappa d \gg 1$) this simplifies to

$$T \approx 16\,\frac{E}{V_0}\left(1 - \frac{E}{V_0}\right)e^{-2\kappa d}$$

The exponential dominates everything. Since $\kappa \propto \sqrt{m(V_0 - E)}$, the exponent grows linearly with the width, with the square root of the mass, and with the square root of the energy deficit. Doubling the width squares the (small) transmission; doubling the mass is like making the barrier 41 % wider.

### The scanning tunnelling microscope

An STM holds a sharp metal tip a few tenths of a nanometre above a conducting surface and applies a small voltage. Electrons tunnel through the vacuum gap; the current goes as $e^{-2\kappa d}$. With $\kappa = 10.25$ nm⁻¹, each extra 0.1 nm multiplies the current by $e^{-2.05} = 0.13$, so it falls about eight times. A feedback loop keeps the current constant while the tip scans, and the tip's height traces the surface atom by atom. Only the very last atom of the tip matters, because atoms further back are a few tenths of a nanometre further away and contribute almost nothing.

### Mass matters: hydrogen against deuterium

Electrons tunnel easily over nanometres. Nuclei are thousands of times heavier, so they tunnel only through narrow barriers, about 0.05 nm. Hydrogen is the lightest nucleus and the only one for which tunnelling is routine in chemistry. Deuterium has twice the mass, so its $\kappa$ is $\sqrt 2$ times larger, and its transmission is the hydrogen value raised to roughly the power 1.4. When $T_\mathrm{H}$ is small, that is a huge factor. This is why very large H/D kinetic isotope effects, together with rates that barely depend on temperature, are read as evidence for tunnelling.

### Double wells and tunnelling splitting

Ammonia is a pyramid. The nitrogen can sit above or below the plane of the three hydrogens, two equivalent shapes separated by a barrier (the planar shape) of about 24 kJ/mol. Model the "umbrella" coordinate as a symmetric double well. If the barrier were infinite, each well would have its own ground state, at the same energy. With a finite barrier the wavefunctions leak through and mix, giving two combinations:

- symmetric, $\psi_+ = (\psi_\text{left} + \psi_\text{right})/\sqrt2$, slightly lower;
- antisymmetric, $\psi_- = (\psi_\text{left} - \psi_\text{right})/\sqrt2$, slightly higher, with a node at the barrier.

The gap $\Delta$ is the tunnelling splitting. A molecule prepared in one well flips to the other and back at the frequency $\Delta/h$. For NH3 this is 23.79 GHz ($\Delta = 0.79$ cm⁻¹): the nitrogen tunnels through the plane about 24 billion times a second. The first maser (1954) ran on exactly this transition. For ND3 it drops to 1.59 GHz, 15 times smaller, because deuterium is heavier.

Try it: narrow the barrier, raise it, change the mass, and watch the splitting and the leaking wavefunction:

[Simulation: Quantum box — tunnelling through a barrier](../../simulations/quantum-box/index.html?preset=tunnel)

## Worked example

### 1. An electron through a thin insulating layer

An electron with $E = 1.00$ eV meets a barrier $V_0 = 2.00$ eV high and $d = 0.50$ nm wide. Find $T$.

1. $\kappa = \sqrt{(2.00 - 1.00)/0.0381} = 5.123$ nm⁻¹, so $\kappa d = 2.562$.
2. $\sinh(2.562) = (e^{2.562} - e^{-2.562})/2 = (12.96 - 0.077)/2 = 6.44$; squared, 41.5.
3. Prefactor $V_0^2/[4E(V_0 - E)] = 4.00/[4 \times 1.00 \times 1.00] = 1.00$.
4. $T = 1/(1 + 41.5) = 0.0235$.

So 2.4 % of the electrons get through. The thick-barrier formula gives $16 \times 0.5 \times 0.5 \times e^{-5.123} = 0.0238$, within 2 %. Make the barrier 1.0 nm wide and $T$ drops to $1.4\times10^{-4}$, about 165 times smaller.

### 2. Proton against deuteron

A hydrogen nucleus with 0.20 eV less energy than the top of a barrier $V_0 = 0.40$ eV crosses a width of 0.050 nm. The proton mass is $1836.15\,m_e$, the deuteron $3670.48\,m_e$.

1. Proton: $\kappa = \sqrt{0.20 \times 1836.15/0.0381} = 98.2$ nm⁻¹; $2\kappa d = 9.82$; $T \approx 16 \times 0.5 \times 0.5 \times e^{-9.82} = 4 \times 5.4\times10^{-5} = 2.2\times10^{-4}$.
2. Deuteron: $\kappa = 98.2\sqrt{2} = 138.8$ nm⁻¹ (the mass ratio is 1.999); $2\kappa d = 13.88$; $T \approx 4 \times 9.4\times10^{-7} = 3.7\times10^{-6}$.
3. Ratio $T_\mathrm{H}/T_\mathrm{D} \approx 58$.

An electron with the same numbers would pass almost freely ($T = 0.99$). The ratio of 58 is far above what a classical over-the-barrier picture gives, and it is the kind of number that signals tunnelling in kinetics.

## Hands-on

What you need: pencil and calculator; Python with the course packages and the [Module 12 lab folder](../../labs/module-12/) (`qm_solver.py` must be in the same folder). Time: about 50 minutes.

### Part A — pencil (15 min)

1. An STM tip sits 0.50 nm above a surface and the current is 1.0 nA. With $\kappa = 10.25$ nm⁻¹, what is the current at 0.60 nm and at 0.40 nm?
2. A muon is 207 times heavier than an electron. For the same barrier (1.00 eV deficit, 0.50 nm wide) roughly how does its $2\kappa d$ compare with the electron's? Is it likely to tunnel?
3. Why does the antisymmetric state of a double well lie above the symmetric one? Answer from the shape of the wavefunctions.

<details><summary>Answers to Part A</summary>

1. $I \propto e^{-2\kappa d}$; a change of 0.10 nm multiplies $I$ by $e^{\mp 2.05}$: 0.13 nA at 0.60 nm and 7.8 nA at 0.40 nm.
2. $\kappa \propto \sqrt m$, so $2\kappa d$ is $\sqrt{207} = 14.4$ times larger: $2 \times 5.12 \times 0.5 \times 14.4 = 74$, and $e^{-74} \approx 10^{-32}$. It will not tunnel through this barrier.
3. The antisymmetric state must pass through zero at the barrier centre, so it bends more (more curvature, more kinetic energy). The symmetric state stays non-zero under the barrier and is a little smoother.

</details>

### Part B — Python (35 min)

1. Open `lesson03_tunnel.py`. Fill in `kappa`, `transmission` (the exact formula above) and the double-well potential $V(x) = V_b[(x/a)^2 - 1]^2$ in `double_well_splitting`.
2. Run it from the lab folder:

```bash
py lesson03_tunnel.py
```

3. Look at `runs/lesson03_tunnel.png`: $T$ against width on a log scale, and the two lowest double-well states.
4. Write on a [notebook page](../../templates/notebook-page.md) the STM factor, the H/D ratio and both splittings, and compare the splittings with the measured ones.

How you know it worked:

- STM case: $\kappa = 10.25$ nm⁻¹, decay length 98 pm, a factor of about 8 per 0.1 nm.
- Electron, $E = 1$ eV, $V_0 = 2$ eV: $T = 0.777$, 0.169, 0.0235 and $1.42\times10^{-4}$ for widths 0.1, 0.3, 0.5 and 1.0 nm. On the log plot the curve becomes a straight line once the barrier is thicker than about 0.3 nm.
- H/D: $T_\mathrm{H} = 2.18\times10^{-4}$, $T_\mathrm{D} = 3.75\times10^{-6}$, ratio 58.
- Double well (barrier 2020 cm⁻¹, minima at ±0.40 Å, effective masses 2.487 u for NH3 and 4.22 u for ND3): splittings 0.87 cm⁻¹ (26 GHz) and 0.049 cm⁻¹ (1.5 GHz), ratio 18. Measured: 0.79 and 0.053 cm⁻¹, ratio 15.

<details><summary>Reference solution and what to notice</summary>

`kappa` returns `np.sqrt((V0 - E) * mass_me / HB2M_E_EV_NM2)`; `transmission` returns `1 / (1 + V0**2 * np.sinh(k * d)**2 / (4 * E * (V0 - E)))`; the potential is `Vb * ((x / a)**2 - 1)**2`. Full code: `lesson03_tunnel_solution.py`.

What to notice: a crude one-dimensional model with a guessed barrier gets the ammonia splitting within about 10 % and the isotope ratio within about 20 %. The splitting depends exponentially on the barrier, so small changes in $a$ or $V_b$ move it a lot; try $a = 0.38$ Å and the NH3 splitting rises to 1.4 cm⁻¹. The second pair of levels, about 980 cm⁻¹ up, is split by 49 cm⁻¹: excited states sit closer to the barrier top and tunnel much faster. Real NH3 shows the same pattern in its umbrella vibration.

</details>

Then open the simulation with the `tunnel` preset. Set a 1 eV electron on a 2 eV barrier and change the width from 0.3 to 0.5 nm: the transmitted fraction should drop about 7 times, as in the table above.

## Common mistakes

- Using $V_0$ instead of $V_0 - E$ in $\kappa$. The decay depends on how far below the top the particle is, not on the barrier height alone.
- Forgetting that $|\psi|^2$ decays as $e^{-2\kappa d}$, not $e^{-\kappa d}$. The factor 2 doubles the exponent and changes answers by orders of magnitude.
- Applying the thick-barrier formula to a thin barrier. When $\kappa d < 1$ the approximation fails; use the exact $\sinh$ form.
- Thinking a tunnelling particle "loses energy" inside the barrier. Energy is conserved; the transmitted particle has the same $E$ it came in with.
- Reading a large H/D isotope effect alone as proof of tunnelling. Zero-point energy differences already give factors up to about 7 at room temperature; tunnelling is suspected when the ratio is much larger and the rate barely changes with temperature.

## Key takeaways

- Under a barrier the wavefunction decays as $e^{-\kappa x}$ with $\kappa = \sqrt{2m(V_0 - E)}/\hbar$; electron decay lengths are about 0.1 nm.
- Transmission is roughly $e^{-2\kappa d}$: exponentially sensitive to width, to the square root of the mass and to the square root of the energy deficit.
- An STM's current changes about eight times per 0.1 nm, which is why it resolves single atoms.
- Hydrogen is the only nucleus that tunnels routinely; deuteration can slow a tunnelling step by factors of tens or more.
- A symmetric double well splits each level into a symmetric and an antisymmetric pair; NH3's 0.79 cm⁻¹ splitting is the nitrogen tunnelling through the plane.

## Sources

- [OpenStax University Physics Volume 3, 7.7 Quantum Tunneling](https://phys.libretexts.org/Bookshelves/University_Physics/University_Physics_(OpenStax)/University_Physics_III_-_Optics_and_Modern_Physics_(OpenStax)/07%3A_Quantum_Mechanics/7.07%3A_Quantum_Tunneling_of_Particles_through_Potential_Barriers) — rectangular barrier transmission, the STM.
- [Flambaum and Kozlov (2007), arXiv 0704.2301](https://arxiv.org/abs/0704.2301) — the NH3 inversion transition near 23.79 GHz (1.25 cm wavelength) as a tunnelling splitting.
- [Nuckolls, Rueger and Lyons (1953), Microwave Absorption Spectrum of ND3](https://tf.nist.gov/general/pdf/2840.pdf) — ND3 inversion lines from 1589 MHz.
- [LibreTexts Physical Chemistry, chapter 4](https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Physical_Chemistry_(LibreTexts)/04%3A_Postulates_and_Principles_of_Quantum_Mechanics) — postulates, superposition and probability used for the double well.
- [MIT OCW 5.61 Physical Chemistry (Field, Fall 2017)](https://ocw.mit.edu/courses/5-61-physical-chemistry-fall-2017/) — lectures on barriers, tunnelling and semi-classical methods.
