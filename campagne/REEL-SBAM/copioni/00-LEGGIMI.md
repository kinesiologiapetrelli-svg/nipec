# I dodici reel SBAM

2 novembre 2026. Uno per file. Il documento stampato con le stesse cose è `../DODICI-REEL-SBAM.pdf`.

*Per chi mantiene il repository: la fonte è `../reel_sbam_dati.py`. Se cambia qualcosa, si cambia lì e si rilanciano `../fai-copioni.py` e `../fai-documento.py`.* <!--repo-->

**La regola dei 5 secondi, in due metà:** i primi 5 secondi contengono il vantaggio intero; nessuno stacco dura più di 5 secondi, poi si cambia stacco **e** inquadratura.

**La terza cosa, qui il punto: SBAM.** Ogni reel ha un colpo o una sorpresa entro i primi 3 secondi. È quello che ferma il dito.

## Le due serie

| Codice | Serie | Titolo | Chi parla | Il colpo | Stacchi | Copione finisce a |
|---|---|---|---|---|---|---|
| L1 | A · adv · Laser | [Trenta pagine in un colpo](l1-adv-trenta-pagine-in-un-colpo.md) | Giorgio (Italia) · Uarda (Albania) | Trenta pagine di calendario strappate in un colpo | 6 | 17 s |
| L2 | A · adv · Laser | [Fermo](l2-adv-fermo.md) | Giorgio (Italia) · Uarda (Albania) | Il portellone del furgone che si spalanca | 6 | 17,5 s |
| L3 | A · adv · Laser | [Ti sta guardando](l3-adv-ti-sta-guardando.md) | Giorgio (Italia) · Uarda (Albania) | Il lampo sull'obiettivo della telecamera | 6 | 16,5 s |
| F1 | A · adv · Afrodite | [Non comprare Afrodite](f1-adv-non-comprare-afrodite.md) | Giorgio (Italia) · Uarda (Albania) | Il palmo sul tavolo: «Non comprare» diventa «Noleggiala» | 6 | 17 s |
| F2 | A · adv · Afrodite | [Quattro colpi](f2-adv-quattro-colpi.md) | Giorgio (Italia) · Uarda (Albania) | Quattro manipoli, quattro colpi a ritmo | 6 | 17 s |
| F3 | A · adv · Afrodite | [I compiti già fatti](f3-adv-i-compiti-gia-fatti.md) | Giorgio (Italia) · Uarda (Albania) | Il fascicolo del protocollo che cade sul tavolo | 6 | 18 s |
| P1 | B · pagina | [Fermo. Non firmare.](p1-pagina-fermo-non-firmare.md) | Giorgio | Il palmo sul tavolo: «Fermo!» | 7 | 20 s |
| P2 | B · pagina | [Sotto il telo](p2-pagina-sotto-il-telo.md) | Giorgio | Il telo che vola via | 7 | 17 s |
| P3 | B · pagina | [L'esame](p3-pagina-lesame.md) | Uarda o la formatrice DEMETRA | Il timbro sul foglio bianco | 7 | 20 s |
| P4 | B · pagina | [Cosa c'è nella scatola](p4-pagina-cosa-ce-nella-scatola.md) | Giorgio | Il coperchio della scatola che scatta | 7 | 18 s |
| P5 | B · pagina | [Falso](p5-pagina-falso.md) | Giorgio | Due timbri: FALSO | 7 | 19 s |
| P6 | B · pagina | [Cinque secondi](p6-pagina-cinque-secondi.md) | Giorgio | La sveglia battuta: «Ti ho fermato» | 7 | 20 s |

## Come si fa lo SBAM

- **Cos'è.** Un colpo secco, in immagine e in suono, che cade entro i primi 3 secondi. Serve a una cosa sola: fermare il dito che scrolla.
- **Suono.** Un colpo breve e grave (0,3 s), seguito da mezzo secondo di silenzio: il silenzio è quello che lo fa sentire. Dove c'è un suono vero (portellone, palmo sul tavolo, timbro, strappo di fogli) si usa quello, alzato in montaggio. Altrimenti un colpo senza diritti: si può generare.
- **Immagine.** Un lampo bianco di 2 fotogrammi (a 30 fps), la scossa dell'inquadratura per 6 fotogrammi, e la scritta che arriva al 130% e si assesta al 100% in 4 fotogrammi.
- **Quanti.** Al massimo due per reel. Quattro colpi a ritmo (F2) contano come uno.
- **Con la musica.** La base musicale si ferma 0,2 s prima del colpo e riparte subito dopo.
- **Sicurezza.** Niente si rompe e niente cade davvero: i manipoli e il dispositivo si appoggiano piano, il colpo lo mette il montaggio. Al massimo un lampo bianco al secondo, per chi è sensibile alla luce.
- **Mai.** Urla, glitch continui, scritte che tremano per tutto il reel. Il colpo è uno: il resto sta fermo.

## Ordine di uscita (proposta)

- **Prima la pagina.** Serie B: sei reel sono sei pubblicazioni, il minimo che la pagina NIPEC deve avere prima di poter sponsorizzare (Campagna 500). Ordine consigliato: P1, P5, P2, P3, P4, P6, due a settimana.
- **Poi il laser.** Serie A, laser, Italia per prima: L1 (dice tutta l'offerta nei primi 5 secondi), poi L2, poi L3. L'Albania segue con gli stessi tre, detti da Uarda.
- **Dopo due settimane, Afrodite.** F1, F2, F3, come nella Campagna 500. Stesso ordine di forza: il più netto per primo.

## Per l'Albania

- **Chi parla.** Uarda. Il copione resta in italiano finché il testo albanese non è approvato; i sottotitoli riportano quello che si sente davvero.
- **Il prezzo.** «500 € / MESE» diventa «50.000 LEKË / MUAJ». A voce: «cinquantamila lekë al mese».
- **L1, stacco 3.** «prima del primo euro» diventa «prima del primo lek».
- **Il numero.** WhatsApp di Uarda: +355 69 212 9786. In P4 è il numero sul foglietto.
- **Le parole di Afrodite.** In F2 la scritta «ULTRASUONO FOCALIZZATO DIREZIONALE» in albanese è «ULTRATINGULL I FOKUSUAR»: da far controllare a Uarda.
- **La parola chiave.** Resta LASER o AFRODITE, scritta così in WhatsApp.

## Parole che non si usano

«Macchina» (si dice **dispositivo**), «LED» (**low laser**), «cavitazione» (**ultrasuono focalizzato direzionale**), percentuali, prima/dopo, il modello del laser, diodi, watt. Il controllo è automatico: `python3 reel_sbam_dati.py`.
