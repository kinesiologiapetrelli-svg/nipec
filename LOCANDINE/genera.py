# -*- coding: utf-8 -*-
"""Una locandina, due lingue. Sorgente unica: si cambia qui e si rigenerano
   tutte e due, cosi' non possono divergere.

   Le macchine stanno in primo piano, perche' e' la prima cosa che il centro
   guarda. Le foto sono i ritagli su trasparente presi dal Drive NIPEC
   (ARES_scontornato.png e AFRODITE_scontornato.png).

   Le altezze sono diverse di proposito: Afrodite e' un carrello alto,
   Ares un apparecchio da banco. Metterle alla stessa altezza farebbe
   sembrare Ares grande il doppio di quello che e'."""
import io, os

QUI = os.path.dirname(os.path.abspath(__file__))

COMUNE = dict(
  foto=[('foto/afrodite-pulita.png', 592), ('foto/ares-pulita.png', 404)],
  sito='www.nipecestetica.eu',
)

TESTI = {
 'it': dict(lingua='it', file='locandina-noleggio-it',
   occhiello='NOLEGGIO MENSILE',
   nomi=['AFRODITE MULTISHAPE', 'LASER ARES'],
   sotto=['5 tecnologie su un\'unica piattaforma', 'epilazione definitiva · 10 diodi'],
   bolli=['5 TECNOLOGIE', 'CONTROLLO IA'],
   prezzo='500', valuta='€', periodo='AL MESE',
   zero='zero anticipo\nzero cauzione',
   chip=['senza vincoli', 'senza rischi', 'assistenza tecnica', 'supporto marketing'],
   patto='Te la porto il <b>primo</b> del mese, me la paghi il <b>trenta</b>.',
   patto_sotto='Trenta giorni per lavorarci prima di tirare fuori un euro.',
   piede='PER INFO', tel='+39 351 846 6025'),
 'al': dict(lingua='sq', file='locandina-noleggio-al',
   occhiello='QIRA MUJORE',
   nomi=['AFRODITE MULTISHAPE', 'LASER ARES'],
   sotto=['5 teknologji në një platformë', 'epilim përfundimtar · 10 dioda'],
   bolli=['5 TEKNOLOGJI', 'KONTROLL ME IA'],
   prezzo='50.000', valuta='LEKË', periodo='NË MUAJ',
   zero='pa paradhënie\npa garanci',
   chip=['pa kontratë afati', 'pa rrezik', 'asistencë teknike', 'mbështetje marketingu'],
   patto='Ta sjell më <b>1</b> të muajit, ma paguan më <b>30</b>.',
   patto_sotto='Tridhjetë ditë punë para se të nxjerrësh një lek.',
   piede='PËR INFO', tel='+355 69 212 9786'),
}

MARCHIO = '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="40" fill="none" stroke="#DBE7F3" stroke-width="2.6"/>
  <path d="M50 10 A40 40 0 1 1 30 15.36" fill="none" stroke="#1C6EA4" stroke-width="7.5" stroke-linecap="round"/>
  <circle cx="30" cy="15.36" r="5.4" fill="#123A63"/>
  <rect x="33.5" y="52" width="7" height="15" rx="3.5" fill="#5AA6D6"/>
  <rect x="46.5" y="44" width="7" height="23" rx="3.5" fill="#1C6EA4"/>
  <rect x="59.5" y="36" width="7" height="31" rx="3.5" fill="#123A63"/>
</svg>'''

PAGINA = '''<!doctype html><html lang="{lingua}"><meta charset="utf-8">
<style>
  *{{box-sizing:border-box;margin:0}}
  html,body{{width:1080px;height:1350px}}
  body{{font-family:Archivo,Arial,sans-serif;color:#123A63;
       background:linear-gradient(180deg,#FFFFFF 0%,#FFFFFF 54%,#EAF2FA 100%);
       display:flex;flex-direction:column;overflow:hidden;position:relative}}

  header{{padding:40px 64px 0;display:flex;align-items:center;gap:18px}}
  header .m{{width:62px;height:62px;flex:none}}
  header .n{{font-size:32px;font-weight:700;letter-spacing:.26em;line-height:1;color:#123A63}}
  header .s{{font-size:12px;font-weight:600;letter-spacing:.3em;color:#5A6B80;margin-top:6px}}
  header .occ{{margin-left:auto;background:#123A63;color:#fff;padding:11px 24px;border-radius:999px;
    font-size:21px;font-weight:700;letter-spacing:.16em;white-space:nowrap}}

  /* il palco: le macchine in primo piano, con la loro ombra a terra */
  .palco{{margin-top:34px;padding:0 54px;height:648px;position:relative;
    display:flex;align-items:flex-end;justify-content:center;gap:48px}}
  .palco::before{{content:'';position:absolute;left:150px;right:150px;bottom:96px;height:34px;
    background:radial-gradient(ellipse at 50% 50%, rgba(18,58,99,.20), rgba(18,58,99,0) 70%)}}
  .pezzo{{display:flex;flex-direction:column;align-items:center;position:relative;z-index:1}}
  .pezzo:first-child .bollo{{right:auto;left:-10px}}
  .pezzo .bollo{{position:absolute;top:6px;right:-6px;z-index:2;
    background:linear-gradient(135deg,#1C6EA4,#123A63);color:#fff;
    padding:11px 20px 11px 16px;border-radius:999px;
    font-size:21px;font-weight:700;letter-spacing:.07em;white-space:nowrap;
    box-shadow:0 8px 18px rgba(18,58,99,.30);display:flex;align-items:center;gap:9px}}
  .pezzo .bollo i{{width:11px;height:11px;border-radius:50%;background:#5AA6D6;
    box-shadow:0 0 0 5px rgba(90,166,214,.28);flex:none}}
  .pezzo img{{display:block;filter:drop-shadow(0 18px 22px rgba(18,58,99,.22))}}
  .pezzo b{{display:block;margin-top:20px;font-size:30px;font-weight:700;color:#123A63;
    text-align:center;line-height:1.1;white-space:nowrap}}
  .pezzo em{{font-style:normal;font-size:20px;color:#5A6B80;font-weight:500;
    text-align:center;margin-top:6px;display:block;line-height:1.25;white-space:nowrap}}

  .prezzo{{padding:0 64px;display:flex;align-items:center;gap:24px}}
  .prezzo .v{{font-size:{dim}px;font-weight:700;line-height:.84;letter-spacing:-.035em;color:#1C6EA4}}
  .prezzo .u{{font-size:58px;font-weight:700;color:#5AA6D6;align-self:flex-start;margin-top:10px}}
  .prezzo .p{{font-size:38px;font-weight:600;letter-spacing:.1em;color:#123A63;line-height:1.1}}
  .prezzo .zero{{margin-left:auto;text-align:right;font-size:27px;font-weight:700;
    color:#1C6EA4;line-height:1.35;white-space:pre-line}}

  .chip{{padding:22px 64px 0;display:flex;flex-wrap:wrap;gap:12px}}
  .chip span{{border:2px solid #1C6EA4;border-radius:999px;background:#fff;
    padding:10px 22px;font-size:24px;font-weight:600;color:#123A63}}

  .patto{{margin:24px 64px 0;background:#EAF2FA;border-left:6px solid #1C6EA4;
    border-radius:9px;padding:22px 28px}}
  .patto p{{font-size:32px;font-weight:600;line-height:1.26;color:#123A63}}
  .patto small{{display:block;margin-top:8px;font-size:22px;color:#5A6B80;font-weight:500}}

  footer{{margin-top:auto;flex:none;background:#123A63;color:#fff;padding:26px 64px;
    display:flex;align-items:center;justify-content:space-between;gap:20px}}
  footer .t{{font-size:16px;font-weight:700;letter-spacing:.26em;color:#9CCBE8}}
  footer .tel{{font-size:40px;font-weight:700;line-height:1.05}}
  footer .sito{{font-size:23px;font-weight:600;color:#D5E6F2;text-align:right}}
</style>
<header><div class="m">{marchio}</div>
  <div><div class="n">NIPEC</div><div class="s">TECNOLOGIE ESTETICHE</div></div>
  <div class="occ">{occhiello}</div></header>
<div class="palco">{pezzi}</div>
<div class="prezzo"><span class="v">{prezzo}</span><span class="u">{valuta}</span>
  <span class="p">{periodo}</span>
  <span class="zero">{zero}</span></div>
<div class="chip">{chips}</div>
<div class="patto"><p>{patto}</p><small>{patto_sotto}</small></div>
<footer><div><div class="t">{piede}</div><div class="tel">{tel}</div></div>
  <div class="sito">{sito}</div></footer>
</html>'''

def costruisci(t):
    pezzi = ''.join(
        '<div class="pezzo">%s<img src="%s" style="height:%dpx"><b>%s</b><em>%s</em></div>'
        % ('<span class="bollo"><i></i>%s</span>' % t['bolli'][i] if t['bolli'][i] else '',
           COMUNE['foto'][i][0], COMUNE['foto'][i][1], t['nomi'][i], t['sotto'][i])
        for i in range(len(t['nomi'])))
    chips = ''.join('<span>%s</span>' % c for c in t['chip'])
    dim = 168 if len(t['prezzo']) <= 3 else 112
    d = dict(t); d.pop('nomi'); d.pop('sotto'); d.pop('chip'); d.pop('file'); d.pop('bolli')
    return PAGINA.format(marchio=MARCHIO, pezzi=pezzi, chips=chips, dim=dim,
                         sito=COMUNE['sito'], **d)

for k, t in TESTI.items():
    f = os.path.join(QUI, t['file'] + '.html')
    io.open(f, 'w', encoding='utf-8').write(costruisci(t))
    print('scritto', t['file'] + '.html')
