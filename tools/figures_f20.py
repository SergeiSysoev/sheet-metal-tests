#!/usr/bin/env python3
"""Clean SVG redraws for the SMY2W2 Friday Written test of 11/20/2026 (code F20), numbers 1-90.
The phone photos of the graded test are only the reference; they are not shipped.

Only the drawings of questions that were not already in the bank are redrawn here:
  No. 59, 60  field-measured offset by two diagonals (law of cosines)
  No. 61, 62  oblique triangle with three sides, find angles A, B, C (law of cosines)
Geometry is written in pixel coordinates of the reference crops (y down, straightened), so each
redraw keeps the printed proportions; the drawings are not to scale, exactly as printed.

    python3 tools/figures_f20.py              # write every figure into img/
    python3 tools/figures_f20.py f20-q59      # only these

Standard library only.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from figures import Fig, OUT, f2, vadd, vsub, unit, angle_of  # noqa: E402


# ---------------------------------------------------------------- local helpers
def diag_dim(f, a, b, off, label, side=+1, size=None, gap=10):
    """Dimension of the straight distance a-b, drawn parallel to it at distance `off` (model units).
    side=+1 puts the dimension line on the left of a->b as seen on screen, -1 on the right."""
    d = unit(vsub(b, a))
    n = (d[1] * side, -d[0] * side)
    f.dim(a, b, vadd(a, n, off), vadd(b, n, off), label, gap=gap, size=size)


def duct_end(f, face_x, y_top, y_bot, far_x, label=None, lpos=None, size=None):
    """Rectangular duct seen from the side: end face at face_x (solid), top and bottom lines,
    cut (break symbol) at far_x."""
    f.line((far_x, y_top), (face_x, y_top))
    f.line((far_x, y_bot), (face_x, y_bot))
    f.line((face_x, y_top), (face_x, y_bot))
    f.zbreak((far_x, y_top), (far_x, y_bot), 0.5, h=12, amp=12)
    if label:
        f.text(lpos, label, size=size)


def q_offset(d1, d2, labels, diag_labels, offs, lab_pos, box, width=640):
    f = Fig(box, width)
    fs = 18 * f.u
    far1, face1, t1, b1 = d1
    face2, far2, t2, b2 = d2
    duct_end(f, face1, t1, b1, far1)
    duct_end(f, face2, t2, b2, far2)
    f.text(lab_pos[0][0], labels[0], size=fs, anchor=lab_pos[0][1])
    f.text(lab_pos[1][0], labels[1], size=fs, anchor=lab_pos[1][1])
    P, T2, B2 = (face1, b1), (face2, t2), (face2, b2)
    ly = box[1] + 42
    f.dim((face1, t1), (face2, t2), (face1, ly), (face2, ly), "LENGTH", gap=10, size=fs)
    ox = face2 + 0.6 * (far2 - face2)
    f.line((lab_pos[2], b1), (ox + 28, b1), thin=True)                     # base line through P
    f.dim((ox, b2), (ox, b1), (ox, b2), (ox, b1), "OFFSET", ext=(False, False),
          tpos=(ox, b2 + 0.52 * (b1 - b2)), size=fs)
    diag_dim(f, P, T2, offs[0], diag_labels[0], +1, size=fs)
    diag_dim(f, P, B2, offs[1], diag_labels[1], -1, size=fs)
    return f


def f20_q59():
    """16"x10" -> 16"x10"; diagonals from P: 7'-4 3/4" (to the top corner), 6'-6 3/16" (to the bottom)."""
    return q_offset(d1=(62, 280, 698, 860), d2=(975, 1215, 205, 372),
                    labels=('16"x10"', '16"x10"'),
                    diag_labels=("7'-4 3/4\"", "6'-6 3/16\""), offs=(92, 64),
                    lab_pos=(((150, 742), "middle"), ((1092, 246), "middle"), 460),
                    box=(10, 15, 1290, 935))


def f20_q60():
    """16"x10" -> 20"x14"; diagonals from P: 6'-9 1/8" (to the top corner), 5'-9 9/16" (to the bottom)."""
    return q_offset(d1=(205, 432, 665, 848), d2=(1128, 1360, 218, 450),
                    labels=('16"x10"', '20"x14"'),
                    diag_labels=("6'-9 1/8\"", "5'-9 9/16\""), offs=(98, 90),
                    lab_pos=(((182, 777), "end"), ((1376, 292), "start"), 455),
                    box=(0, 15, 1590, 975))


def oblique(L, R, T, side_labels, angle_labels, offs, base_y, r, lab_mid=None, box=None, width=600):
    """Oblique triangle L (left), R (right), T (top) with the three sides dimensioned and the three
    angles marked. side_labels = (L-T, T-R, L-R); angle_labels = (at L, at R, at T); r = arc radii."""
    f = Fig(box, width)
    fs = 18 * f.u
    f.poly([L, T, R], closed=True)
    diag_dim(f, L, T, offs[0], side_labels[0], +1, size=fs)      # outside, upper left
    diag_dim(f, T, R, offs[1], side_labels[1], +1, size=fs)      # outside, upper right
    f.dim(L, R, (L[0], base_y), (R[0], base_y), side_labels[2], gap=12, size=fs)
    aLT, aLR = angle_of(vsub(T, L)), angle_of(vsub(R, L))
    aRT, aRL = angle_of(vsub(T, R)), angle_of(vsub(L, R))
    aTL, aTR = angle_of(vsub(L, T)), angle_of(vsub(R, T))
    if aRT < 0:
        aRT += 360
    f.angle(L, r[0], aLR, aLT, angle_labels[0], size=fs)
    f.angle(R, r[1], aRL, aRT, angle_labels[1], size=fs)
    f.angle(T, r[2], aTL, aTR, angle_labels[2], size=fs)
    return f


def f20_q61():
    """Sides 4'-2 3/4" (left), 7'-2 1/2" (right), 8'-1 1/4" (base); A at the top, B right, C left."""
    return oblique(L=(558, 650), R=(1570, 650), T=(866, 232),
                   side_labels=("4'-2 3/4\"", "7'-2 1/2\"", "8'-1 1/4\""),
                   angle_labels=("C", "B", "A"), offs=(90, 92), base_y=738, r=(225, 402, 158),
                   box=(420, 110, 1690, 790), width=620)


def f20_q62():
    """Sides 95" (left), 67.7" (right), 121.5" (base); A at the left, B right, C at the top."""
    return oblique(L=(140, 530), R=(963, 530), T=(652, 118),
                   side_labels=('95"', '67.7"', '121.5"'),
                   angle_labels=("A", "B", "C"), offs=(92, 86), base_y=612, r=(328, 235, 165),
                   box=(20, 15, 1110, 650), width=600)


FIGS = {
    "f20-q59": f20_q59,
    "f20-q60": f20_q60,
    "f20-q61": f20_q61,
    "f20-q62": f20_q62,
}


def main(names):
    OUT.mkdir(parents=True, exist_ok=True)
    for name in names or FIGS:
        fig = FIGS[name]()
        (OUT / f"{name}.svg").write_text(fig.svg(), encoding="utf-8")
        print(f"{name}.svg  viewBox {f2(fig.W)} x {f2(fig.H)}")


if __name__ == "__main__":
    main(sys.argv[1:])
