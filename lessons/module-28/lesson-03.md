---
id: "28.3"
module: 28
minutes: 24
practice_minutes: 70
prerequisites: ["28.2", "15.4", "16.5", "05.3"]
objectives:
  - Derive Hammett σ constants from benzoic acid pKa values and explain the signs of σm and σp for donors and acceptors.
  - Fit a Hammett plot to evaluated pKa data, report ρ with its uncertainty, and interpret its sign and size as charge development at the reaction centre.
  - Predict a pKa or a relative rate for a new meta or para substituted compound, including two substituents, and check the prediction against measured data.
  - Recognise when σ+ or σ− is needed (direct conjugation) and when a Hammett plot is not expected to work (ortho groups, changing mechanism).
volatility: concept
sources:
  - title: "Hammett (1937), The Effect of Structure upon the Reactions of Organic Compounds. Benzene Derivatives, J. Am. Chem. Soc. 59, 96"
    url: https://doi.org/10.1021/ja01280a022
  - title: "Hansch, Leo and Taft (1991), A survey of Hammett substituent constants and resonance and field parameters, Chem. Rev. 91, 165"
    url: https://doi.org/10.1021/cr00002a004
  - title: "IUPAC Digitized pKa Dataset v2.4 (Zheng and Lafontant-Joseph), GitHub IUPAC/Dissociation-Constants, CC BY-NC 4.0"
    url: https://github.com/IUPAC/Dissociation-Constants
  - title: "Reusch, Virtual Textbook of Organic Chemistry, Linear Free Energy Relationships (OrganicChemistryData.org)"
    url: https://organicchemistrydata.org/reusch/virtualtext/linear-free-energy-relationships/
  - title: "Chemistry LibreTexts (Roberts and Caserio), 26.6 Correlations of Structure with Reactivity of Aromatic Compounds"
    url: https://chem.libretexts.org/Bookshelves/Organic_Chemistry/Basic_Principles_of_Organic_Chemistry_(Roberts_and_Caserio)/26:_More_on_Aromatic_Compounds/26.06:_Correlations_of_Structure_with_Reactivity_of_Aromatic_Compounds
  - title: "Brown and Okamoto (1958), Electrophilic Substituent Constants, J. Am. Chem. Soc. 80, 4979"
    url: https://doi.org/10.1021/ja01551a055
last_verified: "2026-10-17"
---

# 28.3 · Linear free-energy relationships: Hammett

In 1937 Louis Hammett noticed that a nitro group speeds up the hydrolysis of an ester by roughly the same factor, on a logarithmic scale, as it strengthens benzoic acid, and that the same is true for chloro, methyl or methoxy groups. One number per substituent and one number per reaction were enough to predict hundreds of rate and equilibrium constants. This lesson builds Hammett's σ scale yourself from evaluated pKa values, fits reaction constants ρ for phenols and anilinium ions, and shows what ρ tells you about the transition state. It is the main tool of this module and of its practical.

## Why it matters

A medicinal chemist needs a phenol on a drug candidate to be about half ionised at pH 8.4, or wants a prodrug ester that hydrolyses ten times faster than the current lead. Making ten analogues to find out takes weeks. With a Hammett relation the answer takes a minute: 3,5-dichlorophenol should have a pKa near 8.4, and a para-nitro group on an ethyl benzoate should speed its alkaline hydrolysis about a hundredfold. Hammett plots also answer mechanism questions. A large negative ρ says positive charge builds up next to the ring in the rate-determining transition state; a sudden bend says the mechanism changes across the series. Physical-organic chemists and process chemists use this daily.

## Core ideas

> [!NOTE]
> The Hammett equation and the meaning of σ and ρ are stable. σ values are those of Hansch, Leo and Taft (1991); ρ values are from the Reusch Virtual Textbook table; pKa values come from the IUPAC Digitized pKa Dataset v2.4 (September 2026), which digitises evaluated compilations from 1965–1979. Checked on 2026-10-17. Later dataset versions may add or correct a few values.

### Benzoic acids define σ

Hammett chose one reference reaction: the ionisation of meta- and para-substituted benzoic acids in water at 25 °C. The **substituent constant** of a group X is

$$\sigma_X = \log_{10}\frac{K_X}{K_H} = \mathrm{p}K_a(\text{benzoic acid}) - \mathrm{p}K_a(\text{X-benzoic acid})$$

Benzoic acid itself has p$K_a$ = 4.20. A 4-nitro group lowers it to 3.43, so $\sigma_p(\mathrm{NO_2}) = 0.78$. A positive σ means an **electron-withdrawing** group (it stabilises the carboxylate anion); a negative σ means an **electron-donating** group. σ depends on position. Methoxy has $\sigma_m = +0.12$ but $\sigma_p = -0.27$: from the meta position only its electronegative oxygen acts, pulling electron density through the σ bonds (the **inductive or field effect**); from the para position its lone pair also pushes electron density into the ring by **resonance**, and that wins. Ortho groups are excluded: they also push sterically on the reaction centre.

| X | $\sigma_m$ | $\sigma_p$ | $\sigma_p^+$ |
|---|---|---|---|
| OCH₃ | +0.12 | −0.27 | −0.78 |
| CH₃ | −0.07 | −0.17 | −0.31 |
| H | 0 | 0 | 0 |
| F | +0.34 | +0.06 | −0.07 |
| Cl | +0.37 | +0.23 | +0.11 |
| CF₃ | +0.43 | +0.54 | +0.61 |
| CN | +0.56 | +0.66 | +0.66 |
| NO₂ | +0.71 | +0.78 | +0.79 |

### The Hammett equation

For any other reaction of a meta- or para-substituted benzene derivative,

$$\log_{10}\frac{k_X}{k_H} = \rho\,\sigma_X \qquad \text{or} \qquad \log_{10}\frac{K_X}{K_H} = \rho\,\sigma_X$$

The **reaction constant** ρ is the slope of a plot of $\log(k_X/k_H)$ against σ. By definition ρ = 1 for benzoic acid ionisation.

- **Sign.** ρ > 0: electron-withdrawing groups speed the reaction, so negative charge builds up (or positive charge is lost) near the ring on the way to the transition state or product. ρ < 0: positive charge builds up.
- **Size.** |ρ| > 1: the reaction is more sensitive than benzoic acid, usually because the charge sits closer to the ring or is conjugated with it. |ρ| < 1: the charge is far away or small.

| Reaction (conditions) | ρ |
|---|---|
| Ionisation of phenols (water, 25 °C) | +2.11 |
| Ionisation of anilinium ions (water, 25 °C) | +2.77 |
| Alkaline hydrolysis of ethyl benzoates (85 % ethanol, 25 °C) | +2.54 |
| Benzyl chlorides + iodide, SN2 (acetone, 20 °C) | +0.79 |
| Hydrolysis of benzyl chlorides, SN1 (50 % acetone, 30 °C) | −1.82 |
| N,N-Dimethylanilines + CH₃I (90 % acetone, 35 °C) | −3.30 |

Phenoxide's charge sits on an oxygen attached directly to the ring, so ρ = 2.1, twice the benzoic acid value, where a CO₂⁻ group sits between ring and charge. Ester hydrolysis has ρ = +2.5: hydroxide adds to the carbonyl and the rate-determining transition state carries a negative charge (the tetrahedral intermediate of [16.3](../module-16/lesson-03.md)). SN1 hydrolysis of benzyl chlorides has ρ = −1.8: a benzylic cation forms ([15.5](../module-15/lesson-05.md)).

### Why "linear free-energy relationship"

Since $\log K = -\Delta G^\circ/(2.303RT)$ and, from transition-state theory, $\log k = \text{const} - \Delta^\ddagger G/(2.303RT)$, the Hammett equation says that changing a substituent changes the free energy of the new reaction ($\Delta^\ddagger G$ or $\Delta G^\circ$) in direct proportion to the change it causes in benzoic acid ionisation. It is the same kind of statement as Leffler's α in [28.2](lesson-02.md), with benzoic acid as the yardstick. Nothing in thermodynamics requires it; it works because a substituent at a distance perturbs the charge at the reaction centre in a consistent way.

### σ+ and σ− for direct conjugation

The σ scale assumes the substituent cannot conjugate directly with the reaction centre, which is true for a carboxylate. When the reaction centre can share charge with the para position through the ring, the normal σ fails:

- **σ−** applies when a negative charge or a lone pair at the reaction centre is delocalised onto a para acceptor (NO₂, CN, C=O). In 4-nitrophenoxide the negative charge spreads onto the nitro oxygens. 4-Nitrophenol (p$K_a$ 7.15) is therefore far more acidic than σp = 0.78 and ρ = 2.1 predict (about 8.3): it needs an effective σ of about 1.3–1.4.
- **σ+** applies when a positive charge at the reaction centre is delocalised onto a para donor (OCH₃, CH₃, halogens). Brown and Okamoto (1958) defined it from the SN1 solvolysis of cumyl chlorides, ArC(CH₃)₂Cl, in 90 % aqueous acetone, for which ρ = −4.54. Methoxy goes from σp = −0.27 to σp+ = −0.78. Electrophilic aromatic substitution ([16.5](../module-16/lesson-05.md)) and other reactions that make cations next to the ring correlate with σ+.

When a plot curves, try σ+ or σ−. The **Yukawa–Tsuno** equation interpolates between the two scales: $\log(k_X/k_H) = \rho[\sigma + r(\sigma^+ - \sigma)]$, where $r$ measures how much extra resonance the transition state demands.

### When Hammett plots break

- **Ortho substituents** add steric effects; Taft's equation separates polar and steric terms for those and for aliphatic compounds.
- A **V-shaped** or **broken** plot (two straight lines meeting at an angle) usually means the rate-determining step or the mechanism changes along the series. That is a finding, not a failure.
- **Scatter** from mixing data from different solvents, temperatures or ionic strengths. ρ depends on all three, so only combine values measured under the same conditions.

## Worked example

### 1. pKa values of two dichlorophenols and a dichloroaniline

Substituent effects are roughly additive, so for two groups use $\sigma = \sigma_1 + \sigma_2$. Phenol has p$K_a$ = 9.99 and ρ = 2.11; the anilinium ion has p$K_a$ = 4.60 and ρ = 2.77.

1. 3,5-Dichlorophenol: two meta chlorines, $\sigma = 2 \times 0.37 = 0.74$. $\Delta\mathrm{p}K_a = 2.11 \times 0.74 = 1.56$, so p$K_a \approx 9.99 - 1.56 = 8.43$.
2. 3,4-Dichlorophenol: one meta and one para chlorine, $\sigma = 0.37 + 0.23 = 0.60$. $\Delta\mathrm{p}K_a = 1.27$, so p$K_a \approx 8.73$.
3. 3,4-Dichloroanilinium: $\sigma = 0.60$, $\Delta\mathrm{p}K_a = 2.77 \times 0.60 = 1.66$, so p$K_a \approx 2.94$.

The IUPAC dataset lists 8.18, 8.63 and 2.97 (water, 25 °C). Errors of 0.03–0.25 p$K_a$ units are typical for Hammett predictions with two substituents; two groups side by side (3,4) can also interact with each other, which the simple sum ignores.

### 2. How much faster does a nitro ester hydrolyse?

Alkaline hydrolysis of ethyl benzoates in 85 % ethanol at 25 °C has ρ = 2.54. Compare ethyl 4-nitrobenzoate and ethyl 4-methoxybenzoate with the parent.

1. 4-Nitro: $\log(k/k_H) = 2.54 \times 0.78 = 1.98$, so $k/k_H = 96$.
2. 4-Methoxy: $\log(k/k_H) = 2.54 \times (-0.27) = -0.69$, so $k/k_H = 0.21$.
3. Between the two: $10^{2.54 \times 1.05} = 10^{2.67} \approx 460$.

Two groups at the far side of a ring change the rate by more than two orders of magnitude. The positive ρ says hydroxide attack builds negative charge that acceptors stabilise. Normal σp is the right scale here: the charge in the transition state sits on the carbonyl oxygen and is not conjugated directly with the para position.

## Hands-on

What you need: Python with the course packages (this lab uses RDKit to match structures), an internet connection for one 7 MB download, the [Module 28 lab folder](../../labs/module-28/), pencil and calculator. Time: about 70 minutes.

### Part A — Python: build σ and fit ρ from evaluated pKa data (45 min)

The IUPAC Digitized pKa Dataset contains about 24,000 aqueous pKa values from the IUPAC compilations, each with the compilers' assessment (Reliable, Approximate, Uncertain). Its licence (CC BY-NC 4.0) does not let us store it in the course, so a script downloads it to your computer.

1. Download and extract the data once. The script prints every compound it keeps and how many values went into its median:

```bash
py fetch_iupac_pka.py
```

2. Open `lesson03_hammett.py`. Complete `sigma_from_benzoic()`, `log_k_ratio()` and `effective_sigma()`. The plotting and fitting are written for you; `line_fit()` in `sr28.py` returns the slope with its standard uncertainty, as in [05.3](../module-05/lesson-03.md).
3. Run it and open `runs/lesson03_hammett.png`:

```bash
py lesson03_hammett.py
```

How you know it worked: your σ values from the IUPAC benzoic acids agree with the Hansch–Leo–Taft table to 0.011 on average (largest difference 0.03, for m-NO₂ and p-I), and the benzoic acid plot has slope 1.016 ± 0.013. Phenols (15 points, normal σ): ρ = 2.00 ± 0.14, R² = 0.94. Anilinium ions (17 points): ρ = 3.07 ± 0.14, R² = 0.97. The red points (para NO₂, CN, COCH₃) lie well above both lines; their effective σ values are 1.42, 1.01 and 0.99 for phenols and 1.17 and 0.93 for anilines.

<details><summary>Reference solution and what the numbers mean</summary>

```python
def sigma_from_benzoic(benzoic):
    ref = benzoic[("", "H")]
    return {key: ref - pka for key, pka in benzoic.items() if key != ("", "H")}

def log_k_ratio(series_pka):
    ref = series_pka[("", "H")]
    return {key: ref - pka for key, pka in series_pka.items() if key != ("", "H")}

def effective_sigma(series_pka, rho, names):
    lk = log_k_ratio(series_pka)
    return {n: lk[("p", n)] / rho for n in names if ("p", n) in lk}
```

Full code: `lesson03_hammett_solution.py`.

Your ρ for phenols (2.00 ± 0.14) agrees with the tabulated 2.11 within its uncertainty. Your anilinium ρ (3.07) is higher than the tabulated 2.77: ρ depends on which substituents you include and on the quality of each value. Many phenol values are only "Approximate" with a spread of 0.3 units, which is where the scatter comes from. The effective σ values are σ⁻: the nitro group is worth almost twice its normal σp when it can take the negative charge of a phenoxide directly. In anilines the effect is smaller, because the lone pair of the neutral amine (the base form) is delocalised, not a full negative charge.

</details>

### Part B — pencil (25 min)

1. A substitution of meta- and para-substituted benzylic substrates gives these rate constants relative to the parent: p-CH₃ 2.3 times faster, p-Cl 2.6 times slower, m-NO₂ 18 times slower. Estimate ρ from each point. What does the sign tell you? Then p-OCH₃ turns out to be 30 times faster. Which σ scale fits it?
2. Will ρ for the ionisation of substituted phenylacetic acids, X–C₆H₄–CH₂–COOH, in water be larger or smaller than 1? Why?
3. You want an ethyl benzoate prodrug that hydrolyses (ρ = 2.54) about 10 times faster than the parent. What σ do you need, and which single substituent from the table comes closest?

<details><summary>Answers to Part B</summary>

1. $\rho = \log(k/k_H)/\sigma$: p-CH₃: $\log 2.3/(-0.17) = 0.362/(-0.17) = -2.1$; p-Cl: $\log(1/2.6)/0.23 = -0.415/0.23 = -1.8$; m-NO₂: $\log(1/18)/0.71 = -1.255/0.71 = -1.8$. ρ ≈ −1.9: positive charge builds next to the ring, as in an SN1 ionisation to a benzylic cation. For p-OCH₃: σp predicts $10^{-1.9 \times -0.27} = 3.3$ times faster, σp+ predicts $10^{-1.9 \times -0.78} = 30$ times. σ+ fits: the methoxy lone pair conjugates directly with the cation.
2. Smaller than 1. The CH₂ group separates the ring from the carboxylate, so the substituent's effect on the charge is weaker and is not transmitted by conjugation. The related cinnamic acids, with a CH=CH spacer, have ρ = 0.47.
3. $\sigma = 1/2.54 = 0.39$. m-Br (0.39) or m-Cl (0.37) gives about $10^{2.54 \times 0.37} = 8.7$ to $10^{0.99} = 9.8$ times; m-CF₃ (0.43) gives about 12 times.

</details>

## Common mistakes

- Using ln instead of log₁₀. σ and ρ are defined with log₁₀; using ln makes ρ 2.3 times too large.
- Swapping the sign of σ. σ = pKa(parent) − pKa(substituted): an acid-strengthening group has positive σ.
- Using σp for a group that conjugates directly with a charged reaction centre. Para acceptors next to a negative charge need σ⁻; para donors next to a positive charge need σ⁺.
- Putting ortho substituents on a Hammett plot. Their steric effects do not follow σ.
- Mixing rate constants from different solvents or temperatures in one plot; ρ itself changes with both.
- Reading a broken or curved plot as bad data before asking whether the mechanism or the rate-determining step changes along the series.

## Key takeaways

- σ is defined by benzoic acid ionisation in water at 25 °C: σ = pKa(benzoic acid) − pKa(substituted acid); positive for acceptors, negative for donors.
- $\log(k_X/k_H) = \rho\sigma$: the sign of ρ tells you which charge develops near the ring, its size how strongly and how close.
- Hammett's equation is a linear free-energy relationship: substituent effects on $\Delta^\ddagger G$ or $\Delta G^\circ$ scale with their effects on benzoic acid.
- Phenols (ρ ≈ 2.0–2.1) and anilinium ions (ρ ≈ 2.8–3.1) need σ⁻ for para acceptors; cations need σ⁺ for para donors.
- Ortho groups, mixed conditions and mechanism changes break simple Hammett plots; the break itself can be the result.

## Sources

- [Hammett, J. Am. Chem. Soc. 59, 96 (1937)](https://doi.org/10.1021/ja01280a022) — the original σρ treatment (record checked via Crossref).
- [Hansch, Leo and Taft, Chem. Rev. 91, 165 (1991)](https://doi.org/10.1021/cr00002a004) — the standard table of σm, σp and σp+; values used here as reproduced in the [Zipse (LMU Munich) teaching table](https://zipse.cup.uni-muenchen.de/site/assets/files/1480/hammett_19_06_02.pdf) and in Table 1 of El Abed et al. (2025).
- [IUPAC Digitized pKa Dataset v2.4, GitHub IUPAC/Dissociation-Constants](https://github.com/IUPAC/Dissociation-Constants) — evaluated aqueous pKa values (CC BY-NC 4.0, "Reproduced by permission of International Union of Pure and Applied Chemistry"; Zenodo doi 10.5281/zenodo.7236452), release v2.4 of 2026-09-21.
- [Reusch, Virtual Textbook of Organic Chemistry, Linear Free Energy Relationships](https://organicchemistrydata.org/reusch/virtualtext/linear-free-energy-relationships/) — ρ values for phenols, anilinium ions, cinnamic acids, ester hydrolysis and substitution reactions.
- [Chemistry LibreTexts (Roberts and Caserio), 26.6 Correlations of Structure with Reactivity of Aromatic Compounds](https://chem.libretexts.org/Bookshelves/Organic_Chemistry/Basic_Principles_of_Organic_Chemistry_(Roberts_and_Caserio)/26:_More_on_Aromatic_Compounds/26.06:_Correlations_of_Structure_with_Reactivity_of_Aromatic_Compounds) — meaning of ρ and σ.
- [Brown and Okamoto, J. Am. Chem. Soc. 80, 4979 (1958)](https://doi.org/10.1021/ja01551a055) — electrophilic substituent constants σ+ from cumyl chloride solvolysis (ρ = −4.54).
