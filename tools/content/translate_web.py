# -*- coding: utf-8 -*-
"""Перевод HTML-фрагментов сайта на английский по словарю site/i18n/en.json.

Ключ словаря — русская строка текстового узла или атрибута (alt, aria-label, title, placeholder, data-k*/t*/c*)
после схлопывания пробелов; значение — английский перевод. Новые строки без перевода выводит `--missing`.

python3 tools/content/translate_web.py --extract   # site/i18n/ru-strings.json — все русские строки страниц
python3 tools/content/translate_web.py --missing   # строки без перевода
"""
import os, re, sys, json, html as H

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
I18N = os.path.join(REPO, 'site', 'i18n')
CYR = re.compile('[А-Яа-яЁё]')
ATTRS = re.compile(r'\b(alt|aria-label|title|placeholder|data-[ktc]\d+)="([^"]*)"')
_dict = None

def norm(s):
    return re.sub(r'\s+', ' ', H.unescape(s)).strip()

def load():
    global _dict
    if _dict is None:
        p = os.path.join(I18N, 'en.json')
        _dict = json.load(open(p)) if os.path.exists(p) else {}
    return _dict

def split_html(html):
    """[(is_tag, chunk)] — теги и текст между ними (в style/script не заходим)."""
    out, i = [], 0
    for m in re.finditer(r'<(script|style)\b[^>]*>.*?</\1>|<[^>]+>', html, re.S):
        if m.start() > i:
            out.append((False, html[i:m.start()]))
        out.append((True, m.group(0)))
        i = m.end()
    if i < len(html):
        out.append((False, html[i:]))
    return out

def strings(html):
    res = []
    for is_tag, ch in split_html(html):
        if is_tag:
            for m in ATTRS.finditer(ch):
                if CYR.search(m.group(2)):
                    res.append(norm(m.group(2)))
        elif CYR.search(ch):
            res.append(norm(ch))
    return res

MISSING = set()

def tr(s):
    d = load()
    k = norm(s)
    if k in d:
        return d[k]
    MISSING.add(k)
    return k

def en_numbers(t):
    """Числа в английском формате: 3,2 → 3.2; 1 500 → 1,500 (только в текстах без кириллицы)."""
    t = re.sub(r'(?<=\d),(?=\d)', '.', t)
    return re.sub(r'(?<=\d)[ \u00a0\u202f](?=\d{3}(?!\d))', ',', t)

def translate_html(html):
    out = []
    for is_tag, ch in split_html(html):
        if is_tag:
            ch = ATTRS.sub(lambda m: '%s="%s"' % (m.group(1), H.escape(tr(m.group(2)), quote=True)) if CYR.search(m.group(2)) else m.group(0), ch)
            ch = ch.replace('lang="ru"', 'lang="en"')
            out.append(ch)
        elif CYR.search(ch):
            lead = re.match(r'\s*', ch).group(0)
            trail = re.search(r'\s*$', ch).group(0)
            out.append(lead + H.escape(tr(ch), quote=False) + trail)
        else:
            out.append(en_numbers(ch))
    return ''.join(out)

if __name__ == '__main__':
    gen = os.path.join(REPO, 'site', 'src', 'generated', 'ru')
    allstr = []
    for f in sorted(os.listdir(gen)):
        for s in strings(open(os.path.join(gen, f)).read()):
            if s not in allstr:
                allstr.append(s)
    os.makedirs(I18N, exist_ok=True)
    if '--extract' in sys.argv:
        json.dump(allstr, open(os.path.join(I18N, 'ru-strings.json'), 'w'), ensure_ascii=False, indent=1)
        print(len(allstr), 'строк')
    if '--missing' in sys.argv:
        d = load()
        miss = [s for s in allstr if s not in d]
        json.dump(miss, open(os.path.join(I18N, 'missing.json'), 'w'), ensure_ascii=False, indent=1)
        print(len(miss), 'без перевода из', len(allstr))
