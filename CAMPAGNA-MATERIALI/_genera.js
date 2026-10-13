// Genera le immagini delle inserzioni: node _genera.js (serve playwright-core).
// Tre idee × due formati: 1080×1080 (feed) e 1080×1920 (storie e reel).
const { chromium } = require('playwright-core');
const path = require('path');
const fs = require('fs');
const R = path.resolve(__dirname, '..');
const F = 'file://' + R + '/SITO/assets/fonts/';
const LOGO = fs.readFileSync(R + '/MARCHIO/nipec-logo-orizzontale-negativo.svg', 'utf8');
const ARES = 'file://' + R + '/SITO/assets/img/ares.webp';
const APP = 'file://' + __dirname + '/_app-oggi.png';

const base = (w, h, corpo) => `<!doctype html><meta charset="utf-8"><style>
@font-face{font-family:A;font-weight:400;src:url(${F}archivo-latin-400-normal.woff2)}
@font-face{font-family:A;font-weight:600;src:url(${F}archivo-latin-600-normal.woff2)}
@font-face{font-family:A;font-weight:700;src:url(${F}archivo-latin-700-normal.woff2)}
*{box-sizing:border-box;margin:0}
body{width:${w}px;height:${h}px;overflow:hidden;font-family:A,sans-serif;background:#123A63;color:#fff;position:relative}
.logo{position:absolute;left:72px;top:64px;width:300px}
.logo svg{width:100%;height:auto;display:block}
.occhiello{white-space:nowrap;font-size:30px;letter-spacing:.2em;text-transform:uppercase;font-weight:600;color:#9CCBE8}
.piede{position:absolute;left:72px;right:72px;bottom:64px;display:flex;justify-content:space-between;align-items:center;font-size:30px;color:#D6E4F0}
.piede b{color:#fff}
.pill{background:#fff;color:#123A63;font-weight:700;border-radius:999px;padding:18px 34px;font-size:32px}
.anello{position:absolute;border-radius:50%;border:3px solid rgba(255,255,255,.08)}
</style><body>${corpo}</body>`;

const idee = {
  noleggio: (w, h) => {
    const alto = h > w;
    return base(w, h, `
<div style="position:absolute;inset:0;background:radial-gradient(circle at 75% ${alto?50:55}%, #1C6EA4 0, #123A63 60%)"></div>
<div class="logo">${LOGO}</div>
<div style="position:absolute;left:72px;top:${alto?280:220}px;max-width:${alto?940:560}px">
  <p class="occhiello">Laser IA a noleggio · ARES 2026</p>
  <h1 style="font-size:${alto?130:82}px;line-height:1;letter-spacing:-.02em;margin-top:24px;white-space:nowrap">500 € al mese.</h1>
  <p style="font-size:${alto?64:50}px;font-weight:700;line-height:1.1;margin-top:18px;color:#9CCBE8">Lo fermi quando vuoi.</p>
</div>
<div style="position:absolute;background:#fff;border-radius:40px;overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.35);${alto?'left:220px;top:780px;width:640px;height:600px':'left:680px;top:330px;width:330px;height:360px'};display:flex;align-items:center;justify-content:center"><img src="${ARES}" style="height:96%;width:auto"></div>
<ul style="position:absolute;left:72px;top:${alto?1450:600}px;list-style:none;padding:0;font-size:${alto?44:36}px;line-height:1.7;color:#D6E4F0">
  <li>✓ Senza vincoli</li><li>✓ Senza firme</li><li>✓ Senza anticipi</li>
</ul>
<div class="piede"><span>+ IVA · CE italiana · MDR</span><span class="pill">Scrivici</span></div>`);
  },
  demetra: (w, h) => {
    const alto = h > w;
    return base(w, h, `
<div class="anello" style="width:${w*1.1}px;height:${w*1.1}px;right:-${w*0.45}px;top:${alto?420:-160}px"></div>
<div class="logo">${LOGO}</div>
<div style="position:absolute;left:72px;right:72px;top:${alto?400:200}px">
  <p class="occhiello">Il sistema Demetra</p>
  <h1 style="font-size:${alto?124:100}px;line-height:1.02;margin-top:24px">Non resti mai da sola.</h1>
  <p style="font-size:${alto?46:38}px;line-height:1.4;color:#D6E4F0;margin-top:${alto?48:32}px">Una tutor sempre in contatto con te, <b style="color:#fff">su un canale WhatsApp tutto tuo.</b> E formazione costante, non una giornata e poi arrangiati.</p>
</div>
${alto ? `<div style="position:absolute;left:72px;right:72px;top:1060px;display:flex;flex-direction:column;gap:22px;font-size:36px;line-height:1.35">
  <p style="font-size:24px;letter-spacing:.18em;text-transform:uppercase;color:#9CCBE8;font-weight:600">Un esempio</p>
  <div style="align-self:flex-end;max-width:760px;background:#D9FDD3;color:#0F1E30;border-radius:28px 28px 6px 28px;padding:24px 30px">Ho una cliente con la pelle scura, da dove parto con i parametri?</div>
  <div style="align-self:flex-start;max-width:760px;background:#fff;color:#0F1E30;border-radius:28px 28px 28px 6px;padding:24px 30px"><b style="color:#1C6EA4">Tutor Demetra</b><br>Ciao! Ti mando subito la scheda giusta. Prima seduta di prova su una zona piccola, poi mi dici com’è andata.</div>
</div>` : ''}
<div class="piede"><span>Laser IA a noleggio<br><b>500 € al mese + IVA</b></span><span class="pill">Scrivici</span></div>`);
  },
  app: (w, h) => {
    const alto = h > w;
    const tw = alto ? 560 : 400;
    return base(w, h, `
<div class="logo">${LOGO}</div>
<div style="position:absolute;left:72px;top:${alto?280:230}px;max-width:${alto?940:470}px">
  <p class="occhiello">Insieme al laser</p>
  <h1 style="font-size:${alto?100:68}px;line-height:1.04;margin-top:24px">Ogni mattina ti dice chi richiamare.</h1>
  <p style="font-size:${alto?44:36}px;line-height:1.35;color:#D6E4F0;margin-top:30px">E quanto vale quella telefonata.</p>
</div>
<div style="position:absolute;${alto?'left:50%;transform:translateX(-50%);top:760px':'right:64px;top:150px'};width:${tw}px;padding:16px;border-radius:64px;background:#0B2440;box-shadow:0 40px 80px rgba(0,0,0,.4)">
  <div style="border-radius:50px;overflow:hidden;height:${alto?tw*1.75:tw*1.85}px"><img src="${APP}" style="width:100%;display:block"></div>
</div>
<div class="piede" ${alto?'':'style="right:auto;width:440px;flex-direction:column;align-items:flex-start;gap:24px"'}><span>Inclusa nel noleggio.<br><b>Chiedi agli altri se te la danno.</b></span><span class="pill">Prova la demo</span></div>`);
  }
};

(async () => {
  const b = await chromium.launch({ executablePath: process.env.CHROMIUM || '/opt/pw-browsers/chromium' });
  for (const [nome, f] of Object.entries(idee)) {
    for (const [w, h, suff] of [[1080, 1080, 'quadrato'], [1080, 1920, 'storia']]) {
      const p = await b.newPage({ viewport: { width: w, height: h } });
      const tmp = path.join(__dirname, '_tmp.html');
      fs.writeFileSync(tmp, f(w, h));
      await p.goto('file://' + tmp, { waitUntil: 'load' });
      await p.evaluate(() => document.fonts.ready);
      await p.screenshot({ path: path.join(__dirname, `NIPEC-${nome}-${suff}.png`) });
      await p.close();
    }
  }
  fs.unlinkSync(path.join(__dirname, '_tmp.html'));
  await b.close();
})();
