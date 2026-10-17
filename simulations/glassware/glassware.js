/* glassware simulation: weighing (paper vs by difference), volumetric dilution with an
 * uncertainty budget, and parallax when reading a meniscus. Uses ../common/sim.js.
 *
 * Sources for the numbers:
 *  - Class A tolerances: ASTM E288 (volumetric flasks), E969 (transfer pipettes),
 *    E287 (burettes), E1272 (graduated cylinders), as tabulated by Harvey, Analytical
 *    Chemistry 2.1, section 2.4 (LibreTexts) and supplier tables (Lesson 07.7). Class B = 2 x Class A.
 *  - Stock 0.10004 mol/L NaCl with u = 0.065 %: Lesson 07.7 worked example.
 *  - Refractive indices: water 1.333, borosilicate glass about 1.47-1.5.
 *  - Burette geometry: a 50 mL burette has its 0-50 mL scale over about 57 cm, so
 *    1 mL = 1.14 cm and the bore is about 1.06 cm; 100 mL cylinder bore about 2.6 cm.
 * Balance model: offset o(t) = o0 + r t (r a few hundredths of a mg per minute), Gaussian
 * noise 0.03 mg with the doors closed and 0.3 mg open, and a warm-object error of
 * -2 mg x exp(-t/180 s) (convection makes warm objects seem lighter).
 */
(function () {
  "use strict";

  var PRESETS = {
    weighing: {
      title: "Weighing by difference", tab: "weighing",
      what: "An analytical balance reads to 0.1 mg, but its zero (offset) drifts and air currents and warm objects disturb it. Weighing by difference cancels the offset and counts only what really left the bottle; weighing onto paper counts whatever sticks to the paper too.",
      task: "Weigh about 0.5 g of solid into the beaker twice: once from a weighing paper and once by difference from a weighing bottle. Keep the doors closed and record promptly. Then reveal the true masses.",
      target: "By difference, within 0.2 mg of the true mass in the beaker."
    },
    dilution: {
      title: "Making a dilution", tab: "dilution",
      what: "A dilution's uncertainty comes from each piece of glassware you use. Class A transfer pipettes and volumetric flasks are accurate to about 0.05–0.3 %; graduated cylinders and beakers to percent level. Small aliquots carry the largest relative uncertainty.",
      task: "Make 100.0 mL of a 1/50 dilution, choosing the glassware yourself. Then repeat it with graduated cylinders and compare.",
      target: "A relative uncertainty below 0.3 % with the right factor (0.02) and final volume (100.0 mL)."
    },
    parallax: {
      title: "Reading a meniscus without parallax", tab: "parallax",
      what: "The scale is on the front of the glass, but the bottom of the meniscus is in the middle of the tube. If your eye is not level with it, the sight line meets the scale at the wrong mark: a parallax error. On a burette the scale reads downward, so looking from above gives a reading that is too small.",
      task: "Read the burette with your eye level (0 cm), then 2 cm too high and 2 cm too low. Record each reading.",
      target: "The parallax error, in mL, when your eye is 2 cm too high (compare it with the 0.01 mL you can estimate)."
    }
  };

  var preset = Sim.preset(PRESETS, "weighing");
  var seed = Sim.seedFromQuery(11);
  var rng;

  Sim.label();
  Sim.presetBox(Sim.$("#preset"), preset);
  var tabs = Sim.tabs(Sim.$("#tabs"), function (name) { if (name === "parallax") drawParallax(); if (name === "dilution") renderDil(); });

  /* ======================= WEIGHING ======================= */
  var W = {};
  var runs = [];
  var wRevealed = false;

  function initBalance() {
    var r = Sim.rng(seed + 1);
    W = {
      r: r,
      o0: r.uniform(-0.5, 0.5),                       // mg
      drift: r.pick([-1, 1]) * r.uniform(0.03, 0.08),  // mg per minute
      t: 0,
      tareRef: 0,                                      // g
      pan: null,
      paperMass: r.uniform(0.28, 0.32),
      bottleMass: r.uniform(17.8, 18.9),
      run: null
    };
    Sim.$("#w-seed").textContent = String(seed);
  }

  function offsetG(t) { return (W.o0 + W.drift * t / 60) * 1e-3; }

  function panLoad() {
    var run = W.run;
    if (W.pan === "paper") return W.paperMass + (run ? run.paperSolid : 0);
    if (W.pan === "bottle") return W.bottleMass + (run ? run.bottleSolid : 0);
    return 0;
  }

  function reading() {
    var doors = Sim.$("#w-doors").checked;
    var noise = W.r.normal(0, doors ? 0.3 : 0.03) * 1e-3;
    var warm = 0;
    if (W.pan === "bottle" && W.run && W.run.warm) warm = -2.0e-3 * Math.exp(-(W.t - W.run.t0) / 180);
    var v = panLoad() + offsetG(W.t) - W.tareRef + noise + warm;
    return Math.round(v * 1e4) / 1e4;
  }

  function show() {
    var v = reading();
    Sim.$("#w-display").textContent = v.toFixed(4) + " g";
    Sim.$("#w-pan").textContent = "Pan: " + (W.pan === "paper" ? "weighing paper" + (W.run && W.run.paperSolid > 0 ? " with solid" : "") : W.pan === "bottle" ? "weighing bottle with solid" : "empty");
    var mm = Math.floor(W.t / 60), ss = Math.round(W.t % 60);
    var kv = Sim.$("#w-clock");
    kv.textContent = "";
    kv.appendChild(Sim.el("span", { text: "clock" }));
    kv.appendChild(Sim.el("span", { text: mm + " min " + ss + " s" }));
    kv.appendChild(Sim.el("span", { text: "run" }));
    kv.appendChild(Sim.el("span", { text: W.run ? "#" + W.run.id + " (" + (W.run.method === "paper" ? "weighing paper" : "by difference") + ")" : "none — press Start a new run" }));
    var info = Sim.$("#w-runinfo");
    info.textContent = "";
    if (W.run) {
      info.appendChild(Sim.el("span", { text: "readings recorded" }));
      info.appendChild(Sim.el("span", { text: String(W.run.readings.length) }));
    }
    return v;
  }

  function wlog(text) { Sim.log(Sim.$("#w-log"), "[" + Math.floor(W.t / 60) + ":" + String(Math.round(W.t % 60)).padStart(2, "0") + "] " + text); }

  function newRun() {
    var method = Sim.$("input[name=w-method]:checked").value;
    W.pan = null;
    W.run = {
      id: runs.length + 1, method: method, t0: W.t,
      paperSolid: 0, bottleSolid: method === "diff" ? W.r.uniform(2.3, 2.7) : 0,
      beaker: 0, readings: [], tareWithPaper: false,
      residue: W.r.uniform(0.4, 1.5) * 1e-3,
      warm: Sim.$("#w-warm").checked
    };
    Sim.$("#w-log").textContent = "";
    wlog("Run " + W.run.id + " started: " + (method === "paper" ? "weighing paper method" : "weighing by difference") + (W.run.warm ? " (bottle still warm)" : ""));
    show();
  }

  var COST = { paper: 15, bottle: 15, remove: 10, tare: 10, scoop: 15, pinch: 10, unpinch: 10, tip: 20, tap: 10, taplittle: 10, record: 5, wait: 30 };

  function act(a) {
    if (!W.run && a !== "wait" && a !== "tare") { newRun(); }
    var run = W.run;
    W.t += COST[a] || 5;
    switch (a) {
      case "paper":
        if (W.pan) { wlog("Take the " + W.pan + " off first."); break; }
        if (run.method !== "paper") { wlog("This run is by difference: use the weighing bottle."); W.t -= COST[a]; break; }
        W.pan = "paper"; wlog("Weighing paper placed on the pan."); break;
      case "bottle":
        if (W.pan) { wlog("Take the " + W.pan + " off first."); break; }
        if (run.method !== "diff") { wlog("This run uses weighing paper."); W.t -= COST[a]; break; }
        W.pan = "bottle"; wlog("Weighing bottle placed on the pan; doors closed again."); break;
      case "remove":
        if (!W.pan) { wlog("The pan is already empty."); break; }
        wlog("Took the " + (W.pan === "paper" ? "weighing paper" : "weighing bottle") + " off the pan."); W.pan = null; break;
      case "tare":
        W.tareRef = panLoad() + offsetG(W.t);
        if (run && W.pan === "paper" && run.paperSolid === 0) run.tareWithPaper = true;
        wlog("Tare: the display now reads zero" + (W.pan ? " with the " + W.pan + " on the pan." : ".")); break;
      case "scoop": case "pinch": case "unpinch":
        if (run.method !== "paper") { wlog("Use the bottle: tap solid out of it."); break; }
        if (W.pan !== "paper") { wlog("Put the weighing paper on the pan first."); break; }
        var amt = a === "scoop" ? W.r.uniform(0.10, 0.20) : W.r.uniform(0.004, 0.02);
        if (a === "unpinch") amt = -Math.min(run.paperSolid, amt);
        run.paperSolid += amt;
        wlog(a === "scoop" ? "Added a scoop of solid to the paper." : a === "pinch" ? "Added a pinch." : "Took a pinch back."); break;
      case "tip":
        if (run.method !== "paper") { wlog("No paper in this run."); break; }
        if (run.paperSolid <= 0) { wlog("There is no solid on the paper."); break; }
        if (W.pan === "paper") { W.pan = null; wlog("Lifted the paper off the pan."); }
        var left = Math.min(run.paperSolid, run.residue);
        run.beaker += run.paperSolid - left;
        run.paperSolid = left;
        run.tipped = true;
        wlog("Tipped the paper into the beaker. A little powder clings to the paper."); break;
      case "tap": case "taplittle":
        if (run.method !== "diff") { wlog("No weighing bottle in this run."); break; }
        if (W.pan === "bottle") { W.pan = null; W.t += 5; wlog("Lifted the bottle off the pan."); }
        var d = a === "tap" ? W.r.uniform(0.08, 0.18) : W.r.uniform(0.01, 0.04);
        d = Math.min(d, run.bottleSolid);
        run.bottleSolid -= d; run.beaker += d;
        wlog(a === "tap" ? "Tapped solid from the bottle into the beaker." : "Tapped gently: a little solid fell into the beaker."); break;
      case "record":
        var v = reading();
        run.readings.push({ t: W.t, pan: W.pan || "empty", value: v, doors: Sim.$("#w-doors").checked });
        wlog("Recorded " + v.toFixed(4) + " g (" + (W.pan || "empty pan") + ")" + (Sim.$("#w-doors").checked ? " with the doors open" : "")); break;
      case "wait":
        wlog("Waited 30 s."); break;
    }
    show();
  }

  function finishRun() {
    var run = W.run;
    if (!run) return;
    var rep = NaN, note = "";
    if (run.method === "paper") {
      var pr = run.readings.filter(function (x) { return x.pan === "paper"; });
      if (!pr.length) note = "Record the reading with the solid on the paper.";
      else {
        rep = pr[pr.length - 1].value;
        if (!run.tareWithPaper) note = "You did not tare with the empty paper on the pan, so the paper is counted too.";
      }
      if (!run.tipped) note = (note ? note + " " : "") + "The solid is still on the paper.";
    } else {
      var br = run.readings.filter(function (x) { return x.pan === "bottle"; });
      if (br.length < 2) note = "Record the bottle before (m1) and after (m2) tapping.";
      else rep = br[0].value - br[br.length - 1].value;
    }
    if (note) wlog(note);
    if (!isFinite(rep)) return;
    runs.push({ id: run.id, method: run.method, reported: rep, truth: run.beaker, readings: run.readings.slice(), warm: run.warm });
    wlog("Run " + run.id + " finished: reported mass " + rep.toFixed(4) + " g.");
    W.run = null; W.pan = null;
    renderRuns();
    show();
  }

  function renderRuns() {
    var tb = Sim.$("#w-results tbody");
    tb.textContent = "";
    runs.forEach(function (r) {
      var err = (r.reported - r.truth) * 1e3;
      var ok = Math.abs(err) <= 0.2;
      tb.appendChild(Sim.el("tr", {},
        Sim.el("td", { text: String(r.id) }),
        Sim.el("td", { text: r.method === "paper" ? "paper" : "difference" }),
        Sim.el("td", { text: r.reported.toFixed(4) }),
        Sim.el("td", { text: wRevealed ? r.truth.toFixed(5) : "hidden" }),
        Sim.el("td", { class: wRevealed ? (ok ? "hit" : "miss") : "", text: wRevealed ? (err >= 0 ? "+" : "") + err.toFixed(2) + (ok ? " ✓" : "") : "—" })));
    });
  }

  Sim.$$("#w-actions button").forEach(function (b) { b.addEventListener("click", function () { act(b.getAttribute("data-act")); }); });
  Sim.$("#w-new").addEventListener("click", newRun);
  Sim.$("#w-finish").addEventListener("click", finishRun);
  Sim.$("#w-reveal").addEventListener("click", function () { wRevealed = !wRevealed; Sim.$("#w-reveal").textContent = wRevealed ? "Hide true masses" : "Reveal true masses"; renderRuns(); });
  Sim.$("#w-doors").addEventListener("change", function () { wlog(Sim.$("#w-doors").checked ? "Opened the draft-shield doors." : "Closed the doors."); show(); });
  Sim.$("#w-rerun").addEventListener("click", function () { seed = Sim.newSeed(seed); initBalance(); initGlass(); runs = []; renderRuns(); Sim.$("#w-log").textContent = ""; show(); newLevel(); renderDil(); });

  /* ======================= DILUTION ======================= */
  // kind: pip (transfer pipette, TD), bur (burette), cyl (graduated cylinder), bk (beaker), fl (volumetric flask, TC)
  var GLASS = [
    { id: "pip1", kind: "pip", v: 1, tol: 0.006, name: "1 mL transfer pipette" },
    { id: "pip2", kind: "pip", v: 2, tol: 0.006, name: "2 mL transfer pipette" },
    { id: "pip5", kind: "pip", v: 5, tol: 0.01, name: "5 mL transfer pipette" },
    { id: "pip10", kind: "pip", v: 10, tol: 0.02, name: "10 mL transfer pipette" },
    { id: "pip20", kind: "pip", v: 20, tol: 0.03, name: "20 mL transfer pipette" },
    { id: "pip25", kind: "pip", v: 25, tol: 0.03, name: "25 mL transfer pipette" },
    { id: "pip50", kind: "pip", v: 50, tol: 0.05, name: "50 mL transfer pipette" },
    { id: "bur50", kind: "bur", v: 50, tol: 0.05, name: "50 mL burette (two readings)" },
    { id: "cyl10", kind: "cyl", v: 10, tol: 0.10, name: "10 mL graduated cylinder" },
    { id: "cyl25", kind: "cyl", v: 25, tol: 0.17, name: "25 mL graduated cylinder" },
    { id: "cyl50", kind: "cyl", v: 50, tol: 0.25, name: "50 mL graduated cylinder" },
    { id: "cyl100", kind: "cyl", v: 100, tol: 0.50, name: "100 mL graduated cylinder" },
    { id: "bk250", kind: "bk", v: 250, tol: 0.05, name: "250 mL beaker (graduations ±5 %)" },
    { id: "fl25", kind: "fl", v: 25, tol: 0.03, name: "25 mL volumetric flask" },
    { id: "fl50", kind: "fl", v: 50, tol: 0.05, name: "50 mL volumetric flask" },
    { id: "fl100", kind: "fl", v: 100, tol: 0.08, name: "100 mL volumetric flask" },
    { id: "fl250", kind: "fl", v: 250, tol: 0.12, name: "250 mL volumetric flask" },
    { id: "fl500", kind: "fl", v: 500, tol: 0.20, name: "500 mL volumetric flask" }
  ];
  var G = {};
  GLASS.forEach(function (g) { G[g.id] = g; });
  var STOCK = { c: 0.10004, rel: 0.00065 };
  var hiddenErr = {}, stockTrue = STOCK.c, attempts = [], dRevealed = false, lastBudget = null;
  var dPlot = Sim.plot(Sim.$("#d-plot"), { xLabel: "attempt", yLabel: "u(c)/c / %", legend: true, yMin: 0 });

  function initGlass() {
    var r = Sim.rng(seed + 2);
    hiddenErr = {};
    // every physical item has a fixed calibration error inside its tolerance (uniform)
    GLASS.forEach(function (g) { hiddenErr[g.id] = r.uniform(-1, 1); });
    stockTrue = STOCK.c * (1 + r.normal(0, STOCK.rel));
    attempts = [];
    rng = Sim.rng(seed + 3);
  }

  function variable(g) { return g.kind === "bur" || g.kind === "cyl" || g.kind === "bk"; }
  function tolOf(g, vol, cls) {
    var f = cls === "B" ? 2 : 1;
    if (g.kind === "bk") return 0.05 * vol;        // percent-level, not class-rated
    return g.tol * f;
  }

  function fillSelect(sel, kinds, def) {
    sel.textContent = "";
    GLASS.forEach(function (g) { if (kinds.indexOf(g.kind) >= 0) sel.appendChild(Sim.el("option", { value: g.id, text: g.name })); });
    sel.value = def;
  }
  fillSelect(Sim.$("#d-a1"), ["pip", "bur", "cyl", "bk"], "pip2");
  fillSelect(Sim.$("#d-a2"), ["pip", "bur", "cyl", "bk"], "pip20");
  fillSelect(Sim.$("#d-f1"), ["fl", "cyl", "bk"], "fl100");
  fillSelect(Sim.$("#d-f2"), ["fl", "cyl", "bk"], "fl100");

  function syncVolFields() {
    [["a1", "#d-a1", "#d-a1v-wrap", "#d-a1v"], ["a2", "#d-a2", "#d-a2v-wrap", "#d-a2v"], ["f1", "#d-f1", "#d-f1v-wrap", "#d-f1v"], ["f2", "#d-f2", "#d-f2v-wrap", "#d-f2v"]].forEach(function (z) {
      var g = G[Sim.$(z[1]).value];
      var wrap = Sim.$(z[2]), inp = Sim.$(z[3]);
      if (variable(g)) { wrap.hidden = false; inp.max = String(g.v); }
      else { wrap.hidden = true; inp.value = String(g.v); }
    });
    Sim.$("#d-step2").hidden = !Sim.$("#d-two").checked;
  }
  ["#d-a1", "#d-a2", "#d-f1", "#d-f2", "#d-two"].forEach(function (s) { Sim.$(s).addEventListener("change", syncVolFields); });

  function makeDilution() {
    var cls = Sim.$("#d-class").value;
    var two = Sim.$("#d-two").checked;
    var tech = { rinse: Sim.$("#m-rinse").checked, blow: Sim.$("#m-blow").checked, over: Sim.$("#m-overshoot").checked, above: Sim.$("#m-above").checked, mix: Sim.$("#m-mix").checked };
    var steps = [["#d-a1", "#d-a1v", "#d-f1", "#d-f1v"]];
    if (two) steps.push(["#d-a2", "#d-a2v", "#d-f2", "#d-f2v"]);
    var budget = [{ name: "Stock concentration", vol: NaN, tol: NaN, u: NaN, rel: STOCK.rel }];
    var factorNom = 1, factorTrue = 1, plan = [], problems = [];
    var ok = true;
    steps.forEach(function (s, i) {
      var ga = G[Sim.$(s[0]).value], gf = G[Sim.$(s[2]).value];
      var va = variable(ga) ? parseFloat(Sim.$(s[1]).value) : ga.v;
      var vf = variable(gf) ? parseFloat(Sim.$(s[3]).value) : gf.v;
      if (!(va > 0) || !(vf > 0) || va > ga.v || vf > gf.v || va >= vf) { ok = false; problems.push("Step " + (i + 1) + ": check the volumes (the aliquot must fit the device and be smaller than the final volume)."); return; }
      // standard uncertainties
      var ta = tolOf(ga, va, cls), tf = tolOf(gf, vf, cls);
      var ua = ta / Math.sqrt(3);
      if (ga.kind === "bur") ua = Math.sqrt(ua * ua + 2 * 0.01 * 0.01);
      var uf = tf / Math.sqrt(3);
      budget.push({ name: "Step " + (i + 1) + " aliquot: " + ga.name, vol: va, tol: ta, u: ua, rel: ua / va });
      budget.push({ name: "Step " + (i + 1) + " final: " + gf.name, vol: vf, tol: tf, u: uf, rel: uf / vf });
      factorNom *= va / vf;
      // true volumes: fixed calibration error of the item + random use scatter + technique
      var errA = hiddenErr[ga.id] * ta * (variable(ga) ? va / ga.v : 1);
      if (ga.kind === "bk") errA = hiddenErr[ga.id] * ta;
      var trueA = va + errA + rng.normal(0, 0.15 * ta);
      if (ga.kind === "pip" || ga.kind === "bur") {
        if (!tech.rinse) { trueA *= 1 - 0.004; if (i === 0) problems.push("Unrinsed pipette or burette: the water film inside diluted the aliquot (about −0.4 %)."); }
      }
      if (ga.kind === "pip" && tech.blow) { trueA += 0.01 * Math.sqrt(ga.v); if (i === 0) problems.push("Blowing out a TD pipette delivers the drop it is calibrated to keep (+" + (100 * 0.01 * Math.sqrt(ga.v) / ga.v).toFixed(1) + " % for this pipette)."); }
      var errF = hiddenErr[gf.id] * tf;
      var trueF = vf + errF + rng.normal(0, 0.15 * tf);
      if (gf.kind === "fl") {
        if (tech.over) { trueF += rng.uniform(0.1, 0.4); if (i === 0) problems.push("Overshooting the mark adds water you cannot remove: start again in real life."); }
        if (tech.above) { trueF -= rng.uniform(0.03, 0.08); if (i === 0) problems.push("Reading the flask mark from above stops the filling a little early (a small, systematic low volume)."); }
      }
      factorTrue *= trueA / trueF;
      plan.push(ga.name.replace(/ \(.*\)/, "") + " " + va + " mL → " + gf.name.replace(/ \(.*\)/, "") + " " + vf + " mL");
    });
    if (!ok) { renderDil(problems); return; }
    var mixFactor = tech.mix ? 1 : 1 + rng.normal(0, 0.02);
    if (!tech.mix) problems.push("Not mixed: the solution is layered, so a portion taken from it is off by a few percent. No uncertainty formula covers this.");
    var rel = Math.sqrt(budget.reduce(function (a, b) { return a + b.rel * b.rel; }, 0));
    budget.forEach(function (b) { b.share = b.rel * b.rel / (rel * rel); });
    var cNom = STOCK.c * factorNom, cTrue = stockTrue * factorTrue * mixFactor;
    var finalVol = parseFloat(Sim.$(steps[steps.length - 1][3]).value);
    var att = { id: attempts.length + 1, plan: plan.join("; then "), cls: cls, finalVol: finalVol, factor: factorNom, rel: rel, cNom: cNom, cTrue: cTrue, budget: budget, problems: problems };
    attempts.push(att);
    lastBudget = att;
    renderDil();
  }

  function renderDil(problems) {
    var res = Sim.$("#d-result");
    res.textContent = "";
    var a = lastBudget;
    function kv(k, v, cls) { res.appendChild(Sim.el("span", { text: k })); res.appendChild(Sim.el("span", { class: cls || "", html: v })); }
    if (problems && problems.length) problems.forEach(function (p) { kv("problem", p, "warn"); });
    var tb = Sim.$("#d-budget tbody");
    tb.textContent = "";
    if (a) {
      var factorOk = Math.abs(a.factor / 0.02 - 1) < 0.005, volOk = Math.abs(a.finalVol - 100) < 0.05, uOk = a.rel < 0.003;
      kv("plan", a.plan + " (Class " + a.cls + ")");
      kv("dilution factor", a.factor.toPrecision(4) + (factorOk ? " = 1/50 ✓" : " (target 1/50 = 0.02)"), factorOk ? "good" : "warn");
      kv("final volume", a.finalVol.toFixed(1) + " mL" + (volOk ? " ✓" : " (target 100.0 mL)"), volOk ? "good" : "warn");
      kv("c (nominal)", Sim.fmtU(a.cNom, a.cNom * a.rel, "mol/L"));
      kv("relative u", (100 * a.rel).toFixed(3) + " %" + (uOk ? " ✓ below 0.3 %" : " (target below 0.3 %)"), uOk ? "good" : "warn");
      if (dRevealed) kv("true c", a.cTrue.toPrecision(6) + " mol/L (error " + ((a.cTrue / a.cNom - 1) * 100).toFixed(3) + " % = " + ((a.cTrue - a.cNom) / (a.cNom * a.rel)).toFixed(2) + " u)");
      a.problems.forEach(function (p) { kv("note", p, "warn"); });
      a.budget.forEach(function (b) {
        tb.appendChild(Sim.el("tr", {},
          Sim.el("td", { text: b.name }), Sim.el("td", { text: isFinite(b.vol) ? b.vol.toFixed(2) : "—" }),
          Sim.el("td", { text: isFinite(b.tol) ? b.tol.toFixed(3) : "—" }), Sim.el("td", { text: isFinite(b.u) ? b.u.toFixed(4) : "—" }),
          Sim.el("td", { text: (100 * b.rel).toFixed(3) + " %" }), Sim.el("td", { text: (100 * b.share).toFixed(1) + " %" })));
      });
    } else kv("status", "Choose the glassware and press Make the dilution.");

    var at = Sim.$("#d-attempts tbody");
    at.textContent = "";
    attempts.forEach(function (x) {
      at.appendChild(Sim.el("tr", {},
        Sim.el("td", { text: String(x.id) }), Sim.el("td", { text: x.plan + " (" + x.cls + ")" }), Sim.el("td", { text: x.finalVol.toFixed(1) }),
        Sim.el("td", { text: x.factor.toPrecision(4) }), Sim.el("td", { text: (100 * x.rel).toFixed(3) + " %" }),
        Sim.el("td", { text: x.cNom.toPrecision(5) }), Sim.el("td", { text: dRevealed ? x.cTrue.toPrecision(5) : "hidden" }),
        Sim.el("td", { text: dRevealed ? ((x.cTrue - x.cNom) / (x.cNom * x.rel)).toFixed(2) : "—" })));
    });
    var bars = attempts.map(function (x) { return [x.id, 100 * x.rel]; });
    dPlot.draw([{ type: "bars", data: bars, color: "s1", barWidth: 0.6, label: "u(c)/c" }, { type: "hline", y: 0.3, color: "s2", dash: [6, 4], label: "target 0.3 %" }],
      { xMin: 0.4, xMax: Math.max(3, attempts.length) + 0.6, xPad: false });
  }

  Sim.$("#d-make").addEventListener("click", function () { makeDilution(); });
  Sim.$("#d-best").addEventListener("click", function () {
    Sim.$("#d-two").checked = false; Sim.$("#d-a1").value = "pip2"; Sim.$("#d-f1").value = "fl100"; Sim.$("#d-class").value = "A";
    syncVolFields();
  });
  Sim.$("#d-cyl").addEventListener("click", function () {
    Sim.$("#d-two").checked = false; Sim.$("#d-a1").value = "cyl10"; Sim.$("#d-a1v").value = "2.0"; Sim.$("#d-f1").value = "cyl100"; Sim.$("#d-f1v").value = "100";
    syncVolFields();
  });
  Sim.$("#d-reveal").addEventListener("click", function () { dRevealed = !dRevealed; Sim.$("#d-reveal").textContent = dRevealed ? "Hide true concentrations" : "Reveal true concentrations"; renderDil(); });
  Sim.$("#d-rerun").addEventListener("click", function () { seed = Sim.newSeed(seed); initGlass(); lastBudget = null; renderDil(); });

  /* ======================= PARALLAX ======================= */
  var VESSELS = {
    burette: { cmPerMl: 1.14, dir: -1, rIn: 0.53, wall: 0.12, minor: 0.1, major: 1, label: 1, window: 0.7, lo: 3, hi: 47, readDec: 2, name: "50 mL burette" },
    cylinder: { cmPerMl: 0.188, dir: 1, rIn: 1.3, wall: 0.2, minor: 1, major: 5, label: 10, window: 7, lo: 20, hi: 92, readDec: 1, name: "100 mL graduated cylinder" }
  };
  var N_GLASS = 1.47, N_WATER = 1.333;
  var par = { level: 23.47, readings: [] };
  var sidePlot = Sim.$("#p-side"), viewCanvas = Sim.$("#p-view");

  function vessel() { return VESSELS[Sim.$("#p-vessel").value]; }
  function eyeH() { return parseFloat(Sim.$("#p-h").value); }
  function eyeD() { return parseFloat(Sim.$("#p-D").value); }
  function apparentDepth(V) { return V.wall / N_GLASS + V.rIn / N_WATER; }
  function shiftCm(V, h, D) { var d = apparentDepth(V); return h * d / (D + d); }   // height above the meniscus where the sight line crosses the scale
  function parallaxMl(V, h, D) { return V.dir * shiftCm(V, h, D) / V.cmPerMl; }   // apparent reading - true reading

  function newLevel() {
    var V = vessel(), r = Sim.rng(seed + 7 + par.readings.length * 13);
    par.level = r.uniform(V.lo, V.hi);
    Sim.$("#p-read").value = "";
    drawParallax();
  }

  function setupCanvas(cv) {
    var dpr = window.devicePixelRatio || 1, w = cv.clientWidth || 300, h = cv.clientHeight || 300;
    cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr);
    var ctx = cv.getContext("2d");
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    return { ctx: ctx, w: w, h: h };
  }

  function drawView() {
    var V = vessel(), h = eyeH(), D = eyeD();
    var c = setupCanvas(viewCanvas), ctx = c.ctx, W2 = c.w, H2 = c.h;
    var ink = Sim.color("ink"), muted = Sim.color("muted"), bg = Sim.color("plot-bg");
    ctx.fillStyle = bg; ctx.fillRect(0, 0, W2, H2);
    var pxPerMl = H2 / (2 * V.window);
    // y on canvas of a scale value v: the window is centred on the true level
    // a scale that reads downward (burette) puts larger values lower on the canvas
    function yOf(v) { return V.dir === -1 ? H2 / 2 + (v - par.level) * pxPerMl : H2 / 2 - (v - par.level) * pxPerMl; };
    var tubeW = Math.min(W2 * 0.55, 260), x0 = (W2 - tubeW) / 2, x1 = x0 + tubeW;
    // the meniscus appears where the sight line meets the scale: shiftCm above the true level
    var shiftPx = shiftCm(V, h, D) / V.cmPerMl * pxPerMl;
    var yMen = H2 / 2 - shiftPx;
    var dark = Sim.isDark();
    // liquid
    ctx.fillStyle = dark ? "rgba(90,169,230,0.18)" : "rgba(31,111,178,0.12)";
    ctx.fillRect(x0, yMen, tubeW, H2 - yMen);
    // meniscus: concave band; seen from above or below it looks like a flattened ellipse
    var ry = Math.max(1.5, Math.abs(Math.sin(Math.atan2(h, D))) * V.rIn / V.cmPerMl * pxPerMl);
    var rise = Math.min(22, 0.18 / V.cmPerMl * pxPerMl + 6);
    ctx.strokeStyle = dark ? "#cfd8e3" : "#24313d";
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(x0, yMen - rise);
    ctx.quadraticCurveTo((x0 + x1) / 2, yMen + rise, x1, yMen - rise);
    ctx.stroke();
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.ellipse((x0 + x1) / 2, yMen - rise / 2, tubeW / 2, ry, 0, 0, 2 * Math.PI);
    ctx.globalAlpha = 0.35; ctx.stroke(); ctx.globalAlpha = 1;
    // tube walls
    ctx.strokeStyle = muted; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(x0, 0); ctx.lineTo(x0, H2); ctx.moveTo(x1, 0); ctx.lineTo(x1, H2); ctx.stroke();
    // scale marks, drawn on the front of the glass
    ctx.strokeStyle = ink; ctx.fillStyle = ink; ctx.font = "13px " + getComputedStyle(document.body).fontFamily;
    ctx.textBaseline = "middle"; ctx.textAlign = "left";
    var start = Math.floor((par.level - V.window) / V.minor) * V.minor;
    for (var v = start; v <= par.level + V.window + 1e-9; v += V.minor) {
      var vv = Math.round(v / V.minor) * V.minor;
      var y = yOf(vv);
      if (y < -5 || y > H2 + 5) continue;
      var isMajor = Math.abs(vv / V.major - Math.round(vv / V.major)) < 1e-6;
      var isLabel = Math.abs(vv / V.label - Math.round(vv / V.label)) < 1e-6;
      var len = isLabel ? tubeW * 0.5 : isMajor ? tubeW * 0.35 : tubeW * 0.2;
      ctx.lineWidth = isLabel ? 2 : 1.2;
      ctx.beginPath(); ctx.moveTo(x0, y); ctx.lineTo(x0 + len, y); ctx.stroke();
      if (isLabel) ctx.fillText(String(Math.round(vv)), x0 + len + 6, y);
    }
    ctx.fillStyle = muted; ctx.textAlign = "right";
    ctx.fillText(V.dir === -1 ? "scale reads downward ↓" : "scale reads upward ↑", W2 - 8, 14);
  }

  function drawSide() {
    var V = vessel(), h = eyeH(), D = eyeD();
    var c = setupCanvas(sidePlot), ctx = c.ctx, W2 = c.w, H2 = c.h;
    ctx.fillStyle = Sim.color("plot-bg"); ctx.fillRect(0, 0, W2, H2);
    var ink = Sim.color("ink"), muted = Sim.color("muted"), acc = Sim.color("s2");
    // not to scale horizontally: distances are compressed so everything fits
    var yMid = H2 / 2, pxPerCm = (H2 / 2 - 16) / 4;
    var tubeX = W2 - 70, tubeR = 22, eyeX = 30;
    ctx.strokeStyle = muted; ctx.lineWidth = 2;
    ctx.strokeRect(tubeX - tubeR, 8, 2 * tubeR, H2 - 16);
    ctx.fillStyle = Sim.isDark() ? "rgba(90,169,230,0.18)" : "rgba(31,111,178,0.12)";
    ctx.fillRect(tubeX - tubeR, yMid, 2 * tubeR, H2 / 2 - 8);
    ctx.strokeStyle = ink; ctx.beginPath(); ctx.moveTo(tubeX - tubeR, yMid - 4); ctx.quadraticCurveTo(tubeX, yMid + 6, tubeX + tubeR, yMid - 4); ctx.stroke();
    var eyeY = yMid - h * pxPerCm;
    ctx.fillStyle = ink; ctx.beginPath(); ctx.ellipse(eyeX, eyeY, 10, 6, 0, 0, 2 * Math.PI); ctx.stroke();
    ctx.beginPath(); ctx.arc(eyeX + 3, eyeY, 2.5, 0, 2 * Math.PI); ctx.fill();
    ctx.strokeStyle = acc; ctx.setLineDash([5, 4]);
    ctx.beginPath(); ctx.moveTo(eyeX + 10, eyeY); ctx.lineTo(tubeX, yMid + 1); ctx.stroke(); ctx.setLineDash([]);
    // where the line crosses the front of the tube (exaggerated for visibility)
    var frontX = tubeX - tubeR, t = (frontX - eyeX - 10) / (tubeX - eyeX - 10), yCross = eyeY + (yMid + 1 - eyeY) * t;
    ctx.fillStyle = acc; ctx.beginPath(); ctx.arc(frontX, yCross, 3.5, 0, 2 * Math.PI); ctx.fill();
    ctx.fillStyle = muted; ctx.font = "11px " + getComputedStyle(document.body).fontFamily; ctx.textAlign = "left";
    ctx.fillText("eye " + (h > 0 ? h.toFixed(1) + " cm above" : h < 0 ? (-h).toFixed(1) + " cm below" : "level"), eyeX - 20, Math.max(12, Math.min(H2 - 4, eyeY - 12)));
    ctx.fillText("D = " + D + " cm (not to scale)", W2 / 2 - 60, H2 - 6);
    ctx.textAlign = "right";
    ctx.fillText("scale mark you line up", frontX - 6, Math.max(12, yCross - 8));
  }

  function drawParallax() {
    var V = vessel(), h = eyeH(), D = eyeD();
    Sim.$("#p-h-out").textContent = (h > 0 ? "+" : "") + h.toFixed(1);
    Sim.$("#p-D-out").textContent = String(D);
    if (Sim.$("#tab-parallax").hidden) return;
    drawView();
    drawSide();
    var info = Sim.$("#p-info");
    info.textContent = "";
    if (Sim.$("#p-geom").checked) {
      var d = apparentDepth(V), s = shiftCm(V, h, D), e = parallaxMl(V, h, D);
      [["apparent depth of the meniscus behind the scale", d.toFixed(3) + " cm (wall/n_glass + r/n_water)"],
        ["sight line meets the scale", (s * 10).toFixed(2) + " mm " + (s >= 0 ? "above" : "below") + " the meniscus"],
        ["scale", V.cmPerMl.toFixed(3) + " cm per mL"],
        ["parallax error (apparent − true)", (e >= 0 ? "+" : "") + e.toFixed(3) + " mL"]].forEach(function (r) {
        info.appendChild(Sim.el("span", { text: r[0] })); info.appendChild(Sim.el("span", { text: r[1] }));
      });
    }
  }

  function recordParallax() {
    var v = parseFloat(Sim.$("#p-read").value);
    if (!isFinite(v)) { Sim.$("#p-read").focus(); return; }
    var V = vessel();
    par.readings.push({ vessel: Sim.$("#p-vessel").value, h: eyeH(), D: eyeD(), read: v, truth: par.level, dec: V.readDec });
    renderParTable();
  }

  function renderParTable() {
    var tb = Sim.$("#p-table tbody");
    tb.textContent = "";
    par.readings.forEach(function (r, i) {
      var e = r.read - r.truth;
      tb.appendChild(Sim.el("tr", {}, Sim.el("td", { text: String(i + 1) }), Sim.el("td", { text: r.vessel }),
        Sim.el("td", { text: (r.h > 0 ? "+" : "") + r.h.toFixed(1) }), Sim.el("td", { text: String(r.D) }),
        Sim.el("td", { text: r.read.toFixed(r.dec) }), Sim.el("td", { text: r.truth.toFixed(r.dec + 1) }),
        Sim.el("td", { text: (e >= 0 ? "+" : "") + e.toFixed(r.dec + 1) })));
    });
  }

  ["#p-h", "#p-D"].forEach(function (s) { Sim.$(s).addEventListener("input", drawParallax); });
  Sim.$("#p-geom").addEventListener("change", drawParallax);
  Sim.$("#p-vessel").addEventListener("change", newLevel);
  Sim.$("#p-new").addEventListener("click", newLevel);
  Sim.$("#p-check").addEventListener("click", recordParallax);
  Sim.$("#p-read").addEventListener("keydown", function (e) { if (e.key === "Enter") recordParallax(); });
  if (typeof window.ResizeObserver === "function") new window.ResizeObserver(function () { drawParallax(); }).observe(viewCanvas);
  Sim.onTheme(drawParallax);

  /* ======================= EXPORT ======================= */
  Sim.exportCSV(Sim.$("#x-weigh"), "weighing_runs.csv", function () {
    var rows = [];
    runs.forEach(function (r) {
      r.readings.forEach(function (x, i) { rows.push([r.id, r.method, i + 1, x.t, x.pan, x.value.toFixed(4), x.doors ? "open" : "closed", r.reported.toFixed(4), wRevealed ? r.truth.toFixed(5) : ""]); });
    });
    return { header: ["run", "method", "reading_no", "time_s", "on_pan", "reading_g", "doors", "reported_mass_g", "true_mass_g"], rows: rows };
  });
  Sim.exportCSV(Sim.$("#x-dil"), "dilution_attempts.csv", function () {
    var rows = [];
    attempts.forEach(function (a) {
      a.budget.forEach(function (b) { rows.push([a.id, a.plan, a.cls, b.name, isFinite(b.vol) ? b.vol : "", isFinite(b.tol) ? b.tol : "", isFinite(b.u) ? b.u : "", b.rel, a.factor, a.rel, a.cNom, dRevealed ? a.cTrue : ""]); });
    });
    return { header: ["attempt", "plan", "class", "input", "volume_mL", "tolerance_mL", "u_mL", "relative_u", "factor", "combined_relative_u", "c_nominal_mol_L", "c_true_mol_L"], rows: rows };
  });
  Sim.exportCSV(Sim.$("#x-par"), "meniscus_readings.csv", function () {
    return { header: ["reading_no", "vessel", "eye_height_cm", "eye_distance_cm", "reading_mL", "true_mL", "error_mL"],
      rows: par.readings.map(function (r, i) { return [i + 1, r.vessel, r.h, r.D, r.read, +r.truth.toFixed(4), +(r.read - r.truth).toFixed(4)]; }) };
  });

  /* ======================= START ======================= */
  initBalance();
  initGlass();
  syncVolFields();
  show();
  renderRuns();
  tabs.select(preset.tab || "weighing");
  newLevel();
})();
