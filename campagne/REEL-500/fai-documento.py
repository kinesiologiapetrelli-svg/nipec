#!/usr/bin/env python3
"""Rifa nel documento stampato (nove-reel.html) le tabelle dei reel, stacco per stacco, dagli stessi dati dei copioni.

Sostituisce solo le sezioni 2, 3, 4 (i nove reel) e 5 (cosa serve avere in mano); il resto del documento resta com'e'.
Poi stampa il PDF.

Uso:  python3 fai-documento.py
"""
import html, os, re, subprocess
import reel_dati as R

QUI = os.path.dirname(os.path.abspath(__file__))
H = os.path.join(QUI, 'nove-reel.html')
PDF = os.path.join(QUI, 'NOVE-REEL-campagna-500-REV3.pdf')
CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'

if not R.controlla():
    raise SystemExit('I dati dei reel non rispettano la regola dei 5 secondi: correggi reel_dati.py')

s = open(H, encoding='utf8').read()

def e(t): return html.escape(t, quote=False)

def sostituisci(vecchio, nuovo):
    global s
    if vecchio in s: s = s.replace(vecchio, nuovo)

def blocco_reel(n):
    paese, camp, chi, lingua, parola, scheda, gancio = R.META[n]
    st = R.stacchi(n); fine = st[-1]['t1']
    righe = ['<tr><th style="width:3%">#</th><th style="width:9%">Tempo</th><th style="width:10%">Inquadr.</th>'
             '<th style="width:24%">Si vede</th><th style="width:28%">Si dice</th><th>Scritta a schermo</th></tr>']
    for x in st:
        parla = f'<b class="parla">«{e(x["parla"])}»</b>' if x['parla'] else '<span class="fab">(in silenzio)</span>'
        sch = '<br>'.join(f'<span class="schermo">{e(r)}</span>' for r in x['schermo']) or '<span class="fab">—</span>'
        righe.append(f'<tr><td class="c">{x["n"]}</td><td><span class="sec">{R.fmt(x["t0"])}–{R.fmt(x["t1"])}″</span></td>'
                     f'<td><b>{x["inq"]}</b></td><td>{e(x["vede"])}</td><td>{parla}</td><td>{sch}</td></tr>')
        if x['n'] == gancio:
            righe.append('<tr class="gancio"><td colspan="6">▲ fine dei primi 5 secondi: il gancio è tutto qui</td></tr>')
    righe.append(f'<tr><td class="c">{len(st) + 1}</td><td><span class="sec">{R.fmt(fine)}–{R.fmt(fine + 2)}″</span></td><td><b>Scheda finale</b></td>'
                 f'<td colspan="3">Subito dopo l\'ultima parola, a tutto schermo, ferma 2 secondi: <b>{scheda}</b></td></tr>')
    righe.append(f'<tr><td class="ser" colspan="6"><b>Serve:</b> {e(R.SERVE[n])}</td></tr>')
    for nota in R.NOTE.get(n, []):
        righe.append(f'<tr><td class="att" colspan="6"><b>Attenzione:</b> {e(nota)}</td></tr>')
    return (f'<div class="reel">\n  <div class="cima"><span class="n3">Reel {n} · {paese} · {R.fmt(fine)}″ + 2″</span>'
            f'<span class="tt">{e(R.TITOLO[n])}</span></div>\n  <div class="corpo"><table class="stacchi">\n    '
            + '\n    '.join(righe) + '\n  </table></div>\n</div>\n')

reel_html = ('<h2><span class="n">2</span>Laser Italia — tre reel</h2>\n'
             '<p class="quando">Parla Giorgio · nessuno stacco oltre i 5 secondi, poi cambia inquadratura</p>\n\n'
             + '\n'.join(blocco_reel(n) for n in (1, 2, 3))
             + '\n<h2><span class="n">3</span>Laser Albania — tre reel</h2>\n'
             '<p class="quando">Parla Uarda · copioni scritti in italiano, si traducono sul testo approvato · in albanese le frasi sono di solito un po\' più lunghe: '
             'uno stacco non supera comunque i 5 secondi</p>\n\n'
             + '\n'.join(blocco_reel(n) for n in (4, 5, 6))
             + '\n<h2><span class="n">4</span>Afrodite Albania — tre reel</h2>\n\n'
             + '\n'.join(blocco_reel(n) for n in (7, 8, 9)) + '\n')

a = s.index('<h2><span class="n">2</span>Laser Italia — tre reel</h2>')
b = re.search(r'<h2[^>]*><span class="n">5</span>', s).start()
s = s[:a] + reel_html + s[b:]

# sezione 5: cosa serve avere in mano
cinque = '''<h2 class="nuovo-foglio"><span class="n">5</span>Cosa serve avere in mano</h2>

<p>Ogni stacco è <b>un gesto e una frase</b>: si gira a pezzi, uno alla volta, nell'ordine dei copioni. Prima di cominciare, ecco cosa deve esserci sul set.</p>

<table>
  <tr><th style="width:74%">Cosa</th><th>Serve nei reel</th></tr>
  <tr><td>Una macchina in cabina, accesa, con il display illuminato</td><td>4 · 5 · 6 · 7 · 8</td></tr>
  <tr><td><b>Il furgone che si apre, la macchina che scende</b></td><td>5</td></tr>
  <tr><td>Due macchine nella stessa inquadratura</td><td>1</td></tr>
  <tr><td><b>Una macchina nuova, ancora imballata, con la pellicola sul display</b></td><td>6</td></tr>
  <tr><td>Dettagli del laser: display touch, telecamera, manipolo in titanio</td><td>6</td></tr>
  <tr><td><b>Un telo che copre una macchina in un angolo, luce bassa</b></td><td>2 · 7</td></tr>
  <tr><td>Il protocollo laser stampato (6 pagine, IT)</td><td>2</td></tr>
  <tr><td>Il protocollo Afrodite e la scheda di cabina stampati</td><td>7</td></tr>
  <tr><td>Un calendario da muro grande, senza mese e senza anno stampati</td><td>3</td></tr>
  <tr><td>I manipoli Afrodite allineati, luce radente</td><td>8</td></tr>
  <tr><td>Un foglio bianco</td><td>9</td></tr>
  <tr><td>La scheda finale (PNG pronta, in <b>schede-finali/</b>)</td><td>tutti e nove</td></tr>
</table>

'''
a = re.search(r'<h2[^>]*><span class="n">5</span>', s).start()
b = s.index('<div class="box verde">\n  <span class="eti">Le tre immagini')
s = s[:a] + cinque + s[b:]

# regola dei 5 secondi: le due meta'
sostituisci('Rev. 2 · 22 ottobre 2026', 'Rev. 3 · 22 ottobre 2026')
sostituisci('Nove reel · Campagna 500 · Rev. 2', 'Nove reel · Campagna 500 · Rev. 3')
sostituisci('<title>Nove reel · Campagna 500 · Rev. 2 · NIPEC</title>', '<title>Nove reel · Campagna 500 · Rev. 3 · NIPEC</title>')

if 'La regola dei 5 secondi vale per tutto il reel' not in s:
    sostituisci('<span class="eti">Cosa è cambiato dal 16 ottobre</span>\n  <p>',
                '<span class="eti">Cosa è cambiato dal 16 ottobre</span>\n'
                '  <p><b>La regola dei 5 secondi vale per tutto il reel.</b> Nessuno stacco dura più di 5 secondi: poi si cambia stacco '
                '<b>e inquadratura</b>. Ogni reel è scritto stacco per stacco (sezioni 2, 3, 4).</p>\n  <p style="margin-top:5px">')

sostituisci("<tr><td class=\"t\"><b>Durata</b></td><td><b>15-22 secondi.</b> Oltre, si perde l'estetista che scorre</td></tr>",
            "<tr><td class=\"t\"><b>Durata</b></td><td>Obiettivo <b>15-22 secondi</b>, oltre si perde l'estetista che scorre. Contati stacco per stacco, i reel finiscono tra 19 e 25 secondi "
            "(più 2 di scheda finale): il 2 e il 7 sono sopra e hanno un taglio proposto</td></tr>")
if 'Gli stacchi</b>' not in s:
    sostituisci('<tr><td class="t"><b>Audio</b></td>',
                '<tr><td class="t"><b>Gli stacchi</b></td><td><b>Nessuno stacco dura più di 5 secondi.</b> Poi si cambia stacco e inquadratura: primo piano, mezzo busto, dettaglio, campo largo. Mai due uguali di fila. È ciò che rende il reel dinamico e semplice da girare</td></tr>\n  <tr><td class="t"><b>Audio</b></td>')

for et in ('detta bene', 'in due metà'):
    pass
i = s.find('<span class="eti">La regola dei 5 secondi, detta bene</span>')
if i < 0:
    i = s.index('<span class="eti">La regola dei 5 secondi, in due metà</span>')
j = s.index('</div>', i)
s = s[:i] + '''<span class="eti">La regola dei 5 secondi, in due metà</span>
  <p><b>1. I primi 5 secondi.</b> Non è «un gancio»: nei primi 5 secondi si vede <b>un vantaggio che l'estetista riconosce come suo.</b> Non la macchina, non il marchio, non il prezzo —
  un problema che ha davvero, detto con le sue parole. Per questo ogni reel apre con una <b>domanda o una frase scomoda</b>, mai con «siamo NIPEC e noleggiamo laser».</p>
  <p style="margin-top:5px"><b>2. Ogni stacco.</b> <b>Nessuno stacco dura più di 5 secondi.</b> Poi si cambia stacco e inquadratura. Il reel resta dinamico alla vista, e ogni pezzo è semplice da girare:
  un gesto, una frase breve. Se una frase non ci sta, si divide in due stacchi: non si accelera.</p>
''' + s[j:]

sostituisci('Stacco ogni <b>2-3 secondi</b> nei primi cinque. Testo a schermo che <b>entra con la\n  parola</b>',
            'Nessuno stacco oltre <b>5 secondi</b>, mai due inquadrature uguali di fila. Testo a schermo che <b>entra con la\n  parola</b>')

# stile
css = '''/* ---------- stacco per stacco ---------- */
.reel table.stacchi{font-size:7.6pt}
.stacchi th{background:#EAF2FA;color:#123A63;font-size:6.8pt;padding:4px 6px;letter-spacing:.06em}
.stacchi td{padding:3px 6px;line-height:1.32}
.stacchi td.c{text-align:center;font-family:"Archivo",sans-serif;font-weight:700;color:#123A63}
.stacchi tr.gancio td{background:#E2F1EA;color:#1B6E52;font-family:"Archivo",sans-serif;font-size:6.8pt;font-weight:700;letter-spacing:.1em;text-transform:uppercase;padding:2px 6px;text-align:center}
.stacchi td.ser{background:#FBFDFE;color:#44535F;font-size:7.6pt}
.stacchi td.att{background:#F8EFDB;color:#6B4A05;font-size:7.6pt}
.stacchi .parla{font-weight:600}
.stacchi .schermo{display:inline-block;margin:1px 0;font-size:6.8pt;padding:2px 5px}
'''
m = '/* ---------- stacco per stacco ---------- */'
if m in s:
    a0 = s.index(m); b0 = s.index('</style>', a0)
    s = s[:a0] + css + s[b0:]
else:
    s = s.replace('</style>', '\n' + css + '</style>', 1)
open(H, 'w', encoding='utf8').write(s)

if os.path.exists(os.path.join(QUI, 'NOVE-REEL-campagna-500-REV2.pdf')):
    os.remove(os.path.join(QUI, 'NOVE-REEL-campagna-500-REV2.pdf'))
subprocess.run([CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer',
                f'--print-to-pdf={PDF}', '--virtual-time-budget=8000', 'file://' + H], check=True,
               stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
print('documento rifatto:', PDF)
