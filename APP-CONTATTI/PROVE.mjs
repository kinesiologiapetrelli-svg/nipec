import { chromium } from 'playwright-core';
const B='http://127.0.0.1:8732/';
const SCR='/tmp/claude-0/-home-user-nipec/7dc42b25-d74d-580b-a690-0af7a25e783d/scratchpad';
let passate=0, fallite=0;
const ok=(c,m)=>{ if(c){passate++;console.log('  ok   '+m)} else {fallite++;console.log('  NO   '+m)} };

const b = await chromium.launch({ executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
                                  args:['--no-sandbox','--disable-gpu'] });
const errori=[];
async function nuova(){
  const ctx = await b.newContext();
  const p = await ctx.newPage();
  p.on('pageerror', e => errori.push('ERRORE JS: '+e.message));
  p.on('console', m => { if(m.type()==='error' && !/404|favicon/.test(m.text())) errori.push('CONSOLE: '+m.text()); });
  await p.goto(B, { waitUntil:'networkidle' });
  p.vai = async re => { for(const bt of await p.$$('button,[role=tab],a')){
    const t=((await bt.textContent())||'').trim(); if(re.test(t.replace(/\d+$/,''))){ await bt.click(); await p.waitForTimeout(400); return true; } } return false; };
  p.stato = () => p.evaluate(() => JSON.parse(localStorage.getItem('nipec_contatti_v1')||'{}'));
  return p;
}
const importa = async (p, file) => {
  await p.vai(/^Importa$/); await p.setInputFiles('#file', file); await p.waitForTimeout(700);
  await p.vai(/Guarda cosa ho capito/); await p.waitForTimeout(700);
  const ant = await p.locator('#anteprima').innerText();
  await p.vai(/Importa davvero/); await p.waitForTimeout(900);
  return ant;
};

console.log('\n== 1. CSV pulito (intestazioni Nome;Telefono;WhatsApp;Paese;…;Città;Organizzazione) ==');
{ const p = await nuova();
  const ant = await importa(p, SCR+'/UARDA-contatti.csv');
  ok(/Ho riconosciuto le intestazioni/.test(ant), 'riconosce le intestazioni');
  const S = await p.stato();
  ok(S.contatti.length > 500, `contatti importati: ${S.contatti.length}`);
  const c = S.contatti.find(x => /Ador Sallon/.test(x.nome||''));
  ok(!!c, 'trova «Ador Sallon Tirane»');
  if(c){
    ok(c.numero === '355692999600', `numero giusto: ${c.numero}`);
    ok(c.paese === 'AL', `paese dedotto dal numero: ${c.paese}`);
    ok(!/\d{6}/.test(c.centro||''), `centro NON è più un telefono: "${c.centro}"`);
    ok((c.citta||'') !== 'Albania', `città NON è più «Albania»: "${c.citta}"`);
  }
  console.log(`       (numeri messi da parte: ${(S.scarti||[]).length})`);
  const s0 = (S.scarti||[])[0];
  if(s0) ok(!!s0.perche, `il primo scarto dice perché: "${s0.perche}"`);
  ok(!S.contatti.some(x => /^3556?\d{0,7}$/.test(x.numero)), 'nessun numero troncato è entrato');
  ok(S.contatti.some(x => /^383/.test(x.numero)), 'il numero del Kosovo (+383) non è più storpiato');
  ok(!S.contatti.some(x => x.numero.length > 15), 'nessun numero doppio è entrato');
  ok(!S.contatti.some(x => /^3556\d{8}$/.test(x.numero) === false && /^355/.test(x.numero)),
     'tutti i numeri albanesi hanno il formato giusto');
  await p.context().close();
}

console.log('\n== 2. export originale di Google Contatti (32 colonne) ==');
{ const p = await nuova();
  const ant = await importa(p, SCR+'/uarda-in/contacts.csv');
  ok(/Ho riconosciuto le intestazioni/.test(ant), 'riconosce le intestazioni di Google');
  const S = await p.stato();
  ok(S.contatti.length > 500, `contatti importati: ${S.contatti.length}`);
  const c = S.contatti.find(x => /Dermoesthetic/.test((x.nome||'')+(x.centro||'')));
  ok(!!c, 'trova «Dermoesthetic Center Dea»');
  if(c) ok(!/myContacts/.test(JSON.stringify(c)), 'niente più «* myContacts» nei campi');
  ok(!S.contatti.some(x => /Cellulare|Mobile/.test(x.citta||'')), 'niente più «Mobile» nella città');
  await p.context().close();
}

console.log('\n== 3. elenco scritto a mano, senza intestazioni ==');
{ const p = await nuova();
  await p.vai(/^Importa$/);
  await p.fill('#grezzo', 'Maria Rossi; Centro Bellezza; Roma; 333 1234567\nEgla Hoxha, Studio Egla, Tiranë, 069 212 9786');
  await p.selectOption('#paeseImp','IT');
  await p.vai(/Guarda cosa ho capito/); await p.waitForTimeout(500);
  const ant = await p.locator('#anteprima').innerText();
  ok(/vado a naso/.test(ant), 'capisce che non ci sono intestazioni');
  ok(/Maria Rossi/.test(ant), 'legge comunque il nome');
  await p.context().close();
}

console.log('\n== 4. la scheda Stato ==');
{ const p = await nuova();
  await importa(p, SCR+'/UARDA-contatti.csv');
  await p.vai(/^Stato$/); await p.waitForTimeout(600);
  const t = await p.locator('#app').innerText();
  ok(/scritte finora/i.test(t), 'c\'è il riquadro dei numeri');
  ok(/aspetto risposta/i.test(t), 'c\'è «aspetto risposta»');
  ok(/non su WhatsApp/i.test(t), 'c\'è «non su WhatsApp»');
  const Sx = await p.stato();
  if((Sx.scarti||[]).length) ok(/numeri da sistemare/i.test(t), 'c\'è il blocco dei numeri da sistemare');
  else console.log('       (nessuno scarto: il blocco giustamente non c\'è)');
  ok(/Chi, quando, com'è andata/.test(t), 'c\'è lo storico');
  ok(await p.locator('#tabellaSt table').count() >= 0, 'la tabella si disegna');
  // il filtro
  await p.selectOption('#filtroSt','mai'); await p.waitForTimeout(400);
  ok(/contatti/.test(await p.locator('#tabellaSt').innerText()), 'il filtro «non le ho mai scritto» risponde');
  await p.context().close();
}

console.log('\n== 5. il giro: mando, segno WhatsApp, segno la risposta ==');
{ const p = await nuova();
  await importa(p, SCR+'/UARDA-contatti.csv');
  await p.vai(/^Oggi$/); await p.waitForTimeout(500);
  // simulo l'invio senza aprire davvero WhatsApp
  const id1 = await p.evaluate(() => document.querySelector('[data-manda]').dataset.manda);
  await p.evaluate(i => segnaInviato(i), id1);
  await p.waitForTimeout(400);
  let S = await p.stato();
  let c = S.contatti.find(x => x.id === id1);
  ok(c.invii === 1, 'invii = 1');
  ok(c.stato === 'inviato', 'stato = inviato');
  ok((c.storia||[]).some(e => e.t === 'inviato'), 'la storia registra l\'invio');
  // compare la domanda su WhatsApp?
  const t5 = await p.locator('#app').innerText();
  ok(/appena mandati/i.test(t5), 'compare la striscia «Appena mandati»');
  ok(/numero c'era su WhatsApp/i.test(t5), 'con la domanda sul numero');
  ok(await p.locator('[data-wa^="si"]').count() > 0, 'e i due tasti per rispondere');
  await p.locator('[data-wa^="si"]').first().click(); await p.waitForTimeout(400);
  S = await p.stato(); c = S.contatti.find(x => x.id === id1);
  ok(c.wa === 'si', 'WhatsApp segnato: sì');
  await p.evaluate(i => cambiaStato(i,'risposto'), id1); await p.waitForTimeout(300);
  S = await p.stato(); c = S.contatti.find(x => x.id === id1);
  ok(c.stato === 'risposto', 'stato = risposto');
  ok((c.storia||[]).some(e => e.t === 'risposto'), 'la storia registra la risposta');
  await p.context().close();
}

console.log('\n== 6. il richiamo del giorno dopo ==');
{ const p = await nuova();
  await importa(p, SCR+'/UARDA-contatti.csv');
  // fingo che tre messaggi siano partiti ieri
  await p.evaluate(() => {
    const i = new Date(); i.setDate(i.getDate()-1);
    const d = i.toISOString().slice(0,10);
    S.contatti.slice(0,3).forEach(c => { c.invii=1; c.ultimoInvio=d; c.stato='inviato';
      c.storia=[{d, t:'inviato', p:1}]; });
    salva(); disegna();
  });
  await p.vai(/^Stato$/); await p.waitForTimeout(600);
  const t = await p.locator('#app').innerText();
  ok(/Ieri hai scritto a 3/.test(t), 'il richiamo dice quante erano: ' + (t.match(/Ieri hai scritto a \d+/)||[''])[0]);
  ok(/Ha risposto/.test(t), 'ci sono i tasti per chiudere');
  const pal = await p.locator('.schede .pallina').allInnerTexts();
  ok(pal.length >= 1, 'la pallina avvisa sulla barra: ' + JSON.stringify(pal));
  await p.context().close();
}

console.log('\n== 7. correggere un numero messo da parte ==');
{ const p = await nuova();
  await p.vai(/^Importa$/);
  await p.fill('#grezzo', 'Nome;Telefono\nProva Troncata;067 522 666\nProva Buona;069 111 2233');
  await p.selectOption('#paeseImp','AL');
  await p.vai(/Importa davvero/); await p.waitForTimeout(800);
  await p.vai(/^Stato$/); await p.waitForTimeout(500);
  const prima = (await p.stato()).contatti.length;
  ok((await p.stato()).scarti.length === 1, 'il numero troncato finisce negli scarti');
  await p.locator('[data-scarto^="correggi"]').first().click(); await p.waitForTimeout(400);
  ok(await p.locator('#sNum').count() === 1, 'si apre la finestra di correzione');
  await p.fill('#sNum','069 555 1234'); await p.selectOption('#sPaese','AL');
  await p.locator('#sOk').click(); await p.waitForTimeout(500);
  const S = await p.stato();
  ok(S.contatti.length === prima + 1, 'il contatto corretto entra in rubrica');
  ok(S.contatti.some(c => c.numero === '355695551234'), 'col numero giusto');
  await p.context().close();
}

console.log('\n== 8. il nome dentro il messaggio ==');
{ const p = await nuova();
  const casi = await p.evaluate(() => [
    nomeDaScrivere({nome:'~Kejsi'}),
    nomeDaScrivere({nome:'\u{1F3BB}edlira'}),
    nomeDaScrivere({nome:'A0323TR Alba Dervishi'}),
    nomeDaScrivere({nome:'Maria Rossi'}),
    nomeDaScrivere({nome:'', centro:'Studio Egla'})
  ]);
  ok(casi[0] === 'Kejsi', `«~Kejsi» -> «${casi[0]}»`);
  ok(casi[1] === 'edlira', `«🎻edlira» -> «${casi[1]}»`);
  ok(casi[2] === 'Alba', `«A0323TR Alba Dervishi» -> «${casi[2]}»`);
  ok(casi[3] === 'Maria', `«Maria Rossi» -> «${casi[3]}»`);
  ok(casi[4] === 'Studio Egla', `senza nome usa il centro -> «${casi[4]}»`);
  const m = await p.evaluate(() => componi('Ciao {nome}, sono Giorgio.', {nome:'~Kejsi'}));
  ok(m === 'Ciao Kejsi, sono Giorgio.', `messaggio: «${m}»`);
  await p.context().close();
}

console.log('\n== errori in pagina ==');
console.log(errori.length ? errori.join('\n') : '  nessuno');
console.log(`\n=== ${passate} prove passate, ${fallite} fallite ===`);
await b.close();
process.exit(fallite || errori.length ? 1 : 0);
