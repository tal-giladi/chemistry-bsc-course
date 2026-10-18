/* simulations/common/sim.js — shared helpers for the course simulations.
 *
 * Classic script (no ES modules: they do not load from file:// in Chrome).
 * Load it before the page's own script:
 *   <link rel="stylesheet" href="../common/sim.css">
 *   <script src="../common/sim.js"></script>
 *   <script src="mysim.js"></script>
 * Everything lives on the global object `Sim`. No network, no cookies, no
 * alert/prompt/confirm, no parent or top access: safe in an iframe sandboxed
 * with allow-scripts only.
 *
 * API
 * ---
 * Constants (CODATA 2022, exact unless noted; source: NIST physics.nist.gov/cuu):
 *   Sim.C.R = 8.314462618 J/(mol K)    Sim.C.kB = 1.380649e-23 J/K
 *   Sim.C.NA = 6.02214076e23 /mol      Sim.C.h = 6.62607015e-34 J s
 *   Sim.C.c = 299792458 m/s            Sim.C.e = 1.602176634e-19 C
 *   Sim.C.F = 96485.33212 C/mol        Sim.C.g = 9.80665 m/s^2 (standard)
 *   Sim.C.u = 1.66053906892e-27 kg (atomic mass constant, CODATA 2022)
 *   Sim.C.atm = 101325 Pa              Sim.C.bar = 1e5 Pa
 *
 * Page scaffolding
 *   Sim.LABEL                      the label text "Educational model — not a real instrument"
 *   Sim.label(el?)                 put the label badge into el (or every [data-sim-label]); returns the node
 *   Sim.$(sel, root?) / Sim.$$(sel, root?)   querySelector / querySelectorAll (array)
 *   Sim.el(tag, attrs?, ...children)         create an element; attrs: {class, text, html, on:{click:fn}, ...attributes}
 *   Sim.presetBox(el, info)        render {title, what, task, target} into el (explanation + task with target)
 *   Sim.tabs(container, onSelect)  wire buttons [data-tab] in container as an ARIA tab list; returns {select(name)}
 *   Sim.log(el, text)              append a line to a log box and scroll it
 *
 * URL query and presets
 *   Sim.query()                    {key: value} from location.search (safe if location is opaque)
 *   Sim.param(name, fallback)      one query value (string), or fallback
 *   Sim.num(name, fallback)        numeric query value, or fallback
 *   Sim.preset(presets, defKey)    picks presets[?preset] (or defKey); returns {key, ...presets[key]}
 *                                  unknown names fall back to defKey and set .unknown = the bad name
 *
 * Random numbers (deterministic)
 *   Sim.seedFromQuery(def?)        integer seed from ?seed=<n>, else def, else a time-based one
 *   Sim.rng(seed)                  -> {seed, random(), uniform(a,b), normal(mu,sd), int(a,b), pick(arr), tri(a,b)}
 *                                  mulberry32 core; normal() by Box–Muller
 *   Sim.newSeed(old)               a different seed for a "re-run" button
 *
 * Storage (optional, all failures swallowed)
 *   Sim.store.get(key, fallback)   JSON value from localStorage, or fallback
 *   Sim.store.set(key, value)      returns true on success
 *
 * Numbers and statistics
 *   Sim.fmt(x, digits=3)           fixed decimals; "—" for non-finite
 *   Sim.sig(x, n=3)                n significant figures as a string
 *   Sim.fmtU(x, u, unit?)          "x ± u unit" with u to 2 sig figs and x rounded to match
 *   Sim.stats.mean(a) / sd(a) / sum(a) / min(a) / max(a)
 *   Sim.stats.tInv(p, df)          two-sided Student t: value t with P(|T|<t) = p (e.g. 0.95)
 *   Sim.stats.tCdf(t, df)          Student t cumulative distribution
 *   Sim.stats.linfit(x, y)         least squares y = a + b x -> {a, b, ua, ub, s, r2, n, cov}
 *   Sim.stats.linfitThrough0(x, y) y = b x -> {b, ub, s, n}
 *   Sim.stats.percentile(sortedArr, p)   p in [0,1]
 *   Sim.stats.histogram(a, lo, hi, bins) -> {edges, counts, width}
 *
 * CSV export (data: link with download, plus a copyable text fallback because
 * a sandboxed iframe without allow-downloads may block the download)
 *   Sim.csv(header[], rows[][])    CSV text (RFC 4180 quoting), LF line endings
 *   Sim.exportCSV(button, filename, getData, outEl?)
 *                                  on click: getData() -> {header, rows}; triggers the download and
 *                                  fills outEl (a <textarea>, created after the button if omitted)
 *
 * Plotting (canvas, HiDPI, theme-aware, redraws on resize and theme change)
 *   const p = Sim.plot(canvas, {xLabel, yLabel, xMin, xMax, yMin, yMax, logY, logX, legend:true,
 *                                 pad:{l,r,t,b}, xReverse})   xReverse: x grows to the left (NMR ppm, IR cm-1)
 *   p.draw(series[], overrides?)   series: {data:[[x,y],...], type:'line'|'points'|'bars'|'step'|'area',
 *                                  color:'s1'..'s6' or CSS colour, width, dash:[..], size, label,
 *                                  err:[u,...] (y error bars), hidden}
 *                                  also {type:'hline', y}, {type:'vline', x}, {type:'text', x, y, text},
 *                                  {type:'band', data:[[x,ylo,yhi],...]}, {type:'hbar', y, x1, x2} (interval)
 *   p.toPx(x, y) / p.fromPx(px, py)  data <-> CSS pixel coordinates after a draw
 *   p.redraw()                     repeat the last draw
 *   Sim.color(name)                resolve a token ('s1', 'ink', 'muted', ...) or pass a CSS colour through
 *   Sim.onTheme(fn)                call fn when light/dark changes
 *   Sim.niceTicks(lo, hi, n)       "nice" tick values
 *
 * Animation
 *   Sim.loop(fn)                   requestAnimationFrame loop; fn(dtSeconds) returns false to stop;
 *                                  returns {stop()}; pauses itself while the page is hidden
 */
(function (global) {
  "use strict";

  var Sim = {};

  Sim.C = {
    R: 8.314462618,
    kB: 1.380649e-23,
    NA: 6.02214076e23,
    h: 6.62607015e-34,
    c: 299792458,
    e: 1.602176634e-19,
    F: 96485.33212,
    g: 9.80665,
    u: 1.66053906892e-27,
    atm: 101325,
    bar: 1e5
  };

  Sim.LABEL = "Educational model — not a real instrument";

  /* ---------- DOM helpers ---------- */

  Sim.$ = function (sel, root) { return (root || document).querySelector(sel); };
  Sim.$$ = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };

  Sim.el = function (tag, attrs) {
    var node = document.createElement(tag);
    var a = attrs || {};
    Object.keys(a).forEach(function (k) {
      var v = a[k];
      if (v === undefined || v === null || v === false) return;
      if (k === "class") node.className = v;
      else if (k === "text") node.textContent = v;
      else if (k === "html") node.innerHTML = v;
      else if (k === "on") Object.keys(v).forEach(function (ev) { node.addEventListener(ev, v[ev]); });
      else if (k === "style" && typeof v === "object") Object.keys(v).forEach(function (s) { node.style[s] = v[s]; });
      else if (v === true) node.setAttribute(k, "");
      else node.setAttribute(k, String(v));
    });
    for (var i = 2; i < arguments.length; i++) {
      var ch = arguments[i];
      if (ch === null || ch === undefined || ch === false) continue;
      if (Array.isArray(ch)) ch.forEach(function (c) { node.appendChild(typeof c === "string" ? document.createTextNode(c) : c); });
      else node.appendChild(typeof ch === "string" ? document.createTextNode(ch) : ch);
    }
    return node;
  };

  Sim.label = function (el) {
    var targets = el ? [el] : Sim.$$("[data-sim-label]");
    var last = null;
    targets.forEach(function (t) {
      t.textContent = "";
      last = Sim.el("span", { class: "sim-label", role: "note", text: Sim.LABEL });
      t.appendChild(last);
    });
    return last;
  };

  Sim.presetBox = function (el, info) {
    if (!el) return;
    el.textContent = "";
    el.classList.add("panel", "preset-box");
    el.appendChild(Sim.el("h2", { text: "Preset: " + (info.title || info.key || "") }));
    if (info.unknown) el.appendChild(Sim.el("p", { class: "warn small", text: "Unknown preset “" + info.unknown + "”; showing the default instead." }));
    if (info.what) el.appendChild(Sim.el("p", { html: info.what }));
    if (info.task) el.appendChild(Sim.el("p", {}, Sim.el("span", { class: "task", text: "Task: " }), Sim.el("span", { html: info.task })));
    if (info.target) el.appendChild(Sim.el("p", {}, Sim.el("span", { class: "target", text: "Target: " }), Sim.el("span", { html: info.target })));
  };

  Sim.tabs = function (container, onSelect) {
    var buttons = Sim.$$("[data-tab]", container);
    container.setAttribute("role", "tablist");
    function select(name) {
      // several tabs may share one panel: hide all first, then show the selected one's
      buttons.forEach(function (b) {
        var panel = document.getElementById(b.getAttribute("aria-controls"));
        if (panel) panel.hidden = true;
      });
      buttons.forEach(function (b) {
        var on = b.getAttribute("data-tab") === name;
        b.setAttribute("aria-selected", on ? "true" : "false");
        b.setAttribute("tabindex", on ? "0" : "-1");
        var panel = document.getElementById(b.getAttribute("aria-controls"));
        if (panel && on) panel.hidden = false;
      });
      if (onSelect) onSelect(name);
    }
    buttons.forEach(function (b, i) {
      b.setAttribute("role", "tab");
      b.addEventListener("click", function () { select(b.getAttribute("data-tab")); });
      b.addEventListener("keydown", function (e) {
        var j = null;
        if (e.key === "ArrowRight") j = (i + 1) % buttons.length;
        if (e.key === "ArrowLeft") j = (i - 1 + buttons.length) % buttons.length;
        if (j !== null) { e.preventDefault(); buttons[j].focus(); select(buttons[j].getAttribute("data-tab")); }
      });
      var panel = document.getElementById(b.getAttribute("aria-controls"));
      if (panel) panel.setAttribute("role", "tabpanel");
    });
    return { select: select };
  };

  Sim.log = function (el, text) {
    if (!el) return;
    el.appendChild(Sim.el("div", { text: text }));
    el.scrollTop = el.scrollHeight;
  };

  /* ---------- query and presets ---------- */

  Sim.query = function () {
    var out = {};
    var s = "";
    try { s = global.location.search || ""; } catch (e) { s = ""; }
    s.replace(/^\?/, "").split("&").forEach(function (pair) {
      if (!pair) return;
      var i = pair.indexOf("=");
      var k = i < 0 ? pair : pair.slice(0, i);
      var v = i < 0 ? "" : pair.slice(i + 1);
      try { k = decodeURIComponent(k.replace(/\+/g, " ")); v = decodeURIComponent(v.replace(/\+/g, " ")); } catch (e) { return; }
      out[k] = v;
    });
    return out;
  };

  Sim.param = function (name, fallback) {
    var q = Sim.query();
    return Object.prototype.hasOwnProperty.call(q, name) ? q[name] : fallback;
  };

  Sim.num = function (name, fallback) {
    var v = parseFloat(Sim.param(name, ""));
    return isFinite(v) ? v : fallback;
  };

  Sim.preset = function (presets, defKey) {
    var want = String(Sim.param("preset", defKey) || defKey).toLowerCase();
    var key = Object.prototype.hasOwnProperty.call(presets, want) ? want : defKey;
    var out = { key: key };
    var src = presets[key] || {};
    Object.keys(src).forEach(function (k) { out[k] = src[k]; });
    if (key !== want) out.unknown = want;
    return out;
  };

  /* ---------- seeded RNG ---------- */

  Sim.seedFromQuery = function (def) {
    var s = parseInt(Sim.param("seed", ""), 10);
    if (isFinite(s)) return s >>> 0;
    if (typeof def === "number") return def >>> 0;
    return (Date.now() ^ 0x5bd1e995) >>> 0;
  };

  Sim.newSeed = function (old) {
    var s = ((old >>> 0) * 1103515245 + 12345 + 7919) >>> 0;
    return s % 100000 || 1;
  };

  Sim.rng = function (seed) {
    var a = (seed >>> 0) || 1;
    var spare = null;
    function random() {
      a = (a + 0x6d2b79f5) >>> 0;
      var t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    }
    function normal(mu, sd) {
      var z;
      if (spare !== null) { z = spare; spare = null; }
      else {
        var u1 = 0, u2 = 0;
        while (u1 <= 1e-300) u1 = random();
        u2 = random();
        var r = Math.sqrt(-2 * Math.log(u1));
        z = r * Math.cos(2 * Math.PI * u2);
        spare = r * Math.sin(2 * Math.PI * u2);
      }
      return (mu || 0) + (sd === undefined ? 1 : sd) * z;
    }
    return {
      seed: seed >>> 0,
      random: random,
      uniform: function (lo, hi) { return lo + (hi - lo) * random(); },
      normal: normal,
      int: function (lo, hi) { return lo + Math.floor(random() * (hi - lo + 1)); },
      pick: function (arr) { return arr[Math.floor(random() * arr.length)]; },
      tri: function (lo, hi) { return lo + (hi - lo) * (random() + random()) / 2; }
    };
  };

  /* ---------- safe storage ---------- */

  Sim.store = {
    get: function (key, fallback) {
      try {
        var v = global.localStorage.getItem("sim:" + key);
        return v === null ? fallback : JSON.parse(v);
      } catch (e) { return fallback; }
    },
    set: function (key, value) {
      try { global.localStorage.setItem("sim:" + key, JSON.stringify(value)); return true; } catch (e) { return false; }
    }
  };

  /* ---------- number formatting ---------- */

  Sim.fmt = function (x, digits) {
    if (typeof x !== "number" || !isFinite(x)) return "—";
    var d = digits === undefined ? 3 : digits;
    var s = x.toFixed(d);
    if (/^-0\.?0*$/.test(s)) s = s.slice(1);
    return s;
  };

  Sim.sig = function (x, n) {
    if (typeof x !== "number" || !isFinite(x)) return "—";
    if (x === 0) return "0";
    var p = n || 3;
    var e = Math.floor(Math.log10(Math.abs(x)));
    if (e >= 6 || e <= -4) return x.toExponential(p - 1);
    return x.toFixed(Math.max(0, p - 1 - e));
  };

  Sim.fmtU = function (x, u, unit) {
    var tail = unit ? " " + unit : "";
    if (!isFinite(x)) return "—";
    if (!isFinite(u) || u <= 0) return Sim.sig(x, 5) + tail;
    var e = Math.floor(Math.log10(u));
    var dec = Math.max(0, 1 - e);
    if (dec > 12) dec = 12;
    if (Math.abs(x) >= 1e6 || (x !== 0 && Math.abs(x) < 1e-3) || e <= -9) {
      var p = Math.floor(Math.log10(Math.abs(x) || u));
      var scale = Math.pow(10, p);
      var dd = Math.max(0, p - e + 1);
      return "(" + (x / scale).toFixed(dd) + " ± " + (u / scale).toFixed(dd) + ")e" + p + tail;
    }
    return x.toFixed(dec) + " ± " + u.toFixed(dec) + tail;
  };

  /* ---------- statistics ---------- */

  function lnGamma(z) {
    // Lanczos approximation (g = 7, n = 9)
    var c = [0.99999999999980993, 676.5203681218851, -1259.1392167224028, 771.32342877765313,
      -176.61502916214059, 12.507343278686905, -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7];
    if (z < 0.5) return Math.log(Math.PI / Math.abs(Math.sin(Math.PI * z))) - lnGamma(1 - z);
    z -= 1;
    var x = c[0];
    for (var i = 1; i < 9; i++) x += c[i] / (z + i);
    var t = z + 7.5;
    return 0.5 * Math.log(2 * Math.PI) + (z + 0.5) * Math.log(t) - t + Math.log(x);
  }

  function betacf(a, b, x) {
    var MAXIT = 300, EPS = 3e-14, FPMIN = 1e-300;
    var qab = a + b, qap = a + 1, qam = a - 1, c = 1, d = 1 - qab * x / qap;
    if (Math.abs(d) < FPMIN) d = FPMIN;
    d = 1 / d;
    var h = d;
    for (var m = 1; m <= MAXIT; m++) {
      var m2 = 2 * m;
      var aa = m * (b - m) * x / ((qam + m2) * (a + m2));
      d = 1 + aa * d; if (Math.abs(d) < FPMIN) d = FPMIN;
      c = 1 + aa / c; if (Math.abs(c) < FPMIN) c = FPMIN;
      d = 1 / d; h *= d * c;
      aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2));
      d = 1 + aa * d; if (Math.abs(d) < FPMIN) d = FPMIN;
      c = 1 + aa / c; if (Math.abs(c) < FPMIN) c = FPMIN;
      d = 1 / d;
      var del = d * c;
      h *= del;
      if (Math.abs(del - 1) < EPS) break;
    }
    return h;
  }

  function betai(a, b, x) {
    if (x <= 0) return 0;
    if (x >= 1) return 1;
    var bt = Math.exp(lnGamma(a + b) - lnGamma(a) - lnGamma(b) + a * Math.log(x) + b * Math.log(1 - x));
    if (x < (a + 1) / (a + b + 2)) return bt * betacf(a, b, x) / a;
    return 1 - bt * betacf(b, a, 1 - x) / b;
  }

  var S = {};
  S.sum = function (a) { var s = 0; for (var i = 0; i < a.length; i++) s += a[i]; return s; };
  S.mean = function (a) { return a.length ? S.sum(a) / a.length : NaN; };
  S.sd = function (a) {
    if (a.length < 2) return NaN;
    var m = S.mean(a), s = 0;
    for (var i = 0; i < a.length; i++) s += (a[i] - m) * (a[i] - m);
    return Math.sqrt(s / (a.length - 1));
  };
  S.min = function (a) { var m = Infinity; for (var i = 0; i < a.length; i++) if (a[i] < m) m = a[i]; return m; };
  S.max = function (a) { var m = -Infinity; for (var i = 0; i < a.length; i++) if (a[i] > m) m = a[i]; return m; };
  S.tCdf = function (t, df) {
    var x = df / (df + t * t);
    var p = 0.5 * betai(df / 2, 0.5, x);
    return t >= 0 ? 1 - p : p;
  };
  S.tInv = function (p, df) {
    // two-sided: find t with P(|T| < t) = p
    if (!(df > 0)) return NaN;
    var target = 0.5 + p / 2, lo = 0, hi = 1000;
    for (var i = 0; i < 200; i++) {
      var mid = (lo + hi) / 2;
      if (S.tCdf(mid, df) < target) lo = mid; else hi = mid;
    }
    return (lo + hi) / 2;
  };
  S.linfit = function (x, y) {
    var n = x.length;
    if (n < 2) return null;
    var mx = S.mean(x), my = S.mean(y), sxx = 0, sxy = 0, syy = 0;
    for (var i = 0; i < n; i++) {
      sxx += (x[i] - mx) * (x[i] - mx);
      sxy += (x[i] - mx) * (y[i] - my);
      syy += (y[i] - my) * (y[i] - my);
    }
    var b = sxy / sxx, a = my - b * mx, ss = 0;
    for (var j = 0; j < n; j++) { var r = y[j] - a - b * x[j]; ss += r * r; }
    var s = n > 2 ? Math.sqrt(ss / (n - 2)) : NaN;
    var ub = s / Math.sqrt(sxx);
    var ua = s * Math.sqrt(1 / n + mx * mx / sxx);
    return { a: a, b: b, ua: ua, ub: ub, s: s, n: n, r2: syy > 0 ? 1 - ss / syy : 1, cov: -mx * ub * ub };
  };
  S.linfitThrough0 = function (x, y) {
    var n = x.length, sxx = 0, sxy = 0;
    for (var i = 0; i < n; i++) { sxx += x[i] * x[i]; sxy += x[i] * y[i]; }
    var b = sxy / sxx, ss = 0;
    for (var j = 0; j < n; j++) { var r = y[j] - b * x[j]; ss += r * r; }
    var s = n > 1 ? Math.sqrt(ss / (n - 1)) : NaN;
    return { b: b, ub: s / Math.sqrt(sxx), s: s, n: n };
  };
  S.percentile = function (sorted, p) {
    if (!sorted.length) return NaN;
    var i = p * (sorted.length - 1), lo = Math.floor(i), hi = Math.ceil(i);
    return sorted[lo] + (sorted[hi] - sorted[lo]) * (i - lo);
  };
  S.histogram = function (a, lo, hi, bins) {
    var counts = [], w = (hi - lo) / bins, edges = [];
    for (var c = 0; c < bins; c++) counts.push(0);
    for (var k = 0; k <= bins; k++) edges.push(lo + k * w);
    for (var i = 0; i < a.length; i++) {
      var j = Math.floor((a[i] - lo) / w);
      if (j >= 0 && j < bins) counts[j]++;
      else if (a[i] === hi) counts[bins - 1]++;
    }
    return { edges: edges, counts: counts, width: w };
  };
  Sim.stats = S;

  /* ---------- CSV export ---------- */

  function csvCell(v) {
    if (v === null || v === undefined) return "";
    var s = typeof v === "number" ? (isFinite(v) ? String(v) : "") : String(v);
    return /[",\n\r]/.test(s) ? "\"" + s.replace(/"/g, "\"\"") + "\"" : s;
  }

  Sim.csv = function (header, rows) {
    var lines = [header.map(csvCell).join(",")];
    rows.forEach(function (r) { lines.push(r.map(csvCell).join(",")); });
    return lines.join("\n") + "\n";
  };

  Sim.exportCSV = function (button, filename, getData, outEl) {
    var out = outEl || null;
    function ensureOut() {
      if (!out) {
        out = Sim.el("textarea", { class: "csv-out", rows: 6, readonly: true, "aria-label": "CSV data (copy it if the download is blocked)" });
        button.insertAdjacentElement("afterend", out);
      }
      out.hidden = false;
      return out;
    }
    button.addEventListener("click", function () {
      var d = getData();
      if (!d || !d.rows || !d.rows.length) { ensureOut().value = "No readings yet."; return; }
      var text = Sim.csv(d.header, d.rows);
      try {
        var a = document.createElement("a");
        a.href = "data:text/csv;charset=utf-8," + encodeURIComponent(text);
        a.download = d.filename || filename;
        a.style.display = "none";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
      } catch (e) { /* download blocked: the textarea still holds the data */ }
      ensureOut().value = text;
    });
  };

  /* ---------- theme ---------- */

  var themeFns = [];
  var mq = null;
  try { mq = global.matchMedia ? global.matchMedia("(prefers-color-scheme: dark)") : null; } catch (e) { mq = null; }
  if (mq) {
    var onChange = function () { themeFns.forEach(function (f) { try { f(); } catch (e) { /* ignore */ } }); };
    if (mq.addEventListener) mq.addEventListener("change", onChange);
    else if (mq.addListener) mq.addListener(onChange);
  }
  Sim.onTheme = function (fn) { themeFns.push(fn); };
  Sim.isDark = function () { return !!(mq && mq.matches); };

  var TOKENS = ["bg", "panel", "panel-2", "ink", "muted", "line", "accent", "good", "warn", "bad", "plot-bg", "plot-grid", "plot-axis", "s1", "s2", "s3", "s4", "s5", "s6"];
  Sim.color = function (name) {
    if (!name) name = "ink";
    if (TOKENS.indexOf(name) >= 0) {
      var v = getComputedStyle(document.documentElement).getPropertyValue("--" + name).trim();
      if (v) return v;
    }
    return name;
  };

  /* ---------- canvas plot helper ---------- */

  Sim.niceTicks = function (lo, hi, n) {
    if (!(hi > lo)) { hi = lo + 1; }
    var span = hi - lo, raw = span / Math.max(1, n || 5);
    var mag = Math.pow(10, Math.floor(Math.log10(raw)));
    var f = raw / mag, step = (f < 1.5 ? 1 : f < 3 ? 2 : f < 7 ? 5 : 10) * mag;
    var out = [], start = Math.ceil(lo / step - 1e-9) * step;
    for (var v = start; v <= hi + step * 1e-9; v += step) out.push(Math.abs(v) < step * 1e-9 ? 0 : v);
    return out;
  };

  function tickLabel(v, step) {
    if (v === 0) return "0";
    var a = Math.abs(v);
    if (a >= 1e5 || a < 1e-3) return v.toExponential(1).replace("e+", "e");
    var dec = Math.max(0, -Math.floor(Math.log10(step) + 1e-9));
    return v.toFixed(Math.min(dec, 6));
  }

  function logLabel(v) {
    var a = Math.abs(v);
    if (a >= 1e-3 && a < 1e5) return String(+v.toPrecision(3));
    return v.toExponential(0).replace("e+", "e");
  }

  Sim.plot = function (canvas, opts) {
    var o = opts || {};
    var ctx = canvas.getContext("2d");
    var last = null, map = null;

    function range(series, axis, log) {
      var lo = Infinity, hi = -Infinity;
      series.forEach(function (s) {
        if (s.hidden || s.noRange) return;
        if (s.type === "hline" && axis === 1) { lo = Math.min(lo, s.y); hi = Math.max(hi, s.y); return; }
        if (s.type === "vline" && axis === 0) { lo = Math.min(lo, s.x); hi = Math.max(hi, s.x); return; }
        if (s.type === "hbar") {
          if (axis === 0) { lo = Math.min(lo, s.x1, s.x2); hi = Math.max(hi, s.x1, s.x2); } else { lo = Math.min(lo, s.y); hi = Math.max(hi, s.y); }
          return;
        }
        if (!s.data) return;
        s.data.forEach(function (p, i) {
          var vals = s.type === "band" && axis === 1 ? [p[1], p[2]] : [p[axis]];
          if (axis === 1 && s.err && isFinite(s.err[i])) vals = [p[1] - s.err[i], p[1] + s.err[i]];
          if (s.type === "bars" && axis === 1) vals.push(0);
          vals.forEach(function (v) {
            if (!isFinite(v) || (log && v <= 0)) return;
            if (v < lo) lo = v;
            if (v > hi) hi = v;
          });
        });
      });
      if (!isFinite(lo)) { lo = log ? 1 : 0; hi = log ? 10 : 1; }
      if (hi === lo) { var d = Math.abs(lo) * 0.1 || 1; lo -= d; hi += d; }
      return [lo, hi];
    }

    function draw(series, over) {
      last = { series: series || [], over: over || {} };
      var cfg = {};
      Object.keys(o).forEach(function (k) { cfg[k] = o[k]; });
      Object.keys(last.over).forEach(function (k) { cfg[k] = last.over[k]; });
      var dpr = global.devicePixelRatio || 1;
      var W = canvas.clientWidth || 600, H = canvas.clientHeight || 300;
      if (canvas.width !== Math.round(W * dpr) || canvas.height !== Math.round(H * dpr)) {
        canvas.width = Math.round(W * dpr);
        canvas.height = Math.round(H * dpr);
      }
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var pad = cfg.pad || {};
      var L = pad.l !== undefined ? pad.l : 62, Rr = pad.r !== undefined ? pad.r : 14, T = pad.t !== undefined ? pad.t : 14, B = pad.b !== undefined ? pad.b : 44;
      var col = { bg: Sim.color("plot-bg"), grid: Sim.color("plot-grid"), axis: Sim.color("plot-axis"), ink: Sim.color("ink") };
      ctx.fillStyle = col.bg;
      ctx.fillRect(0, 0, W, H);

      var xr = range(last.series, 0, cfg.logX), yr = range(last.series, 1, cfg.logY);
      var x0 = cfg.xMin !== undefined ? cfg.xMin : xr[0], x1 = cfg.xMax !== undefined ? cfg.xMax : xr[1];
      var y0 = cfg.yMin !== undefined ? cfg.yMin : yr[0], y1 = cfg.yMax !== undefined ? cfg.yMax : yr[1];
      if (!cfg.logY && cfg.yMin === undefined && cfg.yMax === undefined) { var dy = (y1 - y0) * 0.06; y0 -= dy; y1 += dy; }
      if (!cfg.logX && cfg.xMin === undefined && cfg.xMax === undefined && cfg.xPad !== false) { var dx = (x1 - x0) * 0.03; x0 -= dx; x1 += dx; }
      var fx = cfg.logX ? function (v) { return Math.log10(v); } : function (v) { return v; };
      var fy = cfg.logY ? function (v) { return Math.log10(v); } : function (v) { return v; };
      var X0 = fx(x0), X1 = fx(x1), Y0 = fy(y0), Y1 = fy(y1);
      var pw = Math.max(10, W - L - Rr), ph = Math.max(10, H - T - B);
      var rev = !!cfg.xReverse;
      function px(x) { var f = (fx(x) - X0) / (X1 - X0); return L + (rev ? 1 - f : f) * pw; }
      function py(y) { return T + ph - (fy(y) - Y0) / (Y1 - Y0) * ph; }
      map = { px: px, py: py, L: L, T: T, pw: pw, ph: ph, X0: X0, X1: X1, Y0: Y0, Y1: Y1, logX: cfg.logX, logY: cfg.logY, rev: rev };

      // grid and ticks
      ctx.font = "11px " + (getComputedStyle(document.body).fontFamily || "sans-serif");
      ctx.lineWidth = 1;
      function ticks(lo, hi, log, n) {
        if (!log) return Sim.niceTicks(lo, hi, n);
        var out = [], e0 = Math.floor(Math.log10(lo)), e1 = Math.ceil(Math.log10(hi));
        var mult = e1 - e0 <= 3 ? [1, 2, 5] : [1];
        for (var e = e0; e <= e1; e++) {
          mult.forEach(function (mm) {
            var v = mm * Math.pow(10, e);
            if (v >= lo * 0.999 && v <= hi * 1.001) out.push(v);
          });
        }
        return out;
      }
      var xt = ticks(x0, x1, cfg.logX, Math.max(2, Math.floor(pw / 80)));
      var yt = ticks(y0, y1, cfg.logY, Math.max(2, Math.floor(ph / 45)));
      var xstep = xt.length > 1 ? xt[1] - xt[0] : 1, ystep = yt.length > 1 ? yt[1] - yt[0] : 1;
      ctx.strokeStyle = col.grid;
      ctx.fillStyle = col.axis;
      ctx.textAlign = "center";
      ctx.textBaseline = "top";
      xt.forEach(function (v) {
        var X = px(v);
        ctx.beginPath(); ctx.moveTo(X, T); ctx.lineTo(X, T + ph); ctx.stroke();
        ctx.fillText(cfg.logX ? logLabel(v) : tickLabel(v, xstep), X, T + ph + 4);
      });
      ctx.textAlign = "right";
      ctx.textBaseline = "middle";
      yt.forEach(function (v) {
        var Y = py(v);
        ctx.beginPath(); ctx.moveTo(L, Y); ctx.lineTo(L + pw, Y); ctx.stroke();
        ctx.fillText(cfg.logY ? logLabel(v) : tickLabel(v, ystep), L - 5, Y);
      });
      ctx.strokeStyle = col.axis;
      ctx.strokeRect(L + 0.5, T + 0.5, pw, ph);
      ctx.fillStyle = col.ink;
      ctx.textAlign = "center";
      ctx.textBaseline = "bottom";
      if (cfg.xLabel) ctx.fillText(cfg.xLabel, L + pw / 2, H - 4);
      if (cfg.yLabel) {
        ctx.save();
        ctx.translate(12, T + ph / 2);
        ctx.rotate(-Math.PI / 2);
        ctx.textBaseline = "top";
        ctx.fillText(cfg.yLabel, 0, -8);
        ctx.restore();
      }

      // series
      ctx.save();
      ctx.beginPath();
      ctx.rect(L, T, pw, ph);
      ctx.clip();
      var legend = [];
      last.series.forEach(function (s, idx) {
        if (s.hidden) return;
        var c = Sim.color(s.color || ("s" + ((idx % 6) + 1)));
        ctx.strokeStyle = c;
        ctx.fillStyle = c;
        ctx.lineWidth = s.width || 2;
        ctx.setLineDash(s.dash || []);
        var type = s.type || "line";
        if (s.label) legend.push({ label: s.label, color: c, type: type, dash: s.dash });
        if (type === "hline") { ctx.beginPath(); ctx.moveTo(L, py(s.y)); ctx.lineTo(L + pw, py(s.y)); ctx.stroke(); }
        else if (type === "vline") { ctx.beginPath(); ctx.moveTo(px(s.x), T); ctx.lineTo(px(s.x), T + ph); ctx.stroke(); }
        else if (type === "hbar") {
          var Yb = py(s.y);
          ctx.beginPath(); ctx.moveTo(px(s.x1), Yb); ctx.lineTo(px(s.x2), Yb);
          ctx.moveTo(px(s.x1), Yb - 3); ctx.lineTo(px(s.x1), Yb + 3);
          ctx.moveTo(px(s.x2), Yb - 3); ctx.lineTo(px(s.x2), Yb + 3); ctx.stroke();
          if (isFinite(s.mid)) { ctx.beginPath(); ctx.arc(px(s.mid), Yb, 2.5, 0, 2 * Math.PI); ctx.fill(); }
        }
        else if (type === "text") {
          ctx.setLineDash([]);
          ctx.textAlign = s.align || "left"; ctx.textBaseline = "bottom";
          ctx.font = (s.font || "12px") + " " + (getComputedStyle(document.body).fontFamily || "sans-serif");
          ctx.fillText(s.text, px(s.x), py(s.y));
        }
        else if (type === "band") {
          if (!s.data.length) return;
          ctx.globalAlpha = s.alpha || 0.18;
          ctx.beginPath();
          s.data.forEach(function (p, i) { if (i) ctx.lineTo(px(p[0]), py(p[2])); else ctx.moveTo(px(p[0]), py(p[2])); });
          for (var k = s.data.length - 1; k >= 0; k--) ctx.lineTo(px(s.data[k][0]), py(s.data[k][1]));
          ctx.closePath(); ctx.fill();
          ctx.globalAlpha = 1;
        }
        else if (type === "bars") {
          var bw = s.barWidth;
          if (!bw && s.data.length > 1) bw = Math.abs(s.data[1][0] - s.data[0][0]);
          if (!bw) bw = (x1 - x0) / 20;
          ctx.globalAlpha = s.alpha || 0.55;
          s.data.forEach(function (p) {
            var xa = px(p[0] - bw / 2), xb = px(p[0] + bw / 2), ya = py(p[1]), yb = py(cfg.logY ? y0 : 0);
            ctx.fillRect(Math.min(xa, xb), Math.min(ya, yb), Math.max(1, Math.abs(xb - xa) - 1), Math.abs(yb - ya));
          });
          ctx.globalAlpha = 1;
        }
        else if (type === "points") {
          var r = s.size || 3.2;
          s.data.forEach(function (p, i) {
            if (!isFinite(p[0]) || !isFinite(p[1])) return;
            var X = px(p[0]), Y = py(p[1]);
            if (s.err && isFinite(s.err[i])) {
              ctx.setLineDash([]); ctx.lineWidth = 1;
              ctx.beginPath(); ctx.moveTo(X, py(p[1] - s.err[i])); ctx.lineTo(X, py(p[1] + s.err[i])); ctx.stroke();
            }
            ctx.beginPath(); ctx.arc(X, Y, r, 0, 2 * Math.PI);
            if (s.hollow) { ctx.lineWidth = 1.5; ctx.stroke(); } else ctx.fill();
          });
        }
        else {
          ctx.beginPath();
          var started = false, prevY = null;
          s.data.forEach(function (p) {
            if (!isFinite(p[0]) || !isFinite(p[1]) || (cfg.logY && p[1] <= 0)) { started = false; return; }
            var X = px(p[0]), Y = py(p[1]);
            if (!started) { ctx.moveTo(X, Y); started = true; }
            else if (type === "step") { ctx.lineTo(X, prevY); ctx.lineTo(X, Y); }
            else ctx.lineTo(X, Y);
            prevY = Y;
          });
          ctx.stroke();
          if (type === "area") {
            ctx.globalAlpha = s.alpha || 0.15;
            ctx.lineTo(px(s.data[s.data.length - 1][0]), py(cfg.logY ? y0 : 0));
            ctx.lineTo(px(s.data[0][0]), py(cfg.logY ? y0 : 0));
            ctx.closePath(); ctx.fill(); ctx.globalAlpha = 1;
          }
        }
      });
      ctx.restore();
      ctx.setLineDash([]);

      // legend
      if (cfg.legend !== false && legend.length) {
        ctx.font = "11px " + (getComputedStyle(document.body).fontFamily || "sans-serif");
        var lw = 0;
        legend.forEach(function (g) { lw = Math.max(lw, ctx.measureText(g.label).width); });
        var bx = cfg.legendLeft ? L + 8 : L + pw - lw - 34, by = T + 6;
        ctx.globalAlpha = 0.85; ctx.fillStyle = col.bg;
        ctx.fillRect(bx - 4, by - 2, lw + 32, legend.length * 15 + 4);
        ctx.globalAlpha = 1;
        legend.forEach(function (g, i) {
          var yy = by + i * 15 + 7;
          ctx.strokeStyle = g.color; ctx.fillStyle = g.color; ctx.lineWidth = 2;
          if (g.type === "points") { ctx.beginPath(); ctx.arc(bx + 9, yy, 3, 0, 2 * Math.PI); ctx.fill(); }
          else if (g.type === "bars" || g.type === "band") { ctx.globalAlpha = 0.5; ctx.fillRect(bx + 2, yy - 4, 14, 8); ctx.globalAlpha = 1; }
          else { ctx.setLineDash(g.dash || []); ctx.beginPath(); ctx.moveTo(bx, yy); ctx.lineTo(bx + 18, yy); ctx.stroke(); ctx.setLineDash([]); }
          ctx.fillStyle = col.ink; ctx.textAlign = "left"; ctx.textBaseline = "middle";
          ctx.fillText(g.label, bx + 24, yy);
        });
      }
    }

    function redraw() { if (last) draw(last.series, last.over); }
    if (typeof global.ResizeObserver === "function") {
      try { new global.ResizeObserver(function () { redraw(); }).observe(canvas); } catch (e) { /* ignore */ }
    } else {
      global.addEventListener("resize", redraw);
    }
    Sim.onTheme(redraw);
    if (!canvas.hasAttribute("role")) canvas.setAttribute("role", "img");

    return {
      draw: draw,
      redraw: redraw,
      canvas: canvas,
      toPx: function (x, y) { return map ? [map.px(x), map.py(y)] : [0, 0]; },
      fromPx: function (X, Y) {
        if (!map) return [0, 0];
        var fxp = (X - map.L) / map.pw;
        if (map.rev) fxp = 1 - fxp;
        var xv = map.X0 + fxp * (map.X1 - map.X0);
        var yv = map.Y0 + (map.T + map.ph - Y) / map.ph * (map.Y1 - map.Y0);
        return [map.logX ? Math.pow(10, xv) : xv, map.logY ? Math.pow(10, yv) : yv];
      }
    };
  };

  /* ---------- animation loop ---------- */

  Sim.loop = function (fn) {
    var running = true, prev = null, id = null;
    function frame(t) {
      if (!running) return;
      var dt = prev === null ? 0 : Math.min(0.1, (t - prev) / 1000);
      prev = t;
      var keep = fn(dt);
      if (keep === false) { running = false; return; }
      id = global.requestAnimationFrame(frame);
    }
    id = global.requestAnimationFrame(frame);
    document.addEventListener("visibilitychange", function () { prev = null; });
    return { stop: function () { running = false; if (id !== null) global.cancelAnimationFrame(id); } };
  };

  global.Sim = Sim;
})(typeof window !== "undefined" ? window : this);
