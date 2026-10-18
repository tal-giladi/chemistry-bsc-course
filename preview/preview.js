/* Preview shell for GitHub Pages only (docsify). The course itself is plain markdown; nothing here is needed to learn. */
(function () {
  var REPO = 'https://github.com/tal-giladi/chemistry-bsc-course/blob/main/';
  var TREE = 'https://github.com/tal-giladi/chemistry-bsc-course/tree/main/';

  function resolve(base, rel) {
    var parts = base.split('/'); parts.pop();
    rel.split('/').forEach(function (p) {
      if (p === '..') parts.pop(); else if (p !== '.' && p !== '') parts.push(p);
    });
    return parts.join('/');
  }

  window.CoursePreviewPlugin = function (hook, vm) {
    var maths = [];
    hook.beforeEach(function (md) {
      var file = (vm.route.file || 'README.md').replace(/^\//, '');
      md = md.replace(/^---\n[\s\S]*?\n---\n/, '');                         // front-matter
      md = md.replace(/^> \[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*$/gm, function (_, k) {
        return '> **' + k.charAt(0) + k.slice(1).toLowerCase() + '**';
      });
      var fences = [];
      md = md.replace(/```[\s\S]*?```|`[^`\n]*`/g, function (m) { fences.push(m); return 'KTXF' + (fences.length - 1) + 'FXTK'; });
      maths = [];
      md = md.replace(/\$\$[\s\S]+?\$\$|\$[^$\n]+?\$/g, function (m) { maths.push(m); return 'KTXM' + (maths.length - 1) + 'MXTK'; });
      md = md.replace(/(!?)\[([^\]]*)\]\(([^)\s]+)\)/g, function (all, bang, text, url) {
        if (/^(https?:|mailto:|#|\/$)/.test(url)) return all;
        var path = url.split('#')[0].split('?')[0];
        var abs = resolve(file, path), q = url.slice(path.length);
        if (bang) return '![' + text + '](' + location.origin + location.pathname.replace(/[^/]*$/, '') + abs + q + ')';
        if (/\.md$/.test(path)) return '[' + text + '](/' + abs + q + ')';
        if (/\.html$/.test(path)) return '[' + text + '](' + abs + q + ' \':ignore\')';
        var isDir = /\/$/.test(url) || !/\.[a-z0-9]+$/i.test(path);
        // Offline (local server): open the file from the folder. Online (GitHub Pages): show it on GitHub.
        if (!/github\.io$/.test(location.hostname)) return '[' + text + '](' + abs + (isDir && !/\/$/.test(abs) ? '/' : '') + q + ' \':ignore\')';
        return '[' + text + '](' + (isDir ? TREE : REPO) + abs + ' \':ignore\')';
      });
      md = md.replace(/KTXF(\d+)FXTK/g, function (_, i) { return fences[+i]; });
      return md.replace(/^```mermaid\n([\s\S]*?)```/gm, function (_, code) {
        return '<div class="mermaid">' + code.replace(/</g, '&lt;') + '</div>';
      });
    });
    hook.afterEach(function (html) {
      return html.replace(/KTXM(\d+)MXTK/g, function (_, i) {
        return maths[+i].replace(/&/g, '&amp;').replace(/</g, '&lt;');
      });
    });
    hook.doneEach(function () {
      var el = document.querySelector('.markdown-section');
      if (window.renderMathInElement && el) {
        window.renderMathInElement(el, { delimiters: [{ left: '$$', right: '$$', display: true }, { left: '$', right: '$', display: false }], throwOnError: false });
      }
      if (window.mermaid) {
        var dark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
        window.mermaid.initialize({ startOnLoad: false, theme: dark ? 'dark' : 'neutral', securityLevel: 'strict' });
        window.mermaid.run({ querySelector: '.markdown-section .mermaid' });
      }
    });
  };
})();
