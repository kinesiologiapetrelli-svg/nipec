# -*- coding: utf-8 -*-
"""LA LOCANDINA, versione definitiva. Italiano e albanese da un sorgente solo.

   E' la struttura della locandina albanese di Giorgio — piedistalli, crema,
   oro, i segnaposto sulle citta', il punto esclamativo — con quattro
   correzioni:

   1. Via il furgoncino. Faceva "consegna a domicilio" e abbassava il
      registro. Al suo posto il "30 GIORNI" come ancora: il cervello si
      ricorda i numeri, non le frasi.
   2. Il bollino del noleggio a giornata e' DIVERSO dagli altri due. Prima
      erano tre bollini identici per tre prodotti con tre prezzi diversi:
      chi legge non capiva, e chi non capisce il prezzo non chiama.
   3. Il prezzo dice a cosa si riferisce: "al mese, per il noleggio
      mensile". Sulla giornaliera, il suo prezzo (o "su richiesta").
   4. Le tre colonne hanno altezza fissa: partono tutte dalla stessa riga
      comunque vadano a capo le scritte dentro.
"""
import io, os
QUI = os.path.dirname(os.path.abspath(__file__))

# ---- il prezzo del noleggio a giornata: Giorgio deve ancora darmelo ----
GIORNATA_IT = 'prezzo su richiesta'
GIORNATA_AL = 'çmimi sipas kërkesës'

LINGUE = {
 'it': dict(
   codice='it', lang='it',
   pill='NOLEGGIO FLESSIBILE',
   titolo1='DISPOSITIVI PROFESSIONALI PER', titolo2='IL TUO CENTRO', titoloOro='ESTETICO!',
   occhio='Amplia i servizi che offri<br>senza comprare il macchinario.',
   macchine=[
     dict(foto='foto/ares2025-pulita.png', alt=300, nome='ARES 2024',
          sotto='LASER EPILAZIONE', tipo='A GIORNATA / A SETTIMANA', forte=True,
          dove='Roma e provincia', nota=GIORNATA_IT),
     dict(foto='foto/ares-pulita.png', alt=314, nome='ARES 2026',
          sotto='LASER EPILAZIONE<br>CON IA INTEGRATA', tipo='NOLEGGIO MENSILE', forte=False,
          dove='in tutta Italia', nota=''),
     dict(foto='foto/afrodite-pulita.png', alt=392, nome='AFRODITE SHAPE',
          sotto='RIMODELLAMENTO DEL CORPO', tipo='NOLEGGIO MENSILE', forte=False,
          dove='in tutta Italia', nota=''),
   ],
   prezzo='500', valuta='€', riga2='AL MESE', riga3='PER MACCHINA',
   nota_prezzo='per il noleggio mensile',
   punti=[('doc','SENZA CONTRATTI','a lungo termine'),
          ('no','SENZA ANTICIPO','e senza cauzione'),
          ('cuffia','ASSISTENZA','tecnica inclusa'),
          ('chart','SUPPORTO','marketing')],
   num='30', num_u='GIORNI',
   patto1='Te la portiamo il <b>primo</b> del mese,',
   patto2='la paghi alla <b>fine</b> del mese.',
   patto3='Un mese intero di lavoro prima di tirare fuori un euro.',
   piede='PER INFO', tel='+39 351 846 6025',
   file='prodotto-it'),
 'al': dict(
   codice='al', lang='sq',
   pill='QIRA FLEKSIBËL',
   titolo1='PAJISJE PROFESIONALE PËR', titolo2='QENDRËN TËNDE', titoloOro='ESTETIKE!',
   occhio='Zgjero shërbimet e tua<br>pa investuar në blerjen e pajisjeve.',
   macchine=[
     dict(foto='foto/ares2025-pulita.png', alt=300, nome='ARES 2024',
          sotto='LASER EPILIMI', tipo='DITORE / JAVORE', forte=True,
          dove='Tiranë · Durrës · Elbasan', nota=GIORNATA_AL),
     dict(foto='foto/ares-pulita.png', alt=314, nome='ARES 2026',
          sotto='LASER EPILIMI<br>ME AI TË INTEGRUAR', tipo='QIRA MUJORE', forte=False,
          dove='në të gjithë Shqipërinë', nota=''),
     dict(foto='foto/afrodite-pulita.png', alt=392, nome='AFRODITE SHAPE',
          sotto='RIMODELIM I TRUPIT', tipo='QIRA MUJORE', forte=False,
          dove='në të gjithë Shqipërinë', nota=''),
   ],
   prezzo='50.000', valuta='LEKË', riga2='NË MUAJ', riga3='PËR PAJISJE',
   nota_prezzo='për qiranë mujore',
   punti=[('doc','PA KONTRATA','afatgjata'),
          ('no','PA PARADHËNIE','dhe pa garanci'),
          ('cuffia','ASISTENCË','teknike e përfshirë'),
          ('chart','MBËSHTETJE','marketingu')],
   num='30', num_u='DITË',
   patto1='Ta sjellim pajisjen në <b>fillim</b> të muajit,',
   patto2='ti e paguan në <b>fund</b> të muajit.',
   patto3='Një muaj i tërë pune para se të nxjerrësh një lek.',
   piede='PËR INFO', tel='+355 69 212 9786',
   file='prodotto-al'),
}

ICONE = {
 'doc':   '<path d="M7 2.5h7l5 5v14H7z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M14 2.5v5h5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M10 12.5h8M10 16h8" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>',
 'no':    '<path d="M7 7l10 10M17 7L7 17" stroke="currentColor" stroke-width="2.1" stroke-linecap="round"/>',
 'cuffia':'<path d="M4.5 14v-2a7.5 7.5 0 0 1 15 0v2" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><rect x="2.6" y="13.3" width="4.2" height="6.2" rx="2.1" fill="none" stroke="currentColor" stroke-width="1.6"/><rect x="17.2" y="13.3" width="4.2" height="6.2" rx="2.1" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M19.3 19.5v.5a2.4 2.4 0 0 1-2.4 2.4h-2.3" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>',
 'chart': '<path d="M4 20h16" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><path d="M7.5 20v-5M12 20V9M16.5 20v-8" stroke="currentColor" stroke-width="2.3" stroke-linecap="round"/><path d="M5.5 9.5L10 6l3.5 2.5L19 4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>',
}
PIN = '<svg viewBox="0 0 24 24" fill="none"><path d="M12 22s7-6.1 7-12A7 7 0 0 0 5 10c0 5.9 7 12 7 12z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><circle cx="12" cy="10" r="2.4" fill="currentColor"/></svg>'

MARCHIO = '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="40" fill="none" stroke="#DBE7F3" stroke-width="2.6"/>
  <path d="M50 10 A40 40 0 1 1 30 15.36" fill="none" stroke="#1C6EA4" stroke-width="7.5" stroke-linecap="round"/>
  <circle cx="30" cy="15.36" r="5.4" fill="#123A63"/>
  <rect x="33.5" y="52" width="7" height="15" rx="3.5" fill="#5AA6D6"/>
  <rect x="46.5" y="44" width="7" height="23" rx="3.5" fill="#1C6EA4"/>
  <rect x="59.5" y="36" width="7" height="31" rx="3.5" fill="#123A63"/>
</svg>'''

CSS = '''
  *{box-sizing:border-box;margin:0}
  html,body{width:1080px;height:1350px}
  body{font-family:Archivo,Arial,sans-serif;color:#123A63;overflow:hidden;
       background:linear-gradient(170deg,#FFFFFF 0%,#FDFAF4 58%,#F7EFE1 100%);
       display:flex;flex-direction:column}

  header{padding:36px 56px 0;display:flex;align-items:center;gap:15px}
  header .m{width:56px;height:56px;flex:none}
  header .n{font-size:29px;font-weight:700;letter-spacing:.26em;line-height:1}
  header .s{font-size:10.5px;font-weight:600;letter-spacing:.3em;color:#6B7A8C;margin-top:5px}
  header .occ{margin-left:auto;background:#123A63;color:#fff;padding:12px 26px;border-radius:999px;
    font-size:19px;font-weight:700;letter-spacing:.14em;white-space:nowrap}

  h1{padding:22px 56px 0;font-size:50px;font-weight:700;line-height:1.04;letter-spacing:-.018em}
  h1 em{font-style:normal;color:#B08A3E}
  .occhio{padding:12px 56px 0;font-size:25px;color:#46566B;line-height:1.3;font-weight:500}
  .filetto{margin:16px 56px 0;width:108px;height:4px;background:#B08A3E;border-radius:2px}

  .tre{padding:8px 40px 0;display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;align-items:end}
  .col{position:relative;display:flex;flex-direction:column;justify-content:flex-end;height:620px}

  /* il piedistallo: cilindro crema con la faccia di sopra piu' chiara */
  .scena{position:relative;height:430px}
  .plinto{position:absolute;bottom:0;left:7%;right:7%;height:84px;
    background:linear-gradient(180deg,#EFE3CE 0%,#E6D7BC 55%,#DCCBAB 100%);
    border-radius:50% 50% 16px 16px / 32% 32% 16px 16px;
    box-shadow:0 12px 22px rgba(18,58,99,.12)}
  .plinto i{position:absolute;top:0;left:0;right:0;height:52px;border-radius:50%;
    background:linear-gradient(180deg,#FBF5EA,#F3E9D6)}
  .scena img{position:absolute;left:50%;transform:translateX(-50%);bottom:30px;
    display:block;filter:drop-shadow(0 14px 16px rgba(18,58,99,.22))}

  .scheda{background:#FFFDF8;border:1px solid #EADFC9;border-radius:14px;
    padding:15px 13px 14px;text-align:center;margin-top:12px;
    min-height:176px;display:flex;flex-direction:column;
    box-shadow:0 2px 10px rgba(18,58,99,.05)}
  .scheda b{display:block;font-size:25px;font-weight:700;letter-spacing:-.01em;line-height:1.1}
  .scheda .sub{display:block;font-size:14.5px;color:#6B7A8C;margin-top:4px;line-height:1.3;
    font-weight:700;letter-spacing:.05em}
  .tipo{display:flex;align-items:center;justify-content:center;margin:auto auto 0;width:100%;
    border-radius:999px;padding:9px 10px;font-size:14.5px;font-weight:700;
    letter-spacing:.05em;line-height:1.25;min-height:3.1em;text-align:center}
  .tipo.oro{background:linear-gradient(180deg,#F0DFBC,#E3CDA0);color:#6B5118}
  .tipo.forte{background:#123A63;color:#fff}
  .dove{display:flex;align-items:center;justify-content:center;gap:5px;
    margin-top:9px;font-size:14.5px;color:#46566B;font-weight:600}
  .dove svg{width:15px;height:15px;color:#B08A3E;flex:none}
  .nota{display:block;margin-top:5px;font-size:13.5px;color:#8A7444;font-weight:700;
    letter-spacing:.03em}

  .prezzo{margin:18px 56px 0;display:flex;align-items:center;gap:24px}
  .prezzo .cifra{flex:0 0 auto}
  .prezzo .v{font-size:68px;font-weight:700;line-height:.9;letter-spacing:-.032em}
  .prezzo .v i{font-style:normal;font-size:34px;color:#B08A3E;margin-left:6px}
  .prezzo .r2{font-size:21px;font-weight:700;letter-spacing:.07em;margin-top:5px}
  .prezzo .r3{font-size:14.5px;font-weight:700;letter-spacing:.07em;color:#6B7A8C;margin-top:2px}
  .prezzo .nt{font-size:13.5px;color:#8A7444;font-weight:700;margin-top:5px;letter-spacing:.02em}
  .punti{flex:1 1 auto;display:grid;grid-template-columns:repeat(4,1fr);gap:0}
  .punti div{text-align:center;padding:0 6px;border-left:1px solid #EADFC9}
  .punti .cer{width:46px;height:46px;margin:0 auto 8px;border-radius:50%;
    border:2px solid #DFC9A0;display:flex;align-items:center;justify-content:center;color:#B08A3E}
  .punti svg{width:24px;height:24px}
  .punti b{display:block;font-size:14px;font-weight:700;letter-spacing:.05em;line-height:1.2}
  .punti span{display:block;font-size:13px;color:#6B7A8C;margin-top:2px;line-height:1.2}

  .patto{margin:18px 56px 0;background:#123A63;color:#fff;border-radius:14px;
    padding:20px 28px;display:flex;align-items:center;gap:22px}
  .patto .num{flex:none;display:flex;align-items:baseline;gap:4px;color:#E6D3AC;font-weight:700}
  .patto .num b{font-size:50px;line-height:1;letter-spacing:-.03em}
  .patto .num span{font-size:17px;font-weight:600;letter-spacing:.08em}
  .patto .txt p{font-size:24px;font-weight:600;line-height:1.26}
  .patto .txt small{display:block;margin-top:5px;font-size:17px;color:#C9DCEC;font-weight:500}

  footer{margin-top:auto;flex:none;background:#123A63;color:#fff;padding:22px 56px;
    display:flex;align-items:center;justify-content:space-between;gap:20px}
  footer .t{font-size:13px;font-weight:700;letter-spacing:.26em;color:#9CCBE8}
  footer .tel{font-size:37px;font-weight:700;line-height:1.05}
  footer .sito{font-size:20px;font-weight:600;color:#D5E6F2;text-align:right}
'''

PAGINA = '''<!doctype html><html lang="__LANG__"><meta charset="utf-8">
<style>__CSS__</style>
<header><div class="m">__MARCHIO__</div>
  <div><div class="n">NIPEC</div><div class="s">TECNOLOGIE ESTETICHE</div></div>
  <div class="occ">__PILL__</div></header>
<h1>__T1__<br>__T2__ <em>__TORO__</em></h1>
<div class="occhio">__OCCHIO__</div>
<div class="filetto"></div>
<div class="tre">__COLONNE__</div>
<div class="prezzo">
  <div class="cifra"><div class="v">__PREZZO__<i>__VALUTA__</i></div>
    <div class="r2">__R2__</div><div class="r3">__R3__</div>
    <div class="nt">__NOTAP__</div></div>
  <div class="punti">__PUNTI__</div></div>
<div class="patto">
  <div class="num"><b>__NUM__</b><span>__NUMU__</span></div>
  <div class="txt"><p>__P1__<br>__P2__</p><small>__P3__</small></div></div>
<footer><div><div class="t">__PIEDE__</div><div class="tel">__TEL__</div></div>
  <div class="sito">www.nipecestetica.eu</div></footer>
</html>'''

def costruisci(t):
    colonne = ''.join(
      '<div class="col"><div class="scena"><div class="plinto"><i></i></div>'
      '<img src="%s" style="height:%dpx"></div>'
      '<div class="scheda"><b>%s</b><span class="sub">%s</span>'
      '<span class="tipo %s">%s</span>'
      '<span class="dove">%s%s</span>%s</div></div>'
      % (m['foto'], m['alt'], m['nome'], m['sotto'],
         'forte' if m['forte'] else 'oro', m['tipo'],
         PIN, m['dove'],
         ('<span class="nota">%s</span>' % m['nota']) if m['nota'] else '')
      for m in t['macchine'])
    punti = ''.join(
      '<div><div class="cer"><svg viewBox="0 0 24 24" fill="none">%s</svg></div>'
      '<b>%s</b><span>%s</span></div>' % (ICONE[k], a, b) for k, a, b in t['punti'])
    h = PAGINA
    for chiave, val in (('__LANG__',t['lang']), ('__CSS__',CSS), ('__MARCHIO__',MARCHIO),
        ('__PILL__',t['pill']), ('__T1__',t['titolo1']), ('__T2__',t['titolo2']),
        ('__TORO__',t['titoloOro']), ('__OCCHIO__',t['occhio']), ('__COLONNE__',colonne),
        ('__PREZZO__',t['prezzo']), ('__VALUTA__',t['valuta']), ('__R2__',t['riga2']),
        ('__R3__',t['riga3']), ('__NOTAP__',t['nota_prezzo']), ('__PUNTI__',punti),
        ('__NUM__',t['num']), ('__NUMU__',t['num_u']), ('__P1__',t['patto1']),
        ('__P2__',t['patto2']), ('__P3__',t['patto3']), ('__PIEDE__',t['piede']),
        ('__TEL__',t['tel'])):
        h = h.replace(chiave, val)
    return h

for k, t in LINGUE.items():
    f = os.path.join(QUI, t['file'] + '.html')
    io.open(f, 'w', encoding='utf-8').write(costruisci(t))
    print('scritto', t['file'] + '.html')
