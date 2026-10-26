// gladi.de - Theme-Schalter: System -> Hell -> Dunkel -> System. Die Wahl liegt nur im Browser (localStorage).
(function () {
  var KEY = "theme", root = document.documentElement;
  var LABELS = JSON.parse(root.getAttribute("data-theme-labels") || "{}");
  var ICONS = {
    system: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/></svg>',
    light: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
    dark: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>'
  };
  function read() { try { return localStorage.getItem(KEY) || "system"; } catch (e) { return "system"; } }
  function write(v) { try { v === "system" ? localStorage.removeItem(KEY) : localStorage.setItem(KEY, v); } catch (e) {} }
  function apply(v) {
    if (v === "system") root.removeAttribute("data-theme"); else root.setAttribute("data-theme", v);
    var b = document.querySelector(".theme-toggle");
    if (b) {
      b.innerHTML = ICONS[v] + '<span class="label">' + (LABELS[v] || v) + "</span>";
      b.setAttribute("aria-label", (LABELS.title || "Theme") + ": " + (LABELS[v] || v));
    }
  }
  apply(read());
  document.addEventListener("DOMContentLoaded", function () {
    var b = document.querySelector(".theme-toggle");
    if (!b) return;
    b.hidden = false;
    apply(read());
    b.addEventListener("click", function () {
      var next = { system: "light", light: "dark", dark: "system" }[read()];
      write(next);
      apply(next);
    });
  });
})();
