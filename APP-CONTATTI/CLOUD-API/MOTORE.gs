/**
 * NIPEC — il motore che manda da solo, via Cloud API di Meta.
 * Gira dentro Google Apps Script, attaccato a un foglio Google.
 * Non c'e' nessun server da pagare e nessuna macchina da tenere accesa.
 *
 * LE CHIAVI NON STANNO QUI DENTRO.
 * Si mettono una volta sola in Impostazioni progetto -> Proprieta' script:
 *     TOKEN        il token permanente di Meta
 *     NUMERO_ID    l'ID del numero (Phone Number ID), non il numero
 *     WABA_ID      l'ID dell'account WhatsApp Business
 *     VERIFICA     una parola a piacere, serve solo ad agganciare il webhook
 * Cosi' non finiscono nel codice, non finiscono su GitHub e si cambiano
 * senza toccare una riga.
 */

const API = 'https://graph.facebook.com/v21.0';
const P = () => PropertiesService.getScriptProperties();
const chiave = n => { const v = P().getProperty(n); if (!v) throw new Error('Manca la proprieta\' ' + n); return v; };

/* ---------- il foglio ---------- */
const COLONNE = ['numero','nome','centro','citta','paese','stato','invii','ultimoInvio','risposta','quando'];
function foglio(nome) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let f = ss.getSheetByName(nome);
  if (!f) { f = ss.insertSheet(nome); f.appendRow(COLONNE); f.setFrozenRows(1); }
  return f;
}
function contatti() {
  const f = foglio('Contatti'), v = f.getDataRange().getValues(), cap = v.shift();
  return v.map((r, i) => { const o = { _riga: i + 2 }; cap.forEach((c, j) => o[c] = r[j]); return o; });
}
function scrivi(riga, campo, valore) {
  const f = foglio('Contatti'), cap = f.getRange(1, 1, 1, f.getLastColumn()).getValues()[0];
  const col = cap.indexOf(campo) + 1;
  if (col > 0) f.getRange(riga, col).setValue(valore);
}
function annota(testo) { foglio('Registro').appendRow([new Date(), testo]); }

/* ---------- mandare ---------- */
/**
 * Manda un modello gia' approvato da Meta.
 * @param {string} numero  in formato internazionale senza + (es. 393331234567)
 * @param {string} modello il nome del modello (es. nipec_noleggio_it_1)
 * @param {string} lingua  'it' oppure 'sq'
 * @param {string} nome    quello che va al posto di {{1}}
 */
function manda(numero, modello, lingua, nome) {
  const corpo = {
    messaging_product: 'whatsapp',
    to: String(numero).replace(/\D/g, ''),
    type: 'template',
    template: {
      name: modello,
      language: { code: lingua },
      components: [{ type: 'body', parameters: [{ type: 'text', text: String(nome || '') }] }]
    }
  };
  const r = UrlFetchApp.fetch(API + '/' + chiave('NUMERO_ID') + '/messages', {
    method: 'post', contentType: 'application/json',
    headers: { Authorization: 'Bearer ' + chiave('TOKEN') },
    payload: JSON.stringify(corpo), muteHttpExceptions: true
  });
  const esito = JSON.parse(r.getContentText() || '{}');
  if (r.getResponseCode() >= 300) {
    const e = (esito.error || {});
    // 131026 = quel numero su WhatsApp non c'e'. E' la risposta alla domanda di Giorgio.
    return { ok: false, codice: e.code, perche: e.message, nonSuWhatsApp: e.code === 131026 };
  }
  return { ok: true, id: (esito.messages || [{}])[0].id };
}

/* ---------- il giro del giorno ---------- */
const FERMI = ['risposto', 'interessato', 'non interessato', 'numero errato', 'non disturbare'];
const MODELLO = (paese, passo) => 'nipec_noleggio_' + (paese === 'AL' ? 'sq' : 'it') + '_' + passo;

function giroDiOggi() {
  const quota = Number(P().getProperty('AL_GIORNO') || 250);
  const attesa1 = Number(P().getProperty('ATTESA_1') || 5);
  const attesa2 = Number(P().getProperty('ATTESA_2') || 7);
  const oggi = Utilities.formatDate(new Date(), 'Europe/Rome', 'yyyy-MM-dd');
  let mandati = 0, falliti = 0, senzaWA = 0;

  for (const c of contatti()) {
    if (mandati >= quota) break;
    if (!c.numero || FERMI.indexOf(String(c.stato)) >= 0) continue;
    const n = Number(c.invii || 0);
    const giorni = c.ultimoInvio ? Math.floor((new Date(oggi) - new Date(c.ultimoInvio)) / 86400000) : 9999;
    let passo = 0;
    if (n === 0) passo = 1;
    else if (n === 1 && giorni >= attesa1) passo = 2;
    else if (n === 2 && giorni >= attesa2) passo = 3;
    if (!passo) continue;

    const paese = String(c.paese || 'IT').toUpperCase();
    const nome = String(c.nome || c.centro || '').trim().split(/\s+/)[0] || 'ciao';
    const e = manda(c.numero, MODELLO(paese, passo), paese === 'AL' ? 'sq' : 'it', nome);

    if (e.ok) {
      scrivi(c._riga, 'invii', n + 1);
      scrivi(c._riga, 'ultimoInvio', oggi);
      scrivi(c._riga, 'stato', 'inviato');
      mandati++;
    } else if (e.nonSuWhatsApp) {
      scrivi(c._riga, 'stato', 'non su WhatsApp');
      senzaWA++;
    } else {
      annota('ERRORE ' + c.numero + ' -> ' + e.codice + ' ' + e.perche);
      falliti++;
    }
    Utilities.sleep(1200);   // non si spara: si cammina
  }
  annota('Giro del ' + oggi + ': ' + mandati + ' mandati, ' + senzaWA + ' non su WhatsApp, ' + falliti + ' errori');
  return { mandati: mandati, senzaWA: senzaWA, falliti: falliti };
}

/* ---------- le risposte ---------- */
/** Meta chiama questo indirizzo una volta, per verificare che sia nostro. */
function doGet(e) {
  const p = (e && e.parameter) || {};
  if (p['hub.mode'] === 'subscribe' && p['hub.verify_token'] === chiave('VERIFICA'))
    return ContentService.createTextOutput(p['hub.challenge']);
  return ContentService.createTextOutput('no');
}

/** Qui arrivano le risposte dei clienti e gli stati di consegna. */
function doPost(e) {
  try {
    const dati = JSON.parse(e.postData.contents);
    (dati.entry || []).forEach(voce => (voce.changes || []).forEach(c => {
      const v = c.value || {};
      (v.messages || []).forEach(m => {
        const da = m.from;
        // il bottone «Non ora» vale come: non scrivergli piu'
        const testo = m.text ? m.text.body
                    : m.button ? m.button.text
                    : (m.interactive && m.interactive.button_reply) ? m.interactive.button_reply.title
                    : '(' + m.type + ')';
        segnaRisposta(da, testo);
      });
      (v.statuses || []).forEach(s => {
        if (s.status === 'failed') annota('CONSEGNA FALLITA ' + s.recipient_id + ' -> ' +
          JSON.stringify((s.errors || [{}])[0]));
      });
    }));
  } catch (err) { annota('WEBHOOK rotto: ' + err); }
  return ContentService.createTextOutput('ok');
}

const RIFIUTI = ['non ora', 'jo tani', 'stop', 'non mi interessa', 'nuk me intereson', 'nuk më intereson', 'basta'];
function segnaRisposta(numero, testo) {
  const n = String(numero).replace(/\D/g, '');
  const t = String(testo || '').toLowerCase().trim();
  const rifiuta = RIFIUTI.some(r => t === r || t.indexOf(r) === 0);
  for (const c of contatti()) {
    if (String(c.numero).replace(/\D/g, '') !== n) continue;
    scrivi(c._riga, 'stato', rifiuta ? 'non interessato' : 'risposto');
    scrivi(c._riga, 'risposta', testo);
    scrivi(c._riga, 'quando', new Date());
    return;
  }
  foglio('Contatti').appendRow([n, '', '', '', '', 'risposto', 0, '', testo, new Date()]);
}

/* ---------- prove da fare prima di partire ---------- */
/** Controlla che le chiavi ci siano e che Meta risponda. Non manda niente a nessuno. */
function prova() {
  ['TOKEN', 'NUMERO_ID', 'WABA_ID', 'VERIFICA'].forEach(k => chiave(k));
  const r = UrlFetchApp.fetch(API + '/' + chiave('NUMERO_ID') + '?fields=display_phone_number,verified_name,quality_rating',
    { headers: { Authorization: 'Bearer ' + chiave('TOKEN') }, muteHttpExceptions: true });
  Logger.log(r.getContentText());
  const m = UrlFetchApp.fetch(API + '/' + chiave('WABA_ID') + '/message_templates?fields=name,status,language',
    { headers: { Authorization: 'Bearer ' + chiave('TOKEN') }, muteHttpExceptions: true });
  Logger.log(m.getContentText());
}

/** Manda UN messaggio a un numero tuo, per vedere come arriva. */
function provaSuDiMe() {
  const mio = P().getProperty('NUMERO_DI_PROVA');
  if (!mio) throw new Error('Metti NUMERO_DI_PROVA nelle proprieta\', col prefisso e senza +');
  Logger.log(JSON.stringify(manda(mio, 'nipec_noleggio_it_1', 'it', 'Giorgio')));
}
