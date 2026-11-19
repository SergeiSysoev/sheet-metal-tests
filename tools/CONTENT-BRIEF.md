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
`tools` (shears, brakes, machines, hand tools), `trade` (conduct, customer policy, union, jobsite rules).

## Writing rules
- **Russian (`ru_q`, `ru_opts`, `why_ru`)**: plain natural Russian. Trade and technical terms stay in English, never
  translated: duct, fitting, transition, offset, elbow, throat, heel, cheek, gauge, shear, brake, S&D, drive, slip,
  Pittsburgh, SMAW, GMAW, MIG, stick, DCEN, DCEP, electrode, flux, fillet, groove, bevel, reference line, arrow side,
  FOB, FOT, TOP, take off, spin-in, end cap, layout, true length, OSHA, SDS, etc. Units and numbers exactly as in
  English. Options in Russian must not hint at the answer more than the English ones do (same length/style).
- **Explanations** (`why_en`, `why_ru`, same content): 1–4 short sentences. First the reason the correct answer is
  correct; for calculations the formula and numbers; then, if useful, why the tempting wrong option is wrong
  (trap: in² vs in³, ft-in vs decimal ft, the other acute angle, truncation instead of rounding…).
  No filler, no "Great question", no references to "the key says" except for disputed items.
- For multi-answer items explain each correct choice. For `kind: "input"` items write the solution steps.
- Keep the English question untouched even if it has typos; if there is a typo, mention it in `flag`, not in the text.
