#!/usr/bin/env python3
"""SVG redraws for SMY2W2 Friday Written 11/20/2026 (code F20), printed numbers 91-128.

Sources (reference only, never shipped): the owner's graded test, phone photos, 28 pages
  No.100  page 23 (a77e0bc1-image.jpg)  offset with two 38 deg elbows, R 1'-6", 16"x20", find D
  No.101  page 24 (4871b768-image.jpg)  plan offset with two 40 deg elbows, R 14", 12"x10", find L
  No.105  page 25 (550ff086-image.jpg)  OWL: four notched 16"x12" duct halves A-D
Every other drawing in No.91-128 belongs to a question already in the bank (No.97 = T90-51, No.99 = T90-57).
Questions 1-90 of the same test are drawn in tools/figures_f20.py.

Geometry is written in the pixel coordinates of the photo crops, so the redraw keeps the printed
proportions (the prints are not to scale: the elbows of No.100 are drawn at about 44 deg though
labelled 38 deg, those of No.101 at about 34 deg though labelled 40 deg — kept as printed).

    python3 tools/figures_f20b.py              # write every figure into img/
    python3 tools/figures_f20b.py f20-q105     # only this one

Standard library only.
"""
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from figures import OUT, Fig, f2, pol, vadd, mid  # noqa: E402

FS = 15   # label size in viewBox units at 600 wide (brief: >= 14)


def f20_q100():
    """Elevation: 16"x20" duct offset up with two 38 deg elbows (throat R 1'-6"), bottoms B= 9'-8-1/2" and
    B= 12'-3", ceiling 9'-0"; dimension D between the elbow ends."""
    f = Fig((0, 0, 1600, 1062), 600)
    f.fs = FS
    th = 44.0                                   # elbow angle as drawn (labelled 38 deg)
    s, c = math.sin(math.radians(th)), math.cos(math.radians(th))
    w, Rt = 177.0, 115.0
    x1, ytop = 557.0, 623.0                     # start of the first elbow, top of the lower duct
    ybot = ytop + w
    xr = 1560.0
    # structure: double wall line on the left turning into the double line above the duct; ceiling below
    f.poly([(40, 1062), (40, 215), (xr, 215)])
    f.poly([(100, 1062), (100, 258), (xr, 258)])
    f.line((100, 850), (xr, 850))
    f.line((100, 870), (xr, 870))
    # lower duct (runs through the wall)
    f.line((35, ytop), (x1, ytop))
    f.line((35, ybot), (x1, ybot))
    f.line((x1, ytop), (x1, ybot))
    # elbow 1: throat is the top wall
    C1 = (x1, ytop - Rt)
    f.arc(C1, Rt, 90, 90 - th)
    f.arc(C1, Rt + w, 90, 90 - th)
    T1, H1 = pol(C1, Rt, 90 - th), pol(C1, Rt + w, 90 - th)
    f.line(T1, H1)
    # straight piece, length chosen so the second elbow ends at x = 1030 as printed
    d = (c, -s)
    S = (1030.0 - x1 - 2 * (Rt + w / 2) * s) / c
    T2, H2 = vadd(T1, d, S), vadd(H1, d, S)
    f.line(T1, T2)
    f.line(H1, H2)
    f.line(T2, H2)
    # elbow 2: throat is the bottom wall
    C2 = vadd(H2, (s, c), Rt)
    f.arc(C2, Rt, 270 - th, 270)
    f.arc(C2, Rt + w, 270 - th, 270)
    x2 = C2[0]
    ub, ut = C2[1] - Rt, C2[1] - Rt - w        # upper duct bottom and top
    f.line((x2, ut), (x2, ub))
    f.line((x2, ut), (xr, ut))
    f.line((x2, ub), (xr, ub))
    # D between the elbow ends
    f.dim((x1, ytop), (x2, ut), (x1, 45), (x2, 45), "D", gap=6)
    # labels
    f.text((205, (ytop + ybot) / 2), '16"x20"')
    f.text((x2 + 78, (ut + ub) / 2 - 8), '16"x20"', anchor="start")
    f.text(pol(C1, Rt + 0.55 * w, 90 - th / 2), "38°")
    f.text(pol(C2, Rt + 0.55 * w, 270 - th / 2), "38°")
    tip = pol(C1, Rt, 90 - th * 0.22)
    f.leader([tip, (640, 362), (672, 362)])
    f.text((680, 362), "1'-6\" R", anchor="start")
    tip = pol(C2, Rt, 270 - th * 0.22)
    f.leader([tip, (1045, 632), (1090, 632)])
    f.text((1098, 632), "1'-6\" R", anchor="start")
    f.leader([(1290, ub), (1340, 612), (1372, 612)])
    f.text((1378, 612), "B= 12'-3\"", anchor="start")
    f.leader([(240, ybot), (300, 920), (360, 920)])
    f.text((366, 920), "B= 9'-8-1/2\"", anchor="start")
    f.leader([(690, 870), (750, 985), (805, 985)])
    f.text((812, 985), "CEILING HT.", anchor="start")
    f.text((812, 1030), "9'-0\"", anchor="start")
    return f


def f20_q101():
    """Plan: 12"x10" duct between grid lines 3 and 4 (16'), offset with two 40 deg elbows (throat R 14");
    centerlines 5'-7" and 7'-9-1/2" from grid line 3; trim joint L."""
    f = Fig((20, 50, 1590, 1250), 600)
    f.fs = FS
    th = 34.0                                   # elbow angle as drawn (labelled 40 deg)
    s, c = math.sin(math.radians(th)), math.cos(math.radians(th))
    w, Rt = 118.0, 157.0
    xl, xrw, yj = 514.0, 632.0, 524.0           # upper duct walls, end of the straight upper duct
    g3, g4 = 88.0, 1525.0
    # grid lines with bubbles
    for x, lab in ((g3, "3"), (g4, "4")):
        f.ellipse((x, 116), 50, 50, w=f.tw * 1.2)
        f.text((x, 116), lab, size=FS * 1.5)
        f.line((x, 166), (x, 1232), thin=True)
    f.dim((g3, 247), (g4, 247), (g3, 247), (g4, 247), "16'", ext=(False, False))
    # upper duct
    f.line((xl, 60), (xl, yj))
    f.line((xrw, 60), (xrw, yj))
    f.line((xl, yj), (xrw, yj))
    # elbow 1: throat is the right wall
    C1 = (xrw + Rt, yj)
    f.arc(C1, Rt, 180, 180 - th)
    f.arc(C1, Rt + w, 180, 180 - th)
    T1, H1 = pol(C1, Rt, 180 - th), pol(C1, Rt + w, 180 - th)
    f.line(T1, H1)
    # straight trim joint, length chosen so the lower duct lands where printed (left wall x = 703)
    d = (s, c)
    S = (703.0 - xl - 2 * (Rt + w / 2) * (1 - c)) / s
    T2, H2 = vadd(T1, d, S), vadd(H1, d, S)
    f.line(T1, T2)
    f.line(H1, H2)
    f.line(T2, H2)
    # elbow 2: throat is the left wall
    C2 = vadd(H2, (-c, s), Rt)
    f.arc(C2, Rt, -th, 0)
    f.arc(C2, Rt + w, -th, 0)
    lx1, lx2, yl = C2[0] + Rt, C2[0] + Rt + w, C2[1]
    f.line((lx1, yl), (lx2, yl))
    f.line((lx1, yl), (lx1, 1232))
    f.line((lx2, yl), (lx2, 1232))
    # L along the centre line of the trim joint
    M1, M2 = mid(T1, H1), mid(T2, H2)
    f.dim(M1, M2, M1, M2, "L", ext=(False, False))
    # centre-line dimensions from grid line 3
    xc1, xc2 = (xl + xrw) / 2, (lx1 + lx2) / 2
    f.dim((g3, 449), (xc1, yj - 4), (g3, 449), (xc1, 449), "5'-7\"", ext=(False, True))
    yd = yl + 58
    f.dim((g3, yd), (xc2, yl + 4), (g3, yd), (xc2, yd), "7'-9 1/2\"", ext=(False, True))
    # labels
    f.text((xc1, 350), '12"x10"', rot=-90)
    f.text((xc2, (yl + 76 + 1232) / 2), '12"x10"', rot=-90)
    f.text(pol(C1, Rt + 0.62 * w, 180 - th * 0.45), "40°")
    f.text(pol(C2, Rt + 0.62 * w, -th * 0.45), "40°")
    tip = pol(C1, Rt, 180 - th * 0.35)
    f.leader([tip, (705, 588), (735, 588)])
    f.text((742, 588), '14" R', anchor="start")
    tip = pol(C2, Rt, -th * 0.35)
    f.leader([tip, (640, yl - 30), (612, yl - 30)])
    f.text((605, yl - 30), '14" R', anchor="end")
    return f


def _owl_panel(f, o, letter, shape, dims):
    """One notched duct half. o = origin of the panel (model); shape = outline points and fold line
    (local coords); dims = list of dimension specs in local coords."""
    P = lambda p: (o[0] + p[0], o[1] + p[1])  # noqa: E731
    outline, fold, lab12, lab16, bub = shape
    f.poly([P(p) for p in outline], closed=True)
    f.line(P(fold[0]), P(fold[1]))
    f.text(P(lab12), '12"')
    f.text(P(lab16), '16"')
    f.ellipse(P(bub), 30, 30, w=f.tw * 1.2)
    f.text(P(bub), letter, size=FS * 1.45)
    for kind, a, b, y, lab, side in dims:
        if kind == "w":                         # 60" overall, arrows inside
            f.dim(P(a), P(b), P((a[0], y)), P((b[0], y)), lab)
        else:                                   # narrow notch: arrows outside, label beside
            f.dim(P(a), P(b), P((a[0], y)), P((b[0], y)), None, arrows="out", tail=16)
            if side == "r":
                f.text(P((b[0] + 56, y)), lab, anchor="start")
            else:
                f.text(P((a[0] - 56, y)), lab, anchor="end")


def f20_q105():
    """OWL: four notched halves of a 16"x12" duct, 60" long (12" side above the fold, 16" side below)."""
    f = Fig((150, 600, 1745, 1720), 600)
    f.fs = FS
    n = 22.0                                    # drawn width of a notch (printed about 20 px)
    # A: both sides taper to the fold line by 1-5/8" at each end (V at each end)
    xa0, xa1, yt, yf, yb = 100.0, 540.0, 115.0, 258.0, 450.0
    _owl_panel(f, (256, 605), "A",
               ([(xa0, yt), (xa1, yt), (xa1 - n, yf), (xa1, yb), (xa0, yb), (xa0 + n, yf)],
                ((xa0 + n, yf), (xa1 - n, yf)), (52, 186), (52, 355), (70, 30)),
               [("n", (xa0, yt), (xa0 + n, yf), 80, '1-5/8"', "r"),
                ("n", (xa1 - n, yf), (xa1, yt), 80, '1-5/8"', "r"),
                ("w", (xa0, yb), (xa1, yb), 492, '60"', None)])
    # B: the 12" side is a parallelogram slanted 1-1/4"; the 16" side square
    xb0, xb1, yt, yf, yb = 157.0, 577.0, 118.0, 260.0, 450.0
    _owl_panel(f, (1000, 605), "B",
               ([(xb0 - n, yt), (xb1 - n, yt), (xb1, yf), (xb1, yb), (xb0, yb), (xb0, yf)],
                ((xb0, yf), (xb1, yf)), (88, 190), (92, 365), (100, 30)),
               [("n", (xb1 - n, yt), (xb1, yf), 70, '1-1/4"', "l"),
                ("n", (xb0 - n, yt), (xb0, yb), 470, '1-1/4"', "l"),
                ("w", (xb0 - n, yb), (xb1, yb), 505, '60"', None)])
    # C and D: the 16" side is a parallelogram (C 1-5/8", D 1-1/4"); the 12" side square
    for org, letter, lab, x0, x1, bub in (((215, 1165), "C", '1-5/8"', 150.0, 562.0, (80, 45)),
                                          ((1000, 1165), "D", '1-1/4"', 160.0, 575.0, (95, 40))):
        yt, yf, yb = 157.0, 298.0, 486.0
        _owl_panel(f, org, letter,
                   ([(x0, yt), (x1, yt), (x1, yf), (x1 - n, yb), (x0 - n, yb), (x0, yf)],
                    ((x0, yf), (x1, yf)), (92, 232), (84, 400), bub),
                   [("w", (x0, yt), (x1, yt), 105, '60"', None),
                    ("n", (x0 - n, yb), (x0, yf), 520, lab, "l"),
                    ("n", (x1 - n, yb), (x1, yf), 520, lab, "r")])
    return f


FIGS = {
    "f20-q100": f20_q100,
    "f20-q101": f20_q101,
    "f20-q105": f20_q105,
}


def main(names):
    OUT.mkdir(parents=True, exist_ok=True)
    for name in names or FIGS:
        fig = FIGS[name]()
        (OUT / f"{name}.svg").write_text(fig.svg(), encoding="utf-8")
        print(f"{name}.svg  viewBox {f2(fig.W)} x {f2(fig.H)}")


if __name__ == "__main__":
    main(sys.argv[1:])
