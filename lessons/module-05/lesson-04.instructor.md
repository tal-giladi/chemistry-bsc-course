# Instructor notes — 05.4 Reading real instrument data

- Objective: read a messy European export with pandas 3 and an AFFN JCAMP-DX file with a small parser; check every read; fetch and cite a real NIST spectrum.
- Likely confusion: why `decimal=","` matters when `sep=";"` already "worked". Show `df.dtypes` and `df["A"] * 2` on the half-fixed read.
- Misconception: "No error means the data are right." Silent str columns and a forgotten YFACTOR are the classic counter-examples.
- Analogy: JCAMP-DX is a shipping manifest; NPOINTS and the line x values are the crate count and the seal numbers you check on delivery.
- Expected hands-on result: export 401 points, 350–750 nm, float64, 0 NaN, max 0.875 at 621 nm (band centre 629; shoulder at 580 pulls it). Synthetic IR: 880 points, max 0.917, bands 1066, 2970, 882, 1462, 1390 cm⁻¹. Real NIST ethanol (C64175, gas): 880 points, max 1.121, bands 1066, 2978, 1394, 1250, 3674 cm⁻¹.
- Watch for: learners on corporate networks where the NIST download is blocked; Parts A and B work offline.
- Extension: read a compressed JCAMP file with a maintained library and compare; or read a phyphox CSV export (Module 4 / 14) and resample it to even time steps.
