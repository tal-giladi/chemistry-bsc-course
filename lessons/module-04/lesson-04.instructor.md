# Instructor notes — 04.4 Circuits, current and resistance

- Objective: Ohm's law, resistivity and conductivity, power, series/parallel, Kirchhoff as a linear system, EMF and internal resistance, meter connection, Faraday's law.
- Likely confusion: where a voltmeter goes (across) versus an ammeter (in series). The lesson avoids ammeters on purpose.
- Misconception: "Current is used up as it goes round the circuit." Current is conserved at every node; energy (voltage) is what drops across each resistor.
- Analogy: water pipes. Voltage is the pressure difference, current the flow, resistance the narrowness of the pipe; parallel pipes carry more total flow.
- Expected hands-on result (example data): Req = 568.3 Ω, I = 5.49 mA, VA predicted 1.924 V vs measured 1.921 V, VB 1.445 V vs 1.445 V; all resistor powers < 8 mW. Sim target (3.00 V, nominal values): VA = 1.84 V, VB = 1.38 V, 5.29 mA. Real builds: within ~1 % using measured R; up to 5 % with printed values.
- Safety: AA alkaline cells only, never mains, no shorting, no current range across the battery, no coin cells or Li-ion packs; WARNING box.
- Extension: add a fifth resistor from B back to the battery plus (a bridge) and extend the node matrix; or estimate the battery's internal resistance from Vs measured with and without the network (expect only a few mV difference at 5 mA, so a 47 Ω load is needed to see it).
