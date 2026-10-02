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

  /* ---- sticky nav condenses after 80px ---- */
  var header = d.querySelector(".site-header");
  var ticking = false;
  function onScroll() {
    header.classList.toggle("condensed", window.scrollY > 80);
    ticking = false;
  }
  if (header) {
    window.addEventListener("scroll", function () {
      if (!ticking) {
        window.requestAnimationFrame(onScroll);
        ticking = true;
      }
    }, { passive: true });
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
