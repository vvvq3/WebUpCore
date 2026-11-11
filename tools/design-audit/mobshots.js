// Мобильные кадры (390×844, ×2) для артборда «Мобильные версии»: первый экран и блок продуктов.
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [dir, out] = [process.argv[2], process.argv[3]];
  const b = await chromium.launch();
  for (const name of ['Top1-Video', 'Top2-Light', 'Top3-Bays']) {
    const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
    const p = await ctx.newPage();
    await p.goto('file://' + path.join(dir, name + '.html'), { waitUntil: 'load' });
    await p.waitForTimeout(3500);
    await p.screenshot({ path: path.join(out, `${name}-m1.jpg`), type: 'jpeg', quality: 82 });
    await p.evaluate(() => { const el = document.getElementById('grade'); window.scrollTo(0, el.getBoundingClientRect().top + scrollY - 8); });
    await p.waitForTimeout(3500);
    await p.screenshot({ path: path.join(out, `${name}-m2.jpg`), type: 'jpeg', quality: 82 });
    await p.evaluate(() => { const el = document.getElementById('enterprise'); window.scrollTo(0, el.getBoundingClientRect().top + scrollY - 8); });
    await p.waitForTimeout(800);
    await p.screenshot({ path: path.join(out, `${name}-m3.jpg`), type: 'jpeg', quality: 82 });
    await ctx.close();
    console.log('ok', name);
  }
  await b.close();
})();
