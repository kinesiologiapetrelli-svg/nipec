#!/usr/bin/env python3
"""Il reel «formazione»: NIPEC + DEMETRA, dal workshop del 26 ottobre. 1080 x 1920, 24 secondi.

Regola dei 5 secondi: nessuno stacco oltre 5 secondi (il piu' lungo e' di 3,5), mai due inquadrature uguali di fila.
Il logo non compare nei primi 5 secondi: arriva dopo, nel bollino, e poi nella scheda finale.
L'audio originale e' tolto: non si puo' sapere cosa dice chi parla. Si aggiunge la musica da Instagram.

Foto e video non stanno nel repository (persone e clienti vere): si passano a mano.

Uso:  python3 fai-reel.py <cartella-di-lavoro> <foto-cartella> <ljgg.mp4> <wa-09.59.43.mp4>
         foto-cartella contiene 22.jpg 23.jpg 24.jpg 26.jpg
"""
import os, subprocess, sys

QUI = os.path.dirname(os.path.abspath(__file__))
W = sys.argv[1]
FOTO = sys.argv[2]
LJGG, WA43 = sys.argv[3], sys.argv[4]
OV = os.path.join(W, 'ov'); SEG = os.path.join(W, 'seg')
os.makedirs(SEG, exist_ok=True)

subprocess.run(['node', os.path.join(QUI, 'sovrapposizioni.mjs'), OV], check=True,
               env={**os.environ, 'NODE_PATH': '/opt/node22/lib/node_modules'})

CRF = ['-c:v', 'libx264', '-crf', '12', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-r', '30', '-g', '30', '-an']
SCRITTA = 'format=rgba,fade=t=in:st=0.1:d=0.25:alpha=1'

def esegui(args):
    subprocess.run(['ffmpeg', '-v', 'error', '-y'] + args, check=True)

def video(n, src, ss, dur, taglio=None, tpad=0.0):
    # taglio = (larghezza, altezza, x, y) in frazioni: toglie dal quadro quello che non si vuole mostrare (un volto, troppa pelle)
    pad = f',tpad=stop_mode=clone:stop_duration={tpad}' if tpad else ''
    cr = f'crop=iw*{taglio[0]}:ih*{taglio[1]}:iw*{taglio[2]}:ih*{taglio[3]},' if taglio else ''
    f = (f'[0:v]{cr}scale=1080:1920:flags=lanczos,unsharp=5:5:0.6:5:5:0.0,fps=30,setsar=1{pad},trim=duration={dur},setpts=PTS-STARTPTS,format=yuv420p[v];'
         f'[1:v]{SCRITTA}[o];[v][o]overlay=0:0:format=auto,format=yuv420p[out]')
    esegui(['-ss', str(ss), '-i', src, '-loop', '1', '-t', str(dur), '-i', os.path.join(OV, f't{n}.png'),
            '-filter_complex', f, '-map', '[out]', '-t', str(dur)] + CRF + [os.path.join(SEG, f's{n}.mp4')])

def foto(n, jpg, x0, z0, z1, fx, fy, dur):
    frames = int(dur * 30)
    zp = (f"zoompan=z='{z0}+({z1}-{z0})*on/{frames - 1}':x='(iw-iw/zoom)*{fx}':y='(ih-ih/zoom)*{fy}':d={frames}:s=1080x1920:fps=30")
    f = (f'[0:v]crop=1125:2000:{x0}:0,scale=2160:3840:flags=lanczos,{zp},setsar=1,format=yuv420p[v];'
         f'[1:v]{SCRITTA}[o];[v][o]overlay=0:0:format=auto,format=yuv420p[out]')
    esegui(['-i', os.path.join(FOTO, jpg), '-loop', '1', '-t', str(dur), '-i', os.path.join(OV, f't{n}.png'),
            '-filter_complex', f, '-map', '[out]', '-t', str(dur)] + CRF + [os.path.join(SEG, f's{n}.mp4')])

# (n, inquadratura, durata) — il gancio sono i primi due: 5 secondi
video(1, LJGG, 0.3, 2.5)                                  # dettaglio · la mano sul display
foto(2, '26.jpg', 300, 1.0, 1.15, 0.6, 0.30, 2.5)         # campo largo · la sala, lo schermo con la diretta
foto(3, '23.jpg', 0, 1.0, 1.30, 0.35, 0.30, 3.5)          # mezzo busto · la formatrice con il manipolo
video(4, LJGG, 32.0, 2.5, taglio=(0.86, 0.86, 0.0, 0.02))  # dettaglio · la telecamera in primo piano (tolta la parte bassa)
video(5, LJGG, 22.0, 3.0)                                 # campo largo · lo schermo con la diretta, la sala
foto(6, '24.jpg', 0, 1.2, 1.75, 0.32, 0.28, 2.5)          # dettaglio · le mani, il gel
video(7, WA43, 0.0, 2.0, taglio=(0.86, 0.86, 0.0, 0.04), tpad=0.2)  # campo largo · la sala con il cavalletto (tolto il bordo destro, dove si vede un volto)
foto(8, '22.jpg', 150, 1.0, 1.15, 0.45, 0.30, 2.5)        # mezzo busto · la formatrice alla macchina

esegui(['-loop', '1', '-t', '3', '-i', os.path.join(OV, 'fine.png'), '-vf', 'scale=1080:1920,format=yuv420p'] + CRF
       + [os.path.join(SEG, 's9.mp4')])

lista = os.path.join(W, 'lista.txt')
open(lista, 'w').write(''.join(f"file '{os.path.join(SEG, f's{i}.mp4')}'\n" for i in range(1, 10)))
OUT = os.path.join(W, 'REEL-formazione-NIPEC-DEMETRA.mp4')
esegui(['-f', 'concat', '-safe', '0', '-i', lista, '-loop', '1', '-t', '24', '-i', os.path.join(OV, 'bollino.png'),
        '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo',
        '-filter_complex',
        "[1:v]format=rgba,fade=t=in:st=5:d=0.3:alpha=1,fade=t=out:st=20.7:d=0.3:alpha=1[b];"
        "[0:v][b]overlay=0:0:enable='between(t,5,21)':format=auto,format=yuv420p[v]",
        '-map', '[v]', '-map', '2:a', '-t', '24', '-c:v', 'libx264', '-crf', '20', '-preset', 'slow', '-profile:v', 'high',
        '-pix_fmt', 'yuv420p', '-r', '30', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', OUT])
print(OUT)
