/* titration simulation: a burette bench for acid–base, potentiometric, buffer-capacity,
 * redox (Fe2+/Ce4+), precipitation (Mohr) and EDTA titrations, plus the colorimetric
 * manganese-in-steel method. Uses ../common/sim.js (global Sim).
 *
 * Chemistry (all exact balances solved numerically at every volume, 25 °C):
 *  - Acid–base: charge balance [Na+] + [H+] = [OH-] + [Cl-] + sum C Ka/(Ka + [H+]).
 *    Kw = 1.0e-14. pKa acetic acid 4.757 (Harvey, Analytical Chemistry 2.1, App. 16.11),
 *    KHP (hydrogen phthalate) 5.41 (Harvey 16.11), M(KHP) = 204.22 g/mol (Lesson 10.1).
 *  - Indicators: pKIn methyl orange 3.7, methyl red 5.0, bromothymol blue 7.1, phenol red 7.8,
 *    phenolphthalein 9.6 (Harvey Table 9.2.3; these reproduce the Lesson 10.1 errors).
 *  - Glass electrode: Nernst slope RT ln10 / F = 59.16 mV at 25 °C (R, F from CODATA 2022).
 *  - Redox: E°' Fe3+/Fe2+ 0.68 V (1 M H2SO4) and 0.732 V (1 M HClO4); Ce4+/Ce3+ 1.44 V
 *    (1 M H2SO4) and 1.70 V (1 M HClO4); ferroin 1.147 V; Ag/AgCl (sat. KCl) +0.197 V
 *    (Harvey App. 16.13, section 9.4; Lesson 10.2).
 *  - Mohr: Ksp AgCl 1.8e-10, Ag2CrO4 1.2e-12 (Harvey App. 16.10); pKa HCrO4- 6.51
 *    (Harvey App. 16.11); Ag2O/AgOH: [Ag+][OH-] = 2.0e-8 (Harvey App. 16.10).
 *    E°(Ag+/Ag) = 0.7996 V.
 *  - EDTA: pKa 0.0, 1.5, 2.0, 2.66, 6.16, 10.24; log Kf CaY2- 10.69, MgY2- 8.79
 *    (Harvey 9.3 and App. 16.12). Eriochrome Black T: pKa 6.3, 11.6; log K MgIn 7.0, CaIn 5.4
 *    (Harvey 9.3). Calcon (calconcarboxylic acid) as calcium indicator at pH 12–13:
 *    pKa 9.3 and 13.0, log K CaIn 6.6 (approximate values, for teaching).
 *    Mg(OH)2 Ksp 7.1e-12 (Harvey App. 16.10).
 *  - Mn in steel: MnO4- molar absorptivity about 2.4e3 L mol-1 cm-1 at 525 nm (LibreTexts lab).
 * Burette: Class A 50 mL ±0.05 mL (ASTM E287); one drop 0.050 ± 0.004 mL; parallax from the
 * same tube geometry as the glassware simulation (1.14 cm per mL, inner radius 0.53 cm, wall
 * 0.12 cm, n glass 1.47, n water 1.333, eye 25 cm from the tube).
 * Colours: Beer–Lambert absorbance in three broad colour channels (R, G, B) with rough molar
 * absorptivities; for illustration only.
 */
(function () {
  "use strict";
  var KW = 1.0e-14;
  var NERNST = Sim.C.R * 298.15 * Math.LN10 / Sim.C.F;       // 0.059159 V
  var E_AGCL = 0.197;
  var DROP = 0.050;

  /* ---------------- presets ---------------- */
  var PRESETS = {
    "strong-acid": {
      title: "Strong acid with a strong base", mode: "acidbase", analyte: "HCl", indicator: "btb", meter: true,
      what: "25.00 mL of 0.1000 M HCl is titrated with 0.1000 M NaOH. Before equivalence the pH comes from the acid left over, after it from the excess OH⁻; at equivalence only NaCl and water remain, so the pH is 7.00. Near equivalence the pH jumps by several units within a fraction of a millilitre.",
      task: "Add the base in 1–5 mL steps to 20 mL, then in 0.1 mL steps and single drops through the jump, and stop at the first lasting colour change of bromothymol blue. The pH meter logs the curve. Then press Reveal and compare.",
      target: "End point within 0.10 mL (two drops) of 25.00 mL; a curve that is flat, then near-vertical around pH 7 (pH about 3.7 at 24.90 mL and 10.3 at 25.10 mL)."
    },
    "weak-acid": {
      title: "Weak acid, and the choice of indicator", mode: "acidbase", analyte: "AcOH", indicator: "php", meter: false,
      what: "25.00 mL of 0.1000 M acetic acid (pK<sub>a</sub> 4.757) with 0.1000 M NaOH. The curve has four regions: the weak acid alone, a buffer region where pH = pK<sub>a</sub> + log(n<sub>A⁻</sub>/n<sub>HA</sub>), the equivalence point at about pH 8.7 (acetate is a weak base), and the excess-base region.",
      task: "Titrate three times, once with methyl orange, once with bromothymol blue and once with phenolphthalein, slowing to single drops near each end point. Write down each end point. Then switch on the pH meter and record the full curve.",
      target: "With phenolphthalein, an end point within 0.05 mL of the equivalence point; the pH at half that volume within 0.05 of 4.76."
    },
    "indicator-choice": {
      title: "Choosing an indicator", mode: "acidbase", analyte: "HCl", indicator: "mo", meter: false, eye: "free",
      what: "An indicator changes colour over about pK<sub>In</sub> ± 1. Its window must fall inside the steep jump of the titration curve. For 0.1 M HCl the jump runs from about pH 4 to 10, so almost any indicator works; for acetic acid the curve is buffered up to equivalence and the jump starts only near pH 7.",
      task: "Titrate the strong acid with each of the five indicators and note the end point and the error the simulation reports. Then switch to acetic acid and repeat. Read the burette at eye level every time; the simulation adds parallax if you do not. For the home project (Lesson 10.6): three phenolphthalein titrations of the weak acid, noting how many drops past equivalence each one is.",
      target: "An error under 0.2 % for the weak acid (phenolphthalein or phenol red, single drops for the last 0.5 mL); three end points within one drop of each other."
    },
    buffer: {
      title: "Buffer capacity", mode: "buffer", solution: "buf10",
      what: "A buffer holds its pH because added strong acid turns A⁻ into HA; only the ratio changes. Its capacity β (mol/L of strong acid or base per pH unit) is largest at pH = pK<sub>a</sub> and proportional to the buffer's concentration: a tenfold dilution keeps the pH but cuts the capacity tenfold.",
      task: "Add 0.100 M HCl in small portions to 100.0 mL of water, of 0.10 M acetate buffer (5.00 + 5.00 mmol) and of 0.010 M buffer (0.50 + 0.50 mmol), and watch the pH. Use 1.00 M HCl if the 0.10 M buffer needs too much.",
      target: "The acid that moves each buffer down by 1 pH unit (about 4.1 mmol and 0.41 mmol), and a ratio of about 10 between the two buffers; water drops by a pH unit with a single drop."
    },
    potentiometric: {
      title: "Potentiometric end point with electrode drift", mode: "potentiometric", analyte: "AcOH08",
      what: "A glass electrode follows the titration when no colour can. Its response is E = K − s·pH with s close to 59.16 mV per pH unit; each electrode has its own K and a slightly low s, so you calibrate it with two buffers. The end point comes from the data: the first-derivative peak, the second-derivative zero crossing, or a Gran plot of V·10<sup>−pH</sup> against V.",
      task: "Calibrate with the two buffers, then titrate 25.00 mL of acetic acid with 0.1000 M NaOH: 1 mL steps at first and 0.1 mL steps between 18 and 21 mL, then a few mL past the end. Read the end point from the derivative plot and the Gran plot. Repeat without calibrating, and with the aged electrode (calibrate it and note its slope).",
      target: "End point 20.00 mL within about 0.05 mL by the second derivative; pK<sub>a</sub> within 0.05 of 4.76 when calibrated. Say which result the uncalibrated or aged electrode spoils: the end-point volume or the measured pH."
    },
    redox: {
      title: "Iron(II) with cerium(IV): ferroin or a platinum electrode", mode: "redox",
      what: "25.00 mL of 0.0500 M Fe²⁺ in 1 M H₂SO₄ is titrated with 0.1000 M Ce⁴⁺. Before equivalence the Fe³⁺/Fe²⁺ couple sets the potential of the platinum electrode, after it Ce⁴⁺/Ce³⁺. At half-equivalence E = E°′(Fe) = 0.68 V; at equivalence E = (0.68 + 1.44)/2 = 1.06 V vs SHE. The meter reads against Ag/AgCl, 0.197 V lower.",
      task: "Titrate once with ferroin by eye (red to pale blue) and once with the platinum electrode, logging the potential. Record both end points. Read the two formal potentials from the curve at half and twice the equivalence volume. Then try 1 M HClO₄ as the medium.",
      target: "The two end points agree within 0.05 mL of 12.50 mL; E°′ values near 0.68 and 1.44 V vs SHE."
    },
    precipitation: {
      title: "Chloride with silver nitrate (Mohr)", mode: "precipitation",
      what: "Ag⁺ + Cl⁻ → AgCl(s). After the last chloride, the next silver forms red-brown Ag₂CrO₄ with the chromate indicator. Some excess silver is always needed before the colour shows, so a reagent blank (a chloride-free CaCO₃ suspension) is titrated to the same shade and subtracted. In acid, chromate turns into HCrO₄⁻ and the end point comes late.",
      task: "Titrate the 50.00 mL water sample at pH 8 and stop at the first lasting red-brown tint. Run the reagent blank and subtract it (the simulation does it once you have a blank). Then repeat at pH 5 and note how much later the colour appears.",
      target: "Blank-corrected pH 8 result within 0.5 % of the stated 283.6 mg/L chloride."
    },
    edta: {
      title: "Water hardness with EDTA", mode: "edta",
      what: "EDTA binds Ca²⁺ and Mg²⁺ 1 : 1, but only as Y⁴⁻, which dominates above pH 10.24. The conditional constant K<sub>f</sub>′ = α<sub>Y⁴⁻</sub>K<sub>f</sub> says how strongly it binds at the working pH. Eriochrome Black T is wine red on Mg²⁺ and blue when free: at the end point EDTA takes the last Mg²⁺ from it. At pH 12 Mg(OH)₂ precipitates and only calcium is titrated.",
      task: "Titrate the 50.00 mL tap-water sample at pH 10 with Eriochrome Black T to pure blue. Then try pH 8 and pH 12 (with the calcium indicator at pH 12) and compare the end points.",
      target: "pH 10 total hardness within 2 % of the stated 257 mg/L as CaCO₃ (12.85 mL of 0.01000 M EDTA); at pH 12 about 9.20 mL (calcium alone)."
    }
  };

  /* ---------------- reference data ---------------- */
  // abs: rough molar absorptivity in the R, G, B channels (L mol-1 cm-1)
  var INDICATORS = {
    none: { name: "no indicator" },
    mo: { name: "methyl orange (pK 3.7, red → yellow)", pK: 3.7, acid: [300, 22000, 17000], base: [0, 2500, 20000] },
    mr: { name: "methyl red (pK 5.0, red → yellow)", pK: 5.0, acid: [500, 24000, 14000], base: [0, 2200, 21000] },
    btb: { name: "bromothymol blue (pK 7.1, yellow → blue)", pK: 7.1, acid: [0, 1200, 17000], base: [26000, 11000, 1200] },
    pr: { name: "phenol red (pK 7.8, yellow → red)", pK: 7.8, acid: [0, 1400, 18000], base: [800, 26000, 12000] },
    php: { name: "phenolphthalein (pK 9.6, colourless → pink)", pK: 9.6, acid: [0, 0, 0], base: [1500, 30000, 9000] }
  };
  var IND_C = 1.3e-5;        // indicator in the flask, mol/L (two drops of a 0.1 % solution)
  var PATH = 3;              // effective path through the flask, cm

  var ANALYTES = {
    HCl: { name: "25.00 mL of 0.1000 M HCl", Va: 25.00, c: 0.1000, strong: true },
    AcOH: { name: "25.00 mL of 0.1000 M acetic acid", Va: 25.00, c: 0.1000, pKa: 4.757 },
    KHP: { name: "0.5105 g KHP (primary standard) in 50 mL water", Va: 50.0, n: 0.5105 / 204.22 * 1000, pKa: 5.41, khp: true },
    UNK: { name: "25.00 mL of diluted vinegar (unknown acetic acid)", Va: 25.00, c: null, pKa: 4.757, unknown: true },
    AcOH08: { name: "25.00 mL of 0.0800 M acetic acid", Va: 25.00, c: 0.0800, pKa: 4.757 },
    HCl08: { name: "25.00 mL of 0.0800 M HCl", Va: 25.00, c: 0.0800, strong: true }
  };
  var SOLUTIONS = {
    water: { name: "100.0 mL of water", HA: 0, A: 0 },
    buf10: { name: "100.0 mL of 0.10 M acetate buffer (5.00 mmol HA + 5.00 mmol A⁻)", HA: 5.00, A: 5.00 },
    buf01: { name: "100.0 mL of 0.010 M acetate buffer (0.50 mmol HA + 0.50 mmol A⁻)", HA: 0.50, A: 0.50 }
  };

  /* ---------------- numerical helpers ---------------- */
  function bisect(f, lo, hi, n) {
    // f increasing on [lo, hi]; returns the root (or an end if there is no sign change)
    var flo = f(lo);
    if (flo >= 0) return lo;
    if (f(hi) <= 0) return hi;
    for (var i = 0; i < (n || 80); i++) {
      var mid = (lo + hi) / 2;
      if (f(mid) < 0) lo = mid; else hi = mid;
    }
    return (lo + hi) / 2;
  }

  // pH from the charge balance; concentrations in mol/L; acids: [{C, Ka}]
  function solvePH(Na, Cl, acids) {
    var x = bisect(function (lx) {
      var h = Math.pow(10, lx), s = Na + h - KW / h - Cl;
      for (var i = 0; i < acids.length; i++) s -= acids[i].C * acids[i].Ka / (acids[i].Ka + h);
      return s;
    }, -15, 1, 90);
    return -x;
  }

  function alphaY4(pH) {
    var pk = [0.0, 1.5, 2.0, 2.66, 6.16, 10.24], h = Math.pow(10, -pH), terms = [Math.pow(h, 6)], prod = 1;
    for (var i = 0; i < 6; i++) { prod *= Math.pow(10, -pk[i]); terms.push(prod * Math.pow(h, 5 - i)); }
    var s = 0; terms.forEach(function (t) { s += t; });
    return terms[6] / s;
  }

  function absToRGB(A) {
    return [0, 1, 2].map(function (i) { return 248 * Math.pow(10, -Math.min(4, Math.max(0, A[i]))); });
  }
  function addAbs(A, eps, c) { for (var i = 0; i < 3; i++) A[i] += eps[i] * c * PATH; }
  function mix(rgb, col, t) { return [0, 1, 2].map(function (i) { return rgb[i] * (1 - t) + col[i] * t; }); }

  // a plain colour name from an RGB triple
  function colourName(rgb, milky) {
    var r = rgb[0] / 255, g = rgb[1] / 255, b = rgb[2] / 255;
    var mx = Math.max(r, g, b), mn = Math.min(r, g, b), d = mx - mn, L = (mx + mn) / 2;
    var base = milky ? "milky white" : "colourless";
    if (d < 0.07) return L < 0.45 ? "grey-brown" : base;
    var h;
    if (mx === r) h = 60 * (((g - b) / d) % 6);
    else if (mx === g) h = 60 * ((b - r) / d + 2);
    else h = 60 * ((r - g) / d + 4);
    if (h < 0) h += 360;
    var name;
    if (h < 14 || h >= 350) name = "red";
    else if (h < 38) name = L < 0.5 ? "red-brown" : "orange";
    else if (h < 66) name = L < 0.42 ? "brown" : "yellow";
    else if (h < 160) name = "green";
    else if (h < 200) name = "blue-green";
    else if (h < 255) name = "blue";
    else if (h < 290) name = "violet";
    else if (h < 330) name = "pink";
    else name = "wine red";
    var pale = d < 0.2 ? "faint " : d < 0.4 ? "pale " : "";
    return pale + name + (milky ? " (cloudy)" : "");
  }

  /* ---------------- experiment models ----------------
   * A model knows the flask: Va (mL), the titrant, the true equivalence volume Veq (mL of
   * titrant actually delivered), and state(V) for V mL delivered: {pH, E (V vs SHE), A (absorbance
   * per colour channel), turb: [{t, col}], milky, desc}. result(Vend) turns an end point into
   * the analytical result.
   */
  function acidModel(key, titrantKey, indKey, rng) {
    var an = ANALYTES[key], Va = an.Va;
    var cBottle = titrantKey === "nom" ? 0.1000 * (1 + rng.normal(0, 0.012)) : 0.1000;
    var cLabel = 0.1000;
    var nA = an.khp ? an.n : (an.unknown ? 25.00 * 0.0830 * (1 + rng.normal(0, 0.04)) : an.c * Va);   // mmol
    var Ka = an.strong ? null : Math.pow(10, -an.pKa);
    var ind = INDICATORS[indKey] || INDICATORS.none;
    var m = {
      Va: Va, cBottle: cBottle, cLabel: cLabel, Veq: nA / cBottle, titrant: titrantKey === "nom" ? "NaOH, about 0.1 M (not standardised)" : "0.1000 M NaOH",
      name: an.name.replace(/^25\.00 mL of /, "") + ", " + (indKey === "none" ? "no indicator" : ind.name.split(" (")[0]),
      config: key + "|" + indKey + "|" + titrantKey,
      state: function (V, cEff) {
        var Vt = Va + V, Na = cEff * V / Vt, pH;
        if (an.strong) pH = solvePH(Na, nA / Vt, []);
        else pH = solvePH(Na + (an.khp ? nA / Vt : 0), 0, [{ C: nA / Vt, Ka: Ka }]);
        var A = [0, 0, 0];
        if (ind.pK) {
          var f = 1 / (1 + Math.pow(10, ind.pK - pH)), ci = IND_C * 50 / Vt;
          addAbs(A, ind.acid, ci * (1 - f)); addAbs(A, ind.base, ci * f);
        }
        return { pH: pH, A: A, turb: [] };
      },
      result: function (Vend) {
        if (an.khp) { var c = nA / Vend; return { text: "c(NaOH) = " + Sim.fmtU(c, c * relU(Vend), "mol/L"), value: c, truth: cBottle, unit: "mol/L" }; }
        var ca = cLabel * Vend / Va;
        return { text: "c(acid) = " + Sim.fmtU(ca, ca * relU(Vend), "mol/L"), value: ca, truth: nA / Va, unit: "mol/L" };
      }
    };
    m.nA = nA; m.Ka = Ka; m.strong = !!an.strong;
    return m;
  }

  function bufferModel(solKey, titrantKey) {
    var s = SOLUTIONS[solKey], Va = 100.0, Ka = Math.pow(10, -4.757);
    var t = { hcl01: { c: 0.100, acid: true, name: "0.100 M HCl" }, hcl1: { c: 1.00, acid: true, name: "1.00 M HCl" }, naoh01: { c: 0.100, acid: false, name: "0.100 M NaOH" } }[titrantKey];
    return {
      Va: Va, cBottle: t.c, cLabel: t.c, Veq: null, titrant: t.name, name: s.name.replace(/^100\.0 mL of /, "").replace(/ \(.*/, "") + " + " + t.name,
      config: solKey + "|" + titrantKey, acidTitrant: t.acid,
      state: function (V, cEff) {
        var Vt = Va + V, add = cEff * V / Vt;
        var pH = solvePH(s.A / Vt + (t.acid ? 0 : add), t.acid ? add : 0, s.HA + s.A > 0 ? [{ C: (s.HA + s.A) / Vt, Ka: Ka }] : []);
        return { pH: pH, A: [0, 0, 0], turb: [] };
      },
      result: function () { return null; }
    };
  }

  function redoxModel(medium, ferroin) {
    var Va = 25.00, cFe = 0.0500, cCe = 0.1000, nFe = cFe * Va;
    var EFe = medium === "HClO4" ? 0.732 : 0.68, ECe = medium === "HClO4" ? 1.70 : 1.44, EIn = 1.147;
    var fe30 = nFe * 1e-4;   // a trace of Fe3+ in the sample sets the starting potential
    return {
      Va: Va, cBottle: cCe, cLabel: cCe, Veq: nFe / cCe, titrant: "0.1000 M Ce⁴⁺ in 1 M H₂SO₄",
      name: "Fe²⁺ + Ce⁴⁺ in 1 M " + (medium === "HClO4" ? "HClO₄" : "H₂SO₄") + (ferroin ? ", ferroin" : ""),
      config: medium + "|" + (ferroin ? "f" : "-"), EFe: EFe, ECe: ECe,
      state: function (V, cEff) {
        var nCe = cEff * V, Vt = Va + V;
        var E = bisect(function (e) {
          var x = 1 / (1 + Math.pow(10, (EFe - e) / NERNST)), y = 1 / (1 + Math.pow(10, (e - ECe) / NERNST));
          return nFe * x - fe30 - nCe * y;
        }, -0.5, 2.5, 90);
        var x = 1 / (1 + Math.pow(10, (EFe - E) / NERNST)), y = 1 / (1 + Math.pow(10, (E - ECe) / NERNST));
        var A = [0, 0, 0];
        addAbs(A, [0, 0.3, 3], nFe * x / Vt);            // Fe3+, pale yellow
        addAbs(A, [0, 20, 250], nCe * (1 - y) / Vt);     // Ce4+, yellow
        if (ferroin) {
          var fo = 1 / (1 + Math.pow(10, (EIn - E) / NERNST)), ci = 2.5e-5 * 50 / Vt;
          addAbs(A, [400, 11000, 4000], ci * (1 - fo));  // ferroin, red
          addAbs(A, [1400, 500, 60], ci * fo);           // ferriin, pale blue
        }
        return { E: E, A: A, turb: [] };
      },
      result: function (Vend) { var c = cCe * Vend / Va; return { text: "c(Fe²⁺) = " + Sim.fmtU(c, c * relU(Vend), "mol/L"), value: c, truth: cFe, unit: "mol/L" }; }
    };
  }

  function mohrModel(sample, pH, crMM) {
    var Va = 50.00, cAg = 0.02000, cCl = sample === "blank" ? 0 : 0.00800, nCl = cCl * Va;
    var KSP_CL = 1.8e-10, KSP_CR = 1.2e-12, KA_CR = Math.pow(10, -6.51), K_AGOH = 2.0e-8;
    var h = Math.pow(10, -pH), OH = KW / h, aCr = 1 / (1 + h / KA_CR), aMax = K_AGOH / OH;
    var m = {
      Va: Va, cBottle: cAg, cLabel: cAg, Veq: nCl / cAg, titrant: "0.02000 M AgNO₃", blank: sample === "blank",
      name: (sample === "blank" ? "reagent blank (CaCO₃)" : "chloride sample") + ", pH " + pH + ", CrO₄²⁻ " + crMM + " mM",
      config: sample + "|" + pH + "|" + crMM, blankKey: pH + "|" + crMM,
      state: function (V, cEff) {
        var Vt = Va + V, AgT = cEff * V / Vt, ClT = nCl / Vt, CrT = crMM * 1e-3 * Va / Vt;
        function parts(a) {
          var clFree = Math.min(ClT, KSP_CL / a), crBase = Math.min(CrT * aCr, KSP_CR / (a * a));
          return { pCl: ClT - clFree, pCr: CrT - crBase / aCr, crBase: crBase };
        }
        function f(la) { var a = Math.pow(10, la), p = parts(a); return a + p.pCl + 2 * p.pCr - AgT; }
        var laMax = Math.log10(aMax), a, p, pOH = 0;
        if (AgT <= 0) { a = 1e-20; p = parts(a); }
        else if (f(laMax) < 0) { a = aMax; p = parts(a); pOH = AgT - (a + p.pCl + 2 * p.pCr); }
        else { a = Math.pow(10, bisect(f, -20, laMax, 90)); p = parts(a); }
        var A = [0, 0, 0];
        addAbs(A, [0, 25, 300], p.crBase);
        addAbs(A, [0, 40, 250], p.crBase / aCr - p.crBase);
        var turb = [];
        if (m.blank) turb.push({ t: 0.38, col: [242, 242, 238] });
        turb.push({ t: 0.5 * (1 - Math.exp(-p.pCl / 3e-4)), col: [242, 242, 238] });
        var wCr = 1 - Math.exp(-p.pCr / 3e-5);
        turb.push({ t: 0.7 * wCr, col: [168, 62, 40] });
        var wOH = 1 - Math.exp(-pOH / 1e-5);
        if (pOH > 0) turb.push({ t: 0.75 * wOH, col: [86, 64, 48] });
        var desc;
        if (wOH > 0.15) desc = "dark brown-grey (silver oxide precipitating)";
        else if (wCr > 0.5) desc = "red-brown suspension";
        else if (wCr > 0.15) desc = "yellow suspension with a faint red-brown tint";
        else desc = (p.pCl > 1e-5 || m.blank ? "cloudy " : "") + "yellow";
        return { E: 0.7996 + NERNST * Math.log10(a), pAg: -Math.log10(a), A: A, turb: turb, milky: true, desc: desc };
      },
      result: function (Vend, blankV) {
        if (m.blank) return { text: "blank = " + Sim.fmt(Vend, 2) + " mL", value: Vend, truth: null, unit: "mL" };
        var b = blankV || 0, c = (Vend - b) * cAg / Va * 35.453 * 1000;
        return { text: "Cl⁻ = " + Sim.fmtU(c, c * relU(Vend), "mg/L") + (blankV ? " (blank " + Sim.fmt(b, 2) + " mL subtracted)" : " (no blank subtracted)"), value: c, truth: cCl * 35.453 * 1000, unit: "mg/L" };
      }
    };
    return m;
  }

  function edtaModel(pH, indKey) {
    var Va = 50.00, cY = 0.01000, nCa = 1.840e-3 * Va, nMg = 0.730e-3 * Va;   // mmol (Lesson 10.3 tap water)
    var h = Math.pow(10, -pH), OH = KW / h, aY = alphaY4(pH);
    var KCaY = Math.pow(10, 10.69) * aY, KMgY = Math.pow(10, 8.79) * aY;
    var I = indKey === "calcon" ? { k2: Math.pow(10, -9.3), k3: Math.pow(10, -13.0), lCa: 6.6, lMg: 0 } : { k2: Math.pow(10, -6.3), k3: Math.pow(10, -11.6), lCa: 5.4, lMg: 7.0 };
    var D = h * h + h * I.k2 + I.k2 * I.k3, fH2 = h * h / D, fH = h * I.k2 / D, fIn = I.k2 * I.k3 / D;
    var KCaIn = Math.pow(10, I.lCa) * fIn, KMgIn = I.lMg ? Math.pow(10, I.lMg) * fIn : 0;
    var mgPpt = pH >= 11.5;
    var veq = (nCa + (mgPpt ? 0 : nMg)) / cY;
    var m = {
      Va: Va, cBottle: cY, cLabel: cY, Veq: veq, titrant: "0.01000 M Na₂H₂Y (EDTA)", mgPpt: mgPpt,
      name: "tap water, pH " + pH + ", " + (indKey === "calcon" ? "calcon" : "Eriochrome Black T"), config: pH + "|" + indKey,
      logK: { Ca: Math.log10(KCaY), Mg: Math.log10(KMgY), aY: aY },
      state: function (V, cEff) {
        var Vt = Va + V, YT = cEff * V / Vt, CaT = nCa / Vt, MgT = nMg / Vt, InT = 3e-5 * 50 / Vt;
        if (mgPpt) MgT = Math.min(MgT, 7.1e-12 / (OH * OH));
        var Ca = CaT, Mg = MgT, In = InT;
        function inner(Y) {
          In = InT;
          for (var k = 0; k < 6; k++) {
            Ca = CaT / (1 + KCaY * Y + KCaIn * In);
            Mg = MgT / (1 + KMgY * Y + KMgIn * In);
            In = InT / (1 + KCaIn * Ca + KMgIn * Mg);
          }
        }
        var lY = bisect(function (ly) { var Y = Math.pow(10, ly); inner(Y); return Y * (1 + KCaY * Ca + KMgY * Mg) - YT; }, -30, 0, 80);
        inner(Math.pow(10, lY));
        var bound = InT - In, A = [0, 0, 0];
        addAbs(A, indKey === "calcon" ? [2500, 22000, 9000] : [2500, 24000, 8000], bound);   // metal–indicator complex, wine red
        if (indKey === "calcon") { addAbs(A, [3000, 20000, 6000], In * fH2); addAbs(A, [20000, 11000, 2000], In * fH); addAbs(A, [6000, 16000, 3000], In * fIn); }
        else { addAbs(A, [500, 20000, 12000], In * fH2); addAbs(A, [22000, 12000, 2000], In * fH); addAbs(A, [0, 9000, 20000], In * fIn); }
        return { pCa: -Math.log10(Ca), A: A, turb: mgPpt ? [{ t: 0.15, col: [240, 240, 236] }] : [], milky: mgPpt, freeInd: In / InT };
      },
      result: function (Vend) {
        var mmolL = cY * Vend / Va * 1000;
        if (mgPpt) { var ca = mmolL * 40.078; return { text: "Ca = " + Sim.fmtU(ca, ca * relU(Vend), "mg/L"), value: ca, truth: 1.840 * 40.078, unit: "mg/L Ca" }; }
        var hd = mmolL * 100.09;
        return { text: "hardness = " + Sim.fmtU(hd, hd * relU(Vend), "mg/L as CaCO₃"), value: hd, truth: (1.840 + 0.730) * 100.09, unit: "mg/L CaCO₃" };
      }
    };
    return m;
  }

  // standard uncertainty of a burette volume (Lesson 10.1 budget): tolerance 0.05/sqrt3,
  // two readings of ±0.02 mL, end point ± half a drop (rectangular)
  function uVol() { return Math.sqrt(Math.pow(0.05 / Math.sqrt(3), 2) + 2 * 0.02 * 0.02 + Math.pow(DROP / 2 / Math.sqrt(3), 2)); }
  function relU(V) { return V > 0 ? uVol() / V : 0; }

  /* ---------------- page state ---------------- */
  var preset = Sim.preset(PRESETS, "strong-acid");
  var seed = Sim.seedFromQuery(10);
  var mode = preset.mode;
  var cur = null, runs = [], blanks = {}, tapLoop = null, el = null;
  var plot = Sim.plot(Sim.$("#plot"), { xLabel: "titrant added (burette reading − initial) / mL", yLabel: "pH" });
  var dplot = Sim.plot(Sim.$("#dplot"), { xLabel: "volume / mL", yLabel: "ΔpH/ΔV / mL⁻¹" });
  var gplot = Sim.plot(Sim.$("#gplot"), { xLabel: "volume / mL", yLabel: "V·10^−pH / mL" });

  Sim.label();
  Sim.presetBox(Sim.$("#preset"), preset);
  Sim.$("#seed").textContent = String(seed);

  /* ---------------- electrodes and meters ---------------- */
  function newElectrode(age) {
    var r = Sim.rng(seed * 7 + (age === "aged" ? 3 : 1));
    var aged = age === "aged";
    return {
      age: age,
      slope: 1000 * NERNST * (aged ? r.uniform(0.86, 0.90) : r.uniform(0.980, 0.993)),   // mV per pH
      E0: (r.random() < 0.5 ? -1 : 1) * (aged ? r.uniform(10, 25) : r.uniform(5, 12)),   // mV at pH 7 (asymmetry and reference offset)
      tau: aged ? 12 : 3,                        // response time constant, s
      drift: aged ? 0.2 : 0.03,                  // mV per minute
      noise: aged ? 0.4 : 0.1,                   // mV
      cal: null, Es: null, rng: r
    };
  }
  function glassMV(pH, t) { return el.E0 + el.slope * (7 - pH) + el.drift * t / 60; }
  function meterPH(mv) { return el.cal ? el.cal.p1 + (el.cal.E1 - mv) / el.cal.s : 7 - mv / (1000 * NERNST); }

  function sensorKind() {
    if (mode === "potentiometric") return "glass";
    if (mode === "buffer") return "ideal";
    if (mode === "acidbase") return chk("s-meter") ? "ideal" : null;
    if (mode === "redox") return chk("s-pt") ? "pt" : null;
    if (mode === "precipitation") return chk("s-ag") ? "ag" : null;
    return null;
  }

  // one meter reading of the current flask after waiting `wait` seconds
  function takeReading(wait) {
    var st = cur.model.state(cur.Vdel, cur.cEff), k = cur.sensor, r = cur.rng, out = {};
    if (k === "ideal") { out.ph = st.pH + r.normal(0, 0.004); out.mv = 1000 * NERNST * (7 - out.ph); }
    else if (k === "glass") {
      var target = glassMV(st.pH, cur.clock);
      el.Es = el.Es === null ? target : target + (el.Es - target) * Math.exp(-wait / el.tau);
      out.mv = el.Es + r.normal(0, el.noise);
      out.ph = meterPH(out.mv);
    } else {
      var tE = 1000 * (st.E - E_AGCL), tau = 4;
      cur.Es = cur.Es === undefined || cur.Es === null ? tE : tE + (cur.Es - tE) * Math.exp(-wait / tau);
      out.mv = cur.Es + r.normal(0, 0.3);
    }
    return out;
  }

  function calibrate() {
    if (!el) el = newElectrode(Sim.$("#el-age").value);
    var pair = Sim.$("#el-buf").value === "7-10" ? [7.00, 10.01] : [7.00, 4.01];
    var t0 = cur ? cur.clock : 0, E = [];
    pair.forEach(function (p, i) {
      var target = glassMV(p, t0 + 150 * (i + 1));
      el.Es = el.Es === null ? target : target + (el.Es - target) * Math.exp(-150 / el.tau);
      E.push(el.Es + el.rng.normal(0, el.noise));
    });
    var s = (E[0] - E[1]) / (pair[1] - pair[0]);
    el.cal = { p1: pair[0], E1: E[0], s: s, p2: pair[1], E2: E[1], t: t0 };
    if (cur) cur.clock += 300;
    showElectrode();
  }

  function showElectrode() {
    var rows = [];
    if (!el) el = newElectrode(Sim.$("#el-age").value);
    if (el.cal) {
      rows.push(["buffer " + el.cal.p1.toFixed(2), el.cal.E1.toFixed(1) + " mV"]);
      rows.push(["buffer " + el.cal.p2.toFixed(2), el.cal.E2.toFixed(1) + " mV"]);
      rows.push(["slope", Math.abs(el.cal.s).toFixed(2) + " mV/pH (" + (100 * Math.abs(el.cal.s) / (1000 * NERNST)).toFixed(1) + " % of Nernst)"]);
      rows.push(["status", "calibrated"]);
    } else {
      rows.push(["status", "not calibrated: the meter assumes 0 mV at pH 7.00 and 59.16 mV/pH"]);
    }
    kvFill(Sim.$("#el-info"), rows);
  }

  /* ---------------- the burette ---------------- */
  var BUR = { cmPerMl: 1.14, rIn: 0.53, wall: 0.12, D: 25 };
  function parallaxMl(h) {   // apparent − true reading for an eye h cm above the meniscus (scale reads downward)
    var d = BUR.wall / 1.47 + BUR.rIn / 1.333;
    return -(h * d / (BUR.D + d)) / BUR.cmPerMl;
  }
  function eyeHeight() {
    var v = Sim.$("#eye").value;
    if (v === "free") return Math.max(-6, Math.min(6, cur.rng.normal(0, 2.5)));
    return parseFloat(v);
  }
  function trueLevel() { return cur.L0 + cur.Vdel + (cur.bubble && cur.bubble.out ? cur.bubble.vol : 0); }
  function readBurette() {
    var h = eyeHeight();
    cur.lastEye = h;
    var app = trueLevel() + parallaxMl(h) + cur.rng.normal(0, 0.006);
    cur.lastApp = app;
    return Math.round(app * 100) / 100;
  }

  function deliver(dv) {
    if (!cur || dv <= 0) return;
    cur.Vdel += dv;
    if (cur.bubble && !cur.bubble.out && cur.Vdel >= cur.bubble.at) {
      cur.bubble.out = true;
      cur.notes.push("An air bubble left the burette tip at about " + cur.bubble.at.toFixed(1) + " mL: the reading jumped by " + cur.bubble.vol.toFixed(2) + " mL that never reached the flask.");
    }
    if (trueLevel() > 50) cur.notes.push("The burette is below the 50 mL mark: refill and record a new initial reading in a real titration.");
  }

  function addPortion(kind) {
    if (!cur || tapOpen()) return;
    var r = cur.rng, dv;
    if (kind === "drop") dv = r.normal(DROP, 0.004);
    else if (kind === "half") dv = r.normal(DROP / 2, 0.004);
    else { var n = parseFloat(kind); dv = n * (1 + r.normal(0, n >= 1 ? 0.03 : 0.06)); }
    dv = Math.max(0.005, dv);
    deliver(dv);
    cur.clock += 5;
    afterAddition();
  }

  function tapOpen() { return !!tapLoop; }
  function toggleTap() {
    var b = Sim.$("#tap");
    if (!cur) return;
    if (tapLoop) {
      tapLoop.stop(); tapLoop = null;
      var late = cur.tapRate * cur.rng.uniform(0.1, 0.4);    // your hand closes the tap a little late
      deliver(late);
      b.setAttribute("aria-pressed", "false"); b.textContent = "Open the tap (stream)";
      afterAddition();
      return;
    }
    cur.tapRate = cur.rng.uniform(0.28, 0.38);   // mL per second
    b.setAttribute("aria-pressed", "true"); b.textContent = "Close the tap";
    tapLoop = Sim.loop(function (dt) {
      deliver(cur.tapRate * dt);
      cur.clock += dt;
      drawAll(false);
      return true;
    });
  }

  function afterAddition() {
    if (cur.sensor) {
      var wait = parseFloat(Sim.$("#m-wait").value);
      cur.clock += wait;
      var rd = takeReading(wait), x = readBurette() - cur.init;
      cur.readings.push({ V: x, ph: rd.ph, mv: rd.mv, t: cur.clock, Vtrue: cur.Vdel });
      cur.justRead = true;
    }
    if (cur.stopped && cur.runRef) refreshRun();
    drawAll(true);
  }

  /* ---------------- starting a titration ---------------- */
  function buildModel(rng) {
    if (mode === "acidbase") return acidModel(val("s-an"), val("s-tit"), val("s-ind"), rng);
    if (mode === "potentiometric") return acidModel(val("s-an"), "std", "none", rng);
    if (mode === "buffer") return bufferModel(val("s-sol"), val("s-tit"));
    if (mode === "redox") return redoxModel(val("s-med"), chk("s-fer"));
    if (mode === "precipitation") return mohrModel(val("s-sample"), parseFloat(val("s-ph")), parseFloat(val("s-cr")));
    return edtaModel(parseFloat(val("s-ph")), val("s-ind"));
  }

  function startTitration(first) {
    first = first === true;
    if (tapLoop) { tapLoop.stop(); tapLoop = null; Sim.$("#tap").setAttribute("aria-pressed", "false"); Sim.$("#tap").textContent = "Open the tap (stream)"; }
    var n = runs.length + 1;
    var r = Sim.rng(seed + 101 * n);
    var mrng = Sim.rng(seed + 17);   // the sample (unknowns, unstandardised titrant) depends on the seed only
    var model = buildModel(mrng);
    var t0 = cur ? cur.clock + 120 : 0;   // the bench clock runs on: electrode drift does not reset
    cur = {
      id: n, model: model, rng: r, Vdel: 0, clock: t0, t0: t0, readings: [], notes: [], stopped: false, revealed: false,
      L0: r.uniform(0.2, 1.4), sensor: sensorKind(), Es: null,
      cEff: model.cBottle * (chk("prep-rinse") ? 1 : 1 - r.uniform(0.004, 0.008)),
      bubble: chk("prep-bubble") ? null : { vol: r.uniform(0.06, 0.16), at: r.uniform(1.5, 8), out: false }
    };
    if (!chk("prep-rinse")) cur.notes.push("Burette rinsed with water only: the titrant is slightly diluted.");
    if (cur.sensor === "glass") { if (!el) el = newElectrode(Sim.$("#el-age").value); el.Es = null; }
    if (first && preset.eye !== undefined) Sim.$("#eye").value = preset.eye;
    cur.init = readBurette();
    cur.initEye = cur.lastEye;
    cur.justRead = true;
    if (cur.sensor) { var rd = takeReading(60); cur.readings.push({ V: 0, ph: rd.ph, mv: rd.mv, t: t0, Vtrue: 0 }); }
    Sim.$("#stop").disabled = false;
    Sim.$("#stop").textContent = mode === "buffer" ? "Finish this run" : (visualEnd() ? "Stop: end point here" : "Finish: analyse the readings");
    Sim.$("#show-theory").checked = false;
    Sim.$("#cue").textContent = "";
    drawAll(true);
  }

  function visualEnd() {
    if (mode === "acidbase") return val("s-ind") !== "none";
    if (mode === "redox") return chk("s-fer");
    if (mode === "precipitation" || mode === "edta") return true;
    return false;
  }

  /* ---------------- end point and analysis ---------------- */
  function sigOf(p) {
    if (cur.sensor === "glass" && Sim.$("#m-show").value === "mv") return p.mv;
    if (cur.sensor === "pt" || cur.sensor === "ag") return p.mv;
    return p.ph;
  }
  function sortedReadings() {
    var pts = cur.readings.slice().sort(function (a, b) { return a.V - b.V; }), out = [];
    pts.forEach(function (p) {
      if (out.length && Math.abs(p.V - out[out.length - 1].V) < 0.004) out[out.length - 1] = p;   // same reading twice: keep the later one
      else out.push(p);
    });
    return out;
  }

  // first-derivative peak and second-derivative zero crossing (Lessons 09.5 and 10.2)
  function derivEnd(pts) {
    if (pts.length < 4) return null;
    var vm = [], d1 = [];
    for (var i = 1; i < pts.length; i++) {
      var dv = pts[i].V - pts[i - 1].V;
      if (dv <= 0) continue;
      vm.push((pts[i].V + pts[i - 1].V) / 2);
      d1.push((sigOf(pts[i]) - sigOf(pts[i - 1])) / dv);
    }
    if (d1.length < 3) return null;
    var k = 0;
    for (var j = 1; j < d1.length; j++) if (Math.abs(d1[j]) > Math.abs(d1[k])) k = j;
    var out = { v1: vm[k], vm: vm, d1: d1, v2: null };
    if (k > 0 && k < d1.length - 1) {
      var xa = (vm[k - 1] + vm[k]) / 2, xb = (vm[k] + vm[k + 1]) / 2;
      var da = (d1[k] - d1[k - 1]) / (vm[k] - vm[k - 1]), db = (d1[k + 1] - d1[k]) / (vm[k + 1] - vm[k]);
      if (da * db < 0) out.v2 = xa + (xb - xa) * da / (da - db);
    }
    return out;
  }

  function interpAt(pts, V, key) {
    for (var i = 1; i < pts.length; i++) {
      if (pts[i].V >= V && pts[i - 1].V <= V) {
        var f = (V - pts[i - 1].V) / ((pts[i].V - pts[i - 1].V) || 1);
        return pts[i - 1][key] + f * (pts[i][key] - pts[i - 1][key]);
      }
    }
    return NaN;
  }

  function granFit(pts, vEnd) {
    var lo = parseFloat(Sim.$("#g-lo").value) / 100 * vEnd, hi = parseFloat(Sim.$("#g-hi").value) / 100 * vEnd;
    var xs = [], ys = [];
    pts.forEach(function (p) { if (p.V >= lo && p.V <= hi && p.V > 0) { xs.push(p.V); ys.push(p.V * Math.pow(10, -p.ph)); } });
    if (xs.length < 3) return { n: xs.length };
    var f = Sim.stats.linfit(xs, ys);
    return { n: xs.length, fit: f, veq: -f.a / f.b, ka: -f.b, xs: xs, ys: ys };
  }

  function stopHere() {
    if (!cur || cur.stopped) return;
    if (tapLoop) toggleTap();
    cur.stopped = true;
    cur.final = readBurette();
    cur.finalEye = cur.lastEye;
    var row = { c: cur.model.cLabel, id: cur.id, mode: mode, name: cur.model.name, config: mode + "|" + cur.model.config, Veq: cur.model.Veq, readings: cur.readings };
    if (mode === "buffer") {
      row.end = null;
    } else if (visualEnd()) {
      row.end = cur.final - cur.init;
      row.how = "by eye";
    } else {
      var d = derivEnd(sortedReadings());
      row.end = d ? (d.v2 !== null ? d.v2 : d.v1) : null;
      row.how = d && d.v2 !== null ? "2nd derivative" : "1st derivative";
    }
    row.trueDelivered = cur.Vdel;
    cur.runRef = row;
    runs.push(row);
    finishRow(row);
    Sim.$("#stop").disabled = true;
    renderRuns();
    drawAll(true);
  }

  function finishRow(row) {
    var m = cur.model;
    if (mode === "buffer") { var b = bufferSummary(); row.result = b ? b.text : "—"; row.value = b ? b.mmol : null; return; }
    if (row.end === null || !isFinite(row.end)) { row.result = "too few readings"; return; }
    if (mode === "precipitation" && m.blank) blanks[m.blankKey] = row.end;
    var res = m.result(row.end, mode === "precipitation" ? blanks[m.blankKey] : undefined);
    row.result = res ? res.text : "—";
    row.value = res ? res.value : null;
    row.truth = res ? res.truth : null;
  }

  function refreshRun() {
    var row = cur.runRef;
    if (!visualEnd() && mode !== "buffer") {
      var d = derivEnd(sortedReadings());
      if (d) { row.end = d.v2 !== null ? d.v2 : d.v1; row.how = d.v2 !== null ? "2nd derivative" : "1st derivative"; }
    }
    finishRow(row);
    renderRuns();
  }

  function bufferSummary() {
    var pts = sortedReadings();
    if (pts.length < 2) return null;
    var c = cur.model.cLabel, p0 = pts[0].ph, sign = cur.model.acidTitrant ? -1 : 1, target = p0 + sign;
    for (var i = 1; i < pts.length; i++) {
      var a = pts[i - 1].ph, b = pts[i].ph;
      if ((target - a) * (target - b) <= 0 && a !== b) {
        var V = pts[i - 1].V + (pts[i].V - pts[i - 1].V) * (target - a) / (b - a), mmol = V * c;
        return { V: V, mmol: mmol, text: Sim.fmt(mmol, 3) + " mmol for ΔpH = " + (sign < 0 ? "−1" : "+1") + " (" + Sim.fmt(V, 2) + " mL)" };
      }
    }
    return { V: null, mmol: null, text: "pH has not yet moved by 1 unit (now " + Sim.fmt(pts[pts.length - 1].ph - p0, 2) + ")" };
  }

  function reveal() {
    if (!cur) return;
    cur.revealed = true;
    drawAll(true);
  }

  /* ---------------- drawing ---------------- */
  function flaskColour(st) {
    var rgb = absToRGB(st.A);
    st.turb.forEach(function (tb) { if (tb.t > 0) rgb = mix(rgb, tb.col, tb.t); });
    return rgb;
  }
  function describe(st) {
    if (st.desc) return st.desc;
    return colourName(flaskColour(st), st.milky);
  }

  function setupCanvas(cv) {
    var dpr = window.devicePixelRatio || 1, w = cv.clientWidth || 300, h = cv.clientHeight || 220;
    if (cv.width !== Math.round(w * dpr) || cv.height !== Math.round(h * dpr)) { cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr); }
    var ctx = cv.getContext("2d");
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    return { ctx: ctx, w: w, h: h };
  }

  function drawFlask(st) {
    var c = setupCanvas(Sim.$("#flask")), ctx = c.ctx, W = c.w, H = c.h;
    ctx.fillStyle = Sim.color("plot-bg"); ctx.fillRect(0, 0, W, H);
    var cx = W / 2, top = 18, neck = 16, bw = Math.min(W * 0.42, 120), bot = H - 14, sh = top + 46;
    var rgb = flaskColour(st), level = sh + (bot - sh) * 0.32;
    // white tile under the flask, as on a real bench
    ctx.fillStyle = "#f4f4f2"; ctx.fillRect(cx - bw - 18, bot, 2 * bw + 36, 8);
    ctx.beginPath();
    ctx.moveTo(cx - neck / 2, top); ctx.lineTo(cx - neck / 2, sh); ctx.lineTo(cx - bw, bot); ctx.lineTo(cx + bw, bot); ctx.lineTo(cx + neck / 2, sh); ctx.lineTo(cx + neck / 2, top);
    ctx.save(); ctx.clip();
    ctx.fillStyle = "#fbfbfa"; ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = "rgb(" + rgb.map(function (v) { return Math.round(Math.max(0, Math.min(255, v))); }).join(",") + ")";
    ctx.fillRect(0, level, W, H);
    ctx.restore();
    ctx.strokeStyle = Sim.color("ink"); ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(cx - neck / 2, top); ctx.lineTo(cx - neck / 2, sh); ctx.lineTo(cx - bw, bot); ctx.lineTo(cx + bw, bot); ctx.lineTo(cx + neck / 2, sh); ctx.lineTo(cx + neck / 2, top);
    ctx.stroke();
    // burette tip above the flask
    ctx.fillStyle = Sim.color("muted"); ctx.fillRect(cx - 2, 0, 4, top - 4);
    if (tapOpen()) { ctx.strokeStyle = Sim.color("s1"); ctx.lineWidth = 1.5; ctx.beginPath(); ctx.moveTo(cx, top - 4); ctx.lineTo(cx, level); ctx.stroke(); }
    if (cur && cur.sensor) {
      ctx.fillStyle = Sim.color("muted"); ctx.fillRect(cx + neck / 2 + 6, 4, 7, level + 24 - 4);
      ctx.fillStyle = Sim.color("ink"); ctx.font = "11px " + getComputedStyle(document.body).fontFamily;
      ctx.textAlign = "left"; ctx.fillText(cur.sensor === "pt" ? "Pt | Ag/AgCl" : cur.sensor === "ag" ? "Ag | Ag/AgCl" : "pH electrode", cx + neck / 2 + 16, 14);
    }
  }

  function drawBurette() {
    var c = setupCanvas(Sim.$("#bview")), ctx = c.ctx, W = c.w, H = c.h;
    ctx.fillStyle = Sim.color("plot-bg"); ctx.fillRect(0, 0, W, H);
    if (!cur) return;
    var app = cur.lastApp !== undefined ? cur.lastApp : trueLevel(), span = 1.2, ppm = H / span;
    var x0 = W / 2 - 34, x1 = W / 2 + 34;
    function y(v) { return H / 2 + (v - app) * ppm; }
    // glass and liquid (the liquid is below the meniscus: larger readings are lower)
    ctx.fillStyle = Sim.isDark() ? "#26303a" : "#eef3f7"; ctx.fillRect(x0, 0, x1 - x0, H);
    var liq = mode === "redox" ? "rgba(235,200,40,0.55)" : "rgba(120,170,220,0.35)";
    ctx.fillStyle = liq; ctx.fillRect(x0, H / 2, x1 - x0, H / 2);
    ctx.strokeStyle = Sim.color("ink"); ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.moveTo(x0, H / 2 - 2); ctx.quadraticCurveTo((x0 + x1) / 2, H / 2 + 10, x1, H / 2 - 2); ctx.stroke();
    ctx.strokeRect(x0, -2, x1 - x0, H + 4);
    // scale on the front of the glass
    ctx.font = "11px " + getComputedStyle(document.body).fontFamily;
    ctx.fillStyle = Sim.color("ink"); ctx.textAlign = "right"; ctx.textBaseline = "middle";
    var start = Math.floor((app - span / 2) * 10) / 10;
    for (var v = start; v <= app + span / 2 + 0.1; v = Math.round((v + 0.1) * 10) / 10) {
      var Y = y(v), major = Math.abs(v - Math.round(v)) < 1e-6, half = Math.abs(v * 2 - Math.round(v * 2)) < 1e-6;
      ctx.beginPath(); ctx.moveTo(x0, Y); ctx.lineTo(x0 + (major ? 30 : half ? 20 : 12), Y); ctx.stroke();
      if (major) ctx.fillText(String(Math.round(v)), x0 - 6, Y);
    }
    // the bottom of the meniscus as you see it, and your sight line
    var h = cur.lastEye || 0;
    ctx.strokeStyle = Sim.color("s2"); ctx.setLineDash([4, 3]);
    ctx.beginPath(); ctx.moveTo(x1 + 40, H / 2 - h * 12); ctx.lineTo(x0, H / 2 + 4); ctx.stroke(); ctx.setLineDash([]);
    ctx.textAlign = "left"; ctx.fillStyle = Sim.color("muted");
    ctx.fillText("eye " + (Math.abs(h) < 0.05 ? "level" : Math.abs(h).toFixed(1) + " cm " + (h > 0 ? "above" : "below")), x1 + 8, Math.max(12, Math.min(H - 10, H / 2 - h * 12 - 12)));
  }

  function curState() { return cur.model.state(cur.Vdel, cur.cEff); }

  function drawAll(full) {
    if (!cur) return;
    if (full && !cur.stopped && !cur.justRead) readBurette();
    cur.justRead = false;
    var st = curState();
    drawFlask(st);
    drawBurette();
    Sim.$("#colour-name").textContent = mode === "buffer" ? "colourless (no indicator)" : describe(st);
    // a flash where the drop lands warns that the end point is close
    var cue = "";
    if (visualEnd() && !cur.stopped) {
      var ahead = cur.model.state(cur.Vdel + 0.35, cur.cEff);
      if (describe(ahead) !== describe(st)) cue = "Where the titrant lands the colour flashes to " + describe(ahead) + " and fades as you swirl: you are close. Go drop by drop.";
    }
    if (cur.notes.length) cue += (cue ? " " : "") + cur.notes[cur.notes.length - 1];
    Sim.$("#cue").textContent = cue;
    var rows = [["titration", "#" + cur.id + ": " + cur.model.name], ["titrant", cur.model.titrant]];
    if (cur.sensor && cur.readings.length) {
      var last = cur.readings[cur.readings.length - 1];
      rows.push(["meter", cur.sensor === "pt" || cur.sensor === "ag" ? last.mv.toFixed(1) + " mV vs Ag/AgCl" : (Sim.$("#m-show").value === "mv" && cur.sensor === "glass" ? last.mv.toFixed(1) + " mV" : last.ph.toFixed(2) + " pH")]);
    }
    rows.push(["time on this titration", Math.round(cur.clock - cur.t0) + " s"]);
    kvFill(Sim.$("#live"), rows);
    var br = [["initial reading", cur.init.toFixed(2) + " mL"]];
    if (cur.stopped) br.push(["final reading", cur.final.toFixed(2) + " mL"], ["volume", (cur.final - cur.init).toFixed(2) + " mL"]);
    else br.push(["reading now", (cur.lastApp !== undefined ? Math.round(cur.lastApp * 100) / 100 : cur.init).toFixed(2) + " mL"]);
    if (cur.revealed && cur.model.Veq !== null) br.push(["equivalence", cur.model.Veq.toFixed(3) + " mL delivered (true " + cur.Vdel.toFixed(3) + " mL so far)"]);
    kvFill(Sim.$("#bur-info"), br);
    if (full) { drawCurves(); analyse(); }
  }

  function sigLabel() {
    if (cur.sensor === "pt" || cur.sensor === "ag") return ["E / mV vs Ag/AgCl", "ΔE/ΔV / mV mL⁻¹"];
    if (cur.sensor === "glass" && Sim.$("#m-show").value === "mv") return ["E / mV", "ΔE/ΔV / mV mL⁻¹"];
    return ["pH (meter)", "ΔpH/ΔV / mL⁻¹"];
  }

  function theoryCurve(xmax) {
    var out = [], m = cur.model, n = 240;
    for (var i = 0; i <= n; i++) {
      var V = xmax * i / n, st = m.state(V, cur.cEff), y;
      if (cur.sensor === "pt" || cur.sensor === "ag") y = 1000 * (st.E - E_AGCL);
      else if (cur.sensor === "glass" && Sim.$("#m-show").value === "mv") y = glassMV(st.pH, 0);
      else y = st.pH;
      out.push([V, y]);
    }
    return out;
  }

  function drawCurves() {
    var show = !!cur.sensor;
    Sim.$("#curve-panel").hidden = !show;
    if (!show) return;
    var pts = sortedReadings(), lab = sigLabel();
    var data = pts.map(function (p) { return [mode === "buffer" ? p.V * cur.model.cLabel : p.V, sigOf(p)]; });
    var series = [];
    if (mode === "buffer") {
      // keep the earlier buffer runs on the same axes for comparison
      runs.forEach(function (r, i) {
        if (r.mode !== "buffer" || r === cur.runRef) return;
        var c = r.c;
        series.push({ type: "line", width: 1.5, color: "s" + ((i % 5) + 2), label: r.name, data: r.readings.map(function (p) { return [p.V * c, p.ph]; }).sort(function (a, b) { return a[0] - b[0]; }) });
      });
    }
    series.push({ type: "points", color: "s1", label: "this run", data: data });
    if (Sim.$("#show-theory").checked && cur.stopped && mode !== "buffer") {
      var xmax = Math.max(1, pts.length ? pts[pts.length - 1].V : 1);
      series.push({ type: "line", color: "s3", width: 1.5, dash: [5, 4], label: "exact curve (true volumes)", data: theoryCurve(xmax) });
    }
    if (cur.revealed && cur.model.Veq !== null) series.push({ type: "vline", x: cur.model.Veq, color: "s2", dash: [3, 3], label: "equivalence" });
    plot.draw(series, { yLabel: lab[0], xLabel: mode === "buffer" ? "strong " + (cur.model.acidTitrant ? "acid" : "base") + " added / mmol" : "titrant added (burette reading − initial) / mL" });
    Sim.$("#curve-title").textContent = mode === "buffer" ? "pH against strong acid or base added" : "Titration curve from your readings";
    var showD = mode !== "buffer";
    Sim.$("#dplot").hidden = !showD;
    var d = derivEnd(pts);
    if (showD) {
      var ds = d ? [{ type: "line", color: "s4", label: "first derivative", data: d.vm.map(function (v, i) { return [v, d.d1[i]]; }) }] : [];
      if (d && d.v2 !== null) ds.push({ type: "vline", x: d.v2, color: "s2", dash: [4, 3], label: "2nd-derivative zero" });
      dplot.draw(ds, { yLabel: lab[1] });
    }
    var showG = (mode === "potentiometric" || mode === "acidbase") && cur.model.Ka && cur.sensor !== null;
    Sim.$("#gplot").hidden = !showG; Sim.$("#gran-row").hidden = !showG;
    if (showG && d) {
      var vEnd = d.v2 !== null ? d.v2 : d.v1, g = granFit(pts, vEnd);
      var gs = [{ type: "points", color: "s1", label: "V·10^−pH", data: pts.filter(function (p) { return p.V > 0 && p.V < vEnd; }).map(function (p) { return [p.V, p.V * Math.pow(10, -p.ph)]; }) }];
      if (g.fit) gs.push({ type: "line", color: "s2", label: "fit, x-intercept " + g.veq.toFixed(2) + " mL", data: [[0, g.fit.a], [g.veq, 0]] });
      gplot.draw(gs, { yMin: 0 });
    } else if (showG) gplot.draw([]);
  }

  function analyse() {
    var rows = [], m = cur.model, pts = sortedReadings();
    if (cur.stopped && cur.runRef) {
      var r = cur.runRef;
      if (r.end !== null && r.end !== undefined) rows.push(["end point (" + (r.how || "") + ")", r.end.toFixed(2) + " mL"]);
      if (m.Veq !== null && r.end !== null && m.Veq > 0) {
        var err = 100 * (r.end - m.Veq) / m.Veq, drops = (r.end - m.Veq) / DROP;
        rows.push(["titration error", (err >= 0 ? "+" : "") + err.toFixed(2) + " % (" + (drops >= 0 ? "+" : "") + drops.toFixed(1) + " drops)", Math.abs(err) < 0.2 ? "hit" : "miss"]);
      }
      if (r.result && mode !== "buffer") rows.push(["result", r.result]);
      if (r.truth) rows.push(["true value", Sim.sig(r.truth, 4) + " " + (m.blank ? "" : (r.value !== null ? "(" + (100 * (r.value - r.truth) / r.truth >= 0 ? "+" : "") + (100 * (r.value - r.truth) / r.truth).toFixed(2) + " %)" : ""))]);
      if (mode !== "buffer") rows.push(["burette budget", "u(V) = " + uVol().toFixed(3) + " mL (tolerance, two readings, ½ drop)"]);
      if (visualEnd() && (Math.abs(cur.initEye) > 0.5 || Math.abs(cur.finalEye) > 0.5)) rows.push(["parallax", "eye " + cur.initEye.toFixed(1) + " cm and " + cur.finalEye.toFixed(1) + " cm from level: " + ((parallaxMl(cur.finalEye) - parallaxMl(cur.initEye)) >= 0 ? "+" : "") + (parallaxMl(cur.finalEye) - parallaxMl(cur.initEye)).toFixed(3) + " mL on the volume", "miss"]);
      // repeats of the same experiment
      var same = runs.filter(function (q) { return q.config === r.config && q.value !== null && q.value !== undefined && isFinite(q.value); }).map(function (q) { return q.value; });
      if (same.length >= 2) {
        var mu = Sim.stats.mean(same), sd = Sim.stats.sd(same), t = Sim.stats.tInv(0.95, same.length - 1);
        rows.push(["repeats (n = " + same.length + ")", "mean " + Sim.sig(mu, 5) + ", s = " + Sim.sig(sd, 2) + ", 95 % CI ± " + Sim.sig(t * sd / Math.sqrt(same.length), 2)]);
      }
    } else rows.push(["status", visualEnd() ? "Titrate, and press Stop at the first lasting colour change." : (mode === "buffer" ? "Add acid or base and watch the pH; press Finish to log the run." : "Add titrant and log readings through the jump; Finish analyses them.")]);
    if (cur.sensor && pts.length >= 4 && mode !== "buffer") {
      var d = derivEnd(pts);
      if (d) {
        rows.push(["1st-derivative peak", d.v1.toFixed(3) + " mL"]);
        if (d.v2 !== null) rows.push(["2nd-derivative zero", d.v2.toFixed(3) + " mL"]);
        var vE = d.v2 !== null ? d.v2 : d.v1;
        if ((mode === "potentiometric" || mode === "acidbase") && m.Ka) {
          var pk = interpAt(pts, vE / 2, "ph");
          if (isFinite(pk)) rows.push(["pH at half the end point", pk.toFixed(3) + " (pKa 4.757)"]);
          var g = granFit(pts, vE);
          if (g.fit) rows.push(["Gran plot (" + g.n + " points)", "V_eq = " + g.veq.toFixed(3) + " mL, pKa = " + (-Math.log10(g.ka)).toFixed(3)]);
          else rows.push(["Gran plot", "needs at least 3 readings in the window (" + g.n + " now)"]);
        }
        if (mode === "redox") {
          var e1 = interpAt(pts, vE / 2, "mv"), e2 = interpAt(pts, 2 * vE, "mv");
          if (isFinite(e1)) rows.push(["E at half-equivalence", (e1 / 1000).toFixed(3) + " V vs Ag/AgCl = " + (e1 / 1000 + E_AGCL).toFixed(3) + " V vs SHE (E°′ Fe)"]);
          rows.push(["E at twice the end point", isFinite(e2) ? (e2 / 1000).toFixed(3) + " V vs Ag/AgCl = " + (e2 / 1000 + E_AGCL).toFixed(3) + " V vs SHE (E°′ Ce)" : "titrate on to " + (2 * vE).toFixed(1) + " mL to read it"]);
        }
      }
    }
    if (mode === "buffer") {
      var b = bufferSummary();
      if (b) {
        rows.push(["start pH", pts[0].ph.toFixed(2)]);
        rows.push(["acid or base for 1 pH unit", b.text]);
        if (b.mmol) rows.push(["average capacity", Sim.sig(b.mmol / 1000 / 0.1, 2) + " mol L⁻¹ per pH unit over that range"]);
      }
      var bufRuns = runs.filter(function (q) { return q.mode === "buffer" && q.value; });
      if (bufRuns.length >= 2) rows.push(["ratio of the last two runs", Sim.fmt(Math.max(bufRuns[bufRuns.length - 1].value, bufRuns[bufRuns.length - 2].value) / Math.min(bufRuns[bufRuns.length - 1].value, bufRuns[bufRuns.length - 2].value), 2)]);
    }
    if (mode === "edta") rows.push(["conditional constants", "log K′ CaY " + m.logK.Ca.toFixed(2) + ", MgY " + m.logK.Mg.toFixed(2) + " (α Y⁴⁻ = " + Sim.sig(m.logK.aY, 2) + ")" + (m.mgPpt ? "; Mg(OH)₂ precipitated" : "")]);
    if (mode === "precipitation" && !m.blank) rows.push(["blank for these conditions", blanks[m.blankKey] !== undefined ? blanks[m.blankKey].toFixed(2) + " mL" : "none yet: choose Reagent blank as the sample and titrate it"]);
    kvFill(Sim.$("#analysis"), rows);
  }

  function kvFill(box, rows) {
    box.textContent = "";
    rows.forEach(function (r) { box.appendChild(Sim.el("div", { text: r[0] })); box.appendChild(Sim.el("div", { text: r[1], class: r[2] || null })); });
  }

  function renderRuns() {
    var tb = Sim.$("#runs tbody");
    tb.textContent = "";
    runs.forEach(function (r) {
      var err = r.end !== null && r.end !== undefined && r.Veq ? 100 * (r.end - r.Veq) / r.Veq : NaN;
      tb.appendChild(Sim.el("tr", {},
        Sim.el("td", { text: String(r.id) }), Sim.el("td", { text: r.name }),
        Sim.el("td", { text: r.end !== null && r.end !== undefined ? r.end.toFixed(2) : "—" }),
        Sim.el("td", { text: r.Veq !== null && r.Veq !== undefined ? r.Veq.toFixed(2) : "—" }),
        Sim.el("td", { text: isFinite(err) ? (err >= 0 ? "+" : "") + err.toFixed(2) + " %" : "—" }),
        Sim.el("td", { text: r.result || "—" })));
    });
  }

  /* ---------------- set-up forms ---------------- */
  function val(id) { var e = Sim.$("#" + id); return e ? e.value : null; }
  function chk(id) { var e = Sim.$("#" + id); return !!(e && e.checked); }
  function field(id, label, input) { return Sim.el("div", { class: "field" }, Sim.el("label", { for: id, html: label }), input); }
  function sel(id, opts, def) {
    var s = Sim.el("select", { id: id });
    opts.forEach(function (o) { s.appendChild(Sim.el("option", { value: o[0], text: o[1] })); });
    if (def !== undefined && def !== null) s.value = def;
    return s;
  }
  function box(id, label, on) { return Sim.el("div", { class: "row" }, Sim.el("label", {}, Sim.el("input", { type: "checkbox", id: id, checked: !!on }), " " + label)); }

  var TITLES = { acidbase: "Acid–base titration with an indicator", potentiometric: "Potentiometric acid–base titration", buffer: "Buffer capacity", redox: "Iron(II) with cerium(IV)", precipitation: "Chloride by the Mohr method", edta: "Total hardness with EDTA" };

  function buildSetup(first) {
    var b = Sim.$("#setup");
    b.textContent = "";
    Sim.$("#setup-title").textContent = TITLES[mode];
    var p = first ? preset : {};
    if (mode === "acidbase") {
      b.appendChild(field("s-an", "Sample in the flask", sel("s-an", [["HCl", ANALYTES.HCl.name], ["AcOH", ANALYTES.AcOH.name], ["KHP", ANALYTES.KHP.name], ["UNK", ANALYTES.UNK.name]], p.analyte || "HCl")));
      b.appendChild(field("s-tit", "Titrant in the burette", sel("s-tit", [["std", "0.1000 M NaOH (standardised)"], ["nom", "NaOH, about 0.1 M (standardise it with KHP)"]], "std")));
      var ik = Object.keys(INDICATORS).filter(function (k) { return k !== "none"; }).map(function (k) { return [k, INDICATORS[k].name]; });
      ik.push(["none", "no indicator (pH meter only)"]);
      b.appendChild(field("s-ind", "Indicator (two drops)", sel("s-ind", ik, p.indicator || "php")));
      b.appendChild(box("s-meter", "pH meter in the flask (calibrated), log the curve", p.meter));
    } else if (mode === "potentiometric") {
      b.appendChild(field("s-an", "Sample in the beaker", sel("s-an", [["AcOH08", ANALYTES.AcOH08.name], ["HCl08", ANALYTES.HCl08.name]], "AcOH08")));
      b.appendChild(Sim.el("p", { class: "small muted", text: "Titrant 0.1000 M NaOH. No indicator: the electrode follows the titration." }));
    } else if (mode === "buffer") {
      b.appendChild(field("s-sol", "Solution in the beaker", sel("s-sol", Object.keys(SOLUTIONS).map(function (k) { return [k, SOLUTIONS[k].name]; }), p.solution || "buf10")));
      b.appendChild(field("s-tit", "Added from the burette", sel("s-tit", [["hcl01", "0.100 M HCl"], ["hcl1", "1.00 M HCl"], ["naoh01", "0.100 M NaOH"]], "hcl01")));
      b.appendChild(Sim.el("p", { class: "small muted", text: "A calibrated pH meter is in the beaker. 1 mL of 0.100 M acid is 0.100 mmol." }));
    } else if (mode === "redox") {
      b.appendChild(field("s-med", "Medium", sel("s-med", [["H2SO4", "1 M H₂SO₄ (E°′ Ce 1.44 V)"], ["HClO4", "1 M HClO₄ (E°′ Ce 1.70 V)"]], "H2SO4")));
      b.appendChild(box("s-fer", "Ferroin indicator (red → pale blue at about 1.15 V)", true));
      b.appendChild(box("s-pt", "Platinum electrode against Ag/AgCl, log the potential", false));
      b.appendChild(Sim.el("p", { class: "small muted", text: "25.00 mL of 0.0500 M Fe²⁺ titrated with 0.1000 M Ce⁴⁺." }));
    } else if (mode === "precipitation") {
      b.appendChild(field("s-sample", "Sample", sel("s-sample", [["cl", "50.00 mL water sample (stated Cl⁻ 283.6 mg/L)"], ["blank", "Reagent blank: 50 mL water + CaCO₃, no chloride"]], "cl")));
      b.appendChild(field("s-ph", "pH of the sample", sel("s-ph", [["5", "5 (acidic)"], ["6", "6"], ["7", "7"], ["8", "8 (as recommended)"], ["9", "9"], ["10", "10"], ["11", "11"], ["12", "12 (too basic)"]], "8")));
      b.appendChild(field("s-cr", "Chromate in the flask / mM", sel("s-cr", [["2.5", "2.5"], ["5", "5 (usual)"], ["10", "10"]], "5")));
      b.appendChild(box("s-ag", "Silver electrode against Ag/AgCl, log the potential", false));
      b.appendChild(Sim.el("p", { class: "small muted", text: "Titrant 0.02000 M AgNO₃. A blank is remembered for each pH and chromate level and subtracted from later results." }));
    } else if (mode === "edta") {
      b.appendChild(field("s-ph", "Buffer pH", sel("s-ph", [["8", "8"], ["9", "9"], ["10", "10 (NH₃/NH₄Cl, as recommended)"], ["12", "12 (NaOH: Mg(OH)₂ precipitates)"]], "10")));
      b.appendChild(field("s-ind", "Indicator", sel("s-ind", [["ebt", "Eriochrome Black T (wine red → blue)"], ["calcon", "calcon, a calcium indicator for pH 12–13"]], "ebt")));
      b.appendChild(Sim.el("p", { class: "small muted", text: "50.00 mL of tap water titrated with 0.01000 M EDTA. Stated hardness 257 mg/L as CaCO₃ (Ca 73.7 mg/L, Mg 17.7 mg/L)." }));
    }
    Sim.$$("select, input", b).forEach(function (e) { e.addEventListener("change", function () { if (mode === "edta" && e.id === "s-ph") Sim.$("#s-ind").value = e.value === "12" ? "calcon" : "ebt"; startTitration(); }); });
    Sim.$("#electrode-panel").hidden = mode !== "potentiometric";
    Sim.$("#meter-panel").hidden = !(mode === "potentiometric" || mode === "redox" || mode === "precipitation" || mode === "acidbase" || mode === "buffer");
    Sim.$("#m-show").parentNode.hidden = mode !== "potentiometric";
  }

  /* ---------------- manganese in steel (colorimetric, periodate) ---------------- */
  var MN_EPS = 2.4e3, MN_M = 54.938;          // L mol-1 cm-1 at 525 nm; g/mol
  var mnData = null;
  var mnPlot = Sim.plot(Sim.$("#mn-plot"), { xLabel: "Mn in the measured solution / mg L⁻¹", yLabel: "absorbance at 525 nm" });
  function mnRun() {
    var r = Sim.rng(seed * 3 + 11), mass = parseFloat(Sim.$("#mn-mass").value);
    var wTrue = Sim.rng(seed * 5 + 2).uniform(0.55, 1.35);    // % Mn in this steel (hidden)
    var slope = MN_EPS / MN_M / 1000;                          // absorbance per mg/L in 1 cm
    var fOx = (chk("mn-io4") ? 1 : r.uniform(0.86, 0.93)) * (chk("mn-nox") ? 1 : r.uniform(0.85, 0.92));
    var aFe = chk("mn-h3po4") ? 0.004 : r.uniform(0.05, 0.07), aOther = 0.012;   // yellow Fe3+ and coloured Cr/Ni ions at 525 nm
    function A(x) { return x + r.normal(0, 0.002); }
    var stds = [0, 2, 4, 6, 8, 10].map(function (c) { return { name: "standard " + c + " mg/L", c: c, A: A(0.003 + slope * c) }; });
    // 100.0 mL of solution from `mass` g; 10.00 mL aliquot taken through the colour step to 100.0 mL
    var cSample = mass * 1000 * wTrue / 100 / 0.1 * 10 / 100;    // mg/L in the measured solution
    var reps = [0, 1, 2].map(function () { return A(0.003 + slope * cSample * fOx + aFe + aOther); });
    var blankA = A(aFe + aOther);
    var fit = Sim.stats.linfit(stds.map(function (s) { return s.c; }), stds.map(function (s) { return s.A; }));
    var yS = Sim.stats.mean(reps) - (chk("mn-blank") ? blankA : 0);
    var c = (yS - fit.a) / fit.b;
    var xs = stds.map(function (s) { return s.c; }), xm = Sim.stats.mean(xs), sxx = 0;
    xs.forEach(function (x) { sxx += (x - xm) * (x - xm); });
    var uc = fit.s / fit.b * Math.sqrt(1 / 3 + 1 / xs.length + Math.pow(yS - Sim.stats.mean(stds.map(function (s) { return s.A; })), 2) / (fit.b * fit.b * sxx));
    var w = c * 0.1 * 10 / (mass * 1000) * 100, uw = w * uc / c;
    mnData = { stds: stds, reps: reps, blankA: blankA, fit: fit, c: c, w: w, uw: uw, wTrue: wTrue, mass: mass };
    var tb = Sim.$("#mn-table tbody");
    tb.textContent = "";
    stds.forEach(function (s) { tb.appendChild(Sim.el("tr", {}, Sim.el("td", { text: s.name }), Sim.el("td", { text: s.c.toFixed(1) }), Sim.el("td", { text: s.A.toFixed(4) }))); });
    reps.forEach(function (a, i) { tb.appendChild(Sim.el("tr", {}, Sim.el("td", { text: "sample, replicate " + (i + 1) }), Sim.el("td", { text: "?" }), Sim.el("td", { text: a.toFixed(4) }))); });
    tb.appendChild(Sim.el("tr", {}, Sim.el("td", { text: "reagent blank (aliquot without periodate)" }), Sim.el("td", { text: "—" }), Sim.el("td", { text: blankA.toFixed(4) })));
    var probs = [];
    if (!chk("mn-nox")) probs.push("nitrogen oxides left in the solution used up periodate and reduced some permanganate: low");
    if (!chk("mn-io4")) probs.push("the oxidation to MnO₄⁻ was incomplete: low");
    if (!chk("mn-h3po4")) probs.push("yellow Fe³⁺ absorbs at 525 nm" + (chk("mn-blank") ? " (the blank removes most of it)" : ": high"));
    if (!chk("mn-blank")) probs.push("no reagent blank: the colour of Fe³⁺, Cr and Ni ions is counted as manganese: high");
    kvFill(Sim.$("#mn-result"), [
      ["calibration", "A = " + fit.a.toFixed(4) + " + " + fit.b.toFixed(5) + " c (r² = " + fit.r2.toFixed(5) + ")"],
      ["sample (mean of 3" + (chk("mn-blank") ? ", minus blank" : "") + ")", yS.toFixed(4)],
      ["Mn in the measured solution", Sim.fmtU(c, uc, "mg/L")],
      ["Mn in the steel", Sim.fmtU(w, uw, "%")],
      ["certified value of this steel", wTrue.toFixed(3) + " % (" + (100 * (w - wTrue) / wTrue >= 0 ? "+" : "") + (100 * (w - wTrue) / wTrue).toFixed(1) + " %)", Math.abs(w - wTrue) / wTrue < 0.02 ? "hit" : "miss"],
      ["what went wrong", probs.length ? probs.join("; ") : "nothing: every step done"]
    ]);
    mnPlot.draw([
      { type: "points", color: "s1", label: "standards", data: stds.map(function (s) { return [s.c, s.A]; }) },
      { type: "line", color: "s1", width: 1.5, data: [[0, fit.a], [10, fit.a + 10 * fit.b]] },
      { type: "hline", y: yS, color: "s2", dash: [4, 3], label: "sample" + (chk("mn-blank") ? " − blank" : "") },
      { type: "points", color: "s2", data: [[c, yS]], size: 5 }
    ], { xMin: 0, yMin: 0 });
  }
  Sim.$("#mn-run").addEventListener("click", mnRun);
  Sim.$("#mn-rerun").addEventListener("click", function () { seed = Sim.newSeed(seed); Sim.$("#seed").textContent = String(seed); mnRun(); });
  Sim.exportCSV(Sim.$("#mn-x"), "manganese_steel.csv", function () {
    if (!mnData) return null;
    var rows = mnData.stds.map(function (s) { return ["standard", s.c, +s.A.toFixed(5)]; });
    mnData.reps.forEach(function (a) { rows.push(["sample", "", +a.toFixed(5)]); });
    rows.push(["reagent_blank", "", +mnData.blankA.toFixed(5)]);
    return { header: ["solution", "Mn_mg_per_L", "A_525"], rows: rows, filename: "manganese_steel_" + mnData.mass + "g.csv" };
  });

  /* ---------------- events ---------------- */
  Sim.$$("#add-row [data-add]").forEach(function (b) { b.addEventListener("click", function () { addPortion(b.getAttribute("data-add")); }); });
  Sim.$("#tap").addEventListener("click", toggleTap);
  Sim.$("#tap").setAttribute("aria-pressed", "false");
  Sim.$("#stop").addEventListener("click", stopHere);
  Sim.$("#reveal").addEventListener("click", reveal);
  Sim.$("#start").addEventListener("click", startTitration);
  Sim.$("#rerun").addEventListener("click", function () { seed = Sim.newSeed(seed); Sim.$("#seed").textContent = String(seed); el = null; startTitration(); showElectrode(); });
  ["#prep-rinse", "#prep-bubble"].forEach(function (s) { Sim.$(s).addEventListener("change", startTitration); });
  Sim.$("#eye").addEventListener("change", function () { if (cur && !cur.stopped) { readBurette(); drawAll(false); } });
  Sim.$("#el-cal").addEventListener("click", calibrate);
  Sim.$("#el-uncal").addEventListener("click", function () { if (el) el.cal = null; showElectrode(); });
  Sim.$("#el-age").addEventListener("change", function () { el = newElectrode(Sim.$("#el-age").value); showElectrode(); if (mode === "potentiometric") startTitration(); });
  ["#m-show", "#show-theory", "#g-lo", "#g-hi"].forEach(function (s) { Sim.$(s).addEventListener("change", function () { if (cur) { drawCurves(); analyse(); } }); });
  Sim.$("#m-show").addEventListener("change", function () { if (cur && cur.runRef) refreshRun(); });
  if (typeof window.ResizeObserver === "function") {
    try { new window.ResizeObserver(function () { if (cur) { drawFlask(curState()); drawBurette(); } }).observe(Sim.$("#flask")); } catch (e) { /* ignore */ }
  }
  Sim.onTheme(function () { if (cur) { drawFlask(curState()); drawBurette(); } });

  Sim.exportCSV(Sim.$("#x-run"), "titration_readings.csv", function () {
    if (!cur) return null;
    if (cur.sensor) {
      return { header: ["V_mL", "pH", "E_mV", "time_s"], rows: sortedReadings().map(function (p) { return [+p.V.toFixed(2), cur.sensor === "pt" || cur.sensor === "ag" ? "" : +p.ph.toFixed(3), +p.mv.toFixed(1), Math.round(p.t - cur.t0)]; }), filename: "titration" + cur.id + "_" + mode + ".csv" };
    }
    if (!cur.stopped) return null;
    return { header: ["initial_reading_mL", "final_reading_mL", "volume_mL"], rows: [[cur.init, cur.final, +(cur.final - cur.init).toFixed(2)]], filename: "titration" + cur.id + "_" + mode + ".csv" };
  });
  Sim.exportCSV(Sim.$("#x-all"), "titrations.csv", function () {
    return { header: ["titration", "experiment", "end_point_mL", "equivalence_mL", "error_percent", "result"], rows: runs.map(function (r) {
      return [r.id, r.name, r.end !== null && r.end !== undefined ? +r.end.toFixed(3) : "", r.Veq ? +r.Veq.toFixed(3) : "", r.end && r.Veq ? +(100 * (r.end - r.Veq) / r.Veq).toFixed(3) : "", r.result || ""];
    }) };
  });

  var booted = false;
  var tabs = Sim.tabs(Sim.$("#tabs"), function (name) {
    if (name === "manganese") { if (!mnData) mnRun(); return; }
    var first = !booted;
    booted = true;
    mode = name;
    buildSetup(first || name === preset.mode);
    showElectrode();
    startTitration(first);
  });
  tabs.select(mode);
  if (mode === "potentiometric") showElectrode();
})();
