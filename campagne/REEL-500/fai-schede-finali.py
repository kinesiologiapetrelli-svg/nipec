#!/usr/bin/env python3
"""Le tre schede finali dei reel: 1080 x 1920 PNG, due secondi in coda al video.

Stile dal libro del marchio (MARCHIO/LIBRO-DEL-MARCHIO): fondo blu profondo,
parola chiave in bianco grande, logo negativo, sito. Zone sicure di Instagram:
i primi 250 px e gli ultimi 340 px sono coperti dall'interfaccia, quindi
tutto il contenuto sta in mezzo.

Uso:  python3 fai-schede-finali.py
"""
import base64, os, re, subprocess, tempfile

QUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(QUI))
CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
OUT = os.path.join(QUI, 'schede-finali')
os.makedirs(OUT, exist_ok=True)

arch = base64.b64encode(open(os.path.join(QUI, 'caratteri/archivo.woff2'), 'rb').read()).decode()

def svg(nome):
    s = open(os.path.join(REPO, 'MARCHIO', nome), encoding='utf8').read()
    return re.sub(r'<title>.*?</title>', '', s, flags=re.S)

LOGO = svg('nipec-logo-orizzontale-negativo.svg').replace('<svg ', '<svg style="width:600px;display:block" ', 1)
EMBL = re.sub(r'^<svg[^>]*>|</svg>\s*$', '', svg('nipec-emblema-negativo.svg').strip()).strip()

CARTE = [
    # file, invito, parola, corpo parola in px, riga prezzo, contatto
    ('LASER-italia', 'Scrivimi', 'LASER', 262, '500 € al mese · nessun vincolo', 'WhatsApp 351 846 6025'),
    ('LASER-albania', 'Shkruaj', 'LASER', 262, '50.000 lekë / muaj · pa kontratë', '+355 69 212 9786'),
    ('AFRODITE-albania', 'Shkruaj', 'AFRODITE', 170, '50.000 lekë / muaj · pa kontratë', '+355 69 212 9786'),
]

HTML = '''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:"Archivo";src:url(data:font/woff2;base64,%(arch)s) format("woff2");font-weight:100 900}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;background:#123A63;overflow:hidden}
body{position:relative;font-family:"Archivo","Helvetica Neue",Arial,sans-serif;color:#fff}
.em{position:absolute;right:-470px;bottom:-430px;width:1100px;height:1100px;opacity:.13}
.blocco{position:absolute;left:0;right:0;top:250px;bottom:340px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}
.inv{font-weight:600;font-size:50px;letter-spacing:.2em;text-transform:uppercase;color:#5AA6D6;margin-bottom:26px}
.par{font-weight:800;font-size:%(px)spx;line-height:.95;letter-spacing:-.025em;color:#fff}
.pre{margin-top:58px;font-weight:600;font-size:48px;letter-spacing:.01em;color:#D5E3F0}
.fi{margin-top:92px;margin-bottom:92px;width:140px;height:5px;background:#5AA6D6;border-radius:3px}
.logo{margin-bottom:34px}
.sito{font-weight:600;font-size:40px;letter-spacing:.06em;color:#9CCBE8}
.con{margin-top:12px;font-weight:500;font-size:38px;letter-spacing:.04em;color:#9CCBE8}
</style></head><body>
<svg class="em" viewBox="0 0 100 100" aria-hidden="true">%(embl)s</svg>
<div class="blocco">
<div class="inv">%(inv)s</div>
<div class="par">%(par)s</div>
<div class="pre">%(pre)s</div>
<div class="fi"></div>
<div class="logo">%(logo)s</div>
<div class="sito">www.nipecestetica.eu</div>
<div class="con">%(con)s</div>
</div></body></html>'''

with tempfile.TemporaryDirectory() as tmp:
    for nome, inv, par, px, pre, con in CARTE:
        h = os.path.join(tmp, nome + '.html')
        open(h, 'w', encoding='utf8').write(HTML % dict(arch=arch, px=px, embl=EMBL, inv=inv, par=par, pre=pre, logo=LOGO, con=con))
        subprocess.run([CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars',
                        '--window-size=1080,1920', '--virtual-time-budget=4000',
                        f'--screenshot={os.path.join(OUT, "scheda-finale-" + nome + ".png")}', 'file://' + h],
                       check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
print('schede finali:', sorted(os.listdir(OUT)))
