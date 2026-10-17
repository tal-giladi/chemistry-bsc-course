---
id: "31.4"
module: 31
minutes: 22
practice_minutes: 75
prerequisites: ["31.3", "17.2", "17.3", "17.4", "20.3"]
objectives:
  - Explain why calculated harmonic frequencies differ from measured fundamentals and fit a least-squares scale factor that corrects them.
  - Predict which calculated modes are IR active and turn a list of frequencies and intensities into a broadened spectrum to compare with a measured one.
  - Convert calculated NMR shieldings into chemical shifts with a TMS reference computed at the same level, and judge the size of the remaining errors.
volatility: implementation
sources:
  - title: "NIST CCCBDB, vibrational frequency scaling factors"
    url: https://cccbdb.nist.gov/vibscalejustx.asp
  - title: "NIST CCCBDB, experimental vibrational frequencies of formaldehyde"
    url: https://cccbdb.nist.gov/exp2x.asp?casno=50000&charge=0
  - title: "NIST Chemistry WebBook, formaldehyde gas-phase IR spectrum"
    url: https://webbook.nist.gov/cgi/cbook.cgi?ID=C50000&Type=IR-SPEC&Index=1
  - title: "ORCA 6.1 manual, 5.18 Vibrational spectroscopy (IR spectrum and orca_mapspc)"
    url: https://www.faccts.de/docs/orca/6.1/manual/contents/spectroscopyproperties/vibrations.html
  - title: "ORCA 6.1 manual, NMR chemical shifts"
    url: https://www.faccts.de/docs/orca/6.1/manual/contents/spectroscopyproperties/nmr.html
  - title: "Lodewyk, Siebert and Tantillo (2012), Computational prediction of 1H and 13C chemical shifts, Chem. Rev. 112, 1839"
    url: https://doi.org/10.1021/cr200106v
  - title: "Fulmer et al. (2010), NMR chemical shifts of trace impurities, Organometallics 29, 2176"
    url: https://doi.org/10.1021/om100106e
last_verified: "2026-10-17"
---

# 31.4 · Calculated IR and NMR spectra versus experiment

The spectra you learned to read in Module 17 can also be calculated, and the comparison between a calculated and a measured spectrum is one of the most common jobs in computational chemistry: it confirms a structure, assigns bands that are hard to assign by eye and tells you which conformer you actually made. This lesson shows what a frequency calculation and an NMR calculation give you, why the raw numbers never match experiment exactly, and how chemists correct and compare them honestly. You will calculate the IR spectrum of formaldehyde with xtb and ORCA and the 13C and 1H shifts of acetone with ORCA.

## Why it matters

A synthesis gives a compound whose IR spectrum shows a strong band at 1712 cm⁻¹ and a weaker one at 1745 cm⁻¹. Is the second band a second carbonyl group, an impurity, or an overtone? Two candidate structures, each calculated with one frequency job, answer it in half an hour, but only if you know that a calculated carbonyl stretch is expected to be some 3–5 % too high, how to correct for it and how large the remaining scatter is. NMR is the same story: a calculated 13C shift that disagrees with experiment by 2 ppm may be perfectly normal, while 10 ppm means the structure or the conformer is wrong.

## Core ideas

> [!NOTE]
> The harmonic approximation, scale factors and the shielding-to-shift conversion are stable ideas. Numbers were checked on 2026-10-17: experimental fundamentals and scale factors from the NIST CCCBDB, acetone shifts from Fulmer et al. (2010), ORCA keywords and output tables from the ORCA 6.1 manual. Scale factors depend on the method and basis; always use one fitted for your level.

### What a frequency calculation gives, and what it leaves out

A frequency calculation diagonalises the mass-weighted Hessian ([28.1](../module-28/lesson-01.md)) and returns $3N - 6$ (or $3N - 5$ for linear molecules) **harmonic** wavenumbers $\omega$. A real molecule sits in an anharmonic well, and its measured fundamental band $\nu$ lies below $\omega$. For a diatomic you met the correction in [12.4](../module-12/lesson-04.md) and [20.3](../module-20/lesson-03.md): $\nu = \omega - 2\omega x_e$. For water the "experimental harmonic" values are 3832, 1649 and 3943 cm⁻¹, while the fundamentals you actually see are 3657, 1595 and 3756 cm⁻¹: the O–H stretches drop by about 180 cm⁻¹, nearly 5 %.

On top of anharmonicity comes the method error. HF overestimates force constants, so its wavenumbers are typically 10 % too high; B3LYP harmonic values are close to experimental harmonic values, so they are mainly too high by the anharmonicity.

### Scale factors

The practical fix is one multiplicative **scale factor** $s$ for each method and basis, fitted to many molecules so that $s\,\omega_\text{calc} \approx \nu_\text{exp}$. Least squares over all pairs gives

$$s = \frac{\sum_i \omega_i \nu_i}{\sum_i \omega_i^2}$$

Published values (CCCBDB): HF/6-31G* 0.899, B3LYP/6-31G* 0.960, B3LYP/cc-pVTZ 0.967. A scale factor removes the systematic part of the error. It cannot remove the random part: individual modes still scatter by tens of cm⁻¹ after scaling, and modes with strong anharmonicity (X–H stretches, floppy torsions) scatter most.

### Intensities and selection rules

The IR intensity of a mode is proportional to the square of the change in dipole moment along it, $(\partial\mu/\partial Q)^2$, and programs report it in km/mol. Modes that do not change the dipole have zero intensity: the symmetric stretch of CO₂ and the A₁ and E modes of methane are IR inactive, exactly as the character tables of [20.6](../module-20/lesson-06.md) predict. xtb marks each mode "YES" or "-" in its `vibspectrum` file; ORCA gives an intensity for each mode in its `IR SPECTRUM` table; inactive modes come out at or near zero.

To compare with a measured spectrum, put a line shape on each stick, usually a Lorentzian or Gaussian of 10–20 cm⁻¹ full width at half maximum, and sum. ORCA's `orca_mapspc` does this; the lab's `comp31.lorentzian` does it in Python. Compare with a spectrum of the same phase: calculations here are for isolated molecules, so gas-phase spectra (NIST WebBook) are the fair reference. In liquids, hydrogen bonding moves O–H and N–H stretches down by 100–300 cm⁻¹.

### NMR: shieldings, not shifts

An NMR calculation gives the **shielding** $\sigma$ of each nucleus: how much the electrons reduce the magnetic field at that nucleus, in ppm. ORCA computes it with gauge-including atomic orbitals (GIAO) when you add the keyword `NMR`. Spectrometers report the **chemical shift** relative to tetramethylsilane (TMS), so you calculate TMS at exactly the same level and subtract:

$$\delta_i = \sigma_\text{TMS} - \sigma_i$$

A more shielded nucleus has a larger $\sigma$ and a smaller $\delta$. Average over chemically equivalent nuclei (the three H of a rotating methyl group) and, for flexible molecules, Boltzmann-average over conformers ([31.2](lesson-02.md)). Use a basis made for shieldings, such as pcSseg-1 or pcSseg-2. With a hybrid functional on a good geometry, 13C shifts typically land within a few ppm and 1H shifts within a few tenths of a ppm; fitting a straight line of calculated against measured shifts for a set of known compounds (the approach reviewed by Lodewyk, Siebert and Tantillo) removes most of the systematic part. The shift ranges you learned in [17.3](../module-17/lesson-03.md) and [17.4](../module-17/lesson-04.md) are your sanity check.

## Worked example

### 1. Fit a scale factor for water

B3LYP/def2-TZVP harmonic wavenumbers of water (reference values from `reference_water.csv`) are 1616.8, 3785.3 and 3890.5 cm⁻¹. The measured fundamentals are 1595, 3657 and 3756 cm⁻¹.

1. Numerator: $1616.8 \times 1595 + 3785.3 \times 3657 + 3890.5 \times 3756 = 3.1034\times10^7$.
2. Denominator: $1616.8^2 + 3785.3^2 + 3890.5^2 = 3.2079\times10^7$.
3. $s = 0.9674$. Scaled values: 1564, 3662 and 3764 cm⁻¹; errors −31, +5 and +8 cm⁻¹.
4. RMS error: 108 cm⁻¹ unscaled, 19 cm⁻¹ scaled.

The fitted 0.967 is close to CCCBDB's general B3LYP factors (0.960–0.967): most of the correction here is anharmonicity. The same fit with HF/def2-SVP gives $s = 0.885$, a sign of the extra method error. Note what scaling cannot do: it pulls the stretches into line, but the bend is now 31 cm⁻¹ too low, because one factor cannot fit modes that are anharmonic to different degrees.

### 2. From shieldings to a shift

The arithmetic, with round illustrative numbers (not a real calculation): suppose a calculation gives the TMS carbons a shielding of 185.0 ppm and a carbonyl carbon −20.0 ppm at the same level. Then $\delta = 185.0 - (-20.0) = 205.0$ ppm. A methyl carbon at 154.0 ppm gives $\delta = 31.0$ ppm. If TMS had been calculated with a different functional, its shielding might be 2–5 ppm different and every shift would move by that amount: always use one level for the reference and the molecule.

## Hands-on

What you need: xtb and ORCA, Python with the course packages, the [Module 31 lab folder](../../labs/module-31/), the [spectrum assignment template](../../templates/spectrum-assignment.md) and a [notebook page](../../templates/notebook-page.md). Time: about 75 minutes, about 15 of them waiting for ORCA.

### Part A — formaldehyde IR with xtb (15 min)

1. Open `lesson04_spectra.py` and complete `scale_factor()` with the least-squares formula above.
2. Run `py lesson04_spectra.py`. It optimises formaldehyde with `xtb --ohess`, pairs the six calculated modes with the six measured fundamentals in order of wavenumber, prints the table with your scale factor and plots `runs/lesson04_ir.png` (calculated Lorentzians, measured sticks from the CCCBDB intensities).
3. Open the measured gas-phase spectrum on the [NIST WebBook](https://webbook.nist.gov/cgi/cbook.cgi?ID=C50000&Type=IR-SPEC&Index=1) and compare by eye: the strong C=O stretch near 1746 cm⁻¹ and the two C–H stretches near 2800 cm⁻¹.

How you know it worked (xtb 6.7.1, checked 2026-10-17; printout in `expected/31.4_spectra.txt`): calculated 1085.6, 1202.7, 1489.6, 1805.5, 2790.1, 2836.6 cm⁻¹; scale factor 1.0020; RMS error 46 cm⁻¹ both before and after scaling. GFN2-xTB needs almost no scaling for this molecule, but its random errors are large: the CH₂ wag is 79 cm⁻¹ too low and the C=O stretch 63 cm⁻¹ too high.

### Part B — formaldehyde IR with ORCA (15 min)

Run `orca 04_formaldehyde_ir.inp > 04_formaldehyde_ir.out` in `orca/` (r2SCAN-3c optimisation plus analytic frequencies, about a minute), then `orca_mapspc 04_formaldehyde_ir.out ir -w15` to write a broadened spectrum. Rerun `py lesson04_spectra.py`: it now adds the r2SCAN-3c curve and its own scale factor. Expect a scale factor below 1, since r2SCAN-3c gives harmonic values, and a smaller scatter than xtb. This ORCA job was not run when the module was written, so no reference numbers are given; write yours in your notebook.

### Part C — acetone NMR with ORCA (35 min)

1. In `orca/`, run in this order: `04_acetone_opt.inp`, `04_tms_opt.inp` (r2SCAN-3c geometries), then `04_acetone_nmr.inp` and `04_tms_nmr.inp` (B3LYP/pcSseg-1 GIAO shieldings on those geometries). Each takes from under a minute to a few minutes.
2. In `lesson04_spectra.py` complete `shift()` and `mean_shielding()` (average the isotropic shieldings of one element, optionally only over chosen atom indices; in `acetone.xyz` atom 1 is the carbonyl carbon and atoms 0 and 2 are the methyl carbons).
3. Rerun the script. It prints σ(TMS) for C and H and the three acetone shifts next to the measured values in CDCl₃: 207.07 ppm (C=O), 30.92 ppm (CH₃) and 2.17 ppm (CH₃).

How you know it worked: the carbonyl carbon comes out near 200–215 ppm, the methyl carbon near 25–35 ppm and the methyl hydrogens near 2 ppm. Errors of a few ppm for carbon and a few tenths of a ppm for hydrogen are normal for this level and a gas-phase model of a CDCl₃ measurement. A shift that is tens of ppm off means a mismatch, most often a TMS reference from a different level. The ORCA NMR jobs were not run when the module was written.

<details><summary>Reference solution and interpretation</summary>

```python
def scale_factor(pairs):
    num = sum(w * e for w, e in pairs)
    den = sum(w * w for w, _ in pairs)
    return num / den

def shift(sigma_ref, sigma):
    return sigma_ref - sigma

def mean_shielding(shieldings, element, indices=None):
    vals = [v for (i, el), v in shieldings.items()
            if el == element and (indices is None or i in indices)]
    return sum(vals) / len(vals)
```

Full code: `lesson04_spectra_solution.py`. Pairing by order works for formaldehyde because no two calculated modes swap places relative to experiment; for larger molecules, assign modes by symmetry and by looking at the animation in Avogadro before pairing. For the spectrum assignment template, list each measured band, its calculated partner, the description from `exp_fundamentals.csv`, and the error after scaling.

</details>

## Common mistakes

- Comparing raw harmonic wavenumbers with measured bands and concluding the method is bad. Scale first, with a factor for your method and basis.
- Using a scale factor from a different method or basis. HF needs about 0.90, B3LYP about 0.96–0.97, and GFN2-xTB is close to 1.0 on average for small molecules but with large scatter.
- Comparing an isolated-molecule calculation with a solid or liquid spectrum, especially for O–H and N–H stretches.
- Computing TMS at a different level from the molecule, or forgetting the minus sign: $\delta = \sigma_\text{TMS} - \sigma$.
- Reading shifts of individual methyl hydrogens. They exchange by rotation; average them, and average over conformers for flexible molecules.
- Pairing modes blindly by order in a bigger molecule. Check symmetry labels and animations first.

## Key takeaways

- Calculated frequencies are harmonic; measured fundamentals are lower because of anharmonicity, and HF adds a further 10 % or so.
- One least-squares scale factor per level, $s = \sum\omega\nu / \sum\omega^2$, removes the systematic error; the random scatter (tens of cm⁻¹) remains.
- IR intensity follows the dipole derivative; symmetric modes that keep the dipole unchanged are inactive.
- NMR programs give shieldings; shifts are $\sigma_\text{TMS} - \sigma$ with TMS at the same level, averaged over equivalent nuclei and conformers.
- Compare like with like: gas-phase calculations with gas-phase IR spectra, and expect solvent effects in NMR.

## Sources

- [NIST CCCBDB, vibrational scaling factors](https://cccbdb.nist.gov/vibscalejustx.asp) — HF/6-31G* 0.899, B3LYP/6-31G* 0.960, B3LYP/cc-pVTZ 0.967.
- [NIST CCCBDB, formaldehyde](https://cccbdb.nist.gov/exp2x.asp?casno=50000&charge=0) — six experimental fundamentals and IR intensities; water harmonic and fundamental values from the [water page](https://cccbdb.nist.gov/exp2x.asp?casno=7732185&charge=0).
- [NIST Chemistry WebBook, formaldehyde IR spectrum](https://webbook.nist.gov/cgi/cbook.cgi?ID=C50000&Type=IR-SPEC&Index=1) — measured gas-phase spectrum for comparison.
- [ORCA 6.1 manual, Vibrational spectroscopy](https://www.faccts.de/docs/orca/6.1/manual/contents/spectroscopyproperties/vibrations.html) — the IR SPECTRUM table and `orca_mapspc`.
- [ORCA 6.1 manual, NMR](https://www.faccts.de/docs/orca/6.1/manual/contents/spectroscopyproperties/nmr.html) — the `NMR` keyword, GIAO shieldings for all nuclei, pcSseg-n basis sets.
- [Lodewyk, Siebert and Tantillo, Chem. Rev. 112, 1839 (2012)](https://doi.org/10.1021/cr200106v) — review of calculated 1H and 13C shifts, typical errors and linear scaling.
- [Fulmer et al., Organometallics 29, 2176 (2010)](https://doi.org/10.1021/om100106e) — acetone in CDCl₃: 13C 207.07 and 30.92 ppm, 1H 2.17 ppm.
