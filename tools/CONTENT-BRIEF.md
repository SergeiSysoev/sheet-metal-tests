# Brief: question content for the Sheet Metal Apprentice Test Trainer

Public bilingual (English / Russian) practice web app. Users: sheet metal apprentices (English speakers) and
the owner, Serge (Russian speaker, studies in English). The real tests reuse these exact questions in new
combinations, so **the English question and options must stay word-for-word as printed on the test.**

## Input
`/Users/assistant/sheet-metal-tests/data/part1_base.json` — list of items:
`src` ("T90" = Test-90 "Welding & Layout", 16.11.2026, graded; "TRI" = SMY2W2 Triangulation TotalTrack quiz, official key),
`n` (question number), `q` (English question), `opts` (English options, index-aligned), `answer` (0-based correct
option indices — FINAL course key, multi-answer questions have several), `note_ru` (earlier Russian note; some are
outdated, see below), `fig` (figure id or null), `kind` ("check" = earlier uncertainty flag; "input" = typed answer).

## Ground truth for answers — read before writing anything
- `/Users/assistant/shared-lib/duct-layout/knowledge/08-testy-i-klyuchi.md` — §4 (Test-90 key and positions),
  §9 (Triangulation), worked examples П1–П18, «Ловушки». This document wins over `note_ru`.
- Disputed items and how to explain them: `/Users/assistant/.claude/projects/-Users-assistant/memory/reference_union_course_test_keys.md`.
  Format for a disputed item: state the course-key answer as the one to pick for points, then one sentence why
  the other option is also technically correct, with the reason (e.g. Test-90 №5 straight polarity: key d; b is
  also correct — DCEN means electrode lead to negative, work lead to positive). №26 bevel: 30° (AWS D1.1 B-U2, 60° groove).
  №40 = B (FOT): TOP is the surface facing the viewer (course sheet 2I Transition Terminology). №67 = No (a shear cuts, it does not bend).
- Supporting course notes: `/Users/assistant/shared-lib/duct-layout/knowledge/07-welding-smaw.md`, `06-shvy-pripuski-gauges-mashiny.md`,
  `04-transitions.md`, `03-offsets-elbows-ogee-laterals.md`, `02-matematika-i-hvac-pro.md`, `12-glossary.md`.
- **Never change `answer`.** If you believe the key is wrong, keep it and put your argument in `flag` (see below).
- Every number in an explanation must be computed with python (exact sin/cos/π, no rounded constants mid-way). Show the
  key steps with numbers.

## Output — one JSON list, one object per input item, same order
```
{ "src": "T90", "n": 12,
  "topic": "<one id from the list below>",
  "ru_q": "...", "ru_opts": ["...", ...],            // index-aligned with opts; null when opts is null
  "why_en": "...", "why_ru": "...",
  "flag": null | "short note for the editor: disagreement with key, unreadable input, typo in the original, etc." }
```
Topic ids (pick exactly one): `welding` (SMAW/GMAW processes, polarity, electrodes, settings), `weldsym` (welding
symbols), `safety` (OSHA, WISHA, SDS, hazards, PPE, ladders, first aid, gas cylinders), `materials` (metals, gauges,
properties), `math` (fractions, decimals, ft-in, area, volume, gallons, percent, money), `trig` (right triangles,
angles, diagonals), `drawing` (views, scales, lines, reading prints), `transitions`, `offsets` (offsets, elbows,
ogee, trim joints, rise/run of duct systems), `fittings` (seams, connections, S&D, takeoffs, end caps, allowances),
`tools` (shears, brakes, machines, hand tools), `dampers` (fire, smoke and combination dampers, FSD inspection and testing), `trade` (conduct, customer policy, union, jobsite rules).

## Writing rules
- **Russian (`ru_q`, `ru_opts`, `why_ru`)**: plain natural Russian. Trade and technical terms stay in English, never
  translated: duct, fitting, transition, offset, elbow, throat, heel, cheek, gauge, shear, brake, S&D, drive, slip,
  Pittsburgh, SMAW, GMAW, MIG, stick, DCEN, DCEP, electrode, flux, fillet, groove, bevel, reference line, arrow side,
  FOB, FOT, TOP, take off, spin-in, end cap, layout, true length, OSHA, SDS, etc. Units and numbers exactly as in
  English. Options in Russian must not hint at the answer more than the English ones do (same length/style).
- **Washington rules (owner, 2026-11-19):** we work in Washington State. Where a WAC rule (L&I: chapters 296-155,
  296-880 fall protection, 296-874 scaffolds, 296-876 ladders, 296-24, 296-800 …) differs from OSHA, the stricter one is
  followed on the job. Whenever an explanation quotes an OSHA number, check the matching WAC on app.leg.wa.gov; if WA is
  stricter, say so in the explanation ("In Washington the stricter WAC … applies: …"). The test answer stays the course
  key; if the key itself conflicts with the stricter WA rule, say that too.
- **Do not give the answer away in Russian.** When a question tests knowing an English term or definition
  ("An angle less than 90° is a(n) ____ angle", "Symptoms that show up suddenly are ____ effects"), leave those
  term options in English with no Russian gloss, and keep the term in English in the question too.
- **Explanations** (`why_en`, `why_ru`, same content) must be exhaustive (owner, 2026-11-19): first why the correct answer is correct
  (fact, standard with section, or the full calculation); then EVERY other option — what it actually is and where it is used in the
  trade, and why it is not the answer here; for calculations, how each wrong option is produced (the trap). Yes/No: the full rule,
  the reason, and what would make the opposite true. Usually 4–9 sentences, no filler. Name options by their text, never by letter
  (the app shuffles options). No provenance notes ("sheet", "key says", other test numbers).
  End with one short paragraph "How to use this:" / «Как применять:» — the general rule or method and how it answers other
  questions of the same kind (owner, 2026-11-19).
- For multi-answer items explain each correct choice. For `kind: "input"` items write the solution steps.
- Keep the English question untouched even if it has typos; if there is a typo, mention it in `flag`, not in the text.
