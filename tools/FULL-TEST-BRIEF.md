# Brief: make one real test COMPLETE in the trainer (full exam map + every missing question)

Owner's rule (2026-11-20): the "By test" view must show every real test **whole** — its own name, every printed question in
printed order with the printed numbers — not "only new questions". The "By topic" view is the compilation of all tests
without repeats: whatever a test has that the bank did not, goes into the bank (and so into its topic).

Repo: /Users/assistant/sheet-metal-tests/. Read first: CLAUDE.md, tools/TEST-BRIEF.md (transcription, key, files, figures,
self-check), tools/CONTENT-BRIEF.md (topic ids, Russian and explanation rules — follow exactly). This brief adds the map.

## What you deliver for each test CODE you are given
1. `data/exam_CODE.json` — `{"code": "CODE", "items": [{"n": <printed number>, "id": "<bank id>"}, ...],
   "skipped": [{"n": .., "why": ".."}]}` — one item per printed question, printed order. `id` is `SRC-n` of the bank
   question that is the same question (it may belong to another test). `skipped` only for a number printed with no
   question, a question voided on the test, or a question you truly cannot read after zooming/cropping — say why.
2. Every printed question that is NOT in the bank → add it to `data/CODE_base.json` (+ `data/CODE_content_main.json`,
   + figure in `tools/figures_CODE.py` → `img/code-qNN.svg`) exactly as tools/TEST-BRIEF.md says, `n` = printed number.
   If CODE_base.json already exists, append; never renumber or rewrite existing entries of other tests.
   Open questions: if one or two key words / numbers decide it, use `kind: "text"` (see Y2W5Y-63 in data/Y2W5Y_base.json
   for the format with `accept` / `all` / `reject`) or `kind: "input"`; do not skip them.

## Same question or new?
- **Same** (map to the existing id): same question text and the same set of options (order may differ) and the same
  drawing (same numbers and labels). Differences only in punctuation, hyphens, apostrophes ("it's"/"its"), capitals,
  curly quotes or an obvious typo do NOT make a new question.
- **New**: any difference in a number, a word that changes meaning (SMAW/GMAW, 40'-0"/46'-8"), an option, a label on the
  drawing (FOT/FOB swapped), or the drawing's numbers. On the test these are traps, so they are separate questions.
- Several bank questions can share text + options and differ only by drawing (e.g. "Solve for the missing angle.",
  the plan-and-section transition T90-40 vs MON-76 whose FOB/FOT labels are swapped): open both SVGs in img/ and the
  test photo and pick the one whose drawing matches; if none matches, it is new.
- Search the whole bank (`data/*_base.json`) — the duplicate usually lives under an older test.

## Key
As tools/TEST-BRIEF.md §2. A graded sheet tells which items lost points (red marks / score); unmarked picks on a graded
sheet are confirmed by the grader for that test. If the existing bank key of a mapped question disagrees with the graded
sheet of your test, do NOT edit the other test's files — report it (id, bank answer, sheet answer, your proof).

## Rules
- Do not touch files of other tests, tools/build_questions.py, index.html, questions.js history; do not run git.
- Self-check: `python3 tools/build_questions.py --skip-missing-figs --skip-no-content` (other people work in parallel;
  ignore problems for codes that are not yours, fix every problem of yours). Then check your map: every `id` resolves.
- Every number in an explanation comes from python. No source/provenance words on screen (see CLAUDE.md "Готовый продукт").

## Final message (short, factual)
Per test: printed count; mapped to existing; new added (ids); skipped (n + reason); key conflicts with the bank; any
`flag` you set; anything you could not finish.
