/* organic-bench, part 3: the syntheses (lessons 24.4-24.6). Defines global OB_SYN = {aspirin, sn2, grignard,
 * aldol, multistep}. Uses ob-core.js (OB). Each synthesis is a list of steps; each step offers choices and
 * changes the state st.sp ({compound: mmol}) and st.water (g of water in the product).
 *
 * Amounts and densities follow lessons 24.4 and 24.5 (PubChem densities at 20 C: acetic anhydride 1.082,
 * 1-butanol 0.810, bromobenzene 1.495, benzaldehyde 1.046, acetone 0.785 g/mL).
 * Rates, side-product fractions, solubility losses and recoveries are MODEL values, chosen so that a careful
 * run lands where the lessons say a teaching lab lands (aspirin 70-80 % after recrystallisation; 1-bromobutane
 * 60-75 %; triphenylmethanol 60-80 %; dibenzalacetone near 110 C; benzoin 58 %, benzil 84 %, benzilic acid
 * 75 %) and so that each classic mistake has its classic consequence. They are not kinetic measurements.
 * Aspirin solubility in water about 3.3 g/L at 25 C (PubChem 2244); salicylic acid about 2.2 g/L at 20 C
 * (PubChem 338). Water destroying a Grignard reagent: 18.015 mg per mmol (lesson 24.5).
 */
(function (global) {
  "use strict";
  var C = OB.C;
  function g(name, mmol) { return mmol * C[name].M / 1000; }
  function mm(name, grams) { return grams / C[name].M * 1000; }
  function dryMass(st) { var m = 0; Object.keys(st.sp).forEach(function (k) { if (st.sp[k] > 0 && k !== "water") m += g(k, st.sp[k]); }); return m; }
  function scaleAll(st, f) { Object.keys(st.sp).forEach(function (k) { st.sp[k] *= f; }); st.water *= f; }
  function wetCake(st) { st.water = 0.38 * dryMass(st); st.isolated = true; }
  function sel(id, label, options, def) { return { id: id, type: "select", label: label, options: options, def: def }; }
  function num(id, label, min, max, step, def) { return { id: id, type: "number", label: label, min: min, max: max, step: step, def: def }; }
  function chk(id, label, def) { return { id: id, type: "check", label: label, def: def }; }
  var DRY = sel("dry", "Drying", [["dry", "dry to constant mass (desiccator overnight, weigh until two weighings agree)"], ["air", "air-dry on the filter for 10 minutes"], ["wet", "weigh it straight from the filter"]], "dry");
  function doDry(st, ch, say) {
    var m = dryMass(st);
    if (ch.dry === "dry") { st.water = 0.002 * m; say("Dried to constant mass: two weighings an hour apart agree within 0.01 g."); }
    else if (ch.dry === "air") { st.water = 0.12 * m; say("Air-dried for 10 minutes: it looks dry but still holds water.", "warn"); }
    else { st.water = 0.38 * m; say("Weighed straight from the filter: the mass includes the water that wets the crystals.", "warn"); }
    st.isolated = true;
  }
  function recrystChoice(id, label, opts) { return sel(id, label, opts, opts[1][0]); }

  /* ============================== ASPIRIN ============================== */
  var aspirin = {
    key: "aspirin", title: "Aspirin from salicylic acid", product: "aspirin", sm: "salicylic acid", eluent: 0.5,
    intro: "Salicylic acid (2.00 g, 14.48 mmol) is acetylated by excess acetic anhydride with a few drops of 85 % phosphoric acid, then quenched with water, crystallised, filtered, recrystallised and dried. Theoretical yield 2.61 g; atom economy 75.0 % (acetic acid is the by-product). Mechanism: acid-catalysed nucleophilic acyl substitution of the anhydride by the phenol O–H.",
    cards: [["salicylic acid", "2.00 g (14.48 mmol), M = 138.12", "H302 harmful if swallowed, H318 serious eye damage, H361 suspected of damaging fertility"],
      ["acetic anhydride", "5.0 mL = 5.41 g (53.0 mmol, 3.7 equiv.), d = 1.082 g/mL", "H226 flammable, H302, H314 severe skin burns and eye damage, vapour attacks eyes and lungs"],
      ["phosphoric acid 85 %", "5 drops (catalyst)", "H290 corrosive to metals, H314"],
      ["aspirin (product)", "M = 180.16, mp 135 °C (rapid heating)", "H302"]],
    init: function (st) { st.theo = mm("salicylic acid", 2.00); st.sp = {}; st.water = 0; },
    steps: [
      { title: "Weigh the reagents into the flask", why: "Excess anhydride is cheap, acts as the solvent and drives the reaction to completion; the acid catalyses it. Water destroys acetic anhydride, so everything must be dry.",
        controls: [sel("sa", "Salicylic acid", [["dry", "dry, from a closed bottle"], ["wet", "left open on a humid bench (about 15 % water)"]], "dry"),
          sel("glass", "Flask", [["dry", "clean and dry"], ["wet", "just rinsed, still wet inside"]], "dry"),
          sel("vol", "Acetic anhydride", [["2", "2.0 mL (1.5 equiv.)"], ["3", "3.0 mL (2.2 equiv.)"], ["5", "5.0 mL (3.7 equiv.)"], ["7", "7.0 mL (5.1 equiv.)"]], "5"),
          sel("bottle", "Anhydride bottle", [["fresh", "fresh, recently opened"], ["old", "old, opened many times (partly hydrolysed)"]], "fresh"),
          sel("cat", "Catalyst", [["yes", "5 drops of 85 % H₃PO₄"], ["no", "none"]], "yes")],
        run: function (st, ch, rng, say) {
          var waterSA = ch.sa === "wet" ? 0.30 : 0, nSA = mm("salicylic acid", 2.00 - waterSA);
          var vol = parseFloat(ch.vol), nAn = vol * 1.082 / 102.09 * 1000, ac = 0;
          if (ch.bottle === "old") { ac += 2 * 0.3 * nAn; nAn *= 0.7; }
          var water = (waterSA + (ch.glass === "wet" ? 0.25 : 0)) / 18.015 * 1000, used = Math.min(water, nAn);
          nAn -= used; ac += 2 * used;
          st.sp = { "salicylic acid": nSA, "acetic acid": ac }; st.nAn = nAn; st.cat = ch.cat === "yes";
          say("Weighed 2.00 g of salicylic acid" + (waterSA ? " (but 0.30 g of that is water: only " + (2.00 - waterSA).toFixed(2) + " g of acid)" : "") + " and " + vol.toFixed(1) + " mL of anhydride. Theoretical yield on the weighed mass: " + g("aspirin", st.theo).toFixed(2) + " g.");
          if (used > 0) say("Water destroyed " + used.toFixed(1) + " mmol of anhydride, giving acetic acid.", "warn");
          say("Anhydride left for the reaction: " + nAn.toFixed(1) + " mmol = " + (nAn / nSA).toFixed(2) + " equivalents.");
        } },
      { title: "Heat the mixture", why: "At 70–80 °C the acetylation is fast, and the bath stays far below the anhydride's boiling point (139 °C), so no reflux condenser is needed. Too hot or too long gives coloured by-products.",
        controls: [sel("T", "Water bath", [["25", "no heating (room temperature)"], ["50", "50 °C"], ["75", "75 °C"], ["95", "95 °C (boiling water bath)"]], "75"),
          sel("t", "Time", [["5", "5 min"], ["10", "10 min"], ["15", "15 min"], ["30", "30 min"]], "15")],
        run: function (st, ch, rng, say) {
          var T = parseFloat(ch.T), t = parseFloat(ch.t), nSA = st.sp["salicylic acid"];
          var k = (st.cat ? 0.20 : 0.010) * Math.exp(-60000 / OB.R * (1 / (T + 273.15) - 1 / 348.15));
          var conv = Math.min(1 - Math.exp(-k * t), Math.min(1, st.nAn / nSA) * 0.995);
          var bp = Math.min(0.1, 0.004 * (t / 15) * Math.exp(0.08 * (T - 75))) * nSA;
          var nA = Math.max(0, nSA * conv - bp);
          st.sp.aspirin = nA; st.sp["salicylic acid"] = nSA * (1 - conv); st.sp["ester by-products"] = bp / 2; st.sp["acetic acid"] += nSA * conv;
          st.nAn -= nSA * conv;
          say("After " + t + " min at " + T + " °C about " + (100 * conv).toFixed(0) + " % of the salicylic acid is acetylated." + (st.cat ? "" : " Without the acid catalyst the reaction is slow."));
          if (bp / nSA > 0.015) say("The mixture has turned yellow-tan: coloured ester by-products from overheating.", "warn");
          if (st.nAn < 0.2) say("The anhydride ran out: it limited the reaction.", "warn");
        } },
      { title: "Quench the excess anhydride", why: "Water destroys the excess acetic anhydride (an exothermic reaction that gives acetic acid vapour, so in the hood) and makes aspirin insoluble.",
        controls: [sel("q", "Quench", [["careful", "remove from heat, cool a little, add 2 mL cold water dropwise, then 20 mL cold water"], ["hot", "pour 20 mL of water straight into the hot flask"], ["none", "skip the quench and cool straight in ice"]], "careful")],
        run: function (st, ch, rng, say) {
          if (ch.q === "careful") say("The first drops hiss and give off hot acetic acid vapour; then the rest of the water goes in calmly. Crystals start to form.");
          if (ch.q === "hot") { scaleAll(st, 0.92); st.oiled = true; say("The water boils on contact with the hot anhydride and spatters: some mixture is lost (about 8 %), and the product separates as an oil that sets into lumps.", "bad"); }
          if (ch.q === "none") { st.anLeft = true; say("Excess anhydride is still there: the product comes out sticky and smells sharply of anhydride and vinegar.", "warn"); }
          st.sp["acetic acid"] += 2 * Math.max(0, st.nAn); st.nAn = 0;
        } },
      { title: "Crystallise and vacuum-filter", why: "Aspirin is only slightly soluble in ice-cold water; filtering warm loses product in the filtrate. A wash with a little ice water removes acetic and phosphoric acid without dissolving the crystals.",
        controls: [sel("cool", "Cooling", [["ice", "ice bath for 10 min, scratch the glass if needed"], ["warm", "filter while still warm (about 40 °C)"]], "ice"),
          sel("wash", "Wash on the Büchner funnel", [["ice", "2 × 5 mL ice-cold water"], ["warm", "2 × 5 mL warm water"], ["none", "no wash"]], "ice")],
        run: function (st, ch, rng, say) {
          scaleAll(st, 0.94);
          var lossA = ch.cool === "ice" ? 0.03 : 0.18, lossSA = ch.cool === "ice" ? 0.05 : 0.15;
          if (ch.cool === "warm") { st.sp.aspirin *= 0.90; say("Filtered warm: crystallisation was not complete and more aspirin stays dissolved in the filtrate.", "warn"); }
          if (ch.wash === "warm") lossA += 0.10;
          st.sp.aspirin = Math.max(0, st.sp.aspirin - mm("aspirin", lossA));
          if (!st.oiled) st.sp["salicylic acid"] = Math.max(0, st.sp["salicylic acid"] - mm("salicylic acid", lossSA));
          var keepAc = ch.wash === "none" ? 0.05 : 0.005;
          if (st.anLeft) keepAc = 0.04;
          st.sp["acetic acid"] = mm("acetic acid", keepAc * dryMass({ sp: { aspirin: st.sp.aspirin } }));
          wetCake(st);
          say("Collected the crystals on the Büchner funnel" + (ch.wash === "none" ? "; unwashed, they smell of vinegar and are acidic." : ch.wash === "warm" ? "; the warm wash redissolved some product." : " and washed them with ice water."));
        } },
      { title: "Dry the crude product (then check it)", why: "Wet crystals give a yield over 100 % and a low, broad melting point. Use 'Check the product now' to record the crude mass, melting range and FeCl₃ test before you recrystallise.",
        controls: [DRY], run: function (st, ch, rng, say) { doDry(st, ch, say); } },
      { title: "Recrystallise", why: "Salicylic acid stays in the mother liquor. Dissolve quickly in a little warm ethanol, add warm water until just cloudy and cool slowly. Long boiling in water hydrolyses aspirin back to salicylic acid.",
        controls: [recrystChoice("rc", "Recrystallisation", [["skip", "skip it"], ["slow", "minimum warm ethanol, warm water to cloudiness, cool slowly, then ice"], ["fast", "same, but straight into ice"], ["boil", "boil in water for 15 min until it all dissolves, then cool"]])],
        run: function (st, ch, rng, say) {
          if (ch.rc === "skip") { say("No recrystallisation."); return; }
          var s = st.sp;
          if (ch.rc === "boil") { var h = 0.08 * s.aspirin; s.aspirin -= h; s["salicylic acid"] += h; say("15 min of boiling water hydrolysed about 8 % of the aspirin back to salicylic acid.", "warn"); }
          var f = { slow: [0.83, 0.04, 0.2], fast: [0.86, 0.25, 0.4], boil: [0.80, 0.4, 0.3] }[ch.rc];
          s.aspirin *= f[0]; s["salicylic acid"] *= f[1]; s["ester by-products"] *= f[2]; s["acetic acid"] = 0;
          st.look = ch.rc === "fast" ? "small white crystals" : "white needles";
          wetCake(st);
          say("Recrystallised and filtered: " + (ch.rc === "slow" ? "slow cooling grew clean needles; most salicylic acid stayed in the mother liquor." : ch.rc === "fast" ? "crash cooling gave fine crystals that trapped more salicylic acid." : "crystals formed on cooling."));
        } },
      { title: "Dry the final product", why: "Only a pure, dry product gives an honest yield.", controls: [DRY], run: function (st, ch, rng, say) { doDry(st, ch, say); } }
    ],
    tests: function (st, x) {
      var xs = x["salicylic acid"] || 0, out = [];
      out.push(["FeCl₃ test (phenol)", xs > 0.05 ? "deep violet: much salicylic acid" : xs > 0.01 ? "violet: salicylic acid present" : xs > 0.003 ? "faint violet: a trace of salicylic acid" : "yellow (negative): no free phenol"]);
      if ((x["acetic acid"] || 0) > 0.02) out.push(["smell", "vinegar (acetic acid left in the crystals)"]);
      return out;
    }
  };

  /* ============================== SN2: 1-BROMOBUTANE ============================== */
  function layerStep(title, why, correct, densities, extra) {
    return { title: title, why: why,
      controls: [sel("keep", "Which layer is your 1-bromobutane?", [["top", "the top layer"], ["bottom", "the bottom layer"]], "top"), chk("other", "keep the other layer, labelled, until the end", true)].concat(extra || []),
      layer: { correct: correct, densities: densities } };
  }
  function applyLayer(st, ch, step, say) {
    if (ch.keep === step.layer.correct) { say("Correct: " + step.layer.densities + " You keep the " + ch.keep + " layer."); return true; }
    if (ch.other) { scaleAll(st, 0.96); say("<strong>Wrong layer.</strong> " + step.layer.densities + " You had kept the other layer, so a drop test shows the mistake and you recover the product (about 4 % lost).", "bad"); return true; }
    st.sp["1-bromobutane"] = 0; st.sp["1-butanol"] = 0; st.sp["dibutyl ether"] = 0; st.lost = true; st.water = 0;
    say("<strong>Product discarded.</strong> " + step.layer.densities + " The layer you threw away held the 1-bromobutane. Keep every layer until the product is in your hands.", "bad");
    return false;
  }
  var sn2 = {
    key: "sn2", title: "1-Bromobutane from 1-butanol (SN2)", product: "1-bromobutane", sm: "1-butanol", eluent: 0.2, liquid: true,
    intro: "1-Butanol (10.0 mL, 109 mmol) is heated under reflux with sodium bromide (13.0 g, 126 mmol) and concentrated sulfuric acid. The acid protonates the OH, and bromide attacks the primary carbon from the back side (SN2). The crude product is distilled out, washed (water, cold concentrated H₂SO₄, NaHCO₃), dried and distilled. Theoretical yield 14.97 g (11.8 mL).",
    cards: [["1-butanol", "10.0 mL (8.10 g, 109 mmol), d = 0.810 g/mL", "H226 flammable, H302, H315, H318, H335, H336"],
      ["sodium bromide", "13.0 g (126 mmol)", "irritant"],
      ["sulfuric acid, conc.", "10 mL, then 5 mL cold for the wash", "H290, H314 severe burns; reacts violently with water"],
      ["1-bromobutane (product)", "M = 137.02, d = 1.27 g/mL, bp 101.6 °C", "H225 highly flammable, H315, H319, H335, H411"]],
    init: function (st) { st.theo = 10.0 * 0.810 / 74.12 * 1000; st.sp = { "1-butanol": st.theo }; st.water = 0; st.br = 126.3; st.rate = 1; },
    steps: [
      { title: "Mix the reagents", why: "Sulfuric acid and NaBr make HBr in the flask. Adding the acid slowly with cooling keeps the HBr in solution; hot concentrated acid also oxidises bromide to bromine.",
        controls: [sel("mix", "Order", [["careful", "NaBr + 10 mL water + butanol, then 10 mL conc. H₂SO₄ slowly, swirling in an ice bath"], ["fast", "add the acid quickly without cooling"], ["less", "use only 5 mL of acid"]], "careful")],
        run: function (st, ch, rng, say) {
          if (ch.mix === "careful") { st.br = 126.3 * 0.98; say("The mixture warms but stays below 30 °C; a clear lower salt layer and the butanol."); }
          if (ch.mix === "fast") { st.br = 126.3 * 0.80; say("The mixture gets hot, white HBr fumes escape and an orange-brown colour of bromine appears: bromide is lost.", "warn"); }
          if (ch.mix === "less") { st.br = 126.3 * 0.98; st.rate = 0.5; say("Less acid: less of the alcohol is protonated, so the substitution will be slower.", "warn"); }
        } },
      { title: "Heat under reflux", why: "Reflux holds the mixture at its boiling point without losing it. Gentle heat favours substitution; overheating favours elimination (1-butene gas) and ether formation.",
        controls: [sel("chips", "Boiling chips", [["yes", "added before heating"], ["no", "forgotten"]], "yes"),
          sel("heat", "Heating", [["gentle", "gentle: reflux ring in the lower third of the condenser"], ["vigorous", "vigorous: strong boiling"]], "gentle"),
          sel("t", "Time", [["15", "15 min"], ["45", "45 min"], ["60", "60 min"]], "45")],
        run: function (st, ch, rng, say) {
          var n = st.sp["1-butanol"], t = parseFloat(ch.t), vig = ch.heat === "vigorous";
          var k = (vig ? 0.07 : 0.045) * st.rate, conv = Math.min(1 - Math.exp(-k * t), st.br / n);
          var fB = (vig ? 0.12 : 0.015) * t / 45, fE = (vig ? 0.07 : 0.03) * t / 45;
          var reacted = n * conv, butene = n * fB, ether = n * fE;
          var rbr = Math.max(0, reacted - butene - 2 * ether);
          st.sp = { "1-bromobutane": rbr, "1-butanol": n - reacted, "dibutyl ether": ether };
          if (ch.chips === "no" && rng.random() < 0.8) { scaleAll(st, 0.88); say("<strong>Bump:</strong> without boiling chips the mixture boils violently and some is thrown up the condenser (about 12 % lost).", "bad"); }
          say((100 * conv).toFixed(0) + " % of the butanol has reacted. Gas evolved: about " + (butene * 24.5).toFixed(0) + " mL of 1-butene (from elimination)." + (vig ? " Vigorous heating also made more dibutyl ether." : ""), vig ? "warn" : "");
          if (t < 30) say("15 min is short: much butanol is left.", "warn");
        } },
      { title: "Distil the crude product out of the flask", why: "1-Bromobutane co-distils with water. Distil until the drops coming over are clear (no more oily drops). Never distil to dryness.",
        controls: [sel("d", "Stop when", [["clear", "the distillate drops are clear (no oily drops)"], ["early", "after the first few mL"], ["dry", "the flask is dry"]], "clear")],
        run: function (st, ch, rng, say) {
          var f = ch.d === "early" ? [0.6, 0.15, 0.2] : [0.97, 0.4, 0.5];
          st.sp["1-bromobutane"] *= f[0]; st.sp["1-butanol"] *= f[1]; st.sp["dibutyl ether"] *= f[2]; st.water = 3;
          say("The distillate is two layers: water and an oily layer of crude 1-bromobutane." + (ch.d === "early" ? " Stopping early left much of the product in the flask." : ""), ch.d === "early" ? "warn" : "");
          if (ch.d === "dry") say("Distilling to dryness left a black tarry residue and gave off SO₂ and bromine fumes. Leave some liquid in the flask.", "bad");
        } },
      layerStep("Wash with water", "Water removes the HBr, sulfuric acid and some butanol. Decide which layer is the product from densities: 1-bromobutane 1.27 g/mL, water 1.00 g/mL.", "bottom", "1-Bromobutane (1.27 g/mL) is denser than water (1.00 g/mL): it is the bottom layer."),
      layerStep("Wash with cold concentrated sulfuric acid", "Cold conc. H₂SO₄ protonates leftover butanol and dibutyl ether, which then dissolve in the acid. Densities: 1-bromobutane 1.27 g/mL, conc. H₂SO₄ 1.84 g/mL.", "top", "Concentrated H₂SO₄ (1.84 g/mL) is denser than 1-bromobutane (1.27 g/mL): the product is now the top layer. The layers switched."),
      layerStep("Wash with aqueous NaHCO₃", "Bicarbonate neutralises the last acid; CO₂ forms, so vent. Densities: 1-bromobutane 1.27, NaHCO₃ solution about 1.05 g/mL.", "bottom", "1-Bromobutane (1.27 g/mL) sinks below the bicarbonate solution (about 1.05 g/mL): bottom layer.",
        [chk("vent", "vent the funnel often", true)]),
      { title: "Dry the organic layer", why: "Anhydrous calcium chloride is the usual drying agent for alkyl halides; it also binds traces of alcohol. Add until new granules stay free-flowing and the liquid is clear.",
        controls: [sel("agent", "Drying agent", [["cacl2", "anhydrous CaCl₂"], ["mgso4", "anhydrous MgSO₄"], ["none", "none"]], "cacl2"),
          sel("amt", "Amount", [["free", "until new granules stay free-flowing"], ["one", "one small spatula only"]], "free")],
        run: function (st, ch, rng, say) {
          st.sp["1-bromobutane"] *= 0.98;
          if (ch.agent === "none") { st.water = 0.4; say("Not dried: the liquid is cloudy.", "warn"); return; }
          st.water = ch.amt === "free" ? 0.005 : 0.15;
          if (ch.agent === "cacl2") st.sp["1-butanol"] *= 0.5;
          say(ch.amt === "free" ? "The liquid is clear and the last granules flow freely: dry." : "The drying agent clumped and the liquid is still slightly cloudy.", ch.amt === "free" ? "" : "warn");
        } },
      { title: "Final simple distillation", why: "Collect the fraction that boils near 101.6 °C. A wide cut collects more liquid but also water (early) and butanol or ether (late).",
        controls: [sel("cut", "Fraction collected", [["all", "everything that distils"], ["mid", "99–104 °C only"], ["narrow", "101–102 °C only"]], "mid")],
        run: function (st, ch, rng, say) {
          var f = { all: [0.96, 0.9, 0.6, 1], mid: [0.88, 0.15, 0.02, 0.1], narrow: [0.60, 0.05, 0, 0.05] }[ch.cut];
          st.sp["1-bromobutane"] *= f[0]; st.sp["1-butanol"] *= f[1]; st.sp["dibutyl ether"] *= f[2]; st.water *= f[3];
          st.isolated = true;
          say("Collected " + (g("1-bromobutane", st.sp["1-bromobutane"]) / 1.276).toFixed(1) + " mL of distillate (" + { all: "everything", mid: "99–104 °C", narrow: "101–102 °C" }[ch.cut] + ").");
        } }
    ],
    tests: function (st, x) {
      var xb = x["1-butanol"] || 0, xe = x["dibutyl ether"] || 0, w = st.water > 0.02;
      var lo = 101.6 - (w ? 8 : 0.6), hi = 101.6 + 30 * xb + 40 * xe + 0.8;
      return [["boiling range", lo.toFixed(0) + "–" + hi.toFixed(0) + " °C (lit. 101.6 °C)" + (w ? "; cloudy first drops (water)" : "")],
        ["purity (GC area %)", (100 * (x["1-bromobutane"] || 0)).toFixed(1) + " %"],
        ["TLC", "1-bromobutane and 1-butanol are not UV-active: use the iodine stain, or better GC and IR"]];
    }
  };
  sn2.steps.forEach(function (s) {
    if (s.layer) s.run = function (st, ch, rng, say) {
      if (st.lost) { say("Nothing left to wash: the product was discarded.", "bad"); return; }
      if (ch.vent === false) { scaleAll(st, 0.85); say("<strong>No venting:</strong> CO₂ pressure blows the stopper out and sprays the mixture (about 15 % lost).", "bad"); }
      if (!applyLayer(st, ch, s, say)) return;
      if (/water/.test(s.title)) st.sp["1-butanol"] *= 0.7;
      if (/sulfuric/.test(s.title)) { st.sp["1-butanol"] *= 0.1; st.sp["dibutyl ether"] *= 0.1; st.sp["1-bromobutane"] *= 0.98; say("The acid removed most of the butanol and dibutyl ether."); }
      if (/NaHCO/.test(s.title)) { st.sp["1-bromobutane"] *= 0.98; }
    };
  });

  /* ============================== GRIGNARD ============================== */
  var grignard = {
    key: "grignard", title: "Triphenylmethanol by a Grignard reaction", product: "triphenylmethanol", sm: "benzophenone", eluent: 0.1,
    intro: "Phenylmagnesium bromide is made from bromobenzene (2.2 mL, 21.0 mmol) and magnesium (0.50 g, 20.6 mmol) in dry ether, then added to benzophenone (3.64 g, 20.0 mmol). Acid work-up gives triphenylmethanol. Benzophenone is limiting; theoretical yield 5.20 g. The reagent is a very strong base: 37 mg of water (less than a drop) destroys 10 % of it.",
    cards: [["bromobenzene", "2.2 mL (3.29 g, 21.0 mmol), d = 1.495 g/mL", "H226, H315, H331 toxic if inhaled (as lesson 24.5), H411"],
      ["magnesium turnings", "0.50 g (20.6 mmol)", "H228 flammable solid, H261 releases flammable gas with water"],
      ["diethyl ether, anhydrous", "about 25 mL", "H224 extremely flammable, H302, H336; forms peroxides"],
      ["benzophenone", "3.64 g (20.0 mmol)", "H373, H410"],
      ["triphenylmethanol (product)", "M = 260.34, mp 160–162 °C", "irritant"]],
    init: function (st) { st.theo = 20.0; st.sp = {}; st.water = 0; st.waterMg = 0; st.started = false; st.tries = 0; },
    steps: [
      { title: "Prepare glassware and ether", why: "Any water protonates the Grignard reagent to benzene. Oven-dried glassware assembled warm, anhydrous ether and a drying tube keep water out.",
        controls: [sel("glass", "Glassware", [["oven", "oven-dried, assembled warm"], ["air", "air-dried overnight (a film of water)"], ["rinsed", "rinsed with water just before"]], "oven"),
          sel("ether", "Ether", [["fresh", "anhydrous, fresh bottle"], ["open", "a bottle left open for a week"]], "fresh"),
          chk("tube", "CaCl₂ drying tube on the condenser", true)],
        run: function (st, ch, rng, say) {
          st.waterMg = { oven: 3, air: 37, rinsed: 300 }[ch.glass] + (ch.ether === "fresh" ? 2 : 50) + (ch.tube ? 0 : 15);
          say("Water that will reach the reagent: about " + st.waterMg + " mg = " + (st.waterMg / 18.015).toFixed(1) + " mmol, " + (100 * st.waterMg / 18.015 / 20.6).toFixed(0) + " % of the reagent.", st.waterMg > 30 ? "warn" : "");
        } },
      { title: "Start the Grignard reaction", why: "Magnesium is coated with oxide. A crystal of iodine, crushing a turning with a dry glass rod or gentle warming exposes fresh metal. Signs of starting: cloudiness, the iodine colour fading, the ether boiling by itself.",
        controls: [sel("m", "Method (with Mg and about 0.3 mL of the bromobenzene solution)", [["wait", "just wait"], ["iodine", "add a small crystal of iodine"], ["crush", "crush a turning with a dry glass rod"], ["warm", "warm gently with your hand or warm water"]], "wait")],
        run: function (st, ch, rng, say) {
          var p = { wait: 0.25, iodine: 0.85, crush: 0.8, warm: 0.6 }[ch.m];
          if (st.waterMg > 100) p *= 0.2; else if (st.waterMg > 30) p *= 0.7;
          st.tries++;
          if (rng.random() < p) { st.started = true; say("It starts: the solution turns cloudy grey" + (ch.m === "iodine" ? ", the brown iodine colour fades" : "") + " and the ether begins to boil gently on its own."); return; }
          say("Nothing happens after five minutes: the liquid stays clear" + (ch.m === "iodine" ? " and brown" : "") + ". Try another method." + (st.waterMg > 100 ? " (Wet glassware makes starting very hard.)" : ""), "warn");
          return { stay: true };
        } },
      { title: "Add the rest of the bromobenzene", why: "Slow addition keeps a gentle reflux from the reaction's own heat and keeps the concentration of unreacted bromobenzene low, which limits the biphenyl side product.",
        controls: [sel("add", "Addition", [["slow", "dropwise over 20 min, gentle reflux"], ["fast", "all at once"], ["hot", "dropwise, then strong heating for 30 min"]], "slow")],
        run: function (st, ch, rng, say) {
          var f = { slow: 0.03, fast: 0.20, hot: 0.08 }[ch.add], nPh = 21.0, nMg = 20.6;
          var nbp = f * nPh, w = st.waterMg / 18.015;
          var r = Math.max(0, (Math.min(nMg, nPh) - 2 * nbp) * 0.97 - w);
          if (ch.add === "fast") { r *= 0.9; say("The reaction runs away: the ether boils out of the top of the condenser and the mixture turns dark. Some reagent is lost.", "bad"); }
          st.rmgbr = r; st.sp = { biphenyl: nbp, benzene: w };
          say("Phenylmagnesium bromide formed: about " + r.toFixed(1) + " mmol (" + (w > 0.5 ? w.toFixed(1) + " mmol destroyed by water, " : "") + nbp.toFixed(1) + " mmol of biphenyl formed).");
        } },
      { title: "Add the benzophenone", why: "The phenyl carbanion adds to the C=O carbon. A solution added slowly mixes well; a lump of solid reacts unevenly.",
        controls: [sel("k", "Benzophenone (3.64 g)", [["sol", "dissolved in dry ether, added slowly, then 15 min at reflux"], ["solid", "added all at once as a solid"]], "sol")],
        run: function (st, ch, rng, say) {
          var conv = ch.k === "sol" ? 0.98 : 0.93, n = Math.min(st.rmgbr, 20.0) * conv;
          st.alk = n; st.sp.benzophenone = 20.0 - n;
          say("The pink-red colour of the adduct appears; " + n.toFixed(1) + " mmol of magnesium alkoxide formed." + (st.rmgbr < 20 ? " The Grignard reagent was the limiting reagent now: " + (20 - n).toFixed(1) + " mmol of benzophenone are left over." : ""), st.rmgbr < 19 ? "warn" : "");
        } },
      { title: "Acid work-up", why: "Until acid protonates it, the product is a magnesium alkoxide. Dilute acid on ice dissolves the magnesium salts; water alone leaves a gelatinous emulsion.",
        controls: [sel("w", "Work-up", [["acid", "pour slowly onto ice and 3 M H₂SO₄"], ["water", "just add water"], ["conc", "add concentrated acid quickly"]], "acid")],
        run: function (st, ch, rng, say) {
          var f = { acid: 0.97, water: 0.70, conc: 0.88 }[ch.w];
          st.sp.triphenylmethanol = st.alk * f;
          if (ch.w === "water") say("Basic magnesium salts form a thick gel and an emulsion; much product stays trapped in it.", "bad");
          else if (ch.w === "conc") say("Violent reaction: the ether boils and the solution turns yellow (the trityl cation forms in strong acid). Some product is lost.", "bad");
          else say("Two clear layers: the ether layer on top holds the product.");
        } },
      { title: "Separate, dry and evaporate the ether layer", why: "Ether (0.71 g/mL) is the top layer. Dry it over Na₂SO₄ before evaporating, or the solid comes out wet.",
        controls: [sel("keep", "Keep", [["top", "the top layer"], ["bottom", "the bottom layer"]], "top"), sel("dry", "Drying", [["yes", "dry over anhydrous Na₂SO₄ until free-flowing"], ["no", "evaporate straight away"]], "yes")],
        run: function (st, ch, rng, say) {
          if (ch.keep === "bottom") { scaleAll(st, 0.96); say("Wrong layer: the ether (0.71 g/mL) is on top. You kept both, so you swap back (4 % lost).", "bad"); }
          delete st.sp.benzene;
          scaleAll(st, 0.98);
          st.water = ch.dry === "yes" ? 0.002 * dryMass(st) : 0.15;
          st.isolated = true;
          say("Evaporated: a crude " + (st.sp.biphenyl / (st.sp.triphenylmethanol + 1e-9) > 0.1 ? "yellowish, oily solid smelling of biphenyl" : "off-white solid") + ".");
        } },
      { title: "Remove the biphenyl", why: "Biphenyl dissolves in cold hexane (or petroleum ether); triphenylmethanol hardly does. Stir the crude solid with a little cold hexane and filter.",
        controls: [sel("hex", "Trituration", [["yes", "stir with 10 mL cold hexane and filter"], ["no", "skip it"]], "yes")],
        run: function (st, ch, rng, say) {
          if (ch.hex === "no") { say("Skipped: the biphenyl stays in the product."); return; }
          var removed = st.sp.biphenyl * 0.9;
          st.sp.biphenyl *= 0.1; st.sp.benzophenone *= 0.5; st.sp.triphenylmethanol *= 0.96;
          wetCake(st); st.water = 0.1 * dryMass(st);
          say("The hexane washings carried away " + g("biphenyl", removed).toFixed(2) + " g of biphenyl.");
        } },
      { title: "Recrystallise", why: "Recrystallisation from 2-propanol removes the last biphenyl and benzophenone.",
        controls: [recrystChoice("rc", "Recrystallisation", [["skip", "skip it"], ["ipa", "from hot 2-propanol, slow cooling"]])],
        run: function (st, ch, rng, say) {
          if (ch.rc === "skip") { say("No recrystallisation."); return; }
          st.sp.triphenylmethanol *= 0.85; st.sp.biphenyl *= 0.1; st.sp.benzophenone *= 0.2;
          wetCake(st); say("White crystals from 2-propanol.");
        } },
      { title: "Dry the product", why: "Dry to constant mass before weighing and measuring the melting point.", controls: [DRY], run: function (st, ch, rng, say) { doDry(st, ch, say); } }
    ]
  };

  /* ============================== ALDOL ============================== */
  var aldol = {
    key: "aldol", title: "Dibenzalacetone by a crossed aldol condensation", product: "dibenzalacetone", sm: "benzaldehyde", eluent: 0.2,
    intro: "Benzaldehyde and acetone condense in ethanolic sodium hydroxide (Claisen–Schmidt). Benzaldehyde has no α-hydrogens, so only acetone forms an enolate. Two benzaldehydes per acetone give dibenzalacetone, which precipitates as a yellow solid and drives the equilibrium. Standard amounts: 2.0 mL benzaldehyde (19.7 mmol) and 0.73 mL acetone (9.9 mmol), theoretical yield 2.31 g.",
    cards: [["benzaldehyde", "2.0 mL (2.09 g, 19.7 mmol), d = 1.046 g/mL", "H302 harmful if swallowed"],
      ["acetone", "0.73 mL (0.57 g, 9.9 mmol), d = 0.785 g/mL", "H225 highly flammable, H319, H336"],
      ["sodium hydroxide in ethanol/water", "about 20 mL of a 10 % solution", "H314 severe burns"],
      ["dibenzalacetone (product)", "M = 234.29, mp 110–111 °C (trans,trans)", "irritant"]],
    init: function (st) { st.sp = {}; st.water = 0; st.nAc = 0.73 * 0.785 / 58.08 * 1000; },
    steps: [
      { title: "Measure the reagents", why: "Stoichiometry decides the product: 2 : 1 benzaldehyde to acetone gives the double condensation. Old benzaldehyde has oxidised in air to benzoic acid.",
        controls: [sel("r", "Benzaldehyde : acetone", [["1", "1 : 1 (0.99 mL benzaldehyde)"], ["2", "2 : 1 (2.0 mL)"], ["3", "3 : 1 (3.0 mL)"]], "2"),
          sel("old", "Benzaldehyde", [["fresh", "fresh, colourless"], ["old", "old, yellowed (contains benzoic acid crystals)"]], "fresh")],
        run: function (st, ch, rng, say) {
          var vol = { 1: 0.99, 2: 2.0, 3: 3.0 }[ch.r], n = vol * 1.046 / 106.12 * 1000;
          st.nPh = n * (ch.old === "old" ? 0.9 : 1); st.oldBA = ch.old === "old" ? n * 0.1 : 0;
          st.theo = Math.min(n / 2, st.nAc);
          say(vol + " mL benzaldehyde (" + n.toFixed(1) + " mmol) and 0.73 mL acetone (" + st.nAc.toFixed(1) + " mmol). Theoretical yield of dibenzalacetone: " + g("dibenzalacetone", st.theo).toFixed(2) + " g.");
        } },
      { title: "Add the base and stir", why: "The reaction runs at room temperature; the product precipitates. Heating above about 30 °C speeds up side reactions (Cannizzaro reaction of benzaldehyde, self-condensation of acetone).",
        controls: [sel("T", "Temperature", [["rt", "room temperature (20–25 °C)"], ["warm", "warmed to 50 °C to speed it up"]], "rt"),
          sel("t", "Stirring time", [["15", "15 min"], ["30", "30 min"]], "30")],
        run: function (st, ch, rng, say) {
          var conv = ch.t === "30" ? 0.95 : 0.85, side = 0;
          if (ch.T === "warm") { conv = 0.97; side = 0.12 * st.nPh; }
          var ph = st.nPh - side, p = Math.min(1, ph / (2 * st.nAc)) * conv;
          var di = st.nAc * p * p, mono = st.nAc * 2 * p * (1 - p), left = Math.max(0, ph - st.nAc * 2 * p);
          st.oily = left > 2;
          st.sp = { dibenzalacetone: di * 0.95, benzalacetone: mono * 0.6, benzaldehyde: left * (st.oily ? 0.7 : 0.3), "benzyl alcohol": side * 0.5 * 0.3 };
          say("A yellow precipitate forms within minutes." + (mono > di ? " Only a little precipitates; the solution stays yellow and smells of benzaldehyde." : "") + (left > 2 ? " Excess benzaldehyde gives an oily, almond-smelling layer on the solid." : ""));
          if (side) say("At 50 °C the mixture darkens and turns oily: side reactions consumed some benzaldehyde.", "warn");
          if (st.oldBA) say("The benzoic acid from the old benzaldehyde is neutralised by the base and stays in solution, but there is less aldehyde to react.", "warn");
        } },
      { title: "Filter and wash", why: "Cold water removes the sodium hydroxide; a little cold ethanol removes leftover benzaldehyde and most of the mono product without dissolving much dibenzalacetone.",
        controls: [sel("w", "Wash", [["eth", "cold water, then 2 × 5 mL cold ethanol"], ["water", "cold water only"], ["none", "no wash"]], "eth")],
        run: function (st, ch, rng, say) {
          var s = st.sp;
          if (ch.w === "eth") { s.benzaldehyde *= st.oily ? 0.5 : 0.2; s.benzalacetone *= 0.25; s["benzyl alcohol"] *= 0.3; s.dibenzalacetone *= 0.97; }
          if (ch.w === "water") { s.benzaldehyde *= 0.85; }
          wetCake(st);
          say(ch.w === "none" ? "Unwashed: the solid is slippery with sodium hydroxide (basic, corrosive)." : "Washed on the filter.", ch.w === "none" ? "warn" : "");
        } },
      { title: "Recrystallise", why: "Hot ethanol (or ethyl acetate) and slow cooling give yellow plates of the trans,trans isomer.",
        controls: [sel("rc", "Recrystallisation", [["skip", "skip it (check the crude product first)"], ["eth", "from hot ethanol, slow cooling"]], "skip")],
        run: function (st, ch, rng, say) {
          if (ch.rc === "skip") { say("No recrystallisation."); return; }
          var s = st.sp; s.dibenzalacetone *= 0.85; s.benzalacetone *= 0.3; s.benzaldehyde *= 0.1; s["benzyl alcohol"] *= 0.1;
          wetCake(st); say("Recrystallised from ethanol.");
        } },
      { title: "Dry the product", why: "Dry to constant mass.", controls: [DRY], run: function (st, ch, rng, say) { doDry(st, ch, say); } }
    ],
    look: function (st, x, comp) {
      var liq = g("benzaldehyde", comp.benzaldehyde || 0) + g("benzyl alcohol", comp["benzyl alcohol"] || 0), m = dryMass(st);
      if (liq / Math.max(1e-9, m) > 0.12) return "oily, sticky yellow solid that smells of almonds";
      if ((comp.benzalacetone || 0) > (comp.dibenzalacetone || 0)) return "pale yellow, low-melting solid";
      return null;
    }
  };

  /* ============================== MULTISTEP ============================== */
  function carry(st, stage) {
    st.inter = st.inter || {};
    st.inter[stage] = { sp: JSON.parse(JSON.stringify(st.sp)), water: st.water, mass: dryMass(st) + st.water };
  }
  function takeFrom(st, stage, grams) {
    var it = st.inter[stage], f = Math.min(1, grams / it.mass), sp = {};
    Object.keys(it.sp).forEach(function (k) { sp[k] = it.sp[k] * f; });
    return { sp: sp, water: it.water * f, used: Math.min(grams, it.mass) };
  }
  function decision(stage, name, rec) {
    return { title: "Check " + name + ", then decide", why: "Use 'Check the product now': TLC with a co-spot of the starting material, the melting point, IR and ¹H NMR. Carry the intermediate forward only when it passes.",
      controls: [sel("d", "Decision", [["carry", "it passes: carry it forward"], ["rc", "recrystallise it (from 95 % ethanol) and check again"], ["repeat", "repeat this step from the start"]], "carry")],
      run: function (st, ch, rng, say) {
        if (ch.d === "rc") { rec(st); wetCake(st); st.water = 0.002 * dryMass(st); say("Recrystallised and dried. Check it again."); return { stay: true }; }
        if (ch.d === "repeat") { say("Starting this step again."); return { goto: stage === 1 ? 0 : 3 }; }
        carry(st, stage);
        st.stageYield = st.stageYield || {}; st.stageYield[stage] = st.lastYield;
        say("Carried forward: " + (dryMass(st) + st.water).toFixed(2) + " g of " + name + ".");
      } };
  }
  var multistep = {
    key: "multistep", title: "Benzaldehyde → benzoin → benzil → benzilic acid", product: "benzoin", sm: "benzaldehyde", eluent: 0.2, multi: true,
    intro: "A three-step teaching sequence with a check at every stage. Step 1: thiamine-catalysed benzoin condensation (umpolung), room temperature, about 24 h. Step 2: oxidation of benzoin to benzil with concentrated nitric acid in the hood. Step 3: benzilic acid rearrangement with KOH, then acid. Plan: for 1.00 g of benzilic acid at 70 % per step you need about 2.7 g of benzaldehyde.",
    cards: [["benzaldehyde", "10.0 mL = 10.46 g (98.6 mmol) by default", "H302"], ["thiamine hydrochloride, NaOH", "catalyst and base", "NaOH H314"],
      ["nitric acid, concentrated", "step 2, in the fume hood", "H272 oxidiser, H290, H314, H331; releases toxic NO₂"],
      ["potassium hydroxide; hydrochloric acid", "step 3", "H302, H314; HCl H290, H314, H335"]],
    init: function (st) { st.sp = {}; st.water = 0; st.stage = 1; st.stageYield = {}; },
    stageInfo: { 1: ["benzoin", "benzaldehyde", 2], 2: ["benzil", "benzoin", 1], 3: ["benzilic acid", "benzil", 1] },
    steps: [
      { title: "Step 1: benzoin condensation", why: "Deprotonated thiamine adds to one benzaldehyde and makes its carbon nucleophilic, which then attacks a second aldehyde. NaOH must be added cold and slowly (to pH about 8): heat and strong base destroy thiamine. The reaction needs about a day.",
        controls: [num("vol", "Benzaldehyde / mL", 1, 20, 0.5, 10), sel("old", "Benzaldehyde", [["fresh", "fresh"], ["old", "old (partly oxidised to benzoic acid)"]], "fresh"),
          sel("base", "Base", [["careful", "thiamine in water, cooled, 2 M NaOH dropwise to pH about 8 (pale yellow)"], ["fast", "NaOH added quickly to the warm solution"]], "careful"),
          sel("t", "Time at room temperature", [["1", "1 hour"], ["24", "24 hours"], ["72", "3 days"]], "24")],
        run: function (st, ch, rng, say) {
          st.stage = 1;
          var vol = Math.max(1, parseFloat(ch.vol) || 10), n = vol * 1.046 / 106.12 * 1000, eff = n * (ch.old === "old" ? 0.85 : 1);
          var y = { 1: 0.12, 24: 0.62, 72: 0.66 }[ch.t] * (ch.base === "fast" ? 0.15 : 1);
          var nb = eff / 2 * y;
          st.theo = n / 2; st.startG = vol * 1.046;
          st.sp = { benzoin: nb, benzaldehyde: eff - 2 * nb };
          say("Started from " + (vol * 1.046).toFixed(2) + " g of benzaldehyde (" + n.toFixed(1) + " mmol): at most " + g("benzoin", n / 2).toFixed(2) + " g of benzoin (two in, one out).");
          say(ch.base === "fast" ? "The solution turned deep yellow-brown: the thiamine decomposed and little benzoin forms." : "White crystals of benzoin grow over time.", ch.base === "fast" ? "bad" : "");
        } },
      { title: "Step 1: isolate the benzoin", why: "Cool in ice, filter, and wash with cold 50 % ethanol to remove unreacted benzaldehyde.",
        controls: [sel("w", "Wash", [["eth", "cold 50 % ethanol"], ["none", "no wash"]], "eth"), sel("rc", "Recrystallise from 95 % ethanol", [["no", "no"], ["yes", "yes"]], "no"), DRY],
        run: function (st, ch, rng, say) {
          st.sp.benzoin *= 0.94; st.sp.benzaldehyde *= ch.w === "eth" ? 0.008 : 0.10;
          if (ch.rc === "yes") { st.sp.benzoin *= 0.85; st.sp.benzaldehyde *= 0.1; }
          wetCake(st); doDry(st, ch, say);
          st.lastYield = st.sp.benzoin / st.theo;
        } },
      decision(1, "the benzoin", function (st) { st.sp.benzoin *= 0.85; st.sp.benzaldehyde = (st.sp.benzaldehyde || 0) * 0.1; }),
      { title: "Step 2: oxidise benzoin to benzil", why: "Concentrated nitric acid oxidises the secondary alcohol to a ketone at 70–80 °C, releasing toxic brown NO₂: only in a fume hood. Too short a time leaves benzoin.",
        controls: [num("m", "Benzoin to use / g", 0.2, 20, 0.1, 4.0), sel("hood", "Where", [["hood", "in the fume hood"], ["bench", "on the open bench"]], "hood"),
          sel("t", "Time at 70–80 °C", [["10", "10 min"], ["20", "20 min"], ["30", "30 min"], ["45", "45 min"]], "30")],
        run: function (st, ch, rng, say) {
          if (ch.hood !== "hood") { say("Refused: nitric acid oxidations release brown, toxic NO₂ (H331). Work in the fume hood.", "bad"); return { stay: true }; }
          if (!st.inter || !st.inter[1]) { say("Carry the benzoin forward first.", "warn"); return { stay: true }; }
          st.stage = 2;
          var tk = takeFrom(st, 1, parseFloat(ch.m) || 4), t = parseFloat(ch.t), c = 1 - Math.exp(-0.16 * t);
          var nb = tk.sp.benzoin || 0;
          st.theo = tk.used / C.benzoin.M * 1000; st.startG = tk.used;
          st.sp = { benzil: nb * c, benzoin: nb * (1 - c), "benzoic acid": (tk.sp.benzaldehyde || 0) * 0.5 };
          st.water = 0;
          say("Used " + tk.used.toFixed(2) + " g of the benzoin. Brown NO₂ fumes rise in the hood; after " + t + " min about " + (100 * c).toFixed(0) + " % is oxidised.");
        } },
      { title: "Step 2: isolate the benzil", why: "Pour into ice water: benzil precipitates as a yellow solid. Recrystallisation from ethanol removes most leftover benzoin.",
        controls: [sel("rc", "Recrystallise from 95 % ethanol", [["no", "no"], ["yes", "yes"]], "yes"), DRY],
        run: function (st, ch, rng, say) {
          scaleAll(st, 0.92);
          if (ch.rc === "yes") { st.sp.benzil *= 0.91; st.sp.benzoin *= 0.25; st.sp["benzoic acid"] *= 0.3; }
          wetCake(st); doDry(st, ch, say);
          st.lastYield = st.sp.benzil / st.theo;
        } },
      decision(2, "the benzil", function (st) { st.sp.benzil *= 0.91; st.sp.benzoin *= 0.25; }),
      { title: "Step 3: benzilic acid rearrangement", why: "Hydroxide adds to one C=O, a phenyl group shifts to the neighbouring carbon, and the salt of benzilic acid forms. Acidify well below the pKa (about 3) to precipitate the acid.",
        controls: [num("m", "Benzil to use / g", 0.2, 20, 0.1, 2.0), sel("t", "Reflux with KOH", [["5", "5 min"], ["15", "15 min"]], "15"),
          sel("pH", "Acidify with HCl to", [["2", "pH 1–2 (check with pH paper)"], ["6", "about pH 6"]], "2"), sel("rc", "Recrystallise from hot water", [["no", "no"], ["yes", "yes"]], "no"), DRY],
        run: function (st, ch, rng, say) {
          if (!st.inter || !st.inter[2]) { say("Carry the benzil forward first.", "warn"); return { stay: true }; }
          st.stage = 3;
          var tk = takeFrom(st, 2, parseFloat(ch.m) || 2), conv = ch.t === "15" ? 0.99 : 0.6, nb = tk.sp.benzil || 0, bz = tk.sp.benzoin || 0;
          st.theo = tk.used / C.benzil.M * 1000; st.startG = tk.used;
          var acid = nb * conv, ba = (tk.sp["benzoic acid"] || 0) + 0.5 * bz, side = 0.5 * bz;
          var pf = ch.pH === "2" ? [0.97, 0.8] : [0.4, 0.2];
          st.sp = { "benzilic acid": acid * pf[0] * 0.79, benzil: nb * (1 - conv) * 0.79, "benzoic acid": ba * pf[1] * 0.79, "side products": side * 0.79 };
          if (ch.rc === "yes") { st.sp["benzilic acid"] *= 0.85; st.sp.benzil *= 0.2; st.sp["benzoic acid"] *= 0.6; st.sp["side products"] *= 0.3; }
          wetCake(st); doDry(st, ch, say);
          say("Used " + tk.used.toFixed(2) + " g of benzil. " + (ch.pH === "6" ? "At pH 6 most benzilic acid stays dissolved as its salt: little precipitate." : "White benzilic acid precipitates on acidifying.") + (bz > 0.05 * nb ? " The benzoin carried in reacted in the hot base to brownish side products." : "") + (conv < 0.9 ? " Yellow benzil remains: the rearrangement was incomplete." : ""), ch.pH === "6" || bz > 0.05 * nb ? "warn" : "");
          st.lastYield = st.sp["benzilic acid"] / st.theo; st.stageYield[3] = st.lastYield;
        } }
    ]
  };

  global.OB_SYN = { aspirin: aspirin, sn2: sn2, grignard: grignard, aldol: aldol, multistep: multistep, dryMass: dryMass, g: g, mm: mm };
})(typeof window !== "undefined" ? window : this);
