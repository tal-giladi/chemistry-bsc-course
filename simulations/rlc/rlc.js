/* rlc simulation: a DC resistor ladder measured with a 3½-digit multimeter (lesson 04.4) and a
 * series RLC resonance curve driven by a phone tone (lesson 14.6). Uses ../common/sim.js (Sim).
 *
 * DC: nodes P (battery +), A, B, N (battery -, reference). R1 P-A, R2 A-N, R3 A-B, R4 B-N.
 *   The battery is an EMF in series with its internal resistance r; the meter is part of the
 *   circuit (10 MOhm on volts, about 1 Ohm on the current range). With 3.00 V and the nominal
 *   220/470/330/1000 Ohm: V_A = 1.837 V, V_B = 1.381 V, I = 5.288 mA, R_eq = 567.3 Ohm.
 *   Cells: fresh AA alkaline about 1.58 V and 0.15 Ohm each (typical manufacturer data; lesson
 *   04.4 finds about 0.5 Ohm for a used cell); "tired" cells 1.45 V and 3 Ohm each (illustrative).
 * AC: Z = R + R_coil + R_core(f) + j(wL - 1/(wC)); H = V_R/V_in = A / sqrt(1 + Q^2 (f/f0 - f0/f)^2),
 *   A = R/R_tot, Q = sqrt(L/C)/R_tot, f0 = 1/(2 pi sqrt(LC)) (OpenStax University Physics 2, 15.5).
 *   Printed 10 mH, 1.0 uF, 10 Ohm, coil 28 Ohm -> f0 = 1592 Hz, Q = 2.6 (lesson 14.6).
 *   "Real parts": L and C drawn within about +/-5 %, a 1 % resistor, and coil losses that add
 *   about 5 Ohm at 1.6 kHz growing as sqrt(f) (an illustrative model of core and skin losses that
 *   reproduces the lesson's fitted R_tot of about 43 Ohm against 38 Ohm on the ohmmeter).
 *   Phone output: about 10 Ohm source resistance, level falling slowly with frequency.
 *   Meter: each AC range has its own gain error and high-frequency roll-off (illustrative values);
 *   reading noise 0.5 % rising above 3 kHz. The fit weights follow labs/module-14/lesson06_rlc.py.
 */
(function () {
  "use strict";
  var S = Sim.stats, TAU = 2 * Math.PI;

  var PRESETS = {
    dc: {
      title: "DC resistor network", tab: "dc",
      what: "Ohm's law V = IR and Kirchhoff's two rules (currents in = currents out at a node; voltages round a loop add to zero) predict every voltage in a network. A real battery has an internal resistance and sags under load; a real voltmeter has about 10 MΩ inside and barely disturbs the circuit; an ammeter has almost nothing inside and shorts whatever it is put across.",
      task: "With the lab supply at exactly 3.00 V and the nominal resistors, predict V<sub>A</sub> and V<sub>B</sub> before you read them, then read them. Then switch to two fresh AA cells and real 5 % resistors: measure each resistor alone, the network resistance unpowered, V<sub>s</sub> under load, V<sub>A</sub> and V<sub>B</sub>, and compare with predictions from your measured values.",
      target: "V<sub>A</sub> = 1.84 V, V<sub>B</sub> = 1.38 V and a battery current of 5.29 mA (R<sub>eq</sub> = 567 Ω); with real parts, predictions from measured values within about 1 % of the readings."
    },
    resonance: {
      title: "Resonance curve and Q", tab: "resonance",
      what: "In a series RLC circuit the inductor's and capacitor's reactances cancel at f₀ = 1/(2π√(LC)); there the impedance is just the total resistance and the current peaks. The width of the peak is f₀/Q with Q = √(L/C)/R<sub>tot</sub>. Measuring the ratio V<sub>R</sub>/V<sub>in</sub> on one meter range cancels the phone's and the meter's own frequency errors. The curve has the shape of a spectral line.",
      task: "With L = 10 mH, C = 1.0 µF and R<sub>tot</sub> = 38 Ω (10 Ω resistor + 28 Ω coil), read f₀ and Q. Then set the coil resistance to 0 so that R<sub>tot</sub> = 10 Ω. Finally tick <b>Real parts</b>, measure the 17 frequencies on the fixed 200 mV range, read the ohmmeter values with the plug out, and fit.",
      target: "f₀ = 1592 Hz and Q = 2.6; with R<sub>tot</sub> = 10 Ω, Q = 10 and a bandwidth of 159 Hz. With real parts the fit gives Q a little below 2.6 and R<sub>tot</sub> a few ohms above the ohmmeter's sum, with χ²/dof near 1."
    }
  };

  var preset = Sim.preset(PRESETS, "dc");
  var seed0 = Sim.seedFromQuery(4);
  Sim.label();
  Sim.presetBox(Sim.$("#preset"), preset);

  /* ---------- helpers ---------- */
  function canvas2d(canvas) {
    var dpr = window.devicePixelRatio || 1;
    var W = canvas.clientWidth || 300, H = canvas.clientHeight || 150;
    if (canvas.width !== Math.round(W * dpr) || canvas.height !== Math.round(H * dpr)) { canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr); }
    var ctx = canvas.getContext("2d");
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.fillStyle = Sim.color("plot-bg");
    ctx.fillRect(0, 0, W, H);
    ctx.font = "12px " + (getComputedStyle(document.body).fontFamily || "sans-serif");
    return { ctx: ctx, W: W, H: H };
  }
  function resistor(ctx, x1, y1, x2, y2, label) {
    var dx = x2 - x1, dy = y2 - y1, len = Math.sqrt(dx * dx + dy * dy), ux = dx / len, uy = dy / len, nx = -uy, ny = ux;
    var a = len * 0.3, b = len * 0.7, n = 6, w = 6;
    ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x1 + ux * a, y1 + uy * a);
    for (var i = 1; i <= n; i++) {
      var s = a + (b - a) * (i - 0.5) / n, side = (i % 2 ? 1 : -1) * w;
      ctx.lineTo(x1 + ux * s + nx * side, y1 + uy * s + ny * side);
    }
    ctx.lineTo(x1 + ux * b, y1 + uy * b); ctx.lineTo(x2, y2); ctx.stroke();
    if (label) {
      ctx.save(); ctx.fillStyle = Sim.color("ink"); ctx.textAlign = Math.abs(dy) > Math.abs(dx) ? "left" : "center";
      ctx.fillText(label, (x1 + x2) / 2 + (Math.abs(dy) > Math.abs(dx) ? 12 : 0), (y1 + y2) / 2 + (Math.abs(dy) > Math.abs(dx) ? 4 : -12));
      ctx.restore();
    }
  }
  function line(ctx, pts) { ctx.beginPath(); pts.forEach(function (p, i) { if (i) ctx.lineTo(p[0], p[1]); else ctx.moveTo(p[0], p[1]); }); ctx.stroke(); }
  function dot(ctx, x, y, r, color) { ctx.fillStyle = Sim.color(color); ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.fill(); }
  function tr(cells) { var row = Sim.el("tr"); cells.forEach(function (c) { row.appendChild(Sim.el("td", { html: String(c) })); }); return row; }
  function kv(el, pairs) { el.textContent = ""; pairs.forEach(function (p) { el.appendChild(Sim.el("span", { html: p[0] })); el.appendChild(Sim.el("span", { html: p[1] })); }); }
  function solve(M, b) {           // Gaussian elimination with partial pivoting
    var n = b.length, A = M.map(function (r, i) { return r.concat([b[i]]); });
    for (var c = 0; c < n; c++) {
      var p = c;
      for (var r = c + 1; r < n; r++) if (Math.abs(A[r][c]) > Math.abs(A[p][c])) p = r;
      var tmp = A[c]; A[c] = A[p]; A[p] = tmp;
      if (Math.abs(A[c][c]) < 1e-300) return null;
      for (r = c + 1; r < n; r++) { var f = A[r][c] / A[c][c]; for (var k = c; k <= n; k++) A[r][k] -= f * A[c][k]; }
    }
    var x = new Array(n);
    for (r = n - 1; r >= 0; r--) { var s = A[r][n]; for (k = r + 1; k < n; k++) s -= A[r][k] * x[k]; x[r] = s / A[r][r]; }
    return x;
  }
  function invert(M) {
    var n = M.length, out = [];
    for (var j = 0; j < n; j++) { var e = []; for (var i = 0; i < n; i++) e.push(i === j ? 1 : 0); out.push(solve(M, e)); }
    if (out.some(function (c) { return !c; })) return null;
    return M.map(function (r, i) { return out.map(function (col) { return col[i]; }); });
  }

  /* ======================= DC NETWORK ======================= */
  var BATS = { ideal: { emf: 3.00, r: 0 }, fresh: { emf: 3.16, r: 0.30 }, tired: { emf: 2.90, r: 6.0 } };
  var NAMES = { P: "battery +", A: "node A", B: "node B", N: "battery −" };
  var dc = { seed: seed0, readings: [], fuse: true, last: null };

  function dcInit() {
    var rng = Sim.rng(dc.seed);
    dc.dev = [0, 1, 2, 3].map(function () { return Math.max(-0.05, Math.min(0.05, rng.normal(0, 0.02))); });
    dc.gain = { V: 1 + rng.normal(0, 0.0015), ohm: 1 + rng.normal(0, 0.0015), mA: 1 + rng.normal(0, 0.004) };
    dc.rng = Sim.rng(dc.seed + 101);
    Sim.$("#dc-seed").textContent = dc.seed;
  }
  function dcVals() {
    var nom = [1, 2, 3, 4].map(function (i) { return parseFloat(Sim.$("#dc-R" + i).value); });
    var tol = Sim.$("#dc-tol").checked;
    var act = nom.map(function (r, i) { return tol ? r * (1 + dc.dev[i]) : r; });
    var bat = BATS[Sim.$("#dc-bat").value];
    return { nom: nom, R: act, emf: bat.emf, r: bat.r, conn: Sim.$("#dc-conn").checked };
  }

  // node voltages [P, A, B] with N = 0. extra: {a, b, R} element between two nodes; inject: {a, b, I}
  function dcSolve(R, emf, r, conn, extra, inject) {
    var idx = { P: 0, A: 1, B: 2 }, G = [[0, 0, 0], [0, 0, 0], [0, 0, 0]], I = [0, 0, 0];
    function add(a, b, g) {
      var ia = a === "N" ? -1 : idx[a], ib = b === "N" ? -1 : idx[b];
      if (ia >= 0) G[ia][ia] += g;
      if (ib >= 0) G[ib][ib] += g;
      if (ia >= 0 && ib >= 0) { G[ia][ib] -= g; G[ib][ia] -= g; }
    }
    add("P", "A", 1 / R[0]); add("A", "N", 1 / R[1]); add("A", "B", 1 / R[2]); add("B", "N", 1 / R[3]);
    if (conn) { var gb = 1 / Math.max(r, 1e-6); add("P", "N", gb); I[0] += emf * gb; }
    if (extra && extra.a !== extra.b) add(extra.a, extra.b, 1 / extra.R);
    if (inject) {
      if (inject.a !== "N") I[idx[inject.a]] += inject.I;
      if (inject.b !== "N") I[idx[inject.b]] -= inject.I;
    }
    var v = solve(G, I);
    if (!v) return null;
    return { P: v[0], A: v[1], B: v[2], N: 0 };
  }
  function dcPredict(R, Vs) {       // ideal source Vs across P-N, no meter
    var v = dcSolve(R, Vs, 0, true, null, null);
    var I = (v.P - v.A) / R[0];
    return { VA: v.A, VB: v.B, I: I, Req: R[0] + R[1] * (R[2] + R[3]) / (R[1] + R[2] + R[3]), v: v };
  }

  // 3½-digit autoranging display: returns {text, value, unit, ol}
  function display(x, ranges, unit) {
    for (var i = 0; i < ranges.length; i++) {
      var rg = ranges[i];
      if (Math.abs(x) <= rg.max) {
        var counts = Math.round(x / rg.res + dc.rng.normal(0, 0.4));
        var val = counts * rg.res;
        return { text: val.toFixed(rg.dec), value: +val.toFixed(rg.dec), unit: rg.unit || unit, range: rg.name };
      }
    }
    return { text: "1 .", value: NaN, unit: unit, ol: true, range: "OL" };
  }
  var VR = [{ max: 0.1999, res: 0.0001, dec: 4, name: "200 mV" }, { max: 1.999, res: 0.001, dec: 3, name: "2 V" }, { max: 19.99, res: 0.01, dec: 2, name: "20 V" }];
  var OR = [{ max: 199.9, res: 0.1, dec: 1, name: "200 Ω" }, { max: 1999, res: 1, dec: 0, name: "2 kΩ" }, { max: 19990, res: 10, dec: 0, name: "20 kΩ" }, { max: 199900, res: 100, dec: 0, name: "200 kΩ" }, { max: 1999000, res: 1000, dec: 0, name: "2 MΩ" }, { max: 19990000, res: 10000, dec: 0, name: "20 MΩ" }];
  var AR = [{ max: 0.1999, res: 0.0001, dec: 4, name: "200 mA" }];

  function showDisplay(d, unit) {
    var el = Sim.$("#dc-display");
    el.textContent = d.text;
    el.classList.toggle("ol", !!d.ol);
    Sim.$("#dc-unit").textContent = d.ol ? "overload" : (unit + (d.range ? " (range " + d.range + ")" : ""));
  }

  function dcRead(outOfBoard) {
    var v = dcVals(), mode = Sim.$("#dc-mode").value, red = Sim.$("#dc-red").value, black = Sim.$("#dc-black").value, log = Sim.$("#dc-log");
    var d, unit, quantity, note = "";
    if (outOfBoard !== undefined) {
      var Rt = v.R[outOfBoard] * dc.gain.ohm;
      d = display(Rt, OR, "Ω"); unit = "Ω";
      showDisplay(d, unit);
      dc.readings.push({ fn: "Ω", red: "R" + (outOfBoard + 1) + " alone", black: "", conn: "—", d: d, unit: unit, q: "R" + (outOfBoard + 1) + "_ohm" });
      Sim.log(log, "R" + (outOfBoard + 1) + " out of the board: " + d.text + " Ω (printed " + v.nom[outOfBoard] + " Ω)");
      dcRender();
      return;
    }
    if (mode === "V") {
      var s = dcSolve(v.R, v.emf, v.r, v.conn, { a: red, b: black, R: 10e6 }, null);
      var x = (s[red] - s[black]) * dc.gain.V;
      d = display(x, VR, "V"); unit = "V";
      if (red === "P" && black === "N") quantity = "Vs_V";
      else if (red === "A" && black === "N") quantity = "VA_V";
      else if (red === "B" && black === "N") quantity = "VB_V";
      if (red === black) note = " (both probes on one point)";
      else if (d.value < 0) note = " (negative: the probes are the other way round)";
    } else if (mode === "ohm") {
      unit = "Ω";
      if (v.conn) {
        var junk = 100 + dc.rng.uniform(0, 900);
        d = { text: junk.toFixed(0), value: NaN, unit: "Ω", range: "?" };
        note = " — meaningless: the battery's current mixes with the ohmmeter's own. Disconnect the battery first.";
      } else if (red === black) {
        d = display(0.2, OR, "Ω");
      } else {
        var t = dcSolve(v.R, 0, 0, false, null, { a: red, b: black, I: 1e-3 });
        var Rm = (t[red] - t[black]) / 1e-3 * dc.gain.ohm;
        d = display(Rm, OR, "Ω");
        if ((red === "P" && black === "N") || (red === "N" && black === "P")) quantity = "Req_ohm";
      }
    } else {
      unit = "mA";
      if (!dc.fuse) { d = { text: "0.0", value: 0, unit: "mA", range: "fuse blown" }; note = " — no reading: the meter's fuse has blown."; }
      else {
        var sm = dcSolve(v.R, v.emf, v.r, v.conn, { a: red, b: black, R: 1.0 }, null);
        var Im = (sm[red] - sm[black]) / 1.0;
        if (Math.abs(Im) > 0.2) {
          dc.fuse = false;
          Sim.$("#dc-fuse").hidden = false;
          d = { text: "1 .", value: NaN, unit: "mA", ol: true, range: "OL" };
          note = " — SHORT CIRCUIT: about " + (Math.abs(Im) * 1000).toFixed(0) + " mA flowed through the meter, the fuse blew. With a bare wire the wire would get hot and the cell could leak.";
        } else {
          d = display(Im * dc.gain.mA, AR, "A");
          d.text = (d.value * 1000).toFixed(1); d.value = +(d.value * 1000).toFixed(1);
          note = Math.abs(Im) > 1e-6 ? " — the meter (about 1 Ω) is now a wire across " + NAMES[red] + " and " + NAMES[black] + ": it changed the circuit it measures." : "";
        }
      }
    }
    showDisplay(d, unit);
    dc.readings.push({ fn: mode === "V" ? "DC V" : mode === "ohm" ? "Ω" : "DC mA", red: NAMES[red], black: NAMES[black], conn: v.conn ? "connected" : "off", d: d, unit: unit, q: quantity });
    Sim.log(log, (mode === "V" ? "V" : mode === "ohm" ? "Ω" : "mA") + " " + NAMES[red] + " → " + NAMES[black] + ": " + d.text + " " + unit + note);
    dcRender();
  }

  function latest(q) {
    for (var i = dc.readings.length - 1; i >= 0; i--) if (dc.readings[i].q === q && isFinite(dc.readings[i].d.value)) return dc.readings[i].d.value;
    return NaN;
  }

  function dcRender() {
    var v = dcVals(), tb = Sim.$("#dc-table tbody");
    tb.textContent = "";
    dc.readings.forEach(function (r, i) { tb.appendChild(tr([i + 1, r.fn, r.red, r.black, r.conn, r.d.text + " " + r.unit])); });
    // predictions from nominal values
    var p = dcPredict(v.nom, 3.00);
    var rows = [
      ["Nominal values, V<sub>s</sub> = 3.00 V: R<sub>eq</sub> = R1 + R2 ∥ (R3 + R4)", p.Req.toFixed(1) + " Ω"],
      ["Battery current V<sub>s</sub>/R<sub>eq</sub>", (p.I * 1000).toFixed(2) + " mA"],
      ["V<sub>A</sub>, V<sub>B</sub>", p.VA.toFixed(3) + " V, " + p.VB.toFixed(3) + " V"]
    ];
    var pw = [0, 1, 2, 3].map(function (i) {
      var nodes = [["P", "A"], ["A", "N"], ["A", "B"], ["B", "N"]][i];
      var dv = p.v[nodes[0]] - p.v[nodes[1]];
      return dv * dv / v.nom[i];
    });
    rows.push(["Power in R1…R4 (rating 250 mW)", pw.map(function (x) { return (x * 1000).toFixed(2); }).join(", ") + " mW" + (Math.max.apply(null, pw) > 0.25 ? " <span class=\"bad\">— over the rating: it would get hot</span>" : "")]);
    var mR = [1, 2, 3, 4].map(function (i) { return latest("R" + i + "_ohm"); }), mVs = latest("Vs_V");
    if (mR.every(isFinite) && isFinite(mVs)) {
      var q = dcPredict(mR, mVs);
      rows.push(["From your measured R and V<sub>s</sub> = " + mVs.toFixed(3) + " V", "V<sub>A</sub> = " + q.VA.toFixed(3) + " V, V<sub>B</sub> = " + q.VB.toFixed(3) + " V, I = " + (q.I * 1000).toFixed(2) + " mA"]);
    } else rows.push(["From measured values", "measure R1–R4 alone and V<sub>s</sub> (red on battery +, black on battery −) to get a prediction from your own numbers"]);
    kv(Sim.$("#dc-pred"), rows);
    var chk = [], mA = latest("VA_V"), mB = latest("VB_V");
    if (mR.every(isFinite) && isFinite(mVs) && isFinite(mA)) {
      var q2 = dcPredict(mR, mVs);
      chk.push(["V<sub>A</sub> measured − predicted", ((mA - q2.VA) * 1000).toFixed(1) + " mV (" + (100 * (mA - q2.VA) / q2.VA).toFixed(2) + " %)"]);
      if (isFinite(mB)) chk.push(["V<sub>B</sub> measured − predicted", ((mB - q2.VB) * 1000).toFixed(1) + " mV (" + (100 * (mB - q2.VB) / q2.VB).toFixed(2) + " %)"]);
    }
    if (isFinite(mA)) {
      var pn = dcPredict(v.nom, 3.00);
      chk.push(["V<sub>A</sub> against the nominal prediction", (100 * (mA - pn.VA) / pn.VA).toFixed(2) + " %"]);
    }
    kv(Sim.$("#dc-check"), chk);
    dcDraw();
  }

  function dcDraw() {
    var c = canvas2d(Sim.$("#dc-circ")), ctx = c.ctx, W = c.W, H = c.H, v = dcVals();
    var x0 = 40, xA = W * 0.48, xB = W * 0.85, yT = 40, yB = H - 34;
    var pts = { P: [x0, yT], A: [xA, yT], B: [xB, yT], N: [x0, yB] };
    ctx.strokeStyle = Sim.color("ink"); ctx.lineWidth = 1.6;
    // battery: two cells drawn as long/short plates in the left wire
    var ym = (yT + yB) / 2;
    line(ctx, [[x0, yT], [x0, ym - 12]]); line(ctx, [[x0, ym + 12], [x0, yB]]);
    ctx.lineWidth = 2.5; line(ctx, [[x0 - 14, ym - 12], [x0 + 14, ym - 12]]); line(ctx, [[x0 - 7, ym - 4], [x0 + 7, ym - 4]]);
    line(ctx, [[x0 - 14, ym + 4], [x0 + 14, ym + 4]]); line(ctx, [[x0 - 7, ym + 12], [x0 + 7, ym + 12]]);
    ctx.lineWidth = 1.6;
    if (!v.conn) { ctx.clearRect(x0 - 3, yT + 6, 6, 14); ctx.fillStyle = Sim.color("plot-bg"); ctx.fillRect(x0 - 3, yT + 6, 6, 14); }
    resistor(ctx, x0, yT, xA, yT, "R1 " + v.nom[0] + " Ω");
    resistor(ctx, xA, yT, xA, yB, "R2 " + v.nom[1] + " Ω");
    resistor(ctx, xA, yT, xB, yT, "R3 " + v.nom[2] + " Ω");
    resistor(ctx, xB, yT, xB, yB, "R4 " + v.nom[3] + " Ω");
    line(ctx, [[x0, yB], [xB, yB]]);
    ctx.fillStyle = Sim.color("ink");
    ctx.textAlign = "left";
    ctx.fillText(v.conn ? "+" : "+ (off)", x0 - 30, ym - 16);
    ctx.fillText("−", x0 - 26, ym + 24);
    ctx.textAlign = "center";
    ctx.fillText("A", xA, yT - 10); ctx.fillText("B", xB, yT - 10);
    dot(ctx, xA, yT, 3, "ink"); dot(ctx, xB, yT, 3, "ink");
    var red = Sim.$("#dc-red").value, black = Sim.$("#dc-black").value;
    dot(ctx, pts[black][0] + 6, pts[black][1] + 6, 6, "ink");
    dot(ctx, pts[red][0] - 6, pts[red][1] + 6, 6, "bad");
    ctx.fillStyle = Sim.color("muted"); ctx.textAlign = "left";
    ctx.fillText("red / black dots: meter probes", 8, H - 8);
  }

  ["#dc-bat", "#dc-tol", "#dc-R1", "#dc-R2", "#dc-R3", "#dc-R4", "#dc-conn", "#dc-mode", "#dc-red", "#dc-black"].forEach(function (id) {
    Sim.$(id).addEventListener("change", dcRender);
    Sim.$(id).addEventListener("input", dcRender);
  });
  Sim.$("#dc-read").addEventListener("click", function () { dcRead(); });
  [1, 2, 3, 4].forEach(function (i) { Sim.$("#dc-o" + i).addEventListener("click", function () { dcRead(i - 1); }); });
  Sim.$("#dc-fuse").addEventListener("click", function () { dc.fuse = true; Sim.$("#dc-fuse").hidden = true; Sim.log(Sim.$("#dc-log"), "New fuse fitted. Measure currents by measuring a voltage across a known resistor instead."); });
  Sim.$("#dc-clear").addEventListener("click", function () { dc.readings = []; dcRender(); });
  Sim.$("#dc-rerun").addEventListener("click", function () { dc.seed = Sim.newSeed(dc.seed); dcInit(); dc.readings = []; dcRender(); Sim.log(Sim.$("#dc-log"), "New seed " + dc.seed + ": new resistors and a new meter."); });
  Sim.exportCSV(Sim.$("#dc-x"), "my_network.csv", function () {
    var rows = [], notes = {
      Vs_V: "battery terminal voltage with the network connected", R1_ohm: "measured out of circuit; nominal " + dcVals().nom[0] + " ohm",
      R2_ohm: "measured out of circuit; nominal " + dcVals().nom[1] + " ohm", R3_ohm: "measured out of circuit; nominal " + dcVals().nom[2] + " ohm",
      R4_ohm: "measured out of circuit; nominal " + dcVals().nom[3] + " ohm", VA_V: "node A to battery minus", VB_V: "node B to battery minus"
    };
    ["Vs_V", "R1_ohm", "R2_ohm", "R3_ohm", "R4_ohm", "VA_V", "VB_V"].forEach(function (q) { var x = latest(q); if (isFinite(x)) rows.push([q, x, notes[q]]); });
    return { header: ["quantity", "value", "note"], rows: rows };
  });
  Sim.exportCSV(Sim.$("#dc-x-all"), "network_readings.csv", function () {
    return { header: ["reading", "function", "red", "black", "battery", "value", "unit"], rows: dc.readings.map(function (r, i) { return [i + 1, r.fn, r.red, r.black, r.conn, isFinite(r.d.value) ? r.d.value : r.d.text, r.unit]; }) };
  });
  dcInit();

  /* ======================= AC RESONANCE ======================= */
  var LIST = [300, 500, 800, 1000, 1200, 1400, 1500, 1600, 1700, 1800, 2000, 2300, 2700, 3200, 4000, 5000, 6500];
  var RANGES = {
    "200m": { max: 0.1999, res: 0.0001, fc: 6000, name: "200 mV" },
    "2": { max: 1.999, res: 0.001, fc: 2500, name: "2 V" }
  };
  var rs = { seed: seed0 + 7, readings: [], ohm: {}, fit: null };

  function rsInit() {
    var rng = Sim.rng(rs.seed);
    rs.dev = { L: Math.max(-0.07, Math.min(0.07, rng.normal(0, 0.03))), C: Math.max(-0.07, Math.min(0.07, rng.normal(0, 0.03))), R: rng.normal(0, 0.004) };
    rs.gain = { "200m": 1 + rng.normal(0, 0.004), "2": 1 + rng.normal(0, 0.004) };
    rs.rng = Sim.rng(rs.seed + 202);
    Sim.$("#rs-seed").textContent = rs.seed;
  }
  function rsVals() {
    function n(id) { return parseFloat(Sim.$(id).value); }
    var real = Sim.$("#rs-real").checked;
    var v = { Lp: n("#rs-L") * 1e-3, Cp: n("#rs-C") * 1e-6, Rp: n("#rs-R"), Rc: n("#rs-Rc"), real: real, fault: Sim.$("#rs-fault").value, vol: n("#rs-vol") / 100, plug: Sim.$("#rs-plug").checked };
    v.L = real ? v.Lp * (1 + rs.dev.L) : v.Lp;
    v.C = real ? v.Cp * (1 + rs.dev.C) : v.Cp;
    v.R = real ? v.Rp * (1 + rs.dev.R) : v.Rp;
    if (v.fault === "c104") v.C = v.C / 10;
    if (v.fault === "open") v.C = 5e-12;            // a few pF of stray capacitance across the gap
    if (v.fault === "short") { v.L = 1e-9; v.RcEff = 0.05; } else v.RcEff = v.Rc;
    return v;
  }
  function rCore(v, f) { return v.real && v.fault !== "short" ? 5.0 * Math.sqrt(f / 1592) : 0; }
  // complex helpers
  function cx(re, im) { return { re: re, im: im }; }
  function cabs(z) { return Math.sqrt(z.re * z.re + z.im * z.im); }
  function circuit(v, f) {
    var w = TAU * f;
    var Z = cx(v.R + v.RcEff + rCore(v, f), w * v.L - 1 / (w * v.C));
    var Rs = 10, Voc = v.vol * 0.55 * (1 - 0.06 * Math.log10(f / 1000));
    var Zt = cx(Z.re + Rs, Z.im), I = Voc / cabs(Zt);
    return { Vin: I * cabs(Z), VR: I * v.R, Z: Z, phase: -Math.atan2(Z.im, Z.re) * 180 / Math.PI };
  }
  function meterAC(x, f, rangeKey) {
    var key = rangeKey;
    if (rangeKey === "auto") key = x < 0.190 ? "200m" : "2";
    var rg = RANGES[key];
    var resp = rs.gain[key] / Math.sqrt(1 + Math.pow(f / rg.fc, 2));
    var noise = 0.005 + (f > 3000 ? 0.004 * Math.pow(f / 3000, 2) : 0);
    var val = x * resp * (1 + rs.rng.normal(0, noise));
    if (val > rg.max) return { ol: true, text: "1 .", range: rg.name };
    var counts = Math.round(val / rg.res + rs.rng.normal(0, 0.3));
    return { value: counts * rg.res, text: rg === RANGES["200m"] ? (counts * rg.res * 1000).toFixed(1) : (counts * rg.res).toFixed(3), unitText: rg === RANGES["200m"] ? "mV" : "V", range: rg.name };
  }
  function rsF() { return parseFloat(Sim.$("#rs-f").value); }

  function rsTheory() {
    var v = rsVals(), Rt = v.Rp + v.Rc;
    var f0 = 1 / (TAU * Math.sqrt(v.Lp * v.Cp)), Q = Math.sqrt(v.Lp / v.Cp) / Rt, x = 1 / (2 * Q);
    kv(Sim.$("#rs-theory"), [
      ["From the printed values: f₀ = 1/(2π√(LC))", f0.toFixed(0) + " Hz"],
      ["R<sub>tot</sub> = R + coil", Rt.toFixed(1) + " Ω"],
      ["√(L/C)", Math.sqrt(v.Lp / v.Cp).toFixed(1) + " Ω"],
      ["Q = √(L/C)/R<sub>tot</sub>", Q.toFixed(2)],
      ["Bandwidth f₀/Q", (f0 / Q).toFixed(0) + " Hz"],
      ["Half-power points", (f0 * (Math.sqrt(1 + x * x) - x)).toFixed(0) + " and " + (f0 * (Math.sqrt(1 + x * x) + x)).toFixed(0) + " Hz"],
      ["Peak height A = R/R<sub>tot</sub>", (v.Rp / Rt).toFixed(3)]
    ]);
  }

  function rsMeasure(f, quiet) {
    var v = rsVals(), log = Sim.$("#rs-log");
    if (!v.plug) { Sim.log(log, "The phone is unplugged: no signal. Plug it in to measure the AC voltages."); return null; }
    var c = circuit(v, f), rg = Sim.$("#rs-range").value;
    var a = meterAC(c.Vin, f, rg), b = meterAC(c.VR, f, rg);
    var disp = Sim.$("#rs-display");
    disp.textContent = b.text; disp.classList.toggle("ol", !!b.ol);
    Sim.$("#rs-disp-what").textContent = "V_R" + (b.ol ? " overload" : " " + b.unitText + " (" + b.range + ")");
    if (a.ol || b.ol) { Sim.log(log, f + " Hz: overload on the " + (a.ol ? a.range : b.range) + " range (the display shows only a 1). Turn the volume down or change range."); return null; }
    var row = { f: f, vin: a.value * 1000, vr: b.value * 1000, rin: a.range, rr: b.range };
    rs.readings.push(row);
    if (!quiet) Sim.log(log, f + " Hz: V_in = " + row.vin.toFixed(1) + " mV, V_R = " + row.vr.toFixed(1) + " mV" + (row.rin !== row.rr ? " (different ranges!)" : ""));
    return row;
  }

  function rsOhm(which) {
    var v = rsVals(), log = Sim.$("#rs-log");
    if (v.plug) {
      var junk = (which === "R" ? 5 : 15) + rs.rng.uniform(0, 60);
      Sim.$("#rs-display").textContent = junk.toFixed(1);
      Sim.$("#rs-disp-what").textContent = "Ω, jumping about";
      Sim.log(log, "Ohmmeter with the tone running: the reading jumps about (" + junk.toFixed(1) + " Ω). Pull the plug out first.");
      return;
    }
    var x = which === "R" ? v.R : v.RcEff;
    var val = Math.round((x * (1 + rs.rng.normal(0, 0.003)) + rs.rng.normal(0, 0.05)) * 10) / 10;
    rs.ohm[which] = val;
    Sim.$("#rs-display").textContent = val.toFixed(1);
    Sim.$("#rs-disp-what").textContent = "Ω (DC)";
    Sim.log(log, (which === "R" ? "Resistor" : "Coil") + " on the ohmmeter: " + val.toFixed(1) + " Ω");
    rsAnalysis();
  }

  // Levenberg–Marquardt fit of H = A / sqrt(1 + Q^2 (f/f0 - f0/f)^2), weights as in lesson06_rlc.py
  function fitRes(fs, H, u) {
    var i0 = 0;
    H.forEach(function (h, i) { if (h > H[i0]) i0 = i; });
    var p = [fs[i0], 2.0, H[i0]], lam = 1e-3;
    function model(p, f) { var x = f / p[0] - p[0] / f; return p[2] / Math.sqrt(1 + p[1] * p[1] * x * x); }
    function chi2(p) { var s = 0; fs.forEach(function (f, i) { var r = (H[i] - model(p, f)) / u[i]; s += r * r; }); return s; }
    function jac(p, f) {
      var x = f / p[0] - p[0] / f, D = 1 + p[1] * p[1] * x * x, D32 = Math.pow(D, -1.5);
      var dx = -f / (p[0] * p[0]) - 1 / f;
      return [-p[2] * p[1] * p[1] * x * dx * D32, -p[2] * p[1] * x * x * D32, 1 / Math.sqrt(D)];
    }
    var c = chi2(p);
    for (var it = 0; it < 200; it++) {
      var JTJ = [[0, 0, 0], [0, 0, 0], [0, 0, 0]], JTr = [0, 0, 0];
      fs.forEach(function (f, i) {
        var J = jac(p, f), r = H[i] - model(p, f), w = 1 / (u[i] * u[i]);
        for (var a = 0; a < 3; a++) { JTr[a] += J[a] * r * w; for (var b = 0; b < 3; b++) JTJ[a][b] += J[a] * J[b] * w; }
      });
      var M = JTJ.map(function (row, a) { return row.map(function (x, b) { return a === b ? x * (1 + lam) : x; }); });
      var d = solve(M, JTr);
      if (!d) break;
      var pn = [p[0] + d[0], Math.abs(p[1] + d[1]), p[2] + d[2]], cn = chi2(pn);
      if (cn < c) {
        var done = Math.abs(c - cn) < 1e-10 * Math.max(1, c);
        p = pn; c = cn; lam = Math.max(lam / 10, 1e-12);
        if (done) break;
      } else lam *= 10;
      if (lam > 1e12) break;
    }
    var JTJ2 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]];
    fs.forEach(function (f, i) { var J = jac(p, f), w = 1 / (u[i] * u[i]); for (var a = 0; a < 3; a++) for (var b = 0; b < 3; b++) JTJ2[a][b] += J[a] * J[b] * w; });
    var cov = invert(JTJ2);
    return { f0: p[0], Q: p[1], A: p[2], u: cov ? [Math.sqrt(cov[0][0]), Math.sqrt(cov[1][1]), Math.sqrt(cov[2][2])] : [NaN, NaN, NaN], chi2: c, dof: fs.length - 3, model: model, p: p };
  }

  function rsAnalysis() {
    var rows = [], v = rsVals(), good = rs.readings.filter(function (r) { return r.vin > 0; });
    var mixed = good.some(function (r) { return r.rin !== r.rr; });
    if (rs.fit) {
      var F = rs.fit, x = 1 / (2 * F.Q);
      rows.push(["f₀", Sim.fmtU(F.f0, F.u[0], "Hz")]);
      rows.push(["Q", Sim.fmtU(F.Q, F.u[1])]);
      rows.push(["Peak height A", Sim.fmtU(F.A, F.u[2])]);
      rows.push(["χ² / degrees of freedom", F.chi2.toFixed(1) + " / " + F.dof + (F.dof > 0 ? " = " + (F.chi2 / F.dof).toFixed(2) : "")]);
      rows.push(["Half-power points", (F.f0 * (Math.sqrt(1 + x * x) - x)).toFixed(0) + " and " + (F.f0 * (Math.sqrt(1 + x * x) + x)).toFixed(0) + " Hz (bandwidth " + (F.f0 / F.Q).toFixed(0) + " Hz)"]);
      var Rm = isFinite(rs.ohm.R) ? rs.ohm.R : v.Rp, Rt = Rm / F.A;
      rows.push(["R<sub>tot</sub> = R/A (R = " + Rm.toFixed(1) + " Ω" + (isFinite(rs.ohm.R) ? ", ohmmeter" : ", printed") + ")", Rt.toFixed(1) + " Ω"]);
      rows.push(["L = QR<sub>tot</sub>/(2πf₀)", (F.Q * Rt / (TAU * F.f0) * 1000).toFixed(2) + " mH (printed " + (v.Lp * 1000).toFixed(1) + ")"]);
      rows.push(["C = 1/(2πf₀QR<sub>tot</sub>)", (1e6 / (TAU * F.f0 * F.Q * Rt)).toFixed(3) + " µF (printed " + (v.Cp * 1e6).toFixed(2) + ")"]);
      if (isFinite(rs.ohm.R) && isFinite(rs.ohm.Rc)) {
        var sum = rs.ohm.R + rs.ohm.Rc;
        rows.push(["Ohmmeter R + coil", sum.toFixed(1) + " Ω; the fit's R<sub>tot</sub> is " + (Rt - sum >= 0 ? "+" : "") + (Rt - sum).toFixed(1) + " Ω different (coil losses at kHz)"]);
        rows.push(["Q predicted from printed L, C and the ohmmeter sum", (Math.sqrt(v.Lp / v.Cp) / sum).toFixed(2)]);
      } else rows.push(["Ohmmeter values", "unplug the phone and measure the resistor and the coil"]);
    } else rows.push(["Fit", good.length >= 4 ? "press Fit" : "take at least 4 readings, most between 0.7 f₀ and 1.4 f₀"]);
    if (mixed) rows.push(["Warning", "<span class=\"warn\">some rows were read on different ranges for V<sub>in</sub> and V<sub>R</sub>: the ratio does not cancel the meter's frequency error there</span>"]);
    kv(Sim.$("#rs-analysis"), rows);
  }

  var rsPlot = Sim.plot(Sim.$("#rs-plot"), { xLabel: "f / Hz", yLabel: "H = V_R / V_in", logX: true, xMin: 200, xMax: 10000, yMin: 0 });
  var rsPh = Sim.plot(Sim.$("#rs-phplot"), { xLabel: "f / Hz", yLabel: "phase of I / °", logX: true, xMin: 200, xMax: 10000, yMin: -95, yMax: 95 });

  function rsDraw() {
    var v = rsVals(), ser = [], i;
    var pts = rs.readings.filter(function (r) { return r.vin > 0; });
    if (rs.fit) {
      var F = rs.fit, x = 1 / (2 * F.Q), f1 = F.f0 * (Math.sqrt(1 + x * x) - x), f2 = F.f0 * (Math.sqrt(1 + x * x) + x);
      ser.push({ type: "band", data: [[f1, 0, F.A * 1.08], [f2, 0, F.A * 1.08]], color: "s3", alpha: 0.12, label: "half-power band" });
      var cur = [];
      for (i = 0; i <= 300; i++) { var f = 200 * Math.pow(50, i / 300); cur.push([f, F.model(F.p, f)]); }
      ser.push({ data: cur, color: "s1", label: "fit" });
      ser.push({ type: "hline", y: F.A / Math.SQRT2, color: "muted", dash: [3, 3], width: 1 });
    }
    if (Sim.$("#rs-true").checked) {
      var tc = [];
      for (i = 0; i <= 300; i++) { var ff = 200 * Math.pow(50, i / 300), c = circuit(v, ff); tc.push([ff, c.VR / c.Vin]); }
      ser.push({ data: tc, color: "s4", dash: [5, 4], width: 1.5, label: "model's true ratio" });
    }
    ser.push({ type: "points", data: pts.map(function (r) { return [r.f, r.vr / r.vin]; }), color: "s2", label: "readings" });
    var fNow = rsF();
    if (isFinite(fNow)) ser.push({ type: "vline", x: fNow, color: "muted", width: 1 });
    rsPlot.draw(ser);
    var showPh = Sim.$("#rs-phase").checked;
    Sim.$("#rs-phplot").hidden = !showPh;
    if (showPh) {
      var ph = [];
      for (i = 0; i <= 300; i++) { var fp = 200 * Math.pow(50, i / 300); ph.push([fp, circuit(v, fp).phase]); }
      rsPh.draw([{ data: ph, color: "s4", label: "current relative to V_in (not measurable with a multimeter)" }, { type: "hline", y: 0, color: "muted", width: 1 }]);
    }
    rsCirc();
  }

  function rsCirc() {
    var c = canvas2d(Sim.$("#rs-circ")), ctx = c.ctx, W = c.W, H = c.H, v = rsVals();
    var xL = 50, xR = W - 40, yT = 36, yB = H - 30;
    ctx.strokeStyle = Sim.color("ink"); ctx.lineWidth = 1.6;
    // phone jack on the left
    ctx.fillStyle = Sim.color("panel-2"); ctx.fillRect(8, yT - 10, 34, yB - yT + 20);
    ctx.fillStyle = Sim.color("ink"); ctx.textAlign = "center";
    ctx.fillText("tip", 25, yT + 4); ctx.fillText("sleeve", 25, yB + 4);
    var x1 = xL + (xR - xL) * 0.33, x2 = xL + (xR - xL) * 0.62;
    // inductor: bumps
    line(ctx, [[42, yT], [xL, yT]]);
    var n = 5, w = (x1 - xL) * 0.6, s0 = xL + (x1 - xL) * 0.2;
    line(ctx, [[xL, yT], [s0, yT]]);
    for (var i = 0; i < n; i++) { ctx.beginPath(); ctx.arc(s0 + w / n * (i + 0.5), yT, w / n / 2, Math.PI, 0); ctx.stroke(); }
    line(ctx, [[s0 + w, yT], [x1, yT]]);
    ctx.fillText("L " + (v.Lp * 1000).toFixed(1) + " mH" + (v.fault === "short" ? " (shorted!)" : ""), (xL + x1) / 2, yT - 12);
    if (v.fault === "short") { ctx.strokeStyle = Sim.color("bad"); line(ctx, [[xL + 4, yT + 8], [x1 - 4, yT + 8]]); line(ctx, [[xL + 4, yT], [xL + 4, yT + 8]]); line(ctx, [[x1 - 4, yT], [x1 - 4, yT + 8]]); ctx.strokeStyle = Sim.color("ink"); }
    // capacitor
    var xc = (x1 + x2) / 2;
    line(ctx, [[x1, yT], [xc - 5, yT]]);
    if (v.fault !== "open") line(ctx, [[xc + 5, yT], [x2, yT]]); else line(ctx, [[xc + 18, yT], [x2, yT]]);
    ctx.lineWidth = 2.5; line(ctx, [[xc - 5, yT - 12], [xc - 5, yT + 12]]); line(ctx, [[xc + 5, yT - 12], [xc + 5, yT + 12]]); ctx.lineWidth = 1.6;
    ctx.fillText("C " + (v.fault === "c104" ? "0.1 µF (104)" : (v.Cp * 1e6).toFixed(2) + " µF") + (v.fault === "open" ? " (open)" : ""), xc, yT - 18);
    // resistor down the right side to the sleeve wire
    line(ctx, [[x2, yT], [xR, yT]]);
    resistor(ctx, xR, yT, xR, yB, "R " + v.Rp + " Ω");
    line(ctx, [[xR, yB], [42, yB]]);
    // meter positions
    ctx.fillStyle = Sim.color("s1"); ctx.textAlign = "left";
    ctx.fillText("V_in: tip to sleeve", 50, H - 8);
    ctx.fillText("V_R: across R", xR - 120, (yT + yB) / 2 + 30);
    ctx.fillStyle = Sim.color("muted"); ctx.textAlign = "right";
    ctx.fillText(v.plug ? "tone " + rsF().toFixed(0) + " Hz, volume " + (v.vol * 100).toFixed(0) + " %" : "unplugged", W - 6, 14);
  }

  function rsRender() {
    var tb = Sim.$("#rs-table tbody");
    tb.textContent = "";
    rs.readings.forEach(function (r, i) {
      tb.appendChild(tr([i + 1, r.f.toFixed(0), r.vin.toFixed(1), r.vr.toFixed(1), r.rin === r.rr ? r.rin : r.rin + " / " + r.rr, (r.vr / r.vin).toFixed(4)]));
    });
    rsAnalysis();
    rsDraw();
  }

  function setFreq(f, fromSlider) {
    f = Math.max(100, Math.min(10000, Math.round(f)));
    Sim.$("#rs-f").value = f;
    if (!fromSlider) Sim.$("#rs-fs").value = Math.log10(f).toFixed(3);
    Sim.$("#rs-f-out").textContent = f;
    rsDraw();
  }

  Sim.$("#rs-fs").addEventListener("input", function () { setFreq(Math.pow(10, parseFloat(this.value)), true); });
  Sim.$("#rs-f").addEventListener("change", function () { setFreq(parseFloat(this.value)); });
  ["#rs-L", "#rs-C", "#rs-R", "#rs-Rc", "#rs-real", "#rs-fault", "#rs-vol", "#rs-plug", "#rs-true", "#rs-phase", "#rs-range"].forEach(function (id) {
    Sim.$(id).addEventListener("change", function () { rsTheory(); rsDraw(); });
    Sim.$(id).addEventListener("input", function () { rsTheory(); rsDraw(); });
  });
  Sim.$("#rs-meas").addEventListener("click", function () { rsMeasure(rsF()); rs.fit = null; rsRender(); });
  Sim.$("#rs-list").addEventListener("click", function () {
    var n = 0;
    LIST.forEach(function (f) { if (rsMeasure(f, true)) n++; });
    Sim.log(Sim.$("#rs-log"), "Measured " + n + " of " + LIST.length + " frequencies from the lesson's list.");
    rs.fit = null; rsRender();
  });
  Sim.$("#rs-ohmR").addEventListener("click", function () { rsOhm("R"); });
  Sim.$("#rs-ohmL").addEventListener("click", function () { rsOhm("Rc"); });
  Sim.$("#rs-fit").addEventListener("click", function () {
    var good = rs.readings.filter(function (r) { return r.vin > 0 && r.vr > 0; });
    if (good.length < 4) { rs.fit = null; rsAnalysis(); return; }
    var fs = good.map(function (r) { return r.f; }), H = good.map(function (r) { return r.vr / r.vin; });
    var u = good.map(function (r, i) { var a = H[i] * Math.SQRT2 * 0.005, b = 0.1 / r.vin; return Math.sqrt(a * a + b * b); });
    rs.fit = fitRes(fs, H, u);
    rsRender();
  });
  Sim.$("#rs-undo").addEventListener("click", function () { rs.readings.pop(); rs.fit = null; rsRender(); });
  Sim.$("#rs-clear").addEventListener("click", function () { rs.readings = []; rs.fit = null; rsRender(); });
  Sim.$("#rs-rerun").addEventListener("click", function () { rs.seed = Sim.newSeed(rs.seed); rsInit(); rs.readings = []; rs.ohm = {}; rs.fit = null; rsTheory(); rsRender(); Sim.log(Sim.$("#rs-log"), "New seed " + rs.seed + ": new parts and a new meter."); });
  Sim.exportCSV(Sim.$("#rs-x"), "my_rlc.csv", function () {
    return { header: ["f_Hz", "Vin_mV", "VR_mV"], rows: rs.readings.map(function (r) { return [r.f, +r.vin.toFixed(1), +r.vr.toFixed(1)]; }) };
  });

  /* ======================= TABS ======================= */
  var tabs = Sim.tabs(Sim.$("#tabs"), function (name) {
    if (name === "dc") dcRender();
    if (name === "resonance") { rsTheory(); rsRender(); }
  });
  Sim.onTheme(function () { dcDraw(); rsCirc(); });
  rsInit();
  rsTheory();
  tabs.select(preset.tab || "dc");
})();
