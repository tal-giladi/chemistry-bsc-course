/* ir-esr simulation, part 2: electron spin resonance (lesson 30.2). Defines window.IRESR_ESR(preset, seed),
 * called by ir-esr.js. Uses ../common/sim.js (global Sim).
 *
 * Constants CODATA 2022 (NIST): mu_B = 9.2740100657e-24 J/T, mu_N = 5.0507837393e-27 J/T,
 * g_e = 2.00231930436, g_p = 5.5856946893, g_d = 0.8574382335; g(14N) = 0.403761, g(13C) = 1.4048236
 * (nuclear g factors from the NIST/IAEA nuclear moment tables). h from Sim.C.
 * Methyl radical: g = 2.00255, |a_H| = 2.304 mT (Fessenden and Schuler, J. Chem. Phys. 39, 2147, 1963).
 * Hydrogen atom: A = 1420.405751768 MHz (hydrogen maser), g_J = 2.0022838 (bound-electron g, as in
 * labs/module-30/make_data.py). Exact levels from the 4 x 4 spin Hamiltonian (Breit-Rabi):
 * |+,+> and |-,-> are pure; |+,-> and |-,+> mix, E = -A/4 +- (1/2) sqrt((g_J mu_B B + g_p mu_N B)^2 + A^2).
 * Radical spectra are first order: B(m) = B0 - sum a_k m_k. n equivalent nuclei of spin I give
 * 2nI + 1 lines with intensities from (1 + x + ... + x^2I)^n.
 * Detection: field modulation with a lock-in amplifier. The recorded signal is the first harmonic
 * of the modulated absorption, computed numerically, so overmodulation broadens and distorts the lines.
 * Microwave saturation (homogeneous line): width x sqrt(1 + P/Psat), absorption x sqrt(P)/(1 + P/Psat);
 * Psat = 1 mW is a model value.
 */
(function (global) {
  "use strict";
  var MU_B = 9.2740100657e-24, MU_N = 5.0507837393e-27, G_E = 2.00231930436;
  var NUC = {
    H: { name: "¹H", I: 0.5, g: 5.5856946893 },
    D: { name: "²H", I: 1, g: 0.8574382335 },
    N: { name: "¹⁴N", I: 1, g: 0.403761 },
    C13: { name: "¹³C", I: 0.5, g: 1.4048236 }
  };
  var A_H_HZ = 1420.405751768e6, G_J_H = 2.0022838, PSAT = 1.0;

  global.IRESR_ESR = function (preset, seed0) {
    var C = Sim.C, S = Sim.stats;
    function $(id) { return document.getElementById(id); }
    function tr(cells) { var row = Sim.el("tr"); cells.forEach(function (c) { row.appendChild(Sim.el("td", { html: String(c) })); }); return row; }
    function kv(el, pairs) { el.textContent = ""; pairs.forEach(function (p) { el.appendChild(Sim.el("span", { html: p[0] })); el.appendChild(Sim.el("span", { html: p[1] })); }); }

    var st = { seed: seed0, spec: null, found: [] };
    var plot = Sim.plot($("esr-plot"), { xLabel: "B / mT", yLabel: "dχ″/dB (arb.)", legend: true });
    var fitPlot = Sim.plot($("esr-fitplot"), { xLabel: "line index (m)", yLabel: "B / mT", legend: false });

    function fieldFor(g, nuHz) { return C.h * nuHz / (g * MU_B) * 1e3; }   // mT

    /* ---------- the hydrogen atom, exact ---------- */
    function hFreq(Bt, mI) {
      var A = C.h * A_H_HZ, ez = G_J_H * MU_B * Bt, nz = NUC.H.g * MU_N * Bt;
      var root = 0.5 * Math.sqrt((ez + nz) * (ez + nz) + A * A);
      var E;
      if (mI > 0) E = (ez / 2 - nz / 2 + A / 4) - (-A / 4 - root);      // |+,+> <-> lower mixed state
      else E = (-A / 4 + root) - (-ez / 2 + nz / 2 + A / 4);             // upper mixed state <-> |-,->
      return E / C.h;
    }
    function hField(nuHz, mI) {
      var lo = 0.001, hi = 3.0;
      for (var k = 0; k < 200; k++) { var mid = 0.5 * (lo + hi); if (hFreq(mid, mI) > nuHz) hi = mid; else lo = mid; }
      return 0.5 * (lo + hi) * 1e3;
    }

    /* ---------- line list ---------- */
    function groupPattern(n, I) {
      var unit = [], k = Math.round(2 * I) + 1, out = [1];
      for (var i = 0; i < k; i++) unit.push(1);
      for (var j = 0; j < n; j++) {
        var nx = new Array(out.length + k - 1).fill(0);
        for (var a = 0; a < out.length; a++) for (var b = 0; b < k; b++) nx[a + b] += out[a] * unit[b];
        out = nx;
      }
      return out;   // index 0 is m = -nI
    }
    function vals() {
      var groups = [];
      for (var i = 1; i <= 3; i++) {
        var n = parseInt($("esr-n" + i).value, 10) || 0, t = $("esr-t" + i).value, a = parseFloat($("esr-a" + i).value) || 0;
        if (n > 0) groups.push({ n: n, nuc: NUC[t], key: t, a: a });
      }
      return {
        mode: $("esr-mode").value, nu: parseFloat($("esr-nu").value) * 1e9, g: parseFloat($("esr-g").value),
        groups: groups, dBpp: parseFloat($("esr-w").value), mod: parseFloat($("esr-mod").value),
        P: parseFloat($("esr-P").value), scans: parseInt($("esr-scans").value, 10),
        centre: parseFloat($("esr-c").value), span: parseFloat($("esr-span").value), shape: $("esr-shape").value
      };
    }
    function lineList(v) {
      if (v.mode === "hydrogen") {
        return [{ B: hField(v.nu, 0.5), w: 1, m: 0.5 }, { B: hField(v.nu, -0.5), w: 1, m: -0.5 }];
      }
      var B0 = fieldFor(v.g, v.nu), lines = [{ B: B0, w: 1, m: 0 }];
      v.groups.forEach(function (gr) {
        var pat = groupPattern(gr.n, gr.nuc.I), nI = gr.n * gr.nuc.I, nx = [];
        lines.forEach(function (l) {
          pat.forEach(function (w, k) { var m = k - nI; nx.push({ B: l.B - gr.a * m, w: l.w * w, m: l.m + m }); });
        });
        lines = nx;
      });
      return lines;
    }

    /* ---------- detected spectrum ---------- */
    function absorb(x, shape) { return shape === "gauss" ? Math.exp(-Math.LN2 * x * x) : 1 / (1 + x * x); }
    function compute(v) {
      var lines = lineList(v);
      var s = v.P / PSAT, widen = Math.sqrt(1 + s), ampP = Math.sqrt(v.P) / (1 + s);
      // half width at half maximum of the absorption for a given derivative peak-to-peak width
      var hw = (v.shape === "gauss" ? v.dBpp / 2 * 1.1774100 : v.dBpp * Math.sqrt(3) / 2) * widen;
      var lo = v.centre - v.span / 2, hi = v.centre + v.span / 2, n = 4000, dx = (hi - lo) / (n - 1);
      var Bm = Math.max(1e-6, v.mod), K = 48;
      var rng = Sim.rng(st.seed);
      var sig = 0.004 * Math.sqrt(16 / v.scans);
      var x = [], y = [];
      var wsum = lines.reduce(function (a, l) { return a + l.w; }, 0);
      for (var i = 0; i < n; i++) {
        var B = lo + i * dx, acc = 0;
        for (var k = 0; k < K; k++) {
          var th = Math.PI * (k + 0.5) / K, Bt = B + 0.5 * Bm * Math.cos(th), a = 0;
          for (var j = 0; j < lines.length; j++) a += lines[j].w * absorb((Bt - lines[j].B) / hw, v.shape);
          acc += a * Math.cos(th);
        }
        // first-harmonic amplitude, scaled so that a fixed spectrometer gain is used for every setting
        var val = (2 / K) * acc * ampP / wsum * 40;
        x.push(B); y.push(val + rng.normal(0, sig));
      }
      return { x: x, y: y, lines: lines, hw: hw, sig: sig };
    }

    /* ---------- line finder: zero crossings between a maximum and the following minimum ---------- */
    function findLines(sp) {
      var y = sp.y, x = sp.x, n = y.length, out = [];
      var sm = y.slice();
      for (var r = 0; r < 2; r++) { var t = sm.slice(); for (var i = 2; i < n - 2; i++) t[i] = (sm[i - 2] + sm[i - 1] + sm[i] + sm[i + 1] + sm[i + 2]) / 5; sm = t; }
      var thr = 6 * sp.sig;
      for (i = 1; i < n - 1; i++) {
        if (sm[i] > thr && sm[i] >= sm[i - 1] && sm[i] > sm[i + 1]) {
          for (var j = i + 1; j < n - 1; j++) {
            if (sm[j] <= 0 && sm[j - 1] > 0) {
              var Bz = x[j - 1] + (x[j] - x[j - 1]) * sm[j - 1] / (sm[j - 1] - sm[j]);
              var mn = 0, k = j; while (k < n - 1 && sm[k + 1] <= sm[k]) { k++; } mn = sm[k];
              if (-mn > thr) out.push({ B: Bz, pp: sm[i] - mn, dBpp: x[k] - x[i] });
              i = k; break;
            }
            if (sm[j] > sm[i]) { i = j - 1; break; }
          }
        }
      }
      return out;
    }

    function render() {
      var v = vals();
      $("esr-seed").textContent = st.seed;
      var isH = v.mode === "hydrogen";
      $("esr-groups").hidden = isH;
      $("esr-g-row").hidden = isH;
      if (!(v.span > 0)) return;
      var sp = compute(v);
      st.spec = sp; st.v = v;
      var series = [{ data: sp.x.map(function (b, i) { return [b, sp.y[i]]; }), color: "s1", width: 1.3, label: isH ? "exact (Breit–Rabi)" : "recorded derivative" }];
      if (isH) {
        var B0 = fieldFor(G_J_H, v.nu), a = C.h * A_H_HZ / (G_J_H * MU_B) * 1e3;
        series.push({ type: "vline", x: B0 - a / 2, color: "s2", dash: [5, 4], width: 1.2, label: "first order" });
        series.push({ type: "vline", x: B0 + a / 2, color: "s2", dash: [5, 4], width: 1.2 });
        series.push({ type: "vline", x: B0, color: "muted", dash: [2, 3], width: 1, label: "hν/(g_J μ_B)" });
      }
      plot.draw(series, { xMin: v.centre - v.span / 2, xMax: v.centre + v.span / 2 });
      // readouts
      var pairs = [];
      if (isH) {
        var Bx = hField(v.nu, 0.5), By = hField(v.nu, -0.5), B0h = fieldFor(G_J_H, v.nu);
        var ah = C.h * A_H_HZ / (G_J_H * MU_B) * 1e3, mid = (Bx + By) / 2;
        pairs.push(["free-atom field hν/(g<sub>J</sub>μ<sub>B</sub>)", Sim.fmt(B0h, 2) + " mT"],
          ["a = hA/(g<sub>J</sub>μ<sub>B</sub>)", Sim.fmt(ah, 2) + " mT"],
          ["exact lines (m<sub>I</sub> = +½, −½)", Sim.fmt(Bx, 2) + ", " + Sim.fmt(By, 2) + " mT"],
          ["first-order lines", Sim.fmt(B0h - ah / 2, 2) + ", " + Sim.fmt(B0h + ah / 2, 2) + " mT"],
          ["centre shift (exact − first order)", Sim.fmt(mid - B0h, 2) + " mT; a²/4B₀ = " + Sim.fmt(ah * ah / (4 * B0h), 2) + " mT"],
          ["exact spacing − a", Sim.fmt(By - Bx - ah, 2) + " mT"],
          ["naive g from the midpoint", Sim.fmt(C.h * v.nu / (MU_B * mid * 1e-3), 4) + " (true 2.0023)"]);
      } else {
        var B0r = fieldFor(v.g, v.nu), count = 1;
        v.groups.forEach(function (gr) { count *= Math.round(2 * gr.n * gr.nuc.I) + 1; });
        var pat = v.groups.length === 1 ? groupPattern(v.groups[0].n, v.groups[0].nuc.I).join(" : ") : (v.groups.length ? "product of the group patterns" : "1");
        var width = v.groups.reduce(function (s0, gr) { return s0 + 2 * gr.n * gr.nuc.I * gr.a; }, 0);
        pairs.push(["resonance field hν/(gμ<sub>B</sub>)", Sim.fmt(B0r, 2) + " mT"],
          ["lines expected Π(2n<sub>k</sub>I<sub>k</sub> + 1)", String(count) + " (distinct positions may coincide)"],
          ["intensities", pat],
          ["total width of the pattern", Sim.fmt(width, 3) + " mT"],
          ["absorption HWHM incl. saturation", Sim.fmt(sp.hw, 3) + " mT"],
          ["modulation / ΔB<sub>pp</sub>", Sim.fmt(v.mod / v.dBpp, 2) + (v.mod > v.dBpp / 3 ? " (overmodulated: keep below ⅓)" : "")]);
        v.groups.forEach(function (gr) { pairs.push([gr.n + " × " + gr.nuc.name + " (I = " + gr.nuc.I + ")", "a = " + gr.a + " mT = " + Sim.fmt(gr.a * 1e-3 * v.g * MU_B / C.h / 1e6, 1) + " MHz"]); });
      }
      if (v.P > 3 * PSAT) pairs.push(["power", "saturating: lines broaden and the signal falls"]);
      kv($("esr-out"), pairs);
    }

    function analyse() {
      if (!st.spec) render();
      var found = findLines(st.spec), v = st.v;
      st.found = found;
      var tb = $("esr-lines").querySelector("tbody");
      tb.textContent = "";
      found.forEach(function (f, i) { tb.appendChild(tr([i + 1, Sim.fmt(f.B, 3), Sim.fmt(f.pp, 3), Sim.fmt(f.dBpp, 3)])); });
      var out = $("esr-fitout");
      if (found.length < 2) { kv(out, [["fit", "need at least two lines in the sweep"]]); fitPlot.draw([]); return; }
      var N = found.length, xs = found.map(function (f, i) { return i - (N - 1) / 2; }), ys = found.map(function (f) { return f.B; });
      var lf = S.linfit(xs, ys);
      var B0 = lf.a, uB0 = lf.ua, g = C.h * v.nu / (MU_B * B0 * 1e-3), ug = g * uB0 / B0;
      var pairs = [["lines found", String(N)], ["centre B₀ (intercept)", Sim.fmtU(B0, uB0, "mT")],
        ["spacing a (slope)", Sim.fmtU(lf.b, lf.ub, "mT")], ["g = hν/(μ<sub>B</sub>B₀)", Sim.fmtU(g, ug)],
        ["a in frequency units", Sim.fmt(lf.b * 1e-3 * g * MU_B / C.h / 1e6, 1) + " MHz"],
        ["heights (normalised)", found.map(function (f) { return (f.pp / Math.min.apply(null, found.map(function (q) { return q.pp; }))).toFixed(1); }).join(" : ")]];
      if (v.mode === "hydrogen") pairs.push(["caution", "a straight line through 2 points always fits; the midpoint is biased by −a²/4B₀"]);
      kv(out, pairs);
      fitPlot.draw([{ data: xs.map(function (x, i) { return [x, ys[i]]; }), type: "points", color: "s1" },
        { data: [[xs[0], lf.a + lf.b * xs[0]], [xs[N - 1], lf.a + lf.b * xs[N - 1]]], color: "s2", width: 1.5 }]);
    }

    function autoCentre() {
      var v = vals();
      if (v.mode === "hydrogen") { var c = (hField(v.nu, 0.5) + hField(v.nu, -0.5)) / 2; $("esr-c").value = c.toFixed(1); $("esr-span").value = 90; }
      else {
        var B0 = fieldFor(v.g, v.nu), w = v.groups.reduce(function (s0, gr) { return s0 + 2 * gr.n * gr.nuc.I * gr.a; }, 0);
        $("esr-c").value = B0.toFixed(2); $("esr-span").value = Math.max(4, Math.ceil(w * 1.6 + 2)).toFixed(0);
      }
    }

    function applyMode(m) {
      $("esr-mode").value = m === "hydrogen" ? "hydrogen" : "radical";
      if (m === "hydrogen") { $("esr-w").value = 0.12; }
      else { $("esr-g").value = 2.00255; $("esr-n1").value = 0; $("esr-t1").value = "H"; $("esr-a1").value = 2.304; $("esr-w").value = 0.06; }
      autoCentre();
    }

    // nucleus type change: keep the spin density, rescale a by the nuclear g factor (a_D = a_H g_d/g_p)
    [1, 2, 3].forEach(function (i) {
      var sel = $("esr-t" + i);
      sel.dataset.prev = sel.value;
      sel.addEventListener("change", function () {
        var prev = NUC[sel.dataset.prev], now = NUC[sel.value], a = parseFloat($("esr-a" + i).value);
        if (prev && now && isFinite(a)) $("esr-a" + i).value = +(a * now.g / prev.g).toPrecision(4);
        sel.dataset.prev = sel.value;
        autoCentre(); render();
      });
      $("esr-n" + i).addEventListener("change", function () { autoCentre(); render(); });
      $("esr-a" + i).addEventListener("change", function () { autoCentre(); render(); });
      $("esr-plus" + i).addEventListener("click", function () { var el = $("esr-n" + i); el.value = Math.min(8, (parseInt(el.value, 10) || 0) + 1); autoCentre(); render(); });
      $("esr-minus" + i).addEventListener("click", function () { var el = $("esr-n" + i); el.value = Math.max(0, (parseInt(el.value, 10) || 0) - 1); autoCentre(); render(); });
    });
    ["esr-w", "esr-mod", "esr-P", "esr-scans", "esr-c", "esr-span", "esr-shape", "esr-g"].forEach(function (id) { $(id).addEventListener("change", render); });
    $("esr-nu").addEventListener("change", function () { autoCentre(); render(); });
    $("esr-band").addEventListener("change", function () { if ($("esr-band").value) { $("esr-nu").value = $("esr-band").value; autoCentre(); render(); } });
    $("esr-mode").addEventListener("change", function () { applyMode($("esr-mode").value); render(); });
    $("esr-auto").addEventListener("click", function () { autoCentre(); render(); });
    $("esr-rerun").addEventListener("click", function () { st.seed = Sim.newSeed(st.seed); render(); if (st.found.length) analyse(); });
    $("esr-find").addEventListener("click", analyse);
    Sim.exportCSV($("esr-csv"), "esr_spectrum.csv", function () {
      var sp = st.spec || compute(vals());
      return { header: ["B_mT", "dchi_dB"], rows: sp.x.map(function (b, i) { return [b.toFixed(4), sp.y[i].toFixed(5)]; }) };
    });
    Sim.exportCSV($("esr-lcsv"), "esr_lines.csv", function () {
      return { header: ["line", "B_mT", "peak_to_peak", "dBpp_mT"], rows: st.found.map(function (f, i) { return [i + 1, f.B.toFixed(4), f.pp.toFixed(4), f.dBpp.toFixed(4)]; }) };
    });

    applyMode(preset.esr === "hydrogen" ? "hydrogen" : "radical");
    return { render: render };
  };
})(typeof window !== "undefined" ? window : this);
