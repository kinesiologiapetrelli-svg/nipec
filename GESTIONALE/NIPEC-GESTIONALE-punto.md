# NIPEC · Gestionale — punto tecnico

**Indirizzo:** https://cruscottonipec.netlify.app/
**Rilevato il:** 20 ottobre 2026 · leggendo il sorgente pubblicato, non un repository
**Versione service worker:** `nipec-gestionale-v17` · **versione dati:** `S.v = 2`
**A chi serve questo documento:** a chi deve studiare il gestionale, capirlo e modificarlo.

> **Come usare questo file.** È il punto di partenza, non la fine. Le sezioni da
> §1 a §9 descrivono quello che il codice fa *oggi*, verificato riga per riga.
> La §10 e la §11 sono i problemi che ho trovato. La §12 è vuota apposta:
> va riempita con domande e modifiche richieste, e rimandata indietro.
> Chi riceve questo file può darlo in pasto a Claude e lavorarci sopra
> direttamente: è scritto per essere letto da una persona e da un agente.

---

## 1. Che cos'è

Un gestionale per NIPEC che tiene insieme **quattro cose che di solito stanno in
quattro programmi diversi**:

1. la **contabilità** (entrate e uscite, Italia e Albania separate),
2. lo **scadenziario** dei canoni di noleggio (chi deve pagare, quanto, quando),
3. il **magazzino** macchine e ricambi, con le sedi e i noleggi in corso,
4. l'**anagrafica clienti** unica, che fa da collante fra le altre tre.

Più una quinta scheda, la **Diagnosi**, che non è contabilità: è un cruscotto di
sei indicatori strategici con soglie semaforiche.

**La caratteristica che decide tutto il resto:** è **un solo file HTML**.
Nessun framework, nessun build, nessun `npm install`, nessun backend proprio.
196 KB in cui stanno markup, CSS e JavaScript. Si apre con doppio clic e funziona.

```
 index.html  196 KB   ← tutto qui dentro
 ├── righe    1–16    <head> (font Archivo, favicon SVG inline)
 ├── righe   17–386   CSS (369 righe, variabili su :root, tema chiaro/scuro)
 ├── righe  387–619   markup: header, nav, 8 <dialog>, contenitore #app
 └── righe  620–1735  JavaScript (1115 righe, IIFE, 'use strict')
```

---

## 2. Architettura in cinque righe

```
┌─ BROWSER ──────────────────────────────────────────────┐
│  index.html                                             │
│    S  ← oggetto JavaScript unico, tutto lo stato        │
│    ↕                                                    │
│  localStorage  'nipec_gestionale_v2'  (KEY)             │
│                'nipec_gestionale_v3_safe'  (SAFE)       │
└───────────────────────┬─────────────────────────────────┘
                        │  POST JSON, ogni 60 secondi
                        ▼
          Google Apps Script  (/macros/s/AKfycb…g6BX5A/exec)
                        │
                        ▼
                  Google Drive  ← l'unica copia condivisa
```

Non c'è un database. Non c'è un server NIPEC. Il "cloud" è un foglio di codice
Google Apps Script che legge e scrive un file su Drive. Tutta la logica —
ogni calcolo, ogni regola, ogni semaforo — sta nel browser.

**Conseguenza da tenere a mente prima di qualsiasi modifica:** cambiare una
riga di questo file cambia il comportamento di tutti i dispositivi collegati,
appena ricaricano. Non esiste un ambiente di prova.

---

## 3. I file pubblicati

| File | Stato | A cosa serve |
|---|---|---|
| `index.html` | 200 · 196 KB | L'applicazione intera |
| `manifest.webmanifest` | 200 | PWA: nome, icone, `display: standalone` |
| `sw.js` | 200 | Service worker, cache `nipec-gestionale-v17` |
| `icon-192.png` · `icon-512.png` · `apple-touch-icon.png` | — | Icone |
| `dati-telefono.enc` | **404** | Pacchetto cifrato PC → telefono. **Non c'è** (vedi §11.4) |
| `netlify.toml` | 404 | Nessuna configurazione Netlify |

È una **PWA installabile**: si aggiunge alla schermata Home e si apre a schermo
intero come un'app. Il service worker usa una strategia **network-first con
ripiego sulla cache**: prova sempre la rete, se non c'è serve l'ultima copia.

---

## 4. Lo stato `S` — l'albero completo

Tutta l'applicazione legge e scrive un solo oggetto. Questo è il suo albero
esatto, da `defState()` (riga 639):

```js
S = {
  v: 2,                    // versione del formato dati
  anno: 2026,              // anno contabile di riferimento
  cats: {                  // categorie di entrata/uscita, per paese
    IT: { E: [...], U: [...] },
    AL: { E: [...], U: [...] }
  },
  mov:  [],                // movimenti contabili            → §5.1
  ric:  [],                // contratti e costi ricorrenti    → §5.2
  clienti: [],             // anagrafica unica                → §5.3
  mag: {                   // magazzino                       → §5.4
    articoli: [], movimenti: [], sedi: []
  },
  scadCan: {},             // canoni dei noleggi, scritti a mano → §7.1
  scadStart: '',           // 'AAAA-MM': prima dello scadenziario non esiste
  storico: {},             // { 2023: {E: …, U: …}, … } anni chiusi
  cru: { inputs: {}, snaps: [] },   // Diagnosi: valori e fotografie → §7.5
  gen: {},                 // ⚠️ DICHIARATO E MAI USATO (vedi §11.6)
  ui: {                    // preferenze di vista, NON sincronizzate
    tab: 'panoramica', view: 'mese', cursor: '2026-10-20',
    country: 'ALL', closed: {}, theme: undefined
  },
  // campi di servizio, aggiunti a runtime:
  _rev: 0,                 // revisione locale, per le schede aperte in parallelo
  syncRev: 0,              // revisione vista sul cloud
  syncHash: '', syncAt: '' // impronta e data dell'ultimo invio
}
```

**`normalize()` (riga 650) è la rete di sicurezza.** Ogni volta che si carica
uno stato — da localStorage, da un backup, dal cloud — passa di lì, e ogni
ramo mancante viene ricostruito dal default. Vuol dire che un backup vecchio o
incompleto non rompe l'app. **Qualsiasi campo nuovo va aggiunto in due posti:
`defState()` e `normalize()`.** Saltare il secondo è il modo più comune di
rompere questo tipo di applicazione.

---

## 5. Le entità, una per una

### 5.1 Movimento contabile — `S.mov[]`

Il mattone della contabilità. Un record per ogni euro entrato o uscito.

```js
{
  id:  'lx8f2a9kq',   // uid(): base36 del timestamp + 5 caratteri casuali
  d:   '2026-10-20',  // data ISO
  p:   'IT',          // paese: 'IT' | 'AL'
  t:   'E',           // tipo: 'E' entrata | 'U' uscita
  c:   'Club 500',    // categoria, presa da S.cats[p][t]
  cl:  'ESTETICA X',  // cliente, SEMPRE normalizzato da ensureCli()
  mac: 'Laser 500',   // macchina (testo libero, con datalist di aiuto)
  imp: 500,           // importo
  sp:  0,             // spese dirette — solo sulle entrate
  n:   'Canone …',    // nota
  src: 'scad:…@2026-10'  // provenienza, se generato (vedi sotto)
}
```

**Il campo `src` è il perno dell'automatismo.** Dice *chi* ha creato il
movimento, e serve a non crearlo due volte:

| Valore di `src` | Chi l'ha creato |
|---|---|
| assente | Scritto a mano |
| `<idRicorrente>@AAAA-MM` | Generato da `genMonth()` per i costi fissi |
| `scad:<chiave>@AAAA-MM` | Generato da `markPaid()` quando si segna un canone pagato |

### 5.2 Ricorrente — `S.ric[]`

Due cose nello stesso contenitore, distinte da `t`: i **contratti attivi**
(`t:'E'`, generano scadenze) e i **costi fissi** (`t:'U'`, generano uscite).

```js
{
  id: 'lx8f2…', attivo: true,
  p: 'IT', t: 'E',
  freq: 'mensile',    // 'mensile' (senza fine) | 'rate' (n rate) | 'singola'
  c: 'Club 500', cl: 'ESTETICA X', mac: 'Laser 500',
  imp: 500, sp: 0,
  dal: '2026-01',     // mese della prima scadenza
  al:  '',            // ultimo mese; vuoto = senza fine
  g:   30,            // giorno di scadenza nel mese (default 30)
  inizio: '2024-03'   // contratto dal — usato per la fedeltà, non per le scadenze
}
```

Nota: `freq: 'rate'` non memorizza il numero di rate. Lo calcola: il form chiede
"quante rate", e il codice scrive `al = addYM(dal, n-1)`. Il numero si
ricostruisce con `monthsBetween(dal, al) + 1`. **Modificare `al` cambia il
numero di rate senza dirlo.**

### 5.3 Cliente — `S.clienti[]`

L'anagrafica unica. È quella che tiene insieme le altre schede.

```js
{
  id: 'clx8f2…', nome: 'ESTETICA X',   // nome CANONICO, sempre MAIUSCOLO
  paese: 'IT',
  alias: ['ESTETICA X SRL', 'EST X'],  // gli altri modi in cui è scritto
  stato: 'attivo',                      // 'attivo' | 'sospeso'
  // anagrafica fiscale (costante `CF`, riga 1382):
  ragione, piva, cf, indirizzo, cap, citta, provincia, regione,
  email, pec, sdi, telefono, referente,
  note: '',
  luogoDedotto: 1   // 1 = città indovinata dal nome, non confermata
}
```

**La normalizzazione dei nomi è il meccanismo più delicato dell'app.**

```js
nName(x)  // MAIUSCOLO, punti e slash → spazi, spazi multipli → uno solo
cliOf(n)  // cerca in un indice che mappa nome E alias → cliente
canon(n)  // restituisce il nome canonico, o nName(n) se il cliente non esiste
```

L'indice `_cliIdx` è **memorizzato in cache** e va invalidato con `cliReset()`
dopo ogni modifica all'anagrafica. `render()` lo fa già a ogni disegno. Chi
tocca `S.clienti` fuori da un `render()` deve chiamarlo a mano.

`ensureCli(nome, paese)` crea il cliente se non esiste e restituisce il nome
canonico. Viene chiamato **al salvataggio di ogni entrata e di ogni contratto**:
è così che l'anagrafica si popola da sola.

`renameCli(vecchi, nuovo)` riscrive il nome **in quattro posti** —
`S.mov`, `S.ric`, `S.mag.movimenti[].destinazione` e le chiavi di `S.scadCan`.
Se si aggiunge un quinto posto che contiene nomi di clienti, va aggiunto lì.

C'è anche un controllo di validità su P.IVA e NIPT (`vatOk`, riga 1385):
11 cifre con checksum di Luhn per l'Italia, `lettera + 8 cifre + lettera` per
l'Albania. È un avviso, non un blocco: si può salvare lo stesso.

### 5.4 Magazzino — `S.mag`

Tre liste. `articoli` (il catalogo), `movimenti` (le righe di carico/scarico),
`sedi` (dove stanno le cose).

```js
sedi:     [{ nome: 'Padenghe', paese: 'IT' }, { nome: 'Tirana', paese: 'AL' }, …]
articoli: [{ id, descrizione, attribuzione, categoria, sede, paese,
             kind: 'macchina'|'ricambio', scortaMin, foto: 'data:image/…' }]
movimenti:[{ articoloId, tipo: 'entrata'|'uscita'|'spostamento',
             qta, data, sede, sedeDa, sedeA,
             causale: 'noleggio'|'rientro'|…, destinazione: 'ESTETICA X',
             nota: '500',        // ⚠️ qui dentro ci finisce il canone
             eliminato: false }]
```

**Le giacenze non sono memorizzate: si calcolano.** `stock()` (riga 1209)
ripercorre tutti i movimenti vivi e costruisce `{articoloId: {sede: quantità}}`.
Entrata somma, uscita sottrae, spostamento fa tutte e due.

**I noleggi attivi nemmeno:** `noleggi()` (riga 1214) li ricava incrociando le
uscite con causale che contiene "noleggio" e le entrate con causale "rientro",
raggruppate per `articoloId + destinazione`. Resta attivo quello con quantità
positiva.

> Qui c'è una fragilità reale: **l'aggancio è un `/noleggio/i` e un `/rientro/i`
> sulla causale scritta a mano.** Una causale scritta "Noleggio" va bene,
> "a noleggio" va bene, "NOL." **non** viene vista e la macchina sparisce dai
> noleggi attivi — e quindi dallo scadenziario.

`guessKind()` indovina se un articolo è macchina o ricambio con due espressioni
regolari sul testo (`MACH_RE` elenca i modelli NIPEC: laser ares, afrodite,
borea, cryo, ems, ermes, modularis, shape, uriel; `PART_RE` elenca i pezzi).
Nel dubbio, ricambio.

---

## 6. Le otto schede

Un router di una riga (`render()`, riga 725) sceglie la funzione di disegno.
Ogni scheda **riscrive tutto `#app`** da zero a ogni `render()`.

| Scheda | Funzione | Che cosa fa |
|---|---|---|
| **Panoramica** | `rPanoramica` 770 | KPI dell'anno, grafico 12 mesi, classifiche |
| **Movimenti** | `rMovimenti` 828 | Contabilità, in vista giorno / settimana / mese / anno |
| **Scadenze** | `rScadenze` 1482 | Chi deve pagare questo mese → §7.1 |
| **Clienti** | `rClienti` 1394 | Anagrafica, ricerca, raggruppamenti, unione |
| **Magazzino** | `rMagazzino` 1228 | Articoli, giacenze per sede, noleggi in corso |
| **Ricorrenti** | `rRicorrenti` 992 | Contratti e costi fissi, generazione del mese |
| **Diagnosi** | `rDiagnosi` 1086 | Sei pilastri strategici → §7.5 |
| **Impostazioni** | `rImpostazioni` 1142 | Accesso, categorie, backup, storico |

Sopra tutto c'è un **filtro paese** a tre posizioni — `IT` / `AL` / `ALL` — in
`S.ui.country`. Attraversa ogni scheda tramite `inCountry()` (riga 708).
È il motivo per cui Italia e Albania convivono senza mescolarsi.

Su schermo stretto (`max-width: 760px`) le tabelle diventano schede
(`mvCards`, `ricCards`, `artCards`, `rentCards`, `partCards`) e compare una
barra di navigazione in basso con un pulsante **+** flottante.

---

## 7. Le regole che contano

### 7.1 Scadenziario — come nasce la lista "chi deve pagare"

È la parte con più logica dell'app, e quella che va capita prima di toccarla.
`scadLines(ym)` (riga 1456) costruisce le righe del mese da **due sorgenti**:

1. **dai contratti** — ogni `S.ric` con `t:'E'` attivo nel mese, cliente non
   sospeso. Chiave: `ric:<id>`.
2. **dai noleggi di magazzino** — ogni noleggio attivo. Chiave:
   `nol:<articoloId>|<cliente>`.

**Regola di precedenza:** se un cliente ha già una riga da contratto, il suo
noleggio di magazzino **viene saltato** (`sameCl`). Serve a non far pagare due
volte lo stesso canone. `sameCl` confronta i nomi canonici e, solo se *nessuno
dei due* è in anagrafica, accetta anche un contenimento parziale fra stringhe
più lunghe di 3 caratteri.

**Da dove esce l'importo di un noleggio.** Non c'è un campo "canone" nel
magazzino. Il codice prova, in quest'ordine:

1. `S.scadCan['nol:…']` — se è stato scritto a mano nello scadenziario;
2. `parseCanone(movimento.nota)` — **se la nota del movimento di magazzino
   contiene solo un numero**, quello è il canone;
3. altrimenti zero, e la riga viene marcata `noCan` → stato **"canone?"**.

Poi `scadClients(ym)` (riga 1464) raggruppa per cliente, cerca il pagamento e
assegna lo stato:

```
pagato        tutte le righe hanno un pagamento e nessun canone manca
scaduto       oggi > data di scadenza
in scadenza   mancano 5 giorni o meno
da pagare     tutto il resto
canone?       niente da incassare perché non si sa quanto
```

**La riconciliazione automatica.** Se una riga non ha un pagamento collegato,
il codice cerca in contabilità un'entrata *dello stesso mese, della stessa
categoria, dello stesso cliente* e non già usata da un'altra riga. Se la
trova, la considera il pagamento e la marca `auto: true`.

> Questo è comodo e rischioso insieme. Un incasso registrato a mano per un
> motivo diverso, che per caso cade nel mese giusto con la categoria giusta,
> viene letto come il canone pagato. **Non c'è modo, nell'interfaccia, di
> dire "no, questo incasso non è il canone".**

`markPaid()` scrive le entrate con `src: 'scad:<chiave>@<mese>'`.
`unPaid()` le cancella filtrando su quello stesso `src`. È un'operazione
reversibile e questo va preservato in ogni modifica.

`S.scadStart` è un taglio netto: prima di quel mese lo scadenziario non
produce niente. Serve a non far apparire anni di arretrati inventati quando si
inserisce un contratto vecchio.

### 7.2 Generazione dei costi fissi

`genMonth(ym)` (riga 985) crea i movimenti di uscita del mese dai ricorrenti
`t:'U'`. Protetto contro i doppioni da `isGenerated()`, che cerca un movimento
con `src === r.id+'@'+ym`. Il giorno viene limitato all'ultimo del mese
(`Math.min(g, ultimoGiorno)`): niente 30 febbraio.

### 7.3 Categorie

Non sono una tabella: sono **liste di stringhe** per paese e per tipo
(`DEF_CATS`, riga 630). La categoria sul movimento è il testo stesso.

> Conseguenza: **rinominare una categoria nelle impostazioni non rinomina i
> movimenti già registrati.** Restano agganciati al vecchio testo e di fatto
> escono dai raggruppamenti. È il tipo di cosa che si scopre a fine anno.

`catFor()` (riga 1453) indovina la categoria di un noleggio dal nome
dell'articolo e dall'importo: laser ≥ 500 → "Club 500", laser sotto → "Club 400",
afrodite/shape/modularis → la loro, ems/ermes → "EMS".

### 7.4 Importi e numeri

`num()` (riga 694) legge il formato italiano: toglie `€` e spazi, toglie i punti
delle migliaia **solo quando sono seguiti da tre cifre**, poi converte la virgola
in punto. Quindi `1.250,50` → `1250.5` e `1.5` → `1.5`. È scritto bene.
In uscita, `numIT`/`eur` riformattano all'italiana con lo spazio unificatore
prima dell'euro.

### 7.5 Diagnosi — i sei pilastri

Non è contabilità. È un questionario con soglie, che misura la salute
strategica dell'azienda. Sei pilastri (`PIL`, riga 1046):

| | Pilastro | La domanda a cui risponde |
|---|---|---|
| P1 | Parco & Ricorrente | Se il ricorrente evapora, muore tutto |
| P2 | Utilizzo Parco | Quante macchine sono ferme in magazzino |
| P3 | Affidabilità & Muletto | Quanto ci metto a sostituire una macchina guasta |
| P4 | Acquisizione | Entra sangue nuovo o vivo di passaparola |
| P5 | Ecosistema | Quanto attaccano DEMETRA, Metodo e PRAGMA |
| P6 | Scalabilità / Dipendenza | Regge senza Giorgio |

Ogni campo è `['in'|'out', chiave, etichetta, unità, soglie?, nota?]`.
I campi `in` si digitano, i campi `out` li calcola `derive()` (riga 1066):

```
centri  = nLaser500 + nLaser400 + nAfro500 + nVario + nRate
mrrNol  = nLaser500×500 + nLaser400×400 + nAfro500×500 + nVario×canVario
mrrRate = nRate × rataMedia
mrr     = mrrNol + mrrRate
pctNol  = mrrNol / mrr          ← % di ricorrente che non finisce mai
churn   = persi / (centri + persi)
fedelta = over12 / centri
utilizzo= macRed / macTot
sysIdx  = min(1, pDem/60) + min(1, pMet/40) + min(1, pPra/30) + min(1, upsell/200)
```

Le soglie sono `[verde, giallo, direzione]`, con `direzione: 1` se più alto è
meglio e `-1` se più basso è meglio (`statusOf`, riga 1078). Il punteggio di un
pilastro è la media dei suoi campi con soglia (verde 100, giallo 50, rosso 0);
il punteggio complessivo è la media dei pilastri valorizzati.

**I canoni 500 e 400 sono scritti nel codice** (`CANONE`, riga 1045, e dentro
`derive`). Se cambiano i prezzi, vanno cambiati lì — non c'è un'impostazione.

---

## 8. Sincronizzazione e accesso

### 8.1 Come funziona

Il motore è `syncCall()` (riga 1627): un `POST` di testo con dentro
`{pw, device, op, …}`. Quattro operazioni: `get`, `put`, `rev`, `chpw`.

```
all'avvio          → syncPull()
ogni 60 secondi    → syncPull()
al ritorno a fuoco → syncPull()   (visibilitychange)
al ritorno online  → syncPull()
dopo ogni save()   → syncPush() con 2,5 s di attesa (schedulePush)
```

**Controllo delle revisioni.** `syncPush` manda `base: S.syncRev`. Se il
server ha una revisione più alta risponde `{err: 'conflict', data, rev}` e il
client **scarica e applica i dati remoti**, avvisando con un messaggio. Prima
di inviare, `hashStr()` confronta un'impronta: se non è cambiato niente, non
manda niente.

**Due chiavi di localStorage, non una.** `KEY` e `SAFE` ricevono lo stesso
testo a ogni `save()`. `readBest()` legge tutte e due e tiene quella con `_rev`
più alto. È una difesa contro la scrittura interrotta a metà. In più, un
`window.addEventListener('storage')` tiene allineate le schede aperte in
parallelo sullo stesso computer.

`dataOnly()` toglie `ui`, `_rev`, `syncRev`, `syncHash`, `syncAt`, `_migrated`
prima di inviare: **le preferenze di vista restano locali al dispositivo.**
Giusto così — il telefono non deve ereditare la scheda aperta sul PC.

### 8.2 Accesso

Una sola parola d'ordine, minimo 6 caratteri, uguale su tutti i dispositivi,
inserita una volta per dispositivo. `doLogin()` (riga 1680) la salva in
`nipec_sync_cfg` e prova subito un `op:'get'`. Se arrivano dati, li applica;
se il dispositivo aveva già dati suoi non ancora sincronizzati, ne salva una
copia in `nipec_backup_prima_accesso` prima di sovrascriverli.

Se durante un `syncPull` il server risponde `auth`, la configurazione viene
cancellata e ricompare la schermata di accesso: è il modo in cui un cambio
password propaga l'uscita a tutti i dispositivi.

---

## 9. Gli invarianti — le cose che non si possono rompere

Chi modifica il codice deve poter rispondere di sì a tutte queste.

1. **Un campo nuovo nello stato si aggiunge in `defState()` *e* in `normalize()`.**
   Altrimenti i backup esistenti e i dati dal cloud arrivano senza quel campo.
2. **`S.v` resta 2** finché il formato è compatibile. Se cambia la forma dei
   dati, serve `S.v = 3` e un ramo di migrazione — come `migrateLegacy()`
   (riga 660) fa già per il gestionale precedente.
3. **`src` non si tocca.** È l'unica cosa che distingue un movimento generato
   da uno scritto a mano, e l'unica che rende reversibile `markPaid`/`unPaid`.
4. **`cliReset()` dopo ogni modifica a `S.clienti`.** L'indice è in cache.
5. **`renameCli` deve coprire tutti i posti dove compare un nome cliente.**
   Oggi sono quattro: `mov`, `ric`, `mag.movimenti[].destinazione`, chiavi di
   `scadCan`.
6. **Dopo ogni modifica a `index.html`, alzare `C` in `sw.js`**
   (`nipec-gestionale-v17` → `v18`). Senza questo, i dispositivi che l'hanno
   installata continuano a usare la versione vecchia dalla cache, e non c'è
   modo di accorgersene da fuori.
7. **Non introdurre dipendenze esterne.** Il valore di questo file è che
   funziona offline e senza build. L'unica risorsa remota oggi è il font
   Archivo da Google Fonts, e ha già il ripiego su Helvetica/Arial.
8. **I nomi dei clienti si scrivono sempre tramite `ensureCli()` o `canon()`**,
   mai a mano.

---

## 10. Come si modifica — procedura

Non c'è un repository git: il sito è una copia statica caricata su Netlify.
Finché resta così, la procedura è questa.

1. **Scaricare la versione viva** prima di toccare qualsiasi cosa:
   `curl -o index.html https://cruscottonipec.netlify.app/index.html`
   È l'unica fonte certa di cosa c'è in produzione.
2. **Esportare un backup dei dati** dall'app (Impostazioni → Esporta).
   Produce `nipec-gestionale-backup-AAAA-MM-GG.json`. Da fare *prima*, sempre:
   i dati non stanno nel file HTML, ma un errore di `normalize()` li può
   rendere illeggibili.
3. Modificare `index.html`.
4. **Alzare `C` in `sw.js`** (invariante 6).
5. **Provare in locale** con `python3 -m http.server` e un browser:
   il service worker e `fetch()` non funzionano da `file://`.
6. **Le quattro prove minime**, da rifare a ogni modifica:
   - registrare un'entrata con un cliente nuovo → compare in anagrafica;
   - segnare pagato un canone in Scadenze → nasce il movimento con `src`;
   - annullare lo stesso pagamento → il movimento sparisce;
   - ricaricare la pagina → i dati sono ancora lì, e la pastiglia in alto dice
     *Online*.
7. Caricare su Netlify e **ricaricare l'app due volte** su un dispositivo che
   l'ha installata (la prima volta prende il nuovo service worker, la seconda
   serve la nuova versione).

**La cosa da sistemare per prima, prima ancora delle modifiche:** mettere
questo file in un repository git. Senza, ogni modifica è irreversibile e due
persone che lavorano insieme si sovrascrivono a vicenda.

---

## 11. Problemi aperti

Ordinati per quanto fanno male, non per quanto sono difficili.

### 11.1 · ALTO — La parola d'ordine è l'unica difesa, e il bersaglio è pubblico

L'indirizzo dello script Apps Script è scritto in chiaro dentro `index.html`,
che è una pagina pubblica. Chiunque apra il sorgente lo legge. Da quel momento
l'unica cosa che protegge **tutta la contabilità di NIPEC, Italia e Albania,
con le anagrafiche fiscali dei clienti** è una parola d'ordine di almeno sei
caratteri, inviata nel corpo di un POST.

Quello che manca, lato Apps Script (che non ho potuto leggere — non è
pubblicato):
- un limite ai tentativi, o una pausa crescente dopo gli errori;
- un registro degli accessi;
- una parola d'ordine lunga.

**Primo passo, costa niente:** una parola d'ordine lunga e inventata, non una
parola di senso compiuto. Il minimo di sei caratteri nel codice è troppo basso
per quello che protegge.

Inoltre la parola d'ordine è salvata **in chiaro** in `localStorage`
(`nipec_sync_cfg`). Chi ha accesso fisico al dispositivo sbloccato la legge in
tre secondi dalla console. È il compromesso che permette di non reinserirla
ogni volta; va saputo, non necessariamente cambiato.

### 11.2 · ALTO — Nessun repository, nessuna storia

Il sito è una copia statica. Non si può vedere cosa è cambiato, non si può
tornare indietro, non si può lavorare in due. Questa è la causa prima di cui
quasi tutti gli altri problemi sono sintomi.

### 11.3 · MEDIO — La riconciliazione automatica può sbagliare in silenzio

Vedi §7.1. Un'entrata che coincide per mese, categoria e cliente viene letta
come il canone pagato anche se non lo è. Non c'è modo di smentirla
dall'interfaccia, e il risultato è una scadenza che risulta pagata quando non
lo è. Servirebbe almeno un modo di dire "questo incasso non c'entra".

### 11.4 · MEDIO — Il trasferimento PC → telefono è morto

`receiveFromPC()` esiste, è scritto bene (PBKDF2 + AES-GCM, gzip opzionale),
ma `dati-telefono.enc` **risponde 404**. La funzione è raggiungibile
dall'interfaccia e fallisce con "Nessun pacchetto dati disponibile". Due
strade: rimuoverla, oppure ripristinare lo strumento che genera quel file.
Oggi non fa che confondere.

### 11.5 · MEDIO — L'aggancio dei noleggi dipende da come si scrive una causale

Vedi §5.4. `/noleggio/i` e `/rientro/i` su un campo libero. Una causale scritta
diversamente fa sparire la macchina dai noleggi attivi e quindi dallo
scadenziario — cioè smette di fatturare, senza nessun avviso. Andrebbe
sostituito con un valore scelto da un elenco.

### 11.6 · BASSO — Cose morte o incoerenti

- `S.gen` è dichiarato in `defState()` e **non viene usato da nessuna parte**.
- Rinominare una categoria lascia indietro i movimenti vecchi (§7.3).
- I canoni 500 e 400 della Diagnosi sono scritti nel codice (§7.5).
- `thrNum()` (riga 1080) contiene `.map((x,i) => i<2 ? x : x)`, che restituisce
  sempre `x`: è un'operazione che non fa niente.
- Il dizionario delle città (`cittaDict`, riga 1361) è una lista scritta a mano
  di una trentina di comuni; `guessCity` ci pesca dentro e marca il risultato
  con `luogoDedotto: 1`. Va bene come scorciatoia, ma non cresce da solo.

---

## 12. Da riempire — domande e modifiche

Questa sezione è vuota apposta.

### 12.1 Domande sul funzionamento

> Scrivere qui le domande, una per riga, indicando la sezione di questo
> documento o il numero di riga del codice a cui si riferiscono. Esempio:
> *"§7.1 — se un cliente paga in due volte nello stesso mese, cosa succede?"*

-
-
-

### 12.2 Modifiche richieste

Per ciascuna, servono tre cose, altrimenti non è una richiesta ma un desiderio:

| # | Cosa deve cambiare | Perché (il problema vero) | Come si vede che è fatto |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |

### 12.3 Priorità

> Delle modifiche sopra, quale **una** va fatta per prima, e cosa succede
> se non si fa.

---

## 13. Riassunto in dieci righe

- Un solo file HTML di 196 KB: markup, stile e logica insieme, nessun build.
- Tutto lo stato in un oggetto `S`, salvato in due chiavi di `localStorage`.
- Sincronizzazione via Google Apps Script su Drive, ogni 60 secondi, con
  controllo di revisione e gestione dei conflitti.
- Una parola d'ordine, uguale su tutti i dispositivi. È l'unica difesa.
- Otto schede, un filtro paese Italia / Albania che le attraversa tutte.
- L'anagrafica clienti con gli alias è il collante fra contabilità, magazzino
  e scadenze.
- Lo scadenziario nasce da due sorgenti — contratti e noleggi di magazzino —
  con una regola di precedenza per non fatturare due volte.
- Giacenze e noleggi non sono memorizzati: si ricalcolano dai movimenti.
- La Diagnosi è un questionario a sei pilastri con soglie semaforiche, separato
  dalla contabilità.
- **Le due cose da sistemare prima di tutto: un repository git, e una parola
  d'ordine seria.**

---

*Documento ricavato leggendo il sorgente pubblicato il 20 ottobre 2026.
Ogni riferimento di riga vale per quella versione. L'indirizzo dello script
Apps Script è stato troncato di proposito: si legge nel sorgente.*
