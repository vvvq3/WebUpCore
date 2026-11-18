# -*- coding: utf-8 -*-
"""Презентации UpCore для CTO (PDF): платформа + 4 продукта × 4 варианта.

Варианты: 1 — короткая, 2 — средняя, 3 — длинная (стиль сайта, тёмная тема), 4 — светлая тема (содержание средней, другая раскладка).
Тексты и цифры — с сайта (данные берутся из tools/content/build_pages.py, где возможно).

python3 tools/decks/build_decks.py        # HTML в tools/decks/build/
node tools/decks/render.js                # PDF в docs/decks/ + проверка переполнения + превью
"""
import os, re, sys, html as H

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, 'build')
sys.path.insert(0, os.path.join(ROOT, 'tools', 'content'))
import build_pages as bp  # noqa: E402

IMG = 'file://' + os.path.join(HERE, 'img')
FONTS = 'file://' + os.path.join(HERE, 'fonts')

# цвет продукта: (линия, текст на тёмном, текст на светлом)
ACC = {'platform': ('#63D5FF', '#63D5FF', '#0A7FB0'), 'grade': ('#63D5FF', '#63D5FF', '#0A7FB0'),
       'ai': ('#9B8CFF', '#B9AEFF', '#5B43D6'), 'projects': ('#F2C14E', '#F2C14E', '#9A6B00'),
       'mentor': ('#53C04D', '#7FDB7A', '#23802A')}
NAME = {'platform': ('UpCore', 'Платформа'), 'grade': ('UpCore', 'Grade'), 'ai': ('UpCore', 'AI'),
        'projects': ('UpCore', 'Projects'), 'mentor': ('UpCore', 'Mentor')}
SHOT = {f: (k, t, c) for k, t, c, f in bp.SCREENS}  # '01-level.png' → (ключ, заголовок, подпись)


def e(t):
    return H.escape(str(t), quote=False)


NB = re.compile(r'(?<![\w-])(в|с|к|и|а|о|у|я|на|за|из|до|по|от|не|без|для|при|под|над|об|во|со|ко|то|что|как|или|ни|же|ли)\s', re.I)


def nb(t):
    """Неразрывный пробел после коротких слов и перед тире."""
    return NB.sub(lambda m: m.group(1) + '\u00a0', t).replace(' — ', '\u00a0— ')


def rich(t):
    """**жирное** и [[акцент]]."""
    t = nb(e(t))
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    return re.sub(r'\[\[(.+?)\]\]', r'<span class="acc">\1</span>', t)


# ---------------------------------------------------------------- CSS
CSS = r'''
@font-face { font-family: 'Bricolage'; src: url('%(F)s/bricolage-grotesque-latin-opsz-normal.woff2') format('woff2'); font-weight: 200 800; }
@font-face { font-family: 'Onest'; src: url('%(F)s/onest-cyrillic-wght-normal.woff2') format('woff2'); font-weight: 100 900; unicode-range: U+0301, U+0400-045F, U+0490-0491, U+04B0-04B1, U+2116; }
@font-face { font-family: 'Onest'; src: url('%(F)s/onest-latin-wght-normal.woff2') format('woff2'); font-weight: 100 900; }
@font-face { font-family: 'Mono'; src: url('%(F)s/jetbrains-mono-cyrillic-wght-normal.woff2') format('woff2'); font-weight: 100 800; unicode-range: U+0301, U+0400-045F, U+0490-0491, U+04B0-04B1, U+2116; }
@font-face { font-family: 'Mono'; src: url('%(F)s/jetbrains-mono-latin-wght-normal.woff2') format('woff2'); font-weight: 100 800; }
@page { size: 1920px 1080px; margin: 0; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
:root { --bg: #0D0C15; --card: #1A1925; --card2: #12111C; --line: rgba(255,255,255,0.10); --line2: rgba(255,255,255,0.16); --fg: #FFFFFF;
  --muted: rgba(255,255,255,0.74); --dim: rgba(255,255,255,0.52); --pos: #7FDB7A; --neg: #F08A8A; --amber: #F2C14E; --violet: #B9AEFF;
  --acc: %(A1)s; --acct: %(A2)s; --shadow: none; --logo: url('%(I)s/logo-light-on-dark.svg'); --scr-bar: #12111C; }
.light { --bg: #F4F6FA; --card: #FFFFFF; --card2: #EEF2F7; --line: #E1E6EE; --line2: #D3DAE5; --fg: #0D0C15; --muted: #3E4453; --dim: #6E7586;
  --pos: #23802A; --neg: #C8423F; --amber: #9A6B00; --violet: #5B43D6; --acct: %(A3)s; --shadow: 0 10px 30px rgba(20,30,60,0.08);
  --logo: url('%(I)s/logo-dark-on-light.svg'); --scr-bar: #FFFFFF; }
.slide { position: relative; width: 1920px; height: 1080px; overflow: hidden; background: var(--bg); color: var(--fg);
  font-family: 'Bricolage', 'Onest', system-ui, sans-serif; page-break-after: always; break-after: page; }
.light .slide { font-family: 'Onest', system-ui, sans-serif; }
.content { position: absolute; left: 110px; right: 110px; top: 92px; bottom: 120px; display: flex; flex-direction: column; }
.foot { position: absolute; left: 110px; right: 110px; bottom: 44px; height: 32px; display: flex; align-items: center; justify-content: space-between;
  font-family: 'Mono', monospace; font-size: 17px; color: var(--dim); }
.foot .lg { display: flex; align-items: center; gap: 18px; }
.foot .lg i { display: block; width: 150px; height: 24px; background: var(--logo) left center / contain no-repeat; }
.light .slide::before { content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 14px; background: var(--acc); }
.chev { position: absolute; right: -160px; top: -60px; width: 760px; opacity: 0.12; filter: blur(2px); pointer-events: none; }
.light .chev { opacity: 0.08; filter: none; }
.lbl { font-family: 'Mono', monospace; font-size: 20px; letter-spacing: 0.06em; color: var(--acct); text-transform: uppercase; margin-bottom: 18px; }
.light .lbl { display: inline-flex; align-self: flex-start; padding: 8px 14px; border-radius: 10px; background: color-mix(in srgb, var(--acc) 16%%, transparent); color: var(--acct); }
h1, h2, h3, p { margin: 0; }
h2 { font-size: 60px; line-height: 1.06; letter-spacing: -0.03em; font-weight: 800; max-width: 1640px; }
.light h2 { font-size: 56px; letter-spacing: -0.025em; }
.lead { font-size: 28px; line-height: 1.5; color: var(--muted); margin-top: 22px; max-width: 1350px; font-family: 'Onest', sans-serif; }
.acc { color: var(--acct); }
b { font-weight: 700; color: var(--fg); }
.body { flex: 1 1 auto; min-height: 0; margin-top: 44px; display: flex; flex-direction: column; gap: 22px; }
.row { display: flex; gap: 22px; min-height: 0; }
.grid { display: grid; gap: 22px; }
.g2 { grid-template-columns: repeat(2, minmax(0, 1fr)); } .g3 { grid-template-columns: repeat(3, minmax(0, 1fr)); } .g4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }
.card { min-width: 0; border-radius: 28px; background: var(--card); border: 1px solid var(--line); padding: 34px 36px; display: flex; flex-direction: column; gap: 14px; box-shadow: var(--shadow); }
.light .card { border-radius: 20px; }
.card.acc-b { border-color: color-mix(in srgb, var(--acc) 45%%, transparent); background: linear-gradient(160deg, color-mix(in srgb, var(--acc) 12%%, var(--card)) 0%%, var(--card) 55%%); }
.card .k { font-family: 'Mono', monospace; font-size: 18px; letter-spacing: 0.05em; color: var(--acct); text-transform: uppercase; }
.card .t { font-size: 30px; line-height: 1.2; font-weight: 800; letter-spacing: -0.01em; }
.card .x { font-size: 22px; line-height: 1.5; color: var(--muted); font-family: 'Onest', sans-serif; }
.big { font-size: 84px; line-height: 1; font-weight: 800; letter-spacing: -0.04em; color: var(--acct); font-variant-numeric: tabular-nums; }
.big.s { font-size: 64px; }
.spread > :first-child { margin-bottom: auto; }
.spread .x { font-size: 23px; }
.ctaS .content { justify-content: center; }
.statsS .body { justify-content: center; }
.statsS .stat .n { font-size: 104px; }
.stat .n { white-space: nowrap; }
.light .statsS .stat .n { font-size: 92px; }
.statsS .stats { gap: 56px 40px; padding-top: 48px; }
.pos { color: var(--pos) !important; } .neg { color: var(--neg) !important; } .amb { color: var(--amber) !important; } .vio { color: var(--violet) !important; } .fg { color: var(--fg) !important; }
ul.bl { margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 14px; }
ul.bl li { display: grid; grid-template-columns: 22px minmax(0, 1fr); gap: 12px; font-size: 24px; line-height: 1.45; color: var(--muted); font-family: 'Onest', sans-serif; }
ul.bl li::before { content: '>'; color: var(--acct); font-weight: 800; font-family: 'Bricolage', sans-serif; }
ul.bl.lg li { font-size: 28px; }
.fact { border-radius: 16px; background: color-mix(in srgb, var(--acc) 12%%, transparent); border-left: 4px solid var(--acc); padding: 14px 20px; font-size: 22px; line-height: 1.45; font-family: 'Onest', sans-serif; color: var(--fg); }
.fact b { color: var(--acct); }
.mod { font-weight: 800; font-size: 58px; line-height: 1; letter-spacing: -0.035em; font-family: 'Bricolage', sans-serif; display: flex; align-items: baseline; gap: 14px; }
.mod .gt { color: var(--acc); }
.tag { display: inline-flex; padding: 8px 14px; border-radius: 10px; border: 1px solid var(--line2); font-family: 'Mono', monospace; font-size: 18px; color: var(--muted); }
.tags { display: flex; flex-wrap: wrap; gap: 10px; }
.screen { min-width: 0; border-radius: 22px; overflow: hidden; border: 1px solid color-mix(in srgb, var(--acc) 40%%, transparent); background: #fff; box-shadow: 0 30px 90px rgba(0,0,0,0.35); display: flex; flex-direction: column; }
.light .screen { box-shadow: 0 18px 50px rgba(20,30,60,0.14); border-color: var(--line2); }
.screen .bar { flex: 0 0 auto; display: flex; justify-content: space-between; padding: 12px 18px; background: var(--scr-bar); border-bottom: 1px solid var(--line); font-family: 'Mono', monospace; font-size: 16px; color: var(--dim); }
.screen .bar span:last-child { color: var(--acct); }
.screen .im { flex: 1 1 auto; min-height: 0; background: #fff center top / cover no-repeat; }
.cap { font-size: 20px; color: var(--dim); font-family: 'Onest', sans-serif; margin-top: 10px; }
.stat .n { font-size: 76px; font-weight: 800; letter-spacing: -0.04em; line-height: 1; color: var(--fg); font-variant-numeric: tabular-nums; }
.stat .n.acc { color: var(--acct); }
.stat .d { font-size: 22px; color: var(--muted); margin-top: 10px; line-height: 1.4; font-family: 'Onest', sans-serif; }
.stats { display: grid; gap: 28px 40px; border-top: 1px solid var(--line); padding-top: 32px; }
.tbl { width: 100%%; border-collapse: collapse; font-family: 'Onest', sans-serif; }
.tbl td { padding: 16px 0; border-top: 1px solid var(--line); font-size: 24px; color: var(--muted); }
.tbl td:last-child { text-align: right; font-weight: 800; color: var(--fg); white-space: nowrap; font-family: 'Bricolage', 'Onest', sans-serif; }
.tbl.tight td { padding: 12px 0; } .tbl.tight tr.tot td { padding-top: 14px; }
.tbl tr.tot td { border-top: 2px solid var(--acc); font-size: 32px; font-weight: 800; color: var(--fg); padding-top: 22px; }
.tbl tr.tot td:last-child, .tbl tr.hl td:last-child { color: var(--acct); }
.hbar { display: flex; flex-direction: column; gap: 10px; }
.hbar .lab { display: flex; justify-content: space-between; font-size: 24px; color: var(--muted); font-family: 'Onest', sans-serif; }
.hbar .lab b { color: var(--fg); }
.hbar .tr { height: 26px; border-radius: 13px; background: color-mix(in srgb, var(--fg) 8%%, transparent); overflow: hidden; }
.hbar .tr div { height: 100%%; border-radius: 13px; }
.step { display: grid; grid-template-columns: 64px minmax(0, 1fr); gap: 20px; align-items: start; padding: 22px 0; border-top: 1px solid var(--line); }
.step .num { width: 64px; height: 64px; border-radius: 18px; background: color-mix(in srgb, var(--acc) 16%%, transparent); color: var(--acct); display: flex; align-items: center; justify-content: center; font-family: 'Mono', monospace; font-size: 22px; font-weight: 700; }
.step .st { font-size: 30px; font-weight: 800; line-height: 1.25; }
.step .sx { font-size: 22px; color: var(--muted); margin-top: 6px; line-height: 1.45; font-family: 'Onest', sans-serif; }
.qa .q { font-size: 30px; font-weight: 800; line-height: 1.3; }
.qa .a { font-size: 24px; line-height: 1.55; color: var(--muted); font-family: 'Onest', sans-serif; }
.cta { border-radius: 40px; background: var(--acc); color: #0D0C15; padding: 64px 72px; display: flex; flex-direction: column; gap: 22px; }
.cta h2 { color: #0D0C15; font-size: 64px; }
.cta p { font-size: 28px; line-height: 1.5; color: rgba(13,12,21,0.8); font-family: 'Onest', sans-serif; max-width: 1300px; }
.cta .ct { display: flex; gap: 64px; margin-top: 18px; padding-top: 28px; border-top: 1px solid rgba(13,12,21,0.2); }
.cta .ct div span { display: block; font-family: 'Mono', monospace; font-size: 18px; color: rgba(13,12,21,0.6); margin-bottom: 6px; }
.cta .ct div b { color: #0D0C15; font-size: 32px; }
.cta .pills { display: flex; gap: 14px; flex-wrap: wrap; }
.cta .pill { padding: 14px 22px; border-radius: 16px; background: #0D0C15; color: #fff; font-size: 24px; font-weight: 700; }
.cta .pill.o { background: transparent; border: 2px solid #0D0C15; color: #0D0C15; }
.cover .content { justify-content: center; }
.cover h1 { font-size: 92px; line-height: 1.02; letter-spacing: -0.035em; font-weight: 800; max-width: 1250px; }
.cover .sub { font-size: 32px; line-height: 1.45; color: var(--muted); margin-top: 30px; max-width: 1150px; font-family: 'Onest', sans-serif; }
.cover .kick { font-family: 'Mono', monospace; font-size: 22px; color: var(--acct); letter-spacing: 0.06em; margin-bottom: 26px; text-transform: uppercase; }
.cover .mod { font-size: 76px; margin-bottom: 30px; }
.light .cover h1 { font-size: 86px; }
.light .cover .band { position: absolute; right: 0; top: 0; bottom: 0; width: 620px; background: linear-gradient(160deg, color-mix(in srgb, var(--acc) 22%%, #fff), color-mix(in srgb, var(--acc) 6%%, #fff)); }
.sec .content { justify-content: center; }
.sec h2 { font-size: 84px; max-width: 1400px; }
.sec .no { font-family: 'Mono', monospace; font-size: 26px; color: var(--acct); margin-bottom: 24px; }
.ring text { font-family: 'Bricolage', sans-serif; }
.strike { text-decoration: line-through; text-decoration-color: var(--neg); color: var(--dim); font-size: 26px; font-family: 'Onest', sans-serif; }
.kv { display: flex; flex-direction: column; gap: 4px; } .kv span { font-size: 18px; color: var(--dim); font-family: 'Onest', sans-serif; } .kv b { font-size: 36px; }
.sig { display: flex; align-items: center; gap: 16px; padding: 14px 18px; border-radius: 14px; background: color-mix(in srgb, var(--fg) 4%%, transparent); font-size: 22px; font-family: 'Onest', sans-serif; color: var(--muted); }
.sig i { width: 12px; height: 12px; border-radius: 50%%; flex: 0 0 auto; }
.sig b { font-family: 'Bricolage', 'Onest', sans-serif; }
'''

CHEVRON = ('<svg class="chev" viewBox="0 0 375 645" aria-hidden="true"><path fill="var(--acc)" d="M340.243 410.873C322.404 436.777 298.363 465.078 268.118 495.774L166.429 598.984C149.417 616.251 135.926 628.481 125.958 635.674C116.005 643.826 105.711 645.5 95.078 640.695C84.4595 636.849 69.8902 625.803 51.3702 607.556L9.90889 566.705L249.7 322.254L0.000749597 79.9674L43.9849 35.3256C61.4698 17.5791 75.6986 6.54952 86.6712 2.23669C96.6839 -2.07669 106.793 -0.151217 116.998 8.01309C126.716 15.6972 140.347 28.1827 157.893 45.4695L271.54 157.442C294.446 180.011 314.443 200.659 331.531 219.385C348.146 238.591 359.968 258.274 366.999 278.434C373.542 298.114 374.78 322.343 370.134 347.567C365.05 375.17 358.57 385.448 340.243 410.873Z"/></svg>')


# ---------------------------------------------------------------- компоненты
def mod(key, size=None):
    a, b = NAME[key]
    st = (' style="font-size: %dpx;"' % size) if size else ''
    if key == 'platform':
        return '<div class="mod"%s><span class="gt">&gt;</span><span>UpCore<span class="acc">.</span></span></div>' % st
    return '<div class="mod"%s><span class="gt">&gt;</span><span>UpCore<span class="acc">.%s</span></span></div>' % (st, b)


def card(inner, cls=''):
    return '<div class="card %s">%s</div>' % (cls, inner)


def bl(items, cls=''):
    return '<ul class="bl %s">%s</ul>' % (cls, ''.join('<li><span>%s</span></li>' % rich(x) for x in items))


def screen(f, label=None, style=''):
    k, t, c = SHOT[f]
    im = os.path.join(HERE, 'img', 'screens', f.replace('.png', '.jpg'))
    return ('<div class="screen" style="%s"><div class="bar"><span>upcore://screens / %s</span><span>демо</span></div>'
            '<div class="im" style="background-image: url(\'file://%s\');"></div></div>') % (style, e(label or k), im)


def stats(items, cols=4):
    return '<div class="stats" style="grid-template-columns: repeat(%d, minmax(0, 1fr));">%s</div>' % (cols, ''.join(
        '<div class="stat"><div class="n%s">%s</div><div class="d">%s</div></div>' % (' acc' if i == 0 else '', e(n), e(d)) for i, (n, d) in enumerate(items)))


def hbar(label, val, pct, col):
    return ('<div class="hbar"><div class="lab"><span>%s</span><b>%s</b></div><div class="tr"><div style="width: %d%%; background: %s;"></div></div></div>' % (e(label), e(val), pct, col))


def ring(num='80', of='из 160 ч', pct=50):
    r = 70; c = 2 * 3.14159 * r
    return ('<svg class="ring" viewBox="0 0 180 180" width="260" height="260">'
            '<circle cx="90" cy="90" r="%d" fill="none" stroke="var(--neg)" stroke-width="24"></circle>'
            '<circle cx="90" cy="90" r="%d" fill="none" stroke="var(--acc)" stroke-width="24" stroke-dasharray="%.1f %.1f" transform="rotate(-90 90 90)"></circle>'
            '<text x="90" y="92" text-anchor="middle" font-size="44" font-weight="800" fill="var(--fg)">%s</text>'
            '<text x="90" y="120" text-anchor="middle" font-size="16" fill="var(--dim)">%s</text></svg>') % (r, r, c * pct / 100, c, num, of)


# ---------------------------------------------------------------- слайды
def S(base, inner, label=None, title=None, lead=None, kind=None):
    """Один слайд: kind — 'std' | 'cover' | 'sec' | 'cta'."""
    head = ''
    if label:
        head += '<div class="lbl">%s</div>' % e(label)
    if title:
        head += '<h2>%s</h2>' % rich(title)
    if lead:
        head += '<p class="lead">%s</p>' % rich(lead)
    body = ('<div class="body">%s</div>' % inner) if inner else ''
    return {'kind': kind or base, 'html': head + body}


def s_cover(key, title, sub, kicker, tags, side=None):
    inner = ('<div class="kick">%s</div>%s<h1>%s</h1><p class="sub">%s</p><div class="tags" style="margin-top: 40px;">%s</div>' % (
        e(kicker), mod(key), rich(title), rich(sub), ''.join('<span class="tag">%s</span>' % e(t) for t in tags)))
    return {'kind': 'cover', 'html': inner, 'side': side}


def s_section(no, title, lead=None):
    return {'kind': 'sec', 'html': '<div class="no">%s</div><h2>%s</h2>%s' % (e(no), rich(title), ('<p class="lead">%s</p>' % rich(lead)) if lead else '')}


def s_cta(title, text, extra=None):
    inner = ('<div class="cta"><h2>%s</h2><p>%s</p>%s<div class="pills"><span class="pill">Заказать бесплатный пилот</span><span class="pill o">Провести демо</span></div>'
             '<div class="ct"><div><span>ТЕЛЕФОН</span><b>+7 (985) 848-35-55</b></div><div><span>TELEGRAM</span><b>@IvanGel_Dex</b></div>'
             '<div><span>ПОЧТА</span><b>office@dex-it.ru</b></div><div><span>САЙТ</span><b>up-core.ru</b></div></div></div>') % (rich(title), rich(text), extra or '')
    return {'kind': 'cta', 'html': inner}


# ---------- общие блоки платформы (используются во всех презентациях)
def sl_problem():
    items = [('20% → 4%', 'До 20% ФОТ уходит на инженеров, которые дают лишь **4% результата**.'),
             ('5–10%', 'Изменений в коде тимлид успевает **глубоко проверить** — остальное уходит без ревью.'),
             ('82%', 'Компаний **не знают**, ускоряет ли ИИ команду или плодит техдолг.'),
             ('30–45%', 'В среднем **завышены** акты аутстаффа и подряда относительно кода.')]
    cards = ''.join(card('<div class="big%s" style="font-size: 72px; white-space: nowrap;">%s</div><div class="x" style="font-size: 26px;">%s</div>' % (' neg' if i in (0, 3) else '', e(b), rich(t)), 'spread') for i, (b, t) in enumerate(items))
    return S('std', '<div class="grid g4" style="flex: 1;">%s</div>' % cards, 'Проблема',
             'Разработка — крупнейшая статья расходов. И самая [[непрозрачная]]',
             'Строки, коммиты и закрытые тикеты легко накрутить — особенно с ИИ. Статусы в Jira не показывают, сколько реальной работы за ними стоит.')


def sl_how():
    steps = [('01 · ВХОД', 'Merge Request', 'Код, история репозитория и контекст проекта. Ничего не нужно заполнять вручную.'),
             ('02 · ДЕКОМПОЗИЦИЯ', '50+ факторов', 'Сложность, архитектура (AST), технологии, результирующий код, баги, шум.'),
             ('03 · МОДЕЛЬ', 'Детерминированная математика', 'Откалибрована на 300 000+ MR под каждый стек. Один код — одна оценка.'),
             ('04 · РЕЗУЛЬТАТ', 'Нормо-часы → деньги', 'Эффективность, грейд, рейтинг, бюджет проекта и отдача от ИИ.')]
    cards = ''.join(card('<div class="k">%s</div><div class="t">%s</div><div class="x">%s</div>' % (e(a), e(b), e(c)), 'spread acc-b' if i == 3 else 'spread') for i, (a, b, c) in enumerate(steps))
    formula = ('<div class="card" style="flex-direction: row; align-items: center; gap: 40px; padding: 30px 40px;"><div style="font-size: 38px; font-weight: 800; flex: 1;">'
               'Эффективность = <span class="acc">объективные нормо-часы</span> ÷ фактические часы</div>'
               '<div class="x" style="flex: 0 0 560px;">Пример: за месяц 160 часов, реальной работы в коде — на 80. Эффективность 50%, потери — 80 ч × ставка.</div></div>')
    return S('std', '<div class="grid g4" style="flex: 1;">%s</div>%s' % (cards, formula), 'Как это работает',
             'Каждый Merge Request → [[объективные человеко-часы]]',
             'Ядро — детерминированная математика, поверх — ИИ-агенты для ревью и наставничества. Модель оценивает трудоёмкость изменений так же, как Senior-ревьюер, — за 1 секунду на MR.')


def sl_160():
    left = ('<div class="card" style="flex: 1; gap: 22px;"><div class="k" style="color: var(--dim);">обычные метрики — «выглядит продуктивно»</div>'
            '<div style="display: flex; gap: 36px; flex-wrap: wrap;"><span class="strike">10 423 строк</span><span class="strike">35 merge request</span><span class="strike">27 закрытых задач</span></div>'
            '<div style="display: flex; align-items: center; gap: 48px; margin-top: 10px;">%s<div style="display: flex; flex-direction: column; gap: 18px; font-size: 30px; font-family: Onest, sans-serif;">'
            '<div>Списано за месяц <b>160 ч</b></div><div>Реально решённых задач <b class="neg">80 ч</b></div><div>Эффективность <b class="neg">50%%</b></div></div></div>'
            '<div style="border-top: 1px solid var(--line); padding-top: 22px; font-size: 28px; font-family: Onest, sans-serif;"><b class="neg" style="font-size: 44px;">−140 тыс. ₽ / мес</b>'
            ' <span style="color: var(--muted);">— скрытые потери бюджета на одном разработчике (техдолг, переделки, простой)</span></div></div>') % ring()
    right = '<div style="flex: 0 0 560px; display: flex; flex-direction: column; gap: 22px;">%s</div>' % ''.join(
        card('<div class="t">%s</div><div class="x">%s</div>' % (e(a), e(b))) for a, b in bp.CORE_V2_CARDS[:3])
    return S('std', '<div class="row" style="flex: 1;">%s%s</div>' % (left, right), 'Как работает математическая модель',
             'Считаем [[инженерную ценность кода]], а не строки и часы за экраном')


def sl_model4():
    cards = ''.join(card('<div class="big" style="font-size: 72px; opacity: 0.9;">%02d</div><div class="t">%s</div><div class="x">%s</div>' % (i + 1, e(a), e(b)), 'spread acc-b' if i in (1, 2) else 'spread') for i, (a, b) in enumerate(bp.CORE_V2_CARDS))
    return S('std', '<div class="grid g4" style="flex: 1;">%s</div>' % cards, 'Точность', 'Почему оценке можно доверять',
             '96% совпадения с оценкой Senior-экспертов на 300 000+ MR. Каждый вывод раскрывается в «Глазе» до строчки кода.')


def sl_numbers():
    return S('std', stats([('96%', 'совпадение с оценкой Senior-экспертов'), ('1500+', 'разработчиков проанализировано'), ('300 000+', 'MR в калибровке модели'),
                           ('50+', 'факторов в каждом MR'), ('+14%', 'рост выработки команды за 3 месяца'), ('+12%', 'к производительности сразу — от прозрачности'),
                           ('1 сек', 'на анализ одного MR'), ('1 час', 'на ретро-анализ полугода истории')], 4), 'UpCore в цифрах', 'Цифры, на которых построена платформа', kind='statsS')


def sl_platform4(compact=False):
    cards = []
    for key, m, num, roles, t, fact, lis, q, more in bp.PLATFORM_V2:
        line, txt, _ = ACC[key]
        inner = ('<div style="display: flex; justify-content: space-between; font-family: Mono, monospace; font-size: 16px; color: var(--dim);"><span>%s</span><span>%s</span></div>'
                 '<div class="mod" style="font-size: %dpx;"><span class="gt" style="color: %s;">&gt;</span><span>UpCore<span style="color: %s;">.%s</span></span></div>'
                 '<div class="t" style="font-size: %dpx; font-weight: 700;">%s</div>') % (num, e(roles), 40 if compact else 36, line, line, m, 26 if compact else 24, e(t))
        if not compact:
            inner += '<div class="fact" style="--acc: %s; font-size: 19px;"><b style="color: inherit;">Факт:</b> %s</div>' % (line, e(fact))
            inner += '<ul class="bl" style="gap: 12px;">%s</ul>' % ''.join('<li style="font-size: 20px; grid-template-columns: 18px minmax(0, 1fr);"><span><b>%s</b> %s</span></li>' % (e(a), e(b)) for a, b in lis)
            inner += '<div style="margin-top: auto; font-size: 22px; font-weight: 700; color: %s;">%s</div>' % (line, e(q))
        else:
            inner += '<div class="x">%s</div>' % e(fact)
        cards.append(card(inner, '" style="padding: 30px 28px;' if not compact else ''))
    return S('std', '<div class="grid %s" style="flex: 1;">%s</div>' % ('g2' if compact else 'g4', ''.join(cards)), 'Платформа UpCore',
             'Одна платформа — [[четыре задачи C-level]]', 'Один read-only коннект к Git закрывает контроль грейдов, ROI от ИИ, бюджетов и код-ревью.')


def sl_econ():
    tiles = ''.join(card('<div class="big s%s" style="font-size: 54px;">%s</div><div class="x">%s</div>' % (' pos' if i == 0 else '', e(a), e(b)), '" style="padding: 26px 32px; gap: 8px;') for i, (a, b) in enumerate(
        [('до +30%', 'рост фактической выработки за счёт прозрачности'), ('−20%', 'time-to-market: потери в процессах становятся видны'), ('2,5 ставки', 'тимлидов на 100 инженеров освобождаются от рутинного ревью')]))
    calc = ('<div class="card" style="flex-direction: row; gap: 56px; flex: 1; padding: 28px 36px;"><div style="flex: 0 0 600px; display: flex; flex-direction: column; gap: 16px;"><div class="k">РАСЧЁТ</div>'
            '<div class="t" style="font-size: 40px;">Эффект на команду из 100 разработчиков</div><div class="x" style="font-size: 20px;">База консервативного расчёта: 100 разработчиков при минимальной ставке 250 тыс. ₽/мес (ФОТ 25 млн ₽/мес) и ставке тимлида 400 тыс. ₽/мес. При корпоративном ФОТ 400–600 тыс. ₽/мес эффект больше в 1,6–2,4 раза.</div></div>'
            '<table class="tbl tight" style="flex: 1;"><tr><td>Половина «дыры» 20% неэффективных: −10% потерь ФОТ</td><td>≈2,5 млн ₽</td></tr><tr><td>+12% к выработке остальных — от прозрачности</td><td>≈3,0 млн ₽</td></tr>'
            '<tr><td>2,5 ставки тимлидов освобождаются от ручной оценки</td><td>≈1,0 млн ₽</td></tr><tr class="tot"><td>Итого в месяц</td><td>≈6,5 млн ₽</td></tr>'
            '<tr><td>В год на команду</td><td>≈78 млн ₽</td></tr><tr class="hl"><td>На одного разработчика в год</td><td>≈780 тыс. ₽</td></tr></table></div>')
    return S('std', '<div class="grid g3">%s</div>%s' % (tiles, calc), 'Экономический эффект', 'Окупаемость платформы на команде из 100 инженеров')


def sl_security(short=False):
    steps = [('01', 'Облако или On-Premise', 'подключение к GitHub, GitLab, Bitbucket или локальному Git'), ('02', 'Только Read-Only доступ', 'без прав на изменение репозиториев'),
             ('03', 'Результат через 1 час', 'проанализируем работу за последние 6 месяцев')]
    left = '<div class="card acc-b" style="flex: 1.05;"><div class="k">ПОДКЛЮЧЕНИЕ</div><div class="t" style="font-size: 38px;">Развёртывание и первый отчёт за 1 час</div>%s<div class="tags" style="margin-top: auto;">%s</div></div>' % (
        ''.join('<div class="step"><div class="num">%s</div><div><div class="st">%s</div><div class="sx">%s</div></div></div>' % (a, e(b), e(c)) for a, b, c in steps),
        ''.join('<span class="tag">%s</span>' % x for x in ['C#', 'Java', 'Go', 'Python', 'Kotlin', 'PHP', 'JS/TS', 'C++', '1С']))
    g = [('On-Premise в закрытом контуре', 'Развёртывание внутри периметра компании без доступа в интернет. Серверные GPU не требуются.'),
         ('Простая интеграция', 'С корпоративными трекерами, дашбордами, отчётами и по протоколу MCP.'),
         ('Готовы к проверке ИБ', 'Документация и карта модулей для ИБ. Доступы только на чтение, код не переносится. Ролевая модель и полное логирование.'),
         ('Оплата после пилота', 'Бесплатный пилот на 2–3 проектах. Платите, когда подтвердите точность на своих данных.')]
    right = '<div class="grid g2" style="flex: 1;">%s</div>' % ''.join(card('<div class="t" style="font-size: 27px;">%s</div><div class="x">%s</div>' % (e(a), e(b))) for a, b in g)
    return S('std', '<div class="row" style="flex: 1;">%s%s</div>' % (left, right), 'Безопасность и подключение', 'Подключение за минуты. [[Код остаётся у вас]]')


def sl_pilot():
    steps = [('01', 'Подключение', 'Read-only доступ к 2–3 репозиториям — в облаке или on-premise в вашем контуре.'),
             ('02', 'Ретро-анализ', 'Через 1 час — эффективность, грейды, ИИ и бюджет по истории кода за 6 месяцев.'),
             ('03', 'Разбор с вами', 'Сверяем результаты с вашей экспертной оценкой: команды, проекты, подрядчики.'),
             ('04', 'Решение', 'Платите, только когда подтвердили точность на своих данных.')]
    cards = ''.join(card('<div class="big s" style="font-size: 56px;">%s</div><div class="t">%s</div><div class="x">%s</div>' % (a, e(b), e(c)), 'spread acc-b' if i == 1 else 'spread') for i, (a, b, c) in enumerate(steps))
    return S('std', '<div class="grid g4" style="flex: 1;">%s</div>' % cards, 'Как начать', 'Бесплатный пилот: [[результат через 1 час]]',
             'Без внедрения в процессы, без отчётов и тайм-трекеров — нужен только код.')


def sl_screen(f, label, title, lead, points, title_w=None):
    k, t, c = SHOT[f]
    side = '<div class="card" style="flex: 0 0 520px; justify-content: center;"><div class="t">%s</div><div class="x" style="margin-bottom: 8px;">%s</div>%s</div>' % (e(t), e(c), bl(points))
    return S('std', '<div class="row" style="flex: 1;">%s%s</div>' % (screen(f, style='flex: 1;'), side), label, title, lead)


def sl_gallery(files, label, title, lead=None):
    cells = ''.join('<div style="display: flex; flex-direction: column; min-height: 0;">%s<div class="cap"><b>%s</b> — %s</div></div>' % (
        screen(f, style='flex: 1;'), e(SHOT[f][1]), e(SHOT[f][2])) for f in files)
    cols = 'g2' if len(files) == 4 else 'g3'
    return S('std', '<div class="grid %s" style="flex: 1; grid-auto-rows: minmax(0, 1fr);">%s</div>' % (cols, cells), label, title, lead)


def sl_roles(items, title, label='Для кого'):
    cards = ''.join(card('<div class="t acc" style="font-size: 44px;">%s</div><div class="x" style="font-size: 28px; color: var(--muted);">%s</div>' % (e(r), rich(t)), 'spread') for r, t in items)
    return S('std', '<div class="grid g2" style="flex: 1;">%s</div>' % cards, label, title)


def sl_faq(items, title='Честные ответы на неудобные вопросы'):
    cards = ''.join(card('<div class="q">%s</div><div class="a">%s</div>' % (e(q), rich(a)), 'qa') for q, a in items)
    return S('std', '<div class="grid g2" style="flex: 1;">%s</div>' % cards, 'Вопросы', title)


# ---------- Grade
LV = lambda v: 'var(--pos)' if v >= 7 else ('var(--amber)' if v >= 4.5 else 'var(--neg)')


def sl_grade_profile(full=True):
    rows = ''.join('<div style="display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 16px; align-items: baseline; padding: 9px 0; border-top: 1px solid var(--line);">'
                   '<span style="font-size: 23px; font-family: Onest, sans-serif;"><b%s>%s</b>%s</span><span style="font-size: 19px; color: var(--dim); white-space: nowrap;">%s → <b style="font-size: 27px; color: %s;">%s</b></span></div>' % (
                       ' class="acc"' if i == 0 else '', e(n), ' <span style="color: var(--dim); font-size: 19px;">· %s</span>' % e(d) if full and i < 6 else '', ('%.1f' % w).replace('.', ','), LV(v), ('%.1f' % v).replace('.', ','))
                   for i, (n, v, w, d) in enumerate(bp.LEVEL))
    head = ('<div class="card" style="flex: 0 0 560px; gap: 26px;"><div class="k" style="color: var(--dim);">ДЕМО UPCORE · МЕНЮ «УРОВЕНЬ» · ОКТЯБРЬ 2026</div><div class="t" style="font-size: 40px;">Лукьянов Александр</div>'
            '<div class="x">Backend, C# · проект UpCore Backend</div>'
            '<div class="kv"><span>Грейд за 3 месяца</span><b class="pos" style="font-size: 54px;">Senior 8,5 <span style="font-size: 26px; color: var(--dim);">/ 10</span></b></div>'
            '<div class="kv"><span>Динамика роста</span><b style="font-size: 40px;"><span class="amb">Middle+</span> → <span class="pos">Senior</span></b><span>7,2 → 8,5 с мая по октябрь</span></div>'
            '<div class="kv"><span>Рейтинг за месяц</span><b style="font-size: 40px;">2 <span style="font-size: 24px; color: var(--dim);">из 14</span></b><span>в компании · 4 из 13 в стеке · 4 из 8 в проекте</span></div></div>')
    right = '<div class="card" style="flex: 1; gap: 0;"><div style="display: flex; justify-content: space-between;" class="k"><span>10 основных факторов из 50+</span><span style="color: var(--dim);">май → октябрь</span></div>%s</div>' % rows
    return S('std', '<div class="row" style="flex: 1;">%s%s</div>' % (head, right), 'Методика на примере', 'Прозрачный профиль грейда [[по 50+ факторам]]',
             'Не просто «Senior», а все факторы, из которых он сложился, — с динамикой и местом в рейтинге. Главный фактор — эффективность кода в часах.')


def sl_grade_factors():
    arch = ''.join(hbar(a, b, w, c) for a, b, w, c in [('Ядро', '59 ч · 7%', 7, 'var(--acc)'), ('Middle', '116 ч · 13%', 13, 'color-mix(in srgb, var(--acc) 60%, transparent)'), ('Периферия', '713 ч · 80%', 80, 'var(--dim)')])
    churn = ('<div style="display: flex; height: 30px; border-radius: 15px; overflow: hidden; gap: 4px;"><div style="flex: 1; background: var(--acc);"></div><div style="flex: 1; background: color-mix(in srgb, var(--neg) 60%, transparent);"></div></div>'
             '<div style="display: flex; justify-content: space-between; font-size: 21px; color: var(--muted); font-family: Onest, sans-serif;"><span><b class="acc">150 строк</b> дошли до релиза</span><span><b class="neg">150</b> удалены и переписаны</span></div>')
    tech = ''.join('<div class="sig" style="justify-content: space-between;"><span>%s</span><b style="color: %s;">%s</b></div>' % (a, c, b) for a, b, c in
                   [('Senior-технологии', '2 · 1,8 ч', 'var(--pos)'), ('Middle-технологии', '16 · 191,4 ч', 'var(--fg)'), ('Ввёл в проект новых', '1', 'var(--acct)'), ('Легаси / новое для себя', 'учитывается', 'var(--muted)')])
    cards = [('ФАКТОР 01', 'Архитектура (AST-граф)', arch, ['Разделяем правки в бизнес-ядре, middle-слое и на периферии.', '20 строк в ядре весят больше 200 строк вёрстки.']),
             ('ФАКТОР 02', 'Сложность стека и технологий', tech, ['Часы по карте компетенций каждого языка и фреймворка.', 'Коэффициент за сложный legacy и новые библиотеки.']),
             ('ФАКТОР 03', 'Выживаемость кода (Code Churn)', churn, ['В зачёт идут только строки, дошедшие до продакшена.', 'Отсекает мусорную генерацию и накрутку коммитов.'])]
    html = ''.join(card('<div class="k">%s</div><div class="t">%s</div><div style="display: flex; flex-direction: column; gap: 10px; min-height: 170px;">%s</div><div style="margin-top: auto;">%s</div>' % (a, e(b), v, bl(l))) for a, b, v, l in cards)
    return S('std', '<div class="grid g3" style="flex: 1;">%s</div>' % html, 'Подробно о факторах', 'Что невозможно оценить [[по Jira или резюме]]')


def sl_grade_rating():
    names = [('1', 'Ярослав Землинский', '100%', 'pos'), ('2', 'Александр Лукьянов', '100%', 'pos'), ('3', 'Анна Павловская', '90%', 'pos'), ('…', '', '', ''),
             ('12', 'Ольга Аристова', '35%', 'neg'), ('13', 'Владислав Редкозубов', '19%', 'neg'), ('14', 'Александр Марко', '12%', 'neg')]
    rows = ''.join(('<div style="padding: 4px 16px; color: var(--dim); font-size: 22px;">…</div>' if not n else
                    '<div style="display: grid; grid-template-columns: 54px minmax(0, 1fr) auto; gap: 14px; align-items: center; padding: 8px 18px; border-radius: 14px; margin-bottom: 4px; background: color-mix(in srgb, var(--%s) 12%%, transparent); font-size: 24px; font-family: Onest, sans-serif;">'
                    '<b>%s</b><span>%s</span><b class="%s">%s</b></div>' % (c, p, e(n), c, v)) for p, n, v, c in names)
    left = ('<div class="card" style="flex: 0 0 760px;"><div style="display: flex; justify-content: space-between;" class="k"><span>Демо · рейтинг по компании</span><span style="color: var(--dim);">октябрь 2026</span></div>'
            '<div class="k pos" style="font-size: 16px;">ТОП-20%%</div>%s<div class="k neg" style="font-size: 16px;">ЗОНА РИСКА (20%%) — ФОКУС ДЛЯ КОД-РЕВЬЮ И РОТАЦИИ</div></div>') % rows
    rh = [('Каждый месяц', 'Эффективность', 'Детальный отчёт: часы результата против рабочего времени, ценность в рублях, упущенная выгода.'),
          ('За 3 месяца', 'Грейд', 'Уровень 1–10 → Junior− … Senior. Окно в 3 месяца сглаживает аномалии отдельных задач.'),
          ('Каждый месяц', 'Рейтинг', 'По компании, стеку и проекту: топ-20% и зона риска, сравнение со средним по команде, стеку и компании.')]
    right = '<div style="flex: 1; display: flex; flex-direction: column; gap: 22px;">%s</div>' % ''.join(card('<div class="k">%s</div><div class="t">%s</div><div class="x">%s</div>' % (a, b, c), '" style="padding: 28px 36px; gap: 10px;') for a, b, c in rh)
    return S('std', '<div class="row" style="flex: 1;">%s%s</div>' % (left, right), 'Ритм оценки', 'Рейтинг команды [[каждый месяц]], грейд — за 3 месяца')


def sl_grade_value():
    items = [('Повышения и зарплаты', 'Решения по фактам из кода, а не по резюме, громкости на дейликах и впечатлениям.'),
             ('Испытательный срок', 'За сколько недель новичок вышел на среднюю эффективность команды — видно в цифрах.'),
             ('Performance review', 'Одна шкала для всех стеков и команд: тимлид не собирает статистику и не спорит.'),
             ('Без накруток', 'Шум, копипаст и автогенерация дают 0 часов; переписанный код не засчитывается.')]
    return S('std', '<div class="grid g2" style="flex: 1;">%s</div>' % ''.join(card('<div class="t" style="font-size: 34px;">%s</div><div class="x" style="font-size: 24px;">%s</div>' % (e(a), e(b)), 'spread') for a, b in items),
             'Что получает компания', 'Решения о людях — [[на данных]], а не на впечатлениях')


# ---------- AI
def sl_ai_gap():
    items = [('Раньше', '30%', 'Проблемой был разработчик, который работает на 30% от нормы.', 'neg'),
             ('Сейчас', '100%', 'Проблема — работать «как раньше». С ИИ 100% — это уже отставание.', 'amb'),
             ('Норма с ИИ', '300%', 'С ИИ эффективность может и должна быть 300% — наша цель 300–400%.', 'pos')]
    cards = ''.join(card('<div class="k %s">%s</div><div class="big %s" style="font-size: 120px;">%s</div><div class="x" style="font-size: 26px;">%s</div>' % (c, e(a), c, b, e(t))) for a, b, t, c in items)
    ranges = ''.join('<div style="flex: 1;">%s</div>' % hbar(n, lab, int((b - a) / 350 * 100) + 8, c) for n, a, b, lab, c in
                     [('Senior + ИИ', 50, 300, '+50…300%', 'var(--pos)'), ('Middle + ИИ', -20, 50, '−20…+50%', 'var(--amber)'), ('Junior + ИИ', -50, 0, '−50…0%', 'var(--neg)')])
    return S('std', '<div class="grid g3" style="flex: 1;">%s</div><div class="card" style="flex-direction: row; gap: 40px;">%s</div>' % (cards, ranges), 'Проблема',
             'С ИИ эффективность [[изменилась до неузнаваемости]]', 'Один и тот же инструмент даёт сеньору +300%, а джуну — минус. Разрыв между людьми стал огромным — его важно измерять.')


def sl_ai_roi():
    def row(lab, h, col):
        return ('<div style="display: grid; grid-template-columns: 130px minmax(0, 1fr) 70px; gap: 16px; align-items: center; font-size: 22px; font-family: Onest, sans-serif; color: var(--muted);">'
                '<span>%s</span><div class="hbar"><div class="tr" style="height: 22px;"><div style="width: %d%%; background: %s;"></div></div></div><b style="text-align: right;">%d ч</b></div>') % (lab, h / 8 * 100, col, h)

    def task(t, m, s, pct, col, note):
        return ('<div style="display: flex; flex-direction: column; gap: 14px; padding: 22px 0 6px; border-top: 1px solid var(--line);"><div style="display: flex; justify-content: space-between; align-items: baseline;">'
                '<b style="font-size: 28px;">%s</b><b style="font-size: 44px; color: %s;">%s</b></div>%s%s<div class="x" style="font-size: 20px;">%s</div></div>') % (
            e(t), col, pct, row('вручную', m, 'var(--dim)'), row('с ИИ', s, col), e(note))
    left = '<div class="card" style="flex: 1.2;"><div class="k">Два реальных случая</div>%s%s</div>' % (
        task('Ускорение ×4 · Senior', 8, 2, '×4', 'var(--pos)', 'Задача на 8 нормо-часов закрыта с ИИ за 2 часа чистым кодом.'),
        task('Потеря времени · Junior', 2, 8, '−6 ч', 'var(--neg)', 'Задача на 2 нормо-часа отняла 8 часов из-за галлюцинаций и отладки.'))
    right = '<div class="card acc-b" style="flex: 1; justify-content: center;"><div class="k">Что видит руководитель</div>%s</div>' % bl(
        ['**Доля ИИ-кода в каждом MR** против ручной разработки', '**Чистая экономия ФОТ** в часах и рублях за вычетом переделок', '**Динамика ускорения команды** от месяца к месяцу',
         '**Накрутки видны по коду:** дневную норму за час с ИИ не спрятать — без трекеров и скриншотов'], 'lg')
    return S('std', '<div class="row" style="flex: 1;">%s%s</div>' % (left, right), 'Измерение ROI от ИИ', 'Эталонные нормо-часы [[против фактических часов с ИИ]]',
             'Модель знает, сколько часов задача требует вручную, и сверяет это с фактическим временем и чистотой кода после ИИ.')


def sl_ai_detect():
    items = [('Автодетект', '92%+', 'точность детекта по коду', 'Отличаем ИИ-генерацию от ручного кода напрямую по Git — без плагинов и промпт-коллектора. Работает и для аудита подрядчика.', 'vio'),
             ('Токены', '−35%', 'расхода токенов', 'Норматив токенов на 1 нормо-час и на задачу подсвечивает тех, кто сжигает лимиты впустую.', 'pos'),
             ('Переделки', '−20%', 'переделок (churn)', 'Сгенерированный ИИ-код, который переписали на следующий день, не засчитывается в результат.', 'pos')]
    cards = ''.join(card('<div><div class="k">%s</div><div class="big %s" style="font-size: 110px; margin-top: 18px;">%s</div></div><div class="t">%s</div><div class="x">%s</div>' % (e(a), c, b, e(t), e(p)), 'spread') for a, b, t, p, c in items)
    return S('std', '<div class="grid g3" style="flex: 1;">%s</div>' % cards, 'Автодетект и контроль токенов', 'Контроль бюджета на токены и [[авто-детект ИИ (92%+)]]',
             'Разные модели для ручного и ИИ-кода: точность — на объёме кода за месяц, а для грейда — за 3 месяца.')


def sl_ai_growth():
    items = [('+32%', 'в среднем — когда разработчик начинает использовать скилы'), ('+24%', 'ещё в среднем — когда решает задачу с предварительным планом')]
    left = '<div style="flex: 1; display: flex; flex-direction: column; gap: 22px;">%s</div>' % ''.join(card('<div class="big pos" style="font-size: 120px;">%s</div><div class="x" style="font-size: 28px;">%s</div>' % (a, e(b)), 'spread" style="flex: 1;') for a, b in items)
    right = card('<div class="k">Как разгоняем команду</div>%s' % bl(['**Паттерны сильных** — рекомендации для всей команды', '**Скилы под типовые задачи** — приёмы сильных доступны каждому',
                                                                      '**Шаблон «сначала план, потом код»** — план становится обязательным шагом', '**Спецификации проекта** — контекст собирается один раз',
                                                                      '**Подробно — в UpCore.Mentor:** персональный план роста каждому'], 'lg'), 'acc-b" style="flex: 1.2; justify-content: center;')
    return S('std', '<div class="row" style="flex: 1;">%s%s</div>' % (left, right), 'Рост эффективности · данные Dex', 'Не только измеряем, [[но и разгоняем]]')


def sl_ai_prompts():
    bad = [('11:00', 'Один промпт: задача просто скопирована из Jira'), ('11:00–12:00', 'ИИ работает час'), ('14:00', 'После обеда: «всё не так, переделай»'),
           ('14:00–16:00', 'ИИ работает ещё 2 часа и упирается в дневной лимит'), ('16:00', 'Человек уходит домой')]
    good = ['Постоянно насыщает задачу контекстом проекта', 'Запускает несколько агентов параллельно', 'Следит за токенами и лимитами', 'Не допускает высокого черна: переделок и переписывания кода']
    a = card('<div class="k neg">Неэффективный вайбкодер</div><div class="t">Один промпт и дневной лимит</div>%s' % ''.join(
        '<div style="display: grid; grid-template-columns: 170px minmax(0, 1fr); gap: 14px; padding: 12px 0; border-top: 1px solid var(--line); font-size: 23px; font-family: Onest, sans-serif;"><span class="neg" style="font-family: Mono, monospace; font-size: 19px;">%s</span><span>%s</span></div>' % (x, e(y)) for x, y in bad), '" style="flex: 1;')
    b = card('<div class="k pos">Эффективный разработчик</div><div class="t">Контекст, параллельные агенты, контроль</div>%s' % ''.join(
        '<div style="display: flex; gap: 14px; padding: 12px 0; border-top: 1px solid var(--line); font-size: 23px; font-family: Onest, sans-serif;"><span class="pos" style="font-weight: 800;">✓</span><span>%s</span></div>' % e(x) for x in good), 'acc-b" style="flex: 1;')
    return S('std', '<div class="row" style="flex: 1;">%s%s</div>' % (a, b), 'Промпт-ревью · опционально', 'Промпты — новый язык программирования. [[Им нужно ревью]]',
             'Промпт-коллектор включается по желанию: находит паттерны и антипаттерны, даёт рекомендации и насыщает проект спецификациями и скилами.')


# ---------- Projects
def sl_proj_act():
    left = card('<div class="k">Пример аудита акта</div>%s%s<div style="display: flex; justify-content: space-between; align-items: baseline; border-top: 1px solid var(--line); padding-top: 22px;">'
                '<span style="font-size: 26px; font-family: Onest, sans-serif; color: var(--muted);">К оплате по факту кода</span><b class="neg" style="font-size: 64px;">−640 ч · −43%%</b></div>' % (
                    hbar('Часов в акте подрядчика', '1 500 ч', 100, 'var(--dim)'), hbar('Объективно по коду', '860 ч', 57, 'var(--acc)')), '" style="flex: 1.2; justify-content: center; gap: 30px;')
    right = card('<div class="k">Вместе с актом — отчёт, который можно проверить</div>%s<div class="x">Используйте отчёт UpCore как объективное приложение к акту T&amp;M или Fixed Price: вы оплачиваете только подтверждённый объём инженерной работы в коде.</div>' % bl(
        ['Реальная эффективность каждого разработчика подрядчика в часах', 'Подтверждённый грейд и сложность задач', 'Чистая ценность результирующего кода — без шума и отладки', 'Техдолг и риски по категориям качества']), 'acc-b" style="flex: 1;')
    return S('std', '<div class="row" style="flex: 1;">%s%s</div>' % (left, right), 'Контроль подрядчиков', 'Акт на 1 500 часов? [[Проверьте его по коду]]',
             'При оплате за часы у подрядчика нет стимула ускоряться. UpCore показывает, сколько трудоёмкости в коде на самом деле.')


def sl_proj_x():
    k = [('Эффективность', '74%', 'часы результата по коду против рабочих часов команды', 'amb'), ('MR через ИИ', '16%', 'их эффективность — 120%', 'vio'),
         ('Техдолг', '35%', 'доля критичных дефектов, попавших в ветку main', 'amb'), ('Мэтч команды', '78%', 'соответствие команды технологиям проекта', 'fg')]
    strip = '<div class="grid g4" style="flex: 1;">%s</div>' % ''.join(card('<div class="k">%s</div><div class="big %s" style="font-size: 120px;">%s</div><div class="x" style="font-size: 24px;">%s</div>' % (a, c, b, e(d)), 'spread') for a, b, d, c in k)
    head = ('<div class="card" style="flex-direction: row; align-items: center; gap: 60px;"><div style="flex: 1;"><div class="k" style="color: var(--dim);">Пример отчёта проекта · UpCore Projects</div><div class="t" style="font-size: 44px;">Проект Х</div></div>'
            '<div class="kv"><span>Сложность</span><b>8 / 10</b><span>высоконагруженная архитектура</span></div><div class="kv"><span>Длительность</span><b>1 г. 7 мес</b><span>легаси 0%</span></div>'
            '<div class="kv"><span>Команда</span><b>4 человека</b><span>1 Senior · 2 Middle+ · 1 Junior+</span></div>'
            '<div class="kv" style="text-align: right;"><span>Бюджет проекта</span><b class="acc" style="font-size: 56px;">12,1 млн ₽</b><span>подтверждённая стоимость чистого кода в релизе</span></div></div>')
    return S('std', head + strip, 'Проект на примере', 'Четыре цифры, по которым [[видно здоровье проекта]]', 'Все цифры считаются по коду и раскрываются до MR и строчек в «Глазе».')


def sl_proj_risk():
    td = [('Функциональная пригодность', '273 · 13%', 100), ('Сопровождаемость', '227 · 11%', 83), ('Гибкость', '157 · 7%', 57), ('Надёжность', '39 · 2%', 14), ('Совместимость', '29 · 1%', 11), ('Защищённость', '11 · 1%', 4)]
    a = card('<div class="k">Техдолг · где копится риск</div><div class="x" style="font-size: 20px;">Доля тяжести дефектов, ушедших в main, по категориям качества ISO/IEC 25010.</div>%s' % ''.join(
        hbar(n, v, w, 'var(--amber)') for n, v, w in td), '" style="flex: 1; gap: 16px;')
    tm = [('EF Metadata', '8', '87,3 ч', '81%', 'pos'), ('Multithreading Advanced', '9', '21 ч', '90%', 'pos'), ('java.nio', '8', '16,8 ч', '14%', 'neg'), ('TypeScript Compiler API', '8', '11,9 ч', '0%', 'neg'), ('Spring Security', '9', '23 мин', '0%', 'neg')]
    rows = ''.join('<tr><td style="color: var(--fg);">%s</td><td>%s</td><td>%s</td><td class="%s">%s</td></tr>' % (a_, b_, c_, cls, d_) for a_, b_, c_, d_, cls in tm)
    b = card('<div class="k">Тех-карта · кого не хватает команде</div><div class="x" style="font-size: 20px;">Технологии проекта, их сложность и мэтч команды. Пробелы закрываются ротацией или новой вакансией.</div>'
             '<table class="tbl"><tr><td style="font-family: Mono, monospace; font-size: 17px; color: var(--dim);">ТЕХНОЛОГИЯ</td><td style="font-family: Mono, monospace; font-size: 17px; color: var(--dim);">СЛОЖН.</td><td style="font-family: Mono, monospace; font-size: 17px; color: var(--dim);">В КОДЕ</td><td style="font-family: Mono, monospace; font-size: 17px; color: var(--dim); text-align: right;">МЭТЧ</td></tr>%s</table>' % rows, '" style="flex: 1;')
    return S('std', '<div class="row" style="flex: 1;">%s%s</div>' % (a, b), 'Риски проекта', 'Техдолг по ISO 25010 и [[тех-карта команды]]')


def sl_proj_vendor():
    devs = [('Senior · Backend', 160, 148, 90), ('Middle+ · Backend', 160, 112, 81), ('Middle · Frontend', 160, 72, 64), ('Senior · Frontend', 160, 40, 50)]
    rows = ''
    for n, a, c, rc in devs:
        ef = round(c / a * 100); col = 'var(--pos)' if ef >= 85 else ('var(--amber)' if ef >= 60 else 'var(--neg)')
        rows += ('<div style="padding: 10px 0; border-top: 1px solid var(--line);"><div style="display: grid; grid-template-columns: minmax(0, 1fr) 110px 110px 90px; gap: 10px; font-size: 24px; font-family: Onest, sans-serif;">'
                 '<span>%s</span><span style="text-align: right; color: var(--dim);">%d ч</span><b style="text-align: right;">%d ч</b><b style="text-align: right; color: %s;">%d%%</b></div>'
                 '<div class="hbar" style="margin-top: 8px;"><div class="tr" style="height: 12px;"><div style="width: %d%%; background: %s;"></div></div></div><div style="font-size: 18px; color: var(--dim); margin-top: 4px;">результирующий код %d%%</div></div>') % (n, a, c, col, ef, ef, col, rc)
    left = card('<div style="display: flex; justify-content: space-between;" class="k"><span>Пример отчёта к акту подрядчика</span><span style="color: var(--dim);">октябрь</span></div><div class="t" style="font-size: 36px;">4 разработчика — 4 разные истории</div>'
                '<div style="display: grid; grid-template-columns: minmax(0, 1fr) 110px 110px 90px; gap: 10px; font-family: Mono, monospace; font-size: 16px; color: var(--dim);"><span>РАЗРАБОТЧИК</span><span style="text-align: right;">В АКТЕ</span><span style="text-align: right;">ПО КОДУ</span><span style="text-align: right;">ЭФФ.</span></div>%s'
                '<div style="display: flex; justify-content: space-between; align-items: baseline; border-top: 2px solid var(--acc); padding-top: 16px;"><span style="font-size: 24px; font-family: Onest, sans-serif;">Итого в акте 640 ч · по коду 372 ч</span><b class="neg" style="font-size: 44px;">−268 ч · −42%%</b></div>' % rows, '" style="flex: 1.3;')
    right = '<div style="flex: 1; display: flex; flex-direction: column; gap: 22px;">%s</div>' % ''.join(card('<div class="t" style="font-size: 26px;">%s</div><div class="x">%s</div>' % (e(a), e(b))) for a, b in
                                                                                                   [('Сверка до оплаты', 'Часы в акте сравниваются с фактической трудоёмкостью MR — до оплаты счёта.'), ('Рейтинг подрядчиков', 'Подрядчики сравниваются между собой и с in-house командой.'), ('Аргументы для сметы', 'Объективные нормо-часы — основа для переговоров и следующего бюджета.')])
    return S('std', '<div class="row" style="flex: 1;">%s%s</div>' % (left, right), 'Ежемесячный контроль подрядчиков', 'Каждый разработчик вендора — [[в часах по коду]]')


def sl_proj_scen():
    items = [('CEO · M&A', 'Разовый Due Diligence проекта за 2 дня', 'Оценка реальной стоимости кода и техдолга перед покупкой или приёмкой — без внедрения.'),
             ('CFO · Закупки', 'Ежемесячная верификация актов подрядчиков', 'Сверка часов в акте с фактической трудоёмкостью MR до оплаты счёта.'),
             ('CTO · PMO', 'Управление портфелем и тех-картой команд', 'Прогноз дедлайнов, контроль техдолга по ISO 25010 и закрытие пробелов в стеке.')]
    return S('std', '<div class="grid g3" style="flex: 1;">%s</div>' % ''.join(card('<span class="tag" style="align-self: flex-start; color: var(--acct); border-color: var(--acc);">%s</span><div class="t" style="font-size: 36px;">%s</div><div class="x">%s</div>' % (e(r), e(t), e(p)), 'spread') for r, t, p in items),
             'Сценарии для C-level', 'Три способа [[взять бюджет под контроль]]')


# ---------- Mentor
def sl_mentor_signals():
    groups = [('ЭФФЕКТИВНОСТЬ', 'var(--acct)', [('17%', 'эффективности — время сильно выше объективной сложности', 'neg'), ('45%', 'результирующего кода — остальное переписано', 'amb')]),
              ('ИИ', 'var(--violet)', [('23%', 'промптов в духе «всё переделай»', 'neg'), ('+129%', 'перерасход токенов на 1 час к среднему в компании', 'amb')]),
              ('ТЕХДОЛГ', 'var(--fg)', [('7', 'критических логических ошибок и уязвимостей', 'neg'), ('7 → 2,4', 'резкое падение качества кода', 'neg'),
                                         ('52%', 'выявленных дефектов попадают в main', 'neg'), ('3', 'нетипичных технологии или паттерна', 'amb')])]
    cols = ''.join(card('<div class="k" style="color: %s;">%s</div>%s' % (c, g, ''.join('<div class="sig" style="flex-direction: column; align-items: flex-start; gap: 4px; padding: 12px 20px; flex: 1; justify-content: center;"><b class="%s" style="font-size: 38px; line-height: 1;">%s</b><span>%s</span></div>' % (
        cl, v, e(t)) for v, t, cl in items)), '" style="gap: 14px;') for g, c, items in groups)
    return S('std', '<div class="grid g3" style="flex: 1;">%s</div>' % cols, 'Приоритизация ревью', 'Тимлид видит только то, что [[требует внимания]]',
             'Mentor разбирает каждый MR, задачи и промпты и поднимает наверх сигналы — остальное ревьюит сам.')


def sl_mentor_example():
    cats = [('Функциональная пригодность', 31), ('Сопровождаемость', 24), ('Гибкость', 11), ('Совместимость', 4)]
    left = card('<div class="k" style="color: var(--dim);">Демо UpCore · вкладка «Качество» · анализ код-ревью</div><div class="t" style="font-size: 40px;">Лукьянов Александр · Backend, C#</div><div class="big" style="font-size: 150px; margin: 10px 0;"><span class="neg">3,2</span> <span style="color: var(--dim);">→</span> <span class="pos">8,0</span></div>%s%s'
                '<div class="x">Рост в 2,5 раза — за 30,9 часа исправлений, это 7%% рабочего времени.</div>' % (
                    hbar('До ревью', '3,2 / 10', 32, 'var(--neg)'), hbar('После исправлений', '8,0 / 10', 80, 'var(--pos)')), '" style="flex: 1.2; gap: 24px;')
    right = card('<div style="display: flex; gap: 40px;"><div class="kv"><span>MR разобрано</span><b>47 <span style="font-size: 22px; color: var(--dim);">из 47</span></b></div><div class="kv"><span>На исправления</span><b>30,9 ч</b></div></div>'
                 '<div class="k" style="margin-top: 10px;">Что исправлено</div>%s<div class="fact">Повторяющиеся дефекты автоматически собираются в персональный план обучения разработчика.</div>' % ''.join(
                     hbar(n, '%d дефектов' % v, round(v / 31 * 100), 'var(--pos)') for n, v in cats), 'acc-b" style="flex: 1; gap: 16px;')
    return S('std', '<div class="row" style="flex: 1;">%s%s</div>' % (left, right), 'Наставник на примере', 'Качество кода: [[3,2 → 8,0]] после разбора с наставником')


def sl_mentor_ai():
    a = card('<div class="k neg">Как было · антипаттерн</div><div class="t">Один промпт и дневной лимит</div>%s' % ''.join(
        '<div style="display: grid; grid-template-columns: 90px minmax(0, 1fr); gap: 14px; padding: 12px 0; border-top: 1px solid var(--line); font-size: 23px; font-family: Onest, sans-serif;"><span class="neg" style="font-family: Mono, monospace; font-size: 19px;">%s</span><span>%s</span></div>' % (x, e(y))
        for x, y in [('11:00', 'Один промпт: задача скопирована из Jira'), ('14:00', 'После обеда: «всё не так, переделай»'), ('16:00', 'ИИ упёрся в дневной лимит — человек ушёл домой')]), '" style="flex: 1;')
    b = card('<div class="k pos">Что советует Mentor · паттерн сильных</div><div class="t">Контекст, план, параллельные агенты</div>%s' % bl(
        ['Насыщает задачу контекстом проекта', 'Сначала строит план решения', 'Запускает несколько агентов параллельно', 'Следит за токенами и лимитами']), 'acc-b" style="flex: 1;')
    c = card('<div class="k">И сам добавляет в проект</div>%s<div style="display: flex; gap: 20px; margin-top: auto;"><div><div class="big pos s">+32%%</div><div class="x" style="font-size: 18px;">со скилами</div></div><div><div class="big pos s">+24%%</div><div class="x" style="font-size: 18px;">с планом</div></div></div>' % bl(
        ['**Спецификации проекта** — контекст один раз', '**Скилы под типовые задачи**', '**«Сначала план, потом код»**', '**Рекомендации по промптам** каждому']), '" style="flex: 1;')
    return S('std', '<div class="row" style="flex: 1;">%s%s%s</div>' % (a, b, c), 'ИИ-наставник', 'Учим команду [[работать с ИИ]], а не просто измеряем',
             'Промпты — новый язык программирования: Mentor ревьюит их как код и видит, какие задачи с ИИ дали результат.')


def sl_mentor_ipr():
    steps = [('ШАГ 01', 'Диагностика в Grade', 'Система фиксирует просадку фактора (например, **Архитектурная сложность 3,1 / 10**) и падение качества кода.'),
             ('ШАГ 02', 'Рекомендации в MR', 'Mentor подсвечивает антипаттерны прямо в ходе ревью и предлагает готовые архитектурные скилы проекта.'),
             ('ШАГ 03', 'Контроль прогресса', 'Тимлид и L&D видят рост метрики от спринта к спринту — без ручного микроменеджмента.')]
    return S('std', '<div class="grid g3" style="flex: 1;">%s</div>' % ''.join(card('<div><div class="k">%s</div><div class="big" style="font-size: 120px; margin-top: 14px;">%02d</div></div><div class="t" style="font-size: 36px;">%s</div><div class="x" style="font-size: 24px;">%s</div>' % (a, i + 1, e(b), rich(c)), 'spread acc-b' if i == 0 else 'spread') for i, (a, b, c) in enumerate(steps)),
             'От грейда к плану роста', 'Как просадка в грейде превращается [[в план роста (ИПР)]]')


# ---------------------------------------------------------------- состав презентаций
GRADE_ST = [('96%', 'совпадение с оценкой Senior на 300 000+ MR'), ('50+', 'факторов грейда, главный — эффективность в часах'), ('1500+', 'разработчиков проанализировано'), ('1 день', 'до первых результатов')]
AI_ST = [('до ×2–3', 'ускорение Senior на типовых задачах'), ('92%+', 'точность детекта ИИ-кода'), ('−35%', 'снижение пустого расхода токенов'), ('−20%', 'сокращение переделок (churn) после ИИ')]
PROJ_ST = [('96%', 'точность от экспертной оценки на 300 000+ MR'), ('50+', 'факторов в оценке каждого MR'), ('до −43%', 'выявление переплат по актам'), ('1 день', 'до первых результатов')]


def deck_platform(v):
    cover = s_cover('platform', 'Цифровой тимлид [[автоматически оценивает эффективность]] вашей разработки',
                    'Математическая модель переводит код в реальные человеко-часы и рубли — без тайм-трекеров и отчётов.', 'Презентация для CTO · платформа UpCore',
                    ['CTO', 'CIO', 'CFO', 'HRD', 'тимлиды'], '14-company.png')
    cta = s_cta('Проведите бесплатный пилот на 2–3 репозиториях', 'Покажем реальную трудоёмкость проектов, грейды команды и окупаемость ИИ по истории вашего кода за последние 6 месяцев — через 1 час после подключения.')
    S1 = [cover, sl_problem(), sl_how(), sl_platform4(compact=True), sl_econ(), sl_security(), cta]
    S2 = [cover, sl_problem(), sl_how(), sl_160(), sl_numbers(), sl_platform4(), sl_screen('14-company.png', 'Демо UpCore', 'Вся компания — [[на одном экране]]', None,
          ['Эффективность за месяц и за 3 месяца', 'Динамика против рынка и топ-20%', 'Проекты, специалисты и грейды']), sl_model4(), sl_econ(), sl_security(), sl_pilot(), cta]
    S3 = [cover, sl_problem(), sl_how(), sl_160(), sl_model4(), sl_numbers(), s_section('01', 'Платформа: [[четыре продукта]] на одном коннекте к Git'), sl_platform4(),
          sl_grade_rating(), sl_ai_gap(), sl_proj_act(), sl_mentor_ipr(),
          sl_gallery(['14-company.png', '11-insights.png', '01-level.png', '10-project.png'], 'Демо UpCore', 'Как это выглядит [[в продукте]]'),
          s_section('02', 'Экономика и [[безопасность]]'), sl_econ(), sl_security(), sl_faq(bp.GRADE_FAQ[:2] + bp.PROJ_FAQ[:1] + bp.AI_FAQ2[:1]), sl_pilot(), cta]
    return {'1': S1, '2': S2, '3': S3, '4': S2}[v]


def deck_grade(v):
    cover = s_cover('grade', 'Объективный грейд и [[рейтинг команды]] каждый месяц',
                    'Автоматический расчёт выработки в нормо-часах и подтверждённый грейд Junior–Senior по 50+ параметрам кода из Git.', 'Презентация для CTO и HRD · UpCore Grade',
                    ['CTO', 'HRD', 'тимлиды', 'разработчики'], '01-level.png')
    cta = s_cta('Узнайте реальные грейды вашей команды за 1 час', 'Бесплатный пилот на 2–3 репозиториях с ретро-анализом истории кода за последние 6 месяцев.')
    st = S('std', stats(GRADE_ST, 4), 'UpCore Grade в цифрах', 'Грейд, который [[можно проверить]]', 'Эффективность — каждый месяц, грейд — за 3 месяца, рейтинг — каждый месяц. Всё автоматически: нужен только код.', kind='statsS')
    S1 = [cover, sl_grade_profile(False), sl_grade_factors(), sl_grade_rating(), sl_roles(bp.GRADE_ROLES_V2, 'Одна цифра для CTO, HR, тимлида и разработчика'), sl_security(), cta]
    S2 = [cover, st, sl_grade_profile(), sl_grade_factors(), sl_grade_rating(),
          sl_screen('09-rating.png', 'Демо UpCore', 'Рейтинг [[по компании, стеку и проекту]]', None, ['Изменение позиции за месяц', 'Эффективность, грейд и результирующий код', 'Зона риска — фокус для ревью и ротации']),
          sl_grade_value(), sl_roles(bp.GRADE_ROLES_V2, 'Одна цифра для CTO, HR, тимлида и разработчика'), sl_faq(bp.GRADE_FAQ), sl_security(), cta]
    S3 = [cover, st, sl_problem(), sl_how(), sl_grade_profile(), sl_grade_factors(), sl_model4(), sl_grade_rating(),
          sl_gallery(['01-level.png', '02-efficiency.png', '03-team.png', '09-rating.png'], 'Демо UpCore', 'Грейд и рейтинг [[в продукте]]'),
          sl_screen('12-timesheet.png', 'Демо UpCore', 'Табель эффективности [[по месяцам]]', None, ['Грейд и эффективность каждого по месяцам', 'Видно, кто растёт, а кто проседает', 'Без тайм-трекеров — только код']),
          sl_grade_value(), sl_roles(bp.GRADE_ROLES_V2, 'Одна цифра для CTO, HR, тимлида и разработчика'), sl_faq(bp.GRADE_FAQ),
          s_section('UpCore · платформа', 'Вместе с Grade — [[вся платформа UpCore]]', 'Один read-only коннект к Git — и все четыре продукта работают на одних данных: грейды, ИИ, проекты и наставничество.'), sl_platform4(compact=True), sl_econ(), sl_security(), sl_pilot(), cta]
    return {'1': S1, '2': S2, '3': S3, '4': S2}[v]


def deck_ai(v):
    cover = s_cover('ai', 'Реальная эффективность [[внедрения ИИ]] в вашу разработку',
                    'Измеряем фактическую экономию часов от ИИ-ассистентов, долю выжившего ИИ-кода и окупаемость лицензий по каждому разработчику.', 'Презентация для CTO и CFO · UpCore AI',
                    ['CTO', 'CFO', 'тимлиды', 'разработчики'], '02-efficiency.png')
    cta = s_cta('Посчитайте реальный эффект ИИ в своей команде', 'Бесплатный пилот на 2–3 репозиториях: сравним время «с ИИ» и «вручную» по истории кода за 6 месяцев.')
    st = S('std', stats(AI_ST, 4), 'UpCore AI в цифрах', 'Отдача от ИИ — [[в часах и рублях]]', 'Без промпт-коллектора: модель определяет ИИ-код и считает эффект только по коду из Git.', kind='statsS')
    S1 = [cover, sl_ai_gap(), sl_ai_roi(), sl_ai_detect(), sl_ai_growth(), sl_security(), cta]
    S2 = [cover, st, sl_ai_gap(), sl_ai_roi(), sl_ai_detect(), sl_ai_growth(), sl_ai_prompts(),
          sl_screen('14-company.png', 'Демо UpCore', 'ИИ-эффективность [[всей компании]]', None, ['Доля MR с ИИ и их эффективность', 'Сколько часов ИИ сэкономил и во что обошёлся', 'Динамика внедрения по месяцам']),
          sl_roles(bp.AI_ROLES_V2, 'Одни данные об ИИ для CTO, финансов, тимлида и разработчика'), sl_faq(bp.AI_FAQ2), sl_security(), cta]
    S3 = [cover, st, sl_ai_gap(), sl_how(), sl_ai_roi(), sl_ai_detect(), sl_ai_growth(), sl_ai_prompts(),
          sl_gallery(['14-company.png', '02-efficiency.png', '05-quality.png', '04-code.png'], 'Демо UpCore', 'ИИ в цифрах [[в продукте]]'),
          sl_model4(), sl_roles(bp.AI_ROLES_V2, 'Одни данные об ИИ для CTO, финансов, тимлида и разработчика'), sl_faq(bp.AI_FAQ2),
          s_section('UpCore · платформа', 'Вместе с AI — [[вся платформа UpCore]]', 'Один read-only коннект к Git — и все четыре продукта работают на одних данных: грейды, ИИ, проекты и наставничество.'), sl_platform4(compact=True), sl_mentor_ai(), sl_econ(), sl_security(), sl_pilot(), cta]
    return {'1': S1, '2': S2, '3': S3, '4': S2}[v]


def deck_projects(v):
    cover = s_cover('projects', 'Бюджет проекта и контроль подрядчиков — [[в часах и рублях]]',
                    'Объективная стоимость разработки, сверка актов подрядчиков, техдолг по ISO/IEC 25010 и радар срыва сроков — напрямую по коду из Git.', 'Презентация для CEO, CFO и CTO · UpCore Projects',
                    ['CEO', 'CFO', 'CTO', 'PMO'], '10-project.png')
    cta = s_cta('Проверьте, сколько на самом деле стоит ваш проект', 'Бесплатный пилот на 2–3 репозиториях: объективный бюджет проекта по коду — полгода истории за 1 час.')
    st = S('std', stats(PROJ_ST, 4), 'UpCore Projects в цифрах', 'Сколько [[на самом деле]] стоит ваш проект', 'Объективные нормо-часы по коду — основа для бюджета, приёмки работ и переговоров с подрядчиками.', kind='statsS')
    S1 = [cover, sl_proj_act(), sl_proj_x(), sl_proj_scen(), sl_proj_vendor(), sl_security(), cta]
    S2 = [cover, st, sl_proj_act(), sl_proj_x(), sl_proj_risk(), sl_proj_vendor(),
          sl_screen('13-losses.png', 'Демо UpCore', 'Финансовые потери [[в рублях]]', None, ['Потери по каждому специалисту за 3 месяца', 'Реальная ставка за час результата', 'Эффективные часы против рабочих']),
          sl_proj_scen(), sl_faq(bp.PROJ_FAQ), sl_security(), cta]
    S3 = [cover, st, sl_problem(), sl_how(), sl_proj_act(), sl_proj_x(), sl_proj_risk(), sl_proj_vendor(),
          sl_gallery(['10-project.png', '13-losses.png', '12-timesheet.png', '08-tech.png'], 'Демо UpCore', 'Проекты и подрядчики [[в продукте]]'),
          sl_proj_scen(), sl_roles(bp.PROJ_ROLES, 'Прозрачность, выгодная заказчику и команде'), sl_model4(), sl_faq(bp.PROJ_FAQ),
          s_section('UpCore · платформа', 'Вместе с Projects — [[вся платформа UpCore]]', 'Один read-only коннект к Git — и все четыре продукта работают на одних данных: грейды, ИИ, проекты и наставничество.'), sl_platform4(compact=True), sl_econ(), sl_security(), sl_pilot(), cta]
    return {'1': S1, '2': S2, '3': S3, '4': S2}[v]


def deck_mentor(v):
    cover = s_cover('mentor', 'ИИ-наставник [[для каждого разработчика]]',
                    'Автоматическое ревью каждого MR, задач и промптов: снимает с тимлидов до 80% рутинных проверок и формирует индивидуальный план развития инженера.', 'Презентация для CTO и тимлидов · UpCore Mentor',
                    ['CTO', 'тимлиды', 'L&D', 'разработчики'], '05-quality.png')
    cta = s_cta('Дайте каждому разработчику своего наставника', 'Подключите репозиторий — готовый разбор системных ошибок и промптов вашей команды по истории за 6 месяцев уже через 1 час.')
    st = S('std', stats(bp.MENTOR_STATS3, 4), 'UpCore Mentor в цифрах', 'Наставник, который [[разгружает тимлида]]', 'Тимлид глубоко проверяет лишь 5–10% изменений. Mentor ревьюит 100% MR и приносит тимлиду только важное.', kind='statsS')
    S1 = [cover, st, sl_mentor_signals(), sl_mentor_example(), sl_mentor_ipr(), sl_security(), cta]
    S2 = [cover, st, sl_mentor_signals(), sl_mentor_ai(), sl_mentor_example(), sl_mentor_ipr(),
          sl_screen('05-quality.png', 'Демо UpCore', 'ИИ-ревью [[каждого MR]]', None, ['Дефекты по тяжести и категориям качества', 'Время на исправления', 'Качество кода до и после ревью']),
          sl_roles(bp.MENTOR_ROLES, 'Наставник, который нужен каждому в команде'), sl_faq(bp.MENTOR_FAQ), sl_security(), cta]
    S3 = [cover, st, sl_mentor_signals(), sl_mentor_ai(), sl_mentor_example(), sl_grade_profile(), sl_mentor_ipr(), sl_ai_growth(),
          sl_gallery(['05-quality.png', '04-code.png', '01-level.png', '07-dynamics.png'], 'Демо UpCore', 'Наставник [[в продукте]]'),
          sl_roles(bp.MENTOR_ROLES, 'Наставник, который нужен каждому в команде'), sl_faq(bp.MENTOR_FAQ),
          s_section('UpCore · платформа', 'Вместе с Mentor — [[вся платформа UpCore]]', 'Один read-only коннект к Git — и все четыре продукта работают на одних данных: грейды, ИИ, проекты и наставничество.'), sl_platform4(compact=True), sl_model4(), sl_security(), sl_pilot(), cta]
    return {'1': S1, '2': S2, '3': S3, '4': S2}[v]


DECKS = [('01-platform', 'Platform', 'platform', deck_platform), ('02-grade', 'Grade', 'grade', deck_grade), ('03-ai', 'AI', 'ai', deck_ai),
         ('04-projects', 'Projects', 'projects', deck_projects), ('05-mentor', 'Mentor', 'mentor', deck_mentor)]
VARIANTS = [('1', 'short', 'короткая'), ('2', 'medium', 'средняя'), ('3', 'long', 'длинная'), ('4', 'light', 'светлая')]


def render_deck(key, slides, light, title):
    a1, a2, a3 = ACC[key]
    css = CSS % {'F': FONTS, 'I': IMG, 'A1': a1, 'A2': a2, 'A3': a3}
    prod = 'UpCore' if key == 'platform' else 'UpCore ' + NAME[key][1]
    out = []
    n = len(slides)
    for i, s in enumerate(slides, 1):
        k = s['kind']
        cls = {'cover': 'cover', 'sec': 'sec', 'cta': 'ctaS', 'std': '', 'statsS': 'statsS'}[k]
        deco = CHEVRON if k in ('cover', 'sec', 'cta') else ''
        side = ''
        if k == 'cover':
            if light:
                deco = '<div class="band"></div>'
            if s.get('side'):
                side = ('<div style="position: absolute; right: 110px; top: 50%%; transform: translateY(-54%%); width: 720px; height: 470px; display: flex;">%s</div>' % screen(s['side'], style='flex: 1;'))
                s = dict(s, html=s['html'].replace('<h1>', '<h1 style="max-width: 960px; font-size: 80px;">').replace('<p class="sub">', '<p class="sub" style="max-width: 900px; font-size: 28px;">'))
        foot = ('<div class="foot"><div class="lg"><i></i><span>%s · презентация для руководителей ИТ</span></div><div>up-core.ru · office@dex-it.ru · %02d / %02d</div></div>' % (e(prod), i, n))
        out.append('<section class="slide %s">%s%s<div class="content">%s</div>%s</section>' % (cls, deco, side, s['html'], foot))
    return ('<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>%s</title><style>%s</style></head><body class="%s">%s</body></html>' % (
        e(title), css, 'light' if light else '', '\n'.join(out)))


def main():
    os.makedirs(BUILD, exist_ok=True)
    made = []
    for folder, en, key, fn in DECKS:
        for v, vn, vru in VARIANTS:
            slides = fn(v)
            name = 'UpCore-%s-%s-%s' % (en, v, vn)
            title = '%s — %s презентация' % ('UpCore' if key == 'platform' else 'UpCore ' + NAME[key][1], vru)
            open(os.path.join(BUILD, name + '.html'), 'w').write(render_deck(key, slides, v == '4', title))
            made.append((folder, name, len(slides)))
    with open(os.path.join(BUILD, 'manifest.txt'), 'w') as f:
        for folder, name, n in made:
            f.write('%s %s %d\n' % (folder, name, n))
    for folder, name, n in made:
        print(folder, name, n, 'слайдов')


if __name__ == '__main__':
    main()
