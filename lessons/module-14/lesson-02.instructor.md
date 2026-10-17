# Instructor notes — 14.2 Damping, anharmonicity and the Q factor

- Objective: the learner extracts the damping rate and Q from a phyphox ringdown, compares a low-drag and a high-drag set-up, and detects anharmonicity as a frequency drift with amplitude.
- Likely confusion: gamma (amplitude decay rate) versus 2 gamma (energy decay rate); omega versus f inside Q; why acceleration data can be used when the model is written for displacement.
- Misconception: "Damping lowers the frequency a lot." For Q of 10 or more the shift of omega_d below omega_0 is under 0.1 %; frequency drift in a ringdown is almost always anharmonicity or a second motion.
- Analogy: a playground swing with chains that go slightly slack at the top of a big swing: big swings take a little longer, small swings are back on schedule, exactly like a softening bond.
- Expected hands-on result: example data: spring f_d 1.401 Hz, gamma 0.0400 1/s (peaks 0.039), Q 110; card gamma 0.301 1/s, Q 14.6; band f 1.968 to 2.000 Hz (+1.65 %), Q 51, peak-method gamma biased low (0.113 vs 0.123). Worked example: beta about -46 1/m^2 (true value in make_data.py: -40; the window averaging explains the difference).
- Extension: record a pendulum (phone in a padded bag on a 1 m string, over a bed) at 10, 20 and 30 degree starts and compare the period change with T0 (1 + theta0^2/16).
