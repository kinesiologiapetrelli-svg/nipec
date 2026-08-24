# Memoria cognitiva NIPEC — indice

Mappa di cosa c'è e di quale copia vale. Regola unica: **dove esistono più
versioni dello stesso documento, quella valida è indicata qui.** Le altre
restano come archivio e portano `superato` nel nome.

## Il principio e la sua memoria

| Cosa | File | Stato |
|---|---|---|
| I dodici precetti | `../CLAUDE.md` | **Fonte.** Si aggiorna qui e solo qui |
| Principio, stampabile | `PrincipioAnalisiPetrus-v1.pdf` | Generato dalla fonte |
| Principio, PDF di agosto | `PrincipioAnalisiPetrus.pdf` | Originale di Giorgio, concorde |
| Principio, versione anteriore | `PrincipioAnalisiPetrus-v0-superato.pdf` / `.html` | **Superata** — manca la lettura evolutiva del 05, i trade-off del 10, la biologia evolutiva del 03 |
| File di direttive | `DirettivaPetrus-originale.md` | Originale di Giorgio, concorde |
| La biblioteca | `BibliotecaCognitiva.md` · `.pdf` | Parte canonica (le 13 corde), parte ricostruita da correggere |
| Il profilo cognitivo | `ProfiloCognitivo-MenteAPiuCanali.pdf` | Originale. Spiega da dove nasce il principio |

I dodici precetti sono verificati su **due originali indipendenti** di Giorgio
— il PDF di agosto e il file di direttive — che concordano nella sostanza.

## Materiale operativo — `nipec/`

| Cosa | File | Stato |
|---|---|---|
| Script di approccio, 12 obiezioni | `nipec/ProtocolloPonte.html` | **Fonte.** Contiene tutti e 12 gli script |
| Protocollo Ponte, stampabile | `nipec/ProtocolloPonte-v1.3-COMPLETO.pdf` | **Da usare.** 10 pagine, 12 script su 12 |
| Protocollo Ponte, export originale | `nipec/ProtocolloPonte-v1.3-ORIGINALE.pdf` | **Difettoso:** le fisarmoniche sono stampate chiuse, contiene 1 script su 12 |
| Protocollo Ponte, versione anteriore | `nipec/ProtocolloPonte-v1.0-superato.pdf` | **Superata** — senza il catalogo delle corde |
| Munger applicato, inversione | `nipec/NIPEC-Munger-RibaltareAnalisi.pdf` | Corrente |
| Storico e crescita, previsione | `nipec/StoricoCrescita-previsione.pdf` | **Corrente** — reali gen-ago, da settembre Italia €14k/mese e Albania €7k/mese, nuove macchine incluse |
| Storico e crescita, run-rate | `nipec/StoricoCrescita-runrate-superato.pdf` | **Superata** — annualizzava gen-giu |
| Standard NIPEC, dossier | `nipec/Dossier_Progetto_NIPEC_IT.md` · `_AL.md` | Corrente, italiano e albanese |
| DEMETRA Tirana, dieci reel | `nipec/DEMETRA_Tirana_10_Reel.md` | Corrente |
| DEMETRA Tirana, piano di Egla | `nipec/DEMETRA_Tirana_Piano_Egla.md` | Corrente |
| DEMETRA Tirana, controllo interno | `nipec/DEMETRA_Tirana_Piano_Uarda_INTERNO.md` | Corrente · non si mostra a Egla |

## Punti aperti

1. **Bibliografia** — i titoli reali dei libri non sono ancora arrivati. La
   sezione in `BibliotecaCognitiva.md` contiene ipotesi, non dichiarazioni di
   Giorgio.
2. **Provenienza** — il PDF cita tre lenti più Darwin, Giorgio ne indica
   quattro con Buffett. Da decidere.
3. **Date DEMETRA** — risolto il 24 agosto. Due verifiche distinte: il
   **10 settembre** le azioni (se la partenza non è fatta, la macchina
   rientra), il **30 settembre** il fatturato (500 €/mese). Entrambe le date
   sono ora scritte anche nel piano di Egla. Resta da inserire, nel suo piano,
   il numero di clienti attive che coprono i 500 €: serve il valore mensile di
   un percorso DEMETRA.

## Come si rigenera

```
bash tools/build-pdf.sh
```

I PDF marcati «generato» sono prodotti: non si modificano a mano.
