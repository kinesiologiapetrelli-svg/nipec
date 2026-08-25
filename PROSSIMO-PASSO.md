# Dove eravamo — 25 agosto, mattina

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

## I tre pulsanti delle offerte — FATTI il 25 mattina

In fondo a **Oggi**, tre pulsanti con accanto **quante clienti aspettano quell'offerta
adesso**. Si preme, l'app propone chi (già spuntate), si conferma e parte il giro:
una chat WhatsApp per volta, con il pannello «2 di 5» in cima finché non ha finito.

- il testo del messaggio esce da `Il mio centro → Le tue offerte`: nel codice non c'è
  una parola scritta a mano
- l'app **si ricorda a chi l'ha già mandata** e non la rispunta la volta dopo
- un'offerta senza testo non parte e dice dove scriverlo

Provata a browser: 22 verifiche.

### Le due decisioni, come le ho risolte in attesa di risposta

- **Il post.** Ho aggiunto un campo facoltativo **«Link della foto»** per ogni offerta:
  se c'è, il link parte insieme al testo. Funziona ovunque e non blocca niente.
  **Resta da decidere se vale la pena fare la condivisione nativa** (`navigator.share`,
  allega davvero il file) — è più bella ma va solo da telefono. Serve sapere da Giorgio
  chi fa le immagini e dove stanno.
- **Più clienti insieme.** Fatto una per volta, col contatore. Da confermare che vada bene.

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
