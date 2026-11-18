# Презентации UpCore для CTO (раунд 96)

20 PDF (16:9, 1920×1080, русский): платформа + 4 продукта × 4 варианта.

| Папка | 1 — короткая | 2 — средняя | 3 — длинная | 4 — светлая |
|---|---|---|---|---|
| `01-platform` | 7 | 12 | 19 | 12 |
| `02-grade` | 7 | 11 | 19 | 11 |
| `03-ai` | 7 | 12 | 19 | 12 |
| `04-projects` | 7 | 11 | 19 | 11 |
| `05-mentor` | 7 | 11 | 17 | 11 |

Варианты 1–3 — в стиле сайта (тёмная тема), 4 — светлая тема с содержанием средней.
Оглавление — `index.html` (на Pages: https://vvvq3.github.io/WebUpCore/decks/).

Пересборка:
```bash
python3 tools/decks/build_decks.py && node tools/decks/render.js && python3 tools/decks/index_page.py
```
