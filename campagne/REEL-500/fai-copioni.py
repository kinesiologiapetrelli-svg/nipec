#!/usr/bin/env python3
"""Scrive i nove copioni (copioni/*.md) e le inserzioni (copioni/INSERZIONI.md) dai dati in reel_dati.py.

La fonte e' reel_dati.py: stacco per stacco, secondo la regola dei 5 secondi. Il documento stampato
(nove-reel.html) si rifa con fai-documento.py, dagli stessi dati: i due non possono dire cose diverse.

Uso:  python3 fai-copioni.py
"""
import os, re, unicodedata
import reel_dati as R

QUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(QUI, 'copioni')
os.makedirs(OUT, exist_ok=True)
for f in os.listdir(OUT):
    if f.endswith('.md'): os.remove(os.path.join(OUT, f))

if not R.controlla():
    raise SystemExit('I dati dei reel non rispettano la regola dei 5 secondi: correggi reel_dati.py')

def slug(t):
    t = unicodedata.normalize('NFKD', t.lower().replace("'", '')).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', t).strip('-')[:44].rstrip('-')

def cella(t):
    return t.replace('|', '/')

indice = []
for n in range(1, 10):
    paese, camp, chi, lingua, parola, scheda, gancio = R.META[n]
    titolo = R.TITOLO[n]
    st = R.stacchi(n)
    fine = st[-1]['t1']
    nome = f'reel-{n:02d}-{paese.lower()}-{slug(titolo)}.md'
    L = ['---', f'id: reel-{n:02d}', f'titolo: "{titolo}"', f'campagna: "{camp} {paese}"', f'paese: {paese}',
         f'chi_parla: {chi}', f'lingua_parlata: {lingua}', 'formato: "verticale 9:16, 1080x1920"',
         f'numero_stacchi: {len(st)}', f'stacco_piu_lungo_secondi: {max(s["dur"] for s in st)}',
         f'gancio_finisce_a_secondi: {st[gancio - 1]["t1"]}', f'fine_copione_secondi: {fine}',
         'scheda_finale_secondi: 2', f'durata_totale_secondi: {fine + 2}', f'parola_chiave: {parola}',
         f'scheda_finale: "schede-finali/{scheda}"', '---\n']
    L.append(f'# Reel {n} · {paese} — {titolo}\n')
    L.append(f'**Chi parla:** {chi} (in {lingua}, faccia vera in camera, non voce fuori campo).  ')
    L.append(f'**Parola chiave di chiusura:** {parola}.  ')
    L.append(f'**Durata:** il copione finisce a {R.fmt(fine)} secondi; poi la scheda finale, ferma 2 secondi: {R.fmt(fine + 2)} secondi in tutto.\n')
    L.append('> **La regola dei 5 secondi.** (1) I primi 5 secondi contengono il vantaggio intero. (2) **Nessuno stacco dura più di 5 secondi:** '
             'dopo, si cambia stacco **e inquadratura**. Mai due inquadrature uguali di fila. Il reel resta dinamico, e ogni pezzo è semplice da girare: '
             'un gesto, una frase breve.\n')
    if lingua == 'albanese':
        L.append('> **Lingua.** Il copione è scritto in italiano. Le parole dette sono in albanese, e un testo albanese approvato non esiste ancora. '
                 'I tempi qui sotto sono calcolati sulle parole italiane: **in albanese le frasi sono di solito un po\' più lunghe**. '
                 'Uno stacco non deve comunque superare i 5 secondi: se una frase non ci sta, si divide in due stacchi cambiando inquadratura. '
                 'I sottotitoli riportano **quello che si sente davvero**. Le scritte a schermo in albanese valgono così come sono.\n')
    L.append('## Sequenza, stacco per stacco\n')
    L.append('| # | Tempo | Inquadratura | Si vede | Si dice | Scritta a schermo |')
    L.append('|---|---|---|---|---|---|')
    for s in st:
        sc = ' / '.join(f'`{r}`' for r in s['schermo']) if s['schermo'] else '—'
        L.append(f'| {s["n"]} | {R.fmt(s["t0"])}–{R.fmt(s["t1"])} s | {s["inq"]} | {cella(s["vede"])} | '
                 f'{("«" + cella(s["parla"]) + "»") if s["parla"] else "(in silenzio)"} | {sc} |')
        if s['n'] == gancio:
            L.append(f'| | | | **— fine dei primi 5 secondi: il gancio è tutto qui —** | | |')
    L.append(f'| {len(st) + 1} | {R.fmt(fine)}–{R.fmt(fine + 2)} s | Scheda finale | `schede-finali/{scheda}` a tutto schermo, ferma. Niente altro sopra. | — | — |\n')
    L.append('Le scritte a schermo **entrano insieme alla parola** che dicono, non prima.\n')
    L.append('## Come si gira, semplice\n')
    L.append('- **Un pezzo alla volta.** Ogni stacco è un gesto e una frase: si gira a pezzi, una o due riprese ciascuno. Non serve girare il reel tutto di fila.')
    L.append('- **Le quattro inquadrature:** primo piano (' + R.QUADRO[R.PP] + '), mezzo busto (' + R.QUADRO[R.MB] + '), dettaglio (' + R.QUADRO[R.DET] + '), campo largo (' + R.QUADRO[R.CL] + ').')
    L.append('- **Per cambiare inquadratura senza spostare la camera**, in montaggio si ingrandisce la stessa ripresa (zoom): conta come stacco nuovo. '
             'Così una frase detta di seguito si divide in due stacchi, uno largo e uno stretto.')
    L.append('- **Se una frase non ci sta in 5 secondi**, si divide in due stacchi. Non si accelera.\n')
    ang, testo_ad, tit_ad = R.AD[n]
    L.append("## Per l'inserzione\n")
    if lingua == 'albanese':
        L.append('> Testo scritto in italiano, da approvare. La traduzione in albanese si fa sul testo approvato, non prima.\n')
    L.append(f'- **Angolo:** {ang}')
    L.append('- **Testo principale** (le righe vanno a capo come qui sotto):')
    for r in testo_ad.split('\n'): L.append(f'  > {r}  ')
    L.append(f'- **Titolo:** {tit_ad}  ({len(tit_ad)} caratteri)')
    L.append('- **Pulsante:** Invia messaggio (WhatsApp)')
    L.append(f'- **Messaggio già scritto nella chat:** `{parola}`')
    L.append(f'- **Il numero WhatsApp:** {R.NUM[paese]}')
    L.append('- **Pubblico, zone e budget:** quelli della Campagna 500 (vedi `../FLUSSO-TELEGRAM.md`, «A cosa servono»). Il video è questo reel, montato, senza cambiare niente.')
    L.append('- **Non si scrive:** il modello del laser, diodi o watt, risultati sulla pelle, percentuali, tempi, confronti con un concorrente.\n')
    L.append('## Cosa serve per girarlo\n')
    L.append(R.SERVE[n] + '\n')
    if n in R.NOTE:
        L.append('## Attenzione\n')
        for x in R.NOTE[n]: L.append(f'- {x}')
        L.append('')
    L.append('## Cosa non si mostra\n')
    L.append('Pelle trattata, prima/dopo, percentuali di risultato, tempi di risultato.\n')
    open(os.path.join(OUT, nome), 'w', encoding='utf8').write('\n'.join(L))
    indice.append((n, nome, titolo, paese, camp, chi, parola, fine, len(st)))

I = ['# I nove copioni\n',
     'Rev. 3 · 22 ottobre 2026. Uno per file. Si gira **nell\'ordine dei numeri**. Il documento stampato con le stesse cose è `../NOVE-REEL-campagna-500-REV3.pdf`.\n',
     '*Per chi mantiene il repository: la fonte è `../reel_dati.py`. Se cambia qualcosa, si cambia lì e si rilanciano `../fai-copioni.py` e `../fai-documento.py`.* <!--repo-->\n',
     '**La regola dei 5 secondi:** i primi 5 secondi contengono il vantaggio intero, e **nessuno stacco dura più di 5 secondi**: dopo, si cambia stacco e inquadratura. '
     'Ogni copione è scritto stacco per stacco, con il tempo, l\'inquadratura, cosa si vede, cosa si dice e cosa appare scritto.\n',
     '| # | File | Titolo | Paese | Campagna | Chi parla | Parola | Stacchi | Copione finisce a |', '|---|---|---|---|---|---|---|---|---|']
for n, nome, titolo, paese, camp, chi, parola, fine, ns in indice:
    I.append(f'| {n} | `{nome}` | {titolo} | {paese} | {camp} | {chi} | {parola} | {ns} | {R.fmt(fine)} s |')
I.append('')
I.append('Ogni file ha: i campi fissi in testa, la sequenza stacco per stacco, come si gira, il testo dell\'inserzione e cosa serve per girarlo. '
         'La grafica dei testi a schermo e le regole di montaggio sono in `../FLUSSO-TELEGRAM.md`. '
         'Tutti i testi delle inserzioni, da copiare in Meta, stanno insieme in `INSERZIONI.md`.\n')
open(os.path.join(OUT, '00-LEGGIMI.md'), 'w', encoding='utf8').write('\n'.join(I))

A = ['# Le nove inserzioni, tutte insieme\n',
     'Per chi carica in Gestione inserzioni di Meta: i testi da copiare, uno per reel. Sono gli stessi che stanno in fondo a ogni copione.\n',
     '**Per tutte:** pulsante **Invia messaggio** (WhatsApp); destinazione WhatsApp, non una pagina web; il messaggio già scritto nella chat è la parola chiave. '
     'Pubblico, zone e budget sono quelli della Campagna 500. **Il modello del laser non si nomina.**\n',
     '**Titoli:** tutti sotto i 40 caratteri, così Meta non li taglia.\n',
     '| # | Paese | Angolo | Titolo | Caratteri titolo | Parola nella chat |', '|---|---|---|---|---|---|']
for n, nome, titolo, paese, camp, chi, parola, fine, ns in indice:
    ang, testo_ad, tit_ad = R.AD[n]
    A.append(f'| {n} | {paese} | {ang.split(" (")[0]} | {tit_ad} | {len(tit_ad)} | `{parola}` |')
A.append('')
for n, nome, titolo, paese, camp, chi, parola, fine, ns in indice:
    ang, testo_ad, tit_ad = R.AD[n]
    A.append(f'## Reel {n} · {paese} — {titolo}\n')
    if paese == 'Albania': A.append('*Testo in italiano, da approvare; poi si traduce in albanese.*\n')
    A.append(f'**Angolo:** {ang}  ')
    A.append(f'**Video:** il reel {n}, montato. Copione: `{nome}`  ')
    A.append(f'**Titolo:** {tit_ad}  ')
    A.append(f'**Messaggio nella chat:** `{parola}`  ')
    A.append(f'**WhatsApp:** {R.NUM[paese]}\n')
    A.append('**Testo principale:**\n')
    for r in testo_ad.split('\n'): A.append(f'> {r}  ')
    A.append('')
open(os.path.join(OUT, 'INSERZIONI.md'), 'w', encoding='utf8').write('\n'.join(A))
print(len(indice), 'copioni scritti in', OUT)
