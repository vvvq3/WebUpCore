// Презентации UpCore v2 (раунд 97): слайды собираются из НАСТОЯЩИХ блоков сайта (site/dist) —
// те же стили, шрифты и тексты, без кнопок и ссылок. Для каждой из 5 презентаций — 3 версии по 8–10 слайдов:
//   5 «По сайту»       — блоки страницы продукта в порядке сайта;
//   6 «С демо»         — те же блоки + крупные скриншоты демо (подписи — как в слайдере на сайте);
//   7 «С платформой»   — блоки продукта + блоки платформы с главной (4 продукта, модель, экономика).
// Запуск: cd site && npm run build (если сайт менялся), затем  node tools/decks2/build.js [фильтр]
// Результат: docs/decks/<NN-продукт>/UpCore-<Продукт>-<5|6|7>-<вариант>.pdf + превью в tools/decks2/build/png/.
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const R = require('./recipes.js');

const ROOT = path.resolve(__dirname, '..', '..');
const DIST = path.join(ROOT, 'site', 'dist');
const OUT = path.join(ROOT, 'docs', 'decks');
const PNG = path.join(__dirname, 'build', 'png');
const PORT = 4399;
const filter = process.argv.slice(2).find(a => !a.startsWith('--')) || '';
const previews = !process.argv.includes('--no-png');

function serve() {
  const srv = spawn('python3', ['-m', 'http.server', String(PORT), '--bind', '127.0.0.1'], { cwd: DIST, stdio: 'ignore' });
  return new Promise(res => setTimeout(() => res(srv), 800));
}

// --- выполняется в браузере: собрать слайды по рецепту
async function assemble(deck) {
  const PAGES = { home: '/', grade: '/grade/', ai: '/ai/', projects: '/projects/', mentor: '/mentor/' };
  const docs = {};
  for (const [k, u] of Object.entries(PAGES)) docs[k] = new DOMParser().parseFromString(await (await fetch(u)).text(), 'text/html');
  const home = docs.home;
  document.documentElement.classList.remove('uc-js');
  // стили и шрифты сайта
  document.head.querySelectorAll('style, link[rel=stylesheet]').forEach(n => n.remove());
  home.head.querySelectorAll('style, link[rel=stylesheet], link[rel=preload]').forEach(n => document.head.appendChild(document.importNode(n, true)));
  const st = document.createElement('style');
  st.textContent = `
    @page { size: 1920px 1080px; margin: 0; }
    html, body { margin: 0 !important; padding: 0 !important; background: #0D0C15; }
    body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    .dk-slide { width: 1920px; height: 1080px; overflow: hidden; position: relative; break-after: page; page-break-after: always; background: #0D0C15; }
    .dk { zoom: 1.3333333; width: 1440px; height: 810px; position: relative; overflow: hidden; color: #FFFFFF; }
    .dk-area { position: absolute; left: 64px; right: 64px; top: 44px; bottom: 76px; display: flex; flex-direction: column; justify-content: center; }
    .dk-fit { width: 100%; }
    .dk-fit > section { max-width: none !important; margin: 0 !important; padding: 0 !important; }
    .dk-foot { position: absolute; left: 64px; right: 64px; bottom: 0; height: 56px; display: flex; align-items: center; justify-content: space-between; gap: 24px;
      border-top: 1px solid rgba(255,255,255,0.08); font-size: 13px; color: rgba(255,255,255,0.6); font-family: 'Onest Variable', sans-serif; }
    .dk-foot img { height: 18px; width: auto; display: block; }
    .dk-foot .n { font-family: 'JetBrains Mono Variable', monospace; color: rgba(255,255,255,0.5); }
    .dk-chev { position: absolute; right: -120px; top: -40px; width: 560px; height: auto; opacity: 0.14; filter: blur(2px); pointer-events: none; }
    .dk-cover .dk-area, .dk-cta .dk-area { justify-content: center; }
    .uc-scan, [data-slide-play], .uc-chip { display: none !important; }
    .uc-reveal { opacity: 1 !important; transform: none !important; }
  `;
  document.head.appendChild(st);
  const CHEV = '<svg class="dk-chev" viewBox="0 0 375 645" aria-hidden="true"><path fill="#63D5FF" d="M340.243 410.873C322.404 436.777 298.363 465.078 268.118 495.774L166.429 598.984C149.417 616.251 135.926 628.481 125.958 635.674C116.005 643.826 105.711 645.5 95.078 640.695C84.4595 636.849 69.8902 625.803 51.3702 607.556L9.90889 566.705L249.7 322.254L0.000749597 79.9674L43.9849 35.3256C61.4698 17.5791 75.6986 6.54952 86.6712 2.23669C96.6839 -2.07669 106.793 -0.151217 116.998 8.01309C126.716 15.6972 140.347 28.1827 157.893 45.4695L271.54 157.442C294.446 180.011 314.443 200.659 331.531 219.385C348.146 238.591 359.968 258.274 366.999 278.434C373.542 298.114 374.78 322.343 370.134 347.567C365.05 375.17 358.57 385.448 340.243 410.873Z"/></svg>';
  const footText = (home.querySelector('footer span') || {}).textContent || '';

  const byPath = (root, p) => p.split('>').reduce((el, i) => el && el.children[+i], root);
  const section = (page, which) => {
    const d = docs[page];
    const secs = [...d.querySelectorAll('main section')];
    const s = typeof which === 'number' ? secs[which] : d.getElementById(which);
    if (!s) throw new Error('нет блока ' + page + ' ' + which);
    return document.importNode(s, true);
  };
  const smallestWithText = (root, t) => {
    let best = null;
    root.querySelectorAll('*').forEach(el => { if ((el.textContent || '').trim().startsWith(t) && (!best || best.contains(el))) best = el; });
    return best;
  };
  function applyOps(s, o) {
    // пути считаются по исходной структуре: сначала находим все узлы, потом удаляем
    const styled = (o.cssPath || []).map(([p, css]) => [byPath(s, p), css]);
    const kill = [];
    (o.rm || []).forEach(p => { const el = byPath(s, p); if (!el) throw new Error('нет пути ' + p); kill.push(el); });
    (o.hide || []).forEach(sel => s.querySelectorAll(sel).forEach(el => kill.push(el)));
    (o.hideText || []).forEach(t => { const el = smallestWithText(s, t); if (!el) throw new Error('нет текста ' + t); kill.push(el); });
    kill.forEach(el => el.remove());
    Object.entries(o.css || {}).forEach(([sel, css]) => (sel === ':scope' ? [s] : s.querySelectorAll(sel)).forEach(el => { el.style.cssText += ';' + css; }));
    styled.forEach(([el, css]) => { if (el) el.style.cssText += ';' + css; });
  }
  // всегда убираем: кнопки, «Подробнее …», переключатели
  const ALWAYS = { hide: ['.uc-btns', 'button', '.uc-btn', 'a.uc-btn'] };

  function screenFrame(file, num, key, h) {
    return `<div style="border-radius: 24px; background: #12111C; border: 1px solid rgba(99,213,255,0.3); box-shadow: 0 0 0 1px rgba(99,213,255,0.06), 0 40px 120px rgba(99,213,255,0.12); overflow: hidden;">
      <div style="display: flex; justify-content: space-between; gap: 12px; padding: 14px 18px; border-bottom: 1px solid rgba(255,255,255,0.08); font-family: 'JetBrains Mono Variable', monospace; font-size: 13px; color: rgba(255,255,255,0.72);">
      <span>upcore://screens / ${key}</span><span style="color: #63D5FF;">${num} / 14</span></div>
      <div style="position: relative; ${h ? 'height: ' + h + 'px;' : 'aspect-ratio: 2 / 1;'} background: #FFFFFF; overflow: hidden;"><img src="/img/screens/v2/${file}" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: top left; display: block;"></div></div>`;
  }

  const slides = [];
  for (const sd of deck.slides) {
    let node, cls = '';
    if (sd.shot) {
      const [key, title, cap, file] = sd.shot;
      const num = String(sd.num).padStart(2, '0');
      node = document.createElement('section');
      node.innerHTML = `<div style="font-family: 'JetBrains Mono Variable', monospace; font-size: 13px; color: ${deck.acc}; margin-bottom: 14px; letter-spacing: 0.04em;">ДЕМО UPCORE · ${key.toUpperCase()}</div>
        <div style="display: flex; justify-content: space-between; align-items: flex-end; gap: 24px; margin-bottom: 28px;"><h2 style="margin: 0; font-size: 46px; letter-spacing: -0.03em; line-height: 1.05; font-weight: 800;">${title}</h2>
        <p style="margin: 0; max-width: 460px; color: rgba(255,255,255,0.74); font-size: 17px; line-height: 1.55; text-align: right;">${cap}</p></div>` + screenFrame(file.replace('.png', '.webp'), num, key, 560);
    } else if (sd.html) {
      node = document.createElement('section');
      node.innerHTML = sd.html;
    } else {
      node = section(sd.p, sd.s);
      applyOps(node, ALWAYS);
      node.style.minHeight = '0';
      [...node.children].filter(c => c.tagName.toLowerCase() === 'svg' && (c.getAttribute('style') || '').includes('absolute')).forEach(c => c.remove());
      applyOps(node, sd);
      if (sd.p !== 'home' && sd.s === 'top') cls = 'dk-cover';
      if (sd.p === 'home' && sd.s === 'top') {
        cls = 'dk-cover';
        const sl = node.querySelector('[data-slider]');
        if (sl) {
          const [key, , , file] = sd.coverShot;
          const num = String(sd.coverNum).padStart(2, '0');
          sl.querySelectorAll('img[data-slide]').forEach(im => { im.style.visibility = im.getAttribute('src').endsWith(file.replace('.png', '.webp')) ? 'visible' : 'hidden'; im.loading = 'eager'; });
          const k = sl.querySelector('[data-slide-key]'); if (k) k.textContent = key;
          const n = sl.querySelector('[data-slide-num]'); if (n) n.textContent = num;
        }
      }
      if (sd.s === 'contacts') cls = 'dk-cta';
    }
    slides.push({ node, cls, chev: !!sd.chev || cls === 'dk-cover' || cls === 'dk-cta', minZoom: sd.minZoom || 0.72, maxZoom: sd.maxZoom || (sd.shot ? 1 : (sd.s === 'contacts' ? 1.3 : (sd.s === 'top' ? 1.12 : 1.32))) });
  }
  document.body.innerHTML = '<main></main>';
  const main = document.body.firstChild;
  slides.forEach((s, i) => {
    const wrap = document.createElement('div'); wrap.className = 'dk-slide';
    wrap.innerHTML = `<div class="dk ${s.cls}">${s.chev ? CHEV : ''}<div class="dk-area"><div class="dk-fit"></div></div>
      <div class="dk-foot"><img src="/img/logo.svg" alt="UpCore"><span>${footText}</span><span class="n">${String(i + 1).padStart(2, '0')} / ${String(slides.length).padStart(2, '0')}</span></div></div>`;
    wrap.querySelector('.dk-fit').appendChild(s.node);
    main.appendChild(wrap);
  });
  // ждём картинки и шрифты
  await Promise.all([...document.images].map(im => im.complete ? 0 : new Promise(r => { im.onload = im.onerror = r; })));
  await document.fonts.ready;
  // вписываем каждый блок в поле слайда
  const report = [];
  document.querySelectorAll('.dk-slide').forEach((w, i) => {
    const area = w.querySelector('.dk-area'), fit = w.querySelector('.dk-fit');
    const ah = area.clientHeight, fh = fit.scrollHeight;
    const lo = slides[i].minZoom, hi = slides[i].maxZoom;
    // подбираем масштаб: самый крупный из [lo..hi], при котором блок помещается по высоте;
    // ширина раскладки = ширина поля / масштаб — композиция сайта сохраняется
    const aw = area.clientWidth;
    const setZ = z => { fit.style.zoom = z; fit.style.width = (aw / z) + 'px'; return fit.getBoundingClientRect().height / 1.3333333; };
    let z = lo;
    for (let c = hi; c >= lo - 1e-6; c -= 0.02) { if (setZ(c) <= ah) { z = c; break; } }
    setZ(z);
    const over = Math.round(fit.getBoundingClientRect().height / 1.3333333 - ah);
    report.push({ i: i + 1, h: fh, z: +z.toFixed(2), over: over > 2 ? over : 0 });
  });
  return report;
}

(async () => {
  const srv = await serve();
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.emulateMedia({ media: 'screen' });
  let problems = 0;
  try {
    for (const deck of R.decks()) {
      if (filter && !deck.name.includes(filter)) continue;
      await page.goto(`http://127.0.0.1:${PORT}/404.html`);
      const rep = await page.evaluate(assemble, deck);
      await page.waitForTimeout(300);
      const bad = rep.filter(r => r.over || r.z < 0.85);
      const dir = path.join(OUT, deck.folder);
      fs.mkdirSync(dir, { recursive: true });
      await page.pdf({ path: path.join(dir, deck.name + '.pdf'), width: '1920px', height: '1080px', printBackground: true, preferCSSPageSize: true });
      if (previews) {
        const pd = path.join(PNG, deck.name); fs.rmSync(pd, { recursive: true, force: true }); fs.mkdirSync(pd, { recursive: true });
        require('child_process').execFileSync('pdftoppm', ['-r', '64', '-png', path.join(dir, deck.name + '.pdf'), path.join(pd, 's')], { stdio: 'ignore' });
      }
      const kb = Math.round(fs.statSync(path.join(dir, deck.name + '.pdf')).size / 1024);
      console.log(bad.some(r => r.over) ? '✗' : '✓', deck.name, rep.length + ' сл.', kb + ' KB', bad.length ? JSON.stringify(bad) : '');
      problems += bad.filter(r => r.over).length;
    }
  } finally { await browser.close(); srv.kill(); }
  console.log(problems ? 'Переполнений: ' + problems : 'Переполнений нет');
})();
