// HTML-презентации (tools/decks/build/*.html) → PDF 1920×1080 в docs/decks/<папка>/,
// проверка переполнения каждого слайда и PNG-превью (tools/decks/build/png/).
// node tools/decks/render.js [фильтр-подстрока]
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const HERE = __dirname;
const ROOT = path.resolve(HERE, '..', '..');
const BUILD = path.join(HERE, 'build');
const OUT = path.join(ROOT, 'docs', 'decks');
const filter = process.argv.slice(2).find(a => !a.startsWith('--')) || '';
const previews = !process.argv.includes('--no-png');

(async () => {
  const list = fs.readFileSync(path.join(BUILD, 'manifest.txt'), 'utf8').trim().split('\n').map(l => l.split(' '));
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  let problems = 0;
  for (const [folder, name] of list) {
    if (filter && !name.includes(filter)) continue;
    await page.goto('file://' + path.join(BUILD, name + '.html'));
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(150);
    const issues = await page.evaluate(() => {
      const out = [];
      document.querySelectorAll('.slide').forEach((s, i) => {
        const c = s.querySelector('.content');
        const cb = c.getBoundingClientRect();
        if (c.scrollHeight > c.clientHeight + 2) out.push(`слайд ${i + 1}: контент выше блока на ${c.scrollHeight - c.clientHeight}px`);
        s.querySelectorAll('.content *').forEach(el => {
          const r = el.getBoundingClientRect();
          if (!r.width || !r.height) return;
          const pr = el.parentElement.getBoundingClientRect();
          const parentOut = el.parentElement !== c && (pr.bottom > cb.bottom + 2 || pr.right > cb.right + 2);
          if (!parentOut && (r.bottom > cb.bottom + 2 || r.right > cb.right + 2 || r.left < cb.left - 2)) {
            out.push(`слайд ${i + 1}: <${el.tagName.toLowerCase()} class="${el.className}"> выходит за поле (${Math.round(r.right - cb.right)}/${Math.round(r.bottom - cb.bottom)})`);
          }
          if (el.classList.contains('card') && el.scrollHeight > el.clientHeight + 2) out.push(`слайд ${i + 1}: переполнена карточка «${(el.innerText || '').slice(0, 40)}»`);
        });
      });
      return [...new Set(out)].slice(0, 12);
    });
    if (issues.length) { problems += issues.length; console.log('✗', name); issues.forEach(x => console.log('   ', x)); }
    const dir = path.join(OUT, folder);
    fs.mkdirSync(dir, { recursive: true });
    await page.pdf({ path: path.join(dir, name + '.pdf'), width: '1920px', height: '1080px', printBackground: true, preferCSSPageSize: true });
    if (previews) {
      const pdir = path.join(BUILD, 'png', name);
      fs.mkdirSync(pdir, { recursive: true });
      const slides = await page.$$('.slide');
      for (let i = 0; i < slides.length; i++) await slides[i].screenshot({ path: path.join(pdir, String(i + 1).padStart(2, '0') + '.png') });
    }
    const kb = Math.round(fs.statSync(path.join(dir, name + '.pdf')).size / 1024);
    console.log(issues.length ? ' ' : '✓', name, kb + ' KB');
  }
  await browser.close();
  console.log(problems ? `Проблем: ${problems}` : 'Переполнений нет');
})();
