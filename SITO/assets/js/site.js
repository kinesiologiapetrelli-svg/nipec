/* NIPEC 5.0 — interazioni del sito. Nessuna libreria esterna. */
(function () {
  'use strict';
  var doc = document, root = doc.documentElement;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Header: ombra e barra di avanzamento ---------- */
  var hd = doc.querySelector('.hd');
  var bar = doc.querySelector('.hd__progress');
  var ticking = false;
  function onScroll() {
    var y = window.scrollY || root.scrollTop;
    var max = (root.scrollHeight - window.innerHeight) || 1;
    if (hd) hd.classList.toggle('is-scrolled', y > 24);
    root.classList.toggle('is-scrolled', y > 24);
    if (bar) bar.style.setProperty('--p', Math.min(1, Math.max(0, y / max)).toFixed(4));
    ticking = false;
  }
  window.addEventListener('scroll', function () {
    if (!ticking) { window.requestAnimationFrame(onScroll); ticking = true; }
  }, { passive: true });
  onScroll();

  /* ---------- Mega menu (tastiera e tocco) ---------- */
  doc.querySelectorAll('.dd').forEach(function (dd) {
    var btn = dd.querySelector('.nav__link');
    if (!btn) return;
    btn.addEventListener('click', function (e) {
      var open = !dd.classList.contains('is-open');
      dd.classList.toggle('is-open', open);
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      e.stopPropagation();
    });
    dd.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { dd.classList.remove('is-open'); btn.setAttribute('aria-expanded', 'false'); btn.focus(); }
    });
    doc.addEventListener('click', function (e) {
      if (!dd.contains(e.target)) { dd.classList.remove('is-open'); btn.setAttribute('aria-expanded', 'false'); }
    });
  });

  /* ---------- Menu a tutto schermo (telefono) ---------- */
  var drawer = doc.getElementById('drawer');
  var burger = doc.querySelector('.burger');
  var lastFocus = null;
  function setDrawer(open) {
    if (!drawer) return;
    drawer.classList.toggle('is-open', open);
    drawer.setAttribute('aria-hidden', open ? 'false' : 'true');
    if (burger) burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    doc.body.style.overflow = open ? 'hidden' : '';
    if (open) {
      lastFocus = doc.activeElement;
      var first = drawer.querySelector('button, a');
      if (first) first.focus();
    } else if (lastFocus) {
      lastFocus.focus();
    }
  }
  if (burger) burger.addEventListener('click', function () { setDrawer(true); });
  if (drawer) {
    drawer.querySelectorAll('[data-close]').forEach(function (b) { b.addEventListener('click', function () { setDrawer(false); }); });
    drawer.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') setDrawer(false);
      if (e.key === 'Tab') {
        var f = drawer.querySelectorAll('a, button');
        var a = f[0], z = f[f.length - 1];
        if (e.shiftKey && doc.activeElement === a) { e.preventDefault(); z.focus(); }
        else if (!e.shiftKey && doc.activeElement === z) { e.preventDefault(); a.focus(); }
      }
    });
  }

  /* ---------- Comparsa allo scroll ---------- */
  var sel = [
    'main .section .head', 'main .section .head-row', 'main .grid > *', 'main .products > *', 'main .path > li',
    'main .checks > li', 'main .faq > details', 'main .phase', 'main .cta-box', 'main .cta-band', 'main .table-box',
    'main .split__a', 'main .action-list', 'main .form', 'main .rule-item', 'main .note-box'
  ].join(',');
  // Solo gli elementi sotto la piega: quello che si vede all'apertura resta visibile subito.
  var fold = window.innerHeight || 800;
  var items = Array.prototype.slice.call(doc.querySelectorAll(sel)).filter(function (el) {
    return !el.closest('.hero') && el.getBoundingClientRect().top > fold;
  });
  if (!reduce && 'IntersectionObserver' in window) {
    items.forEach(function (el) {
      var i = Array.prototype.indexOf.call(el.parentNode.children, el);
      el.style.setProperty('--d', (Math.min(i, 6) * 0.07) + 's');
      el.classList.add('rv');
    });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    items.forEach(function (el) { io.observe(el); });
  }

  /* ---------- Filtri tecnologie ---------- */
  doc.querySelectorAll('[data-filters]').forEach(function (group) {
    var list = doc.getElementById(group.getAttribute('data-filters'));
    if (!list) return;
    group.querySelectorAll('button').forEach(function (b) {
      b.addEventListener('click', function () {
        var f = b.getAttribute('data-filter');
        group.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
        list.querySelectorAll('[data-cat]').forEach(function (card) {
          var show = f === 'all' || card.getAttribute('data-cat') === f;
          card.hidden = !show;
          if (show) { card.classList.remove('pop'); void card.offsetWidth; card.classList.add('pop'); card.classList.add('in'); }
        });
      });
    });
  });

  /* ---------- Sottomenu prodotto: voce attiva ---------- */
  var sub = doc.querySelector('.subnav');
  if (sub && 'IntersectionObserver' in window) {
    var links = sub.querySelectorAll('a[href^="#"]');
    var map = {};
    links.forEach(function (a) { var t = doc.getElementById(a.getAttribute('href').slice(1)); if (t) map[t.id] = a; });
    var so = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          links.forEach(function (a) { a.classList.remove('is-active'); a.removeAttribute('aria-current'); });
          var a = map[en.target.id]; if (a) { a.classList.add('is-active'); a.setAttribute('aria-current', 'true'); }
        }
      });
    }, { rootMargin: '-40% 0px -55% 0px' });
    Object.keys(map).forEach(function (id) { so.observe(doc.getElementById(id)); });
  }

  /* ---------- Modulo contatti (Netlify Forms) ---------- */
  var form = doc.querySelector('form[data-netlify]');
  if (form) {
    var ok = doc.getElementById('form-success');
    var err = form.querySelector('.form__error');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var btn = form.querySelector('[type="submit"]');
      if (btn) { btn.disabled = true; btn.dataset.label = btn.textContent; btn.textContent = btn.getAttribute('data-sending') || '…'; }
      var body = new URLSearchParams(new FormData(form)).toString();
      fetch(form.getAttribute('action') || '/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: body })
        .then(function (r) { if (!r.ok) throw new Error(r.status); })
        .then(function () {
          form.hidden = true;
          if (ok) { ok.hidden = false; ok.classList.add('is-on'); ok.setAttribute('tabindex', '-1'); ok.focus(); }
        })
        .catch(function () {
          if (err) err.classList.add('is-on');
          if (btn) { btn.disabled = false; btn.textContent = btn.dataset.label; }
        });
    });
  }

  /* ---------- Anno nel footer ---------- */
  doc.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
