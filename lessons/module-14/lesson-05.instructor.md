# Instructor notes — 14.5 Signals, sampling and the Fourier transform

- Objective: the learner picks a sample rate and record length for a measurement, computes a spectrum of a phyphox recording with numpy, separates close peaks, and judges when a line width gives a valid Q.
- Likely confusion: sample rate (sets the highest frequency) versus record length (sets the resolution); zero-padding versus real resolution; amplitude versus power spectra when reading a half-maximum width.
- Misconception: "More samples per second gives a sharper spectrum." Only a longer record does. Also: "Aliased peaks look odd." They look exactly like real ones.
- Analogy: the wagon wheel in a film that seems to turn slowly backwards; the camera samples the wheel too rarely and sees an alias.
- Expected hands-on result: aliasing table 3.00, 1.00, 1.00, 0.60 Hz; 20 s pendulum record peaks near 0.719 and 0.825 Hz; 120 s record 0.7047, 0.7328, 0.7859 Hz (true 0.7044, 0.7326, 0.7860); without window extra side-lobe peaks; ringdown Q from spectrum 16, 45, 80 for 10, 30, 60 s against 110 from the time fit. Bottle: empty 0.5 L bottle 150 to 250 Hz, ratios near 1.15 and 1.41.
- Extension: record the coupled pendulums of 14.3 with the phone as bob 1 (bag padded to the same mass) for 3 minutes and find all three modes from one recording; compare with the stopwatch periods.
