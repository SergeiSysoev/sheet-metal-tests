"""Drawings for the "Friday test 11/20" practice questions (src "F20") written to cover the instructor's review class
on 11/19. Our own drawings; every size is the one used in the question.
  f20-q81  triangle 2'-0" x 3'-0" x 4'-0", sides not lettered (law of cosines, label it yourself)
  f20-q82  symmetrical shape, perimeter: each side of the centre line carries part of the sizes
  f20-q83  the symmetrical pattern of T90 No.57 (3", 4-1/4", 10-3/8", 5", 7-1/4", 150 and 135 deg), perimeter
Run: python3 tools/figures_f20.py"""
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from figures import Fig, t90_q57  # noqa: E402

OUT = pathlib.Path(__file__).resolve().parent.parent / "img"


def _off(p, q, d):
    """Segment p-q moved d (view units) along its left normal (screen coordinates, y down)."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy)
    nx, ny = dy / L, -dx / L
    return (p[0] + nx * d, p[1] + ny * d), (q[0] + nx * d, q[1] + ny * d)


def tri_unlabeled():
    """Base 3'-0" (36"), left side 2'-0" (24"), long side 4'-0" (48"); the obtuse corner is bottom left."""
    s = 10.0                                  # px per inch
    b, l, g = 36.0, 24.0, 48.0
    x = (l * l - g * g + b * b) / (2 * b)     # apex x from the left base corner (negative: leans out)
    y = math.sqrt(l * l - x * x)
    ox, oy = 170.0, 380.0
    PL, PR, PT = (ox, oy), (ox + b * s, oy), (ox + x * s, oy - y * s)
    f = Fig((0, 70, 640, 470), 600)
    f.poly([PL, PR, PT], closed=True)
    q1, q2 = _off(PR, PL, 42)                 # base, dimension below
    f.dim(PR, PL, q1, q2, "3'-0\"")
    q1, q2 = _off(PL, PT, 40)                 # short side, dimension outside (left)
    f.dim(PL, PT, q1, q2, "2'-0\"")
    q1, q2 = _off(PT, PR, 40)                 # long side, dimension outside (upper right)
    f.dim(PT, PR, q1, q2, "4'-0\"")
    return f


def sym_shape():
    """Symmetrical about the CL. Half outline (inches, from CL, up from the bottom):
    bottom 5 from CL, vertical 9, slant 5 (4 across, 3 up), vertical 6, top 18 overall."""
    s = 16.0
    cl, yb = 330.0, 420.0

    def P(xi, yi):
        return (cl + xi * s, yb - yi * s)
    half = [(5, 0), (5, 9), (9, 12), (9, 18)]
    right = [P(xx, yy) for xx, yy in half]
    left = [P(-xx, yy) for xx, yy in reversed(half)]
    f = Fig((0, 60, 660, 540), 600)
    f.poly(left + right, closed=True)
    f.centerline(P(0, -4.2), P(0, 19.2), pattern=(22 * f.u, 5 * f.u, 5 * f.u, 5 * f.u))
    f.text(P(0, -5.3), "CL", size=15)
    # top, overall 18" (above)
    f.dim(P(-9, 18), P(9, 18), P(-9, 21.0), P(9, 21.0), '18"', gap=6)
    # bottom, 5" from the CL to the right corner (below)
    f.dim(P(0, 0), P(5, 0), P(0, -2.2), P(5, -2.2), '5"', ext=(False, True))
    # right side: lower vertical 9"
    f.dim(P(5, 0), P(5, 9), P(12.2, 0), P(12.2, 9), '9"', gap=8)
    # left side: upper vertical 6"
    f.dim(P(-9, 12), P(-9, 18), P(-12.2, 12), P(-12.2, 18), '6"', gap=8)
    # left side: slant 5", dimensioned along the slant, outside (down-left)
    A, B = P(-9, 12), P(-5, 9)
    q1, q2 = _off(A, B, -38)
    f.dim(A, B, q1, q2, '5"')
    return f


FIGS = {"f20-q81": tri_unlabeled, "f20-q82": sym_shape, "f20-q83": t90_q57}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    names = sys.argv[1:] or list(FIGS)
    for name in names:
        fig = FIGS[name]()
        (OUT / f"{name}.svg").write_text(fig.svg(), encoding="utf-8")
        print(name)


if __name__ == "__main__":
    main()
