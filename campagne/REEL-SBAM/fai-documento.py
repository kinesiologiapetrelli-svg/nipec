#!/usr/bin/env python3
"""Stampa VENTIQUATTRO-REEL-SBAM.pdf dagli stessi dati dei copioni (reel_sbam_dati.py): i due non possono dire cose diverse.

Uso:  python3 fai-documento.py
"""
import html, os, subprocess
import reel_sbam_dati as D

QUI = os.path.dirname(os.path.abspath(__file__))
H = os.path.join(QUI, 'ventiquattro-reel-sbam.html')
PDF = os.path.join(QUI, 'VENTIQUATTRO-REEL-SBAM.pdf')
CHROME = next(p for p in ('/opt/pw-browsers/chromium-1243/chrome-linux64/chrome', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome') if os.path.exists(p))
FONT = os.path.join(QUI, '..', 'REEL-500', 'caratteri', 'archivo.woff2')

if not D.controlla():
    raise SystemExit('I dati dei reel non rispettano le regole: correggi reel_sbam_dati.py')

def e(t): return html.escape(t, quote=False)

def reel(c):
    r = D.R[c]; st = D.stacchi(c); fine = D.fine(c); g = r['gancio']
    righe = ['<tr><th style="width:3%">#</th><th style="width:9%">Tempo</th><th style="width:9%">Inquadr.</th><th style="width:25%">Si vede</th>'
             '<th style="width:24%">Si dice</th><th style="width:16%">Scritta</th><th>Suono</th></tr>']
    for s in st:
        parla = f'<b class="parla">«{e(s["parla"])}»</b>' if s['parla'] else '<span class="fab">(in silenzio)</span>'
        sch = '<br>'.join(f'<span class="schermo">{e(x)}</span>' for x in s['schermo']) or '<span class="fab">—</span>'
        suono = f'<b class="sbam">{e(s["suono"])}</b>' if s['suono'].startswith('SBAM') else f'<span class="fab">{e(s["suono"])}</span>'
        righe.append(f'<tr><td class="c">{s["n"]}</td><td><span class="sec">{D.fmt(s["t0"])}–{D.fmt(s["t1"])}″</span></td><td><b>{s["inq"]}</b></td>'
                     f'<td>{e(s["vede"])}</td><td>{parla}</td><td>{sch}</td><td>{suono}</td></tr>')
        if s['n'] == g:
            righe.append('<tr class="gancio"><td colspan="7">▲ fine dei primi 5 secondi: il gancio è tutto qui</td></tr>')
    righe.append(f'<tr><td class="c">{len(st) + 1}</td><td><span class="sec">{D.fmt(fine)}–{D.fmt(fine + 2)}″</span></td><td><b>Scheda finale</b></td>'
                 f'<td colspan="4">A tutto schermo, ferma 2 secondi. Niente altro sopra.</td></tr>')
    righe.append(f'<tr><td class="ser" colspan="7"><b>Serve:</b> {e(r["serve"])}</td></tr>')
    for n in r['note']: righe.append(f'<tr><td class="att" colspan="7"><b>Attenzione:</b> {e(n)}</td></tr>')
    if r['serie'] == 'A':
        testo, tit = r['ad']
        righe.append(f'<tr><td class="ad" colspan="7"><b>Inserzione.</b> Titolo: <b>{e(tit)}</b> ({len(tit)} car.) · pulsante «Invia messaggio» (WhatsApp) · parola nella chat: <b>{r["parola"]}</b><br>'
                     + '<br>'.join(e(x) for x in testo.split('\n')) + '</td></tr>')
    else:
        righe.append(f'<tr><td class="ad" colspan="7"><b>Didascalia.</b> {e(r["didascalia"])}</td></tr>')
    righe.append(f'<tr><td class="cb" colspan="7"><b>Cosa è cambiato.</b> {e(r["cambi"])}</td></tr>')
    alb = ''
    if r['serie'] == 'A':
        rr = ''.join(f'<tr><td class="c">{k}</td><td>{e(p) if p else "<span class=fab>(në heshtje)</span>"}</td><td>{("<span class=schermo>" + e(sc) + "</span>") if sc else "<span class=fab>—</span>"}</td></tr>'
                     for k, (p, sc) in enumerate(r['albanese'], 1))
        alb = (f'<table class="alb"><tr><th style="width:3%">#</th><th>Versione albanese (bozza, da far controllare a Uarda)</th><th style="width:38%">Scritta</th></tr>{rr}</table>')
    return (f'<div class="reel">\n  <div class="cima"><span class="n3">{c} · {"adv " + r["campagna"] if r["serie"] == "A" else "pagina"} · {D.fmt(fine)}″ + 2″</span>'
            f'<span class="tt">{e(r["titolo"])}</span></div>\n  <p class="conc"><b>Il colpo.</b> {e(r["concetto"])} <span class="chi">Parla: {e(r["chi"])}. Copertina: {e(r["copertina"])}</span></p>\n'
            f'  <table class="stacchi">\n    ' + '\n    '.join(righe) + f'\n  </table>\n  {alb}\n</div>\n')

def sezione(codici): return ''.join(reel(c) for c in codici)
def tab(codici):
    return ''.join(f'<tr><td class="c"><b>{c}</b></td><td><b>{e(D.R[c]["titolo"])}</b></td><td>{e(D.COLPO[c])}</td><td class="c">{D.fmt(D.fine(c))}″</td></tr>' for c in codici)
def lista(v): return ''.join(f'<li><b>{e(k)}.</b> {e(t)}</li>' for k, t in v)

regole = ''.join(f'<li>{e(x)}</li>' for x in D.REGOLE)
decisioni = ''.join(f'<li><b>{e(d)}.</b> {e(x)}</li>' for d, x in D.DECISIONI)

doc = f'''<!doctype html>
<html lang="it"><head><meta charset="utf-8"><title>Ventiquattro reel SBAM · NIPEC</title>
<style>
@font-face{{font-family:"Archivo";src:url("{FONT}") format("woff2");font-weight:400 700}}
:root{{--blu:#1C6EA4;--navy:#123A63;--velo:#E8F0F7;--ink:#17222E;--ink2:#44535F;--grigio:#8E9295;--riga:#D9E2E9;--rosso:#9C3A28;--rosso-velo:#FAEAE6;--giallo-velo:#F8EFDB;--giallo:#6B4A05;--verde:#1B6E52;--verde-velo:#E2F1EA}}
@page{{size:A4;margin:14mm 13mm 16mm}}
*{{box-sizing:border-box}}
body{{margin:0;font:400 9pt/1.45 "Archivo","Helvetica Neue",Arial,sans-serif;color:var(--ink);-webkit-print-color-adjust:exact;print-color-adjust:exact}}
h1{{font-size:21pt;font-weight:700;margin:0 0 2px;color:var(--navy);letter-spacing:-.01em;line-height:1.1}}
.sotto{{font-size:9.5pt;font-weight:600;color:var(--blu);margin:0 0 4px}}
.rev{{font-size:8pt;color:var(--grigio);margin:0 0 14px;border-bottom:2.5px solid var(--blu);padding-bottom:9px}}
h2{{font-size:12pt;font-weight:700;color:var(--navy);margin:18px 0 7px;padding-bottom:4px;border-bottom:1px solid var(--riga);page-break-after:avoid}}
p{{margin:0 0 7px}} b{{font-weight:600;color:var(--navy)}} ul{{margin:0 0 8px;padding-left:16px}} li{{margin-bottom:4px}}
table{{width:100%;border-collapse:collapse;font-size:8.4pt;margin:6px 0 10px}}
th{{background:var(--navy);color:#fff;text-align:left;padding:4px 6px;font-size:7.2pt;font-weight:600;text-transform:uppercase;letter-spacing:.07em}}
td{{padding:4px 6px;border-bottom:1px solid var(--riga);vertical-align:top;line-height:1.35}}
td.c{{text-align:center}}
.box{{border:1px solid var(--riga);border-left:4px solid var(--blu);background:#FBFDFE;padding:8px 12px;margin:9px 0;font-size:8.8pt;page-break-inside:avoid}}
.box.rosso{{border-left-color:var(--rosso);background:var(--rosso-velo)}}
.box .eti{{font-size:7.6pt;font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:var(--blu);display:block;margin-bottom:3px}}
.box.rosso .eti{{color:var(--rosso)}} .box ul{{margin:0}} .box li:last-child{{margin-bottom:0}}
.reel{{margin:0;page-break-after:always;border:1px solid var(--riga);border-radius:3px}}
.cima{{display:flex;align-items:baseline;gap:12px;background:var(--velo);padding:6px 10px;border-bottom:1px solid var(--riga)}}
.n3{{font-size:7.6pt;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--blu);white-space:nowrap}}
.tt{{font-size:12pt;font-weight:700;color:var(--navy)}}
.conc{{padding:7px 12px 3px;margin:0;font-size:9pt}} .chi{{color:var(--grigio)}}
.reel table{{margin:4px 0 0;font-size:8.2pt}} .reel td{{padding:3.5px 6px}} .reel th{{background:#EAF2FA;color:var(--navy)}}
.stacchi td.c{{font-weight:700;color:var(--navy)}}
.sec{{font-weight:700;color:var(--navy);white-space:nowrap}} .fab{{color:var(--grigio)}}
.parla{{font-weight:600}}
.schermo{{display:inline-block;margin:1px 0;font-size:7.6pt;font-weight:700;background:var(--navy);color:#fff;padding:2px 5px;border-radius:2px}}
.sbam{{color:var(--rosso);font-weight:700}}
.stacchi tr.gancio td{{background:var(--verde-velo);color:var(--verde);font-size:7.2pt;font-weight:700;letter-spacing:.1em;text-transform:uppercase;padding:2px 6px;text-align:center}}
.stacchi td.ser{{background:#FBFDFE;color:var(--ink2)}} .stacchi td.att{{background:var(--giallo-velo);color:var(--giallo)}} .stacchi td.ad{{background:var(--velo);color:var(--ink)}}
.stacchi td.cb{{background:#F4F6F8;color:var(--ink2);font-size:8.2pt}}
table.alb{{margin:5px 0 6px;page-break-inside:avoid}} table.alb td{{font-size:7.8pt;padding:2px 6px}} table.alb th{{padding:3px 6px}}
</style></head><body>
<h1>Ventiquattro reel SBAM</h1>
<p class="sotto">Dodici per le inserzioni (laser e Afrodite), dodici per la pagina · stacco per stacco · regola dei 5 secondi</p>
<p class="rev">NIPEC · 2 novembre 2026 · seconda stesura · Giorgio Petrelli</p>

<div class="box"><span class="eti">La regola dei 5 secondi, e la terza cosa</span>
<ul><li><b>1. I primi 5 secondi</b> contengono il vantaggio intero.</li>
<li><b>2. Nessuno stacco dura più di 5 secondi.</b> Dopo, si cambia stacco <b>e</b> inquadratura. Mai due inquadrature uguali di fila.</li>
<li><b>3. SBAM.</b> In ogni reel c'è un colpo o una sorpresa entro i primi 3 secondi: è quello che ferma il dito.</li></ul></div>

<h2>Le regole applicate a tutti e ventiquattro</h2><ul>{regole}</ul>
<h2>Cosa ha deciso Giorgio</h2><ul>{decisioni}</ul>

<h2>Serie A · adv · laser</h2>
<table><tr><th style="width:5%">Codice</th><th style="width:27%">Titolo</th><th>Il colpo</th><th style="width:7%">Dura</th></tr>{tab(D.LASER)}</table>
<h2>Serie A · adv · Afrodite (Italia e Albania)</h2>
<table><tr><th style="width:5%">Codice</th><th style="width:27%">Titolo</th><th>Il colpo</th><th style="width:7%">Dura</th></tr>{tab(D.AFRO)}</table>
<h2>Serie B · la pagina, nell'ordine di uscita</h2>
<table><tr><th style="width:5%">Codice</th><th style="width:27%">Titolo</th><th>Il colpo</th><th style="width:7%">Dura</th></tr>{tab(D.PAGINA)}</table>

<div class="box rosso"><span class="eti">Parole che non si usano</span>
«Macchina» (si dice <b>dispositivo</b>), «LED» (<b>low laser</b>), «cavitazione» (<b>ultrasuono focalizzato direzionale</b>), percentuali, prima/dopo, il modello del laser, diodi, watt, imperativi in -ci. Nessun volto senza consenso.</div>

<h2>Come si fa lo SBAM</h2><ul>{lista(D.SBAM)}</ul>
<h2>Ordine di uscita (proposta)</h2><ul>{lista(D.ORDINE)}</ul>
<h2>Per l'Albania</h2><ul>{lista(D.ALBANIA)}</ul>
<div style="page-break-after:always"></div>

<h2>Serie A · adv · laser</h2>
{sezione(D.LASER)}
<h2>Serie A · adv · Afrodite</h2>
{sezione(D.AFRO)}
<h2>Serie B · la pagina</h2>
<p>Non sono inserzioni: nessuna parola chiave. Servono a far fermare il dito e a far ricordare chi siamo. I primi sei sono le sei pubblicazioni che la pagina deve avere prima di poter sponsorizzare.</p>
{sezione(D.PAGINA)}
</body></html>
'''
open(H, 'w', encoding='utf8').write(doc)
subprocess.run([CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer', '--allow-file-access-from-files',
                f'--print-to-pdf={PDF}', '--virtual-time-budget=8000', 'file://' + H], check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
print('documento:', PDF)
