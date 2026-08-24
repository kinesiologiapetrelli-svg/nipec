# -*- coding: utf-8 -*-
"""Sorgente unica delle formule del Cruscotto Clienti - laser.
Ogni formula e' scritta una volta sola, con i segnaposto {NOME}.
Da qui escono: la pagina ALERT LASER (varianti celle / nomi, separatore ;)
e il file .xlsx vero (stesse formule, separatore , come vuole il formato).

Vincolo che comanda tutto: niente LET, niente IFS, niente FILTER/SORT.
Solo funzioni che esistono ovunque - Google Fogli, Excel e LibreOffice -
cosi' il foglio si puo' verificare davvero prima di consegnarlo."""

CELLE = {
    "SEDUTE_CICLO":   "IMPOSTAZIONI!$C$5",
    "RIENTRO_MIN":    "IMPOSTAZIONI!$C$6",
    "RIENTRO_MAX":    "IMPOSTAZIONI!$C$7",
    "CONFERMA":       "IMPOSTAZIONI!$C$8",
    "MANTENIMENTO":   "IMPOSTAZIONI!$C$9",
    "DORMIENTE_MESI": "IMPOSTAZIONI!$C$10",
    "AVVISI":         "IMPOSTAZIONI!$F$5:$F$12",
}
NOMI = {k: k for k in CELLE}

F = {}

# ---------------------------------------------------------------- il motore
# Undici domande in fila: la prima che risponde vince. Sta in una colonna
# di servizio perche' cosi' la formula si legge, e la B la mette in ordine.
F["S5"] = (
 '=IF($A5="";"";'
 'IF(AND($C5<>"";$C5<TODAY();OR($I5="";$I5<$C5));"APPUNTAMENTO SALTATO";'
 'IF(AND($C5<>"";$C5-TODAY()=1);"CONFERMA DOMANI";'
 'IF(AND($C5<>"";$C5-TODAY()={CONFERMA});"CHIAMA PER CONFERMA";'
 'IF(AND($C5<>"";$C5>=TODAY());"";'
 'IF($E5="Sospesa";"";'
 'IF($E5="Persa";"RECUPERA CON INCENTIVO";'
 'IF(AND($I5<>"";TODAY()>=EDATE($I5;{DORMIENTE_MESI}));"RECUPERA CON INCENTIVO";'
 'IF($E5="Mantenimento";IF(AND($I5<>"";TODAY()-$I5>={MANTENIMENTO});"RICHIAMO MANTENIMENTO";"");'
 'IF($E5="In ciclo";'
   'IF(N($D5)>={SEDUTE_CICLO};"ULTIMA SEDUTA";'
   'IF(AND($I5<>"";TODAY()-$I5>{RIENTRO_MAX});"FUORI FINESTRA";"PRENDI APPUNTAMENTO"));'
 'IF($E5="Da contattare";"PRENDI APPUNTAMENTO";"")))))))))))'
)

F["B5"] = '=IF($S5="";"";IFERROR(MATCH($S5;{AVVISI};0);9)&" · "&$S5)'

# ---------------------------------------------------------- il contorno (F)
_PEZZI = (
 'IF(AND($C5<>"";$C5=TODAY());" · oggi in centro";"")'
 '&IF(AND($C5<>"";$C5>=TODAY();N($D5)+1>={SEDUTE_CICLO});" · ultima del ciclo, proponi il mantenimento";"")'
 '&IF(AND($C5<>"";$C5>=TODAY();$I5<>"";$C5-$I5<{RIENTRO_MIN});" · rientro anticipato, meno di "&{RIENTRO_MIN}&" giorni";"")'
 '&IF(AND($C5<>"";$C5>=TODAY();$I5<>"";$C5-$I5>{RIENTRO_MAX});" · rientro oltre "&{RIENTRO_MAX}&" giorni";"")'
)
F["F5"] = '=IF($A5="";"";IF(LEN(' + _PEZZI + ')=0;"";MID(' + _PEZZI + ';4;300)))'

# ------------------------------------------------------- le altre calcolate
F["J5"] = '=IF($I5="";"";TODAY()-$I5)'
F["K5"] = '=IF($C5="";"";$C5-TODAY())'
F["L5"] = '=IF($A5="";"";N($D5)&"/"&{SEDUTE_CICLO})'
F["M5"] = (
 '=IF($S5="";"";'
 'IF($S5="RECUPERA CON INCENTIVO";INCENTIVI!$C$7;'
 'IF($S5="RICHIAMO MANTENIMENTO";INCENTIVI!$C$6;'
 'IF(OR($S5="FUORI FINESTRA";$S5="ULTIMA SEDUTA");INCENTIVI!$C$5;""))))'
)
F["O5"] = '=IF($A5="";"";N($D5)*N($N5))'
F["P5"] = '=IF($A5="";"";MAX(0;({SEDUTE_CICLO}-N($D5))*N($N5)))'

# chiave d'ordine: prima l'avviso, poi chi ha lasciato piu' soldi, poi la riga
F["T5"] = (
 '=IF($S5="";"";IFERROR(MATCH($S5;{AVVISI};0);9)*100000000'
 '+(9999-MIN(9999;ROUND(N($O5)/100;0)))*10000+ROW())'
)

# ------------------------------------------------------------- il RIEPILOGO
F["R_C5"]  = '=COUNTIF(CLIENTI!$S$5:$S$304;"?*")'
F["R_C7"]  = '=IFERROR(COUNTIFS(CLIENTI!$E$5:$E$304;"In ciclo";CLIENTI!$C$5:$C$304;">="&TODAY())/COUNTIF(CLIENTI!$E$5:$E$304;"In ciclo");"")'
F["R_C8"]  = '=SUMPRODUCT((CLIENTI!$A$5:$A$304<>"")*(CLIENTI!$I$5:$I$304<>"")*(CLIENTI!$I$5:$I$304<=EDATE(TODAY();-{DORMIENTE_MESI})))'
F["R_C13"] = '=COUNTIF(CLIENTI!$E$5:$E$304;"In ciclo")'
F["R_C17"] = '=COUNTA(CLIENTI!$A$5:$A$304)'
F["R_C20"] = '=COUNTIFS(CLIENTI!$Q$5:$Q$304;">="&TODAY()-30;CLIENTI!$Q$5:$Q$304;"<="&TODAY())'
F["R_C26"] = '=IFERROR(MAX(CLIENTI!$Q$5:$Q$304);"")'
F["R_F5"]  = '=SUM(CLIENTI!$P$5:$P$304)'
F["R_F6"]  = '=SUM(CLIENTI!$O$5:$O$304)'
F["R_F7"]  = '=IFERROR(SUM(CLIENTI!$O$5:$O$304)/COUNTA(CLIENTI!$A$5:$A$304);0)'
F["R_C30"] = '=COUNTIF(CLIENTI!$S$5:$S$304;$B30)'

# ----------------------------------------------------------- il foglio OGGI
F["O_G5"] = '=IFERROR(SMALL(CLIENTI!$T$5:$T$304;ROW()-4);"")'
F["O_A5"] = '=IF($G5="";"";IFERROR(INDEX(CLIENTI!A$5:A$304;MATCH($G5;CLIENTI!$T$5:$T$304;0));""))'

# ------------------------------------------------ formattazione condizionale
# il numero davanti all'avviso e' gia' la priorita': basta leggere quello
F["FC_ROSSO"]  = '=OR(LEFT($B5;1)="1";LEFT($B5;1)="2";LEFT($B5;1)="3")'
F["FC_GIALLO"] = '=OR(LEFT($B5;1)="4";LEFT($B5;1)="5")'
F["FC_VERDE"]  = '=OR(LEFT($B5;1)="6";LEFT($B5;1)="7";LEFT($B5;1)="8")'


def rendi(chiave, mappa):
    return F[chiave].format(**mappa)

def coppia(chiave):
    """(variante celle, variante nomi) — separatore punto e virgola, per Google Fogli"""
    return rendi(chiave, CELLE), rendi(chiave, NOMI)

def perExcel(chiave):
    """La stessa formula come la vuole il formato .xlsx: separatore virgola."""
    return rendi(chiave, CELLE).replace(";", ",")

if __name__ == "__main__":
    for k in F:
        c, n = coppia(k)
        assert c.count("(") == c.count(")"), k
        assert "{" not in c and "}" not in c, k
        assert ";" not in perExcel(k), k
        print("%-8s %4d caratteri" % (k, len(c)))
