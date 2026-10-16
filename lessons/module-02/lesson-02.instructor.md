# Instructor notes — 02.2 Derivatives as rates of change

- Objective: rate = −d[A]/dt as a slope, the five differentiation rules, and finite differences on real-looking data.
- Likely confusion: why the forward difference is biased even with perfect data (curvature, not noise). The worked example and SVG show the tangent vs secant.
- Misconception: "Smaller steps are always better." With noise the error grows like σ/h; show this by subsampling the data.
- Analogy: a car's speedometer (instantaneous) vs distance over trip time (average).
- Expected hands-on result: initial rate 3.77e-4 (true 4.00e-4), k ≈ 0.00395 1/s from rate vs c, k ≈ 0.00399 1/s from ln c fit.
- Extension: use every second point (h = 60 s) and every point; compare scatter of the rate plot. Try `np.gradient(c, t, edge_order=2)` and see the initial rate improve.
