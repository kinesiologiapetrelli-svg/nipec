# -*- coding: utf-8 -*-
import io,sys,json,base64,gzip,re,os,hashlib
F,OUT=sys.argv[1],sys.argv[2]
def blk(t,n):
    m=re.findall(r'<script type="__bundler/%s">\s*(.*?)\s*</script>'%n,t,re.S)
    return m[0] if m else None
def dati(v):
    d=base64.b64decode(v['data'])
    return gzip.decompress(d) if v.get('compressed') else d
t=io.open(F,encoding='utf-8',errors='replace').read()
man=json.loads(blk(t,'manifest')); ordine=json.loads(blk(t,'page_order'))
os.makedirs(OUT,exist_ok=True)
pagine=[]
for i,pid in enumerate(ordine):
    d=dati(man[pid]).decode('utf-8','replace')
    tpl=blk(d,'template'); m2=blk(d,'manifest'); ext=blk(d,'ext_resources')
    tpl=json.loads(tpl) if tpl else d
    m2=json.loads(m2) if m2 else {}
    titolo=(re.search(r'<title[^>]*>(.*?)</title>',tpl,re.S) or [None,''])[1].strip()
    io.open(os.path.join(OUT,'p%02d.html'%i),'w',encoding='utf-8').write(tpl)
    io.open(os.path.join(OUT,'p%02d.manifest.json'%i),'w',encoding='utf-8').write(json.dumps({k:{kk:vv for kk,vv in v.items() if kk!='data'} for k,v in m2.items()},indent=1))
    pagine.append(dict(i=i,id=pid,titolo=titolo,tpl=len(tpl),ris=len(m2),ext=json.loads(ext) if ext else []))
    # risorse: salva con hash, per de-duplicare fra le pagine
    for k,v in m2.items():
        b=dati(v); h=hashlib.sha1(b).hexdigest()[:12]
        est={'text/html':'html','text/css':'css','text/javascript':'js','application/javascript':'js',
             'font/woff2':'woff2','image/jpeg':'jpg','image/png':'png','image/svg+xml':'svg','image/webp':'webp'}.get(v['mime'],'bin')
        os.makedirs(os.path.join(OUT,'ris'),exist_ok=True)
        p=os.path.join(OUT,'ris','%s.%s'%(h,est))
        if not os.path.exists(p): io.open(p,'wb').write(b)
        # mappa uuid -> file, per pagina
        pagine[-1].setdefault('mappa',{})[k]='ris/%s.%s'%(h,est)
io.open(os.path.join(OUT,'_pagine.json'),'w',encoding='utf-8').write(json.dumps(pagine,indent=1,ensure_ascii=False))
print('%-3s %-52s %8s %5s %s' % ('#','titolo','tpl B','ris','ext_resources'))
for p in pagine:
    print('%-3d %-52s %8d %5d %s' % (p['i'],p['titolo'],p['tpl'],p['ris'],(p['ext'] or '')if p['ext'] else ''))
