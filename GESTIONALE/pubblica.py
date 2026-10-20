#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prepara la cartella da caricare su Netlify.

Il sorgente in sorgente/ NON contiene l'indirizzo dello script Google:
al suo posto c'e' __INDIRIZZO_SCRIPT__. L'indirizzo vero sta in .segreto,
che non entra in git perche' questo repository e' pubblico e quell'indirizzo
vale come una chiave.

    python3 pubblica.py

Scrive la cartella pubblica/ pronta da trascinare su Netlify.
"""
import io, os, re, shutil, sys

QUI = os.path.dirname(os.path.abspath(__file__))
SORG, FUORI = os.path.join(QUI, 'sorgente'), os.path.join(QUI, 'pubblica')
SEGRETO = os.path.join(QUI, '.segreto')

if not os.path.exists(SEGRETO):
    sys.exit("Manca .segreto. Mettici dentro l'indirizzo dello script Google,\n"
             "quello che finisce per /exec, e rilancia.")
indirizzo = io.open(SEGRETO, encoding='utf-8').read().strip()
if not re.match(r'^https://script\.google\.com/macros/s/[\w-]+/exec$', indirizzo):
    sys.exit('In .segreto non c\'e\' un indirizzo valido: ' + indirizzo[:60])

shutil.rmtree(FUORI, ignore_errors=True)
os.makedirs(FUORI)
n = 0
for f in sorted(os.listdir(SORG)):
    s, d = os.path.join(SORG, f), os.path.join(FUORI, f)
    if f.endswith(('.html', '.js', '.webmanifest')):
        t = io.open(s, encoding='utf-8').read()
        t = t.replace('__INDIRIZZO_SCRIPT__', indirizzo)
        io.open(d, 'w', encoding='utf-8').write(t)
    else:
        shutil.copy2(s, d)
    n += 1

idx = io.open(os.path.join(FUORI, 'index.html'), encoding='utf-8').read()
sw  = io.open(os.path.join(FUORI, 'sw.js'), encoding='utf-8').read()
assert '__INDIRIZZO_SCRIPT__' not in idx, 'il segnaposto e\' rimasto dentro'
versione = (re.search(r"const C='([^']+)'", sw) or ['', '?'])[1]
print('pubblica/ pronta: %d file · guscio offline %s' % (n, versione))
print('Trascina la CARTELLA pubblica/ su Netlify, poi ricarica l\'app due volte.')
