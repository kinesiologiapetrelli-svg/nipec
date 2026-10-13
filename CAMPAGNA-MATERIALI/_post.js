// Genera il carosello del post sul noleggio: node _post.js (serve playwright-core).
// Sette slide 1080×1350 (il formato 4:5 di Instagram), più la didascalia in POST-NOLEGGIO-didascalia.txt.
const { chromium } = require('playwright-core');
const path = require('path');
const fs = require('fs');
const R = path.resolve(__dirname, '..');
const F = 'file://' + R + '/SITO/assets/fonts/';
const LOGO = fs.readFileSync(R + '/MARCHIO/nipec-logo-orizzontale-negativo.svg', 'utf8');
const LOGO_POS = fs.readFileSync(R + '/MARCHIO/nipec-logo-orizzontale.svg', 'utf8');
const ARES = 'file://' + R + '/SITO/assets/img/ares.webp';
const APP = 'file://' + __dirname + '/_app-oggi.png';
const W = 1080, H = 1350, TOT = 7;

const pagina = (n, corpo, chiaro) => `<!doctype html><meta charset="utf-8"><style>
@font-face{font-family:A;font-weight:400;src:url(${F}archivo-latin-400-normal.woff2)}
@font-face{font-family:A;font-weight:600;src:url(${F}archivo-latin-600-normal.woff2)}
@font-face{font-family:A;font-weight:700;src:url(${F}archivo-latin-700-normal.woff2)}
*{box-sizing:border-box;margin:0;padding:0}
body{width:${W}px;height:${H}px;overflow:hidden;font-family:A,sans-serif;position:relative;
  background:${chiaro ? '#F1F5F9' : 'radial-gradient(circle at 80% 30%, #1C6EA4 0, #123A63 58%)'};color:${chiaro ? '#123A63' : '#fff'}}
.logo{position:absolute;left:80px;top:72px;width:260px}.logo svg{width:100%;height:auto;display:block}
.num{position:absolute;right:80px;top:84px;font-size:28px;font-weight:600;letter-spacing:.1em;color:${chiaro ? '#5A6B80' : '#9CCBE8'}}
.occ{font-size:30px;letter-spacing:.2em;text-transform:uppercase;font-weight:600;color:${chiaro ? '#1C6EA4' : '#9CCBE8'}}
h1{font-weight:700;letter-spacing:-.02em;line-height:1.02}
.sub{font-size:44px;line-height:1.35;color:${chiaro ? '#3B4C5E' : '#D6E4F0'}}
.sub b{color:${chiaro ? '#123A63' : '#fff'}}
.box{position:absolute;left:80px;right:80px}
.avanti{position:absolute;right:80px;bottom:72px;font-size:30px;font-weight:600;color:${chiaro ? '#1C6EA4' : '#9CCBE8'}}
.pie{position:absolute;left:80px;bottom:72px;font-size:28px;color:${chiaro ? '#5A6B80' : '#9CCBE8'}}
.tre{display:flex;flex-direction:column;gap:22px;margin-top:56px}
.tre div{font-size:58px;font-weight:700;display:flex;align-items:center;gap:26px}
.tre i{font-style:normal;width:72px;height:72px;border-radius:50%;background:#fff;color:#123A63;display:flex;align-items:center;justify-content:center;font-size:40px;flex:none}
.punti{list-style:none;margin-top:48px;display:flex;flex-direction:column;gap:30px}
.punti li{font-size:42px;line-height:1.3;padding-left:58px;position:relative}
.punti li::before{content:"";position:absolute;left:0;top:14px;width:30px;height:30px;border-radius:50%;background:${chiaro ? '#1C6EA4' : '#5AA6D6'}}
</style><body>
<div class="logo">${chiaro ? LOGO_POS : LOGO}</div><div class="num">${n}/${TOT}</div>
${corpo}
${n < TOT ? '<div class="avanti">scorri →</div>' : ''}
</body>`;

const slide = [
  // 1 · copertina
  () => pagina(1, `
<div class="box" style="top:250px">
  <p class="occ">Laser a noleggio</p>
  <h1 style="font-size:104px;margin-top:28px">Un laser con intelligenza artificiale a <span style="color:#5AA6D6;white-space:nowrap">500 € al mese.</span></h1>
  <div class="tre">
    <div><i>✓</i>Senza vincoli</div>
    <div><i>✓</i>Senza firme</div>
    <div><i>✓</i>Senza anticipi</div>
  </div>
</div>
<p class="pie">+ IVA</p>`),
  // 2 · ti fermi quando vuoi
  () => pagina(2, `
<div class="box" style="top:330px">
  <p class="occ">La regola è una sola</p>
  <h1 style="font-size:150px;margin-top:30px">Ti fermi quando vuoi.</h1>
  <p class="sub" style="margin-top:56px">Niente anni da pagare se la stagione va male. Niente anticipo per cominciare. <b>Se non ti serve più, la macchina torna da noi.</b></p>
</div>`),
  // 3 · la macchina
  () => pagina(3, `
<div class="box" style="top:220px">
  <p class="occ">La tecnologia</p>
  <h1 style="font-size:84px;margin-top:24px">ARES 2026 · con intelligenza artificiale</h1>
</div>
<div style="position:absolute;left:80px;top:520px;width:440px;height:520px;background:#fff;border-radius:40px;overflow:hidden;display:flex;align-items:center;justify-content:center;box-shadow:0 30px 70px rgba(0,0,0,.18)"><img src="${ARES}" style="height:95%"></div>
<ul class="punti" style="position:absolute;left:570px;right:70px;top:500px">
  <li>La telecamera legge pelle e pelo e ti propone i parametri</li>
  <li>Decidi sempre tu</li>
  <li>Diodo 808 nm, 1500 W, testina in titanio</li>
  <li>CE italiana · MDR</li>
</ul>`, true),
  // 4 · sistema Demetra
  () => pagina(4, `
<div class="box" style="top:250px">
  <p class="occ">Il sistema Demetra</p>
  <h1 style="font-size:112px;margin-top:28px">Non resti mai da sola.</h1>
  <ul class="punti">
    <li><b>Una tutor</b> che ti segue, sempre in contatto con te</li>
    <li><b>Un canale WhatsApp tutto tuo</b>: scrivi quando hai un dubbio, in cabina, con la cliente davanti</li>
    <li><b>Formazione costante</b>, non una giornata e poi arrangiati</li>
  </ul>
</div>`),
  // 5 · marketing
  () => pagina(5, `
<div class="box" style="top:280px">
  <p class="occ">Se vuoi · opzionale</p>
  <h1 style="font-size:112px;margin-top:28px">E se vuoi, ti aiutiamo anche a riempire l’agenda.</h1>
  <p class="sub" style="margin-top:56px">Un sistema di marketing costruito in <b>dieci anni di lavoro con i centri estetici</b>. Non te lo raccontiamo: ti facciamo vedere i risultati.</p>
</div>`, true),
  // 6 · in più: PERSELOPE
  () => pagina(6, `
<div class="box" style="top:200px">
  <p class="occ">E in più</p>
  <h1 style="font-size:88px;margin-top:24px">L’app che ogni mattina ti dice chi richiamare.</h1>
</div>
<div style="position:absolute;left:80px;top:610px;width:470px;font-size:40px;line-height:1.35;color:#D6E4F0">
  <p>Chi è in ritardo, chi ha finito il ciclo, chi non vedi da sei mesi. <b style="color:#fff">E quanto vale ogni telefonata.</b></p>
  <p style="margin-top:36px;font-weight:700;color:#fff">PERSELOPE LASER.<br>Inclusa nel noleggio.</p>
  <p style="margin-top:36px;font-size:34px;color:#9CCBE8">Chiedi agli altri se te la danno.</p>
</div>
<div style="position:absolute;right:80px;top:520px;width:400px;padding:14px;border-radius:58px;background:#0B2440;box-shadow:0 40px 80px rgba(0,0,0,.4)">
  <div style="border-radius:46px;overflow:hidden;height:700px"><img src="${APP}" style="width:100%;display:block"></div>
</div>`),
  // 7 · chiusura
  () => pagina(7, `
<div class="box" style="top:260px;text-align:left">
  <p class="occ">Laser IA a noleggio</p>
  <h1 style="font-size:170px;margin-top:24px">500 €<span style="font-size:70px;color:#9CCBE8"> al mese + IVA</span></h1>
  <p class="sub" style="margin-top:40px">Senza vincoli · senza firme · senza anticipi.<br>Tutor Demetra su WhatsApp. L’app in più.</p>
  <div style="margin-top:80px;background:#fff;color:#123A63;border-radius:36px;padding:44px 52px">
    <p style="font-size:40px;font-weight:600">Scrivi <b style="font-size:52px">NOLEGGIO</b> su WhatsApp</p>
    <p style="font-size:64px;font-weight:700;margin-top:10px;letter-spacing:.01em">351 846 6025</p>
  </div>
</div>`)
];

(async () => {
  const b = await chromium.launch({ executablePath: process.env.CHROMIUM || '/opt/pw-browsers/chromium' });
  const tmp = path.join(__dirname, '_tmp.html');
  for (let i = 0; i < slide.length; i++) {
    const p = await b.newPage({ viewport: { width: W, height: H } });
    fs.writeFileSync(tmp, slide[i]());
    await p.goto('file://' + tmp, { waitUntil: 'load' });
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: path.join(__dirname, `POST-NOLEGGIO-${i + 1}.png`) });
    await p.close();
  }
  fs.unlinkSync(tmp);
  await b.close();
})();
