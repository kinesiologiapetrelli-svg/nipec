# -*- coding: utf-8 -*-
"""Un piccolo valutatore di formule: legge la stringa esatta che finisce
nel foglio e la calcola, con le regole di Excel/Fogli.
Serve a provare la trascrizione, non solo il ragionamento."""
import re, datetime

class Vuoto:                      # la cella vuota: "" nei confronti, 0 nei conti
    def __repr__(self): return "(vuoto)"
VUOTO = Vuoto()

def _num(v):
    if isinstance(v, Vuoto): return 0
    if isinstance(v, bool): return 1 if v else 0
    if isinstance(v, datetime.date): return (v - datetime.date(1899, 12, 30)).days
    if isinstance(v, str):
        if v == "": return 0
        try: return float(v)
        except ValueError: raise ValueError("#VALUE! " + v)
    return v

def _txt(v):
    if isinstance(v, Vuoto): return ""
    if isinstance(v, bool): return "TRUE" if v else "FALSE"
    if isinstance(v, float) and v == int(v): return str(int(v))
    if isinstance(v, datetime.date): return str(_num(v))
    return str(v)

def _confronta(a, b, op):
    if isinstance(a, list): return [_confronta(x, b, op) for x in a]
    if isinstance(b, list): return [_confronta(a, y, op) for y in b]
    """Excel: il testo sta sempre sopra i numeri; la cella vuota vale "" o 0
    a seconda di con chi la confronti."""
    def rango(v):
        if isinstance(v, Vuoto): return None
        return 1 if isinstance(v, str) else 0
    ra, rb = rango(a), rango(b)
    if ra is None: a = "" if rb == 1 or rb is None else 0
    if rb is None: b = "" if ra == 1 or ra is None else 0
    ta = 1 if isinstance(a, str) else 0
    tb = 1 if isinstance(b, str) else 0
    if ta != tb:                       # numero contro testo
        x, y = ta, tb
    else:
        x = a.upper() if ta else _num(a)
        y = b.upper() if tb else _num(b)
    return {"=": x == y, "<>": x != y, "<": x < y, ">": x > y, "<=": x <= y, ">=": x >= y}[op]

class Errore(Exception): pass

class Err:                        # un errore di foglio, non un errore di Python
    def __repr__(self): return "#N/D"
ERR = Err()

# ------------------------------------------------------------------ lettura
GETTONE = re.compile(r"""
 \s*(?:
   (?P<testo>"(?:[^"]|"")*")
 | (?P<rif>(?:[A-Z_][A-Z_0-9]*!)?\$?[A-Z]{1,3}\$?\d+(?::\$?[A-Z]{1,3}\$?\d+)?)
 | (?P<fun>[A-Z][A-Z0-9_.]*)\s*\(
 | (?P<num>\d+(?:\.\d+)?)
 | (?P<op><=|>=|<>|[-+*/&=<>])
 | (?P<par>[(),;])
 )""", re.X)

def leggi(s):
    fuori, i = [], 0
    while i < len(s):
        m = GETTONE.match(s, i)
        if not m: raise Errore("non capisco: " + s[i:i+20])
        i = m.end()
        for k in ("testo", "rif", "fun", "num", "op", "par"):
            if m.group(k) is not None:
                fuori.append((k, m.group(k))); break
    return fuori

class Analizzatore:
    def __init__(self, gettoni, foglio): self.g, self.i, self.f = gettoni, 0, foglio
    def sbircia(self): return self.g[self.i] if self.i < len(self.g) else (None, None)
    def prendi(self): t = self.sbircia(); self.i += 1; return t
    def espressione(self):
        v = self.concatena()
        while self.sbircia()[0] == "op" and self.sbircia()[1] in ("=", "<>", "<", ">", "<=", ">="):
            op = self.prendi()[1]; v = _confronta(v, self.concatena(), op)
        return v
    def concatena(self):
        v = self.somma()
        while self.sbircia() == ("op", "&"):
            self.prendi(); v = _txt(v) + _txt(self.somma())
        return v
    def somma(self):
        v = self.prodotto()
        while self.sbircia()[0] == "op" and self.sbircia()[1] in ("+", "-"):
            op = self.prendi()[1]; d = self.prodotto()
            v = _num(v) + _num(d) if op == "+" else _num(v) - _num(d)
        return v
    def prodotto(self):
        v = self.unario()
        while self.sbircia()[0] == "op" and self.sbircia()[1] in ("*", "/"):
            op = self.prendi()[1]; d = self.unario()
            if isinstance(v, list) or isinstance(d, list):
                va = v if isinstance(v, list) else [v] * len(d)
                da = d if isinstance(d, list) else [d] * len(va)
                v = [_num(x) * _num(y) for x, y in zip(va, da)]
            else:
                v = _num(v) * _num(d) if op == "*" else _num(v) / _num(d)
        return v
    def unario(self):
        if self.sbircia() == ("op", "-"): self.prendi(); return -_num(self.unario())
        return self.atomo()
    def argomenti(self):
        args = []
        if self.sbircia()[1] == ")": self.prendi(); return args
        while True:
            args.append(self.espressione())
            k, v = self.prendi()
            if v == ")": return args
            if v not in (",", ";"): raise Errore("virgola attesa, trovato " + str(v))
    def atomo(self):
        k, v = self.prendi()
        if k == "num":  return float(v)
        if k == "testo": return v[1:-1].replace('""', '"')
        if k == "rif":  return self.f.leggi(v)
        if k == "par" and v == "(":
            e = self.espressione()
            if self.prendi()[1] != ")": raise Errore("parentesi")
            return e
        if k == "fun":  return self.chiama(v.upper())
        raise Errore("atomo inatteso: %s %s" % (k, v))
    def chiama(self, nome):
        if nome == "IF":                       # pigro: valuta solo il ramo giusto
            cond = self.espressione(); self.prendi()
            a = self.espressione()
            k, v = self.prendi()
            b = self.espressione() if v in (",", ";") else VUOTO
            if v in (",", ";") and self.prendi()[1] != ")": raise Errore("IF")
            vero = cond if isinstance(cond, bool) else _num(cond) != 0
            return a if vero else (b if b is not VUOTO else False)
        if nome == "IFERROR":
            a = self.espressione(); self.prendi()
            b = self.espressione(); self.prendi()
            return b if a is ERR else a
        a = self.argomenti()
        return self.f.funzione(nome, a)


# ------------------------------------------------------------------- foglio
RIF = re.compile(r"^(?:([A-Z_][A-Z_0-9]*)!)?\$?([A-Z]{1,3})\$?(\d+)(?::\$?([A-Z]{1,3})\$?(\d+))?$")

def num_col(l):
    n = 0
    for c in l: n = n * 26 + ord(c) - 64
    return n

def let_col(n):
    s = ""
    while n: n, r = divmod(n - 1, 26); s = chr(65 + r) + s
    return s

class Foglio:
    def __init__(self, celle, corrente="CLIENTI"):
        self.celle = celle          # {"CLIENTI!A5": valore, ...}
        self.corrente = corrente
        self.riga = 5

    def val(self, foglio, col, riga):
        return self.celle.get("%s!%s%d" % (foglio, col, riga), VUOTO)

    def leggi(self, rif):
        m = RIF.match(rif)
        if not m: raise Errore("riferimento strano: " + rif)
        fg = m.group(1) or self.corrente
        c1, r1, c2, r2 = m.group(2), int(m.group(3)), m.group(4), m.group(5)
        if not c2:
            return self.val(fg, c1, r1)
        fuori = []
        for cn in range(num_col(c1), num_col(c2) + 1):
            for rr in range(r1, int(r2) + 1):
                fuori.append(self.val(fg, let_col(cn), rr))
        return fuori

    def funzione(self, nome, a):
        piatto = lambda x: [v for e in x for v in (e if isinstance(e, list) else [e])]
        vero = lambda v: v if isinstance(v, bool) else _num(v) != 0
        if nome == "AND":  return all(vero(v) for v in piatto(a))
        if nome == "OR":   return any(vero(v) for v in piatto(a))
        if nome == "NOT":  return not vero(a[0])
        if nome == "N":    return _num(a[0]) if not isinstance(a[0], str) else 0
        if nome == "TODAY":return OGGI
        if nome == "ROW":  return self.riga if not a else a[0]
        if nome == "LEN":  return len(_txt(a[0]))
        if nome == "LEFT": return _txt(a[0])[:int(_num(a[1])) if len(a) > 1 else 1]
        if nome == "MID":  return _txt(a[0])[int(_num(a[1])) - 1:int(_num(a[1])) - 1 + int(_num(a[2]))]
        if nome == "MIN":  return min(_num(v) for v in piatto(a) if not isinstance(v, (str, Vuoto)))
        if nome == "MAX":
            n = [_num(v) for v in piatto(a) if not isinstance(v, (str, Vuoto))]
            return max(n) if n else 0
        if nome == "ROUND":return round(_num(a[0]), int(_num(a[1])))
        if nome == "SUM":  return sum(_num(v) for v in piatto(a) if not isinstance(v, (str, Vuoto)))
        if nome == "COUNTA": return sum(1 for v in piatto(a) if not isinstance(v, Vuoto) and v != "")
        if nome == "EDATE":
            d = a[0] if isinstance(a[0], datetime.date) else datetime.date(1899, 12, 30) + datetime.timedelta(days=int(_num(a[0])))
            m = d.month - 1 + int(_num(a[1])); anno = d.year + m // 12; mese = m % 12 + 1
            ultimo = [31, 29 if anno % 4 == 0 and (anno % 100 or anno % 400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][mese - 1]
            return datetime.date(anno, mese, min(d.day, ultimo))
        if nome == "MATCH":
            for i, v in enumerate(piatto([a[1]])):
                if _txt(v).upper() == _txt(a[0]).upper(): return i + 1
            return ERR
        if nome == "INDEX":
            i = int(_num(a[1]))
            lista = a[0] if isinstance(a[0], list) else [a[0]]
            return lista[i - 1] if 1 <= i <= len(lista) else ERR
        if nome == "SMALL":
            n = sorted(_num(v) for v in piatto([a[0]]) if not isinstance(v, (str, Vuoto)))
            k = int(_num(a[1]))
            return n[k - 1] if 1 <= k <= len(n) else ERR
        if nome in ("COUNTIF", "COUNTIFS", "SUMPRODUCT"):
            return self.conta(nome, a)
        raise Errore("funzione che non conosco: " + nome)

    def conta(self, nome, a):
        def combacia(v, crit):
            c = _txt(crit)
            for op in ("<=", ">=", "<>", "<", ">", "="):
                if c.startswith(op):
                    resto = c[len(op):]
                    try: b = float(resto)
                    except ValueError: b = resto
                    return _confronta(v, b, "=" if op == "=" else op)
            if c == "?*": return not isinstance(v, Vuoto) and _txt(v) != ""
            return _txt(v).upper() == c.upper()
        if nome == "COUNTIF":
            return sum(1 for v in a[0] for _ in [0] if combacia(v, a[1]))
        if nome == "COUNTIFS":
            colonne = [(a[i], a[i + 1]) for i in range(0, len(a), 2)]
            n = len(colonne[0][0])
            return sum(1 for i in range(n) if all(combacia(c[i], k) for c, k in colonne))
        if nome == "SUMPRODUCT":
            return sum(a[0]) if not isinstance(a[0], list) else sum(_num(v) for v in a[0])
        return 0

OGGI = datetime.date.today()

def calcola(formula, foglio, riga=5):
    foglio.riga = riga
    a = Analizzatore(leggi(formula.lstrip("=")), foglio)
    v = a.espressione()
    return "" if v is VUOTO else v
