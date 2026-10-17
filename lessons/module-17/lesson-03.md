---
id: "17.3"
module: 17
minutes: 25
practice_minutes: 65
prerequisites: ["17.2", "12.5", "14.5"]
objectives:
  - Predict the number of ¹H NMR signals of a molecule from its symmetry, and the approximate chemical shift of each.
  - Use integration to find the ratio of hydrogens in each environment.
  - Predict and read first-order splitting with the n+1 rule and coupling constants, and recognise when a spectrum is second order.
  - Assign a real ¹H spectrum from SDBS to a structure, signal by signal.
volatility: concept
sources:
  - title: "OpenStax Organic Chemistry (McMurry, 2023), 13.2 The Nature of NMR Absorptions"
    url: https://openstax.org/books/organic-chemistry/pages/13-2-the-nature-of-nmr-absorptions
  - title: "OpenStax Organic Chemistry, 13.4 Chemical Shifts in 1H NMR Spectroscopy"
    url: https://openstax.org/books/organic-chemistry/pages/13-4-chemical-shifts-in-1h-nmr-spectroscopy
  - title: "OpenStax Organic Chemistry, 13.6 Spin-Spin Splitting in 1H NMR Spectra"
    url: https://openstax.org/books/organic-chemistry/pages/13-6-spin-spin-splitting-in-1h-nmr-spectra
  - title: "OpenStax Organic Chemistry, 13.7 1H NMR Spectroscopy and Proton Equivalence"
    url: https://openstax.org/books/organic-chemistry/pages/13-7-1h-nmr-spectroscopy-and-proton-equivalence
  - title: "Hans Reich, NMR Spectroscopy collection (organicchemistrydata.org)"
    url: https://organicchemistrydata.org/hansreich/resources/nmr/
  - title: "NIST CODATA 2022: proton gyromagnetic ratio over 2 pi"
    url: https://physics.nist.gov/cgi-bin/cuu/Value?gammapbar
  - title: "SDBS Spectral Database for Organic Compounds (AIST)"
    url: https://sdbs.db.aist.go.jp/
last_verified: "2026-10-17"
---

# 17.3 · Proton NMR: shift, integration and splitting

Proton nuclear magnetic resonance (¹H NMR) is the most informative single spectrum in organic chemistry. It tells you how many kinds of hydrogen a molecule has, what each one is next to, how many of each there are, and how many hydrogens sit on the neighbouring carbons. Mass spectrometry gave you the formula and IR the functional groups; ¹H NMR shows how the pieces are joined. This lesson covers the three things to read in every signal, shift, integration and splitting, and when the simple rules stop working.

## Why it matters

Two bottles are both C₄H₈O₂ carboxylic acids: one is butanoic acid (rancid-butter smell), the other 2-methylpropanoic acid. IR showed the same O–H and C=O bands for both ([17.2](lesson-02.md)), and their molecular ions are the same. The ¹H NMR spectra differ at a glance. Butanoic acid shows a 3H triplet, a 2H sextet and a 2H triplet; 2-methylpropanoic acid shows a 6H doublet and a 1H septet. A chemist checking a reaction product, a quality-control lab confirming a drug batch, or a hospital MRI scanner (the same physics, applied to water in tissue) all rely on reading these patterns.

## Core ideas

> [!NOTE]
> The physics and the shift and coupling ranges are stable. Constants are CODATA 2022 (NIST), checked 2026-10-17. Typical ranges follow OpenStax Organic Chemistry (2023) chapter 13 and Hans Reich's NMR tables. Real spectra are in SDBS, which you search by compound name; its interface may change.

### Nuclei in a magnet

A proton has spin ½: it behaves like a tiny bar magnet with two allowed orientations in a magnetic field $B_0$, aligned or opposed (the quantised angular momentum of [12.5](../module-12/lesson-05.md)). The energy gap is tiny and corresponds to radio waves:

$$\nu = \frac{\gamma}{2\pi} B_0, \qquad \frac{\gamma}{2\pi}(^1\text{H}) = 42.577\ \text{MHz T}^{-1}$$

A 9.4 T magnet gives $\nu = 42.577 \times 9.4 \approx 400$ MHz, which is why spectrometers are named by their proton frequency ("a 400 MHz NMR"). Modern instruments excite all protons at once with a short radio pulse and record the decaying signal; a Fourier transform turns that signal into the spectrum ([14.5](../module-14/lesson-05.md)).

### Chemical shift: what is the hydrogen next to?

Electrons around a nucleus circulate in the field and create a small opposing field. They **shield** the nucleus, so it resonates at a slightly lower frequency. Electronegative neighbours pull electrons away and **deshield** the proton, moving its signal to higher frequency. The position is reported as the **chemical shift** δ, in parts per million relative to tetramethylsilane (TMS, δ = 0):

$$\delta = \frac{\nu_\text{sample} - \nu_\text{TMS}}{\nu_\text{spectrometer}} \times 10^6$$

Dividing by the spectrometer frequency makes δ the same on every instrument. On the page, δ increases to the left ("downfield").

| δ (ppm) | Typical proton |
|---|---|
| 0.9–1.0 | CH₃ in an alkyl chain |
| 1.2–1.7 | CH₂ and CH in alkyl chains |
| 1.6–1.9 | allylic, H–C–C=C |
| 2.0–2.6 | H–C–C=O (2.1 for CH₃CO), benzylic H–C–Ar (2.3) |
| 2.5–3.0 | terminal alkyne ≡C–H |
| 3.3–4.5 | H–C–O, H–C–Cl, H–C–Br, H–C–NO₂ (more electronegative, higher) |
| 4.5–6.5 | alkene =C–H |
| 6.5–8.5 | aromatic Ar–H |
| 9.5–10.5 | aldehyde CHO |
| 10–13 | carboxylic acid COOH (broad) |
| 1–5, variable | O–H of alcohols, N–H of amines (often broad) |

Aromatic and aldehyde protons sit far downfield not only because of electronegativity but because the circulating π electrons of the ring or C=O create a local field that adds to $B_0$ at those protons (anisotropy).

### Counting signals: equivalence

Protons that can be swapped by a symmetry operation of the molecule or by fast bond rotation are **chemically equivalent** and give one signal. The three H of a CH₃ group are equivalent (rotation). The two CH₃ groups of 2-chloropropane are equivalent (mirror plane). So 2-chloropropane, (CH₃)₂CHCl, shows two signals: 6H and 1H. A quick test: replace each H in turn by a dummy atom X; if two replacements give the same compound, the two H are equivalent.

### Integration: how many of each

The area under a signal is proportional to the number of protons that produce it. Spectrometers draw an integral curve or print a number per signal. You get ratios, not absolute numbers: 2 : 3 might mean 2H and 3H or 4H and 6H. The molecular formula from [17.1](lesson-01.md) fixes the total.

### Splitting: how many neighbours

Each proton feels the small magnetic fields of the protons on neighbouring carbons, passed through the bonding electrons. This **spin–spin coupling** splits its signal. The **n+1 rule**: a proton with n equivalent neighbours (usually on adjacent carbons, three bonds away) gives n+1 lines, with heights from Pascal's triangle:

| Neighbours n | Pattern | Heights |
|---|---|---|
| 0 | singlet (s) | 1 |
| 1 | doublet (d) | 1 : 1 |
| 2 | triplet (t) | 1 : 2 : 1 |
| 3 | quartet (q) | 1 : 3 : 3 : 1 |
| 6 | septet | 1 : 6 : 15 : 20 : 15 : 6 : 1 |

The spacing between lines is the **coupling constant** J, in Hz. Coupled partners share the same J, which is how you find which signal couples to which. Typical values: 6–8 Hz between H on neighbouring sp³ carbons; 12–18 Hz across a trans C=C and 6–12 Hz across a cis C=C; 7–9 Hz between ortho aromatic H. Equivalent protons do not split each other. O–H and N–H protons usually exchange fast between molecules, so they appear as broad singlets and do not split their neighbours.

The ethyl group, CH₃CH₂–X, always gives a 3H triplet and a 2H quartet with the same J. The isopropyl group, (CH₃)₂CH–X, gives a 6H doublet and a 1H septet. Learn to spot both at once.

### When the rules break: second-order spectra

The n+1 rule assumes the shift difference between coupled protons, in Hz, is much larger than J. A useful rule: if $\Delta\nu / J > 10$, the spectrum is close to first order. For bromoethane on a 60 MHz instrument, $\Delta\nu = (3.43 - 1.67) \times 60 = 106$ Hz and $J = 7.3$ Hz, a ratio of 14.5: almost first order. When the ratio falls towards 1, the inner lines of the two multiplets grow and the outer lines shrink ("roofing", the multiplets lean towards each other), extra lines appear, and the n+1 rule fails. A higher-field magnet increases $\Delta\nu$ in Hz while J stays the same, which is one reason chemists pay for bigger magnets. Diastereotopic CH₂ protons next to a stereocentre, and many aromatic rings, often give second-order patterns even at 400 MHz.

## Worked example

### Butanoic acid or 2-methylpropanoic acid?

The unknown C₄H₈O₂ acid shows: δ 0.98 (t, J = 7.4 Hz, 3H), 1.68 (sextet, 2H), 2.35 (t, J = 7.5 Hz, 2H), 11.8 (broad s, 1H).

1. Integration 3 : 2 : 2 : 1 = 8 H, matching C₄H₈O₂.
2. 11.8, broad, 1H: COOH.
3. 2.35, 2H, triplet: a CH₂ next to C=O (2.0–2.6) with 2 neighbours.
4. 0.98, 3H, triplet: a CH₃ with 2 neighbours, at the end of a chain.
5. 1.68, 2H, sextet: 5 neighbours (3 + 2). It sits between the CH₃ and the CH₂C=O.
6. Structure: CH₃–CH₂–CH₂–COOH, butanoic acid.

2-Methylpropanoic acid, (CH₃)₂CH–COOH, would show a 6H doublet near 1.2, a 1H septet near 2.6 and the COOH: an isopropyl pattern. The shifts here are rounded typical values; check them against the real SDBS spectrum of either acid.

### Predicting a spectrum: 1-nitropropane

CH₃–CH₂–CH₂–NO₂ has three environments. The CH₂ next to NO₂ is strongly deshielded (about 4.4, 2H, t). The middle CH₂ has 3 + 2 = 5 neighbours (about 2.0, 2H, sextet). The CH₃ is about 1.0 (3H, t).

## Hands-on

What you need: a browser, Python with the course packages and the [Module 17 lab folder](../../labs/module-17/). Use section 4 of the [spectrum assignment sheet](../../templates/spectrum-assignment.md) for Part C. Time: about 65 minutes.

### Part A — simulation: watch splitting appear (15 min)

[Simulation: NMR — an ethyl group, triplet and quartet](../../simulations/nmr/index.html?preset=ethyl)

[Simulation: NMR — an isopropyl group, doublet and septet](../../simulations/nmr/index.html?preset=isopropyl)

[Simulation: NMR — second-order effects at low field](../../simulations/nmr/index.html?preset=second-order)

Task: in the ethyl preset, measure J from the quartet and from the triplet and confirm they are equal. In the second-order preset, lower the field until $\Delta\nu/J$ is about 2 and note what happens to the line heights. Target: J about 7 Hz in both multiplets; at low ratio the inner lines grow and the outer lines shrink.

### Part B — Python: simulate and count (20 min)

1. Open `lesson03_nmr1h.py`. Complete `multiplet()` (n+1 lines, Pascal heights) and the count in `h_environments()`.
2. Run it:

```bash
py lesson03_nmr1h.py
```

3. Open `runs/lesson03_spectra.png`.

How you know it worked: Pascal rows up to 1 6 15 20 15 6 1; signal counts bromoethane 2, 2-chloropropane 2, 1-nitropropane 3, 2-butanol 5, tert-butyl methyl ether 2, 1,4-dichlorobenzene 1. At 400 MHz the multiplets are much narrower in ppm than at 60 MHz, while J in Hz is unchanged.

<details><summary>Reference solution</summary>

`multiplet` returns `[(k - n/2) * J for k in range(n + 1)]` and `[comb(n, k) for k in range(n + 1)]`. `h_environments` counts the distinct canonical ranks of the H atoms. Full code: `lesson03_nmr1h_solution.py`. The rank method is topological: it cannot see that the two H of the CH₂ in 2-butanol are diastereotopic (the stereocentre next door makes them different), so a real 400 MHz spectrum may show that CH₂ as a complex multiplet rather than a clean quintet.

</details>

### Part C — real spectra from SDBS (30 min)

Open [SDBS](https://sdbs.db.aist.go.jp/), accept the disclaimer, and search by compound name for `bromoethane`, `2-chloropropane` and `1-nitropropane` (if a name gives no hit, try a wildcard such as `%bromoethane` or a synonym such as `ethyl bromide`). Open each ¹H NMR spectrum. For each signal write δ, integration, multiplicity, J and assignment.

<details><summary>What you should find</summary>

- Bromoethane: quartet near 3.4 (2H) and triplet near 1.7 (3H), same J of about 7 Hz.
- 2-Chloropropane: septet near 4.1 (1H) and doublet near 1.5 (6H), J about 6.5 Hz.
- 1-Nitropropane: triplet near 4.4 (2H), sextet-like multiplet near 2.0 (2H), triplet near 1.0 (3H).

Small differences from the lab values (a few hundredths of a ppm) are normal: they depend on solvent, concentration and field.

</details>

## Common mistakes

- Counting the protons of the signal itself when applying n+1. A CH₂ next to a CH₃ is a quartet (3 neighbours), not a triplet.
- Reading integrals as absolute numbers. They are ratios; scale them to the formula.
- Expecting OH and NH protons to split their neighbours or sit at a fixed shift. They usually exchange: broad, movable, unsplit.
- Treating a second-order multiplet as first order. If the lines lean towards a partner signal and the count is wrong, compare Δν with J.
- Forgetting symmetry. 1,4-Dichlorobenzene has four aromatic H but only one signal.

## Key takeaways

- Every signal gives three numbers: δ (environment), integral (how many H), multiplicity and J (how many neighbours, and who couples to whom).
- Electronegative atoms, C=O, aromatic rings and C=C shift protons downfield.
- n equivalent neighbours give n+1 lines with Pascal heights; partners share J.
- Ethyl = 3H t + 2H q; isopropyl = 6H d + 1H septet.
- The simple rules need Δν/J above about 10; higher fields make spectra more first order.

## Sources

- [OpenStax Organic Chemistry, 13.2 The Nature of NMR Absorptions](https://openstax.org/books/organic-chemistry/pages/13-2-the-nature-of-nmr-absorptions) — spin, field and shielding.
- [OpenStax Organic Chemistry, 13.4 Chemical Shifts in 1H NMR Spectroscopy](https://openstax.org/books/organic-chemistry/pages/13-4-chemical-shifts-in-1h-nmr-spectroscopy) — shift ranges.
- [OpenStax Organic Chemistry, 13.6 Spin-Spin Splitting in 1H NMR Spectra](https://openstax.org/books/organic-chemistry/pages/13-6-spin-spin-splitting-in-1h-nmr-spectra) — n+1 rule and coupling constants.
- [OpenStax Organic Chemistry, 13.7 1H NMR Spectroscopy and Proton Equivalence](https://openstax.org/books/organic-chemistry/pages/13-7-1h-nmr-spectroscopy-and-proton-equivalence) — equivalence test.
- [Hans Reich, NMR Spectroscopy collection](https://organicchemistrydata.org/hansreich/resources/nmr/) — shift and coupling tables, second-order spectra.
- [NIST CODATA 2022: proton gyromagnetic ratio over 2π](https://physics.nist.gov/cgi-bin/cuu/Value?gammapbar) — 42.577 MHz/T.
- [SDBS (AIST)](https://sdbs.db.aist.go.jp/) — real ¹H spectra of bromoethane, 2-chloropropane and 1-nitropropane, searched by name.
