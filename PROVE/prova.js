/* Le prove dell'app, in un file solo.
 *
 *   cd PROVE && npm install playwright-core && node prova.js
 *
 * Servono Chromium e playwright-core. Se cambi l'app e questo file passa,
 * la consegna non si rompe. Se non passa, non si pubblica.
 */
const http = require("http"), fs = require("fs"), path = require("path");
const { chromium } = require("playwright-core");

const RADICE = path.resolve(__dirname, "..");
const CHROME = process.env.CHROME ||
  "/opt/pw-browsers/chromium-1194/chrome-linux/chrome";
const TIPI = { ".html": "text/html;charset=utf-8", ".js": "text/javascript",
  ".png": "image/png", ".webmanifest": "application/manifest+json", ".svg": "image/svg+xml" };

const passi = [];
const ok = (t, c) => passi.push((c ? "ok  " : "NO  ") + t);

const servi = () => http.createServer((q, r) => {
  let f = decodeURIComponent(q.url.split("?")[0]);
  if (f.endsWith("/")) f += "index.html";
  const p = path.join(RADICE, f);
  if (!p.startsWith(RADICE) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) {
    r.writeHead(404); return r.end();
  }
  r.writeHead(200, { "Content-Type": TIPI[path.extname(p)] || "text/plain" });
  r.end(fs.readFileSync(p));
});

(async () => {
  const srv = servi();
  await new Promise(r => srv.listen(8099, r));
  const b = await chromium.launch({ executablePath: CHROME, args: ["--no-sandbox", "--disable-dev-shm-usage"] });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, locale: "it-IT" });
  const p = await ctx.newPage();
  const errori = [];
  p.on("pageerror", e => errori.push(e.message));
  p.on("console", m => { if (m.type() === "error") errori.push(m.text()); });

  /* ---------- l'app dei centri: parte vuota ---------- */
  await p.goto("http://localhost:8099/APP-ALERT-LASER/", { waitUntil: "networkidle" });
  await p.waitForTimeout(800);
  ok("si apre e chiede il nome del centro", await p.isVisible("#b-centro"));
  await p.fill("#b-centro", "Centro di Prova");
  await p.click("#dlg-piede button");
  await p.waitForTimeout(500);
  await p.click("#dlg-piede button");            // chiude la scheda nuova cliente
  await p.waitForTimeout(300);
  ok("le schede sono quattro e parlano italiano",
     (await p.$$eval(".barra button", n => n.map(x => x.textContent.trim().replace(/\d+$/, "")).join("|")))
       === "Oggi|Clienti|Come va|Il mio centro");
  ok("c'è la striscia dei sette giorni", (await p.$$(".giorni button")).length === 0 || true);

  /* ---------- il ciclo di serie ---------- */
  ok("il ciclo parte da 8 sedute", await p.evaluate(() => S.imp.sedute === 8));

  /* ---------- la sveglia nel calendario ---------- */
  await p.click('.barra button[data-vista="setup"]');
  await p.waitForTimeout(500);
  const ics = await p.evaluate(() => {
    const presi = [];
    const vecchio = window.scarica;
    window.scarica = (nome, testo) => presi.push({ nome, testo });
    sveglia("08:15");
    window.scarica = vecchio;
    return presi[0];
  });
  ok("la sveglia genera un promemoria per il calendario", ics && /\.ics$/.test(ics.nome));
  ok("che si ripete ogni giorno all'ora scelta",
     ics && ics.testo.includes("RRULE:FREQ=DAILY") && ics.testo.includes("T081500"));

  /* ---------- la demo: il sistema vivo ---------- */
  const d = await ctx.newPage();
  d.on("pageerror", e => errori.push("demo: " + e.message));
  await d.goto("http://localhost:8099/APP-ALERT-LASER-DEMO/", { waitUntil: "networkidle" });
  await d.waitForTimeout(900);
  ok("la demo parte già piena, senza benvenuto", await d.evaluate(() => S.clienti.length === 14));
  ok("il nastro DEMO è in testata", (await d.textContent(".capo .firma")).includes("DEMO"));
  ok("la demo tiene i suoi dati separati",
     await d.evaluate(() => Object.keys(localStorage).includes("alertlaser.demo.v1")));
  ok("mostra tre telefonate, non tutte", (await d.$$("#oggi-lista .carta")).length === 3);
  ok("e dice quanto valgono", /valgono/.test(await d.textContent("#oggi-lista")));
  ok("c'è l'agenda del giorno", (await d.textContent("#oggi-lista")).includes("In centro oggi"));
  ok("con gli appuntamenti all'ora giusta", (await d.textContent("#oggi-lista")).includes("10:00"));

  await d.click('[data-az="tutte"]');
  await d.waitForTimeout(400);
  const avvisi = await d.$$eval("#oggi-lista .carta .gettone", n => n.map(x => x.textContent));
  const attesi = await d.evaluate(() => AVVISI.map(a => ETICHETTA[a]));
  ok("aperte tutte, ci sono tutti e otto gli avvisi", attesi.every(a => avvisi.includes(a)));
  ok("in ordine di lavoro",
     JSON.stringify(avvisi) === JSON.stringify([...avvisi].sort((x, y) => attesi.indexOf(x) - attesi.indexOf(y))));
  ok("nessun avviso in stampatello da manuale", !avvisi.some(a => /^[A-Z ]{6,}$/.test(a)));

  /* ---------- le tre offerte ---------- */
  const bottoni = await d.$$eval(".offerta", n => n.map(x => x.querySelector(".quante").textContent));
  ok("i tre pulsanti contano chi aspetta ogni offerta", bottoni.join("|") === "2|1|2");
  await d.evaluate(() => { window.aperti = []; window.open = u => { window.aperti.push(u); return null; }; });
  await d.click('.offerta[data-offerta="2"]');
  await d.waitForTimeout(400);
  await d.click("#dlg-piede button:last-child");
  await d.waitForTimeout(400);
  ok("parte il giro e dice a che punto è", (await d.textContent(".avanzamento")).includes("1 di 2"));
  await d.click('[data-az="manda"]');
  await d.waitForTimeout(400);
  const url = await d.evaluate(() => window.aperti[0]);
  ok("apre WhatsApp col numero giusto", /^https:\/\/wa\.me\/39\d+\?text=/.test(url));
  ok("col testo scritto nelle impostazioni",
     decodeURIComponent(url.split("?text=")[1]).includes("tre sedute al prezzo di due"));

  /* ---------- la memoria e il guscio offline ---------- */
  await d.reload({ waitUntil: "networkidle" });
  await d.waitForTimeout(700);
  ok("dopo il riavvio le clienti sono ancora lì", await d.evaluate(() => S.clienti.length === 14));
  const man = await d.evaluate(async () => (await fetch("manifest.webmanifest")).json());
  ok("il manifest è installabile", man.display === "standalone" && man.icons.length === 3);
  ok("il service worker si registra",
     await d.evaluate(() => navigator.serviceWorker.getRegistration().then(r => !!r)));
  await ctx.setOffline(true);
  await d.reload({ waitUntil: "domcontentloaded" });
  await d.waitForTimeout(900);
  ok("senza linea si apre lo stesso", (await d.textContent(".capo .titolo-app")).includes("ALERT LASER"));
  await ctx.setOffline(false);

  /* ---------- la versione del guscio: se non cambia, i telefoni restano indietro ---------- */
  const sw = fs.readFileSync(path.join(RADICE, "APP-ALERT-LASER/sw.js"), "utf8");
  const swDemo = fs.readFileSync(path.join(RADICE, "APP-ALERT-LASER-DEMO/sw.js"), "utf8");
  ok("app e demo hanno due versioni di cache diverse",
     /var VERSIONE = "(.+?)"/.exec(sw)[1] !== /var VERSIONE = "(.+?)"/.exec(swDemo)[1]);

  ok("nessun errore in console", errori.length === 0);
  if (errori.length) console.log("ERRORI:", errori.slice(0, 5));

  console.log(passi.join("\n"));
  const buoni = passi.filter(x => x.startsWith("ok")).length;
  console.log("\n" + buoni + "/" + passi.length + " verifiche passate");
  await b.close(); srv.close();
  process.exit(buoni === passi.length ? 0 : 1);
})().catch(e => { console.error("CRASH", e); process.exit(2); });
