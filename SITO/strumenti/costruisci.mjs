import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'fs';
const NOMI = ['index','sq','en','laser-ares','laser-uriel','afrodite','borea-cryo','q-switch','metodo','formazione','chi-siamo','contatti','privacy'];
const b = await chromium.launch({ args:['--no-sandbox'] });
const p = await (await b.newContext({ viewport:{width:1440,height:1200} })).newPage();
await p.goto('http://127.0.0.1:8741/index.html', { waitUntil:'load', timeout:120000 });
await p.waitForTimeout(14000);
const fr = p.frames().slice(1);
fs.mkdirSync('grezzo', { recursive:true });
const mappaImg = {};
for (let i=0; i<NOMI.length; i++) {
  const f = fr[i];
  const r = await f.evaluate(async () => {
    // 1. risolvi le immagini in hash sha1
    const hash = async (u) => {
      const b = await (await fetch(new URL(u,'http://127.0.0.1:8741/').href)).arrayBuffer();
      const h = await crypto.subtle.digest('SHA-1', b);
      return [...new Uint8Array(h)].map(x=>x.toString(16).padStart(2,'0')).join('').slice(0,12);
    };
    const mappa = {};
    for (const el of document.querySelectorAll('img[src]')) {
      const u = el.getAttribute('src');
      if (/^(https?:|data:)/.test(u)) continue;
      const h = await hash(u);
      mappa[u] = h; el.setAttribute('src', 'immagini/' + h + '.jpg');
    }
    return { html: document.documentElement.outerHTML, titolo: document.title, mappa };
  });
  Object.assign(mappaImg, r.mappa);
  fs.writeFileSync(`grezzo/${NOMI[i]}.html`, r.html);
  console.log(`${NOMI[i].padEnd(14)} ${String(r.html.length).padStart(8)} B  ${r.titolo}`);
}
fs.writeFileSync('grezzo/_immagini.json', JSON.stringify(mappaImg, null, 1));
console.log('\nimmagini distinte:', new Set(Object.values(mappaImg)).size);
await b.close();
