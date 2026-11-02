#!/usr/bin/env python3
"""I ventiquattro reel «SBAM», stacco per stacco. E' la fonte unica: da qui nascono i copioni (copioni/*.md) e il documento stampato.

Due serie:
  A · adv     dodici reel per le inserzioni: sei sul laser (L1-L6), sei su Afrodite (F1-F6). Portano a WhatsApp. Italia e Albania.
  B · pagina  dodici reel per la pagina Instagram/Facebook di NIPEC (P1-P12). Non vendono: fanno fermare il dito e fanno ricordare chi siamo.

LA REGOLA DEI 5 SECONDI (la solita, in due meta') + SBAM:
  1. i primi 5 secondi contengono il vantaggio intero;
  2. nessuno stacco dura piu' di 5 secondi: dopo, si cambia stacco E inquadratura;
  3. SBAM: in ogni reel c'e' un colpo, o una sorpresa, entro i primi 3 secondi; mezzo secondo di silenzio dopo il colpo; al massimo due per reel.
In piu', dalla seconda stesura (2 novembre): la voce parte entro 0,5 s; parlato sotto le 2,5 parole al secondo; invito finale
«Chiama o scrivi su WhatsApp: PAROLA»; mai l'imperativo con «ci» (scrivici, seguici...); ogni dato non controllato e' segnato.

Ogni stacco: (inquadratura, cosa si vede, cosa si dice, scritte a schermo, durata in secondi, suono).
Le parole sono scritte per essere dette da Giorgio (Italia) o da Uarda (Albania, tradotte dopo l'approvazione).

Controlli (python3 reel_sbam_dati.py): nessuno stacco oltre 5 s, due stacchi di fila con inquadrature diverse, gancio dentro i 5 secondi,
SBAM che cade entro 3 s (al massimo due), voce dal primo stacco, ritmo del parlato non oltre 2,5 parole al secondo,
durata del copione tra 15 e 22 secondi, invito finale con la parola chiave, parole vietate (macchina, LED, cavitazione,
percentuali, prima/dopo, diodi, watt, imperativi in -ci).
"""
import math, os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'REEL-500'))
from reel_dati import PP, MB, DET, CL, QUADRO as _QUADRO, parole, fmt  # noqa: E402
QUADRO = {**_QUADRO, CL: "la persona e il dispositivo nell'ambiente"}   # «dispositivo», non «macchina»

LASER = ['L1', 'L2', 'L3', 'L4', 'L5', 'L6']
AFRO = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6']
PAGINA = ['P1', 'P5', 'P2', 'P3', 'P4', 'P6', 'P12', 'P9', 'P7', 'P8', 'P10', 'P11']   # nell'ordine di uscita consigliato
CODICI = LASER + AFRO + PAGINA
MAX_PAROLE_AL_SECONDO = 2.5
CTA = 'Chiama o scrivi su WhatsApp'

R = {}

def calendario(): return "Il calendario: un dito va dal 1 al 30."

# =============================== SERIE A · ADV · LASER ===============================

R['L1'] = dict(
    serie='A', campagna='Laser', titolo='Trenta pagine in un colpo', copertina='ARRIVA IL 1. LO PAGHI IL 30.', parola='LASER', gancio=2, sbam=2,
    chi='Giorgio (Italia) · Uarda (Albania)',
    concetto="Un calendario a fogli giornalieri: la mano strappa le pagine dal 1 al 30 in un colpo solo. Lo strappo è il colpo e dice l'offerta in una frase: arriva il 1, lo paghi il 30.",
    stacchi=[
        (PP,  "Giorgio, in camera, il calendario a fogli giornalieri accanto al viso.", "Il dispositivo arriva il primo.", ["ARRIVA IL 1"], 2.0, "fruscio dei fogli (nessuna musica)"),
        (DET, "La mano afferra le pagine dal 1 al 30 e le strappa in un colpo solo.", "E lo paghi il trenta.", ["LO PAGHI IL 30"], 3.0, "SBAM: lo strappo, secco · poi 0,5 s di silenzio"),
        (MB,  "Giorgio posa le pagine strappate sul tavolo, guarda in camera.", "Un mese intero prima del primo euro.", [], 3.0, "—"),
        (CL,  "Giorgio e il dispositivo in cabina.", "Chiudi ad agosto? Quel mese non lo paghi.", [], 3.5, "—"),
        (DET, "Sul tavolo, un foglio bianco. La mano lo liscia.", "Zero anticipo. Zero cauzione. Nessun vincolo.", ["ZERO ANTICIPO · ZERO CAUZIONE · NESSUN VINCOLO"], 2.5, "—"),
        (PP,  "Giorgio, in camera.", "Cinquecento al mese. Chiama o scrivi su WhatsApp: LASER.", ["500 € / MESE", "poi: CHIAMA O SCRIVI «LASER» SU WHATSAPP"], 4.0, "—"),
    ],
    ad=("Il dispositivo arriva il 1. Lo paghi il 30.\nUn mese intero di lavoro prima del primo euro. Zero anticipo, zero cauzione, nessun vincolo.\n500 € al mese. Chiama o scrivi su WhatsApp: LASER.",
        'Arriva il 1. Lo paghi il 30'),
    albanese=[("Pajisja vjen më 1.", "VJEN MË 1"), ("Dhe e paguan më 30.", "E PAGUAN MË 30"), ("Një muaj i tërë para lekut të parë.", ""),
              ("Mbyll gushtin? Atë muaj nuk e paguan.", ""), ("Zero paradhënie. Zero garanci. Asnjë detyrim.", "ZERO PARADHËNIE · ZERO GARANCI · ASNJË DETYRIM"),
              ("Pesëdhjetë mijë lekë në muaj. Telefono ose shkruaj në WhatsApp: LASER.", "50.000 LEKË / MUAJ")],
    serve="Un calendario a fogli giornalieri (quello a blocchetto, un foglio per giorno) con il blocco dal 1 al 30, senza mese né anno stampati: regge ogni mese. Un foglio bianco.",
    note=["Se i fogli non si strappano tutti insieme, si strappa il blocco intero dalla base: conta il gesto e il suono, non i trenta fogli veri.",
          "«Quel mese non lo paghi» è una condizione commerciale (la clausola ferie del copione 3 della Campagna 500): da confermare con Giorgio prima di girare."],
    cambi="Il gancio ora dice l'offerta intera in 5 secondi, con la voce da 0 s e il silenzio subito dopo lo strappo. Frasi accorciate sotto le 2,5 parole al secondo; invito riscritto con «Chiama o scrivi su WhatsApp» (stacco di 4 s).",
)

R['L2'] = dict(
    serie='A', campagna='Laser', titolo='Fermo', copertina='SE SI FERMA, 48 ORE.', parola='LASER', gancio=2, sbam=2,
    chi='Giorgio (Italia) · Uarda (Albania)',
    concetto="Il display si spegne di colpo. Poi il portellone del furgone si spalanca: è il colpo vero, senza effetti. Dice il muletto in 48 ore.",
    stacchi=[
        (DET, "Il display acceso del dispositivo, in cabina. Di colpo, nero.", "Il tuo laser si ferma.", ["DOMANI SI FERMA."], 2.0, "un bip, poi mezzo secondo di silenzio"),
        (CL,  "Stacco: il portellone del furgone si spalanca, il dispositivo scende.", "In 48 ore, un altro.", ["48 ORE"], 3.0, "SBAM: il portellone, suono vero · 0,5 s di silenzio"),
        (PP,  "Giorgio, in camera.", "Non chiudi un'ora. Non disdici nessuna cliente.", [], 3.5, "—"),
        (MB,  "Giorgio, il dispositivo dietro di lui.", "Una settimana ferma: clienti che saltano il turno.", [], 3.5, "—"),
        (DET, "Il display del dispositivo sostitutivo, acceso.", "Il rischio non è tuo. È nostro.", ["IL RISCHIO È NOSTRO"], 3.0, "—"),
        (PP,  "Giorgio, in camera.", "Cinquecento al mese. Chiama o scrivi su WhatsApp: LASER.", ["500 € / MESE", "poi: CHIAMA O SCRIVI «LASER» SU WHATSAPP"], 4.0, "—"),
    ],
    ad=("Domani mattina il tuo laser si ferma. E adesso?\nDa noi, in 48 ore hai un altro dispositivo in cabina: non chiudi un'ora, non disdici nessuna cliente.\n500 € al mese, nessun vincolo. Chiama o scrivi su WhatsApp: LASER.",
        'Se si ferma, 48 ore e ne hai un altro'),
    albanese=[("Lazeri yt ndalon.", "NESËR NDALON."), ("Brenda 48 orëve ke një tjetër.", "48 ORË"), ("Nuk mbyll asnjë orë. Nuk anulon asnjë takim.", ""),
              ("Një javë me lazer të ndalur: klientë që humbasin radhën.", ""), ("Rreziku nuk është yti. Është i yni.", "RREZIKU ËSHTË I YNI"),
              ("Pesëdhjetë mijë lekë në muaj. Telefono ose shkruaj në WhatsApp: LASER.", "50.000 LEKË / MUAJ")],
    serve="Il furgone con il portellone che si apre (il suono vero è il colpo). Un dispositivo che si spegne e si riaccende, e un altro accanto per il display sostitutivo.",
    note=["Il portellone va sbattuto davvero, con la camera già in registrazione: non si ripete bene. Meglio due riprese.",
          "Il «dodici clienti» della prima stesura è tolto: era una stima della Campagna 500, non un dato misurato. «48 ore» e «nessun vincolo» sono nella Campagna 500."],
    cambi="L'apertura ora è «Il tuo laser si ferma» (si capisce in 2 s); «domani» passa nella scritta. Tolto il numero dei dodici clienti. Dopo il portellone c'è mezzo secondo di silenzio prima della voce; stacco 3 e invito allungati per stare sotto le 2,5 parole al secondo.",
)

R['L3'] = dict(
    serie='A', campagna='Laser', titolo='Ti sta guardando', copertina='TI STA GUARDANDO.', parola='LASER', gancio=2, sbam=1,
    chi='Giorgio (Italia) · Uarda (Albania)',
    concetto="Primissimo piano sull'obiettivo della telecamera del dispositivo, un lampo: «Ti sta guardando». Poi la spiegazione: guarda la pelle e suggerisce i parametri, decidi sempre tu.",
    stacchi=[
        (DET, "Primissimo piano sull'obiettivo della telecamera del dispositivo. Lampo bianco.", "Ti sta guardando.", ["TI STA GUARDANDO"], 2.0, "SBAM a 0 s: click e lampo · voce da 0,5 s"),
        (PP,  "Giorgio, in camera. Gira lo sguardo verso l'obiettivo e torna in camera.", "Guarda la pelle, ti suggerisce i parametri.", ["TELECAMERA + IA"], 3.0, "—"),
        (DET, "La telecamera e il manipolo in titanio, da vicino.", "Decidi sempre tu. Lei suggerisce, tu scegli.", ["DECIDI SEMPRE TU"], 3.5, "—"),
        (MB,  "Giorgio, il dispositivo accanto.", "Certificato in Italia, CE, MDR attivo.", ["CERTIFICATO IN ITALIA · MDR ATTIVO"], 3.0, "—"),
        (CL,  "Il dispositivo in cabina, luce ferma.", "Un laser di ultima generazione, a noleggio.", [], 3.0, "—"),
        (PP,  "Giorgio, in camera.", "Cinquecento al mese. Chiama o scrivi su WhatsApp: LASER.", ["500 € / MESE", "poi: CHIAMA O SCRIVI «LASER» SU WHATSAPP"], 4.0, "—"),
    ],
    ad=("Il tuo prossimo laser ha una telecamera.\nGuarda la pelle e, con l'intelligenza artificiale, ti suggerisce i parametri: decidi sempre tu. Certificato in Italia, MDR attivo.\n500 € al mese, nessun vincolo. Chiama o scrivi su WhatsApp: LASER.",
        'Telecamera e IA. Decidi sempre tu'),
    albanese=[("Po të shikon.", "PO TË SHIKON"), ("Shikon lëkurën, të sugjeron parametrat.", "KAMERË + IA"), ("Vendos gjithmonë ti. Ajo sugjeron, ti zgjedh.", "VENDOS GJITHMONË TI"),
              ("I certifikuar në Itali, CE, MDR aktiv.", "I CERTIFIKUAR NË ITALI · MDR AKTIV"), ("Një lazer i brezit të fundit, me qira.", ""),
              ("Pesëdhjetë mijë lekë në muaj. Telefono ose shkruaj në WhatsApp: LASER.", "50.000 LEKË / MUAJ")],
    serve="Dispositivo con il display acceso; obiettivo della telecamera pulito, ripreso da 10 cm. Il lampo bianco si fa in montaggio.",
    note=["Non si mostra pelle: la telecamera si inquadra da sola, mai puntata su una cliente.",
          "«Intelligenza artificiale», «certificato in Italia», «CE» e «MDR attivo» vengono dai testi già approvati (Campagna 500, sito): da confermare con i documenti del dispositivo."],
    cambi="Il reel ha la voce già a 0,5 s («Ti sta guardando»): prima partiva muto. «Lei suggerisce, tu scegli» rende concreta la frase «decidi sempre tu»; «propone» diventa «suggerisce» (non è una diagnosi).",
)

R['L4'] = dict(
    serie='A', campagna='Laser', titolo='Quanto costa un laser?', copertina='QUANTO COSTA UN LASER?', parola='LASER', gancio=2, sbam=2,
    chi='Giorgio (Italia) · Uarda (Albania)',
    concetto="La domanda che tutti si fanno, e una risposta che non ti aspetti: un adesivo «500 €» schiacciato sul dispositivo. Cinquecento, al mese.",
    stacchi=[
        (PP,  "Giorgio, in camera, un adesivo nascosto dietro la schiena.", "Quanto costa un laser?", ["QUANTO COSTA UN LASER?"], 2.0, "silenzio"),
        (DET, "La mano schiaccia un adesivo «500 €» sul cartellino bianco attaccato al dispositivo.", "Cinquecento. Al mese.", ["500 € / MESE"], 3.0, "SBAM: l'adesivo sul dispositivo · 0,5 s di silenzio"),
        (MB,  "Giorgio, il dispositivo accanto.", "Lo paghi dopo trenta giorni di lavoro.", ["LO PAGHI IL 30"], 3.5, "—"),
        (DET, "Sul tavolo, il foglio bianco.", "Zero anticipo. Zero cauzione. Nessun vincolo.", ["ZERO ANTICIPO · ZERO CAUZIONE · NESSUN VINCOLO"], 3.0, "—"),
        (CL,  "Giorgio e il dispositivo in cabina.", "Formazione compresa. Se si ferma, 48 ore.", ["FORMAZIONE COMPRESA"], 3.0, "—"),
        (PP,  "Giorgio, in camera.", "Cinquecento al mese. Chiama o scrivi su WhatsApp: LASER.", ["500 € / MESE", "poi: CHIAMA O SCRIVI «LASER» SU WHATSAPP"], 4.0, "—"),
    ],
    ad=("Quanto costa un laser?\nCinquecento euro al mese, e lo paghi dopo trenta giorni di lavoro. Zero anticipo, zero cauzione, nessun vincolo. Formazione compresa.\nChiama o scrivi su WhatsApp: LASER.",
        'Un laser a 500 € al mese'),
    albanese=[("Sa kushton një lazer?", "SA KUSHTON NJË LAZER?"), ("Pesëdhjetë mijë lekë. Në muaj.", "50.000 LEKË / MUAJ"), ("Paguhet pas tridhjetë ditësh pune.", "E PAGUAN MË 30"),
              ("Zero paradhënie. Zero garanci. Asnjë detyrim.", ""), ("Trajnimi përfshirë. Nëse ndalon, 48 orë.", "TRAJNIMI PËRFSHIRË"),
              ("Pesëdhjetë mijë lekë në muaj. Telefono ose shkruaj në WhatsApp: LASER.", "50.000 LEKË / MUAJ")],
    serve="Un cartellino bianco attaccato al dispositivo e un adesivo con il prezzo, da schiacciare con il palmo. Il foglio bianco di L1.",
    note=["L'adesivo è una scena. Per l'Albania: «50.000 LEKË».", "L'adesivo si schiaccia piano sul cartellino: il colpo lo mette il montaggio."],
    cambi="Reel nuovo (2 novembre).",
)

R['L5'] = dict(
    serie='A', campagna='Laser', titolo='Il foglio che strappo', copertina='NESSUN VINCOLO.', parola='LASER', gancio=2, sbam=2,
    chi='Giorgio (Italia) · Uarda (Albania)',
    concetto="Un foglio con scritto «VINCOLO», strappato in due: «Da noi non c'è». Il gesto dice l'offerta senza spiegarla.",
    stacchi=[
        (PP,  "Giorgio, in camera, un foglio in mano con scritto «VINCOLO».", "Questo è un vincolo.", ["VINCOLO"], 2.0, "silenzio"),
        (DET, "Le mani strappano il foglio in due.", "Da noi non c'è.", ["NESSUN VINCOLO"], 3.0, "SBAM: lo strappo · 0,5 s di silenzio"),
        (MB,  "Giorgio posa i due pezzi sul tavolo.", "Arriva il primo. Lo paghi il trenta.", ["ARRIVA IL 1 · LO PAGHI IL 30"], 3.0, "—"),
        (CL,  "Giorgio e il dispositivo in cabina.", "Chiudi ad agosto? Quel mese non lo paghi.", [], 3.5, "—"),
        (DET, "Il foglio bianco sul tavolo.", "Zero anticipo. Zero cauzione.", ["ZERO ANTICIPO · ZERO CAUZIONE"], 3.0, "—"),
        (PP,  "Giorgio, in camera.", "Cinquecento al mese. Chiama o scrivi su WhatsApp: LASER.", ["500 € / MESE", "poi: CHIAMA O SCRIVI «LASER» SU WHATSAPP"], 4.0, "—"),
    ],
    ad=("Questo è un vincolo. Da noi non c'è.\nIl dispositivo arriva il 1, lo paghi il 30. Zero anticipo, zero cauzione. Se chiudi ad agosto, quel mese non lo paghi.\n500 € al mese. Chiama o scrivi su WhatsApp: LASER.",
        'Nessun vincolo, 500 € al mese'),
    albanese=[("Ky është një detyrim.", "DETYRIM"), ("Tek ne nuk ka.", "ASNJË DETYRIM"), ("Vjen më 1. E paguan më 30.", "VJEN MË 1 · E PAGUAN MË 30"),
              ("Mbyll gushtin? Atë muaj nuk e paguan.", ""), ("Zero paradhënie. Zero garanci.", "ZERO PARADHËNIE · ZERO GARANCI"),
              ("Pesëdhjetë mijë lekë në muaj. Telefono ose shkruaj në WhatsApp: LASER.", "50.000 LEKË / MUAJ")],
    serve="Un foglio con la parola «VINCOLO» scritta a pennarello grosso (non è il contratto di nessuno). Il foglio bianco.",
    note=["Il foglio è una scena: non si inquadra nessun contratto vero, né di NIPEC né di altri.",
          "«Quel mese non lo paghi»: condizione commerciale del copione 3 della Campagna 500, da confermare con Giorgio prima di girare."],
    cambi="Reel nuovo (2 novembre).",
)

R['L6'] = dict(
    serie='A', campagna='Laser', titolo='Tre cose, un prezzo', copertina='LASER · PROTOCOLLO · FORMAZIONE', parola='LASER', gancio=2, sbam=2,
    chi='Giorgio (Italia) · Uarda (Albania)',
    concetto="Tre colpi a ritmo sul tavolo: il manipolo, il protocollo, il foglio della formazione. Per cinquecento al mese arrivano tutti e tre.",
    stacchi=[
        (PP,  "Giorgio, in camera, tre dita alzate.", "Cinquecento al mese. Tre cose.", ["500 € / MESE · 3 COSE"], 2.5, "silenzio"),
        (DET, "Sul tavolo, tre appoggi a ritmo: il manipolo, il protocollo, il foglio «formazione». A ogni appoggio, il nome a schermo.", "", ["IL LASER", "IL PROTOCOLLO", "LA FORMAZIONE"], 2.5, "SBAM ×3, uno ogni 0,8 s (il primo a 2,5 s): contano come un solo SBAM"),
        (MB,  "Giorgio, il dispositivo accanto.", "Il laser. Il protocollo scritto. La formazione.", ["UN SOLO PREZZO"], 3.5, "—"),
        (DET, calendario(), "Arriva il primo. Lo paghi il trenta.", ["ARRIVA IL 1 · LO PAGHI IL 30"], 3.0, "—"),
        (CL,  "Giorgio e il dispositivo in cabina.", "Nessun vincolo. Se si ferma, 48 ore.", ["NESSUN VINCOLO"], 3.0, "—"),
        (PP,  "Giorgio, in camera.", "Cinquecento al mese. Chiama o scrivi su WhatsApp: LASER.", ["500 € / MESE", "poi: CHIAMA O SCRIVI «LASER» SU WHATSAPP"], 4.0, "—"),
    ],
    ad=("Tre cose, un prezzo: il laser, il protocollo scritto e la formazione.\nArriva il 1, lo paghi il 30. Nessun vincolo. Se si ferma, in 48 ore ne hai un altro.\n500 € al mese. Chiama o scrivi su WhatsApp: LASER.",
        'Laser, protocollo e formazione'),
    albanese=[("Pesëdhjetë mijë lekë në muaj. Tre gjëra.", "50.000 LEKË / MUAJ · 3 GJËRA"), ("", "LAZERI", ), ("Lazeri. Protokolli i shkruar. Trajnimi.", "NJË ÇMIM I VETËM"),
              ("Vjen më 1. E paguan më 30.", "VJEN MË 1 · E PAGUAN MË 30"), ("Asnjë detyrim. Nëse ndalon, 48 orë.", "ASNJË DETYRIM"),
              ("Pesëdhjetë mijë lekë në muaj. Telefono ose shkruaj në WhatsApp: LASER.", "50.000 LEKË / MUAJ")],
    serve="Il manipolo, il protocollo laser stampato (6 pagine, IT) e un foglio con scritto «formazione», da appoggiare sul tavolo a ritmo, piano. Il calendario di L1.",
    note=["Niente pelle: solo tavolo e oggetti.", "I tre appoggi vanno girati a ritmo, uno ogni 0,8 secondi; il colpo lo mette il montaggio. Il manipolo non cade: si appoggia."],
    cambi="Reel nuovo (2 novembre).",
)

# =============================== SERIE A · ADV · AFRODITE ===============================

R['F1'] = dict(
    serie='A', campagna='Afrodite', titolo='Non comprare Afrodite', copertina='NON COMPRARE AFRODITE.', parola='AFRODITE', gancio=2, sbam=2,
    chi='Giorgio (Italia) · Uarda (Albania)',
    concetto="Il contrario di quello che dice ogni inserzione: «Non comprare Afrodite». Il palmo batte sul tavolo e la frase si ribalta: «Noleggiala».",
    stacchi=[
        (PP,  "In camera, serio, la mano alzata come un alt.", "Non comprare Afrodite.", ["NON COMPRARE AFRODITE"], 2.0, "silenzio"),
        (DET, "La mano batte sul tavolo, accanto al calendario.", "Noleggiala. Cinquecento al mese.", ["NOLEGGIALA · 500 € / MESE"], 3.0, "SBAM: il palmo sul tavolo · 0,5 s di silenzio"),
        (MB,  "In cabina, il dispositivo dietro.", "Prima di spendere, scopri se nel tuo centro lavora.", [], 4.0, "—"),
        (DET, calendario(), "Arriva il primo, la paghi il trenta.", ["ARRIVA IL 1 · LA PAGHI IL 30"], 3.0, "—"),
        (CL,  "Il dispositivo in cabina.", "Quattro tecnologie. Una rata sola.", [], 3.0, "—"),
        (PP,  "In camera.", "Nessun anticipo. Chiama o scrivi su WhatsApp: AFRODITE.", ["CHIAMA O SCRIVI «AFRODITE» SU WHATSAPP"], 4.0, "—"),
    ],
    ad=("Non comprare Afrodite. Noleggiala.\nPrima di spendere, scopri se nel tuo centro lavora. Arriva il 1, la paghi il 30. Nessun anticipo, nessun vincolo.\n500 € al mese. Chiama o scrivi su WhatsApp: AFRODITE.",
        'Non comprarla. Noleggiala.'),
    albanese=[("Mos e bli Afrodite.", "MOS E BLI AFRODITE"), ("Merre me qira. Pesëdhjetë mijë lekë në muaj.", "MERRE ME QIRA · 50.000 LEKË / MUAJ"),
              ("Para se të shpenzosh, shiko nëse punon në qendrën tënde.", ""), ("Vjen më 1, e paguan më 30.", "VJEN MË 1 · E PAGUAN MË 30"),
              ("Katër teknologji. Një këst i vetëm.", ""), ("Pa paradhënie. Telefono ose shkruaj në WhatsApp: AFRODITE.", "")],
    serve="Un tavolo solido da battere con il palmo (si batte piano: il colpo lo mette il montaggio). Il calendario a fogli giornalieri di L1.",
    note=["«Nessun vincolo» e il prezzo sono nell'inserzione e nella scritta del colpo: non ripetuti a voce per restare nei tempi."],
    cambi="Il prezzo ora è già nello stacco 2, sul colpo: nei primi 5 secondi ci sono «Noleggiala» e «500 € al mese». Stacco 3 allungato a 4 s per la frase lunga; invito con «Chiama o scrivi su WhatsApp».",
)

R['F2'] = dict(
    serie='A', campagna='Afrodite', titolo='Quattro colpi', copertina='4 TECNOLOGIE, 1 RATA.', parola='AFRODITE', gancio=2, sbam=2,
    chi='Giorgio (Italia) · Uarda (Albania)',
    concetto="Quattro tecnologie, quattro colpi: quattro manipoli appoggiati sul lettino uno dopo l'altro, a ogni colpo il nome a schermo (contano come un solo SBAM). Poi il dispositivo solo, una rata sola.",
    stacchi=[
        (PP,  "In camera, quattro dita alzate.", "Quattro tecnologie.", ["4 TECNOLOGIE"], 2.0, "silenzio"),
        (DET, "Quattro manipoli appoggiati piano sul lettino, a 2,0 · 2,7 · 3,4 · 4,1 s. A ogni appoggio, il nome a schermo.", "", ["ULTRASUONO", "RADIOFREQUENZA", "VACUUM", "LOW LASER"], 3.0, "SBAM ×4, uno ogni 0,7 s (il primo a 2,0 s): contano come un solo SBAM"),
        (MB,  "In cabina, ferma.", "Ultrasuono focalizzato direzionale, radiofrequenza, vacuum e low laser.", ["ULTRASUONO FOCALIZZATO DIREZIONALE"], 4.0, "—"),
        (CL,  "Il dispositivo intero, in cabina.", "Un dispositivo. Una rata sola.", [], 3.0, "—"),
        (DET, "Il calendario: arriva il 1, si paga il 30.", "Arriva il primo, la paghi il trenta.", ["ARRIVA IL 1 · LA PAGHI IL 30"], 3.0, "—"),
        (PP,  "In camera.", "Cinquecento al mese. Chiama o scrivi su WhatsApp: AFRODITE.", ["500 € / MESE", "poi: CHIAMA O SCRIVI «AFRODITE» SU WHATSAPP"], 4.0, "—"),
    ],
    ad=("Ultrasuono focalizzato direzionale, radiofrequenza, vacuum e low laser. Quattro tecnologie in un solo dispositivo, una rata sola.\nArriva il 1, la paghi il 30. Nessun vincolo.\n500 € al mese. Chiama o scrivi su WhatsApp: AFRODITE.",
        '4 tecnologie, 1 dispositivo, 1 rata'),
    albanese=[("Katër teknologji.", "4 TEKNOLOGJI"), ("", "ULTRATINGULL I FOKUSUAR · RADIOFREKUENCË · VAKUM · LOW LASER"),
              ("Ultratingull i fokusuar, radiofrekuencë, vakum dhe low laser.", "ULTRATINGULL I FOKUSUAR"), ("Një pajisje. Një këst i vetëm.", ""),
              ("Vjen më 1, e paguan më 30.", "VJEN MË 1 · E PAGUAN MË 30"), ("Pesëdhjetë mijë lekë në muaj. Telefono ose shkruaj në WhatsApp: AFRODITE.", "50.000 LEKË / MUAJ")],
    serve="I quattro manipoli, luce radente, su un lettino con un telo bianco. I quattro appoggi vanno girati a ritmo, uno ogni 0,7 secondi.",
    note=["Niente pelle: solo manipoli e telo. I manipoli non si lasciano cadere: si appoggiano piano, il colpo lo mette il montaggio.",
          "In albanese il nome a schermo è «ULTRATINGULL I FOKUSUAR» (senza «direzionale»): da far controllare a Uarda."],
    cambi="Corretta una contraddizione della prima stesura: il ritmo era «uno ogni 0,7 s» nello stacco e «uno ogni mezzo secondo» nelle note; ora è 0,7 s ovunque e il primo colpo cade a 2,0 s. L'apertura ha la voce a 0 s; la lista delle quattro tecnologie resta a voce nello stacco 3.",
)

R['F3'] = dict(
    serie='A', campagna='Afrodite', titolo='I compiti già fatti', copertina='I COMPITI GIÀ FATTI.', parola='AFRODITE', gancio=2, sbam=1,
    chi='Giorgio (Italia) · Uarda (Albania)',
    concetto="Un fascicolo spesso si posa sul tavolo: il protocollo. «Compiti già fatti». Poi cosa c'è dentro: protocollo, scheda di valutazione, ciclo di sedute.",
    stacchi=[
        (DET, "Un fascicolo spesso si posa sul tavolo: il protocollo stampato.", "Compiti già fatti.", ["I COMPITI GIÀ FATTI"], 2.5, "SBAM a 0 s: il fascicolo sul tavolo · voce da 0,5 s"),
        (PP,  "In camera.", "Arriva con protocollo, scheda, sedute.", ["PROTOCOLLO · SCHEDA · SEDUTE"], 2.5, "—"),
        (DET, "Le pagine del protocollo, sfogliate.", "Pagina per pagina.", [], 2.5, "—"),
        (MB,  "Al tavolo, il protocollo e la scheda di cabina.", "Dieci o dodici sedute: cosa fare, con quali parametri.", ["10-12 SEDUTE"], 4.0, "—"),
        (PP,  "In camera.", "Assistenza sempre. Cinquecento al mese, nessun vincolo.", ["ASSISTENZA SEMPRE · 500 € / MESE"], 3.5, "—"),
        (CL,  "Il dispositivo, il protocollo sul lettino.", "Chiama o scrivi su WhatsApp: AFRODITE. Te lo mostro.", ["CHIAMA O SCRIVI «AFRODITE» SU WHATSAPP"], 4.0, "—"),
    ],
    ad=("Il dispositivo arriva con i compiti già fatti: protocollo scritto, scheda di valutazione e un ciclo di 10-12 sedute. Assistenza sempre.\n500 € al mese, nessun vincolo. Chiama o scrivi su WhatsApp: AFRODITE.",
        'Arriva con il metodo già pronto'),
    albanese=[("Vjen me detyrat e bëra.", "DETYRAT E BËRA"), ("Vjen me protokoll, kartelë, seanca.", "PROTOKOLL · KARTELË · SEANCA"), ("Faqe pas faqeje.", ""),
              ("Dhjetë deri në dymbëdhjetë seanca: çfarë bën, me cilët parametra.", "10-12 SEANCA"),
              ("Asistencë gjithmonë. Pesëdhjetë mijë lekë në muaj, asnjë detyrim.", "ASISTENCË GJITHMONË · 50.000 LEKË / MUAJ"),
              ("Telefono ose shkruaj në WhatsApp: AFRODITE. Ta tregoj.", "")],
    serve="Il protocollo Afrodite e la scheda di cabina stampati (ce li abbiamo). Il fascicolo si posa da 15 cm, da fermo.",
    note=["«10-12 sedute» è nel protocollo Afrodite (protocolli/DEMETRA): da riconfermare sul protocollo in uso."],
    cambi="Il colpo ora cade a 0 s con la frase corta «Compiti già fatti», e il perimetro dell'offerta (protocollo, scheda, sedute) arriva subito dopo, entro i 5 secondi. Invito con «Chiama o scrivi su WhatsApp» e «Te lo mostro».",
)

R['F4'] = dict(
    serie='A', campagna='Afrodite', titolo='Una riga in più nel listino', copertina='UNA RIGA IN PIÙ NEL LISTINO', parola='AFRODITE', gancio=2, sbam=2,
    chi='Giorgio (Italia) · Uarda (Albania)',
    concetto="Il listino dei trattamenti del centro: un timbro aggiunge una riga, «Rimodellamento corpo». Si chiama Afrodite.",
    stacchi=[
        (PP,  "Giorgio, in camera, il listino dei trattamenti in mano.", "Una riga in più nel listino.", ["UNA RIGA IN PIÙ NEL LISTINO"], 2.5, "silenzio"),
        (DET, "Un timbro cala sul listino, su una riga vuota: «RIMODELLAMENTO CORPO».", "Si chiama Afrodite.", ["RIMODELLAMENTO CORPO"], 2.5, "SBAM: il timbro sulla riga nuova · 0,5 s di silenzio"),
        (MB,  "In cabina, il dispositivo dietro.", "Rimodellamento, cellulite, ritenzione, tono.", [], 3.5, "—"),
        (DET, "Un dito sul listino, sulla riga nuova.", "Quattro tecnologie in un solo dispositivo.", ["4 TECNOLOGIE · 1 DISPOSITIVO"], 3.0, "—"),
        (CL,  "Il dispositivo in cabina.", "Arriva il primo. La paghi il trenta.", ["ARRIVA IL 1 · LA PAGHI IL 30"], 3.0, "—"),
        (PP,  "In camera.", "Cinquecento al mese. Chiama o scrivi su WhatsApp: AFRODITE.", ["500 € / MESE", "poi: CHIAMA O SCRIVI «AFRODITE» SU WHATSAPP"], 4.0, "—"),
    ],
    ad=("Una riga in più nel listino: rimodellamento corpo.\nRimodellamento, cellulite, ritenzione, tono: quattro tecnologie in un solo dispositivo. Arriva il 1, la paghi il 30. Nessun vincolo.\n500 € al mese. Chiama o scrivi su WhatsApp: AFRODITE.",
        'Una riga in più nel tuo listino'),
    albanese=[("Një rresht më shumë në listë.", "NJË RRESHT MË SHUMË NË LISTË"), ("Quhet Afrodite.", "RIMODELIM TRUPI"), ("Rimodelim, celulit, mbajtje uji, tonus.", ""),
              ("Katër teknologji në një pajisje të vetme.", "4 TEKNOLOGJI · 1 PAJISJE"), ("Vjen më 1. E paguan më 30.", "VJEN MË 1 · E PAGUAN MË 30"),
              ("Pesëdhjetë mijë lekë në muaj. Telefono ose shkruaj në WhatsApp: AFRODITE.", "50.000 LEKË / MUAJ")],
    serve="Un listino dei trattamenti stampato (anche finto, senza prezzi di nessuno) con una riga vuota in fondo, e un timbro.",
    note=["Niente pelle. Il listino è una scena: non si inquadrano prezzi veri di nessun centro.",
          "Rimodellamento, cellulite, ritenzione e tono sono le parole già approvate per Afrodite: niente promesse di risultato."],
    cambi="Reel nuovo (2 novembre).",
)

R['F5'] = dict(
    serie='A', campagna='Afrodite', titolo='Dieci timbri', copertina='UN CICLO: 10-12 SEDUTE', parola='AFRODITE', gancio=2, sbam=2,
    chi='Giorgio (Italia) · Uarda (Albania)',
    concetto="Un calendario del mese e un timbro: dieci colpi sempre più veloci, uno per ogni seduta di un ciclo. Il protocollo dice cosa fare in ognuna.",
    stacchi=[
        (PP,  "Giorgio, in camera.", "Un ciclo: dieci, dodici sedute.", ["CICLO: 10-12 SEDUTE"], 2.0, "silenzio"),
        (DET, "Il calendario del mese: il timbro cala sulle caselle una dopo l'altra, sempre più veloce.", "", ["1 · 2 · 3 · … · 10"], 3.0, "SBAM ×10, accelerando, il primo a 2,0 s: contano come un solo SBAM"),
        (MB,  "Giorgio, il calendario pieno di timbri alle spalle.", "Il protocollo dice cosa fare, seduta per seduta.", [], 3.5, "—"),
        (DET, "La scheda di valutazione, sul tavolo.", "La scheda di valutazione tiene il conto.", ["SCHEDA DI VALUTAZIONE"], 3.0, "—"),
        (PP,  "In camera.", "Assistenza sempre. Cinquecento al mese, nessun vincolo.", ["ASSISTENZA SEMPRE · 500 € / MESE"], 3.5, "—"),
        (CL,  "Il dispositivo, il calendario sul lettino.", "Chiama o scrivi su WhatsApp: AFRODITE. Te lo mostro.", ["CHIAMA O SCRIVI «AFRODITE» SU WHATSAPP"], 4.0, "—"),
    ],
    ad=("Un ciclo sono dieci-dodici sedute. Il protocollo ti dice cosa fare, la scheda di valutazione tiene il conto.\nAssistenza sempre. 500 € al mese, nessun vincolo.\nChiama o scrivi su WhatsApp: AFRODITE.",
        '10-12 sedute, protocollo incluso'),
    albanese=[("Një cikël: dhjetë deri në dymbëdhjetë seanca.", "CIKËL: 10-12 SEANCA"), ("", "1 · 2 · 3 · … · 10"), ("Protokolli thotë çfarë të bësh, seancë pas seance.", ""),
              ("Dhe kartela e vlerësimit mban llogarinë.", "KARTELA E VLERËSIMIT"), ("Asistencë gjithmonë. Pesëdhjetë mijë lekë në muaj, asnjë detyrim.", "ASISTENCË GJITHMONË · 50.000 LEKË / MUAJ"),
              ("Telefono ose shkruaj në WhatsApp: AFRODITE. Ta tregoj.", "")],
    serve="Un calendario del mese (anche con mese e anno, qui non importa), un timbro e un tampone. La scheda di cabina stampata.",
    note=["I dieci colpi si girano uno alla volta e si montano accelerando; il suono lo mette il montaggio.", "«10-12 sedute» è nel protocollo Afrodite: da riconfermare."],
    cambi="Reel nuovo (2 novembre).",
)

R['F6'] = dict(
    serie='A', campagna='Afrodite', titolo='Una parola sola', copertina='UNA PAROLA SOLA: AFRODITE', parola='AFRODITE', gancio=2, sbam=2,
    chi='Giorgio (Italia) · Uarda (Albania)',
    concetto="Lo schermo di WhatsApp: si scrive «AFRODITE» e si preme invio. Il suono dell'invio è il colpo. Una parola, e al resto pensiamo noi.",
    stacchi=[
        (PP,  "Giorgio, in camera, il telefono in mano.", "Una parola sola.", ["UNA PAROLA SOLA"], 2.0, "silenzio"),
        (DET, "Lo schermo di WhatsApp: si scrive «AFRODITE» e si preme invio.", "Al resto pensiamo noi.", ["AFRODITE"], 3.0, "SBAM: il suono dell'invio, forte · 0,5 s di silenzio"),
        (MB,  "Giorgio, in camera.", "Niente moduli da compilare. Ti risponde Giorgio.", [], 3.5, "—"),
        (DET, calendario(), "Arriva il primo. La paghi il trenta.", ["ARRIVA IL 1 · LA PAGHI IL 30"], 3.0, "—"),
        (CL,  "Il dispositivo in cabina.", "Nessun anticipo, nessun vincolo.", ["NESSUN ANTICIPO · NESSUN VINCOLO"], 3.0, "—"),
        (PP,  "In camera.", "Cinquecento al mese. Chiama o scrivi su WhatsApp: AFRODITE.", ["500 € / MESE", "poi: CHIAMA O SCRIVI «AFRODITE» SU WHATSAPP"], 4.0, "—"),
    ],
    ad=("Una parola sola: AFRODITE. Al resto pensiamo noi.\nArriva il 1, la paghi il 30. Nessun anticipo, nessun vincolo. Niente moduli da compilare.\n500 € al mese. Chiama o scrivi su WhatsApp: AFRODITE.",
        'Una parola sola: AFRODITE'),
    albanese=[("Një fjalë e vetme.", "NJË FJALË E VETME"), ("Për pjesën tjetër kujdesemi ne.", "AFRODITE"), ("Pa formularë për t'u plotësuar. Të përgjigjet Uarda.", ""),
              ("Vjen më 1. E paguan më 30.", "VJEN MË 1 · E PAGUAN MË 30"), ("Pa paradhënie, pa detyrim.", "PA PARADHËNIE · PA DETYRIM"),
              ("Pesëdhjetë mijë lekë në muaj. Telefono ose shkruaj në WhatsApp: AFRODITE.", "50.000 LEKË / MUAJ")],
    serve="Una registrazione dello schermo del telefono con la chat WhatsApp di NIPEC aperta e vuota, in cui si scrive la parola. Il calendario di L1.",
    note=["Nella registrazione non compaiono conversazioni vere né numeri di clienti: si parte da una chat nuova.",
          "In Albania lo stacco 3 lo dice Uarda («Ti risponde Uarda»)."],
    cambi="Reel nuovo (2 novembre).",
)

# =============================== SERIE B · PAGINA ===============================

R['P1'] = dict(
    serie='B', campagna='Pagina', titolo='Fermo. Non firmare.', copertina='FERMO. NON FIRMARE.', parola=None, gancio=2, sbam=1,
    chi='Giorgio',
    concetto="Il palmo sul tavolo e «Fermo!»: il reel si apre come un alt. Poi tre domande da fare prima di comprare un laser.",
    stacchi=[
        (PP,  "Giorgio, mano aperta davanti all'obiettivo, poi il palmo sul tavolo.", "Fermo!", ["FERMO."], 1.5, "SBAM: il palmo (a 0,9 s) · voce a 0 s · 0,5 s di silenzio"),
        (MB,  "Giorgio, serio.", "Prima di comprare un laser, fatti tre domande.", ["3 DOMANDE"], 3.5, "—"),
        (DET, "Un dito alzato. Il dispositivo, sfocato, dietro.", "Uno. Chi ti insegna a usarlo, dopo?", ["1 · CHI TI INSEGNA?"], 3.0, "—"),
        (PP,  "Due dita.", "Due. Se si ferma, in quanto ne hai un altro?", ["2 · SE SI FERMA?"], 4.5, "—"),
        (DET, "Tre dita; un foglio di contratto davanti.", "Tre. Se non va, quanto costa uscirne?", ["3 · QUANTO COSTA USCIRNE?"], 3.5, "—"),
        (MB,  "Giorgio, in camera.", "Se manca una risposta, non firmare ancora.", [], 3.0, "—"),
        (PP,  "Giorgio, in camera.", "Salvalo: ti servirà il giorno che scegli.", ["SALVALO"], 3.0, "—"),
    ],
    didascalia="Prima di comprare un laser, fatti tre domande: chi ti insegna a usarlo, cosa succede se si ferma, quanto costa uscirne. Salva questo reel per il giorno in cui scegli.",
    serve="Un tavolo, un foglio di contratto qualunque (anche vuoto), il dispositivo sullo sfondo. Il palmo si batte piano: il colpo lo mette il montaggio.",
    note=["Le tre domande sono le stesse dei reel adv: qui sono consigli, non offerta. Nessun prezzo, nessuna parola chiave."],
    cambi="Stacchi 2 e 4 allungati (3,5 e 4,5 s, sotto i 5) perché le frasi superavano le 2,5 parole al secondo. La parola d'apertura è anche la scritta («FERMO.») e la voce parte a 0 s, non dopo il palmo.",
)

R['P2'] = dict(
    serie='B', campagna='Pagina', titolo='Sotto il telo', copertina='COSA C\'È SOTTO IL TELO?', parola=None, gancio=3, sbam=3,
    chi='Giorgio',
    concetto="Un dispositivo coperto da un telo, un battito, un conto alla rovescia. Il telo vola via: sotto non c'è solo il dispositivo, c'è chi ti insegna a usarlo.",
    stacchi=[
        (CL,  "Stanza in penombra: un dispositivo coperto da un telo.", "Sotto il telo?", ["COSA C'È SOTTO IL TELO?"], 1.5, "un battito basso"),
        (DET, "Una mano afferra l'orlo del telo.", "Tre. Due. Uno.", [], 1.5, "tic, tic, tic"),
        (MB,  "Il telo vola via. Accanto al dispositivo, seduto, Giorgio con il protocollo in mano.", "Sorpresa.", ["C'È DI PIÙ."], 2.0, "SBAM: il telo (a 3,0 s esatti) · 0,5 s di silenzio"),
        (PP,  "Giorgio, in camera.", "Un dispositivo lo trovi ovunque.", [], 3.0, "—"),
        (DET, "Il protocollo, sfogliato.", "Quello che manca è chi ti spiega come usarlo.", [], 4.0, "—"),
        (MB,  "Giorgio e il dispositivo scoperto.", "Noi lo portiamo con protocollo, formazione, assistenza.", ["PROTOCOLLO · FORMAZIONE · ASSISTENZA"], 3.5, "—"),
        (PP,  "Giorgio, in camera.", "Segui la pagina per vedere come lavoriamo.", [], 3.0, "—"),
    ],
    didascalia="Sotto il telo non c'era solo un dispositivo. Un dispositivo lo trovi ovunque: quello che conta è chi ti spiega come usarlo. NIPEC: noleggio, formazione, assistenza.",
    serve="Un telo bianco grande, il dispositivo, il protocollo stampato. Giorgio seduto accanto al dispositivo prima del via, fuori campo dietro un pannello: sbuca nello stacco 3.",
    note=["Il colpo, cioè il telo, arriva esattamente al terzo secondo: non si sposta più in là."],
    cambi="La voce parte a 0 s («Sotto il telo?»): nella prima stesura i primi 1,5 s erano muti. Tolto «spesso» (affermazione generica); la chiusura è «Segui la pagina», senza forma in -ci.",
)

R['P3'] = dict(
    serie='B', campagna='Pagina', titolo="L'esame", copertina='IL CERTIFICATO NON SI COMPRA.', parola=None, gancio=2, sbam=2,
    chi='Uarda o la formatrice DEMETRA (da decidere con Giorgio)',
    concetto="Un timbro cala su un foglio bianco: «Il certificato non si compra. Si prende all'esame finale». La formazione NIPEC e DEMETRA, a tappe.",
    stacchi=[
        (PP,  "In camera.", "Il certificato non si compra.", ["NON SI COMPRA."], 2.0, "silenzio"),
        (DET, "Un timbro cala su un foglio bianco.", "Si prende all'esame finale.", ["ESAME FINALE"], 3.0, "SBAM: il timbro (a 2,0 s) · 0,5 s di silenzio"),
        (CL,  "La sala della formazione: lettino, dispositivo, partecipanti vestite, di spalle.", "La formazione NIPEC e DEMETRA va a tappe.", [], 3.5, "—"),
        (DET, "Il gesto con il manipolo, su un telo.", "Gesto per gesto.", ["GESTO PER GESTO"], 2.5, "—"),
        (MB,  "La formatrice, in cabina.", "Formazione a tappe. Esame finale. Certificato.", ["TAPPE · ESAME · CERTIFICATO"], 3.5, "—"),
        (PP,  "In camera.", "Lo usi tu. Noi siamo accanto a te.", [], 3.5, "—"),
        (MB,  "In camera, dalla vita in su.", "Mandalo a chi sta per scegliere.", ["MANDALO A UNA COLLEGA"], 3.0, "—"),
    ],
    didascalia="Il certificato non si compra: si prende all'esame finale. Formazione a tappe, gesto per gesto, con NIPEC e DEMETRA. Mandalo a chi sta per scegliere un dispositivo.",
    serve="Un timbro (anche finto) e un foglio bianco; le riprese del workshop del 26 ottobre (partecipanti di spalle, mai volti senza consenso).",
    note=["Il timbro è una scena: il foglio è vuoto, non è un certificato vero. Non si inquadra il nome di nessuna partecipante.",
          "«Esame finale» e «certificato» descrivono il percorso DEMETRA: non risultano nei documenti del repository, da confermare con DEMETRA prima di pubblicare."],
    cambi="Stacco 6 accorciato a «Lo usi tu. Noi siamo accanto a te.» (era sopra le 2,5 parole al secondo). Aggiunto il controllo di consenso sulle partecipanti e la conferma del percorso con DEMETRA.",
)

R['P4'] = dict(
    serie='B', campagna='Pagina', titolo="Cosa c'è nella scatola", copertina='GUARDA FINO IN FONDO.', parola=None, gancio=2, sbam=1,
    chi='Giorgio (Italia) · Uarda (Albania)',
    concetto="Una scatola si apre di scatto: «Guarda fino in fondo». Dentro, ciò che arriva con il dispositivo: protocollo, scheda di cabina, formazione. In fondo, un foglietto con il numero di chi risponde.",
    stacchi=[
        (DET, "Una scatola grande sul tavolo. Giorgio ne strappa il nastro: il coperchio scatta.", "Guarda fino in fondo.", ["GUARDA FINO IN FONDO"], 2.0, "SBAM: il coperchio (a 1,0 s) · voce a 0 s"),
        (MB,  "Giorgio, in camera, la scatola aperta davanti.", "In fondo c'è una sorpresa.", [], 3.0, "—"),
        (DET, "Dalla scatola, il protocollo.", "Il protocollo, pagina per pagina.", ["1 · IL PROTOCOLLO"], 2.5, "—"),
        (MB,  "Giorgio mostra la scheda di cabina.", "La scheda di cabina.", ["2 · LA SCHEDA DI CABINA"], 2.5, "—"),
        (PP,  "Giorgio, in camera.", "Il programma di formazione.", ["3 · LA FORMAZIONE"], 2.5, "—"),
        (DET, "Il fondo della scatola. Un foglietto con il numero scritto a mano.", "In fondo, il mio numero. Scrivi, rispondo io.", ["4 · IL NUMERO DI GIORGIO"], 3.5, "SBAM leggero: il foglietto"),
        (MB,  "Giorgio, la scatola aperta sul tavolo.", "Arriva con il dispositivo. Chiama o scrivi su WhatsApp.", ["+39 351 846 6025"], 4.0, "—"),
    ],
    didascalia="Cosa arriva insieme a un dispositivo NIPEC: il protocollo, la scheda di cabina, la formazione. E un numero di telefono, quello di Giorgio. Chiama o scrivi su WhatsApp: +39 351 846 6025.",
    serve="Una scatola di cartone da riempire per la scena, con protocollo, scheda di cabina e un foglietto scritto a mano sul fondo.",
    note=["Scena preparata: la scatola è un contenitore per il reel, non un imballo vero. Il foglietto lo scrive Giorgio in scena.",
          "Per l'Albania (deciso il 2 novembre): parla Uarda, il foglietto e la scritta hanno il suo numero, +355 69 212 9786."],
    cambi="Eliminati «ci scrivi» e «Scrivici» (forme in -ci): ora «Scrivi, rispondo io» e «Chiama o scrivi su WhatsApp». Aggiunto l'invito parlato nello stacco 7, con il numero in sovrimpressione.",
)

R['P5'] = dict(
    serie='B', campagna='Pagina', titolo='Falso', copertina='FALSO.', parola=None, gancio=2, sbam=2,
    chi='Giorgio',
    concetto="Due frasi che si sentono dire sui laser, due timbri rossi: FALSO. La verità sta nella frase finale: il dispositivo è metà del lavoro, l'altra metà è chi ti insegna.",
    stacchi=[
        (PP,  "Giorgio, in camera.", "Compri il dispositivo, arrivano le clienti.", ["COMPRI IL DISPOSITIVO, ARRIVANO LE CLIENTI"], 2.5, "—"),
        (DET, "Un timbro rosso cala sulla frase, scritta a mano su un foglio.", "Falso.", ["FALSO"], 2.5, "SBAM: il timbro (a 2,5 s) · 0,5 s di silenzio"),
        (MB,  "Giorgio, in camera.", "Arrivano se racconti cosa fai e lo usi bene.", [], 4.0, "—"),
        (CL,  "Giorgio e il dispositivo. Un secondo foglio sul lettino.", "Il dispositivo fa tutto da solo.", ["IL DISPOSITIVO FA TUTTO DA SOLO"], 2.5, "—"),
        (DET, "Il timbro cala di nuovo.", "Falso.", ["FALSO"], 2.0, "SBAM: il timbro, ancora (è il secondo e ultimo)"),
        (MB,  "Giorgio, in camera.", "Il dispositivo è metà. L'altra metà è chi ti insegna.", ["IL DISPOSITIVO È METÀ"], 4.5, "—"),
        (PP,  "Giorgio, in camera.", "Salvalo. Mandalo a una collega.", ["SALVALO"], 3.0, "—"),
    ],
    didascalia="Due falsi miti sul laser, due timbri. Il dispositivo è metà del lavoro: l'altra metà è chi ti insegna. Salvalo e mandalo a una collega.",
    serve="Un timbro rosso (anche finto) e due fogli scritti a mano con le due frasi. Il dispositivo sul lettino.",
    note=["Due SBAM, i due timbri: è il massimo. Il secondo timbro è identico al primo, ma in mezzo c'è un'inquadratura diversa: la regola «mai due uguali di fila» è rispettata."],
    cambi="Il primo falso mito è accorciato («Compri il dispositivo, arrivano le clienti»): il timbro cade a 2,5 s e non al limite dei 3. Frase finale più asciutta: «chi ti insegna».",
)

R['P6'] = dict(
    serie='B', campagna='Pagina', titolo='Cinque secondi', copertina='TI HO FERMATO.', parola=None, gancio=2, sbam=2,
    chi='Giorgio',
    concetto="Il reel parla a chi scrolla: «Ti ho fermato». Poi insegna la regola dei 5 secondi, la nostra, e alla fine dimostra che funziona: hai guardato fino a qui.",
    stacchi=[
        (PP,  "Giorgio, in camera, il pollice in aria come chi scrolla.", "Stai per scrollare. Lo so.", ["STAI PER SCROLLARE."], 2.0, "silenzio"),
        (DET, "Una sveglia da tavolo: la mano la batte di colpo, la lancetta parte.", "Ti ho fermato. Ora ascolta.", ["TI HO FERMATO"], 3.0, "SBAM: la sveglia (a 2,0 s) · 0,5 s di silenzio"),
        (MB,  "Giorgio, in camera.", "Uno: il vantaggio nei primi cinque secondi.", ["1 · IL VANTAGGIO, SUBITO"], 3.5, "—"),
        (DET, "Una mano alza cinque dita.", "Due: nessuno stacco oltre cinque secondi.", ["2 · MAI PIÙ DI 5 SECONDI"], 3.5, "—"),
        (CL,  "Giorgio al tavolo, l'inquadratura più larga del reel.", "Tre: dopo, cambi inquadratura.", ["3 · CAMBIA INQUADRATURA"], 2.5, "—"),
        (PP,  "Giorgio, in camera, sorride.", "Se funziona, hai guardato fino a qui.", ["HAI GUARDATO FINO A QUI"], 3.0, "SBAM leggero (secondo e ultimo)"),
        (MB,  "Giorgio, in camera.", "Salvalo. Provalo sul tuo prossimo reel.", ["SALVALO"], 3.0, "—"),
    ],
    didascalia="Cinque secondi per fermare un dito, cinque secondi per ogni stacco. La nostra regola per i reel: provala sul prossimo. Salvalo.",
    serve="Una sveglia da tavolo (o un cronometro). Il tavolo, un'inquadratura più larga per lo stacco 5.",
    note=["Il reel è fatto con la regola che racconta: se un'inquadratura ripete la precedente, il trucco non funziona."],
    cambi="Le tre regole sono numerate nella voce («Uno… Due… Tre…») come nella scritta, più corte e ritmate; il reel scende da 22 a 20,5 s. Il «Se funziona, hai guardato fino a qui» diventa la prova: l'unico SBAM leggero, dopo il colpo vero della sveglia (due in tutto).",
)

R['P7'] = dict(
    serie='B', campagna='Pagina', titolo='Rispondo io', copertina='CHI RISPONDE?', parola=None, gancio=2, sbam=2,
    chi='Giorgio (Italia) · Uarda (Albania)',
    concetto="«Scrivi a NIPEC. Chi risponde?» La notifica arriva forte, e la risposta è una persona: «Rispondo io».",
    stacchi=[
        (PP,  "Giorgio, in camera.", "Scrivi a NIPEC. Chi risponde?", ["CHI RISPONDE?"], 2.0, "silenzio"),
        (DET, "Un telefono con la chat WhatsApp di NIPEC: arriva una risposta, il pollice la tocca.", "Rispondo io.", ["RISPONDO IO."], 3.0, "SBAM: la notifica, forte · 0,5 s di silenzio"),
        (MB,  "Giorgio, in camera.", "Sono Giorgio. Rispondo dall'Italia, Uarda dall'Albania.", ["GIORGIO · ITALIA", "UARDA · ALBANIA"], 3.5, "—"),
        (DET, "Il telefono sul tavolo, lo schermo acceso.", "Non un modulo da compilare.", [], 3.0, "—"),
        (CL,  "Giorgio al tavolo, il dispositivo dietro.", "Parliamo di dispositivo, formazione, noleggio.", [], 3.0, "—"),
        (PP,  "Giorgio, in camera.", "Chiama o scrivi su WhatsApp: il numero è sullo schermo.", ["+39 351 846 6025"], 4.0, "—"),
    ],
    didascalia="Quando scrivi a NIPEC risponde una persona: Giorgio per l'Italia, Uarda per l'Albania. Chiama o scrivi su WhatsApp: +39 351 846 6025.",
    serve="Un telefono con una chat WhatsApp di prova (nessuna conversazione vera) da registrare, e il dispositivo sullo sfondo.",
    note=["Per l'Albania parla Uarda: «Sono Uarda. Rispondo dall'Albania, Giorgio dall'Italia», numero +355 69 212 9786.",
          "Non si promette un tempo di risposta: i quindici minuti della Campagna 500 sono un obiettivo interno, non una frase da dire in pubblico."],
    cambi="Reel nuovo (2 novembre).",
)

R['P8'] = dict(
    serie='B', campagna='Pagina', titolo='Cosa manca?', copertina='COSA MANCA IN QUESTA CABINA?', parola=None, gancio=2, sbam=2,
    chi='Giorgio',
    concetto="Una cabina ferma: lettino, dispositivo, carrello, un tavolino vuoto. «Cosa manca?» Un cerchio rosso cala sul tavolino: il protocollo.",
    stacchi=[
        (CL,  "Una cabina ferma: lettino, dispositivo acceso, carrello, un tavolino vuoto.", "Cosa manca in questa cabina?", ["COSA MANCA?"], 2.0, "silenzio"),
        (DET, "Un cerchio rosso si stampa sul tavolino vuoto, dove dovrebbe esserci il protocollo.", "Il protocollo.", ["IL PROTOCOLLO"], 3.0, "SBAM: il cerchio rosso · 0,5 s di silenzio"),
        (MB,  "Giorgio, in camera.", "Il dispositivo c'è. Manca il metodo.", [], 3.0, "—"),
        (DET, "La mano posa sul tavolino il protocollo e la scheda di cabina.", "Cosa fai, con quali parametri, in che ordine.", ["COSA · PARAMETRI · ORDINE"], 3.5, "—"),
        (PP,  "In camera.", "Con noi arriva scritto.", [], 3.0, "—"),
        (MB,  "Giorgio, il tavolino con il protocollo.", "Dimmi nei commenti cosa manca nella tua cabina.", [], 4.0, "—"),
    ],
    didascalia="Cosa manca in questa cabina? Il dispositivo c'è, ma senza metodo resta un dispositivo. Dimmi nei commenti cosa manca nella tua.",
    serve="Una cabina vera (o allestita): lettino, dispositivo, carrello e un tavolino VUOTO. Poi lo stesso tavolino con protocollo e scheda di cabina. Il cerchio rosso si fa in montaggio.",
    note=["Nessuna cliente, nessuna pelle."],
    cambi="Reel nuovo (2 novembre).",
)

R['P9'] = dict(
    serie='B', campagna='Pagina', titolo='Cinque risposte', copertina='5 DOMANDE · 5 RISPOSTE', parola=None, gancio=2, sbam=2,
    chi='Giorgio (Italia) · Uarda (Albania)',
    concetto="Cinque domande da fare prima di scegliere un laser, cinque risposte da un respiro. Il primo colpo è il timbro «NOI».",
    stacchi=[
        (PP,  "Giorgio, in camera.", "Cinque domande. Cinque risposte.", ["5 DOMANDE · 5 RISPOSTE"], 2.0, "silenzio"),
        (DET, "Un foglio con la prima domanda: «Chi mi insegna?». Un timbro «NOI» cala sulla risposta.", "Chi ti insegna? Noi.", ["CHI TI INSEGNA? NOI."], 3.0, "SBAM: il timbro «NOI» · 0,5 s di silenzio"),
        (MB,  "Giorgio, in camera.", "Se si ferma? In 48 ore, un altro.", ["SE SI FERMA? 48 ORE"], 3.5, "—"),
        (CL,  "Giorgio al tavolo, il dispositivo dietro.", "Chi risponde? Io.", ["CHI RISPONDE? GIORGIO"], 3.0, "—"),
        (DET, "Un foglio bianco.", "Vincoli? Nessuno.", ["VINCOLI? NESSUNO."], 3.0, "—"),
        (PP,  "In camera.", "E il protocollo? Arriva scritto.", ["IL PROTOCOLLO? SCRITTO."], 3.0, "—"),
        (MB,  "Giorgio, in camera.", "Altre domande? Chiedile nei commenti.", [], 3.0, "—"),
    ],
    didascalia="Cinque domande da fare prima di scegliere un laser, cinque risposte da un respiro: chi ti insegna, se si ferma, chi risponde, i vincoli, il protocollo. Altre domande? Chiedile nei commenti.",
    serve="Un tavolo, un foglio con le domande scritte a mano (una per stacco) e un timbro «NOI» (anche finto). Il dispositivo sullo sfondo.",
    note=["Per l'Albania: «Chi risponde? Uarda.»"],
    cambi="Reel nuovo (2 novembre).",
)

R['P10'] = dict(
    serie='B', campagna='Pagina', titolo='Il rumore', copertina='ASCOLTA.', parola=None, gancio=2, sbam=2,
    chi='Giorgio',
    concetto="Silenzio totale su un display nero: «Un laser fermo». Poi il bip e il ronzio del dispositivo che si accende: il colpo è il suono.",
    stacchi=[
        (DET, "Il display del dispositivo, spento, nero.", "Ascolta. Un laser fermo.", ["UN LASER FERMO"], 2.0, "silenzio assoluto"),
        (MB,  "Giorgio preme il tasto: il display si accende.", "", [], 3.0, "SBAM: il bip e il ronzio del dispositivo che si accende · 0,5 s di silenzio"),
        (PP,  "Giorgio, in camera.", "Questo è un laser che lavora.", ["UN LASER CHE LAVORA"], 3.5, "—"),
        (DET, "Il manipolo in titanio, da vicino.", "Quel rumore ci piace.", [], 3.0, "—"),
        (CL,  "Il dispositivo in cabina, acceso.", "Se si ferma, in 48 ore ne hai un altro.", ["48 ORE"], 4.0, "—"),
        (MB,  "Giorgio, in camera.", "Così il silenzio dura poco.", [], 3.0, "—"),
        (PP,  "In camera.", "Mandalo a chi ha un laser fermo.", ["MANDALO A UNA COLLEGA"], 3.0, "—"),
    ],
    didascalia="Un laser fermo non fa rumore. Un laser che lavora sì: ci piace sentirlo. Se si ferma, da noi in 48 ore ne hai un altro. Mandalo a chi ha un laser fermo.",
    serve="Il dispositivo, spento e poi acceso: il suono vero del bip e del ronzio va registrato da vicino, senza musica.",
    note=["Il suono del dispositivo è l'unico colpo: se il bip non si sente bene, si registra a parte.", "«48 ore» è nella Campagna 500."],
    cambi="Reel nuovo (2 novembre).",
)

R['P11'] = dict(
    serie='B', campagna='Pagina', titolo='La polvere', copertina='QUANTI NE HAI VISTI COSÌ?', parola=None, gancio=2, sbam=2,
    chi='Giorgio',
    concetto="Un dispositivo coperto da un telo grigio di polvere, in un angolo. La mano sbatte il telo: nuvola di polvere. «Dopo tre mesi.»",
    stacchi=[
        (CL,  "Un angolo della stanza: un dispositivo coperto da un telo grigio di polvere.", "Quanti ne hai visti così?", ["QUANTI NE HAI VISTI COSÌ?"], 2.0, "silenzio"),
        (DET, "Una mano sbatte il telo: nuvola di polvere.", "In un angolo, dopo tre mesi.", ["DOPO TRE MESI"], 3.0, "SBAM: il telo sbattuto, la polvere · 0,5 s di silenzio"),
        (MB,  "Giorgio, in camera, un po' di polvere sulle spalle.", "Non perché non funziona. Perché nessuno ha scritto il metodo.", [], 4.0, "—"),
        (DET, "Il dispositivo scoperto si accende.", "Con un protocollo, ha un lavoro da fare.", [], 3.5, "—"),
        (PP,  "In camera.", "Noi lo portiamo con il protocollo.", [], 3.0, "—"),
        (CL,  "Il dispositivo scoperto, pulito, in cabina.", "Mandalo a chi ha un angolo così.", ["MANDALO A CHI HA UN ANGOLO COSÌ"], 3.5, "—"),
    ],
    didascalia="Quanti dispositivi hai visto finire in un angolo? Non perché non funzionano: perché nessuno ha scritto il metodo. Noi lo portiamo con il protocollo. Mandalo a chi ha un angolo così.",
    serve="Un dispositivo coperto da un telo con sopra polvere finta (farina o borotalco, lontano dal dispositivo e dai suoi fori di aerazione), in un angolo. Poi lo stesso dispositivo pulito e acceso.",
    note=["La polvere finta si mette sul telo, mai sul dispositivo: si sbatte il telo lontano dal dispositivo.",
          "«Dopo tre mesi» è nel copione 7 della Campagna 500, approvato da Giorgio."],
    cambi="Reel nuovo (2 novembre).",
)

R['P12'] = dict(
    serie='B', campagna='Pagina', titolo='Tre cose che non ti diremo', copertina='3 COSE CHE NON TI DIREMO', parola=None, gancio=2, sbam=2,
    chi='Giorgio',
    concetto="Un timbro rosso «NO» sulle frasi che un venditore ti direbbe: quanto guadagnerai, che fa tutto da solo. La terza non ha il timbro: «che devi firmare».",
    stacchi=[
        (PP,  "Giorgio, in camera.", "Tre cose che non ti diremo.", ["3 COSE CHE NON TI DIREMO"], 2.5, "silenzio"),
        (DET, "Un timbro rosso «NO» cala sulla prima frase scritta a mano: «Quanto guadagnerai».", "Quanto guadagnerai.", ["QUANTO GUADAGNERAI"], 2.5, "SBAM: il timbro NO · 0,5 s di silenzio"),
        (MB,  "Giorgio, in camera.", "Non lo sappiamo. Dipende da te.", [], 3.0, "—"),
        (DET, "Il timbro cala sulla seconda frase: «Fa tutto da solo».", "Che fa tutto da solo.", ["FA TUTTO DA SOLO"], 2.5, "SBAM: il timbro NO, ancora (è il secondo e ultimo)"),
        (CL,  "Giorgio e il dispositivo.", "Lo usi tu. Noi ti insegniamo come.", [], 3.0, "—"),
        (DET, "Il foglio bianco sul tavolo, senza timbro.", "Che devi firmare un vincolo.", ["NESSUN VINCOLO"], 3.0, "—"),
        (MB,  "Giorgio, in camera.", "Un vincolo non c'è. Salvalo.", ["SALVALO"], 3.0, "—"),
    ],
    didascalia="Tre cose che non ti diremo: quanto guadagnerai, che il dispositivo fa tutto da solo, che devi firmare un vincolo. Il resto te lo diciamo volentieri.",
    serve="Un timbro rosso «NO» (anche finto), due fogli scritti a mano e un foglio bianco. Il dispositivo sullo sfondo.",
    note=["Due SBAM, i due timbri. Il terzo punto è senza colpo, di proposito: è quello che resta."],
    cambi="Reel nuovo (2 novembre).",
)

# ----- calcolo e controlli
def stacchi(c):
    t, out = 0.0, []
    for k, (inq, vede, parla, schermo, dur, suono) in enumerate(R[c]['stacchi'], 1):
        out.append(dict(n=k, t0=t, t1=t + dur, dur=dur, inq=inq, vede=vede, parla=parla, schermo=schermo, suono=suono, parole=parole(parla)))
        t += dur
    return out

def fine(c):
    return stacchi(c)[-1]['t1']

VIETATE = [(r'macchin', 'macchina: si dice «dispositivo»'), (r'\bLED\b', 'LED: si dice «low laser»'), (r'cavitaz', 'cavitazione: si dice «ultrasuono focalizzato direzionale»'),
           (r'%', 'percentuali'), (r'prima\s*[/e]\s*dopo|before|after', 'prima/dopo'), (r'\bdiod', 'diodi'), (r'\bwatt\b', 'watt'),
           (r'\b(scrivici|seguici|chiamaci|contattaci|telefonaci|mandaci|dicci|vienici|chiedici)\b', "imperativo in -ci: si dice «Chiama o scrivi», «Segui la pagina»")]

def testi(c):
    r = R[c]; out = [r['concetto'], r['serve'], *r['note'], r['copertina']]
    for s in stacchi(c): out += [s['vede'], s['parla'], *s['schermo'], s['suono']]
    if r['serie'] == 'A': out += [r['ad'][0], r['ad'][1]]
    else: out.append(r['didascalia'])
    return out

def controlla():
    ok = True
    for c in CODICI:
        r = R[c]; st = stacchi(c)
        def no(msg):
            nonlocal ok
            print(f'{c}: {msg}'); ok = False
        for a, b in zip(st, st[1:]):
            if a['inq'] == b['inq']: no(f'stacchi {a["n"]} e {b["n"]} hanno la stessa inquadratura ({a["inq"]})')
        for s in st:
            if s['dur'] > 5.0: no(f'stacco {s["n"]} dura {s["dur"]} s')
            if s['parole'] and s['parole'] / s['dur'] > MAX_PAROLE_AL_SECONDO: no(f'stacco {s["n"]} troppo veloce ({s["parole"]} parole in {s["dur"]} s)')
        if not st[0]['parla']: no('il primo stacco non ha la voce: deve partire entro 0,5 s')
        if st[r['gancio'] - 1]['t1'] > 5.0: no(f'il gancio finisce a {st[r["gancio"] - 1]["t1"]} s')
        if st[r['sbam'] - 1]['t0'] > 3.0: no(f'lo SBAM comincia a {st[r["sbam"] - 1]["t0"]} s: deve cadere entro 3 s')
        if not st[r['sbam'] - 1]['suono'].startswith('SBAM'): no('lo stacco dello SBAM non ha il suono SBAM')
        n_sbam = sum(1 for s in st if s['suono'].startswith('SBAM'))
        if n_sbam > 2: no(f'{n_sbam} stacchi con SBAM: al massimo due')
        if not 15.0 <= fine(c) <= 22.0: no(f'il copione dura {fine(c)} s: tra 15 e 22')
        if r['parola'] and not (f'{CTA}: {r["parola"]}' in st[-1]['parla']): no(f'l\'ultimo stacco non dice «{CTA}: {r["parola"]}»')
        if r['serie'] == 'A':
            if len(r['ad'][1]) > 40: no(f'titolo troppo lungo ({len(r["ad"][1])} caratteri)')
            if len(r['albanese']) != len(st): no(f'la versione albanese ha {len(r["albanese"])} righe, il copione {len(st)} stacchi')
        for t in testi(c) + ([x for riga in r.get('albanese', []) for x in riga] if r['serie'] == 'A' else []):
            for rx, perche in VIETATE:
                if re.search(rx, t, re.I): no(f'parola vietata ({perche}): «{t[:60]}»')
    return ok

# ----- testi comuni ai copioni e al documento stampato (una sola fonte)
COLPO = {
    'L1': "Trenta pagine di calendario strappate in un colpo", 'L2': "Il portellone del furgone che si spalanca", 'L3': "Il lampo sull'obiettivo della telecamera",
    'L4': "L'adesivo «500 €» schiacciato sul dispositivo", 'L5': "Il foglio «VINCOLO» strappato in due", 'L6': "Tre appoggi a ritmo: laser, protocollo, formazione",
    'F1': "Il palmo sul tavolo: «Non comprare» diventa «Noleggiala»", 'F2': "Quattro manipoli, quattro colpi a ritmo", 'F3': "Il fascicolo del protocollo sul tavolo",
    'F4': "Il timbro sulla riga nuova del listino", 'F5': "Dieci timbri sul calendario, sempre più veloci", 'F6': "Il suono dell'invio su WhatsApp",
    'P1': "Il palmo sul tavolo: «Fermo!»", 'P2': "Il telo che vola via", 'P3': "Il timbro sul foglio bianco", 'P4': "Il coperchio della scatola che scatta",
    'P5': "Due timbri: FALSO", 'P6': "La sveglia battuta: «Ti ho fermato»", 'P7': "La notifica: «Rispondo io»", 'P8': "Il cerchio rosso sul tavolino vuoto",
    'P9': "Il timbro «NOI»", 'P10': "Il bip del dispositivo che si accende", 'P11': "Il telo sbattuto, la polvere", 'P12': "Il timbro «NO» sulle frasi del venditore",
}

REGOLE = [
    "Il vantaggio intero sta nei primi 5 secondi; la voce parte entro 0,5 s.",
    "SBAM entro i primi 3 secondi, al massimo due per reel; mezzo secondo di silenzio dopo il colpo.",
    "Nessuno stacco oltre 5 secondi; mai due inquadrature uguali di fila.",
    "Parlato sotto le 2,5 parole al secondo, verificato stacco per stacco.",
    "Parole evitate: «macchina», «LED», «cavitazione», percentuali, prima/dopo, modello del laser, diodi, watt. Nessun volto senza consenso.",
    "Forme dirette: «Chiama o scrivi su WhatsApp», mai l'imperativo con «ci» (scrivici, seguici…).",
    "Ogni dato che non risulta nei documenti di NIPEC è segnato «da confermare».",
]

DECISIONI = [
    ("2 novembre 2026", "Afrodite parte anche in Italia, non solo in Albania."),
    ("2 novembre 2026", "Servono più di dodici reel: da dodici a ventiquattro (dodici adv, dodici pagina)."),
    ("2 novembre 2026", "In P4, per l'Albania, il foglietto ha il numero di Uarda."),
]

SBAM = [
    ("Cos'è", "Un colpo secco, in immagine e in suono, che cade entro i primi 3 secondi. Serve a una cosa sola: fermare il dito che scrolla."),
    ("Suono", "Un colpo breve e grave (0,3 s), seguito da mezzo secondo di silenzio: il silenzio è quello che lo fa sentire. Dove c'è un suono vero (portellone, palmo sul tavolo, timbro, strappo di fogli, notifica) si usa quello, alzato in montaggio. Altrimenti un colpo senza diritti: si può generare."),
    ("Immagine", "Un lampo bianco di 2 fotogrammi (a 30 fps), la scossa dell'inquadratura per 6 fotogrammi, e la scritta che arriva al 130% e si assesta al 100% in 4 fotogrammi."),
    ("Quanti", "Al massimo due per reel. Quattro, tre o dieci colpi a ritmo (F2, L6, F5) contano come uno."),
    ("Con la musica", "La base musicale si ferma 0,2 s prima del colpo e riparte subito dopo."),
    ("Sicurezza", "Niente si rompe e niente cade davvero: i manipoli e il dispositivo si appoggiano piano, il colpo lo mette il montaggio. Al massimo un lampo bianco al secondo, per chi è sensibile alla luce."),
    ("Mai", "Urla, glitch continui, scritte che tremano per tutto il reel. Il colpo è uno: il resto sta fermo."),
]

ORDINE = [
    ("Prima la pagina", "Serie B: i primi sei reel (P1, P5, P2, P3, P4, P6) sono le sei pubblicazioni che la pagina NIPEC deve avere prima di poter sponsorizzare (Campagna 500). Due a settimana. Gli altri sei (P12, P9, P7, P8, P10, P11) continuano il ritmo."),
    ("Poi il laser", "Serie A, laser, Italia per prima: L1 (dice tutta l'offerta nei primi 5 secondi), poi L4, L2, L5, L3, L6. L'Albania segue con gli stessi, detti da Uarda."),
    ("Dopo due settimane, Afrodite, in Italia e in Albania", "F1, F6, F2, F4, F3, F5. Stesso criterio: i più netti per primi."),
]

ALBANIA = [
    ("Chi parla", "Uarda. Il copione resta in italiano finché il testo albanese non è approvato; i sottotitoli riportano quello che si sente davvero. Le versioni albanesi sono bozze: da far controllare a Uarda prima dell'uso."),
    ("Il prezzo", "«500 € / MESE» diventa «50.000 LEKË / MUAJ»; a voce «cinquantamila lekë al mese»."),
    ("L1, stacco 3", "«prima del primo euro» diventa «para lekut të parë»."),
    ("Il numero", "WhatsApp di Uarda: +355 69 212 9786. In P4 e P7 è il numero sul foglietto e sullo schermo."),
    ("Le parole di Afrodite", "In F2 la scritta «ULTRASUONO FOCALIZZATO DIREZIONALE» in albanese è «ULTRATINGULL I FOKUSUAR»: da far controllare a Uarda."),
    ("La parola chiave", "Resta LASER o AFRODITE, scritta così in WhatsApp."),
    ("Afrodite in Italia", "Stessi copioni, stesso prezzo (500 € al mese), parla Giorgio. Numero: +39 351 846 6025."),
]

if __name__ == '__main__':
    if controlla():
        for c in CODICI:
            st = stacchi(c); r = R[c]
            print(f'{c} · {r["titolo"]}: {len(st)} stacchi, il più lungo {max(s["dur"] for s in st)} s, il gancio finisce a {st[r["gancio"]-1]["t1"]} s, '
                  f'lo SBAM comincia a {st[r["sbam"]-1]["t0"]} s, il copione finisce a {fine(c)} s')
    else:
        raise SystemExit(1)
