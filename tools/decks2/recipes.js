// Состав презентаций v2 (раунд 97). Каждый слайд — блок сайта: {p: страница, s: id или номер блока, rm: пути детей, hide: селекторы, hideText: начало текста}.
// shot — скриншот демо с подписью из слайдера сайта (SCREENS в build_pages.py).
const SCREENS = {
  level: ['Уровень', 'Уровень разработчика', 'звезда грейда по 10 факторам и динамика роста', '01-level.png', 1],
  efficiency: ['Эффективность', 'Эффективность специалиста', 'ценность за месяц в часах и рублях, рейтинг', '02-efficiency.png', 2],
  team: ['Команда', 'Команда', 'эффективность, грейд и вклад каждого за месяц и за 3 месяца', '03-team.png', 3],
  code: ['Код', 'Код', 'результирующий код, контрибуция, архитектура и уровень багов', '04-code.png', 4],
  quality: ['Качество', 'Качество', 'ИИ-ревью каждого MR и дефекты по тяжести', '05-quality.png', 5],
  calendar: ['Календарь', 'Календарь работы', 'Jira, MR и коммиты по дням', '06-calendar.png', 6],
  dynamics: ['Динамика', 'Динамика', 'тренд производительности по неделям', '07-dynamics.png', 7],
  tech: ['Технологии', 'Технологии', 'карта технологий и мэтч с проектом', '08-tech.png', 8],
  rating: ['Рейтинг', 'Рейтинг сотрудников', 'по компании, стеку и проекту', '09-rating.png', 9],
  project: ['Проект', 'Проект', 'эффективность проекта за месяц и за 3 месяца', '10-project.png', 10],
  insights: ['Выводы', 'Выводы и рекомендации', 'сводный отчёт по компании', '11-insights.png', 11],
  timesheet: ['Табель', 'Табель', 'эффективность команды по месяцам', '12-timesheet.png', 12],
  losses: ['Потери', 'Финансовые потери', 'потери в рублях и реальная ставка', '13-losses.png', 13],
  company: ['Компания', 'Дашборд компании', 'эффективность, ИИ, проекты и грейды', '14-company.png', 14],
};
const shot = k => ({ shot: SCREENS[k].slice(0, 4), num: SCREENS[k][4] });

// общие блоки
const HOME_TOP = k => ({ p: 'home', s: 'top', coverShot: SCREENS[k].slice(0, 4), coverNum: SCREENS[k][4] });
const PRODUCTS = { p: 'home', s: 'products', hideText: ['Подробнее о Grade', 'Подробнее об AI', 'Подробнее о Projects', 'Подробнее о Mentor'],
  css: { '.g2': 'grid-template-columns: repeat(4, minmax(0, 1fr)) !important; gap: 16px !important;', 'article': 'padding: 22px !important;', '[style*="7.6vw"]': 'font-size: 36px !important;', '[style*="7vw, 48px"]': 'font-size: 32px !important;' } };
const CORE = { p: 'home', s: 'core' };
const RESULTS = { p: 'home', s: 'results' };
const SAAS = p => ({ p, s: 'saas' });
const CTA = p => ({ p, s: 'contacts' });

// профиль грейда: без звезды, 10 факторов в две колонки
const TWO_COL = [['2>1', 'display: block !important;'], ['2>1>1', 'display: grid !important; grid-template-columns: 1fr 1fr; column-gap: 48px; width: 100% !important; max-width: none !important;'], ['2>1>1>0', 'grid-column: 1 / -1;']];
const GRADE_METHOD = { p: 'grade', s: 'method', rm: ['2>1>0'], cssPath: TWO_COL };
const MENTOR_GRADE = { p: 'mentor', s: 'mentor-grade', rm: ['2>1>0'], cssPath: TWO_COL };
const ACC = { platform: '#63D5FF', grade: '#63D5FF', ai: '#B9AEFF', projects: '#F2C14E', mentor: '#7FDB7A' };

const DECKS = {
  platform: {
    5: [HOME_TOP('company'), PRODUCTS, CORE, { p: 'grade', s: 'top' }, { p: 'ai', s: 'top' }, { p: 'projects', s: 'top' }, { p: 'mentor', s: 'top' }, RESULTS, SAAS('home'), CTA('home')],
    6: [HOME_TOP('company'), PRODUCTS, CORE, shot('level'), shot('efficiency'), shot('losses'), RESULTS, SAAS('home'), CTA('home')],
    7: [HOME_TOP('code'), PRODUCTS, CORE, { p: 'grade', s: 'factors' }, { p: 'ai', s: 'gap' }, { p: 'projects', s: 'audit' }, { p: 'mentor', s: 'mentor-ipr' }, RESULTS, SAAS('home'), CTA('home')],
  },
  grade: {
    5: [{ p: 'grade', s: 'top' }, CORE, GRADE_METHOD, { p: 'grade', s: 'factors' }, { p: 'grade', s: 3 }, { p: 'grade', s: 4 }, SAAS('grade'), CTA('grade')],
    6: [{ p: 'grade', s: 'top' }, GRADE_METHOD, shot('level'), { p: 'grade', s: 'factors' }, shot('rating'), shot('timesheet'), { p: 'grade', s: 3 }, SAAS('grade'), CTA('grade')],
    7: [{ p: 'grade', s: 'top' }, PRODUCTS, CORE, GRADE_METHOD, { p: 'grade', s: 'factors' }, RESULTS, { p: 'grade', s: 4 }, SAAS('grade'), CTA('grade')],
  },
  ai: {
    5: [{ p: 'ai', s: 'top' }, { p: 'ai', s: 'gap' }, { p: 'ai', s: 'measure' }, { p: 'ai', s: 'detect' }, { p: 'ai', s: 'growth' }, { p: 'ai', s: 'prompts', rm: ['1>1', '2>3'] }, { p: 'ai', s: 6 }, SAAS('ai'), CTA('ai')],
    6: [{ p: 'ai', s: 'top' }, { p: 'ai', s: 'gap' }, { p: 'ai', s: 'measure' }, shot('company'), { p: 'ai', s: 'detect' }, shot('efficiency'), { p: 'ai', s: 'growth' }, SAAS('ai'), CTA('ai')],
    7: [{ p: 'ai', s: 'top' }, PRODUCTS, CORE, { p: 'ai', s: 'gap' }, { p: 'ai', s: 'measure' }, { p: 'ai', s: 'detect' }, RESULTS, SAAS('ai'), CTA('ai')],
  },
  projects: {
    5: [{ p: 'projects', s: 'top' }, { p: 'projects', s: 'example', rm: ['2>3'] }, { p: 'projects', s: 'example', rm: ['1', '2>0', '2>1', '2>2'], hideText: ['Ротация в команде', 'Сформировать вакансию'] }, { p: 'projects', s: 'audit' }, { p: 'projects', s: 3 }, { p: 'projects', s: 4 }, SAAS('projects'), CTA('projects')],
    6: [{ p: 'projects', s: 'top' }, { p: 'projects', s: 'example', rm: ['2>3'] }, shot('project'), { p: 'projects', s: 'audit' }, shot('losses'), shot('tech'), { p: 'projects', s: 3 }, SAAS('projects'), CTA('projects')],
    7: [{ p: 'projects', s: 'top' }, PRODUCTS, CORE, { p: 'projects', s: 'example', rm: ['2>3'] }, { p: 'projects', s: 'audit' }, { p: 'projects', s: 3 }, RESULTS, SAAS('projects'), CTA('projects')],
  },
  mentor: {
    5: [{ p: 'mentor', s: 'top' }, { p: 'mentor', s: 'mentor-ai', rm: ['4', '5', '6'] }, { p: 'mentor', s: 'mentor-ai', rm: ['1', '2', '3', '4'] }, { p: 'mentor', s: 'example' }, { p: 'mentor', s: 'mentor-ipr' }, { p: 'mentor', s: 5 }, { p: 'mentor', s: 6 }, SAAS('mentor'), CTA('mentor')],
    6: [{ p: 'mentor', s: 'top' }, { p: 'mentor', s: 'example' }, shot('quality'), { p: 'mentor', s: 'mentor-ai', rm: ['4', '5', '6'] }, shot('code'), { p: 'mentor', s: 'mentor-ipr' }, shot('level'), SAAS('mentor'), CTA('mentor')],
    7: [{ p: 'mentor', s: 'top' }, PRODUCTS, CORE, { p: 'mentor', s: 'mentor-ai', rm: ['4', '5', '6'] }, { p: 'mentor', s: 'example' }, MENTOR_GRADE, { p: 'mentor', s: 'mentor-ipr' }, SAAS('mentor'), CTA('mentor')],
  },
};
const META = [['01-platform', 'Platform', 'platform'], ['02-grade', 'Grade', 'grade'], ['03-ai', 'AI', 'ai'], ['04-projects', 'Projects', 'projects'], ['05-mentor', 'Mentor', 'mentor']];
const VAR = { 5: 'site', 6: 'demo', 7: 'platform' };

exports.SCREENS = SCREENS;
exports.VAR = VAR;
exports.decks = () => {
  const out = [];
  for (const [folder, en, key] of META) for (const v of [5, 6, 7]) out.push({ folder, name: `UpCore-${en}-${v}-${VAR[v]}`, key, acc: ACC[key], slides: DECKS[key][v] });
  return out;
};
