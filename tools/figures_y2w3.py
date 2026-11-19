#!/usr/bin/env python3
"""Clean SVG redraws for SMY2W3 Monday Written Review (Y2W3M) and SMY2W3 Friday Written (Y2W3F).

References (photos are NOT shipped, they are only the reference):
  Y2W3M  /Users/assistant/.telegram-archive/local_66/inbox/msg_1247 (No.23)
  Y2W3F  msg_1299 (No.23, 24), msg_1300 (No.26), msg_1301 (No.29, 30), msg_1302 (No.31, 32)
  No.25 and No.27 are the same printed drawings as SMY2W2 Monday No.43 and No.45 (functions reused).

Model coordinates are the pixels of the 960x1280 photos (y down), except No.29 (inches, drawn to scale
as printed). Style and helpers come from tools/figures.py.

    python3 tools/figures_y2w3.py                 # write every figure into img/
    python3 tools/figures_y2w3.py y2w3f-q30       # only this one

Standard library only.
"""
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from figures import (Fig, OUT, f2, pol, unit, vadd, vsub, mid, lnorm, angle_of,  # noqa: E402
                     mon_q43, mon_q45)


# ======================================================================= Monday
def y2w3m_q23():
    """Square-groove weld symbol: two parallel lines standing on a dashed reference line
    (as on the Monday copy the dashes also run between the two lines)."""
    f = Fig((180, 262, 600, 400), 600)
    y = 381.0
    x1, x2, top = 342.0, 393.0, 284.0
    f.line((x1, top), (x1, y + 3), w=12)
    f.line((x2, top), (x2, y + 3), w=12)
    dash = (27, 16)
    f.line((192, y), (x1 - 4, y), w=7.5, dash=dash)
    f.line((x1 + 4, y), (x2 - 14, y), w=7.5)
    f.line((x2 + 4, y), (588, y), w=7.5, dash=dash)
    return f


# ======================================================================= Friday
def y2w3f_q23():
    """Plan view: 16"x12" (BOD 9' 3-3/4") -> transition (TU, arrow, empty box) -> 14"x8" (BOD 10' 1")."""
    f = Fig((112, 150, 652, 392), 600)
    yb = 362.0
    yl, yr = 228.0, 243.0
    xL, xj1, xj2, xR = 140.0, 305.0, 462.0, 617.0
    f.line((xL, yl), (xj1, yl))
    f.line((xj1, yl), (xj2, yr))
    f.line((xj2, yr), (xR, yr))
    f.line((xL, yb), (xR, yb))
    f.line((xj1, yl), (xj1, yb))
    f.line((xj2, yr), (xj2, yb))
    f.zbreak((xL, yl - 8), (xL, yb + 10), (300 - (yl - 8)) / (yb + 10 - (yl - 8)), h=12, amp=15)
    f.zbreak((xR, yr - 8), (xR, yb + 10), (292 - (yr - 8)) / (yb + 10 - (yr - 8)), h=12, amp=15)
    f.rt((xj1, yb), (xj1, yl), (xj2, yb), 17)
    f.text((380, 258), "TU")
    f.line((346, 272), (428, 272), thin=True)
    f.arrow((428, 272), (346, 272))
    f.poly([(342, 282), (405, 282), (405, 300), (342, 300)], closed=True, w=f.lw * 0.8)
    f.text((210, 279), '16" x 12"')
    f.text((214, 318), "BOD= 9' 3-3/4\"")
    f.text((540, 272), '14" x 8"')
    f.text((538, 312), "BOD= 10' 1\"")
    f.text((385, 172), "PLAN VIEW")
    return f


def y2w3f_q24():
    """Right triangle: hypotenuse 2-3/8", vertical side 1-5/16", horizontal side A."""
    f = Fig((372, 470, 792, 772), 600)
    BL, BR, T = (431.0, 701.0), (689.0, 701.0), (689.0, 530.0)
    f.poly([BL, BR, T], closed=True)
    f.dim(T, BR, (733, T[1]), (733, BR[1]), '1 5/16"', gap=8)
    n = lnorm(unit(vsub(T, BL)))
    f.dim(BL, T, vadd(BL, n, 46), vadd(T, n, 46), '2 3/8"')
    f.dim(BL, BR, (BL[0], 744), (BR[0], 744), "A", gap=6)
    return f


def y2w3f_q26():
    """Right triangle: vertical side 4", 56 deg between the hypotenuse and the vertical side, hypotenuse x."""
    f = Fig((428, 28, 768, 250), 600)
    BL, BR, T = (481.0, 221.0), (681.0, 221.0), (681.0, 94.0)
    f.poly([BL, BR, T], closed=True)
    n = lnorm(unit(vsub(T, BL)))
    f.dim(BL, T, vadd(BL, n, 30), vadd(T, n, 30), "x", size=20)
    f.dim(T, BR, (720, T[1]), (720, BR[1]), '4"', gap=6)
    # 56 deg: label inside the triangle with two leader arrows (hypotenuse and vertical side), as printed
    hyp_pt = vadd(BL, unit(vsub(T, BL)), 0.585 * math.dist(BL, T))
    f.text((620, 186), "56°", size=19)
    f.leader([hyp_pt, (607, 174)])
    f.leader([(BR[0], 201), (643, 194)])
    return f


def y2w3f_q29():
    """Flat piece with a 45 deg corner cut (135 deg), R2" hole and two R1/4" holes; 7", 4", 9 1/2". Inches."""
    f = Fig((-2.3, -1.45, 13.1, 10.1), 600)
    P = [(4, 0), (11, 0), (11, 9.5), (0, 9.5), (0, 4)]
    f.poly(P, closed=True)
    c = (5.46, 4.78)
    f.ellipse(c, 2.0, 2.0)
    for h in ((2.73, 7.24), (8.03, 7.24)):
        f.ellipse(h, 0.2, 0.2, w=f.lw * 0.8)
        f.line((h[0] - 0.13, h[1]), (h[0] + 0.13, h[1]), thin=True)
        f.line((h[0], h[1] - 0.13), (h[0], h[1] + 0.13), thin=True)
    # R2": arrow on the circle, leader toward the centre, label inside
    tip = pol(c, 2.0, 231.6)
    f.leader([tip, (4.95, 4.2), (5.15, 4.2)])
    f.text((5.22, 4.2), 'R2"', anchor="start")
    # R1/4" leaders
    f.leader([(2.73, 7.03), (2.73, 6.35), (2.95, 6.35)])
    f.text((3.0, 6.35), 'R1/4"', anchor="start")
    f.leader([(8.18, 7.09), (8.62, 6.66), (8.82, 6.66)])
    f.text((8.87, 6.66), 'R1/4"', anchor="start")
    # dimensions
    f.dim((4, 0), (11, 0), (4, -0.62), (11, -0.62), '7"')
    f.dim((4, 0), (0, 4), (-0.62, 0), (-0.62, 4), '4"')
    f.dim((11, 0), (11, 9.5), (11.85, 0), (11.85, 9.5), '9 1/2"')
    f.angle((4, 0), 1.45, 0, 135, "135°", tpos=pol((4, 0), 1.45, 92))
    return f


def _offset(g):
    """Offset of two elbows with a straight piece D between them and overall L (SMY2W3 Friday No.30/31).
    g: C1 (centre of elbow 1), th (elbow angle), Rt (throat), Wd (duct depth / diameter), Ls (straight),
    xL / xR (duct ends), yL (L dimension), labels."""
    f = Fig(g["box"], 640)
    C1, th, Rt, Wd, Ls = g["C1"], g["th"], g["Rt"], g["Wd"], g["Ls"]
    Rh = Rt + Wd
    u = (math.sin(math.radians(th)), math.cos(math.radians(th)))
    t = (u[1], -u[0])
    C2 = vadd(vadd(C1, u, 2 * Rt + Wd), t, Ls)
    a1 = angle_of(u)
    a2 = a1 + 180
    xL, xR, yL = g["xL"], g["xR"], g["yL"]
    # lower duct + elbow 1
    f.line((xL, C1[1] + Rt), (C1[0], C1[1] + Rt))
    f.line((xL, C1[1] + Rh), (C1[0], C1[1] + Rh))
    f.arc(C1, Rt, 90, a1)
    f.arc(C1, Rh, 90, a1)
    f.line(C1, vadd(C1, u, Rh))
    # straight piece
    T1, H1 = vadd(C1, u, Rt), vadd(C1, u, Rh)
    f.line(T1, vadd(T1, t, Ls))
    f.line(H1, vadd(H1, t, Ls))
    # elbow 2 + upper duct
    f.arc(C2, Rt, a2, 270)
    f.arc(C2, Rh, a2, 270)
    f.line(C2, vadd(C2, u, -Rh))
    f.line((C2[0], C2[1] - Rt), (xR, C2[1] - Rt))
    f.line((C2[0], C2[1] - Rh), (xR, C2[1] - Rh))
    # verticals for L
    f.line((C1[0], yL), (C1[0], C1[1] + Rh), thin=True)
    f.line((C2[0], yL), (C2[0], C2[1] - Rt), thin=True)
    f.dim((C1[0], yL), (C2[0], yL), (C1[0], yL), (C2[0], yL), "L", ext=(False, False), size=27, bold=True)
    # D along the straight piece
    Q = vadd(C1, u, Rt + 0.5 * Wd)
    f.dim(Q, vadd(Q, t, Ls), Q, vadd(Q, t, Ls), "D", ext=(False, False), size=25, bold=True)
    # radius labels at the centres
    rl = g["rad"]
    f.line((C1[0] - 4, C1[1]), (C1[0] - 16, C1[1]), thin=True)
    f.text((C1[0] - 20, C1[1]), rl, anchor="end")
    f.line((C2[0] + 4, C2[1]), (C2[0] + 16, C2[1]), thin=True)
    f.text((C2[0] + 20, C2[1]), rl, anchor="start")
    # angle, sizes
    f.text(g["ang_pos"], f"{g['th']:g}°")
    for s, p in g["sizes"]:
        f.text(p, s)
    # elevations: arrow on the bottom line of each duct, leader to the text
    (pL, bL, tL1, tL2), (pR, bR, tR1, tR2) = g["floor"]
    yb1 = C1[1] + Rh
    yb2 = C2[1] - Rt
    f.leader([(pL, yb1), bL])
    f.text(tL1[1], tL1[0])
    f.text(tL2, "To Floor")
    f.leader([(pR, yb2), bR])
    f.text(tR1[1], tR1[0], anchor="start")
    f.text(tR2, "To Floor", anchor="start")
    return f


Q30 = dict(box=(222, 548, 872, 900), C1=(388.0, 646.0), th=30, Rt=92.0, Wd=92.0, Ls=196.0,
           xL=322.0, xR=770.0, yL=574.0, rad='24" Rad.', ang_pos=(420, 790),
           sizes=[('26 x 12', (300, 786)), ('26 x 12', (748, 652))],
           floor=((356.0, (342.0, 856.0), ("8'-4\"", (300.0, 862.0)), (290.0, 888.0)),
                  (726.0, (734.0, 722.0), ("11'-2\"", (744.0, 728.0)), (744.0, 754.0))))

Q31 = dict(box=(318, 92, 920, 508), C1=(478.0, 258.0), th=50, Rt=92.0, Wd=94.0, Ls=110.0,
           xL=400.0, xR=812.0, yL=116.0, rad='24" Rad.', ang_pos=(527, 396),
           sizes=[('30"Ø', (430, 392)), ('30"Ø', (800, 214))],
           floor=((440.0, (426.0, 470.0), ("10'-6\"", (392.0, 474.0)), (382.0, 500.0)),
                  (792.0, (798.0, 280.0), ("13'-4\"", (808.0, 286.0)), (808.0, 312.0))))


def y2w3f_q30():
    """Offset 26 x 12, 24" Rad. (throat), 30 deg, 8'-4" and 11'-2" to floor; L and D."""
    return _offset(Q30)


def y2w3f_q31():
    """Offset 30"Ø round, 24" Rad. (throat), 50 deg, 10'-6" and 13'-4" to floor; L and D."""
    return _offset(Q31)


def y2w3f_q32():
    """Transition side view: 8" x 12" -> 16" x 6", 15", FOT, square (∟) left side, drive hooks on both collars."""
    f = Fig((470, 640, 905, 950), 520)
    xl, xt, xb = 569.0, 717.5, 865.6
    t0, t1 = 676.0, 697.5            # top collar
    b0, b1 = 889.0, 910.0            # bottom collar
    f.poly([(xl, t0), (xt, t0), (xt, t1), (xl, t1)], closed=True)
    f.poly([(xl, b0), (xb, b0), (xb, b1), (xl, b1)], closed=True)
    f.line((xl, t1), (xl, b0))
    f.line((xt, t1), (xb, b0))
    f.rt((xl, b0), (xl, t1), (xb, b0), 20)
    hs = 14
    f.hook((xl, 683.0), (-1, 0), (0, 1), hs)
    f.hook((xt, 683.0), (1, 0), (0, 1), hs)
    f.hook((xl, 903.0), (-1, 0), (0, -1), hs)
    f.hook((xb, 903.0), (1, 0), (0, -1), hs)
    f.dim((xl - 12, 683.0), (xl - 12, 903.0), (532, 683.0), (532, 903.0), '15"', gap=4)
    f.text(((xl + xt) / 2, 660), '8" x 12"')
    f.text(((xl + xb) / 2, 930), '16" x 6"')
    f.text((666, 793), "FOT")
    return f


FIGS = {
    "y2w3m-q23": y2w3m_q23,
    "y2w3f-q23": y2w3f_q23,
    "y2w3f-q24": y2w3f_q24,
    "y2w3f-q25": mon_q43,     # same printed drawing as SMY2W2 Monday No.43 (options differ)
    "y2w3f-q26": y2w3f_q26,
    "y2w3f-q27": mon_q45,     # same printed drawing as SMY2W2 Monday No.45 (options differ)
    "y2w3f-q29": y2w3f_q29,
    "y2w3f-q30": y2w3f_q30,
    "y2w3f-q31": y2w3f_q31,
    "y2w3f-q32": y2w3f_q32,
}


def main(names):
    OUT.mkdir(parents=True, exist_ok=True)
    for name in names or FIGS:
        fig = FIGS[name]()
        (OUT / f"{name}.svg").write_text(fig.svg(), encoding="utf-8")
        print(f"{name}.svg  viewBox {f2(fig.W)} x {f2(fig.H)}")


if __name__ == "__main__":
    main(sys.argv[1:])
