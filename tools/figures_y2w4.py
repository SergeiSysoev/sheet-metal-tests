#!/usr/bin/env python3
"""Clean SVG redraws for SMY2W4 Fitting Review — Monday Written (Y2W4M) and Friday Written/Math Wk4 (Y2W4F).

References (photos are NOT shipped, they are only the reference):
  Y2W4M  /Users/assistant/.telegram-archive/local_66/inbox/msg_1871 (No.11, 12), msg_1872 (No.13, 14),
         msg_1873 (No.15, 16), msg_1881 (No.50), msg_1883 (No.55, 56),
         msg_1884 (No.59), msg_1885 (No.60)
  Y2W4F  msg_1891 (No.19, 20), msg_1892 (No.21), msg_1900 (No.64)
Reused drawings: Monday No.59 = SMY2W3 Friday No.30 (y2w3f_q30),
Friday No.64 = T90 No.76 (t90_q76) — same printed drawings, the questions differ.

The round elbows (No.11-16, No.60) are drawn with true gored-elbow geometry, as on the sheets (they are
drawn to scale there too); the other figures use the pixel coordinates of the photos (y down).

    python3 tools/figures_y2w4.py                 # write every figure into img/
    python3 tools/figures_y2w4.py y2w4m-q50       # only this one

Standard library only.
"""
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from figures import Fig, OUT, INK, f2, pol, mid, t90_q76  # noqa: E402
from figures_y2w3 import y2w3f_q30  # noqa: E402


# ============================================================== round gored elbows
def _gored_elbow(f, C, D, Rt, n, theta=90.0, dashed=(), seam=True):
    """Gored elbow seen from the side. C = radius point; the first end is horizontal (bottom, pipe going down),
    heel on the left/top, throat on the right/bottom. Returns a dict of useful points.
    Corners on the miter lines lie at R / cos(miter) from C (end gore height at radius R = R * tan(miter))."""
    Rh = Rt + D
    Rc = Rt + D / 2.0
    m = theta / (2 * (n - 1))
    cm = math.cos(math.radians(m))

    def P(r, phi):                      # phi measured from the bottom end line (pointing left), toward up
        return pol(C, r, 180 + phi)

    angs = [0.0] + [m * (2 * i + 1) for i in range(n - 1)] + [theta]
    heel = [P(Rh if a in (0.0, theta) else Rh / cm, a) for a in angs]
    thr = [P(Rt if a in (0.0, theta) else Rt / cm, a) for a in angs]
    f.poly(heel + list(reversed(thr)), closed=True)
    for a in angs[1:-1]:                # miter lines
        f.line(P(Rh / cm, a), P(Rt / cm, a))
    cl = [P(Rc if a in (0.0, theta) else Rc / cm, a) for a in angs]
    if seam:
        for i in range(n):
            if i in dashed:
                f.line(cl[i], cl[i + 1], w=f.lw * 0.75, dash=(7, 5))
            else:
                f.line(cl[i], cl[i + 1], w=f.lw * 0.9)
    return dict(heel=heel, thr=thr, cl=cl, angs=angs, m=m, Rh=Rh, Rc=Rc, P=P)


def _xmark(f, p, s=7):
    """Small x at the radius point."""
    P = f.P(p)
    f._line((P[0] - s, P[1] - s), (P[0] + s, P[1] + s), f.tw * 1.4)
    f._line((P[0] - s, P[1] + s), (P[0] + s, P[1] - s), f.tw * 1.4)


QS = 22                                                # size of the '?' labels

# 5-piece 90 deg elbow as on Monday No.11-16 (throat radius = diameter, true geometry)
E5 = dict(C=(400.0, 400.0), D=100.0, Rt=100.0, n=5)


def _elbow5(box, width=520):
    f = Fig(box, width)
    g = _gored_elbow(f, E5["C"], E5["D"], E5["Rt"], E5["n"], dashed=(1, 3))
    return f, g


def y2w4m_q11():
    """5-piece round elbow; dimension ? from the middle of the bottom end to the radius point x."""
    f, g = _elbow5((150, 160, 450, 470))
    C = E5["C"]
    x0 = g["cl"][0][0]
    y = C[1] + 42
    _xmark(f, (C[0], C[1] - 6))
    f.dim((x0, C[1]), (C[0], C[1] + 4), (x0, y), (C[0], y), "?", gap=4, size=QS)
    return f


def y2w4m_q12():
    """5-piece round elbow; leader ? to the miter line between the top end gore and the next gore."""
    f, g = _elbow5((150, 160, 460, 420))
    P = g["P"]
    a = g["angs"][-2]                                   # last miter line
    tip = mid(P(g["Rh"] / math.cos(math.radians(g["m"])), a), P(E5["Rt"] / math.cos(math.radians(g["m"])), a), 0.22)
    f.leader([tip, (405, 182), (428, 182)])
    f.text((434, 182), "?", anchor="start", size=QS)
    return f


def y2w4m_q13():
    """5-piece round elbow; dimension ? from the inside (throat) edge of the bottom end to the radius point x."""
    f, g = _elbow5((150, 160, 450, 470))
    C = E5["C"]
    x0 = g["thr"][0][0]
    y = C[1] + 42
    _xmark(f, (C[0], C[1] - 6))
    f.dim((x0, C[1]), (C[0], C[1] + 4), (x0, y), (C[0], y), "?", gap=4, size=QS)
    return f


def y2w4m_q14():
    """5-piece round elbow; leader ? into the first middle gore."""
    f, g = _elbow5((110, 160, 440, 420))
    P = g["P"]
    tip = P(g["Rh"] - 14, 2 * g["m"] + 2)
    f.leader([tip, (172, 262), (146, 262)])
    f.text((140, 262), "?", anchor="end", size=QS)
    return f


def y2w4m_q15():
    """5-piece round elbow; leader ? to the seam line of the bottom end gore."""
    f, g = _elbow5((150, 160, 430, 460))
    a, b = g["cl"][0], g["cl"][1]
    tip = mid(a, b, 0.45)
    f.leader([tip, (318, 440), (338, 440)])
    f.text((344, 440), "?", anchor="start", size=QS)
    return f


def y2w4m_q16():
    """5-piece round elbow; leader ? into the bottom end gore."""
    f, g = _elbow5((110, 160, 440, 420))
    C = E5["C"]
    tip = (C[0] - g["Rh"] + 30, C[1] - 13)
    f.leader([tip, (180, 362), (146, 362)])
    f.text((140, 362), "?", anchor="end", size=QS)
    return f


def y2w4m_q60():
    """3-piece 90 deg round elbow, 8"Ø, 12"R to the throat, 90 deg; ? = height of the end gore at the centerline."""
    s = 37.5                                             # px per inch (as printed, to scale)
    C = (535.0 + 12 * s, 780.0)
    f = Fig((30, 10, 1130, 920), 560)          # 20 units more room on top: the heel line touched the edge
    g = _gored_elbow(f, C, 8 * s, 12 * s, 3)
    P = g["P"]
    m = g["m"]
    cm = math.cos(math.radians(m))
    yq = g["cl"][1][1]                                  # centerline point on the first miter line
    xh = g["heel"][0][0]
    xd = xh - 135
    f.line((xd - 40, yq), (g["cl"][1][0] - 26, yq), thin=True)
    f.line((xd - 40, C[1]), (xh - 25, C[1]), thin=True)
    f.dim((xd, yq), (xd, C[1]), (xd, yq), (xd, C[1]), "?", ext=(False, False), size=QS)
    f.text(((g["heel"][0][0] + g["thr"][0][0]) / 2, C[1] + 55), '8"Ø', size=21)
    mid_h = P(12 * s / cm + 0.6 * 8 * s, 2 * m)
    f.text(mid_h, "90°", size=21)
    tip = P(12 * s, 2 * m + 6)                           # throat line of the middle gore
    f.leader([tip, (C[0] - 120, C[1] - 40), (C[0] - 70, C[1] - 40)], arrow=True)
    f.text((C[0] - 62, C[1] - 40), '12"R', anchor="start", size=21)
    return f


# ================================================= Monday No.50 and No.56 (plan, two elbows)
def _turn(g):
    """Plan view: L-shaped concrete wall, pipe B through the bottom wall, pipe A through the right wall,
    dimensions from A's centre line to B's wall face and from B's centre line to A's wall face."""
    f = Fig(g["box"], 640)
    hw_t, hw_b, x_l, x_r = g["hwall"]                 # horizontal wall: top, bottom, left end, outer right
    vw_l, y_t = g["vwall"]                            # vertical wall: inner (left) face, top end
    ax0, ay0, ax1, ay1 = g["A"]
    bx0, by0, bx1, by1 = g["B"]
    # concrete
    f.concrete([(x_l, hw_t), (bx0, hw_t), (bx0, hw_b), (x_l, hw_b)], seed=3, n_tri=4, n_dot=20)
    f.concrete([(bx1, hw_t), (vw_l, hw_t), (vw_l, ay1), (x_r, ay1), (x_r, hw_b), (bx1, hw_b)],
               seed=5, n_tri=22, n_dot=90)
    f.concrete([(vw_l, y_t), (x_r, y_t), (x_r, ay0), (vw_l, ay0)], seed=7, n_tri=4, n_dot=16)
    # wall outlines
    f.line((x_l, hw_t), (bx0, hw_t))
    f.line((x_l, hw_b), (bx0, hw_b))
    f.poly([(bx1, hw_t), (vw_l, hw_t), (vw_l, ay1)])
    f.poly([(bx1, hw_b), (x_r, hw_b), (x_r, ay1)])
    f.line((vw_l, ay0), (vw_l, y_t))
    f.line((x_r, ay0), (x_r, y_t))
    f.zbreak((x_l, hw_t - 6), (x_l, hw_b + 6), 0.5, h=6, amp=6, w=f.tw * 1.3)
    f.zbreak((vw_l - 6, y_t), (x_r + 6, y_t), 0.5, h=6, amp=6, w=f.tw * 1.3)
    # pipe boxes
    f.poly([(ax0, ay0), (ax1, ay0), (ax1, ay1), (ax0, ay1)], closed=True)
    f.poly([(bx0, by0), (bx1, by0), (bx1, by1), (bx0, by1)], closed=True)
    acy, bcx = (ay0 + ay1) / 2, (bx0 + bx1) / 2
    f.text(((ax0 + ax1) / 2, acy), "A")
    f.text((bcx, (by0 + by1) / 2), "B")
    # size: brace on the right of A, text below B
    bx = ax1 + 3
    f.poly([(bx - 3, ay0), (bx + 4, ay0), (bx + 4, acy - 9), (bx + 11, acy), (bx + 4, acy + 9),
            (bx + 4, ay1), (bx - 3, ay1)], thin=True, join="round")
    f.text((bx + 16, acy), g["size"], anchor="start")
    f.text((bcx + 8, by1 + 24), g["size"])
    # vertical dimension: A centre line -> B wall face
    xv = g["xv"]
    f.dim((ax0 - 12, acy), (bx0 - 8, by0), (xv, acy), (xv, by0), g["v"], gap=0, ovr=14)
    # horizontal dimension: B centre line -> A wall face
    yh = g["yh"]
    f.dim((bcx, by0 - 6), (ax0, ay1 + 12), (bcx, yh), (ax0, yh), g["h"], gap=6, ovr=12)
    return f


Q50 = dict(box=(40, 20, 1440, 1100), hwall=(860.0, 905.0, 65.0, 1210.0), vwall=(1155.0, 40.0),
           A=(1108.0, 165.0, 1258.0, 278.0), B=(205.0, 848.0, 318.0, 1015.0),
           xv=150.0, yh=790.0, v="8'-9\"", h="9'-8\"", size='12"Ø')
Q56 = dict(box=(0, 0, 1400, 820), hwall=(672.0, 705.0, 25.0, 1180.0), vwall=(1133.0, 25.0),
           A=(1088.0, 130.0, 1240.0, 215.0), B=(165.0, 636.0, 278.0, 765.0),
           xv=118.0, yh=592.0, v="7'-1\"", h="14'-7\"", size='28"Ø')


def y2w4m_q50():
    """Two elbows A and B turning 90 deg, 12"Ø, 8'-9" and 9'-8" (read from a blurred photo)."""
    return _turn(Q50)


def y2w4m_q56():
    """Two elbows A and B turning 90 deg, 28"Ø, 7'-1" and 14'-7"."""
    return _turn(Q56)


# ====================================================================== Monday No.55
def y2w4m_q55():
    """Round window: chord 1'-6", rise 6" from the chord to the top of the circle (to scale, inches)."""
    R = 9.75
    yc = -(R - 6.0)                                     # chord level (centre at 0,0, y down)
    hc = math.sqrt(R * R - yc * yc)
    f = Fig((-11.2, -10.9, 15.6, 10.5), 560)
    f.el.append(f'<circle cx="{f2(f.P((0, 0))[0])}" cy="{f2(f.P((0, 0))[1])}" r="{f2(R * f.k)}"'
                f' fill="none" stroke="{INK}" stroke-width="{f2(f.lw * 0.8)}"/>')
    xr = 14.2
    f.line((0, -R), (xr, -R), w=f.lw * 0.8)
    f.line((-hc, yc), (xr, yc), w=f.lw * 0.8)
    f.dim((xr, -R), (xr, yc), (13.4, -R), (13.4, yc), '6"', ext=(False, False))
    yd = yc + 1.7
    f.dim((-hc, yc + 0.5), (hc, yc + 0.5), (-hc, yd), (hc, yd), "1'-6\"", gap=0, ovr=0.6 * f.k)
    return f


# ====================================================== Friday No.19-21 (hoisting signals)
def _body(f, arms):
    """Half-length worker facing the viewer, hard hat, shirt with pocket, belt. Arms drawn by `arms`."""
    lw = f.lw
    # hard hat and head
    f._path(_d(f, [("M", (-56, 62)), ("C", (-56, -6), (56, -6), (56, 62))]), lw)
    f._path(_d(f, [("M", (-74, 64)), ("Q", (0, 52), (74, 64))]), lw)
    a = math.degrees(math.asin((64 - 104) / 54.0))
    f.ellipse_arc((0, 104), 44, 54, a, 180 - a, w=lw)
    for x in (-17, 17):
        f.el.append(f'<circle cx="{f2(f.P((x, 96))[0])}" cy="{f2(f.P((x, 96))[1])}" r="{f2(3.4 * f.k)}" fill="{INK}"/>')
    f.line((0, 101), (-3, 116), w=lw * 0.6)
    f.line((-11, 132), (11, 132), w=lw * 0.7)
    # neck, collar
    f.line((-20, 156), (-22, 170), w=lw * 0.8)
    f.line((20, 156), (22, 170), w=lw * 0.8)
    f.poly([(-40, 166), (-6, 196), (0, 176), (6, 196), (40, 166)], w=lw * 0.8, join="round")
    # torso, placket, pocket
    f.poly([(-40, 166), (-104, 186)], w=lw)
    f.poly([(40, 166), (104, 186)], w=lw)
    f.line((-98, 236), (-94, 356))
    f.line((98, 236), (94, 356))
    f.line((0, 196), (0, 356), w=lw * 0.7)
    f.poly([(26, 232), (72, 232), (72, 286), (26, 286)], closed=True, w=lw * 0.7)
    f.line((26, 246), (72, 246), w=lw * 0.6)
    # belt and trousers (cut off below the hips)
    f.poly([(-97, 356), (97, 356), (98, 378), (-98, 378)], closed=True, fill=INK, w=lw * 0.6)
    f.line((-98, 378), (-104, 500))
    f.line((98, 378), (104, 500))
    f.line((0, 378), (0, 440), w=lw * 0.6)
    arms(f)


def _d(f, cmds):
    out = []
    for c in cmds:
        pts = " ".join(f"{f2(f.P(p)[0])},{f2(f.P(p)[1])}" for p in c[1:])
        out.append(c[0] + pts)
    return " ".join(out)


def _hanging_arm(f, s):
    """Arm hanging at the side, s = +1 viewer's right, -1 viewer's left."""
    lw = f.lw
    f.line((s * 104, 186), (s * 130, 396))
    f.line((s * 98, 236), (s * 106, 396))
    f.line((s * 104, 396), (s * 132, 396), w=lw * 0.8)
    f.ellipse((s * 119, 424), 15, 27, w=lw * 0.9)


def _fist(f, x0, y0, x1, y1):
    f.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], closed=True, w=f.lw * 0.9, join="round")
    for k in (1, 2):
        y = y0 + (y1 - y0) * k / 3
        f.line((x0 + 4, y), (x0 + 0.45 * (x1 - x0), y), w=f.lw * 0.5)


def y2w4f_q19():
    """Arm extended horizontally to the side, fist closed, thumb up (crane hook block behind the arm)."""
    f = Fig((-470, -30, 170, 510), 520)

    def arms(f):
        # hoist lines and hook block behind the arm
        for x in (-292, -272, -252):
            f.line((x, -24), (x, 166), w=f.lw * 1.2)
            f.line((x, 214), (x, 300), w=f.lw * 1.2)
        f._path(_d(f, [("M", (-300, 300)), ("L", (-244, 300)), ("Q", (-226, 300), (-226, 320)),
                       ("L", (-232, 410)), ("Q", (-236, 430), (-256, 432)), ("L", (-288, 432)),
                       ("Q", (-306, 430), (-310, 410)), ("L", (-316, 320)), ("Q", (-316, 300), (-300, 300))]), f.lw)
        f._path(_d(f, [("M", (-268, 432)), ("L", (-268, 450)), ("Q", (-268, 478), (-248, 478)),
                       ("Q", (-232, 478), (-232, 462))]), f.lw)
        # extended arm (in front of the hoist lines)
        f.poly([(-104, 186), (-170, 170), (-388, 170)], w=f.lw, join="round")
        f.poly([(-98, 236), (-170, 214), (-388, 210)], w=f.lw, join="round")
        f.el.append(f'<rect x="{f2(f.P((-387, 171))[0])}" y="{f2(f.P((-387, 171))[1])}" '
                    f'width="{f2(140 * f.k)}" height="{f2(38 * f.k)}" fill="#fff"/>')
        f.line((-388, 170), (-250, 170), w=f.lw)
        f.line((-388, 210), (-250, 210), w=f.lw)
        f.line((-388, 166), (-388, 214), w=f.lw * 0.8)
        _fist(f, -436, 174, -390, 212)
        f.poly([(-424, 174), (-424, 134), (-410, 134), (-410, 174)], w=f.lw * 0.9, join="round")
        _hanging_arm(f, 1)

    _body(f, arms)
    return f


def y2w4f_q20():
    """Both fists in front of the body at waist level, thumbs pointing outward."""
    f = Fig((-250, -30, 250, 510), 420)

    def arms(f):
        for s in (-1, 1):
            f.line((s * 104, 186), (s * 136, 330))
            f.line((s * 98, 236), (s * 108, 330))
            f.line((s * 104, 330), (s * 140, 330), w=f.lw * 0.8)
            x0, x1 = sorted((s * 108, s * 150))
            _fist(f, x0, 334, x1, 370)
            xa, xb = sorted((s * 150, s * 196))
            f.poly([(xa, 340), (xb, 340), (xb, 354), (xa, 354)], closed=True, w=f.lw * 0.9, join="round")

    _body(f, arms)
    return f


def y2w4f_q21():
    """Upper arm out to the side, forearm vertical, index finger up, hand making small circles."""
    f = Fig((-330, -130, 170, 510), 430)

    def arms(f):
        f.poly([(-104, 186), (-210, 176), (-200, 42)], w=f.lw, join="round")
        f.poly([(-98, 236), (-258, 226), (-248, 42)], w=f.lw, join="round")
        f.line((-250, 42), (-198, 42), w=f.lw * 0.8)
        _fist(f, -246, 0, -204, 40)
        f.poly([(-232, 0), (-232, -52), (-218, -52), (-218, 0)], w=f.lw * 0.9, join="round")
        c, rx, ry = (-225, -58), 50, 17
        for a0, a1 in ((200, 262), (278, 340)):
            f.ellipse_arc(c, rx, ry, a0, a1, w=f.lw * 0.8)
        for a, sgn in ((200, -1), (340, 1)):
            p = (c[0] + rx * math.cos(math.radians(a)), c[1] + ry * math.sin(math.radians(a)))
            tang = (-rx * math.sin(math.radians(a)) * sgn, ry * math.cos(math.radians(a)) * sgn)
            f._arrow(f.P(p), (tang[0], tang[1]))
        _hanging_arm(f, 1)

    _body(f, arms)
    return f


FIGS = {
    "y2w4m-q11": y2w4m_q11,
    "y2w4m-q12": y2w4m_q12,
    "y2w4m-q13": y2w4m_q13,
    "y2w4m-q14": y2w4m_q14,
    "y2w4m-q15": y2w4m_q15,
    "y2w4m-q16": y2w4m_q16,
    "y2w4m-q50": y2w4m_q50,
    "y2w4m-q55": y2w4m_q55,
    "y2w4m-q56": y2w4m_q56,
    "y2w4m-q59": y2w3f_q30,     # same printed drawing as SMY2W3 Friday No.30 (options differ)
    "y2w4m-q60": y2w4m_q60,
    "y2w4f-q19": y2w4f_q19,
    "y2w4f-q20": y2w4f_q20,
    "y2w4f-q21": y2w4f_q21,
    "y2w4f-q64": t90_q76,       # same printed drawing as T90 No.76 / SMY2W2 Monday No.34
}


def main(names):
    OUT.mkdir(parents=True, exist_ok=True)
    for name in names or FIGS:
        fig = FIGS[name]()
        (OUT / f"{name}.svg").write_text(fig.svg(), encoding="utf-8")
        print(f"{name}.svg  viewBox {f2(fig.W)} x {f2(fig.H)}")


if __name__ == "__main__":
    main(sys.argv[1:])
