# UpCore — сайт up-core.ru

Сайт продукта UpCore («цифровой тимлид»). Статический: сервера в рантайме нет, `npm run build` собирает готовые HTML/CSS/JS в `dist/`.

- **RU** (основной язык): `/` — главная, `/grade/`, `/ai/`, `/projects/`, `/mentor/`, блог `/blog/`, `/blog/2/`, `/blog/3/`.
- **EN**: `/en/`, `/en/grade/`, `/en/ai/`, `/en/projects/`, `/en/mentor/` (без блога).
- `404.html`, `sitemap-index.xml`, `robots.txt`, OG-картинки для соцсетей.

Прежняя версия лендинга (Next.js) сохранена в ветке **`old-site`**.

## Стек
Astro 5 + TypeScript + Tailwind CSS 4. Шрифты Bricolage Grotesque, Onest, JetBrains Mono — из npm (`@fontsource-variable/*`), без внешних CDN.

## Выкладка (как и раньше — Docker)
`Dockerfile`: сборка на `node:22-alpine` (`npm ci` → `npm run build`) → образ `nginx:alpine` со статикой из `dist/` и конфигом `nginx.conf`, порт 80.
Версии образов — по `.gitversion.yml` (ветки develop / feature / stage / main).

```bash
docker build -t upcore-landing .
docker run --rm -p 8080:80 upcore-landing     # http://localhost:8080
```

`nginx.conf`: `/grade` → `/grade/` (относительный редирект, работает за HTTPS-прокси), `404.html` для несуществующих адресов,
gzip, кэш `/_astro/*` на год (имена с хэшем), `/img/*` и `/og/*` — на 30 дней, HTML — `no-cache`, заголовки безопасности.

### Параметры сборки (`--build-arg`, по умолчанию уже заданы)
| Параметр | По умолчанию | Что делает |
|---|---|---|
| `PUBLIC_FORM_ENDPOINT` | `https://formsubmit.co/ajax/office@dex-it.ru` | куда отправляется форма заявки («Провести демо», «Бесплатный пилот» и др.). Пусто — форма открывает письмо на почту с заполненными полями |
| `PUBLIC_FORM_EMAIL` | `office@dex-it.ru` | почта для заявок (и для запасного варианта письмом) |
| `PUBLIC_YM_ID` | пусто | номер счётчика Яндекс Метрики. Пусто — Метрики и cookie-баннера нет; со счётчиком Метрика грузится только после согласия в баннере |

**Форма через FormSubmit:** первая заявка с нового домена приходит на office@dex-it.ru письмом от FormSubmit со ссылкой активации — по ней нужно один раз перейти, дальше заявки приходят сразу.

## Локальный запуск
Нужен Node.js 20+.

```bash
npm ci
npm run dev        # http://localhost:4321
npm run build      # результат — dist/
npm run preview    # посмотреть сборку
```

## Структура
| Путь | Что внутри |
|---|---|
| `src/pages/[...path].astro` | все страницы RU и EN (маршруты и SEO-данные) |
| `src/layouts/Base.astro` | `<head>`: мета, canonical, hreflang, OG, JSON-LD, шрифты |
| `src/generated/ru`, `src/generated/en` | содержимое страниц (HTML-фрагменты) |
| `src/components/` | форма заявки, мобильное меню, cookie-баннер, Метрика |
| `src/scripts/site.ts` | поведение: меню, слайдер, анимации, форма |
| `src/styles/` | общие стили |
| `src/data/` | SEO-тексты и строки интерфейса RU/EN |
| `i18n/en.json` | словарь перевода EN |
| `public/` | логотип, скриншоты демо, OG-картинки, `robots.txt` |

Тексты страниц генерируются из исходного проекта сайта (генератор и база знаний — в репозитории разработки сайта); при правке напрямую в `src/generated/` следующая выгрузка из генератора их перезапишет.
