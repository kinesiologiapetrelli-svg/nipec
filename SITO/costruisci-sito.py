# -*- coding: utf-8 -*-
"""Monta le pagine del sito NIPEC: una sola testata, un solo piede,
   il contenuto cambia. Si rilancia dopo ogni modifica ai testi."""
import os, re

WA_IT = 'https://wa.me/393518466025'
WA_AL = 'https://wa.me/355692129786'

LOGO = open('marchio/nipec-logo-orizzontale.svg', encoding='utf-8').read()
LOGO = re.sub(r'<title>.*?</title>', '', LOGO, flags=re.S).strip()
LOGO_NEG = open('marchio/nipec-logo-orizzontale-negativo.svg', encoding='utf-8').read()
LOGO_NEG = re.sub(r'<title>.*?</title>', '', LOGO_NEG, flags=re.S).strip()

PAGINE = [('index.html','Home'),('noleggio.html','Il noleggio'),
          ('macchine.html','Le macchine'),('metodo.html','Come lavoriamo'),
          ('contatti.html','Contatti')]

def nav(attiva):
    righe=[]
    for f, t in PAGINE:
        corrente = ' aria-current="page"' if f == attiva else ''
        righe.append('    <a href="%s"%s>%s</a>' % (f, corrente, t))
    return '\n'.join(righe)

def pagina(file, titolo, descrizione, corpo):
    html = f'''<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{titolo}</title>
<meta name="description" content="{descrizione}">
<link rel="stylesheet" href="stile.css">
<link rel="icon" href="marchio/nipec-emblema.svg" type="image/svg+xml">
<meta property="og:title" content="{titolo}">
<meta property="og:description" content="{descrizione}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://nipecestetica.eu/{'' if file=='index.html' else file}">
<meta property="og:locale" content="it_IT">
</head>
<body>

<header>
  <div class="barra">
    <a class="marchio" href="index.html" aria-label="NIPEC · Tecnologie Estetiche">{LOGO}</a>
    <nav>
{nav(file)}
    </nav>
  </div>
</header>

{corpo}

<footer>
  <div class="dentro">
    <div class="piede-righe">
      <div>
        {LOGO_NEG}
        <p style="margin:0;max-width:26em">Noleggio e vendita di tecnologie estetiche
        professionali. Macchine certificate in Italia, formazione compresa, assistenza
        sempre.</p>
      </div>
      <div>
        <h4>Parliamone</h4>
        <ul>
          <li>Italia · <a href="{WA_IT}">351 846 6025</a></li>
          <li>Albania · <a href="{WA_AL}">+355 69 212 9786</a></li>
        </ul>
      </div>
      <div>
        <h4>Pagine</h4>
        <ul>
''' + '\n'.join(f'          <li><a href="{f}">{t}</a></li>' for f, t in PAGINE) + '''
          <li><a href="privacy.html">Privacy</a></li>
        </ul>
      </div>
    </div>
    <div class="fine">
      <span>NIPEC · Tecnologie Estetiche</span>
      <span><a href="privacy.html">Informativa privacy</a></span>
    </div>
  </div>
</footer>

</body>
</html>
'''
    open(file, 'w', encoding='utf-8').write(html)
    return len(html)

def chiamata(testo="Parliamone tre minuti"):
    return f'''<section class="chiamata">
  <div class="dentro">
    <h2>{testo}</h2>
    <p style="max-width:34em">Non ti vendiamo niente al primo messaggio. Otto domande sul
    tuo giro clienti, e alla fine hai in mano un numero che oggi non hai.</p>
    <div class="bottoni">
      <a class="btn" href="{WA_IT}">Scrivi in Italia · 351 846 6025</a>
      <a class="btn vuoto" href="{WA_AL}">Shkruaj në Shqipëri · +355 69 212 9786</a>
    </div>
  </div>
</section>'''

CONDIZIONI = '''<table>
  <tr><th>Voce</th><th>Com'è</th></tr>
  <tr><td>Canone</td><td><b>500 € al mese</b> — in Albania 50.000 Lekë</td></tr>
  <tr><td>Vincolo</td><td><b>Nessuno.</b> La fermi quando vuoi</td></tr>
  <tr><td>Anticipo</td><td>Zero</td></tr>
  <tr><td>Cauzione</td><td>Zero</td></tr>
  <tr><td>Quando si paga</td><td>La macchina arriva il <b>1</b>. Si paga entro il <b>30</b></td></tr>
  <tr><td>Ferie</td><td>La restituisci e <b>quel mese non paghi</b></td></tr>
  <tr><td>Formazione</td><td><b>Compresa</b>, in sede, il giorno della consegna</td></tr>
  <tr><td>Assistenza</td><td>Sempre. Se si ferma, <b>macchina sostitutiva entro 48 ore</b></td></tr>
  <tr><td>Protocollo</td><td>Scritto, pagina per pagina. Arriva con la macchina</td></tr>
  <tr><td>Certificazione</td><td>CE italiana, <b>MDR attivo</b></td></tr>
</table>'''

# ======================= HOME =======================
pagina('index.html',
 'NIPEC · Tecnologie estetiche a noleggio — 500 € al mese',
 'Laser e rimodellamento corpo a noleggio per centri estetici. 500 € al mese, nessun vincolo, nessun anticipo. Formazione compresa, assistenza sempre, macchina sostitutiva in 48 ore.',
f'''<section class="apre">
  <div class="dentro">
    <p class="occhiello">Noleggio per centri estetici</p>
    <h1>La macchina arriva il 1. La paghi il 30.</h1>
    <p class="sotto">Trenta giorni di lavoro prima di tirare fuori il primo euro.
    Nessun anticipo, nessuna cauzione, nessun vincolo da firmare.</p>
    <div class="bottoni">
      <a class="btn" href="{WA_IT}">Parliamone · 351 846 6025</a>
      <a class="btn vuoto" href="noleggio.html">Tutte le condizioni</a>
    </div>
    <p class="sotto-btn">500 € al mese · in Albania 50.000 Lekë</p>
  </div>
</section>

<section>
  <div class="dentro">
    <h2>Tre cose che cambiano come lavori</h2>
    <p class="guida">Non è il prezzo a fare la differenza. È quello che succede quando
    qualcosa non va.</p>
    <div class="tre">
      <div class="scheda">
        <span class="num">Se si ferma</span>
        <h3>Macchina sostitutiva in 48 ore</h3>
        <p>Non chiudi un'ora, non disdici nessuna cliente. Un laser fermo una settimana sono
        dodici clienti che saltano il turno — e la maggior parte non rientra più.</p>
      </div>
      <div class="scheda">
        <span class="num">Se non sai usarla</span>
        <h3>Il protocollo arriva scritto</h3>
        <p>Cosa si fa da quando la cliente entra a quando esce, con quali parametri, e ogni
        quanto si richiama. Più la formazione in sede, compresa.</p>
      </div>
      <div class="scheda">
        <span class="num">Se arriva un controllo</span>
        <h3>Certificate in Italia, MDR attivo</h3>
        <p>Dichiarazione di conformità e numero di serie rintracciabili. C'è una carta da
        mostrare, con un nome e un indirizzo dietro.</p>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="dentro">
    <h2>Le condizioni, tutte qui</h2>
    <p class="guida">Niente da cercare nelle note in fondo.</p>
    {CONDIZIONI}
    <div class="nota verde">
      <span class="eti">Perché il 1 e il 30</span>
      <p>Perché il rischio sta dalla nostra parte. Tu lavori trenta giorni, e paghi con
      quello che la macchina ti ha già portato.</p>
    </div>
  </div>
</section>

<section>
  <div class="dentro">
    <h2>Cosa noleggiamo</h2>
    <div class="due">
      <div class="scheda">
        <span class="num">Epilazione</span>
        <h3>Laser a diodo 808 nm</h3>
        <p>Ultima generazione, con telecamera e intelligenza artificiale a bordo. Fino a
        sedici diodi, fino a 2000 watt, testina in titanio.</p>
        <p style="margin-top:10px"><a href="macchine.html">Vedi le macchine →</a></p>
      </div>
      <div class="scheda">
        <span class="num">Rimodellamento corpo</span>
        <h3>Afrodite VS++</h3>
        <p>Quattro tecnologie in una macchina sola: cavitazione, radiofrequenza, vacuum e
        LED. Con il metodo DEMETRA e i protocolli di cabina.</p>
        <p style="margin-top:10px"><a href="macchine.html">Vedi le macchine →</a></p>
      </div>
    </div>
  </div>
</section>

{chiamata()}''')

# ======================= NOLEGGIO =======================
pagina('noleggio.html',
 'Il noleggio · NIPEC — 500 € al mese, nessun vincolo',
 'Le condizioni del noleggio NIPEC per intero: 500 € al mese, zero anticipo, zero cauzione, nessun vincolo, consegna il 1 e pagamento entro il 30, formazione e assistenza comprese.',
f'''<section class="apre">
  <div class="dentro">
    <p class="occhiello">Il noleggio</p>
    <h1>Zero anticipo, zero cauzione, nessuna firma di vincolo</h1>
    <p class="sotto">E la prima rata la paghi dopo trenta giorni di lavoro.</p>
  </div>
</section>

<section>
  <div class="dentro">
    <h2>Le condizioni</h2>
    {CONDIZIONI}
  </div>
</section>

<section>
  <div class="dentro">
    <h2>Le domande che ci fanno sempre</h2>

    <h3>Quanto devo tenerla come minimo?</h3>
    <p>Quanto ti serve. Non c'è un minimo e non c'è un vincolo da firmare: se smette di
    renderti, ce la ridai.</p>

    <h3>E se ad agosto chiudo?</h3>
    <p>Ce la restituisci e quel mese non paghi. Riapri a settembre e te la riportiamo.</p>

    <h3>Se si rompe, chi paga?</h3>
    <p>L'assistenza è nostra. Se la macchina si ferma te ne arriva un'altra entro 48 ore:
    tu non chiudi un'ora. Rispondi solo dei danni che derivano da un uso contrario ai
    protocolli — gli stessi che ti consegniamo scritti.</p>

    <h3>La formazione quanto costa?</h3>
    <p>È compresa. Si fa in sede il giorno della consegna, con le operatrici che ci sono.</p>

    <h3>Posso comprarla invece di noleggiarla?</h3>
    <p>Sì. Ma il nostro consiglio è provarla a noleggio: se il trattamento gira, la scelta
    la fai con i numeri in mano invece che sulla fiducia.</p>

    <div class="nota">
      <span class="eti">Una cosa che diciamo prima che ce la chiedi</span>
      <p>Il noleggio non ti serve se la macchina resta in un angolo. Per questo con la
      macchina arrivano il protocollo, la formazione e qualcuno che risponde al telefono —
      <a href="metodo.html">è così che lavoriamo</a>.</p>
    </div>
  </div>
</section>

{chiamata("Vuoi vedere i numeri sul tuo centro?")}''')

# ======================= MACCHINE =======================
pagina('macchine.html',
 'Le macchine · NIPEC — laser a diodo 808 nm e Afrodite VS++',
 'Laser a diodo 808 nm con telecamera e intelligenza artificiale, fino a 16 diodi e 2000 watt. Afrodite VS++ per il rimodellamento corpo: cavitazione, radiofrequenza, vacuum e LED.',
f'''<section class="apre">
  <div class="dentro">
    <p class="occhiello">Le macchine</p>
    <h1>Due macchine, due lavori diversi</h1>
    <p class="sotto">Il laser porta la cliente dodici volte. Afrodite la tiene per un
    percorso intero.</p>
  </div>
</section>

<section>
  <div class="dentro">
    <h2>Laser a diodo 808 nm</h2>
    <p class="guida">Epilazione corpo. Ultima generazione, con telecamera e intelligenza
    artificiale a bordo: i parametri non li cerchi più a memoria.</p>
    <table>
      <tr><th>Caratteristica</th><th>Valore</th></tr>
      <tr><td>Tipo</td><td>Laser a diodo. Fino a tre lunghezze d'onda sullo stesso manipolo — 755 / 808 / 1064 nm</td></tr>
      <tr><td>Diodi</td><td>Fino a 16 diodi da 100 W</td></tr>
      <tr><td>Potenza</td><td>Fino a 2000 W</td></tr>
      <tr><td>Emissione</td><td>1–400 ms · macrocanale</td></tr>
      <tr><td>Telecamera e IA</td><td>Sì — la macchina propone griglia, kJ target e fluenza</td></tr>
      <tr><td>Sistemi</td><td>HR · SHR · SHR Stack</td></tr>
      <tr><td>Testina</td><td>Titanio</td></tr>
      <tr><td>Gestione e alimentazione</td><td>Digitali, a controllo elettronico</td></tr>
      <tr><td>Sicurezza</td><td>Classe 4 · interlock</td></tr>
      <tr><td>Certificazione</td><td>CE italiana · MDR attivo</td></tr>
    </table>
    <div class="nota">
      <span class="eti">Tre bande, una cosa sola da ricordare</span>
      <p>755 prende il pelo sottile e chiaro, 808 è il cavallo di battaglia, 1064 scende in
      profondità e lavora sulle pelli scure. La pelle scura e il pelo chiaro — i due casi che
      di solito si rifiutano — qui si lavorano.</p>
    </div>
  </div>
</section>

<section>
  <div class="dentro">
    <h2>Afrodite VS++</h2>
    <p class="guida">Rimodellamento corpo, cellulite, ritenzione, tono. Quattro tecnologie
    in una macchina sola — e una rata sola.</p>
    <table>
      <tr><th>Tecnologia</th><th>Dove lavora</th></tr>
      <tr><td>Cavitazione</td><td>1 MHz, fino a 50 W — adiposità localizzata</td></tr>
      <tr><td>Radiofrequenza</td><td>1,2 MHz bipolare e multipolare, fino a 50 W — tono e compattezza</td></tr>
      <tr><td>Vacuum</td><td>fino a 350 mmHg, pulsazione 1–15 Hz — drenaggio e cellulite</td></tr>
      <tr><td>LED</td><td>rosso 630 nm collagene · blu 430 nm pelle impura</td></tr>
      <tr><td>Manipoli</td><td>Grande, medio, piccolo e cavitazione</td></tr>
      <tr><td>Interfaccia</td><td>Colonna con touch LCD 10,2"</td></tr>
    </table>
    <div class="nota verde">
      <span class="eti">Non arriva da sola</span>
      <p>Con Afrodite arriva il <b>metodo DEMETRA</b>: ciclo di 10-12 sedute, scheda di
      valutazione da compilare in cabina e protocollo scritto fase per fase. È la differenza
      fra una macchina che lavora e una che dopo tre mesi finisce sotto un telo.</p>
    </div>
  </div>
</section>

<section>
  <div class="dentro">
    <h2>Quale delle due</h2>
    <p>Dipende da cosa ti manca in agenda, non da cosa è più bello. È la prima cosa che
    guardiamo insieme nei tre minuti al telefono: se non ti serve, te lo diciamo.</p>
  </div>
</section>

{chiamata("Quale ti serve davvero?")}''')

# ======================= METODO =======================
pagina('metodo.html',
 'Come lavoriamo · NIPEC — formazione, protocolli, assistenza',
 "Con la macchina arrivano il protocollo scritto, la formazione in sede e l'assistenza. Se si ferma, macchina sostitutiva entro 48 ore.",
f'''<section class="apre">
  <div class="dentro">
    <p class="occhiello">Come lavoriamo</p>
    <h1>Una macchina che non sai usare è un mobile costoso</h1>
    <p class="sotto">Per questo non ti lasciamo sola con la macchina. Lasciarti sola è il
    modo più veloce per vedersela restituire.</p>
  </div>
</section>

<section>
  <div class="dentro">
    <h2>Cosa arriva insieme alla macchina</h2>
    <ul class="spunte">
      <li><b>La formazione, in sede.</b> Il giorno della consegna, con le operatrici che ci
      sono. È compresa nel canone.</li>
      <li><b>Il protocollo scritto.</b> Cosa si fa dal momento in cui la cliente entra a
      quando esce: i controlli prima, i parametri, la seduta, cosa si dice dopo, e ogni
      quanto si richiama.</li>
      <li><b>La scheda di cabina.</b> Una facciata da appendere: il semaforo delle
      controindicazioni, i parametri delle fasi, i prodotti.</li>
      <li><b>La scheda cliente.</b> Da compilare seduta per seduta, con le misure alle
      sedute 1, 5 e 10 — quelle che tengono la cliente al quinto appuntamento.</li>
      <li><b>Un riferimento con nome e cognome.</b> Non un call center.</li>
    </ul>
  </div>
</section>

<section>
  <div class="dentro">
    <h2>Se la macchina si ferma</h2>
    <p class="guida">È la domanda da fare a chiunque ti noleggi qualcosa.</p>
    <div class="due">
      <div class="scheda">
        <span class="num">Entro 48 ore</span>
        <h3>Te ne arriva un'altra</h3>
        <p>Non chiudi un'ora, non disdici nessuna cliente, non spieghi niente a nessuno.</p>
      </div>
      <div class="scheda">
        <span class="num">Prima ancora</span>
        <h3>Quattro controlli al telefono</h3>
        <p>Metà delle volte non è guasta: manca corrente, il manipolo non è collegato fino
        in fondo, o il tubo è sporco di gel. Li facciamo insieme in due minuti.</p>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="dentro">
    <h2>I tre minuti</h2>
    <p>Prima di proporti qualunque macchina ti facciamo otto domande sul tuo giro clienti.
    Non è un sondaggio: alla fine hai in mano un numero che oggi non hai — quanto esce dalla
    tua cassa ogni anno per le clienti che nessuno ha richiamato.</p>
    <p>Se da quel numero esce che non ti serve una macchina, te lo diciamo. Capita.</p>
  </div>
</section>

{chiamata("Facciamo i tre minuti?")}''')

# ======================= CONTATTI =======================
pagina('contatti.html',
 'Contatti · NIPEC — Italia e Albania',
 'Parliamone su WhatsApp. Italia: 351 846 6025. Albania: +355 69 212 9786.',
f'''<section class="apre">
  <div class="dentro">
    <p class="occhiello">Contatti</p>
    <h1>Scrivici su WhatsApp</h1>
    <p class="sotto">Rispondiamo noi, non un centralino. Il primo messaggio non è un
    preventivo: sono tre minuti di domande sul tuo centro.</p>
  </div>
</section>

<section>
  <div class="dentro">
    <div class="due">
      <div class="scheda">
        <span class="num">Italia</span>
        <h3>Giorgio</h3>
        <p style="margin-bottom:14px">Lazio e resto d'Italia.</p>
        <a class="btn" href="{WA_IT}">351 846 6025</a>
      </div>
      <div class="scheda">
        <span class="num">Shqipëri</span>
        <h3>Uarda</h3>
        <p style="margin-bottom:14px">Tiranë dhe gjithë Shqipëria.</p>
        <a class="btn" href="{WA_AL}">+355 69 212 9786</a>
      </div>
    </div>

    <div class="nota" style="margin-top:24px">
      <span class="eti">Cosa succede dopo che ci scrivi</span>
      <p>Ti rispondiamo e ti proponiamo una chiamata di tre minuti. Otto domande sul tuo
      giro clienti, rispondi di pancia. Alla fine hai un numero in mano e decidi tu se
      andare avanti. <b>Quel giorno non ti vendiamo niente.</b></p>
    </div>
  </div>
</section>

<section>
  <div class="dentro">
    <h2>Dati societari</h2>
    <table>
      <tr><td>Ragione sociale</td><td><span style="color:#B45309">da completare</span></td></tr>
      <tr><td>Sede</td><td><span style="color:#B45309">da completare</span></td></tr>
      <tr><td>Partita IVA</td><td><span style="color:#B45309">da completare</span></td></tr>
      <tr><td>E-mail</td><td><span style="color:#B45309">da completare</span></td></tr>
      <tr><td>Assistenza Italia</td><td>351 846 6025</td></tr>
      <tr><td>Assistenza Albania</td><td>+355 69 212 9786</td></tr>
    </table>
  </div>
</section>''')

# ======================= PRIVACY =======================
pagina('privacy.html',
 'Informativa privacy · NIPEC',
 'Come trattiamo i dati di chi ci scrive o naviga su nipecestetica.eu.',
'''<section class="apre">
  <div class="dentro">
    <p class="occhiello">Informativa</p>
    <h1>Privacy</h1>
    <p class="sotto">In breve: questo sito non ti profila, non ha moduli e non installa
    cookie di tracciamento. Se ci scrivi su WhatsApp, i tuoi dati li usiamo per
    risponderti.</p>
  </div>
</section>

<section>
  <div class="dentro">
    <h2>Chi tratta i dati</h2>
    <table>
      <tr><td>Titolare del trattamento</td><td><span style="color:#B45309">ragione sociale, sede e P.IVA da completare</span></td></tr>
      <tr><td>Contatto</td><td><span style="color:#B45309">e-mail da completare</span> · 351 846 6025</td></tr>
    </table>

    <h2>Quali dati, e perché</h2>
    <ul class="spunte">
      <li><b>Se ci scrivi su WhatsApp</b> — numero, nome e il contenuto del messaggio.
      Servono a risponderti e a seguire la richiesta. Base giuridica: riscontro alla tua
      richiesta e, dove serve, esecuzione di misure precontrattuali.</li>
      <li><b>Se navighi</b> — il server registra indirizzo IP, data, pagina e tipo di
      browser, come fa qualunque server web. Servono alla sicurezza e al funzionamento del
      sito.</li>
      <li><b>Se arrivi da un'inserzione</b> — la piattaforma pubblicitaria (Meta) tratta
      dati suoi secondo la propria informativa. Noi riceviamo soltanto il tuo messaggio.</li>
    </ul>

    <h2>Cookie</h2>
    <p>Questo sito <b>non usa cookie di profilazione</b> e non ha strumenti di statistica di
    terze parti. I caratteri e le immagini sono serviti dal nostro stesso dominio: nessuna
    richiesta parte verso servizi esterni mentre leggi queste pagine.</p>

    <h2>Per quanto li teniamo</h2>
    <p>Le conversazioni restano finché serve a gestire il rapporto, e comunque non oltre il
    tempo necessario alle finalità per cui sono state raccolte. I registri del server
    seguono i tempi tecnici del fornitore di hosting.</p>

    <h2>A chi li comunichiamo</h2>
    <p>A nessuno, se non ai fornitori tecnici che ci permettono di lavorare — hosting e
    servizio di messaggistica — e a chi la legge ci obbliga. <b>Non vendiamo e non cediamo
    dati a terzi.</b></p>

    <h2>I tuoi diritti</h2>
    <p>Puoi chiederci in ogni momento di accedere ai tuoi dati, correggerli, cancellarli,
    limitarne il trattamento od opporti. Basta scriverci ai contatti qui sopra.</p>
    <p>Se ritieni che il trattamento non sia corretto puoi rivolgerti all'autorità di
    controllo: in <b>Italia</b> il Garante per la protezione dei dati personali
    (<a href="https://www.garanteprivacy.it">garanteprivacy.it</a>); in <b>Albania</b> il
    Komisioneri për të Drejtën e Informimit dhe Mbrojtjen e të Dhënave Personale
    (<a href="https://www.idp.al">idp.al</a>).</p>

    <div class="nota">
      <span class="eti">Ultimo aggiornamento</span>
      <p>Ottobre 2026. Se cambia qualcosa, lo scriviamo qui.</p>
    </div>
  </div>
</section>''')

print('pagine scritte:', ', '.join(f for f,_ in PAGINE), '+ privacy.html')
