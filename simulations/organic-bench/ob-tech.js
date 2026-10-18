/* organic-bench, part 2: the technique stations (lessons 24.1-24.3). Defines window.OB_TECH(seed).
 * Uses ../common/sim.js (Sim) and ob-core.js (OB).
 *
 * Reflux: Arrhenius with Ea = 80 kJ/mol (lesson 24.1: about 150 times faster at 80 C than at 25 C);
 *   ethanol bp 78 C.
 * Extraction: D = K_D [H3O+]/([H3O+] + Ka) (lesson 19.3/24.1); benzoic acid pKa 4.20, log Kow 1.87
 *   (PubChem), benzophenone log Kow 3.18 (PubChem); octanol-water values stand in for ether-water.
 *   Ether holds about 1.2 % water by mass when saturated (model value of the size Nichols gives);
 *   MgSO4 binds about 0.25 g water per g and Na2SO4 about 0.2 g per g in practice (model values).
 * Recrystallisation: acetanilide 1 g in 185 mL cold and 20 mL boiling water (PubChem 904), mp 114.3 C.
 *   Ethanol, hexane and xylene solubilities are approximate model values for comparison.
 * Distillation: Raoult's law with NIST Antoine constants; batch (Rayleigh) distillation through
 *   N equilibrium stages at total reflux (pot = 1 stage; a slow column adds its plates, a fast one
 *   about 40 % of them). Molar volumes from densities 0.7781 (cyclohexane) and 0.8669 g/mL (toluene).
 * TLC and melting point: OB.rf and OB.meltRange (ob-core.js).
 */
(function (global) {
  "use strict";
  global.OB_TECH = function (seed0) {
    var C = OB.C, S = Sim.stats;
    function $(id) { return document.getElementById(id); }
    function tr(cells) { var row = Sim.el("tr"); cells.forEach(function (c) { row.appendChild(Sim.el("td", { html: String(c) })); }); return row; }
    function kv(el, pairs) { el.textContent = ""; pairs.forEach(function (p) { el.appendChild(Sim.el("span", { html: p[0] })); el.appendChild(Sim.el("span", { html: p[1] })); }); }
    function say(el, text, cls) { var d = Sim.el("div", { html: text }); if (cls) d.className = cls; el.appendChild(d); el.scrollTop = el.scrollHeight; }
    var seed = seed0, rng = Sim.rng(seed0);

    /* ======================= reflux ======================= */
    $("t-rf-go").addEventListener("click", function () {
      var stir = $("t-rf-stir").value, water = $("t-rf-water").value, top = $("t-rf-top").value, heat = $("t-rf-heat").value, level = $("t-rf-level").value;
      var log = $("t-rf-log"), solvent = 50, T = 78, minutes = 60, lostMix = 0, events = [];
      say(log, "<strong>Run:</strong> " + [$("t-rf-stir").selectedOptions[0].text, $("t-rf-water").selectedOptions[0].text, $("t-rf-top").selectedOptions[0].text, $("t-rf-heat").selectedOptions[0].text, $("t-rf-level").selectedOptions[0].text].join("; "));
      if (heat === "flame") { say(log, "Stopped before you start: an open flame next to ethanol vapour (flash point 13 °C) can set the bench alight. Use a heating mantle, an aluminium block or a water or oil bath.", "bad"); return; }
      if (top === "stopper") { say(log, "After a few minutes the pressure in the closed apparatus lifts the stopper with a spray of hot solvent (or a joint cracks). Heating a closed system is never allowed: the top of a reflux condenser stays open (a drying tube is fine).", "bad"); return; }
      if (level === "low") { T = 62; events.push("The liquid never boils and no reflux ring forms: the reaction runs at about 62 °C, not 78 °C."); }
      if (stir === "none" && level !== "low") {
        if (rng.random() < 0.8) { lostMix = 0.15; events.push("<span class=\"bad\">Bump!</span> The superheated liquid boils all at once and shoots up the condenser: about 15 % of the mixture is lost. Never add boiling chips to a hot liquid; cool it first."); }
        else events.push("No bump this time, but the boiling is jerky: a superheated liquid can bump at any moment.");
      }
      if (water === "top") { solvent -= 20; events.push("Water in at the top drains straight out: the condenser jacket is half empty and vapour escapes from the top. About 20 mL of solvent lost; the flask runs low."); }
      if (water === "none") { solvent = 0; events.push("<span class=\"bad\">No cooling water:</span> the vapour goes straight out of the condenser into the room. The flask boils dry after about 35 minutes: overheating, charring and a fire risk."); minutes = 35; }
      if (level === "high" && water === "bottom") { solvent -= 12; events.push("The reflux ring climbs to the top of the condenser and vapour escapes: about 12 mL of solvent lost. Turn the heat down until the ring stays in the lower third."); }
      if (level === "gentle" && water === "bottom" && stir !== "none") events.push("<span class=\"good\">Steady reflux:</span> the ring stays in the lower third of the condenser, the liquid boils smoothly at 78 °C.");
      var k78 = 0.05, Ea = 80000, k = k78 * Math.exp(-Ea / OB.R * (1 / (T + 273.15) - 1 / 351.15));
      var conv = 1 - Math.exp(-k * minutes), k25 = k78 * Math.exp(-Ea / OB.R * (1 / 298.15 - 1 / 351.15));
      events.forEach(function (e) { say(log, e); });
      kv($("t-rf-out"), [["temperature of the mixture", T + " °C"], ["time at temperature", minutes + " min"],
        ["conversion", (100 * conv * (1 - lostMix)).toFixed(0) + " %" + (lostMix ? " of the original mixture (some lost)" : "")],
        ["the same 60 min at 25 °C", (100 * (1 - Math.exp(-k25 * 60))).toFixed(1) + " % (rate ratio " + (k78 / k25).toFixed(0) + ")"],
        ["solvent left of 50 mL", Math.max(0, solvent) + " mL"]]);
    });

    /* ======================= extraction ======================= */
    var KD_BA = Math.pow(10, 1.87), KA_BA = Math.pow(10, -4.20), KD_BP = Math.pow(10, 3.18);
    var WATER_SAT = 0.43;  // g of water in 50 mL of wet ether
    var ex;
    function exReset() {
      ex = { BA: 1.000 / C["benzoic acid"].M * 1000, BP: 1.000 / C.benzophenone.M * 1000, water: WATER_SAT, Vorg: 50, aqBA: 0, Vaq: 0, emulsion: false, bound: 0, agent: 0, evaporated: false, washes: 0, mistakes: 0 };
      $("t-ex-log").textContent = "";
      say($("t-ex-log"), "Separatory funnel: 1.00 g benzoic acid and 1.00 g benzophenone in 50 mL diethyl ether. Ether (0.71 g/mL) floats on water.");
      exShow();
    }
    function exShow() {
      var free = Math.max(0, ex.water - ex.bound);
      kv($("t-ex-state"), [
        ["benzoic acid in the ether", (ex.BA * C["benzoic acid"].M / 1000).toFixed(3) + " g"],
        ["benzophenone in the ether", (ex.BP * C.benzophenone.M / 1000).toFixed(3) + " g"],
        ["benzoate in the aqueous extracts", (ex.aqBA * C["benzoic acid"].M / 1000).toFixed(3) + " g in " + ex.Vaq + " mL"],
        ["water dissolved in the ether", (free * 1000).toFixed(0) + " mg" + (ex.agent ? " (drying agent added: " + ex.agent.toFixed(1) + " g, " + (free > 0.005 ? "clumps" : "free-flowing") + ")" : "")],
        ["state", ex.emulsion ? "<span class=\"bad\">emulsion: cloudy middle layer</span>" : ex.evaporated ? "evaporated" : "two clear layers"]]);
      drawFunnel();
    }
    function drawFunnel() {
      var cv = $("t-ex-funnel"), ctx = cv.getContext("2d"), dpr = global.devicePixelRatio || 1, W = cv.clientWidth || 160, H = cv.clientHeight || 220;
      cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.fillStyle = Sim.color("plot-bg"); ctx.fillRect(0, 0, W, H);
      var cx = W / 2, topY = 20, botY = H - 50, wTop = Math.min(110, W * 0.6);
      function xAt(y) { var f = (y - topY) / (botY - topY); return wTop / 2 * (1 - f * 0.85); }
      var mid = topY + (botY - topY) * 0.5, emTop = mid - 10, emBot = mid + 10;
      function band(y0, y1, col) { ctx.fillStyle = col; ctx.beginPath(); ctx.moveTo(cx - xAt(y0), y0); ctx.lineTo(cx + xAt(y0), y0); ctx.lineTo(cx + xAt(y1), y1); ctx.lineTo(cx - xAt(y1), y1); ctx.closePath(); ctx.fill(); }
      if (!ex.evaporated) {
        band(topY + 8, mid, Sim.isDark() ? "#5b4a1e" : "#fff2c4");
        band(mid, botY, Sim.isDark() ? "#1e3d5b" : "#cfe6fb");
        if (ex.emulsion) band(emTop, emBot, Sim.isDark() ? "#777" : "#ddd");
      }
      ctx.strokeStyle = Sim.color("ink"); ctx.lineWidth = 1.5;
      ctx.beginPath(); ctx.moveTo(cx - wTop / 2, topY); ctx.lineTo(cx - xAt(botY), botY); ctx.lineTo(cx - 3, botY + 30); ctx.moveTo(cx + wTop / 2, topY); ctx.lineTo(cx + xAt(botY), botY); ctx.lineTo(cx + 3, botY + 30); ctx.stroke();
      ctx.fillStyle = Sim.color("ink"); ctx.font = "11px " + getComputedStyle(document.body).fontFamily; ctx.textAlign = "left";
      if (!ex.evaporated) {
        ctx.fillText("ether (top)", cx + wTop / 2 - 10, topY + 30 > mid - 4 ? mid - 4 : topY + 30);
        ctx.fillText("aqueous", cx + xAt(mid + 30) + 6, mid + 30);
      }
    }
    function pHof(reagent) { return reagent === "bicarb" ? 8.3 : reagent === "naoh" ? 13 : 3.0; }
    $("t-ex-wash").addEventListener("click", function () {
      var log = $("t-ex-log");
      if (ex.evaporated) { say(log, "The ether has been evaporated. Reset to start again."); return; }
      if (ex.emulsion) { say(log, "The emulsion is still there: you cannot see the boundary. Wait, swirl gently, or wash with brine.", "warn"); return; }
      if (ex.agent > 0) { say(log, "You have already added drying agent: filter it off first (reset to start again).", "warn"); return; }
      var reagent = $("t-ex-reagent").value, V = Math.max(1, parseFloat($("t-ex-vol").value) || 15), vig = $("t-ex-shake").value === "vigorous", vent = $("t-ex-vent").checked, keep = $("t-ex-keep").value;
      var names = { water: "water", bicarb: "saturated NaHCO₃ (pH 8.3)", naoh: "1 M NaOH (pH 13)", brine: "brine (saturated NaCl)" };
      var h = Math.pow(10, -pHof(reagent)), D = KD_BA * h / (h + KA_BA);
      var keepBA = D * ex.Vorg / (D * ex.Vorg + V), keepBP = KD_BP * ex.Vorg / (KD_BP * ex.Vorg + V) * 0.995;
      var moved = ex.BA * (1 - keepBA);
      ex.BA *= keepBA; ex.BP *= keepBP; ex.aqBA += moved; ex.Vaq += V; ex.washes++;
      var msg = "Wash " + ex.washes + ": " + V + " mL " + names[reagent] + ", " + (vig ? "shaken vigorously" : "inverted gently") + ". D(benzoic acid) = " + Sim.sig(D, 2) + ": " + (100 * keepBA).toFixed(1) + " % of it stays in the ether.";
      say(log, msg);
      if (reagent === "bicarb" && moved > 0.3) say(log, "CO₂ fizzes as the acid is neutralised" + (vent ? "; you vent after every few inversions." : "."));
      if (!vent) {
        var loss = reagent === "bicarb" && moved > 0.3 ? 0.10 : 0.03;
        ex.BA *= 1 - loss; ex.BP *= 1 - loss;
        say(log, "<strong>No venting:</strong> " + (loss > 0.05 ? "CO₂ and ether vapour blow the stopper out; a spray of ether (extremely flammable, H224) hits the hood. " : "ether vapour builds up and hisses past the stopper when you open it. ") + (100 * loss).toFixed(0) + " % of the organic layer lost. Invert, point the tip into the hood and open the tap after the first gentle shake.", "bad");
      }
      if (vig && (reagent === "bicarb" || reagent === "naoh") && rng.random() < 0.6) { ex.emulsion = true; say(log, "Vigorous shaking with base has made an emulsion: a cloudy band hides the boundary.", "warn"); }
      else if (vig && reagent === "water" && rng.random() < 0.15) { ex.emulsion = true; say(log, "A small emulsion has formed at the boundary.", "warn"); }
      if (reagent === "naoh") say(log, "NaOH works here, but it would hydrolyse an ester (aspirin, ethyl acetate); bicarbonate is the gentle choice.", "muted");
      ex.water = reagent === "brine" ? WATER_SAT * 0.3 : WATER_SAT;
      if (reagent === "brine") say(log, "Brine pulls most of the dissolved water out of the ether (about 70 %).");
      if (keep === "bottom") {
        ex.BA *= 0.97; ex.BP *= 0.97; ex.mistakes++;
        say(log, "<strong>Wrong layer:</strong> you ran the bottom layer into your product flask and poured the ether into the extracts beaker. Ether is 0.71 g/mL and floats on water: the top layer is organic. Because you kept and labelled every layer, the drop test shows the mistake and you swap them back, losing about 3 %.", "bad");
      }
      exShow();
    });
    $("t-ex-drop").addEventListener("click", function () { say($("t-ex-log"), "Drop test: a few drops of water fall through the top layer and merge with the bottom one. The bottom layer is aqueous; the top layer is the ether."); });
    $("t-ex-wait").addEventListener("click", function () {
      if (!ex.emulsion) { say($("t-ex-log"), "Nothing to wait for: the layers are sharp."); return; }
      if (rng.random() < 0.5) { ex.emulsion = false; say($("t-ex-log"), "After 10 minutes and gentle swirling the emulsion has broken."); }
      else say($("t-ex-log"), "Still cloudy after 10 minutes. Try brine.", "warn");
      exShow();
    });
    $("t-ex-brine").addEventListener("click", function () {
      if (!ex.emulsion) { say($("t-ex-log"), "No emulsion. (A brine wash is still a good last wash: choose brine in the wash menu.)"); return; }
      ex.emulsion = false; ex.Vaq += 5; say($("t-ex-log"), "5 mL of brine: the denser, more polar water layer pushes the organic molecules out and the emulsion breaks."); exShow();
    });
    $("t-ex-dry").addEventListener("click", function () {
      if (ex.evaporated) return;
      if (ex.emulsion) { say($("t-ex-log"), "Separate the layers first.", "warn"); return; }
      var agent = $("t-ex-agent").value, cap = agent === "MgSO4" ? 0.25 : 0.2;
      ex.agent += 0.5; ex.bound += 0.5 * cap; ex.BP *= 0.997;
      var free = Math.max(0, ex.water - ex.bound);
      say($("t-ex-log"), "Added 0.5 g anhydrous " + (agent === "MgSO4" ? "MgSO₄" : "Na₂SO₄") + ". " + (free > 0.005 ? "It clumps on the bottom; the solution is still slightly cloudy. Add more." : "New crystals stay free-flowing and swirl like a snow globe; the solution is clear. Dry.") + (agent === "Na2SO4" ? " (Na₂SO₄ is slower: swirl and give it a few minutes.)" : ""));
      exShow();
    });
    $("t-ex-evap").addEventListener("click", function () {
      if (ex.evaporated) return;
      if (ex.emulsion) { say($("t-ex-log"), "Separate the layers first.", "warn"); return; }
      ex.BP *= 0.995; ex.evaporated = true;
      var free = Math.max(0, ex.water - ex.bound), mBP = ex.BP * C.benzophenone.M / 1000, mBA = ex.BA * C["benzoic acid"].M / 1000;
      var wet = free > 0.005;
      say($("t-ex-log"), "Rotary evaporator: " + (mBP + mBA + free).toFixed(3) + " g of residue. Benzophenone recovery " + (100 * mBP).toFixed(1) + " %, containing " + (1000 * mBA).toFixed(0) + " mg benzoic acid. " + (wet ? "<span class=\"bad\">Wet product:</span> droplets of water and a cloudy oil that will not crystallise; you stopped the drying agent while it still clumped." : "<span class=\"good\">Dry:</span> a clear oil that crystallises on standing (mp 48 °C)."), wet ? "warn" : "good");
      exShow();
    });
    $("t-ex-acid").addEventListener("click", function () {
      if (ex.aqBA <= 0) { say($("t-ex-log"), "The aqueous extracts hold no benzoate yet."); return; }
      var Vaq = ex.Vaq, q = Vaq / (KD_BA * 20 + Vaq), rec = ex.aqBA * (1 - q * q);
      say($("t-ex-log"), "Acidify the combined aqueous extracts (" + Vaq + " mL) to pH 1 with HCl: benzoic acid comes back to the neutral form (D ≈ 74). Two 20 mL ether extractions recover " + (rec * C["benzoic acid"].M / 1000).toFixed(3) + " g, " + (100 * rec * C["benzoic acid"].M / 1000).toFixed(1) + " % of the original 1.00 g.");
    });
    $("t-ex-reset").addEventListener("click", exReset);
    exReset();

    /* ======================= recrystallisation ======================= */
    var SOLV = {
      water: { name: "water", bp: 100, hot: 0.050, cold: 0.0054, rt: 0.0075 },
      ethanol: { name: "ethanol", bp: 78, hot: 1.0, cold: 0.29, rt: 0.29 },
      hexane: { name: "hexane", bp: 69, hot: 0.003, cold: 0.0005, rt: 0.0005 },
      xylene: { name: "xylenes", bp: 140, hot: 0.25, cold: 0.02, rt: 0.025 }
    };
    var rcRuns = [];
    $("t-rc-go").addEventListener("click", function () {
      var sv = SOLV[$("t-rc-solvent").value], V = Math.max(1, parseFloat($("t-rc-vol").value) || 40), hot = $("t-rc-hot").checked;
      var cool = $("t-rc-cool").value, wash = $("t-rc-wash").value, dry = $("t-rc-dry").value === "dry";
      var mA = 2.00, mImp = 0.15, notes = [];
      var Vmin = mA / sv.hot, dissolved = Math.min(mA, sv.hot * V), undissolved = mA - dissolved;
      if (undissolved > 0.01) notes.push("Not all of it dissolves at the boiling point: " + undissolved.toFixed(2) + " g of acetanilide stays solid (you need at least " + Vmin.toFixed(0) + " mL of boiling " + sv.name + ").");
      var oiled = sv.bp > C.acetanilide.mp && dissolved > 0.1;
      if (oiled) notes.push("<span class=\"bad\">Oiling out:</span> " + sv.name + " boils at " + sv.bp + " °C, above the melting point of acetanilide (114 °C). The compound melts in the hot solvent and separates as an oil, which traps the impurity and sets into a sticky lump.");
      var crystals = dissolved - (cool === "rt" ? sv.rt : sv.cold) * V;
      if (crystals < 0) crystals = 0;
      if (hot) {
        if (V < 1.08 * Vmin && sv.hot < 0.5) { crystals *= 0.94; notes.push("Hot filtration with barely enough solvent: crystals form in the funnel stem and on the paper (about 6 % lost). A 10 % excess avoids it."); }
        else notes.push("Hot gravity filtration removes the insoluble dust.");
        if (undissolved > 0) notes.push("The undissolved acetanilide is filtered off with the dust and lost.");
      } else crystals += undissolved;
      var trap = oiled ? 1 : cool === "ice" ? 0.35 : cool === "rt" ? 0.06 : 0.03;
      var liq = wash === "none" ? 0.10 : wash === "warm" ? 0.02 : 0.03;
      var impKept = mImp * Math.min(1, trap + liq);
      if (wash === "ice") crystals -= 6 * sv.cold;
      if (wash === "warm") { crystals -= 6 * sv.hot * 0.5; notes.push("Warm wash solvent redissolves part of the crystals."); }
      crystals = Math.max(0, crystals * 0.99);
      if (crystals < 0.02) notes.push("Almost nothing crystallises: acetanilide is far too soluble in cold " + sv.name + ".");
      if (sv.hot < 0.01) notes.push("Acetanilide hardly dissolves even in boiling " + sv.name + ": wrong solvent.");
      var look = oiled ? "a sticky, off-white lump" : cool === "ice" ? "many small crystals, faintly coloured" : "large, colourless plates";
      var comp = { acetanilide: crystals / C.acetanilide.M * 1000, "side products": impKept / C["side products"].M * 1000 };
      var water = dry ? 0 : 0.3 * crystals;
      var mp = crystals > 0.02 ? OB.meltRange(comp, "acetanilide", sv.name === "water" ? water : 0, 2, rng) : null;
      var rec = 100 * crystals / mA;
      var row = { solvent: sv.name, V: V, hot: hot ? "yes" : "no", cool: cool, wash: wash, dry: dry ? "yes" : "no", mass: crystals + impKept + (sv.name === "water" ? water : 0), rec: rec, mp: mp ? mp.lo + "–" + mp.hi : "—", look: look };
      rcRuns.push(row);
      var tb = $("t-rc-runs").querySelector("tbody");
      tb.appendChild(tr([rcRuns.length, row.solvent, row.V, row.hot, row.cool, row.wash, row.dry, row.mass.toFixed(2), rec.toFixed(0), row.mp, row.look]));
      kv($("t-rc-out"), [["minimum boiling solvent", Vmin.toFixed(1) + " mL"], ["best possible recovery with " + V + " mL", (100 * Math.max(0, (mA - sv.cold * V) / mA)).toFixed(0) + " %"],
        ["acetanilide recovered", crystals.toFixed(2) + " g (" + rec.toFixed(0) + " %)"], ["melting range (2 °C/min)", mp ? mp.lo + "–" + mp.hi + " °C (pure 114 °C)" : "—"],
        ["appearance", look]]);
      var log = $("t-rc-log"); log.textContent = ""; notes.forEach(function (n) { say(log, n); });
      if (!dry) say(log, "Weighed wet: the mass includes water, so the 'yield' is too high and the melting point low.", "warn");
    });
    Sim.exportCSV($("t-rc-csv"), "recrystallisation_runs.csv", function () {
      return { header: ["run", "solvent", "volume_mL", "hot_filtration", "cooling", "wash", "dried", "mass_g", "recovery_pct", "mp_C", "appearance"],
        rows: rcRuns.map(function (r, i) { return [i + 1, r.solvent, r.V, r.hot, r.cool, r.wash, r.dry, r.mass.toFixed(3), r.rec.toFixed(1), r.mp, r.look]; }) };
    });

    /* ======================= distillation ======================= */
    var VM = { cyclohexane: 84.16 / 0.7781, toluene: 92.14 / 0.8669 }, P = 1.01325, ds;
    var dsPlot = Sim.plot($("t-ds-plot"), { xLabel: "volume collected / mL", yLabel: "head T / °C or % cyclohexane", legend: true });
    function bubbleT(x) {
      var lo = 330, hi = 400;
      for (var i = 0; i < 60; i++) { var m = (lo + hi) / 2, f = x * OB.antoineBar("cyclohexane", m) + (1 - x) * OB.antoineBar("toluene", m) - P; if (f > 0) hi = m; else lo = m; }
      return (lo + hi) / 2;
    }
    function dewT(y) {
      var lo = 330, hi = 400;
      for (var i = 0; i < 60; i++) { var m = (lo + hi) / 2, f = y / OB.antoineBar("cyclohexane", m) + (1 - y) / OB.antoineBar("toluene", m) - 1 / P; if (f < 0) hi = m; else lo = m; }
      return (lo + hi) / 2;
    }
    function dsReset() {
      var n = 50 / (VM.cyclohexane + VM.toluene);
      ds = { n1: n, n2: n, V: 0, fr: [], pts: [], done: false };
      $("t-ds-table").querySelector("tbody").textContent = "";
      $("t-ds-log").textContent = "";
      say($("t-ds-log"), "Pot: 50 mL of an equimolar cyclohexane–toluene mixture (" + (ds.n1 * 1000).toFixed(0) + " mmol of each), boiling chips added.");
      dsDraw();
    }
    function nEff() {
      var plates = { simple: 0, vigreux: 3, packed: 6 }[$("t-ds-app").value];
      return 1 + plates * ($("t-ds-rate").value === "slow" ? 1 : 0.4);
    }
    function distil(Vwant) {
      var N = nEff(), therm = $("t-ds-therm").value, step = 0.25, frac = { V0: ds.V, n1: 0, n2: 0, Tmin: Infinity, Tmax: -Infinity };
      while (Vwant > 1e-9) {
        var x = ds.n1 / (ds.n1 + ds.n2), Tb = bubbleT(x), alpha = OB.antoineBar("cyclohexane", Tb) / OB.antoineBar("toluene", Tb), y = x;
        for (var k = 0; k < Math.floor(N); k++) y = alpha * y / (1 + (alpha - 1) * y);
        var fr = N - Math.floor(N); if (fr > 0) { var y2 = alpha * y / (1 + (alpha - 1) * y); y = y + fr * (y2 - y); }
        var dV = Math.min(step, Vwant), dn = dV / (y * VM.cyclohexane + (1 - y) * VM.toluene);
        var d1 = Math.min(ds.n1, dn * y), d2 = Math.min(ds.n2, dn - d1);
        ds.n1 -= d1; ds.n2 -= d2; frac.n1 += d1; frac.n2 += d2; ds.V += dV; Vwant -= dV;
        var Th = dewT(y) - 273.15;
        var read = therm === "high" ? Th - 4 : therm === "low" ? 0.5 * (Th + Tb - 273.15) + 1 : Th;
        read += rng.normal(0, 0.15);
        frac.Tmin = Math.min(frac.Tmin, read); frac.Tmax = Math.max(frac.Tmax, read);
        ds.pts.push([ds.V, read, 100 * y]);
        if ((ds.n1 + ds.n2) * 0.5 * (VM.cyclohexane + VM.toluene) < 3) break;
      }
      return frac;
    }
    function dsDraw() {
      dsPlot.draw([{ data: ds.pts.map(function (p) { return [p[0], p[1]]; }), color: "s2", label: "head temperature / °C" },
        { data: ds.pts.map(function (p) { return [p[0], p[2]]; }), color: "s1", label: "distillate / % cyclohexane (mol)" }], { xMin: 0, xMax: 50, yMin: 40, yMax: 120 });
    }
    $("t-ds-frac").addEventListener("click", function () {
      if (ds.done) { say($("t-ds-log"), "Stopped: start a new distillation."); return; }
      var left = (ds.n1 + ds.n2) * 0.5 * (VM.cyclohexane + VM.toluene);
      if (left < 8) { say($("t-ds-log"), "Only about " + left.toFixed(0) + " mL left in the pot. Stop here: never distil to dryness.", "warn"); return; }
      var f = distil(5), xc = f.n1 / (f.n1 + f.n2);
      ds.fr.push({ V0: f.V0, V1: ds.V, Tmin: f.Tmin, Tmax: f.Tmax, xc: xc });
      $("t-ds-table").querySelector("tbody").appendChild(tr([ds.fr.length, f.V0.toFixed(0) + "–" + ds.V.toFixed(0), f.Tmin.toFixed(1) + "–" + f.Tmax.toFixed(1), (100 * xc).toFixed(1)]));
      if (ds.fr.length === 1) say($("t-ds-log"), "First fraction: " + (100 * xc).toFixed(0) + " % cyclohexane with " + nEff().toFixed(1) + " equilibrium stages" + ($("t-ds-app").value === "simple" ? " (simple distillation: one stage, the pot)." : "."));
      if ($("t-ds-therm").value !== "level") say($("t-ds-log"), "The thermometer bulb is not level with the side arm, so it does not read the temperature of the vapour that is leaving.", "warn");
      dsDraw();
    });
    $("t-ds-dry").addEventListener("click", function () {
      if (ds.done) return;
      distil(200); ds.done = true;
      say($("t-ds-log"), "<strong>Distilled to dryness.</strong> The last drops overheat the residue; with ethers, concentrated peroxides can explode. Always leave a little liquid in the pot.", "bad");
      dsDraw();
    });
    $("t-ds-reset").addEventListener("click", dsReset);
    Sim.exportCSV($("t-ds-csv"), "distillation_fractions.csv", function () {
      return { header: ["fraction", "from_mL", "to_mL", "head_T_min_C", "head_T_max_C", "cyclohexane_mol_pct"], rows: ds.fr.map(function (f, i) { return [i + 1, f.V0.toFixed(1), f.V1.toFixed(1), f.Tmin.toFixed(2), f.Tmax.toFixed(2), (100 * f.xc).toFixed(2)]; }) };
    });
    dsReset();

    /* ======================= TLC ======================= */
    var tlcLast = null;
    function tlcRun() {
      var t = parseFloat($("t-tlc-time").value), phi = parseFloat($("t-tlc-eluent").value), big = $("t-tlc-spot").value === "big";
      var c = 1 - Math.exp(-0.03 * t);
      var lanes = [{ label: "SM", comp: { benzoin: 1 } }, { label: "co", comp: { benzoin: 1 + (1 - c), benzil: c } }, { label: "RM", comp: { benzoin: 1 - c, benzil: c } }];
      var r = OB.tlc($("t-tlc-canvas"), lanes, phi, "uv", Sim.rng(seed + Math.round(t * 7 + phi * 100)), { big: big, noFront: !$("t-tlc-front").checked });
      tlcLast = r;
      var tb = $("t-tlc-table").querySelector("tbody"); tb.textContent = "";
      r.spots.forEach(function (s) { tb.appendChild(tr([s.lane, s.dist.toFixed(1), $("t-tlc-front").checked ? (s.dist / r.front).toFixed(2) : "front not marked", s.streak ? "streak" : ""])); });
      var note = $("t-tlc-note");
      note.textContent = ($("t-tlc-front").checked ? "Front: " + r.front.toFixed(0) + " mm from the start line. " : "You did not mark the front before it evaporated: no Rf can be calculated. ") +
        (big ? "Overloaded spots streak and run into each other. " : "") + (c > 0.995 ? "" : "Is starting material still present in the RM lane?");
    }
    $("t-tlc-run").addEventListener("click", tlcRun);
    Sim.exportCSV($("t-tlc-csv"), "tlc_spots.csv", function () {
      return { header: ["lane", "distance_mm", "front_mm", "Rf"], rows: (tlcLast ? tlcLast.spots : []).map(function (s) { return [s.lane, s.dist.toFixed(1), tlcLast.front.toFixed(1), (s.dist / tlcLast.front).toFixed(3)]; }) };
    });

    /* ======================= melting point ======================= */
    var mpRows = [];
    var SAMPLES = {
      pure: { label: "pure benzoic acid", comp: { "benzoic acid": 1 }, water: 0 },
      impure: { label: "benzoic acid with 5 mol% impurity", comp: { "benzoic acid": 0.95, "side products": 0.05 }, water: 0 },
      wet: { label: "benzoic acid, not dried", comp: { "benzoic acid": 1 }, water: 0.010 },
      x: { label: "white solid X", comp: { "2-naphthol": 1 }, water: 0 },
      mixx: { label: "X + authentic benzoic acid (1 : 1)", comp: { "2-naphthol": 0.5, "benzoic acid": 0.5 }, water: 0 },
      mixsame: { label: "your benzoic acid + authentic benzoic acid (1 : 1)", comp: { "benzoic acid": 1 }, water: 0 }
    };
    $("t-mp-go").addEventListener("click", function () {
      var smp = SAMPLES[$("t-mp-sample").value], rate = parseFloat($("t-mp-rate").value), loose = $("t-mp-pack").value === "loose";
      var comp = {}; Object.keys(smp.comp).forEach(function (k) { comp[k] = smp.comp[k] * 1000 / C[k].M * 0.122; });
      var main = Object.keys(smp.comp)[0];
      var r = OB.meltRange(comp, main, smp.water, rate, rng, { loose: loose });
      mpRows.push({ label: smp.label, rate: rate, pack: loose ? "10 mm, loose" : "2–3 mm, packed", lo: r.lo, hi: r.hi });
      $("t-mp-table").querySelector("tbody").appendChild(tr([mpRows.length, smp.label, rate, loose ? "10 mm, loose" : "2–3 mm", r.lo + "–" + r.hi, (r.hi - r.lo) + " °C"]));
      var note = "";
      if (rate >= 5) note = "Fast heating: the thermometer lags behind the sample, so both readings come out high.";
      if (smp === SAMPLES.mixx) note = "The mixture melts far lower and over a wide range: X is a different compound (it is 2-naphthol, mp 121–123 °C), even though it melts like benzoic acid on its own.";
      if (smp === SAMPLES.mixsame) note = "Same compound: the mixture melts sharply at the same temperature.";
      if (smp === SAMPLES.wet) note = "Water acts as an impurity: dry the sample to constant mass and measure again.";
      $("t-mp-note").textContent = note;
    });
    Sim.exportCSV($("t-mp-csv"), "melting_points.csv", function () {
      return { header: ["run", "sample", "rate_C_per_min", "packing", "onset_C", "clear_C"], rows: mpRows.map(function (r, i) { return [i + 1, r.label, r.rate, r.pack, r.lo, r.hi]; }) };
    });

    return { redraw: function () { drawFunnel(); dsDraw(); if (tlcLast) tlcRun(); }, tlcRun: tlcRun };
  };
})(typeof window !== "undefined" ? window : this);
