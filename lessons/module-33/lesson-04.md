---
id: "33.4"
module: 33
minutes: 20
practice_minutes: 180
prerequisites: ["33.3", "11.1", "11.2"]
objectives:
  - Check a finished project package against a written list and fix every failure before anyone else sees it.
  - Find a suitable academic reader and write a short request that states the result, the specific question and the time asked for.
  - Give and receive a structured review, record the feedback and the changes it caused.
  - Archive the project with a licence and a persistent identifier, and choose a realistic next step.
volatility: implementation
sources:
  - title: "Bourne and Korngreen (2006), Ten simple rules for reviewers, PLoS Computational Biology 2(9), e110"
    url: https://doi.org/10.1371/journal.pcbi.0020110
  - title: "Zenodo, open research repository (CERN and OpenAIRE)"
    url: https://about.zenodo.org/
  - title: "ORCID, What is ORCID"
    url: https://info.orcid.org/what-is-orcid/
  - title: "ChemRxiv, FAQs for authors"
    url: https://chemrxiv.org/engage/assets/public/chemrxiv/term/author-faq.htm
  - title: "Israel Chemical Society"
    url: https://www.chemistry.org.il/
  - title: "Creative Commons, CC BY 4.0 licence deed"
    url: https://creativecommons.org/licenses/by/4.0/
last_verified: "2026-10-17"
---

# 33.4 · Getting feedback and what comes next

This last lesson closes the project and the course. A Technion research project ends with a report that the supervising researcher approves; yours ends with a report that you check against a list, that a peer reviews, and that, if you can find one, an academic reader comments on. Then you archive it so that it can be found and cited, and decide what to do next. The lesson is also the module's practical piece: the finished package of your 180-hour project.

## Why it matters

Without feedback, a self-taught project has one reader: you. You will not see the mistake you made in week 3, because you have read past it fifty times. A reader who knows the field sees it in five minutes, and one useful comment from an expert can be worth more than the last 30 hours of polishing. Feedback is also the only outside evidence that the work is sound. A report read and commented on by a researcher means more, to you and to anyone you show it to, than one nobody has checked.

The honest limit stays: a reader is not a supervisor. They did not watch the work, did not check your raw data, and do not award credit. Say exactly what they did when you mention them.

## Core ideas

> [!NOTE]
> Stable: self-review, peer review, how to ask an expert for feedback, why archiving matters. Will go out of date: the services and their terms (Zenodo, ORCID, ChemRxiv, the Israel Chemical Society's meeting and fees, all checked 2026-10-17). Read each service's current terms before you use it.

### Three rounds of review

1. **Self-review.** Run the package check (Hands-on), then leave the report for a week and read it cold, from the title down, as a stranger would. Check every number in the abstract against the results, and every result against `results/`.
2. **Peer review.** Swap reports with another learner, or with a scientifically literate friend. Use a fixed form, so that the review is useful and not just polite: (a) the main result in the reviewer's own words; (b) the claim they believe least and why; (c) one thing in the methods they could not repeat; (d) one figure that confused them; (e) a firm verdict: ready to send, minor changes, or major changes. Bourne and Korngreen's rules for reviewers apply to you as a reviewer too: write the review you would find fair and useful, be neutral, and give a firm recommendation.
3. **Academic reader.** One expert, one specific question, about an hour of their time.

Record every comment and what you changed in `doc/reader-feedback.md`. A comment you decide not to act on gets one line saying why.

### Finding an academic reader

Good candidates are people who already care about your question:

- **Authors of the papers and data sets you used.** The author of a benchmark you extended is the person most likely to find your result interesting. The contact address is on the paper.
- **Researchers whose group pages match your topic.** Faculty pages at Israeli universities (Technion, Weizmann, Hebrew University, Tel Aviv, Ben-Gurion, Bar-Ilan and others) list research interests. A computational chemist for a computational project, an analytical chemist for a measurement project.
- **Teachers and retired researchers.** A university lecturer who teaches the relevant course, or a retired researcher, often has more time than an active group leader.
- **The chemistry community.** The Israel Chemical Society holds its annual meeting in mid-February (the 89th was on 10–11 February 2026 at Tel Aviv University) and lists membership fees for students. A meeting is a place to meet people in person, which makes a later e-mail much easier.

Expect most requests to go unanswered. Researchers receive many e-mails. Send to one person at a time, wait two weeks, send one polite reminder, then move to the next name. A no, or silence, is not a judgement of your work.

### Writing the request

Keep it under 150 words. Say who you are, what you found, what you are asking, and how much time it takes. Attach the one-page abstract or poster, and offer the full report on request.

- **Who you are, honestly:** a self-taught learner who has finished a structured chemistry curriculum and a 180-hour project. Do not suggest an affiliation you do not have.
- **The result in one sentence**, with the number.
- **One specific question.** "Is it fair to compare harmonic frequencies with gas-phase band centres for amides, or is there a better reference?" is easy to answer. "Could you give me feedback?" is not.
- **The time:** "I estimate 30 minutes to read the abstract and figures."
- **What you will do with the answer:** "I will revise the report and acknowledge your comments by name only if you agree."

### Archiving and identifiers

A project on your laptop disappears. Two free services make it findable and citable:

- **ORCID** gives you a free, persistent researcher identifier that links your outputs to you, whatever your affiliation.
- **Zenodo**, run by CERN with OpenAIRE, archives research outputs of any field and gives each record a DOI; the IUPAC pKa data set of 33.1 is archived there. You can deposit the report, the poster, the data you are allowed to share, and the code.

Choose licences explicitly: CC BY 4.0 for the text and figures (others may reuse them with attribution), an open-source licence such as MIT for code. Data keep the licence of their source: you may not republish data whose licence forbids it, even inside your own archive; link to them instead.

A **preprint server** such as ChemRxiv is for manuscripts intended for a journal; its submissions are screened by a curation team. Post there only if your reader agrees the work is new enough and written as a paper. For most course projects, Zenodo is the right place.

### What comes next

The course ends here, and so does its honest scope: you understand the chemistry of a Technion B.Sc., you have done real computational work and safe home measurements, and you have a finished, documented research project. You do not have bench hands, and an employer or a research group would still train you at the bench ([01.1](../module-01/lesson-01.md)). Realistic next steps:

- **Extend the project with your reader.** If the reader is interested, ask whether a second phase is worth doing. This is how many collaborations start.
- **Formal credit.** If you want a degree, Israeli universities' own programmes are the route. The Open University of Israel admits undergraduates without a matriculation certificate and teaches chemistry courses; check its current rules and whether its credits are recognised where you want to go.
- **Bench skills.** Short practical courses, a volunteer or technician position in a teaching lab, or industry training are the only way to gain what this course could not train.
- **A portfolio.** Your project folder, report, poster and the Module 31 calculations are evidence of what you can do. Put the archived versions where an employer can see them.

## Worked example

### A request that gets answered

This is an illustrative exchange, continuing Noa's example from 33.3. Her first draft (190 words) opened with three sentences about her career change, asked "Would you be willing to look at my research and give me feedback?" and attached a 16-page PDF. It got no answer. Her second version, to the first author of a benchmark of fast vibrational methods she had cited:

> Subject: Question on xtb carbonyl frequencies (your 2023 benchmark)
>
> Dear Dr. ...,
>
> I am a self-taught chemistry learner who has just finished a 180-hour project extending part of your benchmark to 30 carbonyl compounds. GFN2-xTB overestimates the C=O stretch by 52 ± 6 cm⁻¹ against NIST gas-phase data, and most for amides (78 ± 9 cm⁻¹, n = 7). The one-page abstract is attached.
>
> My question: is it fair to compare harmonic frequencies with gas-phase band centres for amides, or would you use a different reference? I think it would take about 20 minutes to read the abstract and figure 2.
>
> I would revise the report with your answer and acknowledge you only if you agree. Thank you for your time.
>
> Noa ..., ORCID 0000-..., link to the report on Zenodo

It is 135 words, names a specific question, says how long it takes and what happens next. The reply, a week later, was two lines: amide band centres in the gas phase are affected by Fermi resonance in some molecules; check those three. That comment changed one result and added a paragraph to her limitations section.

### Acting on a peer review

Her peer reviewer believed the amide claim least ("seven molecules") and could not repeat one step ("which conformer did you use for the esters?"). Noa added the conformer choice to the methods, softened "xtb fails for amides" to "the error is larger for amides in this set", and recorded both changes in `doc/reader-feedback.md`.

## Hands-on

This is the module's practical piece: your finished 180-hour project package. What you need: your project folder, the [Module 33 lab folder](../../labs/module-33/), the report and poster from 33.3, the [lab report template](../../templates/lab-report.md) for the checklist. Time: about 3 hours of work, plus the waiting time for reviews.

1. **Package check (45 min).** Complete the two TODO functions in `lesson04_package_check.py` (`check_hours` and `check_pinned`). Test them on the demo project, then on your own folder, and fix every FAIL:

```bash
py make_project.py runs/demo-project --demo
py lesson04_package_check.py runs/demo-project
py lesson04_package_check.py ../../../my-project
```

2. **Cold read (30 min, a week later).** Read the report from the title down with the checklist from 33.3. Rerun `src/run_all.py` from a fresh clone and compare every number in the report.
3. **Peer review (60 min each way).** Swap with another learner and use the five-part form (a–e above). Record the comments and your changes.
4. **Reader request (30 min).** Pick three candidate readers, with a reason for each. Write the request to the first one, under 150 words, with one specific question. Send it yourself from your own e-mail account when you are ready, then wait two weeks before trying the next name.
5. **Archive (15 min).** Create an ORCID iD if you want one. Choose licences, then deposit the report, poster and code (and the data you may share) on Zenodo, or keep a dated, public repository. Put the link on the poster.

How you know it worked: the package check prints `0 failed`; `run_all.py` rebuilds every number in the report from a fresh clone; `doc/reader-feedback.md` lists the peer's comments and what you changed; the reader request is under 150 words with one question; the project has a public, dated home.

<details><summary>Reference output</summary>

On the demo folder the exercise prints 10 PASS and 2 FAIL (the two TODO checks). The solution prints 12 passed, 0 failed, including `PASS requirements: all pinned` and `PASS hours: 180 h logged`. On a fresh, empty folder from `make_project.py` it prints 4 failures: no raw data, no poster, no feedback note and `0 h logged; phases never logged: reading, setup and pilot, ...`. That is the list of what a project still owes its reader.

A typical first run on a real project fails on unpinned requirements (`numpy` without a version) and an hours log with a phase name typed two ways ("analysis" and "Analysis"). Fix the log in one place and pin every package with `pip freeze`.

</details>

## Common mistakes

- **Sending the report before checking it.** The first reader should not find what the package check would have found.
- **A vague request to a busy expert.** Ask one specific question, say how long it takes, attach one page.
- **Overstating the reader's role.** "Read and commented on by Dr. X" is accurate; "supervised by" or "approved by" is not, unless it is true.
- **Republishing data you may not share.** Archive your code and results; link to restricted data instead of uploading them.
- **Treating silence as rejection of the work.** Most requests get no reply for reasons that have nothing to do with you. Move to the next name.

## Key takeaways

- Review in three rounds: self-review with a written check, a peer review on a fixed form, and one academic reader with one specific question.
- The best readers already care about your question: the authors of your sources and researchers in the field.
- Archive the work with licences and a persistent identifier so others can find and cite it.
- The course gives understanding, computational skill and a finished research project, not bench hands; choose a next step that builds on what you have and trains what you lack.

## Sources

- [Bourne and Korngreen (2006), Ten simple rules for reviewers](https://doi.org/10.1371/journal.pcbi.0020110) — fair, useful, neutral reviews with a firm recommendation.
- [Zenodo](https://about.zenodo.org/) — open repository for any research output, run by CERN and OpenAIRE, with DataCite DOIs.
- [ORCID](https://info.orcid.org/what-is-orcid/) — free persistent identifier for researchers.
- [ChemRxiv author FAQ](https://chemrxiv.org/engage/assets/public/chemrxiv/term/author-faq.htm) — preprints before peer review; submissions curated.
- [Israel Chemical Society](https://www.chemistry.org.il/) — annual meeting (89th, 10–11 February 2026, Tel Aviv University) and student membership.
- [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — the licence suggested for the report and poster.
