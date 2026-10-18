/* oscillators simulation, part 1: shared helpers, presets, the single mass on a spring and the
 * damped ringdown. Part 2 (oscillators-modes.js) has the coupled masses and CO2 and selects the
 * starting tab. Uses ../common/sim.js (global Sim). Classic scripts, no modules.
 *
 * Physics and numbers (lessons 03.4, 04.2, 14.1, 14.2):
 *  - m x'' + b x' + k x = 0: omega0 = sqrt(k/m), gamma = b/2m, Q = omega0/(2 gamma).
 *  - Anharmonic spring F = -k x (1 + beta x^2): omega ~ omega0 (1 + 3/8 beta A^2) (lesson 14.2).
 *  - Quadratic air drag F = -c v|v| (a card under the phone at large speed).
 *  - A uniform spring adds about m_s/3 to the moving mass (lesson 14.1).
 *  - Local gravity 9.795 m/s^2 (Israel, as used in lesson 14.1); standard g is 9.80665.
 *  - Scenario parameters are chosen to reproduce the lesson example data: steel spring
 *    f_d = 1.40 Hz, gamma = 0.040 1/s (Q 110); card gamma = 0.30 1/s (Q 14.6); hair bands
 *    2.000 Hz, Q 51, beta = -46 m^-2 (frequency rises 1.6 % as a 3.1 cm swing dies).
 *  - Measurement noise: stopwatch reaction about 0.08 s per 10-period timing, phyphox period
 *    about 0.003 s (lesson 14.1), ruler reading 1 mm, accelerometer noise a few hundredths m/s^2.
 */
(function (global) {
  "use strict";
  var S = Sim.stats, TAU = 2 * Math.PI, G_LOCAL = 9.795;

  var PRESETS = {
    single: {
      title: "A single mass on a spring", tab: "single",
      what: "A mass on a spring oscillates at ω = √(k/m), whatever the amplitude: stiffer is faster, heavier is slower. The same formula with the reduced mass gives the vibration of a chemical bond. You can measure k two independent ways: statically (stretch per newton) and dynamically (the period). When the spring's own mass is not negligible, about a third of it moves with the load.",
      task: "With m = 0.20 kg, find the spring constant that gives a period of exactly 1.00 s. Then set the spring's mass to 30 g, take static readings and phyphox periods at four or five masses (0.150–0.350 kg), and compare the static and dynamic k.",
      target: "k = 4π²m/T² = 7.9 N/m. With a free intercept the two values of k agree within about 2 u<sub>c</sub>, and m<sub>eff</sub> comes out near 10 g (m<sub>s</sub>/3)."
    },
    damped: {
      title: "Damped mass on a spring", tab: "damped", scenario: "book",
      what: "Friction adds a force −bẋ. The roots of mr² + br + k = 0 decide the motion: underdamped (a decaying oscillation inside e<sup>−γt</sup>), critically damped (the fastest return without overshoot) or overdamped (a slow creep). The quality factor Q = ω₀/2γ counts how long the oscillator rings; a ringdown recorded with a phone measures it.",
      task: "Textbook spring (m 0.200 kg, k 20.0 N/m, b 0.40 kg/s): classify the motion and read Q. Raise b to 4.0 and then 10 kg/s. Then choose <b>Phone on a steel spring</b>, record 60 s and measure Q from the peaks; repeat with the cardboard disc and the elastic bands.",
      target: "Q = 5 and critical damping at b = 2√(mk) = 4.0 kg/s; the steel spring gives Q ≈ 110 (γ ≈ 0.040 s⁻¹), the card Q ≈ 15, and the bands a frequency that rises about 1.6 % as the swing dies."
    },
    "coupled-three": {
      title: "Three coupled masses between walls", tab: "coupled",
      what: "Join three masses with springs and they stop moving independently, yet every motion is a sum of three normal modes in which all masses move at one frequency in a fixed shape. The frequencies are the square roots of the eigenvalues of K v = ω² M v. Release one mass alone and the energy wanders along the chain at the beat frequency.",
      task: "With m = 0.100 kg and k = 10.0 N/m between walls, read the three mode frequencies. Start each mode from its shape, then pull mass 1 only and watch the energy move. Double the middle mass and predict first which mode does not change.",
      target: "1.22, 2.25 and 2.94 Hz; with m₂ = 0.200 kg mode 2 stays at 2.25 Hz because the middle mass does not move in it."
    },
    co2: {
      title: "CO₂ normal modes", tab: "co2",
      what: "CO₂ is a free chain O–C–O with a light middle mass. Its vibrations are the symmetric stretch ν₁ (carbon still), the doubly degenerate bend ν₂ and the antisymmetric stretch ν₃. One force constant per bond cannot fit both stretches; a bond–bond interaction constant k₁₂ fixes that. Only modes that change the dipole moment absorb infrared light.",
      task: "With the default force constants read the frequency of each stretch for ¹²C and for ¹³C. Then set the interaction constant to zero and watch the ν₃/ν₁ ratio.",
      target: "ν₁ unchanged at 1333 cm⁻¹; ν₃ falls about 3 %, from 2349 to 2282 cm⁻¹; with k₁₂ = 0 the ratio ν₃/ν₁ jumps from 1.762 to 1.92."
    }
  };

  var preset = Sim.preset(PRESETS, "single");
  var seed0 = Sim.seedFromQuery(14);
  Sim.label();
  Sim.presetBox(Sim.$("#preset"), preset);

  /* ---------- shared helpers ---------- */

  function canvas2d(canvas) {
    var dpr = global.devicePixelRatio || 1;
    var W = canvas.clientWidth || 300, H = canvas.clientHeight || 150;
    if (canvas.width !== Math.round(W * dpr) || canvas.height !== Math.round(H * dpr)) {
      canvas.width = Math.round(W * dpr);
      canvas.height = Math.round(H * dpr);
    }
    var ctx = canvas.getContext("2d");
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.fillStyle = Sim.color("plot-bg");
    ctx.fillRect(0, 0, W, H);
    return { ctx: ctx, W: W, H: H };
  }

  // a zig-zag spring from (x1,y1) to (x2,y2)
  function zigzag(ctx, x1, y1, x2, y2, coils, width) {
    var dx = x2 - x1, dy = y2 - y1, len = Math.sqrt(dx * dx + dy * dy) || 1;
    var ux = dx / len, uy = dy / len, nx = -uy, ny = ux;
    var lead = Math.min(8, len * 0.1);
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x1 + ux * lead, y1 + uy * lead);
    var n = coils * 2, seg = (len - 2 * lead) / n;
    for (var i = 1; i <= n; i++) {
      var s = lead + seg * (i - 0.5), side = (i % 2 ? 1 : -1) * width;
      ctx.lineTo(x1 + ux * s + nx * side, y1 + uy * s + ny * side);
    }
    ctx.lineTo(x2 - ux * lead, y2 - uy * lead);
    ctx.lineTo(x2, y2);
    ctx.stroke();
  }

  // vertical spring with a mass: x is the displacement in metres (down positive), scale px per m
  function drawHangingSpring(canvas, x, scale, label) {
    var c = canvas2d(canvas), ctx = c.ctx, W = c.W, H = c.H;
    var top = 12, eq = H * 0.55, y = eq + x * scale;
    y = Math.max(top + 30, Math.min(H - 26, y));
    ctx.fillStyle = Sim.color("muted");
    ctx.fillRect(W * 0.2, 4, W * 0.6, 6);
    ctx.strokeStyle = Sim.color("ink");
    ctx.lineWidth = 1.5;
    zigzag(ctx, W / 2, top, W / 2, y - 12, 9, Math.min(12, W * 0.12));
    ctx.fillStyle = Sim.color("s1");
    ctx.fillRect(W / 2 - 18, y - 12, 36, 24);
    ctx.strokeStyle = Sim.color("plot-grid");
    ctx.setLineDash([3, 3]);
    ctx.beginPath(); ctx.moveTo(4, eq); ctx.lineTo(W - 4, eq); ctx.stroke();
    ctx.setLineDash([]);
    if (label) {
      ctx.fillStyle = Sim.color("muted");
      ctx.font = "11px " + (getComputedStyle(document.body).fontFamily || "sans-serif");
      ctx.textAlign = "center";
      ctx.fillText(label, W / 2, H - 6);
    }
  }

  // Jacobi eigen-decomposition of a small symmetric matrix A (array of rows). Returns {values, vectors}
  // with vectors[k] the k-th eigenvector, sorted by ascending eigenvalue.
  function jacobiEigen(A0) {
    var n = A0.length, A = A0.map(function (r) { return r.slice(); });
    var V = [];
    for (var i = 0; i < n; i++) { V.push([]); for (var j = 0; j < n; j++) V[i].push(i === j ? 1 : 0); }
    for (var sweep = 0; sweep < 100; sweep++) {
      var off = 0;
      for (var p = 0; p < n; p++) for (var q = p + 1; q < n; q++) off += A[p][q] * A[p][q];
      if (off < 1e-30) break;
      for (p = 0; p < n; p++) {
        for (q = p + 1; q < n; q++) {
          if (Math.abs(A[p][q]) < 1e-300) continue;
          var th = (A[q][q] - A[p][p]) / (2 * A[p][q]);
          var t = (th >= 0 ? 1 : -1) / (Math.abs(th) + Math.sqrt(th * th + 1));
          var cs = 1 / Math.sqrt(t * t + 1), sn = t * cs;
          for (var k = 0; k < n; k++) {
            var akp = A[k][p], akq = A[k][q];
            A[k][p] = cs * akp - sn * akq; A[k][q] = sn * akp + cs * akq;
          }
          for (k = 0; k < n; k++) {
            var apk = A[p][k], aqk = A[q][k];
            A[p][k] = cs * apk - sn * aqk; A[q][k] = sn * apk + cs * aqk;
          }
          for (k = 0; k < n; k++) {
            var vkp = V[k][p], vkq = V[k][q];
            V[k][p] = cs * vkp - sn * vkq; V[k][q] = sn * vkp + cs * vkq;
          }
        }
      }
    }
    var idx = [];
    for (i = 0; i < n; i++) idx.push(i);
    idx.sort(function (a, b) { return A[a][a] - A[b][b]; });
    return {
      values: idx.map(function (i) { return A[i][i]; }),
      vectors: idx.map(function (i) { return V.map(function (row) { return row[i]; }); })
    };
  }

  // generalised problem K v = w2 M v with diagonal masses m[]: returns modes sorted by w2,
  // shapes normalised to largest |component| = 1, first non-zero component positive
  function normalModes(K, m) {
    var n = m.length, A = [];
    for (var i = 0; i < n; i++) { A.push([]); for (var j = 0; j < n; j++) A[i].push(K[i][j] / Math.sqrt(m[i] * m[j])); }
    var e = jacobiEigen(A);
    return e.values.map(function (w2, k) {
      var v = e.vectors[k].map(function (y, i) { return y / Math.sqrt(m[i]); });
      var big = 0;
      v.forEach(function (c) { if (Math.abs(c) > Math.abs(big)) big = c; });
      v = v.map(function (c) { return Math.abs(c / big) < 1e-9 ? 0 : c / Math.abs(big); });
      var first = 0;
      for (i = 0; i < n; i++) if (v[i] !== 0) { first = v[i]; break; }
      if (first < 0) v = v.map(function (c) { return c === 0 ? 0 : -c; });
      if (Math.abs(w2) < 1e-9 * Math.max(1, Math.abs(e.values[n - 1]))) w2 = 0;
      return { w2: w2, w: Math.sqrt(Math.max(0, w2)), v: v };
    });
  }

  function setLog(el, text) { Sim.log(el, text); }
  function tr(cells) {
    var row = Sim.el("tr");
    cells.forEach(function (c) { row.appendChild(Sim.el("td", { html: String(c) })); });
    return row;
  }
  function kv(el, pairs) {
    el.textContent = "";
    pairs.forEach(function (p) {
      el.appendChild(Sim.el("span", { html: p[0] }));
      el.appendChild(Sim.el("span", { html: p[1] }));
    });
  }

  global.OscApp = {
    preset: preset, seed0: seed0, canvas2d: canvas2d, zigzag: zigzag, drawHangingSpring: drawHangingSpring,
    normalModes: normalModes, tr: tr, kv: kv, setLog: setLog, refresh: {}
  };

  /* ======================= SINGLE MASS ON A SPRING ======================= */
  var sp = {
    seed: seed0, rng: Sim.rng(seed0), readings: [], running: false, t: 0, A: 0.02, trace: [],
    damaged: false, L0: 0.150
  };
  var sPlot = Sim.plot(Sim.$("#s-plot"), { xLabel: "time / s", yLabel: "x / cm" });
  var sFitL = Sim.plot(Sim.$("#s-fitL"), { xLabel: "m / kg", yLabel: "length / m" });
  var sFitT = Sim.plot(Sim.$("#s-fitT"), { xLabel: "m / kg", yLabel: "T² / s²", xMin: 0, yMin: 0 });

  function sVals() {
    var k = parseFloat(Sim.$("#s-k").value);
    return {
      m: parseFloat(Sim.$("#s-m").value), k: k, kEff: k * (sp.damaged ? 0.85 : 1),
      ms: parseFloat(Sim.$("#s-ms").value) / 1000, A: parseFloat(Sim.$("#s-A").value) / 100,
      tension: Sim.$("#s-tension").checked
    };
  }
  function sPeriod(v) { return TAU * Math.sqrt((v.m + v.ms / 3) / v.kEff); }

  function sTheory() {
    var v = sVals();
    Sim.$("#s-k-out").textContent = v.k.toFixed(1);
    Sim.$("#s-seed").textContent = sp.seed;
    if (!(v.m > 0 && v.k > 0 && v.ms >= 0)) { Sim.$("#s-theory").textContent = "Enter positive values."; return; }
    var w = Math.sqrt(v.kEff / (v.m + v.ms / 3)), T = TAU / w;
    var rows = [
      ["ω₀ = √(k/(m + m<sub>s</sub>/3))", w.toFixed(3) + " rad/s"],
      ["f = ω₀/2π", (w / TAU).toFixed(3) + " Hz"],
      ["Period T", T.toFixed(4) + " s"],
      ["Energy ½kA²", (0.5 * v.kEff * v.A * v.A * 1000).toFixed(2) + " mJ"],
      ["Static stretch mg/k", (100 * v.m * G_LOCAL / v.kEff).toFixed(1) + " cm"]
    ];
    if (sp.damaged) rows.push(["Spring", "<span class=\"bad\">overstretched: k is now 15 % lower</span>"]);
    kv(Sim.$("#s-theory"), rows);
  }

  function sDrawTrace() {
    var data = sp.trace.map(function (p) { return [p[0], p[1] * 100]; });
    var t1 = sp.trace.length ? sp.trace[sp.trace.length - 1][0] : 0;
    var A = Math.max(0.5, sVals().A * 100 * 1.15);
    sPlot.draw([{ data: data, color: "s1", width: 1.6 }], { xMin: Math.max(0, t1 - 8), xMax: Math.max(8, t1), yMin: -A, yMax: A });
  }

  function sPosition(t) {
    var v = sVals();
    if (v.tension && v.m * G_LOCAL < 0.4) return 0;
    var w = TAU / sPeriod(v);
    return sp.A * Math.exp(-0.015 * t) * Math.cos(w * t);
  }

  function sFrame(dt) {
    if (!sp.running) return false;
    sp.t += dt;
    var x = sPosition(sp.t);
    sp.trace.push([sp.t, x]);
    while (sp.trace.length && sp.trace[0][0] < sp.t - 8.5) sp.trace.shift();
    if (!Sim.$("#tab-single").hidden) {
      sDrawSpring(x);
      sDrawTrace();
    }
    return true;
  }
  function sDrawSpring(x) { drawHangingSpring(Sim.$("#s-anim"), x, 1400, "m = " + sVals().m.toFixed(3) + " kg"); }

  function sRelease() {
    var v = sVals();
    if (sp.loop) { sp.loop.stop(); sp.loop = null; }
    if (sp.running) { sp.running = false; Sim.$("#s-go").textContent = "Release"; return; }
    if (v.tension && v.m * G_LOCAL < 0.4) {
      setLog(Sim.$("#s-log"), "The load (" + (v.m * G_LOCAL).toFixed(2) + " N) is below the built-in tension: the coils stay closed and nothing oscillates.");
    }
    sp.A = v.A; sp.t = 0; sp.trace = []; sp.running = true;
    Sim.$("#s-go").textContent = "Stop";
    sp.loop = Sim.loop(sFrame);
  }

  function sTrial(m, method) {
    var n = 0;
    sp.readings.forEach(function (r) { if (r.method !== "static" && Math.abs(r.m - m) < 1e-9) n++; });
    return n + 1;
  }

  function sStatic() {
    var v = sVals(), rng = sp.rng;
    if (!(v.m > 0)) return;
    var F = v.m * G_LOCAL + v.ms * G_LOCAL / 2;          // the spring's own weight stretches it by half its weight
    var ext = Math.max(0, (F - (v.tension ? 0.4 : 0)) / v.kEff);
    if (ext > 0.22 && !sp.damaged) {
      sp.damaged = true; sp.L0 += 0.03;
      setLog(Sim.$("#s-log"), "Overstretched: " + (ext * 100).toFixed(0) + " cm is past the elastic limit. The spring stays 3 cm longer and its k drops. Re-run for a new spring.");
      ext = Math.max(0, (F - (v.tension ? 0.4 : 0)) / (v.k * 0.85));
    }
    var L = sp.L0 + ext + rng.normal(0, 0.0006);
    L = Math.round(L * 1000) / 1000;
    sp.readings.push({ method: "static", m: v.m, value: L });
    setLog(Sim.$("#s-log"), "Static: m = " + v.m.toFixed(3) + " kg, length = " + L.toFixed(3) + " m");
    sRender();
    sTheory();
  }

  function sDynamic(kind) {
    var v = sVals(), rng = sp.rng;
    if (!(v.m > 0)) return;
    if (v.tension && v.m * G_LOCAL < 0.4) { setLog(Sim.$("#s-log"), "No oscillation: the load is below the spring's built-in tension."); return; }
    var T = sPeriod(v), rec;
    if (kind === "stopwatch") {
      var t10 = 10 * T + rng.normal(0, 0.08);
      t10 = Math.round(t10 * 100) / 100;
      rec = { method: "stopwatch", m: v.m, value: t10 / 10, raw: t10 };
      setLog(Sim.$("#s-log"), "Stopwatch: 10 periods in " + t10.toFixed(2) + " s, T = " + (t10 / 10).toFixed(3) + " s");
    } else {
      var Tp = Math.round((T + rng.normal(0, 0.003)) * 1000) / 1000;
      rec = { method: "phyphox", m: v.m, value: Tp };
      setLog(Sim.$("#s-log"), "phyphox: T = " + Tp.toFixed(3) + " s");
    }
    rec.trial = sTrial(v.m, kind);
    sp.readings.push(rec);
    sRender();
  }

  function sAnalysis() {
    var st = sp.readings.filter(function (r) { return r.method === "static"; });
    var dy = sp.readings.filter(function (r) { return r.method !== "static"; });
    var out = [], res = { st: null, dy: null };
    function distinct(a) { var s = {}; a.forEach(function (r) { s[r.m.toFixed(6)] = 1; }); return Object.keys(s).length; }
    if (st.length >= 2 && distinct(st) >= 2) {
      var f = S.linfit(st.map(function (r) { return r.m; }), st.map(function (r) { return r.value; }));
      var k = G_LOCAL / f.b, uk = k * f.ub / Math.abs(f.b);
      res.st = { k: k, uk: uk, fit: f };
      out.push(["Static: slope of length against m", Sim.fmtU(f.b, f.ub, "m/kg")]);
      out.push(["Static k = g/slope", Sim.fmtU(k, uk, "N/m")]);
    } else out.push(["Static", "need readings at two or more masses"]);
    if (dy.length >= 2 && distinct(dy) >= 2) {
      var x = dy.map(function (r) { return r.m; }), y = dy.map(function (r) { return r.value * r.value; });
      var g = S.linfit(x, y);
      var kd = 4 * Math.PI * Math.PI / g.b, ukd = kd * g.ub / Math.abs(g.b);
      var me = g.a / g.b;
      var cov = isFinite(g.cov) ? g.cov : 0;
      var ume = Math.sqrt(Math.max(0, Math.pow(g.ua / g.b, 2) + Math.pow(g.a * g.ub / (g.b * g.b), 2) - 2 * g.a * cov / Math.pow(g.b, 3)));
      var g0 = S.linfitThrough0(x, y), k0 = 4 * Math.PI * Math.PI / g0.b;
      res.dy = { k: kd, uk: ukd, fit: g };
      out.push(["Dynamic: T² = (4π²/k)(m + m<sub>eff</sub>)", "slope " + Sim.fmtU(g.b, g.ub, "s²/kg")]);
      out.push(["Dynamic k = 4π²/slope", Sim.fmtU(kd, ukd, "N/m")]);
      out.push(["m<sub>eff</sub> = intercept/slope", Sim.fmtU(me * 1000, ume * 1000, "g")]);
      out.push(["Forced through the origin (wrong)", "k = " + k0.toFixed(2) + " N/m"]);
    } else out.push(["Dynamic", "need periods at two or more masses"]);
    if (res.st && res.dy) {
      var uc = Math.sqrt(res.st.uk * res.st.uk + res.dy.uk * res.dy.uk);
      var z = Math.abs(res.st.k - res.dy.k) / uc;
      out.push(["Difference / u<sub>c</sub>", "<span class=\"" + (z < 2 ? "good" : z < 3 ? "warn" : "bad") + "\">" + z.toFixed(1) + (z < 2 ? " (agree)" : z < 3 ? " (borderline)" : " (disagree: look for a systematic error)") + "</span>"]);
    }
    kv(Sim.$("#s-analysis"), out);
    return res;
  }

  function sRender() {
    var tb = Sim.$("#s-table tbody");
    tb.textContent = "";
    sp.readings.forEach(function (r, i) {
      var reading, derived;
      if (r.method === "static") { reading = "L = " + r.value.toFixed(3) + " m"; derived = ""; }
      else if (r.method === "stopwatch") { reading = "t₁₀ = " + r.raw.toFixed(2) + " s"; derived = "T = " + r.value.toFixed(3) + " s"; }
      else { reading = "T = " + r.value.toFixed(3) + " s"; derived = "T² = " + (r.value * r.value).toFixed(4) + " s²"; }
      tb.appendChild(tr([i + 1, r.method, r.m.toFixed(3), reading, derived]));
    });
    var res = sAnalysis();
    var st = sp.readings.filter(function (r) { return r.method === "static"; });
    var dy = sp.readings.filter(function (r) { return r.method !== "static"; });
    var serL = [{ type: "points", data: st.map(function (r) { return [r.m, r.value]; }), color: "s2", label: "readings" }];
    if (res.st) {
      var ms = st.map(function (r) { return r.m; }), lo = Math.min.apply(null, ms), hi = Math.max.apply(null, ms);
      serL.push({ data: [[lo, res.st.fit.a + res.st.fit.b * lo], [hi, res.st.fit.a + res.st.fit.b * hi]], color: "s1", label: "fit" });
    }
    sFitL.draw(serL);
    var serT = [{ type: "points", data: dy.map(function (r) { return [r.m, r.value * r.value]; }), color: "s2", label: "readings" }];
    if (res.dy) {
      var hi2 = Math.max.apply(null, dy.map(function (r) { return r.m; }));
      serT.push({ data: [[0, res.dy.fit.a], [hi2 * 1.05, res.dy.fit.a + res.dy.fit.b * hi2 * 1.05]], color: "s1", label: "fit, free intercept" });
    }
    sFitT.draw(serT);
  }

  Sim.$("#s-go").addEventListener("click", sRelease);
  Sim.$("#s-static").addEventListener("click", sStatic);
  Sim.$("#s-time10").addEventListener("click", function () { sDynamic("stopwatch"); });
  Sim.$("#s-phy").addEventListener("click", function () { sDynamic("phyphox"); });
  Sim.$("#s-clear").addEventListener("click", function () { sp.readings = []; sRender(); });
  Sim.$("#s-rerun").addEventListener("click", function () {
    sp.seed = Sim.newSeed(sp.seed); sp.rng = Sim.rng(sp.seed); sp.damaged = false; sp.L0 = 0.150;
    sp.readings = []; sRender(); sTheory();
    setLog(Sim.$("#s-log"), "New seed " + sp.seed + " and a fresh spring.");
  });
  ["#s-m", "#s-k", "#s-ms", "#s-A", "#s-tension"].forEach(function (id) {
    Sim.$(id).addEventListener("input", function () { sTheory(); if (!sp.running) sDrawSpring(0); });
  });
  Sim.exportCSV(Sim.$("#s-x-static"), "my_static.csv", function () {
    return { header: ["mass_kg", "length_m"], rows: sp.readings.filter(function (r) { return r.method === "static"; }).map(function (r) { return [r.m, r.value]; }) };
  });
  Sim.exportCSV(Sim.$("#s-x-dyn"), "my_dynamic.csv", function () {
    return { header: ["mass_kg", "trial", "period_s"], rows: sp.readings.filter(function (r) { return r.method !== "static"; }).map(function (r) { return [r.m, r.trial, +r.value.toFixed(4)]; }) };
  });
  OscApp.refresh.single = function () { sTheory(); sDrawSpring(sp.running ? sPosition(sp.t) : 0); sDrawTrace(); sRender(); };
  sTheory();

  /* ======================= DAMPED RINGDOWN ======================= */
  var SCN = {
    book: { m: 0.200, k: 20.0, b: 0.40, c2: 0, beta: 0, A: 3, noise: 0.015, dur: 20 },
    steel: { m: 0.210, k: 16.27, b: 0.0168, c2: 0, beta: 0, A: 3, noise: 0.015, dur: 60 },
    card: { m: 0.210, k: 16.27, b: 0.126, c2: 0.04, beta: 0, A: 3, noise: 0.015, dur: 20 },
    band: { m: 0.210, k: 33.16, b: 0.0517, c2: 0, beta: -46, A: 3.1, noise: 0.015, dur: 30 }
  };
  var dp = { seed: seed0 + 1, rec: null, an: null, play: null };
  var dPlot = Sim.plot(Sim.$("#d-plot"), { xLabel: "time / s", yLabel: "a / m s⁻²" });
  var dPeaks = Sim.plot(Sim.$("#d-peaks"), { xLabel: "time / s", yLabel: "ln(peak / m s⁻²)" });
  var dFreq = Sim.plot(Sim.$("#d-freq"), { xLabel: "amplitude / cm", yLabel: "f / Hz" });

  function dVals() {
    function n(id) { return parseFloat(Sim.$(id).value); }
    return { m: n("#d-m"), k: n("#d-k"), b: n("#d-b"), c2: n("#d-c2"), beta: n("#d-beta"), A: n("#d-A") / 100, noise: n("#d-noise"), dur: n("#d-dur") };
  }
  function dApplyScenario(name) {
    var s = SCN[name];
    if (!s) return;
    Sim.$("#d-m").value = s.m; Sim.$("#d-k").value = s.k; Sim.$("#d-b").value = s.b; Sim.$("#d-c2").value = s.c2;
    Sim.$("#d-beta").value = s.beta; Sim.$("#d-A").value = s.A; Sim.$("#d-noise").value = s.noise; Sim.$("#d-dur").value = s.dur;
  }

  function dTheory() {
    var v = dVals();
    Sim.$("#d-seed").textContent = dp.seed;
    if (!(v.m > 0 && v.k > 0 && v.b >= 0)) { Sim.$("#d-theory").textContent = "Enter positive values."; return; }
    var w0 = Math.sqrt(v.k / v.m), g = v.b / (2 * v.m), bc = 2 * Math.sqrt(v.m * v.k), rows = [];
    rows.push(["ω₀ = √(k/m)", w0.toFixed(3) + " rad/s (" + (w0 / TAU).toFixed(3) + " Hz)"]);
    rows.push(["γ = b/2m", g.toFixed(4) + " s⁻¹"]);
    rows.push(["Critical b = 2√(mk)", bc.toFixed(3) + " kg/s"]);
    var disc = g * g - w0 * w0, cls;
    if (Math.abs(disc) <= 1e-6 * w0 * w0) cls = "critically damped (double root r = " + (-g).toFixed(3) + " s⁻¹)";
    else if (disc < 0) {
      var wd = Math.sqrt(-disc);
      cls = "underdamped, r = " + (-g).toFixed(3) + " ± " + wd.toFixed(3) + "i s⁻¹";
      rows.push(["ω<sub>d</sub> = √(ω₀² − γ²)", wd.toFixed(3) + " rad/s, period " + (TAU / wd).toFixed(4) + " s"]);
      rows.push(["Q = ω₀/2γ", g > 0 ? (w0 / (2 * g)).toFixed(1) : "∞"]);
      if (g > 0) rows.push(["Amplitude half-life ln2/γ", (Math.LN2 / g).toFixed(2) + " s"]);
    } else {
      var sq = Math.sqrt(disc);
      cls = "overdamped, r = " + (-g + sq).toFixed(3) + " and " + (-g - sq).toFixed(3) + " s⁻¹";
    }
    rows.splice(2, 0, ["Motion", cls]);
    if (v.beta) rows.push(["Predicted frequency shift at the start, ⅜βA²", (100 * 3 / 8 * v.beta * v.A * v.A).toFixed(2) + " %"]);
    if (v.c2) rows.push(["Drag at the first swing, quadratic / linear", (v.c2 * w0 * v.A / Math.max(1e-12, v.b)).toFixed(2)]);
    kv(Sim.$("#d-theory"), rows);
  }

  // integrate m x'' = -k x (1 + beta x^2) - b v - c v|v| with RK4, sample at 100 Hz
  function dSimulate(v, rng) {
    var fs = 100, n = Math.round(v.dur * fs);
    var stiff = Math.max(Math.sqrt(v.k * (1 + Math.abs(v.beta) * v.A * v.A * 3) / v.m), v.b / v.m, 1);
    var sub = Math.max(4, Math.ceil(0.01 / Math.min(0.0025, 0.2 / stiff)));
    var h = 1 / fs / sub;
    function acc(x, u) { return (-v.k * x * (1 + v.beta * x * x) - v.b * u - v.c2 * u * Math.abs(u)) / v.m; }
    var x = v.A, u = 0, t = [], xs = [], as = [], ax = [], ay = [];
    for (var i = 0; i < n; i++) {
      t.push(i / fs); xs.push(x);
      var a = acc(x, u);
      as.push(a + rng.normal(0, v.noise));
      ax.push(rng.normal(0, v.noise)); ay.push(rng.normal(0, v.noise));
      for (var s = 0; s < sub; s++) {
        var k1x = u, k1u = acc(x, u);
        var k2x = u + 0.5 * h * k1u, k2u = acc(x + 0.5 * h * k1x, u + 0.5 * h * k1u);
        var k3x = u + 0.5 * h * k2u, k3u = acc(x + 0.5 * h * k2x, u + 0.5 * h * k2u);
        var k4x = u + h * k3u, k4u = acc(x + h * k3x, u + h * k3u);
        x += h / 6 * (k1x + 2 * k2x + 2 * k3x + k4x);
        u += h / 6 * (k1u + 2 * k2u + 2 * k3u + k4u);
      }
    }
    return { t: t, x: xs, a: as, ax: ax, ay: ay, v: v };
  }

  // data-driven analysis: cycles between upward zero crossings (with hysteresis), peak per cycle
  function dAnalyse(rec, thrSD) {
    var a = rec.a, t = rec.t, sd = rec.v.noise, hyst = Math.max(3 * sd, 1e-9);
    var ups = [], armed = false, i;
    for (i = 1; i < a.length; i++) {
      if (a[i] < -hyst) armed = true;
      if (armed && a[i - 1] < 0 && a[i] >= 0) {
        ups.push({ t: t[i - 1] + (0 - a[i - 1]) / (a[i] - a[i - 1]) * (t[i] - t[i - 1]), i: i });
        armed = false;
      }
    }
    var peaks = [];
    for (var c = 0; c + 1 < ups.length; c++) {
      var best = -Infinity, bt = 0;
      for (i = ups[c].i; i < ups[c + 1].i; i++) if (a[i] > best) { best = a[i]; bt = t[i]; }
      if (best > 0) peaks.push({ t: bt, a: best, used: best > thrSD * sd, cycleStart: ups[c].t, cycleEnd: ups[c + 1].t });
    }
    var out = { peaks: peaks };
    var used = peaks.filter(function (p) { return p.used; });
    if (used.length >= 3) {
      var f = S.linfit(used.map(function (p) { return p.t; }), used.map(function (p) { return Math.log(p.a); }));
      var gamma = -f.b, ug = f.ub;
      var span = used[used.length - 1].cycleEnd - used[0].cycleStart;
      var fd = used.length / span;
      var w0 = Math.sqrt(Math.pow(TAU * fd, 2) + gamma * gamma);
      out.fit = f; out.gamma = gamma; out.ug = ug; out.fd = fd; out.w0 = w0;
      out.Q = w0 / (2 * gamma); out.uQ = Math.abs(out.Q * ug / gamma);
      out.delta = gamma / fd; out.Qdec = Math.PI / out.delta;
      // windowed frequency: 4 cycles per window, step 2 cycles
      var win = [];
      for (c = 0; c + 4 <= used.length; c += 2) {
        var p0 = used[c], p3 = used[c + 3];
        var fw = 4 / (p3.cycleEnd - p0.cycleStart);
        var amp = (p0.a + used[c + 1].a + used[c + 2].a + p3.a) / 4;
        win.push([amp / Math.pow(TAU * fw, 2) * 100, fw]);
      }
      out.win = win;
      if (win.length >= 2) out.drift = (win[win.length - 1][1] - win[0][1]) / win[0][1];
    }
    return out;
  }

  function dRender() {
    var rec = dp.rec, show = Sim.$("#d-show").value;
    if (!rec) { dPlot.draw([]); dPeaks.draw([]); dFreq.draw([]); kv(Sim.$("#d-analysis"), [["Analysis", "Record a ringdown first."]]); return; }
    var an = dp.an = dAnalyse(rec, parseFloat(Sim.$("#d-thr").value) || 0);
    var step = Math.max(1, Math.floor(rec.t.length / 3000));
    var sig = [], i;
    for (i = 0; i < rec.t.length; i += step) sig.push([rec.t[i], show === "a" ? rec.a[i] : rec.x[i] * 100]);
    var series = [{ data: sig, color: "s1", width: 1, label: show === "a" ? "acceleration (with noise)" : "displacement" }];
    if (show === "a") {
      series.push({ type: "points", data: an.peaks.filter(function (p) { return p.used; }).map(function (p) { return [p.t, p.a]; }), color: "s2", size: 3, label: "peaks used" });
      series.push({ type: "points", hollow: true, data: an.peaks.filter(function (p) { return !p.used; }).map(function (p) { return [p.t, p.a]; }), color: "muted", size: 3, label: "peaks rejected" });
      if (an.fit) {
        var env = [];
        for (i = 0; i <= 60; i++) { var tt = rec.v.dur * i / 60; env.push([tt, Math.exp(an.fit.a + an.fit.b * tt)]); }
        series.push({ data: env, color: "s3", dash: [5, 4], width: 1.5, label: "fitted envelope", noRange: true });
        series.push({ data: env.map(function (p) { return [p[0], -p[1]]; }), color: "s3", dash: [5, 4], width: 1.5, noRange: true });
      }
    }
    dPlot.draw(series, { yLabel: show === "a" ? "a / m s⁻²" : "x / cm" });
    var pser = [
      { type: "points", data: an.peaks.filter(function (p) { return p.used; }).map(function (p) { return [p.t, Math.log(p.a)]; }), color: "s2", label: "used" },
      { type: "points", hollow: true, data: an.peaks.filter(function (p) { return !p.used; }).map(function (p) { return [p.t, Math.log(p.a)]; }), color: "muted", label: "rejected" }
    ];
    if (an.fit) pser.push({ data: [[0, an.fit.a], [rec.v.dur, an.fit.a + an.fit.b * rec.v.dur]], color: "s1", label: "slope −γ", noRange: true });
    dPeaks.draw(pser);
    dFreq.draw(an.win && an.win.length ? [{ type: "points", data: an.win, color: "s4", label: "4-cycle windows" }] : []);
    var rows = [];
    if (!an.fit) {
      rows.push(["Peaks", an.peaks.length ? an.peaks.length + " found, too few above the threshold" : "no oscillation to analyse (critically or overdamped, or all lost in the noise)"]);
    } else {
      rows.push(["Peaks used / found", an.peaks.filter(function (p) { return p.used; }).length + " / " + an.peaks.length]);
      rows.push(["Damped frequency f<sub>d</sub>", an.fd.toFixed(4) + " Hz"]);
      rows.push(["γ from the peaks (−slope)", Sim.fmtU(an.gamma, an.ug, "s⁻¹")]);
      rows.push(["Log decrement δ = γT<sub>d</sub>", an.delta.toFixed(4)]);
      rows.push(["Q = ω₀/2γ", Sim.fmtU(an.Q, an.uQ)]);
      rows.push(["Q ≈ π/δ", an.Qdec.toFixed(1)]);
      rows.push(["Cycles for the amplitude to fall by e", (1 / an.delta).toFixed(1)]);
      if (isFinite(an.drift)) rows.push(["Frequency change, first to last window", (100 * an.drift).toFixed(2) + " %" + (Math.abs(an.drift) < 0.003 ? " (within the noise)" : an.drift > 0 ? " (rises as the swing dies, as for a softening spring, β &lt; 0)" : " (falls as the swing dies, as for a stiffening spring, β &gt; 0)")]);
      var v = rec.v;
      rows.push(["Model's own Q from b alone", v.b > 0 ? (Math.sqrt(v.k / v.m) * v.m / v.b).toFixed(1) : "∞"]);
    }
    kv(Sim.$("#d-analysis"), rows);
  }

  function dRun() {
    var v = dVals();
    if (!(v.m > 0 && v.k > 0 && v.b >= 0 && v.dur > 0)) return;
    dp.rec = dSimulate(v, Sim.rng(dp.seed));
    dRender();
  }

  function dPlay() {
    if (dp.play) { dp.play.stop(); dp.play = null; Sim.$("#d-play").textContent = "Play it back"; return; }
    if (!dp.rec) dRun();
    var rec = dp.rec, t = 0, scale = 35 / Math.max(0.001, rec.v.A);
    Sim.$("#d-play").textContent = "Stop playback";
    dp.play = Sim.loop(function (dt) {
      t += dt;
      var i = Math.min(rec.x.length - 1, Math.round(t * 100));
      drawHangingSpring(Sim.$("#d-anim"), rec.x[i], scale, t.toFixed(1) + " s");
      if (i >= rec.x.length - 1) { dp.play = null; Sim.$("#d-play").textContent = "Play it back"; return false; }
      return true;
    });
  }

  Sim.$("#d-scn").addEventListener("change", function () { dApplyScenario(this.value); dTheory(); dRun(); });
  ["#d-m", "#d-k", "#d-b", "#d-c2", "#d-beta", "#d-A", "#d-noise", "#d-dur"].forEach(function (id) {
    Sim.$(id).addEventListener("input", function () { Sim.$("#d-scn").value = "custom"; dTheory(); });
  });
  Sim.$("#d-run").addEventListener("click", dRun);
  Sim.$("#d-play").addEventListener("click", dPlay);
  Sim.$("#d-rerun").addEventListener("click", function () { dp.seed = Sim.newSeed(dp.seed); dTheory(); dRun(); });
  Sim.$("#d-show").addEventListener("change", dRender);
  Sim.$("#d-thr").addEventListener("input", dRender);
  Sim.exportCSV(Sim.$("#d-x-rec"), "my_spring.csv", function () {
    var r = dp.rec;
    if (!r) return null;
    var rows = r.t.map(function (t, i) { return [+t.toFixed(3), +r.ax[i].toFixed(5), +r.ay[i].toFixed(5), +r.a[i].toFixed(5)]; });
    return { header: ["Time (s)", "Linear Acceleration x (m/s^2)", "Linear Acceleration y (m/s^2)", "Linear Acceleration z (m/s^2)"], rows: rows };
  });
  Sim.exportCSV(Sim.$("#d-x-peaks"), "my_peaks.csv", function () {
    if (!dp.an) return null;
    return { header: ["t_s", "peak_m_s2", "ln_peak", "used"], rows: dp.an.peaks.map(function (p) { return [+p.t.toFixed(3), +p.a.toFixed(5), +Math.log(p.a).toFixed(5), p.used ? 1 : 0]; }) };
  });
  OscApp.refresh.damped = function () {
    dTheory();
    if (!dp.rec) dRun(); else dRender();
    if (!dp.play) drawHangingSpring(Sim.$("#d-anim"), dp.rec ? dp.rec.x[0] : 0, 35 / Math.max(0.001, dVals().A), "");
  };
  if (preset.scenario) Sim.$("#d-scn").value = preset.scenario;
  dApplyScenario(Sim.$("#d-scn").value);
  dTheory();
})(window);
