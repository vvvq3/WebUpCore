# -*- coding: utf-8 -*-
"""Генератор макетов страниц UpCore (раунд 4 — тексты) в формате .dc.html холста.

Стиль — концепт v3 «Командный центр». Тексты — из исследования (docs/content/research-notes.md)
и таблицы тезисов (docs/content/theses.md).

python3 tools/content/build_pages.py <out_dc_dir> [<out_preview_dir>]
  out_dc_dir      — .dc.html для холста (картинки как /_blob/<id>)
  out_preview_dir — обычный HTML с локальными картинками для замера и проверки вёрстки
"""
import os, sys, html as H

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
LOGO = '8c539bd29559b45927b81ec6072a2f13'
IMG = {  # blob на холсте → локальный файл
    'star': ('7cd7cff4eff6a602425a03a2f2943123', 'star.jpg'),
    'company': ('874ddb64d6ed37abac1670b8eff89422', 'company.jpg'),
    'efficiency': ('09020e28d571e789863f902b9c601584', 'efficiency.jpg'),
    'timesheet': ('9a5ee819cdf63a048d4a2b3cbb0e9c2e', 'timesheet.jpg'),
    'eye': ('fa83739845c10442627b3456f340371d', 'eye.jpg'),
    'rating': ('f1cbfde1916dfb0e20dde04d6b589af0', 'rating.jpg'),
    'quality': ('691189383b549ed50f9587ae5aedff28', 'quality.jpg'),
    'techmap': ('d08fc0c9136af956f7ae24957a0b8b9d', 'techmap.jpg'),
}
MODE = 'dc'
# высоты артбордов на 1440 px (замер Playwright, tools/content/measure.js)
HEIGHTS = {}

def src(key):
    if key == 'logo':
        return '/_blob/' + LOGO if MODE == 'dc' else 'file://' + REPO + '/docs/brand/logo.svg'
    b, f = IMG[key]
    return '/_blob/' + b if MODE == 'dc' else 'file://' + REPO + '/docs/reference/demo/slides/' + f

ACC = {  # цвет модуля: (линия/фон, текст)
    None: ('#63D5FF', '#63D5FF'), 'grade': ('#63D5FF', '#63D5FF'), 'ai': ('#9B8CFF', '#B9AEFF'),
    'projects': ('#F2C14E', '#F2C14E'), 'mentor': ('#53C04D', '#7FDB7A'),
}
MONO = "font-family: 'JetBrains Mono', monospace;"
DIM = 'rgba(255,255,255,0.74)'

def e(t):
    """Экранирование + [[акцент]] → голубой span."""
    t = H.escape(t, quote=False)
    return t.replace('[[', '<span style="color: #63D5FF;">').replace(']]', '</span>')

# ---------------------------------------------------------------- каркас
HELMET = """<helmet>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400..800&amp;family=Onest:wght@400..800&amp;family=JetBrains+Mono:wght@400;600&amp;display=swap" rel="stylesheet">
<style>
body{margin:0;background:#0D0C15}
a{color:#63D5FF}a:hover{color:#A8E8FF}
@keyframes ucBlink{0%,100%{opacity:1}50%{opacity:.25}}
@keyframes ucIn{from{opacity:0;transform:scale(.985)}to{opacity:1;transform:none}}
@keyframes ucProg{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes ucScanY{0%{top:0}100%{top:100%}}
.uc-blink{animation:ucBlink 1.4s ease-in-out infinite}
.uc-in{animation:ucIn .6s ease-out both}
.uc-prog{transform-origin:left;animation:ucProg 4.5s linear both}
.uc-scan{animation:ucScanY 4.5s linear infinite}
.uc-chips{display:flex;gap:6px;overflow-x:auto;scrollbar-width:none}
.uc-ml{display:none}
.g2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}
.uc-row{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:40px;align-items:start}
.g3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.g4{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
.g4m2{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
@media (max-width:1100px){.g3,.g4{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:720px){.uc-sc{grid-template-columns:minmax(0,1fr) minmax(0,1fr)!important}.uc-sc>span:first-child{grid-column:1/-1}.uc-sc>span:first-child:empty{display:none}.uc-ml{display:block!important;font-family:'JetBrains Mono',monospace;font-size:12px;font-weight:400;color:rgba(255,255,255,0.55);margin-bottom:2px;white-space:normal}th .uc-ml{display:inline!important;font-family:inherit;font-size:inherit;color:inherit}.uc-res thead{display:none}.uc-res tr{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr)}.uc-res th[scope=row]{grid-column:1/-1}.uc-res td,.uc-res th{border-top:0!important;padding:4px 8px 4px 0!important}.uc-res tr{border-top:1px solid rgba(255,255,255,0.1);padding:12px 0}.uc-row{grid-template-columns:minmax(0,1fr);gap:16px}.g2,.g3,.g4{grid-template-columns:minmax(0,1fr)}.g4m2{grid-template-columns:repeat(2,minmax(0,1fr))}.uc-cmp thead{display:none}.uc-cmp tr{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr)}.uc-cmp th[scope=row]{grid-column:1/-1;padding:14px 0 6px!important}.uc-cmp td{padding:6px 10px 14px!important;border-top:0!important}}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important}}
</style>
</helmet>"""

SLIDES = [
    ('Звезда грейда', 'Уровень', 'звезда грейда по 10 осям и динамика роста', 'star'),
    ('Компания', 'Дашборд компании', 'эффективность, ИИ, проекты, грейды', 'company'),
    ('Эффективность', 'Эффективность специалиста', 'создано ценности в часах и рублях', 'efficiency'),
    ('Табель', 'Табель', 'Jira, MR и коммиты в одном календаре', 'timesheet'),
    ('Глаз', '«Глаз»', 'разбор каждого MR до строчки кода', 'eye'),
    ('Рейтинг', 'Рейтинг сотрудников', 'по компании, стеку и проекту', 'rating'),
    ('Качество', 'ИИ-ревью кода', 'дефекты по тяжести и блокам качества', 'quality'),
    ('Тех-карта', 'Тех-карта проекта', 'технологии, уровни и мэтч команды', 'techmap'),
]

SLIDER_SCRIPT = """class Component extends DCLogic {
  constructor(props) { super(props); this.state = { idx: 0, playing: true }; }
  slidesData() {
    return [
%s
    ];
  }
  reduced() { try { return window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) { return false; } }
  componentDidMount() { if (this.reduced()) this.setState({ playing: false }); else this.start(); }
  componentWillUnmount() { clearInterval(this.timer); }
  start() {
    clearInterval(this.timer);
    this.timer = setInterval(() => this.setState((st) => ({ idx: ((st.idx || 0) + 1) %% 8 })), 4500);
  }
  renderVals() {
    const data = this.slidesData();
    const idx = (this.state && this.state.idx) || 0;
    const slides = data.map((s, i) => Object.assign({}, s, { active: i === idx, inactive: i !== idx, pick: () => { this.setState({ idx: i }); if ((this.state || {}).playing) this.start(); } }));
    const cur = Object.assign({}, data[idx], { num: '0' + (idx + 1) });
    const st = this.state || {};
    return {
      slides, cur, playing: !!st.playing, paused: !st.playing, running: !!st.playing,
      playLabel: st.playing ? 'Остановить автопрокрутку' : 'Включить автопрокрутку',
      togglePlay: () => { if (st.playing) { clearInterval(this.timer); this.setState({ playing: false }); } else { this.start(); this.setState({ playing: true }); } }
    };
  }
}"""

PLAIN_SCRIPT = """class Component extends DCLogic {
  renderVals() { return {}; }
}"""

def page(title, body, height, slider=False, name=None):
    height = HEIGHTS.get(name, height) + (60 if slider else 0)  # консоль со слайдером выше статичного превью
    if slider:
        rows = ',\n'.join("      { key: '%s', title: '%s', caption: '%s', src: '/_blob/%s' }" % (k, t, c, IMG[i][0]) for k, t, c, i in SLIDES)
        script = SLIDER_SCRIPT % rows
    else:
        script = PLAIN_SCRIPT
    root = ('<div style="background: #0D0C15; color: #FFFFFF; font-family: \'Bricolage Grotesque\', \'Onest\', system-ui, sans-serif; '
            'min-height: 100vh; overflow: hidden;">\n%s\n</div>' % body)
    if MODE == 'dc':
        return ('<!doctype html>\n<html lang="ru">\n<head>\n<meta charset="utf-8">\n<title>%s</title>\n<script src="./support.js"></script>\n</head>\n<body>\n<x-dc>\n%s\n%s\n</x-dc>\n'
                '<script type="text/x-dc" data-dc-script data-props=\'{"$preview":{"width":1440,"height":%d}}\'>\n%s\n</script>\n</body>\n</html>\n') % (H.escape(title), HELMET, root, height, script)
    head = HELMET.replace('<helmet>', '').replace('</helmet>', '')
    return '<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>%s</title>%s</head><body>%s</body></html>' % (H.escape(title), head, root)

def header(active=None):
    items = [('Платформа', None), ('Grade', 'grade'), ('AI', 'ai'), ('Projects', 'projects'), ('Mentor', 'mentor'), ('Блог', 'blog')]
    links = []
    for name, key in items:
        on = (key == active) or (active is None and key is None)
        st = ('color: #FFFFFF; background: rgba(255,255,255,0.08); border-radius: 12px;' if on else 'color: rgba(255,255,255,0.78);')
        links.append('<a href="#%s" style="%s text-decoration: none; padding: 10px 14px;">%s</a>' % (key or 'top', st, name))
    return ('<header style="max-width: 1280px; margin: 0 auto; padding: 24px 32px; display: flex; flex-wrap: wrap; align-items: center; gap: 24px; justify-content: space-between;">\n'
            '<a href="#top" aria-label="UpCore — на главную" style="display: flex; align-items: center;"><img src="%s" alt="UpCore" style="height: 28px; width: auto; display: block;"></a>\n'
            '<nav aria-label="Основное меню" style="display: flex; flex-wrap: wrap; gap: 8px; font-size: 15px;">%s</nav>\n'
            '<div style="display: flex; align-items: center; gap: 12px;"><a href="#lang" style="color: rgba(255,255,255,0.78); text-decoration: none; %s font-size: 13px; padding: 10px 8px;">RU / EN</a>'
            '<a href="https://demo.up-core.ru/" style="display: inline-flex; align-items: center; min-height: 44px; padding: 0 20px; border-radius: 14px; background: #63D5FF; color: #0D0C15; font-weight: 700; text-decoration: none; font-size: 15px;">Регистрация</a></div>\n'
            '</header>') % (src('logo'), ''.join(links), MONO)

CHEVRON = '<svg aria-hidden="true" viewBox="0 0 375 645" style="position: absolute; right: -120px; top: -40px; width: 560px; height: auto; opacity: 0.14; filter: blur(2px);"><path fill="#63D5FF" d="M340.243 410.873C322.404 436.777 298.363 465.078 268.118 495.774L166.429 598.984C149.417 616.251 135.926 628.481 125.958 635.674C116.005 643.826 105.711 645.5 95.078 640.695C84.4595 636.849 69.8902 625.803 51.3702 607.556L9.90889 566.705L249.7 322.254L0.000749597 79.9674L43.9849 35.3256C61.4698 17.5791 75.6986 6.54952 86.6712 2.23669C96.6839 -2.07669 106.793 -0.151217 116.998 8.01309C126.716 15.6972 140.347 28.1827 157.893 45.4695L271.54 157.442C294.446 180.011 314.443 200.659 331.531 219.385C348.146 238.591 359.968 258.274 366.999 278.434C373.542 298.114 374.78 322.343 370.134 347.567C365.05 375.17 358.57 385.448 340.243 410.873Z"></path></svg>'

def btn(text, href, primary=True, dark=False):
    if dark:
        st = 'background: #0D0C15; color: #FFFFFF;' if primary else 'border: 1.5px solid #0D0C15; color: #0D0C15;'
    else:
        st = 'background: #63D5FF; color: #0D0C15;' if primary else 'border: 1px solid rgba(255,255,255,0.22); color: #FFFFFF;'
    return ('<a href="%s" style="display: inline-flex; align-items: center; min-height: 52px; padding: 0 28px; border-radius: 16px; %s font-weight: 700; font-size: 17px; text-decoration: none;">%s</a>' % (href, st, e(text)))

REG = 'https://demo.up-core.ru/'
MAIL = 'mailto:office@dex-it.ru'

def stats(items, note=None):
    cells = []
    for i, (big, small) in enumerate(items):
        col = '#63D5FF' if i == 0 else ('#7FDB7A' if big.startswith('+') else '#FFFFFF')
        cells.append('<div style="min-width: 0;"><div style="font-size: clamp(24px, 6.4vw, 34px); font-weight: 800; color: %s; letter-spacing: -0.02em; line-height: 1.1; white-space: nowrap; font-variant-numeric: tabular-nums;">%s</div>'
                     '<div style="font-size: 14px; color: rgba(255,255,255,0.72); line-height: 1.4; margin-top: 4px;">%s</div></div>' % (col, e(big), e(small)))
    cols = 'repeat(2, minmax(0, 1fr))' if len(items) == 4 else 'repeat(auto-fit, minmax(150px, 1fr))'
    out = '<div style="display: grid; grid-template-columns: %s; gap: 18px 20px; border-top: 1px solid rgba(255,255,255,0.12); padding-top: 24px;">%s</div>' % (cols, ''.join(cells))
    if note:
        out += '<div style="%s font-size: 12px; color: rgba(255,255,255,0.55); margin-top: -12px;">%s</div>' % (MONO, e(note))
    return out

# Цифры первых экранов (раунд 8): самые сильные — рост, экономия, деньги. Ориентиры рынка подписаны в note.
HERO_STATS = {
 ('home', 'A'): ([('96%', 'точность от экспертной оценки'), ('1500+', 'разработчиков уже посчитано'),
                  ('+14%', 'рост эффективности разработки за 3 месяца'), ('500 тыс. ₽', 'экономии в год на каждого разработчика')], 'данные и расчёт UpCore'),
 ('home', 'B'): ([('≈9,7 млн ₽', 'в месяц эффекта на 100 разработчиков'), ('+12%', 'производительности сразу'), ('20% → 4%', 'находим, кто съедает ФОТ')], 'данные и расчёт UpCore'),
 ('home', 'C'): ([('100%', 'кода проверено — а не 5–10%'), ('114 ч', 'ручного ревью в месяц экономии'), ('≈1,1 млн ₽', 'в месяц возвращаем времени тимлидов')], 'данные UpCore; расчёт на 100 разработчиков'),
 ('grade', 'A'): ([('96%', 'совпадение с экспертной оценкой'), ('+12%', 'производительности команды сразу'),
                   ('≈5 млн ₽', 'в месяц стоят 20% неэффективных на 100 разработчиков'), ('≈1,1 млн ₽', 'в месяц экономии времени тимлидов')], 'данные и расчёт UpCore'),
 ('grade', 'B'): ([('99%', 'работодателей сталкиваются с накруткой опыта'), ('до 200%', 'годовой зарплаты стоит ошибка найма'), ('3 мес.', 'и реальный грейд подтверждён кодом')], 'Хабр Карьера 2025; SHRM; UpCore'),
 ('grade', 'C'): ([('−210 ч', 'в год на performance review у руководителя'), ('+12%', 'производительности от прозрачных правил'), ('≈1,1 млн ₽', 'в месяц экономии времени тимлидов')], 'CEB / Gartner; данные и расчёт UpCore'),
 ('ai', 'A'): ([('×1,9', 'отдачи на каждый рубль, вложенный в ИИ'), ('−41%', 'расходов на токены'),
                ('+50–100%', 'выработки у Senior с ИИ'), ('+22 п.п.', 'эффективность задач с ИИ — кейс Dex')], 'данные UpCore; ориентиры: Exceeds AI, CodeScene'),
 ('ai', 'B'): ([('−19%', 'реальная скорость с ИИ'), ('+20%', 'ощущаемое ускорение'), ('×1,9', 'отдачи на рубль, когда ИИ мерят по коду')], 'METR, 2025; ориентир: Exceeds AI'),
 ('ai', 'C'): ([('×1,9', 'отдачи на рубль в ИИ'), ('−41%', 'расходов на токены'), ('+19%', 'выработки команды под контролем ИИ')], 'ориентиры: Exceeds AI, CodeScene, Weave'),
 ('projects', 'A'): ([('−75%', 'к оплате по акту — пример аудита'), ('≈19 млн ₽', 'в год переплаты у подрядчика из 10 человек'),
                      ('−50%', 'затрат на сопровождение'), ('2 дня', 'на аудит бюджета проекта')], 'расчёт UpCore; ориентир: SIG'),
 ('projects', 'B'): ([('−120 ч', 'к оплате по одному акту'), ('≈1,6 млн ₽', 'переплаты в месяц на 10 разработчиков'), ('$7 млн', 'возвращено у вендоров')], 'расчёт UpCore; ориентир: BlueOptima'),
 ('projects', 'C'): ([('+45%', 'к бюджету крупных ИТ-проектов'), ('−56%', 'ценности от плана'), ('−75%', 'к оплате находит аудит по коду')], 'McKinsey и Оксфорд; пример UpCore'),
 ('mentor', 'A'): ([('≈1,9 млн ₽', 'в месяц экономии на ревью — 50 разработчиков'), ('−38%', 'времени на код-ревью'),
                    ('×2', 'быстрее онбординг'), ('6,0 → 8,0', 'качество кода после ревью')], 'расчёт и демо UpCore; ориентиры: CodeScene, DX'),
 ('mentor', 'B'): ([('114 ч', 'ручного ревью в месяц экономии'), ('15 мин', 'на критичные MR у лида'), ('×3', 'меньше возвратов из тестирования')], 'демо UpCore; ориентир: Tech Talent Score'),
 ('mentor', 'C'): ([('50% / 67%', 'понимание с ИИ и без'), ('×2', 'быстрее онбординг с наставником'), ('94%', 'остаются, если компания вкладывается в рост')], 'Anthropic 2026; DX; LinkedIn'),
}

def slider_console():
    return """<div style="flex: 1.15 1 520px; min-width: 0; position: relative;">
<div style="border-radius: 24px; background: #12111C; border: 1px solid rgba(99,213,255,0.3); box-shadow: 0 0 0 1px rgba(99,213,255,0.06), 0 40px 120px rgba(99,213,255,0.12); overflow: hidden;">
<div style="display: flex; justify-content: space-between; gap: 12px; flex-wrap: wrap; padding: 14px 18px; border-bottom: 1px solid rgba(255,255,255,0.08); font-family: 'JetBrains Mono', monospace; font-size: 13px; color: rgba(255,255,255,0.72);"><span>upcore://screens / {{cur.key}}</span><span style="color: #63D5FF;">{{cur.num}} / 08</span></div>
<div style="position: relative; aspect-ratio: 16 / 10; background: #FFFFFF; overflow: hidden;">
<sc-for list="{{slides}}" as="s" hint-placeholder-count="1">
<sc-if value="{{s.active}}" hint-placeholder-val="{{true}}"><img class="uc-in" src="{{s.src}}" alt="{{s.title}}" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: top center; display: block;"></sc-if>
</sc-for>
<div class="uc-scan" aria-hidden="true" style="position: absolute; left: 0; right: 0; height: 2px; background: #63D5FF; box-shadow: 0 0 18px 4px rgba(99,213,255,0.6);"></div>
</div>
<div style="padding: 16px 18px; display: flex; flex-direction: column; gap: 12px;">
<div style="display: flex; align-items: center; justify-content: space-between; gap: 12px;"><div style="font-size: 17px; font-weight: 700; min-width: 0;">{{cur.title}} <span style="font-weight: 400; color: rgba(255,255,255,0.72); font-family: 'Onest', sans-serif; font-size: 15px;">— {{cur.caption}}</span></div><button type="button" onClick="{{togglePlay}}" aria-label="{{playLabel}}" style="flex: 0 0 auto; width: 44px; height: 44px; border-radius: 50%; border: 1px solid rgba(255,255,255,0.22); background: transparent; color: #FFFFFF; display: flex; align-items: center; justify-content: center; cursor: pointer;"><sc-if value="{{playing}}" hint-placeholder-val="{{true}}"><svg aria-hidden="true" viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><rect x="6" y="5" width="4" height="14" rx="1"></rect><rect x="14" y="5" width="4" height="14" rx="1"></rect></svg></sc-if><sc-if value="{{paused}}" hint-placeholder-val="{{false}}"><svg aria-hidden="true" viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M8 5v14l11-7z"></path></svg></sc-if></button></div>
<div class="uc-chips" role="tablist" aria-label="Экраны продукта">
<sc-for list="{{slides}}" as="s" hint-placeholder-count="8">
<sc-if value="{{s.active}}" hint-placeholder-val="{{false}}"><button type="button" role="tab" aria-selected="true" onClick="{{s.pick}}" style="position: relative; overflow: hidden; flex: 0 0 auto; white-space: nowrap; min-height: 44px; padding: 0 12px; border-radius: 10px; border: 1px solid #63D5FF; background: rgba(99,213,255,0.12); color: #FFFFFF; font: 600 13px Onest, sans-serif; cursor: pointer;">{{s.key}}<sc-if value="{{running}}" hint-placeholder-val="{{true}}"><span class="uc-prog" style="position: absolute; left: 0; bottom: 0; height: 2px; width: 100%; background: #63D5FF;"></span></sc-if></button></sc-if>
<sc-if value="{{s.inactive}}" hint-placeholder-val="{{true}}"><button type="button" role="tab" aria-selected="false" onClick="{{s.pick}}" style="flex: 0 0 auto; white-space: nowrap; min-height: 44px; padding: 0 12px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.14); background: transparent; color: rgba(255,255,255,0.78); font: 600 13px Onest, sans-serif; cursor: pointer;">{{s.key}}</button></sc-if>
</sc-for>
</div>
</div>
</div>
</div>"""

def static_slider_preview():
    """Для превью: консоль с первым слайдом без шаблонов."""
    k, t, c, i = SLIDES[0]
    return image_console(i, 'screens / ' + k, t, c, None, '01 / 08')

def image_console(img, path, title, caption, acc_key, right=None):
    line, txt = ACC[acc_key]
    right = right or '● онлайн'
    return ('<div style="flex: 1.15 1 520px; min-width: 0; position: relative;">'
            '<div style="border-radius: 24px; background: #12111C; border: 1px solid %s; box-shadow: 0 40px 120px rgba(99,213,255,0.10); overflow: hidden;">'
            '<div style="display: flex; justify-content: space-between; gap: 12px; flex-wrap: wrap; padding: 14px 18px; border-bottom: 1px solid rgba(255,255,255,0.08); %s font-size: 13px; color: rgba(255,255,255,0.72);"><span>upcore://%s</span><span style="color: %s;">%s</span></div>'
            '<div style="position: relative; aspect-ratio: 16 / 10; background: #FFFFFF; overflow: hidden;"><img src="%s" alt="%s" style="position: absolute; inset: 0; width: 100%%; height: 100%%; object-fit: cover; object-position: top center; display: block;">'
            '<div class="uc-scan" aria-hidden="true" style="position: absolute; left: 0; right: 0; height: 2px; background: %s; box-shadow: 0 0 18px 4px rgba(99,213,255,0.5);"></div></div>'
            '<div style="padding: 16px 18px; font-size: 17px; font-weight: 700;">%s <span style="font-weight: 400; color: rgba(255,255,255,0.72); font-family: \'Onest\', sans-serif; font-size: 15px;">— %s</span></div>'
            '</div></div>') % (line + '66' if line.startswith('#') else line, MONO, e(path), txt, e(right), src(img), e(title), line, e(title), e(caption))

def hero(badge, h1, sub, ctas, stat_items, visual, note=None, acc_key=None, h1_size='clamp(38px, 4.4vw, 64px)'):
    line, txt = ACC[acc_key]
    dot = '#53C04D'
    if len(h1.replace('[[', '').replace(']]', '')) > 60:  # длинный заголовок — мельче, чтобы уложился в ~4 строки
        h1_size = 'clamp(34px, 3.5vw, 50px)'
    return ('<section id="top" style="position: relative; max-width: 1280px; margin: 0 auto; padding: 48px 32px 96px; display: flex; flex-wrap: wrap; gap: 56px; align-items: center;">\n%s\n'
            '<div style="flex: 1 1 500px; min-width: 0; position: relative; display: flex; flex-direction: column; gap: 28px;">\n'
            '<div style="display: inline-flex; align-self: flex-start; align-items: center; gap: 10px; padding: 8px 14px; border-radius: 999px; border: 1px solid %s; %s font-size: 13px; color: %s;"><span class="uc-blink" style="width: 8px; height: 8px; border-radius: 50%%; background: %s; display: inline-block;"></span><span>%s</span></div>\n'
            '<h1 style="margin: 0; font-size: %s; line-height: 1.03; letter-spacing: -0.03em; font-weight: 800;">%s</h1>\n'
            '<p style="margin: 0; font-size: clamp(17px, 1.35vw, 20px); line-height: 1.55; color: rgba(255,255,255,0.8); max-width: 600px;">%s</p>\n'
            '<div style="display: flex; flex-wrap: wrap; gap: 12px;">%s</div>\n%s\n</div>\n%s\n</section>') % (
        CHEVRON, line + '59', MONO, txt, dot, e(badge), h1_size, e(h1), e(sub), ''.join(ctas), stats(stat_items, note), visual)

def sec_head(label, h2, lead=None, acc_key=None):
    _, txt = ACC[acc_key]
    out = '<div style="%s font-size: 13px; color: %s; margin-bottom: 14px; letter-spacing: 0.04em;">%s</div>' % (MONO, txt, e(label))
    if lead:
        out += ('<div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: flex-end; gap: 24px; margin-bottom: 40px;">'
                '<h2 style="margin: 0; font-size: clamp(32px, 3.4vw, 52px); letter-spacing: -0.03em; line-height: 1.05; font-weight: 800; max-width: 760px;">%s</h2>'
                '<p style="margin: 0; max-width: 420px; color: rgba(255,255,255,0.74); font-size: 17px; line-height: 1.55;">%s</p></div>') % (e(h2), e(lead))
    else:
        out += '<h2 style="margin: 0 0 40px; font-size: clamp(32px, 3.4vw, 52px); letter-spacing: -0.03em; line-height: 1.05; font-weight: 800; max-width: 900px;">%s</h2>' % e(h2)
    return out

def section(inner, sid=None, pb=96):
    return '<section %sstyle="max-width: 1280px; margin: 0 auto; padding: 0 32px %dpx;">\n%s\n</section>' % (('id="%s" ' % sid) if sid else '', pb, inner)

def card(inner, pad='28px', bg='#1A1925', border='rgba(255,255,255,0.08)', gap=14):
    return ('<article style="min-width: 0; border-radius: 24px; background: %s; border: 1px solid %s; padding: %s; display: flex; flex-direction: column; gap: %dpx;">%s</article>' % (bg, border, pad, gap, inner))

def src_line(t):
    return '<div style="margin-top: auto; %s font-size: 12px; color: rgba(255,255,255,0.55); line-height: 1.4;">%s</div>' % (MONO, e(t)) if t else ''

def pains(label, h2, items, acc_key=None, lead=None):
    _, txt = ACC[acc_key]
    cards = []
    for big, text, s in items:
        cards.append(card('<div style="font-size: clamp(34px, 3vw, 46px); font-weight: 800; letter-spacing: -0.03em; line-height: 1; color: %s;">%s</div>'
                          '<p style="margin: 0; color: rgba(255,255,255,0.84); font-size: 16px; line-height: 1.5;">%s</p>%s' % (txt, e(big), e(text), src_line(s))))
    return section(sec_head(label, h2, lead, acc_key) + '<div class="g4">%s</div>' % ''.join(cards))

def text_pains(label, h2, items, lead=None):
    cards = [card('<div style="font-size: 21px; font-weight: 700; line-height: 1.25;">%s</div><p style="margin: 0; color: %s; font-size: 16px; line-height: 1.55;">%s</p>%s' % (e(t), DIM, e(p), src_line(s))) for t, p, s in items]
    return section(sec_head(label, h2, lead) + '<div class="g4">%s</div>' % ''.join(cards))

def modules(label, h2, items, acc_key=None, lead=None, cols='g3'):
    _, txt = ACC[acc_key]
    cards = []
    for i, (t, p) in enumerate(items, 1):
        cards.append(card('<div style="%s font-size: 13px; color: %s;">%02d</div><div style="font-size: 21px; font-weight: 700; line-height: 1.25;">%s</div>'
                          '<p style="margin: 0; color: %s; font-size: 16px; line-height: 1.55;">%s</p>' % (MONO, txt, i, e(t), DIM, e(p))))
    return section(sec_head(label, h2, lead, acc_key) + '<div class="%s">%s</div>' % (cols, ''.join(cards)))

def roles(label, h2, items, acc_key=None):
    _, txt = ACC[acc_key]
    cards = [card('<div style="%s font-size: 13px; color: %s;">%s</div><p style="margin: 0; color: rgba(255,255,255,0.86); font-size: 17px; line-height: 1.55;">%s</p>' % (MONO, txt, e(r.upper()), e(p))) for r, p in items]
    return section(sec_head(label, h2, None, acc_key) + '<div class="g4">%s</div>' % ''.join(cards))

def faq(items, h2='Честные ответы на неудобные вопросы', acc_key=None):
    cards = [card('<div style="font-size: 20px; font-weight: 700; line-height: 1.3;">%s</div><p style="margin: 0; color: %s; font-size: 16px; line-height: 1.6;">%s</p>' % (e(q), DIM, e(a)), pad='28px 30px') for q, a in items]
    return section(sec_head('ВОПРОСЫ', h2, None, acc_key) + '<div class="g2">%s</div>' % ''.join(cards))

def compare(label, h2, left_title, left, right_title, right, lead=None, acc_key=None):
    def col(title, items, good):
        mark = '<span style="color: %s; font-weight: 800; margin-right: 10px;">%s</span>' % (('#7FDB7A', '✓') if good else ('#F08A8A', '✕'))
        lis = ''.join('<li style="display: flex; padding: 12px 0; border-top: 1px solid rgba(255,255,255,0.07); font-size: 17px; line-height: 1.45;">%s<span>%s</span></li>' % (mark, e(i)) for i in items)
        bg = 'rgba(99,213,255,0.07)' if good else '#1A1925'
        bd = 'rgba(99,213,255,0.4)' if good else 'rgba(255,255,255,0.08)'
        return card('<div style="font-size: 22px; font-weight: 800;">%s</div><ul style="margin: 0; padding: 0; list-style: none;">%s</ul>' % (e(title), lis), pad='32px', bg=bg, border=bd)
    return section(sec_head(label, h2, lead, acc_key) + '<div class="g2">%s%s</div>' % (col(left_title, left, False), col(right_title, right, True)))

def steps(label, h2, items, acc_key=None, highlight_last=True):
    _, txt = ACC[acc_key]
    cells = []
    for i, (k, t, p) in enumerate(items):
        last = highlight_last and i == len(items) - 1
        st = 'background: rgba(99,213,255,0.08); border: 1px solid rgba(99,213,255,0.4);' if last else 'border: 1px solid rgba(255,255,255,0.1);'
        cells.append('<div style="min-width: 0; border-radius: 20px; %s padding: 24px;"><div style="%s color: %s; font-size: 13px;">%s</div><div style="font-size: 21px; font-weight: 700; margin: 10px 0 8px;">%s</div><div style="color: rgba(255,255,255,0.74); font-size: 15px; line-height: 1.55;">%s</div></div>' % (st, MONO, txt, e(k), e(t), e(p)))
    cls = 'g4' if len(items) == 4 else 'g3'
    return section(sec_head(label, h2, None, acc_key) + '<div class="%s">%s</div>' % (cls, ''.join(cells)))

def method_block(h2, step_items, big, big_cap, paras, note=None):
    cells = ''.join('<div style="min-width: 0; border-radius: 20px; %s padding: 24px;"><div style="%s color: #63D5FF; font-size: 13px;">%s</div><div style="font-size: 21px; font-weight: 700; margin: 10px 0 8px;">%s</div><div style="color: rgba(255,255,255,0.74); font-size: 15px; line-height: 1.55;">%s</div></div>' % (
        ('background: rgba(99,213,255,0.08); border: 1px solid rgba(99,213,255,0.4);' if i == len(step_items) - 1 else 'border: 1px solid rgba(255,255,255,0.1);'), MONO, e(k), e(t), e(p)) for i, (k, t, p) in enumerate(step_items))
    ps = ''.join('<p style="margin: 0;">%s</p>' % e(p) for p in paras)
    n = ('<div style="%s font-size: 12px; color: rgba(255,255,255,0.55); line-height: 1.5;">%s</div>' % (MONO, e(note))) if note else ''
    inner = ('<div style="border-radius: 40px; background: #12111C; border: 1px solid rgba(255,255,255,0.08); padding: clamp(28px, 4vw, 56px); display: flex; flex-direction: column; gap: 40px;">'
             '<h2 style="margin: 0; font-size: clamp(30px, 3vw, 46px); letter-spacing: -0.03em; font-weight: 800; max-width: 860px; line-height: 1.08;">%s</h2>'
             '<div class="g4">%s</div>'
             '<div style="display: flex; flex-wrap: wrap; gap: 40px; align-items: center; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 40px;">'
             '<div style="flex: 0 1 auto;"><div style="font-size: clamp(80px, 10vw, 152px); font-weight: 800; color: #63D5FF; line-height: 0.9; letter-spacing: -0.04em;">%s</div><div style="font-size: 20px; color: rgba(255,255,255,0.85); margin-top: 8px;">%s</div></div>'
             '<div style="flex: 1 1 420px; min-width: 0; display: flex; flex-direction: column; gap: 14px; font-size: 17px; line-height: 1.55; color: rgba(255,255,255,0.82);">%s%s</div>'
             '</div></div>') % (e(h2), cells, e(big), e(big_cap), ps, n)
    return section(inner, 'method')

def effect(label, h2, items, lead=None):
    cells = ''.join(card('<div style="font-size: clamp(40px, 4vw, 60px); font-weight: 800; letter-spacing: -0.03em; line-height: 1; color: %s;">%s</div><p style="margin: 0; color: rgba(255,255,255,0.84); font-size: 16px; line-height: 1.5;">%s</p>%s' % (
        '#7FDB7A' if big.startswith('+') else '#FFFFFF', e(big), e(t), src_line(s))) for big, t, s in items)
    return section(sec_head(label, h2, lead) + '<div class="g4">%s</div>' % cells)


def kpi(label, h2, tiles, acc_key=None, calc=None, lead=None, note=None):
    """Плитки бизнес-показателей (как у Tech Talent Score) + необязательная карточка расчёта.
    tiles: [(big, text, src)]; calc: (title, [(label, value)], (total_label, total_value), footnote)"""
    _, txt = ACC[acc_key]
    cells = []
    for big, text, s in tiles:
        col = '#7FDB7A' if big.startswith('+') else txt
        cells.append(card('<div style="font-size: clamp(32px, 3vw, 46px); font-weight: 800; letter-spacing: -0.03em; line-height: 1.05; color: %s; font-variant-numeric: tabular-nums; white-space: nowrap;">%s</div>'
                          '<p style="margin: 0; color: rgba(255,255,255,0.86); font-size: 16px; line-height: 1.5;">%s</p>%s' % (col, e(big), e(text), src_line(s)), pad='26px'))
    cls = 'g4' if len(tiles) % 4 == 0 else 'g3'
    out = sec_head(label, h2, lead, acc_key) + '<div class="%s">%s</div>' % (cls, ''.join(cells))
    if calc:
        title, rows, total, foot = calc
        lines = ''.join('<div style="display: flex; justify-content: space-between; gap: 16px; padding: 14px 0; border-top: 1px solid rgba(255,255,255,0.08); font-size: 17px; line-height: 1.4;"><span style="color: rgba(255,255,255,0.84);">%s</span><b style="white-space: nowrap; font-variant-numeric: tabular-nums;">%s</b></div>' % (e(a), e(b)) for a, b in rows)
        tot = ('<div style="display: flex; justify-content: space-between; gap: 16px; padding: 18px 0 0; border-top: 2px solid %s; font-size: 22px; font-weight: 800;"><span>%s</span><span style="color: %s; white-space: nowrap; font-variant-numeric: tabular-nums;">%s</span></div>' % (txt, e(total[0]), txt, e(total[1])))
        out += ('<div style="margin-top: 16px; border-radius: 28px; background: #12111C; border: 1px solid rgba(255,255,255,0.1); padding: clamp(24px, 3vw, 40px); display: flex; flex-wrap: wrap; gap: 32px;">'
                '<div style="flex: 1 1 280px; min-width: 0;"><div style="%s font-size: 13px; color: %s; margin-bottom: 10px;">РАСЧЁТ</div><div style="font-size: clamp(24px, 2.2vw, 32px); font-weight: 800; line-height: 1.15;">%s</div>'
                '<p style="margin: 14px 0 0; color: rgba(255,255,255,0.62); font-size: 14px; line-height: 1.5;">%s</p></div>'
                '<div style="flex: 1.4 1 420px; min-width: 0;">%s%s</div></div>') % (MONO, txt, e(title), e(foot), lines, tot)
    if note:
        out += '<div style="margin-top: 14px; %s font-size: 12px; color: rgba(255,255,255,0.55);">%s</div>' % (MONO, e(note))
    return section(out, 'effect')

CALC_100 = ('Эффект на команду из 100 разработчиков',
            [('Закрываем «дыру» 20% неэффективных', '≈5,0 млн ₽'), ('+12% к выработке остальных — от прозрачности', '≈3,6 млн ₽'), ('400 ч тимлидов в месяц освобождаются от ручной оценки', '≈1,1 млн ₽')],
            ('Итого в месяц', '≈9,7 млн ₽'),
            'Допущения: 100 разработчиков, затраты 300 тыс. ₽ в месяц на человека (ФОТ 30 млн ₽), ставка тимлида 450 тыс. ₽. Даже при 30% реализации — ≈2,9 млн ₽ в месяц.')

def results(key):
    """Блок «Результаты для бизнеса» (как «Результаты внедрения» у Tech Talent Score): главная цифра, 8 плиток, расчёт.
    Цифры — направления смыслов: UpCore + ориентиры конкурентов (подписаны); владелец заменит на реальные."""
    d = RESULTS[key]
    acc = None if key == 'home' else key
    line, txt = ACC[acc]
    big, text, subs = d['head']
    sub_html = ''.join('<div style="min-width: 0;"><div style="font-size: clamp(26px, 2.4vw, 36px); font-weight: 800; letter-spacing: -0.02em; color: #FFFFFF; white-space: nowrap; font-variant-numeric: tabular-nums;">%s</div>'
                       '<div style="font-size: 14px; color: rgba(255,255,255,0.7); line-height: 1.4; margin-top: 4px;">%s</div></div>' % (e(n), e(l)) for n, l in subs)
    banner = ('<div style="border-radius: 32px; background: #12111C; border: 1px solid %s; box-shadow: inset 0 0 120px rgba(99,213,255,0.06); padding: clamp(28px, 4vw, 48px); display: flex; flex-wrap: wrap; gap: 32px 48px; align-items: center; margin-bottom: 16px;">'
              '<div style="flex: 1.2 1 420px; min-width: 0;"><div style="font-size: clamp(56px, 7vw, 104px); font-weight: 800; letter-spacing: -0.04em; line-height: 0.95; color: %s; font-variant-numeric: tabular-nums;">%s</div>'
              '<p style="margin: 16px 0 0; font-size: clamp(18px, 1.5vw, 22px); line-height: 1.45; color: rgba(255,255,255,0.88); max-width: 560px;">%s</p></div>'
              '<div class="g3" style="flex: 1 1 420px; min-width: 0; gap: 20px;">%s</div></div>') % (line + '73', txt, e(big), e(text), sub_html)
    tiles = []
    for b, l, s in d['tiles']:
        col = '#7FDB7A' if b.startswith('+') else txt
        tiles.append(card('<div style="font-size: clamp(30px, 2.7vw, 42px); font-weight: 800; letter-spacing: -0.03em; line-height: 1.05; color: %s; white-space: nowrap; font-variant-numeric: tabular-nums;">%s</div>'
                          '<p style="margin: 0; color: rgba(255,255,255,0.86); font-size: 15px; line-height: 1.5;">%s</p>%s' % (col, e(b), e(l), src_line(s)), pad='24px', gap=10))
    out = sec_head('РЕЗУЛЬТАТЫ ДЛЯ БИЗНЕСА', d['h2'], d.get('lead'), acc) + banner + '<div class="g4">%s</div>' % ''.join(tiles)
    if d.get('calc'):
        title, rows, total, foot = d['calc']
        lines = ''.join('<div style="display: flex; justify-content: space-between; gap: 16px; padding: 14px 0; border-top: 1px solid rgba(255,255,255,0.08); font-size: 17px; line-height: 1.4;"><span style="color: rgba(255,255,255,0.84);">%s</span><b style="white-space: nowrap; font-variant-numeric: tabular-nums;">%s</b></div>' % (e(a), e(b)) for a, b in rows)
        tot = ('<div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 8px 16px; padding: 18px 0 0; border-top: 2px solid %s; font-size: 22px; font-weight: 800;"><span>%s</span><span style="color: %s; font-variant-numeric: tabular-nums;">%s</span></div>' % (txt, e(total[0]), txt, e(total[1])))
        out += ('<div style="margin-top: 16px; border-radius: 28px; background: #12111C; border: 1px solid rgba(255,255,255,0.1); padding: clamp(24px, 3vw, 40px); display: flex; flex-wrap: wrap; gap: 32px;">'
                '<div style="flex: 1 1 280px; min-width: 0;"><div style="%s font-size: 13px; color: %s; margin-bottom: 10px;">РАСЧЁТ</div><div style="font-size: clamp(24px, 2.2vw, 32px); font-weight: 800; line-height: 1.15;">%s</div>'
                '<p style="margin: 14px 0 0; color: rgba(255,255,255,0.62); font-size: 14px; line-height: 1.5;">%s</p></div>'
                '<div style="flex: 1.4 1 420px; min-width: 0;">%s%s</div></div>') % (MONO, txt, e(title), e(foot), lines, tot)
    out += '<div style="margin-top: 14px; %s font-size: 12px; color: rgba(255,255,255,0.5);">Цифры — направления смыслов: данные UpCore и ориентиры рынка; перед публикацией заменить на подтверждённые показатели UpCore.</div>' % MONO
    return section(out, 'results')

U = 'UpCore'
RESULTS = {
 'home': dict(h2='Что получает бизнес — в цифрах, процентах и рублях',
   lead='Платформа окупается в десятки раз: эффект виден уже в первый месяц — по истории вашего кода.',
   head=('≈500 тыс. ₽', 'экономического эффекта в год на каждого разработчика — с первых месяцев работы платформы',
         [('≈9,7 млн ₽', 'в месяц на команду из 100 разработчиков'), ('×10+', 'окупаемость вложений в платформу'), ('1 месяц', 'до первых решений на данных')]),
   tiles=[('+14%', 'эффективность разработки за 3 месяца', U), ('+12%', 'производительность команды сразу после запуска', U),
          ('до +30%', 'рост эффективности разработки за счёт контроля продуктивности', 'ориентир: Tech Talent Score'), ('−20%', 'time-to-market: потери в процессах становятся видны', 'ориентир: Tech Talent Score'),
          ('×2', 'скорость доставки обновлений', 'ориентир: Tech Talent Score'), ('−30%', 'времени на непродуктивные задачи', 'ориентир: KODA'),
          ('2,5 ставки', 'тимлидов на каждые 100 разработчиков освобождается от ручной оценки', U), ('−20–30%', 'дефектов, которые находят клиенты', 'ориентир: McKinsey')],
   calc=('Эффект на команду из 100 разработчиков',
         [('Закрываем «дыру» 20% неэффективных', '≈5,0 млн ₽'), ('+12% к выработке остальных — от прозрачности', '≈3,6 млн ₽'), ('400 ч тимлидов в месяц освобождаются от ручной оценки', '≈1,1 млн ₽')],
         ('Итого в месяц', '≈9,7 млн ₽'), 'Допущения: 100 разработчиков, затраты 300 тыс. ₽ в месяц на человека (ФОТ 30 млн ₽), ставка тимлида 450 тыс. ₽. Даже при 30% реализации — ≈2,9 млн ₽ в месяц.')),
 'grade': dict(h2='Объективная оценка людей — это прямые деньги',
   head=('≈5 млн ₽', 'в месяц теряет компания на 100 разработчиков из-за 20% неэффективных — Grade делает их видимыми',
         [('+12%', 'производительности сразу'), ('−210 ч', 'в год на ревью у руководителя'), ('3 мес.', 'до подтверждённого грейда')]),
   tiles=[('+12%', 'производительность команды от прозрачной оценки', U), ('до +30%', 'рост эффективности при контроле продуктивности', 'ориентир: Tech Talent Score'),
          ('+18%', 'продуктивность разработчиков после внедрения объективных метрик', 'ориентир: BlueOptima, DSK Bank'), ('−9,5%', 'ФОТ «инженеров-призраков», которые почти не создают результат', 'ориентир: Стэнфорд'),
          ('≈1,1 млн ₽', 'в месяц экономии времени тимлидов на 100 разработчиков (400 ч)', U), ('−210 ч', 'в год на performance review у каждого руководителя', 'ориентир: CEB / Gartner'),
          ('−202 тыс. ₽', 'потерь в месяц на одном разработчике в красной зоне — теперь видно сразу', U), ('до 200%', 'годовой зарплаты стоит ошибка найма — ловим её на испытательном сроке', 'ориентир: SHRM')],
   calc=('Эффект Grade на команду из 100 разработчиков',
         [('20% неэффективных: ротация, обучение или расставание', '≈5,0 млн ₽'), ('+12% выработки от прозрачных правил', '≈3,6 млн ₽'), ('Оценка и performance review без ручной работы тимлидов', '≈1,1 млн ₽')],
         ('Итого в месяц', '≈9,7 млн ₽'), 'Допущения: 100 разработчиков, 300 тыс. ₽ в месяц на человека, ставка тимлида 450 тыс. ₽.')),
 'ai': dict(h2='Каждый рубль на ИИ — с понятной отдачей',
   head=('×1,9', 'отдачи на каждый рубль, вложенный в ИИ-инструменты, когда лицензии и обучение идут туда, где есть эффект',
         [('+50–100%', 'выработки у Senior с ИИ'), ('−41%', 'расходов на токены'), ('0 мес.', 'до отчёта «до и после»')]),
   tiles=[('+50–100%', 'выработка Senior-разработчиков с ИИ', U), ('+22 п.п.', 'эффективность задач с ИИ против ручных — кейс Dex', U),
          ('−41%', 'расходы на токены у команд, следящих за качеством кода', 'ориентир: CodeScene'), ('+19%', 'измеренная выработка команды после контроля ИИ', 'ориентир: Weave'),
          ('−30%', 'время цикла задач у команд, где ИИ пишет большую часть кода', 'ориентир: Jellyfish, Loadsmart'), ('−38%', 'времени на ревью ИИ-кода', 'ориентир: CodeScene'),
          ('до −50%', 'выработки у Junior с ИИ — UpCore показывает, где ИИ вредит', U), ('×1,9', 'отдача на вложенный рубль с учётом качества кода', 'ориентир: Exceeds AI')],
   calc=('Куда направить бюджет на ИИ', [('Senior + ИИ', '+50–100%'), ('Middle + ИИ', '0…+20%'), ('Junior + ИИ', 'до −50%')], ('Лицензии и обучение', 'по отдаче'),
         'Один и тот же инструмент даёт разный результат: UpCore показывает отдачу по каждому человеку и команде, чтобы бюджет на ИИ не делили «на всех поровну».')),
 'projects': dict(h2='Контроль по коду возвращает бюджет',
   head=('−75%', 'к оплате по акту подрядчика в примере аудита: выставлено 160 часов, объективно по коду — 40',
         [('$7 млн', 'возвращено у вендоров'), ('−50%', 'затрат на сопровождение'), ('2 дня', 'на аудит проекта')]),
   tiles=[('−75%', 'к оплате по акту в примере аудита', U), ('$7 млн', 'кредитов от вендоров: метрики выявили 250 неактивных разработчиков', 'ориентир: BlueOptima'),
          ('$2 млн', 'в год экономии: −40% in-house команды без потери продуктивности', 'ориентир: BlueOptima'), ('−50%', 'затраты на сопровождение после снижения техдолга', 'ориентир: SIG'),
          ('+30%', 'мощности команды высвобождается', 'ориентир: SIG'), ('×4,5', 'быстрее выход на рынок после снижения техдолга', 'ориентир: SIG'),
          ('−45%', 'перерасхода бюджета — столько в среднем теряют крупные ИТ-проекты', 'ориентир: McKinsey'), ('2 дня', 'на аудит бюджета проекта по коду', U)],
   calc=('Подрядчик из 10 разработчиков', [('Часов в актах за месяц', '1 600 ч'), ('Стоимость при ставке 2 500 ₽/ч', '4,0 млн ₽'), ('Объективно по коду при эффективности 60%', '960 ч')],
         ('Переплата в месяц', '≈1,6 млн ₽'), 'Пример расчёта: ставку и эффективность подставьте свои — UpCore посчитает их по вашему коду. За год — ≈19 млн ₽.')),
 'mentor': dict(h2='Наставник для каждого — и время старших инженеров возвращается в разработку',
   head=('≈1,9 млн ₽', 'в месяц экономии на ревью для команды из 50 разработчиков — по часу на каждый MR',
         [('−38%', 'времени на код-ревью'), ('×2', 'быстрее онбординг'), ('6,0 → 8,0', 'качество кода')]),
   tiles=[('114 ч', 'ручного ревью в месяц экономит авто-ревью, +228 тыс. ₽', 'UpCore, демо'), ('~1 ч', 'экономии на каждом MR с ИИ-ревью', 'ориентир: Qodo'),
          ('−30%', 'циклов ревью, +70% к скорости мёржа', 'ориентир: CodeRabbit, Swiggy'), ('−38%', 'времени на код-ревью', 'ориентир: CodeScene'),
          ('×2', 'быстрее новички проходят вехи онбординга', 'ориентир: DX'), ('×3', 'меньше возвратов из тестирования', 'ориентир: Tech Talent Score'),
          ('6,0 → 8,0', 'качество кода по ревью после исправлений', 'UpCore, демо'), ('94%', 'сотрудников остаются дольше, если компания вкладывается в их рост', 'ориентир: LinkedIn')],
   calc=('Команда из 50 разработчиков', [('MR в месяц', '≈1 000'), ('Экономия ревью на MR', '≈1 ч'), ('Стоимость часа инженера (300 тыс. ₽ в месяц)', '≈1 900 ₽')],
         ('Экономия в месяц', '≈1,9 млн ₽'), 'Пример расчёта: подставьте число MR и стоимость часа вашей команды.')),
}

# ---------------------------------------------------------------- раунд 25: «Результаты для бизнеса» — варианты для C-level
RES_FOOT = 'Допущения: 100 разработчиков, полные затраты 300 тыс. ₽ в месяц на человека (ФОТ разработки 30 млн ₽), ставка тимлида 450 тыс. ₽. Цифры — ориентиры, перед публикацией заменить на подтверждённые показатели UpCore.'
RES_PARTS = [('Видно, кто не даёт результата: 20% неэффективных', 5.0, '#63D5FF'), ('Прозрачность: +12% к выработке остальных', 3.6, '#7FDB7A'), ('Тимлиды освобождаются от ручной оценки: 400 ч', 1.1, '#B9AEFF')]

def res_label():
    return '<div style="%s font-size: 13px; color: #63D5FF; margin-bottom: 14px; letter-spacing: 0.04em;">РЕЗУЛЬТАТЫ ДЛЯ БИЗНЕСА</div>' % MONO

def res_foot(t=RES_FOOT):
    return '<p style="margin: 0; %s font-size: 12px; line-height: 1.6; color: rgba(255,255,255,0.5);">%s</p>' % (MONO, e(t))

def stat_row(items, cls='g4'):
    return '<div class="%s" style="gap: 24px;">%s</div>' % (cls, ''.join(
        '<div style="min-width: 0;"><div style="font-size: clamp(28px, 2.6vw, 40px); font-weight: 800; letter-spacing: -0.02em; white-space: nowrap; color: %s; font-variant-numeric: tabular-nums;">%s</div>'
        '<div style="font-size: 15px; color: rgba(255,255,255,0.72); margin-top: 4px; line-height: 1.4;">%s</div></div>' % (c, e(a), e(b)) for a, b, c in items))

PROOFS = [('+12%', 'производительности сразу после запуска — эффект прозрачности', '#7FDB7A'), ('+14%', 'эффективности разработки за 3 месяца', '#7FDB7A'),
          ('1 месяц', 'до первых решений — по истории вашего Git', '#FFFFFF'), ('0 ₽', 'за пилот: платите после того, как подтвердите точность', '#FFFFFF')]

def results_variant(n):
    if n == 1:
        return results('home')
    box = 'border-radius: 40px; background: #12111C; border: 1px solid rgba(255,255,255,0.08); padding: clamp(28px, 4vw, 56px); display: flex; flex-direction: column; gap: 36px;'
    h2st = 'margin: 0; font-size: clamp(32px, 3.6vw, 56px); letter-spacing: -0.03em; line-height: 1.04; font-weight: 800;'
    if n == 2:  # «Одна цифра»: ≈9,7 млн ₽ в месяц, из чего она складывается, 4 доказательства
        total = sum(v for _, v, _ in RES_PARTS)
        bar = ''.join('<div style="flex: %s 1 0; min-width: 0; height: 100%%; background: %s;"></div>' % (v, c) for _, v, c in RES_PARTS)
        legend = ''.join('<div style="display: flex; gap: 12px; align-items: baseline; justify-content: space-between; padding: 12px 0; border-top: 1px solid rgba(255,255,255,0.08);">'
                         '<span style="display: flex; gap: 10px; align-items: baseline; min-width: 0; color: rgba(255,255,255,0.86); font-size: 16px; line-height: 1.4;"><span style="flex: 0 0 auto; width: 10px; height: 10px; border-radius: 3px; background: %s;"></span>%s</span>'
                         '<b style="white-space: nowrap; font-size: 18px; font-variant-numeric: tabular-nums;">≈%s млн ₽</b></div>' % (c, e(l), ('%.1f' % v).replace('.', ',')) for l, v, c in RES_PARTS)
        inner = ('<div style="%s">'
                 '<div style="display: flex; flex-wrap: wrap; gap: 32px 56px; align-items: flex-end;">'
                 '<div style="flex: 1.2 1 520px; min-width: 0;">%s<h2 style="%s">UpCore возвращает до трети ФОТ разработки</h2>'
                 '<p style="margin: 16px 0 0; font-size: clamp(17px, 1.4vw, 20px); line-height: 1.55; color: rgba(255,255,255,0.84); max-width: 640px;">Деньги, которые сейчас уходят в работу без результата, становятся видны — и возвращаются в разработку. Без найма, без новых процессов, с первого месяца.</p></div>'
                 '<div style="flex: 1 1 360px; min-width: 0;"><div style="font-size: clamp(52px, 6.2vw, 92px); font-weight: 800; letter-spacing: -0.045em; line-height: 0.9; color: #63D5FF; white-space: nowrap; font-variant-numeric: tabular-nums;">≈9,7 млн ₽</div>'
                 '<div style="font-size: 19px; color: rgba(255,255,255,0.88); margin-top: 12px;">в месяц на команду из 100 разработчиков</div>'
                 '<div style="font-size: 15px; color: rgba(255,255,255,0.62); margin-top: 6px;">≈116 млн ₽ в год · это 32%% ФОТ разработки</div></div></div>'
                 '<div><div style="display: flex; gap: 3px; height: 14px; border-radius: 8px; overflow: hidden; margin-bottom: 8px;">%s</div>%s</div>'
                 '<div style="border-top: 1px solid rgba(255,255,255,0.08); padding-top: 32px;">%s</div>%s</div>') % (
                     box, res_label(), h2st, bar, legend, stat_row(PROOFS), res_foot())
        return section(inner, 'results')
    if n == 3:  # «Найдите свою компанию»: эффект по размеру команды + консервативный сценарий
        rows = [(50, '15 млн ₽', '≈4,9 млн ₽', '≈58 млн ₽', '≈17 млн ₽'), (100, '30 млн ₽', '≈9,7 млн ₽', '≈116 млн ₽', '≈35 млн ₽'),
                (300, '90 млн ₽', '≈29 млн ₽', '≈349 млн ₽', '≈105 млн ₽'), (1000, '300 млн ₽', '≈97 млн ₽', '≈1,16 млрд ₽', '≈349 млн ₽')]
        heads = ['Разработчиков', 'ФОТ разработки в месяц', 'Эффект в месяц', 'Эффект в год', 'Даже при 30% реализации, в год']
        th = ''.join('<th scope="col" style="text-align: left; padding: 0 16px 12px 0; %s font-size: 12px; font-weight: 400; color: %s;">%s</th>' % (MONO, '#63D5FF' if i == 3 else 'rgba(255,255,255,0.55)', e(h).upper()) for i, h in enumerate(heads))
        trs = ''
        for i, (nn, fot, m, y, c) in enumerate(rows):
            hi = nn == 100
            td = 'padding: 16px 16px 16px 0; border-top: 1px solid rgba(255,255,255,0.08); font-variant-numeric: tabular-nums; vertical-align: baseline;'
            ml = lambda t: '<span class="uc-ml">%s</span>' % e(t)
            trs += ('<tr style="%s"><th scope="row" style="%s text-align: left; font-size: 22px; font-weight: 800;">%s<span class="uc-ml" style="display: none;"> разработчиков</span></th><td style="%s color: rgba(255,255,255,0.72); font-size: 17px;">%s%s</td>'
                    '<td style="%s font-size: 19px; font-weight: 700;">%s%s</td><td style="%s font-size: clamp(20px, 2vw, 28px); font-weight: 800; color: #63D5FF; white-space: nowrap;">%s%s</td><td style="%s color: rgba(255,255,255,0.8); font-size: 17px;">%s%s</td></tr>') % (
                        'background: rgba(99,213,255,0.06);' if hi else '', td, '{:,}'.format(nn).replace(',', ' '), td, ml('ФОТ в месяц'), fot, td, ml('эффект в месяц'), m, td, ml('эффект в год'), y, td, ml('при 30% реализации'), c)
        table = '<div style="overflow-x: auto;"><table class="uc-res" style="width: 100%%; border-collapse: collapse;"><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (th, trs)
        inner = ('<div style="%s">'
                 '<div style="display: flex; flex-wrap: wrap; gap: 24px 56px; align-items: flex-end; justify-content: space-between;">'
                 '<div style="flex: 1.3 1 560px; min-width: 0;">%s<h2 style="%s">Каждый разработчик приносит ≈1,2 млн ₽ эффекта в год</h2></div>'
                 '<p style="flex: 1 1 320px; margin: 0; font-size: 17px; line-height: 1.55; color: rgba(255,255,255,0.78);">Эффект растёт вместе с командой. Найдите свою компанию в таблице — а точную цифру UpCore посчитает по истории вашего кода за первый месяц.</p></div>'
                 '%s<div style="border-top: 1px solid rgba(255,255,255,0.08); padding-top: 32px;">%s</div>%s</div>') % (
                     box, res_label(), h2st, table, stat_row(PROOFS), res_foot('Расчёт: эффект ≈97 тыс. ₽ в месяц на разработчика (−20% потерь на неэффективности, +12% от прозрачности, время тимлидов) при затратах 300 тыс. ₽ в месяц на человека. Цифры — ориентиры, перед публикацией заменить на подтверждённые.'))
        return section(inner, 'results')
    # n == 4: «Четыре решения — четыре статьи экономии»: деньги по каждому модулю
    mods = [('grade', 'Grade', '≈5 млн ₽', 'в месяц', 'Перестаёте платить за работу без результата: 20% неэффективных видны сразу — решение за вами: обучение, ротация или расставание.', '100 разработчиков'),
            ('ai', 'AI', '×1,9', 'отдачи на рубль', 'Бюджет на ИИ идёт туда, где он ускоряет, а не плодит переделки: лицензии и обучение — по реальной отдаче каждого.', 'ориентир: Exceeds AI'),
            ('projects', 'Projects', '≈1,6 млн ₽', 'в месяц', 'Платите подрядчику за результат в коде, а не за часы в акте: переплата видна по каждому MR.', 'подрядчик из 10 разработчиков'),
            ('mentor', 'Mentor', '≈1,9 млн ₽', 'в месяц', 'Авто-ревью и ИИ-наставник возвращают сеньорам часы, которые уходили на рутинное ревью и разбор ошибок.', '50 разработчиков')]
    cards = ''
    for key, mod, big, unit, text, basis in mods:
        line, txt = ACC[key]
        cards += ('<article style="min-width: 0; border-radius: 28px; background: linear-gradient(160deg, %s1A 0%%, #1A1925 50%%); border: 1px solid %s4D; padding: clamp(24px, 3vw, 36px); display: flex; flex-direction: column; gap: 12px;">'
                  '<div style="font-family: \'Bricolage Grotesque\', sans-serif; font-weight: 800; font-size: 20px;"><span style="color: %s;">&gt;</span> UpCore<span style="color: %s;">.%s</span></div>'
                  '<div style="display: flex; flex-wrap: wrap; align-items: baseline; gap: 4px 12px;"><span style="font-size: clamp(44px, 4.4vw, 64px); font-weight: 800; letter-spacing: -0.04em; line-height: 1; white-space: nowrap; color: #FFFFFF; font-variant-numeric: tabular-nums;">%s</span>'
                  '<span style="font-size: 18px; color: %s; font-weight: 700;">%s</span></div>'
                  '<p style="margin: 0; color: rgba(255,255,255,0.8); font-size: 16px; line-height: 1.55;">%s</p>'
                  '<div style="margin-top: auto; %s font-size: 12px; color: rgba(255,255,255,0.5);">%s</div></article>') % (line, line, line, txt, mod, e(big), txt, e(unit), e(text), MONO, e(basis))
    inner = ('<div style="%s">'
             '<div style="display: flex; flex-wrap: wrap; gap: 24px 56px; align-items: flex-end; justify-content: space-between;">'
             '<div style="flex: 1.3 1 560px; min-width: 0;">%s<h2 style="%s">Четыре решения — четыре статьи экономии</h2></div>'
             '<div style="flex: 1 1 320px; min-width: 0;"><div style="font-size: clamp(40px, 4vw, 56px); font-weight: 800; letter-spacing: -0.03em; color: #7FDB7A; line-height: 1;">+12%%</div>'
             '<p style="margin: 8px 0 0; font-size: 16px; line-height: 1.5; color: rgba(255,255,255,0.78);">производительности команды сразу после запуска — ещё до любых решений, только за счёт прозрачности.</p></div></div>'
             '<div class="g2">%s</div>%s</div>') % (box, res_label(), h2st, cards, res_foot('Цифры — ориентиры из расчётов UpCore и данных рынка (подписаны), перед публикацией заменить на подтверждённые. Затраты 300 тыс. ₽ в месяц на разработчика.'))
    return section(inner, 'results')

# ---------------------------------------------------------------- раунд 26: «Результаты для бизнеса» на основе варианта 1, большая цифра согласована с расчётом
RES_SCEN = {
  'full': dict(big='≈1,2 млн ₽', text='экономического эффекта в год на каждого разработчика — столько возвращает UpCore при полной реализации',
               rows=[('Закрываем «дыру» 20% неэффективных', '≈5,0 млн ₽'), ('+12% к выработке остальных — от прозрачности', '≈3,6 млн ₽'), ('2,5 ставки тимлидов (400 ч) освобождаются от ручной оценки', '≈1,1 млн ₽')],
               month='≈9,7 млн ₽', year='≈116 млн ₽', per='≈1,2 млн ₽'),
  'cons': dict(big='≈500 тыс. ₽', text='экономического эффекта в год на каждого разработчика — даже в осторожном сценарии',
               rows=[('Закрываем только четверть «дыры» неэффективных', '≈1,3 млн ₽'), ('+6% к выработке — половина эффекта прозрачности', '≈1,8 млн ₽'), ('2,5 ставки тимлидов (400 ч) освобождаются от ручной оценки', '≈1,1 млн ₽')],
               month='≈4,2 млн ₽', year='≈50 млн ₽', per='≈500 тыс. ₽'),
}
RES_TILES = [('до +30%', 'рост эффективности разработки за счёт контроля продуктивности', 'ориентир: Tech Talent Score'),
             ('−20%', 'time-to-market: потери в процессах становятся видны', 'ориентир: Tech Talent Score'),
             ('2,5 ставки', 'тимлидов на каждые 100 разработчиков освобождается от ручной оценки', U)]
RES_ASSUME = 'Допущения: 100 разработчиков, полные затраты 300 тыс. ₽ в месяц на человека (ФОТ разработки 30 млн ₽), ставка тимлида 450 тыс. ₽.'

def results_v5(n):
    """1 — полный эффект (≈1,2 млн ₽ на разработчика), 2 — осторожный сценарий (≈500 тыс. ₽), 3 — вилка с двумя колонками расчёта."""
    line, txt = ACC[None]
    if n == 3:
        big, text = '0,5–1,2 млн ₽', 'экономического эффекта в год на каждого разработчика: от осторожного сценария до полной реализации'
        month_sub = '4,2–9,7 млн ₽'
    else:
        d = RES_SCEN['full' if n == 1 else 'cons']
        big, text, month_sub = d['big'], d['text'], d['month']
    subs = [(month_sub, 'в месяц на команду из 100 разработчиков'), ('1 месяц', 'до первых решений — по истории вашего Git'), ('0 ₽', 'за пилот: платите после того, как подтвердите точность')]
    sub_html = ''.join('<div style="min-width: 0;"><div style="font-size: %s; font-weight: 800; letter-spacing: -0.02em; color: #FFFFFF; white-space: nowrap; font-variant-numeric: tabular-nums;">%s</div>'
                       '<div style="font-size: 14px; color: rgba(255,255,255,0.7); line-height: 1.4; margin-top: 4px;">%s</div></div>' % ('clamp(20px, 1.6vw, 24px)' if n == 3 and i == 0 else 'clamp(24px, 2.2vw, 34px)', e(a), e(b)) for i, (a, b) in enumerate(subs))
    banner = ('<div style="border-radius: 32px; background: #12111C; border: 1px solid %s73; box-shadow: inset 0 0 120px rgba(99,213,255,0.06); padding: clamp(28px, 4vw, 48px); display: flex; flex-wrap: wrap; gap: 32px 48px; align-items: center; margin-bottom: 16px;">'
              '<div style="flex: 1.2 1 420px; min-width: 0;"><div style="font-size: %s; font-weight: 800; letter-spacing: -0.04em; line-height: 0.95; color: %s; font-variant-numeric: tabular-nums;">%s</div>'
              '<p style="margin: 16px 0 0; font-size: clamp(18px, 1.5vw, 22px); line-height: 1.45; color: rgba(255,255,255,0.88); max-width: 560px;">%s</p></div>'
              '<div class="g3" style="flex: 1 1 420px; min-width: 0; gap: 20px;">%s</div></div>') % (
                  line, 'clamp(56px, 6.4vw, 96px)' if n == 3 else 'clamp(56px, 7vw, 104px)', txt, e(big), e(text), sub_html)
    tiles = ''.join(card('<div style="font-size: clamp(30px, 2.7vw, 42px); font-weight: 800; letter-spacing: -0.03em; line-height: 1.05; color: %s; white-space: nowrap; font-variant-numeric: tabular-nums;">%s</div>'
                         '<p style="margin: 0; color: rgba(255,255,255,0.86); font-size: 15px; line-height: 1.5;">%s</p>%s' % ('#7FDB7A' if b.startswith(('+', 'до +')) else txt, e(b), e(l), src_line(s_)), pad='24px', gap=10) for b, l, s_ in RES_TILES)
    rowst = 'display: flex; justify-content: space-between; gap: 16px; padding: 14px 0; border-top: 1px solid rgba(255,255,255,0.08); font-size: 17px; line-height: 1.4;'
    if n in (1, 2):
        d = RES_SCEN['full' if n == 1 else 'cons']
        lines = ''.join('<div style="%s"><span style="color: rgba(255,255,255,0.84);">%s</span><b style="white-space: nowrap; font-variant-numeric: tabular-nums;">%s</b></div>' % (rowst, e(a), e(b)) for a, b in d['rows'])
        tot = ('<div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 8px 16px; padding: 18px 0 12px; border-top: 2px solid %s; font-size: 22px; font-weight: 800;"><span>Итого в месяц</span><span style="color: %s; font-variant-numeric: tabular-nums;">%s</span></div>'
               '<div style="%s"><span style="color: rgba(255,255,255,0.84);">В год на команду</span><b style="white-space: nowrap;">%s</b></div>'
               '<div style="%s"><span style="color: rgba(255,255,255,0.84);">На одного разработчика в год</span><b style="white-space: nowrap; color: %s;">%s</b></div>') % (txt, txt, d['month'], rowst, d['year'], rowst, txt, d['per'])
        title = 'Эффект на команду из 100 разработчиков' if n == 1 else 'Осторожный сценарий: команда из 100 разработчиков'
        foot = RES_ASSUME + (' Даже при 30% реализации — ≈2,9 млн ₽ в месяц, или ≈350 тыс. ₽ на разработчика в год.' if n == 1 else ' При полной реализации эффект больше в 2,3 раза — ≈1,2 млн ₽ на разработчика в год.')
        right = lines + tot
    else:
        f, c = RES_SCEN['full'], RES_SCEN['cons']
        grid = 'display: grid; grid-template-columns: minmax(0, 1fr) minmax(76px, auto) minmax(76px, auto); gap: 6px 20px; align-items: baseline; padding: 12px 0; border-top: 1px solid rgba(255,255,255,0.08); font-size: 16px; line-height: 1.4;'
        head = '<div class="uc-sc" style="%s border-top: 0; padding-top: 0;"><span></span><span style="%s font-size: 12px; color: rgba(255,255,255,0.6); text-align: right;">ОСТОРОЖНО</span><span style="%s font-size: 12px; color: %s; text-align: right;">ПОЛНЫЙ ЭФФЕКТ</span></div>' % (grid, MONO, MONO, txt)
        labels = ['Неэффективность: «дыра» 20% разработчиков', 'Прозрачность: рост выработки остальных', 'Тимлиды: 2,5 ставки без ручной оценки']
        body = ''.join('<div class="uc-sc" style="%s"><span style="color: rgba(255,255,255,0.84);">%s</span><b style="text-align: right; white-space: nowrap; color: rgba(255,255,255,0.8);">%s</b><b style="text-align: right; white-space: nowrap;">%s</b></div>' % (grid, e(l), c['rows'][i][1], f['rows'][i][1]) for i, l in enumerate(labels))
        tot = ''.join('<div class="uc-sc" style="%s%s"><span style="font-weight: %s;">%s</span><b style="text-align: right; white-space: nowrap; color: rgba(255,255,255,0.86); font-size: %s;">%s</b><b style="text-align: right; white-space: nowrap; color: %s; font-size: %s;">%s</b></div>' % (
            grid, ' border-top: 2px solid %s;' % txt if i == 0 else '', 800 if i == 0 else 400, a, '20px' if i == 2 else '17px', cv, txt, '20px' if i == 2 else '17px', fv)
            for i, (a, cv, fv) in enumerate([('Итого в месяц', c['month'], f['month']), ('В год на команду', c['year'], f['year']), ('На одного разработчика в год', c['per'], f['per'])]))
        title = 'Эффект на команду из 100 разработчиков: два сценария'
        foot = RES_ASSUME + ' Осторожно: закрываем четверть «дыры» неэффективных и берём половину эффекта прозрачности (+6%). Полный эффект: −20% потерь и +12% выработки.'
        right = head + body + tot
    calc = ('<div style="margin-top: 16px; border-radius: 28px; background: #12111C; border: 1px solid rgba(255,255,255,0.1); padding: clamp(24px, 3vw, 40px); display: flex; flex-wrap: wrap; gap: 32px;">'
            '<div style="flex: 1 1 280px; min-width: 0;"><div style="%s font-size: 13px; color: %s; margin-bottom: 10px;">РАСЧЁТ</div><div style="font-size: clamp(24px, 2.2vw, 32px); font-weight: 800; line-height: 1.15;">%s</div>'
            '<p style="margin: 14px 0 0; color: rgba(255,255,255,0.62); font-size: 14px; line-height: 1.5;">%s</p></div>'
            '<div style="flex: 1.4 1 420px; min-width: 0;">%s</div></div>') % (MONO, txt, e(title), e(foot), right)
    out = (sec_head('РЕЗУЛЬТАТЫ ДЛЯ БИЗНЕСА', RESULTS['home']['h2'], RESULTS['home'].get('lead')) + banner + '<div class="g3">%s</div>' % tiles + calc +
           '<div style="margin-top: 14px; %s font-size: 12px; color: rgba(255,255,255,0.5);">Цифры — ориентиры: данные UpCore и рынка; перед публикацией заменить на подтверждённые показатели UpCore.</div>' % MONO)
    return section(out, 'results')

# ---------------------------------------------------------------- раунд 27: «Результаты для бизнеса» — 4 расчёта, без сносок-ориентиров
RES6 = {
 1: dict(big='≈1,2 млн ₽', month='≈9,7 млн ₽', title='Эффект на команду из 100 разработчиков',
         rows=[('Закрываем «дыру» 20% неэффективных', '≈5,0 млн ₽'), ('+12% к выработке остальных — от прозрачности', '≈3,6 млн ₽'), ('2,5 ставки тимлидов (400 ч) освобождаются от ручной оценки', '≈1,1 млн ₽')],
         total=('Итого в месяц', '≈9,7 млн ₽'), tail=[('В год на команду', '≈116 млн ₽'), ('На одного разработчика в год', '≈1,2 млн ₽')],
         foot='Допущения: 100 разработчиков, полные затраты 300 тыс. ₽ в месяц на человека (ФОТ разработки 30 млн ₽), ставка тимлида 450 тыс. ₽. Даже при 30% реализации — ≈2,9 млн ₽ в месяц, или ≈350 тыс. ₽ на разработчика в год.'),
 2: dict(big='≈780 тыс. ₽', month='≈6,5 млн ₽', title='Эффект на команду из 100 разработчиков',
         rows=[('Берём половину «дыры» 20% неэффективных: −10% потерь ФОТ', '≈2,5 млн ₽'), ('+12% к выработке остальных — от прозрачности', '≈3,0 млн ₽'), ('2,5 ставки тимлидов освобождаются от ручной оценки', '≈1,0 млн ₽')],
         total=('Итого в месяц', '≈6,5 млн ₽'), tail=[('В год на команду', '≈78 млн ₽'), ('На одного разработчика в год', '≈780 тыс. ₽')],
         foot='Допущения: 100 разработчиков, полные затраты 250 тыс. ₽ в месяц на человека (ФОТ разработки 25 млн ₽), ставка тимлида 400 тыс. ₽. Из «дыры» 20% неэффективных учитываем только половину эффекта — 10% ФОТ.'),
 3: dict(big='≈450 тыс. ₽', month='≈3,75 млн ₽', title='Эффект на команду из 100 разработчиков',
         rows=[('Закрываем четверть «дыры» неэффективных: −5% потерь ФОТ', '≈1,25 млн ₽'), ('+6% к выработке — половина эффекта прозрачности', '≈1,5 млн ₽'), ('2,5 ставки тимлидов освобождаются от ручной оценки', '≈1,0 млн ₽')],
         total=('Итого в месяц', '≈3,75 млн ₽'), tail=[('В год на команду', '≈45 млн ₽'), ('На одного разработчика в год', '≈450 тыс. ₽')],
         foot='Допущения: 100 разработчиков, полные затраты 250 тыс. ₽ в месяц на человека (ФОТ разработки 25 млн ₽), ставка тимлида 400 тыс. ₽. Берём осторожно: четверть «дыры» неэффективных и половину эффекта прозрачности.'),
 4: dict(big='≈450 тыс. ₽', month='≈3,75 млн ₽', title='Эффект на одного разработчика',
         rows=[('Затраты компании на разработчика в месяц', '250 тыс. ₽'), ('+10% к выработке — прозрачность и саморегуляция', '≈25 тыс. ₽'), ('−5% потерь на работу без результата и переделки', '≈12,5 тыс. ₽')],
         total=('Эффект в месяц на разработчика', '≈37,5 тыс. ₽'), tail=[('На одного разработчика в год', '≈450 тыс. ₽'), ('На команду из 100 разработчиков в год', '≈45 млн ₽')],
         foot='Считаем от одного человека: эффект 15% от затрат на разработчика. Время тимлидов не учитываем — это бонус сверху, ещё ≈10 тыс. ₽ в месяц на каждого разработчика (2,5 ставки по 400 тыс. ₽ на 100 человек).'),
}
RES6_TILES = [('до +30%', 'рост эффективности разработки за счёт контроля продуктивности'),
              ('−20%', 'time-to-market: потери в процессах становятся видны'),
              ('2,5 ставки', 'тимлидов на каждые 100 разработчиков освобождается от ручной оценки')]

def results_v6(n):
    d = RES6[n]
    line, txt = ACC[None]
    subs = [(d['month'], 'в месяц на команду из 100 разработчиков'), ('1 неделя', 'до первых результатов'), ('0 ₽', 'за пилот: платите после того, как подтвердите точность')]
    sub_html = ''.join('<div style="min-width: 0;"><div style="font-size: clamp(24px, 2.2vw, 34px); font-weight: 800; letter-spacing: -0.02em; color: #FFFFFF; white-space: nowrap; font-variant-numeric: tabular-nums;">%s</div>'
                       '<div style="font-size: 14px; color: rgba(255,255,255,0.7); line-height: 1.4; margin-top: 4px;">%s</div></div>' % (e(a), e(b)) for a, b in subs)
    banner = ('<div style="border-radius: 32px; background: #12111C; border: 1px solid %s73; box-shadow: inset 0 0 120px rgba(99,213,255,0.06); padding: clamp(28px, 4vw, 48px); display: flex; flex-wrap: wrap; gap: 32px 48px; align-items: center; margin-bottom: 16px;">'
              '<div style="flex: 1.2 1 420px; min-width: 0;"><div style="font-size: clamp(44px, 7vw, 104px); font-weight: 800; letter-spacing: -0.04em; line-height: 0.95; color: %s; white-space: nowrap; font-variant-numeric: tabular-nums;">%s</div>'
              '<p style="margin: 16px 0 0; font-size: clamp(18px, 1.5vw, 22px); line-height: 1.45; color: rgba(255,255,255,0.88); max-width: 560px;">экономического эффекта в год на каждого разработчика</p></div>'
              '<div class="g3" style="flex: 1 1 420px; min-width: 0; gap: 20px;">%s</div></div>') % (line, txt, e(d['big']), sub_html)
    tiles = ''.join(card('<div style="font-size: clamp(30px, 2.7vw, 42px); font-weight: 800; letter-spacing: -0.03em; line-height: 1.05; color: %s; white-space: nowrap; font-variant-numeric: tabular-nums;">%s</div>'
                         '<p style="margin: 0; color: rgba(255,255,255,0.86); font-size: 15px; line-height: 1.5;">%s</p>' % ('#7FDB7A' if b.startswith(('+', 'до +')) else txt, e(b), e(l)), pad='24px', gap=10) for b, l in RES6_TILES)
    rowst = 'display: flex; justify-content: space-between; gap: 16px; padding: 14px 0; border-top: 1px solid rgba(255,255,255,0.08); font-size: 17px; line-height: 1.4;'
    lines = ''.join('<div style="%s"><span style="color: rgba(255,255,255,%s);">%s</span><b style="white-space: nowrap; font-variant-numeric: tabular-nums;%s">%s</b></div>' % (
        rowst, '0.62' if (n == 4 and i == 0) else '0.84', e(a), ' font-weight: 400; color: rgba(255,255,255,0.7);' if (n == 4 and i == 0) else '', e(b)) for i, (a, b) in enumerate(d['rows']))
    tot = ('<div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 8px 16px; padding: 18px 0 12px; border-top: 2px solid %s; font-size: 22px; font-weight: 800;"><span>%s</span><span style="color: %s; font-variant-numeric: tabular-nums;">%s</span></div>' % (txt, e(d['total'][0]), txt, e(d['total'][1])))
    tot += ''.join('<div style="%s"><span style="color: rgba(255,255,255,0.84);">%s</span><b style="white-space: nowrap;%s">%s</b></div>' % (rowst, e(a), (' color: %s;' % txt) if 'одного' in a else '', e(b)) for a, b in d['tail'])
    calc = ('<div style="margin-top: 16px; border-radius: 28px; background: #12111C; border: 1px solid rgba(255,255,255,0.1); padding: clamp(24px, 3vw, 40px); display: flex; flex-wrap: wrap; gap: 32px;">'
            '<div style="flex: 1 1 280px; min-width: 0;"><div style="%s font-size: 13px; color: %s; margin-bottom: 10px;">РАСЧЁТ</div><div style="font-size: clamp(24px, 2.2vw, 32px); font-weight: 800; line-height: 1.15;">%s</div>'
            '<p style="margin: 14px 0 0; color: rgba(255,255,255,0.62); font-size: 14px; line-height: 1.5;">%s</p></div>'
            '<div style="flex: 1.4 1 420px; min-width: 0;">%s%s</div></div>') % (MONO, txt, e(d['title']), e(d['foot']), lines, tot)
    out = sec_head('РЕЗУЛЬТАТЫ ДЛЯ БИЗНЕСА', RESULTS['home']['h2'], 'Платформа окупается в десятки раз: эффект виден уже в первый месяц.') + banner + '<div class="g3">%s</div>' % tiles + calc
    return section(out, 'results')

def core_block():
    """Сердце UpCore: запатентованная модель 50+ факторов → человеко-часы. Уникальная механика, отличие от конкурентов."""
    factors = ['Язык, технологии и их грейд', 'Объём, тип и сложность задачи', 'Цикломатическая, когнитивная, логическая сложность',
               'Ядро или периферия: AST-граф связей', 'Результирующий код и переделки', 'Шум: автогенерация, копипаст, ренеймы',
               'Баги и замечания код-ревью', 'Опыт человека в проекте']
    chips = ''.join('<span style="padding: 7px 10px; border-radius: 8px; background: rgba(99,213,255,0.10); color: #CFF3FF; font-size: 13px; line-height: 1.3;">%s</span>' % e(f) for f in factors)
    def step(n, title, body):
        return ('<div style="min-width: 0; border-radius: 22px; background: #0B0A12; border: 1px solid rgba(255,255,255,0.1); padding: 22px; display: flex; flex-direction: column; gap: 12px;">'
                '<div style="%s font-size: 12px; color: #63D5FF;">%s</div><div style="font-size: 20px; font-weight: 800; line-height: 1.2;">%s</div>%s</div>') % (MONO, n, e(title), body)
    s1 = step('01 · ВХОД', 'Merge Request', '<p style="margin: 0; color: rgba(255,255,255,0.74); font-size: 15px; line-height: 1.5;">Код, история репозитория и контекст проекта. Ничего не нужно заполнять вручную.</p>')
    s2 = step('02 · ДЕКОМПОЗИЦИЯ', '50+ факторов', '<div style="display: flex; flex-wrap: wrap; gap: 6px;">%s</div>' % chips)
    s3 = step('03 · МОДЕЛЬ', 'Запатентованная математика', '<p style="margin: 0; color: rgba(255,255,255,0.74); font-size: 15px; line-height: 1.5;">Детерминированная модель, откалиброванная под каждый стек на экспертных оценках. Один и тот же код — всегда один и тот же результат.</p>')
    s4 = step('04 · РЕЗУЛЬТАТ', 'Объективные человеко‑часы',
              '<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; font-variant-numeric: tabular-nums;">'
              '<div><div style="font-size: 12px; color: rgba(255,255,255,0.6);">объективно</div><div style="font-size: 30px; font-weight: 800; color: #63D5FF;">2 ч</div></div>'
              '<div><div style="font-size: 12px; color: rgba(255,255,255,0.6);">потрачено</div><div style="font-size: 30px; font-weight: 800;">8 ч</div></div></div>'
              '<div style="border-top: 1px solid rgba(255,255,255,0.08); padding-top: 10px; font-size: 15px;">Эффективность <b style="color: #F08A8A;">25%</b> · потери — 6 ч × ставка</div>')
    pipeline = '<div class="g4">%s%s%s%s</div>' % (s1, s2, s3, s4)
    formula = ('<div style="display: flex; flex-wrap: wrap; gap: 20px 40px; align-items: center; justify-content: space-between; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 28px;">'
               '<div style="font-size: clamp(20px, 2vw, 28px); font-weight: 800; line-height: 1.3;">Эффективность = <span style="color: #63D5FF;">объективные часы</span> ÷ фактические часы</div>'
               '<div style="font-size: 16px; color: rgba(255,255,255,0.78); line-height: 1.5; max-width: 520px;">Пример: за месяц 160 рабочих часов, результата — на 80. Эффективность 50%, а потери — 80 часов, умноженные на ставку. Так код превращается в деньги.</div></div>')
    diffs = [('Результат, а не активность', 'Не строки, коммиты и тикеты, которые легко накрутить, а трудоёмкость работы, которая осталась в продукте.'),
             ('Архитектура имеет вес', '50 строк в ядре системы стоят дороже 1000 строк формочек: модель видит, где именно работал человек.'),
             ('Точность на дистанции', 'Оценка строится по 100+ задачам подряд — статистика сглаживает аномалии, и результат совпадает с экспертом на 96%.')]
    dcards = ''.join('<div style="min-width: 0;"><div style="font-size: 18px; font-weight: 800; margin-bottom: 6px;">%s</div><div style="color: rgba(255,255,255,0.74); font-size: 15px; line-height: 1.55;">%s</div></div>' % (e(a), e(b)) for a, b in diffs)
    inner = ('<div style="position: relative; overflow: hidden; border-radius: 40px; background: #12111C; border: 1px solid rgba(99,213,255,0.45); box-shadow: inset 0 0 160px rgba(99,213,255,0.07); padding: clamp(28px, 4vw, 56px); display: flex; flex-direction: column; gap: 32px;">'
             '<div style="display: flex; flex-wrap: wrap; gap: 20px 48px; align-items: flex-end; justify-content: space-between;">'
             '<div style="flex: 1 1 520px; min-width: 0;"><div style="%s font-size: 13px; color: #63D5FF; letter-spacing: 0.04em; margin-bottom: 14px;">СЕРДЦЕ UPCORE · ЗАПАТЕНТОВАННЫЙ МЕТОД</div>'
             '<h2 style="margin: 0; font-size: clamp(32px, 3.4vw, 52px); letter-spacing: -0.03em; line-height: 1.05; font-weight: 800;">Мы переводим код в <span style="color: #63D5FF;">объективные человеко‑часы</span></h2></div>'
             '<p style="flex: 1 1 380px; min-width: 0; margin: 0; color: rgba(255,255,255,0.8); font-size: 17px; line-height: 1.55;">Каждый Merge Request раскладывается на 50+ факторов, а запатентованная математическая модель вычисляет, сколько часов эта работа объективно требует. '
             'Сравниваем с фактическим временем — и получаем эффективность, грейд и деньги. Без отчётов, опросов и оценок «на глаз».</p></div>'
             '%s%s<div class="g3">%s</div></div>') % (MONO, pipeline, formula, dcards)
    return section(inner, 'core')

def _bar(label, val, pct, color):
    return ('<div><div style="display: flex; justify-content: space-between; gap: 12px; font-size: 16px; margin-bottom: 8px;"><span style="color: rgba(255,255,255,0.84);">%s</span><b style="font-variant-numeric: tabular-nums;">%s</b></div>'
            '<div style="height: 14px; border-radius: 7px; background: rgba(255,255,255,0.07); overflow: hidden;"><div style="width: %d%%; height: 100%%; background: %s; border-radius: 7px;"></div></div></div>') % (e(label), e(val), pct, color)

CORE_LABEL = 'СЕРДЦЕ UPCORE · ЗАПАТЕНТОВАННЫЙ МЕТОД'
CORE_PANEL = 'border-radius: 32px; background: #12111C; border: 1px solid rgba(99,213,255,0.45); box-shadow: inset 0 0 140px rgba(99,213,255,0.07); padding: clamp(24px, 3.5vw, 48px);'

def core_variant(n):
    """Три компактных варианта блока об уникальной механике (раунд 10)."""
    lab = '<div style="%s font-size: 12px; color: #63D5FF; letter-spacing: 0.04em; margin-bottom: 12px;">%s</div>' % (MONO, CORE_LABEL)
    if n == 1:  # «Формула»: заголовок + одна фраза слева, пример со шкалами справа
        left = ('<div style="flex: 1 1 420px; min-width: 0;">%s<h2 style="margin: 0; font-size: clamp(30px, 3vw, 44px); letter-spacing: -0.03em; line-height: 1.08; font-weight: 800;">'
                'Код → <span style="color: #63D5FF;">объективные человеко‑часы</span></h2>'
                '<p style="margin: 16px 0 0; color: rgba(255,255,255,0.8); font-size: 17px; line-height: 1.55; max-width: 480px;">Запатентованная математическая модель по 50+ факторам считает, сколько часов работа в коде стоит на самом деле.</p></div>') % lab
        right = ('<div style="flex: 1 1 420px; min-width: 0; border-radius: 22px; background: #0B0A12; border: 1px solid rgba(255,255,255,0.08); padding: 24px; display: flex; flex-direction: column; gap: 18px;">'
                 '%s%s<div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 8px 16px; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 14px; font-size: 17px;">'
                 '<span>Эффективность <b style="color: #63D5FF;">50%%</b></span><span style="color: rgba(255,255,255,0.74);">потери — 80 ч × ставка</span></div></div>') % (
                 _bar('Отработано за месяц', '160 ч', 100, 'rgba(255,255,255,0.35)'), _bar('Реальная ценность кода', '80 ч', 50, '#63D5FF'))
        inner = '<div style="%s display: flex; flex-wrap: wrap; gap: 32px 48px; align-items: center;">%s%s</div>' % (CORE_PANEL, left, right)
    elif n == 2:  # «Конвейер»: одна строка шагов + строка расчёта
        steps_ = ['Merge Request', '50+ факторов', 'Запатентованная модель', 'Объективные часы']
        chain = ''.join(('<span aria-hidden="true" style="color: #63D5FF; font-size: 26px; font-weight: 800;">›</span>' if i else '') +
                        '<span style="padding: 12px 16px; border-radius: 14px; background: %s; border: 1px solid %s; font-size: 16px; font-weight: 700; white-space: nowrap;">%s</span>' % (
                            'rgba(99,213,255,0.14)' if i == 3 else '#0B0A12', 'rgba(99,213,255,0.5)' if i == 3 else 'rgba(255,255,255,0.1)', e(s)) for i, s in enumerate(steps_))
        calc = [('160 ч', 'отработал разработчик'), ('80 ч', 'реальная ценность кода'), ('50%', 'эффективность'), ('−80 ч', '× ставка — потери')]
        cells = ''.join('<div style="min-width: 0;"><div style="font-size: clamp(30px, 3vw, 44px); font-weight: 800; letter-spacing: -0.03em; color: %s; white-space: nowrap; font-variant-numeric: tabular-nums;">%s</div>'
                        '<div style="font-size: 14px; color: rgba(255,255,255,0.72); margin-top: 4px;">%s</div></div>' % ('#63D5FF' if i in (1, 2) else '#FFFFFF', e(a), e(b)) for i, (a, b) in enumerate(calc))
        inner = ('<div style="%s display: flex; flex-direction: column; gap: 28px;"><div>%s<h2 style="margin: 0; font-size: clamp(28px, 2.8vw, 40px); letter-spacing: -0.03em; line-height: 1.1; font-weight: 800;">Как UpCore видит реальную ценность кода</h2></div>'
                 '<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 10px;">%s</div>'
                 '<div class="g4m2" style="border-top: 1px solid rgba(255,255,255,0.08); padding-top: 24px;">%s</div></div>') % (CORE_PANEL, lab, chain, cells)
    else:  # «Контраст»: две гигантские цифры
        big = lambda v, l, c: ('<div style="min-width: 0;"><div style="font-size: clamp(64px, 9vw, 128px); font-weight: 800; letter-spacing: -0.05em; line-height: 0.9; color: %s; white-space: nowrap; font-variant-numeric: tabular-nums;">%s</div>'
                               '<div style="font-size: 16px; color: rgba(255,255,255,0.75); margin-top: 10px;">%s</div></div>') % (c, e(v), e(l))
        nums = ('<div style="display: flex; flex-wrap: wrap; align-items: flex-end; gap: 16px 32px;">%s<div aria-hidden="true" style="font-size: clamp(40px, 5vw, 72px); font-weight: 800; color: rgba(255,255,255,0.3); line-height: 1; padding-bottom: 28px;">→</div>%s</div>') % (
                big('160 ч', 'отработано за месяц', '#FFFFFF'), big('80 ч', 'реальная ценность кода', '#63D5FF'))
        tags = ''.join('<span style="padding: 8px 12px; border-radius: 10px; background: rgba(99,213,255,0.1); color: #CFF3FF; font-size: 14px;">%s</span>' % e(x) for x in ['50+ факторов', 'запатентованная модель', '96% совпадения с экспертом'])
        text = ('<div style="flex: 1 1 360px; min-width: 0;">%s<h2 style="margin: 0; font-size: clamp(26px, 2.4vw, 34px); letter-spacing: -0.02em; line-height: 1.15; font-weight: 800;">Эффективность — 50%%. Остальное видно до строчки кода.</h2>'
                '<p style="margin: 14px 0 18px; color: rgba(255,255,255,0.78); font-size: 16px; line-height: 1.55;">Сердце UpCore переводит код в объективные человеко‑часы — и сразу в деньги.</p>'
                '<div style="display: flex; flex-wrap: wrap; gap: 8px;">%s</div></div>') % (lab, tags)
        inner = '<div style="%s display: flex; flex-wrap: wrap; gap: 32px 56px; align-items: center;"><div style="flex: 1.3 1 480px; min-width: 0;">%s</div>%s</div>' % (CORE_PANEL, nums, text)
    return section(inner, 'core')

def core_v2(n):
    """Раунд 11: три варианта на основе «Сердце 1» — уникальная механика, ценность вместо строк, 160 ч → 80 ч."""
    def lab(text):
        return '<div style="%s font-size: 12px; color: #63D5FF; letter-spacing: 0.04em; margin-bottom: 12px;">%s</div>' % (MONO, e(text))
    def h2(html_):
        return '<h2 style="margin: 0; font-size: clamp(30px, 3vw, 44px); letter-spacing: -0.03em; line-height: 1.08; font-weight: 800;">%s</h2>' % html_
    def para(text):
        return '<p style="margin: 16px 0 0; color: rgba(255,255,255,0.8); font-size: 17px; line-height: 1.55; max-width: 500px;">%s</p>' % text
    def foot(a, b):
        return ('<div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 8px 16px; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 14px; font-size: 17px;">'
                '<span>%s</span><span style="color: rgba(255,255,255,0.78);">%s</span></div>') % (a, b)
    bars = _bar('Списано за месяц', '160 ч', 100, 'rgba(255,255,255,0.35)') + _bar('Реально решено задач — по коду', '80 ч', 50, '#63D5FF')
    card_style = 'flex: 1 1 420px; min-width: 0; border-radius: 22px; background: #0B0A12; border: 1px solid rgba(255,255,255,0.08); padding: 24px; display: flex; flex-direction: column; gap: 18px;'
    if n == 4:
        left = lab('УНИКАЛЬНАЯ МЕХАНИКА UPCORE') + h2('Мы не считаем строки кода. Мы измеряем его <span style="color: #63D5FF;">реальную ценность</span>') + para(
            'В основе — запатентованная математическая модель. Она разбирает каждый Merge Request по 50+ факторам и переводит написанный код в фактические человеко‑часы.')
        right = bars + foot('Эффективность <b style="color: #63D5FF;">50%</b>', '80 ч оплачено впустую')
    elif n == 5:
        left = lab('НОВАЯ МЕХАНИКА ОЦЕНКИ') + h2('Написанный код → <span style="color: #63D5FF;">фактические человеко‑часы</span>') + para(
            'Строки, коммиты и закрытые тикеты легко накрутить — особенно с ИИ. Наша запатентованная матмодель по 50+ факторам считает другое: сколько часов работы на самом деле стоит результат в коде.')
        noise = ''.join('<span style="text-decoration: line-through; text-decoration-color: rgba(240,138,138,0.8); color: rgba(255,255,255,0.55); font-size: 15px; white-space: nowrap;">%s</span>' % e(x)
                        for x in ['2 400 строк', '37 коммитов', '18 закрытых задач'])
        right = ('<div><div style="%s font-size: 12px; color: rgba(255,255,255,0.55); margin-bottom: 8px;">обычные метрики — «выглядит продуктивно»</div>'
                 '<div style="display: flex; flex-wrap: wrap; gap: 8px 18px;">%s</div></div>') % (MONO, noise) + bars + foot('Реальная эффективность <b style="color: #63D5FF;">50%</b>', 'видно до строчки кода')
    else:
        left = lab('СЕРДЦЕ UPCORE · ЗАПАТЕНТОВАННАЯ МАТМОДЕЛЬ') + h2('Списано 160 часов. Задач решено — на 80. <span style="color: #63D5FF;">UpCore видит разницу.</span>') + para(
            'Наша уникальная механика оценивает не количество строк, а реальную ценность кода: математическая модель по 50+ факторам переводит каждый MR в фактические человеко‑часы — и показывает, за что вы на самом деле платите.')
        right = bars + foot('Эффективность <b style="color: #63D5FF;">50%</b>', '≈150 тыс. ₽ в месяц — переплата за одного разработчика')
    inner = ('<div style="%s display: flex; flex-wrap: wrap; gap: 32px 48px; align-items: center;"><div style="flex: 1 1 440px; min-width: 0;">%s</div><div style="%s">%s</div></div>') % (CORE_PANEL, left, card_style, right)
    return section(inner, 'core')

RED, RED_T = '#E86565', '#F08A8A'
RED_STRIPES = 'repeating-linear-gradient(135deg, rgba(232,101,101,0.95) 0 6px, rgba(232,101,101,0.55) 6px 12px)'

def core_v3(n):
    """Раунд 12: левая часть «Сердце 4» с новым заголовком; правая — 3 представления часов, потери красным."""
    lab = '<div style="%s font-size: 12px; color: #63D5FF; letter-spacing: 0.04em; margin-bottom: 12px;">УНИКАЛЬНАЯ МЕХАНИКА UPCORE</div>' % MONO
    left = (lab + '<h2 style="margin: 0; font-size: clamp(30px, 3vw, 44px); letter-spacing: -0.03em; line-height: 1.08; font-weight: 800;">UpCore не считает строчки кода, а вычисляет его <span style="color: #63D5FF;">реальную ценность</span></h2>'
            '<p style="margin: 16px 0 0; color: rgba(255,255,255,0.8); font-size: 17px; line-height: 1.55; max-width: 500px;">В основе — запатентованная математическая модель. Она разбирает каждый Merge Request по 50+ факторам и переводит написанный код в фактические человеко‑часы.</p>')
    noise = ''.join('<span style="text-decoration: line-through; text-decoration-color: rgba(240,138,138,0.85); color: rgba(255,255,255,0.55); font-size: 15px; white-space: nowrap;">%s</span>' % e(x)
                    for x in ['10 423 строк', '35 merge request', '27 закрытых задач'])
    top = ('<div><div style="%s font-size: 12px; color: rgba(255,255,255,0.55); margin-bottom: 8px;">обычные метрики — «выглядит продуктивно»</div>'
           '<div style="display: flex; flex-wrap: wrap; gap: 8px 18px;">%s</div></div>') % (MONO, noise)
    bottom = ('<div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: baseline; gap: 8px 16px; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 14px;">'
              '<span style="font-size: 17px;">Эффективность <b style="color: #63D5FF;">50%%</b></span>'
              '<span style="font-size: 17px; color: %s; font-weight: 700;">−150 тыс. ₽ в месяц <span style="font-weight: 400; color: rgba(255,255,255,0.7);">— переплата за одного разработчика</span></span></div>') % RED_T
    legend = lambda c, a, b: ('<div style="display: flex; align-items: center; gap: 10px; min-width: 0;"><span aria-hidden="true" style="flex: 0 0 auto; width: 14px; height: 14px; border-radius: 4px; background: %s;"></span>'
                              '<span style="font-size: 15px; color: rgba(255,255,255,0.84);"><b style="color: #FFFFFF; font-variant-numeric: tabular-nums;">%s</b> %s</span></div>') % (c, e(a), e(b))
    if n == 7:  # одна полоса 160 ч: ценность + потери
        mid = ('<div><div style="display: flex; justify-content: space-between; font-size: 16px; margin-bottom: 10px;"><span style="color: rgba(255,255,255,0.84);">Списано за месяц</span><b>160 ч</b></div>'
               '<div role="img" aria-label="160 часов: 80 часов ценности, 80 часов потерь" style="display: flex; height: 44px; border-radius: 12px; overflow: hidden; font-size: 14px; font-weight: 800; white-space: nowrap;">'
               '<div style="width: 50%%; background: #63D5FF; color: #0D0C15; display: flex; align-items: center; padding-left: 10px;">80 ч ценности</div>'
               '<div style="width: 50%%; background: %s; color: #FFFFFF; display: flex; align-items: center; padding-left: 10px;">80 ч потерь</div></div>'
               '<div style="display: flex; flex-wrap: wrap; gap: 8px 20px; margin-top: 12px;">%s%s</div></div>') % (RED_STRIPES, legend('#63D5FF', '80 ч', 'задачи, реально решённые в коде'), legend(RED, '80 ч', 'оплачено без результата'))
    elif n == 8:  # месяц = 20 рабочих дней по 8 ч
        cells = ''.join('<span aria-hidden="true" style="aspect-ratio: 1; border-radius: 6px; background: %s;"></span>' % ('#63D5FF' if i < 10 else RED_STRIPES) for i in range(20))
        mid = ('<div><div style="display: flex; justify-content: space-between; font-size: 16px; margin-bottom: 10px;"><span style="color: rgba(255,255,255,0.84);">Месяц — 20 рабочих дней, 160 ч</span><span style="%s font-size: 12px; color: rgba(255,255,255,0.55);">1 клетка = 8 ч</span></div>'
               '<div role="img" aria-label="20 рабочих дней: 10 дней результата, 10 дней потерь" style="display: grid; grid-template-columns: repeat(10, minmax(0, 1fr)); gap: 6px;">%s</div>'
               '<div style="display: flex; flex-wrap: wrap; gap: 8px 20px; margin-top: 12px;">%s%s</div></div>') % (MONO, cells, legend('#63D5FF', '10 дней', 'реальной работы в коде — 80 ч'), legend(RED, '10 дней', 'оплачено впустую — 80 ч'))
    else:  # кольцо
        r = 52; c = 2 * 3.14159 * r
        ring = ('<svg viewBox="0 0 140 140" width="150" height="150" role="img" aria-label="Эффективность 50%%: 80 из 160 часов" style="flex: 0 0 auto;">'
                '<circle cx="70" cy="70" r="%d" fill="none" stroke="%s" stroke-width="18"></circle>'
                '<circle cx="70" cy="70" r="%d" fill="none" stroke="#63D5FF" stroke-width="18" stroke-dasharray="%.1f %.1f" transform="rotate(-90 70 70)"></circle>'
                '<text x="70" y="68" text-anchor="middle" font-family="Onest, sans-serif" font-size="26" font-weight="800" fill="#FFFFFF">80</text>'
                '<text x="70" y="88" text-anchor="middle" font-family="Onest, sans-serif" font-size="12" fill="rgba(255,255,255,0.7)">из 160 ч</text></svg>') % (r, RED, r, c / 2, c)
        line = lambda a, b, c: '<div style="font-size: 17px; color: rgba(255,255,255,0.84);">%s <b style="color: %s; font-size: 20px; white-space: nowrap;">%s</b></div>' % (e(a), c, e(b))
        mid = ('<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 20px 28px;">%s<div style="flex: 1 1 200px; min-width: 0; display: flex; flex-direction: column; gap: 14px;">'
               '%s%s%s</div></div>') % (ring, line('Списано за месяц', '160 час', '#FFFFFF'), line('Реально решённых задач', '80 час', RED_T), line('Эффективность', '50%', RED_T))
        bottom = ('<div style="border-top: 1px solid rgba(255,255,255,0.08); padding-top: 14px; font-size: 17px;"><b style="color: %s; font-size: 24px; letter-spacing: -0.01em;">−140 тыс. ₽ в месяц</b>'
                  ' <span style="color: rgba(255,255,255,0.72);">— переплата за одного разработчика</span></div>') % RED_T
    right = top + mid + bottom
    card = 'flex: 1 1 440px; min-width: 0; border-radius: 22px; background: #0B0A12; border: 1px solid rgba(255,255,255,0.08); padding: 24px; display: flex; flex-direction: column; gap: 20px;'
    inner = ('<div style="%s display: flex; flex-wrap: wrap; gap: 32px 48px; align-items: center;"><div style="flex: 1 1 420px; min-width: 0;">%s</div><div style="%s">%s</div></div>') % (CORE_PANEL, left, card, right)
    return section(inner, 'core')

def core_v4(n):
    """Раунд 13: на основе «Сердце 9» (кольцо). Эффективность 50% — красным; подписи: списано 160 ч, решено задач на 80 ч, эффективность 50%."""
    lab = '<div style="%s font-size: 12px; color: #63D5FF; letter-spacing: 0.04em; margin-bottom: 12px;">УНИКАЛЬНАЯ МЕХАНИКА UPCORE</div>' % MONO
    left = (lab + '<h2 style="margin: 0; font-size: clamp(30px, 3vw, 44px); letter-spacing: -0.03em; line-height: 1.08; font-weight: 800;">UpCore не считает строчки кода, а вычисляет его <span style="color: #63D5FF;">реальную ценность</span></h2>'
            '<p style="margin: 16px 0 0; color: rgba(255,255,255,0.8); font-size: 17px; line-height: 1.55; max-width: 500px;">В основе — запатентованная математическая модель. Она разбирает каждый Merge Request по 50+ факторам и переводит написанный код в фактические человеко‑часы.</p>')
    noise = ''.join('<span style="text-decoration: line-through; text-decoration-color: rgba(240,138,138,0.85); color: rgba(255,255,255,0.55); font-size: 15px; white-space: nowrap;">%s</span>' % e(x)
                    for x in ['2 400 строк', '37 коммитов', '18 закрытых задач'])
    top = ('<div><div style="%s font-size: 12px; color: rgba(255,255,255,0.55); margin-bottom: 8px;">обычные метрики — «выглядит продуктивно»</div>'
           '<div style="display: flex; flex-wrap: wrap; gap: 8px 18px;">%s</div></div>') % (MONO, noise)
    money = ('<div style="border-top: 1px solid rgba(255,255,255,0.08); padding-top: 14px; font-size: 17px;"><b style="color: %s;">−150 тыс. ₽ в месяц</b>'
             ' <span style="color: rgba(255,255,255,0.72);">— переплата за одного разработчика</span></div>') % RED_T
    def row(mark, label, val, vcol='#FFFFFF', big=False):
        fs = '30px' if big else '24px'
        return ('<div style="display: flex; align-items: center; justify-content: space-between; gap: 14px; padding: 10px 0; border-top: 1px solid rgba(255,255,255,0.06);">'
                '<span style="display: flex; align-items: center; gap: 10px; min-width: 0; font-size: 15px; color: rgba(255,255,255,0.84);">%s<span>%s</span></span>'
                '<b style="font-size: %s; letter-spacing: -0.02em; color: %s; white-space: nowrap; font-variant-numeric: tabular-nums;">%s</b></div>') % (mark, e(label), fs, vcol, e(val))
    def dot(c, ring=False):
        st = 'border: 3px solid %s; background: transparent;' % c if ring else 'background: %s;' % c
        return '<span aria-hidden="true" style="flex: 0 0 auto; width: 14px; height: 14px; border-radius: 50%%; %s"></span>' % st
    rows = (row(dot('rgba(255,255,255,0.45)', True), 'Списано за месяц', '160 ч') + row(dot('#63D5FF'), 'Реально решённых задач', 'на 80 ч', '#63D5FF')
            + row(dot(RED), 'Эффективность', '50%', RED_T, True))
    r = 52; C = 2 * 3.14159 * r
    stripes = ('<defs><pattern id="ucStr%d" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
               '<rect width="8" height="8" fill="rgba(232,101,101,0.55)"></rect><rect width="4" height="8" fill="#E86565"></rect></pattern></defs>') % n
    if n == 10:  # кольцо: голубая половина — решено, красная — потери; в центре 50% красным
        svg = ('<svg viewBox="0 0 140 140" width="168" height="168" role="img" aria-label="Эффективность 50%%: решено задач на 80 из 160 часов" style="flex: 0 0 auto;">%s'
               '<circle cx="70" cy="70" r="%d" fill="none" stroke="url(#ucStr%d)" stroke-width="18"></circle>'
               '<circle cx="70" cy="70" r="%d" fill="none" stroke="#63D5FF" stroke-width="18" stroke-dasharray="%.1f %.1f" transform="rotate(-90 70 70)"></circle>'
               '<text x="70" y="80" text-anchor="middle" font-family="Onest, sans-serif" font-size="30" font-weight="800" fill="%s">50%%</text></svg>') % (stripes, r, n, r, C / 2, C, RED_T)
    elif n == 11:  # два кольца: внешнее — списано 160 ч, внутреннее — решено 80 ч
        r2 = 36; C2 = 2 * 3.14159 * r2
        svg = ('<svg viewBox="0 0 140 140" width="168" height="168" role="img" aria-label="Списано 160 часов, решено задач на 80 часов, эффективность 50%%" style="flex: 0 0 auto;">' + stripes +
               '<circle cx="70" cy="70" r="%d" fill="none" stroke="rgba(255,255,255,0.45)" stroke-width="12"></circle>'
               '<circle cx="70" cy="70" r="%d" fill="none" stroke="url(#ucStr11)" stroke-width="12"></circle>'
               '<circle cx="70" cy="70" r="%d" fill="none" stroke="#63D5FF" stroke-width="12" stroke-dasharray="%.1f %.1f" stroke-linecap="round" transform="rotate(-90 70 70)"></circle>'
               '<text x="70" y="77" text-anchor="middle" font-family="Onest, sans-serif" font-size="19" font-weight="800" fill="%s">50%%</text></svg>') % (r + 6, r2, r2, C2 / 2, C2, RED_T)
    else:  # полукольцо-спидометр: 50% красным
        R = 58; half = 3.14159 * R
        svg = ('<svg viewBox="0 0 150 108" width="200" height="144" role="img" aria-label="Эффективность 50%%" style="flex: 0 0 auto;">%s'
               '<path d="M 17 80 A 58 58 0 0 1 133 80" fill="none" stroke="url(#ucStr%d)" stroke-width="16" stroke-linecap="butt"></path>'
               '<path d="M 17 80 A 58 58 0 0 1 133 80" fill="none" stroke="#63D5FF" stroke-width="16" stroke-dasharray="%.1f %.1f"></path>'
               '<line x1="75" y1="80" x2="75" y2="34" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"></line><circle cx="75" cy="80" r="5" fill="#FFFFFF"></circle>'
               '<text x="75" y="104" text-anchor="middle" font-family="Onest, sans-serif" font-size="17" font-weight="800" fill="%s">50%%</text></svg>') % (stripes, n, half / 2, half, RED_T)
    mid = '<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 16px 28px;">%s<div style="flex: 1 1 220px; min-width: 0;">%s</div></div>' % (svg, rows)
    card = 'flex: 1 1 440px; min-width: 0; border-radius: 22px; background: #0B0A12; border: 1px solid rgba(255,255,255,0.08); padding: 24px; display: flex; flex-direction: column; gap: 20px;'
    inner = ('<div style="%s display: flex; flex-wrap: wrap; gap: 32px 48px; align-items: center;"><div style="flex: 1 1 420px; min-width: 0;">%s</div><div style="%s">%s</div></div>') % (CORE_PANEL, left, card, top + mid + money)
    return section(inner, 'core')

ROLE_COL = {'CTO': ('rgba(99,213,255,0.14)', '#9FE6FF'), 'HRD': ('rgba(155,140,255,0.16)', '#C9C0FF'), 'CFO': ('rgba(242,193,78,0.14)', '#F7D88A'), 'CEO': ('rgba(242,193,78,0.14)', '#F7D88A')}

def role_tags(roles):
    return ''.join('<span style="padding: 4px 9px; border-radius: 7px; background: %s; color: %s; %s font-size: 12px; letter-spacing: 0.04em;">%s</span>' % (ROLE_COL[r][0], ROLE_COL[r][1], MONO, r) for r in roles)

def pains_variant(n):
    """Раунд 17: три варианта блока «Почему это важно» — главные боли CTO и HRD."""
    if n == 1:  # две колонки: CTO | HRD
        cols = [
            ('CTO', 'Вы отвечаете за разработку, но не видите её изнутри', [
                ('5–10%', 'кода успевает глубоко проверить тимлид. Остальное уходит в продакшен на доверии — а ИИ пишет код быстрее, чем его успевают ревьюить.', 'данные UpCore; Faros AI: +91% времени ревью'),
                ('18%', 'компаний измеряют эффект ИИ-инструментов. Остальные платят за лицензии и токены вслепую — хотя опытные разработчики с ИИ бывают на 19% медленнее.', 'LeadDev 2025; METR 2025'),
                ('20% → 4%', 'пятая часть команды даёт лишь 4% результата. В Jira всё зелёное, а релиз снова переносится.', 'данные UpCore')]),
            ('HRD', 'Вы принимаете решения о людях, опираясь на слова', [
                ('99%', 'работодателей в ИТ сталкиваются с накруткой опыта. На испытательном сроке её выявляют лишь в 2% случаев.', 'Хабр Карьера, 2025'),
                ('≈60%', 'разброса в оценках сотрудников объясняется личностью руководителя, а не работой. Повышают «за выслугу» и харизму.', 'Scullen et al.; HBR'),
                ('до 200%', 'годовой зарплаты стоит ошибка найма. А сильные уходят туда, где их рост видят и ценят.', 'SHRM')]),
        ]
        panels = []
        for role, title, items in cols:
            bg, fg = ROLE_COL[role]
            rows = ''.join('<div style="display: flex; flex-direction: column; gap: 8px; padding: 18px 0; border-top: 1px solid rgba(255,255,255,0.07);">'
                           '<div style="font-size: clamp(28px, 2.6vw, 38px); font-weight: 800; letter-spacing: -0.03em; line-height: 1; color: %s; white-space: nowrap;">%s</div>'
                           '<div><p style="margin: 0; color: rgba(255,255,255,0.86); font-size: 16px; line-height: 1.5;">%s</p>%s</div></div>' % (fg, e(b), e(tx), src_line(s)) for b, tx, s in items)
            panels.append('<article style="min-width: 0; border-radius: 28px; background: #1A1925; border: 1px solid rgba(255,255,255,0.08); padding: clamp(24px, 3vw, 36px);">'
                          '<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">%s</div>'
                          '<div style="font-size: clamp(22px, 2vw, 28px); font-weight: 800; line-height: 1.2; margin-bottom: 8px;">%s</div>%s</article>' % (role_tags([role]), e(title), rows))
        body = sec_head('ПОЧЕМУ ЭТО ВАЖНО', 'Разработка — самая дорогая статья расходов. И самая непрозрачная.') + '<div class="g2">%s</div>' % ''.join(panels)
    elif n == 2:  # шесть вопросов без ответа
        qs = [(['HRD', 'CTO'], 'Кто в команде реально тянет свой грейд?', '99% работодателей сталкиваются с накруткой опыта, а на испытательном сроке её ловят лишь в 2% случаев.'),
              (['CTO', 'CFO'], 'Окупается ли ИИ, за который вы платите?', 'Эффект ИИ-инструментов измеряют лишь 18% компаний. Ощущение ускорения и реальное ускорение расходятся на десятки процентов.'),
              (['HRD', 'CFO'], 'Сколько ФОТ уходит на работу без результата?', 'Около 5 млн ₽ в месяц на каждые 100 разработчиков: столько стоят 20% команды, которые дают лишь 4% результата.'),
              (['CTO'], 'Почему Jira зелёная, а релиз снова сдвинулся?', 'Статусы и дейлики показывают активность, а не результат в коде. Тимлид глубоко видит лишь 5–10% изменений.'),
              (['HRD', 'CTO'], 'Кто из удалёнщиков работает на двух работах сразу?', 'До 14% удалённых инженеров почти не создают результата, по данным Стэнфорда. Тайм-трекер этого не покажет, а код покажет.'),
              (['CTO', 'CFO'], 'Сколько на самом деле стоит работа подрядчика?', 'Акт на 1500 часов принимают на веру: проверить, сколько работы реально в коде, нечем.')]
        cards = ''.join(card('<div style="display: flex; flex-wrap: wrap; gap: 6px;">%s</div><div style="font-size: clamp(20px, 1.8vw, 24px); font-weight: 800; line-height: 1.25;">%s</div>'
                             '<p style="margin: 0; color: rgba(255,255,255,0.74); font-size: 15px; line-height: 1.55;">%s</p>' % (role_tags(r), e(q), e(a)), pad='26px') for r, q, a in qs)
        body = sec_head('ПОЧЕМУ ЭТО ВАЖНО', 'Шесть вопросов, на которые у вас нет ответов в цифрах', 'UpCore отвечает на каждый — по коду, без отчётов, анкет и тайм-трекеров.') + '<div class="g3">%s</div>' % cards
    else:  # цена непрозрачности
        items = [(['CTO', 'CFO'], '≈5 млн ₽', 'в месяц стоят 20% неэффективных на каждые 100 разработчиков — и это не видно ни в Jira, ни на дейликах', 'расчёт UpCore'),
                 (['HRD'], 'до 200%', 'годовой зарплаты стоит ошибка найма. 99% работодателей сталкиваются с накруткой опыта в резюме', 'SHRM; Хабр Карьера, 2025'),
                 (['CTO'], '+91%', 'времени на ревью с приходом ИИ: кода стало больше, а тимлиды тонут в проверке сгенерированного', 'Faros AI, 2025'),
                 (['HRD', 'CTO'], '210 ч', 'в год тратит каждый руководитель на performance review — и оценка всё равно субъективна', 'CEB / Gartner')]
        cards = ''.join(card('<div style="display: flex; flex-wrap: wrap; gap: 6px;">%s</div><div style="font-size: clamp(36px, 3.4vw, 52px); font-weight: 800; letter-spacing: -0.03em; line-height: 1; color: %s; white-space: nowrap;">%s</div>'
                             '<p style="margin: 0; color: rgba(255,255,255,0.86); font-size: 16px; line-height: 1.5;">%s</p>%s' % (role_tags(r), RED_T, e(b), e(tx), src_line(s)), pad='26px') for r, b, tx, s in items)
        strip = ('<div style="margin-top: 16px; border-radius: 22px; background: rgba(99,213,255,0.08); border: 1px solid rgba(99,213,255,0.4); padding: 20px 26px; display: flex; flex-wrap: wrap; gap: 8px 24px; align-items: center; justify-content: space-between;">'
                 '<span style="font-size: clamp(18px, 1.6vw, 22px); font-weight: 800;">Каждый месяц без данных — это реальные деньги.</span>'
                 '<span style="font-size: 16px; color: rgba(255,255,255,0.8);">UpCore показывает их по коду — в часах и рублях.</span></div>')
        body = sec_head('ЦЕНА НЕПРОЗРАЧНОСТИ', 'Пока у вас нет данных, вы платите за это каждый месяц') + '<div class="g4">%s</div>%s' % (cards, strip)
    return section(body, 'pains')

def pains_board(n):
    names = {1: 'CTO и HRD', 2: 'Шесть вопросов', 3: 'Цена непрозрачности'}
    return page('UpCore — блок «Почему это важно» %d (%s)' % (n, names[n]), '<div style="padding-top: 48px;">%s</div>' % pains_variant(n), 700, name='Pains-%d' % n)

TRUST_H2 = 'Не тайм-трекер. Не слежка. Не KPI по строкам кода.'
TRUST_LEAD = 'Это не токсичный контроль, а обычное классическое код-ревью — только его делает цифровой тимлид. По каждому MR, без усталости и любимчиков. И гораздо точнее.'
PILLARS = [('100+ задач подряд', 'Оценка строится по сотне задач: на дистанции статистика сглаживает любые аномалии.'),
           ('Математика, а не LLM', 'Детерминированная модель не «галлюцинирует»: один и тот же код — всегда одна и та же оценка.'),
           ('«Глаз» и апелляции', 'Любой вывод открывается до строчки кода, а сотрудник может оспорить оценку.'),
           ('1500+ разработчиков', 'Модели откалиброваны на экспертных оценках под каждый стек и проверены на сотнях проектов.')]

def trust_variant(n):
    """Раунд 20: «Принцип» + «Почему этой оценке можно доверять» в одном блоке, три варианта."""
    head = ('<div style="%s font-size: 13px; color: #63D5FF; letter-spacing: 0.04em; margin-bottom: 14px;">ПРИНЦИП</div>'
            '<h2 style="margin: 0; font-size: clamp(30px, 3.2vw, 48px); letter-spacing: -0.03em; line-height: 1.06; font-weight: 800; max-width: 900px;">%s</h2>'
            '<p style="margin: 16px 0 0; font-size: clamp(17px, 1.4vw, 20px); line-height: 1.55; color: rgba(255,255,255,0.84); max-width: 760px;">%s</p>') % (MONO, e(TRUST_H2), e(TRUST_LEAD))
    big96 = ('<div style="min-width: 0;"><div style="font-size: clamp(88px, 10vw, 152px); font-weight: 800; color: #63D5FF; line-height: 0.9; letter-spacing: -0.04em;">96%%</div>'
             '<div style="font-size: 20px; color: rgba(255,255,255,0.88); margin-top: 10px;">совпадение с экспертной оценкой</div>%s</div>')
    if n == 1:  # принцип сверху, ниже 96% слева и 4 опоры 2×2 справа
        pil = ''.join('<div style="min-width: 0; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); padding: 20px;"><div style="font-size: 19px; font-weight: 800; margin-bottom: 6px;">%s</div>'
                      '<div style="color: rgba(255,255,255,0.74); font-size: 15px; line-height: 1.5;">%s</div></div>' % (e(a), e(b)) for a, b in PILLARS)
        inner = ('<div style="border-radius: 40px; background: #12111C; border: 1px solid rgba(255,255,255,0.08); padding: clamp(28px, 4vw, 56px); display: flex; flex-direction: column; gap: 36px;">%s'
                 '<div style="display: flex; flex-wrap: wrap; gap: 32px 48px; align-items: center; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 36px;">'
                 '<div style="flex: 0 1 320px;">%s</div><div class="g2" style="flex: 1 1 520px; min-width: 0;">%s</div></div></div>') % (head, big96 % '', pil)
    elif n == 2:  # сравнение: живой тимлид / цифровой тимлид
        rows = [('Проверяет кода', '5–10%', '100%'), ('Время на один MR', 'часы', '≈ 1 секунда'),
                ('Точность', '«4 часа или 8?» — зависит от того, кто оценивает', '96% от экспертной оценки'),
                ('Стабильность', 'устаёт, спешит, есть любимчики', 'одна шкала на 100+ задачах'),
                ('Проверяемость', '«я так вижу»', 'расчёт до строчки кода и апелляция')]
        trs = ''.join('<tr><th scope="row" style="text-align: left; padding: 14px 16px 14px 0; font-weight: 600; color: rgba(255,255,255,0.7); font-size: 15px; border-top: 1px solid rgba(255,255,255,0.08); vertical-align: top;">%s</th>'
                      '<td style="padding: 14px 16px; color: rgba(255,255,255,0.72); font-size: 16px; border-top: 1px solid rgba(255,255,255,0.08); vertical-align: top;">%s</td>'
                      '<td style="padding: 14px 16px; font-weight: 800; font-size: 17px; color: #FFFFFF; background: rgba(99,213,255,0.07); border-top: 1px solid rgba(99,213,255,0.25); vertical-align: top;">%s</td></tr>' % (e(a), e(b), e(c)) for a, b, c in rows)
        table = ('<div style="overflow-x: auto;"><table class="uc-cmp" style="width: 100%%; border-collapse: collapse;"><thead><tr><th></th>'
                 '<th scope="col" style="text-align: left; padding: 0 16px 12px; %s font-size: 12px; color: rgba(255,255,255,0.55); font-weight: 400;">ЖИВОЙ ТИМЛИД</th>'
                 '<th scope="col" style="text-align: left; padding: 0 16px 12px; %s font-size: 12px; color: #63D5FF; font-weight: 400;">ЦИФРОВОЙ ТИМЛИД UPCORE</th></tr></thead><tbody>%s</tbody></table></div>') % (MONO, MONO, trs)
        inner = ('<div style="border-radius: 40px; background: #12111C; border: 1px solid rgba(255,255,255,0.08); padding: clamp(28px, 4vw, 56px); display: flex; flex-direction: column; gap: 32px;">%s%s</div>') % (head, table)
    else:  # компактно: принцип слева, 96% справа, строка из 4 доказательств
        proofs = [('100+', 'задач в каждой оценке'), ('50+', 'факторов в каждом MR'), ('1500+', 'разработчиков в калибровке'), ('100%', 'выводов открываются в «Глазе»')]
        cells = ''.join('<div style="min-width: 0;"><div style="font-size: clamp(28px, 2.6vw, 38px); font-weight: 800; letter-spacing: -0.02em; white-space: nowrap;">%s</div>'
                        '<div style="font-size: 14px; color: rgba(255,255,255,0.7); margin-top: 4px;">%s</div></div>' % (e(a), e(b)) for a, b in proofs)
        inner = ('<div style="border-radius: 40px; background: #12111C; border: 1px solid rgba(255,255,255,0.08); padding: clamp(28px, 4vw, 56px); display: flex; flex-direction: column; gap: 32px;">'
                 '<div style="display: flex; flex-wrap: wrap; gap: 32px 56px; align-items: center;"><div style="flex: 1.4 1 480px; min-width: 0;">%s</div><div style="flex: 0 1 320px;">%s</div></div>'
                 '<div class="g4m2" style="border-top: 1px solid rgba(255,255,255,0.08); padding-top: 28px;">%s</div></div>') % (head, big96 % '<div style="font-size: 14px; color: rgba(255,255,255,0.6); margin-top: 8px;">даже два сильных лида расходятся: один скажет 4 часа, другой — 8</div>', cells)
    return section(inner, 'trust')

# ---------------------------------------------------------------- раунд 23: «Принцип + точность» с 50+ факторами и очисткой от шума
WITHOUT = ['Без тайм-трекеров', 'Без скриншотов экрана', 'Без отчётов от разработчиков', 'Без субъективных оценок']
FACTORS = ['Сложность задачи', 'Технологии и их грейд', 'Результирующий код (churn)', 'Архитектурная сложность',
           'Уровень багов и переделок', 'Когнитивная сложность', 'Логическая сложность', 'Цикломатическая сложность', 'Качество кода и ревью']
NOISE = ['Автогенерация', 'Копипаст', 'Бойлерплейт', 'Синтаксис и форматирование', 'Переименования']
CHIP = 'display: inline-flex; align-items: center; min-height: 32px; padding: 4px 12px; border-radius: 16px; font-size: 14px; line-height: 1.3;'

def chips(items, kind='factor', more=None):
    if kind == 'factor':
        st = CHIP + ' background: rgba(99,213,255,0.08); border: 1px solid rgba(99,213,255,0.3); color: #FFFFFF;'
    elif kind == 'noise':
        st = CHIP + ' background: rgba(232,101,101,0.08); border: 1px dashed rgba(232,101,101,0.5); color: %s; text-decoration: line-through; text-decoration-color: rgba(240,138,138,0.7);' % RED_T
    else:  # without
        st = CHIP + ' background: rgba(83,192,77,0.08); border: 1px solid rgba(83,192,77,0.35); color: #9BE397;'
    out = ''.join('<span style="%s">%s</span>' % (st, e(x)) for x in items)
    if more:
        out += '<span style="%s color: rgba(255,255,255,0.6); border: 1px solid rgba(255,255,255,0.12);">%s</span>' % (CHIP, e(more))
    return '<div style="display: flex; flex-wrap: wrap; gap: 8px;">%s</div>' % out

def trust_head(with_chips=True):
    return ('<div style="%s font-size: 13px; color: #63D5FF; letter-spacing: 0.04em; margin-bottom: 14px;">ПРИНЦИП</div>'
            '<h2 style="margin: 0; font-size: clamp(30px, 3.2vw, 48px); letter-spacing: -0.03em; line-height: 1.06; font-weight: 800; max-width: 900px;">%s</h2>'
            '<p style="margin: 16px 0 0; font-size: clamp(17px, 1.4vw, 20px); line-height: 1.55; color: rgba(255,255,255,0.84); max-width: 760px;">%s</p>%s') % (
                MONO, e(TRUST_H2), e(TRUST_LEAD), ('<div style="margin-top: 20px;">%s</div>' % chips(WITHOUT, 'without')) if with_chips else '')

def big_96(size='clamp(88px, 10vw, 152px)', note=True):
    return ('<div style="min-width: 0;"><div style="font-size: %s; font-weight: 800; color: #63D5FF; line-height: 0.9; letter-spacing: -0.04em;">96%%</div>'
            '<div style="font-size: 20px; color: rgba(255,255,255,0.88); margin-top: 10px;">точность экспертной оценки</div>%s</div>') % (
                size, '<div style="font-size: 15px; color: rgba(255,255,255,0.66); margin-top: 8px; line-height: 1.45;">на более чем 300 тыс. MR</div>' if note else '')

TRUST_BOX = 'border-radius: 40px; background: #12111C; border: 1px solid rgba(255,255,255,0.08); padding: clamp(28px, 4vw, 56px); display: flex; flex-direction: column; gap: 36px;'

def trust_v4(n):
    """Раунд 23: три варианта на основе Trust-1 + 50+ факторов и очистка от шума; упор на точность и отсутствие токсичности."""
    if n == 1:  # раунд 24: принят; 96% (на 300 тыс. MR) слева, четыре опоры 2×2 справа
        pillars = [
            ('50+ факторов оценки', 'Сложность задачи, технологии, результирующий код (churn), архитектурная сложность, уровень багов, когнитивная и логическая сложность — и ещё десятки параметров.'),
            ('Глубокая очистка от шума', 'Автогенерация, копипаст, бойлерплейт, синтаксис, переименования не добавляют ни часа. В оценку идёт только значимый код.'),
            ('Математика, а не LLM', 'Детерминированная модель не «галлюцинирует»: один и тот же код — всегда одна и та же оценка.'),
            ('1500+ разработчиков', 'Модели откалиброваны на экспертных оценках под каждый стек и проверены на сотнях проектов.')]
        pil = ''.join('<div style="min-width: 0; border-radius: 20px; border: 1px solid %s; background: %s; padding: 20px;"><div style="font-size: 19px; font-weight: 800; margin-bottom: 6px;">%s</div>'
                      '<div style="color: rgba(255,255,255,0.74); font-size: 15px; line-height: 1.5;">%s</div></div>' % (
                          'rgba(99,213,255,0.35)' if i < 2 else 'rgba(255,255,255,0.1)', 'rgba(99,213,255,0.05)' if i < 2 else 'transparent', e(a), e(b)) for i, (a, b) in enumerate(pillars))
        inner = ('<div style="%s">%s<div style="display: flex; flex-wrap: wrap; gap: 32px 48px; align-items: center; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 36px;">'
                 '<div style="flex: 0 1 300px;">%s</div><div class="g2" style="flex: 1 1 560px; min-width: 0;">%s</div></div></div>') % (TRUST_BOX, trust_head(), big_96(), pil)
    elif n == 2:  # конвейер точности: шум → 50+ факторов → 96%, внизу — почему это не токсично
        def step(num, title, text, body):
            return ('<div style="min-width: 0; border-radius: 24px; background: #1A1925; border: 1px solid rgba(255,255,255,0.08); padding: 24px; display: flex; flex-direction: column; gap: 14px;">'
                    '<div style="%s font-size: 13px; color: #63D5FF;">%s</div><div style="font-size: 22px; font-weight: 800; letter-spacing: -0.01em; line-height: 1.2;">%s</div>'
                    '<p style="margin: 0; color: rgba(255,255,255,0.74); font-size: 15px; line-height: 1.5;">%s</p>%s</div>') % (MONO, num, e(title), e(text), body)
        s1 = step('01 / ОЧИСТКА', 'Убираем шум', 'Перед оценкой код проходит глубокую очистку: всё, что не требует мысли разработчика, не добавляет часов.', chips(NOISE, 'noise', 'и другой шум'))
        s2 = step('02 / ОЦЕНКА', 'Считаем по 50+ факторам', 'Каждый значимый фрагмент кода переводится в человеко-часы с учётом его реальной сложности и ценности.', chips(FACTORS[:7], 'factor', 'и ещё 40+'))
        s3 = step('03 / ПРОВЕРКА', 'Сверяем с экспертами', 'Модели откалиброваны на 1500+ разработчиках, а оценка складывается из 100+ задач. Детерминированная математика: один и тот же код — одна оценка.',
                  big_96('clamp(64px, 6vw, 88px)', note=False))
        nt = [('Оцениваем код, а не людей', 'Ни трекеров, ни скриншотов, ни отчётов — разработчик просто работает.'),
              ('Как обычное код-ревью', 'Около секунды на MR, без вмешательства в процесс.'),
              ('Прозрачно до строчки', 'Каждый вывод открывается в «Глазе»: видно, за что и сколько.'),
              ('Можно оспорить', 'Апелляция по любой оценке. Правила одни для всех.')]
        ntc = ''.join('<div style="min-width: 0;"><div style="font-size: 17px; font-weight: 800; margin-bottom: 6px; color: #9BE397;">%s</div><div style="color: rgba(255,255,255,0.72); font-size: 15px; line-height: 1.5;">%s</div></div>' % (e(a), e(b)) for a, b in nt)
        inner = ('<div style="%s">%s<div class="g3">%s%s%s</div>'
                 '<div style="border-top: 1px solid rgba(255,255,255,0.08); padding-top: 28px;"><div style="%s font-size: 13px; color: #9BE397; letter-spacing: 0.04em; margin-bottom: 18px;">ПОЧЕМУ ЭТО НЕ ТОКСИЧНО</div><div class="g4">%s</div></div></div>') % (
                     TRUST_BOX, trust_head(False), s1, s2, s3, MONO, ntc)
    else:  # две колонки: «Почему точно» и «Почему не токсично»
        def item(title, body):
            return '<div style="display: flex; flex-direction: column; gap: 10px; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 18px;"><div style="font-size: 19px; font-weight: 800;">%s</div>%s</div>' % (e(title), body)
        P = lambda t: '<p style="margin: 0; color: rgba(255,255,255,0.74); font-size: 15px; line-height: 1.55;">%s</p>' % e(t)
        left = ('<div style="min-width: 0; border-radius: 28px; background: #1A1925; border: 1px solid rgba(99,213,255,0.3); padding: clamp(24px, 3vw, 36px); display: flex; flex-direction: column; gap: 20px;">'
                '<div style="%s font-size: 13px; color: #63D5FF; letter-spacing: 0.04em;">ПОЧЕМУ ОЦЕНКА ТОЧНАЯ</div>%s%s%s%s</div>') % (
                    MONO, big_96('clamp(72px, 7vw, 104px)'),
                    item('50+ факторов оценки', chips(FACTORS[:7], 'factor', 'и ещё 40+')),
                    item('Глубокая очистка от шума', chips(NOISE, 'noise', 'и другой шум') + P('Сгенерировал 1000 строк и через неделю удалил 950? В оценку пойдут только 50, которые остались в проекте.')),
                    item('100+ задач и 1500+ разработчиков', P('Оценка складывается на дистанции, а модели откалиброваны на экспертных оценках под каждый стек. В ядре — математика, а не LLM: один код — одна оценка.')))
        nt = [('Никаких трекеров, скриншотов и отчётов', 'Разработчик просто пишет код. Система смотрит только на результат в репозитории.'),
              ('Обычное код-ревью', 'То же, что делает тимлид, только по каждому MR и примерно за секунду.'),
              ('Одна шкала для всех', 'Без любимчиков, усталости и «я так вижу». Сильных видно сразу, даже тихих.'),
              ('Прозрачно до строчки', 'Каждый вывод открывается в «Глазе»: видно, какой код и сколько часов дал.'),
              ('Апелляция по любой оценке', 'Не согласен — оспорь. Решение принимает человек, а не алгоритм.'),
              ('Для роста, а не для наказания', 'UpCore.Mentor превращает оценку в персональный план развития.')]
        right = ('<div style="min-width: 0; border-radius: 28px; background: #1A1925; border: 1px solid rgba(83,192,77,0.3); padding: clamp(24px, 3vw, 36px); display: flex; flex-direction: column; gap: 20px;">'
                 '<div style="%s font-size: 13px; color: #9BE397; letter-spacing: 0.04em;">ПОЧЕМУ ЭТО НЕ ТОКСИЧНЫЙ КОНТРОЛЬ</div>%s</div>') % (MONO, ''.join(item(a, P(b)) for a, b in nt))
        inner = '<div style="%s">%s<div class="g2" style="align-items: stretch;">%s%s</div></div>' % (TRUST_BOX, trust_head(False), left, right)
    return section(inner, 'trust')

def block_board(prefix, n, html, title):
    return page('UpCore — %s %d' % (title, n), '<div style="padding-top: 48px;">%s</div>' % html, 900, name='%s-%d' % (prefix, n))

def core_board(n):
    names = {1: 'Формула', 2: 'Конвейер', 3: 'Контраст', 4: 'Ценность, а не строки', 5: 'Обычные метрики против UpCore', 6: '160 ч → 80 ч',
             7: 'Полоса ценность / потери', 8: 'Месяц — 20 рабочих дней', 9: 'Кольцо 80 из 160', 10: 'Кольцо, 50% в центре', 11: 'Два кольца', 12: 'Спидометр'}
    body = '<div style="padding-top: 48px;">%s</div>' % (core_variant(n) if n <= 3 else core_v2(n) if n <= 6 else core_v3(n) if n <= 9 else core_v4(n))
    return page('UpCore — блок «Сердце» %d (%s)' % (n, names[n]), body, 600, name='Core-%d' % n)

SEC_CARDS = [
    ('Вход через GitHub или GitLab', 'Подключите репозиторий — и получите первые оценки по истории проекта. Код, написанный за год, анализируется за несколько минут.'),
    ('Код не покидает ваш контур', 'Локальный агент анализирует код на вашей стороне. На сервер уходят только метрики — исходники никуда не передаются.'),
    ('On-premise без интернета', 'Полностью в вашей инфраструктуре, в закрытом контуре. Нужен только read-only доступ к Git. GPU не нужны.'),
    ('Права и конфиденциальность', 'Гибкие роли, вход через SSO и режим «скрыть чувствительные данные»: зарплаты и рейтинги видят только те, кому положено.'),
    ('Любой стек', 'C#, Java, Go, Python, Kotlin, PHP, JS/TS, C++ и 1С. Интеграции с GitLab, GitHub и Jira.'),
    ('Платите за подтверждённый результат', 'Бесплатный пилот на 2–3 ваших проектах. Оплата — только после того, как вы подтвердите точность на своих данных.'),
]

def security(full=True, h2='Подключение за минуты. Код остаётся у вас.', home=False):
    items = SEC_CARDS if full else [SEC_CARDS[1], SEC_CARDS[2], SEC_CARDS[5]]
    if home:  # раунд 28: на главной без «Код не покидает ваш контур» и «Права и конфиденциальность», сетка 2×2
        items = [SEC_CARDS[0], SEC_CARDS[2], SEC_CARDS[4], SEC_CARDS[5]]
        cards = ''.join(card('<div style="font-size: 21px; font-weight: 700;">%s</div><p style="margin: 0; color: rgba(255,255,255,0.74); font-size: 16px; line-height: 1.55;">%s</p>' % (e(t), e(p))) for t, p in items)
        return section(sec_head('SAAS И БЕЗОПАСНОСТЬ', h2) + '<div class="g2">%s</div>' % cards)
    cards = ''.join(card('<div style="font-size: 21px; font-weight: 700;">%s</div><p style="margin: 0; color: rgba(255,255,255,0.74); font-size: 16px; line-height: 1.55;">%s</p>' % (e(t), e(p))) for t, p in items)
    return section(sec_head('SAAS И БЕЗОПАСНОСТЬ', h2) + '<div class="g3">%s</div>' % cards)

def cta(h2, sub, primary=('Регистрация', REG), secondary=('office@dex-it.ru', MAIL)):
    inner = ('<div style="position: relative; overflow: hidden; border-radius: 40px; background: #63D5FF; color: #0D0C15; padding: clamp(32px, 5vw, 72px); display: flex; flex-wrap: wrap; gap: 32px; align-items: center; justify-content: space-between;">'
             '<div style="flex: 1 1 520px; min-width: 0;"><h2 style="margin: 0; font-size: clamp(30px, 3.4vw, 52px); letter-spacing: -0.03em; line-height: 1.05; font-weight: 800;">%s</h2><p style="margin: 16px 0 0; font-size: 18px; line-height: 1.5; color: rgba(13,12,21,0.8);">%s</p></div>'
             '<div style="display: flex; flex-wrap: wrap; gap: 12px;">%s%s</div></div>') % (e(h2), e(sub), btn(primary[0], primary[1], True, True), btn(secondary[0], secondary[1], False, True))
    return section(inner, pb=72)

def footer():
    return ('<footer style="border-top: 1px solid rgba(255,255,255,0.08); background: #171620;"><div style="max-width: 1280px; margin: 0 auto; padding: 32px; display: flex; flex-wrap: wrap; gap: 24px; justify-content: space-between; align-items: center; font-size: 14px; color: rgba(255,255,255,0.7);">'
            '<img src="%s" alt="UpCore" style="height: 22px; width: auto;"><span>Продукт компании Dex · +7 (985) 848-35-55 · office@dex-it.ru · @upcore_ai</span></div></footer>') % src('logo')

PRODUCT_TEXTS = {  # раунд 20: три варианта абзаца и 3 пунктов в карточках продуктов
 1: ('РЕЗУЛЬТАТ ДЛЯ БИЗНЕСА', {
   'grade': ('Реальный грейд и эффективность каждого разработчика — в часах и рублях, по коду за 3 месяца. Видно, кто тянет свой уровень, а кто живёт на накрученном резюме.',
             ['+12% к производительности команды от прозрачных правил', '≈5 млн ₽ в месяц на 100 разработчиков — потери от 20% неэффективных', 'Грейд новичка подтверждён до конца испытательного срока']),
   'ai': ('Сколько часов на самом деле экономит ИИ — по каждому разработчику, команде и инструменту. И где он вместо ускорения плодит переделки и техдолг.',
          ['Senior с ИИ: +50–100%, Junior: до −50%', '×1,9 отдачи на рубль, когда лицензии идут туда, где есть эффект', 'Отчёт «до и после ИИ» — сразу, по истории Git']),
   'projects': ('Объективная стоимость кода в часах и рублях — сверьте с актами подрядчика, бюджетом и сроками. Разовый аудит без внедрения.',
                ['−75% к оплате в примере аудита акта', 'Бюджет всего проекта по коду — за 2 дня', 'Прогноз сроков и риск сорвать дедлайн']),
   'mentor': ('Персональный ИИ-наставник для каждого разработчика: разбирает MR, задачи и промпты и показывает, что исправить, чтобы вырасти.',
              ['114 часов ручного ревью в месяц экономии', 'Качество кода 6,0 → 8,0 после ревью', 'Лиду — 15 минут на критичное вместо часов']),
 }),
 2: ('ЧТО ВЫ УВИДИТЕ', {
   'grade': ('Цифровой тимлид оценивает каждого разработчика по реальной работе и выдаёт подтверждённый грейд Junior− … Senior — без анкет и собеседований.',
             ['Звезда компетенций по 10 осям и динамика роста', 'Рейтинг по компании, стеку и проекту, красная зона', 'Авто-резюме: реальный стек и уровень по коду']),
   'ai': ('Авто-детект ИИ-кода и промпт-коллектор показывают, кто и как работает с ИИ, сколько это экономит и сколько стоит.',
          ['Доля ИИ-кода в каждом MR', 'Время «вручную» и «с ИИ» по каждой задаче', 'Сессии, ходы и токены на задачу']),
   'projects': ('Трудоёмкость каждого MR складывается в полную картину проекта — от эффективности команды до техдолга.',
                ['Акт подрядчика против объективных часов', 'Рейтинг проектов, потери и прогноз сроков', 'Техдолг и тех-карта команды']),
   'mentor': ('ИИ-агенты ревьюят код, постановки задач и промпты, а из системных ошибок собирают персональный план развития.',
              ['ИИ-ревью кода в каждом MR', 'Ревью промптов и постановок задач', 'План роста и Топ-3 технологии для каждого']),
 }),
 3: ('КАКИЕ РЕШЕНИЯ ВЫ ПРИМЕТЕ', {
   'grade': ('Для CTO и HRD: повышения, зарплаты и испытательный срок — на фактах из кода, а не на впечатлениях и самооценке.',
             ['Кого повысить, а кому пересмотреть зарплату', 'Кто не тянет грейд — и что с этим делать', 'Прошёл ли новичок испытательный срок']),
   'ai': ('Для CTO и финансов: бюджет на ИИ, который можно защитить перед советом директоров — в часах и рублях.',
          ['Кому давать лицензии, а кому — обучение', 'Где ИИ ускоряет, а где плодит переделки', 'Продолжать ли тратить на токены — и сколько']),
   'projects': ('Для заказчиков, PMO и финансов: платите за результат в коде, а не за часы в акте.',
                ['Сколько проект стоит на самом деле', 'Переплачиваете ли вы подрядчику', 'Успеет ли команда к дедлайну']),
   'mentor': ('Для тимлидов и L&D: менторство, которое масштабируется на всю команду и не съедает время сеньоров.',
              ['Как быстрее вывести новичков на эффективность', 'Как разгрузить сеньоров от ревью', 'Что прокачать каждому для следующего грейда']),
 }),
}

def _products_items():
    return [
        ('grade', '01 / UPCORE GRADE', '«Кто в команде реально тянет свой грейд?»', 'Объективная оценка разработчика',
         'Эффективность в часах и рублях, подтверждённый грейд Junior− … Senior и рейтинг — по реальному коду за 3 месяца, а не по собеседованию и впечатлениям.',
         ['Грейд и звезда компетенций по 10 осям', 'Рейтинг по компании, стеку и проекту', 'Авто-резюме: реальный стек по коммитам'], 'Подробнее о Grade →'),
        ('ai', '02 / UPCORE AI', '«Окупаются ли ИИ-инструменты?»', 'Реальная эффективность ИИ и вайбкодинга',
         'Авто-детект ИИ-кода и промпт-коллектор показывают, кто и как работает с ИИ, сколько часов это экономит и сколько стоит каждый токен.',
         ['Время «вручную» и «с ИИ» по каждому MR', 'Сессии, ходы и токены на задачу', 'Базовая линия «до ИИ» — из истории Git'], 'Подробнее об AI →'),
        ('projects', '03 / UPCORE PROJECTS', '«Сколько на самом деле стоит проект?»', 'Бюджет проекта и контроль подрядчиков',
         'Считаем объективную стоимость кода в часах и рублях: сравните с актами, бюджетом и сроками. Разовый аудит — без внедрения.',
         ['Акт подрядчика против трудоёмкости кода', 'Прогноз сроков и риски дедлайна', 'Техдолг и тех-карта проекта'], 'Подробнее о Projects →'),
        ('mentor', '04 / UPCORE MENTOR', '«Как команде расти быстрее?»', 'ИИ-наставник для каждого разработчика',
         'Разбирает каждый MR, задачи и промпты, находит, где проседает эффективность, и даёт конкретные рекомендации — от ошибок в коде до плана развития.',
         ['ИИ-ревью кода и постановок задач', 'Ревью промптов: как работать с ИИ', 'Персональный план роста и Топ-3 технологии'], 'Подробнее о Mentor →'),
    ]

def products_2x2(variant=None):
    items = _products_items()
    ul_label = ''
    if variant:
        ul_label, texts = PRODUCT_TEXTS[variant]
        items = [(k, lab, q, tt) + texts[k] + (more,) for k, lab, q, tt, p0, l0, more in items]
    cards = []
    for key, lab, q, t, p, lis, more in items:
        line, txt = ACC[key]
        lab_html = ('<div style="%s font-size: 12px; letter-spacing: 0.06em; color: rgba(255,255,255,0.58); margin: 2px 0 -8px;">%s</div>' % (MONO, e(ul_label))) if ul_label else ''
        ul = '<ul style="margin: 0; padding-left: 20px; color: rgba(255,255,255,0.86); font-size: 16px; line-height: 1.8;">%s</ul>' % ''.join('<li>%s</li>' % e(x) for x in lis)
        cards.append('<article id="%s" style="min-width: 0; border-radius: 28px; background: #1A1925; border: 1px solid rgba(255,255,255,0.08); padding: clamp(24px, 3vw, 40px); display: flex; flex-direction: column; gap: 16px;">'
                     '<div style="%s font-size: 13px; color: %s;">%s</div>'
                     '<div style="font-size: 17px; color: rgba(255,255,255,0.62); font-style: italic;">%s</div>'
                     '<h3 style="margin: 0; font-size: clamp(26px, 2.3vw, 34px); letter-spacing: -0.02em; line-height: 1.1;">%s</h3>'
                     '<p style="margin: 0; color: rgba(255,255,255,0.78); line-height: 1.55; font-size: 17px;">%s</p>%s%s'
                     '<a href="#%s-page" style="margin-top: auto; font-weight: 600; text-decoration: none; min-height: 44px; display: inline-flex; align-items: center; color: %s;">%s</a></article>' % (
                         key, MONO, txt, e(lab), e(q), e(t), e(p), lab_html, ul, key, txt, e(more)))
    return section(sec_head('ПЛАТФОРМА UPCORE', 'Одна платформа. Четыре ответа для бизнеса.', 'Подключите репозиторий один раз — и получите оценки по каждому направлению: люди, ИИ, проекты и рост команды.') +
                   '<div class="g2">%s</div>' % ''.join(cards), 'products')

PLATFORM = [  # раунд 21: модули с крупными названиями через точку, без тезисов, описание длиннее
    ('grade', 'Grade', '01', '«Кто в команде реально тянет свой грейд?»', 'Объективная оценка разработчика', 'CTO · HRD · тимлиды',
     'Цифровой тимлид разбирает каждый MR и переводит код в реально затраченные часы. Из них складываются эффективность, рейтинг и подтверждённый грейд Junior− … Senior для каждого разработчика. Повышения, зарплаты и испытательный срок решаются по фактам из кода, а не по резюме и впечатлениям.',
     'Подробнее о Grade →'),
    ('ai', 'AI', '02', '«Окупаются ли ИИ-инструменты?»', 'Реальная эффективность ИИ и вайбкодинга', 'CTO · CFO',
     'Авто-детект находит ИИ-код в каждом MR, а промпт-коллектор показывает, как разработчики работают с ассистентами. Вы видите, сколько часов ИИ на самом деле экономит каждому, где он плодит переделки и техдолг и окупается ли каждый рубль, потраченный на лицензии и токены.',
     'Подробнее об AI →'),
    ('projects', 'Projects', '03', '«Сколько на самом деле стоит проект?»', 'Бюджет проекта и контроль подрядчиков', 'CEO · PMO · CFO',
     'Трудоёмкость каждого MR складывается в объективную стоимость проекта в часах и рублях. Сверьте её с актами подрядчика, бюджетом и сроками — и найдите переплаты и риск сорвать дедлайн. Нужен разовый ответ — проведём аудит готового проекта без внедрения.',
     'Подробнее о Projects →'),
    ('mentor', 'Mentor', '04', '«Как команде расти быстрее?»', 'ИИ-наставник для каждого разработчика', 'тимлиды · L&D',
     'ИИ-наставник ревьюит код, постановки задач и промпты каждого разработчика и находит, где проседает эффективность. Из системных ошибок он собирает персональный план роста и разгружает сеньоров от рутинного ревью — менторство начинает работать на всю команду.',
     'Подробнее о Mentor →'),
]
PLATFORM_HEAD = ('ПЛАТФОРМА UPCORE', 'Одна платформа. Четыре ответа для бизнеса.', 'Подключите репозиторий один раз — и получите оценки по каждому направлению: люди, ИИ, проекты и рост команды.')

def mod_name(key, mod, size='clamp(34px, 8.6vw, 60px)', whole=False):
    """Название модуля через точку: UpCore.Grade — крупно, модуль акцентным цветом."""
    line, txt = ACC[key]
    head_col = txt if whole else '#FFFFFF'
    return ('<div style="font-family: \'Bricolage Grotesque\', \'Onest\', sans-serif; font-weight: 800; font-size: %s; line-height: 0.95; letter-spacing: -0.035em;">'
            '<span style="color: %s;">UpCore</span><span style="color: %s;">.<wbr>%s</span></div>') % (size, head_col, txt, mod)

def more_link(key, more):
    return ('<a href="#%s-page" style="font-weight: 600; text-decoration: none; min-height: 44px; display: inline-flex; align-items: center; color: %s;">%s</a>' % (key, ACC[key][1], e(more)))

P_DESC = 'margin: 0; color: rgba(255,255,255,0.8); line-height: 1.6; font-size: 17px;'

def platform_variant(n):
    if n == 4:  # вариант 2 раунда 20 («Что вы увидите») без тезисов
        items = [(k, lab, q, tt, PRODUCT_TEXTS[2][1][k][0], [], more) for k, lab, q, tt, p0, l0, more in _products_items()]
        cards = []
        for key, lab, q, t, p, lis, more in items:
            cards.append('<article style="min-width: 0; border-radius: 28px; background: #1A1925; border: 1px solid rgba(255,255,255,0.08); padding: clamp(24px, 3vw, 40px); display: flex; flex-direction: column; gap: 16px;">'
                         '<div style="%s font-size: 13px; color: %s;">%s</div>'
                         '<div style="font-size: 17px; color: rgba(255,255,255,0.62); font-style: italic;">%s</div>'
                         '<h3 style="margin: 0; font-size: clamp(26px, 2.3vw, 34px); letter-spacing: -0.02em; line-height: 1.1;">%s</h3>'
                         '<p style="margin: 0; color: rgba(255,255,255,0.78); line-height: 1.55; font-size: 17px;">%s</p>'
                         '<div style="margin-top: auto;">%s</div></article>' % (MONO, ACC[key][1], e(lab), e(q), e(t), e(p), more_link(key, more)))
        body = '<div class="g2">%s</div>' % ''.join(cards)
    elif n == 1:  # «Имя вместо заголовка»: карточки 2×2, крупное UpCore.Модуль, вопрос, описание
        cards = []
        for key, mod, num, q, t, roles, p, more in PLATFORM:
            line = ACC[key][0]
            cards.append('<article style="min-width: 0; position: relative; overflow: hidden; border-radius: 28px; background: #1A1925; border: 1px solid rgba(255,255,255,0.08); border-top: 3px solid %s; padding: clamp(24px, 3vw, 40px); display: flex; flex-direction: column; gap: 18px;">'
                         '<div style="position: absolute; right: 0; top: 0; width: 240px; height: 240px; background: radial-gradient(circle at 100%% 0%%, %s33 0%%, transparent 65%%); pointer-events: none;"></div>'
                         '<div style="%s font-size: 13px; color: rgba(255,255,255,0.58);">%s</div>%s'
                         '<div style="font-size: 19px; color: rgba(255,255,255,0.92); font-style: italic; font-weight: 500;">%s</div>'
                         '<p style="%s">%s</p><div style="margin-top: auto;">%s</div></article>' % (
                             line, line, MONO, num, mod_name(key, mod), e(q), P_DESC, e(p), more_link(key, more)))
        body = '<div class="g2">%s</div>' % ''.join(cards)
    elif n == 2:  # «Оглавление»: четыре строки, слева огромное название и роли, справа заголовок и описание
        rows = []
        for key, mod, num, q, t, roles, p, more in PLATFORM:
            rows.append('<article class="uc-row" style="border-top: 1px solid rgba(255,255,255,0.1); padding: clamp(28px, 3.4vw, 44px) 0;">'
                        '<div style="min-width: 0; display: flex; flex-direction: column; gap: 14px;">'
                        '<div style="%s font-size: 13px; color: rgba(255,255,255,0.58);">%s / для: %s</div>%s</div>'
                        '<div style="min-width: 0; display: flex; flex-direction: column; gap: 12px;">'
                        '<h3 style="margin: 0; font-size: clamp(22px, 2vw, 28px); letter-spacing: -0.02em; line-height: 1.15;">%s</h3>'
                        '<div style="font-size: 17px; color: rgba(255,255,255,0.62); font-style: italic;">%s</div>'
                        '<p style="%s">%s</p><div>%s</div></div></article>' % (
                            MONO, num, e(roles), mod_name(key, mod, 'clamp(36px, 9vw, 72px)', whole=True), e(t), e(q), P_DESC, e(p), more_link(key, more)))
        body = '<div style="border-bottom: 1px solid rgba(255,255,255,0.1);">%s</div>' % ''.join(rows)
    else:  # n == 3 — «Шеврон»: карточка с цветной плашкой-названием, заголовком-обещанием и вопросом внизу
        cards = []
        for key, mod, num, q, t, roles, p, more in PLATFORM:
            line, txt = ACC[key]
            cards.append('<article style="min-width: 0; border-radius: 28px; background: linear-gradient(160deg, %s1F 0%%, #1A1925 45%%); border: 1px solid %s55; padding: clamp(24px, 3vw, 40px); display: flex; flex-direction: column; gap: 16px;">'
                         '<div style="display: flex; flex-wrap: wrap; gap: 8px 16px; justify-content: space-between; %s font-size: 13px; color: rgba(255,255,255,0.62);"><span>%s</span><span>%s</span></div>'
                         '<div style="display: flex; align-items: baseline; gap: 10px; min-width: 0;"><span style="font-family: \'Bricolage Grotesque\', sans-serif; font-weight: 800; font-size: clamp(30px, 7vw, 48px); color: %s; line-height: 1;">&gt;</span><div style="min-width: 0;">%s</div></div>'
                         '<h3 style="margin: 0; font-size: clamp(20px, 1.8vw, 24px); letter-spacing: -0.01em; line-height: 1.2; color: #FFFFFF;">%s</h3>'
                         '<p style="%s">%s</p>'
                         '<div style="margin-top: auto; display: flex; flex-wrap: wrap; gap: 8px 20px; align-items: center; justify-content: space-between; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 14px;">'
                         '<span style="font-size: 16px; color: rgba(255,255,255,0.62); font-style: italic;">%s</span>%s</div></article>' % (
                             line, line, MONO, num, e(roles), line, mod_name(key, mod, 'clamp(32px, 7.6vw, 54px)'), e(t), P_DESC, e(p), e(q), more_link(key, more)))
        body = '<div class="g2">%s</div>' % ''.join(cards)
    return section(sec_head(*PLATFORM_HEAD) + body, 'products')

# ---------------------------------------------------------------- специальные блоки продуктов
def grade_example():
    a = card('<div style="%s font-size: 12px; color: rgba(255,255,255,0.6);">рост · Лукьянов Александр</div>'
             '<div style="display: flex; flex-wrap: wrap; gap: 28px;">'
             '<div><div style="font-size: 13px; color: rgba(255,255,255,0.6);">Грейд</div><div style="font-size: 30px; font-weight: 800;"><span style="color: #F2C14E;">Middle+</span> → <span style="color: #63D5FF;">Senior</span></div></div>'
             '<div><div style="font-size: 13px; color: rgba(255,255,255,0.6);">Уровень работы</div><div style="font-size: 30px; font-weight: 800;">7,2 → 8,5</div></div>'
             '<div><div style="font-size: 13px; color: rgba(255,255,255,0.6);">Рейтинг в компании</div><div style="font-size: 30px; font-weight: 800;">#8 → #2</div></div></div>'
             '<p style="margin: 0; color: %s; font-size: 16px; line-height: 1.55;">Рост виден в цифрах — повышение обосновано данными, а не громкостью на дейликах.</p>' % (MONO, DIM), pad='32px', bg='#12111C', border='rgba(99,213,255,0.4)')
    b = card('<div style="%s font-size: 12px; color: rgba(255,255,255,0.6);">красная зона · пример из канала</div>'
             '<div style="display: flex; flex-wrap: wrap; gap: 28px;">'
             '<div><div style="font-size: 13px; color: rgba(255,255,255,0.6);">Эффективность</div><div style="font-size: 30px; font-weight: 800; color: #F08A8A;">24%%</div></div>'
             '<div><div style="font-size: 13px; color: rgba(255,255,255,0.6);">Сверх нормы</div><div style="font-size: 30px; font-weight: 800;">+102 ч</div></div>'
             '<div><div style="font-size: 13px; color: rgba(255,255,255,0.6);">Потери за месяц</div><div style="font-size: 30px; font-weight: 800; color: #F08A8A;">−202 тыс. ₽</div></div></div>'
             '<p style="margin: 0; color: %s; font-size: 16px; line-height: 1.55;">Переработки ≠ результат. UpCore показывает, где человек тонет, — пока это не стало увольнением или сорванным релизом.</p>' % (MONO, DIM), pad='32px', bg='#12111C', border='rgba(232,101,101,0.45)')
    return section(sec_head('ПРИМЕР', 'Одна методика — два очень разных сотрудника') + '<div class="g2">%s%s</div>' % (a, b))

def grade_axes():
    items = [('E', 'Эффективность', 'Часы результата против рабочего времени — по каждому MR.'),
             ('B', 'Сложность задач', 'Доля сложных и средних задач: senior не может жить на простых.'),
             ('A', 'Архитектура', 'Работа в ядре системы весит больше, чем в периферии (AST-граф связей).'),
             ('Q', 'Качество', 'Баги, переделки и замечания ревью — плотность на объём работы.')]
    cells = ''.join('<div style="min-width: 0; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); padding: 24px;"><div style="font-size: 44px; font-weight: 800; color: #63D5FF; line-height: 1;">%s</div><div style="font-size: 21px; font-weight: 700; margin: 12px 0 8px;">%s</div><div style="color: rgba(255,255,255,0.74); font-size: 15px; line-height: 1.55;">%s</div></div>' % (a, e(t), e(p)) for a, t, p in items)
    note = ('<div style="margin-top: 20px; border-radius: 20px; background: rgba(99,213,255,0.08); border: 1px solid rgba(99,213,255,0.4); padding: 24px; font-size: 17px; line-height: 1.55; color: rgba(255,255,255,0.86);">'
            'Итог — уровень 1–10 за 3 месяца, который переводится в грейд Junior− · Junior · Junior+ · Middle · Middle+ · Senior. '
            'Шум — копипаст, автогенерация, ренеймы — отсеивается; в зачёт идёт только результирующий код, который остался в продукте.</div>')
    return section(sec_head('МЕТОДИКА', 'Как считается грейд: 4 оси вместо одного мнения') + '<div class="g4">%s</div>%s' % (cells, note))

def ai_insight():
    bars = [('Senior + ИИ', '+50–100%', 100, '#53C04D', '#7FDB7A'), ('Middle + ИИ', '0…+20%', 30, '#F2C14E', '#F2C14E'), ('Junior + ИИ', 'до −50%', 55, '#E86565', '#F08A8A')]
    rows = ''.join('<div><div style="display: flex; justify-content: space-between; font-size: 18px; margin-bottom: 10px;"><span>%s</span><b style="color: %s;">%s</b></div>'
                   '<div style="height: 16px; border-radius: 8px; background: rgba(255,255,255,0.06); overflow: hidden;"><div style="width: %d%%; height: 100%%; background: %s;"></div></div></div>' % (e(a), t, e(b), w, c) for a, b, w, c, t in bars)
    left = card('<div style="%s font-size: 12px; color: rgba(255,255,255,0.6);">прирост эффективности с ИИ · данные UpCore</div>%s' % (MONO, rows), pad='32px', bg='#12111C', border='rgba(155,140,255,0.5)', gap=22)
    right = card('<p style="margin: 0; font-size: 19px; line-height: 1.55; color: rgba(255,255,255,0.88);">Средний прирост от ИИ на рынке — 10–20%%, а не 50–100%%, как обещают вендоры: половину ускорения съедают переделки.</p>'
                 '<p style="margin: 0; font-size: 17px; line-height: 1.55; color: %s;">Сильным инженерам ИИ даёт кратный рост. Слабым — иллюзию скорости, переделки и техдолг. UpCore показывает, где именно в вашей команде ИИ работает, а где — нет.</p>'
                 '<div style="border-top: 1px solid rgba(255,255,255,0.08); padding-top: 16px; font-size: 17px; line-height: 1.5;"><b style="color: #B9AEFF;">Кейс Dex:</b> 23%% MR пишутся с ИИ, их эффективность — 86%% против 64%% у ручных.</div>%s' % (DIM, src_line('Стэнфорд, 100 000+ разработчиков; данные UpCore')), pad='32px')
    return section(sec_head('ГЛАВНОЕ ОТКРЫТИЕ', 'Один и тот же ИИ ускоряет одних и тормозит других', None, 'ai') + '<div class="g2">%s%s</div>' % (left, right))

def projects_example():
    inner = ('<div style="display: flex; flex-direction: column; gap: 20px;">'
             '<div style="%s font-size: 12px; color: rgba(255,255,255,0.62);">аудит акта подрядчика · пример</div>'
             '<div><div style="display: flex; justify-content: space-between; font-size: 17px; margin-bottom: 8px;"><span>Выставлено в акте</span><b>160 ч</b></div><div style="height: 18px; border-radius: 6px; background: rgba(255,255,255,0.06); overflow: hidden;"><div style="width: 100%%; height: 100%%; background: rgba(255,255,255,0.35);"></div></div></div>'
             '<div><div style="display: flex; justify-content: space-between; font-size: 17px; margin-bottom: 8px;"><span>Объективно по коду (UpCore)</span><b style="color: #F2C14E;">40 ч</b></div><div style="height: 18px; border-radius: 6px; background: rgba(255,255,255,0.06); overflow: hidden;"><div style="width: 25%%; height: 100%%; background: #F2C14E;"></div></div></div>'
             '<div style="display: flex; flex-wrap: wrap; gap: 16px; align-items: center; justify-content: space-between;"><div style="padding: 12px 18px; border-radius: 14px; background: rgba(232,101,101,0.14); border: 1px solid rgba(232,101,101,0.5); font-size: 24px; font-weight: 800; color: #F08A8A;">−120 ч к оплате</div>'
             '<div style="font-size: 15px; color: rgba(255,255,255,0.74); max-width: 320px; line-height: 1.5;">Твёрдые аргументы для пересмотра сметы — по каждой строчке кода.</div></div>'
             '<div class="g3" style="border-top: 1px solid rgba(255,255,255,0.08); padding-top: 16px; font-size: 14px;">'
             '<div><div style="color: rgba(255,255,255,0.6);">UpCore Backend</div><div style="font-size: 24px; font-weight: 800;">10 127 ч</div><div style="color: rgba(255,255,255,0.6);">эффективных часов за месяц</div></div>'
             '<div><div style="color: rgba(255,255,255,0.6);">Техдолг</div><div style="font-size: 24px; font-weight: 800; color: #F2C14E;">35%%</div><div style="color: rgba(255,255,255,0.6);">дефектов ушло в main</div></div>'
             '<div><div style="color: rgba(255,255,255,0.6);">Мэтч команды</div><div style="font-size: 24px; font-weight: 800;">76%%</div><div style="color: rgba(255,255,255,0.6);">по тех-карте проекта</div></div></div></div>') % MONO
    left = card(inner, pad='32px', bg='#12111C', border='rgba(242,193,78,0.5)')
    right = card('<p style="margin: 0; font-size: 19px; line-height: 1.55; color: rgba(255,255,255,0.88);">UpCore считает объективную трудоёмкость каждого MR — сколько часов эта работа требует при данной сложности и стеке.</p>'
                 '<p style="margin: 0; font-size: 17px; line-height: 1.55; color: %s;">Сравнение с актом показывает разницу не «по ощущениям», а по каждой задаче: где работа заняла столько, сколько должна, а где часы ушли в никуда. Любую цифру можно открыть в «Глазе» до строчки кода.</p>'
                 '<p style="margin: 0; font-size: 17px; line-height: 1.55; color: %s;">Dex — сам ИТ-подрядчик — отдаёт своим клиентам отчёты UpCore вместо таблицы часов.</p>' % (DIM, DIM), pad='32px')
    return section(sec_head('ПРИМЕР', 'Акт против кода', None, 'projects') + '<div class="g2">%s%s</div>' % (left, right))

def scenarios():
    items = [('Разовый аудит проекта', 'Считаем бюджет всего проекта по коду: объективная стоимость разработки в часах и рублях, техдолг и риски. Без внедрения, отчёт — за 2 дня.',
              ['при приёмке проекта', 'перед продлением контракта', 'при покупке компании или инвестиции']),
             ('Ежемесячный контроль подрядчиков', 'Объективная трудоёмкость каждого MR против часов в акте. Эффективность каждого разработчика вендора и сравнение подрядчиков между собой и с in-house командой.',
              ['сверка актов', 'рейтинг подрядчиков', 'аргументы для сметы']),
             ('Управление портфелем проектов', 'Рейтинг проектов, прогноз сроков, потери в рублях, техдолг и тех-карта команды — для PMO и CTO в одном окне.',
              ['прогноз дедлайна', 'потери в ₽', 'техдолг по ISO 25010'])]
    cards = []
    for i, (t, p, tags) in enumerate(items, 1):
        tg = ''.join('<span style="padding: 6px 10px; border-radius: 8px; background: rgba(242,193,78,0.12); color: #F7D88A; font-size: 13px;">%s</span>' % e(x) for x in tags)
        cards.append(card('<div style="%s font-size: 13px; color: #F2C14E;">СЦЕНАРИЙ %02d</div><div style="font-size: 24px; font-weight: 800; line-height: 1.2;">%s</div><p style="margin: 0; color: %s; font-size: 16px; line-height: 1.55;">%s</p><div style="margin-top: auto; display: flex; flex-wrap: wrap; gap: 6px;">%s</div>' % (MONO, i, e(t), DIM, e(p), tg), pad='32px'))
    return section(sec_head('СЦЕНАРИИ', 'Три способа взять бюджет под контроль', None, 'projects') + '<div class="g3">%s</div>' % ''.join(cards))

def mentor_chat():
    msgs = [('#F08A8A', 'Уровень багов 5,1 / 10.', 'Переделано 60 из 123 MR (49%). Начни с самопроверки перед ревью — чек-лист ниже.'),
            ('#F2C14E', 'Код-ревью:', '0 замечаний в 442 MR команды. Подключись к ревью — это шаг к уровню лида.'),
            ('#7FDB7A', 'Изучи:', 'Multithreading Advanced — сложность 9, много в проекте, у тебя пока низкий уровень.'),
            ('#B9AEFF', 'Промпты:', 'в постановке не хватает контекста задачи — отсюда лишние ходы с ИИ. Шаблон постановки — в карточке.')]
    bubbles = ''.join('<div style="align-self: flex-start; max-width: 94%%; padding: 14px 16px; border-radius: 6px 18px 18px 18px; background: #1A1F1B; font-size: 16px; line-height: 1.5;"><b style="color: %s;">%s</b> %s</div>' % (c, e(a), e(b)) for c, a, b in msgs)
    left = card('<div style="display: flex; justify-content: space-between; %s font-size: 12px; color: rgba(255,255,255,0.62);"><span>ИИ-наставник · Лукьянов Александр</span><span class="uc-blink" style="color: #7FDB7A;">● пишет</span></div>%s'
                '<div style="margin-top: auto; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 14px;"><div style="display: flex; justify-content: space-between; font-size: 15px; margin-bottom: 8px;"><span>Качество кода по ревью</span><span>5,5 → <b style="color: #7FDB7A;">7,5</b> / 10</span></div><div style="height: 8px; border-radius: 4px; background: rgba(255,255,255,0.08); overflow: hidden;"><div style="width: 75%%; height: 100%%; background: #53C04D;"></div></div></div>' % (MONO, bubbles),
                pad='24px', bg='#0F1510', border='rgba(83,192,77,0.5)', gap=12)
    right = card('<p style="margin: 0; font-size: 19px; line-height: 1.55; color: rgba(255,255,255,0.88);">Не общие советы, а разбор именно вашего кода, задач и промптов — с цифрами и следующим шагом.</p>'
                 '<p style="margin: 0; font-size: 17px; line-height: 1.55; color: %s;">Наставник опирается на оценки UpCore и все артефакты разработчика. Системные ошибки превращаются в персональный план развития, а прогресс виден по звезде компетенций и динамике грейда.</p>'
                 '<p style="margin: 0; font-size: 17px; line-height: 1.55; color: %s;">Из строгого цифрового контролёра — в персонального наставника для каждого члена команды.</p>' % (DIM, DIM), pad='32px')
    return section(sec_head('КАК ЭТО ВЫГЛЯДИТ', 'Наставник, который знает ваш код', None, 'mentor') + '<div class="g2">%s%s</div>' % (left, right))

# ---------------------------------------------------------------- страницы
def home(variant):
    hv = {
        'A': dict(h1='Цифровой тимлид для [[автоматической оценки эффективности]] вашей разработки',
                  sub='UpCore переводит каждый Merge Request в реально затраченные человеко-часы. Видно, кто и сколько создаёт ценности, окупается ли ИИ и сколько на самом деле стоит проект — без отчётов, тайм-трекеров и слежки.',
                  st=[('96%', 'точность от экспертной оценки'), ('1500+', 'разработчиков уже посчитано'), ('50+', 'факторов в каждом MR'), ('1 сек', 'на проверку одного MR')], note=None),
        'B': dict(h1='ФОТ разработки — крупнейшая статья расходов. Сколько из неё [[превращается в результат?]]',
                  sub='UpCore анализирует каждый Merge Request по 50+ факторам и считает эффективность каждого разработчика, проекта и подрядчика — в часах и рублях. Без отчётов, тайм-трекеров и субъективных оценок.',
                  st=[('20% → 4%', '20% команды дают лишь 4% результата'), ('+12%', 'к производительности сразу — от прозрачности'), ('96%', 'точность от экспертной оценки')], note='данные UpCore по 1500+ разработчикам'),
        'C': dict(h1='ИИ пишет код быстрее, чем вы успеваете его проверить. [[UpCore успевает.]]',
                  sub='Живой тимлид глубоко проверяет 5–10% кода. Цифровой тимлид — 100%, по секунде на каждый Merge Request: реальная эффективность, грейд, отдача от ИИ и техдолг каждого разработчика.',
                  st=[('100%', 'кода проверено'), ('1 сек', 'на один Merge Request'), ('5–10%', 'успевает проверить человек')], note=None),
    }[variant]
    visual = slider_console() if MODE == 'dc' else static_slider_preview()
    st, note = HERO_STATS.get(('home', variant), (hv['st'], hv['note']))
    body = [header(None), hero('цифровой тимлид · онлайн', hv['h1'], hv['sub'], [btn('Подключить репозиторий', REG), btn('Заказать аудит', MAIL, False)], st, visual, note)]
    if variant != 'A':
        return page('UpCore — главная, первый экран ' + variant, '\n'.join(body), 1000, slider=True, name='Home-' + variant)
    body += [
        pains_variant(2),
        core_v3(9),
        platform_variant(3),  # раунд 22: принят вариант 3 «Шеврон»
        trust_v4(1),  # раунд 24: принят вариант 1 (без «100+ задач» и «Глаза»)
        results_v6(2),  # раунд 28: принят расчёт 2 (≈780 тыс. ₽ на разработчика)
        security(True, home=True),
        cta('Узнайте реальную эффективность команды уже сегодня', 'Подключите репозиторий или закажите аудит — первые результаты по истории вашего кода, без ожидания.', ('Подключить UpCore', REG)),
        footer()]
    return page('UpCore — главная A', '\n'.join(body), 5600, slider=True, name='Home-A')

def product_hero(key, v):
    return PRODUCTS[key]['heroes'][v]

PRODUCTS = {
 'grade': {
  'badge': 'UpCore Grade · для CTO, HRD и тимлидов',
  'heroes': {
   'A': dict(h1='Грейд, который подтверждает [[код]], а не собеседование',
             sub='UpCore оценивает каждого разработчика по реальной работе за 3 месяца: эффективность в часах и рублях, сложность задач, архитектурный вклад и качество кода. Объективный грейд Junior− … Senior, рейтинг и авто-резюме — без анкет, отчётов и субъективных ревью.',
             st=[('96%', 'совпадение с экспертной оценкой'), ('+12%', 'к производительности команды сразу'), ('≈5 млн ₽', 'в месяц стоят 20% неэффективных на 100 разработчиков')], note='данные и расчёт UpCore',
             img=('star', 'grade / звезда грейда', 'Уровень', 'звезда грейда по 10 осям и динамика роста')),
   'B': dict(h1='Резюме можно накрутить. [[Код — нет.]]',
             sub='99% работодателей в ИТ сталкивались с накруткой опыта, а на испытательном сроке её выявляют лишь в 2% случаев. UpCore Grade покажет реальный уровень сотрудника по его коду — уже в первые месяцы работы.',
             st=[('99%', 'работодателей знают о накрутке опыта'), ('27%', 'видели кандидатов с нейросетью на интервью'), ('2%', 'накруток выявляют на испытательном сроке')], note='Хабр Карьера, «Киберпротект», HR-клуб АПКИТ, 2025',
             img=('rating', 'grade / рейтинг', 'Рейтинг сотрудников', 'по компании, стеку и проекту')),
   'C': dict(h1='Performance review [[без споров]] и «любимчиков»',
             sub='Больше половины разброса в оценках сотрудников объясняется личностью оценивающего, а не работой. UpCore даёт руководителю, HR и разработчику одну и ту же цифру — с расчётом до строчки кода и правом на апелляцию.',
             st=[('1 шкала', 'для всей компании и всех стеков'), ('100+', 'задач в каждой оценке'), ('210 ч', 'в год тратит руководитель на ревью — можно меньше')], note='CEB / Gartner; Scullen, Mount, Goff, 2000',
             img=('efficiency', 'grade / эффективность', 'Эффективность специалиста', 'создано ценности в часах и рублях')),
  },
 },
 'ai': {
  'badge': 'UpCore AI · для руководителей, внедряющих ИИ',
  'heroes': {
   'A': dict(h1='Реальная эффективность [[внедрения ИИ]] в вашу разработку — в часах и рублях',
             sub='UpCore распознаёт ИИ-код в каждом MR, собирает промпты агентом на машине разработчика и сравнивает время «с ИИ» и «вручную». Видно, кто вайбкодит эффективно, а кто генерирует техдолг, — и сколько стоит каждый токен.',
             st=[('+22 п.п.', 'эффективность MR с ИИ против ручных — кейс Dex'), ('+50–100%', 'у Senior с ИИ — и до −50% у Junior'), ('0 мес.', 'ожидания: базовая линия — из истории Git')], note='данные UpCore',
             img=('company', 'ai / дашборд компании', 'Дашборд компании', 'доля MR с ИИ и ИИ-эффективность')),
   'B': dict(h1='Разработчики уверены, что ИИ их ускорил. [[Измерения]] часто говорят обратное',
             sub='В эксперименте METR опытные разработчики с ИИ работали на 19% дольше — и были уверены, что стали на 20% быстрее. UpCore AI измеряет реальный эффект ИИ по коду каждого разработчика, команды и инструмента.',
             st=[('−19%', 'реальная скорость с ИИ'), ('+20%', 'ощущаемое ускорение'), ('39 п.п.', 'разрыв между ощущением и фактом')], note='METR, рандомизированное исследование, 2025',
             img=('efficiency', 'ai / эффективность', 'Эффективность специалиста', 'создано через ИИ — в часах и рублях')),
   'C': dict(h1='Senior с ИИ: [[+50–100%]]. Junior с ИИ: до −50%',
             sub='Один и тот же ИИ-инструмент ускоряет одних и тормозит других. UpCore показывает, кому ИИ даёт результат, кому — переделки и техдолг, и сколько стоит каждый токен.',
             st=[('+50–100%', 'Senior с ИИ'), ('0…+20%', 'Middle с ИИ'), ('до −50%', 'Junior с ИИ')], note='данные UpCore',
             img=('quality', 'ai / качество', 'ИИ-ревью кода', 'дефекты по тяжести и блокам качества')),
  },
 },
 'projects': {
  'badge': 'UpCore Projects · для заказчиков, PMO и финансов',
  'heroes': {
   'A': dict(h1='Сколько на самом деле стоит ваш проект? [[Посчитаем по коду]]',
             sub='UpCore переводит код проекта в объективные человеко-часы и рубли. Сравните с актами подрядчика, бюджетом и сроками — и получите аргументы по каждой строчке кода. Разовый аудит — без внедрения.',
             st=[('2 дня', 'на быстрый аудит проекта'), ('−75%', 'к оплате в примере: акт 160 ч, по коду 40 ч'), ('≈1,6 млн ₽', 'в месяц переплаты у подрядчика из 10 человек при эффективности 60%')], note='пример расчёта UpCore',
             img=('techmap', 'projects / тех-карта', 'Тех-карта проекта', 'технологии, уровни и мэтч команды')),
   'B': dict(h1='В акте 160 часов. В коде — [[40]]. Кто прав?',
             sub='Проверяйте подрядчиков не на доверии. UpCore считает объективную трудоёмкость каждого MR и показывает, за что вы на самом деле платите, — с аргументами по каждой строчке кода.',
             st=[('160 ч', 'выставлено в акте'), ('40 ч', 'объективно по коду'), ('−120 ч', 'к оплате')], note='пример расчёта UpCore',
             img=('eye', 'projects / глаз', '«Глаз»', 'разбор каждого MR до строчки кода')),
   'C': dict(h1='Крупные ИТ-проекты в среднем выходят на [[45% дороже]] бюджета',
             sub='И дают на 56% меньше ценности, чем планировали. UpCore заранее показывает, где проект теряет деньги и сроки: реальная эффективность команды, техдолг и прогноз завершения.',
             st=[('+45%', 'к бюджету'), ('+7%', 'к срокам'), ('−56%', 'ценности от плана')], note='McKinsey и Оксфорд, 5400+ крупных ИТ-проектов',
             img=('timesheet', 'projects / табель', 'Табель', 'Jira, MR и коммиты в одном календаре')),
  },
 },
 'mentor': {
  'badge': 'UpCore Mentor · для тимлидов, L&D и разработчиков',
  'heroes': {
   'A': dict(h1='Персональный [[ИИ-наставник]] для каждого разработчика',
             sub='UpCore Mentor видит каждую задачу, промпт и строчку кода. Находит, где проседает эффективность, и даёт конкретные рекомендации — от ошибок в коде до персонального плана роста. Тимлид тратит время только на главное.',
             st=[('100%', 'MR проходят ИИ-ревью'), ('6,0 → 8,0', 'качество кода после ревью — из 10, демо'), ('15 мин', 'на критичные MR у лида вместо часов')], note=None,
             img=('quality', 'mentor / ревью', 'ИИ-ревью кода', 'дефекты по тяжести и блокам качества')),
   'B': dict(h1='Тимлид успевает менторить троих. [[UpCore Mentor]] — всю команду',
             sub='Ревью каждого MR, разбор системных ошибок и персональный план роста — автоматически, каждый день. Лид тратит 15 минут на критичное, а не часы на всё подряд.',
             st=[('100%', 'MR с разбором'), ('15 мин', 'на критичные MR у лида'), ('1 план', 'развития на каждого — по реальным ошибкам')], note=None,
             img=('star', 'mentor / уровень', 'Уровень', 'звезда компетенций и динамика роста')),
   'C': dict(h1='ИИ ускоряет работу, но может [[тормозить рост]]',
             sub='В эксперименте Anthropic разработчики, которые учились с ИИ, усвоили материал хуже: 50% против 67% в тесте. UpCore Mentor учит работать с ИИ так, чтобы расти: ревью промптов, постановок задач и кода.',
             st=[('50% / 67%', 'понимание с ИИ и без'), ('≥65%', 'у тех, кто спрашивал ИИ «почему»'), ('<40%', 'у тех, кто просто делегировал код')], note='Anthropic, рандомизированное исследование, 2026',
             img=('eye', 'mentor / глаз', '«Глаз»', 'разбор каждого MR до строчки кода')),
  },
 },
}

def product_top(key, v):
    p = PRODUCTS[key]; hv = p['heroes'][v]
    img, path, t, c = hv['img']
    ctas = [btn('Подключить репозиторий', REG), btn('Заказать аудит' if key == 'projects' else 'Получить демо-отчёт', MAIL, False)]
    if key == 'projects':
        ctas = [btn('Заказать аудит', MAIL), btn('Подключить репозиторий', REG, False)]
    st, note = HERO_STATS.get((key, v), (hv['st'], hv['note']))
    return [header(key), hero(p['badge'], hv['h1'], hv['sub'], ctas, st, image_console(img, path, t, c, key), note, key)]

def product(key, v):
    names = {'grade': 'Grade', 'ai': 'AI', 'projects': 'Projects', 'mentor': 'Mentor'}
    body = product_top(key, v)
    if v != 'A':
        return page('UpCore %s — первый экран %s' % (names[key], v), '\n'.join(body), 1000, name='%s-%s' % (names[key], v))
    if key == 'grade':
        body += [
            pains('ПРОБЛЕМА', 'Грейды сегодня ставят по словам, а платят за них деньгами', [
                ('99%', 'работодателей в ИТ знают о накрутке опыта в резюме, 64% сталкиваются с ней регулярно', 'Хабр Карьера, «Киберпротект», АПКИТ, 2025'),
                ('2%', '«накрученного» опыта выявляют на испытательном сроке — дальше компания платит за грейд, которого нет', 'там же'),
                ('≈60%', 'разброса в оценках сотрудников объясняется особенностями оценивающего, а не работой оцениваемого', 'Scullen, Mount, Goff, 2000'),
                ('20% → 4%', 'столько результата дают 20% наименее эффективных разработчиков — при полной зарплате', 'данные UpCore')], 'grade'),
            modules('ЧТО ВНУТРИ', 'Всё для решений о людях — на данных, а не на впечатлениях', [
                ('Эффективность в часах и рублях', 'Время UpCore против рабочего времени: создано ценности, упущенная выгода и реальная ставка за час результата.'),
                ('Подтверждённый грейд', 'Junior− … Senior по 4 осям: эффективность, сложность задач, архитектура и качество. Звезда компетенций по 10 осям и динамика роста.'),
                ('Рейтинг и красная зона', 'Рейтинг по компании, стеку и проекту. Сразу видно лидеров — и тех, кто 2 месяца подряд ниже нормы.'),
                ('Авто-резюме по коду', 'Какие технологии и на каком уровне человек реально использует. Цифровой паспорт опыта вместо слов в резюме.'),
                ('Онбординг и испытательный срок', 'За сколько недель новичок вышел на среднюю эффективность команды — решение по испытательному сроку на фактах.'),
                ('«Глаз» и апелляции', 'Расчёт до строчки кода. Сотрудник видит ту же оценку, что и руководитель, и может её оспорить.')], 'grade'),
            grade_axes(),
            results('grade'),
            grade_example(),
            roles('ДЛЯ КОГО', 'Одна цифра для CTO, HR, тимлида и разработчика', [
                ('CTO', 'Видит реальную силу команд и проектов, находит 20% неэффективных — и «звёздочек» для сложных задач.'),
                ('HRD', 'Повышения, пересмотр зарплат, калибровка грейдов и испытательный срок — на данных, а не на впечатлениях.'),
                ('Тимлид', 'Не тратит ~4 часа в месяц на оценку каждого разработчика и не спорит на ревью: у всех один расчёт.'),
                ('Разработчик', 'Никаких отчётов и тайм-трекеров. Вклад наконец виден, а путь к следующему грейду — понятен.')], 'grade'),
            faq([
                ('Это слежка за разработчиками?', 'Нет. Мы не считаем время в IDE, клики, скриншоты и активность в мессенджерах. Оценивается только результат — код, который вошёл в продукт.'),
                ('Разве код нельзя «накрутить»?', 'Строки и коммиты — можно. Поэтому UpCore отсеивает копипаст, автогенерацию и ренеймы, взвешивает код по архитектуре и учитывает только сохранившийся результат.'),
                ('А если оценка ошибётся?', 'Оценка строится по 100+ задачам, а не по одной. Любой вывод открывается в «Глазе» до строчки кода, а сотрудник может подать апелляцию.'),
                ('Как к этому отнесутся разработчики?', 'Сильные — с облегчением: отчёты не нужны, правила честные, вклад виден. Прозрачность сразу даёт команде в среднем +12% к производительности.')]),
            security(False, 'Данные о людях — под защитой'),
            cta('Узнайте реальный грейд своей команды', 'Подключите репозиторий — оценка по истории за 3 месяца, без ожидания и анкет.'),
            footer()]
    elif key == 'ai':
        body += [
            pains('ИИ-ПАРАДОКС', 'Ощущение ускорения — ещё не ускорение', [
                ('−19%', 'Опытные разработчики с ИИ работали на 19% дольше — и были уверены, что ускорились на 20%', 'METR, 2025'),
                ('+91%', 'Команды с ИИ мёржат на 98% больше PR, но время ревью растёт на 91% — узким местом становится человек', 'Faros AI, 10 000+ разработчиков, 2025'),
                ('×8', 'Дублирующегося кода с приходом ИИ стало в 8 раз больше, переписываний у активных ИИ-пользователей — в 9 раз', 'GitClear, 211 млн строк кода'),
                ('18%', 'компаний измеряют эффект ИИ-инструментов. Остальные платят за лицензии и токены вслепую', 'LeadDev AI Impact Report, 2025')], 'ai'),
            ai_insight(),
            modules('ЧТО ИЗМЕРЯЕМ', 'Полная картина работы с ИИ — от промпта до мёржа', [
                ('Авто-детект ИИ-кода', 'Доля MR с ИИ по каждому разработчику, команде и проекту. Видно, кто и где вайбкодит.'),
                ('Промпт-коллектор', 'Агент на машине разработчика собирает сессии, ходы и токены по каждому MR. Без прокси — исходный код никуда не уходит.'),
                ('ИИ-эффективность', 'Сколько часов задача заняла бы вручную и сколько заняла с ИИ — по каждому MR.'),
                ('Стоимость результата', 'Токены на MR и на час результата с нормами: где ИИ окупается, а где сжигает бюджет.'),
                ('Качество ИИ-кода', 'Та же мерка, что и для человека: результирующий код, переделки, баги и техдолг.'),
                ('До и после внедрения', 'Базовая линия строится по истории вашего Git — не нужно ждать полгода, чтобы сравнить.')], 'ai'),
            compare('ПОЧЕМУ НЕ ХВАТАЕТ ОБЫЧНЫХ МЕТРИК', 'Доля принятых подсказок и число коммитов ничего не говорят о пользе', 'Как меряют обычно', [
                'процент принятых подсказок ИИ — принятый код часто переписывают', 'число коммитов и PR — растёт и от мусора', 'опросы «стало ли быстрее» — ошибаются на десятки процентов', 'отчёты вендора об использовании лицензий'],
                'Как меряет UpCore', ['код, который остался в продукте', 'часы результата против часов работы — по каждому MR', 'разработчики, команды и инструменты — на одной шкале', 'рубли: стоимость токенов на час результата'], None, 'ai'),
            results('ai'),
            faq([
                ('С какими ИИ-инструментами работает?', 'Авто-детект смотрит на сам код — он не зависит от инструмента. Промпт-коллектор собирает сессии ИИ-агента на машине разработчика.'),
                ('Это не слежка за промптами?', 'Промпты разбираются для ревью и обучения: где теряется контекст и как получать результат быстрее. Доступ — по ролям, в on-premise всё остаётся у вас.'),
                ('Нужно ждать, пока накопится статистика?', 'Нет. История за 3–6 месяцев уже лежит в вашем Git — UpCore сразу построит картину «до» и «после» внедрения ИИ.'),
                ('Чем это отличается от отчёта вендора ИИ?', 'Вендор показывает использование своего продукта. UpCore показывает результат в коде — одинаково для любых инструментов и людей.')], acc_key='ai'),
            security(False),
            cta('Посчитайте реальный эффект ИИ в своей команде', 'Подключите репозиторий — сравним время «с ИИ» и «вручную» по истории вашего кода.'),
            footer()]
    elif key == 'projects':
        body += [
            pains('ПРОБЛЕМА', 'Бюджеты ИТ-проектов утекают незаметно', [
                ('+45%', 'к бюджету в среднем у крупных ИТ-проектов — и на 56% меньше ценности, чем планировали', 'McKinsey и Оксфорд, 5400+ проектов'),
                ('1500 ч', 'в акте приходится принимать на веру: у заказчика нет инструмента, чтобы проверить подрядчика', 'из практики Dex'),
                ('«почти готово»', 'Часы растут, а функциональность не меняется. При оплате за часы у подрядчика нет стимула ускоряться', None),
                ('−75%', 'работали ключевые разработчики вендора относительно среднего в кейсе банка — проект оказался на 76% менее продуктивным', 'BlueOptima, кейс')], 'projects'),
            scenarios(),
            modules('ЧТО В ОТЧЁТЕ', 'Всё о проекте — в часах, рублях и рисках', [
                ('Объективная стоимость', 'Трудоёмкость кода в часах и рублях — за месяц, квартал или весь проект.'),
                ('Эффективность команды', 'Часы результата против списанных и рабочих часов — по людям и подрядчикам.'),
                ('Прогноз сроков', 'Когда команда закроет объём и насколько велик риск выйти за дедлайн.'),
                ('Техдолг', 'Какая доля дефектов, найденных ревью, ушла в main — по категориям качества ISO/IEC 25010.'),
                ('Сложность и легаси', 'Размер, сложность, доля легаси и прирост проекта — чтобы сравнивать проекты честно.'),
                ('Тех-карта и мэтч команды', 'Какие технологии есть в коде и насколько им соответствует команда; вакансия и подбор под пробелы.')], 'projects'),
            results('projects'),
            projects_example(),
            roles('ДЛЯ КОГО', 'Прозрачность, выгодная обеим сторонам', [
                ('Заказчикам аутсорса', 'Платите за результат, а не за часы: каждый акт сверяется с кодом.'),
                ('Финансам и закупкам', 'Объективная стоимость для переговоров о смете и продлении контракта.'),
                ('PMO и CTO', 'Портфель проектов, риски сроков и потери — на одном экране.'),
                ('ИТ-подрядчикам', 'Отдавайте клиенту отчёт UpCore вместо таблицы часов — так делает Dex. Прозрачность становится преимуществом.')], 'projects'),
            steps('КАК ПРОХОДИТ АУДИТ', 'Три шага — и бюджет проекта посчитан', [
                ('01 · ДОСТУП', 'Read-only или локальный агент', 'Доступ к репозиторию только на чтение — или анализ агентом в вашем контуре. Код остаётся у вас.'),
                ('02 · АНАЛИЗ', 'Вся история проекта', 'Оцениваем каждый MR и коммит, сверяем с ворклогами Jira и актами.'),
                ('03 · ОТЧЁТ', 'Результат за 2 дня', 'Бюджет проекта по коду, эффективность команды, техдолг и риски — с расчётом до строчки.')], 'projects'),
            faq([
                ('А если подрядчик не даст доступ к коду?', 'Как правило, код по договору принадлежит заказчику. Анализ можно провести локальным агентом в вашем контуре — исходники никуда не передаются.'),
                ('Подходит для 1С и легаси?', 'Да: C#, Java, Go, Python, Kotlin, PHP, JS/TS, C++ и 1С. Доля легаси и сложность учитываются в оценке.'),
                ('Это заменит приёмку работ?', 'Нет — даст приёмке объективную основу: сколько трудоёмкости в коде на самом деле, а сколько в акте.'),
                ('Можно оценить проект при покупке компании?', 'Да. Разовый аудит покажет, сколько стоил код, сколько в нём техдолга и насколько команда соответствует технологиям.')], acc_key='projects'),
            security(False),
            cta('Проверьте, сколько на самом деле стоит ваш проект', 'Закажите аудит — объективный бюджет проекта по коду за 2 дня.', ('Заказать аудит', MAIL), ('Регистрация', REG)),
            footer()]
    elif key == 'mentor':
        body += [
            pains('ПРОБЛЕМА', 'Менторство не масштабируется. А с ИИ стало ещё сложнее', [
                ('5–10%', 'кода успевает глубоко проверить живой тимлид — на обучение по остальному просто нет времени', 'данные UpCore'),
                ('81%', 'руководителей: время, сэкономленное ИИ на написании кода, теперь уходит на ревью ИИ-кода', 'Harness, 2026'),
                ('50% / 67%', 'Разработчики, учившиеся с ИИ, хуже усвоили материал — сильнее всего просела отладка', 'Anthropic, 2026'),
                ('3–9 мес.', 'уходит у нового разработчика на выход на полную продуктивность', 'Swimm; DX')], 'mentor'),
            modules('ЧТО ДЕЛАЕТ НАСТАВНИК', 'Ревью, разбор ошибок и план роста — каждый день, автоматически', [
                ('ИИ-ревью кода', 'Каждый MR: уязвимости, архитектура, логика, читаемость, производительность. Дефекты по тяжести и блокам качества.'),
                ('Системные ошибки → план развития', 'Mentor находит повторяющиеся ошибки конкретного человека и собирает из них персональный трек обучения.'),
                ('Ревью промптов', 'Где разработчик теряет контекст и как выжимать из ИИ максимум без потери качества.'),
                ('Ревью постановок задач', 'Оценка качества аналитики — чтобы не сливать бюджет ещё до старта разработки.'),
                ('Топ-3 технологии для роста', 'По тех-мэтчу с проектом и реальному уровню разработчика — что изучать в первую очередь.'),
                ('Приоритеты для тимлида', 'Подсвечивает MR, где нужен человек: затронуто ядро, найдены уязвимости, время сильно выше сложности.')], 'mentor'),
            mentor_chat(),
            results('mentor'),
            roles('ДЛЯ КОГО', 'Что получает каждый в команде', [
                ('Разработчик', 'Конкретные рекомендации по своему коду вместо общих советов. Прогресс по звезде компетенций и понятный путь к следующему грейду.'),
                ('Тимлид', '15 минут на критичные MR вместо часов ревью всего подряд. Менторит всю команду, а не троих.'),
                ('L&D и HR', 'План развития строится сам — по реальным ошибкам, а не по впечатлениям раз в полгода.'),
                ('CTO', 'Рост грейдов и качества кода в цифрах. Быстрее онбординг, меньше багов в main.')], 'mentor'),
            faq([
                ('Чем Mentor отличается от ИИ-ревьюера кода?', 'Ревьюер смотрит один MR. Mentor видит всю историю разработчика — задачи, промпты, код и оценки — и превращает системные ошибки в план роста.'),
                ('Mentor заменит тимлида?', 'Нет. Он снимает рутину — ревью всего подряд и разбор типовых ошибок, — чтобы тимлид тратил время на архитектуру и людей.'),
                ('Это не очередной контроль?', 'Рекомендации видит сам разработчик, и они про рост, а не про наказание. Цифровой тимлид из контролёра становится наставником.'),
                ('Как Mentor учит работать с ИИ?', 'Разбирает промпты и решения: где не хватило контекста, где ИИ увёл в сторону. Цель — чтобы разработчик рос вместе с ИИ, а не вместо себя отдавал ему работу.')], acc_key='mentor'),
            security(False),
            cta('Дайте каждому разработчику своего наставника', 'Подключите репозиторий — первые рекомендации по истории MR вашей команды.'),
            footer()]
    return page('UpCore %s — страница A' % names[key], '\n'.join(body), 5400, name='%s-A' % names[key])

def build(out, mode):
    global MODE
    MODE = mode
    os.makedirs(out, exist_ok=True)
    files = {}
    for v in 'ABC':
        files['Home-%s' % v] = home(v)
    # раунд 19: блоки «Сердце» и «Почему это важно» зафиксированы на Главной A, отдельные артборды вариантов сняты
    # раунд 22: блок «Платформа» (вариант 3) зафиксирован на Главной A, артборды Platform-1..4 сняты
    # раунд 24: «Принцип + точность» (вариант 1) зафиксирован на Главной A, Trust-1..3 сняты
    # раунд 28: «Результаты для бизнеса» (расчёт 2) зафиксирован на Главной A, артборды Results-1..4 сняты
    # (функции core_board / pains_board оставлены, чтобы можно было снова вывести варианты)
    for k, n in (('grade', 'Grade'), ('ai', 'AI'), ('projects', 'Projects'), ('mentor', 'Mentor')):
        for v in 'ABC':
            files['%s-%s' % (n, v)] = product(k, v)
    ext = '.dc.html' if mode == 'dc' else '.html'
    for name, txt in files.items():
        with open(os.path.join(out, name + ext), 'w', encoding='utf-8') as f:
            f.write(txt)
    return list(files)

if __name__ == '__main__':
    hp = os.path.join(os.path.dirname(__file__), 'heights.json')
    if os.path.exists(hp):
        import json; HEIGHTS.update(json.load(open(hp)))
    names = build(sys.argv[1], 'dc')
    if len(sys.argv) > 2:
        build(sys.argv[2], 'preview')
    print(len(names), 'файлов:', ', '.join(names))
