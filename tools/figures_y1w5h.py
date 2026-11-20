#!/usr/bin/env python3
"""Drawings for the SMY1W5 Orthographics & Ogee Offsets homework (src "Y1W5H"): the six shop-math
worksheets (perimeter, circumference and area tables, items 38-43) and the five solids
(cube, rectangular box, triangular prism, cylinder, trapezoid prism, items 44-48).
Our own line drawings with the printed numbers; the printed pictures are shaded 3D renders and
are not to scale, so the redraws keep their look and proportions, not true scale. No answers.

    python3 tools/figures_y1w5h.py               # write every figure into img/
    python3 tools/figures_y1w5h.py y1w5h-q44     # only these

Standard library only.
"""
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from figures import Fig, OUT  # noqa: E402


# ---------------------------------------------------------------- local helpers (model = view units)
def rect(f, x, y, w, h, lw=None):
    f.poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], closed=True, w=lw)


def txt(f, p, s, size, anchor="middle", bold=False):
    f.text(p, s, size=size, anchor=anchor, bold=bold)


def worksheet(title, cols, rows, width):
    """Fill-in table. cols = dicts (label before the box, x where that label ends, box x, box width,
    header above the column); rows = [(row label, [printed value or None per column])].
    Text is sized so it stays >= 14.5 units when the figure is shown 600 wide."""
    s_lab = max(18, math.ceil(14.5 * width / 600))
    s_val, s_tit = s_lab + 4, s_lab + 2
    top, rh = 96, 64
    H = top + rh * len(rows) + 10
    f = Fig((0, 0, width, H), width)
    txt(f, (18, 30), title, s_tit, anchor="start", bold=True)
    for c in cols:
        if c.get("header"):
            txt(f, (c["bx"] + c["bw"] / 2, top - 16), c["header"], s_lab, bold=True)
    for i, (rl, vals) in enumerate(rows):
        yc = top + rh * i + rh / 2
        txt(f, (cols[0]["rx"], yc), rl, s_lab, anchor="end", bold=True)
        for c, v in zip(cols, vals):
            if c.get("label"):
                txt(f, (c["lx"], yc), c["label"], s_lab, anchor="end", bold=True)
            rect(f, c["bx"], yc - 21, c["bw"], 42, lw=2.6)
            if v is not None:
                txt(f, (c["bx"] + 8, yc), v, s_val, anchor="start", bold=True)
    return f


def col(label, lx, bx, bw, header=None, rx=None):
    return {"label": label, "lx": lx, "bx": bx, "bw": bw, "header": header, "rx": rx}


# ---------------------------------------------------------------- 2D worksheets (printed numbers only)
def q38():
    cols = [col("Side #1=", 230, 236, 150, rx=96), col(None, 0, 450, 150, "Perimeter")]
    rows = [("1)", [None, "328"]), ("2)", ["59", None]), ("3)", [None, "68"])]
    return worksheet("Perimeter of a Square", cols, rows, 620)


def q39():
    cols = [col("Side #1=", 236, 242, 120, rx=100), col("Side #2=", 500, 506, 120),
            col(None, 0, 660, 120, "Perimeter")]
    rows = [("4)", ["11", None, "82"]), ("5)", ["53", "80", None]), ("6)", [None, "39", "196"])]
    return worksheet("Perimeter of a Rectangle", cols, rows, 800)


def q40():
    cols = [col("Radius=", 206, 212, 130, rx=96), col("Diameter=", 496, 502, 130),
            col(None, 0, 662, 228, "Circumference")]
    rows = [("7)", ["147", None, None]), ("8)", [None, None, "69.1150384"]),
            ("9)", ["157", None, None]), ("10)", [None, "134", None])]
    return worksheet("Circumference of a Circle", cols, rows, 900)


def q41():
    cols = [col("Side #1=", 230, 236, 150, rx=96), col(None, 0, 450, 150, "Area")]
    rows = [("1)", [None, "5776"]), ("2)", ["64", None]), ("3)", [None, "7921"])]
    return worksheet("Area of a Square", cols, rows, 620)


def q42():
    cols = [col("Side #1=", 236, 242, 120, rx=100), col("Side #2=", 500, 506, 120),
            col(None, 0, 660, 120, "Area")]
    rows = [("4)", ["34", "14", None]), ("5)", [None, "18", "1350"]), ("6)", ["9", None, "396"])]
    return worksheet("Area of a Rectangle", cols, rows, 800)


def q43():
    cols = [col("Radius=", 206, 212, 130, rx=96), col("Diameter=", 496, 502, 130),
            col(None, 0, 662, 228, "Area")]
    rows = [("7)", [None, "42", None]), ("8)", [None, "186", None]),
            ("9)", [None, None, "3848.451001"]), ("10)", [None, None, "14957.12262"])]
    return worksheet("Area of a Circle", cols, rows, 900)


# ---------------------------------------------------------------- solids: the drawing on top, the printed
# "Question #N" table under it (stacked so the text stays readable on a phone)
W3 = 600
S_LAB = 19
S_TAB = 19
TY = 318          # top of the table


def tag(f, x, y, w, h, l1, l2=None):
    """Label box like the printed one: name and number on one line, or on two lines."""
    rect(f, x, y, w, h, lw=2.0)
    if l2 is None:
        txt(f, (x + w / 2, y + h / 2), l1, S_LAB, bold=True)
    else:
        txt(f, (x + w / 2, y + h * 0.3), l1, S_LAB, bold=True)
        txt(f, (x + w / 2, y + h * 0.72), l2, S_LAB + 1, bold=True)


def table(f, qno, name, rows):
    """'Question #N | Name / Calculate / Area 1 End= / Volume= / Perimeter=' with empty answer cells."""
    c1, c2, rh = 190, 220, 36
    x, y = (W3 - c1 - c2) / 2, TY
    lines = [("Question #%d" % qno, name), ("Calculate", None)] + [(r, None) for r in rows]
    for i, (a, b) in enumerate(lines):
        yy = y + rh * i
        rect(f, x, yy, c1, rh, lw=1.6)
        rect(f, x + c1, yy, c2, rh, lw=1.6)
        if i == 0:
            txt(f, (x + 10, yy + rh / 2), a, S_TAB - 1, anchor="start", bold=True)
            txt(f, (x + c1 + c2 / 2, yy + rh / 2), b, S_TAB, bold=True)
            tw = len(b) * S_TAB * 0.6
            f.line((x + c1 + c2 / 2 - tw / 2, yy + rh / 2 + 11), (x + c1 + c2 / 2 + tw / 2, yy + rh / 2 + 11), w=1.4)
        elif i == 1:
            txt(f, (x + 10, yy + rh / 2), a, S_TAB + 1, anchor="start", bold=True)
        else:
            txt(f, (x + c1 - 8, yy + rh / 2), a, S_TAB - 1, anchor="end", bold=True)
    return y + rh * len(lines)


def lead(f, tip, frm):
    f.leader([tip, frm])


def sheet(nrows, extra=0):
    return Fig((0, 0, W3, TY + 36 * nrows + 16 + extra), W3)


def q44():
    """Cube 49 x 49 x 49."""
    f = sheet(5)
    A, B, C, D = (90, 95), (255, 95), (255, 260), (90, 260)
    v = (55, -45)
    Av, Bv, Cv = (A[0] + v[0], A[1] + v[1]), (B[0] + v[0], B[1] + v[1]), (C[0] + v[0], C[1] + v[1])
    f.poly([A, B, C, D], closed=True)
    f.poly([A, Av, Bv, B])
    f.poly([Bv, Cv, C])
    tag(f, 375, 92, 150, 40, "Height  49")
    lead(f, (318, 132), (373, 112))
    tag(f, 375, 222, 150, 40, "Width  49")
    lead(f, (287, 240), (373, 242))
    tag(f, 15, 272, 150, 38, "Length  49")
    lead(f, (99, 256), (80, 272))
    table(f, 1, "Cube", ["Area 1 End=", "Volume=", "Perimeter="])
    return f


def q45():
    """Rectangular box: Length 41 (long front edge), Height 40, Width 16 (end face)."""
    f = sheet(5)
    A, B, C, D = (60, 100), (330, 100), (330, 215), (60, 215)
    v = (45, -45)
    Av, Bv, Cv = (A[0] + v[0], A[1] + v[1]), (B[0] + v[0], B[1] + v[1]), (C[0] + v[0], C[1] + v[1])
    f.poly([A, B, C, D], closed=True)
    f.poly([A, Av, Bv, B])
    f.poly([Bv, Cv, C])
    tag(f, 425, 92, 150, 40, "Height  40")
    lead(f, (382, 122), (423, 112))
    tag(f, 425, 222, 150, 40, "Width  16")
    lead(f, (356, 194), (430, 222))
    tag(f, 40, 236, 110, 66, "Length", "41")
    lead(f, (128, 219), (108, 236))
    table(f, 2, "Rectangle", ["Area 1 End=", "Volume=", "Perimeter="])
    return f


def q46():
    """Triangular prism: end triangle Width 14 (base) x Vertical Height 20, Length 8."""
    f = sheet(4)
    P1, P2, P3 = (230, 280), (360, 280), (305, 120)          # front end: base left, base right, apex
    v = (-110, -70)                                           # length recedes up-left
    Q1, Q3 = (P1[0] + v[0], P1[1] + v[1]), (P3[0] + v[0], P3[1] + v[1])
    f.poly([P1, P2, P3], closed=True)
    f.poly([P1, Q1, Q3, P3])
    tag(f, 388, 92, 195, 64, "Vertical  Height", "20")
    lead(f, (320, 133), (386, 122))
    tag(f, 400, 222, 110, 64, "Width", "14")
    lead(f, (332, 273), (398, 258))
    tag(f, 15, 236, 100, 64, "Length", "8")
    lead(f, (170, 244), (117, 262))
    table(f, 3, "Triangle", ["Area 1 End=", "Volume="])
    return f


def q47():
    """Cylinder: Diameter 50, Length 44."""
    f = sheet(5)
    cx0, cx1, cy, R, rx = 95, 400, 150, 90, 34
    f.ellipse_arc((cx0, cy), rx, R, 90, 270)                 # far end: only the visible half
    f.ellipse((cx1, cy), rx, R)
    f.line((cx0, cy - R), (cx1, cy - R))
    f.line((cx0, cy + R), (cx1, cy + R))
    tag(f, 40, 262, 150, 42, "Length  44")
    lead(f, (235, cy + R + 4), (150, 262))
    tag(f, 425, 252, 160, 52, "Diameter", "50")
    lead(f, (cx1 + rx * 0.72 + 3, cy + R * 0.69 + 3), (440, 252))
    table(f, 4, "Circle", ["Area 1 End=", "Volume=", "Perimeter="])
    return f


def q48():
    """Trapezoid prism: Top of Trapezoid 33, Bottom of Trapezoid 17, Vertical Height 14, Length 28.
    The printed note (in a cloud) says all dimensions and answers are in inches, 3 decimal places."""
    f = sheet(4, extra=122)
    T1, T2 = (150, 140), (350, 140)                          # front end: top edge (33)
    B1, B2 = (210, 240), (295, 240)                          # bottom edge (17)
    v = (-75, -55)                                           # length recedes up-left
    U1, U2, L1 = (T1[0] + v[0], T1[1] + v[1]), (T2[0] + v[0], T2[1] + v[1]), (B1[0] + v[0], B1[1] + v[1])
    f.poly([T1, T2, B2, B1], closed=True)
    f.poly([B1, L1, U1, U2, T2])
    f.line(U1, T1)
    tag(f, 40, 4, 210, 62, "Top of Trapezoid", "33")
    lead(f, (190, 90), (160, 66))
    tag(f, 388, 140, 195, 62, "Vertical  Height", "14")
    lead(f, (330, 186), (386, 171))
    tag(f, 330, 248, 230, 62, "Bottom of Trapezoid", "17")
    lead(f, (272, 245), (340, 248))
    tag(f, 15, 238, 100, 62, "Length", "28")
    lead(f, (168, 218), (117, 258))
    y = table(f, 5, "Trapezoid", ["Area 1 End=", "Volume="]) + 16
    x, w, h, r = 95, 410, 106, 24                            # printed note, drawn as a rounded box
    f._path(f"M{x + r},{y} H{x + w - r} Q{x + w},{y} {x + w},{y + r} V{y + h - r} Q{x + w},{y + h} {x + w - r},{y + h}"
            f" H{x + r} Q{x},{y + h} {x},{y + h - r} V{y + r} Q{x},{y} {x + r},{y} Z", 1.8)
    for i, s in enumerate(["All questions are in inch's!", "All answers in inch's to 3", "Decimal places"]):
        txt(f, (x + 20, y + 26 + 28 * i), s, 19, anchor="start", bold=True)
    return f


FIGS = {"y1w5h-q38": q38, "y1w5h-q39": q39, "y1w5h-q40": q40, "y1w5h-q41": q41, "y1w5h-q42": q42,
        "y1w5h-q43": q43, "y1w5h-q44": q44, "y1w5h-q45": q45, "y1w5h-q46": q46, "y1w5h-q47": q47,
        "y1w5h-q48": q48}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    want = sys.argv[1:] or list(FIGS)
    for name in want:
        (OUT / f"{name}.svg").write_text(FIGS[name]().svg(), encoding="utf-8")
        print(name)


if __name__ == "__main__":
    main()
