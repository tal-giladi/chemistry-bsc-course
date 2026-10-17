# Module 11 labs — Scientific English: Reading and Writing Chemistry

A reading worksheet (lesson 11.1), a DOI checker (lesson 11.2), and a bad figure to redraw plus a writing self-check list for the module practical (lesson 11.3). Exercise files have functions marked TODO; the matching `*_solution.py` file is the reference solution. Plots are written to `runs/` in this folder (ignored by git).

Setup (once, Python 3.14, packages pinned in `labs/common/requirements.txt`; checked 2026-10-17):

```bash
py -3.14 -m venv .venv
.venv\Scripts\python -m pip install -r labs/common/requirements.txt
```

On macOS or Linux use `python3.14` and `.venv/bin/python`. The figure scripts need numpy, scipy and matplotlib; `doi_check.py` needs only the Python standard library. Run each file from this folder, for example `py good_figure.py`.

| Lesson | File | Solution | Data |
|---|---|---|---|
| 11.1 Reading a research paper efficiently | `paper_summary_worksheet.md` | in the lesson | the paper (open access, linked in the lesson) |
| 11.2 Finding and judging sources and data | `doi_check.py` | `doi_check_solution.py` | `dois.txt` or your own list; `doi_cache.json` for offline use |
| 11.3 Writing a lab report and a figure that tells the story | `bad_figure.py` (run as is), `good_figure.py` | `good_figure_solution.py` | `class_vinegar.csv`, `titration_curve.csv` |
| 11.3 Module practical: the full report | `writing_checklist.md` | — | your data from lesson 10.6 or 09.6 |

## The DOI checker and the network

`doi_check.py` sends each DOI to the public Crossref REST API (`https://api.crossref.org/works/<DOI>`) and reports whether the DOI exists, its journal and licence, and any retraction or correction notice (Crossref includes the Retraction Watch data). If the network fails it uses `doi_cache.json`, which holds the records as they were on 2026-10-17. Options:

```bash
py doi_check.py                # dois.txt, live API, cache as fallback
py doi_check.py my_dois.txt    # your own list, one DOI per line
py doi_check.py --offline      # cache only
```

Crossref asks heavy users to identify themselves: set the environment variable `CROSSREF_MAILTO` to your own e-mail address to use its "polite pool". The script sends nothing else about you. Citation counts and notices change, so live output may differ from the cache.

## Data

- `class_vinegar.csv` and `titration_curve.csv` are simulated by `make_data.py` with fixed seeds (run `py make_data.py` to regenerate them). The class data model six learners repeating the lesson 10.6 vinegar titration five times each (true value 4.95 % w/w; learner D without an indicator blank, a spill in C's trial 4, F with a 0.1 g scale). The curve is an exact charge-balance model of 10.00 mL of 0.0830 mol/L acetic acid titrated with 0.1000 mol/L NaOH (pKa 4.757, Harvey, Analytical Chemistry 2.1, Appendix 11), with pH noise. They are realistic but not measured.
- `doi_cache.json` holds Crossref metadata (openly available from Crossref) for the six DOIs in `dois.txt`; one of them is deliberately invented and has no record.
- No paper text or figures are copied here; the two papers in lesson 11.1 are open access (CC BY 4.0) and are read at the publisher's site.
