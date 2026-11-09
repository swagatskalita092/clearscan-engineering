(function () {
  "use strict";
  var root = document.body.getAttribute("data-root") || "./";
  var input = document.getElementById("q");
  var list = document.getElementById("results");
  var menu = document.querySelector(".menu-btn");
  var rows = null;
  var loading = null;
  var shown = [];
  var active = -1;

  if (menu) {
    menu.addEventListener("click", function () {
      var open = document.body.classList.toggle("nav-open");
      menu.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }
  if (!input || !list) { return; }

  function load() {
    if (rows) { return Promise.resolve(rows); }
    if (!loading) {
      loading = fetch(root + "search-index.json")
        .then(function (r) {
          if (!r.ok) { throw new Error("HTTP " + r.status); }
          return r.json();
        })
        .then(function (data) {
          rows = data.map(function (d) {
            return { t: d.t, h: d.h, u: d.u, x: d.x,
                     lt: d.t.toLowerCase(), lh: d.h.toLowerCase(), lx: d.x.toLowerCase() };
          });
          return rows;
        });
    }
    return loading;
  }

  function tokens(q) {
    return q.toLowerCase().match(/[\p{L}\p{N}]+/gu) || [];
  }

  function count(hay, needle) {
    var n = 0, i = hay.indexOf(needle);
    while (i >= 0 && n < 5) { n += 1; i = hay.indexOf(needle, i + needle.length); }
    return n;
  }

  function search(q) {
    var toks = tokens(q);
    if (!toks.length) { return []; }
    var phrase = toks.join(" ");
    var scored = [];
    rows.forEach(function (c) {
      var score = 0, ok = true;
      for (var i = 0; i < toks.length; i++) {
        var t = toks[i];
        var inH = c.lh.indexOf(t) >= 0, inT = c.lt.indexOf(t) >= 0, n = count(c.lx, t);
        if (!inH && !inT && n === 0) { ok = false; break; }
        score += (inH ? 8 : 0) + (inT ? 4 : 0) + (n ? 2 + n : 0);
      }
      if (!ok) { return; }
      if (toks.length > 1 && (c.lx.indexOf(phrase) >= 0 || c.lh.indexOf(phrase) >= 0)) { score += 10; }
      if (c.h && c.lh === phrase) { score += 6; }
      scored.push({ c: c, s: score });
    });
    scored.sort(function (a, b) { return b.s - a.s; });
    var perPage = {}, out = [];
    for (var k = 0; k < scored.length && out.length < 8; k++) {
      var page = scored[k].c.u.split("#")[0];
      perPage[page] = (perPage[page] || 0) + 1;
      if (perPage[page] <= 2) { out.push(scored[k].c); }
    }
    return out;
  }

  function highlight(parent, text, toks) {
    var esc = toks.map(function (t) { return t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); });
    if (!esc.length) { parent.appendChild(document.createTextNode(text)); return; }
    var re = new RegExp("(" + esc.join("|") + ")", "giu");
    text.split(re).forEach(function (part, i) {
      if (i % 2 === 1) {
        var m = document.createElement("mark");
        m.textContent = part;
        parent.appendChild(m);
      } else if (part) {
        parent.appendChild(document.createTextNode(part));
      }
    });
  }

  function snippet(c, toks) {
    var text = c.x, low = c.lx, pos = -1;
    for (var i = 0; i < toks.length && pos < 0; i++) { pos = low.indexOf(toks[i]); }
    if (pos < 0) { return text.slice(0, 150) + (text.length > 150 ? "..." : ""); }
    var start = Math.max(0, pos - 60), end = Math.min(text.length, pos + 110);
    return (start > 0 ? "..." : "") + text.slice(start, end) + (end < text.length ? "..." : "");
  }

  function setActive(i) {
    var items = list.querySelectorAll("li[role=option]");
    if (!items.length) { active = -1; return; }
    active = (i + items.length) % items.length;
    items.forEach(function (li, n) {
      li.setAttribute("aria-selected", n === active ? "true" : "false");
    });
    items[active].scrollIntoView({ block: "nearest" });
    input.setAttribute("aria-activedescendant", items[active].id);
  }

  function note(text) {
    list.textContent = "";
    var li = document.createElement("li");
    li.className = "r-note";
    li.textContent = text;
    list.appendChild(li);
    list.hidden = false;
    input.setAttribute("aria-expanded", "true");
  }

  function close() {
    list.hidden = true;
    input.setAttribute("aria-expanded", "false");
    input.removeAttribute("aria-activedescendant");
    active = -1;
  }

  function run() {
    var q = input.value.trim();
    if (!q) { close(); return; }
    load().then(function () {
      var toks = tokens(input.value);
      shown = search(input.value);
      if (!shown.length) { note("Nothing found for \"" + q + "\"."); return; }
      list.textContent = "";
      shown.forEach(function (c, n) {
        var li = document.createElement("li");
        li.setAttribute("role", "option");
        li.id = "r" + n;
        li.setAttribute("aria-selected", "false");
        var a = document.createElement("a");
        a.href = root + c.u;
        var t = document.createElement("span");
        t.className = "r-title";
        t.textContent = c.h && c.h !== c.t ? c.t + " > " + c.h : c.t;
        var s = document.createElement("span");
        s.className = "r-snip";
        highlight(s, snippet(c, toks), toks);
        a.appendChild(t);
        a.appendChild(s);
        li.appendChild(a);
        list.appendChild(li);
      });
      list.hidden = false;
      input.setAttribute("aria-expanded", "true");
      active = -1;
    }).catch(function () {
      note("Search needs the published site. It cannot load when the page is opened from a file.");
    });
  }

  input.addEventListener("focus", function () { load().catch(function () {}); });
  input.addEventListener("input", run);
  input.addEventListener("keydown", function (e) {
    if (e.key === "ArrowDown") { e.preventDefault(); setActive(active + 1); }
    else if (e.key === "ArrowUp") { e.preventDefault(); setActive(active - 1); }
    else if (e.key === "Enter") {
      var items = list.querySelectorAll("li[role=option] a");
      var go = items[active >= 0 ? active : 0];
      if (go && !list.hidden) { e.preventDefault(); window.location.href = go.href; }
    } else if (e.key === "Escape") { close(); input.blur(); }
  });
  document.addEventListener("keydown", function (e) {
    var tag = (e.target && e.target.tagName) || "";
    if (e.key === "/" && tag !== "INPUT" && tag !== "TEXTAREA" && !e.metaKey && !e.ctrlKey) {
      e.preventDefault();
      input.focus();
    }
  });
  document.addEventListener("click", function (e) {
    if (!e.target.closest(".search")) { close(); }
  });
})();
