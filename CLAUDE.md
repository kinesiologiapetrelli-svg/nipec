# NIPEC — memoria di progetto

Contesto permanente per ogni sessione. Titolare: Giorgio Petrelli
(`kinesiologiapetrelli@gmail.com`). Referente operativa: Uarda
(`nipecuarda@gmail.com`). Lingua di lavoro: **italiano**; parte del materiale
va prodotto anche in **albanese**.

---

## 1. Principio di Analisi Petrus — la lente

Dodici precetti da applicare prima di ogni decisione o analisi.
*Non correggere il pensiero: arreda il contesto perché dia il meglio.*

1. Parti sempre da **chi hai davanti**: bisogni, valori, paure — prima della mossa.
2. **Inverti.** Chiediti come fallisce, non solo come riesce, ed evita il disastro.
3. Ragiona con **più modelli mentali** — psicologia, probabilità, fisica, biologia, economia. Mai un martello solo.
4. Cerca il **Lollapalooza**: dove più forze convergono e si moltiplicano.
5. Filtra ogni scelta con le **25 tendenze psicologiche**: incentivi, riprova sociale, avversione alla perdita, autorità.
6. **Fatti verificati** prima delle opinioni.
7. **Strategia prima della tattica**: prima il perché, poi gli strumenti.
8. Leggi denaro e ruoli col **Quadrante E/S/B/I**: dove sta, dove può spostarsi. Asset contro passività.
9. **Fai più con meno.** Cerca la sinergia di sistema; progetta il contesto invece di predicare.
10. Pensa agli **effetti di secondo e terzo ordine**: «e poi cosa succede?»
11. Chiudi ogni analisi in una **raccomandazione netta più una domanda**.
12. Aiuta a **chiudere e a esternalizzare**, non ad aprire.

Provenienza: Munger · Kiyosaki · Fuller, più il metodo operativo di Giorgio.

**Come si traduce nel lavoro con lui:** ogni risposta finisce con una
raccomandazione netta e una sola domanda. Mai un ventaglio di opzioni
equivalenti — quello apre, non chiude.

---

## 2. Profilo cognitivo — come consegnare il lavoro

Motore 88 / Attrito 75. Canali accesi: novità 90, iperfocus 90, slancio 85,
fiuto business 85; funzioni esecutive 80, attenzione 75, emozioni 70.
Sintesi: **motore da corsa, guardrail deboli.** La crescita non passa da più
gas: passa dai freni — persone, automazioni, regole di chiusura.

Sei guardrail da rispettare quando gli si consegna qualcosa:

1. **Uno entra, uno esce** — non proporre progetti nuovi se non se ne chiude uno.
2. **L'iperfocus va prenotato** — il lavoro ad alto valore in blocchi, non a spizzichi.
3. **Esternalizza l'esecutivo** — ciò che non entra in un sistema, per lui non esiste. Checklist, promemoria, automazioni.
4. **Un solo raccoglitore di idee** — le idee nuove si annotano, non si aprono.
5. **Deadline vere, non intenzioni** — una data comunicata a qualcuno, non un promemoria rimandabile.
6. **La critica è un dato, non una ferita** — 24 ore prima di rispondere a caldo.

**Regola operativa:** consegne corte, una cosa alla volta, con la data.
Niente elenchi di opzioni. Niente lavoro lasciato "da rifinire".
Se una cosa è bloccata, dirlo subito e in chiaro — non annegarla in fondo.

---

## 3. Lo stack NIPEC

**Cos'è.** NIPEC noleggia tecnologie estetiche (Laser Ares/Uriel, Afrodite
VS++) ai centri e fornisce, insieme alla macchina, il sistema per farla
rendere: protocolli, formazione a tappe, e un cruscotto clienti.

**Le tre frasi del progetto:**
- «Usarlo bene è più facile che usarlo male.»
- «Prima di chiamarmi, tre controlli.»
- «Se serve, io ci sono.»

**Contatti (sempre così, col prefisso internazionale):**
Assistenza IT +39 351 846 6025 · AL +355 69 212 9786

### L'architettura del cruscotto

```
NIPEC_MASTER_Centri  ──IMPORTRANGE──▶  RIEPILOGO di ogni cruscotto centro
   (solo numeri,                          (CLIENTI → RIEPILOGO → IMPOSTAZIONI)
    mai nominativi)
```

- **Un cruscotto per centro**, in due varianti: `CENTRO` (estetica generica,
  percorsi) e `LASER` (ciclo 12 sedute, finestra di rientro 28 giorni,
  mantenimento a 90 giorni, tre incentivi).
- **Il MASTER funziona SOLO come Foglio Google** — usa IMPORTRANGE, che in
  Excel non esiste. Stessa cosa per i cruscotti che deve leggere:
  IMPORTRANGE non legge un `.xlsx`, legge solo Fogli Google nativi.
- **Regola invalicabile:** nel MASTER non entrano mai nomi di clienti dei
  centri. Solo numeri di sintesi. È la promessa scritta in ogni LEGGIMI
  («NIPEC non contatta mai le tue clienti»); se si rompe, si rompe
  l'adozione di tutto il sistema molto prima di qualsiasi problema legale.

### Il portale centro (Netlify)

Una cartella per centro, caricata su Netlify in drag&drop. Struttura:
`index.html` · `netlify.toml` · `netlify/edge-functions/accesso.js` (gate di
accesso) · `_centri.csv` e `_genera-centri.py` (generatore) ·
`_CREDENZIALI.txt` (**contiene segreti — non aprire, non copiare, non
pubblicare**).

In `index.html` l'**unica parte da cambiare per ogni centro** è il blocco
`const CENTRO = {…}`: `nome`, `citta`, `titolare`, `foglio` (link del Google
Foglio), `gidClienti`, `gidRiepilogo`, `referente`, `whatsapp`.
Il segnaposto di fabbrica è `INCOLLA-QUI-IL-LINK`: finché resta, la pagina
disattiva i tre pulsanti e mostra un avviso. I `gid` sono i numeri dopo
`#gid=` nell'URL quando si è sulla pagina CLIENTI / RIEPILOGO.

Condivisione dei fogli: **sempre "Persone specifiche"**, mai "Chiunque abbia
il link".

### La rubrica NIPEC (l'app «alert»)

Non è il cruscotto di un centro: è la rubrica interna NIPEC, 1005 contatti.
Ogni lunedì dice **chi chiamare**, in ordine di priorità P1→P5
(P1 noleggio attivo freddo da 4 mesi · P2 cliente perso 6 mesi–5 anni ·
P3 contatto caldo fermo da 1 mese · P4 chi ha comprato la macchina, target
DEMETRA · P5 richiesta info vecchia di 1 anno).

Posizione unica, dal 24-08-2026 — `Drive → 4 · CLIENTI E CENTRI → RUBRICHE`:

```
RUBRICHE/                    ← condivisa con nipecuarda@gmail.com (Editor)
├── NIPEC/
│   ├── RUBRICA NIPEC.html   l'app (134 KB)
│   ├── rubrica-nipec.json   i dati, 1005 contatti
│   ├── LEGGIMI - come si usa.txt
│   ├── DA-CARICARE-SU-NETLIFY/
│   └── _vecchie-versioni/
└── MAJA/
```

Ogni rubrica nuova va dentro `RUBRICHE/`: eredita la condivisione.

**Come funziona, e qual è il limite.** L'app è un singolo HTML che si apre
in locale (Chrome/Edge) e scrive con la File System Access API dentro
`rubrica-nipec.json`. La sincronizzazione fra Giorgio e Uarda la fa **Google
Drive per desktop**, non l'app: quindi serve Drive installato e la cartella
sincronizzata in locale — vederla dal browser non basta.

**Il passaggio che blocca sempre:** Drive per desktop **non sincronizza
«Condivisi con me»**. Chi riceve la condivisione deve fare tasto destro
sulla cartella → *Organizza* → *Aggiungi scorciatoia a Drive* → *Il mio
Drive*. Finché non lo fa, la cartella sul suo computer non esiste e l'app
non può aprirla. Istruzioni complete in `PER UARDA - primo avvio.txt`.

Conseguenza da non dimenticare: **non è lavoro simultaneo.** Drive non
fonde le modifiche, tiene l'ultima versione. Chi apre preme sempre prima
`Dati → Ricarica dal file`, e ci si avvisa su WhatsApp («entro io» / «ho
finito»). Se servirà davvero il lavoro a due in contemporanea, l'unica
strada è cambiare il magazzino dei dati (Foglio Google o un piccolo
backend), non aggiustare l'app.

---

## 4. Stile delle consegne

Documenti a pagina singola HTML, autoconsistenti, in italiano.
Riferimento in questo repo: `PERSELOPE.html`.

- Font: Archivo (sans) + Source Serif 4 (serif), da Google Fonts.
- Palette: navy `#123a63`, blu `#1c6ea4`, con varianti allerta/avviso/ok.
- Tema chiaro **e** scuro: token su `:root`, ridefiniti sotto
  `@media (prefers-color-scheme:dark)` con guardia
  `:root:not([data-theme="light"])` **e** sotto `:root[data-theme="dark"]`.
- Sempre un blocco `@media print` che funzioni davvero: è materiale che si stampa.
- Nomi delle classi CSS **in italiano** (`.foglio`, `.testata`, `.passo`,
  `.riquadro`, `.avvertenza`). Mantenere la convenzione.
- Registro: diretto, concreto, niente gergo da consulente. Frasi corte.
  I numeri e le date sempre espliciti.

---

## 5. Limiti dell'ambiente remoto

- `nipec-alert1.netlify.app` (e in genere Netlify) è **bloccato dal proxy di
  rete**: non si può né leggere né pubblicare il sito da qui. I sorgenti si
  leggono dal Drive.
- **Non c'è accesso a Netlify**: il deploy resta sempre un drag&drop di
  Giorgio.
- Condividere un file di Drive con un indirizzo esterno può essere bloccato
  dal classificatore dei permessi: va chiesto esplicitamente a Giorgio.
- `poppler-utils` non è installato; per leggere i PDF usare `pypdf` in un
  virtualenv.
