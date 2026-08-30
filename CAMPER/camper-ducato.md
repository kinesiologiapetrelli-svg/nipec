---
name: camper-ducato
description: Progetto camper di Giorgio sul Fiat Ducato (ex Indie Campers); lavoro attivo = impianto elettrico/solare. Contiene la scheda tecnica dettagliata del mezzo.
metadata: 
  node_type: memory
  type: project
  originSessionId: 9fda513e-b7a8-45b8-8217-66e6c99cb824
  modified: 2026-08-07T10:42:33.541Z
---

Giorgio possiede un **furgonato Weinsberg su base Fiat Ducato** (ex **Indie Campers**), targa **albanese AB 589 ZL**, ritirato ~**giugno 2026**, ~200 km alle prime prove (Venezia/Brescia). NON è un autocostruito: è un camper di fabbrica (Weinsberg CaraBus, ~6m, furgonato con porta scorrevole + 2 finestre lato vivibile) → ha già impianto elettrico di serie (caricabatterie/centralina tipo Schaudt/similare + predisposizione solare). **CONFERMATO (foto+utente):** tetto LIBERO (oggetti metallici sul retro = barre/portapacchi, NON pannelli solari; nessun solare di fabbrica). **Frigo a COMPRESSORE (elettrico)** = vampiro principale. Ancoraggio empirico consumo: AGM 120Ah dura ~1 giorno → ~60Ah usabili/giorno ≈ **~720 Wh/giorno** di consumo casa.

**Scheda tecnica memorizzata (dati dichiarati dall'utente):**
- Gas: bombola tradizionale. Riscaldamento/boiler **Truma Combi**, comando **Touch**, acqua a 60°C. Errore discusso: **W412H**. Fornelli ok.
- **Pannello/centralina = sistema CBE** (rimarchiato Weinsberg; barra 0-100% + tasti pompa/luci). → caricabatterie CBE tarato piombo/AGM, NON litio: con LiFePO₄ carica a metà e la barra % legge falsato. Serve soluzione litio (swap caricatore CBE lithium-ready o aggiunta Victron) + SmartShunt per SoC reale.
- 230V: presente (prova in colonnina ok).
- Batteria servizi: originaria AGM ~100-110Ah → sostituita con **AGM 120Ah**. Problema: autonomia ~1 giorno, insufficiente.
- **Storage portatile già posseduto:** power station **SOUOP 2400W / 2232Wh** + **EcoFlow DELTA 3 Classic 1024Wh**. Climatizzatore **EcoFlow WAVE 3**.
- Pannelli sul tetto: forse presenti ma potenza/modello NON noti.

**Progetto discusso (NON ancora installato):** Alternatore → **DC-DC 60A** → **LiFePO₄ 280Ah** (~3,58 kWh) → **inverter 3000W** → 230V; in parallelo **pannelli 500-600W → MPPT → LiFePO₄**. Valutato anche EcoFlow Alternator Charger ~800/1000W.

**Assistenza:** **Sami Camper, Tirana** (impianto/pannelli/modifiche — coerente con residenza AL, vedi [[eros-fiscalita-albania]]); officina zona Altavilla Vicentina/Vicenza.

**Dati mancanti per dimensionare il FV:** modello/anno Ducato, lunghezza camper, spazio libero tetto, eventuali pannelli esistenti + wattaggio, modello caricabatterie 230V, centralina camper, marca AGM 120Ah. Servono foto di batteria servizi + centralina + tetto.

**Target autonomia scelto da Giorgio: 5+ notti** senza sole/colonnina/guida → serve batteria grande (300-400Ah) + solare generoso (400W). Requisito che rimette in gioco il "numero grosso" del piano originale.

**Nodo strategico aperto:** decidere l'ARCHITETTURA prima dei componenti — sistema fisso integrato (LiFePO₄ 280Ah + inverter 3000W) VS ecosistema portatile (SOUOP + EcoFlow) VS ibrido. Rischio: costruire due impianti energetici paralleli ridondanti che non dialogano. Missione camper ancora da definire; collega al motore-movimento di [[barbara-percorso]].
