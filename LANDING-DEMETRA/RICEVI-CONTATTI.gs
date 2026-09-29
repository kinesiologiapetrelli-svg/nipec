/**
 * DEMETRA · ricevitore dei contatti della landing
 * ---------------------------------------------------------------
 * Scrive ogni richiesta in un foglio Google. Non legge e non
 * restituisce mai niente: chi conoscesse l'indirizzo puo' al massimo
 * aggiungere righe finte, non leggere i contatti gia' raccolti.
 *
 * COME SI METTE IN OPERA
 *  1. Foglio Google nuovo -> Estensioni -> Apps Script
 *  2. Incolla tutto questo al posto di quello che c'e'
 *  3. Cambia PAROLA con una tua, e mettila uguale nella landing
 *  4. Distribuisci -> Nuova distribuzione -> Applicazione web
 *       Esegui come: Me    ·    Chi ha accesso: Chiunque
 *  5. Copia l'indirizzo che finisce con /exec e incollalo nella
 *     landing, dentro CFG.endpoint
 *
 * SE POI MODIFICHI QUESTO CODICE: Gestisci distribuzioni -> matita ->
 * Nuova versione. Mai una distribuzione nuova, altrimenti cambia
 * l'indirizzo e la landing continua a parlare con quella vecchia.
 */

var PAROLA = "CAMBIAMI-CON-UNA-TUA";
var FOGLIO = "CONTATTI";

function doPost(e) {
  var esito = { ok: false };
  var lucchetto = LockService.getScriptLock();
  try {
    lucchetto.waitLock(20000);
    var dati = JSON.parse(e.postData.contents);
    if (String(dati.parola || "") !== PAROLA) return risposta({ ok: false });

    var f = foglio();
    var col = intestazione(f);
    col = allarga(f, col, Object.keys(dati).filter(function (k) { return k !== "parola"; }));

    var riga = col.map(function (nome) {
      if (nome === "ricevuto") return new Date();
      if (nome === "stato")    return "da richiamare";
      return dati[nome] === undefined ? "" : String(dati[nome]);
    });
    f.appendRow(riga);
    esito.ok = true;
  } catch (err) {
    esito.ok = false;
  } finally {
    try { lucchetto.releaseLock(); } catch (x) {}
  }
  return risposta(esito);
}

/* Chi apre l'indirizzo nel browser non deve vedere niente di utile. */
function doGet() { return risposta({ ok: true }); }

function risposta(o) {
  return ContentService.createTextOutput(JSON.stringify(o))
                       .setMimeType(ContentService.MimeType.JSON);
}

function foglio() {
  var libro = SpreadsheetApp.getActiveSpreadsheet();
  var f = libro.getSheetByName(FOGLIO);
  if (!f) {
    f = libro.insertSheet(FOGLIO);
    f.appendRow(["ricevuto", "stato", "nome", "telefono", "obiettivo", "quando", "pagina"]);
    f.getRange(1, 1, 1, 7).setFontWeight("bold");
    f.setFrozenRows(1);
  }
  return f;
}

/* La riga 1 e' l'elenco vero delle colonne: si legge, non si indovina. */
function intestazione(f) {
  if (f.getLastRow() === 0) return [];
  return f.getRange(1, 1, 1, f.getLastColumn()).getValues()[0]
          .map(function (x) { return String(x).trim(); });
}

/* Se la landing un giorno manda un campo nuovo, la colonna si aggiunge da sola. */
function allarga(f, col, chiavi) {
  var mancanti = chiavi.filter(function (k) { return col.indexOf(k) === -1; });
  if (!mancanti.length) return col;
  var tutte = col.concat(mancanti);
  f.getRange(1, 1, 1, tutte.length).setValues([tutte]);
  f.getRange(1, 1, 1, tutte.length).setFontWeight("bold");
  return tutte;
}
