# -*- coding: utf-8 -*-
"""docs/content/theses.json → .xlsx для импорта в Sheet «Тезисы UpCore» (итог — формулой).
python3 tools/content/theses_xlsx.py <out.xlsx>"""
import json, os, sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

root = os.path.join(os.path.dirname(__file__), '..', '..', 'docs', 'content')
rows = json.load(open(os.path.join(root, 'theses.json'), encoding='utf-8'))
wb = Workbook(); ws = wb.active; ws.title = 'Тезисы'
ws['A1'] = 'Как читать'; ws['B1'] = ('Оценки 1–5: Б — острота боли и актуальность · Ц — бизнес-ценность (деньги, время, риски) · К — конкретика, цифры · '
                                      'Д — доказуемость · О — отличие от конкурентов · Я — ясность за 5 секунд.')
ws['A2'] = 'Итог'; ws['B2'] = ('= (Б×0,25 + Ц×0,20 + К×0,15 + Д×0,15 + О×0,125 + Я×0,125) × 20, от 0 до 100 — пересчитывается при изменении оценок. '
                                'Тип «Бизнес-показатель» с пометкой «таблица (конкурент)» — ориентир рынка, на сайт не выносим. '
                                'В «Решение» отмечайте: оставить / править / убрать.')
for c in ('A1', 'A2'):
    ws[c].font = Font(bold=True)
head = ['Итог', 'Тезис', 'Раздел', 'Решение', 'Комментарий', 'ЦА', 'Тип', 'Б', 'Ц', 'К', 'Д', 'О', 'Я', 'Источник', 'Где в макетах', '№']
ws.append([]); ws.append(head)
for i, cell in enumerate(ws[4], 1):
    cell.fill = PatternFill('solid', fgColor='E8F6FC')
for n, x in enumerate(rows, 5):
    t = x['тезис']
    if t[:1] in '=+-@':
        t = "'" + t
    ws.append([f'=ROUND((H{n}*0.25+I{n}*0.2+J{n}*0.15+K{n}*0.15+L{n}*0.125+M{n}*0.125)*20,0)', t, x['раздел'], None, None, x['ЦА'], x['тип'],
               x['боль'], x['бизнес-ценность'], x['конкретика'], x['доказуемость'], x['отличие'], x['ясность'], x['источник'], x['где в макетах'], x['id']])
    if x['ссылка']:
        ws.cell(n, 14).hyperlink = x['ссылка']
    ws.cell(n, 1).font = Font(bold=True)
    for col in (2, 5, 14, 15):
        ws.cell(n, col).alignment = Alignment(wrap_text=True, vertical='top')
widths = {'A': 7, 'B': 57, 'C': 15, 'D': 12, 'E': 34, 'F': 16, 'G': 17, 'H': 5, 'I': 5, 'J': 5, 'K': 5, 'L': 5, 'M': 5, 'N': 37, 'O': 31, 'P': 6}
for k, v in widths.items():
    ws.column_dimensions[k].width = v
ws.freeze_panes = 'A5'
wb.save(sys.argv[1])
print(len(rows), 'строк →', sys.argv[1])
