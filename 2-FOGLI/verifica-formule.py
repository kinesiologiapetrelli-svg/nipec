# -*- coding: utf-8 -*-
"""Prende le formule esatte che finiscono nel foglio (versione con la virgola,
quella del file .xlsx) e le calcola sui 19 casi. Verifica la trascrizione,
non il ragionamento: quello e' gia' provato altrove."""
import sys, os, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import valuta
from valuta import Foglio, calcola, VUOTO
from formule import perExcel
import prova

OGGI = valuta.OGGI
g = lambda n: OGGI - datetime.timedelta(days=n)
f = lambda n: OGGI + datetime.timedelta(days=n)

AVVISI = ["CONFERMA DOMANI", "CHIAMA PER CONFERMA", "APPUNTAMENTO SALTATO", "PRENDI APPUNTAMENTO",
          "FUORI FINESTRA", "ULTIMA SEDUTA", "RICHIAMO MANTENIMENTO", "RECUPERA CON INCENTIVO"]

base = {"IMPOSTAZIONI!C5": 12.0, "IMPOSTAZIONI!C6": 21.0, "IMPOSTAZIONI!C7": 28.0,
        "IMPOSTAZIONI!C8": 7.0, "IMPOSTAZIONI!C9": 90.0, "IMPOSTAZIONI!C10": 6.0,
        "INCENTIVI!C5": "Offerta Laser 1", "INCENTIVI!C6": "Offerta Laser 2", "INCENTIVI!C7": "Offerta Laser 3"}
for i, a in enumerate(AVVISI):
    base["IMPOSTAZIONI!F%d" % (5 + i)] = a

# i casi di prova diventano righe vere del foglio
celle = dict(base)
attesi, etichette = [], []
riga = 5
for etichetta, (nome, pross, sed, st, ult), atteso in prova.casi:
    if not nome: continue
    celle["CLIENTI!A%d" % riga] = nome
    if pross: celle["CLIENTI!C%d" % riga] = pross
    celle["CLIENTI!D%d" % riga] = float(sed)
    celle["CLIENTI!E%d" % riga] = st
    if ult: celle["CLIENTI!I%d" % riga] = ult
    celle["CLIENTI!N%d" % riga] = 50.0
    celle["CLIENTI!Q%d" % riga] = OGGI
    attesi.append(atteso); etichette.append(etichetta); riga += 1
ultima = riga - 1

fg = Foglio(celle)

def metti(chiave, col, righe):
    """Calcola la formula riga per riga e scrive il risultato nel foglio,
    come farebbe il foglio vero."""
    for r in righe:
        formula = perExcel(chiave)
        for c in "ABCDEFGHIJKLMNOPQRST":
            formula = formula.replace("$%s5" % c, "$%s%d" % (c, r))
        celle["CLIENTI!%s%d" % (col, r)] = calcola(formula, fg, r)

righe = range(5, ultima + 1)
for chiave, col in (("S5", "S"), ("O5", "O"), ("B5", "B"), ("F5", "F"), ("J5", "J"),
                    ("K5", "K"), ("L5", "L"), ("M5", "M"), ("P5", "P"), ("T5", "T")):
    metti(chiave, col, righe)

buoni = 0
print("LA COLONNA B, CALCOLATA DALLA FORMULA VERA\n")
for i, atteso in enumerate(attesi):
    r = 5 + i
    letto = celle["CLIENTI!B%d" % r]
    ok = letto == atteso
    buoni += ok
    print("%s %-24s -> %-28s %s" % ("ok " if ok else "NO ", etichette[i], letto or "(vuoto)",
                                    "" if ok else "atteso: " + (atteso or "(vuoto)")))
print("\n%d/%d" % (buoni, len(attesi)))

print("\nLE ALTRE COLONNE, SU TRE RIGHE")
for r in (5, 6, 12):
    print("  riga %d  %-12s sedute %-6s offerta %-16s lasciati %-6s da fare %-6s ordine %s"
          % (r, celle["CLIENTI!A%d" % r], celle["CLIENTI!L%d" % r], celle["CLIENTI!M%d" % r] or "—",
             celle["CLIENTI!O%d" % r], celle["CLIENTI!P%d" % r], celle["CLIENTI!T%d" % r] or "—"))
print("  promemoria riga 5:", repr(celle["CLIENTI!F5"]))

print("\nIL RIEPILOGO")
fg.corrente = "RIEPILOGO"
for chiave, nome in (("R_C5", "da richiamare"), ("R_C7", "copertura"), ("R_C8", "dormienti"),
                     ("R_C13", "in ciclo"), ("R_C17", "persone"), ("R_C20", "nuove 30 gg"),
                     ("R_F5", "da incassare"), ("R_F6", "gia' lasciati"), ("R_F7", "media")):
    v = calcola(perExcel(chiave), fg, 5)
    print("  %-16s %s" % (nome, round(v, 2) if isinstance(v, float) else v))

print("\nIL FOGLIO OGGI, PESCATO DALLA CHIAVE")
fg.corrente = "OGGI"
for i in range(12):
    r = 5 + i
    k = calcola(perExcel("O_G5").replace("$G5", "$G%d" % r), fg, r)
    celle["OGGI!G%d" % r] = k
    if k == "" or k is valuta.ERR: break
    fa = perExcel("O_A5").replace("$G5", "$G%d" % r)
    nome = calcola(fa, fg, r)
    avviso = calcola(fa.replace("CLIENTI!A$5:A$304", "CLIENTI!B$5:B$304"), fg, r)
    print("  %-14s %s" % (nome, avviso))

print("\nI COLORI")
fg.corrente = "CLIENTI"
for chiave in ("FC_ROSSO", "FC_GIALLO", "FC_VERDE"):
    acceso = [celle["CLIENTI!A%d" % r] for r in righe if calcola(perExcel(chiave).replace("$B5", "$B%d" % r), fg, r) is True]
    print("  %-10s %s" % (chiave.replace("FC_", "").lower(), ", ".join(acceso) or "nessuna"))

sys.exit(0 if buoni == len(attesi) else 1)
