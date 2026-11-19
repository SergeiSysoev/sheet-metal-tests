"""Part 1 source extraction: test-90 (Welding & Layout, 16.11.2026) + SMY2W2 Triangulation (18).
Reads the reconstructions in /Users/assistant/shared-lib/duct-layout/prior-work/ and the final key
(t90_key.txt, updated 17.11 after the graded sheets). Writes data/part1_base.json."""
import json, re, pathlib
PW = pathlib.Path('/Users/assistant/shared-lib/duct-layout/prior-work')
OUT = pathlib.Path(__file__).resolve().parent.parent / 'data' / 'part1_base.json'

def load_Q(path):
    s = (PW / path).read_text()
    i = s.find('Q = ')
    m = re.compile(r'^[\]\}]\s*$', re.M).search(s, i)
    ns = {'__file__': str(PW / path)}
    exec(s[:m.end()], ns)
    extra = PW / pathlib.Path(path).parent / 'patch_extra.py'
    if extra.exists():
        e = extra.read_text(); k = e.find('Q.update(')
        exec(e[k:e.find('\n})\n', k) + 4], ns)
    return ns['Q']

key = {}
for line in (PW / 't90/t90_key.txt').read_text().splitlines():
    m = re.match(r'- (\d+)\. .*→ \*\*(.+)\*\*', line)
    if m:
        key[int(m.group(1))] = m.group(2)

items = []
Q90 = load_Q('t90/build.py')
for n in sorted(Q90):
    text, img, opts, correct, note, kind = Q90[n]
    letters = re.findall(r'(?:^|\+\s*|,\s*)([a-h])\)', key.get(n, ''))
    ans = [ord(c) - 97 for c in letters] if letters else correct
    items.append(dict(src='T90', n=n, q=text, opts=opts, answer=ans, key_text=key.get(n), note_ru=note, kind=kind,
                      fig=f'q{n}' if n in (25,27,40,50,51,54,55,56,57,75,76,88,89,90) else None,
                      build_answer=correct))
QT = load_Q('smy2w2/build.py')
for k, (text, img, hint, opts, ci, sol) in enumerate(QT, 1):
    items.append(dict(src='TRI', n=k, q=text, hint=hint, opts=opts, answer=[ci], note_ru=sol, fig=img and img[:-4]))
t = (PW / 'smy2w2/build.py').read_text()
ns = {}
exec(t[t.find('Q18 = ('):t.find('\nQ18_SOL')], ns)
items.append(dict(src='TRI', n=18, q=ns['Q18'], hint=None, opts=None, answer=None, kind='input',
                  input_answer='22.21', input_unit='$', note_ru='Открытый ответ в TotalTrack. Официальный ответ $22.21; $23.73 — если не вычесть углы.', fig=None))
OUT.write_text(json.dumps(items, ensure_ascii=False, indent=1))
print(len(items), 'items')
diff = [(i['n'], i['answer'], i['build_answer']) for i in items if i['src']=='T90' and i['answer'] != i['build_answer']]
print('key vs build differences:', diff)
print('no key parsed:', [i['n'] for i in items if i['src']=='T90' and not i['key_text']])
