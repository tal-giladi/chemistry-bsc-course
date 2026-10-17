/* kinetics simulation: integrated rate laws and the order test (with Euler's method),
 * consecutive first-order reactions A -> B -> C with the steady-state approximation,
 * Arrhenius / Eyring analysis, a phone-camera dye-fading experiment in dilute bleach
 * (pseudo-first-order isolation) and Michaelis–Menten enzyme kinetics with inhibition.
 * Uses ../common/sim.js (global Sim).
 *
 * Data and sources:
 *  - R, kB, h: CODATA 2022 (Sim.C).
 *  - Worked-example values: first order k = 0.0040 s-1, c0 = 0.100 M; second order k = 0.54 L mol-1 s-1,
 *    c0 = 0.0100 M (Lesson 03.3); k1 = 0.150, k2 = 0.050 min-1, A0 = 10.0 mM (Lesson 03.5).
 *  - N2O5 -> NO2 + NO3 high-pressure limit: Ea 92.5 kJ/mol, A 1.05e15 s-1 (IUPAC 1997 evaluation,
 *    NIST SRD 17; Lesson 22.4).
 *  - Dye fading (Lesson 23.4 example, illustrative, not measured): k = 0.559 L mol-1 s-1 at 20 °C
 *    (k' = 2.99e-3 s-1 with 2.0 mL of 0.54 M bleach in 200 mL), Ea = 50 kJ/mol, A0 = 0.613, A∞ = 0.012.
 *    About 8 OCl- per dye molecule (illustrative) makes isolation fail with very little bleach.
 *    An open cup relaxes to room temperature with a time constant of about 40 min (illustrative).
 *  - Invertase Km 16.7 mM (Michaelis and Menten 1913, via Johnson and Goody 2011; Lessons 22.5, 29.2).
 */
(function () {
  "use strict";
  var R = Sim.C.R, S = Sim.stats;

  var PRESETS = {
    "first-order": {
      title: "First-order decay", tab: "orders", n: 1, k: 0.0040, c0: 0.100, tend: 900,
      what: "For dc/dt = −kc the concentration falls exponentially, c = c₀e<sup>−kt</sup>, and ln c falls in a straight line with slope −k. The half-life t½ = ln 2/k is the same for every starting concentration: the first half-life and the second are equal.",
      task: "Change k and c₀ and watch which quantities change the half-life. Then look at the three straight-line plots of the readings and decide which one is straight; switch on Euler's method with h = 60 s and halve h a few times.",
      target: "t½ = 173 s for k = 0.0040 s⁻¹ whatever c₀; the ln c plot straight with R² near 1 and random residuals; the Euler error at the end roughly halving each time h halves."
    },
    "second-order": {
      title: "Second-order decay", tab: "orders", n: 2, k: 0.54, c0: 0.0100, tend: 1500,
      what: "For 2A → products with dc/dt = −kc², 1/c rises in a straight line with slope k, and the half-life t½ = 1/(kc₀) depends on the starting concentration: each half-life is twice as long as the one before. That doubling is the fingerprint of second order.",
      task: "With k = 0.54 L mol⁻¹ s⁻¹ and c₀ = 0.0100 mol/L, read the first and second half-lives. Then decide from the readings which of the three plots is straight, and look at the residuals of the wrong ones.",
      target: "First half-life 185 s, second 370 s; the 1/c plot straight, with k ≈ 0.54 L mol⁻¹ s⁻¹ from its slope."
    },
    consecutive: {
      title: "Consecutive reactions A → B → C", tab: "consecutive", k1: 0.150, k2: 0.050,
      what: "B is made from A at the rate k₁A and lost at k₂B, so it rises, peaks at t<sub>max</sub> = ln(k₁/k₂)/(k₁ − k₂) and falls. If k₂ ≫ k₁, B stays small and nearly constant after a short induction period: the steady-state approximation, which predicts C = A₀(1 − e<sup>−k₁t</sup>).",
      task: "Move k₁ and k₂ and watch the peak of B move. Then compare the exact C with the steady-state approximation for k₂ = 20 k₁ and for k₂ = k₁. Finally show B with the two constants swapped, scaled to the same peak.",
      target: "t<sub>max</sub> = 11.0 min and B<sub>max</sub> = 5.77 mM for k₁ = 0.150 and k₂ = 0.050 min⁻¹; the largest SSA error about 0.04 A₀ for k₂ = 20k₁ and 0.37 A₀ for k₂ = k₁; the swapped B curve is identical once scaled."
    },
    arrhenius: {
      title: "Arrhenius plot", tab: "arrhenius", ea: 50, la: 10,
      what: "k = A e<sup>−E<sub>a</sub>/RT</sup>: a plot of ln k against 1/T is a straight line with slope −E<sub>a</sub>/R. The larger E<sub>a</sub>, the more strongly a few kelvin change the rate. Real plots curve when the prefactor depends on temperature (k = A(T/298)ⁿe<sup>−E/RT</sup> has a local E<sub>a</sub> = E + nRT).",
      task: "Change E<sub>a</sub> and A and watch how strongly a 10 K change moves the rate. Find the E<sub>a</sub> at which the rate doubles from 25 to 35 °C. Then measure six rate constants with 5 % scatter and fit them; compare the uncertainty of E<sub>a</sub> with that of A.",
      target: "About 53 kJ/mol doubles the rate per 10 K near room temperature; from 25 to 37 °C, E<sub>a</sub> = 100 kJ/mol gives a factor of about 4.8 and 50 kJ/mol about 2.2."
    },
    "dye-fading": {
      title: "Food dye fading in dilute bleach", tab: "dye",
      what: "Hypochlorite destroys the blue dye: v = k[D][OCl⁻]. With hypochlorite in large excess its concentration hardly changes, so the dye decays as a single exponential with k′ = k[OCl⁻] (pseudo-first-order). The phone measures a pseudo-absorbance A = −log₁₀(I/I<sub>blank</sub>) that is proportional to [D], plus a small offset A∞.",
      task: "Run three cases: 2 mL bleach at 20 °C, 4 mL at 20 °C, and 2 mL starting at 30 °C. Read k′ from each, check that doubling the bleach doubles k′, and estimate E<sub>a</sub> from the mean temperatures. Then try 0.2 mL of bleach (photograph for 60–120 min: it is slow) and watch the decay stop being a single exponential as the hypochlorite runs out.",
      target: "k′ about 3.0 × 10⁻³ s⁻¹ (t½ about 3.9 min) at 2 mL and 20 °C; order in hypochlorite n ≈ 1; E<sub>a</sub> near 50 kJ/mol when you use the mean temperature of the warm run."
    },
    enzyme: {
      title: "Enzyme saturation (Michaelis–Menten)", tab: "enzyme", km: 16.7, vm: 3.9,
      what: "An enzyme saturates: at [S] ≪ K<sub>m</sub> the rate is nearly proportional to [S] (first order), at [S] ≫ K<sub>m</sub> it approaches V<sub>max</sub> (zero order). K<sub>m</sub> is the [S] that gives half of V<sub>max</sub>. A competitive inhibitor raises the apparent K<sub>m</sub>; a noncompetitive one lowers V<sub>max</sub>.",
      task: "Set any K<sub>m</sub> and V<sub>max</sub> and find the [S] that gives 0.5, 0.8 and 0.9 V<sub>max</sub>, as multiples of K<sub>m</sub>. Compare a curve with K<sub>m</sub> doubled (competitive, [I] = K<sub>i</sub>) and one with V<sub>max</sub> halved (noncompetitive, [I] = K<sub>i</sub>). Then measure rates with the good and the poor design and compare the nonlinear fit with Lineweaver–Burk.",
      target: "1 K<sub>m</sub>, 4 K<sub>m</sub> and 9 K<sub>m</sub> (99 K<sub>m</sub> for 99 %); the nonlinear K<sub>m</sub> within its uncertainty of the true value with the good design."
    }
  };

  var preset = Sim.preset(PRESETS, "first-order");
  var seed = Sim.seedFromQuery(22);
  var csvFns = {}, tabName = preset.tab;

  Sim.label();
  Sim.presetBox(Sim.$("#preset"), preset);
  function showSeed() { Sim.$$(".seed").forEach(function (e) { e.textContent = String(seed); }); }
  showSeed();

  function num(id) { return parseFloat(Sim.$("#" + id).value); }
  function chk(id) { return !!Sim.$("#" + id).checked; }
  function kvFill(box, rows) {
    box.textContent = "";
    rows.forEach(function (r) { box.appendChild(Sim.el("div", { html: r[0] })); box.appendChild(Sim.el("div", { html: r[1], class: r[2] || null })); });
  }
  function lg(id) { return Math.pow(10, num(id)); }
  function setLog(id, value) { Sim.$("#" + id).value = String(Math.log10(value)); }

  // golden-section minimum of f on [a, b]
  function golden(f, a, b, n) {
    var g = (Math.sqrt(5) - 1) / 2, c = b - g * (b - a), d = a + g * (b - a), fc = f(c), fd = f(d);
    for (var i = 0; i < (n || 80); i++) {
      if (fc < fd) { b = d; d = c; fd = fc; c = b - g * (b - a); fc = f(c); }
      else { a = c; c = d; fc = fd; d = a + g * (b - a); fd = f(d); }
    }
    return (a + b) / 2;
  }

  /* ======================= RATE LAWS AND ORDER ======================= */
  var oPlot = Sim.plot(Sim.$("#o-plot"), { xLabel: "t / s", yLabel: "c / mol L⁻¹" });
  var oL = Sim.plot(Sim.$("#o-lplot"), { xLabel: "t / s", yLabel: "ln c" });
  var oR = Sim.plot(Sim.$("#o-rplot"), { xLabel: "t / s", yLabel: "residual" });
  var oMeas = 0;
  var K_UNITS = { 0: "mol L⁻¹ s⁻¹", 1: "s⁻¹", 2: "L mol⁻¹ s⁻¹" };

  function cOf(n, k, c0, t) {
    if (n === 0) return Math.max(0, c0 - k * t);
    if (n === 1) return c0 * Math.exp(-k * t);
    return 1 / (1 / c0 + k * t);
  }
  function halfLife(n, k, c) { return n === 0 ? c / (2 * k) : n === 1 ? Math.LN2 / k : 1 / (k * c); }

  function ordersDraw() {
    var n = parseInt(Sim.$("#o-n").value, 10), k = lg("o-k"), c0 = num("o-c0"), tend = Math.max(10, num("o-tend"));
    Sim.$("#o-k-label").textContent = "k / " + K_UNITS[n];
    Sim.$("#o-k-out").textContent = Sim.sig(k, 3);
    Sim.$("#o-c0-out").textContent = c0.toFixed(4);
    var curve = [];
    for (var i = 0; i <= 300; i++) { var t = tend * i / 300; curve.push([t, cOf(n, k, c0, t)]); }
    // readings
    var r = Sim.rng(seed + 13 * oMeas), np = Math.max(5, Math.min(61, Math.round(num("o-npts")))), sd = Math.max(0, num("o-noise"));
    var data = [];
    for (var j = 0; j < np; j++) { var tj = tend * j / (np - 1); data.push([tj, cOf(n, k, c0, tj) + r.normal(0, sd)]); }
    var series = [{ type: "line", color: "s1", label: "exact", data: curve }, { type: "points", color: "s2", label: "readings", data: data }];
    // successive half-lives
    var info = [], tAcc = 0, cc = c0, hl = [];
    for (var h = 0; h < 4; h++) { var th = halfLife(n, k, cc); if (tAcc + th > tend * 1.0001) break; tAcc += th; cc /= 2; hl.push(th); series.push({ type: "vline", x: tAcc, color: "muted", dash: [3, 4] }); }
    info.push(["half-life now", Sim.sig(halfLife(n, k, c0), 3) + " s" + (n === 1 ? " (ln 2/k: independent of c₀)" : n === 2 ? " (1/(kc₀))" : " (c₀/2k)")]);
    if (hl.length) info.push(["successive half-lives", hl.map(function (x) { return Sim.sig(x, 3); }).join(", ") + " s"]);
    info.push(["c at the end", Sim.sig(cOf(n, k, c0, tend), 4) + " mol/L (" + (100 * cOf(n, k, c0, tend) / c0).toFixed(1) + " % left)"]);
    if (chk("o-euler")) {
      var step = Math.max(1e-3, num("o-h")), ce = c0, te = 0, eu = [[0, c0]], nsteps = Math.min(20000, Math.ceil(tend / step));
      for (var s2 = 0; s2 < nsteps; s2++) {
        var f = n === 0 ? (ce > 0 ? -k : 0) : n === 1 ? -k * ce : -k * ce * ce;
        ce += step * f; te += step; eu.push([te, ce]);
      }
      series.push({ type: "line", color: "s4", width: 1.5, dash: [6, 3], label: "Euler, h = " + Sim.sig(step, 3) + " s", data: eu });
      var exactEnd = cOf(n, k, c0, te);
      info.push(["Euler at t = " + Sim.sig(te, 4) + " s", Sim.sig(ce, 5) + " mol/L; exact " + Sim.sig(exactEnd, 5) + "; error " + Sim.sig(ce - exactEnd, 2)]);
      if (n === 1) info.push(["hk", Sim.sig(step * k, 3) + (step * k > 2 ? ": unstable, the steps oscillate and grow" : step * k > 1 ? ": the steps overshoot below zero" : ""), step * k > 1 ? "miss" : null]);
    }
    oPlot.draw(series, { xMin: 0, xMax: tend });
    kvFill(Sim.$("#o-info"), info);
    // the three linearisations
    var tb = Sim.$("#o-fits tbody"), sel = Sim.$("#o-lin").value, which = { c: 0, ln: 1, inv: 2 };
    tb.textContent = "";
    var lin = [["c", function (c) { return c; }, "c against t"], ["ln", function (c) { return c > 0 ? Math.log(c) : NaN; }, "ln c against t"], ["inv", function (c) { return c > 0 ? 1 / c : NaN; }, "1/c against t"]];
    var selFit = null, selPts = null;
    lin.forEach(function (L, idx) {
      var xs = [], ys = [];
      data.forEach(function (p) { var y = L[1](p[1]); if (isFinite(y)) { xs.push(p[0]); ys.push(y); } });
      var f = xs.length >= 3 ? S.linfit(xs, ys) : null;
      var kk = f ? (idx === 2 ? f.b : -f.b) : NaN;
      tb.appendChild(Sim.el("tr", { class: L[0] === sel ? "hit" : null }, Sim.el("td", { text: L[2] }), Sim.el("td", { text: f ? Sim.sig(f.b, 3) : "—" }),
        Sim.el("td", { text: f ? Sim.sig(kk, 3) + " " + K_UNITS[idx] : "—" }), Sim.el("td", { text: f ? f.r2.toFixed(4) : "—" })));
      if (L[0] === sel) { selFit = f; selPts = xs.map(function (x, q) { return [x, ys[q]]; }); }
    });
    var yl = { c: "c / mol L⁻¹", ln: "ln(c / mol L⁻¹)", inv: "1/c / L mol⁻¹" }[sel];
    if (selFit) {
      oL.draw([{ type: "points", color: "s2", data: selPts }, { type: "line", color: "s1", data: [[0, selFit.a], [tend, selFit.a + selFit.b * tend]] }], { yLabel: yl, xMin: 0, xMax: tend });
      oR.draw([{ type: "hline", y: 0, color: "muted" }, { type: "points", color: "s4", data: selPts.map(function (p) { return [p[0], p[1] - selFit.a - selFit.b * p[0]]; }) }], { yLabel: "residual of " + yl.split(" /")[0], xMin: 0, xMax: tend });
    }
    csvFns.orders = function () { return { header: ["t_s", "c_mol_per_L"], rows: data.map(function (p) { return [+p[0].toFixed(3), +p[1].toPrecision(6)]; }), filename: "kinetics_order" + n + "_readings.csv" }; };
  }

  function ordersInit(p) {
    Sim.$("#o-n").value = String(p.n !== undefined ? p.n : 1);
    setLog("o-k", p.k || 0.0040);
    Sim.$("#o-c0").value = String(p.c0 || 0.100);
    Sim.$("#o-tend").value = String(p.tend || 900);
    Sim.$("#o-noise").value = String(+(0.005 * (p.c0 || 0.100)).toPrecision(2));
  }
  ordersInit(preset.tab === "orders" ? preset : PRESETS["first-order"]);
  Sim.$("#o-n").addEventListener("change", function () {
    var n = Sim.$("#o-n").value;
    // sensible starting values for each order
    if (n === "2") ordersInit(PRESETS["second-order"]); else if (n === "1") ordersInit(PRESETS["first-order"]); else ordersInit({ n: 0, k: 1e-4, c0: 0.050, tend: 600 });
    ordersDraw();
  });
  ["#o-k", "#o-c0"].forEach(function (q) { Sim.$(q).addEventListener("input", ordersDraw); });
  ["#o-tend", "#o-npts", "#o-noise", "#o-euler", "#o-h", "#o-lin"].forEach(function (q) { Sim.$(q).addEventListener("change", ordersDraw); });
  Sim.$("#o-measure").addEventListener("click", function () { oMeas++; ordersDraw(); });
  Sim.$("#o-rerun").addEventListener("click", function () { seed = Sim.newSeed(seed); showSeed(); ordersDraw(); });

  /* ======================= A -> B -> C ======================= */
  var cPlot = Sim.plot(Sim.$("#c-plot"), { xLabel: "t / min", yLabel: "concentration / mM" });

  function abc(k1, k2, A0, t) {
    var A = A0 * Math.exp(-k1 * t), B;
    if (Math.abs(k1 - k2) < 1e-9 * Math.max(k1, k2)) B = A0 * k1 * t * Math.exp(-k1 * t);
    else B = k1 * A0 / (k2 - k1) * (Math.exp(-k1 * t) - Math.exp(-k2 * t));
    return [A, B, A0 - A - B];
  }

  function consecDraw() {
    var k1 = lg("c-k1"), k2 = lg("c-k2"), A0 = num("c-a0"), tend = Math.max(1, num("c-tend"));
    Sim.$("#c-k1-out").textContent = Sim.sig(k1, 3);
    Sim.$("#c-k2-out").textContent = Sim.sig(k2, 3);
    var sa = [], sb = [], sc = [], ss = [], sw = [], maxErr = 0, tAtErr = 0;
    var same = Math.abs(k1 - k2) < 1e-9 * Math.max(k1, k2);
    var tmax = same ? 1 / k1 : Math.log(k1 / k2) / (k1 - k2);
    var Bmax = abc(k1, k2, A0, tmax)[1];
    for (var i = 0; i <= 400; i++) {
      var t = tend * i / 400, c = abc(k1, k2, A0, t);
      sa.push([t, c[0]]); sb.push([t, c[1]]); sc.push([t, c[2]]);
      var cs = A0 * (1 - Math.exp(-k1 * t));
      ss.push([t, cs]);
      if (Math.abs(cs - c[2]) > maxErr) { maxErr = Math.abs(cs - c[2]); tAtErr = t; }
      sw.push([t, abc(k2, k1, A0, t)[1] * (k1 / k2)]);
    }
    var series = [{ type: "line", color: "s1", label: "A", data: sa }, { type: "line", color: "s2", label: "B", data: sb }, { type: "line", color: "s3", label: "C", data: sc }];
    if (chk("c-ssa")) series.push({ type: "line", color: "s3", dash: [5, 4], width: 1.5, label: "C, steady state", data: ss });
    if (chk("c-swap")) series.push({ type: "line", color: "s6", dash: [2, 3], width: 2.5, label: "B, k₁ ↔ k₂, × k₁/k₂", data: sw });
    var pts = [];
    if (chk("c-data")) {
      var r = Sim.rng(seed + 5);
      for (var tt = 0; tt <= tend + 1e-9; tt += 2) { var cc = abc(k1, k2, A0, tt); pts.push([tt, cc[0] + r.normal(0, 0.1), cc[1] + r.normal(0, 0.1), cc[2] + r.normal(0, 0.1)]); }
      series.push({ type: "points", color: "s1", data: pts.map(function (p) { return [p[0], p[1]]; }) });
      series.push({ type: "points", color: "s2", data: pts.map(function (p) { return [p[0], p[2]]; }) });
      series.push({ type: "points", color: "s3", data: pts.map(function (p) { return [p[0], p[3]]; }) });
    }
    if (tmax <= tend) series.push({ type: "vline", x: tmax, color: "muted", dash: [3, 4] });
    cPlot.draw(series, { xMin: 0, xMax: tend, yMin: 0 });
    kvFill(Sim.$("#c-info"), [
      ["k₂/k₁", Sim.sig(k2 / k1, 3)],
      ["t<sub>max</sub>", Sim.sig(tmax, 3) + " min" + (same ? " (k₁ = k₂: B = A₀kte<sup>−kt</sup>, peak at 1/k)" : "")],
      ["B<sub>max</sub>", Sim.sig(Bmax, 3) + " mM (" + (100 * Bmax / A0).toFixed(1) + " % of A₀)"],
      ["eigenvalues of K", "−" + Sim.sig(k1, 3) + ", −" + Sim.sig(k2, 3) + ", 0 min⁻¹"],
      ["largest SSA error in C", Sim.sig(maxErr / A0, 3) + " A₀ (at t = " + Sim.sig(tAtErr, 3) + " min)", maxErr / A0 < 0.05 ? "hit" : "miss"],
      ["induction period", "a few times 1/k₂ = " + Sim.sig(1 / k2, 3) + " min"],
      ["mass balance", "A + B + C = " + A0.toFixed(2) + " mM at every t"]
    ]);
    csvFns.consecutive = function () {
      if (pts.length) return { header: ["t_min", "A_mM", "B_mM", "C_mM"], rows: pts.map(function (p) { return [p[0], +p[1].toFixed(4), +p[2].toFixed(4), +p[3].toFixed(4)]; }), filename: "consecutive_readings.csv" };
      return { header: ["t_min", "A_mM", "B_mM", "C_mM"], rows: sa.filter(function (p, i) { return i % 4 === 0; }).map(function (p, i) { var j = i * 4; return [+p[0].toFixed(3), +sa[j][1].toFixed(6), +sb[j][1].toFixed(6), +sc[j][1].toFixed(6)]; }), filename: "consecutive_exact.csv" };
    };
  }
  setLog("c-k1", preset.k1 || 0.150); setLog("c-k2", preset.k2 || 0.050);
  ["#c-k1", "#c-k2"].forEach(function (q) { Sim.$(q).addEventListener("input", consecDraw); });
  ["#c-a0", "#c-tend", "#c-ssa", "#c-swap", "#c-data"].forEach(function (q) { Sim.$(q).addEventListener("change", consecDraw); });
  Sim.$("#c-r20").addEventListener("click", function () { setLog("c-k2", 20 * lg("c-k1")); consecDraw(); });
  Sim.$("#c-r1").addEventListener("click", function () { setLog("c-k2", lg("c-k1")); consecDraw(); });
  Sim.$("#c-rerun").addEventListener("click", function () { seed = Sim.newSeed(seed); showSeed(); Sim.$("#c-data").checked = true; consecDraw(); });

  /* ======================= ARRHENIUS ======================= */
  var aPlot = Sim.plot(Sim.$("#a-plot"), { xLabel: "1000 K / T", yLabel: "ln(k / s⁻¹)" });
  var aMeas = null, aCount = 0;
  function kArr(T) { return Math.pow(10, num("a-la")) * Math.pow(T / 298.15, num("a-n")) * Math.exp(-num("a-ea") * 1000 / (R * T)); }

  function arrDraw() {
    var Ea = num("a-ea"), la = num("a-la"), n = num("a-n");
    Sim.$("#a-ea-out").textContent = Ea.toFixed(1);
    Sim.$("#a-la-out").textContent = la.toFixed(2);
    Sim.$("#a-n-out").textContent = n.toFixed(1);
    var T1 = num("a-t1") + 273.15, T2 = num("a-t2") + 273.15, tlo = num("a-tlo") + 273.15, thi = num("a-thi") + 273.15;
    if (!(thi > tlo)) { var tmp = tlo; tlo = thi; thi = tmp + 1; }
    var lo = Math.max(50, Math.min(tlo, T1, T2) - 10), hi = Math.max(thi, T1, T2) + 10, line = [];
    for (var i = 0; i <= 120; i++) { var T = 1 / (1 / hi + (1 / lo - 1 / hi) * i / 120); line.push([1000 / T, Math.log(kArr(T))]); }
    var series = [{ type: "line", color: "s1", label: "model", data: line }];
    series.push({ type: "points", color: "s3", size: 5, label: "T₁ and T₂", data: [[1000 / T1, Math.log(kArr(T1))], [1000 / T2, Math.log(kArr(T2))]] });
    var fitRows = [];
    if (aMeas) {
      series.push({ type: "points", color: "s2", label: "measured", data: aMeas.map(function (p) { return [1000 / p[0], Math.log(p[1])]; }) });
      var xs = aMeas.map(function (p) { return 1 / p[0]; }), ys = aMeas.map(function (p) { return Math.log(p[1]); });
      var f = S.linfit(xs, ys), fe = S.linfit(xs, aMeas.map(function (p) { return Math.log(p[1] / p[0]); }));
      var EaF = -f.b * R / 1000, uEa = f.ub * R / 1000, A = Math.exp(f.a), uA = A * f.ua;
      var corr = f.cov / (f.ua * f.ub);
      series.push({ type: "line", color: "s2", dash: [5, 4], width: 1.5, label: "fit", data: [[1000 / lo, f.a + f.b / lo], [1000 / hi, f.a + f.b / hi]] });
      var dH = -fe.b * R / 1000, dS = (fe.a - Math.log(Sim.C.kB / Sim.C.h)) * R;
      var Tm = S.mean(aMeas.map(function (p) { return p[0]; }));
      var exact = uEa < 1e-6 * Math.abs(EaF);
      if (exact) { uEa = 0; uA = 0; }
      fitRows = [
        ["E<sub>a</sub> from the fit", (exact ? EaF.toFixed(2) + " kJ/mol (no scatter: the points lie exactly on the model, so the fit uncertainty is zero)" : Sim.fmtU(EaF, uEa, "kJ/mol")) + " (model local value " + (Ea + n * R * Tm / 1000).toFixed(1) + " at " + Tm.toFixed(0) + " K)"],
        ["A from the fit", exact ? Sim.sig(A, 4) + " s⁻¹" : Sim.fmtU(A, uA, "s⁻¹") + " (relative uncertainty " + (100 * uA / A).toFixed(0) + " %)"],
        ["correlation of ln A and E<sub>a</sub>", exact ? "—" : corr.toFixed(3) + " (strongly correlated: the intercept is far from the data)"],
        ["Eyring: Δ<sup>‡</sup>H", dH.toFixed(1) + " kJ/mol (= E<sub>a</sub> − RT for a unimolecular step)"],
        ["Eyring: Δ<sup>‡</sup>S", dS.toFixed(0) + " J mol⁻¹ K⁻¹" + (dS > 10 ? " (loose transition state)" : dS < -10 ? " (tight transition state)" : "")],
        ["readings", aMeas.length + " between " + aMeas[0][0].toFixed(0) + " and " + aMeas[aMeas.length - 1][0].toFixed(0) + " K"]
      ];
    }
    aPlot.draw(series, {});
    var k1 = kArr(T1), k2 = kArr(T2), dbl = R * Math.LN2 / (1 / T1 - 1 / (T1 + 10)) / 1000;
    kvFill(Sim.$("#a-info"), [
      ["k(T₁ = " + T1.toFixed(1) + " K)", Sim.sig(k1, 3) + " s⁻¹"],
      ["k(T₂ = " + T2.toFixed(1) + " K)", Sim.sig(k2, 3) + " s⁻¹"],
      ["k(T₂)/k(T₁)", Sim.sig(k2 / k1, 3), ""],
      ["local E<sub>a</sub> = E + nRT at T₁", (Ea + n * R * T1 / 1000).toFixed(1) + " kJ/mol"],
      ["E<sub>a</sub> that doubles k from T₁ to T₁ + 10 K", dbl.toFixed(1) + " kJ/mol"],
      ["half-life at T₁ (first order)", Sim.sig(Math.LN2 / k1, 3) + " s"]
    ]);
    kvFill(Sim.$("#a-fit"), fitRows.length ? fitRows : [["status", "Measure some rate constants to fit them."]]);
    csvFns.arrhenius = function () { return aMeas ? { header: ["T_K", "k_per_s"], rows: aMeas.map(function (p) { return [+p[0].toFixed(2), +p[1].toPrecision(5)]; }), filename: "arrhenius_rate_constants.csv" } : null; };
  }
  function arrMeasure() {
    aCount++;
    var r = Sim.rng(seed + 29 * aCount), tlo = num("a-tlo") + 273.15, thi = num("a-thi") + 273.15, sd = num("a-noise") / 100;
    aMeas = [];
    for (var i = 0; i < 6; i++) { var T = tlo + (thi - tlo) * i / 5 + r.normal(0, 0.05); aMeas.push([T, kArr(T) * Math.exp(r.normal(0, sd))]); }
    arrDraw();
  }
  Sim.$("#a-ea").value = String(preset.ea || 50);
  Sim.$("#a-la").value = String(preset.la || 10);
  ["#a-ea", "#a-la", "#a-n"].forEach(function (q) { Sim.$(q).addEventListener("input", function () { aMeas = null; arrDraw(); }); });
  ["#a-t1", "#a-t2", "#a-tlo", "#a-thi", "#a-noise"].forEach(function (q) { Sim.$(q).addEventListener("change", arrDraw); });
  Sim.$("#a-measure").addEventListener("click", arrMeasure);
  Sim.$("#a-rerun").addEventListener("click", function () { seed = Sim.newSeed(seed); showSeed(); arrMeasure(); });
  Sim.$("#a-n2o5").addEventListener("click", function () {
    Sim.$("#a-ea").value = "92.5"; Sim.$("#a-la").value = String(Math.log10(1.05e15)); Sim.$("#a-n").value = "0";
    Sim.$("#a-tlo").value = "-73"; Sim.$("#a-thi").value = "27"; Sim.$("#a-t1").value = "25"; Sim.$("#a-t2").value = "35"; Sim.$("#a-noise").value = "0";
    arrMeasure();
  });
  Sim.$("#a-rule").addEventListener("click", function () {
    var T1 = num("a-t1") + 273.15;
    Sim.$("#a-ea").value = (R * Math.LN2 / (1 / T1 - 1 / (T1 + 10)) / 1000).toFixed(1); Sim.$("#a-n").value = "0"; Sim.$("#a-t2").value = String(num("a-t1") + 10);
    aMeas = null; arrDraw();
  });

  /* ======================= DYE FADING ======================= */
  var dPlot = Sim.plot(Sim.$("#d-plot"), { xLabel: "t / s", yLabel: "pseudo-absorbance" });
  var dL = Sim.plot(Sim.$("#d-lplot"), { xLabel: "t / s", yLabel: "ln(A − A∞)" });
  var dRuns = [], dLast = null;
  var K20 = 0.559, EA_DYE = 50000, NU = 8, BLEACH = 0.54;

  function fitExp(t, A, withInf) {
    // A = A0 exp(-k t) + Ainf; linear in A0 and Ainf for fixed k, so scan k
    function lin(k) {
      var g = t.map(function (x) { return Math.exp(-k * x); });
      if (!withInf) {
        var sgy = 0, sgg = 0; for (var i = 0; i < g.length; i++) { sgy += g[i] * A[i]; sgg += g[i] * g[i]; }
        var a0 = sgy / sgg, rss = 0; for (var j = 0; j < g.length; j++) rss += Math.pow(A[j] - a0 * g[j], 2);
        return { a0: a0, ainf: 0, rss: rss };
      }
      var f = S.linfit(g, A), rs = 0;
      for (var q = 0; q < g.length; q++) rs += Math.pow(A[q] - f.a - f.b * g[q], 2);
      return { a0: f.b, ainf: f.a, rss: rs };
    }
    var lk = golden(function (x) { return lin(Math.pow(10, x)).rss; }, -6, -0.5, 90), k = Math.pow(10, lk), best = lin(k);
    var h = k * 1e-3, d2 = (lin(k + h).rss - 2 * best.rss + lin(k - h).rss) / (h * h);
    var p = withInf ? 3 : 2, s2 = best.rss / Math.max(1, t.length - p);
    return { k: k, uk: d2 > 0 ? Math.sqrt(2 * s2 / d2) : NaN, a0: best.a0, ainf: best.ainf, s: Math.sqrt(s2) };
  }

  function dyeRun() {
    var r = Sim.rng(seed + 41 * (dRuns.length + 1));
    var Vb = Math.max(0.05, Math.min(10, num("d-bleach"))), T0 = num("d-temp"), Troom = num("d-room");
    var ocl = BLEACH * Vb / (200 + Vb), D0 = 1.0e-5 * (1 + r.normal(0, 0.02)), D = D0, tau = 2400;
    var A0 = 0.613 * D0 / 1.0e-5, Ainf = 0.012, lock = chk("d-lock");
    function Tc(t) { return Troom + (T0 - Troom) * Math.exp(-t / tau); }
    function kT(t) { return K20 * Math.exp(-EA_DYE / R * (1 / (Tc(t) + 273.15) - 1 / 293.15)); }
    var data = [], dt = 0.5, Tsum = 0, len = 60 * parseFloat(Sim.$("#d-len").value), step = len / 30;
    dt = Math.min(1, step / 20);
    for (var i = 0, t = 0; i <= 30; i++) {
      var tEnd = i * step;
      while (t < tEnd - 1e-9) {
        // RK2 on dye and hypochlorite
        var k1 = kT(t), r1 = k1 * D * ocl, Dm = D - r1 * dt / 2, Om = ocl - NU * r1 * dt / 2, r2 = kT(t + dt / 2) * Dm * Om;
        D -= r2 * dt; ocl -= NU * r2 * dt; t += dt;
      }
      var Atrue = A0 * D / D0 + Ainf, Aobs = Atrue;
      if (!lock) Aobs = Atrue * (1 - 0.3 * Atrue / 0.65) * (1 + r.normal(0, 0.03));   // auto-exposure compresses and wanders
      Aobs += r.normal(0, 0.004);
      data.push([tEnd, Aobs, Tc(tEnd)]);
      Tsum += Tc(tEnd);
    }
    var ts = data.map(function (p) { return p[0]; }), As = data.map(function (p) { return p[1]; });
    var fit = fitExp(ts, As, chk("d-ainf"));
    var shifted = As.map(function (a) { return a - fit.ainf; });
    var early = fitExp(ts.slice(0, 11), shifted.slice(0, 11), false), late = fitExp(ts.slice(10, 21).map(function (x) { return x - ts[10]; }), shifted.slice(10, 21), false);
    var Tmean = Tsum / data.length;
    dLast = { len: len, data: data, fit: fit, Vb: Vb, Tmean: Tmean, T0: T0, Tend: Tc(len), early: early.k, late: late.k, oclUse: 1 - ocl / (BLEACH * Vb / (200 + Vb)) };
    dRuns.push({ id: dRuns.length + 1, Vb: Vb, Tmean: Tmean, k: fit.k, uk: fit.uk });
    dyeDraw();
  }

  function dyeDraw() {
    if (!dLast) { dPlot.draw([], { xMin: 0, xMax: 900, yMin: 0, yMax: 0.7 }); dL.draw([], { xMin: 0, xMax: 900 }); kvFill(Sim.$("#d-derived"), []); kvFill(Sim.$("#d-info"), [["status", "Set up a run and take the photos."]]); return; }
    var L = dLast, f = L.fit, curve = [], tl = L.len;
    for (var t = 0; t <= tl + 1e-9; t += tl / 200) curve.push([t, f.a0 * Math.exp(-f.k * t) + f.ainf]);
    dPlot.draw([{ type: "points", color: "s1", label: "photos", data: L.data.map(function (p) { return [p[0], p[1]]; }) }, { type: "line", color: "s2", label: "fit", data: curve }, { type: "hline", y: f.ainf, color: "muted", dash: [3, 3] }], { xMin: 0, xMax: tl, yMin: 0 });
    var lnPts = L.data.filter(function (p) { return p[1] - f.ainf > 0.004; }).map(function (p) { return [p[0], Math.log(p[1] - f.ainf)]; });
    dL.draw([{ type: "points", color: "s1", data: lnPts }, { type: "line", color: "s2", data: [[0, Math.log(f.a0)], [tl, Math.log(f.a0) - f.k * tl]] }], { xMin: 0, xMax: tl, yLabel: chk("d-ainf") ? "ln(A − A∞)" : "ln A" });
    var drift = (L.late - L.early) / L.early * 100;
    var res = L.data.map(function (p) { return p[1] - f.a0 * Math.exp(-f.k * p[0]) - f.ainf; }), flips = 0, rms = 0;
    res.forEach(function (x, i) { rms += x * x; if (i && (x > 0) !== (res[i - 1] > 0)) flips++; });
    rms = Math.sqrt(rms / res.length);
    var pattern = flips < 9;
    kvFill(Sim.$("#d-info"), [
      ["k′", Sim.fmtU(f.k * 1000, f.uk * 1000, "× 10⁻³ s⁻¹") + " (fit uncertainty only)"],
      ["half-life", (Math.LN2 / f.k / 60).toFixed(2) + " min"],
      ["A₀, A∞ from the fit", f.a0.toFixed(3) + ", " + f.ainf.toFixed(3) + (f.ainf > 0.03 ? ": A∞ far above the usual 0.01–0.02, so the curve levels off for another reason (here the hypochlorite runs out)" : ""), f.ainf > 0.03 ? "miss" : null],
      ["k′ from the first and second third (A∞ fixed)", (L.early * 1000).toFixed(2) + " and " + (L.late * 1000).toFixed(2) + " × 10⁻³ s⁻¹ (" + (drift >= 0 ? "+" : "−") + Math.abs(drift).toFixed(0) + " %)", Math.abs(drift) > 10 ? "miss" : null],
      ["residuals", "rms " + rms.toFixed(4) + "; sign changes " + flips + " of " + (res.length - 1) + (pattern ? ": a pattern, the single exponential does not fit" : ": random"), pattern ? "miss" : null],
      ["hypochlorite used during the run", (100 * L.oclUse).toFixed(1) + " %" + (L.oclUse > 0.05 ? ": not in large excess, isolation fails" : ""), L.oclUse > 0.05 ? "miss" : null],
      ["temperature", L.T0.toFixed(1) + " °C at the start, " + L.Tend.toFixed(1) + " °C at the end, mean " + L.Tmean.toFixed(1) + " °C"]
    ]);
    var tb = Sim.$("#d-runs tbody");
    tb.textContent = "";
    dRuns.forEach(function (q) { tb.appendChild(Sim.el("tr", {}, Sim.el("td", { text: String(q.id) }), Sim.el("td", { text: q.Vb.toFixed(1) }), Sim.el("td", { text: q.Tmean.toFixed(1) }), Sim.el("td", { text: (q.k * 1000).toFixed(2) }), Sim.el("td", { text: (Math.LN2 / q.k / 60).toFixed(2) }))); });
    // order in hypochlorite and activation energy from pairs of runs
    var der = [], ord = null, ea = null;
    for (var i = dRuns.length - 1; i >= 0 && (!ord || !ea); i--) for (var j = i - 1; j >= 0; j--) {
      var a = dRuns[j], b = dRuns[i];
      if (!ord && Math.abs(a.Tmean - b.Tmean) < 1 && Math.abs(Math.log(b.Vb / a.Vb)) > 0.3) {
        var ra = (BLEACH * b.Vb / (200 + b.Vb)) / (BLEACH * a.Vb / (200 + a.Vb));
        ord = "n = " + (Math.log(b.k / a.k) / Math.log(ra)).toFixed(2) + " (runs " + a.id + " and " + b.id + ")";
      }
      if (!ea && Math.abs(a.Vb - b.Vb) < 0.05 && Math.abs(a.Tmean - b.Tmean) > 3) {
        ea = "E<sub>a</sub> = " + (R * Math.log(b.k / a.k) / (1 / (a.Tmean + 273.15) - 1 / (b.Tmean + 273.15)) / 1000).toFixed(0) + " kJ/mol from the mean temperatures (runs " + a.id + " and " + b.id + "; two points only)";
      }
    }
    der.push(["order in hypochlorite", ord || "needs two runs at the same temperature with different bleach"]);
    der.push(["activation energy", ea || "needs two runs with the same bleach at different temperatures"]);
    if (dRuns.length) { var k20 = dRuns[0].k / (BLEACH * dRuns[0].Vb / (200 + dRuns[0].Vb)); der.push(["second-order k (run 1)", k20.toFixed(2) + " L mol⁻¹ s⁻¹ (k′/[OCl⁻])"]); }
    kvFill(Sim.$("#d-derived"), der);
    csvFns.dye = function () { return { header: ["t_s", "A_pseudo", "T_C"], rows: L.data.map(function (p) { return [p[0], +p[1].toFixed(4), +p[2].toFixed(2)]; }), filename: "dye_fading_" + L.Vb + "mL.csv" }; };
  }
  Sim.$("#d-run").addEventListener("click", dyeRun);
  Sim.$("#d-rerun").addEventListener("click", function () { seed = Sim.newSeed(seed); showSeed(); dyeRun(); });
  Sim.$("#d-ainf").addEventListener("change", function () { if (dLast) { var ts = dLast.data.map(function (p) { return p[0]; }), As = dLast.data.map(function (p) { return p[1]; }); dLast.fit = fitExp(ts, As, chk("d-ainf")); dRuns[dRuns.length - 1].k = dLast.fit.k; dyeDraw(); } });

  /* ======================= ENZYME ======================= */
  var zPlot = Sim.plot(Sim.$("#z-plot"), { xLabel: "[S] / mM", yLabel: "v / (mM min⁻¹)" });
  var zLB = Sim.plot(Sim.$("#z-lb"), { xLabel: "1/[S] / mM⁻¹", yLabel: "1/v / (min mM⁻¹)" });
  var zData = null, zCount = 0;
  function inhib() {
    var t = Sim.$("#z-inh").value, i = num("z-i");
    if (t === "comp") return { a: 1 + i, b: 1 };
    if (t === "uncomp") return { a: 1, b: 1 + i };
    if (t === "noncomp") return { a: 1 + i, b: 1 + i };
    return { a: 1, b: 1 };
  }
  function nlFit(Sx, v) {
    function lin(K) { var sgv = 0, sgg = 0; Sx.forEach(function (s, i) { var g = s / (K + s); sgv += g * v[i]; sgg += g * g; }); var V = sgv / sgg, rss = 0; Sx.forEach(function (s, i) { rss += Math.pow(v[i] - V * s / (K + s), 2); }); return { V: V, rss: rss }; }
    var lK = golden(function (x) { return lin(Math.pow(10, x)).rss; }, -4, 5, 100), K = Math.pow(10, lK), b = lin(K);
    // standard errors from (J^T J)^-1 s^2
    var a11 = 0, a12 = 0, a22 = 0;
    Sx.forEach(function (s) { var g = s / (K + s), dk = -b.V * s / Math.pow(K + s, 2); a11 += g * g; a12 += g * dk; a22 += dk * dk; });
    var det = a11 * a22 - a12 * a12, s2 = b.rss / Math.max(1, Sx.length - 2);
    return { V: b.V, K: K, uV: Math.sqrt(s2 * a22 / det), uK: Math.sqrt(s2 * a11 / det) };
  }
  function enzDraw() {
    var Km = lg("z-km"), Vm = num("z-vm"), f = num("z-f"), I = inhib();
    var Kapp = I.a * Km / I.b, Vapp = Vm / I.b, inh = Sim.$("#z-inh").value !== "none";
    Sim.$("#z-km-out").textContent = Sim.sig(Km, 3);
    Sim.$("#z-vm-out").textContent = Vm.toFixed(2);
    Sim.$("#z-f-out").textContent = f.toFixed(2);
    Sim.$("#z-i-out").textContent = num("z-i").toFixed(1);
    var Sf = Km * f / (1 - f), xmax = Math.max(10 * Km, Sf * 1.1, zData ? zData.S[zData.S.length - 1] * 1.1 : 0);
    var c0 = [], c1 = [];
    for (var i = 0; i <= 300; i++) { var s = xmax * i / 300; c0.push([s, Vm * s / (Km + s)]); c1.push([s, Vapp * s / (Kapp + s)]); }
    var series = [{ type: "line", color: "s1", label: inh ? "no inhibitor" : "v", data: c0, dash: inh ? [5, 4] : null }];
    if (inh) series.push({ type: "line", color: "s2", label: "with inhibitor", data: c1 });
    series.push({ type: "hline", y: Vm, color: "muted", dash: [2, 4] });
    series.push({ type: "points", color: "s4", size: 5, label: "v = " + f.toFixed(2) + " Vmax", data: [[Sf, f * Vm]] });
    series.push({ type: "vline", x: Km, color: "s3", dash: [3, 3], label: "Km" });
    var fitRows = [];
    if (zData) {
      series.push({ type: "points", color: "s6", label: "measured", data: zData.S.map(function (s, k) { return [s, zData.v[k]]; }) });
      var nl = nlFit(zData.S, zData.v);
      var lbx = [], lby = [];
      zData.S.forEach(function (s, k) { if (zData.v[k] > 0) { lbx.push(1 / s); lby.push(1 / zData.v[k]); } });
      var lb = lbx.length >= 2 ? S.linfit(lbx, lby) : null;
      fitRows.push(["true (apparent) values", "K<sub>m</sub> = " + Sim.sig(Kapp, 3) + " mM, V<sub>max</sub> = " + Sim.sig(Vapp, 3)]);
      fitRows.push(["nonlinear least squares", "K<sub>m</sub> = " + Sim.fmtU(nl.K, nl.uK, "mM") + ", V<sub>max</sub> = " + Sim.fmtU(nl.V, nl.uV)]);
      if (lb) fitRows.push(["Lineweaver–Burk line", "K<sub>m</sub> = " + Sim.sig(lb.b / lb.a, 3) + " mM, V<sub>max</sub> = " + Sim.sig(1 / lb.a, 3) + (lb.a <= 0 ? " (negative intercept: meaningless)" : "")]);
      fitRows.push(["design", zData.design + " (" + zData.S.map(function (s) { return Sim.sig(s, 2); }).join(", ") + " mM)"]);
      var xm = Math.max.apply(null, lbx.concat([1 / Kapp])) * 1.1;
      zLB.draw([{ type: "points", color: "s6", label: "1/v", data: lbx.map(function (x, k) { return [x, lby[k]]; }) },
        lb ? { type: "line", color: "s2", label: "LB fit", data: [[0, lb.a], [xm, lb.a + lb.b * xm]] } : { type: "text", x: 0, y: 0, text: "" },
        { type: "line", color: "s1", dash: [5, 4], label: "true", data: [[0, 1 / Vapp], [xm, 1 / Vapp + Kapp / Vapp * xm]] }], { xMin: 0 });
    } else {
      var xm2 = 2 / Km, lines = [{ type: "line", color: "s1", label: "no inhibitor", data: [[-1 / Km, 0], [xm2, 1 / Vm + Km / Vm * xm2]] }];
      if (inh) lines.push({ type: "line", color: "s2", label: "with inhibitor", data: [[-1 / Kapp, 0], [xm2, 1 / Vapp + Kapp / Vapp * xm2]] });
      zLB.draw(lines.concat([{ type: "vline", x: 0, color: "muted" }]), {});
    }
    zPlot.draw(series, { xMin: 0, xMax: xmax, yMin: 0 });
    kvFill(Sim.$("#z-info"), [
      ["[S] for v = " + f.toFixed(2) + " V<sub>max</sub>", Sim.sig(Sf, 3) + " mM = " + Sim.sig(f / (1 - f), 3) + " K<sub>m</sub>"],
      ["V<sub>max</sub>/K<sub>m</sub> (first-order constant at low [S])", Sim.sig(Vm / Km, 3) + " min⁻¹"]
    ].concat(inh ? [["apparent K<sub>m</sub>, V<sub>max</sub>", Sim.sig(Kapp, 3) + " mM, " + Sim.sig(Vapp, 3) + " (α = " + I.a.toFixed(2) + ", α′ = " + I.b.toFixed(2) + ")"]] : []));
    kvFill(Sim.$("#z-fit"), fitRows.length ? fitRows : [["status", "Measure initial rates to fit them."]]);
    csvFns.enzyme = function () { return zData ? { header: ["S_mM", "v_mM_per_min"], rows: zData.S.map(function (s, k) { return [+s.toPrecision(4), +zData.v[k].toFixed(5)]; }), filename: "enzyme_initial_rates.csv" } : null; };
  }
  function enzMeasure() {
    zCount++;
    var r = Sim.rng(seed + 61 * zCount), Km = lg("z-km"), Vm = num("z-vm"), I = inhib(), sd = num("z-noise") / 100 * Vm;
    var d = Sim.$("#z-design").value;
    var rel = d === "good" ? [0.2, 0.4, 0.8, 1.6, 3.2, 6.4] : d === "poor" ? [2, 3.6, 5.2, 6.8, 8.4, 10] : [0.05, 0.1, 0.15, 0.2, 0.3, 0.4];
    var Sx = rel.map(function (q) { return q * Km; });
    zData = { S: Sx, v: Sx.map(function (s) { return Vm / I.b * s / (I.a * Km / I.b + s) + r.normal(0, sd); }), design: { good: "good", poor: "poor", low: "below Km only" }[d] };
    enzDraw();
  }
  setLog("z-km", preset.km || 16.7);
  Sim.$("#z-vm").value = String(preset.vm || 3.9);
  ["#z-km", "#z-vm", "#z-f", "#z-i"].forEach(function (q) { Sim.$(q).addEventListener("input", function () { if (q === "#z-km" || q === "#z-vm" || q === "#z-i") zData = null; enzDraw(); }); });
  ["#z-inh", "#z-design", "#z-noise"].forEach(function (q) { Sim.$(q).addEventListener("change", function () { zData = null; enzDraw(); }); });
  Sim.$("#z-measure").addEventListener("click", enzMeasure);
  Sim.$("#z-rerun").addEventListener("click", function () { seed = Sim.newSeed(seed); showSeed(); enzMeasure(); });

  /* ======================= tabs and export ======================= */
  Sim.exportCSV(Sim.$("#x-data"), "kinetics.csv", function () { var f = csvFns[tabName]; return f ? f() : null; });
  var DRAW = { orders: ordersDraw, consecutive: consecDraw, arrhenius: arrDraw, dye: dyeDraw, enzyme: enzDraw };
  var tabs = Sim.tabs(Sim.$("#tabs"), function (name) { tabName = name; DRAW[name](); });
  tabs.select(tabName);
})();
