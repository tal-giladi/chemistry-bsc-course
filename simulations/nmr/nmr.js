/* nmr simulation, part 2: presets and user interface (lessons 17.3, 17.5).
 * Uses ../common/sim.js (global Sim) and nmr-engine.js (global NMR).
 * Sample effects: TMS at 0 ppm; residual CHCl3 in CDCl3 at 7.26 ppm and dissolved water at 1.56 ppm
 * (Fulmer et al., Organometallics 29, 2176, 2010). Noise is seeded (&seed=<n>).
 */
(function () {
  "use strict";
  var S = Sim.stats;

  var PRESETS = {
    ethyl: {
      title: "An ethyl group: triplet and quartet", mol: "bromoethane", MHz: 60,
      what: "Bromoethane, CH₃CH₂Br, has two kinds of proton. The CH₂ has three neighbours and appears as a quartet (1 : 3 : 3 : 1); the CH₃ has two and appears as a triplet (1 : 2 : 1). Both are split by the same coupling constant J, which is how you know they are partners. The spectrum is computed exactly from the spin Hamiltonian, not from the n+1 rule.",
      task: "Find the peaks. Measure J as the spacing in Hz between neighbouring lines of the quartet and of the triplet, and confirm they are equal. Read the integrals and scale them to 5 H. Then raise the field to 400 MHz: what happens to the width of each multiplet in ppm and in Hz?",
      target: "J ≈ 7.3 Hz in both multiplets; integrals 2 : 3; quartet near 3.43 ppm and triplet near 1.67 ppm; Δν/J = 14.5 at 60 MHz."
    },
    isopropyl: {
      title: "An isopropyl group: doublet and septet", mol: "chloropropane", MHz: 60,
      what: "2-Chloropropane, (CH₃)₂CHCl, has two equivalent CH₃ groups (a mirror plane) and one CH. The six CH₃ protons have one neighbour and give a 6H doublet; the CH has six neighbours and gives a septet (1 : 6 : 15 : 20 : 15 : 6 : 1) whose outer lines are easy to miss.",
      task: "Count the lines of the septet (switch on the first-order sticks if the outer ones hide in the noise, or average more scans). Measure J from both signals and read the integrals.",
      target: "Septet near 4.14 ppm and doublet near 1.54 ppm, J ≈ 6.5 Hz in both; integrals 1 : 6; the outer septet lines are 1/20 of the central one."
    },
    "second-order": {
      title: "Second-order effects at low field", mol: "bromoethane", MHz: 60,
      what: "The n+1 rule assumes the shift difference in Hz is much larger than J. At 60 MHz bromoethane has Δν/J = 14.5, almost first order. Lower the field and Δν shrinks while J stays the same: the inner lines of the two multiplets grow, the outer lines shrink (roofing), extra lines appear and the patterns stop looking like a quartet and a triplet.",
      task: "Lower the field until Δν/J is about 2 and note what happens to the line heights. Compare with the first-order sticks. Then choose the AB pair and watch two doublets turn into a 'roofed' four-line pattern and finally one line.",
      target: "At Δν/J ≈ 2 (about 8 MHz) the inner lines are several times taller than the outer ones and the multiplets lean towards each other; above about 300 MHz the spectrum matches the n+1 sticks."
    },
    unknown: {
      title: "Identify an unknown from its ¹H spectrum", mol: "unknown", MHz: 400,
      what: "A compound with a known molecular formula. Read every signal (shift, integral, multiplicity and J) before you look at the candidates, then choose the structure that explains all of them. 'New unknown' gives another compound.",
      task: "Find the peaks and integrals, write down each signal, compute the DBE, then pick a candidate and check. Read the explanation and the full assignment.",
      target: "The correct structure with every signal assigned (shift, integral, multiplicity and the protons responsible)."
    }
  };

  var preset = Sim.preset(PRESETS, "ethyl");
  var seed0 = Sim.seedFromQuery(17);
  Sim.label();
  Sim.presetBox(Sim.$("#preset"), preset);

  function $(id) { return document.getElementById(id); }
  function tr(cells) { var row = Sim.el("tr"); cells.forEach(function (c) { row.appendChild(Sim.el("td", { html: String(c) })); }); return row; }
  function kv(el, pairs) { el.textContent = ""; pairs.forEach(function (p) { el.appendChild(Sim.el("span", { html: p[0] })); el.appendChild(Sim.el("span", { html: p[1] })); }); }

  var st = { seed: seed0, uSeed: seed0, uIdx: seed0 % NMR.UNKNOWNS.length, sp: null, peaks: [], regions: [], clicks: [], answered: false, cache: {} };
  var plot = Sim.plot($("nmr-plot"), { xLabel: "δ / ppm", yLabel: "intensity", xReverse: true, legend: true });

  // field slider is logarithmic: 5 to 900 MHz
  function fieldMHz() { return Math.round(Math.pow(10, parseFloat($("nmr-field").value)) * 10) / 10; }
  function setField(MHz) { $("nmr-field").value = Math.log10(MHz); }

  function currentMol() {
    var key = $("nmr-mol").value;
    if (key === "unknown") return NMR.UNKNOWNS[st.uIdx % NMR.UNKNOWNS.length];
    return NMR.MOLECULES[key];
  }

  function lineCache(m, MHz) {
    var k = m.name + "@" + MHz;
    if (!st.cache[k]) {
      st.cache[k] = NMR.spectrumLines(m, MHz);
      var keys = Object.keys(st.cache); if (keys.length > 30) delete st.cache[keys[0]];
    }
    return st.cache[k];
  }

  function vals() {
    return {
      MHz: fieldMHz(), lw: parseFloat($("nmr-lw").value), scans: parseInt($("nmr-scans").value, 10),
      wet: $("nmr-wet").checked, lo: parseFloat($("nmr-lo").value), hi: parseFloat($("nmr-hi").value)
    };
  }

  function compute(m, v) {
    var lines = lineCache(m, v.MHz).slice();
    // reference and solvent: TMS (0 ppm), CHCl3 residual (7.26), water (1.56); intensities relative to one proton
    lines.push({ f: 0, I: 0.6, w: 0, tag: "TMS" });
    lines.push({ f: 7.26 * v.MHz, I: 0.04, w: 0, tag: "CHCl₃" });
    if (v.wet) lines.push({ f: 1.56 * v.MHz, I: 0.5, w: 1.5, tag: "H₂O" });
    var lo = Math.min(v.lo, v.hi), hi = Math.max(v.lo, v.hi);
    var fwhmPpm = v.lw / v.MHz;
    var n = Math.min(60000, Math.max(4000, Math.ceil((hi - lo) / (fwhmPpm / 4))));
    var dx = (hi - lo) / (n - 1), y = new Float64Array(n);
    lines.forEach(function (l) {
      var x0 = l.f / v.MHz, g = (v.lw + (l.w || 0)) / v.MHz / 2;   // HWHM in ppm
      var W = 300 * g;
      if (x0 < lo - W || x0 > hi + W) return;
      var i0 = Math.max(0, Math.floor((x0 - W - lo) / dx)), i1 = Math.min(n - 1, Math.ceil((x0 + W - lo) / dx));
      var a = l.I * g / Math.PI;
      for (var i = i0; i <= i1; i++) { var d = lo + i * dx - x0; y[i] += a / (d * d + g * g); }
    });
    // scale: peak of a 1H singlet with 1 Hz width = 1 at any field (heights scale with 1/width)
    var sc = Math.PI * 0.5 / v.MHz;
    var rng = Sim.rng(st.seed), sig = 0.004 * Math.sqrt(16 / v.scans);
    var xs = [], ys = [];
    for (var i = 0; i < n; i++) { xs.push(lo + i * dx); ys.push(y[i] * sc + rng.normal(0, sig)); }
    return { x: xs, y: ys, dx: dx, sig: sig, lines: lines, lo: lo, hi: hi };
  }

  /* ---------- peaks and integrals ---------- */
  function findPeaks(sp, v) {
    var x = sp.x, y = sp.y, n = x.length, out = [];
    var thr = 6 * sp.sig;
    var half = Math.max(1, Math.round(0.45 * v.lw / v.MHz / sp.dx));
    for (var i = 1; i < n - 1; i++) {
      if (y[i] < thr) continue;
      var ok = true;
      for (var j = Math.max(0, i - half); j <= Math.min(n - 1, i + half); j++) if (y[j] > y[i]) { ok = false; break; }
      if (!ok) continue;
      var a = y[i - 1], b = y[i], c = y[i + 1], den = a - 2 * b + c, off = den !== 0 ? 0.5 * (a - c) / den : 0;
      if (Math.abs(off) > 1) off = 0;
      out.push({ d: x[i] + off * sp.dx, h: b });
      i += half;
    }
    out.sort(function (p, q) { return q.d - p.d; });
    return out;
  }
  function findRegions(sp, v) {
    // regions where the smoothed spectrum exceeds a threshold, merged across small gaps
    var y = sp.y, x = sp.x, n = y.length, k = Math.max(1, Math.round(2 * v.lw / v.MHz / sp.dx));
    var cs = [0]; for (var i = 0; i < n; i++) cs.push(cs[i] + y[i]);
    var thr = Math.max(4 * sp.sig / Math.sqrt(2 * k + 1), 0.002), regs = [], inR = false, start = 0;
    var gap = Math.round(Math.max(0.02, 25 / v.MHz) / sp.dx), pad = Math.round(Math.max(0.01, 6 * v.lw / v.MHz) / sp.dx);
    for (i = 0; i < n; i++) {
      var a = Math.max(0, i - k), b = Math.min(n, i + k + 1), m = (cs[b] - cs[a]) / (b - a);
      if (m > thr && !inR) { inR = true; start = i; }
      if ((m <= thr || i === n - 1) && inR) { inR = false; regs.push([start, i]); }
    }
    var merged = [];
    regs.forEach(function (r) { if (merged.length && r[0] - merged[merged.length - 1][1] < gap) merged[merged.length - 1][1] = r[1]; else merged.push(r.slice()); });
    return merged.map(function (r) {
      var i0 = Math.max(0, r[0] - pad), i1 = Math.min(n - 1, r[1] + pad), area = 0;
      for (var j = i0; j <= i1; j++) area += y[j];
      area *= sp.dx;
      var tag = "";
      sp.lines.forEach(function (l) { if (l.tag && l.f / v.MHz >= x[i0] && l.f / v.MHz <= x[i1]) tag = l.tag; });
      return { lo: x[i0], hi: x[i1], area: area, tag: tag, noise: sp.sig * sp.dx * Math.sqrt(i1 - i0 + 1) };
    }).filter(function (r, i, all) {
      var big = Math.max.apply(null, all.map(function (q) { return q.area; }));
      return r.area > 8 * r.noise && r.area > 0.02 * big;
    });
  }

  /* ---------- rendering ---------- */
  function setView(lo, hi) { $("nmr-lo").value = lo.toFixed(2); $("nmr-hi").value = hi.toFixed(2); }
  function fullView(m) {
    var maxd = Math.max.apply(null, m.sites.map(function (s) { return s.d; }));
    setView(-0.5, maxd > 9 ? Math.ceil(maxd + 1) : (maxd > 6.5 ? 8.5 : Math.max(5, Math.ceil(maxd + 1))));
  }

  function render() {
    var m = currentMol(), v = vals();
    var isU = $("nmr-mol").value === "unknown";
    $("nmr-field-out").textContent = v.MHz.toFixed(v.MHz < 20 ? 1 : 0) + " MHz (" + (v.MHz / NMR.GAMMA_H).toFixed(2) + " T)";
    $("nmr-seed").textContent = st.seed;
    $("nmr-unknown").hidden = !isU;
    if (!(Math.abs(v.hi - v.lo) > 0.01)) { fullView(m); v = vals(); }
    var sp = compute(m, v);
    st.sp = sp; st.v = v; st.m = m;
    var series = [{ data: sp.x.map(function (x, i) { return [x, sp.y[i]]; }), color: "s1", width: 1.2, label: "spectrum" }];
    var ymax = Math.max.apply(null, sp.y);
    if ($("nmr-int").checked) {
      var cum = 0, tot = 0, data = [];
      sp.y.forEach(function (yy) { tot += Math.max(0, yy); });
      for (var i = sp.x.length - 1; i >= 0; i--) { cum += Math.max(0, sp.y[i] - 2 * sp.sig); data.push([sp.x[i], cum]); }
      var cmax = cum || 1;
      series.push({ data: data.map(function (d) { return [d[0], d[1] / cmax * ymax * 0.9]; }), color: "s3", width: 1.2, label: "integral" });
    }
    if ($("nmr-fo").checked && !isU) {
      var fo = NMR.firstOrder(m, v.MHz), fmax = Math.max.apply(null, fo.map(function (l) { return l.I; })) || 1;
      var sticks = [];
      fo.forEach(function (l) { var x = l.f / v.MHz; sticks.push([x, NaN], [x, 0], [x, -l.I / fmax * ymax * 0.35]); });
      series.push({ data: sticks, color: "s2", width: 1.5, label: "n+1 rule (first order), drawn downwards" });
    }
    st.clicks.forEach(function (c) { series.push({ type: "vline", x: c, color: "s4", dash: [4, 3], width: 1 }); });
    plot.draw(series, { xMin: sp.lo, xMax: sp.hi });
    // readouts
    var pairs = [["spectrometer", v.MHz.toFixed(v.MHz < 20 ? 1 : 0) + " MHz, B₀ = " + (v.MHz / NMR.GAMMA_H).toFixed(3) + " T"],
      ["1 ppm is", v.MHz.toFixed(1) + " Hz"], ["line width", v.lw + " Hz = " + (v.lw / v.MHz).toFixed(4) + " ppm"]];
    if (!isU) {
      m.J.forEach(function (j) {
        var a = m.sites[j[0]], b = m.sites[j[1]], dv = Math.abs(a.d - b.d) * v.MHz;
        if (!j[2] || dv === 0 || j[2] < 1.5) return;
        var r = dv / j[2];
        pairs.push([a.label + " / " + b.label, "Δν = " + dv.toFixed(1) + " Hz, J = " + j[2] + " Hz, Δν/J = " + r.toFixed(1) + (r > 10 ? " (≈ first order)" : r > 3 ? " (mild second order)" : " (strongly second order)")]);
      });
    } else {
      pairs.push(["molecular formula", m.formula], ["DBE", String(dbe(m.formula))]);
    }
    kv($("nmr-out"), pairs);
    measureOut();
    if (st.peaks.length) analyse(true);
  }

  function dbe(f) {
    var plain = f.replace(/[₀-₉]/g, function (c) { return String(c.charCodeAt(0) - 8320); });
    var cnt = {}; plain.replace(/([A-Z][a-z]?)(\d*)/g, function (_, el, n) { cnt[el] = (cnt[el] || 0) + (n ? parseInt(n, 10) : 1); return ""; });
    var X = (cnt.F || 0) + (cnt.Cl || 0) + (cnt.Br || 0) + (cnt.I || 0);
    return ((2 * (cnt.C || 0) + 2 + (cnt.N || 0) - (cnt.H || 0) - X) / 2);
  }

  function analyse(quiet) {
    if (!st.sp) render();
    var sp = st.sp, v = st.v;
    st.peaks = findPeaks(sp, v);
    var tb = $("nmr-peaks").querySelector("tbody");
    tb.textContent = "";
    st.peaks.forEach(function (p, i) {
      var dHz = i ? (st.peaks[i - 1].d - p.d) * v.MHz : NaN;
      tb.appendChild(tr([i + 1, p.d.toFixed(3), (p.d * v.MHz).toFixed(1), isFinite(dHz) ? dHz.toFixed(2) : "—", p.h.toFixed(3)]));
    });
    st.regions = findRegions(sp, v);
    var sample = st.regions.filter(function (r) { return !r.tag; });
    var minA = sample.length ? Math.min.apply(null, sample.map(function (r) { return r.area; })) : 1;
    var rb = $("nmr-ints").querySelector("tbody");
    rb.textContent = "";
    st.regions.slice().sort(function (a, b) { return b.lo - a.lo; }).forEach(function (r, i) {
      rb.appendChild(tr([i + 1, r.hi.toFixed(2) + " – " + r.lo.toFixed(2), (r.area / minA).toFixed(2), r.tag || ""]));
    });
    if (!quiet) Sim.log($("nmr-log"), "Found " + st.peaks.length + " peaks and " + st.regions.length + " integral regions.");
  }

  function measureOut() {
    var c = st.clicks, v = st.v || vals(), out = $("nmr-measure");
    if (c.length < 2) { out.textContent = c.length ? "Marker at " + c[0].toFixed(3) + " ppm. Click a second point." : "Click two points on the spectrum to measure a spacing."; return; }
    var d = Math.abs(c[0] - c[1]);
    out.textContent = "Markers at " + c[0].toFixed(3) + " and " + c[1].toFixed(3) + " ppm: Δ = " + d.toFixed(4) + " ppm = " + (d * v.MHz).toFixed(2) + " Hz.";
  }

  $("nmr-plot").addEventListener("click", function (e) {
    var r = $("nmr-plot").getBoundingClientRect(), xy = plot.fromPx(e.clientX - r.left, e.clientY - r.top);
    st.clicks.push(xy[0]); if (st.clicks.length > 2) st.clicks.shift();
    render();
  });
  $("nmr-clear").addEventListener("click", function () { st.clicks = []; render(); });

  /* ---------- unknowns ---------- */
  function setupUnknown() {
    var m = currentMol();
    st.answered = false;
    $("nmr-u-formula").textContent = m.formula + " (DBE " + dbe(m.formula) + ")";
    var box = $("nmr-u-cands");
    box.textContent = "";
    var cands = m.candidates.slice();
    var rng = Sim.rng(st.uSeed + 7);
    for (var i = cands.length - 1; i > 0; i--) { var j = rng.int(0, i); var t = cands[i]; cands[i] = cands[j]; cands[j] = t; }
    cands.forEach(function (c, i) {
      var id = "nmr-cand-" + i;
      box.appendChild(Sim.el("div", { class: "row" }, Sim.el("label", { for: id }, Sim.el("input", { type: "radio", name: "nmr-cand", id: id, value: c }), " " + c)));
    });
    $("nmr-u-result").innerHTML = "";
    $("nmr-u-assign").hidden = true;
  }
  function checkUnknown() {
    var m = currentMol(), sel = document.querySelector("input[name=nmr-cand]:checked");
    var out = $("nmr-u-result");
    if (!sel) { out.innerHTML = "<p class=\"warn\">Choose a candidate first.</p>"; return; }
    var ok = sel.value === m.name;
    out.innerHTML = ok ? "<p class=\"good\"><strong>Correct: " + m.name + ".</strong> " + m.why + "</p>"
      : "<p class=\"bad\"><strong>Not " + sel.value + ".</strong> Find the one observation that this structure cannot explain, then try again.</p>";
    if (ok) showAssignment(m);
  }
  function showAssignment(m) {
    var tb = $("nmr-u-table").querySelector("tbody");
    tb.textContent = "";
    var merged = [];
    m.sites.forEach(function (s) {
      var last = merged[merged.length - 1];
      if (last && last.d === s.d && last.mult === s.mult && last.assign === s.assign) last.n += s.n; else merged.push({ d: s.d, n: s.n, mult: s.mult, assign: s.assign, label: s.label });
    });
    merged.forEach(function (s) {
      var js = [];
      m.J.forEach(function (j) { var a = m.sites[j[0]], b = m.sites[j[1]]; if (j[2] >= 1.5 && (a.d === s.d || b.d === s.d) && a.d !== b.d) js.push(j[2]); });
      js = js.filter(function (x, i) { return js.indexOf(x) === i; });
      tb.appendChild(tr([s.d.toFixed(2), s.n + "H", s.mult, js.length ? js.join(", ") : "—", s.assign]));
    });
    $("nmr-u-assign").hidden = false;
  }
  $("nmr-u-check").addEventListener("click", checkUnknown);
  $("nmr-u-show").addEventListener("click", function () { showAssignment(currentMol()); $("nmr-u-result").innerHTML = "<p class=\"muted\">Answer shown: " + currentMol().name + ". " + currentMol().why + "</p>"; });
  $("nmr-u-new").addEventListener("click", function () {
    st.uIdx = (st.uIdx + 1) % NMR.UNKNOWNS.length;
    st.uSeed = Sim.newSeed(st.uSeed); st.seed = st.uSeed; st.peaks = []; st.clicks = [];
    fullView(currentMol()); setupUnknown(); render();
    $("nmr-peaks").querySelector("tbody").textContent = ""; $("nmr-ints").querySelector("tbody").textContent = "";
  });

  /* ---------- wiring ---------- */
  $("nmr-field").addEventListener("input", render);
  ["nmr-lw", "nmr-scans", "nmr-wet", "nmr-lo", "nmr-hi", "nmr-int", "nmr-fo"].forEach(function (id) { $(id).addEventListener("change", render); });
  $("nmr-mol").addEventListener("change", function () {
    st.peaks = []; st.clicks = [];
    $("nmr-peaks").querySelector("tbody").textContent = ""; $("nmr-ints").querySelector("tbody").textContent = "";
    fullView(currentMol());
    if ($("nmr-mol").value === "unknown") setupUnknown();
    render();
  });
  $("nmr-full").addEventListener("click", function () { fullView(currentMol()); render(); });
  $("nmr-zoom").addEventListener("click", function () {
    var m = currentMol(), v = vals(), sites = m.sites.filter(function (s) { return s.w < 5; });
    var idx = (st.zoomIdx = ((st.zoomIdx || 0) + 1) % sites.length), s = sites.slice().sort(function (a, b) { return b.d - a.d; })[idx];
    var half = Math.max(0.12, 45 / v.MHz);
    setView(s.d - half, s.d + half); render();
  });
  $("nmr-find").addEventListener("click", function () { analyse(false); });
  $("nmr-rerun").addEventListener("click", function () { st.seed = Sim.newSeed(st.seed); render(); });
  Sim.exportCSV($("nmr-csv"), "nmr_spectrum.csv", function () {
    var sp = st.sp, step = Math.max(1, Math.floor(sp.x.length / 20000)), rows = [];
    for (var i = 0; i < sp.x.length; i += step) rows.push([sp.x[i].toFixed(5), sp.y[i].toFixed(5)]);
    return { header: ["delta_ppm", "intensity"], rows: rows };
  });
  Sim.exportCSV($("nmr-pcsv"), "nmr_peaks.csv", function () {
    var v = st.v;
    return { header: ["peak", "delta_ppm", "nu_Hz_from_TMS", "height"], rows: st.peaks.map(function (p, i) { return [i + 1, p.d.toFixed(4), (p.d * v.MHz).toFixed(2), p.h.toFixed(4)]; }) };
  });
  Sim.exportCSV($("nmr-icsv"), "nmr_integrals.csv", function () {
    var sample = st.regions.filter(function (r) { return !r.tag; });
    var minA = sample.length ? Math.min.apply(null, sample.map(function (r) { return r.area; })) : 1;
    return { header: ["from_ppm", "to_ppm", "relative_integral", "note"], rows: st.regions.map(function (r) { return [r.hi.toFixed(3), r.lo.toFixed(3), (r.area / minA).toFixed(3), r.tag]; }) };
  });

  // start
  $("nmr-mol").value = preset.mol;
  setField(preset.MHz);
  if (preset.key === "unknown") setupUnknown();
  fullView(currentMol());
  render();
})();
