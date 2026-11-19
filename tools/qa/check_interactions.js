// Проверка интерактива: меню на телефоне, форма заявки, фильтр блога, слайдер (высота не прыгает),
// прокрутка при переходе, анимация блока #core. Запуск при работающем `npm run preview`: node tools/qa/check_interactions.js
const { chromium } = require('playwright');
const BASE = process.env.BASE || 'http://localhost:4321';
(async () => {
  const b = await chromium.launch(); const out = []; const errs = [];
  const page = async (w) => { const p = await b.newPage({ viewport: { width: w, height: 844 } }); p.on('pageerror', (e) => errs.push(e.message)); return p; };
  // меню + форма
  let p = await page(390);
  // отправку формы подменяем: тест не должен слать настоящие письма (FormSubmit) и сообщения в Telegram (/api/lead)
  await p.route('https://formsubmit.co/**', (r) => r.fulfill({ status: 200, contentType: 'application/json', body: '{"success":"true"}' }));
  await p.route('**/api/lead', (r) => r.fulfill({ status: 200, contentType: 'application/json', body: '{"ok":true}' }));
  await p.goto(BASE + '/mentor/', { waitUntil: 'networkidle' });
  await p.click('.uc-burger'); out.push(['меню открывается', await p.isVisible('#uc-menu')]);
  await p.click('#uc-menu a[data-form]'); out.push(['форма открывается из меню', await p.isVisible('#uc-lead')]);
  await p.click('[data-lead-submit]'); out.push(['форма проверяет поля', !(await p.isHidden('[data-lead-error]'))]);
  await p.fill('input[name=name]', 'Тест'); await p.fill('input[name=contact]', '@test'); await p.click('[data-lead-submit]');
  await p.waitForSelector('[data-lead-done]:not([hidden])', { timeout: 5000 }).catch(() => {});
  out.push(['форма: экран «готово»', await p.isVisible('[data-lead-done]')]); await p.close();
  // фильтр блога
  p = await page(390); await p.goto(BASE + '/blog/', { waitUntil: 'networkidle' });
  await p.click('[data-filter="ИИ"]'); await p.waitForTimeout(200);
  const cats = await p.evaluate(() => [...document.querySelectorAll('#posts article')].filter((a) => a.offsetParent).map((a) => a.dataset.cat));
  out.push(['фильтр блога: только «ИИ»', cats.length > 0 && cats.every((c) => c === 'ИИ')]);
  await p.click('[data-filter="all"]'); out.push(['фильтр: «Все» возвращает страницы', await p.isVisible('[data-blog-paged]')]);
  // прокрутка при переходе
  await p.evaluate(() => window.scrollTo(0, 2000)); await p.click('.uc-burger'); await p.click('#uc-menu .uc-menu__product >> nth=1');
  await p.waitForLoadState('load'); await p.waitForTimeout(300); out.push(['переход из меню — страница сверху', (await p.evaluate(() => scrollY)) === 0]); await p.close();
  // слайдер
  for (const w of [390, 1440]) {
    p = await page(w); await p.goto(BASE + '/', { waitUntil: 'networkidle' }); const hs = new Set(); await p.evaluate(() => document.querySelector('[data-slider]').scrollIntoView({ block: 'center' }));
    for (let i = 0; i < 6; i++) { await p.waitForTimeout(1000); hs.add(await p.evaluate(() => Math.round(document.querySelector('[data-slider]').getBoundingClientRect().height))); }
    const nums = new Set(); for (let i = 0; i < 4; i++) { nums.add(await p.evaluate(() => document.querySelector('[data-slide-num]').textContent)); await p.waitForTimeout(1000); } out.push([`слайдер ${w}px: экраны сменяются сами`, nums.size >= 2]);
    out.push([`слайдер ${w}px: высота постоянна`, hs.size === 1]); await p.close();
  }
  // анимация #core
  p = await page(390); await p.goto(BASE + '/', { waitUntil: 'networkidle' });
  await p.evaluate(() => document.querySelector('#core svg').scrollIntoView({ block: 'center' })); await p.waitForTimeout(5000);
  out.push(['#core: в конце 80 из 160', (await p.evaluate(() => document.querySelector('#core svg text').textContent)) === '80']); await p.close();
  // раунд 81: мгновенный прыжок в конец (End / #якорь) — блоки и цифры в экране видны; «Контакты» показывают блок контактов
  for (const u of ['/', '/ai/', '/projects/', '/en/']) {
    p = await page(1440); await p.goto(BASE + u, { waitUntil: 'networkidle' });
    await p.evaluate(() => { document.documentElement.style.scrollBehavior = 'auto'; window.scrollTo(0, document.documentElement.scrollHeight); }); await p.waitForTimeout(1200);
    const hid = await p.evaluate(() => [...document.querySelectorAll('.uc-reveal, [data-odo]')].filter((e) => { const r = e.getBoundingClientRect(); return r.top < innerHeight && r.bottom > 0 && (getComputedStyle(e).opacity === '0' || (e.hasAttribute('data-odo') && !e.classList.contains('uc-on'))); }).length);
    out.push([`прыжок в конец ${u}: всё видно`, hid === 0]); await p.close();
  }
  for (const w of [390, 1440]) {
    p = await page(w); await p.goto(BASE + '/', { waitUntil: 'networkidle' }); await p.waitForTimeout(1500);
    const z = await p.evaluate(() => [...document.querySelectorAll('[data-odo]')].filter((e) => { const r = e.getBoundingClientRect(); return r.top < innerHeight && r.bottom > 0 && !e.classList.contains('uc-on'); }).length);
    out.push([`цифры первого экрана ${w}px: крутятся сразу`, z === 0]);
    await p.click('[data-form]:visible >> nth=0'); await p.waitForTimeout(400);
    const c = await p.evaluate(() => { const r = document.getElementById('uc-lead').getBoundingClientRect(); return Math.abs(r.left + r.width / 2 - innerWidth / 2) < 2 && Math.abs(r.top + r.height / 2 - innerHeight / 2) < 2; });
    out.push([`форма заявки ${w}px: по центру`, c]); await p.close();
  }
  out.forEach(([n, ok]) => console.log(ok ? '✓' : '✗', n));
  console.log('ошибки JS:', errs.length ? errs.join(' | ') : 'нет');
  await b.close(); process.exit(out.every(([, ok]) => ok) && !errs.length ? 0 : 1);
})();
