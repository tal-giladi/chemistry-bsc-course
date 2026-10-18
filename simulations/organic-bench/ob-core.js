/* organic-bench, part 1: compound data and shared models (lessons 24.1-24.6). Defines global OB.
 * Uses ../common/sim.js (global Sim).
 *
 * Data sources (as in labs/module-24/org24.py, retrieved 2026-10-17):
 *  - melting and boiling points, densities, pKa, log Kow, GHS statements: PubChem compound pages
 *    (salicylic acid 338, aspirin 2244, acetic anhydride 7918, 1-butanol 263, 1-bromobutane 8002,
 *    bromobenzene 7961, benzophenone 3102, biphenyl 7095, benzaldehyde 240, acetone 180, benzoin 8400,
 *    benzilic acid 6463, benzoic acid 243, acetanilide 904); triphenylmethanol and benzil from the NIST
 *    WebBook phase-change pages; dibenzalacetone trans,trans 110-111 C (teaching-lab literature value).
 *  - benzoic acid: Tfus 395.52 K, dfusH 18.006 kJ/mol (NIST WebBook, Ginnings and Furukawa 1953).
 *    Other enthalpies of fusion are estimated with Walden's rule, dfusS = 56.5 J/(mol K): a model value.
 *  - Antoine constants (NIST WebBook): cyclohexane A 3.96988, B 1203.526, C -50.287; toluene A 4.07827,
 *    B 1343.943, C -53.773; log10(P/bar) = A - B/(T/K + C).
 *  - IR bands and 1H shifts are typical literature values (OpenStax Organic Chemistry 12.8 and 13.4,
 *    lessons 24.4-24.6), described by key peaks only. They are NOT copied from SDBS or NIST spectra; the
 *    lessons send you to the real spectra there. TLC Rf values are model values for silica with
 *    ethyl acetate-hexane, calibrated to lesson 24.3 (benzoin 0.34, benzil 0.65 in 20 % EtOAc).
 * R from CODATA 2022 (Sim.C.R).
 */
(function (global) {
  "use strict";
  var R = Sim.C.R;
  var WALDEN = 56.5;

  /* name: M (g/mol), mp (C) or null, bp (C) or null, rho (g/mL) for liquids, dH (J/mol, else Walden),
   * rf20 (Rf in 20 % EtOAc/hexane), s (log10 k' change per unit EtOAc fraction), uv (dark spot at 254 nm),
   * acid (streaks), ir [[band, strength, label]], nmr [[delta, nH, mult, J, label]], ref (index of the NMR
   * peak used to normalise integrals), look (appearance) */
  var C = {
    "salicylic acid": { M: 138.12, mp: 159, rf20: 0.15, s: 3, uv: true, acid: true, look: "white needles",
      ir: [["3230", "m, broad", "phenol O–H (H-bonded)"], ["3000–2500", "m, very broad", "acid O–H"], ["1660", "s", "acid C=O, lowered by the internal H-bond"], ["1610, 1480", "m", "aromatic C=C"]],
      nmr: [[10.4, 1, "br s", 0, "phenol OH"], [7.93, 1, "dd", 7.9, "ArH next to COOH"], [7.53, 1, "td", 7.8, "ArH"], [7.00, 1, "d", 8.3, "ArH next to OH"], [6.94, 1, "t", 7.6, "ArH"]], ref: 1 },
    "aspirin": { M: 180.16, mp: 135, rf20: 0.06, s: 3, uv: true, acid: true, look: "white crystals",
      ir: [["3300–2500", "m, very broad", "acid O–H"], ["1750", "s", "ester C=O (new)"], ["1690", "s", "acid C=O"], ["1605", "m", "aromatic C=C"], ["1190", "s", "ester C–O"]],
      nmr: [[11.5, 1, "br s", 0, "COOH"], [8.12, 1, "dd", 7.9, "ArH next to COOH"], [7.62, 1, "td", 7.8, "ArH"], [7.35, 1, "t", 7.6, "ArH"], [7.14, 1, "d", 8.1, "ArH next to OAc"], [2.36, 3, "s", 0, "acetyl CH₃ (new)"]], ref: 1 },
    "acetic acid": { M: 60.05, mp: 16.6, bp: 118, rf20: 0.1, s: 3, uv: false, acid: true, look: "liquid, vinegar smell",
      ir: [["3300–2500", "s, very broad", "acid O–H"], ["1710", "s", "C=O"]], nmr: [[11.4, 1, "br s", 0, "COOH"], [2.10, 3, "s", 0, "CH₃"]], ref: 1 },
    "ester by-products": { M: 300, mp: null, rf20: 0.12, s: 3, uv: true, acid: true, look: "tan",
      ir: [["1770", "m", "extra ester C=O"]], nmr: [[7.5, 2, "m", 0, "aromatic (oligomeric esters)"]], ref: 0 },
    "1-butanol": { M: 74.12, bp: 117.7, rho: 0.810, rf20: 0.25, s: 5.5, uv: false, look: "colourless liquid",
      ir: [["3330", "s, broad", "O–H"], ["2960–2870", "s", "C–H"], ["1070", "s", "C–O"]],
      nmr: [[3.64, 2, "t", 6.6, "CH₂OH"], [1.55, 2, "quintet", 7, "CH₂"], [1.39, 2, "sextet", 7.4, "CH₂"], [0.94, 3, "t", 7.4, "CH₃"], [1.6, 1, "br s", 0, "OH"]], ref: 0 },
    "1-bromobutane": { M: 137.02, bp: 101.6, rho: 1.276, rf20: 0.85, s: 5.5, uv: false, look: "colourless liquid",
      ir: [["2960–2870", "s", "C–H"], ["1250", "m", "CH₂–Br wag"], ["645", "m", "C–Br"]],
      nmr: [[3.42, 2, "t", 6.8, "CH₂Br (new)"], [1.85, 2, "quintet", 7, "CH₂"], [1.47, 2, "sextet", 7.4, "CH₂"], [0.94, 3, "t", 7.4, "CH₃"]], ref: 0 },
    "dibutyl ether": { M: 130.23, bp: 142, rho: 0.764, rf20: 0.75, s: 5.5, uv: false, look: "colourless liquid",
      ir: [["1120", "s", "C–O–C"]], nmr: [[3.40, 4, "t", 6.6, "OCH₂"], [1.55, 4, "m", 0, "CH₂"], [1.37, 4, "m", 0, "CH₂"], [0.92, 6, "t", 7.3, "CH₃"]], ref: 0 },
    "water": { M: 18.015, mp: 0, bp: 100, rf20: 0, s: 0, uv: false, look: "", ir: [["3400", "s, broad", "O–H of water"], ["1640", "m", "H–O–H bend"]], nmr: [[1.56, 2, "s", 0, "dissolved water"]], ref: 0 },
    "benzophenone": { M: 182.22, mp: 48, rf20: 0.6, s: 5.5, uv: true, look: "white solid",
      ir: [["3060", "w", "aromatic C–H"], ["1660", "s", "conjugated ketone C=O"], ["1600, 1450", "m", "aromatic C=C"]],
      nmr: [[7.80, 4, "d", 7.6, "ArH ortho to C=O"], [7.58, 2, "t", 7.4, "ArH para"], [7.48, 4, "t", 7.6, "ArH meta"]], ref: 0 },
    "triphenylmethanol": { M: 260.34, mp: 162, rf20: 0.35, s: 5.5, uv: true, look: "white crystals",
      ir: [["3470", "m, sharp-ish", "O–H (new)"], ["3060", "w", "aromatic C–H"], ["1490, 1450", "m", "aromatic C=C"], ["1010", "m", "C–O"]],
      nmr: [[7.28, 15, "m", 0, "15 ArH"], [2.78, 1, "s", 0, "OH (new)"]], ref: 0 },
    "biphenyl": { M: 154.21, mp: 69, rf20: 0.9, s: 5.5, uv: true, look: "white flakes",
      ir: [["3060", "w", "aromatic C–H"], ["1480", "m", "aromatic C=C"], ["730, 695", "s", "monosubstituted ring C–H bends"]],
      nmr: [[7.60, 4, "d", 7.5, "ArH ortho"], [7.44, 4, "t", 7.6, "ArH meta"], [7.34, 2, "t", 7.4, "ArH para"]], ref: 0 },
    "benzene": { M: 78.11, bp: 80.1, rf20: 0.95, s: 5.5, uv: true, look: "liquid", ir: [], nmr: [[7.36, 6, "s", 0, "benzene"]], ref: 0 },
    "benzaldehyde": { M: 106.12, bp: 178.1, rho: 1.046, rf20: 0.62, s: 5.5, uv: true, look: "oily liquid, almond smell",
      ir: [["2820, 2720", "w", "aldehyde C–H (Fermi doublet)"], ["1700", "s", "aldehyde C=O"], ["1600, 1585", "m", "aromatic C=C"]],
      nmr: [[10.0, 1, "s", 0, "CHO"], [7.88, 2, "d", 7.5, "ArH ortho"], [7.63, 1, "t", 7.4, "ArH para"], [7.53, 2, "t", 7.6, "ArH meta"]], ref: 0 },
    "benzoic acid": { M: 122.12, mp: 122.4, dH: 18006, rf20: 0.15, s: 3, uv: true, acid: true, look: "white plates",
      ir: [["3300–2500", "m, very broad", "acid O–H"], ["1685", "s", "acid C=O"]],
      nmr: [[12.5, 1, "br s", 0, "COOH"], [8.12, 2, "d", 7.6, "ArH ortho"], [7.62, 1, "t", 7.4, "ArH para"], [7.48, 2, "t", 7.7, "ArH meta"]], ref: 1 },
    "benzalacetone": { M: 146.19, mp: 42, rf20: 0.45, s: 5.5, uv: true, look: "pale yellow, low-melting solid",
      ir: [["1665", "s", "conjugated C=O"], ["1610", "m", "C=C"], ["975", "m", "trans CH=CH bend"]],
      nmr: [[7.55, 2, "m", 0, "ArH"], [7.50, 1, "d", 16.3, "PhCH= (trans)"], [7.40, 3, "m", 0, "ArH"], [6.71, 1, "d", 16.3, "=CHCO"], [2.38, 3, "s", 0, "CH₃CO"]], ref: 4 },
    "dibenzalacetone": { M: 234.29, mp: 111, rf20: 0.5, s: 5.5, uv: true, look: "yellow crystals",
      ir: [["1650", "s", "conjugated C=O (lower than acetone's 1715)"], ["1625", "m", "C=C"], ["980", "m", "trans CH=CH bend"]],
      nmr: [[7.75, 2, "d", 15.9, "PhCH= (trans, J ≈ 16 Hz)"], [7.62, 4, "m", 0, "ArH ortho"], [7.41, 6, "m", 0, "ArH meta, para"], [7.09, 2, "d", 15.9, "=CHCO"]], ref: 0 },
    "benzyl alcohol": { M: 108.14, bp: 205, rf20: 0.25, s: 5.5, uv: true, look: "liquid",
      ir: [["3330", "s, broad", "O–H"]], nmr: [[7.33, 5, "m", 0, "ArH"], [4.67, 2, "s", 0, "CH₂OH"]], ref: 1 },
    "benzoin": { M: 212.24, mp: 137, rf20: 0.34, s: 5.5, uv: true, look: "white crystals",
      ir: [["3415", "m", "O–H"], ["3060", "w", "aromatic C–H"], ["1679", "s", "aryl ketone C=O"], ["1597, 1450", "m", "aromatic C=C"]],
      nmr: [[7.92, 2, "d", 7.6, "ArH ortho to C=O"], [7.40, 8, "m", 0, "8 ArH"], [5.95, 1, "d", 6, "CH(OH) (new)"], [4.55, 1, "d", 6, "OH"]], ref: 2 },
    "benzil": { M: 210.23, mp: 95, rf20: 0.65, s: 5.5, uv: true, look: "bright yellow crystals",
      ir: [["3060", "w", "aromatic C–H"], ["1677, 1660", "s", "two conjugated C=O"], ["1595, 1450", "m", "aromatic C=C"]],
      nmr: [[7.98, 4, "d", 7.6, "ArH ortho"], [7.66, 2, "t", 7.4, "ArH para"], [7.50, 4, "t", 7.7, "ArH meta"]], ref: 0 },
    "benzilic acid": { M: 228.25, mp: 150, rf20: 0.05, s: 3, uv: true, acid: true, look: "white crystals",
      ir: [["3405", "m", "alcohol O–H"], ["3300–2500", "m, very broad", "acid O–H (new)"], ["1718", "s", "acid C=O (moved up)"], ["1490, 1450", "m", "aromatic C=C"]],
      nmr: [[12.8, 1, "br s", 0, "COOH"], [7.35, 10, "m", 0, "10 ArH"], [6.4, 1, "br s", 0, "C–OH"]], ref: 1 },
    "side products": { M: 230, mp: null, rf20: 0.2, s: 4, uv: true, look: "brownish", ir: [["1700", "w", "unidentified C=O"]], nmr: [[7.7, 2, "m", 0, "unexplained aromatic signals"], [5.2, 0.3, "s", 0, "unexplained singlet"]], ref: 0 },
    "acetanilide": { M: 135.17, mp: 114.3, rf20: 0.2, s: 5.5, uv: true, look: "white plates" },
    "2-naphthol": { M: 144.17, mp: 122, rf20: 0.35, s: 5.5, uv: true, look: "white powder" }
  };
  Object.keys(C).forEach(function (k) { C[k].name = k; });

  function rf(name, phi) {
    var c = C[name]; if (!c || !c.rf20) return 0;
    var k20 = 1 / c.rf20 - 1, k = k20 * Math.pow(10, -c.s * (phi - 0.2));
    return 1 / (1 + k);
  }

  // melting range of a solid. comp: {name: mmol}; main: product name; water_g; rate C/min; packing factor
  function meltRange(comp, main, water_g, rate, rng, opts) {
    opts = opts || {};
    var nMain = comp[main] || 0, nOther = 0, mass = 0;
    Object.keys(comp).forEach(function (k) { mass += comp[k] * C[k].M / 1000; if (k !== main && k !== "water") nOther += comp[k]; });
    // the species that is actually the bulk of the solid decides what melts
    var bulk = main, best = nMain;
    Object.keys(comp).forEach(function (k) { if (k !== "water" && C[k].mp !== null && C[k].mp !== undefined && comp[k] > best) { best = comp[k]; bulk = k; } });
    var c = C[bulk], tot = 0;
    Object.keys(comp).forEach(function (k) { if (k !== "water") tot += comp[k]; });
    var xImp = tot > 0 ? (tot - comp[bulk]) / tot : 0;
    var wfrac = water_g / Math.max(1e-9, mass + water_g);
    var x = Math.min(0.6, xImp + 0.25 * wfrac);
    var Tm = c.mp + 273.15, dH = c.dH || WALDEN * Tm;
    var Tend = 1 / (1 / Tm - R * Math.log(1 - x) / dH);
    var dT = Tm - Tend;
    var onset = dT < 0.2 ? Tend - 0.8 : Tend - (1.5 * dT + 0.6);
    if (dT > 10) onset = Math.max(onset, Tend - 15);   // grossly impure: softens over a wide range
    var lag = 0.4 * rate + (opts.loose ? 1 : 0);
    var lo = onset - 273.15 + lag + rng.normal(0, 0.3) - (opts.loose ? 1.5 : 0);
    var hi = Tend - 273.15 + lag + rng.normal(0, 0.3);
    lo = Math.round(lo); hi = Math.round(hi);
    if (hi <= lo) hi = lo + 1;
    return { lo: lo, hi: hi, bulk: bulk, x: x, wfrac: wfrac };
  }

  /* ---------- TLC plate drawing ---------- */
  // lanes: [{label, comp:{name: amount}}]; phi: EtOAc fraction; viz: "uv" | "iodine"; big: spot overload
  function tlc(canvas, lanes, phi, viz, rng, opts) {
    opts = opts || {};
    var ctx = canvas.getContext("2d"), dpr = global.devicePixelRatio || 1;
    var W = canvas.clientWidth || 300, H = canvas.clientHeight || 260;
    canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.fillStyle = Sim.color("plot-bg"); ctx.fillRect(0, 0, W, H);
    var pw = Math.min(W - 20, 60 + lanes.length * 55), px = (W - pw) / 2, top = 14, bot = H - 26;
    var front = opts.front || (62 + rng.normal(0, 1.5));       // mm
    var mm = (bot - top - 12) / 72;                               // plate: start line at 10 mm, 72 mm usable
    var start = bot - 10 * mm;
    ctx.fillStyle = Sim.isDark() ? "#2b3138" : "#f2f2ec";
    ctx.fillRect(px, top, pw, bot - top);
    ctx.strokeStyle = Sim.color("muted"); ctx.lineWidth = 1; ctx.strokeRect(px + 0.5, top + 0.5, pw, bot - top);
    ctx.setLineDash([3, 3]);
    ctx.beginPath(); ctx.moveTo(px, start); ctx.lineTo(px + pw, start); ctx.stroke();
    var fy = start - front * mm;
    if (!opts.noFront) { ctx.beginPath(); ctx.moveTo(px, fy); ctx.lineTo(px + pw, fy); ctx.stroke(); }
    ctx.setLineDash([]);
    ctx.font = "11px " + getComputedStyle(document.body).fontFamily;
    ctx.fillStyle = Sim.color("ink"); ctx.textAlign = "left";
    ctx.fillText("front", px + pw + 3 > W - 30 ? px + 2 : px + pw + 3, fy + 4);
    var spots = [];
    lanes.forEach(function (ln, i) {
      var cx = px + pw * (i + 0.5) / lanes.length;
      ctx.textAlign = "center"; ctx.fillStyle = Sim.color("ink");
      ctx.fillText(ln.label, cx, H - 8);
      var tot = 0; Object.keys(ln.comp).forEach(function (k) { tot += ln.comp[k]; });
      Object.keys(ln.comp).forEach(function (k) {
        var c = C[k]; if (!c || k === "water") return;
        var f = ln.comp[k] / Math.max(1e-12, tot);
        if (f < 0.012) return;
        var vis = viz === "uv" ? c.uv : true;
        if (!vis) return;
        var r = rf(k, phi), d = r * front + rng.normal(0, 0.4);
        var y = start - d * mm;
        var alpha = Math.min(0.9, 0.25 + 0.9 * Math.sqrt(f)) * (viz === "iodine" ? 0.7 : 1);
        var rx = (opts.big ? 9 : 5) * Math.min(1.4, 0.7 + f), ry = rx * 0.75;
        var streak = c.acid || opts.big ? (c.acid ? 6 : 4) * mm : 0;
        ctx.globalAlpha = alpha;
        ctx.fillStyle = viz === "iodine" ? "#8a5a1e" : (Sim.isDark() ? "#9fb3c8" : "#3a4a5c");
        ctx.beginPath(); ctx.ellipse(cx, y + streak / 3, rx, ry + streak / 2, 0, 0, 2 * Math.PI); ctx.fill();
        ctx.globalAlpha = 1;
        spots.push({ lane: ln.label, name: k, dist: d, rf: d / front, streak: !!streak });
      });
    });
    return { front: front, spots: spots };
  }

  /* ---------- spectrum sketches from key peaks ---------- */
  function bandRange(s) {
    var m = String(s).split(",")[0].split("–").map(function (v) { return parseFloat(v); });
    return m.length > 1 ? [Math.min(m[0], m[1]), Math.max(m[0], m[1])] : [m[0], m[0]];
  }
  // bands: [{band, strength, label, w (weight 0..1)}]
  function irSketch(plot, bands) {
    var xs = [], n = 900;
    for (var i = 0; i <= n; i++) xs.push(4000 - 3500 * i / n);
    var y = xs.map(function () { return 0; });
    bands.forEach(function (b) {
      String(b.band).split(",").forEach(function (part) {
        var r = bandRange(part.trim()), c = (r[0] + r[1]) / 2, broad = /broad/.test(b.strength);
        var hw = broad ? Math.max(120, (r[1] - r[0]) / 2) : Math.max(10, (r[1] - r[0]) / 2 + 8);
        var depth = (/^s/.test(b.strength) ? 0.75 : /^m/.test(b.strength) ? 0.45 : 0.2) * (b.w === undefined ? 1 : b.w);
        xs.forEach(function (x, k) { var d = (x - c) / hw; y[k] += depth / (1 + d * d); });
      });
    });
    var T = y.map(function (v) { return 100 * Math.exp(-v); });
    plot.draw([{ data: xs.map(function (x, k) { return [x, T[k]]; }), color: "s1", width: 1.4 }], { yMin: 0, yMax: 105 });
  }
  function pascal(n) { var r = [1]; for (var i = 0; i < n; i++) { var nr = [1]; for (var j = 1; j < r.length; j++) nr.push(r[j - 1] + r[j]); nr.push(1); r = nr; } return r; }
  var MULT = { s: 0, d: 1, t: 2, q: 3, quintet: 4, sextet: 5, septet: 6 };
  function nmrSketch(plot, peaks, MHz) {
    MHz = MHz || 400;
    var lines = [];
    peaks.forEach(function (p) {
      var w = /br/.test(p.mult) ? 30 : 1.2, J = p.J || 7;
      var m = p.mult.replace("br ", "");
      if (m === "m") { for (var k = -3; k <= 3; k++) lines.push({ d: p.d + k * 0.012, I: p.I * Math.exp(-k * k / 4) / 3.4, w: 3 }); return; }
      var pats = [];
      if (m === "dd") pats = [[1, J], [1, 1.7]]; else if (m === "td") pats = [[2, J], [1, 1.5]]; else pats = [[MULT[m] || 0, J]];
      var ls = [{ f: 0, I: 1 }];
      pats.forEach(function (pt) { var row = pascal(pt[0]), tot = Math.pow(2, pt[0]), nx = []; ls.forEach(function (l) { row.forEach(function (h, k) { nx.push({ f: l.f + (k - pt[0] / 2) * pt[1], I: l.I * h / tot }); }); }); ls = nx; });
      ls.forEach(function (l) { lines.push({ d: p.d + l.f / MHz, I: p.I * l.I, w: w }); });
    });
    var maxd = Math.max(9, Math.max.apply(null, peaks.map(function (p) { return p.d; })) + 0.8);
    var n = 5000, xs = [], ys = [];
    for (var i = 0; i < n; i++) { var x = -0.3 + (maxd + 0.3) * i / (n - 1); xs.push(x); ys.push(0); }
    lines.forEach(function (l) {
      var g = l.w / MHz / 2;
      for (var i = 0; i < n; i++) { var d = xs[i] - l.d; ys[i] += l.I * g * g / (d * d + g * g); }
    });
    var ser = [{ data: xs.map(function (x, i) { return [x, ys[i]]; }), color: "s1", width: 1.2 }];
    plot.draw(ser, { xMin: -0.3, xMax: maxd, yMin: 0 });
  }

  function antoineBar(name, T) {
    var A = { cyclohexane: [3.96988, 1203.526, -50.287], toluene: [4.07827, 1343.943, -53.773] }[name];
    return Math.pow(10, A[0] - A[1] / (T + A[2]));
  }

  global.OB = { C: C, rf: rf, meltRange: meltRange, tlc: tlc, irSketch: irSketch, nmrSketch: nmrSketch, antoineBar: antoineBar, R: R };
})(typeof window !== "undefined" ? window : this);
