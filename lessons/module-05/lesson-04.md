---
id: "05.4"
module: 5
minutes: 20
practice_minutes: 60
prerequisites: ["05.2"]
objectives:
  - Read an instrument CSV export with metadata lines, semicolon separators and decimal commas into a pandas DataFrame with numeric columns.
  - Parse an AFFN JCAMP-DX spectrum, scale it with XFACTOR and YFACTOR, and rebuild its x axis.
  - Verify what was read (point count, axis range, data types, missing values) before using the data.
  - Download a real IR spectrum from the NIST Chemistry WebBook, cite it correctly and find its strongest bands.
volatility: implementation
sources:
  - title: "pandas 3.0.6 documentation, pandas.read_csv"
    url: https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html
  - title: "pandas 3.0.0 release notes (default string dtype, Copy-on-Write)"
    url: https://pandas.pydata.org/docs/whatsnew/v3.0.0.html
  - title: "McDonald and Wilks, JCAMP-DX: A Standard Form for Exchange of Infrared Spectra in Computer Readable Form, Applied Spectroscopy 42 (1988) 151-162 (IUPAC copy)"
    url: https://iupac.org/wp-content/uploads/2021/08/JCAMP-DX_IR_1988.pdf
  - title: "NIST Chemistry WebBook, Ethanol, IR spectrum (gas phase)"
    url: https://webbook.nist.gov/cgi/cbook.cgi?ID=C64175&Type=IR-SPEC&Index=0
  - title: "SciPy v1.18 manual, scipy.signal.find_peaks"
    url: https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html
last_verified: "2026-10-16"
---

# 05.4 · Reading real instrument data

Real data never arrive as a clean two-column file. A spectrophotometer export starts with ten lines of settings, uses semicolons and decimal commas because the PC is set to a European locale, and puts units inside the column names. Spectral libraries use JCAMP-DX, a text format from 1988 that is still the common exchange format for IR, UV-Vis, NMR and mass spectra. This lesson shows how to read both kinds of file into numpy and pandas, and how to check that what you read is what the instrument measured.

## Why it matters

A misread file does not always crash. It can silently give you numbers that look fine. Read a decimal-comma file as if it used points and pandas keeps the absorbances as text: the "maximum" is then picked alphabetically, and multiplying by 2 repeats the text instead of doubling the number. Forget the YFACTOR of a JCAMP file and every absorbance is ten thousand times too large. Fit a calibration to that and the result is wrong in a way no residual plot will reveal. The habit this lesson builds is simple: read, then check the shape, the types, the range and the point count, every time.

## Core ideas

> [!NOTE]
> File formats change slowly; JCAMP-DX 4.24 dates from 1988–1991 and is still what the NIST WebBook serves. Library behaviour changes faster: checked on 2026-10-16 against pandas 3.0.6, which (since 3.0.0, January 2026) stores text columns as a dedicated `str` type and uses Copy-on-Write. The NIST URLs and file layout were checked on the same date.

### pandas in brief

**pandas** stores a table as a **DataFrame**: named columns, each a numpy array with one type. `pd.read_csv` reads text tables and has an option for almost every quirk:

| Quirk in the file | Option |
|---|---|
| Lines of settings before the header | `skiprows=n` (or find `n` in code) |
| `;` between columns | `sep=";"` |
| `0,8752` instead of `0.8752` | `decimal=","` |
| Comment lines starting with `#` | `comment="#"` |
| `----` or `OVER` where a value is missing | `na_values=["----", "OVER"]` |
| Non-UTF-8 text from an old PC | `encoding="cp1252"` (or `"latin-1"`) |

Two pandas 3 behaviours matter here. A column that cannot be read as numbers becomes type `str`, not a number, without any warning. And under Copy-on-Write, `df["A"][mask] = 0` no longer changes `df`; write `df.loc[mask, "A"] = 0`.

### Check what you read

After every read, print four things: `df.shape` (rows, columns), `df.dtypes` (all numeric columns must be `float64` or `int64`), `df.isna().sum()` (missing values) and the min and max of the x column. Compare them with what you expect from the instrument settings: a scan from 350 to 750 nm in 1 nm steps must have 401 rows.

### JCAMP-DX

A **JCAMP-DX** file is plain text made of **labelled data records**. Each starts with `##LABEL=` and a value:

```text
##TITLE=Ethanol
##XUNITS=1/CM
##YUNITS=ABSORBANCE
##XFACTOR=1.0
##YFACTOR=0.000112097
##FIRSTX=450.0
##LASTX=3966.0
##DELTAX=4.0
##NPOINTS=880
##XYDATA=(X++(Y..Y))
450.0 149 402 451 319 274 248 174 256 130 148
490.0 135 190 143 195 108 29 114 109 56 74
...
##END=
```

`(X++(Y..Y))` means: each line starts with an x value, followed by several y values at equally spaced x, each step being DELTAX. The numbers are stored as integers to save space; the true values are `y = integer × YFACTOR` and `x = number × XFACTOR`. Plain numbers, as here, are called **AFFN** (ASCII free-format numeric). The standard also allows **compressed** forms (named SQZ, DIF and DUP) that replace digits and signs by letters and symbols, such as `@`, `A`–`I` or `%`; reading those needs a full library. A `$$` starts a comment. The x at the start of each line is a checkpoint: it must equal FIRSTX plus DELTAX times the number of y values read so far.

So a reader does three things: collect the labels, turn the data lines into numbers, and check the result against NPOINTS and the line checkpoints.

### Real spectra and their terms of use

The **NIST Chemistry WebBook** offers thousands of IR spectra as JCAMP-DX downloads. NIST states that the data compilation is copyrighted ("all rights reserved") by the U.S. Secretary of Commerce, so this course does not copy their files into the repo. You download one for your own study with a small script and cite it. The SDBS library (Module 17) has stricter terms and is browsed online only.

## Worked example

### 1. The UV-Vis export

The first lines of `uvvis_export.csv` (simulated, in the layout of a typical instrument PC export):

```text
Instrument;Example UV-Vis (simulated data for this course)
Sample;Blue drink, diluted 1:10
...
Path length [cm];1,000
Scan speed [nm/min];600
Slit width [nm];2,0

Wavelength [nm];Absorbance [A]
350,0;0,0072
351,0;0,0098
```

`pd.read_csv("uvvis_export.csv")` stops with `ParserError: Expected 2 fields in line 10, saw 3`, because the comma in `350,0` looks like a column separator. Adding `sep=";", skiprows=8` reads without error, but `df.dtypes` shows both columns as `str`, and `df["Absorbance [A]"] * 2` turns `0,0072` into `0,00720,0072`. The full fix:

```python
lines = Path(path).read_text(encoding="utf-8").splitlines()
start = next(i for i, s in enumerate(lines) if s.startswith("Wavelength"))   # 8
df = pd.read_csv(path, sep=";", decimal=",", skiprows=start)
df.columns = ["wavelength_nm", "A"]
```

Checks: 401 rows, 350–750 nm, both columns `float64`, no missing values. The maximum is $A = 0.875$ at 621 nm. Finding the start line in code, rather than typing `skiprows=8`, keeps the script working when the instrument adds one more settings line.

### 2. The scale factor in a real file

In the NIST ethanol file, the third y value on the first line is 451 and YFACTOR is 0.000112097, so the absorbance at $450 + 2 \times 4 = 458$ cm⁻¹ is $451 \times 0.000112097 = 0.0506$. The file's MAXY of 1.12097 corresponds to the integer 10000, which is how the scale was chosen. Without YFACTOR you would report a peak absorbance of 10000.

## Hands-on

What you need: your environment from [05.1](lesson-01.md), `labs/module-05/lesson04_reading.py`, `uvvis_export.csv` and `example_ir.jdx`. For Part C, internet access. Time: about 60 minutes.

### Part A — the export (20 min)

Fill in `read_export(path)`: find the header line, put the `key;value` lines above it into a dictionary, read the table with the right `sep`, `decimal` and `skiprows`, and rename the columns.

### Part B — a JCAMP-DX reader (25 min)

Finish the data loop in `read_jcamp(path)`: take the numbers on each line, keep the first as the line's x checkpoint and add the rest to the list of y values, then scale by YFACTOR. The checks against NPOINTS and the checkpoints are already written. Run:

```bash
..\..\.venv\Scripts\python lesson04_reading.py
```

How you know it worked: Part 1 prints 401 points, 350–750 nm, both columns `float64`, 0 missing values, maximum 0.875 at 621 nm. Part 2 prints 880 points from 450 to 3966 cm⁻¹ and the strongest bands at 1066, 2970, 882, 1462 and 1390 cm⁻¹. The plot `runs/lesson04_reading.png` shows the IR spectrum with high wavenumber on the left, the usual convention.

### Part C — a real NIST spectrum (15 min)

```bash
..\..\.venv\Scripts\python fetch_nist_ir.py
..\..\.venv\Scripts\python lesson04_reading.py data/downloaded/ethanol_ir.jdx
```

The first command downloads the gas-phase IR spectrum of ethanol (about 4 KB) from the [NIST WebBook](https://webbook.nist.gov/cgi/cbook.cgi?ID=C64175&Type=IR-SPEC&Index=0) into the git-ignored `data/downloaded/` folder. Expected: 880 points, maximum absorbance 1.121, strongest bands near 1066 cm⁻¹ (C–O stretch), 2978 cm⁻¹ (C–H stretch), 1394 and 1250 cm⁻¹, and a weak 3674 cm⁻¹ band (the O–H stretch of free, gas-phase molecules; in liquid ethanol hydrogen bonding moves it to a broad band near 3300 cm⁻¹). Record the citation the script prints in your notebook. Try a second compound: acetone is `C67641`.

<details><summary>Reference solution</summary>

```python
def read_export(path):
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith("Wavelength"))
    meta = {}
    for line in lines[:start]:
        if ";" in line:
            key, value = line.split(";", 1)
            meta[key.strip()] = value.strip()
    df = pd.read_csv(path, sep=";", decimal=",", skiprows=start)
    df.columns = ["wavelength_nm", "A"]
    return meta, df
```

Inside the loop of `read_jcamp`:

```python
        nums = [float(n) for n in NUMBER.findall(line)]
        line_x.append((nums[0] * xf, len(ys)))
        ys.extend(nums[1:])
    y = np.array(ys) * yf
```

The maximum at 621 nm is not the centre of the main band (629 nm in the model that made the data): a shoulder at 580 nm adds to the blue side and pulls the peak. A maximum is a property of the summed spectrum, not of one band. Full code: `labs/module-05/lesson04_reading_solution.py`.

</details>

## Common mistakes

- Reading a decimal-comma file without `decimal=","`. pandas 3 keeps the column as `str`, with no warning. Always print `df.dtypes`.
- Hard-coding `skiprows=8`. One extra settings line from a firmware update and you skip a data row or read a setting as data. Find the header line in code.
- Forgetting YFACTOR or XFACTOR in JCAMP-DX. Check the maximum against the `##MAXY` label.
- Rebuilding x from FIRSTX and LASTX with `linspace` but the wrong count. Use NPOINTS and DELTAX, and check the line checkpoints.
- Assuming every JCAMP file is AFFN. If you see letters such as `@`, `J` or `%` in the data lines, the file is compressed; use a full reader rather than guessing.
- Committing downloaded library spectra to a public repo. Respect the source's terms; store a download script and a citation instead.

## Key takeaways

- `pd.read_csv` has an option for each common export quirk: `sep`, `decimal`, `skiprows`, `comment`, `na_values`, `encoding`.
- In pandas 3 a misread numeric column silently becomes `str`; check dtypes, shape, range and missing values after every read.
- JCAMP-DX AFFN files are labelled text: x at the start of each line, y values after it, real values = integers × YFACTOR.
- NPOINTS and the per-line x checkpoints let your reader prove that it read the file correctly.
- Download library spectra with a script, cite them, and do not redistribute them.

## Sources

- [pandas.read_csv (pandas 3.0.6)](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html) — the options for separators, decimals, skipped lines, comments and missing values.
- [pandas 3.0.0 release notes](https://pandas.pydata.org/docs/whatsnew/v3.0.0.html) — default `str` dtype and Copy-on-Write.
- [McDonald and Wilks 1988, JCAMP-DX for infrared spectra (IUPAC copy)](https://iupac.org/wp-content/uploads/2021/08/JCAMP-DX_IR_1988.pdf) — the original definition of the format and its labels.
- [NIST Chemistry WebBook, ethanol IR spectrum](https://webbook.nist.gov/cgi/cbook.cgi?ID=C64175&Type=IR-SPEC&Index=0) — the real spectrum used in Part C and its copyright statement.
- [scipy.signal.find_peaks (SciPy 1.18)](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html) — peak picking by prominence.
