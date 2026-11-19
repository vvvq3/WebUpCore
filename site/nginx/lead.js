// Заявка с формы сайта → сообщение в Telegram (nginx njs, POST /api/lead, JSON).
// Токен бота и получатели — только в переменных окружения контейнера:
//   TG_BOT_TOKEN — токен бота от @BotFather;
//   TG_CHAT_ID   — id чата получателя (несколько — через запятую).
// Без них обработчик отвечает 503, а письмо через FormSubmit уходит как обычно.

function json(r, code, obj) {
    r.headersOut['Content-Type'] = 'application/json; charset=utf-8';
    r.headersOut['Cache-Control'] = 'no-store';
    r.return(code, JSON.stringify(obj));
}

function clip(v, n) {
    return String(v === undefined || v === null ? '' : v).replace(/\s+/g, ' ').trim().slice(0, n);
}

function esc(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

async function handle(r) {
    if (r.method !== 'POST') {
        json(r, 405, { ok: false, error: 'method' });
        return;
    }
    const token = process.env.TG_BOT_TOKEN || '';
    const chats = (process.env.TG_CHAT_ID || '').split(',').map(function (s) { return s.trim(); }).filter(Boolean);
    if (!token || !chats.length) {
        json(r, 503, { ok: false, error: 'not configured' });
        return;
    }
    let d;
    try {
        d = JSON.parse(r.requestText || '');
    } catch (e) {
        json(r, 400, { ok: false, error: 'bad json' });
        return;
    }
    if (d.website) {            // ловушка для ботов: тихо «принимаем»
        json(r, 200, { ok: true });
        return;
    }
    const f = {
        topic: clip(d.topic, 80),
        name: clip(d.name, 120),
        company: clip(d.company, 160),
        team: clip(d.team, 40),
        contact: clip(d.contact, 160),
        page: clip(d.page, 300),
        lang: clip(d.lang, 5),
    };
    if (!f.name || !f.contact) {
        json(r, 400, { ok: false, error: 'required' });
        return;
    }
    const lines = [
        '<b>Заявка с сайта UpCore' + (f.topic ? ' — ' + esc(f.topic) : '') + '</b>',
        '',
        'Имя: ' + esc(f.name),
        'Компания: ' + esc(f.company || '—'),
        'Размер команды: ' + esc(f.team || '—'),
        'Контакт: ' + esc(f.contact),
        'Страница: ' + esc(f.page || '—') + (f.lang ? ' (' + esc(f.lang.toUpperCase()) + ')' : ''),
    ];
    const api = (process.env.TG_API || 'https://api.telegram.org').replace(/\/+$/, '');
    let sent = 0;
    for (let i = 0; i < chats.length; i++) {
        try {
            const res = await ngx.fetch(api + '/bot' + token + '/sendMessage', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ chat_id: chats[i], text: lines.join('\n'), parse_mode: 'HTML', disable_web_page_preview: true }),
            });
            if (res.ok) {
                sent++;
            } else {
                ngx.log(ngx.ERR, 'lead: telegram ' + res.status + ' for chat ' + chats[i]);
            }
        } catch (e) {
            ngx.log(ngx.ERR, 'lead: telegram fetch failed: ' + e);
        }
    }
    if (sent) {
        json(r, 200, { ok: true });
    } else {
        json(r, 502, { ok: false, error: 'telegram' });
    }
}

export default { handle };
