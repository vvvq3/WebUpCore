# SEO сайта UpCore (раунд 69, 14.11.2026)

Семантика собрана по продуктам, страницам и темам блога (без доступа к Wordstat — частотность проверить после подключения
Яндекс Вебмастера / Wordstat и поправить приоритеты). Мета-теги страниц — `site/src/data/seo.ts`.

## Что уже сделано на сайте
- У каждой страницы RU и EN: свой `title`, `description`, `keywords`, канонический адрес, `hreflang` ru / en / x-default.
- Open Graph и Twitter-превью: `site/public/og/<lang>-<page>.png` (1200×630, генератор — `tools/content/og_images.js`).
- Разметка schema.org (JSON-LD): Organization (UpCore, родитель — Dex), SoftwareApplication (на страницах продуктов),
  FAQPage (из блоков «Вопросы» — сниппеты с ответами в поиске), BreadcrumbList.
- `sitemap-index.xml` + `sitemap-0.xml` с языковыми альтернативами, `robots.txt`, страница 404 (noindex).
- Скорость: статический HTML, шрифты со своего сервера, скриншоты в WebP, JS ~4 КБ (gzip).
- Один `h1` на странице (первый экран), заголовки блоков — `h2`.

## Семантическое ядро (RU)
| Кластер | Страница | Ключевые запросы |
|---|---|---|
| Эффективность разработки | `/` | оценка эффективности разработчиков; эффективность разработки; метрики эффективности разработки; продуктивность программистов; как оценить работу программиста; оценка программистов по коду; управление ИТ-командой; цифровой тимлид; аналитика разработки |
| Грейд и рейтинг | `/grade/` | грейд разработчика; грейдирование программистов; оценка уровня разработчика; junior middle senior как определить; матрица компетенций разработчика; performance review разработчиков; рейтинг разработчиков; ассессмент программистов |
| ИИ в разработке | `/ai/` | эффективность ИИ в разработке; вайбкодинг; ИИ-ассистенты для программистов эффективность; как измерить эффект Copilot / Cursor / Claude; детект ИИ-кода; расходы на токены LLM; внедрение ИИ в разработку |
| Подрядчики и бюджет | `/projects/` | аудит ИТ-подрядчика; проверка акта выполненных работ разработка; аудит кода; оценка стоимости разработки; контроль аутсорса разработки; бюджет ИТ-проекта; технический долг оценка; due diligence ИТ-компании |
| Наставничество и ревью | `/mentor/` | ИИ код-ревью; автоматическое код-ревью; ИИ-наставник для разработчиков; ИПР программиста; развитие разработчиков; онбординг разработчиков; качество кода |
| Блог (информационные) | `/blog/` | code churn; закон Гудхарта метрики; ROI внедрения; сколько стоит код; правило 20% неэффективных сотрудников; инженеры-призраки удалёнка |

## Семантическое ядро (EN)
| Cluster | Page | Keywords |
|---|---|---|
| Engineering efficiency | `/en/` | developer productivity; engineering efficiency; software engineering metrics; engineering intelligence platform; developer performance; measure developer productivity |
| Grades | `/en/grade/` | developer leveling; engineering career ladder; developer performance review; senior developer assessment; developer ranking |
| AI | `/en/ai/` | AI coding productivity; vibe coding; measure Copilot impact; AI-generated code detection; LLM token costs |
| Vendors | `/en/projects/` | software vendor management; IT vendor audit; code audit; software development cost estimation; technical due diligence |
| Mentoring | `/en/mentor/` | AI code review; automated code review; developer growth plan; engineering mentoring |

## Что сделать после запуска (нужен доступ владельца)
1. Яндекс Вебмастер и Google Search Console: подтвердить права на up-core.ru (мета-тег или DNS), отправить `https://up-core.ru/sitemap-index.xml`.
2. Яндекс Метрика: номер счётчика → `PUBLIC_YM_ID` в `site/.env`, пересобрать. Цели (JavaScript-события) завести в интерфейсе Метрики:
   `connect`, `form_open_demo`, `form_open_report`, `form_open_audit`, `form_sent_demo`, `form_sent_report`, `form_sent_audit`, `phone`, `telegram`, `email`, `channel`.
3. Проверить частотность ключей в Wordstat и при необходимости поправить `title`/`description` в `site/src/data/seo.ts`.
4. Если у старого сайта были страницы в поиске с другими адресами — настроить 301-редиректы на новые (список даст Вебмастер).
