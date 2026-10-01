# Come si scrivono le landing NIPEC

Quattro regole date da Giorgio il 1° ottobre 2026.
**Valgono per sempre, su ogni pagina e ogni cliente.**

---

## 1 · Lo stesso piano di lettura che usiamo con le estetiste

Non si cambia registro perché cambia il lettore. Si scrive come si parla
a una titolare di centro: diretto, concreto, senza giri.

| Si scrive così | Non così |
|---|---|
| «Quel punto non si muove.» | «L'adiposità localizzata presenta una resistenza» |
| «Il corpo decide lui da dove togliere.» | «La distribuzione adiposa risponde a fattori endocrini» |
| «Te lo diciamo noi se non è il caso.» | «Procederemo a una valutazione di idoneità» |
| «Mezz'ora in cui non ti vendiamo niente.» | «Un percorso che nasce dall'ascolto della persona» |

**Frasi corte.** Una idea per frase. Se una frase ha due virgole e un
trattino, si spezza in due.

**Parole che una dice davvero.** Niente «inestetismi» nel testo
emotivo, niente «percorso personalizzato che nasce da», niente
«sinergia». Quelle restano nei testi tecnici e legali.

---

## 2 · Massimo 5 o 6 righe, poi stacco

Nessun blocco di testo più lungo di sei righe sullo schermo del
telefono. Dopo, uno stacco vero: spazio bianco, una riga sottile,
un cambio di fondo.

Un muro di testo su un telefono non si legge: si scorre via.

---

## 3 · I reel, dove servono

Ogni landing ha la sezione dei video pronta. **Resta invisibile finché
i video non ci sono**, così la pagina non sembra mai incompleta.

Quando i reel esistono si mettono nella cartella `video` e si scrivono
tre righe nel blocco `CFG.video`. Serve anche un fotogramma di
copertina `.jpg` per ognuno, altrimenti su telefono resta un
rettangolo nero.

---

## 4 · Il carattere: Impact

Titoli in **Impact**, maiuscolo. È il carattere che Giorgio ha chiesto:
pesante, stretto, si legge da lontano e sullo schermo di un telefono
tenuto in mano mentre si cammina.

Impact c'è già su quasi tutti i computer e i telefoni. Dove non c'è,
la pagina usa **Anton**, che è lo stesso disegno ed è servito dalla
cartella qui accanto. Il risultato è lo stesso: nessuno si accorge
della differenza.

In CSS sta scritto una volta sola, nella variabile `--titoli`:

```css
--titoli: Impact, "Anton", "Haettenschweiler", "Franklin Gothic Bold",
          "Arial Narrow", sans-serif;
```

Testo in **Inter**. Niente serif eleganti: la pagina deve colpire
prima di essere letta.

I caratteri stanno sempre nella cartella `caratteri` accanto alla
pagina, mai sui server di Google: così l'indirizzo IP di chi visita
non esce dal sito.

---

## Due cose che si controllano sempre, prima di consegnare

**I punti elenco col grassetto.** Il segno di spunta va posizionato
fuori dal flusso del testo (`position:absolute`). Se la riga è una
griglia, il grassetto finisce in una colonna sua e l'elenco si
sfascia. È già successo: controllare.

**Il contrasto.** Scritta bianca su oro non si legge — il pulsante
oro vuole la scritta scura. E l'oro del marchio, a 12px, non basta:
per il testo piccolo serve un oro più scuro (`--oro-testo`).

---

## Quello che non cambia

Queste quattro regole si aggiungono a quelle che valevano già:

- **Niente numeri né tempi sul corpo** — «meno 5 cm», «in 2 settimane»
  fanno bocciare l'inserzione su Meta dal 22 luglio 2026.
- **Mai domande sull'aspetto di chi legge.** Si gira in terza persona.
- **Mai garanzie sul risultato.** Si garantisce il rimborso, non l'esito.
- **Il modulo chiede il consenso**, e l'informativa è raggiungibile.
- **Un blocco CONFIGURAZIONE solo**, in fondo alla pagina: chi deve
  cambiare un numero non deve cercare dentro il codice.

---
NIPEC · assistenza 351 846 6025
