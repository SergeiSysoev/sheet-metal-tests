#!/usr/bin/env python3
"""Clean SVG redraws for two SMY2W5 "Intro to Arch Metals" tests (photos are only the reference):

  Y2W5M  SMY2W5 Monday Written Review (2026-06-08), photos msg_2721 ... msg_2730 (rotated 90 deg)
  Y2W5Y  SMY2W5 Year End Cumulative Written Exam (2026-06-11), photos msg_2739 ... msg_2752

Geometry is written in the pixel coordinates of the reference crops (y down) or in inches where the
original is drawn to scale, so each redraw keeps the printed proportions. Helpers and style come from
tools/figures.py. Questions already in the bank (SMY2W3 Friday reuses most of the Monday test) get no figure here.

    python3 tools/figures_y2w5.py                 # write every figure into img/
    python3 tools/figures_y2w5.py y2w5m-q20       # only these

Standard library only.
"""
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from figures import (Fig, OUT, INK, f2, vadd, vsub, vmul, unit, pol, angle_of, lnorm)  # noqa: E402


# ---------------------------------------------------------------- small local helpers
def path(f, cmds, w=None, fill=None):
    """Path in model coordinates: cmds = [("M", p), ("L", p), ("Q", c, p), ("C", c1, c2, p), ("Z",)]."""
    out = []
    for c in cmds:
        pts = [f.P(p) for p in c[1:]]
        out.append(c[0] + " ".join(f"{f2(x)},{f2(y)}" for x, y in pts))
    f._path(" ".join(out), w or f.lw, fill=fill)


def dot_(f, p, r):
    P = f.P(p)
    f.el.append(f'<circle cx="{f2(P[0])}" cy="{f2(P[1])}" r="{f2(r * f.k)}" fill="{INK}"/>')


def open_arrow(f, tip, frm, size=14):
    """Open (chevron) arrowhead at tip, line coming from frm."""
    T, Fr = f.P(tip), f.P(frm)
    d = unit(vsub(T, Fr))
    n = (-d[1], d[0])
    s = size * f.u
    b = vadd(T, d, -s)
    f._poly([vadd(b, n, s * 0.55), T, vadd(b, n, -s * 0.55)], f.tw * 1.3)


def arc_arrows(f, c, r, a0, a1, w=None):
    """Arc (model) with filled arrowheads at both ends (motion arrow)."""
    f.arc(c, r, a0, a1, w=w or f.lw)
    C = f.P(c)
    R = r * f.k
    s = 1 if a1 > a0 else -1
    da = math.degrees(f.al * 1.5 / R)
    for a, back in ((a0, a0 + s * da), (a1, a1 - s * da)):
        p, q = pol(C, R, a), pol(C, R, back)
        f._arrow(p, vsub(p, q), al=f.al * 1.5, aw=f.aw * 1.8)


# ======================================================================= Y2W5M (Monday Written)
def y2w5m_q20():
    """Crane signal: forefinger pointing out, other hand held still under it (hoist slowly)."""
    f = Fig((40, 30, 360, 520), 360)
    lw = f.lw * 1.6
    # hard hat
    f.ellipse((265, 97), 54, 9, w=lw)
    path(f, [("M", (233, 92)), ("C", (231, 52), (297, 46), (298, 90))], w=lw)
    path(f, [("M", (236, 82)), ("Q", (265, 75), (296, 80))], w=f.tw * 1.4)
    # head
    path(f, [("M", (240, 106)), ("Q", (236, 142), (256, 158)), ("Q", (272, 168), (291, 151)),
             ("Q", (300, 132), (296, 106))], w=lw)
    dot_(f, (256, 123), 2.6)
    dot_(f, (279, 121), 2.6)
    f.line((262, 146), (276, 144), w=f.tw * 1.4)
    f.line((252, 160), (249, 174), w=lw)
    f.line((288, 156), (292, 172), w=lw)
    # pointing arm (crosses in front of the body), fist and forefinger
    path(f, [("M", (334, 186)), ("Q", (250, 160), (152, 150))], w=lw)
    path(f, [("M", (322, 236)), ("Q", (240, 206), (154, 188))], w=lw)
    f.line((152, 150), (154, 188), w=lw)
    path(f, [("M", (152, 152)), ("Q", (126, 142), (112, 152)), ("Q", (102, 168), (112, 184)),
             ("Q", (132, 194), (154, 186))], w=lw)
    path(f, [("M", (114, 151)), ("L", (66, 141)), ("Q", (58, 144), (64, 150)), ("L", (110, 162))], w=lw)
    f.line((118, 168), (140, 170), w=f.tw * 1.4)
    # the other hand, held still under the pointing hand, and its arm
    path(f, [("M", (98, 192)), ("Q", (90, 216), (102, 242)), ("L", (128, 242)), ("Q", (138, 216), (130, 194)),
             ("Q", (114, 186), (98, 192))], w=lw)
    f.line((106, 200), (106, 226), w=f.tw * 1.3)
    f.line((116, 198), (117, 228), w=f.tw * 1.3)
    path(f, [("M", (102, 242)), ("L", (156, 306)), ("Q", (182, 322), (206, 300))], w=lw)
    path(f, [("M", (128, 242)), ("L", (182, 276)), ("L", (206, 262))], w=lw)
    f.line((150, 270), (160, 262), w=f.tw * 1.3)
    # body
    f.line((206, 262), (206, 346), w=lw)
    path(f, [("M", (334, 186)), ("Q", (348, 262), (306, 346))], w=lw)
    f.line((258, 238), (254, 344), w=f.tw * 1.5)
    path(f, [("M", (268, 250)), ("L", (298, 248)), ("L", (296, 280)), ("L", (270, 282)), ("Z",)], w=f.tw * 1.5)
    f.poly([(204, 346), (308, 346), (308, 360), (204, 360)], closed=True, w=lw)
    f.line((206, 360), (199, 512), w=lw)
    f.line((304, 360), (307, 512), w=lw)
    f.line((255, 398), (251, 512), w=lw)
    return f


def y2w5m_q21():
    """Crane signal: both arms straight out, palms down, motion arrows at the hands (emergency stop)."""
    f = Fig((10, 40, 600, 430), 600)
    lw = f.lw * 1.6
    # hard hat and head
    f.ellipse((298, 98), 43, 7, w=lw)
    path(f, [("M", (268, 95)), ("C", (266, 60), (328, 56), (329, 95))], w=lw)
    path(f, [("M", (277, 104)), ("Q", (277, 132), (298, 140)), ("Q", (319, 132), (319, 104))], w=lw)
    dot_(f, (290, 114), 2.4)
    dot_(f, (307, 114), 2.4)
    f.line((293, 129), (303, 129), w=f.tw * 1.3)
    f.line((286, 138), (284, 150), w=lw)
    f.line((311, 138), (313, 150), w=lw)
    f.poly([(266, 150), (298, 168), (330, 150)], w=lw)
    # arms
    path(f, [("M", (266, 150)), ("Q", (190, 146), (132, 152))], w=lw)
    path(f, [("M", (256, 196)), ("Q", (186, 182), (134, 184))], w=lw)
    f.line((132, 152), (134, 184), w=lw)
    path(f, [("M", (132, 154)), ("L", (76, 158)), ("Q", (64, 166), (74, 174)), ("L", (134, 182))], w=lw)
    f.line((86, 166), (122, 166), w=f.tw * 1.3)
    path(f, [("M", (330, 150)), ("Q", (410, 150), (470, 164))], w=lw)
    path(f, [("M", (340, 198)), ("Q", (410, 186), (466, 196))], w=lw)
    f.line((470, 164), (466, 196), w=lw)
    path(f, [("M", (470, 166)), ("L", (530, 178)), ("Q", (544, 188), (532, 196)), ("L", (466, 196))], w=lw)
    f.line((480, 184), (516, 186), w=f.tw * 1.3)
    # motion arrows at the hands
    arc_arrows(f, (98, 164), 52, 215, 145, w=lw)
    arc_arrows(f, (500, 186), 52, -35, 35, w=lw)
    # body
    f.line((256, 196), (247, 282), w=lw)
    f.line((340, 198), (346, 282), w=lw)
    f.line((298, 168), (297, 278), w=f.tw * 1.5)
    f.poly([(260, 204), (286, 204), (286, 228), (260, 228)], closed=True, w=f.tw * 1.5)
    f.poly([(308, 204), (334, 204), (334, 228), (308, 228)], closed=True, w=f.tw * 1.5)
    f.poly([(245, 282), (348, 282), (348, 295), (245, 295)], closed=True, w=lw)
    f.line((249, 295), (234, 418), w=lw)
    f.line((344, 295), (354, 418), w=lw)
    f.poly([(284, 418), (292, 384), (300, 418)], w=lw)
    return f












def _plate(f, chamfer, top, height, circle, holes=(), squares=(), hlabel='9-1/2"'):
    """Sample plate in inches: chamfered top-left corner (45 deg), top edge `top` from the chamfer."""
    W = chamfer + top
    f.poly([(chamfer, 0), (W, 0), (W, height), (0, height), (0, chamfer)], closed=True)
    C, R = circle
    f.ellipse(C, R, R)
    for h in holes:
        f.ellipse(h, 0.25, 0.25, w=f.lw * 0.9)
        f.line((h[0] - 0.13, h[1]), (h[0] + 0.13, h[1]), thin=True)
        f.line((h[0], h[1] - 0.13), (h[0], h[1] + 0.13), thin=True)
    for (x, y) in squares:
        f.poly([(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)], closed=True)
    # top length from the end of the chamfer, chamfer height, overall height
    f.dim((chamfer, 0), (W, 0), (chamfer, -0.85), (W, -0.85), f'{top}"', size=20)
    f.dim((chamfer, 0), (0, chamfer), (-0.85, 0), (-0.85, chamfer), f'{chamfer}"', size=20, gap=0)
    f.dim((W, 0), (W, height), (W + 1.15, 0), (W + 1.15, height), hlabel, size=20,
          tpos=(W + 1.15, height * 0.47))
    V = (chamfer, 0)
    f.angle(V, 1.7, 0, 135, "135°", size=19, tpos=pol(V, 1.75, 66))
    tip = pol(C, R, 232)
    f.leader([tip, (C[0] - 0.42, C[1] - 0.42), (C[0] - 0.25, C[1] - 0.42)])
    f.text((C[0] - 0.2, C[1] - 0.42), 'R2"', anchor="start", size=19)
    return W












# ======================================================================= Y2W5Y (Year End exam)
def y2w5y_q59():
    """Sample plate (to scale, inches): 3" x 45 deg chamfer, 8" top, 9-1/2" high, R2" hole, two 1" squares."""
    f = Fig((-2.0, -1.75, 13.5, 10.2), 600)
    sq = ((1.5, 7.0), (8.5, 7.0))
    _plate(f, 3, 8, 9.5, ((5.5, 4.3), 2.0), squares=sq, hlabel='9 1/2"')
    # 1" dimensions of the squares
    x, y = sq[0]
    f.dim((x, y + 1), (x + 1, y + 1), (x, y + 1.85), (x + 1, y + 1.85), '1"', arrows="out", size=18, tail=24)
    f.dim((x + 1, y), (x + 1, y + 1), (x + 2.0, y), (x + 2.0, y + 1), '1"', arrows="out", size=18, tail=22)
    x, y = sq[1]
    f.dim((x, y), (x, y + 1), (x - 1.0, y), (x - 1.0, y + 1), '1"', arrows="out", size=18, tail=22)
    f.dim((x, y + 1), (x + 1, y + 1), (x, y + 1.85), (x + 1, y + 1.85), '1"', arrows="out", size=18, tail=24)
    return f


def y2w5y_q102():
    """Coping over a corner: vertical leg and top piece meeting at 105 deg (pictorial)."""
    f = Fig((60, 10, 640, 590), 520)
    A, B, C, D = (115.0, 190.0), (290.0, 300.0), (515.0, 45.0), (572.0, 195.0)
    E, F = (300.0, 532.0), (140.0, 545.0)
    f.poly([A, C, D, B], closed=True)
    f.line(A, F)
    f.line(B, E)
    f.poly([(118, 548), (192, 548), (214, 500), (238, 574), (262, 538), (340, 534)])
    f.leader([(440, 248), (440, 370)], arrow=True)
    f.leader([(304, 462), (400, 426)], arrow=True)
    f.text((428, 398), "105°", size=22, bold=True)
    return f


HOOKS = {  # top end, bottom end of each hook strip profile
    "A": ("flange_r", None), "B": ("kick", "kick"), "C": (None, "hook"), "D": ("flange_r", "kick"),
    "E": ("flange_r", "hook"), "F": (None, "kick"), "G": ("kick", "hook"), "H": ("flange_l", "kick"),
}


def y2w5y_q104():
    """Eight hook-strip profiles A-H (bend cleat / continuous cleat / J-hook questions)."""
    f = Fig((30, 0, 560, 500), 520)
    cols = (110.0, 220.0, 330.0, 440.0)
    rows = ((70.0, 210.0, "ABCD", 34.0), (280.0, 420.0, "EFGH", 466.0))
    for yt, yb, letters, yl in rows:
        for x, L in zip(cols, letters):
            top, bot = HOOKS[L]
            pts = [(x, yt), (x, yb)]
            if top == "flange_r":
                pts.insert(0, (x + 48, yt))
            elif top == "flange_l":
                pts.insert(0, (x - 48, yt))
            elif top == "kick":
                pts.insert(0, (x + 13, yt + 14))
            if bot == "kick":
                pts.append((x - 17, yb + 15))
            elif bot == "hook":
                pts.append((x - 15, yb - 17))
            f.poly(pts, join="miter")
            f.text((x + (4 if L not in "H" else 0), yl), L, size=28, bold=True)
    return f


def y2w5y_q107():
    """Coping in plan: 3'-2" outside, 2' 11-7/16" inside, 6" wide; miter angle A."""
    f = Fig((40, 20, 760, 470), 620)
    TL, TR, BL, BR = (76.0, 135.0), (545.0, 135.0), (76.0, 295.0), (480.0, 295.0)
    f.poly([TR, TL, BL, BR, TR])
    f.line(TR, (715.0, 325.0))
    f.line(BR, (625.0, 458.0))
    f.line((BR[0], TL[1]), BR, thin=True)
    a_m = angle_of(vsub(TR, BR)) % 360
    f.angle(BR, 62, 270, a_m, ends=(False, False))
    f.text((497, 196), "A", size=21)
    f.dim(TL, TR, (TL[0], 55), (TR[0], 55), "3'-2\"", size=20)
    f.dim(BL, BR, (BL[0], 375), (BR[0], 375), "2' 11-7/16", size=20)
    f.dim((178, TL[1]), (178, BL[1]), (178, TL[1]), (178, BL[1]), '6"', ext=(False, False), size=20)
    return f


def _roof(slopes):
    """Roof plan: main roof (ridge N-S, hip end at the bottom) with a wing (ridge E-W, hip end at the right)."""
    main, wing, end = slopes
    f = Fig((0, 20, 960, 745), 640)
    xl, xm, xr = 15.0, 245.0, 472.0          # main: left eave, ridge, right eave
    yt, yh, yb = 35.0, 598.0, 722.0          # main: top, hip point, bottom eave
    wy_t, wy_r, wy_b = 122.0, 272.0, 425.0   # wing: upper eave, ridge, lower eave
    xv, xwh, xwe = 305.0, 775.0, 935.0       # wing: valley point, hip point, end eave
    f.poly([(xl, yt), (xr, yt), (xr, wy_t), (xwe, wy_t), (xwe, wy_b), (xr, wy_b), (xr, yb), (xl, yb)],
           closed=True)
    f.line((xm, yt), (xm, yh))
    f.line((xm, yh), (xl, yb))
    f.line((xm, yh), (xr, yb))
    f.line((xv, wy_r), (xwh, wy_r))
    f.line((xv, wy_r), (xr, wy_t))
    f.line((xv, wy_r), (xr, wy_b))
    f.line((xwh, wy_r), (xwe, wy_t))
    f.line((xwh, wy_r), (xwe, wy_b))
    s = 16
    f.text((118, 430), f"{main} SLOPE", size=s)
    f.text((345, 426), f"{main} SLOPE", size=s)
    f.text((722, 142), f"{wing} SLOPE", size=s)
    f.text((742, 400), f"{wing} SLOPE", size=s)
    f.text((240, 712), f"{end} SLOPE", size=s)
    fs = 20
    f.text((316, 140), "VALLEY", size=fs - 1)
    f.text((316, 170), "FLASHING", size=fs - 1)
    f.leader([(312, 86), (326, 116)])
    f._path("M{0},{1} Q{2},{3} {4},{5}".format(*map(f2, (*f.P((392, 186)), *f.P((415, 212)), *f.P((458, 214))))),
            f.tw)
    f.arrow((458, 214), (440, 216))
    f.text((640, 214), "RIDGE", size=fs)
    f.text((640, 244), "FLASHING", size=fs)
    f.leader([(632, 152), (632, 192)])
    f._path("M{0},{1} Q{2},{3} {4},{5}".format(*map(f2, (*f.P((656, 282)), *f.P((664, 316)), *f.P((706, 334))))),
            f.tw)
    f.arrow((706, 334), (690, 330))
    f.text((360, 568), "HIP", size=fs)
    f.text((360, 598), "FLASHING", size=fs)
    f.leader([(424, 546), (392, 562)])
    f._path("M{0},{1} Q{2},{3} {4},{5}".format(*map(f2, (*f.P((346, 618)), *f.P((330, 648)), *f.P((328, 702))))),
            f.tw)
    f.arrow((328, 702), (329, 686))
    return f


def y2w5y_q108():
    """Roof plan, main 5/12, wing 8/12, hip end 12/12 (brake angle for the valley flashing)."""
    return _roof(("5/12", "8/12", "12/12"))


def y2w5y_q109():
    """Same roof plan as No.108 (brake angle for the hip flashing)."""
    return _roof(("5/12", "8/12", "12/12"))


def y2w5y_q110():
    """Roof plan, main 4/12, wing 9/12, hip end 14/12 (brake angle for the ridge flashing)."""
    return _roof(("4/12", "9/12", "14/12"))


def y2w5y_q111():
    """Gable building (pictorial): walls 19' high, 60' gable end (SIDE A), 99' long (SIDE B), roof pitch 3:12."""
    f = Fig((10, 40, 880, 790), 620)
    P1, P2, P3 = (112.0, 372.0), (232.0, 345.0), (378.0, 490.0)
    P4, P5 = (130.0, 570.0), (408.0, 690.0)
    P6, P7, P8, P9 = (765.0, 212.0), (790.0, 410.0), (622.0, 68.0), (498.0, 96.0)
    f.poly([P4, P1, P2, P3, P5], closed=True)
    f.poly([P3, P6, P7, P5])
    f.line(P1, P3)
    f.line(P1, P9)
    f.line(P9, P8)
    f.line(P2, P8)
    f.line(P8, P6)
    f.dim(P1, P4, (52, P1[1]), (52, P4[1]), "19'", size=20, gap=12, tpos=(52, 472))
    n = vmul(lnorm(unit(vsub(P5, P4))), -1)
    f.dim(P4, P5, vadd(P4, n, 64), vadd(P5, n, 64), "60'", size=20, gap=12)
    m = vmul(lnorm(unit(vsub(P7, P5))), -1)
    f.dim(P5, P7, vadd(P5, m, 64), vadd(P7, m, 64), "99'", size=20, gap=12)
    f.text((468, 290), "ROOF PITCH", size=19)
    f.text((468, 320), "3:12", size=19)
    f.text((248, 528), "SIDE A", size=19)
    f.text((598, 452), "SIDE B", size=19)
    return f


def _elbow(f, c, r_out=290.0, r_in=146.0, deg=30.0):
    """Loose 30 deg elbow drawn as an annular sector: heel arc on the left, throat arc on the right."""
    o0, o1 = f.P(pol(c, r_out, 180)), f.P(pol(c, r_out, 180 + deg))
    i0, i1 = f.P(pol(c, r_in, 180)), f.P(pol(c, r_in, 180 + deg))
    ro, ri = r_out * f.k, r_in * f.k
    f._path(f"M{f2(o0[0])},{f2(o0[1])} A{f2(ro)},{f2(ro)} 0 0 1 {f2(o1[0])},{f2(o1[1])} "
            f"L{f2(i1[0])},{f2(i1[1])} A{f2(ri)},{f2(ri)} 0 0 0 {f2(i0[0])},{f2(i0[1])} Z", f.lw)


def y2w5y_q63():
    """Trim joint (= Formula Sheets p.15): two 30 deg elbows R1'-6", 18"x20" ducts at 8'-2" and 12'-1" to floor,
    6'-5 7/8" between the duct ends; the trim joint and the trim are the two "?" (no answers on the drawing).
    Model = pixels of the formula-sheet page rendered at scale 2; the exam photo (msg_2747) shows the same drawing."""
    f = Fig((112, 252, 1440, 1206), 640)
    WL, WR, TOP, FL = 150.0, 1418.0, 268.0, 1157.0
    f.poly([(WL, FL), (WL, TOP), (WR, TOP), (WR, FL)])                     # room: walls and ceiling
    f.poly([(130, FL), (756.5, FL), (768.5, 1188.5), (792.5, 1125), (805, FL), (WR, FL)])   # floor with break
    # loose fittings: two elbows and the trim joint
    for c, lab, tip, frm, txt in (((506.0, 457.0), (288, 411), (363.1, 427), (418, 441), (424, 446)),
                                  ((477.0, 644.0), (259, 600), (335.0, 610), (398, 630), (404, 635))):
        _elbow(f, c)
        f.text(lab, "30°")
        f.leader([tip, frm])
        f.text(txt, 'R1\'-6"', anchor="start")
    f.poly([(544, 332), (1022, 332), (1022, 476), (544, 476)], closed=True)
    f.dim((544, 476), (1022, 476), (544, 561), (1022, 561), "?", gap=10)
    # installed ducts: lower one from the left wall (dashed cut line), upper one into the right wall
    f.poly([(WL, 711), (628, 711), (628, 855), (WL, 855)])
    f.line((533, 711), (533, 855), thin=True, dash=(9 * f.u, 5 * f.u))
    f.text((313, 782), '18"x20"')
    f.poly([(WR, 338), (1251, 338), (1251, 482), (WR, 482)])
    f.text((1336, 408), '18"x20"')
    # trim "?": extension lines through the dimension line, label to the right
    f.line((533, 640), (533, 688), thin=True)
    f.line((628, 640), (628, 688), thin=True)
    f.dim((533, 656), (628, 656), (533, 656), (628, 656), None, ext=(False, False))
    f.line((628, 656), (700, 656), thin=True)
    f.text((710, 656), "?", anchor="start")
    # 6'-5 7/8" between the duct ends
    f.line((628, 880), (628, 998), thin=True)
    f.line((1249, 505), (1249, 998), thin=True)
    f.dim((628, 981), (1249, 981), (628, 981), (1249, 981), "6'-5 7/8\"", ext=(False, False), tpos=(935, 981))
    # elevations of the duct bottoms
    for x, ytop, ty, label, tx, anc in ((373.0, 855.0, 1096.0, "8'-2\" TO FLOOR", 372.0, "middle"),
                                        (1337.0, 482.0, 1058.0, "12'-1\" TO FLOOR", 1406.0, "end")):
        f.line((x, FL), (x, ty + 20), thin=True)
        f.line((x, ty - 20), (x, ytop), thin=True)
        f.arrow((x, ytop), (x, ytop + 40))
        f.text((tx, ty), label, size=15, anchor=anc)
    return f


def y2w5y_q22():
    """Same flat oval as SMY2W2 Triangulation No.9 (R4" ends, 10" between centres)."""
    from figures import tri_q09
    return tri_q09()


def y2w5y_q113():
    """Same pattern as Test-90 No.57 (shear size, symmetrical about the centre line)."""
    from figures import t90_q57
    return t90_q57()


FIGS = {
    "y2w5m-q20": y2w5m_q20,
    "y2w5m-q21": y2w5m_q21,
    "y2w5y-q22": y2w5y_q22,     # = Triangulation No.9 drawing (question printed without the rounding hint)
    "y2w5y-q59": y2w5y_q59,
    "y2w5y-q63": y2w5y_q63,
    "y2w5y-q102": y2w5y_q102,
    "y2w5y-q104": y2w5y_q104,
    "y2w5y-q105": y2w5y_q104,   # same hook strips
    "y2w5y-q106": y2w5y_q104,   # same hook strips
    "y2w5y-q107": y2w5y_q107,
    "y2w5y-q108": y2w5y_q108,
    "y2w5y-q109": y2w5y_q109,
    "y2w5y-q110": y2w5y_q110,
    "y2w5y-q111": y2w5y_q111,
    "y2w5y-q113": y2w5y_q113,   # = Test-90 No.57 drawing (question printed with "Roundoff")
}


def main(names):
    OUT.mkdir(parents=True, exist_ok=True)
    for name in names or FIGS:
        fig = FIGS[name]()
        (OUT / f"{name}.svg").write_text(fig.svg(), encoding="utf-8")
        print(f"{name}.svg  viewBox {f2(fig.W)} x {f2(fig.H)}")


if __name__ == "__main__":
    main(sys.argv[1:])
