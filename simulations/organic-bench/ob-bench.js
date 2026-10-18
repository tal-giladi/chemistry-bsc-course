/* organic-bench, part 4: presets, tabs, the step-by-step synthesis bench and the product analysis
 * (yield, melting point, TLC, IR and 1H NMR described by key peaks). Uses Sim, OB, OB_TECH, OB_SYN.
 */
(function () {
  "use strict";
  var C = OB.C;
  var PRESETS = {
    techniques: {
      title: "Lab techniques", tab: "tech",
      what: "Six stations for the core techniques of an organic lab: reflux, extraction and drying (24.1), recrystallisation and distillation (24.2), TLC and melting point (24.3). Each station lets you make the decisions a student makes at the bench and shows what happens when one is wrong: bumping, solvent loss, emulsions, the wrong layer, a wet product, oiling out, a merged distillation, an overloaded plate, a lagging thermometer.",
      task: "Reflux: run once correctly, once with no stirrer and once too hot. Extraction: water wash, three NaHCO₃ washes, brine, drying agent until free-flowing, evaporate. Recrystallise 2.00 g of acetanilide three ways (minimum water and slow cooling; double the water; straight into ice) and once from a solvent that boils above 114 °C. Distil 50:50 cyclohexane–toluene simply and with a column. Run TLC at three eluents and melting points at 2 and 10 °C/min.",
      target: "Benzophenone recovered above 95 % and dry; recrystallisation close to 88 % with slow cooling, less with double solvent, a lower melting point after crash cooling, oiling out from xylenes; first fraction near 71 % cyclohexane (simple) and above 90 % (column); 20 % ethyl acetate separates benzoin (Rf ≈ 0.34) from benzil (≈ 0.65); pure benzoic acid within 1 °C of 122 °C at 2 °C/min, several degrees high at 10 °C/min."
    },
    aspirin: {
      title: "Aspirin synthesis", tab: "synth", syn: "aspirin",
      what: "Acetylate salicylic acid with acetic anhydride, quench, crystallise, filter, recrystallise and dry, deciding each step yourself. The bench tracks every gram: unreacted salicylic acid, acetic acid, water, by-products. Then check the product: mass and yield, melting range, the FeCl₃ test, TLC with a co-spot, and the IR and ¹H NMR key peaks.",
      task: "Write the amounts and hazards from the reagent cards. Run the synthesis once by the procedure table: record the crude mass, melting range and FeCl₃ result, then recrystallise, dry and record again. Make two deliberate mistakes in separate runs: wet salicylic acid, and skipping the drying. Run a TLC of crude, recrystallised product and salicylic acid.",
      target: "A careful run: 2.2–2.4 g crude, then 1.8–2.1 g (70–80 %) melting within 2 °C of 135 °C with a negative FeCl₃ test and no salicylic-acid spot. Wet salicylic acid gives a low yield; the undried product weighs more than 2.61 g."
    },
    sn2: {
      title: "SN2: 1-bromobutane from 1-butanol", tab: "synth", syn: "sn2",
      what: "Convert 1-butanol to 1-bromobutane with NaBr and sulfuric acid under reflux, distil the crude product out, wash it three times (the product layer switches from bottom to top and back), dry it and distil it.",
      task: "Run the synthesis as described; at each wash, choose the layer from the densities, not from where it was last time. Then run it again with vigorous heating and compare the yield, the 1-butene gas and the dibutyl ether.",
      target: "60–75 % of a liquid boiling near 101 °C with no O–H band in the IR; overheating lowers the yield and makes 1-butene and dibutyl ether."
    },
    grignard: {
      title: "Grignard: triphenylmethanol", tab: "synth", syn: "grignard",
      what: "Make phenylmagnesium bromide from bromobenzene and magnesium in dry ether, start it, add it to benzophenone, work up with acid and remove the biphenyl side product.",
      task: "Run with oven-dried glassware; try to start the reaction first without iodine; add the bromobenzene slowly. Then run with air-dried glassware and fast addition. Compare yields, melting points and the biphenyl removed by the hexane wash.",
      target: "Dry, slow run: 60–80 % of white crystals melting near 160 °C. Wet, fast run: under 40 %, a lower melting point and more biphenyl."
    },
    aldol: {
      title: "Aldol: dibenzalacetone", tab: "synth", syn: "aldol",
      what: "Condense benzaldehyde with acetone in ethanolic NaOH. The ratio of the reagents decides which product you get.",
      task: "Run with the 2 : 1 ratio, then 1 : 1 and 3 : 1. Record the product mass, appearance and melting point each time.",
      target: "2 : 1 gives a yellow solid melting near 110 °C; 1 : 1 gives mainly benzalacetone (a low-melting solid); 3 : 1 gives an oily, almond-smelling product."
    },
    multistep: {
      title: "Multi-step synthesis with spectra at every step", tab: "synth", syn: "multistep",
      what: "Benzaldehyde → benzoin → benzil → benzilic acid, with a check after every step: TLC with a co-spot of the starting material, melting point, IR and ¹H NMR key peaks. You decide whether each intermediate passes.",
      task: "Plan for 1.00 g of benzilic acid at 70 % per step. Run step 1 and check it. In step 2 stop the first oxidation early on purpose (10 min), check it and quantify the leftover benzoin from the NMR integrals (5.95 ppm against 10 aromatic H); then fix it and check again. Run step 3. Record every mass and compute step and overall yields.",
      target: "Benzoin about 58 % (mp 134–136 °C), benzil about 84 % after recrystallisation (mp 94–95 °C, no O–H band, no 5.95 ppm signal), benzilic acid about 75 % (mp 149–151 °C); overall 30–45 %. A 10-minute oxidation leaves about 20 mol% benzoin."
    }
  };

  var preset = Sim.preset(PRESETS, "techniques");
  var seed0 = Sim.seedFromQuery(24);
  Sim.label();
  Sim.presetBox(Sim.$("#preset"), preset);
  function $(id) { return document.getElementById(id); }
  function tr(cells) { var row = Sim.el("tr"); cells.forEach(function (c) { row.appendChild(Sim.el("td", { html: String(c) })); }); return row; }
  function kv(el, pairs) { el.textContent = ""; pairs.forEach(function (p) { el.appendChild(Sim.el("span", { html: p[0] })); el.appendChild(Sim.el("span", { html: p[1] })); }); }

  var tech = OB_TECH(seed0);

  /* ======================= synthesis bench ======================= */
  var b = { seed: seed0, rng: Sim.rng(seed0), def: null, st: null, i: 0, log: [], runs: [], lastAnalysis: null, done: [] };
  var irPlot = Sim.plot($("s-ir"), { xLabel: "wavenumber / cm⁻¹", yLabel: "transmittance / %", xReverse: true, legend: false });
  var nmrPlot = Sim.plot($("s-nmr"), { xLabel: "δ / ppm", yLabel: "intensity", xReverse: true, legend: false });

  function say(text, cls) {
    var d = Sim.el("div", { html: text }); if (cls) d.className = cls;
    $("s-log").appendChild(d); $("s-log").scrollTop = $("s-log").scrollHeight;
    b.log.push([b.i + 1, b.def.steps[Math.min(b.i, b.def.steps.length - 1)].title, text.replace(/<[^>]+>/g, "")]);
  }

  function start(key) {
    b.def = OB_SYN[key]; b.st = { sp: {}, water: 0 }; b.def.init(b.st); b.i = 0; b.log = []; b.done = [];
    b.rng = Sim.rng(b.seed);
    $("s-intro").innerHTML = b.def.intro;
    $("s-eluent").value = String(b.def.eluent);
    $("s-viz").value = b.def.liquid ? "iodine" : "uv";
    var cards = $("s-cards"); cards.textContent = "";
    b.def.cards.forEach(function (c) { cards.appendChild(tr(["<strong>" + c[0] + "</strong>", c[1], c[2]])); });
    $("s-log").textContent = "";
    $("s-analysis").hidden = true;
    $("s-seed").textContent = b.seed;
    renderSteps(); renderCard(); renderState();
  }

  function renderSteps() {
    var ol = $("s-steps"); ol.textContent = "";
    b.def.steps.forEach(function (s, i) {
      var li = Sim.el("li", { text: s.title });
      if (i < b.i || b.done.indexOf(i) >= 0 && i !== b.i) li.className = "done";
      if (i === b.i) { li.className = "current"; li.setAttribute("aria-current", "step"); }
      ol.appendChild(li);
    });
  }

  function renderCard() {
    var box = $("s-controls"); box.textContent = "";
    if (b.i >= b.def.steps.length) {
      $("s-step-title").textContent = "Finished";
      $("s-step-why").textContent = "The run is complete. Check the product, save the run to the table, or start a new run with different choices.";
      $("s-go").disabled = true;
      return;
    }
    var s = b.def.steps[b.i];
    $("s-step-title").textContent = "Step " + (b.i + 1) + " of " + b.def.steps.length + ": " + s.title;
    $("s-step-why").textContent = s.why;
    $("s-go").disabled = false;
    s.controls.forEach(function (c) {
      var id = "sc-" + c.id;
      if (c.type === "select") {
        var se = Sim.el("select", { id: id });
        c.options.forEach(function (o) { se.appendChild(Sim.el("option", { value: o[0], text: o[1] })); });
        se.value = c.def;
        box.appendChild(Sim.el("div", { class: "field" }, Sim.el("label", { for: id, text: c.label }), se));
      } else if (c.type === "number") {
        box.appendChild(Sim.el("div", { class: "field" }, Sim.el("label", { for: id, text: c.label }), Sim.el("input", { type: "number", id: id, min: c.min, max: c.max, step: c.step, value: c.def })));
      } else if (c.type === "check") {
        var inp = Sim.el("input", { type: "checkbox", id: id }); inp.checked = !!c.def;
        box.appendChild(Sim.el("div", { class: "row" }, Sim.el("label", { for: id }, inp, " " + c.label)));
      }
    });
  }

  function choices() {
    var s = b.def.steps[b.i], ch = {}, txt = [];
    s.controls.forEach(function (c) {
      var el = $("sc-" + c.id);
      if (c.type === "check") { ch[c.id] = el.checked; txt.push(c.label + ": " + (el.checked ? "yes" : "no")); }
      else { ch[c.id] = el.value; txt.push(c.type === "select" ? el.selectedOptions[0].text : c.label + " " + el.value); }
    });
    return { ch: ch, txt: txt.join("; ") };
  }

  $("s-go").addEventListener("click", function () {
    if (b.i >= b.def.steps.length) return;
    var s = b.def.steps[b.i], c = choices();
    say("<strong>Step " + (b.i + 1) + ":</strong> " + c.txt);
    var res = s.run(b.st, c.ch, b.rng, say) || {};
    if (b.done.indexOf(b.i) < 0) b.done.push(b.i);
    if (res.goto !== undefined) b.i = res.goto;
    else if (!res.stay) b.i++;
    if (b.i >= b.def.steps.length) say("<strong>Run complete.</strong> Check the product and save the run.", "good");
    renderSteps(); renderCard(); renderState();
    if (!$("s-analysis").hidden && b.st.isolated) analyse(true);
  });
  $("s-restart").addEventListener("click", function () { b.seed = Sim.newSeed(b.seed); start($("s-pick").value); });
  $("s-pick").addEventListener("change", function () { start($("s-pick").value); });

  function composition() {
    var out = {};
    Object.keys(b.st.sp).forEach(function (k) { if (C[k] && b.st.sp[k] > 1e-6) out[k] = b.st.sp[k]; });
    return out;
  }
  function stageProduct() {
    if (b.def.multi) { var si = b.def.stageInfo[b.st.stage || 1]; return { product: si[0], sm: si[1] }; }
    return { product: b.def.product, sm: b.def.sm };
  }
  function renderState() {
    var comp = composition(), pairs = [];
    Object.keys(comp).forEach(function (k) { pairs.push([k, OB_SYN.g(k, comp[k]).toFixed(3) + " g (" + comp[k].toFixed(2) + " mmol)"]); });
    if (b.st.water > 0.0005) pairs.push(["water", b.st.water.toFixed(3) + " g"]);
    if (!pairs.length) pairs.push(["flask", "empty: start with step 1"]);
    if (b.def.multi && b.st.inter) Object.keys(b.st.inter).forEach(function (k) { pairs.push(["stored intermediate " + k, b.st.inter[k].mass.toFixed(2) + " g"]); });
    kv($("s-state"), pairs);
  }

  /* ---------- analysis of the current product ---------- */
  function analyse(quiet) {
    var st = b.st, comp = composition(), sp = stageProduct(), prod = sp.product;
    $("s-analysis").hidden = false;
    var names = Object.keys(comp), tot = 0, NH = {};
    names.forEach(function (k) { tot += comp[k]; NH[k] = (C[k].nmr || []).reduce(function (s, p) { return s + p[1]; }, 0); });
    var x = {}; names.forEach(function (k) { x[k] = comp[k] / Math.max(1e-12, tot); });
    var mass = OB_SYN.dryMass(st) + st.water;
    var theoG = st.theo ? OB_SYN.g(prod, st.theo) : NaN;
    var rate = parseFloat($("s-rate").value);
    var res = [];
    if (!st.isolated) res.push(["status", "nothing isolated yet: only a TLC of the reaction mixture is meaningful"]);
    res.push(["product expected", prod]);
    res.push(["mass obtained", mass.toFixed(2) + " g" + (st.water > 0.01 ? " (of which " + st.water.toFixed(2) + " g is water)" : "")]);
    if (isFinite(theoG)) res.push(["theoretical yield", theoG.toFixed(2) + " g" + (b.def.multi ? " (from " + (st.startG || 0).toFixed(2) + " g used in this step)" : "")]);
    var yld = 100 * mass / theoG;
    if (isFinite(yld)) res.push(["yield (by mass)", yld.toFixed(1) + " %"]);
    res.push(["purity (mol %, by NMR)", (100 * (x[prod] || 0)).toFixed(1) + " % " + prod]);
    var look = (b.def.look && b.def.look(st, x, comp)) || (st.look && prod === b.def.product ? st.look : null) || (C[prod] ? C[prod].look : "");
    if (st.water > 0.05 * mass) look += b.def.liquid ? ", cloudy (water)" : ", damp and clumpy";
    if (st.lost) look = "—";
    res.push(["appearance", look]);
    var mpTxt = "—", mp = null;
    if (st.isolated && !b.def.liquid && tot > 0) {
      mp = OB.meltRange(comp, prod, st.water, rate, Sim.rng(b.seed + 11 + Math.round(mass * 1000)));
      mpTxt = mp.lo + "–" + mp.hi + " °C (lit. " + C[prod].mp + " °C" + (prod === "aspirin" ? ", rapid heating; decomposes" : "") + ")";
      res.push(["melting range (" + rate + " °C/min)", mpTxt]);
    }
    var tests = b.def.tests && OB_SYN.dryMass(st) > 0.005 ? b.def.tests(st, x) : [];
    tests.forEach(function (t) { res.push(t); });
    // verdict
    var v = [];
    if (yld > 100) v.push("over 100 %: wet or impure. Dry to constant mass, then judge again");
    if (mp && (mp.hi - mp.lo > 2 || mp.hi < C[prod].mp - 2)) v.push("melting low and/or broad: impure");
    if ((x[prod] || 0) < 0.9 && st.isolated) v.push("contains " + names.filter(function (k) { return k !== prod && x[k] > 0.02; }).map(function (k) { return k + " (" + (100 * x[k]).toFixed(0) + " mol%)"; }).join(", "));
    if (b.def.key === "aspirin" && (x["salicylic acid"] || 0) > 0.003) v.push("phenol present (FeCl₃): recrystallise");
    var verdict = !st.isolated ? "—" : v.length ? v.join("; ") + "." : b.def.liquid ? "pure enough: boils over a narrow range at the literature boiling point, with the expected spectra." : "pure enough: sharp melting point close to the literature value and the expected spectra.";
    if (st.lost || OB_SYN.dryMass(st) < 0.005) verdict = "no product: it was discarded or never formed.";
    res.push(["verdict", verdict]);
    kv($("s-res"), res);

    // TLC
    var lanes = [{ label: "SM", comp: {} }, { label: "co", comp: {} }, { label: "product", comp: comp }];
    lanes[0].comp[sp.sm] = 1;
    lanes[1].comp[sp.sm] = 1; Object.keys(comp).forEach(function (k) { lanes[1].comp[k] = (lanes[1].comp[k] || 0) + x[k]; });
    if (b.def.key === "aspirin") lanes.splice(2, 0, { label: "aspirin ref.", comp: { aspirin: 1 } });
    var phi = parseFloat($("s-eluent").value), viz = $("s-viz").value;
    var t = OB.tlc($("s-tlc"), lanes, phi, viz, Sim.rng(b.seed + 5), {});
    var tb = $("s-tlc-table").querySelector("tbody"); tb.textContent = "";
    t.spots.forEach(function (s) { tb.appendChild(tr([s.lane, s.dist.toFixed(1), (s.dist / t.front).toFixed(2), s.streak ? "streaks" : ""])); });
    if (!t.spots.length) tb.appendChild(tr(["—", "no spots visible", viz === "uv" ? "try the iodine stain" : "", ""]));

    // IR key bands
    var bands = [];
    names.forEach(function (k) {
      var thr = k === prod ? 0 : 0.05;
      if (x[k] < thr || !C[k].ir) return;
      C[k].ir.forEach(function (bd) { bands.push({ band: bd[0], strength: bd[1], label: bd[2] + (k === prod ? "" : " — " + k), w: Math.min(1, x[k] * 1.1), who: k }); });
    });
    if (st.water / Math.max(1e-9, mass) > 0.05) C.water.ir.forEach(function (bd) { bands.push({ band: bd[0], strength: bd[1], label: bd[2] + " (wet sample)", w: 0.8, who: "water" }); });
    OB.irSketch(irPlot, bands);
    var ib = $("s-ir-table").querySelector("tbody"); ib.textContent = "";
    bands.forEach(function (bd) { ib.appendChild(tr([bd.band, bd.strength + (bd.w < 0.5 ? " (weak: minor component)" : ""), bd.label])); });

    // NMR key peaks with integrals: species i gives nH x_i / X, X scaled so the product's molecule integrates to its own H count
    var X = 0; names.forEach(function (k) { X += x[k] * NH[k]; });
    var norm = NH[prod] ? X / NH[prod] : 1;
    if ((x[prod] || 0) < 0.3) { var big = names.reduce(function (a, k) { return !a || x[k] > x[a] ? k : a; }, null); norm = big && NH[big] ? X / NH[big] : 1; }
    var peaks = [];
    names.forEach(function (k) {
      if (x[k] < 0.02 || !C[k].nmr) return;
      C[k].nmr.forEach(function (p) { peaks.push({ d: p[0], I: p[1] * x[k] / Math.max(1e-9, norm), mult: p[2], J: p[3], label: p[4] + (k === prod ? "" : " — " + k) }); });
    });
    if (st.water / Math.max(1e-9, mass) > 0.02) peaks.push({ d: 1.56, I: Math.min(4, 30 * st.water / mass), mult: "s", J: 0, label: "water (wet sample)" });
    peaks.sort(function (p, q) { return q.d - p.d; });
    OB.nmrSketch(nmrPlot, peaks, 400);
    var nb = $("s-nmr-table").querySelector("tbody"); nb.textContent = "";
    peaks.forEach(function (p) { nb.appendChild(tr([p.d.toFixed(2), p.mult, p.J ? p.J.toFixed(1) : "—", p.I.toFixed(2), p.label])); });
    $("s-nmr-solvent").textContent = "CDCl₃ (DMSO-d₆ for the acids), 400 MHz. Integrals are scaled so the product's molecule counts its own protons; a minor component appears with a fractional integral.";

    // overall yield for the multi-step sequence
    if (b.def.multi) {
      var sy = st.stageYield || {}, ks = Object.keys(sy), ov = ks.length ? ks.reduce(function (a, k) { return a * sy[k]; }, 1) : NaN;
      $("s-overall").textContent = ks.length ? "Step yields (pure product, by moles): " + ks.map(function (k) { return "step " + k + " " + (100 * sy[k]).toFixed(1) + " %"; }).join(", ") + (ks.length > 1 ? "; overall " + (100 * ov).toFixed(1) + " %." : ".") : "";
    } else $("s-overall").textContent = "";

    b.lastAnalysis = { stage: b.def.multi ? "step " + (st.stage || 1) + " (" + prod + ")" : (b.i >= b.def.steps.length ? "final" : "after step " + b.i), mass: mass, theo: theoG, yld: yld, mp: b.def.liquid ? (tests[0] ? tests[0][1] : "") : mpTxt, tests: tests.map(function (t2) { return t2[0] + ": " + t2[1]; }).join("; "), verdict: verdict };
    if (!quiet) say("Checked: " + mass.toFixed(2) + " g, " + (isFinite(yld) ? yld.toFixed(1) + " %, " : "") + (b.def.liquid ? "" : "mp " + mpTxt + ", ") + verdict);
  }
  $("s-check").addEventListener("click", function () { analyse(false); });
  ["s-rate", "s-eluent", "s-viz"].forEach(function (id) { $(id).addEventListener("change", function () { if (!$("s-analysis").hidden) analyse(true); }); });
  $("s-save").addEventListener("click", function () {
    if (!b.lastAnalysis) analyse(true);
    var a = b.lastAnalysis, choicesTxt = b.log.filter(function (l) { return /^Step \d+:/.test(l[2]); }).map(function (l) { return l[2].replace(/^Step \d+:\s*/, ""); }).join(" | ");
    b.runs.push({ syn: b.def.title, stage: a.stage, mass: a.mass, theo: a.theo, yld: a.yld, mp: a.mp, tests: a.tests, verdict: a.verdict, choices: choicesTxt });
    var tb = $("s-runs").querySelector("tbody");
    tb.appendChild(tr([b.runs.length, b.def.key, a.stage, a.mass.toFixed(2), isFinite(a.yld) ? a.yld.toFixed(1) : "—", a.mp, a.tests || "—", a.verdict]));
  });
  Sim.exportCSV($("s-runs-csv"), "organic_bench_runs.csv", function () {
    return { header: ["run", "synthesis", "stage", "mass_g", "theoretical_g", "yield_pct", "mp_or_bp", "tests", "verdict", "choices"],
      rows: b.runs.map(function (r, i) { return [i + 1, r.syn, r.stage, r.mass.toFixed(3), isFinite(r.theo) ? r.theo.toFixed(3) : "", isFinite(r.yld) ? r.yld.toFixed(1) : "", r.mp, r.tests, r.verdict, r.choices]; }) };
  });
  Sim.exportCSV($("s-log-csv"), "organic_bench_log.csv", function () {
    return { header: ["step", "title", "entry"], rows: b.log };
  });

  /* ======================= tabs and start ======================= */
  var tabs = Sim.tabs($("tabs"), function (name) { if (name === "tech") tech.redraw(); else if (!$("s-analysis").hidden) analyse(true); });
  var ttabs = Sim.tabs($("tech-tabs"), function () { tech.redraw(); });
  ttabs.select("t-reflux");
  if (preset.syn) $("s-pick").value = preset.syn;
  start($("s-pick").value);
  tabs.select(preset.tab || "tech");
  tech.tlcRun();
})();
