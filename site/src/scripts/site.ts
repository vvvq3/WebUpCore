// Поведение сайта UpCore: шапка, меню на телефоне, слайдер, форма заявки, cookie и Метрика, анимации.
// Анимации — по docs/design/ANIMATIONS.md (утверждено, раунд 67): один раз при появлении, 200–800 мс, «уменьшить движение» уважается.

const root = document.documentElement;
const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const lang = (document.body.dataset.lang || 'ru') as 'ru' | 'en';
// класс анимаций ставится сразу, до разметки элементов — иначе скрытие запустится переходом с задержкой
if (!reduced && 'IntersectionObserver' in window) root.classList.add('uc-js');

/* ---------------- Аналитика: Яндекс Метрика после согласия ---------------- */
const ymId = Number(document.querySelector<HTMLMetaElement>('meta[name="uc-ym"]')?.content || 0);
const CONSENT_KEY = 'uc-consent';
let ymLoaded = false;

function store(key: string, value?: string): string | null {
  try {
    if (value !== undefined) localStorage.setItem(key, value);
    return localStorage.getItem(key);
  } catch { return null; }
}

function loadMetrika() {
  if (!ymId || ymLoaded) return;
  ymLoaded = true;
  const w = window as any;
  w.ym = w.ym || function (...args: unknown[]) { (w.ym.a = w.ym.a || []).push(args); };
  w.ym.l = Date.now();
  const s = document.createElement('script');
  s.async = true;
  s.src = 'https://mc.yandex.ru/metrika/tag.js';
  document.head.appendChild(s);
  w.ym(ymId, 'init', { clickmap: true, trackLinks: true, accurateTrackBounce: true, webvisor: true });
}

export function goal(name: string, params?: Record<string, unknown>) {
  const w = window as any;
  if (ymId && ymLoaded && typeof w.ym === 'function') w.ym(ymId, 'reachGoal', name, params);
}

function initCookie() {
  const box = document.getElementById('uc-cookie');
  if (!ymId) return;
  const consent = store(CONSENT_KEY);
  if (consent === 'accept') { loadMetrika(); return; }
  if (consent === 'decline' || !box) return;
  box.hidden = false;
  box.addEventListener('click', (ev) => {
    const b = (ev.target as HTMLElement).closest<HTMLButtonElement>('[data-cookie]');
    if (!b) return;
    store(CONSENT_KEY, b.dataset.cookie!);
    box.hidden = true;
    if (b.dataset.cookie === 'accept') loadMetrika();
  });
}

function initGoals() {
  document.addEventListener('click', (ev) => {
    const a = (ev.target as HTMLElement).closest<HTMLAnchorElement>('a');
    if (!a || a.dataset.form) return;
    const h = a.getAttribute('href') || '';
    if (h.startsWith('https://demo.up-core.ru')) goal('connect');
    else if (h.startsWith('tel:')) goal('phone');
    else if (h.includes('t.me/IvanGel_Dex')) goal('telegram');
    else if (h.startsWith('mailto:')) goal('email');
    else if (h.includes('t.me/upcore_ai')) goal('channel');
  });
}

/* ---------------- Прокрутка при переходе между страницами ----------------
   Новая страница всегда открывается сверху (если в адресе нет #якоря): браузер и окна предпросмотра
   иначе могут сохранить прокрутку прошлой страницы. Кнопка «Назад» по-прежнему возвращает на прежнее место. */
function initScrollReset() {
  const nav = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming | undefined;
  const back = nav?.type === 'back_forward';
  if (!back && !location.hash) {
    if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
    const top = () => window.scrollTo({ top: 0, left: 0, behavior: 'instant' as ScrollBehavior });
    top();
    window.addEventListener('pageshow', (ev) => { if (!ev.persisted) top(); });
  } else if ('scrollRestoration' in history) {
    history.scrollRestoration = 'auto';
  }
}

/* ---------------- Шапка ---------------- */
function initHeader() {
  const onScroll = () => root.classList.toggle('uc-scrolled', window.scrollY > 40);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
}

/* ---------------- Меню на телефоне ---------------- */
function initMenu() {
  const menu = document.getElementById('uc-menu');
  if (!menu) return;
  let opener: HTMLElement | null = null;
  const open = (from: HTMLElement) => {
    opener = from;
    menu.hidden = false;
    menu.classList.add('uc-open');
    document.body.style.overflow = 'hidden';
    menu.querySelector<HTMLElement>('[data-menu-close]')?.focus();
  };
  const close = () => {
    menu.hidden = true;
    menu.classList.remove('uc-open');
    document.body.style.overflow = '';
    opener?.focus();
  };
  document.querySelectorAll<HTMLAnchorElement>('.uc-burger').forEach((b) => {
    b.setAttribute('role', 'button');
    b.setAttribute('aria-controls', 'uc-menu');
    b.setAttribute('aria-expanded', 'false');
    b.addEventListener('click', (ev) => { ev.preventDefault(); open(b); b.setAttribute('aria-expanded', 'true'); });
  });
  menu.addEventListener('click', (ev) => {
    const t = ev.target as HTMLElement;
    if (t.closest('[data-menu-close]') || t.closest('a[data-form]')) {
      close();
      document.querySelectorAll('.uc-burger').forEach((b) => b.setAttribute('aria-expanded', 'false'));
    }
  });
  document.addEventListener('keydown', (ev) => { if (ev.key === 'Escape' && !menu.hidden) close(); });
  window.matchMedia('(min-width: 1161px)').addEventListener('change', (m) => { if (m.matches && !menu.hidden) close(); });
}

/* ---------------- Форма заявки ---------------- */
function initLeadForm() {
  const dlg = document.getElementById('uc-lead') as HTMLDialogElement | null;
  if (!dlg) return;
  const form = dlg.querySelector('form')!;
  const titles = JSON.parse(dlg.dataset.titles || '{}');
  const leads = JSON.parse(dlg.dataset.leads || '{}');
  const titleEl = dlg.querySelector('#uc-lead-title')!;
  const leadEl = dlg.querySelector('[data-lead-lead]')!;
  const errEl = dlg.querySelector<HTMLElement>('[data-lead-error]')!;
  const body = dlg.querySelector<HTMLElement>('.uc-lead__body')!;
  const done = dlg.querySelector<HTMLElement>('[data-lead-done]')!;
  const submit = dlg.querySelector<HTMLButtonElement>('[data-lead-submit]')!;
  let topic = 'demo';

  const openForm = (tp: string) => {
    topic = titles[tp] ? tp : 'demo';
    titleEl.textContent = titles[topic];
    leadEl.textContent = leads[topic];
    (form.elements.namedItem('topic') as HTMLInputElement).value = topic;
    body.hidden = false; done.hidden = true; errEl.hidden = true;
    if (typeof dlg.showModal === 'function') dlg.showModal(); else dlg.setAttribute('open', '');
    // раунд 89: на телефоне курсор в поле не ставим — человек сначала видит всю форму (без клавиатуры)
    if (matchMedia('(hover: hover) and (pointer: fine)').matches) (form.elements.namedItem('name') as HTMLInputElement).focus();
    else { dlg.setAttribute('tabindex', '-1'); dlg.focus({ preventScroll: true }); dlg.scrollTop = 0; } // фокус на окне, а не в поле — клавиатура не открывается
    goal('form_open_' + topic);
  };
  document.addEventListener('click', (ev) => {
    const a = (ev.target as HTMLElement).closest<HTMLElement>('[data-form]');
    if (!a) return;
    ev.preventDefault();
    openForm(a.dataset.form || 'demo');
  });
  dlg.querySelector('[data-lead-close]')!.addEventListener('click', () => dlg.close());
  dlg.addEventListener('click', (ev) => { if (ev.target === dlg) dlg.close(); });

  form.addEventListener('submit', async (ev) => {
    ev.preventDefault();
    const fd = new FormData(form);
    const name = String(fd.get('name') || '').trim();
    const contact = String(fd.get('contact') || '').trim();
    form.querySelectorAll('[aria-invalid]').forEach((el) => el.removeAttribute('aria-invalid'));
    if (!name || !contact) {
      if (!name) (form.elements.namedItem('name') as HTMLElement).setAttribute('aria-invalid', 'true');
      if (!contact) (form.elements.namedItem('contact') as HTMLElement).setAttribute('aria-invalid', 'true');
      errEl.textContent = dlg.dataset.msgRequired || ''; errEl.hidden = false; return;
    }
    if (fd.get('website')) return; // защита от ботов
    errEl.hidden = true;
    const endpoint = dlg.dataset.endpoint;
    const tgEndpoint = dlg.dataset.tg;
    const showDone = (title: string, text: string) => {
      body.hidden = true; done.hidden = false;
      done.querySelector('[data-lead-done-title]')!.textContent = title;
      done.querySelector('[data-lead-done-text]')!.textContent = text;
    };
    const labels = lang === 'ru'
      ? { name: 'Имя', company: 'Компания', team: 'Размер команды', contact: 'Контакт', page: 'Страница', topic: 'Тема' }
      : { name: 'Name', company: 'Company', team: 'Team size', contact: 'Contact', page: 'Page', topic: 'Topic' };
    const subject = `UpCore — ${titles[topic]}`;
    if (endpoint || tgEndpoint) {
      submit.disabled = true; submit.textContent = dlg.dataset.msgSending || '';
      // раунд 92: письмо через FormSubmit — поля с русскими подписями, тема письма, без капчи
      const sendMail = async (): Promise<boolean> => {
        if (!endpoint) return false;
        try {
          let payload: FormData = fd;
          if (endpoint.includes('formsubmit.co')) {
            payload = new FormData();
            payload.append(labels.topic, titles[topic]);
            (['name', 'company', 'team', 'contact'] as const).forEach((k) => payload.append(labels[k], String(fd.get(k) || '—')));
            payload.append(labels.page, location.href);
            payload.append('_subject', subject); payload.append('_template', 'table'); payload.append('_captcha', 'false');
          }
          const r = await fetch(endpoint, { method: 'POST', body: payload, headers: { Accept: 'application/json' } });
          const j = await r.json().catch(() => ({}));
          return r.ok && j.success !== false && j.success !== 'false' && j.ok !== false;
        } catch { return false; }
      };
      // раунд 99: копия заявки в Telegram через свой обработчик (nginx/lead.js)
      const sendTg = async (): Promise<boolean> => {
        if (!tgEndpoint) return false;
        try {
          const r = await fetch(tgEndpoint, {
            method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
            body: JSON.stringify({ topic: titles[topic], name: fd.get('name'), company: fd.get('company'), team: fd.get('team'),
              contact: fd.get('contact'), page: location.href, lang }),
          });
          const j = await r.json().catch(() => ({}));
          return r.ok && j.ok === true;
        } catch { return false; }
      };
      const [mailOk, tgOk] = await Promise.all([sendMail(), sendTg()]);
      const sent = mailOk || tgOk;
      submit.disabled = false; submit.textContent = dlg.dataset.msgSubmit || '';
      if (sent) {
        goal('form_sent_' + topic);
        form.reset();
        showDone(dlg.dataset.msgOkTitle || '', dlg.dataset.msgOkText || '');
        return;
      }
      // не дошло (сервис недоступен или форма ещё не активирована) — заявку не теряем: открываем письмо с заполненными полями
    }
    // Нет обработчика — письмо на почту с заполненной заявкой.
    const lines = (['name', 'company', 'team', 'contact'] as const)
      .map((k) => `${labels[k]}: ${String(fd.get(k) || '—')}`).concat(`${labels.page}: ${location.href}`);
    location.href = `mailto:${dlg.dataset.email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(lines.join('\n'))}`;
    goal('form_sent_' + topic, { via: 'mailto' });
    showDone(dlg.dataset.msgMailTitle || '', dlg.dataset.msgMailText || '');
  });
}

/* ---------------- Слайдер скриншотов (главная) ---------------- */
function initSlider() {
  // Раунд 101: возвращён эффект раунда 77 — голубая полоса идёт сверху вниз за 1,5 с и «рисует» новый экран
  // (выше полосы уже новый, ниже — ещё старый). Между сменами экран держится 3,5 с (раунд 102: было 5 с, −30%).
  // Раунд 102: сразу грузится только первый экран; следующий подгружается заранее, пока показывается текущий (data-src → src).
  // Пауза при наведении мыши, когда окно вне экрана и когда вкладка скрыта; при «уменьшить движение» — без автосмены.
  document.querySelectorAll<HTMLElement>('[data-slider]').forEach((box) => {
    const imgs = [...box.querySelectorAll<HTMLImageElement>('[data-slide]')];
    const scan = box.querySelector<HTMLElement>('.uc-scan');
    const keyEl = box.querySelector('[data-slide-key]');
    const numEl = box.querySelector('[data-slide-num]');
    if (scan) { scan.classList.remove('uc-scan'); scan.style.top = '0'; scan.style.opacity = '0'; scan.style.zIndex = '3'; }
    const WIPE = 1500; // проход полосы = смена экрана, мс
    const HOLD = 3500; // сколько показывается экран между сменами, мс
    const n = imgs.length;
    if (n < 2 || reduced || !imgs[0].animate) return;
    let idx = 0;
    let busy = false;
    let hover = false;
    let visible = true;
    let timer = 0;
    imgs.forEach((im, k) => { im.style.zIndex = k === 0 ? '1' : '0'; });
    const load = (im: HTMLImageElement) => { if (!im.getAttribute('src') && im.dataset.src) im.src = im.dataset.src; };
    const ready = (im: HTMLImageElement) => new Promise<void>((res) => { load(im); if (im.complete && im.naturalWidth) res(); else { im.addEventListener('load', () => res(), { once: true }); im.addEventListener('error', () => res(), { once: true }); } });
    const preload = () => load(imgs[(idx + 1) % n]); // следующий экран — заранее, пока показывается текущий
    const canRun = () => visible && !hover && !document.hidden;
    const schedule = () => { window.clearTimeout(timer); if (!busy && canRun()) timer = window.setTimeout(step, HOLD); };
    const step = async () => {
      if (busy || !canRun()) return;
      busy = true;
      const next = imgs[(idx + 1) % n];
      await ready(next); // смена начинается, только когда следующий экран загружен
      if (!canRun()) { busy = false; return; }
      const prev = idx;
      idx = (idx + 1) % n;
      preload();
      const old = imgs[prev];
      old.style.visibility = 'visible'; old.style.zIndex = '1';
      next.style.visibility = 'visible'; next.style.zIndex = '2';
      if (keyEl) keyEl.textContent = box.dataset['k' + idx] || '';
      if (numEl) numEl.textContent = String(idx + 1).padStart(2, '0');
      const wipe = next.animate([{ clipPath: 'inset(0 0 100% 0)' }, { clipPath: 'inset(0 0 0% 0)' }], { duration: WIPE, easing: 'linear', fill: 'forwards' });
      if (scan) { scan.style.opacity = '1'; scan.animate([{ top: '0%' }, { top: '100%' }], { duration: WIPE, easing: 'linear' }); }
      wipe.onfinish = () => {
        old.style.visibility = 'hidden'; old.style.zIndex = '0'; next.style.zIndex = '1';
        wipe.cancel(); next.style.clipPath = '';
        if (scan) scan.style.opacity = '0';
        busy = false;
        schedule();
      };
    };
    if (matchMedia('(hover: hover) and (pointer: fine)').matches) {
      box.addEventListener('mouseenter', () => { hover = true; window.clearTimeout(timer); });
      box.addEventListener('mouseleave', () => { hover = false; schedule(); });
    }
    document.addEventListener('visibilitychange', schedule);
    if ('IntersectionObserver' in window) new IntersectionObserver((es) => { visible = es[0].isIntersecting; schedule(); }).observe(box);
    // следующий экран начинаем грузить после полной загрузки страницы — не мешаем логотипу, шрифтам и первому экрану
    if (document.readyState === 'complete') preload(); else window.addEventListener('load', preload, { once: true });
    schedule();
  });
}

/* ---------------- Главная: анимация блока #core ---------------- */
function initCore() {
  const core = document.querySelector<HTMLElement>('#core');
  if (!core || reduced || !('IntersectionObserver' in window)) return;
  const strikes = [...core.querySelectorAll<HTMLElement>('span')].filter((s) => (s.getAttribute('style') || '').includes('line-through'));
  strikes.forEach((s, i) => { s.classList.add('uc-strike'); s.style.setProperty('--d', 100 + i * 150 + 'ms'); });
  const circles = core.querySelectorAll<SVGCircleElement>('svg circle');
  const arc = circles[1];
  const full = arc ? (arc.getAttribute('stroke-dasharray') || '').split(' ').map(Number) : [];
  const num = core.querySelector<SVGTextElement>('svg text');
  if (arc && full.length === 2) {
    arc.style.strokeDasharray = `${full[1]} ${full[1]}`; // старт: полное кольцо — «160 часов выглядят продуктивно»
    arc.getBoundingClientRect();
    requestAnimationFrame(() => arc.classList.add('uc-core-arc'));
  }
  const rows = [...core.querySelectorAll<HTMLElement>('svg + div > div')];
  rows.forEach((r, i) => { r.classList.add('uc-core-row'); r.style.setProperty('--d', 700 + i * 200 + 'ms'); });
  const loss = [...core.querySelectorAll<HTMLElement>('b')].find((b) => /140/.test(b.textContent || ''));
  loss?.classList.add('uc-core-loss');
  const target = Number(num?.textContent || 0);
  if (num && target) num.textContent = String(target * 2); // до анимации — «160 часов выглядят продуктивно»
  const box = (arc?.closest('div[style*="flex-direction: column"]') as HTMLElement) || core;
  const io = new IntersectionObserver((ents) => {
    if (!ents.some((e) => e.isIntersecting)) return;
    io.disconnect();
    box.classList.add('uc-core-on');
    if (arc && full.length === 2) requestAnimationFrame(() => { arc.style.strokeDasharray = `${full[0]} ${full[1]}`; });
    if (num && target) {
      const from = target * 2; const t0 = performance.now() + 600; const dur = 1100;
      const tick = (t: number) => {
        const k = Math.min(1, Math.max(0, (t - t0) / dur));
        const e = k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2;
        num.textContent = String(Math.round(from - (from - target) * e));
        if (k < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    }
  }, { rootMargin: '0px 0px -15% 0px', threshold: 0 }); // раунд 90: старт, как только верх карточки поднялся выше 85% экрана (на телефоне карточка высокая)
  io.observe(box);
}

/* ---------------- Фильтр блога по темам ---------------- */
function initBlogFilter() {
  const bar = document.querySelector<HTMLElement>('[data-blog-filter]');
  if (!bar) return;
  const paged = document.querySelector<HTMLElement>('[data-blog-paged]');
  const all = document.querySelector<HTMLElement>('[data-blog-all]');
  const empty = all?.querySelector<HTMLElement>('[data-blog-empty]');
  if (!paged || !all) return;
  const apply = (f: string) => {
    bar.querySelectorAll<HTMLButtonElement>('[data-filter]').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.filter === f)));
    const on = f !== 'all';
    paged.hidden = on;
    all.hidden = !on;
    let n = 0;
    all.querySelectorAll<HTMLElement>('article[data-cat]').forEach((a) => {
      const show = a.dataset.cat === f;
      a.hidden = !show;
      if (show) { n += 1; a.classList.add('uc-on'); }
    });
    if (empty) empty.hidden = n > 0 || !on;
  };
  bar.addEventListener('click', (ev) => {
    const b = (ev.target as HTMLElement).closest<HTMLButtonElement>('[data-filter]');
    if (b) apply(b.dataset.filter || 'all');
  });
}

/* ---------------- Разметка для анимаций ---------------- */
function tagElements() {
  const main = document.getElementById('main');
  if (!main) return;
  // кнопки
  document.querySelectorAll<HTMLAnchorElement>('header a[style*="min-height"], main a[style*="min-height: 52px"], main a[style*="min-height: 48px"], main a[style*="min-height: 44px"]').forEach((a) => {
    a.classList.add('uc-btn');
    const bg = getComputedStyle(a).backgroundColor;
    const solid = bg && !/rgba\([^)]*,\s*0(\.\d+)?\)$/.test(bg) && bg !== 'transparent';
    if (!solid) a.classList.add('uc-btn--ghost');
    else a.style.setProperty('--glow', bg);
    if (a.closest('#contacts')) a.classList.add('uc-btn--on-color');
  });
  // карточки
  main.querySelectorAll<HTMLElement>('article').forEach((el) => el.classList.add('uc-card'));
  // подсветка за курсором — снята в раунде 100
}

/* ---------------- Появление и шкалы ---------------- */
function initMotion() {
  if (reduced || !('IntersectionObserver' in window)) return;
  const main = document.getElementById('main')!;
  root.classList.add('uc-js');
  // кандидаты на появление: заголовки секций, карточки, элементы сеток; оставляем самые «мелкие» (без вложенных кандидатов)
  const sel = 'section > *, article, .g2 > *, .g3 > *, .g4 > *, .g4m2 > *, .uc-row > *';
  const cands = new Set<HTMLElement>([...main.querySelectorAll<HTMLElement>(sel)].filter((el) => !el.closest('header') && !el.closest('[data-slider]') && el.getAttribute('aria-hidden') !== 'true' && !el.closest('[data-blog-all]') && !el.closest('main > div > section:first-of-type') && !(el.closest('#core') && el.closest('div[style*="background: #0B0A12"]'))));
  const leaves = [...cands].filter((el) => ![...cands].some((o) => o !== el && el.contains(o)));
  leaves.forEach((el) => {
    const sibs = [...(el.parentElement?.children || [])].filter((s) => leaves.includes(s as HTMLElement));
    el.style.setProperty('--d', Math.min(sibs.indexOf(el), 3) * 60 + 'ms');
    el.classList.add('uc-reveal');
  });
  // шкалы: div с шириной в % и высотой 100% внутри дорожки
  const bars = [...main.querySelectorAll<HTMLElement>('div[style*="height: 100%"][style*="width:"]')].filter((el) => /width:\s*\d+(\.\d+)?%/.test(el.getAttribute('style') || '') && (el.parentElement?.getBoundingClientRect().height || 99) <= 24);
  bars.forEach((el) => {
    const sibs = bars.filter((b) => b.closest('section') === el.closest('section'));
    el.style.setProperty('--d', Math.min(sibs.indexOf(el), 5) * 60 + 'ms');
    el.classList.add('uc-bar');
  });
  // цифры-табло сняты в раунде 100: цифры статичные и появляются вместе со своим блоком.
  // Раунд 81: наблюдатель + «страховка» по прокрутке — при мгновенном прыжке (клавиша End, переход по #якорю)
  // наблюдатель может не сработать, и пролистанные блоки оставались бы невидимыми.
  const pending = new Set<HTMLElement>([...leaves, ...bars]);
  const show = (el: HTMLElement) => { pending.delete(el); el.classList.add('uc-on'); io.unobserve(el); };
  const io = new IntersectionObserver((entries) => {
    entries.forEach((en) => { if (en.isIntersecting) show(en.target as HTMLElement); });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
  pending.forEach((el) => io.observe(el));
  const vh = () => window.innerHeight || document.documentElement.clientHeight;
  let ticking = false;
  const sweep = () => {
    ticking = false;
    const h = vh();
    const atEnd = window.scrollY + h >= document.documentElement.scrollHeight - 4;
    pending.forEach((el) => { const r = el.getBoundingClientRect(); if (r.bottom < 0 || r.top < h * 0.92 || (atEnd && r.top < h)) show(el); });
    if (!pending.size) { window.removeEventListener('scroll', onScroll); window.removeEventListener('hashchange', onScroll); }
  };
  const onScroll = () => { if (!ticking) { ticking = true; requestAnimationFrame(sweep); } };
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('hashchange', onScroll);
  window.setTimeout(onScroll, 400); // открытие страницы сразу на #якоре или с восстановленной прокруткой
}

initScrollReset();
initHeader();
initMenu();
initSlider();
initLeadForm();
initBlogFilter();
initCore();
initCookie();
initGoals();
tagElements();
initMotion();
