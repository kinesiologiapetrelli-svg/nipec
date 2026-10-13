# Genera SITO/offerta-ares.html dalla struttura di laser-ares.html: python3 SITO-STRUMENTI/pagina-offerta.py
import re,sys
import os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'SITO'))
src=open('laser-ares.html').read()
head,rest=src.split('<main id="contenuto">',1)
_,foot=rest.split('</main>',1)
check=re.search(r'<ul class="checks"><li>(<svg.*?</svg>)',src,re.S).group(1)
WA='https://wa.me/393518466025?text=Ciao%20NIPEC%2C%20vorrei%20l%E2%80%99offerta%20ARES%202026%20a%20%E2%88%9230%25.'
DEMO='https://kinesiologiapetrelli-svg.github.io/nipec/APP-ALERT-LASER-DEMO/'
TITLE='Laser ARES 2026 · IA a −30% fino al 30 novembre | NIPEC'
DESC='Prezzo lancio: 17.500 € invece di 25.000, oppure noleggio a 500 € al mese senza vincoli. Permuta del tuo laser, formazione con esame e l’app che ti dice chi richiamare.'
head=re.sub(r'<title>.*?</title>','<title>%s</title>'%TITLE,head)
head=re.sub(r'(<meta name="description" content=")[^"]*','\\g<1>'+DESC,head)
head=re.sub(r'(<meta property="og:title" content=")[^"]*','\\g<1>'+TITLE,head)
head=re.sub(r'(<meta property="og:description" content=")[^"]*','\\g<1>'+DESC,head)
head=head.replace('https://nipecestetica.com/laser-ares.html','https://nipecestetica.com/offerta-ares.html')
head=re.sub(r'<link rel="alternate" hreflang[^\n]*\n','',head)
head=head.replace('<meta name="theme-color"','<meta name="robots" content="noindex">\n<meta name="theme-color"',1)
def li(x): return '<li>%s<span>%s</span></li>'%(check,x)
main='''<main id="contenuto">
<section class="hero"><div class="wrap">
<div class="hero__grid">
  <div class="hero__text">
    <p class="eyebrow">Offerta lancio · fino al 30 novembre 2026</p>
    <h1 class="h-display">Quante clienti non vedi da sei mesi?</h1>
    <p class="tagline">Non serve il numero esatto. <span class="accent">Ognuna ha già pagato metà del ciclo.</span></p>
    <p class="lead">Con NIPEC non arriva solo il laser ARES 2026 con intelligenza artificiale. Arriva un sistema: formazione con esame, assistenza diretta in italiano e un’app che ogni mattina ti dice chi richiamare, e quanto vale quella telefonata.</p>
    <ul class="chips"><li class="chip">−30% fino al 30/11</li><li class="chip">808 nm · 1500 W</li><li class="chip">CE italiana · MDR</li><li class="chip">Permuta del tuo laser</li></ul>
    <div class="btn-row"><a class="btn btn--primary" href="%(WA)s" target="_blank" rel="noopener">Scrivici su WhatsApp</a><a class="btn btn--outline" href="#richiesta">Prenota l’analisi gratuita</a></div>
  </div>
  <div class="hero__media"><div class="media-box media-box--square"><img src="assets/img/ares.webp" alt="Laser a diodo ARES 2026 NIPEC" width="460" height="460" fetchpriority="high"></div></div>
</div></div></section>

<section class="section bg-ground" id="prezzo"><div class="wrap">
  <div class="head"><p class="eyebrow">Il prezzo</p><h2 class="h2">Due modi di averla. Il −30% è già dentro.</h2><p class="lead">La stessa ARES 2026 · IA: 10 diodi da 100 W, testina in titanio, telecamera che legge pelle e pelo e ti propone i parametri. Decidi sempre tu.</p></div>
  <div class="grid grid--2" data-offerta>
    <div class="card card--navy" style="padding:36px"><span class="card__label">Acquisto</span><h3 class="h2" style="font-size:44px">17.500 €</h3><p class="body"><s>Listino 25.000 €</s> · risparmi 7.500 €</p><ul style="margin:12px 0 0;padding-left:20px;line-height:1.9"><li>Hai già un laser? Lo valutiamo e lo scaliamo dal prezzo</li><li>Formazione del team inclusa</li><li>Garanzia 12 mesi</li></ul></div>
    <div class="card card--plain" style="padding:36px"><span class="card__label" style="color:#5A6B80">Noleggio</span><h3 class="h2" style="font-size:44px">500 € / mese</h3><p class="body" style="color:#5A6B80">+ IVA</p><p class="body">Senza vincoli: se non ti serve più, lo fermi.</p><ul class="checks">%(L1)s%(L2)s%(L3)s</ul></div>
  </div>
  <div class="card card--ice" data-scaduta style="display:none;padding:28px;margin-top:16px"><h3 class="h3">Il prezzo lancio è finito il 30 novembre.</h3><p class="body" style="color:#0F1E30">Scrivici lo stesso: ti diciamo le condizioni di oggi, e se c’è una permuta da valutare.</p></div>
  <p class="body" style="margin-top:16px;color:#5A6B80">Prezzi IVA esclusa. Prezzo lancio valido fino al 30 novembre 2026.</p>
</div></section>

<section class="section" id="sistema"><div class="wrap">
  <div class="head"><p class="eyebrow">Perché è diverso</p><h2 class="h2">Una macchina, da sola, non riempie l’agenda.</h2></div>
  <div class="grid grid--3">
    <div class="rule-item"><h3 class="h3">Ti dice chi richiamare</h3><p class="body">Ogni mattina tre telefonate, in ordine, con quanto vale ognuna. Chi è in ritardo, chi ha finito il ciclo, chi è sparita. L’app è tua e i dati restano sul tuo telefono.</p><p style="margin-top:12px"><a href="%(DEMO)s" target="_blank" rel="noopener">Prova l’app demo →</a></p></div>
    <div class="rule-item"><h3 class="h3">L’operatrice esce certificata</h3><p class="body">Consegna in cabina, richiamo a 7 giorni, sessione online a 21, esame a 45. Certificato nominale valido 12 mesi, da esporre in centro.</p></div>
    <div class="rule-item"><h3 class="h3">Qualcuno risponde</h3><p class="body">Un referente unico, sostituzione dei pezzi, e dieci minuti di videochiamata al mese per fermare i guasti prima che fermino te.</p></div>
  </div>
</div></section>

<section class="section bg-ground" id="richiesta"><div class="wrap split" style="align-items:flex-start">
  <div class="split__a hero__text" style="gap:22px">
    <p class="eyebrow">Analisi gratuita del centro</p><h2 class="h2">Prima i numeri, poi la macchina.</h2>
    <p class="lead">Venti minuti, in videochiamata o in centro. Guardiamo clienti, cabine e listino, e ti diciamo quanto può rendere il laser da te. Se non ti serve una macchina nuova, te lo diciamo.</p>
    <div class="btn-row"><a class="btn btn--primary" href="%(WA)s" target="_blank" rel="noopener">Più veloce: WhatsApp</a></div>
  </div>
  <div class="split__b">
    <form class="form" name="offerta-ares" method="POST" action="/" data-netlify="true" netlify-honeypot="bot-field">
      <input type="hidden" name="form-name" value="offerta-ares">
      <input type="hidden" name="fonte" value="">
      <p hidden><label>Non compilare <input name="bot-field"></label></p>
      <h2>Prenota l’analisi</h2>
      <label class="field">Nome e cognome<input type="text" name="nome" autocomplete="name" required></label>
      <label class="field">Telefono o WhatsApp<input type="tel" name="telefono" autocomplete="tel" inputmode="tel" required></label>
      <label class="field">Nome del centro<input type="text" name="centro" autocomplete="organization"></label>
      <label class="field">Città<input type="text" name="citta" autocomplete="address-level2" required></label>
      <fieldset class="chipset full"><legend>Che laser usi oggi?</legend><div class="chipset__opts"><input type="radio" name="laser" id="la0" value="Nessuno" checked><label for="la0">Nessuno</label><input type="radio" name="laser" id="la1" value="Vecchio"><label for="la1">Ce l’ho, ma è vecchio</label><input type="radio" name="laser" id="la2" value="Recente"><label for="la2">Ne ho uno recente</label></div></fieldset>
      <fieldset class="chipset full"><legend>Ti interessa di più</legend><div class="chipset__opts"><input type="radio" name="formula" id="fo0" value="Acquisto" checked><label for="fo0">Acquisto</label><input type="radio" name="formula" id="fo1" value="Noleggio"><label for="fo1">Noleggio</label><input type="radio" name="formula" id="fo2" value="Non so"><label for="fo2">Ancora non so</label></div></fieldset>
      <label class="check full"><input type="checkbox" name="privacy" value="si" required><span>Ho letto l’<a href="privacy.html">informativa privacy</a> e acconsento a essere ricontattato.</span></label>
      <p class="form__error" role="alert">Non siamo riusciti a inviare il modulo. Scrivici su WhatsApp: ti rispondiamo subito.</p>
      <button class="btn btn--primary" type="submit" data-sending="Invio in corso…">Prenota l’analisi gratuita</button>
    </form>
    <div class="success" id="form-success" role="status" hidden>
      <h2 class="h2" style="font-size:32px">Grazie, richiesta ricevuta.</h2><p class="lead">Ti ricontattiamo entro un giorno lavorativo. Se hai fretta, scrivici su WhatsApp.</p>
      <a class="btn btn--primary" href="%(WA)s" target="_blank" rel="noopener">Apri WhatsApp</a>
    </div>
  </div>
</div></section>
<script>
(function(){ // dopo il 30/11 il prezzo lancio sparisce da solo
  if (new Date() < new Date('2026-12-01T00:00:00+01:00')) return;
  var o = document.querySelector('[data-offerta]'), s = document.querySelector('[data-scaduta]');
  if (o) o.style.display = 'none'; if (s) s.style.display = '';
})();
</script>
'''
for k,v in dict(WA=WA,DEMO=DEMO,L1=li('Formazione del team inclusa'),L2=li('Stessa macchina, stessa IA'),L3=li('Assistenza diretta in italiano')).items(): main=main.replace('%('+k+')s',v)
open('offerta-ares.html','w').write(head+main+'</main>'+foot)
