---
id: "14.3"
module: 14
minutes: 25
practice_minutes: 100
prerequisites: ["14.1", "03.2", "03.5"]
objectives:
  - Write the equations of motion of three coupled masses as K v = ω² M v and solve them for the normal-mode frequencies and shapes.
  - Predict how the mode frequencies change between a chain fixed to walls, a free chain, and a chain of coupled pendulums.
  - "Excite the three normal modes of a home pendulum chain, measure their periods and test the predicted 0 : 1 : 3 pattern."
  - Explain beating and energy transfer as a superposition of normal modes.
volatility: concept
sources:
  - title: "MIT OpenCourseWare 8.03SC Physics III: Vibrations and Waves"
    url: https://ocw.mit.edu/courses/8-03sc-physics-iii-vibrations-and-waves-fall-2016/
  - title: "SciPy v1.18 manual, scipy.linalg.eigh"
    url: https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.eigh.html
  - title: "NumPy manual, numpy.linalg.eigh"
    url: https://numpy.org/doc/stable/reference/generated/numpy.linalg.eigh.html
  - title: "LibreTexts, Normal Modes (Vibrational Spectroscopy supplemental module)"
    url: https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Supplemental_Modules_(Physical_and_Theoretical_Chemistry)/Spectroscopy/Vibrational_Spectroscopy/Vibrational_Modes/Normal_Modes
last_verified: "2026-10-17"
---

# 14.3 · Normal modes of three coupled masses

Join oscillators with springs and they stop moving independently. Push one and the motion spreads to the others, comes back, and wanders about in a pattern that looks complicated. Yet underneath it are a few simple motions, called normal modes, in which every part moves at the same frequency and in step. Any motion of the system is a mix of them. This lesson finds the normal modes of three coupled masses with an eigenvalue problem, then you build a chain of three pendulums joined by rubber bands, excite each mode by hand and check the prediction. Lesson 14.4 uses exactly the same mathematics for the three atoms of CO2.

## Why it matters

A molecule with $N$ atoms has $3N$ ways to move, and its infrared and Raman spectra show only the frequencies of its normal modes. Every vibrational band a chemist assigns, the C=O stretch of a ketone at 1715 cm⁻¹ or the O–H stretch of an alcohol near 3300 cm⁻¹, is a normal mode, and every quantum chemistry program that "calculates the IR spectrum" is solving the eigenproblem you meet here, only bigger. Normal modes also explain why energy put into one bond does not stay there: it is shared among modes, which is how a molecule spreads energy before it reacts. With three pendulums you can see all of this with your eyes.

## Core ideas

> [!NOTE]
> The mathematics is stable. The lab uses `scipy.linalg.eigh` from SciPy 1.18, checked 2026-10-17. The pendulum chain is a model: rubber bands are not perfect springs, so expect agreement within a few percent, not better.

### From coupled equations to an eigenproblem

Take three masses $m_1, m_2, m_3$ on a line, joined by springs. Each mass feels forces from its neighbours. Newton's law for all three at once is a matrix equation

$$M\ddot{\mathbf x} = -K\mathbf x$$

with $M$ the diagonal matrix of masses and $K$ the force-constant matrix: $K_{ij}$ is minus the force on mass $i$ when mass $j$ alone moves by one metre. Look for motions in which everything oscillates at one angular frequency $\omega$, $\mathbf x(t) = \mathbf v\cos\omega t$. Substituting gives

$$K\mathbf v = \omega^2 M\mathbf v$$

a generalised eigenvalue problem. Each eigenvalue is $\omega^2$ of one normal mode; its eigenvector $\mathbf v$ is the mode shape, the relative amplitudes of the three masses. Lesson [03.2](../module-03/lesson-02.md) did the same thing by mass-weighting; `scipy.linalg.eigh(K, M)` does it directly. Lesson [03.5](../module-03/lesson-05.md) used the same idea for a reaction network: find the eigenvectors, and the coupled problem falls apart into independent ones.

### Three masses between two walls

Three equal masses $m$, four equal springs $k$, the outer springs fixed to walls:

$$K = k\begin{pmatrix} 2 & -1 & 0 \\ -1 & 2 & -1 \\ 0 & -1 & 2 \end{pmatrix}$$

The eigenvalues are $\omega^2 = (2 - \sqrt2,\ 2,\ 2 + \sqrt2)\,k/m$, so

| Mode | $\omega/\sqrt{k/m}$ | Shape (mass 1, 2, 3) | What you see |
|---|---|---|---|
| 1 | 0.765 | (1, √2, 1) | all three move the same way, the middle one most |
| 2 | 1.414 | (1, 0, −1) | outer two move opposite, the middle one stands still |
| 3 | 1.848 | (1, −√2, 1) | neighbours move opposite, the middle one most |

The more the neighbours move against each other, the more the springs stretch, and the higher the frequency. The middle mass is still in mode 2 because of symmetry: the chain looks the same in a mirror, so every mode is either symmetric or antisymmetric, and an antisymmetric mode cannot move the centre. The matrix is $k$ times (2 × identity − the Hückel connection matrix of a three-carbon chain, the allyl system), so its eigenvalues are $2 - x$ with the Hückel values $x = \sqrt2, 0, -\sqrt2$ you would get by the method of 03.2. Same algebra, different physics.

### A free chain and a pendulum chain

Remove the walls and keep only the two springs between the masses. Now

$$K = k\begin{pmatrix} 1 & -1 & 0 \\ -1 & 2 & -1 \\ 0 & -1 & 1 \end{pmatrix},\qquad \omega^2 = (0,\ 1,\ 3)\,k/m$$

The zero mode is the whole chain sliding without stretching anything: a translation, not a vibration. A free molecule has such zero modes too.

Now hang each mass as a pendulum of length $L$ and join neighbours with weak springs (rubber bands). Gravity adds a restoring force $mg/L$ to every mass equally, which adds $g/L$ to every eigenvalue without changing the shapes:

$$\omega^2 = \frac{g}{L} + c\,(0,\ 1,\ 3),\qquad c = \frac{\kappa}{m}$$

with $\kappa$ the effective spring constant of a band. Shapes: $(1, 1, 1)$, $(1, 0, -1)$, $(1, -2, 1)$. The pattern 0 : 1 : 3 in the shifts of $\omega^2$ is the prediction you will test.

### Beats: energy moving between masses

Any motion is a sum of normal modes, each with its own frequency. If you pull only pendulum 1 and let go, you start all three modes at once:

$$x_1(t) = \tfrac13\cos\omega_1 t + \tfrac12\cos\omega_2 t + \tfrac16\cos\omega_3 t\quad(\text{times the starting pull})$$

At first the modes add up to motion of pendulum 1 only. Because their frequencies differ, they drift out of step, and within roughly half a beat period, $\pi/(\omega_2 - \omega_1)$, the swing has moved to the other pendulums. It then drifts back. The weaker the coupling, the closer the frequencies and the slower the transfer. This is the classical picture of energy flowing between bonds in a molecule.

[Simulation: Oscillators — three coupled masses between walls](../../simulations/oscillators/index.html?preset=coupled-three)

## Worked example

### 1. Three gliders between walls

Three 0.100 kg masses sit between two walls, joined by four springs of $k$ = 10.0 N/m. Then $\sqrt{k/m} = 10.0$ rad/s, and the three modes are at

- $\omega_1 = 0.765 \times 10.0 = 7.65$ rad/s, $f_1 = 1.22$ Hz;
- $\omega_2 = 1.414 \times 10.0 = 14.1$ rad/s, $f_2 = 2.25$ Hz;
- $\omega_3 = 1.848 \times 10.0 = 18.5$ rad/s, $f_3 = 2.94$ Hz.

A single glider on one spring of the same $k$ would be at 1.59 Hz. Coupling splits that one frequency into three, spread both below and above it. In a molecule, the same splitting is why two identical C=O groups in an anhydride give two carbonyl bands instead of one.

### 2. Testing the 0 : 1 : 3 pattern

Three 50 cm pendulums joined by rubber bands give, for ten swings of each pure mode, mean times 14.14, 13.63 and 12.70 s.

- Periods: 1.414, 1.363, 1.270 s. Angular frequencies $\omega = 2\pi/T$: 4.444, 4.610, 4.947 rad/s.
- $\omega^2$: 19.75, 21.25, 24.48 s⁻².
- Shifts from mode 1: $\omega_2^2 - \omega_1^2 = 1.51$ and $\omega_3^2 - \omega_1^2 = 4.73$ s⁻². Ratio 3.1, close to the predicted 3.
- So $c \approx 1.55$ s⁻² and $g/L \approx 19.75$ s⁻², which gives $L = 9.795/19.75 = 0.496$ m, within 1 % of the 0.500 m measured with the tape.

The coupling is weak ($c$ is 8 % of $g/L$), so the modes are close together. The slowest beat, between modes 1 and 2, has period $2\pi/(\omega_2 - \omega_1) = 38$ s, so after releasing one pendulum you wait about 18 s for its swing to pass along the chain.

## Hands-on

### Explore first: the simulation (15 min)

Set three equal masses between walls, start each mode from its shape, then start only the left mass and watch the energy wander.

Task: with $m$ = 0.100 kg and $k$ = 10.0 N/m, read the three mode frequencies. Target: 1.22, 2.25 and 2.94 Hz. Then double the middle mass and predict, before you look, which mode does not change (mode 2, because the middle mass does not move in it).

### Home experiment: three coupled pendulums (about 60 min)

> [!CAUTION]
> Use light bobs: three equal bags of rice or three small plastic bottles part-filled with water, about 150 g each, never glass. Lay a broom handle across the backs of two heavy chairs and tape it down so it cannot roll. Keep swings small (2–3 cm), and keep faces out of the swing path. Rubber bands under tension can snap; wear ordinary safety glasses. Nothing here uses mains power.

What you need: about 2 m of thin string, three equal bobs (weigh them; they should match within 2 %), two thin rubber bands, the broom handle and chairs, a tape measure, the phone stopwatch, your notebook and the [Module 14 lab folder](../../labs/module-14/).

Steps:

1. Tie three pendulums to the handle, 15 cm apart, each 50 cm from the knot to the centre of the bob. Make the lengths equal to within 2 mm; unequal lengths spoil the modes.
2. Tie a rubber band between strings 1 and 2, and another between strings 2 and 3, both about 15 cm below the handle. They should be slightly stretched when everything hangs still, so they stay taut while swinging.
3. All swings go along the line of the pendulums (in the plane of the three strings).
4. Mode 1: hold a ruler against all three bobs, pull them 2 cm sideways together and release. Count 10 swings; repeat three times.
5. Mode 2: pull bob 1 left and bob 3 right by 2 cm each, hold bob 2 still, release together. Time 10 swings three times.
6. Mode 3: pull bobs 1 and 3 left by 2 cm and bob 2 right by 4 cm, release together. Time 10 swings three times. This one is hardest; if it turns into a mess, try again.
7. Finally, pull only bob 1 and release. Note roughly when bob 1 is almost still and the others swing.
8. Type the data as `mode,trial,t10_s`, as in `coupled_pendulums_example.csv`. Fill in the two TODO functions in `lesson03_modes.py` and run:

```bash
py lesson03_modes.py
py lesson03_modes.py my_pendulums.csv
```

How you know it worked: on the example data the script prints the three wall-chain modes 0.7654, 1.4142 and 1.8478 times $\sqrt{k/m}$, the free chain 0, 1 and 1.7321, then for the pendulums $g/L$ = 19.72 s⁻² and $c$ = 1.59 s⁻² with residuals under 0.05 s⁻², and a first energy transfer near 18 s. With your own pendulums, the three periods should be clearly different (mode 3 shortest), the residuals should be small compared with $c$, and the transfer time you saw in step 7 should be within a few seconds of the prediction.

<details><summary>Reference solution and troubleshooting</summary>

`normal_modes`: `w2, V = eigh(K, np.diag(masses))`, then $\omega = \sqrt{\max(w^2, 0)}$; the clip removes tiny negative round-off for the zero mode. `fit_pendulum_modes`: a straight line $\omega^2 = \omega_0^2 + c\lambda$ with $\lambda$ = 0, 1, 3, solved with `np.linalg.lstsq`. Full code: `lesson03_modes_solution.py`.

If modes 1 and 2 have nearly the same period, the bands are too slack or too low on the strings; the coupling seen by the bob scales as the square of the band's height on the string relative to $L$, so move the bands lower. If the mode-3 period scatters a lot, your release was not quite in the mode shape and some mode 1 or 2 mixed in; the beat in the amplitude shows this. If the residuals are large, check that the three lengths are equal: a pendulum 1 cm longer than the others is a different oscillator, and the symmetric shapes no longer apply.

Write it up with the [lab report template](../../templates/lab-report.md): a sketch of the set-up, the table of periods, $\omega^2$ against $\lambda$ with the fitted line, $g/L$ against your tape-measured length, and one sentence on how well the 0 : 1 : 3 pattern held.

</details>

## Common mistakes

- Solving $K\mathbf v = \omega^2\mathbf v$ and forgetting $M$. With unequal masses the frequencies come out wrong; pass $M$ to `eigh` or mass-weight first.
- Reading eigenvalues as frequencies. They are $\omega^2$; take the square root, and divide by $2\pi$ for hertz.
- Expecting a mode to appear by pulling one mass. Pulling one mass starts every mode that moves it; to see a pure mode, release in its shape.
- Treating the zero mode as an error. A free chain or a free molecule always has one: it is translation.
- Unequal pendulum lengths. Two pendulums 2 % different in length behave as two different oscillators and barely exchange energy.

## Key takeaways

- Coupled oscillators obey $M\ddot{\mathbf x} = -K\mathbf x$; normal modes solve $K\mathbf v = \omega^2 M\mathbf v$.
- Each normal mode moves all masses at one frequency, in a fixed shape; any motion is a sum of modes.
- Three masses between walls: $\omega/\sqrt{k/m}$ = 0.765, 1.414, 1.848. Free chain: 0, 1, √3. Pendulum chain: $\omega^2 = g/L + c(0, 1, 3)$.
- Symmetry sorts modes into symmetric and antisymmetric ones; antisymmetric modes leave the centre still.
- Releasing one oscillator makes energy move along the chain at the beat frequency between modes.

## Sources

- [MIT OCW 8.03SC Vibrations and Waves](https://ocw.mit.edu/courses/8-03sc-physics-iii-vibrations-and-waves-fall-2016/) — coupled oscillators and normal modes in depth.
- [SciPy v1.18 manual, scipy.linalg.eigh](https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.eigh.html) — the generalised symmetric eigensolver used in the lab.
- [NumPy manual, numpy.linalg.eigh](https://numpy.org/doc/stable/reference/generated/numpy.linalg.eigh.html) — the ordinary eigensolver from lesson 03.2.
- [LibreTexts, Normal Modes](https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Supplemental_Modules_(Physical_and_Theoretical_Chemistry)/Spectroscopy/Vibrational_Spectroscopy/Vibrational_Modes/Normal_Modes) — normal modes of molecules and the 3N − 6 rule.
