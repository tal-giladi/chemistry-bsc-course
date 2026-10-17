/* gravimetry simulation: chloride as AgCl (precipitation gravimetry), copper by
 * electrodeposition (electrogravimetry), a coulometric titration of vitamin C with
 * electrogenerated iodine, and baking soda heated to constant mass (volatilisation).
 * Uses ../common/sim.js (global Sim).
 *
 * Data:
 *  - Ksp AgCl 1.8e-10 at 25 °C (Harvey, Analytical Chemistry 2.1, App. 16.10); M(AgCl) 143.32,
 *    M(Cl) 35.453 g/mol; gravimetric factor 0.2474 (Lesson 10.4). Example salt: 59.48 % Cl
 *    (the worked example of Lesson 09.6).
 *  - E°(Cu2+/Cu) = 0.339 V (Harvey App. 16.13); 99.99 % deposition from 1e-4 M needs the cathode
 *    below about +0.10 V vs SHE (Harvey 11.3, Lesson 10.4). M(Cu) = 63.546 g/mol.
 *  - F = 96485.33212 C/mol (CODATA 2022, via Sim.C.F). Ascorbic acid 176.12 g/mol, 2 e- per molecule.
 *  - 2NaHCO3 -> Na2CO3 + H2O + CO2: mass loss 62.02/168.01 = 36.92 % (Lesson 10.4).
 * Model sizes that are rules of thumb, not measured constants (illustrative): particles passing
 * the filter, peptisation per wash, co-precipitation, water left after drying, water taken up
 * while cooling (0.2 mg for AgCl on the bench; 0.015 g for 10 g of warm Na2CO3, as in the Lesson 10.4
 * example), the warm-crucible buoyancy error, the hydrogen Tafel current (1 mA at −0.30 V vs SHE,
 * 120 mV/decade) and the fall of iodine-generation efficiency at high current.
 */
(function () {
  "use strict";
  var F = Sim.C.F, KSP = 1.8e-10, M_AGCL = 143.32, M_CL = 35.453, M_CU = 63.546, M_ASC = 176.12;
  var GF = M_CL / M_AGCL, W_CL = 0.5948, CU_STATED = 0.1581, ASC_STATED = 0.0500e-3;
  var NERNST = Sim.C.R * 298.15 * Math.LN10 / F;

  var PRESETS = {
    precipitate: {
      title: "Chloride as silver chloride", tab: "precipitate",
      what: "Chloride is precipitated with silver nitrate as AgCl, filtered through a weighed sintered-glass crucible, washed, dried to constant mass and weighed; the gravimetric factor 35.453/143.32 = 0.2474 turns the AgCl into chloride. Every bench choice moves the result a little: crystal size (how fast and how hot you precipitate, and digestion), the wash liquid, and how you dry and cool.",
      task: "Analyse the 0.2500 g sample twice: once fast and cold without digestion, once slowly from hot solution with digestion, and compare the filtering losses. Then wash once with water and once with dilute HNO₃; dry once to constant mass and once for a single fixed hour. Note which choice moves the result most.",
      target: "A result within 0.3 % of the stated 59.48 % Cl (relative), with two final weighings that agree within 0.3 mg."
    },
    electrogravimetry: {
      title: "Copper by electrodeposition", tab: "electrogravimetry",
      what: "Cu²⁺ + 2e⁻ → Cu(s) on a weighed platinum gauze cathode. The charge passed is Q = ∫I dt, and the copper it could deposit is Q/(2F) × 63.546 g/mol. The current efficiency is the copper you weigh divided by that: below 100 % when some charge reduces H⁺ to hydrogen instead.",
      task: "Plate the 0.1581 g of copper at two cathode potentials, +0.10 V and −0.40 V vs SHE, and compare the current efficiency and the mass. Try +0.30 V too and run the completeness test. Then try a constant current of 0.50 A.",
      target: "Current efficiency above 99 % at the better potential, and copper found within 0.2 % of 0.1581 g."
    },
    coulometry: {
      title: "Coulometric titration", tab: "coulometry",
      what: "Instead of adding a standard solution from a burette, the cell makes its own titrant: a constant current oxidises iodide to iodine at a platinum anode, and the iodine oxidises the vitamin C. The charge to the end point, Q = I t, counts the moles: n = Q/(2F). No standard solution is needed, only an accurate current and clock.",
      task: "Titrate the vitamin C sample at 10 mA to the first lasting blue (or the jump in indicator current); use short pulses near the end. Run the reagent blank and subtract it. Compare the moles from Q = It with the stated 0.0500 mmol. Then repeat at 100 mA.",
      target: "Moles within 0.5 % of the stated amount at 10 mA after the blank; a visibly larger error at 100 mA, where some charge is lost to a side reaction."
    },
    oven: {
      title: "Baking soda to constant mass", tab: "oven",
      what: "Volatilisation gravimetry: heating turns 2NaHCO₃ into Na₂CO₃ + H₂O + CO₂, a theoretical loss of 36.92 %. Constant mass, two weighings in a row that agree, proves the reaction has finished; how you cool the tray before each weighing decides whether the warm carbonate picks up water from the air.",
      task: "Heat about 10 g in 15-minute steps at 200 °C until two weighings agree within 0.02 g. Do it once cooling on a board and once in a closed jar; also try weighing warm.",
      target: "Mass loss between 36.0 and 37.0 % (an apparent purity near 99–100 %)."
    }
  };

  var preset = Sim.preset(PRESETS, "precipitate");
  var seed = Sim.seedFromQuery(4);
  var tabName = preset.tab;
  var runs = [], lastCSV = null;

  Sim.label();
  Sim.presetBox(Sim.$("#preset"), preset);
  function showSeed() { Sim.$$(".seed").forEach(function (e) { e.textContent = String(seed); }); }
  showSeed();

  function v(id) { return parseFloat(Sim.$("#" + id).value); }
  function s(id) { return Sim.$("#" + id).value; }
  function chk(id) { return !!Sim.$("#" + id).checked; }
  function kvFill(box, rows) {
    box.textContent = "";
    rows.forEach(function (r) { box.appendChild(Sim.el("div", { text: r[0] })); box.appendChild(Sim.el("div", { text: r[1], class: r[2] || null })); });
  }
  function pct(x, ref) { return (x - ref) / ref * 100; }
  function sgn(x, d) { return (x >= 0 ? "+" : "−") + Math.abs(x).toFixed(d === undefined ? 2 : d); }
  function addRun(exp, choices, result, stated, err) {
    runs.push({ id: runs.length + 1, exp: exp, choices: choices, result: result, stated: stated, err: err });
    var tb = Sim.$("#runs tbody");
    tb.textContent = "";
    runs.forEach(function (r) {
      tb.appendChild(Sim.el("tr", {}, Sim.el("td", { text: String(r.id) }), Sim.el("td", { text: r.exp }), Sim.el("td", { text: r.choices }),
        Sim.el("td", { text: r.result }), Sim.el("td", { text: r.stated }), Sim.el("td", { text: isFinite(r.err) ? sgn(r.err) + " %" : "—" })));
    });
  }
  function setupCanvas(cv) {
    var dpr = window.devicePixelRatio || 1, w = cv.clientWidth || 300, h = cv.clientHeight || 180;
    if (cv.width !== Math.round(w * dpr) || cv.height !== Math.round(h * dpr)) { cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr); }
    var ctx = cv.getContext("2d");
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    return { ctx: ctx, w: w, h: h };
  }

  /* ======================= PRECIPITATION GRAVIMETRY ======================= */
  var pg = null, pgCount = 0;

  function pgStart() {
    pgCount++;
    var r = Sim.rng(seed + 31 * pgCount);
    var m = v("p-mass");
    if (!(m > 0.05 && m < 1)) { m = 0.2500; Sim.$("#p-mass").value = "0.2500"; }
    var slow = s("p-how") === "slow", dig = chk("p-digest"), ex = parseFloat(s("p-excess")), dark = chk("p-dark");
    var coarse = s("p-filter") === "coarse", water = s("p-wash") === "water", nw = parseInt(s("p-nwash"), 10);
    var mAgCl = m * W_CL / M_CL * M_AGCL;                       // g, if nothing were lost or gained
    var Vml = slow ? 0.150 : 0.025, nCl = m * W_CL / M_CL;
    var cex = ex / 100 * nCl / Vml;
    var sML = (-cex + Math.sqrt(cex * cex + 4 * KSP)) / 2;
    var eff = {};
    eff.liquor = -sML * Vml * M_AGCL;                            // dissolved in the mother liquor
    eff.washSol = -nw * 0.010 * 0.5 * Math.sqrt(KSP) * M_AGCL;  // each wash half-saturates
    var fPass = (slow ? 0.0004 : 0.004) * (dig ? 0.3 : 1) * (coarse ? 4 : 1) * r.uniform(0.7, 1.3);
    eff.filter = -fPass * mAgCl;
    eff.peptise = water ? -nw * (slow ? 0.0006 : 0.0020) * (dig ? 0.5 : 1) * r.uniform(0.7, 1.3) * mAgCl : 0;
    var co = (slow ? 0.0006 : 0.003) * (dig ? 0.4 : 1) + (ex >= 50 ? (water ? 0.0015 : 0.0005) : 0);
    eff.coprec = co * r.uniform(0.8, 1.2) * mAgCl;
    eff.light = dark ? 0 : -r.uniform(0.0008, 0.0016) * mAgCl;
    var solid = mAgCl + eff.liquor + eff.washSol + eff.filter + eff.peptise + eff.coprec + eff.light;
    pg = {
      r: r, m: m, mAgCl: mAgCl, eff: eff, solid: solid, tare: 21 + r.uniform(0.1, 0.9),
      water: mAgCl * (slow ? 0.02 : 0.04), fixedWater: mAgCl * (slow ? 0.0001 : 0.0006) * (dig ? 0.5 : 1),
      dryFrac: slow ? 0.08 : 0.15, weighings: [], cycles: 0, accepted: false,
      choices: (slow ? "slow, hot" : "fast, cold") + (dig ? ", digested" : "") + ", " + ex + " % excess, " + (water ? "water" : "HNO₃") + " × " + nw + (coarse ? ", coarse filter" : "") + (dark ? "" : ", in light")
    };
    pg.tareRead = Math.round((pg.tare + r.normal(0, 0.00005)) * 1e4) / 1e4;
    Sim.$("#p-readout").textContent = pg.tareRead.toFixed(4) + " g";
    kvFill(Sim.$("#p-info"), [["sample", m.toFixed(4) + " g"], ["empty crucible (constant mass)", pg.tareRead.toFixed(4) + " g"],
      ["precipitate", slow ? "coarse white curds that settle quickly" : "fine, milky suspension; slow to settle"],
      ["filtrate", (fPass > 0.002 || eff.peptise < -0.0015 * mAgCl) ? "slightly cloudy" : "clear"]].concat(dark ? [] : [["colour", "the precipitate turns violet-grey in the light"]]));
    Sim.$("#p-weighings tbody").textContent = "";
    kvFill(Sim.$("#p-result"), [["status", "Dry and weigh until two weighings agree."]]);
    Sim.$("#p-budget tbody").textContent = "";
  }

  function pgDry() {
    if (!pg) pgStart();
    if (pg.accepted) return;
    var r = pg.r, cool = s("p-cool");
    pg.cycles++;
    pg.water *= pg.dryFrac * r.uniform(0.8, 1.2);
    var coolEff = cool === "desic" ? 0.00002 : cool === "bench" ? r.normal(0.00020, 0.00005) : -r.normal(0.0005, 0.0002);
    var mass = pg.tare + pg.solid + pg.water + pg.fixedWater + coolEff + r.normal(0, 0.00005);
    var read = Math.round(mass * 1e4) / 1e4;
    var prev = pg.weighings.length ? pg.weighings[pg.weighings.length - 1].read : null;
    pg.weighings.push({ cycle: pg.cycles, read: read, cool: cool, coolEff: coolEff });
    Sim.$("#p-readout").textContent = read.toFixed(4) + " g";
    var tb = Sim.$("#p-weighings tbody");
    tb.appendChild(Sim.el("tr", {}, Sim.el("td", { text: pg.cycles + " (" + { desic: "desiccator", bench: "bench", warm: "warm" }[cool] + ")" }), Sim.el("td", { text: read.toFixed(4) }),
      Sim.el("td", { text: prev === null ? "—" : sgn((read - prev) * 1000, 1), class: prev !== null && Math.abs(read - prev) <= 0.00030 ? "hit" : null })));
    lastCSV = function () { return { header: ["weighing", "cooling", "crucible_plus_AgCl_g"], rows: pg.weighings.map(function (w) { return [w.cycle, w.cool, w.read]; }), filename: "gravimetry_AgCl_weighings.csv" }; };
  }

  function pgAccept() {
    if (!pg || !pg.weighings.length || pg.accepted) { kvFill(Sim.$("#p-result"), [["status", "Weigh the dried precipitate first."]]); return; }
    pg.accepted = true;
    var w = pg.weighings, last = w[w.length - 1], mppt = last.read - pg.tareRead;
    var constant = w.length >= 2 && Math.abs(last.read - w[w.length - 2].read) <= 0.00030;
    var cl = mppt * GF / pg.m * 100, err = pct(cl, W_CL * 100);
    var uM = 0.0001 / Math.sqrt(6), ucl = cl * Math.sqrt(Math.pow(uM / mppt, 2) + Math.pow(uM / pg.m, 2));
    kvFill(Sim.$("#p-result"), [
      ["AgCl", (mppt * 1000).toFixed(1) + " mg"],
      ["Cl in the sample", Sim.fmtU(cl, ucl, "%") + " (balance only)"],
      ["stated", (W_CL * 100).toFixed(2) + " %"],
      ["error", sgn(err) + " % relative", Math.abs(err) <= 0.3 ? "hit" : "miss"],
      ["constant mass", constant ? "yes: last two weighings agree within 0.3 mg" : "no: the last two weighings differ, or only one weighing", constant ? "hit" : "miss"]
    ]);
    var e = pg.eff, tb = Sim.$("#p-budget tbody");
    tb.textContent = "";
    var rows = [["dissolved in the mother liquor", e.liquor], ["dissolved by the washes", e.washSol], ["fine particles through the filter", e.filter],
      ["peptised by water washes", e.peptise], ["co-precipitated impurities", e.coprec], ["chlorine lost in light", e.light],
      ["water still in the solid", pg.water + pg.fixedWater], ["cooling (" + { desic: "desiccator", bench: "moist air", warm: "weighed warm" }[last.cool] + ")", last.coolEff]];
    var tot = 0;
    rows.forEach(function (q) {
      tot += q[1];
      tb.appendChild(Sim.el("tr", {}, Sim.el("td", { text: q[0] }), Sim.el("td", { text: sgn(q[1] * 1000, 2) }), Sim.el("td", { text: sgn(q[1] / pg.mAgCl * 100, 3) + " %" })));
    });
    tb.appendChild(Sim.el("tr", {}, Sim.el("td", { text: "total (the rest is balance noise)" }), Sim.el("td", { text: sgn(tot * 1000, 2) }), Sim.el("td", { text: sgn(tot / pg.mAgCl * 100, 3) + " %" })));
    addRun("AgCl gravimetry", pg.choices + "; " + w.length + " weighing" + (w.length > 1 ? "s" : ""), cl.toFixed(2) + " % Cl", (W_CL * 100).toFixed(2) + " %", err);
  }

  Sim.$("#p-start").addEventListener("click", pgStart);
  Sim.$("#p-dry").addEventListener("click", pgDry);
  Sim.$("#p-accept").addEventListener("click", pgAccept);
  Sim.$("#p-rerun").addEventListener("click", function () { seed = Sim.newSeed(seed); showSeed(); pgStart(); });

  /* ======================= ELECTROGRAVIMETRY ======================= */
  var eg = null, egCount = 0;
  var ePlot = Sim.plot(Sim.$("#e-plot"), { xLabel: "time / min", yLabel: "current / mA", logY: true });

  function egModeUI() { var pot = s("e-mode") === "pot"; Sim.$("#e-pot-f").hidden = !pot; Sim.$("#e-cur-f").hidden = pot; }

  // integrate the cell from state st for `secs` seconds; returns the added record
  function egIntegrate(st, secs) {
    var dt = 2, V = 0.100, rec = [];
    for (var t = 0; t < secs; t += dt) {
      var iCu, iH, iBg = 5e-5;
      if (st.pot) {
        var ceq = Math.pow(10, (st.E - 0.339) / (NERNST / 2));
        iCu = st.C > ceq ? Math.min(2.0, 2 * F * V * st.k * (st.C - ceq)) : 0;
        iH = 1e-3 * Math.pow(10, -(st.E + 0.30) / 0.12);
      } else {
        iCu = Math.min(st.I - iBg, 2 * F * V * st.k * st.C);
        iH = Math.max(0, st.I - iBg - iCu);
      }
      var dn = iCu * dt / (2 * F);
      st.C = Math.max(0, st.C - dn / V);
      st.dep += dn * M_CU;
      st.Q += (iCu + iH + iBg) * dt;
      st.QH += iH * dt;
      st.t += dt;
      if (st.t % 30 === 0) rec.push([st.t / 60, 1000 * (iCu + iH + iBg), 1000 * iCu]);
    }
    return rec;
  }

  function egRun() {
    egCount++;
    var r = Sim.rng(seed + 53 * egCount), pot = s("e-mode") === "pot";
    var st = {
      pot: pot, E: parseFloat(s("e-pot")), I: parseFloat(s("e-cur")), k: (chk("e-stir") ? 1 / 150 : 1 / 1500) * r.uniform(0.9, 1.1),
      C: CU_STATED / M_CU / 0.100, dep: 0, Q: 0, QH: 0, t: 0, r: r, tare: 12 + r.uniform(0.1, 0.9), checks: 0
    };
    st.rec = egIntegrate(st, 60 * parseFloat(s("e-time")));
    st.lift = chk("e-lift");
    eg = st;
    egFinish(true);
  }

  function egFinish(log) {
    var st = eg, r = st.r;
    var spongy = st.pot ? st.E <= -0.30 : st.QH > 0.02 * st.Q;
    var flake = spongy ? r.uniform(0.002, 0.006) * st.dep : 0;
    var redissolve = st.lift ? 0 : r.uniform(0.0003, 0.0010);
    var gain = st.dep - flake - redissolve;
    var before = Math.round((st.tare + r.normal(0, 0.00005)) * 1e4) / 1e4;
    var after = Math.round((st.tare + gain + r.normal(0, 0.00005)) * 1e4) / 1e4;
    var mFound = after - before, mQ = st.Q / (2 * F) * M_CU, effc = mFound / mQ * 100;
    var left = st.C * 0.100 * M_CU * 1000;
    var mode = st.pot ? "E = " + (st.E >= 0 ? "+" : "−") + Math.abs(st.E).toFixed(2) + " V" : "I = " + st.I.toFixed(2) + " A";
    kvFill(Sim.$("#e-result"), [
      ["control", mode + ", " + Math.round(st.t / 60) + " min" + (chk("e-stir") ? ", stirred" : ", not stirred")],
      ["cathode before / after", before.toFixed(4) + " g / " + after.toFixed(4) + " g"],
      ["copper found", (mFound * 1000).toFixed(1) + " mg (stated " + (CU_STATED * 1000).toFixed(1) + " mg, " + sgn(pct(mFound, CU_STATED)) + " %)", Math.abs(pct(mFound, CU_STATED)) <= 0.2 ? "hit" : "miss"],
      ["charge passed", st.Q.toFixed(1) + " C"],
      ["copper that charge could deposit", (mQ * 1000).toFixed(1) + " mg"],
      ["current efficiency", effc.toFixed(2) + " %", effc >= 99 ? "hit" : "miss"],
      ["deposit", spongy ? "dark and spongy, with gas bubbles; some flakes come off when rinsed" : "bright, salmon-pink and adherent"],
      ["copper still in solution", left < 0.01 ? "< 0.01 mg" : left.toFixed(2) + " mg"]
    ].concat(st.pot ? [] : [["note", "At constant current the current cannot fall as the copper runs out: once mass transport cannot carry enough Cu²⁺, the rest of the charge makes hydrogen."]]).concat(st.lift ? [] : [["warning", "The current was switched off before lifting the cathode: copper redissolved in the nitric acid.", "miss"]]));
    var series = [{ type: "line", color: "s1", label: "total current", data: st.rec }, { type: "line", color: "s2", dash: [5, 3], label: "copper part", data: st.rec.filter(function (p) { return p[2] > 1e-4; }) }];
    ePlot.draw(series, { logY: chk("e-log"), yLabel: "current / mA" });
    lastCSV = function () { return { header: ["t_min", "I_total_mA", "I_copper_mA"], rows: st.rec.map(function (p) { return [+p[0].toFixed(2), +p[1].toFixed(4), +p[2].toFixed(4)]; }), filename: "electrogravimetry_current.csv" }; };
    if (log) addRun("Cu electrogravimetry", mode + ", " + Math.round(st.t / 60) + " min" + (st.lift ? "" : ", lifted without current"), (mFound * 1000).toFixed(1) + " mg Cu; efficiency " + effc.toFixed(1) + " %", (CU_STATED * 1000).toFixed(1) + " mg", pct(mFound, CU_STATED));
  }

  function egCheck() {
    if (!eg) { egRun(); return; }
    var dep0 = eg.dep;
    var rec = egIntegrate(eg, 600);
    eg.rec = eg.rec.concat(rec);
    var extra = (eg.dep - dep0) * 1000;
    egFinish(false);
    var box = Sim.$("#e-result");
    box.appendChild(Sim.el("div", { text: "completeness test" }));
    var leftMg = eg.C * 0.100 * M_CU * 1000, msg, ok = false;
    if (extra > 0.1) msg = "a pink film of copper forms on the newly covered stem (" + extra.toFixed(2) + " mg more): not complete";
    else if (leftMg > 0.1) msg = "the stem stays bright, yet " + leftMg.toFixed(1) + " mg of copper is still in solution: at this potential no more copper can deposit (Nernst)";
    else { msg = "the newly covered platinum stays bright: deposition is complete"; ok = true; }
    box.appendChild(Sim.el("div", { text: msg, class: ok ? "hit" : "miss" }));
  }

  Sim.$("#e-mode").addEventListener("change", egModeUI);
  Sim.$("#e-run").addEventListener("click", egRun);
  Sim.$("#e-check").addEventListener("click", egCheck);
  Sim.$("#e-log").addEventListener("change", function () { if (eg) ePlot.draw(ePlot && eg ? [{ type: "line", color: "s1", label: "total current", data: eg.rec }, { type: "line", color: "s2", dash: [5, 3], label: "copper part", data: eg.rec.filter(function (p) { return p[2] > 1e-4; }) }] : [], { logY: chk("e-log") }); });
  Sim.$("#e-rerun").addEventListener("click", function () { seed = Sim.newSeed(seed); showSeed(); egRun(); });

  /* ======================= COULOMETRIC TITRATION ======================= */
  var ct = null, ctLoop = null, blankT = {};
  var cPlot = Sim.plot(Sim.$("#c-plot"), { xLabel: "generation time / s", yLabel: "indicator current / µA" });

  function ctNew() {
    if (ctLoop) { ctLoop.stop(); ctLoop = null; }
    var r = Sim.rng(seed + 71 * (runs.length + 1));
    var I = parseFloat(s("c-cur")) / 1000;
    ct = {
      r: r, I: I, Itrue: I * (1 + r.normal(0, 0.0003)), t: 0, sample: s("c-sample"),
      nRed: (s("c-sample") === "vitc" ? ASC_STATED : 0) + 0.40e-6 * r.uniform(0.9, 1.1),   // mol of 2-electron reductant; 0.4 µmol of impurities in KI/starch
      eff: 1 - 0.0004 * Math.pow(parseFloat(s("c-cur")) / 10, 1.5), rec: [[0, 0.02]], stopped: false, det: s("c-det")
    };
    Sim.$("#c-go").setAttribute("aria-pressed", "false"); Sim.$("#c-go").textContent = "Start generating";
    Sim.$("#c-amp-panel").hidden = ct.det !== "amp";
    kvFill(Sim.$("#c-result"), [["status", "Generate iodine and stop at the end point."]]);
    ctDraw();
  }

  function i2Excess(t) { var nI2 = ct.eff * ct.Itrue * t / (2 * F); return Math.max(0, nI2 - ct.nRed) / 0.055; }   // mol/L in 55 mL
  function ampCurrent(t) { return 0.02 + 2.5e6 * i2Excess(t) + ct.r.normal(0, 0.01); }   // µA

  function ctAdvance(dt) {
    if (!ct || ct.stopped) return;
    var steps = Math.max(1, Math.round(dt / 0.25));
    for (var i = 0; i < steps; i++) { ct.t += dt / steps; }
    ct.rec.push([ct.t, ampCurrent(ct.t)]);
    ctDraw();
  }

  function ctDraw() {
    var c = setupCanvas(Sim.$("#c-cell")), ctx = c.ctx, W = c.w, H = c.h;
    ctx.fillStyle = Sim.color("plot-bg"); ctx.fillRect(0, 0, W, H);
    var ex = ct ? i2Excess(ct.t) : 0, A = 4e4 * ex * 3;    // starch–triiodide, about 4e4 L mol-1 cm-1 at 600 nm
    var rgb = [248 * Math.pow(10, -A), 248 * Math.pow(10, -0.55 * A), 248 * Math.pow(10, -0.12 * A)];
    var bx = W / 2 - Math.min(80, W * 0.3), bw = 2 * Math.min(80, W * 0.3), top = 30, bot = H - 12;
    ctx.fillStyle = "rgb(" + rgb.map(function (q) { return Math.round(q); }).join(",") + ")";
    ctx.fillRect(bx, top + 20, bw, bot - top - 20);
    ctx.strokeStyle = Sim.color("ink"); ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(bx, top); ctx.lineTo(bx, bot); ctx.lineTo(bx + bw, bot); ctx.lineTo(bx + bw, top); ctx.stroke();
    ctx.fillStyle = Sim.color("muted");
    ctx.fillRect(bx + 18, 8, 6, bot - 40); ctx.fillRect(bx + bw - 34, 8, 14, bot - 50);
    ctx.font = "11px " + getComputedStyle(document.body).fontFamily; ctx.textAlign = "left"; ctx.fillStyle = Sim.color("ink");
    ctx.fillText("Pt anode", bx + 28, 18); ctx.textAlign = "right"; ctx.fillText("cathode (frit)", bx + bw - 2, top + 4);
    if (ctLoop && ct && ex === 0 && i2Excess(ct.t + 3) > 0) {   // local excess near the anode before mixing
      ctx.fillStyle = "rgba(40,50,140,0.6)"; ctx.beginPath(); ctx.arc(bx + 21, bot - 46, 9, 0, 2 * Math.PI); ctx.fill();
    }
    var name = A < 0.03 ? "colourless" : A < 0.25 ? "faint blue" : A < 0.8 ? "blue" : "deep blue";
    Sim.$("#c-colour").textContent = ct && ct.det === "amp" ? name + " (no starch needed: watch the current)" : name;
    if (!ct) return;
    Sim.$("#c-readout").textContent = ct.t.toFixed(1) + " s";
    kvFill(Sim.$("#c-live"), [["current", (ct.I * 1000).toFixed(3) + " mA"], ["charge", (ct.I * ct.t).toFixed(4) + " C"], ["indicator", ct.det === "amp" ? ct.rec[ct.rec.length - 1][1].toFixed(2) + " µA" : "starch"]]);
    if (ct.det === "amp") cPlot.draw([{ type: "line", color: "s1", data: ct.rec }], { yMin: 0 });
  }

  function ctToggle() {
    if (!ct || ct.stopped) ctNew();
    var b = Sim.$("#c-go");
    if (ctLoop) { ctLoop.stop(); ctLoop = null; b.setAttribute("aria-pressed", "false"); b.textContent = "Start generating"; ctDraw(); return; }
    b.setAttribute("aria-pressed", "true"); b.textContent = "Stop generating";
    ctLoop = Sim.loop(function (dt) { ctAdvance(dt * 20); return true; });
  }
  function ctPulse(sec) { if (!ct || ct.stopped) ctNew(); if (ctLoop) return; ctAdvance(sec); }

  function ctStop() {
    if (!ct || ct.stopped) return;
    if (ctLoop) { ctLoop.stop(); ctLoop = null; Sim.$("#c-go").setAttribute("aria-pressed", "false"); Sim.$("#c-go").textContent = "Start generating"; }
    ct.stopped = true;
    var key = String(ct.I), t = ct.t, Q = ct.I * t;
    if (ct.sample === "blank") {
      blankT[key] = t;
      kvFill(Sim.$("#c-result"), [["blank", t.toFixed(1) + " s at " + (ct.I * 1000).toFixed(1) + " mA (" + (Q / (2 * F) * 1e6).toFixed(4) + " µmol)"], ["next", "Titrate the sample; this blank is subtracted automatically at the same current."]]);
      addRun("coulometric blank", (ct.I * 1000) + " mA, " + (ct.det === "amp" ? "biamperometric" : "starch"), t.toFixed(1) + " s", "—", NaN);
    } else {
      var tb = blankT[key] || 0, n = ct.I * (t - tb) / (2 * F), err = pct(n, ASC_STATED);
      kvFill(Sim.$("#c-result"), [
        ["time to end point", t.toFixed(1) + " s" + (tb ? " − blank " + tb.toFixed(1) + " s" : " (no blank subtracted)")],
        ["charge Q = I t", (ct.I * (t - tb)).toFixed(4) + " C"],
        ["ascorbic acid n = Q/(2F)", (n * 1e3).toFixed(5) + " mmol = " + (n * M_ASC * 1000).toFixed(3) + " mg"],
        ["stated", "0.05000 mmol = 8.806 mg"],
        ["error", sgn(err) + " %", Math.abs(err) <= 0.5 ? "hit" : "miss"],
        ["generation efficiency (hidden)", (ct.eff * 100).toFixed(2) + " %"]
      ]);
      addRun("coulometric titration", (ct.I * 1000) + " mA, " + (ct.det === "amp" ? "biamperometric" : "starch") + (tb ? ", blank subtracted" : ""), (n * 1e3).toFixed(5) + " mmol", "0.05000 mmol", err);
    }
    var rec = ct.rec, I = ct.I;
    lastCSV = function () { return { header: ["t_s", "indicator_uA", "charge_C"], rows: rec.map(function (p) { return [+p[0].toFixed(2), +p[1].toFixed(3), +(I * p[0]).toFixed(5)]; }), filename: "coulometry_record.csv" }; };
  }

  Sim.$("#c-go").addEventListener("click", ctToggle);
  Sim.$("#c-p1").addEventListener("click", function () { ctPulse(1); });
  Sim.$("#c-p5").addEventListener("click", function () { ctPulse(5); });
  Sim.$("#c-stop").addEventListener("click", ctStop);
  Sim.$("#c-new").addEventListener("click", ctNew);
  ["#c-sample", "#c-cur", "#c-det"].forEach(function (q) { Sim.$(q).addEventListener("change", ctNew); });

  /* ======================= OVEN: BAKING SODA ======================= */
  var ov = null, ovCount = 0;
  var oPlot = Sim.plot(Sim.$("#o-plot"), { xLabel: "total heating time / min", yLabel: "tray + sample / g" });

  function ovStart() {
    ovCount++;
    var r = Sim.rng(seed + 97 * ovCount), m0 = v("o-mass");
    if (!(m0 >= 1 && m0 <= 30)) { m0 = 10; Sim.$("#o-mass").value = "10.00"; }
    var tray = 3.4 + r.uniform(0, 0.25), Tset = parseFloat(s("o-temp"));
    ov = { r: r, m0: m0, tray: tray, Tset: Tset, T: Tset + r.normal(0, 8), t: 0, rows: [] };
    var trayRead = Math.round((tray + r.normal(0, 0.003)) * 100) / 100, totRead = Math.round((tray + m0 + r.normal(0, 0.003)) * 100) / 100;
    ov.trayRead = trayRead; ov.startRead = totRead;
    ov.rows.push([0, totRead]);
    Sim.$("#o-readout").textContent = totRead.toFixed(2) + " g";
    ovTable();
  }
  function ovTable() {
    var tb = Sim.$("#o-table tbody");
    tb.textContent = "";
    var ms = ov.startRead - ov.trayRead;
    ov.rows.forEach(function (q, i) {
      var prev = i ? ov.rows[i - 1][1] : null;
      tb.appendChild(Sim.el("tr", { class: prev !== null && Math.abs(q[1] - prev) <= 0.02 ? "hit" : null }, Sim.el("td", { text: String(q[0]) }), Sim.el("td", { text: q[1].toFixed(2) }), Sim.el("td", { text: ((ov.startRead - q[1]) / ms * 100).toFixed(2) })));
    });
    oPlot.draw([{ type: "line", color: "s1", data: ov.rows }, { type: "points", color: "s1", data: ov.rows }], {});
    var n = ov.rows.length, last = ov.rows[n - 1];
    var rows = [["tray (empty)", ov.trayRead.toFixed(2) + " g"], ["sample", ms.toFixed(2) + " g"]];
    if (n >= 2) {
      var loss = (ov.startRead - last[1]) / ms * 100, constant = n >= 3 && Math.abs(last[1] - ov.rows[n - 2][1]) <= 0.02;
      rows.push(["mass loss", loss.toFixed(2) + " % (theory 36.92 %)"]);
      rows.push(["apparent NaHCO₃", (loss / 36.92 * 100).toFixed(1) + " %"]);
      rows.push(["constant mass", constant ? "yes: the last two weighings agree within 0.02 g" : "not yet", constant ? "hit" : "miss"]);
      rows.push(["uncertainty of each mass", "± " + (0.01 / Math.sqrt(6)).toFixed(3) + " g (difference of two readings, 0.01 g scale)"]);
      ov.loss = loss; ov.constant = constant;
    }
    kvFill(Sim.$("#o-result"), rows);
    lastCSV = function () { return { header: ["t_min", "m_total_g"], rows: ov.rows.map(function (q) { return [q[0], q[1]]; }), filename: "oven_baking_soda.csv" }; };
  }
  function ovHeat() {
    if (!ov) ovStart();
    var r = ov.r, cool = s("o-cool");
    ov.t += 15;
    // first-order decomposition of a thin layer; half-life about 9 min at 200 °C, Ea about 100 kJ/mol (illustrative)
    var k = Math.LN2 / 9 * Math.exp(-100000 / Sim.C.R * (1 / (ov.T + 273.15) - 1 / 473.15));
    var x = 1 - Math.exp(-k * ov.t);
    var up = cool === "board" ? r.normal(0.015, 0.003) * x : cool === "jar" ? 0.002 * x : -r.normal(0.03, 0.008);
    var mass = ov.tray + ov.m0 * (1 - 0.3692 * x) + up + r.normal(0, 0.003);
    var read = Math.round(mass * 100) / 100;
    ov.rows.push([ov.t, read]);
    Sim.$("#o-readout").textContent = read.toFixed(2) + " g";
    ovTable();
    if (ov.constant && !ov.logged) {
      ov.logged = true;
      addRun("baking soda, oven", ov.Tset + " °C, " + { board: "cooled on a board", jar: "cooled in a jar", hot: "weighed warm" }[cool] + ", " + ov.t + " min", ov.loss.toFixed(2) + " % loss", "36.92 %", pct(ov.loss, 36.92));
    }
  }
  Sim.$("#o-start").addEventListener("click", ovStart);
  Sim.$("#o-heat").addEventListener("click", ovHeat);
  Sim.$("#o-rerun").addEventListener("click", function () { seed = Sim.newSeed(seed); showSeed(); ovStart(); });

  /* ======================= tabs and export ======================= */
  Sim.exportCSV(Sim.$("#x-run"), "gravimetry_readings.csv", function () { return lastCSV ? lastCSV() : null; });
  Sim.exportCSV(Sim.$("#x-all"), "gravimetry_results.csv", function () {
    return { header: ["run", "experiment", "choices", "result", "stated", "error_percent"], rows: runs.map(function (r) { return [r.id, r.exp, r.choices, r.result, r.stated, isFinite(r.err) ? +r.err.toFixed(3) : ""]; }) };
  });
  Sim.onTheme(function () { if (ct) ctDraw(); });

  var tabs = Sim.tabs(Sim.$("#tabs"), function (name) {
    tabName = name;
    if (name === "precipitate" && !pg) pgStart();
    if (name === "electrogravimetry") { egModeUI(); if (!eg) { ePlot.draw([], { logY: false, yMin: 0, yMax: 1, xMin: 0, xMax: 45 }); kvFill(Sim.$("#e-result"), [["status", "Choose the conditions and run the electrolysis."]]); } }
    if (name === "coulometry" && !ct) ctNew();
    if (name === "oven" && !ov) ovStart();
    if (name === "coulometry") ctDraw();
  });
  tabs.select(tabName);
})();
