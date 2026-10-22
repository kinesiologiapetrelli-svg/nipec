#!/usr/bin/env python3
"""Genera il LIBRO DEL MARCHIO NIPEC e il KIT-CARTOLERIA.

Parte dai file gia' esistenti in MARCHIO/ (loghi SVG, caratteri) e dal testo
vero del sito: non inventa un marchio nuovo, mette in ordine quello che c'e'.

Uso:  python3 fai-il-libro.py
Esce: NIPEC-libro-del-marchio.html / .pdf  e  KIT-CARTOLERIA/
"""
import base64, io, os, re, subprocess, sys

QUI = os.path.dirname(os.path.abspath(__file__))
MARCHIO = os.path.dirname(QUI)
REPO = os.path.dirname(MARCHIO)
KIT = os.path.join(QUI, 'KIT-CARTOLERIA')
os.makedirs(KIT, exist_ok=True)
CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'

# ------------------------------------------------------------------ risorse
def b64(p):
    return base64.b64encode(open(p, 'rb').read()).decode()

ARCH = b64(os.path.join(MARCHIO, 'proposte-made-in-italy/caratteri/archivo.woff2'))
SERIF = b64(os.path.join(MARCHIO, 'proposte-made-in-italy/caratteri/sourceserif.woff2'))

def svg_file(nome):
    s = open(os.path.join(MARCHIO, nome), encoding='utf8').read()
    s = re.sub(r'<title>.*?</title>', '', s, flags=re.S)
    return s.strip()

def svg_inner(nome):
    s = svg_file(nome)
    return re.sub(r'^<svg[^>]*>|</svg>\s*$', '', s).strip()

def logo(nome, stile='', cls=''):
    s = svg_file(nome).replace('<svg ', f'<svg class="{cls}" style="{stile}" aria-hidden="true" ', 1)
    return s

def foto(nome, lato=900, q=82):
    from PIL import Image
    im = Image.open(os.path.join(REPO, 'SITO/pubblica/immagini', nome)).convert('RGB')
    im.thumbnail((lato, lato))
    buf = io.BytesIO(); im.save(buf, 'JPEG', quality=q, optimize=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()

# ------------------------------------------------------------------ colori
NAVY, BLU, CHIARO = '#123A63', '#1C6EA4', '#5AA6D6'
INK, INK2, GRIGIO = '#17222E', '#44535F', '#8E9295'
RIGA, VELO, BIANCO = '#D4E3EF', '#EAF2FA', '#FFFFFF'

def _rgb(h):
    h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def lum(h):
    def f(c):
        c /= 255
        return c / 12.92 if c <= .03928 else ((c + .055) / 1.055) ** 2.4
    r, g, b = (f(x) for x in _rgb(h)); return .2126 * r + .7152 * g + .0722 * b

def rapporto(a, b):
    la, lb = lum(a), lum(b)
    if la < lb: la, lb = lb, la
    return (la + .05) / (lb + .05)

def cmyk(h):
    r, g, b = (x / 255 for x in _rgb(h))
    k = 1 - max(r, g, b)
    if k >= 1: return (0, 0, 0, 100)
    c, m, y = ((1 - r - k) / (1 - k), (1 - g - k) / (1 - k), (1 - b - k) / (1 - k))
    return tuple(round(v * 100) for v in (c, m, y, k))

# ------------------------------------------------------------------ icone (solo con le forme del logo)
ICONE = {
    'tecnologia': '<rect x="11" y="5" width="26" height="38" rx="7"/><circle cx="24" cy="20" r="6.5"/><path d="M18 34h12"/>',
    'metodo': '<path d="M24 5 A19 19 0 1 1 14.5 7.55"/><circle cx="14.5" cy="7.55" r="2.8" fill="currentColor" stroke="none"/><path d="M19 27l4 4 7-9"/>',
    'formazione': '<path d="M7 39h10v-8h10v-8h10v-8"/><circle cx="41" cy="9" r="2.9" fill="currentColor" stroke="none"/>',
    'supporto': '<circle cx="17.5" cy="24" r="11.5"/><circle cx="30.5" cy="24" r="11.5"/>',
    'strategia': '<path d="M6 42h36"/><path d="M8 34l10-10 8 6 14-17"/><circle cx="40" cy="13" r="2.9" fill="currentColor" stroke="none"/>',
}

def icona(nome, mm=11, colore=BLU):
    return (f'<svg viewBox="0 0 48 48" style="width:{mm}mm;height:{mm}mm;color:{colore}" fill="none" '
            f'stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONE[nome]}</svg>')

# ------------------------------------------------------------------ CSS
CSS = """
@font-face{font-family:"Archivo";src:url(data:font/woff2;base64,@@ARCH@@) format("woff2");font-weight:100 900}
@font-face{font-family:"Source Serif 4";src:url(data:font/woff2;base64,@@SERIF@@) format("woff2");font-weight:200 900}
:root{--navy:#123A63;--blu:#1C6EA4;--chiaro:#5AA6D6;--ink:#17222E;--ink2:#44535F;--grigio:#8E9295;
  --riga:#D4E3EF;--velo:#EAF2FA;--verde:#1B6E52;--giallo:#8A6208;--rosso:#9C3A28}
*{box-sizing:border-box;margin:0;padding:0}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font:9.2pt/1.5 "Source Serif 4",Georgia,serif;color:var(--ink);background:#fff}
@page{size:297mm 210mm;margin:0}
.pg{width:297mm;height:210mm;position:relative;overflow:hidden;break-after:page;page-break-after:always;background:#fff}
.pg:last-child{break-after:auto;page-break-after:auto}
.hd,.ft{position:absolute;left:16mm;right:16mm;display:flex;justify-content:space-between;
  font:600 6.4pt "Archivo",sans-serif;letter-spacing:.16em;text-transform:uppercase;color:var(--ink2)}
.hd{top:9mm}.ft{bottom:8mm;font-weight:500;letter-spacing:.08em}
.in{position:absolute;left:16mm;right:16mm;top:20mm;bottom:17mm}
.dk{background:var(--navy);color:#fff}
.dk .hd,.dk .ft{color:#9CCBE8}
h1,h2,h3,.eti,.sans{font-family:"Archivo","Helvetica Neue",Arial,sans-serif}
h1{font-weight:700;font-size:25pt;line-height:1.08;letter-spacing:-.012em;color:var(--navy)}
h2{font-weight:700;font-size:12.5pt;line-height:1.2;color:var(--navy);letter-spacing:-.005em}
h3{font-weight:700;font-size:9.4pt;line-height:1.25;color:var(--navy)}
.eti{font-weight:600;font-size:6.9pt;letter-spacing:.16em;text-transform:uppercase;color:var(--blu);display:block;margin-bottom:2.2mm}
.dk h1,.dk h2,.dk h3{color:#fff}.dk .eti{color:var(--chiaro)}
p{margin:0 0 2.4mm}p.sm{font-size:8.2pt;line-height:1.45}p.xs{font-size:7.4pt;line-height:1.4}
.mut{color:var(--ink2)}
.dk p{color:#D5E3F0}
b,strong{font-weight:650}
.card{border:1px solid var(--riga);border-radius:2.4mm;padding:4.5mm 5mm;background:#fff}
.card.velo{background:var(--velo)}
.box{border-left:1.1mm solid var(--blu);background:#F4F8FC;padding:3.4mm 4.6mm;border-radius:0 1.6mm 1.6mm 0}
.box.no{border-left-color:var(--rosso);background:#FAEAE6}
.box.ok{border-left-color:var(--verde);background:#E7F3EC}
.box h3{margin-bottom:1.4mm}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:6mm}.g3{display:grid;grid-template-columns:repeat(3,1fr);gap:5mm}
.g4{display:grid;grid-template-columns:repeat(4,1fr);gap:4mm}.g5{display:grid;grid-template-columns:repeat(5,1fr);gap:4mm}
ul.pt{list-style:none}ul.pt li{position:relative;padding-left:4.2mm;margin-bottom:1.6mm;font-size:8.6pt;line-height:1.42}
ul.pt li:before{content:"";position:absolute;left:0;top:.62em;width:1.7mm;height:1.7mm;border-radius:50%;background:var(--blu)}
ul.pt.no li:before{background:var(--rosso)}
.num{font:700 8pt "Archivo",sans-serif;color:var(--blu);letter-spacing:.1em}
.tab{width:100%;border-collapse:collapse;font-size:8.2pt}
.tab th{font:600 6.6pt "Archivo",sans-serif;letter-spacing:.12em;text-transform:uppercase;text-align:left;
  background:var(--navy);color:#fff;padding:2.2mm 3mm}
.tab td{padding:2.3mm 3mm;border-bottom:1px solid var(--riga);vertical-align:top;line-height:1.38}
.tab td:first-child{font:600 7.4pt "Archivo",sans-serif;color:var(--navy)}
.chip{display:inline-block;font:600 6.4pt "Archivo",sans-serif;letter-spacing:.1em;text-transform:uppercase;
  padding:.9mm 2.2mm;border-radius:1mm;background:var(--velo);color:var(--blu)}
.logo{display:block}
.sw{border-radius:2.4mm;overflow:hidden;border:1px solid var(--riga);background:#fff}
.sw .col{display:flex;align-items:flex-end;padding:3.5mm 4mm;font:700 10pt "Archivo",sans-serif}
.sw .dati{padding:3mm 4mm 3.4mm;font:500 7.2pt/1.55 "Archivo",sans-serif;color:var(--ink2)}
.sw .dati b{font-weight:700;color:var(--navy);font-size:8pt;display:block;margin-bottom:.4mm}
.mono{font-family:ui-monospace,"SFMono-Regular",Menlo,monospace;font-size:7pt}
.scala{transform-origin:0 0}
"""

# ------------------------------------------------------------------ pagine
pagine = []

def pagina(sezione, corpo, scuro=False, zoom=1.0):
    n = len(pagine) + 1
    cls = 'pg dk' if scuro else 'pg'
    if zoom != 1.0:
        corpo = f'<div style="zoom:{zoom};width:{265/zoom:.2f}mm;height:{173/zoom:.2f}mm">{corpo}</div>'
    pagine.append(f'''<section class="{cls}">
<div class="hd"><span>NIPEC · Libro del marchio</span><span>{sezione}</span></div>
<div class="in">{corpo}</div>
<div class="ft"><span>Non vendiamo macchine. Costruiamo sistemi di lavoro.</span><span>{n}</span></div>
</section>''')

# ---- 1. COPERTINA
EMBL_NEG = svg_inner('nipec-emblema-negativo.svg')
pagine.append(f'''<section class="pg dk">
<svg viewBox="0 0 100 100" style="position:absolute;right:-58mm;top:-18mm;width:270mm;height:270mm;opacity:.2" aria-hidden="true">{EMBL_NEG}</svg>
{logo('nipec-logo-orizzontale-negativo.svg','position:absolute;left:12mm;top:12mm;width:78mm')}
<div style="position:absolute;left:16mm;bottom:30mm;width:170mm">
<span class="eti" style="font-size:7.6pt">Identità di marca</span>
<h1 style="font-size:50pt;line-height:1;letter-spacing:-.02em;color:#fff;margin-bottom:6mm">Libro del<br>marchio</h1>
<p style="font-size:12pt;line-height:1.45;color:#CFE0EF;width:140mm">Chi è NIPEC, come parla, come si presenta.
Per chi disegna, stampa, scrive o gira un video per noi.</p>
</div>
<div style="position:absolute;left:16mm;bottom:12mm;right:16mm;display:flex;justify-content:space-between;
font:600 6.6pt Archivo;letter-spacing:.16em;text-transform:uppercase;color:#9CCBE8">
<span>Versione 1.0 · Ottobre 2026</span><span>NIPEC · Tecnologie Estetiche · Italia e Albania</span></div>
</section>''')

# ---- 2. COME SI USA
voci = [('Chi siamo', 3), ('Il sistema', 4), ('Persone e carattere', 5), ('La voce', 6), ('Il marchio', 7),
        ('Spazio, misure, fondi', 8), ('Gli errori', 9), ('Colore', 10), ('Colore in uso', 11),
        ('Tipografia', 12), ('Linguaggio grafico', 13), ('Immagini', 14), ('Due paesi, tre lingue', 15),
        ('Applicazioni: stampa', 16), ('Applicazioni: digitale', 17), ('Prima di mandare fuori', 18)]
righe = ''.join(f'<div style="display:flex;align-items:baseline;gap:4mm;padding:1.55mm 0;border-bottom:1px solid var(--riga)">'
                f'<span class="num" style="width:7mm">{i+1:02d}</span><span class="sans" style="font-weight:600;font-size:9.6pt;color:var(--navy);flex:1">{t}</span>'
                f'<span class="sans mut" style="font-size:8pt">{p}</span></div>' for i, (t, p) in enumerate(voci))
pagina('Come si usa', f'''
<div style="display:grid;grid-template-columns:1fr 112mm;gap:18mm;height:100%">
<div style="padding-top:6mm">
<span class="eti">Come si usa</span>
<h1 style="margin-bottom:6mm">Un libro corto,<br>da tenere aperto.</h1>
<p style="font-size:10.4pt;line-height:1.55">Serve a chi fa una grafica, stampa un’insegna, scrive un testo o gira un video per NIPEC.
Ogni pagina dice cosa si fa e cosa no.</p>
<p style="font-size:10.4pt;line-height:1.55">Quando una cosa qui non c’è, si chiede a Giorgio <b>prima</b>, non dopo.</p>
<div class="box" style="margin-top:8mm"><h3>In una riga</h3>
<p class="sm" style="margin:0">NIPEC non vende macchine: costruisce sistemi di lavoro per i centri estetici.
Il marchio, i colori e le parole servono tutti a far vedere questo, e niente altro.</p></div>
</div>
<div style="padding-top:6mm">{righe}</div>
</div>''', zoom=1.12)

# ---- 3. CHI SIAMO
pagina('01 · Chi siamo', f'''
<div style="display:grid;grid-template-columns:128mm 1fr;gap:12mm;height:100%">
<div style="background:var(--navy);border-radius:3mm;position:relative;overflow:hidden;padding:11mm 11mm">
<svg viewBox="0 0 100 100" style="position:absolute;right:-30mm;bottom:-32mm;width:112mm;height:112mm;opacity:.16" aria-hidden="true">{EMBL_NEG}</svg>
<span class="eti" style="color:var(--chiaro)">La promessa</span>
<h1 style="color:#fff;font-size:30pt;line-height:1.08;margin-bottom:9mm">Non vendiamo<br>macchine.<br><span style="color:var(--chiaro)">Costruiamo sistemi<br>di lavoro.</span></h1>
<p class="sm" style="color:#CFE0EF;margin-bottom:1.5mm"><b style="color:#fff">SQ</b> &nbsp;Nuk shesim makineri. Ndërtojmë sisteme pune.</p>
<p class="sm" style="color:#CFE0EF"><b style="color:#fff">EN</b> &nbsp;We don’t sell machines. We build working systems.</p>
</div>
<div style="display:flex;flex-direction:column;gap:5mm;padding-top:1mm">
<div><span class="eti">Cosa facciamo</span>
<p style="font-size:10pt">NIPEC è il marchio di tecnologie estetiche di PHD System. Lavoriamo con centri estetici in Italia e in Albania:
laser e dispositivi per il corpo, in vendita o a noleggio, con protocolli, formazione e assistenza.</p></div>
<div><span class="eti">La tesi</span>
<p style="font-size:10pt">Se una macchina si rompe, la causa di solito parte da noi. Una giornata di formazione, poi più nessuno: la macchina
viene usata male e il guasto arriva dopo qualche mese. Per questo consegniamo a tappe, con un’operatrice certificata,
un referente per centro e un controllo ogni mese.</p></div>
<div><span class="eti">Da dove viene</span>
<p style="font-size:10pt">Giorgio Petrelli viene dalla fisioterapia e dalla kinesiologia, con anni di lavoro nelle spa internazionali.
Conosce il centro dalla parte della cabina, non solo da quella del fornitore.</p></div>
<div class="g4" style="margin-top:auto">
<div class="card velo" style="padding:3.5mm"><div class="sans" style="font:700 17pt Archivo;color:var(--navy)">2</div><p class="xs mut" style="margin:0">paesi: Italia e Albania</p></div>
<div class="card velo" style="padding:3.5mm"><div class="sans" style="font:700 17pt Archivo;color:var(--navy)">5</div><p class="xs mut" style="margin:0">tecnologie, dal laser al corpo</p></div>
<div class="card velo" style="padding:3.5mm"><div class="sans" style="font:700 17pt Archivo;color:var(--navy)">12</div><p class="xs mut" style="margin:0">mesi di validità del certificato operatore</p></div>
<div class="card velo" style="padding:3.5mm"><div class="sans" style="font:700 17pt Archivo;color:var(--navy)">1</div><p class="xs mut" style="margin:0">centro pilota: Demetra Center, Tirana</p></div>
</div></div></div>''')

# ---- 4. IL SISTEMA
pilastri = [('tecnologia', 'Tecnologia', 'Dispositivi professionali con certificazione CE italiana. I laser sono già conformi MDR.'),
            ('metodo', 'Metodo', 'Protocolli operativi scritti per ogni trattamento, in italiano e in albanese.'),
            ('formazione', 'Formazione', 'Percorso a tappe con esame finale e certificato operatore valido 12 mesi.'),
            ('supporto', 'Supporto', 'Assistenza diretta, sostituzione dei pezzi e un controllo mensile in videochiamata.'),
            ('strategia', 'Strategia di ricavo', 'Consulenza marketing e campagna di avvio per riempire l’agenda dal primo mese.')]
cp = ''.join(f'''<div class="card" style="padding:5mm 4.6mm 4mm"><div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:4mm">
{icona(k, 11)}<span class="num">0{i+1}</span></div><h3 style="margin-bottom:1.6mm">{t}</h3><p class="sm mut" style="margin:0">{d}</p></div>'''
             for i, (k, t, d) in enumerate(pilastri))
fasi = [('Analisi', 'Chi sono le clienti, quante cabine, quanto costa un’ora di lavoro. Dove sta il margine che oggi perdi.'),
        ('Progettazione', 'La tecnologia giusta e il trattamento intorno: prezzi, pacchetti, vendita o noleggio, con i numeri sul tavolo.'),
        ('Formazione', 'Consegna in cabina, richiamo a +7, online a +21, esame a +45 giorni. Certificato per l’operatrice.'),
        ('Supporto continuo', 'Un referente unico, assistenza diretta e una videochiamata di 10 minuti ogni mese.')]
cf = ''.join(f'''<div style="position:relative;padding-top:9mm"><div style="position:absolute;left:0;top:0;width:6.4mm;height:6.4mm;border-radius:50%;
background:{'var(--navy)' if i < 3 else 'var(--blu)'};color:#fff;font:700 8pt Archivo;display:flex;align-items:center;justify-content:center">{i+1}</div>
<h3 style="margin-bottom:1.4mm">{t}</h3><p class="xs mut" style="margin:0">{d}</p></div>''' for i, (t, d) in enumerate(fasi))
pagina('02 · Il sistema', f'''
<span class="eti">Il sistema NIPEC</span>
<h1 style="font-size:23pt;margin-bottom:2mm">Una macchina, da sola, non riempie l’agenda.</h1>
<p style="font-size:10pt;margin-bottom:6mm">Per questo ogni dispositivo NIPEC arriva con cinque cose, non con una.</p>
<div class="g5" style="margin-bottom:8mm">{cp}</div>
<span class="eti">Il metodo, in quattro fasi</span>
<div style="position:relative">
<div style="position:absolute;left:3mm;right:3mm;top:3mm;height:0;border-top:1.4px solid var(--riga)"></div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:6mm;position:relative">{cf}</div></div>
<div class="box" style="margin-top:6mm"><p class="sm" style="margin:0"><b>La fase 1 è gratuita.</b> Partiamo dall’analisi del centro.
Se non serve una macchina nuova, te lo diciamo.</p></div>''', zoom=1.2)

# ---- 5. PERSONE E CARATTERE
pagina('03 · Persone e carattere', f'''
<div style="display:grid;grid-template-columns:1fr 1fr;gap:14mm">
<div><span class="eti">Chi ci ascolta</span>
<h2 style="margin-bottom:4mm">Parliamo a tre persone.</h2>
<div class="card" style="margin-bottom:3.5mm"><h3>La titolare del centro · Italia e Albania</h3>
<p class="sm mut" style="margin:1mm 0 0">Ha una cabina, un’agenda da riempire e un investimento da far rendere. Non ha tempo per i giri di parole.
Cerca una macchina che lavora, numeri chiari e qualcuno che risponde. Teme la macchina ferma e la promessa che non si avvera.</p></div>
<div class="card" style="margin-bottom:3.5mm"><h3>Lo studio medico · Laser Q-Switch</h3>
<p class="sm mut" style="margin:1mm 0 0">Cerca tecnologia certificata e documenti in ordine. Vuole la scheda tecnica, non lo slogan.</p></div>
<div class="card"><h3>L’operatrice · chi usa la macchina ogni giorno</h3>
<p class="sm mut" style="margin:1mm 0 0">Le parliamo con protocolli e regole chiare, in italiano e in albanese. È lei che fa durare la macchina.</p></div>
</div>
<div><span class="eti">Come siamo</span>
<h2 style="margin-bottom:4mm">Quattro tratti. E il loro contrario.</h2>
<table class="tab"><thead><tr><th style="width:36%">Siamo</th><th>Non siamo</th></tr></thead><tbody>
<tr><td>Diretti</td><td>Bruschi. Diretto vuol dire chiaro, non secco.</td></tr>
<tr><td>Concreti</td><td>Tecnici a vuoto. Un numero, un esempio, una cabina.</td></tr>
<tr><td>Onesti sui numeri</td><td>Miracolosi. Mostriamo quanto rende un trattamento prima che tu firmi.</td></tr>
<tr><td>Presenti dopo la consegna</td><td>Spariti. Il rapporto comincia quando la macchina entra in cabina.</td></tr>
</tbody></table>
<div style="margin-top:6mm"><span class="eti">In cosa crediamo</span>
<div class="g3">
<div class="box" style="padding:3mm 3.4mm"><h3 style="font-size:8.4pt">Dire la verità sui numeri</h3></div>
<div class="box" style="padding:3mm 3.4mm"><h3 style="font-size:8.4pt">Restare dopo la consegna</h3></div>
<div class="box" style="padding:3mm 3.4mm"><h3 style="font-size:8.4pt">Documenti in ordine</h3></div>
</div></div></div></div>
<div style="margin-top:7mm"><span class="eti">Cosa deve restare a chi ci incontra</span>
<div class="g3">
<div class="card velo"><h3>«Parlano chiaro.»</h3><p class="sm mut" style="margin:1mm 0 0">Niente giri di parole né gergo: capisco cosa mi vendono e quanto costa.</p></div>
<div class="card velo"><h3>«Fanno i conti con me.»</h3><p class="sm mut" style="margin:1mm 0 0">Mi mostrano quanto rende un trattamento, prima che io firmi.</p></div>
<div class="card velo"><h3>«Ci sono anche dopo.»</h3><p class="sm mut" style="margin:1mm 0 0">Il giorno dopo la consegna qualcuno risponde, e ogni mese mi richiamano.</p></div>
</div></div>''', zoom=1.12)

# ---- 6. LA VOCE
pagina('04 · La voce', f'''
<div style="display:grid;grid-template-columns:1fr 1fr;gap:14mm;height:100%">
<div><span class="eti">Come parliamo</span>
<h1 style="font-size:22pt;margin-bottom:5mm">Come a una titolare di centro.</h1>
<ul class="pt">
<li><b>Diretto e concreto, dai del tu.</b> Non cambiamo registro perché cambia il lettore.</li>
<li><b>Frasi corte.</b> Un’idea per frase. Se ha due virgole e un trattino, si spezza.</li>
<li><b>Cinque o sei righe, poi uno stacco.</b> Spazio bianco, una riga sottile, un cambio di fondo.</li>
<li><b>Parole che una dice davvero.</b> Niente «sinergia», niente «inestetismi» nel testo emotivo. Restano nei testi tecnici e legali.</li>
<li><b>I numeri prima della firma.</b> Nessuna promessa miracolosa.</li>
<li><b>Euro in Italia, Lek in Albania.</b> Il Lek è sempre euro × 100, su ogni riga: 500 €/mese = 50.000 Lek/mese.</li>
<li><b>Le lettere albanesi si controllano</b> prima di consegnare: ë ç Ë Ç.</li>
</ul>
<div class="box ok" style="margin-top:4mm"><h3>Un messaggio che suona come noi</h3>
<p class="sm" style="margin:0">«Ciao Marta, sono Giorgio di NIPEC. Noleggio a 500 euro al mese, zero anticipo, zero cauzione,
nessun vincolo di durata. Te la porto il primo del mese, me la paghi il trenta. Ti interessa che ti racconti come funziona?»</p></div>
</div>
<div style="padding-top:2mm"><span class="eti">Si scrive così, non così</span>
<table class="tab"><thead><tr><th style="width:50%">Così</th><th>Non così</th></tr></thead><tbody>
<tr><td style="font:500 8.4pt Archivo;color:var(--ink)">«Quel punto non si muove.»</td><td class="mut">«L’adiposità localizzata presenta una resistenza.»</td></tr>
<tr><td style="font:500 8.4pt Archivo;color:var(--ink)">«Te lo diciamo noi se non è il caso.»</td><td class="mut">«Procederemo a una valutazione di idoneità.»</td></tr>
<tr><td style="font:500 8.4pt Archivo;color:var(--ink)">«Mezz’ora in cui non ti vendiamo niente.»</td><td class="mut">«Un percorso che nasce dall’ascolto della persona.»</td></tr>
<tr><td style="font:500 8.4pt Archivo;color:var(--ink)">«Se non serve una macchina nuova, te lo diciamo.»</td><td class="mut">«Soluzioni sinergiche per la crescita del tuo business.»</td></tr>
</tbody></table>
<div style="margin-top:7mm"><span class="eti">La frase di marca, in tre lingue</span>
<div class="card velo" style="padding:4mm 5mm">
<p style="margin:0 0 1.6mm"><span class="chip" style="margin-right:3mm">IT</span><b class="sans" style="font-size:9.6pt;color:var(--navy)">Non vendiamo macchine. Costruiamo sistemi di lavoro.</b></p>
<p style="margin:0 0 1.6mm"><span class="chip" style="margin-right:3mm">SQ</span><b class="sans" style="font-size:9.6pt;color:var(--navy)">Nuk shesim makineri. Ndërtojmë sisteme pune.</b></p>
<p style="margin:0"><span class="chip" style="margin-right:3mm">EN</span><b class="sans" style="font-size:9.6pt;color:var(--navy)">We don’t sell machines. We build working systems.</b></p></div>
<p class="xs mut" style="margin-top:2.4mm">Si usa in chiusura di sito, documenti e presentazioni. Non si accorcia e non si cambia.</p></div>
</div></div>''', zoom=1.22)

# ---- 7. IL MARCHIO
anat = f'''<svg viewBox="0 -24 392 190" style="width:100%;display:block" aria-hidden="true">
<g>{svg_inner('nipec-logo-orizzontale.svg')}</g>
<g stroke="#8E9295" stroke-width=".9" fill="none"><path d="M24 80V127"/><path d="M40 19V-3"/><path d="M73 78V127"/><path d="M343 76.5H356"/></g>
<g font-family="Archivo,sans-serif" font-weight="700" font-size="11" text-anchor="middle" fill="#fff">
<circle cx="24" cy="136" r="9" fill="#123A63"/><text x="24" y="140">1</text>
<circle cx="40" cy="-12" r="9" fill="#123A63"/><text x="40" y="-8">2</text>
<circle cx="73" cy="136" r="9" fill="#123A63"/><text x="73" y="140">3</text>
<circle cx="365" cy="76.5" r="9" fill="#123A63"/><text x="365" y="80.5">4</text></g></svg>'''

pagina('05 · Il marchio', f'''
<div style="display:grid;grid-template-columns:1fr 100mm;gap:12mm;height:100%">
<div>
<span class="eti">Il marchio</span>
<h1 style="font-size:22pt;margin-bottom:5mm">Un anello che non si chiude.</h1>
<div class="card velo" style="padding:8mm 9mm 5mm;margin-bottom:5mm">{anat}</div>
<div class="g2" style="gap:5mm">
<div><p class="sm" style="margin-bottom:1.6mm"><span class="num">1</span>&nbsp; <b>L’anello aperto</b> è un’orbita: un processo che continua, e non si ferma alla consegna.</p>
<p class="sm" style="margin:0"><span class="num">2</span>&nbsp; <b>Il punto</b> che avanza siamo noi, che andiamo avanti con te.</p></div>
<div><p class="sm" style="margin-bottom:1.6mm"><span class="num">3</span>&nbsp; <b>Le tre barre</b> che salgono sono il tuo centro che cresce.</p>
<p class="sm" style="margin:0"><span class="num">4</span>&nbsp; <b>Il filetto verde, bianco e rosso</b> dice «macchina italiana» senza una parola in più.</p></div></div>
</div>
<div>
<span class="eti">Le quattro versioni</span>
<div class="g2" style="gap:3mm;margin-bottom:3mm">
<div class="card" style="padding:3.5mm;height:30mm;display:flex;flex-direction:column;justify-content:space-between"><span class="chip" style="align-self:flex-start">Orizzontale · principale</span>{logo('nipec-logo-orizzontale.svg','width:38mm')}</div>
<div class="card" style="padding:3.5mm;height:30mm;display:flex;flex-direction:column;justify-content:space-between"><span class="chip" style="align-self:flex-start">Verticale</span>{logo('nipec-logo-verticale.svg','width:25mm;align-self:center')}</div>
<div class="card" style="padding:3.5mm;height:30mm;display:flex;flex-direction:column;justify-content:space-between"><span class="chip" style="align-self:flex-start">Compatto</span>{logo('nipec-logo-compatto.svg','width:34mm')}</div>
<div class="card" style="padding:3.5mm;height:30mm;display:flex;flex-direction:column;justify-content:space-between"><span class="chip" style="align-self:flex-start">Emblema</span>{logo('nipec-emblema.svg','width:13mm')}</div>
</div>
<div style="background:var(--navy);border-radius:2.4mm;padding:4mm 5mm;display:flex;justify-content:space-between;align-items:center;margin-bottom:4mm">
<span class="chip" style="background:rgba(255,255,255,.12);color:#9CCBE8">Negativo · su scuro</span>{logo('nipec-logo-orizzontale-negativo.svg','width:44mm')}</div>
<ul class="pt">
<li><b>Orizzontale:</b> carta intestata, copertine, preventivi, sito, video.</li>
<li><b>Verticale:</b> spazio alto e stretto. Vetrofanie, roll-up, adesivi.</li>
<li><b>Compatto:</b> sotto i 28 px la coda non si legge: si usa questo.</li>
<li><b>Emblema:</b> icone, timbri, favicon, spazi quadrati.</li>
</ul>
<p class="xs mut">I file stanno in <span class="mono">MARCHIO/</span>: SVG, PNG, PDF vettoriale. Per stampare si parte sempre dall’SVG o dal PDF, mai da un PNG.</p>
</div></div>''', zoom=1.12)

# ---- 8. SPAZIO, MISURE, FONDI
spazio = f'''<svg viewBox="-36 -36 440 192" style="width:100%;display:block" aria-hidden="true">
<rect x="-28" y="-28" width="424" height="176" fill="#EAF2FA" rx="4"/>
<g stroke="#1C6EA4" stroke-width=".8" fill="rgba(28,110,164,.12)">
<rect x="-28" y="16" width="44" height="88"/><rect x="352" y="16" width="44" height="88"/>
<rect x="16" y="-28" width="336" height="44"/><rect x="16" y="104" width="336" height="44"/></g>
<rect x="16" y="16" width="336" height="88" fill="#fff" stroke="#1C6EA4" stroke-width=".8" stroke-dasharray="3 2.4"/>
<g>{svg_inner('nipec-logo-orizzontale.svg')}</g>
<g font-family="Archivo,sans-serif" font-weight="700" font-size="11" fill="#1C6EA4" text-anchor="middle">
<text x="-6" y="64">x</text><text x="374" y="64">x</text><text x="184" y="-4">x</text><text x="184" y="130">x</text></g>
</svg>'''
fondi = [('Bianco', '#FFFFFF', 'orizzontale-pos.', 'nipec-logo-orizzontale.svg', False),
         ('Velo blu', VELO, 'positivo', 'nipec-logo-orizzontale.svg', False),
         ('Blu profondo', NAVY, 'negativo', 'nipec-logo-orizzontale-negativo.svg', True),
         ('Blu NIPEC', BLU, 'negativo', 'nipec-logo-orizzontale-negativo.svg', True)]
cfondi = ''.join(f'''<div><div style="background:{c};border:1px solid var(--riga);border-radius:2mm;height:19mm;display:flex;align-items:center;justify-content:center">
{logo(f, 'width:30mm')}</div><p class="xs mut" style="margin:1.4mm 0 0"><b style="color:var(--navy)">{n}</b> · {v.replace('orizzontale-pos.','positivo')}</p></div>'''
                 for n, c, v, f, d in fondi)
pagina('06 · Spazio, misure, fondi', f'''
<div style="display:grid;grid-template-columns:1fr 1fr;gap:12mm;height:100%">
<div><span class="eti">Zona di rispetto</span>
<h2 style="margin-bottom:3mm">Intorno al logo, mezzo emblema di aria.</h2>
<div style="margin-bottom:3mm">{spazio}</div>
<p class="sm mut">La <b style="color:var(--blu)">x</b> è la metà dell’emblema. Niente ci entra dentro: né testi, né bordi, né il margine della pagina.</p>
<div style="margin-top:6mm"><span class="eti">Misura minima</span>
<div style="display:flex;gap:9mm;align-items:flex-end;margin-top:1mm">
<div>{logo('nipec-logo-orizzontale.svg','height:7.41mm;width:auto')}<p class="xs mut" style="margin:1.6mm 0 0">Orizzontale e verticale<br><b style="color:var(--navy)">28 px</b> ≈ 7,5 mm di altezza</p></div>
<div>{logo('nipec-logo-compatto.svg','height:4.23mm;width:auto')}<p class="xs mut" style="margin:1.6mm 0 0">Compatto<br><b style="color:var(--navy)">16 px</b> ≈ 4,2 mm</p></div>
<div>{logo('nipec-emblema.svg','height:4.23mm;width:auto')}<p class="xs mut" style="margin:1.6mm 0 0">Emblema<br><b style="color:var(--navy)">16 px</b> ≈ 4,2 mm</p></div>
</div></div></div>
<div><span class="eti">Su che fondo</span>
<h2 style="margin-bottom:3mm">Chiaro: positivo. Scuro: negativo.</h2>
<div class="g2" style="gap:4mm;margin-bottom:5mm">{cfondi}</div>
<div class="box ok" style="margin-bottom:3mm"><h3>Su una foto</h3><p class="sm" style="margin:0">Solo il negativo, e solo su una zona uniforme e scura. Se la zona non è uniforme, si mette il logo su un riquadro blu profondo.</p></div>
<div class="box"><h3>Non si schiarisce il positivo</h3><p class="sm" style="margin:0">Su fondo scuro non si prende il logo normale e lo si rende bianco: esiste il file negativo, con i colori già calibrati.</p></div>
<div class="box" style="margin-top:3mm"><h3>Il filetto tricolore</h3><p class="sm" style="margin:0">Ce l’hanno orizzontale e verticale. Compatto ed emblema <b>no</b>, e non si aggiunge a mano.</p></div>
</div></div>''', zoom=1.15)

# ---- 9. GLI ERRORI
def sbaglio(titolo, contenuto, bg='#fff', nota=''):
    return f'''<div><div style="background:{bg};border:1px solid var(--riga);border-radius:2mm;height:36mm;display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden">
{contenuto}<svg viewBox="0 0 20 20" style="position:absolute;right:2mm;top:2mm;width:6mm;height:6mm" aria-hidden="true"><circle cx="10" cy="10" r="10" fill="#9C3A28"/><path d="M6 6l8 8M14 6l-8 8" stroke="#fff" stroke-width="2.2" stroke-linecap="round"/></svg></div>
<h3 style="margin:2mm 0 .4mm;font-size:8.6pt">{titolo}</h3><p class="xs mut" style="margin:0">{nota}</p></div>'''

L = svg_file('nipec-logo-orizzontale.svg')
Lcol = (L.replace('#1C6EA4', '#E08A1E').replace('#123A63', '#7A1F5C').replace('#5AA6D6', '#E8C33A'))
Lfont = L.replace("font-family=\"Archivo, 'Helvetica Neue', Arial, sans-serif\"", 'font-family="Georgia,serif" font-style="italic"')
def L_(s, st): return s.replace('<svg ', f'<svg style="{st}" ', 1)
compat_fil = f'''<div style="width:36mm">{logo('nipec-logo-compatto.svg','width:36mm')}
<div style="display:flex;margin-top:1mm;height:1mm"><i style="flex:1;background:#008C45"></i><i style="flex:1;background:#F4F5F0;border:.1mm solid #C9D4DE"></i><i style="flex:1;background:#CD212A"></i></div></div>'''
errori = [
    sbaglio('Stirato o schiacciato', f'<div style="transform:scale(1.55,.62)">{L_(L,"width:30mm")}</div>', nota='Si rimpicciolisce tutto insieme, oppure si cambia versione.'),
    sbaglio('Ricolorato', L_(Lcol, 'width:36mm'), nota='I colori del marchio non si cambiano, nemmeno quelli del tricolore.'),
    sbaglio('Con ombra o bagliore', L_(L, 'width:36mm;filter:drop-shadow(1.2mm 1.4mm .9mm rgba(0,0,0,.5))'), nota='Niente ombre, bordi, bagliori, sfumature.'),
    sbaglio('Inclinato o ruotato', f'<div style="transform:rotate(-13deg)">{L_(L,"width:34mm")}</div>', nota='Sempre dritto, su una riga.'),
    sbaglio('Su un fondo che lo disturba', L_(L, 'width:36mm'), bg='repeating-linear-gradient(115deg,#123A63 0 3mm,#1C6EA4 3mm 6mm,#5AA6D6 6mm 9mm)', nota='Se il fondo non è uniforme, il logo non ci va.'),
    sbaglio('Con un altro carattere', L_(Lfont, 'width:36mm'), nota='«NIPEC» è sempre in Archivo: i file master hanno già il testo in tracciati.'),
    sbaglio('Positivo su fondo scuro', L_(L, 'width:36mm'), bg=NAVY, nota='Su scuro si usa il negativo, non il positivo schiarito.'),
    sbaglio('Filetto aggiunto al compatto', compat_fil, nota='Il filetto esiste solo dove c’è la coda: orizzontale e verticale.'),
]
pagina('07 · Gli errori', f'''
<span class="eti">Cosa non si fa</span>
<h1 style="font-size:22pt;margin-bottom:5mm">Otto modi di rovinare il marchio.</h1>
<div class="g4" style="gap:5mm 4.5mm">{''.join(errori)}</div>
<div class="box" style="margin-top:5mm"><p class="sm" style="margin:0"><b>La regola dietro tutte le altre:</b> il marchio si usa com’è, dal file giusto. Se il file giusto non c’è, si chiede: non si ritocca.
Se serve una variante nuova, la si fa una volta, bene, e entra in <span class="mono">MARCHIO/</span>.</p></div>''', zoom=1.2)

# ---- 10. COLORE
def swatch(nome, hexv, ruolo, testo_chiaro=True, alto=34):
    r, g, b = _rgb(hexv); c, m, y, k = cmyk(hexv)
    fg = '#fff' if testo_chiaro else INK
    return f'''<div class="sw"><div class="col" style="background:{hexv};height:{alto}mm;color:{fg}">{nome}</div>
<div class="dati"><b>{hexv}</b>RGB {r} · {g} · {b}<br>CMYK {c} · {m} · {y} · {k}<br><span style="color:var(--ink)">{ruolo}</span></div></div>'''
pagina('08 · Colore', f'''
<span class="eti">Colore</span>
<h1 style="font-size:22pt;margin-bottom:1.6mm">Tre blu, tanto bianco.</h1>
<p style="font-size:9.6pt;margin-bottom:5mm;width:200mm" class="mut">Il blu profondo è il colore di NIPEC. Gli altri due lo accompagnano. Il fondo resta bianco: i colori fanno il contorno, non il riempimento.</p>
<div class="g3" style="margin-bottom:5mm">
{swatch('Blu profondo', NAVY, 'Il nodo, la parola NIPEC, i titoli, i fondi scuri.')}
{swatch('Blu NIPEC', BLU, 'L’anello, i pulsanti, i link, gli accenti.')}
{swatch('Blu chiaro', CHIARO, 'La barra bassa, i grafici, il nodo sul negativo. Su scuro.')}
</div>
<span class="eti">Neutri</span>
<div style="display:grid;grid-template-columns:repeat(6,1fr);gap:4mm">
{swatch('Inchiostro', INK, 'Il testo.', True, 17)}{swatch('Grigio testo', INK2, 'Testi secondari, note.', True, 17)}
{swatch('Grigio', GRIGIO, 'Solo stampa, testi grandi.', True, 17)}{swatch('Riga', RIGA, 'Filetti, bordi delle schede.', False, 17)}
{swatch('Velo blu', VELO, 'Fondo dei riquadri.', False, 17)}{swatch('Bianco', BIANCO, 'Il fondo di tutto.', False, 17)}
</div>
<p class="xs mut" style="margin-top:4mm">I valori CMYK sono la conversione standard dai valori RGB, indicativi: non c’è un Pantone. Prima di una stampa grande si chiede una prova colore.
Le tinte «Velo» e «Riga» sono quelle del sito; nei documenti se ne usavano due versioni quasi identiche: da qui in poi vale questa.</p>''', zoom=1.08)

# ---- 11. COLORE IN USO
coppie_t = [('Inchiostro', INK), ('Grigio testo', INK2), ('Blu profondo', NAVY), ('Blu NIPEC', BLU), ('Blu chiaro', CHIARO), ('Grigio', GRIGIO), ('Bianco', BIANCO)]
coppie_f = [('Bianco', BIANCO), ('Velo blu', VELO), ('Blu profondo', NAVY), ('Blu NIPEC', BLU)]
righe_c = ''
for tn, tc in coppie_t:
    celle = ''
    for fn, fc in coppie_f:
        if tc.upper() == fc.upper():
            celle += '<td style="text-align:center;color:#B7C3CD">—</td>'; continue
        r = rapporto(tc, fc)
        if r >= 4.5: st, tx = 'background:#E7F3EC;color:#1B6E52', f'{r:.1f}'
        elif r >= 3: st, tx = 'background:#F8EFDB;color:#8A6208', f'{r:.1f}'
        else: st, tx = 'background:#FAEAE6;color:#9C3A28', f'{r:.1f}'
        celle += f'<td style="text-align:center;font:600 8pt Archivo;{st}">{tx}</td>'
    righe_c += f'<tr><td><span style="display:inline-block;width:3mm;height:3mm;border-radius:50%;background:{tc};border:1px solid #C9D4DE;vertical-align:-.5mm;margin-right:2mm"></span>{tn}</td>{celle}</tr>'
pagina('09 · Colore in uso', f'''
<div style="display:grid;grid-template-columns:1fr 1fr;gap:14mm">
<div><span class="eti">Le proporzioni</span>
<h2 style="margin-bottom:3mm">Quasi tutto bianco. Il blu profondo guida.</h2>
<div style="display:flex;height:16mm;border-radius:2mm;overflow:hidden;border:1px solid var(--riga);margin-bottom:2mm">
<i style="flex:70;background:#fff"></i><i style="flex:0 0 0;background:var(--velo)"></i><i style="flex:18;background:var(--navy)"></i><i style="flex:9;background:var(--blu)"></i><i style="flex:3;background:var(--chiaro)"></i></div>
<div style="display:flex;flex-wrap:wrap;gap:1.4mm 5mm;font:600 7pt Archivo;color:var(--ink2)">
<span><i style="display:inline-block;width:2.6mm;height:2.6mm;border:1px solid #C9D4DE;margin-right:1.4mm;vertical-align:-.3mm"></i>Bianco e velo, circa 70%</span>
<span><i style="display:inline-block;width:2.6mm;height:2.6mm;background:var(--navy);margin-right:1.4mm;vertical-align:-.3mm"></i>Blu profondo 18%</span>
<span><i style="display:inline-block;width:2.6mm;height:2.6mm;background:var(--blu);margin-right:1.4mm;vertical-align:-.3mm"></i>Blu NIPEC 9%</span>
<span><i style="display:inline-block;width:2.6mm;height:2.6mm;background:var(--chiaro);margin-right:1.4mm;vertical-align:-.3mm"></i>Blu chiaro 3%</span></div>
<div style="margin-top:6mm"><span class="eti">Il tricolore</span>
<div style="display:flex;gap:3mm;align-items:center"><div style="display:flex;width:44mm;height:3.4mm;flex:none"><i style="flex:1;background:#008C45"></i><i style="flex:1;background:#F4F5F0;border:.1mm solid #C9D4DE"></i><i style="flex:1;background:#CD212A"></i></div>
<p class="sm mut" style="margin:0">Verde <span class="mono">#008C45</span> · Bianco <span class="mono">#F4F5F0</span> · Rosso <span class="mono">#CD212A</span></p></div>
<p class="sm" style="margin-top:2mm">Vive <b>solo</b> nel filetto del marchio. Non diventa un colore della grafica: non lo si usa per bordi, sfondi, pulsanti.</p></div>
<div style="margin-top:5mm"><span class="eti">Colori di stato</span>
<div class="g3" style="gap:3mm">
<div style="background:#E2F1EA;color:#1B6E52;border-radius:1.6mm;padding:3mm"><b class="sans" style="font-size:8.2pt">Tutto a posto</b><br><span class="mono">#1B6E52</span></div>
<div style="background:#F8EFDB;color:#8A6208;border-radius:1.6mm;padding:3mm"><b class="sans" style="font-size:8.2pt">Attenzione</b><br><span class="mono">#8A6208</span></div>
<div style="background:#FAEAE6;color:#9C3A28;border-radius:1.6mm;padding:3mm"><b class="sans" style="font-size:8.2pt">Problema, no</b><br><span class="mono">#9C3A28</span></div></div>
<p class="xs mut" style="margin-top:1.6mm">Servono nei documenti e nelle schede per dire ok, attenzione, errore. Non sono colori di marca.</p></div></div>
<div><span class="eti">Si legge o non si legge</span>
<h2 style="margin-bottom:3mm">Il contrasto, misurato.</h2>
<table class="tab"><thead><tr><th>Testo su sfondo</th>{''.join(f'<th style="text-align:center">{n}</th>' for n, _ in coppie_f)}</tr></thead>
<tbody>{righe_c}</tbody></table>
<div style="display:flex;gap:3mm;margin-top:3mm;font:600 6.8pt Archivo">
<span style="background:#E7F3EC;color:#1B6E52;padding:1mm 2.4mm;border-radius:1mm">4,5 o più · si legge a ogni misura</span>
<span style="background:#F8EFDB;color:#8A6208;padding:1mm 2.4mm;border-radius:1mm">3 – 4,5 · solo testo grande</span>
<span style="background:#FAEAE6;color:#9C3A28;padding:1mm 2.4mm;border-radius:1mm">sotto 3 · non si usa per testo</span></div>
<ul class="pt" style="margin-top:4mm">
<li><b>Blu chiaro e Grigio</b> su bianco non reggono un testo piccolo: sono per elementi grafici, o per testi grandi.</li>
<li><b>Il pulsante principale</b> è blu profondo con scritta bianca: su bianco è quello che si vede di più.</li>
<li>Il colore forte <b>fa il contorno</b>: filetti fra le fasce, filo intorno alle schede, riga in testa alle colonne.</li></ul></div></div>''', zoom=1.28)

# ---- 12. TIPOGRAFIA
scala = [('Titolo di pagina', 'Archivo 700', '25 pt', '34 px'), ('Titolo di sezione', 'Archivo 700', '12,5 pt', '20 px'),
         ('Etichetta', 'Archivo 600 · MAIUSCOLO', '7 pt · spaziatura .16em', '11 px'),
         ('Testo', 'Source Serif 4 · 400', '9,2 pt', '16 px'), ('Nota', 'Source Serif 4 · 400', '7,4 pt', '13 px')]
rs = ''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>' for a, b, c, d in scala)
pagina('10 · Tipografia', f'''
<div style="display:grid;grid-template-columns:1fr 1fr;gap:12mm">
<div class="card" style="padding:6mm 7mm"><span class="eti">Marchio, titoli, etichette, interfacce</span>
<div style="font:700 62pt/1 Archivo;color:var(--navy);letter-spacing:-.02em;margin:1mm 0 3mm">Archivo</div>
<div class="sans" style="font-size:10.6pt;line-height:1.7;color:var(--ink)"><span style="font-weight:400">Regular 400 · Tecnologie estetiche professionali</span><br>
<span style="font-weight:500">Medium 500 · Il metodo NIPEC</span><br><span style="font-weight:600">Semibold 600 · Laser Ares · Afrodite VS++</span><br>
<span style="font-weight:700">Bold 700 · Non vendiamo macchine.</span></div>
<p class="xs mut" style="margin:3mm 0 0">Sans-serif grottesco. È il carattere del logo, quindi dei titoli: se stona col logo, la pagina sembra fatta da due persone.</p></div>
<div class="card" style="padding:6mm 7mm"><span class="eti">Testo lungo nei documenti</span>
<div style="font:600 62pt/1 'Source Serif 4',serif;color:var(--navy);letter-spacing:-.01em;margin:1mm 0 3mm">Source Serif</div>
<p style="font-size:10pt;line-height:1.55;margin:0 0 2mm">Una macchina, da sola, non riempie l’agenda. La differenza tra il centro che rientra dell’investimento e quello che si ferma non è il macchinario: è tutto quello che gli sta intorno.</p>
<p class="xs mut" style="margin:0">Serif di lettura. Protocolli, contratti, proposte, schede: tutto ciò che si legge a lungo. Sul sito il testo è in Archivo.</p></div></div>
<div style="display:grid;grid-template-columns:1.25fr 1fr;gap:12mm;margin-top:6mm">
<div><span class="eti">La scala</span>
<table class="tab"><thead><tr><th>Uso</th><th>Carattere</th><th>Stampa</th><th>Schermo</th></tr></thead><tbody>{rs}</tbody></table></div>
<div><span class="eti">Poche regole</span>
<ul class="pt">
<li><b>Il maiuscolo</b> è per le etichette corte. I titoli si scrivono normali: si leggono meglio.</li>
<li><b>Il corpo non scende</b> sotto i 7,4 pt in stampa e i 13 px a schermo.</li>
<li><b>ë ç Ë Ç</b> si controllano nel file del carattere, non si danno per scontate. Archivo e Source Serif le hanno.</li>
<li><b>Licenza libera</b> (SIL Open Font), uso commerciale incluso. I file stanno nella cartella <span class="mono">caratteri</span>, mai sui server di Google.</li>
<li>Senza i caratteri: Helvetica Neue o Arial per i titoli, Georgia per il testo.</li></ul></div></div>''')

# ---- 13. LINGUAGGIO GRAFICO
ico = ''.join(f'<div style="text-align:center">{icona(k, 12)}<p class="xs" style="margin:1.2mm 0 0;font-family:Archivo;font-weight:600;color:var(--navy)">{t}</p></div>' for k, t, _ in pilastri)
pagina('11 · Linguaggio grafico', f'''
<span class="eti">Linguaggio grafico</span>
<h1 style="font-size:22pt;margin-bottom:5mm">Quattro segni, presi dal marchio.</h1>
<div class="g2" style="gap:5mm 6mm">
<div class="card" style="display:grid;grid-template-columns:42mm 1fr;gap:5mm;align-items:center;min-height:51mm">
<div style="background:var(--navy);border-radius:2mm;height:40mm;position:relative;overflow:hidden"><svg viewBox="0 0 100 100" style="position:absolute;left:4mm;top:6mm;width:62mm;height:62mm" aria-hidden="true">
<circle cx="50" cy="50" r="40" fill="none" stroke="rgba(255,255,255,.3)" stroke-width="2.6"/><path d="M50 10 A40 40 0 1 1 30 15.36" fill="none" stroke="#fff" stroke-width="7.5" stroke-linecap="round"/><circle cx="30" cy="15.36" r="5.4" fill="#5AA6D6"/></svg></div>
<div><h3>L’orbita</h3><p class="sm mut" style="margin:1mm 0 0">L’anello aperto, grande, tagliato dal bordo della pagina. Sta sui fondi blu profondo, come firma. Uno solo per pagina, mai sopra al testo.</p></div></div>
<div class="card" style="display:grid;grid-template-columns:42mm 1fr;gap:5mm;align-items:center;min-height:51mm">
<div style="background:var(--velo);border-radius:2mm;height:40mm;display:flex;align-items:flex-end;justify-content:center;gap:3.4mm;padding-bottom:8mm">
<i style="width:5.6mm;height:10mm;border-radius:2.8mm;background:var(--chiaro)"></i><i style="width:5.6mm;height:17mm;border-radius:2.8mm;background:var(--blu)"></i><i style="width:5.6mm;height:25mm;border-radius:2.8mm;background:var(--navy)"></i></div>
<div><h3>Le barre</h3><p class="sm mut" style="margin:1mm 0 0">Tre barre che salgono, sempre a punta tonda. Per i numeri che crescono: un grafico, un contatore, un elenco di risultati. Mai in discesa.</p></div></div>
<div class="card" style="min-height:51mm"><h3>Le icone</h3><p class="sm mut" style="margin:1mm 0 3.4mm">Cinque icone, per i cinque pilastri. Fatte con le forme del logo: anello, punto, barre. Linea di 3 px su griglia 48, estremi tondi, solo blu NIPEC.</p>
<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:2mm">{ico}</div></div>
<div class="card" style="min-height:51mm"><h3>Riquadri e schede</h3><p class="sm mut" style="margin:1mm 0 3mm">Una scheda ha un filo da 1 px color Riga e angoli appena tondi. Un riquadro che dice qualcosa ha una barra a sinistra: blu per il «si fa», rossa per il «non si fa».</p>
<div class="box" style="margin-bottom:2mm;padding:2.4mm 4mm"><p class="xs" style="margin:0"><b>Si fa</b> · barra blu, fondo velo</p></div>
<div class="box no" style="padding:2.4mm 4mm"><p class="xs" style="margin:0"><b>Non si fa</b> · barra rossa, fondo rosato</p></div></div>
</div>''', zoom=1.22)

# ---- 14. IMMAGINI
F1, F2 = foto('741b069dc662.jpg', 760), foto('24b97aa371e6.jpg', 760)
pagina('12 · Immagini', f'''
<div style="display:grid;grid-template-columns:128mm 1fr;gap:12mm;height:100%">
<div><span class="eti">Le macchine</span>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:4mm;margin-bottom:3mm">
<div style="border:1px solid var(--riga);border-radius:2.4mm;background:#fff;height:92mm;display:flex;align-items:center;justify-content:center;overflow:hidden"><img src="{F1}" style="max-height:88mm;max-width:100%"></div>
<div style="border:1px solid var(--riga);border-radius:2.4mm;background:#fff;height:92mm;display:flex;align-items:center;justify-content:center;overflow:hidden"><img src="{F2}" style="max-height:88mm;max-width:100%"></div></div>
<p class="sm"><b>Così:</b> la macchina intera, ritagliata, su fondo bianco, con luce uniforme e un’ombra morbida sotto. Frontale o tre quarti. Sono le due foto che oggi reggono: Afrodite e Cryo 360.</p>
<div class="box no" style="margin-top:3mm"><p class="sm" style="margin:0"><b>Da rifare:</b> delle otto foto di macchine, sei sono piccole o miniature. Mancano in alta risoluzione Uriel, Borea e le Ares. Si chiedono ai fornitori: lato lungo almeno 1600 px.</p></div>
</div>
<div><span class="eti">Le regole</span>
<h2 style="margin-bottom:3mm">Vere, chiare, senza effetti.</h2>
<ul class="pt">
<li><b>Fondo bianco o velo blu.</b> Mai un colore di fondo dietro la macchina, mai un logo aggiunto sopra la macchina.</li>
<li><b>Centri e persone vere.</b> Cabine, mani, operatrici, i centri dei nostri clienti, a cominciare da Demetra Center. Luce naturale. Niente foto stock con modelle.</li>
<li><b>Nessun «prima e dopo» che prometta.</b> Se si mostra un risultato è vero, con data e con il permesso della persona.</li>
<li><b>Nessun filtro</b>, nessuna cornice, nessuna sfumatura colorata sopra la foto.</li>
<li><b>Testo sopra una foto</b> solo su una zona uniforme, con il logo negativo.</li>
<li><b>Misure:</b> sito, lato lungo almeno 1600 px. Stampa, 300 dpi alla dimensione finale. Si parte dall’originale, mai da uno screenshot.</li>
<li><b>Ogni foto ha un nome</b> che dice cosa è e di chi: <span class="mono">afrodite-vs-frontale.jpg</span>, non <span class="mono">IMG_4471.jpg</span>.</li></ul></div></div>''', zoom=1.15)

# ---- 15. DUE PAESI
pagina('13 · Due paesi, tre lingue', f'''
<span class="eti">Un marchio, due società</span>
<h1 style="font-size:22pt;margin-bottom:4mm">NIPEC è lo stesso a Padenghe e a Tirana.</h1>
<table class="tab"><thead><tr><th style="width:14%"></th><th style="width:43%">Italia</th><th>Albania</th></tr></thead><tbody>
<tr><td>Società</td><td>PHD System S.r.l.</td><td>PHD SYSTEM</td></tr>
<tr><td>Dati fiscali</td><td>P.IVA 04696530981</td><td>NIPT M27101203D</td></tr>
<tr><td>Sede</td><td>Via Rovetta 29, 25080 Padenghe sul Garda (BS)</td><td>Rruga Donika Kastrioti 3, Tiranë</td></tr>
<tr><td>Contatti</td><td>WhatsApp +39 351 846 6025 · Numero verde 800 141 726<br>info@nipecestetica.com</td><td>+355 69 212 9786<br>info@nipecestetica.com</td></tr>
<tr><td>Lingue</td><td>Italiano · inglese</td><td>Shqip · inglese</td></tr>
<tr><td>Prezzi</td><td>Euro: 500 €/mese</td><td>Lek: 50.000 Lek/mese <span class="mut">(euro × 100, sempre)</span></td></tr>
<tr><td>Centro pilota</td><td>—</td><td>Demetra Center, Tirana</td></tr>
</tbody></table>
<div class="g4" style="margin-top:6mm">
<div class="box"><h3>Il logo non cambia</h3><p class="sm" style="margin:0">Identico in tutte le lingue. La scritta «TECNOLOGIE ESTETICHE» resta in italiano ovunque: fa parte del marchio, non si traduce.</p></div>
<div class="box"><h3>Cambia la riga legale</h3><p class="sm" style="margin:0">Ogni documento porta <b>una sola società</b>: quella che lo emette. Mai le due insieme sulla stessa carta intestata, contratto o fattura.</p></div>
<div class="box"><h3>Tre lingue, un impaginato</h3><p class="sm" style="margin:0">Sito in italiano, albanese e inglese, con la stessa grafica. L’albanese si controlla sempre: ë ç Ë Ç, e i prezzi in Lek.</p></div>
<div class="box"><h3>Una voce sola</h3><p class="sm" style="margin:0">Stesso tono, stesse frasi corte. Non si traduce parola per parola: si dice la stessa cosa come la direbbe una titolare di Tirana.</p></div>
</div>''', zoom=1.12)

# ---- 16/17. APPLICAZIONI (oggetti a misura vera, poi scalati)
WEB, MAIL = 'www.nipecestetica.eu', 'info@nipecestetica.com'
LEGALI = {
    'it': ('NIPEC · Tecnologie Estetiche — PHD System S.r.l. · P.IVA 04696530981 · Via Rovetta 29, 25080 Padenghe sul Garda (BS)',
           f'WhatsApp +39 351 846 6025 · Numero verde 800 141 726 · {MAIL} · {WEB}'),
    'al': ('NIPEC · Tecnologie Estetiche — PHD SYSTEM · NIPT M27101203D · Rruga Donika Kastrioti 3, Tiranë',
           f'+355 69 212 9786 · {MAIL} · {WEB}'),
}
def carta(paese):
    a, b = LEGALI[paese]
    return f'''<div style="width:210mm;height:297mm;background:#fff;position:relative;overflow:hidden">
{logo('nipec-logo-orizzontale.svg','position:absolute;left:18mm;top:14mm;width:62mm')}
<div style="position:absolute;left:21mm;right:21mm;bottom:14mm;border-top:.25mm solid #D4E3EF;padding-top:3mm;text-align:center;
font:500 6.6pt/1.7 Archivo,sans-serif;color:#44535F;letter-spacing:.03em">{a}<br>{b}</div></div>'''

def biglietto_fronte():
    return f'''<div style="width:85mm;height:55mm;background:#123A63;position:relative;overflow:hidden">
<svg viewBox="0 0 100 100" style="position:absolute;right:-22mm;bottom:-24mm;width:70mm;height:70mm;opacity:.16" aria-hidden="true">{EMBL_NEG}</svg>
{logo('nipec-logo-orizzontale-negativo.svg','position:absolute;left:9mm;top:9mm;width:50mm')}
<div style="position:absolute;left:9.6mm;bottom:8mm;font:600 5.2pt Archivo;letter-spacing:.14em;color:#9CCBE8;text-transform:uppercase">Italia · Albania</div></div>'''

def biglietto_retro():
    return f'''<div style="width:85mm;height:55mm;background:#fff;position:relative;overflow:hidden;border:.2mm solid #D4E3EF;box-sizing:border-box">
<div style="position:absolute;left:9mm;top:9mm">
<div style="font:700 10.4pt Archivo;color:#123A63;letter-spacing:-.005em">Giorgio Petrelli</div>
<div style="font:600 5.4pt Archivo;letter-spacing:.14em;text-transform:uppercase;color:#1C6EA4;margin-top:.8mm">Fondatore</div></div>
<div style="position:absolute;left:9mm;bottom:8mm;font:500 6.4pt/1.7 Archivo;color:#44535F">WhatsApp +39 351 846 6025<br>{MAIL}<br>{WEB}<br>Via Rovetta 29, 25080 Padenghe sul Garda (BS)</div>
{logo('nipec-emblema.svg','position:absolute;right:8mm;top:8mm;width:11mm')}</div>'''

def scala_blocco(html, w, h, s):
    return f'<div style="width:{w*s}mm;height:{h*s}mm;position:relative;overflow:hidden"><div style="width:{w}mm;height:{h}mm;zoom:{s}">{html}</div></div>'

SH = 'box-shadow:0 .6mm 2.4mm rgba(18,58,99,.22);'
firma = f'''<div style="border-top:.9mm solid #1C6EA4;padding:3.4mm 4mm;background:#fff;font:400 7.6pt/1.55 Arial,Helvetica,sans-serif;color:#17222E;width:100%">
<b style="font-size:9pt;color:#123A63">Giorgio Petrelli</b><br>Fondatore · <b style="color:#123A63">NIPEC</b> — Tecnologie Estetiche<br>
<span style="color:#44535F">WhatsApp +39 351 846 6025 · {MAIL}<br>{WEB}</span><br>
<span style="color:#44535F;font-size:6.6pt">Non vendiamo macchine. Costruiamo sistemi di lavoro.</span></div>'''

pagina('14 · Applicazioni: stampa', f'''
<div style="display:grid;grid-template-columns:auto 86mm 1fr;gap:11mm;height:100%">
<div><span class="eti">Carta intestata · A4</span>
<div style="{SH}border:.2mm solid #D4E3EF;width:max-content">{scala_blocco(carta('it'), 210, 297, .5)}</div>
<p class="xs mut" style="margin:2mm 0 0;width:105mm">Il logo orizzontale a sinistra, la riga legale in fondo. Il resto è bianco: la lettera la scrive chi la firma.</p></div>
<div><span class="eti">Biglietto da visita · 85 × 55</span>
<div style="{SH}width:max-content;margin-bottom:4mm">{biglietto_fronte()}</div>
<div style="{SH}width:max-content">{biglietto_retro()}</div>
<p class="xs mut" style="margin:2mm 0 0">Fronte blu profondo con il negativo. Retro bianco con nome e dati.</p></div>
<div><span class="eti">Come si usa</span>
<ul class="pt">
<li><b>Una società per foglio.</b> Per l’Albania c’è la carta intestata con PHD SYSTEM e il NIPT.</li>
<li><b>Il logo non si ingrandisce:</b> 62 mm di larghezza, mai oltre.</li>
<li><b>Carta:</b> bianca, opaca, 100 g o più. Niente patinata lucida.</li>
<li><b>Il biglietto</b> si stampa con 3 mm di abbondanza: il file pronto è in <span class="mono">KIT-CARTOLERIA/</span>.</li>
<li><b>Niente cornici</b>, niente logo ripetuto in filigrana sulla lettera.</li></ul>
<div class="box" style="margin-top:3mm"><p class="xs" style="margin:0"><b>Il file della lettera</b> è per la tipografia. Per scrivere in Word o Docs serve il modello con logo e riga legale già dentro: si fa dopo.</p></div></div></div>''')

proposta = f'''<div style="width:210mm;height:297mm;background:#fff;position:relative;overflow:hidden">
<div style="position:absolute;left:0;top:0;right:0;height:158mm;background:#123A63;overflow:hidden">
<svg viewBox="0 0 100 100" style="position:absolute;right:-70mm;top:-12mm;width:230mm;height:230mm;opacity:.17" aria-hidden="true">{EMBL_NEG}</svg>
{logo('nipec-logo-orizzontale-negativo.svg','position:absolute;left:20mm;top:18mm;width:70mm')}
<div style="position:absolute;left:20mm;bottom:20mm;width:150mm">
<div style="font:600 8pt Archivo;letter-spacing:.16em;text-transform:uppercase;color:#5AA6D6;margin-bottom:5mm">Proposta per il tuo centro</div>
<div style="font:700 36pt/1.05 Archivo;color:#fff;letter-spacing:-.015em">Un sistema di lavoro,<br>non solo una macchina.</div></div></div>
<div style="position:absolute;left:20mm;top:174mm;font:600 7pt Archivo;letter-spacing:.14em;text-transform:uppercase;color:#1C6EA4">Preparata per</div>
<div style="position:absolute;left:20mm;top:181mm;font:700 15pt Archivo;color:#123A63">[Nome del centro]</div>
<div style="position:absolute;left:20mm;top:190mm;font:400 10pt 'Source Serif 4',serif;color:#44535F">[Città] · [Data]</div>
<div style="position:absolute;left:20mm;right:20mm;bottom:14mm;border-top:.25mm solid #D4E3EF;padding-top:3mm;font:500 6.8pt/1.7 Archivo;color:#44535F">{LEGALI['it'][0]}</div></div>'''

post_a = f'''<div style="width:70mm;height:70mm;background:#123A63;position:relative;overflow:hidden">
<svg viewBox="0 0 100 100" style="position:absolute;right:-26mm;bottom:-28mm;width:84mm;height:84mm;opacity:.2" aria-hidden="true">{EMBL_NEG}</svg>
{logo('nipec-emblema-negativo.svg','position:absolute;left:6mm;top:6mm;width:9mm')}
<div style="position:absolute;left:6mm;right:6mm;top:24mm;font:700 15.2pt/1.1 Archivo;color:#fff;letter-spacing:-.012em">Non vendiamo<br>macchine.<br><span style="color:#5AA6D6">Costruiamo sistemi<br>di lavoro.</span></div>
<div style="position:absolute;left:6mm;bottom:5.6mm;font:600 5pt Archivo;letter-spacing:.16em;color:#9CCBE8">NIPEC · TECNOLOGIE ESTETICHE</div></div>'''
post_b = f'''<div style="width:70mm;height:70mm;background:#fff;border:.2mm solid #D4E3EF;box-sizing:border-box;position:relative;overflow:hidden">
<div style="position:absolute;left:0;top:0;bottom:0;width:2.2mm;background:#1C6EA4"></div>
{logo('nipec-logo-compatto.svg','position:absolute;left:8mm;top:6mm;width:24mm')}
<div style="position:absolute;left:8mm;top:20mm;font:600 5.2pt Archivo;letter-spacing:.16em;text-transform:uppercase;color:#1C6EA4">Noleggio · Laser Ares</div>
<div style="position:absolute;left:8mm;right:6mm;top:25.5mm;font:700 15pt/1.08 Archivo;color:#123A63;letter-spacing:-.012em">Zero anticipo.<br>Zero cauzione.<br>Nessun vincolo.</div>
<div style="position:absolute;left:8mm;right:6mm;bottom:5.6mm;display:flex;align-items:flex-end;justify-content:space-between">
<div><div style="font:700 17pt/1 Archivo;color:#123A63">500 €</div><div style="font:500 5.4pt Archivo;color:#44535F">al mese</div></div>
<div style="font:600 5pt Archivo;letter-spacing:.08em;color:#1C6EA4">{WEB}</div></div></div>'''

pagina('15 · Applicazioni: digitale', f'''
<div style="display:grid;grid-template-columns:153mm 1fr;gap:12mm;height:100%">
<div>
<div style="display:grid;grid-template-columns:72mm 72mm;gap:9mm;margin-bottom:7mm">
<div><span class="eti">Post · il marchio</span><div style="{SH}width:max-content">{post_a}</div>
<p class="xs mut" style="margin:2mm 0 0">Blu profondo, emblema in orbita, la frase di marca. Per presentarci.</p></div>
<div><span class="eti">Post · un’offerta</span><div style="{SH}width:max-content">{post_b}</div>
<p class="xs mut" style="margin:2mm 0 0">Fondo bianco, barra blu, una cifra sola in grande. Esempio: i numeri sono quelli del noleggio di oggi.</p></div></div>
<div style="display:grid;grid-template-columns:96mm 1fr;gap:9mm">
<div><span class="eti">Firma e-mail</span>
<div style="border:1px solid var(--riga);border-radius:1.6mm;padding:3mm">{firma}</div>
<p class="xs mut" style="margin:2mm 0 0">Solo testo: l’immagine non serve e non finisce in spam. Il file da copiare è in <span class="mono">KIT-CARTOLERIA/</span>.</p></div>
<div><span class="eti">Sui social</span>
<ul class="pt"><li>Un post, <b>una frase</b>.</li><li>Una sola cifra in grande.</li><li>Il logo, <b>una volta</b>, piccolo.</li><li>1080 × 1080 px; storie 1080 × 1920.</li></ul></div></div>
</div>
<div><span class="eti">Copertina proposta · A4</span><div style="{SH}width:max-content">{scala_blocco(proposta, 210, 297, .46)}</div>
<p class="xs mut" style="margin:2mm 0 0">Metà blu, metà bianca. Il nome del centro in primo piano.</p></div></div>''')

# ---- 18. PRIMA DI MANDARE FUORI
chk = ['Il logo è quello giusto: positivo su chiaro, negativo su scuro, preso dal file e non da una foto dello schermo.',
       'C’è mezzo emblema di aria intorno al logo, e nessun errore tra gli otto della pagina 9.',
       'I colori sono quelli del libro. Il tricolore c’è solo nel filetto del logo.',
       'I titoli sono in Archivo, il testo lungo in Source Serif. Nessun terzo carattere.',
       'Frasi corte. Nessun blocco di testo sopra le sei righe. Nessuna parola da brochure.',
       'I numeri sono veri e con la data. Nessuna promessa che non si può mantenere.',
       'Una sola società emittente: PHD System S.r.l. oppure PHD SYSTEM, mai le due insieme.',
       'In albanese: ë ç Ë Ç controllati, e ogni prezzo in Lek è l’euro × 100.',
       'Il telefono è 351 846 6025 (Italia) o +355 69 212 9786 (Albania). Nessun altro.',
       'Le foto sono vere, grandi e senza effetti.']
chk_h = ''.join(f'<div style="display:flex;gap:3mm;padding:1.7mm 0;border-bottom:1px solid var(--riga);align-items:flex-start">'
                f'<i style="flex:none;width:4mm;height:4mm;border:1.2px solid var(--blu);border-radius:1mm;margin-top:.5mm"></i>'
                f'<span style="font-size:8.8pt;line-height:1.4">{t}</span></div>' for t in chk)
pagina('16 · Prima di mandare fuori', f'''
<div style="display:grid;grid-template-columns:1fr 94mm;gap:14mm;height:100%">
<div><span class="eti">Prima di mandare fuori qualunque cosa</span>
<h1 style="font-size:22pt;margin-bottom:4mm">Dieci domande. Dieci sì.</h1>{chk_h}</div>
<div><span class="eti">Dove sta tutto</span>
<div class="card" style="margin-bottom:3.4mm"><h3>MARCHIO/</h3><p class="xs mut" style="margin:.6mm 0 0">Logo in SVG, PNG, PDF vettoriale e icone dell’app. Quattro versioni, positivo e negativo. Caratteri Archivo e Source Serif.</p></div>
<div class="card" style="margin-bottom:3.4mm"><h3>MARCHIO/LIBRO-DEL-MARCHIO/</h3><p class="xs mut" style="margin:.6mm 0 0">Questo libro in PDF, il sorgente e lo script che lo rigenera.</p></div>
<div class="card" style="margin-bottom:3.4mm"><h3>KIT-CARTOLERIA/</h3><p class="xs mut" style="margin:.6mm 0 0">Carta intestata Italia e Albania, biglietto da visita pronto per la tipografia, firma e-mail da copiare.</p></div>
<div class="box"><h3>Chi decide</h3><p class="sm" style="margin:0">Se una cosa non è in questo libro, o la regola sembra sbagliata per il caso che hai davanti, si chiede a <b>Giorgio Petrelli</b> prima di stampare, pubblicare o mandare. Se la risposta è nuova, entra nel libro.</p></div></div></div>''', zoom=1.17)

# ---- 19. RETRO
pagine.append(f'''<section class="pg dk">
<svg viewBox="0 0 100 100" style="position:absolute;right:-122mm;bottom:-134mm;width:230mm;height:230mm;opacity:.16" aria-hidden="true">{EMBL_NEG}</svg>
<div style="position:absolute;left:0;right:0;top:66mm;text-align:center">{logo('nipec-logo-orizzontale-negativo.svg','width:96mm;margin:0 auto')}</div>
<div style="position:absolute;left:0;right:0;top:112mm;text-align:center;color:#fff">
<div style="font:700 17pt/1.25 Archivo;letter-spacing:-.01em">Non vendiamo macchine.<br><span style="color:#5AA6D6">Costruiamo sistemi di lavoro.</span></div></div>
<div style="position:absolute;left:0;right:0;bottom:14mm;text-align:center;font:500 6.8pt/1.7 Archivo;letter-spacing:.06em;color:#9CCBE8">
NIPEC · Tecnologie Estetiche — PHD System S.r.l. · P.IVA 04696530981 · Via Rovetta 29, 25080 Padenghe sul Garda (BS)<br>
PHD SYSTEM · NIPT M27101203D · Rruga Donika Kastrioti 3, Tiranë</div>
</section>''')

# ------------------------------------------------------------------ assemblaggio e PDF
def pdf(html_path, pdf_path):
    subprocess.run([CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer',
                    f'--print-to-pdf={pdf_path}', '--virtual-time-budget=8000', 'file://' + html_path],
                   check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

CSSF = CSS.replace('@@ARCH@@', ARCH).replace('@@SERIF@@', SERIF)
doc = ('<!doctype html><html lang="it"><head><meta charset="utf-8"><title>NIPEC · Libro del marchio</title>'
       f'<style>{CSSF}</style></head><body>' + '\n'.join(pagine) + '</body></html>')
h = os.path.join(QUI, 'NIPEC-libro-del-marchio.html')
open(h, 'w', encoding='utf8').write(doc)
pdf(h, os.path.join(QUI, 'NIPEC-libro-del-marchio.pdf'))
print('libro:', len(pagine), 'pagine')

# ---- kit cartoleria
def kit_doc(titolo, w, h_, corpo, extra=''):
    return ('<!doctype html><html lang="it"><head><meta charset="utf-8"><title>%s</title><style>'
            '@font-face{font-family:"Archivo";src:url(data:font/woff2;base64,%s) format("woff2");font-weight:100 900}'
            '@font-face{font-family:"Source Serif 4";src:url(data:font/woff2;base64,%s) format("woff2");font-weight:200 900}'
            '*{box-sizing:border-box;margin:0;padding:0}html{-webkit-print-color-adjust:exact;print-color-adjust:exact}'
            '@page{size:%smm %smm;margin:0}body{background:#fff}.p{width:%smm;height:%smm;overflow:hidden;position:relative;break-after:page}.p:last-child{break-after:auto}%s'
            '</style></head><body>%s</body></html>') % (titolo, ARCH, SERIF, w, h_, w, h_, extra, corpo)

for paese, nome in (('it', 'carta-intestata-ITALIA'), ('al', 'carta-intestata-ALBANIA')):
    p = os.path.join(KIT, nome + '.html')
    open(p, 'w', encoding='utf8').write(kit_doc(nome, 210, 297, f'<div class="p">{carta(paese)}</div>'))
    pdf(p, os.path.join(KIT, nome + '.pdf')); os.remove(p)

# biglietto: 91 x 61 con 3 mm di abbondanza, fronte e retro
def con_abbondanza(inner_85x55, fondo):
    return f'<div class="p" style="background:{fondo}"><div style="position:absolute;left:3mm;top:3mm">{inner_85x55}</div></div>'
fr = (f'<div class="p" style="background:#123A63"><div style="position:absolute;left:3mm;top:3mm;width:85mm;height:55mm">'
      f'{biglietto_fronte().replace("width:85mm;height:55mm;background:#123A63;position:relative;overflow:hidden", "width:85mm;height:55mm;position:relative;overflow:hidden")}</div>'
      f'<svg viewBox="0 0 100 100" style="position:absolute;right:-19mm;bottom:-21mm;width:70mm;height:70mm;opacity:.0" aria-hidden="true"></svg></div>')
re_ = (f'<div class="p" style="background:#fff"><div style="position:absolute;left:3mm;top:3mm;width:85mm;height:55mm">'
       f'{biglietto_retro().replace("border:.2mm solid #D4E3EF;box-sizing:border-box", "")}</div></div>')
p = os.path.join(KIT, 'biglietto-da-visita.html')
open(p, 'w', encoding='utf8').write(kit_doc('Biglietto da visita NIPEC', 91, 61, fr + re_))
pdf(p, os.path.join(KIT, 'biglietto-da-visita-tipografia.pdf')); os.remove(p)

# la firma per Gmail vuole pixel, non millimetri: nei programmi di posta mm e pt non si capiscono
FIRMA_PX = (f'<div style="border-top:3px solid #1C6EA4;padding:12px 14px;font-family:Arial,Helvetica,sans-serif;font-size:13px;line-height:1.5;color:#17222E">'
            f'<b style="font-size:15px;color:#123A63">Giorgio Petrelli</b><br>Fondatore · <b style="color:#123A63">NIPEC</b> — Tecnologie Estetiche<br>'
            f'<span style="color:#44535F">WhatsApp +39 351 846 6025 · {MAIL}<br>{WEB}</span><br>'
            f'<span style="color:#44535F;font-size:11px">Non vendiamo macchine. Costruiamo sistemi di lavoro.</span></div>')
open(os.path.join(KIT, 'firma-email.html'), 'w', encoding='utf8').write(
    '<!doctype html><html lang="it"><head><meta charset="utf-8"><title>Firma e-mail NIPEC</title></head>'
    '<body style="font-family:Arial,sans-serif;background:#fff;padding:24px">'
    '<p style="font-size:13px;color:#44535F;max-width:520px">Seleziona la firma qui sotto, copiala, e incollala in Gmail: '
    'Impostazioni → Visualizza tutte le impostazioni → Firma. Cambia nome e ruolo se serve.</p>'
    f'<div style="max-width:430px">{FIRMA_PX}</div></body></html>')
print('kit: ok')
