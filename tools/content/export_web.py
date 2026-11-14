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
    return re.sub(r'href="([^"]*)"', href, html)

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
    for key, (_, f) in bp.IMG.items():
        dst = os.path.join(img, 'screens', f.replace('.jpg', '.webp'))
        if not os.path.exists(dst):
            im = Image.open(os.path.join(REPO, 'docs/reference/demo/slides', f)).convert('RGB')
            if im.width > 1600:
                im = im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS)
            im.save(dst, 'WEBP', quality=82, method=6)

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
        open(os.path.join(GEN, 'ru', key + '.html'), 'w').write(localize(html, 'ru', route))
        if tr:
            open(os.path.join(GEN, 'en', key + '.html'), 'w').write(localize(tr.translate_html(html), 'en', route))
    open(os.path.join(SITE, 'src', 'styles', 'generated.css'), 'w').write(css())
    assets()
    print('RU:', len(PAGES), 'страниц', '· EN:', 'да' if tr else 'нет (site/i18n/en.json не найден)')

if __name__ == '__main__':
    main()
