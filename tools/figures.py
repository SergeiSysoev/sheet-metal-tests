#!/usr/bin/env python3
"""Clean SVG redraws of the exam figures used by the sheet-metal test app.

Sources (photos / scans are NOT shipped; they are only the reference):
  T90 "Welding & Layout"  — phone photos, prior-work/t90/src/pNN.jpg (crop boxes in prior-work/t90/crops.py)
  SMY2W2 "Triangulation"  — images embedded in prior-work/smy2w2/out.pdf
  SMY2W2 "Monday Written" — images embedded in msg_993_Monday_Written_SMY2W2_Answers.pdf (Local 66 archive)

Every figure is one function. Geometry is written in the coordinates of the
reference image (pixels of the crop, y pointing down) or in inches where the
original is drawn to scale, so the redraw keeps the original proportions.
`Fig` maps those model coordinates to a viewBox; line widths, arrowheads and
text sizes are given in viewBox units so they stay readable on a phone.

    python3 tools/figures.py               # write every figure into img/
    python3 tools/figures.py t90-q40 tri-q17   # only these

Standard library only.
"""
import html
import math
import pathlib
import random
import sys

OUT = pathlib.Path(__file__).resolve().parent.parent / "img"
INK = "#111"
FONT = "Arial, Helvetica, sans-serif"

# Base sizes in viewBox units for a ~600-unit-wide figure (u = 1).
LW = 2.2    # object (visible) line
TW = 1.15   # thin line: dimension, extension, leader, centre line
FS = 17     # label font size
AL = 13     # arrowhead length
AW = 3.5    # arrowhead half width
GAP = 4     # gap between an object and its extension line
OVR = 7     # extension line overshoot past the dimension line

# Arial advance widths (1/1000 em) for text-width estimates.
_CW = {" ": 278, '"': 355, "'": 191, "-": 333, ".": 278, "/": 278, "?": 556, "°": 400,
       "Ø": 778, "(": 333, ")": 333, ":": 278, "½": 834}
_CW.update({c: 556 for c in "0123456789"})
_CW.update(dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                    [667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833,
                     722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611])))
_CW.update(dict(zip("abcdefghijklmnopqrstuvwxyz",
                    [556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833,
                     556, 556, 556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500])))


def text_w(s, size, bold=False):
    w = sum(_CW.get(c, 600) for c in s) / 1000.0 * size
    return w * (1.08 if bold else 1.0)


# ---------------------------------------------------------------- vector helpers
def vadd(a, b, s=1.0):
    return (a[0] + b[0] * s, a[1] + b[1] * s)


def vsub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def vmul(a, s):
    return (a[0] * s, a[1] * s)


def vlen(a):
    return math.hypot(a[0], a[1])


def unit(a):
    n = vlen(a)
    return (a[0] / n, a[1] / n)


def dist(a, b):
    return vlen(vsub(a, b))


def mid(a, b, t=0.5):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def lnorm(d):
    """Left-hand normal on screen (y down): (1,0) -> (0,-1), i.e. 'up' for a left-to-right line."""
    return (d[1], -d[0])


def pol(c, r, a_deg):
    a = math.radians(a_deg)
    return (c[0] + r * math.cos(a), c[1] + r * math.sin(a))


def angle_of(v):
    return math.degrees(math.atan2(v[1], v[0]))


def f2(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


# ---------------------------------------------------------------- drawing class
class Fig:
    """Model coordinates (y down) -> viewBox. `box` = model area shown (x0, y0, x1, y1)."""

    def __init__(self, box, width=600, u=None):
        x0, y0, x1, y1 = box
        self.x0, self.y0 = x0, y0
        self.k = width / float(x1 - x0)
        self.W = float(width)
        self.H = (y1 - y0) * self.k
        u = max(1.0, width / 600.0) if u is None else u   # never shrink text below the base size
        self.u = u
        self.lw, self.tw, self.fs = LW * u, TW * u, FS * u
        self.al, self.aw, self.gap, self.ovr = AL * u, AW * u, GAP * u, OVR * u
        self.el = []

    # -- model -> view
    def P(self, p):
        return ((p[0] - self.x0) * self.k, (p[1] - self.y0) * self.k)

    # -- raw view-space primitives
    def _stroke(self, w, dash):
        s = f' fill="none" stroke="{INK}" stroke-width="{f2(w)}"'
        if dash:
            s += f' stroke-dasharray="{" ".join(f2(x) for x in dash)}"'
        return s

    def _line(self, a, b, w, dash=None, cap="butt"):
        self.el.append(f'<line x1="{f2(a[0])}" y1="{f2(a[1])}" x2="{f2(b[0])}" y2="{f2(b[1])}"'
                       f'{self._stroke(w, dash)} stroke-linecap="{cap}"/>')

    def _poly(self, pts, w, closed=False, dash=None, fill=None, join="miter"):
        tag = "polygon" if closed else "polyline"
        p = " ".join(f"{f2(x)},{f2(y)}" for x, y in pts)
        st = self._stroke(w, dash)
        if fill:
            st = st.replace('fill="none"', f'fill="{fill}"')
        self.el.append(f'<{tag} points="{p}"{st} stroke-linejoin="{join}"/>')

    def _path(self, d, w, dash=None, fill=None):
        st = self._stroke(w, dash)
        if fill:
            st = st.replace('fill="none"', f'fill="{fill}"')
        self.el.append(f'<path d="{d}"{st} stroke-linejoin="round" stroke-linecap="round"/>')

    def _arc(self, C, R, a0, a1, w, dash=None):
        p0, p1 = pol(C, R, a0), pol(C, R, a1)
        large = 1 if abs(a1 - a0) > 180 else 0
        sweep = 1 if a1 > a0 else 0
        self.el.append(f'<path d="M{f2(p0[0])},{f2(p0[1])} A{f2(R)},{f2(R)} 0 {large} {sweep} '
                       f'{f2(p1[0])},{f2(p1[1])}"{self._stroke(w, dash)}/>')

    def _arrow(self, tip, d, al=None, aw=None):
        al = self.al if al is None else al
        aw = self.aw if aw is None else aw
        d = unit(d)
        n = (-d[1], d[0])
        b = vadd(tip, d, -al)
        pts = [tip, vadd(b, n, aw), vadd(b, n, -aw)]
        self.el.append('<polygon points="' + " ".join(f"{f2(x)},{f2(y)}" for x, y in pts)
                       + f'" fill="{INK}" stroke="none"/>')

    def _text(self, c, s, size=None, anchor="middle", bold=False, rot=None):
        size = size or self.fs
        x, y = c
        yb = y + 0.355 * size  # vertical centring on cap height
        tr = f' transform="rotate({f2(rot)} {f2(x)} {f2(y)})"' if rot else ""
        wt = ' font-weight="bold"' if bold else ""
        self.el.append(f'<text x="{f2(x)}" y="{f2(yb)}" font-size="{f2(size)}" text-anchor="{anchor}"'
                       f'{wt} fill="{INK}"{tr}>{html.escape(s, quote=False)}</text>')

    def _half_break(self, label, size, d, bold=False):
        """Half length of the gap a centred label cuts out of a line with direction d (view)."""
        hx = text_w(label, size, bold) / 2 + 0.32 * size
        hy = 0.36 * size + 0.32 * size
        cand = []
        if abs(d[0]) > 1e-6:
            cand.append(hx / abs(d[0]))
        if abs(d[1]) > 1e-6:
            cand.append(hy / abs(d[1]))
        return min(cand)

    # -- public, model coordinates
    def line(self, p, q, w=None, dash=None, thin=False):
        self._line(self.P(p), self.P(q), w or (self.tw if thin else self.lw), dash)

    def poly(self, pts, w=None, closed=False, dash=None, fill=None, thin=False, join="miter"):
        self._poly([self.P(p) for p in pts], w or (self.tw if thin else self.lw), closed, dash, fill, join)

    def arc(self, c, r, a0, a1, w=None, dash=None, thin=False):
        self._arc(self.P(c), r * self.k, a0, a1, w or (self.tw if thin else self.lw), dash)

    def ellipse_arc(self, c, rx, ry, a0, a1, w=None):
        """Elliptical arc (parametric angles in degrees, screen sense)."""
        C = self.P(c)
        RX, RY = rx * self.k, ry * self.k
        p0 = (C[0] + RX * math.cos(math.radians(a0)), C[1] + RY * math.sin(math.radians(a0)))
        p1 = (C[0] + RX * math.cos(math.radians(a1)), C[1] + RY * math.sin(math.radians(a1)))
        large = 1 if abs(a1 - a0) > 180 else 0
        sweep = 1 if a1 > a0 else 0
        self._path(f"M{f2(p0[0])},{f2(p0[1])} A{f2(RX)},{f2(RY)} 0 {large} {sweep} {f2(p1[0])},{f2(p1[1])}",
                   w or self.lw)

    def ellipse(self, c, rx, ry, w=None):
        C = self.P(c)
        self.el.append(f'<ellipse cx="{f2(C[0])}" cy="{f2(C[1])}" rx="{f2(rx * self.k)}" ry="{f2(ry * self.k)}"'
                       f'{self._stroke(w or self.lw, None)}/>')

    def text(self, p, s, size=None, anchor="middle", bold=False, rot=None):
        self._text(self.P(p), s, size, anchor, bold, rot)

    def arrow(self, tip, toward_tip_from):
        T = self.P(tip)
        self._arrow(T, vsub(T, self.P(toward_tip_from)))

    def dim(self, p1, p2, q1, q2, label=None, *, arrows="in", tpos=None, tbreak=True,
            ext=(True, True), size=None, bold=False, tail=None, gap=None, ovr=None):
        """Dimension: extension lines p->q, dimension line q1-q2, arrowheads, label.

        arrows="in": arrowheads inside pointing out to the extension lines (line broken by the label);
        arrows="out": short tails outside with arrowheads pointing in (for narrow spaces)."""
        P1, P2, Q1, Q2 = (self.P(p) for p in (p1, p2, q1, q2))
        gap = self.gap if gap is None else gap
        ovr = self.ovr if ovr is None else ovr
        for Pp, Qq, on in ((P1, Q1, ext[0]), (P2, Q2, ext[1])):
            L = dist(Pp, Qq)
            if on and L > gap + 1:
                e = unit(vsub(Qq, Pp))
                self._line(vadd(Pp, e, gap), vadd(Qq, e, ovr), self.tw)
        d = unit(vsub(Q2, Q1))
        size = size or self.fs
        T = self.P(tpos) if tpos is not None else mid(Q1, Q2)
        if arrows == "in":
            if label is not None and tbreak:
                tc = dot(vsub(T, Q1), d)
                h = self._half_break(label, size, d, bold)
                self._line(Q1, vadd(Q1, d, tc - h), self.tw)
                self._line(vadd(Q1, d, tc + h), Q2, self.tw)
            else:
                self._line(Q1, Q2, self.tw)
            self._arrow(Q1, vmul(d, -1))
            self._arrow(Q2, d)
        else:
            tl = tail or 2.2 * self.al
            self._line(vadd(Q1, d, -tl), Q1, self.tw)
            self._arrow(Q1, d)
            self._line(Q2, vadd(Q2, d, tl), self.tw)
            self._arrow(Q2, vmul(d, -1))
        if label is not None:
            self._text(T, label, size, bold=bold)

    def angle(self, c, r, a0, a1, label=None, *, arrows="in", ends=(True, True), tpos=None,
              tbreak=True, size=None, tail=None, bold=False, al=None):
        """Angle dimension arc centred at c, radius r (model), from a0 to a1 degrees (screen sense)."""
        if al is not None:                       # smaller arrowheads for a short arc
            keep = (self.al, self.aw)
            self.al, self.aw = al, al * AW / AL
            try:
                return self.angle(c, r, a0, a1, label, arrows=arrows, ends=ends, tpos=tpos,
                                  tbreak=tbreak, size=size, tail=tail, bold=bold)
            finally:
                self.al, self.aw = keep
        C = self.P(c)
        R = r * self.k
        s = 1 if a1 >= a0 else -1
        size = size or self.fs
        da = math.degrees(self.al / R)
        am = (a0 + a1) / 2.0
        if tpos is not None:
            T = self.P(tpos)
            am = angle_of(vsub(T, C))
            # keep am inside the a0..a1 range when angles wrap
            while (am - a0) * s < 0:
                am += 360 * s
            while (am - a1) * s > 0:
                am -= 360 * s
        else:
            T = pol(C, R, am)

        def pt(a):
            return pol(C, R, a)

        if arrows == "in":
            segs = [(a0, a1)]
            if label is not None and tbreak:
                tang = (-math.sin(math.radians(am)), math.cos(math.radians(am)))
                hg = math.degrees(self._half_break(label, size, tang, bold) / R)
                segs = [(a0, am - s * hg), (am + s * hg, a1)]
            for b0, b1 in segs:
                if (b1 - b0) * s > 0:
                    self._arc(C, R, b0, b1, self.tw)
            if ends[0]:
                self._arrow(pt(a0), vsub(pt(a0), pt(a0 + s * da)))
            if ends[1]:
                self._arrow(pt(a1), vsub(pt(a1), pt(a1 - s * da)))
        else:
            tl = math.degrees((tail or 2.4 * self.al) / R)
            self._arc(C, R, a0 - s * tl, a0, self.tw)
            self._arrow(pt(a0), vsub(pt(a0), pt(a0 - s * da)))
            self._arc(C, R, a1, a1 + s * tl, self.tw)
            self._arrow(pt(a1), vsub(pt(a1), pt(a1 + s * da)))
        if label is not None:
            self._text(T, label, size, bold=bold)

    def leader(self, pts, label=None, tpos=None, anchor="start", size=None, arrow=True):
        V = [self.P(p) for p in pts]
        self._poly(V, self.tw)
        if arrow:
            self._arrow(V[0], vsub(V[0], V[1]))
        if label is not None:
            self._text(self.P(tpos), label, size, anchor)

    def rt(self, c, a, b, s=None):
        """Right-angle mark at corner c, legs toward points a and b; s = size in view units."""
        C = self.P(c)
        s = s or 11 * self.u
        e1, e2 = unit(vsub(self.P(a), C)), unit(vsub(self.P(b), C))
        self._poly([vadd(C, e1, s), vadd(vadd(C, e1, s), e2, s), vadd(C, e2, s)], self.tw)

    def zbreak(self, p, q, t=0.5, h=None, amp=None, w=None):
        """Straight line p-q with a Z-shaped break symbol at fraction t."""
        A, B = self.P(p), self.P(q)
        d = unit(vsub(B, A))
        n = (-d[1], d[0])
        m = mid(A, B, t)
        h = h or 11 * self.u
        amp = amp or 10 * self.u
        pts = [A, vadd(m, d, -h), vadd(vadd(m, d, -h / 3), n, amp), vadd(vadd(m, d, h / 3), n, -amp),
               vadd(m, d, h), B]
        self._poly(pts, w or self.lw)

    def hook(self, p, out, body, s=None):
        """Small connection hook at a duct end: leaves p along `out`, curls toward `body`."""
        A = self.P(p)
        s = s or 8 * self.u
        o, b = unit(out), unit(body)
        p1 = vadd(A, o, 0.45 * s)
        c = vadd(A, o, s)
        e = vadd(vadd(A, o, 0.95 * s), b, 0.6 * s)
        self._path(f"M{f2(A[0])},{f2(A[1])} L{f2(p1[0])},{f2(p1[1])} Q{f2(c[0])},{f2(c[1])} {f2(e[0])},{f2(e[1])}",
                   self.lw * 0.75)

    def centerline(self, p, q, centers=(), long=None, short=None, g=None, pattern=None):
        """Thin chain line p-q. With `centers` (model points on the line) a short dash is centred on
        each of them; otherwise a regular long-gap-short-gap pattern is used."""
        A, B = self.P(p), self.P(q)
        L = dist(A, B)
        d = unit(vsub(B, A))
        long = long or 26 * self.u
        short = short or 7 * self.u
        g = g or 5 * self.u
        if not centers:
            pat = pattern or (long, g, short, g)
            self._line(A, B, self.tw, dash=pat)
            return
        cs = sorted(dot(vsub(self.P(c), A), d) for c in centers)
        segs, zones = [], []
        for c in cs:
            segs.append((c - short / 2, c + short / 2))
            zones.append((c - short / 2 - g, c + short / 2 + g))
        free, start = [], 0.0
        for z0, z1 in zones:
            free.append((start, z0))
            start = z1
        free.append((start, L))
        for f0, f1 in free:
            span = f1 - f0
            if span <= 0:
                continue
            n = max(1, int(round((span + g + short + g) / (long + g + short + g))))
            ll = (span - (n - 1) * (2 * g + short)) / n
            x = f0
            for i in range(n):
                segs.append((x, x + ll))
                x += ll
                if i < n - 1:
                    segs.append((x + g, x + g + short))
                    x += 2 * g + short
        for s0, s1 in segs:
            s0, s1 = max(0.0, s0), min(L, s1)
            if s1 > s0:
                self._line(vadd(A, d, s0), vadd(A, d, s1), self.tw)

    def concrete(self, poly, seed=3, n_tri=30, n_dot=110, tri=None, margin=None):
        """Concrete section symbol: small triangles and dots scattered inside polygon (model pts)."""
        V = [self.P(p) for p in poly]
        rnd = random.Random(seed)
        tri = tri or 5.2 * self.u
        margin = margin or 3.0 * self.u
        xs, ys = [p[0] for p in V], [p[1] for p in V]

        def inside(x, y):
            c = False
            for i in range(len(V)):
                (x1, y1), (x2, y2) = V[i], V[(i + 1) % len(V)]
                if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
                    c = not c
            return c

        def clear(x, y, r):
            for i in range(len(V)):
                a, b = V[i], V[(i + 1) % len(V)]
                ab = vsub(b, a)
                t = max(0.0, min(1.0, dot(vsub((x, y), a), ab) / max(dot(ab, ab), 1e-9)))
                if dist((x, y), vadd(a, ab, t)) < r:
                    return False
            return True

        def sample(r):
            for _ in range(2000):
                x, y = rnd.uniform(min(xs), max(xs)), rnd.uniform(min(ys), max(ys))
                if inside(x, y) and clear(x, y, r):
                    return x, y
            return None

        for _ in range(n_tri):
            p = sample(tri * 0.75 + margin)
            if not p:
                continue
            a0 = rnd.uniform(0, 120)
            s = tri * rnd.uniform(0.75, 1.15)
            pts = [pol(p, s * 0.6, a0 + k * 120) for k in range(3)]
            self._poly(pts, self.tw * 0.9, closed=True)
        for _ in range(n_dot):
            p = sample(margin)
            if not p:
                continue
            self.el.append(f'<circle cx="{f2(p[0])}" cy="{f2(p[1])}" r="{f2(0.85 * self.u)}" fill="{INK}"/>')

    def svg(self):
        W, H = f2(self.W), f2(self.H)
        return ("\n".join([
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="{FONT}">',
            f'<rect x="0" y="0" width="{W}" height="{H}" fill="#fff"/>',
            *self.el,
            "</svg>"]) + "\n")


# ======================================================================= T90 figures
def t90_q25():
    """Fillet weld symbol: triangle (perpendicular leg on the left) above a dashed reference line."""
    f = Fig((0, 0, 600, 180), 600)
    y = 160
    xl, xr, top = 212, 356, 26
    f.poly([(xl, y), (xl, top), (xr, y)], w=5, closed=True)
    f.line((14, y), (xl - 8, y), w=4.5, dash=(20, 16))
    f.line((xr + 9, y), (590, y), w=4.5, dash=(20, 16))
    return f


def t90_q27():
    """Square-groove weld symbol: two parallel perpendicular lines above a dashed reference line."""
    f = Fig((0, 0, 600, 230), 600)
    y = 170
    x1, x2, top = 240, 309, 40
    f.line((14, y), (590, y), w=4.5, dash=(20, 16))   # dashed reference line runs on under the symbol
    f.line((x1, top), (x1, y + 2), w=6)
    f.line((x2, top), (x2, y + 2), w=6)
    return f


def t90_q40(ab=("FOB", "FOT")):
    """Plan + section of two ducts and four candidate transitions A-D (same figure as SMY1W5 No.24
    and SMY2W2 Monday No.24). `ab` = the labels written inside A and B; Monday No.76 has them swapped."""
    f = Fig((0, 0, 1080, 775), 1080, u=1.0)
    f.lw, f.tw, f.fs, f.al, f.aw, f.gap, f.ovr = 2.6, 1.5, 25.5, 15, 4.2, 5, 9
    s = 8.2                      # view units per inch
    yT, yB = 118.0, 118.0 + 19 * s
    big = 44
    flange = 5.0

    def strips(TL, TR, BL, BR):
        f.poly([TL, TR, (TR[0], TR[1] - flange), (TL[0], TL[1] - flange)], closed=True)
        f.poly([BL, BR, (BR[0], BR[1] + flange), (BL[0], BL[1] + flange)], closed=True)

    # ---- A
    xa = 50.0
    BL, BR, TL, TR = (xa, yB), (xa + 14 * s, yB), (xa + 8 * s, yT), (xa + 16 * s, yT)
    f.poly([BL, TL, TR, BR], closed=True)
    strips(TL, TR, BL, BR)
    f.dim((xa, yB + flange), (TL[0], yT - flange), (xa, yT - 32), (TL[0], yT - 32), '8"')
    f.text((TL[0] + 10, yT - 26), '8"x16"', anchor="start")
    xd = TR[0] + 30
    f.dim(TR, BR, (xd, yT), (xd, yB), "1'-7\"")
    f.text(((BL[0] + BR[0] + TL[0] + TR[0]) / 4, (yT + yB) / 2), ab[0])
    f.text(((BL[0] + BR[0]) / 2, yB + 28), '14"x20"')
    f.text((122, 48), "A", size=big, bold=True)

    # ---- B
    xb = 338.0
    BL, BR, TL, TR = (xb, yB), (xb + 14 * s, yB), (xb + 8 * s, yT), (xb + 16 * s, yT)
    f.poly([BL, TL, TR, BR], closed=True)
    strips(TL, TR, BL, BR)
    xd = xb - 32
    f.dim((TL[0] - 4, yT), BL, (xd, yT), (xd, yB), "1'-7\"")
    yd = yB + 26
    f.dim((TR[0], yT - flange), (BR[0], yB + flange), (TR[0], yd), (BR[0], yd), arrows="out", tail=26)
    f.text((TR[0] + 26 + 8, yd), '2"', anchor="start")
    f.text((BR[0] - 26 - 8, yd), '14"x20"', anchor="end")
    f.text(((TL[0] + TR[0]) / 2, yT - 26), '8"x16"')
    f.text(((BL[0] + BR[0] + TL[0] + TR[0]) / 4, (yT + yB) / 2), ab[1])
    f.text((410, 48), "B", size=big, bold=True)

    # ---- C and D
    def cd(xc, up, letter):
        BL, BR = (xc, yB), (xc + 20 * s, yB)
        TR, TL = (xc + 20 * s, yT), (xc + 4 * s, yT)
        f.poly([BL, TL, TR, BR], closed=True)
        f.rt(BR, TR, BL, 11)
        for p, o, b in ((TL, (-1, 0), (0, 1)), (TR, (1, 0), (0, 1)),
                        (BL, (-1, 0), (0, -1)), (BR, (1, 0), (0, -1))):
            f.hook(p, o, b, 9)
        xd = TR[0] + 30
        f.dim(TR, BR, (xd, yT), (xd, yB), "1'-7\"")
        f.text(((TL[0] + TR[0]) / 2, yT - 22), '16"x8"')
        f.text(((BL[0] + BR[0]) / 2, yB + 24), '20"x14"')
        cx = (TL[0] + TR[0] + BL[0] + BR[0]) / 4
        H = yB - yT
        if up == 8:
            f.line((cx, yT + 0.47 * H), (cx, yT + 0.29 * H), thin=True)
            f._arrow(f.P((cx, yT + 0.29 * H)), (0, -1))
            f.text((cx, yT + 0.60 * H), "TOP")
            f.text((cx, yT + 0.75 * H), 'UP 8"')
        else:
            f.text((cx, yT + 0.33 * H), "TOP")
            f.text((cx, yT + 0.48 * H), 'UP 2"')
            f.line((cx, yT + 0.57 * H), (cx, yT + 0.75 * H), thin=True)
            f._arrow(f.P((cx, yT + 0.75 * H)), (0, 1))
        f.text((cx, 48), letter, size=big, bold=True)

    cd(592.0, 8, "C")
    cd(850.0, 2, "D")

    # ---- section view AA (left bottom)
    b1l, b1r, b1t = 40.0, 165.0, 400.0
    b1b = b1t + 14 * s
    f.line((b1l, b1t), (b1r, b1t))
    f.line((b1l, b1b), (b1r, b1b))
    f.zbreak((b1l, b1t), (b1l, b1b), 0.5)
    f.line((b1r, b1t), (b1r, b1b))
    f.line((b1r - 5, b1t), (b1r - 5, b1b), thin=True)
    f.text((108, b1t + 30), '14"x20"')
    b2l = b1r + 19 * s
    b2r = b2l + 100
    b2t = b1t - 2 * s
    b2b = b2t + 8 * s
    f.line((b2l, b2t), (b2r, b2t))
    f.line((b2l, b2b), (b2r, b2b))
    f.line((b2l, b2t), (b2l, b2b))
    f.line((b2l + 5, b2t), (b2l + 5, b2b), thin=True)
    f.zbreak((b2r, b2t), (b2r, b2b), 0.5, h=9, amp=9)
    f.text((b2l + 47, b2t + 21), '8"x16"')
    yd = b1b + 24
    f.dim((b1r, b1b), (b2l, b2b), (b1r, yd), (b2l, yd), "1'-7\"")
    ytx = 592
    for x, y0, label, anchor, tx in ((85.0, b1b, "7'-1\" TO FLOOR", "start", 12.0),
                                     (b2l + 62, b2b, "7'-9\" TO FLOOR", "middle", b2l + 62)):
        f.line((x, y0), (x, ytx - 16), thin=True)
        f._arrow(f.P((x, y0)), (0, -1))
        f.line((x, ytx + 16), (x, 772), thin=True)
        f.text((tx, ytx), label, anchor=anchor)
    f.text((234, 652), "SECTION")
    f.text((234, 682), "VIEW AA")

    # ---- plan view (right bottom)
    px = 20.0                    # plan view x offset
    wl, wr, wt, wb = 470.0 + px, 1036.0 + px, 352.0, 392.0
    f.poly([(wl, wt), (wr, wt), (wr, wb), (wl, wb)], closed=True)
    d1l = 494.6 + px
    d1r = d1l + 14 * s
    dt = wb + 9.5 * s
    d1b = dt + 20 * s
    f.line((d1l, dt), (d1r, dt))
    f.line((d1l, d1b), (d1r, d1b))
    f.zbreak((d1l, dt), (d1l, d1b), 0.5)
    f.line((d1r, dt), (d1r, d1b))
    f.hook((d1r - 3, dt), (0, -1), (-1, 0), 9)
    f.hook((d1r - 3, d1b), (0, 1), (-1, 0), 9)
    f.text(((d1l + d1r) / 2 + 7, dt + 0.56 * 20 * s), '20"x14"')
    d2l = d1r + 19 * s
    d2r = d2l + 13 * s
    d2b = dt + 16 * s
    f.line((d2l, dt), (d2r, dt))
    f.line((d2l, d2b), (d2r, d2b))
    f.line((d2l, dt), (d2l, d2b))
    f.zbreak((d2r, dt), (d2r, d2b), 0.5)
    f.hook((d2l + 3, dt), (0, -1), (1, 0), 9)
    f.hook((d2l + 3, d2b), (0, 1), (1, 0), 9)
    f.text(((d2l + d2r) / 2 - 2, dt + 0.55 * 16 * s), '16"x8"')
    for x in (d1l + 0.48 * (d1r - d1l), d2l + 0.52 * (d2r - d2l)):
        f.dim((x, wb), (x, dt), (x, wb), (x, dt), '9 1/2"', ext=(False, False))
    yd = d1b + 26
    f.dim((d1r, d1b), (d2l, d2b), (d1r, yd), (d2l, yd), "1'-7\"")
    yc = 752.0
    f.line((480 + px, yc), (880 + px, yc))
    f.poly([(480 + px, yc), (500 + px, yc - 38), (520 + px, yc)])
    f.poly([(840 + px, yc), (860 + px, yc - 38), (880 + px, yc)])
    f.text((680 + px, yc - 20), "PLAN VIEW")
    f.text((896 + px, yc - 20), "SECTION AA", anchor="start")
    return f


def t90_q50():
    """Offset with two elbows (12"R, 45 deg marks) and straight piece D; L between elbow centres."""
    f = Fig((30, 0, 1205, 885), 640)
    th = 30.0                                # elbow angle as drawn in the original (labelled 45 deg)
    R = 235.0                                # throat radius = duct depth (12")
    u = (math.sin(math.radians(th)), math.cos(math.radians(th)))
    t = (u[1], -u[0])
    Dl = 283.0
    C1 = (290.0, 185.0)
    C2 = vadd(vadd(C1, u, 3 * R), t, Dl)
    yl_top, yl_bot = C1[1] + R, C1[1] + 2 * R
    yu_bot, yu_top = C2[1] - R, C2[1] - 2 * R
    a1 = angle_of(u)                         # 60 deg (screen)
    # lower duct + elbow 1
    f.line((215, yl_top), (C1[0], yl_top))
    f.line((215, yl_bot), (C1[0], yl_bot))
    f.arc(C1, R, 90, a1)
    f.arc(C1, 2 * R, 90, a1)
    f.line(C1, vadd(C1, u, 2 * R))           # radial joint line drawn from the centre
    # straight piece D
    T1, H1 = vadd(C1, u, R), vadd(C1, u, 2 * R)
    f.line(T1, vadd(T1, t, Dl))
    f.line(H1, vadd(H1, t, Dl))
    M1 = vadd(C1, u, 1.5 * R)
    f.line(M1, vadd(M1, t, Dl), thin=True)
    Q1 = vadd(C1, u, 1.3 * R)
    f.dim(Q1, vadd(Q1, t, Dl), Q1, vadd(Q1, t, Dl), "D", ext=(False, False), size=24, bold=True)
    # elbow 2 + upper duct
    a2 = a1 + 180
    f.arc(C2, R, a2, 270)
    f.arc(C2, 2 * R, a2, 270)
    f.line(C2, vadd(C2, u, -2 * R))
    f.line((C2[0], yu_bot), (1000, yu_bot))
    f.line((C2[0], yu_top), (1000, yu_top))
    # centre verticals: L extension + 12"R radius + elbow end joint
    rlab = "12\"R"
    yt1 = 368.0
    h = f._half_break(rlab, f.fs, (0, 1)) / f.k
    f.line((C1[0], 35), (C1[0], yt1 - h), thin=True)
    f.line((C1[0], yt1 + h), (C1[0], yl_top), thin=True)
    f.line((C1[0], yl_top), (C1[0], yl_bot))
    f.arrow((C1[0], yl_top), (C1[0], yl_top - 50))
    f.text((C1[0], yt1), rlab)
    yt2 = 528.0
    f.line((C2[0], C2[1]), (C2[0], yt2 + h), thin=True)
    f.line((C2[0], yt2 - h), (C2[0], yu_bot), thin=True)
    f.line((C2[0], yu_bot), (C2[0], yu_top))
    f.line((C2[0], yu_top), (C2[0], 15), thin=True)
    f.arrow((C2[0], yu_bot), (C2[0], yu_bot + 50))
    f.text((C2[0], yt2), rlab)
    # 45 deg marks with leaders
    ra = 112.0
    f.angle(C1, ra, 90, a1, al=9)
    pa = pol(C1, ra, a1)
    f.leader([pa, (pa[0] + 40, pa[1] - 14), (pa[0] + 52, pa[1] - 14)], arrow=False)
    f.text((pa[0] + 58, pa[1] - 14), "45°", anchor="start")
    f.angle(C2, ra, 270, a2, al=9)
    pb = pol(C2, ra, a2)
    f.leader([pb, (pb[0] - 40, pb[1] + 14), (pb[0] - 52, pb[1] + 14)], arrow=False)
    f.text((pb[0] - 58, pb[1] + 14), "45°", anchor="end")
    # L
    f.dim((C1[0], 48), (C2[0], 48), (C1[0], 48), (C2[0], 48), "L", ext=(False, False), size=27, bold=True)
    # duct sizes
    f.text((165, 545), '12"x18"')
    f.text((1035, 300), '12"x18"')
    # elevations
    f.line((128, yl_bot), (203, yl_bot), thin=True)
    f.line((143, yl_bot), (143, 765), thin=True)
    f.arrow((143, yl_bot), (143, yl_bot + 50))
    f.text((143, 800), "8'-3\"")
    f.text((143, 838), "TO FLOOR")
    f.line((1012, yu_bot), (1112, yu_bot), thin=True)
    f.line((1085, yu_bot), (1085, 785), thin=True)
    f.arrow((1085, yu_bot), (1085, yu_bot + 50))
    f.text((1085, 820), "11'-8\"")
    f.text((1085, 858), "TO FLOOR")
    return f


def t90_q51():
    """Duct trim joint: riser 6"/35"/35"/A, R10" elbow, 12"x8", 12" transition, 6" of 8"x8" into wall."""
    f = Fig((20, 0, 1290, 1370), 560)
    ceil, xl, xr = 25.0, 215.0, 345.0
    wi, wo, wbot = 1035.0, 1072.0, 1356.0
    f.line((30, ceil), (wi, ceil))
    f.line((wi, ceil), (wi, wbot))
    f.line((wo, ceil - 14), (wo, wbot))   # outer wall line crosses the dimension's extension line, as printed
    joints = [ceil, 92.0, 467.0, 828.0, 1103.0]
    f.line((xl, ceil), (xl, joints[-1]))
    f.line((xr, ceil), (xr, joints[-1]))
    for y in joints[1:]:
        f.line((xl, y), (xr, y))
    C = (445.0, 1103.0)
    f.arc(C, 100, 180, 90)
    f.arc(C, 230, 180, 90)
    ht, hb = C[1] + 100, C[1] + 230
    f.line((C[0], ht), (860, ht))
    f.line((C[0], hb), (wi, hb))
    f.line((C[0], ht), (C[0], hb))
    f.line((860, ht), (860, hb))
    y8 = 1248.0
    f.line((860, ht), (978, y8))
    f.line((978, y8), (wi, y8))
    f.line((978, y8), (978, hb))
    cx = (xl + xr) / 2
    f.text((cx, 58), '6"')
    f.text((cx, 285), '35"')
    f.text((cx, 565), '35"')
    f.text((cx - 8, 705), '14" x 8"', rot=-90)
    f.text((640, 1282), '12" x 8"')
    f.text((919, 1290), '12"')
    f.text((1006, 1290), '6"')
    f.dim((xl, 828), (xl, 1103), (135, 828), (135, 1103), "A", gap=10)
    tip = pol(C, 100, 135)
    f.leader([tip, (418, 1137), (440, 1137)])
    f.text((446, 1137), 'R10"', anchor="start")
    f.leader([(1003, y8), (935, 1108), (885, 1108)])
    f.text((880, 1108), '8"x8"', anchor="end")
    yc = (y8 + hb) / 2
    f.dim((wi, ceil), (wi, yc), (1205, ceil), (1205, yc), "10'-0 1/2\"", tpos=(1205, 650), gap=6)
    return f


def t90_q54():
    """Brake angle measured with a square: 8-13/16" rise over 4-11/16" run, inside angle A."""
    f = Fig((0, 0, 1121, 785), 600)
    t = 12.0
    yb = 600.0
    xe = 795.0
    d = unit((-225.0, -570.0))               # slanted leg direction, bend -> top
    n = (-d[1], d[0])                        # toward the inside of the bend
    if n[0] < 0:
        n = (-n[0], -n[1])
    Bo = (248.0, yb)
    Ti0 = vadd(Bo, n, t)
    s_in = (Ti0[1] - (yb - t)) / -d[1]
    Bi = vadd(Ti0, d, s_in)
    To = vadd(Bo, d, (yb - 15.0) / -d[1])
    Ti = vadd(To, n, t)
    f.poly([Ti, To, Bo, (xe, yb), (xe, yb - t), Bi], closed=True)
    ytop = min(To[1], Ti[1])
    f.dim((Ti[0] + 18, ytop), (xe, yb), (1015, ytop), (1015, yb), "8-13/16\"", gap=8,
          tpos=(1015, 335))
    f.dim((To[0], To[1] + 12), Bo, (To[0], 715), (Bo[0], 715), "4-11/16\"", gap=10)
    a_leg = angle_of(d) % 360
    f.angle(Bi, 210, a_leg, 360, "A")
    return f


def _tri13_geom():
    P, R = (95.0, 405.0), (1020.0, 990.0)
    M = mid(P, R)
    r = dist(P, R) / 2
    Q = vadd(M, unit(vsub((540.0, 150.0), M)), r)   # exact right angle (Thales)
    return P, Q, R


def tri_q13():
    """Right triangle: hypotenuse 13.67", angle 52.4 deg, leg L (= T90 No.55)."""
    P, Q, R = _tri13_geom()
    f = Fig((0, 0, 1060, 1135), 520)
    f.poly([P, Q, R], closed=True)
    f.rt(Q, P, R, 18)
    n = lnorm(unit(vsub(Q, P)))              # up-left of PQ
    f.dim(P, Q, vadd(P, n, 114), vadd(Q, n, 114), "L", size=19)
    m = vmul(lnorm(unit(vsub(R, P))), -1)    # down-left of PR
    f.dim(P, R, vadd(P, m, 112), vadd(R, m, 112), '13.67"', size=19)
    f.angle(P, 262, angle_of(vsub(Q, P)), angle_of(vsub(R, P)), "52.4°", size=19)
    return f


def _tri14_geom():
    B, R = (230.0, 890.0), (1075.0, 355.0)
    M = mid(B, R)
    r = dist(B, R) / 2
    C = vadd(M, unit(vsub((680.0, 130.0), M)), r)
    return B, C, R


def tri_q14():
    """Right triangle: leg 18-5/8", hypotenuse 25-3/8", angle A (= T90 No.56)."""
    B, C, R = _tri14_geom()
    f = Fig((40, 20, 1176, 1018), 540)
    f.poly([B, C, R], closed=True)
    f.rt(C, B, R, 18)
    n = lnorm(unit(vsub(C, B)))
    f.dim(B, C, vadd(B, n, 130), vadd(C, n, 130), '18-5/8"', size=19)
    m = vmul(lnorm(unit(vsub(R, B))), -1)
    f.dim(B, R, vadd(B, m, 94), vadd(R, m, 94), '25-3/8"', size=19)
    a0 = angle_of(vsub(B, R)) % 360
    a1 = angle_of(vsub(C, R)) % 360
    f.angle(R, 285, a0, a1, "A", size=19)
    return f


def t90_q57():
    """Pattern symmetrical about the centre line: 3", 4-1/4", 10-3/8", 5", 7-1/4", 150 and 135 deg."""
    f = Fig((-115, 0, 1230, 1240), 600)
    s = 45.6                                  # px per inch in the original photo
    cl, yb = 560.0, 1030.0
    xb = 3 * s
    h1 = (10.375 - 4.25 / math.tan(math.radians(30))) * s
    y1 = yb - h1
    x2 = (3 + 4.25) * s
    y2 = yb - 10.375 * s
    y3 = y2 - 5 * s
    d45 = 7.25 * math.cos(math.radians(45)) * s
    x4, y4 = x2 + d45, y3 - d45
    right = [(cl + xb, yb), (cl + xb, y1), (cl + x2, y2), (cl + x2, y3), (cl + x4, y4)]
    left = [(2 * cl - x, y) for x, y in reversed(right)]
    f.poly(left + right, closed=True)
    f.centerline((cl, 8), (cl, 1228), pattern=(22 * f.u, 5 * f.u, 5 * f.u, 5 * f.u))
    # 3"
    f.dim((cl, yb), (cl + xb, yb), (cl, 1196), (cl + xb, 1196), '3"', ext=(False, True))
    # 4-1/4"
    f.dim((cl + xb, 945), (cl + x2, y2), (cl + xb, 945), (cl + x2, 945), '4-1/4"', ext=(False, True), gap=8)
    # 10-3/8"
    f.dim((cl + x2, y2), (cl + xb, yb), (955, y2), (955, yb), '10-3/8"', gap=8)
    # 5" (inside, left)
    f.dim((cl - x2, y3), (cl - x2, y2), (cl - 235, y3), (cl - 235, y2), '5"', gap=8)
    # 7-1/4" along the upper-left slant, offset outward (down-left)
    A, B = (cl - x4, y4), (cl - x2, y3)
    nrm = unit((-1.0, 1.0))
    f.dim(A, B, vadd(A, nrm, 120), vadd(B, nrm, 120), '7-1/4"')
    # angles
    V1 = (cl - xb, y1)
    a_sl = angle_of(vsub((cl - x2, y2), V1)) % 360
    f.angle(V1, 112, 90, a_sl, "150°", tpos=pol(V1, 112, 165))
    V2 = (cl + x2, y3)
    a_up = angle_of(vsub((cl + x4, y4), V2))
    f.angle(V2, 126, a_up, 90, "135°", tpos=pol(V2, 126, 22))
    return f


def t90_q75():
    """Triangle with height 8" and base 4" (apex overhangs the base, as drawn)."""
    f = Fig((90, 50, 570, 830), 420)
    f.fs, f.lw = 22, 2.4                      # tall, narrow figure: larger labels
    A, B1, B2 = (245.0, 85.0), (332.0, 688.0), (530.0, 688.0)
    f.poly([A, B1, B2], closed=True)
    f.dim((A[0] - 18, A[1]), (B1[0] - 25, B1[1]), (150, A[1]), (150, B1[1]), '8"', gap=6)
    f.dim(B1, B2, (B1[0], 772), (B2[0], 772), '4"', gap=12)
    return f


def t90_q76():
    """Box 11" x 5" x 8" in oblique view with hidden edges (= SMY2W2 Triangulation No.10)."""
    f = Fig((140, 65, 870, 905), 460)
    FTL, FTR, FBR, FBL = (170.0, 170.0), (558.0, 293.0), (558.0, 743.0), (170.0, 620.0)
    r = (125.0, -80.0)
    BTL, BTR, BBR, BBL = (vadd(p, r) for p in (FTL, FTR, FBR, FBL))
    f.poly([FTL, FTR, FBR, FBL], closed=True)
    f.poly([FTL, BTL, BTR, FTR])
    f.poly([BTR, BBR, FBR])
    dash = (8 * f.u, 5.5 * f.u)
    f.line(BTL, BBL, dash=dash, w=f.lw * 0.8)
    f.line(BBL, FBL, dash=dash, w=f.lw * 0.8)
    f.line(BBL, BBR, dash=dash, w=f.lw * 0.8)
    ru = unit(r)
    x8 = 785.0
    k1 = (x8 - BTR[0]) / ru[0]
    k2 = (x8 - BBR[0]) / ru[0]
    f.dim(BTR, BBR, vadd(BTR, ru, k1), vadd(BBR, ru, k2), '8"', gap=8)
    f.dim(FBL, FBR, (FBL[0], FBL[1] + 105), (FBR[0], FBR[1] + 105), '11"', gap=8)
    f.dim(FBR, BBR, (FBR[0], FBR[1] + 128), (BBR[0], BBR[1] + 128), '5"', gap=8)
    return f


# Side view of a 15 deg transition with a flat bottom; geometry in the pixels of each reference image.
#   zl / zr = left / right end break line: (top y, bottom y, y of the break), zh / za = break size (view units)
#   ref = horizontal reference line of the angle (start offset from the joint, end x)
#   ang = (dimension arc radius, arrow tail, text radius); dim = (y of LENGTH ?, gap)
T88 = dict(box=(0, 0, 1533, 708), width=640, yb=560.0, ytl=220.0, ytr=60.0,
           xj1=380.0, xj2=1055.0, xL=25.0, xR=1500.0, zl=(185, 610, 390), zr=(25, 610, 320), zh=None, za=None,
           rt=13, ref=(34, 760), ang=(340, 26, 352), dim=(665, 10),
           left=('24" x 12"', (190, 345)), right=('34" x 18"', (1235, 355)))
MON54 = dict(T88, box=(0, -6, 404, 196), yb=153.0, ytl=59.5, ytr=13.0,
             xj1=104.5, xj2=280.0, xL=14.5, xR=389.5, zl=(51, 178, 111.3), zr=(1, 165, 80.5), zh=9.5, za=11.5,
             rt=17.5, ref=(11.5, 199.5), ang=(88.5, 20, 88), dim=(183, 12.5),
             left=('24" x 12"', (53, 97)), right=('36" x 18"', (323, 93)))


def t90_q88(g=T88):
    """Transition 24"x12" -> 34"x18" (T90; Monday No.54: -> 36"x18"), flat bottom, 15 deg top, LENGTH ?."""
    f = Fig(g["box"], g["width"])
    yb, ytl, ytr = g["yb"], g["ytl"], g["ytr"]
    xj1, xj2, xL, xR = g["xj1"], g["xj2"], g["xL"], g["xR"]
    f.line((xL, yb), (xR, yb))
    f.line((xL, ytl), (xj1, ytl))
    f.line((xj1, ytl), (xj2, ytr))
    f.line((xj2, ytr), (xR, ytr))
    f.line((xj1, ytl), (xj1, yb))
    f.line((xj2, ytr), (xj2, yb))
    for x, (y0, y1, yz) in ((xL, g["zl"]), (xR, g["zr"])):
        f.zbreak((x, y0), (x, y1), (yz - y0) / float(y1 - y0), h=g["zh"], amp=g["za"])
    f.rt((xj1, yb), (xj1, ytl), (xj2, yb), g["rt"])
    f.line((xj1 + g["ref"][0], ytl), (g["ref"][1], ytl), thin=True)
    a_top = angle_of((xj2 - xj1, ytr - ytl))
    r, tail, rt = g["ang"]
    f.angle((xj1, ytl), r, a_top, 0, "15°", arrows="out", tail=tail,
            tpos=pol((xj1, ytl), rt, a_top / 2))
    yd, gap = g["dim"]
    f.dim((xj1, yb), (xj2, yb), (xj1, yd), (xj2, yd), "LENGTH ?", gap=gap)
    for s, p in (g["left"], g["right"]):
        f.text(p, s)
    return f


def t90_q89():
    """Cylinder, 14" diameter, height to find (dimension left without a value, as printed)."""
    f = Fig((10, 0, 560, 610), 480)
    c1, c2, rx, ry = (274.0, 160.0), (274.0, 512.0), 104.0, 86.0
    f.ellipse(c1, rx, ry)
    f.line((c1[0] - rx, c1[1]), (c2[0] - rx, c2[1]))
    f.line((c1[0] + rx, c1[1]), (c2[0] + rx, c2[1]))
    f.ellipse_arc(c2, rx, ry, 180, 0)
    x = 52.0
    f.line((150, c1[1]), (24, c1[1]), thin=True)
    f.line((150, c2[1]), (24, c2[1]), thin=True)
    gy, gh = 345.0, 22.0
    f.line((x, c1[1]), (x, gy - gh), thin=True)
    f.line((x, gy + gh), (x, c2[1]), thin=True)
    f.arrow((x, c1[1]), (x, c1[1] + 40))
    f.arrow((x, c2[1]), (x, c2[1] - 40))
    tx = 345.0
    ty = c1[1] - ry * math.sqrt(1 - ((tx - c1[0]) / rx) ** 2)
    f.leader([(tx, ty), (450, 36), (464, 36)])
    f.text((470, 36), '14" Ø', anchor="start")
    return f


def t90_q90():
    """Concrete section, outside wall angle A and inside angle B (to scale, inches)."""
    def Q(x, y):
        return (x, -y)

    f = Fig((-9, -68, 206, 29), 640)
    t = 6.0
    xo, top_out, xt = 126.0, 54.25, 173.25
    top = 62.0
    A_deg = math.degrees(math.atan2(top_out, xt - xo))
    u = (math.cos(math.radians(A_deg)), math.sin(math.radians(A_deg)))
    nrm = (-u[1], u[0])
    p0 = (xo + t * nrm[0], t * nrm[1])
    s_c = (t - p0[1]) / u[1]
    xi = p0[0] + s_c * u[0]
    s_t = (xt - t - p0[0]) / u[0]
    yi_top = p0[1] + s_t * u[1]
    outer = [Q(0, top), Q(0, 0), Q(xo, 0), Q(xt, top_out), Q(xt, top)]
    inner = [Q(t, top), Q(t, t), Q(xi, t), Q(xt - t, yi_top), Q(xt - t, top)]
    f.concrete(outer + list(reversed(inner)), seed=11, n_tri=26, n_dot=120)
    f.poly(outer)
    f.poly(inner)
    f.dim(Q(0, 0), Q(xo, 0), Q(0, -10), Q(xo, -10), "10'-6\"")
    f.dim(Q(0, 0), Q(xt, top_out), Q(0, -21), Q(xt, -21), "14'-5 1/4\"", gap=10)
    f.dim(Q(xt, top_out), Q(xo, 0), Q(194, top_out), Q(194, 0), "4'-6 1/4\"", gap=5)
    f.angle(Q(xo, 0), 32, -A_deg, 0, "A")
    f.angle(Q(xi, t), 19, 180, 360 - A_deg, "B")
    return f


# ================================================================ Triangulation figures
def tri_q09():
    """Flat oval: R4" ends, 10" between centres."""
    f = Fig((30, 40, 1430, 790), 620)
    c1, c2, R = (448.0, 393.0), (1043.0, 393.0), 238.0
    f.line((c1[0], c1[1] - R), (c2[0], c2[1] - R))
    f.line((c1[0], c1[1] + R), (c2[0], c2[1] + R))
    f.arc(c1, R, 90, 270)
    f.arc(c2, R, -90, 90)
    f.centerline((50, c1[1]), (1405, c1[1]), centers=(c1, c2))
    for c in (c1, c2):
        f.centerline((c[0], 65), (c[0], 760), centers=(c,))
    tip = pol(c1, R, -146.4)
    f.leader([tip, c1])
    f.text((168, 238), 'R4"', size=22)
    f.dim((c1[0], 718), (c2[0], 718), (c1[0], 718), (c2[0], 718), '10"', ext=(False, False), size=22)
    return f


def tri_q11():
    """Right triangle: hypotenuse 15", vertical leg 9", angle A."""
    f = Fig((30, 5, 905, 595), 600)
    A, C, B = (150.0, 35.0), (705.0, 35.0), (705.0, 435.0)
    f.poly([A, C, B], closed=True)
    f.rt(C, A, B, 13)
    f.text((272, 76), "A", size=20)
    m = vmul(lnorm(unit(vsub(B, A))), -1)
    f.dim(A, B, vadd(A, m, 108), vadd(B, m, 108), '15"', size=20)
    f.dim(C, B, (830, C[1]), (830, B[1]), '9"', size=20, gap=14)
    return f


def tri_q12():
    """Right triangle: hypotenuse 19', angle 73 deg at the bottom, side a."""
    f = Fig((40, 25, 1250, 860), 600)
    C, T, B = (285.0, 75.0), (1095.0, 75.0), (285.0, 655.0)
    f.poly([C, T, B], closed=True)
    f.rt(C, T, B, 14)
    f.angle(B, 235, -90, angle_of(vsub(T, B)), "73°", tbreak=False, tpos=(450, 350), size=22)
    f.dim((210, C[1]), (210, B[1]), (150, C[1]), (150, B[1]), "a", size=22, gap=0)
    m = vmul(lnorm(unit(vsub(T, B))), -1)
    f.dim(B, T, vadd(B, m, 142), vadd(T, m, 142), "19'", size=22)
    return f


def tri_q17():
    """Offset with two 37 deg elbows, R1'-4" throats, 28"x20" duct; find L and D."""
    f = Fig((-25, 0, 1269, 935), 640)
    th = 37.0
    u = (math.sin(math.radians(th)), math.cos(math.radians(th)))
    t = (u[1], -u[0])
    Rt, Wd, Ls = 224.0, 215.0, 376.0
    Rh = Rt + Wd
    C1 = (270.0, 246.0)
    C2 = vadd(vadd(C1, u, 2 * Rt + Wd), t, Ls)
    a1 = angle_of(u)
    yl_t, yl_b = C1[1] + Rt, C1[1] + Rh
    yu_b, yu_t = C2[1] - Rt, C2[1] - Rh
    xL, xR = 165.0, 1068.0
    # lower duct, elbow 1
    f.line((xL, yl_t), (C1[0], yl_t))
    f.line((xL, yl_b), (C1[0], yl_b))
    f.zbreak((xL, yl_t - 25), (xL, yl_b + 20), 0.5, h=13, amp=14)
    f.line((C1[0], yl_t), (C1[0], yl_b))
    f.arc(C1, Rt, 90, a1)
    f.arc(C1, Rh, 90, a1)
    J1t, J1h = vadd(C1, u, Rt), vadd(C1, u, Rh)
    f.line(J1t, J1h)
    # straight
    J2h, J2t = vadd(J1t, t, Ls), vadd(J1h, t, Ls)
    f.line(J1t, J2h)
    f.line(J1h, J2t)
    f.line(J2h, J2t)
    # elbow 2, upper duct
    a2 = a1 + 180
    f.arc(C2, Rt, a2, 270)
    f.arc(C2, Rh, a2, 270)
    f.line((C2[0], yu_t), (C2[0], yu_b))
    f.line((C2[0], yu_t), (xR, yu_t))
    f.line((C2[0], yu_b), (xR, yu_b))
    f.zbreak((xR, yu_t - 22), (xR, yu_b + 20), 0.5, h=13, amp=14)
    # D
    f.dim((C1[0], yl_t - 20), (C2[0], yu_t - 12), (C1[0], 33), (C2[0], 33), "D")
    # L along the straight piece
    q1, q2 = mid(J1t, J1h, 0.55), mid(J2h, J2t, 0.55)
    f.dim(q1, q2, q1, q2, "L", ext=(False, False))
    # radii
    tip1 = pol(C1, Rt, 67)
    f.leader([tip1, (327, 368), (340, 368)])
    f.text((346, 368), "R1'-4\"", anchor="start")
    tip2 = pol(C2, Rt, 247)
    f.leader([tip2, (912, 430), (926, 430)])
    f.text((932, 430), "R1'-4\"", anchor="start")
    # 37 deg
    f.angle(C2, 324, a2, 270, "37°")
    f.angle(C1, 334, 78, 90, ends=(False, True))
    f.text(pol(C1, 336, 71), "37°")
    # elevations
    f.line((228, yl_b), (228, 842), thin=True)
    f.arrow((228, yl_b), (228, yl_b + 40))
    f.text((234, 878), "9'-5\"")
    f.text((234, 912), "To the Floor")
    f.line((1048, yu_b), (1048, 500), thin=True)
    f.arrow((1048, yu_b), (1048, yu_b + 40))
    f.text((1046, 528), "12'-1\"")
    f.text((1046, 562), "To the Floor")
    f.text((62, 603), '28" x 20"')
    f.text((1172, 183), '28" x 20"')
    return f


# ======================================================= SMY2W2 Monday Written figures
# Model coordinates = pixels of the images embedded in msg_993_Monday_Written_SMY2W2_Answers.pdf.
def mon_q42():
    """Plan: wall, W-column on its centre line, two 16"x12" ducts; 6'-8 5/8", 2'-2 3/4", 2'-1 1/4"."""
    f = Fig((0, 0, 256, 203), 620)
    for x in (5.5, 21.5):                                    # wall
        f.line((x, 0), (x, 203))
    xc = 240.0                                               # column centre line
    f.centerline((xc, 0), (xc, 113))
    for y0 in (38.0, 79.0):                                  # W-column in plan: flanges + web
        f.poly([(232, y0), (249, y0), (249, y0 + 3.5), (232, y0 + 3.5)], closed=True, w=f.lw * 0.75)
    for x in (238.5, 241.5):
        f.line((x, 41.5), (x, 79), w=f.lw * 0.75)
    # upper duct, cut at the top
    f.poly([(124.5, 40), (124.5, 93.5), (168.5, 93.5), (168.5, 40)])
    f.zbreak((121, 40), (171.5, 40), (145.5 - 121) / 50.5, h=10, amp=14)
    f.text((146.5, 77), '16" x 12"')
    # lower duct, cut at the bottom
    f.poly([(68, 193.5), (68, 160), (112, 160), (112, 193.5)])
    f.zbreak((65, 193.5), (115.5, 193.5), (90 - 65) / 50.5, h=10, amp=14)
    f.text((90, 176), '16" x 12"')
    f.dim((21.5, 20.5), (xc, 20.5), (21.5, 20.5), (xc, 20.5), "6'-8 5/8\"", ext=(False, False))
    f.dim((168.5, 93.5), (xc, 109.5), (168.5, 109.5), (xc, 109.5), "2'-2 3/4\"", ext=(True, False), gap=8)
    f.dim((21.5, 141.5), (90, 160), (21.5, 141.5), (90, 141.5), "2'-1 1/4\"", ext=(False, True), gap=7)
    return f


def mon_q43():
    """Right triangle: base 94 3\\8" (printed with a backslash), 72.4 deg at the top, vertical side x."""
    f = Fig((0, 2, 272, 182), 560)
    fs = 21
    BL, BR, T = (19.0, 128.5), (187.5, 128.5), (187.5, 15.5)
    f.poly([BL, BR, T], closed=True)
    f.dim(T, BR, (245, T[1]), (245, BR[1]), "x", gap=9, size=fs + 2)
    f.dim(BL, BR, (BL[0], 157), (BR[0], 157), '94 3\\8"', gap=7, size=fs)
    a_h = angle_of(vsub(BL, T))
    r = 58.5
    f.angle(T, r, 90, a_h, al=11)
    tip = pol(T, r, a_h)
    f.leader([tip, (131, 35), (121, 35)], arrow=False)
    f.text((117, 35), "72.4°", anchor="end", size=fs)
    return f


def mon_q44():
    """Right triangle: base 43.922", vertical side 14.375", angle theta at the left end of the base."""
    f = Fig((8, -4, 302, 192), 600)
    fs = 21
    BL, BR, T = (29.5, 136.5), (224.0, 136.5), (224.0, 6.5)
    f.poly([BL, BR, T], closed=True)
    f.dim(T, BR, (268.5, T[1]), (268.5, BR[1]), '14.375"', gap=12, size=fs)
    f.dim(BL, BR, (BL[0], 169), (BR[0], 169), '43.922"', gap=12, size=fs)
    a_h = angle_of(vsub(T, BL))
    r = 79.5
    f.angle(BL, r, a_h, 0, al=11)
    tip = pol(BL, r, a_h)
    f.leader([tip, (87, 80.5), (71, 80.5)], arrow=False)
    f.text((62, 82), "θ", size=fs + 3)
    return f


def mon_q45():
    """Right triangle: sides 132 3\\16" and 94 3\\16" (printed with backslashes), angle theta."""
    f = Fig((4, 4, 176, 198), 440)
    fs = 20
    V, T = (33.1, 171.1), (80.7, 40.1)
    M, r = mid(V, T), dist(V, T) / 2
    R = vadd(M, unit(vsub((127.0, 102.6), M)), r)              # exact right angle (Thales)
    f.poly([V, T, R], closed=True)
    n = unit(vsub(R, V))                                     # along V-R, away from V
    f.dim(T, R, vadd(T, n, 38.8), vadd(R, n, 38.8), '132 3\\16"', size=fs, bold=True, gap=5)
    m = unit(vsub(R, T))                                     # along T-R, away from T
    f.dim(V, R, vadd(V, m, 19.3), vadd(R, m, 19.3), '94 3\\16"', size=fs, bold=True, gap=5)
    a_vr, a_vt = angle_of(vsub(R, V)), angle_of(vsub(T, V))
    rr = 52.0
    f.angle(V, rr, a_vr, a_vt, al=10)
    tip = pol(V, rr, a_vt)
    f.leader([tip, (34, 120.3)], arrow=False)
    f.text((26.5, 120.5), "θ", size=fs + 3, bold=True)
    return f


def mon_q54():
    """Transition 24"x12" -> 36"x18", flat bottom, 15 deg top, LENGTH ? (T90 No.88 layout, other size)."""
    return t90_q88(MON54)


def mon_q57():
    """Offset in 36" round pipe: two 44 deg elbows (drawn at 37 deg), R38" throats; find L and D."""
    f = Fig((0, 3, 236, 199), 600)
    th = 37.0                                                # elbow angle as drawn (labelled 44 deg)
    u = (math.sin(math.radians(th)), math.cos(math.radians(th)))
    t = (u[1], -u[0])
    Rt, Wd, Ls = 42.5, 43.0, 74.5
    Rh, Rc = Rt + Wd, Rt + Wd / 2
    C1 = (50.0, 58.5)
    C2 = vadd(vadd(C1, u, 2 * Rt + Wd), t, Ls)
    a1 = angle_of(u)
    yl_t, yl_b = C1[1] + Rt, C1[1] + Rh
    yu_b, yu_t = C2[1] - Rt, C2[1] - Rh
    xL, xR = 28.5, 207.5
    # lower pipe, elbow 1
    f.line((xL, yl_t), (C1[0], yl_t))
    f.line((xL, yl_b), (C1[0], yl_b))
    f.zbreak((xL, yl_t - 4), (xL, yl_b + 4), (121.5 - yl_t + 4) / (Wd + 8), h=14, amp=18)
    f.line((C1[0], yl_t), (C1[0], yl_b))
    f.arc(C1, Rt, 90, a1)
    f.arc(C1, Rh, 90, a1)
    J1t, J1h = vadd(C1, u, Rt), vadd(C1, u, Rh)
    f.line(J1t, J1h)
    # straight piece
    J2h, J2t = vadd(J1t, t, Ls), vadd(J1h, t, Ls)
    f.line(J1t, J2h)
    f.line(J1h, J2t)
    f.line(J2h, J2t)
    # elbow 2, upper pipe
    a2 = a1 + 180
    f.arc(C2, Rt, a2, 270)
    f.arc(C2, Rh, a2, 270)
    f.line((C2[0], yu_t), (C2[0], yu_b))
    f.line((C2[0], yu_t), (xR, yu_t))
    f.line((C2[0], yu_b), (xR, yu_b))
    f.zbreak((xR, yu_t - 6), (xR, yu_b + 3), (51.5 - yu_t + 6) / (Wd + 9), h=14, amp=18)
    # D
    f.dim((C1[0], yl_t), (C2[0], yu_t), (C1[0], 14), (C2[0], 14), "D", gap=10)
    # L along the centre line of the straight piece, 44 deg arcs on the elbow centre lines
    q1 = vadd(C1, u, Rc)
    q2 = vadd(q1, t, Ls)
    f.dim(q1, q2, q1, q2, "L", ext=(False, False))
    f.angle(C1, Rc, 90, a1, "44°")
    f.angle(C2, Rc, a2, 270, "44°")
    # radii
    tip1 = pol(C1, Rt, 67)
    f.leader([tip1, (60.5, 81.5), (63, 81.5)])
    f.text((64.5, 81.5), 'R38"', anchor="start")
    tip2 = pol(C2, Rt, 246)
    f.leader([tip2, (176.5, 94.5), (184, 94.5)])
    f.text((185.5, 94.5), 'R38"', anchor="start")
    # pipe size at the cut ends
    f.text((13.5, 128), '36"Ø')
    f.text((222, 45), '36"Ø')
    # elevations
    f.line((40.5, yl_b), (40.5, 180), thin=True)
    f.arrow((40.5, yl_b), (40.5, yl_b + 12))
    f.text((40.5, 185), "8'-9\"")
    f.text((40.5, 192.5), "To the Floor")
    f.line((203.5, yu_b), (203.5, 109), thin=True)
    f.arrow((203.5, yu_b), (203.5, yu_b + 12))
    f.text((203.5, 113.5), "15'-2\"")
    f.text((203.5, 121), "To the Floor")
    return f


def mon_q58():
    """Transition in plan: 8"x12" -> 16"x6", 15" long, left side square, FOT; S&D hooks at the corners."""
    f = Fig((10, 8, 242, 190), 560)
    fs = 22
    xl, xt, xb = 49.5, 137.0, 224.5
    yt0, yt1, yb0, yb1 = 32.5, 43.5, 154.5, 165.0
    f.poly([(xl, yt0), (xt, yt0), (xt, yt1), (xl, yt1)], closed=True)       # top connection
    f.poly([(xl, yb0), (xb, yb0), (xb, yb1), (xl, yb1)], closed=True)       # bottom connection
    f.line((xl, yt1), (xl, yb0))
    f.line((xt, yt1), (xb, yb0))
    f.rt((xl, yb0), (xl, yt1), (xb, yb0), 26)
    s = 13
    f.hook((xl, 37), (-1, 0), (0, 1), s)
    f.hook((xt, 37), (1, 0), (0, 1), s)
    f.hook((xl, 160), (-1, 0), (0, -1), s)
    f.hook((xb, 160), (1, 0), (0, -1), s)
    f.dim((41, 36.5), (41, 159.5), (29.5, 36.5), (29.5, 159.5), '15"', gap=1, ovr=20, size=fs)
    f.text((93, 24), '8" x 12"', size=fs)
    f.text((132, 178.5), '16" x 6"', size=fs)
    f.text((107, 98), "FOT", size=fs + 2)
    return f


def mon_q70():
    """Six candidate break-line symbols A-F on a rectangle (as printed; the answer is not marked)."""
    f = Fig((5, 8, 222, 190), 600)
    big = 30
    dash = (11 * f.u, 4 * f.u)
    # A: right end dashed
    f.poly([(90.5, 17.5), (15.5, 17.5), (15.5, 60.5), (90.5, 60.5)])
    f.line((90.5, 17.5), (90.5, 60.5), dash=dash)
    f.text((52, 39), "A", size=big)
    # B: dashed line inside, pointed at by a leader
    f.poly([(15.5, 75.5), (90.5, 75.5), (90.5, 119), (15.5, 119)], closed=True)
    f.line((75.5, 75.5), (75.5, 119), dash=dash)
    f.leader([(75.5, 97.8), (57, 109.5), (38.5, 109.5)])
    f.text((52, 98), "B", size=big)
    # C: jagged end
    f.poly([(90.5, 135.5), (15.5, 135.5), (15.5, 178), (81, 178)])
    f.poly([(90.5, 135.5), (82.5, 143), (90.5, 150.5), (82, 159.5), (90.5, 168.5), (81, 178)])
    f.text((52, 157), "C", size=big)
    # D: V cut into the right end
    f.poly([(129.5, 17.5), (204.5, 17.5), (204.5, 60.5), (129.5, 60.5)], closed=True)
    f.poly([(204.5, 17.5), (195.5, 38.5), (204.5, 60.5)])
    f.text((165, 38.5), "D", size=big)
    # E: long break line, runs past both edges, one zigzag
    f.poly([(204, 75), (129.5, 75), (129.5, 119.5), (204, 119.5)])
    f.poly([(204, 72), (204, 92.5), (199, 95.3), (209.5, 99.2), (204, 101.5), (204, 122.5)])
    f.text((165, 98), "E", size=big)
    # F: S-break (figure eight) at the right end
    f.poly([(204.5, 135.5), (129.5, 135.5), (129.5, 178.5), (204.5, 178.5)])

    def curve(p0, c1, c2, p1):
        a, b, c, d = (f.P(p) for p in (p0, c1, c2, p1))
        f._path(f"M{f2(a[0])},{f2(a[1])} C{f2(b[0])},{f2(b[1])} {f2(c[0])},{f2(c[1])} {f2(d[0])},{f2(d[1])}", f.lw)

    curve((204.5, 135.5), (209.5, 140), (209.5, 151), (205, 155.5))
    curve((205, 155.5), (199, 160), (197.5, 172), (204.5, 178.5))
    curve((205, 155.5), (210, 159), (210.5, 172), (204.5, 178.5))
    f.text((165, 157), "F", size=big)
    return f


def mon_q76():
    """= T90 No.40 / Monday No.24 drawing, but FOT is written in A and FOB in B (swapped, as printed)."""
    return t90_q40(("FOT", "FOB"))


FIGS = {
    "t90-q25": t90_q25,
    "t90-q27": t90_q27,
    "t90-q40": t90_q40,
    "t90-q50": t90_q50,
    "t90-q51": t90_q51,
    "t90-q54": t90_q54,
    "t90-q55": tri_q13,     # same drawing as Triangulation No.13
    "t90-q56": tri_q14,     # same drawing as Triangulation No.14
    "t90-q57": t90_q57,
    "t90-q75": t90_q75,
    "t90-q76": t90_q76,
    "t90-q88": t90_q88,
    "t90-q89": t90_q89,
    "t90-q90": t90_q90,
    "tri-q09": tri_q09,
    "tri-q10": t90_q76,     # same drawing as T90 No.76
    "tri-q11": tri_q11,
    "tri-q12": tri_q12,
    "tri-q13": tri_q13,
    "tri-q14": tri_q14,
    "tri-q17": tri_q17,
    "mon-q33": t90_q75,     # same drawing as T90 No.75
    "mon-q34": t90_q76,     # same drawing as T90 No.76 / Triangulation No.10
    "mon-q40": tri_q09,     # same drawing as Triangulation No.9
    "mon-q42": mon_q42,
    "mon-q43": mon_q43,
    "mon-q44": mon_q44,
    "mon-q45": mon_q45,
    "mon-q54": mon_q54,     # T90 No.88 layout, 36"x18" instead of 34"x18"
    "mon-q56": tri_q17,     # same drawing as Triangulation No.17
    "mon-q57": mon_q57,
    "mon-q58": mon_q58,
    "mon-q70": mon_q70,
    "mon-q76": mon_q76,     # T90 No.40 with FOB/FOT swapped
}


def main(names):
    OUT.mkdir(parents=True, exist_ok=True)
    for name in names or FIGS:
        fig = FIGS[name]()
        (OUT / f"{name}.svg").write_text(fig.svg(), encoding="utf-8")
        print(f"{name}.svg  viewBox {f2(fig.W)} x {f2(fig.H)}")


if __name__ == "__main__":
    main(sys.argv[1:])
