#!/usr/bin/env python3
"""Il piano delle riprese: tutti e 24 i reel girati in un giorno solo, a blocchi.

Si raggruppano gli stacchi per scena (stesso posto, stessi oggetti) invece che per reel: si prepara la scena una volta e si girano tutte le inquadrature
che la usano, anche di reel diversi. Le battute parlate di Giorgio (o di Uarda) stanno insieme in due blocchi, primo piano e mezzo busto.

La fonte e' reel_sbam_dati.py. Scrive PIANO-RIPRESE.pdf e piano-riprese.md.

Uso:  python3 fai-piano-riprese.py
"""
import html, os, re, subprocess
import reel_sbam_dati as D

QUI = os.path.dirname(os.path.abspath(__file__))
H = os.path.join(QUI, 'piano-riprese.html'); PDF = os.path.join(QUI, 'PIANO-RIPRESE.pdf'); MD = os.path.join(QUI, 'piano-riprese.md')
CHROME = next(p for p in ('/opt/pw-browsers/chromium-1243/chrome-linux64/chrome', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome') if os.path.exists(p))
FONT = os.path.join(QUI, '..', 'REEL-500', 'caratteri', 'archivo.woff2')

if not D.controlla():
    raise SystemExit('I dati dei reel non rispettano le regole: correggi reel_sbam_dati.py')

# ---- i blocchi della giornata, nell'ordine in cui si girano: (sigla, titolo, dove, preparazione)
BLOCCHI = [
    ('C1', 'Giorgio in camera · primo piano', 'Un angolo neutro, luce di finestra davanti, camera all\'altezza degli occhi',
     "Tutte le battute in primo piano, una dopo l'altra. Si comincia da queste: la voce è fresca. Le frasi corte (Fermo!, Falso.) in fondo."),
    ('C2', 'Giorgio in camera · mezzo busto', 'Lo stesso angolo, camera più indietro (dalla vita in su)',
     "Tutte le battute in mezzo busto, una dopo l'altra. Alcune hanno un oggetto in mano o sul tavolo: è scritto nella colonna «Oggetti»."),
    ('A7', 'Giorgio con il dispositivo · mezzo busto', 'In cabina, con il dispositivo accanto o dietro',
     "Come C2, ma con il dispositivo nell'inquadratura. Luce ferma, display acceso."),
    ('A6', 'Il dispositivo in cabina · campo largo', 'In cabina, camera lontana: si vede la stanza',
     "Le inquadrature larghe: il dispositivo, a volte con Giorgio. Una persona sola in scena."),
    ('A5', 'Il dispositivo da vicino', 'In cabina, camera su treppiede, a 10–40 cm',
     "Display, telecamera, manipolo in titanio. Per L2 serve un secondo dispositivo (quello sostitutivo). Nessuna pelle."),
    ('A4', 'Il lettino con i manipoli', 'Lettino con un telo bianco, luce radente',
     "I quattro manipoli di Afrodite appoggiati piano, a ritmo (F2). Niente pelle."),
    ('A3', 'La cabina ferma e il tavolino', 'In cabina: lettino, dispositivo, carrello, un tavolino',
     "Solo per P8 (Cosa manca?). Prima il tavolino VUOTO, poi con il protocollo e la scheda."),
    ('A1', 'Il telo bianco sul dispositivo', 'In cabina, luce bassa',
     "Solo per P2 (Sotto il telo). Giorgio dietro un pannello, sbuca allo stacco 3."),
    ('A2', 'L\'angolo con la polvere', 'Un angolo della stanza, lontano dal dispositivo vero',
     "Solo per P11 (La polvere). Polvere finta (farina o borotalco) sul telo, mai sul dispositivo."),
    ('B1', 'Tavolo · il calendario', 'Un tavolo solido, camera dall\'alto e di fronte',
     "Il calendario a fogli giornalieri (strappo, dito dal 1 al 30) e il palmo sul tavolo."),
    ('B2', 'Tavolo · fogli, cartellini', 'Lo stesso tavolo',
     "Foglio bianco, foglio «VINCOLO» (da strappare), contratto qualunque, foglio con le domande."),
    ('B3', 'Tavolo · timbri e listino', 'Lo stesso tavolo',
     "Il timbro (FALSO, NO, NOI, ESAME FINALE, la riga nuova del listino, dieci timbri sul calendario). Prove su un foglio di scarto prima."),
    ('B4', 'Tavolo · protocolli e schede', 'Lo stesso tavolo',
     "Il protocollo laser (6 pagine), il protocollo Afrodite, la scheda di cabina, la scheda di valutazione."),
    ('B5', 'Tavolo · la scatola', 'Lo stesso tavolo',
     "Solo per P4 (Cosa c'è nella scatola). Dentro: protocollo, scheda di cabina, foglietto con il numero scritto a mano."),
    ('B6', 'Tavolo · la sveglia', 'Lo stesso tavolo',
     "Solo per P6 (Cinque secondi). Una sveglia da tavolo."),
    ('B7', 'Tavolo · altri gesti', 'Lo stesso tavolo',
     "Mani che alzano le dita, i tre appoggi a ritmo di L6."),
    ('E', 'Il telefono · registrazione dello schermo', 'Anche seduti, senza camera: si registra lo schermo',
     "Una chat WhatsApp nuova e vuota (nessuna conversazione vera, nessun numero di clienti)."),
    ('D', 'Il furgone', 'All\'aperto, luce del giorno, in fondo alla giornata',
     "Solo per L2. Il portellone va sbattuto davvero, con la camera già in registrazione. Due riprese."),
    ('V', 'La voce fuori campo', 'Una stanza silenziosa, microfono a 20 cm, a fine giornata',
     "Le battute dei dettagli e dei campi larghi (le mani, gli oggetti, il dispositivo): si girano in silenzio e si dicono dopo, tutte insieme, guardando il video. "
     "Ogni battuta due volte. Dopo ogni colpo (SBAM) la voce aspetta mezzo secondo."),
    ('F', 'La sala della formazione · già girato', 'Materiale del workshop del 26 ottobre',
     "Non si gira: si prende dalle riprese del workshop (partecipanti di spalle, mai volti senza consenso). Per P3."),
]
NOME = {b[0]: b for b in BLOCCHI}

def blocco(c, s):
    v = s['vede'].lower(); inq = s['inq']
    if 'portellone' in v: return 'D'
    if 'sala della formazione' in v or 'formatrice' in v or 'gesto con il manipolo' in v: return 'F'
    if 'polvere' in v: return 'A2'
    if 'telo' in v: return 'A1'
    if 'tavolino' in v or 'cabina ferma' in v: return 'A3'
    if inq == D.PP: return 'C1'
    if inq == D.MB:
        return 'A7' if ('dispositivo' in v or 'display' in v or 'cabina' in v) else 'C2'
    if inq == D.CL: return 'A6'
    # dettagli
    if 'telefono' in v or 'whatsapp' in v: return 'E'
    if 'scatola' in v: return 'B5'
    if 'sveglia' in v: return 'B6'
    if 'lettino' in v and 'manipol' in v: return 'A4'
    if 'tre appoggi' in v: return 'B7'
    if 'adesivo' in v: return 'A5'
    if ('timbro' in v and 'senza timbro' not in v) or 'listino' in v: return 'B3'
    if 'protocollo' in v or 'scheda' in v or 'fascicolo' in v: return 'B4'
    if 'calendario' in v or 'pagine dal 1' in v: return 'B1'
    if 'foglio' in v or 'fogli' in v or 'contratto' in v: return 'B2'
    if 'display' in v or 'telecamera' in v or 'obiettivo' in v or 'manipolo' in v or 'dispositivo' in v: return 'A5'
    return 'B7'

OGGETTI = [('calendario', 'calendario'), ('foglio', 'foglio'), ('contratto', 'contratto'), ('scatola', 'scatola'), ('telefono', 'telefono'), ('timbro', 'timbro'),
           ('sveglia', 'sveglia'), ('protocollo', 'protocollo'), ('scheda', 'scheda'), ('listino', 'listino'), ('adesivo', 'adesivo'), ('polvere', 'polvere'),
           ('dita', 'dita'), ('dito', 'dito'), ('palmo', 'palmo'), ('manipol', 'manipoli'), ('telo', 'telo'), ('pagine', 'pagine strappate')]
def oggetti(vede):
    v = vede.lower(); out = []
    for k, n in OGGETTI:
        if k in v and n not in out: out.append(n)
    return ', '.join(out) or '—'

# ---- raggruppo
TUTTI = {c: D.stacchi(c) for c in D.CODICI}
for _c in TUTTI:
    for _s in TUTTI[_c]: _s['c'] = _c
FUORI = lambda s: (s['inq'] in (D.DET, D.CL) or blocco(s['c'], s) == 'F') and bool(s['parla'])   # mani, oggetti, campo largo, materiale del workshop: la voce si registra dopo
gruppi = {b[0]: [] for b in BLOCCHI}
for c in D.CODICI:
    for s in TUTTI[c]:
        gruppi[blocco(c, s)].append((c, s))
tot_stacchi = sum(len(v) for v in gruppi.values())
assert tot_stacchi == sum(len(D.stacchi(c)) for c in D.CODICI)
gruppi['V'] = [(c, s) for c in D.CODICI for s in TUTTI[c] if FUORI(s)]

PARLATE = lambda g: sum(1 for c, s in g if s['parla'] and not FUORI(s))
def dice(s):
    if FUORI(s): return '<fuori campo: blocco V>'
    return ('«' + s['parla'] + '»') if s['parla'] else '(in silenzio)'
def minuti(sigla, g):
    """Stima: prepara la scena 10 min, poi per ogni inquadratura 1,5 min se si parla in camera, 2 min per un dettaglio o un campo largo in silenzio,
    3 min se c'e' un oggetto o un gesto da preparare; la voce fuori campo, 1 min a battuta."""
    if sigla == 'F': return 0
    if sigla == 'V': return int(round(10 + 1.0 * len(g)))
    per = sum((1.5 if sigla in ('C1', 'C2') else 2.0 if sigla in ('A7', 'A6', 'A5') else 3.0) for _ in g)
    return int(round(10 + per))

TOT_MIN = sum(minuti(b[0], gruppi[b[0]]) for b in BLOCCHI)
MATTINA = ['C1', 'C2', 'A7', 'A6', 'A5', 'A4', 'A3', 'A1', 'A2']; POMERIGGIO = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'E', 'D', 'V']
MIN_M = sum(minuti(b, gruppi[b]) for b in MATTINA); MIN_P = sum(minuti(b, gruppi[b]) for b in POMERIGGIO)
def ore(m): return f'{m // 60} ore e {m % 60} minuti'
DUE_META = (f'Se un giorno solo è troppo lungo, si divide a metà. **Mattina** (il parlato e la cabina: blocchi {", ".join(MATTINA)}): circa {ore(MIN_M)}. '
            f'**Pomeriggio** (il tavolo, il telefono, il furgone e la voce fuori campo: blocchi {", ".join(POMERIGGIO)}): circa {ore(MIN_P)}.')

REGOLE_GIORNO = [
    "Verticale 9:16, 1080 × 1920, 30 fotogrammi al secondo, camera su treppiede (tranne dove è scritto). Telefono in modalità «aereo» e luce fissa, non automatica.",
    "Ogni inquadratura si gira due volte almeno. Si parte 1 secondo prima e si finisce 1 secondo dopo: il montaggio ha bisogno di quel margine.",
    "Si dice la battuta come sta scritta, con le pause scritte. Il montaggio taglia, non allunga. Se una frase non esce in tempo, si dice due volte e si sceglie dopo.",
    "L'audio si registra pulito, con il microfono vicino (anche quello del telefono, a 40 cm). Dopo ogni blocco, 10 secondi di silenzio della stanza (serve al montaggio).",
    "Il colpo (SBAM) si gira, ma il suono lo mette il montaggio (cartella suoni/): niente si rompe e niente cade davvero. Dove c'è un suono vero (portellone, timbro, strappo) lo si registra comunque.",
    "Ogni file si chiama con il codice del reel e il numero dello stacco: «L1-2» è il reel L1, stacco 2. Nel canale Telegram la didascalia è la stessa, senza altro.",
    "Nessuna pelle trattata, nessuna cliente in campo, nessun volto senza consenso.",
]

MATERIALE = [
    ("Il dispositivo", "Laser acceso e spento. Un secondo dispositivo accanto, per il display sostitutivo (L2). I quattro manipoli di Afrodite."),
    ("Carta", "Calendario a fogli giornalieri (un foglio per giorno, dal 1 al 30, senza mese né anno). Fogli bianchi e un pennarello grosso. Un foglio con scritto «VINCOLO». Un contratto qualunque, anche vuoto. Un listino dei trattamenti finto."),
    ("Protocolli", "Protocollo laser (6 pagine, IT). Protocollo Afrodite, scheda di cabina, scheda di valutazione, stampati."),
    ("Timbri", "Un timbro e un tampone rosso. Le parole: FALSO, NO, NOI, ESAME FINALE (anche con un solo timbro e adesivi, se il montaggio aggiunge la parola). Un foglio di scarto per le prove."),
    ("Oggetti di scena", "Una scatola di cartone. Un foglietto con il numero. Una sveglia da tavolo. Un adesivo «500 €» (in Albania «50.000 LEKË») e un cartellino bianco. Un telo bianco grande. Un telo grigio con polvere finta (farina o borotalco)."),
    ("Telefono", "Un telefono con una chat WhatsApp di NIPEC nuova e vuota, per registrare lo schermo."),
    ("Il posto", "Una cabina con lettino, carrello, tavolino. Un tavolo solido. Un angolo neutro con luce di finestra. Il furgone."),
    ("Tecnica", "Treppiede, microfono, una luce morbida, un pannello per nascondere Giorgio (P2), fogli di scarto."),
]

def e(t): return html.escape(t, quote=False)

# ---- markdown
L = ['# Piano delle riprese · ventiquattro reel in un giorno\n',
     f'Seconda stesura, 3 novembre 2026. Generato da `reel_sbam_dati.py`. **{tot_stacchi} inquadrature in {sum(1 for b in BLOCCHI if gruppi[b[0]])} blocchi.** '
     f'Stima: circa **{ore(TOT_MIN)}** di lavoro (preparazione di ogni scena compresa), pause escluse. È una stima: si conferma sul posto. ' + DUE_META.replace('**', '**') + '\n',
     '## Le regole del giorno\n'] + [f'- {x}' for x in REGOLE_GIORNO]
L += ['\n## Cosa si porta\n'] + [f'- **{k}.** {v}' for k, v in MATERIALE]
L += ['\n## Per Uarda (Albania)\n',
      'Stesse inquadrature, stesso ordine. Cambiano: le battute (versioni albanesi, bozze, nelle tabelle dei copioni `copioni/*.md`), il prezzo sull\'adesivo («50.000 LEKË»), '
      'il numero sul foglietto di P4 e sullo schermo di P7 (+355 69 212 9786). I reel della pagina che girano anche in Albania: P4, P7, P9. Gli altri sono di Giorgio.\n']
for sigla, titolo, dove, prep in BLOCCHI:
    g = gruppi[sigla]
    if not g: continue
    if sigla == 'V':
        L += [f'\n## Blocco V · {titolo}\n', f'**Dove:** {dove}  ', f'**Come:** {prep}  ', f'**Battute:** {len(g)} · **Stima:** {minuti(sigla, g)} min\n',
              '| File | Si dice | Dura | Dopo il colpo |', '|---|---|---|---|']
        for c, s in g:
            L.append(f'| **{c}-{s["n"]}** | «{s["parla"]}» | {D.fmt(s["dur"])} s | {"aspetta mezzo secondo" if s["suono"].startswith("SBAM") else ""} |')
        continue
    L += [f'\n## Blocco {sigla} · {titolo}\n', f'**Dove:** {dove}  ', f'**Come:** {prep}  ',
          f'**Inquadrature:** {len(g)} ({PARLATE(g)} con la voce) · **Stima:** {minuti(sigla, g)} min\n',
          '| File | Inq. | Si vede | Si dice | Oggetti | Dura | Colpo |', '|---|---|---|---|---|---|---|']
    for c, s in sorted(g, key=lambda x: (D.CODICI.index(x[0]), x[1]['n'])):
        colpo = 'SBAM' if s['suono'].startswith('SBAM') else ''
        L.append(f'| **{c}-{s["n"]}** | {s["inq"]} | {s["vede"].replace("|", "/")} | {dice(s)} | {oggetti(s["vede"])} | {D.fmt(s["dur"])} s | {colpo} |')
L += ['\n## Lista di controllo, reel per reel\n', 'Si segna lo stacco quando è girato.\n', '| Reel | Titolo | Stacchi |', '|---|---|---|']
for c in D.CODICI:
    n = len(D.stacchi(c))
    L.append(f'| {c} | {D.R[c]["titolo"]} | ' + ' '.join(f'☐ {c}-{k}' for k in range(1, n + 1)) + ' |')
open(MD, 'w', encoding='utf8').write('\n'.join(L) + '\n')

# ---- pdf
def tab(sigla):
    g = sorted(gruppi[sigla], key=lambda x: (D.CODICI.index(x[0]), x[1]['n']))
    righe = ['<tr><th style="width:7%">File</th><th style="width:9%">Inq.</th><th style="width:33%">Si vede</th><th style="width:27%">Si dice</th><th style="width:14%">Oggetti</th><th style="width:5%">Dura</th><th>Colpo</th></tr>']
    for c, s in g:
        parla = '<span class="fab">fuori campo · blocco V</span>' if FUORI(s) else (f'<b class="parla">«{e(s["parla"])}»</b>' if s['parla'] else '<span class="fab">(in silenzio)</span>')
        colpo = '<b class="sbam">SBAM</b>' if s['suono'].startswith('SBAM') else ''
        righe.append(f'<tr><td><b class="cod">{c}-{s["n"]}</b></td><td>{s["inq"]}</td><td>{e(s["vede"])}</td><td>{parla}</td><td class="fab">{e(oggetti(s["vede"]))}</td><td class="c">{D.fmt(s["dur"])}″</td><td>{colpo}</td></tr>')
    return '<table class="rip">' + ''.join(righe) + '</table>'

def tab_v():
    righe = ['<tr><th style="width:8%">File</th><th>Si dice</th><th style="width:8%">Dura</th><th style="width:22%">Dopo il colpo</th></tr>']
    for c, s in gruppi['V']:
        righe.append(f'<tr><td><b class="cod">{c}-{s["n"]}</b></td><td><b class="parla">«{e(s["parla"])}»</b></td><td class="c">{D.fmt(s["dur"])}″</td>'
                     f'<td>{"<b class=sbam>aspetta mezzo secondo</b>" if s["suono"].startswith("SBAM") else ""}</td></tr>')
    return '<table class="rip">' + ''.join(righe) + '</table>'

corpo = ''
for sigla, titolo, dove, prep in BLOCCHI:
    g = gruppi[sigla]
    if not g: continue
    corpo += (f'<div class="blocco"><div class="cima"><span class="n3">Blocco {sigla}</span><span class="tt">{e(titolo)}</span>'
              f'<span class="stima">{len(g)} {"battute" if sigla == "V" else "inquadrature"} · {minuti(sigla, g)} min</span></div>'
              f'<p class="prep"><b>Dove.</b> {e(dove)}. <b>Come.</b> {e(prep)}</p>{tab_v() if sigla == "V" else tab(sigla)}</div>')
spunte = ''.join(f'<tr><td class="c"><b>{c}</b></td><td>{e(D.R[c]["titolo"])}</td><td class="box">' + ' '.join(f'<span class="sp">☐ {k}</span>' for k in range(1, len(D.stacchi(c)) + 1)) + '</td></tr>' for c in D.CODICI)

doc = f'''<!doctype html>
<html lang="it"><head><meta charset="utf-8"><title>Piano delle riprese · NIPEC</title>
<style>
@font-face{{font-family:"Archivo";src:url("{FONT}") format("woff2");font-weight:400 700}}
:root{{--blu:#1C6EA4;--navy:#123A63;--velo:#E8F0F7;--ink:#17222E;--ink2:#44535F;--grigio:#8E9295;--riga:#D9E2E9;--rosso:#9C3A28;--verde:#1B6E52;--verde-velo:#E2F1EA}}
@page{{size:A4;margin:14mm 13mm 16mm}}
*{{box-sizing:border-box}}
body{{margin:0;font:400 9pt/1.45 "Archivo","Helvetica Neue",Arial,sans-serif;color:var(--ink);-webkit-print-color-adjust:exact;print-color-adjust:exact}}
h1{{font-size:21pt;font-weight:700;margin:0 0 2px;color:var(--navy);letter-spacing:-.01em;line-height:1.1}}
.sotto{{font-size:9.5pt;font-weight:600;color:var(--blu);margin:0 0 4px}}
.rev{{font-size:8pt;color:var(--grigio);margin:0 0 14px;border-bottom:2.5px solid var(--blu);padding-bottom:9px}}
h2{{font-size:12pt;font-weight:700;color:var(--navy);margin:16px 0 7px;padding-bottom:4px;border-bottom:1px solid var(--riga);page-break-after:avoid}}
p{{margin:0 0 7px}} b{{font-weight:600;color:var(--navy)}} ul{{margin:0 0 8px;padding-left:16px}} li{{margin-bottom:4px}}
table{{width:100%;border-collapse:collapse;font-size:8.3pt;margin:4px 0 8px}}
th{{background:#EAF2FA;color:var(--navy);text-align:left;padding:4px 6px;font-size:7.2pt;font-weight:600;text-transform:uppercase;letter-spacing:.07em}}
td{{padding:4px 6px;border-bottom:1px solid var(--riga);vertical-align:top;line-height:1.35}}
td.c{{text-align:center}}
.blocco{{margin:0 0 12px;border:1px solid var(--riga);border-radius:3px;page-break-inside:auto}}
.cima{{display:flex;align-items:baseline;gap:12px;background:var(--velo);padding:6px 10px;border-bottom:1px solid var(--riga);page-break-after:avoid}}
.n3{{font-size:7.6pt;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--blu);white-space:nowrap}}
.tt{{font-size:11pt;font-weight:700;color:var(--navy)}} .stima{{margin-left:auto;font-size:8pt;color:var(--grigio);white-space:nowrap}}
.prep{{padding:7px 10px 2px;margin:0;font-size:8.8pt;page-break-after:avoid}}
tr{{page-break-inside:avoid}}
.cod{{color:var(--navy);white-space:nowrap}} .parla{{font-weight:600}} .fab{{color:var(--grigio)}} .sbam{{color:var(--rosso)}}
.box{{line-height:1.7}} .sp{{display:inline-block;margin-right:7px;white-space:nowrap}}
.nota{{border:1px solid var(--riga);border-left:4px solid var(--blu);background:#FBFDFE;padding:8px 12px;margin:9px 0;font-size:8.8pt}}
</style></head><body>
<h1>Piano delle riprese</h1>
<p class="sotto">Ventiquattro reel SBAM, girati in un giorno solo · per scena, non per reel</p>
<p class="rev">NIPEC · 3 novembre 2026 · {tot_stacchi} inquadrature · circa {ore(TOT_MIN)} (stima)</p>
<div class="nota">{DUE_META.replace("**", "")}</div>
<div class="nota">Si prepara la scena una volta e si girano tutte le inquadrature che la usano, anche di reel diversi. Si comincia dal parlato in camera (la voce è fresca), poi la cabina, poi il tavolo, poi il telefono, il furgone, e a fine giornata la voce fuori campo.</div>
<h2>Le regole del giorno</h2><ul>{''.join(f'<li>{e(x)}</li>' for x in REGOLE_GIORNO)}</ul>
<h2>Cosa si porta</h2><ul>{''.join(f'<li><b>{e(k)}.</b> {e(v)}</li>' for k, v in MATERIALE)}</ul>
<h2>Per Uarda (Albania)</h2>
<p>Stesse inquadrature, stesso ordine. Cambiano: le battute (versioni albanesi, bozze, nelle tabelle dei copioni), il prezzo sull'adesivo («50.000 LEKË»), il numero sul foglietto di P4 e sullo schermo di P7 (+355 69 212 9786). I reel della pagina che girano anche in Albania: P4, P7, P9. Gli altri sono di Giorgio.</p>
<h2>I blocchi, nell'ordine della giornata</h2>
{corpo}
<h2>Lista di controllo, reel per reel</h2>
<table><tr><th style="width:6%">Reel</th><th style="width:26%">Titolo</th><th>Stacchi girati</th></tr>{spunte}</table>
</body></html>
'''
open(H, 'w', encoding='utf8').write(doc)
subprocess.run([CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer', '--allow-file-access-from-files',
                f'--print-to-pdf={PDF}', '--virtual-time-budget=8000', 'file://' + H], check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
print('piano:', PDF)
for sigla, titolo, *_ in BLOCCHI:
    g = gruppi[sigla]
    print(f'  {sigla:3s} {titolo[:48]:48s} {len(g):3d} inquadrature ({PARLATE(g)} parlate) · {minuti(sigla, g)} min')
print(f'  totale {tot_stacchi} inquadrature, circa {TOT_MIN} min')
