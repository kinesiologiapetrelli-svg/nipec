/*  MAGAZZINO NIPEC — ponte fra l'app e il Foglio Google
 *  VERSIONE 2: da usare quando NON trovi il menu "Estensioni".
 *  ----------------------------------------------------------
 *  Si incolla su  script.google.com  →  Nuovo progetto.
 *  Rispetto all'altra versione cambia una cosa sola: qui devi dirgli
 *  QUALE foglio usare, scrivendo il suo codice qui sotto.
 *
 *  Cosa fa: tiene il magazzino su tre schede del foglio e risponde all'app.
 *  Non sovrascrive mai tutto: aggiorna riga per riga, così se Alice registra
 *  un'uscita mentre Giorgio registra un'entrata, restano tutte e due.
 */

/* ⚠️ DUE COSE DA SCRIVERE QUI SOTTO, poi non tocchi più niente.

   1) La parola d'ordine: inventane una tua. La stessa va messa nell'app.        */
var PAROLA = "CAMBIAMI-CON-UNA-TUA";

/* 2) Il codice del foglio. Apri il foglio e guarda l'indirizzo in alto:

        docs.google.com/spreadsheets/d/1AbC...XyZ/edit
                                      \_____________/
                                       questo pezzo qui

      Copialo e incollalo qui in mezzo alle virgolette.                          */
var CODICE_FOGLIO = "INCOLLA-QUI-IL-CODICE-DEL-FOGLIO";

var SCHEDE = { articoli: "ARTICOLI", movimenti: "MOVIMENTI", magazzini: "MAGAZZINI" };
var COLONNE = {
  articoli: ["id", "attribuzione", "codice", "descrizione", "categoria", "unita",
             "scortaMin", "prezzoAcquisto", "fornitore", "paese", "posizione",
             "magazzinoId", "foto", "agg"],
  movimenti: ["id", "articoloId", "tipo", "qta", "data", "fornitore", "numeroAcquisto",
              "prezzo", "destinazione", "causale", "nota", "da", "a",
              "paeseDa", "paeseA", "agg"],
  magazzini: ["id", "nome", "agg"]
};

function doGet(e) {
  var p = (e && e.parameter) || {};
  if (p.token !== PAROLA) return rispondi({ errore: "parola d'ordine sbagliata" });
  return rispondi(leggiTutto());
}

function doPost(e) {
  var corpo;
  try { corpo = JSON.parse(e.postData.contents); }
  catch (err) { return rispondi({ errore: "dati illeggibili" }); }
  if (!corpo || corpo.token !== PAROLA) return rispondi({ errore: "parola d'ordine sbagliata" });

  /* un lucchetto per volta: se due telefoni scrivono insieme, si mettono in fila */
  var lucchetto = LockService.getScriptLock();
  try { lucchetto.waitLock(25000); }
  catch (err) { return rispondi({ errore: "foglio occupato, riprova" }); }

  try {
    ["magazzini", "articoli", "movimenti"].forEach(function (t) {
      if (corpo[t] && corpo[t].length) scrivi(t, corpo[t]);
    });
    return rispondi(leggiTutto());
  } finally {
    lucchetto.releaseLock();
  }
}

function leggiTutto() {
  var out = { ok: true, quando: new Date().toISOString() };
  Object.keys(SCHEDE).forEach(function (t) { out[t] = leggi(t); });
  return out;
}

function foglio(tipo) {
  var ss = SpreadsheetApp.openById(CODICE_FOGLIO);
  var f = ss.getSheetByName(SCHEDE[tipo]);
  if (!f) {
    f = ss.insertSheet(SCHEDE[tipo]);
    f.getRange(1, 1, 1, COLONNE[tipo].length).setValues([COLONNE[tipo]]);
    f.setFrozenRows(1);
  }
  if (f.getLastRow() === 0) {
    f.getRange(1, 1, 1, COLONNE[tipo].length).setValues([COLONNE[tipo]]);
    f.setFrozenRows(1);
  }
  return f;
}

function leggi(tipo) {
  var f = foglio(tipo), col = COLONNE[tipo];
  var n = f.getLastRow();
  if (n < 2) return [];
  var righe = f.getRange(2, 1, n - 1, col.length).getValues();
  var out = [];
  righe.forEach(function (r) {
    if (!r[0]) return;                       /* riga senza id: la salto */
    var o = {};
    col.forEach(function (c, i) { o[c] = r[i] === "" ? "" : r[i]; });
    o.id = String(o.id);
    if (tipo === "movimenti") { o.articoloId = String(o.articoloId); o.qta = Number(o.qta) || 0; }
    out.push(o);
  });
  return out;
}

/* Aggiorna le righe esistenti (per id) e aggiunge quelle nuove in fondo. */
function scrivi(tipo, elenco) {
  var f = foglio(tipo), col = COLONNE[tipo];
  var n = f.getLastRow();
  var indice = {};
  if (n >= 2) {
    var ids = f.getRange(2, 1, n - 1, 1).getValues();
    for (var i = 0; i < ids.length; i++) {
      if (ids[i][0] !== "") indice[String(ids[i][0])] = i + 2;   /* id -> numero di riga */
    }
  }
  var nuove = [];
  elenco.forEach(function (o) {
    if (!o || !o.id) return;
    var riga = col.map(function (c) { return o[c] === undefined || o[c] === null ? "" : o[c]; });
    var dove = indice[String(o.id)];
    if (dove) f.getRange(dove, 1, 1, col.length).setValues([riga]);
    else nuove.push(riga);
  });
  if (nuove.length) f.getRange(f.getLastRow() + 1, 1, nuove.length, col.length).setValues(nuove);
}

function rispondi(o) {
  return ContentService.createTextOutput(JSON.stringify(o))
    .setMimeType(ContentService.MimeType.JSON);
}

/* PROVA PRIMA DI PUBBLICARE.
   Nell'editor scegli "prova" dal menu delle funzioni e premi Esegui.
   - Se dice "foglio trovato" sei a posto.
   - Se dà errore, quasi sempre il CODICE_FOGLIO è sbagliato o incompleto. */
function prova() {
  try {
    var nome = SpreadsheetApp.openById(CODICE_FOGLIO).getName();
    Logger.log("foglio trovato: " + nome);
    Logger.log(JSON.stringify(leggiTutto()).slice(0, 300));
  } catch (e) {
    Logger.log("NON riesco ad aprire il foglio. Controlla CODICE_FOGLIO. " + e.message);
  }
}
