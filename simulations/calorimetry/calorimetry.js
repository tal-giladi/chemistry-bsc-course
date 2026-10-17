/* calorimetry simulation: coffee-cup calibration, enthalpy of solution, enthalpy of
 * neutralisation and a bomb calorimeter, all analysed by extrapolating fore- and
 * after-lines to the mixing (firing) time. Uses ../common/sim.js (global Sim).
 *
 * Data (kJ/mol unless stated):
 *  - H+ + OH- -> H2O: -55.8 (OpenStax Chemistry 2e Appendix G: -285.83 - (-230.0)); Lesson 23.2.
 *  - Ionisation enthalpies: acetic acid -0.41, NH4+ +52.2 (Goldberg, Kishore, Lennen,
 *    J. Phys. Chem. Ref. Data 31 (2002) 231).
 *  - Enthalpies of solution at infinite dilution: NaHCO3 +19.6 (OpenStax App. G / NBS,
 *    Lesson 08.7); NH4NO3 +25.69, CaCl2 -81.3, NaCl +3.88, KCl +17.22 (CRC Handbook,
 *    "Enthalpy of solution of electrolytes").
 *  - Specific heats of the solids (J g^-1 K^-1, approximate): NaHCO3 1.0 (as in Lesson 08.7),
 *    NH4NO3 1.74, CaCl2 0.67, NaCl 0.86, KCl 0.69.
 *  - Benzoic acid 26.434 kJ/g (NIST SRM 39j certificate); sucrose DcH = DcU = -5644 kJ/mol
 *    and naphthalene DcH = -5156.3 kJ/mol (NIST Chemistry WebBook).
 *  - Fuse wire: about 9.6 J per cm burned (2.3 cal/cm, typical nickel-alloy fuse wire).
 *  - Water c = 4.184 J g^-1 K^-1. RT at 298.15 K = 2.479 kJ/mol (R from CODATA 2022).
 * Hidden "true" calorimeter constants: foam cup 30 J/K (35 J/K in the neutralisation set-up,
 * as in Lesson 23.2), bomb 10.885 kJ/K (Lesson 13.2). The 100 mL of 0.5 mol/L salt solution
 * made by neutralisation is given an effective heat capacity of 422.6 J/K (1 % above 100 g of
 * water), so that treating it as water gives the small error discussed in Lesson 23.2.
 */
(function () {
  "use strict";
  var S = Sim.stats, CW = 4.184, RT298 = Sim.C.R * 298.15 / 1000;

  var PRESETS = {
    "coffee-cup": {
      title: "Coffee-cup calorimeter", mode: "calibration",
      what: "A foam cup with a lid is a simple constant-pressure calorimeter. The cup, lid and thermometer absorb some of the heat, so you first calibrate them with hot and cold water. Because the cup slowly exchanges heat with the room, you extrapolate fore- and after-lines to the moment of mixing instead of trusting the highest or lowest reading.",
      task: "Run a calibration (50 g of water at 45 °C into 100 g of cold water) and note C<sub>cal</sub>. Then switch to <b>Dissolving a salt</b> and dissolve 5.00 g of baking soda in 100 g of water. Compare the extrapolated ΔT with the one from the lowest reading.",
      target: "C<sub>cal</sub> of a few tens of J/K, and Δ<sub>sol</sub>H(NaHCO₃) of about +16 to +20 kJ/mol; the lowest-reading ΔT differs from the extrapolated one."
    },
    dissolution: {
      title: "Enthalpy of solution", mode: "dissolution",
      what: "Dissolving breaks the crystal (costs energy) and hydrates the ions (releases energy). The difference can have either sign. A salt that dissolves slowly spreads its heat over minutes, while the cup keeps exchanging heat with the room; the extrapolation corrects for both.",
      task: "Calibrate the cup first (Cup calibration tab), then dissolve ammonium nitrate (endothermic, the cold-pack salt) and then anhydrous calcium chloride (exothermic). Note how the after-line and the extrapolation handle the slowly dissolving CaCl₂.",
      target: "Δ<sub>sol</sub>H(NH₄NO₃) close to +25.7 kJ/mol and Δ<sub>sol</sub>H(CaCl₂) close to −81 kJ/mol, each within about 5 %."
    },
    neutralisation: {
      title: "Enthalpy of neutralisation", mode: "neutralisation",
      what: "Strong acids and bases are fully ionised, so every strong-acid / strong-base pair runs the same reaction, H⁺ + OH⁻ → H₂O. A weak acid must also give up its proton, which adds its ionisation enthalpy.",
      task: "Mix 50.0 mL of 1.00 M HCl with 50.0 mL of 1.00 M NaOH, then HNO₃ + KOH, then acetic acid + NaOH. Predict each before you run it. Use the extrapolated ΔT, not the peak reading.",
      target: "From the strong-acid run, Δ<sub>neut</sub>H within 2 % of −55.8 kJ/mol (C<sub>cal</sub> = 35 J/K)."
    },
    bomb: {
      title: "Bomb calorimeter", mode: "bomb",
      what: "A sealed steel bomb with about 30 bar of oxygen sits in a stirred water bath. It works at constant volume, so it measures Δ<sub>c</sub>U. Its constant C<sub>cal</sub> (about 10 kJ/K) comes from burning benzoic acid, certified at 26.434 kJ/g.",
      task: "Burn about 1 g of benzoic acid and find C<sub>cal</sub> from the corrected rise. Burn the unknown sample offered and calculate Δ<sub>c</sub>U per gram and per mole, then Δ<sub>c</sub>H. Repeat the calibration once and compare the two C<sub>cal</sub> values.",
      target: "C<sub>cal</sub> around 10 kJ/K, with two calibrations agreeing within about 0.5 % when you use the corrected rise."
    }
  };

  var SALTS = {
    NaHCO3: { name: "sodium hydrogen carbonate (baking soda), NaHCO₃", M: 84.007, dH: 19.6, cs: 1.0, tau: 35 },
    NH4NO3: { name: "ammonium nitrate, NH₄NO₃", M: 80.043, dH: 25.69, cs: 1.74, tau: 25 },
    CaCl2: { name: "calcium chloride, anhydrous, CaCl₂", M: 110.98, dH: -81.3, cs: 0.67, tau: 60 },
    NaCl: { name: "sodium chloride, NaCl", M: 58.443, dH: 3.88, cs: 0.86, tau: 40 },
    KCl: { name: "potassium chloride, KCl", M: 74.551, dH: 17.22, cs: 0.69, tau: 30 }
  };
  var PAIRS = {
    "HCl-NaOH": { name: "HCl + NaOH", dH: -55.8 },
    "HNO3-KOH": { name: "HNO₃ + KOH", dH: -55.8 },
    "AcOH-NaOH": { name: "acetic acid + NaOH", dH: -55.8 - 0.41 },
    "NH4Cl-NaOH": { name: "NH₄Cl + NaOH (weak acid NH₄⁺)", dH: -55.8 + 52.2 }
  };
  var FUELS = {
    benzoic: { name: "benzoic acid, C₇H₆O₂ (calibration standard)", M: 122.12, perGram: 26.434, dn: -0.5, eq: "C₇H₆O₂(s) + 7.5 O₂ → 7 CO₂ + 3 H₂O(l)" },
    sucrose: { name: "sucrose, C₁₂H₂₂O₁₁", M: 342.30, dU: -5644, dn: 0, eq: "C₁₂H₂₂O₁₁(s) + 12 O₂ → 12 CO₂ + 11 H₂O(l)" },
    naphthalene: { name: "naphthalene, C₁₀H₈", M: 128.17, dU: -5156.3 + 2 * RT298, dn: -2, eq: "C₁₀H₈(s) + 12 O₂ → 10 CO₂ + 4 H₂O(l)" }
  };

  var preset = Sim.preset(PRESETS, "coffee-cup");
  var seed = Sim.seedFromQuery(23);
  var mode = preset.mode;
  var lastCcal = null;          // {value J/K, u}
  var bombCals = [];            // kJ/K values
  var runs = [], cur = null, anim = null;
  var plot = Sim.plot(Sim.$("#plot"), { xLabel: "time / s", yLabel: "temperature / °C" });

  Sim.label();
  Sim.presetBox(Sim.$("#preset"), preset);
  Sim.$("#seed").textContent = String(seed);

  /* ---------------- set-up forms ---------------- */
  function field(id, label, input) { return Sim.el("div", { class: "field" }, Sim.el("label", { for: id, html: label }), input); }
  function num(id, val, step, min, max) { return Sim.el("input", { type: "number", id: id, value: String(val), step: String(step), min: String(min), max: String(max) }); }
  function sel(id, obj, def) {
    var s = Sim.el("select", { id: id });
    Object.keys(obj).forEach(function (k) { s.appendChild(Sim.el("option", { value: k, text: obj[k].name })); });
    s.value = def;
    return s;
  }
  function v(id) { return parseFloat(Sim.$("#" + id).value); }
  function chk(id) { var e = Sim.$("#" + id); return !!(e && e.checked); }

  var unknownKey = Sim.rng(seed + 5).random() < 0.5 ? "sucrose" : "naphthalene";

  function buildSetup() {
    var box = Sim.$("#setup");
    box.textContent = "";
    var title = { calibration: "Calibration: hot water into cold water", dissolution: "Dissolving a salt in water", neutralisation: "Acid + base in a foam cup", bomb: "Bomb calorimeter" }[mode];
    Sim.$("#setup-title").textContent = title;
    if (mode === "calibration") {
      box.appendChild(field("s-mcold", "Cold water in the cup / g", num("s-mcold", "100.0", 0.1, 20, 200)));
      box.appendChild(field("s-mhot", "Hot water poured in / g", num("s-mhot", "50.0", 0.1, 10, 150)));
      box.appendChild(field("s-thot", "Hot water temperature (measured just before pouring) / °C", num("s-thot", "45.0", 0.1, 30, 60)));
      box.appendChild(Sim.el("div", { class: "row" }, Sim.el("label", {}, Sim.el("input", { type: "checkbox", id: "s-pour", checked: true }), " Hot water cools by about 0.5 K while being poured (realistic)")));
    } else if (mode === "dissolution") {
      box.appendChild(field("s-salt", "Salt", sel("s-salt", SALTS, preset.key === "coffee-cup" ? "NaHCO3" : "NH4NO3")));
      box.appendChild(field("s-ms", "Mass of salt / g", num("s-ms", "5.00", 0.01, 0.5, 20)));
      box.appendChild(field("s-mw", "Water in the cup / g", num("s-mw", "100.0", 0.1, 20, 200)));
      box.appendChild(field("s-ccal", "C<sub>cal</sub> used in the calculation / J K⁻¹", num("s-ccal", lastCcal ? lastCcal.value.toFixed(1) : "0", 0.1, 0, 500)));
      if (!lastCcal) box.appendChild(Sim.el("p", { class: "small warn", text: "No calibration yet in this session: run the Cup calibration first, or type a value." }));
    } else if (mode === "neutralisation") {
      box.appendChild(field("s-pair", "Acid + base", sel("s-pair", PAIRS, "HCl-NaOH")));
      box.appendChild(field("s-conc", "Concentration of each / mol L⁻¹", num("s-conc", "1.00", 0.01, 0.1, 2)));
      box.appendChild(field("s-vol", "Volume of each / mL", num("s-vol", "50.0", 0.1, 10, 100)));
      box.appendChild(field("s-ccal", "C<sub>cal</sub> used in the calculation / J K⁻¹", num("s-ccal", "35", 0.1, 0, 500)));
      box.appendChild(Sim.el("p", { class: "small muted", text: "Both solutions start at about 21 °C. The base is poured into the acid over about 10 s." }));
    } else {
      var fuels = { benzoic: FUELS.benzoic };
      fuels[unknownKey] = { name: "unknown sample offered: " + FUELS[unknownKey].name };
      box.appendChild(field("s-fuel", "Sample", sel("s-fuel", fuels, "benzoic")));
      box.appendChild(field("s-mass", "Pellet mass aimed for / g", num("s-mass", "1.00", 0.01, 0.3, 1.2)));
      box.appendChild(field("s-ccalb", "C<sub>cal</sub> used for the unknown / kJ K⁻¹", num("s-ccalb", bombCals.length ? S.mean(bombCals).toFixed(4) : "0", 0.0001, 0, 30)));
      box.appendChild(Sim.el("div", { class: "row" }, Sim.el("label", {}, Sim.el("input", { type: "checkbox", id: "s-fuse", checked: true }), " Correct for the fuse-wire energy (9.6 J per cm burned)")));
      box.appendChild(Sim.el("p", { class: "small muted", text: "The jacket is at 25.000 °C. The bath starts a little below it and drifts slowly towards it. Never burn more than about 1 g." }));
    }
    box.querySelectorAll("input, select").forEach(function (e) { e.addEventListener("change", function () { if (cur && cur.done && cur.mode === mode) reanalyseOnly(); }); });
  }

  function setTiming() {
    if (mode === "bomb") {
      Sim.$("#t-mix").value = "300"; Sim.$("#t-end").value = "1200"; Sim.$("#t-res").value = "0.001"; Sim.$("#a-skip").value = "300";
      Sim.$("#t-mix-label").textContent = "Fire at / s";
    } else {
      Sim.$("#t-mix").value = "180"; Sim.$("#t-end").value = mode === "dissolution" ? "900" : "600";
      if (Sim.$("#t-res").value === "0.001") Sim.$("#t-res").value = "0.01";
      Sim.$("#a-skip").value = mode === "dissolution" ? "300" : "120";
      Sim.$("#t-mix-label").textContent = "Mix at / s";
    }
  }

  /* ---------------- the physical model ---------------- */
  function simulate() {
    var r = Sim.rng(seed + 31 * (runs.length + 1));
    var tm = v("t-mix"), tEnd = Math.max(v("t-end"), tm + 120), step = v("t-int"), res = parseFloat(Sim.$("#t-res").value);
    var run = { mode: mode, tm: tm, tEnd: tEnd, res: res, readings: [], p: {} };
    var dt = 0.25, Tr, tau, tauP, noise, C, T, events;
    if (mode === "bomb") {
      Tr = 25.0; tau = 20000; tauP = 10; noise = 0.0005;
      C = 10885; T = 24.2 + r.uniform(-0.15, 0.15);
      var key = Sim.$("#s-fuel").value;
      var F = FUELS[key];
      var aim = v("s-mass");
      var m = Math.round((aim + r.uniform(-0.02, 0.02)) * 1e4) / 1e4;
      var Lfuse = Math.round(r.uniform(6, 9) * 10) / 10, Efuse = 9.6 * Lfuse;
      var perGram = key === "benzoic" ? F.perGram * 1000 : -F.dU / F.M * 1000;   // J/g released
      var Q = m * perGram + Efuse, tauC = r.uniform(35, 45);
      var Pstir = C * 0.001 / 60;
      run.p = { fuel: key, m: m, Lfuse: Lfuse, Efuse: Efuse, Q: Q };
      events = function (t) { var P = Pstir; if (t >= tm) P += Q / tauC * Math.exp(-(t - tm) / tauC); return { P: P }; };
    } else {
      Tr = 22.0; tau = 2400; tauP = 6; noise = 0.01;
      if (mode === "calibration") {
        var mc = v("s-mcold"), mh = v("s-mhot"), Th = v("s-thot"), loss = chk("s-pour") ? 0.5 : 0;
        C = mc * CW + 30; T = 21.0 + r.uniform(-0.3, 0.3);
        run.p = { mc: mc, mh: mh, Th: Th, loss: loss, Ccup: 30 };
        events = function (t) {
          if (t >= tm && t < tm + 10) return { dm: mh / 10, Tin: Th - loss, cin: CW };
          return {};
        };
      } else if (mode === "dissolution") {
        var sk = Sim.$("#s-salt").value, Sx = SALTS[sk], ms = v("s-ms"), mw = v("s-mw");
        var n = ms / Sx.M, tauS = Sx.tau * r.uniform(0.8, 1.2), added = false;
        C = mw * CW + 30; T = Tr - 0.4 + r.uniform(-0.2, 0.2);
        run.p = { salt: sk, ms: ms, mw: mw, n: n };
        events = function (t) {
          var out = {};
          if (t >= tm && !added) { added = true; out.addC = ms * Sx.cs; out.Tadd = Tr; }
          if (t >= tm) out.P = -n * Sx.dH * 1000 / tauS * Math.exp(-(t - tm) / tauS);
          return out;
        };
      } else {
        var pk = Sim.$("#s-pair").value, conc = v("s-conc"), vol = v("s-vol");
        var nA = conc * vol / 1000, nB = nA, Csol = 211.3 * vol / 50, Tb, reacted = 0;
        C = Csol + 35; T = 21.0 + r.uniform(-0.1, 0.1); Tb = T + r.uniform(-0.05, 0.05);
        run.p = { pair: pk, conc: conc, vol: vol, n: Math.min(nA, nB) };
        events = function (t) {
          if (t >= tm && t < tm + 10) {
            var dn = nB / 10, react = Math.min(dn, Math.max(0, nA - reacted) / dt);   // mol/s
            reacted += react * dt;
            return { dm: 1, Cin: Csol / 10, Tin: Tb, P: -PAIRS[pk].dH * 1000 * react };
          }
          return {};
        };
      }
    }
    var Tp = T, t = 0, nextRead = 0;
    while (t <= tEnd + 1e-9) {
      if (t >= nextRead - 1e-9) {
        var val = Math.round((Tp + r.normal(0, noise)) / res) * res;
        run.readings.push([Math.round(t), +val.toFixed(4)]);
        nextRead += step;
      }
      var e = events(t);
      if (e.addC) { T = (C * T + e.addC * e.Tadd) / (C + e.addC); C += e.addC; }
      if (e.dm) {
        var dC = e.Cin !== undefined ? e.Cin * dt : e.dm * dt * e.cin;
        T = (C * T + dC * e.Tin) / (C + dC); C += dC;
      }
      var P = e.P || 0;
      T += ((Tr - T) / tau + P / C) * dt;
      Tp += (T - Tp) / tauP * dt;
      t += dt;
    }
    run.Ctrue = C;
    return run;
  }

  /* ---------------- analysis ---------------- */
  function lineAt(f, t) { return f.a + f.b * t; }
  function lineU(f, t, n, res) {
    var u2 = f.ua * f.ua + t * t * f.ub * f.ub + 2 * t * f.cov;
    if (!isFinite(u2) || u2 < 0) u2 = 0;
    return Math.sqrt(u2 + res * res / 12 / n);
  }

  function propagate(fn, vals, us) {
    var y = fn(vals), u2 = 0;
    for (var i = 0; i < vals.length; i++) {
      if (!us[i]) continue;
      var h = Math.abs(vals[i]) * 1e-6 + 1e-9, vv = vals.slice();
      vv[i] += h;
      var d = (fn(vv) - y) / h;
      u2 += d * d * us[i] * us[i];
    }
    return { y: y, u: Math.sqrt(u2) };
  }

  function kvFill(el, rows) {
    el.textContent = "";
    rows.forEach(function (r) { el.appendChild(Sim.el("span", { text: r[0] })); el.appendChild(Sim.el("span", { class: r[2] || "", html: r[1] })); });
  }

  function analyse() {
    if (!cur) return null;
    var R = cur.readings, tm = cur.tm, skip = v("a-skip"), res = cur.res;
    var pre = R.filter(function (p) { return p[0] < tm; }), post = R.filter(function (p) { return p[0] >= tm + skip; });
    var series = [{ type: "points", data: R, color: "s1", size: 2.8, label: "readings" }, { type: "vline", x: tm, color: "muted", dash: [3, 3] }];
    var out = null;
    if (pre.length >= 2 && post.length >= 2 && cur.done) {
      var fa = S.linfit(pre.map(function (p) { return p[0]; }), pre.map(function (p) { return p[1]; }));
      var fb = S.linfit(post.map(function (p) { return p[0]; }), post.map(function (p) { return p[1]; }));
      var tx = tm;
      if (Sim.$("#a-to").value === "dick") {
        for (var i = 1; i < R.length; i++) {
          var t0 = R[i - 1][0], t1 = R[i][0];
          if (t1 < tm) continue;
          var f0 = (R[i - 1][1] - lineAt(fa, t0)) / (lineAt(fb, t0) - lineAt(fa, t0));
          var f1 = (R[i][1] - lineAt(fa, t1)) / (lineAt(fb, t1) - lineAt(fa, t1));
          if (t0 < tm) { f0 = 0; t0 = tm; }
          if (f1 >= 0.63) { tx = t0 + (0.63 - f0) / ((f1 - f0) || 1) * (t1 - t0); break; }
        }
      }
      var Ta = lineAt(fa, tx), Tb = lineAt(fb, tx), ua = lineU(fa, tx, pre.length, res), ub = lineU(fb, tx, post.length, res);
      var dT = Tb - Ta, udT = Math.sqrt(ua * ua + ub * ub);
      var postAll = R.filter(function (p) { return p[0] >= tm; }).map(function (p) { return p[1]; });
      var lastPre = pre[pre.length - 1][1];
      var dTx = (dT >= 0 ? S.max(postAll) : S.min(postAll)) - lastPre;
      out = { fa: fa, fb: fb, tx: tx, Ta: Ta, Tb: Tb, ua: ua, ub: ub, dT: dT, udT: udT, dTx: dTx };
      series.push({ type: "line", data: [[0, lineAt(fa, 0)], [tx + 30, lineAt(fa, tx + 30)]], color: "s2", width: 1.5, dash: [6, 3], label: "fore-line" });
      series.push({ type: "line", data: [[tx - 30, lineAt(fb, tx - 30)], [cur.tEnd, lineAt(fb, cur.tEnd)]], color: "s3", width: 1.5, dash: [6, 3], label: "after-line" });
      series.push({ type: "points", data: [[tx, Ta], [tx, Tb]], color: "s4", size: 4.5, label: "extrapolated to t = " + tx.toFixed(0) + " s" });
      if (tx !== tm) series.push({ type: "vline", x: tx, color: "s4", dash: [2, 3] });
      var dec = res < 0.005 ? 4 : 3;
      kvFill(Sim.$("#analysis"), [
        ["fore-line slope (drift)", (fa.b >= 0 ? "+" : "") + (fa.b * 60).toFixed(4) + " K/min, from " + pre.length + " readings"],
        ["after-line slope (drift)", (fb.b >= 0 ? "+" : "") + (fb.b * 60).toFixed(4) + " K/min, from " + post.length + " readings"],
        ["extrapolated to", tx.toFixed(0) + " s" + (tx !== tm ? " (63 % of the rise)" : " (mixing / firing)")],
        ["T before → after", Ta.toFixed(dec) + " → " + Tb.toFixed(dec) + " °C"],
        ["ΔT (extrapolated)", "<b>" + Sim.fmtU(dT, udT, "K") + "</b>"],
        ["ΔT from the extreme reading", dTx.toFixed(dec) + " K (" + (dTx >= 0 ? "highest" : "lowest") + " reading − last fore reading)"],
        ["difference", (100 * (dTx / dT - 1)).toFixed(2) + " %"]
      ]);
      result(out);
    } else {
      kvFill(Sim.$("#analysis"), [["status", cur.done ? "Need at least 2 readings before mixing and 2 after the after-line start." : "Run in progress…"]]);
      kvFill(Sim.$("#result"), []);
    }
    plot.draw(series, { xMin: 0, xMax: cur.tEnd, xPad: false });
    return out;
  }

  /* ---------------- results per experiment ---------------- */
  function result(a) {
    var rows = [], summary = "", p = cur.p;
    if (cur.mode === "calibration") {
      var fC = function (x) { return x[4] * CW * (x[2] - x[1]) / (x[1] - x[0]) - x[3] * CW; };
      var r1 = propagate(fC, [a.Ta, a.Tb, p.Th, p.mc, p.mh], [a.ua, a.ub, 0.05, 0.05, 0.05]);
      var postAll = cur.readings.filter(function (q) { return q[0] >= cur.tm; }).map(function (q) { return q[1]; });
      var rx = fC([a.Ta, S.max(postAll), p.Th, p.mc, p.mh]);
      rows = [
        ["C_cal = m_hot c (T_hot − T_f)/(T_f − T_cold) − m_cold c", "<b>" + Sim.fmtU(r1.y, r1.u, "J/K") + "</b>"],
        ["with T_f = highest reading instead", rx.toFixed(1) + " J/K"],
        ["model's true cup value", "30 J/K" + (p.loss ? " (the 0.5 K lost while pouring makes the fitted value too large)" : "")]
      ];
      lastCcal = { value: r1.y, u: r1.u };
      summary = "C_cal = " + Sim.fmtU(r1.y, r1.u, "J/K");
    } else if (cur.mode === "dissolution") {
      var Sx = SALTS[p.salt], Cc = v("s-ccal"), uC = lastCcal && Math.abs(lastCcal.value - Cc) < 0.05 ? lastCcal.u : 0;
      var fH = function (x) { return (x[1] * CW + x[2] * Sx.cs + x[3]) * (-x[0]) / (x[2] / Sx.M) / 1000; };
      var r2 = propagate(fH, [a.dT, p.mw, p.ms, Cc], [a.udT, 0.05, 0.005, uC]);
      var hx = fH([a.dTx, p.mw, p.ms, Cc]);
      var h0 = fH([a.dT, p.mw, p.ms, 0]);
      var dev = 100 * (r2.y / Sx.dH - 1);
      rows = [
        ["n(salt)", (p.ms / Sx.M).toFixed(5) + " mol"],
        ["q = (m_w c + m_s c_s + C_cal)(−ΔT)", ((p.mw * CW + p.ms * Sx.cs + Cc) * (-a.dT)).toFixed(0) + " J absorbed by the dissolving salt"],
        ["Δ_sol H (extrapolated ΔT)", "<b>" + Sim.fmtU(r2.y, r2.u, "kJ/mol") + "</b>"],
        ["Δ_sol H from the extreme reading", hx.toFixed(2) + " kJ/mol"],
        ["Δ_sol H ignoring the cup (C_cal = 0)", h0.toFixed(2) + " kJ/mol"],
        ["table (infinite dilution)", (Sx.dH > 0 ? "+" : "") + Sx.dH + " kJ/mol; yours is " + (dev >= 0 ? "+" : "") + dev.toFixed(1) + " %", Math.abs(dev) <= 5 ? "good" : "warn"]
      ];
      if (Cc === 0) rows.push(["warning", "C_cal is 0: calibrate the cup first", "warn"]);
      summary = Sx.name.split(",")[0] + ": " + Sim.fmtU(r2.y, r2.u, "kJ/mol");
    } else if (cur.mode === "neutralisation") {
      var Pp = PAIRS[p.pair], Cn = v("s-ccal"), mtot = 2 * p.vol;
      var fN = function (x) { return -(x[1] * CW + x[2]) * x[0] / x[3] / 1000; };
      var r3 = propagate(fN, [a.dT, mtot, Cn, p.n], [a.udT, 0.1, 2, p.n * 0.002]);
      var nx = fN([a.dTx, mtot, Cn, p.n]);
      var dev2 = 100 * (r3.y / -55.8 - 1);
      rows = [
        ["n (limiting)", p.n.toFixed(4) + " mol"],
        ["q = −(m c + C_cal) ΔT", (-(mtot * CW + Cn) * a.dT).toFixed(0) + " J (treating " + mtot.toFixed(1) + " g of solution as water)"],
        ["Δ_neut H (extrapolated ΔT)", "<b>" + Sim.fmtU(r3.y, r3.u, "kJ/mol") + "</b>"],
        ["Δ_neut H from the peak reading", nx.toFixed(2) + " kJ/mol"],
        ["vs −55.8 kJ/mol (H⁺ + OH⁻)", (dev2 >= 0 ? "+" : "") + dev2.toFixed(2) + " %" + (Math.abs(dev2) <= 2 ? " ✓ within 2 %" : ""), Math.abs(dev2) <= 2 ? "good" : "warn"]
      ];
      summary = Pp.name + ": " + Sim.fmtU(r3.y, r3.u, "kJ/mol");
    } else {
      var F = FUELS[p.fuel], useFuse = chk("s-fuse");
      if (p.fuel === "benzoic") {
        var fB = function (x) { return (x[1] * F.perGram * 1000 + (useFuse ? p.Efuse : 0)) / x[0] / 1000; };
        var r4 = propagate(fB, [a.dT, p.m], [a.udT, 0.00004]);
        var bx = fB([a.dTx, p.m]);
        bombCals.push(r4.y);
        rows = [
          ["pellet mass", p.m.toFixed(4) + " g"],
          ["fuse wire burned", p.Lfuse.toFixed(1) + " cm = " + p.Efuse.toFixed(0) + " J" + (useFuse ? " (included)" : " (ignored)")],
          ["C_cal = (m · 26.434 kJ/g + fuse) / ΔT", "<b>" + Sim.fmtU(r4.y, r4.u, "kJ/K") + "</b>"],
          ["with the raw maximum instead", bx.toFixed(4) + " kJ/K (" + (100 * (bx / r4.y - 1)).toFixed(2) + " %)"],
          ["calibrations so far", bombCals.map(function (c) { return c.toFixed(4); }).join(", ") + " kJ/K"]
        ];
        if (bombCals.length >= 2) {
          var d = 100 * Math.abs(bombCals[bombCals.length - 1] / bombCals[bombCals.length - 2] - 1);
          rows.push(["last two agree within", d.toFixed(2) + " %", d <= 0.5 ? "good" : "warn"]);
        }
        rows.push(["model's true C_cal", "10.885 kJ/K"]);
        Sim.$("#s-ccalb").value = S.mean(bombCals).toFixed(4);
        summary = "C_cal = " + Sim.fmtU(r4.y, r4.u, "kJ/K");
      } else {
        var Cb = v("s-ccalb");
        var uCb = bombCals.length >= 2 ? S.sd(bombCals) / Math.sqrt(bombCals.length) : Cb * 0.002;
        var fU = function (x) { return -((x[1] * x[0] * 1000 - (useFuse ? p.Efuse : 0)) / x[2]) * F.M / 1000; };
        var r5 = propagate(fU, [a.dT, Cb, p.m], [a.udT, uCb, 0.00004]);
        var qJ = Cb * a.dT * 1000 - (useFuse ? p.Efuse : 0);
        var dH = r5.y + F.dn * RT298;
        var ref = F.dU + F.dn * RT298;
        rows = [
          ["sample", F.name + ", M = " + F.M + " g/mol"],
          ["pellet mass", p.m.toFixed(4) + " g"],
          ["q released = C_cal ΔT − fuse", (qJ / 1000).toFixed(3) + " kJ = " + (qJ / 1000 / p.m).toFixed(3) + " kJ/g"],
          ["Δ_c U", "<b>" + Sim.fmtU(r5.y, r5.u, "kJ/mol") + "</b>"],
          ["balanced equation", F.eq + " (Δn_gas = " + F.dn + ")"],
          ["Δ_c H = Δ_c U + Δn_gas RT", Sim.fmtU(dH, r5.u, "kJ/mol")],
          ["NIST Δ_c H", ref.toFixed(1) + " kJ/mol; yours " + (100 * (dH / ref - 1)).toFixed(2) + " %"]
        ];
        if (Cb === 0) rows.push(["warning", "C_cal is 0: run a benzoic acid calibration first", "warn"]);
        summary = F.name.split(",")[0] + ": ΔcU = " + Sim.fmtU(r5.y, r5.u, "kJ/mol");
      }
    }
    kvFill(Sim.$("#result"), rows);
    cur.summary = summary;
    cur.analysis = a;
  }

  /* ---------------- running a experiment ---------------- */
  var NAMES = { calibration: "cup calibration", dissolution: "dissolution", neutralisation: "neutralisation", bomb: "bomb" };

  function startRun() {
    if (anim) anim.stop();
    cur = simulate();
    cur.shown = 0; cur.done = false; cur.id = runs.length + 1;
    var full = cur.readings;
    cur.readings = [];
    var clock = 0;
    anim = Sim.loop(function (dt) {
      clock += dt * 30;
      while (cur.shown < full.length && full[cur.shown][0] <= clock) { cur.readings.push(full[cur.shown]); cur.shown++; }
      liveInfo(clock);
      if (cur.shown >= full.length) { finish(full); return false; }
      analyse();
      return true;
    });
    cur.full = full;
    analyse();
  }

  function finish(full) {
    if (!cur || cur.done) return;
    if (anim) anim.stop();
    cur.readings = full; cur.done = true;
    liveInfo(cur.tEnd);
    analyse();
    if (cur.analysis) {
      runs.push({ id: cur.id, mode: cur.mode, dT: cur.analysis.dT, udT: cur.analysis.udT, dTx: cur.analysis.dTx, summary: cur.summary, readings: full });
      renderRuns();
    }
  }

  function liveInfo(clock) {
    var last = cur.readings.length ? cur.readings[cur.readings.length - 1] : null;
    kvFill(Sim.$("#live"), [
      ["experiment", NAMES[cur.mode] + " (run " + cur.id + ")"],
      ["clock", Math.min(clock, cur.tEnd).toFixed(0) + " s"],
      ["last reading", last ? last[1].toFixed(cur.res < 0.005 ? 3 : cur.res < 0.05 ? 2 : 1) + " °C" : "—"],
      ["status", cur.done ? "finished" : clock < cur.tm ? "fore-period" : "after " + (cur.mode === "bomb" ? "firing" : "mixing")]
    ]);
  }

  function renderRuns() {
    var tb = Sim.$("#runs tbody");
    tb.textContent = "";
    runs.forEach(function (r) {
      tb.appendChild(Sim.el("tr", {}, Sim.el("td", { text: String(r.id) }), Sim.el("td", { text: NAMES[r.mode] }),
        Sim.el("td", { text: Sim.fmtU(r.dT, r.udT) }), Sim.el("td", { text: r.dTx.toFixed(4) }), Sim.el("td", { text: r.summary })));
    });
  }

  Sim.$("#run").addEventListener("click", startRun);
  Sim.$("#skip").addEventListener("click", function () { if (cur && !cur.done) finish(cur.full); });
  Sim.$("#rerun").addEventListener("click", function () { seed = Sim.newSeed(seed); Sim.$("#seed").textContent = String(seed); unknownKey = Sim.rng(seed + 5).random() < 0.5 ? "sucrose" : "naphthalene"; if (mode === "bomb") buildSetup(); startRun(); });
  ["#a-skip", "#a-to"].forEach(function (s) { Sim.$(s).addEventListener("change", function () { if (cur && cur.done) { reanalyseOnly(); } }); });

  function reanalyseOnly() {
    // re-fitting must not add another bomb calibration to the list
    if (cur.mode === "bomb" && cur.p.fuel === "benzoic" && bombCals.length) bombCals.pop();
    analyse();
    var last = runs[runs.length - 1];
    if (last && last.id === cur.id && cur.analysis) { last.dT = cur.analysis.dT; last.udT = cur.analysis.udT; last.dTx = cur.analysis.dTx; last.summary = cur.summary; renderRuns(); }
  }

  Sim.exportCSV(Sim.$("#x-run"), "calorimetry_run.csv", function () {
    if (!cur || !cur.done) return null;
    return { header: ["time_s", "T_C"], rows: cur.readings.map(function (q) { return [q[0], q[1]]; }), filename: "calorimetry_run" + cur.id + "_" + cur.mode + ".csv" };
  });
  Sim.exportCSV(Sim.$("#x-all"), "calorimetry_runs.csv", function () {
    return { header: ["run", "experiment", "dT_extrapolated_K", "u_dT_K", "dT_extreme_K", "result"], rows: runs.map(function (r) { return [r.id, r.mode, +r.dT.toFixed(5), +r.udT.toFixed(5), +r.dTx.toFixed(5), r.summary]; }) };
  });

  var tabs = Sim.tabs(Sim.$("#tabs"), function (name) {
    if (anim) anim.stop();
    mode = name;
    cur = null;
    buildSetup();
    setTiming();
    kvFill(Sim.$("#analysis"), [["status", "Set up the experiment and press Start the run."]]);
    kvFill(Sim.$("#result"), []);
    kvFill(Sim.$("#live"), []);
    plot.draw([], { xMin: 0, xMax: v("t-end"), xPad: false, yMin: mode === "bomb" ? 24 : 18, yMax: mode === "bomb" ? 28 : 30 });
  });
  tabs.select(mode);
})();
