# -*- coding: utf-8 -*-
import io,os,re,sys,shutil,glob
S=os.path.dirname(os.path.abspath(__file__))
SRC=os.path.join(S,'pulito'); OUT=os.path.join(S,'sitonuovo')
LINGUA={'sq':'sq','en':'en'}
DESCR={
 'index':"Noleggio e vendita di tecnologie estetiche professionali in Italia e Albania. Laser a diodo, corpo e viso, criolipolisi. Formazione con esame e assistenza inclusa.",
 'sq':"Qira dhe shitje teknologjish estetike profesionale në Shqipëri dhe Itali. Lazer me diodë, trup dhe fytyrë, kriolipolizë. Trajnim me provim dhe asistencë.",
 'en':"Professional aesthetic technology for rent or purchase in Italy and Albania. Diode lasers, body and face, cryolipolysis. Training with exam and support included.",
 'laser-ares':"Laser a diodo ARES 808 nm: fino a 2000 watt, gestione digitale, telecamera integrata. Certificazione CE italiana e MDR attivo.",
 'laser-uriel':"Laser a diodo URIEL tri-onda 755/808/1064 nm con gestione software IA. Certificazione CE italiana e MDR attivo.",
 'afrodite':"Afrodite VS++: sistema multifunzione NIPEC per corpo e viso, con protocolli di cabina e formazione inclusa.",
 'borea-cryo':"Borea e Cryo 360°: criolipolisi ed EMS per il rimodellamento del corpo, con protocolli NIPEC.",
 'q-switch':"Laser Q-Switch NIPEC per la divisione medicale.",
 'metodo':"Il metodo NIPEC in quattro fasi: prima capiamo il centro, poi scegliamo la tecnologia.",
 'formazione':"Formazione NIPEC a tappe con esame finale e certificazione operatore valida 12 mesi.",
 'chi-siamo':"NIPEC: tecnologie estetiche professionali fra Italia e Albania. Chi siamo e come lavoriamo.",
 'contatti':"Contatta NIPEC per una consulenza gratuita e senza impegno su WhatsApp. Italia e Albania.",
 'privacy':"Informativa privacy e cookie del sito NIPEC.",
}
CARATTERE = """<style>
@font-face{font-family:'Archivo';src:url('caratteri/archivo.woff2') format('woff2');font-weight:100 900;font-style:normal;font-display:swap}
</style>"""
PRIVACY = {
 'Ultimo aggiornamento: [DATA]':'Ultimo aggiornamento: ottobre 2026',
 "Testo legale da far redigere o verificare al consulente privacy (GDPR, Reg. UE 2016/679). Qui sotto c'è solo la struttura della pagina.":
   "In breve: questo sito non ti profila e non installa cookie di tracciamento. Se ci scrivi su WhatsApp o compili il modulo dei contatti, i tuoi dati li usiamo per risponderti.",
 'PHD System Srl, Via Rovetta 29, 25080 Padenghe sul Garda (BS), P.IVA 04696530981. Contatto: info@nipecestetica.com':
   'PHD System S.r.l., Via Rovetta 29, 25080 Padenghe sul Garda (BS), P.IVA 04696530981. Per esercitare i tuoi diritti scrivi a quell’indirizzo oppure su WhatsApp al +39 351 846 6025.',
 '[DATI DEL MODULO CONTATTI, DATI DI NAVIGAZIONE]':
   'Se compili il modulo dei contatti o ci scrivi su WhatsApp: nome, telefono, nome e città del centro, l’interesse che indichi e il testo del messaggio. Se navighi e basta: il server registra indirizzo IP, data, pagina e tipo di browser, come fa qualunque server web.',
 '[FINALITÀ E BASE GIURIDICA]':
   'I dati del modulo e di WhatsApp servono a risponderti e a seguire la richiesta: la base giuridica è il riscontro alla tua richiesta e, dove serve, l’esecuzione di misure precontrattuali. I registri del server servono alla sicurezza e al funzionamento del sito, per nostro legittimo interesse.',
 '[TEMPI DI CONSERVAZIONE]':
   'Le richieste e le conversazioni restano finché serve a gestire il rapporto, e comunque non oltre il tempo necessario alle finalità per cui sono state raccolte. I registri del server seguono i tempi tecnici del fornitore di hosting.',
 '[FORNITORI, HOSTING, TRASFERIMENTI EXTRA UE — ALBANIA]':
   'Soltanto ai fornitori tecnici che ci permettono di lavorare — l’hosting del sito e il servizio di messaggistica — e a chi la legge ci obbliga. Le richieste che riguardano l’Albania sono gestite dal nostro referente a Tirana: l’Albania è un paese terzo rispetto all’Unione europea e il trasferimento avviene nei limiti del Capo V del Regolamento. Non vendiamo e non cediamo dati a terzi.',
 '[ACCESSO, RETTIFICA, CANCELLAZIONE, OPPOSIZIONE, RECLAMO AL GARANTE]':
   'Puoi chiederci in ogni momento di accedere ai tuoi dati, correggerli, cancellarli, limitarne il trattamento od opporti. Basta scriverci ai contatti qui sopra. Se ritieni che il trattamento non sia corretto puoi rivolgerti all’autorità di controllo: in Italia il Garante per la protezione dei dati personali (garanteprivacy.it), in Albania il Komisioneri për të Drejtën e Informimit dhe Mbrojtjen e të Dhënave Personale (idp.al).',
 '[ELENCO COOKIE TECNICI E DI TERZE PARTI, CON DURATA E FINALITÀ]':
   'Questo sito non usa cookie di profilazione e non ha strumenti di statistica di terze parti. I caratteri e le immagini sono serviti dal nostro stesso dominio: mentre leggi queste pagine non parte nessuna richiesta verso servizi esterni. Restano solo i cookie tecnici necessari al funzionamento, che non richiedono consenso.',
}
MODULO = """<script>
(function(){
  var f=document.querySelector('main form'); if(!f) return;
  var NUM='393518466025';
  f.addEventListener('submit',function(ev){
    ev.preventDefault();
    var righe=[];
    Array.prototype.forEach.call(f.querySelectorAll('input,select,textarea'),function(c){
      if(c.type==='checkbox'){ if(c.checked) righe.push('Consenso privacy: si'); return; }
      if(!c.value||!c.value.trim()) return;
      var et=(c.labels&&c.labels[0]?c.labels[0].innerText:(c.placeholder||c.name||'')).replace(/\\s+/g,' ').trim();
      righe.push((et?et+': ':'')+c.value.trim());
    });
    var testo='Richiesta dal sito NIPEC\\n'+righe.join('\\n');
    window.open('https://wa.me/'+NUM+'?text='+encodeURIComponent(testo),'_blank','noopener');
  });
})();
</script>"""

os.makedirs(OUT,exist_ok=True)
rapporto=[]
for f in sorted(glob.glob(os.path.join(SRC,'*.html'))):
    nome=os.path.basename(f)[:-5]
    t=io.open(f,encoding='utf-8',errors='replace').read()
    prima=len(t)
    # 1. via tutti gli script
    t=re.sub(r'<script[^>]*>.*?</script>','',t,flags=re.S)
    t=re.sub(r'<script[^>]*/?>','',t)
    # 2. via i due fogli di Google Fonts (191 KB l'uno) e il preconnect
    t=re.sub(r'<style[^>]*>(?:(?!</style>).)*?fonts\.gstatic\.com(?:(?!</style>).)*?</style>','',t,flags=re.S)
    t=re.sub(r'<link rel="preconnect"[^>]*>','',t)
    t=re.sub(r'<link[^>]*fonts\.googleapis\.com[^>]*>','',t)
    # 3. testa: lingua, viewport, descrizione, carattere locale
    t=re.sub(r'<html[^>]*>','<html lang="%s">'%LINGUA.get(nome,'it'),t,count=1)
    testa=('<meta name="viewport" content="width=device-width, initial-scale=1">\n'
           '<meta name="description" content="%s">\n'
           '<meta name="theme-color" content="#123A63">\n'
           '<link rel="icon" href="favicon.svg" type="image/svg+xml">\n%s\n' % (DESCR.get(nome,''),CARATTERE))
    t=t.replace('<meta charset="utf-8">','<meta charset="utf-8">\n'+testa,1)
    # 4. numero verde che non esiste
    t=re.sub(r'\s*<br>\s*Numero verde 800 141 726','',t)
    t=t.replace('Numero verde 800 141 726','')
    # 5. privacy
    if nome=='privacy':
        for a,b in PRIVACY.items():
            if a not in t: rapporto.append('  !! privacy, non trovato: '+a[:40])
            t=t.replace(a,b)
    # 6. modulo -> WhatsApp
    if nome=='contatti':
        t=t.replace('</body>',MODULO+'\n</body>',1)
    io.open(os.path.join(OUT,nome+'.html'),'w',encoding='utf-8').write(t)
    rapporto.append('%-14s %8d -> %6d B' % (nome,prima,len(t)))
print('\n'.join(rapporto))
