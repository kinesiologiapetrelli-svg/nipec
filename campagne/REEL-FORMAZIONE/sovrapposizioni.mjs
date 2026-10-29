// Le scritte, il bollino dei due logo e la scheda finale del reel «formazione», come PNG 1080 x 1920.
// Si lancia da fai-reel.py:  node sovrapposizioni.mjs <cartella-di-uscita>
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const QUI = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(QUI, '../..');
const OUT = process.argv[2];
fs.mkdirSync(OUT, { recursive: true });

const b64 = (p) => fs.readFileSync(p).toString('base64');
const ARCHIVO = b64(path.join(REPO, 'SITO/pubblica/caratteri/archivo.woff2'));
const CINZEL = b64(path.join(REPO, 'LANDING-DEMETRA/caratteri/cinzel.woff2'));
const svg = (n) => fs.readFileSync(path.join(REPO, 'MARCHIO', n), 'utf8').replace(/<title>.*?<\/title>/s, '');
const LOGO_NEG = svg('nipec-logo-orizzontale-negativo.svg').replace('<svg ', '<svg style="width:100%;display:block" ');
const EMBL_NEG = svg('nipec-emblema-negativo.svg').replace(/^<svg[^>]*>|<\/svg>\s*$/g, '');
const DEMETRA_EMBL = 'data:image/png;base64,' + b64(path.join(REPO, 'LANDING-DEMETRA/logo-demetra-emblema.png'));

const BASE = `
@font-face{font-family:"Archivo";src:url(data:font/woff2;base64,${ARCHIVO}) format("woff2");font-weight:100 900}
@font-face{font-family:"Cinzel";src:url(data:font/woff2;base64,${CINZEL}) format("woff2");font-weight:400 900}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;background:transparent;overflow:hidden}
body{position:relative;font-family:"Archivo","Helvetica Neue",Arial,sans-serif}
`;

// Le scritte: fascia blu profondo, bianco, Archivo grassetto. Nella fascia sicura (niente nei primi 250 px e negli ultimi 340).
const TESTI = {
  t1: { y: 1010, size: 70, righe: ['Chi ti insegna a usare', 'il dispositivo…'] },
  t2: { y: 1010, size: 70, righe: ['…dopo che l’hai preso?'] },
  t3: { y: 1330, size: 56, righe: ['Noi. In cabina,', 'con il dispositivo in mano.'] },
  t4: { y: 1330, size: 56, righe: ['E davanti a una telecamera,', 'in diretta.'] },
  t5: { y: 1330, size: 56, righe: ['Workshop DEMETRA,', '26 ottobre.'] },
  t6: { y: 1330, size: 56, righe: ['Gesto per gesto.'] },
  t7: { y: 1330, size: 56, righe: ['Formazione a tappe.', 'Esame finale. Certificato.'] },
  t8: { y: 1330, size: 56, righe: ['Non vendiamo dispositivi.', 'Costruiamo sistemi di lavoro.'] },
};

const browser = await chromium.launch({ args: ['--no-sandbox'] });
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
const salva = async (html, nome, trasparente = true) => {
  await page.setContent(html, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: path.join(OUT, nome + '.png'), omitBackground: trasparente });
};

for (const [nome, t] of Object.entries(TESTI)) {
  await salva(`<style>${BASE}
  .p{position:absolute;left:0;right:0;top:${t.y}px;transform:translateY(-50%);text-align:center}
  .p span{display:inline-block;background:rgba(18,58,99,.95);color:#fff;font-weight:700;font-size:${t.size}px;line-height:1.2;
    letter-spacing:-.01em;padding:${Math.round(t.size * .46)}px ${Math.round(t.size * .66)}px;border-radius:${Math.round(t.size * .5)}px;max-width:960px}
  </style><div class="p"><span>${t.righe.join('<br>')}</span></div>`, nome);
}

// Il bollino dei due logo: NIPEC e DEMETRA, su blu profondo, in alto a sinistra sotto la zona coperta da Instagram.
await salva(`<style>${BASE}
 .b{position:absolute;left:44px;top:276px;display:flex;align-items:center;gap:26px;background:rgba(18,58,99,.95);border-radius:30px;padding:22px 32px 22px 30px}
 .b .n{width:250px}
 .b i{display:block;width:3px;height:70px;background:rgba(255,255,255,.28)}
 .b img{width:96px;height:96px;display:block}
</style><div class="b"><div class="n">${LOGO_NEG}</div><i></i><img src="${DEMETRA_EMBL}"></div>`, 'bollino');

// La scheda finale: blu profondo, i due marchi, l'invito, il contatto.
await salva(`<style>${BASE}
 html,body{background:#123A63}
 .em{position:absolute;right:-470px;bottom:-430px;width:1100px;height:1100px;opacity:.12}
 .c{position:absolute;left:0;right:0;top:250px;bottom:340px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;color:#fff}
 .nipec{width:620px}
 .x{margin:46px 0 30px;font-weight:600;font-size:46px;color:#5AA6D6;letter-spacing:.2em}
 .dem img{width:230px;height:230px;display:block;margin:0 auto}
 .dem b{display:block;margin-top:14px;font-family:"Cinzel",serif;font-weight:500;font-size:84px;letter-spacing:.22em;color:#D9B25F;padding-left:.22em}
 .dem s{display:block;text-decoration:none;margin-top:6px;font-weight:500;font-size:30px;letter-spacing:.34em;color:#C8D6E4;padding-left:.34em}
 .f{margin:84px 0 0;width:140px;height:5px;background:#5AA6D6;border-radius:3px}
 .inv{margin-top:70px;font-weight:700;font-size:62px;line-height:1.15;letter-spacing:-.01em}
 .con{margin-top:34px;font-weight:600;font-size:38px;letter-spacing:.04em;color:#9CCBE8;line-height:1.5}
</style>
<svg class="em" viewBox="0 0 100 100">${EMBL_NEG}</svg>
<div class="c">
 <div class="nipec">${LOGO_NEG}</div>
 <div class="x">×</div>
 <div class="dem"><img src="${DEMETRA_EMBL}"><b>DEMETRA</b><s>SYNERGIA</s></div>
 <div class="f"></div>
 <div class="inv">Vuoi vederlo dal vivo?<br>Scrivici.</div>
 <div class="con">WhatsApp 351 846 6025<br>www.nipecestetica.eu</div>
</div>`, 'fine', false);

await browser.close();
console.log('sovrapposizioni:', fs.readdirSync(OUT).filter((f) => f.endsWith('.png')).sort().join(' '));
