/* gas-laws simulation: ideal gas (Boyle, work of compression), van der Waals real gas
 * (Z, isotherms, Maxwell construction), a 3D hard-sphere kinetic box, and a
 * Clement-Desormes bench for gamma. Uses ../common/sim.js (global Sim).
 *
 * Data and sources:
 *  - R, kB: CODATA 2022 exact (NIST). Atomic masses: IUPAC standard atomic weights.
 *  - van der Waals a (L^2 bar mol^-2) and b (L mol^-1): CRC Handbook of Chemistry and
 *    Physics table, as reproduced in Atkins' Physical Chemistry.
 *  - Experimental critical constants for comparison: NIST Chemistry WebBook
 *    (CO2: Tc = 304.13 K, pc = 73.80 bar).
 *  - Hard-sphere diameters: kinetic (collision) diameters, e.g. Ar 0.340 nm, He 0.260 nm.
 *  - Heat-capacity ratios: dry air 1.401, Ar 1.667, CO2 1.289 near 293 K (NIST WebBook Cp/Cv).
 */
(function () {
  "use strict";
  var C = Sim.C, S = Sim.stats;
  var RL = 0.08314462618;   // L bar mol^-1 K^-1

  var PRESETS = {
    ideal: {
      title: "Ideal gas", tab: "ideal",
      what: "For an ideal gas pV = nRT. At fixed n and T, p is proportional to 1/V (Boyle's law), so a plot of p against 1/V is a straight line through the origin with slope nRT. The second panel compares the work of a slow (reversible) and a sudden compression between the same two states.",
      task: "Keep n and T fixed and set five volumes; record the pressure each time. Read the slope of p against 1/V and get R back. Then double T at fixed V and check that p doubles. Optional: compress the gas slowly and suddenly and compare the work.",
      target: "A straight line through the origin with slope nRT, and R within 2 % of 8.314 J mol⁻¹ K⁻¹."
    },
    real: {
      title: "Real gas (van der Waals)", tab: "real",
      what: "Real molecules attract each other and take up space. The van der Waals equation, (p + a/V<sub>m</sub>²)(V<sub>m</sub> − b) = RT, captures both. The compression factor Z = pV<sub>m</sub>/RT shows which wins. Below the critical temperature the model's isotherms have a loop; the Maxwell equal-area line replaces it with the two-phase plateau.",
      task: "Choose CO₂ at 320 K and plot Z from 1 to 150 bar; find the pressure where Z is smallest (use the probe). Switch to helium at the same T. Then plot CO₂ isotherms at 280, 300, 304 and 320 K, read the vapour pressure on each flat part, and compare the model's critical pressure with NIST's 73.80 bar.",
      target: "A CO₂ minimum near 100 bar with Z well below 0.5; helium Z slightly above 1 everywhere; the flat part shrinks to a point at about 304 K."
    },
    kinetic: {
      title: "Kinetic theory in a box", tab: "kinetic",
      what: "A gas is a crowd of atoms. Pressure is the momentum they deliver to the walls, and temperature is their average kinetic energy: ½M⟨v²⟩ = 3/2 RT. Collisions spread the speeds into the Maxwell–Boltzmann distribution. The Clément–Desormes tab measures γ = C<sub>p</sub>/C<sub>V</sub> of air.",
      task: "Argon at 300 K: let the histogram settle, read p and the rms speed (theory 433 m/s). Double T to 600 K (predict 612 m/s and double p), then switch to helium at 300 K (speeds ×3.16, same p). Export 3000 speeds. On the Clément–Desormes tab run 8 trials with a 1 s opening and one each with 0.2 s and 5 s.",
      target: "The histogram matches the Maxwell–Boltzmann curve; the 1 s trials give γ between about 1.38 and 1.43, and the 5 s opening a clearly lower γ."
    }
  };

  var preset = Sim.preset(PRESETS, "ideal");
  var seed = Sim.seedFromQuery(17);
  var rng = Sim.rng(seed);

  Sim.label();
  Sim.presetBox(Sim.$("#preset"), preset);

  /* ======================= IDEAL ======================= */
  var ideal = { readings: [], shown: NaN };
  var iPlot = Sim.plot(Sim.$("#i-plot"), { xLabel: "1/V / L⁻¹", yLabel: "p / kPa", xMin: 0, yMin: 0 });
  var wPlot = Sim.plot(Sim.$("#w-plot"), { xLabel: "V / L", yLabel: "p / kPa", yMin: 0 });

  function iVals() {
    return { n: parseFloat(Sim.$("#i-n").value), T: parseFloat(Sim.$("#i-T").value), V: parseFloat(Sim.$("#i-V").value) };
  }

  function idealRead() {
    var v = iVals();
    Sim.$("#i-V-out").textContent = v.V.toFixed(3);
    if (!(v.n > 0 && v.T > 0 && v.V > 0)) { Sim.$("#i-p").textContent = "—"; return; }
    var p = v.n * C.R * v.T / v.V;      // J/L = kPa
    var reading = Math.round(p * (1 + rng.normal(0, 0.002)) * 100) / 100;
    ideal.shown = reading;
    Sim.$("#i-p").textContent = reading.toFixed(2) + " kPa";
    drawCylinder(v);
  }

  function drawCylinder(v) {
    var cv = Sim.$("#i-cyl"), dpr = window.devicePixelRatio || 1, W = cv.clientWidth || 300, H = cv.clientHeight || 200;
    cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
    var ctx = cv.getContext("2d");
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.fillStyle = Sim.color("plot-bg"); ctx.fillRect(0, 0, W, H);
    var x0 = 20, x1 = W - 20, y0 = 30, y1 = H - 20;
    var frac = Math.min(1, v.V / 10);
    var px = x0 + (x1 - x0) * frac;
    ctx.strokeStyle = Sim.color("muted"); ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(x1, y0); ctx.lineTo(x0, y0); ctx.lineTo(x0, y1); ctx.lineTo(x1, y1); ctx.stroke();
    ctx.fillStyle = Sim.color("s5"); ctx.fillRect(px, y0 + 2, 10, y1 - y0 - 4);
    ctx.fillRect(px + 10, (y0 + y1) / 2 - 3, x1 - px, 6);
    var r = Sim.rng(Math.round(v.n * 1000) + 7), N = Math.min(250, Math.round(v.n * 600) + 5);
    var hot = Math.min(1, v.T / 1000);
    ctx.fillStyle = "rgb(" + Math.round(60 + 190 * hot) + "," + Math.round(110 - 40 * hot) + "," + Math.round(200 - 150 * hot) + ")";
    for (var i = 0; i < N; i++) {
      ctx.beginPath();
      ctx.arc(x0 + 5 + r.random() * (px - x0 - 10), y0 + 5 + r.random() * (y1 - y0 - 10), 2, 0, 2 * Math.PI);
      ctx.fill();
    }
    ctx.fillStyle = Sim.color("ink"); ctx.font = "12px " + getComputedStyle(document.body).fontFamily;
    ctx.fillText("V = " + v.V.toFixed(2) + " L, T = " + v.T + " K, n = " + v.n + " mol", x0, 18);
  }

  function idealRecord() {
    var v = iVals();
    if (!isFinite(ideal.shown)) return;
    ideal.readings.push({ n: v.n, T: v.T, V: v.V, p: ideal.shown });
    idealRead();
    renderIdeal();
  }

  function renderIdeal() {
    var tb = Sim.$("#i-table tbody");
    tb.textContent = "";
    ideal.readings.forEach(function (r, i) {
      tb.appendChild(Sim.el("tr", {}, Sim.el("td", { text: String(i + 1) }), Sim.el("td", { text: String(r.n) }), Sim.el("td", { text: String(r.T) }),
        Sim.el("td", { text: r.V.toFixed(3) }), Sim.el("td", { text: (1 / r.V).toFixed(4) }), Sim.el("td", { text: r.p.toFixed(2) })));
    });
    // group readings by (n, T)
    var groups = {}, order = [];
    ideal.readings.forEach(function (r) {
      var k = r.n + "|" + r.T;
      if (!groups[k]) { groups[k] = []; order.push(k); }
      groups[k].push(r);
    });
    var series = [], fit = Sim.$("#i-fit");
    fit.textContent = "";
    order.forEach(function (k, gi) {
      var g = groups[k], col = "s" + ((gi % 6) + 1);
      series.push({ type: "points", data: g.map(function (r) { return [1 / r.V, r.p]; }), color: col, label: "n = " + g[0].n + " mol, T = " + g[0].T + " K" });
      if (g.length >= 2) {
        var f = S.linfitThrough0(g.map(function (r) { return 1 / r.V; }), g.map(function (r) { return r.p; }));
        var xmax = S.max(g.map(function (r) { return 1 / r.V; })) * 1.05;
        series.push({ type: "line", data: [[0, 0], [xmax, f.b * xmax]], color: col, width: 1.5, dash: [5, 3] });
        var R = f.b / (g[0].n * g[0].T), uR = f.ub / (g[0].n * g[0].T);
        var dev = 100 * (R / C.R - 1);
        [["n = " + g[0].n + ", T = " + g[0].T + " K", g.length + " readings"],
          ["slope nRT", Sim.fmtU(f.b, f.ub, "kPa L (= J)")],
          ["R = slope/(nT)", Sim.fmtU(R, uR, "J mol⁻¹ K⁻¹")],
          ["vs 8.314462618", (dev >= 0 ? "+" : "") + dev.toFixed(2) + " %" + (Math.abs(dev) <= 2 ? " ✓" : "")]].forEach(function (row) {
          fit.appendChild(Sim.el("span", { text: row[0] })); fit.appendChild(Sim.el("span", { text: row[1] }));
        });
      }
    });
    iPlot.draw(series);
  }

  ["#i-n", "#i-T", "#i-V"].forEach(function (s) { Sim.$(s).addEventListener("input", idealRead); });
  Sim.$("#i-rec").addEventListener("click", idealRecord);
  Sim.$("#i-clear").addEventListener("click", function () { ideal.readings = []; renderIdeal(); });

  function workProcess(kind) {
    var v = iVals(), V1 = v.V, V2 = parseFloat(Sim.$("#w-V2").value), gamma = parseFloat(Sim.$("#w-gas").value);
    if (!(V2 > 0) || !(v.n > 0) || !(v.T > 0)) return;
    var nR = v.n * C.R, p1 = nR * v.T / V1, Cv = C.R / (gamma - 1);
    var w, q, dU, T2, p2, path = [], ext = [], iso = [];
    var N = 120;
    for (var i = 0; i <= N; i++) { var V = Math.min(V1, V2) * 0.85 + (Math.max(V1, V2) * 1.1 - Math.min(V1, V2) * 0.85) * i / N; iso.push([V, nR * v.T / V]); }
    if (kind === "rev") {
      T2 = v.T; p2 = nR * T2 / V2;
      w = -nR * v.T * Math.log(V2 / V1); q = -w; dU = 0;
      for (var j = 0; j <= N; j++) { var Vj = V1 + (V2 - V1) * j / N; path.push([Vj, nR * v.T / Vj]); }
      ext = path;
    } else if (kind === "one") {
      T2 = v.T; p2 = nR * T2 / V2;
      w = -p2 * (V2 - V1); q = -w; dU = 0;
      ext = [[V1, p2], [V2, p2]];
      path = [];   // the gas is not in equilibrium on the way: only the two end states are defined
    } else {
      T2 = v.T * Math.pow(V1 / V2, gamma - 1); p2 = nR * T2 / V2;
      dU = v.n * Cv * (T2 - v.T); w = dU; q = 0;
      for (var k = 0; k <= N; k++) { var Vk = V1 + (V2 - V1) * k / N; path.push([Vk, p1 * Math.pow(V1 / Vk, gamma)]); }
      ext = path;
    }
    var name = kind === "rev" ? "reversible isothermal" : kind === "one" ? "one step against p_ext = " + p2.toFixed(1) + " kPa, then back to T" : "reversible adiabatic";
    var out = Sim.$("#w-out");
    out.textContent = "";
    [["process", name], ["V₁ → V₂", V1.toFixed(3) + " → " + V2.toFixed(3) + " L"], ["p₁ → p₂", p1.toFixed(1) + " → " + p2.toFixed(1) + " kPa"],
      ["T₂", T2.toFixed(2) + " K"], ["w (on the gas)", (w >= 0 ? "+" : "") + w.toFixed(1) + " J"], ["q", (q >= 0 ? "+" : "") + q.toFixed(1) + " J"],
      ["ΔU = q + w", (dU >= 0 ? "+" : "") + dU.toFixed(1) + " J"],
      ["reversible isothermal w for comparison", (-nR * v.T * Math.log(V2 / V1)).toFixed(1) + " J"]].forEach(function (r) {
      out.appendChild(Sim.el("span", { text: r[0] })); out.appendChild(Sim.el("span", { text: r[1] }));
    });
    wPlot.draw([
      { type: "line", data: iso, color: "muted", width: 1, dash: [4, 4], label: "isotherm at T₁" },
      { type: "area", data: ext, color: "s1", alpha: 0.18, label: "p_ext path (area = |w|)" },
      { type: "line", data: path, color: "s2", label: "state of the gas" },
      { type: "points", data: [[V1, p1], [V2, p2]], color: "s2", size: 4 }
    ]);
  }
  Sim.$("#w-rev").addEventListener("click", function () { workProcess("rev"); });
  Sim.$("#w-one").addEventListener("click", function () { workProcess("one"); });
  Sim.$("#w-adi").addEventListener("click", function () { workProcess("adi"); });

  /* ======================= REAL GAS ======================= */
  var GASES = {
    CO2: { name: "carbon dioxide, CO₂", a: 3.640, b: 0.04267, Tc: 304.13, pc: 73.80 },
    He: { name: "helium, He", a: 0.0346, b: 0.0238, Tc: 5.19, pc: 2.27 },
    Ne: { name: "neon, Ne", a: 0.208, b: 0.01672, Tc: 44.4, pc: 27.6 },
    Ar: { name: "argon, Ar", a: 1.355, b: 0.03201, Tc: 150.7, pc: 48.6 },
    H2: { name: "hydrogen, H₂", a: 0.2476, b: 0.02661, Tc: 33.2, pc: 13.0 },
    N2: { name: "nitrogen, N₂", a: 1.370, b: 0.0387, Tc: 126.2, pc: 34.0 },
    O2: { name: "oxygen, O₂", a: 1.382, b: 0.03186, Tc: 154.6, pc: 50.4 },
    CH4: { name: "methane, CH₄", a: 2.303, b: 0.04310, Tc: 190.6, pc: 46.0 },
    NH3: { name: "ammonia, NH₃", a: 4.225, b: 0.0371, Tc: 405.4, pc: 113.3 },
    H2O: { name: "water, H₂O", a: 5.537, b: 0.03049, Tc: 647.1, pc: 220.6 }
  };
  var real = { zCurves: [], isos: [] };
  var gasSel = Sim.$("#r-gas");
  Object.keys(GASES).forEach(function (k) { gasSel.appendChild(Sim.el("option", { value: k, text: GASES[k].name })); });
  gasSel.value = "CO2";
  var zPlot = Sim.plot(Sim.$("#r-zplot"), { xLabel: "p / bar", yLabel: "Z", xMin: 0 });
  var isoPlot = Sim.plot(Sim.$("#r-iso"), { xLabel: "Vm / L mol⁻¹ (log scale)", yLabel: "p / bar", logX: true, yMin: 0 });

  function vdwP(V, T, g) { return RL * T / (V - g.b) - g.a / (V * V); }

  function cubicRoots(p, T, g) {
    var A = -(g.b + RL * T / p), B = g.a / p, Cc = -g.a * g.b / p;
    var P = B - A * A / 3, Q = 2 * A * A * A / 27 - A * B / 3 + Cc;
    var disc = Q * Q / 4 + P * P * P / 27, roots = [];
    if (disc > 0) {
      var sq = Math.sqrt(disc);
      roots.push(Math.cbrt(-Q / 2 + sq) + Math.cbrt(-Q / 2 - sq) - A / 3);
    } else {
      var m = 2 * Math.sqrt(-P / 3), th = Math.acos(Math.max(-1, Math.min(1, 3 * Q / (P * m)))) / 3;
      for (var k = 0; k < 3; k++) roots.push(m * Math.cos(th - 2 * Math.PI * k / 3) - A / 3);
    }
    return roots.filter(function (v) { return v > g.b * (1 + 1e-9); }).sort(function (x, y) { return x - y; });
  }

  function vdwCrit(g) { return { Tc: 8 * g.a / (27 * RL * g.b), pc: g.a / (27 * g.b * g.b), Vc: 3 * g.b }; }

  // Maxwell equal-area construction: vapour pressure and coexisting molar volumes
  var satCache = {};
  function saturation(T, g, key) {
    var ck = key + "|" + T;
    if (satCache[ck] !== undefined) return satCache[ck];
    var res = null;
    if (T < vdwCrit(g).Tc) {
      // spinodal points: dp/dV = 0  <=>  RT V^3 = 2a (V - b)^2
      var f = function (V) { return RL * T * V * V * V - 2 * g.a * (V - g.b) * (V - g.b); };
      var sp = [], prev = g.b * 1.000001, fp = f(prev);
      for (var i = 1; i <= 4000; i++) {
        var V = g.b * Math.pow(60, i / 4000) * 1.000001, fv = f(V);
        if (fp * fv < 0) {
          var lo = prev, hi = V;
          for (var k = 0; k < 80; k++) { var mid = (lo + hi) / 2; if (f(lo) * f(mid) <= 0) hi = mid; else lo = mid; }
          sp.push((lo + hi) / 2);
        }
        prev = V; fp = fv;
      }
      if (sp.length >= 2) {
        var pLo = Math.max(1e-9, vdwP(sp[0], T, g)), pHi = vdwP(sp[1], T, g);
        var area = function (p) {
          var r = cubicRoots(p, T, g);
          if (r.length < 3) return NaN;
          var Vl = r[0], Vg = r[r.length - 1];
          return { F: RL * T * Math.log((Vg - g.b) / (Vl - g.b)) - g.a * (1 / Vl - 1 / Vg) - p * (Vg - Vl), Vl: Vl, Vg: Vg };
        };
        var lo2 = pLo * (1 + 1e-9), hi2 = pHi * (1 - 1e-9), out = null;
        for (var j = 0; j < 100; j++) {
          var pm = (lo2 + hi2) / 2, a2 = area(pm);
          if (!a2 || !isFinite(a2.F)) break;
          out = { p: pm, Vl: a2.Vl, Vg: a2.Vg };
          if (a2.F > 0) lo2 = pm; else hi2 = pm;
        }
        res = out;
      }
    }
    satCache[ck] = res;
    return res;
  }

  function stableVm(p, T, g, key) {
    var r = cubicRoots(p, T, g);
    if (r.length === 1) return { V: r[0], phase: T >= vdwCrit(g).Tc ? "supercritical / gas" : (r[0] < vdwCrit(g).Vc ? "liquid" : "gas"), n: 1 };
    var sat = saturation(T, g, key);
    if (sat && p > sat.p) return { V: r[0], phase: "liquid", n: r.length };
    return { V: r[r.length - 1], phase: "gas", n: r.length };
  }

  function realVals() { return { key: gasSel.value, g: GASES[gasSel.value], T: parseFloat(Sim.$("#r-T").value), pmax: parseFloat(Sim.$("#r-pmax").value) }; }

  function renderConsts() {
    var v = realVals(), c = vdwCrit(v.g), el = Sim.$("#r-consts");
    el.textContent = "";
    [["a", v.g.a + " L² bar mol⁻²"], ["b", v.g.b + " L mol⁻¹"],
      ["van der Waals T_c = 8a/27Rb", c.Tc.toFixed(2) + " K"], ["van der Waals p_c = a/27b²", c.pc.toFixed(2) + " bar"], ["van der Waals V_c = 3b", c.Vc.toFixed(4) + " L mol⁻¹"],
      ["NIST T_c, p_c", v.g.Tc + " K, " + v.g.pc.toFixed(2) + " bar"]].forEach(function (r) {
      el.appendChild(Sim.el("span", { text: r[0] })); el.appendChild(Sim.el("span", { text: r[1] }));
    });
    var slider = Sim.$("#r-p");
    slider.max = String(v.pmax);
    probe();
  }

  function probe() {
    var v = realVals(), p = parseFloat(Sim.$("#r-p").value), el = Sim.$("#r-probe");
    Sim.$("#r-p-out").textContent = String(p);
    el.textContent = "";
    if (!(v.T > 0)) return;
    var s = stableVm(p, v.T, v.g, v.key), Z = p * s.V / (RL * v.T), sat = saturation(v.T, v.g, v.key);
    [["gas, T", v.g.name + ", " + v.T + " K"], ["V_m (van der Waals)", s.V.toFixed(4) + " L mol⁻¹"], ["V_m (ideal) = RT/p", (RL * v.T / p).toFixed(4) + " L mol⁻¹"],
      ["Z = pV_m/RT", Z.toFixed(4)], ["phase in the model", s.phase],
      ["vapour pressure at this T", sat ? sat.p.toFixed(2) + " bar" : "none (T ≥ T_c)"]].forEach(function (r) {
      el.appendChild(Sim.el("span", { text: r[0] })); el.appendChild(Sim.el("span", { text: r[1] }));
    });
  }

  function addZ() {
    var v = realVals();
    if (!(v.T > 0) || !(v.pmax > 1)) return;
    var data = [];
    for (var p = 1; p <= v.pmax + 1e-9; p += Math.max(0.25, v.pmax / 600)) {
      var s = stableVm(p, v.T, v.g, v.key);
      data.push([p, p * s.V / (RL * v.T)]);
    }
    real.zCurves.push({ key: v.key, T: v.T, data: data });
    drawReal();
  }

  function addIso() {
    var v = realVals();
    if (!(v.T > 0)) return;
    var loop = [], stable = [], sat = saturation(v.T, v.g, v.key);
    var Vmin = v.g.b * 1.03, Vmax = Math.max(3, 60 * v.g.b);
    for (var i = 0; i <= 500; i++) {
      var V = Vmin * Math.pow(Vmax / Vmin, i / 500), p = vdwP(V, v.T, v.g);
      if (sat && V > sat.Vl && V < sat.Vg) { loop.push([V, p]); stable.push([V, sat.p]); }
      else { stable.push([V, p]); loop.push([V, NaN]); }
    }
    real.isos.push({ key: v.key, T: v.T, loop: loop, stable: stable, sat: sat });
    drawReal();
  }

  function drawReal() {
    var zs = [{ type: "hline", y: 1, color: "muted", dash: [4, 4], label: "ideal, Z = 1" }];
    real.zCurves.forEach(function (c, i) { zs.push({ type: "line", data: c.data, color: "s" + ((i % 6) + 1), label: c.key + ", " + c.T + " K" }); });
    zPlot.draw(zs);
    var is = [], tb = Sim.$("#r-isotable tbody"), ymax = 10;
    tb.textContent = "";
    real.isos.forEach(function (c, i) {
      var col = "s" + ((i % 6) + 1);
      ymax = Math.max(ymax, 1.6 * vdwCrit(GASES[c.key]).pc);
      is.push({ type: "line", data: c.stable, color: col, label: c.key + ", " + c.T + " K" });
      if (c.sat) is.push({ type: "line", data: c.loop, color: col, dash: [4, 4], width: 1 });
      tb.appendChild(Sim.el("tr", {}, Sim.el("td", { text: c.key + " " + c.T }),
        Sim.el("td", { text: c.sat ? c.sat.p.toFixed(2) : "— (T ≥ T_c)" }),
        Sim.el("td", { text: c.sat ? c.sat.Vl.toFixed(4) : "—" }), Sim.el("td", { text: c.sat ? c.sat.Vg.toFixed(4) : "—" })));
    });
    isoPlot.draw(is, { yMax: ymax, xMin: 0.02, xMax: 3 });
  }

  gasSel.addEventListener("change", renderConsts);
  Sim.$("#r-T").addEventListener("input", probe);
  Sim.$("#r-pmax").addEventListener("change", renderConsts);
  Sim.$("#r-p").addEventListener("input", probe);
  Sim.$("#r-addZ").addEventListener("click", addZ);
  Sim.$("#r-addIso").addEventListener("click", addIso);
  Sim.$("#r-clear").addEventListener("click", function () { real.zCurves = []; real.isos = []; drawReal(); });

  /* ======================= KINETIC BOX ======================= */
  // Units inside the box: nm, ps, nm/ps (1 nm/ps = 1000 m/s).
  var KGASES = {
    Ar: { name: "argon", M: 39.948, sigma: 0.340 },
    He: { name: "helium", M: 4.0026, sigma: 0.260 },
    Ne: { name: "neon", M: 20.180, sigma: 0.275 },
    Kr: { name: "krypton", M: 83.798, sigma: 0.360 },
    Xe: { name: "xenon", M: 131.29, sigma: 0.396 },
    N2: { name: "nitrogen (as a sphere)", M: 28.014, sigma: 0.364 }
  };
  var kSel = Sim.$("#k-gas");
  Object.keys(KGASES).forEach(function (k) { kSel.appendChild(Sim.el("option", { value: k, text: KGASES[k].name })); });
  var K = null, kRunning = true, kLoop = null, kHistAcc = [];
  var boxCanvas = Sim.$("#k-box");
  var hPlot = Sim.plot(Sim.$("#k-hist"), { xLabel: "speed / m s⁻¹", yLabel: "probability density / (m/s)⁻¹", xMin: 0, yMin: 0 });

  function kT() { return parseFloat(Sim.$("#k-T").value); }

  function kReset() {
    var g = KGASES[kSel.value], N = parseInt(Sim.$("#k-N").value, 10), L = parseFloat(Sim.$("#k-L").value), T = kT();
    var r = Sim.rng(seed + 101);
    var m = g.M * 1e-3 / C.NA;                       // kg per atom
    var vScale = Math.sqrt(3 * C.kB * T / m) / 1000;  // nm/ps
    var pos = new Float64Array(3 * N), vel = new Float64Array(3 * N), s = g.sigma, rad = s / 2;
    var placed = 0, tries = 0;
    while (placed < N && tries < N * 200) {
      tries++;
      var x = rad + r.random() * (L - s), y = rad + r.random() * (L - s), z = rad + r.random() * (L - s), ok = true;
      for (var j = Math.max(0, placed - 400); j < placed && ok; j++) {
        var dx = pos[3 * j] - x, dy = pos[3 * j + 1] - y, dz = pos[3 * j + 2] - z;
        if (dx * dx + dy * dy + dz * dz < s * s * 1.2) ok = false;
      }
      if (!ok) continue;
      pos[3 * placed] = x; pos[3 * placed + 1] = y; pos[3 * placed + 2] = z;
      // all atoms start at the same speed, in random directions
      var u = 2 * r.random() - 1, ph = 2 * Math.PI * r.random(), st = Math.sqrt(1 - u * u);
      vel[3 * placed] = vScale * st * Math.cos(ph); vel[3 * placed + 1] = vScale * st * Math.sin(ph); vel[3 * placed + 2] = vScale * u;
      placed++;
    }
    K = { g: g, m: m, N: placed, L: L, s: s, pos: pos, vel: vel, t: 0, r: r, imp: [], impSum: 0, impT: 0 };
    kHistAcc = [];
    kSetDt();
  }

  function kSetDt() {
    var Tm = Math.max(kT(), kineticT() || 0);
    var vrms = Math.sqrt(3 * C.kB * Tm / K.m) / 1000;
    K.dt = 0.12 * K.s / (3 * vrms);
  }

  function kineticT() {
    if (!K) return NaN;
    var s2 = 0;
    for (var i = 0; i < 3 * K.N; i++) s2 += K.vel[i] * K.vel[i];
    var v2 = s2 / K.N * 1e6;                        // m^2/s^2
    return K.m * v2 / (3 * C.kB);
  }

  function kStep() {
    var N = K.N, L = K.L, s = K.s, rad = s / 2, dt = K.dt, pos = K.pos, vel = K.vel, r = K.r;
    var thermal = Sim.$("#k-thermal").checked, T = kT();
    var sdv = Math.sqrt(C.kB * T / K.m) / 1000;     // nm/ps
    var imp = 0;                                    // sum of |dv| at walls, nm/ps
    for (var i = 0; i < N; i++) {
      for (var a = 0; a < 3; a++) {
        var k = 3 * i + a;
        pos[k] += vel[k] * dt;
        var hitLo = pos[k] < rad, hitHi = pos[k] > L - rad;
        if (hitLo || hitHi) {
          var vin = Math.abs(vel[k]), vout;
          if (thermal) {
            var U = r.random();
            vout = sdv * Math.sqrt(-2 * Math.log(U > 1e-300 ? U : 1e-300));
            // the tangential components are re-drawn too (diffuse wall)
            for (var b = 0; b < 3; b++) if (b !== a) vel[3 * i + b] = r.normal(0, sdv);
          } else vout = vin;
          vel[k] = hitLo ? vout : -vout;
          pos[k] = hitLo ? 2 * rad - pos[k] : 2 * (L - rad) - pos[k];
          imp += vin + vout;
        }
      }
    }
    // collisions: linked-cell list
    var nc = Math.max(1, Math.min(48, Math.floor(L / s))), cs = L / nc;
    var head = K.head && K.head.length === nc * nc * nc ? K.head : (K.head = new Int32Array(nc * nc * nc));
    var next = K.next && K.next.length === N ? K.next : (K.next = new Int32Array(N));
    head.fill(-1);
    for (var p = 0; p < N; p++) {
      var cx = Math.min(nc - 1, Math.max(0, Math.floor(pos[3 * p] / cs))), cy = Math.min(nc - 1, Math.max(0, Math.floor(pos[3 * p + 1] / cs))), cz = Math.min(nc - 1, Math.max(0, Math.floor(pos[3 * p + 2] / cs)));
      var c = (cx * nc + cy) * nc + cz;
      next[p] = head[c]; head[c] = p;
    }
    var s2 = s * s;
    for (var q = 0; q < N; q++) {
      var qx = pos[3 * q], qy = pos[3 * q + 1], qz = pos[3 * q + 2];
      var ix = Math.min(nc - 1, Math.max(0, Math.floor(qx / cs))), iy = Math.min(nc - 1, Math.max(0, Math.floor(qy / cs))), iz = Math.min(nc - 1, Math.max(0, Math.floor(qz / cs)));
      for (var ax = ix - 1; ax <= ix + 1; ax++) {
        if (ax < 0 || ax >= nc) continue;
        for (var ay = iy - 1; ay <= iy + 1; ay++) {
          if (ay < 0 || ay >= nc) continue;
          for (var az = iz - 1; az <= iz + 1; az++) {
            if (az < 0 || az >= nc) continue;
            for (var o = head[(ax * nc + ay) * nc + az]; o >= 0; o = next[o]) {
              if (o <= q) continue;
              var dx = qx - pos[3 * o], dy = qy - pos[3 * o + 1], dz = qz - pos[3 * o + 2];
              var d2 = dx * dx + dy * dy + dz * dz;
              if (d2 >= s2 || d2 === 0) continue;
              var dvx = vel[3 * q] - vel[3 * o], dvy = vel[3 * q + 1] - vel[3 * o + 1], dvz = vel[3 * q + 2] - vel[3 * o + 2];
              var dot = dvx * dx + dvy * dy + dvz * dz;
              if (dot >= 0) continue;                // already separating
              var f = dot / d2;                       // equal masses: swap the normal components
              vel[3 * q] -= f * dx; vel[3 * q + 1] -= f * dy; vel[3 * q + 2] -= f * dz;
              vel[3 * o] += f * dx; vel[3 * o + 1] += f * dy; vel[3 * o + 2] += f * dz;
            }
          }
        }
      }
    }
    K.t += dt;
    return imp;
  }

  function kFrame() {
    if (!K) return;
    var steps = parseInt(Sim.$("#k-speed").value, 10), imp = 0;
    for (var i = 0; i < steps; i++) imp += kStep();
    var tSpan = steps * K.dt;
    K.imp.push([imp, tSpan]);
    K.impSum += imp; K.impT += tSpan;
    while (K.impT > 300 && K.imp.length > 1) { var o = K.imp.shift(); K.impSum -= o[0]; K.impT -= o[1]; }
    kDraw();
  }

  function speedsNow() {
    var out = new Array(K.N);
    for (var i = 0; i < K.N; i++) {
      var vx = K.vel[3 * i], vy = K.vel[3 * i + 1], vz = K.vel[3 * i + 2];
      out[i] = Math.sqrt(vx * vx + vy * vy + vz * vz) * 1000;
    }
    return out;
  }

  function kDraw() {
    var c = boxCanvas, dpr = window.devicePixelRatio || 1, W = c.clientWidth || 300, H = c.clientHeight || 300;
    if (c.width !== Math.round(W * dpr) || c.height !== Math.round(H * dpr)) { c.width = Math.round(W * dpr); c.height = Math.round(H * dpr); }
    var ctx = c.getContext("2d");
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.fillStyle = Sim.color("plot-bg"); ctx.fillRect(0, 0, W, H);
    var size = Math.min(W, H) - 10, ox = (W - size) / 2, oy = 5, sc = size / K.L;
    ctx.strokeStyle = Sim.color("muted"); ctx.strokeRect(ox, oy, size, size);
    var T = kT(), vmp = Math.sqrt(2 * C.kB * T / K.m);
    var rpx = Math.max(1.2, K.s / 2 * sc);
    var sp = speedsNow();
    for (var i = 0; i < K.N; i++) {
      var f = Math.min(1, sp[i] / (2.2 * vmp));
      ctx.fillStyle = "hsl(" + Math.round(220 - 220 * f) + ",75%,52%)";
      ctx.beginPath(); ctx.arc(ox + K.pos[3 * i] * sc, oy + K.pos[3 * i + 1] * sc, rpx, 0, 2 * Math.PI); ctx.fill();
    }
    // histogram, accumulated over the last few frames
    kHistAcc.push(sp);
    if (kHistAcc.length > 12) kHistAcc.shift();
    var all = [];
    kHistAcc.forEach(function (a) { for (var j = 0; j < a.length; j++) all.push(a[j]); });
    var vmax = 3.6 * vmp, bins = 40, h = S.histogram(all, 0, vmax, bins);
    var bars = h.counts.map(function (n, k) { return [h.edges[k] + h.width / 2, n / (all.length * h.width)]; });
    var mb = [], Mk = K.m * C.NA;
    for (var k2 = 0; k2 <= 200; k2++) {
      var v = vmax * k2 / 200;
      mb.push([v, 4 * Math.PI * Math.pow(Mk / (2 * Math.PI * C.R * T), 1.5) * v * v * Math.exp(-Mk * v * v / (2 * C.R * T))]);
    }
    hPlot.draw([{ type: "bars", data: bars, color: "s1", barWidth: h.width, label: "simulation (last 12 frames)" },
      { type: "line", data: mb, color: "s2", label: "Maxwell–Boltzmann at " + T + " K" }], { xMax: vmax });
    // numbers
    var Tk = kineticT();
    var v2 = 0;
    for (var q = 0; q < sp.length; q++) v2 += sp[q] * sp[q];
    var vrms = Math.sqrt(v2 / sp.length), vmean = S.mean(sp);
    var V = Math.pow(K.L * 1e-9, 3), A = 6 * Math.pow(K.L * 1e-9, 2);
    var p = K.impT > 0 ? K.m * K.impSum * 1000 / (K.impT * 1e-12 * A) : NaN;   // Pa
    var pid = K.N * C.kB * Tk / V;
    var out = Sim.$("#k-out");
    out.textContent = "";
    [["simulated time", (K.t / 1000).toFixed(3) + " ns"],
      ["atoms, box", K.N + " " + K.g.name + ", " + K.L + " nm edge"],
      ["pressure (wall impulses, last 300 ps)", isFinite(p) ? (p / 1e3).toFixed(1) + " kPa = " + (p / 1e5).toFixed(3) + " bar" : "—"],
      ["N k T/V (ideal, with T from speeds)", (pid / 1e3).toFixed(1) + " kPa"],
      ["Z = pV/NkT", isFinite(p) ? (p / pid).toFixed(3) : "—"],
      ["T from speeds = m⟨v²⟩/3k", Tk.toFixed(1) + " K"],
      ["rms speed (simulation)", vrms.toFixed(0) + " m/s"],
      ["√(3RT/M) at the wall T", Math.sqrt(3 * C.R * T / (K.g.M * 1e-3)).toFixed(0) + " m/s"],
      ["mean speed (simulation)", vmean.toFixed(0) + " m/s"],
      ["√(8RT/πM) at the wall T", Math.sqrt(8 * C.R * T / (Math.PI * K.g.M * 1e-3)).toFixed(0) + " m/s"],
      ["last export (3000 speeds)", K.exportInfo || "—"],
      ["walls", Sim.$("#k-thermal").checked ? "thermal (exchange energy at T)" : "elastic (isolated gas: changing T has no effect until restart)"]].forEach(function (r) {
      out.appendChild(Sim.el("span", { text: r[0] })); out.appendChild(Sim.el("span", { text: r[1] }));
    });
  }

  function kStart() {
    if (kLoop) kLoop.stop();
    kLoop = Sim.loop(function () {
      if (!kRunning || Sim.$("#tab-kinetic").hidden) return true;
      kFrame();
      return true;
    });
  }

  function kExport() {
    if (!K) return null;
    var speeds = speedsNow().slice();
    var decor = Math.max(1, Math.round(60 / K.dt));      // about 60 ps between snapshots
    while (speeds.length < 3000) {
      for (var i = 0; i < decor; i++) kStep();
      speeds = speeds.concat(speedsNow());
    }
    speeds = speeds.slice(0, 3000);
    var v2 = 0;
    speeds.forEach(function (v) { v2 += v * v; });
    v2 /= speeds.length;
    var T = K.g.M * 1e-3 * v2 / (3 * C.R), uT = T * Math.sqrt(2 / (3 * speeds.length));
    K.exportInfo = "⟨v²⟩ = " + v2.toExponential(4) + " m²/s², T = " + Sim.fmtU(T, uT, "K");
    kDraw();
    return { header: ["speed_m_s"], rows: speeds.map(function (v) { return [+v.toFixed(2)]; }), filename: "my_speeds.csv" };
  }

  Sim.$("#k-speed").addEventListener("input", function () { Sim.$("#k-speed-out").textContent = Sim.$("#k-speed").value + " steps/frame"; });
  Sim.$("#k-run").addEventListener("click", function () { kRunning = !kRunning; Sim.$("#k-run").textContent = kRunning ? "Pause" : "Run"; });
  Sim.$("#k-reset").addEventListener("click", function () { kReset(); kDraw(); });
  ["#k-gas", "#k-N", "#k-L"].forEach(function (s) { Sim.$(s).addEventListener("change", function () { kReset(); kDraw(); }); });
  Sim.$("#k-T").addEventListener("change", function () { if (K) kSetDt(); });
  Sim.exportCSV(Sim.$("#k-export"), "my_speeds.csv", kExport);

  /* ======================= CLEMENT-DESORMES ======================= */
  // Educational model: heat exchange with the room is Newtonian with two time constants,
  // tuned to the behaviour described in Lesson 23.1: a 1 s opening loses only about 1 % of
  // the cooling (TAU_OPEN), and the closed bottle settles within 2-3 minutes (TAU_TH).
  var RHO_W = 998.2, TAU_TH = 30, TAU_OPEN = 100, TAU_FLOW = 0.12, TAU_LEAK = 600, T_ROOM = 293.15;
  var cd = null, trials = [];
  var tracePlot = Sim.plot(Sim.$("#c-trace"), { xLabel: "time / min", yLabel: "h / cm of water", legend: false, yMin: 0 });
  var cr = Sim.rng(seed + 202);

  function p0() { return parseFloat(Sim.$("#c-p0").value) * 1000; }
  function gam() { return parseFloat(Sim.$("#c-gas").value); }
  function hOf(p) { return (p - p0()) / (RHO_W * C.g) * 100; }

  function cdReset() {
    cd = { p: p0(), T: T_ROOM, t: 0, trace: [[0, 0]], h1: null, opened: null };
    Sim.$("#c-log").textContent = "";
  }

  function clog(text) { Sim.log(Sim.$("#c-log"), "[" + (cd.t / 60).toFixed(1) + " min] " + text); }

  function evolveClosed(dtTotal) {
    // closed bottle: gas relaxes to room temperature at constant volume, p proportional to T
    var stepT = Math.min(1, dtTotal);
    var n = Math.max(1, Math.round(dtTotal / stepT)), dt = dtTotal / n;
    var leak = Sim.$("#c-leak").checked;
    for (var i = 0; i < n; i++) {
      var Tn = T_ROOM + (cd.T - T_ROOM) * Math.exp(-dt / TAU_TH);
      cd.p *= Tn / cd.T;
      cd.T = Tn;
      if (leak) cd.p = p0() + (cd.p - p0()) * Math.exp(-dt / TAU_LEAK);
      cd.t += dt;
      if (i % Math.max(1, Math.round(5 / dt)) === 0 || i === n - 1) cd.trace.push([cd.t, hOf(cd.p)]);
    }
  }

  function pump() {
    var g = gam(), dp = cr.uniform(360, 440);
    var pn = cd.p + dp;
    cd.T = cd.T * Math.pow(pn / cd.p, (g - 1) / g);   // the gas already inside is compressed adiabatically
    cd.p = pn;
    cd.t += 3;
    cd.trace.push([cd.t, hOf(cd.p)]);
    clog("Pump stroke: h jumps to " + hOf(cd.p).toFixed(1) + " cm (the gas is warm).");
    if (hOf(cd.p) > 35) {
      cd.p = p0();
      cd.trace.push([cd.t, 0]);
      clog("The stopper popped out! Too much pressure. Real setups stay at 10–20 cm of water.");
    }
    evolveClosed(2);
  }

  function readH() { return Math.round((hOf(cd.p) + cr.normal(0, 0.07)) * 20) / 20; }   // two arms, each read to about 0.05 cm

  function openTap(tOpen) {
    var g = gam(), P0 = p0(), pStart = cd.p, period = cr.uniform(0.25, 1.2), w = 2 * Math.PI / period;
    var tClose = Math.max(0.02, tOpen + cr.normal(0, 0.04));   // the hand is not a perfect timer
    var dt = 0.0005, t = 0, p = cd.p, T = cd.T;
    while (t < tClose) {
      var pn = P0 + (pStart - P0) * Math.exp(-(t + dt) / TAU_FLOW) * Math.cos(w * (t + dt));
      // gas left in the bottle: reversible adiabatic change plus heat from the walls
      T += (g - 1) / g * T / p * (pn - p) + (T_ROOM - T) / TAU_OPEN * dt;
      p = pn; t += dt;
      if (Math.round(t / dt) % 40 === 0) cd.trace.push([cd.t + t, hOf(p)]);
    }
    cd.p = p; cd.T = T; cd.t += t;
    cd.trace.push([cd.t, hOf(cd.p)]);
    clog("Tap open for " + tOpen + " s, closed. The gas inside is now " + (T_ROOM - T).toFixed(2) + " K colder than the room.");
    cd.opened = { tOpen: tOpen };
    evolveClosed(1);
  }

  function addTrial(h1, h2, tOpen) {
    var P0 = p0(), p1 = P0 + RHO_W * C.g * h1 / 100, p2 = P0 + RHO_W * C.g * h2 / 100;
    trials.push({ h1: h1, h2: h2, tOpen: tOpen, gApprox: h1 / (h1 - h2), gLog: Math.log(p1 / P0) / Math.log(p1 / p2) });
    renderTrials();
  }

  function renderTrials() {
    var tb = Sim.$("#c-table tbody");
    tb.textContent = "";
    trials.forEach(function (x, i) {
      tb.appendChild(Sim.el("tr", {}, Sim.el("td", { text: String(i + 1) }), Sim.el("td", { text: String(x.tOpen) }), Sim.el("td", { text: x.h1.toFixed(2) }),
        Sim.el("td", { text: x.h2.toFixed(2) }), Sim.el("td", { text: x.gApprox.toFixed(3) }), Sim.el("td", { text: x.gLog.toFixed(3) })));
    });
    var sel = trials.filter(function (x) { return Math.abs(x.tOpen - 1) < 0.25; }).map(function (x) { return x.gApprox; });
    var el = Sim.$("#c-summary");
    el.textContent = "";
    if (sel.length >= 2) {
      var m = S.mean(sel), s = S.sd(sel), t = S.tInv(0.95, sel.length - 1), hw = t * s / Math.sqrt(sel.length);
      [["trials with about 1 s opening", String(sel.length)], ["mean γ", m.toFixed(3)], ["s", s.toFixed(3)],
        ["95 % interval of the mean", m.toFixed(3) + " ± " + hw.toFixed(3)], ["C_V,m = R/(γ − 1)", (1 / (m - 1)).toFixed(2) + " R"]].forEach(function (r) {
        el.appendChild(Sim.el("span", { text: r[0] })); el.appendChild(Sim.el("span", { text: r[1] }));
      });
    }
  }

  function drawMano() {
    var cv = Sim.$("#c-mano"), dpr = window.devicePixelRatio || 1, W = cv.clientWidth || 110, H = cv.clientHeight || 300;
    cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
    var ctx = cv.getContext("2d");
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.fillStyle = Sim.color("plot-bg"); ctx.fillRect(0, 0, W, H);
    var h = hOf(cd.p), pxcm = (H - 40) / 44, mid = H / 2 + 10;
    var lx = W * 0.3, rx = W * 0.62, tw = 10;
    ctx.fillStyle = Sim.isDark() ? "rgba(90,169,230,0.55)" : "rgba(31,111,178,0.45)";
    var yl = mid + h / 2 * pxcm, yr = mid - h / 2 * pxcm;
    ctx.fillRect(lx - tw / 2, yl, tw, H - 12 - yl);
    ctx.fillRect(rx - tw / 2, yr, tw, H - 12 - yr);
    ctx.fillRect(lx - tw / 2, H - 16, rx - lx + tw, 6);
    ctx.strokeStyle = Sim.color("muted"); ctx.lineWidth = 1;
    ctx.strokeRect(lx - tw / 2, 6, tw, H - 16); ctx.strokeRect(rx - tw / 2, 6, tw, H - 16);
    ctx.fillStyle = Sim.color("ink"); ctx.font = "10px " + getComputedStyle(document.body).fontFamily; ctx.textAlign = "left";
    for (var c = -20; c <= 20; c += 2) {
      var y = mid - c * pxcm;
      ctx.beginPath(); ctx.moveTo(rx + tw / 2 + 2, y); ctx.lineTo(rx + tw / 2 + (c % 10 === 0 ? 12 : 6), y); ctx.stroke();
      if (c % 10 === 0) ctx.fillText(String(c), rx + tw / 2 + 14, y + 3);
    }
    ctx.textAlign = "center";
    ctx.fillText("bottle", lx, H - 1);
    ctx.fillText("h = " + h.toFixed(1), W / 2, 12);
  }

  function renderClement() {
    if (!cd) return;
    drawMano();
    var tr = cd.trace.filter(function (pt) { return pt[0] > cd.t - 900; }).map(function (pt) { return [pt[0] / 60, pt[1]]; });
    tracePlot.draw([{ type: "line", data: tr, color: "s1" }]);
    var st = Sim.$("#c-state");
    st.textContent = "";
    [["clock", (cd.t / 60).toFixed(2) + " min"], ["h now (gauge)", hOf(cd.p).toFixed(2) + " cm"], ["gas temperature − room", (cd.T - T_ROOM).toFixed(3) + " K"],
      ["pending h₁", cd.h1 === null ? "—" : cd.h1.toFixed(2) + " cm"]].forEach(function (r) {
      st.appendChild(Sim.el("span", { text: r[0] })); st.appendChild(Sim.el("span", { text: r[1] }));
    });
  }

  function doRead(which) {
    var h = readH();
    cd.t += 5;
    if (which === 1) {
      cd.h1 = h; cd.opened = null;
      clog("Read h₁ = " + h.toFixed(2) + " cm" + (Math.abs(cd.T - T_ROOM) > 0.02 ? " (the manometer was still moving)" : "") + ".");
    } else {
      if (cd.h1 === null || !cd.opened) { clog("Read h = " + h.toFixed(2) + " cm. Read h₁ and open the tap first to make a trial."); return; }
      clog("Read h₂ = " + h.toFixed(2) + " cm" + (Math.abs(cd.T - T_ROOM) > 0.02 ? " (the manometer was still moving)" : "") + ". Trial recorded.");
      addTrial(cd.h1, h, cd.opened.tOpen);
      cd.h1 = null; cd.opened = null;
    }
  }

  function autoTrial() {
    var tOpen = parseFloat(Sim.$("#c-topen").value) || 1;
    if (hOf(cd.p) > 2) { clog("Venting the bottle before a new trial."); cd.p = p0(); cd.T = T_ROOM; evolveClosed(30); }
    var strokes = 0;
    while (hOf(cd.p) < 18 && strokes < 8) { pump(); strokes++; }
    evolveClosed(180);
    doRead(1);
    openTap(tOpen);
    evolveClosed(240);
    doRead(2);
  }

  function cAct(fn) { return function () { if (!cd) cdReset(); fn(); renderClement(); }; }
  Sim.$("#c-pump").addEventListener("click", cAct(pump));
  Sim.$("#c-wait").addEventListener("click", cAct(function () { evolveClosed(30); clog("Waited 30 s."); }));
  Sim.$("#c-wait3").addEventListener("click", cAct(function () { evolveClosed(180); clog("Waited 3 min."); }));
  Sim.$("#c-h1").addEventListener("click", cAct(function () { doRead(1); }));
  Sim.$("#c-h2").addEventListener("click", cAct(function () { doRead(2); }));
  Sim.$("#c-open").addEventListener("click", cAct(function () { openTap(parseFloat(Sim.$("#c-topen").value) || 1); }));
  Sim.$("#c-auto").addEventListener("click", cAct(autoTrial));
  Sim.$("#c-auto8").addEventListener("click", cAct(function () { for (var i = 0; i < 8; i++) autoTrial(); }));
  Sim.$("#c-clear").addEventListener("click", function () { trials = []; renderTrials(); });
  ["#c-gas", "#c-p0"].forEach(function (s) { Sim.$(s).addEventListener("change", function () { cdReset(); renderClement(); }); });
  Sim.exportCSV(Sim.$("#c-export"), "my_clement.csv", function () {
    return { header: ["trial", "h1_cm", "h2_cm"], rows: trials.map(function (x, i) { return [i + 1, x.h1.toFixed(2), x.h2.toFixed(2)]; }) };
  });

  /* ======================= EXPORT AND START ======================= */
  Sim.exportCSV(Sim.$("#x-ideal"), "ideal_gas_readings.csv", function () {
    return { header: ["reading", "n_mol", "T_K", "V_L", "inv_V_per_L", "p_kPa"], rows: ideal.readings.map(function (r, i) { return [i + 1, r.n, r.T, r.V, +(1 / r.V).toFixed(6), r.p]; }) };
  });
  Sim.exportCSV(Sim.$("#x-real"), "real_gas_curves.csv", function () {
    var rows = [];
    real.zCurves.forEach(function (c) { c.data.forEach(function (pt) { rows.push(["Z", c.key, c.T, +pt[0].toFixed(3), "", +pt[1].toFixed(5)]); }); });
    real.isos.forEach(function (c) { c.stable.forEach(function (pt) { rows.push(["isotherm", c.key, c.T, +pt[1].toFixed(4), +pt[0].toFixed(5), ""]); }); });
    return { header: ["curve", "gas", "T_K", "p_bar", "Vm_L_per_mol", "Z"], rows: rows };
  });

  var tabs = Sim.tabs(Sim.$("#tabs"), function (name) {
    if (name === "ideal") { idealRead(); renderIdeal(); }
    if (name === "real") { renderConsts(); drawReal(); }
    if (name === "kinetic" && K) kDraw();
    if (name === "clement") { if (!cd) cdReset(); renderClement(); }
  });
  Sim.onTheme(function () { if (cd) drawMano(); if (K) kDraw(); idealRead(); });

  if (preset.key === "real") { gasSel.value = "CO2"; Sim.$("#r-T").value = "320"; }
  if (preset.key === "kinetic") { kSel.value = "Ar"; Sim.$("#k-T").value = "300"; }
  kReset();
  kStart();
  cdReset();
  tabs.select(preset.tab || "ideal");
  if (preset.key === "real") addZ();
})();
