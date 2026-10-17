import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'fs';
const P=['index','sq','en','laser-ares','laser-uriel','afrodite','borea-cryo','q-switch','metodo','formazione','chi-siamo','contatti','privacy'];
const b = await chromium.launch({ args:['--no-sandbox'] });
let problemi=0; const link=new Set();
for (const larg of [1440, 390]) {
  const c = await b.newContext({ viewport:{width:larg,height:900} });
  console.log(`\n================= ${larg==390?'TELEFONO':'DESKTOP'} (${larg}px) =================`);
  for (const n of P) {
    const p = await c.newPage(); const err=[];
    p.on('pageerror',e=>err.push('JS: '+e.message));
    p.on('console',m=>{ if(m.type()==='error') err.push('console: '+m.text()); });
    p.on('requestfailed',r=>err.push('richiesta fallita: '+r.url().split('/').pop()));
    p.on('response',r=>{ if(r.status()>=400) err.push('HTTP '+r.status()+': '+r.url().split('/').pop()); });
    await p.goto(`http://127.0.0.1:8751/${n}.html`, { waitUntil:'networkidle' });
    await p.waitForTimeout(500);
    const r = await p.evaluate(()=>{
      const t=document.body.innerText;
      const seg=[...new Set((t.match(/\[[A-ZÀ-ÙÈÉ][^\]]{2,70}\]|\{\{[^}]+\}\}/g)||[]))];
      const rotte=[...document.querySelectorAll('img')].filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.getAttribute('src'));
      const car=getComputedStyle(document.querySelector('h1')||document.body).fontFamily;
      return {h:document.documentElement.scrollHeight, w:document.documentElement.scrollWidth,
        car:t.length, seg, rotte, font:car,
        overflow: document.documentElement.scrollWidth > window.innerWidth+1,
        link:[...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href'))};
    });
    r.link.forEach(h=>link.add(h));
    const bad = err.length||r.seg.length||r.rotte.length||r.overflow;
    if (bad) problemi++;
    console.log(`${bad?'✗':'·'} ${n.padEnd(13)} ${String(r.h).padStart(5)}px alto · ${String(r.car).padStart(5)} car`
      + (r.overflow?`  ⚠ SBORDA (${r.w}px)`:'')
      + (r.seg.length?`  ⚠ SEGNAPOSTO: ${r.seg.join(', ')}`:'')
      + (r.rotte.length?`  ⚠ IMMAGINI ROTTE: ${r.rotte.join(', ')}`:'')
      + (err.length?`\n      ${[...new Set(err)].join('\n      ')}`:''));
    if (larg===1440 && n==='index') console.log('      carattere h1: '+r.font);
    await p.close();
  }
  await c.close();
}
console.log('\n=== link interni ===');
const files = new Set(fs.readdirSync('sitonuovo'));
[...link].filter(h=>h && !/^(https?:|mailto:|tel:|#)/.test(h)).sort().forEach(h=>{
  const f=h.split('#')[0];
  console.log((files.has(f)?'  ok  ':'  ROTTO ')+h);
  if(!files.has(f)) problemi++;
});
console.log('\nPROBLEMI:', problemi);
await b.close();
