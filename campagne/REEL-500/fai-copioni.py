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


# ---- le inserzioni: il testo che accompagna il reel quando diventa pubblicita'
# Testi presi dalla Campagna 500 (campagne/LASER-AFRODITE-500) e accorciati: nel video il messaggio e' gia' detto,
# il testo lo ripete in poche righe e dice cosa fare. Per l'Albania sono scritti in italiano, da approvare e poi tradurre.
NUM = {'Italia': '+39 351 846 6025 (Giorgio)', 'Albania': '+355 69 212 9786 (Uarda)'}
AD = {
    1: ('B · Il rischio ribaltato',
        "Se la tua macchina si ferma domani mattina, quante clienti disdici?\nDa noi, in 48 ore ne hai un'altra in cabina.\n500 € al mese, nessun vincolo. Scrivimi «LASER».",
        'Muletto in 48 ore, sempre'),
    2: ('C · Il metodo compreso',
        "Quante macchine hai visto prendere polvere in un angolo?\nNon è la macchina: è che nessuno ti ha dato il protocollo.\nCon la nostra arriva scritto, con la formazione. 500 € al mese, nessun vincolo. Scrivimi «LASER» e te lo faccio vedere.",
        'La macchina, e il protocollo per usarla'),
    3: ('A · Trenta giorni prima',
        "Il laser arriva il 1. Lo paghi il 30.\nUn mese intero di lavoro prima di tirare fuori il primo euro. Zero anticipo, zero cauzione, nessun vincolo.\n500 € al mese. Scrivimi «LASER».",
        '500 € al mese. Paghi dopo 30 giorni'),
    4: ('A · Trenta giorni prima',
        "La macchina ti arriva il 1 del mese. Paghi il 30.\nTrenta giorni di lavoro prima di tirare fuori il primo lek. Nessun vincolo, nessun anticipo, nessuna cauzione.\n50.000 lekë al mese. Scrivi «LASER».",
        '50.000 Lekë/mese · nessun vincolo'),
    5: ('B · Il rischio non è tuo',
        "La domanda da fare a qualunque fornitore: «Se la macchina si ferma, in quanto tempo ne ho un'altra in cabina?»\nDa noi: 48 ore. Il rischio non è tuo, è nostro.\n50.000 lekë al mese, nessun vincolo. Scrivi «LASER».",
        'Macchina sostitutiva entro 48 ore'),
    6: ('Nuovo · Ultima generazione (non è uno dei quattro angoli della Campagna 500)',
        "Un laser di quattro anni fa non è lo stesso laser.\nLa telecamera guarda la pelle e l'intelligenza artificiale ti propone i parametri: decidi sempre tu. Certificata in Italia, MDR attivo.\n50.000 lekë al mese, nessun vincolo. Scrivi «LASER».",
        'Laser di ultima generazione, con IA'),
    7: ('C · Il metodo compreso (Afrodite)',
        "Tanti centri comprano la macchina e dopo tre mesi la lasciano in un angolo. Non perché non funzioni: perché nessuno ha dato loro il protocollo.\nCon noi arriva il metodo DEMETRA: ciclo di 10-12 sedute, scheda di valutazione, protocollo pagina per pagina.\n50.000 lekë al mese, nessun vincolo. Scrivi «AFRODITE».",
        'La macchina e il metodo per usarla'),
    8: ('Nuovo · Più tecnologie in una macchina (Afrodite)',
        "Cavitazione, radiofrequenza, vacuum. Una macchina sola, una rata sola.\nTi arriva il 1, la paghi il 30. Nessun vincolo, nessun anticipo.\n50.000 lekë al mese. Scrivi «AFRODITE».",
        'Rimodellamento corpo — 50.000 Lekë/mese'),
    9: ('A · Trenta giorni prima (Afrodite)',
        "Nessun anticipo. Nessuna cauzione. Nessun vincolo.\nLa paghi dopo trenta giorni di lavoro. Se si ferma, in 48 ore ne hai un'altra.\n50.000 lekë al mese. Scrivi «AFRODITE».",
        'Arriva il 1, la paghi il 30'),
}

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
    ang, testo_ad, tit_ad = AD[n]
    L.append('## Per l\'inserzione\n')
    if lingua == 'albanese':
        L.append('> Testo scritto in italiano, da approvare. La traduzione in albanese si fa sul testo approvato, non prima.\n')
    L.append(f'- **Angolo:** {ang}')
    L.append('- **Testo principale** (le righe vanno a capo come qui sotto):')
    for r in testo_ad.split('\n'): L.append(f'  > {r}  ')
    L.append(f'- **Titolo:** {tit_ad}  ({len(tit_ad)} caratteri)')
    L.append('- **Pulsante:** Invia messaggio (WhatsApp)')
    L.append(f'- **Messaggio già scritto nella chat:** `{parola}`')
    L.append(f'- **Il numero WhatsApp:** {NUM[paese]}')
    L.append('- **Pubblico, zone e budget:** quelli della Campagna 500 (vedi `../FLUSSO-TELEGRAM.md`, sezione 2). Il video è questo reel, montato, senza cambiare niente.')
    L.append('- **Non si scrive:** il modello del laser, diodi o watt, risultati sulla pelle, percentuali, tempi, confronti con un concorrente.\n')
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
         'il testo dell\'inserzione e cosa serve per girarlo. La grafica dei testi a schermo e le regole di montaggio sono in `../FLUSSO-TELEGRAM.md`. '
         'Tutti i testi delle inserzioni, da copiare in Meta, stanno insieme in `INSERZIONI.md`.\n')
open(os.path.join(OUT, '00-LEGGIMI.md'), 'w', encoding='utf8').write('\n'.join(I))

A = ['# Le nove inserzioni, tutte insieme\n',
     'Per chi carica in Gestione inserzioni di Meta: i testi da copiare, uno per reel. Sono gli stessi che stanno in fondo a ogni copione.\n',
     '**Per tutte:** pulsante **Invia messaggio** (WhatsApp); destinazione WhatsApp, non una pagina web; il messaggio già scritto nella chat è la parola chiave. '
     'Pubblico, zone e budget sono quelli della Campagna 500. **Il modello del laser non si nomina.**\n',
     '| # | Paese | Angolo | Titolo | Caratteri titolo | Parola nella chat |', '|---|---|---|---|---|---|']
A.insert(3, '**Titoli:** tutti sotto i 40 caratteri, così Meta non li taglia.\n')
for n, nome, titolo, paese, camp, chi, parola, durata in indice:
    ang, testo_ad, tit_ad = AD[n]
    A.append(f'| {n} | {paese} | {ang.split(" (")[0]} | {tit_ad} | {len(tit_ad)} | `{parola}` |')
A.append('')
for n, nome, titolo, paese, camp, chi, parola, durata in indice:
    ang, testo_ad, tit_ad = AD[n]
    A.append(f'## Reel {n} · {paese} — {titolo}\n')
    if paese == 'Albania': A.append('*Testo in italiano, da approvare; poi si traduce in albanese.*\n')
    A.append(f'**Angolo:** {ang}  ')
    A.append(f'**Video:** il reel {n}, montato. Copione: `{nome}`  ')
    A.append(f'**Titolo:** {tit_ad}  ')
    A.append(f'**Messaggio nella chat:** `{parola}`  ')
    A.append(f'**WhatsApp:** {NUM[paese]}\n')
    A.append('**Testo principale:**\n')
    for r in testo_ad.split('\n'): A.append(f'> {r}  ')
    A.append('')
open(os.path.join(OUT, 'INSERZIONI.md'), 'w', encoding='utf8').write('\n'.join(A))
print(len(indice), 'copioni scritti in', OUT)
