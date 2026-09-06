/* MAGAZZINO NIPEC — service worker.
   L'app deve aprirsi anche senza rete, MA gli aggiornamenti devono arrivare:
   per questo la pagina si prende prima dalla rete e solo se non c'è si usa la copia. */
var CACHE = "magazzino-nipec-v1";
var FILE = ["./", "./index.html", "./manifest.webmanifest",
            "./icona-192.png", "./icona-512.png", "./icona-maskable-512.png", "./apple-touch-icon.png"];

self.addEventListener("install", function (e) {
  e.waitUntil(caches.open(CACHE).then(function (c) { return c.addAll(FILE); })
    .then(function () { return self.skipWaiting(); }));
});
self.addEventListener("activate", function (e) {
  e.waitUntil(caches.keys().then(function (k) {
    return Promise.all(k.map(function (n) { return n === CACHE ? null : caches.delete(n); }));
  }).then(function () { return self.clients.claim(); }));
});
self.addEventListener("fetch", function (e) {
  if (e.request.method !== "GET") return;
  var pagina = e.request.mode === "navigate" ||
               (e.request.destination === "document") ||
               e.request.url.indexOf("index.html") >= 0;
  if (pagina) {
    /* rete per prima: così una versione nuova si vede subito */
    e.respondWith(fetch(e.request).then(function (r) {
      var copia = r.clone();
      caches.open(CACHE).then(function (c) { c.put(e.request, copia); });
      return r;
    }).catch(function () {
      return caches.match(e.request).then(function (r) { return r || caches.match("./index.html"); });
    }));
    return;
  }
  /* il resto (icone, manifest) dalla cache: non cambia mai */
  e.respondWith(caches.match(e.request).then(function (r) { return r || fetch(e.request); }));
});
