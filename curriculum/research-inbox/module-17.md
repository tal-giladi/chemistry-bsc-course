# Research log — Module 17

| source | url | date accessed | claim supported | lesson(s) |
|---|---|---|---|---|
| SDBS home page (AIST) | https://sdbs.db.aist.go.jp/ | 2026-10-17 | free database of MS, ¹H/¹³C NMR, IR, Raman and ESR spectra run by AIST; compound pages redirect to a disclaimer that must be accepted | 17.2–17.6 |
| SDBS disclaimer | https://sdbs.db.aist.go.jp/Htmls/disclaimer_eng.html | 2026-10-17 | access free; automated collection and large downloads prohibited; citation format "SDBS, URL, AIST, date of access" | 17.6, labs README |
| SDBS help | https://sdbs.db.aist.go.jp/Htmls/help_eng.html | 2026-10-17 | search by name (exact match, % wildcard), formula, MW, SDBS number, shifts, peaks; CAS search "unable to use"; disclaimer accepted at each use; toluene = sdbsno 97 in its URL example | 17.6 |
| SDBS introduction | https://sdbs.db.aist.go.jp/Htmls/Introduction_eng.html | 2026-10-17 | IR spectra measured as liquid film, KBr disc or Nujol paste | 17.2 |
| NIST Chemistry WebBook | https://webbook.nist.gov/chemistry/ | 2026-10-17 | Mask=200 EI mass spectrum and Mask=80 IR pages with anchors #Mass-Spec and #IR-Spec; all 50 project CAS numbers and 26 of 27 lesson compounds have both MS and IR (isobutyl acetate has MS only) | 17.1–17.6 |
| NIST WebBook EI spectra (read for verification, not copied) | https://webbook.nist.gov/cgi/cbook.cgi?ID=C591786&Mask=200 | 2026-10-17 | base peaks and main fragments quoted in lessons and answer key (2-hexanone 43/58/100; 3-hexanone 43/57/71; 1-chlorobutane base 56; butylbenzene 91/92/134; all 50 unknowns) | 17.1, 17.5, 17.6 |
| NIST WebBook IR spectra (JCAMP state lines) | https://webbook.nist.gov/cgi/cbook.cgi?ID=C107926&Mask=80 | 2026-10-17 | the NIST IR records checked are gas phase; butanoic acid C=O ≈ 1780, free O–H ≈ 3580; 2-hexanone C=O ≈ 1730; 1-octyne ≈ 3330 and 2120; methyl acetate C=O ≈ 1780 | 17.2, 17.6 |
| NIST Atomic Weights and Isotopic Compositions | https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl | 2026-10-17 | isotope masses and abundances for H, C, N, O, S, Cl, Br (¹³C 0.0107, ³⁷Cl 0.2424, ⁸¹Br 0.4931) | 17.1, labs |
| NIST CODATA 2022 proton gyromagnetic ratio over 2π | https://physics.nist.gov/cgi-bin/cuu/Value?gammapbar | 2026-10-17 | 42.577 478 461 MHz/T | 17.3 |
| NIST CODATA 2022 electron mass in u | https://physics.nist.gov/cgi-bin/cuu/Value?meu | 2026-10-17 | 5.485 799 090 441 × 10⁻⁴ u | 17.1, labs |
| NIST CODATA 2022 atomic mass constant | https://physics.nist.gov/cgi-bin/cuu/Value?u | 2026-10-17 | 1.660 539 068 92 × 10⁻²⁷ kg | 17.2, labs |
| PubChem PUG REST | https://pubchem.ncbi.nlm.nih.gov/ | 2026-10-17 | CID, formula, SMILES and CAS synonym for all 50 unknowns and the lesson compounds; SMILES matched the intended structures by RDKit canonical comparison; each CAS then confirmed by the NIST page title | 17.5, 17.6 |
| OpenStax Organic Chemistry 12.1–12.3 | https://openstax.org/books/organic-chemistry/pages/12-2-interpreting-mass-spectra | 2026-10-17 | EI, molecular ion, base peak, HRMS, alpha-cleavage, McLafferty (pages exist) | 17.1 |
| OpenStax Organic Chemistry 12.7, 12.8 | https://openstax.org/books/organic-chemistry/pages/12-8-infrared-spectra-of-some-common-functional-groups | 2026-10-17 | IR regions and functional-group bands (pages exist) | 17.2 |
| OpenStax Organic Chemistry 13.2–13.8 | https://openstax.org/books/organic-chemistry/pages/13-6-spin-spin-splitting-in-1h-nmr-spectra | 2026-10-17 | shielding, shift ranges, integration, n+1 rule, equivalence (pages exist) | 17.3 |
| OpenStax Organic Chemistry 13.10–13.13 | https://openstax.org/books/organic-chemistry/pages/13-12-dept-13c-nmr-spectroscopy | 2026-10-17 | ¹³C ranges, decoupling, DEPT (pages exist) | 17.4 |
| OpenStax Organic Chemistry 7.2 | https://openstax.org/books/organic-chemistry/pages/7-2-calculating-the-degree-of-unsaturation | 2026-10-17 | DBE formula | 17.5 |
| LibreTexts, Introduction to Organic Spectroscopy, ch. 7 | https://chem.libretexts.org/Bookshelves/Organic_Chemistry/Introduction_to_Organic_Spectroscopy/07%3A_Two-Dimensional_NMR_Spectroscopy | 2026-10-17 | COSY, HSQC (one bond), HMBC (two to three bonds) | 17.4 |
| Hans Reich NMR collection | https://organicchemistrydata.org/hansreich/resources/nmr/ | 2026-10-17 | shift and coupling tables, second-order spectra (site loads) | 17.3, 17.4 |
| RDKit 2026.09.1 (local run) | https://www.rdkit.org/docs/GettingStartedInPython.html | 2026-10-17 | CanonicalRankAtoms(breakTies=False) for symmetry classes; all lab scripts run with RDKit 2026.9.1, numpy 2.5.3, matplotlib 3.11.2 on Python 3.14 | labs |
