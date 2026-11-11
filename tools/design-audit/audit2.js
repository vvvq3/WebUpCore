// Повторный замер на 390px без overflow:hidden у корня — что реально вылезает за экран.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
(async () => {
  const dir = process.argv[2];
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.html'));
  const b = await chromium.launch();
  const res = {};
  for (const f of files) {
    const ctx = await b.newContext({ viewport: { width: 390, height: 844 } });
    const p = await ctx.newPage();
    await p.goto('file://' + path.join(dir, f), { waitUntil: 'load' });
    await p.waitForTimeout(1500);
    res[f] = await p.evaluate(() => {
      const root = document.body.firstElementChild;
      root.style.overflow = 'visible';
      const W = window.innerWidth;
      const out = [];
      document.querySelectorAll('body *').forEach(el => {
        const r = el.getBoundingClientRect();
        if (!r.width || !r.height) return;
        if (r.right > W + 4) {
          let a = el.parentElement, clipped = false;
          while (a && a !== root) { const cs = getComputedStyle(a); if (['hidden', 'auto', 'scroll', 'clip'].includes(cs.overflowX) && a.getBoundingClientRect().right <= W + 4) { clipped = true; break; } a = a.parentElement; }
          if (!clipped) out.push({ tag: el.tagName, text: (el.innerText || el.getAttribute('aria-label') || '').slice(0, 50).replace(/\s+/g, ' '), right: Math.round(r.right), y: Math.round(r.top + scrollY) });
        }
      });
      // оставляем только «верхние» нарушители (у которых родитель не нарушает)
      const top = out.filter((o, i) => i === 0 || o.y !== out[i - 1].y || o.right !== out[i - 1].right).slice(0, 12);
      return { scrollW: document.documentElement.scrollWidth, count: out.length, top };
    });
    await ctx.close();
    console.log(f, 'scrollW=', res[f].scrollW, 'count=', res[f].count);
    res[f].top.slice(0, 5).forEach(o => console.log('   ', o.tag, o.right + 'px', 'y=' + o.y, o.text));
  }
  fs.writeFileSync(path.join(dir, '..', 'overflow.json'), JSON.stringify(res, null, 1));
  await b.close();
})();
