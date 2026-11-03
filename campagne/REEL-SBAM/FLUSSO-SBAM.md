# Reel NIPEC · SBAM · dal copione al montaggio

**Seconda stesura · 3 novembre 2026.** Ventiquattro reel: dodici per le inserzioni (adv), dodici per la pagina social.

Scritto per essere letto da chi parte da zero, **anche da un Claude che non ha visto nessuna delle conversazioni precedenti**.
Tutto quello che serve sta nel pacchetto (`fai-pacchetto.py` lo costruisce da questa cartella). Niente sta "nella chat".

---

## 0. Se sei il Claude che monta: leggi questo per primo

**Chi sei in questa storia.** Sei il Claude Code che Eros ha messo come amministratore nel canale Telegram dove lavorate in tre:
**Giorgio Petrelli** (NIPEC), **Eros** e tu. Nel canale fai i lavori. In Albania gira **Uarda**, che mette i suoi video nello stesso canale (da confermare).

**Da dove arriva questa cartella.** La prepara l'altro Claude, quello di NIPEC, con Giorgio. Quel Claude **non è nel canale** e non vede quello che fai tu.
Per questo qui c'è scritto tutto.

**Cosa devi fare.** Montare ogni reel secondo il suo copione, partendo dagli stacchi che Giorgio e Uarda mettono nel canale (e dalla voce fuori campo), e rimettere nel canale il reel montato.

**Come leggere, in questo ordine:**
1. questo file;
2. `copioni/00-LEGGIMI.md`: l'indice dei ventiquattro reel, le regole, come si fa lo SBAM;
3. il copione del reel che stai montando: `copioni/l1-adv-….md`, `p1-pagina-….md`. È scritto **stacco per stacco**: tempo, inquadratura, cosa si vede, cosa si dice, cosa appare scritto, che suono c'è;
4. `suoni/LEGGIMI.txt` e `musica/LEGGIMI.txt`, quando arrivi al suono;
5. `VENTIQUATTRO-REEL-SBAM.pdf` solo se ti serve il contesto (è la stessa cosa dei copioni, stampata).

**Se qualcosa manca o non torna:** non inventare. Scrivi a Giorgio nel canale **una domanda sola, precisa**. Esempi: «in L1-2 il calendario si vede ma lo strappo non si sente: uso il colpo di `suoni/sbam.wav`?»,
«in P4 la voce dello stacco 6 è più lunga dello stacco: lo allungo a 4 s?».

**Cosa rimandi nel canale:** il video montato con la didascalia `REEL L1 · montato`, e sotto, in poche righe, **quello che non hai potuto fare o hai dovuto scegliere**.

**Cosa non cambi mai:** le parole dette, i prezzi, le scritte a schermo, la parola chiave, i numeri di telefono. Se ti sembra sbagliato, lo dici a Giorgio; non lo correggi.

---

## 1. In una frase

Giorgio e Uarda girano i reel seguendo il piano delle riprese e li mettono nel canale Telegram; il Claude di Eros li monta secondo il copione, con lo SBAM, la musica e la scheda finale, e li rimette nel canale per essere approvati.
**Dodici reel (serie A) servono per le inserzioni del noleggio di laser e di Afrodite; dodici (serie B) per la pagina Instagram/Facebook di NIPEC.**

## 2. Cosa c'è nel pacchetto

| Cosa | Dove sta |
|---|---|
| Questo file | `FLUSSO-SBAM.md` |
| I ventiquattro copioni, stacco per stacco | `copioni/l1-adv-….md` … `p12-pagina-….md`, indice in `copioni/00-LEGGIMI.md` |
| I testi delle inserzioni (serie A) | `copioni/INSERZIONI.md` (gli stessi sono in fondo a ogni copione) |
| Le didascalie della pagina (serie B) | `copioni/PAGINA.md` |
| Il piano delle riprese | `PIANO-RIPRESE.pdf` e `piano-riprese.md`: i nomi dei file che arrivano («L1-2») e le battute fuori campo |
| I suoni dello SBAM | `suoni/` (cinque file `.wav`, senza diritti) |
| La base musicale | `musica/musica-base-24s.wav`, e `musica/musica.py` per rifarla più lunga o più corta |
| Le schede finali, PNG 1080 × 1920 | `schede-finali/` (cinque) |
| Logo, carattere dei testi a schermo e colori | `grafica/` |
| Come abbiamo montato un reel con ffmpeg | `riferimento-tecnico/` (solo da leggere) |
| Il contesto della campagna pubblicitaria | `CAMPAGNA-500-laser-e-afrodite.pdf` |

## 3. A cosa servono (serie A, adv)

Dal documento della Campagna 500. Chi monta non decide niente di questo, ma deve sapere perché i reel sono fatti così.

| | |
|---|---|
| **L'offerta** | 500 € al mese (in Albania 50.000 lekë), nessun vincolo, zero anticipo, zero cauzione. Il dispositivo arriva il 1, si paga entro il 30. |
| **Dove porta l'inserzione** | Su **WhatsApp**, non su una pagina web. Il pulsante è «Invia messaggio»; nel messaggio c'è la **parola chiave** (`LASER` o `AFRODITE`). |
| **Chi risponde** | Italia: Giorgio, +39 351 846 6025. Albania: Uarda, +355 69 212 9786. |
| **Dove** | Italia: Roma e 40 km intorno. Albania: Tiranë, Durrës, Shkodër, Elbasan, Vlorë, Peshkopi. |
| **Chi parte per prima** | **L'Italia**. Poi l'Albania. **Afrodite** circa due settimane dopo il laser, **in Italia e in Albania** (deciso il 2 novembre). |
| **Nome del laser** | Nelle inserzioni **non si nomina il modello**. Niente diodi, niente watt. |

**Cosa non va in un'inserzione** (è il motivo di rifiuto numero uno su Meta): pelle trattata, prima/dopo, percentuali di risultato, tempi di risultato.

Serie B (pagina): non vendono. Servono a far fermare il dito e a far ricordare chi siamo. **La pagina NIPEC deve avere almeno sei pubblicazioni prima di poter sponsorizzare:** i primi sei reel della serie B (P1, P5, P2, P3, P4, P6) sono quelle sei.

## 4. Regole di montaggio, uguali per i ventiquattro

### La regola dei 5 secondi, in due metà, e SBAM

1. **I primi 5 secondi** contengono il vantaggio intero. La voce parte entro 0,5 s.
2. **Nessuno stacco dura più di 5 secondi.** Dopo, si cambia stacco **e inquadratura**. Mai due inquadrature uguali di fila.
3. **SBAM.** Ogni reel ha un colpo o una sorpresa entro i primi 3 secondi: è quello che ferma il dito.

Le quattro inquadrature: **primo piano** (il viso), **mezzo busto** (dalla vita in su), **dettaglio** (mani o oggetto, da vicino), **campo largo** (la persona e il dispositivo nell'ambiente).

- **Se non c'è un'altra ripresa**, si cambia inquadratura ingrandendo (zoom) la stessa ripresa: conta come stacco nuovo.
- **Se la voce non sta nel tempo dello stacco:** non accelerare. Se manca meno di mezzo secondo, allunga lo stacco; se manca di più, **allunga fino a 5 secondi al massimo** e avvisa Giorgio nel rimando; oltre i 5 si divide in due stacchi, il secondo con un'altra inquadratura (zoom).
- Il logo **non** compare nei primi cinque secondi. Compare solo nella scheda finale.

### Come si fa lo SBAM

- **Cos'è.** Un colpo secco, in immagine e in suono, che cade entro i primi 3 secondi. Serve a una cosa sola: fermare il dito che scrolla.
- **Suono.** Un colpo breve e grave (0,3 s), seguito da mezzo secondo di silenzio: il silenzio è quello che lo fa sentire. Dove c'è un suono vero (portellone, palmo sul tavolo, timbro, strappo di fogli, notifica) si usa quello, alzato in montaggio. Altrimenti un colpo senza diritti: si può generare.
- **Immagine.** Un lampo bianco di 2 fotogrammi (a 30 fps), la scossa dell'inquadratura per 6 fotogrammi, e la scritta che arriva al 130% e si assesta al 100% in 4 fotogrammi.
- **Quanti.** Al massimo due per reel. Quattro, tre o dieci colpi a ritmo (F2, L6, F5) contano come uno.
- **Con la musica.** La base musicale si ferma 0,2 s prima del colpo e riparte subito dopo.
- **Sicurezza.** Niente si rompe e niente cade davvero: i manipoli e il dispositivo si appoggiano piano, il colpo lo mette il montaggio. Al massimo un lampo bianco al secondo, per chi è sensibile alla luce.
- **Mai.** Urla, glitch continui, scritte che tremano per tutto il reel. Il colpo è uno: il resto sta fermo.

### Le regole dei copioni, applicate a tutti

- Il vantaggio intero sta nei primi 5 secondi; la voce parte entro 0,5 s.
- SBAM entro i primi 3 secondi, al massimo due per reel; mezzo secondo di silenzio dopo il colpo.
- Nessuno stacco oltre 5 secondi; mai due inquadrature uguali di fila.
- Parlato sotto le 2,5 parole al secondo, verificato stacco per stacco.
- Parole evitate: «macchina», «LED», «cavitazione», percentuali, prima/dopo, modello del laser, diodi, watt. Nessun volto senza consenso.
- Forme dirette: «Chiama o scrivi su WhatsApp», mai l'imperativo con «ci» (scrivici, seguici…).
- Ogni dato che non risulta nei documenti di NIPEC è segnato «da confermare».

### Formato e durata

- Verticale **9:16, 1080 × 1920**, 30 fotogrammi al secondo, H.264 (profilo high), AAC 160 kbps, `+faststart`.
- Il copione dura tra 15 e 22 secondi (è contato stacco per stacco). Poi viene la **scheda finale, 2 secondi**.
- **Il peso:** Telegram, con un bot, permette di scaricare file fino a circa 20 MB e di inviarne fino a circa 50 MB. Se il tuo accesso ha un limite, dillo a Giorgio: si manda una versione più leggera. Non abbassare la risoluzione prima di averlo detto.

### Scritte a schermo

- Entrano **insieme alla parola** che dicono, non prima. Se una riga ha «poi:», la seconda parte entra dopo la prima.
- Carattere **Archivo grassetto, bianco**, su una banda **blu profondo `#123A63`** (quasi opaca, angoli arrotondati). Mai sopra la pelle di una persona. Mai effetti, mai i colori della bandiera.
- Come punto di partenza: la scritta del gancio, corpo 70, a circa 1010 px dall'alto; le altre, corpo 56, a circa 1330 px. In `riferimento-tecnico/sovrapposizioni.mjs` c'è un esempio funzionante.
- Le righe del copione sono righe separate: vanno a capo dove vanno a capo nel copione.
- Restano nella fascia centrale: **i primi 250 e gli ultimi 340 pixel** li copre l'interfaccia di Instagram.

### Sottotitoli

- Sempre, nella lingua in cui si parla. **Riportano quello che si sente davvero.** Se Uarda dice una cosa diversa dal copione, vale quello che dice.
- Il copione albanese è scritto in italiano, con le versioni albanesi in bozza: da far controllare a Uarda prima di usarle.

### Voce e musica

- Le battute in primo piano e in mezzo busto si dicono in camera (audio originale, pulito). Le battute dei dettagli e dei campi larghi sono **fuori campo**: Giorgio le registra a parte e le metti sotto l'immagine; sono elencate in `piano-riprese.md`, blocco V.
- La base musicale sta sotto la voce, **bassa** (circa −19 LUFS), e **si ferma 0,2 s prima del colpo**, riparte subito dopo. Quando parla qualcuno, la musica si abbassa ancora.
- **Dopo il colpo, mezzo secondo di silenzio**, poi la voce (dove il copione dice «voce da 0,5 s» la voce parte mezzo secondo dopo il colpo).
- Si usa il suono vero (portellone, palmo sul tavolo, timbro, strappo, notifica) e si mette sotto il colpo di `suoni/`, mai al posto se il vero si sente bene.

### Scheda finale

- Subito dopo l'ultima parola, a tutto schermo, ferma **2 secondi**. Niente altro sopra.
- Ce ne sono cinque, già pronte, in `schede-finali/`:

| Reel | Titolo | Scheda finale · Italia | Scheda finale · Albania |
|---|---|---|---|
| L1 | Trenta pagine in un colpo | `scheda-finale-LASER-italia.png` | `scheda-finale-LASER-albania.png` |
| L2 | Fermo | `scheda-finale-LASER-italia.png` | `scheda-finale-LASER-albania.png` |
| L3 | Ti sta guardando | `scheda-finale-LASER-italia.png` | `scheda-finale-LASER-albania.png` |
| L4 | Quanto costa un laser? | `scheda-finale-LASER-italia.png` | `scheda-finale-LASER-albania.png` |
| L5 | Il foglio che strappo | `scheda-finale-LASER-italia.png` | `scheda-finale-LASER-albania.png` |
| L6 | Tre cose, un prezzo | `scheda-finale-LASER-italia.png` | `scheda-finale-LASER-albania.png` |
| F1 | Non comprare Afrodite | `scheda-finale-AFRODITE-italia.png` | `scheda-finale-AFRODITE-albania.png` |
| F2 | Quattro colpi | `scheda-finale-AFRODITE-italia.png` | `scheda-finale-AFRODITE-albania.png` |
| F3 | I compiti già fatti | `scheda-finale-AFRODITE-italia.png` | `scheda-finale-AFRODITE-albania.png` |
| F4 | Una riga in più nel listino | `scheda-finale-AFRODITE-italia.png` | `scheda-finale-AFRODITE-albania.png` |
| F5 | Dieci timbri | `scheda-finale-AFRODITE-italia.png` | `scheda-finale-AFRODITE-albania.png` |
| F6 | Una parola sola | `scheda-finale-AFRODITE-italia.png` | `scheda-finale-AFRODITE-albania.png` |
| P1 | Fermo. Non firmare. | `scheda-finale-PAGINA.png` | `scheda-finale-PAGINA.png` (P4, P7, P9; gli altri solo Italia) |
| P5 | Falso | `scheda-finale-PAGINA.png` | `scheda-finale-PAGINA.png` (P4, P7, P9; gli altri solo Italia) |
| P2 | Sotto il telo | `scheda-finale-PAGINA.png` | `scheda-finale-PAGINA.png` (P4, P7, P9; gli altri solo Italia) |
| P3 | L'esame | `scheda-finale-PAGINA.png` | `scheda-finale-PAGINA.png` (P4, P7, P9; gli altri solo Italia) |
| P4 | Cosa c'è nella scatola | `scheda-finale-PAGINA.png` | `scheda-finale-PAGINA.png` (P4, P7, P9; gli altri solo Italia) |
| P6 | Cinque secondi | `scheda-finale-PAGINA.png` | `scheda-finale-PAGINA.png` (P4, P7, P9; gli altri solo Italia) |
| P12 | Tre cose che non ti diremo | `scheda-finale-PAGINA.png` | `scheda-finale-PAGINA.png` (P4, P7, P9; gli altri solo Italia) |
| P9 | Cinque risposte | `scheda-finale-PAGINA.png` | `scheda-finale-PAGINA.png` (P4, P7, P9; gli altri solo Italia) |
| P7 | Rispondo io | `scheda-finale-PAGINA.png` | `scheda-finale-PAGINA.png` (P4, P7, P9; gli altri solo Italia) |
| P8 | Cosa manca? | `scheda-finale-PAGINA.png` | `scheda-finale-PAGINA.png` (P4, P7, P9; gli altri solo Italia) |
| P10 | Il rumore | `scheda-finale-PAGINA.png` | `scheda-finale-PAGINA.png` (P4, P7, P9; gli altri solo Italia) |
| P11 | La polvere | `scheda-finale-PAGINA.png` | `scheda-finale-PAGINA.png` (P4, P7, P9; gli altri solo Italia) |

### Non si mostra mai

Pelle trattata, prima/dopo, percentuali di risultato, tempi di risultato. Nessuna cliente in campo, nessun volto senza consenso.

### Prima di rimandare, controlla

1. Il vantaggio intero sta nei primi 5 secondi, e la voce parte entro 0,5 s.
2. Il colpo cade entro i 3 secondi (il copione dice a che secondo), con il mezzo secondo di silenzio dopo.
3. Nessuno stacco oltre i 5 secondi; mai due inquadrature uguali di fila.
4. Le scritte sono quelle del copione, scritte uguali, entrano con la parola.
5. Il copione dura da 15 a 22 secondi, più 2 di scheda finale; il logo non c'è nei primi 5 secondi.
6. L'invito finale è quello del copione (serie A: «Chiama o scrivi su WhatsApp» con la parola chiave).
7. Sottotitoli presenti, dentro la fascia sicura.

## 5. Come arrivano i video e come tornano

- Ogni stacco girato arriva nel canale come **video verticale**, con una didascalia sola: il codice del reel e il numero dello stacco, **`L1-2`** (reel L1, stacco 2). Se c'è più di una ripresa: `L1-2 · ripresa 2`.
- La voce fuori campo arriva come messaggio vocale o audio, con la didascalia **`L1-2 · voce`**. Se è un messaggio solo con più battute, le battute sono nell'ordine di `piano-riprese.md`, blocco V.
- Una registrazione dello schermo del telefono (F6, P7) arriva come video, con il codice dello stacco.
- Il montato torna nel canale con la didascalia **`REEL L1 · montato`**. Per l'Albania, **`REEL L1 · Albania · montato`**.
- Il copione dice il tempo di ogni stacco: è il tempo del montato, non della ripresa. Le riprese sono più lunghe (un secondo prima, un secondo dopo): tagli tu.

## 6. Ordine di uscita (proposta)

- **Prima la pagina.** Serie B: i primi sei reel (P1, P5, P2, P3, P4, P6) sono le sei pubblicazioni che la pagina NIPEC deve avere prima di poter sponsorizzare (Campagna 500). Due a settimana. Gli altri sei (P12, P9, P7, P8, P10, P11) continuano il ritmo.
- **Poi il laser.** Serie A, laser, Italia per prima: L1 (dice tutta l'offerta nei primi 5 secondi), poi L4, L2, L5, L3, L6. L'Albania segue con gli stessi, detti da Uarda.
- **Dopo due settimane, Afrodite, in Italia e in Albania.** F1, F6, F2, F4, F3, F5. Stesso criterio: i più netti per primi.

## 7. Per l'Albania

- **Chi parla.** Uarda. Il copione resta in italiano finché il testo albanese non è approvato; i sottotitoli riportano quello che si sente davvero. Le versioni albanesi sono bozze: da far controllare a Uarda prima dell'uso.
- **Il prezzo.** «500 € / MESE» diventa «50.000 LEKË / MUAJ»; a voce «cinquantamila lekë al mese».
- **L1, stacco 3.** «prima del primo euro» diventa «para lekut të parë».
- **Il numero.** WhatsApp di Uarda: +355 69 212 9786. In P4 e P7 è il numero sul foglietto e sullo schermo.
- **Le parole di Afrodite.** In F2 la scritta «ULTRASUONO FOCALIZZATO DIREZIONALE» in albanese è «ULTRATINGULL I FOKUSUAR»: da far controllare a Uarda.
- **La parola chiave.** Resta LASER o AFRODITE, scritta così in WhatsApp.
- **Afrodite in Italia.** Stessi copioni, stesso prezzo (500 € al mese), parla Giorgio. Numero: +39 351 846 6025.

## 8. Da chiarire

1. **Dove finiscono i reel approvati.** Giorgio aveva parlato di una cartella assegnata per ricevere foto e video. Quale? Chi ci mette i file?
2. **Il testo albanese.** Chi lo approva, e quando? Le versioni dei copioni sono bozze.
3. **«Esame finale» e «certificato»** (P3, P9): descrivono il percorso DEMETRA, ma non risultano nei documenti. Da confermare con DEMETRA prima di pubblicare.
4. **«Chiama o scrivi»** nelle inserzioni: il pulsante di Meta resta «Invia messaggio». Da confermare con Giorgio se si può chiamare anche il numero.
5. **«Quel mese non lo paghi»** (se chiudi ad agosto), L1 e L5: condizione commerciale, da confermare con Giorgio prima di girare.
6. **Dove si carica l'inserzione e chi lo fa:** Gestione inserzioni di Meta, caricata da Giorgio? I testi sono pronti: `copioni/INSERZIONI.md`.
7. **Come si pubblica sulla pagina** (serie B): Giorgio, o il canale? Per ora «pubblicare» vuol dire farlo vedere a Giorgio e a Eros per approvarlo.

## 9. Registro di quello che ha detto Giorgio

**22–23 ottobre 2026**
- I reel si montano con la **regola dei 5 secondi**: nessuno stacco più di 5 secondi, poi si cambia stacco e inquadratura.
- L'Italia parte per prima. «Cavitazione» diventa «ultrasuono focalizzato direzionale»; «LED» diventa «low laser».
- Eros ha fatto un canale Telegram con Giorgio e il Claude Code di Eros come amministratore: lì si fanno i lavori.

**29 ottobre 2026**
- Si dice «dispositivo», non «macchina». La base musicale sotto i reel. Sotto DEMETRA si scrive «Synergia», non «360° Transformation».

**2 novembre 2026**
- Afrodite parte anche in Italia, non solo in Albania.
- Servono più di dodici reel: da dodici a ventiquattro (dodici adv, dodici pagina).
- In P4, per l'Albania, il foglietto ha il numero di Uarda.
- I reel devono rompere gli schemi e giocare sull'effetto SBAM o sull'effetto sorpresa, sempre con la struttura dei 5 secondi.
