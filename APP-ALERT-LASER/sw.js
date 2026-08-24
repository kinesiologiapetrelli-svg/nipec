/* ALERT LASER — il guscio offline.
   Cambia VERSIONE a ogni pubblicazione: è l'unico modo perché i telefoni
   già installati si accorgano che c'è una versione nuova. */
var VERSIONE = "alert-laser-1";
var ROBA = ["./", "index.html", "manifest.webmanifest",
            "icona-192.png", "icona-512.png", "icona-maskable-512.png", "apple-touch-icon.png"];

self.addEventListener("install", function (e) {
  e.waitUntil(caches.open(VERSIONE).then(function (c) { return c.addAll(ROBA); }).then(function () {
    return self.skipWaiting();
  }));
});

self.addEventListener("activate", function (e) {
  e.waitUntil(caches.keys().then(function (chiavi) {
    return Promise.all(chiavi.filter(function (k) { return k !== VERSIONE; })
      .map(function (k) { return caches.delete(k); }));
  }).then(function () { return self.clients.claim(); }));
});

/* Rete prima, cassetto dopo: se c'è linea prendi la versione nuova,
   se non c'è l'app si apre lo stesso. */
self.addEventListener("fetch", function (e) {
  if (e.request.method !== "GET") return;
  var u = new URL(e.request.url);
  if (u.origin !== location.origin) return;
  e.respondWith(
    fetch(e.request).then(function (r) {
      var copia = r.clone();
      caches.open(VERSIONE).then(function (c) { c.put(e.request, copia); });
      return r;
    }).catch(function () {
      return caches.match(e.request).then(function (r) {
        return r || caches.match("index.html");
      });
    })
  );
});
