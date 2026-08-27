# PERSELOPE — la sequenza di consegna

Trascrizione di `../../PERSELOPE.html`, perché la procedura sia leggibile e
cercabile e non chiusa in una pagina web.

Da «ho deciso di dare la macchina a questo centro» a «il centro è vivo nel
master». **Le prime tre fasi si fanno tutte entro 24 ore.**

| Fase | Dove | Tempo |
|---|---|---|
| **A** | in ufficio, il giorno prima | 25 min |
| **B** | in centro, la consegna | 20 min |
| **C** | in macchina, prima di ripartire | 5 min |
| **D** | dopo 30 giorni | 10 min |

## Le tre cartelle, nell'ordine in cui si usano

**1 · PROCEDURA** — `NIPEC-Prima-Accensione.html`. La consegna in 20 minuti:
script verbatim per l'operativo, le sei obiezioni con la risposta pronta, i
cinque divieti. Si apre dal telefono in centro, oppure si stampa.
*La tesi: il cruscotto non si consegna, si accende.* Tutto converge sul minuto
15 — la titolare chiama una cliente rossa mentre l'operativo è ancora lì. Se
quello non succede, hai consegnato un file.

**2 · FOGLI** — Cruscotto Clienti e Master Centri. Il cruscotto si duplica per
ogni centro: una riga per persona, il rosso si accende da solo. Il master è uno
solo, tuo: una riga per centro, sei numeri di sintesi letti via IMPORTRANGE.
**Nessun nominativo, mai.**

**3 · APP** — `_MODELLO · CENTRI`. Un guscio: brand NIPEC, icona sul telefono,
un pulsante che apre il foglio giusto. Non contiene dati e non ha login — la
serratura è la condivisione del Foglio Google.

### L'ordine giusto per un centro nuovo

1. **Foglio** — duplichi il cruscotto e lo condividi con la titolare.
2. **App** — generi e pubblichi la sua app.
3. **Consegna** — porti la macchina e fai la Prima Accensione.
4. **Master** — torni in ufficio e aggiungi la sua riga.
5. **A 30 giorni** — aprite il cruscotto insieme, al telefono.

---

## Fase A · in ufficio, il giorno prima (~25 min)

Se arrivi al centro senza questa fase finita, la consegna non parte.

### Il foglio

| | Passo | Dettaglio |
|---|---|---|
| **A1** | Duplica il modello | `PERSELOPE\2-FOGLI\NIPEC_Cruscotto_Clienti_CENTRO.xlsx`, salva una copia col nome del centro |
| **A2** | Caricala su Drive | nella cartella dei centri |
| **A3** | Convertila in Foglio Google | tasto destro → Apri con → Fogli, poi File → Salva come Foglio Google. L'xlsx si cestina |
| **A4** | Rinomina | `Cruscotto Clienti - <Nome Centro>` |
| **A5** | Compila IMPOSTAZIONI | solo le celle gialle: nome centro, titolare, soglia richiamo (lascia 30), referente NIPEC. Se il centro fa solo epilazione, sistema la lista TRATTAMENTI |
| **A6** | Togli la riga di esempio | sul foglio CLIENTI: clicca il numero 6 a sinistra, Ctrl+C; clicca il 5, Ctrl+V. **Non cancellare la riga intera: sballa i conteggi del RIEPILOGO** |
| **A7** | Condividi con la titolare come **Editor** | **«Persone specifiche». Mai «Chiunque abbia il link»:** là dentro ci sono i dati delle sue clienti |
| **A8** | Copia il link del foglio | serve in A10 e in C3 |
| **A9** | Segnati i due gid *(facoltativo)* | clicca la scheda CLIENTI e leggi `#gid=NUMERO` nell'indirizzo; ripeti su RIEPILOGO |

### L'app

| | Passo | Dettaglio |
|---|---|---|
| **A10** | Aggiungi la riga al CSV | in `PERSELOPE\3-APP\_MODELLO\_centri.csv`. Campi: `cartella;nome;citta;titolare;foglio;gidClienti;gidRiepilogo;referente;whatsapp`. `cartella` è il nome breve senza spazi (es. `bellezza-taranto`), `foglio` è il link di A8 |
| **A11** | Lancia `_genera-centri.py` | la cartella pronta esce in `PERSELOPE\3-APP\CENTRI\<cartella>\`. Senza Python: duplica `_MODELLO` a mano, cambia il blocco ⚙️ in `index.html`, cancella i tre file che iniziano per `_` e il `LEGGIMI-GIORGIO` |
| **A12** | Pubblica su Netlify | Add new site → Deploy manually. **Trascina la cartella, non i file singoli** |
| **A13** | Nome pulito al sito | Site configuration → Change site name, es. `cruscotto-bellezza-taranto` |
| **A14** | **Prova il link dal tuo telefono** | deve aprirsi, e il pulsante I MIEI CLIENTI deve aprire il foglio. **Adesso, non domani:** se lo scopri in centro, hai bruciato la consegna |
| **A15** | Salva l'indirizzo | scheda del centro, o bozza WhatsApp già pronta |

---

## Fase B · in centro, il giorno della consegna (20 min)

Si fa mentre la macchina si scalda. I minuti sono cumulativi.

**00' · L'aggancio.** Non stai consegnando un file: le stai facendo vedere un
buco che non sapeva di avere.
> «Quante clienti hai che non vedi da sei mesi?»

**Mai dire *gestionale* o *software*. Si dice *rubrica*.**

**02' · L'icona.** Se l'icona non gliela installi tu, quel link non viene
riaperto. Le prendi il telefono tu, apri il link, Aggiungi alla schermata Home,
le mostri l'icona.

**05' · Le prime venti.** Venti bastano: quaranta righe rosse non motivano,
paralizzano. Il tablet lo tieni tu, lei detta dall'agenda. Solo clienti viste
negli ultimi sei mesi. **Ti fermi a venti**, anche se ne avrebbe altre trenta.

**15' · La prima telefonata.** È il cuore della consegna, tutto il resto serve
ad arrivare qui. Apri RIEPILOGO, le fai leggere «Da richiamare», le fai
scegliere la più facile. **Chiama lei, adesso, con te lì che stai zitto.**
Se esci senza che abbia chiamato qualcuno, hai consegnato un file. È l'unico
passaggio che non si recupera con una telefonata dopo.

**18' · Il patto.** Due caselle da aggiornare, non dieci. Appuntamento a 30
giorni fissato sulla sua agenda **prima di uscire**. La frase sulla privacy la
dici tu per primo.

---

## Fase C · in macchina, prima di ripartire (5 min)

Senza questa fase il centro non esiste nel master, e tu non sai più niente di lui.

| | Passo |
|---|---|
| **C1** | Apri il Foglio Google del MASTER CENTRI |
| **C2** | Nuova riga: centro, città, titolare, device, referente, **data consegna** — da lì partono i trenta giorni |
| **C3** | Incolla il link (quello di A8) nella colonna LINK FOGLIO |
| **C4** | **Clicca «Consenti accesso»** sulle celle azzurre che mostrano `#REF!`. Succede una volta sola per centro. **Se non lo clicchi, quel centro resta cieco nel master per sempre** |
| **C5** | Controlla la tua agenda: l'appuntamento a 30 giorni deve stare anche sulla tua |

---

## Fase D · dopo 30 giorni (10 min)

| | Passo |
|---|---|
| **D1** | Apri il master e guarda **GIORNI FERMO**: verde 0-14 sta usando il sistema · giallo 15-30 sta rallentando · rosso oltre 30 ha smesso |
| **D2** | Chiami. Non «come va?», ma «apriamo il cruscotto e guardiamolo insieme» |
| **D3** | Leggete insieme due numeri: quanti sono i DA RICHIAMARE, e qual è il semaforo peggiore |
| **D4** | Concordate **una** azione, una sola, per i prossimi trenta giorni |
| **D5** | Fissi il prossimo appuntamento **prima** di chiudere la telefonata |

---

## I quattro punti dove si rompe tutto

Quattro passi su trenta. Sono questi.

| Passo | L'errore | La conseguenza |
|---|---|---|
| **A7** | Condiviso con «chiunque abbia il link» | I dati delle sue clienti diventano aperti a chiunque |
| **A14** | Link non provato prima | Consegna bruciata in centro, davanti alla titolare |
| **15'** | Nessuna telefonata fatta davanti a te | Hai consegnato un file, non un sistema |
| **C4** | «Consenti accesso» non cliccato | Centro invisibile nel master, per sempre |

---

## I fogli, in breve

Quello che devi sapere a memoria quando la titolare ti chiama.

### Cruscotto Clienti · centro estetico
Schede: LEGGIMI · CLIENTI · RIEPILOGO · IMPOSTAZIONI

Una riga per persona. Le prime cinque colonne sono pensate per lo schermo del
telefono — **Nome · Stato · Ultimo contatto · Giorni · DA RICHIAMARE** — le
altre scorrono a destra.

**DA RICHIAMARE** si accende da solo quando sono passati più giorni della
soglia (default 30), oppure quando l'appuntamento è saltato e restano sedute da
fare. Non si accende mai su «Persa» e «Percorso completato».

Gli otto stati: Da contattare · Contattata · Consulenza fissata · Consulenza
fatta · Percorso attivo · Percorso completato · Dormiente · Persa.

**Lei aggiorna due caselle sole:** Ultimo contatto e Stato. Giallo = lo scrive
lei, grigio = si calcola da solo.

### Cruscotto Clienti · laser
Schede: LEGGIMI · CLIENTI · RIEPILOGO · INCENTIVI · IMPOSTAZIONI

Il laser non ha un ritmo generico, ha **un orologio**: ciclo di 12 sedute,
rientro tra il 21° e il 28° giorno, conferma a −7 e il giorno prima,
mantenimento ogni 90 giorni. I quattro numeri stanno in IMPOSTAZIONI e comandano
tutti gli avvisi.

La colonna che comanda è **COSA FARE OGGI**: si ordina per quella e si lavora
dall'alto.

| Avviso | Significa |
|---|---|
| PRENDI APPUNTAMENTO | È uscita senza il prossimo. **È il buco numero uno** |
| CHIAMA PER CONFERMA | Mancano sette giorni |
| CONFERMA DOMANI | Appuntamento domani: manda l'orario |
| APPUNTAMENTO SALTATO | La data è passata e non è venuta |
| FUORI FINESTRA | Oltre 28 giorni e nessun appuntamento |
| ULTIMA SEDUTA | Si propone mantenimento o una zona nuova |
| RICHIAMO MANTENIMENTO | Tre mesi: chiama e manda l'incentivo |
| RECUPERA CON INCENTIVO | È una persa: si riaccende con un'offerta |

Tre famiglie, tre lavori diversi: **in ciclo** è il fatturato di oggi,
**mantenimento** quello dell'anno prossimo, **perse** sono addormentate, non
morte. Tre incentivi separati, uno per famiglia: se si somigliano, tanto vale
averne uno solo.

> **La regola d'oro: nessuna esce senza il prossimo appuntamento.**
> Sotto il 90% il centro sta perdendo clienti.

### Master Centri
Schede: ISTRUZIONI · CENTRI — **funziona solo come Foglio Google**

Una riga per centro. Le colonne gialle le scrivi tu una volta sola; le azzurre
si riempiono da sole leggendo il RIEPILOGO di quel centro: da richiamare,
persone, nuovi 30 gg, percorsi attivi, da incassare €, ultimo inserimento.
In Excel restano vuote: è normale, non è rotto.

La colonna che conta è **GIORNI FERMO**, tradotta da STATO in
OK ≤ 14 · RALLENTA 15-30 · A RISCHIO > 30. **Un centro che smette di aggiornare
è la disdetta vista con mesi di anticipo.** I rossi sono la lista delle
telefonate, già in ordine di priorità.

Se dopo la conversione le colonne azzurre restano vuote, incolla nella riga 6 e
trascina in basso:

| Cella | Formula | Legge |
|---|---|---|
| I6 | `=IF($H6="";"";IFERROR(IMPORTRANGE($H6;"RIEPILOGO!C5");""))` | da richiamare |
| J6 | `=IF($H6="";"";IFERROR(IMPORTRANGE($H6;"RIEPILOGO!C17");""))` | persone in archivio |
| K6 | `=IF($H6="";"";IFERROR(IMPORTRANGE($H6;"RIEPILOGO!C20");""))` | contatti nuovi 30 gg |
| L6 | `=IF($H6="";"";IFERROR(IMPORTRANGE($H6;"RIEPILOGO!C13");""))` | percorsi attivi |
| M6 | `=IF($H6="";"";IFERROR(IMPORTRANGE($H6;"RIEPILOGO!F5");""))` | da incassare |
| N6 | `=IF($H6="";"";IFERROR(IMPORTRANGE($H6;"RIEPILOGO!C26");""))` | ultimo inserimento |

In Fogli Google il separatore degli argomenti è il **punto e virgola**; in Excel
è la virgola.

> **NIPEC non contatta mai le tue clienti.** Nel master non entrano mai nomi di
> clienti dei centri, solo numeri. È una scelta, non un limite tecnico: se
> quella promessa si rompe, si rompe l'adozione di tutto il sistema — molto
> prima di qualunque problema legale.

---

*NIPEC · Tecnologie Estetiche · assistenza 351 846 6025.*
*«Questo è il ponte: quando DEMETRA 360 sarà in campo, i fogli si spengono.»*
