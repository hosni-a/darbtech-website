/* DarbTech — site interactions. No dependencies. */
(function () {
  "use strict";

  var doc = document.documentElement;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var finePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* ---------- Sticky header: shrink on scroll, hide on fast scroll down ---------- */
  var header = $(".site-header");
  var lastY = window.scrollY;
  var ticking = false;
  function onScroll() {
    var y = window.scrollY;
    if (header) {
      header.classList.toggle("is-scrolled", y > 24);
      var navOpen = document.body.classList.contains("nav-open");
      var menuOpen = !!$(".nav__item.is-open");
      if (!navOpen && !menuOpen && y > 480 && y - lastY > 6) header.classList.add("is-hidden");
      else if (lastY - y > 4 || y < 480) header.classList.remove("is-hidden");
    }
    lastY = y;
    ticking = false;
  }
  window.addEventListener("scroll", function () {
    if (!ticking) { window.requestAnimationFrame(onScroll); ticking = true; }
  }, { passive: true });
  onScroll();

  /* ---------- Desktop dropdowns ---------- */
  $$(".nav__item[data-dropdown]").forEach(function (item) {
    var trigger = $(".nav__trigger", item);
    var closeTimer;
    function open() {
      clearTimeout(closeTimer);
      $$(".nav__item.is-open").forEach(function (o) { if (o !== item) close(o); });
      item.classList.add("is-open");
      trigger.setAttribute("aria-expanded", "true");
    }
    function close(el) {
      el = el || item;
      el.classList.remove("is-open");
      var t = $(".nav__trigger", el);
      if (t) t.setAttribute("aria-expanded", "false");
    }
    trigger.addEventListener("click", function () {
      item.classList.contains("is-open") ? close() : open();
    });
    if (finePointer) {
      item.addEventListener("mouseenter", open);
      item.addEventListener("mouseleave", function () { closeTimer = setTimeout(close, 160); });
    }
    item.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { close(); trigger.focus(); }
    });
    item.addEventListener("focusout", function (e) {
      if (!item.contains(e.relatedTarget)) close();
    });
  });
  document.addEventListener("click", function (e) {
    $$(".nav__item.is-open").forEach(function (o) {
      if (!o.contains(e.target)) {
        o.classList.remove("is-open");
        var t = $(".nav__trigger", o);
        if (t) t.setAttribute("aria-expanded", "false");
      }
    });
  });

  /* ---------- Mobile menu ---------- */
  var burger = $(".burger");
  var mobileNav = $("#mobile-nav");
  function setMenu(open) {
    if (!burger || !mobileNav) return;
    burger.setAttribute("aria-expanded", String(open));
    burger.setAttribute("aria-label", open ? burger.dataset.close : burger.dataset.open);
    mobileNav.classList.toggle("is-open", open);
    mobileNav.setAttribute("aria-hidden", String(!open));
    document.body.classList.toggle("nav-open", open);
    if (open) {
      mobileNav.removeAttribute("inert");
      var first = $("a, button", mobileNav);
      if (first) setTimeout(function () { first.focus(); }, 60);
    } else {
      mobileNav.setAttribute("inert", "");
    }
  }
  if (burger && mobileNav) {
    mobileNav.setAttribute("inert", "");
    burger.addEventListener("click", function () { setMenu(burger.getAttribute("aria-expanded") !== "true"); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && document.body.classList.contains("nav-open")) { setMenu(false); burger.focus(); }
    });
    // keep focus inside the open menu (burger + menu links)
    document.addEventListener("keydown", function (e) {
      if (e.key !== "Tab" || !document.body.classList.contains("nav-open")) return;
      var items = [burger].concat($$("a, button", mobileNav));
      var idx = items.indexOf(document.activeElement);
      if (e.shiftKey && idx <= 0) { e.preventDefault(); items[items.length - 1].focus(); }
      else if (!e.shiftKey && idx === items.length - 1) { e.preventDefault(); items[0].focus(); }
    });
    window.addEventListener("resize", function () { if (window.innerWidth >= 1080) setMenu(false); });
  }

  /* ---------- Split heading words (hero) ---------- */
  $$("[data-split]").forEach(function (el) {
    if (reduce) return;
    var i = 0;
    (function walk(node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (child) {
        if (child.nodeType === 3) {
          var frag = document.createDocumentFragment();
          child.textContent.split(/(\s+)/).forEach(function (part) {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(part)); return; }
            var w = document.createElement("span");
            w.className = "w";
            var inner = document.createElement("span");
            inner.style.setProperty("--wi", i++);
            inner.textContent = part;
            w.appendChild(inner);
            frag.appendChild(w);
          });
          node.replaceChild(frag, child);
        } else if (child.nodeType === 1 && child.classList.contains("accent")) {
          // keep gradient-text spans whole (background-clip:text breaks on transformed children)
          var wa = document.createElement("span");
          wa.className = "w";
          var ia = document.createElement("span");
          ia.style.setProperty("--wi", i++);
          node.replaceChild(wa, child);
          ia.appendChild(child);
          wa.appendChild(ia);
        } else if (child.nodeType === 1 && child.tagName !== "BR") {
          walk(child);
        }
      });
    })(el);
    el.classList.add("split-words");
    requestAnimationFrame(function () { requestAnimationFrame(function () { el.classList.add("is-in"); }); });
  });

  /* ---------- Scroll reveal ---------- */
  var revealEls = $$("[data-reveal]");
  function revealAll() { revealEls.forEach(function (el) { el.classList.add("is-in"); }); }
  if ("IntersectionObserver" in window && !reduce) {
    var ioAlive = false;
    var io = new IntersectionObserver(function (entries) {
      ioAlive = true;
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    revealEls.forEach(function (el) { io.observe(el); });
    // Safety net: an observer always reports once after observe(). If it never does, show everything.
    setTimeout(function () { if (!ioAlive) revealAll(); }, 2500);
  } else {
    revealAll();
  }
  window.__dtReady = true; // tells the inline guard in <head> that reveal is wired up

  /* ---------- Counters ---------- */
  var counters = $$("[data-count]");
  function runCounter(el) {
    var to = parseFloat(el.dataset.count);
    var from = parseFloat(el.dataset.from || "0");
    var dur = 1600;
    var start = null;
    function frame(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 4);
      el.textContent = Math.round(from + (to - from) * eased);
      if (p < 1) requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }
  if ("IntersectionObserver" in window && !reduce) {
    // The final value stays in the markup until the observer reports, so a dead observer never leaves "0".
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { runCounter(en.target); cio.unobserve(en.target); }
        else if (!en.target._armed) { en.target._armed = true; en.target.textContent = en.target.dataset.from || "0"; }
      });
    }, { threshold: 0.6 });
    counters.forEach(function (el) { cio.observe(el); });
  }

  /* ---------- Card spotlight + magnetic buttons ---------- */
  if (finePointer && !reduce) {
    document.addEventListener("pointermove", function (e) {
      var card = e.target.closest && e.target.closest(".card");
      if (!card) return;
      var r = card.getBoundingClientRect();
      card.style.setProperty("--mx", (e.clientX - r.left) + "px");
      card.style.setProperty("--my", (e.clientY - r.top) + "px");
    }, { passive: true });

    $$("[data-magnetic]").forEach(function (btn) {
      btn.addEventListener("pointermove", function (e) {
        var r = btn.getBoundingClientRect();
        var x = (e.clientX - r.left - r.width / 2) * 0.18;
        var y = (e.clientY - r.top - r.height / 2) * 0.3;
        btn.style.transform = "translate(" + x + "px," + y + "px)";
      });
      btn.addEventListener("pointerleave", function () { btn.style.transform = ""; });
    });
  }

  /* ---------- Method timeline progress ---------- */
  $$("[data-steps]").forEach(function (list) {
    var line = $(".steps__line span", list);
    var steps = $$(".step", list);
    function update() {
      var r = list.getBoundingClientRect();
      var vh = window.innerHeight;
      var p = (vh * 0.62 - r.top) / r.height;
      p = Math.max(0, Math.min(1, p));
      if (line) line.parentNode.style.setProperty("--progress", p.toFixed(3));
      if (line) line.style.setProperty("--progress", p.toFixed(3));
      steps.forEach(function (s) {
        var sr = s.getBoundingClientRect();
        s.classList.toggle("is-active", sr.top < vh * 0.66);
      });
    }
    if (reduce) {
      steps.forEach(function (s) { s.classList.add("is-active"); });
      if (line) line.style.setProperty("--progress", 1);
      return;
    }
    var raf = false;
    window.addEventListener("scroll", function () {
      if (!raf) { raf = true; requestAnimationFrame(function () { update(); raf = false; }); }
    }, { passive: true });
    window.addEventListener("resize", update);
    update();
  });

  /* ---------- Hero particles (canvas 2D, paused off-screen) ---------- */
  var canvas = $(".hero__canvas");
  if (canvas && !reduce && canvas.getContext) {
    var ctx = canvas.getContext("2d");
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var pts = [];
    var W = 0, H = 0, running = true, rafId;
    var mouse = { x: -9999, y: -9999 };
    function resize() {
      var rect = canvas.getBoundingClientRect();
      W = rect.width; H = rect.height;
      canvas.width = W * dpr; canvas.height = H * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var n = Math.round(Math.min(70, Math.max(26, (W * H) / 24000)));
      pts = [];
      for (var i = 0; i < n; i++) {
        pts.push({
          x: Math.random() * W, y: Math.random() * H,
          vx: (Math.random() - 0.5) * 0.22, vy: (Math.random() - 0.5) * 0.22,
          r: Math.random() * 1.4 + 0.6, g: Math.random() < 0.18
        });
      }
    }
    function draw() {
      ctx.clearRect(0, 0, W, H);
      var maxD = 140;
      for (var i = 0; i < pts.length; i++) {
        var p = pts[i];
        p.x += p.vx; p.y += p.vy;
        if (p.x < -10) p.x = W + 10; if (p.x > W + 10) p.x = -10;
        if (p.y < -10) p.y = H + 10; if (p.y > H + 10) p.y = -10;
        for (var j = i + 1; j < pts.length; j++) {
          var q = pts[j];
          var dx = p.x - q.x, dy = p.y - q.y;
          var d = dx * dx + dy * dy;
          if (d < maxD * maxD) {
            var a = 1 - Math.sqrt(d) / maxD;
            ctx.strokeStyle = "rgba(141,181,255," + (a * 0.22).toFixed(3) + ")";
            ctx.lineWidth = 1;
            ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(q.x, q.y); ctx.stroke();
          }
        }
        var mdx = p.x - mouse.x, mdy = p.y - mouse.y;
        var md = Math.sqrt(mdx * mdx + mdy * mdy);
        if (md < 180) {
          ctx.strokeStyle = "rgba(233,196,106," + ((1 - md / 180) * 0.35).toFixed(3) + ")";
          ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(mouse.x, mouse.y); ctx.stroke();
        }
        ctx.fillStyle = p.g ? "rgba(243,213,138,.9)" : "rgba(200,218,255,.75)";
        ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2); ctx.fill();
      }
      if (running) rafId = requestAnimationFrame(draw);
    }
    resize();
    window.addEventListener("resize", function () { clearTimeout(canvas._t); canvas._t = setTimeout(resize, 150); });
    var hero = canvas.closest(".hero");
    if (hero && finePointer) {
      hero.addEventListener("pointermove", function (e) {
        var r = canvas.getBoundingClientRect();
        mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top;
      });
      hero.addEventListener("pointerleave", function () { mouse.x = mouse.y = -9999; });
    }
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (en) {
        var vis = en[0].isIntersecting;
        if (vis && !running) { running = true; draw(); }
        else if (!vis) { running = false; cancelAnimationFrame(rafId); }
      }).observe(canvas);
    }
    document.addEventListener("visibilitychange", function () {
      if (document.hidden) { running = false; cancelAnimationFrame(rafId); }
      else if (!running) { running = true; draw(); }
    });
    draw();
  }

  /* ---------- Team filter + bio modal ---------- */
  var filterBtns = $$("[data-filter]");
  if (filterBtns.length) {
    filterBtns.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var f = btn.dataset.filter;
        filterBtns.forEach(function (b) { b.setAttribute("aria-pressed", String(b === btn)); });
        var shown = 0;
        $$(".team-grid .member").forEach(function (m) {
          var ok = f === "all" || (m.dataset.group || "").split(" ").indexOf(f) > -1;
          m.hidden = !ok;
          if (ok) {
            shown++;
            if (!reduce && m.animate) m.animate([{ opacity: 0, transform: "translateY(12px)" }, { opacity: 1, transform: "none" }], { duration: 450, delay: Math.min(shown, 12) * 30, easing: "cubic-bezier(.16,1,.3,1)", fill: "backwards" });
          }
        });
        var live = $("#team-count");
        if (live) live.textContent = live.dataset.tpl.replace("{n}", shown);
      });
    });
  }
  var modal = $("#bio-modal");
  if (modal && typeof modal.showModal === "function") {
    var modalContent = $(".modal__content", modal);
    var lastTrigger = null;
    $$("[data-bio]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var tpl = document.getElementById(btn.dataset.bio);
        if (!tpl) return;
        lastTrigger = btn;
        modalContent.innerHTML = "";
        modalContent.appendChild(tpl.content.cloneNode(true));
        modal.showModal();
        var h = $("h2", modal);
        if (h) { h.setAttribute("tabindex", "-1"); h.focus(); }
      });
    });
    $(".modal__close", modal).addEventListener("click", function () { modal.close(); });
    modal.addEventListener("click", function (e) { if (e.target === modal) modal.close(); });
    modal.addEventListener("close", function () { if (lastTrigger) lastTrigger.focus(); });
  } else if (modal) {
    // <dialog> unsupported: fall back to showing bios inline is not needed; templates remain accessible via LinkedIn
    $$("[data-bio]").forEach(function (btn) { btn.disabled = true; });
  }
  // open a bio from a hash such as #viet
  if (modal && location.hash) {
    var target = $('[data-bio="bio-' + location.hash.slice(1) + '"]');
    if (target) setTimeout(function () { target.click(); }, 400);
  }

  /* ---------- Contact form (static demo: validates, shows success, sends nothing) ---------- */
  var form = $("#contact-form");
  if (form) {
    form.setAttribute("novalidate", "");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var firstBad = null;
      $$(".field", form).forEach(function (f) {
        var inputs = $$("input, select, textarea", f);
        var bad = inputs.some(function (i) { return !i.checkValidity(); });
        if (inputs.length && inputs[0].type === "radio") bad = !inputs.some(function (i) { return i.checked; }) && inputs[0].required;
        f.classList.toggle("has-error", bad);
        inputs.forEach(function (i) { i.setAttribute("aria-invalid", String(bad)); });
        if (bad && !firstBad) firstBad = inputs[0];
      });
      if (firstBad) { firstBad.focus(); return; }
      var card = form.closest(".form-card");
      card.classList.add("is-sent");
      var ok = $(".form-success", card);
      if (ok) { ok.setAttribute("tabindex", "-1"); ok.focus(); }
    });
    form.addEventListener("input", function (e) {
      var f = e.target.closest(".field");
      if (f && f.classList.contains("has-error") && e.target.checkValidity()) { f.classList.remove("has-error"); e.target.setAttribute("aria-invalid", "false"); }
    });
    var again = $("[data-form-reset]");
    if (again) again.addEventListener("click", function () {
      form.reset();
      form.closest(".form-card").classList.remove("is-sent");
      var first = $("input", form); if (first) first.focus();
    });
  }

  /* ---------- Page transition (fade out on internal navigation) ---------- */
  if (!reduce && !("onpagereveal" in window)) {
    document.addEventListener("click", function (e) {
      var a = e.target.closest && e.target.closest("a[href]");
      if (!a || e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      if (a.target && a.target !== "_self") return;
      if (a.hasAttribute("download")) return;
      var href = a.getAttribute("href");
      if (!href || href.charAt(0) === "#" || /^(mailto|tel):/i.test(href)) return;
      if (a.protocol !== location.protocol || a.host !== location.host) return;
      if (a.pathname === location.pathname && a.hash) return;
      e.preventDefault();
      doc.classList.add("is-leaving");
      setTimeout(function () { location.href = a.href; }, 170);
    });
  }
  window.addEventListener("pageshow", function () { doc.classList.remove("is-leaving"); });

  /* ---------- Footer year ---------- */
  $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
