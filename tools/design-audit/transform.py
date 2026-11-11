"""Перенос наполнения A1 в макеты нового холста: точечные замены с проверкой количества вхождений."""
import re, sys

D = sys.argv[1]
IDS = {
    # холст топ-3 → новый холст
    'bf93e9d9d986cce0fe07717349a58372': 'f43be9baafd8829d6b16ffe80acc1058',
    'e5d3c964350fd7d4aa2972071c2dfc5f': 'b75df264cd5b3518da714c1bfe73295a',
    '10523aa730bf9b6cf46e6f20733ff512': 'bafb77824e1d39daa3b420922830060f',
    'b3cfb286fc63dac12b16ea1c9396363b': 'd8917cd1a1d057105dfc6c6f648403a0',
    '33df02474899e07db8fd39fb946dc103': '078b103a94164c4d026935ab418de02e',
    '6df194d7dfb12cde45e704a49b987210': '8e065b6e6d912548df6ac04a1d4801aa',
    'e676139660e4ea00b101c92ec42793d7': '1b955fad8df5479c19c6d27c0152e677',
    'fe9e6754803798391fc83dcc562c7e25': '15b42da0691260ad6b49fb37e4d648bf',
    '556228af3ab2ef50bde7808479c72f26': '93d0ed58db776563015d10b8660132e6',
    'aaaadea38505d8b9831a28ae186670c4': 'dd9427e92ed40645720e9a95710530d7',
    # холст концептов → новый холст
    'd4c2740f35d5c35e496626ba187a1752': 'f43be9baafd8829d6b16ffe80acc1058',
    '75fbf6048ce4882bb5f39aa3202b0f6d': 'b75df264cd5b3518da714c1bfe73295a',
    'afdf675f8bedfead15e609fdb13aa49b': 'bafb77824e1d39daa3b420922830060f',
    '9cba81e6ca23a0c1263f23c20f8003d1': 'd8917cd1a1d057105dfc6c6f648403a0',
    '6c6353e4a251a57072c1e2bf94de7c76': '078b103a94164c4d026935ab418de02e',
    '13400136e70882d874f7a2528f15026e': '8e065b6e6d912548df6ac04a1d4801aa',
    '40525ebf8d2111c88f08ef46f71635b4': '1b955fad8df5479c19c6d27c0152e677',
    'd7c8fafeeb9ade6b82b3400769fbe356': '15b42da0691260ad6b49fb37e4d648bf',
    '2696bde9510556b393f5f92bee142467': 'd4215a5dcf98764dc2068afdfb82ca2f',
    '43a5f658acd56dde7b15581b6f106e43': '00ee65e2d395b5fdbfdbabcfe4a1b3ef',
}
A1_H1 = 'Цифровой тимлид, который проверяет <span style="color: {c};">100%</span> кода вашей команды'
A1_P = 'Каждый Merge Request — 50+ факторов, реальные часы, грейд, отдача от ИИ и бюджет проекта. Без отчётов и тайм-трекеров.'
SLIDES = """    return [
      { key: 'Звезда грейда', title: 'Уровень', caption: 'звезда грейда по 10 осям и динамика роста', src: '/_blob/bafb77824e1d39daa3b420922830060f' },
      { key: 'Компания', title: 'Дашборд компании', caption: 'эффективность, ИИ, проекты, грейды', src: '/_blob/d8917cd1a1d057105dfc6c6f648403a0' },
      { key: 'Эффективность', title: 'Эффективность специалиста', caption: 'создано ценности в часах и рублях', src: '/_blob/078b103a94164c4d026935ab418de02e' },
      { key: 'Табель', title: 'Табель', caption: 'Jira, MR и коммиты в одном календаре', src: '/_blob/8e065b6e6d912548df6ac04a1d4801aa' },
      { key: 'Глаз', title: '«Глаз»', caption: 'разбор каждого MR до строчки кода', src: '/_blob/1b955fad8df5479c19c6d27c0152e677' },
      { key: 'Рейтинг', title: 'Рейтинг сотрудников', caption: 'по компании, стеку и проекту', src: '/_blob/15b42da0691260ad6b49fb37e4d648bf' },
      { key: 'Качество', title: 'ИИ-ревью кода', caption: 'дефекты по тяжести и блокам качества', src: '/_blob/d4215a5dcf98764dc2068afdfb82ca2f' },
      { key: 'Тех-карта', title: 'Тех-карта проекта', caption: 'технологии, уровни и мэтч команды', src: '/_blob/00ee65e2d395b5fdbfdbabcfe4a1b3ef' }
    ];"""

def rep(s, old, new, count=1, regex=False):
    if regex:
        n = len(re.findall(old, s, flags=re.S))
        assert n == count, f'regex {old[:60]!r}: {n} != {count}'
        return re.sub(old, new, s, flags=re.S)
    n = s.count(old)
    assert n == count, f'{old[:70]!r}: {n} != {count}'
    return s.replace(old, new)

def common(s, accent):
    for a, b in IDS.items():
        s = s.replace(a, b)
    s = rep(s, r'(?:\n<!-- ENTERPRISE -->)?\n<section id="enterprise".*?</section>\n', '\n', regex=True)
    s = s.replace('#enterprise', '#method').replace('>Для банков и enterprise<', '>Методология<').replace('>Для банков<', '>Методология<')
    s = s.replace('mailto:office@dex-it.ru?subject=%D0%9F%D0%B8%D0%BB%D0%BE%D1%82%20UpCore', 'mailto:office@dex-it.ru')
    s = s.replace('>Запросить пилот<', '>Заказать аудит<')
    s = rep(s, 'цифровой тимлид</div>', 'цифровой тимлид · онлайн</div>')
    s = rep(s, r'(<h1 style="[^"]*">).*?(</h1>)', r'\g<1>' + A1_H1.format(c=accent) + r'\g<2>', regex=True)
    # первая кнопка первого экрана → «Подключить репозиторий»
    i = s.index('<h1')
    j = s.index('>Регистрация</a>', i)
    s = s[:j] + '>Подключить репозиторий</a>' + s[j + len('>Регистрация</a>'):]
    # финальный призыв A1
    k = s.rfind('<h2 style="margin: 0; flex: 1 1 520px;')
    if k != -1:
        e = s.index('</section>', k)
        block = s[k:e]
        block = re.sub(r'(<h2 [^>]*>).*?(</h2>)', r'\g<1>Узнайте реальную эффективность команды уже сегодня\g<2>', block, count=1, flags=re.S)
        block = block.replace('>Заказать аудит<', '>office@dex-it.ru<')
        s = s[:k] + block + s[e:]
    return s

def fix_slides(s, n_old):
    s = rep(s, r'  slidesData\(\) \{\n    return \[.*?\];', '  slidesData() {\n' + SLIDES, regex=True)
    s = s.replace(f'% {n_old} }}))', '% 8 }))').replace(f'+ {n_old}) % {n_old}', '+ 8) % 8').replace(f'(i - idx + {n_old}) % {n_old}', '(i - idx + 8) % 8')
    return s

# ---------- Main = светлая ----------
p = D + '/Main.dc.html'; s = open(p, encoding='utf-8').read()
s = common(s, '#0A6F96')
s = rep(s, 'UpCore проверяет каждый Merge Request по 50+ факторам и переводит код в часы, грейд, отдачу от ИИ и бюджет проекта. Без отчётов и тайм-трекеров.', A1_P)
s = fix_slides(s, 6)
s = rep(s, '<title>UpCore — №2 Светлая корпоративная</title>', '<title>UpCore — 1 Светлая корпоративная</title>')
open(p, 'w', encoding='utf-8').write(s); print('Main ok')

# ---------- Video ----------
p = D + '/Video.dc.html'; s = open(p, encoding='utf-8').read()
s = common(s, '#63D5FF')
s = rep(s, 'UpCore проверяет каждый Merge Request по 50+ факторам и переводит код в часы, грейд, отдачу от ИИ и бюджет проекта. Без отчётов и тайм-трекеров.', A1_P)
s = rep(s, r'<div><div style="font-size: 36px; font-weight: 800;">\+14%</div>.*?</div></div>\n', '', regex=True)
s = rep(s, r'<div><div style="font-size: 36px; font-weight: 800;">On-prem</div>.*?</div></div>\n', '', regex=True)
s = rep(s, '<title>UpCore — №1 Видео на первом экране</title>', '<title>UpCore — 2 Видео на первом экране</title>')
open(p, 'w', encoding='utf-8').write(s); print('Video ok')

# ---------- Bays = цветные отсеки ----------
p = D + '/Bays.dc.html'; s = open(p, encoding='utf-8').read()
s = common(s, '#63D5FF')
s = rep(s, 'Оценка специалистов, отдача от ИИ, бюджет проектов и наставничество — на одном анализе каждого Merge Request. 96% от экспертной оценки.', A1_P)
s = rep(s, '<b>On-premise</b></span>', '<b>50+</b> факторов в MR</span>')
s = fix_slides(s, 6)
s = rep(s, '{{num}} / 06', '{{num}} / 08')
s = re.sub(r'0(\d) / UPCORE ', r'0\1 / ', s)
DARK = 'rgba(13,12,21,0.86)'
heads = [
    ('Грейд, который нельзя «нарисовать»', 'Автоматическая оценка специалиста'),
    ('Кто вайбкодит — и окупается ли это', 'Оценка эффективности ИИ и вайбкодеров'),
    ('Бюджет проекта — по коду, а не по акту', 'Эффективность проектов и контроль подрядчиков'),
    ('Наставник, который видит каждый MR', 'ИИ-наставник для каждого разработчика'),
]
for a, b in heads:
    s = rep(s, a, b)
UL = '<ul style="margin: 0; padding-left: 20px; color: ' + DARK + '; font-size: 16px; line-height: 1.75;">{}</ul>'
bodies = [
    ('Рейтинг эффективности и подтверждённый грейд-уровень по анализу MR. Звезда грейда — 10 осей от эффективности до уровня багов.</p>',
     'По анализу MR выдаём рейтинг эффективности и подтверждённый грейд-уровень. Звезда грейда показывает сильные и слабые стороны по 10 осям.</p>' + UL.format('<li>Грейд Junior− … Senior по 3 месяцам работы</li><li>Рейтинг по компании, стеку и проекту</li><li>Эффективность в часах и рублях, авто-резюме</li>')),
    ('Авто-детект ИИ-кода и агент на машине разработчика, который собирает промпты. Каждый MR получает метку и оценку эффективности.</p>',
     'Авто-детект ИИ-кода и агент на машине разработчика, который собирает промпты. Видно, кто вайбкодит и насколько это окупается.</p><div style="display: flex; flex-direction: column; gap: 6px; font-size: 16px;"><span><b>+50–100%</b> — Senior с ИИ</span><span><b>0…+20%</b> — Middle с ИИ</span><span><b>до −50%</b> — Junior с ИИ</span></div>'),
    ('Оценка бюджетов и контроль подрядчиков. Разовый аудит: объективная стоимость всего проекта в часах и рублях.</p>',
     'Сравниваем акты и списанные часы с объективной трудоёмкостью кода. Разовый аудит: считаем бюджет всего проекта по коду.</p>' + UL.format('<li>Аудит аутсорса и аутстаффа</li><li>Прогноз сроков и риски дедлайна</li><li>Техдолг и тех-карта команды</li>')),
    ('По оценкам, задачам, промптам и коду показывает, где проседает эффективность, и собирает персональный план роста.</p>',
     'Опираясь на оценки и все артефакты — задачи, промпты, код — показывает, где проседает эффективность, и даёт рекомендации.</p>' + UL.format('<li>Персональный план развития по реальным ошибкам</li><li>Ревью промптов и постановок задач</li><li>Топ-3 технологии для роста по тех-мэтчу</li>')),
]
for a, b in bodies:
    s = rep(s, a, b)
s = rep(s, '<!-- GRADE -->', '<section style="max-width: 1320px; margin: 0 auto; padding: 0 24px 36px;"><div style="font-family: \'JetBrains Mono\', monospace; font-size: 13px; color: #63D5FF; margin-bottom: 12px;">ПЛАТФОРМА UPCORE</div><h2 style="margin: 0; font-size: clamp(30px, 3.6vw, 56px); letter-spacing: -0.03em; line-height: 1.04; font-weight: 800; max-width: 860px;">Четыре продукта. Один анализ кода.</h2></section>\n\n<!-- GRADE -->')
METHOD_NEW = '''<div style="flex: 1 1 420px; min-width: 0; display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 18px 28px;">
<div><div style="font-size: 26px; font-weight: 800;">50+</div><div style="color: rgba(255,255,255,0.76); line-height: 1.5;">факторов в каждом MR</div></div>
<div><div style="font-size: 26px; font-weight: 800;">100+</div><div style="color: rgba(255,255,255,0.76); line-height: 1.5;">задач подряд в оценке</div></div>
<div><div style="font-size: 26px; font-weight: 800;">AST</div><div style="color: rgba(255,255,255,0.76); line-height: 1.5;">граф проекта: ядро весит больше</div></div>
<div><div style="font-size: 26px; font-weight: 800;">1500+</div><div style="color: rgba(255,255,255,0.76); line-height: 1.5;">разработчиков в калибровке</div></div>
</div>
</div>
</section>

<section style="max-width: 1320px; margin: 0 auto; padding: 0 24px 64px;">
<div style="border-radius: 36px; background: #63D5FF; color: #0D0C15; padding: clamp(28px, 5vw, 64px); display: flex; flex-wrap: wrap; gap: 24px; align-items: center; justify-content: space-between;">
<h2 style="margin: 0; flex: 1 1 520px; font-size: clamp(28px, 3.4vw, 50px); letter-spacing: -0.03em; line-height: 1.05; font-weight: 800;">Узнайте реальную эффективность команды уже сегодня</h2>
<div style="display: flex; flex-wrap: wrap; gap: 10px; flex: 0 1 auto;"><a class="uc-full" href="https://demo.up-core.ru/" style="display: inline-flex; align-items: center; min-height: 52px; padding: 0 24px; border-radius: 16px; background: #0D0C15; color: #FFFFFF; font-weight: 700; text-decoration: none;">Регистрация</a><a class="uc-full" href="mailto:office@dex-it.ru" style="display: inline-flex; align-items: center; min-height: 52px; padding: 0 24px; border-radius: 16px; border: 1.5px solid #0D0C15; color: #0D0C15; font-weight: 700; text-decoration: none;">office@dex-it.ru</a></div>
</div>
</section>'''
s = rep(s, r'<p style="flex: 1 1 420px; min-width: 0; margin: 0; font-size: 18px; line-height: 1\.6; color: rgba\(255,255,255,0\.84\);">50\+ факторов.*?</div>\n</div>\n</section>', METHOD_NEW, regex=True)
s = rep(s, '<title>UpCore — №3 Цветные отсеки продуктов</title>', '<title>UpCore — 4 Цветные отсеки продуктов</title>')
open(p, 'w', encoding='utf-8').write(s); print('Bays ok')
