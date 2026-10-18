/* chromatography simulation: temperature-programmed capillary GC with retention indices, overload
 * and an MS detector; reversed-phase HPLC method building (linear solvent strength, pH, solvent,
 * gradient, system suitability); van Deemter plate-height measurements and fit.
 * Uses ../common/sim.js (global Sim).
 *
 * Data and sources:
 *  - GC retention model: ln k = a0 + a1 n + (b0 + b1 n)/T (T in K) for an n-alkane with n carbons,
 *    fitted to the simulated ladders of the course labs (Lesson 25.4, DB-5 type 30 m x 0.25 mm x 0.25 um,
 *    He about 30 cm/s, 60 °C + 3 K/min: C8 3.40, C9 5.60, C10 8.70, C11 12.30, C12 16.05, C13 19.80,
 *    C14 23.45 min; Lesson 19.4, DB-Wax: C10 4.10 ... C16 17.70 min) with b1 fixed at 560 K
 *    (about 4.7 kJ/mol per CH2). A compound of retention index I behaves as an alkane with n = I/100.
 *  - DB-5 retention indices: NIST Chemistry WebBook medians as used in the Lesson 25.4 lab
 *    (alpha-pinene 937, beta-pinene 979, myrcene 991, p-cymene 1026, limonene 1031, gamma-terpinene 1061,
 *    linalool 1099, alpha-terpineol 1190, neral 1241, geranial 1270). DB-Wax: limonene 1196, linalool 1552
 *    (Lesson 19.4, NIST); alpha-pinene 1021, beta-pinene 1110, myrcene 1161, p-cymene 1270,
 *    gamma-terpinene 1245, alpha-terpineol 1700, neral 1680, geranial 1730 are approximate literature
 *    values (illustrative).
 *  - Lemon-oil area percentages as in the Lesson 25.4 simulated run (limonene 65, beta-pinene 11.5,
 *    gamma-terpinene 9.5, ... p-cymene 0.9 co-eluting with limonene).
 *  - Golay plate height for a 0.25 mm capillary: H = (Hmin/2)(uopt/u + u/uopt), Hmin 0.25 mm,
 *    uopt N2 12, He 25, H2 40 cm/s (Lesson 19.4 ranges).
 *  - HPLC: linear solvent strength log k = log kw - S phi at pH 2.5 in acetonitrile (Lesson 25.5 data);
 *    pKa aspirin 3.5, salicylic acid 2.97 (PubChem); paracetamol and caffeine neutral between pH 2 and 7.
 *    The anion is retained 2 % as strongly as the neutral acid (illustrative). Methanol parameters
 *    illustrative. t0 = 1.00 min for 150 mm at 1.0 mL/min. Areas, tailing and the aged column as in the
 *    Lesson 25.5 system-suitability data.
 *  - van Deemter: packed GC A 0.35 mm, B 6.0 mm cm/s, C 0.040 mm s/cm, 2 m (Lesson 19.3 data);
 *    HPLC 5 um A 5.0 um, B 8.0 um mm/s, C 4.0 um s/mm; 2.7 um core-shell 2.5, 8.0, 1.2 (Lesson 19.5 data);
 *    u = 1.554 mm/s per mL/min in 4.6 mm columns; 80.4 bar (5 um) and 276 bar (core-shell) per mL/min
 *    per 100 mm in water/methanol 70/30 (from the Lesson 19.5 practical answers).
 */
(function () {
  "use strict";
  var S = Sim.stats;

  var PRESETS = {
    gc: {
      title: "Gas chromatography and the general elution problem", tab: "gc", sample: "mix", gas: "N2", u: 12, T0: 60, rate: 0, Tmax: 250,
      what: "A capillary GC separates volatile compounds by how long each spends dissolved in the stationary film. At a fixed oven temperature light compounds come out early and crowded while heavy ones take very long: the general elution problem. A temperature programme (start cool, ramp) spaces early and late peaks evenly. The carrier gas sets how fast you can go at the same efficiency: hydrogen has the highest optimum velocity.",
      task: "Run the citrus test mix isothermally at 60 °C, then at 150 °C. Set a ramp (60 °C, then 5 K/min) and find a programme that resolves every pair with R<sub>s</sub> ≥ 1.5 in under 20 minutes. Then switch the carrier from nitrogen to hydrogen, press \"Set u to this gas's optimum\", and compare the run time at the same efficiency. Finally run the alkane ladder and read the retention indices.",
      target: "At 60 °C only four peaks appear within 120 min (α-pinene at about 34 min); at 150 °C all eight leave within 5 min and the first six crowd together (R<sub>s</sub> below 1); 60 °C + 5 K/min separates all eight (worst pair β-pinene/myrcene, R<sub>s</sub> about 4) in about 17 min with nitrogen at 12 cm/s and about 12 min with hydrogen at 40 cm/s. With the ladder: RIs within a few units of 937, 979, 991, 1031, 1061, 1099, 1241 and 1270."
    },
    "temperature-program": {
      title: "Temperature programme for a lemon oil", tab: "gc", sample: "lemon", gas: "He", u: 30, T0: 60, rate: 3, Tmax: 250, det: "ms",
      what: "Lemon oil is about two-thirds limonene with smaller amounts of pinenes, γ-terpinene, citrals and a trace of p-cymene. On a non-polar DB-5 column p-cymene (RI 1026) elutes 5 index units before limonene (1031), under a peak 70 times bigger. The ramp rate trades run time against resolution; no reasonable ramp separates that pair on this column.",
      task: "Run the lemon oil isothermally at 60 °C and at 150 °C and note what goes wrong. Then run 60 °C followed by 3, 5 and 10 K/min; for each, read R<sub>s</sub> of p-cymene/limonene and the run time. Choose the fastest ramp that keeps every other pair above 1.5, and run the alkane ladder under that programme. Overlay the m/z 119 extracted-ion chromatogram, then try the polar wax column.",
      target: "Isothermal runs either crowd the early peaks or take far too long. At split 1:50, 3, 5 and 10 K/min give run times of about 18.7, 12.9 and 7.8 min and p-cymene/limonene R<sub>s</sub> of about 1.2, 1.1 and 0.7: never baseline-separated, while every other pair stays above 4. The m/z 119 trace shows p-cymene as its own small peak just before limonene; on the wax column the two are about 70 index units apart (limonene 1196, p-cymene 1270)."
    },
    hplc: {
      title: "HPLC method building", tab: "hplc", sample: "four", org: "acn", phi: 20, pH: 2.5,
      what: "Reversed phase on C18: the more hydrophobic compound elutes later. Retention falls about tenfold for every 20–25 % more organic solvent (log k = log k<sub>w</sub> − Sφ). Aspirin and salicylic acid are carboxylic acids and are retained only as the neutral molecule, so their retention follows the pH; paracetamol and caffeine are neutral at these pH values.",
      task: "Inject the four-compound standard at pH 2.5 with 20 % and then 40 % acetonitrile and record the retention times (the log under the table fits log k<sub>w</sub> and S). Change the pH to 3.5 and 4.5 at 25 %. Replace acetonitrile by methanol at a composition with similar retention. Then run a 5–60 % gradient in 10 min. Finish with a system-suitability test on the new and on the aged column.",
      target: "At 20 %: about 2.8, 3.8, 13.6 and 19.2 min; at 40 %: 1.4–2.7 min; S ≈ 3.2, 4.3, 5.0, 5.2 and log k<sub>w</sub> ≈ 0.90, 1.30, 2.10, 2.30. At pH 3.5 salicylic acid moves ahead of aspirin. At pH 4.5 the two acids elute near the void and almost together; methanol (about 43 %) changes the spacing of paracetamol and caffeine; the gradient is faster but its baseline drifts. The new column passes the SST, the aged one fails on the tailing of salicylic acid (about 2.3)."
    },
    overlap: {
      title: "Overlapping peaks and the three levers", tab: "hplc", sample: "pair", org: "acn", phi: 33, pH: 2.5,
      what: "R<sub>s</sub> = (√N/4)·((α − 1)/α)·(k/(1 + k)). Paracetamol and caffeine at 33 % acetonitrile have k below 1 and α only about 1.09, so they overlap. You can raise N (a longer column), k (less organic solvent) or α (another solvent). They cost very different amounts of time.",
      task: "Inject at 33 % acetonitrile and note R<sub>s</sub> and the run time. Then improve it three ways, one at a time: the 300 mm column, 28 % acetonitrile, and methanol at a composition with similar retention (about 43 %). Compare the gain in R<sub>s</sub> and the cost in time in the run log.",
      target: "R<sub>s</sub> about 0.9 at 33 % (run 1.8 min); the 300 mm column gives about 1.3 (+40 %, ×√2) for twice the time and pressure; 28 % acetonitrile about 2.8 and 43 % methanol about 5, both in about 2.1–2.2 min."
    },
    "van-deemter": {
      title: "van Deemter curve and plate height", tab: "vd", col: "packed",
      what: "A band broadens as it travels: by multiple paths around particles (A, independent of flow), by diffusion along the column while it waits (B/u) and by slow exchange with the stationary phase (Cu). The sum H = A + B/u + Cu has a minimum at u<sub>opt</sub> = √(B/C), where the column gives the most plates, N = L/H.",
      task: "Change the velocity in steps from very slow to very fast and measure H at each (or measure 12 velocities). Find the velocity that gives the most plates, then double it and note how many plates you lose. Switch from the packed to the capillary column and watch the A term disappear.",
      target: "Packed column: u<sub>opt</sub> ≈ 12.2 cm/s, H<sub>min</sub> ≈ 1.33 mm, about 1500 plates for 2 m; at twice u<sub>opt</sub> about 16 % fewer plates; capillary: A ≈ 0."
    }
  };

  var preset = Sim.preset(PRESETS, "gc");
  var seed = Sim.seedFromQuery(19);
  var csvFns = {}, tabName = preset.tab;

  Sim.label();
  Sim.presetBox(Sim.$("#preset"), preset);
  function showSeed() { Sim.$$(".seed").forEach(function (e) { e.textContent = String(seed); }); }
  showSeed();

  function $id(id) { return Sim.$("#" + id); }
  function num(id) { return parseFloat($id(id).value); }
  function chk(id) { return !!$id(id).checked; }
  function kvFill(box, rows) {
    box.textContent = "";
    rows.forEach(function (r) { box.appendChild(Sim.el("div", { html: r[0] })); box.appendChild(Sim.el("div", { html: r[1], class: r[2] || null })); });
  }
  function fillBody(tbody, rows) {
    tbody.textContent = "";
    rows.forEach(function (r) {
      var tr = Sim.el("tr");
      r.forEach(function (c) { tr.appendChild(Sim.el("td", typeof c === "object" && c ? c : { html: String(c) })); });
      tbody.appendChild(tr);
    });
  }
  // error function (Abramowitz–Stegun 7.1.26, |error| < 1.5e-7)
  function erf(x) {
    var s = x < 0 ? -1 : 1; x = Math.abs(x);
    var t = 1 / (1 + 0.3275911 * x);
    var y = 1 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * Math.exp(-x * x);
    return s * y;
  }
  // cumulative fraction of a split Gaussian (sigma sf before the apex, sb after) up to x
  function splitCdf(x, mu, sf, sb) {
    var w = sf / (sf + sb);
    if (x < mu) return w * (1 + erf((x - mu) / (sf * Math.SQRT2)));
    return w + (1 - w) * erf((x - mu) / (sb * Math.SQRT2));
  }

  /* ======================= GC ======================= */
  var PHASE = {
    db5: { a0: -21.5928, a1: -0.5743, b0: 4396.82, b1: 560, name: "DB-5" },
    wax: { a0: -38.893, a1: -0.5873, b0: 9725.22, b1: 560, name: "DB-Wax" }
  };
  var GAS = { N2: { uopt: 12, name: "N₂" }, He: { uopt: 25, name: "He" }, H2: { uopt: 40, name: "H₂" } };
  var HMIN = 0.25;          // mm, 0.25 mm i.d. capillary
  // name, RI on DB-5, RI on wax, m/z 119 (relative to TIC), fraction in the test mix, in lemon oil
  var TERP = [
    ["α-pinene", 937, 1021, 0, 0.12, 0.018],
    ["β-pinene", 979, 1110, 0, 0.12, 0.115],
    ["myrcene", 991, 1161, 0, 0.12, 0.016],
    ["p-cymene", 1026, 1270, 0.9, 0, 0.009],
    ["limonene", 1031, 1196, 0, 0.12, 0.650],
    ["γ-terpinene", 1061, 1245, 0.02, 0.12, 0.095],
    ["linalool", 1099, 1552, 0, 0.12, 0.004],
    ["α-terpineol", 1190, 1700, 0, 0, 0.005],
    ["neral", 1241, 1680, 0, 0.12, 0.011],
    ["geranial", 1270, 1730, 0, 0.12, 0.018]
  ];
  var gPlot = Sim.plot($id("g-plot"), { xLabel: "t / min", yLabel: "signal / pA" });
  var gRuns = [], gCount = 0, ladders = {}, gLast = null;

  function gcCond() {
    return {
      sample: $id("g-sample").value, split: parseInt($id("g-split").value, 10), phase: $id("g-phase").value,
      L: parseInt($id("g-len").value, 10), gas: $id("g-gas").value, u: Math.max(1, num("g-u")),
      T0: num("g-T0"), hold: Math.max(0, num("g-hold") || 0), rate: Math.max(0, num("g-rate") || 0), Tmax: Math.max(num("g-T0"), num("g-Tmax")),
      det: $id("g-det").value, delay: Math.max(0, num("g-delay") || 0)
    };
  }
  function condKey(c) { return [c.phase, c.L, c.gas, c.u, c.T0, c.hold, c.rate, c.Tmax].join("|"); }
  function condText(c) {
    return PHASE[c.phase].name + " " + c.L + " m, " + GAS[c.gas].name + " " + c.u + " cm/s, " + (c.rate > 0 ? c.T0 + " °C" + (c.hold ? " (" + c.hold + " min)" : "") + " + " + c.rate + " K/min to " + c.Tmax + " °C" : "isothermal " + c.T0 + " °C") + ", " + (c.split > 1 ? "split 1:" + c.split : "splitless");
  }
  function components(c) {
    var out = [], dil = 0.85 * 1e3 * 0.01 / (c.split > 1 ? c.split + 1 : 1.1);   // ug of oil reaching the column
    out.push({ name: "hexane (solvent)", n: 6, solvent: true, m: 660 / (c.split > 1 ? c.split + 1 : 1.1), e119: 0 });
    if (c.sample === "ladder") {
      for (var n = 8; n <= 18; n++) out.push({ name: "n-C" + n, n: n, alk: n, m: 0.1 / (c.split > 1 ? c.split + 1 : 1.1), e119: 0 });
    } else if (c.sample !== "blank") {
      TERP.forEach(function (t) {
        var fr = c.sample === "mix" ? t[4] : t[5];
        if (fr > 0) out.push({ name: t[0], n: (c.phase === "db5" ? t[1] : t[2]) / 100, m: dil * fr, e119: t[3], ri5: t[1] });
      });
    }
    return out;
  }
  function gcSimulate(c, rng) {
    var ph = PHASE[c.phase], tM = c.L * 100 / c.u / 60;                // min
    var H = HMIN / 2 * (GAS[c.gas].uopt / c.u + c.u / GAS[c.gas].uopt), N = c.L * 1000 / H;
    var comps = components(c), dt = 0.004, tEnd = 120, Tk = function (t) { return 273.15 + (c.rate > 0 ? Math.min(c.Tmax, c.T0 + c.rate * Math.max(0, t - c.hold)) : c.T0); };
    var frac = comps.map(function () { return 0; }), done = comps.map(function () { return false; });
    for (var t = 0; t < tEnd; t += dt) {
      var T = Tk(t + dt / 2), all = true;
      for (var j = 0; j < comps.length; j++) {
        if (done[j]) continue;
        all = false;
        var k = Math.exp(ph.a0 + ph.a1 * comps[j].n + (ph.b0 + ph.b1 * comps[j].n) / T), df = dt / (tM * (1 + k));
        if (frac[j] + df >= 1) {
          comps[j].tR = t + dt * (1 - frac[j]) / df; comps[j].ke = k; comps[j].Te = T - 273.15; done[j] = true;
        } else frac[j] += df;
      }
      if (all) break;
    }
    comps.forEach(function (p) {
      if (!p.tR) return;
      p.tR += rng.normal(0, 0.002);
      var sig = tM * (1 + p.ke) / Math.sqrt(N);
      var ov = p.solvent ? 1 : 1 + p.m / 0.03;                       // overload above about 0.03 ug
      p.sf = sig * (p.solvent ? 3 : ov); p.sb = sig * (p.solvent ? 6 : 1 + 0.25 * (ov - 1));
      p.w = 2 * (p.sf + p.sb); p.wh = 1.1774 * (p.sf + p.sb); p.ov = ov;
      p.area = p.m * 4000 * (p.alk || p.solvent ? 1 : 0.95);             // FID: roughly proportional to mass
    });
    return { c: c, tM: tM, N: N, comps: comps, Tk: Tk };
  }
  function gcTrace(res, rng, which) {
    var c = res.c, el = res.comps.filter(function (p) { return p.tR; });
    var tLast = el.length ? Math.max.apply(null, el.map(function (p) { return p.tR + 4 * p.sb; })) : 10;
    var tEnd = Math.min(120, Math.max(tLast * 1.05, res.tM * 2)), nb = 6000, dt = tEnd / nb, out = [];
    var top = 0;
    el.forEach(function (p) { if (!p.solvent) top = Math.max(top, p.area / (2.5066 * (p.sf + p.sb) / 2) / 60); });
    if (!top) top = 50;
    for (var b = 0; b < nb; b++) {
      var a = b * dt, z = a + dt, y = 0;
      for (var j = 0; j < el.length; j++) {
        var p = el[j], wgt = which === "eic" ? p.e119 : 1;
        if (!wgt || a > p.tR + 8 * p.sb || z < p.tR - 8 * p.sf) continue;
        y += wgt * p.area * (splitCdf(z, p.tR, p.sf, p.sb) - splitCdf(a, p.tR, p.sf, p.sb)) / (dt * 60);
      }
      var T = res.Tk(a) - 273.15;
      y += 0.004 * top * Math.exp((T - 250) / 20) + rng.normal(0, 0.002 * top);   // column bleed and noise
      if (c.det === "ms" && a < c.delay) y = 0;
      out.push([a + dt / 2, Math.min(y, top * 1.25)]);
    }
    return { data: out, top: top };
  }
  function riOf(p, c, lad) {
    if (!lad) return null;
    var ns = Object.keys(lad).map(Number).sort(function (a, b) { return a - b; });
    for (var i = 0; i < ns.length - 1; i++) {
      var t1 = lad[ns[i]], t2 = lad[ns[i + 1]];
      if (p.tR >= t1 && p.tR <= t2) {
        if (c.rate > 0) return 100 * (ns[i] + (p.tR - t1) / (t2 - t1));
        var tm = lad.tM, l = function (x) { return Math.log(x - tm); };
        return 100 * (ns[i] + (l(p.tR) - l(t1)) / (l(t2) - l(t1)));
      }
    }
    return null;
  }
  function gcRun() {
    gCount++;
    var c = gcCond(), rng = Sim.rng(seed + 31 * gCount), res = gcSimulate(c, rng);
    var tr = gcTrace(res, rng, "tic"), eic = c.det === "ms" && chk("g-eic") ? gcTrace(res, Sim.rng(seed + 31 * gCount + 5), "eic") : null;
    res.trace = tr; res.eic = eic; res.id = gCount;
    var smp = res.comps.filter(function (p) { return !p.solvent; });
    if (c.sample === "ladder") {
      var lad = { tM: res.tM };
      smp.forEach(function (p) { if (p.tR) lad[p.alk] = p.tR; });
      ladders[condKey(c)] = lad;
    }
    var el = smp.filter(function (p) { return p.tR; }).sort(function (a, b) { return a.tR - b.tR; });
    var worst = null;
    for (var i = 0; i < el.length - 1; i++) {
      var rs = (el[i + 1].tR - el[i].tR) / (2 * (el[i].sb + el[i + 1].sf));   // facing sides of the two peaks
      el[i].rs = rs;
      if (!worst || rs < worst.rs) worst = { rs: rs, a: el[i].name, b: el[i + 1].name };
    }
    res.el = el; res.worst = worst; res.missing = smp.length - el.length;
    gLast = res;
    gRuns.push({ id: gCount, sample: c.sample, cond: condText(c), last: el.length ? el[el.length - 1].tR : NaN, worst: worst, missing: res.missing });
    gcDraw();
  }
  function gcDraw() {
    $id("g-ms-row").hidden = $id("g-det").value !== "ms";
    $id("g-eic-row").hidden = $id("g-det").value !== "ms";
    var info = [], names = chk("g-names");
    if (!gLast) { gPlot.draw([{ type: "hline", y: 0, color: "muted" }], {}); kvFill($id("g-info"), [["status", "Set the conditions and inject."]]); return; }
    var r = gLast, c = r.c, ser = [{ type: "line", color: "s1", label: c.det === "ms" ? "TIC" : "FID", data: r.trace.data }];
    if (r.eic) ser.push({ type: "line", color: "s2", label: "m/z 119 (×5)", data: r.eic.data.map(function (q) { return [q[0], q[1] * 5]; }) });
    var lad = ladders[condKey(c)];
    if (names) r.el.forEach(function (p) { if (p.area / (p.sf + p.sb) > r.trace.top * 0.05 * 2.5066 / 2 * 60 || r.el.length < 12) ser.push({ type: "text", x: p.tR, y: Math.min(r.trace.top * 1.12, p.area / (1.2533 * (p.sf + p.sb)) / 60 * 1.03 + r.trace.top * 0.03), text: p.alk ? "C" + p.alk : p.name }); });
    gPlot.draw(ser, { yMin: 0, yMax: r.trace.top * 1.25 });
    info.push(["dead time t<sub>M</sub>", r.tM.toFixed(2) + " min (L/u)"]);
    info.push(["plates at this velocity", Math.round(r.N).toLocaleString("en-US") + " (H = " + (c.L * 1000 / r.N).toFixed(3) + " mm; optimum for " + GAS[c.gas].name + " " + GAS[c.gas].uopt + " cm/s)"]);
    var solv = r.comps[0];
    if (solv.tR) info.push(["solvent peak", "ends near " + (solv.tR + 4 * solv.sb).toFixed(2) + " min" + (c.det === "ms" && c.delay < solv.tR + 4 * solv.sb ? " — the filament is on during the solvent: raise the solvent delay" : "")]);
    if (r.missing) info.push(["not eluted by 120 min", r.missing + " compound(s): too cold"]);
    if (r.worst) info.push(["worst pair", (names ? r.worst.a + " / " + r.worst.b : "") + " R<sub>s</sub> = " + r.worst.rs.toFixed(2), r.worst.rs < 1.5 ? "miss" : "hit"]);
    var big = r.el.filter(function (p) { return p.ov > 1.5; });
    if (big.length) info.push(["overloaded", big.map(function (p) { return names ? p.name : "t = " + p.tR.toFixed(2); }).join(", ") + ": broad, fronting peaks; a higher split ratio sharpens them"]);
    info.push(["RI", lad ? "from the ladder run under the same conditions" : "run the alkane ladder under these exact conditions to get indices"]);
    kvFill($id("g-info"), info);
    var tot = r.el.reduce(function (s, p) { return s + p.area; }, 0);
    fillBody(Sim.$("#g-table tbody"), r.el.map(function (p, i) {
      var ri = riOf(p, c, lad);
      return [names ? (p.alk ? "n-C" + p.alk : p.name) : "P" + (i + 1), p.tR.toFixed(3), p.wh.toFixed(3), Sim.sig(p.ke, 2), (100 * p.area / tot).toFixed(1), ri ? Math.round(ri) : "—", p.rs !== undefined ? { text: p.rs.toFixed(2), class: p.rs < 1.5 ? "miss" : "" } : "—"];
    }));
    fillBody(Sim.$("#g-log tbody"), gRuns.slice().reverse().map(function (g) {
      return [g.id, g.sample, g.cond, isFinite(g.last) ? g.last.toFixed(2) + (g.missing ? " (+" + g.missing + " missing)" : "") : "—", g.worst ? (names ? g.worst.a + " / " + g.worst.b : "") : "—", g.worst ? g.worst.rs.toFixed(2) : "—"];
    }));
    csvFns.gc = function () {
      var rows = [];
      gRuns.forEach(function () {});
      r.el.forEach(function (p, i) { rows.push(["peak", r.id, names ? (p.alk ? "n-C" + p.alk : p.name) : "P" + (i + 1), +p.tR.toFixed(3), +p.wh.toFixed(4), +(100 * p.area / tot).toFixed(2), riOf(p, c, lad) ? Math.round(riOf(p, c, lad)) : ""]); });
      r.trace.data.forEach(function (q, i) { if (i % 3 === 0) rows.push(["trace", r.id, "", +q[0].toFixed(4), "", +q[1].toFixed(3), ""]); });
      return { header: ["row", "run", "peak", "t_min", "w_half_min", "area_percent_or_signal_pA", "RI"], rows: rows, filename: "gc_run_" + r.id + ".csv" };
    };
  }
  $id("g-sample").value = preset.sample || "mix";
  $id("g-gas").value = preset.gas || "He";
  $id("g-u").value = String(preset.u || 30);
  $id("g-T0").value = String(preset.T0 || 60);
  $id("g-rate").value = String(preset.rate === undefined ? 3 : preset.rate);
  $id("g-Tmax").value = String(preset.Tmax || 250);
  $id("g-det").value = preset.det || "fid";
  $id("g-run").addEventListener("click", gcRun);
  $id("g-rerun").addEventListener("click", function () { seed = Sim.newSeed(seed); showSeed(); gcRun(); });
  $id("g-uopt").addEventListener("click", function () { $id("g-u").value = String(GAS[$id("g-gas").value].uopt); });
  ["g-names", "g-det"].forEach(function (id) { $id(id).addEventListener("change", gcDraw); });

  /* ======================= HPLC ======================= */
  // name, pKa (null = neutral), {acn: [log kw, S], meoh: [log kw, S]} at pH 2.5, area at 1 mL/min, tailing (new)
  var DRUGS = [
    { name: "paracetamol", pKa: null, acn: [0.90, 3.2], meoh: [0.95, 2.6], area: 1520, tail: 1.10 },
    { name: "caffeine", pKa: null, acn: [1.30, 4.3], meoh: [1.45, 3.3], area: 980, tail: 1.10 },
    { name: "aspirin", pKa: 3.5, acn: [2.10, 5.0], meoh: [2.30, 4.0], area: 2210, tail: 1.10 },
    { name: "salicylic acid", pKa: 2.97, acn: [2.30, 5.2], meoh: [2.55, 4.1], area: 340, tail: 1.25 }
  ];
  var ANION = 0.02;
  var NORM = 10000 / 9166;     // scales the van Deemter plate count so the 150 mm, 5 um column gives N = 10 000 at 1 mL/min, as in the Lesson 25.5 data
  var COLS = {
    "5": { L: 150, dp: "5 µm", A: 5.0, B: 8.0, C: 4.0, bar: 80.4 },
    "5L": { L: 300, dp: "5 µm", A: 5.0, B: 8.0, C: 4.0, bar: 80.4 },
    "27": { L: 150, dp: "2.7 µm core–shell", A: 2.5, B: 8.0, C: 1.2, bar: 276 }
  };
  var hPlot = Sim.plot($id("h-plot"), { xLabel: "t / min", yLabel: "A₂₃₀ / mAU" });
  var hRuns = [], hCount = 0, hLast = null, hSST = null;

  function fNeutral(pH, pKa) { return pKa === null ? 1 : 1 / (1 + Math.pow(10, pH - pKa)); }
  function kOf(d, phi, pH, org) {
    var p = d[org], kHA = Math.pow(10, p[0] - p[1] * phi), f25 = fNeutral(2.5, d.pKa), f = fNeutral(pH, d.pKa);
    return kHA / (f25 + ANION * (1 - f25)) * (f + ANION * (1 - f));
  }
  function visc(phi, org) { return org === "meoh" ? 1 + 3.2 * phi * (1 - phi) : 1 + 0.6 * phi * (1 - phi); }
  function hCond() {
    var mode = $id("h-mode").value;
    return {
      sample: $id("h-sample").value, col: $id("h-col").value, age: $id("h-age").value, org: $id("h-org").value,
      pH: num("h-pH"), mode: mode, phi: num("h-phi") / 100, g1: num("h-g1") / 100, g2: num("h-g2") / 100, gt: Math.max(0.5, num("h-gt")),
      flow: Math.max(0.05, num("h-flow"))
    };
  }
  function hText(c) {
    return COLS[c.col].L + " mm " + COLS[c.col].dp + (c.age === "old" ? " (aged)" : "") + ", " + (c.org === "acn" ? "MeCN" : "MeOH") + " " +
      (c.mode === "iso" ? Math.round(c.phi * 100) + " %" : Math.round(c.g1 * 100) + "→" + Math.round(c.g2 * 100) + " % in " + c.gt + " min") + ", pH " + c.pH.toFixed(1) + ", " + c.flow.toFixed(2) + " mL/min";
  }
  function hSimulate(c, rng) {
    var col = COLS[c.col], t0 = 1.00 * (col.L / 150) / c.flow, u = 1.554 * c.flow;
    var H = col.A + col.B / u + col.C * u, N = NORM * col.L * 1000 / H * (c.age === "old" ? 0.55 : 1);
    var phiMax = c.mode === "iso" ? c.phi : Math.max(c.g1, c.g2);
    var pressure = c.flow * col.bar * col.L / 100 * visc(phiMax, c.org) / visc(0.3, "meoh");
    var phiAt = function (t) { return c.mode === "iso" ? c.phi : c.g1 + (c.g2 - c.g1) * Math.min(1, Math.max(0, t - t0) / c.gt); };
    var flowJit = 1 + rng.normal(0, 0.0015);
    var list = (c.sample === "pair" ? DRUGS.slice(0, 2) : DRUGS).map(function (d) {
      var p = { name: d.name, area: d.area / c.flow * (1 + rng.normal(0, 0.004)) };
      if (c.mode === "iso") { p.k = kOf(d, c.phi, c.pH, c.org); p.tR = t0 * (1 + p.k); }
      else {
        var x = 0, t = 0, dt = 0.002;
        while (x < 1 && t < 200) { var kk = kOf(d, phiAt(t), c.pH, c.org); x += dt / (t0 * (1 + kk)); t += dt; p.k = kk; }
        p.tR = t;
      }
      p.tR *= flowJit * (1 + rng.normal(0, 0.0002));   // pump flow varies all peaks together
      var tail = (d.name === "salicylic acid" && c.age === "old") ? 2.35 : d.tail;
      var sd = t0 * (1 + p.k) / Math.sqrt(N) * (c.mode === "grad" ? 0.8 : 1), rr = tauPerSigma(tail);
      p.sig = sd / Math.sqrt(1 + rr * rr);        // keep the total peak variance (and so N) set by the column
      p.tau = p.sig * rr;
      return p;
    });
    return { c: c, t0: t0, N: N, pressure: pressure, list: list, phiAt: phiAt };
  }
  // one peak on a grid: Gaussian convolved with an exponential (tail)
  function emg(grid, dt, p) {
    var y = new Float64Array(grid.length), h = p.area / 60 / (p.sig * 2.5066);
    for (var i = 0; i < grid.length; i++) { var z = (grid[i] - p.tR + p.tau) / p.sig; if (z > -9 && z < 9) y[i] = h * Math.exp(-0.5 * z * z); }
    if (p.tau > 1e-9) { var a = Math.exp(-dt / p.tau), prev = 0; for (var j = 0; j < y.length; j++) { prev = prev * a + y[j] * (1 - a); y[j] = prev; } }
    return y;
  }
  // measure apex, half width, USP tailing (5 % height) and plates on a single noise-free peak
  function measure(grid, y) {
    var im = 0;
    for (var i = 1; i < y.length; i++) if (y[i] > y[im]) im = i;
    var top = y[im];
    function cross(level, dir) { var j = im; while (j > 0 && j < y.length - 1 && y[j] > level * top) j += dir; var y1 = y[j], y2 = y[j - dir]; return grid[j] + (grid[j - dir] - grid[j]) * (level * top - y1) / (y2 - y1); }
    var l5 = cross(0.5, -1), r5 = cross(0.5, 1), l05 = cross(0.05, -1), r05 = cross(0.05, 1);
    var tR = grid[im], wh = r5 - l5, m0 = 0, m1 = 0, m2 = 0;
    for (var q = 0; q < y.length; q++) { m0 += y[q]; m1 += y[q] * grid[q]; }
    var mean = m1 / m0;
    for (q = 0; q < y.length; q++) m2 += y[q] * (grid[q] - mean) * (grid[q] - mean);
    var sd = Math.sqrt(m2 / m0);
    // plates from the statistical moments (robust for tailing peaks); Rs below uses the same widths
    return { tR: tR, wh: wh, sd: sd, N: Math.pow(mean / sd, 2), T: (r05 - l05) / (2 * (tR - l05)), top: top };
  }
  // tau/sigma of an exponentially modified Gaussian that gives a USP tailing factor T (table built once)
  var TAILTAB = null;
  function tauPerSigma(T) {
    if (T <= 1.0005) return 0;
    if (!TAILTAB) {
      TAILTAB = [];
      var n = 4000, dt = 0.01, grid = new Float64Array(n);
      for (var i = 0; i < n; i++) grid[i] = (i + 0.5) * dt;
      for (var r = 0; r <= 60; r++) { var ts = r * 0.1; TAILTAB.push([ts, measure(grid, emg(grid, dt, { tR: 12, sig: 1, tau: ts, area: 60 })).T]); }
    }
    for (var k = 1; k < TAILTAB.length; k++) if (TAILTAB[k][1] >= T) { var a = TAILTAB[k - 1], b = TAILTAB[k]; return a[0] + (b[0] - a[0]) * (T - a[1]) / (b[1] - a[1]); }
    return TAILTAB[TAILTAB.length - 1][0];
  }
  function hRun(silent, rngSeed) {
    var c = hCond(), rng = Sim.rng(rngSeed || seed + 41 * (++hCount)), r = hSimulate(c, rng);
    if (r.pressure > 400) {
      if (!silent) { hLast = { error: "Pump stopped: " + Math.round(r.pressure) + " bar is above the 400 bar limit. Lower the flow, or use the larger particles or a shorter column.", c: c }; hDraw(); }
      return null;
    }
    var tEnd = Math.max.apply(null, r.list.map(function (p) { return p.tR + 6 * p.sig + 6 * p.tau; })) * 1.05;
    if (c.mode === "grad") tEnd = Math.max(tEnd, r.t0 + c.gt + 1);
    var n = 5000, dt = tEnd / n, grid = new Float64Array(n), sig = new Float64Array(n);
    for (var i = 0; i < n; i++) grid[i] = (i + 0.5) * dt;
    r.list.forEach(function (p) { var y = emg(grid, dt, p); var m = measure(grid, y); p.meas = m; for (var j = 0; j < n; j++) sig[j] += y[j]; });
    var uracil = emg(grid, dt, { tR: r.t0, sig: r.t0 / Math.sqrt(r.N) * 1.2, tau: 0, area: 60 / c.flow });
    var data = [];
    for (var k = 0; k < n; k++) {
      var drift = c.mode === "grad" ? (c.org === "acn" ? 15 : 45) * (r.phiAt(grid[k]) - c.g1) : 0;
      data.push([grid[k], sig[k] + uracil[k] + drift + rng.normal(0, 0.05)]);
    }
    r.trace = data;
    var sorted = r.list.slice().sort(function (a, b) { return a.tR - b.tR; }), worst = null;
    for (var q = 0; q < sorted.length - 1; q++) {
      var A = sorted[q].meas, B = sorted[q + 1].meas, rs = (B.tR - A.tR) / (2 * (A.sd + B.sd));
      sorted[q].rs = rs;
      if (!worst || rs < worst.rs) worst = { rs: rs, a: sorted[q].name, b: sorted[q + 1].name };
    }
    r.sorted = sorted; r.worst = worst; r.tEnd = sorted[sorted.length - 1].meas.tR;
    if (!silent) {
      hLast = r;
      hRuns.push({ id: hCount, c: c, text: hText(c), time: r.tEnd, worst: worst, pressure: r.pressure, ks: r.list.map(function (p) { return { name: p.name, k: (p.meas.tR - r.t0) / r.t0 }; }) });
      hDraw();
    }
    return r;
  }
  function hRunSST() {
    var reps = [];
    for (var i = 0; i < 6; i++) { var r = hRun(true, seed + 977 + 13 * i + 1000 * hCount); if (!r) { hRun(); return; } reps.push(r); }
    hCount++;
    var names = reps[0].sorted.map(function (p) { return p.name; }), rows = [], fails = [];
    names.forEach(function (nm) {
      var ps = reps.map(function (r) { return r.list.filter(function (p) { return p.name === nm; })[0]; });
      var areas = ps.map(function (p) { return p.area; }), rsd = 100 * S.sd(areas) / S.mean(areas);
      var T = S.mean(ps.map(function (p) { return p.meas.T; })), N = S.mean(ps.map(function (p) { return p.meas.N; }));
      if (rsd > 2) fails.push("area RSD of " + nm);
      if (T > 2) fails.push("tailing of " + nm);
      if (N < 5000) fails.push("plates of " + nm);
      rows.push([nm, "t<sub>R</sub> " + S.mean(ps.map(function (p) { return p.meas.tR; })).toFixed(3) + " min, area RSD " + rsd.toFixed(2) + " %, tailing " + T.toFixed(2) + ", N " + Math.round(N)]);
    });
    var rsMin = S.mean(reps.map(function (r) { return r.worst.rs; }));
    if (rsMin < 2) fails.push("critical-pair resolution");
    rows.unshift(["critical pair (mean of 6)", reps[0].worst.a + " / " + reps[0].worst.b + ": R<sub>s</sub> " + rsMin.toFixed(2)]);
    rows.push(["limits", "R<sub>s</sub> ≥ 2.0, tailing ≤ 2.0, area RSD ≤ 2.0 %, N ≥ 5000"]);
    rows.push(["verdict", fails.length ? "FAIL: " + fails.join(", ") + ". Results of this sequence would not be valid." : "PASS: the system may run samples today.", fails.length ? "miss" : "hit"]);
    hSST = { rows: rows, reps: reps };
    hLast = reps[5]; hLast.c = hCond();
    hDraw();
  }
  function hDraw() {
    $id("h-pH-out").textContent = num("h-pH").toFixed(1);
    $id("h-phi-out").textContent = num("h-phi").toFixed(0) + " %";
    $id("h-iso-row").hidden = $id("h-mode").value !== "iso";
    $id("h-grad-row").hidden = $id("h-mode").value === "iso";
    var info = [];
    if (!hLast) { hPlot.draw([{ type: "hline", y: 0, color: "muted" }], {}); kvFill($id("h-info"), [["status", "Set the method and inject."]]); }
    else if (hLast.error) { kvFill($id("h-info"), [["pump", hLast.error, "miss"]]); }
    else {
      var r = hLast, ser = [{ type: "line", color: "s1", label: "230 nm", data: r.trace }];
      r.sorted.forEach(function (p) { ser.push({ type: "text", x: p.meas.tR, y: p.meas.top * 1.06 + 2, text: p.name }); });
      ser.push({ type: "text", x: r.t0, y: 8, text: "t₀" });
      hPlot.draw(ser, { yMin: -2, xMin: 0 });
      info.push(["t₀, plates of the column", r.t0.toFixed(2) + " min, N ≈ " + Math.round(r.N).toLocaleString("en-US")]);
      info.push(["pressure", Math.round(r.pressure) + " bar (limit 400)"]);
      info.push(["run time (last peak)", r.tEnd.toFixed(2) + " min"]);
      if (r.worst) info.push(["critical pair", r.worst.a + " / " + r.worst.b + ", R<sub>s</sub> = " + r.worst.rs.toFixed(2), r.worst.rs < 1.5 ? "miss" : "hit"]);
      var acids = DRUGS.filter(function (d) { return d.pKa !== null; }).map(function (d) { return d.name + " " + Math.round(100 * fNeutral(r.c.pH, d.pKa)) + " %"; });
      if (r.c.sample === "four") info.push(["neutral fraction of the acids", acids.join(", ")]);
      if (r.c.mode === "grad") info.push(["gradient", "baseline rises with the organic fraction (the solvent absorbs a little at 230 nm)"]);
      kvFill($id("h-info"), info);
      fillBody(Sim.$("#h-table tbody"), r.sorted.map(function (p) {
        return [p.name, p.meas.tR.toFixed(3), ((p.meas.tR - r.t0) / r.t0).toFixed(2), r.c.mode === "grad" ? "—" : Math.round(p.meas.N), { text: p.meas.T.toFixed(2), class: p.meas.T > 2 ? "miss" : "" }, p.area.toFixed(0), p.rs !== undefined ? { text: p.rs.toFixed(2), class: p.rs < 1.5 ? "miss" : "" } : "—"];
      }));
    }
    kvFill($id("h-sstbox"), hSST ? hSST.rows : []);
    fillBody(Sim.$("#h-log tbody"), hRuns.slice().reverse().map(function (g) { return [g.id, g.text, g.time.toFixed(2), g.worst ? g.worst.a + " / " + g.worst.b : "—", g.worst ? g.worst.rs.toFixed(2) : "—", Math.round(g.pressure)]; }));
    // linear solvent strength from the two most recent isocratic runs at different phi (same pH, solvent, column)
    var iso = hRuns.filter(function (g) { return g.c.mode === "iso"; }), pair = null;
    for (var i = iso.length - 1; i > 0 && !pair; i--) for (var j = i - 1; j >= 0; j--) {
      var a = iso[i].c, b = iso[j].c;
      if (a.phi !== b.phi && a.pH === b.pH && a.org === b.org && a.col === b.col && a.sample === b.sample) { pair = [iso[j], iso[i]]; break; }
    }
    var lss = [];
    if (pair) {
      lss.push(["two scouting runs", Math.round(pair[0].c.phi * 100) + " % and " + Math.round(pair[1].c.phi * 100) + " % " + (pair[0].c.org === "acn" ? "acetonitrile" : "methanol") + ", pH " + pair[0].c.pH.toFixed(1)]);
      pair[0].ks.forEach(function (x, q) {
        var y = pair[1].ks[q], S2 = (Math.log10(x.k) - Math.log10(y.k)) / (pair[1].c.phi - pair[0].c.phi), lkw = Math.log10(x.k) + S2 * pair[0].c.phi;
        lss.push([x.name, "S = " + S2.toFixed(2) + ", log k<sub>w</sub> = " + lkw.toFixed(2)]);
      });
    } else lss.push(["linear solvent strength", "run the same sample isocratically at two compositions to fit log k = log k<sub>w</sub> − Sφ"]);
    kvFill($id("h-lss"), lss);
    csvFns.hplc = function () {
      var rows = [];
      hRuns.forEach(function (g) { g.ks.forEach(function (x) { rows.push(["run", g.id, g.text, x.name, +x.k.toFixed(4), ""]); }); });
      if (hSST) hSST.reps.forEach(function (r, i) { r.list.forEach(function (p) { rows.push(["sst", i + 1, hText(r.c), p.name, +p.meas.tR.toFixed(4), +p.area.toFixed(1) + ";N=" + Math.round(p.meas.N) + ";T=" + p.meas.T.toFixed(2)]); }); });
      return { header: ["kind", "run", "conditions", "compound", "k_or_tR_min", "area_plates_tailing"], rows: rows, filename: "hplc_runs.csv" };
    };
  }
  $id("h-sample").value = preset.sample === "pair" ? "pair" : "four";
  $id("h-org").value = preset.org || "acn";
  $id("h-phi").value = String(preset.phi || 25);
  $id("h-pH").value = String(preset.pH || 2.5);
  $id("h-run").addEventListener("click", function () { hRun(); });
  $id("h-sst").addEventListener("click", hRunSST);
  $id("h-rerun").addEventListener("click", function () { seed = Sim.newSeed(seed); showSeed(); hRun(); });
  ["h-pH", "h-phi"].forEach(function (id) { $id(id).addEventListener("input", function () { $id("h-pH-out").textContent = num("h-pH").toFixed(1); $id("h-phi-out").textContent = num("h-phi").toFixed(0) + " %"; }); });
  $id("h-mode").addEventListener("change", hDraw);

  /* ======================= VAN DEEMTER ======================= */
  var VCOL = {
    packed: { A: 0.35, B: 6.0, C: 0.040, L: 2000, uMin: 1, uMax: 45, uU: "cm/s", hU: "mm", Lmm: 2000, series: [2, 3, 4, 6, 8, 10, 12, 15, 20, 25, 30, 40] },
    cap: { A: 0, B: HMIN * 25 / 2, C: HMIN / (2 * 25), L: 30000, uMin: 3, uMax: 100, uU: "cm/s", hU: "mm", series: [5, 8, 10, 15, 20, 25, 30, 40, 50, 60, 80, 100] },
    lc5: { A: 5.0, B: 8.0, C: 4.0, L: 100000, uMin: 0.2, uMax: 5, uU: "mm/s", hU: "µm", bar: 80.4, series: [0.4, 0.6, 0.8, 1.0, 1.3, 1.6, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5] },
    lc27: { A: 2.5, B: 8.0, C: 1.2, L: 100000, uMin: 0.2, uMax: 5, uU: "mm/s", hU: "µm", bar: 276, series: [0.4, 0.6, 0.8, 1.0, 1.3, 1.6, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5] }
  };
  var vPlot = Sim.plot($id("v-plot"), { xLabel: "u", yLabel: "H" }), vPeak = Sim.plot($id("v-peak"), { xLabel: "t / s", yLabel: "signal" });
  var vData = [], vCount = 0;
  function vc() { return VCOL[$id("v-col").value]; }
  function vU() { var c = vc(); return c.uMin + (c.uMax - c.uMin) * num("v-u"); }
  function Hof(c, u) { return c.A + c.B / u + c.C * u; }
  function vMeasure(u) {
    vCount++;
    var c = vc(), r = Sim.rng(seed + 53 * vCount);
    var H = Hof(c, u) * (1 + r.normal(0, 0.02));
    vData.push({ col: $id("v-col").value, u: u, H: H });
  }
  // least squares H = A + B/u + C u (3 x 3 normal equations), with the covariance matrix
  function vFit(pts) {
    var X = pts.map(function (p) { return [1, 1 / p.u, p.u]; }), y = pts.map(function (p) { return p.H; });
    var M = [[0, 0, 0], [0, 0, 0], [0, 0, 0]], v = [0, 0, 0];
    X.forEach(function (x, i) { for (var a = 0; a < 3; a++) { v[a] += x[a] * y[i]; for (var b = 0; b < 3; b++) M[a][b] += x[a] * x[b]; } });
    var inv = inv3(M);
    if (!inv) return null;
    var p = [0, 1, 2].map(function (a) { return inv[a][0] * v[0] + inv[a][1] * v[1] + inv[a][2] * v[2]; });
    var ss = 0;
    X.forEach(function (x, i) { var e = y[i] - (p[0] + p[1] * x[1] + p[2] * x[2]); ss += e * e; });
    var s2 = pts.length > 3 ? ss / (pts.length - 3) : 0;
    var cov = inv.map(function (row) { return row.map(function (q) { return q * s2; }); });
    return { A: p[0], B: p[1], C: p[2], cov: cov };
  }
  function inv3(m) {
    var a = m[0][0], b = m[0][1], c = m[0][2], d = m[1][0], e = m[1][1], f = m[1][2], g = m[2][0], h = m[2][1], k = m[2][2];
    var det = a * (e * k - f * h) - b * (d * k - f * g) + c * (d * h - e * g);
    if (!isFinite(det) || Math.abs(det) < 1e-300) return null;
    return [[(e * k - f * h) / det, (c * h - b * k) / det, (b * f - c * e) / det],
            [(f * g - d * k) / det, (a * k - c * g) / det, (c * d - a * f) / det],
            [(d * h - e * g) / det, (b * g - a * h) / det, (a * e - b * d) / det]];
  }
  function propU(fn, p, cov) {      // first-order uncertainty of fn(A,B,C)
    var base = fn(p), g = [];
    for (var i = 0; i < 3; i++) { var q = p.slice(), hh = Math.abs(q[i]) * 1e-6 + 1e-9; q[i] += hh; g.push((fn(q) - base) / hh); }
    var v = 0;
    for (var a = 0; a < 3; a++) for (var b = 0; b < 3; b++) v += g[a] * g[b] * cov[a][b];
    return Math.sqrt(Math.max(0, v));
  }
  function vdDraw() {
    var key = $id("v-col").value, c = vc(), u = vU(), H = Hof(c, u), N = c.L / H, now = [];
    $id("v-u-label").textContent = "Velocity u / " + c.uU;
    $id("v-u-out").textContent = Sim.sig(u, 3) + " " + c.uU;
    now.push(["plate height H (true)", Sim.sig(H, 3) + " " + c.hU]);
    now.push(["plates N = L/H", Math.round(N).toLocaleString("en-US")]);
    var uo = Math.sqrt(c.B / c.C);
    now.push(["at u<sub>opt</sub> (true)", Sim.sig(uo, 3) + " " + c.uU + ", N = " + Math.round(c.L / Hof(c, uo)).toLocaleString("en-US")]);
    if (c.bar) { var flow = u / 1.554; now.push(["flow and pressure", flow.toFixed(2) + " mL/min, " + Math.round(flow * c.bar) + " bar" + (flow * c.bar > 400 ? " — above a 400 bar pump" : "")]); }
    kvFill($id("v-now"), now);
    // test peak with k = 3
    var Lcm = c.uU === "cm/s" ? c.L / 10 : c.L / 1000, t0 = c.uU === "cm/s" ? Lcm / u : (c.L / 1000) / u, tR = 4 * t0, sd = tR / Math.sqrt(N), pk = [];
    for (var i = 0; i <= 200; i++) { var t = tR - 5 * sd + 10 * sd * i / 200; pk.push([t, Math.exp(-0.5 * Math.pow((t - tR) / sd, 2))]); }
    vPeak.draw([{ type: "line", color: "s1", label: "t_R = " + Sim.sig(tR, 3) + " s, width 4σ = " + Sim.sig(4 * sd, 2) + " s", data: pk }], { yMin: 0 });
    // van Deemter plot
    var pts = vData.filter(function (p) { return p.col === key; }), ser = [], curve = [], cb = [], cc = [];
    for (var j = 0; j <= 200; j++) { var uu = c.uMin + (c.uMax - c.uMin) * j / 200; curve.push([uu, Hof(c, uu)]); cb.push([uu, c.B / uu]); cc.push([uu, c.C * uu]); }
    ser.push({ type: "line", color: "muted", label: "H (true)", data: curve });
    ser.push({ type: "hline", y: c.A, color: "s3", dash: [6, 4], label: "A" });
    ser.push({ type: "line", color: "s4", dash: [6, 4], label: "B/u", data: cb });
    ser.push({ type: "line", color: "s5", dash: [6, 4], label: "Cu", data: cc });
    ser.push({ type: "points", color: "s2", label: "measured", data: pts.map(function (p) { return [p.u, p.H]; }) });
    ser.push({ type: "vline", x: u, color: "s1", dash: [2, 3] });
    var fitRows = [];
    if (pts.length >= 4) {
      var f = vFit(pts);
      if (f) {
        var P = [f.A, f.B, f.C];
        var uopt = function (q) { return Math.sqrt(Math.max(1e-30, q[1] / q[2])); }, hmin = function (q) { return q[0] + 2 * Math.sqrt(Math.max(0, q[1] * q[2])); };
        fitRows.push(["A", Sim.fmtU(f.A, Math.sqrt(f.cov[0][0]), c.hU)]);
        fitRows.push(["B", Sim.fmtU(f.B, Math.sqrt(f.cov[1][1]), c.hU + " " + c.uU)]);
        fitRows.push(["C", Sim.fmtU(f.C, Math.sqrt(f.cov[2][2]), c.hU + " per " + c.uU)]);
        var uo2 = uopt(P), hm = hmin(P);
        fitRows.push(["u<sub>opt</sub> = √(B/C)", Sim.fmtU(uo2, propU(uopt, P, f.cov), c.uU)]);
        fitRows.push(["H<sub>min</sub> = A + 2√(BC)", Sim.fmtU(hm, propU(hmin, P, f.cov), c.hU) + ", N = " + Math.round(c.L / hm).toLocaleString("en-US")]);
        var h2 = f.A + f.B / (2 * uo2) + f.C * 2 * uo2;
        fitRows.push(["at 2 u<sub>opt</sub>", "N falls by " + Math.round(100 * (1 - hm / h2)) + " %, R<sub>s</sub> by " + Math.round(100 * (1 - Math.sqrt(hm / h2))) + " %, for half the run time"]);
        var fc = [];
        for (var q = 0; q <= 200; q++) { var ux = c.uMin + (c.uMax - c.uMin) * q / 200; fc.push([ux, f.A + f.B / ux + f.C * ux]); }
        ser.push({ type: "line", color: "s2", label: "fit", data: fc });
      }
    } else fitRows.push(["fit", "measure at least 4 velocities (spread both sides of the minimum)"]);
    var ymax = Math.max(Hof(c, c.uMin + (c.uMax - c.uMin) * 0.02), Hof(c, c.uMax)) * 1.1;
    vPlot.draw(ser, { xMin: 0, xMax: c.uMax, yMin: 0, yMax: Math.min(ymax, Hof(c, Math.sqrt(c.B / c.C)) * 5) });
    kvFill($id("v-fit"), fitRows);
    fillBody(Sim.$("#v-table tbody"), pts.map(function (p) { return [Sim.sig(p.u, 3) + " " + c.uU, Sim.sig(p.H, 4) + " " + c.hU, Math.round(c.L / p.H)]; }));
    csvFns.vd = function () { return { header: ["column", "u", "u_unit", "H", "H_unit", "N"], rows: vData.map(function (p) { var cc2 = VCOL[p.col]; return [p.col, +p.u.toPrecision(4), cc2.uU, +p.H.toPrecision(5), cc2.hU, Math.round(cc2.L / p.H)]; }), filename: "van_deemter.csv" }; };
  }
  $id("v-col").value = preset.col || "packed";
  (function () { var c = vc(); $id("v-u").value = String((Math.sqrt(c.B / c.C) * 0.5 - c.uMin) / (c.uMax - c.uMin)); })();
  $id("v-col").addEventListener("change", function () { var c = vc(); $id("v-u").value = String((Math.sqrt(c.B / c.C) * 0.5 - c.uMin) / (c.uMax - c.uMin)); vdDraw(); });
  $id("v-u").addEventListener("input", vdDraw);
  $id("v-meas").addEventListener("click", function () { vMeasure(vU()); vdDraw(); });
  $id("v-series").addEventListener("click", function () { vc().series.forEach(function (u) { vMeasure(u); }); vdDraw(); });
  $id("v-clear").addEventListener("click", function () { vData = vData.filter(function (p) { return p.col !== $id("v-col").value; }); vdDraw(); });
  $id("v-rerun").addEventListener("click", function () {
    seed = Sim.newSeed(seed); showSeed();
    var key = $id("v-col").value, us = vData.filter(function (p) { return p.col === key; }).map(function (p) { return p.u; });
    vData = vData.filter(function (p) { return p.col !== key; });
    us.forEach(vMeasure); vdDraw();
  });

  /* ======================= tabs and export ======================= */
  Sim.exportCSV($id("x-data"), "chromatography.csv", function () { var f = csvFns[tabName]; return f ? f() : null; });
  var DRAW = { gc: gcDraw, hplc: hDraw, vd: vdDraw };
  var tabs = Sim.tabs($id("tabs"), function (name) { tabName = name; DRAW[name](); });
  tabs.select(tabName);
})();
