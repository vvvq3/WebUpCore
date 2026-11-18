# -*- coding: utf-8 -*-
"""Страница-оглавление презентаций docs/decks/index.html (+ обложки-превью). Запуск после render.js."""
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
OUT = os.path.join(ROOT, 'docs', 'decks')
PNG = os.path.join(HERE, 'build', 'png')

DECKS = [('01-platform', 'Platform', 'Платформа UpCore', 'Цифровой тимлид: проблема, математическая модель, 4 продукта, экономика, безопасность.', '#63D5FF'),
         ('02-grade', 'Grade', 'UpCore Grade', 'Объективный грейд и рейтинг команды каждый месяц — для CTO и HRD.', '#63D5FF'),
         ('03-ai', 'AI', 'UpCore AI', 'Реальная эффективность ИИ и вайбкодеров: ROI, автодетект 92%+, токены, промпт-ревью.', '#B9AEFF'),
         ('04-projects', 'Projects', 'UpCore Projects', 'Бюджет проекта и контроль подрядчиков в часах и рублях — для CEO, CFO, CTO.', '#F2C14E'),
         ('05-mentor', 'Mentor', 'UpCore Mentor', 'ИИ-наставник для каждого разработчика: ревью, промпты, ИПР.', '#7FDB7A')]
VAR = [('1-short', 'Короткая'), ('2-medium', 'Средняя'), ('3-long', 'Длинная'), ('4-light', 'Светлая')]


def pages(name):
    d = os.path.join(PNG, name)
    return len([f for f in os.listdir(d) if f.endswith('.png')]) if os.path.isdir(d) else 0


cards = []
for folder, en, title, sub, col in DECKS:
    for v in ('2-medium', '4-light'):
        src = os.path.join(PNG, 'UpCore-%s-%s' % (en, v), '01.png')
        if os.path.exists(src):
            Image.open(src).convert('RGB').resize((800, 450), Image.LANCZOS).save(os.path.join(OUT, folder, 'cover-%s.jpg' % v.split('-')[1]), quality=84)
    links = ''.join('<a href="%s/UpCore-%s-%s.pdf"><b>%s</b><span>%d слайдов · %d МБ</span></a>' % (
        folder, en, v, lab, pages('UpCore-%s-%s' % (en, v)), round(os.path.getsize(os.path.join(OUT, folder, 'UpCore-%s-%s.pdf' % (en, v))) / 1048576) or 1) for v, lab in VAR)
    cards.append('<article style="--c: %s"><div class="pics"><img src="%s/cover-medium.jpg" alt=""><img src="%s/cover-light.jpg" alt=""></div><h2>%s</h2><p>%s</p><nav>%s</nav></article>' % (col, folder, folder, title, sub, links))

html = '''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex">
<title>Презентации UpCore</title><style>
:root { --bg: #0D0C15; --card: #1A1925; --fg: #fff; --mut: rgba(255,255,255,.7); --line: rgba(255,255,255,.12); }
* { box-sizing: border-box; } body { margin: 0; background: var(--bg); color: var(--fg); font: 16px/1.5 system-ui, -apple-system, 'Segoe UI', sans-serif; }
main { max-width: 1180px; margin: 0 auto; padding: 48px 16px 64px; } h1 { font-size: clamp(28px, 5vw, 44px); margin: 0 0 8px; letter-spacing: -.02em; }
.lead { color: var(--mut); margin: 0 0 32px; max-width: 760px; } .grid { display: grid; gap: 20px; grid-template-columns: repeat(auto-fill, minmax(min(100%, 520px), 1fr)); }
article { background: var(--card); border: 1px solid var(--line); border-radius: 20px; padding: 18px; } .pics { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.pics img { width: 100%; border-radius: 10px; display: block; aspect-ratio: 16/9; object-fit: cover; } h2 { margin: 16px 0 4px; font-size: 24px; color: var(--c); }
article p { margin: 0 0 14px; color: var(--mut); } nav { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }
nav a { display: flex; flex-direction: column; gap: 2px; padding: 10px 12px; border-radius: 12px; border: 1px solid var(--line); color: var(--fg); text-decoration: none; }
nav a:hover { border-color: var(--c); } nav b { font-size: 15px; } nav span { font-size: 12px; color: var(--mut); }
@media (max-width: 560px) { nav { grid-template-columns: 1fr 1fr; } } footer { margin-top: 40px; color: var(--mut); font-size: 14px; }
footer a { color: #63D5FF; }
</style></head><body><main><h1>Презентации UpCore для CTO</h1>
<p class="lead">Платформа и 4 продукта, по 4 варианта: короткая (7 слайдов), средняя (11–12), длинная (17–19) — в стиле сайта, и светлая (содержание средней). PDF 16:9, на русском.</p>
<div class="grid">%%CARDS%%</div><footer>UpCore · Dex · <a href="mailto:office@dex-it.ru">office@dex-it.ru</a> · +7 (985) 848-35-55 · Telegram @IvanGel_Dex</footer></main></body></html>'''.replace('%%CARDS%%', ''.join(cards))
open(os.path.join(OUT, 'index.html'), 'w').write(html)
print('ok', os.path.join(OUT, 'index.html'))
