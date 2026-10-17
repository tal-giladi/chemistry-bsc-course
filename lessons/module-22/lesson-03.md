---
id: "22.3"
module: 22
minutes: 24
practice_minutes: 50
prerequisites: ["22.1", "03.5"]
objectives:
  - Propose a mechanism of elementary steps that adds up to the overall reaction and derive its rate law with the rate-determining-step, pre-equilibrium or steady-state approximation.
  - State when the steady-state approximation holds and measure its error against an exact numerical solution.
  - Use the Lindemann mechanism to explain why a unimolecular decomposition changes from first to second order as the pressure falls, with real N2O5 data.
  - Explain a negative activation energy and a fractional order as signatures of a pre-equilibrium and a chain mechanism.
volatility: concept
sources:
  - title: "LibreTexts Physical Chemistry, 29.4 The Steady-State Approximation"
    url: https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Physical_Chemistry_(LibreTexts)/29%3A_Chemical_Kinetics_II-_Reaction_Mechanisms/29.04%3A_The_Steady-State_Approximation
  - title: "LibreTexts Physical Chemistry, 29.6 The Lindemann Mechanism"
    url: https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Physical_Chemistry_(LibreTexts)/29%3A_Chemical_Kinetics_II-_Reaction_Mechanisms/29.06%3A_The_Lindemann_Mechanism
  - title: "LibreTexts Physical Chemistry, 29.7 Some Reaction Mechanisms Involve Chain Reactions"
    url: https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Physical_Chemistry_(LibreTexts)/29%3A_Chemical_Kinetics_II-_Reaction_Mechanisms/29.07%3A_Some_Reaction_Mechanisms_Involve_Chain_Reactions
  - title: "NIST Chemical Kinetics Database (SRD 17), N2O5 → NO2 + NO3 and 2NO + O2 → 2NO2"
    url: https://kinetics.nist.gov/kinetics/
  - title: "OpenStax Chemistry 2e, 12.6 Reaction Mechanisms"
    url: https://openstax.org/books/chemistry-2e/pages/12-6-reaction-mechanisms
last_verified: "2026-10-17"
---

# 22.3 · Mechanisms and the steady-state approximation

A balanced equation says what goes in and what comes out. A mechanism says what actually happens: a sequence of elementary steps, each one a single collision or a single molecule falling apart, passing through short-lived intermediates. You cannot watch most mechanisms directly, but you can predict the rate law each one implies and compare it with experiment. This lesson gives the three approximations that make those predictions possible, tests the most important one numerically, and applies them to three real gas-phase reactions with evaluated data: the pressure dependence of N₂O₅ decomposition, the oxidation of NO that slows down when you heat it, and the chain reaction of hydrogen with bromine.

## Why it matters

Nitric oxide from engines and power plants turns into brown NO₂ in air by $\mathrm{2NO + O_2 \to 2NO_2}$, and the rate is proportional to $[\mathrm{NO}]^2$. In a flue gas with 1 % NO half of it reacts in tens of seconds; at the 100 parts per billion of a polluted street it would take weeks, so in the open air ozone does the job instead. The square comes from the mechanism, and so does a stranger fact: this reaction gets *slower* as the temperature rises. Engineers designing nitric acid plants and atmospheric chemists predicting smog both rely on rate laws that only make sense once the mechanism is known.

## Core ideas

> [!NOTE]
> The approximations are stable textbook theory. The N₂O₅ low- and high-pressure limits are the IUPAC evaluation (1997) and the 2NO + O₂ rate constant the IUPAC evaluation (2004), both as listed in the NIST Chemical Kinetics Database (SRD 17, Data Version 2026), checked on 2026-10-17.

### What a mechanism must do

A proposed mechanism must (1) add up to the overall equation, with the intermediates cancelling; (2) use only elementary steps, whose rate laws follow from their molecularity (lesson [22.1](lesson-01.md)); and (3) reproduce the measured rate law. Agreement does not prove a mechanism: several mechanisms can give the same rate law. Kineticists then look for the intermediates directly (by spectroscopy), use isotopes, or test predictions at other temperatures and pressures.

### The rate-determining step

If one step is much slower than all the others, and the steps after it are fast, the overall rate equals the rate of that step. It is the **rate-determining step** (RDS). Steps before the RDS matter only through how much of the RDS's reactant they supply. A car ferry is the classic picture: however fast the motorway, the traffic crossing the river is set by the ferry.

### Pre-equilibrium

Sometimes a fast reversible step comes before the slow one. Then the first step stays near equilibrium and you can use its equilibrium constant. For the oxidation of NO:

$$\mathrm{2NO \rightleftharpoons N_2O_2} \quad (K_1, \text{ fast}), \qquad \mathrm{N_2O_2 + O_2 \to 2NO_2} \quad (k_2, \text{ slow})$$

$$v = k_2[\mathrm{N_2O_2}][\mathrm{O_2}] = k_2K_1[\mathrm{NO}]^2[\mathrm{O_2}]$$

The observed constant is $k = k_2K_1$. Taking logarithms and differentiating with respect to $1/T$ (lesson [22.4](lesson-04.md)) gives an apparent activation energy $E_a = E_{a,2} + \Delta H_1^\circ$. Forming the weakly bound dimer N₂O₂ releases heat, $\Delta H_1^\circ < 0$, and if it is larger than $E_{a,2}$ the overall activation energy is negative. The IUPAC evaluation gives $E_a = -4.4$ kJ/mol: $k$ falls from $2.35\times10^{-38}$ cm⁶ molecule⁻² s⁻¹ at 270 K to $7.98\times10^{-39}$ at 600 K. Heating shifts the pre-equilibrium back towards NO faster than it speeds up step 2.

### The steady-state approximation

A reactive intermediate I is formed slowly and destroyed quickly, so it never builds up. After a short start-up, its concentration is small and nearly constant, and you may set

$$\frac{d[\mathrm{I}]}{dt} \approx 0$$

This is the **steady-state approximation** (SSA). It turns differential equations for intermediates into algebra. For $\mathrm{A} \xrightarrow{k_1} \mathrm{I} \xrightarrow{k_2} \mathrm{P}$ you met it in [03.5](../module-03/lesson-05.md): $[\mathrm{I}] = k_1[\mathrm{A}]/k_2$ and $d[\mathrm{P}]/dt = k_1[\mathrm{A}]$. It holds when $k_2 \gg k_1$, and only after an induction period of a few times $1/k_2$. In the lab you will measure how wrong it gets: with $k_2 = 20k_1$ the product curve is off by at most 4 % of $[\mathrm{A}]_0$, almost all of it at the very start; with $k_2 = k_1$ it is off by 37 %.

Watch the intermediate rise and settle when $k_2$ is large, and fail to settle when it is not:

[Simulation: Kinetics — consecutive reactions A → B → C](../../simulations/kinetics/index.html?preset=consecutive)

### Lindemann: how one molecule gets the energy to react

A molecule that falls apart on its own, such as $\mathrm{N_2O_5 \to NO_2 + NO_3}$, needs energy first, and in a gas it gets it from collisions with any other molecule M. Lindemann (1922) wrote:

$$\mathrm{A + M \underset{k_{-a}}{\overset{k_a}{\rightleftharpoons}} A^* + M}, \qquad \mathrm{A^* \xrightarrow{k_b} P}$$

A* is an energised molecule. The SSA on A* gives

$$v = k_\text{uni}[\mathrm{A}], \qquad k_\text{uni} = \frac{k_ak_b[\mathrm{M}]}{k_{-a}[\mathrm{M}] + k_b}$$

At high pressure, collisions remove energy faster than A* reacts ($k_{-a}[\mathrm{M}] \gg k_b$), so $k_\text{uni} \to k_\infty = k_ak_b/k_{-a}$, independent of pressure: first order. At low pressure every energising collision leads to reaction, and $k_\text{uni} \to k_0[\mathrm{M}]$ with $k_0 = k_a$: second order overall. In terms of the two limits,

$$k_\text{uni} = \frac{k_0[\mathrm{M}]\,k_\infty}{k_0[\mathrm{M}] + k_\infty}$$

The change between them is the **falloff** region. It is centred on the pressure where $k_0[\mathrm{M}] = k_\infty$. Real falloff curves are broader than this simple formula, because molecules with more energy react faster than those with just enough; Hinshelwood, RRKM theory and the Troe formula used in evaluations refine it.

### Chain reactions

Some intermediates are regenerated by the steps they take part in. Bodenstein and Lind (1907) found that $\mathrm{H_2 + Br_2 \to 2HBr}$ follows

$$v = \frac{k[\mathrm{H_2}][\mathrm{Br_2}]^{1/2}}{1 + k'[\mathrm{HBr}]/[\mathrm{Br_2}]}$$

The mechanism is a **chain**. Initiation: $\mathrm{Br_2 \to 2Br}$. Propagation: $\mathrm{Br + H_2 \to HBr + H}$, then $\mathrm{H + Br_2 \to HBr + Br}$, which hands the Br atom back. Inhibition: $\mathrm{H + HBr \to H_2 + Br}$, the reason HBr appears in the denominator. Termination: $\mathrm{2Br \to Br_2}$. The SSA on H and Br gives the rate law exactly; the half order comes from the square root of the Br₂ ⇌ 2Br equilibrium. When a step makes two chain carriers from one (chain branching), the rate can run away; that is why some gas mixtures explode rather than burn steadily.

## Worked example

### 1. Why N₂O₅ looked first order in 1921

At 298 K the IUPAC limits for N₂O₅ in nitrogen are $k_0 = 9.31\times10^{-20}$ cm³ molecule⁻¹ s⁻¹ and $k_\infty = 0.065$ s⁻¹.

1. At 1 bar, $[\mathrm{M}] = p/(k_BT) = 10^5/(1.381\times10^{-23} \times 298) = 2.43\times10^{25}$ m⁻³ $= 2.43\times10^{19}$ cm⁻³.
2. $k_0[\mathrm{M}] = 2.26$ s⁻¹, much larger than $k_\infty$. So $k_\text{uni} = 2.26 \times 0.065/(2.26 + 0.065) = 0.063$ s⁻¹, 97 % of $k_\infty$: first order, half-life 11 s.
3. At 10 mbar, $k_0[\mathrm{M}] = 0.0226$ s⁻¹ and $k_\text{uni} = 0.0226 \times 0.065/0.0876 = 0.017$ s⁻¹, only 26 % of $k_\infty$.
4. The falloff is centred where $k_0[\mathrm{M}] = k_\infty$: $[\mathrm{M}] = 0.065/9.31\times10^{-20} = 7.0\times10^{17}$ cm⁻³, about 29 mbar.

Daniels and Johnston (1921) worked at moderately high pressures and saw clean first-order kinetics. Later work at much lower pressures (Johnston and Perrine, 1951, among the records in NIST SRD 17) found the rate constant falling, as the Lindemann mechanism predicts. In the stratosphere, at 10–100 mbar and colder, N₂O₅ sits in the falloff region, so atmospheric models must use the full pressure-dependent expression.

### 2. A negative activation energy from a pre-equilibrium

For $\mathrm{2NO + O_2}$, NIST lists $k = 2.35\times10^{-38}$ at 270 K and $7.98\times10^{-39}$ cm⁶ molecule⁻² s⁻¹ at 600 K.

1. $E_a = -R\,\dfrac{\ln(k_2/k_1)}{1/T_2 - 1/T_1} = -8.314 \times \dfrac{\ln(0.340)}{1/600 - 1/270} = -8.314 \times \dfrac{-1.080}{-2.037\times10^{-3}} = -4.41$ kJ/mol.
2. With the pre-equilibrium mechanism, $E_a = E_{a,2} + \Delta H_1^\circ$. A negative $E_a$ means the dimerisation releases more heat than step 2 needs to climb its barrier. A single elementary step with a real barrier cannot do this; seeing it is strong evidence for a pre-equilibrium.

## Hands-on

What you need: pencil, Python with the course packages and the [Module 22 lab folder](../../labs/module-22/). Record derivations on a [notebook page](../../templates/notebook-page.md). Time: about 50 minutes.

### Part A — pencil derivations (25 min)

1. Ozone decomposes, $\mathrm{2O_3 \to 3O_2}$, by $\mathrm{O_3 \rightleftharpoons O_2 + O}$ (fast, $K$) then $\mathrm{O + O_3 \to 2O_2}$ (slow, $k_2$). Derive the rate law. What does adding O₂ do?
2. Apply the SSA to the oxygen atom in the same mechanism, with forward $k_1$, reverse $k_{-1}$ and $k_2$, and show that it reduces to your answer to 1 when $k_{-1}[\mathrm{O_2}] \gg k_2[\mathrm{O_3}]$.
3. In the Lindemann expression, find the order of the reaction at high and at low pressure, and the units of $k_0$ and $k_\infty$.
4. For the H₂ + Br₂ chain at the start ($[\mathrm{HBr}] = 0$), add the two steady-state equations for H and Br and show that $[\mathrm{Br}] = (k_i/k_t)^{1/2}[\mathrm{Br_2}]^{1/2}$, where the initiation rate is $2k_i[\mathrm{Br_2}]$ and the termination rate $2k_t[\mathrm{Br}]^2$. What order in Br₂ follows?

<details><summary>Answers to Part A</summary>

1. $[\mathrm{O}] = K[\mathrm{O_3}]/[\mathrm{O_2}]$, so $v = k_2[\mathrm{O}][\mathrm{O_3}] = k_2K[\mathrm{O_3}]^2/[\mathrm{O_2}]$. Second order in O₃, order −1 in O₂: added O₂ slows the reaction by pushing the pre-equilibrium back.
2. $d[\mathrm{O}]/dt = k_1[\mathrm{O_3}] - k_{-1}[\mathrm{O_2}][\mathrm{O}] - k_2[\mathrm{O}][\mathrm{O_3}] = 0$ gives $[\mathrm{O}] = k_1[\mathrm{O_3}]/(k_{-1}[\mathrm{O_2}] + k_2[\mathrm{O_3}])$, so $v = k_1k_2[\mathrm{O_3}]^2/(k_{-1}[\mathrm{O_2}] + k_2[\mathrm{O_3}])$. If $k_{-1}[\mathrm{O_2}]$ dominates the denominator, $v = (k_1/k_{-1})k_2[\mathrm{O_3}]^2/[\mathrm{O_2}]$, the pre-equilibrium result with $K = k_1/k_{-1}$. The SSA contains the pre-equilibrium as a limit.
3. High pressure: $k_\text{uni} = k_\infty$, first order in A; $k_\infty$ in s⁻¹. Low pressure: $v = k_0[\mathrm{M}][\mathrm{A}]$, first order in A and in M, second overall; $k_0$ in cm³ molecule⁻¹ s⁻¹ (or L mol⁻¹ s⁻¹).
4. The propagation steps cancel when the two steady-state equations are added, leaving initiation = termination: $2k_i[\mathrm{Br_2}] = 2k_t[\mathrm{Br}]^2$. So $[\mathrm{Br}] \propto [\mathrm{Br_2}]^{1/2}$, and $v = k_p[\mathrm{Br}][\mathrm{H_2}] \propto [\mathrm{H_2}][\mathrm{Br_2}]^{1/2}$: order ½ in Br₂.

</details>

### Part B — Python: test the SSA and plot the falloff (25 min)

1. Open `lesson03_mechanisms.py`. `exact_product()` already solves A → I → P with `solve_ivp`.
2. Complete `ssa_product()`, `lindemann()` and `half_pressure()`.
3. Run it and open `runs/lesson03_mechanisms.png`:

```bash
py lesson03_mechanisms.py
```

How you know it worked: the largest SSA error is 0.043 of $[\mathrm{A}]_0$ for $k_2/k_1 = 20$ and 0.368 for $k_2/k_1 = 1$. For N₂O₅ at 298 K, $k_\text{uni}/k_\infty$ is 0.003, 0.034, 0.259, 0.778 and 0.972 at 0.0001, 0.001, 0.01, 0.1 and 1 bar, and the half-pressure is 29 mbar. The 2NO + O₂ rate constant falls from $2.35\times10^{-38}$ at 270 K to $7.98\times10^{-39}$ at 600 K.

<details><summary>Reference solution</summary>

```python
def ssa_product(t, A0, k1):
    return A0 * (1 - np.exp(-k1 * t))

def lindemann(k0, kinf, M):
    return k0 * M * kinf / (k0 * M + kinf)

def half_pressure(k0, kinf, T):
    return (kinf / k0) * 1e6 * K_B * T / 1e5
```

Full code: `lesson03_mechanisms_solution.py`. Try $k_2/k_1 = 100$: the error drops to about 1 %, and nearly all of it sits in the first $1/k_2$ of time.

</details>

## Common mistakes

- Writing a rate law from the overall equation instead of from the slow step and what feeds it.
- Leaving an intermediate in the final rate law. Express every intermediate through reactants and products with the SSA or a pre-equilibrium.
- Using the SSA when the intermediate is not short-lived, or during the induction period. Check with a numerical solution, as in Part B.
- Calling a reaction "unimolecular, so first order" without stating the pressure. Gas-phase decompositions fall off to second order at low pressure.
- Believing a mechanism because it reproduces the rate law. It is consistent, not proven; look for independent evidence.

## Key takeaways

- A mechanism is a set of elementary steps that adds up to the overall equation and must reproduce the measured rate law.
- The rate-determining step sets the rate; a fast pre-equilibrium before it contributes its $K$, and can make $E_a$ negative.
- The steady-state approximation, $d[\mathrm{I}]/dt \approx 0$, is accurate when the intermediate is destroyed much faster than it forms, after a short induction period.
- Lindemann: $k_\text{uni} = k_0[\mathrm{M}]k_\infty/(k_0[\mathrm{M}] + k_\infty)$, first order at high pressure and second order at low; for N₂O₅ at 298 K the switch is near 29 mbar.
- Fractional orders and inhibition by products are fingerprints of chain mechanisms such as H₂ + Br₂.

## Sources

- [LibreTexts Physical Chemistry, 29.4 The Steady-State Approximation](https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Physical_Chemistry_(LibreTexts)/29%3A_Chemical_Kinetics_II-_Reaction_Mechanisms/29.04%3A_The_Steady-State_Approximation) — derivation and conditions.
- [LibreTexts Physical Chemistry, 29.6 The Lindemann Mechanism](https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Physical_Chemistry_(LibreTexts)/29%3A_Chemical_Kinetics_II-_Reaction_Mechanisms/29.06%3A_The_Lindemann_Mechanism) — energised molecules and the two pressure limits.
- [LibreTexts Physical Chemistry, 29.7 Chain Reactions](https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Physical_Chemistry_(LibreTexts)/29%3A_Chemical_Kinetics_II-_Reaction_Mechanisms/29.07%3A_Some_Reaction_Mechanisms_Involve_Chain_Reactions) — the H₂ + Br₂ mechanism and rate law.
- [NIST Chemical Kinetics Database, SRD 17](https://kinetics.nist.gov/kinetics/) — N₂O₅ → NO₂ + NO₃, IUPAC 1997: $k_\infty = 9.71\times10^{14}(T/298)^{0.1}e^{-92.3\ \mathrm{kJ/mol}/RT}$ s⁻¹ and $k_0 = 1.0\times10^{-3}(T/298)^{-3.5}e^{-91.5\ \mathrm{kJ/mol}/RT}$ cm³ molecule⁻¹ s⁻¹ (M = N₂); 2NO + O₂ → 2NO₂, IUPAC 2004: $k = 3.30\times10^{-39}e^{+4.41\ \mathrm{kJ/mol}/RT}$ cm⁶ molecule⁻² s⁻¹, 270–600 K; retrieved 2026-10-17.
- [OpenStax Chemistry 2e, 12.6 Reaction Mechanisms](https://openstax.org/books/chemistry-2e/pages/12-6-reaction-mechanisms) — elementary steps, molecularity and rate-determining steps.
