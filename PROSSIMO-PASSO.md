# Dove eravamo — 24 agosto, sera

Da riprendere domani. Tutto quello che c'è scritto qui è deciso, non da discutere:
serve solo a non ripartire da capo.

## Fatto oggi

- **RADIOGRAFIA.html** — lo studio sull'estetista italiana con la griglia di Munger,
  nord/centro/sud **più l'Albania** come quarta piazza.
- **L'app riscritta nella loro lingua** — ogni avviso è un verbo, quattro schede
  (Oggi · Clienti · Come va · Il mio centro), tre telefonate al giorno e non venti,
  la sveglia nel calendario, il premio di fine mese, due campi per una cliente nuova.
- **L'agenda dentro l'app.** Deciso: *non si aggancia a niente*. Quindi è lei l'agenda —
  striscia dei sette giorni, appuntamenti con l'ora, «in centro oggi» sopra le telefonate.
- Ciclo di serie portato da 12 a **8 sedute** (i protocolli pubblicati dicono 6-8).

Provate a browser: 61 verifiche sull'app, 18 sulla demo.

## Il prossimo pezzo: i tre pulsanti delle offerte

Come nell'alert NIPEC. In fondo a **Oggi**, tre pulsanti — uno per offerta:
`Offerta Laser 1`, `Offerta Laser 2`, `Offerta Laser 3`.

Come deve funzionare:

1. Preme il pulsante dell'offerta.
2. L'app propone **a chi mandarla**, già filtrato per famiglia:
   - Laser 1 → chi è in ritardo o ha finito il ciclo
   - Laser 2 → chi è in mantenimento da tre mesi
   - Laser 3 → le sparite
3. Sceglie una o più clienti.
4. Si apre **WhatsApp** con il messaggio già scritto: testo dell'offerta + scadenza,
   presi da `Il mio centro → le tre offerte`. Nessun testo scritto a mano nel codice.
5. Insieme al testo va **il post** (l'immagine dell'offerta).

### Le due cose da decidere prima di scrivere codice

- **Il post.** WhatsApp da link (`wa.me`) porta solo testo: non si allega un'immagine.
  Due strade: *(a)* l'immagine sta online e nel messaggio va il link — semplice, funziona
  ovunque; *(b)* la condivisione nativa del telefono (`navigator.share` con file) che
  allega davvero la foto — più bello, ma funziona solo su telefono e non su tutti.
  **Serve una risposta da Giorgio: chi fa le immagini delle offerte e dove stanno.**
- **Mandare a più clienti insieme.** WhatsApp apre una chat per volta: dieci clienti sono
  dieci aperture. Va bene così (è anche più sano), ma va detto chiaramente nell'interfaccia,
  con un contatore «3 di 10 mandate».

## Le lacune ancora aperte (dalla RADIOGRAFIA)

1. ~~Doppio inserimento~~ — **chiusa**: l'app è l'agenda, non si aggancia a nulla.
2. ~~Nessun innesco~~ — **chiusa**: sveglia nel calendario.
3. ~~Lista senza freno~~ — **chiusa**: tre al giorno.
4. ~~Parole sbagliate~~ — **chiusa**: dizionario applicato.
5. ~~Nessuna ricompensa~~ — **chiusa**: «negli ultimi trenta giorni hai tenuto in agenda…».
6. ~~Dati su un telefono solo~~ — **chiusa**: promemoria della copia a 30 giorni.
7. ~~Nove campi~~ — **chiusa**: due.
8. ~~12 sedute~~ — **chiusa**: 8.
9. **Albania: come ci si fa pagare** — aperta. Non la risolve il prodotto: dogana,
   valuta, contratti. Serve il commercialista.
10. **Le dieci telefonate** — aperte. Cinque domande a dieci clienti già tuoi. Restano
    la cosa a più alto rendimento di tutto il progetto.

## Il collaudo del foglio

`2-FOGLI/NIPEC_Cruscotto_Clienti_LASER.xlsx` non è mai stato eseguito da un motore di
calcolo vero (LibreOffice non funziona nell'ambiente dove lavoro). La logica è provata
su 19 casi, la forma è verificata. **Il collaudo in quattro righe è scritto nel LEGGIMI
di `2-FOGLI`: va fatto la prima volta che si converte il foglio in Foglio Google.**

## Gli indirizzi

- App dei centri — https://nipecalert.netlify.app
- Demo — https://kinesiologiapetrelli-svg.github.io/nipec/APP-ALERT-LASER-DEMO/
- Radiografia — https://kinesiologiapetrelli-svg.github.io/nipec/RADIOGRAFIA.html
- Repo — https://github.com/kinesiologiapetrelli-svg/nipec (ramo `claude/persefore-y6fpo8`)

Si ripubblica tutto da solo a ogni modifica. Se si tocca l'app, cambiare il numero di
`VERSIONE` dentro `sw.js`, se no i telefoni già installati non se ne accorgono.
