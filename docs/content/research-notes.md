# Исследование для текстов сайта UpCore (11.11.2026)

Сырые выписки: формулировки конкурентов, исследований и статей. Цитаты на языке оригинала, рядом — что берём для UpCore.
Итоговая отобранная и оценённая таблица — `docs/content/theses.csv` / `theses.md`.

## 1. Конкуренты — главные страницы

### BlueOptima (blueoptima.com) — ближайший по смыслу (Coding Effort, подрядчики, AI-детект)
- Hero: «Your Code. Consistent Evidence. Your Decisions.» / «AI Moves Fast. Gain Certainty. See Where to Act.»
- «Get objective evidence of performance — productivity, cost and quality — across your AI-assisted and human-written code»
- «Is AI-assisted code improving engineering performance, or just increasing activity?»
- «Measure effort, not just time spent» · «Analyse every change» · «Compare across teams and technologies» · «Put performance in context»
- Боли-вопросы: «How do we compare, and where can we improve?» «How is faster output impacting code quality?» «Is our engineering spend paying off?» «Is AI-assisted code increasing exposure?»
- Цифры: 970 000+ разработчиков, 14,8 млрд ревизий, 70+ языков, 20+ лет; кейс DSK Bank: +18% продуктивности, +40% выше рынка, 1,6 млн BGN (~$960k) высвобождено; «$25m saved»; «Zero secrets leaked, down from 20 per month».
- Безопасность: «without your source code leaving your environment», cloud / on-prem / hybrid, SSO, SOC 2 Type 2, Zero Trust.
- Use-cases: Benchmark delivery performance · Limit technical debt · Improve AI ROI · Manage code security.

### LinearB
- Hero: «Drive productivity with engineering context»; «board-ready AI ROI report on demand».
- Боль: CTO Emburse — совет директоров «is specifically asking questions about our use of AI and what our ROI is».
- APEX-вопросы: «Is AI helping us ship more?» «Do we deliver what we commit to?» «Are the gains sustainable for developers?»
- Kraken: 70–80% задержек ревью — часовые пояса, силосы, доступность ревьюеров; размер/сложность — 5–10%.
- Цены: $29 / $59 за контрибьютора в месяц. Gartner MQ Leader 2026. SOC 1/2, ISO 27001.
- «Cost per effective PR» — метрика стоимости результата.

### Jellyfish
- Hero: «Engineering Intelligence for Your AI-Native SDLC» / «See how your people and agents really build software».
- «More code isn't the same as more value» — сильный тезис, близкий к UpCore (результирующий код).
- «Metrics built for human-only teams can't tell you which changes are helping.»
- «AI can double the code moving through your pipeline. It also creates new bottlenecks in review and CI, new costs in tokens and seats, and new questions from finance and the board.»
- «Rolling out AI tooling without measurement is just hope.» (цитата клиента) · «operating blind isn't an option»
- «Find out which teams are compounding with AI and which are spinning their wheels.» · «Catch burnout before it costs you.»
- Три вопроса к ИИ-инвестициям: «Where do I stand? Am I transforming? What is it worth?»
- Цифры: бенчмарк 1000+ инженерных организаций, 100M+ PR, 9,4% PR открыты агентами (октябрь); клиенты: Siigo +30% производительности, Loadsmart ~80% кода от ИИ, −30% цикл.
- DevFinOps: «Align with Finance and automate financial reporting» (капитализация R&D).

### DX (getdx.com)
- Hero: «Delivery intelligence for the AI era»; «engineering intelligence platform designed by researchers».
- «Track AI-generated code by commit, PR, team, agent, and repo to understand AI's real impact on productivity.»
- «See how developers work and where they get stuck» · «Measure output, find bottlenecks, and align engineering with business goals.»

### Swarmia
- Hero: «The gap between good and great software is growing» / «Good teams use AI to make individual engineers faster. Great teams… get that speed all the way to production.»
- Боль: команды используют одни и те же ИИ-инструменты, но получают «wildly different results».
- «Swarmia acts as a mirror for the teams.» (клиент) — близко к «саморегуляции» UpCore.
- «Insights that find you» / «Strong defaults» / «Capitalize software development costs».

### GitClear — исследование качества ИИ-кода
- Hero: «See which AI tools are actually earning their license.»
- «Find the folders where AI is creating more work than it saves.» · «See human vs. LLM code, measured by the same yardstick.»
- «Every line tagged with the model that wrote it.» · «Moves, renames, and reformatting don't inflate a model's numbers.»
- Цифры: 211 млн строк в 3 исследованиях; **в 8 раз больше дублирующихся блоков** с приходом ИИ-ассистентов; **в 9 раз выше churn у «ИИ-power users»**, при этом кода в 4–10 раз больше.
- «One comprehensive scorecard. Ten minutes to get started. No sales call required.»

### Waydev
- «Understand the impact and ROI of AI across your organization»; «DORA, SPACE, and DX on autopilot».
- «Ask your engineering data anything. Nothing leaves your network.» — приватный ИИ.
- Боли из отзывов: ручные отчёты, burndown не даёт глубины, баги считают по закрытым тикетам.
- Gartner: доля компаний с DPI-платформами вырастет до 50% к 2027.

### CodeScene — техдолг и здоровье кода
- Hero: «Accelerate with AI, without losing control».
- «The average enterprise codebase scores 5.15 out of 10 on Code Health. AI needs 9.5 to work reliably.»
- «AI agents introduce at least 60% more defects and burn up to 50% more tokens in unhealthy code.»
- «AI error rates increase by 2–5x in problematic code» · «Cuts human code review time in half»
- «Manage technical debt where it impacts delivery» · «Prioritize and quantify technical debt»

### Faros AI
- Hero: «Ship more work per AI dollar» / «Stop token maxxing. Start outcome maxxing.» / «Don't scale your AI bill. Scale your outcomes.»
- Боли: «Exploding token bills», «Model prices vary by 10x, but nobody knows which is best», «Same tools, different results: AI budgets get devoured without uniform outcomes across teams.»

### Weave (weaveos.com)
- «Weave builds models to measure engineering work.» · «Turn AI adoption into engineering output.» · «Get more output from every AI dollar.»
- Вопросы: «Which engineers are using AI most effectively?» «Analyze the strengths and weaknesses of our teams».
- Клиент: «We use Weave to get an objective measurement and keep ourselves honest». Reducto: +19% выработки, 14 дней от установки до первого отчёта руководству.

### Span (span.app)
- «Your SDLC needs production-grade observability» / «You know the second a service degrades. Span tells you when your delivery does.»
- «Track AI code from prompt to prod» · запись сессий агента на машине разработчика (через MDM), «not a proxy», редактирование секретов и ПДн до сохранения, zero-retention LLM. (Аналог промпт-коллектора UpCore.)

### Exceeds AI
- Hero: «Your engineers adopted AI. Now, prove it's working.» · «AI writes code fast. Is it writing it well?» · «Know exactly who's using AI, and who's not.» · «Every prompt, every PR, every dollar».
- «Performance reviews went from dreaded to data-driven.» (отзыв) — сильная формулировка для Grade.
- «Live in 15 minutes», «extracts insights without storing code»; бенчмарк 356K+ инженеров; «Engineers who write 2+ spec lines before coding merge 2.1x more AI-assisted tokens» (качество постановки → Mentor).

### BlueOptima — кейсы подрядчиков
- «$7M in Vendor Credits – How Objective Metrics Exposed 250 Inactive Developers» (заголовок кейса).
- Фин. компания: проект на 76% менее продуктивен ожидаемого; ключевые разработчики вендора на 75% ниже среднего по компании; код на 38% хуже сопровождаем; «the outsourced developers were delivering a minimum effort», «appeared to be working on other projects», «high risk of knowledge loss».
- Кейс in-house vs outsourcing: сокращение in-house на 40% без потери продуктивности, $2 млн/год экономии.

## 2. Российские конкуренты
### KODA (ITFB Group, itfbgroup.ru/koda)
- «ДАННЫЕ. ПРОЗРАЧНОСТЬ. ЭФФЕКТИВНОСТЬ.»; «Как измерить неосязаемое?»; «Как найти неэффективных разработчиков и повысить их отдачу?»
- Боли: «До 30% времени тратится на непродуктивные задачи», «Неэффективные TL-оценки на основе устных отчётов», «Риски overemployment», «руководитель видит разработку как „черный ящик“», «невозможность получить объективные ответы».
- Обещания: «сократит время разработки до 40%», «Система не „ищет виноватых“», развёртывание в контуре, «без необходимости передачи данных во вне».
### DevGhost (devghost.ru)
- Hero: «Вы платите за разработку. Поймите, какую отдачу получаете от каждого разработчика» — очень сильный, ровно наша ЦА.
- «второе мнение о команде», «Когда нужно независимое второе мнение»; «Кто выше и ниже эталона», «Где стоит разобраться».
- Эталон: middle на полной ставке, знакомый с проектом, без AI. Без слежки (время, экран, клавиатура не отслеживаются).
- Боли: сроки постоянно переносятся, объяснения меняются; подрядчик занят, а результат неясен; непонятно, выросла ли отдача после AI; самые заметные ≠ самые результативные; Jira и Slack показывают активность, а не объём работы в коде.
- Бесплатный пилот, SaaS 0 ₽ + кредиты, Local-режим без внешних вызовов.
### CodeScoring.TQI
- Боли: «более 60% проектов забрасываются из-за смены команды и плохого качества реализации»; при большом copy-paste «разработка превращается в поддержку»; при цикломатической сложности >50 вероятность ошибки стремится к 1; код-ревью «не всегда может показать общую картину качества».
### Tech Talent Score
- «Раскройте весь потенциал ваших разработчиков и команд разработки»; 60+ метрик, 5000+ разработчиков ежедневно, реестр отечественного ПО №19596, on-premise.
- «Средний экономический эффект ~500 000 ₽ в год на разработчика»; «инженеры-призраки» со ссылкой на Стэнфорд.
### PanDev Metrics (Казахстан) — IDE-плагины, «Give PanDev two weeks… If you do not get value in those two weeks, we have not done our job.»

## 3. Исследования (цифры для тезисов)
- **Стэнфорд, «инженеры-призраки»** (Денисов-Бланш, 2024, 50 000+ инженеров): ~9,5% инженеров «практически ничего не делают» (выработка ≤ 0,1 медианы); удалённо 14%, в офисе 6%. Метод — анализ приватных Git-репозиториев + модель, имитирующая экспертную оценку коммитов.
- **Стэнфорд, ИИ и продуктивность** (~100–120 тыс. разработчиков, 600+ компаний): метод — панель из 10–15 сеньоров оценивала изменения кода (сложность, время, качество), ML-модель обучена на их оценках, корреляция r = 0,82–0,86. **Это ровно подход UpCore** → аргумент в пользу «96% от экспертной оценки».
  - медианный прирост от ИИ 10–15% (вендоры обещают 60%); брутто +30–40%, нетто после переделок +15–20%; ~половину прироста съедают переделки;
  - greenfield простые +30–40%, brownfield сложные 0–10% и может быть минус; нижний квартиль команд — 0% или минус;
  - разрыв между самооценкой и измерением ~30 п.п.; лишь треть разработчиков верно оценивает свой квартиль; опросы «почти как подбрасывание монетки»;
  - первые 30–100 часов с ИИ разработчики часто медленнее; «rich get richer» — разрыв между командами растёт.
- **METR (июль 2025, RCT)**: 16 опытных разработчиков, 246 задач в зрелых репозиториях — с ИИ на **19% дольше**, при этом сами считали, что ускорились на 20% (разрыв 39 п.п.).
- **DORA 2025** (≈5000 специалистов): ИИ используют 90%; ИИ теперь коррелирует с ростом пропускной способности, но **по-прежнему увеличивает нестабильность поставки**; ~30% мало или совсем не доверяют ИИ-коду; ИИ — «усилитель»: умножает сильные и слабые стороны организации.
- **Stack Overflow 2025**: ИИ используют 84%, **46% не доверяют точности** (было 31%); доверяют 29–33%; главная фрустрация — «решения, которые почти правильные, но не совсем» (66%); 45% — отладка ИИ-кода дольше, чем ждали.
- **GitClear**: дублирующихся блоков кода ×8 с приходом ИИ; churn у активных ИИ-пользователей ×9.
- **CodeScene**: средний enterprise-код 5,15/10 Code Health; ИИ-агенты вносят ≥60% больше дефектов в нездоровом коде.
- **Faros AI, «AI Productivity Paradox» (июнь 2025, 10 000+ разработчиков, 1255 команд)**: при высокой доле ИИ команды закрывают на 21% больше задач и мёржат на 98% больше PR, но **время ревью +91%**, PR на 154% крупнее; позже — багов на разработчика +9%. Вывод: «ИИ повышает выработку разработчика, но не продуктивность компании; узкое место — человеческое ревью».
- **Uplevel (2024, ~800 разработчиков)**: с Copilot — нет значимого роста cycle time / throughput, **+41% багов**; переработки снизились меньше, чем у группы без Copilot.
- **Harness, State of Engineering Excellence 2026 (700 респондентов)**: 89% лидеров говорят о росте продуктивности с ИИ, но **81% — сэкономленное на написании кода время теперь уходит на ревью ИИ-кода**; главные сложности: измерить реальный эффект (26%), удержать качество (24%), доказать ROI руководству (18%).
- **LeadDev AI Impact Report 2025**: эффект ИИ-инструментов измеряют **лишь 18% организаций**.
- **Россия, ИИ-код**: Сбер — доля принятого ИИ-кода 45% → 69% за 2025 г., ~80% из 14 000 разработчиков ежедневно в GigaCode, «на 60% больше коммитов» (внутренний замер); Яндекс — 70–73% регулярно используют ИИ, «на 10–20% больше коммитов», цель «75/75/75» к концу 2026; Т-Банк — доля регулярных пользователей ИИ 17% → 85% за 10 мес. Все меряют охват и коммиты, а не ценность → ниша UpCore AI.
- **Накрутка опыта (Хабр Карьера + «Киберпротект» + HR-клуб АПКИТ, ноябрь 2025)**: 99% работодателей знают о накрутке, 64% сталкиваются регулярно (35% — несколько раз в неделю); приписывают достижения (81%), стаж (77%), несуществующие компании (68%), полностью вымышленные резюме (48%); чаще всего — backend/frontend-разработчики (35%); по грейдам — мидлы 43%, джуны 37%. Нейросети на интервью — 27%, «подсказчики» в реальном времени — 24%. **На испытательном сроке выявляют лишь 2%.** Рынку не хватает «механизма подтверждения реального опыта» (26%) — запрос на «цифровой паспорт опыта». «Кризис доверия между соискателем и работодателем».
- **Работа.ру (Коммерсант)**: 39% рекрутеров видели тестовые, сделанные ИИ; признаются лишь 3% кандидатов.
- **Performance review**: CEB/Gartner — 95% руководителей недовольны системой оценки, ~210 ч в год на руководителя, ~40 ч на сотрудника, ~$35 млн/год на компанию в 10 000 человек; ~90% HR-лидеров: процесс не даёт точной информации. Scullen, Mount, Goff (2000, J. Applied Psychology; цит. HBR/Deloitte): **более половины (≈60%) разброса оценок объясняется особенностями оценивающего, а не работой оцениваемого** («idiosyncratic rater effect»).
- **Цена ошибки найма**: Минтруд США — ≥30% годовой зарплаты (прямые затраты); SHRM — замена сотрудника 50–200% годового дохода.
- **McKinsey + Оксфорд (5400+ крупных ИТ-проектов)**: в среднем **+45% к бюджету, +7% к срокам и на 56% меньше ценности**, чем планировали. По 6000+ проектам (2001–2017): бюджет +75%, сроки +46%, ценность −39%.
- **Stripe Developer Coefficient (2018)**: 17,3 ч в неделю (≈42% времени) разработчик тратит на техдолг и плохой код; ~$85 млрд упущенной выгоды в год.
- **Контроль подрядчиков (Хабр, клерк, arisweb)**: признак накрутки — часы растут, а функциональность не меняется; задача неделями «почти готова»; при оплате за активность (часы, тикеты) у подрядчика нет стимула работать быстрее; заказчик «не знает, как выявлять», что 20 ч по ТЗ — это 15.
- **DX AI Measurement Framework**: 3 измерения — Utilization / Impact / Cost; «most engineering leaders can't answer basic questions about their AI investments»; реальный прирост 5–15%, а не 50–100%; acceptance rate — плохая метрика (принятый код часто правят/удаляют до коммита); «You cannot retroactively recreate perceptual measurements once AI changes workflows» → **у UpCore базовая линия строится ретроспективно по истории Git** (сильное отличие); нужно 3–6 мес. для надёжных выводов (у UpCore — сразу по истории).
- **Jellyfish AI Impact**: «Lead AI Transformation with Clarity», «fund what works, cut waste, and invest with evidence», «vendor-neutral»; боль: руководители опираются на «vendor-reported activity metrics», нужно обосновать бюджет на ИИ перед финансами.
- **Anthropic (янв. 2026, RCT, 52 разработчика)**: с ИИ — 50% в тесте на понимание против 67% без ИИ (−17 п.п.), сильнее всего просела отладка; кто спрашивал ИИ «почему» — ≥65%, кто делегировал генерацию кода — <40%. → тезис для Mentor: ИИ ускоряет, но может тормозить рост; учим работать с ИИ правильно.
- **Онбординг**: Swimm — 3–9 мес. до полной продуктивности; Cortex 2024 — 72% разработчиков >1 мес. до первых 3 значимых PR; Google — удалённый онбординг +3–6 недель.
- **LinkedIn Workplace Learning 2018**: 94% сотрудников остались бы дольше, если компания вкладывается в их развитие; 2025 — лишь 15% говорят, что руководитель помог составить план развития за полгода.
- **Kent Beck & Gergely Orosz vs McKinsey (2023)**: мерить импакт, а не усилия; индивидуальные метрики «геймятся» (закон Гудхарта). → Возражение, которое снимаем: UpCore меряет результат, сохранившийся в продукте, с отсевом шума и весом архитектуры; не активность.
- **Хабр, performance review**: калибровка нужна, т. к. «оценки всегда содержат субъективность»; кейс Авито — инженер сэкономил ~600 тыс. ₽/мес, но получил «ниже ожиданий» за неучастие в активностях; риск «любимчиков».
- **Хабр/Tproger, вайбкодинг**: ассистент за 38 минут создал 47 файлов и ~1900 строк — ревью никто не отменял; основная нагрузка проверки ИИ-кода ложится на сеньоров (Fastly); ИИ-правки «логичны локально», но ломают целостность системы.
- **ИИ-ревьюеры**: CodeRabbit — «The future isn't writing code. It's reviewing it.» «AI-driven code now outpaces human capacity.» «Fast code. Faster chaos.» «Raise the quality bar. Lower the review burden.» Qodo — «Code review for agents. Governance for humans.» «Wikis go stale. Linters miss intent.» «~1 час экономии на PR», «Qodo does about 90% of that initial code review».
- **SIG / Sigrid**: «AI coding agents ship code faster than anyone can check it.» «Evidence you can take to the board.» «Not ready for a subscription? Start with a scan.» — формат «разовый скан» = наш разовый аудит; 63% организаций не видят эффекта ИИ на EBIT; бенчмарк 40 000+ систем; ISO 25010.
- **Tech due diligence (M&A)**: стоимость кода и техдолга закладывается в цену сделки; тех-аудит при покупке — $6–30 тыс. → сценарий Projects: «оценка кодовой базы при покупке / инвестиции / приёмке».
- **Зарплаты РФ** (Хабр Карьера): медиана ИТ ~183 тыс. ₽ (2П 2025), 191 тыс. ₽ (1П 2026); разработчики ~220 тыс. ₽; backend — ~228–235 тыс. ₽. → для расчёта потерь в рублях.

## 4. Что берём (сводно)
1. **Деньги и прозрачность** — «вы платите за разработку, но не видите отдачу», «чёрный ящик», «активность ≠ результат» (KODA, DevGhost, Jellyfish «More code isn't the same as more value»).
2. **ИИ-парадокс** — ощущение ускорения vs измерения (METR, Стэнфорд, Faros, Uplevel, GitClear); ревью — новое узкое место; ROI ИИ спрашивает совет директоров (LinearB); лишь 18% меряют.
3. **Кризис доверия в найме** — накрутка опыта (Хабр Карьера 2025), ИИ на собеседованиях; «цифровой паспорт опыта» → Grade/авто-резюме.
4. **Субъективные ревью** — rater effect, калибровки, любимчики, 210 ч на руководителя.
5. **Подрядчики** — «акт на веру», BlueOptima: −75% у вендора, «$7M vendor credits», «250 inactive developers»; McKinsey +45% бюджет.
6. **Обучение** — ИИ тормозит рост навыков (Anthropic), онбординг 3–9 мес., ИПР раз в полгода, 94% остались бы при развитии.
7. **Доверие к методике** — модель на экспертных оценках (как у Стэнфорда, r = 0,82–0,86) → 96% у UpCore; не LOC/коммиты (закон Гудхарта).
8. **Безопасность SaaS** — код не покидает контур (BlueOptima, Waydev «Nothing leaves your network», Span «not a proxy», Exceeds «without storing code»), on-prem, SSO, роли; «первый результат за минуты/дни» (GitClear 10 мин, Exceeds 15 мин, Weave 14 дней); пилот бесплатно / оплата после подтверждения.
