/* ir-esr simulation, part 1: presets, tabs and the HCl rotation-vibration band (lessons 20.3, 30.1).
 * Uses ../common/sim.js (global Sim) and ir-esr-esr.js (global IRESR_ESR, loaded before this file).
 *
 * Physics. Term values (NIST WebBook, constants of diatomic molecules, H35Cl X 1Sigma+, as in
 * labs/module-30/pc30.py): G(v) = we(v+1/2) - wexe(v+1/2)^2 + weye(v+1/2)^3,
 * F_v(J) = B_v J(J+1) - D [J(J+1)]^2, B_v = Be - ae(v+1/2).
 * we 2990.9463, wexe 52.8186, weye 0.22437, Be 10.593416, ae 0.307181, De 5.3194e-4 cm^-1.
 * H37Cl by isotope scaling with rho = sqrt(mu35/mu37) (NIST atomic masses): we*rho, wexe*rho^2,
 * weye*rho^3, Be*rho^2, ae*rho^3, De*rho^4. Natural abundance of 35Cl 0.7576 (IUPAC).
 * Selection rules Delta J = +-1 (R, P); Delta v = 1 (fundamental) or 2 (overtone, allowed by
 * anharmonicity and the curvature of the dipole function).
 * Line strength: S_band x abundance x Hoenl-London factor (J+1 for R, J for P)/(2J+1) x Boltzmann
 * population of J'' x nu/nu0 x Herman-Wallis factor (1 + C m)^2.
 * Band strengths: fundamental about 5.1e-18 cm/molecule (order of the HITRAN value for the 1-0 band;
 * approximate), overtone 50 times weaker (lesson 30.1). Herman-Wallis C = 0.006 (fundamental) and
 * 0.02 (overtone) are approximate model values that make R lines a little stronger than P lines.
 * Line shape: Voigt (pseudo-Voigt, Thompson-Cox-Hastings) of Doppler width (CODATA k_B, u) and
 * self-broadening, HWHM about 0.24 - 0.01|m| cm^-1/atm (at least 0.06; approximate, of the size
 * HITRAN lists for HCl), scaled by (296/T)^0.7.
 * Beer-Lambert on a fine grid: T(nu) = exp(-sum S phi N L); the spectrometer then convolves the
 * transmittance with a triangular instrument function of FWHM = the resolution (an apodised FTIR),
 * so strong lines saturate (flat tops, apparent broadening) exactly as in a real cell.
 * CODATA 2022 constants come from Sim.C.
 */
(function () {
  "use strict";
  var C = Sim.C, S = Sim.stats;
  var HC_K = C.h * C.c * 100 / C.kB;               // cm K, 1.438777
  var MASS = { H: 1.00782503223, Cl35: 34.968852682, Cl37: 36.965902602 };
  var AB35 = 0.7576;
  var HCL35 = { we: 2990.9463, wexe: 52.8186, weye: 0.22437, Be: 10.593416, ae: 0.307181, De: 5.3194e-4 };
  function mu(a, b) { return a * b / (a + b); }
  var MU35 = mu(MASS.H, MASS.Cl35), MU37 = mu(MASS.H, MASS.Cl37), RHO = Math.sqrt(MU35 / MU37);
  function scale(c, r) {
    return { we: c.we * r, wexe: c.wexe * r * r, weye: c.weye * r * r * r, Be: c.Be * r * r, ae: c.ae * r * r * r, De: c.De * Math.pow(r, 4) };
  }
  var HCL37 = scale(HCL35, RHO);
  var S_BAND = { 1: 5.1e-18, 2: 5.1e-18 / 50 };
  var HW_C = { 1: 0.006, 2: 0.02 };
  var JMAX = 26;

  var PRESETS = {
    hcl: {
      title: "HCl rotation-vibration band", tab: "ir",
      what: "Gas-phase HCl absorbs near 2886 cm⁻¹. Each line is a change of v by one and of J by ±1: the R branch (ΔJ = +1) on the high side, the P branch (ΔJ = −1) on the low side, and a gap of about 4B at the band centre where the forbidden Q branch would be. Line heights follow the Boltzmann population of the lower J. Natural chlorine is 75.8 % ³⁵Cl and 24.2 % ³⁷Cl, so at high resolution every line is a doublet about 2.1 cm⁻¹ apart with intensities (areas) 3 : 1; the peak heights are closer than 3 : 1 because the line centres absorb almost all the light even at low pressure. The spectrum is computed from the NIST constants with Beer–Lambert absorption in a real cell, pressure broadening and the spectrometer's resolution.",
      task: "At 300 K and 4 cm⁻¹ label R(0), R(1), P(1), P(2) and find the gap. Go to 0.5 cm⁻¹ and measure the doublet spacing at R(0) and R(8). Switch off centrifugal distortion and see how far R(10) moves. Raise the pressure from 50 towards 500 mbar until the doublets merge, then switch to the overtone and decide what you must change. Finally find the peaks and fit them.",
      target: "Gap about 4B ≈ 42 cm⁻¹ around 2886 cm⁻¹; doublet spacing about 2.1 cm⁻¹, growing slightly with m; R(10) moves by about 3 cm⁻¹ with D = 0; at 0.5 cm⁻¹ and low pressure the fit gives ν̃₀ ≈ 2886.0 cm⁻¹, B₀ ≈ 10.44 and B₁ ≈ 10.13 cm⁻¹."
    },
    "esr-methyl": {
      title: "Methyl radical hyperfine pattern", tab: "esr", esr: "methyl",
      what: "An unpaired electron in a field B has two spin states gμ<sub>B</sub>B apart, and microwaves of frequency ν flip it when hν = gμ<sub>B</sub>B. Each magnetic nucleus it visits splits the line: n equivalent nuclei of spin I give 2nI + 1 lines with binomial-type heights, a apart (the hyperfine coupling). The spectrometer records the first derivative of the absorption. You start with no nuclei and build CH₃• (g = 2.00255, |a<sub>H</sub>| = 2.304 mT, Fessenden and Schuler 1963).",
      task: "Read the centre of the single line and check it against hν/(gμ<sub>B</sub>). Add protons one at a time up to three, then swap them for deuterons. Raise the modulation amplitude above the line width. Change the frequency from 9.45 to 35 GHz. Then find the lines and fit g and a.",
      target: "Single line at 337.16 mT for 9.4500 GHz; CH₃• lines at 333.70, 336.01, 338.31 and 340.62 mT, heights 1 : 3 : 3 : 1; CD₃• 7 lines spanning 2.12 mT (a<sub>D</sub> = 0.354 mT); at 35 GHz the centre moves to about 1249 mT and the spacing stays 2.304 mT."
    },
    "esr-hydrogen": {
      title: "Hydrogen atom and Breit–Rabi shifts", tab: "esr", esr: "hydrogen",
      what: "In the hydrogen atom the electron is in a 1s orbital, with the most density at the proton, so the hyperfine coupling is huge: A = 1420.405 751 768 MHz (the 21 cm line), 50.7 mT in field units. That is 15 % of the resonance field, so the first-order rule B = B₀ − a m<sub>I</sub> fails: the exact Breit–Rabi levels move both lines down by about a²/4B₀.",
      task: "Compare the exact and first-order line positions at 9.45 GHz, then at 35 GHz. Take the midpoint of the two exact lines as B₀ and compute the naive g.",
      target: "At 9.45 GHz: exact 309.81 and 360.78 mT, first order 311.86 and 362.55 mT, centre shift −1.9 mT, naive g ≈ 2.0137 instead of 2.0023. At 35 GHz the shift is about four times smaller (≈ −0.5 mT): first order works better at high field."
    }
  };

  var preset = Sim.preset(PRESETS, "hcl");
  var seed0 = Sim.seedFromQuery(30);
  Sim.label();
  Sim.presetBox(Sim.$("#preset"), preset);

  function $(id) { return document.getElementById(id); }
  function tr(cells) { var row = Sim.el("tr"); cells.forEach(function (c) { row.appendChild(Sim.el("td", { html: String(c) })); }); return row; }
  function kv(el, pairs) { el.textContent = ""; pairs.forEach(function (p) { el.appendChild(Sim.el("span", { html: p[0] })); el.appendChild(Sim.el("span", { html: p[1] })); }); }

  /* ======================= molecular model ======================= */

  function term(c, v, J, useD) {
    var x = v + 0.5, jj = J * (J + 1);
    var G = c.we * x - c.wexe * x * x + c.weye * x * x * x;
    var Bv = c.Be - c.ae * x;
    return G + Bv * jj - (useD ? c.De * jj * jj : 0);
  }
  function rotE0(c, J, useD) { return term(c, 0, J, useD) - term(c, 0, 0, useD); }

  // all lines of one band; S in cm/molecule (per molecule of HCl, abundance included)
  function bandLines(p) {
    var out = [];
    var isos = [{ name: "35", c: HCL35, ab: AB35, m: MASS.H + MASS.Cl35 }];
    if (p.iso37) isos.push({ name: "37", c: HCL37, ab: 1 - AB35, m: MASS.H + MASS.Cl37 });
    isos.forEach(function (iso) {
      var Q = 0, pops = [];
      for (var J = 0; J <= JMAX + 1; J++) { var w = (2 * J + 1) * Math.exp(-HC_K * rotE0(iso.c, J, true) / p.T); pops.push(w); Q += w; }
      var nu0 = term(iso.c, p.band, 0, p.useD) - term(iso.c, 0, 0, p.useD);
      var massKg = iso.m * C.u;
      for (J = 0; J <= JMAX; J++) {
        var pop = pops[J] / Q;
        var br = [["R", J + 1, J + 1], ["P", J - 1, -J]];
        br.forEach(function (b) {
          var Jup = b[1], m = b[2];
          if (Jup < 0) return;
          var nu = term(iso.c, p.band, Jup, p.useD) - term(iso.c, 0, J, p.useD);
          var hl = (b[0] === "R" ? J + 1 : J) / (2 * J + 1);
          var hw = p.hw ? Math.pow(1 + HW_C[p.band] * m, 2) : 1;
          var stim = 1 - Math.exp(-HC_K * nu / p.T);
          var Sl = S_BAND[p.band] * iso.ab * pop * hl * (nu / nu0) * hw * stim;
          var gS = Math.max(0.06, 0.24 - 0.01 * Math.abs(m)) * Math.pow(296 / p.T, 0.7); // cm-1/atm
          var gL = gS * p.pmbar / 1013.25;
          var gD = nu * Math.sqrt(2 * Math.LN2 * C.kB * p.T / massKg) / C.c;
          out.push({ iso: iso.name, br: b[0], J: J, m: m, nu: nu, S: Sl, gL: gL, gD: gD, label: b[0] + "(" + J + ")" });
        });
      }
    });
    return out;
  }

  function voigtPars(gL, gD) {
    var fL = 2 * gL, fG = 2 * gD;
    var f = Math.pow(Math.pow(fG, 5) + 2.69269 * Math.pow(fG, 4) * fL + 2.42843 * Math.pow(fG, 3) * fL * fL +
      4.47163 * fG * fG * Math.pow(fL, 3) + 0.07842 * fG * Math.pow(fL, 4) + Math.pow(fL, 5), 0.2);
    var r = fL / f;
    var eta = 1.36603 * r - 0.47719 * r * r + 0.11116 * r * r * r;
    return { f: f, eta: Math.min(1, Math.max(0, eta)) };
  }

  // boxcar of k points (centred), in place, by prefix sums with edge clamping
  function boxcar(y, k) {
    if (k <= 1) return y;
    var n = y.length, cs = new Float64Array(n + 1), out = new Float64Array(n), h = Math.floor(k / 2);
    for (var i = 0; i < n; i++) cs[i + 1] = cs[i] + y[i];
    for (i = 0; i < n; i++) {
      var a = Math.max(0, i - h), b = Math.min(n, i - h + k);
      out[i] = (cs[b] - cs[a]) / Math.max(1, b - a);
    }
    return out;
  }

  // the measured spectrum in the window [lo, hi]
  function computeSpectrum(p) {
    var lines = bandLines(p);
    var N = p.pmbar * 100 / (C.kB * p.T) * 1e-6;     // molecules per cm^3
    var lo = p.lo - 2 * p.res, hi = p.hi + 2 * p.res;
    var fmin = Infinity;
    lines.forEach(function (l) {
      var vp = voigtPars(l.gL, l.gD); l.f = vp.f; l.eta = vp.eta; l.amp = l.S * N * p.L;
      if (l.nu > lo - 1 && l.nu < hi + 1) fmin = Math.min(fmin, l.f);
    });
    if (!isFinite(fmin)) fmin = 0.05;
    var h = Math.max((hi - lo) / 450000, Math.min(p.res / 10, fmin / 4));
    var n = Math.floor((hi - lo) / h) + 1;
    var tau = new Float64Array(n);
    var peakTauMax = 0;
    lines.forEach(function (l) {
      var hwf = l.f / 2;
      var Lpk = 1 / (Math.PI * hwf), Gpk = Math.sqrt(Math.LN2 / Math.PI) / hwf;
      var pk = l.amp * (l.eta * Lpk + (1 - l.eta) * Gpk);
      if (l.nu > p.lo && l.nu < p.hi) peakTauMax = Math.max(peakTauMax, pk);
      l.tauPeak = pk;
      var W = Math.sqrt(l.amp * l.eta * hwf / Math.PI / 1e-4);
      W = Math.max(W, 8 * l.f);
      var i0 = Math.max(0, Math.floor((l.nu - W - lo) / h)), i1 = Math.min(n - 1, Math.ceil((l.nu + W - lo) / h));
      var gcut = 5 * hwf, aL = l.amp * l.eta / Math.PI * hwf, aG = l.amp * (1 - l.eta) * Gpk, kG = Math.LN2 / (hwf * hwf);
      for (var i = i0; i <= i1; i++) {
        var d = lo + i * h - l.nu, d2 = d * d;
        var v = aL / (d2 + hwf * hwf);
        if (Math.abs(d) < gcut) v += aG * Math.exp(-kG * d2);
        tau[i] += v;
      }
    });
    var T = new Float64Array(n);
    for (var i = 0; i < n; i++) T[i] = Math.exp(-tau[i]);
    var k = Math.max(1, Math.round(p.res / h));
    var Tc = boxcar(boxcar(T, k), k);
    // sample for display
    var dx = Math.max(p.res / 5, (p.hi - p.lo) / 12000, h);
    var rng = Sim.rng(p.seed);
    var sigT = 0.0046 * Math.sqrt(16 / p.scans);
    var xs = [], ys = [], ts = [];
    for (var x = p.lo; x <= p.hi + 1e-9; x += dx) {
      var j = (x - lo) / h, j0 = Math.floor(j), fr = j - j0;
      var tv = j0 + 1 < n ? Tc[j0] * (1 - fr) + Tc[j0 + 1] * fr : Tc[n - 1];
      var base = 0.004 + 0.00001 * (x - p.lo);
      var tObs = tv * Math.pow(10, -base) + rng.normal(0, sigT);
      ts.push(tObs);
      xs.push(x);
      ys.push(-Math.log10(Math.max(tObs, 0.002)));
    }
    return { lines: lines, x: xs, A: ys, Tr: ts, dx: dx, sigA: sigT / Math.LN10, peakTauMax: peakTauMax, N: N };
  }

  /* ======================= peak finding and fits ======================= */

  function findPeaks(sp, res) {
    var x = sp.x, y = sp.A, n = x.length, out = [];
    var thr = Math.max(0.006, 6 * sp.sigA) + 0.004;
    var half = Math.max(1, Math.round(Math.max(0.6 * res, 0.12) / sp.dx));
    for (var i = 1; i < n - 1; i++) {
      if (y[i] < thr) continue;
      var ok = true;
      for (var j = Math.max(0, i - half); j <= Math.min(n - 1, i + half); j++) { if (y[j] > y[i]) { ok = false; break; } }
      if (!ok) continue;
      var a = y[i - 1], b = y[i], c = y[i + 1], den = a - 2 * b + c;
      var off = den !== 0 ? 0.5 * (a - c) / den : 0;
      if (Math.abs(off) > 1) off = 0;
      out.push({ nu: x[i] + off * sp.dx, A: b - 0.25 * (a - c) * off });
      i += half;
    }
    return out;
  }

  // least squares polynomial fit y = sum c_k x^k, k = 0..deg, with standard uncertainties
  function polyfit(x, y, deg) {
    var m = deg + 1, n = x.length, A = [], b = [];
    for (var r = 0; r < m; r++) { A.push(new Array(m).fill(0)); b.push(0); }
    for (var i = 0; i < n; i++) {
      var pw = [1]; for (var k = 1; k < 2 * m; k++) pw.push(pw[k - 1] * x[i]);
      for (r = 0; r < m; r++) { b[r] += pw[r] * y[i]; for (var c = 0; c < m; c++) A[r][c] += pw[r + c]; }
    }
    // invert A (Gauss-Jordan)
    var M = A.map(function (row, ri) { var e = new Array(m).fill(0); e[ri] = 1; return row.concat(e); });
    for (var col = 0; col < m; col++) {
      var piv = col;
      for (r = col + 1; r < m; r++) if (Math.abs(M[r][col]) > Math.abs(M[piv][col])) piv = r;
      var tmp = M[col]; M[col] = M[piv]; M[piv] = tmp;
      var d = M[col][col]; if (Math.abs(d) < 1e-300) return null;
      for (c = 0; c < 2 * m; c++) M[col][c] /= d;
      for (r = 0; r < m; r++) if (r !== col) { var f = M[r][col]; for (c = 0; c < 2 * m; c++) M[r][c] -= f * M[col][c]; }
    }
    var inv = M.map(function (row) { return row.slice(m); });
    var coef = inv.map(function (row) { return row.reduce(function (s, v, j) { return s + v * b[j]; }, 0); });
    var ss = 0;
    for (i = 0; i < n; i++) { var yy = 0, xp = 1; for (k = 0; k < m; k++) { yy += coef[k] * xp; xp *= x[i]; } ss += (y[i] - yy) * (y[i] - yy); }
    var s2 = n > m ? ss / (n - m) : NaN;
    return { c: coef, u: inv.map(function (row, j) { return Math.sqrt(Math.max(0, row[j] * s2)); }), rms: Math.sqrt(ss / Math.max(1, n)), n: n };
  }

  /* ======================= IR user interface ======================= */

  var ir = { seed: seed0, sp: null, peaks: [], fit: null };
  var irPlot = Sim.plot($("ir-plot"), { xLabel: "wavenumber / cm⁻¹", yLabel: "absorbance", legend: false });
  var irBoltz = Sim.plot($("ir-boltz"), { xLabel: "F₀(J″) / cm⁻¹", yLabel: "ln[A/(|m| ν̃)]", legend: false });
  var irResid = Sim.plot($("ir-resid"), { xLabel: "m", yLabel: "residual / cm⁻¹", legend: false });

  function irVals() {
    var band = parseInt($("ir-band").value, 10);
    return {
      band: band, T: parseFloat($("ir-T").value), pmbar: parseFloat($("ir-p").value), L: parseFloat($("ir-L").value),
      res: parseFloat($("ir-res").value), scans: parseInt($("ir-scans").value, 10), iso37: $("ir-iso").checked,
      useD: $("ir-D").checked, hw: $("ir-hw").checked, lo: parseFloat($("ir-lo").value), hi: parseFloat($("ir-hi").value),
      seed: ir.seed
    };
  }
  function setView(lo, hi) { $("ir-lo").value = lo.toFixed(1); $("ir-hi").value = hi.toFixed(1); }
  function wholeBand(band) { if (band === 2) setView(5560, 5800); else setView(2650, 3080); }

  function predicted(p, br, J, iso) {
    var c = iso === "37" ? HCL37 : HCL35, Jup = br === "R" ? J + 1 : J - 1;
    return term(c, p.band, Jup, p.useD) - term(c, 0, J, p.useD);
  }

  function irRender() {
    var p = irVals();
    $("ir-T-out").textContent = p.T.toFixed(0);
    $("ir-p-out").textContent = p.pmbar.toFixed(0);
    $("ir-seed").textContent = ir.seed;
    if (!(p.hi > p.lo)) { wholeBand(p.band); p = irVals(); }
    var t0 = Date.now();
    var sp = computeSpectrum(p);
    ir.sp = sp; ir.p = p;
    var series = [];
    var showT = $("ir-trans").checked;
    var data = sp.x.map(function (x, i) { return [x, showT ? sp.Tr[i] : sp.A[i]]; });
    series.push({ data: data, color: "s1", width: 1.2 });
    var yMax = Math.max.apply(null, data.map(function (d) { return d[1]; }));
    if ($("ir-labels").checked) {
      sp.lines.forEach(function (l) {
        if (l.iso !== "35" || l.nu < p.lo || l.nu > p.hi || l.J > 12) return;
        var i = Math.round((l.nu - p.lo) / sp.dx), w = Math.max(1, Math.round(p.res / sp.dx));
        var yv = showT ? 1 : 0;
        for (var j = Math.max(0, i - w); j <= Math.min(data.length - 1, i + w); j++) yv = showT ? Math.min(yv, data[j][1]) : Math.max(yv, data[j][1]);
        series.push({ type: "text", x: l.nu, y: showT ? yv - 0.04 : yv + yMax * 0.03, text: l.label, align: "center", color: "muted", font: "10px" });
      });
    }
    irPlot.draw(series, showT ? { yLabel: "transmittance", yMin: 0, yMax: 1.05 } : { yLabel: "absorbance", yMin: -0.02, yMax: Math.max(0.05, yMax * 1.15) });
    // readouts
    var c = HCL35, nu0 = term(c, p.band, 0, p.useD) - term(c, 0, 0, p.useD);
    var nu037 = term(HCL37, p.band, 0, p.useD) - term(HCL37, 0, 0, p.useD);
    var B0 = c.Be - c.ae * 0.5;
    var jmax = Math.sqrt(p.T / (2 * HC_K * B0)) - 0.5;
    var dR0 = predicted(p, "R", 0, "35") - predicted(p, "R", 0, "37");
    var dR8 = predicted(p, "R", 8, "35") - predicted(p, "R", 8, "37");
    var gap = predicted(p, "R", 0, "35") - predicted(p, "P", 1, "35");
    var strongest = sp.lines.filter(function (l) { return l.nu > p.lo && l.nu < p.hi; }).reduce(function (a, l) { return !a || l.tauPeak > a.tauPeak ? l : a; }, null);
    var aTrue = strongest ? strongest.tauPeak / Math.LN10 : 0;
    var aObs = Math.max.apply(null, sp.A);
    // what Beer-Lambert would give if the line were weak: its integrated absorbance spread over the instrument width
    var aLin = strongest ? Math.min(aTrue, strongest.amp / Math.max(p.res, strongest.f) / Math.LN10) + 0.004 : 0;
    var lw = strongest ? strongest.f : NaN;
    var pairs = [
      ["band centre ν̃₀ (H³⁵Cl)", Sim.fmt(nu0, 2) + " cm⁻¹"],
      ["band centre ν̃₀ (H³⁷Cl)", Sim.fmt(nu037, 2) + " cm⁻¹"],
      ["gap R(0) − P(1)", Sim.fmt(gap, 2) + " cm⁻¹ (about 4B)"],
      ["³⁵Cl − ³⁷Cl at R(0) / R(8)", Sim.fmt(dR0, 2) + " / " + Sim.fmt(dR8, 2) + " cm⁻¹"],
      ["most populated J″ (k<sub>B</sub>T/2hcB)<sup>½</sup> − ½", Sim.fmt(jmax, 1)],
      ["true line FWHM (strongest line)", Sim.sig(lw, 2) + " cm⁻¹"],
      ["true peak absorbance at the line centre (before the instrument)", Sim.sig(aTrue, 3)],
      ["observed peak absorbance", Sim.fmt(aObs, 2)],
      ["weak-line (linear) prediction at this resolution", Sim.fmt(aLin, 2)],
      ["noise (absorbance, 1σ)", Sim.sig(sp.sigA, 2)]
    ];
    kv($("ir-out"), pairs);
    var warn = [];
    if (aObs > 1.5) warn.push("The strongest lines are saturated: almost no light gets through at their centres, the tops go flat and noisy and the lines look broader. Positions and heights from these peaks are unreliable. Lower the pressure or the path.");
    else if (aLin > 0.05 && aObs < 0.5 * aLin) warn.push("Note: the line cores are much narrower than the resolution and absorb nearly all the light there, so the observed heights (" + Sim.fmt(aObs, 2) + ") grow more slowly than the number of molecules (weak-line value " + Sim.fmt(aLin, 2) + "). Positions are fine; temperatures from heights will be biased.");
    if (aObs < 10 * sp.sigA) warn.push("The band is barely above the noise: increase the path (multi-pass cell), the pressure or the number of scans.");
    if (p.res >= 2 && p.iso37) warn.push("At " + p.res + " cm⁻¹ each ³⁵Cl/³⁷Cl doublet (2.1 cm⁻¹ apart) is blurred into one peak, which pulls the peak positions.");
    if (p.pmbar > 1013) warn.push("Above 1 atm the cell windows are not rated for this model.");
    $("ir-warn").innerHTML = warn.map(function (w) { return "<p class=\"warn small\">" + w + "</p>"; }).join("");
    $("ir-time").textContent = (Date.now() - t0) + " ms";
  }

  function irAnalyse() {
    if (!ir.sp) irRender();
    var p = ir.p, sp = ir.sp;
    ir.peaks = findPeaks(sp, p.res);
    // assign each peak to the nearest H35Cl line (the numbering a careful student would reach)
    var tol = Math.max(0.6, p.res * 0.6);
    var wrong = $("ir-misnumber").checked;
    var model = sp.lines.filter(function (l) { return l.iso === "35"; });
    var model37 = sp.lines.filter(function (l) { return l.iso === "37"; });
    ir.peaks.forEach(function (pk) {
      var best = null, bd = Infinity;
      model.forEach(function (l) { var d = Math.abs(l.nu - pk.nu); if (d < bd) { bd = d; best = l; } });
      var best37 = null, bd37 = Infinity;
      model37.forEach(function (l) { var d = Math.abs(l.nu - pk.nu); if (d < bd37) { bd37 = d; best37 = l; } });
      if (best && bd < tol && bd <= bd37 + 0.05) { pk.as = best; pk.iso = "35"; }
      else if (best37 && bd37 < tol) { pk.as = best37; pk.iso = "37"; }
      if (pk.as) {
        pk.m = pk.as.m;
        if (wrong && pk.as.br === "P") pk.m = pk.as.m - 1;   // P branch numbered from the wrong gap
        pk.label = pk.as.br + "(" + (pk.as.br === "P" ? -pk.m : pk.m - 1) + ")" + (pk.iso === "37" ? " ³⁷Cl" : "");
      }
    });
    var tb = $("ir-peaks").querySelector("tbody");
    tb.textContent = "";
    ir.peaks.forEach(function (pk, i) {
      tb.appendChild(tr([i + 1, Sim.fmt(pk.nu, 3), Sim.fmt(pk.A, 4), pk.label || "—", pk.m !== undefined ? pk.m : "—"]));
    });
    var use = ir.peaks.filter(function (pk) { return pk.iso === "35"; });
    var out = $("ir-fitout");
    if (use.length < 6) { kv(out, [["fit", "need at least 6 assigned H³⁵Cl peaks (widen the view)"]]); irResid.draw([]); irBoltz.draw([]); return; }
    var f = polyfit(use.map(function (q) { return q.m; }), use.map(function (q) { return q.nu; }), 3);
    if (!f) return;
    var c0 = f.c[0], c1 = f.c[1], c2 = f.c[2], c3 = f.c[3];
    var Blo = (c1 - c2) / 2, Bup = (c1 + c2) / 2, D = -c3 / 4;
    var uB = 0.5 * Math.sqrt(f.u[1] * f.u[1] + f.u[2] * f.u[2]);
    var label = p.band === 1 ? "B₁" : "B₂";
    var res = [["lines used (H³⁵Cl)", String(use.length)],
      ["ν̃₀", Sim.fmtU(c0, f.u[0], "cm⁻¹")],
      ["B₀ = B″", Sim.fmtU(Blo, uB, "cm⁻¹")],
      [label + " = B′", Sim.fmtU(Bup, uB, "cm⁻¹")],
      ["D (from −c₃/4)", Sim.fmtU(D * 1e4, f.u[3] / 4 * 1e4, "× 10⁻⁴ cm⁻¹")],
      ["rms residual", Sim.sig(f.rms, 2) + " cm⁻¹"]];
    if (p.band === 1) {
      var ae = Blo - Bup, Be = Blo + ae / 2;
      var re = Math.sqrt(C.h / (8 * Math.PI * Math.PI * C.c * 100 * Be * MU35 * C.u)) * 1e10;
      res.push(["α<sub>e</sub> = B₀ − B₁", Sim.fmt(ae, 4) + " cm⁻¹"], ["B<sub>e</sub>, r<sub>e</sub>", Sim.fmt(Be, 4) + " cm⁻¹, " + Sim.fmt(re, 4) + " Å (NIST 1.2746 Å)"]);
    }
    // Boltzmann plot from heights
    var bx = [], by = [];
    use.forEach(function (q) {
      var Jlow = q.m > 0 ? q.m - 1 : -q.m;
      var F = Blo * Jlow * (Jlow + 1) - D * Math.pow(Jlow * (Jlow + 1), 2);
      if (q.A > 0) { bx.push(F); by.push(Math.log(q.A / (Math.abs(q.m) * q.nu))); }
    });
    var lf = S.linfit(bx, by);
    var Tfit = -HC_K / lf.b, uT = Math.abs(Tfit * lf.ub / lf.b);
    res.push(["temperature from heights", Sim.fmtU(Tfit, uT, "K") + " (set " + p.T + " K)"]);
    kv(out, res);
    ir.fit = { c: f.c, Blo: Blo, Bup: Bup, D: D, T: Tfit };
    irResid.draw([{ data: use.map(function (q) { var yy = c0 + c1 * q.m + c2 * q.m * q.m + c3 * Math.pow(q.m, 3); return [q.m, q.nu - yy]; }), type: "points", color: "s2" }, { type: "hline", y: 0, color: "muted", width: 1 }]);
    var xr = [Math.min.apply(null, bx), Math.max.apply(null, bx)];
    irBoltz.draw([{ data: bx.map(function (v, i) { return [v, by[i]]; }), type: "points", color: "s1" },
      { data: xr.map(function (v) { return [v, lf.a + lf.b * v]; }), color: "s2", width: 1.5 }]);
  }

  ["ir-band", "ir-T", "ir-p", "ir-L", "ir-res", "ir-scans", "ir-iso", "ir-D", "ir-hw", "ir-lo", "ir-hi", "ir-labels", "ir-trans"].forEach(function (id) {
    $(id).addEventListener(id === "ir-T" || id === "ir-p" ? "input" : "change", function () {
      if (id === "ir-band") wholeBand(parseInt($("ir-band").value, 10));
      irRender();
    });
  });
  $("ir-whole").addEventListener("click", function () { wholeBand(parseInt($("ir-band").value, 10)); irRender(); });
  $("ir-centre").addEventListener("click", function () {
    var p = irVals(), c = p.band === 2 ? 5668 : 2886; setView(c - 50, c + 50); irRender();
  });
  $("ir-r8").addEventListener("click", function () {
    var p = irVals(); var a = predicted(p, "R", 7, "37") - 3, b = predicted(p, "R", 10, "35") + 3; setView(a, b); irRender();
  });
  $("ir-rerun").addEventListener("click", function () { ir.seed = Sim.newSeed(ir.seed); irRender(); if (ir.peaks.length) irAnalyse(); });
  $("ir-fit").addEventListener("click", irAnalyse);
  Sim.exportCSV($("ir-csv"), "hcl_ir_spectrum.csv", function () {
    var sp = ir.sp || computeSpectrum(irVals());
    return { header: ["wavenumber_cm1", "absorbance"], rows: sp.x.map(function (x, i) { return [x.toFixed(4), sp.A[i].toFixed(5)]; }) };
  });
  Sim.exportCSV($("ir-pcsv"), "hcl_ir_peaks.csv", function () {
    return { header: ["peak", "wavenumber_cm1", "absorbance", "assignment", "m"], rows: ir.peaks.map(function (pk, i) { return [i + 1, pk.nu.toFixed(4), pk.A.toFixed(5), pk.label || "", pk.m !== undefined ? pk.m : ""]; }) };
  });

  /* ======================= tabs and start ======================= */

  var esr = window.IRESR_ESR ? window.IRESR_ESR(preset, seed0) : null;
  var tabs = Sim.tabs($("tabs"), function (name) { if (name === "ir") irRender(); else if (esr) esr.render(); });
  tabs.select(preset.tab || "ir");
})();
