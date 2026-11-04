// Controlla che nessuna pagina delle brochure tagli il testo: le pagine sono alte 297 mm e nascondono cio' che esce.
// Per ogni pagina misura il fondo del contenuto e lo confronta con l'inizio della fascia fissa in basso (piede, banda o firma).
// Uso:  node controlla-pagine.mjs [sorgenti/brochure-*.html ...]     (senza argomenti: tutte)
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const QUI = path.dirname(fileURLToPath(import.meta.url));
const SORG = path.join(QUI, 'sorgenti');
const files = process.argv.slice(2).length ? process.argv.slice(2).map((f) => path.resolve(f))
  : fs.readdirSync(SORG).filter((f) => f.endsWith('.html')).sort().map((f) => path.join(SORG, f));

const browser = await chromium.launch({ args: ['--no-sandbox', '--allow-file-access-from-files'] });
const page = await browser.newPage({ viewport: { width: 794, height: 1123 } });
await page.emulateMedia({ media: 'print' });
let problemi = 0;
for (const f of files) {
  await page.goto('file://' + f, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  const r = await page.evaluate(() => {
    const mm = 96 / 25.4;
    return [...document.querySelectorAll('.page')].map((p, i) => {
      const R = p.getBoundingClientRect();
      const fisse = [...p.querySelectorAll('.piede,.banda,.firma')];
      const limite = fisse.length ? Math.min(...fisse.map((e) => e.getBoundingClientRect().top)) : R.bottom;
      let fondo = 0, destra = 0, chi = '';
      for (const e of p.querySelectorAll('*')) {
        if (e.classList.contains('p4') || e.closest('.piede,.banda,.firma') || e.closest('svg') || e.tagName === 'IMG' && e.closest('.foto')) continue;
        if (getComputedStyle(e).position === 'absolute') continue;
        const b = e.getBoundingClientRect();
        if (!b.width || !b.height) continue;
        if (b.bottom > fondo) { fondo = b.bottom; chi = e.className || e.tagName; }
        destra = Math.max(destra, b.right);
      }
      const cta = p.querySelector('.cta'), con = p.querySelector('.contatti');
      const respiro = cta && con ? +((con.getBoundingClientRect().top - cta.getBoundingClientRect().bottom) / mm).toFixed(1) : null;
      return { n: i + 1, respiro, vuoto_mm: +((limite - fondo) / mm).toFixed(1), destra_mm: +((R.right - destra) / mm).toFixed(1), chi: String(chi).slice(0, 24) };
    });
  });
  const brutti = r.filter((x) => x.vuoto_mm < 2 || x.destra_mm < 8 || (x.respiro !== null && x.respiro < 5));
  problemi += brutti.length;
  const riga = r.map((x) => `p${x.n}:${x.vuoto_mm}mm` + (x.respiro !== null ? `(tra riquadro e contatti ${x.respiro})` : '')).join('  ');
  console.log((brutti.length ? 'XX ' : 'ok ') + path.basename(f).padEnd(30) + riga + (brutti.length ? '   <- ' + brutti.map((x) => `p${x.n} ${x.chi} (vuoto ${x.vuoto_mm}, margine dx ${x.destra_mm})`).join('; ') : ''));
}
await browser.close();
console.log(problemi ? `\n${problemi} pagine da sistemare` : '\ntutte le pagine entrano');
process.exit(problemi ? 1 : 0);
