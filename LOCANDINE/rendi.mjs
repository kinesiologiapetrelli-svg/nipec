/* Rende le locandine alla misura esatta. Chromium da riga di comando
   non rispetta --window-size al pixel: Playwright sì. */
import { chromium } from 'playwright-core';
const L = 1080, A = 1350;
const b = await chromium.launch({ executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
                                  args:['--no-sandbox','--disable-gpu'] });
for (const nome of process.argv.slice(2)) {
  const p = await b.newPage({ viewport:{ width:L, height:A }, deviceScaleFactor:1 });
  await p.goto('file:///home/user/nipec/LOCANDINE/' + nome + '.html', { waitUntil:'networkidle' });
  // controllo che niente esca dal foglio prima di scattare
  const h = await p.evaluate(() => document.body.scrollHeight);
  await p.screenshot({ path: '/home/user/nipec/LOCANDINE/' + nome + '.png', clip:{ x:0, y:0, width:L, height:A } });
  console.log(`${nome}.png  contenuto alto ${h}px su ${A}px  ${h > A ? '← ESCE DAL FOGLIO' : 'ok'}`);
  await p.close();
}
await b.close();
