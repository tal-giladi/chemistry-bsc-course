"""Generate the example data for the Module 14 labs (seeded, so the files never change).

Run:   py make_data.py
The models and their true parameters are written here so you can check your answers.
The data are realistic but NOT measured. Replace them with your own measurements.
"""
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

HERE = Path(__file__).resolve().parent
rng = np.random.default_rng(1414)
G = 9.795  # m/s^2, close to local g in Israel


def write(name, lines):
    (HERE / name).write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def spring():
    """Steel extension spring, true k = 24.0 N/m, spring mass 30 g (effective mass m_s/3 = 10 g).
    Static: water-bottle masses on the spring, length read on a tape measure (sd 1 mm).
    Dynamic: phone (195 g) in a zip bag (5 g) plus added masses, period from phyphox Spring
    (sd 0.003 s per run)."""
    k, m_s = 24.0, 0.030
    L0 = 0.152
    lines = ["mass_kg,length_m"]
    for m in (0.0, 0.050, 0.100, 0.150, 0.200, 0.250, 0.300):
        lines.append(f"{m:.3f},{L0 + m * G / k + rng.normal(0, 0.001):.3f}")
    write("spring_static_example.csv", lines)

    lines = ["mass_kg,trial,period_s"]
    for added in (0.0, 0.050, 0.100, 0.150, 0.200):
        m = 0.200 + added
        T = 2 * np.pi * np.sqrt((m + m_s / 3) / k)
        for trial in (1, 2, 3):
            lines.append(f"{m:.3f},{trial},{T + rng.normal(0, 0.003):.4f}")
    write("spring_dynamic_example.csv", lines)


def ringdown(name, m, k, gamma, beta, x0, t_end=60.0, fs=100.0):
    """Phone on a spring, released from x0 (m). Equation of motion
    x'' = -2 gamma x' - (k/m) x (1 + beta x^2), beta in 1/m^2 (beta < 0 softens at large amplitude).
    Written like a phyphox 'Acceleration (without g)' CSV export: time, then x, y, z, absolute.
    The spring axis is the phone's z axis. Sample times have a little jitter, as real sensors do."""
    w2 = k / m

    def f(t, y):
        x, v = y
        return [v, -2 * gamma * v - w2 * x * (1 + beta * x * x)]

    t = np.arange(0, t_end, 1 / fs) + rng.normal(0, 0.0005, int(t_end * fs))
    t = np.sort(np.clip(t, 0, None))
    t[0] = 0.0
    sol = solve_ivp(f, (0, t_end), [x0, 0.0], t_eval=t, rtol=1e-10, atol=1e-12)
    x, v = sol.y
    az = -2 * gamma * v - w2 * x * (1 + beta * x * x) + rng.normal(0, 0.03, t.size)
    ax = 0.15 * np.sin(2 * np.pi * 0.72 * t) * np.exp(-t / 30) + rng.normal(0, 0.03, t.size)
    ay = rng.normal(0, 0.03, t.size)
    lines = ['"Time (s)","Acceleration x (m/s^2)","Acceleration y (m/s^2)","Acceleration z (m/s^2)",'
             '"Absolute acceleration (m/s^2)"']
    for row in zip(t, ax, ay, az, np.sqrt(ax**2 + ay**2 + az**2)):
        lines.append(",".join(f"{val:.6f}" if i == 0 else f"{val:.4f}" for i, val in enumerate(row)))
    write(name, lines)


def ringdowns():
    """Bare spring: m_eff = 0.310 kg on k = 24.0 N/m, gamma = 0.040 1/s, Q = omega0/(2 gamma) = 110.
    Same spring with a 20 cm cardboard disc under the bag: gamma = 0.30 1/s, Q = 14.7.
    Loop of elastic hair bands: k = 49.0 N/m, gamma = 0.12 1/s, softening beta = -40 1/m^2."""
    ringdown("ringdown_spring.csv", 0.310, 24.0, 0.040, 2.0, 0.030)
    ringdown("ringdown_card.csv", 0.310, 24.0, 0.30, 2.0, 0.030, t_end=20.0)
    ringdown("ringdown_band.csv", 0.310, 49.0, 0.12, -40.0, 0.045, t_end=30.0)


def pendulums():
    """Three equal pendulums, L = 0.500 m, neighbours joined by thin rubber bands.
    omega^2 = g/L + c * {0, 1, 3} with c = 1.60 1/s^2. Time for 10 swings, hand stopwatch (sd 0.08 s)."""
    w0sq, c = G / 0.500, 1.60
    lines = ["mode,trial,t10_s"]
    for mode, lam in ((1, 0), (2, 1), (3, 3)):
        T = 2 * np.pi / np.sqrt(w0sq + c * lam)
        for trial in (1, 2, 3):
            lines.append(f"{mode},{trial},{10 * T + rng.normal(0, 0.08):.2f}")
    write("coupled_pendulums_example.csv", lines)

    # Phone (in a bag padded to the same mass) as bob 1; pendulum 1 released alone from 4 cm.
    # x1 = (1/3) cos w1 t + (1/2) cos w2 t + (1/6) cos w3 t, each mode damped with gamma = 0.008 1/s.
    fs, t_end, A, gam = 100.0, 120.0, 0.04, 0.008
    t = np.arange(0, t_end, 1 / fs)
    a = np.zeros_like(t)
    for weight, lam in ((1 / 3, 0), (1 / 2, 1), (1 / 6, 3)):
        w = np.sqrt(w0sq + c * lam)
        a += -A * weight * w**2 * np.cos(w * t) * np.exp(-gam * t)
    a += rng.normal(0, 0.01, t.size)
    lines = ['"Time (s)","Acceleration x (m/s^2)"']
    lines += [f"{ti:.4f},{ai:.5f}" for ti, ai in zip(t, a)]
    write("pendulum_phone_example.csv", lines)


def rlc():
    """Series RLC driven by a phone's headphone output (phyphox Tone Generator, sine).
    True: L = 10.3 mH (10 mH nominal, +3 %), C = 0.970 uF (1.0 uF nominal, -3 %), R = 10.1 ohm.
    Coil DC resistance 28 ohm, but its effective resistance at kHz is 33 ohm (core losses),
    so R_total = 43.1 ohm. f0 = 1593 Hz, Q = sqrt(L/C)/R_total = 2.39.
    Source: 160 mV rms open circuit (volume turned down so every reading fits the 200 mV range),
    output resistance 20 ohm. The cheap meter rolls off above
    about 3 kHz; the roll-off multiplies Vin and VR alike, so the ratio is unaffected."""
    L, C, R, Rcoil = 10.3e-3, 0.970e-6, 10.1, 33.0
    Vs, Rs = 160.0, 20.0
    lines = ["f_Hz,Vin_mV,VR_mV"]
    for f in (300, 400, 500, 650, 800, 1000, 1200, 1400, 1500, 1600, 1700, 1800, 2000, 2300,
              2700, 3200, 4000, 5000, 6500, 8000):
        w = 2 * np.pi * f
        Z = R + Rcoil + 1j * (w * L - 1 / (w * C))
        I = Vs / (Z + Rs)
        meter = 1 / np.sqrt(1 + (f / 3000) ** 2)
        vin = abs(I * Z) * meter * (1 + rng.normal(0, 0.004))
        vr = abs(I * R) * meter * (1 + rng.normal(0, 0.004))
        lines.append(f"{f},{vin:.1f},{vr:.1f}")
    write("rlc_example.csv", lines)


if __name__ == "__main__":
    spring()
    ringdowns()
    pendulums()
    rlc()
    print("Example data written to", HERE)
