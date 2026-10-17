import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'fs';
const NOMI = ['index','sq','en','laser-ares','laser-uriel','afrodite','borea-cryo','q-switch','metodo','formazione','chi-siamo','contatti','privacy'];
const PAGINE = {'Main.dc.html':'index.html','Home-SQ.dc.html':'sq.html','Home-EN.dc.html':'en.html',
  'Laser-Ares.dc.html':'laser-ares.html','Laser-Uriel.dc.html':'laser-uriel.html','Afrodite.dc.html':'afrodite.html',
  'Borea-Cryo.dc.html':'borea-cryo.html','Q-Switch.dc.html':'q-switch.html','Metodo.dc.html':'metodo.html',
  'Formazione.dc.html':'formazione.html','Chi-siamo.dc.html':'chi-siamo.html','Contatti.dc.html':'contatti.html',
  'Privacy.dc.html':'privacy.html'};
// marcatore -> quanti livelli salire prima di rimuovere (0 = il genitore del nodo di testo)
const TOGLI = [
  ['[FOTO]', 1], ['[FOTO LASER Q-SWITCH]', 1], ['[FOTO LAZER Q-SWITCH]', 1], ['[Q-SWITCH LASER PHOTO]', 1],
  ['[VOTO]', 0], ['[NOTA]', 0], ['[RATING]', 0],
  ['[DETTAGLIO DA CONFERMARE]', 1],
  ['[POTENZA,', 1], ['[DA SCHEDA', 1],
  ['[FOTO LASER Q-SWITCH —', 1],
  ['[FOTO DEL FONDATORE', 1],
  ['[UNA FRASE PERSONALE DI GIORGIO', 0],
];
const SEZIONI = ['[TESTIMONIANZA REALE','[DËSHMI E VËRTETË','[REAL TESTIMONIAL','[SEDE E ORARI]'];
const FOTO = [[/ARES/i,'e493bbb796de'],[/URIEL/i,'6f5180704064'],[/Afrodite/i,'741b069dc662'],[/Borea|Cryo/i,'6e62d1fde578']];

const b = await chromium.launch({ args:['--no-sandbox'] });
const p = await (await b.newContext({viewport:{width:1440,height:1200}})).newPage();
await p.goto('http://127.0.0.1:8741/index.html', { waitUntil:'load', timeout:120000 });
await p.waitForTimeout(14000);
const fr = p.frames().slice(1);
fs.mkdirSync('pulito', { recursive:true });
for (let i=0;i<NOMI.length;i++){
  const r = await fr[i].evaluate(async ([TOGLI,SEZIONI,FOTO_S,PAGINE]) => {
    const log=[];
    const FOTO = FOTO_S.map(([re,h])=>[new RegExp(re[0],re[1]),h]);
    const nodiCon = (frag) => {
      const out=[], w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
      let n; while(n=w.nextNode()){
        if(n.parentElement && n.parentElement.closest('script,style')) continue;
        if(n.nodeValue.includes(frag)) out.push(n);
      } return out;
    };
    // 1. sezioni intere
    for (const s of SEZIONI){
      for (const n of nodiCon(s)){
        const sez = n.parentElement.closest('section');
        if (sez) { sez.remove(); log.push('sezione tolta: '+s); }
      }
    }
    // 2. elementi singoli
    for (const [marc,su] of TOGLI){
      for (const n of nodiCon(marc)){
        let e = n.parentElement; for(let k=0;k<su&&e&&e.parentElement;k++) e=e.parentElement;
        if (e && e !== document.body) { e.remove(); log.push('tolto '+marc+' ('+su+')'); }
      }
    }
    // 3. righe di tabella rimaste vuote / segnaposto residui in TD
    document.querySelectorAll('td,th').forEach(td=>{ if(/\[[^\]]{3,70}\]/.test(td.textContent)){ const tr=td.closest('tr'); if(tr){tr.remove(); log.push('riga tolta');} } });
    // 4a. immagini vere: calcola l'impronta e punta al file locale
    const impronta = async (u) => {
      const bb = await (await fetch(new URL(u,'http://127.0.0.1:8741/').href)).arrayBuffer();
      const h = await crypto.subtle.digest('SHA-1', bb);
      return [...new Uint8Array(h)].map(x=>x.toString(16).padStart(2,'0')).join('').slice(0,12);
    };
    for (const im of document.querySelectorAll('img[src^="blob:"]')) {
      const h = await impronta(im.getAttribute('src'));
      im.setAttribute('src','immagini/'+h+'.jpg');
      im.setAttribute('loading','lazy'); im.setAttribute('decoding','async');
      log.push('immagine: '+h);
    }
    // 4b. immagini rotte: assegna la foto giusta dall'alt, altrimenti togli
    document.querySelectorAll('img').forEach(im=>{
      const src=im.getAttribute('src')||'';
      if (!src.startsWith('/_blob/')) return;
      const alt=im.getAttribute('alt')||'';
      const f=FOTO.find(([re])=>re.test(alt));
      if (f){ im.setAttribute('src','immagini/'+f[1]+'.jpg'); im.setAttribute('loading','lazy'); log.push('foto da alt: '+alt.slice(0,30)); }
      else { const sp=im.parentElement; im.remove(); if(sp&&!sp.children.length&&!sp.textContent.trim()) sp.remove(); log.push('img tolta: '+alt.slice(0,30)); }
    });
    // 5. link
    document.querySelectorAll('a[href]').forEach(a=>{
      const h=a.getAttribute('href');
      if (PAGINE[h]) { a.setAttribute('href',PAGINE[h]); return; }
      if (h && h.startsWith('Privacy.dc.html#')) { a.setAttribute('href','privacy.html#'+h.split('#')[1]); return; }
      if (h==='[LINK SCHEDA LASER 808 PDF]'){ a.setAttribute('href','scheda-laser-808.pdf'); a.setAttribute('target','_blank'); a.setAttribute('rel','noopener'); return; }
      if (h && h.startsWith('[')) {                       // link morto: smonta l'ancora
        const sp=document.createElement('span'); sp.innerHTML=a.innerHTML;
        if (/CATALOG|KATALOG/i.test(h)) a.remove(); else a.replaceWith(sp);
        log.push('link morto: '+h); return;
      }
      if (h==='tel:800141726' || h==='mailto:info@nipecestetica.com'){ a.remove(); log.push('contatto tolto: '+h); }
    });
    return { html: document.documentElement.outerHTML, log };
  }, [TOGLI,SEZIONI,FOTO.map(([re,h])=>[[re.source,re.flags],h]),PAGINE]);
  fs.writeFileSync(`pulito/${NOMI[i]}.html`, r.html);
  console.log(`\n### ${NOMI[i]} (${r.html.length} B)`);
  if (r.log.length) console.log('   '+[...new Set(r.log)].join('\n   '));
}
await b.close();
