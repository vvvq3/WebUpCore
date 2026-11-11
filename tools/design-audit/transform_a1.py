"""A1 «Консоль»: перенос UX-правок без изменения наполнения."""
import re, sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()
IDS = {
    'd4c2740f35d5c35e496626ba187a1752': 'f43be9baafd8829d6b16ffe80acc1058',
    'afdf675f8bedfead15e609fdb13aa49b': 'bafb77824e1d39daa3b420922830060f',
    '9cba81e6ca23a0c1263f23c20f8003d1': 'd8917cd1a1d057105dfc6c6f648403a0',
    '6c6353e4a251a57072c1e2bf94de7c76': '078b103a94164c4d026935ab418de02e',
    '13400136e70882d874f7a2528f15026e': '8e065b6e6d912548df6ac04a1d4801aa',
    '40525ebf8d2111c88f08ef46f71635b4': '1b955fad8df5479c19c6d27c0152e677',
    'd7c8fafeeb9ade6b82b3400769fbe356': '15b42da0691260ad6b49fb37e4d648bf',
    '2696bde9510556b393f5f92bee142467': 'd4215a5dcf98764dc2068afdfb82ca2f',
    '43a5f658acd56dde7b15581b6f106e43': '00ee65e2d395b5fdbfdbabcfe4a1b3ef',
}
for a, b in IDS.items():
    s = s.replace(a, b)
assert '/_blob/' in s and not any(k in s for k in IDS)

def rep(old, new):
    global s
    n = s.count(old)
    assert n == 1, f'{old[:80]!r}: {n}'
    s = s.replace(old, new)

CSS = """.uc-mob{display:none}
.uc-chips{display:flex;gap:6px;overflow-x:auto;scrollbar-width:none}
@media (max-width:820px){
.uc-desk{display:none!important}
.uc-mob{display:inline-flex!important}
.uc-hdr{padding:12px 16px!important;gap:10px!important}
.uc-reg{padding:0 14px!important}
.uc-hero{flex-direction:column!important;align-items:stretch!important;gap:18px!important;padding-top:16px!important}
.uc-col1{display:contents!important}
.uc-col1>*{order:3}
.uc-col1>.uc-o1{order:1}
.uc-hero>.uc-o2{order:2}
.uc-full{flex:1 1 100%!important;justify-content:center}
}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important}}
</style>"""
rep('</style>', CSS)
rep('<header style="max-width: 1280px; margin: 0 auto; padding: 24px 32px; display: flex; flex-wrap: wrap; align-items: center; gap: 24px; justify-content: space-between;">',
    '<header class="uc-hdr" style="max-width: 1280px; margin: 0 auto; padding: 24px 32px; display: flex; align-items: center; gap: 24px; justify-content: space-between;">')
rep('<nav aria-label="Основное меню" style="display: flex; flex-wrap: wrap; gap: 6px; font-size: 15px;">',
    '<nav class="uc-desk" aria-label="Основное меню" style="display: flex; flex-wrap: wrap; gap: 6px; font-size: 15px;">')
rep('<a href="#en" style="color: rgba(255,255,255,0.78); text-decoration: none; font-family: \'JetBrains Mono\', monospace; font-size: 13px; padding: 12px 8px;">RU / EN</a>',
    '<a class="uc-desk" href="#en" style="color: rgba(255,255,255,0.78); text-decoration: none; font-family: \'JetBrains Mono\', monospace; font-size: 13px; padding: 12px 8px;">RU / EN</a>')
BURGER = '''<a class="uc-reg" href="https://demo.up-core.ru/" style="display: inline-flex; align-items: center; min-height: 44px; padding: 0 20px; border-radius: 14px; background: #63D5FF; color: #0D0C15; font-weight: 700; text-decoration: none;">Регистрация</a>
<button class="uc-mob" type="button" aria-label="Открыть меню" aria-expanded="{{menuOpen}}" onClick="{{toggleMenu}}" style="width: 44px; height: 44px; align-items: center; justify-content: center; border-radius: 12px; border: 1px solid rgba(255,255,255,0.22); background: transparent; color: #FFFFFF; cursor: pointer;"><svg aria-hidden="true" viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"></path></svg></button>
</div>
</header>
<sc-if value="{{menuOpen}}" hint-placeholder-val="{{false}}">
<nav aria-label="Мобильное меню" style="margin: 0 16px 8px; padding: 8px; border-radius: 18px; background: #1A1925; display: flex; flex-direction: column; font-size: 17px;">
<a href="#grade" style="color: #FFFFFF; text-decoration: none; padding: 14px 12px;">UpCore Grade</a>
<a href="#ai" style="color: #FFFFFF; text-decoration: none; padding: 14px 12px;">UpCore AI</a>
<a href="#projects" style="color: #FFFFFF; text-decoration: none; padding: 14px 12px;">UpCore Projects</a>
<a href="#mentor" style="color: #FFFFFF; text-decoration: none; padding: 14px 12px;">UpCore Mentor</a>
<a href="#method" style="color: #FFFFFF; text-decoration: none; padding: 14px 12px;">Методология</a>
<a href="#blog" style="color: #FFFFFF; text-decoration: none; padding: 14px 12px;">Блог</a>
<a href="#en" style="color: rgba(255,255,255,0.75); text-decoration: none; padding: 14px 12px;">English</a>
</nav>
</sc-if>'''
rep('''<a href="https://demo.up-core.ru/" style="display: inline-flex; align-items: center; min-height: 44px; padding: 0 20px; border-radius: 14px; background: #63D5FF; color: #0D0C15; font-weight: 700; text-decoration: none;">Регистрация</a>
</div>
</header>''', BURGER)
rep('<section id="top" style="max-width: 1280px; margin: 0 auto; padding: 40px 32px 88px; display: flex; flex-wrap: wrap; gap: 48px; align-items: center;">',
    '<section id="top" class="uc-hero" style="max-width: 1280px; margin: 0 auto; padding: 40px 32px 88px; display: flex; flex-wrap: wrap; gap: 48px; align-items: center;">')
rep('<div style="flex: 1 1 440px; min-width: 0; display: flex; flex-direction: column; gap: 26px;">',
    '<div class="uc-col1" style="flex: 1 1 500px; min-width: 0; display: flex; flex-direction: column; gap: 26px;">')
rep('<div style="display: inline-flex; align-self: flex-start; align-items: center; gap: 10px; padding: 8px 14px; border-radius: 999px; border: 1px solid rgba(99,213,255,0.35);',
    '<div class="uc-o1" style="display: inline-flex; align-self: flex-start; align-items: center; gap: 10px; padding: 8px 14px; border-radius: 999px; border: 1px solid rgba(99,213,255,0.35);')
rep('<h1 style="margin: 0; font-size: clamp(40px, 4.8vw, 72px);', '<h1 class="uc-o1" style="margin: 0; font-size: clamp(36px, 4.3vw, 64px);')
rep('<a href="https://demo.up-core.ru/" style="display: inline-flex; align-items: center; min-height: 52px; padding: 0 26px; border-radius: 16px; background: #63D5FF;',
    '<a class="uc-full" href="https://demo.up-core.ru/" style="display: inline-flex; align-items: center; min-height: 52px; padding: 0 26px; border-radius: 16px; background: #63D5FF;')
rep('<a href="mailto:office@dex-it.ru" style="display: inline-flex; align-items: center; min-height: 52px; padding: 0 26px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.22);',
    '<a class="uc-full" href="mailto:office@dex-it.ru" style="display: inline-flex; align-items: center; min-height: 52px; padding: 0 26px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.22);')
rep('<div style="flex: 1.35 1 560px; min-width: 0;">', '<div class="uc-o2" style="flex: 1.2 1 520px; min-width: 0;">')
rep('<div role="tablist" aria-label="Экраны продукта" style="display: flex; flex-wrap: wrap; gap: 6px;">', '<div class="uc-chips" role="tablist" aria-label="Экраны продукта">')
rep('style="position: relative; overflow: hidden; min-height: 40px; padding: 0 12px;', 'style="position: relative; overflow: hidden; flex: 0 0 auto; white-space: nowrap; min-height: 44px; padding: 0 12px;')
rep('style="min-height: 40px; padding: 0 12px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.14);', 'style="flex: 0 0 auto; white-space: nowrap; min-height: 44px; padding: 0 12px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.14);')
rep('<span class="uc-prog" style="position: absolute; left: 0; bottom: 0; height: 2px; width: 100%; background: #63D5FF;"></span>',
    '<sc-if value="{{running}}" hint-placeholder-val="{{true}}"><span class="uc-prog" style="position: absolute; left: 0; bottom: 0; height: 2px; width: 100%; background: #63D5FF;"></span></sc-if>')
rep('''<div style="font-size: 17px; font-weight: 700;">{{cur.title}} <span style="font-weight: 400; color: rgba(255,255,255,0.7); font-family: 'Onest', sans-serif; font-size: 15px;">— {{cur.caption}}</span></div>''',
    '''<div style="display: flex; align-items: center; justify-content: space-between; gap: 12px;"><div style="font-size: 17px; font-weight: 700; min-width: 0;">{{cur.title}} <span style="font-weight: 400; color: rgba(255,255,255,0.72); font-family: 'Onest', sans-serif; font-size: 15px;">— {{cur.caption}}</span></div><button type="button" onClick="{{togglePlay}}" aria-label="{{playLabel}}" style="flex: 0 0 auto; width: 44px; height: 44px; border-radius: 50%; border: 1px solid rgba(255,255,255,0.22); background: transparent; color: #FFFFFF; display: flex; align-items: center; justify-content: center; cursor: pointer;"><sc-if value="{{playing}}" hint-placeholder-val="{{true}}"><svg aria-hidden="true" viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><rect x="6" y="5" width="4" height="14" rx="1"></rect><rect x="14" y="5" width="4" height="14" rx="1"></rect></svg></sc-if><sc-if value="{{paused}}" hint-placeholder-val="{{false}}"><svg aria-hidden="true" viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M8 5v14l11-7z"></path></svg></sc-if></button></div>''')
rep('viewBox="0 0 300 300" role="img" aria-label="Звезда грейда: радар', 'viewBox="-14 -6 328 312" role="img" aria-label="Звезда грейда: радар')
rep('<g font-family="Onest" font-size="10" fill="rgba(255,255,255,0.72)" text-anchor="middle"><text x="150" y="28">Эффективность</text><text x="236" y="46">Задачи</text><text x="274" y="104">Качество</text><text x="276" y="198">Ревью</text><text x="236" y="262">Архитектура</text><text x="150" y="282">Сложность</text><text x="64" y="262">Технологии</text><text x="26" y="198">Тех-мэтч</text><text x="26" y="104">Результат</text><text x="64" y="46">Баги</text></g>',
    '<g font-family="Onest" font-size="15" fill="rgba(255,255,255,0.82)" text-anchor="middle"><text x="150" y="24">Эффект.</text><text x="240" y="42">Задачи</text><text x="282" y="104">Качество</text><text x="284" y="200">Ревью</text><text x="240" y="268">Архит.</text><text x="150" y="288">Сложн.</text><text x="60" y="268">Технол.</text><text x="16" y="200">Мэтч</text><text x="16" y="104">Итог</text><text x="60" y="42">Баги</text></g>')
rep('constructor(props) { super(props); this.state = { idx: 0 }; }', 'constructor(props) { super(props); this.state = { idx: 0, playing: true, menu: false }; }')
rep('componentDidMount() { this.start(); }', "reduced() { try { return window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) { return false; } }\n  componentDidMount() { if (this.reduced()) this.setState({ playing: false }); else this.start(); }")
rep('pick: () => { this.setState({ idx: i }); this.start(); }', 'pick: () => { this.setState({ idx: i }); if ((this.state || {}).playing) this.start(); }')
rep('return { slides, cur };', '''const st = this.state || {};
    return {
      slides, cur, playing: !!st.playing, paused: !st.playing, running: !!st.playing,
      playLabel: st.playing ? 'Остановить автопрокрутку' : 'Включить автопрокрутку',
      togglePlay: () => { if (st.playing) { clearInterval(this.timer); this.setState({ playing: false }); } else { this.start(); this.setState({ playing: true }); } },
      menuOpen: !!st.menu, toggleMenu: () => this.setState((x) => ({ menu: !x.menu }))
    };''')
rep('<title>UpCore — A1 Консоль</title>', '<title>UpCore — 3 Консоль (A1)</title>')
open(p, 'w', encoding='utf-8').write(s)
print('A1 ok')
