// Картинки-превью для соцсетей и мессенджеров (Open Graph, 1200×630): site/public/og/<lang>-<page>.png
// node tools/content/og_images.js   (нужен Playwright с Chromium)
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const ROOT = path.resolve(__dirname, '..', '..');
const OUT = path.join(ROOT, 'site', 'public', 'og');
fs.mkdirSync(OUT, { recursive: true });
const logo = 'data:image/svg+xml;base64,' + fs.readFileSync(path.join(ROOT, 'docs/brand/logo.svg')).toString('base64');
const fontDir = path.join(ROOT, 'site/node_modules/@fontsource-variable');
const font = (pkg, file) => 'data:font/woff2;base64,' + fs.readFileSync(path.join(fontDir, pkg, 'files', file)).toString('base64');
const C = { home: '#63D5FF', blog: '#63D5FF', grade: '#63D5FF', ai: '#B9AEFF', projects: '#F2C14E', mentor: '#7FDB7A' };
const P = {
  ru: {
    home: ['ЦИФРОВОЙ ТИМЛИД', 'Оценка эффективности разработки по коду', '96% совпадения с экспертной оценкой · 50+ факторов · без тайм-трекеров'],
    grade: ['> UpCore.Grade', 'Грейд и рейтинг разработчиков по коду', '50+ факторов · каждый фактор — до строчки кода'],
    ai: ['> UpCore.AI', 'Эффективность ИИ и вайбкодинга в часах и деньгах', 'Автодетект ИИ-кода 92%+ · нормы токенов · промпт-ревью'],
    projects: ['> UpCore.Projects', 'Аудит подрядчика и бюджета проекта по коду', 'Акт 1 500 ч → 860 ч по коду · техдолг ISO 25010'],
    mentor: ['> UpCore.Mentor', 'ИИ-наставник для каждого разработчика', 'Качество кода 3,2 → 8,0 · план роста по 50+ факторам'],
    blog: ['БЛОГ UPCORE', 'Об эффективности разработки — без воды', 'Канал «ИИ-тимлид UpCore» · Иван Гель'],
  },
  en: {
    home: ['DIGITAL TEAM LEAD', 'Engineering efficiency measured from code', '96% agreement with expert assessment · 50+ factors · no time trackers'],
    grade: ['> UpCore.Grade', 'Developer grades and ranking from code', '50+ factors · every factor drills down to the line of code'],
    ai: ['> UpCore.AI', 'The real impact of AI and vibe coding', 'AI-code detection 92%+ · token norms · prompt review'],
    projects: ['> UpCore.Projects', 'Audit vendors and project budgets from code', 'Invoice 1,500 h → 860 h from code · ISO 25010 tech debt'],
    mentor: ['> UpCore.Mentor', 'An AI mentor for every developer', 'Code quality 3.2 → 8.0 · a growth plan across 50+ factors'],
    blog: ['UPCORE BLOG', 'On engineering efficiency — no fluff', 'The “AI Team Lead UpCore” channel · Ivan Gel'],
  },
};
const html = (k, [kicker, title, sub]) => `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:B;font-weight:100 900;src:url(${font('bricolage-grotesque', 'bricolage-grotesque-latin-opsz-normal.woff2')})}
@font-face{font-family:O;font-weight:100 900;src:url(${font('onest', 'onest-cyrillic-wght-normal.woff2')});unicode-range:U+0400-045F}
@font-face{font-family:O;font-weight:100 900;src:url(${font('onest', 'onest-latin-wght-normal.woff2')})}
@font-face{font-family:M;font-weight:100 900;src:url(${font('jetbrains-mono', 'jetbrains-mono-latin-wght-normal.woff2')})}
@font-face{font-family:M;font-weight:100 900;src:url(${font('jetbrains-mono', 'jetbrains-mono-cyrillic-wght-normal.woff2')});unicode-range:U+0400-045F}
body{margin:0;width:1200px;height:630px;background:#0D0C15;color:#fff;font-family:B,O,sans-serif;overflow:hidden;position:relative}
.glow{position:absolute;right:-140px;top:-120px;width:620px;height:620px;border-radius:50%;background:radial-gradient(circle,${C[k]}33,transparent 65%)}
svg.ch{position:absolute;right:60px;top:80px;width:300px;opacity:.16}
.wrap{position:absolute;inset:64px 72px;display:flex;flex-direction:column}
.k{margin-top:auto;font-family:M,monospace;font-size:26px;letter-spacing:.04em;color:${C[k]}}
h1{margin:18px 0 0;font-size:68px;line-height:1.04;letter-spacing:-.03em;font-weight:800;max-width:960px}
p{margin:24px 0 0;font-family:O,sans-serif;font-size:26px;color:rgba(255,255,255,.72)}
.bar{position:absolute;left:0;right:0;bottom:0;height:8px;background:linear-gradient(90deg,#63D5FF,#B9AEFF,#F2C14E,#7FDB7A)}
</style></head><body><div class="glow"></div>
<svg class="ch" viewBox="0 0 375 645"><path fill="${C[k]}" d="M340 411C322 437 298 465 268 496L166 599C149 616 136 628 126 636C116 644 106 646 95 641C84 637 70 626 51 608L10 567L250 322L0 80L44 35C61 18 76 7 87 2C97-2 107 0 117 8C127 16 140 28 158 45L272 157C294 180 314 201 332 219C348 239 360 258 367 278C374 298 375 322 370 348C365 375 359 385 340 411Z"/></svg>
<div class="wrap"><img src="${logo}" style="height:40px;width:auto;align-self:flex-start"><div class="k">${kicker.replace('>', '&gt;')}</div><h1>${title}</h1><p>${sub}</p></div><div class="bar"></div></body></html>`;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
  for (const lang of ['ru', 'en']) for (const [k, v] of Object.entries(P[lang])) {
    await p.setContent(html(k, v), { waitUntil: 'load' });
    await p.waitForTimeout(150);
    await p.screenshot({ path: path.join(OUT, `${lang}-${k}.png`) });
  }
  await b.close();
  console.log('OG:', fs.readdirSync(OUT).length, 'картинок');
})();
