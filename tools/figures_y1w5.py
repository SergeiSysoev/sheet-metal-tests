#!/usr/bin/env python3
"""SVG redraws for the SMY1W5 tests (codes Y1W5F = Friday Written Ortho & Ogee, Y1W5M = Monday Written/Math).

Sources (reference only, never shipped): the owner's graded sheets, phone photos
  Y1W5F  /Users/assistant/.telegram-archive/local_66/inbox/msg_2607 ... msg_2621 (page 15 ... page 1)
  Y1W5M  /Users/assistant/.telegram-archive/local_66/inbox/msg_2572 ... msg_2582 (page 11 ... page 1)

Only the questions not already in the bank get a figure here. Every other drawing on these sheets belongs to a
question that is a duplicate of MON / T90 / Y1W3 and is drawn in tools/figures.py.

  Y1W5M No.64  box 11" x 5" x 8" — the same printed picture as Y1W5M No.63 = MON No.34 = T90 No.76
               (photo msg_2573, page 10), so the existing t90_q76 drawing is reused unchanged.

    python3 tools/figures_y1w5.py              # write every figure into img/
    python3 tools/figures_y1w5.py y1w5m-q64    # only this one

Standard library only.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from figures import OUT, f2, t90_q76  # noqa: E402


FIGS = {
    "y1w5m-q64": t90_q76,   # same drawing as T90 No.76 / MON No.34 (11" x 5" x 8" box)
}


def main(names):
    OUT.mkdir(parents=True, exist_ok=True)
    for name in names or FIGS:
        fig = FIGS[name]()
        (OUT / f"{name}.svg").write_text(fig.svg(), encoding="utf-8")
        print(f"{name}.svg  viewBox {f2(fig.W)} x {f2(fig.H)}")


if __name__ == "__main__":
    main(sys.argv[1:])
