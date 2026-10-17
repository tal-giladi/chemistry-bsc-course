# Instructor notes — 09.4 Calibration, linear regression and detection limits

- **Objective:** design and judge an external calibration; compute LOD/LOQ from blanks and from the regression; report low results in three tiers; detect and correct a matrix effect with standard additions.
- **Likely confusion:** the LOD is a concentration, computed from a signal (blank mean + 3s) divided by the slope; learners mix the signal and concentration forms. Also: IUPAC 3s versus ICH 3.3σ — both are fine if stated.
- **Misconception:** "a result below the LOD is zero". It means "not distinguishable from zero with this method"; the analyte may well be present (type II error is 50 % at the LOD).
- **Analogy:** hearing a whisper in a noisy room. The LOD is the softest whisper you notice reliably; the LOQ is the softest one you can understand word for word. Standard additions is asking the speaker to repeat louder in the same room.
- **Expected hands-on result:** A = 0.0032 + 2.905 c, s_r = 0.0030; blanks s = 0.0023; LOD 0.0024, LOQ 0.0080 mg/L; ICH 0.0034 / 0.0104; well 1 0.0614 ± 0.0008 mg/L (true 0.0620); farm well SA slope 2.543 (0.88 of external), 0.0417 ± 0.0010 mg/L vs external 0.0348 (true 0.0400). Without the two lowest standards: intercept 0.0063, well 1 0.0607 ± 0.0010. Pencil: 0.0017 (< LOD), 0.0072 (between LOD and LOQ).
- **Extension:** fit the same data with `curve_fit` and `absolute_sigma=False` (Lesson 05.3) and compare; or simulate 1000 blank sets to show how much an LOD from only 3 blanks scatters.
- **Scope:** the Griess data are simulated and the slope is not a validated method value; real nitrite methods (e.g. EPA, ISO) have their own ranges and limits.
