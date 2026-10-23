#!/usr/bin/env python3
"""I nove reel, stacco per stacco. E' la fonte unica: da qui nascono i copioni (copioni/*.md)
e le tabelle del documento stampato (nove-reel.html).

LA REGOLA DEI 5 SECONDI ha due meta':
  1. i primi 5 secondi contengono il vantaggio intero;
  2. nessuno stacco dura piu' di 5 secondi: dopo, si cambia stacco E inquadratura.
Cosi' il reel e' dinamico alla vista e ogni pezzo e' semplice da girare: un gesto, una frase breve.

Ogni stacco: (inquadratura, cosa si vede, cosa si dice, scritte a schermo, durata fissata a mano o None).
Se la durata e' None si calcola dalle parole (2,8 parole al secondo, arrotondata ai 0,5 s, minimo 2 s).
Le parole dette sono quelle approvate: qui si dividono, non si cambiano.

Controlli (python3 reel-dati.py): nessuno stacco oltre 5 s, due stacchi di fila con inquadrature diverse,
gancio dentro i 5 secondi, ritmo del parlato non oltre 3,7 parole al secondo.
"""
import math, re

PP, MB, DET, CL = 'Primo piano', 'Mezzo busto', 'Dettaglio', 'Campo largo'
QUADRO = {PP: 'il viso, riempie lo schermo', MB: 'dalla vita in su', DET: 'mani o oggetto, da vicino', CL: 'la persona e la macchina nell\'ambiente'}

TITOLO = {
    1: 'Se si ferma, non lavori', 2: 'Una macchina che non sai usare è un mobile', 3: 'Arriva il 1. La paghi il 30',
    4: 'Arriva il 1. La paghi il 30', 5: "Se si ferma, in 48 ore ne hai un'altra",
    6: 'Un laser di quattro anni fa non è lo stesso laser', 7: 'Dopo tre mesi finisce in un angolo',
    8: 'Quattro tecnologie, una macchina sola', 9: 'Chiedi in giro se qualcuno te la dà così',
}
META = {  # paese, campagna, chi parla, lingua parlata, parola chiave, scheda finale, stacchi del gancio
    1: ('Italia', 'Laser', 'Giorgio', 'italiano', 'LASER', 'scheda-finale-LASER-italia.png', 2),
    2: ('Italia', 'Laser', 'Giorgio', 'italiano', 'LASER', 'scheda-finale-LASER-italia.png', 2),
    3: ('Italia', 'Laser', 'Giorgio', 'italiano', 'LASER', 'scheda-finale-LASER-italia.png', 2),
    4: ('Albania', 'Laser', 'Uarda', 'albanese', 'LASER', 'scheda-finale-LASER-albania.png', 2),
    5: ('Albania', 'Laser', 'Uarda', 'albanese', 'LASER', 'scheda-finale-LASER-albania.png', 2),
    6: ('Albania', 'Laser', 'Uarda', 'albanese', 'LASER', 'scheda-finale-LASER-albania.png', 2),
    7: ('Albania', 'Afrodite', 'Uarda', 'albanese', 'AFRODITE', 'scheda-finale-AFRODITE-albania.png', 2),
    8: ('Albania', 'Afrodite', 'Uarda', 'albanese', 'AFRODITE', 'scheda-finale-AFRODITE-albania.png', 2),
    9: ('Albania', 'Afrodite', 'Uarda', 'albanese', 'AFRODITE', 'scheda-finale-AFRODITE-albania.png', 2),
}
SERVE = {
    1: "Due macchine nella stessa inquadratura, o una macchina e un furgone aperto",
    2: "Il protocollo laser stampato (ce l'abbiamo già: 6 pagine, IT) e un telo per coprire una macchina",
    3: "Un calendario da muro grande, senza mese e senza anno stampati: il reel regge tutti i mesi. Niente macchina: qui conta la faccia",
    4: "Un centro vero, non il magazzino. Meglio se con una cliente sul lettino, vestita",
    5: "Il furgone. È l'immagine che vale più di mille parole",
    6: "Una macchina nuova, ancora imballata. La pellicola che si stacca è il piano più forte del reel",
    7: "Il protocollo Afrodite e la scheda di cabina stampati (ce li abbiamo) e un telo per coprire la macchina",
    8: "I manipoli, luce radente. Niente pelle: solo i manipoli",
    9: "Un foglio bianco. Non un contratto vero: l'immagine è «non firmi niente»",
}
NOTE = {
    2: ["Con le parole come sono dura 25,5 secondi. Togliere «Non è che la macchina non funziona.» (lo dice già la scritta dello stacco 2) lo porta a 23."],
    7: ["Con le parole come sono dura 24 secondi. Togliere «cosa si fa, con quali parametri, in che ordine, e quante sedute.» lo porta a 20: il metodo DEMETRA lo ripete subito dopo."],
    4: ["La scritta dello stacco 1 e 2 è ancora in italiano nel copione approvato: per il pubblico albanese va tradotta."],
    8: ["Parole decise da Giorgio: «ultrasuono focalizzato direzionale» al posto di «cavitazione», «low laser» al posto di «LED» (confermato il 23 ottobre).",
        "In albanese la scritta è «ULTRATINGULL I FOKUSUAR», senza «direzionale»: da far controllare a Uarda.",
        "Il sito conta anche il Micropulse; qui sono quattro tecnologie perché il Micropulse è una vibrazione che rende il massaggio confortevole, non una tecnologia a sé. Da allineare."],
    5: ["Il gancio ha 18 parole in 5 secondi: va detto svelto. Se non regge, si toglie «una domanda a» e resta «Chiedi a chiunque ti noleggi una macchina»."],
}

# (inquadratura, si vede, si dice, scritte, durata)
S = {
 1: [
  (MB,  "In magazzino, la macchina alle spalle.", "Se la tua macchina si ferma domani mattina,", [], None),
  (PP,  "Stessa ripresa, ingrandita sul viso.", "quante clienti disdici?", ["QUANTE CLIENTI DISDICI?"], None),
  (CL,  "Cammina verso un'altra macchina.", "Da noi, in 48 ore ne hai un'altra in cabina.", ["MULETTO IN 48 ORE"], None),
  (DET, "La mano si appoggia sull'altra macchina.", "Non chiudi un'ora, non disdici nessuno.", [], None),
  (PP,  "Giorgio, in camera.", "Un laser fermo una settimana sono dodici clienti che saltano il turno.", [], None),
  (MB,  "Fermo, in camera.", "E la maggior parte non rientra più.", [], None),
  (PP,  "Fermo, guarda in camera.", "500 al mese, senza firmare niente. Scrivimi LASER.", ["SCRIVI «LASER»"], None),
 ],
 2: [
  (DET, "Una mano sfila un telo da una macchina ferma in un angolo.", "Quante macchine hai visto", [], None),
  (PP,  "Giorgio, in camera.", "prendere polvere in un angolo?", ["NON È LA MACCHINA.", "È CHE NESSUNO TI HA DETTO COME SI USA"], 3.0),
  (MB,  "Al tavolo, il protocollo laser davanti.", "Non è che la macchina non funziona.", [], None),
  (DET, "La mano sfoglia il protocollo, pagina per pagina.", "È che nessuno ti ha dato il protocollo:", [], None),
  (PP,  "Giorgio, in camera.", "cosa fai da quando la cliente entra a quando esce,", [], None),
  (DET, "Le pagine del protocollo scorrono.", "con quali parametri, e ogni quanto la richiami.", [], None),
  (MB,  "Giorgio con il protocollo in mano.", "Con la nostra arriva scritto. E la formazione è compresa.", ["PROTOCOLLO SCRITTO", "FORMAZIONE COMPRESA"], None),
  (PP,  "Chiude il fascicolo, lo appoggia, guarda in camera.", "Scrivimi LASER e te lo faccio vedere prima di decidere.", ["SCRIVI «LASER»"], None),
 ],
 3: [
  (PP,  "Giorgio con il calendario accanto al viso, segna il 1.", "Te la porto il primo del mese.", ["ARRIVA IL 1"], None),
  (DET, "Il dito va dal 1 al 30 sul calendario.", "Me la paghi il trenta.", ["LA PAGHI IL 30"], None),
  (MB,  "Abbassa il calendario, guarda in camera.", "Trenta giorni di lavoro prima di tirare fuori il primo euro.", [], None),
  (DET, "Il dito scorre sul calendario, dal 1 al 30.", "Zero anticipo, zero cauzione, nessun vincolo.", ["ZERO ANTICIPO · ZERO CAUZIONE", "NESSUN VINCOLO"], None),
  (PP,  "Giorgio, in camera.", "E se ad agosto chiudi, me la ridai: quel mese non paghi.", [], None),
  (MB,  "Posa il calendario, guarda in camera.", "500 al mese. Chiedi in giro se qualcuno te la dà così. Scrivimi LASER.", ["SCRIVI «LASER»"], None),
 ],
 4: [
  (PP,  "Uarda, in un centro vero.", "Te la porto il primo del mese.", ["ARRIVA IL 1"], None),
  (DET, "Il display acceso della macchina, in cabina.", "Me la paghi il trenta.", ["LA PAGHI IL 30"], None),
  (MB,  "Uarda, la macchina dietro di lei.", "Trenta giorni di lavoro prima di tirare fuori il primo lek.", [], None),
  (PP,  "Uarda, in camera.", "Senza anticipo, senza cauzione, senza firmare nessun vincolo.", ["PA PARADHËNIE · PA GARANCI", "PA KONTRATË"], None),
  (CL,  "Uarda e la macchina accesa, in cabina.", "E quando chiudi per le ferie me la ridai: quel mese non paghi.", [], None),
  (PP,  "Uarda, in camera.", "50.000 lekë al mese. Scrivimi LASER.", ["50.000 LEKË / MUAJ", "SHKRUAJ «LASER»"], None),
 ],
 5: [
  (DET, "Uarda spegne una macchina: lo schermo del display diventa nero.", "Fai una domanda a chiunque ti noleggi una macchina:", ["FAI QUESTA DOMANDA", "A CHIUNQUE"], 2.5),
  (PP,  "Uarda, in camera.", "se si ferma, in quanto tempo ne ho un'altra?", [], 2.5),
  (CL,  "Stacco: il furgone si apre, la macchina scende.", "Da noi: 48 ore.", ["48 ORË"], None),
  (PP,  "Uarda, in camera.", "Non chiudi un'ora, non disdici una cliente.", [], None),
  (MB,  "Uarda, la macchina nuova dietro di lei.", "Perché un laser fermo una settimana sono dodici clienti che saltano il turno", [], None),
  (DET, "Il display della macchina sostitutiva, acceso.", "e la maggior parte non rientra più.", [], None),
  (PP,  "Uarda, in camera.", "Il rischio non è tuo. È nostro. Scrivimi LASER.", ["RREZIKU NUK ËSHTË YTI", "SHKRUAJ «LASER»"], None),
 ],
 6: [
  (DET, "Una mano toglie la pellicola protettiva da un display nuovo.", "Un laser di quattro anni fa non è lo stesso laser.", [], 3.5),
  (PP,  "Uarda, in camera. Resta in silenzio un attimo.", "", ["E LA TUA, DI CHE ANNO È?"], 1.5),
  (DET, "Il display touch si accende.", "La nostra è di ultima generazione:", [], None),
  (MB,  "Uarda, la macchina in cabina.", "la telecamera guarda la pelle e l'intelligenza artificiale ti propone i parametri.", ["KAMERË + IA"], None),
  (DET, "La telecamera e il manipolo in titanio.", "Decidi sempre tu.", [], None),
  (PP,  "Uarda, in camera.", "Certificata in Italia, con MDR attivo.", ["CE ITALIANE · MDR AKTIV"], None),
  (MB,  "Uarda, in camera.", "50.000 lekë al mese, senza vincoli. Scrivimi LASER.", ["SHKRUAJ «LASER»"], None),
 ],
 7: [
  (CL,  "Una macchina coperta da un telo, in un angolo, luce bassa.", "Quante macchine hai visto finire così, dopo tre mesi?", [], None),
  (PP,  "Uarda, in camera. Resta in silenzio un attimo.", "", ["NON È CHE NON FUNZIONA"], 1.5),
  (DET, "Si scopre la macchina e si accende.", "È che nessuno ha dato alla titolare il protocollo:", [], None),
  (MB,  "Uarda al tavolo, con il protocollo e la scheda di cabina.", "cosa si fa, con quali parametri, in che ordine, e quante sedute.", [], None),
  (DET, "Il protocollo e la scheda di cabina stampati, sul tavolo.", "Con la nostra arriva il metodo DEMETRA:", [], None),
  (PP,  "Uarda, in camera.", "ciclo di 10-12 sedute, scheda di valutazione, protocollo pagina per pagina.", ["PROTOKOLLI · SKEDA · TRAJNIMI"], None),
  (MB,  "Uarda, in camera.", "E l'assistenza sempre. 50.000 lekë al mese, senza vincoli. Scrivimi AFRODITE.", ["SHKRUAJ «AFRODITE»"], None),
 ],
 8: [
  (DET, "I manipoli allineati sul lettino. Una mano li tocca uno a uno.", "Quattro tecnologie.", [], None),
  (PP,  "Uarda, in camera.", "Una macchina sola. Una rata sola.", ["4 TEKNOLOGJI", "1 MAKINË"], None),
  (DET, "Il primo manipolo, da vicino. Il nome a schermo.", "Ultrasuono focalizzato direzionale.", ["ULTRATINGULL I FOKUSUAR"], None),
  (MB,  "Uarda tiene in mano il secondo manipolo. Il nome a schermo.", "Radiofrequenza.", ["RADIOFREKUENCË"], 1.5),
  (DET, "Il terzo manipolo, da vicino. Il nome a schermo.", "Vacuum.", ["VAKUM"], 1.5),
  (MB,  "Uarda tiene in mano il quarto manipolo. Il nome a schermo.", "Low laser.", ["LOW LASER"], 1.5),
  (PP,  "Uarda, in camera.", "Rimodellamento, cellulite, ritenzione, tono —", [], None),
  (MB,  "Uarda, in camera.", "con una macchina che ti arriva il primo del mese", [], None),
  (CL,  "Uarda e la macchina, in cabina.", "e la paghi il trenta.", [], None),
  (PP,  "Uarda, in camera.", "50.000 lekë al mese, senza vincoli. Scrivimi AFRODITE.", ["SHKRUAJ «AFRODITE»"], None),
 ],
 9: [
  (DET, "Uarda tiene un foglio di contratto. Lo gira: è bianco.", "Senza firmare nessun vincolo.", ["PA KONTRATË"], None),
  (PP,  "Uarda, in camera.", "Chiedi in giro se qualcuno te la dà così.", [], 3.0),
  (MB,  "Uarda, in camera.", "Nessun anticipo. Nessuna cauzione. Nessun vincolo.", ["0 PARADHËNIE · 0 GARANCI", "0 KONTRATË"], None),
  (DET, "Il foglio bianco, posato sul tavolo.", "La paghi dopo trenta giorni di lavoro.", [], None),
  (PP,  "Uarda, in camera.", "Se si ferma, in 48 ore ne hai un'altra. Formazione compresa.", ["48 ORË"], None),
  (MB,  "Uarda, in camera.", "E quando chiudi per le ferie, me la ridai e quel mese non paghi.", [], None),
  (PP,  "Uarda, in camera.", "50.000 lekë al mese. Scrivimi AFRODITE.", ["SHKRUAJ «AFRODITE»"], None),
 ],
}

# ---- le inserzioni: il testo che accompagna il reel quando diventa pubblicita'
NUM = {'Italia': '+39 351 846 6025 (Giorgio)', 'Albania': '+355 69 212 9786 (Uarda)'}
AD = {
    1: ('B · Il rischio ribaltato',
        "Se la tua macchina si ferma domani mattina, quante clienti disdici?\nDa noi, in 48 ore ne hai un'altra in cabina.\n500 € al mese, nessun vincolo. Scrivimi «LASER».",
        'Muletto in 48 ore, sempre'),
    2: ('C · Il metodo compreso',
        "Quante macchine hai visto prendere polvere in un angolo?\nNon è la macchina: è che nessuno ti ha dato il protocollo.\nCon la nostra arriva scritto, con la formazione. 500 € al mese, nessun vincolo. Scrivimi «LASER» e te lo faccio vedere.",
        'La macchina, e il protocollo per usarla'),
    3: ('A · Trenta giorni prima',
        "Il laser arriva il 1. Lo paghi il 30.\nUn mese intero di lavoro prima di tirare fuori il primo euro. Zero anticipo, zero cauzione, nessun vincolo.\n500 € al mese. Scrivimi «LASER».",
        '500 € al mese. Paghi dopo 30 giorni'),
    4: ('A · Trenta giorni prima',
        "La macchina ti arriva il 1 del mese. Paghi il 30.\nTrenta giorni di lavoro prima di tirare fuori il primo lek. Nessun vincolo, nessun anticipo, nessuna cauzione.\n50.000 lekë al mese. Scrivi «LASER».",
        '50.000 Lekë/mese · nessun vincolo'),
    5: ('B · Il rischio non è tuo',
        "La domanda da fare a qualunque fornitore: «Se la macchina si ferma, in quanto tempo ne ho un'altra in cabina?»\nDa noi: 48 ore. Il rischio non è tuo, è nostro.\n50.000 lekë al mese, nessun vincolo. Scrivi «LASER».",
        'Macchina sostitutiva entro 48 ore'),
    6: ('Nuovo · Ultima generazione (non è uno dei quattro angoli della Campagna 500)',
        "Un laser di quattro anni fa non è lo stesso laser.\nLa telecamera guarda la pelle e l'intelligenza artificiale ti propone i parametri: decidi sempre tu. Certificata in Italia, MDR attivo.\n50.000 lekë al mese, nessun vincolo. Scrivi «LASER».",
        'Laser di ultima generazione, con IA'),
    7: ('C · Il metodo compreso (Afrodite)',
        "Tanti centri comprano la macchina e dopo tre mesi la lasciano in un angolo. Non perché non funzioni: perché nessuno ha dato loro il protocollo.\nCon noi arriva il metodo DEMETRA: ciclo di 10-12 sedute, scheda di valutazione, protocollo pagina per pagina.\n50.000 lekë al mese, nessun vincolo. Scrivi «AFRODITE».",
        'La macchina e il metodo per usarla'),
    8: ('Nuovo · Quattro tecnologie in una macchina (Afrodite)',
        "Ultrasuono focalizzato direzionale, radiofrequenza, vacuum e low laser. Una macchina sola, una rata sola.\nTi arriva il 1, la paghi il 30. Nessun vincolo, nessun anticipo.\n50.000 lekë al mese. Scrivi «AFRODITE».",
        'Rimodellamento corpo — 50.000 Lekë/mese'),
    9: ('A · Trenta giorni prima (Afrodite)',
        "Nessun anticipo. Nessuna cauzione. Nessun vincolo.\nLa paghi dopo trenta giorni di lavoro. Se si ferma, in 48 ore ne hai un'altra.\n50.000 lekë al mese. Scrivi «AFRODITE».",
        'Arriva il 1, la paghi il 30'),
}

def parole(t):
    t = re.sub(r'(?<=\d)\.(?=\d)', '', t)
    return len(re.findall(r"[\w'’]+", t))

def stacchi(n):
    """Lista di dict con tempi calcolati."""
    t, out = 0.0, []
    for k, (inq, vede, parla, schermo, fisso) in enumerate(S[n], 1):
        w = parole(parla)
        d = fisso if fisso else max(2.0, math.ceil(w / 2.8 * 2) / 2)
        out.append(dict(n=k, t0=t, t1=t + d, dur=d, inq=inq, vede=vede, parla=parla, schermo=schermo, parole=w))
        t += d
    return out

def fine(n):
    return stacchi(n)[-1]['t1']

def fmt(x):
    return ('%g' % x).replace('.', ',')

def controlla():
    ok = True
    for n in S:
        st = stacchi(n); g = META[n][6]
        for a, b in zip(st, st[1:]):
            if a['inq'] == b['inq']:
                print(f'reel {n}: stacchi {a["n"]} e {b["n"]} hanno la stessa inquadratura ({a["inq"]})'); ok = False
        for s_ in st:
            if s_['dur'] > 5.0:
                print(f'reel {n}: stacco {s_["n"]} dura {s_["dur"]} s'); ok = False
            if s_['parole'] and s_['parole'] / s_['dur'] > 3.7:
                print(f'reel {n}: stacco {s_["n"]} troppo veloce ({s_["parole"]} parole in {s_["dur"]} s)'); ok = False
        gancio = st[g - 1]['t1']
        if gancio > 5.0:
            print(f'reel {n}: il gancio finisce a {gancio} s'); ok = False
    return ok

if __name__ == '__main__':
    if controlla():
        for n in S:
            st = stacchi(n)
            print(f'reel {n}: {len(st)} stacchi, il più lungo {max(s["dur"] for s in st)} s, il gancio finisce a {st[META[n][6]-1]["t1"]} s, il copione finisce a {fine(n)} s')
