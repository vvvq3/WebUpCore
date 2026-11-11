// Кадровая запись тизера по демо UpCore: снимаем кадры только когда страница готова,
// плавная прокрутка детерминирована по кадрам. Потом ffmpeg собирает mp4.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const EMP = '/employeeDashboard?user=ab59515a-2092-4aab-91f2-5c78be0534c4&name=%D0%9B%D1%83%D0%BA%D1%8C%D1%8F%D0%BD%D0%BE%D0%B2+%D0%90%D0%BB%D0%B5%D0%BA%D1%81%D0%B0%D0%BD%D0%B4%D1%80&project=bad8eb0d-36df-46ed-8bb9-99ba0b1f1122&projectName=UpCore+Backend&date=2026-10-11';
const TRAIN = '/training?user=ab59515a-2092-4aab-91f2-5c78be0534c4&name=%D0%9B%D1%83%D0%BA%D1%8C%D1%8F%D0%BD%D0%BE%D0%B2+%D0%90%D0%BB%D0%B5%D0%BA%D1%81%D0%B0%D0%BD%D0%B4%D1%80&project=bad8eb0d-36df-46ed-8bb9-99ba0b1f1122&date=2026-10-11';
const PROJ = '/projectReport?project=bad8eb0d-36df-46ed-8bb9-99ba0b1f1122&name=UpCore+Backend&date=2026-10-11';
const MR = '/mergeRequestsShortPagination?vcsProjectId=1048&mergeRequestNumber=2627';

(async () => {
  const out = process.argv[2];
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1, locale: 'ru-RU' });
  await ctx.route('**/*', async route => {
    for (let i = 0; i < 6; i++) {
      try { const r = await route.fetch(); if (r.status() >= 500) { await new Promise(x => setTimeout(x, 500 * (i + 1))); continue; } return route.fulfill({ response: r }); }
      catch (e) { await new Promise(x => setTimeout(x, 500 * (i + 1))); }
    }
    return route.abort();
  });
  const p = await ctx.newPage();
  let n = 0; const scenes = [];
  const clean = () => p.evaluate(() => document.querySelectorAll('.Toastify').forEach(e => e.remove()));
  const frame = async () => { await p.screenshot({ path: path.join(out, `f${String(n++).padStart(5, '0')}.jpg`), type: 'jpeg', quality: 82 }); };
  const hold = async (k) => { for (let i = 0; i < k; i++) await frame(); };
  const scroll = async (k, step) => {
    for (let i = 0; i < k; i++) {
      await p.evaluate((s) => {
        const cands = [document.scrollingElement, ...document.querySelectorAll('main, div')].filter(e => e && e.scrollHeight - e.clientHeight > 50 && (e === document.scrollingElement || ['auto', 'scroll'].includes(getComputedStyle(e).overflowY)));
        cands.sort((a, b) => (b.scrollHeight - b.clientHeight) - (a.scrollHeight - a.clientHeight));
        const el = cands[0] || document.scrollingElement; el.scrollTop += s;
      }, step);
      await p.waitForTimeout(30);
      await frame();
    }
  };
  const go = async (url) => { await p.goto('https://demo.up-core.ru' + url, { waitUntil: 'networkidle', timeout: 90000 }).catch(() => {}); await p.waitForTimeout(5000); await clean(); };
  const tab = async (name) => { await p.getByRole('tab', { name, exact: true }).click(); await p.waitForTimeout(6000); await clean(); };
  const mark = (name) => scenes.push({ name, start: n });

  await go(TRAIN); mark('star'); await hold(30); await scroll(36, 14); await hold(8);
  await go('/organizationReport'); mark('company'); await hold(30); await scroll(24, 14); await hold(6);
  await go(EMP); mark('efficiency'); await hold(26);
  await tab('Качество'); mark('quality'); await hold(14); await scroll(34, 16); await hold(6);
  await tab('Табель'); mark('timesheet'); await hold(10); await scroll(40, 18); await hold(6);
  await go('/developerRating'); mark('rating'); await hold(22); await scroll(26, 16); await hold(6);
  await go(PROJ); await tab('Технологии'); mark('techmap'); await hold(18); await scroll(24, 16); await hold(6);
  await go(MR); mark('eye'); await hold(24); await scroll(20, 14); await hold(10);
  fs.writeFileSync(path.join(out, 'scenes.json'), JSON.stringify({ total: n, scenes }, null, 1));
  console.log('frames', n, JSON.stringify(scenes));
  await b.close();
})();
