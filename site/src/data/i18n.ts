// Тексты интерфейса вне макетов: меню на телефоне, форма заявки, cookie-баннер, 404.
export type Lang = 'ru' | 'en';

export const ui = {
  ru: {
    menu: 'Меню', close: 'Закрыть меню', platform: 'Платформа', blog: 'Блог', contacts: 'Контакты',
    connect: 'Открыть демо', demo: 'Провести демо',  // раунд 86: новая версия — как в шапке
    products: {
      grade: 'грейд и рейтинг разработчиков',
      ai: 'эффективность ИИ и вайбкодинга',
      projects: 'бюджет проекта и подрядчики',
      mentor: 'ИИ-наставник для каждого',
    },
    form: {
      close: 'Закрыть',
      titles: { demo: 'Провести демо', report: 'Получить пример отчёта', audit: 'Заказать аудит', pilot: 'Заказать бесплатный пилот' },
      leads: {
        demo: 'Проведем быстрый тест на ваших данных и ответим на вопросы. Оставьте контакты — свяжемся в течение рабочего дня.',
        report: 'Пришлём пример отчёта UpCore и расскажем, что он покажет по вашей команде.',
        audit: 'Посчитаем объективную трудоёмкость и бюджет проекта по коду. Расскажите о проекте — свяжемся и обсудим аудит.',
        pilot: 'Покажем работу UpCore на 2–3 ваших репозиториях по истории кода за 6 месяцев. Оставьте контакты — свяжемся в течение рабочего дня.',
      },
      name: 'Имя', company: 'Компания', team: 'Размер команды', teamPh: 'Выберите',
      teamOpts: ['до 10 разработчиков', '10–50', '50–200', 'более 200'],
      contact: 'Телефон, Telegram или почта', contactPh: '+7 900 000-00-00 или @username',
      comment: 'Комментарий', commentPh: 'Что хотите посмотреть или посчитать',
      submit: 'Отправить заявку', sending: 'Отправляем…',
      okTitle: 'Заявка отправлена', okText: 'Спасибо! Мы свяжемся с вами в течение рабочего дня.',
      mailTitle: 'Почти готово', mailText: 'Откроется письмо с заполненной заявкой — отправьте его, и мы свяжемся с вами.',
      error: 'Не удалось отправить. Напишите нам на office@dex-it.ru или в Telegram @IvanGel_Dex.',
      required: 'Заполните имя и контакт для связи.',
      note: 'Нажимая «Отправить заявку», вы соглашаетесь на обработку контактных данных для ответа на заявку.',
    },
    cookie: {
      text: 'Мы используем cookie и Яндекс Метрику, чтобы понимать, как улучшить сайт.',
      accept: 'Хорошо', decline: 'Только необходимые',
    },
    notFound: { title: 'Страница не найдена', text: 'Такой страницы нет. Возможно, её перенесли — начните с главной.', home: 'На главную' },
    skip: 'Перейти к содержанию',
  },
  en: {
    menu: 'Menu', close: 'Close menu', platform: 'Platform', blog: 'Blog', contacts: 'Contacts',
    connect: 'See the demo', demo: 'Book a demo',  // раунд 94: как в шапке новой версии
    products: {
      grade: 'developer grades and ranking',
      ai: 'AI and vibe-coding efficiency',
      projects: 'project budget and vendors',
      mentor: 'an AI mentor for every developer',
    },
    form: {
      close: 'Close',
      titles: { demo: 'Book a demo', report: 'Get a sample report', audit: 'Order an audit', pilot: 'Book a free pilot' },
      leads: {
        demo: 'We’ll run a quick test on your data and answer your questions. Leave your contacts and we’ll get back to you within one business day.',
        report: 'We will send you a sample UpCore report and explain what it will show for your team.',
        audit: 'We will calculate the objective effort and budget of your project from its code. Tell us about the project and we will get in touch.',
        pilot: 'We’ll show UpCore at work on 2–3 of your repositories using 6 months of code history. Leave your contacts and we’ll get back to you within one business day.',
      },
      name: 'Name', company: 'Company', team: 'Team size', teamPh: 'Select',
      teamOpts: ['up to 10 developers', '10–50', '50–200', '200+'],
      contact: 'Phone, Telegram or email', contactPh: '+7 900 000-00-00 or @username',
      comment: 'Comment', commentPh: 'What would you like to see or calculate',
      submit: 'Send request', sending: 'Sending…',
      okTitle: 'Request sent', okText: 'Thank you! We will get back to you within one business day.',
      mailTitle: 'Almost done', mailText: 'An email with your request will open — just send it and we will get in touch.',
      error: 'Could not send. Please email office@dex-it.ru or message @IvanGel_Dex on Telegram.',
      required: 'Please fill in your name and a contact.',
      note: 'By clicking “Send request” you agree to the processing of your contact details to answer your request.',
    },
    cookie: {
      text: 'We use cookies and Yandex Metrica to understand how to improve the website.',
      accept: 'OK', decline: 'Necessary only',
    },
    notFound: { title: 'Page not found', text: 'This page does not exist. It may have moved — start from the home page.', home: 'Go to home page' },
    skip: 'Skip to content',
  },
} as const;

export const PRODUCT_KEYS = ['grade', 'ai', 'projects', 'mentor'] as const;
export const PRODUCT_NAMES = { grade: 'Grade', ai: 'AI', projects: 'Projects', mentor: 'Mentor' } as const;
export const PRODUCT_COLORS = {
  home: { line: '#63D5FF', text: '#63D5FF' }, blog: { line: '#63D5FF', text: '#63D5FF' },
  grade: { line: '#63D5FF', text: '#63D5FF' }, ai: { line: '#9B8CFF', text: '#B9AEFF' },
  projects: { line: '#F2C14E', text: '#F2C14E' }, mentor: { line: '#53C04D', text: '#7FDB7A' },
} as const;

export const CONTACTS = {
  phone: '+7 (985) 848-35-55', phoneHref: 'tel:+79858483555',
  phone2: '+7 (930) 066-46-20', email: 'office@dex-it.ru', telegram: '@IvanGel_Dex', telegramHref: 'https://t.me/IvanGel_Dex',
  channel: 'https://t.me/upcore_ai', app: 'https://demo.up-core.ru/',
};
