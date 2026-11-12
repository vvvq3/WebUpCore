// Замер высоты превью на 1440 px и проверка переполнения на 390 px. node measure.js <preview_dir> → печать + heights.json
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const dir = process.argv[2];
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.html')).sort();
  const b = await chromium.launch();
  const H = {};
  for (const f of files) {
    const out = {};
    for (const w of [1440, 390]) {
      const p = await b.newPage({ viewport: { width: w, height: 900 } });
      await p.goto('file://' + path.join(dir, f), { waitUntil: 'load' });
      await p.waitForTimeout(400);
      out[w] = await p.evaluate((W) => {
        const root = document.body.firstElementChild;
        root.style.overflow = 'visible';
        const bad = [];
        document.querySelectorAll('body *').forEach(el => { const r = el.getBoundingClientRect(); if (r.width && r.right > W + 2 && !el.closest('svg')) bad.push(el.tagName + ':' + (el.innerText||'').slice(0,30).replace(/\s+/g,' ') + '@' + Math.round(r.right)); });
        let small = 0; document.querySelectorAll('body *').forEach(el => { if ([...el.childNodes].some(n => n.nodeType===3 && n.textContent.trim())) { if (parseFloat(getComputedStyle(el).fontSize) < 12) small++; } });
        const fn = location.pathname.split('/').pop();
        const blk = fn.startsWith('Core-') ? document.querySelector('#core') : fn.startsWith('Pains-') ? document.querySelector('#pains') : null;
        const hh = blk ? Math.ceil(blk.getBoundingClientRect().bottom + scrollY) : document.documentElement.scrollHeight;
        return { h: hh, bad: bad.slice(0, 4), nbad: bad.length, small };
      }, w);
      await p.close();
    }
    H[f.replace('.html','')] = out[1440].h;
    console.log(f.padEnd(16), 'h1440=' + out[1440].h, 'h390=' + out[390].h, 'over1440=' + out[1440].nbad, 'over390=' + out[390].nbad, out[390].bad.join(' | '), 'small=' + out[390].small);
  }
  fs.writeFileSync(path.join(__dirname, 'heights.json'), JSON.stringify(H, null, 1));
  await b.close();
})();
