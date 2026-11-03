#!/usr/bin/env python3
"""I suoni dei reel SBAM, scritti da zero: nessun brano o campione di altri, nessun diritto da pagare.

  sbam.wav          il colpo pieno (0,9 s): per il colpo vero del reel quando non c'e' un suono vero abbastanza forte
  sbam-leggero.wav  il colpo piccolo (0,5 s): per i colpi «leggeri» (secondo SBAM di P4 e P6)
  colpo.wav         un colpo secco e breve (0,3 s): per le serie a ritmo (F2 x4, L6 x3, F5 x10); ogni volta un po' diverso se si passa un seme
  tic.wav           un tic d'orologio (0,15 s): per il conto alla rovescia di P2
  battito.wav       un battito basso (1,0 s: «lub-dub»): per l'apertura di P2

Dove c'e' un suono vero (portellone, palmo sul tavolo, timbro, strappo, notifica, bip del dispositivo) si usa quello. Questi servono quando
il suono vero non si sente bene, o per rinforzarlo.

Uso:  python3 fai-suoni.py <cartella-di-uscita>
"""
import os, sys, wave
import numpy as np

SR = 44100
rng = np.random.default_rng(11)

def t_(d): return np.arange(int(SR * d)) / SR

def spegni(x, d=0.01):
    n = int(SR * d); x[-n:] *= np.linspace(1, 0, n); return x

def passa_alto(x, k=1):
    for _ in range(k): x = np.diff(x, prepend=0)
    return x

def passa_basso(x, a):
    y = np.zeros_like(x); s = 0.0
    for i, v in enumerate(x):
        s += a * (v - s); y[i] = s
    return y

def riverbero(x, coda, forza):
    ir_t = t_(coda); ir = rng.standard_normal(len(ir_t)) * np.exp(-ir_t * (4.0 / coda)); ir /= np.sqrt((ir ** 2).sum())
    n = len(x) + len(ir)
    wet = np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(ir, n), n)[:len(x)]
    return x + wet * forza

def colpo_pieno(dur=0.9, profondita=1.0, rumore=1.0, coda=0.6, seme=None):
    g = np.random.default_rng(seme) if seme is not None else rng
    t = t_(dur)
    f = 38 + (120 - 38) * np.exp(-t * 22)                                   # il tonfo scende da 120 a 38 Hz
    tonfo = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9) * profondita
    f2 = 70 + (190 - 70) * np.exp(-t * 35)
    corpo = np.sin(2 * np.pi * np.cumsum(f2) / SR) * np.exp(-t * 16) * 0.55
    crack = passa_alto(g.standard_normal(len(t)), 2) * np.exp(-t * 140) * 0.35 * rumore   # lo schiocco
    sordo = passa_basso(g.standard_normal(len(t)), 0.08) * np.exp(-t * 11) * 0.9 * rumore   # il rumore sordo del colpo
    f3 = 160 + (520 - 160) * np.exp(-t * 55)                                 # il «toc» che si sente anche dall'altoparlante di un telefono
    toc = np.sin(2 * np.pi * np.cumsum(f3) / SR) * np.exp(-t * 32) * 1.5
    medio = passa_basso(passa_alto(g.standard_normal(len(t)), 1), 0.45) * np.exp(-t * 38) * 2.2 * rumore   # rumore tra 500 Hz e 4 kHz
    x = tonfo + corpo + crack + sordo + toc + medio
    x[:int(SR * 0.002)] *= np.linspace(0, 1, int(SR * 0.002))                # attacco di 2 ms: niente click
    return spegni(riverbero(x, coda, 0.35), 0.05)

def scrivi(nome, x, picco):
    x = x / np.abs(x).max() * picco
    pcm = (np.clip(np.stack([x, x]).T, -1, 1) * 32767).astype('<i2')
    with wave.open(nome, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    print(nome, f'{len(x) / SR:.2f} s')

out = sys.argv[1]; os.makedirs(out, exist_ok=True)
scrivi(os.path.join(out, 'sbam.wav'), colpo_pieno(0.9, 1.0, 1.0, 0.6, seme=3), 0.89)
scrivi(os.path.join(out, 'sbam-leggero.wav'), colpo_pieno(0.5, 0.35, 0.8, 0.3, seme=5), 0.6)
scrivi(os.path.join(out, 'colpo.wav'), colpo_pieno(0.3, 0.8, 1.1, 0.15, seme=7), 0.79)

t = t_(0.15)
tic = np.sin(2 * np.pi * 2300 * t) * np.exp(-t * 110) + passa_alto(rng.standard_normal(len(t)), 1) * np.exp(-t * 300) * 0.4
tic[:int(SR * 0.0008)] *= np.linspace(0, 1, int(SR * 0.0008))
scrivi(os.path.join(out, 'tic.wav'), tic, 0.5)

t = t_(1.0); b = np.zeros(len(t))
for inizio, forza in ((0.0, 1.0), (0.28, 0.7)):                           # lub-dub
    i = int(SR * inizio); tt = t_(0.45)
    f = 45 + (85 - 45) * np.exp(-tt * 28)
    base = np.sin(2 * np.pi * np.cumsum(f) / SR)
    arm = np.sin(2 * np.pi * np.cumsum(f * 3.2) / SR) * 0.55 + np.sin(2 * np.pi * np.cumsum(f * 5.5) / SR) * 0.25   # armoniche, per l'altoparlante di un telefono
    pulso = (base + arm) * np.exp(-tt * 13) * forza
    pulso[:int(SR * 0.004)] *= np.linspace(0, 1, int(SR * 0.004))
    b[i:i + len(pulso)] += pulso[:len(b) - i]
scrivi(os.path.join(out, 'battito.wav'), riverbero(b, 0.3, 0.2), 0.7)
