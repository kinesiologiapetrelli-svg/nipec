#!/usr/bin/env python3
"""Fa il PDF di UN copione, da dare a chi lo deve girare o a chi lo deve montare.

Legge copioni/reel-NN-*.md — cioe' quello che fai-copioni.py ha gia' scritto
dai dati — e ne fa un foglio A4 autosufficiente: il carattere e' dentro il
file, quindi si apre uguale su qualunque computer.

Uso:   python3 fai-copione-pdf.py 1
       python3 fai-copione-pdf.py 1 2 3
       python3 fai-copione-pdf.py tutti
"""
import os, re, sys, glob, base64, subprocess, html as H

QUI = os.path.dirname(os.path.abspath(__file__))
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

NAVY, CHIARO, VERDE, VERDEF = "#123A63", "#EAF2FA", "#1B6E52", "#E2F1EA"
AMBRA, AMBRAF, GRIGIO, TENUE = "#6B4A05", "#F8EFDB", "#44535F", "#FBFDFE"

def font_b64():
    p = os.path.join(QUI, "caratteri", "archivo.woff2")
    if not os.path.exists(p): return ""
    d = base64.b64encode(open(p, "rb").read()).decode()
    return ("@font-face{font-family:'Archivo';font-weight:100 900;font-display:swap;"
            f"src:url(data:font/woff2;base64,{d}) format('woff2')}}")

def leggi(path):
    t = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", t, re.S)
    meta, corpo = {}, t
    if m:
        for r in m.group(1).split("\n"):
            if ":" in r:
                k, v = r.split(":", 1)
                meta[k.strip()] = v.strip().strip('"')
        corpo = m.group(2)
    return meta, corpo

def inline(s):
    s = H.escape(s)
    def _cod(m):
        t = m.group(1)
        e = t.replace("&lt;","<").replace("&gt;",">")
        # badge blu solo se e' una scritta che compare a video: tutta maiuscola
        if e.upper() == e and re.search(r"[A-Z]", e) and "/" not in e:
            return f'<span class="schermo">{t}</span>'
        return f'<span class="perc">{t}</span>' 
    s = re.sub(r"`([^`]+)`", _cod, s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<i>\1</i>", s)
    s = s.replace("&lt;br&gt;", "<br>")
    return s

def tabella(righe):
    out = ['<table class="stacchi">']
    intest = [c.strip() for c in righe[0].strip("|").split("|")]
    out.append("<tr>" + "".join(f"<th>{inline(c)}</th>" for c in intest) + "</tr>")
    for r in righe[2:]:
        c = [x.strip() for x in r.strip("|").split("|")]
        testo = " ".join(c)
        if "fine dei primi 5 secondi" in testo or "gancio" in testo.lower() and not c[0]:
            out.append(f'<tr class="gancio"><td colspan="{len(intest)}">'
                       + inline(re.sub(r"[—*]", "", testo).strip()) + "</td></tr>")
            continue
        celle = []
        for i, x in enumerate(c):
            cl = ""
            if i == 4: cl = ' class="ser"'      # si dice
            elif i == 5: cl = ' class="att"'    # scritta a schermo
            celle.append(f"<td{cl}>{inline(x) if x != '—' else '<span class=vuoto>—</span>'}</td>")
        out.append("<tr>" + "".join(celle) + "</tr>")
    out.append("</table>")
    return "\n".join(out)

def corpo_html(corpo):
    out, righe, i = [], corpo.split("\n"), 0
    lista = False
    while i < len(righe):
        r = righe[i]
        if r.startswith("|"):
            blocco = []
            while i < len(righe) and righe[i].startswith("|"):
                blocco.append(righe[i]); i += 1
            if lista: out.append("</ul>"); lista = False
            out.append(tabella(blocco)); continue
        if r.startswith("## "):
            if lista: out.append("</ul>"); lista = False
            out.append(f"<h2>{inline(r[3:])}</h2>")
        elif r.startswith("# "):
            pass                                  # il titolo sta gia' in testata
        elif r.lstrip().startswith("> "):
            if lista: out.append("</ul>"); lista = False
            t = r.lstrip()[2:]
            cl = "nota" if "regola dei 5 secondi" in t else "cit"
            out.append(f'<div class="{cl}">{inline(t)}</div>')
        elif r.startswith("- "):
            if not lista: out.append("<ul>"); lista = True
            out.append(f"<li>{inline(r[2:])}</li>")
        elif r.strip():
            if lista: out.append("</ul>"); lista = False
            out.append(f"<p>{inline(r.strip())}</p>")
        i += 1
    if lista: out.append("</ul>")
    return "\n".join(out)

CSS = f"""
{{FONT}}
@page{{size:A4;margin:14mm 13mm 13mm}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:'Archivo',system-ui,sans-serif;color:#1A2A3A;
     font-size:9pt;line-height:1.5;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.testata{{background:{NAVY};color:#fff;padding:14px 16px;border-radius:8px;margin-bottom:12px}}
.occhiello{{font-size:6.6pt;letter-spacing:.22em;color:#9CCBE8;font-weight:600;margin:0 0 5px}}
.titolo{{font-size:17pt;font-weight:700;margin:0;line-height:1.15}}
.dati{{display:flex;flex-wrap:wrap;gap:4px 18px;margin-top:10px;font-size:7.4pt;color:#D6E4F0}}
.dati b{{color:#fff;font-weight:600}}
h2{{font-size:10pt;color:{NAVY};margin:16px 0 6px;padding-bottom:3px;border-bottom:1.5px solid {CHIARO}}}
p{{margin:5px 0}}
ul{{margin:5px 0 5px 16px;padding:0}} li{{margin:3px 0}}
.cit{{background:#F6F8FB;border-left:3px solid #C8D6E5;padding:6px 11px;margin:3px 0;font-size:8.4pt;border-radius:0 4px 4px 0}}
.perc{{font-family:ui-monospace,monospace;font-size:7.6pt;color:{GRIGIO};background:#F1F4F8;padding:1px 4px;border-radius:3px}}
.nota{{background:{CHIARO};border-left:3px solid {NAVY};padding:8px 11px;margin:8px 0;
      font-size:8.2pt;border-radius:0 5px 5px 0}}
table.stacchi{{width:100%;border-collapse:collapse;font-size:7.4pt;margin:6px 0 10px}}
.stacchi th{{background:{CHIARO};color:{NAVY};font-size:6.6pt;padding:5px 6px;
            letter-spacing:.06em;text-transform:uppercase;text-align:left;font-weight:700}}
.stacchi td{{padding:4px 6px;line-height:1.34;border-top:1px solid #E6EDF4;vertical-align:top}}
.stacchi tr.gancio td{{background:{VERDEF};color:{VERDE};font-size:6.6pt;font-weight:700;
                      letter-spacing:.1em;text-transform:uppercase;text-align:center;padding:3px 6px}}
.stacchi td.ser{{background:{TENUE};color:{GRIGIO}}}
.stacchi td.att{{background:{AMBRAF};color:{AMBRA}}}
.vuoto{{color:#AEBCC9}}
.schermo{{display:inline-block;background:{NAVY};color:#fff;font-size:6.6pt;font-weight:700;
         padding:2px 6px;border-radius:3px;letter-spacing:.06em}}
tr,li,.nota,.cit{{break-inside:avoid}} h2{{break-after:avoid}}
.piede{{margin-top:16px;padding-top:7px;border-top:1px solid {CHIARO};
       font-size:6.8pt;color:#7A8A99;display:flex;justify-content:space-between}}
"""

def fai(n):
    g = glob.glob(os.path.join(QUI, "copioni", f"reel-{n:02d}-*.md"))
    if not g: print(f"  reel {n}: copione non trovato"); return None
    meta, corpo = leggi(g[0])
    dati = [("Chi parla", meta.get("chi_parla","")), ("Lingua", meta.get("lingua_parlata","")),
            ("Paese", meta.get("paese","")), ("Formato", meta.get("formato","")),
            ("Stacchi", meta.get("numero_stacchi","")),
            ("Durata totale", (meta.get("durata_totale_secondi","") + " s").strip()),
            ("Parola chiave", meta.get("parola_chiave",""))]
    doc = f"""<!DOCTYPE html><html lang="it"><head><meta charset="utf-8">
<title>{H.escape(meta.get('titolo',''))}</title>
<style>{CSS.replace('{FONT}', font_b64())}</style></head><body>
<div class="testata">
  <p class="occhiello">COPIONE REEL · {H.escape(meta.get('campagna','').upper())}</p>
  <h1 class="titolo">{H.escape(meta.get('id','').replace('reel-','Reel '))} — {H.escape(meta.get('titolo',''))}</h1>
  <div class="dati">{''.join(f'<span><b>{k}:</b> {H.escape(str(v))}</span>' for k,v in dati if v)}</div>
</div>
{corpo_html(corpo)}
<div class="piede"><span>NIPEC · PHD System S.r.l.</span>
<span>{H.escape(os.path.basename(g[0]))}</span></div>
</body></html>"""
    htm = os.path.join(QUI, f".copione-{n:02d}.html")
    pdf = os.path.join(QUI, f"COPIONE-reel-{n:02d}-{meta.get('paese','').lower()}.pdf")
    open(htm, "w", encoding="utf-8").write(doc)
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                    "--no-pdf-header-footer", f"--print-to-pdf={pdf}", "file://" + htm],
                   capture_output=True)
    os.remove(htm)
    print(f"  reel {n:02d}  ->  {os.path.basename(pdf)}  ({os.path.getsize(pdf)//1024} kB)")
    return pdf

if __name__ == "__main__":
    a = sys.argv[1:] or ["1"]
    nums = range(1, 10) if a[0] == "tutti" else [int(x) for x in a]
    print("PDF generati:")
    for n in nums: fai(n)
