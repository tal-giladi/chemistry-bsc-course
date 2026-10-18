/* nmr simulation, part 1: spin-system engine and molecule data (lessons 17.3, 17.5).
 * Defines the global NMR = {MOLECULES, UNKNOWNS, spectrumLines, firstOrder, GAMMA_H}.
 *
 * Physics. Each coupled cluster of protons is solved exactly (no n+1 shortcut): the Hamiltonian
 *   H/h = sum_i nu_i Iz_i + sum_{i<j} J_ij I_i . I_j    (nu_i = delta_i x spectrometer MHz, in Hz)
 * is built in the product basis, split into blocks of equal total Mz, and each block is diagonalised
 * with the cyclic Jacobi method. Lines are the transitions of I- = sum_i I_i^- between neighbouring
 * blocks, with intensity |<b|I-|a>|^2. When |delta nu| >> J this reproduces the n+1 rule with Pascal
 * heights; when delta nu/J approaches 1 it gives roofing, extra lines and AB/A2B3 patterns.
 * Magnetically equivalent protons (a CH3) are expanded into separate spins with no coupling among
 * themselves (couplings inside an equivalent set do not change the spectrum).
 * gamma/2pi of 1H = 42.577478 MHz/T (CODATA 2022, shielded-proton value differs in the 5th digit).
 *
 * Data. Chemical shifts (ppm, CDCl3) and couplings (Hz) are rounded typical textbook values, chosen to
 * match lesson 17.3 and 17.5 (OpenStax Organic Chemistry ch. 13; Hans Reich's NMR tables). They are not
 * copied from SDBS; compare them with the real SDBS spectra as the lessons ask.
 */
(function (global) {
  "use strict";
  var GAMMA_H = 42.577478;   // MHz/T

  /* site: [label, nH, delta, extraWidthHz, multiplicity text, assignment]
   * J: [siteIndex, siteIndex, J in Hz] */
  function mol(name, formula, sites, J, extra) {
    var m = { name: name, formula: formula, sites: sites.map(function (s) { return { label: s[0], n: s[1], d: s[2], w: s[3] || 0, mult: s[4], assign: s[5] }; }), J: J };
    if (extra) Object.keys(extra).forEach(function (k) { m[k] = extra[k]; });
    return m;
  }
  // monosubstituted benzene ring as three sites (ortho 2H, meta 2H, para 1H), strongly coupled
  function phenyl(o, mm, p, assign) {
    return { sites: [["o-H", 2, o, 0, "m", assign + " (ortho)"], ["m-H", 2, mm, 0, "m", assign + " (meta)"], ["p-H", 1, p, 0, "m", assign + " (para)"]],
      J: [[0, 1, 7.7], [1, 2, 7.5], [0, 2, 1.2]] };
  }
  function withRing(name, formula, before, ring, after, J, extra) {
    var sites = before.concat(ring.sites, after || []);
    var off = before.length;
    var JJ = (J || []).concat(ring.J.map(function (j) { return [j[0] + off, j[1] + off, j[2]]; }));
    return mol(name, formula, sites, JJ, extra);
  }

  var MOLECULES = {
    bromoethane: mol("bromoethane, CH₃CH₂Br", "C₂H₅Br",
      [["CH₂Br", 2, 3.43, 0, "q", "CH₂ next to Br (3 neighbours)"], ["CH₃", 3, 1.67, 0, "t", "CH₃ (2 neighbours)"]], [[0, 1, 7.3]]),
    chloropropane: mol("2-chloropropane, (CH₃)₂CHCl", "C₃H₇Cl",
      [["CHCl", 1, 4.14, 0, "septet", "CH next to Cl (6 neighbours)"], ["2 × CH₃", 6, 1.54, 0, "d", "two equivalent CH₃ (1 neighbour)"]], [[0, 1, 6.5]]),
    nitropropane: mol("1-nitropropane, CH₃CH₂CH₂NO₂", "C₃H₇NO₂",
      [["CH₂NO₂", 2, 4.37, 0, "t", "CH₂ next to NO₂"], ["CH₂", 2, 2.03, 0, "sextet", "middle CH₂ (5 neighbours)"], ["CH₃", 3, 1.03, 0, "t", "CH₃"]],
      [[0, 1, 7.0], [1, 2, 7.4]]),
    butanoic: mol("butanoic acid, CH₃CH₂CH₂COOH", "C₄H₈O₂",
      [["COOH", 1, 11.8, 18, "br s", "carboxylic acid OH (exchanging)"], ["CH₂C=O", 2, 2.35, 0, "t", "CH₂ next to C=O"], ["CH₂", 2, 1.68, 0, "sextet", "middle CH₂"], ["CH₃", 3, 0.98, 0, "t", "CH₃"]],
      [[1, 2, 7.5], [2, 3, 7.4]]),
    isobutyric: mol("2-methylpropanoic acid, (CH₃)₂CHCOOH", "C₄H₈O₂",
      [["COOH", 1, 11.9, 18, "br s", "carboxylic acid OH"], ["CH", 1, 2.58, 0, "septet", "CH next to C=O"], ["2 × CH₃", 6, 1.21, 0, "d", "two CH₃"]], [[1, 2, 7.0]]),
    ab: mol("AB pair: two coupled CH protons (δ 4.00 and 3.80, J = 10 Hz)", "—",
      [["Hₐ", 1, 4.00, 0, "d", "proton A"], ["H_b", 1, 3.80, 0, "d", "proton B"]], [[0, 1, 10]])
  };

  // unknowns for lesson 17.5 part A; each has a formula, candidate names and the answer
  var ESTER4 = ["butanoic acid", "2-methylpropanoic acid", "ethyl acetate", "methyl propanoate"];
  var ESTER5 = ["propyl acetate", "methyl butanoate", "ethyl propanoate", "isopropyl acetate", "methyl 2-methylpropanoate"];
  var ESTER6 = ["isobutyl acetate", "butyl acetate", "sec-butyl acetate", "ethyl butanoate"];
  var UNKNOWNS = [
    mol("butanoic acid", "C₄H₈O₂", MOLECULES.butanoic.sites.map(function (s) { return [s.label, s.n, s.d, s.w, s.mult, s.assign]; }), MOLECULES.butanoic.J,
      { candidates: ESTER4, why: "A 3H triplet, 2H sextet and 2H triplet: a CH₃CH₂CH₂ chain; the 2H triplet at 2.35 sits next to C=O; the broad 1H at 11.8 is COOH. 2-Methylpropanoic acid would show a 6H doublet and a 1H septet; the esters have no signal above 10 ppm." }),
    mol("ethyl acetate", "C₄H₈O₂",
      [["OCH₂", 2, 4.12, 0, "q", "OCH₂ of the ethyl ester"], ["CH₃C=O", 3, 2.05, 0, "s", "acetyl CH₃ (no neighbours)"], ["CH₃", 3, 1.26, 0, "t", "CH₃ of the ethyl group"]], [[0, 2, 7.1]],
      { candidates: ESTER4, why: "An ethyl group (2H quartet, 3H triplet) with the quartet at 4.12, so the CH₂ is on oxygen; a 3H singlet at 2.05 is CH₃C=O. Methyl propanoate would put the singlet at 3.7 (OCH₃) and the quartet at 2.3." }),
    mol("propyl acetate", "C₅H₁₀O₂",
      [["OCH₂", 2, 4.03, 0, "t", "OCH₂"], ["CH₃C=O", 3, 2.05, 0, "s", "acetyl CH₃"], ["CH₂", 2, 1.65, 0, "sextet", "middle CH₂"], ["CH₃", 3, 0.94, 0, "t", "CH₃"]], [[0, 2, 6.7], [2, 3, 7.4]],
      { candidates: ESTER5, why: "Singlet at 2.05 (CH₃C=O) and a 2H triplet at 4.03 (OCH₂ with 2 neighbours). Methyl butanoate has its singlet at 3.67 (OCH₃); ethyl propanoate has no singlet; isopropyl acetate would show a 1H septet near 5.0." }),
    mol("methyl butanoate", "C₅H₁₀O₂",
      [["OCH₃", 3, 3.67, 0, "s", "methyl ester OCH₃"], ["CH₂C=O", 2, 2.30, 0, "t", "CH₂ next to C=O"], ["CH₂", 2, 1.66, 0, "sextet", "middle CH₂"], ["CH₃", 3, 0.95, 0, "t", "CH₃"]], [[1, 2, 7.4], [2, 3, 7.4]],
      { candidates: ESTER5, why: "A 3H singlet at 3.67 is OCH₃ on oxygen; the 2H triplet at 2.30 is CH₂C=O; a propyl chain completes it. Propyl acetate would show its singlet at 2.05 and a triplet near 4.0." }),
    mol("isobutyl acetate", "C₆H₁₂O₂",
      [["OCH₂", 2, 3.85, 0, "d", "OCH₂ next to one CH"], ["CH₃C=O", 3, 2.05, 0, "s", "acetyl CH₃"], ["CH", 1, 1.93, 0, "m (nonet)", "CH (8 neighbours)"], ["2 × CH₃", 6, 0.93, 0, "d", "two CH₃"]], [[0, 2, 6.7], [2, 3, 6.7]],
      { candidates: ESTER6, why: "The OCH₂ at 3.85 is a doublet, so it sits next to a single CH; a 6H doublet is an isopropyl end. Butyl acetate would show a triplet OCH₂; sec-butyl acetate an OCH near 4.9; ethyl butanoate a quartet at 4.1." }),
    mol("4'-methoxyacetophenone", "C₉H₁₀O₂",
      [["ArH (2,6)", 1, 7.93, 0, "d (AA′BB′)", "ring H next to C=O"], ["ArH (2,6)′", 1, 7.93, 0, "d (AA′BB′)", "ring H next to C=O"],
        ["ArH (3,5)", 1, 6.93, 0, "d (AA′BB′)", "ring H next to OCH₃"], ["ArH (3,5)′", 1, 6.93, 0, "d (AA′BB′)", "ring H next to OCH₃"],
        ["OCH₃", 3, 3.87, 0, "s", "aryl methyl ether"], ["CH₃C=O", 3, 2.55, 0, "s", "methyl ketone"]],
      [[0, 2, 8.9], [1, 3, 8.9], [0, 3, 0.4], [1, 2, 0.4], [0, 1, 2.2], [2, 3, 2.6]],
      { candidates: ["4'-methoxyacetophenone", "methyl 4-methylbenzoate", "2'-methoxyacetophenone", "ethyl benzoate"], why: "Two 2H 'doublets' with J ≈ 9 Hz: a para-disubstituted ring (really AA′BB′, look closely). One ring pair at 6.93 is shielded by an O substituent; singlets at 3.87 (OCH₃) and 2.55 (CH₃C=O). Methyl 4-methylbenzoate would show its ring CH₃ at 2.40 and the ring H at 7.94 and 7.23; ¹³C (197 vs 167 ppm) decides it firmly. The ortho isomer has four different ring H; ethyl benzoate has a quartet and five ring H." }),
    withRing("(E)-cinnamaldehyde", "C₉H₈O",
      [["CHO", 1, 9.70, 0, "d", "aldehyde H (J ≈ 7.7 Hz to its neighbour)"], ["Ph–CH=", 1, 7.48, 0, "d", "alkene H next to the ring (J ≈ 16 Hz: trans)"], ["=CH–CHO", 1, 6.71, 0, "dd", "alkene H next to CHO"]],
      phenyl(7.56, 7.42, 7.43, "ring H"), [], [[0, 2, 7.7], [1, 2, 16.0]],
      { candidates: ["(E)-cinnamaldehyde", "(Z)-cinnamaldehyde", "4-vinylbenzaldehyde", "1-phenylprop-2-yn-1-ol"], why: "A 1H doublet at 9.70 is an aldehyde next to a CH; the alkene H couple with J ≈ 16 Hz, so they are trans; five ring H mean a monosubstituted benzene. The Z isomer would have J ≈ 12 Hz; 4-vinylbenzaldehyde a singlet CHO and two 2H ring doublets; the alkynol a ≡C–H near 2.6 and a CH(OH) near 5.4." }),
    mol("butan-1-amine", "C₄H₁₁N",
      [["CH₂N", 2, 2.68, 0, "t", "CH₂ next to N"], ["CH₂", 2, 1.43, 0, "m", "CH₂ next to CH₂N"], ["CH₂", 2, 1.33, 0, "m", "CH₂ next to CH₃"], ["CH₃", 3, 0.91, 0, "t", "CH₃"], ["NH₂", 2, 1.10, 6, "br s", "NH₂ (exchanging, no coupling)"]],
      [[0, 1, 7.0], [1, 2, 7.3], [2, 3, 7.3]],
      { candidates: ["butan-1-amine", "2-methylpropan-1-amine", "butan-2-amine", "diethylamine"], why: "A 3H triplet at 0.91 and a 2H triplet at 2.68 (CH₂ on N) with two CH₂ between: a straight butyl chain. Isobutylamine would show a 6H doublet; butan-2-amine a 1H multiplet near 2.9 and a 3H doublet; diethylamine a quartet and a triplet only. The NH₂ is broad and does not split anything." })
  ];

  /* ---------- exact spin-system solver ---------- */

  function jacobi(A, n) {
    // A: Float64Array n*n symmetric (destroyed). Returns {e, V} with eigenvectors in the columns of V.
    var V = new Float64Array(n * n), i, j, k;
    for (i = 0; i < n; i++) V[i * n + i] = 1;
    for (var sweep = 0; sweep < 60; sweep++) {
      var off = 0;
      for (i = 0; i < n; i++) for (j = i + 1; j < n; j++) off += A[i * n + j] * A[i * n + j];
      if (off < 1e-18) break;
      for (var p = 0; p < n; p++) {
        for (var q = p + 1; q < n; q++) {
          var apq = A[p * n + q];
          if (Math.abs(apq) < 1e-14) continue;
          var app = A[p * n + p], aqq = A[q * n + q];
          var theta = (aqq - app) / (2 * apq);
          var t = (theta >= 0 ? 1 : -1) / (Math.abs(theta) + Math.sqrt(theta * theta + 1));
          var c = 1 / Math.sqrt(t * t + 1), s = t * c;
          for (k = 0; k < n; k++) {
            var akp = A[k * n + p], akq = A[k * n + q];
            A[k * n + p] = c * akp - s * akq;
            A[k * n + q] = s * akp + c * akq;
          }
          for (k = 0; k < n; k++) {
            var apk = A[p * n + k], aqk = A[q * n + k];
            A[p * n + k] = c * apk - s * aqk;
            A[q * n + k] = s * apk + c * aqk;
          }
          for (k = 0; k < n; k++) {
            var vkp = V[k * n + p], vkq = V[k * n + q];
            V[k * n + p] = c * vkp - s * vkq;
            V[k * n + q] = s * vkp + c * vkq;
          }
        }
      }
    }
    var e = new Float64Array(n);
    for (i = 0; i < n; i++) e[i] = A[i * n + i];
    return { e: e, V: V };
  }

  function popcount(x) { var c = 0; while (x) { c += x & 1; x >>= 1; } return c; }

  // nu: array of Hz per spin; Jm: function(i,j) -> Hz. Returns lines [{f, I}] with total intensity = N.
  function solveCluster(nu, Jm) {
    var N = nu.length, dim = 1 << N, blocks = [];
    for (var k = 0; k <= N; k++) blocks.push({ states: [], index: {} });
    for (var s = 0; s < dim; s++) { var b = blocks[popcount(s)]; b.index[s] = b.states.length; b.states.push(s); }
    blocks.forEach(function (bl) {
      var n = bl.states.length, A = new Float64Array(n * n);
      for (var a = 0; a < n; a++) {
        var st = bl.states[a], diag = 0;
        for (var i = 0; i < N; i++) {
          var mi = (st >> i) & 1 ? 0.5 : -0.5;
          diag += nu[i] * mi;
          for (var j = i + 1; j < N; j++) {
            var J = Jm(i, j);
            if (!J) continue;
            var mj = (st >> j) & 1 ? 0.5 : -0.5;
            diag += J * mi * mj;
            if (((st >> i) & 1) !== ((st >> j) & 1)) {
              var t = st ^ ((1 << i) | (1 << j));
              A[a * n + bl.index[t]] += J / 2;
            }
          }
        }
        A[a * n + a] += diag;
      }
      var r = jacobi(A, n);
      bl.e = r.e; bl.V = r.V; bl.n = n;
    });
    var lines = [], norm = Math.pow(2, N - 1);
    for (k = 1; k <= N; k++) {
      var up = blocks[k], dn = blocks[k - 1];
      for (var p = 0; p < up.n; p++) {
        var w = new Float64Array(dn.n);
        for (var a = 0; a < up.n; a++) {
          var cf = up.V[a * up.n + p];
          if (Math.abs(cf) < 1e-12) continue;
          var st = up.states[a];
          for (var i = 0; i < N; i++) if ((st >> i) & 1) w[dn.index[st ^ (1 << i)]] += cf;
        }
        for (var q = 0; q < dn.n; q++) {
          var amp = 0;
          for (var bb = 0; bb < dn.n; bb++) amp += dn.V[bb * dn.n + q] * w[bb];
          var I = amp * amp / norm;
          if (I > 1e-5) lines.push({ f: up.e[p] - dn.e[q], I: I });
        }
      }
    }
    return lines;
  }

  // all lines of a molecule at a given spectrometer frequency (MHz); f in Hz from TMS
  function spectrumLines(m, MHz) {
    var spins = [];
    m.sites.forEach(function (s, si) { for (var k = 0; k < s.n; k++) spins.push(si); });
    var Jsite = {};
    m.J.forEach(function (j) { Jsite[j[0] + "," + j[1]] = j[2]; Jsite[j[1] + "," + j[0]] = j[2]; });
    // clusters of coupled sites
    var parent = m.sites.map(function (s, i) { return i; });
    function find(x) { while (parent[x] !== x) x = parent[x] = parent[parent[x]]; return x; }
    m.J.forEach(function (j) { if (j[2]) parent[find(j[0])] = find(j[1]); });
    var groups = {};
    m.sites.forEach(function (s, i) { var r = find(i); (groups[r] = groups[r] || []).push(i); });
    var out = [];
    Object.keys(groups).forEach(function (g) {
      var siteIdx = groups[g], sp = [];
      siteIdx.forEach(function (si) { for (var k = 0; k < m.sites[si].n; k++) sp.push(si); });
      var width = Math.max.apply(null, siteIdx.map(function (si) { return m.sites[si].w; }));
      if (sp.length > 11) {   // safety fallback, not used by the data above
        firstOrder(m, MHz).forEach(function (l) { if (siteIdx.indexOf(l.site) >= 0) out.push({ f: l.f, I: l.I, w: width }); });
        return;
      }
      var nu = sp.map(function (si) { return m.sites[si].d * MHz; });
      var lines = solveCluster(nu, function (i, j) { return sp[i] === sp[j] ? 0 : (Jsite[sp[i] + "," + sp[j]] || 0); });
      lines.forEach(function (l) { out.push({ f: l.f, I: l.I, w: width }); });
    });
    return out;
  }

  // first-order (n+1 rule) prediction: each coupled site splits again with Pascal heights
  function firstOrder(m, MHz) {
    var out = [];
    m.sites.forEach(function (s, si) {
      var lines = [{ f: s.d * MHz, I: s.n }];
      m.J.forEach(function (j) {
        var other = j[0] === si ? j[1] : j[1] === si ? j[0] : -1;
        if (other < 0 || !j[2]) return;
        var n = m.sites[other].n, nx = [];
        var row = [1]; for (var r = 0; r < n; r++) { var nr = [1]; for (var c = 1; c < row.length; c++) nr.push(row[c - 1] + row[c]); nr.push(1); row = nr; }
        var tot = Math.pow(2, n);
        lines.forEach(function (l) { row.forEach(function (h, k) { nx.push({ f: l.f + (k - n / 2) * j[2], I: l.I * h / tot }); }); });
        lines = nx;
      });
      lines.forEach(function (l) { l.site = si; out.push(l); });
    });
    return out;
  }

  global.NMR = { MOLECULES: MOLECULES, UNKNOWNS: UNKNOWNS, spectrumLines: spectrumLines, firstOrder: firstOrder, solveCluster: solveCluster, GAMMA_H: GAMMA_H };
})(typeof window !== "undefined" ? window : this);
