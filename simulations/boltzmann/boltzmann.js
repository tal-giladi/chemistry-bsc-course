/* boltzmann simulation: two-level systems, the energy ladder, the rigid rotor and the counting of
 * microstates (lessons 21.1, 21.2, 21.3). Uses ../common/sim.js (global Sim).
 *
 * p_i = g_i exp(-E_i/kT)/q; hc/k_B = 1.438777 cm K and R from CODATA 2022 (Sim.C).
 * Two levels: C_V/R = r x^2 e^-x/(1 + r e^-x)^2 (Schottky), r = g1/g0, x = eps/kT.
 * Ladder (harmonic, from v = 0): q = 1/(1 - e^-x), C_V/R = x^2 e^x/(e^x - 1)^2 (Einstein).
 * Anharmonic levels G(v) - G(0) = we v - wexe v(v + 1) summed up to D0, as in stat21.py.
 * Rotor: q = (1/sigma) sum (2J+1) exp(-theta J(J+1)/T); high T: T/(sigma theta).
 * Nuclear-spin weights for X states: 14N2 (I = 1) even 6 : odd 3; 1H2 (I = 1/2) even 1 : odd 3;
 * 127I2 (I = 5/2) even 15 : odd 21; 16O2 (I = 0, 3Sigma_g-) odd N only.
 * Data: Cl and I 2P1/2 at 882.3515 and 7602.9762 cm^-1 (NIST ASD); NO 2Pi3/2 about 120 cm^-1
 * (lesson 21.1); NIST WebBook constants as in labs/module-21/stat21.py: N2 we 2358.57, wexe 14.324,
 * Be 1.998241, ae 0.017318; CO Be 1.93128087, ae 0.01750441; HCl we 2990.9463, wexe 52.8186,
 * B0 10.4398; O2 Be 1.4376766, ae 0.01593; I2 we 214.502, wexe 0.6147, Be 0.037372, ae 0.0001138;
 * H2 Be 60.853, ae 3.062 (B0 59.322). D0: I2 12440.7 cm^-1 (NIST-JANAF), N2 9.759 eV, HCl 4.43 eV.
 */
(function () {
  "use strict";
  var C = Sim.C, S = Sim.stats, HC_K = C.h * C.c * 100 / C.kB, R = C.R, EV_CM = C.e / (C.h * C.c * 100);

  var PRESETS = {
    "two-level": {
      title: "Two-level system", tab: "two",
      what: "A molecule in a bath at temperature T sits in level i with probability g<sub>i</sub>e<sup>−E<sub>i</sub>/k<sub>B</sub>T</sup>/q. With only two levels the upper population rises with T but can never pass g₁/g₀ times the lower one, and the heat capacity shows a peak, the Schottky anomaly.",
      task: "Raise the temperature of the chlorine atom and watch N₁/N₀ approach, but never pass, g₁/g₀ = 0.5. Read the upper fraction at 298 K and 1000 K, then choose NO and read it at 298 K. Finally count molecules at five temperatures and recover the gap from the slope of ln ratio against 1/T.",
      target: "Cl: upper fraction 0.0070 at 298 K and 0.123 at 1000 K, never above 1/3; NO: 0.36 at 298 K; the fitted gap within its uncertainty of the gap you set."
    },
    ladder: {
      title: "Energy ladder", tab: "ladder",
      what: "A harmonic ladder of equally spaced levels has q = 1/(1 − e<sup>−x</sup>): roughly the number of states the molecule can reach. Its heat capacity rises from zero to R (equipartition) and never passes it, unlike a two-level system, which fills up.",
      task: "Set the spacing to 1 in units of k<sub>B</sub>T at the start (T = 1) and read q and the populations as you raise T. Watch C<sub>V</sub> approach R but never pass it. Then choose I₂ at 298 K and N₂ at 1000 K.",
      target: "At T = ε/k<sub>B</sub>: q = 1.582 and C<sub>V</sub>/R = 0.921. I₂ at 298 K: q = 1.56 and C<sub>V,vib</sub> = 7.62 J mol⁻¹ K⁻¹; N₂ at 1000 K: C<sub>V,vib</sub>/R = 0.422."
    },
    rotor: {
      title: "Rigid rotor", tab: "rotor",
      what: "The rotational partition function sums (2J + 1)e<sup>−θ<sub>rot</sub>J(J+1)/T</sup>. Far above θ<sub>rot</sub> = hcB/k<sub>B</sub> the sum becomes an integral, T/(σθ<sub>rot</sub>); near θ<sub>rot</sub> the exact sum separates from it. The symmetry number σ removes the rotations that give an indistinguishable copy.",
      task: "HCl: lower the temperature from 298 K towards θ<sub>rot</sub> = 15 K and watch the exact q separate from T/σθ<sub>rot</sub>. Find where the gap reaches 5 %. Then look at H₂ at room temperature, and switch on nuclear-spin statistics for N₂ and H₂.",
      target: "HCl at 298 K: exact 20.19 against 19.85; the gap reaches about 5 % near 100 K; for H₂ the high-temperature formula is off by about 10 % even at 298 K."
    },
    microstates: {
      title: "Counting microstates", tab: "micro",
      what: "q identical quanta can be shared among N oscillators in W = (q + N − 1)!/(q!(N − 1)!) ways. Two solids in contact settle at the split with the most microstates, where their temperatures are equal. One oscillator among many follows the Boltzmann distribution.",
      task: "Check W(3, 3) = 10 by listing. Share 6 quanta between two 3-oscillator solids, then 100 quanta between 300 and 200 oscillators. Play the exchange game with 10 cups and then 400.",
      target: "28, 63, 90, 100, 90, 63, 28 for the small solids; the peak at q<sub>A</sub> = 60 with slopes 1.775 and 1.767 and 95 % within ±10; game fractions near 0.50, 0.25, 0.125."
    }
  };

  var preset = Sim.preset(PRESETS, "two-level");
  var seed0 = Sim.seedFromQuery(21);
  Sim.label();
  Sim.presetBox(Sim.$("#preset"), preset);

  function tr(cells) { var row = Sim.el("tr"); cells.forEach(function (c) { row.appendChild(Sim.el("td", { html: String(c) })); }); return row; }
  function kv(el, pairs) { el.textContent = ""; pairs.forEach(function (p) { el.appendChild(Sim.el("span", { html: p[0] })); el.appendChild(Sim.el("span", { html: p[1] })); }); }
  function sig(x, n) { return Math.abs(x) < 1e-3 && x !== 0 ? x.toExponential(n - 1) : x.toPrecision(n); }
  function logGrid(a, b, n) { var out = []; for (var i = 0; i <= n; i++) out.push(Math.pow(10, a + (b - a) * i / n)); return out; }

  /* ======================= TWO LEVELS ======================= */
  var SYS2 = { Cl: { eps: 882.3515, g0: 4, g1: 2 }, I: { eps: 7602.9762, g0: 4, g1: 2 }, NO: { eps: 120, g0: 2, g1: 2 } };
  var b2 = { seed: seed0, rng: Sim.rng(seed0), counts: [] };
  var b2Bars = Sim.plot(Sim.$("#b2-bars"), { xLabel: "level", yLabel: "fraction", yMin: 0, yMax: 1, xMin: -0.6, xMax: 1.6 });
  var b2Curve = Sim.plot(Sim.$("#b2-curve"), { xLabel: "T / K", yLabel: "fraction or C_V/R", logX: true, yMin: 0 });
  var b2Fit = Sim.plot(Sim.$("#b2-fit"), { xLabel: "1/T / K⁻¹", yLabel: "ln[(n₁/g₁)/(n₀/g₀)]" });

  function b2Vals() {
    function n(id) { return parseFloat(Sim.$(id).value); }
    return { eps: n("#b2-eps"), g0: Math.max(1, Math.round(n("#b2-g0"))), g1: Math.max(1, Math.round(n("#b2-g1"))), T: Math.pow(10, n("#b2-T")) };
  }
  function two(v, T) {
    var x = v.eps * HC_K / T, r = v.g1 / v.g0, e = Math.exp(-x);
    var q = v.g0 + v.g1 * e, f1 = v.g1 * e / q;
    var cv = r * x * x * e / Math.pow(1 + r * e, 2);
    var u = R * T * x * f1;                       // J/mol
    return { x: x, q: q, f1: f1, f0: 1 - f1, ratio: r * e, cv: cv, u: u, s: u / T + R * Math.log(q) };
  }
  function b2Render() {
    var v = b2Vals();
    Sim.$("#b2-T-out").textContent = v.T < 10 ? v.T.toFixed(2) : v.T.toFixed(0);
    Sim.$("#b2-seed").textContent = b2.seed;
    if (!(v.eps > 0)) return;
    var o = two(v, v.T), grid = logGrid(0, 4.3, 300), best = { cv: 0, T: 0 };
    var fc = [], cc = [];
    grid.forEach(function (T) { var t = two(v, T); fc.push([T, t.f1]); cc.push([T, t.cv]); if (t.cv > best.cv) best = { cv: t.cv, T: T }; });
    kv(Sim.$("#b2-out"), [
      ["x = ε/k<sub>B</sub>T", o.x.toPrecision(4)],
      ["q = g₀ + g₁e<sup>−x</sup>", o.q.toFixed(4)],
      ["Fraction in the upper level", sig(o.f1, 3)],
      ["N₁/N₀ (limit g₁/g₀ = " + (v.g1 / v.g0).toFixed(3) + ")", sig(o.ratio, 3)],
      ["Per state, upper/lower", sig(Math.exp(-o.x), 3)],
      ["U − U(0)", o.u.toFixed(1) + " J/mol"],
      ["C<sub>V</sub> (Schottky)", (o.cv * R).toFixed(3) + " J mol⁻¹ K⁻¹ (C<sub>V</sub>/R = " + o.cv.toFixed(4) + ")"],
      ["Peak of C<sub>V</sub>", (best.cv * R).toFixed(2) + " J mol⁻¹ K⁻¹ near " + best.T.toFixed(0) + " K"],
      ["S<sub>el</sub> = (U − U(0))/T + R ln q", o.s.toFixed(2) + " J mol⁻¹ K⁻¹"]
    ]);
    b2Bars.draw([{ type: "bars", data: [[0, o.f0]], color: "s1", barWidth: 0.6, label: "lower, g = " + v.g0 }, { type: "bars", data: [[1, o.f1]], color: "s2", barWidth: 0.6, label: "upper, g = " + v.g1 }, { type: "hline", y: v.g1 / (v.g0 + v.g1), color: "muted", dash: [4, 3], width: 1, label: "high-T limit of the upper level" }]);
    b2Curve.draw([
      { data: fc, color: "s2", label: "upper fraction" },
      { data: cc, color: "s4", label: "C_V/R" },
      { type: "hline", y: v.g1 / (v.g0 + v.g1), color: "muted", dash: [4, 3], width: 1 },
      { type: "vline", x: v.T, color: "muted", width: 1 }
    ], { xMin: 1, xMax: 20000, yMax: Math.max(v.g1 / (v.g0 + v.g1), best.cv) * 1.2 });
    b2Table();
  }
  function binomial(n, p, rng) {
    if (n <= 20000) { var k = 0; for (var i = 0; i < n; i++) if (rng.random() < p) k++; return k; }
    var m = n * p, sd = Math.sqrt(n * p * (1 - p));
    return Math.max(0, Math.min(n, Math.round(rng.normal(m, sd))));
  }
  function b2Count() {
    var v = b2Vals(), N = Math.max(10, Math.round(parseFloat(Sim.$("#b2-N").value) || 1000));
    var o = two(v, v.T), n1 = binomial(N, o.f1, b2.rng);
    b2.counts.push({ T: +v.T.toFixed(2), n0: N - n1, n1: n1, g0: v.g0, g1: v.g1, eps: v.eps });
    b2Table();
  }
  function b2Table() {
    var tb = Sim.$("#b2-table tbody"), v = b2Vals();
    tb.textContent = "";
    var pts = [], err = [];
    b2.counts.forEach(function (c, i) {
      var y = c.n0 > 0 && c.n1 > 0 ? Math.log((c.n1 / c.g1) / (c.n0 / c.g0)) : NaN;
      tb.appendChild(tr([i + 1, c.T, c.n0, c.n1, isFinite(y) ? y.toFixed(4) : "— (a zero count)"]));
      if (isFinite(y) && c.eps === v.eps && c.g0 === v.g0 && c.g1 === v.g1) { pts.push([1 / c.T, y]); err.push(Math.sqrt(1 / c.n0 + 1 / c.n1)); }
    });
    var ser = [{ type: "points", data: pts, err: err, color: "s2", label: "counts (±1/√n)" }], out = [];
    var distinct = {};
    pts.forEach(function (p) { distinct[p[0].toPrecision(6)] = 1; });
    if (Object.keys(distinct).length >= 2) {
      var f = S.linfit(pts.map(function (p) { return p[0]; }), pts.map(function (p) { return p[1]; }));
      var xs = pts.map(function (p) { return p[0]; }), lo = Math.min.apply(null, xs), hi = Math.max.apply(null, xs);
      ser.push({ data: [[lo, f.a + f.b * lo], [hi, f.a + f.b * hi]], color: "s1", label: "fit" });
      out.push(["Slope = −ε/k<sub>B</sub>", Sim.fmtU(f.b, f.ub, "K")]);
      out.push(["Gap ε = −slope/(hc/k<sub>B</sub>)", Sim.fmtU(-f.b / HC_K, f.ub / HC_K, "cm⁻¹") + " (set " + v.eps + ")"]);
      out.push(["Intercept (should be 0 per state)", Sim.fmtU(f.a, f.ua)]);
    } else out.push(["Fit", "count at two or more temperatures with the same levels"]);
    b2Fit.draw(ser);
    kv(Sim.$("#b2-fitout"), out);
  }
  Sim.$("#b2-sys").addEventListener("change", function () {
    var s = SYS2[this.value];
    if (s) { Sim.$("#b2-eps").value = s.eps; Sim.$("#b2-g0").value = s.g0; Sim.$("#b2-g1").value = s.g1; }
    b2Render();
  });
  ["#b2-eps", "#b2-g0", "#b2-g1"].forEach(function (id) { Sim.$(id).addEventListener("input", function () { Sim.$("#b2-sys").value = "custom"; b2Render(); }); });
  Sim.$("#b2-T").addEventListener("input", b2Render);
  Sim.$("#b2-count").addEventListener("click", b2Count);
  Sim.$("#b2-clear").addEventListener("click", function () { b2.counts = []; b2Table(); });
  Sim.$("#b2-rerun").addEventListener("click", function () { b2.seed = Sim.newSeed(b2.seed); b2.rng = Sim.rng(b2.seed); b2.counts = []; b2Render(); });
  Sim.exportCSV(Sim.$("#b2-x"), "two_level_counts.csv", function () {
    return { header: ["T_K", "n_lower", "n_upper", "g_lower", "g_upper", "gap_cm"], rows: b2.counts.map(function (c) { return [c.T, c.n0, c.n1, c.g0, c.g1, c.eps]; }) };
  });

  /* ======================= LADDER ======================= */
  var MOLV = {
    I2: { we: 214.502, wexe: 0.6147, D0: 12440.7, T: 298.15 },
    N2: { we: 2358.57, wexe: 14.324, D0: 9.759 * EV_CM, T: 1000 },
    HCl: { we: 2990.9463, wexe: 52.8186, D0: 4.43 * EV_CM, T: 298.15 }
  };
  var blBars = Sim.plot(Sim.$("#bl-bars"), { xLabel: "v", yLabel: "fraction", yMin: 0 });
  var blCurve = Sim.plot(Sim.$("#bl-curve"), { xLabel: "T", yLabel: "C_V/R", logX: true, yMin: 0, yMax: 1.25 });

  function blLevels() {         // level energies in temperature units (K, or eps/k in reduced mode)
    var sys = Sim.$("#bl-sys").value, anh = Sim.$("#bl-anh").checked && sys !== "reduced", th = [];
    if (sys === "reduced") { for (var v = 0; v < 400; v++) th.push(v); return { th: th, theta: 1, reduced: true }; }
    var m = MOLV[sys], nu = m.we - 2 * m.wexe;
    if (!anh) { for (v = 0; v < 400; v++) th.push(v * nu * HC_K); }
    else {
      var prev = -1;
      for (v = 0; v < 2000; v++) {
        var e = m.we * v - m.wexe * v * (v + 1);
        if (e > m.D0 || e < prev) break;
        th.push(e * HC_K); prev = e;
      }
    }
    return { th: th, theta: nu * HC_K, reduced: false, anh: anh };
  }
  function ladderAt(L, T) {
    var q = 0, e1 = 0, e2 = 0, ps = [];
    L.th.forEach(function (t) { var w = Math.exp(-t / T); q += w; e1 += t * w; e2 += t * t * w; ps.push(w); });
    var mean = e1 / q, cv = (e2 / q - mean * mean) / (T * T);     // C_V/R = <(E - <E>)^2>/(kT)^2
    return { q: q, mean: mean, cv: cv, s: mean / T + Math.log(q), p: ps.map(function (w) { return w / q; }) };
  }
  function blRange() {
    var sys = Sim.$("#bl-sys").value, sl = Sim.$("#bl-T");
    if (sys === "reduced") { sl.min = -1.5; sl.max = 1.3; Sim.$("#bl-T-label").innerHTML = "Temperature T / (ε/k<sub>B</sub>)"; }
    else { sl.min = 1; sl.max = 3.7; Sim.$("#bl-T-label").textContent = "Temperature T / K"; }
  }
  function blRender() {
    var L = blLevels(), T = Math.pow(10, parseFloat(Sim.$("#bl-T").value)), o = ladderAt(L, T), x = L.theta / T;
    Sim.$("#bl-T-out").textContent = L.reduced ? T.toFixed(3) : T.toFixed(1);
    var qc = 1 / (1 - Math.exp(-x)), cvE = x * x * Math.exp(x) / Math.pow(Math.exp(x) - 1, 2);
    var rows = [
      ["x = θ<sub>vib</sub>/T", x.toPrecision(4) + (L.reduced ? "" : " (θ<sub>vib</sub> = " + L.theta.toFixed(0) + " K)")],
      ["q (sum over " + L.th.length + " levels)", o.q.toPrecision(6)],
      ["q = 1/(1 − e<sup>−x</sup>)", qc.toPrecision(6)],
      ["Populations v = 0, 1, 2", o.p.slice(0, 3).map(function (p) { return sig(p, 3); }).join(", ")],
      ["C<sub>V</sub>/R", o.cv.toFixed(4) + " (Einstein formula " + cvE.toFixed(4) + ")"]
    ];
    if (L.reduced) rows.push(["⟨E⟩ per molecule", o.mean.toFixed(4) + " ε"]);
    else {
      rows.push(["U − U(0)", (R * o.mean / 1000).toFixed(4) + " kJ/mol"]);
      rows.push(["C<sub>V,vib</sub>", (R * o.cv).toFixed(3) + " J mol⁻¹ K⁻¹"]);
      rows.push(["S<sub>vib</sub>", (R * o.s).toFixed(3) + " J mol⁻¹ K⁻¹ (S/R = " + o.s.toFixed(4) + ")"]);
    }
    if (L.reduced) rows.push(["S/R", o.s.toFixed(4)]);
    if (Sim.$("#bl-two").checked) { var e = Math.exp(-x); rows.push(["Two levels, same gap: C<sub>V</sub>/R", (x * x * e / Math.pow(1 + e, 2)).toFixed(4)]); }
    kv(Sim.$("#bl-out"), rows);
    var nb = Math.min(o.p.length, 16), bars = [];
    for (var i = 0; i < nb; i++) bars.push([i, o.p[i]]);
    blBars.draw([{ type: "bars", data: bars, color: "s1", label: "fraction in v" }], { xMin: -0.6, xMax: nb - 0.4, yMax: 1 });
    var sl = Sim.$("#bl-T"), grid = logGrid(parseFloat(sl.min), parseFloat(sl.max), 160), cv = [], cv2 = [];
    grid.forEach(function (t) {
      cv.push([t, ladderAt(L, t).cv]);
      var xx = L.theta / t, ee = Math.exp(-xx);
      cv2.push([t, xx * xx * ee / Math.pow(1 + ee, 2)]);
    });
    var ser = [{ data: cv, color: "s1", label: "ladder" }, { type: "hline", y: 1, color: "muted", dash: [4, 3], width: 1, label: "equipartition, C_V = R" }];
    if (Sim.$("#bl-two").checked) ser.push({ data: cv2, color: "s2", dash: [5, 3], label: "two levels (Schottky)" });
    ser.push({ type: "vline", x: T, color: "muted", width: 1 });
    blCurve.draw(ser, { xLabel: L.reduced ? "T / (ε/k)" : "T / K", xMin: grid[0], xMax: grid[grid.length - 1] });
  }
  Sim.$("#bl-sys").addEventListener("change", function () {
    blRange();
    var m = MOLV[this.value];
    Sim.$("#bl-T").value = m ? Math.log10(m.T).toFixed(4) : "0";
    blRender();
  });
  ["#bl-anh", "#bl-two"].forEach(function (id) { Sim.$(id).addEventListener("change", blRender); });
  Sim.$("#bl-T").addEventListener("input", blRender);
  Sim.exportCSV(Sim.$("#bl-x"), "ladder_thermo.csv", function () {
    var L = blLevels(), sl = Sim.$("#bl-T");
    var rows = logGrid(parseFloat(sl.min), parseFloat(sl.max), 60).map(function (t) {
      var o = ladderAt(L, t);
      return [+t.toPrecision(5), +o.q.toPrecision(7), L.reduced ? +o.mean.toPrecision(6) : +(R * o.mean).toPrecision(6), +o.cv.toPrecision(6), +o.s.toPrecision(6)];
    });
    return { header: ["T", "q", L.reduced ? "E_mean_eps" : "U_minus_U0_J_per_mol", "Cv_over_R", "S_over_R"], rows: rows };
  });

  /* ======================= ROTOR ======================= */
  var ROT = {
    HCl: { B: 10.4398, sigma: 1 },
    N2: { B: 1.998241 - 0.017318 / 2, sigma: 2, w: [6, 3] },
    CO: { B: 1.93128087 - 0.01750441 / 2, sigma: 1 },
    O2: { B: 1.4376766 - 0.01593 / 2, sigma: 2, w: [0, 1] },
    I2: { B: 0.037372 - 0.0001138 / 2, sigma: 2, w: [15, 21] },
    H2: { B: 60.853 - 3.062 / 2, sigma: 2, w: [1, 3] }
  };
  var brBars = Sim.plot(Sim.$("#br-bars"), { xLabel: "J", yLabel: "fraction", yMin: 0 });
  var brQ = Sim.plot(Sim.$("#br-q"), { xLabel: "T / K", yLabel: "q_rot", logX: true, logY: true });

  function rotor() { var m = ROT[Sim.$("#br-mol").value]; return { B: m.B, sigma: m.sigma, w: m.w, ns: Sim.$("#br-ns").checked && !!m.w }; }
  function qRot(m, T, parts) {
    var th = m.B * HC_K, q = 0, J = 0, list = [];
    var jmax = Math.max(20, Math.ceil(12 * Math.sqrt(T / th)) + 10);
    for (J = 0; J <= jmax; J++) {
      var g = m.ns ? m.w[J % 2] : 1;
      var t = g * (2 * J + 1) * Math.exp(-th * J * (J + 1) / T);
      q += t;
      if (parts) list.push(t);
    }
    var norm = m.ns ? (m.w[0] + m.w[1]) : m.sigma;
    if (parts) return { q: q / norm, terms: list.map(function (t) { return t / q; }) };
    return q / norm;
  }
  function brRender() {
    var m = rotor(), T = Math.pow(10, parseFloat(Sim.$("#br-T").value)), th = m.B * HC_K;
    Sim.$("#br-T-out").textContent = T < 10 ? T.toFixed(2) : T.toFixed(0);
    var ex = qRot(m, T, true), hi = T / (m.sigma * th), corr = hi * (1 + th / (3 * T) + th * th / (15 * T * T));
    var dT = T * 1e-4, lq = function (t) { return Math.log(qRot(m, t)); };
    var d1 = (lq(T + dT) - lq(T - dT)) / (2 * dT), d2 = (lq(T + dT) - 2 * lq(T) + lq(T - dT)) / (dT * dT);
    var sEx = R * (Math.log(ex.q) + T * d1), sHi = R * (Math.log(hi) + 1), cv = 2 * T * d1 + T * T * d2;
    var best = 0;
    ex.terms.forEach(function (f, J) { if (f > ex.terms[best]) best = J; });
    kv(Sim.$("#br-out"), [
      ["θ<sub>rot</sub> = hcB₀/k<sub>B</sub>", th.toPrecision(4) + " K"],
      ["q<sub>rot</sub> exact sum", ex.q.toPrecision(5)],
      ["q<sub>rot</sub> = T/(σθ<sub>rot</sub>)", hi.toPrecision(5) + " (" + ((hi / ex.q - 1) * 100).toFixed(2) + " %)"],
      ["with (1 + θ/3T + θ²/15T²)", corr.toPrecision(5)],
      ["S<sub>rot</sub> exact", sEx.toFixed(2) + " J mol⁻¹ K⁻¹"],
      ["S<sub>rot</sub> = R(ln q + 1), high T", sHi.toFixed(2) + " J mol⁻¹ K⁻¹"],
      ["C<sub>V,rot</sub>/R", cv.toFixed(3) + " (classical limit 1)"],
      ["Most populated level", "J = " + best]
    ]);
    var bars = [], nb = 0;
    ex.terms.forEach(function (f, J) { if (J <= 4 || f > 1e-3) { bars.push([J, f]); nb = J; } });
    brBars.draw([{ type: "bars", data: bars, color: "s1", barWidth: 0.8, label: m.ns ? "fraction (with nuclear-spin weights)" : "fraction in J" }], { xMin: -0.6, xMax: nb + 0.6 });
    var grid = logGrid(0, 3, 150), a = [], b = [], c = [];
    grid.forEach(function (t) { a.push([t, qRot(m, t)]); var h = t / (m.sigma * th); b.push([t, h]); c.push([t, h * (1 + th / (3 * t) + th * th / (15 * t * t))]); });
    brQ.draw([
      { data: a, color: "s1", label: "exact sum" },
      { data: b, color: "s2", dash: [5, 3], label: "T/(σθ_rot)" },
      { data: c, color: "s3", dash: [2, 3], label: "with the correction" },
      { type: "vline", x: T, color: "muted", width: 1 }
    ], { xMin: 1, xMax: 1000, yMin: Math.max(1e-3, Math.min(a[0][1], 0.3) * 0.5), legendLeft: true });
  }
  Sim.$("#br-mol").addEventListener("change", brRender);
  Sim.$("#br-ns").addEventListener("change", brRender);
  Sim.$("#br-T").addEventListener("input", brRender);
  Sim.exportCSV(Sim.$("#br-x"), "rotor_q.csv", function () {
    var m = rotor(), th = m.B * HC_K;
    return { header: ["T_K", "q_rot_exact", "q_rot_high_T", "S_rot_exact_J_per_mol_K"], rows: logGrid(0, 3, 80).map(function (t) {
      var dT = t * 1e-4, l1 = Math.log(qRot(m, t + dT)), l0 = Math.log(qRot(m, t - dT)), q = qRot(m, t);
      return [+t.toPrecision(5), +q.toPrecision(7), +(t / (m.sigma * th)).toPrecision(7), +(R * (Math.log(q) + t * (l1 - l0) / (2 * dT))).toFixed(4)];
    }) };
  });

  /* ======================= MICROSTATES ======================= */
  var LNF = [0];
  function lnFact(n) { while (LNF.length <= n) LNF.push(LNF[LNF.length - 1] + Math.log(LNF.length)); return LNF[n]; }
  function lnW(N, q) { return lnFact(q + N - 1) - lnFact(q) - lnFact(N - 1); }
  function showW(l) { var w = Math.exp(l); return w < 1e15 ? Math.round(w).toLocaleString("en-US") : "10^" + (l / Math.LN10).toFixed(2); }
  var bmW = Sim.plot(Sim.$("#bm-W"), { xLabel: "q_A", yLabel: "probability", yMin: 0 });
  var bmH = Sim.plot(Sim.$("#bm-hist"), { xLabel: "coins in a cup", yLabel: "fraction of readings", yMin: 0 });
  var gm = { seed: seed0 + 3, rng: Sim.rng(seed0 + 3), cups: null, tally: [], snaps: 0 };

  function bmRender() {
    var NA = Math.max(1, Math.round(parseFloat(Sim.$("#bm-NA").value))), NB = Math.max(1, Math.round(parseFloat(Sim.$("#bm-NB").value))), Q = Math.max(0, Math.round(parseFloat(Sim.$("#bm-q").value)));
    if (!(NA > 0 && NB > 0 && Q >= 0) || NA > 5000 || NB > 5000 || Q > 5000) return;
    var ls = [], mx = -Infinity, qa;
    for (qa = 0; qa <= Q; qa++) { var l = lnW(NA, qa) + lnW(NB, Q - qa); ls.push(l); if (l > mx) mx = l; }
    var tot = 0;
    ls.forEach(function (l) { tot += Math.exp(l - mx); });
    var probs = ls.map(function (l) { return Math.exp(l - mx) / tot; });
    var peak = 0;
    probs.forEach(function (p, i) { if (p > probs[peak]) peak = i; });
    var within = 0;
    probs.forEach(function (p, i) { if (Math.abs(i - peak) <= 10) within += p; });
    var sA = lnW(NA, peak + 1) - lnW(NA, peak), sB = lnW(NB, Q - peak + 1) - lnW(NB, Q - peak);
    kv(Sim.$("#bm-out"), [
      ["Total microstates W(N<sub>A</sub> + N<sub>B</sub>, q)", showW(lnW(NA + NB, Q))],
      ["Most probable q<sub>A</sub>", peak + " (" + (100 * probs[peak]).toFixed(1) + " % of all microstates)"],
      ["Within ±10 quanta of the peak", (100 * within).toFixed(1) + " %"],
      ["ln W<sub>A</sub>(q<sub>A</sub> + 1) − ln W<sub>A</sub>(q<sub>A</sub>) at the peak", sA.toFixed(3)],
      ["ln W<sub>B</sub>(q<sub>B</sub> + 1) − ln W<sub>B</sub>(q<sub>B</sub>) at the peak", sB.toFixed(3) + " (equal slopes: equal temperatures)"]
    ]);
    bmW.draw([{ type: "bars", data: probs.map(function (p, i) { return [i, p]; }), color: "s1", label: "W_A W_B / W_total" }], { xMin: -0.6, xMax: Q + 0.6 });
    var tb = Sim.$("#bm-Wtable tbody");
    tb.textContent = "";
    var lo = Q <= 60 ? 0 : Math.max(0, peak - 30), hi = Q <= 60 ? Q : Math.min(Q, peak + 30);
    for (qa = lo; qa <= hi; qa++) tb.appendChild(tr([qa, showW(lnW(NA, qa)), showW(lnW(NB, Q - qa)), showW(ls[qa]), probs[qa].toFixed(4)]));
  }

  function gmReset() {
    var N = Math.max(2, Math.min(2000, Math.round(parseFloat(Sim.$("#bm-cups").value) || 10)));
    gm.cups = []; for (var i = 0; i < N; i++) gm.cups.push(1);
    gm.tally = []; gm.snaps = 0; gm.burned = false;
    Sim.$("#bm-seed").textContent = gm.seed;
    gmRender();
  }
  function gmMove() {
    var N = gm.cups.length, from;
    do { from = Math.floor(gm.rng.random() * N); } while (gm.cups[from] === 0);
    gm.cups[from]--;
    gm.cups[Math.floor(gm.rng.random() * N)]++;
  }
  function gmPlay(nSnap) {
    if (!gm.cups) gmReset();
    var N = gm.cups.length, every = Math.max(5, Math.round(N / 2)), i, k;
    if (!gm.burned) { for (i = 0; i < Math.max(20, 2 * N); i++) gmMove(); gm.burned = true; }
    for (k = 0; k < nSnap; k++) {
      for (i = 0; i < every; i++) gmMove();
      gm.cups.forEach(function (c) { while (gm.tally.length <= c) gm.tally.push(0); gm.tally[c]++; });
      gm.snaps++;
    }
    gmRender();
  }
  function gmRender() {
    if (!gm.cups) return;
    var N = gm.cups.length, Qt = N, tot = gm.tally.reduce(function (a, b) { return a + b; }, 0);
    var nmax = Math.max(6, gm.tally.length - 1), obs = [], exact = [], boltz = [];
    for (var n = 0; n <= nmax; n++) {
      obs.push([n, tot ? (gm.tally[n] || 0) / tot : 0]);
      exact.push([n, n <= Qt ? Math.exp(lnW(N - 1, Qt - n) - lnW(N, Qt)) : 0]);
      boltz.push([n, Math.pow(0.5, n + 1)]);
    }
    bmH.draw([
      { type: "bars", data: obs, color: "s1", barWidth: 0.7, label: "your tally (" + tot + " readings)" },
      { type: "points", data: exact, color: "s2", label: "exact for " + N + " cups" },
      { data: boltz, color: "s3", dash: [4, 3], label: "Boltzmann (½)ⁿ⁺¹" }
    ], { xMin: -0.6, xMax: nmax + 0.6, yMax: 0.65 });
    var f = function (n) { return tot ? (gm.tally[n] || 0) / tot : NaN; };
    kv(Sim.$("#bm-hout"), [
      ["Snapshots", gm.snaps + " (" + tot + " cup readings)"],
      ["Fractions with 0, 1, 2 coins", [0, 1, 2].map(function (n) { return isFinite(f(n)) ? f(n).toFixed(3) : "—"; }).join(", ")],
      ["Ratio N(1)/N(0) = e<sup>−ε/k<sub>B</sub>T</sup>", isFinite(f(1) / f(0)) && f(0) > 0 ? (f(1) / f(0)).toFixed(3) + " → k<sub>B</sub>T = " + (-1 / Math.log(f(1) / f(0))).toFixed(2) + " ε" : "—"]
    ]);
  }
  ["#bm-NA", "#bm-NB", "#bm-q"].forEach(function (id) { Sim.$(id).addEventListener("input", bmRender); });
  Sim.$("#bm-big").addEventListener("click", function () { Sim.$("#bm-NA").value = 300; Sim.$("#bm-NB").value = 200; Sim.$("#bm-q").value = 100; bmRender(); });
  Sim.$("#bm-play").addEventListener("click", function () { gmPlay(20); });
  Sim.$("#bm-play1000").addEventListener("click", function () { gmPlay(1000); });
  Sim.$("#bm-reset").addEventListener("click", function () { gm.seed = Sim.newSeed(gm.seed); gm.rng = Sim.rng(gm.seed); gmReset(); });
  Sim.$("#bm-cups").addEventListener("change", gmReset);
  Sim.exportCSV(Sim.$("#bm-x"), "my_cups.csv", function () {
    return { header: ["n", "count"], rows: gm.tally.map(function (c, n) { return [n, c]; }) };
  });

  /* ======================= TABS ======================= */
  var REFRESH = { two: b2Render, ladder: function () { blRange(); blRender(); }, rotor: brRender, micro: function () { bmRender(); if (!gm.cups) gmReset(); else gmRender(); } };
  var tabs = Sim.tabs(Sim.$("#tabs"), function (name) { if (REFRESH[name]) REFRESH[name](); });
  if (preset.key === "rotor") Sim.$("#br-mol").value = "HCl";
  tabs.select(preset.tab || "two");
})();
