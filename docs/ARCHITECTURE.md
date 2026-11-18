# Архитектура сайта UpCore и как с ним работать

Версия: **release1 — 18.11.2026** (ветка `release1`; описание — `docs/release1/README.md`). **Развёртывание на боевом хостинге — `docs/DEPLOY.md`.** Предыдущая — v5 (ветка `upcore-v5`). Рабочая ветка разработки: `claude/charming-tesla-nky17x`.

## 1. Коротко

Сайт `up-core.ru` — статический сайт на **Astro 5 + TypeScript + Tailwind 4**. Языки: русский (`/`) и английский (`/en/`).
На каждый язык 8 страниц: главная, Grade, AI, Projects, Mentor, блог (3 страницы с пагинацией).

Главная особенность: **вёрстка страниц не пишется вручную в Astro.** Её генерирует Python-скрипт `tools/content/build_pages.py`.
Этот же скрипт рисует утверждённые макеты на холсте дизайна (https://claude.ai/artifact/57F1KYxREb3qKCN4yMdioJ).
Поэтому сайт всегда совпадает с макетами, а правка текста делается в одном месте.

```
build_pages.py ──(режим 'dc')──▶ холст дизайна (.dc.html)
       │
       └──(режим 'web', export_web.py)──▶ site/src/generated/{ru,en}/*.html ──▶ Astro ──▶ site/dist/ (готовый сайт)
                                   ▲
                       site/i18n/en.json (перевод)
```

## 2. Как запустить

Нужен **Node.js 20+** (Mac: `brew install node` или установщик с nodejs.org). Python 3 и Pillow нужны только для правки текстов.

```bash
cd site
npm install          # один раз
npm run dev          # http://localhost:4321, правки видны сразу
npm run dev:lan      # то же, но доступно с телефона/других компьютеров в той же сети
npm run build        # сборка в site/dist/
npm run preview      # посмотреть сборку (http://localhost:4321)
npm run check        # проверка типов TypeScript
```

## 3. Что где лежит

```
WebUpCore/
├── CLAUDE.md                     — краткий контекст проекта для Claude
├── docs/
│   ├── ARCHITECTURE.md           — этот файл
│   ├── DEPLOY.md                 — развёртывание на боевом хостинге и нюансы работы системы
│   ├── UPCORE_KNOWLEDGE_BASE.md  — база знаний о продукте и все решения владельца (раздел 18 — по раундам)
│   ├── SEO.md                    — семантическое ядро RU/EN и что сделать после запуска
│   ├── PRE_BUILD_QUESTIONS.md    — вопросы перед вёрсткой и ответы владельца
│   ├── brand/                    — логотипы, фавикон
│   ├── design/
│   │   ├── ANIMATIONS.md         — утверждённые анимации (спецификация)
│   │   ├── content/              — актуальные .dc.html макетов с холста
│   │   ├── final/canvas.json     — раскладка холста
│   │   └── v1 … v5/              — снимки версий (README в каждой)
│   └── reference/demo/screens/   — скриншоты демо для слайдера главной (slides/ — старые, для холста)
├── tools/
│   ├── content/
│   │   ├── build_pages.py        — ГЕНЕРАТОР: все тексты, блоки и стили страниц
│   │   ├── export_web.py         — экспорт страниц в сайт (RU + EN), стили, картинки
│   │   ├── translate_web.py      — перевод на английский по словарю site/i18n/en.json
│   │   ├── og_images.js          — картинки-превью для соцсетей (site/public/og/)
│   │   ├── preview_bundle.py     — копия сборки с относительными ссылками (просмотр на claude.ai)
│   │   └── measure.js            — замер высоты макетов для холста
│   └── qa/
│       ├── check_layout.js       — проверка вёрстки 16 страниц × 7 ширин
│       └── check_interactions.js — проверка меню, формы, фильтра, слайдера, анимаций
└── site/                         — САЙТ (Astro)
    ├── package.json, astro.config.mjs, tsconfig.json
    ├── .env.example              — настройки: Метрика, обработчик формы, почта
    ├── README.md                 — краткая инструкция для разработчика
    ├── deploy/form-handler.php   — пример обработчика формы для хостинга с PHP
    ├── i18n/en.json              — перевод всех строк страниц на английский (RU → EN)
    ├── public/                   — favicon, robots.txt, img/ (логотип, скриншоты WebP), og/ (превью)
    └── src/
        ├── generated/{ru,en}/*.html — страницы из генератора (НЕ ПРАВИТЬ вручную)
        ├── pages/[...path].astro — маршруты всех страниц RU/EN, SEO, schema.org (FAQ, хлебные крошки)
        ├── pages/404.astro       — страница «не найдено»
        ├── layouts/Base.astro    — общий шаблон: <head>, мета-теги, шрифты, компоненты
        ├── components/
        │   ├── MobileMenu.astro  — меню на весь экран для телефона и планшета
        │   ├── LeadForm.astro    — форма заявки (демо / демо-отчёт / аудит)
        │   ├── CookieBanner.astro— баннер cookie (только если включена Метрика)
        │   └── Analytics.astro   — подключение Яндекс Метрики по PUBLIC_YM_ID
        ├── data/
        │   ├── seo.ts            — title / description / keywords страниц RU и EN
        │   └── i18n.ts           — тексты интерфейса (меню, форма, cookie, 404), цвета продуктов, контакты
        ├── scripts/site.ts       — поведение: шапка, меню, слайдер, форма, фильтр блога, Метрика, анимации
        └── styles/
            ├── global.css        — стили сайта: шрифты, шапка, анимации, меню, форма, cookie
            └── generated.css     — общие стили макетов (из генератора, НЕ ПРАВИТЬ вручную)
```

## 4. Как править

### Текст или блок на странице
1. Найти текст в `tools/content/build_pages.py` (функции страниц: `home('A')`, `grade_page(3)`, `ai_page_final()`, `proj_main2()`, `mentor_main2()`, `blog_page2(n)`).
2. Исправить и выполнить:
   ```bash
   python3 tools/content/export_web.py           # пересобрать страницы RU и EN
   python3 tools/content/translate_web.py --missing   # какие новые строки ещё не переведены
   ```
3. Если есть непереведённые строки (список в `site/i18n/missing.json`), добавить их в `site/i18n/en.json` (ключ — русская строка, значение — английская) и снова запустить `export_web.py`.
4. `cd site && npm run build` и проверить.
5. Чтобы холст дизайна совпадал с сайтом — `python3 tools/content/build_pages.py <папка холста> <папка превью>` и опубликовать изменённые `.dc.html` на холст.

### Новая версия сайта (раунды 82–88)
- Русские страницы — **новая версия**: `home_v2()`, `grade_v2()`, `ai_v2()`, `proj_v2()`, `mentor_v2()`, `blog_v2(n)` в `build_pages.py`; общие блоки — `header_v2()`, `saas_v2()`, `cta_v2()`, `hero_ctas_v2()`.
  Все «демо»-кнопки открывают форму «Провести демо». Переключателя языков нет; EN-страницы — перевод новой версии (раунд 94), открываются по адресам `/en/…`.
- Прежняя версия снята с публикации (раунд 88); её статичный снимок — в истории git (коммит 9b7d65c, `site/public/old/`).
- Вернуть страницу к прежней версии — убрать её из `RU_OVERRIDES` в `tools/content/export_web.py`.

### Заголовки и описания для поисковиков
`site/src/data/seo.ts` (RU и EN отдельно). FAQ для поисковиков собирается автоматически из блоков «Вопросы».

### Меню, форма, cookie, тексты интерфейса
`site/src/components/*.astro` и `site/src/data/i18n.ts`.

### Поведение и анимации
`site/src/scripts/site.ts` + `site/src/styles/global.css`. Правила анимаций — `docs/design/ANIMATIONS.md`.

### Презентации для CTO (PDF, раунд 96)
`tools/decks/build_decks.py` — слайды (функции `sl_*`), темы (тёмная по сайту и светлая `.light`) и состав 20 презентаций (`deck_*`, варианты 1–4); данные — из `tools/content/build_pages.py`.
`node tools/decks/render.js [фильтр]` — PDF 1920×1080 в `docs/decks/`, проверка переполнения каждого слайда, превью `tools/decks/build/png/` (`--no-png` — без превью).
`python3 tools/decks/index_page.py` — оглавление `docs/decks/index.html` и обложки. На Pages копируется в `/decks/` (шаг в `pages.yml`).

## 5. Как устроены ключевые части

- **Шапка.** Липкая, при прокрутке становится ниже и получает фон с размытием.
  - ≥ 1360 px — полная: «Платформа · [UpCore. ● Grade ● AI ● Projects ● Mentor] · Блог · Контакты», RU/EN, «Провести демо», «Подключить».
  - 1161–1359 px — компактная (без подписи «UpCore.»); 1161–1239 px — ещё без RU/EN.
  - ≤ 1160 px — логотип, «Подключить» и бургер → меню на весь экран (`MobileMenu.astro`).
- **Форма заявки.** Кнопки с `data-form="demo|report|audit|pilot"` открывают одну форму с нужной темой. Поля: имя, компания, размер команды, контакт.
  На GitHub Pages заявки уходят письмом на office@dex-it.ru через FormSubmit (`PUBLIC_FORM_ENDPOINT` в `.github/workflows/pages.yml`; один раз подтвердить письмо «Activate Form»). На хостинге в РФ — `site/deploy/form-handler.php` (почта + Telegram по TG_BOT_TOKEN / TG_CHAT_ID). Если отправка не удалась — открывается письмо с заполненной заявкой.
  Если задан `PUBLIC_FORM_ENDPOINT` — отправка POST на этот адрес, иначе открывается письмо на `PUBLIC_FORM_EMAIL` с заполненными полями.
- **Яндекс Метрика.** `PUBLIC_YM_ID` → появляется cookie-баннер; счётчик грузится только после согласия.
  Цели: `connect`, `form_open_*`, `form_sent_*`, `phone`, `telegram`, `email`, `channel`.
- **Блог.** Посты ведут в Telegram-канал. Фильтр по темам показывает посты темы со всех трёх страниц.
- **Слайдер на главной.** 14 скриншотов демо в пропорции 2:1 (список и подписи — `SCREENS` в `build_pages.py`; `export_web.py` готовит WebP 1600×800 в `site/public/img/screens/v2/` из `docs/reference/demo/screens/`). Чтобы заменить экраны — положить PNG в `docs/reference/demo/screens/` и поправить `SCREENS`. Без кнопок и подписи: голубая полоса без пауз идёт сверху вниз за 1,5 с и «рисует» новый скриншот поверх старого; пауза при наведении мыши.
- **Анимации.** Появление блоков, рост шкал, цифры-табло, отклик карточек и кнопок, подсветка за курсором, анимация блока «UpCore не считает строчки кода».
  Уважается системная настройка «уменьшить движение». Первый экран показывается сразу, без анимации появления.
- **SEO.** canonical, hreflang ru/en/x-default, Open Graph, sitemap (`@astrojs/sitemap`), robots.txt, JSON-LD: Organization, SoftwareApplication, FAQPage, BreadcrumbList.
- **Шрифты.** Bricolage Grotesque, Onest, JetBrains Mono — свои файлы (`@fontsource-variable`), без Google Fonts; основные предзагружаются.

## 6. Публикация на хостинге

1. `cd site && npm install && npm run build` → папка `site/dist/`.
2. Выложить содержимое `dist/` на хостинг в РФ (Yandex Cloud Object Storage + CDN, Selectel, VK Cloud, Timeweb, nginx).
3. Настройки сервера:
   - сжатие gzip/brotli для HTML/CSS/JS (без него страницы в ~5 раз тяжелее);
   - `404.html` для несуществующих адресов;
   - адреса со слешем на конце (`/grade/` → `grade/index.html`);
   - кэш надолго для `/_astro/*` и `/img/*`, без кэша для HTML.
4. Если нужен приём заявок без открытия почты — разместить обработчик (пример `site/deploy/form-handler.php`) и указать его адрес в `PUBLIC_FORM_ENDPOINT`.
5. После запуска: Яндекс Вебмастер и Google Search Console, отправить `https://up-core.ru/sitemap-index.xml` (см. `docs/SEO.md`).

Автодеплой через GitHub Actions подключается после выбора хостинга (шаги: `npm ci` → `npm run build` → загрузка `site/dist/`).

### Показ коллегам — GitHub Pages
Адрес: **https://vvvq3.github.io/WebUpCore/** (копия сайта для показа: относительные ссылки, `noindex`, ветка `gh-pages`).
Обновляется сама: при каждом push в `claude/charming-tesla-nky17x` workflow `.github/workflows/pages.yml` собирает сайт
(`npm ci && npm run build` → `python3 tools/content/preview_bundle.py --pages ghp`) и выкладывает в `gh-pages`.
Один раз в настройках репозитория: Settings → Pages → Source «Deploy from a branch» → `gh-pages` / `(root)`.

## 7. Проверка качества

При работающем `npm run preview`:
```bash
node tools/qa/check_layout.js        # 16 страниц × 7 ширин (360…1920): переполнения, h1, картинки, ошибки, ссылки
node tools/qa/check_interactions.js  # меню, форма (и что она по центру), фильтр, слайдер, прокрутка, прыжок в конец, цифры, анимация #core
```
Результат проверки v5: 112 комбинаций без замечаний, 10/10 сценариев.
Lighthouse: компьютер — 100 / 100 / 100 / 100; телефон (медленный 4G) — скорость 84–91, доступность 100, лучшие практики 100, SEO 100.

## 8. Версии и ветки

| Версия | Что | Где |
|---|---|---|
| v1–v4 | макеты на холсте | `docs/design/v1…v4/` |
| v5 | свёрстанный сайт RU+EN, меню, форма, анимации, SEO | ветка `upcore-v5`, `docs/design/v5/` |
| **release1** | новая главная и 4 продукта по ТЗ владельца, единые блоки, форма с отправкой, без переключателя языков | ветка `release1`, `docs/release1/`, `docs/DEPLOY.md` |

Вернуться к версии v5: `git checkout upcore-v5`.
