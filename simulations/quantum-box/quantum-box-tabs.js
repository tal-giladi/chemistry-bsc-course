/* quantum-box simulation, part 2: vibrations (lesson 12.4), the rigid rotor and the hydrogen
 * atom (lesson 12.5), the conjugated dye series (lessons 12.2 and 30.4), and the tab set-up.
 * Needs quantum-box.js (global QB) and ../common/sim.js (global Sim).
 *
 * Data: H35Cl we = 2990.9463, wexe = 52.8186, re = 1.274552 A, B0 = 10.4398 (Be - ae/2),
 * D = 5.32e-4 cm^-1; 12C16O B0 = 1.9225 (Be 1.93128087, ae 0.01750441), D = 6.12e-6 cm^-1
 * (NIST Chemistry WebBook, Huber and Herzberg). Atomic masses (NIST): 1H 1.00782503207,
 * 2H 2.01410177812, 35Cl 34.968852682, 37Cl 36.965902602, 12C 12, 16O 15.99491462.
 * Isotopes keep the potential: we ~ mu^-1/2, wexe ~ mu^-1.
 * Dyes (labs/module-30/cyanine_dyes.csv): 2,2'-cyanines p = 3, 5, 7 at 523, 605, 705 nm (methanol);
 * 4,4'-carbocyanine p = 9 at 708 nm; beta-carotene N = 22 at 451 nm (hexane).
 * Kuhn's model: N = p + 3, L = (N + alpha) l, lambda = 8 m_e c L^2 / (h (N + 1)); polyene gap
 * V0 (1 - 1/N) added to the HOMO-LUMO energy when bond alternation is on.
 */
(function () {
  "use strict";
  var Q = window.QB, K = Q.K, C = Sim.C, TAU = 2 * Math.PI;
  var MASS = { H: 1.00782503207, D: 2.01410177812, Cl35: 34.968852682, Cl37: 36.965902602 };
  function red(a, b) { return a * b / (a + b); }
  var MU_HCL = red(MASS.H, MASS.Cl35);
  var MOLS = {
    HCl: { mu: MU_HCL },
    DCl: { mu: red(MASS.D, MASS.Cl35) },
    H37: { mu: red(MASS.H, MASS.Cl37) }
  };

  /* ======================= VIBRATIONS ======================= */
  var oPlot = Sim.plot(Sim.$("#qo-plot"), { xLabel: "bond length r / Å", yLabel: "E / cm⁻¹" });
  var oLast = null;

  function oSetMolecule() {
    var m = Sim.$("#qo-mol").value;
    if (!MOLS[m]) return;
    var ratio = MU_HCL / MOLS[m].mu;
    Sim.$("#qo-we").value = (2990.9463 * Math.sqrt(ratio)).toFixed(4);
    Sim.$("#qo-wexe").value = (52.8186 * ratio).toFixed(4);
    Sim.$("#qo-mu").value = MOLS[m].mu.toFixed(6);
    Sim.$("#qo-re").value = "1.274552";
  }
  function oVals() {
    function n(id) { return parseFloat(Sim.$(id).value); }
    return { we: n("#qo-we"), wexe: n("#qo-wexe"), mu: n("#qo-mu"), re: n("#qo-re"), morse: Sim.$("#qo-morse").checked, n: Math.round(n("#qo-n")), show: Sim.$("#qo-show").value };
  }
  function oRender() {
    var v = oVals();
    if (!(v.we > 0 && v.wexe > 0 && v.mu > 0 && v.n >= 1)) return;
    var c = K.HB2M_U / v.mu, Kf = v.we * v.we / (2 * c), De = v.we * v.we / (4 * v.wexe), a = Math.sqrt(Kf / (2 * De));
    var x = Q.linspace(-0.6, 3.0, 3001), V = new Float64Array(x.length), i;
    for (i = 0; i < x.length; i++) V[i] = v.morse ? De * Math.pow(1 - Math.exp(-a * x[i]), 2) : 0.5 * Kf * x[i] * x[i];
    var nMax = v.morse ? Math.min(v.n, Math.floor(v.we / (2 * v.wexe) - 0.5)) : v.n;
    var sol = Q.solve(x, V, c, Math.max(1, nMax)), dx = sol.dx;
    oLast = { v: v, sol: sol };
    var tb = Sim.$("#qo-table tbody"), turn = [];
    tb.textContent = "";
    sol.E.forEach(function (E, k) {
      var form = v.morse ? v.we * (k + 0.5) - v.wexe * (k + 0.5) * (k + 0.5) : v.we * (k + 0.5);
      var p = sol.psi[k], beyond = 0, mean = 0, lo = Infinity, hi = -Infinity;
      for (i = 0; i < x.length; i++) {
        var w = p[i] * p[i] * dx;
        mean += x[i] * w;
        if (V[i] > E) beyond += w; else { lo = Math.min(lo, x[i]); hi = Math.max(hi, x[i]); }
      }
      turn.push([lo, hi]);
      tb.appendChild(Q.tr([k, E.toFixed(1), form.toFixed(1), k ? (E - sol.E[k - 1]).toFixed(1) : "—", Q.nodes(p), (v.re + mean).toFixed(3), beyond.toFixed(3)]));
    });
    var E = sol.E, ext = [];
    ext.push(["Force constant k", (Kf * C.h * K.C_CM * 1e20).toFixed(1) + " N/m"]);
    ext.push(["Zero-point energy (numerical)", E[0].toFixed(1) + " cm⁻¹ = " + (E[0] * K.CM1_KJMOL).toFixed(2) + " kJ/mol (harmonic ½ω<sub>e</sub> = " + (v.we / 2).toFixed(1) + ")"]);
    if (E.length > 1) ext.push(["Fundamental 0 → 1", (E[1] - E[0]).toFixed(1) + " cm⁻¹ (ω<sub>e</sub> = " + v.we.toFixed(1) + ")"]);
    if (E.length > 2) ext.push(["First overtone 0 → 2", (E[2] - E[0]).toFixed(1) + " cm⁻¹ (twice the fundamental would be " + (2 * (E[1] - E[0])).toFixed(1) + ")"]);
    if (E.length > 1) ext.push(["Fraction in v = 1 at 298 K", Math.exp(-(E[1] - E[0]) * K.HC_K / 298.15).toExponential(2)]);
    ext.push(["Zero-point length α = (2c/k)<sup>¼</sup>", Math.pow(2 * c / Kf, 0.25).toFixed(4) + " Å"]);
    if (v.morse) {
      ext.push(["Morse D<sub>e</sub> = ω<sub>e</sub>²/4ω<sub>e</sub>x<sub>e</sub>", De.toFixed(0) + " cm⁻¹ = " + (De * K.CM1_EV).toFixed(2) + " eV; a = " + a.toFixed(4) + " Å⁻¹"]);
      ext.push(["D₀ = D<sub>e</sub> − G(0)", (De - E[0]).toFixed(0) + " cm⁻¹ = " + ((De - E[0]) * K.CM1_EV).toFixed(2) + " eV (HCl measured 4.43 eV)"]);
      if (nMax < v.n) ext.push(["Levels", "a Morse well holds only " + (Math.floor(v.we / (2 * v.wexe) - 0.5) + 1) + " bound levels; showing " + nMax]);
    }
    Q.kv(Sim.$("#qo-extra"), ext);
    // plot in r = re + x
    var top = E[E.length - 1] + (E.length > 1 ? (E[E.length - 1] - E[E.length - 2]) : v.we) * 0.9;
    var pot = [];
    for (i = 0; i < x.length; i += 5) if (V[i] < top * 1.6) pot.push([v.re + x[i], V[i]]);
    var ser = [{ data: pot, color: "ink", width: 2, label: v.morse ? "Morse V(r)" : "harmonic V(r)" }];
    var amp = 0.42 * (E.length > 1 ? Math.min(E[1] - E[0], E[E.length - 1] - E[E.length - 2]) : v.we);
    var xr = Q.linspace(v.re - 0.6, v.re + 3.0, 3001);
    ser = ser.concat(Q.levelSeries(xr, sol, sol.E.length, v.show, amp, function (k) { return v.re + turn[k][0]; }, function (k) { return v.re + turn[k][1]; }, 0.3));
    ser.forEach(function (s) { if (s.label && s.label.indexOf("n = ") === 0) s.label = "v = " + (parseInt(s.label.slice(4), 10) - 1); });
    oPlot.draw(ser, { xMin: v.re - 0.45, xMax: v.re + (v.morse ? 1.6 : 0.6), yMin: 0, yMax: top });
  }
  ["#qo-we", "#qo-wexe", "#qo-mu", "#qo-re", "#qo-morse", "#qo-n", "#qo-show"].forEach(function (id) {
    Sim.$(id).addEventListener("input", function () { if (id !== "#qo-morse" && id !== "#qo-n" && id !== "#qo-show") Sim.$("#qo-mol").value = "custom"; oRender(); });
    Sim.$(id).addEventListener("change", oRender);
  });
  Sim.$("#qo-mol").addEventListener("change", function () { oSetMolecule(); oRender(); });
  Sim.exportCSV(Sim.$("#qo-x"), "vibrational_levels.csv", function () {
    if (!oLast) return null;
    var v = oLast.v;
    return { header: ["v", "E_numerical_cm", "E_formula_cm", "model"], rows: oLast.sol.E.map(function (E, k) { return [k, +E.toFixed(3), +(v.morse ? v.we * (k + 0.5) - v.wexe * (k + 0.5) * (k + 0.5) : v.we * (k + 0.5)).toFixed(3), v.morse ? "Morse" : "harmonic"]; }) };
  });
  Q.refresh.oscillator = oRender;

  /* ======================= ROTOR AND HYDROGEN ======================= */
  var ROT = { HCl: { B: 10.4398, D: 0.000532, mu: MU_HCL }, CO: { B: 1.9225, D: 0.00000612, mu: red(12, 15.99491462) } };
  var rPlot = Sim.plot(Sim.$("#qr-plot"), { xLabel: "J", yLabel: "fraction of molecules", yMin: 0 });
  var hPlot = Sim.plot(Sim.$("#qh-plot"), { xLabel: "r / bohr", yLabel: "u² = r²R² / bohr⁻¹", xMin: 0, yMin: 0 });
  var rLast = null;

  function rVals() {
    function n(id) { return parseFloat(Sim.$(id).value); }
    return { B: n("#qr-B"), D: n("#qr-D"), mu: n("#qr-mu"), T: n("#qr-T") };
  }
  function rRender() {
    var v = rVals();
    Sim.$("#qr-T-out").textContent = v.T.toFixed(0);
    if (!(v.B > 0 && v.T > 0)) return;
    var kT = v.T / K.HC_K, rows = [], q = 0, J;
    for (J = 0; J < 400; J++) {
      var F = v.B * J * (J + 1) - v.D * J * J * (J + 1) * (J + 1), w = (2 * J + 1) * Math.exp(-F / kT);
      rows.push({ J: J, F: F, w: w });
      q += w;
      if (J > 3 && w / q < 1e-7) break;
    }
    rows.forEach(function (r) { r.f = r.w / q; });
    var best = rows.reduce(function (a, b) { return b.f > a.f ? b : a; });
    var shown = rows.filter(function (r) { return r.f > 1e-3 || r.J <= 6; });
    rLast = { v: v, rows: rows };
    rPlot.draw([{ type: "bars", data: shown.map(function (r) { return [r.J, r.f]; }), color: "s1", label: "N_J / N" }, { type: "vline", x: Math.sqrt(kT / (2 * v.B)) - 0.5, color: "s2", dash: [4, 3], width: 1.5, label: "J ≈ √(kT/2hcB) − ½" }], { xMin: -0.6, xMax: Math.max(6, shown[shown.length - 1].J + 0.6) });
    var I = C.h / (8 * Math.PI * Math.PI * K.C_CM * v.B), r = Math.sqrt(I / (v.mu * C.u)) * 1e10;
    Q.kv(Sim.$("#qr-out"), [
      ["k<sub>B</sub>T/hc", kT.toFixed(1) + " cm⁻¹"],
      ["Most populated level", "J = " + best.J + " (formula √(k<sub>B</sub>T/2hcB) − ½ = " + (Math.sqrt(kT / (2 * v.B)) - 0.5).toFixed(2) + ")"],
      ["Partition function q (sum)", q.toFixed(3) + " (k<sub>B</sub>T/hcB = " + (kT / v.B).toFixed(3) + ")"],
      ["Bond length from B: I = h/(8π²cB), r = √(I/μ)", r.toFixed(4) + " Å"],
      ["First line 2B − 4D", (2 * v.B - 4 * v.D).toFixed(3) + " cm⁻¹ = " + ((2 * v.B - 4 * v.D) * K.C_CM * 1e-9).toFixed(2) + " GHz"]
    ]);
    var tb = Sim.$("#qr-table tbody");
    tb.textContent = "";
    shown.forEach(function (rw) {
      var j1 = rw.J + 1, line = 2 * v.B * j1 - 4 * v.D * j1 * j1 * j1;
      tb.appendChild(Q.tr([rw.J + " → " + j1, line.toFixed(2), (line * K.C_CM * 1e-9).toFixed(2), rw.f.toFixed(4)]));
    });
  }
  function hRender() {
    var l = parseInt(Sim.$("#qh-l").value, 10), n = Math.max(1, Math.min(4, parseInt(Sim.$("#qh-n").value, 10) || 3)), useMu = Sim.$("#qh-mu").checked;
    var N = 6000, rmax = 80, r = new Float64Array(N), V = new Float64Array(N), h = rmax / (N + 1), i;
    for (i = 0; i < N; i++) { r[i] = (i + 1) * h; V[i] = l * (l + 1) / (2 * r[i] * r[i]) - 1 / r[i]; }
    var f = useMu ? 1 / (1 + 1 / 1836.15267343) : 1;
    var sol = Q.solve(r, V, 0.5, n);
    var tb = Sim.$("#qh-table tbody"), ser = [], letters = "spdf";
    tb.textContent = "";
    sol.E.forEach(function (E, k) {
      var nn = l + 1 + k, p = sol.psi[k], mean = 0, best = 0, rb = 0;
      for (i = 0; i < N; i++) { var w = p[i] * p[i]; mean += r[i] * w * h; if (w > best) { best = w; rb = r[i]; } }
      tb.appendChild(Q.tr([nn + letters[l], (E * f).toFixed(5), (-0.5 / (nn * nn) * f).toFixed(5), Q.nodes(p), (mean / f).toFixed(3), (rb / f).toFixed(3)]));
      var data = [];
      for (i = 0; i < N; i += 10) if (r[i] < 4 * nn * nn + 10) data.push([r[i] / f, p[i] * p[i] * f]);
      ser.push({ data: data, color: "s" + (k + 1), label: nn + letters[l] });
    });
    hPlot.draw(ser, { xMax: Math.min(60, 4.5 * Math.pow(l + n, 2) + 6) });
    Q.kv(Sim.$("#qh-out"), [
      ["Ionisation energy", (0.5 * K.HARTREE_EV * f).toFixed(3) + " eV" + (useMu ? " (with the reduced mass; NIST 13.598)" : " (infinite nuclear mass)")],
      ["Bohr radius a₀", "1 bohr = 52.92 pm"]
    ]);
  }
  ["#qr-B", "#qr-D", "#qr-mu", "#qr-T"].forEach(function (id) {
    Sim.$(id).addEventListener("input", function () { if (id !== "#qr-T") Sim.$("#qr-mol").value = "custom"; rRender(); });
  });
  Sim.$("#qr-mol").addEventListener("change", function () {
    var m = ROT[this.value];
    if (m) { Sim.$("#qr-B").value = m.B; Sim.$("#qr-D").value = m.D; Sim.$("#qr-mu").value = m.mu.toFixed(6); }
    rRender();
  });
  ["#qh-l", "#qh-n", "#qh-mu"].forEach(function (id) { Sim.$(id).addEventListener("change", hRender); Sim.$(id).addEventListener("input", hRender); });
  Sim.exportCSV(Sim.$("#qr-x"), "rotor_levels.csv", function () {
    if (!rLast) return null;
    var v = rLast.v;
    return { header: ["J", "F_cm", "degeneracy", "fraction", "line_J_to_J+1_cm"], rows: rLast.rows.filter(function (r) { return r.f > 1e-6; }).map(function (r) { var j1 = r.J + 1; return [r.J, +r.F.toFixed(4), 2 * r.J + 1, +r.f.toExponential(5), +(2 * v.B * j1 - 4 * v.D * j1 * j1 * j1).toFixed(4)]; }) };
  });
  Q.refresh.rotor = function () { rRender(); hRender(); };

  /* ======================= DYE SERIES ======================= */
  var DYES = {
    cy: [
      { name: "2,2′-cyanine", p: 3, lam: 523, fit: true },
      { name: "2,2′-carbocyanine (pinacyanol)", p: 5, lam: 605, fit: true },
      { name: "2,2′-dicarbocyanine", p: 7, lam: 705, fit: true },
      { name: "4,4′-carbocyanine (blind test)", p: 9, lam: 708, fit: false }
    ],
    po: [{ name: "β-carotene (hexane)", p: 11, lam: 451, fit: false }]
  };
  var dPlot = Sim.plot(Sim.$("#qd-plot"), { xLabel: "π electrons N", yLabel: "λ / nm" });
  var dFit = null;

  function dVals() {
    function n(id) { return parseFloat(Sim.$(id).value); }
    var fam = Sim.$("#qd-fam").value, p = Math.round(n("#qd-p"));
    return { fam: fam, p: p, N: fam === "cy" ? p + 3 : 2 * p, l: n("#qd-l"), a: n("#qd-a"), alt: Sim.$("#qd-alt").checked, V0: n("#qd-V0") };
  }
  function lambdaBox(N, l, a) { var L = (N + a) * l * 1e-9; return 8 * K.ME * C.c * L * L / (C.h * (N + 1)) * 1e9; }
  function lambdaModel(N, v, alt) {
    var lb = lambdaBox(N, v.l, v.a);
    if (!alt) return lb;
    var dE = K.HC_EV_NM / lb + v.V0 * (1 - 1 / N);
    return K.HC_EV_NM / dE;
  }
  function famN(fam, p) { return fam === "cy" ? p + 3 : 2 * p; }

  function wlRGB(lam) {
    var r = 0, g = 0, b = 0;
    if (lam >= 380 && lam < 440) { r = (440 - lam) / 60; b = 1; }
    else if (lam < 490 && lam >= 440) { g = (lam - 440) / 50; b = 1; }
    else if (lam < 510 && lam >= 490) { g = 1; b = (510 - lam) / 20; }
    else if (lam < 580 && lam >= 510) { r = (lam - 510) / 70; g = 1; }
    else if (lam < 645 && lam >= 580) { r = 1; g = (645 - lam) / 65; }
    else if (lam <= 780 && lam >= 645) { r = 1; }
    var f = lam < 420 ? 0.3 + 0.7 * (lam - 380) / 40 : lam > 700 ? 0.3 + 0.7 * (780 - lam) / 80 : 1;
    if (lam < 380 || lam > 780) return null;
    return [r, g, b].map(function (c) { return Math.round(255 * Math.pow(c * f, 0.8)); });
  }
  function colourName(lam) {
    if (lam < 380) return "ultraviolet";
    if (lam < 450) return "violet"; if (lam < 495) return "blue"; if (lam < 570) return "green";
    if (lam < 590) return "yellow"; if (lam < 620) return "orange"; if (lam <= 780) return "red";
    return "infrared";
  }

  function dLevels(v, lam) {
    var cv = Sim.$("#qd-levels"), dpr = window.devicePixelRatio || 1, W = cv.clientWidth || 200, H = cv.clientHeight || 300;
    if (cv.width !== Math.round(W * dpr) || cv.height !== Math.round(H * dpr)) { cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr); }
    var ctx = cv.getContext("2d");
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.fillStyle = Sim.color("plot-bg"); ctx.fillRect(0, 0, W, H);
    var L = (v.N + v.a) * v.l, E1 = K.H2_8ME / (L * L), homo = v.N / 2, top = homo + 2;
    var gapAlt = v.alt ? v.V0 * (1 - 1 / v.N) : 0;
    function En(n) { return E1 * n * n + (n > homo ? gapAlt : 0); }
    var Emax = En(top) * 1.06, y0 = H - 18, y1 = 14;
    function Y(E) { return y0 - (y0 - y1) * E / Emax; }
    ctx.font = "11px " + (getComputedStyle(document.body).fontFamily || "sans-serif");
    for (var n = 1; n <= top; n++) {
      var y = Y(En(n));
      ctx.strokeStyle = Sim.color(n === homo ? "s1" : n === homo + 1 ? "s2" : "ink"); ctx.lineWidth = n === homo || n === homo + 1 ? 2.2 : 1.2;
      ctx.beginPath(); ctx.moveTo(W * 0.3, y); ctx.lineTo(W * 0.8, y); ctx.stroke();
      ctx.fillStyle = Sim.color("muted"); ctx.textAlign = "right";
      if (n === homo || n === homo + 1 || n === 1) ctx.fillText((n === homo ? "HOMO " : n === homo + 1 ? "LUMO " : "") + "n=" + n, W * 0.28, y + 4);
      if (n <= homo) {
        ctx.fillStyle = Sim.color("s1"); ctx.textAlign = "center";
        ctx.fillText("↑", W * 0.5, y - 1); ctx.fillText("↓", W * 0.6, y - 1);
      }
    }
    ctx.strokeStyle = Sim.color("s6"); ctx.fillStyle = Sim.color("s6"); ctx.lineWidth = 2;
    var ya = Y(En(homo)), yb = Y(En(homo + 1)), xa = W * 0.88;
    ctx.beginPath(); ctx.moveTo(xa, ya); ctx.lineTo(xa, yb + 4); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(xa - 4, yb + 8); ctx.lineTo(xa, yb); ctx.lineTo(xa + 4, yb + 8); ctx.fill();
    ctx.textAlign = "left"; ctx.fillStyle = Sim.color("muted");
    ctx.fillText(v.N + " π electrons", 4, H - 4);
    if (v.alt) ctx.fillText("gap + V₀(1 − 1/N)", W * 0.3, Y(En(homo + 1)) - 6);
  }

  function dRender() {
    var v = dVals();
    Sim.$("#qd-p-out").textContent = v.p;
    Sim.$("#qd-V0-f").hidden = !v.alt;
    var pIn = Sim.$("#qd-p");
    if (v.fam === "cy") { pIn.min = 1; pIn.max = 15; pIn.step = 2; Sim.$("#qd-p-label").textContent = "Carbons on the path between the nitrogens, p"; }
    else { pIn.min = 2; pIn.max = 15; pIn.step = 1; Sim.$("#qd-p-label").textContent = "Conjugated C=C bonds"; }
    if (!(v.l > 0) || v.N + v.a <= 0) return;
    var lam = lambdaModel(v.N, v, v.alt), L = (v.N + v.a) * v.l;
    var E1 = K.H2_8ME / (L * L), dE = K.HC_EV_NM / lam;
    var out = [
      ["π electrons N, box length L = (N + α)ℓ", v.N + ", " + L.toFixed(3) + " nm"],
      ["HOMO → LUMO", "n = " + v.N / 2 + " → " + (v.N / 2 + 1) + ", ΔE = " + dE.toFixed(3) + " eV" + (v.alt ? " (box " + (K.HC_EV_NM / lambdaBox(v.N, v.l, v.a)).toFixed(3) + " + alternation " + (v.V0 * (1 - 1 / v.N)).toFixed(3) + ")" : "")],
      ["Predicted λ<sub>max</sub>", lam.toFixed(0) + " nm (" + colourName(lam) + " light absorbed)"],
      ["E₁ = h²/(8m<sub>e</sub>L²)", E1.toFixed(4) + " eV"]
    ];
    var meas = DYES[v.fam].filter(function (d) { return famN(v.fam, d.p) === v.N; })[0];
    if (meas) out.push(["Measured", meas.lam + " nm, " + meas.name + " (model " + (lam - meas.lam >= 0 ? "+" : "") + (lam - meas.lam).toFixed(0) + " nm)"]);
    Q.kv(Sim.$("#qd-out"), out);
    var rgb = wlRGB(lam);
    Sim.$("#qd-sw1").style.background = rgb ? "rgb(" + rgb.join(",") + ")" : "transparent";
    Sim.$("#qd-sw2").style.background = rgb ? "rgb(" + rgb.map(function (c) { return 255 - c; }).join(",") + ")" : "transparent";
    Sim.$("#qd-sw1").title = rgb ? "absorbed: " + colourName(lam) : "outside the visible range";
    dLevels(v, lam);
    // series plot and table
    var ser = [], line = [], lineNo = [], pList = [], pmax = 15, p;
    for (p = v.fam === "cy" ? 1 : 2; p <= pmax; p += v.fam === "cy" ? 2 : 1) pList.push(p);
    pList.forEach(function (pp) { var N = famN(v.fam, pp); line.push([N, lambdaModel(N, v, v.alt)]); lineNo.push([N, lambdaModel(N, v, false)]); });
    ser.push({ data: line, color: "s1", label: v.alt ? "box + alternation" : "box model" });
    if (v.alt) ser.push({ data: lineNo, color: "muted", dash: [4, 3], width: 1.3, label: "box without alternation" });
    var fitPts = DYES[v.fam].filter(function (d) { return d.fit; }), blind = DYES[v.fam].filter(function (d) { return !d.fit; });
    if (fitPts.length) ser.push({ type: "points", data: fitPts.map(function (d) { return [famN(v.fam, d.p), d.lam]; }), color: "s2", label: "measured" });
    if (blind.length) ser.push({ type: "points", hollow: true, size: 5, data: blind.map(function (d) { return [famN(v.fam, d.p), d.lam]; }), color: "s6", label: v.fam === "cy" ? "4,4′ dye (not fitted)" : "β-carotene" });
    ser.push({ type: "points", data: [[v.N, lam]], color: "s4", size: 4, label: "current" });
    dPlot.draw(ser, { yMin: 0 });
    var tb = Sim.$("#qd-table tbody");
    tb.textContent = "";
    DYES[v.fam].forEach(function (d) {
      var N = famN(v.fam, d.p), lm = lambdaModel(N, v, v.alt);
      tb.appendChild(Q.tr([d.name, N, ((N + v.a) * v.l).toFixed(3), lm.toFixed(1), d.lam, (lm - d.lam >= 0 ? "+" : "") + (lm - d.lam).toFixed(1)]));
    });
    dFitShow();
  }

  function dFitShow() {
    if (!dFit) { Q.kv(Sim.$("#qd-fitout"), []); return; }
    var f = dFit;
    Q.kv(Sim.$("#qd-fitout"), [
      ["Fit to the three 2,2′ dyes: ℓ", Sim.fmtU(f.l, f.ul, "nm")],
      ["α", Sim.fmtU(f.a, f.ua)],
      ["Correlation of ℓ and α", f.r.toFixed(3)],
      ["Residuals (model − measured)", f.res.map(function (x) { return (-x >= 0 ? "+" : "") + (-x).toFixed(1); }).join(", ") + " nm (1 degree of freedom)"],
      ["Blind prediction for the 4,4′ dye (p = 9)", f.pred.toFixed(0) + " nm against 708 nm (" + ((f.pred / 708 - 1) * 100).toFixed(0) + " %)"]
    ]);
  }

  function dDoFit() {
    var pts = DYES.cy.filter(function (d) { return d.fit; }), l = 0.139, a = 0, i;
    for (var it = 0; it < 100; it++) {
      var JTJ = [[0, 0], [0, 0]], JTr = [0, 0];
      pts.forEach(function (d) {
        var N = d.p + 3, m = lambdaBox(N, l, a), J = [2 * m / l, 2 * m / (N + a)], r = d.lam - m;
        for (var x = 0; x < 2; x++) { JTr[x] += J[x] * r; for (var y = 0; y < 2; y++) JTJ[x][y] += J[x] * J[y]; }
      });
      var det = JTJ[0][0] * JTJ[1][1] - JTJ[0][1] * JTJ[1][0];
      var dl = (JTJ[1][1] * JTr[0] - JTJ[0][1] * JTr[1]) / det, da = (JTJ[0][0] * JTr[1] - JTJ[1][0] * JTr[0]) / det;
      l += dl; a += da;
      if (Math.abs(dl) < 1e-12 && Math.abs(da) < 1e-10) break;
    }
    var res = [], ssr = 0, H = [[0, 0], [0, 0]];
    pts.forEach(function (d) {
      var N = d.p + 3, m = lambdaBox(N, l, a), J = [2 * m / l, 2 * m / (N + a)];
      res.push(d.lam - m); ssr += Math.pow(d.lam - m, 2);
      for (var x = 0; x < 2; x++) for (var y = 0; y < 2; y++) H[x][y] += J[x] * J[y];
    });
    var s2 = ssr / (pts.length - 2), det2 = H[0][0] * H[1][1] - H[0][1] * H[1][0];
    var cov = [[H[1][1] / det2 * s2, -H[0][1] / det2 * s2], [-H[1][0] / det2 * s2, H[0][0] / det2 * s2]];
    dFit = { l: l, a: a, ul: Math.sqrt(cov[0][0]), ua: Math.sqrt(cov[1][1]), r: cov[0][1] / Math.sqrt(cov[0][0] * cov[1][1]), res: res, pred: lambdaBox(12, l, a) };
    Sim.$("#qd-fam").value = "cy";
    Sim.$("#qd-l").value = l.toFixed(4); Sim.$("#qd-a").value = a.toFixed(2); Sim.$("#qd-alt").checked = false;
    dRender();
  }

  ["#qd-fam", "#qd-p", "#qd-l", "#qd-a", "#qd-alt", "#qd-V0"].forEach(function (id) {
    Sim.$(id).addEventListener("input", dRender);
    Sim.$(id).addEventListener("change", dRender);
  });
  Sim.$("#qd-fam").addEventListener("change", function () {
    Sim.$("#qd-p").value = this.value === "cy" ? 3 : 11;
    if (this.value === "po") { Sim.$("#qd-alt").checked = true; Sim.$("#qd-l").value = "0.139"; Sim.$("#qd-a").value = "0"; }
    dRender();
  });
  Sim.$("#qd-cal").addEventListener("click", function () {
    var l = parseFloat(Sim.$("#qd-l").value), N = 6;
    var Lnm = Math.sqrt(523e-9 * C.h * (N + 1) / (8 * K.ME * C.c)) * 1e9;
    Sim.$("#qd-fam").value = "cy"; Sim.$("#qd-alt").checked = false; Sim.$("#qd-p").value = 3;
    Sim.$("#qd-a").value = (Lnm / l - N).toFixed(2);
    dRender();
  });
  Sim.$("#qd-fit").addEventListener("click", dDoFit);
  Sim.$("#qd-reset").addEventListener("click", function () { Sim.$("#qd-l").value = "0.139"; Sim.$("#qd-a").value = "0"; dFit = null; dRender(); });
  Sim.exportCSV(Sim.$("#qd-x"), "dye_series.csv", function () {
    var v = dVals(), rows = [];
    DYES[v.fam].forEach(function (d) { var N = famN(v.fam, d.p); rows.push([d.name, d.p, N, +((N + v.a) * v.l).toFixed(4), +lambdaModel(N, v, v.alt).toFixed(2), d.lam]); });
    return { header: ["dye", "p_or_CC", "pi_electrons", "L_nm", "lambda_model_nm", "lambda_measured_nm"], rows: rows };
  });
  Q.refresh.dye = dRender;

  /* ======================= TABS ======================= */
  var tabs = Sim.tabs(Sim.$("#tabs"), function (name) { if (Q.refresh[name]) Q.refresh[name](); });
  Sim.onTheme(function () { if (!Sim.$("#tab-dye").hidden) dRender(); });
  if (Q.preset.key === "tunnel") { Sim.$("#qt-d").value = "0.30"; }
  if (Q.preset.key === "oscillator") { Sim.$("#qo-morse").checked = false; }
  tabs.select(Q.preset.tab || "box");
})();
