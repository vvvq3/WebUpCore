// Поведение сайта UpCore: шапка, меню на телефоне, слайдер, форма заявки, cookie и Метрика, анимации.
// Анимации — по docs/design/ANIMATIONS.md (утверждено, раунд 67): один раз при появлении, 200–800 мс, «уменьшить движение» уважается.

const root = document.documentElement;
const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
const lang = (document.body.dataset.lang || 'ru') as 'ru' | 'en';

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
  window.matchMedia('(min-width: 721px)').addEventListener('change', (m) => { if (m.matches && !menu.hidden) close(); });
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
    (form.elements.namedItem('name') as HTMLInputElement).focus();
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
    const showDone = (title: string, text: string) => {
      body.hidden = true; done.hidden = false;
      done.querySelector('[data-lead-done-title]')!.textContent = title;
      done.querySelector('[data-lead-done-text]')!.textContent = text;
    };
    if (endpoint) {
      submit.disabled = true; submit.textContent = dlg.dataset.msgSending || '';
      try {
        const r = await fetch(endpoint, { method: 'POST', body: fd, headers: { Accept: 'application/json' } });
        if (!r.ok) throw new Error(String(r.status));
        goal('form_sent_' + topic);
        form.reset();
        showDone(dlg.dataset.msgOkTitle || '', dlg.dataset.msgOkText || '');
      } catch {
        errEl.textContent = dlg.dataset.msgError || ''; errEl.hidden = false;
      } finally {
        submit.disabled = false; submit.textContent = dlg.dataset.msgSubmit || '';
      }
      return;
    }
    // Нет обработчика — письмо на почту с заполненной заявкой.
    const labels = lang === 'ru'
      ? { name: 'Имя', company: 'Компания', team: 'Размер команды', contact: 'Контакт', comment: 'Комментарий', page: 'Страница' }
      : { name: 'Name', company: 'Company', team: 'Team size', contact: 'Contact', comment: 'Comment', page: 'Page' };
    const lines = (['name', 'company', 'team', 'contact', 'comment'] as const)
      .map((k) => `${labels[k]}: ${String(fd.get(k) || '—')}`).concat(`${labels.page}: ${location.href}`);
    const subject = `UpCore — ${titles[topic]}`;
    location.href = `mailto:${dlg.dataset.email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(lines.join('\n'))}`;
    goal('form_sent_' + topic, { via: 'mailto' });
    showDone(dlg.dataset.msgMailTitle || '', dlg.dataset.msgMailText || '');
  });
}

/* ---------------- Слайдер скриншотов (главная) ---------------- */
function initSlider() {
  document.querySelectorAll<HTMLElement>('[data-slider]').forEach((box) => {
    const imgs = [...box.querySelectorAll<HTMLImageElement>('[data-slide]')];
    const btns = [...box.querySelectorAll<HTMLButtonElement>('[data-slide-btn]')];
    const play = box.querySelector<HTMLButtonElement>('[data-slide-play]')!;
    const n = imgs.length;
    let idx = 0;
    let timer = 0;
    const set = (i: number) => {
      idx = (i + n) % n;
      imgs.forEach((im, k) => {
        im.style.visibility = k === idx ? 'visible' : 'hidden';
        im.classList.toggle('uc-in', k === idx);
        if (Math.abs(k - idx) <= 1) im.loading = 'eager';
      });
      btns.forEach((b, k) => b.setAttribute('aria-selected', String(k === idx)));
      box.querySelector('[data-slide-key]')!.textContent = box.dataset['k' + idx] || '';
      box.querySelector('[data-slide-title]')!.textContent = box.dataset['t' + idx] || '';
      box.querySelector('[data-slide-caption]')!.textContent = box.dataset['c' + idx] || '';
      box.querySelector('[data-slide-num]')!.textContent = '0' + (idx + 1);
      // перезапуск полосы прогресса на активной кнопке
      const prog = btns[idx]?.querySelector<HTMLElement>('.uc-prog');
      if (prog) { prog.style.animation = 'none'; void prog.offsetWidth; prog.style.animation = ''; }
    };
    const labels = lang === 'ru' ? ['Остановить автопрокрутку', 'Включить автопрокрутку'] : ['Pause autoplay', 'Resume autoplay'];
    const start = () => { stop(); box.setAttribute('data-playing', ''); timer = window.setInterval(() => set(idx + 1), 4500); upd(); };
    const stop = () => { window.clearInterval(timer); timer = 0; box.removeAttribute('data-playing'); upd(); };
    const upd = () => {
      const on = Boolean(timer);
      play.setAttribute('aria-label', on ? labels[0] : labels[1]);
      play.querySelector<SVGElement>('[data-icon-pause]')!.style.display = on ? '' : 'none';
      play.querySelector<SVGElement>('[data-icon-play]')!.style.display = on ? 'none' : '';
    };
    btns.forEach((b, k) => b.addEventListener('click', () => { set(k); if (timer) start(); }));
    play.addEventListener('click', () => (timer ? stop() : start()));
    if (reduced) stop(); else start();
    set(0);
  });
}

/* ---------------- Разметка для анимаций ---------------- */
function tagElements() {
  const main = document.getElementById('main');
  if (!main) return;
  // кнопки
  main.querySelectorAll<HTMLAnchorElement>('a[style*="min-height: 52px"], a[style*="min-height: 44px"]').forEach((a) => {
    a.classList.add('uc-btn');
    if (!a.style.background && !a.style.backgroundColor) a.classList.add('uc-btn--ghost');
  });
  // карточки
  main.querySelectorAll<HTMLElement>('article').forEach((el) => el.classList.add('uc-card'));
  // подсветка за курсором: карточки продуктов на главной и плашки «> UpCore.X»
  const spots: HTMLElement[] = [];
  if (document.body.dataset.page === 'home') main.querySelectorAll<HTMLElement>('#products article').forEach((el) => spots.push(el));
  main.querySelectorAll<HTMLAnchorElement>('a[href*="/grade/"], a[href*="/ai/"], a[href*="/projects/"], a[href*="/mentor/"]').forEach((a) => {
    if (!a.closest('header') && a.textContent?.includes('UpCore')) spots.push(a);
  });
  spots.forEach((el) => {
    el.classList.add('uc-spot');
    const c = getComputedStyle(el).borderTopColor;
    if (c) el.style.setProperty('--spot', c.replace(/rgba?\(([^)]+)\)/, (m, v) => `rgb(${v.split(',').slice(0, 3).join(',')})`));
  });
  if (finePointer) {
    spots.forEach((el) => el.addEventListener('pointermove', (ev) => {
      const r = el.getBoundingClientRect();
      el.style.setProperty('--mx', ev.clientX - r.left + 'px');
      el.style.setProperty('--my', ev.clientY - r.top + 'px');
    }));
  }
}

/* ---------------- Появление, шкалы, табло ---------------- */
function initMotion() {
  if (reduced || !('IntersectionObserver' in window)) return;
  const main = document.getElementById('main')!;
  root.classList.add('uc-js');
  // кандидаты на появление: заголовки секций, карточки, элементы сеток; оставляем самые «мелкие» (без вложенных кандидатов)
  const sel = 'section > *, article, .g2 > *, .g3 > *, .g4 > *, .g4m2 > *, .uc-row > *';
  const cands = new Set<HTMLElement>([...main.querySelectorAll<HTMLElement>(sel)].filter((el) => !el.closest('header') && !el.closest('[data-slider]')));
  const leaves = [...cands].filter((el) => ![...cands].some((o) => o !== el && el.contains(o)));
  leaves.forEach((el) => {
    const sibs = [...(el.parentElement?.children || [])].filter((s) => leaves.includes(s as HTMLElement));
    el.style.setProperty('--d', Math.min(sibs.indexOf(el), 6) * 80 + 'ms');
    el.classList.add('uc-reveal');
  });
  // шкалы: div с шириной в % и высотой 100% внутри дорожки
  const bars = [...main.querySelectorAll<HTMLElement>('div[style*="height: 100%"][style*="width:"]')].filter((el) => /width:\s*\d+(\.\d+)?%/.test(el.getAttribute('style') || '') && (el.parentElement?.getBoundingClientRect().height || 99) <= 24);
  bars.forEach((el) => {
    const sibs = bars.filter((b) => b.closest('section') === el.closest('section'));
    el.style.setProperty('--d', Math.min(sibs.indexOf(el), 8) * 100 + 'ms');
    el.classList.add('uc-bar');
  });
  // цифры-табло: ключевые цифры первых экранов (data-odo)
  const odos = [...main.querySelectorAll<HTMLElement>('[data-odo]')];
  odos.forEach((el, i) => {
    const text = el.textContent || '';
    el.setAttribute('aria-label', text);
    el.innerHTML = [...text].map((ch, k) => (/\d/.test(ch)
      ? `<span class="uc-odo" aria-hidden="true"><span class="uc-odo__col" style="--d:${(i % 4) * 120 + k * 60}ms" data-digit="${ch}">${'0123456789'.split('').map((d) => `<span>${d}</span>`).join('')}</span></span>`
      : `<span aria-hidden="true">${ch === ' ' ? '&nbsp;' : ch}</span>`)).join('');
  });
  const io = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (!en.isIntersecting) return;
      const el = en.target as HTMLElement;
      el.classList.add('uc-on');
      el.querySelectorAll<HTMLElement>('.uc-odo__col').forEach((c) => { c.style.transform = `translateY(-${Number(c.dataset.digit) * 1.1}em)`; });
      io.unobserve(el);
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
  [...leaves, ...bars, ...odos].forEach((el) => io.observe(el));
}

initHeader();
initMenu();
initSlider();
initLeadForm();
initCookie();
initGoals();
tagElements();
initMotion();
