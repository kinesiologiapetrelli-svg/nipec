import re, sys, html

CSS = """
:root{--carta:#fff;--riga:#d9e2e9;--inchiostro:#16222e;--tenue:#5a6b79;
--blu:#1c6ea4;--navy:#123a63;--blu-tenue:#e6eff7;
--sans:"Archivo","Liberation Sans",ui-sans-serif,system-ui,sans-serif;
--serif:"Source Serif 4","Liberation Serif",Georgia,serif;}
@page{size:A4;margin:16mm 15mm 14mm;}
*{box-sizing:border-box}
body{margin:0;font-family:var(--serif);color:var(--inchiostro);
font-size:10pt;line-height:1.5;background:var(--carta);}
h1{font-family:var(--sans);font-size:24pt;color:var(--navy);font-weight:700;
letter-spacing:-.015em;margin:0 0 .5em;line-height:1.1}
h2{font-family:var(--sans);font-size:13pt;color:var(--navy);font-weight:700;
margin:1.5em 0 .45em;padding-top:.5em;border-top:2px solid var(--navy);
break-after:avoid;letter-spacing:-.01em}
h3{font-family:var(--sans);font-size:10pt;color:var(--blu);font-weight:600;
margin:1.1em 0 .35em;break-after:avoid;text-transform:uppercase;
letter-spacing:.08em}
p{margin:.42em 0}
strong{font-family:var(--sans);font-weight:600;color:var(--navy)}
em{font-style:italic;color:var(--tenue)}
code{font-family:ui-monospace,"Liberation Mono",monospace;font-size:8.6pt;
background:var(--blu-tenue);padding:.5px 3px;border-radius:2px;color:var(--navy)}
hr{border:0;border-top:1px solid var(--riga);margin:1.2em 0}
ul{margin:.42em 0;padding-left:1.1em}
li{margin:.2em 0}
blockquote{margin:.6em 0;padding:.1em 0 .1em .9em;border-left:3px solid var(--blu);
color:var(--tenue);font-style:italic}
table{border-collapse:collapse;width:100%;margin:.7em 0;font-size:9pt;
break-inside:avoid}
th{font-family:var(--sans);font-size:8pt;text-transform:uppercase;
letter-spacing:.06em;text-align:left;background:var(--blu-tenue);
color:var(--navy);padding:5px 7px;border-bottom:1.5px solid var(--navy)}
td{padding:4.5px 7px;border-bottom:1px solid var(--riga);vertical-align:top}
.voce{break-inside:avoid;margin:.55em 0}
.ext{color:var(--blu);}
"""


def inline(t):
    t = html.escape(t)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', t)
    t = t.replace('▸', '<span class="ext">▸</span>')
    return t


def convert(md):
    lines = md.split('\n')
    out, i, n = [], 0, len(lines)
    para, ul, tbl = [], [], []

    def flush_p():
        if para:
            out.append('<p>' + inline(' '.join(para)) + '</p>')
            para.clear()

    def flush_ul():
        if ul:
            out.append('<ul>' + ''.join('<li>' + inline(x) + '</li>' for x in ul) + '</ul>')
            ul.clear()

    def flush_tbl():
        if not tbl:
            return
        rows = [r for r in tbl if not re.match(r'^\s*\|[\s:|-]+\|\s*$', r)]
        cells = [[c.strip() for c in r.strip().strip('|').split('|')] for r in rows]
        h = '<tr>' + ''.join('<th>' + inline(c) + '</th>' for c in cells[0]) + '</tr>'
        b = ''.join('<tr>' + ''.join('<td>' + inline(c) + '</td>' for c in r) + '</tr>'
                    for r in cells[1:])
        out.append('<table>' + h + b + '</table>')
        tbl.clear()

    def flush_all():
        flush_p(); flush_ul(); flush_tbl()

    while i < n:
        ln = lines[i]
        s = ln.strip()
        if s.startswith('|'):
            flush_p(); flush_ul(); tbl.append(s); i += 1; continue
        flush_tbl()
        if not s:
            flush_p(); flush_ul(); i += 1; continue
        if s.startswith('### '):
            flush_all(); out.append('<h3>' + inline(s[4:]) + '</h3>'); i += 1; continue
        if s.startswith('## '):
            flush_all(); out.append('<h2>' + inline(s[3:]) + '</h2>'); i += 1; continue
        if s.startswith('# '):
            flush_all(); out.append('<h1>' + inline(s[2:]) + '</h1>'); i += 1; continue
        if re.match(r'^---+$', s):
            flush_all(); out.append('<hr>'); i += 1; continue
        if s.startswith('> '):
            flush_all(); out.append('<blockquote>' + inline(s[2:]) + '</blockquote>')
            i += 1; continue
        if s.startswith('- '):
            flush_p(); ul.append(s[2:]); i += 1; continue
        # riga di continuazione di una voce di elenco: rientrata e con elenco aperto
        if ul and not para and (ln.startswith('  ') or ln.startswith('\t')):
            ul[-1] += ' ' + s; i += 1; continue
        flush_ul(); para.append(s); i += 1

    flush_all()
    return '\n'.join(out)


src, dst, title = sys.argv[1], sys.argv[2], sys.argv[3]
body = convert(open(src, encoding='utf-8').read())
open(dst, 'w', encoding='utf-8').write(
    '<!doctype html><html lang="it"><head><meta charset="utf-8">'
    f'<title>{html.escape(title)}</title><style>{CSS}</style></head><body>'
    + body + '</body></html>')
print('scritto', dst)
