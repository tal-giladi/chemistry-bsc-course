/* voltammetry simulation: cyclic voltammetry of a dissolved or adsorbed redox couple (finite
 * differences with Butler–Volmer boundary kinetics, uncompensated resistance, charging current,
 * oxygen interference, fouled electrode) and steady-state Butler–Volmer polarisation curves with
 * Tafel and micro-polarisation analysis. Uses ../common/sim.js (global Sim).
 *
 * Data and sources:
 *  - F, R: CODATA 2022 (Sim.C). F/RT = 38.92 V-1 at 25 °C.
 *  - Ferricyanide (Lesson 19.5): 2.0 mM in 0.1 M KCl, D = 7.2e-6 cm2/s, E0' = 0.220 V vs Ag/AgCl,
 *    3 mm Pt disc (0.0707 cm2), Cdl 20 uF/cm2. The "reversible" preset uses k0 = 1 cm/s; the lesson's
 *    Python data use k0 = 0.02 cm/s (quasi-reversible on Pt).
 *  - Quasi-reversible couple (Lesson 25.6 data, illustrative): 1.0 mM in 0.5 M KCl, D = 7.0e-6 cm2/s,
 *    k0 = 0.004 cm/s, alpha = 0.5, E0' = 0.220 V, glassy carbon 3 mm, window 0.70 to -0.30 V.
 *  - Randles–Ševčík ip = 2.69e5 n^1.5 A D^0.5 C v^0.5 (25 °C); Lavagnini, Antiochia and Magno,
 *    Electroanalysis 16, 505 (2004): psi = (-0.6288 + 0.0021 X)/(1 - 0.017 X), X = n dEp / mV;
 *    Nicholson, Anal. Chem. 37, 1351 (1965): ipa/ipc = (ipa)0/ipc + 0.485 (isp)0/ipc + 0.086.
 *  - Dissolved O2 about 0.26 mM in air-saturated water at 25 °C, D about 2.0e-5 cm2/s; its wave is
 *    modelled as an irreversible 2-electron reduction (to H2O2) with k0 = 4e-5 cm/s at 0.0 V and
 *    alpha n = 0.5 (illustrative; puts the peak near -0.3 V at 0.1 V/s).
 *  - Adsorbed couple: Laviron surface kinetics, Gamma of the order of a monolayer (1e-10 to 1e-9 mol/cm2).
 *  - Hydrogen evolution in 0.5 M H2SO4, typical orders (Trasatti 1972; Nørskov et al., J. Electrochem.
 *    Soc. 152, J23 (2005); Lesson 32.1 and its data): Pt i0 1e-3 A/cm2, b 30 mV/dec; Ni 8e-6, 118 mV/dec;
 *    Cu 2.6e-7, 114 mV/dec; Hg 1e-12, 118 mV/dec. Ru = 2.5 ohm cm2 as in the Lesson 32.1 data.
 */
(function () {
  "use strict";
  var F = Sim.C.F, R = Sim.C.R, S = Sim.stats;

  var PRESETS = {
    reversible: {
      title: "A reversible couple: ferricyanide", tab: "cv", couple: "fecn", v: 50, series: [25, 50, 100, 200, 400],
      what: "Fe(CN)₆³⁻ + e⁻ ⇌ Fe(CN)₆⁴⁻ with fast electron transfer. The sweep starts at +0.50 V where nothing happens; near E°′ = 0.22 V the surface must follow the Nernst equation, reduction starts, the surface runs out of ferricyanide and the current passes a peak. On the way back the ferrocyanide made near the surface is oxidised again. For a reversible couple ΔE<sub>p</sub> ≈ 57/n mV at every scan rate, E<sub>1/2</sub> ≈ E°′ and i<sub>p</sub> follows Randles–Ševčík, i<sub>p</sub> ∝ C√v.",
      task: "Record a CV at 50 mV/s and read E<sub>pc</sub>, E<sub>pa</sub> and i<sub>pc</sub>. Repeat at 100, 200 and 400 mV/s (or press Scan-rate series): does ΔE<sub>p</sub> change, and does i<sub>p</sub> double when v quadruples? Then double the concentration. Finally set k⁰ = 0.02 cm/s, the value behind the Lesson 19.5 Python data, and watch ΔE<sub>p</sub> grow with v.",
      target: "ΔE<sub>p</sub> 57–60 mV at every rate; i<sub>pc</sub> ≈ 32 µA at 100 mV/s and ≈ 64 µA at 400 mV/s; i<sub>p</sub> doubles with C; E<sub>1/2</sub> = 0.220 V. With k⁰ = 0.02 cm/s ΔE<sub>p</sub> rises from about 62 mV at 25 mV/s to about 80 mV at 400 mV/s, as in the Python data."
    },
    "scan-rate": {
      title: "Scan-rate study: diffusion, adsorption, resistance", tab: "cv", couple: "quasi", v: 100, series: [20, 50, 100, 200, 500, 1000],
      what: "A scan-rate series tells you what controls the current. A dissolved species gives i<sub>p</sub> ∝ √v (log–log slope 0.5, a little less for a slow couple); a species adsorbed on the electrode gives symmetric peaks with almost no separation and i<sub>p</sub> ∝ v (slope 1). A ΔE<sub>p</sub> that grows with v is either slow electron transfer or uncompensated resistance; only the iR part depends on the concentration.",
      task: "Record CVs at 20, 50, 100, 200, 500 and 1000 mV/s (Scan-rate series) and look at i<sub>p</sub> against √v and the log–log slope. Switch to the adsorbed species and repeat. Then set the species back to dissolved, enter R<sub>u</sub> = 300 Ω and run the series at 1.0 mM and at 0.5 mM; compare ΔE<sub>p</sub> at 1 V/s with the R<sub>u</sub> = 0 run.",
      target: "Dissolved: log–log slope about 0.47 and ΔE<sub>p</sub> growing from about 84 to 190 mV; adsorbed: slope 1.00 and ΔE<sub>p</sub> near 0; with 300 Ω the extra ΔE<sub>p</sub> at 1 V/s is about 2i<sub>p</sub>R<sub>u</sub> ≈ 25 mV at 1.0 mM and about half of that at 0.5 mM."
    },
    quasi: {
      title: "Quasi-reversible kinetics and Nicholson's ψ", tab: "cv", couple: "quasi", v: 100, series: [20, 50, 100, 200, 500, 1000],
      what: "If electron transfer is slow compared with the scan, the surface cannot stay at Nernstian equilibrium and the peaks move apart. Nicholson showed that ΔE<sub>p</sub> depends only on ψ = k⁰/√(πDnFv/RT): large ψ gives the reversible 57–60 mV, ψ = 1 about 84 mV, ψ = 0.25 about 141 mV. Lavagnini's equation turns a measured ΔE<sub>p</sub> back into ψ and so into k⁰, valid for about 63–150 mV.",
      task: "At 0.1 V/s, set k⁰ to 1, 0.01 and 0.001 cm/s and record each. Read ΔE<sub>p</sub>, compare with ψ, and see whether the k⁰ the table recovers from ΔE<sub>p</sub> matches the one you set. Then reset k⁰ = 0.004 cm/s and run the scan-rate series: which scans are inside the range of the method?",
      target: "ΔE<sub>p</sub> about 59 mV at k⁰ = 1 (ψ ≈ 108), about 80 mV at 0.01 (ψ ≈ 1.1; the table recovers about 0.012) and about 200 mV at 0.001 (ψ ≈ 0.11, outside the range of the method); at k⁰ = 0.004 the four scans from 20 to 200 mV/s (ΔE<sub>p</sub> 83–132 mV) give k⁰ = 0.0037–0.0047, mean about 0.0042 cm/s."
    },
    "butler-volmer": {
      title: "Butler–Volmer kinetics and the Tafel plot", tab: "bv", mat: "custom", i0: 1e-5, alpha: 0.5,
      what: "Push an electrode away from equilibrium by an overpotential η and a net current flows: i = i₀[e<sup>α<sub>a</sub>fη</sup> − e<sup>−α<sub>c</sub>fη</sup>]. Near η = 0 the electrode behaves as a resistor R<sub>ct</sub> = RT/(Fi₀); beyond about 100 mV one exponential wins and log|i| falls on a straight Tafel line of slope 2.303RT/(αF) that extrapolates to log i₀ at η = 0. Solution resistance and the mass-transport limit bend that line.",
      task: "With i₀ = 10⁻⁵ A/cm², α = 0.5, R<sub>u</sub> = 0 and no limit, sweep from +0.2 to −0.4 V and read both slopes. Change α to 0.3 and 0.7. Switch on R<sub>u</sub> = 5 Ω cm² and find where the line starts to bend; correct for iR. Switch on a limiting current of 20 mA/cm² and fit through the plateau.",
      target: "Both slopes 118 mV/dec meeting at log i₀ = −5 at η = 0; α = 0.3 gives a cathodic slope of 197 and an anodic slope of 84 mV/dec; with 5 Ω cm² the bend shows above about 2 mA/cm² (10 mV of iR); a fit into the limiting-current region gives a falsely large slope."
    }
  };

  var COUPLES = {
    fecn: { conc: 2.0, D: 7.2, k0: 1.0, alpha: 0.5, n: 1, E0: 0.220, Es: 0.50, Ew: -0.10, diam: 3.0, mat: "Pt" },
    quasi: { conc: 1.0, D: 7.0, k0: 0.004, alpha: 0.5, n: 1, E0: 0.220, Es: 0.70, Ew: -0.30, diam: 3.0, mat: "glassy carbon" }
  };

  var preset = Sim.preset(PRESETS, "reversible");
  var seed = Sim.seedFromQuery(25);
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
  function fOf(Tc) { return F / (R * (Tc + 273.15)); }

  /* ======================= CV: the finite-difference engine ======================= */
  // p: {C (mol/cm3), D (cm2/s), A (cm2), E0, k0, alpha, n, Es, Ew, v (V/s), Ru (ohm), Cdl (F/cm2),
  //     ads, Gamma (mol/cm2), ks (1/s), o2 (bool), offset (V), noise (A), rng}
  function cvSim(p) {
    var f = fOf(25), dE = 0.0005;
    var down = p.Ew < p.Es, nHalf = Math.max(2, Math.round(Math.abs(p.Ew - p.Es) / dE));
    var nTot = 2 * nHalf, dt = dE / p.v, tTot = dt * nTot;
    var Es = [], cur = new Float64Array(nTot);
    for (var j = 0; j < nTot; j++) {
      var s = j < nHalf ? j : nTot - 1 - j;
      Es.push(p.Es + (down ? -1 : 1) * s * dE);
    }
    var dx = Math.sqrt(p.D * dt / 0.45), nx = Math.floor(6 * Math.sqrt(p.D * tTot) / dx) + 3;
    var lam = p.D * dt / (dx * dx), g = p.D / dx;
    var O = new Float64Array(nx), Rr = new Float64Array(nx), tmpO = new Float64Array(nx), tmpR = new Float64Array(nx);
    // the solution holds only the form that reacts first: O if the sweep goes negative, R if positive
    for (var a = 0; a < nx; a++) { O[a] = down ? p.C : 0; Rr[a] = down ? 0 : p.C; }
    // oxygen (irreversible 2e- reduction), its own grid because D differs
    var Do2 = 2.0e-5, Co2 = p.o2 ? 0.26e-6 : 0, dx2 = Math.sqrt(Do2 * dt / 0.45), nx2 = Math.floor(6 * Math.sqrt(Do2 * tTot) / dx2) + 3;
    var lam2 = Do2 * dt / (dx2 * dx2), g2 = Do2 / dx2, X = new Float64Array(p.o2 ? nx2 : 1), tmpX = new Float64Array(p.o2 ? nx2 : 1);
    if (p.o2) for (var b = 0; b < nx2; b++) X[b] = Co2;
    var GO = down ? p.Gamma : 0, Gt = p.Gamma;
    var iPrev = 0, best = 0, profPeak = null, profSw = null;
    var nf = p.n * f;

    function faradaic(E) {           // returns {i, O0, R0, X0, GOn} for the true electrode potential E
      var out = { i: 0 };
      var eta = E - p.E0;
      if (p.ads) {
        var kfs = p.ks * Math.exp(-p.alpha * nf * eta), kbs = p.ks * Math.exp((1 - p.alpha) * nf * eta);
        var GOn = (GO + dt * kbs * Gt) / (1 + dt * (kfs + kbs));
        out.GOn = GOn;
        out.i += -p.n * F * p.A * (GO - GOn) / dt;
      } else if (p.C > 0) {
        var ex = Math.max(-200, Math.min(200, -p.alpha * nf * eta));
        var kf = p.k0 * Math.exp(ex), kb = p.k0 * Math.exp(ex + nf * eta);
        var S0 = (4 * (O[1] + Rr[1]) - (O[2] + Rr[2])) / 3;
        var O0 = (g / 2 * (4 * O[1] - O[2]) + kb * S0) / (1.5 * g + kf + kb);
        if (!isFinite(O0)) O0 = kf > kb ? 0 : S0;
        out.O0 = O0; out.R0 = S0 - O0;
        var J = g / 2 * (4 * O[1] - O[2] - 3 * O0);      // reduction flux, mol cm-2 s-1
        out.i += -p.n * F * p.A * J;
      }
      if (p.o2) {
        var kf2 = 4e-5 * Math.exp(Math.max(-200, Math.min(200, -0.5 * f * E)));
        var X0 = (g2 / 2 * (4 * X[1] - X[2])) / (1.5 * g2 + kf2);
        out.X0 = X0;
        out.i += -2 * F * p.A * kf2 * X0;
      }
      return out;
    }

    for (var k = 0; k < nTot; k++) {
      var sign = (k < nHalf) === down ? -1 : 1;           // charging current follows dE/dt
      var ic = sign * p.Cdl * p.A * p.v;
      var Eapp = Es[k] - p.offset, res, iF = iPrev;
      if (p.Ru > 0) {
        for (var it = 0; it < 12; it++) {
          res = faradaic(Eapp - (iF + ic) * p.Ru);
          var nxt = 0.5 * iF + 0.5 * res.i;
          if (Math.abs(nxt - iF) < 1e-12) { iF = nxt; break; }
          iF = nxt;
        }
        res = faradaic(Eapp - (iF + ic) * p.Ru);
      } else res = faradaic(Eapp);
      iF = res.i; iPrev = iF;
      if (p.ads) GO = res.GOn;
      else if (p.C > 0) {
        O[0] = res.O0; Rr[0] = res.R0;
        for (var q = 1; q < nx - 1; q++) { tmpO[q] = O[q] + lam * (O[q + 1] - 2 * O[q] + O[q - 1]); tmpR[q] = Rr[q] + lam * (Rr[q + 1] - 2 * Rr[q] + Rr[q - 1]); }
        for (q = 1; q < nx - 1; q++) { O[q] = tmpO[q]; Rr[q] = tmpR[q]; }
      }
      if (p.o2) {
        X[0] = res.X0;
        for (var r2 = 1; r2 < nx2 - 1; r2++) tmpX[r2] = X[r2] + lam2 * (X[r2 + 1] - 2 * X[r2] + X[r2 - 1]);
        for (r2 = 1; r2 < nx2 - 1; r2++) X[r2] = tmpX[r2];
      }
      cur[k] = iF + ic + (p.noise ? p.rng.normal(0, p.noise) : 0);
      // concentration snapshots: at the largest forward current, and at the switching potential
      if (!p.ads && p.C > 0) {
        if (k < nHalf && Math.abs(iF) > best) { best = Math.abs(iF); profPeak = { O: Array.prototype.slice.call(O), R: Array.prototype.slice.call(Rr), E: Es[k] }; }
        if (k === nHalf - 1) profSw = { O: Array.prototype.slice.call(O), R: Array.prototype.slice.call(Rr), E: Es[k] };
      }
    }
    return { E: Es, i: cur, nHalf: nHalf, down: down, dx: dx, profPeak: profPeak, profSw: profSw, ic: p.Cdl * p.A * p.v };
  }

  // peak analysis of one run; currents in A; charging baseline (known Cdl, as from a blank) removed
  function peaks(run, n, D, v) {
    var E = run.E, i = run.i, m = run.nHalf, sgn = run.down ? -1 : 1, ic = run.ic;
    var fwd = -1, fi = 0, rev = -1, ri = 0;
    for (var k = 2; k < m; k++) { var y = sgn * (i[k] - sgn * ic); if (y > fi) { fi = y; fwd = k; } }
    for (k = m + 2; k < 2 * m; k++) { var z = -sgn * (i[k] + sgn * ic); if (z > ri) { ri = z; rev = k; } }
    var out = { v: v, ok: fwd > 2 && fwd < m - 3 };
    if (!out.ok) return out;
    out.Ef = E[fwd]; out.ipf = fi;
    var isp = sgn * (i[m - 1] - sgn * ic);
    if (rev > m + 2 && rev < 2 * m - 3 && ri > 0) {
      out.Er = E[rev]; out.ipr0 = ri;
      out.ratio = ri / fi + 0.485 * isp / fi + 0.086;
      var Epc = run.down ? out.Ef : out.Er, Epa = run.down ? out.Er : out.Ef;
      out.Epc = Epc; out.Epa = Epa; out.dEp = (Epa - Epc) * 1000; out.E12 = (Epa + Epc) / 2;
      var X = n * out.dEp;
      out.psi = (-0.6288 + 0.0021 * X) / (1 - 0.017 * X);
      out.psiOk = X >= 63 && X <= 150;
      out.k0 = out.psi * Math.sqrt(Math.PI * D * n * fOf(25) * v);
    }
    out.ipc = run.down ? out.ipf : out.ipr0;
    return out;
  }

  /* ======================= CV: controls, runs and plots ======================= */
  var cPlot = Sim.plot($id("c-plot"), { xLabel: "E / V vs Ag/AgCl", yLabel: "i / µA" });
  var cIp = Sim.plot($id("c-ipplot"), { xLabel: "√v / (V/s)^½", yLabel: "i_p / µA" });
  var cProf = Sim.plot($id("c-prof"), { xLabel: "distance from the electrode / µm", yLabel: "c / mM" });
  var runs = [], runCount = 0, blank = null;
  var COLORS = ["s1", "s2", "s3", "s4", "s5", "s6"];

  function setCouple(key) {
    var c = COUPLES[key];
    if (!c) return;
    $id("c-conc").value = c.conc.toFixed(2);
    $id("c-D").value = c.D.toFixed(1);
    $id("c-k0").value = String(Math.log10(c.k0));
    $id("c-alpha").value = String(c.alpha);
    $id("c-n").value = String(c.n);
    $id("c-E0").value = c.E0.toFixed(3);
    $id("c-Es").value = c.Es.toFixed(2);
    $id("c-Ew").value = c.Ew.toFixed(2);
    $id("c-diam").value = c.diam.toFixed(1);
  }
  function cvParams() {
    var ads = $id("c-species").value === "ads";
    var diam = Math.max(0.01, num("c-diam")) / 10, A = Math.PI * diam * diam / 4;
    var Ru = Math.max(0, num("c-Ru") || 0), offset = 0, notes = [];
    var k0 = Math.pow(10, num("c-k0")), ks = Math.max(1e-3, num("c-ks") || 1000);
    if (!chk("c-polish")) { k0 *= 0.02; ks *= 0.02; notes.push("electrode not polished: electron transfer 50 times slower"); }
    if (!chk("c-ref")) { Ru += 1500; offset = 0.010 + 0.004 * runCount; notes.push("blocked reference frit: +1.5 kΩ and a drifting reference potential"); }
    if (!chk("c-elec")) { Ru += 4000; notes.push("no supporting electrolyte: Ru about 4 kΩ more (and in reality migration too)"); }
    if (!chk("c-purge")) notes.push("not purged: dissolved O₂ is reduced at negative potentials");
    return {
      C: Math.max(0, num("c-conc")) * 1e-6, D: Math.max(1e-8, num("c-D")) * 1e-6, A: A, E0: num("c-E0"), k0: k0,
      alpha: num("c-alpha"), n: parseInt($id("c-n").value, 10), Es: num("c-Es"), Ew: num("c-Ew"),
      v: Math.max(0.001, num("c-v") / 1000), Ru: Ru, Cdl: Math.max(0, num("c-Cdl")) * 1e-6, ads: ads,
      Gamma: Math.max(0, num("c-gamma")) * 1e-10, ks: ks, o2: !chk("c-purge"), offset: offset, noise: 20e-9, notes: notes
    };
  }
  function cvLabels() {
    var ads = $id("c-species").value === "ads";
    $id("c-gamma-row").hidden = !ads;
    $id("c-ks-row").hidden = !ads;
    $id("c-k0").disabled = ads;
    $id("c-conc").disabled = ads;
    $id("c-k0-out").textContent = Sim.sig(Math.pow(10, num("c-k0")), 2);
    $id("c-alpha-out").textContent = num("c-alpha").toFixed(2);
  }

  // adsorbed: same peak reading, no psi, plus the reversible theory value
  function adsPeaks(run, p) {
    var o = peaks(run, p.n, p.D, p.v);
    o.psi = NaN; o.k0 = NaN; o.psiOk = false;
    if (isFinite(o.ipr0)) o.ratio = o.ipr0 / o.ipf;   // no diffusion tail: read both peaks from the baseline
    if (o.ok) o.theory = p.n * p.n * F * F * p.v * p.A * p.Gamma / (4 * R * 298.15);
    return o;
  }

  function record(vmV) {
    var p = cvParams();
    if (vmV) p.v = vmV / 1000;
    if (Math.abs(p.Ew - p.Es) < 0.05) { Sim.log($id("c-log"), "The window is too narrow: start and switch must be at least 50 mV apart."); return null; }
    runCount++;
    p.rng = Sim.rng(seed + 101 * runCount);
    var run = cvSim(p);
    run.p = p; run.id = runCount;
    run.pk = p.ads ? adsPeaks(run, p) : peaks(run, p.n, p.D, p.v);
    run.pk.n = p.n;
    runs.push(run);
    if (runs.length > 12) runs.shift();
    Sim.log($id("c-log"), "Run " + run.id + ": " + (p.ads ? "adsorbed, Γ = " + Sim.sig(p.Gamma, 2) + " mol/cm²" : Sim.sig(p.C * 1e6, 3) + " mM") + ", " + Sim.sig(p.v * 1000, 3) + " mV/s, Ru = " + Math.round(p.Ru) + " Ω");
    p.notes.forEach(function (t) { Sim.log($id("c-log"), "  note: " + t); });
    if (!run.pk.ok) Sim.log($id("c-log"), "  no forward peak inside the window: switch further past E°′.");
    return run;
  }

  function lineOf(r, step) { var d = []; for (var j = 0; j < r.E.length; j += step) d.push([r.E[j], r.i[j] * 1e6]); return d; }

  function cvDraw() {
    cvLabels();
    var series = [], last = runs.length ? runs[runs.length - 1] : null;
    runs.slice(-6).forEach(function (r, k) {
      series.push({ type: "line", color: COLORS[k % 6], label: Sim.sig(r.p.v * 1000, 3) + " mV/s" + (r.p.ads ? " ads" : "") + (r.p.Ru ? ", " + Math.round(r.p.Ru) + " Ω" : ""), data: lineOf(r, 2) });
    });
    if (blank) series.push({ type: "line", color: "muted", dash: [4, 4], label: "blank", data: lineOf(blank, 2) });
    if (last && last.pk.ok && isFinite(last.pk.Epc)) {
      series.push({ type: "vline", x: last.pk.Epc, color: "muted", dash: [2, 4] });
      series.push({ type: "vline", x: last.pk.Epa, color: "muted", dash: [2, 4] });
    }
    if (!series.length) series.push({ type: "hline", y: 0, color: "muted" });
    cPlot.draw(series, {});

    var tb = Sim.$("#c-table tbody");
    tb.textContent = "";
    runs.forEach(function (r) {
      var k = r.pk, f = function (x, d) { return isFinite(x) ? x.toFixed(d) : "—"; };
      var psiTxt = "—";
      if (isFinite(k.psi) && k.dEp > 0) psiTxt = k.psiOk ? Sim.sig(k.psi, 3) : (k.n * k.dEp < 63 ? "rev." : "(" + Sim.sig(k.psi, 2) + ")");
      tb.appendChild(Sim.el("tr", {},
        Sim.el("td", { text: Sim.sig(r.p.v * 1000, 3) + (r.p.ads ? " (ads)" : "") }),
        Sim.el("td", { text: f(k.Epc, 3) }), Sim.el("td", { text: f(k.Epa, 3) }),
        Sim.el("td", { text: f(k.dEp, 1) }), Sim.el("td", { text: f(k.E12, 3) }),
        Sim.el("td", { text: isFinite(k.ipc) ? (k.ipc * 1e6).toFixed(2) : "—" }),
        Sim.el("td", { text: f(k.ratio, 2) }),
        Sim.el("td", { text: psiTxt }),
        Sim.el("td", { text: isFinite(k.k0) && k.psiOk ? Sim.sig(k.k0, 2) : "—" })));
    });

    var info = [];
    if (last) {
      var p = last.p, rs = 2.69e5 * Math.pow(p.n, 1.5) * p.A * Math.sqrt(p.D) * p.C * Math.sqrt(p.v);
      var psiTrue = p.k0 / Math.sqrt(Math.PI * p.D * p.n * fOf(25) * p.v);
      info.push(["electrode area", Sim.sig(p.A, 3) + " cm²"]);
      if (!p.ads) {
        info.push(["Randles–Ševčík i<sub>p</sub> (reversible)", Sim.sig(rs * 1e6, 3) + " µA"]);
        info.push(["true ψ = k⁰/√(πDnFv/RT)", Sim.sig(psiTrue, 3) + " (k⁰ used " + Sim.sig(p.k0, 2) + " cm/s)"]);
      } else if (last.pk.theory) info.push(["n²F²vAΓ/(4RT), reversible adsorbed peak", Sim.sig(last.pk.theory * 1e6, 3) + " µA; width at half height 90.6/n mV"]);
      info.push(["charging current C<sub>dl</sub>Av", Sim.sig(last.ic * 1e6, 2) + " µA"]);
      if (p.Ru > 0 && last.pk.ok) info.push(["i<sub>p</sub>R<sub>u</sub> shift of each peak", Sim.sig(last.pk.ipf * p.Ru * 1000, 3) + " mV"]);
    }
    kvFill($id("c-info"), info.length ? info : [["status", "Prepare the cell, then record a CV."]]);

    // peak current against scan rate: runs of the same kind, concentration and Ru as the last one
    var mode = $id("c-xaxis").value, pts = [];
    if (last) runs.forEach(function (r) {
      if (r.pk.ok && isFinite(r.pk.ipc) && r.pk.ipc > 0 && r.p.ads === last.p.ads && Math.abs(r.p.C - last.p.C) < 1e-12 && Math.abs(r.p.Ru - last.p.Ru) < 1e-9 && r.p.k0 === last.p.k0 && r.p.ks === last.p.ks && r.p.alpha === last.p.alpha && r.p.Gamma === last.p.Gamma) pts.push([r.p.v, r.pk.ipc * 1e6]);
    });
    var xs = pts.map(function (q) { return mode === "sqrt" ? Math.sqrt(q[0]) : mode === "v" ? q[0] : Math.log10(q[0]); });
    var ys = pts.map(function (q) { return mode === "log" ? Math.log10(q[1]) : q[1]; });
    var ser = [{ type: "points", color: "s2", label: "runs", data: xs.map(function (x, k) { return [x, ys[k]]; }) }];
    var fitRows = [];
    if (pts.length >= 2) {
      var lf = S.linfit(xs, ys);
      var x0 = mode === "log" ? Math.min.apply(null, xs) : 0, x1 = Math.max.apply(null, xs);
      ser.push({ type: "line", color: "s1", label: "straight line", data: [[x0, lf.a + lf.b * x0], [x1, lf.a + lf.b * x1]] });
      if (mode === "log") fitRows.push(["slope of log i<sub>p</sub> against log v", (pts.length > 2 ? Sim.fmtU(lf.b, lf.ub) : lf.b.toFixed(3)) + " (0.50 diffusion, 1.0 adsorbed)"]);
      else {
        fitRows.push(["slope", Sim.sig(lf.b, 4) + (mode === "sqrt" ? " µA (V/s)^−½" : " µA per V/s")]);
        fitRows.push(["intercept", pts.length > 2 ? Sim.fmtU(lf.a, lf.ua, "µA") : Sim.sig(lf.a, 3) + " µA"]);
        fitRows.push(["R²", lf.r2.toFixed(4)]);
        if (mode === "sqrt" && !last.p.ads && last.p.C > 0) {
          var rsK = 2.69e5 * Math.pow(last.p.n, 1.5) * last.p.A * last.p.C;
          var t0 = S.linfitThrough0(xs, ys);
          var slow = pts.slice().sort(function (a, b) { return a[0] - b[0]; })[0];
          fitRows.push(["D from the line through 0", Sim.sig(Math.pow(t0.b * 1e-6 / rsK, 2), 3) + " cm²/s"]);
          fitRows.push(["D from the slowest scan", Sim.sig(Math.pow(slow[1] * 1e-6 / Math.sqrt(slow[0]) / rsK, 2), 3) + " cm²/s (true " + Sim.sig(last.p.D, 3) + ")"]);
        }
      }
    }
    cIp.draw(ser, mode === "log" ? {} : { xMin: 0, yMin: 0 });
    kvFill($id("c-fit"), fitRows.length ? fitRows : [["status", "Record two or more scan rates of the same solution."]]);

    var pr = [];
    if (last && last.profPeak) {
      var toSer = function (arr, col, lab, dash) {
        var d = [], lim = Math.min(arr.length, 400);
        for (var k2 = 0; k2 < lim; k2++) d.push([k2 * last.dx * 1e4, arr[k2] * 1e6]);
        return { type: "line", color: col, label: lab, data: d, dash: dash };
      };
      pr.push(toSer(last.profPeak.O, "s1", "O at the forward peak (" + last.profPeak.E.toFixed(3) + " V)"));
      pr.push(toSer(last.profPeak.R, "s2", "R at the forward peak"));
      if (last.profSw) { pr.push(toSer(last.profSw.O, "s1", "O at the switch", [5, 4])); pr.push(toSer(last.profSw.R, "s2", "R at the switch", [5, 4])); }
    } else pr.push({ type: "hline", y: 0, color: "muted" });
    cProf.draw(pr, { yMin: 0 });

    csvFns.cv = function () {
      if (!runs.length) return null;
      var rows = [];
      runs.forEach(function (r) {
        for (var k3 = 0; k3 < r.E.length; k3 += 4) rows.push([r.id, +r.p.v.toPrecision(4), +(r.p.C * 1e6).toPrecision(4), Math.round(r.p.Ru), r.p.ads ? "adsorbed" : "dissolved", +r.E[k3].toFixed(4), +(r.i[k3] * 1e6).toFixed(4)]);
      });
      return { header: ["run", "scan_rate_V_per_s", "C_mM", "Ru_ohm", "species", "E_V", "i_uA"], rows: rows, filename: "cv_runs.csv" };
    };
  }

  $id("c-xaxis").addEventListener("change", function () {
    var m = $id("c-xaxis").value;
    cIp = Sim.plot($id("c-ipplot"), { xLabel: m === "sqrt" ? "√v / (V/s)^½" : m === "v" ? "v / V s⁻¹" : "log₁₀(v / V s⁻¹)", yLabel: m === "log" ? "log₁₀(i_p / µA)" : "i_p / µA" });
    cvDraw();
  });
  setCouple(preset.couple || "fecn");
  $id("c-couple").value = preset.couple || "fecn";
  $id("c-v").value = String(preset.v || 100);
  $id("c-couple").addEventListener("change", function () { setCouple($id("c-couple").value); cvLabels(); });
  ["c-k0", "c-alpha"].forEach(function (id) { $id(id).addEventListener("input", cvLabels); });
  ["c-conc", "c-D", "c-E0", "c-diam", "c-Es", "c-Ew", "c-n", "c-k0"].forEach(function (id) { $id(id).addEventListener("change", function () { $id("c-couple").value = "custom"; }); });
  $id("c-species").addEventListener("change", cvLabels);
  $id("c-run").addEventListener("click", function () { record(); cvDraw(); });
  $id("c-series").addEventListener("click", function () {
    (preset.series || [20, 50, 100, 200, 500, 1000]).forEach(function (v) { record(v); });
    cvDraw();
  });
  $id("c-clear").addEventListener("click", function () { runs = []; blank = null; $id("c-log").textContent = ""; cvDraw(); });
  $id("c-blank").addEventListener("click", function () {
    var p = cvParams();
    p.C = 0; p.ads = false; p.Gamma = 0; p.rng = Sim.rng(seed + 7);
    blank = cvSim(p);
    Sim.log($id("c-log"), "Blank (electrolyte only), " + Sim.sig(p.v * 1000, 3) + " mV/s" + (p.o2 ? ": an O₂ wave at negative potentials. Purge first." : ": only the charging current, flat across the window."));
    cvDraw();
  });
  $id("c-rerun").addEventListener("click", function () { seed = Sim.newSeed(seed); showSeed(); runs = []; blank = null; $id("c-log").textContent = ""; record(); cvDraw(); });

  /* ======================= BUTLER–VOLMER and TAFEL ======================= */
  var MATS = {
    custom: null,
    pt: { i0: 1e-3, aa: 0.5, ac: 2.303 * R * 298.15 / (F * 0.030), Ru: 2.5, multi: true },
    ni: { i0: 8e-6, aa: 0.5, ac: 0.5, Ru: 2.5, multi: false },
    cu: { i0: 2.6e-7, aa: 0.48, ac: 2.303 * R * 298.15 / (F * 0.114), Ru: 2.5, multi: true },
    hg: { i0: 1e-12, aa: 0.5, ac: 0.5, Ru: 2.5, multi: false }
  };
  var bLog = Sim.plot($id("b-log"), { xLabel: "E − E_eq / V", yLabel: "log₁₀(|i| / A cm⁻²)" });
  var bLin = Sim.plot($id("b-lin"), { xLabel: "E − E_eq / V", yLabel: "i / mA cm⁻²" });
  var bData = null, bCount = 0;

  function bvPar() {
    var multi = chk("b-multi"), a = num("b-alpha");
    var ilim = chk("b-lim") ? Math.max(1e-6, num("b-ilim") / 1000) : Infinity;
    return {
      i0: Math.pow(10, num("b-i0")), aa: multi ? Math.max(0.01, num("b-aa")) : 1 - a, ac: multi ? Math.max(0.01, num("b-ac")) : a,
      f: fOf(num("b-T")), Ru: Math.max(0, num("b-Ru") || 0), ilim: ilim, T: num("b-T")
    };
  }
  // current density for true overpotential eta, with a symmetric mass-transport limit
  function iOfEta(eta, p) {
    var ea = Math.exp(Math.min(300, p.aa * p.f * eta)), ec = Math.exp(Math.min(300, -p.ac * p.f * eta));
    if (!isFinite(p.ilim)) return p.i0 * (ea - ec);
    return (ea - ec) / (1 / p.i0 + ea / p.ilim + ec / p.ilim);
  }
  // solve E = eta + i(eta) Ru for eta by bisection (h is increasing in eta)
  function iOfE(E, p) {
    if (p.Ru <= 0) return iOfEta(E, p);
    var lo = -Math.abs(E) - 0.01, hi = Math.abs(E) + 0.01;
    for (var k = 0; k < 80; k++) {
      var mid = (lo + hi) / 2, h = mid + iOfEta(mid, p) * p.Ru - E;
      if (h > 0) hi = mid; else lo = mid;
    }
    return iOfEta((lo + hi) / 2, p);
  }
  function bvRecord() {
    bCount++;
    var p = bvPar(), r = Sim.rng(seed + 211 * bCount), E1 = num("b-E1"), E2 = num("b-E2");
    var n = Math.max(2, Math.round(Math.abs(E2 - E1) / 0.005)), pts = [];
    for (var k = 0; k <= n; k++) {
      var E = E1 + (E2 - E1) * k / n, i = iOfE(E, p);
      pts.push([E, i * (1 + r.normal(0, 0.01)) + r.normal(0, 0.2e-6)]);
    }
    bData = { p: p, pts: pts };
    bvDraw();
  }
  function bvDraw() {
    $id("b-i0-out").textContent = Sim.sig(Math.pow(10, num("b-i0")), 2) + " A/cm²";
    $id("b-alpha-out").textContent = num("b-alpha").toFixed(2);
    $id("b-multi-row").hidden = !chk("b-multi");
    $id("b-alpha").disabled = chk("b-multi");
    var p = bvPar(), info = [], micro = [];
    var bc = 2.303 / (p.ac * p.f) * 1000, ba = 2.303 / (p.aa * p.f) * 1000;
    info.push(["true values", "i₀ = " + Sim.sig(p.i0, 3) + " A/cm², b<sub>c</sub> = " + bc.toFixed(1) + ", b<sub>a</sub> = " + ba.toFixed(1) + " mV/dec, R<sub>ct</sub> = " + Sim.sig(1 / (p.f * p.i0), 3) + " Ω cm²"]);
    var lser = [], logser = [];
    // the true curve, dense, without noise
    var E1 = num("b-E1"), E2 = num("b-E2"), curve = [], lcurve = [];
    for (var k = 0; k <= 300; k++) {
      var E = E1 + (E2 - E1) * k / 300, i = iOfE(E, p);
      curve.push([E, i * 1000]);
      if (Math.abs(i) > 0) lcurve.push([E, Math.log10(Math.abs(i))]);
    }
    lser.push({ type: "line", color: "muted", label: "model", data: curve });
    logser.push({ type: "line", color: "muted", label: "model", data: lcurve });
    var corr = chk("b-ircorr");
    if (bData) {
      var Ru = bData.p.Ru;
      var pts = bData.pts.map(function (q) { return [corr ? q[0] - q[1] * Ru : q[0], q[1]]; });
      lser.push({ type: "points", color: "s2", label: corr ? "data, iR-corrected" : "data", data: pts.map(function (q) { return [q[0], q[1] * 1000]; }) });
      logser.push({ type: "points", color: "s1", label: "cathodic", data: pts.filter(function (q) { return q[1] < 0; }).map(function (q) { return [q[0], Math.log10(-q[1])]; }) });
      logser.push({ type: "points", color: "s2", label: "anodic", data: pts.filter(function (q) { return q[1] > 0; }).map(function (q) { return [q[0], Math.log10(q[1])]; }) });
      function tafel(lo, hi, cath) {
        var a = Math.min(lo, hi), b = Math.max(lo, hi), xs = [], ys = [];
        pts.forEach(function (q) { if (q[0] >= a && q[0] <= b && (cath ? q[1] < 0 : q[1] > 0)) { xs.push(q[0]); ys.push(Math.log10(Math.abs(q[1]))); } });
        if (xs.length < 3) return null;
        var lf = S.linfit(xs, ys);
        return { lf: lf, a: a, b: b, n: xs.length };
      }
      var tc = tafel(num("b-t1"), num("b-t2"), true), ta = tafel(num("b-a1"), num("b-a2"), false);
      if (tc && tc.lf.b < 0) {
        var bfit = -1000 / tc.lf.b, ub = 1000 * tc.lf.ub / (tc.lf.b * tc.lf.b);
        info.push(["cathodic Tafel fit (" + tc.n + " points)", "b<sub>c</sub> = " + Sim.fmtU(bfit, ub, "mV/dec") + ", α<sub>c</sub> = " + Sim.sig(2.303 / (p.f * bfit / 1000), 3) + ", log i₀ = " + Sim.fmtU(tc.lf.a, tc.lf.ua)]);
        logser.push({ type: "line", color: "s1", dash: [6, 4], label: "cathodic Tafel line", data: [[0, tc.lf.a], [tc.b < 0 ? tc.a : tc.b, tc.lf.a + tc.lf.b * (tc.b < 0 ? tc.a : tc.b)]] });
        var target = Math.max(1e-9, num("b-target") / 1000);
        var etaFit = bfit / 1000 * (Math.log10(target) - tc.lf.a);
        // the true overpotential for that current (no iR, the electrode alone)
        var lo = -3, hi = 0;
        for (var j = 0; j < 80; j++) { var mid = (lo + hi) / 2; if (-iOfEta(mid, p) > target) lo = mid; else hi = mid; }
        var reach = isFinite(p.ilim) && target >= p.ilim;
        info.push(["|η| for " + Sim.sig(target * 1000, 3) + " mA/cm²", "from the fit " + (etaFit * 1000).toFixed(0) + " mV; true " + (reach ? "unreachable (above i<sub>lim</sub>)" : ((-(lo + hi) / 2) * 1000).toFixed(0) + " mV") + "; iR at that current " + (target * p.Ru * 1000).toFixed(0) + " mV"]);
      } else info.push(["cathodic Tafel fit", "needs 3 or more cathodic points in the window"]);
      if (ta && ta.lf.b > 0) {
        var bfa = 1000 / ta.lf.b, uba = 1000 * ta.lf.ub / (ta.lf.b * ta.lf.b);
        info.push(["anodic Tafel fit (" + ta.n + " points)", "b<sub>a</sub> = " + Sim.fmtU(bfa, uba, "mV/dec") + ", α<sub>a</sub> = " + Sim.sig(2.303 / (p.f * bfa / 1000), 3) + ", log i₀ = " + Sim.fmtU(ta.lf.a, ta.lf.ua)]);
        logser.push({ type: "line", color: "s2", dash: [6, 4], label: "anodic Tafel line", data: [[0, ta.lf.a], [ta.b, ta.lf.a + ta.lf.b * ta.b]] });
      }
      // micro-polarisation within +-10 mV
      var mx = [], my = [];
      pts.forEach(function (q) { if (Math.abs(q[0]) <= 0.0101) { mx.push(q[0]); my.push(q[1]); } });
      if (mx.length >= 3) {
        var ml = S.linfit(mx, my), Rct = 1 / ml.b, i0m = 1 / (p.f * Rct);
        micro.push(["micro-polarisation slope (±10 mV, " + mx.length + " points)", Sim.sig(ml.b * 1000, 3) + " mA cm⁻² V⁻¹ ± " + Sim.sig(ml.ub * 1000, 2)]);
        micro.push(["R<sub>ct</sub> = 1/slope, i₀ = RT/(F R<sub>ct</sub>)", Sim.sig(Rct, 3) + " Ω cm², i₀ = " + Sim.sig(i0m, 3) + " A/cm² (" + (ml.ub / Math.abs(ml.b) > 0.2 ? "poorly defined: the current is close to the noise" : "± " + Math.round(100 * ml.ub / Math.abs(ml.b)) + " %") + ")"]);
      } else micro.push(["micro-polarisation", "include η = −0.01 to +0.01 V in the sweep"]);
      if (p.Ru > 0) micro.push(["largest iR in this sweep", (Math.max.apply(null, bData.pts.map(function (q) { return Math.abs(q[1]); })) * p.Ru * 1000).toFixed(1) + " mV"]);
    }
    logser.push({ type: "vline", x: 0, color: "muted", dash: [2, 4] });
    logser.push({ type: "hline", y: Math.log10(p.i0), color: "muted", dash: [2, 4] });
    bLog.draw(logser, {});
    bLin.draw(lser.concat([{ type: "hline", y: 0, color: "muted" }]), {});
    kvFill($id("b-info"), info);
    kvFill($id("b-micro"), micro.length ? micro : [["status", "Record a polarisation curve."]]);
    csvFns.bv = function () {
      if (!bData) return null;
      return { header: ["E_minus_Eeq_V", "i_A_per_cm2", "Ru_ohm_cm2"], rows: bData.pts.map(function (q) { return [+q[0].toFixed(4), +q[1].toPrecision(5), bData.p.Ru]; }), filename: "polarisation_curve.csv" };
    };
  }
  function setMat(key) {
    var m = MATS[key];
    if (!m) return;
    $id("b-i0").value = String(Math.log10(m.i0));
    $id("b-multi").checked = m.multi;
    $id("b-alpha").value = String(m.ac);
    $id("b-aa").value = m.aa.toFixed(2);
    $id("b-ac").value = m.ac.toFixed(2);
    $id("b-Ru").value = String(m.Ru);
  }
  $id("b-mat").value = preset.mat || "custom";
  $id("b-i0").value = String(Math.log10(preset.i0 || 1e-5));
  $id("b-alpha").value = String(preset.alpha || 0.5);
  if (preset.mat && preset.mat !== "custom") setMat(preset.mat);
  $id("b-mat").addEventListener("change", function () { setMat($id("b-mat").value); bData = null; bvDraw(); });
  ["b-i0", "b-alpha"].forEach(function (id) { $id(id).addEventListener("input", function () { bData = null; bvDraw(); }); });
  ["b-multi", "b-aa", "b-ac", "b-T", "b-Ru", "b-lim", "b-ilim", "b-E1", "b-E2"].forEach(function (id) { $id(id).addEventListener("change", function () { bData = null; bvDraw(); }); });
  ["b-ircorr", "b-t1", "b-t2", "b-a1", "b-a2", "b-target"].forEach(function (id) { $id(id).addEventListener("change", bvDraw); });
  $id("b-run").addEventListener("click", bvRecord);
  $id("b-rerun").addEventListener("click", function () { seed = Sim.newSeed(seed); showSeed(); bvRecord(); });

  /* ======================= tabs and export ======================= */
  Sim.exportCSV($id("x-data"), "voltammetry.csv", function () { var f = csvFns[tabName]; return f ? f() : null; });
  var DRAW = { cv: cvDraw, bv: bvDraw };
  var tabs = Sim.tabs($id("tabs"), function (name) { tabName = name; DRAW[name](); });
  if (tabName === "cv") record();
  tabs.select(tabName);
})();
