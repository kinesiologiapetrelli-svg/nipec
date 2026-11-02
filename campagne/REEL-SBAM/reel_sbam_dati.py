#!/usr/bin/env python3
"""I dodici reel «SBAM», stacco per stacco. E' la fonte unica: da qui nascono i copioni (copioni/*.md) e il documento stampato.

Due serie:
  A · adv   sei reel per le inserzioni: tre sul laser (L1-L3), tre su Afrodite (F1-F3). Portano a WhatsApp.
  B · pagina  sei reel per la pagina Instagram/Facebook di NIPEC (P1-P6). Non vendono: fanno fermare il dito e fanno ricordare chi siamo.

LA REGOLA DEI 5 SECONDI (la solita, in due meta') + una terza cosa, che qui e' il punto:
  1. i primi 5 secondi contengono il vantaggio intero;
  2. nessuno stacco dura piu' di 5 secondi: dopo, si cambia stacco E inquadratura;
  3. SBAM: in ogni reel c'e' un colpo, o una sorpresa, che cade entro i primi 3 secondi. E' il motivo per cui il dito si ferma.

Ogni stacco: (inquadratura, cosa si vede, cosa si dice, scritte a schermo, durata in secondi, suono).
Le parole sono scritte per essere dette da Giorgio (Italia) o da Uarda (Albania, tradotte dopo l'approvazione).

Controlli (python3 reel_sbam_dati.py): nessuno stacco oltre 5 s, due stacchi di fila con inquadrature diverse, gancio dentro i 5 secondi,
SBAM che cade entro 3 s, ritmo del parlato non oltre 3,7 parole al secondo, al massimo due SBAM per reel,
durata del copione tra 15 e 22 secondi, parole vietate (macchina, LED, cavitazione, percentuali, prima/dopo, diodi, watt).
"""
import math, os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'REEL-500'))
from reel_dati import PP, MB, DET, CL, QUADRO, parole, fmt  # noqa: E402

CODICI = ['L1', 'L2', 'L3', 'F1', 'F2', 'F3', 'P1', 'P2', 'P3', 'P4', 'P5', 'P6']

# parola chiave, scheda finale (le tre schede di REEL-500/schede-finali), prezzo
OFFERTA = {'IT': '500 € al mese', 'AL': '50.000 lekë al mese'}

R = {}

# =============================== SERIE A · ADV ===============================

R['L1'] = dict(
    serie='A', campagna='Laser', titolo='Trenta pagine in un colpo', parola='LASER', gancio=2, sbam=2,
    chi='Giorgio (Italia) · Uarda (Albania)',
    concetto="Un calendario a fogli giornalieri: la mano strappa tutte le pagine dal 1 al 30 in un colpo solo. Lo strappo è il colpo, e dice l'offerta: arriva il 1, lo paghi il 30.",
    stacchi=[
        (PP,  "Giorgio, in camera, il calendario a fogli giornalieri accanto al viso.", "Il dispositivo arriva il primo.", ["ARRIVA IL 1"], 2.0, "silenzio, solo il fruscio dei fogli"),
        (DET, "La mano afferra tutte le pagine dal 1 al 30 e le strappa in un colpo solo.", "E lo paghi il trenta.", ["LO PAGHI IL 30"], 3.0, "SBAM: lo strappo, secco"),
        (MB,  "Giorgio posa le pagine strappate sul tavolo, guarda in camera.", "Trenta giorni di lavoro prima del primo euro.", [], 3.0, "—"),
        (CL,  "Giorgio e il dispositivo in cabina.", "E se ad agosto chiudi, me lo ridai: quel mese non paghi.", [], 3.5, "—"),
        (DET, "Sul tavolo, un foglio bianco. La mano lo liscia.", "Zero anticipo. Zero cauzione. Nessun vincolo.", ["ZERO ANTICIPO · ZERO CAUZIONE", "NESSUN VINCOLO"], 2.5, "—"),
        (PP,  "Giorgio, in camera.", "Cinquecento al mese. Scrivimi LASER.", ["500 € / MESE", "SCRIVI «LASER»"], 3.0, "—"),
    ],
    ad=("Il dispositivo arriva il 1. Lo paghi il 30.\nUn mese intero di lavoro prima di tirare fuori il primo euro. Zero anticipo, zero cauzione, nessun vincolo.\n500 € al mese. Scrivimi «LASER».",
        'Arriva il 1. Lo paghi il 30'),
    serve="Un calendario a fogli giornalieri (quello a blocchetto, un foglio per giorno), con il blocco dal 1 al 30; niente mese e niente anno stampati, così il reel regge tutti i mesi. Un foglio bianco.",
    note=["Se i fogli non si strappano tutti insieme, si strappa il blocco intero dalla base: conta il gesto e il suono, non i trenta fogli veri."],
)

R['L2'] = dict(
    serie='A', campagna='Laser', titolo='Fermo', parola='LASER', gancio=2, sbam=2,
    chi='Giorgio (Italia) · Uarda (Albania)',
    concetto="Il display si spegne di colpo, silenzio. Poi il portellone del furgone si spalanca: è il colpo vero, senza effetti. Dice il muletto in 48 ore.",
    stacchi=[
        (DET, "Il display acceso del dispositivo, in cabina. Di colpo, nero.", "Domani mattina si ferma.", ["SI FERMA."], 2.0, "un bip, poi mezzo secondo di silenzio"),
        (CL,  "Stacco: il portellone del furgone si spalanca, il dispositivo scende.", "In 48 ore ne hai un altro.", ["48 ORE"], 3.0, "SBAM: il portellone, vero"),
        (PP,  "Giorgio, in camera.", "Non chiudi un'ora. Non disdici nessuna cliente.", [], 3.0, "—"),
        (MB,  "Giorgio, il dispositivo dietro di lui.", "Un laser fermo una settimana sono dodici clienti che saltano il turno.", [], 4.0, "—"),
        (DET, "Il display del dispositivo sostitutivo, acceso.", "Il rischio non è tuo. È nostro.", ["IL RISCHIO È NOSTRO"], 2.5, "—"),
        (PP,  "Giorgio, in camera.", "Cinquecento al mese, nessun vincolo. Scrivimi LASER.", ["500 € / MESE", "SCRIVI «LASER»"], 3.0, "—"),
    ],
    ad=("Domani mattina il tuo laser si ferma. E adesso?\nDa noi, in 48 ore hai un altro dispositivo in cabina: non chiudi un'ora, non disdici nessuna cliente.\n500 € al mese, nessun vincolo. Scrivimi «LASER».",
        'Se si ferma, 48 ore e ne hai un altro'),
    serve="Il furgone con il portellone che si apre (il suono vero è il colpo). Un dispositivo che si spegne e si riaccende, e un altro accanto, per il display sostitutivo.",
    note=["Il portellone va sbattuto davvero, ma con la camera già in registrazione: non si ripete bene. Meglio due riprese."],
)

R['L3'] = dict(
    serie='A', campagna='Laser', titolo='Ti sta guardando', parola='LASER', gancio=2, sbam=1,
    chi='Giorgio (Italia) · Uarda (Albania)',
    concetto="Primissimo piano sull'obiettivo della telecamera del dispositivo, un lampo: «TI STA GUARDANDO». Poi la spiegazione: guarda la pelle e propone i parametri, decidi sempre tu.",
    stacchi=[
        (DET, "Primissimo piano sull'obiettivo della telecamera del dispositivo. Un lampo bianco.", "", ["TI STA GUARDANDO"], 1.5, "SBAM: un click e il lampo"),
        (PP,  "Giorgio, in camera. Gira lo sguardo verso l'obiettivo e torna in camera.", "È una telecamera: guarda la pelle e ti propone i parametri.", ["TELECAMERA + IA"], 3.5, "—"),
        (DET, "La telecamera e il manipolo in titanio, da vicino.", "Decidi sempre tu.", ["DECIDI SEMPRE TU"], 2.5, "—"),
        (MB,  "Giorgio, il dispositivo accanto.", "Certificato in Italia, con MDR attivo.", ["CE ITALIANE · MDR ATTIVO"], 3.0, "—"),
        (CL,  "Il dispositivo in cabina, luce ferma.", "Un laser di ultima generazione, a noleggio.", [], 3.0, "—"),
        (PP,  "Giorgio, in camera.", "Cinquecento al mese. Scrivimi LASER.", ["500 € / MESE", "SCRIVI «LASER»"], 3.0, "—"),
    ],
    ad=("Il tuo prossimo laser ha una telecamera.\nGuarda la pelle e, con l'intelligenza artificiale, ti propone i parametri: decidi sempre tu. Certificato in Italia, MDR attivo.\n500 € al mese, nessun vincolo. Scrivimi «LASER».",
        'Telecamera e IA. Decidi sempre tu'),
    serve="Il dispositivo con il display acceso; un obiettivo della telecamera pulito, ripreso da 10 cm. Il lampo bianco si fa in montaggio.",
    note=["Non si mostra pelle: la telecamera si inquadra da sola, mai puntata su una cliente."],
)

R['F1'] = dict(
    serie='A', campagna='Afrodite', titolo='Non comprare Afrodite', parola='AFRODITE', gancio=2, sbam=2,
    chi='Giorgio (Italia) · Uarda (Albania)',
    concetto="Il contrario di quello che dice ogni inserzione: «Non comprare Afrodite». Il palmo batte sul tavolo, e la frase si ribalta: «Noleggiala».",
    stacchi=[
        (PP,  "In camera, serio, con la mano alzata come un alt.", "Non comprare Afrodite.", ["NON COMPRARE AFRODITE"], 2.0, "silenzio"),
        (DET, "La mano batte sul tavolo, accanto a un calendario.", "Noleggiala. Cinquecento al mese, nessun vincolo.", ["NOLEGGIALA", "500 € / MESE"], 3.0, "SBAM: il palmo sul tavolo"),
        (MB,  "In cabina, il dispositivo dietro.", "Prima di spendere, scopri se nel tuo centro lavora.", [], 3.5, "—"),
        (DET, "Il calendario: un dito va dal 1 al 30.", "Arriva il primo. La paghi il trenta.", ["ARRIVA IL 1 · LA PAGHI IL 30"], 2.5, "—"),
        (CL,  "Il dispositivo in cabina.", "Quattro tecnologie. Una rata sola.", [], 3.0, "—"),
        (PP,  "In camera.", "Nessun anticipo. Scrivimi AFRODITE.", ["SCRIVI «AFRODITE»"], 3.0, "—"),
    ],
    ad=("Non comprare Afrodite. Noleggiala.\nPrima di spendere, scopri se nel tuo centro lavora. Arriva il 1, la paghi il 30. Nessun anticipo, nessun vincolo.\n500 € al mese. Scrivimi «AFRODITE».",
        'Non comprarla. Noleggiala.'),
    serve="Un tavolo solido da battere con il palmo (si batte piano: il colpo vero lo mette il montaggio). Il calendario a fogli giornalieri di L1.",
    note=[],
)

R['F2'] = dict(
    serie='A', campagna='Afrodite', titolo='Quattro colpi', parola='AFRODITE', gancio=2, sbam=2,
    chi='Giorgio (Italia) · Uarda (Albania)',
    concetto="Quattro tecnologie, quattro colpi: quattro manipoli appoggiati sul lettino uno dopo l'altro, a ogni colpo il nome a schermo. Poi il dispositivo solo, una rata sola.",
    stacchi=[
        (PP,  "In camera, quattro dita alzate.", "Quattro tecnologie.", ["4 TECNOLOGIE"], 2.0, "silenzio"),
        (DET, "Quattro manipoli, appoggiati sul lettino uno dopo l'altro, a ritmo. A ogni appoggio, il nome a schermo.", "", ["ULTRASUONO", "RADIOFREQUENZA", "VACUUM", "LOW LASER"], 3.0, "SBAM SBAM SBAM SBAM: quattro colpi, uno ogni 0,7 secondi (contano come un solo SBAM)"),
        (MB,  "In cabina, ferma.", "Ultrasuono focalizzato direzionale, radiofrequenza, vacuum e low laser.", ["ULTRASUONO FOCALIZZATO DIREZIONALE"], 4.0, "—"),
        (CL,  "Il dispositivo intero, in cabina.", "Un dispositivo. Una rata.", [], 2.5, "—"),
        (DET, "Il calendario: arriva il 1, si paga il 30.", "Arriva il primo, la paghi il trenta.", ["ARRIVA IL 1 · LA PAGHI IL 30"], 2.5, "—"),
        (PP,  "In camera.", "Cinquecento al mese. Scrivimi AFRODITE.", ["500 € / MESE", "SCRIVI «AFRODITE»"], 3.0, "—"),
    ],
    ad=("Ultrasuono focalizzato direzionale, radiofrequenza, vacuum e low laser. Quattro tecnologie in un solo dispositivo, una rata sola.\nArriva il 1, la paghi il 30. Nessun vincolo.\n500 € al mese. Scrivimi «AFRODITE».",
        '4 tecnologie, 1 dispositivo, 1 rata'),
    serve="I quattro manipoli, luce radente, su un lettino con un telo bianco. Un montaggio che prende il tempo dai colpi: i quattro appoggi vanno girati a ritmo, uno ogni mezzo secondo.",
    note=["Niente pelle: solo i manipoli e il telo.",
          "I manipoli non si lasciano cadere: si appoggiano piano, a ritmo. Il colpo lo mette il montaggio.",
          "In albanese il nome a schermo è «ULTRATINGULL I FOKUSUAR»: da far controllare a Uarda."],
)

R['F3'] = dict(
    serie='A', campagna='Afrodite', titolo='I compiti già fatti', parola='AFRODITE', gancio=2, sbam=1,
    chi='Giorgio (Italia) · Uarda (Albania)',
    concetto="Un fascicolo spesso cade sul tavolo: il protocollo. «Arriva con i compiti già fatti». Poi cosa c'è dentro: protocollo, scheda di valutazione, ciclo di sedute.",
    stacchi=[
        (DET, "Un fascicolo spesso cade sul tavolo: il protocollo stampato.", "Arriva con i compiti già fatti.", ["I COMPITI GIÀ FATTI"], 2.0, "SBAM: il fascicolo sul tavolo"),
        (PP,  "In camera.", "Protocollo, scheda di valutazione, ciclo di sedute.", ["PROTOCOLLO · SCHEDA · SEDUTE"], 3.0, "—"),
        (DET, "Le pagine del protocollo, sfogliate.", "Pagina per pagina.", [], 2.5, "—"),
        (MB,  "Al tavolo, il protocollo e la scheda di cabina.", "Dieci-dodici sedute: cosa fai, con quali parametri, in che ordine.", ["10-12 SEDUTE"], 4.0, "—"),
        (PP,  "In camera.", "E l'assistenza c'è sempre. Cinquecento al mese, nessun vincolo.", ["ASSISTENZA SEMPRE", "500 € / MESE"], 3.5, "—"),
        (CL,  "Il dispositivo, il protocollo sul lettino.", "Scrivimi AFRODITE e te lo faccio vedere.", ["SCRIVI «AFRODITE»"], 3.0, "—"),
    ],
    ad=("Il dispositivo arriva con i compiti già fatti: protocollo scritto, scheda di valutazione e un ciclo di 10-12 sedute. Assistenza sempre.\n500 € al mese, nessun vincolo. Scrivimi «AFRODITE».",
        'Arriva con il metodo già pronto'),
    serve="Il protocollo Afrodite e la scheda di cabina stampati (ce li abbiamo). Il fascicolo si lascia cadere da 15 cm, da fermo.",
    note=[],
)

# =============================== SERIE B · PAGINA ===============================

R['P1'] = dict(
    serie='B', campagna='Pagina', titolo='Fermo. Non firmare.', parola=None, gancio=2, sbam=1,
    chi='Giorgio',
    concetto="Il palmo sul tavolo e «Fermo!»: il reel si apre come un alt. Poi tre domande da fare prima di comprare un laser.",
    stacchi=[
        (PP,  "Giorgio, mano aperta davanti all'obiettivo, poi il palmo sul tavolo.", "Fermo!", ["FERMO."], 1.5, "SBAM: il palmo"),
        (MB,  "Giorgio, serio.", "Prima di comprare un laser, fatti tre domande.", ["3 DOMANDE"], 3.0, "—"),
        (DET, "Un dito alzato. Il dispositivo, sfocato, dietro.", "Uno. Chi ti insegna a usarlo, dopo?", ["1 · CHI TI INSEGNA?"], 3.0, "—"),
        (PP,  "Due dita.", "Due. Se si ferma, in quanto ne hai un altro?", ["2 · SE SI FERMA?"], 3.5, "—"),
        (DET, "Tre dita; un foglio di contratto davanti.", "Tre. Se non va, quanto ti costa uscirne?", ["3 · QUANTO COSTA USCIRNE?"], 3.0, "—"),
        (MB,  "Giorgio, in camera.", "Se una risposta manca, non firmare ancora.", [], 3.0, "—"),
        (PP,  "Giorgio, in camera.", "Salvalo: ti servirà il giorno che scegli.", ["SALVALO"], 3.0, "—"),
    ],
    didascalia="Prima di comprare un laser, fatti tre domande: chi ti insegna a usarlo, cosa succede se si ferma, quanto ti costa uscirne. Salva questo reel per il giorno in cui scegli.",
    serve="Un tavolo, un foglio di contratto qualunque (anche vuoto), il dispositivo sullo sfondo. Il palmo si batte piano: il colpo lo mette il montaggio.",
    note=["Le tre domande sono le stesse dei reel adv: qui sono consigli, non offerta. Nessun prezzo, nessuna parola chiave."],
)

R['P2'] = dict(
    serie='B', campagna='Pagina', titolo='Sotto il telo', parola=None, gancio=3, sbam=3,
    chi='Giorgio',
    concetto="Un dispositivo coperto da un telo, un battito, un conto alla rovescia. Il telo vola via: sotto non c'è solo il dispositivo, c'è chi ti insegna a usarlo.",
    stacchi=[
        (CL,  "Una stanza in penombra: un dispositivo coperto da un telo.", "", ["COSA C'È SOTTO IL TELO?"], 1.5, "un battito basso"),
        (DET, "Una mano afferra l'orlo del telo.", "Tre, due, uno.", [], 1.5, "tic, tic, tic"),
        (MB,  "Il telo vola via. Accanto al dispositivo, seduto, Giorgio con il protocollo in mano.", "Sorpresa.", ["C'È DI PIÙ."], 2.0, "SBAM: il telo"),
        (PP,  "Giorgio, in camera.", "Un dispositivo lo trovi ovunque.", [], 3.0, "—"),
        (DET, "Il protocollo, sfogliato.", "Quello che spesso manca è chi ti spiega come usarlo.", [], 3.5, "—"),
        (MB,  "Giorgio e il dispositivo scoperto.", "Noi te lo portiamo insieme: protocollo, formazione, assistenza.", ["PROTOCOLLO · FORMAZIONE · ASSISTENZA"], 3.0, "—"),
        (PP,  "Giorgio, in camera.", "Seguici per vedere come lavoriamo.", [], 2.5, "—"),
    ],
    didascalia="Sotto il telo non c'era solo un dispositivo. Un dispositivo lo trovi ovunque: quello che conta è chi ti spiega come usarlo. NIPEC: noleggio, formazione, assistenza.",
    serve="Un telo bianco grande, il dispositivo, il protocollo stampato. Giorgio seduto accanto al dispositivo prima del via, fuori campo, dietro un pannello: sbuca nello stacco 3.",
    note=["Il colpo, cioè il telo, arriva esattamente al terzo secondo: non si sposta più in là, o il reel perde il gancio."],
)

R['P3'] = dict(
    serie='B', campagna='Pagina', titolo="L'esame", parola=None, gancio=2, sbam=2,
    chi='Uarda o la formatrice DEMETRA',
    concetto="Un timbro cala su un foglio bianco: «Il certificato non si compra. Si prende all'esame finale». La formazione NIPEC e DEMETRA, a tappe.",
    stacchi=[
        (PP,  "In camera.", "Il certificato non si compra.", ["NON SI COMPRA."], 2.0, "silenzio"),
        (DET, "Un timbro cala su un foglio bianco.", "Si prende all'esame finale.", ["ESAME FINALE"], 3.0, "SBAM: il timbro"),
        (CL,  "La sala della formazione: lettino, dispositivo, partecipanti vestite, di spalle.", "La formazione NIPEC e DEMETRA va a tappe.", [], 3.0, "—"),
        (DET, "Il gesto con il manipolo, su un telo.", "Gesto per gesto.", ["GESTO PER GESTO"], 2.5, "—"),
        (MB,  "La formatrice, in cabina.", "Formazione a tappe. Esame finale. Certificato.", ["TAPPE · ESAME · CERTIFICATO"], 3.5, "—"),
        (PP,  "In camera.", "Il dispositivo lo usi tu. Noi restiamo accanto a te.", [], 3.0, "—"),
        (MB,  "In camera, dalla vita in su.", "Mandalo a chi sta per scegliere un dispositivo.", ["MANDALO A UNA COLLEGA"], 3.0, "—"),
    ],
    didascalia="Il certificato non si compra: si prende all'esame finale. Formazione a tappe, gesto per gesto, con NIPEC e DEMETRA. Mandalo a chi sta per scegliere un dispositivo.",
    serve="Un timbro (anche finto) e un foglio bianco; le riprese del workshop del 26 ottobre (partecipanti di spalle, mai volti senza consenso).",
    note=["Il timbro è una scena: il foglio è vuoto, non è un certificato vero. Non si inquadra il nome di nessuna partecipante."],
)

R['P4'] = dict(
    serie='B', campagna='Pagina', titolo='Cosa c\'è nella scatola', parola=None, gancio=2, sbam=1,
    chi='Giorgio',
    concetto="Una scatola si apre di scatto: «Guarda fino in fondo». Dentro, ciò che arriva con il dispositivo: protocollo, scheda di cabina, formazione. In fondo, un foglietto con il numero di Giorgio.",
    stacchi=[
        (DET, "Una scatola grande sul tavolo. Giorgio ne strappa il nastro: il coperchio si apre di scatto.", "Guarda fino in fondo.", ["GUARDA FINO IN FONDO"], 2.0, "SBAM: il coperchio"),
        (MB,  "Giorgio, in camera, la scatola aperta davanti.", "In fondo alla scatola c'è una sorpresa.", [], 3.0, "—"),
        (DET, "Dalla scatola, il protocollo.", "Il protocollo, scritto pagina per pagina.", ["1 · IL PROTOCOLLO"], 2.5, "—"),
        (MB,  "Giorgio mostra la scheda di cabina.", "La scheda di cabina.", ["2 · LA SCHEDA DI CABINA"], 2.5, "—"),
        (PP,  "Giorgio, in camera.", "Il programma di formazione.", ["3 · LA FORMAZIONE"], 2.5, "—"),
        (DET, "Il fondo della scatola. Un foglietto con un numero di telefono scritto a mano.", "E in fondo, il mio numero. Ci scrivi, rispondo io.", ["4 · IL NUMERO DI GIORGIO"], 3.0, "SBAM leggero: il foglietto"),
        (MB,  "Giorgio, la scatola aperta sul tavolo.", "Questa scatola arriva con il dispositivo.", [], 2.5, "—"),
    ],
    didascalia="Cosa arriva insieme a un dispositivo NIPEC: il protocollo, la scheda di cabina, la formazione. E un numero di telefono, quello di Giorgio. Scrivici su WhatsApp: +39 351 846 6025.",
    serve="Una scatola di cartone da riempire per la scena, con protocollo, scheda di cabina e un foglietto scritto a mano sul fondo. Il numero sul foglietto: quello di Giorgio.",
    note=["Scena preparata: la scatola è un contenitore per il reel, non un imballo vero. Il foglietto lo scrive Giorgio in scena.",
          "Per l'Albania: il numero sul foglietto è quello di Uarda."],
)

R['P5'] = dict(
    serie='B', campagna='Pagina', titolo='Falso', parola=None, gancio=2, sbam=2,
    chi='Giorgio',
    concetto="Due frasi che si sentono dire sui laser, due timbri rossi: FALSO. La verità sta nella frase finale: il dispositivo è metà del lavoro, l'altra metà è chi te lo insegna.",
    stacchi=[
        (PP,  "Giorgio, in camera.", "Basta comprare il dispositivo e le clienti arrivano.", ["«BASTA COMPRARE IL DISPOSITIVO E LE CLIENTI ARRIVANO»"], 3.0, "—"),
        (DET, "Un timbro rosso cala sulla frase, scritta a mano su un foglio.", "Falso.", ["FALSO"], 2.0, "SBAM: il timbro"),
        (MB,  "Giorgio, in camera.", "Arrivano se sai raccontare cosa fai e sai usarlo bene.", [], 3.5, "—"),
        (CL,  "Giorgio e il dispositivo. Un secondo foglio sul lettino.", "Il dispositivo fa tutto da solo.", ["«IL DISPOSITIVO FA TUTTO DA SOLO»"], 2.5, "—"),
        (DET, "Il timbro cala di nuovo.", "Falso.", ["FALSO"], 2.0, "SBAM: il timbro, ancora"),
        (MB,  "Giorgio, in camera.", "Il dispositivo è metà. L'altra metà è chi te lo insegna.", ["IL DISPOSITIVO È METÀ"], 3.5, "—"),
        (PP,  "Giorgio, in camera.", "Salvalo. Mandalo a una collega.", ["SALVALO"], 2.5, "—"),
    ],
    didascalia="Due falsi miti sul laser, due timbri. Il dispositivo è metà del lavoro: l'altra metà è chi te lo insegna. Salvalo e mandalo a una collega.",
    serve="Un timbro rosso (anche finto) e due fogli scritti a mano con le due frasi. Il dispositivo sul lettino.",
    note=["Due SBAM, i due timbri: è il massimo. Il secondo è identico al primo: è il gioco."],
)

R['P6'] = dict(
    serie='B', campagna='Pagina', titolo='Cinque secondi', parola=None, gancio=2, sbam=2,
    chi='Giorgio',
    concetto="Il reel parla a chi scrolla: «Ti ho fermato». Poi insegna la regola dei 5 secondi, la nostra, e alla fine dimostra che funziona: hai guardato fino a qui.",
    stacchi=[
        (PP,  "Giorgio, in camera, il pollice in aria come chi scrolla.", "Stai per scrollare. Lo so.", ["STAI PER SCROLLARE."], 2.0, "silenzio"),
        (DET, "Una sveglia da tavolo: la mano la batte di colpo, la lancetta parte.", "Ti ho fermato. Ora ascolta.", ["TI HO FERMATO"], 3.0, "SBAM: la sveglia"),
        (MB,  "Giorgio, in camera.", "Regola uno: il vantaggio sta nei primi cinque secondi.", ["1 · IL VANTAGGIO, SUBITO"], 3.5, "—"),
        (DET, "Una mano alza cinque dita.", "Regola due: nessuno stacco dura più di cinque secondi.", ["2 · MAI PIÙ DI 5 SECONDI"], 3.0, "—"),
        (CL,  "Giorgio al tavolo, l'inquadratura più larga del reel.", "Regola tre: dopo, cambi inquadratura.", ["3 · CAMBIA INQUADRATURA"], 3.0, "—"),
        (PP,  "Giorgio, in camera, sorride.", "Se la regola funziona, hai guardato fino a qui.", ["HAI GUARDATO FINO A QUI"], 3.0, "SBAM leggero"),
        (MB,  "Giorgio, in camera.", "Salvalo. Provalo sul tuo prossimo reel.", ["SALVALO"], 2.5, "—"),
    ],
    didascalia="Cinque secondi per fermare un dito, cinque secondi per ogni stacco. La nostra regola per i reel: provala sul prossimo. Salvalo.",
    serve="Una sveglia da tavolo (o un cronometro). Il tavolo, un'inquadratura più larga per lo stacco 5.",
    note=["Il reel è fatto con la regola che racconta: se un'inquadratura ripete la precedente, il trucco non funziona."],
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
           (r'%', 'percentuali'), (r'prima\s*[/e]\s*dopo|before|after', 'prima/dopo'), (r'\bdiod', 'diodi'), (r'\bwatt\b', 'watt')]

def testi(c):
    r = R[c]; out = [r['concetto'], r['serve'], *r['note']]
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
            if s['parole'] and s['parole'] / s['dur'] > 3.7: no(f'stacco {s["n"]} troppo veloce ({s["parole"]} parole in {s["dur"]} s)')
        if st[r['gancio'] - 1]['t1'] > 5.0: no(f'il gancio finisce a {st[r["gancio"] - 1]["t1"]} s')
        if st[r['sbam'] - 1]['t0'] > 3.0: no(f'lo SBAM comincia a {st[r["sbam"] - 1]["t0"]} s: deve cadere entro 3 s')
        if not st[r['sbam'] - 1]['suono'].startswith('SBAM'): no('lo stacco dello SBAM non ha il suono SBAM')
        n_sbam = sum(1 for s in st if s['suono'].startswith('SBAM'))
        if n_sbam > 2: no(f'{n_sbam} stacchi con SBAM: al massimo due')
        if not 15.0 <= fine(c) <= 22.0: no(f'il copione dura {fine(c)} s: tra 15 e 22')
        if r['parola'] and f'Scrivimi {r["parola"]}' not in st[-1]['parla']: no('l\'ultimo stacco non dice «Scrivimi ' + r['parola'] + '»')
        if r['serie'] == 'A' and len(r['ad'][1]) > 40: no(f'titolo troppo lungo ({len(r["ad"][1])} caratteri)')
        for t in testi(c):
            for rx, perche in VIETATE:
                if re.search(rx, t, re.I): no(f'parola vietata ({perche}): «{t[:60]}»')
    return ok

if __name__ == '__main__':
    if controlla():
        for c in CODICI:
            st = stacchi(c); r = R[c]
            print(f'{c} · {r["titolo"]}: {len(st)} stacchi, il più lungo {max(s["dur"] for s in st)} s, il gancio finisce a {st[r["gancio"]-1]["t1"]} s, '
                  f'lo SBAM comincia a {st[r["sbam"]-1]["t0"]} s, il copione finisce a {fine(c)} s')
    else:
        raise SystemExit(1)

# ----- testi comuni ai copioni e al documento stampato (una sola fonte)
SBAM = [
    ("Cos'è", "Un colpo secco, in immagine e in suono, che cade entro i primi 3 secondi. Serve a una cosa sola: fermare il dito che scrolla."),
    ("Suono", "Un colpo breve e grave (0,3 s), seguito da mezzo secondo di silenzio: il silenzio è quello che lo fa sentire. Dove c'è un suono vero (portellone, palmo sul tavolo, timbro, strappo di fogli) si usa quello, alzato in montaggio. Altrimenti un colpo senza diritti: si può generare."),
    ("Immagine", "Un lampo bianco di 2 fotogrammi (a 30 fps), la scossa dell'inquadratura per 6 fotogrammi, e la scritta che arriva al 130% e si assesta al 100% in 4 fotogrammi."),
    ("Quanti", "Al massimo due per reel. Quattro colpi a ritmo (F2) contano come uno."),
    ("Con la musica", "La base musicale si ferma 0,2 s prima del colpo e riparte subito dopo."),
    ("Sicurezza", "Niente si rompe e niente cade davvero: i manipoli e il dispositivo si appoggiano piano, il colpo lo mette il montaggio. Al massimo un lampo bianco al secondo, per chi è sensibile alla luce."),
    ("Mai", "Urla, glitch continui, scritte che tremano per tutto il reel. Il colpo è uno: il resto sta fermo."),
]

ORDINE = [
    ("Prima la pagina", "Serie B: sei reel sono sei pubblicazioni, il minimo che la pagina NIPEC deve avere prima di poter sponsorizzare (Campagna 500). Ordine consigliato: P1, P5, P2, P3, P4, P6, due a settimana."),
    ("Poi il laser", "Serie A, laser, Italia per prima: L1 (dice tutta l'offerta nei primi 5 secondi), poi L2, poi L3. L'Albania segue con gli stessi tre, detti da Uarda."),
    ("Dopo due settimane, Afrodite", "F1, F2, F3, come nella Campagna 500. Stesso ordine di forza: il più netto per primo."),
]

ALBANIA = [
    ("Chi parla", "Uarda. Il copione resta in italiano finché il testo albanese non è approvato; i sottotitoli riportano quello che si sente davvero."),
    ("Il prezzo", "«500 € / MESE» diventa «50.000 LEKË / MUAJ». A voce: «cinquantamila lekë al mese»."),
    ("L1, stacco 3", "«prima del primo euro» diventa «prima del primo lek»."),
    ("Il numero", "WhatsApp di Uarda: +355 69 212 9786. In P4 è il numero sul foglietto."),
    ("Le parole di Afrodite", "In F2 la scritta «ULTRASUONO FOCALIZZATO DIREZIONALE» in albanese è «ULTRATINGULL I FOKUSUAR»: da far controllare a Uarda."),
    ("La parola chiave", "Resta LASER o AFRODITE, scritta così in WhatsApp."),
]

# il colpo in poche parole, per l'indice
COLPO = {'L1': 'Trenta pagine di calendario strappate in un colpo', 'L2': 'Il portellone del furgone che si spalanca', 'L3': "Il lampo sull'obiettivo della telecamera", 'F1': 'Il palmo sul tavolo: «Non comprare» diventa «Noleggiala»', 'F2': 'Quattro manipoli, quattro colpi a ritmo', 'F3': 'Il fascicolo del protocollo che cade sul tavolo', 'P1': 'Il palmo sul tavolo: «Fermo!»', 'P2': 'Il telo che vola via', 'P3': 'Il timbro sul foglio bianco', 'P4': 'Il coperchio della scatola che scatta', 'P5': 'Due timbri: FALSO', 'P6': 'La sveglia battuta: «Ti ho fermato»'}
