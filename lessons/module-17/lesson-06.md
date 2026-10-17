---
id: "17.6"
module: 17
minutes: 15
practice_minutes: 120
prerequisites: ["17.5"]
objectives:
  - Identify unknown organic compounds from real MS, IR, ¹H and ¹³C spectra, working through the full workflow for each.
  - Record each solution on the spectrum assignment template, with the decisive observation against every rejected candidate.
  - Check answers with a script and analyse the pattern of your own mistakes across 50 unknowns.
volatility: implementation
sources:
  - title: "NIST Chemistry WebBook, SRD 69"
    url: https://webbook.nist.gov/chemistry/
  - title: "SDBS Spectral Database for Organic Compounds (AIST)"
    url: https://sdbs.db.aist.go.jp/
  - title: "SDBS help: how to search (no CAS search; name, formula, SDBS number)"
    url: https://sdbs.db.aist.go.jp/Htmls/help_eng.html
  - title: "SDBS disclaimer and terms of use"
    url: https://sdbs.db.aist.go.jp/Htmls/disclaimer_eng.html
  - title: "PubChem"
    url: https://pubchem.ncbi.nlm.nih.gov/
last_verified: "2026-10-17"
---

# 17.6 · Project: 50 unknowns from real SDBS spectra

This is the module's practical piece. You will identify 50 organic compounds from their real spectra: electron-ionisation mass spectra and gas-phase IR from the NIST Chemistry WebBook, and ¹H NMR, ¹³C NMR and liquid-phase IR from SDBS, the free spectral database of Japan's National Institute of Advanced Industrial Science and Technology (AIST). The unknowns come in three tiers, from small one-group molecules to isomers that only careful reading separates. Each answer, with the evidence that proves it, is hidden in a details block. Plan on spreading the project over several weeks: five unknowns per sitting is a good pace.

## Why it matters

Reading spectra is a skill like reading a language: rules help, but fluency comes from volume. Chemists who solve spectra fast have simply seen hundreds of them. Fifty unknowns, worked properly, is the minimum that turns the rules of [17.1](lesson-01.md) to [17.4](lesson-04.md) into recognition: you will start to see "ethyl group", "para-disubstituted ring" or "methyl ketone" before you have consciously reasoned it out. This is also exactly the exercise that Technion's organic chemistry courses ask for in their spectroscopy problem sets, here with real data instead of textbook drawings.

## Core ideas

> [!NOTE]
> The method is stable; the databases are not. Every compound's CAS number, formula and NIST spectra were checked on 2026-10-17 against PubChem and the NIST WebBook. SDBS asks each user to accept its disclaimer before every session and forbids automated downloading, so its pages were not fetched for this course: you search SDBS by compound name, by hand. SDBS has no CAS-number search (its help page says so). Never copy SDBS data into files you share; SDBS asks you to cite it as "SDBS, https://sdbs.db.aist.go.jp/, AIST, date of access" when you use its data.

### How the project works

Every public database shows the compound name next to its spectra, and SDBS can only be searched by name or formula. So each unknown is solved in two phases:

1. **Phase 1, blind (MS + IR).** You get the formula, the CAS number and links that jump straight to the NIST mass spectrum and gas-phase IR spectrum. The name is at the top of the NIST page; the link lands below it. Do not scroll up. Press <kbd>F11</kbd> (full screen) so the browser tab title, which also shows the name, is hidden. From the formula, DBE, fragments and IR bands, write down **every** candidate structure.
2. **Phase 2, NMR (SDBS).** Open the details block for that unknown: it gives the name to search in SDBS and the answer. Open the ¹H and ¹³C spectra (and the liquid IR) in SDBS. Even though you now know the answer, assign **every** NMR signal on the template and write which observation rules out each of your other candidates. Score yourself on phase 1: was the answer on your candidate list, and was it your first choice?

If you have a study partner, the partner can open SDBS for you and show you only the spectra; then the whole project is blind.

### What counts as solved

An unknown is solved when your [spectrum assignment sheet](../../templates/spectrum-assignment.md) has: the formula and DBE; at least three assigned MS peaks (including M⁺· or a reason it is missing); the diagnostic IR bands; every ¹H signal with δ, integral, multiplicity and assignment; every ¹³C line assigned; all candidates with the evidence against each; and the one observation that proves the answer.

### Searching SDBS by name

SDBS matches names exactly, except for the wildcard `%`. If a name gives no hit, try `%name` (to allow a prefix such as "n-"), a synonym given in the details block, or a formula search (for example `C5H10O`) and pick the compound from the list. Choose the record whose formula matches; several compounds can share a name fragment.

## Worked example

### A demonstration unknown (not one of the 50): C₃H₆O₂, CAS 79-20-9

1. Formula C₃H₆O₂, DBE 1: one C=O or one ring.
2. NIST MS ([link](https://webbook.nist.gov/cgi/cbook.cgi?ID=C79209&Mask=200#Mass-Spec)): M⁺· 74 (about 25 %), base 43, a peak at 59. 43 suggests CH₃CO⁺; 74 − 15 = 59 is loss of a methyl.
3. NIST IR ([link](https://webbook.nist.gov/cgi/cbook.cgi?ID=C79209&Mask=80#IR-Spec), gas phase): C=O near 1780 (in the liquid it would be near 1745) and a strong C–O band near 1250; no O–H.
4. Candidates with one C=O and no O–H: methyl acetate (CH₃COOCH₃) and ethyl formate (HCOOCH₂CH₃). Propanoic acid and hydroxyacetone are out: no O–H band.
5. MS already leans one way: ethyl formate's EI spectrum has its base peak at 31 and no large 43, because it has no CH₃CO group.
6. Phase 2, SDBS (`methyl acetate`): two 3H singlets, near 3.7 (OCH₃) and 2.0 (CH₃C=O); ¹³C lines near 171, 52 and 21. Ethyl formate would show a 1H singlet near 8.0, a quartet and a triplet.
7. Answer: methyl acetate. Decisive observation: two singlets and no splitting at all, with a 3H singlet at 3.7 ppm.

## Hands-on

What you need: a browser, the [spectrum assignment template](../../templates/spectrum-assignment.md) (one copy per unknown, on paper or as a file), Python with the course packages, and the [Module 17 lab folder](../../labs/module-17/) (`unknowns.csv`, `project_answers.csv`, `lesson06_project.py`). Time: about 20–30 minutes per unknown; the project as a whole is 20–25 hours. The `practice_minutes` above covers one sitting of five unknowns.

Steps for each sitting:

1. Pick the next five unknowns. Solve phase 1 for all five before opening any details block.
2. Do phase 2 for each, and finish the template.
3. Write your phase-1 answer (as a SMILES string, see [15.1](../module-15/lesson-01.md)) in `project_answers.csv`, then run the checker from the lab folder:

```bash
py lesson06_project.py
```

The checker compares your SMILES with a hashed key (so it does not reveal answers), and tells you when your structure has the wrong formula.

4. Keep a mistakes log: for each miss, write which step misled you (formula, DBE, MS, IR, ¹³C, ¹H, or not listing a candidate).

How you know it worked: the checker reports each answer as correct; your template for each unknown explains every peak you listed. A good target is 40 of 50 correct in phase 1, and all 50 fully assigned after phase 2.

### Tier 1 — one functional group, up to five carbons (unknowns 1–15)

| No. | Formula | CAS | NIST MS | NIST IR (gas) |
|---|---|---|---|---|
| 1 | C₃H₆O | 67-64-1 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C67641&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C67641&Mask=80#IR-Spec) |
| 2 | C₂H₆O | 64-17-5 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C64175&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C64175&Mask=80#IR-Spec) |
| 3 | C₂H₄O₂ | 64-19-7 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C64197&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C64197&Mask=80#IR-Spec) |
| 4 | C₄H₁₀O | 60-29-7 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C60297&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C60297&Mask=80#IR-Spec) |
| 5 | C₃H₈O | 67-63-0 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C67630&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C67630&Mask=80#IR-Spec) |
| 6 | C₂H₃N | 75-05-8 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C75058&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C75058&Mask=80#IR-Spec) |
| 7 | C₄H₈O₂ | 141-78-6 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C141786&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C141786&Mask=80#IR-Spec) |
| 8 | C₃H₈O | 71-23-8 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C71238&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C71238&Mask=80#IR-Spec) |
| 9 | C₄H₈O | 123-72-8 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C123728&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C123728&Mask=80#IR-Spec) |
| 10 | C₄H₁₀O | 75-65-0 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C75650&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C75650&Mask=80#IR-Spec) |
| 11 | C₃H₆O₂ | 79-09-4 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C79094&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C79094&Mask=80#IR-Spec) |
| 12 | C₄H₈O | 78-93-3 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C78933&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C78933&Mask=80#IR-Spec) |
| 13 | C₄H₈O₂ | 123-91-1 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C123911&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C123911&Mask=80#IR-Spec) |
| 14 | C₄H₈O₂ | 554-12-1 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C554121&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C554121&Mask=80#IR-Spec) |
| 15 | C₄H₁₀O | 78-83-1 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C78831&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C78831&Mask=80#IR-Spec) |

<details><summary>Unknown 1 — SDBS search name and answer</summary>

Search SDBS for `acetone`. Answer: **acetone (propan-2-one)**, `CC(C)=O`. Key evidence: M⁺· 58, base 43 (CH₃CO⁺); ¹³C C=O near 206; one ¹H singlet near 2.1 (6H).

</details>

<details><summary>Unknown 2 — SDBS search name and answer</summary>

Search SDBS for `ethanol`. Answer: **ethanol**, `CCO`. Key evidence: base 31 (CH₂OH⁺), 45; broad O–H; ¹H quartet near 3.7, triplet near 1.2, OH.

</details>

<details><summary>Unknown 3 — SDBS search name and answer</summary>

Search SDBS for `acetic acid`. Answer: **acetic acid (ethanoic acid)**, `CC(=O)O`. Key evidence: M⁺· 60, 45, 43; very broad O–H and C=O near 1710; ¹H singlets near 2.1 (3H) and 11–12 (1H).

</details>

<details><summary>Unknown 4 — SDBS search name and answer</summary>

Search SDBS for `diethyl ether`. Answer: **diethyl ether (ethoxyethane)**, `CCOCC`. Key evidence: M⁺· 74, 59, base 31; no O–H, no C=O, strong C–O near 1120; ¹H quartet near 3.5, triplet near 1.2; two ¹³C lines.

</details>

<details><summary>Unknown 5 — SDBS search name and answer</summary>

Search SDBS for `2-propanol` or `isopropyl alcohol`. Answer: **propan-2-ol**, `CC(C)O`. Key evidence: base 45 (CH₃CH=OH⁺); broad O–H; ¹H septet near 4.0 (1H), doublet near 1.2 (6H); two ¹³C lines.

</details>

<details><summary>Unknown 6 — SDBS search name and answer</summary>

Search SDBS for `acetonitrile`. Answer: **acetonitrile (ethanenitrile)**, `CC#N`. Key evidence: M⁺· 41, odd (one N); C≡N near 2250; one ¹H singlet near 2.0; ¹³C near 117 (CN) and 2.

</details>

<details><summary>Unknown 7 — SDBS search name and answer</summary>

Search SDBS for `ethyl acetate`. Answer: **ethyl acetate (ethyl ethanoate)**, `CCOC(C)=O`. Key evidence: M⁺· 88, base 43, 61, 70; C=O near 1740 + C–O near 1240; ¹H quartet 4.1, singlet 2.0, triplet 1.3.

</details>

<details><summary>Unknown 8 — SDBS search name and answer</summary>

Search SDBS for `1-propanol`. Answer: **propan-1-ol**, `CCCO`. Key evidence: base 31 (CH₂OH⁺, a primary alcohol); ¹H triplet near 3.6, sextet near 1.6, triplet near 0.9; three ¹³C lines.

</details>

<details><summary>Unknown 9 — SDBS search name and answer</summary>

Search SDBS for `butanal` or `butyraldehyde`. Answer: **butanal**, `CCCC=O`. Key evidence: M⁺· 72, base 44 (McLafferty of an aldehyde); C=O near 1730 with 2720/2820; ¹H triplet near 9.8 (small J); ¹³C near 202.

</details>

<details><summary>Unknown 10 — SDBS search name and answer</summary>

Search SDBS for `2-methyl-2-propanol` or `tert-butyl alcohol`. Answer: **2-methylpropan-2-ol**, `CC(C)(C)O`. Key evidence: no M⁺·, base 59 (M − CH₃); broad O–H; ¹H 9H singlet near 1.3 + OH; two ¹³C lines (C–O near 69).

</details>

<details><summary>Unknown 11 — SDBS search name and answer</summary>

Search SDBS for `propionic acid`. Answer: **propanoic acid**, `CCC(=O)O`. Key evidence: M⁺· 74 (base), 45, 29; very broad O–H; ¹H quartet near 2.4, triplet near 1.2, broad near 11.5; ¹³C near 181.

</details>

<details><summary>Unknown 12 — SDBS search name and answer</summary>

Search SDBS for `2-butanone` or `methyl ethyl ketone`. Answer: **butan-2-one**, `CCC(C)=O`. Key evidence: M⁺· 72, base 43, 57, 29; C=O near 1715; ¹H quartet 2.4, singlet 2.1, triplet 1.0; ¹³C near 209.

</details>

<details><summary>Unknown 13 — SDBS search name and answer</summary>

Search SDBS for `1,4-dioxane`. Answer: **1,4-dioxane**, `C1COCCO1`. Key evidence: DBE 1 with no C=O or C=C: a ring. M⁺· 88, 58, 28; strong C–O; one ¹H singlet near 3.7 (8H); one ¹³C line near 67.

</details>

<details><summary>Unknown 14 — SDBS search name and answer</summary>

Search SDBS for `methyl propionate`. Answer: **methyl propanoate**, `CCC(=O)OC`. Key evidence: M⁺· 88, 57 (C₂H₅CO⁺), 59 (COOCH₃⁺); ester C=O; ¹H singlet near 3.7 (OCH₃), quartet near 2.3, triplet near 1.1.

</details>

<details><summary>Unknown 15 — SDBS search name and answer</summary>

Search SDBS for `2-methyl-1-propanol` or `isobutyl alcohol`. Answer: **2-methylpropan-1-ol**, `CC(C)CO`. Key evidence: M⁺· weak, base 43, 31; broad O–H; ¹H doublet near 3.4 (2H), multiplet near 1.75 (1H), doublet near 0.9 (6H); three ¹³C lines.

</details>

### Tier 2 — aromatic rings, halogens and nitrogen (unknowns 16–35)

| No. | Formula | CAS | NIST MS | NIST IR (gas) |
|---|---|---|---|---|
| 16 | C₇H₈ | 108-88-3 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C108883&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C108883&Mask=80#IR-Spec) |
| 17 | C₆H₆O | 108-95-2 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C108952&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C108952&Mask=80#IR-Spec) |
| 18 | C₆H₅Br | 108-86-1 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C108861&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C108861&Mask=80#IR-Spec) |
| 19 | C₇H₆O | 100-52-7 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C100527&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C100527&Mask=80#IR-Spec) |
| 20 | C₆H₁₅N | 121-44-8 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C121448&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C121448&Mask=80#IR-Spec) |
| 21 | C₇H₈O | 100-66-3 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C100663&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C100663&Mask=80#IR-Spec) |
| 22 | C₃H₇Br | 75-26-3 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C75263&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C75263&Mask=80#IR-Spec) |
| 23 | C₈H₈O | 98-86-2 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C98862&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C98862&Mask=80#IR-Spec) |
| 24 | C₅H₅N | 110-86-1 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C110861&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C110861&Mask=80#IR-Spec) |
| 25 | C₇H₆O₂ | 65-85-0 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C65850&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C65850&Mask=80#IR-Spec) |
| 26 | C₆H₅Cl | 108-90-7 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C108907&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C108907&Mask=80#IR-Spec) |
| 27 | C₆H₇N | 62-53-3 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C62533&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C62533&Mask=80#IR-Spec) |
| 28 | C₈H₁₀ | 106-42-3 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C106423&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C106423&Mask=80#IR-Spec) |
| 29 | C₄H₉Br | 109-65-9 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C109659&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C109659&Mask=80#IR-Spec) |
| 30 | C₇H₅N | 100-47-0 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C100470&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C100470&Mask=80#IR-Spec) |
| 31 | C₃H₇NO | 68-12-2 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C68122&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C68122&Mask=80#IR-Spec) |
| 32 | C₈H₁₀ | 100-41-4 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C100414&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C100414&Mask=80#IR-Spec) |
| 33 | C₇H₈O | 100-51-6 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C100516&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C100516&Mask=80#IR-Spec) |
| 34 | C₈H₈O₂ | 93-58-3 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C93583&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C93583&Mask=80#IR-Spec) |
| 35 | C₇H₈O | 106-44-5 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C106445&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C106445&Mask=80#IR-Spec) |

<details><summary>Unknown 16 — SDBS search name and answer</summary>

Search SDBS for `toluene`. Answer: **toluene (methylbenzene)**, `Cc1ccccc1`. Key evidence: M⁺· 92, base 91 (tropylium); DBE 4; ¹H about 7.2 (5H) and singlet near 2.35 (3H); five ¹³C lines.

</details>

<details><summary>Unknown 17 — SDBS search name and answer</summary>

Search SDBS for `phenol`. Answer: **phenol**, `Oc1ccccc1`. Key evidence: M⁺· 94 (base), 66 (M − CO); broad O–H; ¹H 6.8–7.3 (5H) + OH; four ¹³C lines, C–O near 155.

</details>

<details><summary>Unknown 18 — SDBS search name and answer</summary>

Search SDBS for `bromobenzene`. Answer: **bromobenzene**, `Brc1ccccc1`. Key evidence: 156/158 in 1 : 1 (one Br), base 77 (C₆H₅⁺); five aromatic H; four ¹³C lines, C–Br near 122.

</details>

<details><summary>Unknown 19 — SDBS search name and answer</summary>

Search SDBS for `benzaldehyde`. Answer: **benzaldehyde**, `O=Cc1ccccc1`. Key evidence: M⁺· 106, 105 (M − H), base 77; C=O near 1700 with 2740/2820; ¹H singlet near 10.0; ¹³C near 192.

</details>

<details><summary>Unknown 20 — SDBS search name and answer</summary>

Search SDBS for `triethylamine`. Answer: **triethylamine (N,N-diethylethanamine)**, `CCN(CC)CC`. Key evidence: M⁺· 101, odd (one N); base 86 (alpha-cleavage, M − CH₃); no N–H; ¹H quartet near 2.5 (6H), triplet near 1.0 (9H).

</details>

<details><summary>Unknown 21 — SDBS search name and answer</summary>

Search SDBS for `anisole`. Answer: **anisole (methoxybenzene)**, `COc1ccccc1`. Key evidence: M⁺· 108 (base), 78, 65; strong C–O near 1250; ¹H singlet near 3.8 (3H) + 5 aromatic H; ¹³C near 160 and 55.

</details>

<details><summary>Unknown 22 — SDBS search name and answer</summary>

Search SDBS for `2-bromopropane`. Answer: **2-bromopropane**, `CC(C)Br`. Key evidence: 122/124 in 1 : 1 (one Br), base 43 (C₃H₇⁺); ¹H septet near 4.2 (1H), doublet near 1.7 (6H); two ¹³C lines.

</details>

<details><summary>Unknown 23 — SDBS search name and answer</summary>

Search SDBS for `acetophenone`. Answer: **acetophenone (1-phenylethan-1-one)**, `CC(=O)c1ccccc1`. Key evidence: M⁺· 120, base 105 (C₆H₅CO⁺), 77; conjugated C=O near 1685; ¹H singlet near 2.6 + 5 aromatic H; ¹³C near 198.

</details>

<details><summary>Unknown 24 — SDBS search name and answer</summary>

Search SDBS for `pyridine`. Answer: **pyridine**, `c1ccncc1`. Key evidence: M⁺· 79 (base), odd (one N); DBE 4, aromatic; ¹H three signals near 8.6 (2H), 7.6 (1H), 7.2 (2H); three ¹³C lines near 150, 136, 124.

</details>

<details><summary>Unknown 25 — SDBS search name and answer</summary>

Search SDBS for `benzoic acid`. Answer: **benzoic acid**, `OC(=O)c1ccccc1`. Key evidence: M⁺· 122, base 105, 77; very broad O–H with C=O near 1685; ¹H broad near 12–13 + 5 aromatic H; ¹³C near 172.

</details>

<details><summary>Unknown 26 — SDBS search name and answer</summary>

Search SDBS for `chlorobenzene`. Answer: **chlorobenzene**, `Clc1ccccc1`. Key evidence: 112/114 in 3 : 1 (one Cl), 77; five aromatic H; four ¹³C lines, C–Cl near 134.

</details>

<details><summary>Unknown 27 — SDBS search name and answer</summary>

Search SDBS for `aniline`. Answer: **aniline (benzenamine)**, `Nc1ccccc1`. Key evidence: M⁺· 93 (base), odd (one N), 66; two N–H bands near 3430 and 3350; ¹H 6.6–7.2 (5H) + broad NH₂; C–N near 146.

</details>

<details><summary>Unknown 28 — SDBS search name and answer</summary>

Search SDBS for `p-xylene`. Answer: **1,4-dimethylbenzene**, `Cc1ccc(C)cc1`. Key evidence: M⁺· 106, base 91; ¹H two singlets, near 7.05 (4H) and 2.3 (6H); three ¹³C lines.

</details>

<details><summary>Unknown 29 — SDBS search name and answer</summary>

Search SDBS for `1-bromobutane` or `butyl bromide`. Answer: **1-bromobutane**, `CCCCBr`. Key evidence: 136/138 in 1 : 1, small; base 57 (C₄H₉⁺); ¹H triplet near 3.4 (2H), two multiplets, triplet near 0.9; four ¹³C lines.

</details>

<details><summary>Unknown 30 — SDBS search name and answer</summary>

Search SDBS for `benzonitrile`. Answer: **benzonitrile**, `N#Cc1ccccc1`. Key evidence: M⁺· 103 (base), odd (one N), 76; conjugated C≡N near 2230; 5 aromatic H; ¹³C CN near 119.

</details>

<details><summary>Unknown 31 — SDBS search name and answer</summary>

Search SDBS for `N,N-dimethylformamide`. Answer: **N,N-dimethylformamide (DMF)**, `CN(C)C=O`. Key evidence: M⁺· 73 (base), odd; amide C=O near 1675, no N–H; ¹H singlet near 8.0 (1H) and two 3H singlets near 2.9 (slow C–N rotation); ¹³C near 162.

</details>

<details><summary>Unknown 32 — SDBS search name and answer</summary>

Search SDBS for `ethylbenzene`. Answer: **ethylbenzene**, `CCc1ccccc1`. Key evidence: M⁺· 106, base 91; ¹H quartet near 2.65 (2H), triplet near 1.25 (3H), 5 aromatic H; six ¹³C lines.

</details>

<details><summary>Unknown 33 — SDBS search name and answer</summary>

Search SDBS for `benzyl alcohol`. Answer: **phenylmethanol (benzyl alcohol)**, `OCc1ccccc1`. Key evidence: M⁺· 108, base 79, 107, 77; broad O–H; ¹H singlet near 4.6 (2H) + 5 aromatic H + OH; ¹³C near 65.

</details>

<details><summary>Unknown 34 — SDBS search name and answer</summary>

Search SDBS for `methyl benzoate`. Answer: **methyl benzoate**, `COC(=O)c1ccccc1`. Key evidence: M⁺· 136, base 105, 77; ester C=O near 1725; ¹H singlet near 3.9 (3H), 5 aromatic H; ¹³C near 167 and 52.

</details>

<details><summary>Unknown 35 — SDBS search name and answer</summary>

Search SDBS for `p-cresol`. Answer: **4-methylphenol**, `Cc1ccc(O)cc1`. Key evidence: M⁺· 108, base 107; broad O–H; ¹H two 2H doublets near 7.0 and 6.75 (para), singlet near 2.25; five ¹³C lines.

</details>

### Tier 3 — rings, alkenes, alkynes and close isomers (unknowns 36–50)

| No. | Formula | CAS | NIST MS | NIST IR (gas) |
|---|---|---|---|---|
| 36 | C₆H₁₀O | 108-94-1 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C108941&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C108941&Mask=80#IR-Spec) |
| 37 | C₆H₁₂ | 592-41-6 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C592416&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C592416&Mask=80#IR-Spec) |
| 38 | C₉H₁₂ | 98-82-8 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C98828&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C98828&Mask=80#IR-Spec) |
| 39 | C₅H₁₀O | 96-22-0 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C96220&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C96220&Mask=80#IR-Spec) |
| 40 | C₆H₁₂O | 108-93-0 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C108930&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C108930&Mask=80#IR-Spec) |
| 41 | C₆H₁₀ | 693-02-7 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C693027&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C693027&Mask=80#IR-Spec) |
| 42 | C₅H₁₀O | 107-87-9 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C107879&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C107879&Mask=80#IR-Spec) |
| 43 | C₅H₁₀O₂ | 105-37-3 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C105373&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C105373&Mask=80#IR-Spec) |
| 44 | C₆H₁₀ | 110-83-8 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C110838&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C110838&Mask=80#IR-Spec) |
| 45 | C₆H₁₂O | 108-10-1 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C108101&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C108101&Mask=80#IR-Spec) |
| 46 | C₈H₁₀O | 60-12-8 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C60128&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C60128&Mask=80#IR-Spec) |
| 47 | C₅H₈O₂ | 80-62-6 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C80626&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C80626&Mask=80#IR-Spec) |
| 48 | C₇H₇NO₂ | 99-99-0 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C99990&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C99990&Mask=80#IR-Spec) |
| 49 | C₉H₁₀O₂ | 93-89-0 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C93890&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C93890&Mask=80#IR-Spec) |
| 50 | C₆H₁₀O₃ | 141-97-9 | [MS](https://webbook.nist.gov/cgi/cbook.cgi?ID=C141979&Mask=200#Mass-Spec) | [IR](https://webbook.nist.gov/cgi/cbook.cgi?ID=C141979&Mask=80#IR-Spec) |

<details><summary>Unknown 36 — SDBS search name and answer</summary>

Search SDBS for `cyclohexanone`. Answer: **cyclohexanone**, `O=C1CCCCC1`. Key evidence: DBE 2: ring + C=O. M⁺· 98, base 55; C=O near 1715; four ¹³C lines, C=O near 212.

</details>

<details><summary>Unknown 37 — SDBS search name and answer</summary>

Search SDBS for `1-hexene`. Answer: **hex-1-ene**, `C=CCCCC`. Key evidence: M⁺· 84, 56, 41; =C–H near 3080, C=C near 1640; ¹H about 5.8 (1H) and 4.95 (2H); six ¹³C lines incl. 139 and 114.

</details>

<details><summary>Unknown 38 — SDBS search name and answer</summary>

Search SDBS for `cumene` or `isopropylbenzene`. Answer: **(propan-2-yl)benzene (cumene)**, `CC(C)c1ccccc1`. Key evidence: M⁺· 120, base 105 (M − CH₃); ¹H septet near 2.9 (1H), doublet near 1.25 (6H), 5 aromatic H.

</details>

<details><summary>Unknown 39 — SDBS search name and answer</summary>

Search SDBS for `3-pentanone` or `diethyl ketone`. Answer: **pentan-3-one**, `CCC(=O)CC`. Key evidence: M⁺· 86, base 57 (C₂H₅CO⁺), 29; ¹H quartet near 2.45 (4H), triplet near 1.05 (6H); three ¹³C lines, C=O near 212.

</details>

<details><summary>Unknown 40 — SDBS search name and answer</summary>

Search SDBS for `cyclohexanol`. Answer: **cyclohexanol**, `OC1CCCCC1`. Key evidence: DBE 1 and no C=O: a ring. M⁺· weak, base 57, 82 (M − H₂O); broad O–H; ¹H multiplet near 3.6 (1H); four ¹³C lines, C–O near 70.

</details>

<details><summary>Unknown 41 — SDBS search name and answer</summary>

Search SDBS for `1-hexyne`. Answer: **hex-1-yne**, `C#CCCCC`. Key evidence: base 67; sharp ≡C–H near 3310 and weak C≡C near 2120; ¹H triplet near 1.95 (≡C–H, J about 2.6 Hz); ¹³C near 84 and 68.

</details>

<details><summary>Unknown 42 — SDBS search name and answer</summary>

Search SDBS for `2-pentanone`. Answer: **pentan-2-one**, `CCCC(C)=O`. Key evidence: M⁺· 86, base 43, 58 (McLafferty), 71; ¹H singlet near 2.1 (3H), triplet 2.4, sextet 1.6, triplet 0.9; five ¹³C lines.

</details>

<details><summary>Unknown 43 — SDBS search name and answer</summary>

Search SDBS for `ethyl propionate`. Answer: **ethyl propanoate**, `CCOC(=O)CC`. Key evidence: M⁺· 102, base 29, 57 (C₂H₅CO⁺); ester C=O; ¹H quartet near 4.1 (OCH₂), quartet near 2.3, two triplets; no singlet.

</details>

<details><summary>Unknown 44 — SDBS search name and answer</summary>

Search SDBS for `cyclohexene`. Answer: **cyclohexene**, `C1=CCCCC1`. Key evidence: DBE 2: ring + C=C. M⁺· 82, base 67, 54 (retro-Diels–Alder); ¹H near 5.7 (2H), 2.0 (4H), 1.6 (4H); three ¹³C lines, 127.

</details>

<details><summary>Unknown 45 — SDBS search name and answer</summary>

Search SDBS for `4-methyl-2-pentanone` or `methyl isobutyl ketone`. Answer: **4-methylpentan-2-one**, `CC(C)CC(C)=O`. Key evidence: M⁺· 100, base 43, 58 (McLafferty), 85; ¹H singlet 2.1 (3H), doublet 2.3 (2H), multiplet 2.1 (1H), doublet 0.9 (6H).

</details>

<details><summary>Unknown 46 — SDBS search name and answer</summary>

Search SDBS for `2-phenylethanol` or `phenethyl alcohol`. Answer: **2-phenylethan-1-ol**, `OCCc1ccccc1`. Key evidence: M⁺· 122, base 91, 92; broad O–H; ¹H two 2H triplets near 3.85 and 2.85, 5 aromatic H; ¹³C near 63 and 39.

</details>

<details><summary>Unknown 47 — SDBS search name and answer</summary>

Search SDBS for `methyl methacrylate`. Answer: **methyl 2-methylprop-2-enoate**, `C=C(C)C(=O)OC`. Key evidence: M⁺· 100, 69 (CH₂=C(CH₃)CO⁺), 41; conjugated ester C=O near 1725, C=C near 1640; ¹H two 1H near 6.1 and 5.55, singlets near 3.75 and 1.95.

</details>

<details><summary>Unknown 48 — SDBS search name and answer</summary>

Search SDBS for `4-nitrotoluene` or `p-nitrotoluene`. Answer: **1-methyl-4-nitrobenzene**, `Cc1ccc(cc1)[N+](=O)[O-]`. Key evidence: M⁺· 137, odd (one N), base 91 (M − NO₂); NO₂ bands near 1520 and 1345; ¹H two 2H doublets near 8.1 and 7.3, singlet near 2.45.

</details>

<details><summary>Unknown 49 — SDBS search name and answer</summary>

Search SDBS for `ethyl benzoate`. Answer: **ethyl benzoate**, `CCOC(=O)c1ccccc1`. Key evidence: M⁺· 150, base 105, 122, 77; ester C=O near 1720; ¹H quartet near 4.4, triplet near 1.4, 5 aromatic H; ¹³C near 166.

</details>

<details><summary>Unknown 50 — SDBS search name and answer</summary>

Search SDBS for `ethyl acetoacetate`. Answer: **ethyl 3-oxobutanoate**, `CCOC(=O)CC(C)=O`. Key evidence: M⁺· 130 weak, base 43, 88; two C=O (ester near 1745, ketone near 1720); ¹H quartet 4.2, singlet 3.45 (2H), singlet 2.25, triplet 1.3, plus small enol signals; ¹³C near 201 and 167.

</details>

## Common mistakes

- Opening the details block before finishing phase 1. Once you know the answer, every spectrum "obviously" fits; you learn nothing about your own reasoning. Write candidates first.
- Using the gas-phase NIST IR as if it were a liquid spectrum. Gas-phase C=O bands sit 10–40 cm⁻¹ higher and O–H bands are sharp; compare with the SDBS liquid spectrum in phase 2.
- Skipping the full assignment once the name is known. The project trains assignment as much as identification: every ¹H and ¹³C signal needs a label.
- Searching SDBS with the wrong form of a name and concluding "no spectrum". Try a wildcard, a synonym or the formula.
- Copying SDBS spectra or peak lists into a shared file or repository. Look, assign and cite; do not redistribute.

## Key takeaways

- Fifty worked unknowns turn rules into recognition: ethyl, isopropyl, para-ring, methyl ketone and ester patterns become visible at a glance.
- Phase 1 (formula, DBE, MS, IR) should always end with a written list of candidates.
- NMR (¹³C line count, ¹H integrals, splitting and shifts) makes the final decision in almost every case.
- A mistakes log shows which step you rely on too little; most learners under-use the DBE and the ¹³C line count.

## Sources

- [NIST Chemistry WebBook](https://webbook.nist.gov/chemistry/) — EI mass spectra and gas-phase IR spectra for all 50 unknowns (CAS numbers and spectra checked 2026-10-17).
- [SDBS (AIST)](https://sdbs.db.aist.go.jp/) — ¹H NMR, ¹³C NMR and condensed-phase IR spectra, searched by compound name.
- [SDBS help](https://sdbs.db.aist.go.jp/Htmls/help_eng.html) — search by name with the `%` wildcard, by formula or by SDBS number; no CAS search.
- [SDBS disclaimer](https://sdbs.db.aist.go.jp/Htmls/disclaimer_eng.html) — free access, no automated collection, citation request.
- [PubChem](https://pubchem.ncbi.nlm.nih.gov/) — structures and CAS numbers used to build the answer key.
