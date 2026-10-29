#!/usr/bin/env python3
"""La base musicale del reel «formazione»: 24 secondi, 120 BPM, la minore. Generata da zero, nessun brano di altri: libera da diritti.

Un pad morbido, un arpeggio leggero, un basso, un battito appena accennato dal secondo 2,
e un ultimo accordo che si spegne con la scheda finale. Pensata come sottofondo: piano, senza voce.

Uso:  python3 musica.py <musica.wav> [durata-in-secondi, di solito 24]
"""
import sys, wave
import numpy as np

SR = 44100
DUR = float(sys.argv[2]) if len(sys.argv) > 2 else 24.0
BPM = 120
BEAT = 60 / BPM                       # 0,5 s
BAR = 4 * BEAT                        # 2 s
N = int(SR * DUR)
t_all = np.arange(N) / SR

def hz(m): return 440.0 * 2 ** ((m - 69) / 12)

# Am - F - C - G, tre giri = 12 battute = 24 s
ACCORDI = [(45, (57, 60, 64)), (41, (53, 57, 60)), (48, (55, 60, 64)), (43, (50, 55, 59))]
NB = int(np.ceil(DUR / BAR))

def aggiungi(buf, inizio, seg, pan=0.0):
    i = int(inizio * SR); j = min(N, i + len(seg))
    if i >= N or j <= i: return
    s = seg[:j - i]
    buf[0, i:j] += s * (1 - max(pan, 0)); buf[1, i:j] += s * (1 + min(pan, 0))

def pad(note, dur):
    t = np.arange(int(SR * dur)) / SR
    f = hz(note); y = np.zeros_like(t)
    for det in (-0.004, 0.0, 0.004):
        for k, a in ((1, 1.0), (2, 0.35), (3, 0.12)):
            y += a * np.sin(2 * np.pi * f * (1 + det) * k * t)
    env = np.minimum(1, t / 0.5) * np.minimum(1, (dur - t) / 0.6)
    return y * env * 0.05

def pluck(note, dur=0.9):
    t = np.arange(int(SR * dur)) / SR; f = hz(note)
    y = np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 9) + 0.15 * np.sin(2 * np.pi * 3 * f * t) * np.exp(-t * 14)
    return y * np.exp(-t * 5.5) * np.minimum(1, t / 0.004) * 0.17

def basso(note, dur):
    t = np.arange(int(SR * dur)) / SR; f = hz(note)
    y = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2 * f * t)
    return y * np.minimum(1, t / 0.02) * np.minimum(1, (dur - t) / 0.15) * 0.22

def cassa():
    t = np.arange(int(SR * 0.3)) / SR
    fase = 2 * np.pi * (45 * t + (120 - 45) * (1 - np.exp(-t * 28)) / 28)
    return np.sin(fase) * np.exp(-t * 11) * 0.38

def charleston(rng):
    t = np.arange(int(SR * 0.06)) / SR
    r = rng.standard_normal(len(t)); r = np.diff(r, prepend=0)
    return r * np.exp(-t * 90) * 0.035

rng = np.random.default_rng(7)
mus = np.zeros((2, N)); ritmo = np.zeros((2, N))
for b in range(NB):
    radice, tri = ACCORDI[b % 4]; t0 = b * BAR
    for nota in tri: aggiungi(mus, t0, pad(nota, BAR + 0.5), pan=0.0)
    aggiungi(ritmo, t0, basso(radice, BAR - 0.05))
    # arpeggio a ottavi: radice, terza, quinta, ottava, quinta, terza, radice, quinta
    arp = [tri[0], tri[1], tri[2], tri[0] + 12, tri[2], tri[1], tri[0], tri[2]]
    for k, nota in enumerate(arp):
        if b == 0 and k < 2: continue
        aggiungi(mus, t0 + k * BEAT / 2, pluck(nota + (12 if b % 4 == 3 and k == 3 else 0)), pan=-0.25 if k % 2 else 0.25)
    if b >= 1 and b < NB - 1:
        for k in (0, 2):  aggiungi(ritmo, t0 + k * BEAT, cassa())
        for k in range(8): aggiungi(ritmo, t0 + k * BEAT / 2 + BEAT / 4 * (k % 2 == 1) * 0, charleston(rng) * (1.0 if k % 2 else 0.4))

# riverbero: coda di rumore che decade, solo su pad e arpeggio
ir_t = np.arange(int(SR * 1.4)) / SR
ir = rng.standard_normal(len(ir_t)) * np.exp(-ir_t * 3.2); ir /= np.sqrt((ir ** 2).sum())
def riverbero(x):
    n = N + len(ir)
    return np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(ir, n), n)[:N]
mus_r = np.stack([riverbero(mus[0]), riverbero(mus[1])])
out = mus * 0.8 + mus_r * 0.45 + ritmo

# entra piano, si chiude con la scheda finale
fade_in = np.minimum(1, t_all / 0.8)
fade_out = np.minimum(1, (DUR - t_all) / 2.0) ** 1.5
out *= fade_in * fade_out
picco = np.abs(out).max()
out = out / picco * 0.55
pcm = (np.clip(out, -1, 1).T * 32767).astype('<i2')
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print(sys.argv[1])
