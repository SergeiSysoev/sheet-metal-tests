"""Drawings for the review-class practice set (src "CLS"): the two law-of-cosines examples of the course
formula sheets, page 12 (000 SM Formula Sheets rev 5.13.26). Our own drawings, same numbers as the sheet.
Run: python3 tools/figures_cls.py"""
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from figures import Fig  # noqa: E402

OUT = pathlib.Path(__file__).resolve().parent.parent / "img"


def tri_example():
    """Triangle A = 5'-11 1/2", B = 3'-8", C = 3'-0 1/2"; angle letters opposite their sides."""
    s = 7.0                                   # px per inch
    a, b, c = 71.5, 44.0, 36.5
    Cang = math.acos((a * a + b * b - c * c) / (2 * a * b))
    PL = (60.0, 360.0)                        # vertex with angle C (between sides A and B)
    PR = (PL[0] + b * s, PL[1])               # vertex with angle A (between B and C)
    PT = (PL[0] + a * s * math.cos(Cang), PL[1] - a * s * math.sin(Cang))   # vertex with angle B
    f = Fig((0, 70, 660, 430), 600)
    f.poly([PL, PR, PT], closed=True)

    def off(p, q, d):
        dx, dy = q[0] - p[0], q[1] - p[1]
        L = math.hypot(dx, dy)
        nx, ny = dy / L, -dx / L                # left normal in screen coords
        return (p[0] + nx * d, p[1] + ny * d), (q[0] + nx * d, q[1] + ny * d)

    q1, q2 = off(PL, PT, 40)
    f.dim(PL, PT, q1, q2, "5'-11 1/2\"  A")
    q1, q2 = off(PR, PL, 40)
    f.dim(PR, PL, q1, q2, "3'-8\"  B")
    q1, q2 = off(PT, PR, 64)                  # far enough out that the label clears side C
    f.dim(PT, PR, q1, q2, "3'-0 1/2\"  C")
    f.text((PR[0] - 30, PR[1] - 22), "A", size=20, bold=True)
    f.text((PT[0] - 52, PT[1] + 50), "B", size=20, bold=True)
    f.text((PL[0] + 70, PL[1] - 12), "C", size=20, bold=True)
    return f


def offset_example():
    """Duct offset (plan): 18"x20" to 24"x20"; A = 7'-5 5/8" and B = 6'-5 7/8" from the corner P to the ends of the
    24" side C; OFFSET (vertical) and OFFSET LENGTH (horizontal) are the unknowns."""
    s = 4.6
    ox, oy = 150.0, 420.0                     # P, the corner of the 18"x20"
    def P(x, y):
        return (ox + x * s, oy - y * s)
    xl = 72.2728
    f = Fig((0, 60, 860, 520), 600)
    # 18"x20" duct, coming from the left
    f.poly([P(-30, 0), P(0, 0), P(0, 18), P(-30, 18)])
    f.text(P(-17, 6), '18"x20"', size=17)
    # 24"x20" duct, going to the right; its 24" side is C
    f.poly([P(xl + 40, 29), P(xl, 29), P(xl, 53), P(xl + 40, 53)])
    f.text(P(xl + 22, 41), '24"x20"', size=17)
    f.text(P(xl - 4, 41), "C", size=18, bold=True, anchor="end")
    # triangle sides A and B (dashed), as the formula sheet draws them
    f.line(P(0, 0), P(xl, 53), dash=(10, 7))
    f.line(P(0, 0), P(xl, 29), dash=(10, 7))
    f.line(P(0, 0), P(xl, 0), dash=(10, 7), thin=True)
    f.line(P(xl, 0), P(xl, 29), dash=(10, 7), thin=True)
    # A and B dimensions, offset outward
    def off(p, q, d):
        dx, dy = q[0] - p[0], q[1] - p[1]
        L = math.hypot(dx, dy)
        nx, ny = dy / L, -dx / L
        return (p[0] + nx * d, p[1] + ny * d), (q[0] + nx * d, q[1] + ny * d)
    a0, a1 = P(0, 0), P(xl, 53)
    q1, q2 = off(a0, a1, 46)
    f.dim(a0, a1, q1, q2, "7'-5 5/8\"  A")
    b0, b1 = P(xl, 29), P(0, 0)
    q1, q2 = off(b0, b1, 50)
    f.dim(b0, b1, q1, q2, "6'-5 7/8\"  B")
    # unknowns
    f.dim(P(xl, 0), P(xl + 40, 29), P(xl + 50, 0), P(xl + 50, 29))   # lower extension continues the base line
    f.text(P(xl + 53, 14.5), "OFFSET", size=17, anchor="start")
    f.dim(P(0, 0), P(xl, 0), P(0, -16), P(xl, -16), "OFFSET LENGTH")
    return f


FIGS = {"cls-q01": tri_example, "cls-q03": offset_example}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in FIGS.items():
        fig = fn()
        (OUT / f"{name}.svg").write_text(fig.svg(), encoding="utf-8")
        print(name)


if __name__ == "__main__":
    main()
