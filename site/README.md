# Сайт UpCore (up-core.ru)

**Развёртывание на боевом хостинге (up-core.ru) — `docs/DEPLOY.md`.** Конфиги: `deploy/nginx.conf`, `deploy/form-handler.php`, `deploy/deploy.yml.example`.

> Полная архитектура, правка и публикация — **`docs/ARCHITECTURE.md`** в корне репозитория.

Astro + TypeScript + Tailwind. Статический сайт: RU (`/`) и EN (`/en/`), 8 страниц на язык —
главная, Grade, AI, Projects, Mentor, блог (3 страницы).

## Запуск на Mac
Нужен Node.js 20 или новее (https://nodejs.org → LTS, или `brew install node`).

```bash
cd site
npm install
npm run dev
```
Сайт откроется на http://localhost:4321. Чтобы показать коллегам в той же сети (Wi-Fi/офис):

```bash
npm run dev:lan
```
В консоли появится адрес вида `http://192.168.x.x:4321` — его можно открыть с телефона или другого компьютера.

## Сборка для хостинга
```bash
npm run build
```
Готовый сайт — папка `site/dist/` (обычные HTML/CSS/JS/картинки). Её можно выложить на любой хостинг/CDN в РФ
(Yandex Cloud Object Storage, Selectel, VK Cloud, Timeweb, nginx на своём сервере). Посмотреть сборку локально: `npm run preview`.

Настройки сервера:
- отдавать `404.html` для несуществующих адресов;
- адреса со слешем на конце (`/grade/` → `grade/index.html`);
- кэш для `/_astro/*` и `/img/*` — надолго (файлы с хешами), для HTML — без кэша.

## Настройки (`site/.env`, пример — `.env.example`)
| Переменная | Что делает |
|---|---|
| `PUBLIC_YM_ID` | номер счётчика Яндекс Метрики. Пусто — Метрики и cookie-баннера нет. Метрика грузится только после согласия в баннере. |
| `PUBLIC_FORM_ENDPOINT` | адрес обработчика формы заявки (POST, multipart/form-data, поля: topic, name, company, team, contact, comment, page, lang). Пусто — форма открывает письмо на почту с заполненной заявкой. Пример обработчика на PHP — `deploy/form-handler.php`. |
| `PUBLIC_FORM_EMAIL` | почта для заявок, по умолчанию office@dex-it.ru |

После изменения `.env` — снова `npm run build`.

## Как устроено
- `src/generated/<lang>/*.html` — страницы из утверждённых макетов. **Не править вручную**: их создаёт
  `python3 tools/content/export_web.py` из генератора макетов `tools/content/build_pages.py` (тот же код, что рисует холст).
- `site/i18n/en.json` — перевод всех строк на английский. Новые строки без перевода: `python3 tools/content/translate_web.py --missing`.
- `src/pages/[...path].astro` — маршруты RU/EN, SEO и schema.org; `src/data/seo.ts` — заголовки и описания страниц.
- `src/layouts/Base.astro` — общий шаблон; `src/components/` — меню на телефоне, форма заявки, cookie-баннер, Метрика.
- `src/scripts/site.ts` — поведение: липкая шапка, меню, слайдер, форма, цели Метрики, анимации (`docs/design/ANIMATIONS.md`).
- `public/og/` — картинки-превью для соцсетей (`node tools/content/og_images.js`), `public/img/` — логотип и скриншоты.

Порядок правки текста: `tools/content/build_pages.py` → `python3 tools/content/export_web.py` → при новых строках дописать `site/i18n/en.json`
→ снова `export_web.py` → `npm run build`.

## Проверка качества
При работающем `npm run preview` (из корня репозитория):
```bash
node tools/qa/check_layout.js
node tools/qa/check_interactions.js
```
