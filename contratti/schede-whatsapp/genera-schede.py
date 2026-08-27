# -*- coding: utf-8 -*-
import io, os
OUT = os.path.dirname(os.path.abspath(__file__))

BLU      = "#1C6EA4"
PROFONDO = "#123A63"
CHIARO   = "#5AA6D6"
GRIGIO   = "#8E9295"
INK      = "#17222E"
VELO     = "#DBE7F3"

EMBLEMA = """<svg viewBox="0 0 100 100" class="em"><circle cx="50" cy="50" r="40" fill="none" stroke="%s" stroke-width="2.6"/><path d="M50 10 A40 40 0 1 1 30 15.36" fill="none" stroke="%s" stroke-width="7.5" stroke-linecap="round"/><circle cx="30" cy="15.36" r="5.4" fill="%s"/><rect x="33.5" y="52" width="7" height="15" rx="3.5" fill="%s"/><rect x="46.5" y="44" width="7" height="23" rx="3.5" fill="%s"/><rect x="59.5" y="36" width="7" height="31" rx="3.5" fill="%s"/></svg>"""
EM_CHIARO = EMBLEMA % (VELO, BLU, PROFONDO, CHIARO, BLU, PROFONDO)
EM_SCURO  = EMBLEMA % ("rgba(255,255,255,.28)", "#FFFFFF", CHIARO, CHIARO, "#FFFFFF", "#FFFFFF")

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1350px;overflow:hidden}
body{font-family:"DejaVu Sans","Liberation Sans",Arial,sans-serif;background:#fff;color:%(INK)s;
     display:flex;flex-direction:column}
.bar{height:12px;background:linear-gradient(90deg,%(PROFONDO)s 0%%,%(BLU)s 55%%,%(CHIARO)s 100%%);flex:none}
header{flex:none;display:flex;align-items:center;justify-content:space-between;padding:34px 66px 0}
.brand{display:flex;align-items:center;gap:16px}
.em{width:52px;height:52px;flex:none}
.bname{font-size:23px;font-weight:700;letter-spacing:7px;color:%(PROFONDO)s;line-height:1}
.btag{font-size:11px;font-weight:600;letter-spacing:3.2px;color:%(BLU)s;margin-top:5px}
.step{font-size:16px;font-weight:700;letter-spacing:2px;color:%(GRIGIO)s}
main{flex:1;padding:38px 66px 0;display:flex;flex-direction:column;min-height:0}
.eyebrow{font-size:19px;font-weight:700;letter-spacing:5px;color:%(BLU)s;margin-bottom:14px}
h1{font-size:68px;line-height:1.1;font-weight:700;color:%(PROFONDO)s;letter-spacing:-1px}
h1 .lite{font-weight:400;color:%(BLU)s}
.sub{font-size:26px;color:%(GRIGIO)s;margin-top:14px;line-height:1.4}
.rule{height:3px;width:96px;background:%(BLU)s;margin:26px 0 4px}
.opt{border:2px solid %(VELO)s;border-left:12px solid %(BLU)s;border-radius:16px;padding:34px 38px;margin-top:30px}
.opt .n{font-size:15px;font-weight:700;letter-spacing:3px;color:%(BLU)s}
.opt .t{font-size:44px;font-weight:700;color:%(PROFONDO)s;margin-top:6px}
.opt .d{font-size:26px;color:%(INK)s;margin-top:10px;line-height:1.45}
.price{margin-top:24px}
.price .big{font-size:88px;font-weight:700;color:%(PROFONDO)s;letter-spacing:-2px;line-height:1}
.price .iva{font-size:34px;font-weight:600;color:%(BLU)s}
.price .note{font-size:23px;color:%(GRIGIO)s;margin-top:10px}
main>ul{list-style:none;margin-top:30px}
main>ul>li{display:flex;gap:22px;align-items:flex-start;padding:22px 0;border-top:1.5px solid %(VELO)s;
   font-size:27px;line-height:1.35}
main>ul>li:last-child{border-bottom:1.5px solid %(VELO)s}
main>ul>li .ic{flex:none;width:46px;height:46px;border-radius:12px;background:%(VELO)s;color:%(PROFONDO)s;
       display:flex;align-items:center;justify-content:center;font-size:23px;font-weight:700}
main>ul>li b{font-weight:700;color:%(PROFONDO)s}
main>ul>li .s{display:block;font-size:22px;color:%(GRIGIO)s;margin-top:4px;line-height:1.35}
.hl{background:%(PROFONDO)s;color:#fff;border-radius:18px;padding:36px 40px;margin-top:30px}
.hl .k{font-size:17px;font-weight:700;letter-spacing:4px;color:%(CHIARO)s}
.hl .h{font-size:42px;font-weight:700;margin-top:8px;line-height:1.2}
.hl .g{display:flex;flex-wrap:wrap;gap:10px 14px;margin-top:20px}
.hl .g span{background:rgba(255,255,255,.13);border-radius:10px;padding:11px 18px;font-size:23px}
.hl .p{font-size:27px;margin-top:20px;line-height:1.4;border-top:1px solid rgba(255,255,255,.22);padding-top:18px}
.hl .p b{color:%(CHIARO)s}
.tip{background:#F3F8FC;border-radius:18px;padding:32px 36px;margin-top:30px}
.tip .k{font-size:16px;font-weight:700;letter-spacing:3px;color:%(BLU)s}
.tip ol{margin:18px 0 0 30px;font-size:24px;line-height:1.5;list-style:decimal}
.tip ol li{display:list-item;border:none;padding:0;margin-bottom:14px}
.tip ol li::marker{color:%(BLU)s;font-weight:700}
.tip ol b{color:%(PROFONDO)s}
.callout{border:2px dashed %(CHIARO)s;border-radius:16px;padding:30px 34px;margin-top:30px;
         font-size:26px;color:%(INK)s;line-height:1.45}
.tel{margin-top:30px;background:%(BLU)s;color:#fff;border-radius:18px;padding:28px 34px;
     display:flex;align-items:center;justify-content:space-between}
.tel .l{font-size:17px;font-weight:700;letter-spacing:3px;color:#DDEEFB}
.tel .n{font-size:48px;font-weight:700;letter-spacing:1px;margin-top:4px}
.ask{font-size:35px;font-weight:700;color:%(PROFONDO)s;margin-top:30px;line-height:1.3}
footer{flex:none;padding:22px 66px 30px;display:flex;align-items:center;justify-content:space-between;
       border-top:2px solid %(VELO)s;margin:0 0 0;font-size:18px;color:%(GRIGIO)s}
footer b{color:%(PROFONDO)s}
.next{color:%(BLU)s;font-weight:700}
""" % dict(INK=INK,PROFONDO=PROFONDO,BLU=BLU,CHIARO=CHIARO,GRIGIO=GRIGIO,VELO=VELO)

def page(step, main_html, foot_right):
    return """<!doctype html><html lang="it"><head><meta charset="utf-8"><style>%s</style></head><body>
<div class="bar"></div>
<header><div class="brand">%s<div><div class="bname">NIPEC</div><div class="btag">TECNOLOGIE ESTETICHE</div></div></div>
<div class="step">%s</div></header>
<main>%s</main>
<footer><div><b>AFRODITE</b> · sistema multifunzione</div><div class="next">%s</div></footer>
</body></html>""" % (CSS, EM_CHIARO, step, main_html, foot_right)

cards = []

# ---------- 1 ----------
cards.append(page("1 / 5", """
<div class="eyebrow">NIPEC AFRODITE</div>
<h1>Due modi<br><span class="lite">per averla.</span></h1>
<div class="sub">Te li riassumo qui in due minuti.<br>Così quando ci vediamo, il contratto lo leggi già sapendo cosa c'è dentro.</div>
<div class="opt"><div class="n">OPZIONE 1</div><div class="t">La compri</div>
<div class="d">15.000 € + IVA, a rate.<br><b>Alla fine è tua.</b></div></div>
<div class="opt"><div class="n">OPZIONE 2</div><div class="t">La noleggi</div>
<div class="d">500 € + IVA al mese.<br>Resta nostra, ma <b>se si rompe è un problema nostro.</b></div></div>
<div class="callout">In tutti e due i casi <b>consegna, installazione e formazione sono incluse</b>.<br>Quello che cambia è solo chi si prende il rischio della macchina.</div>
""", "continua →"))

# ---------- 2 ----------
cards.append(page("2 / 5", """
<div class="eyebrow">OPZIONE 1 · LA COMPRI</div>
<div class="price"><div class="big">15.000 €<span class="iva"> + IVA</span></div>
<div class="note">18.300 € totali · un anticipo, poi rate mensili</div></div>
<div class="rule"></div>
<ul>
<li><div class="ic">€</div><div><b>Anticipo + rate mensili</b><span class="s">Quante e di quanto lo decidiamo insieme, sui tuoi numeri.</span></div></li>
<li><div class="ic">✓</div><div><b>Consegna e installazione incluse</b><span class="s">Te la portiamo, te la montiamo, te l'accendiamo noi.</span></div></li>
<li><div class="ic">✓</div><div><b>Una giornata di formazione nel tuo centro</b><span class="s">Viene un Beauty Trainer da te. Non un video: una persona.</span></div></li>
<li><div class="ic">✓</div><div><b>Garanzia 12 mesi</b><span class="s">Se si guasta qualcosa, lo sistemiamo noi.</span></div></li>
<li><div class="ic">✓</div><div><b>Percorso di formazione a tappe</b><span class="s">Ci risentiamo a 7, 21 e 45 giorni. Non ti lascio sola dopo il primo giorno.</span></div></li>
</ul>
<div class="callout">🔑 <b>La macchina diventa tua quando finisci di pagare le rate.</b><br>
Fino ad allora resta intestata a noi: è normale, quando si paga a rate funziona così per legge.</div>
""", "continua →"))

# ---------- 3 ----------
cards.append(page("3 / 5", """
<div class="eyebrow">OPZIONE 2 · LA NOLEGGI</div>
<div class="price"><div class="big">500 €<span class="iva"> + IVA / mese</span></div>
<div class="note">610 € al mese · nessun investimento iniziale</div></div>
<div class="hl"><div class="k">FULL KASKO · INCLUSO NEL CANONE</div>
<div class="h">Si rompe? Chiami e basta.</div>
<div class="g"><span>✓ riparazione</span><span>✓ ricambi</span><span>✓ manodopera</span><span>✓ viaggio del tecnico</span></div>
<div class="p">E intanto ti mandiamo la <b>macchina sostitutiva</b>:<br><b>non stai ferma un giorno.</b></div></div>
<ul>
<li><div class="ic">✓</div><div><b>Consegna e installazione incluse</b></div></li>
<li><div class="ic">✓</div><div><b>Manutenzione inclusa</b><span class="s">Ordinaria e straordinaria: non ci pensi tu.</span></div></li>
<li><div class="ic">✓</div><div><b>Formazione base inclusa</b><span class="s">Con le tappe a 7, 21 e 45 giorni.</span></div></li>
<li><div class="ic">🔑</div><div><b>La macchina resta nostra</b><span class="s">Tu paghi solo per usarla.</span></div></li>
</ul>
""", "continua →"))

# ---------- 4 ----------
cards.append(page("4 / 5", """
<div class="eyebrow">IN TUTTI E DUE I CASI</div>
<h1>Cosa resta<br><span class="lite">a carico tuo.</span></h1>
<div class="sub">I pezzi che si consumano lavorando, come le lame di una forbice.</div>
<ul>
<li><div class="ic">◆</div><div><b>Manipoli</b> — 300 € + IVA</div></li>
<li><div class="ic">◆</div><div><b>Tubo del vacuum</b> — 200 € + IVA</div></li>
<li><div class="ic">◆</div><div><b>Gel conduttivo</b></div></li>
</ul>
<div class="callout">Non è un guasto: è <b>usura</b>, come è normale che sia.<br><b>Te lo dico adesso e non dopo</b>, così non ci sono sorprese.</div>
<div class="tip"><div class="k">COME FARLI DURARE IL DOPPIO</div>
<ol><li><b>Sempre gel sulla pelle</b>, mai lavorare a secco.</li>
<li><b>Mai gel sul manipolo vacuum</b>: è quello che intasa il tubo, il guasto n°1.</li>
<li><b>Manipoli sempre nel loro alloggiamento</b>, mai appesi al cavo.</li></ol></div>
""", "continua →"))

# ---------- 5 ----------
cards.append(page("5 / 5", """
<div class="eyebrow">QUANDO CI VEDIAMO</div>
<h1>Cosa trovi<br><span class="lite">nel contratto.</span></h1>
<div class="sub">Esattamente le cose che ti ho scritto qui, scritte per bene. Niente di nascosto.</div>
<ul>
<li><div class="ic">✓</div><div><b>Il verbale di consegna</b><span class="s">Lo firmiamo insieme il giorno che te la porto, con la foto dello stato della macchina.</span></div></li>
<li><div class="ic">✓</div><div><b>La card delle regole</b><span class="s">Da appendere in cabina.</span></div></li>
<li><div class="ic">✓</div><div><b>Il listino dei ricambi</b><span class="s">I prezzi li sai prima, non dopo.</span></div></li>
<li><div class="ic">✓</div><div><b>Il percorso di formazione</b><span class="s">Non ti lascio sola dopo il primo giorno: ci risentiamo a 7, 21 e 45 giorni.</span></div></li>
</ul>
<div class="tel"><div><div class="l">ASSISTENZA NIPEC</div><div class="n">351 846 6025</div></div>%s</div>
<div class="ask">Ti conviene di più comprarla o noleggiarla?<br><span style="font-weight:400;font-size:27px;color:%s">Se non sei sicura, ne parliamo sui tuoi numeri.</span></div>
""" % (EM_SCURO, GRIGIO), "fine"))

for i, html in enumerate(cards, 1):
    io.open(os.path.join(OUT, "card%d.html" % i), "w", encoding="utf-8").write(html)
print("generate %d schede" % len(cards))
