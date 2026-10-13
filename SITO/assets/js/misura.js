/* NIPEC 5.0 — misura delle campagne.
   Finché gli ID qui sotto sono vuoti non parte niente: nessun banner, nessun cookie.
   Quando li riempi, il banner chiede il consenso e Pixel e Google partono solo dopo un «Accetto». */
(function () {
  'use strict';

  var ID = {
    META_PIXEL: '',      // Meta → Gestione eventi → il numero del Pixel (15-16 cifre)
    GOOGLE_TAG: '',      // Google Ads → Strumenti → Google tag: «AW-…» (oppure «G-…» di Analytics)
    GOOGLE_LEAD: '',     // conversione «Modulo inviato»: «AW-…/etichetta»
    GOOGLE_WHATSAPP: ''  // conversione «Clic su WhatsApp»: «AW-…/etichetta»
  };

  var doc = document, win = window;
  var CHIAVE = 'nipec-consenso';
  var SEI_MESI = 1000 * 60 * 60 * 24 * 182;

  /* ---------- Da dove arriva: utm e codice dell'annuncio ---------- */
  // Si legge all'arrivo e si tiene per la visita, così il modulo e WhatsApp sanno quale annuncio ha portato il contatto.
  var fonte = '';
  try {
    var q = new URLSearchParams(win.location.search);
    var pezzi = ['utm_source', 'utm_campaign', 'utm_content'].map(function (k) { return q.get(k) || ''; });
    if (q.get('gclid')) pezzi[0] = pezzi[0] || 'google';
    if (q.get('fbclid')) pezzi[0] = pezzi[0] || 'meta';
    if (pezzi.join('')) sessionStorage.setItem('nipec-fonte', pezzi.filter(Boolean).join(' / '));
    fonte = sessionStorage.getItem('nipec-fonte') || '';
  } catch (e) {}

  if (fonte) {
    doc.querySelectorAll('input[name="fonte"]').forEach(function (i) { i.value = fonte; });
    var codice = fonte.split(' / ').pop();
    doc.querySelectorAll('a[href*="wa.me/"]').forEach(function (a) {
      // Si aggiunge in coda già codificato: WhatsApp non legge i «+» come spazi.
      var h = a.getAttribute('href');
      if (h.indexOf('text=') !== -1 && h.indexOf('%5Brif') === -1) a.setAttribute('href', h + encodeURIComponent(' [rif: ' + codice + ']'));
    });
  }

  /* ---------- Senza ID non si chiede niente ---------- */
  var attivo = !!(ID.META_PIXEL || ID.GOOGLE_TAG);
  if (!attivo) return;

  var lingua = (doc.documentElement.lang || 'it').slice(0, 2);
  var TESTI = {
    it: { t: 'Cookie per misurare le nostre pubblicità', p: 'Se accetti, usiamo Meta Pixel e Google per sapere quali annunci portano qui i centri che ci scrivono. Se rifiuti, il sito funziona uguale.', si: 'Accetto', no: 'Rifiuto', info: 'Informativa', pref: 'Preferenze cookie' },
    sq: { t: 'Cookie për të matur reklamat tona', p: 'Nëse pranon, përdorim Meta Pixel dhe Google për të ditur cilat reklama sjellin këtu qendrat që na shkruajnë. Nëse refuzon, faqja funksionon njësoj.', si: 'Pranoj', no: 'Refuzoj', info: 'Informacion', pref: 'Preferencat e cookie' },
    en: { t: 'Cookies to measure our advertising', p: 'If you accept, we use Meta Pixel and Google to learn which ads bring the salons that contact us. If you decline, the site works just the same.', si: 'Accept', no: 'Decline', info: 'Privacy notice', pref: 'Cookie preferences' },
    es: { t: 'Cookies para medir nuestra publicidad', p: 'Si aceptas, usamos Meta Pixel y Google para saber qué anuncios traen aquí a los centros que nos escriben. Si rechazas, el sitio funciona igual.', si: 'Acepto', no: 'Rechazo', info: 'Información', pref: 'Preferencias de cookies' }
  };
  var T = TESTI[lingua] || TESTI.it;
  var link = doc.querySelector('a[href$="privacy.html"]');
  var privacy = link ? link.getAttribute('href') : 'privacy.html';

  function leggi() {
    try {
      var s = JSON.parse(localStorage.getItem(CHIAVE) || 'null');
      if (s && Date.now() - s.quando < SEI_MESI) return s.scelta;
    } catch (e) {}
    return null;
  }
  function scrivi(scelta) {
    try { localStorage.setItem(CHIAVE, JSON.stringify({ scelta: scelta, quando: Date.now() })); } catch (e) {}
  }

  /* ---------- Gli strumenti, solo dopo il sì ---------- */
  var caricati = false;
  function script(src) { var s = doc.createElement('script'); s.async = true; s.src = src; doc.head.appendChild(s); }
  function carica() {
    if (caricati) return;
    caricati = true;
    if (ID.META_PIXEL) {
      var f = win.fbq = function () { f.callMethod ? f.callMethod.apply(f, arguments) : f.queue.push(arguments); };
      if (!win._fbq) win._fbq = f;
      f.push = f; f.loaded = true; f.version = '2.0'; f.queue = [];
      script('https://connect.facebook.net/en_US/fbevents.js');
      win.fbq('init', ID.META_PIXEL);
      win.fbq('track', 'PageView');
    }
    if (ID.GOOGLE_TAG) {
      win.dataLayer = win.dataLayer || [];
      win.gtag = function () { win.dataLayer.push(arguments); };
      win.gtag('js', new Date());
      win.gtag('config', ID.GOOGLE_TAG);
      script('https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(ID.GOOGLE_TAG));
    }
  }

  function evento(tipo) {
    if (!caricati) return;
    if (win.fbq) win.fbq('track', tipo === 'lead' ? 'Lead' : 'Contact');
    if (win.gtag) {
      var invio = tipo === 'lead' ? ID.GOOGLE_LEAD : ID.GOOGLE_WHATSAPP;
      if (invio) win.gtag('event', 'conversion', { send_to: invio });
      win.gtag('event', tipo === 'lead' ? 'generate_lead' : 'whatsapp_click');
    }
  }
  doc.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href*="wa.me/"]');
    if (a) evento('whatsapp');
  });
  doc.addEventListener('nipec:lead', function () { evento('lead'); });

  /* ---------- Il banner ---------- */
  var banner;
  function chiudi() { if (banner) { banner.remove(); banner = null; } }
  function mostra() {
    if (banner) return;
    banner = doc.createElement('div');
    banner.className = 'consenso';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-live', 'polite');
    banner.setAttribute('aria-label', T.t);
    banner.innerHTML =
      '<p class="consenso__t"></p><p class="consenso__p"></p>' +
      '<div class="consenso__azioni"><button type="button" class="btn btn--outline btn--sm" data-scelta="no"></button>' +
      '<button type="button" class="btn btn--primary btn--sm" data-scelta="si"></button>' +
      '<a class="consenso__info"></a></div>';
    banner.querySelector('.consenso__t').textContent = T.t;
    banner.querySelector('.consenso__p').textContent = T.p;
    banner.querySelector('[data-scelta="no"]').textContent = T.no;
    banner.querySelector('[data-scelta="si"]').textContent = T.si;
    var info = banner.querySelector('.consenso__info');
    info.textContent = T.info; info.href = privacy;
    banner.addEventListener('click', function (e) {
      var b = e.target.closest('[data-scelta]');
      if (!b) return;
      var s = b.getAttribute('data-scelta');
      var prima = leggi();
      scrivi(s);
      chiudi();
      if (s === 'si') carica();
      else if (prima === 'si' && caricati) win.location.reload(); // revoca: si ricarica senza strumenti
    });
    doc.body.appendChild(banner);
  }

  // Il link per cambiare idea, accanto all'informativa nel piè di pagina.
  var legale = doc.querySelector('.ft__bottom nav');
  if (legale) {
    var pref = doc.createElement('button');
    pref.type = 'button';
    pref.className = 'consenso__riapri';
    pref.textContent = T.pref;
    pref.addEventListener('click', mostra);
    legale.appendChild(pref);
  }

  var scelta = leggi();
  if (scelta === 'si') carica();
  else if (scelta === null) mostra();
})();
