#!/usr/bin/env python3
"""Le brochure NIPEC: Uriel, Ares, Afrodite, Hermes. A4, quattro pagine ciascuna, nello stile del sito www.nipecestetica.eu.

I testi vengono dal sito (SITO/pubblica: laser-ares, laser-uriel, afrodite, metodo, formazione) e, per Hermes, dal depliant e dal manuale d'uso
del produttore (ERMES Slim, Drive). Niente prezzi. Si dice «dispositivo», non «macchina».

Uso:  python3 fai-brochure.py
"""
import html, os, re, subprocess

QUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(QUI)
CHROME = next(p for p in ('/opt/pw-browsers/chromium-1243/chrome-linux64/chrome', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome') if os.path.exists(p))
FONT = os.path.join(REPO, 'SITO', 'pubblica', 'caratteri', 'archivo.woff2')
IMG = os.path.join(REPO, 'SITO', 'pubblica', 'immagini')
FOTO = os.path.join(REPO, 'schede', 'LASER', 'foto')
EDIZIONE = 'novembre 2026'

def esc(t): return html.escape(t, quote=False)

def svg(nome):
    s = open(os.path.join(REPO, 'MARCHIO', nome), encoding='utf8').read()
    return re.sub(r'<title>.*?</title>', '', s, flags=re.S)
LOGO = svg('nipec-logo-orizzontale.svg').replace('<svg ', '<svg class="logo" ', 1)
LOGO_NEG = svg('nipec-logo-orizzontale-negativo.svg').replace('<svg ', '<svg class="logo" ', 1)
EMBL_NEG = re.sub(r'^<svg[^>]*>|</svg>\s*$', '', svg('nipec-emblema-negativo.svg').strip()).strip()

CSS = '''
@font-face{font-family:"Archivo";src:url("%(font)s") format("woff2");font-weight:100 900}
:root{--navy:#123A63;--blu:#1C6EA4;--chiaro:#5AA6D6;--testo:#4A5B6E;--ink:#0F2B4A;--velo:#EEF3F8;--velo2:#E6EFF8;--riga:#DCE4EC;--scuro:#0B2545}
@page{size:A4;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#fff}
body{font-family:"Archivo","Helvetica Neue",Arial,sans-serif;color:var(--testo);font-size:9.6pt;line-height:1.55;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:210mm;height:297mm;position:relative;overflow:hidden;page-break-after:always;padding:13mm 15mm 0}
.testa{display:flex;justify-content:space-between;align-items:center;padding-bottom:5mm;border-bottom:1px solid var(--riga);margin-bottom:8mm}
.testa .logo{height:11mm;width:auto}
.testa .et{font-size:7.2pt;letter-spacing:.14em;text-transform:uppercase;color:var(--blu);font-weight:600}
.piede{position:absolute;left:15mm;right:15mm;bottom:8mm;display:flex;justify-content:space-between;font-size:7.4pt;color:#7B8A9A;border-top:1px solid var(--riga);padding-top:3mm}
.eyebrow{font-size:7.4pt;letter-spacing:.17em;text-transform:uppercase;color:var(--blu);font-weight:600;margin-bottom:3mm}
h1{font-size:52pt;line-height:1.02;font-weight:700;color:var(--navy);letter-spacing:-.025em}
h1 small{display:block;font-size:17pt;font-weight:500;letter-spacing:-.005em;color:var(--blu);margin-top:2mm}
h2{font-size:21pt;line-height:1.12;font-weight:700;color:var(--navy);letter-spacing:-.015em;margin-bottom:4mm}
h3{font-size:11.5pt;line-height:1.25;font-weight:700;color:var(--navy);margin-bottom:1.5mm}
.lead{font-size:17pt;line-height:1.28;color:var(--navy);margin:6mm 0 5mm;font-weight:500}
.lead .acc{color:var(--blu)}
p{margin-bottom:3mm}
.pills{display:flex;flex-wrap:wrap;gap:2mm;margin:4mm 0 0}
.pill{border:1px solid var(--navy);color:var(--navy);border-radius:20px;padding:1.2mm 3.4mm;font-size:8pt;font-weight:500}
.foto{background:var(--velo);border-radius:5mm;display:flex;align-items:center;justify-content:center;overflow:hidden;position:relative}
.foto img{mix-blend-mode:multiply;display:block}
.banda{position:absolute;left:0;right:0;bottom:0;height:34mm;background:var(--navy);color:#fff;padding:0 15mm;display:flex;align-items:center;justify-content:space-between;gap:10mm}
.banda .frase{font-size:15pt;line-height:1.25;font-weight:600;max-width:105mm}
.banda .sito{font-size:9pt;letter-spacing:.05em;color:#BFD7EC;text-align:right;line-height:1.7}
.banda .sito b{color:#fff;font-weight:600;font-size:10.5pt}
.sez{margin-bottom:9mm}
.due{display:grid;grid-template-columns:1fr 1fr;gap:5mm}
.tre{display:grid;grid-template-columns:1fr 1fr 1fr;gap:5mm}
.card{background:var(--velo);border-radius:4mm;padding:5mm 5.5mm}
.card.bianca{background:#fff;border:1px solid var(--riga)}
.card.navy{background:var(--navy);color:#DDE9F5}
.card.navy h3{color:#fff}
.card.navy .eyebrow{color:#9CCBE8}
.card .eyebrow{margin-bottom:2mm}
.card ul,.col ul{list-style:none;margin-top:2mm}
.card li,.col li{position:relative;padding-left:4mm;margin-bottom:1.2mm;font-size:9pt}
.card li:before,.col li:before{content:"";position:absolute;left:0;top:2.1mm;width:1.4mm;height:1.4mm;border-radius:50%;background:var(--blu)}
.card.navy li:before{background:#9CCBE8}
.col{border-top:2px solid var(--blu);padding-top:3.5mm}
.col h3{font-size:10.5pt}
.col p{font-size:9pt;margin:0}
table{width:100%;border-collapse:separate;border-spacing:0;border:1px solid var(--riga);border-radius:3mm;overflow:hidden;font-size:9pt}
th{background:var(--navy);color:#fff;text-align:left;font-weight:600;padding:2.6mm 4mm;font-size:8.6pt}
td{padding:2.3mm 4mm;border-top:1px solid var(--riga);vertical-align:top}
td:first-child{color:#6B7C8F;width:30%}
td b{color:var(--ink);font-weight:600}
tr:nth-child(even) td{background:#FAFCFE}
.passi{display:grid;grid-template-columns:1fr 1fr;gap:5mm 7mm}
.passo{display:flex;gap:4mm}
.passo .n{flex:none;width:9mm;height:9mm;border-radius:50%;background:var(--navy);color:#fff;font-weight:700;font-size:9pt;display:flex;align-items:center;justify-content:center;margin-top:.5mm}
.passo h3{margin-bottom:1mm}
.passo p{font-size:8.8pt;margin-bottom:1.5mm}
.passo ul{list-style:none}
.passo li{font-size:8.5pt;padding-left:3.5mm;position:relative;margin-bottom:.6mm}
.passo li:before{content:"";position:absolute;left:0;top:1.9mm;width:1.2mm;height:1.2mm;border-radius:50%;background:var(--blu)}
.cta{background:var(--navy);color:#DDE9F5;border-radius:5mm;padding:7mm 8mm;display:flex;justify-content:space-between;align-items:center;gap:8mm}
.cta h2{color:#fff;font-size:17pt;margin-bottom:2mm}
.cta p{margin:0;font-size:9.4pt}
.cta .bottone{flex:none;background:#fff;color:var(--navy);border-radius:20px;padding:3mm 6mm;font-weight:600;font-size:9.4pt;text-align:center}
.contatti{display:grid;grid-template-columns:1.1fr 1.1fr 1fr;gap:6mm;margin-top:8mm;font-size:8.6pt}
.contatti .eyebrow{margin-bottom:1.5mm}
.contatti p{margin-bottom:1mm;color:var(--testo)}
.contatti b{color:var(--ink);font-weight:600}
.firma{position:absolute;left:0;right:0;bottom:0;background:var(--scuro);color:#9FB4CB;padding:5mm 15mm 7mm;font-size:7.6pt;display:flex;justify-content:space-between;gap:6mm}
.firma .logo{height:8mm;width:auto}
.nota{font-size:7.8pt;color:#7B8A9A}
.tappe{display:grid;grid-template-columns:repeat(5,1fr);gap:4mm;margin-top:8mm}
.tappa{border-top:2px solid var(--blu);padding-top:3mm}
.tappa .q{font-size:15pt;font-weight:700;color:var(--navy);letter-spacing:-.01em;line-height:1.1}
.tappa h3{font-size:9.6pt;margin:1.5mm 0 1mm}
.tappa p{font-size:8.2pt;line-height:1.45;margin:0}
.chip{display:inline-block;background:var(--velo2);color:var(--navy);border-radius:20px;padding:1.5mm 4mm;margin:0 1.5mm 2mm 0;font-size:8.8pt;font-weight:500}
.grande{font-size:26pt;font-weight:700;color:var(--blu);letter-spacing:-.02em;line-height:1}
.red{border-color:#E7C7C0;background:#FBF1EF}
'''

CONTATTI = '''<div class="contatti">
<div><div class="eyebrow">Scrivici</div><p><b>WhatsApp +39 351 846 6025</b></p><p>Numero verde 800 141 726</p><p>info@nipecestetica.com</p></div>
<div><div class="eyebrow">Dove siamo</div><p>Via Rovetta 29, 25080 Padenghe sul Garda (BS)</p><p>Rruga Donika Kastrioti 3, Tiranë · +355 69 212 9786</p></div>
<div><div class="eyebrow">Online</div><p><b>www.nipecestetica.eu</b></p><p>Il metodo · La formazione · Il catalogo</p></div>
</div>'''

PASSI = [
    ('Analisi', "Prima di parlare di dispositivi guardiamo il tuo centro: chi sono le clienti, quante cabine hai, quanto costa un'ora di lavoro, cosa vendi già.",
     ['Questionario e visita (o videochiamata)', 'Lettura di listino e agenda', 'Dove sta il margine che oggi perdi']),
    ('Progettazione', "Scegliamo insieme la tecnologia giusta e costruiamo il trattamento intorno: prezzi, pacchetti, durata delle sedute, formula di acquisto.",
     ['Dispositivo e configurazione', 'Listino trattamenti e pacchetti', 'Vendita o noleggio, con i numeri sul tavolo']),
    ('Formazione', "Consegna pratica in cabina e un percorso a tappe che finisce con un esame. L'operatrice esce con un certificato valido 12 mesi.",
     ['Giorno 0 in cabina, +7 richiamo, +21 online', 'Esame a +45 giorni', 'Protocolli e card delle regole, in italiano e albanese']),
    ('Supporto continuo', "Dopo la consegna restiamo. Un referente unico per il tuo centro, assistenza diretta e un controllo mensile per prevenire il fermo del dispositivo.",
     ['Videochiamata mensile di 10 minuti', 'Sostituzione pezzi e logistica', 'Campagna marketing di avvio']),
]

def testa(nome): return f'<div class="testa">{LOGO}<span class="et">Brochure · {nome} · edizione {EDIZIONE}</span></div>'
def piede(nome, n): return f'<div class="piede"><span>NIPEC · Tecnologie Estetiche — www.nipecestetica.eu</span><span>{nome} · {n}/4</span></div>'

def pagina(nome, n, corpo, intesta=True, con_piede=True):
    return f'<section class="page">{testa(nome) if intesta else ""}{corpo}{piede(nome, n) if con_piede else ""}</section>'

def pill(lista): return '<div class="pills">' + ''.join(f'<span class="pill">{esc(x)}</span>' for x in lista) + '</div>'

def copertina(d):
    foto = d.get('foto')
    cornice = (f'<div class="foto" style="height:{d.get("altezza", 108)}mm;margin-top:7mm"><img src="{foto}" style="max-height:{d.get("img_h", 92)}mm;max-width:{d.get("img_w", 120)}mm"></div>'
               if foto else f'<div class="foto" style="height:{d.get("altezza", 108)}mm;margin-top:7mm;background:var(--navy)">{d["grafica"]}</div>')
    sotto = f'<small>{esc(d["sotto"])}</small>' if d.get('sotto') else ''
    corpo = (f'<div class="eyebrow">{esc(d["eyebrow"])}</div><h1>{esc(d["nome"])}{sotto}</h1>'
             f'<div class="lead">{d["lead"]}</div><p style="max-width:165mm;font-size:10.4pt;line-height:1.6">{esc(d["intro"])}</p>{pill(d["pill"])}{cornice}'
             f'<div class="banda"><div class="frase">Non vendiamo dispositivi.<br>Costruiamo sistemi di lavoro.</div>'
             f'<div class="sito"><b>www.nipecestetica.eu</b><br>WhatsApp +39 351 846 6025</div></div>')
    return corpo

def tabella(righe, intestazioni):
    th = ''.join(f'<th>{esc(h)}</th>' for h in intestazioni)
    tr = ''.join('<tr>' + ''.join(f'<td>{c if i else esc(c)}</td>' for i, c in enumerate(r)) + '</tr>' for r in righe)
    return f'<table><tr>{th}</tr>{tr}</table>'

def passi():
    return ('<div class="passi">' + ''.join(
        f'<div class="passo"><div class="n">{i:02d}</div><div><h3>{esc(t)}</h3><p>{esc(p)}</p><ul>' + ''.join(f'<li>{esc(b)}</li>' for b in bl) + '</ul></div></div>'
        for i, (t, p, bl) in enumerate(PASSI, 1)) + '</div>')

TAPPE = [('Giorno 0', 'Consegna pratica', 'In cabina, sul dispositivo del centro, con clienti vere.'), ('+7', 'Richiamo', 'Si correggono le abitudini sbagliate della prima settimana.'),
         ('+21', 'Online', 'Protocolli avanzati e casi reali portati dalle operatrici.'), ('+45', 'Esame', 'Prova pratica e test scritto di 20 domande.'),
         ('12 mesi', 'Certificato', 'Attestato nominale da esporre in centro. Si rinnova ogni anno.')]
def percorso():
    return ('<div class="eyebrow" style="margin-top:9mm">Il percorso di certificazione</div><div class="tappe" style="margin-top:3mm">' +
            ''.join(f'<div class="tappa"><div class="q">{esc(q)}</div><h3>{esc(t)}</h3><p>{esc(x)}</p></div>' for q, t, x in TAPPE) + '</div>')

def ultima(d, n=4):
    cta = (f'<div class="cta"><div><h2>{esc(d["cta_t"])}</h2><p>{esc(d["cta_p"])}</p></div><div class="bottone">{esc(d["cta_b"])}</div></div>')
    corpo = (f'<div class="eyebrow">Il metodo NIPEC</div><h2>Un processo che non si ferma alla consegna.</h2>'
             f'<p style="max-width:150mm;margin-bottom:7mm">Il dispositivo è l\'inizio. Quello che fa lavorare un centro è quello che viene dopo: i protocolli, l\'operatrice formata, qualcuno che risponde. Per questo lavoriamo in quattro tappe.</p>'
             f'{passi()}{percorso()}<div style="margin-top:9mm">{cta}</div>{CONTATTI}'
             f'<div class="firma">{LOGO_NEG}<span>© 2026 NIPEC · Tecnologie Estetiche — PHD System Srl · P. IVA 04696530981<br>Il dispositivo è venduto o noleggiato dopo l\'analisi del centro. Le caratteristiche possono variare con gli aggiornamenti.</span></div>')
    return pagina(d['nome_breve'], n, corpo, con_piede=False)

# =============================== ARES ===============================
ARES = dict(
    nome='Laser Ares', nome_breve='Ares', file='ARES', eyebrow='Epilazione laser · Diodo 808 nm',
    lead='Il laser non ti porta la cliente una volta. <span class="acc">Te la porta dodici.</span>',
    intro="Ma solo se il dispositivo non si ferma e i parametri sono giusti. Ares è il diodo 808 su cui lavorano già molti centri: 10 diodi, 1500 W, testina in titanio. Nella versione 2026 la telecamera e il software IA ti propongono i parametri, e tu controlli.",
    pill=['808 nm', '1500 W · 10 diodi', 'CE italiana · MDR', 'Vendita o noleggio'],
    foto='../SITO/pubblica/immagini/e493bbb796de.jpg', altezza=124, img_h=112,
    cta_t='Hai già una Ares 2025?', cta_p='Non hai un dispositivo inferiore: hai lo stesso dispositivo con meno aiuti. Valutiamo la permuta verso la 2026.', cta_b='Chiedi una valutazione',
)
def ares_pagine():
    d = ARES; nome = d['nome_breve']
    p1 = pagina(nome, 1, copertina(d), con_piede=False)
    p2 = pagina(nome, 2,
        '<div class="sez"><div class="eyebrow">Due versioni</div><h2>Stesso dispositivo.<br>Cambia chi fa i conti.</h2>'
        '<p style="max-width:150mm;margin-bottom:5mm">Le due Ares hanno lo stesso motore: stessi diodi, stessi watt, stessa testina. Sulla 2025 imposti tu Joule, millisecondi e Hertz. Sulla 2026 li calcola il software. Chi sa lavorare sulla 2025 impara la 2026 in mezza giornata.</p>'
        '<div class="due"><div class="card bianca"><div class="eyebrow">Quella che molti hanno già</div><h3 style="font-size:15pt">Ares 2025</h3>'
        '<div class="foto" style="height:38mm;margin:3mm 0;background:#fff"><img src="../schede/LASER/foto/ares-2025.jpg" style="max-height:36mm"></div>'
        '<p style="font-size:9pt">Diodo 808, lavoro pieno, comandi a mano. Pannello manuale: Joule, millisecondi, Hertz.</p><ul><li>10 diodi da 100 W · 1500 W</li><li>Niente telecamera, niente IA</li><li>Valutata anche in permuta</li></ul></div>'
        '<div class="card navy"><div class="eyebrow">Il passo avanti</div><h3 style="font-size:15pt">Ares 2026 · IA</h3>'
        '<div class="foto" style="height:38mm;margin:3mm 0;background:#fff"><img src="../schede/LASER/foto/ares-2026.jpg" style="max-height:36mm"></div>'
        '<p style="font-size:9pt;color:#DDE9F5">La telecamera guarda pelle e pelo, il software propone griglia, kJ target e fluenza. Il dispositivo non parte da solo: decidi sempre tu.</p><ul><li>Telecamera integrata e software IA</li><li>Modalità HR / SHR / SHR Stack</li><li>Gestione e alimentazione digitali</li></ul></div></div></div>'
        '<div class="sez"><div class="eyebrow">In cabina</div><h2>Cosa cambia per te, in pratica.</h2><div class="tre">'
        '<div class="col"><h3>Il colpo cento è uguale al primo</h3><p>L\'elettronica tiene ferma la corrente ai diodi anche se la rete del negozio balla. La cliente non ti dice più «oggi l\'ho sentito di più».</p></div>'
        '<div class="col"><h3>L\'operatrice nuova lavora bene dal primo giorno</h3><p>Sulla 2026 il software propone i parametri a partire da quello che vede la telecamera. Tu non devi stare dietro a ogni impostazione.</p></div>'
        '<div class="col"><h3>La testina non si consuma</h3><p>Il titanio non si opacizza come le altre testine: è il pezzo che di solito si cambia e si paga.</p></div></div></div>')
    righe = [('Tipo', 'Laser a diodo', 'Laser a diodo'), ('Lunghezza d\'onda', '808 nm', '808 nm'), ('Diodi', '10 da 100 W', '10 da 100 W'), ('Potenza', '1500 W', '1500 W'),
             ('Emissione', '1–400 ms · macro canale', '1–400 ms · macro canale'), ('Raffreddamento', 'TECH cool con micro chip', 'TECH cool con micro chip'),
             ('Interfaccia', 'Pannello manuale: J · ms · Hz', 'Display touch digitale'), ('Telecamera e IA', 'No', 'Sì · HR / SHR / SHR Stack'), ('Testina', 'Titanio', 'Titanio'),
             ('Rete elettrica', 'AC 220 V / 110 V', 'AC 220 V / 110 V'), ('Sicurezza', 'Classe 4 · interlock', 'Classe 4 · interlock'),
             ('Certificazione', 'CE italiana · MDR', 'CE italiana · MDR'), ('Formato', 'Da banco', 'Da banco')]
    p3 = pagina(nome, 3,
        '<div class="sez"><div class="eyebrow">Scheda tecnica</div><h2>I dati ufficiali.</h2>' + tabella(righe, ['Caratteristica', 'Ares 2025', 'Ares 2026 · IA']) + '</div>'
        '<div class="due"><div class="card" style="background:var(--velo2)"><div class="eyebrow">Certificata in Italia</div><h3 style="font-size:13pt">CE italiana e MDR attivo.</h3>'
        '<p style="font-size:9pt;margin:0">Non è un dispositivo importato e rimarchiato. Fascicolo tecnico, dichiarazione di conformità e numero di serie sono rintracciabili: se arriva un controllo, c\'è una carta da mostrare con un nome e un indirizzo dietro.</p></div>'
        '<div class="card" style="background:var(--velo2)"><div class="eyebrow">Laser di classe 4</div><h3 style="font-size:13pt">Un laser vero, trattato come tale.</h3>'
        '<p style="font-size:9pt;margin:0">Occhiali sempre, chiave e interlock che spegne il dispositivo se qualcosa non è a posto. Lo insegniamo alla consegna e lo verifichiamo all\'esame.</p></div></div>')
    return [p1, p2, p3, ultima(d)]

# =============================== URIEL ===============================
URIEL = dict(
    nome='Laser Uriel', sotto='2026 · IA', nome_breve='Uriel', file='URIEL', eyebrow='Epilazione laser · Top di gamma',
    lead='Non dici più di no a nessuno. <span class="acc">E quello che prima rifiutavi, lo fatturi.</span>',
    intro="Tre lunghezze d'onda sullo stesso manipolo: 755, 808 e 1064 nm. Pelle scura e pelo chiaro, i due casi che di solito si mandano via, qui si lavorano. Fino a 2000 W per fare le zone grandi in meno passaggi.",
    pill=['755 / 808 / 1064 nm', 'Fino a 2000 W · 16 diodi', 'Telecamera + IA', 'CE italiana · MDR'],
    foto='../schede/LASER/foto/uriel-2026.jpg', altezza=124, img_h=112,
    cta_t='Parti con i diodi che ti servono oggi.', cta_p='I diodi si aggiungono quando il centro cresce, senza cambiare dispositivo. Progettiamo la configurazione insieme.', cta_b='Progettiamo la configurazione',
)
def uriel_pagine():
    d = URIEL; nome = d['nome_breve']
    p1 = pagina(nome, 1, copertina(d), con_piede=False)
    p2 = pagina(nome, 2,
        '<div class="sez"><div class="eyebrow">Tre bande, tre clienti</div><h2>Un solo manipolo<br>per ogni pelle.</h2><div class="tre">'
        '<div class="card"><div class="grande">755 nm</div><h3 style="margin-top:3mm">Pelo sottile e chiaro</h3><p style="font-size:9pt;margin:0">Prende il pelo che gli altri dispositivi lasciano lì.</p></div>'
        '<div class="card" style="background:var(--navy);color:#DDE9F5"><div class="grande" style="color:#9CCBE8">808 nm</div><h3 style="margin-top:3mm;color:#fff">Il cavallo di battaglia</h3><p style="font-size:9pt;margin:0">La banda che lavora la maggior parte delle clienti, tutti i giorni.</p></div>'
        '<div class="card"><div class="grande">1064 nm</div><h3 style="margin-top:3mm">Pelli scure</h3><p style="font-size:9pt;margin:0">Scende più in profondità e lavora in sicurezza sui fototipi alti.</p></div></div></div>'
        '<div class="sez"><div class="eyebrow">In cabina</div><h2>Cosa cambia per te, in pratica.</h2><div class="tre">'
        '<div class="col"><h3>Più clienti nella stessa giornata</h3><p>500 W in più della Ares: gambe intere, schiena e addome in meno passaggi, a parità di risultato.</p></div>'
        '<div class="col"><h3>Si ferma meno a raffreddare</h3><p>Radiatore, aria e TEC cool insieme. Più diodi vuol dire meno fatica per il dispositivo.</p></div>'
        '<div class="col"><h3>Parametri proposti, decisione tua</h3><p>Telecamera e software IA leggono pelle e pelo e propongono l\'impostazione. Tu confermi.</p></div></div></div>'
        '<div class="sez"><div class="eyebrow">Uriel e Ares, in breve</div>'
        + tabella([('Lunghezze d\'onda', '755 / 808 / 1064 nm', '808 nm'), ('Diodi', 'Fino a 16 da 100 W', '10 da 100 W'), ('Potenza', '2000 W', '1500 W'), ('Formato', 'Carrellata', 'Da banco')], ['', 'Uriel 2026 · IA', 'Ares']) + '</div>')
    righe = [('Tipo', 'Laser a diodo tri-onda'), ('Lunghezze d\'onda', '755 / 808 / 1064 nm, fino a 3 bande sullo stesso manipolo'), ('Diodi', 'Fino a 16 da 100 W'), ('Potenza', '2000 W'),
             ('Frequenza', '1–10 Hz'), ('Emissione', '1–400 ms · macro canale'), ('Raffreddamento', 'Radiatore + aria + TEC cool'), ('Interfaccia', 'Touch LCD 15"'),
             ('Telecamera e IA', 'Sì'), ('Testina', 'Titanio'), ('Rete elettrica', 'AC 220 V / 110 V'), ('Sicurezza', 'Classe 4 · interlock'), ('Certificazione', 'CE italiana · MDR'), ('Formato', 'Carrellata')]
    p3 = pagina(nome, 3,
        '<div class="sez"><div class="eyebrow">Scheda tecnica</div><h2>I dati ufficiali.</h2>' + tabella(righe, ['Caratteristica', 'Uriel 2026 · IA']) + '</div>'
        '<div class="due"><div class="card" style="background:var(--velo2)"><div class="eyebrow">Certificato in Italia</div><h3 style="font-size:13pt">CE italiana e MDR attivo.</h3>'
        '<p style="font-size:9pt;margin:0">Non è un dispositivo importato e rimarchiato. Fascicolo tecnico, dichiarazione di conformità e numero di serie sono rintracciabili: se arriva un controllo, c\'è una carta da mostrare con un nome e un indirizzo dietro.</p></div>'
        '<div class="card" style="background:var(--velo2)"><div class="eyebrow">Laser di classe 4</div><h3 style="font-size:13pt">Un laser vero, trattato come tale.</h3>'
        '<p style="font-size:9pt;margin:0">Occhiali sempre, chiave e interlock che spegne il dispositivo se qualcosa non è a posto. Lo insegniamo alla consegna e lo verifichiamo all\'esame.</p></div></div>')
    return [p1, p2, p3, ultima(d)]

# =============================== AFRODITE ===============================
AFRODITE = dict(
    nome='Afrodite VS++', nome_breve='Afrodite', file='AFRODITE', eyebrow='Corpo e dimagrimento · Viso',
    lead='Non ti serve un dispositivo. <span class="acc">Ti serve un progetto che vince.</span>',
    intro="Una colonna professionale con display touch da 10\" e manipoli per corpo e viso. Le tecnologie lavorano insieme su adipe, cellulite, tono e contorno. Con Afrodite arrivano i protocolli pronti e il percorso per lanciare il trattamento corpo nel tuo centro, anche se parti da zero.",
    pill=['Viso + corpo', 'Display touch 10"', 'Certificato CE', 'Protocolli IT · SQ'],
    foto='../SITO/pubblica/immagini/741b069dc662.jpg', altezza=124, img_h=118, img_w=100,
    cta_t='Vuoi lanciare il corpo nel tuo centro?', cta_p='Vendita o noleggio. Ti mostriamo i numeri prima di firmare.', cta_b='Prenota una consulenza',
)
def afrodite_pagine():
    d = AFRODITE; nome = d['nome_breve']
    p1 = pagina(nome, 1, copertina(d), con_piede=False)
    tec = [('Ultrasuono focalizzato direzionale', "Agisce sull'adipe sottocutaneo, dove si accumula il grasso localizzato."), ('Radiofrequenza', 'Scalda i tessuti in profondità: sostiene il collagene e il tono della pelle.'),
           ('Vacuum', 'Aspirazione e rilascio: drenaggio, circolazione, contorno di corpo e viso.'), ('Micropulse', 'Vibrazione a impulsi che rende il massaggio profondo ma confortevole.'), ('Low laser', '')]
    cards = ''.join(f'<div class="col"><h3>{esc(t)}</h3><p>{esc(x)}</p></div>' for t, x in tec[:3])
    cards2 = ''.join(f'<div class="col"><h3>{esc(t)}</h3><p>{esc(x)}</p></div>' for t, x in tec[3:]) + '<div></div>'
    chips = ''.join(f'<span class="chip">{esc(x)}</span>' for x in ["Riduzione dell'adipe localizzato", 'Cellulite', 'Rassodamento della pelle', 'Rimodellamento del corpo', 'Drenaggio', 'Trattamenti viso'])
    p2 = pagina(nome, 2,
        '<div class="sez"><div class="eyebrow">Le tecnologie</div><h2>Ognuna fa una cosa.<br>Insieme fanno il trattamento.</h2>'
        f'<div class="tre" style="row-gap:7mm">{cards}{cards2}</div></div>'
        '<div class="sez"><div class="eyebrow">Cosa offri alle clienti</div><h2>Un listino corpo completo,<br>da un\'unica colonna.</h2>' + chips + '</div>'
        '<div class="card navy"><div class="eyebrow">Il progetto</div><h3 style="font-size:15pt">Un dispositivo, da solo, non riempie l\'agenda.</h3>'
        '<p style="margin:2mm 0 0;font-size:9.6pt;color:#DDE9F5">Quello che fa la differenza è il progetto: dispositivo giusto, protocolli pronti, un gestionale per fidelizzare e qualcuno accanto a te. Questo ti portiamo.</p></div>')
    scheda = [('Tipo', 'Colonna professionale per corpo e viso'), ('Display', 'Touch, 10"'), ('Tecnologie', 'Ultrasuono focalizzato direzionale · radiofrequenza · vacuum · Micropulse · low laser'),
              ('Manipoli', 'Corpo e viso'), ('Certificazione', 'CE'), ('Protocolli', 'In italiano e in albanese'), ('Formula', 'Vendita o noleggio')]
    p3 = pagina(nome, 3,
        '<div class="sez"><div class="eyebrow">Scheda</div><h2>In breve.</h2>' + tabella(scheda, ['Caratteristica', 'Afrodite VS++']) + '</div>'
        '<div class="sez"><div class="eyebrow">Il metodo DEMETRA</div><h2>Arriva con i compiti già fatti.</h2><div class="tre">'
        '<div class="col"><h3>Protocollo scritto</h3><p>Cosa fai, con quali parametri, in che ordine: pagina per pagina.</p></div>'
        '<div class="col"><h3>Scheda di valutazione</h3><p>Per seguire la cliente seduta dopo seduta e tenere il conto del percorso.</p></div>'
        '<div class="col"><h3>Ciclo di 10–12 sedute</h3><p>Il trattamento è un percorso, non una seduta sola. La scheda di cabina lo accompagna.</p></div></div></div>'
        '<div class="sez"><div class="eyebrow">Uso conforme</div><h2>Sei regole.<br>Il dispositivo dura il doppio.</h2>'
        '<p style="max-width:150mm;margin-bottom:5mm">La maggior parte dei guasti nasce dall\'uso, non dal dispositivo. Per questo ogni operatrice esce dalla formazione con la card delle 6 regole e un certificato da rinnovare ogni anno.</p>'
        '<div class="tre"><div class="card"><h3>Consegna in cabina</h3><p style="font-size:9pt;margin:0">Installazione, prime sedute guidate e verbale di consegna firmato.</p></div>'
        '<div class="card"><h3>Operatrice certificata</h3><p style="font-size:9pt;margin:0">Esame dopo 45 giorni, certificato valido 12 mesi.</p></div>'
        '<div class="card"><h3>Controllo mensile</h3><p style="font-size:9pt;margin:0">Dieci minuti in videochiamata per intercettare i problemi prima del fermo.</p></div></div></div>')
    return [p1, p2, p3, ultima(d)]

# =============================== HERMES ===============================
GRAFICA_HERMES = '''<svg viewBox="0 0 400 300" style="width:100%;height:100%" xmlns="http://www.w3.org/2000/svg">
<defs><radialGradient id="g" cx="50%" cy="50%" r="60%"><stop offset="0" stop-color="#1C6EA4" stop-opacity=".55"/><stop offset="1" stop-color="#123A63" stop-opacity="0"/></radialGradient></defs>
<rect width="400" height="300" fill="#123A63"/><circle cx="200" cy="150" r="170" fill="url(#g)"/>
<g fill="none" stroke="#9CCBE8" stroke-width="1.3">
<ellipse cx="200" cy="150" rx="26" ry="14" stroke-width="2.2" stroke="#fff"/><ellipse cx="200" cy="150" rx="54" ry="30" opacity=".95"/><ellipse cx="200" cy="150" rx="86" ry="48" opacity=".8"/>
<ellipse cx="200" cy="150" rx="122" ry="68" opacity=".6"/><ellipse cx="200" cy="150" rx="162" ry="90" opacity=".42"/><ellipse cx="200" cy="150" rx="206" ry="114" opacity=".26"/></g>
<g fill="#fff"><text x="200" y="262" text-anchor="middle" font-family="Archivo, Arial, sans-serif" font-size="13" letter-spacing="5" font-weight="600" fill="#BFD7EC">CAMPO ELETTROMAGNETICO FOCALIZZATO</text></g></svg>'''
HERMES = dict(
    nome='Hermes Slim', nome_breve='Hermes', file='HERMES', eyebrow='Corpo · Rimodellamento · Tecnologia HI-EMT',
    lead='Fa lavorare il muscolo in profondità. <span class="acc">Senza elettrodi, senza contatto elettrico.</span>',
    intro="Hermes Slim usa un campo elettromagnetico focalizzato (HI-EMT, detto anche HIFEM) che raggiunge i muscoli fino a 8 cm di profondità e li fa contrarre oltre quello che si ottiene con l'attività fisica normale. Non è un'elettrostimolazione. La seduta standard dura 30 minuti.",
    pill=['HI-EMT', 'Fino a 8 cm', 'Seduta da 30 minuti', 'Uno o due manipoli', 'Certificato CE'],
    grafica=GRAFICA_HERMES, altezza=124,
    cta_t='Vuoi portare Hermes nel tuo centro?', cta_p='Vendita o noleggio. Partiamo dall\'analisi del tuo centro e ti mostriamo i numeri prima di firmare.', cta_b='Chiedi la proposta',
)
def hermes_pagine():
    d = HERMES; nome = d['nome_breve']
    p1 = pagina(nome, 1, copertina(d), con_piede=False)
    conf = [('Come arriva l\'energia', 'Corrente attraverso elettrodi sulla pelle', 'Campo elettromagnetico focalizzato: <b>nessun elettrodo</b>'),
            ('Sensazione', 'Può dare pizzicore o bruciore', '<b>Nessun pizzicore o bruciore</b>'), ('Profondità', 'Strati superficiali', '<b>In profondità, fino a 8 cm</b>'),
            ('Fibre muscolari attivate', 'Meno fibre', '<b>Molte più fibre</b>'), ('Contrazione', 'Convenzionale', '<b>Supermassimale</b>'), ('L\'intensità è limitata da', 'Tolleranza della pelle', 'Tolleranza del muscolo')]
    chips1 = ''.join(f'<span class="chip">{x}</span>' for x in ['Addome', 'Glutei', 'Cosce', 'Interno coscia', 'Schiena'])
    chips2 = ''.join(f'<span class="chip" style="background:#fff;border:1px solid var(--riga)">{x}</span>' for x in ['Braccia', 'Spalle', 'Polpacci'])
    p2 = pagina(nome, 2,
        '<div class="sez"><div class="eyebrow">Come funziona</div><h2>Non è un\'elettrostimolazione.</h2>'
        '<p style="max-width:152mm;margin-bottom:5mm">Il campo elettromagnetico focalizzato attraversa la cute e il tessuto adiposo e stimola direttamente i neuroni motori profondi: il muscolo si contrae in modo supermassimale, a un ritmo che l\'esercizio normale non raggiunge. '
        'Il dispositivo è non ionizzante, atermico e agisce solo sui neuroni motori, non su quelli sensoriali.</p>'
        + tabella(conf, ['', 'EMS con elettrodi', 'HI-EMT · Hermes Slim']) + '</div>'
        '<div class="sez"><div class="eyebrow">Le zone</div><h2>Dove lavora.</h2>'
        '<p style="margin-bottom:3mm"><b style="color:var(--ink)">Zone principali</b></p>' + chips1 +
        '<p style="margin:3mm 0"><b style="color:var(--ink)">Trattabili con sedute più numerose</b></p>' + chips2 + '</div>'
        '<div class="card" style="background:var(--velo2)"><div class="eyebrow">Doppia azione</div><h3 style="font-size:13pt">Muscolo e tessuto adiposo.</h3>'
        '<p style="font-size:9pt;margin:0">Il produttore descrive Hermes Slim come una tecnologia che lavora insieme sul rinforzo del muscolo e sul grasso localizzato nella stessa seduta. Per ogni trattamento, i parametri e il numero di sedute si decidono in cabina, dopo la valutazione della cliente.</p></div>')
    spec = [('Tecnologia', 'HI-EMT (HIFEM), non invasiva'), ('Profondità', 'Fino a 8 cm, con due grandi piastre'), ('Manipoli', 'Versione con uno o con due manipoli'),
            ('Interfaccia', 'Schermo LCD touch · modalità Auto e Manuale'), ('Impulso', '4 livelli: continuo, impulso 1, impulso 2, automatico'),
            ('Frequenze', 'F1 · F2 · F3 da 1 a 150 Hz nel protocollo manuale'), ('Raffreddamento', 'TEC continuo (−10 °C ~ 40 °C)'), ('Consumo massimo', '900 W'),
            ('Alimentazione', 'AC 220 V / 50 Hz oppure 110 V / 60 Hz'), ('Natura', 'Dispositivo per uso estetico, certificato CE. Non è un dispositivo medico')]
    p3 = pagina(nome, 3,
        '<div class="sez"><div class="eyebrow">Scheda tecnica</div><h2>I dati dal manuale d\'uso.</h2>' + tabella(spec, ['Caratteristica', 'Hermes Slim']) + '</div>'
        '<div class="sez"><div class="eyebrow">Le sedute</div><h2>Quanto dura, ogni quanto.</h2><div class="tre">'
        '<div class="col"><h3>30 · 45 · 60 minuti</h3><p>Seduta standard, intensiva, massimale. Al massimo due trattamenti al giorno: parte alta e parte bassa del corpo.</p></div>'
        '<div class="col"><h3>2 a settimana, per un mese</h3><p>È il protocollo ottimale indicato dal manuale. Poi, una seduta al mese di mantenimento.</p></div>'
        '<div class="col"><h3>5 modalità per zona</h3><p>HIIT, forza, sviluppo muscolare, modellamento corpo, brucia grassi: potenza e frequenze già impostate per braccia, polpacci, cosce, glutei e addome.</p></div></div></div>'
        '<div class="card red" style="border:1px solid #E7C7C0;background:#FBF1EF"><div class="eyebrow" style="color:#9C3A28">Quando non si usa</div><h3 style="font-size:12pt">Controindicazioni assolute.</h3>'
        '<p style="font-size:8.8pt;margin:0">Pacemaker, defibrillatore e altri impianti elettronici attivi, neurostimolatori e impianto cocleare · gravidanza · tumore attivo · epilessia · infezioni attive e febbre alta · trombosi venosa profonda · emorragia attiva · gravi malattie cardiache · ictus o infarto recente. '
        'Altre condizioni richiedono una valutazione caso per caso: l\'elenco completo è nel manuale d\'uso, che consegniamo con il dispositivo.</p></div>')
    return [p1, p2, p3, ultima(d)]

# =============================== stampa ===============================
def stampa(d, pagine):
    doc = f'<!doctype html><html lang="it"><head><meta charset="utf-8"><title>{esc(d["nome"])} · NIPEC</title><style>{CSS.replace("%(font)s", FONT)}</style></head><body>{"".join(pagine)}</body></html>'
    h = os.path.join(QUI, f'brochure-{d["file"].lower()}.html'); pdf = os.path.join(QUI, f'BROCHURE-{d["file"]}.pdf')
    open(h, 'w', encoding='utf8').write(doc)
    subprocess.run([CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer', '--allow-file-access-from-files',
                    f'--print-to-pdf={pdf}', '--virtual-time-budget=8000', 'file://' + h], check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    print(pdf)

for d, f in ((URIEL, uriel_pagine), (ARES, ares_pagine), (AFRODITE, afrodite_pagine), (HERMES, hermes_pagine)):
    stampa(d, f())
