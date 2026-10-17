---
id: "22.4"
module: 22
minutes: 24
practice_minutes: 75
prerequisites: ["22.3", "02.1", "13.4"]
objectives:
  - Fit the Arrhenius equation to rate constants and report the activation energy and pre-exponential factor with uncertainties.
  - Estimate a collision-theory rate constant and the steric factor for a real gas-phase reaction.
  - Extract the enthalpy and entropy of activation from an Eyring plot and interpret the sign of the entropy.
  - Explain why real Arrhenius plots curve, using OH + CH4 data from 196 to 2000 K.
volatility: concept
sources:
  - title: "LibreTexts Physical Chemistry, 28.7 Rate Constants Are Usually Strongly Temperature Dependent"
    url: https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Physical_Chemistry_(LibreTexts)/28%3A_Chemical_Kinetics_I_-_Rate_Laws/28.07%3A_Rate_Constants_Are_Usually_Strongly_Temperature_Dependent
  - title: "LibreTexts Physical Chemistry, 28.8 Transition-State Theory Can Be Used to Estimate Reaction Rate Constants"
    url: https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Physical_Chemistry_(LibreTexts)/28%3A_Chemical_Kinetics_I_-_Rate_Laws/28.08%3A_Transition-State_Theory_Can_Be_Used_to_Estimate_Reaction_Rate_Constants
  - title: "NIST Chemical Kinetics Database (SRD 17), CH4 + OH and N2O5 records"
    url: https://kinetics.nist.gov/kinetics/
  - title: "OpenStax Chemistry 2e, 12.5 Collision Theory"
    url: https://openstax.org/books/chemistry-2e/pages/12-5-collision-theory
  - title: "NIST CODATA fundamental physical constants"
    url: https://physics.nist.gov/cuu/Constants/
last_verified: "2026-10-17"
---

# 22.4 · Temperature dependence: Arrhenius and transition-state theory

Almost every reaction speeds up when you heat it, often by a factor of two or more for 10 K. In [02.1](../module-02/lesson-01.md) you learnt to straighten the Arrhenius equation into a line of $\ln k$ against $1/T$. This lesson asks what the two numbers from that line mean: collision theory reads the pre-exponential factor as a collision rate, and transition-state theory turns both numbers into an enthalpy and an entropy of activation. You will analyse real data for two atmospheric reactions and time an effervescent tablet at four temperatures.

## Why it matters

A vaccine that must be kept between 2 and 8 °C, a food label that says "keep refrigerated", and an accelerated stability test in which a drug is stored at 40 °C for six months to predict two years at 25 °C all rest on one assumption: that you know how the rate of decay depends on temperature. The extrapolation uses the activation energy. With $E_a$ = 100 kJ/mol, a reaction runs 4.8 times faster at 37 °C than at 25 °C; with 50 kJ/mol, only 2.2 times. Choose the wrong $E_a$, or assume the Arrhenius line is straight when it is not, and the predicted shelf life is wrong by months.

## Core ideas

> [!NOTE]
> The theory is stable. The OH + CH₄ values are from two experimental studies listed in the NIST Chemical Kinetics Database (Gierczak et al. 1997, 196–420 K; Srinivasan et al. 2005, 840–2025 K), computed from each study's fitted expression; the N₂O₅ high-pressure limit is the IUPAC (1997) evaluation; constants are CODATA 2022. All checked on 2026-10-17.

### The Arrhenius equation

$$k = A\,e^{-E_a/RT}, \qquad \ln k = \ln A - \frac{E_a}{R}\,\frac{1}{T}$$

$E_a$ is the **activation energy** and $A$ the **pre-exponential factor**, with the same units as $k$. A more general definition, which works even when the plot is curved, is the local slope

$$E_a = RT^2\,\frac{d\ln k}{dT} = -R\,\frac{d\ln k}{d(1/T)}$$

Near room temperature, a reaction with $E_a \approx 53$ kJ/mol doubles its rate for every 10 K. Fit $\ln k$ against $1/T$ by least squares and take the uncertainties from the covariance matrix (lesson [05.3](../module-05/lesson-03.md)). The intercept sits far outside the data, at $1/T = 0$, so $A$ is always much less certain than $E_a$, and the two are strongly correlated.

### Collision theory

For a gas-phase reaction between A and B, the most it could possibly do is react at every collision with enough energy. Collision theory gives

$$k = P\,\sigma\,\bar v_\text{rel}\,e^{-E_a/RT}, \qquad \bar v_\text{rel} = \sqrt{\frac{8k_BT}{\pi\mu}}$$

$\sigma = \pi d^2$ is the collision cross-section, $d$ the sum of the two molecular radii, $\mu$ the reduced mass and $\bar v_\text{rel}$ the mean relative speed. $P$ is the **steric factor**, the fraction of collisions with a useful orientation. Collision theory cannot calculate $P$, which is often far below 1; transition-state theory fixes that weakness.

### Transition-state theory

Picture the reaction as a path over a mountain pass on the potential energy surface; the configuration at the top is the **transition state** (activated complex), written ‡. Transition-state theory (Eyring, Evans and Polanyi, 1935) makes two assumptions: the transition state is in equilibrium with the reactants, and every complex that reaches the top crosses over at a rate set by a universal frequency $k_BT/h$. Then

$$k = \kappa\,\frac{k_BT}{h}\,K^\ddagger$$

where $K^\ddagger$ is the equilibrium constant for forming the transition state and $\kappa \le 1$ the **transmission coefficient** (often set to 1). $k_BT/h = 6.21\times10^{12}$ s⁻¹ at 298 K. $K^\ddagger$ can be calculated from partition functions of the reactants and the transition state, exactly as an ordinary equilibrium constant is in [21.4](../module-21/lesson-04.md). Writing it thermodynamically, $K^\ddagger = e^{-\Delta^\ddagger G/RT}$ with $\Delta^\ddagger G = \Delta^\ddagger H - T\Delta^\ddagger S$ (the same relation as in [13.4](../module-13/lesson-04.md)), gives the **Eyring equation**:

$$k = \frac{k_BT}{h}\,e^{\Delta^\ddagger S/R}\,e^{-\Delta^\ddagger H/RT}$$

A plot of $\ln(k/T)$ against $1/T$ has slope $-\Delta^\ddagger H/R$ and intercept $\ln(k_B/h) + \Delta^\ddagger S/R$. For a unimolecular reaction, comparison with Arrhenius gives $E_a = \Delta^\ddagger H + RT$ and $A = e\,(k_BT/h)\,e^{\Delta^\ddagger S/R}$.

The entropy of activation tells you about the shape of the transition state. A molecule breaking apart passes through a loose, floppy transition state with more freedom than the reactant: $\Delta^\ddagger S > 0$ and $A$ above about $10^{13}$ s⁻¹. Two molecules joining into one, or a ring closing, pass through a tight transition state: $\Delta^\ddagger S < 0$ and a small $A$. For a bimolecular reaction, $\Delta^\ddagger S$ also depends on the standard state you choose (1 bar or 1 mol/L), so always say which one.

### Why real Arrhenius plots curve

The simple equation assumes $A$ and $E_a$ do not depend on $T$. Transition-state theory says $A$ contains $k_BT/h$ and partition functions that change with temperature, so evaluations often use the modified form $k = A(T/298)^n e^{-E/RT}$, whose local activation energy is $E + nRT$, rising with temperature. At low temperature a second effect adds to this for reactions that move a hydrogen atom: the H atom can **tunnel** through the top of the barrier ([12.3](../module-12/lesson-03.md)), so the rate falls less steeply than Arrhenius predicts. For OH + CH₄ the local activation energy climbs from about 13 kJ/mol near 200 K to 34 kJ/mol above 800 K. A straight line through room-temperature data, extrapolated to a flame, would be wrong by a large factor.

Change $E_a$ and $A$ and watch how strongly a 10 K change moves the rate:

[Simulation: Kinetics — Arrhenius plot](../../simulations/kinetics/index.html?preset=arrhenius)

## Worked example

### 1. Enthalpy and entropy of activation for N₂O₅ → NO₂ + NO₃

The IUPAC high-pressure limit gives $k_\infty = 0.065$ s⁻¹ at 298 K and an Arrhenius slope corresponding to $E_a = 92.5$ kJ/mol.

1. $\Delta^\ddagger H = E_a - RT = 92.5 - 2.48 = 90.0$ kJ/mol.
2. $\Delta^\ddagger G = -RT\ln\dfrac{kh}{k_BT} = -2.478 \times \ln\dfrac{0.065}{6.21\times10^{12}} = -2.478 \times (-32.19) = 79.8$ kJ/mol.
3. $\Delta^\ddagger S = (\Delta^\ddagger H - \Delta^\ddagger G)/T = (90.0 - 79.8)\times10^3/298 = +34$ J mol⁻¹ K⁻¹.

The positive entropy fits a loose transition state in which the N–O bond to the NO₃ group is stretched and the two halves rotate freely. The Eyring fit in the lab gives the same answer from the whole 200–300 K range.

### 2. The steric factor of OH + CH₄

1. Reduced mass: $\mu = 17.0 \times 16.0/33.0 = 8.25$ u $= 1.37\times10^{-26}$ kg.
2. $\bar v_\text{rel} = \sqrt{8 \times 1.381\times10^{-23} \times 298/(\pi \times 1.37\times10^{-26})} = 874$ m/s.
3. With a rough collision diameter of 0.35 nm, $\sigma = \pi(0.35\times10^{-7}\ \mathrm{cm})^2 = 3.85\times10^{-15}$ cm², and $\sigma\bar v_\text{rel} = 3.4\times10^{-10}$ cm³ molecule⁻¹ s⁻¹.
4. The measured $A$ for 196–300 K is $1.6\times10^{-12}$ cm³ molecule⁻¹ s⁻¹, so $P = 1.6\times10^{-12}/3.4\times10^{-10} \approx 0.005$.

Only about one collision in 200 with enough energy reacts. OH must hit one of the four H atoms end-on, along the C–H bond; transition-state theory captures that geometry in a negative $\Delta^\ddagger S$.

## Hands-on

What you need: pencil, calculator, Python with the course packages and the [Module 22 lab folder](../../labs/module-22/); for Part C, four identical effervescent tablets, four glasses, a kitchen thermometer and a phone stopwatch. Write up Part C with the [lab report template](../../templates/lab-report.md). Time: about 75 minutes.

### Part A — pencil (15 min)

1. A drug degrades 3.0 times faster at 40 °C than at 25 °C. What is $E_a$? Using it, how much slower is the degradation at 5 °C than at 25 °C?
2. Two first-order isomerisations have the same $\Delta^\ddagger H$ = 100 kJ/mol. One has $\Delta^\ddagger S = +40$ J mol⁻¹ K⁻¹, the other $-40$ J mol⁻¹ K⁻¹. What is the ratio of their rate constants at 298 K, and which one is likely a ring closure?
3. An Eyring plot for a unimolecular reaction gives a slope of $-1.20\times10^4$ K. What are $\Delta^\ddagger H$ and $E_a$ at 300 K?

<details><summary>Answers to Part A</summary>

1. $E_a = R\ln 3/(1/298.15 - 1/313.15) = 8.314 \times 1.099/1.607\times10^{-4} = 56.8$ kJ/mol. From 25 °C to 5 °C: $\exp[-56\,800/8.314 \times (1/278.15 - 1/298.15)] = e^{-1.65} = 0.19$, about five times slower. This is accelerated stability testing; it fails if the mechanism changes with temperature.
2. $k_1/k_2 = e^{(40 - (-40))/8.314} = e^{9.62} = 1.5\times10^4$. The one with negative $\Delta^\ddagger S$ is likely the ring closure, because the chain loses its freedom to rotate in the transition state.
3. $\Delta^\ddagger H = 1.20\times10^4 \times 8.314 = 99.8$ kJ/mol; $E_a = \Delta^\ddagger H + RT = 99.8 + 2.5 = 102.3$ kJ/mol.

</details>

### Part B — Python: OH + CH₄ and N₂O₅ (25 min)

1. Open `lesson04_arrhenius.py`. It reads `oh_ch4_k.csv` (20 rate constants from 196 to 2000 K) and builds the N₂O₅ high-pressure rate constants from 200 to 300 K.
2. Complete `arrhenius_fit()` (with uncertainties from `np.polyfit(..., cov=True)`), `eyring_fit()` and `local_ea()`.
3. Run it and open `runs/lesson04_arrhenius.png`:

```bash
py lesson04_arrhenius.py
```

How you know it worked: OH + CH₄ gives $E_a$ = 13.8 kJ/mol for 196–300 K, 16.5 for 300–420 K and 34.4 for 840–2000 K; the local $E_a$ climbs from 12.9 kJ/mol at 198 K to about 34 kJ/mol above 900 K, and the dashed low-temperature line misses the high-temperature points by a large factor. For N₂O₅, $E_a$ = 92.5 kJ/mol, $A = 1.05\times10^{15}$ s⁻¹, $\Delta^\ddagger H$ = 90.5 kJ/mol and $\Delta^\ddagger S$ = +36 J mol⁻¹ K⁻¹.

The uncertainties printed for these fits are tiny, and for the shock-tube range zero. That is not a sign of good data: the CSV holds values computed from each study's own fitted expression, so they lie exactly on a smooth curve. With raw measurements, expect several per cent scatter and an $E_a$ uncertainty of 1–2 kJ/mol.

<details><summary>Reference solution</summary>

```python
def arrhenius_fit(T, k):
    (slope, intercept), cov = np.polyfit(1.0 / T, np.log(k), 1, cov=True)
    A = math.exp(intercept)
    return -slope * R, A, math.sqrt(cov[0, 0]) * R, A * math.sqrt(cov[1, 1])

def eyring_fit(T, k):
    slope, intercept = np.polyfit(1.0 / T, np.log(k / T), 1)
    return -slope * R, (intercept - math.log(K_B / H)) * R

def local_ea(T, k):
    return -R * np.diff(np.log(k)) / np.diff(1.0 / T)
```

Full code: `lesson04_arrhenius_solution.py`.

</details>

### Part C — kitchen: an effervescent tablet at four temperatures (35 min)

> [!WARNING]
> Use hot tap water no hotter than about 50 °C, never boiling water: water above 50 °C can scald. Prefer plain vitamin C or electrolyte effervescent tablets; tablets that contain a drug (for example aspirin) should not be used for play and must be kept away from children. Do not drink the solutions. Work at a sink, because the glasses can fizz over.

1. Fill four identical glasses with the same volume of water (about 200 mL) at roughly 8 °C (from the fridge), 20 °C, 35 °C and 50 °C. Measure each temperature with the thermometer just before you start.
2. Drop one whole tablet into the first glass and start the stopwatch. Stop it when the last solid disappears and the fizzing becomes slow. Use the same end point every time.
3. Repeat for the other glasses. If you have eight tablets, do each temperature twice.
4. Copy `tablet_times_template.csv` to `tablet_times.csv`, enter one row per run (temperature in °C, time in seconds) and rerun `py lesson04_arrhenius.py`. The script uses $1/t$ as the rate.

How you know it worked: the dissolving time falls steadily with temperature and the Arrhenius plot of $\ln(1/t)$ against $1/T$ is roughly straight. Compare your apparent activation energy with about 16 kJ/mol, the value you get from the viscosity of water between 20 and 40 °C (1.002 and 0.653 mPa s), which is typical for processes limited by diffusion.

<details><summary>What the result means</summary>

The tablet is not one elementary reaction. Citric acid and sodium hydrogen carbonate must dissolve, diffuse together and react, and the CO₂ must escape. The slowest of these sets the time, and dissolving and diffusion have low activation energies. An apparent $E_a$ of a few tens of kJ/mol tells you the process is partly physical, not limited by breaking a bond. Repeat runs at one temperature give the scatter; expect 5–10 % from judging the end point. This experiment trains the analysis, not bench technique: it measures no concentration and uses no reagent.

</details>

## Common mistakes

- Plotting $\ln k$ against $T$ instead of $1/T$, or using °C instead of K.
- Quoting $A$ to three figures. It is an extrapolation to $1/T = 0$, far beyond the data; give its uncertainty.
- Extrapolating a straight Arrhenius line far outside the measured range. Real plots curve, especially for H-atom transfer.
- Mixing up $E_a$ and $\Delta^\ddagger H$. They differ by $RT$ (about 2.5 kJ/mol at room temperature) for a unimolecular reaction.
- Fitting points that are themselves outputs of a fit and reporting the tiny uncertainty as if it were measured.

## Key takeaways

- Arrhenius: $\ln k = \ln A - E_a/RT$; the general definition $E_a = RT^2\,d\ln k/dT$ also works for curved plots.
- Collision theory gives an upper limit $\sigma\bar v_\text{rel}$; the steric factor $P$ is often far below 1 (about 0.005 for OH + CH₄).
- Transition-state theory: $k = (k_BT/h)K^\ddagger$; the Eyring plot of $\ln(k/T)$ against $1/T$ gives $\Delta^\ddagger H$ and $\Delta^\ddagger S$.
- Loose transition states (bond fission) have $\Delta^\ddagger S > 0$; tight ones (association, ring closure) have $\Delta^\ddagger S < 0$.
- Temperature-dependent prefactors and tunnelling bend Arrhenius plots: OH + CH₄ goes from 13 to 34 kJ/mol between 200 and 2000 K.

## Sources

- [LibreTexts Physical Chemistry, 28.7 Rate Constants Are Usually Strongly Temperature Dependent](https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Physical_Chemistry_(LibreTexts)/28%3A_Chemical_Kinetics_I_-_Rate_Laws/28.07%3A_Rate_Constants_Are_Usually_Strongly_Temperature_Dependent) — Arrhenius equation and activation energy.
- [LibreTexts Physical Chemistry, 28.8 Transition-State Theory](https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Physical_Chemistry_(LibreTexts)/28%3A_Chemical_Kinetics_I_-_Rate_Laws/28.08%3A_Transition-State_Theory_Can_Be_Used_to_Estimate_Reaction_Rate_Constants) — Eyring equation, enthalpy and entropy of activation.
- [NIST Chemical Kinetics Database, SRD 17](https://kinetics.nist.gov/kinetics/) — CH₄ + OH: Gierczak et al., J. Phys. Chem. A 101, 3125 (1997), $1.76\times10^{-13}(T/298)^{2.82}e^{-8.21\ \mathrm{kJ/mol}/RT}$ (flash photolysis, laser-induced fluorescence); Srinivasan et al., J. Phys. Chem. A 109, 1857 (2005), $9.52\times10^{-11}e^{-34.4\ \mathrm{kJ/mol}/RT}$ cm³ molecule⁻¹ s⁻¹ (shock tube); N₂O₅ high-pressure limit, IUPAC 1997; retrieved 2026-10-17.
- [OpenStax Chemistry 2e, 12.5 Collision Theory](https://openstax.org/books/chemistry-2e/pages/12-5-collision-theory) — collisions, orientation and the Arrhenius equation.
- [NIST Chemistry WebBook, thermophysical properties of fluids](https://webbook.nist.gov/chemistry/fluid/) — viscosity of water at 20 and 40 °C (1.002 and 0.653 mPa s).
- [NIST CODATA constants](https://physics.nist.gov/cuu/Constants/) — $k_B$, $h$, $N_A$ (exact in the 2019 SI).
