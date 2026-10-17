# Instructor notes — 09.2 Statistics: mean, standard deviation and confidence intervals

- **Objective:** compute mean, s, RSD and a t-based 95 % CI; run a one-sample t-test, an F-test with a pooled or Welch t-test, and Grubbs' test for one outlier; state conclusions in plain words.
- **Likely confusion:** s versus s/√n (spread of results versus uncertainty of the mean); the F-test uses variances, not standard deviations (quiz q3).
- **Misconception:** "not significant" means "no difference". The worked example shows the opposite can hide behind one gross error; the CI is the honest summary.
- **Analogy:** a court verdict. "Not guilty" is not "innocent"; it means the evidence was not strong enough. α is the rate of convicting the innocent.
- **Expected hands-on result:** simulation: about 19 of 20 intervals contain the true value (17–20 normal). Python: ISE Grubbs G = 2.21 > 2.02; after removal mean 24.39, s 0.233, t_exp 6.41, p = 0.0014; titration 24.96 ± 0.34, p = 0.79; F = 2.48 < 6.98; pooled t = 3.28, p = 0.0074. With `REMOVE_OUTLIERS = False`: ISE p = 0.51, F = 6.86 > 5.82, Welch t = 0.56, p = 0.59 — the bias disappears. Home: s = 0 on a 0.1 g scale; report d/√12 = 0.029 g.
- **Extension:** compute the power of the ISE test: how many replicates would be needed to detect a 0.3 mg/L bias with s = 0.25 at α = 0.05 and 80 % power (`statsmodels` is not pinned, so do it by simulation with numpy).
- **Scope:** the tests assume roughly normal data; mention robust statistics (median, MAD) only as a pointer.
