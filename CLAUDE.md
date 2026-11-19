# Тренажёр к тестам курса — https://sergeisysoev.github.io/sheet-metal-tests/

Задача Сержа 2026-11-19: тренажёр для подготовки к письменным тестам курса (Local 66 apprenticeship).
Тесты курса повторяют те же вопросы в новых наборах, поэтому **английский текст вопроса и вариантов —
дословно с бланка**, даже с опечатками (опечатку отметить в пояснении). Сайт открытый, для всех,
ссылка с главной https://sergeisysoev.github.io/ (репозиторий /Users/assistant/sergeisysoev.github.io/).

## Правила
- Ответы — по ключу курса: /Users/assistant/shared-lib/duct-layout/knowledge/08-testy-i-klyuchi.md и
  /Users/assistant/.claude/projects/-Users-assistant/memory/reference_union_course_test_keys.md.
  Спорный ключ: «для балла — X; технически Y тоже верен, потому что…». Ответ в данных не менять без доказательства.
- **Насколько верить источнику (Серж 2026-11-19):** без ошибок только распечатки TotalTrack, где компьютер пометил
  верный и неверный ответ («Correct Answer»). Фото бумажных листков (свои и чужие, даже с пометками инструктора) —
  критически: там бывают ошибки. Каждый ответ с такого листка проверять расчётом, листами курса, стандартом;
  неподтверждённый — честно пометить в пояснении.
- Источник новых тестов — группа Telegram «Local 66» (архив /Users/assistant/.telegram-archive/local_66/,
  докачка: python3.14 /Users/assistant/shared-scripts/tg-pull.py --chat -1002847377893 --from <дата>).
- Каждое число в пояснении — посчитано кодом.
- Рисунки — только свои чертежи (SVG из tools/figures.py) с теми же размерами, что на бланке. Фото и сканы не вставлять.
- Русский: простой язык, термины трейда по-английски. В русском режиме под переводом — английский оригинал.
- Один и тот же вопрос с другими числами или с другим словом (SMAW / GMAW) — отдельный вопрос: на тесте это ловушка.
  Точные дубли сливать.

## Что внутри (2026-11-19 вечер): 574 вопроса после удаления дублей
Коды тестов (src) и откуда взяты — архив группы Local 66, /Users/assistant/.telegram-archive/local_66/inbox/:
- T90 Welding & Layout (16.11, фото Сержа, prior-work/t90), FRI SMY2W2 Friday (msg_994), MON SMY2W2 Monday (msg_993),
  TRI SMY2W2 Triangulation (TotalTrack, официальный ключ);
- Y2W3M/F SMY2W3 Monday msg_1244–1270, Friday msg_1295–1306; Y2W4M/F SMY2W4 msg_1869–1885, 1887–1903;
  Y2W5M SMY2W5 Monday Review msg_2721–2730; Y2W5Y Year End Cumulative msg_2739–2752 (лист Тимофея);
- Y1W3 SMY1W3 Monday = Trade Intro (msg_997 + листы msg_980–990, 754–766); Y1W5F/M SMY1W5 Friday msg_2604–2621,
  Monday msg_2572–2582 (листы Сержа, проверены красным); APR апрель 2026 (видимо SMY1W4) msg_2213–2215;
- BRZ brazing (msg_995) и FSD units 1–6 (msg_999…1007) — TotalTrack, официальный ключ; FIN5 «005 Final» msg_3247–3249.
Не вошли: Y2W4M №49, 52 (не читаются чертежи), Y2W3M №3, Y2W3F №35, BRZ №19, Y2W5Y №63 (открытые списки).
Темы в приложении — 7 крупных (сварка, математика, чертежи/layout/fittings, металлы/инструменты, безопасность,
fire & smoke dampers, профессия/профсоюз); в данных — мелкие id, сборка сворачивает (GROUP_OF).
«also» в данных — второй засчитываемый вариант, где проверенный лист и доказательство расходятся (Y1W3-51, Y2W3F-7, Y2W5Y-41).

## Как добавить новый тест
Бриф для исполнителя — tools/TEST-BRIEF.md (+ CONTENT-BRIEF.md): data/CODE_base.json, CODE_content_main.json,
tools/figures_CODE.py, img/code-qNN.svg; код добавить в SOURCES/SRC_ORDER в build_questions.py. Дубли между тестами
сборка убирает сама (текст + набор вариантов + рисунок). После — независимая проверка (отдельный агент, только чтение).

## Данные и сборка
- data/<part>_base.json — английский текст, варианты, ответ по ключу (tools/extract_*.py).
- data/<part>_content_*.json — тема, перевод, пояснения EN/RU (бриф: tools/CONTENT-BRIEF.md).
- python3 tools/build_questions.py → questions.js; поднять ?v=N в index.html.
- Выкладка: git push в main; проверять живую страницу по содержимому, не по коду 200.
