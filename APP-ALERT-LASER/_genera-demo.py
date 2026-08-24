# -*- coding: utf-8 -*-
"""Genera la copia DEMO dall'app vera. Una sorgente sola: se cambia l'app,
si rilancia questo e la demo si riallinea. Non si modifica mai la demo a mano."""
import os, re, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
FUORI = os.path.join(os.path.dirname(BASE), "APP-ALERT-LASER-DEMO")

# ------------------------------------------------ le clienti finte
# Costruite per mostrare tutti e otto gli avvisi in una schermata sola,
# e una copertura appuntamento al 50%: e' il buco che vende il sistema.
DEMO_JS = r'''
<script>
"use strict";
/* ================= la rubrica finta della DEMO =================
   Nessuna di queste persone esiste. Le date sono relative a oggi,
   cosi' la demo e' sempre "viva" qualunque giorno la apri. */
function caricaDemo() {
  var o = oggiISO(), g = function (n) { return piuGiorni(o, -n); }, f = function (n) { return piuGiorni(o, n); };
  S.centro = "Centro Dimostrativo";
  S.prefisso = "39";
  S.offerte = [
    { nome: "Offerta Laser 1", testo: "seduta di rientro a metà prezzo", scade: f(20) },
    { nome: "Offerta Laser 2", testo: "richiamo di mantenimento a 39 € invece di 60", scade: f(30) },
    { nome: "Offerta Laser 3", testo: "tre sedute al prezzo di due, per ripartire", scade: f(15) }
  ];
  S.imp.sedute = 8;              /* il ciclo vero, non quello vecchio da 12 */
  var righe = [
    ["Anna Ferri",       "3391112201", "ascelle", "In ciclo",       7, 45, g(23), f(1)],
    ["Bea Conti",        "3391112202", "inguine", "In ciclo",       3, 70, g(21), f(7)],
    ["Chiara Neri",      "3391112203", "gambe",   "In ciclo",       4, 90, g(30), g(2)],
    ["Daniela Russo",    "3391112204", "ascelle", "In ciclo",       2, 45, g(2),  ""],
    ["Elena Vitale",     "3391112205", "inguine", "In ciclo",       5, 70, g(34), ""],
    ["Federica Sala",    "3391112206", "gambe",   "In ciclo",       8, 90, g(12), ""],
    ["Giulia Marino",    "3391112207", "ascelle", "Mantenimento",   8, 45, g(95), ""],
    ["Ilaria Costa",     "3391112208", "gambe",   "Persa",          3, 90, g(150), ""],
    ["Laura Greco",      "3391112209", "inguine", "In ciclo",       3, 70, g(210), ""],
    ["Martina Bruno",    "3391112210", "gambe",   "Sospesa",        4, 90, g(60), ""],
    ["Nadia Fontana",    "3391112211", "ascelle", "In ciclo",       6, 45, g(20), f(12)],
    ["Paola Ricci",      "3391112212", "inguine", "In ciclo",       1, 70, g(24), o],
    ["Sara De Luca",     "3391112213", "gambe",   "In ciclo",       7, 90, g(22), f(3)],
    ["Valentina Longo",  "3391112214", "ascelle", "Mantenimento",   8, 45, g(40), ""]
  ];
  S.clienti = righe.map(function (r, i) {
    return { id: "demo" + i, nome: r[0], tel: r[1], zona: r[2], stato: r[3],
             sedute: r[4], prezzo: r[5], ultima: r[6], prossimo: r[7],
             inserita: piuGiorni(o, -(200 - i * 9)), note: "", rinviato: "" };
  });
  S.battito = ""; S.allineato = "";
  salva();
  disegna();
}
</script>
'''

def genera():
    if os.path.isdir(FUORI):
        shutil.rmtree(FUORI)
    shutil.copytree(BASE, FUORI)
    for spazzatura in ("_genera-demo.py", "LEGGIMI-GIORGIO.txt"):
        p = os.path.join(FUORI, spazzatura)
        if os.path.exists(p):
            os.remove(p)

    p = os.path.join(FUORI, "index.html")
    s = open(p, encoding="utf-8").read()

    def cambia(vecchio, nuovo, quante=1):
        nonlocal s
        assert s.count(vecchio) == quante, "non trovato: " + vecchio[:60]
        s = s.replace(vecchio, nuovo)

    cambia("<title>ALERT LASER</title>", "<title>ALERT LASER · DEMO</title>")
    cambia('<meta name="apple-mobile-web-app-title" content="Alert Laser">',
           '<meta name="apple-mobile-web-app-title" content="Laser DEMO">')
    cambia('var CHIAVE = "alertlaser.v1";', 'var CHIAVE = "alertlaser.demo.v1";')

    # il nastro DEMO in testata: deve essere impossibile confonderla
    cambia('<div class="firma">Persefone <b>By NIPEC</b></div>',
           '<div class="firma"><span class="nastro">DEMO</span> Persefone <b>By NIPEC</b></div>')
    cambia(".capo .firma b{font-weight:700;opacity:.95}",
           ".capo .firma b{font-weight:700;opacity:.95}\n"
           ".nastro{background:#e0917a;color:#2a1b17;font-weight:700;letter-spacing:.1em;"
           "border-radius:.25rem;padding:.05rem .3rem;margin-right:.3rem}")

    # niente benvenuto: la demo si carica da sola, gia' piena
    cambia('if (!S.centro && !S.clienti.length) setTimeout(benvenuto, 400);',
           'if (!S.clienti.length) caricaDemo();')

    # il bottone dei dati di prova diventa "ricarica la demo"
    cambia('<button class="btn" type="button" data-az="prova">Carica tre clienti di prova</button>',
           '<button class="btn" type="button" data-az="prova">Ricarica la demo da capo</button>')
    cambia("'<button class=\"btn\" type=\"button\" data-vai=\"prova\">Carica tre clienti di prova</button>' +",
           "'<button class=\"btn\" type=\"button\" data-vai=\"prova\">Ricarica la demo</button>' +")
    cambia("<p style=\"margin-bottom:.7rem\">Stanno solo su questo telefono. Nessuno le vede, nemmeno noi. Ma se perdi il telefono le perdi: <b>salva una copia ogni tanto</b>, e tienila dove vuoi tu.</p>",
           "<p style=\"margin-bottom:.7rem\"><b>Questa è la copia dimostrativa.</b> Le clienti qui dentro sono inventate e servono a far vedere come funziona. Puoi combinarci quello che vuoi: si rimette a posto con un pulsante.</p>")

    # la demo si carica prima che parta l'ultimo blocco di codice
    ultimo = s.rindex('<script>\n"use strict";\n/* ======================= collegamenti')
    s = s[:ultimo] + DEMO_JS.strip() + "\n\n" + s[ultimo:]

    # e "carica dati di prova" diventa "ricarica la demo"
    s = s.replace("if (az === \"prova\") return datiProva();", "if (az === \"prova\") return caricaDemo();")
    s = s.replace('if (t.dataset.vai === "prova") { datiProva(); return; }',
                  'if (t.dataset.vai === "prova") { caricaDemo(); return; }')
    open(p, "w", encoding="utf-8").write(s)

    # manifest e guscio offline, con nomi propri
    m = os.path.join(FUORI, "manifest.webmanifest")
    t = open(m, encoding="utf-8").read()
    t = t.replace('"name": "ALERT LASER"', '"name": "ALERT LASER · DEMO"')
    t = t.replace('"short_name": "Alert Laser"', '"short_name": "Laser DEMO"')
    t = t.replace('"description": "La rubrica del laser che dice chi richiamare oggi."',
                  '"description": "La copia dimostrativa di ALERT LASER, già piena di clienti finte."')
    open(m, "w", encoding="utf-8").write(t)

    w = os.path.join(FUORI, "sw.js")
    t = open(w, encoding="utf-8").read()
    t = t.replace('var VERSIONE = "alert-laser-1";', 'var VERSIONE = "alert-laser-demo-1";')
    open(w, "w", encoding="utf-8").write(t)
    return FUORI

if __name__ == "__main__":
    print("scritta:", genera())
