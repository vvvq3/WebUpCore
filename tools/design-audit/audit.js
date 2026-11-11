// Аудит вёрстки: десктоп 1440 и телефон 390. Скриншоты + метрики переполнения.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
(async () => {
  const [dir, out] = [process.argv[2], process.argv[3]];
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.html'));
  const b = await chromium.launch();
  const report = {};
  for (const f of files) {
    const name = f.replace('.html', '');
    report[name] = {};
    for (const [label, vp] of [['desktop', { width: 1440, height: 900 }], ['mobile', { width: 390, height: 844 }]]) {
      const ctx = await b.newContext({ viewport: vp, deviceScaleFactor: 1, reducedMotion: 'no-preference' });
      const p = await ctx.newPage();
      await p.goto('file://' + path.join(dir, f), { waitUntil: 'load' });
      await p.waitForTimeout(2500);
      const m = await p.evaluate(() => {
        const W = window.innerWidth;
        const doc = document.documentElement;
        const offenders = [];
        document.querySelectorAll('body *').forEach(el => {
          const r = el.getBoundingClientRect();
          if (r.width === 0 || r.height === 0) return;
          // ищем элементы, выходящие за правый край, у которых родитель не обрезает переполнение
          if (r.right > W + 2 || r.left < -2) {
            let clipped = false; let a = el.parentElement;
            while (a && a !== document.body) { const cs = getComputedStyle(a); if (['hidden', 'auto', 'scroll', 'clip'].includes(cs.overflowX)) { const ar = a.getBoundingClientRect(); if (ar.right <= W + 2) { clipped = true; break; } } a = a.parentElement; }
            if (!clipped) offenders.push({ tag: el.tagName, cls: el.className && el.className.baseVal === undefined ? String(el.className).slice(0, 40) : '', text: (el.innerText || '').slice(0, 40).replace(/\n/g, ' '), right: Math.round(r.right), w: Math.round(r.width) });
          }
        });
        // мелкий текст
        let tiny = 0; const tinySamples = [];
        document.querySelectorAll('body *').forEach(el => {
          if (!el.childNodes.length) return;
          const hasText = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim().length > 2);
          if (!hasText) return;
          const fs = parseFloat(getComputedStyle(el).fontSize);
          let scale = 1; const svg = el.closest('svg');
          if (svg) { const vb = svg.viewBox && svg.viewBox.baseVal; if (vb && vb.width) scale = svg.getBoundingClientRect().width / vb.width; }
          const eff = fs * scale;
          if (eff < 11.5 && el.getBoundingClientRect().width > 0) { tiny++; if (tinySamples.length < 6) tinySamples.push(Math.round(eff * 10) / 10 + 'px «' + el.textContent.trim().slice(0, 24) + '»'); }
        });
        const header = document.querySelector('header');
        const h1 = document.querySelector('h1');
        const smallTargets = [...document.querySelectorAll('a, button')].filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && (r.height < 40) && getComputedStyle(e).display !== 'none'; }).length;
        return { scrollW: doc.scrollWidth, innerW: W, height: doc.scrollHeight, offenders: offenders.slice(0, 8), offendersCount: offenders.length, tiny, tinySamples, headerH: header ? Math.round(header.getBoundingClientRect().height) : 0, h1Size: h1 ? getComputedStyle(h1).fontSize : '', h1Bottom: h1 ? Math.round(h1.getBoundingClientRect().bottom) : 0, smallTargets };
      });
      report[name][label] = m;
      await p.screenshot({ path: path.join(out, `${name}_${label}.png`), fullPage: true });
      await p.screenshot({ path: path.join(out, `${name}_${label}_fold.png`) });
      await ctx.close();
      console.log(name, label, 'h=', m.height, 'overflowX=', m.scrollW > m.innerW, 'offenders=', m.offendersCount, 'tiny=', m.tiny, 'header=', m.headerH);
    }
  }
  fs.writeFileSync(path.join(out, 'report.json'), JSON.stringify(report, null, 1));
  await b.close();
})();
