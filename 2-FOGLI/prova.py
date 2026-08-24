# -*- coding: utf-8 -*-
"""Riproduce in Python la catena di COSA FARE OGGI per verificarla su casi reali."""
from datetime import date, timedelta

SEDUTE_CICLO, RIENTRO_MIN, RIENTRO_MAX = 12, 21, 28
CONFERMA, MANTENIMENTO, DORMIENTE_MESI = 7, 90, 6
AVVISI = ["CONFERMA DOMANI","CHIAMA PER CONFERMA","APPUNTAMENTO SALTATO",
          "PRENDI APPUNTAMENTO","FUORI FINESTRA","ULTIMA SEDUTA",
          "RICHIAMO MANTENIMENTO","RECUPERA CON INCENTIVO"]
OGGI = date(2026, 8, 24)

def edate(d, mesi):
    m = d.month - 1 + mesi
    y = d.year + m // 12
    return date(y, m % 12 + 1, min(d.day, [31,29 if y%4==0 and (y%100!=0 or y%400==0) else 28,
                                           31,30,31,30,31,31,30,31,30,31][m % 12]))

def cosa_fare(nome, pross, sed, st, ult, oggi=OGGI):
    if not nome: return ""
    attesa = pross is not None and pross >= oggi
    if pross is not None and pross < oggi and (ult is None or ult < pross): a = "APPUNTAMENTO SALTATO"
    elif attesa and (pross-oggi).days == 1: a = "CONFERMA DOMANI"
    elif attesa and (pross-oggi).days == CONFERMA: a = "CHIAMA PER CONFERMA"
    elif attesa: a = ""
    elif st == "Sospesa": a = ""
    elif st == "Persa": a = "RECUPERA CON INCENTIVO"
    elif ult is not None and oggi >= edate(ult, DORMIENTE_MESI): a = "RECUPERA CON INCENTIVO"
    elif st == "Mantenimento":
        a = "RICHIAMO MANTENIMENTO" if (ult is not None and (oggi-ult).days >= MANTENIMENTO) else ""
    elif st == "In ciclo":
        if sed >= SEDUTE_CICLO: a = "ULTIMA SEDUTA"
        elif ult is not None and (oggi-ult).days > RIENTRO_MAX: a = "FUORI FINESTRA"
        else: a = "PRENDI APPUNTAMENTO"
    elif st == "Da contattare": a = "PRENDI APPUNTAMENTO"
    else: a = ""
    return "" if not a else "%d · %s" % (AVVISI.index(a)+1, a)

g = lambda n: OGGI - timedelta(days=n)   # n giorni fa
f = lambda n: OGGI + timedelta(days=n)   # fra n giorni

casi = [
 ("riga vuota",            ("", None, 0, "", None),                    ""),
 ("appuntamento domani",   ("Anna", f(1), 4, "In ciclo", g(24)),       "1 · CONFERMA DOMANI"),
 ("appuntamento a 7 gg",   ("Bea", f(7), 5, "In ciclo", g(18)),        "2 · CHIAMA PER CONFERMA"),
 ("appuntamento a 10 gg",  ("Cira", f(10), 5, "In ciclo", g(15)),      ""),
 ("oggi in centro",        ("Dora", OGGI, 5, "In ciclo", g(25)),       ""),
 ("saltato ieri",          ("Ely", g(1), 6, "In ciclo", g(29)),        "3 · APPUNTAMENTO SALTATO"),
 ("venuta, non riprenota", ("Fana", g(3), 7, "In ciclo", g(3)),        "4 · PRENDI APPUNTAMENTO"),
 ("uscita senza prossimo", ("Gina", None, 7, "In ciclo", g(2)),        "4 · PRENDI APPUNTAMENTO"),
 ("ferma da 35 gg",        ("Ines", None, 7, "In ciclo", g(35)),       "5 · FUORI FINESTRA"),
 ("ciclo finito 12/12",    ("Lia", None, 12, "In ciclo", g(10)),       "6 · ULTIMA SEDUTA"),
 ("mantenimento 60 gg",    ("Mara", None, 12, "Mantenimento", g(60)),  ""),
 ("mantenimento 95 gg",    ("Nina", None, 12, "Mantenimento", g(95)),  "7 · RICHIAMO MANTENIMENTO"),
 ("mantenimento 200 gg",   ("Ola", None, 12, "Mantenimento", g(200)),  "8 · RECUPERA CON INCENTIVO"),
 ("persa",                 ("Pia", None, 3, "Persa", g(120)),          "8 · RECUPERA CON INCENTIVO"),
 ("persa riprenotata",     ("Rita", f(1), 3, "Persa", g(200)),         "1 · CONFERMA DOMANI"),
 ("dormiente 7 mesi",      ("Sara", None, 6, "In ciclo", g(215)),      "8 · RECUPERA CON INCENTIVO"),
 ("sospesa (gravidanza)",  ("Tea", None, 5, "Sospesa", g(150)),        ""),
 ("nuova mai vista",       ("Ute", None, 0, "Da contattare", None),    "4 · PRENDI APPUNTAMENTO"),
 ("nuova gia prenotata",   ("Vera", f(3), 0, "Da contattare", None),   ""),
]

ok = True
for etichetta, args, atteso in casi:
    r = cosa_fare(*args)
    stato = "ok " if r == atteso else "NO "
    if r != atteso: ok = False
    print("%s %-24s -> %-28s %s" % (stato, etichetta, r or "(vuoto)",
                                    "" if r == atteso else "atteso: " + (atteso or "(vuoto)")))
print("\nTutti i casi passano." if ok else "\nCI SONO CASI ROTTI.")
