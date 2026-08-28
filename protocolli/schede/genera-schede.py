# -*- coding: utf-8 -*-
import io, os
OUT = os.path.dirname(os.path.abspath(__file__))

BLU="#1C6EA4"; PROF="#123A63"; CHIARO="#5AA6D6"; GRIGIO="#8E9295"; INK="#17222E"; VELO="#DBE7F3"
ROSSO="#B3261E"; VERDE="#2E7D4F"; AMBRA="#B8860B"

EM = """<svg viewBox="0 0 100 100" class="em"><circle cx="50" cy="50" r="40" fill="none" stroke="%s" stroke-width="2.6"/><path d="M50 10 A40 40 0 1 1 30 15.36" fill="none" stroke="%s" stroke-width="7.5" stroke-linecap="round"/><circle cx="30" cy="15.36" r="5.4" fill="%s"/><rect x="33.5" y="52" width="7" height="15" rx="3.5" fill="%s"/><rect x="46.5" y="44" width="7" height="23" rx="3.5" fill="%s"/><rect x="59.5" y="36" width="7" height="31" rx="3.5" fill="%s"/></svg>""" % (VELO,BLU,PROF,CHIARO,BLU,PROF)

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1350px;overflow:hidden}
body{font-family:"DejaVu Sans","Liberation Sans",Arial,sans-serif;background:#fff;color:%(INK)s;
     display:flex;flex-direction:column}
.bar{height:12px;background:linear-gradient(90deg,%(PROF)s 0%%,%(BLU)s 55%%,%(CHIARO)s 100%%);flex:none}
header{flex:none;display:flex;align-items:center;justify-content:space-between;padding:30px 60px 0}
.brand{display:flex;align-items:center;gap:15px}.em{width:48px;height:48px;flex:none}
.bname{font-size:21px;font-weight:700;letter-spacing:6px;color:%(PROF)s;line-height:1}
.btag{font-size:10px;font-weight:600;letter-spacing:3px;color:%(BLU)s;margin-top:5px}
.step{font-size:15px;font-weight:700;letter-spacing:2px;color:%(GRIGIO)s}
main{flex:1;padding:30px 60px 0;display:flex;flex-direction:column;min-height:0}
.fase{font-size:17px;font-weight:700;letter-spacing:4px;color:%(BLU)s;margin-bottom:10px}
h1{font-size:66px;line-height:1.08;font-weight:700;color:%(PROF)s;letter-spacing:-1px}
h1 .lite{font-weight:400;color:%(BLU)s}
.sub{font-size:27px;color:%(GRIGIO)s;margin-top:14px;line-height:1.4}
.min{display:inline-block;background:%(VELO)s;color:%(PROF)s;font-size:20px;font-weight:700;
     border-radius:8px;padding:6px 16px;margin-top:18px}
ol.fasi{list-style:none;margin-top:26px;counter-reset:f}
ol.fasi li{counter-increment:f;display:flex;gap:22px;align-items:baseline;padding:21px 0;
           border-top:1.5px solid %(VELO)s;font-size:32px;font-weight:700;color:%(PROF)s}
ol.fasi li:last-child{border-bottom:1.5px solid %(VELO)s}
ol.fasi li::before{content:counter(f);flex:none;width:44px;height:44px;border-radius:11px;
   background:%(BLU)s;color:#fff;font-size:22px;display:flex;align-items:center;justify-content:center;
   align-self:center}
ol.fasi li span{font-weight:400;font-size:22px;color:%(GRIGIO)s;margin-left:auto;align-self:center}
ul.chk{list-style:none;margin-top:22px}
ul.chk li{display:flex;gap:18px;align-items:flex-start;padding:16px 0;font-size:27px;line-height:1.3;
          border-top:1px solid %(VELO)s}
ul.chk li:last-child{border-bottom:1px solid %(VELO)s}
ul.chk li .bx{flex:none;width:30px;height:30px;border:2.5px solid %(ROSSO)s;border-radius:6px;margin-top:2px}
table{width:100%%;border-collapse:collapse;margin-top:24px;font-size:26px}
th{background:%(PROF)s;color:#fff;font-size:19px;letter-spacing:2px;padding:14px 18px;text-align:left}
td{border-bottom:1.5px solid %(VELO)s;padding:20px 18px;vertical-align:middle}
td.k{color:%(GRIGIO)s;font-size:26px}
td.v{font-weight:700;color:%(PROF)s;text-align:right;font-size:33px}
.stop{background:%(ROSSO)s;color:#fff;border-radius:16px;padding:30px 34px;margin-top:26px;
      font-size:29px;line-height:1.35;font-weight:700}
.sem{border-radius:16px;padding:24px 30px;margin-top:18px;color:#fff}
.sem .t{font-size:33px;font-weight:700}
.sem .d{font-size:25px;margin-top:8px;line-height:1.35;opacity:.95}
.sem.sv{background:%(VERDE)s}.sem.sa{background:%(AMBRA)s}.sem.sr{background:%(ROSSO)s}
.note{background:#F3F8FC;border-radius:16px;padding:28px 32px;margin-top:24px;font-size:26px;
      line-height:1.4;color:%(INK)s}
.note b{color:%(PROF)s}
.big{font-size:40px;font-weight:700;color:%(PROF)s;margin-top:22px;line-height:1.2}
.tel{margin-top:auto;margin-bottom:8px;background:%(BLU)s;color:#fff;border-radius:16px;
     padding:22px 30px;display:flex;align-items:center;justify-content:space-between}
.tel .l{font-size:16px;font-weight:700;letter-spacing:3px;color:#DDEEFB}
.tel .n{font-size:42px;font-weight:700;margin-top:4px}
footer{flex:none;padding:20px 60px 26px;display:flex;justify-content:space-between;
       border-top:2px solid %(VELO)s;font-size:17px;color:%(GRIGIO)s}
footer b{color:%(PROF)s}
""" % dict(INK=INK,PROF=PROF,BLU=BLU,CHIARO=CHIARO,GRIGIO=GRIGIO,VELO=VELO,ROSSO=ROSSO,VERDE=VERDE,AMBRA=AMBRA)

def page(step, body, foot="PROTOCOLLO DEMETRA · AFRODITE"):
    return """<!doctype html><html lang="it"><head><meta charset="utf-8"><style>%s</style></head><body>
<div class="bar"></div>
<header><div class="brand">%s<div><div class="bname">NIPEC</div><div class="btag">TECNOLOGIE ESTETICHE</div></div></div>
<div class="step">%s</div></header>
<main>%s</main>
<footer><div><b>%s</b></div><div>livello BASE</div></footer>
</body></html>""" % (CSS, EM, step, body, foot)

C=[]

C.append(page("1 / 9", """
<div class="fase">PROTOCOLLO DEMETRA</div>
<h1>La seduta<br><span class="lite">in 6 fasi.</span></h1>
<div class="sub">Corpo · Afrodite · livello BASE</div>
<ol class="fasi">
<li>Controindicazioni <span>5 min</span></li>
<li>Valutazione <span>5 min</span></li>
<li>Il cancello <span>1 min</span></li>
<li>Apertura circolatoria <span>5-8 min</span></li>
<li>Gambe <b>oppure</b> ventre <span>30-45 min</span></li>
<li>Chiusura e prossimo appuntamento <span>13 min</span></li>
</ol>
<div class="note"><b>Ciclo:</b> 10-12 sedute, 2 a settimana.<br><b>Misure e foto</b> alle sedute <b>1, 5 e 10</b>.<br>Durata della seduta: <b>45-60 minuti</b>.</div>
<div class="note">Si esegue con la <b>Scheda di Valutazione</b> in mano. Senza quella, il protocollo non parte.</div>
"""))

C.append(page("2 / 9", """
<div class="fase">FASE 1 · PRIMA DI TOCCARE LA CLIENTE</div>
<h1>Le 11<br><span class="lite">controindicazioni.</span></h1>
<ul class="chk">
<li><div class="bx"></div><div>Gravidanza o allattamento</div></li>
<li><div class="bx"></div><div>Ferite o lesioni nell'area</div></li>
<li><div class="bx"></div><div>Infiammazioni acute o malattie infettive</div></li>
<li><div class="bx"></div><div>Acne cistica o acuta nell'area</div></li>
<li><div class="bx"></div><div>Filler dermico nell'area</div></li>
<li><div class="bx"></div><div>Cheloidi nell'area</div></li>
<li><div class="bx"></div><div>Herpes simplex · diabete · epilessia</div></li>
<li><div class="bx"></div><div>Angiotelettasia acuta · emofilia</div></li>
<li><div class="bx"></div><div>Tumori maligni</div></li>
<li><div class="bx"></div><div>Tessuto mammario o protesi mammarie</div></li>
<li><div class="bx"></div><div>Pacemaker, defibrillatori o impianti metallici</div></li>
</ul>
<div class="stop">Se anche UNA sola casella è barrata,<br>la seduta non si fa. Nessuna eccezione.</div>
"""))

C.append(page("3 / 9", """
<div class="fase">FASE 2 · CLIENTE SUPINA</div>
<h1>Guardi<br><span class="lite">quattro cose.</span></h1>
<div class="min">5 minuti</div>
<table>
<tr><th>Cosa</th><th>Come si guarda</th></tr>
<tr><td class="k"><b style="color:#123A63">1 · Piedi</b></td><td class="k">A cliente rilassata cadono verso l'esterno.<br>Uguali, o uno più aperto?</td></tr>
<tr><td class="k"><b style="color:#123A63">2 · Lunghezza</b></td><td class="k">Confronti i <b>malleoli</b>.<br>Una gamba arriva più corta?</td></tr>
<tr><td class="k"><b style="color:#123A63">3 · Caviglia</b></td><td class="k">Ruoti piano, una per volta.<br>Una si muove meno?</td></tr>
<tr><td class="k"><b style="color:#123A63">4 · Il lato</b></td><td class="k">Dove c'è l'asimmetria<br>ti aspetti <b>più ristagno</b></td></tr>
</table>
<div class="note"><b>Questo è il momento che la cliente sente.</b> Diglielo a voce:<br>
«Il tuo piede destro cade più aperto e la caviglia si muove meno. Su quella gamba il ristagno
è più probabile — partiamo da lì.»</div>
"""))

C.append(page("4 / 9", """
<div class="fase">FASE 3 · PRIMA DI ACCENDERE</div>
<h1>Il cancello.</h1>
<div class="sem sv"><div class="t">🟢 VERDE — tutto regolare</div><div class="d">Protocollo completo.</div></div>
<div class="sem sa"><div class="t">🟡 GIALLO — asimmetria lieve</div><div class="d">Protocollo completo, ma <b>parti dal lato critico</b>.</div></div>
<div class="sem sr"><div class="t">🔴 ROSSO — caviglia bloccata o gamba corta evidente</div>
<div class="d"><b>Niente rimodellamento oggi.</b> Fai solo circolatorio e drenaggio, scrivi sulla scheda e chiama NIPEC.</div></div>
<div class="note"><b>Rosso non vuol dire seduta annullata.</b><br>La cliente viene trattata lo stesso e paga lo stesso. Salta solo la parte di rimodellamento.</div>
<div class="note">Qualunque sia l'esito, <b>scrivilo sulla scheda</b>. Se è rosso segna anche il giorno in cui hai chiamato.</div>
"""))

C.append(page("5 / 9", """
<div class="fase">FASE 4 · APERTURA CIRCOLATORIA</div>
<h1>Manipolo<br><span class="lite">piccolo.</span></h1>
<div class="sub">Si comincia dal lato critico.</div>
<table>
<tr><th>Parametro</th><th style="text-align:right">Valore</th></tr>
<tr><td class="k">Manipolo</td><td class="v">PICCOLO</td></tr>
<tr><td class="k">Livello RF</td><td class="v">2</td></tr>
<tr><td class="k">Livello vacuum</td><td class="v">1 - 2</td></tr>
<tr><td class="k">Pulsazione</td><td class="v">2 - 3 Hz</td></tr>
<tr><td class="k">Durata</td><td class="v">5 - 8 min</td></tr>
<tr><td class="k">Da dove parti</td><td class="v">LATO CRITICO</td></tr>
</table>
<div class="note"><b>Si parte sempre bassi e si sale piano.</b> Mai partire alti.<br>
Lozione <b>solo dove tocca il manipolo</b>: se ne metti troppa intasi l'ugello — è il guasto n°1.<br>
Il manipolo deve restare <b>ben aderente alla pelle</b>.</div>
"""))

C.append(page("6 / 9", """
<div class="fase">FASE 5 · IL BIVIO</div>
<h1>Gambe.<br><span class="lite">Cliente prona.</span></h1>
<table>
<tr><th>Ultrasuoni · manipolo cavitazione</th><th style="text-align:right"></th></tr>
<tr><td class="k">Modalità</td><td class="v">PULSAZIONE 1</td></tr>
<tr><td class="k">Potenza</td><td class="v">bassa → sali</td></tr>
<tr><td class="k">Durata</td><td class="v">8 min per gamba</td></tr>
</table>
<table>
<tr><th>Rimodellamento · RF + vacuum</th><th style="text-align:right"></th></tr>
<tr><td class="k">Manipolo</td><td class="v">GRANDE</td></tr>
<tr><td class="k">Livello RF</td><td class="v">2 - 3</td></tr>
<tr><td class="k">Livello vacuum</td><td class="v">2 - 3</td></tr>
<tr><td class="k">Super pulsazione</td><td class="v">10 - 12 Hz</td></tr>
<tr><td class="k">Durata</td><td class="v">10 - 25 min</td></tr>
</table>
<div class="note">Inizia sempre <b>dal lato critico</b> e dedicagli più tempo.</div>
"""))

C.append(page("7 / 9", """
<div class="fase">FASE 5 · IL BIVIO</div>
<h1>Ventre.<br><span class="lite">Resta supina.</span></h1>
<table>
<tr><th>Ultrasuoni · manipolo cavitazione</th><th style="text-align:right"></th></tr>
<tr><td class="k">Modalità</td><td class="v">PULSAZIONE 1</td></tr>
<tr><td class="k">Potenza</td><td class="v">bassa → sali</td></tr>
<tr><td class="k">Durata</td><td class="v">10 min</td></tr>
</table>
<table>
<tr><th>Rimodellamento · RF + vacuum</th><th style="text-align:right"></th></tr>
<tr><td class="k">Manipolo</td><td class="v">GRANDE</td></tr>
<tr><td class="k">Livello RF</td><td class="v">2 - 3</td></tr>
<tr><td class="k">Livello vacuum</td><td class="v">2 - 3</td></tr>
<tr><td class="k">Super pulsazione</td><td class="v">10 - 12 Hz</td></tr>
<tr><td class="k">Durata</td><td class="v">10 - 25 min</td></tr>
</table>
<div class="note">La super pulsazione c'è <b>solo sul manipolo grande e sul medio</b>. Sul piccolo non esiste.</div>
"""))

C.append(page("8 / 9", """
<div class="fase">FASE 6 · CHIUSURA</div>
<h1>Prima che esca<br><span class="lite">dalla porta.</span></h1>
<table>
<tr><th>Cosa</th><th style="text-align:right">Quanto</th></tr>
<tr><td class="k">Massaggio drenante total body</td><td class="v">10 min</td></tr>
<tr><td class="k">Compili la scheda</td><td class="v">✓</td></tr>
<tr><td class="k"><b style="color:#123A63">Fissi il prossimo appuntamento</b></td><td class="v">ADESSO</td></tr>
<tr><td class="k">Registri sul cruscotto clienti</td><td class="v">✓</td></tr>
<tr><td class="k">Prodotto Certezze secondo l'obiettivo</td><td class="v">✓</td></tr>
</table>
<div class="note"><b>Non "ti chiamo io". La cliente esce con una data.</b><br>
Se meno del 90% delle clienti in ciclo ha già il prossimo appuntamento, il centro sta perdendo clienti.</div>
<div class="note"><b>Seduta 1, 5 o 10?</b> Misure, foto, e <b>gliele fai vedere</b>.<br>
Alla quinta nessuna ricorda com'era alla prima — se non glielo mostri, molla lì.</div>
"""))

C.append(page("9 / 9", """
<div class="fase">DOPO LA SEDUTA</div>
<h1>La macchina.</h1>
<table>
<tr><th>Cosa fai</th><th style="text-align:right"></th></tr>
<tr><td class="k">Pulisci e disinfetta i manipoli</td><td class="v">✓</td></tr>
<tr><td class="k"><b style="color:#123A63">Controlli il filtro dell'aria</b></td><td class="v">✓</td></tr>
<tr><td class="k">Manipoli sul supporto, mai appesi al cavo</td><td class="v">✓</td></tr>
<tr><td class="k">Spegni</td><td class="v">✓</td></tr>
</table>
<div class="big">I 4 controlli prima di chiamare</div>
<div class="note">1 · C'è corrente e l'interruttore è acceso?<br>
2 · Il manipolo è collegato bene fino in fondo?<br>
3 · <b>L'aspirazione è calata? Guarda clessidra e tubo: se c'è gel, pulisci.</b><br>
4 · Hai messo abbastanza gel sulla pelle?</div>
<div class="note">Se la macchina si ferma <b>chiami e basta</b>: riparazione, ricambi e manodopera sono coperti, e intanto ti arriva la <b>macchina sostitutiva</b>. Non chiudi un'ora.</div>
<div class="tel"><div><div class="l">ASSISTENZA NIPEC</div><div class="n">351 846 6025</div></div></div>
"""))

for i,h in enumerate(C,1):
    io.open(os.path.join(OUT,"c%d.html"%i),"w",encoding="utf-8").write(h)
print("generate", len(C), "schede")
