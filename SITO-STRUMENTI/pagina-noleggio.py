# Genera SITO/noleggio-laser.html, la pagina dove arrivano le inserzioni sul noleggio:
#   python3 SITO-STRUMENTI/pagina-noleggio.py
# Testata e piè di pagina vengono da laser-ares.html, così restano uguali al resto del sito.
# Ogni promessa qui sotto viene dai documenti NIPEC (preventivo ARES/URIEL 2026, STANDARD noleggio,
# scheda 808): non aggiungere condizioni che non stanno in un contratto.
import os, re
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'SITO'))
src = open('laser-ares.html').read()
head, rest = src.split('<main id="contenuto">', 1)
_, foot = rest.split('</main>', 1)
check = re.search(r'<ul class="checks"><li>(<svg.*?</svg>)', src, re.S).group(1)
piu = re.search(r'<div class="faq"><details><summary><span>.*?</span>(<svg.*?</svg>)', open('index.html').read(), re.S).group(1)

WA = 'https://wa.me/393518466025?text=Ciao%20NIPEC%2C%20mi%20interessa%20il%20laser%20a%20noleggio.'
DEMO = 'https://kinesiologiapetrelli-svg.github.io/nipec/APP-ALERT-LASER-DEMO/'
TITLE = 'Laser a noleggio, 500 € al mese senza vincoli | NIPEC'
DESC = 'Laser a diodo ARES 2026 con IA a noleggio: 500 € al mese + IVA, lo fermi quando vuoi. Formazione inclusa, muletto entro 48 ore e l’app che ti dice chi richiamare.'

head = re.sub(r'<title>.*?</title>', '<title>%s</title>' % TITLE, head)
for k in ('name="description"', 'property="og:description"'):
    head = re.sub(r'(<meta %s content=")[^"]*' % k, lambda m: m.group(1) + DESC, head)
head = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + TITLE, head)
head = head.replace('https://nipecestetica.com/laser-ares.html', 'https://nipecestetica.com/noleggio-laser.html')
head = re.sub(r'<link rel="alternate" hreflang[^\n]*\n', '', head)
head = head.replace('<meta name="theme-color"', '<meta name="robots" content="noindex">\n<meta name="theme-color"', 1)

li = lambda x: '<li>%s<span>%s</span></li>' % (check, x)
faq = lambda d, r: '<details><summary><span>%s</span>%s</summary><p class="faq__a">%s</p></details>' % (d, piu, r)

main = '''<main id="contenuto">
<section class="hero"><div class="wrap">
<div class="hero__grid">
  <div class="hero__text">
    <p class="eyebrow">Laser a noleggio · ARES 2026 con IA</p>
    <h1 class="h-display">500 € al mese. Lo fermi quando vuoi.</h1>
    <p class="tagline">Senza vincoli. <span class="accent">E con qualcuno che risponde.</span></p>
    <p class="lead">Un laser a diodo professionale nel tuo centro, con la formazione, l’installazione, l’assistenza diretta e un’app che ogni mattina ti dice quali clienti richiamare. Se si ferma, entro 48 ore hai una macchina sostitutiva.</p>
    <ul class="chips"><li class="chip">500 €/mese + IVA</li><li class="chip">Senza vincoli</li><li class="chip">Muletto in 48 ore</li><li class="chip">App inclusa</li></ul>
    <div class="btn-row"><a class="btn btn--primary" href="{WA}" target="_blank" rel="noopener">Scrivici su WhatsApp</a><a class="btn btn--outline" href="#richiesta">Chiedi di essere richiamata</a></div>
  </div>
  <div class="hero__media"><div class="media-box media-box--square"><img src="assets/img/ares.webp" alt="Laser a diodo ARES 2026 NIPEC a noleggio" width="460" height="460" fetchpriority="high"></div></div>
</div></div></section>

<section class="section bg-ground" id="dentro"><div class="wrap">
  <div class="head"><p class="eyebrow">Dentro il canone</p><h2 class="h2">Non noleggi una macchina. Noleggi tutto quello che le serve per rendere.</h2></div>
  <div class="grid grid--2">
    <div class="card card--navy" style="padding:36px"><span class="card__label">La macchina</span><h3 class="h2" style="font-size:30px">ARES 2026 · IA</h3><p class="body">Diodo 808 nm, 10 diodi da 100 W, 1500 W, testina in titanio. La telecamera legge pelle e pelo e ti propone i parametri: tu confermi.</p><ul style="margin:12px 0 0;padding-left:20px;line-height:1.9"><li>CE italiana · MDR</li><li>Installazione e avvio seguiti da noi</li><li>Guasti da difetto o usura coperti dal canone</li></ul></div>
    <div class="card card--plain" style="padding:36px"><span class="card__label" style="color:#5A6B80">Tutto il resto</span><h3 class="h2" style="font-size:30px">Incluso, non a parte</h3><ul class="checks">{L1}{L2}{L3}{L4}</ul></div>
  </div>
</div></section>

<section class="section" id="app"><div class="wrap split" style="align-items:center">
  <div class="split__a hero__text" style="gap:20px">
    <p class="eyebrow">L’app che arriva con il laser</p>
    <h2 class="h2">Ogni mattina ti dice chi richiamare. E quanto vale.</h2>
    <p class="lead">Chi è in ritardo con la seduta, chi ha finito il ciclo e va proposto il mantenimento, chi non vedi da sei mesi. Tre telefonate al giorno, non venti. Funziona sul tuo telefono, anche senza rete, e le tue clienti restano lì: noi non le vediamo.</p>
    <p class="lead"><b>Chiedi a qualunque altro fornitore di laser se te la dà.</b></p>
    <div class="btn-row"><a class="btn btn--primary" href="{DEMO}" target="_blank" rel="noopener">Prova la demo</a></div>
  </div>
  <div class="split__b"><div class="card card--ice" style="padding:28px"><p class="eyebrow" style="margin-bottom:10px">Come te lo dice, ogni mattina</p><h3 class="h3">3 telefonate · valgono 885 €</h3><p class="body" style="color:#0F1E30;margin-top:8px">Anna — 7 sedute su 8, ultima del ciclo: proponi il mantenimento.<br>Bea — 3 su 8, ricordale la data.<br>Carla — non viene da sei mesi: mandale l’offerta.</p></div></div>
</div></section>

<section class="section bg-ground" id="come"><div class="wrap">
  <div class="head"><p class="eyebrow">Come funziona</p><h2 class="h2">Dalla prima chiamata alla prima cliente.</h2></div>
  <ol class="path">
    <li style="--c:#5AA6D6"><span class="path__k">Oggi</span><span class="path__t">Ci scrivi</span><span class="path__d">Su WhatsApp o col modulo. Ti richiamiamo e guardiamo insieme il tuo centro, gratis.</span></li>
    <li style="--c:#5AA6D6"><span class="path__k">Giorno 0</span><span class="path__t">Consegna in cabina</span><span class="path__d">Installiamo, accendiamo e fai le prime sedute guidate. L’app la installiamo noi sul tuo telefono.</span></li>
    <li style="--c:#1C6EA4"><span class="path__k">+7, +21, +45</span><span class="path__t">Formazione a tappe</span><span class="path__d">Richiamo, sessione online ed esame. L’operatrice esce con un certificato valido 12 mesi.</span></li>
    <li style="--c:#123A63"><span class="path__k">Ogni mese</span><span class="path__t">Dieci minuti con noi</span><span class="path__d">Una videochiamata per controllare la macchina prima che si fermi.</span></li>
  </ol>
</div></section>

<section class="section" id="domande"><div class="wrap">
  <div class="head"><p class="eyebrow">Le domande di tutte</p><h2 class="h2">Prima di scriverci.</h2></div>
  <div class="faq">{FAQ}</div>
</div></section>

<section class="section bg-ground" id="richiesta"><div class="wrap split" style="align-items:flex-start">
  <div class="split__a hero__text" style="gap:22px">
    <p class="eyebrow">Ti richiamiamo noi</p><h2 class="h2">Due minuti di modulo, poi parliamo.</h2>
    <p class="lead">Ti diciamo se il noleggio conviene al tuo centro, con i tuoi numeri. Se non ti conviene, te lo diciamo.</p>
    <div class="btn-row"><a class="btn btn--primary" href="{WA}" target="_blank" rel="noopener">Più veloce: WhatsApp</a></div>
  </div>
  <div class="split__b">
    <form class="form" name="noleggio-laser" method="POST" action="/" data-netlify="true" netlify-honeypot="bot-field">
      <input type="hidden" name="form-name" value="noleggio-laser">
      <input type="hidden" name="fonte" value="">
      <p hidden><label>Non compilare <input name="bot-field"></label></p>
      <h2>Chiedi il noleggio</h2>
      <label class="field">Nome e cognome<input type="text" name="nome" autocomplete="name" required></label>
      <label class="field">Telefono o WhatsApp<input type="tel" name="telefono" autocomplete="tel" inputmode="tel" required></label>
      <label class="field">Nome del centro<input type="text" name="centro" autocomplete="organization"></label>
      <label class="field">Città<input type="text" name="citta" autocomplete="address-level2" required></label>
      <fieldset class="chipset full"><legend>Che laser usi oggi?</legend><div class="chipset__opts"><input type="radio" name="laser" id="la0" value="Nessuno" checked><label for="la0">Nessuno</label><input type="radio" name="laser" id="la1" value="Vecchio"><label for="la1">Ce l’ho, ma è vecchio</label><input type="radio" name="laser" id="la2" value="Recente"><label for="la2">Ne ho uno recente</label></div></fieldset>
      <fieldset class="chipset full"><legend>Dove segni gli appuntamenti?</legend><div class="chipset__opts"><input type="radio" name="agenda" id="ag0" value="Quaderno" checked><label for="ag0">Quaderno</label><input type="radio" name="agenda" id="ag1" value="Telefono"><label for="ag1">Sul telefono</label><input type="radio" name="agenda" id="ag2" value="Gestionale"><label for="ag2">Un gestionale</label></div></fieldset>
      <label class="check full"><input type="checkbox" name="privacy" value="si" required><span>Ho letto l’<a href="privacy.html">informativa privacy</a> e acconsento a essere ricontattata.</span></label>
      <p class="form__error" role="alert">Non siamo riusciti a inviare il modulo. Scrivici su WhatsApp: ti rispondiamo subito.</p>
      <button class="btn btn--primary" type="submit" data-sending="Invio in corso…">Richiamatemi</button>
    </form>
    <div class="success" id="form-success" role="status" hidden>
      <h2 class="h2" style="font-size:32px">Grazie, richiesta ricevuta.</h2><p class="lead">Ti ricontattiamo entro un giorno lavorativo. Se hai fretta, scrivici su WhatsApp.</p>
      <a class="btn btn--primary" href="{WA}" target="_blank" rel="noopener">Apri WhatsApp</a>
    </div>
  </div>
</div></section>
'''
FAQ = ''.join([
  faq('Cosa vuol dire «senza vincoli»?', 'Che il noleggio lo fermi quando vuoi. Le condizioni sono scritte nel contratto: te lo mandiamo da leggere prima, con calma, e rispondiamo a ogni domanda.'),
  faq('E se la macchina si rompe?', 'Ci chiami e parli con una persona che conosce la tua macchina, non con un call center. Se si deve fermare, entro 48 ore hai il muletto: il centro non chiude. I guasti da difetto o da usura normale sono coperti dal canone.'),
  faq('Non ho mai usato un laser. Ce la faccio?', 'La formazione è inclusa ed è un percorso, non una giornata: consegna pratica in cabina, richiamo a 7 giorni, sessione online a 21, esame a 45. E sulla ARES 2026 la telecamera ti propone i parametri.'),
  faq('L’app costa a parte?', 'No, arriva con il laser. La installiamo noi sul tuo telefono il giorno della consegna. Le tue clienti restano sul tuo telefono: noi non le vediamo.'),
  faq('C’è una soluzione che costa meno?', 'C’è la ARES 2025: stessa fisica della 2026, senza telecamera e IA, a 400 € al mese + IVA. Ti diciamo quale ti conviene guardando il tuo centro.'),
  faq('Il prezzo è IVA compresa?', 'No: 500 € al mese + IVA per la ARES 2026 · IA.'),
])
for k, v in dict(WA=WA, DEMO=DEMO, FAQ=FAQ, L1=li('Formazione del team, con esame e certificato'), L2=li('Assistenza diretta: un nome e un numero'), L3=li('Muletto entro 48 ore se si ferma'), L4=li('L’app che ti dice chi richiamare')).items():
    main = main.replace('{' + k + '}', v)
open('noleggio-laser.html', 'w').write(head + main + '</main>' + foot)
