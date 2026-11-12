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
.g2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}
.g3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.g4{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
@media (max-width:1100px){.g3,.g4{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:720px){.g2,.g3,.g4{grid-template-columns:minmax(0,1fr)}}
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
        col = '#63D5FF' if i == 0 else '#FFFFFF'
        cells.append('<div style="flex: 1 1 130px; padding-right: 16px; min-width: 0;"><div style="font-size: 34px; font-weight: 800; color: %s; letter-spacing: -0.02em; line-height: 1.1;">%s</div>'
                     '<div style="font-size: 14px; color: rgba(255,255,255,0.7); line-height: 1.4; margin-top: 4px;">%s</div></div>' % (col, e(big), e(small)))
    out = '<div style="display: flex; flex-wrap: wrap; row-gap: 16px; border-top: 1px solid rgba(255,255,255,0.12); padding-top: 24px;">%s</div>' % ''.join(cells)
    if note:
        out += '<div style="%s font-size: 12px; color: rgba(255,255,255,0.55); margin-top: -12px;">%s</div>' % (MONO, e(note))
    return out

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

SEC_CARDS = [
    ('Вход через GitHub или GitLab', 'Подключите репозиторий — и получите первые оценки по истории проекта. Код, написанный за год, анализируется за несколько минут.'),
    ('Код не покидает ваш контур', 'Локальный агент анализирует код на вашей стороне. На сервер уходят только метрики — исходники никуда не передаются.'),
    ('On-premise без интернета', 'Полностью в вашей инфраструктуре, в закрытом контуре. Нужен только read-only доступ к Git. GPU не нужны.'),
    ('Права и конфиденциальность', 'Гибкие роли, вход через SSO и режим «скрыть чувствительные данные»: зарплаты и рейтинги видят только те, кому положено.'),
    ('Любой стек', 'C#, Java, Go, Python, Kotlin, PHP, JS/TS, C++ и 1С. Интеграции с GitLab, GitHub и Jira.'),
    ('Платите за подтверждённый результат', 'Бесплатный пилот на 2–3 ваших проектах. Оплата — только после того, как вы подтвердите точность на своих данных.'),
]

def security(full=True, h2='Подключение за минуты. Код остаётся у вас.'):
    items = SEC_CARDS if full else [SEC_CARDS[1], SEC_CARDS[2], SEC_CARDS[5]]
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

def products_2x2():
    items = [
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
    cards = []
    for key, lab, q, t, p, lis, more in items:
        line, txt = ACC[key]
        ul = ''.join('<li>%s</li>' % e(x) for x in lis)
        cards.append('<article id="%s" style="min-width: 0; border-radius: 28px; background: #1A1925; border: 1px solid rgba(255,255,255,0.08); padding: clamp(24px, 3vw, 40px); display: flex; flex-direction: column; gap: 16px;">'
                     '<div style="%s font-size: 13px; color: %s;">%s</div>'
                     '<div style="font-size: 17px; color: rgba(255,255,255,0.62); font-style: italic;">%s</div>'
                     '<h3 style="margin: 0; font-size: clamp(26px, 2.3vw, 34px); letter-spacing: -0.02em; line-height: 1.1;">%s</h3>'
                     '<p style="margin: 0; color: rgba(255,255,255,0.78); line-height: 1.55; font-size: 17px;">%s</p>'
                     '<ul style="margin: 0; padding-left: 20px; color: rgba(255,255,255,0.86); font-size: 16px; line-height: 1.8;">%s</ul>'
                     '<a href="#%s-page" style="margin-top: auto; font-weight: 600; text-decoration: none; min-height: 44px; display: inline-flex; align-items: center; color: %s;">%s</a></article>' % (
                         key, MONO, txt, e(lab), e(q), e(t), e(p), ul, key, txt, e(more)))
    return section(sec_head('ПЛАТФОРМА UPCORE', 'Одна платформа. Четыре ответа для бизнеса.', 'Подключите репозиторий один раз — и получите оценки по каждому направлению: люди, ИИ, проекты и рост команды.') +
                   '<div class="g2">%s</div>' % ''.join(cards), 'products')

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
        'A': dict(h1='Цифровой тимлид, который проверяет [[100%]] кода вашей команды',
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
    body = [header(None), hero('цифровой тимлид · онлайн', hv['h1'], hv['sub'], [btn('Подключить репозиторий', REG), btn('Заказать аудит', MAIL, False)], hv['st'], visual, hv['note'])]
    if variant != 'A':
        return page('UpCore — главная, первый экран ' + variant, '\n'.join(body), 1000, slider=True, name='Home-' + variant)
    body += [
        text_pains('ПОЧЕМУ ЭТО ВАЖНО', 'Разработка — самая дорогая статья расходов. И самая непрозрачная.', [
            ('Jira зелёная, а релиз снова переносится', 'Статусы, дейлики и отчёты показывают активность, а не результат в коде. Почему сорваны сроки, объяснить никто не может.', None),
            ('20% команды дают 4% результата', 'Неэффективность прячется в «средней температуре по больнице». Без данных её не видно — а зарплату вы платите полностью.', 'данные UpCore'),
            ('Тимлид видит 5–10% кода', 'Остальное принимается на доверии. С приходом ИИ кода стало в разы больше, а ревьюеров — нет.', None),
            ('ИИ куплен. Окупился?', 'Эффект ИИ-инструментов измеряют лишь 18% компаний. Остальные платят за лицензии и токены вслепую.', 'LeadDev AI Impact Report, 2025'),
        ]),
        products_2x2(),
        compare('ПРИНЦИП', 'Не тайм-трекер. Не слежка. Не KPI по строкам кода.', 'Мы не считаем', [
            'время в IDE, клики и скриншоты', 'активность в мессенджерах и на дейликах', 'строки кода, коммиты и закрытые тикеты — их легко накрутить, особенно с ИИ'],
            'Мы считаем', ['объективную трудоёмкость каждого MR в часах', 'вес кода по архитектуре: 50 строк в ядре дороже 1000 строк формочек', 'результирующий код: что осталось в продукте, а что переписано',
                           'без шума: копипаст, автогенерация и ренеймы отсеиваются'],
            'Больше кода — не значит больше ценности. UpCore оценивает только результат, который остался в продукте.'),
        method_block('Как цифровой тимлид превращает код в часы, грейд и деньги', [
            ('ВХОД', 'Код и история', 'MR и коммиты из GitLab или GitHub, ворклоги Jira, сессии ИИ-агента. История за 3–6 месяцев — результат в первый же день.'),
            ('АНАЛИЗ', '50+ факторов', 'AST-граф проекта: ядро и периферия; цикломатическая, когнитивная и технологическая сложность; результирующий код; отсев шума.'),
            ('МОДЕЛЬ', 'Детерминированная математика', 'Модели откалиброваны под каждый стек на экспертных оценках. Не «галлюцинирует» и не требует GPU. Поверх — ИИ-агенты для ревью и наставничества.'),
            ('РЕЗУЛЬТАТ', 'Решения для бизнеса', 'Эффективность в часах и рублях, грейд, рейтинг, ROI от ИИ, бюджет проекта и план развития.')],
            '96%', 'от экспертной оценки', [
                'Модель обучена повторять оценку опытных тимлидов. Даже два сильных лида расходятся: один оценит задачу в 4 часа, другой — в 8. UpCore даёт одну шкалу для всех.',
                'Оценка строится по 100+ задачам подряд — на дистанции статистика сглаживает аномалии. «Глаз» показывает расчёт до строчки кода, а сотрудник может подать апелляцию.',
                'Модели проверены на 1500+ разработчиках и сотнях проектов.'],
            'Тот же принцип — модель, обученная на оценках экспертов, — исследователи Стэнфорда применили к 100 000+ разработчиков (корреляция с экспертами 0,82–0,86).'),
        kpi('ЭФФЕКТ ДЛЯ БИЗНЕСА', 'Что получает бизнес — в цифрах', [
            ('+14%', 'к эффективности разработки в среднем за 3 месяца после внедрения', 'замер 3 мес. до и 3 мес. после'),
            ('≈500 тыс. ₽', 'ценности в год на каждого разработчика — +14% при затратах 300 тыс. ₽ в месяц на человека', 'расчёт UpCore'),
            ('+12%', 'производительности сразу — как бесплатно нанять 12 мидлов на каждые 100 разработчиков', 'данные UpCore'),
            ('20% → 4%', 'находим 20% команды, которые дают лишь 4% результата, — и «звёздочек» для сложных задач', 'данные UpCore'),
            ('2,5 ставки', 'тимлидов освобождается на каждые 100 разработчиков: оценка и ревью идут автоматически', '~4 ч в месяц на человека'),
            ('114 ч', 'ручного ревью в месяц экономит авто-ревью: проверено 94% MR, +228 тыс. ₽', 'демо-компания, 488 MR в месяц'),
            ('−75%', 'к оплате в примере аудита акта подрядчика: 160 ч в акте, 40 ч по коду', 'пример расчёта UpCore'),
            ('2 дня', 'на аудит бюджета проекта по коду — без внедрения', None)],
            None, CALC_100, 'Деньги вместо story points: потери, созданная ценность и реальная ставка — в рублях по каждому человеку, проекту и подрядчику.'),
        security(True),
        cta('Узнайте реальную эффективность команды уже сегодня', 'Подключите репозиторий или закажите аудит — первые результаты по истории вашего кода, без ожидания.'),
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
   'A': dict(h1='Окупается ли ИИ в вашей разработке? [[Ответ — в коде]], а не в опросах',
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
    return [header(key), hero(p['badge'], hv['h1'], hv['sub'], ctas, hv['st'], image_console(img, path, t, c, key), hv['note'], key)]

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
            kpi('ЭФФЕКТ ДЛЯ БИЗНЕСА', 'Что Grade даёт в цифрах', [
                ('+12%', 'к производительности команды сразу: прозрачные правила — и люди сами держат темп', 'данные UpCore'),
                ('≈5 млн ₽', 'в месяц стоят 20% неэффективных на каждые 100 разработчиков — Grade показывает, кто они', 'расчёт UpCore'),
                ('2,5 ставки', 'тимлидов освобождается на 100 разработчиков: оценка и performance review — автоматически', '~4 ч в месяц на человека'),
                ('3 мес.', 'и грейд новичка подтверждён кодом — до конца испытательного срока', 'методика UpCore'),
                ('−202 тыс. ₽', 'потерь за месяц на одном разработчике в красной зоне — пример из практики', 'канал UpCore'),
                ('30–200%', 'годовой зарплаты стоит ошибка найма — Grade снижает этот риск', 'Минтруд США; SHRM')], 'grade', CALC_100),
            grade_axes(),
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
            kpi('ЭФФЕКТ ДЛЯ БИЗНЕСА', 'Бюджет на ИИ, который можно защитить', [
                ('+22 п.п.', 'эффективность MR, сделанных с ИИ, против ручных — кейс Dex (86% и 64%)', 'данные UpCore'),
                ('20–30%', 'средний реальный прирост от ИИ — UpCore показывает, где он есть, а где ИИ только тратит токены', 'данные UpCore'),
                ('250 тыс.', 'токенов на MR и 30 тыс. на час результата — нормы, перерасход виден по каждому разработчику', 'демо UpCore'),
                ('0 мес.', 'ожидания отчёта «до и после ИИ»: базовая линия — из истории Git', None)], 'ai',
                ('Куда направить бюджет на ИИ', [('Senior + ИИ', '+50–100%'), ('Middle + ИИ', '0…+20%'), ('Junior + ИИ', 'до −50%')], ('Лицензии и обучение', 'по отдаче'),
                 'Данные UpCore. Один и тот же инструмент даёт разный результат: UpCore показывает отдачу по каждому человеку и команде, чтобы бюджет на ИИ не делили «на всех поровну».')),
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
            modules('РЕЗУЛЬТАТ', 'Решения по ИИ — на данных', [
                ('Бюджет на ИИ, который себя защищает', 'Отчёт «ROI от ИИ» для совета директоров и финансов — в часах и рублях.'),
                ('Лицензии и обучение — тем, кому нужно', 'Понятно, кому ИИ даёт +50%, а кому пока вредит, — и кого научить работать с ним.'),
                ('Контроль качества вайбкодинга', 'Слепая генерация видна сразу: рост переделок, дублей и багов — до того, как это станет техдолгом.')], 'ai'),
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
            kpi('ЭФФЕКТ ДЛЯ БИЗНЕСА', 'Сколько возвращает контроль по коду', [
                ('−75%', 'к оплате в примере аудита: в акте 160 часов, объективно по коду — 40', 'пример расчёта UpCore'),
                ('≈1,6 млн ₽', 'в месяц переплаты у подрядчика из 10 разработчиков при эффективности 60%', 'пример расчёта'),
                ('2 дня', 'на аудит бюджета проекта по коду — до акта, продления контракта или сделки', None),
                ('100%', 'MR подрядчика проверены — не выборочно, а каждый', None)], 'projects',
                ('Подрядчик из 10 разработчиков', [('Часов в актах за месяц', '1 600 ч'), ('Стоимость при ставке 2 500 ₽/ч', '4,0 млн ₽'), ('Объективно по коду при эффективности 60%', '960 ч')],
                 ('Переплата в месяц', '≈1,6 млн ₽'), 'Пример расчёта: ставку и эффективность подставьте свои — UpCore посчитает их по вашему коду.')),
            projects_example(),
            modules('ЧТО В ОТЧЁТЕ', 'Всё о проекте — в часах, рублях и рисках', [
                ('Объективная стоимость', 'Трудоёмкость кода в часах и рублях — за месяц, квартал или весь проект.'),
                ('Эффективность команды', 'Часы результата против списанных и рабочих часов — по людям и подрядчикам.'),
                ('Прогноз сроков', 'Когда команда закроет объём и насколько велик риск выйти за дедлайн.'),
                ('Техдолг', 'Какая доля дефектов, найденных ревью, ушла в main — по категориям качества ISO/IEC 25010.'),
                ('Сложность и легаси', 'Размер, сложность, доля легаси и прирост проекта — чтобы сравнивать проекты честно.'),
                ('Тех-карта и мэтч команды', 'Какие технологии есть в коде и насколько им соответствует команда; вакансия и подбор под пробелы.')], 'projects'),
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
            kpi('ЭФФЕКТ ДЛЯ БИЗНЕСА', 'Что Mentor даёт в цифрах', [
                ('114 ч', 'ручного ревью в месяц экономит авто-ревью: проверено 94% MR, +228 тыс. ₽', 'демо-компания, 488 MR в месяц'),
                ('6,0 → 8,0', 'качество кода по ревью после исправлений — из 10', 'демо UpCore'),
                ('15 мин', 'нужно лиду на критичные MR вместо часов ревью всего подряд', 'данные UpCore')], 'mentor', None, None,
                'Время старших инженеров возвращается в разработку, а рост каждого разработчика виден в цифрах — по звезде компетенций и динамике грейда.'),
            mentor_chat(),
            roles('РЕЗУЛЬТАТ', 'Что получает каждый в команде', [
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
