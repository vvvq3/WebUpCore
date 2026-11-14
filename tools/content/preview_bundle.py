# -*- coding: utf-8 -*-
"""Копия собранного сайта (site/dist) с относительными ссылками — чтобы открыть её как страницу на claude.ai
или прямо из файлов, без сервера.  python3 tools/content/preview_bundle.py <out_dir>"""
import os, re, sys, shutil
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DIST = os.path.join(REPO, 'site', 'dist')
SKIP = {'sitemap-0.xml', 'sitemap-index.xml', 'robots.txt'}

def rel(path, depth):
    pre = '../' * depth
    p, _, frag = path.partition('#')
    if p == '/':
        p = 'index.html'
    elif p.endswith('/'):
        p = p[1:] + 'index.html'
    else:
        p = p[1:]
    return pre + p + ('#' + frag if frag else '')

def main(out):
    if os.path.exists(out):
        shutil.rmtree(out)
    for d, _, files in os.walk(DIST):
        for f in files:
            src = os.path.join(d, f)
            r = os.path.relpath(src, DIST)
            if r in SKIP:
                continue
            dst = os.path.join(out, r)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if f.endswith('.html'):
                depth = r.count('/')
                t = open(src).read()
                t = re.sub(r'(href|src)="(/(?!/)[^"]*)"', lambda m: '%s="%s"' % (m.group(1), rel(m.group(2), depth)), t)
                t = re.sub(r'url\((/(?!/)[^)]*)\)', lambda m: 'url(%s)' % rel(m.group(1), depth), t)  # шрифты во встроенных стилях
                open(dst, 'w').write(t)
            elif f.endswith('.css'):
                t = open(src).read()
                open(dst, 'w').write(re.sub(r'url\(/_astro/', 'url(', t))
            else:
                shutil.copy(src, dst)
    print('готово:', out)

if __name__ == '__main__':
    main(sys.argv[1])
