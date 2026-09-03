import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const { chromium } = require('../qa-node/node_modules/playwright');
const browser = await chromium.launch({headless:true, executablePath:'/opt/data/projects/bovis-visuals/.artifacts/playwright-browsers/chromium-1200/chrome-linux64/chrome'});
const pages=[['integrated','http://127.0.0.1:4173/kbo/'],['players','http://127.0.0.1:4173/kbo-players/']];
const output=[];
for(const [kind,url] of pages) for(const width of [390,768,1440]){
  const page=await browser.newPage({viewport:{width,height:1200}}), errors=[];
  page.on('pageerror',e=>errors.push(e.message)); page.on('console',m=>{if(m.type()==='error'&&!m.text().includes('404'))errors.push(m.text())});
  await page.goto(url,{waitUntil:'networkidle'}); await page.waitForSelector(kind==='players'?'[data-player-card]':'[data-game-card]');
  const result=await page.evaluate(()=>({
    overflow:document.documentElement.scrollWidth<=document.documentElement.clientWidth,
    date:document.body.innerText.includes('2026.09.03'), games:document.querySelectorAll('[data-game-card]').length,
    metrics:[...document.querySelectorAll('.metric strong')].map(x=>x.textContent.trim()),
    inactive:[...document.querySelectorAll('.none')].map(x=>x.textContent.trim()),
    text:document.body.innerText,
    metaMono:[...document.querySelectorAll('.status,.venue')].every(x=>getComputedStyle(x).fontFamily.includes('Geist Mono')),
    winnerOrder:[...document.querySelectorAll('[data-game-card]')].every(c=>{const a=c.querySelector('.away .winner'),an=c.querySelector('.away .team-name'),h=c.querySelector('.home .winner'),hn=c.querySelector('.home .team-name');return (!a||a.getBoundingClientRect().right<=an.getBoundingClientRect().left)&&(!h||h.getBoundingClientRect().left>=hn.getBoundingClientRect().right)}),
    numeric:[...document.querySelectorAll('[data-stat-value]')].filter(x=>x.textContent.trim()).every(x=>{const r=document.createRange();r.selectNodeContents(x);return r.getClientRects().length===1})
  }));
  await page.screenshot({path:`.artifacts/kbo-2026-09-03/local-${kind}-${width}.png`,fullPage:true}); output.push({kind,width,errors,...result}); await page.close();
}
await browser.close();
for(const r of output){
  if(!r.overflow||!r.date||r.errors.length||!r.numeric) throw Error(JSON.stringify(r));
  if(r.kind==='integrated'&&(r.games!==4||r.metrics.join('|')!=='4|35|4|2'||!r.winnerOrder||!r.metaMono||!r.text.includes('경기 결과')))throw Error(JSON.stringify(r));
  if(r.kind==='players'&&(r.inactive.filter(x=>x==='등판 없음').length!==7||!r.text.includes('원태인')||!r.text.includes('박영현')))throw Error(JSON.stringify(r));
}
console.log(JSON.stringify(output.map(({text,...r})=>r),null,2));
