# NIPEC · Cruscotto Clienti

Da «ho deciso di dare la macchina a questo centro» a «il centro è vivo nel master».
Quattro pezzi che si tengono: la procedura di consegna, il motore degli avvisi,
il foglio già fatto e l'app che la titolare si mette sul telefono.

| | Cos'è | Come si usa |
|---|---|---|
| **`PERSELOPE.html`** | La sequenza di consegna, quattro fasi. Le prime tre si fanno entro 24 ore. | Pagina singola: si trascina su Netlify, oppure si stampa. |
| **`ALERT-LASER.html`** | Il motore degli avvisi del cruscotto laser: le formule esatte, riga per riga, con il pulsante «copia». | Pagina singola. |
| **`2-FOGLI/`** | Il **Cruscotto Clienti · laser** già fatto: sei fogli, tendine, colori, i sei numeri dentro. | Carichi su Drive → Apri con Fogli Google → File → Salva come Foglio Google. |
| **`APP-ALERT-LASER/`** | **L'app dei centri.** Ogni mattina dice chi richiamare e in che ordine. Si installa sulla schermata Home e funziona offline. Parte vuota. | Si trascina su Netlify **la cartella intera**: senza `manifest`, `sw.js` e le icone non si installa. |
| **`APP-ALERT-LASER-DEMO/`** | **La copia dimostrativa.** Stessa app, già piena di quattordici clienti finte che accendono tutti e otto gli avvisi. Serve a far vedere il sistema in trenta secondi. | Generata da `APP-ALERT-LASER/_genera-demo.py`: non si modifica a mano. |
| **`MARCHIO/`** | Il marchio NIPEC 5.0: orizzontale, verticale, compatto ed emblema, in positivo e negativo. | `LEGGIMI.txt` dice quale file va dove. |

## Online

Le pagine e le due app si pubblicano da sole a ogni modifica del ramo principale
(`.github/workflows/pubblica.yml` → GitHub Pages).

- **App dei centri** — https://kinesiologiapetrelli-svg.github.io/nipec/APP-ALERT-LASER/
- **Demo** — https://kinesiologiapetrelli-svg.github.io/nipec/APP-ALERT-LASER-DEMO/

Sono due indirizzi diversi, quindi **due archivi separati**: l'app tiene la rubrica
nel browser, legata all'indirizzo da cui è stata aperta. La demo non può sporcare
una rubrica vera, e cambiare indirizzo a lavoro iniziato significa perdere i dati —
si sposta solo passando da NIPEC → Copia di sicurezza.

## L'orologio del laser

Ciclo di **12 sedute** · rientro tra il **21°** e il **28°** giorno · conferma a **−7** e il
giorno prima · mantenimento ogni **90 giorni** · dormiente dopo **6 mesi**.
I sei numeri stanno in un posto solo — il foglio `IMPOSTAZIONI`, e le Impostazioni
dell'app — e comandano tutti gli avvisi.

## Gli otto avvisi, in ordine di lavoro

1. CONFERMA DOMANI · 2. CHIAMA PER CONFERMA · 3. APPUNTAMENTO SALTATO ·
4. PRENDI APPUNTAMENTO · 5. FUORI FINESTRA · 6. ULTIMA SEDUTA ·
7. RICHIAMO MANTENIMENTO · 8. RECUPERA CON INCENTIVO

Prima quello che oggi si spegne da solo, poi quello che resta acceso finché non lo chiudi.

## La regola d'oro

**Nessuna esce senza il prossimo appuntamento.** Sotto il 90% di copertura il centro
sta perdendo clienti senza accorgersene.

## Le clienti dei centri non stanno qui

In questo repository non entrano nomi, telefoni o link a fogli di centri: solo
strumenti vuoti. La rubrica dell'app resta sul dispositivo della titolare; verso
NIPEC viaggia il **battito**, sei numeri e una data, senza nessun nome.

---
NIPEC · Tecnologie Estetiche — Assistenza 351 846 6025
