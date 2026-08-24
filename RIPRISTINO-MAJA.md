# Cruscotto MAJA — cosa è rotto e come si chiude

Diagnosi del 24 agosto 2026. Sito: `nipec-alert1.netlify.app` · Centro:
Centro Estetico MAJA · Referente: Uarda.

## Il guasto, in una riga

Il sito non apre il foglio sbagliato: **non apre niente.** Il link non è mai
stato incollato, il file non è mai stato condiviso, e non esiste nessun
Foglio Google.

## I tre difetti

| # | Difetto | Prova |
|---|---------|-------|
| 1 | Link del foglio mai incollato | In `maja/index.html` e in `_centri.csv` c'è ancora il segnaposto `INCOLLA-QUI-IL-LINK`. La pagina se ne accorge e disattiva i tre pulsanti. |
| 2 | Nessun Foglio Google esistente | I cruscotti sono `.xlsx`. In tutto il Drive non c'è **nessun** Foglio Google NIPEC. Il sito si aspetta un URL `docs.google.com/spreadsheets/...` con ancora `#gid=`. |
| 3 | File non condiviso | Permessi di `Cruscotto Clienti - Centro Estetico MAJA.xlsx`, del gemello `LASER` e della cartella `2-FOGLI`: **un solo utente, il proprietario.** Uarda non c'è. |

## Dove NON sono i dati

Nessuno dei quattro file in `2-FOGLI` è stato modificato dopo il
**21/08/2026 20:06**. Il foglio CLIENTI di MAJA è vuoto, il RIEPILOGO segna
0 ovunque. Le uniche caselle compilate sono, in IMPOSTAZIONI:
`Nome del centro = Centro Estetico MAJA` e `Referente NIPEC = Uarda`.

## I quattro file in `2-FOGLI`

| File | ID | Ruolo |
|------|----|-------|
| `Cruscotto Clienti - Centro Estetico MAJA.xlsx` | `1jaXWqJBrvZG9dFki4CZEApHzVwkUxlaq` | **Il file del centro** |
| `NIPEC_Cruscotto_Clienti_LASER.xlsx` | `133SRiPzdWZDhl2-jysF65XCWGt8aTWUN` | Modello LASER, non personalizzato |
| `NIPEC_Cruscotto_Clienti_CENTRO.xlsx` | `1BsTeBZtWQS24VLOzvFHGHWgTCQMe1YMR` | Modello estetica generica |
| `NIPEC_MASTER_Centri.xlsx` | `1txmNe7w-Fx2j-MlcEXwUVxkVf1zQWWHv` | Master (vuoto) |

Due nomi quasi identici — `..._CENTRO` e `...Centro Estetico MAJA` — nella
stessa cartella. È lì che l'occhio inciampa. Vale la pena rinominare i
modelli con prefisso `MODELLO_`.

## La chiusura, in ordine

1. **Condividi** `Cruscotto Clienti - Centro Estetico MAJA.xlsx` con
   `nipecuarda@gmail.com`, ruolo *Editor*, opzione **"Persone specifiche"** —
   mai "Chiunque abbia il link".
2. **Incolla il link** in `maja/index.html`, sostituendo il blocco `CENTRO`
   con quello qui sotto.
3. **Ricarica la cartella `maja/` su Netlify** in drag&drop.

### Il blocco da sostituire in `maja/index.html`

```js
const CENTRO = {
  nome:      "Centro Estetico MAJA",
  citta:     "",
  titolare:  "",

  foglio:    "https://docs.google.com/spreadsheets/d/1jaXWqJBrvZG9dFki4CZEApHzVwkUxlaq/edit",

  gidClienti:   "",
  gidRiepilogo: "",

  referente:  "Uarda",
  whatsapp:   "393518466025",
};
```

I due `gid` restano vuoti finché non si apre il foglio: sono i numeri dopo
`#gid=` nell'URL quando si è sulla pagina CLIENTI e sulla pagina RIEPILOGO.
Con i `gid` vuoti i pulsanti funzionano lo stesso, ma aprono il foglio alla
prima pagina invece che a quella giusta.

## Il passo successivo, non urgente

Quando si collega il **MASTER**, il cruscotto va convertito in Foglio Google
(tasto destro → Apri con → Google Fogli → File → Salva come Foglio Google):
`IMPORTRANGE` legge solo Fogli Google nativi, non i `.xlsx`. La conversione
crea un **file nuovo**, di solito nella radice di "Il mio Drive" — va
rinominato e rimesso in `2-FOGLI`, e il link nel punto 2 va aggiornato col
nuovo ID.

## Difetto minore, da correggere nel modello

`NIPEC_Cruscotto_Clienti_CENTRO.xlsx` → IMPOSTAZIONI →
*Telefono assistenza NIPEC* = **`351 846 605`**: manca una cifra.
Il numero giusto è **`+39 351 846 6025`**. Nel file MAJA è corretto.
Va sistemato nel modello, altrimenti ogni centro nuovo nasce col numero
sbagliato.
