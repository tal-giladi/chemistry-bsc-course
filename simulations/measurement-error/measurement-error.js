/* measurement-error simulation: repeat readings, confidence intervals, bias and
 * calibration with a CRM, and propagation of uncertainty (first order and
 * Monte Carlo). Uses ../common/sim.js (global Sim).
 *
 * Model of a reading: x = true * (1 + bProp) + bConst + N(0, sd), rounded to the
 * display resolution d. Values used:
 *  - Chloride CRM 25.0 +- 0.3 mg/L (k = 2) and analyst scatter 0.64 mg/L: Lesson 09.1
 *    worked example (simulated data; the CRM is illustrative, not a real certificate).
 *  - Sugar solution: 10 % sucrose, 1.0381 g/mL at 20 C, 1.0374 g/mL at 23 C (Plato
 *    table, as quoted in Lesson 01.5); scatter 0.0055 g/mL (s = 0.55 g on 100 mL).
 *  - One-shekel coin 3.5 g (Bank of Israel coin page, Lesson 09.1).
 *  - KHP M = 204.221 g/mol (PubChem CID 23676735); worked-example inputs from Lesson 09.3.
 */
(function () {
  "use strict";
  var S = Sim.stats;

  var PRESETS = {
    repeat: {
      title: "Repeat readings",
      tab: "repeat",
      what: "Random error makes repeat readings scatter. The standard deviation <i>s</i> describes the scatter of single readings and stays about the same however many you take. The uncertainty of the <i>mean</i>, u<sub>A</sub> = s/√n, shrinks as you take more. The second panel shows what a 95 % confidence interval means.",
      task: "Take 5, then 20, then 80 (or 50) readings and write down x̄, s and u<sub>A</sub> each time. Then take 20 sets of 5 readings, reveal the true value and count how many 95 % intervals contain it; repeat with sets of 3.",
      target: "s stays about the same while u<sub>A</sub> halves for every fourfold n (about 3× smaller from 5 to 50). Find the smallest n that brings u<sub>A</sub> below a quarter of s. About 19 of 20 intervals contain the true value (17–20 is normal)."
    },
    bias: {
      title: "A biased instrument",
      tab: "bias",
      what: "This instrument has a systematic error: it reads a few per cent off, the same way every time. Repeats cannot show it. Measuring a certified reference material (CRM) does.",
      task: "With the bias on, take 20 and then 100 readings of the sample and watch the mean settle on a wrong value. Then measure the CRM (at least 6 readings), estimate the bias with its uncertainty, and apply the calibration correction. Reveal the true values to check.",
      target: "Your bias estimate agrees with the true bias within its uncertainty (|difference| ≤ 2 u), more repeats do not shrink it, and the corrected sample result agrees with the true value."
    },
    propagation: {
      title: "Propagation of uncertainty",
      tab: "propagation",
      what: "A result calculated from several inputs inherits their uncertainties. For a product or quotient, the relative uncertainties add in quadrature. The budget shows each input's share of the variance; Monte Carlo checks the first-order formula.",
      task: "Halve each input's uncertainty in turn (then press Worked example to reset) and note the new combined uncertainty. Then try the poor design and compare first order with Monte Carlo.",
      target: "Find the one input whose halving lowers u(c) most (it carries about 97 % of the variance), and check that the value shown matches √Σ(u<sub>i</sub>/x<sub>i</sub>)² and the Monte Carlo spread to within 2 %."
    }
  };

  var preset = Sim.preset(PRESETS, "repeat");
  var seed = Sim.seedFromQuery(preset.key === "bias" ? 2024 : preset.key === "propagation" ? 31 : 7);

  /* ---------------- measurands for the repeat tab ---------------- */
  var MEASURANDS = {
    density: { name: "Density of a 10 % sugar solution (syringe + scale)", unit: "g/mL", centre: 1.0374, spread: 0.003, sd: 0.0055, d: 0.001,
      note: "Five fills of a calibrated 20 mL syringe weighed on a kitchen scale, at 23 °C. Display resolution 0.001 g/mL." },
    chloride: { name: "Chloride in tap water (titration)", unit: "mg/L", centre: 25, spread: 5, sd: 0.64, d: 0.01,
      note: "One analyst, one day (repeatability conditions). Display resolution 0.01 mg/L." },
    coin: { name: "Mass of a one-shekel coin (0.01 g pocket scale)", unit: "g", centre: 3.50, spread: 0.03, sd: 0.004, d: 0.01,
      note: "The scatter is smaller than the resolution, so many readings show the same digits: s underestimates the uncertainty unless you add d/√12." }
  };

  var state = {
    seed: seed,
    rng: null,
    m: "density",
    truth: {},
    readings: [],
    revealed: false,
    sets: [],
    noise: 1,
    bias: null,
    prop: null,
    trials: []
  };

  function decimals(d) { return Math.max(0, Math.round(-Math.log10(d))); }
  function roundTo(x, d) { return Math.round(x / d) * d; }

  function initTruth() {
    state.rng = Sim.rng(state.seed);
    var r = state.rng;
    state.truth = {};
    Object.keys(MEASURANDS).forEach(function (k) {
      var M = MEASURANDS[k];
      state.truth[k] = M.centre + r.uniform(-M.spread, M.spread);
    });
    // bias tab: hidden sample value, CRM true value (certificate is itself uncertain) and the bias
    state.bias = {
      sampleTrue: r.uniform(18, 32),
      crmTrue: 25.0 + r.normal(0, 0.15),
      bProp: r.pick([-1, 1]) * r.uniform(0.03, 0.06),
      bConst: r.uniform(-0.15, 0.15),
      sd: 0.30,
      d: 0.01,
      readings: { sample: [], crm: [] },
      revealed: false
    };
    Sim.$("#r-seed").textContent = String(state.seed);
    Sim.$("#b-seed").textContent = String(state.seed);
  }

  /* ---------------- tabs and preset ---------------- */
  Sim.label();
  Sim.presetBox(Sim.$("#preset"), preset);
  var tabs = Sim.tabs(Sim.$("#tabs"), function () { redrawAll(); });

  /* ---------------- repeat tab ---------------- */
  var selM = Sim.$("#r-measurand");
  Object.keys(MEASURANDS).forEach(function (k) { selM.appendChild(Sim.el("option", { value: k, text: MEASURANDS[k].name })); });

  var rPlot = Sim.plot(Sim.$("#r-plot"), { xLabel: "reading number n", yLabel: "reading" });
  var rHist = Sim.plot(Sim.$("#r-hist"), { xLabel: "reading", yLabel: "count", legend: false });
  var ciPlot = Sim.plot(Sim.$("#ci-plot"), { xLabel: "value", yLabel: "set number" });

  function readOne(kind) {
    var M = MEASURANDS[kind];
    var x = state.truth[kind] + state.rng.normal(0, M.sd * state.noise);
    return roundTo(x, M.d);
  }

  function take(n) {
    var M = MEASURANDS[state.m], last = null;
    for (var i = 0; i < n; i++) { last = readOne(state.m); state.readings.push(last); }
    Sim.$("#r-display").textContent = last.toFixed(decimals(M.d)) + " " + M.unit;
    renderRepeat();
  }

  function statRows(a, M) {
    var n = a.length, mean = S.mean(a), s = S.sd(a), uA = s / Math.sqrt(n);
    var ures = M.d / Math.sqrt(12);
    var t = n > 1 ? S.tInv(0.95, n - 1) : NaN;
    var dec = decimals(M.d) + 2;
    var rows = [
      ["n", String(n)],
      ["mean x̄", isFinite(mean) ? mean.toFixed(dec) + " " + M.unit : "—"],
      ["s", isFinite(s) ? s.toFixed(dec) + " " + M.unit : "— (need 2 readings)"],
      ["u_A = s/√n", isFinite(uA) ? uA.toFixed(dec) + " " + M.unit : "—"],
      ["u_A / s", isFinite(uA) && s > 0 ? (1 / Math.sqrt(n)).toFixed(3) : "—"],
      ["u_res = d/√12", ures.toFixed(dec) + " " + M.unit],
      ["u = √(u_A² + u_res²)", isFinite(uA) ? Math.sqrt(uA * uA + ures * ures).toFixed(dec) + " " + M.unit : "—"],
      ["t (95 %, " + (n > 1 ? n - 1 : "—") + " df)", isFinite(t) ? t.toFixed(3) : "—"],
      ["95 % interval", isFinite(t) && isFinite(uA) ? mean.toFixed(dec) + " ± " + (t * uA).toFixed(dec) + " " + M.unit : "—"]
    ];
    return { rows: rows, mean: mean, s: s, uA: uA, t: t, n: n };
  }

  function fillKV(el, rows) {
    el.textContent = "";
    rows.forEach(function (r) {
      el.appendChild(Sim.el("span", { text: r[0] }));
      el.appendChild(Sim.el("span", { html: r[1] }));
    });
  }

  function renderRepeat() {
    var M = MEASURANDS[state.m];
    var st = statRows(state.readings, M);
    var rows = st.rows.slice();
    if (state.revealed) {
      var tv = state.truth[state.m];
      rows.push(["true value", "<b>" + tv.toFixed(decimals(M.d) + 2) + " " + M.unit + "</b>"]);
      if (isFinite(st.mean)) rows.push(["error of the mean", (st.mean - tv).toFixed(decimals(M.d) + 2) + " " + M.unit + (isFinite(st.uA) && st.uA > 0 ? "  (" + ((st.mean - tv) / Math.sqrt(st.uA * st.uA + M.d * M.d / 12)).toFixed(2) + " u)" : "")]);
    } else rows.push(["true value", "hidden"]);
    fillKV(Sim.$("#r-stats"), rows);
    Sim.$("#r-instr-note").textContent = M.note;
    Sim.$("#r-plot").setAttribute("aria-label", "Readings plot: " + st.n + " readings, mean " + (isFinite(st.mean) ? st.mean.toFixed(4) : "none"));

    var pts = [], run = [], band = [], sum = 0, sum2 = 0;
    state.readings.forEach(function (x, i) {
      var n = i + 1;
      sum += x; sum2 += x * x;
      pts.push([n, x]);
      var m = sum / n;
      run.push([n, m]);
      if (n > 1) {
        var v = Math.max(0, (sum2 - n * m * m) / (n - 1));
        var u = Math.sqrt(v / n);
        band.push([n, m - u, m + u]);
      }
    });
    var series = [
      { type: "band", data: band, color: "s1", label: "x̄ ± u_A" },
      { type: "points", data: pts, color: "s2", size: 2.4, label: "readings" },
      { type: "line", data: run, color: "s1", label: "running mean" }
    ];
    if (state.revealed) series.push({ type: "hline", y: state.truth[state.m], color: "s3", dash: [6, 4], label: "true value" });
    rPlot.draw(series, { yLabel: "reading / " + M.unit });

    if (state.readings.length) {
      var lo = S.min(state.readings), hi = S.max(state.readings);
      var bins = Math.max(5, Math.min(30, Math.round(Math.sqrt(state.readings.length) * 2)));
      var step = Math.max(M.d, (hi - lo) / bins);
      var nb = Math.max(1, Math.round((hi - lo) / step) + 1);
      var h = S.histogram(state.readings, lo - step / 2, lo - step / 2 + nb * step, nb);
      var bars = h.counts.map(function (c, i) { return [h.edges[i] + h.width / 2, c]; });
      var hs = [{ type: "bars", data: bars, color: "s2", barWidth: h.width }];
      if (state.revealed) hs.push({ type: "vline", x: state.truth[state.m], color: "s3", dash: [6, 4] });
      rHist.draw(hs, { xLabel: "reading / " + M.unit, yMin: 0 });
    } else rHist.draw([], { xLabel: "reading / " + M.unit });
    renderSets();
  }

  /* --- confidence-interval sets --- */
  function takeSet() {
    var n = Math.max(2, Math.min(100, parseInt(Sim.$("#ci-n").value, 10) || 5));
    var a = [];
    for (var i = 0; i < n; i++) a.push(readOne(state.m));
    var mean = S.mean(a), s = S.sd(a), t = S.tInv(0.95, n - 1);
    state.sets.push({ m: state.m, n: n, mean: mean, s: s, t: t, hw: t * s / Math.sqrt(n), readings: a });
  }

  function renderSets() {
    var sets = state.sets.filter(function (z) { return z.m === state.m; });
    var M = MEASURANDS[state.m], dec = decimals(M.d) + 2, tv = state.truth[state.m];
    var tb = Sim.$("#ci-table tbody");
    tb.textContent = "";
    var hits = 0;
    var series = [];
    sets.forEach(function (z, i) {
      var inside = Math.abs(z.mean - tv) <= z.hw;
      if (inside) hits++;
      var mark = state.revealed ? (inside ? "yes" : "NO") : "hidden";
      tb.appendChild(Sim.el("tr", {},
        Sim.el("td", { text: String(i + 1) }), Sim.el("td", { text: String(z.n) }),
        Sim.el("td", { text: z.mean.toFixed(dec) }), Sim.el("td", { text: z.s.toFixed(dec) }),
        Sim.el("td", { text: z.t.toFixed(3) }), Sim.el("td", { text: z.hw.toFixed(dec) }),
        Sim.el("td", { class: state.revealed ? (inside ? "hit" : "miss") : "", text: mark })));
      series.push({ type: "hbar", y: i + 1, x1: z.mean - z.hw, x2: z.mean + z.hw, mid: z.mean, color: state.revealed && !inside ? "bad" : "s1", width: 2 });
    });
    if (state.revealed) series.push({ type: "vline", x: tv, color: "s3", dash: [6, 4], label: "true value" });
    ciPlot.draw(series, { xLabel: "value / " + M.unit, yMin: 0, yMax: Math.max(5, sets.length + 1) });
    var sum = Sim.$("#ci-summary");
    if (!sets.length) sum.textContent = "No sets yet.";
    else if (!state.revealed) sum.textContent = sets.length + " sets taken. Reveal the true value to count how many intervals contain it.";
    else sum.innerHTML = "<b>" + hits + " of " + sets.length + "</b> intervals contain the true value (" + (100 * hits / sets.length).toFixed(0) + " %; expected about 95 %).";
  }

  selM.addEventListener("change", function () {
    state.m = selM.value;
    state.readings = [];
    Sim.$("#r-display").textContent = "—";
    renderRepeat();
  });
  Sim.$("#r-noise").addEventListener("input", function (e) {
    state.noise = parseFloat(e.target.value);
    Sim.$("#r-noise-out").textContent = state.noise.toFixed(2) + "×";
  });
  Sim.$("#r-take1").addEventListener("click", function () { take(1); });
  Sim.$("#r-take5").addEventListener("click", function () { take(5); });
  Sim.$("#r-take20").addEventListener("click", function () { take(20); });
  Sim.$("#r-taken").addEventListener("click", function () { take(Math.max(1, Math.min(2000, parseInt(Sim.$("#r-n").value, 10) || 1))); });
  Sim.$("#r-clear").addEventListener("click", function () { state.readings = []; Sim.$("#r-display").textContent = "—"; renderRepeat(); });
  Sim.$("#r-reveal").addEventListener("click", function () { state.revealed = !state.revealed; Sim.$("#r-reveal").textContent = state.revealed ? "Hide true value" : "Reveal true value"; renderRepeat(); });
  Sim.$("#ci-one").addEventListener("click", function () { takeSet(); renderSets(); });
  Sim.$("#ci-twenty").addEventListener("click", function () { for (var i = 0; i < 20; i++) takeSet(); renderSets(); });
  Sim.$("#ci-clear").addEventListener("click", function () { state.sets = state.sets.filter(function (z) { return z.m !== state.m; }); renderSets(); });

  function rerun() {
    state.seed = Sim.newSeed(state.seed);
    state.readings = [];
    state.sets = [];
    state.revealed = false;
    Sim.$("#r-reveal").textContent = "Reveal true value";
    Sim.$("#b-reveal").textContent = "Reveal true values";
    initTruth();
    Sim.$("#r-display").textContent = "—";
    Sim.$("#b-display").textContent = "—";
    renderRepeat();
    renderBias();
  }
  Sim.$("#r-rerun").addEventListener("click", rerun);

  /* ---------------- bias tab ---------------- */
  var CRM = { value: 25.0, U: 0.3, k: 2 };
  var bPlot = Sim.plot(Sim.$("#b-plot"), { xLabel: "number of sample readings n", yLabel: "chloride / mg/L" });

  function biasWhat() { var r = Sim.$("input[name=b-what]:checked"); return r ? r.value : "sample"; }

  function biasRead(which) {
    var B = state.bias, on = Sim.$("#b-biason").checked;
    var tv = which === "crm" ? B.crmTrue : B.sampleTrue;
    var x = on ? tv * (1 + B.bProp) + B.bConst : tv;
    return roundTo(x + state.rng.normal(0, B.sd), B.d);
  }

  function biasTake(n) {
    var which = biasWhat(), on = Sim.$("#b-biason").checked, last = null;
    for (var i = 0; i < n; i++) {
      last = biasRead(which);
      state.bias.readings[which].push({ x: last, biasOn: on });
    }
    Sim.$("#b-display").textContent = last.toFixed(2) + " mg/L";
    renderBias();
  }

  function biasSummary() {
    var B = state.bias, on = Sim.$("#b-biason").checked;
    // statistics use only readings taken with the current bias setting
    var s = B.readings.sample.filter(function (r) { return r.biasOn === on; }).map(function (r) { return r.x; });
    var c = B.readings.crm.filter(function (r) { return r.biasOn === on; }).map(function (r) { return r.x; });
    var out = { s: s, c: c, on: on };
    out.sMean = S.mean(s); out.sSd = S.sd(s); out.sU = out.sSd / Math.sqrt(s.length);
    out.cMean = S.mean(c); out.cSd = S.sd(c);
    var uCert = CRM.U / CRM.k;
    out.bias = out.cMean - CRM.value;
    out.uBias = Math.sqrt((isFinite(out.cSd) ? out.cSd * out.cSd / c.length : NaN) + uCert * uCert);
    out.z = Math.abs(out.bias) / out.uBias;
    out.R = out.cMean / CRM.value;
    out.uR = out.R * out.uBias / out.cMean;
    out.corr = out.sMean / out.R;
    out.uCorr = Math.abs(out.corr) * Math.sqrt(Math.pow(out.sU / out.sMean, 2) + Math.pow(out.uR / out.R, 2));
    out.trueBias = on ? B.crmTrue * B.bProp + B.bConst + (B.crmTrue - CRM.value) : B.crmTrue - CRM.value;
    return out;
  }

  function renderBias() {
    var B = state.bias, q = biasSummary();
    var f2 = function (x) { return isFinite(x) ? x.toFixed(3) : "—"; };
    var rows = [
      ["CRM readings n", String(q.c.length)],
      ["CRM mean", isFinite(q.cMean) ? f2(q.cMean) + " mg/L" : "—"],
      ["CRM s", isFinite(q.cSd) ? f2(q.cSd) + " mg/L" : "— (need 2 readings)"],
      ["bias = x̄ − 25.0", isFinite(q.bias) ? f2(q.bias) + " mg/L (" + (100 * q.bias / CRM.value).toFixed(2) + " %)" : "—"],
      ["u(bias)", isFinite(q.uBias) ? f2(q.uBias) + " mg/L" : "—"],
      ["z = |bias| / u", isFinite(q.z) ? q.z.toFixed(2) + (q.z > 2 ? "  → the bias is real" : "  → no evidence of bias") : "—"],
      ["recovery R", isFinite(q.R) ? (100 * q.R).toFixed(2) + " %" : "—"]
    ];
    if (B.revealed) {
      rows.push(["true bias of these readings", "<b>" + f2(q.trueBias) + " mg/L</b>"]);
      if (isFinite(q.bias)) {
        var dd = q.bias - q.trueBias;
        rows.push(["your estimate − true", f2(dd) + " mg/L = " + (dd / q.uBias).toFixed(2) + " u" + (Math.abs(dd) <= 2 * q.uBias ? "  (agrees)" : "  (disagrees)")]);
      }
      rows.push(["CRM true content", f2(B.crmTrue) + " mg/L (the certificate says 25.0 ± 0.3)"]);
    }
    fillKV(Sim.$("#b-stats"), rows);

    var res = [
      ["sample readings n", String(q.s.length)],
      ["sample mean x̄", isFinite(q.sMean) ? f2(q.sMean) + " mg/L" : "—"],
      ["s, u_A = s/√n", isFinite(q.sSd) ? f2(q.sSd) + ", " + f2(q.sU) + " mg/L" : "—"]
    ];
    var corrOn = Sim.$("#b-correct").checked;
    if (corrOn) {
      res.push(["corrected x̄ / R", isFinite(q.corr) && isFinite(q.uCorr) ? Sim.fmtU(q.corr, q.uCorr, "mg/L") : "needs ≥ 2 CRM and ≥ 2 sample readings"]);
    }
    if (B.revealed) {
      res.push(["true sample value", "<b>" + f2(B.sampleTrue) + " mg/L</b>"]);
      if (isFinite(q.sMean)) res.push(["error of x̄", f2(q.sMean - B.sampleTrue) + " mg/L"]);
      if (corrOn && isFinite(q.corr)) res.push(["error after correction", f2(q.corr - B.sampleTrue) + " mg/L" + (isFinite(q.uCorr) ? " = " + ((q.corr - B.sampleTrue) / q.uCorr).toFixed(2) + " u" : "")]);
      if (q.on) res.push(["hidden bias model", "proportional " + (100 * B.bProp).toFixed(2) + " %, constant " + B.bConst.toFixed(3) + " mg/L"]);
    } else res.push(["true values", "hidden"]);
    if (!q.on) res.push(["note", "bias switched off: the instrument reads true on average"]);
    fillKV(Sim.$("#b-result"), res);

    var run = [], band = [], sum = 0, sum2 = 0, corrRun = [];
    q.s.forEach(function (x, i) {
      var n = i + 1; sum += x; sum2 += x * x;
      var m = sum / n;
      run.push([n, m]);
      if (n > 1) { var u = Math.sqrt(Math.max(0, (sum2 - n * m * m) / (n - 1)) / n); band.push([n, m - u, m + u]); }
      if (corrOn && isFinite(q.R)) corrRun.push([n, m / q.R]);
    });
    var series = [
      { type: "band", data: band, color: "s1", label: "x̄ ± u_A" },
      { type: "line", data: run, color: "s1", label: "running mean (as read)" }
    ];
    if (corrRun.length) series.push({ type: "line", data: corrRun, color: "s4", label: "corrected (÷ R)" });
    if (B.revealed) series.push({ type: "hline", y: B.sampleTrue, color: "s3", dash: [6, 4], label: "true value" });
    bPlot.draw(series);
  }

  Sim.$("#b-take1").addEventListener("click", function () { biasTake(1); });
  Sim.$("#b-take5").addEventListener("click", function () { biasTake(5); });
  Sim.$("#b-take20").addEventListener("click", function () { biasTake(20); });
  Sim.$("#b-take100").addEventListener("click", function () { biasTake(100); });
  Sim.$("#b-biason").addEventListener("change", renderBias);
  Sim.$("#b-correct").addEventListener("change", renderBias);
  Sim.$$("input[name=b-what]").forEach(function (r) { r.addEventListener("change", renderBias); });
  Sim.$("#b-clear").addEventListener("click", function () { state.bias.readings = { sample: [], crm: [] }; Sim.$("#b-display").textContent = "—"; renderBias(); });
  Sim.$("#b-reveal").addEventListener("click", function () {
    state.bias.revealed = !state.bias.revealed;
    Sim.$("#b-reveal").textContent = state.bias.revealed ? "Hide true values" : "Reveal true values";
    renderBias();
  });
  Sim.$("#b-rerun").addEventListener("click", rerun);

  /* ---------------- propagation tab ---------------- */
  var INPUTS0 = [
    { key: "m", name: "Mass of KHP, m (0.1 mg balance, by difference)", unit: "g", value: 0.5106, u: 0.1e-3 / Math.sqrt(6), dist: "rect", p: 1 },
    { key: "P", name: "Purity, P (certificate 99.95 ± 0.05 %)", unit: "", value: 0.9995, u: 0.0005 / Math.sqrt(3), dist: "rect", p: 1 },
    { key: "M", name: "Molar mass of KHP, M", unit: "g/mol", value: 204.221, u: 0, dist: "normal", p: -1 },
    { key: "V", name: "Titrant volume at the end point, V (50 mL Class A burette)", unit: "mL", value: 24.87, u: 0.044, dist: "normal", p: -1 }
  ];
  var SMALL = { m: [0.0511, 0.1e-3 / Math.sqrt(6)], V: [2.00, 0.30] };
  var sharePlot = Sim.plot(Sim.$("#p-share"), { xLabel: "input", yLabel: "share of variance / %", legend: false, xMin: 0.4, xMax: 4.6, yMin: 0, yMax: 100, xPad: false });
  var histPlot = Sim.plot(Sim.$("#p-hist"), { xLabel: "c / mol L⁻¹", yLabel: "probability density" });

  function cloneInputs(src) { return src.map(function (x) { var o = {}; Object.keys(x).forEach(function (k) { o[k] = x[k]; }); return o; }); }
  state.prop = { inputs: cloneInputs(INPUTS0), mc: null };

  function model(m, P, M, VmL) { return m * P / (M * VmL / 1000); }

  function firstOrder() {
    var I = state.prop.inputs;
    var v = {};
    I.forEach(function (x) { v[x.key] = x.value; });
    var c = model(v.m, v.P, v.M, v.V);
    var contribs = I.map(function (x) {
      // c is a product of powers (exponent p = +1 or -1), so dc/dx * u = p * c * u/x
      var rel = x.value !== 0 ? x.u / Math.abs(x.value) : NaN;
      return { key: x.key, name: x.name, rel: rel, contrib: Math.abs(x.p) * Math.abs(c) * rel };
    });
    var uc2 = 0;
    contribs.forEach(function (k) { uc2 += k.contrib * k.contrib; });
    var uc = Math.sqrt(uc2);
    contribs.forEach(function (k) { k.share = uc2 > 0 ? k.contrib * k.contrib / uc2 : 0; });
    var relSum = Math.sqrt(contribs.reduce(function (a, k) { return a + k.rel * k.rel; }, 0));
    return { c: c, uc: uc, rel: uc / c, relCheck: relSum, contribs: contribs };
  }

  function renderInputs() {
    var tb = Sim.$("#p-inputs tbody");
    tb.textContent = "";
    state.prop.inputs.forEach(function (x, i) {
      var val = Sim.el("input", { type: "number", step: "any", value: String(x.value), "aria-label": x.name + " value" });
      var unc = Sim.el("input", { type: "number", step: "any", min: "0", value: String(+x.u.toPrecision(4)), "aria-label": x.name + " standard uncertainty" });
      var dist = Sim.el("select", { "aria-label": x.name + " distribution" },
        Sim.el("option", { value: "normal", text: "normal" }), Sim.el("option", { value: "rect", text: "rectangular" }));
      dist.value = x.dist;
      var half = Sim.el("button", { type: "button", text: "Halve u" });
      val.addEventListener("change", function () { var v = parseFloat(val.value); if (isFinite(v) && v > 0) { x.value = v; logTrial(x.key + " = " + v); } else val.value = String(x.value); });
      unc.addEventListener("change", function () { var v = parseFloat(unc.value); if (isFinite(v) && v >= 0) { x.u = v; logTrial("u(" + x.key + ") = " + v); } else unc.value = String(x.u); });
      dist.addEventListener("change", function () { x.dist = dist.value; state.prop.mc = null; renderProp(); });
      half.addEventListener("click", function () { x.u = x.u / 2; unc.value = String(+x.u.toPrecision(4)); logTrial("halve u(" + x.key + ")"); });
      tb.appendChild(Sim.el("tr", {}, Sim.el("td", { text: x.name }), Sim.el("td", {}, val), Sim.el("td", { text: x.unit || "—" }), Sim.el("td", {}, unc), Sim.el("td", {}, dist), Sim.el("td", {}, half)));
    });
  }

  function logTrial(change) {
    var f = firstOrder();
    state.trials.push({ change: change, c: f.c, rel: f.rel, check: f.relCheck });
    state.prop.mc = null;
    renderProp();
  }

  function pct(x, d) { return isFinite(x) ? (100 * x).toFixed(d === undefined ? 3 : d) + " %" : "—"; }

  function renderProp() {
    var f = firstOrder();
    fillKV(Sim.$("#p-first"), [
      ["c", f.c.toFixed(5) + " mol/L"],
      ["u(c)", f.uc.toPrecision(2) + " mol/L"],
      ["u(c)/c", pct(f.rel)],
      ["result", Sim.fmtU(f.c, f.uc, "mol/L")],
      ["first-order 95 % interval (±2u)", (f.c - 2 * f.uc).toFixed(5) + " to " + (f.c + 2 * f.uc).toFixed(5)],
      ["check √Σ(u_i/x_i)²", pct(f.relCheck)]
    ]);
    var tb = Sim.$("#p-budget tbody");
    tb.textContent = "";
    var maxShare = -1, maxKey = "";
    f.contribs.forEach(function (k) {
      if (k.share > maxShare) { maxShare = k.share; maxKey = k.key; }
      tb.appendChild(Sim.el("tr", {}, Sim.el("td", { text: k.name.split(",")[0] }), Sim.el("td", { text: pct(k.rel) }),
        Sim.el("td", { text: k.contrib.toPrecision(2) + " mol/L" }), Sim.el("td", { text: pct(k.share, 1) })));
    });
    var bars = f.contribs.map(function (k, i) { return [i + 1, 100 * k.share]; });
    var labels = f.contribs.map(function (k, i) { return { type: "text", x: i + 1, y: Math.min(92, 100 * k.share + 6), text: k.key + (k.key === maxKey ? " (largest)" : ""), align: "center", noRange: true }; });
    sharePlot.draw([{ type: "bars", data: bars, color: "s1", barWidth: 0.6 }].concat(labels));

    var mcEl = Sim.$("#p-mcout");
    var mc = state.prop.mc;
    if (!mc) {
      fillKV(mcEl, [["status", "press Run Monte Carlo"]]);
      histPlot.draw([]);
    } else {
      var agree = mc.sd / f.uc - 1;
      fillKV(mcEl, [
        ["draws", String(mc.N)],
        ["mean", mc.mean.toFixed(5) + " mol/L"],
        ["median", mc.median.toFixed(5) + " mol/L"],
        ["standard deviation u(c)", mc.sd.toPrecision(2) + " mol/L (" + pct(mc.sd / mc.mean) + ")"],
        ["95 % coverage interval", "[" + mc.lo.toFixed(5) + ", " + mc.hi.toFixed(5) + "]"],
        ["asymmetry (hi − median) / (median − lo)", ((mc.hi - mc.median) / (mc.median - mc.lo)).toFixed(3)],
        ["MC u vs first-order u", (agree >= 0 ? "+" : "") + (100 * agree).toFixed(2) + " %" + (Math.abs(agree) <= 0.02 ? "  (agree within 2 %)" : "  (first order is not good enough)")]
      ]);
      var pdf = [];
      for (var i = 0; i <= 200; i++) {
        var x = mc.hLo + (mc.hHi - mc.hLo) * i / 200;
        pdf.push([x, Math.exp(-0.5 * Math.pow((x - f.c) / f.uc, 2)) / (f.uc * Math.sqrt(2 * Math.PI))]);
      }
      histPlot.draw([
        { type: "bars", data: mc.bars, color: "s1", barWidth: mc.bw, label: "Monte Carlo" },
        { type: "line", data: pdf, color: "s2", label: "first order (normal)" },
        { type: "vline", x: mc.lo, color: "s3", dash: [4, 4], label: "95 % interval (MC)" },
        { type: "vline", x: mc.hi, color: "s3", dash: [4, 4] }
      ], { yMin: 0 });
    }

    var tt = Sim.$("#p-trials tbody");
    tt.textContent = "";
    state.trials.forEach(function (t, i) {
      tt.appendChild(Sim.el("tr", {}, Sim.el("td", { text: String(i + 1) }), Sim.el("td", { text: t.change }),
        Sim.el("td", { text: t.c.toFixed(5) }), Sim.el("td", { text: pct(t.rel) }), Sim.el("td", { text: pct(t.check) })));
    });
  }

  function runMC() {
    var N = parseInt(Sim.$("#p-N").value, 10) || 100000;
    var r = Sim.rng(state.seed + 99);
    var I = state.prop.inputs;
    var out = new Float64Array(N);
    var draw = I.map(function (x) {
      if (x.u <= 0) return function () { return x.value; };
      if (x.dist === "rect") { var a = x.u * Math.sqrt(3); return function () { return x.value + a * (2 * r.random() - 1); }; }
      return function () { return r.normal(x.value, x.u); };
    });
    var sum = 0;
    for (var i = 0; i < N; i++) {
      var v = model(draw[0](), draw[1](), draw[2](), draw[3]());
      out[i] = v; sum += v;
    }
    var mean = sum / N, ss = 0;
    for (var j = 0; j < N; j++) ss += (out[j] - mean) * (out[j] - mean);
    out.sort();
    var pc = function (p) { return S.percentile(out, p); };
    var hLo = pc(0.001), hHi = pc(0.999), bins = 70, bw = (hHi - hLo) / bins, counts = [];
    for (var b = 0; b < bins; b++) counts.push(0);
    for (var k = 0; k < N; k++) { var q = Math.floor((out[k] - hLo) / bw); if (q >= 0 && q < bins) counts[q]++; }
    var bars = counts.map(function (c, i2) { return [hLo + (i2 + 0.5) * bw, c / (N * bw)]; });
    state.prop.mc = { N: N, mean: mean, sd: Math.sqrt(ss / (N - 1)), median: pc(0.5), lo: pc(0.025), hi: pc(0.975), bars: bars, bw: bw, hLo: hLo, hHi: hHi };
    renderProp();
  }

  Sim.$("#p-mc").addEventListener("click", runMC);
  Sim.$("#p-reset").addEventListener("click", function () { state.prop.inputs = cloneInputs(INPUTS0); renderInputs(); logTrial("worked example"); });
  Sim.$("#p-small").addEventListener("click", function () {
    state.prop.inputs = cloneInputs(INPUTS0);
    state.prop.inputs.forEach(function (x) { if (SMALL[x.key]) { x.value = SMALL[x.key][0]; x.u = SMALL[x.key][1]; } });
    renderInputs();
    logTrial("poor design");
  });

  /* ---------------- export ---------------- */
  Sim.exportCSV(Sim.$("#export-readings"), "measurement_readings.csv", function () {
    var rows = [];
    state.readings.forEach(function (x, i) { rows.push(["repeat", state.m, "sample", i + 1, x, MEASURANDS[state.m].unit, ""]); });
    ["sample", "crm"].forEach(function (w) {
      state.bias.readings[w].forEach(function (r, i) { rows.push(["bias", "chloride", w, i + 1, r.x, "mg/L", r.biasOn ? "on" : "off"]); });
    });
    return { header: ["tab", "measurand", "what", "index", "reading", "unit", "bias"], rows: rows };
  });
  Sim.exportCSV(Sim.$("#export-sets"), "measurement_sets.csv", function () {
    var rows = [];
    state.sets.forEach(function (z, i) {
      var tv = state.truth[z.m];
      z.readings.forEach(function (x, j) {
        rows.push([i + 1, z.m, z.n, j + 1, x, z.mean, z.s, z.t, z.hw, state.revealed ? tv : "", state.revealed ? (Math.abs(z.mean - tv) <= z.hw ? 1 : 0) : ""]);
      });
    });
    return { header: ["set", "measurand", "n", "reading_no", "reading", "set_mean", "set_s", "t95", "half_width", "true_value", "contains_true"], rows: rows };
  });
  Sim.exportCSV(Sim.$("#export-budget"), "propagation_budget.csv", function () {
    var f = firstOrder(), rows = [];
    state.prop.inputs.forEach(function (x, i) {
      var k = f.contribs[i];
      rows.push(["input", x.key, x.value, x.unit, x.u, x.dist, k.rel, k.contrib, k.share]);
    });
    rows.push(["result", "c", f.c, "mol/L", f.uc, "", f.rel, "", 1]);
    state.trials.forEach(function (t, i) { rows.push(["trial " + (i + 1), t.change, t.c, "mol/L", t.c * t.rel, "", t.rel, "", ""]); });
    return { header: ["row", "name", "value", "unit", "standard_u", "distribution", "relative_u", "contribution", "share_of_variance"], rows: rows };
  });

  /* ---------------- start ---------------- */
  function redrawAll() { renderRepeat(); renderBias(); renderProp(); }

  initTruth();
  if (preset.key === "bias") { state.m = "chloride"; }
  selM.value = state.m;
  renderInputs();
  state.trials.push((function () { var f = firstOrder(); return { change: "worked example", c: f.c, rel: f.rel, check: f.relCheck }; })());
  tabs.select(preset.tab || "repeat");
})();
