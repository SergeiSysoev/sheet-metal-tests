"""Raw extraction of tests that have a text layer (Local 66 chat archive PDFs).
Output: data/raw_<code>.json — number, English question, options, the student's pick ('<- Selected'),
page. The student's pick is NOT the key: keys come from knowledge/08-testy-i-klyuchi.md."""
import json, re, pathlib, sys
import pypdfium2 as pdfium
INBOX = pathlib.Path('/Users/assistant/.telegram-archive/local_66/inbox')
OUT = pathlib.Path(__file__).resolve().parent.parent / 'data'
TESTS = {
    'MON79': 'msg_993_Monday_Written_SMY2W2_Answers.pdf',
    'FRI53': 'msg_994_5-A_SMY2W2_Friday_Written-Welding_Intro_Answers.pdf',
    'SMY1W3': 'msg_997_Monday_Review_Test_Print_ready__3__SMY1W4__1_.pdf',
}
QRE = re.compile(r'^(\d{1,2})\.\s+(.*)')
ORE = re.compile(r'^([a-l])\.\s*(.*)')

def parse(path):
    d = pdfium.PdfDocument(str(path))
    items, cur, last = [], None, None
    for pi in range(len(d)):
        text = d[pi].get_textpage().get_text_range()
        for raw in text.splitlines():
            line = raw.strip()
            if not line:
                continue
            m = QRE.match(line); o = ORE.match(line)
            if m and (cur is None or int(m.group(1)) == cur['n'] + 1):
                cur = {'n': int(m.group(1)), 'q': m.group(2), 'opts': [], 'selected': [], 'page': pi + 1}
                items.append(cur); last = 'q'
            elif o and cur is not None and ord(o.group(1)) - 97 == len(cur['opts']):
                txt = o.group(2); sel = '<- Selected' in txt
                txt = txt.replace('<- Selected', '').strip()
                if sel: cur['selected'].append(len(cur['opts']))
                cur['opts'].append(txt); last = 'o'
            elif cur is not None and pi == 0 and cur is None:
                pass
            elif cur is not None:
                if last == 'q':
                    cur['q'] += ' ' + line
                elif last == 'o':
                    sel = '<- Selected' in line
                    t = line.replace('<- Selected', '').strip()
                    if sel: cur['selected'].append(len(cur['opts']) - 1)
                    cur['opts'][-1] += ' ' + t
    return items

for code, f in TESTS.items():
    items = parse(INBOX / f)
    (OUT / f'raw_{code}.json').write_text(json.dumps(items, ensure_ascii=False, indent=1))
    nums = [i['n'] for i in items]
    gaps = sorted(set(range(1, max(nums) + 1)) - set(nums))
    noopt = [i['n'] for i in items if not i['opts']]
    print(code, len(items), 'items; gaps', gaps, '; no options', noopt)
