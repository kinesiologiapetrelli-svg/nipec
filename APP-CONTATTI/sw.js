/* CONTATTI NIPEC — il guscio offline.
   Cambia VERSIONE a ogni pubblicazione: è l'unico modo perché i telefoni
   già installati vedano la versione nuova. */
const VERSIONE = 'contatti-nipec-12';
const ROBA = ['./','./index.html','./manifest.webmanifest','./caratteri/archivo.woff2',
              './icona-192.png','./icona-512.png','./apple-touch-icon.png'];
self.addEventListener('install', e => { self.skipWaiting();
  e.waitUntil(caches.open(VERSIONE).then(c => c.addAll(ROBA)).catch(()=>{})); });
self.addEventListener('activate', e => e.waitUntil(
  caches.keys().then(k => Promise.all(k.filter(x => x !== VERSIONE).map(x => caches.delete(x))))
    .then(() => self.clients.claim())));
self.addEventListener('fetch', e => {
  if(e.request.method !== 'GET') return;
  if(new URL(e.request.url).origin !== location.origin) return;
  e.respondWith(fetch(e.request).then(r => { if(r.ok){ const cp = r.clone();
    caches.open(VERSIONE).then(c => c.put(e.request, cp)); } return r; })
    .catch(() => caches.match(e.request).then(r => r || caches.match('./index.html'))));
});
