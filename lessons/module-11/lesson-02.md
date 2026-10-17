---
id: "11.2"
module: 11
minutes: 20
practice_minutes: 75
prerequisites: ["11.1", "09.2"]
objectives:
  - Place a source on the ladder from primary measurement to chatbot answer, and say what each rung can be trusted for.
  - Check a DOI for existence, licence, retraction and correction with Crossref, by script or by hand.
  - Trace a physical constant from an encyclopedia or aggregator back to the primary measurement, and choose the value to cite.
  - Judge a journal and a paper with a short evidence checklist instead of by reputation or citation count.
volatility: implementation
sources:
  - title: "Crossref REST API documentation"
    url: https://www.crossref.org/documentation/retrieve-metadata/rest-api/
  - title: "Crossref (2023-09-12), Crossref acquires Retraction Watch data and opens it for the scientific community"
    url: https://www.crossref.org/blog/news-crossref-and-retraction-watch/
  - title: "Chemistry World (2020), Frances Arnold's masterful retraction highlights the problems with publication-driven science"
    url: https://www.chemistryworld.com/opinion/frances-arnolds-retraction-and-the-case-for-slow-science/4010994.article
  - title: "Ioannidis (2005), Why most published research findings are false, PLoS Medicine 2(8), e124"
    url: https://doi.org/10.1371/journal.pmed.0020124
  - title: "Wilkinson et al. (2016), The FAIR Guiding Principles for scientific data management and stewardship, Scientific Data 3, 160018"
    url: https://doi.org/10.1038/sdata.2016.18
  - title: "NIST Chemistry WebBook (SRD 69), acetic acid, condensed phase thermochemistry"
    url: https://webbook.nist.gov/cgi/cbook.cgi?ID=C64197&Mask=2
  - title: "NIST Chemistry WebBook (SRD 69), ethanol, condensed phase thermochemistry"
    url: https://webbook.nist.gov/cgi/cbook.cgi?ID=C64175&Mask=2
  - title: "Think. Check. Submit."
    url: https://thinkchecksubmit.org/
last_verified: "2026-10-17"
---

# 11.2 · Finding and judging sources and data

Every number you use came from someone's measurement, and between that measurement and you there may be a review, a handbook, a database, an encyclopedia or a chatbot, each of which can drop the conditions, round the value or copy it wrongly. This lesson shows where to find papers and data, how to check that a reference exists and has not been retracted, how to trace a value back to the measurement it came from, and how to judge a journal or a paper by its evidence rather than its fame.

## Why it matters

In May 2019 *Science* published a paper from the lab of Frances Arnold, who won the Nobel Prize in Chemistry the year before. It reported enzymes that make lactams, ring compounds found in many drugs. In January 2020 the authors retracted it. Other researchers could not reproduce the results, and the first author's notebook was missing contemporaneous entries and raw data for key experiments: the exact failure lesson [01.3](../module-01/lesson-03.md) warns about.

Retractions are rare. Copying errors, missing conditions and invented references are not: a chatbot can format a perfect citation to a paper that does not exist, and a database can show a value with a digit swapped. A report that rests on such a number is wrong however good your own measurement is.

## Core ideas

### The source ladder

Sources differ in how close they are to the measurement and in who checked them.

| Source | Trust it for | Watch out for |
|---|---|---|
| Primary article (first report, peer reviewed) | The method and the data, as reported | Small studies; one lab; errors reviewers missed |
| Preprint (e.g. ChemRxiv; not yet reviewed) | Very recent work | Not reviewed; may change or vanish |
| Review article | Overview and the key primary papers | The reviewers' own views |
| Evaluated data (NIST WebBook, CODATA, IUPAC: experts compare measurements) | Constants, with uncertainty and conditions | Old data, if never re-evaluated |
| Aggregator (PubChem) | Finding values and their sources | Each value is only as good as its cited source |
| Textbook (Harvey, OpenStax) | Concepts, standard methods | Rounded values, older editions |
| Encyclopedia (Wikipedia) | A map to sources | Values without footnotes; changes daily |
| News, press release | Knowing that something happened | Overstated claims |
| Chatbot answer | Ideas for search terms | Invented facts and references |

The rule: **cite as close to the measurement as you can, and from a source that states uncertainty and conditions.** Use the lower rungs to find the higher ones.

### Where to look

- **Papers.** Google Scholar for broad search, PubMed for biochemistry, OpenAlex and Crossref as open indexes. For a paywalled paper, Unpaywall finds a legal free copy if one exists.
- **Citation chasing.** Go *backward* through a good paper's references, and *forward* with "cited by" to newer work that confirms or contradicts it.
- **Data.** The NIST Chemistry WebBook for thermochemistry and spectra; PubChem for compound records, properties and safety (lesson [01.4](../module-01/lesson-04.md)); CAS Common Chemistry for names and CAS Registry Numbers; SDBS for spectra (Module 17); the Protein Data Bank for structures (Module 6).
- **Search terms.** Use the systematic name, the common name and the CAS number: "ethanoic acid", "acetic acid", "64-19-7".

### Does the reference exist, and is it still standing?

A **DOI** (Digital Object Identifier) is a permanent ID for a paper or a data set, such as `10.1038/sdata.2016.18`. Crossref, the main DOI registry for journals, keeps the metadata for each DOI and offers it through a free public interface (an **API**: a web address a program can query). Since 12 September 2023 Crossref also owns the Retraction Watch database of retractions and has made it open, so a Crossref record shows whether a paper has been **retracted** (withdrawn as unreliable), **corrected** or flagged with an **expression of concern**.

Three checks, by hand at `doi.org` or with this lesson's script:

1. **Does the DOI resolve?** If Crossref has no record and there is no typo, treat the reference as invented.
2. **Has it been updated?** A retraction means do not use it as evidence. A correction means read the notice: it may change a result, or, as in the 2022 correction of Ioannidis's 2005 paper, add a missing pair of brackets to one formula.
3. **Is it open?** A Creative Commons licence (CC BY, CC0) means you may read, share and reuse it with attribution.

### Is the journal real?

**Predatory journals** take fees and publish anything, with no real peer review. For an unfamiliar journal, use the Think. Check. Submit. checklist: a known publisher, a named editorial board, a described review process, open fees, and (for open access) a listing in the Directory of Open Access Journals (DOAJ).

### Is the paper good? Judge the evidence

Reputation and citation counts measure attention, not truth. Ioannidis argued in 2005 that a published finding is less likely to be true when studies are small, effects are small, many relationships are tested, designs and analyses are flexible, there are financial interests, and many teams chase the same hot result. Turn that into a checklist:

- **Sample size and repeats.** How many samples, how many independent repeats (lesson [09.2](../module-09/lesson-02.md))?
- **Controls and references.** A blank, a certified material, a reference method?
- **Uncertainty.** Are results given with an uncertainty and the meaning of the "±"?
- **Data.** Are raw data available? The **FAIR** principles say data should be Findable, Accessible, Interoperable and Reusable: in a repository, with a persistent ID, in an open format, with a clear licence.
- **Independent confirmation.** Has another lab reproduced it?
- **Interests.** Who paid, and does anyone gain from the result?

### Is the number good? Trace it

For a constant, ask: who measured it, by what method, under what conditions (temperature, phase, standard state), with what uncertainty, and do independent measurements agree? An **evaluated** value, where experts compared all measurements, is best; one old measurement copied through three handbooks is worst.

> [!NOTE]
> The ladder and the checklists are stable. The tools are not: Crossref's API fields, the databases' contents, and what Wikipedia and PubChem show for a value change over time. Everything here was checked on 2026-10-17, including the values in the worked example and the Crossref records in the lab cache.

## Worked example

### Tracing the enthalpy of combustion of ethanol

You need the standard enthalpy of combustion of liquid ethanol, $\Delta_c H^\circ$, for a calorimetry report (lesson [08.1](../module-08/lesson-01.md)). On 2026-10-17 three sources gave:

| Source | Value / (kJ/mol) | What it cites |
|---|---|---|
| Wikipedia, "Ethanol", Combustion section | −1371 (water liquid); −1236 (water gas) | Rossini 1937 (a review of heats of formation); a 1968 handbook |
| PubChem, ethanol (CID 702), Heat of Combustion | 1336.8 at 25 °C | CRC Handbook, 95th edition |
| NIST WebBook, ethanol, condensed phase | −1367.6 ± 0.3 (Chao and Rossini 1965); −1367.0 ± 0.42 (Green 1960); three older values from 1911–1925 | The original calorimetry papers |

**Step 1: put all values on the same convention.** Combustion of liquid ethanol:

$$\text{C}_2\text{H}_5\text{OH(l)} + 3\,\text{O}_2\text{(g)} \rightarrow 2\,\text{CO}_2\text{(g)} + 3\,\text{H}_2\text{O}$$

The standard value has liquid water as product. The −1236 kJ/mol value has water as gas. Is the difference just the heat of vaporising 3 mol of water? From the CODATA values on the NIST WebBook, $\Delta_f H^\circ$ is −285.830 kJ/mol for liquid water and −241.826 kJ/mol for water vapour, so vaporisation takes 44.004 kJ/mol:

$$-1367.6 + 3 \times 44.004 = -1235.6 \text{ kJ/mol}$$

That matches −1236. Not an error: a different product state. Always check the conditions before you call two values different.

**Step 2: find the outlier.** PubChem's 1336.8 is about 31 kJ/mol (2 %) below all the calorimetric values. It cites a handbook page, not a measurement. The digits suggest a copying slip, because 1366.8 would sit among the measured values. You cannot be sure without the handbook itself, and you do not need to be: you do not cite it.

**Step 3: compare with the primary measurements.** Wikipedia's 1371 cites a 1937 review; the NIST entries include a 1965 measurement by the same research group with a stated uncertainty of ± 0.3 kJ/mol. The two modern measurements, −1367.6 ± 0.3 and −1367.0 ± 0.42, agree within about their combined uncertainty ($\sqrt{0.3^2 + 0.42^2} = 0.52$ kJ/mol, difference 0.6 kJ/mol).

**Decision.** Cite $\Delta_c H^\circ = -1367.6 \pm 0.3$ kJ/mol (Chao and Rossini 1965, via the NIST Chemistry WebBook), state that water is liquid in the product, and note that it agrees with an independent value. The sign also matters: a heat *released* of 1367.6 kJ/mol is an enthalpy *change* of −1367.6 kJ/mol.

## Hands-on

What you need: a web browser, the [Module 11 lab folder](../../labs/module-11/) with Python 3.14 (pinned set-up from lesson [05.1](../module-05/lesson-01.md); the DOI script uses only the standard library), and your notebook. Time: about 75 minutes. The script contacts the public Crossref API; with no internet it falls back to the saved records in `doi_cache.json`.

### Part A — trace a number (30 min)

You want the standard enthalpy of combustion of liquid acetic acid, the acid in your vinegar (Module 10).

1. Look it up on Wikipedia ("Acetic acid", the data box on the right). Write down every value and whether it has a footnote.
2. Look it up on PubChem (acetic acid, CID 176, section "Heat of Combustion"). Write down the value and the source it cites.
3. Open the [NIST WebBook condensed-phase page for acetic acid](https://webbook.nist.gov/cgi/cbook.cgi?ID=C64197&Mask=2). Write down each $\Delta_c H^\circ_{\text{liquid}}$ entry with its uncertainty, method and reference.
4. Put the values in one table. Which agree within their uncertainties? Which source is closest to the measurement? Write the value you would cite, with its uncertainty and source, in one sentence.

How you know it worked: you can say, for every value in your table, which measurement it ultimately comes from.

<details><summary>Reference answer (values as shown on 2026-10-17)</summary>

| Source | Value / (kJ/mol) | Ultimate origin |
|---|---|---|
| NIST: Steele, Chirico et al. 1997 | −875.16 ± 0.34 | Combustion calorimetry |
| NIST: Lebedeva 1964 | −874.2 ± 0.2 | Combustion calorimetry |
| NIST: Evans and Skinner 1959 | −874.5 ± 0.4 | Combustion calorimetry |
| NIST: Schjanberg 1935 | −872.4 (no uncertainty) | Combustion calorimetry |
| PubChem (CRC Handbook, 94th ed.) | 874.2 | Matches Lebedeva 1964 |
| Wikipedia data box | −875.50 to −874.82, and a separate −876.1 | The range is the 1997 value ± its uncertainty; the −876.1 had no footnote of its own |

The 1997 and 1964 values differ by 0.96 kJ/mol, more than their combined stated uncertainty (0.39 kJ/mol): at least one uncertainty was too small. That is common, and it is why evaluated compilations exist. A good sentence: "$\Delta_c H^\circ$(CH₃COOH, l) = −875.16 ± 0.34 kJ/mol (Steele et al. 1997, via the NIST Chemistry WebBook); older calorimetric values lie up to 1 kJ/mol less negative." Wikipedia changes, so your values may differ; the method of tracing them does not.

</details>

### Part B — check references with a script (25 min)

1. Open `doi_check.py` and complete the two TODOs: `is_open`, which says whether a licence is Creative Commons, and `verdict`, which turns a Crossref record into OK, CORRECTED, RETRACTED or NOT-FOUND.
2. Run it from the lab folder:

```bash
py doi_check.py
```

3. Add three DOIs from the reference list of either lesson 11.1 paper to a new file `my_dois.txt` and run `py doi_check.py my_dois.txt`.
4. For each CORRECTED result, open the notice (`https://doi.org/` plus the notice DOI) and write one line on what changed.

How you know it worked: the summary line for the supplied list reads `CORRECTED 2, NOT-FOUND 1, OK 2, RETRACTED 1`. If you have no internet, add `--offline`.

<details><summary>Reference solution for the TODOs</summary>

```python
# TODO 1
return any(any(o in lic for o in OPEN_LICENCES) for lic in rec.get("licences", []))
# TODO 2
kinds = {u["type"] for u in rec.get("updates", [])}
if "retraction" in kinds or "withdrawal" in kinds:
    return "RETRACTED"
if kinds & {"correction", "erratum", "expression_of_concern", "addendum"}:
    return "CORRECTED"
return "OK"
```

The retraction check comes first because a retracted paper often also has corrections. The full script is `doi_check_solution.py`.

</details>

### Part C — score four sources (20 min)

A friend claims "phones measure food dyes as accurately as a spectrophotometer" and sends four sources, invented for this exercise: (1) a university press release with no numbers; (2) a peer-reviewed paper comparing a phone method with UV–vis on ten samples, one phone, one dye; (3) a preprint with 200 samples, three phones and public data, not yet reviewed; (4) a chatbot answer citing doi:10.1021/acs.jchemed.9b99999. Score each 0–2 on closeness to the measurement, peer review, stated uncertainty, available data and independent confirmation. Which supports the claim, and for what?

<details><summary>Reference scoring</summary>

The press release only points to a study. The paper scores high on review and uncertainty, low on generality. The preprint is high on data and size, zero on review: read it, do not yet cite it as settled. The chatbot scores zero; its DOI does not exist (Part B). Only source 2 supports a claim, and a narrower one: "a phone method agreed with UV–vis for one dye and one phone". It does not support "as accurately": in lesson 11.1 the phone's detection limit was about 74 times higher.

</details>

## Common mistakes

- **Citing the encyclopedia or the aggregator.** They are maps. Follow the footnote to the measurement and cite that, or an evaluated compilation.
- **Comparing values under different conditions.** Liquid or gas water, 25 °C or 18 °C, per mole or per gram: check before calling a value wrong.
- **Trusting a citation you have not opened.** Chatbots and careless authors produce references that do not exist or do not say what is claimed. Resolve every DOI.
- **Treating every correction as fatal, or ignoring retractions.** Read the notice. A retraction removes the paper as evidence; a correction may be a typo.
- **Judging by fame.** A famous lab, a high-impact journal or many citations do not replace sample size, controls and data. Arnold's retracted paper was in *Science*.

## Key takeaways

- Cite as close to the measurement as you can, from a source that states uncertainty and conditions; use lower rungs only to find higher ones.
- Resolve every DOI, and check Crossref for retractions and corrections before relying on a paper.
- Judge a journal with Think. Check. Submit. and DOAJ, and a paper by its evidence: n, controls, uncertainty, data, confirmation, interests.
- Trace a constant: who measured it, how, under what conditions, with what uncertainty, and do independent measurements agree?
- Note the date you checked any online value; databases and encyclopedias change.

## Sources

- [Crossref REST API documentation](https://www.crossref.org/documentation/retrieve-metadata/rest-api/) (checked 2026-10-17).
- [Crossref (2023), acquisition and opening of the Retraction Watch database](https://www.crossref.org/blog/news-crossref-and-retraction-watch/) (announced 12 September 2023).
- [Chemistry World (2020) on the Arnold retraction](https://www.chemistryworld.com/opinion/frances-arnolds-retraction-and-the-case-for-slow-science/4010994.article); the retracted paper is [doi:10.1126/science.aaw9068](https://doi.org/10.1126/science.aaw9068).
- [Ioannidis (2005), PLoS Medicine 2(8), e124](https://doi.org/10.1371/journal.pmed.0020124).
- [Wilkinson et al. (2016), Scientific Data 3, 160018](https://doi.org/10.1038/sdata.2016.18) (FAIR principles).
- [NIST Chemistry WebBook, acetic acid](https://webbook.nist.gov/cgi/cbook.cgi?ID=C64197&Mask=2) and [ethanol](https://webbook.nist.gov/cgi/cbook.cgi?ID=C64175&Mask=2) condensed-phase thermochemistry; [water](https://webbook.nist.gov/cgi/cbook.cgi?ID=C7732185&Mask=3) (CODATA $\Delta_f H^\circ$ values).
- [PubChem, ethanol (CID 702)](https://pubchem.ncbi.nlm.nih.gov/compound/702) and [acetic acid (CID 176)](https://pubchem.ncbi.nlm.nih.gov/compound/176) (checked 2026-10-17).
- [Think. Check. Submit.](https://thinkchecksubmit.org/) (checklist for judging journals).
