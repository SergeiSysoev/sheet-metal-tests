"""Build questions.js from data/*_base.json + data/*_content_*.json.
Checks: English text untouched, answers in range, RU options aligned, topics valid, figure files present.
Run: python3 tools/build_questions.py"""
import json, pathlib, sys

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
}
SOURCES = {
    'T90': {'name': {'en': 'Welding & Layout test', 'ru': 'Тест Welding & Layout'},
            'sub': {'en': 'Monday written test, graded key', 'ru': 'Письменный тест понедельника, проверенный ключ'},
            'short': {'en': 'Welding & Layout', 'ru': 'Welding & Layout'}},
    'FRI': {'name': {'en': 'SMY2W2 Friday Written — Math / Welding', 'ru': 'SMY2W2 Friday Written — математика / сварка'},
            'sub': {'en': "Last year's Friday test: only the questions not already in Welding & Layout", 'ru': 'Пятничный тест прошлого года: только вопросы, которых нет в Welding & Layout'},
            'short': {'en': 'Friday Written', 'ru': 'Friday Written'}},
    'TRI': {'name': {'en': 'SMY2W2 Triangulation quiz', 'ru': 'SMY2W2 Triangulation'},
            'sub': {'en': 'TotalTrack homework quiz, official key', 'ru': 'Домашний квиз TotalTrack, официальный ключ'},
            'short': {'en': 'Triangulation', 'ru': 'Triangulation'}},
}
HINT_RU = {
    'Round to 2 Decimals': 'Округлить до 2 знаков после запятой',
    'Convert to a 3 place decimal': 'Перевести в десятичную дробь с 3 знаками',
    'Round to 2 decimal places': 'Округлить до 2 знаков после запятой',
}
UI = {
    'app_title': {'en': 'Sheet Metal Apprentice Test Trainer', 'ru': 'Тренажёр к тестам sheet metal apprentice'},
    'wordmark': {'en': 'SM Test Trainer', 'ru': 'Тренажёр SM'},
    'home_title': {'en': 'Sheet Metal Apprentice Test Trainer', 'ru': 'Тренажёр к тестам sheet metal apprentice'},
    'home_p1': {'en': '{N} questions from the written tests of the sheet metal apprenticeship. Questions and answer options are word for word as on the tests; every answer comes with an explanation; drawings are redrawn.',
                'ru': '{N} вопросов из письменных тестов sheet metal apprenticeship. Вопросы и варианты — слово в слово как на тестах, у каждого ответа есть пояснение, чертежи перерисованы. В русском режиме под переводом показан английский оригинал — так на тесте вопрос узнаётся сразу.'},
    'home_note': {'en': 'Study material, not an official answer key. Answers follow the course key; where a key answer is debatable, the explanation says so. More tests are being added.',
                  'ru': 'Это учебный материал, а не официальный ключ. Ответы — по ключу курса; где ответ ключа спорный, это сказано в пояснении. Новые тесты добавляются.'},
    'mode_mixed': {'en': 'Practice set — {N} questions', 'ru': 'Тренировка — {N} вопросов'},
    'mode_mixed_sub': {'en': 'Random mix of all topics, no repeats until a topic is used up', 'ru': 'Вперемешку из всех тем, без повторов, пока тема не пройдена'},
    'mode_all': {'en': 'All questions', 'ru': 'Все вопросы'},
    'mode_all_sub': {'en': 'The whole bank in random order', 'ru': 'Вся база в случайном порядке'},
    'mode_mistakes': {'en': 'My mistakes', 'ru': 'Мои ошибки'},
    'mode_mistakes_sub': {'en': 'A question leaves this list once you answer it right', 'ru': 'Вопрос уходит из списка, когда ответишь на него верно'},
    'mode_mistakes_empty': {'en': 'Wrong answers collect here', 'ru': 'Сюда собираются вопросы, где ты ошибся'},
    'by_topic': {'en': 'By topic', 'ru': 'По темам'},
    'by_test': {'en': 'By test, in original order', 'ru': 'По тестам, в исходном порядке'},
    'footer': {'en': 'Free, no ads, no sign-up.', 'ru': 'Бесплатно, без рекламы и регистрации.'},
    'more_tools': {'en': 'More tools →', 'ru': 'Другие инструменты →'},
    'original': {'en': 'Original', 'ru': 'Оригинал'},
    'figure_alt': {'en': 'Drawing for the question', 'ru': 'Чертёж к вопросу'},
    'choose_prompt': {'en': 'Choose one answer', 'ru': 'Выбери один ответ'},
    'multi_prompt': {'en': 'Choose {N} answers, then press Check', 'ru': 'Выбери {N} ответа и нажми «Проверить»'},
    'multi_prompt_many': {'en': 'Choose {N} answers, then press Check', 'ru': 'Выбери {N} ответов и нажми «Проверить»'},
    'type_prompt': {'en': 'Type your answer, then press Check', 'ru': 'Впиши ответ и нажми «Проверить»'},
    'check': {'en': 'Check', 'ru': 'Проверить'},
    'next': {'en': 'Next question', 'ru': 'Следующий вопрос'},
    'finish': {'en': 'See results', 'ru': 'Итог'},
    'to_home': {'en': 'Home', 'ru': 'На главную'},
    'correct': {'en': 'Correct', 'ru': 'Верно'},
    'incorrect': {'en': 'Not quite', 'ru': 'Неверно'},
    'answer_is': {'en': 'answer:', 'ru': 'ответ:'},
    'theme': {'en': 'Light / dark theme', 'ru': 'Светлая / тёмная тема'},
    'end_head': {'en': '{S} of {T} — {P}%', 'ru': '{S} из {T} — {P}%'},
    'end_line_missed': {'en': '{N} to review. They are saved in “My mistakes”.', 'ru': 'Ошибок: {N}. Они сохранены в «Мои ошибки».'},
    'end_line_perfect': {'en': 'No mistakes. Nice work.', 'ru': 'Без ошибок.'},
    'review_missed': {'en': 'Redo the {N} missed', 'ru': 'Перерешать ошибки ({N})'},
    'again': {'en': 'New set', 'ru': 'Новый набор'},
}


def fig_file(src, fig):
    if not fig:
        return None
    return f"{src.lower()}-{fig}.svg"


def main():
    out, problems, held = [], [], []
    for base_path in sorted(D.glob('*_base.json')):
        part = base_path.name[:-len('_base.json')]
        base = json.loads(base_path.read_text())
        content = {}
        for cp in sorted(D.glob(f'{part}_content_*.json')):
            for c in json.loads(cp.read_text()):
                content[(c['src'], c['n'])] = c
        for b in base:
            k = (b['src'], b['n'])
            c = content.get(k)
            if not c:
                problems.append(f'{k}: no content'); continue
            qid = f"{b['src']}-{b['n']}"
            if c['topic'] not in TOPICS:
                problems.append(f'{qid}: bad topic {c["topic"]}')
            item = {'id': qid, 'src': b['src'], 'n': b['n'], 'topic': c['topic'],
                    'q': {'en': b['q'], 'ru': c['ru_q']},
                    'why': {'en': c['why_en'], 'ru': c['why_ru']}}
            if b.get('hint'):
                item['hint'] = {'en': b['hint'], 'ru': HINT_RU[b['hint']]}
            if b.get('kind') == 'input':
                v = float(b['input_answer'])
                item.update(type='input', answer={'value': v, 'tol': 0.005, 'prefix': b.get('input_unit', ''), 'text': b['input_answer']})
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
            f = fig_file(b['src'], b.get('fig'))
            if f:
                if not (ROOT / 'img' / f).exists():
                    if '--skip-missing-figs' in sys.argv:
                        held.append(qid); continue
                    problems.append(f'{qid}: figure {f} missing')
                item['fig'] = f
            out.append(item)
    if held:
        print('HELD BACK until the drawing exists:', ', '.join(held))
    if problems:
        print('PROBLEMS:'); print('\n'.join(problems))
        if '--force' not in sys.argv:
            sys.exit(1)
    js = ('// Generated by tools/build_questions.py — do not edit by hand.\n'
          f'const TOPICS = {json.dumps(TOPICS, ensure_ascii=False, indent=1)};\n'
          f'const SOURCES = {json.dumps(SOURCES, ensure_ascii=False, indent=1)};\n'
          f'const UI = {json.dumps(UI, ensure_ascii=False, indent=1)};\n'
          f'const QUESTIONS = {json.dumps(out, ensure_ascii=False, indent=1)};\n')
    (ROOT / 'questions.js').write_text(js)
    from collections import Counter
    print(len(out), 'questions;', dict(Counter(i['topic'] for i in out)))


if __name__ == '__main__':
    main()
