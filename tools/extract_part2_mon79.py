"""Part 2: SMY2W2 Monday Written (last year's sheet, 79). English text from the PDF text layer
(data/raw_MON79.json via tools/extract_pdf_tests.py); answers from knowledge/08-testy-i-klyuchi.md §6.
Exact duplicates of part 1 (same question and same options) are dropped; variants are kept."""
import json, re, pathlib
D = pathlib.Path(__file__).resolve().parent.parent / 'data'
K = ("1 a,2 c,3 a,4 abd,5 a,6 a,7 d,8 a,9 b,10 d,11 b,12 b,13 d,14 c,15 c,16 ac,17 b,18 d,19 a,20 c,21 b,22 c,"
     "23 a,24 b,25 a,26 a,27 b,28 a,29 a,30 a,31 d,32 b,33 a,34 a,35 a,36 c,37 b,38 a,39 c,40 a,41 c,42 c,43 d,"
     "44 b,45 c,46 c,47 a,48 d,49 a,50 c,51 a,52 a,53 b,54 a,55 d,56 bf,57 ae,58 bdgl,59 a,60 c,61 c,62 a,63 c,"
     "64 d,65 b,66 b,67 b,68 c,69 a,70 e,71 a,72 d,73 c,74 c,75 a,76 a,78 d,79 a")
KEY = {int(x.split()[0]): [ord(c) - 97 for c in x.split()[1]] for x in K.split(',')}
# questions with a drawing on the sheet (checked on the PDF pages)
FIGS = {24, 33, 34, 40, 42, 43, 44, 45, 49, 54, 56, 57, 58, 70, 76}  # image objects on the PDF pages
# same text as Test-90 №40, but the drawing has the FOB/FOT labels on A and B swapped -> a different question
KEEP_DESPITE_SAME_TEXT = {76}
norm = lambda s: re.sub(r'[^a-z0-9]+', ' ', s.lower()).strip()
have = {}
for p in D.glob('part1*_base.json'):
    for i in json.loads(p.read_text()):
        have[(norm(i['q']), tuple(norm(o) for o in (i['opts'] or [])))] = f"{i['src']}-{i['n']}"
out, dropped = [], []
for r in json.loads((D / 'raw_MON79.json').read_text()):
    n = r['n']
    sig = (norm(r['q']), tuple(norm(o) for o in r['opts']))
    if sig in have and n not in KEEP_DESPITE_SAME_TEXT:
        dropped.append(f"MON-{n} = {have[sig]}"); continue
    item = dict(src='MON', n=n, q=r['q'], opts=r['opts'] or None, answer=KEY.get(n), note_ru=None,
                fig=f'q{n:02d}' if n in FIGS else None, page=r['page'])
    if n == 77:
        item.update(q='Is a number 9 welding lens darker or lighter than a number 12?', opts=None, answer=None,
                    kind='text', accept=['lighter'], answer_text='Lighter')
    out.append(item)
(D / 'part2_base.json').write_text(json.dumps(out, ensure_ascii=False, indent=1))
print(len(out), 'kept; dropped exact duplicates:', ', '.join(dropped))
