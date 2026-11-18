<?php
// Обработчик формы заявки для хостинга с PHP (в РФ): положить рядом с сайтом, например /api/lead.php,
// и при сборке указать PUBLIC_FORM_ENDPOINT=/api/lead.php. Заявка уходит письмом на office@dex-it.ru
// и (если заданы переменные окружения TG_BOT_TOKEN и TG_CHAT_ID) сообщением в Telegram.
//   TG_BOT_TOKEN — токен бота от @BotFather; TG_CHAT_ID — ваш chat id (бот должен получить от вас /start).
// Для надёжной доставки почты лучше SMTP хостинга; здесь минимальный вариант на mail().
header('Content-Type: application/json; charset=utf-8');
if ($_SERVER['REQUEST_METHOD'] !== 'POST' || !empty($_POST['website'])) { http_response_code(400); echo '{"ok":false}'; exit; }
$f = fn($k) => trim(mb_substr(strip_tags($_POST[$k] ?? ''), 0, 2000));
if ($f('name') === '' || $f('contact') === '') { http_response_code(422); echo '{"ok":false}'; exit; }
$topics = ['demo' => 'Провести демо', 'report' => 'Получить пример отчёта', 'audit' => 'Заказать аудит', 'pilot' => 'Заказать бесплатный пилот'];
$topic = $topics[$f('topic')] ?? 'Заявка';
$body = "Тема: $topic\nИмя: {$f('name')}\nКомпания: {$f('company')}\nРазмер команды: {$f('team')}\nКонтакт: {$f('contact')}\n"
      . "Страница: {$f('page')} ({$f('lang')})\n";
$ok = mail('office@dex-it.ru', '=?UTF-8?B?' . base64_encode("UpCore — $topic") . '?=', $body,
  "From: UpCore <no-reply@up-core.ru>\r\nContent-Type: text/plain; charset=utf-8");
$token = getenv('TG_BOT_TOKEN'); $chat = getenv('TG_CHAT_ID');
if ($token && $chat) {
  $ctx = stream_context_create(['http' => ['method' => 'POST', 'header' => "Content-Type: application/x-www-form-urlencoded\r\n", 'timeout' => 10,
    'content' => http_build_query(['chat_id' => $chat, 'text' => "Заявка UpCore — $topic\n\n$body"])]]);
  $tg = @file_get_contents("https://api.telegram.org/bot$token/sendMessage", false, $ctx);
  $ok = $ok || ($tg !== false && strpos($tg, '"ok":true') !== false);
}
http_response_code($ok ? 200 : 500);
echo json_encode(['ok' => $ok]);
