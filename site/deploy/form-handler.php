<?php
// Пример обработчика формы заявки для хостинга с PHP (положить рядом с сайтом, например /api/lead.php,
// и указать PUBLIC_FORM_ENDPOINT=/api/lead.php в site/.env). Письмо уходит на office@dex-it.ru.
// Для надёжной доставки лучше SMTP хостинга или почтовый сервис; это минимальный вариант на mail().
header('Content-Type: application/json; charset=utf-8');
if ($_SERVER['REQUEST_METHOD'] !== 'POST' || !empty($_POST['website'])) { http_response_code(400); echo '{"ok":false}'; exit; }
$f = fn($k) => trim(mb_substr(strip_tags($_POST[$k] ?? ''), 0, 2000));
if ($f('name') === '' || $f('contact') === '') { http_response_code(422); echo '{"ok":false}'; exit; }
$topics = ['demo' => 'Провести демо', 'report' => 'Получить демо-отчёт', 'audit' => 'Заказать аудит'];
$topic = $topics[$f('topic')] ?? 'Заявка';
$body = "Тема: $topic\nИмя: {$f('name')}\nКомпания: {$f('company')}\nРазмер команды: {$f('team')}\nКонтакт: {$f('contact')}\n"
      . "Комментарий: {$f('comment')}\nСтраница: {$f('page')} ({$f('lang')})\n";
$ok = mail('office@dex-it.ru', '=?UTF-8?B?' . base64_encode("UpCore — $topic") . '?=', $body,
  "From: UpCore <no-reply@up-core.ru>\r\nContent-Type: text/plain; charset=utf-8");
http_response_code($ok ? 200 : 500);
echo json_encode(['ok' => $ok]);
