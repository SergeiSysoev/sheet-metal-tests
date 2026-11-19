# Brief: add one whole test to the Sheet Metal Apprentice Test Trainer

Public bilingual (EN/RU) practice app at /Users/assistant/sheet-metal-tests/ (live: https://sergeisysoev.github.io/sheet-metal-tests/).
Apprentices practice here for written tests that **reuse the same questions in new combinations**, so the English text
must be exactly what is printed. You own one test end to end: transcribe → key → translate/explain → figures → self-check.
Do not edit files other than the ones named for your test. Do not run git.

## 1. Transcribe (English, word for word)
- Question text, any printed instruction (e.g. "Round to 2 decimals" → `hint`), and every option, exactly as printed,
  including the original typos (note them in `flag`, never fix them in the text). Ignore handwriting, circles, check marks.
- Phone photos can be blurry or rotated: zoom/crop/rotate (PIL) and read carefully; compare with any other copy of the
  same question in the bank. If a word or number cannot be read with certainty, say so in `flag` and do not guess silently.
- Number the items with the printed question numbers (`n`).

## 2. Key — how far to trust each source (owner's rule)
- **Error-free key:** only TotalTrack computer printouts that mark the correct answer ("Correct Answer").
- **Everything else is evidence, not truth:** photos of paper sheets (the owner's or another student's), even with the
  instructor's marks or a score, can be wrong. A graded sheet tells you which items lost points; pencil picks on an
  ungraded sheet are only a student's guess.
- Decide every answer yourself and prove it: calculation (python, exact π/sin/cos), the course knowledge base
  /Users/assistant/shared-lib/duct-layout/knowledge/ (README.md is the router; 08-testy-i-klyuchi.md has known keys,
  disputes, traps and solved examples П1–П18; reference_union_course_test_keys.md in
  /Users/assistant/.claude/projects/-Users-assistant/memory/), course sheets in /Users/assistant/shared-lib/duct-layout/sources/,
  standards (AWS, OSHA, SMACNA) or manufacturer documentation.
- When the proven answer differs from the sheet/instructor mark, keep the proven one and explain both in `why`
  ("The course key marks X; technically Y, because …"), following 08-testy-i-klyuchi.md §2. When the only basis is a
  student's pick and you cannot prove it, keep the most defensible answer and end the explanation with
  "Note: not confirmed by a graded key." / «Внимание: проверенного ключа нет.»

## 3. Files you write (CODE = your test code given in the task, e.g. "W3M")
`data/CODE_base.json` — list, one object per question, in printed order:
```
{"src": "CODE", "n": 12, "q": "<English, verbatim>", "hint": null | "<printed instruction>",
 "opts": ["<verbatim>", ...] | null, "answer": [0-based correct indices] | null,
 "kind": null | "input" | "text", "input_answer": "22.21", "input_unit": "$",      // kind "input": numeric typed answer
 "accept": ["lighter"], "answer_text": "Lighter",                                 // kind "text": typed word answer
 "fig": null | "q12", "evidence": "<where the answer comes from: TotalTrack key / graded sheet / calculation / course sheet …>"}
```
Multiple correct options → several indices (the app then asks to pick that many). Open questions that expect a list
or a long answer: turn into `kind: "text"` only if one or two key words decide it; otherwise skip the item and list it in
your report.

`data/CODE_content_main.json` — same order, one object per question:
```
{"src": "CODE", "n": 12, "topic": "<id>", "ru_q": "...", "ru_hint": null | "...", "ru_opts": [...] | null,
 "why_en": "...", "why_ru": "...", "flag": null | "note for the editor"}
```
Topic ids: welding, weldsym, safety, materials, math, trig, drawing, transitions, offsets, fittings, tools, trade
(see tools/CONTENT-BRIEF.md for what each covers, and for the Russian/explanation writing rules — follow them exactly).

## 4. Duplicates
Before writing, load every existing `data/*_base.json`. Skip a question if the bank already has the same question text
with the same set of options (letters may be shuffled) **and** the same drawing; list skipped ones in the report.
Keep as a separate question anything that differs in a number, a word (SMAW vs GMAW), an option, or the drawing.

## 5. Figures
Every question that has a drawing gets our own vector redraw — never a photo. Write a generator
`tools/figures_CODE.py` (standard Python only) that imports helpers from `tools/figures.py` (read it first and keep the
exact style: viewBox only, white background, #111 lines, Arial, dimension arrows, labels ≥ 14 units at 600 wide,
proportions as printed — not redrawn to scale, no answers/student marks, stacked fractions on one line with the same
value). Output `img/<code-lowercase>-qNN.svg` (e.g. `img/w3m-q07.svg` with `"fig": "q07"`; NN = two digits).
If the drawing is identical to one already in img/, you may call the existing function, but any difference (a label,
a number, a letter) needs its own variant. Render each SVG and compare it side by side with the original crop; fix
mismatches.

## 6. Self-check before finishing
Run `python3 tools/build_questions.py --skip-missing-figs --skip-no-content` and make sure it reports no PROBLEMS for
your CODE. Every number in your explanations must come from python. Final message: count of questions written, items
skipped (duplicates / unreadable / open-ended) with reasons, every answer that differs from the sheet's marks with the
evidence, and every non-null flag.
