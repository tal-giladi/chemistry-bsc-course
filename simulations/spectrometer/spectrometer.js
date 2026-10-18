/* spectrometer simulation: a UV-Vis bench (Beer–Lambert, slit bandwidth, stray light, cuvette
 * material, photometric error), two-dye mixture analysis (two wavelengths and full-spectrum least
 * squares), the Fe3+/SCN- equilibrium constant with the incomplete-complexation correction and a
 * Job plot, quinine fluorescence (inner filter, chloride quenching, external calibration and
 * standard addition) and flame AAS of calcium (warm-up, burner height, La, ionisation, background).
 * Uses ../common/sim.js (global Sim).
 *
 * Data and sources:
 *  - Brilliant Blue FCF: specific absorptivity 164 L g-1 cm-1 at 629 nm (FAO/JECFA monograph), 0.006
 *    L mg-1 cm-1 at 426 nm (Lesson 25.1 standards). Tartrazine: E1%1cm 530 at about 426 nm, i.e.
 *    0.053 L mg-1 cm-1 (EU Regulation 231/2012), none at 630 nm. Band shapes are Gaussians fitted to
 *    those values (illustrative). Allura Red band at 504 nm, 0.052 L mg-1 cm-1 (illustrative).
 *  - Stray light A_obs = -log10[(T + s)/(1 + s)] and the error s_c/c = 0.4343 s_T/(T |log T|),
 *    Harvey, Analytical Chemistry 2.1, 10.2–10.3 (Lesson 19.1). Sports drink 64.0 mg/L dye.
 *  - FeSCN2+: K = 140, epsilon = 4600 L mol-1 cm-1 at 447 nm in 0.5 M HNO3 (illustrative teaching-lab
 *    values used in Lesson 23.3). Fe(SCN)2+ stepwise K2 = 20 (illustrative), FeOH2+ hydrolysis
 *    constant 10^-2.2 (order of magnitude of literature values); weak Fe3+ and FeOH2+ absorption at
 *    447 nm and the fading rate are illustrative.
 *  - Quinine in 0.05 M H2SO4: epsilon about 5700 L mol-1 cm-1 near 347 nm, emission near 450 nm
 *    (PhotochemCAD); M = 324.42 g/mol (PubChem); chloride Stern–Volmer K = 130 L/mol; tonic 72.0 mg/L
 *    (Lesson 25.2 data). The 250 nm band height is illustrative.
 *  - Flame AAS calcium (Lesson 25.3 data): A = 0.0420 c - 0.00045 c^2 with La; mineral water 48.0 mg/L,
 *    diluted 1 + 9, read 18 % low without La; spike 2.0 mg/L. Lamp warm-up time constant, burner
 *    profiles, Na sensitivity, ionisation fractions and the brine background are illustrative.
 */
(function () {
  "use strict";
  var S = Sim.stats;

  var PRESETS = {
    "beer-lambert": {
      title: "Beer–Lambert calibration", tab: "uv", stray: 0.4, series: [0, 1, 2, 4, 6],
      what: "A spectrophotometer measures the fraction of light a solution lets through, T = P/P₀, and reports A = −log₁₀T. For a dilute solution A = εbc, so a calibration line of A against c turns a reading into a concentration. Measure at the absorption maximum, where the reading is least sensitive to a small wavelength error, and keep samples inside the range of the standards.",
      task: "Zero on the blank, scan a standard to find λ<sub>max</sub>, then read five standards (0–6 mg/L) and note the slope. Read the sports drink straight from the bottle, then diluted 1 + 19, and report its dye concentration with its uncertainty.",
      target: "λ<sub>max</sub> near 630 nm; slope about 0.161 (absorptivity × 1 cm, a little below the true 0.164 because of the 0.4 % stray light and the slit); the undiluted drink reads about 2.4, the stray-light ceiling, and means nothing; diluted 1 + 19 it reads about 0.52, giving 64 ± 1 mg/L."
    },
    "stray-light": {
      title: "Stray light and the top of the range", tab: "uv", stray: 0, series: [0, 1, 2, 4, 6, 8, 10, 12, 15, 20],
      what: "A little light always reaches the detector without passing through the sample. With a stray fraction s the instrument reports A<sub>obs</sub> = −log₁₀[(T + s)/(1 + s)]: nothing changes at low absorbance, but as T falls towards s the reading flattens, up to a ceiling of −log₁₀[s/(1 + s)].",
      task: "Read the standard series from 0 to 20 mg/L with s = 0 and fit the line through the standards up to 6 mg/L. Raise s to 0.1 % and then to 1 % and read the series again; watch the top standards flatten and the residuals hump and drop. For each s, find the concentration at which the reading is 5 % below the line.",
      target: "With s = 1 % the highest possible reading is 2.00 and the reading is 5 % low near A ≈ 1.2–1.3 (about 7 mg/L against the true slope, about 9 mg/L against your line to 6 mg/L, which the stray light has already pulled down). For s = 0.1 % the 5 % point lies near A ≈ 2.5 (about 15 mg/L), where single readings already scatter by 10 % or more: in practice that range is unusable anyway."
    },
    mixture: {
      title: "Two dyes in one solution", tab: "mix",
      what: "Absorbances add: A(λ) = b[a<sub>B</sub>(λ)c<sub>B</sub> + a<sub>Y</sub>(λ)c<sub>Y</sub>]. Read at two wavelengths and you have two linear equations in two unknowns; choose each wavelength where one dye absorbs strongly and the other weakly. A full-spectrum least-squares fit (classical least squares) uses every wavelength and averages the noise.",
      task: "Record the spectra of pure tartrazine and pure Brilliant Blue standards; note each maximum and how much each absorbs at the other's. Read five standards of each dye at 630 and 426 nm and get the four absorptivities. Read the green drink, solve the 2 × 2 system and compare with the full-spectrum fit. Then change to 500 and 550 nm and compare the scatter of five repeat readings.",
      target: "Absorptivities near 0.164 and 0.000 at 630 nm, 0.006 and 0.053 L mg⁻¹ cm⁻¹ at 426 nm; the diluted drink holds about 4.50 mg/L blue and 9.15 mg/L yellow (22.5 and 45.8 mg/L in the drink), and both methods agree; at 500/550 nm the scatter of c<sub>B</sub> is several times larger."
    },
    equilibrium: {
      title: "FeSCN²⁺ equilibrium constant", tab: "eq",
      what: "Only the blood-red complex absorbs at 447 nm, so its absorbance gives x = [FeSCN²⁺] and an ICE table gives the rest: K = x/([Fe]₀ − x)([SCN]₀ − x). Standards with a large Fe³⁺ excess give εb; mixtures with comparable concentrations give K. The standards are not quite fully complexed, so εb must be corrected and K recomputed until it stops changing.",
      task: "Scan a mixture from 380 to 600 nm and confirm the maximum near 447 nm. Read six standards in 0.200 M Fe³⁺ (SCN⁻ 0 to 2.0 × 10⁻⁴ M) with a matched blank, then five mixtures with 1.00 × 10⁻³ M Fe³⁺ and 2–10 × 10⁻⁴ M SCN⁻ within 15 min, and the Job series at a total of 2.0 × 10⁻³ M. Break it on purpose: one mixture without nitric acid, one with 20 × 10⁻⁴ M SCN⁻, and the standards blanked with water. Export the CSV.",
      target: "Standards on a straight line through almost zero with slope about 4430 L/mol; mixtures between about 0.1 and 0.5; naive K about 145–150, after the correction (96.6 % complexed) K ≈ 140 with a 95 % interval of a few units and no trend; Job maximum at 0.5. Without acid K is far off (hydrolysis to FeOH²⁺); with 20 × 10⁻⁴ M SCN⁻ K reads a few per cent high (Fe(SCN)₂⁺); standards blanked with water give an intercept near 0.07 and a K that is badly wrong."
    },
    fluorescence: {
      title: "Quinine fluorescence in tonic water", tab: "fl",
      what: "Quinine absorbs near 350 nm and emits near 450 nm. The emission is collected at 90° so the lamp beam stays out of the detector, and the signal is proportional to concentration only while the sample absorbs little of the excitation light. Chloride quenches the excited molecule (Stern–Volmer), so standards and samples are made in sulfuric acid.",
      task: "Record an excitation spectrum (emission at 450 nm) and an emission spectrum (excitation at 350 nm). Read undiluted tonic and the dilutions 1 + 9, 1 + 99 and 1 + 199: which is the first whose signal scales with the dilution? Make tonic in 0.05 M HCl and compare. Run a five-point calibration and a five-flask standard addition on the 1 + 99 dilution and compare the two results.",
      target: "Excitation maximum near 347–350 nm, emission near 450 nm; undiluted tonic reads about a quarter of the straight-line value; 1 + 9 is still about 14 % low, 1 + 99 within about 2 % of 1 + 199; in HCl the signal falls about 7.5-fold, so external calibration reads about 10 mg/L while standard addition in HCl still gives the right answer; in H₂SO₄ both methods give 72–74 mg/L (standard addition ± about 1.5 mg/L at 95 %), below the 83 mg/L limit."
    },
    aas: {
      title: "Flame atomic absorption: calcium in mineral water", tab: "aas",
      what: "The sample is sprayed into a flame, where it dries, melts, vaporises and breaks into free atoms; ground-state Ca atoms absorb the 422.7 nm line of a calcium hollow-cathode lamp. Every step of the procedure protects either the number of atoms in the light path or the stability of the lamp. Phosphate and sulfate hold Ca back (a chemical interference, fixed by La); in a hot flame atoms ionise (fixed by excess K).",
      task: "Zero and read a blank every minute as the lamp warms. Optimise the burner height with a 4 mg/L standard. Calibrate 0–10 mg/L and find the linear range from the residuals. Read the water 1 + 9 with La in every solution and without La; read the phosphate standard with and without La. Switch to the Na lamp in the nitrous oxide flame and read a 0.5 mg/L standard with and without K. Turn background correction off and read the salty sample.",
      target: "The blank drifts for about 10–15 min; best height near 7 mm; straight to about 6 mg/L; water 48 ± 1 mg/L with La, about 18 % low without (the La result about 20 % higher); the phosphate standard reads far low without La and about 4.0 with it; spike recovery a few per cent low on the 0–6 mg/L line (the spiked solution lies above it) and about 100 % with the quadratic calibration; K raises the Na signal in the hot flame by about 2.4 times; the salty sample reads high without background correction."
    }
  };

  var preset = Sim.preset(PRESETS, "beer-lambert");
  var seed = Sim.seedFromQuery(23);
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
  function fillBody(tbody, rows) {
    tbody.textContent = "";
    rows.forEach(function (r) {
      var tr = Sim.el("tr");
      r.forEach(function (c) { tr.appendChild(Sim.el("td", typeof c === "object" && c ? c : { html: String(c) })); });
      tbody.appendChild(tr);
    });
  }
  function G(x, mu, sd) { var z = (x - mu) / sd; return Math.exp(-0.5 * z * z); }
  // Harvey eq. 5.12: uncertainty of x from m replicate readings of mean ys on a line a + b x
  function sx(fit, xs, ys, m) {
    var xm = S.mean(xs), sxx = 0, ym = S.mean(fit.ysData);
    xs.forEach(function (x) { sxx += (x - xm) * (x - xm); });
    return fit.s / Math.abs(fit.b) * Math.sqrt(1 / m + 1 / xs.length + Math.pow(ys - ym, 2) / (fit.b * fit.b * sxx));
  }
  function line(xs, ys) { var f = S.linfit(xs, ys); f.ysData = ys; return f; }

  /* ======================= dye spectra (L mg-1 cm-1) ======================= */
  var BB = (function () {
    var h2 = 0.035, sh = function (l) { return h2 * G(l, 585, 22); };
    // solve h1 (629 nm band) and h3 (412 nm band) so that a(629) = 0.164 and a(426) = 0.006
    var a11 = G(629, 629, 26), a12 = G(629, 412, 28), a21 = G(426, 629, 26), a22 = G(426, 412, 28);
    var r1 = 0.164 - sh(629), r2 = 0.006 - sh(426), det = a11 * a22 - a12 * a21;
    var h1 = (r1 * a22 - a12 * r2) / det, h3 = (a11 * r2 - a21 * r1) / det;
    return function (l) { return h1 * G(l, 629, 26) + sh(l) + h3 * G(l, 412, 28) + 0.02 * G(l, 308, 22); };
  })();
  var TZ = function (l) { return 0.053 * G(l, 426, 48) + 0.035 * G(l, 257, 22); };
  var AR = function (l) { return 0.052 * G(l, 504, 35); };
  // average transmittance over a triangular slit of full width at half height bw
  function slitT(Afun, lam, bw) {
    if (bw <= 0.5) return Math.pow(10, -Afun(lam));
    var sum = 0, wsum = 0;
    for (var k = -10; k <= 10; k++) { var d = k / 10 * bw, w = 1 - Math.abs(k) / 10 + 1e-9; sum += w * Math.pow(10, -Afun(lam + d)); wsum += w; }
    return sum / wsum;
  }
  function cellT(cell, l) {
    if (cell === "glass") return 0.92 / (1 + Math.exp(-(l - 310) / 7));
    if (cell === "plastic") return 0.90 / (1 + Math.exp(-(l - 290) / 6));
    return 0.92;
  }

  /* ======================= UV-VIS ======================= */
  var uSpec = Sim.plot($id("u-spec"), { xLabel: "λ / nm", yLabel: "A" });
  var uCal = Sim.plot($id("u-cal"), { xLabel: "c / mg L⁻¹", yLabel: "A" });
  var uRes = Sim.plot($id("u-res"), { xLabel: "c / mg L⁻¹", yLabel: "residual" });
  var uErr = Sim.plot($id("u-err"), { xLabel: "A", yLabel: "s_c/c / %" });
  var uReads = [], uScan = null, uCount = 0, uZero = false;
  var DRINK = 64.0;

  function uSolution() {
    var sol = $id("u-sol").value;
    if (sol === "drink") { var d = parseInt($id("u-dil").value, 10); return { kind: "drink", c: DRINK / d, dil: d, label: d === 1 ? "drink, undiluted" : "drink 1 + " + (d - 1) }; }
    var c = Math.max(0, num("u-c"));
    return { kind: "std", c: c, dil: 1, label: "standard " + c + " mg/L" };
  }
  function uMeasure(c, lam, rng) {
    var s = num("u-stray") / 100, bw = parseFloat($id("u-bw").value), cell = $id("u-cell").value;
    var T = slitT(function (l) { return BB(l) * c; }, lam, bw), Tobs = (T + s) / (1 + s);
    var Tm = Tobs + rng.normal(0, 0.002 / cellT(cell, lam) * 0.92);
    var A = Tm > 1e-5 ? -Math.log10(Tm) : 5;
    if (!uZero) A += 0.045;
    return Math.min(A, 5);
  }
  function uRead(sol) {
    sol = sol || uSolution();
    uCount++;
    var rng = Sim.rng(seed + 17 * uCount), lam = num("u-lam"), a = [];
    for (var k = 0; k < 3; k++) a.push(uMeasure(sol.c, lam, rng));
    var r = { kind: sol.kind, c: sol.c, dil: sol.dil, label: sol.label, lam: lam, A: S.mean(a), sd: S.sd(a), reads: a, s: num("u-stray"), bw: parseFloat($id("u-bw").value), zero: uZero, cell: $id("u-cell").value };
    uReads.push(r);
    $id("u-readout").textContent = r.A >= 4.99 ? "overrange" : r.A.toFixed(3);
    $id("u-readT").textContent = "T = " + (100 * Math.pow(10, -r.A)).toFixed(2) + " %" + (uZero ? "" : " (not zeroed)");
    return r;
  }
  function uFit() {
    var lam = num("u-lam"), max = num("u-max");
    var st = uReads.filter(function (r) { return r.kind === "std" && Math.abs(r.lam - lam) < 0.5; });
    var use = st.filter(function (r) { return r.c <= max + 1e-9; });
    if (use.length < 3) return { st: st, fit: null };
    var xs = use.map(function (r) { return r.c; }), ys = use.map(function (r) { return r.A; });
    return { st: st, xs: xs, ys: ys, fit: line(xs, ys), top: Math.max.apply(null, ys) };
  }
  function uDraw() {
    $id("u-stray-out").textContent = num("u-stray").toFixed(2) + " %";
    $id("u-c-row").hidden = $id("u-sol").value !== "std";
    $id("u-dil-row").hidden = $id("u-sol").value === "std";
    var info = [];
    // spectrum
    if (uScan) uSpec.draw([{ type: "line", color: "s1", label: uScan.label, data: uScan.data }, { type: "vline", x: num("u-lam"), color: "muted", dash: [3, 3] }], { yMin: 0 });
    else uSpec.draw([{ type: "vline", x: num("u-lam"), color: "muted", dash: [3, 3] }], { xMin: 250, xMax: 750, yMin: 0, yMax: 1 });
    var F = uFit(), ser = [], res = [];
    var s = num("u-stray") / 100, bw = parseFloat($id("u-bw").value), lam = num("u-lam");
    var cmax = Math.max(6, F.st.length ? Math.max.apply(null, F.st.map(function (r) { return r.c; })) : 6), model = [];
    for (var i = 0; i <= 100; i++) { var c = cmax * i / 100, T = slitT(function (l) { return BB(l) * c; }, lam, bw); model.push([c, -Math.log10((T + s) / (1 + s))]); }
    ser.push({ type: "line", color: "muted", dash: [4, 4], label: "model (s, slit)", data: model });
    ser.push({ type: "points", color: "s2", label: "standards", data: F.st.map(function (r) { return [r.c, r.A]; }) });
    if (F.fit) {
      var f = F.fit;
      ser.push({ type: "line", color: "s1", label: "line to " + num("u-max") + " mg/L", data: [[0, f.a], [cmax, f.a + f.b * cmax]] });
      res = F.st.map(function (r) { return [r.c, r.A - (f.a + f.b * r.c)]; });
      info.push(["calibration line", "A = " + f.a.toFixed(4) + " + " + f.b.toFixed(4) + " c (s<sub>r</sub> = " + f.s.toFixed(4) + ", R² = " + f.r2.toFixed(4) + ")"]);
      info.push(["absorptivity a (b = 1.00 cm)", Sim.fmtU(f.b, f.ub, "L mg⁻¹ cm⁻¹") + "; ε = a × 792 900 mg/mol = " + Sim.sig(f.b * 792900, 3) + " L mol⁻¹ cm⁻¹"]);
      var dr = uReads.filter(function (r) { return r.kind === "drink" && Math.abs(r.lam - lam) < 0.5; });
      if (dr.length) {
        var d = dr[dr.length - 1], cc = (d.A - f.a) / f.b, u = sx(f, F.xs, d.A, 3);
        var out = d.A > F.top * 1.02;
        info.push(["last drink reading (" + d.label + ")", "A = " + d.A.toFixed(3) + " → " + Sim.fmtU(cc, u, "mg/L") + " in the cell → " + Sim.fmtU(cc * d.dil, u * d.dil, "mg/L") + " in the drink" + (out ? " — above the top standard: the line says nothing here, dilute" : ""), out ? "miss" : ""]);
      }
    } else info.push(["calibration", "read at least three standards (up to the fit limit) at this wavelength"]);
    if (s > 0) info.push(["stray-light ceiling −log₁₀[s/(1 + s)]", (-Math.log10(s / (1 + s))).toFixed(2)]);
    if (!uZero) info.push(["zero", "not zeroed on the blank: every reading includes the cell and water (about +0.045)", "miss"]);
    if ($id("u-cell").value !== "quartz" && lam < 320) info.push(["cuvette", "glass and plastic absorb below about 300 nm: little light reaches the detector and the noise is large", "miss"]);
    uCal.draw(ser, { xMin: 0, yMin: 0 });
    uRes.draw([{ type: "points", color: "s2", data: res }, { type: "hline", y: 0, color: "muted" }], {});
    kvFill($id("u-info"), info);
    fillBody(Sim.$("#u-table tbody"), uReads.slice().reverse().map(function (r) {
      var dev = F.fit && r.kind === "std" && r.c > 0 ? (100 * (r.A - (F.fit.a + F.fit.b * r.c)) / (F.fit.a + F.fit.b * r.c)).toFixed(1) + " %" : "—";
      return [r.label + (r.s ? ", s " + r.s + " %" : ""), r.lam, r.A >= 4.99 ? "overrange" : r.A.toFixed(4), r.sd.toFixed(4), dev];
    }));
    var ec = [];
    for (var j = 1; j <= 125; j++) { var A = j * 0.02, T2 = Math.pow(10, -A); ec.push([A, 100 * 0.4343 * 0.002 / (T2 * Math.abs(Math.log10(T2)))]); }
    var marks = uReads.filter(function (r) { return r.A > 0.02 && r.A < 2.5; }).map(function (r) { var T3 = Math.pow(10, -r.A); return [r.A, 100 * 0.4343 * 0.002 / (T3 * Math.abs(Math.log10(T3)))]; });
    uErr.draw([{ type: "line", color: "s1", label: "s_T = 0.002", data: ec }, { type: "points", color: "s2", label: "your readings", data: marks }, { type: "vline", x: 0.4343, color: "muted", dash: [3, 3] }], { yMin: 0, yMax: 6, xMin: 0, xMax: 2.5 });
    csvFns.uv = function () {
      var rows = [];
      uReads.forEach(function (r) { r.reads.forEach(function (a) { rows.push([r.kind, r.kind === "std" ? r.c : "", r.dil, r.lam, r.bw, r.s, r.cell, +a.toFixed(4)]); }); });
      return { header: ["type", "c_mg_per_L", "dilution_factor", "wavelength_nm", "bandwidth_nm", "stray_percent", "cell", "absorbance"], rows: rows, filename: "uvvis_readings.csv" };
    };
  }
  $id("u-stray").value = String(preset.stray !== undefined ? preset.stray : 0.4);
  $id("u-zero").addEventListener("click", function () { uZero = true; $id("u-readout").textContent = "0.000"; $id("u-readT").textContent = "T = 100 % (blank)"; uDraw(); });
  $id("u-read").addEventListener("click", function () { uRead(); uDraw(); });
  $id("u-series").addEventListener("click", function () { (preset.series || [0, 1, 2, 4, 6, 8, 10, 12, 15, 20]).forEach(function (c) { uRead({ kind: "std", c: c, dil: 1, label: "standard " + c + " mg/L" }); }); uDraw(); });
  $id("u-scan").addEventListener("click", function () {
    uCount++;
    var sol = uSolution(), rng = Sim.rng(seed + 17 * uCount), d = [];
    for (var l = 250; l <= 750; l += 2) d.push([l, uMeasure(sol.c, l, rng)]);
    uScan = { label: sol.label, data: d };
    uDraw();
  });
  $id("u-clear").addEventListener("click", function () { uReads = []; uScan = null; uDraw(); });
  $id("u-rerun").addEventListener("click", function () { seed = Sim.newSeed(seed); showSeed(); uReads = []; uScan = null; uDraw(); });
  ["u-stray"].forEach(function (id) { $id(id).addEventListener("input", uDraw); });
  ["u-sol", "u-lam", "u-bw", "u-cell", "u-max", "u-dil"].forEach(function (id) { $id(id).addEventListener("change", uDraw); });

  /* ======================= MIXTURE ======================= */
  var mSpec = Sim.plot($id("m-spec"), { xLabel: "λ / nm", yLabel: "A" });
  var mReads = [], mScans = [], mCount = 0;
  var MIXCELL = { B: 4.50, Y: 9.15 };
  function mAfun(sol, c) {
    if (sol === "Y") return function (l) { return TZ(l) * c; };
    if (sol === "B") return function (l) { return BB(l) * c; };
    var base = function (l) { return BB(l) * MIXCELL.B + TZ(l) * MIXCELL.Y; };
    if (sol === "GC") return function (l) { return base(l) + 0.030; };
    if (sol === "GR") return function (l) { return base(l) + AR(l) * 2.0; };
    return base;
  }
  function mLabel(sol, c) { return { Y: "tartrazine " + c + " mg/L", B: "Brilliant Blue " + c + " mg/L", G: "green drink 1 + 4", GC: "cloudy green drink 1 + 4", GR: "green drink + red dye 1 + 4" }[sol]; }
  function mRead(sol, c) {
    mCount++;
    var rng = Sim.rng(seed + 29 * mCount), f = mAfun(sol, c), l1 = num("m-l1"), l2 = num("m-l2");
    var A1 = -Math.log10(slitT(f, l1, 2)) + rng.normal(0, 0.002), A2 = -Math.log10(slitT(f, l2, 2)) + rng.normal(0, 0.002);
    mReads.push({ sol: sol, c: c, l1: l1, l2: l2, A1: A1, A2: A2, label: mLabel(sol, c) });
  }
  function mAbs() {     // absorptivities at the current pair from standards (lines through the origin)
    var l1 = num("m-l1"), l2 = num("m-l2"), out = {};
    ["B", "Y"].forEach(function (d) {
      var st = mReads.filter(function (r) { return r.sol === d && r.l1 === l1 && r.l2 === l2; });
      if (st.length >= 2) {
        var x = st.map(function (r) { return r.c; });
        var f1 = S.linfitThrough0(x, st.map(function (r) { return r.A1; })), f2 = S.linfitThrough0(x, st.map(function (r) { return r.A2; }));
        out[d] = { a1: f1.b, u1: f1.ub, a2: f2.b, u2: f2.ub, n: st.length };
      }
    });
    return out;
  }
  function mSolve(ab, A1, A2) {
    var det = ab.B.a1 * ab.Y.a2 - ab.Y.a1 * ab.B.a2;
    return { cB: (A1 * ab.Y.a2 - ab.Y.a1 * A2) / det, cY: (ab.B.a1 * A2 - A1 * ab.B.a2) / det, det: det };
  }
  function cls(scan, pures, baseline) {
    var cols = [pures.B, pures.Y], rows = [];
    scan.data.forEach(function (p, i) { if (p[0] >= 400 && p[0] <= 700) rows.push(i); });
    var k = baseline ? 3 : 2, M = [], v = [];
    for (var a = 0; a < k; a++) { M.push([0, 0, 0].slice(0, k)); v.push(0); }
    rows.forEach(function (i) {
      var x = [cols[0][i][1], cols[1][i][1]]; if (baseline) x.push(1);
      for (var a2 = 0; a2 < k; a2++) { v[a2] += x[a2] * scan.data[i][1]; for (var b = 0; b < k; b++) M[a2][b] += x[a2] * x[b]; }
    });
    var sol = gauss(M, v);
    if (!sol) return null;
    var res = [], ss = 0;
    rows.forEach(function (i) { var fit = sol[0] * cols[0][i][1] + sol[1] * cols[1][i][1] + (baseline ? sol[2] : 0); var e = scan.data[i][1] - fit; ss += e * e; res.push([scan.data[i][0], e]); });
    return { cB: sol[0], cY: sol[1], base: baseline ? sol[2] : 0, rms: Math.sqrt(ss / rows.length), res: res };
  }
  function gauss(M, v) {
    var n = v.length, A = M.map(function (r, i) { return r.slice().concat([v[i]]); });
    for (var c = 0; c < n; c++) {
      var p = c; for (var r = c + 1; r < n; r++) if (Math.abs(A[r][c]) > Math.abs(A[p][c])) p = r;
      var t = A[c]; A[c] = A[p]; A[p] = t;
      if (Math.abs(A[c][c]) < 1e-300) return null;
      for (var r2 = 0; r2 < n; r2++) if (r2 !== c) { var f = A[r2][c] / A[c][c]; for (var k = c; k <= n; k++) A[r2][k] -= f * A[c][k]; }
    }
    return A.map(function (row, i) { return row[n] / A[i][i]; });
  }
  function mDraw() {
    $id("m-c-row").hidden = !($id("m-sol").value === "B" || $id("m-sol").value === "Y");
    var ser = [], colors = { B: "s1", Y: "s5", G: "s3", GC: "s4", GR: "s6" }, info = [], clsRows = [];
    mScans.slice(-5).forEach(function (sc) { ser.push({ type: "line", color: colors[sc.sol], label: sc.label, data: sc.data }); });
    ser.push({ type: "vline", x: num("m-l1"), color: "muted", dash: [3, 3] }, { type: "vline", x: num("m-l2"), color: "muted", dash: [3, 3] });
    // pure spectra per mg/L from the latest standard scans
    var pures = {};
    ["B", "Y"].forEach(function (d) { var sc = mScans.filter(function (s) { return s.sol === d && s.c > 0; }).pop(); if (sc) pures[d] = sc.data.map(function (p) { return [p[0], p[1] / sc.c]; }); });
    var mixScan = mScans.filter(function (s) { return s.sol.charAt(0) === "G"; }).pop();
    if (mixScan && pures.B && pures.Y) {
      var r1 = cls(mixScan, pures, false), r2 = cls(mixScan, pures, true);
      if (r1) {
        clsRows.push(["full-spectrum fit (" + mixScan.label + ")", "c<sub>B</sub> = " + r1.cB.toFixed(3) + ", c<sub>Y</sub> = " + r1.cY.toFixed(3) + " mg/L in the cell; drink × 5: " + (5 * r1.cB).toFixed(1) + " and " + (5 * r1.cY).toFixed(1) + " mg/L"]);
        clsRows.push(["residual (rms, 400–700 nm)", r1.rms.toFixed(4) + (r1.rms > 0.006 ? " — larger than the noise: something absorbs that is not in the model" : " — at the noise level"), r1.rms > 0.006 ? "miss" : ""]);
        clsRows.push(["fit with a constant baseline", "c<sub>B</sub> = " + r2.cB.toFixed(3) + ", c<sub>Y</sub> = " + r2.cY.toFixed(3) + ", baseline " + r2.base.toFixed(4)]);
        ser.push({ type: "line", color: "s2", dash: [2, 2], label: "residual of the fit", data: r1.res });
      }
    } else clsRows.push(["full-spectrum fit", "record spectra of a blue standard, a yellow standard and a drink"]);
    mSpec.draw(ser, { xMin: 380, xMax: 750 });
    kvFill($id("m-cls"), clsRows);
    var ab = mAbs(), tab = [];
    if (ab.B) info.push(["Brilliant Blue at λ₁, λ₂ (" + ab.B.n + " standards)", Sim.fmtU(ab.B.a1, ab.B.u1) + ", " + Sim.fmtU(ab.B.a2, ab.B.u2) + " L mg⁻¹ cm⁻¹"]);
    if (ab.Y) info.push(["tartrazine at λ₁, λ₂ (" + ab.Y.n + " standards)", Sim.fmtU(ab.Y.a1, ab.Y.u1) + ", " + Sim.fmtU(ab.Y.a2, ab.Y.u2) + " L mg⁻¹ cm⁻¹"]);
    var l1 = num("m-l1"), l2 = num("m-l2"), sols = [];
    mReads.forEach(function (r) {
      var cB = "—", cY = "—";
      if (ab.B && ab.Y && r.l1 === l1 && r.l2 === l2) { var s = mSolve(ab, r.A1, r.A2); cB = s.cB.toFixed(3); cY = s.cY.toFixed(3); if (r.sol.charAt(0) === "G") sols.push(s); }
      tab.push([r.label + " (" + r.l1 + "/" + r.l2 + ")", r.A1.toFixed(4), r.A2.toFixed(4), cB, cY]);
    });
    if (sols.length) {
      var bs = sols.map(function (s) { return s.cB; }), ys = sols.map(function (s) { return s.cY; });
      info.push(["drink, 2 × 2 solution (" + sols.length + " readings)", "c<sub>B</sub> = " + S.mean(bs).toFixed(3) + (sols.length > 1 ? " (SD " + S.sd(bs).toFixed(3) + ")" : "") + ", c<sub>Y</sub> = " + S.mean(ys).toFixed(3) + (sols.length > 1 ? " (SD " + S.sd(ys).toFixed(3) + ")" : "") + " mg/L in the cell"]);
      if (ab.B && ab.Y) info.push(["conditioning", "determinant " + Sim.sig(sols[0].det, 3) + " (L mg⁻¹ cm⁻¹)²" + (Math.abs(sols[0].det) < 2e-3 ? " — ill-conditioned: small absorbance errors become large concentration errors" : "")]);
      var naive = ab.Y ? mReads.filter(function (r) { return r.sol.charAt(0) === "G" && r.l2 === l2; }).map(function (r) { return r.A2 / ab.Y.a2; }) : [];
      if (naive.length && ab.Y.a2 > 0.02) info.push(["yellow read at λ₂ alone (ignoring the blue)", S.mean(naive).toFixed(3) + " mg/L"]);
    }
    if (!info.length) info.push(["status", "read standards of both dyes at the same λ₁ and λ₂"]);
    kvFill($id("m-info"), info);
    fillBody(Sim.$("#m-table tbody"), tab.reverse());
    csvFns.mix = function () {
      var rows = mReads.map(function (r) { return ["reading", r.sol, r.c || "", r.l1, +r.A1.toFixed(4), r.l2, +r.A2.toFixed(4)]; });
      mScans.forEach(function (sc) { sc.data.forEach(function (p) { rows.push(["spectrum", sc.sol, sc.c || "", p[0], +p[1].toFixed(4), "", ""]); }); });
      return { header: ["kind", "solution", "c_mg_per_L", "wavelength1_nm", "A1", "wavelength2_nm", "A2"], rows: rows, filename: "two_dye_mixture.csv" };
    };
  }
  $id("m-read").addEventListener("click", function () { mRead($id("m-sol").value, num("m-c")); mDraw(); });
  $id("m-rep").addEventListener("click", function () { for (var i = 0; i < 5; i++) mRead($id("m-sol").value, num("m-c")); mDraw(); });
  $id("m-std").addEventListener("click", function () { [2, 4, 6, 8, 10].forEach(function (c) { mRead("B", c / 2); mRead("Y", c * 1.5); }); mDraw(); });
  $id("m-scan").addEventListener("click", function () {
    mCount++;
    var sol = $id("m-sol").value, c = num("m-c"), f = mAfun(sol, c), rng = Sim.rng(seed + 29 * mCount), d = [];
    for (var l = 380; l <= 750; l += 2) d.push([l, -Math.log10(slitT(f, l, 2)) + rng.normal(0, 0.002)]);
    mScans.push({ sol: sol, c: (sol === "B" || sol === "Y") ? c : 0, label: mLabel(sol, c), data: d });
    mDraw();
  });
  $id("m-clear").addEventListener("click", function () { mReads = []; mScans = []; mDraw(); });
  $id("m-rerun").addEventListener("click", function () { seed = Sim.newSeed(seed); showSeed(); mReads = []; mScans = []; mDraw(); });
  ["m-sol", "m-l1", "m-l2"].forEach(function (id) { $id(id).addEventListener("change", mDraw); });

  /* ======================= FeSCN2+ EQUILIBRIUM ======================= */
  var K1 = 140, K2 = 20, KH = Math.pow(10, -2.2), FADE = 0.0005;
  var eSpec = Sim.plot($id("e-spec"), { xLabel: "λ / nm", yLabel: "A" }), ePlot = Sim.plot($id("e-plot"), { xLabel: "[SCN⁻]₀ / M", yLabel: "A" });
  var eReads = [], eCount = 0, eScan = null;
  function eps1(l) { return 4600 * G(l, 447, 48); }
  function eps2(l) { return 5000 * G(l, 465, 52); }
  function epsFe(l) { return 0.15 * Math.exp(-(l - 447) / 45); }
  function epsFeOH(l) { return 15 * Math.exp(-(l - 447) / 40); }
  function speciate(Fe0, SCN0, acid) {
    var H = acid ? 0.5 : 0.002, lo = 0, hi = SCN0, f = Fe0, s = 0;
    for (var k = 0; k < 100; k++) {
      s = (lo + hi) / 2;
      f = Fe0 / (1 + K1 * s + K1 * K2 * s * s + KH / H);
      var g = s + K1 * f * s + 2 * K1 * K2 * f * s * s - SCN0;
      if (g > 0) hi = s; else lo = s;
    }
    return { f: f, s: s, x1: K1 * f * s, x2: K1 * K2 * f * s * s, foh: f * KH / H };
  }
  function eAbs(sp, l, Fe0, t, blank) {
    var fade = Math.exp(-FADE * t);
    var A = (eps1(l) * sp.x1 + eps2(l) * sp.x2) * fade + epsFe(l) * sp.f + epsFeOH(l) * sp.foh;
    if (blank === "match") { var b0 = speciate(Fe0, 0, true); A -= epsFe(l) * b0.f + epsFeOH(l) * b0.foh; }   // blank: same Fe3+ in 0.5 M HNO3
    return A;
  }
  function eMake(type, Fe0, SCN0) {
    eCount++;
    var rng = Sim.rng(seed + 37 * eCount), acid = chk("e-acid"), lam = num("e-lam"), t = Math.max(0, num("e-time")), blank = $id("e-blank").value;
    var vol = function () { return 1 + rng.normal(0, 0.004); };   // pipetting: about 0.4 % per volume
    var sp = speciate(Fe0 * vol(), SCN0 * vol(), acid), A = eAbs(sp, lam, Fe0, t, blank) + rng.normal(0, 0.002);
    var test = !acid || (type !== "standard" && SCN0 > 1.0001e-3);
    eReads.push({ type: type, Fe0: Fe0, SCN0: SCN0, A: A, lam: lam, acid: acid, blank: blank, t: t, test: test });
  }
  function eAnalyse() {
    var lam = num("e-lam");
    var st = eReads.filter(function (r) { return r.type === "standard" && !r.test && Math.abs(r.lam - lam) < 0.5; });
    var mixes = eReads.filter(function (r) { return r.type === "mix" && Math.abs(r.lam - lam) < 0.5; });
    var out = { st: st, mixes: mixes };
    if (st.length < 3) return out;
    var fit = line(st.map(function (r) { return r.SCN0; }), st.map(function (r) { return r.A; }));
    out.fit = fit;
    var feStd = S.mean(st.map(function (r) { return r.Fe0; }));
    function Kof(r, eb) { var x = (r.A - fit.a) / eb; return x / ((r.Fe0 - x) * (r.SCN0 - x)); }
    mixes.forEach(function (r) { r.Kn = Kof(r, fit.b); });
    var good = mixes.filter(function (r) { return !r.test; });
    var eb = fit.b, frac = 1, Km = good.length ? S.mean(good.map(function (r) { return r.Kn; })) : K1;
    for (var it = 0; it < 30 && good.length; it++) {
      frac = Km * feStd / (1 + Km * feStd); eb = fit.b / frac;
      Km = S.mean(good.map(function (r) { return Kof(r, eb); }));
    }
    mixes.forEach(function (r) { r.Kc = Kof(r, eb); });
    out.eb = eb; out.frac = frac; out.feStd = feStd; out.good = good;
    return out;
  }
  function eDraw() {
    var view = $id("e-view").value, an = eAnalyse(), info = [], ser = [];
    if (eScan) eSpec.draw([{ type: "line", color: "s6", label: eScan.label, data: eScan.data }, { type: "vline", x: num("e-lam"), color: "muted", dash: [3, 3] }], { yMin: 0 });
    else eSpec.draw([{ type: "vline", x: num("e-lam"), color: "muted", dash: [3, 3] }], { xMin: 380, xMax: 600, yMin: 0, yMax: 0.5 });
    if (an.fit) {
      info.push(["standards (" + an.st.length + ")", "A = " + an.fit.a.toFixed(4) + " + " + an.fit.b.toFixed(0) + " [SCN⁻]₀; apparent εb = " + Sim.fmtU(an.fit.b, an.fit.ub, "L/mol")]);
      if (an.st.some(function (r) { return r.blank === "water"; })) info.push(["blank", "standards blanked with water: Fe³⁺ (and a little FeOH²⁺) adds about " + (function () { var b0 = speciate(an.feStd, 0, true), l = num("e-lam"); return epsFe(l) * b0.f + epsFeOH(l) * b0.foh; })().toFixed(3) + " to every standard (intercept)", "miss"]);
    } else info.push(["standards", "read at least three standards (acid, same wavelength)"]);
    if (an.good && an.good.length) {
      var kn = an.good.map(function (r) { return r.Kn; }), kc = an.good.map(function (r) { return r.Kc; }), n = kc.length;
      info.push(["naive K (εb from the standards as measured)", Math.min.apply(null, kn).toFixed(0) + "–" + Math.max.apply(null, kn).toFixed(0) + ", mean " + S.mean(kn).toFixed(1)]);
      info.push(["standards complexed, K[Fe]₀/(1 + K[Fe]₀)", (100 * an.frac).toFixed(1) + " %; corrected εb = " + an.eb.toFixed(0) + " L/mol"]);
      if (n >= 2) {
        var sd = S.sd(kc), ci = S.tInv(0.95, n - 1) * sd / Math.sqrt(n);
        var sorted = an.good.slice().sort(function (a, b) { return a.SCN0 - b.SCN0; });
        info.push(["corrected K (" + n + " mixtures)", S.mean(kc).toFixed(1) + ", SD " + sd.toFixed(1) + ", 95 % interval ± " + ci.toFixed(1)]);
        info.push(["drift (last − first, by [SCN⁻]₀)", (sorted[sorted.length - 1].Kc - sorted[0].Kc).toFixed(1) + (Math.abs(sorted[sorted.length - 1].Kc - sorted[0].Kc) > 3 * sd + 1 ? " — a trend: find the cause" : " — no trend")]);
      }
      var late = an.good.filter(function (r) { return r.t > 15; });
      if (late.length) info.push(["timing", late.length + " mixture(s) read more than 15 min after mixing: the colour fades", "miss"]);
    }
    var tests = an.mixes.filter(function (r) { return r.test; });
    tests.forEach(function (r) { if (isFinite(r.Kc)) info.push(["test: " + (r.acid ? "[SCN⁻]₀ = " + Sim.sig(r.SCN0, 2) + " M" : "no nitric acid"), "K = " + r.Kc.toFixed(0)]); });
    var jobs = eReads.filter(function (r) { return r.type === "job"; });
    if (view === "cal") {
      ePlot = Sim.plot($id("e-plot"), { xLabel: "[SCN⁻]₀ / M", yLabel: "A" });
      ser.push({ type: "points", color: "s2", label: "standards", data: an.st.map(function (r) { return [r.SCN0, r.A]; }) });
      if (an.fit) { var xm = Math.max.apply(null, an.st.map(function (r) { return r.SCN0; })); ser.push({ type: "line", color: "s1", label: "fit", data: [[0, an.fit.a], [xm, an.fit.a + an.fit.b * xm]] }); }
      ePlot.draw(ser, { xMin: 0 });
    } else if (view === "k") {
      ePlot = Sim.plot($id("e-plot"), { xLabel: "[SCN⁻]₀ / M", yLabel: "K" });
      ser.push({ type: "points", color: "s4", label: "naive", data: an.mixes.filter(function (r) { return isFinite(r.Kn); }).map(function (r) { return [r.SCN0, r.Kn]; }) });
      ser.push({ type: "points", color: "s1", label: "corrected", data: an.mixes.filter(function (r) { return isFinite(r.Kc); }).map(function (r) { return [r.SCN0, r.Kc]; }) });
      ePlot.draw(ser, {});
    } else {
      ePlot = Sim.plot($id("e-plot"), { xLabel: "mole fraction of Fe³⁺", yLabel: "A" });
      var jd = jobs.map(function (r) { return [r.Fe0 / (r.Fe0 + r.SCN0), r.A]; }).sort(function (a, b) { return a[0] - b[0]; });
      ser.push({ type: "line", color: "s2", label: "Job series", data: jd });
      ePlot.draw(ser, { xMin: 0, xMax: 1, yMin: 0 });
      if (jd.length >= 3) { var best = jd.reduce(function (a, b) { return b[1] > a[1] ? b : a; }); info.push(["Job maximum", "at x<sub>Fe</sub> = " + best[0].toFixed(2) + " (0.5 for 1:1, 0.33 for FeL₂)"]); }
    }
    kvFill($id("e-info"), info);
    fillBody(Sim.$("#e-table tbody"), eReads.slice().reverse().map(function (r) {
      return [r.test ? "test" : r.type, Sim.sig(r.Fe0, 3), Sim.sig(r.SCN0, 3), r.A.toFixed(4), isFinite(r.Kn) && r.type === "mix" ? r.Kn.toFixed(0) : "—", isFinite(r.Kc) && r.type === "mix" ? r.Kc.toFixed(0) : "—"];
    }));
    csvFns.eq = function () { return { header: ["type", "Fe0_M", "SCN0_M", "A447"], rows: eReads.map(function (r) { return [r.test ? "test" : r.type, +r.Fe0.toPrecision(4), +r.SCN0.toPrecision(4), +r.A.toFixed(4)]; }), filename: "my_fescn.csv" }; };
  }
  function eSetType() {
    var t = $id("e-type").value;
    if (t === "standard") { $id("e-fe").value = "0.200"; $id("e-scn").value = "0.0001"; }
    else if (t === "mix") { $id("e-fe").value = "0.00100"; $id("e-scn").value = "0.00060"; }
    else { $id("e-fe").value = "0.00100"; $id("e-scn").value = "0.00100"; }
  }
  $id("e-type").addEventListener("change", eSetType);
  $id("e-read").addEventListener("click", function () { eMake($id("e-type").value, Math.max(0, num("e-fe")), Math.max(0, num("e-scn"))); eDraw(); });
  $id("e-fstd").addEventListener("click", function () { [0, 0.4, 0.8, 1.2, 1.6, 2.0].forEach(function (s) { eMake("standard", 0.200, s * 1e-4); }); $id("e-view").value = "cal"; eDraw(); });
  $id("e-fmix").addEventListener("click", function () { [2, 4, 6, 8, 10].forEach(function (s) { eMake("mix", 1.00e-3, s * 1e-4); }); $id("e-view").value = "k"; eDraw(); });
  $id("e-fjob").addEventListener("click", function () { for (var i = 1; i <= 9; i++) eMake("job", 2.0e-3 * i / 10, 2.0e-3 * (10 - i) / 10); $id("e-view").value = "job"; eDraw(); });
  $id("e-scan").addEventListener("click", function () {
    eCount++;
    var rng = Sim.rng(seed + 37 * eCount), Fe0 = Math.max(0, num("e-fe")), SCN0 = Math.max(0, num("e-scn")), sp = speciate(Fe0, SCN0, chk("e-acid")), d = [];
    for (var l = 380; l <= 600; l += 2) d.push([l, eAbs(sp, l, Fe0, num("e-time"), $id("e-blank").value) + rng.normal(0, 0.002)]);
    eScan = { label: Sim.sig(Fe0, 2) + " M Fe³⁺, " + Sim.sig(SCN0, 2) + " M SCN⁻", data: d };
    eDraw();
  });
  $id("e-view").addEventListener("change", eDraw);
  $id("e-clear").addEventListener("click", function () { eReads = []; eScan = null; eDraw(); });
  $id("e-rerun").addEventListener("click", function () { seed = Sim.newSeed(seed); showSeed(); eReads = []; eScan = null; eDraw(); });
  ["e-lam", "e-blank", "e-acid"].forEach(function (id) { $id(id).addEventListener("change", eDraw); });

  /* ======================= FLUORESCENCE ======================= */
  var MQ = 324.42, TONIC = 72.0, KSV = 130;
  var fSpec = Sim.plot($id("f-spec"), { xLabel: "λ / nm", yLabel: "F" }), fPlot = Sim.plot($id("f-plot"), { xLabel: "quinine / mg L⁻¹ (standard or added)", yLabel: "F" });
  var fReads = [], fScans = [], fCount = 0;
  function epsQ(l) { return 5700 * G(l, 347, 20) + 24000 * G(l, 250, 12); }
  var KF = 1000 / (epsQ(350) / (MQ * 1000));      // 1.000 mg/L read at 350/450 gives 1000 in the linear limit
  function fSignal(c, ex, em, acid) {
    var cM = c / (MQ * 1000), A = epsQ(ex) * cM;
    var inner = A > 1e-9 ? (Math.pow(10, -0.4 * A) - Math.pow(10, -0.6 * A)) / (0.2 * A * Math.LN10) : 1;   // 0.4–0.6 cm window
    var q = 1 / (1 + KSV * (acid === "hcl" ? 0.05 : 0));
    var lamR = 1e7 / (1e7 / ex - 3400);              // water Raman band
    return KF * epsQ(ex) * cM * inner * G(em, 450, 38) * q + 3 + 6 * G(em, lamR, 6) + 3000 * G(em, ex, 4) + 300 * G(em, 2 * ex, 5);
  }
  function fSol() {
    var s = $id("f-sol").value, c = Math.max(0, num("f-c")), d = parseInt($id("f-dil").value, 10);
    if (s === "blank") return { kind: "blank", c: 0, x: 0, dil: 1, label: "blank" };
    if (s === "std") return { kind: "std", c: c, x: c, dil: 1, label: "standard " + c + " mg/L" };
    if (s === "tonic") return { kind: "tonic", c: TONIC / d, x: NaN, dil: d, label: d === 1 ? "tonic, undiluted" : "tonic 1 + " + (d - 1) };
    return { kind: "sa", c: TONIC / 200 + c, x: c, dil: 200, label: "addition flask +" + c + " mg/L" };
  }
  function fRead(sol, acid) {
    fCount++;
    var rng = Sim.rng(seed + 43 * fCount), ex = num("f-ex"), em = num("f-em"), a = [];
    for (var k = 0; k < 3; k++) a.push(fSignal(sol.c, ex, em, acid) * (1 + rng.normal(0, 0.004)) + rng.normal(0, 0.3));
    fReads.push({ kind: sol.kind, c: sol.c, x: sol.x, dil: sol.dil, label: sol.label, acid: acid, ex: ex, em: em, F: S.mean(a), reads: a });
  }
  function fAnalyse() {
    var at = fReads.filter(function (r) { return Math.abs(r.ex - 350) <= 1 && Math.abs(r.em - 450) <= 1; }), out = {};
    var stds = at.filter(function (r) { return (r.kind === "std" || r.kind === "blank") && r.acid === "h2so4"; });
    if (stds.filter(function (r) { return r.kind === "std"; }).length >= 3) {
      var xs = stds.map(function (r) { return r.x; }), ys = stds.map(function (r) { return r.F; });
      out.ext = line(xs, ys); out.extx = xs; out.stds = stds;
      var ton = at.filter(function (r) { return r.kind === "tonic"; });
      if (ton.length) {
        var last = ton[ton.length - 1], same = ton.filter(function (r) { return r.dil === last.dil && r.acid === last.acid; });
        var Fm = S.mean(same.map(function (r) { return r.F; })), c = (Fm - out.ext.a) / out.ext.b, u = sx(out.ext, xs, Fm, same.length * 3);
        out.ton = { c: c * last.dil, u: u * last.dil, n: same.length, dil: last.dil, acid: last.acid, top: Math.max.apply(null, ys), F: Fm };
      }
    }
    var sa = at.filter(function (r) { return r.kind === "sa"; });
    if (sa.length) {
      var acid = sa[sa.length - 1].acid;
      sa = sa.filter(function (r) { return r.acid === acid; });
      var bl = at.filter(function (r) { return r.kind === "blank" && r.acid === acid; });
      var b0 = bl.length ? S.mean(bl.map(function (r) { return r.F; })) : 0;
      if (sa.length >= 3) {
        var xx = sa.map(function (r) { return r.x; }), yy = sa.map(function (r) { return r.F - b0; }), f = S.linfit(xx, yy), n = xx.length;
        var xm = S.mean(xx), sxx = 0, ym = S.mean(yy);
        xx.forEach(function (x) { sxx += (x - xm) * (x - xm); });
        var xint = f.a / f.b, sxi = f.s / f.b * Math.sqrt(1 / n + ym * ym / (f.b * f.b * sxx));
        out.sa = { fit: f, c: xint * 200, u: sxi * 200, t: S.tInv(0.95, n - 2), acid: acid, blank: bl.length > 0, pts: xx.map(function (x, i) { return [x, yy[i]]; }) };
      }
    }
    return out;
  }
  function fDraw() {
    var s = $id("f-sol").value;
    $id("f-c-row").hidden = !(s === "std" || s === "sa");
    $id("f-dil-row").hidden = s !== "tonic";
    $id("f-c-label").textContent = s === "sa" ? "Quinine added (final) / mg L⁻¹" : "Quinine / mg L⁻¹";
    var sser = [], sinfo = [];
    fScans.slice(-4).forEach(function (sc, i) { sser.push({ type: "line", color: ["s1", "s2", "s3", "s4"][i], label: sc.label, data: sc.data }); });
    fSpec.draw(sser.length ? sser : [{ type: "hline", y: 0, color: "muted" }], { yMin: 0 });
    fScans.slice(-4).forEach(function (sc) {
      var lo = sc.kind === "ex" ? 300 : 0;
      var pk = sc.data.filter(function (p) { return sc.kind === "ex" ? p[0] >= lo && p[0] <= sc.fixed - 20 : p[0] >= sc.fixed + 30; }).reduce(function (a, b) { return b[1] > a[1] ? b : a; }, [0, -1]);
      sinfo.push([sc.label, "maximum near " + pk[0] + " nm" + (sc.kind === "ex" ? " (above 300 nm)" : " (Raman and scatter peaks near the excitation are not fluorescence)")]);
    });
    kvFill($id("f-specinfo"), sinfo);
    var an = fAnalyse(), ser = [], info = [];
    if (an.ext) {
      ser.push({ type: "points", color: "s1", label: "standards (H₂SO₄)", data: an.stds.map(function (r) { return [r.x, r.F]; }) });
      var xm = Math.max.apply(null, an.extx); ser.push({ type: "line", color: "s1", label: "external line", data: [[0, an.ext.a], [xm, an.ext.a + an.ext.b * xm]] });
      info.push(["external calibration", "F = " + an.ext.a.toFixed(1) + " + " + an.ext.b.toFixed(1) + " c (s<sub>r</sub> " + an.ext.s.toFixed(1) + ")"]);
      if (an.ton) info.push(["tonic by external calibration (" + (an.ton.dil === 1 ? "undiluted" : "1 + " + (an.ton.dil - 1)) + ", " + (an.ton.acid === "hcl" ? "in HCl" : "in H₂SO₄") + ")", Sim.fmtU(an.ton.c, an.ton.u, "mg/L") + " (s)" + (an.ton.F > an.ton.top * 1.05 ? " — above the top standard" : "") + (an.ton.acid === "hcl" ? " — chloride quenches the sample but not the standards" : ""), an.ton.acid === "hcl" || an.ton.F > an.ton.top * 1.05 ? "miss" : ""]);
    } else info.push(["external calibration", "read three or more standards in H₂SO₄ at 350/450 nm (Five-point calibration)"]);
    if (an.sa) {
      ser.push({ type: "points", color: "s2", label: "addition flasks" + (an.sa.acid === "hcl" ? " (HCl)" : ""), data: an.sa.pts });
      var f = an.sa.fit, x0 = -f.a / f.b, x1 = Math.max.apply(null, an.sa.pts.map(function (p) { return p[0]; }));
      ser.push({ type: "line", color: "s2", label: "standard addition", data: [[x0, 0], [x1, f.a + f.b * x1]] });
      info.push(["standard addition line", "F = " + f.a.toFixed(1) + " + " + f.b.toFixed(1) + " c<sub>added</sub>" + (an.sa.blank ? " (blank subtracted)" : " — no blank read in this acid, so none subtracted"), an.sa.blank ? "" : "miss"]);
      info.push(["tonic by standard addition", Sim.fmtU(an.sa.c, an.sa.u, "mg/L") + " (s); 95 % interval ± " + (an.sa.t * an.sa.u).toFixed(1) + " mg/L"]);
    }
    var res = an.sa ? an.sa.c : an.ton ? an.ton.c : NaN;
    if (isFinite(res)) info.push(["against the 83 mg/L limit (21 CFR 172.575)", res < 83 ? "below" : "not below", res < 83 ? "hit" : "miss"]);
    fPlot.draw(ser.length ? ser : [{ type: "hline", y: 0, color: "muted" }], {});
    kvFill($id("f-info"), info);
    fillBody(Sim.$("#f-table tbody"), fReads.slice().reverse().map(function (r) { return [r.label, r.acid === "hcl" ? "HCl" : "H₂SO₄", r.ex + "/" + r.em, r.F.toFixed(1), r.kind === "tonic" ? (r.F * r.dil).toFixed(0) : "—"]; }));
    csvFns.fl = function () {
      var rows = [];
      fReads.forEach(function (r) { r.reads.forEach(function (F) { rows.push([r.kind, isFinite(r.x) ? r.x : "", r.dil, r.acid, r.ex, r.em, +F.toFixed(1)]); }); });
      return { header: ["type", "quinine_added_or_std_mg_per_L", "dilution_factor", "acid", "ex_nm", "em_nm", "fluorescence"], rows: rows, filename: "quinine_fluorimeter.csv" };
    };
  }
  $id("f-read").addEventListener("click", function () { fRead(fSol(), $id("f-acid").value); fDraw(); });
  $id("f-cal").addEventListener("click", function () {
    $id("f-ex").value = "350"; $id("f-em").value = "450";
    fRead({ kind: "blank", c: 0, x: 0, dil: 1, label: "blank" }, "h2so4");
    [0.1, 0.2, 0.3, 0.4, 0.5].forEach(function (c) { fRead({ kind: "std", c: c, x: c, dil: 1, label: "standard " + c + " mg/L" }, "h2so4"); });
    fDraw();
  });
  $id("f-sadd").addEventListener("click", function () {
    $id("f-ex").value = "350"; $id("f-em").value = "450";
    var acid = $id("f-acid").value;
    fRead({ kind: "blank", c: 0, x: 0, dil: 1, label: "blank" }, acid);
    [0, 0.1, 0.2, 0.3, 0.4].forEach(function (c) { fRead({ kind: "sa", c: TONIC / 200 + c, x: c, dil: 200, label: "addition flask +" + c + " mg/L" }, acid); });
    fDraw();
  });
  function fScan(kind) {
    fCount++;
    var sol = fSol(), acid = $id("f-acid").value, rng = Sim.rng(seed + 43 * fCount), d = [], fixed = kind === "ex" ? num("f-em") : num("f-ex");
    if (kind === "ex") for (var l = 220; l <= 420; l += 2) d.push([l, fSignal(sol.c, l, fixed, acid) * (1 + rng.normal(0, 0.004))]);
    else for (var m = 300; m <= 650; m += 2) d.push([m, fSignal(sol.c, fixed, m, acid) * (1 + rng.normal(0, 0.004))]);
    var top = Math.max.apply(null, d.filter(function (p) { return Math.abs(p[0] - fixed) > 25; }).map(function (p) { return p[1]; }));
    d = d.map(function (p) { return [p[0], Math.min(p[1], top * 1.3)]; });
    fScans.push({ kind: kind, fixed: fixed, label: (kind === "ex" ? "excitation, em " : "emission, ex ") + fixed + " nm (" + sol.label + ")", data: d });
    fDraw();
  }
  $id("f-exscan").addEventListener("click", function () { fScan("ex"); });
  $id("f-emscan").addEventListener("click", function () { fScan("em"); });
  $id("f-clear").addEventListener("click", function () { fReads = []; fScans = []; fDraw(); });
  $id("f-rerun").addEventListener("click", function () { seed = Sim.newSeed(seed); showSeed(); fReads = []; fScans = []; fDraw(); });
  ["f-sol", "f-dil", "f-acid"].forEach(function (id) { $id(id).addEventListener("change", fDraw); });

  /* ======================= FLAME AAS ======================= */
  var aPlot = Sim.plot($id("a-plot"), { xLabel: "c / mg L⁻¹", yLabel: "A" });
  var aRes = Sim.plot($id("a-res"), { xLabel: "c / mg L⁻¹", yLabel: "residual" });
  var aDrift = Sim.plot($id("a-drift"), { xLabel: "t since the lamp was switched on / min", yLabel: "A" });
  var aClock = 0, aRef = null, aReads = [], aCount = 0, aProfile = null;
  var WATER = 48.0;
  function lampI(t) { return 1 - 0.06 * Math.exp(-t / 4); }
  function aCond() { return { el: $id("a-el").value, flame: $id("a-flame").value, h: num("a-h"), bg: chk("a-bg"), la: $id("a-la").value, k: chk("a-k") }; }
  function caA(c) { var x = Math.min(c, 46); return 0.0420 * x - 0.00045 * x * x; }
  function naA(c) { return 1.6 * (1 - Math.exp(-0.40 * c / 1.6)); }
  // true absorbance (before lamp drift and noise) of a solution under the conditions
  function aTrue(sol, c, k) {
    var isStd = sol === "std" || sol === "blank";
    var laIn = k.la === "all" || (k.la === "samples" && !isStd);
    var hot = k.flame === "n2o", el = k.el;
    var hopt = el === "Ca" ? (hot ? 10 : 7) : (hot ? 8 : 5), g = G(k.h, hopt, 3.0);
    var conc, fac = 1;
    if (el === "Ca") {
      conc = { blank: 0, std: c, water: WATER / 10, spike: WATER / 10 + 2.0, phos: 4.0, salt: 4.0 }[sol];
      if (!hot) { fac *= { water: laIn ? 1 : 0.845, phos: laIn ? 1 : 0.64, salt: laIn ? 1 : 0.90, spike: laIn ? 1 : 0.845 }[sol] || 1; }   // with the 3 % La effect below: water 18 % low without La
      else fac *= 0.9 * (k.k ? 0.98 : 0.75);
      fac *= laIn ? 1 : 0.97;
    } else {
      conc = { blank: 0, std: c, water: 1.2, spike: 1.2, phos: 0, salt: 40 }[sol];
      fac *= hot ? (k.k ? 0.97 : 0.40) : (k.k ? 1.0 : 0.90);
    }
    if (sol === "salt") fac *= 0.95;                        // salt and viscosity: less sample reaches the flame
    var A = (el === "Ca" ? caA(conc * fac * g) : naA(conc * fac * g));
    if (sol === "salt") A += k.bg ? 0.0005 : (el === "Ca" ? 0.035 : 0.02);
    return A;
  }
  function aRead(sol, c) {
    aCount++;
    var k = aCond(), rng = Sim.rng(seed + 59 * aCount), a = [];
    aClock += 0.5;
    var ref = aRef === null ? lampI(0) : aRef;
    for (var i = 0; i < 3; i++) a.push(aTrue(sol, c, k) + Math.log10(ref / lampI(aClock)) + rng.normal(0, 0.0015));
    var labels = { blank: "blank", std: k.el + " standard " + c + " mg/L", water: "water 1 + 9", spike: "water 1 + 9 + 2.0 mg/L", phos: "4 mg/L Ca + phosphate", salt: "brine 1 + 9" };
    aReads.push({ t: aClock, sol: sol, c: c, label: labels[sol], k: k, A: S.mean(a), sd: S.sd(a), reads: a });
    $id("a-clock").textContent = aClock.toFixed(1);
  }
  function aCalib() {
    var last = aReads.length ? aReads[aReads.length - 1].k : aCond();
    var same = function (r) { return r.k.el === last.el && r.k.flame === last.flame && r.k.k === last.k && Math.abs(r.k.h - last.h) < 0.01; };
    var st = aReads.filter(function (r) { return r.sol === "std" && same(r); });
    var bl = aReads.filter(function (r) { return r.sol === "blank" && same(r); }).slice(-1);
    var pts = st.map(function (r) { return [r.c, r.A]; }).concat(bl.map(function (r) { return [0, r.A]; }));
    var out = { pts: pts, same: same, last: last };
    var lin = pts.filter(function (p) { return p[0] <= num("a-max") + 1e-9; });
    if (lin.length >= 3) { out.lin = line(lin.map(function (p) { return p[0]; }), lin.map(function (p) { return p[1]; })); out.linx = lin.map(function (p) { return p[0]; }); }
    if (chk("a-quad") && pts.length >= 4) {
      var M = [[0, 0, 0], [0, 0, 0], [0, 0, 0]], v = [0, 0, 0];
      pts.forEach(function (p) { var x = [1, p[0], p[0] * p[0]]; for (var a = 0; a < 3; a++) { v[a] += x[a] * p[1]; for (var b = 0; b < 3; b++) M[a][b] += x[a] * x[b]; } });
      out.quad = gauss(M, v);
    }
    return out;
  }
  function aConc(cal, A) {
    if (cal.quad) { var q = cal.quad, a = q[2], b = q[1], c = q[0] - A; if (Math.abs(a) < 1e-12) return -c / b; return (-b + Math.sqrt(Math.max(0, b * b - 4 * a * c))) / (2 * a); }
    return cal.lin ? (A - cal.lin.a) / cal.lin.b : NaN;
  }
  function aDraw() {
    $id("a-h-out").textContent = num("a-h").toFixed(1) + " mm";
    $id("a-c-row").hidden = $id("a-sol").value !== "std";
    var cal = aCalib(), ser = [], res = [], info = [];
    ser.push({ type: "points", color: "s2", label: "standards", data: cal.pts });
    var xmax = cal.pts.length ? Math.max.apply(null, cal.pts.map(function (p) { return p[0]; })) : 10;
    if (cal.lin) {
      var L = cal.lin;
      ser.push({ type: "line", color: "s1", label: "line to " + num("a-max") + " mg/L", data: [[0, L.a], [xmax, L.a + L.b * xmax]] });
      info.push(["linear calibration", "A = " + L.a.toFixed(4) + " + " + L.b.toFixed(5) + " c (s<sub>r</sub> " + L.s.toFixed(4) + ")"]);
      res = cal.pts.map(function (p) { return [p[0], p[1] - (L.a + L.b * p[0])]; });
    }
    if (cal.quad) { var qd = []; for (var i = 0; i <= 50; i++) { var x = xmax * i / 50; qd.push([x, cal.quad[0] + cal.quad[1] * x + cal.quad[2] * x * x]); } ser.push({ type: "line", color: "s3", label: "quadratic", data: qd }); }
    aPlot.draw(ser, { xMin: 0, yMin: 0 });
    aRes.draw([{ type: "points", color: "s2", data: res }, { type: "hline", y: 0, color: "muted" }], {});
    if (cal.lin || cal.quad) {
      var latest = function (sol, la) { return aReads.filter(function (r) { return r.sol === sol && cal.same(r) && (la === undefined || (r.k.la !== "none") === la); }).pop(); };
      var w = latest("water", true), w0 = latest("water", false), sp = latest("spike", true) || latest("spike");
      if (w) {
        var cw = aConc(cal, w.A), uw = cal.lin && !cal.quad ? sx(cal.lin, cal.linx, w.A, 3) : NaN;
        info.push(["water 1 + 9 with La", "A = " + w.A.toFixed(4) + " → " + (isFinite(uw) ? Sim.fmtU(cw, uw, "mg/L") : cw.toFixed(2) + " mg/L") + " → " + (isFinite(uw) ? Sim.fmtU(10 * cw, 10 * uw, "mg/L") : (10 * cw).toFixed(1) + " mg/L") + " in the water (s)"]);
        if (w0) { var c0 = aConc(cal, w0.A); info.push(["water 1 + 9 without La", (10 * c0).toFixed(1) + " mg/L: " + (100 * (c0 / cw - 1)).toFixed(0) + " % (La result " + (100 * (cw / c0 - 1)).toFixed(0) + " % higher)"]); }
        if (sp) { var cs = aConc(cal, sp.A); info.push(["spike recovery (+2.0 mg/L)", (100 * (cs - cw) / 2.0).toFixed(0) + " %" + (cs > num("a-max") && !cal.quad ? " — the spiked solution is above the linear range" : ""), Math.abs((cs - cw) / 2.0 - 1) > 0.1 ? "miss" : "hit"]); }
      }
      ["phos", "salt"].forEach(function (s2) {
        var seen = {};
        aReads.filter(function (r) { return r.sol === s2 && cal.same(r); }).reverse().forEach(function (r) {
          var key = (r.k.la !== "none") + "|" + r.k.bg;
          if (seen[key]) return; seen[key] = 1;
          info.push([r.label + (r.k.la === "none" ? ", no La" : ", La") + (r.k.bg ? "" : ", no background correction"), aConc(cal, r.A).toFixed(2) + " mg/L (true 4.00 in the cell)"]);
        });
      });
    } else info.push(["calibration", "read at least two standards and a blank under the same conditions"]);
    // repeated standards: drift
    var groups = {};
    aReads.forEach(function (r) { if (r.sol === "std" && cal.same(r)) (groups[r.c] = groups[r.c] || []).push(r); });
    Object.keys(groups).forEach(function (c) { var g = groups[c]; if (g.length >= 2 && +c > 0) info.push(["check standard " + c + " mg/L", "drift " + (100 * (g[g.length - 1].A / g[0].A - 1)).toFixed(1) + " % from t = " + g[0].t.toFixed(1) + " to " + g[g.length - 1].t.toFixed(1) + " min (limit ± 5 %)", Math.abs(g[g.length - 1].A / g[0].A - 1) > 0.05 ? "miss" : ""]); });
    if (aProfile) info.push(["burner-height profile (" + aProfile.label + ")", "best at " + aProfile.best + " mm; falls to " + aProfile.drop + " % 3 mm either side"]);
    var na = aReads.filter(function (r) { return r.k.el === "Na" && r.sol === "std" && r.k.flame === "n2o"; });
    var naK = na.filter(function (r) { return r.k.k; }).pop(), na0 = na.filter(function (r) { return !r.k.k; }).pop();
    if (naK && na0 && naK.c === na0.c) info.push(["Na in the hot flame", "with K / without K = " + (naK.A / na0.A).toFixed(2)]);
    if (aClock < 10) info.push(["lamp", "warming up: readings drift for about 10–15 min", "miss"]);
    kvFill($id("a-info"), info);
    var cols = { blank: "muted", std: "s1", water: "s3", spike: "s4", phos: "s5", salt: "s6" }, dser = [];
    Object.keys(cols).forEach(function (s3) { var d = aReads.filter(function (r) { return r.sol === s3; }).map(function (r) { return [r.t, r.A]; }); if (d.length) dser.push({ type: "points", color: cols[s3], label: s3, data: d }); });
    aDrift.draw(dser.length ? dser : [{ type: "hline", y: 0, color: "muted" }], { xMin: 0 });
    fillBody(Sim.$("#a-table tbody"), aReads.slice().reverse().map(function (r) {
      return [r.t.toFixed(1), r.label, r.k.el + ", " + (r.k.flame === "air" ? "air–C₂H₂" : "N₂O–C₂H₂") + ", " + r.k.h + " mm, La " + r.k.la + (r.k.k ? ", K" : "") + (r.k.bg ? "" : ", no BC"), r.A.toFixed(4), r.sd.toFixed(4)];
    }));
    csvFns.aas = function () {
      var rows = [];
      aReads.forEach(function (r) { r.reads.forEach(function (A) { rows.push([+r.t.toFixed(1), r.sol, r.sol === "std" ? r.c : "", r.k.el, r.k.flame, r.k.h, r.k.la, r.k.k ? 1 : 0, r.k.bg ? 1 : 0, +A.toFixed(4)]); }); });
      return { header: ["t_min", "type", "c_mg_per_L", "element", "flame", "height_mm", "lanthanum", "potassium", "background_correction", "absorbance"], rows: rows, filename: "aas_readings.csv" };
    };
  }
  $id("a-wait").addEventListener("click", function () { aClock += 1; $id("a-clock").textContent = aClock.toFixed(1); aDraw(); });
  $id("a-wait10").addEventListener("click", function () { aClock += 10; $id("a-clock").textContent = aClock.toFixed(1); aDraw(); });
  $id("a-zero").addEventListener("click", function () {
    var k = aCond(); aRef = lampI(aClock) * Math.pow(10, -aTrue("blank", 0, k)); aClock += 0.5; $id("a-clock").textContent = aClock.toFixed(1);
    aDraw();
  });
  $id("a-read").addEventListener("click", function () { aRead($id("a-sol").value, Math.max(0, num("a-c"))); aDraw(); });
  $id("a-series").addEventListener("click", function () {
    var el = $id("a-el").value;
    aRead("blank", 0);
    (el === "Ca" ? [1, 2, 4, 6, 8, 10] : [0.1, 0.2, 0.5, 1.0, 2.0]).forEach(function (c) { aRead("std", c); });
    aDraw();
  });
  $id("a-hscan").addEventListener("click", function () {
    var k = aCond(), c = k.el === "Ca" ? 4 : 0.5, best = 0, bh = 0, prof = [];
    for (var h = 1; h <= 16; h += 0.5) { k.h = h; var A = aTrue("std", c, k); prof.push([h, A]); if (A > best) { best = A; bh = h; } }
    k.h = bh + 3; var A3 = aTrue("std", c, k);
    aProfile = { label: k.el + " " + c + " mg/L, " + (k.flame === "air" ? "air" : "N₂O"), best: bh, drop: Math.round(100 * A3 / best), data: prof };
    aClock += 3; $id("a-clock").textContent = aClock.toFixed(1);
    aDraw();
  });
  $id("a-clear").addEventListener("click", function () { aReads = []; aProfile = null; aDraw(); });
  $id("a-rerun").addEventListener("click", function () { seed = Sim.newSeed(seed); showSeed(); aReads = []; aProfile = null; aDraw(); });
  ["a-h"].forEach(function (id) { $id(id).addEventListener("input", function () { $id("a-h-out").textContent = num("a-h").toFixed(1) + " mm"; }); });
  ["a-el", "a-sol", "a-max", "a-quad", "a-flame", "a-la", "a-k", "a-bg"].forEach(function (id) { $id(id).addEventListener("change", aDraw); });

  /* ======================= tabs and export ======================= */
  Sim.exportCSV($id("x-data"), "spectrometer.csv", function () { var f = csvFns[tabName]; return f ? f() : null; });
  var DRAW = { uv: uDraw, mix: mDraw, eq: eDraw, fl: fDraw, aas: aDraw };
  var tabs = Sim.tabs($id("tabs"), function (name) { tabName = name; DRAW[name](); });
  tabs.select(tabName);
})();
