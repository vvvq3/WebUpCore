"""Грубый пререндер .dc.html → обычный HTML для проверки вёрстки в браузере.
Раскрывает <helmet>, <sc-for> (по данным слайдов/вкладок), <sc-if>, подставляет {{holes}}
и заменяет /_blob/<id> на локальные файлы."""
import re, sys, os, html

SRC, OUT = sys.argv[1], sys.argv[2]
REPO = '/home/user/WebUpCore'
BLOBS = {
    'f43be9baafd8829d6b16ffe80acc1058': REPO + '/docs/brand/logo.svg',
    'b75df264cd5b3518da714c1bfe73295a': REPO + '/docs/brand/logo-dark.svg',
    'bafb77824e1d39daa3b420922830060f': REPO + '/docs/reference/demo/slides/star.jpg',
    'd8917cd1a1d057105dfc6c6f648403a0': REPO + '/docs/reference/demo/slides/company.jpg',
    '078b103a94164c4d026935ab418de02e': REPO + '/docs/reference/demo/slides/efficiency.jpg',
    '8e065b6e6d912548df6ac04a1d4801aa': REPO + '/docs/reference/demo/slides/timesheet.jpg',
    '1b955fad8df5479c19c6d27c0152e677': REPO + '/docs/reference/demo/slides/eye.jpg',
    '15b42da0691260ad6b49fb37e4d648bf': REPO + '/docs/reference/demo/slides/rating.jpg',
    'd4215a5dcf98764dc2068afdfb82ca2f': REPO + '/docs/reference/demo/slides/quality.jpg',
    '00ee65e2d395b5fdbfdbabcfe4a1b3ef': REPO + '/docs/reference/demo/slides/techmap.jpg',
    '93d0ed58db776563015d10b8660132e6': REPO + '/docs/reference/demo/video/teaser.mp4',
    'dd9427e92ed40645720e9a95710530d7': REPO + '/docs/reference/demo/video/poster.jpg',
    'd4c2740f35d5c35e496626ba187a1752': REPO + '/docs/brand/logo.svg',
    '75fbf6048ce4882bb5f39aa3202b0f6d': REPO + '/docs/brand/logo-dark.svg',
    'afdf675f8bedfead15e609fdb13aa49b': REPO + '/docs/reference/demo/slides/star.jpg',
    '9cba81e6ca23a0c1263f23c20f8003d1': REPO + '/docs/reference/demo/slides/company.jpg',
    '6c6353e4a251a57072c1e2bf94de7c76': REPO + '/docs/reference/demo/slides/efficiency.jpg',
    '13400136e70882d874f7a2528f15026e': REPO + '/docs/reference/demo/slides/timesheet.jpg',
    '40525ebf8d2111c88f08ef46f71635b4': REPO + '/docs/reference/demo/slides/eye.jpg',
    'd7c8fafeeb9ade6b82b3400769fbe356': REPO + '/docs/reference/demo/slides/rating.jpg',
    '2696bde9510556b393f5f92bee142467': REPO + '/docs/reference/demo/slides/quality.jpg',
    '43a5f658acd56dde7b15581b6f106e43': REPO + '/docs/reference/demo/slides/techmap.jpg',
    'bf93e9d9d986cce0fe07717349a58372': REPO + '/docs/brand/logo.svg',
    'e5d3c964350fd7d4aa2972071c2dfc5f': REPO + '/docs/brand/logo-dark.svg',
    '10523aa730bf9b6cf46e6f20733ff512': REPO + '/docs/reference/demo/slides/star.jpg',
    'b3cfb286fc63dac12b16ea1c9396363b': REPO + '/docs/reference/demo/slides/company.jpg',
    '33df02474899e07db8fd39fb946dc103': REPO + '/docs/reference/demo/slides/efficiency.jpg',
    '6df194d7dfb12cde45e704a49b987210': REPO + '/docs/reference/demo/slides/timesheet.jpg',
    'e676139660e4ea00b101c92ec42793d7': REPO + '/docs/reference/demo/slides/eye.jpg',
    'fe9e6754803798391fc83dcc562c7e25': REPO + '/docs/reference/demo/slides/rating.jpg',
    '556228af3ab2ef50bde7808479c72f26': REPO + '/docs/reference/demo/video/teaser.mp4',
    'aaaadea38505d8b9831a28ae186670c4': REPO + '/docs/reference/demo/video/poster.jpg',
}
SL = [
    ('Звезда грейда', 'Уровень', 'звезда грейда по 10 осям', 'afdf675f8bedfead15e609fdb13aa49b'),
    ('Компания', 'Дашборд компании', 'эффективность, ИИ, проекты', '9cba81e6ca23a0c1263f23c20f8003d1'),
    ('Эффективность', 'Эффективность специалиста', 'ценность в часах и рублях', '6c6353e4a251a57072c1e2bf94de7c76'),
    ('Табель', 'Табель', 'Jira, MR и коммиты', '13400136e70882d874f7a2528f15026e'),
    ('Глаз', '«Глаз»', 'разбор каждого MR', '40525ebf8d2111c88f08ef46f71635b4'),
    ('Рейтинг', 'Рейтинг сотрудников', 'по компании, стеку и проекту', 'd7c8fafeeb9ade6b82b3400769fbe356'),
    ('Качество', 'ИИ-ревью кода', 'дефекты по тяжести', '2696bde9510556b393f5f92bee142467'),
    ('Тех-карта', 'Тех-карта проекта', 'технологии и мэтч', '43a5f658acd56dde7b15581b6f106e43'),
]
N = int(os.environ.get('UC_SLIDES', '0')) or len(SL)
SL = SL[:N]
def slide(i):
    k, t, c, b = SL[i]
    pos = (i - 0 + len(SL)) % len(SL)
    return {'key': k, 'title': t, 'caption': c, 'note': c, 'src': '/_blob/' + b, 'num': '0%d' % (i + 1),
            'active': i == 0, 'inactive': i != 0, 'front': pos == 0, 'b1': pos == 1, 'b2': pos == 2}
TABS = [{'label': 'UpCore ' + x, 'active': i == 0, 'inactive': i != 0} for i, x in enumerate(['Grade', 'AI', 'Projects', 'Mentor'])]
CHAP = [{'t': x, 'time': y, 'active': i == 0, 'inactive': i != 0} for i, (x, y) in enumerate([('Звезда грейда', '0:00'), ('Компания', '0:05'), ('ИИ-ревью кода', '0:12'), ('Табель', '0:16'), ('Рейтинг', '0:20'), ('«Глаз»', '0:28')])]
GLOBAL = {'isGrade': True, 'isAI': False, 'isProjects': False, 'isMentor': False, 'num': '01', 'menuOpen': False, 'menuClosed': True,
          'playing': True, 'paused': False, 'running': True, 'playLabel': 'Пауза', 'cur': slide(0), 'yes': True}

s = open(SRC, encoding='utf-8').read()
helmet = re.search(r'<helmet>(.*?)</helmet>', s, re.S)
head_extra = helmet.group(1) if helmet else ''
body = re.search(r'<x-dc>(.*?)</x-dc>', s, re.S).group(1)
body = re.sub(r'<helmet>.*?</helmet>', '', body, flags=re.S)

def lookup(path, scope):
    parts = path.strip().split('.')
    v = scope.get(parts[0], GLOBAL.get(parts[0]))
    for p in parts[1:]:
        v = v.get(p) if isinstance(v, dict) else None
    return v

def render(fragment, scope):
    def sc_if(m):
        val = lookup(m.group(1), scope)
        return m.group(2) if val else ''
    fragment = re.sub(r'<sc-if value="\{\{\s*(.*?)\s*\}\}"[^>]*>(.*?)</sc-if>', sc_if, fragment, flags=re.S)
    def hole(m):
        v = lookup(m.group(1), scope)
        if v is None or isinstance(v, (dict, bool)):
            return ''
        return html.escape(str(v), quote=True)
    return re.sub(r'\{\{\s*([\w.$]+)\s*\}\}', hole, fragment)

def sc_for(m):
    lst, var, inner = m.group(1), m.group(2), m.group(3)
    data = {'slides': [slide(i) for i in range(len(SL))], 'tabs': TABS, 'chapters': CHAP}.get(lst, [])
    return ''.join(render(inner, {var: d}) for d in data)

body = re.sub(r'<sc-for list="\{\{\s*(\w+)\s*\}\}" as="(\w+)"[^>]*>(.*?)</sc-for>', sc_for, body, flags=re.S)
body = render(body, {})
body = re.sub(r'\s(onClick|onclick)="[^"]*"', '', body)
def blob(m):
    return 'file://' + BLOBS.get(m.group(1), '')
out = '<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">' + head_extra + '</head><body>' + body + '</body></html>'
out = re.sub(r'/_blob/([0-9a-f]{32})', blob, out)
open(OUT, 'w', encoding='utf-8').write(out)
print('ok', OUT, len(out))
