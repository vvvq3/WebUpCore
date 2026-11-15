// Проверка вёрстки всех страниц (RU + EN) на 7 ширинах: выход за край, обрезанный текст, один h1, картинки, ошибки JS/404,
// маленькие кнопки, alt, битые внутренние ссылки. Запуск: cd site && npm run build && npm run preview, затем
// node tools/qa/check_layout.js   (BASE=http://адрес — другой сервер). Нужен Playwright с Chromium.
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const DIST=require('path').resolve(__dirname,'..','..','site','dist');
const BASE=process.env.BASE||'http://localhost:4321';
const pages=['/','/grade/','/ai/','/projects/','/mentor/','/blog/','/blog/2/','/blog/3/'];const all=[...pages,...pages.map(p=>'/en'+p),'/old/'];
const widths=[360,390,768,1024,1200,1440,1920];
(async()=>{const b=await chromium.launch();const issues=[];const linkSet=new Set();
for(const pth of all){for(const w of widths){
  const p=await b.newPage({viewport:{width:w,height:900}});const errs=[];
  p.on('pageerror',e=>errs.push('JS:'+e.message));p.on('response',r=>{if(r.status()>=400&&r.url().startsWith(BASE))errs.push(r.status()+':'+r.url())});
  await p.goto(BASE+pth,{waitUntil:'networkidle'});
  await p.evaluate(()=>document.querySelectorAll('.uc-reveal,.uc-bar').forEach(e=>e.classList.add('uc-on')));await p.waitForTimeout(150);
  const r=await p.evaluate((w)=>{
    const out={};out.sw=document.documentElement.scrollWidth;
    const over=[];for(const el of document.querySelectorAll('body *')){const cs=getComputedStyle(el);if(cs.display=='none'||cs.visibility=='hidden'||el.closest('[hidden]')||el.closest('dialog:not([open])'))continue;const rc=el.getBoundingClientRect();if(!rc.width)continue;
      let clip=false,a=el.parentElement;while(a&&a!==document.body){const s=getComputedStyle(a);if(s.overflowX!='visible'&&a.getBoundingClientRect().right<=w+1){clip=true;break}a=a.parentElement}
      if(!clip&&(rc.right>w+1||rc.left<-1))over.push(el.tagName+':'+(el.textContent||'').trim().slice(0,25))}
    out.over=over.slice(0,4);
    const clipped=[];for(const el of document.querySelectorAll('main *')){if(el.children.length)continue;const cs=getComputedStyle(el);if(cs.textOverflow=='ellipsis'||el.closest('.uc-slide-cap')||el.closest('.uc-odo')||el.classList.contains('uc-sr'))continue;if(el.scrollWidth>el.clientWidth+2&&el.clientWidth>0&&cs.overflow!='visible')clipped.push((el.textContent||'').trim().slice(0,25));
      if(cs.overflow=='visible'&&el.scrollWidth>el.clientWidth+3&&el.clientWidth>0&&cs.display!='inline'&&!el.closest('svg'))clipped.push('spill:'+(el.textContent||'').trim().slice(0,25));}
    out.clipped=[...new Set(clipped)].slice(0,4);
    out.h1=document.querySelectorAll('h1').length;
    out.imgs=[...document.images].filter(i=>!i.complete||(!i.naturalWidth&&i.loading!='lazy')).map(i=>i.src.slice(-30));
    const hdr=document.querySelector('.uc-site-header');out.hdr=hdr?Math.round(hdr.getBoundingClientRect().height):0;
    const small=[...document.querySelectorAll('main a, main button, header a, header button')].filter(e=>{const r=e.getBoundingClientRect();const cs=getComputedStyle(e);return r.width&&cs.visibility!='hidden'&&(r.height<32)&&!e.closest('p')&&!e.closest('[class*=uc-tg-p]')}).map(e=>(e.textContent||e.getAttribute('aria-label')||'').trim().slice(0,20));
    out.small=small.slice(0,4);
    out.links=[...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href'));
    out.noalt=[...document.images].filter(i=>!i.hasAttribute('alt')).length;
    return out},w);
  r.links.forEach(l=>linkSet.add(l));delete r.links;
  const bad=r.sw>w||r.over.length||r.clipped.length||r.h1!==1||r.imgs.length||errs.length||r.small.length||r.noalt;
  if(bad)issues.push(pth+' '+w+' '+JSON.stringify(r)+' '+errs.join(';'));
  await p.close();}}
// links
const broken=[];for(const l of linkSet){if(!l.startsWith('/'))continue;const [u]=l.split('#');if(!u)continue;const f=path.join(DIST,u.endsWith('/')?u+'index.html':u);if(!fs.existsSync(f))broken.push(l)}
console.log('проверено страниц×ширин:',all.length*widths.length);console.log('ссылок внутренних:',[...linkSet].filter(l=>l.startsWith('/')).length,'битых:',broken.join(' ')||0);
console.log('внешние:',[...linkSet].filter(l=>/^https?:/.test(l)).join(' '));
console.log('проблем:',issues.length);issues.slice(0,40).forEach(i=>console.log(i));
await b.close();})();
