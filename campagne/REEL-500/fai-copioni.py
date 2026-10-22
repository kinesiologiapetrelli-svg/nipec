#!/usr/bin/env python3
"""Estrae i nove copioni da nove-reel.html e li scrive uno per file in copioni/.

Il sorgente resta nove-reel.html (e' quello che si stampa). I file in copioni/ sono
la stessa cosa in forma che si legge bene anche da un programma: un'intestazione
con i campi fissi, poi la sequenza, secondo per secondo.

Uso:  python3 fai-copioni.py
"""
import html, os, re

QUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(QUI, 'copioni')
os.makedirs(OUT, exist_ok=True)
for f in os.listdir(OUT):
    if f.endswith('.md'): os.remove(os.path.join(OUT, f))

src = open(os.path.join(QUI, 'nove-reel.html'), encoding='utf8').read()

def testo(s):
    s = re.sub(r'<br\s*/?>', ' ', s)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', s))).strip()

def righe(s):
    return [re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', x))).strip() for x in re.split(r'<br\s*/?>', s) if x.strip()]

META = {
    1: ('Italia', 'Laser', 'Giorgio', 'italiano', 'LASER', 'scheda-finale-LASER-italia.png'),
    2: ('Italia', 'Laser', 'Giorgio', 'italiano', 'LASER', 'scheda-finale-LASER-italia.png'),
    3: ('Italia', 'Laser', 'Giorgio', 'italiano', 'LASER', 'scheda-finale-LASER-italia.png'),
    4: ('Albania', 'Laser', 'Uarda', 'albanese', 'LASER', 'scheda-finale-LASER-albania.png'),
    5: ('Albania', 'Laser', 'Uarda', 'albanese', 'LASER', 'scheda-finale-LASER-albania.png'),
    6: ('Albania', 'Laser', 'Uarda', 'albanese', 'LASER', 'scheda-finale-LASER-albania.png'),
    7: ('Albania', 'Afrodite', 'Uarda', 'albanese', 'AFRODITE', 'scheda-finale-AFRODITE-albania.png'),
    8: ('Albania', 'Afrodite', 'Uarda', 'albanese', 'AFRODITE', 'scheda-finale-AFRODITE-albania.png'),
    9: ('Albania', 'Afrodite', 'Uarda', 'albanese', 'AFRODITE', 'scheda-finale-AFRODITE-albania.png'),
}
ETI = {'I 5 secondi': 'I primi 5 secondi', 'Sviluppo': 'Sviluppo', 'Chiusura': 'Chiusura'}

reel = []
for blocco in src.split('<div class="reel">')[1:]:
    n = int(re.search(r'Reel (\d)', blocco).group(1))
    titolo = testo(re.search(r'<span class="tt">(.*?)</span>', blocco, re.S).group(1))
    seg, serve = [], ''
    for et, cont in re.findall(r'<tr><td class="t">(.*?)</td><td>(.*?)</td></tr>', blocco, re.S):
        et = testo(et)
        if et == 'Serve':
            serve = testo(cont); continue
        sec = re.search(r'<span class="sec">(.*?)</span>', cont)
        parla = re.search(r'<b class="parla">(.*?)</b>', cont, re.S)
        sch = re.search(r'<span class="schermo">(.*?)</span>', cont, re.S)
        vede = re.sub(r'<span class="sec">.*?</span>', '', cont, flags=re.S)
        vede = re.split(r'<b class="parla">', vede)[0]
        seg.append(dict(et=ETI.get(et, et), sec=testo(sec.group(1)) if sec else '', vede=testo(vede),
                        parla=testo(parla.group(1)) if parla else '', schermo=righe(sch.group(1)) if sch else []))
    reel.append((n, titolo, seg, serve))

def slug(t):
    import unicodedata
    t = unicodedata.normalize('NFKD', t.lower().replace("'", '')).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', t).strip('-')[:44].rstrip('-')

def fine(seg):
    m = re.findall(r'(\d+)[-–](\d+)', seg[-1]['sec'])
    return int(m[-1][1]) if m else 0

indice = []
for n, titolo, seg, serve in reel:
    paese, camp, chi, lingua, parola, scheda = META[n]
    durata = fine(seg)
    nome = f'reel-{n:02d}-{paese.lower()}-{slug(titolo)}.md'
    L = []
    L.append('---')
    L.append(f'id: reel-{n:02d}')
    L.append(f'titolo: "{titolo}"')
    L.append(f'campagna: "{camp} {paese}"')
    L.append(f'paese: {paese}')
    L.append(f'chi_parla: {chi}')
    L.append(f'lingua_parlata: {lingua}')
    L.append('formato: "verticale 9:16, 1080x1920"')
    L.append(f'fine_copione_secondi: {durata}')
    L.append('scheda_finale_secondi: 2')
    L.append(f'durata_totale_secondi: {durata + 2}')
    L.append(f'parola_chiave: {parola}')
    L.append(f'scheda_finale: "schede-finali/{scheda}"')
    L.append('---\n')
    L.append(f'# Reel {n} · {paese} — {titolo}\n')
    L.append(f'**Chi parla:** {chi} (in {lingua}, faccia vera in camera, non voce fuori campo).  ')
    L.append(f'**Parola chiave di chiusura:** {parola}.  ')
    L.append(f'**Durata:** il copione finisce a {durata} secondi; poi la scheda finale, ferma 2 secondi: {durata + 2} secondi in tutto.\n')
    if lingua == 'albanese':
        L.append('> **Lingua.** Il copione qui sotto è scritto in italiano. Le parole dette sono in albanese, e un testo albanese '
                 'approvato non esiste ancora. I sottotitoli devono riportare **quello che si sente davvero**, non una traduzione '
                 'fatta a tavolino. Le scritte a schermo sono già in albanese: quelle valgono così come sono.\n')
    L.append('## Sequenza\n')
    for k, s in enumerate(seg, 1):
        L.append(f'### {k} · {s["et"]} · {s["sec"]}\n')
        if s['vede']: L.append(f'- **Si vede:** {s["vede"]}')
        if s['parla']: L.append(f'- **Si dice:** {s["parla"]}')
        if s['schermo']:
            L.append('- **Scritta a schermo:** ' + ' / '.join(f'`{r}`' for r in s['schermo']) + ('  (righe separate)' if len(s['schermo']) > 1 else ''))
        L.append('')
    L.append(f'### {len(seg) + 1} · Scheda finale · dopo l\'ultima parola, 2 secondi\n')
    L.append(f'- **Si vede:** `schede-finali/{scheda}` a tutto schermo, ferma. Niente altro sopra.\n')
    L.append('## Cosa serve per girarlo\n')
    L.append(serve + '\n')
    L.append('## Cosa non si mostra\n')
    L.append('Pelle trattata, prima/dopo, percentuali di risultato, tempi di risultato.\n')
    open(os.path.join(OUT, nome), 'w', encoding='utf8').write('\n'.join(L))
    indice.append((n, nome, titolo, paese, camp, chi, parola, durata))

I = ['# I nove copioni\n',
     'Rev. 2 · 22 ottobre 2026. Uno per file. Si gira **nell\'ordine dei numeri**. Il documento da cui nascono è `../nove-reel.html` '
     '(stampato: `../NOVE-REEL-campagna-500-REV2.pdf`): se cambia il documento, si rilancia `../fai-copioni.py` e questi file si rifanno.\n',
     '| # | File | Titolo | Paese | Campagna | Chi parla | Parola | Copione finisce a |', '|---|---|---|---|---|---|---|---|']
for n, nome, titolo, paese, camp, chi, parola, durata in indice:
    I.append(f'| {n} | `{nome}` | {titolo} | {paese} | {camp} | {chi} | {parola} | {durata}″ |')
I.append('')
I.append('Ogni file ha: i campi fissi in testa, la sequenza (cosa si vede, cosa si dice, cosa appare scritto, secondo per secondo), '
         'e cosa serve per girarlo. La grafica dei testi a schermo e le regole di montaggio sono in `../FLUSSO-TELEGRAM.md`.\n')
open(os.path.join(OUT, '00-LEGGIMI.md'), 'w', encoding='utf8').write('\n'.join(I))
print(len(indice), 'copioni scritti in', OUT)
