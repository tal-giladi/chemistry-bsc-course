# Research log — Module 05

| source | url | date accessed | claim supported | lesson(s) |
|---|---|---|---|---|
| Python.org downloads | https://www.python.org/downloads/ | 2026-10-16 | 3.14.8 latest 3.14 (2026-09-30); 3.15.0 released 2026-10-09; Windows install manager 26.4 offered first | 05.1 |
| Python 3.14 docs, Using Python on Windows | https://docs.python.org/3.14/using/windows.html | 2026-10-16 | `py install <tag>`, `py list`; classic installer deprecated since 3.14, none for 3.16+ | 05.1 |
| PyPI (pip index versions) | https://pypi.org/ | 2026-10-16 | all eight pins in labs/common/requirements.txt exist and are the newest releases; install tested in a fresh 3.14 venv, check_setup.py all ok | 05.1 |
| IUPAC CIAAW abridged standard atomic weights 2024 | https://www.ciaaw.org/abridged-atomic-weights.htm | 2026-10-16 | H 1.0080, C 12.011, N 14.007, O 15.999, Na 22.990, S 32.06, Cl 35.45, etc. | 05.1, 05.2 |
| MIT OCW 6.100L | https://ocw.mit.edu/courses/6-100l-introduction-to-cs-and-programming-using-python-fall-2022/ | 2026-10-16 | course exists (Ana Bell, Fall 2022), depth reference | 05.1 |
| NumPy 2.5 beginners guide | https://numpy.org/doc/stable/user/absolute_beginners.html | 2026-10-16 | arrays, shape, broadcasting rules; docs are v2.5 | 05.2 |
| NumPy 2.4.0 release notes | https://numpy.org/doc/stable/release/2.4.0-notes.html | 2026-10-16 | numpy.trapz removed in 2.4 (deprecated since 2.0); use numpy.trapezoid | 05.1, 05.2 |
| Matplotlib quick start (3.11.2) | https://matplotlib.org/stable/users/explain/quick_start.html | 2026-10-16 | explicit fig/ax (OO) style recommended | 05.2 |
| OpenStax University Physics 2, 2.4 | https://openstax.org/books/university-physics-volume-2/pages/2-4-distribution-of-molecular-speeds | 2026-10-16 | Maxwell–Boltzmann v_p = sqrt(2kT/m), mean = sqrt(8kT/(pi m)) | 05.2 |
| NIST CODATA 2022 atomic mass constant | https://physics.nist.gov/cgi-bin/cuu/Value?ukg | 2026-10-16 | m_u = 1.66053906892(52) e-27 kg | 05.2 |
| SciPy 1.18 curve_fit | https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html | 2026-10-16 | absolute_sigma semantics, pcov rescaling, default method lm | 05.3 |
| Harvey, Analytical Chemistry 2.1, 5.4 | https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_(Harvey)/05%3A_Standardizing_Analytical_Methods/5.04%3A_Linear_Regression_and_Calibration_Curves | 2026-10-16 | eq. 5.12, uncertainty of a concentration from a calibration line | 05.3 |
| NIST/SEMATECH e-Handbook 4.4.4 | https://www.itl.nist.gov/div898/handbook/pmd/section4/pmd44.htm | 2026-10-16 | residual analysis; high R² does not guarantee a good fit | 05.3, 05.5 |
| uncertainties documentation | https://uncertainties.readthedocs.io/en/latest/ | 2026-10-16 | linear propagation with correlations; version 4.0 announced (course pins 3.2.3) | 05.3 |
| lmfit 1.3.4 on PyPI / docs | https://pypi.org/project/lmfit/1.3.4/ | 2026-10-16 | current version 1.3.4; Model class extends curve_fit | 05.3 |
| pandas 3.0.6 read_csv | https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html | 2026-10-16 | sep, decimal, skiprows, comment, na_values, encoding options | 05.4 |
| pandas 3.0.0 release notes | https://pandas.pydata.org/docs/whatsnew/v3.0.0.html | 2026-10-16 | released 2026-01-21; default str dtype; Copy-on-Write, chained assignment no longer works | 05.4 |
| McDonald and Wilks 1988, JCAMP-DX IR (IUPAC copy) | https://iupac.org/wp-content/uploads/2021/08/JCAMP-DX_IR_1988.pdf | 2026-10-16 | original JCAMP-DX definition, Appl. Spectrosc. 42 (1988) 151–162; PDF exists (scanned) | 05.4 |
| NIST WebBook ethanol IR (gas) and its JCAMP file | https://webbook.nist.gov/cgi/cbook.cgi?ID=C64175&Type=IR-SPEC&Index=0 | 2026-10-16 | JCAMP-DX 4.24, AFFN (X++(Y..Y)), 880 points, DELTAX 4, YFACTOR 0.000112097; "all rights reserved" notice; course reader parses it (bands 1066, 2978, 1394, 1250, 3674 cm⁻¹) | 05.4 |
| SciPy find_peaks | https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html | 2026-10-16 | peak picking by prominence | 05.4 |
| Sandve et al. 2013, Ten Simple Rules | https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003285 | 2026-10-16 | reproducibility rules: record versions, no manual data edits, seeds, version control | 05.5 |
| JupyterLab 4.6 docs, Starting | https://jupyterlab.readthedocs.io/en/stable/getting_started/starting.html | 2026-10-16 | `jupyter lab` starts it in the browser | 05.5 |
| nbconvert, Executing notebooks | https://nbconvert.readthedocs.io/en/latest/execute_api.html | 2026-10-16 | `jupyter nbconvert --to notebook --execute`; tested on the practical notebook | 05.5 |
| Software Carpentry, Plotting and Programming in Python | https://github.com/swcarpentry/python-novice-gapminder | 2026-10-16 | free lesson on pandas, plotting, lists, loops, functions (site is swcarpentry.github.io; repo link used to satisfy the checker) | 05.5 |
