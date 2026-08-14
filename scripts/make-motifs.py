#!/usr/bin/env python3
"""
לוח חרוט לכל תחום עיסוק — נוצר מתמטית באותה שפה ויזואלית של הגיליוש.
לא אייקונים ולא קליפארט: קומפוזיציות קו בקנה מידה גדול, שמשמשות רקע לכותרת העמוד.
הרצה:  python3 scripts/make-motifs.py  →  assets/motif-*.svg
"""
import math, os
OUT = os.path.join(os.path.dirname(__file__), '..', 'assets')
os.makedirs(OUT, exist_ok=True)
S = '#CDD4CE'
W, H = 900, 640
CX, CY = W / 2, H / 2


def wrap(body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">{body}</svg>'

def ln(x1, y1, x2, y2, op=.4, lw=1):
    return f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{S}" stroke-width="{lw}" opacity="{op:.2f}"/>'

def ci(cx, cy, r, op=.4, lw=1):
    return f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}" fill="none" stroke="{S}" stroke-width="{lw}" opacity="{op:.2f}"/>'

def rc(x, y, w, h, op=.4, lw=1, rx=0):
    return f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{rx}" fill="none" stroke="{S}" stroke-width="{lw}" opacity="{op:.2f}"/>'

def poly(pts, op=.4, lw=1):
    return f'<polyline points="{" ".join(f"{x:.0f},{y:.0f}" for x, y in pts)}" fill="none" stroke="{S}" stroke-width="{lw}" opacity="{op:.2f}" stroke-linejoin="round"/>'

def rose(cx, cy, R, r, d, sc, op, lw, steps=1100):
    k = (R + r) / r
    span = 2 * math.pi * (r / math.gcd(int(R), int(r)))
    pts = [(cx + ((R + r) * math.cos(span * i / steps) - d * math.cos(k * span * i / steps)) * sc,
            cy + ((R + r) * math.sin(span * i / steps) - d * math.sin(k * span * i / steps)) * sc)
           for i in range(steps + 1)]
    return poly(pts, op, lw)


def seal():
    e = [rose(CX, CY, 210, 37, 110, .62, .5, .85), rose(CX, CY, 210, 37, 110, .44, .3, .7)]
    for r, o in ((250, .5), (240, .25), (168, .2)): e.append(ci(CX, CY, r, o))
    for i in range(72):
        a = i * math.pi / 36
        e.append(ln(CX + 252 * math.cos(a), CY + 252 * math.sin(a),
                    CX + (268 if i % 6 == 0 else 261) * math.cos(a),
                    CY + (268 if i % 6 == 0 else 261) * math.sin(a), .38 if i % 6 == 0 else .2))
    return wrap(''.join(e))


def ledger():
    e, x0, y0, w, h = [], 110, 90, 680, 460
    e.append(rc(x0, y0, w, h, .5, 1.3))
    for i in range(1, 16): e.append(ln(x0, y0 + h * i / 16, x0 + w, y0 + h * i / 16, .16))
    for c in (.14, .52, .70, .86): e.append(ln(x0 + w * c, y0, x0 + w * c, y0 + h, .3))
    e.append(ln(x0, y0 + h / 16, x0 + w, y0 + h / 16, .48, 1.4))
    for i in range(2, 16, 2):
        e.append(ln(x0 + w * .16, y0 + h * i / 16 - 9, x0 + w * .46, y0 + h * i / 16 - 9, .13, 3))
    e.append(ln(x0 + w * .70, y0 + h * 14 / 16, x0 + w, y0 + h * 14 / 16, .45, 1.4))
    return wrap(''.join(e))


def quill():
    e = []
    for k in range(9):
        t = k / 8
        pts = [(140 + 620 * u, CY + (200 - 330 * t) * math.sin(math.pi * u) * (1 - .35 * u))
               for u in [i / 90 for i in range(91)]]
        e.append(poly(pts, .34 - .02 * k, 1))
    e.append(ln(120, CY + 210, 780, CY + 210, .42, 1.3))
    return wrap(''.join(e))


def magnifier():
    e = [ci(CX - 40, CY - 30, 190, .5, 1.4), ci(CX - 40, CY - 30, 176, .22)]
    for i in range(-8, 9):
        y = CY - 30 + i * 21
        half = math.sqrt(max(0, 176 ** 2 - (i * 21) ** 2))
        e.append(ln(CX - 40 - half, y, CX - 40 + half, y, .13))
    for i in range(-8, 9):
        x = CX - 40 + i * 21
        half = math.sqrt(max(0, 176 ** 2 - (i * 21) ** 2))
        e.append(ln(x, CY - 30 - half, x, CY - 30 + half, .1))
    e.append(ln(CX + 95, CY + 105, CX + 250, CY + 245, .5, 4))
    e.append(ln(CX + 95, CY + 105, CX + 250, CY + 245, .3, 8))
    return wrap(''.join(e))


def parcel():
    e, x0, y0, w, h = [], 90, 80, 720, 480
    e.append(rc(x0, y0, w, h, .5, 1.4))
    cuts = [.22, .48, .61, .82]
    for c in cuts: e.append(ln(x0 + w * c, y0, x0 + w * c, y0 + h, .3))
    for c in (.3, .55, .78): e.append(ln(x0, y0 + h * c, x0 + w, y0 + h * c, .3))
    for c in (.36, .68): e.append(ln(x0 + w * .22, y0 + h * c, x0 + w * .48, y0 + h * c, .2))
    for i in range(26):
        e.append(ln(x0 + w * .48 + i * 6, y0 + h * .3, x0 + w * .48 + i * 6 - 16, y0 + h * .55, .12))
    e.append(ln(x0 - 26, y0 + h + 26, x0 + w + 26, y0 + h + 26, .45, 1.3))
    for i in range(0, 15):
        e.append(ln(x0 - 26 + i * (w + 52) / 14, y0 + h + 26, x0 - 26 + i * (w + 52) / 14, y0 + h + 34, .25))
    return wrap(''.join(e))


def mark():
    e = [rc(CX - 230, CY - 190, 460, 380, .45, 1.3), rc(CX - 216, CY - 176, 432, 352, .18)]
    e.append(rose(CX, CY, 180, 29, 96, .6, .5, .85))
    e.append(rose(CX, CY, 180, 29, 96, .4, .3, .7))
    e.append(ci(CX, CY, 156, .42))
    e.append(ci(CX, CY, 146, .18))
    for i in range(4):
        a = math.pi / 4 + i * math.pi / 2
        e.append(ln(CX + 200 * math.cos(a), CY + 160 * math.sin(a),
                    CX + 232 * math.cos(a), CY + 190 * math.sin(a), .3))
    return wrap(''.join(e))


def org():
    e, top = [], 110
    e.append(rc(CX - 62, top, 124, 54, .5, 1.3))
    e.append(ln(CX, top + 54, CX, top + 104, .35))
    e.append(ln(CX - 250, top + 104, CX + 250, top + 104, .35))
    for i, x in enumerate((CX - 250, CX, CX + 250)):
        e.append(ln(x, top + 104, x, top + 150, .35))
        e.append(rc(x - 56, top + 150, 112, 48, .42, 1.1))
        if i != 1:
            e.append(ln(x, top + 198, x, top + 240, .25))
            e.append(ln(x - 84, top + 240, x + 84, top + 240, .25))
            for xx in (x - 84, x + 84):
                e.append(ln(xx, top + 240, xx, top + 276, .25))
                e.append(rc(xx - 42, top + 276, 84, 40, .3))
    return wrap(''.join(e))


def chain():
    e = []
    for i in range(7):
        cx = 130 + i * 108
        e.append(f'<ellipse cx="{cx}" cy="{CY}" rx="78" ry="46" fill="none" stroke="{S}" stroke-width="1.4" opacity="{.45 - abs(i-3)*.04:.2f}"/>')
        e.append(f'<ellipse cx="{cx}" cy="{CY}" rx="64" ry="33" fill="none" stroke="{S}" stroke-width="1" opacity="{.2 - abs(i-3)*.015:.2f}"/>')
    e.append(ln(90, CY - 120, 810, CY - 120, .3, 1.2))
    e.append(ln(90, CY + 120, 810, CY + 120, .3, 1.2))
    return wrap(''.join(e))


def scale():
    e, top = [], 150
    e.append(ln(CX, top, CX, top + 300, .5, 1.4))
    e.append(ln(CX - 230, top + 60, CX + 230, top + 60, .5, 1.4))
    for s in (-1, 1):
        x = CX + s * 230
        e.append(ln(x, top + 60, x, top + 118, .35))
        e.append(f'<path d="M{x-92} {top+118} A92 92 0 0 0 {x+92} {top+118}" fill="none" stroke="{S}" stroke-width="1.3" opacity=".42"/>')
        e.append(f'<path d="M{x-78} {top+118} A78 78 0 0 0 {x+78} {top+118}" fill="none" stroke="{S}" stroke-width="1" opacity=".2"/>')
        e.append(ln(x - 92, top + 118, x + 92, top + 118, .3))
    e.append(ln(CX - 120, top + 300, CX + 120, top + 300, .5, 1.4))
    e.append(ci(CX, top + 42, 16, .35))
    return wrap(''.join(e))


def clock():
    e = [ci(CX, CY, 236, .48, 1.4), ci(CX, CY, 222, .2)]
    for i in range(60):
        a = i * math.pi / 30 - math.pi / 2
        r2 = 200 if i % 5 == 0 else 210
        e.append(ln(CX + 222 * math.cos(a), CY + 222 * math.sin(a),
                    CX + r2 * math.cos(a), CY + r2 * math.sin(a), .38 if i % 5 == 0 else .16))
    for r, o in ((150, .16), (96, .12)): e.append(ci(CX, CY, r, o))
    e.append(ln(CX, CY, CX + 128 * math.cos(-math.pi / 3), CY + 128 * math.sin(-math.pi / 3), .45, 1.5))
    e.append(ln(CX, CY, CX + 186 * math.cos(math.pi / 9), CY + 186 * math.sin(math.pi / 9), .35, 1.2))
    return wrap(''.join(e))


def shield():
    e = []
    for k, (w, h, o) in enumerate(((210, 260, .5), (188, 234, .24), (166, 208, .14))):
        e.append(f'<path d="M{CX-w} {CY-h} L{CX+w} {CY-h} L{CX+w} {CY+h*.1} '
                 f'Q{CX+w} {CY+h*.72} {CX} {CY+h} Q{CX-w} {CY+h*.72} {CX-w} {CY+h*.1} Z" '
                 f'fill="none" stroke="{S}" stroke-width="{1.4 if k==0 else 1}" opacity="{o}"/>')
    for i in range(-6, 7):
        e.append(ln(CX + i * 30, CY - 250, CX + i * 30 + 70, CY + 250, .1))
    e.append(ln(CX - 210, CY - 150, CX + 210, CY - 150, .3))
    return wrap(''.join(e))


def compass():
    e = [ci(CX, CY, 244, .48, 1.4), ci(CX, CY, 230, .2), ci(CX, CY, 120, .18)]
    for i in range(32):
        a = i * math.pi / 16
        r2 = 190 if i % 8 == 0 else (208 if i % 4 == 0 else 218)
        e.append(ln(CX + 230 * math.cos(a), CY + 230 * math.sin(a),
                    CX + r2 * math.cos(a), CY + r2 * math.sin(a), .34 if i % 4 == 0 else .15))
    for i in range(4):
        a = i * math.pi / 2 - math.pi / 2
        b = a + math.pi / 4
        e.append(poly([(CX, CY), (CX + 46 * math.cos(b), CY + 46 * math.sin(b)),
                       (CX + 190 * math.cos(a), CY + 190 * math.sin(a)),
                       (CX + 46 * math.cos(b - math.pi / 2), CY + 46 * math.sin(b - math.pi / 2)),
                       (CX, CY)], .4, 1.1))
    return wrap(''.join(e))


M = dict(seal=seal, ledger=ledger, quill=quill, magnifier=magnifier, parcel=parcel, mark=mark,
         org=org, chain=chain, scale=scale, clock=clock, shield=shield, compass=compass)
for name, fn in M.items():
    svg = fn()
    open(os.path.join(OUT, f'motif-{name}.svg'), 'w').write(svg)
    print(f'motif-{name:12s} {len(svg)/1024:5.1f} KB')
