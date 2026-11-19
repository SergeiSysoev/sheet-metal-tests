#!/usr/bin/env python3
"""Vector redraws for SMY1W3 Monday Review Test (= Trade Intro Final), code Y1W3.

Reference: clean blank /Users/assistant/.telegram-archive/local_66/inbox/
msg_997_Monday_Review_Test_Print_ready__3__SMY1W4__1_.pdf, pages 3 (No.12-14), 9 (No.51, 52), 11 (No.60).
Model coordinates = pixels of crops of that PDF rendered at scale 3 (y down), so the redraw keeps the
printed proportions (the printed figures are not to scale; e.g. the 8'R arc of No.60 is wider than tall).

    python3 tools/figures_y1w3.py            # write every figure into img/
    python3 tools/figures_y1w3.py y1w3-q60   # only this one

Standard library only; helpers and style from tools/figures.py.
"""
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from figures import Fig, OUT, INK, f2, pol, vsub  # noqa: E402


def _path(f, cmds):
    """Object-line path from model-space commands: ('M', p) ('L', p) ('A', r, sweep, p) in model units."""
    d = []
    for c in cmds:
        if c[0] in ("M", "L"):
            x, y = f.P(c[1])
            d.append(f"{c[0]}{f2(x)},{f2(y)}")
        else:
            _, r, sweep, p = c
            x, y = f.P(p)
            R = r * f.k
            d.append(f"A{f2(R)},{f2(R)} 0 0 {sweep} {f2(x)},{f2(y)}")
    f._path(" ".join(d), f.lw)


def _dot(f, p, r=2.6):
    x, y = f.P(p)
    f.el.append(f'<circle cx="{f2(x)}" cy="{f2(y)}" r="{f2(r * f.u)}" fill="{INK}"/>')


# --------------------------------------------------------------------- No.12-14 components
def y1w3_q12():
    """Drive cleat in section: flat strip, both edges folded back 180 deg, gap in the middle of the top."""
    f = Fig((0, 0, 585, 95), 600)
    r, cy = 26.0, 47.5
    _path(f, [("M", (201, cy - r)), ("L", (48, cy - r)), ("A", r, 0, (48, cy + r)),
              ("L", (536, cy + r)), ("A", r, 0, (536, cy - r)), ("L", (394, cy - r))])
    return f


def y1w3_q13():
    """Male Pittsburgh: sheet with a single 90 deg flange at the edge."""
    f = Fig((0, 0, 585, 195), 600)
    f.poly([(50, 173), (543, 173), (543, 19)])
    return f


def y1w3_q14():
    """Female Pittsburgh: offset (jog), then the edge folded into a pocket (two 180 deg folds)."""
    f = Fig((0, 0, 585, 97), 600)
    r1, r2 = 16.5, 11.75
    _path(f, [("M", (16, 76)), ("L", (180, 76)), ("L", (276, 19.5)), ("L", (450, 19.5)),
              ("A", r1, 1, (450, 52.5)), ("L", (285, 52.5)), ("A", r2, 0, (285, 76)), ("L", (530, 76))])
    return f


# --------------------------------------------------------------------- No.51 flat oval
def y1w3_q51():
    """Flat oval: R6" ends, 1'-4" between the ends of the flat sides."""
    f = Fig((0, 0, 470, 310), 600)
    yt, yb = 17.0, 204.5
    xl, xr = 107.5, 357.5
    cy, R = (yt + yb) / 2, (yb - yt) / 2
    f.line((xl, yt), (xr, yt))
    f.line((xl, yb), (xr, yb))
    f.line((xl, yt), (xl, yb))
    f.line((xr, yt), (xr, yb))
    f.arc((xl, cy), R, 90, 270)
    f.arc((xr, cy), R, -90, 90)
    tip = pol((xl, cy), R, 221)
    f.leader([tip, (78, 85.5), (xl - 3, 85.5)])
    f.text((xl + 6, 85.5), 'R6"', anchor="start")
    f.dim((xl, yb), (xr, yb), (xl, 279.5), (xr, 279.5), "1'-4\"", gap=10)
    return f


# --------------------------------------------------------------------- No.52 trapezoid
def y1w3_q52():
    """Trapezoid: top 48" set in 12" from the left end of the 52" bottom, height 35"."""
    f = Fig((0, 0, 686, 515), 600)
    BL, BR, TL, TR = (41.5, 420.5), (478.5, 420.5), (142.0, 116.5), (547.5, 116.5)
    f.poly([BL, TL, TR, BR], closed=True)
    yd = 45.5
    f.dim(BL, TL, (BL[0], yd), (TL[0], yd), '12"', gap=6)
    f.dim(TL, TR, (TL[0], yd), (TR[0], yd), '48"', ext=(False, True), gap=8)
    f.dim(TR, BR, (622.5, TR[1]), (622.5, BR[1]), '35"', gap=8)
    f.dim(BL, BR, (BL[0], 480.5), (BR[0], 480.5), '52"', gap=8)
    return f


# --------------------------------------------------------------------- No.60 perimeter
def y1w3_q60():
    """Plate outline: 12', 18', 8' rise at 30 deg, 8'R and 5'R quarter arcs, 8' step (as printed)."""
    f = Fig((20, 10, 995, 705), 640)
    c8, c5 = (140.5, 207.0), (642.0, 147.5)
    A0, A1 = (140.5, 371.5), (342.0, 207.0)            # 8'R arc ends (printed wider than tall)
    B0, B1 = (642.0, 35.0), (771.0, 147.5)             # 5'R arc ends
    S0, S1 = (891.5, 451.0), (557.0, 620.5)            # 30 deg slope
    # outline
    f.poly([S1, (140.5, 620.5), A0])
    f.ellipse_arc(c8, A1[0] - c8[0], A0[1] - c8[1], 90, 0)
    f.poly([A1, (342.0, 35.0), B0])
    f.ellipse_arc(c5, B1[0] - c5[0], c5[1] - B0[1], -90, 0)
    f.poly([B1, (771.0, 330.0), (891.5, 330.0), S0, S1])
    # radius construction lines and centres
    f.line(c8, (c8[0], A0[1] - 4), thin=True)
    f.line(c8, (A1[0] - 4, c8[1]), thin=True)
    f.line((c5[0], B0[1] + 4), c5, thin=True)
    f.line(c5, (B1[0] - 4, c5[1]), thin=True)
    _dot(f, c8, 3.2)
    _dot(f, c5, 2.2)
    # 8'R: radius line broken by the label, arrow on the arc
    rx8, ry8 = A1[0] - c8[0], A0[1] - c8[1]
    t8 = (c8[0] + rx8 * math.cos(math.radians(45)), c8[1] + ry8 * math.sin(math.radians(45)))
    f.line(c8, (186, 241), thin=True)
    f.leader([t8, (247, 298)])
    f.text((216, 271), "8'R")
    # 5'R
    rx5, ry5 = B1[0] - c5[0], c5[1] - B0[1]
    t5 = (c5[0] + rx5 * math.cos(math.radians(45)), c5[1] - ry5 * math.sin(math.radians(45)))
    f.leader([t5, c5])
    f.text((726, 116), "5'R")
    # dimensions
    f.dim((342.0, 35.0), (342.0, 207.0), (279.0, 35.0), (279.0, 207.0), "8'", ext=(True, False), gap=12)
    f.dim(A0, (140.5, 620.5), (76.5, A0[1]), (76.5, 620.5), "12'", gap=10)
    f.dim((140.5, 620.5), S1, (140.5, 678.5), (S1[0], 678.5), "18'", gap=10)
    f.dim(S0, (S1[0] + 30, 620.5), (937.5, S0[1]), (937.5, 620.5), "8'", gap=12)
    f.line((S1[0] + 30, 620.5), (937.5, 620.5), thin=True)
    a_slope = math.degrees(math.atan2(S0[1] - S1[1], S0[0] - S1[0]))
    f.angle(S1, 222, a_slope, 0, "30°", tpos=pol(S1, 222, a_slope / 2 - 1))
    return f


FIGS = {
    "y1w3-q12": y1w3_q12,
    "y1w3-q13": y1w3_q13,
    "y1w3-q14": y1w3_q14,
    "y1w3-q51": y1w3_q51,
    "y1w3-q52": y1w3_q52,
    "y1w3-q60": y1w3_q60,
}


def main(names):
    OUT.mkdir(parents=True, exist_ok=True)
    for name in names or FIGS:
        fig = FIGS[name]()
        (OUT / f"{name}.svg").write_text(fig.svg(), encoding="utf-8")
        print(f"{name}.svg  viewBox {f2(fig.W)} x {f2(fig.H)}")


if __name__ == "__main__":
    main(sys.argv[1:])
