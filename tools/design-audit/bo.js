// Снимок сайта BlueOptima для анализа стилистики (не для копирования).
const { chromium } = require('playwright');
(async () => {
  const out = process.argv[2];
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  await p.goto('https://www.blueoptima.com/', { waitUntil: 'networkidle', timeout: 90000 }).catch(e => console.log('goto', e.message));
  await p.waitForTimeout(4000);
  for (let i = 0; i < 6; i++) { await p.mouse.wheel(0, i === 0 ? 0 : 900); await p.waitForTimeout(1200); await p.screenshot({ path: `${out}/bo${i}.jpg`, type: 'jpeg', quality: 70 }); }
  const st = await p.evaluate(() => {
    const pick = s => { const e = document.querySelector(s); if (!e) return null; const c = getComputedStyle(e); return { font: c.fontFamily, size: c.fontSize, weight: c.fontWeight, color: c.color, bg: c.backgroundColor }; };
    const cols = {}; document.querySelectorAll('section, div, a, button').forEach(e => { const c = getComputedStyle(e).backgroundColor; if (c !== 'rgba(0, 0, 0, 0)') cols[c] = (cols[c] || 0) + 1; });
    return { h1: pick('h1'), h2: pick('h2'), body: pick('body'), btn: pick('a[class*=button], .button, button'), bgs: Object.entries(cols).sort((a, b) => b[1] - a[1]).slice(0, 12), text: document.body.innerText.slice(0, 1500) };
  });
  console.log(JSON.stringify(st, null, 1));
  await b.close();
})();
