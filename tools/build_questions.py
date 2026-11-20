"""Build questions.js from data/*_base.json + data/*_content_*.json.
Checks: English text untouched, answers in range, RU options aligned, topics valid, figure files present.
Run: python3 tools/build_questions.py"""
import json, pathlib, sys, re, hashlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
D = ROOT / 'data'

TOPICS = {
    'welding':     {'en': 'Welding (SMAW, GMAW)',          'ru': 'Сварка (SMAW, GMAW)'},
    'weldsym':     {'en': 'Welding symbols',               'ru': 'Сварочные символы'},
    'materials':   {'en': 'Metals & gauges',               'ru': 'Металлы и gauge'},
    'math':        {'en': 'Shop math',                     'ru': 'Математика'},
    'trig':        {'en': 'Triangles & angles',            'ru': 'Треугольники и углы'},
    'drawing':     {'en': 'Drawings & views',              'ru': 'Чертёж и виды'},
    'transitions': {'en': 'Transitions',                   'ru': 'Transitions'},
    'offsets':     {'en': 'Offsets & elbows',              'ru': 'Offsets и elbows'},
    'fittings':    {'en': 'Fittings, seams & connections', 'ru': 'Fittings, швы и соединения'},
    'tools':       {'en': 'Tools & machines',              'ru': 'Инструменты и станки'},
    'safety':      {'en': 'Safety',                        'ru': 'Безопасность'},
    'trade':       {'en': 'Trade & conduct',               'ru': 'Профессия и поведение на работе'},
    'dampers':     {'en': 'Fire & smoke dampers',          'ru': 'Fire & smoke dampers'},
}
SOURCES = {
    'F20': {'name': {'en': 'Friday test 11/20 — practice', 'ru': 'Пятничный тест 20.11 — подготовка'},
            'sub': {'en': "This week's tests and the old-test questions the instructor went over on 11/19, in one test",
                    'ru': 'Тесты этой недели и вопросы старых тестов, которые инструктор разбирал 19.11, в одном тесте'},
            'short': {'en': 'Friday 11/20', 'ru': 'Пятница 20.11'}},
    'T90': {'name': {'en': 'Welding & Layout test', 'ru': 'Тест Welding & Layout'},
            'sub': {'en': '2nd year: welding, layout, safety, math', 'ru': '2-й год: сварка, layout, безопасность, математика'},
            'short': {'en': 'Welding & Layout', 'ru': 'Welding & Layout'}},
    'FRI': {'name': {'en': 'SMY2W2 Friday Written — Math / Welding', 'ru': 'SMY2W2 Friday Written — математика / сварка'},
            'sub': {'en': '2nd year, week 2', 'ru': '2-й год, неделя 2'},
            'short': {'en': 'Friday Written', 'ru': 'Friday Written'}},
    'MON': {'name': {'en': 'SMY2W2 Monday Written', 'ru': 'SMY2W2 Monday Written'},
            'sub': {'en': '2nd year, week 2', 'ru': '2-й год, неделя 2'},
            'short': {'en': 'Monday Written', 'ru': 'Monday Written'}},
    'Y1W3': {'name': {'en': 'SMY1W3 Monday Review = Trade Intro Final', 'ru': 'SMY1W3 Monday Review = Trade Intro Final'}, 'sub': {'en': '1st year: trade intro, shop standards, math', 'ru': '1-й год: введение в профессию, shop standards, математика'}, 'short': {'en': 'SMY1W3 Monday', 'ru': 'SMY1W3 Monday'}},
    'BRZ': {'name': {'en': 'SMY1W3 Friday — Brazing & Soldering', 'ru': 'SMY1W3 Friday — brazing и soldering'}, 'sub': {'en': '1st year, week 3', 'ru': '1-й год, неделя 3'}, 'short': {'en': 'Brazing', 'ru': 'Brazing'}},
    'FSD': {'name': {'en': 'Fire & Smoke Damper Technician (FSD units 1–6)', 'ru': 'Fire & Smoke Damper Technician (FSD, части 1–6)'}, 'sub': {'en': 'Inspection and testing of dampers', 'ru': 'Осмотр и проверка dampers'}, 'short': {'en': 'FSD', 'ru': 'FSD'}},
    'Y1W5F': {'name': {'en': 'SMY1W5 Friday Written — Ortho & Ogee', 'ru': 'SMY1W5 Friday Written — Ortho & Ogee'}, 'sub': {'en': '1st year, week 5', 'ru': '1-й год, неделя 5'}, 'short': {'en': 'SMY1W5 Friday', 'ru': 'SMY1W5 Friday'}},
    'Y1W5M': {'name': {'en': 'SMY1W5 Monday Written/Math — Ortho & Ogee Offsets', 'ru': 'SMY1W5 Monday Written/Math — Ortho & Ogee Offsets'}, 'sub': {'en': '1st year, week 5', 'ru': '1-й год, неделя 5'}, 'short': {'en': 'SMY1W5 Monday', 'ru': 'SMY1W5 Monday'}},
    'Y2W3M': {'name': {'en': 'SMY2W3 Monday Written Review', 'ru': 'SMY2W3 Monday Written Review'}, 'sub': {'en': '2nd year, week 3', 'ru': '2-й год, неделя 3'}, 'short': {'en': 'SMY2W3 Monday', 'ru': 'SMY2W3 Monday'}},
    'Y2W3F': {'name': {'en': 'SMY2W3 Friday Written', 'ru': 'SMY2W3 Friday Written'}, 'sub': {'en': '2nd year, week 3', 'ru': '2-й год, неделя 3'}, 'short': {'en': 'SMY2W3 Friday', 'ru': 'SMY2W3 Friday'}},
    'Y2W4M': {'name': {'en': 'SMY2W4 Fitting Review — Monday Written', 'ru': 'SMY2W4 Fitting Review — Monday Written'}, 'sub': {'en': '2nd year, week 4', 'ru': '2-й год, неделя 4'}, 'short': {'en': 'SMY2W4 Monday', 'ru': 'SMY2W4 Monday'}},
    'Y2W4F': {'name': {'en': 'SMY2W4 Friday Written/Math', 'ru': 'SMY2W4 Friday Written/Math'}, 'sub': {'en': '2nd year, week 4', 'ru': '2-й год, неделя 4'}, 'short': {'en': 'SMY2W4 Friday', 'ru': 'SMY2W4 Friday'}},
    'Y2W5M': {'name': {'en': 'SMY2W5 Intro to Arch Metals — Monday Written Review', 'ru': 'SMY2W5 Intro to Arch Metals — Monday Written Review'}, 'sub': {'en': '2nd year, week 5', 'ru': '2-й год, неделя 5'}, 'short': {'en': 'SMY2W5 Monday', 'ru': 'SMY2W5 Monday'}},
    'Y2W5Y': {'name': {'en': 'SMY2W5 Year End Cumulative Written Exam', 'ru': 'SMY2W5 Year End Cumulative Written Exam'}, 'sub': {'en': '2nd year, end of year', 'ru': '2-й год, итоговый экзамен года'}, 'short': {'en': 'Year End', 'ru': 'Year End'}},
    'FIN5': {'name': {'en': '005 Final Written Test', 'ru': '005 Final Written Test'}, 'sub': {'en': 'Final written test', 'ru': 'Итоговый письменный тест'}, 'short': {'en': '005 Final', 'ru': '005 Final'}},
    'APR': {'name': {'en': 'Written test, April 2026', 'ru': 'Письменный тест, апрель 2026'}, 'sub': {'en': 'Shop standards, tools, math', 'ru': 'Shop standards, инструменты, математика'}, 'short': {'en': 'April test', 'ru': 'April test'}},
    'CLS': {'name': {'en': 'Review class 11/19: law of cosines and the new-test question', 'ru': 'Разбор 19.11: law of cosines и вопрос с нового теста'},
            'sub': {'en': 'Law of cosines on the formula sheet example (p. 12); the question the instructor read from the new test', 'ru': 'Law of cosines по примеру formula sheet (стр. 12); вопрос, который инструктор зачитал с нового теста'},
            'short': {'en': 'Review 11/19', 'ru': 'Разбор 19.11'}},
    'Y1W5H': {'name': {'en': 'SMY1W5 Orthographics & Ogee Offsets — homework', 'ru': 'SMY1W5 Orthographics & Ogee Offsets — домашнее задание'},
              'sub': {'en': '1st year, week 5: homework', 'ru': '1-й год, неделя 5: домашнее задание'},
              'short': {'en': 'SMY1W5 homework', 'ru': 'SMY1W5 домашнее'}},
    'Y2W1H': {'name': {'en': 'SMY2W1 Welding Intro & Fundamentals — homework', 'ru': 'SMY2W1 Welding Intro & Fundamentals — домашнее задание'},
              'sub': {'en': '2nd year, week 1: homework', 'ru': '2-й год, неделя 1: домашнее задание'},
              'short': {'en': 'SMY2W1 homework', 'ru': 'SMY2W1 домашнее'}},
    'TRI': {'name': {'en': 'SMY2W2 Triangulation quiz', 'ru': 'SMY2W2 Triangulation'},
            'sub': {'en': '2nd year, week 2: homework quiz', 'ru': '2-й год, неделя 2: домашний квиз'},
            'short': {'en': 'Triangulation', 'ru': 'Triangulation'}},
}
# Fine topic ids (used in the data files) roll up into six big topics shown in the app (owner, 2026-11-19:
# "welding symbols belong to welding", fewer, bigger topics).
GROUPS = {
    'welding': {'en': 'Welding & brazing',               'ru': 'Сварка и brazing'},
    'math':    {'en': 'Shop math & trig',                'ru': 'Математика и тригонометрия'},
    'layout':  {'en': 'Drawings, layout & fittings',     'ru': 'Чертежи, layout и fittings'},
    'shop':    {'en': 'Metals, tools & machines',        'ru': 'Металлы, инструменты и станки'},
    'safety':  {'en': 'Safety',                          'ru': 'Безопасность'},
    'dampers': {'en': 'Fire & smoke dampers',            'ru': 'Fire & smoke dampers'},
    'trade':   {'en': 'Trade, union & conduct',          'ru': 'Профессия, профсоюз и поведение'},
}
GROUP_OF = {'welding': 'welding', 'weldsym': 'welding', 'math': 'math', 'trig': 'math',
            'drawing': 'layout', 'transitions': 'layout', 'offsets': 'layout', 'fittings': 'layout',
            'materials': 'shop', 'tools': 'shop', 'safety': 'safety', 'trade': 'trade', 'dampers': 'dampers'}
# Fire & smoke dampers are their own topic (owner, 2026-11-19): the whole FSD course, plus damper questions in any test.
DAMPER_RE = re.compile(r'\bdampers?\b|fusible link|UL ?555|smoke detector', re.I)
SRC_ORDER = ['F20', 'CLS', 'T90', 'FRI', 'MON', 'TRI', 'Y2W3M', 'Y2W3F', 'Y2W4M', 'Y2W4F', 'Y2W5M', 'Y2W5Y', 'Y1W3', 'Y1W5M', 'Y1W5F', 'Y1W5H', 'Y2W1H',
             'APR', 'BRZ', 'FSD', 'FIN5']
SOURCES = {k: SOURCES[k] for k in SRC_ORDER + [k for k in SOURCES if k not in SRC_ORDER]}
# Tests after the first one repeat many questions; the bank keeps each question once, under the first test it
# appeared in. Say so on every later test card, so a small count is not mistaken for a missing test.
for _k, _v in SOURCES.items():
    if _k in ('F20', 'T90', 'FRI', 'MON', 'CLS'):
        continue
    if 'only new' not in _v['sub']['en']:
        _v['sub'] = {'en': _v['sub']['en'] + ' · new questions only',
                     'ru': _v['sub']['ru'] + ' · только новые вопросы'}
HINT_RU = {
    'Round to 2 Decimals': 'Округлить до 2 знаков после запятой',
    'Convert to a 3 place decimal': 'Перевести в десятичную дробь с 3 знаками',
    'Round to 2 decimal places': 'Округлить до 2 знаков после запятой',
}
UI = {
    'app_title': {'en': 'Sheet Metal Apprentice Test Trainer', 'ru': 'Тренажёр к тестам sheet metal apprentice'},
    'wordmark': {'en': 'SM Test Trainer', 'ru': 'Тренажёр SM'},
    'home_title': {'en': 'Sheet Metal Apprentice Test Trainer', 'ru': 'Тренажёр к тестам sheet metal apprentice'},
    'home_p1': {'en': 'Practice for the written tests of the sheet metal apprenticeship: {N} questions with explanations.',
                'ru': 'Подготовка к письменным тестам sheet metal apprenticeship. Вопросов с пояснениями: {N}.'},
    'mode_all': {'en': 'Start the test — all questions', 'ru': 'Начать тест — все вопросы'},
    'mode_all_sub': {'en': 'Random order. Answer as many as you like, then finish and see your result', 'ru': 'Вперемешку. Отвечай сколько хочешь, потом заверши тест и посмотри результат'},
    'finish_test': {'en': 'Finish test and show results', 'ru': 'Завершить тест и показать результат'},
    'continue_test': {'en': 'Continue the test ({N} left)', 'ru': 'Продолжить тест (осталось {N})'},
    'end_answered': {'en': 'Answered {D} of {T} questions.', 'ru': 'Отвечено {D} из {T} вопросов.'},
    'mode_mistakes': {'en': 'My mistakes', 'ru': 'Мои ошибки'},
    'mode_mistakes_sub': {'en': 'A question leaves this list once you answer it right', 'ru': 'Вопрос уходит из списка, когда ответишь на него верно'},
    'mode_mistakes_empty': {'en': 'Wrong answers collect here', 'ru': 'Сюда собираются вопросы, где ты ошибся'},
    'by_topic': {'en': 'By topic', 'ru': 'По темам'},
    'by_test': {'en': 'By test, in original order', 'ru': 'По тестам, в исходном порядке'},
    'footer': {'en': 'Free, no ads, no sign-up.', 'ru': 'Бесплатно, без рекламы и регистрации.'},
    'more_tools': {'en': 'More tools →', 'ru': 'Другие инструменты →'},
    'original': {'en': 'Original', 'ru': 'Оригинал'},
    'tap_to_enlarge': {'en': 'Tap the drawing to open it full size', 'ru': 'Нажми на чертёж, чтобы открыть его крупно'},
    'figure_alt': {'en': 'Drawing for the question', 'ru': 'Чертёж к вопросу'},
    'choose_prompt': {'en': 'Choose one answer', 'ru': 'Выбери один ответ'},
    'multi_prompt': {'en': 'Choose all correct answers, then press Check', 'ru': 'Выбери все верные ответы и нажми «Проверить»'},
    'multi_prompt_many': {'en': 'Choose all correct answers, then press Check', 'ru': 'Выбери все верные ответы и нажми «Проверить»'},
    'type_prompt': {'en': 'Type your answer, then press Check', 'ru': 'Впиши ответ и нажми «Проверить»'},
    'check': {'en': 'Check', 'ru': 'Проверить'},
    'next': {'en': 'Next question', 'ru': 'Следующий вопрос'},
    'finish': {'en': 'See results', 'ru': 'Итог'},
    'to_home': {'en': 'Home', 'ru': 'На главную'},
    'correct': {'en': 'Correct', 'ru': 'Верно'},
    'incorrect': {'en': 'Not quite', 'ru': 'Неверно'},
    'answer_is': {'en': 'answer:', 'ru': 'ответ:'},
    'you_chose': {'en': 'you chose', 'ru': 'твой выбор:'},
    'theme': {'en': 'Light / dark theme', 'ru': 'Светлая / тёмная тема'},
    'end_head': {'en': '{S} of {D} right — {P}%', 'ru': 'Верно {S} из {D} — {P}%'},
    'end_line_missed': {'en': 'Mistakes: {N}. They are saved in “My mistakes”.', 'ru': 'Ошибок: {N}. Они сохранены в «Мои ошибки».'},
    'end_line_perfect': {'en': 'No mistakes. Nice work.', 'ru': 'Без ошибок.'},
    'review_missed': {'en': 'Redo the {N} missed', 'ru': 'Перерешать ошибки ({N})'},
    'again': {'en': 'Start over', 'ru': 'Начать заново'},
    'run_all': {'en': 'All questions', 'ru': 'Все вопросы'},
    'resume_run': {'en': 'Continue: {NAME}', 'ru': 'Продолжить: {NAME}'},
    'resume_sub': {'en': 'Question {N} of {T} · {P}% right so far', 'ru': 'Вопрос {N} из {T} · пока верно {P}%'},
    'resume_sub0': {'en': 'Question {N} of {T}', 'ru': 'Вопрос {N} из {T}'},
}


def ru_plural(n, one, few, many):
    if n % 10 == 1 and n % 100 != 11: return one
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14: return few
    return many


def fig_file(src, fig):
    if not fig:
        return None
    return f"{src.lower()}-{fig}.svg"


def main():
    out, problems, held = [], [], []
    for base_path in sorted(D.glob('*_base.json'), key=lambda p: (not p.name.startswith('part'), p.name)):
        part = base_path.name[:-len('_base.json')]
        excl = [a.split('=', 1)[1].split(',') for a in sys.argv if a.startswith('--exclude=')]
        if excl and part in excl[0]:
            continue
        base = json.loads(base_path.read_text())
        content = {}
        for cp in sorted(D.glob(f'{part}_content_*.json')):
            for c in json.loads(cp.read_text()):
                content[(c['src'], c['n'])] = c
        for b in base:
            k = (b['src'], b['n'])
            c = content.get(k)
            if not c:
                if '--skip-no-content' in sys.argv:
                    held.append(f'{b["src"]}-{b["n"]}'); continue
                problems.append(f'{k}: no content'); continue
            qid = f"{b['src']}-{b['n']}"
            if b['src'] not in SOURCES:
                problems.append(f'{qid}: source {b["src"]} not in SOURCES')
            if c['topic'] not in TOPICS:
                problems.append(f'{qid}: bad topic {c["topic"]}')
            grp = GROUP_OF.get(c['topic'], c['topic'])
            if b['src'] == 'FSD' or DAMPER_RE.search(b['q'] + ' ' + ' '.join(b.get('opts') or [])):
                grp = 'dampers'
            item = {'id': qid, 'src': b['src'], 'n': b['n'], 'topic': grp,
                    'q': {'en': b['q'], 'ru': c['ru_q']},
                    'why': {'en': c['why_en'], 'ru': c['why_ru']}}
            if b.get('hint'):
                ru_h = c.get('ru_hint') or HINT_RU.get(b['hint'])
                if not ru_h:
                    problems.append(f'{qid}: hint without Russian')
                item['hint'] = {'en': b['hint'], 'ru': ru_h or b['hint']}
            if b.get('kind') == 'text':
                item.update(type='input', answer={'accept': b.get('accept') or [], 'all': b.get('all') or [], 'reject': b.get('reject', []), 'text': b['answer_text'], 'prefix': ''})
            elif b.get('kind') == 'input':
                v = float(b['input_answer'])
                item.update(type='input', answer={'value': v, 'tol': b.get('tol', 0.005), 'prefix': b.get('input_unit') or '',
                                                  'text': b.get('answer_text') or b['input_answer']})
            else:
                opts, ru = b['opts'], c['ru_opts']
                if not ru or len(ru) != len(opts):
                    problems.append(f'{qid}: ru_opts misaligned')
                    continue
                ans = b['answer']
                if not ans or any(not (0 <= a < len(opts)) for a in ans):
                    problems.append(f'{qid}: answer out of range')
                item['opts'] = [{'en': e, 'ru': r} for e, r in zip(opts, ru)]
                item['answer'] = ans
                item['type'] = 'multi' if len(ans) > 1 else 'single'
                if b.get('also'):
                    item['also'] = b['also']        # also accepted (proven on graded sheets), single-choice only
            f = fig_file(b['src'], b.get('fig'))
            if f:
                if not (ROOT / 'img' / f).exists():
                    if '--skip-missing-figs' in sys.argv:
                        held.append(qid); continue
                    problems.append(f'{qid}: figure {f} missing')
                item['fig'] = f
            out.append(item)
    # Options are shuffled in the app on every showing. Keep the printed order only where an option names other
    # options by letter ("a and c", "both b and d"). Explanations must name options by their text, never by letter.
    OPT_REF = re.compile(r'\b(both|either) [a-d]\b|\b[a-d] (and|&|or) [a-d]\b|\b[a-d], [a-d]\b')
    EXPL_REF = re.compile(r'\b(pick|option|answer|key|вариант|балла —) [a-h]\b', re.I)
    for it in out:
        if it.get('opts') and len(it['opts']) > 2:
            if any(OPT_REF.search(o['en']) for o in it['opts']):
                it['keep'] = 1
            elif EXPL_REF.search(it['why']['en']) or EXPL_REF.search(it['why']['ru']):
                problems.append(f"{it['id']}: explanation names an option by letter (options are shuffled)")
    # cross-test dedup (tests reuse questions with shuffled letters): keep the first occurrence
    norm = lambda t: re.sub(r'[^a-z0-9]+', ' ', t.lower()).strip()
    seen, kept, dups = {}, [], []
    for it in out:
        figsig = hashlib.md5((ROOT / 'img' / it['fig']).read_bytes()).hexdigest() if it.get('fig') else ''
        opts = tuple(sorted(norm(o['en']) for o in it.get('opts', [])))
        sig = (norm(it['q']['en']), opts, figsig, json.dumps(it.get('hint'), sort_keys=True))
        if sig in seen:
            dups.append(f"{it['id']}={seen[sig]}"); continue
        seen[sig] = it['id']; kept.append(it)
    out = kept
    if dups:
        print('Duplicates dropped:', ', '.join(dups))
    # Full exams (data/exam_CODE.json): every printed question of one test, in printed order, pointing at the bank
    # question that is word for word the same (it may live under another test). The app's "By test" view then
    # shows the whole exam with its own numbers.
    resolve = dict(d.split('=') for d in dups)
    by_id = {it['id']: it for it in out}
    for ep in ([] if '--no-exams' in sys.argv else sorted(D.glob('exam_*.json'))):
        ex = json.loads(ep.read_text())
        code = ex['code']
        if code not in SOURCES:
            problems.append(f'{ep.name}: unknown code {code}'); continue
        for e in ex['items']:
            qid = resolve.get(e['id'], e['id'])
            it = by_id.get(qid)
            if not it:
                problems.append(f'{ep.name}: №{e["n"]} -> {e["id"]} not in bank'); continue
            it.setdefault('on', []).append([code, e['n']])
        SOURCES[code]['full'] = len(ex['items'])
        SOURCES[code]['sub'] = {'en': SOURCES[code]['sub']['en'].split(' · new questions only')[0] + f" · full test, {len(ex['items'])} questions",
                                'ru': SOURCES[code]['sub']['ru'].split(' · только новые')[0] + f" · полный тест, {len(ex['items'])} {ru_plural(len(ex['items']), 'вопрос', 'вопроса', 'вопросов')}"}
    if held:
        print('HELD BACK until the drawing exists:', ', '.join(held))
    if problems:
        print('PROBLEMS:'); print('\n'.join(problems))
        if '--force' not in sys.argv:
            sys.exit(1)
    js = ('// Generated by tools/build_questions.py — do not edit by hand.\n'
          f'const TOPICS = {json.dumps(GROUPS, ensure_ascii=False, indent=1)};\n'
          f'const SOURCES = {json.dumps(SOURCES, ensure_ascii=False, indent=1)};\n'
          f'const UI = {json.dumps(UI, ensure_ascii=False, indent=1)};\n'
          f'const QUESTIONS = {json.dumps(out, ensure_ascii=False, indent=1)};\n')
    (ROOT / 'questions.js').write_text(js)
    from collections import Counter
    print(len(out), 'questions;', dict(Counter(i['topic'] for i in out)))


if __name__ == '__main__':
    main()
