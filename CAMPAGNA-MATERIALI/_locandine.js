// Genera le locandine della campagna noleggio: node _locandine.js (serve playwright-core).
// Quattro locandine, una per testo dell'annuncio, in due formati:
//   LOCANDINA-n-social.png  1080×1350 (feed Instagram e Facebook, 4:5)
//   LOCANDINA-n-A4.png/pdf  A4 a 300 dpi, con il codice QR che apre WhatsApp col messaggio «NOLEGGIO [LOC-n]»
// I QR stanno in _qr/ (generati con segno: https://wa.me/393518466025?text=Ciao NIPEC, NOLEGGIO [LOC-n]).
const { chromium } = require('playwright-core');
const path = require('path');
const fs = require('fs');
const R = path.resolve(__dirname, '..');
const F = 'file://' + R + '/SITO/assets/fonts/';
const LOGO = fs.readFileSync(R + '/MARCHIO/nipec-logo-orizzontale.svg', 'utf8');
const LOGO_NEG = fs.readFileSync(R + '/MARCHIO/nipec-logo-orizzontale-negativo.svg', 'utf8');
const ARES = 'file://' + __dirname + '/_ares-scontornato.png';  // ares.webp senza il fondo grigio
const APP = 'file://' + __dirname + '/_app-oggi.png';
const W = 1080;

const css = (H) => `
@font-face{font-family:A;font-weight:400;src:url(${F}archivo-latin-400-normal.woff2)}
@font-face{font-family:A;font-weight:600;src:url(${F}archivo-latin-600-normal.woff2)}
@font-face{font-family:A;font-weight:700;src:url(${F}archivo-latin-700-normal.woff2)}
*{box-sizing:border-box;margin:0;padding:0}
body{width:${W}px;height:${H}px;overflow:hidden;font-family:A,sans-serif;display:flex;flex-direction:column;background:#fff;color:#123A63}
.su{flex:1;position:relative;background:#fff;overflow:hidden}
.giu{background:#123A63;color:#fff;padding:56px 72px 52px;position:relative}
.giu.alto{flex:1;display:flex;flex-direction:column}
.logo{position:absolute;left:72px;top:60px;width:250px;z-index:2}.logo svg{width:100%;height:auto;display:block}
.etic{position:absolute;right:72px;top:74px;font-size:24px;letter-spacing:.2em;font-weight:700;color:#1C6EA4;text-transform:uppercase;z-index:2}
h1{font-size:84px;line-height:1.02;letter-spacing:-.02em;font-weight:700}
.sub{font-size:36px;line-height:1.38;color:#D6E4F0;margin-top:22px}
.sub b{color:#fff}
.badge{display:flex;flex-wrap:wrap;gap:14px;margin-top:30px}
.badge span{border:2px solid #5AA6D6;color:#fff;border-radius:999px;padding:12px 24px;font-size:28px;font-weight:700;letter-spacing:.04em}
.pie{display:flex;align-items:center;justify-content:space-between;gap:30px;margin-top:40px;padding-top:32px;border-top:2px solid rgba(255,255,255,.18)}
.cta{font-size:30px;color:#D6E4F0;line-height:1.3}
.cta b{display:block;font-size:46px;color:#fff;letter-spacing:.01em}
.iva{font-size:24px;color:#9CCBE8}
.qr{background:#fff;border-radius:18px;padding:10px;width:190px;flex:none;text-align:center}
.qr img{width:100%;display:block}.qr p{font-size:17px;color:#123A63;font-weight:700;margin-top:4px}
.bolla{max-width:700px;border-radius:30px;padding:24px 30px;font-size:33px;line-height:1.35;color:#0F1E30;box-shadow:0 12px 30px rgba(18,58,99,.12)}
.lei{align-self:flex-end;background:#D9FDD3;border-bottom-right-radius:8px}
.tut{align-self:flex-start;background:#F1F5F9;border-bottom-left-radius:8px}
.chat{position:absolute;left:72px;right:72px;top:150px;bottom:36px;display:flex;flex-direction:column;justify-content:center;gap:20px}
.tut b{color:#1C6EA4;display:block;font-size:26px;margin-bottom:4px}
.dom{display:grid;grid-template-columns:86px 1fr;gap:6px 26px;margin-top:44px;align-items:start}
.dom .n{width:86px;height:86px;border-radius:50%;background:#5AA6D6;color:#123A63;font-size:48px;font-weight:700;display:flex;align-items:center;justify-content:center;grid-row:span 2}
.dom .q{font-size:38px;font-weight:700;line-height:1.2;padding-top:6px}
.dom .a{font-size:32px;color:#9CCBE8;margin-bottom:30px}
.dom.grande{gap:10px 30px;margin-top:80px}.dom.grande .q{font-size:46px}.dom.grande .a{font-size:38px;margin-bottom:64px}
`;

const pie = (n, a4) => `<div class="pie"><div class="cta">Scrivi NOLEGGIO su WhatsApp<b>351 846 6025</b><span class="iva">500 € al mese + IVA · nipecestetica.com</span></div>
${a4 ? `<div class="qr"><img src="file://${__dirname}/_qr/qr-LOC-${n}.svg"><p>Inquadra e scrivici</p></div>` : ''}</div>`;

const locandine = [
  // 1 · prezzo, senza firme
  (H, a4) => `<div class="su"><div class="logo">${LOGO}</div><div class="etic">Laser IA a noleggio</div>
  <img src="${ARES}" style="position:absolute;left:50%;transform:translateX(-62%);bottom:0;height:${a4 ? 82 : 78}%">
  <div style="position:absolute;right:80px;top:${a4 ? 260 : 190}px;width:290px;height:290px;border-radius:50%;background:#1C6EA4;color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;box-shadow:0 20px 50px rgba(18,58,99,.35);transform:rotate(-8deg)">
    <span style="font-size:96px;font-weight:700;line-height:1">500 €</span><span style="font-size:30px;font-weight:600;margin-top:6px">al mese + IVA</span></div></div>
  <div class="giu"><h1>Un laser con intelligenza artificiale. Ti fermi quando vuoi.</h1>
  <div class="badge"><span>SENZA VINCOLI</span><span>SENZA FIRME</span><span>SENZA ANTICIPI</span></div>${pie(1, a4)}</div>`,
  // 2 · Demetra
  (H, a4) => `<div class="su"><div class="logo">${LOGO}</div><div class="etic">Il sistema Demetra</div>
  <div class="chat" style="font-size:${a4 ? 36 : 30}px">
  <div class="bolla lei" style="font-size:inherit">Ho una cliente con la pelle scura, da dove parto con i parametri?</div>
  <div class="bolla tut" style="font-size:inherit"><b>Tutor Demetra</b>Ciao! Ti mando subito la scheda giusta. Prima seduta di prova su una zona piccola, poi mi dici com’è andata.</div>
  ${a4 ? '<div class="bolla lei" style="font-size:inherit">Fatto, tutto perfetto. Grazie!</div>' : ''}</div></div>
  <div class="giu"><h1>Non resti mai da sola.</h1>
  <p class="sub">Con il laser a noleggio entri nel sistema Demetra: <b>una tutor sempre in contatto con te, su un canale WhatsApp tutto tuo.</b> E formazione costante, non una giornata e poi arrangiati.</p>
  <div class="badge"><span>LASER CON IA</span><span>SENZA FIRME</span><span>SENZA ANTICIPI</span></div>${pie(2, a4)}</div>`,
  // 3 · app in più + marketing
  (H, a4) => `<div class="su"><div class="logo">${LOGO}</div><div class="etic">E in più</div>
  <div style="position:absolute;right:90px;top:${a4 ? 190 : 150}px;width:${a4 ? 400 : 340}px;padding:12px;border-radius:52px;background:#0B2440;box-shadow:0 30px 60px rgba(18,58,99,.35)">
    <div style="border-radius:42px;overflow:hidden;height:${a4 ? 760 : 600}px"><img src="${APP}" style="width:100%;display:block"></div></div>
  <img src="${ARES}" style="position:absolute;left:30px;bottom:0;height:${a4 ? 78 : 76}%">
  </div>
  <div class="giu"><h1>Il laser che ti riporta le clienti.</h1>
  <p class="sub">In più <b>PERSELOPE</b>, l’app che ogni mattina ti dice chi richiamare e quanto vale ogni telefonata. E se vuoi, <b>dieci anni di marketing per i centri estetici</b>.</p>
  <p class="sub" style="color:#9CCBE8;margin-top:14px">Chiedi agli altri se te la danno.</p>${pie(3, a4)}</div>`,
  // 4 · tre domande
  (H, a4) => `<div class="giu alto" style="padding-top:60px"><div style="width:250px">${LOGO_NEG}</div>
  <p style="font-size:26px;letter-spacing:.2em;font-weight:700;color:#9CCBE8;text-transform:uppercase;margin-top:${a4 ? 120 : 60}px">Prima di noleggiare un laser</p>
  <h1 style="margin-top:16px;${a4 ? 'font-size:104px' : ''}">Fai queste tre domande.</h1>
  <div class="dom${a4 ? ' grande' : ''}">
    <div class="n">1</div><p class="q">Devo firmare, e versare un anticipo?</p><p class="a">Da noi: no. E ti fermi quando vuoi.</p>
    <div class="n">2</div><p class="q">Se ho un dubbio con la cliente davanti, chi mi risponde?</p><p class="a">La tua tutor Demetra, su WhatsApp.</p>
    <div class="n">3</div><p class="q">Mi dai qualcosa che mi riporta le clienti?</p><p class="a">Sì: l’app che ti dice chi richiamare, in più.</p>
  </div>
  <div style="flex:1"></div>${pie(4, a4)}</div>`
];

(async () => {
  const b = await chromium.launch({ executablePath: process.env.CHROMIUM || '/opt/pw-browsers/chromium' });
  const tmp = path.join(__dirname, '_tmp.html');
  for (let i = 0; i < locandine.length; i++) {
    for (const [H, a4, scala, nome] of [[1350, false, 1, 'social'], [Math.round(W * 297 / 210), true, 2480 / W, 'A4']]) {
      const p = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: scala });
      fs.writeFileSync(tmp, `<!doctype html><meta charset="utf-8"><style>${css(H)}</style><body>${locandine[i](H, a4)}</body>`);
      await p.goto('file://' + tmp, { waitUntil: 'load' });
      await p.evaluate(() => document.fonts.ready);
      await p.screenshot({ path: path.join(__dirname, `LOCANDINA-${i + 1}-${nome}.png`) });
      await p.close();
    }
  }
  fs.unlinkSync(tmp);
  await b.close();
})();
