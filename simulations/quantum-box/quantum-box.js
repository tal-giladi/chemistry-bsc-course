/* quantum-box simulation, part 1: constants, the finite-difference solver, presets, the
 * particle in a box (lesson 12.2) and tunnelling (lesson 12.3). Part 2 (quantum-box-tabs.js) has
 * vibrations, the rotor and hydrogen, the dye series and the tab set-up. Uses ../common/sim.js.
 *
 * Solver: -c psi'' + V psi = E psi on a uniform grid, psi = 0 just outside it. The matrix is
 * tridiagonal (2t + V_i on the diagonal, -t beside it, t = c/dx^2); its lowest eigenvalues are
 * found by Sturm-sequence bisection and the eigenvectors by inverse iteration with a pivoted
 * tridiagonal solve (LAPACK dgtsv algorithm). Same method as labs/module-12/qm_solver.py.
 * Constants CODATA 2022 (NIST): h, c, e exact; m_e = 9.1093837139e-31 kg; u = 1.66053906892e-27 kg;
 * m_p/m_e = 1836.15267343, m_d/m_e = 3670.48296788, m_mu/m_e = 206.7682827.
 * hbar^2/(2 m_e) = 0.0380998 eV nm^2; hbar^2/(2 u) = 16.8576 cm^-1 A^2; h^2/(8 m_e) = 0.376030 eV nm^2.
 */
(function (global) {
  "use strict";
  var C = Sim.C, TAU = 2 * Math.PI;
  var ME = 9.1093837139e-31, HBAR = C.h / TAU;
  var K = {
    ME: ME,
    HB2M_E: HBAR * HBAR / (2 * ME) / C.e * 1e18,              // eV nm^2
    HB2M_U: HBAR * HBAR / (2 * C.u) / (C.h * C.c * 100) * 1e20, // cm^-1 A^2
    H2_8ME: C.h * C.h / (8 * ME) / C.e * 1e18,                 // eV nm^2
    HC_EV_NM: C.h * C.c / C.e * 1e9,                            // 1239.84 eV nm
    C_CM: C.c * 100,
    HC_K: C.h * C.c * 100 / C.kB,                               // 1.438777 cm K
    CM1_KJMOL: C.h * C.c * 100 * C.NA / 1000,                   // 0.0119627 kJ/mol per cm^-1
    CM1_EV: C.h * C.c * 100 / C.e,
    HARTREE_EV: 27.211386245981
  };

  var PRESETS = {
    box: {
      title: "Particle in a box", tab: "box",
      what: "A particle trapped between two walls can only have energies E<sub>n</sub> = n²h²/(8mL²): no n = 0, n − 1 nodes in state n, and levels that spread as n² and crowd together for a heavier particle or a longer box. The solver turns the Schrödinger equation into a matrix eigenvalue problem, the method used for every other tab.",
      task: "Electron in a 1.00 nm box: compare the numerical E₁ … E₅ with the exact values, then change L and the mass and watch the levels move as 1/mL². Switch to finite walls 1.00 eV high and count the bound states.",
      target: "E₁ = 0.376 eV and E<sub>n</sub> = 0.376 n² eV, matched to better than 10⁻³ with 200 points; the 1.00 eV well holds 2 bound states at 0.191 and 0.706 eV, with about 6 % of the ground state inside the walls."
    },
    tunnel: {
      title: "Tunnelling through a barrier", tab: "tunnel",
      what: "Where the potential is higher than the energy, the wavefunction does not stop: it decays as e<sup>−κx</sup>, κ = √(2m(V₀ − E))/ħ. A thin enough barrier lets part of the wave through. In a double well, the leaking wavefunctions mix into a symmetric and an antisymmetric pair, split by the tunnelling splitting Δ.",
      task: "Send a 1.00 eV electron at a 2.00 eV barrier and change the width from 0.3 to 0.5 nm. Then switch to the double well and compare NH₃ with ND₃; narrow and raise the barrier.",
      target: "T falls from 0.169 to 0.0235, about 7 times. The ammonia-like well gives splittings near 0.87 cm⁻¹ (26 GHz) for NH₃ and 0.049 cm⁻¹ for ND₃ (measured 0.79 and 0.053 cm⁻¹)."
    },
    oscillator: {
      title: "Harmonic oscillator levels and wavefunctions", tab: "oscillator",
      what: "A bond near the bottom of its well is a quantum harmonic oscillator: equally spaced levels (v + ½)ħω and a zero-point energy. A real bond is better described by the Morse potential, whose levels crowd together towards dissociation, so the fundamental lies below ω<sub>e</sub> and the overtone below twice the fundamental.",
      task: "H³⁵Cl from the NIST constants: read the harmonic levels, then switch on anharmonicity and check that the spacing shrinks as you go up, and that the v = 0 wavefunction leaks past the classical turning points. Then switch to D³⁵Cl.",
      target: "Morse levels 1482.3, 4367.5, 7147.2, 9821.2 cm⁻¹; fundamental 2885.3 cm⁻¹ (harmonic 2990.9), overtone 5664.9 cm⁻¹; about 16 % of the harmonic v = 0 probability lies beyond the turning points; DCl fundamental near 2091 cm⁻¹."
    },
    rotor: {
      title: "Rigid rotor levels and populations", tab: "rotor",
      what: "A rotating diatomic has levels BJ(J + 1), each 2J + 1 times degenerate, and absorbs at 2B(J + 1). Because rotational gaps are small compared with k<sub>B</sub>T, many levels are filled, and the degeneracy pushes the most populated level above J = 0. The same angular momentum, with a Coulomb potential, gives the hydrogen atom.",
      task: "Set B = 10.4 cm⁻¹ (HCl) and T = 298 K and find the most populated level. Cool to 50 K and find the new peak. Then look at the hydrogen radial functions for ℓ = 0, 1, 2.",
      target: "The peak is at J = 3 at 298 K (J = 2 is close behind) and at J = 1 at 50 K; hydrogen energies −0.5, −0.125, −0.0556 hartree for n = 1, 2, 3, the same for every allowed ℓ."
    },
    dye: {
      title: "Conjugated dye series", tab: "dye",
      what: "The π electrons of a cyanine dye move along an almost flat chain: a particle in a box of length L = (N + α)ℓ holding N electrons, two per level. The lowest absorption lifts an electron from the HOMO (level N/2) to the LUMO, at λ = 8m<sub>e</sub>cL²/(h(N + 1)). Polyenes have alternating bonds and an extra gap, so they break the simple box.",
      task: "Start with p = 3: find the HOMO, the LUMO and λ. Step p to 5, 7 and 9. Increase the end extension α until p = 3 gives 523 nm and compare p = 5 and 7 with 605 and 705 nm. Switch on bond alternation at about 2 eV and watch the gap stop shrinking as the chain grows.",
      target: "The bare box gives 328, 453 and 579 nm; α = 1.58 gives 523, 650 and 777 nm; the two-parameter fit gives ℓ ≈ 0.120 nm and α ≈ 2.8 with a correlation near −0.99 and predicts the 4,4′ dye 12 % too red. With alternation the wavelengths bunch towards a limit."
    }
  };

  var preset = Sim.preset(PRESETS, "box");
  Sim.label();
  Sim.presetBox(Sim.$("#preset"), preset);

  /* ---------- tridiagonal eigen-solver ---------- */
  function lowestEigen(d, e, nStates) {
    var n = d.length, e2 = new Float64Array(n), lo = Infinity, hi = -Infinity, i;
    for (i = 0; i < n - 1; i++) e2[i] = e[i] * e[i];
    for (i = 0; i < n; i++) {
      var r = (i > 0 ? Math.abs(e[i - 1]) : 0) + (i < n - 1 ? Math.abs(e[i]) : 0);
      lo = Math.min(lo, d[i] - r); hi = Math.max(hi, d[i] + r);
    }
    var scale = Math.max(Math.abs(lo), Math.abs(hi), 1e-300);
    function count(x) {
      var c = 0, q = d[0] - x;
      if (q < 0) c++;
      for (var j = 1; j < n; j++) {
        if (Math.abs(q) < 1e-300) q = 1e-300;
        q = d[j] - x - e2[j - 1] / q;
        if (q < 0) c++;
      }
      return c;
    }
    var E = [], vecs = [];
    nStates = Math.min(nStates, n);
    for (var k = 0; k < nStates; k++) {
      var a = lo, b = hi;
      for (var it = 0; it < 200; it++) {
        var mid = 0.5 * (a + b);
        if (mid === a || mid === b) break;
        if (count(mid) > k) b = mid; else a = mid;
      }
      E.push(0.5 * (a + b));
    }
    E.forEach(function (lam) { vecs.push(inverseIteration(d, e, lam, scale)); });
    return { E: E, vecs: vecs };
  }

  // solve (T - lam I) x = rhs repeatedly; LAPACK dgtsv with partial pivoting
  function inverseIteration(d, e, lam, scale) {
    var n = d.length, x = new Float64Array(n), i;
    for (i = 0; i < n; i++) x[i] = 1 + 0.37 * Math.sin(1.3 * i + 0.2);
    var tiny = 1e-15 * scale;
    for (var pass = 0; pass < 3; pass++) {
      var dl = new Float64Array(n), dd = new Float64Array(n), du = new Float64Array(n), b = x;
      for (i = 0; i < n; i++) dd[i] = d[i] - lam;
      for (i = 0; i < n - 1; i++) { dl[i] = e[i]; du[i] = e[i]; }
      var fact, temp;
      for (i = 0; i < n - 1; i++) {
        if (Math.abs(dd[i]) >= Math.abs(dl[i])) {
          if (dd[i] === 0) dd[i] = tiny;
          fact = dl[i] / dd[i];
          dd[i + 1] -= fact * du[i];
          b[i + 1] -= fact * b[i];
          dl[i] = 0;
        } else {
          fact = dd[i] / dl[i];
          dd[i] = dl[i];
          temp = dd[i + 1];
          dd[i + 1] = du[i] - fact * temp;
          if (i < n - 2) { dl[i] = du[i + 1]; du[i + 1] = -fact * dl[i]; } else dl[i] = 0;
          du[i] = temp;
          temp = b[i]; b[i] = b[i + 1]; b[i + 1] = temp - fact * b[i + 1];
        }
      }
      if (dd[n - 1] === 0) dd[n - 1] = tiny;
      b[n - 1] /= dd[n - 1];
      if (n > 1) b[n - 2] = (b[n - 2] - du[n - 2] * b[n - 1]) / dd[n - 2];
      for (i = n - 3; i >= 0; i--) b[i] = (b[i] - du[i] * b[i + 1] - dl[i] * b[i + 2]) / dd[i];
      var s = 0;
      for (i = 0; i < n; i++) s += b[i] * b[i];
      s = Math.sqrt(s);
      for (i = 0; i < n; i++) x[i] = b[i] / s;
    }
    // sign convention: first significant lobe positive
    var big = 0;
    for (i = 0; i < n; i++) big = Math.max(big, Math.abs(x[i]));
    for (i = 0; i < n; i++) if (Math.abs(x[i]) > 0.1 * big) { if (x[i] < 0) for (var j = 0; j < n; j++) x[j] = -x[j]; break; }
    return x;
  }

  // grid x[], potential V[], coefficient c (energy * length^2): returns {E, psi (normalised, sum psi^2 dx = 1)}
  function solve(x, V, c, nStates) {
    var n = x.length, dx = x[1] - x[0], t = c / (dx * dx);
    var d = new Float64Array(n), e = new Float64Array(n - 1);
    for (var i = 0; i < n; i++) d[i] = 2 * t + V[i];
    for (i = 0; i < n - 1; i++) e[i] = -t;
    var r = lowestEigen(d, e, nStates);
    var s = 1 / Math.sqrt(dx);
    return { E: r.E, psi: r.vecs.map(function (v) { var p = new Float64Array(n); for (var j = 0; j < n; j++) p[j] = v[j] * s; return p; }), dx: dx };
  }
  function nodes(psi) {
    var big = 0, i, c = 0, prev = 0;
    for (i = 0; i < psi.length; i++) big = Math.max(big, Math.abs(psi[i]));
    for (i = 0; i < psi.length; i++) {
      if (Math.abs(psi[i]) < 1e-3 * big) continue;
      var s = psi[i] > 0 ? 1 : -1;
      if (prev && s !== prev) c++;
      prev = s;
    }
    return c;
  }
  function linspace(a, b, n) { var x = new Float64Array(n); for (var i = 0; i < n; i++) x[i] = a + (b - a) * i / (n - 1); return x; }
  function tr(cells) { var row = Sim.el("tr"); cells.forEach(function (c) { row.appendChild(Sim.el("td", { html: String(c) })); }); return row; }
  function kv(el, pairs) { el.textContent = ""; pairs.forEach(function (p) { el.appendChild(Sim.el("span", { html: p[0] })); el.appendChild(Sim.el("span", { html: p[1] })); }); }
  function fmtE(x, d) { return isFinite(x) ? x.toFixed(d) : "—"; }

  // levels-and-wavefunctions series for Sim.plot: wavefunctions drawn at their energy
  function levelSeries(x, sol, n, show, ampScale, xLo, xHi, clip) {
    var ser = [], step = Math.max(1, Math.floor(x.length / 700));
    for (var k = 0; k < n; k++) {
      var E = sol.E[k], p = sol.psi[k], big = 0, i;
      var lo = xLo ? xLo(k) : x[0], hi = xHi ? xHi(k) : x[x.length - 1];
      for (i = 0; i < p.length; i++) big = Math.max(big, show === "psi2" ? p[i] * p[i] : Math.abs(p[i]));
      var data = [];
      for (i = 0; i < x.length; i += step) {
        if (clip && (x[i] < lo - clip || x[i] > hi + clip)) continue;
        var y = show === "psi2" ? p[i] * p[i] : p[i];
        data.push([x[i], E + ampScale * y / big]);
      }
      ser.push({ data: [[lo, E], [hi, E]], color: "muted", width: 1, dash: [3, 3] });
      ser.push({ data: data, color: "s" + ((k % 6) + 1), width: 1.6, label: k < 6 ? "n = " + (k + 1) : undefined });
    }
    return ser;
  }

  global.QB = { K: K, preset: preset, solve: solve, nodes: nodes, linspace: linspace, tr: tr, kv: kv, fmtE: fmtE, levelSeries: levelSeries, refresh: {} };

  /* ======================= PARTICLE IN A BOX ======================= */
  var bPlot = Sim.plot(Sim.$("#qb-plot"), { xLabel: "x / nm", yLabel: "E / eV" });
  var bCPlot = Sim.plot(Sim.$("#qb-cplot"), { xLabel: "grid points inside the box", yLabel: "relative error of E₁", logX: true, logY: true });
  var bLast = null;

  function bVals() {
    function n(id) { return parseFloat(Sim.$(id).value); }
    return { L: n("#qb-L"), m: n("#qb-mass"), fin: Sim.$("#qb-walls").value === "fin", V0: n("#qb-V0"), N: Math.round(n("#qb-N")), n: Math.round(n("#qb-n")), show: Sim.$("#qb-show").value, x1: n("#qb-x1"), x2: n("#qb-x2") };
  }
  function bGrid(v) {
    var N = Math.max(10, Math.min(1500, v.N)), dx = v.L / (N + 1), x, V, i;
    if (!v.fin) {
      x = new Float64Array(N); V = new Float64Array(N);
      for (i = 0; i < N; i++) x[i] = (i + 1) * dx;
      return { x: x, V: V };
    }
    // finite walls: the wall edges fall half-way between grid points, and the grid runs about
    // 1 nm into each wall (fewer points per wall if the total would pass 4000)
    dx = v.L / N;
    var Mw = Math.min(Math.round(1.0 / dx), Math.floor((4000 - N) / 2)), M = N + 2 * Mw;
    x = new Float64Array(M); V = new Float64Array(M);
    for (i = 0; i < M; i++) { x[i] = (i - Mw + 0.5) * dx; V[i] = (x[i] < 0 || x[i] > v.L) ? v.V0 : 0; }
    return { x: x, V: V };
  }

  function bRender() {
    var v = bVals();
    Sim.$("#qb-L-out").textContent = v.L.toFixed(2);
    Sim.$("#qb-V0-f").hidden = !v.fin;
    if (!(v.L > 0 && v.m > 0 && v.n >= 1)) return;
    var g = bGrid(v), c = K.HB2M_E / v.m, sol = solve(g.x, g.V, c, v.n), dx = g.x[1] - g.x[0];
    bLast = { v: v, g: g, sol: sol };
    var tb = Sim.$("#qb-table tbody");
    tb.textContent = "";
    var E1x = K.H2_8ME / (v.m * v.L * v.L), bound = 0, extra = [];
    sol.E.forEach(function (E, k) {
      var ex = E1x * (k + 1) * (k + 1), p = sol.psi[k], preg = 0, pin = 0;
      for (var i = 0; i < p.length; i++) {
        var w = p[i] * p[i] * dx;
        if (g.x[i] >= v.x1 * v.L && g.x[i] <= v.x2 * v.L) preg += w;
        if (g.x[i] < 0 || g.x[i] > v.L) pin += w;
      }
      var isBound = !v.fin || E < v.V0;
      if (isBound) bound++;
      tb.appendChild(tr([k + 1, E.toFixed(5) + (isBound ? "" : " (not bound)"), ex.toFixed(5), v.fin ? "—" : ((E - ex) / ex).toExponential(2), nodes(p), preg.toFixed(3), v.fin ? pin.toFixed(3) : "0"]));
    });
    extra.push(["Exact E₁ = h²/(8mL²)", E1x.toFixed(5) + " eV (" + (E1x / K.CM1_EV).toFixed(0) + " cm⁻¹)"]);
    if (sol.E.length >= 2) {
      var dE = sol.E[1] - sol.E[0];
      extra.push(["1 → 2 absorption", dE.toFixed(4) + " eV, λ = " + (K.HC_EV_NM / dE).toFixed(1) + " nm"]);
    }
    extra.push(["Classical probability for the region", Math.max(0, Math.min(1, v.x2) - Math.max(0, v.x1)).toFixed(3)]);
    if (v.fin) extra.push(["Bound states among those shown (E < V₀)", bound + (bound === sol.E.length ? " (show more states to find the last one)" : "")]);
    extra.push(["Grid spacing Δx", (dx * 1000).toFixed(3) + " pm, " + g.x.length + " points in all"]);
    kv(Sim.$("#qb-extra"), extra);
    // plot
    var Etop = v.fin ? Math.max(v.V0 * 1.15, sol.E[Math.min(sol.E.length - 1, Math.max(0, bound - 1))] * 1.2) : sol.E[sol.E.length - 1] * 1.15;
    var gap = sol.E.length > 1 ? sol.E[1] - sol.E[0] : sol.E[0];
    var amp = 0.4 * Math.min(gap, sol.E[0] * 2);
    var ser = [];
    if (v.fin) {
      var pot = [];
      for (var i = 0; i < g.x.length; i += Math.max(1, Math.floor(g.x.length / 400))) pot.push([g.x[i], g.V[i]]);
      ser.push({ type: "step", data: pot, color: "ink", width: 2, label: "V(x)" });
    } else {
      ser.push({ data: [[0, Etop * 2], [0, 0], [v.L, 0], [v.L, Etop * 2]], color: "ink", width: 2, label: "walls" });
    }
    var nShow = v.fin ? Math.min(sol.E.length, Math.max(bound, 1)) : sol.E.length;
    ser = ser.concat(levelSeries(g.x, sol, nShow, v.show, amp, function () { return v.fin ? -0.1 * v.L : 0; }, function () { return v.fin ? 1.1 * v.L : v.L; }));
    var xlo = v.fin ? -0.5 * v.L - 0.3 : -0.05 * v.L, xhi = v.fin ? 1.5 * v.L + 0.3 : 1.05 * v.L;
    bPlot.draw(ser, { xMin: xlo, xMax: xhi, yMin: v.fin ? -0.05 * Etop : -0.08 * Etop, yMax: Etop });
  }

  function bConvergence() {
    var v = bVals(), Ns = [25, 50, 100, 200, 400, 800], pts = [], c = K.HB2M_E / v.m, ex = K.H2_8ME / (v.m * v.L * v.L);
    Ns.forEach(function (N) {
      var g = bGrid({ L: v.L, N: N, fin: false }), s = solve(g.x, g.V, c, 1);
      pts.push([N, Math.abs(s.E[0] - ex) / ex]);
    });
    Sim.$("#qb-conv-panel").hidden = false;
    var f = Sim.stats.linfit(pts.map(function (p) { return Math.log10(p[0]); }), pts.map(function (p) { return Math.log10(p[1]); }));
    bCPlot.draw([{ type: "points", data: pts, color: "s2", label: "E₁ error" }, { data: pts.map(function (p) { return [p[0], Math.pow(10, f.a + f.b * Math.log10(p[0]))]; }), color: "s1", dash: [4, 3], label: "slope " + f.b.toFixed(2) }]);
    kv(Sim.$("#qb-ctext"), [["Errors", pts.map(function (p) { return p[0] + ": " + p[1].toExponential(1); }).join(", ")], ["Slope of log(error) against log(N)", f.b.toFixed(2) + " (−2 means error ∝ Δx²)"]]);
  }

  ["#qb-L", "#qb-mass", "#qb-walls", "#qb-V0", "#qb-N", "#qb-n", "#qb-show", "#qb-x1", "#qb-x2"].forEach(function (id) {
    Sim.$(id).addEventListener("input", bRender);
    Sim.$(id).addEventListener("change", bRender);
  });
  Sim.$("#qb-conv").addEventListener("click", bConvergence);
  Sim.exportCSV(Sim.$("#qb-x"), "box_energies.csv", function () {
    if (!bLast) return null;
    var v = bLast.v, ex = K.H2_8ME / (v.m * v.L * v.L);
    return { header: ["n", "E_numerical_eV", "E_exact_infinite_eV", "nodes"], rows: bLast.sol.E.map(function (E, k) { return [k + 1, +E.toFixed(7), +(ex * (k + 1) * (k + 1)).toFixed(7), nodes(bLast.sol.psi[k])]; }) };
  });
  Sim.exportCSV(Sim.$("#qb-xpsi"), "box_wavefunctions.csv", function () {
    if (!bLast) return null;
    var g = bLast.g, s = bLast.sol, rows = [], step = Math.max(1, Math.floor(g.x.length / 1000));
    for (var i = 0; i < g.x.length; i += step) rows.push([+g.x[i].toFixed(6)].concat(s.psi.map(function (p) { return +p[i].toFixed(6); })));
    return { header: ["x_nm"].concat(s.psi.map(function (p, k) { return "psi" + (k + 1) + "_per_sqrt_nm"; })), rows: rows };
  });
  QB.refresh.box = bRender;

  /* ======================= TUNNELLING ======================= */
  var tPlot = Sim.plot(Sim.$("#qt-plot"), { xLabel: "x / nm", yLabel: "|ψ|² (incident wave = 1)", logY: true });
  var tPlot2 = Sim.plot(Sim.$("#qt-plot2"), { xLabel: "barrier width d / nm", yLabel: "transmission T", logY: true });
  var tRec = [], dwStore = {};

  // complex arithmetic
  function cx(re, im) { return { re: re, im: im || 0 }; }
  function cadd(a, b) { return cx(a.re + b.re, a.im + b.im); }
  function csub(a, b) { return cx(a.re - b.re, a.im - b.im); }
  function cmul(a, b) { return cx(a.re * b.re - a.im * b.im, a.re * b.im + a.im * b.re); }
  function cdiv(a, b) { var d = b.re * b.re + b.im * b.im; return cx((a.re * b.re + a.im * b.im) / d, (a.im * b.re - a.re * b.im) / d); }
  function cexp(z) { var m = Math.exp(z.re); return cx(m * Math.cos(z.im), m * Math.sin(z.im)); }
  function cabs2(z) { return z.re * z.re + z.im * z.im; }
  function cscale(a, s) { return cx(a.re * s, a.im * s); }

  function tVals() {
    function n(id) { return parseFloat(Sim.$(id).value); }
    var mSel = Sim.$("#qt-m");
    return { mode: Sim.$("#qt-mode").value, E: n("#qt-E"), V0: n("#qt-V0"), d: n("#qt-d"), m: n("#qt-m"), mName: mSel.options[mSel.selectedIndex].text, Vb: n("#qt-Vb"), a: n("#qt-a"), mu: n("#qt-mu"), loc: Sim.$("#qt-loc").checked };
  }
  function transmission(E, V0, d, m) {
    var c = K.HB2M_E / m;
    if (Math.abs(E - V0) < 1e-12) return 1 / (1 + V0 * d * d / (4 * c));
    if (E < V0) {
      var kap = Math.sqrt((V0 - E) / c), sh = Math.sinh(kap * d);
      return 1 / (1 + V0 * V0 * sh * sh / (4 * E * (V0 - E)));
    }
    var q = Math.sqrt((E - V0) / c), sn = Math.sin(q * d);
    return 1 / (1 + V0 * V0 * sn * sn / (4 * E * (E - V0)));
  }
  // exact scattering state, incident amplitude 1 from the left
  function scatter(E, V0, d, m) {
    var c = K.HB2M_E / m, k = Math.sqrt(E / c);
    var kap = E < V0 ? cx(Math.sqrt((V0 - E) / c), 0) : cx(0, Math.sqrt(Math.max(E - V0, 1e-12) / c));
    var ik = cx(0, k);
    // region III: psi = t e^{ik(x-d)} with t = 1, then propagate back to x = 0
    var psiD = cx(1, 0), dpsiD = ik;
    var eKd = cexp(cscale(kap, d));
    var A = cdiv(cadd(psiD, cdiv(dpsiD, kap)), cscale(eKd, 2));
    var B = cscale(cmul(csub(psiD, cdiv(dpsiD, kap)), eKd), 0.5);
    var psi0 = cadd(A, B), dpsi0 = cmul(kap, csub(A, B));
    var a = cscale(cadd(psi0, cdiv(dpsi0, ik)), 0.5), b = cscale(csub(psi0, cdiv(dpsi0, ik)), 0.5);
    return function (x) {
      var z;
      if (x < 0) z = cadd(cmul(a, cexp(cx(0, k * x))), cmul(b, cexp(cx(0, -k * x))));
      else if (x <= d) z = cadd(cmul(A, cexp(cscale(kap, x))), cmul(B, cexp(cscale(kap, -x))));
      else z = cexp(cx(0, k * (x - d)));
      return cabs2(cdiv(z, a));
    };
  }

  function tRect(v) {
    var c = K.HB2M_E / v.m, out = [];
    var T = transmission(v.E, v.V0, v.d, v.m);
    if (v.E < v.V0) {
      var kap = Math.sqrt((v.V0 - v.E) / c);
      var Tap = 16 * v.E / v.V0 * (1 - v.E / v.V0) * Math.exp(-2 * kap * v.d);
      out.push(["κ = √(2m(V₀ − E))/ħ", kap.toFixed(3) + " nm⁻¹ (decay length 1/κ = " + (1000 / kap).toFixed(1) + " pm)"]);
      out.push(["κd", (kap * v.d).toFixed(3) + (kap * v.d < 1 ? " — thin barrier: use the exact formula" : "")]);
      out.push(["T exact", T.toExponential(3) + " (" + (100 * T).toPrecision(3) + " %)"]);
      out.push(["T thick-barrier 16(E/V₀)(1 − E/V₀)e<sup>−2κd</sup>", Tap.toExponential(3)]);
      out.push(["Factor per extra 0.1 nm, e<sup>−0.2κ</sup>", Math.exp(-0.2 * kap).toPrecision(3) + " (STM current falls " + (1 / Math.exp(-0.2 * kap)).toPrecision(2) + " times)"]);
    } else {
      out.push(["E ≥ V₀", "over the barrier: T = " + T.toFixed(4) + " (below 1: the wave still reflects off the steps)"]);
    }
    QB.kv(Sim.$("#qt-out"), out);
    // wavefunction plot
    var f = scatter(v.E, v.V0, v.d, v.m), pts = [], lo = -0.6, hi = v.d + 0.6;
    for (var i = 0; i <= 600; i++) { var x = lo + (hi - lo) * i / 600; pts.push([x, f(x)]); }
    var ymin = Math.max(1e-30, Math.min.apply(null, pts.map(function (p) { return p[1]; })) / 3);
    tPlot.draw([
      { type: "band", data: [[0, ymin, 10], [v.d, ymin, 10]], color: "s5", alpha: 0.15, label: "barrier" },
      { data: pts, color: "s1", label: "|ψ|²" },
      { type: "hline", y: T, color: "s2", dash: [4, 3], width: 1, label: "transmitted |ψ|² = T" }
    ], { xMin: lo, xMax: hi, yMin: ymin, yMax: 10, xLabel: "x / nm", yLabel: "|ψ|² (incident wave = 1)" });
    // transmission against width
    var tc = [], ta = [];
    for (i = 1; i <= 120; i++) {
      var d = 1.2 * i / 120;
      tc.push([d, transmission(v.E, v.V0, d, v.m)]);
      if (v.E < v.V0) { var kk = Math.sqrt((v.V0 - v.E) / c); ta.push([d, 16 * v.E / v.V0 * (1 - v.E / v.V0) * Math.exp(-2 * kk * d)]); }
    }
    var lowT = Math.max(1e-30, Math.min(tc[tc.length - 1][1], ta.length ? ta[ta.length - 1][1] : 1) / 2);
    tPlot2.draw([
      { data: tc, color: "s1", label: "exact" },
      { data: ta, color: "s2", dash: [5, 4], label: "thick-barrier formula" },
      { type: "points", data: [[v.d, T]], color: "s6", size: 5, label: "this barrier" }
    ], { xMin: 0, xMax: 1.2, yMin: lowT, yMax: 2, xLabel: "barrier width d / nm", yLabel: "transmission T", logY: true });
  }

  function tDouble(v) {
    var x = linspace(-1.5, 1.5, 3001), V = new Float64Array(x.length);
    for (var i = 0; i < x.length; i++) { var y = x[i] / v.a; V[i] = v.Vb * (y * y - 1) * (y * y - 1); }
    var c = K.HB2M_U / v.mu, s = solve(x, V, c, 4);
    var d0 = s.E[1] - s.E[0], d1 = s.E[3] - s.E[2], GHz = K.C_CM * 1e-9;
    dwStore[v.mu.toFixed(3)] = d0;
    var out = [
      ["Lowest pair E₀, E₁", s.E[0].toFixed(2) + ", " + s.E[1].toFixed(2) + " cm⁻¹"],
      ["Tunnelling splitting Δ = E₁ − E₀", d0.toPrecision(3) + " cm⁻¹ = " + (d0 * GHz).toPrecision(3) + " GHz"],
      ["Flip time h/Δ (left → right → left)", (1e12 / (d0 * K.C_CM)).toPrecision(3) + " ps"],
      ["Second pair, splitting", s.E[2].toFixed(1) + " cm⁻¹, Δ = " + d1.toPrecision(3) + " cm⁻¹ (nearer the top, tunnels faster)"],
      ["Measured (NH₃ / ND₃)", "0.79 cm⁻¹ (23.79 GHz) / 0.053 cm⁻¹ (1.59 GHz), ratio 15"]
    ];
    if (dwStore["2.487"] && dwStore["4.220"]) out.push(["Model ratio NH₃/ND₃", (dwStore["2.487"] / dwStore["4.220"]).toFixed(1)]);
    QB.kv(Sim.$("#qt-out"), out);
    var ser = [], pot = [];
    for (i = 0; i < x.length; i += 6) pot.push([x[i], V[i]]);
    ser.push({ data: pot, color: "ink", width: 2, label: "V(x)" });
    var amp = 0.18 * v.Vb, psis = [s.psi[0], s.psi[1]], labels = ["ψ₀ (symmetric)", "ψ₁ (antisymmetric)"];
    if (v.loc) {
      var L = new Float64Array(x.length), R = new Float64Array(x.length);
      for (i = 0; i < x.length; i++) { L[i] = (s.psi[0][i] + s.psi[1][i]) / Math.SQRT2; R[i] = (s.psi[0][i] - s.psi[1][i]) / Math.SQRT2; }
      psis = [L, R]; labels = ["(ψ₀ + ψ₁)/√2: in one well", "(ψ₀ − ψ₁)/√2: in the other"];
    }
    psis.forEach(function (p, k) {
      var big = 0, data = [];
      for (i = 0; i < p.length; i++) big = Math.max(big, Math.abs(p[i]));
      for (i = 0; i < p.length; i += 6) data.push([x[i], s.E[0] + (k === 1 && !v.loc ? d0 : 0) + amp * p[i] / big]);
      ser.push({ data: data, color: k ? "s2" : "s1", width: 1.6, label: labels[k] });
    });
    ser.push({ type: "hline", y: s.E[0], color: "muted", dash: [3, 3], width: 1 });
    tPlot.draw(ser, { xMin: -1.2, xMax: 1.2, yMin: 0, yMax: Math.max(1.3 * v.Vb, s.E[0] * 1.6), xLabel: "umbrella coordinate x / Å", yLabel: "E / cm⁻¹", logY: false });
    var per = 1e12 / (d0 * K.C_CM), pr = [];
    for (i = 0; i <= 300; i++) { var t = 2 * per * i / 300; pr.push([t, Math.pow(Math.sin(Math.PI * t / per), 2)]); }
    tPlot2.draw([{ data: pr, color: "s4", label: "started in the left well" }], { xMin: 0, xMax: 2 * per, yMin: 0, yMax: 1.05, xLabel: "time / ps", yLabel: "probability in the right well", logY: false });
  }

  function tRender() {
    var v = tVals(), dw = v.mode === "dw";
    Sim.$("#qt-rect").hidden = dw; Sim.$("#qt-dw").hidden = !dw; Sim.$("#qt-recpanel").hidden = dw;
    Sim.$("#qt-d-out").textContent = v.d.toFixed(2);
    Sim.$("#qt-h1").textContent = dw ? "Double well: levels and wavefunctions" : "Scattering state through the barrier (log scale)";
    if (dw) { if (v.Vb > 0 && v.a > 0 && v.mu > 0) tDouble(v); }
    else if (v.E > 0 && v.V0 >= 0 && v.d > 0) tRect(v);
  }
  function tRecRender() {
    var tb = Sim.$("#qt-table tbody");
    tb.textContent = "";
    tRec.forEach(function (r, i) { tb.appendChild(tr([i + 1].concat(r.map(function (x) { return typeof x === "number" ? (Math.abs(x) < 1e-3 && x !== 0 ? x.toExponential(3) : +x.toPrecision(4)) : x; })))); });
  }

  ["#qt-mode", "#qt-E", "#qt-V0", "#qt-d", "#qt-m", "#qt-Vb", "#qt-a", "#qt-mu", "#qt-loc"].forEach(function (id) {
    Sim.$(id).addEventListener("input", tRender);
    Sim.$(id).addEventListener("change", tRender);
  });
  Sim.$("#qt-rec").addEventListener("click", function () {
    var v = tVals(), c = K.HB2M_E / v.m, kap = v.E < v.V0 ? Math.sqrt((v.V0 - v.E) / c) : NaN;
    var T = transmission(v.E, v.V0, v.d, v.m), Tap = isFinite(kap) ? 16 * v.E / v.V0 * (1 - v.E / v.V0) * Math.exp(-2 * kap * v.d) : NaN;
    tRec.push([v.mName, v.E, v.V0, v.d, kap, T, Tap]);
    tRecRender();
  });
  Sim.$("#qt-clear").addEventListener("click", function () { tRec = []; tRecRender(); });
  Sim.exportCSV(Sim.$("#qt-x"), "tunnelling_cases.csv", function () {
    return { header: ["particle", "E_eV", "V0_eV", "d_nm", "kappa_per_nm", "T_exact", "T_thick_barrier"], rows: tRec };
  });
  QB.refresh.tunnel = tRender;
})(window);
