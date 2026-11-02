#!/usr/bin/env python3
"""Scrive i dodici copioni (copioni/*.md), le inserzioni della serie A (copioni/INSERZIONI.md) e le didascalie della serie B (copioni/PAGINA.md).

La fonte e' reel_sbam_dati.py: stacco per stacco, secondo la regola dei 5 secondi. Il documento stampato si rifa con fai-documento.py.

Uso:  python3 fai-copioni.py
"""
import os, re, unicodedata
import reel_sbam_dati as D

QUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(QUI, 'copioni')
os.makedirs(OUT, exist_ok=True)
for f in os.listdir(OUT):
    if f.endswith('.md'): os.remove(os.path.join(OUT, f))

if not D.controlla():
    raise SystemExit('I dati dei reel non rispettano le regole: correggi reel_sbam_dati.py')

def slug(t):
    t = unicodedata.normalize('NFKD', t.lower().replace("'", '')).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', t).strip('-')[:40].rstrip('-')

def cella(t): return t.replace('|', '/')

nomi = {}
for c in D.CODICI:
    r = D.R[c]; st = D.stacchi(c); fine = D.fine(c); g = r['gancio']
    serie = 'adv' if r['serie'] == 'A' else 'pagina'
    nome = f'{c.lower()}-{serie}-{slug(r["titolo"])}.md'; nomi[c] = nome
    L = ['---', f'id: {c}', f'titolo: "{r["titolo"]}"', f'serie: "{"A · adv" if r["serie"] == "A" else "B · pagina"}"', f'campagna: "{r["campagna"]}"',
         f'chi_parla: "{r["chi"]}"', 'formato: "verticale 9:16, 1080x1920"', f'numero_stacchi: {len(st)}',
         f'stacco_piu_lungo_secondi: {max(s["dur"] for s in st)}', f'gancio_finisce_a_secondi: {st[g - 1]["t1"]}',
         f'sbam_comincia_a_secondi: {st[r["sbam"] - 1]["t0"]}', f'fine_copione_secondi: {fine}', 'scheda_finale_secondi: 2',
         f'durata_totale_secondi: {fine + 2}']
    if r['parola']: L.append(f'parola_chiave: {r["parola"]}')
    L += ['---\n', f'# {c} · {r["titolo"]}\n']
    L.append(f'**Chi parla:** {r["chi"]}  ')
    L.append(f'**Il colpo (SBAM):** {r["concetto"]}  ')
    L.append(f'**Durata:** il copione finisce a {D.fmt(fine)} secondi; poi la scheda finale, ferma 2 secondi: {D.fmt(fine + 2)} secondi in tutto.\n')
    L.append('> **La regola dei 5 secondi.** (1) I primi 5 secondi contengono il vantaggio intero. (2) **Nessuno stacco dura più di 5 secondi:** dopo, si cambia stacco **e inquadratura**, mai due uguali di fila. '
             f'(3) **SBAM:** il colpo cade entro i primi 3 secondi, qui a {D.fmt(st[r["sbam"] - 1]["t0"])} s. Come si fa: `00-LEGGIMI.md`, sezione «Come si fa lo SBAM».\n')
    L.append('## Sequenza, stacco per stacco\n')
    L.append('| # | Tempo | Inquadratura | Si vede | Si dice | Scritta a schermo | Suono |')
    L.append('|---|---|---|---|---|---|---|')
    for s in st:
        sc = ' / '.join(f'`{x}`' for x in s['schermo']) if s['schermo'] else '—'
        L.append(f'| {s["n"]} | {D.fmt(s["t0"])}–{D.fmt(s["t1"])} s | {s["inq"]} | {cella(s["vede"])} | '
                 f'{("«" + cella(s["parla"]) + "»") if s["parla"] else "(in silenzio)"} | {sc} | {cella(s["suono"])} |')
        if s['n'] == g: L.append('| | | | **— fine dei primi 5 secondi: il gancio è tutto qui —** | | | |')
    L.append(f'| {len(st) + 1} | {D.fmt(fine)}–{D.fmt(fine + 2)} s | Scheda finale | A tutto schermo, ferma. Niente altro sopra. | — | — | — |\n')
    L.append('Le scritte a schermo **entrano insieme alla parola** che dicono, non prima. Il logo non compare nei primi 5 secondi.\n')
    L.append('## Come si gira, semplice\n')
    L.append('- **Un pezzo alla volta.** Ogni stacco è un gesto e una frase: una o due riprese ciascuno. Non serve girare il reel tutto di fila.')
    L.append('- **Le quattro inquadrature:** primo piano (' + D.QUADRO[D.PP] + '), mezzo busto (' + D.QUADRO[D.MB] + '), dettaglio (' + D.QUADRO[D.DET] + '), campo largo (' + D.QUADRO[D.CL] + ').')
    L.append('- **Per cambiare inquadratura senza spostare la camera**, in montaggio si ingrandisce la stessa ripresa: conta come stacco nuovo.')
    L.append('- **Se una frase non ci sta in 5 secondi**, si divide in due stacchi. Non si accelera.\n')
    if r['serie'] == 'A':
        testo_ad, tit = r['ad']
        L.append("## Per l'inserzione\n")
        L.append('- **Testo principale** (le righe vanno a capo come qui sotto):')
        for x in testo_ad.split('\n'): L.append(f'  > {x}  ')
        L.append(f'- **Titolo:** {tit}  ({len(tit)} caratteri)')
        L.append('- **Pulsante:** Invia messaggio (WhatsApp)')
        L.append(f'- **Messaggio già scritto nella chat:** `{r["parola"]}`')
        L.append('- **Numeri WhatsApp:** Italia +39 351 846 6025 (Giorgio) · Albania +355 69 212 9786 (Uarda)')
        L.append('- **Pubblico, zone e budget:** quelli della Campagna 500. Il video è questo reel, montato, senza cambiare niente.')
        L.append('- **Non si scrive:** il modello del laser, diodi o watt, risultati sulla pelle, percentuali, tempi, confronti con un concorrente.\n')
    else:
        L.append('## Per la pagina\n')
        L.append('- **Didascalia:**')
        L.append(f'  > {r["didascalia"]}')
        L.append('- **Non è un\'inserzione:** nessun prezzo, nessuna parola chiave da scrivere. Il reel serve a far fermare il dito e a far ricordare chi siamo.\n')
    L.append('## Cosa serve per girarlo\n')
    L.append(r['serve'] + '\n')
    if r['note']:
        L.append('## Attenzione\n')
        for x in r['note']: L.append(f'- {x}')
        L.append('')
    L.append('## Cosa non si mostra\n')
    L.append('Pelle trattata, prima/dopo, percentuali di risultato, tempi di risultato. Nessun volto senza consenso.\n')
    open(os.path.join(OUT, nome), 'w', encoding='utf8').write('\n'.join(L))

# indice, con le regole comuni
I = ['# I dodici reel SBAM\n',
     '2 novembre 2026. Uno per file. Il documento stampato con le stesse cose è `../DODICI-REEL-SBAM.pdf`.\n',
     '*Per chi mantiene il repository: la fonte è `../reel_sbam_dati.py`. Se cambia qualcosa, si cambia lì e si rilanciano `../fai-copioni.py` e `../fai-documento.py`.* <!--repo-->\n',
     '**La regola dei 5 secondi, in due metà:** i primi 5 secondi contengono il vantaggio intero; nessuno stacco dura più di 5 secondi, poi si cambia stacco **e** inquadratura.\n',
     '**La terza cosa, qui il punto: SBAM.** Ogni reel ha un colpo o una sorpresa entro i primi 3 secondi. È quello che ferma il dito.\n',
     '## Le due serie\n',
     '| Codice | Serie | Titolo | Chi parla | Il colpo | Stacchi | Copione finisce a |', '|---|---|---|---|---|---|---|']
for c in D.CODICI:
    r = D.R[c]
    I.append(f'| {c} | {"A · adv · " + r["campagna"] if r["serie"] == "A" else "B · pagina"} | [{r["titolo"]}]({nomi[c]}) | {r["chi"]} | '
             f'{D.COLPO[c]} | {len(D.stacchi(c))} | {D.fmt(D.fine(c))} s |')
I.append('\n## Come si fa lo SBAM\n')
for k, v in D.SBAM: I.append(f'- **{k}.** {v}')
I.append('\n## Ordine di uscita (proposta)\n')
for k, v in D.ORDINE: I.append(f'- **{k}.** {v}')
I.append('\n## Per l\'Albania\n')
for k, v in D.ALBANIA: I.append(f'- **{k}.** {v}')
I.append('\n## Parole che non si usano\n')
I.append('«Macchina» (si dice **dispositivo**), «LED» (**low laser**), «cavitazione» (**ultrasuono focalizzato direzionale**), percentuali, prima/dopo, il modello del laser, diodi, watt. '
         'Il controllo è automatico: `python3 reel_sbam_dati.py`.\n')
open(os.path.join(OUT, '00-LEGGIMI.md'), 'w', encoding='utf8').write('\n'.join(I))

A = ['# Le sei inserzioni, tutte insieme\n',
     'Per chi carica in Gestione inserzioni di Meta: i testi da copiare, uno per reel. Sono gli stessi che stanno in fondo a ogni copione.\n',
     '**Per tutte:** pulsante **Invia messaggio** (WhatsApp); destinazione WhatsApp, non una pagina web; il messaggio già scritto nella chat è la parola chiave. '
     'Pubblico, zone e budget sono quelli della Campagna 500. **Il modello del laser non si nomina.** Per l\'Albania: 500 € diventa 50.000 lekë, il numero è quello di Uarda.\n',
     '| Reel | Campagna | Titolo | Caratteri titolo | Parola nella chat |', '|---|---|---|---|---|']
for c in D.CODICI:
    r = D.R[c]
    if r['serie'] != 'A': continue
    A.append(f'| {c} · {r["titolo"]} | {r["campagna"]} | {r["ad"][1]} | {len(r["ad"][1])} | `{r["parola"]}` |')
A.append('')
for c in D.CODICI:
    r = D.R[c]
    if r['serie'] != 'A': continue
    A.append(f'## {c} · {r["titolo"]}\n')
    A.append(f'**Video:** il reel {c}, montato. Copione: `{nomi[c]}`  ')
    A.append(f'**Titolo:** {r["ad"][1]}  ')
    A.append(f'**Messaggio nella chat:** `{r["parola"]}`\n')
    A.append('**Testo principale:**\n')
    for x in r['ad'][0].split('\n'): A.append(f'> {x}  ')
    A.append('')
open(os.path.join(OUT, 'INSERZIONI.md'), 'w', encoding='utf8').write('\n'.join(A))

P = ['# Le sei didascalie della pagina\n',
     'Per i reel della serie B. Non sono inserzioni: nessun prezzo, nessuna parola chiave. Ordine consigliato: P1, P5, P2, P3, P4, P6.\n']
for c in ('P1', 'P5', 'P2', 'P3', 'P4', 'P6'):
    r = D.R[c]
    P.append(f'## {c} · {r["titolo"]}\n')
    P.append(f'**Video:** il reel {c}, montato. Copione: `{nomi[c]}`\n')
    P.append('**Didascalia:**\n')
    P.append(f'> {r["didascalia"]}\n')
open(os.path.join(OUT, 'PAGINA.md'), 'w', encoding='utf8').write('\n'.join(P))
print(len(nomi), 'copioni scritti in', OUT)
