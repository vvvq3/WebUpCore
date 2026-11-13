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
.uc-rl{}
.g2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}
.uc-row{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:40px;align-items:start}
.g3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.g4{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
.g4m2{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
@media (max-width:1100px){.g3,.g4{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:720px){.uc-rl{display:none}.uc-sc{grid-template-columns:minmax(0,1fr) minmax(0,1fr)!important}.uc-sc>span:first-child{grid-column:1/-1}.uc-sc>span:first-child:empty{display:none}.uc-ml{display:block!important;font-family:'JetBrains Mono',monospace;font-size:12px;font-weight:400;color:rgba(255,255,255,0.55);margin-bottom:2px;white-space:normal}th .uc-ml{display:inline!important;font-family:inherit;font-size:inherit;color:inherit}.uc-res thead{display:none}.uc-res tr{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr)}.uc-res th[scope=row]{grid-column:1/-1}.uc-res td,.uc-res th{border-top:0!important;padding:4px 8px 4px 0!important}.uc-res tr{border-top:1px solid rgba(255,255,255,0.1);padding:12px 0}.uc-row{grid-template-columns:minmax(0,1fr);gap:16px}.g2,.g3,.g4{grid-template-columns:minmax(0,1fr)}.g4m2{grid-template-columns:repeat(2,minmax(0,1fr))}.uc-cmp thead{display:none}.uc-cmp tr{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr)}.uc-cmp th[scope=row]{grid-column:1/-1;padding:14px 0 6px!important}.uc-cmp td{padding:6px 10px 14px!important;border-top:0!important}}
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
                  ('+14%', 'рост эффективности разработки за 3 месяца'), ('≈780 тыс. ₽', 'экономии в год на каждого разработчика')], 'данные и расчёт UpCore'),
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
    subs = [(d['month'], 'в месяц на команду из 100 разработчиков'), ('1 день', 'до первых результатов'), ('0 ₽', 'за пилот: платите после того, как подтвердите точность')]
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

# ---------------------------------------------------------------- раунд 33: нижний блок главной «SaaS и безопасность» — 2 варианта
def ico(kind, col='#63D5FF', size=30):
    paths = {
        'plug': '<path d="M9 7V3M15 7V3M7 7h10v4a5 5 0 0 1-10 0V7zM12 16v5"/>',
        'code': '<path d="M8 8l-4 4 4 4M16 8l4 4-4 4M14 5l-4 14"/>',
        'link': '<path d="M10 14a4 4 0 0 0 5.66 0l3-3a4 4 0 0 0-5.66-5.66l-1 1M14 10a4 4 0 0 0-5.66 0l-3 3a4 4 0 0 0 5.66 5.66l1-1"/>',
        'lock': '<rect x="4.5" y="10.5" width="15" height="10" rx="2.5"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3M9 15.5h.01M12 15.5h.01M15 15.5h.01"/>',
        'eye': '<path d="M2.5 12s3.5-6.5 9.5-6.5 9.5 6.5 9.5 6.5-3.5 6.5-9.5 6.5S2.5 12 2.5 12z"/><circle cx="12" cy="12" r="3"/>',
        'shield': '<path d="M12 3l7.5 3v5.5c0 4.6-3.2 8.3-7.5 9.5-4.3-1.2-7.5-4.9-7.5-9.5V6L12 3z"/><path d="M9 12l2 2 4-4"/>',
        'target': '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1"/>',
        'wallet': '<rect x="3.5" y="6.5" width="17" height="12" rx="2.5"/><path d="M3.5 10h17M16 14.5h1.5"/>',
    }
    return ('<svg aria-hidden="true" viewBox="0 0 24 24" width="%d" height="%d" fill="none" stroke="%s" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="flex: 0 0 auto; display: block;">%s</svg>' % (size, size, col, paths[kind]))

SAAS6 = [
    ('plug', 'Подключение за минуты', 'Вход через GitHub или GitLab, подключили репозиторий — первые результаты через 1 день. Код за год анализируется за несколько минут.'),
    ('code', 'Нужен только код', 'Без отчётов, анкет и тайм-трекеров. Любой язык: C#, Java, Go, Python, Kotlin, PHP, JS/TS, C++ и 1С.'),
    ('link', 'Встраивается в ваши процессы', 'GitLab, GitHub и Jira, корпоративные трекеры, дашборды и отчёты. Подключение по протоколу MCP.'),
    ('lock', 'On-premise без интернета', 'Полностью в вашем контуре безопасности, без доступа к интернету. Нужен только read-only доступ к Git, GPU не нужны.'),
    ('eye', 'Любой вывод можно проверить', '«Глаз» раскрывает расчёт до строчки кода и подсвечивает значимые изменения — это ускоряет и ручное код-ревью.'),
    ('wallet', 'Платите за подтверждённый результат', 'Бесплатный пилот на 2–3 ваших проектах. Оплата — только после того, как вы подтвердите точность на своих данных.'),
]

def saas_variant(n):
    if n == 1:  # 6 карточек 3×2 с иконками
        cards = ''.join(card('<div style="display: flex; align-items: center; gap: 14px;">' + ico(k) + '<div style="font-size: 20px; font-weight: 700; line-height: 1.25; color: #FFFFFF;">' + e(t) + '</div></div>'
                             '<p style="margin: 0; color: rgba(255,255,255,0.74); font-size: 16px; line-height: 1.55;">' + e(p) + '</p>') for k, t, p in SAAS6)
        return section(sec_head('SAAS И БЕЗОПАСНОСТЬ', 'Подключение за минуты. Код остаётся у вас.') + '<div class="g3">' + cards + '</div>', 'saas')
    # n == 2: слева — путь подключения за 3 шага, справа — 4 гарантии
    steps = [('01', 'Вход через GitHub или GitLab', 'или установка on-premise в вашем контуре'), ('02', 'Подключаете репозиторий', 'read-only доступ, нужен только код'), ('03', 'Сразу смотрите результат', 'проанализируем последние полгода работы за 1 час')]
    st = ''.join('<div style="display: grid; grid-template-columns: 44px minmax(0, 1fr); gap: 14px; align-items: start; padding: 16px 0; border-top: 1px solid rgba(255,255,255,0.08);">'
                 '<div style="width: 44px; height: 44px; border-radius: 14px; background: ' + ('#63D5FF' if i == 2 else 'rgba(99,213,255,0.12)') + '; color: ' + ('#0D0C15' if i == 2 else '#63D5FF') + '; display: flex; align-items: center; justify-content: center; ' + MONO + ' font-size: 14px; font-weight: 600;">' + a + '</div>'
                 '<div style="min-width: 0;"><div style="font-size: 19px; font-weight: 700; line-height: 1.3;">' + e(b) + '</div><div style="font-size: 15px; color: rgba(255,255,255,0.66); margin-top: 2px;">' + e(c) + '</div></div></div>' for i, (a, b, c) in enumerate(steps))
    stacks = ''.join('<span style="font-size: 13px; padding: 6px 10px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.14); color: rgba(255,255,255,0.82);">' + x + '</span>' for x in ['C#', 'Java', 'Go', 'Python', 'Kotlin', 'PHP', 'JS/TS', 'C++', '1С'])
    integ = ''.join('<span style="font-size: 13px; padding: 6px 10px; border-radius: 10px; background: rgba(99,213,255,0.1); border: 1px solid rgba(99,213,255,0.3); color: #FFFFFF;">' + x + '</span>' for x in ['GitLab', 'GitHub', 'Jira', 'трекеры и дашборды', 'MCP'])
    left = ('<div style="flex: 1.1 1 440px; min-width: 0; border-radius: 32px; background: #12111C; border: 1px solid rgba(99,213,255,0.35); padding: clamp(24px, 3.4vw, 40px); display: flex; flex-direction: column; gap: 18px;">'
            '<div style="' + MONO + ' font-size: 12px; color: #63D5FF;">ПОДКЛЮЧЕНИЕ</div><div style="font-size: clamp(24px, 2.2vw, 32px); font-weight: 800; line-height: 1.15;">Нужен только код — без отчётов, анкет и тайм-трекеров</div>'
            '<div>' + st + '</div>'
            '<div><div style="' + MONO + ' font-size: 12px; color: rgba(255,255,255,0.55); margin-bottom: 8px;">ЛЮБОЙ СТЕК</div><div style="display: flex; flex-wrap: wrap; gap: 6px;">' + stacks + '</div></div></div>')
    g = [('lock', 'On-premise без интернета', 'Полностью в вашем контуре безопасности. Read-only доступ к Git, GPU не нужны.'),
         ('link', 'Простая интеграция', 'Система легко интегрируется с уже существующими корпоративными трекерами, дашбордами, отчётами и MCP.'),
         ('shield', 'Без «токсичного контроля»', 'Это обычное код-ревью, только автоматическое: около секунды на MR. Накрутки и шум отсекаются.'),
         ('wallet', 'Оплата после пилота', 'Бесплатный пилот на 2–3 проектах. Платите, когда подтвердите точность на своих данных.')]
    right = ('<div class="g2" style="flex: 1 1 460px; min-width: 0;">' + ''.join(card('<div>' + ico(k, size=28) + '</div><div style="font-size: 19px; font-weight: 700; line-height: 1.25;">' + e(t) + '</div><p style="margin: 0; color: rgba(255,255,255,0.74); font-size: 15px; line-height: 1.55;">' + e(p) + '</p>', pad='24px', gap=10) for k, t, p in g) + '</div>')
    return section(sec_head('SAAS И БЕЗОПАСНОСТЬ', 'Подключение за минуты. Код остаётся у вас.') + '<div style="display: flex; flex-wrap: wrap; gap: 16px; align-items: stretch;">' + left + right + '</div>', 'saas')

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

# ---------------------------------------------------------------- раунд 29: Grade — пример по демо «Уровень» и 4 варианта методики
LEVEL = [  # демо, страница «Уровень»: Лукьянов Александр, Backend C#, октябрь 2026 (май → окт.)
    ('Эффективность', 10.0, 8.4, 'часы результата по коду против рабочего времени — главный фактор'),
    ('Количество и сложность задач', 6.8, 6.1, 'доля сложных, средних и простых задач'),
    ('Качество кода', 7.5, 7.2, 'оценка ИИ-ревью до и после исправлений'),
    ('Код-ревью', 7.7, 8.1, 'замечания, которые получил и оставил сам'),
    ('Архитектурная сложность', 3.1, 3.7, 'сколько кода в ядре, middle и на периферии (AST)'),
    ('Сложность кода', 5.2, 5.1, 'цикломатическая, логическая, когнитивная'),
    ('Технологии', 6.4, 7.4, 'сложность технологий по карте компетенций стека'),
    ('Тех-метч', 9.5, 9.5, 'соответствие технологиям проекта и контрибуция'),
    ('Результирующий код', 9.1, 8.7, 'какая доля кода дошла до релиза'),
    ('Уровень багов', 5.1, 6.4, 'переделанные MR и исправления'),
]
GREEN, AMBER = '#7FDB7A', '#F2C14E'

def lvl_col(v):
    return GREEN if v >= 7.5 else (AMBER if v >= 5 else RED_T)

def radar_svg(vals, size=360, rings=(4.5, 7.5), dots=True):
    import math
    c, R, n = size / 2, size / 2 - 14, len(vals)
    pt = lambda i, v: (c + R * v / 10 * math.sin(2 * math.pi * i / n), c - R * v / 10 * math.cos(2 * math.pi * i / n))
    poly = lambda v_list: ' '.join('%.1f,%.1f' % pt(i, v) for i, v in enumerate(v_list))
    out = ['<svg viewBox="0 0 %d %d" role="img" aria-label="Звезда грейда: 10 факторов" style="width: 100%%; max-width: %dpx; height: auto; display: block; margin: 0 auto;">' % (size, size, size)]
    for k in (2, 4, 6, 8, 10):
        out.append('<polygon points="%s" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="1"></polygon>' % poly([k] * n))
    for i in range(n):
        x, y = pt(i, 10)
        out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="rgba(255,255,255,0.08)"></line>' % (c, c, x, y))
    for r_, dash in zip(rings, ('3 4', '7 5')):
        out.append('<polygon points="%s" fill="none" stroke="rgba(255,255,255,0.45)" stroke-width="1.4" stroke-dasharray="%s"></polygon>' % (poly([r_] * n), dash))
    out.append('<polygon points="%s" fill="rgba(99,213,255,0.18)" stroke="#63D5FF" stroke-width="2.5" stroke-linejoin="round"></polygon>' % poly(vals))
    if dots:
        for i, v in enumerate(vals):
            x, y = pt(i, v)
            out.append('<circle cx="%.1f" cy="%.1f" r="5.5" fill="%s" stroke="#12111C" stroke-width="2"></circle>' % (x, y, lvl_col(v)))
    out.append('</svg>')
    return ''.join(out)

def fmt1(v):
    return ('%.1f' % v).replace('.', ',')

def arrow(now, was):
    if now - was >= 0.5:
        return '<span style="color: %s;">↑</span>' % GREEN
    if was - now >= 0.5:
        return '<span style="color: %s;">↓</span>' % RED_T
    return '<span style="color: rgba(255,255,255,0.5);">→</span>'

def grade_example_v2():
    """Пример без «красной зоны»: профиль разработчика из демо — звезда, 10 факторов с динамикой, рейтинги."""
    rows = ''.join('<div style="display: grid; grid-template-columns: minmax(0, 1fr) auto auto; gap: 12px; align-items: baseline; padding: 9px 0; border-top: 1px solid rgba(255,255,255,0.07);">'
                   '<span style="font-size: 15px; color: rgba(255,255,255,0.84);">' + e(n) + '</span>'
                   '<span style="font-size: 13px; color: rgba(255,255,255,0.5); white-space: nowrap; font-variant-numeric: tabular-nums;">' + fmt1(w) + ' → </span>'
                   '<span style="font-size: 17px; font-weight: 800; white-space: nowrap; color: ' + lvl_col(v) + '; font-variant-numeric: tabular-nums;">' + fmt1(v) + ' ' + arrow(v, w) + '</span></div>' for n, v, w, _ in LEVEL)
    def kv(k, v, sub=''):
        return ('<div style="min-width: 0;"><div style="font-size: 13px; color: rgba(255,255,255,0.6);">' + e(k) + '</div><div style="font-size: clamp(22px, 2vw, 28px); font-weight: 800; white-space: nowrap;">' + v + '</div>'
                + ('<div style="font-size: 13px; color: rgba(255,255,255,0.55);">' + e(sub) + '</div>' if sub else '') + '</div>')
    head = ('<div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 16px 32px; align-items: flex-end; padding-bottom: 24px; border-bottom: 1px solid rgba(255,255,255,0.08);">'
            '<div style="min-width: 0;"><div style="' + MONO + ' font-size: 12px; color: rgba(255,255,255,0.55);">ДЕМО UPCORE · МЕНЮ «УРОВЕНЬ» · ОКТЯБРЬ 2026</div>'
            '<div style="font-size: clamp(22px, 2vw, 28px); font-weight: 800; margin-top: 8px;">Лукьянов Александр</div><div style="font-size: 15px; color: rgba(255,255,255,0.66);">Backend, C# · проект UpCore Backend</div></div>'
            '<div style="display: flex; flex-wrap: wrap; gap: 20px 36px;">'
            + kv('Грейд', '<span style="color: #7FDB7A;">Senior</span> 8,5<span style="font-size: 16px; color: rgba(255,255,255,0.5);"> / 10</span>', 'за 3 месяца')
            + kv('Рост за полгода', '<span style="color: ' + AMBER + ';">Middle+</span> → <span style="color: #7FDB7A;">Senior</span>', '7,2 → 8,5')
            + kv('Рейтинг', '2 <span style="font-size: 16px; color: rgba(255,255,255,0.5);">из 14</span>', 'в компании · 4 из 13 в стеке') + '</div></div>')
    legend = ('<div style="display: flex; flex-wrap: wrap; gap: 8px 18px; justify-content: center; font-size: 13px; color: rgba(255,255,255,0.62); margin-top: 12px;">'
              '<span><span style="color: #63D5FF;">■</span> оценки за период</span><span>┅ уровень Middle</span><span>╍ уровень Senior</span></div>')
    insights = ('<div class="g2" style="margin-top: 24px;">'
                + card('<div style="' + MONO + ' font-size: 12px; color: #7FDB7A;">СИЛЬНЫЕ СТОРОНЫ</div><p style="margin: 0; font-size: 15px; line-height: 1.55; color: rgba(255,255,255,0.84);">Эффективность 10 из 10: 889 часов результата при 436 рабочих за период, 123 MR. 91% кода дошло до релиза, тех-метч с проектом — 95%.</p>', pad='22px', bg='rgba(83,192,77,0.06)', border='rgba(83,192,77,0.3)', gap=8)
                + card('<div style="' + MONO + ' font-size: 12px; color: ' + AMBER + ';">ЗОНА РОСТА</div><p style="margin: 0; font-size: 15px; line-height: 1.55; color: rgba(255,255,255,0.84);">Архитектурная сложность 3,1: 80% времени — периферия, в ядре системы только 7%. Следующий шаг — задачи в ядре; это видно сразу, без ревью-сессий.</p>', pad='22px', bg='rgba(242,193,78,0.06)', border='rgba(242,193,78,0.3)', gap=8)
                + '</div>')
    body = ('<div style="border-radius: 32px; background: #12111C; border: 1px solid rgba(99,213,255,0.35); padding: clamp(24px, 3.4vw, 44px);">' + head +
            '<div style="display: flex; flex-wrap: wrap; gap: 32px 48px; align-items: center; margin-top: 28px;">'
            '<div style="flex: 1 1 320px; min-width: 0; max-width: 420px; margin: 0 auto;">' + radar_svg([v for _, v, _, _ in LEVEL]) + legend + '</div>'
            '<div style="flex: 1.3 1 420px; min-width: 0;"><div style="display: grid; grid-template-columns: minmax(0, 1fr) auto auto; gap: 12px; padding-bottom: 8px; ' + MONO + ' font-size: 12px; color: rgba(255,255,255,0.5);"><span>10 ФАКТОРОВ ГРЕЙДА</span><span>МАЙ</span><span>ОКТЯБРЬ</span></div>' + rows + '</div></div>'
            + insights + '</div>')
    return section(sec_head('ПРИМЕР', 'Не просто «Senior», а все факторы, из которых он сложился', 'Реальный профиль из демо UpCore: звезда грейда, динамика по каждому фактору и место в рейтинге — без единого отчёта от разработчика.', 'grade') + body)

METHOD_FACTORS = [(n, d) for n, _, _, d in LEVEL]

def method_head(h2, lead):
    return sec_head('МЕТОДИКА', h2, lead, 'grade')

def method_rhythm():
    """Полоса «каждый месяц / каждые 3 месяца» — общая для вариантов."""
    m = ['Эффективность и детальный отчёт за месяц', 'Рейтинг по компании, стеку и проекту: топ-20% и 20% отстающих', 'Сравнение со средним по команде, стеку и компании', 'Динамика эффективности, грейда и рейтинга на графиках']
    li = lambda xs: ''.join('<li style="margin: 0 0 6px;">' + e(x) + '</li>' for x in xs)
    return ('<div class="g2" style="margin-top: 16px;">'
            + card('<div style="' + MONO + ' font-size: 12px; color: #63D5FF;">КАЖДЫЙ МЕСЯЦ</div><ul style="margin: 0; padding-left: 20px; color: rgba(255,255,255,0.84); font-size: 15px; line-height: 1.5;">' + li(m) + '</ul>', pad='24px', gap=10)
            + card('<div style="' + MONO + ' font-size: 12px; color: #63D5FF;">КАЖДЫЕ 3 МЕСЯЦА</div><div style="font-size: 22px; font-weight: 800;">Грейд</div><p style="margin: 0; color: rgba(255,255,255,0.8); font-size: 15px; line-height: 1.55;">Грейд считаем по трём месяцам работы: так данных хватает для объективной оценки, а случайный месяц не перекашивает результат.</p>', pad='24px', gap=10)
            + '</div>')

def method_foot():
    return ('<div style="margin-top: 16px; display: flex; flex-wrap: wrap; gap: 12px 32px; align-items: center; justify-content: space-between; border-radius: 20px; border: 1px solid rgba(99,213,255,0.3); background: rgba(99,213,255,0.06); padding: 18px 24px; font-size: 16px; line-height: 1.5; color: rgba(255,255,255,0.86);">'
            '<span>Всё — автоматически. <b style="color: #FFFFFF;">Нужен только код.</b></span><span style="color: rgba(255,255,255,0.7);">Гибкая интеграция с вашими системами и по протоколу MCP.</span></div>')

def method_variant(n):
    if n == 1:  # звезда из 10 факторов + описание каждого + ритм
        items = ''.join('<div style="display: flex; gap: 14px; align-items: baseline; padding: 11px 0; border-top: 1px solid rgba(255,255,255,0.07);">'
                        '<span style="' + MONO + ' font-size: 13px; color: ' + ('#63D5FF' if i == 0 else 'rgba(255,255,255,0.45)') + '; flex: 0 0 24px;">' + '%02d' % (i + 1) + '</span>'
                        '<span style="min-width: 0;"><b style="font-size: 16px; color: ' + ('#63D5FF' if i == 0 else '#FFFFFF') + ';">' + e(nm) + '</b><span style="font-size: 15px; color: rgba(255,255,255,0.66);"> — ' + e(d) + '</span></span></div>' for i, (nm, d) in enumerate(METHOD_FACTORS))
        star = ('<div style="flex: 1 1 300px; min-width: 0; max-width: 400px; margin: 0 auto; text-align: center;">' + radar_svg([10, 7, 7.5, 7.5, 6, 6.5, 7, 8.5, 8.5, 7], dots=False) +
                '<div style="font-size: clamp(40px, 4vw, 56px); font-weight: 800; letter-spacing: -0.03em; margin-top: 8px;"><span style="color: ' + AMBER + ';">Middle+</span> 7,8<span style="font-size: 20px; color: rgba(255,255,255,0.5);"> / 10</span></div>'
                '<div style="font-size: 15px; color: rgba(255,255,255,0.66);">итог — не мнение, а сумма факторов</div></div>')
        body = ('<div style="display: flex; flex-wrap: wrap; gap: 32px 56px; align-items: center; border-radius: 32px; background: #12111C; border: 1px solid rgba(255,255,255,0.08); padding: clamp(24px, 3.4vw, 44px);">'
                + star + '<div style="flex: 1.4 1 460px; min-width: 0;">' + items + '</div></div>')
        return section(method_head('Грейд — это сложная математика по 10+ факторам, а не мнение', 'Главный фактор — объективная эффективность кода в часах. Остальные девять уточняют, на каком уровне и с каким качеством человек работает.') + body + method_rhythm() + method_foot(), 'method')
    if n == 2:  # три глубоких фактора
        chips_html = ''.join('<span style="display: inline-flex; align-items: center; min-height: 32px; padding: 4px 12px; border-radius: 16px; font-size: 14px; background: ' + ('rgba(99,213,255,0.16)' if i == 0 else 'rgba(255,255,255,0.05)') + '; border: 1px solid ' + ('#63D5FF' if i == 0 else 'rgba(255,255,255,0.12)') + '; color: #FFFFFF;">' + e(nm) + '</span>' for i, (nm, _) in enumerate(METHOD_FACTORS))
        ring = ('<svg viewBox="0 0 220 220" aria-hidden="true" style="width: 100%; max-width: 200px; height: auto; display: block; margin: 0 auto;">'
                '<circle cx="110" cy="110" r="100" fill="rgba(255,255,255,0.04)" stroke="rgba(255,255,255,0.15)"></circle>'
                '<circle cx="110" cy="110" r="64" fill="rgba(99,213,255,0.10)" stroke="rgba(99,213,255,0.4)"></circle>'
                '<circle cx="110" cy="110" r="28" fill="#63D5FF"></circle></svg>'
                '<div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 6px 14px; font-size: 13px; color: rgba(255,255,255,0.66);"><span><span style="color: #63D5FF;">●</span> ядро</span><span><span style="color: rgba(99,213,255,0.6);">●</span> middle</span><span><span style="color: rgba(255,255,255,0.35);">●</span> периферия</span></div>')
        tech = ('<div style="display: flex; flex-direction: column; gap: 8px;">'
                + ''.join('<div style="display: flex; justify-content: space-between; gap: 12px; font-size: 14px; padding: 8px 12px; border-radius: 12px; background: rgba(255,255,255,0.04);"><span>' + e(a) + '</span><b style="color: ' + c + '; white-space: nowrap;">' + e(b) + '</b></div>'
                          for a, b, c in [('Senior-технологии', '2 · 1,8 ч', GREEN), ('Middle-технологии', '16 · 191,4 ч', '#FFFFFF'), ('Ввёл в проект новых', '1', '#63D5FF'), ('Легаси / новое для себя', 'учитывается', 'rgba(255,255,255,0.7)')]) + '</div>')
        churn = ('<div><div style="display: flex; height: 18px; border-radius: 9px; overflow: hidden; gap: 3px;"><div style="flex: 150 1 0; background: #63D5FF;"></div><div style="flex: 150 1 0; background: rgba(232,101,101,0.5);"></div></div>'
                 '<div style="display: flex; justify-content: space-between; font-size: 13px; color: rgba(255,255,255,0.66); margin-top: 8px;"><span><b style="color: #63D5FF;">150 строк</b> дошли до релиза</span><span><b style="color: ' + RED_T + ';">150</b> удалены и переписаны</span></div></div>')
        def deep(num, title, viz, text):
            return ('<article style="min-width: 0; border-radius: 28px; background: #1A1925; border: 1px solid rgba(255,255,255,0.08); padding: clamp(22px, 2.6vw, 32px); display: flex; flex-direction: column; gap: 16px;">'
                    '<div style="' + MONO + ' font-size: 12px; color: #63D5FF;">' + num + '</div><div style="font-size: 22px; font-weight: 800; line-height: 1.2;">' + e(title) + '</div>' + viz +
                    '<p style="margin: 0; color: rgba(255,255,255,0.78); font-size: 15px; line-height: 1.55;">' + e(text) + '</p></article>')
        cards = (deep('ФАКТОР · АРХИТЕКТУРА', 'Где написан код: в ядре или на периферии', ring, 'Строим AST-дерево всего проекта и видим, где работает разработчик. 20 строк в ядре системы бывают сложнее и ценнее 200 строк на периферии, которые меняют цвет кнопок.')
                 + deep('ФАКТОР · ТЕХНОЛОГИИ', 'Какие технологии и в каком объёме', tech, 'Разбираем каждую строчку и считаем часы по каждой технологии. Карта компетенций стека задаёт её сложность и грейд. Учитываем легаси, новое для человека и новые технологии, которые он ввёл в проект.')
                 + deep('ФАКТОР · РЕЗУЛЬТИРУЮЩИЙ КОД', 'Сколько кода дошло до релиза', churn, 'Написал 300 строк, а назавтра половину удалили и переписали — значит, до релиза дошло 50% работы. Фактор особенно важен с ИИ и отсекает любые накрутки.'))
        intro = ('<div style="border-radius: 28px; background: #12111C; border: 1px solid rgba(255,255,255,0.08); padding: clamp(22px, 2.6vw, 32px); margin-bottom: 16px; display: flex; flex-direction: column; gap: 14px;">'
                 '<div style="font-size: 17px; line-height: 1.55; color: rgba(255,255,255,0.86);">Грейд складывается из 10+ факторов. <b style="color: #63D5FF;">Главный — эффективность кода в часах.</b> Вот три, которые обычно не видит ни один руководитель:</div>'
                 '<div style="display: flex; flex-wrap: wrap; gap: 8px;">' + chips_html + '</div></div>')
        return section(method_head('Что стоит за грейдом: три фактора, которые не видны глазом', 'Мы разбираем каждую строчку кода — и знаем то, что не скажет ни резюме, ни самооценка.') + intro + '<div class="g3">' + cards + '</div>' + method_rhythm() + method_foot(), 'method')
    if n == 3:  # прозрачность: от цифры до строчки кода
        steps = [('01', 'Грейд', '<span style="color: ' + AMBER + ';">Middle+</span> 7,8', 'одна цифра за 3 месяца'),
                 ('02', 'Меню «Уровень»', '10 факторов', 'звезда грейда, динамика и дашборд'),
                 ('03', 'Меню «Отчёты»', 'Архитектура 3,1', 'ядро 59 ч · middle 116 ч · периферия 713 ч'),
                 ('04', '«Глаз»', 'MR и строки', 'каждый фактор — до строчки кода')]
        cells = ''.join('<div style="min-width: 0; position: relative; border-radius: 24px; background: ' + ('rgba(99,213,255,0.08)' if i == 3 else '#1A1925') + '; border: 1px solid ' + ('rgba(99,213,255,0.4)' if i == 3 else 'rgba(255,255,255,0.08)') + '; padding: 24px; display: flex; flex-direction: column; gap: 8px;">'
                        '<div style="' + MONO + ' font-size: 12px; color: #63D5FF;">' + a + ' · ' + e(b).upper() + '</div><div style="font-size: clamp(24px, 2.2vw, 30px); font-weight: 800; letter-spacing: -0.02em; line-height: 1.1;">' + c + '</div>'
                        '<div style="font-size: 15px; color: rgba(255,255,255,0.7); line-height: 1.45;">' + e(d) + '</div></div>' for i, (a, b, c, d) in enumerate(steps))
        quote = ('<div style="margin-top: 16px; border-radius: 28px; background: #12111C; border: 1px solid rgba(255,255,255,0.08); padding: clamp(22px, 2.6vw, 32px); font-size: clamp(18px, 1.5vw, 21px); line-height: 1.55; color: rgba(255,255,255,0.88);">'
                 'Мы не просто говорим «этот разработчик — Middle+, 7,8 из 10». Мы показываем <b style="color: #FFFFFF;">все факторы, из которых сложился грейд</b>, и каждый открывается в отчётах до строчек кода. '
                 'Любую цифру можно проверить самому — так разработка становится прозрачной.</div>')
        return section(method_head('Полная прозрачность: любую цифру можно проверить до строчки кода', 'Грейд — это верхушка. Под ней 10 факторов, под каждым фактором — отчёт, под отчётом — MR и код.') + '<div class="g4">' + cells + '</div>' + quote + method_rhythm() + method_foot(), 'method')
    # n == 4: ритм оценки и рейтинг
    names = [('Ярослав Землинский', None, 'top'), ('Александр Лукьянов', None, 'top'), ('Анна Павловская', None, 'top'), ('…', None, 'mid'), ('Ольга Аристова', None, 'low'), ('Владислав Редкозубов', None, 'low'), ('Александр Марко', None, 'low')]
    rank_rows = ''
    eff = {0: '100%', 1: '100%', 2: '90%', 4: '35%', 5: '19%', 6: '12%'}  # демо, «Рейтинг сотрудников», октябрь 2026
    for i, (nm, _, zone) in enumerate(names):
        if zone == 'mid':
            rank_rows += '<div style="padding: 6px 12px; font-size: 14px; color: rgba(255,255,255,0.4);">…</div>'
            continue
        col = GREEN if zone == 'top' else RED_T
        pos = i + 1 if zone == 'top' else 14 - (6 - i)
        rank_rows += ('<div style="display: grid; grid-template-columns: 36px minmax(0, 1fr) auto; gap: 12px; align-items: center; padding: 10px 12px; border-radius: 12px; background: ' + ('rgba(83,192,77,0.08)' if zone == 'top' else 'rgba(232,101,101,0.08)') + '; margin-bottom: 4px;">'
                      '<b style="font-variant-numeric: tabular-nums;">' + str(pos) + '</b><span style="font-size: 15px;">' + e(nm) + '</span><b style="color: ' + col + '; font-variant-numeric: tabular-nums;">' + eff[i] + '</b></div>')
    rank = ('<article style="min-width: 0; border-radius: 28px; background: #1A1925; border: 1px solid rgba(255,255,255,0.08); padding: clamp(22px, 2.6vw, 32px); display: flex; flex-direction: column; gap: 14px;">'
            '<div style="' + MONO + ' font-size: 12px; color: #63D5FF;">ДЕМО · РЕЙТИНГ ПО КОМПАНИИ · ОКТЯБРЬ</div><div style="font-size: 22px; font-weight: 800;">Топ-20% и 20% отстающих — сразу видно, с кем работать в первую очередь</div>'
            '<div>' + rank_rows + '</div><div style="display: flex; flex-wrap: wrap; gap: 8px;">' + ''.join('<span style="font-size: 13px; padding: 6px 10px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.14); color: rgba(255,255,255,0.8);">' + e(x) + '</span>' for x in ['по компании', 'по стеку', 'по проекту', 'vs среднее по команде', 'vs среднее по стеку', 'vs среднее по компании']) + '</div></article>')
    months = [('Месяц 1', 0, 70), ('Месяц 2', 0, 82), ('Месяц 3', 0, 96)]
    bars = ''.join('<div style="flex: 1 1 0; min-width: 0; display: flex; flex-direction: column; gap: 8px; align-items: stretch;"><div style="height: 140px; display: flex; align-items: flex-end;"><div style="width: 100%; height: ' + str(int(h * 1.3)) + 'px; border-radius: 10px 10px 4px 4px; background: linear-gradient(180deg, #63D5FF, rgba(99,213,255,0.35));"></div></div>'
                   '<div style="text-align: center; font-size: 14px; color: rgba(255,255,255,0.7);">' + m + '</div><div style="text-align: center; font-size: 13px; color: rgba(255,255,255,0.55);">отчёт · рейтинг</div></div>' for m, g, h in months)
    timeline = ('<article style="min-width: 0; border-radius: 28px; background: #1A1925; border: 1px solid rgba(255,255,255,0.08); padding: clamp(22px, 2.6vw, 32px); display: flex; flex-direction: column; gap: 14px;">'
                '<div style="' + MONO + ' font-size: 12px; color: #63D5FF;">РИТМ ОЦЕНКИ</div><div style="font-size: 22px; font-weight: 800;">Эффективность — каждый месяц, грейд — за 3 месяца</div>'
                '<div style="display: flex; gap: 12px;">' + bars + '</div>'
                '<div style="border-top: 2px solid #63D5FF; padding-top: 12px; display: flex; justify-content: space-between; gap: 12px; flex-wrap: wrap;"><span style="font-size: 15px; color: rgba(255,255,255,0.8);">Грейд за 3 месяца</span><b style="font-size: 20px;"><span style="color: #7FDB7A;">Senior</span> 8,5</b></div>'
                '<p style="margin: 0; color: rgba(255,255,255,0.7); font-size: 14px; line-height: 1.5;">Каждый месяц — детальный отчёт и динамика эффективности, грейда и рейтинга на графиках.</p></article>')
    return section(method_head('Каждый месяц — отчёт и рейтинг. Каждые 3 месяца — грейд', 'Полностью автоматически: никаких анкет, самооценок и калибровочных сессий. Нужен только код.') + '<div class="g2">' + timeline + rank + '</div>' + method_foot(), 'method')

# ---------------------------------------------------------------- раунд 30: Grade — 3 полные страницы
def star_demo(vals, size=560, rings=(4.5, 7.5)):
    """Звезда грейда как в демо: сетка 2–10 с подписями шкалы, пунктиры Middle/Senior, цветные точки, подписи осей со значениями."""
    import math
    n = len(vals); c = size / 2; R = size * 0.31; pad = 72
    ang = lambda i: 2 * math.pi * i / n
    pt = lambda i, v: (c + R * v / 10 * math.sin(ang(i)), c - R * v / 10 * math.cos(ang(i)))
    poly = lambda vl: ' '.join('%.1f,%.1f' % pt(i, v) for i, v in enumerate(vl))
    o = ['<svg viewBox="%d 0 %d %d" role="img" aria-label="Звезда грейда по 10 факторам" style="width: 100%%; height: auto; display: block;">' % (-pad, size + 2 * pad, size)]
    for k in (2, 4, 6, 8, 10):
        o.append('<polygon points="%s" fill="%s" stroke="rgba(255,255,255,0.10)" stroke-width="1"></polygon>' % (poly([k] * n), 'rgba(255,255,255,0.015)' if k == 10 else 'none'))
        if k < 10:
            x, y = pt(0, k)
            o.append('<text class="uc-rl" x="%.1f" y="%.1f" fill="rgba(255,255,255,0.35)" font-size="12" font-family="Onest, sans-serif" text-anchor="start">%d</text>' % (x + 6, y + 4, k))
    for i in range(n):
        x, y = pt(i, 10)
        o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="rgba(255,255,255,0.08)"></line>' % (c, c, x, y))
    o.append('<polygon points="%s" fill="none" stroke="rgba(255,255,255,0.55)" stroke-width="1.5" stroke-dasharray="2 4"></polygon>' % poly([rings[0]] * n))
    o.append('<polygon points="%s" fill="none" stroke="rgba(255,255,255,0.7)" stroke-width="1.5" stroke-dasharray="8 5"></polygon>' % poly([rings[1]] * n))
    o.append('<polygon points="%s" fill="rgba(99,213,255,0.20)" stroke="#63D5FF" stroke-width="3" stroke-linejoin="round"></polygon>' % poly([v for _, v in vals]))
    for i, (nm, v) in enumerate(vals):
        x, y = pt(i, v)
        o.append('<circle cx="%.1f" cy="%.1f" r="7" fill="%s" stroke="#12111C" stroke-width="2.5"></circle>' % (x, y, lvl_col(v)))
        lx, ly = c + (R + 24) * math.sin(ang(i)), c - (R + 24) * math.cos(ang(i))
        sx = math.sin(ang(i))
        anchor = 'middle' if abs(sx) < 0.2 else ('start' if sx > 0 else 'end')
        words = nm.split(' ')
        lines = [nm] if len(nm) <= 14 else [' '.join(words[:len(words) // 2 + (len(words) % 2)]), ' '.join(words[len(words) // 2 + (len(words) % 2):])]
        dy0 = -14 - 10 * (len(lines) - 1) if math.cos(ang(i)) > 0.3 else (-4 if abs(math.cos(ang(i))) <= 0.3 else 8)
        for j, ln in enumerate(lines):
            o.append('<text class="uc-rl" x="%.1f" y="%.1f" fill="rgba(255,255,255,0.76)" font-size="16" font-family="Onest, sans-serif" text-anchor="%s">%s</text>' % (lx, ly + dy0 + 19 * j, anchor, e(ln)))
        o.append('<text class="uc-rl" x="%.1f" y="%.1f" fill="%s" font-size="22" font-weight="800" font-family="Bricolage Grotesque, Onest, sans-serif" text-anchor="%s">%s</text>' % (lx, ly + dy0 + 19 * len(lines) + 5, lvl_col(v), anchor, fmt1(v)))
    o.append('</svg>')
    return ''.join(o)

def star_legend():
    return ('<div style="display: flex; flex-wrap: wrap; gap: 8px 20px; justify-content: center; font-size: 13px; color: rgba(255,255,255,0.66); margin-top: 4px;">'
            '<span><span style="display: inline-block; width: 14px; height: 10px; border: 2px solid #63D5FF; background: rgba(99,213,255,0.2); border-radius: 3px; vertical-align: -1px;"></span> оценки за период</span>'
            '<span style="white-space: nowrap;"><span style="letter-spacing: 1px;">····</span> уровень Middle</span><span style="white-space: nowrap;"><span>– – –</span> уровень Senior</span></div>')

def profile_head():
    def kv(k, v, sub=''):
        return ('<div style="min-width: 0;"><div style="font-size: 13px; color: rgba(255,255,255,0.6);">' + e(k) + '</div><div style="font-size: clamp(22px, 2vw, 28px); font-weight: 800; white-space: nowrap;">' + v + '</div>'
                + ('<div style="font-size: 13px; color: rgba(255,255,255,0.55);">' + e(sub) + '</div>' if sub else '') + '</div>')
    return ('<div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 16px 32px; align-items: flex-end; padding-bottom: 24px; border-bottom: 1px solid rgba(255,255,255,0.08);">'
            '<div style="min-width: 0;"><div style="' + MONO + ' font-size: 12px; color: rgba(255,255,255,0.55);">ДЕМО UPCORE · МЕНЮ «УРОВЕНЬ» · ОКТЯБРЬ 2026</div>'
            '<div style="font-size: clamp(22px, 2vw, 28px); font-weight: 800; margin-top: 8px;">Лукьянов Александр</div><div style="font-size: 15px; color: rgba(255,255,255,0.66);">Backend, C# · проект UpCore Backend</div></div>'
            '<div style="display: flex; flex-wrap: wrap; gap: 20px 36px;">'
            + kv('Грейд за 3 месяца', '<span style="color: #7FDB7A;">Senior</span> 8,5<span style="font-size: 16px; color: rgba(255,255,255,0.5);"> / 10</span>')
            + kv('Динамика роста', '<span style="color: ' + AMBER + ';">Middle+</span> → <span style="color: #7FDB7A;">Senior</span>', '7,2 → 8,5 с мая по октябрь')
            + kv('Рейтинг за месяц', '2 <span style="font-size: 16px; color: rgba(255,255,255,0.5);">из 14</span>', 'в компании · 4 из 13 в стеке · 4 из 8 в проекте') + '</div></div>')

def method_example(h2='Грейд — сложная математика по 10+ факторам. Главный — эффективность кода в часах', insights_on=True, list_label='10 ФАКТОРОВ ГРЕЙДА'):
    """Методика + пример в одном блоке: звезда как в демо, 10 факторов с описанием и динамикой, сильные стороны / зона роста."""
    rows = ''.join('<div style="display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 4px 16px; align-items: baseline; padding: 10px 0; border-top: 1px solid rgba(255,255,255,0.07);">'
                   '<span style="min-width: 0;"><b style="font-size: 16px; color: ' + ('#63D5FF' if i == 0 else '#FFFFFF') + ';">' + e(n) + (' · главный фактор' if i == 0 else '') + '</b><br><span style="font-size: 14px; color: rgba(255,255,255,0.6);">' + e(d.replace(' — главный фактор', '')) + '</span></span>'
                   '<span style="white-space: nowrap; font-variant-numeric: tabular-nums;"><span style="font-size: 13px; color: rgba(255,255,255,0.5);">' + fmt1(w) + ' → </span><b style="font-size: 19px; color: ' + lvl_col(v) + ';">' + fmt1(v) + '</b> ' + arrow(v, w) + '</span></div>'
                   for i, (n, v, w, d) in enumerate(LEVEL))
    insights = ('<div class="g3" style="margin-top: 24px;">'
                + card('<div style="' + MONO + ' font-size: 12px; color: #7FDB7A;">СИЛЬНЫЕ СТОРОНЫ</div><p style="margin: 0; font-size: 15px; line-height: 1.55; color: rgba(255,255,255,0.84);">Эффективность 10 из 10: 889 часов результата при 436 рабочих, 123 MR за период. 91% кода дошло до релиза, тех-метч с проектом — 95%.</p>', pad='22px', bg='rgba(83,192,77,0.06)', border='rgba(83,192,77,0.3)', gap=8)
                + card('<div style="' + MONO + ' font-size: 12px; color: ' + AMBER + ';">ЗОНА РОСТА</div><p style="margin: 0; font-size: 15px; line-height: 1.55; color: rgba(255,255,255,0.84);">Архитектурная сложность 3,1: 80% времени — периферия, в ядре системы только 7%. Следующий шаг к росту — задачи в ядре.</p>', pad='22px', bg='rgba(242,193,78,0.06)', border='rgba(242,193,78,0.3)', gap=8)
                + card('<div style="' + MONO + ' font-size: 12px; color: #63D5FF;">ПРОВЕРИТЬ САМОМУ</div><p style="margin: 0; font-size: 15px; line-height: 1.55; color: rgba(255,255,255,0.84);">Каждый фактор раскрывается в меню «Отчёты», а оттуда — до MR и строчек кода в «Глазе». Ни одной цифры «на веру».</p>', pad='22px', bg='rgba(99,213,255,0.06)', border='rgba(99,213,255,0.3)', gap=8)
                + '</div>')
    body = ('<div style="border-radius: 32px; background: #12111C; border: 1px solid rgba(99,213,255,0.35); padding: clamp(24px, 3.4vw, 44px);">' + profile_head() +
            '<div style="display: flex; flex-wrap: wrap; gap: 24px 48px; align-items: center; margin-top: 24px;">'
            '<div style="flex: 1.1 1 420px; min-width: 0; max-width: 600px; margin: 0 auto;"><div style="' + MONO + ' font-size: 12px; color: rgba(255,255,255,0.55); margin-bottom: 4px;">УРОВЕНЬ РАБОТЫ · <span style="color: #7FDB7A;">SENIOR 8,5 / 10</span></div>' + star_demo([(n, v) for n, v, _, _ in LEVEL]) + star_legend() + '</div>'
            '<div style="flex: 1 1 400px; min-width: 0;"><div style="display: flex; justify-content: space-between; gap: 12px; padding-bottom: 8px; ' + MONO + ' font-size: 12px; color: rgba(255,255,255,0.5);"><span>' + list_label + '</span><span>МАЙ → ОКТЯБРЬ</span></div>' + rows + '</div></div>'
            + (insights if insights_on else '') + '</div>')
    return section(sec_head('МЕТОДИКА НА ПРИМЕРЕ', h2, 'Реальный профиль из демо UpCore: не просто «Senior», а все факторы, из которых он сложился, — с динамикой за полгода и местом в рейтинге.', 'grade') + body, 'method')

def factors_deep():
    """Подробный разбор 3 важных факторов (из 50+) — тексты, которые одобрил владелец."""
    arch = ('<div style="display: flex; flex-direction: column; gap: 8px;">'
            + ''.join('<div><div style="display: flex; justify-content: space-between; gap: 12px; font-size: 14px; margin-bottom: 4px;"><span>' + a + '</span><b style="white-space: nowrap;">' + b + '</b></div>'
                      '<div style="height: 8px; border-radius: 4px; background: rgba(255,255,255,0.06); overflow: hidden;"><div style="width: ' + str(w) + '%; height: 100%; background: ' + c + ';"></div></div></div>'
                      for a, b, w, c in [('Ядро', '59 ч · 7%', 7, '#63D5FF'), ('Middle', '116 ч · 13%', 13, 'rgba(99,213,255,0.6)'), ('Периферия', '713 ч · 80%', 80, 'rgba(255,255,255,0.35)')])
            + '<div style="font-size: 12px; color: rgba(255,255,255,0.5);">пример из демо: архитектурная сложность 3,1 / 10</div></div>')
    tech = ('<div style="display: flex; flex-direction: column; gap: 8px;">'
            + ''.join('<div style="display: flex; justify-content: space-between; gap: 12px; font-size: 14px; padding: 8px 12px; border-radius: 12px; background: rgba(255,255,255,0.04);"><span>' + e(a) + '</span><b style="color: ' + c + '; white-space: nowrap;">' + e(b) + '</b></div>'
                      for a, b, c in [('Senior-технологии', '2 · 1,8 ч', GREEN), ('Middle-технологии', '16 · 191,4 ч', '#FFFFFF'), ('Ввёл в проект новых', '1', '#63D5FF'), ('Легаси / новое для себя', 'учитывается', 'rgba(255,255,255,0.7)')]) + '</div>')
    churn = ('<div><div style="display: flex; height: 18px; border-radius: 9px; overflow: hidden; gap: 3px;"><div style="flex: 150 1 0; background: #63D5FF;"></div><div style="flex: 150 1 0; background: rgba(232,101,101,0.5);"></div></div>'
             '<div style="display: flex; justify-content: space-between; gap: 8px; font-size: 13px; color: rgba(255,255,255,0.66); margin-top: 8px;"><span><b style="color: #63D5FF;">150 строк</b> дошли до релиза</span><span><b style="color: ' + RED_T + ';">150</b> удалены и переписаны</span></div></div>')
    def deep(num, title, viz, text):
        return ('<article style="min-width: 0; border-radius: 28px; background: #1A1925; border: 1px solid rgba(255,255,255,0.08); padding: clamp(22px, 2.6vw, 32px); display: flex; flex-direction: column; gap: 16px;">'
                '<div style="' + MONO + ' font-size: 12px; color: #63D5FF;">' + num + '</div><div style="font-size: 22px; font-weight: 800; line-height: 1.2;">' + e(title) + '</div>' + viz +
                '<p style="margin: 0; color: rgba(255,255,255,0.78); font-size: 15px; line-height: 1.55;">' + e(text) + '</p></article>')
    cards = (deep('ФАКТОР · АРХИТЕКТУРА', 'Где написан код: в ядре или на периферии', arch, 'Строим AST-дерево всего проекта и видим, где работает разработчик. 20 строк в ядре системы бывают сложнее и ценнее 200 строк на периферии, которые меняют цвет кнопок.')
             + deep('ФАКТОР · ТЕХНОЛОГИИ', 'Какие технологии и в каком объёме', tech, 'Разбираем каждую строчку и считаем часы по каждой технологии. Карта компетенций стека задаёт её сложность и грейд. Учитываем легаси, новое для человека и новые технологии, которые он ввёл в проект.')
             + deep('ФАКТОР · РЕЗУЛЬТИРУЮЩИЙ КОД', 'Сколько кода дошло до релиза', churn, 'Написал 300 строк, а назавтра половину удалили и переписали — значит, до релиза дошло 50% работы. Фактор особенно важен с ИИ и отсекает любые накрутки.'))
    return section(sec_head('ПОДРОБНО О ФАКТОРАХ', 'Разбираем подробно несколько важных факторов — из 50+', 'Мы анализируем каждую строчку кода. Вот три фактора, которые не покажут ни резюме, ни самооценка, ни выборочное ревью.', 'grade') + '<div class="g3">' + cards + '</div>', 'factors')

def rating_card():
    names = [('Ярослав Землинский', '100%', 'top', 1), ('Александр Лукьянов', '100%', 'top', 2), ('Анна Павловская', '90%', 'top', 3), ('…', '', 'mid', 0),
             ('Ольга Аристова', '35%', 'low', 12), ('Владислав Редкозубов', '19%', 'low', 13), ('Александр Марко', '12%', 'low', 14)]
    rows = ''
    for nm, ef, z, pos in names:
        if z == 'mid':
            rows += '<div style="padding: 4px 12px; font-size: 14px; color: rgba(255,255,255,0.4);">…</div>'
            continue
        rows += ('<div style="display: grid; grid-template-columns: 32px minmax(0, 1fr) auto; gap: 12px; align-items: center; padding: 10px 12px; border-radius: 12px; margin-bottom: 4px; background: ' + ('rgba(83,192,77,0.08)' if z == 'top' else 'rgba(232,101,101,0.08)') + ';">'
                 '<b style="font-variant-numeric: tabular-nums;">' + str(pos) + '</b><span style="font-size: 15px; min-width: 0;">' + e(nm) + '</span><b style="color: ' + (GREEN if z == 'top' else RED_T) + '; font-variant-numeric: tabular-nums;">' + ef + '</b></div>')
    tags = ''.join('<span style="font-size: 13px; padding: 6px 10px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.14); color: rgba(255,255,255,0.8);">' + e(x) + '</span>' for x in ['по компании', 'по стеку', 'по проекту', 'vs среднее по команде', 'vs среднее по стеку', 'vs среднее по компании'])
    return ('<div style="display: flex; justify-content: space-between; gap: 12px; ' + MONO + ' font-size: 12px; color: rgba(255,255,255,0.55); margin-bottom: 10px;"><span>ДЕМО · РЕЙТИНГ ПО КОМПАНИИ</span><span>ОКТЯБРЬ 2026</span></div>'
            '<div style="display: flex; justify-content: space-between; ' + MONO + ' font-size: 12px; margin-bottom: 6px;"><span style="color: ' + GREEN + ';">ТОП-20%</span><span style="color: rgba(255,255,255,0.45);">эффективность</span></div>' + rows +
            '<div style="' + MONO + ' font-size: 12px; color: ' + RED_T + '; margin: 2px 0 12px;">20% ОТСТАЮЩИХ — С НИМИ РАБОТАТЬ В ПЕРВУЮ ОЧЕРЕДЬ</div><div style="display: flex; flex-wrap: wrap; gap: 8px;">' + tags + '</div>')

def rhythm_block(with_rating=True):
    """Один блок: каждый месяц (отчёт, рейтинг, сравнения, динамика) + каждые 3 месяца (грейд)."""
    li = lambda xs: ''.join('<li style="margin: 0 0 8px;">' + e(x) + '</li>' for x in xs)
    month = ['Эффективность и детальный отчёт за месяц', 'Рейтинг по компании, стеку и проекту: топ-20% и 20% отстающих', 'Сравнение со средним по команде, стеку и компании', 'Динамика эффективности, грейда и рейтинга на графиках']
    steps = ''.join('<div style="flex: 1 1 0; min-width: 0; text-align: center; padding: 10px 6px; border-radius: 12px; background: rgba(99,213,255,0.08); border: 1px solid rgba(99,213,255,0.25); font-size: 14px;"><b>Месяц ' + str(i) + '</b><div style="font-size: 12px; color: rgba(255,255,255,0.6);">отчёт · рейтинг</div></div>' for i in (1, 2, 3))
    timeline = ('<div style="display: flex; gap: 8px; align-items: stretch;">' + steps +
                '<div style="flex: 1.1 1 0; min-width: 0; text-align: center; padding: 10px 6px; border-radius: 12px; background: #63D5FF; color: #0D0C15; font-size: 14px;"><b>Грейд</b><div style="font-size: 12px;">за 3 месяца</div></div></div>')
    inner = ('<div style="display: flex; flex-direction: column; gap: 22px;">' + timeline +
             '<div style="display: flex; flex-wrap: wrap; gap: 24px 40px;">'
             '<div style="flex: 1.3 1 300px; min-width: 0;"><div style="' + MONO + ' font-size: 12px; color: #63D5FF; margin-bottom: 10px;">КАЖДЫЙ МЕСЯЦ</div><ul style="margin: 0; padding-left: 20px; color: rgba(255,255,255,0.86); font-size: 16px; line-height: 1.5;">' + li(month) + '</ul></div>'
             '<div style="flex: 1 1 240px; min-width: 0; border-left: 1px solid rgba(255,255,255,0.08); padding-left: 24px;"><div style="' + MONO + ' font-size: 12px; color: #63D5FF; margin-bottom: 10px;">КАЖДЫЕ 3 МЕСЯЦА</div><div style="font-size: 24px; font-weight: 800; margin-bottom: 8px;">Грейд</div>'
             '<p style="margin: 0; color: rgba(255,255,255,0.8); font-size: 15px; line-height: 1.55;">Грейд считаем по трём месяцам работы: так данных хватает для объективной оценки, а случайный месяц не перекашивает результат.</p></div></div>'
             '<div style="display: flex; flex-wrap: wrap; gap: 8px 24px; justify-content: space-between; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 16px; font-size: 15px; color: rgba(255,255,255,0.8);"><span>Всё — автоматически. <b style="color: #FFFFFF;">Нужен только код.</b></span><span style="color: rgba(255,255,255,0.66);">Гибкая интеграция с вашими системами и по протоколу MCP.</span></div></div>')
    box = 'border-radius: 32px; background: #12111C; border: 1px solid rgba(255,255,255,0.08); padding: clamp(24px, 3.4vw, 40px);'
    if with_rating:
        body = ('<div style="display: flex; flex-wrap: wrap; gap: 16px;"><div style="flex: 1.2 1 480px; min-width: 0; ' + box + '">' + inner + '</div>'
                '<div style="flex: 1 1 380px; min-width: 0; ' + box + '">' + rating_card() + '</div></div>')
    else:
        body = '<div style="' + box + '">' + inner + '</div>'
    return section(sec_head('РИТМ ОЦЕНКИ', 'Каждый месяц — отчёт и рейтинг. Каждые 3 месяца — грейд', 'Полностью автоматически: никаких анкет, самооценок и калибровочных сессий.', 'grade') + body, 'rhythm')

def transparency_block():
    steps = [('01', 'Грейд', '<span style="color: ' + AMBER + ';">Middle+</span> 7,8', 'одна цифра за 3 месяца'),
             ('02', 'Меню «Уровень»', '10 факторов', 'звезда грейда, динамика и дашборд'),
             ('03', 'Меню «Отчёты»', 'Архитектура 3,1', 'ядро 59 ч · middle 116 ч · периферия 713 ч'),
             ('04', '«Глаз»', 'MR и строки', 'каждый фактор — до строчки кода')]
    cells = ''.join('<div style="min-width: 0; border-radius: 24px; background: ' + ('rgba(99,213,255,0.08)' if i == 3 else '#1A1925') + '; border: 1px solid ' + ('rgba(99,213,255,0.4)' if i == 3 else 'rgba(255,255,255,0.08)') + '; padding: 24px; display: flex; flex-direction: column; gap: 8px;">'
                    '<div style="' + MONO + ' font-size: 12px; color: #63D5FF;">' + a + ' · ' + e(b).upper() + '</div><div style="font-size: clamp(24px, 2.2vw, 30px); font-weight: 800; letter-spacing: -0.02em; line-height: 1.1;">' + c + '</div>'
                    '<div style="font-size: 15px; color: rgba(255,255,255,0.7); line-height: 1.45;">' + e(d) + '</div></div>' for i, (a, b, c, d) in enumerate(steps))
    quote = ('<div style="margin-top: 16px; border-radius: 28px; background: #12111C; border: 1px solid rgba(255,255,255,0.08); padding: clamp(22px, 2.6vw, 32px); font-size: clamp(18px, 1.5vw, 21px); line-height: 1.55; color: rgba(255,255,255,0.88);">'
             'Мы не просто говорим «этот разработчик — Middle+, 7,8 из 10». Мы показываем <b style="color: #FFFFFF;">все факторы, из которых сложился грейд</b>, и каждый открывается в отчётах до строчек кода. '
             'Любую цифру можно проверить самому — так разработка становится прозрачной.</div>')
    return section(sec_head('ПРОЗРАЧНОСТЬ', 'Любую цифру можно проверить до строчки кода', 'Грейд — это верхушка. Под ней 10 факторов, под каждым фактором — отчёт, под отчётом — MR и код.', 'grade') + '<div class="g4">' + cells + '</div>' + quote, 'transparency')

def drill_visual():
    rows = [('ГРЕЙД', '<span style="color: ' + AMBER + ';">Middle+</span> 7,8 / 10', '100%'), ('ФАКТОР', 'Архитектурная сложность 3,1', '88%'),
            ('ОТЧЁТ', 'Ядро 59 ч · Middle 116 ч · Периферия 713 ч', '76%'), ('КОД', 'MR → файлы → строки в «Глазе»', '64%')]
    out = ''.join('<div style="margin-left: ' + str(i * 18) + 'px; border-radius: 18px; background: ' + ('rgba(99,213,255,0.1)' if i == 3 else '#1A1925') + '; border: 1px solid ' + ('rgba(99,213,255,0.45)' if i == 3 else 'rgba(255,255,255,0.1)') + '; padding: 16px 18px; display: flex; flex-direction: column; gap: 4px;">'
                  '<span style="' + MONO + ' font-size: 12px; color: #63D5FF;">' + '%02d' % (i + 1) + ' · ' + a + '</span><span style="font-size: clamp(17px, 1.5vw, 21px); font-weight: 800; line-height: 1.25;">' + b + '</span></div>' for i, (a, b, _) in enumerate(rows))
    return ('<div style="flex: 1.15 1 480px; min-width: 0; position: relative;"><div style="border-radius: 24px; background: #12111C; border: 1px solid rgba(99,213,255,0.4); box-shadow: 0 40px 120px rgba(99,213,255,0.10); padding: 22px; display: flex; flex-direction: column; gap: 10px;">'
            '<div style="display: flex; justify-content: space-between; ' + MONO + ' font-size: 13px; color: rgba(255,255,255,0.72); padding-bottom: 6px; border-bottom: 1px solid rgba(255,255,255,0.08);"><span>upcore://grade / от цифры к коду</span><span style="color: #63D5FF;">● прозрачно</span></div>' + out + '</div></div>')

GRADE_STATS = [('96%', 'точность экспертной оценки на 300+ тыс. MR'), ('10+', 'факторов грейда, главный — эффективность в часах'), ('3 мес.', 'до объективного грейда'), ('1 день', 'до первых результатов')]

def grade_hero(h1, sub, visual, kicker=None, st=None):
    line, txt = ACC['grade']
    name = ('<div style="font-family: \'Bricolage Grotesque\', \'Onest\', sans-serif; font-weight: 800; font-size: clamp(36px, 4vw, 56px); line-height: 1; letter-spacing: -0.035em; display: flex; align-items: baseline; gap: 12px;">'
            '<span style="color: #63D5FF;">&gt;</span><span>UpCore<span style="color: #63D5FF;">.Grade</span></span></div>')
    kick = ('<div style="font-size: 19px; color: rgba(255,255,255,0.72); font-style: italic;">' + e(kicker) + '</div>') if kicker else ''
    ctas = btn('Подключить UpCore', REG) + btn('Получить демо-отчёт', MAIL, False)
    return ('<section id="top" style="position: relative; max-width: 1280px; margin: 0 auto; padding: 40px 32px 96px; display: flex; flex-wrap: wrap; gap: 56px; align-items: center;">' + CHEVRON +
            '<div style="flex: 1 1 500px; min-width: 0; position: relative; display: flex; flex-direction: column; gap: 24px;">'
            '<div style="display: flex; flex-wrap: wrap; gap: 8px 16px; ' + MONO + ' font-size: 13px; color: rgba(255,255,255,0.62);"><span style="color: #63D5FF;">01 · ОБЪЕКТИВНАЯ ОЦЕНКА РАЗРАБОТЧИКА</span><span>CTO · HRD · ТИМЛИДЫ</span></div>'
            + name + kick +
            '<h1 style="margin: 0; font-size: clamp(32px, 3.4vw, 50px); line-height: 1.05; letter-spacing: -0.03em; font-weight: 800;">' + h1 + '</h1>'
            '<p style="margin: 0; font-size: clamp(17px, 1.35vw, 20px); line-height: 1.55; color: rgba(255,255,255,0.8); max-width: 600px;">' + e(sub) + '</p>'
            '<div style="display: flex; flex-wrap: wrap; gap: 12px;">' + ctas + '</div>' + stats(st or GRADE_STATS) + '</div>' + visual + '</section>')

GRADE_FAQ = [
    ('Это слежка за разработчиками?', 'Нет. Мы не считаем время в IDE, клики, скриншоты и активность в мессенджерах. Оценивается только результат — код, который вошёл в продукт. Это обычное код-ревью, только его делает цифровой тимлид.'),
    ('Разве код нельзя «накрутить»?', 'Строки и коммиты — можно. Поэтому UpCore очищает код от шума — автогенерации, копипаста, бойлерплейта, ренеймов, — взвешивает его по архитектуре и учитывает только результирующий код, который дошёл до релиза.'),
    ('А если оценка ошибётся?', 'Грейд считается по трём месяцам работы, а не по одной задаче. Любой фактор открывается в «Отчётах» и в «Глазе» до строчки кода, а сотрудник может подать апелляцию.'),
    ('Как к этому отнесутся разработчики?', 'Сильные — с облегчением: отчёты не нужны, правила честные, вклад виден. Прозрачность сразу даёт команде в среднем +12% к производительности.')]
GRADE_ROLES = [('CTO', 'Видит реальную силу команд и проектов, топ-20% для сложных задач и 20% отстающих, с которыми нужно работать в первую очередь.'),
               ('HRD', 'Повышения, пересмотр зарплат, калибровка грейдов и испытательный срок — на данных, а не на впечатлениях.'),
               ('Тимлид', 'Не тратит часы на оценку каждого разработчика и не спорит на ревью: у всех один расчёт, который можно проверить.'),
               ('Разработчик', 'Никаких отчётов и тайм-трекеров. Вклад наконец виден, а путь к следующему грейду — понятен по каждому фактору.')]

def grade_page(n):
    if n == 1:
        top = grade_hero('Грейд, который подтверждает код', 'Объективная оценка разработчика по реальному коду: эффективность в часах, грейд по 10+ факторам и рейтинг по компании, стеку и проекту. Каждую цифру можно проверить до строчки кода.',
                         image_console('star', 'grade / уровень', 'Звезда грейда', '10 факторов и динамика роста', 'grade'))
        blocks = [method_example(), factors_deep(), rhythm_block(True), transparency_block(),
                  modules('ЧТО ВНУТРИ', 'Всё для решений о людях — на данных, а не на впечатлениях', [
                      ('Эффективность в часах и рублях', 'Время UpCore против рабочего времени: создано ценности, упущенная выгода и реальная ставка за час результата. Каждый месяц.'),
                      ('Грейд по 10+ факторам', 'Звезда грейда, динамика роста и дашборд по каждому фактору. Главный фактор — эффективность кода в часах.'),
                      ('Рейтинг каждый месяц', 'По компании, стеку и проекту. Топ-20% и 20% отстающих видны сразу, плюс сравнение со средним.'),
                      ('Авто-резюме по коду', 'Какие технологии и на каком уровне человек реально использует — по карте компетенций стека.'),
                      ('Онбординг и испытательный срок', 'За сколько недель новичок вышел на среднюю эффективность команды — решение по испытательному сроку на фактах.'),
                      ('Отчёты, «Глаз» и апелляции', 'Каждый фактор раскрывается до строчки кода. Сотрудник видит тот же расчёт и может его оспорить.')], 'grade')]
    elif n == 2:
        top = grade_hero('Не просто «Middle+, 7,8 из 10». Все факторы — до строчки кода', 'UpCore.Grade считает грейд по 10+ факторам и показывает каждый: от звезды грейда до MR и строк кода. Оценка, которую можно проверить, — а не мнение.', drill_visual())
        blocks = [method_example('Главный фактор — эффективность кода в часах. Ещё девять уточняют уровень'), factors_deep(), rhythm_block(True)]
    else:
        # раунд 31: принят за основу; правки владельца — без вопроса-кикера, 50+ факторов, новые цифры, без «Прозрачности» и «Ритма»
        top = grade_hero('Объективная оценка разработчика — и рейтинг всей команды каждый месяц', 'Эффективность каждого разработчика в часах, рейтинг по компании, стеку и проекту, а также объективный грейд по 50+ факторам. Полностью автоматически: нужен только код.',
                         '<div style="flex: 1 1 460px; min-width: 0;"><div style="border-radius: 24px; background: #12111C; border: 1px solid rgba(99,213,255,0.4); box-shadow: 0 40px 120px rgba(99,213,255,0.10); padding: 22px;">' + rating_card() + '</div></div>',
                         st=[('96%', 'точность от экспертной оценки на 300+ тыс. MR'), ('50+', 'факторов грейда'), ('1500+', 'разработчиков уже посчитано'), ('1 день', 'до первых результатов')])
        blocks = [method_example('Грейд — сложная математика по 50+ факторам', insights_on=False, list_label='10 ОСНОВНЫХ ФАКТОРОВ'), factors_deep()]
    body = [header('grade'), top] + blocks + [
        roles('ДЛЯ КОГО', 'Одна цифра для CTO, HR, тимлида и разработчика', GRADE_ROLES, 'grade'),
        faq(GRADE_FAQ, acc_key='grade'),
        saas_variant(2),  # раунд 35: единый блок «SaaS и безопасность»
        cta('Узнайте реальный грейд своей команды', 'Подключите репозиторий — оценка по истории за 3 месяца, без ожидания и анкет.', ('Подключить UpCore', REG)),
        footer()]
    return page('UpCore Grade — макет %d' % n, '\n'.join(body), 6000, name='Grade-%d' % n)

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
        saas_variant(2),  # раунд 34: принят вариант 2 блока «SaaS и безопасность»
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
                ('Подтверждённый грейд', 'Junior− … Senior по 10+ факторам, главный — эффективность кода в часах. Звезда грейда, динамика и дашборд по каждому фактору.'),
                ('Рейтинг и красная зона', 'Рейтинг по компании, стеку и проекту. Сразу видно лидеров — и тех, кто 2 месяца подряд ниже нормы.'),
                ('Авто-резюме по коду', 'Какие технологии и на каком уровне человек реально использует. Цифровой паспорт опыта вместо слов в резюме.'),
                ('Онбординг и испытательный срок', 'За сколько недель новичок вышел на среднюю эффективность команды — решение по испытательному сроку на фактах.'),
                ('«Глаз» и апелляции', 'Расчёт до строчки кода. Сотрудник видит ту же оценку, что и руководитель, и может её оспорить.')], 'grade'),
            method_variant(1),  # раунд 29: методика (варианты Method-1..4), блок «Результаты» убран
            grade_example_v2(),
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
            saas_variant(2),
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
            saas_variant(2),
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
            saas_variant(2),
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
            saas_variant(2),
            cta('Дайте каждому разработчику своего наставника', 'Подключите репозиторий — первые рекомендации по истории MR вашей команды.'),
            footer()]
    return page('UpCore %s — страница A' % names[key], '\n'.join(body), 5400, name='%s-A' % names[key])

# ---------------------------------------------------------------- раунд 36: страницы AI, Projects, Mentor (по образцу Grade) и Блог — по 3 макета
MODC = {'ai': ('AI', '02', 'ЭФФЕКТИВНОСТЬ ИИ И ВАЙБКОДИНГА', 'CTO · CFO · ТИМЛИДЫ'),
        'projects': ('Projects', '03', 'БЮДЖЕТ ПРОЕКТА И КОНТРОЛЬ ПОДРЯДЧИКОВ', 'CEO · PMO · CFO'),
        'mentor': ('Mentor', '04', 'ИИ-НАСТАВНИК ДЛЯ КАЖДОГО РАЗРАБОТЧИКА', 'ТИМЛИДЫ · L&D · РАЗРАБОТЧИКИ')}

def mod_hero(key, h1, sub, visual, st):
    line, txt = ACC[key]; mod, num, lab, rl = MODC[key]
    name = ('<div style="font-family: \'Bricolage Grotesque\', \'Onest\', sans-serif; font-weight: 800; font-size: clamp(36px, 4vw, 56px); line-height: 1; letter-spacing: -0.035em; display: flex; align-items: baseline; gap: 12px;">'
            '<span style="color: ' + line + ';">&gt;</span><span>UpCore<span style="color: ' + txt + ';">.' + mod + '</span></span></div>')
    sec = btn('Заказать аудит', MAIL, False) if key == 'projects' else btn('Получить демо-отчёт', MAIL, False)
    return ('<section id="top" style="position: relative; max-width: 1280px; margin: 0 auto; padding: 40px 32px 96px; display: flex; flex-wrap: wrap; gap: 56px; align-items: center;">' + CHEVRON +
            '<div style="flex: 1 1 500px; min-width: 0; position: relative; display: flex; flex-direction: column; gap: 24px;">'
            '<div style="display: flex; flex-wrap: wrap; gap: 8px 16px; ' + MONO + ' font-size: 13px; color: rgba(255,255,255,0.62);"><span style="color: ' + txt + ';">' + num + ' · ' + e(lab) + '</span><span>' + e(rl) + '</span></div>'
            + name +
            '<h1 style="margin: 0; font-size: clamp(32px, 3.4vw, 50px); line-height: 1.05; letter-spacing: -0.03em; font-weight: 800;">' + h1 + '</h1>'
            '<p style="margin: 0; font-size: clamp(17px, 1.35vw, 20px); line-height: 1.55; color: rgba(255,255,255,0.8); max-width: 600px;">' + e(sub) + '</p>'
            '<div style="display: flex; flex-wrap: wrap; gap: 12px;">' + btn('Подключить UpCore', REG) + sec + '</div>' + stats(st) + '</div>' + visual + '</section>')

def panel(key, path, right, body, flex='1.15 1 480px'):
    line, txt = ACC[key]
    return ('<div style="flex: ' + flex + '; min-width: 0; position: relative;"><div style="border-radius: 24px; background: #12111C; border: 1px solid ' + line + '66; box-shadow: 0 40px 120px rgba(99,213,255,0.10); overflow: hidden;">'
            '<div style="display: flex; justify-content: space-between; gap: 12px; flex-wrap: wrap; padding: 14px 18px; border-bottom: 1px solid rgba(255,255,255,0.08); ' + MONO + ' font-size: 13px; color: rgba(255,255,255,0.72);"><span>upcore://' + e(path) + '</span><span style="color: ' + txt + ';">' + e(right) + '</span></div>'
            '<div style="padding: 20px;">' + body + '</div></div></div>')

def tile(big, small, col='#FFFFFF'):
    return ('<div style="min-width: 0; border-radius: 16px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); padding: 14px 16px;">'
            '<div style="font-size: clamp(22px, 2vw, 28px); font-weight: 800; letter-spacing: -0.02em; white-space: nowrap; color: ' + col + '; font-variant-numeric: tabular-nums;">' + big + '</div>'
            '<div style="font-size: 13px; color: rgba(255,255,255,0.66); line-height: 1.4; margin-top: 2px;">' + e(small) + '</div></div>')

def hbar(label, val_txt, pct, col, sub=''):
    return ('<div><div style="display: flex; justify-content: space-between; gap: 12px; font-size: 14px; margin-bottom: 5px;"><span style="min-width: 0;">' + e(label) + '</span><b style="white-space: nowrap; color: ' + col + ';">' + val_txt + '</b></div>'
            '<div style="height: 8px; border-radius: 4px; background: rgba(255,255,255,0.06); overflow: hidden;"><div style="width: ' + str(pct) + '%; height: 100%; background: ' + col + ';"></div></div>'
            + ('<div style="font-size: 12px; color: rgba(255,255,255,0.5); margin-top: 3px;">' + e(sub) + '</div>' if sub else '') + '</div>')

def deep_block(key, h2, lead, items, cols='g2'):
    line, txt = ACC[key]
    cards = ''.join('<article style="min-width: 0; border-radius: 28px; background: #1A1925; border: 1px solid rgba(255,255,255,0.08); padding: clamp(22px, 2.6vw, 32px); display: flex; flex-direction: column; gap: 16px;">'
                    '<div style="' + MONO + ' font-size: 12px; color: ' + txt + ';">' + e(a) + '</div><div style="font-size: 22px; font-weight: 800; line-height: 1.2;">' + e(b) + '</div>' + viz +
                    '<p style="margin: 0; color: rgba(255,255,255,0.78); font-size: 15px; line-height: 1.55;">' + e(t) + '</p></article>' for a, b, viz, t in items)
    return section(sec_head('ПОДРОБНО О ФАКТОРАХ', h2, lead, key) + '<div class="' + cols + '">' + cards + '</div>', 'factors')

def example_shell(key, label, h2, lead, head_html, body_html):
    line, txt = ACC[key]
    return section(sec_head(label, h2, lead, key) + '<div style="border-radius: 32px; background: #12111C; border: 1px solid ' + line + '59; padding: clamp(24px, 3.4vw, 44px); display: flex; flex-direction: column; gap: 24px;">' + head_html + body_html + '</div>', 'example')

def demo_head(key, title, sub, kvs):
    line, txt = ACC[key]
    kv = ''.join('<div style="min-width: 0;"><div style="font-size: 13px; color: rgba(255,255,255,0.6);">' + e(k) + '</div><div style="font-size: clamp(22px, 2vw, 28px); font-weight: 800; white-space: nowrap;">' + v + '</div>'
                 + ('<div style="font-size: 13px; color: rgba(255,255,255,0.55);">' + e(s_) + '</div>' if s_ else '') + '</div>' for k, v, s_ in kvs)
    return ('<div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 16px 32px; align-items: flex-end; padding-bottom: 22px; border-bottom: 1px solid rgba(255,255,255,0.08);">'
            '<div style="min-width: 0;"><div style="' + MONO + ' font-size: 12px; color: rgba(255,255,255,0.55);">' + e(sub) + '</div><div style="font-size: clamp(22px, 2vw, 28px); font-weight: 800; margin-top: 8px;">' + e(title) + '</div></div>'
            '<div style="display: flex; flex-wrap: wrap; gap: 20px 36px;">' + kv + '</div></div>')

# ------------------------------- AI
AI_MR = [('№ 2494', 'Обновление выводов', 100, '2,5 ч', '1 ч', '7 · 70'), ('№ 2376', 'Поиск по виджетам', 100, '9,7 ч', '1 ч', '1 · 10'),
         ('№ 2356', 'Учёт работы в выходные', 90, '5,3 ч', '5,9 ч', '1 · 7'), ('№ 2374', 'Грейды и рост: зона внимания', 67, '1,2 ч', '1,8 ч', '1 · 8'),
         ('№ 2271', 'Повторная оценка строк в MR', 39, '5,4 ч', '13,7 ч', '1 · 2'), ('№ 2370', 'Пороги динамики эффективности', 22, '2,5 ч', '11,3 ч', '1 · 8')]

def ai_mr_rows(short=False):
    head = ('<div style="display: grid; grid-template-columns: minmax(0, 1fr) 64px 120px; gap: 10px; ' + MONO + ' font-size: 12px; color: rgba(255,255,255,0.5); padding: 0 0 8px;">'
            '<span>MR, СДЕЛАННЫЕ С ИИ</span><span style="text-align: right;">ЭФФ.</span><span style="text-align: right;">UPCORE / СПИСАНО</span></div>')
    rows = ''.join('<div style="display: grid; grid-template-columns: minmax(0, 1fr) 64px 120px; gap: 10px; align-items: baseline; padding: 10px 0; border-top: 1px solid rgba(255,255,255,0.07); font-size: 14px;">'
                   '<span style="min-width: 0;"><span style="' + MONO + ' font-size: 12px; color: rgba(255,255,255,0.5);">' + a + '</span> ' + e(b) + '</span>'
                   '<b style="text-align: right; color: ' + (GREEN if c >= 85 else (AMBER if c >= 60 else RED_T)) + '; font-variant-numeric: tabular-nums;">' + str(c) + '%</b>'
                   '<span style="text-align: right; white-space: nowrap; color: rgba(255,255,255,0.8); font-variant-numeric: tabular-nums;">' + d + ' / ' + f + '</span></div>' for a, b, c, d, f, g in (AI_MR[:4] if short else AI_MR))
    return head + rows

def ai_smj(compact=False):
    rows = [('Senior + ИИ', '+50…100%', 100, GREEN, 'знает, что спросить, и быстро ревьюит ответ'), ('Middle + ИИ', '0…+20%', 30, AMBER, 'эффект есть, но нестабильный'), ('Junior + ИИ', 'до −50%', 50, RED_T, 'копирует галлюцинации и часами отлаживает')]
    out = ''
    for nm, v, w, c, d in rows:
        neg = v.startswith('до −')
        bar = ('<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0; height: 12px;"><div style="display: flex; justify-content: flex-end; background: rgba(255,255,255,0.04); border-radius: 6px 0 0 6px;">' + ('<div style="width: ' + str(w) + '%; background: ' + c + '; border-radius: 6px 0 0 6px;"></div>' if neg else '') + '</div>'
               '<div style="background: rgba(255,255,255,0.04); border-left: 2px solid rgba(255,255,255,0.4); border-radius: 0 6px 6px 0;">' + ('' if neg else '<div style="width: ' + str(w) + '%; height: 100%; background: ' + c + '; border-radius: 0 6px 6px 0;"></div>') + '</div></div>')
        out += ('<div style="display: flex; flex-direction: column; gap: 6px; padding: 12px 0; border-top: 1px solid rgba(255,255,255,0.07);"><div style="display: flex; justify-content: space-between; gap: 12px;"><b style="font-size: 16px;">' + e(nm) + '</b><b style="color: ' + c + '; font-size: 18px; white-space: nowrap;">' + e(v) + '</b></div>' + bar
                + ('' if compact else '<div style="font-size: 13px; color: rgba(255,255,255,0.6);">' + e(d) + '</div>') + '</div>')
    return out

def ai_example():
    head = demo_head('ai', 'Лукьянов Александр · Backend, C#', 'ДЕМО UPCORE · ВКЛАДКА «ИИ-ЭФФЕКТИВНОСТЬ»', [
        ('MR через ИИ', '6 <span style="font-size: 16px; color: rgba(255,255,255,0.5);">из 47</span>', ''), ('Эффективность ИИ-MR', '<span style="color: ' + AMBER + ';">77%</span>', ''), ('UpCore / списано', '26,6 / 34,7 ч', '−8,1 ч')])
    left = '<div style="flex: 1.3 1 460px; min-width: 0;">' + ai_mr_rows() + '</div>'
    right = ('<div style="flex: 1 1 300px; min-width: 0; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; align-content: start;">'
             + tile('12', 'сессий с ИИ-агентом · 8,1 ч') + tile('121 тыс.', 'токенов на 1 MR при норме 250 тыс.') + tile('23 тыс.', 'токенов на час результата при норме 30 тыс.') + tile('<span style="color: ' + GREEN + ';">3</span> / <span style="color: ' + RED_T + ';">2</span>', 'MR, где ИИ ускорил / где замедлил') + '</div>')
    note = ('<div style="border-radius: 18px; background: rgba(155,140,255,0.08); border: 1px solid rgba(155,140,255,0.3); padding: 16px 20px; font-size: 15px; line-height: 1.55; color: rgba(255,255,255,0.86);">'
            'На трёх задачах ИИ дал результат быстрее, чем вручную. На двух — человек потратил с ИИ больше времени, чем заняла бы ручная работа. Без UpCore это выглядело бы одинаково: «задача закрыта».</div>')
    return example_shell('ai', 'ИИ-ЭФФЕКТИВНОСТЬ НА ПРИМЕРЕ', 'Сколько ИИ реально дал одному разработчику — по каждому MR', 'Профиль из демо UpCore: какие задачи сделаны с ИИ, сколько часов результата они дали и сколько токенов на это ушло.', head,
                         '<div style="display: flex; flex-wrap: wrap; gap: 24px 40px;">' + left + right + '</div>' + note)

def ai_deep():
    churn = ('<div><div style="display: flex; height: 18px; border-radius: 9px; overflow: hidden; gap: 3px;"><div style="flex: 50 1 0; background: #9B8CFF;"></div><div style="flex: 50 1 0; background: rgba(232,101,101,0.5);"></div></div>'
             '<div style="display: flex; justify-content: space-between; gap: 8px; font-size: 13px; color: rgba(255,255,255,0.66); margin-top: 8px;"><span><b style="color: #B9AEFF;">дошло до релиза</b></span><span><b style="color: ' + RED_T + ';">переписано</b></span></div></div>')
    items = [('ФАКТОР · АВТО-ДЕТЕКТ', 'Где в коде ИИ', hbar('MR с вайбкодингом по всей компании', '37 из 488', 8, '#B9AEFF', 'демо: сводный отчёт по компании'),
              'Определяем ИИ-код в каждом MR — по разработчику, команде и проекту. Не зависит от инструмента: смотрим на сам код.'),
             ('ФАКТОР · ПРОМПТ-КОЛЛЕКТОР', 'Как именно работали с ИИ', '<div class="g3" style="gap: 8px;">' + tile('7', 'сессий') + tile('70', 'ходов') + tile('604 тыс.', 'токенов') + '</div>',
              'Агент на машине разработчика собирает сессии, ходы и токены по каждому MR. Видно, где не хватило контекста и где ИИ увёл в сторону.'),
             ('ФАКТОР · РЕЗУЛЬТИРУЮЩИЙ КОД', 'Сколько ИИ-кода дошло до релиза', churn,
              'ИИ пишет быстрее, но если половину кода назавтра переписывают — эффекта нет. Считаем только результат, который остался в продукте.'),
             ('ФАКТОР · СТОИМОСТЬ', 'Сколько стоит час результата', '<div style="display: flex; flex-direction: column; gap: 10px;">' + hbar('Токенов на 1 MR', '121 / 250 тыс.', 48, GREEN) + hbar('Токенов на час результата', '23 / 30 тыс.', 77, AMBER) + '</div>',
              'Сравниваем расход токенов с нормой: где ИИ окупается, а где сжигает бюджет без пользы.')]
    return deep_block('ai', 'Разбираем подробно, как ИИ меняет вашу разработку', 'Та же мерка, что и для человека: часы результата, результирующий код и качество — плюс данные о самой работе с ИИ.', items)

def ai_smj_block():
    left = ('<div style="flex: 1 1 380px; min-width: 0; border-radius: 28px; background: #12111C; border: 1px solid rgba(155,140,255,0.35); padding: clamp(22px, 3vw, 36px);">'
            '<div style="' + MONO + ' font-size: 12px; color: #B9AEFF; margin-bottom: 8px;">ПРИРОСТ ЭФФЕКТИВНОСТИ С ИИ</div>' + ai_smj() + '</div>')
    right = ('<div style="flex: 1 1 380px; min-width: 0; border-radius: 28px; background: #1A1925; border: 1px solid rgba(255,255,255,0.08); padding: clamp(22px, 3vw, 36px); display: flex; flex-direction: column; gap: 16px;">'
             '<div style="' + MONO + ' font-size: 12px; color: #B9AEFF;">КЕЙС · ПРОЕКТНЫЙ ОФИС DEX, ВНЕДРЕНИЕ CLAUDE</div>'
             '<div style="display: flex; flex-wrap: wrap; gap: 16px 32px;"><div><div style="font-size: clamp(40px, 4vw, 56px); font-weight: 800; color: #B9AEFF; line-height: 1;">23%</div><div style="font-size: 14px; color: rgba(255,255,255,0.7);">MR уже пишутся с ИИ</div></div>'
             '<div><div style="font-size: clamp(40px, 4vw, 56px); font-weight: 800; color: ' + GREEN + '; line-height: 1;">+22 п.п.</div><div style="font-size: 14px; color: rgba(255,255,255,0.7);">эффективность MR с ИИ</div></div></div>'
             + hbar('MR с ИИ', '86%', 86, GREEN) + hbar('Средняя ручная эффективность команды', '64%', 64, 'rgba(255,255,255,0.45)') +
             '<p style="margin: 0; font-size: 15px; line-height: 1.55; color: rgba(255,255,255,0.78);">86% — это эффективность хорошего сеньора. Теперь видно, в чьих руках ИИ приносит прибыль, а в чьих — это дорогая игрушка.</p></div>')
    return section(sec_head('КОМУ ИИ ДАЁТ РЕЗУЛЬТАТ', 'Один инструмент — три разных результата', 'Один и тот же ИИ ускоряет сильных и тормозит новичков. UpCore показывает это по каждому человеку, чтобы бюджет на ИИ не делили «на всех поровну».', 'ai')
                   + '<div style="display: flex; flex-wrap: wrap; gap: 16px;">' + left + right + '</div>', 'smj')

AI_FAQ = [('С какими ИИ-инструментами работает?', 'Авто-детект смотрит на сам код — он не зависит от инструмента. Промпт-коллектор собирает сессии ИИ-агента на машине разработчика.'),
          ('Это не слежка за промптами?', 'Промпты разбираются для ревью и обучения: где теряется контекст и как получать результат быстрее. Доступ — по ролям, в on-premise всё остаётся у вас.'),
          ('Нужно ждать, пока накопится статистика?', 'Нет. История за полгода уже лежит в вашем Git — UpCore проанализирует её за час и сразу покажет картину «до» и «после» внедрения ИИ.'),
          ('Чем это отличается от отчёта вендора ИИ?', 'Вендор показывает использование своего продукта. UpCore показывает результат в коде — одинаково для любых инструментов и людей.')]
AI_ROLES = [('CTO', 'Видит, где ИИ ускоряет разработку, а где плодит переделки и техдолг, — по командам и проектам.'),
            ('CFO', 'Бюджет на лицензии и токены, который можно защитить: отдача в часах и рублях на каждый вложенный рубль.'),
            ('Тимлид', 'Понимает, кому из команды нужно обучение работе с ИИ, а кому — больше сложных задач.'),
            ('Разработчик', 'Видит, как работает с ИИ, и где теряет время на отладку сгенерированного кода.')]
AI_STATS = [('23%', 'MR уже пишутся с ИИ — проектный офис Dex'), ('+22 п.п.', 'эффективность MR с ИИ против ручных'), ('+50–100%', 'к эффективности у Senior с ИИ'), ('1 день', 'до первых результатов')]

# ------------------------------- Projects
TECHDEBT = [('Функциональная пригодность', 273, 13), ('Сопровождаемость', 227, 11), ('Гибкость', 157, 7), ('Надёжность', 39, 2), ('Совместимость', 29, 1), ('Защищённость', 11, 1), ('Производительность', 4, 0)]
TECHMAP = [('EF Metadata', 8, '87,3 ч', 81), ('Multithreading Advanced', 9, '21 ч', 90), ('java.nio', 8, '16,8 ч', 14), ('TypeScript Compiler API', 8, '11,9 ч', 0), ('Spring Security', 9, '23 мин', 0)]

def proj_summary():
    return ('<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px;">'
            + tile('<span style="color: ' + GREEN + ';">90%</span>', 'эффективность за месяц · 1,3 из 1,4 тыс. ч') + tile('88%', 'за 3 месяца · 2,9 из 3,3 тыс. ч')
            + tile('<span style="color: ' + AMBER + ';">35%</span>', 'найденной тяжести дефектов ушло в main') + tile('78%', 'мэтч команды с тех-картой проекта') + '</div>'
            '<div style="display: flex; flex-wrap: wrap; gap: 8px 18px; margin-top: 14px; font-size: 13px; color: rgba(255,255,255,0.66);"><span>сложность 8 / 10</span><span>1 год 7 мес</span><span>размер сильно больше среднего</span><span>легаси 0%</span></div>')

def techdebt_bars(n=7):
    return '<div style="display: flex; flex-direction: column; gap: 10px;">' + ''.join(hbar(a, str(b) + ' · ' + str(c) + '%', max(3, int(b / 273 * 100)), AMBER if i < 3 else 'rgba(242,193,78,0.5)') for i, (a, b, c) in enumerate(TECHDEBT[:n])) + '</div>'

def techmap_rows():
    head = '<div style="display: grid; grid-template-columns: minmax(0, 1fr) 44px 64px 52px; gap: 8px; ' + MONO + ' font-size: 12px; color: rgba(255,255,255,0.5); padding-bottom: 6px;"><span>ТЕХНОЛОГИЯ</span><span>СЛОЖН.</span><span>В КОДЕ</span><span style="text-align: right;">МЭТЧ</span></div>'
    return head + ''.join('<div style="display: grid; grid-template-columns: minmax(0, 1fr) 44px 64px 52px; gap: 8px; align-items: baseline; padding: 9px 0; border-top: 1px solid rgba(255,255,255,0.07); font-size: 14px;">'
                          '<span style="min-width: 0;">' + e(a) + '</span><span>' + str(b) + '</span><span style="white-space: nowrap;">' + e(c) + '</span><b style="text-align: right; color: ' + (GREEN if d >= 75 else (AMBER if d >= 30 else RED_T)) + ';">' + str(d) + '%</b></div>' for a, b, c, d in TECHMAP)

def act_vs_code():
    return ('<div style="display: flex; flex-direction: column; gap: 14px;">'
            '<div><div style="display: flex; justify-content: space-between; font-size: 14px; margin-bottom: 6px;"><span>Часов в акте подрядчика</span><b>160 ч</b></div><div style="height: 22px; border-radius: 8px; background: rgba(255,255,255,0.25);"></div></div>'
            '<div><div style="display: flex; justify-content: space-between; font-size: 14px; margin-bottom: 6px;"><span>Объективно по коду</span><b style="color: #F2C14E;">40 ч</b></div><div style="height: 22px; border-radius: 8px; background: rgba(255,255,255,0.06);"><div style="width: 25%; height: 100%; border-radius: 8px; background: #F2C14E;"></div></div></div>'
            '<div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 8px; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 14px;"><span style="font-size: 15px; color: rgba(255,255,255,0.8);">К оплате по факту кода</span><b style="font-size: 26px; color: ' + RED_T + ';">−120 ч · −75%</b></div></div>')

def proj_example():
    head = demo_head('projects', 'Проект «UpCore Backend»', 'ДЕМО UPCORE · МЕНЮ «ОТЧЁТЫ ПРОЕКТА» · ОКТЯБРЬ 2026', [
        ('Эффективность', '<span style="color: ' + GREEN + ';">90%</span>', 'за месяц · 88% за 3 месяца'), ('Сложность', '8 <span style="font-size: 16px; color: rgba(255,255,255,0.5);">/ 10</span>', 'размер сильно больше среднего'), ('Мэтч команды', '78%', 'с тех-картой проекта')])
    a = ('<div style="flex: 1 1 360px; min-width: 0;"><div style="' + MONO + ' font-size: 12px; color: #F2C14E; margin-bottom: 4px;">ТЕХДОЛГ ЗА МЕСЯЦ · ISO/IEC 25010</div>'
         '<div style="font-size: 15px; color: rgba(255,255,255,0.75); margin-bottom: 12px;"><b style="color: #FFFFFF;">35%</b> найденной ревью тяжести ушло в main — 750 из 2 147 баллов</div>' + techdebt_bars() + '</div>')
    b = ('<div style="flex: 1 1 360px; min-width: 0;"><div style="' + MONO + ' font-size: 12px; color: #F2C14E; margin-bottom: 12px;">ТЕХ-КАРТА ПРОЕКТА · SENIOR-ТЕХНОЛОГИИ</div>' + techmap_rows() +
         '<div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px;"><span style="font-size: 13px; padding: 8px 12px; border-radius: 10px; background: rgba(242,193,78,0.12); color: #F7D88A;">Сформировать вакансию</span><span style="font-size: 13px; padding: 8px 12px; border-radius: 10px; background: rgba(242,193,78,0.12); color: #F7D88A;">Подобрать специалиста</span></div></div>')
    return example_shell('projects', 'ПРОЕКТ НА ПРИМЕРЕ', 'Всё о проекте — в часах, рисках и технологиях', 'Отчёт проекта из демо UpCore: эффективность команды, техдолг по категориям качества и тех-карта с мэтчем команды.', head,
                         '<div style="display: flex; flex-wrap: wrap; gap: 32px 48px;">' + a + b + '</div>')

def proj_deep():
    items = [('ФАКТОР · ОБЪЕКТИВНАЯ СТОИМОСТЬ', 'Сколько стоит код на самом деле', act_vs_code(),
              'Трудоёмкость каждого MR складывается в объективную стоимость проекта в часах и рублях. Сверяйте её с актами, бюджетом и сроками.'),
             ('ФАКТОР · ТЕХДОЛГ', 'Сколько дефектов ушло в main', techdebt_bars(4),
              'ИИ-ревью находит дефекты, а UpCore считает, какая доля их тяжести ушла в main, — по категориям качества ISO/IEC 25010 и с динамикой.'),
             ('ФАКТОР · ТЕХ-КАРТА И МЭТЧ', 'Подходит ли команда проекту', '<div style="display: flex; flex-direction: column; gap: 10px;">' + hbar('Мэтч команды с тех-картой', '78%', 78, GREEN) + hbar('Senior-технологий в проекте', '1%', 3, AMBER) + hbar('Middle-технологий в проекте', '9%', 9, AMBER) + '</div>',
              'Какие технологии есть в коде и в каком объёме, насколько им соответствует команда. Пробелы закрываются вакансией или подбором специалиста.'),
             ('ФАКТОР · СЛОЖНОСТЬ И РИСКИ', 'Честное сравнение проектов', '<div class="g2" style="gap: 8px;">' + tile('8 / 10', 'сложность') + tile('0%', 'легаси') + tile('1 г. 7 мес', 'длительность') + tile('≫ среднего', 'размер') + '</div>',
              'Размер, сложность, доля легаси и прирост проекта учитываются в оценке — проекты и подрядчиков можно сравнивать между собой.')]
    return deep_block('projects', 'Разбираем подробно, из чего складывается картина проекта', 'Каждая цифра отчёта считается по коду и раскрывается до MR и строчек в «Глазе».', items)

def proj_audit():
    pts = ['Реальная эффективность каждого разработчика подрядчика в часах', 'Подтверждённый грейд и сложность задач', 'Чистая ценность результирующего кода — без шума и часов, потерянных при отладке', 'Техдолг и риски по категориям качества']
    left = ('<div style="flex: 1 1 380px; min-width: 0; border-radius: 28px; background: #12111C; border: 1px solid rgba(242,193,78,0.35); padding: clamp(22px, 3vw, 36px); display: flex; flex-direction: column; gap: 16px;">'
            '<div style="' + MONO + ' font-size: 12px; color: #F2C14E;">ПРИМЕР АУДИТА АКТА</div>' + act_vs_code() + '</div>')
    right = ('<div style="flex: 1.2 1 420px; min-width: 0; border-radius: 28px; background: #1A1925; border: 1px solid rgba(255,255,255,0.08); padding: clamp(22px, 3vw, 36px); display: flex; flex-direction: column; gap: 14px;">'
             '<div style="font-size: clamp(22px, 2vw, 28px); font-weight: 800; line-height: 1.2;">Вместе с актом — отчёт, который можно проверить</div>'
             '<ul style="margin: 0; padding-left: 20px; font-size: 16px; line-height: 1.55; color: rgba(255,255,255,0.84);">' + ''.join('<li style="margin-bottom: 8px;">' + e(x) + '</li>' for x in pts) + '</ul>'
             '<p style="margin: 0; font-size: 15px; line-height: 1.55; color: rgba(255,255,255,0.7);">Так Dex сам работает со своими клиентами на аутстаффе. Прогоним репозиторий вашего подрядчика через UpCore — и покажем объективную ценность его кода.</p></div>')
    return section(sec_head('КОНТРОЛЬ ПОДРЯДЧИКОВ', 'Акт на 1 500 часов? Проверьте его по коду', 'При оплате за часы у подрядчика нет стимула ускоряться. UpCore показывает, сколько трудоёмкости в коде на самом деле.', 'projects')
                   + '<div style="display: flex; flex-wrap: wrap; gap: 16px;">' + left + right + '</div>', 'audit')

PROJ_FAQ = [('А если подрядчик не даст доступ к коду?', 'Как правило, код по договору принадлежит заказчику. Анализ можно провести on-premise — полностью в вашем контуре, без доступа к интернету.'),
            ('Подходит для 1С и легаси?', 'Да: C#, Java, Go, Python, Kotlin, PHP, JS/TS, C++ и 1С. Доля легаси и сложность учитываются в оценке.'),
            ('Это заменит приёмку работ?', 'Нет — даст приёмке объективную основу: сколько трудоёмкости в коде на самом деле, а сколько в акте.'),
            ('Можно оценить проект при покупке компании?', 'Да. Разовый аудит покажет, сколько стоил код, сколько в нём техдолга и насколько команда соответствует технологиям.')]
PROJ_ROLES = [('CEO', 'Понимает, сколько на самом деле стоит продукт и за что компания платит подрядчикам.'),
              ('PMO', 'Рейтинг проектов, прогноз сроков и риски дедлайна — в одном окне, по коду, а не по статусам в Jira.'),
              ('CFO', 'Сверяет акты с объективной трудоёмкостью и находит переплаты до оплаты счёта.'),
              ('CTO', 'Видит техдолг, сложность и мэтч команды с технологиями каждого проекта.')]
PROJ_STATS = [('−75%', 'к оплате по акту — пример аудита'), ('50+', 'факторов в оценке каждого MR'), ('1 час', 'на анализ полугода истории проекта'), ('1 день', 'до первых результатов')]

# ------------------------------- Mentor
DEFECTS = [('Критические', 1, 1, RED_T), ('Высокие', 11, 13, '#F2A65E'), ('Средние', 35, 41, AMBER), ('Мелкие', 30, 35, 'rgba(255,255,255,0.5)'), ('Без уровня', 9, 10, 'rgba(255,255,255,0.3)')]

def defects_bars():
    return '<div style="display: flex; flex-direction: column; gap: 10px;">' + ''.join(hbar(a, str(b) + ' · ' + str(c) + '%', max(3, c * 2), col) for a, b, c, col in DEFECTS) + '</div>'

def quality_summary():
    return ('<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; margin-bottom: 16px;">'
            + tile('6,0 → <span style="color: ' + GREEN + ';">8,0</span>', 'качество кода до и после ревью') + tile('41 из 47', 'MR разобрано ИИ-ревью')
            + tile('86', 'дефектов найдено') + tile('30,9 ч', 'на исправления · 7% времени') + '</div>')

def review_queue():
    items = [('затронуто архитектурное ядро', RED_T), ('найдена логическая ошибка или уязвимость', RED_T), ('время сильно больше объективной сложности', AMBER), ('нетипичная технология или паттерн', AMBER)]
    rows = ''.join('<div style="display: flex; gap: 12px; align-items: center; padding: 11px 14px; border-radius: 12px; background: rgba(255,255,255,0.04); margin-bottom: 6px; font-size: 15px;"><span style="flex: 0 0 auto; width: 10px; height: 10px; border-radius: 50%; background: ' + c + ';"></span><span style="min-width: 0;">' + e(t) + '</span></div>' for t, c in items)
    return ('<div style="' + MONO + ' font-size: 12px; color: rgba(255,255,255,0.55); margin-bottom: 10px;">ТРЕБУЮТ ВНИМАНИЯ ЛИДА</div>' + rows +
            '<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; margin-top: 12px;">' + tile('<span style="color: ' + GREEN + ';">94%</span>', 'MR проверено авто-ревью · 457 из 488') + tile('15 мин', 'у лида на критичное вместо часов') + '</div>')

def ipr_card():
    top3 = [('Multithreading Advanced', 'сложность 9'), ('EF Advanced', 'сложность 8'), ('Spring Security', 'сложность 9')]
    return (hbar('Тех-метч с проектом', '60%', 60, GREEN, 'пример из поста канала: соответствие технологиям проекта') +
            '<div style="' + MONO + ' font-size: 12px; color: rgba(255,255,255,0.55); margin: 16px 0 10px;">ТОП-3 ТЕХНОЛОГИИ ДЛЯ РОСТА</div>'
            + ''.join('<div style="display: flex; justify-content: space-between; gap: 12px; padding: 11px 14px; border-radius: 12px; background: rgba(83,192,77,0.08); border: 1px solid rgba(83,192,77,0.25); margin-bottom: 6px; font-size: 15px;"><span><b style="color: #7FDB7A;">' + str(i + 1) + '.</b> ' + e(a) + '</span><span style="color: rgba(255,255,255,0.6); white-space: nowrap;">' + e(b) + '</span></div>' for i, (a, b) in enumerate(top3))
            + '<div style="font-size: 13px; color: rgba(255,255,255,0.6); margin-top: 8px;">технологии, которых больше всего в проекте, но которые человек ещё не знает</div>')

def mentor_example():
    head = demo_head('mentor', 'Лукьянов Александр · Backend, C#', 'ДЕМО UPCORE · ВКЛАДКА «КАЧЕСТВО» · АНАЛИЗ КОД-РЕВЬЮ', [
        ('Качество кода', '6,0 → <span style="color: ' + GREEN + ';">8,0</span>', 'до и после ревью'), ('MR разобрано', '41 <span style="font-size: 16px; color: rgba(255,255,255,0.5);">из 47</span>', '38 с дефектами'), ('На исправления', '30,9 ч', '7% времени UpCore')])
    iso = [('Функциональная пригодность', '0/9/16/6'), ('Сопровождаемость', '0/0/5/19'), ('Гибкость', '1/1/7/2'), ('Совместимость', '0/0/3/1'), ('Надёжность', '0/0/3/1')]
    isoh = ('<div style="' + MONO + ' font-size: 12px; color: #7FDB7A; margin-bottom: 10px;">ДЕФЕКТЫ ПО БЛОКАМ ISO 25010 · К / В / С / М</div>'
            + ''.join('<div style="display: flex; justify-content: space-between; gap: 12px; padding: 9px 0; border-top: 1px solid rgba(255,255,255,0.07); font-size: 14px;"><span>' + e(a) + '</span><b style="white-space: nowrap; font-variant-numeric: tabular-nums;">' + b + '</b></div>' for a, b in iso))
    body = ('<div style="display: flex; flex-wrap: wrap; gap: 32px 48px;"><div style="flex: 1 1 340px; min-width: 0;"><div style="' + MONO + ' font-size: 12px; color: #7FDB7A; margin-bottom: 12px;">86 ДЕФЕКТОВ ПО ТЯЖЕСТИ</div>' + defects_bars() + '</div>'
            '<div style="flex: 1 1 340px; min-width: 0;">' + isoh + '</div></div>'
            '<div style="border-radius: 18px; background: rgba(83,192,77,0.08); border: 1px solid rgba(83,192,77,0.3); padding: 16px 20px; font-size: 15px; line-height: 1.55; color: rgba(255,255,255,0.86);">'
            'Из системных ошибок Mentor собирает персональный план: что исправить в коде, как ставить задачи и писать промпты, какие технологии прокачать для следующего грейда.</div>')
    return example_shell('mentor', 'НАСТАВНИК НА ПРИМЕРЕ', 'Каждый MR разобран — и превращён в план роста', 'Профиль из демо UpCore: ИИ-ревью нашло дефекты по тяжести и категориям качества, после исправлений качество кода выросло с 6,0 до 8,0.', head, body)

def mentor_deep():
    items = [('ФАКТОР · ИИ-РЕВЬЮ КОДА', 'Ревью каждого MR, а не 5–10%', quality_summary().replace('margin-bottom: 16px;', ''),
              'ИИ-агент разбирает каждый MR: дефекты по тяжести и категориям ISO 25010, что ушло в main и сколько времени заняли исправления.'),
             ('ФАКТОР · ЗАДАЧИ И ПРОМПТЫ', 'Ревью постановок и работы с ИИ', '<div class="g3" style="gap: 8px;">' + tile('задачи', 'полнота постановки') + tile('промпты', 'контекст и ход сессии') + tile('ИИ-код', 'что дошло до релиза') + '</div>',
              'Разбираем постановки задач и промпты: где не хватило контекста и где ИИ увёл в сторону. Цель — расти вместе с ИИ, а не отдавать ему работу вместо себя.'),
             ('ФАКТОР · ПЛАН РОСТА', 'ИПР по тех-метчу — точечно', ipr_card(),
              'Накладываем цифровое резюме разработчика на тех-карту проекта и вычисляем Топ-3 технологии, которые дадут максимальный рост эффективности прямо сейчас.'),
             ('ФАКТОР · ПРИОРИТИЗАЦИЯ РЕВЬЮ', 'Лиду — только критичное', review_queue(),
              'Система подсвечивает MR, которым нужен человек. Остальное ревьюит цифровой тимлид — лид тратит 15 минут вместо часов.')]
    return deep_block('mentor', 'Разбираем подробно, как работает цифровое менторство', 'Mentor видит всю историю разработчика — задачи, промпты, код и оценки — и превращает её в конкретные шаги роста.', items)

MENTOR_FAQ = [('Чем Mentor отличается от ИИ-ревьюера кода?', 'Ревьюер смотрит один MR. Mentor видит всю историю разработчика — задачи, промпты, код и оценки — и превращает системные ошибки в план роста.'),
              ('Mentor заменит тимлида?', 'Нет. Он снимает рутину — ревью всего подряд и разбор типовых ошибок, — чтобы тимлид тратил время на архитектуру и людей.'),
              ('Это не очередной контроль?', 'Рекомендации видит сам разработчик, и они про рост, а не про наказание. Цифровой тимлид из контролёра становится наставником.'),
              ('Как Mentor учит работать с ИИ?', 'Разбирает промпты и решения: где не хватило контекста, где ИИ увёл в сторону. Цель — чтобы разработчик рос вместе с ИИ, а не вместо себя отдавал ему работу.')]
MENTOR_ROLES = [('Тимлид', 'Не ревьюит всё подряд: тратит 15 минут на критичные MR, остальное разбирает цифровой тимлид.'),
                ('L&D', 'Персональные планы развития по фактам из кода, а не по анкетам — и видно, как они работают.'),
                ('Разработчик', 'Получает разбор каждого MR и понятный путь к следующему грейду — без страха и оценок «на глаз».'),
                ('CTO', 'Качество кода растёт, новички быстрее выходят на эффективность, сеньоры возвращаются к архитектуре.')]
MENTOR_STATS = [('94%', 'MR проверено авто-ревью'), ('114 ч', 'ручного ревью в месяц экономии'), ('6,0 → 8,0', 'качество кода после ревью'), ('1 день', 'до первых результатов')]

def module_page(key, n):
    mod = MODC[key][0]
    if key == 'ai':
        heroes = {1: ('Реальная эффективность внедрения ИИ в вашу разработку', 'Авто-детект ИИ-кода и промпт-коллектор показывают, сколько часов ИИ на самом деле экономит каждому разработчику, где он плодит переделки и окупается ли каждый рубль на лицензии и токены.',
                      image_console('efficiency', 'ai / эффективность', 'Эффективность специалиста', 'создано через ИИ — в часах и рублях', 'ai')),
                  2: ('Сколько часов на самом деле экономит ИИ — по каждому MR', 'UpCore сравнивает время, за которое задача решается вручную, с реальными часами работы с ИИ. По каждому разработчику, команде и инструменту.',
                      panel('ai', 'ai / mr с ии', 'демо', ai_mr_rows(short=True))),
                  3: ('Senior с ИИ: +50–100%. Junior: до −50%. Узнайте, где ИИ окупается', 'Один и тот же ИИ ускоряет одних и тормозит других. UpCore показывает, кому ИИ даёт результат, кому — переделки и техдолг, и сколько стоит каждый токен.',
                      panel('ai', 'ai / кому ии даёт результат', 'кейс Dex', ai_smj()))}
        blocks = {1: [ai_example(), ai_deep(), ai_smj_block()], 2: [ai_smj_block(), ai_deep(), ai_example()], 3: [ai_example(), ai_deep()]}[n]
        st, roles_, faq_, cta_ = AI_STATS, AI_ROLES, AI_FAQ, ('Посчитайте реальный эффект ИИ в своей команде', 'Подключите репозиторий — сравним время «с ИИ» и «вручную» по истории вашего кода.')
    elif key == 'projects':
        heroes = {1: ('Сколько на самом деле стоит проект? Посчитаем по коду', 'Объективная стоимость разработки в часах и рублях, эффективность команды и подрядчиков, техдолг и тех-карта — по каждому MR. Разовый аудит — без внедрения.',
                      panel('projects', 'projects / upcore backend', 'демо', proj_summary())),
                  2: ('В акте 160 часов. В коде — 40. Проверьте подрядчика по коду', 'UpCore считает объективную трудоёмкость каждого MR и сверяет её с актами. Переплата видна до оплаты счёта — по каждому разработчику подрядчика.',
                      panel('projects', 'projects / аудит акта', 'пример', act_vs_code())),
                  3: ('Бюджет проекта и контроль подрядчиков — в часах и рублях', 'Эффективность команды, техдолг по категориям качества, тех-карта и мэтч команды, прогноз сроков — всё по коду, а не по статусам в Jira.',
                      panel('projects', 'projects / техдолг', 'демо', '<div style="font-size: 15px; color: rgba(255,255,255,0.75); margin-bottom: 12px;"><b style="color: #FFFFFF;">35%</b> найденной тяжести ушло в main</div>' + techdebt_bars()))}
        blocks = {1: [proj_example(), proj_deep(), scenarios()], 2: [proj_audit(), proj_example(), proj_deep()], 3: [proj_example(), proj_deep(), proj_audit()]}[n]
        st, roles_, faq_, cta_ = PROJ_STATS, PROJ_ROLES, PROJ_FAQ, ('Проверьте, сколько на самом деле стоит ваш проект', 'Закажите аудит — объективный бюджет проекта по коду: полгода истории за 1 час.')
    else:
        heroes = {1: ('ИИ-наставник для каждого разработчика', 'Mentor разбирает каждый MR, постановки задач и промпты, находит, где проседает эффективность, и собирает персональный план роста. Сеньоры возвращаются к архитектуре.',
                      panel('mentor', 'mentor / качество', 'демо', quality_summary() + defects_bars())),
                  2: ('Тимлид успевает менторить троих. UpCore.Mentor — всю команду', 'Ревью каждого MR, разбор системных ошибок и план роста — автоматически, каждый день. Лид тратит 15 минут на критичное, а не часы на всё подряд.',
                      panel('mentor', 'mentor / приоритизация ревью', 'онлайн', review_queue())),
                  3: ('Из оценки — в план роста: у каждого разработчика свой ИИ-наставник', 'UpCore превращает слабые факторы грейда и тех-метч в конкретные шаги: что исправить в коде, как работать с ИИ и какие технологии прокачать.',
                      panel('mentor', 'mentor / план роста', 'ИПР', ipr_card()))}
        blocks = {1: [mentor_example(), mentor_deep()], 2: [mentor_deep(), mentor_example()], 3: [mentor_example(), mentor_deep()]}[n]
        st, roles_, faq_, cta_ = MENTOR_STATS, MENTOR_ROLES, MENTOR_FAQ, ('Дайте каждому разработчику своего наставника', 'Подключите репозиторий — первые рекомендации по истории MR вашей команды за 1 день.')
    h1, sub, vis = heroes[n]
    primary = ('Заказать аудит', MAIL) if (key == 'projects' and n == 2) else ('Подключить UpCore', REG)
    body = [header(key), mod_hero(key, h1, sub, vis, st)] + blocks + [
        roles('ДЛЯ КОГО', {'ai': 'Одни данные об ИИ для CTO, финансов, тимлида и разработчика', 'projects': 'Прозрачность, выгодная заказчику и команде', 'mentor': 'Наставник, который нужен каждому в команде'}[key], roles_, key),
        faq(faq_, acc_key=key), saas_variant(2), cta(cta_[0], cta_[1], primary), footer()]
    return page('UpCore %s — макет %d' % (mod, n), '\n'.join(body), 6000, name='%s-%d' % (mod, n))

# ------------------------------- Блог
TG_URL = 'https://t.me/upcore_ai'
BLOG = [  # 7 самых популярных постов канала по просмотрам (без оффтопа: №15, №26, №42)
    (25, '25 августа 2026', 294, 'Интервью', 'Большое интервью про UpCore для Александра Поломодова, CTO Т-Банка', 'Почти 2 часа неудобных и правильных вопросов: как измерить вайбкодинг, как защититься от «хакинга» метрик, не приведёт ли машинная оценка к увольнению полезных людей и почему мы отказались от LLM в ядре оценки.'),
    (22, '24 августа 2026', 236, 'Деньги', 'Сколько на самом деле стоит код?', 'UpCore переводит код в реально затраченное на задачу время. Из 160 часов в месяц результата на 80 — эффективность 50%, а потери — 80 часов, умноженные на ставку.'),
    (27, '26 августа 2026', 236, 'ИИ', 'Как измерить эффективность ИИ в разработке?', 'Кейс проектного офиса Dex с Claude: 23% MR пишутся с ИИ, их эффективность 86% против 64% вручную. Senior + ИИ — до +100%, Junior + ИИ — до −50%.'),
    (20, '23 августа 2026', 212, 'Методика', 'Про математику и точность', 'Как UpCore работает «под капотом»: 50+ факторов в каждой задаче, статистика на сотне задач подряд и детерминированная математика вместо LLM.'),
    (41, '22 сентября 2026', 204, 'Менторство', 'Как UpCore превращает код в индивидуальный план обучения', 'Тех-карта проекта, автоматическое резюме по коммитам и тех-метч — и Топ-3 технологии, которые дадут максимальный рост прямо сейчас.'),
    (28, '27 августа 2026', 192, 'Методика', 'Code Churn: кто съедает ваш ФОТ и как с этим бороться?', 'Один инженер пишет чуть медленнее, но сохраняет 90% кода. Второй печатает как пулемёт, но 50% его работы уходит в корзину вместе с деньгами бизнеса.'),
    (35, '4 сентября 2026', 177, 'Деньги', 'Правило 20%: кто на самом деле сжигает ваш ФОТ?', '20% неэффективных сотрудников дают всего 4% результата. В командах от 50 человек найти их интуитивно невозможно — в Jira у всех закрываются задачи.'),
]
TAGC = {'Интервью': '#63D5FF', 'Деньги': '#F2C14E', 'ИИ': '#B9AEFF', 'Методика': '#63D5FF', 'Менторство': '#7FDB7A'}

def tg_icon(size=28, col='#FFFFFF'):
    return '<svg aria-hidden="true" viewBox="0 0 24 24" width="%d" height="%d" fill="%s" style="flex: 0 0 auto; display: block;"><path d="M21.9 4.3 18.7 19.4c-.2 1-.9 1.3-1.8.8l-4.9-3.6-2.4 2.3c-.3.3-.5.5-1 .5l.3-5 9.1-8.2c.4-.4-.1-.6-.6-.2L6.2 13 1.4 11.5c-1-.3-1.1-1 .2-1.5L20.6 2.9c.9-.3 1.6.2 1.3 1.4z"/></svg>' % (size, size, col)

def tg_banner(compact=False):
    return ('<div style="border-radius: 32px; background: linear-gradient(135deg, rgba(99,213,255,0.16), #12111C 60%); border: 1px solid rgba(99,213,255,0.4); padding: clamp(24px, 3.4vw, 44px); display: flex; flex-wrap: wrap; gap: 24px 40px; align-items: center; justify-content: space-between;">'
            '<div style="display: flex; gap: 20px; align-items: center; flex: 1 1 420px; min-width: 0;"><div style="flex: 0 0 auto; width: 72px; height: 72px; border-radius: 22px; background: #63D5FF; display: flex; align-items: center; justify-content: center;">' + tg_icon(36, '#0D0C15') + '</div>'
            '<div style="min-width: 0;"><div style="' + MONO + ' font-size: 13px; color: #63D5FF;">TELEGRAM · @UPCORE_AI</div><div style="font-size: clamp(24px, 2.4vw, 34px); font-weight: 800; line-height: 1.15; margin-top: 4px;">ИИ-тимлид UpCore</div>'
            + ('' if compact else '<p style="margin: 8px 0 0; font-size: 16px; line-height: 1.55; color: rgba(255,255,255,0.78); max-width: 620px;">Канал об эффективности разработки от основателя Dex Ивана Геля: как работает цифровой тимлид, как измерять ИИ в разработке и переводить код в деньги. Дневник продукта и разборы реальных кейсов.</p>') + '</div></div>'
            + btn('Подписаться на канал', TG_URL) + '</div>')

def post_card(p, big=False):
    pid, date, views, tag, title, ex = p
    col = TAGC.get(tag, '#63D5FF')
    return ('<article style="min-width: 0; border-radius: 28px; background: #1A1925; border: 1px solid rgba(255,255,255,0.08); padding: ' + ('clamp(26px, 3.4vw, 44px)' if big else 'clamp(22px, 2.6vw, 30px)') + '; display: flex; flex-direction: column; gap: 14px;">'
            '<div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 8px; ' + MONO + ' font-size: 12px; color: rgba(255,255,255,0.55);"><span style="color: ' + col + ';">' + e(tag).upper() + '</span><span>' + e(date) + ' · ' + str(views) + ' просмотров</span></div>'
            '<div style="font-size: ' + ('clamp(26px, 2.8vw, 40px)' if big else '22px') + '; font-weight: 800; line-height: 1.2; letter-spacing: -0.01em;">' + e(title) + '</div>'
            '<p style="margin: 0; color: rgba(255,255,255,0.76); font-size: ' + ('17px' if big else '15px') + '; line-height: 1.6;">' + e(ex) + '</p>'
            '<a href="' + TG_URL + '/' + str(pid) + '" style="margin-top: auto; display: inline-flex; align-items: center; gap: 8px; min-height: 44px; font-weight: 600; text-decoration: none; color: ' + col + ';">Читать в Telegram →</a></article>')

def post_row(p, i):
    pid, date, views, tag, title, ex = p
    col = TAGC.get(tag, '#63D5FF')
    return ('<a href="' + TG_URL + '/' + str(pid) + '" style="display: grid; grid-template-columns: 64px minmax(0, 1fr); gap: 20px; padding: 24px 0; border-top: 1px solid rgba(255,255,255,0.08); text-decoration: none; color: #FFFFFF;">'
            '<div style="font-size: 40px; font-weight: 800; color: rgba(255,255,255,0.2); line-height: 1;">' + '%02d' % i + '</div>'
            '<div style="min-width: 0; display: flex; flex-direction: column; gap: 8px;"><div style="display: flex; flex-wrap: wrap; gap: 8px 16px; ' + MONO + ' font-size: 12px; color: rgba(255,255,255,0.55);"><span style="color: ' + col + ';">' + e(tag).upper() + '</span><span>' + e(date) + '</span><span>' + str(views) + ' просмотров</span></div>'
            '<div style="font-size: clamp(20px, 1.9vw, 26px); font-weight: 800; line-height: 1.25;">' + e(title) + '</div><p style="margin: 0; color: rgba(255,255,255,0.72); font-size: 15px; line-height: 1.55;">' + e(ex) + '</p></div></a>')

def blog_hero(h1, sub, right=''):
    return ('<section id="top" style="position: relative; max-width: 1280px; margin: 0 auto; padding: 40px 32px 64px; display: flex; flex-wrap: wrap; gap: 40px; align-items: flex-end; justify-content: space-between;">' + CHEVRON +
            '<div style="flex: 1 1 560px; min-width: 0; position: relative; display: flex; flex-direction: column; gap: 18px;"><div style="' + MONO + ' font-size: 13px; color: #63D5FF;">БЛОГ UPCORE</div>'
            '<h1 style="margin: 0; font-size: clamp(36px, 4.2vw, 60px); line-height: 1.04; letter-spacing: -0.03em; font-weight: 800;">' + h1 + '</h1>'
            '<p style="margin: 0; font-size: clamp(17px, 1.35vw, 20px); line-height: 1.55; color: rgba(255,255,255,0.8); max-width: 640px;">' + e(sub) + '</p></div>' + right + '</section>')

def blog_page(n):
    chips = '<div style="display: flex; flex-wrap: wrap; gap: 8px;">' + ''.join('<span style="font-size: 14px; padding: 8px 14px; border-radius: 12px; border: 1px solid ' + ('#63D5FF' if i == 0 else 'rgba(255,255,255,0.14)') + '; background: ' + ('rgba(99,213,255,0.12)' if i == 0 else 'transparent') + '; color: #FFFFFF;">' + e(x) + '</span>' for i, x in enumerate(['Все', 'Методика', 'ИИ', 'Деньги', 'Менторство', 'Интервью'])) + '</div>'
    if n == 1:  # баннер канала → главный пост крупно → сетка 6
        top = blog_hero('Код — лучший отчёт. Разбираем, как это работает', 'Самые читаемые посты Telegram-канала UpCore: методика оценки, эффективность ИИ, деньги и цифровое менторство.')
        body = [section(tg_banner(), pb=48), section('<div style="' + MONO + ' font-size: 13px; color: rgba(255,255,255,0.55); margin-bottom: 14px;">САМОЕ ПОПУЛЯРНОЕ</div>' + post_card(BLOG[0], big=True) + '<div class="g3" style="margin-top: 16px;">' + ''.join(post_card(p) for p in BLOG[1:]) + '</div>', 'posts')]
    elif n == 2:  # журнал: список-рейтинг слева, канал справа
        side = ('<aside style="flex: 1 1 320px; min-width: 0; display: flex; flex-direction: column; gap: 16px;">'
                '<div style="border-radius: 28px; background: #12111C; border: 1px solid rgba(99,213,255,0.4); padding: 28px; display: flex; flex-direction: column; gap: 14px;">'
                '<div style="width: 56px; height: 56px; border-radius: 18px; background: #63D5FF; display: flex; align-items: center; justify-content: center;">' + tg_icon(28, '#0D0C15') + '</div>'
                '<div style="font-size: 24px; font-weight: 800;">ИИ-тимлид UpCore</div><p style="margin: 0; font-size: 15px; line-height: 1.55; color: rgba(255,255,255,0.75);">Канал основателя Dex Ивана Геля: дневник продукта, разборы кейсов и цифры об ИИ в разработке.</p>'
                + btn('Подписаться', TG_URL) + '</div>'
                '<div style="border-radius: 28px; background: #1A1925; border: 1px solid rgba(255,255,255,0.08); padding: 24px;"><div style="' + MONO + ' font-size: 12px; color: rgba(255,255,255,0.55); margin-bottom: 12px;">ТЕМЫ</div>' + chips + '</div></aside>')
        lst = '<div style="flex: 2 1 560px; min-width: 0;"><div style="' + MONO + ' font-size: 13px; color: rgba(255,255,255,0.55); margin-bottom: 4px;">ТОП-7 ПОСТОВ ПО ПРОСМОТРАМ</div>' + ''.join(post_row(p, i + 1) for i, p in enumerate(BLOG)) + '</div>'
        top = blog_hero('Блог UpCore: самое читаемое из канала', 'Методика, ИИ в разработке и деньги — короткие разборы от команды, которая сама считает эффективность 1500+ разработчиков.')
        body = [section('<div style="display: flex; flex-wrap: wrap; gap: 32px 48px; align-items: flex-start;">' + lst + side + '</div>', 'posts')]
    else:  # фильтры тем → карточки 2 колонки → большой CTA канала внизу
        right = '<div style="flex: 0 1 auto; position: relative;">' + btn('Подписаться в Telegram', TG_URL) + '</div>'
        top = blog_hero('Об эффективности разработки — без воды', 'Самые популярные посты канала «ИИ-тимлид UpCore»: как работает цифровой тимлид и что он находит в коде.', right)
        body = [section('<div style="margin-bottom: 20px;">' + chips + '</div><div class="g2">' + ''.join(post_card(p) for p in BLOG[:6]) + '</div>', 'posts'), section(tg_banner(), pb=72)]
    page_body = [header('blog'), top] + body + [cta('Посмотрите на свою команду глазами цифрового тимлида', 'Подключите репозиторий — первые результаты за 1 день.', ('Подключить UpCore', REG)), footer()]
    return page('UpCore — блог, макет %d' % n, '\n'.join(page_body), 3000, name='Blog-%d' % n)


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
    # раунд 34: блок «SaaS и безопасность» (вариант 2) зафиксирован на Главной A, Sec-1/2 сняты
    for n in (1, 2, 3):  # раунд 30: три полных макета страницы Grade; раунд 31 — на холсте остаётся только Grade-3
        files['Grade-%d' % n] = grade_page(n)
    # (функции core_board / pains_board оставлены, чтобы можно было снова вывести варианты)
    for k, n in (('grade', 'Grade'), ('ai', 'AI'), ('projects', 'Projects'), ('mentor', 'Mentor')):
        for v in 'ABC':
            files['%s-%s' % (n, v)] = product(k, v)
    for k, nm in (('ai', 'AI'), ('projects', 'Projects'), ('mentor', 'Mentor')):  # раунд 36: по 3 полных макета
        for n in (1, 2, 3):
            files['%s-%d' % (nm, n)] = module_page(k, n)
    for n in (1, 2, 3):
        files['Blog-%d' % n] = blog_page(n)
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
