# UpCore — сайт up-core.ru

Сайт продукта UpCore («цифровой тимлид» — оценка эффективности разработки по коду). Статика: сервера в рантайме нет, `npm run build` собирает готовые HTML/CSS/JS в `dist/`.

Два языка:

| Язык | Страницы |
|---|---|
| RU (основной) | `/` — главная, `/grade/`, `/ai/`, `/projects/`, `/mentor/`, блог `/blog/`, `/blog/2/`, `/blog/3/` |
| EN | `/en/`, `/en/grade/`, `/en/ai/`, `/en/projects/`, `/en/mentor/` (без блога) |

Плюс `404.html`, `sitemap-index.xml`, `robots.txt` и OG-картинки для соцсетей.

Прежний лендинг на Next.js сохранён в ветке `old-site`.

## Стек

- **Astro 5** + **TypeScript** — страницы собираются в статику, клиентского фреймворка нет, поведение — один скрипт `src/scripts/site.ts`
- **Tailwind CSS 4** через `@tailwindcss/vite`
- Шрифты Bricolage Grotesque, Onest и JetBrains Mono — из npm (`@fontsource-variable/*`), без внешних CDN
- `@astrojs/sitemap` — карта сайта с RU/EN

## Запуск

Нужен Node >= 20.

```bash
npm ci
```

```bash
npm run dev
```

Дев-сервер поднимется на http://localhost:4321.

## Сборка

```bash
npm run build
```

Результат — статика в `dist/`. Посмотреть собранный сайт локально:

```bash
npm run preview
```

## Выкладка (Docker)

Как и раньше, образ собирается по `Dockerfile`: `node:22-alpine` (`npm ci` → `npm run build`) → `nginx:alpine` со статикой из `dist/` и конфигом `nginx.conf`, порт 80. Версии образов — по `.gitversion.yml`.

```bash
docker build -t upcore-landing .
```

```bash
docker run --rm -p 8080:80 upcore-landing
```

Сайт откроется на http://localhost:8080.

`nginx.conf`:

- адрес без слеша → со слешем (`/grade` → `/grade/`), редирект относительный — работает за HTTPS-прокси;
- `404.html` для несуществующих адресов;
- gzip; кэш `/_astro/*` на год (имена с хэшем), `/img/*` и `/og/*` — на 30 дней, HTML — `no-cache`;
- заголовки безопасности (`X-Content-Type-Options`, `Referrer-Policy`, `X-Frame-Options`).

### Параметры сборки

Передаются как `--build-arg`, значения по умолчанию уже заданы в `Dockerfile`. Для локальной сборки без Docker — в `.env` (пример — `.env.example`).

| Параметр | По умолчанию | Что делает |
|---|---|---|
| `PUBLIC_FORM_ENDPOINT` | `https://formsubmit.co/ajax/office@dex-it.ru` | куда уходит форма заявки («Провести демо», «Бесплатный пилот» и др.). Пусто — форма открывает письмо на почту с заполненными полями |
| `PUBLIC_FORM_EMAIL` | `office@dex-it.ru` | почта для заявок |
| `PUBLIC_YM_ID` | пусто | номер счётчика Яндекс Метрики. Пусто — Метрики и cookie-баннера нет; со счётчиком Метрика грузится только после согласия в баннере |

Форма идёт через FormSubmit: первая заявка с нового домена приходит на office@dex-it.ru письмом от FormSubmit со ссылкой активации — по ней нужно один раз перейти, дальше заявки приходят сразу.

## Проверки

```bash
npm run check
```

Проверка типов и шаблонов Astro (`astro check`).

## Структура

| Путь | Что внутри |
|---|---|
| `src/pages/[...path].astro` | все страницы RU и EN: маршруты, заголовки, описания |
| `src/pages/404.astro` | страница «не найдено» |
| `src/layouts/Base.astro` | `<head>`: мета, canonical, hreflang, OG, JSON-LD, шрифты; подключает меню, форму заявки, cookie-баннер, Метрику |
| `src/generated/ru`, `src/generated/en` | содержимое страниц — HTML-фрагменты |
| `src/components/*` | форма заявки, мобильное меню, cookie-баннер, Метрика |
| `src/scripts/site.ts` | поведение: меню, слайдер скриншотов, анимации цифр, форма |
| `src/styles/*` | общие стили и адаптив |
| `src/data/*` | SEO-тексты и строки интерфейса RU/EN |
| `i18n/*` | словарь перевода на английский |
| `public/` | логотип, скриншоты демо (`img/screens/`), OG-картинки (`og/`), `robots.txt` |

## Ветки

| Ветка | Что |
|---|---|
| `develop` | рабочая ветка сайта |
| `feature/*` | правки → Merge Request в `develop` |
| `old-site` | прежний лендинг на Next.js (архив) |

## Правила

- Тексты страниц (`src/generated/`) выгружаются из генератора в репозитории разработки сайта: правка напрямую здесь будет перезаписана следующей выгрузкой — изменения текстов лучше вносить через генератор.
- Цифры и формулировки на сайте согласованы с владельцем продукта; цены не публикуются.
- Бренд: тёмный фон `#0D0C15`, карточки `#1A1925`, акцент `#63D5FF`, у продуктов свои акценты (AI — сиреневый, Projects — жёлтый, Mentor — зелёный).
