// SEO: заголовки, описания и семантика страниц (раунд 69, собрано по темам продукта и блога).
// Семантическое ядро целиком — docs/SEO.md (корень репозитория).
import type { Lang } from './i18n';

export type PageKey = 'home' | 'grade' | 'ai' | 'projects' | 'mentor' | 'blog' | 'blog-2' | 'blog-3';

export const ROUTES: Record<PageKey, string> = {
  home: '', grade: 'grade/', ai: 'ai/', projects: 'projects/', mentor: 'mentor/', blog: 'blog/', 'blog-2': 'blog/2/', 'blog-3': 'blog/3/',
};

type Meta = { title: string; description: string; keywords: string };

export const SEO: Record<Lang, Record<PageKey, Meta>> = {
  ru: {
    home: {
      title: 'UpCore — цифровой тимлид: оценка эффективности разработчиков по коду',
      description: 'UpCore анализирует каждый merge request по 50+ факторам и переводит код в реально затраченные часы: эффективность, грейд и рейтинг разработчиков, эффект ИИ, бюджет проекта. 96% совпадения с экспертной оценкой. Без тайм-трекеров и отчётов.',
      keywords: 'оценка эффективности разработчиков, эффективность разработки, метрики разработки, анализ кода, цифровой тимлид, продуктивность программистов, оценка программистов по коду, управление ИТ-командой',
    },
    grade: {
      title: 'UpCore Grade — грейд и рейтинг разработчиков по коду, 50+ факторов',
      description: 'Объективный грейд Junior–Senior и ежемесячный рейтинг разработчиков по анализу кода: 50+ факторов, главный — эффективность в часах. Каждый фактор раскрывается до строчки кода. Для CTO, HRD и тимлидов.',
      keywords: 'грейд разработчика, грейдирование программистов, оценка уровня разработчика, рейтинг разработчиков, матрица компетенций разработчика, performance review разработчиков, оценка senior middle junior',
    },
    ai: {
      title: 'UpCore AI — эффективность ИИ и вайбкодинга в разработке, в часах и деньгах',
      description: 'Сколько на самом деле экономит ИИ: время «вручную» против времени с ИИ по каждой задаче, автодетект ИИ-кода (точность 92%+), нормы токенов, промпт-ревью. Senior +50…300%, Junior −50…0% — измеряем и разгоняем.',
      keywords: 'эффективность ИИ в разработке, вайбкодинг, AI-ассистенты программирования, оценка эффекта Copilot, детект ИИ-кода, расходы на токены, внедрение ИИ в разработку, продуктивность с ИИ',
    },
    projects: {
      title: 'UpCore Projects — аудит ИТ-подрядчика и бюджета проекта по коду',
      description: 'Проверьте акт подрядчика по коду: объективная трудоёмкость в часах и рублях, эффективность команды, техдолг по ISO 25010, тех-карта и прогноз сроков. Разовый аудит бюджета проекта или ежемесячный контроль подрядчиков.',
      keywords: 'аудит ИТ-подрядчика, проверка акта подрядчика, аудит кода, оценка стоимости разработки, контроль аутсорса разработки, бюджет ИТ-проекта, техдолг, оценка трудоёмкости по коду',
    },
    mentor: {
      title: 'UpCore Mentor — ИИ-наставник и ИИ-ревью кода для каждого разработчика',
      description: 'ИИ-наставник разбирает каждый MR, постановки задач и промпты, находит, где проседает эффективность, и собирает персональный план роста по 50+ факторам грейда. Качество кода 3,2 → 8,0 на примере из демо.',
      keywords: 'ИИ-наставник для разработчиков, ИИ код-ревью, автоматическое код-ревью, развитие разработчиков, ИПР программиста, менторинг разработчиков, онбординг разработчиков, качество кода',
    },
    blog: {
      title: 'Блог UpCore — эффективность разработки, ИИ и управление ИТ-командами',
      description: 'Посты Ивана Гель и команды UpCore: как оценивать разработчиков по коду, сколько стоит код, code churn, эффективность ИИ, аудит подрядчиков и ROI цифрового тимлида.',
      keywords: 'блог об эффективности разработки, управление разработкой, оценка программистов, code churn, эффективность ИИ, ROI разработки',
    },
    'blog-2': {
      title: 'Блог UpCore — страница 2',
      description: 'Посты канала «ИИ-тимлид UpCore»: знакомство с продуктом, аудит за 1 клик, оценка эффективности и грейда разработчиков.',
      keywords: 'блог UpCore, эффективность разработчиков, аудит разработки',
    },
    'blog-3': {
      title: 'Блог UpCore — страница 3',
      description: 'Посты канала «ИИ-тимлид UpCore»: ROI цифрового тимлида, закон Гудхарта, эпоха вайбкодинга.',
      keywords: 'блог UpCore, ROI разработки, вайбкодинг',
    },
  },
  en: {
    home: {
      title: 'UpCore — a digital team lead: developer efficiency measured from code',
      description: 'UpCore analyzes every merge request across 50+ factors and turns code into the hours actually spent: developer efficiency, grade and ranking, AI impact, project budget. 96% agreement with expert assessment. No time trackers, no reports.',
      keywords: 'developer productivity, engineering efficiency, software engineering metrics, code analysis, developer performance, engineering intelligence, digital team lead',
    },
    grade: {
      title: 'UpCore Grade — developer grades and ranking from code, 50+ factors',
      description: 'An objective Junior-to-Senior grade and a monthly developer ranking based on code analysis: 50+ factors, efficiency in hours first. Every factor drills down to the line of code. For CTOs, HR directors and team leads.',
      keywords: 'developer grade, developer leveling, engineering career ladder, developer ranking, developer performance review, senior middle junior assessment',
    },
    ai: {
      title: 'UpCore AI — the real impact of AI and vibe coding, in hours and money',
      description: 'How much AI actually saves: manual time vs. time with AI for every task, AI-code detection (92%+ accuracy), token budgets, prompt review. Seniors +50–300%, juniors −50–0% — we measure it and help you speed up.',
      keywords: 'AI coding productivity, vibe coding, AI coding assistants ROI, measure Copilot impact, AI-generated code detection, LLM token costs, AI adoption in engineering',
    },
    projects: {
      title: 'UpCore Projects — audit IT vendors and project budgets from code',
      description: 'Check a vendor’s invoice against the code: objective effort in hours and money, team efficiency, ISO 25010 tech debt, tech map and delivery forecast. A one-off project budget audit or monthly vendor control.',
      keywords: 'IT vendor audit, software vendor management, code audit, software development cost estimation, outsourcing control, IT project budget, technical debt',
    },
    mentor: {
      title: 'UpCore Mentor — an AI mentor and AI code review for every developer',
      description: 'The AI mentor reviews every MR, task description and prompt, finds where efficiency drops and builds a personal growth plan across 50+ grade factors. Code quality 3.2 → 8.0 in the demo example.',
      keywords: 'AI mentor for developers, AI code review, automated code review, developer growth plan, engineering mentoring, developer onboarding, code quality',
    },
    blog: {
      title: 'UpCore Blog — engineering efficiency, AI and managing IT teams',
      description: 'Posts by Ivan Gel and the UpCore team: measuring developers by code, what code really costs, code churn, AI efficiency, vendor audits and the ROI of a digital team lead.',
      keywords: 'engineering efficiency blog, software engineering management, developer productivity, code churn, AI coding',
    },
    'blog-2': {
      title: 'UpCore Blog — page 2',
      description: 'Posts from the “AI Team Lead UpCore” channel: getting to know the product, one-click audit, measuring developer efficiency and grade.',
      keywords: 'UpCore blog, developer efficiency, engineering audit',
    },
    'blog-3': {
      title: 'UpCore Blog — page 3',
      description: 'Posts from the “AI Team Lead UpCore” channel: digital team lead ROI, Goodhart’s law, the era of vibe coding.',
      keywords: 'UpCore blog, engineering ROI, vibe coding',
    },
  },
};
