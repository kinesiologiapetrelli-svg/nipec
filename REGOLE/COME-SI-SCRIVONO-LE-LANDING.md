# Come si scrivono le landing NIPEC

Regole date da Giorgio il 1° ottobre 2026.
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

## 4 · Il carattere segue il marchio

La regola non è «metti Impact». È: **il carattere deve essere dello
stesso genere del logo del cliente.** Se stona col logo, la pagina
sembra fatta da due persone diverse.

| Il logo è… | Titoli | Nome del marchio |
|---|---|---|
| grosso, diretto, da insegna | **Impact** (riserva: Anton) | lo stesso |
| una capitale romana in oro, filigranata | **Playfair Display** | **Cinzel** |

- **Bodycharme** — marchio schietto, messaggio diretto: Impact.
- **DEMETRA** — emblema d'oro e scritta in capitale romana: Playfair
  Display per i titoli, Cinzel per il nome. Impact lì era sbagliato,
  e si vedeva: un grottesco da manifesto accanto a una filigrana.

Il testo è sempre **Inter**: è il più leggibile sui telefoni e ha
tutte le lettere che servono.

**Le lettere albanesi vanno verificate nel file del carattere**, non
date per scontate: ë ç Ë Ç. Si controllano prima di consegnare —
un titolo con le dieresi mancanti è una pagina che non si può usare.

Se il titolo è in un serif ad alto contrasto, **non si scrive tutto
maiuscolo**: si legge peggio. La maiuscola resta alle etichette corte.

I caratteri stanno sempre nella cartella `caratteri` accanto alla
pagina, mai sui server di Google: così l'indirizzo IP di chi visita
non esce dal sito.

---

## 5 · Il fondo bianco e i colori del marchio

Quando il marchio ha colori forti — un oro, un verde — questi
**fanno il contorno, non il fondo**: filetti fra le fasce, filo
intorno alle schede, riga in testa alle colonne, cornice del
riquadro dell'offerta.

Il fondo resta bianco. Un fondo pieno color oro spegne l'oro; una
riga d'oro su bianco lo accende.

I colori si **campionano dal file del logo**, pixel per pixel, non
si scelgono a occhio.

Il pulsante principale prende il colore più scuro del marchio: su
bianco è quello che si vede di più. L'oro pieno si tiene per i due
punti dove si parla di soldi — il riquadro dell'offerta e il modulo.

---

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

Queste regole si aggiungono a quelle che valevano già:

- **Niente numeri né tempi sul corpo** — «meno 5 cm», «in 2 settimane»
  fanno bocciare l'inserzione su Meta dal 22 luglio 2026.
- **Mai domande sull'aspetto di chi legge.** Si gira in terza persona.
- **Mai garanzie sul risultato.** Si garantisce il rimborso, non l'esito.
- **Il modulo chiede il consenso**, e l'informativa è raggiungibile.
- **Un blocco CONFIGURAZIONE solo**, in fondo alla pagina: chi deve
  cambiare un numero non deve cercare dentro il codice.

---
NIPEC · assistenza 351 846 6025
