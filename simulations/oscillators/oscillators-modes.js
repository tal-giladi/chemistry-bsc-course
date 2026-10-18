/* oscillators simulation, part 2: three coupled masses and the normal modes of CO2, then the tab
 * set-up. Needs oscillators.js (global OscApp) and ../common/sim.js (global Sim).
 *
 * Coupled masses (lesson 14.3): M x'' = -K x, normal modes from K v = w^2 M v.
 *   walls: K = k [[2,-1,0],[-1,2,-1],[0,-1,2]] -> w/sqrt(k/m) = 0.765, 1.414, 1.848
 *   free:  K = k [[1,-1,0],[-1,2,-1],[0,-1,1]] -> 0, 1, sqrt(3)
 *   pendulums: K = diag(m g/L) + kappa [[1,-1,0],[-1,2,-1],[0,-1,1]] -> w^2 = g/L + c (0, 1, 3)
 * CO2 (lesson 14.4): valence force field V = 1/2 k (s1^2 + s2^2) + k12 s1 s2 + 1/2 kd delta^2,
 *   w1^2 = (k + k12)/mO, w3^2 = (k - k12)(1/mO + 2/mC), w2^2 = 2 kd/(mO r^2) (1 + 2 mO/mC).
 *   Fundamentals 1333 (unperturbed), 667, 2349 cm^-1 from NIST CCCBDB; 13C16O2 nu3 2282.4 cm^-1 in
 *   CO2 ice (SSHADE). Masses 12C 12.0000, 13C 13.0034, 16O 15.9949, 18O 17.9992 u (NIST).
 *   Defaults k = 1547 N/m, k12 = 128 N/m, kd = 0.769 aJ/rad^2, r = 1.16 angstrom (lesson 14.4).
 */
(function () {
  "use strict";
  var A = window.OscApp, S = Sim.stats, TAU = 2 * Math.PI, G_LOCAL = 9.795;
  var U = Sim.C.u, C_CM = Sim.C.c * 100, CM1_KJMOL = Sim.C.h * C_CM * Sim.C.NA / 1000;

  /* ======================= COUPLED MASSES ======================= */
  var cp = { seed: A.seed0 + 2, rng: Sim.rng(A.seed0 + 2), modes: null, x0: [0, 0, 0], c: [0, 0, 0], t: 0, running: false, loop: null, readings: [], startKind: "1" };
  var cPlot = Sim.plot(Sim.$("#c-plot"), { xLabel: "time / s", yLabel: "displacement / cm (offset)" });

  function cVals() {
    function n(id) { return parseFloat(Sim.$(id).value); }
    return { cfg: Sim.$("#c-cfg").value, m: n("#c-m"), m2: n("#c-m2"), k: n("#c-k"), L: n("#c-L"), kap: n("#c-kap") };
  }
  function cMatrix(v) {
    var m = [v.m, v.m2, v.m];
    if (v.cfg === "walls") return { m: m, K: [[2 * v.k, -v.k, 0], [-v.k, 2 * v.k, -v.k], [0, -v.k, 2 * v.k]] };
    if (v.cfg === "free") return { m: m, K: [[v.k, -v.k, 0], [-v.k, 2 * v.k, -v.k], [0, -v.k, v.k]] };
    var g = G_LOCAL / v.L;
    return { m: m, K: [[m[0] * g + v.kap, -v.kap, 0], [-v.kap, m[1] * g + 2 * v.kap, -v.kap], [0, -v.kap, m[2] * g + v.kap]] };
  }
  function cShowFields() {
    var cfg = Sim.$("#c-cfg").value;
    Sim.$("#c-k-f").hidden = cfg === "pend";
    Sim.$("#c-L-f").hidden = cfg !== "pend";
    Sim.$("#c-kap-f").hidden = cfg !== "pend";
  }
  function shapeText(v) { return "(" + v.map(function (c) { return (Math.abs(c) < 1e-9 ? 0 : c).toFixed(3); }).join(", ") + ")"; }

  function cSolve() {
    var v = cVals();
    if (!(v.m > 0 && v.m2 > 0 && (v.cfg === "pend" ? v.L > 0 && v.kap >= 0 : v.k > 0))) return false;
    var mk = cMatrix(v);
    cp.modes = A.normalModes(mk.K, mk.m);
    cp.mass = mk.m;
    var tb = Sim.$("#c-modes tbody");
    tb.textContent = "";
    var ref = v.cfg === "pend" ? null : Math.sqrt(v.k / v.m);
    Sim.$("#c-modes thead th:nth-child(4)").textContent = v.cfg === "pend" ? "λ = (ω² − g/L)/c" : "ω/√(k/m)";
    cp.modes.forEach(function (md, i) {
      var col4 = ref ? (md.w / ref).toFixed(4) : (v.kap > 0 ? ((md.w2 - G_LOCAL / v.L) / (v.kap / v.m)).toFixed(3) : "—");
      tb.appendChild(A.tr([i + 1, md.w.toFixed(3), (md.w / TAU).toFixed(3), col4, shapeText(md.v)]));
    });
    var extra = [];
    var w1 = cp.modes[0].w, w2 = cp.modes[1].w;
    if (w1 === 0) extra.push(["Mode 1", "ω = 0: the whole chain slides (a translation, not a vibration)"]);
    if (w2 > w1 && w1 > 0) extra.push(["First energy transfer after releasing mass 1, π/(ω₂ − ω₁)", (Math.PI / (w2 - w1)).toFixed(1) + " s"]);
    if (v.cfg === "pend") extra.push(["g/L and c = κ/m", (G_LOCAL / v.L).toFixed(3) + " s⁻² and " + (v.kap / v.m).toFixed(3) + " s⁻²"]);
    if (v.cfg !== "pend") extra.push(["A single mass on one spring k", (Math.sqrt(v.k / v.m) / TAU).toFixed(3) + " Hz"]);
    A.kv(Sim.$("#c-extra"), extra);
    Sim.$("#c-seed").textContent = cp.seed;
    return true;
  }

  function cSetStart() {
    if (!cp.modes) return;
    var kind = Sim.$("#c-start").value, hand = Sim.$("#c-hand").checked, amp = 0.02, rng = cp.rng;
    var x0;
    if (kind === "m1") x0 = [amp, 0, 0];
    else x0 = cp.modes[parseInt(kind, 10) - 1].v.map(function (c) { return amp * c; });
    if (hand) x0 = x0.map(function (x) { return x + rng.normal(0, 0.05 * amp); });
    cp.x0 = x0; cp.startKind = kind;
    // modal coefficients c_k = (v_k^T M x0) / (v_k^T M v_k)
    var m = cp.mass;
    cp.c = cp.modes.map(function (md) {
      var num = 0, den = 0;
      for (var i = 0; i < 3; i++) { num += md.v[i] * m[i] * x0[i]; den += md.v[i] * m[i] * md.v[i]; }
      return num / den;
    });
  }
  function cX(t) {
    var x = [0, 0, 0];
    cp.modes.forEach(function (md, k) { for (var i = 0; i < 3; i++) x[i] += cp.c[k] * md.v[i] * Math.cos(md.w * t); });
    return x;
  }
  function cWindow() {
    var w = cp.modes ? cp.modes.filter(function (m) { return m.w > 0; }) : [];
    var Tbeat = 20;
    if (w.length >= 2) Tbeat = TAU / Math.max(1e-6, Math.abs(cp.modes[1].w - cp.modes[0].w || cp.modes[2].w - cp.modes[1].w));
    return Math.min(120, Math.max(10, Tbeat * 1.2));
  }

  function cDrawAnim(x) {
    var c = A.canvas2d(Sim.$("#c-anim")), ctx = c.ctx, W = c.W, H = c.H, v = cVals();
    var scale = Math.min(W / 6, 90) / 0.03;  // px per m
    ctx.lineWidth = 1.5;
    ctx.font = "11px " + (getComputedStyle(document.body).fontFamily || "sans-serif");
    ctx.textAlign = "center";
    var xs = [W * 0.25, W * 0.5, W * 0.75];
    if (v.cfg === "pend") {
      var top = 14, bob = H - 34, bandY = top + (bob - top) * 0.3;
      ctx.fillStyle = Sim.color("muted"); ctx.fillRect(W * 0.12, top - 6, W * 0.76, 6);
      var bx = xs.map(function (x0, i) { return x0 + x[i] * scale; });
      ctx.strokeStyle = Sim.color("ink");
      for (var i = 0; i < 3; i++) { ctx.beginPath(); ctx.moveTo(xs[i], top); ctx.lineTo(bx[i], bob); ctx.stroke(); }
      ctx.strokeStyle = Sim.color("s2");
      for (i = 0; i < 2; i++) {
        var f = 0.3;
        A.zigzag(ctx, xs[i] + (bx[i] - xs[i]) * f, bandY, xs[i + 1] + (bx[i + 1] - xs[i + 1]) * f, bandY, 5, 4);
      }
      for (i = 0; i < 3; i++) {
        ctx.fillStyle = Sim.color(i === 1 ? "s4" : "s1");
        var r = 10 * Math.cbrt(cp.mass[i] / 0.1);
        ctx.beginPath(); ctx.arc(bx[i], bob, Math.min(18, r), 0, TAU); ctx.fill();
        ctx.fillStyle = Sim.color("muted"); ctx.fillText(String(i + 1), xs[i], H - 6);
      }
      return;
    }
    var y = H * 0.5, walls = v.cfg === "walls";
    var pos = xs.map(function (x0, i) { return x0 + x[i] * scale; });
    ctx.fillStyle = Sim.color("muted");
    if (walls) { ctx.fillRect(4, y - 40, 8, 80); ctx.fillRect(W - 12, y - 40, 8, 80); }
    ctx.strokeStyle = Sim.color("ink");
    var half = pos.map(function (p, i) { return 12 * Math.cbrt(cp.mass[i] / 0.1); });
    if (walls) A.zigzag(ctx, 12, y, pos[0] - half[0], y, 6, 7);
    A.zigzag(ctx, pos[0] + half[0], y, pos[1] - half[1], y, 6, 7);
    A.zigzag(ctx, pos[1] + half[1], y, pos[2] - half[2], y, 6, 7);
    if (walls) A.zigzag(ctx, pos[2] + half[2], y, W - 12, y, 6, 7);
    pos.forEach(function (p, i) {
      ctx.fillStyle = Sim.color(i === 1 ? "s4" : "s1");
      ctx.fillRect(p - half[i], y - half[i], 2 * half[i], 2 * half[i]);
      ctx.fillStyle = Sim.color("muted"); ctx.fillText(String(i + 1), xs[i], H - 8);
    });
  }

  function cDrawPlot() {
    if (!cp.modes) return;
    var T = cWindow(), n = 600, d1 = [], d2 = [], d3 = [];
    var amp = 100 * Math.max(Math.abs(cp.x0[0]), Math.abs(cp.x0[1]), Math.abs(cp.x0[2]), 0.005), off = 2.6 * amp;
    for (var i = 0; i <= n; i++) {
      var t = T * i / n, x = cX(t);
      d1.push([t, 100 * x[0] + off]); d2.push([t, 100 * x[1]]); d3.push([t, 100 * x[2] - off]);
    }
    var ser = [
      { data: d1, color: "s1", width: 1.3, label: "mass 1 (shifted up)" },
      { data: d2, color: "s4", width: 1.3, label: "mass 2" },
      { data: d3, color: "s3", width: 1.3, label: "mass 3 (shifted down)" }
    ];
    if (cp.running || cp.t > 0) ser.push({ type: "vline", x: cp.t % T, color: "muted", width: 1, dash: [3, 3] });
    cPlot.draw(ser, { xMin: 0, xMax: T, yMin: -2 * off, yMax: 2 * off });
  }

  function cRelease() {
    if (cp.loop) { cp.loop.stop(); cp.loop = null; }
    if (cp.running) { cp.running = false; Sim.$("#c-go").textContent = "Release"; return; }
    if (!cSolve()) return;
    cSetStart();
    cp.t = 0; cp.running = true;
    Sim.$("#c-go").textContent = "Stop";
    var frame = 0;
    cp.loop = Sim.loop(function (dt) {
      if (!cp.running) return false;
      cp.t += dt;
      if (!Sim.$("#tab-coupled").hidden) {
        cDrawAnim(cX(cp.t));
        if (frame++ % 6 === 0) cDrawPlot();
      }
      return true;
    });
    cDrawPlot();
  }

  function cTime10() {
    if (!cSolve()) return;
    var kind = Sim.$("#c-start").value, log = Sim.$("#c-log");
    if (kind === "m1") { A.setLog(log, "Not a pure mode: when one mass is pulled the swing changes from cycle to cycle, so 10 swings have no single period. Release in a mode shape."); return; }
    var k = parseInt(kind, 10), md = cp.modes[k - 1];
    if (md.w === 0) { A.setLog(log, "Mode " + k + " has ω = 0: the chain slides away, nothing swings."); return; }
    var hand = Sim.$("#c-hand").checked;
    var sd = 0.07 * (hand && k === 3 ? 1.8 : 1);
    var t10 = Math.round((10 * TAU / md.w + cp.rng.normal(0, sd)) * 100) / 100;
    var trial = 1;
    cp.readings.forEach(function (r) { if (r.mode === k) trial++; });
    cp.readings.push({ mode: k, trial: trial, t10: t10, cfg: cVals().cfg });
    A.setLog(log, "Mode " + k + ", trial " + trial + ": 10 swings in " + t10.toFixed(2) + " s");
    cRender();
  }

  function cRender() {
    var tb = Sim.$("#c-table tbody"), v = cVals();
    tb.textContent = "";
    cp.readings.forEach(function (r, i) {
      var w = TAU * 10 / r.t10;
      tb.appendChild(A.tr([i + 1, r.mode, r.trial, r.t10.toFixed(2), (w * w).toFixed(3)]));
    });
    var rows = [], same = cp.readings.filter(function (r) { return r.cfg === v.cfg; });
    var byMode = [1, 2, 3].map(function (k) { return same.filter(function (r) { return r.mode === k; }).map(function (r) { return TAU * 10 / r.t10; }); });
    byMode.forEach(function (ws, i) {
      if (!ws.length) return;
      var f = ws.map(function (w) { return w / TAU; }), mean = S.mean(f), u = ws.length > 1 ? S.sd(f) / Math.sqrt(ws.length) : NaN;
      var pred = cp.modes ? cp.modes[i].w / TAU : NaN;
      rows.push(["Mode " + (i + 1) + " measured f", (isFinite(u) ? Sim.fmtU(mean, u, "Hz") : mean.toFixed(3) + " Hz") + " (model " + pred.toFixed(3) + " Hz)"]);
    });
    if (v.cfg === "pend") {
      var lam = { 1: 0, 2: 1, 3: 3 }, xs = [], ys = [];
      same.forEach(function (r) { var w = TAU * 10 / r.t10; xs.push(lam[r.mode]); ys.push(w * w); });
      var distinct = {};
      xs.forEach(function (x) { distinct[x] = 1; });
      if (Object.keys(distinct).length >= 2) {
        var f = S.linfit(xs, ys);
        rows.push(["Fit ω² = g/L + cλ: g/L", Sim.fmtU(f.a, f.ua, "s⁻²")]);
        rows.push(["c", Sim.fmtU(f.b, f.ub, "s⁻²")]);
        rows.push(["L from g/L (g = 9.795)", (G_LOCAL / f.a).toFixed(3) + " m (set " + v.L.toFixed(3) + " m)"]);
        var res = [0, 1, 3].map(function (l, i) {
          var ws = byMode[i];
          if (!ws.length) return null;
          return (S.mean(ws.map(function (w) { return w * w; })) - (f.a + f.b * l)).toFixed(3);
        }).filter(function (x) { return x !== null; });
        rows.push(["Residuals of the mode means", res.join(", ") + " s⁻²"]);
      } else rows.push(["Fit ω² = g/L + cλ", "time at least two different modes"]);
    }
    A.kv(Sim.$("#c-analysis"), rows);
  }

  function cRefresh() {
    cShowFields();
    if (!cSolve()) return;
    cSetStart();
    if (!cp.running) cp.t = 0;
    cDrawAnim(cp.running ? cX(cp.t) : cp.x0);
    cDrawPlot();
    cRender();
  }

  ["#c-cfg", "#c-m", "#c-m2", "#c-k", "#c-L", "#c-kap", "#c-start", "#c-hand"].forEach(function (id) {
    Sim.$(id).addEventListener("input", cRefresh);
    Sim.$(id).addEventListener("change", cRefresh);
  });
  Sim.$("#c-go").addEventListener("click", cRelease);
  Sim.$("#c-time10").addEventListener("click", cTime10);
  Sim.$("#c-clear").addEventListener("click", function () { cp.readings = []; cRender(); });
  Sim.$("#c-rerun").addEventListener("click", function () {
    cp.seed = Sim.newSeed(cp.seed); cp.rng = Sim.rng(cp.seed); cRefresh();
    A.setLog(Sim.$("#c-log"), "New seed " + cp.seed + ".");
  });
  Sim.exportCSV(Sim.$("#c-x"), "my_pendulums.csv", function () {
    return { header: ["mode", "trial", "t10_s"], rows: cp.readings.map(function (r) { return [r.mode, r.trial, r.t10]; }) };
  });
  Sim.exportCSV(Sim.$("#c-x-tr"), "coupled_displacements.csv", function () {
    if (!cp.modes) return null;
    var T = cWindow(), rows = [];
    for (var t = 0; t <= T + 1e-9; t += 0.05) { var x = cX(t); rows.push([+t.toFixed(2), +(100 * x[0]).toFixed(4), +(100 * x[1]).toFixed(4), +(100 * x[2]).toFixed(4)]); }
    return { header: ["t_s", "x1_cm", "x2_cm", "x3_cm"], rows: rows };
  });
  A.refresh.coupled = cRefresh;

  /* ======================= CO2 NORMAL MODES ======================= */
  var MEAS = { "12.0000|15.9949": [1333, 667, 2349], "13.0034|15.9949": [null, null, 2282.4] };
  var op = { mode: 1, phase: 0, running: false, loop: null, rec: [] };
  var oSpec = Sim.plot(Sim.$("#o-spec"), { xLabel: "wavenumber / cm⁻¹", yLabel: "relative intensity", yMin: 0, yMax: 1.15, xMin: 400, xMax: 2600, legendLeft: true });

  function oVals() {
    function n(id) { return parseFloat(Sim.$(id).value); }
    return { mC: n("#o-mC"), mO: n("#o-mO"), k: n("#o-k"), k12: n("#o-k12"), kd: n("#o-kd"), r: n("#o-r") };
  }
  function nu(w2) { return w2 > 0 ? Math.sqrt(w2) / (TAU * C_CM) : NaN; }
  function oCompute(v) {
    var mO = v.mO * U, mC = v.mC * U, r = v.r * 1e-10, kd = v.kd * 1e-18;
    var w1 = (v.k + v.k12) / mO, w3 = (v.k - v.k12) * (1 / mO + 2 / mC);
    var w2 = 2 * kd / (mO * r * r) * (1 + 2 * mO / mC);
    // the same stretches from the 3 x 3 eigenproblem (k12 enters as k12 * d2(s1 s2)/dx_i dx_j)
    var k = v.k, q = v.k12;
    var K = [[k, -k + q, -q], [-k + q, 2 * k - 2 * q, -k + q], [-q, -k + q, k]];
    var modes = A.normalModes(K, [mO, mC, mO]);
    var asym = -2 * mO / mC, n3 = Math.max(1, Math.abs(asym));
    return {
      nu1: nu(w1), nu2: nu(w2), nu3: nu(w3), eig: modes.map(function (m) { return nu(m.w2); }),
      shape1: [-1, 0, 1], shape3: [1 / n3, asym / n3, 1 / n3]
    };
  }
  function dipole(shape) { return -shape[0] + 2 * shape[1] - shape[2]; }

  function oRender() {
    var v = oVals(), o = oCompute(v), meas = MEAS[v.mC.toFixed(4) + "|" + v.mO.toFixed(4)] || [null, null, null];
    var tb = Sim.$("#o-modes tbody");
    tb.textContent = "";
    var rows = [
      ["ν₁ symmetric stretch", o.nu1, meas[0], o.shape1, dipole(o.shape1), "Raman"],
      ["ν₂ bend (×2, degenerate)", o.nu2, meas[1], o.shape3, dipole(o.shape3), "IR"],
      ["ν₃ antisymmetric stretch", o.nu3, meas[2], o.shape3, dipole(o.shape3), "IR"]
    ];
    rows.forEach(function (r, i) {
      var shape = shapeText(r[3]) + (i === 1 ? " sideways" : " along");
      var dm = Math.abs(r[4]) < 1e-9 ? "0 (inactive)" : r[4].toFixed(3) + " q";
      var mtxt = r[2] ? r[2] + (isFinite(r[1]) ? " (" + (r[1] - r[2] >= 0 ? "+" : "") + (r[1] - r[2]).toFixed(1) + ")" : "") : "—";
      tb.appendChild(A.tr([r[0], isFinite(r[1]) ? r[1].toFixed(1) : "unstable", mtxt, shape, dm, r[5]]));
    });
    var zpe = 0.5 * (o.nu1 + 2 * o.nu2 + o.nu3);
    A.kv(Sim.$("#o-extra"), [
      ["Ratio ν₃/ν₁", isFinite(o.nu3 / o.nu1) ? (o.nu3 / o.nu1).toFixed(3) + " (measured 2349/1333 = 1.762; one constant: " + Math.sqrt(1 + 2 * v.mO / v.mC).toFixed(3) + ")" : "—"],
      ["3N − 5 vibrations", "4 (ν₁, two ν₂, ν₃)"],
      ["Zero-point energy ½(ν₁ + 2ν₂ + ν₃)", isFinite(zpe) ? zpe.toFixed(0) + " cm⁻¹ = " + (zpe * CM1_KJMOL).toFixed(1) + " kJ/mol" : "—"],
      ["IR bands as wavelengths", isFinite(o.nu2) && isFinite(o.nu3) ? (1e4 / o.nu2).toFixed(2) + " µm (bend), " + (1e4 / o.nu3).toFixed(2) + " µm (ν₃)" : "—"],
      ["Check: 3 × 3 eigenproblem (stretches)", o.eig.map(function (x) { return isFinite(x) ? x.toFixed(1) : "0"; }).join(", ") + " cm⁻¹"]
    ]);
    var ser = [];
    function stick(x, h, color, dash, label) { if (isFinite(x)) ser.push({ data: [[x, 0], [x, h]], color: color, width: 3, dash: dash, label: label }); }
    stick(o.nu3, 1.0, "s2", null, "model, IR");
    stick(o.nu2, 0.45, "s2", null);
    stick(o.nu1, 0.6, "s4", [4, 3], "model, Raman only");
    var mm = MEAS["12.0000|15.9949"];
    mm.forEach(function (x, i) { ser.push({ type: "vline", x: x, color: "muted", width: 1, dash: [2, 3], label: i === 0 ? "measured ¹²C¹⁶O₂" : undefined }); });
    oSpec.draw(ser);
  }

  function oDraw() {
    var c = A.canvas2d(Sim.$("#o-anim")), ctx = c.ctx, W = c.W, H = c.H, v = oVals(), o = oCompute(v);
    var mode = parseInt(Sim.$("#o-mode").value, 10), s = Math.sin(op.phase), amp = Math.min(W * 0.06, 26);
    var shape = mode === 1 ? o.shape1 : o.shape3;
    var bx = [W * 0.28, W * 0.5, W * 0.72], y = H * 0.48;
    var px = bx.slice(), py = [y, y, y];
    for (var i = 0; i < 3; i++) {
      if (mode === 2) py[i] = y - amp * shape[i] * s;
      else px[i] = bx[i] + amp * shape[i] * s;
    }
    ctx.strokeStyle = Sim.color("muted"); ctx.lineWidth = 4;
    ctx.beginPath(); ctx.moveTo(px[0], py[0]); ctx.lineTo(px[1], py[1]); ctx.lineTo(px[2], py[2]); ctx.stroke();
    var rad = [16, 13 * Math.cbrt(v.mC / 12), 16];
    ["s2", "ink", "s2"].forEach(function (col, j) {
      ctx.fillStyle = Sim.color(col);
      ctx.beginPath(); ctx.arc(px[j], py[j], rad[j], 0, TAU); ctx.fill();
    });
    ctx.fillStyle = Sim.color("plot-bg");
    ctx.font = "bold 12px " + (getComputedStyle(document.body).fontFamily || "sans-serif");
    ctx.textAlign = "center"; ctx.textBaseline = "middle";
    ctx.fillText("O", px[0], py[0]); ctx.fillText("C", px[1], py[1]); ctx.fillText("O", px[2], py[2]);
    // dipole moment with charges -q, +2q, -q relative to the resting positions
    var dx = -(px[0] - bx[0]) + 2 * (px[1] - bx[1]) - (px[2] - bx[2]);
    var dy = -(py[0] - y) + 2 * (py[1] - y) - (py[2] - y);
    ctx.strokeStyle = Sim.color("s3"); ctx.fillStyle = Sim.color("s3"); ctx.lineWidth = 2.5;
    var ax = W * 0.5, ay = H - 26, L = 0.9;
    ctx.beginPath(); ctx.moveTo(ax, ay); ctx.lineTo(ax + dx * L, ay - dy * L); ctx.stroke();
    ctx.font = "11px " + (getComputedStyle(document.body).fontFamily || "sans-serif");
    ctx.textBaseline = "alphabetic";
    var mag = Math.sqrt(dx * dx + dy * dy);
    ctx.fillText(mode === 1 ? "dipole moment: always zero (IR inactive)" : "dipole moment oscillates (IR active)", W / 2, H - 6);
    if (mag > 1) { ctx.beginPath(); ctx.arc(ax + dx * L, ay - dy * L, 3, 0, TAU); ctx.fill(); }
    ctx.fillStyle = Sim.color("muted"); ctx.textAlign = "left";
    var nuv = mode === 1 ? o.nu1 : mode === 2 ? o.nu2 : o.nu3;
    ctx.fillText((mode === 1 ? "ν₁ " : mode === 2 ? "ν₂ " : "ν₃ ") + (isFinite(nuv) ? nuv.toFixed(0) + " cm⁻¹" : ""), 8, 16);
  }

  function oStart() {
    if (op.loop) { op.loop.stop(); op.loop = null; }
    if (op.running) { op.running = false; Sim.$("#o-go").textContent = "Start"; return; }
    op.running = true; Sim.$("#o-go").textContent = "Stop";
    op.loop = Sim.loop(function (dt) {
      if (!op.running) return false;
      var v = oVals(), o = oCompute(v), mode = parseInt(Sim.$("#o-mode").value, 10);
      var nuv = mode === 1 ? o.nu1 : mode === 2 ? o.nu2 : o.nu3;
      op.phase += dt * TAU * 0.9 * (isFinite(nuv) ? nuv / 2349 : 0);
      if (!Sim.$("#tab-co2").hidden) oDraw();
      return true;
    });
  }

  function fitMain(two) {
    var mO = 15.9949 * U, mC = 12.0000 * U;
    var w1 = Math.pow(TAU * C_CM * 1333, 2), w2 = Math.pow(TAU * C_CM * 667, 2), w3 = Math.pow(TAU * C_CM * 2349, 2);
    var d = w3 / (1 / mO + 2 / mC);
    if (two) {
      var s = mO * w1;
      Sim.$("#o-k").value = ((s + d) / 2).toFixed(0);
      Sim.$("#o-k12").value = ((s - d) / 2).toFixed(0);
    } else {
      Sim.$("#o-k").value = d.toFixed(0);
      Sim.$("#o-k12").value = "0";
    }
    var r = parseFloat(Sim.$("#o-r").value) * 1e-10;
    Sim.$("#o-kd").value = (w2 * r * r * mO / (2 * (1 + 2 * mO / mC)) * 1e18).toFixed(3);
    oRender(); oDraw();
  }

  function oRecord() {
    var v = oVals(), o = oCompute(v);
    var name = (v.mC > 12.5 ? "¹³C" : "¹²C") + (v.mO > 17 ? "¹⁸O₂" : "¹⁶O₂");
    op.rec.push([name, v.k, v.k12, v.kd, +o.nu1.toFixed(1), +o.nu2.toFixed(1), +o.nu3.toFixed(1), +(o.nu3 / o.nu1).toFixed(4)]);
    var tb = Sim.$("#o-table tbody");
    tb.textContent = "";
    op.rec.forEach(function (r, i) { tb.appendChild(A.tr([i + 1].concat(r))); });
  }

  ["#o-mC", "#o-mO", "#o-k", "#o-k12", "#o-kd", "#o-r", "#o-mode"].forEach(function (id) {
    Sim.$(id).addEventListener("input", function () { oRender(); oDraw(); });
    Sim.$(id).addEventListener("change", function () { oRender(); oDraw(); });
  });
  Sim.$("#o-go").addEventListener("click", oStart);
  Sim.$("#o-fit1").addEventListener("click", function () { fitMain(false); });
  Sim.$("#o-fit2").addEventListener("click", function () { fitMain(true); });
  Sim.$("#o-k120").addEventListener("click", function () { Sim.$("#o-k12").value = "0"; oRender(); oDraw(); });
  Sim.$("#o-def").addEventListener("click", function () {
    Sim.$("#o-k").value = "1547"; Sim.$("#o-k12").value = "128"; Sim.$("#o-kd").value = "0.769"; Sim.$("#o-r").value = "1.16";
    oRender(); oDraw();
  });
  Sim.$("#o-rec").addEventListener("click", oRecord);
  Sim.$("#o-clear").addEventListener("click", function () { op.rec = []; Sim.$("#o-table tbody").textContent = ""; });
  Sim.exportCSV(Sim.$("#o-x"), "co2_predictions.csv", function () {
    return { header: ["molecule", "k_N_per_m", "k12_N_per_m", "kdelta_aJ_per_rad2", "nu1_cm", "nu2_cm", "nu3_cm", "nu3_over_nu1"], rows: op.rec };
  });
  A.refresh.co2 = function () { oRender(); oDraw(); };

  /* ======================= TABS ======================= */
  var tabs = Sim.tabs(Sim.$("#tabs"), function (name) {
    if (A.refresh[name]) A.refresh[name]();
  });
  Sim.onTheme(function () {
    if (!Sim.$("#tab-coupled").hidden) cRefresh();
    if (!Sim.$("#tab-co2").hidden) oDraw();
  });
  tabs.select(A.preset.tab || "single");
})();
