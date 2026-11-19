// Светлая тема (раунд 105). Тёмная тема — исходная и не меняется.
// Цвета страниц заданы прямо в разметке (style="…"). При сборке каждый такой цвет, у которого есть светлая пара,
// оборачивается в var(--lt-…, <исходный цвет>): в тёмной теме переменная не задана → браузер берёт исходный цвет
// (вид в точности прежний); в светлой теме html[data-theme="light"] задаёт переменные → светлые цвета.
// SVG-атрибуты fill/stroke перекрашиваются CSS-правилами по значению атрибута (только в светлой теме).

type Kind = 't' | 'b' | 'l'; // t — цвет текста, b — фон, l — линии (рамки, обводки)

const INK = '13,12,21'; // #0D0C15 — основной тёмный цвет бренда, им пишется текст в светлой теме

// Текст: белый → тёмный; белый с прозрачностью → тёмный с чуть большей плотностью (иерархия сохраняется, контраст ≥ 4,5:1);
// фирменные акценты → их тёмные варианты (светлые акценты на белом не читаются).
const TEXT: Record<string, string> = {
  '#ffffff': '#0D0C15', '#fff': '#0D0C15',
  '#63d5ff': '#0A6F9C', '#7fdb7a': '#1D7A2C', '#53c04d': '#1D7A2C', '#f2c14e': '#8A5E00', '#f7d88a': '#8A5E00',
  '#b9aeff': '#5A3FD0', '#9b8cff': '#5A3FD0', '#f08a8a': '#C0392B', '#e86565': '#C0392B', '#a8e8ff': '#075A80',
};
// Фон: подложки страницы и карточек → светлые; полупрозрачный белый → полупрозрачный тёмный. Цветные заливки (кнопки, полосы, плашки) — как есть.
const BG: Record<string, string> = {
  '#0d0c15': '#F4F6FA', '#1a1925': '#FFFFFF', '#12111c': '#F2F4F8', '#171620': '#EBEEF4', '#0b0a12': '#F6F8FB',
};
const LINE: Record<string, string> = { '#12111c': '#FFFFFF' };

const WHITE_A = /^rgba\(\s*255\s*,\s*255\s*,\s*255\s*,\s*([\d.]+)\s*\)$/i;
const AMBER_A = /^rgba\(\s*242\s*,\s*193\s*,\s*78\s*,\s*([\d.]+)\s*\)$/i;
const INK_A = /^rgba\(\s*13\s*,\s*12\s*,\s*21\s*,\s*([\d.]+)\s*\)$/i;
const r2 = (x: number) => Math.round(x * 1000) / 1000;

function light(kind: Kind, c: string): string | null {
  const k = c.toLowerCase();
  let m = k.match(WHITE_A);
  if (m) {
    const a = parseFloat(m[1]);
    if (kind === 't') return `rgba(${INK},${r2(Math.min(0.92, 0.45 + a * 0.5))})`;
    if (kind === 'b') return `rgba(${INK},${r2(a <= 0.1 ? a * 0.8 + 0.01 : a * 0.6)})`;
    return `rgba(${INK},${r2(Math.min(0.3, a * 0.9 + 0.02))})`;
  }
  m = k.match(AMBER_A);
  if (m && kind === 't') return '#8A5E00'; // приглушённые жёлтые подписи → тёмно-янтарный (на белом читается)
  m = k.match(INK_A);
  if (m && kind === 't') { const a = parseFloat(m[1]); return a < 0.75 ? `rgba(${INK},${r2(a + 0.15)})` : null; } // тёмный текст на цветных плашках — чуть плотнее
  if (kind === 't') return TEXT[k] ?? null;
  if (kind === 'b') return BG[k] ?? null;
  return LINE[k] ?? null;
}

const key = (kind: Kind, c: string) => `--lt-${kind}-` + c.toLowerCase().replace(/^#/, '').replace(/rgba?\(|\)|\s/g, '').replace(/[,.]/g, '_');
const COLOR = /#[0-9a-fA-F]{3,8}\b|rgba?\([^)]*\)/g;
const used = new Map<string, string>(); // имя переменной → светлый цвет

function kindOf(prop: string): Kind | null {
  if (prop === 'color' || prop === 'text-decoration-color' || prop === 'caret-color' || prop === '-webkit-text-fill-color') return 't';
  if (prop === 'background' || prop === 'background-color' || prop === 'background-image') return 'b';
  if (prop.startsWith('border') || prop.startsWith('outline')) return 'l';
  return null; // тени, fill/stroke в style и пр. — без изменений
}

// Остаются как есть целиком: ссылки-кнопки со сплошной тёмной или цветной заливкой (например, тёмная кнопка в цветном блоке контактов)
// и плашки с цветной заливкой и своим цветом текста (активный продукт в меню и т. п.). Обёртка страницы (div с тёмным фоном) — перекрашивается.
const SOLID_DARK_OR_ACCENT = /(^|;)\s*background(-color)?:\s*(#0D0C15|#63D5FF|#7FDB7A|#F2C14E|#B9AEFF|#F08A8A|#53C04D|#9B8CFF)\s*(;|$)/i;
const SOLID_ACCENT = /(^|;)\s*background(-color)?:\s*(#63D5FF|#7FDB7A|#F2C14E|#B9AEFF|#F08A8A|#53C04D|#9B8CFF)\s*(;|$)/i;

function themeStyle(tag: string, style: string): string {
  if ((tag === 'a' || tag === 'button') && SOLID_DARK_OR_ACCENT.test(style)) return style;
  if (SOLID_ACCENT.test(style) && /(^|;)\s*color:/i.test(style)) return style;
  return style.split(';').map((decl) => {
    const i = decl.indexOf(':');
    if (i < 0) return decl;
    const prop = decl.slice(0, i).trim().toLowerCase();
    const kind = kindOf(prop);
    if (!kind) return decl;
    const val = decl.slice(i + 1).replace(COLOR, (c) => {
      const lc = light(kind, c);
      if (!lc) return c;
      const v = key(kind, c);
      used.set(v, lc);
      return `var(${v}, ${c})`;
    });
    return decl.slice(0, i + 1) + val;
  }).join(';');
}

/** Разметка страницы → та же разметка, где цвета со светлой парой обёрнуты в var(--lt-…, исходный цвет). */
export function themeHtml(html: string): string {
  return html.replace(/<([a-zA-Z][\w-]*)\b([^>]*?)\sstyle="([^"]*)"/g, (_m, tag: string, attrs: string, style: string) =>
    `<${tag}${attrs} style="${themeStyle(tag.toLowerCase(), style)}"`);
}

// SVG: значения атрибутов fill/stroke → светлые (только в светлой теме). Текст в акцентном цвете — тёмный вариант акцента; фигуры — как есть.
const SVG_FILL: Record<string, string> = {
  '#fff': '#0D0C15', '#FFFFFF': '#0D0C15', 'rgba(255,255,255,0.76)': `rgba(${INK},0.78)`, 'rgba(255,255,255,0.7)': `rgba(${INK},0.72)`,
  'rgba(255,255,255,0.35)': `rgba(${INK},0.64)`, 'rgba(255,255,255,0.015)': `rgba(${INK},0.02)`,
};
const SVG_STROKE: Record<string, string> = {
  '#FFFFFF': '#0D0C15', '#fff': '#0D0C15', '#12111C': '#FFFFFF', 'rgba(255,255,255,0.08)': `rgba(${INK},0.12)`, 'rgba(255,255,255,0.10)': `rgba(${INK},0.14)`,
  'rgba(255,255,255,0.1)': `rgba(${INK},0.14)`, 'rgba(255,255,255,0.55)': `rgba(${INK},0.45)`, 'rgba(255,255,255,0.7)': `rgba(${INK},0.55)`,
};
const SVG_TEXT_FILL: Record<string, string> = { '#63D5FF': '#0A6F9C', '#7FDB7A': '#1D7A2C', '#F2C14E': '#8A5E00', '#F08A8A': '#C0392B', '#B9AEFF': '#5A3FD0' };

// Все фрагменты страниц — чтобы набор переменных был полным и не зависел от порядка сборки страниц.
const FRAGMENTS = import.meta.glob('../generated/*/*.html', { query: '?raw', import: 'default', eager: true }) as Record<string, string>;
let ready = false;

/** CSS светлой темы для разметки страниц (переменные + SVG). Подключается в Base.astro, действует только при html[data-theme="light"]. */
export function lightCss(extra: string[] = []): string {
  if (!ready) { Object.values(FRAGMENTS).forEach((h) => themeHtml(h)); ready = true; }
  extra.forEach((h) => themeHtml(h));
  const L = 'html[data-theme="light"]';
  const vars = [...used].map(([k, v]) => `${k}:${v}`).join(';');
  const fill = Object.entries(SVG_FILL).map(([a, v]) => `${L} [fill="${a}"]{fill:${v}}`).join('');
  const stroke = Object.entries(SVG_STROKE).map(([a, v]) => `${L} [stroke="${a}"]{stroke:${v}}`).join('');
  const text = Object.entries(SVG_TEXT_FILL).map(([a, v]) => `${L} text[fill="${a}"],${L} tspan[fill="${a}"]{fill:${v}}`).join('');
  return `${L}{${vars}}${fill}${stroke}${text}`;
}

/** Цвет для style="…" в компонентах (меню, 404): var(--lt-…, цвет), если у цвета есть светлая пара, иначе сам цвет. */
export function themeColor(kind: Kind, c: string): string {
  const lc = light(kind, c);
  if (!lc) return c;
  const v = key(kind, c);
  used.set(v, lc);
  return `var(${v}, ${c})`;
}
