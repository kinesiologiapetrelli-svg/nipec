#!/usr/bin/env python3
"""Rigenera llms-full.txt dal contenuto reale delle pagine."""
#
# Si lancia dalla cartella SITO/pubblica/ ogni volta che cambia il testo
# delle pagine:   python3 ../strumenti/rigenera-llms-full.py
import re, html, os, datetime
S="https://nipecestetica.eu"
PAG=[("index.html","Home — chi siamo e cosa facciamo"),
 ("noleggio.html","Noleggio operativo: canone, Full Kasko, cosa e' incluso e cosa no"),
 ("laser-ares.html","Laser Ares, diodo 808 nm"),
 ("laser-uriel.html","Laser Uriel, diodo tri-onda 755/808/1064 nm"),
 ("afrodite.html","Afrodite VS++, sistema multifunzione corpo e viso"),
 ("borea-cryo.html","Borea e Cryo 360°, criolipolisi ed elettrostimolazione"),
 ("q-switch.html","Laser Q-Switch, divisione medicale"),
 ("formazione.html","Formazione e certificazione operatore"),
 ("metodo.html","Il metodo NIPEC in quattro fasi"),
 ("chi-siamo.html","Chi siamo"),("contatti.html","Contatti e consulenza gratuita"),
 ("privacy.html","Informativa privacy e cookie")]

def testo(p):
    s=open(p,encoding="utf-8").read()
    m=re.search(r"<main.*?</main>", s, re.S)
    if not m: return ""
    b=re.sub(r"<script.*?</script>","",m.group(0),flags=re.S)
    b=re.sub(r"<style.*?</style>","",b,flags=re.S)
    b=re.sub(r"<h1[^>]*>(.*?)</h1>", lambda x:"\n\n# "+x.group(1)+"\n", b, flags=re.S)
    b=re.sub(r"<h2[^>]*>(.*?)</h2>", lambda x:"\n\n## "+x.group(1)+"\n", b, flags=re.S)
    b=re.sub(r"<summary[^>]*>(.*?)</summary>", lambda x:"\n\nD: "+x.group(1)+"\nR:", b, flags=re.S)
    b=re.sub(r"</(p|div|li|span|section|details)>", "\n", b)
    b=re.sub(r"<[^>]+>", " ", b)
    b=html.unescape(b)
    out=[]
    for r in (re.sub(r"[ \t]+"," ",x).strip() for x in b.split("\n")):
        if not r: continue
        if out and out[-1]==r: continue
        if out and out[-1]=="R:": out[-1]="R: "+r; continue
        if out and out[-1]=="D:": out[-1]="D: "+r; continue
        out.append(r)
    return "\n".join(out)

F=["# NIPEC — tecnologie estetiche professionali",
   "# Testo completo del sito nipecestetica.eu",
   "# PHD System S.r.l. — P.IVA 04696530981",
   f"# Aggiornato: {datetime.date.today().isoformat()}",""]
for f,d in PAG:
    if not os.path.exists(f): continue
    F+=["", "="*70, f"URL: {S}/{'' if f=='index.html' else f}", f"PAGINA: {d}", "="*70, "", testo(f)]
open("llms-full.txt","w",encoding="utf-8").write("\n".join(F)+"\n")
t=open("llms-full.txt",encoding="utf-8").read()
print(f"llms-full.txt: {len(t.split())} parole, {t.count(chr(10)+'D: ')} domande incluse")
