# -*- coding: utf-8 -*-
import pymupdf

NAVY   = (0x11/255, 0x39/255, 0x62/255)
BLU    = (0x1B/255, 0x6E/255, 0xA3/255)
AZZURRO= (0x59/255, 0xA6/255, 0xD5/255)
RIGA   = (0xE1/255, 0xE7/255, 0xEF/255)
VELO   = (0xF4/255, 0xF7/255, 0xFB/255)
GRIGIO = (0x6B/255, 0x74/255, 0x7C/255)
INK    = (0x1F/255, 0x2A/255, 0x36/255)
CREMA  = (0xEB/255, 0xDE/255, 0xC6/255)
CREMAV = (0xFD/255, 0xF8/255, 0xEE/255)

L, R = 61.5, 533.8          # margini come nelle pagine 1-2
W = R - L
COL = (W - 22) / 2          # due colonne

d = pymupdf.open('originale.pdf')
pg = d.new_page(width=595.276, height=841.890)
CARATTERI = {}
for nome, file in (('Arch', 'caratteri/archivo-400.ttf'), ('ArchS', 'caratteri/archivo-600.ttf'), ('ArchB', 'caratteri/archivo-700.ttf')):
    pg.insert_font(fontname=nome, fontfile=file)
    CARATTERI[nome] = pymupdf.Font(fontfile=file)

def larghezza(s, f='Arch', size=9):
    return CARATTERI[f].text_length(s, fontsize=size)

def testo(x, y, s, f='Arch', size=9, col=INK, spazio=0):
    if spazio:
        for ch in s:
            pg.insert_text((x, y), ch, fontname=f, fontsize=size, color=col)
            x += larghezza(ch, f, size) + spazio
    else:
        pg.insert_text((x, y), s, fontname=f, fontsize=size, color=col)

def etichetta(x, y, s):
    testo(x, y, s.upper(), 'ArchS', 7.2, BLU, spazio=1.5)

campi = []   # (nome, x, y, w, h, dimensione)

def campo(x, y, w, nome, etich, h=19):
    """etichetta piccola, poi la riga su cui si scrive"""
    testo(x, y, etich, 'Arch', 7.6, GRIGIO)
    pg.draw_rect(pymupdf.Rect(x, y + 4, x + w, y + 4 + h), color=None, fill=VELO)
    pg.draw_line(pymupdf.Point(x, y + 4 + h), pymupdf.Point(x + w, y + 4 + h), color=RIGA, width=0.8)
    campi.append((nome, x + 3, y + 5, w - 6, h - 2))

# ---------- titolo ----------
testo(L, 64, 'Pranimi i propozimit', 'ArchB', 19, NAVY)
testo(L, 82, 'Paketa VOGUE · qira me opsion blerjeje · propozim i datës 6 tetor 2026',
      'Arch', 9, GRIGIO)
pg.draw_line(pymupdf.Point(L, 94), pymupdf.Point(R, 94), color=RIGA, width=1)

# ---------- dati del cliente ----------
y = 118
etichetta(L, y, 'Të dhënat e klientit')
y += 16
campo(L,        y, COL, 'subjekti',      'Subjekti / qendra')
campo(L+COL+22, y, COL, 'nipt',          'NIPT')
y += 46
campo(L,        y, COL, 'adresa',        'Adresa')
campo(L+COL+22, y, COL, 'email',         'E-mail')
y += 46
campo(L,        y, COL, 'perfaqesuesi',  'Përfaqësuesi ligjor')
campo(L+COL+22, y, COL, 'telefon',       'Telefon')
y += 46

# ---------- cosa si firma ----------
alt = 118
pg.draw_rect(pymupdf.Rect(L, y, R, y + alt), color=BLU, fill=(0xF5/255,0xF9/255,0xFB/255),
             width=1, radius=0.03)
etichetta(L + 14, y + 22, 'Çfarë nënshkruhet')
righe = [
    ('Paketa',                      'Afrodite · Ermes · Ares'),
    ('Çmimi i bllokuar i paketës',  '€ 32.500   (në vend të € 65.000 të listës)'),
    ('Kaparo fillestar',            '€ 5.000'),
    ('Qira mujore',                 '€ 1.500 / muaj   ·   kohëzgjatja maks. 24 muaj'),
    ('Dorëzimi',                    'brenda 40 ditëve pune nga nënshkrimi i kontratës'),
]
yy = y + 40
for et, val in righe:
    testo(L + 14, yy, et, 'Arch', 8.4, GRIGIO)
    testo(L + 172, yy, val, 'ArchS', 8.8, NAVY)
    yy += 15.5
y += alt + 20

# ---------- dichiarazione ----------
testo(L, y, 'Nënshkruesi deklaron se ka lexuar dhe pranon propozimin në faqet 1 dhe 2, përfshirë kushtet e', 'Arch', 9, INK)
testo(L, y + 13.5, 'pagesës dhe të tërheqjes, dhe kërkon nënshkrimin e kontratës përkatëse.', 'Arch', 9, INK)
y += 36

# ---------- luogo e data ----------
campo(L,        y, COL, 'vendi', 'Vendi')
campo(L+COL+22, y, COL, 'data',  'Data')
y += 50

# ---------- firme ----------
etichetta(L, y, 'Nënshkrimet')
y += 12
altf = 96
for i, (tit, sotto) in enumerate((('Për NIPEC', 'Tecnologie Estetiche'), ('Klienti', 'vula dhe firma'))):
    x = L + i * (COL + 22)
    pg.draw_rect(pymupdf.Rect(x, y, x + COL, y + altf), color=RIGA, fill=(1,1,1), width=1)
    pg.draw_line(pymupdf.Point(x+12, y+altf-24), pymupdf.Point(x+COL-12, y+altf-24), color=RIGA, width=0.8)
    testo(x + 12, y + altf - 11, tit, 'ArchS', 8.6, NAVY)
    testo(x + 12 + larghezza(tit, 'ArchS', 8.6) + 6, y + altf - 11, '· ' + sotto, 'Arch', 7.6, GRIGIO)
y += altf + 16

# ---------- come si firma ----------
pg.draw_rect(pymupdf.Rect(L, y, R, y + 30), color=CREMA, fill=CREMAV, width=0.8)
testo(L + 12, y + 12.5, 'Nënshkrimi në ekran, me stilolaps:', 'ArchS', 7.8, (0x8A/255,0x62/255,0x08/255))
testo(L + 12 + larghezza('Nënshkrimi në ekran, me stilolaps: ', 'ArchS', 7.8), y + 12.5, 'Microsoft Edge > Vizato (Draw)   ·   Adobe Acrobat Reader > Plotëso dhe nënshkruaj > Vizato.', 'Arch', 7.8, GRIGIO)
testo(L + 12, y + 23.5, 'Fushat e bardha plotësohen duke shkruar; nënshkrimi vizatohet brenda kutive.', 'Arch', 7.8, GRIGIO)

# ---------- piè di pagina, uguale alle pagine 1-2 ----------
pg.draw_line(pymupdf.Point(L, 700), pymupdf.Point(R, 700), color=RIGA, width=1)
testo(L, 717, 'NIPEC', 'ArchB', 8.6, NAVY)
testo(L + 34, 717, '· Tecnologie Estetiche', 'Arch', 8.6, GRIGIO)
s = 'Asistencë '
w1 = larghezza(s, 'Arch', 8.6)
w2 = larghezza('351 846 6025', 'ArchB', 8.6)
testo(R - w1 - w2, 717, s, 'Arch', 8.6, GRIGIO)
testo(R - w2, 717, '351 846 6025', 'ArchB', 8.6, NAVY)

# ---------- i campi compilabili ----------
for nome, x, yy, w, h in campi:
    wd = pymupdf.Widget()
    wd.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    wd.field_name = nome
    wd.rect = pymupdf.Rect(x, yy, x + w, yy + h)
    wd.text_fontsize = 10
    wd.text_font = 'Helv'
    wd.text_color = (0, 0, 0)
    wd.fill_color = None
    wd.border_width = 0
    pg.add_widget(wd)

d.save('VOGUE-da-firmare.pdf', garbage=4, deflate=True)
print('fatto: %d pagine, %d campi' % (d.page_count, len(campi)))
