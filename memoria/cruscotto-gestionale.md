---
name: cruscotto-gestionale
description: "Il gestionale NIPEC (cruscottonipec.netlify.app): come funziona, cosa è stato corretto il 17 ottobre 2026, cosa resta aperto"
metadata:
  node_type: memory
  type: project
---

# Il cruscotto / gestionale NIPEC

Pagina sola, `index.html`, pubblicata su Netlify. Non sta in questo
repository: il codice sorgente è il file pubblicato. Qui c'è solo la
memoria di come funziona e di cosa è stato toccato.

**Il repository `nipec` è pubblico.** Dentro il gestionale c'è
l'indirizzo dell'endpoint Apps Script, che vale come una chiave: il
file dell'app non va committato qui, e nessuna credenziale va scritta
in nessun file del repository.

## Come sono fatti i dati

- Stato in `localStorage`, chiavi `nipec_gestionale_v2` e
  `nipec_gestionale_v3_safe`, con guardia `_rev` contro le
  sovrascritture fra dispositivi.
- Database condiviso su Google Drive via Apps Script. Una sola parola
  d'ordine, uguale per tutti i dispositivi, salvata in chiaro in
  `localStorage` e spedita nel corpo di ogni richiesta.
- Service worker `sw.js`, strategia *network first*: la versione nuova
  arriva al prossimo caricamento online, senza bisogno di cambiare il
  nome della cache.

## «Da registrare» (prima «da generare»)

Un ricorrente di uscita produce un movimento in prima nota solo quando
si preme il pulsante del mese. La riga esiste in `S.ric`; il movimento
nasce con `src = id + '@' + mese`. Finché quel movimento non c'è, lo
stato è «da registrare». La generazione è manuale, non si duplica
(`isGenerated`) ed è filtrata per paese.

## Correzioni del 17 ottobre 2026

1. **Voci fuori periodo.** Un ricorrente con data di fine passata usciva
   in silenzio da `activeIn()`: spariva dalla copertura dei costi fissi
   e dalla registrazione del mese, e il conto sembrava migliore del
   vero. Aggiunto `fuoriPeriodo(ym)` (finestra di tre mesi), un riquadro
   in Ricorrenti con il pulsante che azzera `r.al` in un clic, e una
   riga di avviso in Panoramica sotto «Copertura costi fissi».
2. **Parola d'ordine.** Minimo portato a 12 caratteri **solo per le
   parole nuove** (`changePw`). Login e `syncConnect` restano a 6: alzare
   anche quelli chiudeva fuori da tutti i dispositivi chi usa la parola
   attuale, che è più corta. Aggiunti il controllo «diversa da quella
   attuale» e, in Impostazioni, l'avviso che compare finché la parola in
   uso sta sotto i 12.
3. **Avviso sul dispositivo.** Schermata di accesso e Impostazioni
   dicono che la parola resta salvata sul dispositivo e che chi apre
   l'app da lì vede i dati dei clienti.
4. **Parole.** «da generare» → «da registrare», come il pulsante;
   spiegazione sotto il pulsante; messaggi di conferma riscritti.
5. **Nota in fondo.** Diceva «I dati restano su questo dispositivo»:
   falso da quando c'è il database online.

## Cosa resta aperto

Codice fiscale, partita IVA, indirizzo e telefono dei clienti stanno
dietro **una sola parola d'ordine condivisa**, con l'indirizzo
dell'endpoint visibile nel sorgente della pagina. Regge per due
persone. Se entra qualcun altro serve un accesso per persona.
