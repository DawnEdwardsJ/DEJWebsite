/* dawnedwards-jones.com: navigation, motion and the enquiry form. No libraries. */
(function () {
  var d = document;
  window.ndReady = true; // tells the head failsafe that this script loaded
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---- mobile menu ---- */
  var toggle = d.querySelector(".nav-toggle");
  var nav = d.getElementById("main-nav");
  function setMenu(open) {
    nav.classList.toggle("open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
  }
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      setMenu(!nav.classList.contains("open"));
    });
  }

  /* ---- dropdowns: click/tap or keyboard, Escape closes ---- */
  function closeDrops(except) {
    d.querySelectorAll(".has-drop.open").forEach(function (li) {
      if (li === except) return;
      li.classList.remove("open");
      li.querySelector(".drop-toggle").setAttribute("aria-expanded", "false");
    });
  }
  d.querySelectorAll(".drop-toggle").forEach(function (btn) {
    var li = btn.parentElement;
    btn.addEventListener("click", function () {
      var open = !li.classList.contains("open");
      closeDrops(li);
      li.classList.toggle("open", open);
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
    // close when keyboard focus moves on past the dropdown
    li.addEventListener("focusout", function (e) {
      if (e.relatedTarget && !li.contains(e.relatedTarget)) closeDrops();
    });
  });
  d.addEventListener("click", function (e) {
    if (!e.target.closest(".has-drop")) closeDrops();
  });
  d.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    var openDrop = d.querySelector(".has-drop.open");
    if (openDrop) {
      closeDrops();
      openDrop.querySelector(".drop-toggle").focus();
    } else if (nav && nav.classList.contains("open")) {
      setMenu(false);
      toggle.focus();
    }
  });

  /* ---- photos fade in over their blurred preview once loaded ---- */
  d.querySelectorAll('.fig .ph[loading="lazy"]').forEach(function (img) {
    function done() { img.classList.add("is-loaded"); }
    if (img.complete && img.naturalWidth) done();
    else { img.addEventListener("load", done, { once: true }); img.addEventListener("error", done, { once: true }); }
  });

  function esc(t) { return t.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }

  /* ---- headlines rise line by line: split the h1 into the lines the browser drew ---- */
  var masks = d.querySelectorAll(".line-mask");
  function splitLines(h, animate) {
    var inner = h.firstElementChild;
    if (!inner) return;
    if (!h.dataset.src) h.dataset.src = inner.innerHTML;
    var holder = d.createElement("span");
    holder.innerHTML = h.dataset.src;
    var tokens = [];
    var ok = true;
    (function walk(node, wrap) {
      node.childNodes.forEach(function (n) {
        if (n.nodeType === 3) {
          n.textContent.split(/(\s+)/).forEach(function (part) {
            if (!part) return;
            tokens.push(/^\s+$/.test(part) ? null : wrap(esc(part)));
          });
        } else if (n.nodeType === 1 && /^(EM|STRONG|I|B)$/.test(n.tagName)) {
          var tag = n.tagName.toLowerCase();
          walk(n, function (t) { return wrap("<" + tag + ">" + t + "</" + tag + ">"); });
        } else if (n.nodeType === 1) {
          ok = false;
        }
      });
    })(holder, function (t) { return t; });
    if (!ok || !tokens.length) { h.classList.add("is-split"); return; }
    inner.innerHTML = tokens.map(function (t) { return t === null ? " " : '<span class="w">' + t + "</span>"; }).join("");
    var lines = [], top = null;
    inner.querySelectorAll(".w").forEach(function (w) {
      if (top === null || Math.abs(w.offsetTop - top) > 4) { lines.push([]); top = w.offsetTop; }
      lines[lines.length - 1].push(w.innerHTML);
    });
    inner.innerHTML = lines.map(function (l, i) {
      return '<span class="ln" style="--i:' + i + '"><span>' + l.join(" ") + "</span></span>";
    }).join("");
    h.classList.toggle("no-anim", !animate);
    h.classList.add("is-split");
    h.dataset.width = h.offsetWidth;
  }
  function splitAll(animate) {
    masks.forEach(function (h) {
      try { splitLines(h, animate); } catch (err) { h.classList.add("is-split"); }
    });
  }
  if (masks.length) {
    var fontsReady = d.fonts && d.fonts.ready
      ? Promise.race([d.fonts.ready, new Promise(function (r) { setTimeout(r, 500); })])
      : Promise.resolve();
    var go = function () { fontsReady.then(function () { splitAll(true); }); };
    if (d.prerendering) d.addEventListener("prerenderingchange", go, { once: true }); else go();
    var lastW = window.innerWidth;
    window.addEventListener("resize", function () {
      if (Math.abs(window.innerWidth - lastW) < 40) return;
      lastW = window.innerWidth;
      splitAll(false);
    });
  }
  /* a page loaded ahead of the click replays its opening animations when it is shown */
  if (d.prerendering) {
    d.addEventListener("prerenderingchange", function () {
      if (d.getAnimations) d.getAnimations().forEach(function (a) { a.cancel(); a.play(); });
    }, { once: true });
  }

  /* ---- pull quotes light up word by word with the scroll ---- */
  var quotes = [];
  if (!reduceMotion) {
    d.querySelectorAll(".pullquote blockquote").forEach(function (q) {
      var walker = d.createTreeWalker(q, NodeFilter.SHOW_TEXT);
      var texts = [];
      while (walker.nextNode()) texts.push(walker.currentNode);
      texts.forEach(function (node) {
        var frag = d.createDocumentFragment();
        node.textContent.split(/(\s+)/).forEach(function (part) {
          if (!part) return;
          if (/^\s+$/.test(part)) { frag.appendChild(d.createTextNode(part)); return; }
          var s = d.createElement("span");
          s.className = "w";
          s.textContent = part;
          frag.appendChild(s);
        });
        node.parentNode.replaceChild(frag, node);
      });
      quotes.push({ el: q, words: q.querySelectorAll(".w") });
    });
  }
  function lightQuotes() {
    var vh = window.innerHeight;
    quotes.forEach(function (q) {
      var r = q.el.getBoundingClientRect();
      var p = Math.max(0, Math.min(1, (vh * 0.92 - r.top) / (vh * 0.5)));
      var n = q.words.length;
      q.words.forEach(function (w, i) {
        var v = Math.max(0, Math.min(1, p * (n + 2) - i));
        w.style.setProperty("--lit", (0.18 + 0.82 * v).toFixed(3));
      });
    });
  }

  /* ---- reading line on long pages ---- */
  var readLine = d.querySelector(".read-line");
  function updateReadLine() {
    var max = d.documentElement.scrollHeight - window.innerHeight;
    readLine.style.transform = "scaleX(" + (max > 0 ? Math.min(1, window.scrollY / max) : 0).toFixed(4) + ")";
  }

  /* ---- sticky nav condenses after 80px; scroll-linked details update together ---- */
  var header = d.querySelector(".site-header");
  var ticking = false;
  function onScroll() {
    header.classList.toggle("condensed", window.scrollY > 80);
    if (quotes.length) lightQuotes();
    if (readLine) updateReadLine();
    ticking = false;
  }
  if (header) {
    window.addEventListener("scroll", function () {
      if (!ticking) {
        window.requestAnimationFrame(onScroll);
        ticking = true;
      }
    }, { passive: true });
    window.addEventListener("resize", onScroll);
    onScroll();
  }

  /* ---- one-time count-up on credential numbers (>=1.5s, never repeats) ---- */
  function countUp(el) {
    var m = (el.dataset.count || "").match(/^([\d,]+)(.*)$/);
    if (!m) return;
    var target = parseInt(m[1].replace(/,/g, ""), 10);
    var suffix = m[2];
    var useCommas = m[1].indexOf(",") > -1;
    var start = null;
    var duration = 1600;
    function fmt(n) {
      return (useCommas ? n.toLocaleString("en-AU") : String(n)) + suffix;
    }
    function step(ts) {
      if (start === null) start = ts;
      var t = Math.min((ts - start) / duration, 1);
      var eased = t === 1 ? 1 : 1 - Math.pow(2, -10 * t);
      el.textContent = fmt(Math.round(target * eased));
      if (t < 1) window.requestAnimationFrame(step);
    }
    el.textContent = fmt(0);
    window.requestAnimationFrame(step);
  }

  /* ---- scroll reveal ---- */
  var reveals = d.querySelectorAll(".reveal");
  var counters = d.querySelectorAll(".count[data-count]");
  if (reduceMotion || !("IntersectionObserver" in window)) {
    reveals.forEach(function (el) { el.classList.add("in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        var el = e.target;
        var delay = parseInt(el.dataset.delay || 0, 10);
        el.style.transitionDelay = delay + "ms";
        el.classList.add("in");
        // clear the stagger afterwards so hover effects respond instantly
        window.setTimeout(function () { el.style.transitionDelay = ""; }, delay + 700);
        e.target.querySelectorAll(".count[data-count]").forEach(countUp);
        io.unobserve(e.target);
      });
    }, { rootMargin: "0px 0px -12% 0px", threshold: 0.15 });
    reveals.forEach(function (el) { io.observe(el); });
    counters.forEach(function (el) {
      if (!el.closest(".reveal")) countUp(el);
    });
  }

  /* ---- enquiry form ---- */
  var form = d.getElementById("enquiry");
  if (form) {
    var params = new URLSearchParams(window.location.search);
    var select = form.querySelector("#f-about");
    var wanted = params.get("type");
    if (wanted && select && Array.prototype.some.call(select.options, function (o) { return o.value === wanted; })) {
      select.value = wanted;
    }
    var status = form.querySelector("#f-status");
    function show(kind) {
      status.textContent = kind === "ok" ? form.dataset.success : form.dataset.error;
      status.className = "fine form-status " + kind;
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var button = form.querySelector('button[type="submit"]');
      button.disabled = true;
      status.textContent = "";
      fetch(form.action, {
        method: "POST",
        headers: { Accept: "application/json" },
        body: new FormData(form),
      })
        .then(function (res) {
          return res.json().catch(function () { return {}; }).then(function (data) {
            if (!res.ok || !data.ok) throw new Error("send failed");
          });
        })
        .then(function () {
          var type = select ? select.value : "";
          show("ok");
          form.reset();
          if (window.gtag) window.gtag("event", "generate_lead", { enquiry_type: type });
          if (window.fbq) window.fbq("track", "Lead", { content_category: type });
        })
        .catch(function () { show("err"); })
        .then(function () { button.disabled = false; });
    });
  }
})();
