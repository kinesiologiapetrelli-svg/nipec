#!/usr/bin/env python3
"""Le brochure NIPEC: Uriel, Ares, Afrodite, Hermes, in quattro lingue (IT, SQ, EN, ES). A4, quattro pagine ciascuna, nello stile del sito www.nipecestetica.eu.

I testi stanno tutti in testi.py (una struttura sola, quattro lingue: controlla() si ferma se una lingua ha una riga in meno).
Vengono dal sito (SITO/pubblica: laser-ares, laser-uriel, afrodite, metodo, formazione) e, per Hermes, dal depliant e dal manuale d'uso
del produttore (ERMES Slim, Drive). Niente prezzi. Si dice «dispositivo», non «macchina». L'albanese e' una bozza: la controlla Uarda.

Uso:  python3 fai-brochure.py            # tutte e 16
      python3 fai-brochure.py EN ES      # solo alcune lingue
Esce:  BROCHURE-<DISPOSITIVO>-<LINGUA>.pdf  e, in sorgenti/, l'HTML da cui nasce.
"""
import html, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import testi

QUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(QUI)
CHROME = next(p for p in ('/opt/pw-browsers/chromium-1243/chrome-linux64/chrome', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome') if os.path.exists(p))
FONT = os.path.join(REPO, 'SITO', 'pubblica', 'caratteri', 'archivo.woff2')
IMG = os.path.join(REPO, 'SITO', 'pubblica', 'immagini')
FOTO = os.path.join(REPO, 'schede', 'LASER', 'foto')
SORG = os.path.join(QUI, 'sorgenti')
os.makedirs(SORG, exist_ok=True)

def esc(t): return html.escape(t, quote=False)

def svg(nome):
    s = open(os.path.join(REPO, 'MARCHIO', nome), encoding='utf8').read()
    return re.sub(r'<title>.*?</title>', '', s, flags=re.S)
LOGO = svg('nipec-logo-orizzontale.svg').replace('<svg ', '<svg class="logo" ', 1)
LOGO_NEG = svg('nipec-logo-orizzontale-negativo.svg').replace('<svg ', '<svg class="logo" ', 1)
EMBL_NEG = re.sub(r'^<svg[^>]*>|</svg>\s*$', '', svg('nipec-emblema-negativo.svg').strip()).strip()

CSS = '''
@font-face{font-family:"Archivo";src:url("%(font)s") format("woff2");font-weight:100 900}
:root{--navy:#123A63;--blu:#1C6EA4;--chiaro:#5AA6D6;--testo:#4A5B6E;--ink:#0F2B4A;--velo:#EEF3F8;--velo2:#E6EFF8;--riga:#DCE4EC;--scuro:#0B2545}
@page{size:A4;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#fff}
body{font-family:"Archivo","Helvetica Neue",Arial,sans-serif;color:var(--testo);font-size:9.6pt;line-height:1.55;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:210mm;height:297mm;position:relative;overflow:hidden;page-break-after:always;padding:13mm 15mm 0}
.testa{display:flex;justify-content:space-between;align-items:center;padding-bottom:5mm;border-bottom:1px solid var(--riga);margin-bottom:8mm}
.testa .logo{height:11mm;width:auto}
.testa .et{font-size:7.2pt;letter-spacing:.14em;text-transform:uppercase;color:var(--blu);font-weight:600}
.piede{position:absolute;left:15mm;right:15mm;bottom:8mm;display:flex;justify-content:space-between;font-size:7.4pt;color:#7B8A9A;border-top:1px solid var(--riga);padding-top:3mm}
.eyebrow{font-size:7.4pt;letter-spacing:.17em;text-transform:uppercase;color:var(--blu);font-weight:600;margin-bottom:3mm}
h1{font-size:52pt;line-height:1.02;font-weight:700;color:var(--navy);letter-spacing:-.025em}
h1 small{display:block;font-size:17pt;font-weight:500;letter-spacing:-.005em;color:var(--blu);margin-top:2mm}
h2{font-size:21pt;line-height:1.12;font-weight:700;color:var(--navy);letter-spacing:-.015em;margin-bottom:4mm}
h3{font-size:11.5pt;line-height:1.25;font-weight:700;color:var(--navy);margin-bottom:1.5mm}
.lead{font-size:17pt;line-height:1.28;color:var(--navy);margin:6mm 0 5mm;font-weight:500}
.lead .acc{color:var(--blu)}
p{margin-bottom:3mm}
.pills{display:flex;flex-wrap:wrap;gap:2mm;margin:4mm 0 0}
.pill{border:1px solid var(--navy);color:var(--navy);border-radius:20px;padding:1.2mm 3.4mm;font-size:8pt;font-weight:500}
.foto{background:var(--velo);border-radius:5mm;display:flex;align-items:center;justify-content:center;overflow:hidden;position:relative}
.foto img{mix-blend-mode:multiply;display:block}
.banda{position:absolute;left:0;right:0;bottom:0;height:34mm;background:var(--navy);color:#fff;padding:0 15mm;display:flex;align-items:center;justify-content:space-between;gap:10mm}
.banda .frase{font-size:15pt;line-height:1.25;font-weight:600;max-width:105mm}
.banda .sito{font-size:9pt;letter-spacing:.05em;color:#BFD7EC;text-align:right;line-height:1.7}
.banda .sito b{color:#fff;font-weight:600;font-size:10.5pt}
.sez{margin-bottom:9mm}
.due{display:grid;grid-template-columns:1fr 1fr;gap:5mm}
.tre{display:grid;grid-template-columns:1fr 1fr 1fr;gap:5mm}
.card{background:var(--velo);border-radius:4mm;padding:5mm 5.5mm}
.card.bianca{background:#fff;border:1px solid var(--riga)}
.card.navy{background:var(--navy);color:#DDE9F5}
.card.navy h3{color:#fff}
.card.navy .eyebrow{color:#9CCBE8}
.card .eyebrow{margin-bottom:2mm}
.card ul,.col ul{list-style:none;margin-top:2mm}
.card li,.col li{position:relative;padding-left:4mm;margin-bottom:1.2mm;font-size:9pt}
.card li:before,.col li:before{content:"";position:absolute;left:0;top:2.1mm;width:1.4mm;height:1.4mm;border-radius:50%;background:var(--blu)}
.card.navy li:before{background:#9CCBE8}
.col{border-top:2px solid var(--blu);padding-top:3.5mm}
.col h3{font-size:10.5pt}
.col p{font-size:9pt;margin:0}
table{width:100%;border-collapse:separate;border-spacing:0;border:1px solid var(--riga);border-radius:3mm;overflow:hidden;font-size:9pt}
th{background:var(--navy);color:#fff;text-align:left;font-weight:600;padding:2.6mm 4mm;font-size:8.6pt}
td{padding:2.3mm 4mm;border-top:1px solid var(--riga);vertical-align:top}
td:first-child{color:#6B7C8F;width:30%}
td b{color:var(--ink);font-weight:600}
tr:nth-child(even) td{background:#FAFCFE}
.passi{display:grid;grid-template-columns:1fr 1fr;gap:5mm 7mm}
.passo{display:flex;gap:4mm}
.passo .n{flex:none;width:9mm;height:9mm;border-radius:50%;background:var(--navy);color:#fff;font-weight:700;font-size:9pt;display:flex;align-items:center;justify-content:center;margin-top:.5mm}
.passo h3{margin-bottom:1mm}
.passo p{font-size:8.8pt;margin-bottom:1.5mm}
.passo ul{list-style:none}
.passo li{font-size:8.5pt;padding-left:3.5mm;position:relative;margin-bottom:.6mm}
.passo li:before{content:"";position:absolute;left:0;top:1.9mm;width:1.2mm;height:1.2mm;border-radius:50%;background:var(--blu)}
.cta{background:var(--navy);color:#DDE9F5;border-radius:5mm;padding:7mm 8mm;display:flex;justify-content:space-between;align-items:center;gap:8mm}
.cta h2{color:#fff;font-size:17pt;margin-bottom:2mm}
.cta p{margin:0;font-size:9.4pt}
.cta .bottone{flex:none;background:#fff;color:var(--navy);border-radius:20px;padding:3mm 6mm;font-weight:600;font-size:9.4pt;text-align:center}
.contatti{display:grid;grid-template-columns:1.1fr 1.1fr 1fr;gap:6mm;margin-top:8mm;font-size:8.6pt}
.contatti .eyebrow{margin-bottom:1.5mm}
.contatti p{margin-bottom:1mm;color:var(--testo)}
.contatti b{color:var(--ink);font-weight:600}
.firma{position:absolute;left:0;right:0;bottom:0;background:var(--scuro);color:#9FB4CB;padding:4.5mm 15mm 6mm;font-size:7.6pt;display:flex;justify-content:space-between;gap:6mm}
.firma .logo{height:8mm;width:auto}
.nota{font-size:7.8pt;color:#7B8A9A}
.tappe{display:grid;grid-template-columns:repeat(5,1fr);gap:4mm;margin-top:8mm}
.tappa{border-top:2px solid var(--blu);padding-top:3mm}
.tappa .q{font-size:15pt;font-weight:700;color:var(--navy);letter-spacing:-.01em;line-height:1.1}
.tappa h3{font-size:9.6pt;margin:1.5mm 0 1mm}
.tappa p{font-size:8.2pt;line-height:1.45;margin:0}
.chip{display:inline-block;background:var(--velo2);color:var(--navy);border-radius:20px;padding:1.5mm 4mm;margin:0 1.5mm 2mm 0;font-size:8.8pt;font-weight:500}
.grande{font-size:26pt;font-weight:700;color:var(--blu);letter-spacing:-.02em;line-height:1}
.red{border-color:#E7C7C0;background:#FBF1EF}
.ult{display:flex;flex-direction:column}
.ult .p4{flex:1;display:flex;flex-direction:column;margin-bottom:21mm}
.p4 .passi{gap:5mm 7mm}
.p4 .passo p{font-size:8.6pt;line-height:1.5;margin-bottom:1.3mm}
.p4 .passo li{font-size:8.2pt}
.p4 .tappa p{font-size:8pt;line-height:1.42}
.p4 .cta{padding:6mm 8mm}
.p4 .cta h2{font-size:15.5pt}
.p4 .contatti{margin-top:auto}
'''

def foto_rel(percorso_repo):
    """Percorso dell'immagine visto dalla cartella sorgenti/ (dove sta l'HTML)."""
    return os.path.relpath(os.path.join(REPO, percorso_repo), SORG)

# ---- i dispositivi: quello che non cambia con la lingua (foto, misure, nomi brevi, nome del file) ----
DISP = dict(
    ares=dict(breve='Ares', file='ARES', foto='SITO/pubblica/immagini/e493bbb796de.jpg', altezza=124, img_h=112),
    uriel=dict(breve='Uriel', file='URIEL', foto='schede/LASER/foto/uriel-2026.jpg', altezza=124, img_h=112),
    afrodite=dict(breve='Afrodite', file='AFRODITE', foto='SITO/pubblica/immagini/741b069dc662.jpg', altezza=124, img_h=118, img_w=100),
    hermes=dict(breve='Hermes', file='HERMES', altezza=124),
)

def contatti(u):
    c = u['contatti']
    return (f'<div class="contatti">'
            f'<div><div class="eyebrow">{esc(c["c1"])}</div><p><b>{esc(u["wa"])}</b></p><p>{esc(c["verde"])}</p><p>info@nipecestetica.com</p></div>'
            f'<div><div class="eyebrow">{esc(c["c2"])}</div><p>Via Rovetta 29, 25080 Padenghe sul Garda (BS)</p><p>Rruga Donika Kastrioti 3, Tiranë · <span style="white-space:nowrap">+355 69 212 9786</span></p></div>'
            f'<div><div class="eyebrow">{esc(c["c3"])}</div><p><b>www.nipecestetica.eu</b></p><p>{esc(c["sito2"])}</p></div></div>')

def testa(u, nome): return f'<div class="testa">{LOGO}<span class="et">{esc(u["testa"].format(nome=nome))}</span></div>'
def piede(u, nome, n): return f'<div class="piede"><span>NIPEC · {esc(u["marchio"])} — www.nipecestetica.eu</span><span>{nome} · {n}/4</span></div>'

def pagina(u, nome, n, corpo, intesta=True, con_piede=True, classe=''):
    return f'<section class="page{classe}">{testa(u, nome) if intesta else ""}{corpo}{piede(u, nome, n) if con_piede else ""}</section>'

def pill(lista): return '<div class="pills">' + ''.join(f'<span class="pill">{esc(x)}</span>' for x in lista) + '</div>'

def copertina(u, t, dp, grafica=None):
    if 'foto' in dp:
        cornice = (f'<div class="foto" style="height:{dp["altezza"]}mm;margin-top:7mm"><img src="{foto_rel(dp["foto"])}" '
                   f'style="max-height:{dp["img_h"]}mm;max-width:{dp.get("img_w", 120)}mm"></div>')
    else:
        cornice = f'<div class="foto" style="height:{dp["altezza"]}mm;margin-top:7mm;background:var(--navy)">{grafica}</div>'
    sotto = f'<small>{esc(t["sotto"])}</small>' if t.get('sotto') else ''
    return (f'<div class="eyebrow">{esc(t["eyebrow"])}</div><h1>{esc(t["nome"])}{sotto}</h1>'
            f'<div class="lead">{t["lead"]}</div><p style="max-width:165mm;font-size:10.4pt;line-height:1.6">{esc(t["intro"])}</p>{pill(t["pill"])}{cornice}'
            f'<div class="banda"><div class="frase">{"<br>".join(esc(x) for x in u["banda"])}</div>'
            f'<div class="sito"><b>www.nipecestetica.eu</b><br>{esc(u["wa"])}</div></div>')

def tabella(righe, intestazioni):
    th = ''.join(f'<th>{esc(h)}</th>' for h in intestazioni)
    tr = ''.join('<tr>' + ''.join(f'<td>{c if i else esc(c)}</td>' for i, c in enumerate(r)) + '</tr>' for r in righe)
    return f'<table><tr>{th}</tr>{tr}</table>'

def passi(u):
    return ('<div class="passi">' + ''.join(
        f'<div class="passo"><div class="n">{i:02d}</div><div><h3>{esc(t)}</h3><p>{esc(p)}</p><ul>' + ''.join(f'<li>{esc(b)}</li>' for b in bl) + '</ul></div></div>'
        for i, (t, p, bl) in enumerate(u['passi'], 1)) + '</div>')

def percorso(u):
    return (f'<div class="eyebrow" style="margin-top:8mm">{esc(u["percorso_eyebrow"])}</div><div class="tappe" style="margin-top:3mm">' +
            ''.join(f'<div class="tappa"><div class="q">{esc(q)}</div><h3>{esc(t)}</h3><p>{esc(x)}</p></div>' for q, t, x in u['tappe']) + '</div>')

def ultima(u, t, dp, n=4):
    ct, cp, cb = t['cta']
    cta = f'<div class="cta"><div><h2>{esc(ct)}</h2><p>{esc(cp)}</p></div><div class="bottone">{esc(cb)}</div></div>'
    corpo = (f'<div class="p4"><div class="eyebrow">{esc(u["metodo_eyebrow"])}</div><h2>{esc(u["metodo_h2"])}</h2>'
             f'<p style="max-width:150mm;margin-bottom:7mm">{esc(u["metodo_p"])}</p>'
             f'{passi(u)}{percorso(u)}<div style="margin-top:8mm;margin-bottom:6mm">{cta}</div>{contatti(u)}</div>'
             f'<div class="firma">{LOGO_NEG}<span>© 2026 NIPEC · {esc(u["marchio"])} — PHD System Srl · {esc(u["piva"])} 04696530981<br>{esc(u["firma"])}</span></div>')
    return pagina(u, dp['breve'], n, corpo, con_piede=False, classe=' ult')

def box_certificazione(t):
    (e1, h1, p1), (e2, h2, p2) = t['c1'], t['c2']
    return ('<div class="due">'
            f'<div class="card" style="background:var(--velo2)"><div class="eyebrow">{esc(e1)}</div><h3 style="font-size:13pt">{esc(h1)}</h3><p style="font-size:9pt;margin:0">{esc(p1)}</p></div>'
            f'<div class="card" style="background:var(--velo2)"><div class="eyebrow">{esc(e2)}</div><h3 style="font-size:13pt">{esc(h2)}</h3><p style="font-size:9pt;margin:0">{esc(p2)}</p></div></div>')

def colonne(voci, classe='col'):
    return ''.join(f'<div class="{classe}"><h3>{esc(a)}</h3><p>{esc(b)}</p></div>' for a, b in voci)

# =============================== ARES ===============================
def ares_pagine(u, t):
    dp = DISP['ares']; nome = dp['breve']; h25, h26 = t['tab_heads'][1], t['tab_heads'][2]
    p1 = pagina(u, nome, 1, copertina(u, t, dp), con_piede=False)
    p2 = pagina(u, nome, 2,
        f'<div class="sez"><div class="eyebrow">{esc(t["due_eyebrow"])}</div><h2>{t["due_h2"]}</h2>'
        f'<p style="max-width:150mm;margin-bottom:5mm">{esc(t["due_p"])}</p>'
        f'<div class="due"><div class="card bianca"><div class="eyebrow">{esc(t["v25_eyebrow"])}</div><h3 style="font-size:15pt">{esc(h25)}</h3>'
        f'<div class="foto" style="height:38mm;margin:3mm 0;background:#fff"><img src="{foto_rel("schede/LASER/foto/ares-2025.jpg")}" style="max-height:36mm"></div>'
        f'<p style="font-size:9pt">{esc(t["v25_p"])}</p><ul>' + ''.join(f'<li>{esc(x)}</li>' for x in t['v25_ul']) + '</ul></div>'
        f'<div class="card navy"><div class="eyebrow">{esc(t["v26_eyebrow"])}</div><h3 style="font-size:15pt">{esc(h26)}</h3>'
        f'<div class="foto" style="height:38mm;margin:3mm 0;background:#fff"><img src="{foto_rel("schede/LASER/foto/ares-2026.jpg")}" style="max-height:36mm"></div>'
        f'<p style="font-size:9pt;color:#DDE9F5">{esc(t["v26_p"])}</p><ul>' + ''.join(f'<li>{esc(x)}</li>' for x in t['v26_ul']) + '</ul></div></div></div>'
        f'<div class="sez"><div class="eyebrow">{esc(t["cab_eyebrow"])}</div><h2>{esc(t["cab_h2"])}</h2><div class="tre">{colonne(t["cab"])}</div></div>')
    p3 = pagina(u, nome, 3,
        f'<div class="sez"><div class="eyebrow">{esc(t["tec_eyebrow"])}</div><h2>{esc(t["tec_h2"])}</h2>' + tabella(t['tab_rows'], t['tab_heads']) + '</div>' + box_certificazione(t))
    return [p1, p2, p3, ultima(u, t, dp)]

# =============================== URIEL ===============================
def uriel_pagine(u, t):
    dp = DISP['uriel']; nome = dp['breve']
    (b1, b2, b3) = t['bande']
    p1 = pagina(u, nome, 1, copertina(u, t, dp), con_piede=False)
    p2 = pagina(u, nome, 2,
        f'<div class="sez"><div class="eyebrow">{esc(t["bande_eyebrow"])}</div><h2>{t["bande_h2"]}</h2><div class="tre">'
        f'<div class="card"><div class="grande">{esc(b1[0])}</div><h3 style="margin-top:3mm">{esc(b1[1])}</h3><p style="font-size:9pt;margin:0">{esc(b1[2])}</p></div>'
        f'<div class="card" style="background:var(--navy);color:#DDE9F5"><div class="grande" style="color:#9CCBE8">{esc(b2[0])}</div><h3 style="margin-top:3mm;color:#fff">{esc(b2[1])}</h3><p style="font-size:9pt;margin:0">{esc(b2[2])}</p></div>'
        f'<div class="card"><div class="grande">{esc(b3[0])}</div><h3 style="margin-top:3mm">{esc(b3[1])}</h3><p style="font-size:9pt;margin:0">{esc(b3[2])}</p></div></div></div>'
        f'<div class="sez"><div class="eyebrow">{esc(t["cab_eyebrow"])}</div><h2>{esc(t["cab_h2"])}</h2><div class="tre">{colonne(t["cab"])}</div></div>'
        f'<div class="sez"><div class="eyebrow">{esc(t["conf_eyebrow"])}</div>' + tabella(t['conf_rows'], t['conf_heads']) + '</div>')
    p3 = pagina(u, nome, 3,
        f'<div class="sez"><div class="eyebrow">{esc(t["tec_eyebrow"])}</div><h2>{esc(t["tec_h2"])}</h2>' + tabella(t['tab_rows'], t['tab_heads']) + '</div>' + box_certificazione(t))
    return [p1, p2, p3, ultima(u, t, dp)]

# =============================== AFRODITE ===============================
def afrodite_pagine(u, t):
    dp = DISP['afrodite']; nome = dp['breve']
    tec = t['tec']
    cards = colonne(tec[:3]); cards2 = colonne(tec[3:]) + '<div></div>'
    chips = ''.join(f'<span class="chip">{esc(x)}</span>' for x in t['chips'])
    pe, ph, pp = t['prog']
    p1 = pagina(u, nome, 1, copertina(u, t, dp), con_piede=False)
    p2 = pagina(u, nome, 2,
        f'<div class="sez"><div class="eyebrow">{esc(t["tec_eyebrow"])}</div><h2>{t["tec_h2"]}</h2><div class="tre" style="row-gap:7mm">{cards}{cards2}</div></div>'
        f'<div class="sez"><div class="eyebrow">{esc(t["off_eyebrow"])}</div><h2>{t["off_h2"]}</h2>{chips}</div>'
        f'<div class="card navy"><div class="eyebrow">{esc(pe)}</div><h3 style="font-size:15pt">{esc(ph)}</h3><p style="margin:2mm 0 0;font-size:9.6pt;color:#DDE9F5">{esc(pp)}</p></div>')
    uso = ''.join(f'<div class="card"><h3>{esc(a)}</h3><p style="font-size:9pt;margin:0">{esc(b)}</p></div>' for a, b in t['uso'])
    p3 = pagina(u, nome, 3,
        f'<div class="sez"><div class="eyebrow">{esc(t["sch_eyebrow"])}</div><h2>{esc(t["sch_h2"])}</h2>' + tabella(t['sch_rows'], t['sch_heads']) + '</div>'
        f'<div class="sez"><div class="eyebrow">{esc(t["dem_eyebrow"])}</div><h2>{esc(t["dem_h2"])}</h2><div class="tre">{colonne(t["dem"])}</div></div>'
        f'<div class="sez"><div class="eyebrow">{esc(t["uso_eyebrow"])}</div><h2>{t["uso_h2"]}</h2>'
        f'<p style="max-width:150mm;margin-bottom:5mm">{esc(t["uso_p"])}</p><div class="tre">{uso}</div></div>')
    return [p1, p2, p3, ultima(u, t, dp)]

# =============================== HERMES ===============================
def grafica_hermes(testo):
    return f"""<svg viewBox="0 0 400 300" style="width:100%;height:100%" xmlns="http://www.w3.org/2000/svg">
<defs><radialGradient id="g" cx="50%" cy="50%" r="60%"><stop offset="0" stop-color="#1C6EA4" stop-opacity=".55"/><stop offset="1" stop-color="#123A63" stop-opacity="0"/></radialGradient></defs>
<rect width="400" height="300" fill="#123A63"/><circle cx="200" cy="150" r="170" fill="url(#g)"/>
<g fill="none" stroke="#9CCBE8" stroke-width="1.3">
<ellipse cx="200" cy="150" rx="26" ry="14" stroke-width="2.2" stroke="#fff"/><ellipse cx="200" cy="150" rx="54" ry="30" opacity=".95"/><ellipse cx="200" cy="150" rx="86" ry="48" opacity=".8"/>
<ellipse cx="200" cy="150" rx="122" ry="68" opacity=".6"/><ellipse cx="200" cy="150" rx="162" ry="90" opacity=".42"/><ellipse cx="200" cy="150" rx="206" ry="114" opacity=".26"/></g>
<g fill="#fff"><text x="200" y="262" text-anchor="middle" font-family="Archivo, Arial, sans-serif" font-size="13" font-weight="600" fill="#BFD7EC" textLength="{min(340, len(testo) * 10)}" lengthAdjust="spacing">{esc(testo)}</text></g></svg>"""

def hermes_pagine(u, t):
    dp = DISP['hermes']; nome = dp['breve']
    chips1 = ''.join(f'<span class="chip">{esc(x)}</span>' for x in t['zone1'])
    chips2 = ''.join(f'<span class="chip" style="background:#fff;border:1px solid var(--riga)">{esc(x)}</span>' for x in t['zone2'])
    de, dh, dpp = t['dop']; ce, ch, cp = t['ctr']
    p1 = pagina(u, nome, 1, copertina(u, t, dp, grafica=grafica_hermes(t['grafica'])), con_piede=False)
    p2 = pagina(u, nome, 2,
        f'<div class="sez"><div class="eyebrow">{esc(t["come_eyebrow"])}</div><h2>{esc(t["come_h2"])}</h2>'
        f'<p style="max-width:152mm;margin-bottom:5mm">{esc(t["come_p"])}</p>' + tabella(t['conf_rows'], t['conf_heads']) + '</div>'
        f'<div class="sez"><div class="eyebrow">{esc(t["zone_eyebrow"])}</div><h2>{esc(t["zone_h2"])}</h2>'
        f'<p style="margin-bottom:3mm"><b style="color:var(--ink)">{esc(t["zone1_label"])}</b></p>{chips1}'
        f'<p style="margin:3mm 0"><b style="color:var(--ink)">{esc(t["zone2_label"])}</b></p>{chips2}</div>'
        f'<div class="card" style="background:var(--velo2)"><div class="eyebrow">{esc(de)}</div><h3 style="font-size:13pt">{esc(dh)}</h3><p style="font-size:9pt;margin:0">{esc(dpp)}</p></div>')
    p3 = pagina(u, nome, 3,
        f'<div class="sez"><div class="eyebrow">{esc(t["tec_eyebrow"])}</div><h2>{esc(t["tec_h2"])}</h2>' + tabella(t['tab_rows'], t['tab_heads']) + '</div>'
        f'<div class="sez"><div class="eyebrow">{esc(t["sed_eyebrow"])}</div><h2>{esc(t["sed_h2"])}</h2><div class="tre">{colonne(t["sed"])}</div></div>'
        f'<div class="card red" style="border:1px solid #E7C7C0;background:#FBF1EF"><div class="eyebrow" style="color:#9C3A28">{esc(ce)}</div><h3 style="font-size:12pt">{esc(ch)}</h3>'
        f'<p style="font-size:8.8pt;margin:0">{esc(cp)}</p></div>')
    return [p1, p2, p3, ultima(u, t, dp)]

# =============================== stampa ===============================
PAGINE = (('uriel', uriel_pagine), ('ares', ares_pagine), ('afrodite', afrodite_pagine), ('hermes', hermes_pagine))

def stampa(chiave, codice, L, fn):
    u, t = L['ui'], L[chiave]; dp = DISP[chiave]
    doc = (f'<!doctype html><html lang="{u["lang"]}"><head><meta charset="utf-8"><title>{esc(t["nome"])} · NIPEC</title>'
           f'<style>{CSS.replace("%(font)s", FONT)}</style></head><body>{"".join(fn(u, t))}</body></html>')
    base = f'{dp["file"]}-{codice}'
    h = os.path.join(SORG, f'brochure-{base.lower()}.html'); pdf = os.path.join(QUI, f'BROCHURE-{base}.pdf')
    open(h, 'w', encoding='utf8').write(doc)
    subprocess.run([CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer', '--allow-file-access-from-files',
                    f'--print-to-pdf={pdf}', '--virtual-time-budget=8000', 'file://' + h], check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    pagine = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout).group(1))
    assert pagine == 4, f'{pdf}: {pagine} pagine invece di 4 (una pagina e\' strabordata)'
    print(os.path.basename(pdf), pagine, 'pagine')

if __name__ == '__main__':
    testi.controlla()
    scelte = [a.upper() for a in sys.argv[1:]] or [c for c, _ in testi.LINGUE]
    for codice, L in testi.LINGUE:
        if codice in scelte:
            for chiave, fn in PAGINE: stampa(chiave, codice, L, fn)
