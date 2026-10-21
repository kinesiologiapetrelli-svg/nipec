/* La prova che conta: parto dai dati VERI di Giorgio, come stanno adesso nel
   suo telefono, e verifico che l'aggiornamento non porti via niente. */
import { chromium } from 'playwright-core';
import fs from 'node:fs';
const SUOI = JSON.parse(fs.readFileSync('/tmp/claude-0/-home-user-nipec/7dc42b25-d74d-580b-a690-0af7a25e783d/scratchpad/suoi/copia.json','utf8'));
let ok_ = 0, no_ = 0;
const ok = (c,m)=>{ if(c){ok_++;console.log('  ok   '+m)} else {no_++;console.log('  NO   '+m)} };

const b = await chromium.launch({ executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args:['--no-sandbox','--disable-gpu'] });
const ctx = await b.newContext(); const p = await ctx.newPage();
const err=[]; p.on('pageerror', e=>err.push(e.message));
p.on('console', m=>{ if(m.type()==='error' && !/404|favicon/.test(m.text())) err.push(m.text()); });

await p.goto('http://127.0.0.1:8732/', { waitUntil:'networkidle' });
// metto nel browser i suoi dati esattamente come stanno nel suo telefono
await p.evaluate(d => { localStorage.clear(); localStorage.setItem('nipec_contatti_v1', JSON.stringify(d)); }, SUOI);
await p.reload({ waitUntil:'networkidle' });
await p.waitForTimeout(1200);

const S = await p.evaluate(()=>JSON.parse(JSON.stringify(S)));
console.log('\n--- la rubrica dopo l\'aggiornamento ---');
ok(S.contatti.length === 522, `522 contatti, ce ne sono ${S.contatti.length}`);
ok(S.contatti.filter(c=>c.stato==='inviato').length === 25, `i 25 gia mandati sono ancora "inviato" (${S.contatti.filter(c=>c.stato==='inviato').length})`);
ok(S.contatti.filter(c=>c.stato==='non interessato').length === 2, 'i 2 che hanno detto no restano fuori dal giro');
ok(S.contatti.filter(c=>c.wa==='si').length === 27, `i 27 segnati su WhatsApp restano (${S.contatti.filter(c=>c.wa==='si').length})`);
ok(S.registro['2026-10-21'] === 25, 'il registro di oggi dice ancora 25: non ti fa ricominciare la quota');
ok(S.cfg.alGiorno === 25 && S.cfg.attesa1 === 5, 'le tue impostazioni sono intatte');
const uno = S.contatti.find(c=>c.nome==='AleMirandaeste');
ok(uno && uno.numero==='393922316135' && uno.centro==='ALMIRÒ MEDICAL BEAUTY', 'un contatto a campione e identico');
ok(uno && uno.storia.length===2, 'con la sua storia (invio + whatsapp)');
ok(S.contatti.every(c=>c.numero && c.nome!==undefined), 'nessun contatto si e rotto');
ok(!S._errore && !S._recuperati, 'nessun avviso di problemi');

console.log('\n--- cosa si aggiunge ---');
ok(S.modelli.some(m=>m.id==='it4'), 'arriva il quarto messaggio italiano');
ok(S.modelli.some(m=>m.id==='al4'), 'e quello albanese');
const it1 = S.modelli.find(m=>m.id==='it1');
ok(/ampliato il modo di dare i Dispositivi/.test(it1.testo),
   'IL TESTO CHE HAI SCRITTO TU NON VIENE TOCCATO (e giusto cosi)');
ok(!/\{nome\}/.test(it1.testo),
   'ma attenzione: il tuo testo non ha {nome} — i messaggi partono senza il nome');
const copia = await p.evaluate(()=>localStorage.getItem('nipec_contatti_prima_aggiornamento'));
const vecchio = JSON.parse(copia);
ok(vecchio.contatti.length === 522, 'ed e stata messa da parte la copia dei 522 di prima');

console.log('\n--- cosa vedi aprendo ---');
await p.evaluate(()=>{ S.cfg.scheda='oggi'; disegna(); }); await p.waitForTimeout(600);
const oggi = await p.locator('#app').innerText();
ok(/25\s*\/\s*25|25\/25/.test(oggi.replace(/\s+/g,'')) || /25/.test(oggi), 'la scheda Oggi sa che oggi hai gia finito');
await p.evaluate(()=>{ S.cfg.scheda='stato'; disegna(); }); await p.waitForTimeout(600);
const stato = await p.locator('#app').innerText();
ok(/25/.test(stato) && /scritte finora/i.test(stato), 'la scheda Stato dice 25 scritte');
ok(!/da raddrizzare/i.test(stato), 'nessun prefisso da raddrizzare: la tua lista era gia pulita');
ok(!/numeri da sistemare/i.test(stato), 'e nessun numero da sistemare');
const q = await p.evaluate(()=>codaDaSeguire().length);
ok(q === 0, 'nessuno in coda per le informazioni: nessuno ha ancora detto si');

console.log('\n--- errori ---');
console.log(err.length ? err.join('\n') : '  nessuno');
console.log(`\n=== ${ok_} verifiche passate, ${no_} fallite ===`);
await p.screenshot({ path:'suoi-stato.png', fullPage:false });
await b.close();
process.exit(no_ || err.length ? 1 : 0);
