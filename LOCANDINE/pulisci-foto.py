# -*- coding: utf-8 -*-
"""Toglie il bianco residuo attorno ai macchinari ritagliati male.

   Il punto delicato: le macchine SONO bianche. Quindi non si puo' togliere
   "tutto il bianco", o si buca la macchina. Si parte dai quattro bordi e si
   allaga verso l'interno finche' i pixel restano chiari: cosi' sparisce solo
   lo sfondo attaccato al bordo, e il bianco dentro la scocca resta."""
from PIL import Image
from collections import deque
import sys, os

def ritaglia(entrata, uscita, soglia=232, sfuma=2):
    im = Image.open(entrata).convert('RGBA')
    w, h = im.size
    px = im.load()

    chiaro = lambda p: p[0] >= soglia and p[1] >= soglia and p[2] >= soglia
    visti = bytearray(w * h)
    coda = deque()
    for x in range(w):
        for y in (0, h - 1):
            if not visti[y*w+x] and chiaro(px[x, y]): visti[y*w+x] = 1; coda.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if not visti[y*w+x] and chiaro(px[x, y]): visti[y*w+x] = 1; coda.append((x, y))

    tolti = 0
    while coda:
        x, y = coda.popleft()
        px[x, y] = (px[x, y][0], px[x, y][1], px[x, y][2], 0)
        tolti += 1
        for dx, dy in ((1,0), (-1,0), (0,1), (0,-1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not visti[ny*w+nx] and chiaro(px[nx, ny]):
                visti[ny*w+nx] = 1; coda.append((nx, ny))

    # Secondo passaggio: restano le macchie bianche che il bordo non raggiunge
    # — l'ellisse dietro ad Afrodite, chiusa dall'arco del manipolo, e l'ombra
    # sotto ad Ares. Sono bianco pieno; la scocca delle macchine invece e'
    # sfumata e quasi mai arriva a 248 su tutti e tre i canali. Quindi tolgo
    # solo le isole di bianco PIENO abbastanza grandi da non essere un riflesso.
    pieno = lambda p: p[3] > 0 and p[0] >= 248 and p[1] >= 248 and p[2] >= 248
    segnati = bytearray(w * h)
    isole = 0
    for y0 in range(h):
        for x0 in range(w):
            if segnati[y0*w+x0] or not pieno(px[x0, y0]): continue
            isola = []; c = deque([(x0, y0)]); segnati[y0*w+x0] = 1
            while c:
                x, y = c.popleft(); isola.append((x, y))
                for dx, dy in ((1,0), (-1,0), (0,1), (0,-1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and not segnati[ny*w+nx] and pieno(px[nx, ny]):
                        segnati[ny*w+nx] = 1; c.append((nx, ny))
            if len(isola) >= 1500:
                for x, y in isola: px[x, y] = (px[x, y][0], px[x, y][1], px[x, y][2], 0)
                tolti += len(isola); isole += 1
    if isole: print('   ...e %d macchie di bianco pieno dentro al contorno' % isole)

    # Terzo passaggio: l'ombra morbida della foto originale. Non e' bianca
    # piena, quindi i passaggi di prima non la prendono, ma e' sempre attaccata
    # al vuoto. La limo: un pixel chiaro che tocca il trasparente sparisce.
    # La scocca non si consuma perche' e' circondata dal suo contorno scuro.
    for giro in range(6):
        bordo = []
        for y in range(h):
            for x in range(w):
                p0 = px[x, y]
                if p0[3] == 0 or min(p0[0], p0[1], p0[2]) < 206: continue
                for dx, dy in ((1,0), (-1,0), (0,1), (0,-1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and px[nx, ny][3] == 0:
                        bordo.append((x, y)); break
        if not bordo: break
        for x, y in bordo: px[x, y] = (px[x, y][0], px[x, y][1], px[x, y][2], 0)
        tolti += len(bordo)

    # un filo di sfumatura sul bordo, se no il contorno resta seghettato
    if sfuma:
        alfa = im.getchannel('A')
        from PIL import ImageFilter
        im.putalpha(alfa.filter(ImageFilter.GaussianBlur(sfuma)))

    # ritaglio la cornice vuota: cosi' la foto nella locandina e' tutta macchina
    bbox = im.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
    if bbox: im = im.crop(bbox)

    im.save(uscita)
    print('%-16s %4dx%-4d -> %4dx%-4d  · %d pixel di sfondo tolti'
          % (os.path.basename(uscita), w, h, im.size[0], im.size[1], tolti))
    return im.size

for nome in ('afrodite', 'ares', 'ares2025'):
    ritaglia('foto/%s.png' % nome, 'foto/%s-pulita.png' % nome)
