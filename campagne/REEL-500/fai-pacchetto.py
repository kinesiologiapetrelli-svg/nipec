#!/usr/bin/env python3
"""Il pacchetto da dare al Claude che monta: una cartella sola, tutto dentro, nessun rimando fuori.

Il Claude di Eros lavora in un canale Telegram e non vede il repository: quello che gli serve va con lui.
Prima rifai copioni e documento (fai-copioni.py, fai-documento.py), poi lancia questo.

Uso:  python3 fai-pacchetto.py [percorso.zip]
"""
import os, shutil, sys, tempfile, zipfile

QUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(QUI))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(QUI, 'NIPEC-REEL-pacchetto.zip')
NOME = 'NIPEC-REEL-pacchetto'

GRAFICA_LEGGIMI = """GRAFICA NIPEC — quello che serve per montare i reel
==================================================

LOGO
  nipec-logo-orizzontale-negativo.svg   su fondo scuro o su foto. Quello della scheda finale.
  nipec-logo-orizzontale.svg            su fondo chiaro.
  nipec-emblema-negativo.svg / nipec-emblema.svg   solo il simbolo.
Il logo non si ricolora, non si stira, non si inclina, non prende ombre. Non compare nei primi cinque secondi di un reel.

CARATTERE
  archivo.woff2   Archivo, licenza libera. Titoli e testi a schermo, in grassetto.

COLORI
  Blu profondo  #123A63   fondi scuri, bande sotto le scritte
  Blu NIPEC     #1C6EA4   accenti
  Blu chiaro    #5AA6D6   sul fondo scuro
  Bianco        #FFFFFF   le scritte
Il tricolore (verde, bianco, rosso) vive solo dentro il logo: non si usa altrove.
"""

LEGGI_PRIMA = """# Leggi prima

Sei il Claude che monta i reel di NIPEC. Apri **`FLUSSO-TELEGRAM.md`**: la sezione 0 ti dice chi sei in questa storia, cosa devi fare e in che ordine leggere.

Poi `copioni/00-LEGGIMI.md`, e il copione del reel che stai montando.
"""

with tempfile.TemporaryDirectory() as tmp:
    d = os.path.join(tmp, NOME)
    os.makedirs(os.path.join(d, 'copioni')); os.makedirs(os.path.join(d, 'schede-finali')); os.makedirs(os.path.join(d, 'grafica'))
    shutil.copy(os.path.join(QUI, 'FLUSSO-TELEGRAM.md'), d)
    open(os.path.join(d, '00-LEGGI-PRIMA.md'), 'w', encoding='utf8').write(LEGGI_PRIMA)
    for f in sorted(os.listdir(os.path.join(QUI, 'copioni'))):
        if not f.endswith('.md'): continue
        t = open(os.path.join(QUI, 'copioni', f), encoding='utf8').read()
        t = '\n'.join(r for r in t.split('\n') if '<!--repo-->' not in r)
        open(os.path.join(d, 'copioni', f), 'w', encoding='utf8').write(t)
    for f in sorted(os.listdir(os.path.join(QUI, 'schede-finali'))):
        shutil.copy(os.path.join(QUI, 'schede-finali', f), os.path.join(d, 'schede-finali'))
    shutil.copy(os.path.join(QUI, 'NOVE-REEL-campagna-500-REV3.pdf'), d)
    shutil.copy(os.path.join(REPO, 'campagne/LASER-AFRODITE-500/CAMPAGNA-500-laser-e-afrodite.pdf'), d)
    for f in ('nipec-logo-orizzontale.svg', 'nipec-logo-orizzontale-negativo.svg', 'nipec-emblema.svg', 'nipec-emblema-negativo.svg'):
        shutil.copy(os.path.join(REPO, 'MARCHIO', f), os.path.join(d, 'grafica'))
    shutil.copy(os.path.join(QUI, 'caratteri/archivo.woff2'), os.path.join(d, 'grafica'))
    open(os.path.join(d, 'grafica', 'LEGGIMI.txt'), 'w', encoding='utf8').write(GRAFICA_LEGGIMI)
    if os.path.exists(OUT): os.remove(OUT)
    with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(d):
            for f in sorted(files):
                full = os.path.join(root, f)
                z.write(full, os.path.relpath(full, tmp))
print('pacchetto:', OUT, round(os.path.getsize(OUT) / 1024), 'KB')
