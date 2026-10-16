import re
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen

SORG='protocolli/DEMETRA/caratteri/archivo.woff2'
CACHE={}
def _font(peso):
    if peso not in CACHE:
        CACHE[peso]=instancer.instantiateVariableFont(TTFont(SORG), {'wght': peso})
    return CACHE[peso]

def tracciati(testo, x, y, dim, spaziatura, peso, colore):
    f=_font(peso); gs=f.getGlyphSet(); cmap=f.getBestCmap(); upm=f['head'].unitsPerEm
    s=dim/upm; d=[]; px=x
    for ch in testo:
        nome=cmap.get(ord(ch))
        if nome is None:
            px += dim*0.5 + spaziatura; continue
        g=gs[nome]; pen=SVGPathPen(gs); g.draw(pen); fr=pen.getCommands()
        if fr:
            d.append(f'<path transform="translate({px:.3f},{y:.3f}) scale({s:.6f},{-s:.6f})" d="{fr}"/>')
        px += g.width*s + spaziatura
    return '  <g fill="{}">\n    {}\n  </g>'.format(colore, '\n    '.join(d))

def converti(svg):
    """Ogni <text> del logo diventa contorni. Il resto non si tocca."""
    def sost(m):
        tag, testo = m.group(0), m.group(2)
        def attr(n, d=None, num=True):
            r=re.search(r'%s="([^"]+)"'%n, tag)
            if not r: return d
            return float(r.group(1)) if num else r.group(1)
        return tracciati(testo, attr('x'), attr('y'), attr('font-size'),
                         attr('letter-spacing',0.0), attr('font-weight',400.0),
                         attr('fill','#000000',num=False))
    return re.sub(r'<text([^>]*)>(.*?)</text>', sost, svg, flags=re.S)

# --------------------------------------------------------------------------
# Rifa' da zero il pacchetto del marchio da girare a chi lavora.
# Si lancia dalla radice del repository:   python3 MARCHIO/fai-il-pacchetto.py
# --------------------------------------------------------------------------
import os, glob, shutil, subprocess

SH='/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell'
CH='/opt/pw-browsers/chromium-1194/chrome-linux/chrome'

def costruisci(base):
    out=os.path.join(base,'NIPEC-MARCHIO-2026')
    shutil.rmtree(out, ignore_errors=True)
    cart=['1-SVG','1-SVG/testo-modificabile','2-PNG-trasparente','3-PNG-con-fondo',
          '4-PDF-vettoriale','5-ICONE-APP','6-CARATTERI']
    for d in cart: os.makedirs(os.path.join(out,d), exist_ok=True)
    tmp=os.path.join(base,'tmp'); os.makedirs(tmp, exist_ok=True)

    def png(svg,w,h,dest,fondo='transparent'):
        p=os.path.join(tmp,'p.html')
        open(p,'w',encoding='utf-8').write(
            f'<!doctype html><meta charset="utf-8"><style>html,body{{margin:0;padding:0;'
            f'background:{fondo};overflow:hidden}}svg{{display:block}}</style>'
            + svg.replace('<svg ', f'<svg width="{w}" height="{h}" ',1))
        subprocess.run([SH,'--no-sandbox',f'--screenshot={dest}',f'--window-size={w},{h}',
                        '--default-background-color=00000000','--hide-scrollbars',p],capture_output=True)

    def pdf(svg,wmm,hmm,dest):
        p=os.path.join(tmp,'p.html')
        open(p,'w',encoding='utf-8').write(
            f'<!doctype html><meta charset="utf-8"><style>@page{{size:{wmm:.2f}mm {hmm:.2f}mm;margin:0}}'
            f'html,body{{margin:0;padding:0}}svg{{display:block}}</style>'
            + svg.replace('<svg ', f'<svg width="{wmm:.2f}mm" height="{hmm:.2f}mm" ',1))
        subprocess.run([CH,'--headless=new','--no-sandbox','--disable-gpu','--no-pdf-header-footer',
                        f'--print-to-pdf={dest}','--virtual-time-budget=4000',p],capture_output=True)

    for f in sorted(glob.glob('MARCHIO/*.svg')):
        vivo=open(f,encoding='utf-8').read()
        n=os.path.basename(f)[:-4]
        w,h=re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"',vivo).group(1,2)
        w,h=float(w),float(h); r=h/w; neg='negativo' in f
        sv=converti(vivo)                      # il testo diventa contorni
        open(os.path.join(out,'1-SVG',n+'.svg'),'w',encoding='utf-8').write(sv)
        open(os.path.join(out,'1-SVG/testo-modificabile',n+'.svg'),'w',encoding='utf-8').write(vivo)
        for larg in ([256,512,1024] if w==h else [500,1000,2000]):
            png(sv,larg,max(1,round(larg*r)), os.path.join(out,'2-PNG-trasparente',f'{n}-{larg}px.png'))
        larg=1024 if w==h else 2000
        png(sv,larg,max(1,round(larg*r)),
            os.path.join(out,'3-PNG-con-fondo',
                         f'{n}-{"fondo-blu" if neg else "fondo-bianco"}-{larg}px.png'),
            '#123A63' if neg else '#FFFFFF')
        pdf(sv,120.0,120.0*r, os.path.join(out,'4-PDF-vettoriale',n+'.pdf'))

    for f in glob.glob('APP-ALERT-LASER/icona-*.png')+glob.glob('APP-ALERT-LASER/apple-touch-icon.png'):
        shutil.copy(f, os.path.join(out,'5-ICONE-APP', os.path.basename(f)))
    for f in glob.glob('protocolli/DEMETRA/caratteri/*.woff2'):
        shutil.copy(f, os.path.join(out,'6-CARATTERI', os.path.basename(f)))
    return out

if __name__=='__main__':
    import sys
    base=sys.argv[1] if len(sys.argv)>1 else '.'
    print('fatto:', costruisci(base))
