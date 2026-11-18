# -*- coding: utf-8 -*-
"""Экспорт утверждённых макетов в сайт на Astro (site/).

python3 tools/content/export_web.py

Берёт те же функции страниц, что и холст (build_pages.py), в режиме MODE='web' и пишет:
  site/src/generated/ru/<page>.html  — HTML-фрагменты страниц (RU)
  site/src/generated/en/<page>.html  — то же на английском (перевод — site/i18n/en.json)
  site/src/styles/generated.css      — общие стили макетов (из HELMET)
  site/public/img/                   — логотип, фавикон, скриншоты демо в WebP
Правки текстов и вёрстки — в build_pages.py, затем снова запустить этот скрипт.
"""
import os, re, sys, json, shutil
sys.path.insert(0, os.path.dirname(__file__))
import build_pages as bp

REPO = bp.REPO
SITE = os.path.join(REPO, 'site')
GEN = os.path.join(SITE, 'src', 'generated')

# key → (маршрут, функция страницы)
PAGES = {
    'home': ('', lambda: bp.home('A')),
    'grade': ('grade/', lambda: bp.grade_page(3)),
    'ai': ('ai/', bp.ai_page_final),
    'projects': ('projects/', bp.proj_main2),
    'mentor': ('mentor/', bp.mentor_main2),
    'blog': ('blog/', lambda: bp.blog_page2(1)),
    'blog-2': ('blog/2/', lambda: bp.blog_page2(2)),
    'blog-3': ('blog/3/', lambda: bp.blog_page2(3)),
}
# Раунды 82–94: страницы — новая версия по ТЗ владельца (RU и перевод EN).
# Прежняя версия сайта снята с публикации (раунд 88) — есть в истории git (коммит 9b7d65c, папка site/public/old/).
# Откатить страницу к прежней версии — убрать её из RU_OVERRIDES.
RU_OVERRIDES = {'home': bp.home_v2, 'grade': bp.grade_v2, 'ai': bp.ai_v2, 'projects': bp.proj_v2, 'mentor': bp.mentor_v2,
                'blog': lambda: bp.blog_v2(1), 'blog-2': lambda: bp.blog_v2(2), 'blog-3': lambda: bp.blog_v2(3)}
RU_EXTRA = {}
ANCHORS = {'#top': '', '#grade': 'grade/', '#ai': 'ai/', '#projects': 'projects/', '#mentor': 'mentor/', '#blog': 'blog/',
           '#grade-page': 'grade/', '#ai-page': 'ai/', '#projects-page': 'projects/', '#mentor-page': 'mentor/'}
FONTS = [("'Bricolage Grotesque'", "'Bricolage Grotesque Variable'"), ("'Onest'", "'Onest Variable'"), ("'JetBrains Mono'", "'JetBrains Mono Variable'"),
         ('Onest, sans-serif', "'Onest Variable', sans-serif")]

def fonts(s):
    for a, b in FONTS:
        s = s.replace(a, b)
    return s

def localize(html, lang, route):
    pre = '/' if lang == 'ru' else '/en/'
    html = html.replace('<header style=', '<header class="uc-site-header" style=', 1)
    def href(m):
        h = m.group(1)
        if h in ANCHORS:
            return 'href="' + pre + ANCHORS[h] + '"'
        if h == '#lang':
            return 'href="' + ('/en/' if lang == 'ru' else '/') + route + '" hreflang="' + ('en' if lang == 'ru' else 'ru') + '" lang="' + ('en' if lang == 'ru' else 'ru') + '"'
        if h.startswith('/blog/') and lang == 'en':
            return 'href="/en' + h + '"'
        return m.group(0)
    html = re.sub(r'href="([^"]*)"', href, html)
    if lang == 'en':  # раунд 95: в английской версии блога нет — ссылки на него убираем
        html = re.sub(r'<a href="/en/blog/[^"]*"[^>]*>.*?</a>', '', html, flags=re.S)
    return html

def css():
    m = re.search(r'<style>(.*?)</style>', bp.HELMET, re.S)
    body = m.group(1)
    return ('/* Сгенерировано tools/content/export_web.py из HELMET (build_pages.py) — не править вручную */\n'
            + fonts(body).replace('body{margin:0;background:#0D0C15}', '').strip() + '\n')

def assets():
    img = os.path.join(SITE, 'public', 'img')
    os.makedirs(os.path.join(img, 'screens'), exist_ok=True)
    shutil.copy(os.path.join(REPO, 'docs/brand/logo.svg'), os.path.join(img, 'logo.svg'))
    shutil.copy(os.path.join(REPO, 'docs/brand/favicon.svg'), os.path.join(SITE, 'public', 'favicon.svg'))
    from PIL import Image
    # Слайды главной (раунд 72): все скриншоты приводятся к одной пропорции 16:10 (как окно слайдера) — показываются целиком,
    # без обрезки и без скачков высоты. Широкие — вписываются по ширине с полями цвета фона интерфейса, высокие («Глаз») — верх экрана.
    W, H = 1600, 1000
    for key, (_, f) in bp.IMG.items():
        dst = os.path.join(img, 'screens', f.replace('.jpg', '.webp'))
        im = Image.open(os.path.join(REPO, 'docs/reference/demo/slides', f)).convert('RGB')
        if im.width / im.height >= W / H:
            im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
            bg = im.getpixel((im.width - 4, im.height - 4))
            canvas = Image.new('RGB', (W, H), bg)
            canvas.paste(im, (0, (H - im.height) // 2))
        else:
            im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
            canvas = im.crop((0, 0, W, H))
        canvas.save(dst, 'WEBP', quality=90, method=6)
    # Раунд 78: скриншоты владельца для слайдера — окно 2:1 (1600×800), привязка к левому верхнему углу:
    # широкие дополняются белым снизу (фон интерфейса белый), высокие подрезаются снизу; по ширине ничего не теряется.
    os.makedirs(os.path.join(img, 'screens', 'v2'), exist_ok=True)
    W2, H2 = 1600, 800
    for _, _, _, f in bp.SCREENS:
        im = Image.open(os.path.join(REPO, 'docs/reference/demo/screens', f)).convert('RGB')
        im = im.resize((W2, round(im.height * W2 / im.width)), Image.LANCZOS)
        canvas = Image.new('RGB', (W2, H2), (255, 255, 255))
        canvas.paste(im.crop((0, 0, W2, min(H2, im.height))), (0, 0))
        canvas.save(os.path.join(img, 'screens', 'v2', f.replace('.png', '.webp')), 'WEBP', quality=88, method=6)

def main():
    hp = os.path.join(os.path.dirname(__file__), 'heights.json')
    bp.MODE = 'web'
    os.makedirs(os.path.join(GEN, 'ru'), exist_ok=True)
    os.makedirs(os.path.join(GEN, 'en'), exist_ok=True)
    tr = None
    trp = os.path.join(SITE, 'i18n', 'en.json')
    if os.path.exists(trp):
        sys.path.insert(0, os.path.join(REPO, 'tools', 'content'))
        import translate_web
        tr = translate_web
    for key, (route, fn) in PAGES.items():
        html = fonts(fn())
        ru = fonts(RU_OVERRIDES[key]()) if key in RU_OVERRIDES else html
        open(os.path.join(GEN, 'ru', key + '.html'), 'w').write(localize(ru, 'ru', route))
        enf = os.path.join(GEN, 'en', key + '.html')
        if key.startswith('blog'):  # раунд 95: в английской версии блога нет
            if os.path.exists(enf):
                os.remove(enf)
        elif tr:
            open(enf, 'w').write(localize(tr.translate_html(ru), 'en', route))  # раунд 94: EN — перевод новой версии
    for key, (route, fn) in RU_EXTRA.items():
        open(os.path.join(GEN, 'ru', key + '.html'), 'w').write(localize(fonts(fn()), 'ru', route))
    for key in os.listdir(os.path.join(GEN, 'ru')):  # убрать устаревшие дополнительные страницы
        k = key[:-5]
        if k not in PAGES and k not in RU_EXTRA:
            os.remove(os.path.join(GEN, 'ru', key))
    open(os.path.join(SITE, 'src', 'styles', 'generated.css'), 'w').write(css())
    assets()
    print('RU:', len(PAGES), 'страниц', '· EN:', 'да' if tr else 'нет (site/i18n/en.json не найден)')

if __name__ == '__main__':
    main()
